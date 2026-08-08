// Toy-diorama bake. Re-derives a chunky, miniature-model version of the city
// from the base pipeline's already-cleaned footprints (out/footprints.json) —
// nothing is downloaded or re-cleaned here.
//
//   out/toy/{cx}_{cz}.bin         version 3 building records (+ garnish, lore)
//   out/toystreets/{cx}_{cz}.bin  charcoal roads plus white edge ribbons
//   out/toyland/{cx}_{cz}.bin     base landcover with 1.5x park trees + roof trees
//   out/toy.json                  indexes, stats and validation numbers
//
// Dev loop: `node toy.mjs --cells=downtown,sunset` bakes two test cells only.

import { copyFile, mkdir, readFile, readdir, rm, writeFile } from 'node:fs/promises';
import earcut from 'earcut';
import { CELL_SIZE, GRID, cellIndex, cellOrigin, hash01, project } from './lib/geo.mjs';
import { ringArea, ringCentroid, simplifyRing } from './lib/poly.mjs';
import { frameRect, fromFrame, obbFrame, obbRing } from './lib/obb.mjs';
import { STREET_CLASSES } from './lib/classes.mjs';
import {
  TOY_ACCENT,
  TOY_BASE,
  TOY_EDGE_INSET,
  TOY_EDGE_LIFT,
  TOY_FLAG_GARNISH,
  TOY_FLAG_PITCHED,
  TOY_FLOOR,
  TOY_GARDEN,
  TOY_HELIPAD,
  TOY_HVAC,
  TOY_PALETTE,
  TOY_ROOFS,
  TOY_ROOF_RISE,
  TOY_SOLAR,
  TOY_TOWER_GLASS,
  toyStreetClasses,
} from './lib/toy.mjs';
import { writeBuildingsBlob, writeLandcoverBlob, writeStreetsBlob } from './lib/binio.mjs';
import { readLandcoverBlob, readStreetsBlob } from './lib/blobread.mjs';
import { CATS, NIGHT_PROFILE, SUPPRESS_BANDS } from './taxonomy.mjs';
import { countProps } from './props.mjs';

const OUT = new URL('./out/', import.meta.url);
const TOY_OUT = new URL('./out/toy/', import.meta.url);
const TOY_STREETS_OUT = new URL('./out/toystreets/', import.meta.url);
const TOY_LAND_OUT = new URL('./out/toyland/', import.meta.url);

const SIMPLIFY = 2.5;
const OBB_AREA = 80;
const PITCH_MAX_FLOORS = 4;
const PITCH_MAX_AREA = 300;
const MIN_HEIGHT = 7;
const MAX_HEIGHT = 200;
const MAX_HELIPADS = 6;
const TREE_MULTIPLIER = 1.5;
const STREET_REACH = 25; // a prop only faces a street this close (§2.4)
const MAX_VEHICLES = 4000;
const TOWER_FLOORS = 6;

// PROP.* bits, packed into bits 3..7 of the record flag byte.
const PROP_STREET = 1;
const PROP_VEHICLE = 2;
const PROP_TOWER = 4;
const PROP_CORNER = 8;
const PROP_HELIPAD = 16;
const PROP_SHIFT = 3;

// Categories that may park one vehicle at the kerb, in the order they get to
// claim from the citywide ration.
const VEHICLE_CATS = new Set(['fire_station', 'police', 'hospital', 'warehouse'].map((c) => CATS.indexOf(c)));

// Named dev cells: one downtown block and one Sunset block.
const TEST_CELLS = {
  downtown: [-122.401, 37.79],
  sunset: [-122.49, 37.753],
};

const arg = process.argv.slice(2).find((a) => a.startsWith('--cells='));
const onlyCells = arg
  ? new Set(
      arg
        .slice('--cells='.length)
        .split(',')
        .map((name) => {
          const lonlat = TEST_CELLS[name.trim()];
          if (!lonlat) throw new Error(`unknown dev cell "${name}"`);
          const idx = cellIndex(...project(lonlat[0], lonlat[1]));
          if (!idx) throw new Error(`dev cell "${name}" is outside the grid`);
          return idx.key;
        })
    )
  : null;
if (onlyCells) console.log(`dev bake, cells: ${[...onlyCells].join(', ')}`);

