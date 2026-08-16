// Export a slab of the REAL baked city as JSON for the in-city scale renders.
//
//   node export_city_cell.mjs [--cell 19_8] [--out city-cell.json]
//
// The transit README requires "a 1.6x-scaled render against real baked city
// geometry before the model is called done" - not against a stand-in. This
// reads the same tiles the app streams (app/public/tiles/toy, toystreets,
// toyland) through the app's own reader (app/src/tilebin.js), rebuilds the
// buildings, streets and landcover the way app/src/city.worker.js does, and
// writes flat position/normal/colour arrays for render_scenarios.py to turn
// into one Blender mesh.
//
// Default cell 19_8 is Hyde Street between Lombard and Chestnut - the
// Powell-Hyde block the postcards are taken on, and the steepest ground the
// car ever runs over.

import { promises as fs } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

import { readBuildings, readLandcover, readStreets } from '../../app/src/tilebin.js';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const TILES = path.resolve(HERE, '../../app/public/tiles');

const argv = process.argv.slice(2);
const arg = (flag, fallback) => {
  const i = argv.indexOf(flag);
  return i >= 0 ? argv[i + 1] : fallback;
};
const cell = arg('--cell', '19_8');
const radius = Number(arg('--radius', '190'));   // metres of context to keep
const out = arg('--out', path.join(HERE, 'city-cell.json'));

const manifest = JSON.parse(await fs.readFile(path.join(TILES, 'manifest.json'), 'utf8'));
const toy = JSON.parse(await fs.readFile(path.join(TILES, 'toy.json'), 'utf8'));
const landMeta = JSON.parse(await fs.readFile(path.join(TILES, 'landcover.json'), 'utf8'));

const buildingPalette = toy.palette.map((p) => p.color);
const streetClasses = manifest.streetClasses;
const landKinds = landMeta.kinds.map((k) => k.color);

const positions = [];
const normals = [];
const colors = [];

// Crop to a radius around the cell centre: nine full cells is 1.5 km of city
// and a 34 MB file, where the render only ever sees the block the car is on.
let CX = 0;
let CZ = 0;
function tri(a, b, c, n, col) {
  const mx = (a[0] + b[0] + c[0]) / 3 - CX;
  const mz = (a[2] + b[2] + c[2]) / 3 - CZ;
  if (mx * mx + mz * mz > radius * radius) return;
  // The baked ground triangulations do not guarantee a winding, and the render
  // scene rebuilds faces from the winding alone: a clockwise ground triangle
  // faces DOWN and renders as a black hole in the street.
  const ux = b[0] - a[0];
  const uy = b[1] - a[1];
  const uz = b[2] - a[2];
  const vx = c[0] - a[0];
  const vy = c[1] - a[1];
  const vz = c[2] - a[2];
  const cy = uz * vx - ux * vz;
  if (n[1] > 0.5 && cy < 0) {
    const t = b;
    b = c;
    c = t;
  }
  for (const p of [a, b, c]) {
    positions.push(p[0], p[1], p[2]);
    normals.push(n[0], n[1], n[2]);
    colors.push(col[0], col[1], col[2]);
  }
}

async function tile(kind, key) {
  try {
    const buf = await fs.readFile(path.join(TILES, kind, `${key}.bin`));
    return buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength);
  } catch {
    return null;
  }
}

// --- buildings: per-edge wall quads plus the baked roof triangulation -------
async function addBuildings(key) {
  const buffer = await tile('toy', key);
  if (!buffer) return 0;
  const d = readBuildings(buffer);
  for (let b = 0; b < d.count; b++) {
    const n = d.vertCount[b];
    if (n < 3) continue;
    const vo = d.vertOffset[b];
    const base = d.baseY[b] * 0.1;
    const top = d.topY[b] * 0.1;
    const wall = buildingPalette[d.palette[b]] || buildingPalette[0];
    const roof = (d.roofPalette && buildingPalette[d.roofPalette[b]]) || wall;
    const px = (i) => d.originX + d.verts[i * 2] * d.quant;
    const pz = (i) => d.originZ + d.verts[i * 2 + 1] * d.quant;

    for (let e = 0; e < n; e++) {
      const i0 = vo + e;
      const i1 = vo + ((e + 1) % n);
      const x0 = px(i0);
      const z0 = pz(i0);
      const x1 = px(i1);
      const z1 = pz(i1);
      const dx = x1 - x0;
      const dz = z1 - z0;
      const len = Math.hypot(dx, dz);
      if (len < 0.05) continue;
      const nrm = [dz / len, 0, -dx / len];
      tri([x0, base, z0], [x1, base, z1], [x1, top, z1], nrm, wall);
      tri([x0, base, z0], [x1, top, z1], [x0, top, z0], nrm, wall);
    }
    const io = d.idxOffset[b];
    for (let k = 0; k + 2 < d.idxCount[b]; k += 3) {
      const a = vo + d.indices[io + k];
      const c = vo + d.indices[io + k + 1];
      const e = vo + d.indices[io + k + 2];
      tri([px(a), top, pz(a)], [px(c), top, pz(c)], [px(e), top, pz(e)], [0, 1, 0], roof);
    }
  }
  return d.count;
}