// Seeded, deterministic and stable per building: the same footprint always gets
// the same colour, roof and clutter across bakes.
function rnd(seed, salt) {
  return hash01(Math.imul(seed + 1, 0x9e3779b1) ^ Math.imul(salt + 1, 0x85ebca6b));
}

// ------------------------------------------------------------------ geometry ---

function orientRing(ring) {
  if (ringArea(ring) < 0) {
    const out = [];
    for (let i = ring.length - 2; i >= 0; i -= 2) out.push(ring[i], ring[i + 1]);
    return out;
  }
  return ring;
}

// ------------------------------------------------------------------ buildings ---

const source = JSON.parse(await readFile(new URL('footprints.json', OUT), 'utf8'));
console.log(`${source.buildings.length} cleaned base footprints`);

const cells = new Map();
function cellFor(x, z) {
  const idx = cellIndex(x, z);
  if (!idx) return null;
  if (onlyCells && !onlyCells.has(idx.key)) return null;
  let cell = cells.get(idx.key);
  if (!cell) {
    const [ox, oz] = cellOrigin(idx.cx, idx.cz);
    cells.set(idx.key, (cell = { key: idx.key, cx: idx.cx, cz: idx.cz, originX: ox, originZ: oz, buildings: [] }));
  }
  return cell;
}

// Emit one record: ring is triangulated for its roof/top face here so the
// runtime worker only extrudes.
function emit(cell, ring, baseY, topY, palette, seed, flags = 0, roofPalette = 0, lore = null) {
  const oriented = orientRing(ring);
  const indices = earcut(oriented);
  if (indices.length < 3) return;
  cell.buildings.push({
    ring: oriented,
    indices,
    baseY,
    topY,
    palette,
    seed,
    flags,
    roofPalette,
    cat: lore ? lore.cat : 0,
    yaw: lore ? lore.yaw : 0,
    night: lore ? lore.night : 12,
  });
}

// ---------------------------------------------------------------- street frame
// Props only make sense facing a street, so every building is matched to the
// nearest street centreline within 25 m. That segment's heading becomes the
// building's local `u` axis and decides which face is the front.
const STREET_GRID = 60;
const streetGrid = new Map();
const streetKey = (x, z) => `${Math.floor(x / STREET_GRID)}_${Math.floor(z / STREET_GRID)}`;

for (const file of (await readdir(new URL('streets/', OUT))).filter((f) => f.endsWith('.bin'))) {
  const blob = await readStreetsBlob(new URL(`streets/${file}`, OUT));
  for (const line of blob.lines) {
    for (let i = 0; i + 5 < line.pts.length; i += 3) {
      const x0 = line.pts[i];
      const z0 = line.pts[i + 2];
      const x1 = line.pts[i + 3];
      const z1 = line.pts[i + 5];
      const seg = [x0, z0, x1, z1];
      const steps = Math.max(1, Math.ceil(Math.hypot(x1 - x0, z1 - z0) / STREET_GRID));
      for (let s = 0; s <= steps; s++) {
        const key = streetKey(x0 + ((x1 - x0) * s) / steps, z0 + ((z1 - z0) * s) / steps);
        let bucket = streetGrid.get(key);
        if (!bucket) streetGrid.set(key, (bucket = []));
        bucket.push(seg);
      }
    }
  }
}

function nearestStreet(x, z) {
  let best = null;
  let bestD = Infinity;
  const gx = Math.floor(x / STREET_GRID);
  const gz = Math.floor(z / STREET_GRID);
  for (let dx = -1; dx <= 1; dx++) {
    for (let dz = -1; dz <= 1; dz++) {
      const bucket = streetGrid.get(`${gx + dx}_${gz + dz}`);
      if (!bucket) continue;
      for (const [x0, z0, x1, z1] of bucket) {
        const ex = x1 - x0;
        const ez = z1 - z0;
        const len2 = ex * ex + ez * ez || 1;
        const t = Math.max(0, Math.min(1, ((x - x0) * ex + (z - z0) * ez) / len2));
        const px = x0 + ex * t;
        const pz = z0 + ez * t;
        const d = Math.hypot(x - px, z - pz);
        if (d < bestD) {
          bestD = d;
          best = { px, pz, ex, ez, d };
        }
      }
    }
  }
  return best && best.d <= STREET_REACH ? best : null;
}

// The local frame: `u` runs along the street (or the footprint's long axis when
// there is no street), and `v` points away from it, into the block.
function loreFrame(ring, cx, cz) {
  const street = nearestStreet(cx, cz);
  let ux;
  let uz;
  if (street) {
    const len = Math.hypot(street.ex, street.ez) || 1;
    ux = street.ex / len;
    uz = street.ez / len;
    // Flip so that +v points away from the kerb: recipes build on the -v face.
    const toStreetV = -uz * (street.px - cx) + ux * (street.pz - cz);
    if (toStreetV > 0) {
      ux = -ux;
      uz = -uz;
    }
  } else {
    let longest = 0;
    ux = 1;
    uz = 0;
    for (let k = 0; k + 3 < ring.length; k += 2) {
      const dx = ring[k + 2] - ring[k];
      const dz = ring[k + 3] - ring[k + 1];
      const len = Math.hypot(dx, dz);
      if (len > longest) {
        longest = len;
        ux = dx / len;
        uz = dz / len;
      }
    }
  }
  let angle = Math.atan2(uz, ux);
  if (angle < 0) angle += Math.PI * 2;
  return { yaw: Math.round((angle / (Math.PI * 2)) * 256) & 255, street: Boolean(street) };
}

const roofTrees = [];
let helipads = 0;
let pitchedCount = 0;
let garnishCount = 0;
let tallestToy = 0;

// Garnish is axis-aligned to the roof's own OBB (A.3), inset from the edge.
function addGarnish(cell, frame, roofY, seed) {
  const lenU = frame.maxU - frame.minU;
  const lenV = frame.maxV - frame.minV;
  if (lenU < 6 || lenV < 6) return;
  const inset = 1.5;
  const u0 = frame.minU + inset;
  const u1 = frame.maxU - inset;
  const v0 = frame.minV + inset;
  const v1 = frame.maxV - inset;
  if (u1 - u0 < 3 || v1 - v0 < 3) return;

  const roll = rnd(seed, 11);
  if (roll < 0.4) {
    // HVAC: 1-3 grey boxes, 2 x 1.5 x 2.5 m.
    const units = 1 + Math.floor(rnd(seed, 12) * 3);
    for (let i = 0; i < units; i++) {
      const u = u0 + rnd(seed, 20 + i) * Math.max(0.01, u1 - u0 - 2);
      const v = v0 + rnd(seed, 30 + i) * Math.max(0.01, v1 - v0 - 2.5);
      emit(cell, frameRect(frame, u, u + 2, v, v + 2.5), roofY, roofY + 1.5, TOY_HVAC, seed, TOY_FLAG_GARNISH);
      garnishCount++;
    }
  } else if (roll < 0.55) {
    // Rooftop garden: a slab over a seeded ~40% corner patch, plus small trees.
    const cu = rnd(seed, 13) < 0.5 ? u0 : u1 - (u1 - u0) * 0.63;
    const cv = rnd(seed, 14) < 0.5 ? v0 : v1 - (v1 - v0) * 0.63;
    const pu = Math.min(u1, cu + (u1 - u0) * 0.63);
    const pv = Math.min(v1, cv + (v1 - v0) * 0.63);
    emit(cell, frameRect(frame, cu, pu, cv, pv), roofY, roofY + 0.3, TOY_GARDEN, seed, TOY_FLAG_GARNISH);
    garnishCount++;
    const trees = 2 + Math.floor(rnd(seed, 15) * 3);
    for (let i = 0; i < trees; i++) {
      const [x, z] = fromFrame(
        frame,
        cu + rnd(seed, 40 + i) * (pu - cu),
        cv + rnd(seed, 50 + i) * (pv - cv)
      );
      roofTrees.push([x, roofY + 0.3, z]);
    }
  } else if (roll < 0.65) {
    // Solar: a grid of 2 x 1 m panels over roughly half the roof.
    let panels = 0;
    for (let u = u0; u + 2 < u0 + (u1 - u0) * 0.72 && panels < 14; u += 2.3) {
      for (let v = v0; v + 1 < v0 + (v1 - v0) * 0.72 && panels < 14; v += 1.3) {
        emit(cell, frameRect(frame, u, u + 2, v, v + 1), roofY, roofY + 0.15, TOY_SOLAR, seed, TOY_FLAG_GARNISH);
        panels++;
        garnishCount++;
      }
    }
  }
}