// --- streets: a flat ribbon per centreline segment, width by class ----------
async function addStreets(key) {
  const buffer = await tile('toystreets', key);
  if (!buffer) return 0;
  const d = readStreets(buffer);
  for (let s = 0; s < d.count; s++) {
    const klass = streetClasses[d.klass[s]] || streetClasses[streetClasses.length - 1];
    const half = klass.width / 2;
    const o = d.ptOffset[s];
    for (let k = 0; k + 1 < d.ptCount[s]; k++) {
      const ax = d.originX + d.xz[(o + k) * 2] * d.quant;
      const az = d.originZ + d.xz[(o + k) * 2 + 1] * d.quant;
      const ay = d.y[o + k] * 0.1;
      const bx = d.originX + d.xz[(o + k + 1) * 2] * d.quant;
      const bz = d.originZ + d.xz[(o + k + 1) * 2 + 1] * d.quant;
      const by = d.y[o + k + 1] * 0.1;
      const dx = bx - ax;
      const dz = bz - az;
      const len = Math.hypot(dx, dz);
      if (len < 0.2) continue;
      const ox = (dz / len) * half;
      const oz = (-dx / len) * half;
      const p0 = [ax - ox, ay + 0.05, az - oz];
      const p1 = [ax + ox, ay + 0.05, az + oz];
      const p2 = [bx + ox, by + 0.05, bz + oz];
      const p3 = [bx - ox, by + 0.05, bz - oz];
      tri(p0, p1, p2, [0, 1, 0], klass.color);
      tri(p0, p2, p3, [0, 1, 0], klass.color);
    }
  }
  return d.count;
}

// --- terrain: the USGS heightfield the whole city stands on ------------------
//
// Without this the reconstruction has HOLES: landcover only covers parks,
// water and paved surfaces, and the app draws terrain.bin underneath
// everything else. Missing it left a black gap down the middle of the street
// in the first in-city render.
async function addTerrain() {
  const t = manifest.terrain;
  const buf = await fs.readFile(path.join(TILES, 'terrain.bin'));
  const h = new Int16Array(buf.buffer, buf.byteOffset, buf.byteLength / 2);
  const N = t.size;
  const sample = (x, z) => {
    const i = Math.min(N - 1, Math.max(0, Math.round((x - t.minX) / t.cellX)));
    const j = Math.min(N - 1, Math.max(0, Math.round((z - t.minZ) / t.cellZ)));
    return h[j * N + i] * t.scale;
  };
  // app/src/terrain.js urbanColor(): warm grey bare urban ground.
  const ground = (x, y) => {
    const west = Math.min(1, Math.max(0, (-x - 2000) / 5000));
    const high = Math.min(1, Math.max(0, (y - 60) / 180));
    return [
      0.44 + west * 0.16 - high * 0.05,
      0.41 + west * 0.13 - high * 0.03,
      0.37 + west * 0.08 + high * 0.02,
    ];
  };
  const step = 6;
  const R = radius + step * 2;
  for (let z = CZ - R; z < CZ + R; z += step) {
    for (let x = CX - R; x < CX + R; x += step) {
      const p00 = [x, sample(x, z), z];
      const p10 = [x + step, sample(x + step, z), z];
      const p11 = [x + step, sample(x + step, z + step), z + step];
      const p01 = [x, sample(x, z + step), z + step];
      const col = ground(x, p00[1]);
      tri(p00, p01, p11, [0, 1, 0], col);
      tri(p00, p11, p10, [0, 1, 0], col);
    }
  }
}