function addHelipad(cell, cx, cz, roofY, seed) {
  const disc = (r, sides) => {
    const ring = [];
    for (let i = 0; i < sides; i++) {
      const a = (i / sides) * Math.PI * 2;
      ring.push(cx + Math.cos(a) * r, cz + Math.sin(a) * r);
    }
    return ring;
  };
  // White rim first, then the grey pad on top of it: a flat ring needs a hole,
  // which the single-ring record format cannot carry.
  emit(cell, disc(7, 14), roofY, roofY + 0.15, TOY_PALETTE.length - 1, seed, TOY_FLAG_GARNISH);
  emit(cell, disc(6, 14), roofY + 0.15, roofY + 0.3, TOY_HELIPAD, seed, TOY_FLAG_GARNISH);
  garnishCount += 2;
  helipads++;
}

// The identity join from stage 1: the toy bake reads it so a fire station gets
// bay doors and a church gets a steeple. Missing means `misc`, which is exactly
// the generic toy building the diorama shipped with.
const lore = JSON.parse(await readFile(new URL('lore.json', OUT), 'utf8'));

let vehicles = 0;
let propBuildings = 0;
let propTrianglesTotal = 0;
let propTrianglesMax = 0;
const catCounts = new Array(CATS.length).fill(0);

let buildingId = -1;
for (const [ringIn, height, baseY, seed] of source.buildings) {
  buildingId++;
  let ring = simplifyRing(ringIn, SIMPLIFY);
  if (ring.length / 2 < 3) ring = ringIn;
  let area = Math.abs(ringArea(ring));
  if (area < OBB_AREA) {
    ring = obbRing(ring);
    area = Math.abs(ringArea(ring));
  }

  const [cx, cz] = ringCentroid(ring);
  const cell = cellFor(cx, cz);
  if (!cell) continue;

  const floors = Math.max(2, Math.round(height / TOY_FLOOR));
  const toyHeight = Math.min(MAX_HEIGHT, Math.max(MIN_HEIGHT, floors * TOY_FLOOR));
  const pitched = floors < PITCH_MAX_FLOORS && area < PITCH_MAX_AREA;

  let palette;
  if (floors > 20) palette = TOY_TOWER_GLASS;
  else if (rnd(seed, 1 + Math.round(cx)) < 0.7) palette = TOY_BASE[Math.floor(rnd(seed, 2) * TOY_BASE.length)];
  else palette = TOY_ACCENT[Math.floor(rnd(seed, 3) * TOY_ACCENT.length)];

  // ---------------------------------------------------------------- identity
  const rec = lore[buildingId] || { cat: 0 };
  const cat = rec.cat || 0;
  catCounts[cat]++;
  const frame = loreFrame(ring, cx, cz);
  let props = 0;
  if (frame.street) props |= PROP_STREET;
  if (floors >= TOWER_FLOORS) props |= PROP_TOWER;
  // Corner lots read differently, and a few categories earn scarce extras: one
  // vehicle each until the citywide ration runs out, a helipad on big hospitals.
  if (frame.street && rnd(seed, 61) > 0.72) props |= PROP_CORNER;
  if (VEHICLE_CATS.has(cat) && frame.street && vehicles < MAX_VEHICLES) {
    props |= PROP_VEHICLE;
    vehicles++;
  }
  if (cat === CATS.indexOf('hospital') && area > 1200) props |= PROP_HELIPAD;
  const night = NIGHT_PROFILE[cat] * 4 + (SUPPRESS_BANDS.has(cat) ? 1 : 0);
  const loreRec = { cat, yaw: frame.yaw, night, props };
  const flagBits = (props << PROP_SHIFT) & 0xf8;

  if (pitched) {
    // Row houses: an OBB mass with walls to (floors - 1) * 3.5 and a ridge prism
    // generated in the worker from the four corners.
    const box = obbRing(ring);
    const wallH = Math.max(TOY_FLOOR, (floors - 1) * TOY_FLOOR);
    const roofPalette = TOY_ROOFS[Math.floor(rnd(seed, 4) * TOY_ROOFS.length)];
    emit(cell, box, baseY, baseY + wallH, palette, seed, TOY_FLAG_PITCHED | flagBits, roofPalette, loreRec);
    pitchedCount++;
    tallestToy = Math.max(tallestToy, wallH + TOY_ROOF_RISE);
    measureProps(box, cx, cz, baseY, baseY + wallH + TOY_ROOF_RISE, loreRec, seed);
  } else {
    const top = baseY + toyHeight;
    emit(cell, ring, baseY, top, palette, seed, flagBits, 0, loreRec);
    tallestToy = Math.max(tallestToy, toyHeight);
    addGarnish(cell, obbFrame(ring), top, seed + Math.round(cx));
    if (floors > 30 && helipads < MAX_HELIPADS) addHelipad(cell, cx, cz, top, seed);
    measureProps(ring, cx, cz, baseY, top, loreRec, seed);
  }
}

// The props themselves are generated in the tile worker, so the budget is
// audited here by running the identical recipes through a counting emitter.
function measureProps(ring, cx, cz, base, top, loreRec, seed) {
  const angle = (loreRec.yaw / 256) * Math.PI * 2;
  const ux = Math.cos(angle);
  const uz = Math.sin(angle);
  let hu = 0;
  let hv = 0;
  for (let k = 0; k + 1 < ring.length; k += 2) {
    const dx = ring[k] - cx;
    const dz = ring[k + 1] - cz;
    hu = Math.max(hu, Math.abs(dx * ux + dz * uz));
    hv = Math.max(hv, Math.abs(-dx * uz + dz * ux));
  }
  const triangles = countProps({
    cat: loreRec.cat,
    props: loreRec.props,
    sub: null,
    hu,
    hv,
    base,
    top,
    seed,
  });
  if (triangles === 0) return;
  propBuildings++;
  propTrianglesTotal += triangles;
  propTrianglesMax = Math.max(propTrianglesMax, triangles);
}

await rm(TOY_OUT, { recursive: true, force: true });
await mkdir(TOY_OUT, { recursive: true });
let toyBytes = 0;
let toyRecords = 0;
const toyIndex = [];
for (const key of [...cells.keys()].sort()) {
  const cell = cells.get(key);
  if (cell.buildings.length === 0) continue;
  const blob = writeBuildingsBlob(cell, { version: 3 });
  await writeFile(new URL(`${key}.bin`, TOY_OUT), blob);
  toyBytes += blob.length;
  toyRecords += cell.buildings.length;
  toyIndex.push({
    key,
    cx: cell.cx,
    cz: cell.cz,
    originX: cell.originX,
    originZ: cell.originZ,
    buildings: cell.buildings.length,
    bytes: blob.length,
  });
}
console.log(
  `toy buildings: ${toyRecords} records in ${toyIndex.length} cells, ${(toyBytes / 1e6).toFixed(1)} MB ` +
    `(${pitchedCount} pitched, ${garnishCount} garnish, ${helipads} helipads, tallest ${tallestToy.toFixed(0)} m)`
);
console.log(
  `lore props: ${propBuildings} buildings, avg ${(propTrianglesTotal / Math.max(1, propBuildings)).toFixed(1)} tris ` +
    `(cap ${propTrianglesMax}), ${vehicles} vehicles, ` +
    `${catCounts.map((n, i) => `${CATS[i]} ${n}`).filter((_, i) => catCounts[i] > 0).length} categories present`
);

// -------------------------------------------------------------------- streets ---
// The same polylines the base build ribbons, restyled charcoal, plus two white
// edge ribbons per road offset to ±(w/2 - 0.3) and lifted 0.02 m.

const TOY_STREET_CLASSES = toyStreetClasses(STREET_CLASSES);
const EDGE_CLASS = TOY_STREET_CLASSES.length - 1;

function offsetLine(pts, offset) {
  const n = pts.length / 3;
  const out = { pts: [], y: [] };
  for (let k = 0; k < n; k++) {
    let tx;
    let tz;
    if (k === 0) {
      tx = pts[3] - pts[0];
      tz = pts[5] - pts[2];
    } else if (k === n - 1) {
      tx = pts[(n - 1) * 3] - pts[(n - 2) * 3];
      tz = pts[(n - 1) * 3 + 2] - pts[(n - 2) * 3 + 2];
    } else {
      tx = pts[(k + 1) * 3] - pts[(k - 1) * 3];
      tz = pts[(k + 1) * 3 + 2] - pts[(k - 1) * 3 + 2];
    }
    const tl = Math.hypot(tx, tz) || 1;
    out.pts.push(pts[k * 3] + (tz / tl) * offset, pts[k * 3 + 2] - (tx / tl) * offset);
    out.y.push(pts[k * 3 + 1] + TOY_EDGE_LIFT);
  }
  return out;
}