// --- landcover: the baked ground triangulation ------------------------------
async function addLandcover(key) {
  const buffer = await tile('toyland', key);
  if (!buffer) return 0;
  const d = readLandcover(buffer);
  const P = (i) => [
    d.originX + d.xz[i * 2] * d.quant,
    d.y[i] * 0.1,
    d.originZ + d.xz[i * 2 + 1] * d.quant,
  ];
  for (let k = 0; k + 2 < d.indexTotal; k += 3) {
    const a = d.indices[k];
    const b = d.indices[k + 1];
    const c = d.indices[k + 2];
    const col = landKinds[d.kind[a]] || [0.4, 0.4, 0.4];
    tri(P(a), P(b), P(c), [0, 1, 0], col);
  }
  return d.vertexTotal;
}

// The car needs a block of context around it, not one cell: take the target
// cell and its eight neighbours so the render has street frontage on all sides.
const [cx, cz] = cell.split('_').map(Number);
const keys = [];
for (let dz = -1; dz <= 1; dz++) {
  for (let dx = -1; dx <= 1; dx++) keys.push(`${cx + dx}_${cz + dz}`);
}

const grid0 = manifest.grid;
CX = grid0.originX + (cx + 0.5) * manifest.cellSize;
CZ = grid0.originZ + (cz + 0.5) * manifest.cellSize;

// The nearest street centreline to the cell centre, with its heading and
// height: where the car is stood for the in-city and tilted renders, so the
// scale test happens on a real SF street rather than a guessed spot.
let placement = null;
let placementFlat = null;
async function findPlacement(key) {
  const buffer = await tile('toystreets', key);
  if (!buffer) return;
  const d = readStreets(buffer);
  for (let s = 0; s < d.count; s++) {
    const o = d.ptOffset[s];
    for (let k = 0; k + 1 < d.ptCount[s]; k++) {
      const ax = d.originX + d.xz[(o + k) * 2] * d.quant;
      const az = d.originZ + d.xz[(o + k) * 2 + 1] * d.quant;
      const bx = d.originX + d.xz[(o + k + 1) * 2] * d.quant;
      const bz = d.originZ + d.xz[(o + k + 1) * 2 + 1] * d.quant;
      const mx = (ax + bx) / 2;
      const mz = (az + bz) / 2;
      const dist = Math.hypot(mx - CX, mz - CZ);
      const rise = (d.y[o + k + 1] - d.y[o + k]) * 0.1;
      const run = Math.hypot(bx - ax, bz - az);
      if (run < 4) continue;
      if (dist > 150) continue;
      const klass = streetClasses[d.klass[s]]?.id ?? 'other';
      if (klass === 'other') continue;   // service alleys are not cable car lines
      // Of the real streets near the centre, take the one closest to the 20%
      // grade the plan asks the tilted render to prove. Not the steepest:
      // this cell also contains Lombard's crooked block at 40%+, which no
      // cable car has ever climbed.
      const grade = Math.abs((rise / run) * 100);
      const score = Math.abs(grade - 20);
      const row = {
        score,
        gradeAbs: grade,
        dist,
        x: mx,
        z: mz,
        y: ((d.y[o + k] + d.y[o + k + 1]) / 2) * 0.1,
        headingRad: Math.atan2(bx - ax, bz - az),
        gradePct: (rise / run) * 100,
        klass,
        runM: run,
      };
      if (!placement || score < placement.score) placement = row;
      // A second, near-level segment: the 1.6x scale comparison is easier to
      // judge with the three vehicles standing on flat ground.
      if (run > 8 && (!placementFlat || grade < placementFlat.gradeAbs)) placementFlat = row;
    }
  }
}

let buildings = 0;
for (const key of keys) await findPlacement(key);
await addTerrain();
for (const key of keys) {
  buildings += await addBuildings(key);
  await addStreets(key);
  await addLandcover(key);
}

await fs.writeFile(
  out,
  JSON.stringify({
    cell,
    cells: keys,
    center: [CX, CZ],
    radius,
    placement,
    placementFlat,
    buildings,
    triangles: positions.length / 9,
    positions,
    normals,
    colors,
  })
);
console.log(
  `[city] cell ${cell} (+8 neighbours, ${radius} m crop): ${buildings} buildings, ` +
    `${positions.length / 9} triangles -> ${out}`
);
console.log(`[city] grade placement ${JSON.stringify(placement)}`);
console.log(`[city] level placement ${JSON.stringify(placementFlat)}`);