const streetFiles = (await readdir(new URL('streets/', OUT))).filter((f) => f.endsWith('.bin'));
await rm(TOY_STREETS_OUT, { recursive: true, force: true });
await mkdir(TOY_STREETS_OUT, { recursive: true });
let toyStreetBytes = 0;
const toyStreetIndex = [];
for (const file of streetFiles.sort()) {
  const key = file.replace(/\.bin$/, '');
  if (onlyCells && !onlyCells.has(key)) continue;
  const [cx, cz] = key.split('_').map(Number);
  const [originX, originZ] = cellOrigin(cx, cz);
  const base = await readStreetsBlob(new URL(`streets/${file}`, OUT));
  const lines = [];
  for (const line of base.lines) {
    const n = line.pts.length / 3;
    const road = { pts: [], y: [], klass: line.klass, flags: line.flags };
    for (let k = 0; k < n; k++) {
      road.pts.push(line.pts[k * 3], line.pts[k * 3 + 2]);
      road.y.push(line.pts[k * 3 + 1]);
    }
    lines.push(road);
    const halfW = TOY_STREET_CLASSES[line.klass].width / 2 - TOY_EDGE_INSET;
    if (n >= 2 && halfW > 0.5) {
      for (const side of [halfW, -halfW]) {
        const edge = offsetLine(line.pts, side);
        lines.push({ ...edge, klass: EDGE_CLASS, flags: line.flags });
      }
    }
  }
  const blob = writeStreetsBlob({ key, cx, cz, originX, originZ, lines });
  await writeFile(new URL(`${key}.bin`, TOY_STREETS_OUT), blob);
  toyStreetBytes += blob.length;
  toyStreetIndex.push({ key, cx, cz, originX, originZ, lines: lines.length, bytes: blob.length });
}
console.log(
  `toy streets: ${toyStreetIndex.length} cells, ${(toyStreetBytes / 1e6).toFixed(1)} MB (roads + white edge ribbons)`
);

// ------------------------------------------------------------------ landcover ---
// Same polygons as the base build; only the tree scatter changes: 1.5x park
// density plus the rooftop garden trees the building bake produced.

const roofTreesByCell = new Map();
for (const [x, y, z] of roofTrees) {
  const idx = cellIndex(x, z);
  if (!idx) continue;
  if (!roofTreesByCell.has(idx.key)) roofTreesByCell.set(idx.key, []);
  roofTreesByCell.get(idx.key).push([x, y, z]);
}

const landFiles = (await readdir(new URL('landcover/', OUT))).filter((f) => f.endsWith('.bin'));
await rm(TOY_LAND_OUT, { recursive: true, force: true });
await mkdir(TOY_LAND_OUT, { recursive: true });
let toyLandBytes = 0;
let toyTrees = 0;
const toyLandIndex = [];
for (const file of landFiles.sort()) {
  const key = file.replace(/\.bin$/, '');
  if (onlyCells && !onlyCells.has(key)) continue;
  const [cx, cz] = key.split('_').map(Number);
  const [originX, originZ] = cellOrigin(cx, cz);
  const base = await readLandcoverBlob(new URL(`landcover/${file}`, OUT), { full: true });

  const trees = [];
  for (let i = 0; i < base.treeTotal; i++) {
    const x = base.trees[i * 3];
    const y = base.trees[i * 3 + 1];
    const z = base.trees[i * 3 + 2];
    trees.push(x, y, z, base.treeVariant[i]);
    // Extra half-density pass: a seeded 6 m nudge off every other tree.
    if (hash01(i * 2654435761 + cx * 977 + cz) < TREE_MULTIPLIER - 1) {
      const a = hash01(i * 40503 + 7) * Math.PI * 2;
      trees.push(x + Math.cos(a) * 6, y, z + Math.sin(a) * 6, base.treeVariant[i]);
    }
  }
  for (const [x, y, z] of roofTreesByCell.get(key) || []) trees.push(x, y, z, 2);

  const blob = writeLandcoverBlob({
    key,
    originX,
    originZ,
    verts: base.verts,
    kinds: base.kinds,
    indices: base.indices,
    trees,
  });
  await writeFile(new URL(`${key}.bin`, TOY_LAND_OUT), blob);
  toyLandBytes += blob.length;
  toyTrees += trees.length / 4;
  toyLandIndex.push({
    key,
    cx,
    cz,
    originX,
    originZ,
    triangles: base.triangles,
    trees: trees.length / 4,
    bytes: blob.length,
  });
}
console.log(`toy landcover: ${toyLandIndex.length} cells, ${toyTrees} trees, ${(toyLandBytes / 1e6).toFixed(1)} MB`);

// ------------------------------------------------------------------ manifest ---

await writeFile(
  new URL('toy.json', OUT),
  JSON.stringify(
    {
      cellSize: CELL_SIZE,
      grid: GRID,
      dev: onlyCells ? [...onlyCells] : null,
      palette: TOY_PALETTE,
      streetClasses: TOY_STREET_CLASSES,
      stats: {
        baseBuildings: source.buildings.length,
        records: toyRecords,
        pitched: pitchedCount,
        garnish: garnishCount,
        helipads,
        tallest: Math.round(tallestToy),
        trees: toyTrees,
        bytes: { buildings: toyBytes, streets: toyStreetBytes, landcover: toyLandBytes },
      },
      cells: toyIndex,
      streetCells: toyStreetIndex,
      landcoverCells: toyLandIndex,
    },
    null,
    1
  )
);

// ----------------------------------------------------------------- validation ---
// The toy tier must cover the same city as the near tier, stay under the toy
// height clamp, and never cost more bytes than the geometry it replaces.

const baseBuildings = JSON.parse(await readFile(new URL('buildings.json', OUT), 'utf8'));
const baseStreets = JSON.parse(await readFile(new URL('streets.json', OUT), 'utf8'));
const failures = [];
function check(label, ok, detail) {
  console.log(`  ${ok ? 'ok  ' : 'FAIL'} ${label} — ${detail}`);
  if (!ok) failures.push(label);
}

if (onlyCells) {
  console.log(`dev bake — skipping the citywide validation gate`);
} else {
  const toyBuildings = toyRecords - garnishCount;
  const drift = Math.abs(toyBuildings - baseBuildings.stats.total) / baseBuildings.stats.total;
  check(
    'toy building count within 1% of the near tier',
    drift <= 0.01,
    `${toyBuildings} toy / ${baseBuildings.stats.total} base (${(drift * 100).toFixed(2)}%)`
  );
  check('tallest toy building <= 200 m', tallestToy <= MAX_HEIGHT + 0.01, `${tallestToy.toFixed(1)} m`);
  check(
    'toy building payload <= near tier',
    toyBytes <= baseBuildings.stats.bytes,
    `${(toyBytes / 1e6).toFixed(1)} MB toy / ${(baseBuildings.stats.bytes / 1e6).toFixed(1)} MB base`
  );
  check(
    'toy street payload <= base streets x 3 (roads plus two edge ribbons)',
    toyStreetBytes <= baseStreets.stats.bytes * 3,
    `${(toyStreetBytes / 1e6).toFixed(1)} MB toy / ${(baseStreets.stats.bytes / 1e6).toFixed(1)} MB base`
  );
  if (failures.length) {
    console.error(`\nTOY VALIDATION FAILED: ${failures.join(', ')}`);
    process.exit(1);
  }
}

// ------------------------------------------------------------------- publish ---

const APP_TILES = new URL('../app/public/tiles/', import.meta.url);
for (const [dir, src] of [
  ['toy', TOY_OUT],
  ['toystreets', TOY_STREETS_OUT],
  ['toyland', TOY_LAND_OUT],
]) {
  const dst = new URL(`${dir}/`, APP_TILES);
  await rm(dst, { recursive: true, force: true });
  await mkdir(dst, { recursive: true });
  for (const f of await readdir(src)) await copyFile(new URL(f, src), new URL(f, dst));
}
await copyFile(new URL('toy.json', OUT), new URL('toy.json', APP_TILES));

console.log('wrote out/toy.json and published the toy tier to app/public/tiles/');
