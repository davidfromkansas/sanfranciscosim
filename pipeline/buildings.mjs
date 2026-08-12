// Bakes building footprints into per-cell binary blobs.
//
// Primary source: DataSF footprints (ynuv-fyni) — LiDAR/Pictometry-derived
// outlines with `hgt_median_m` (median roof height above ground).
// Gap-fill: Overture Maps buildings, which carry current OSM heights. The 2010
// DataSF height refresh predates the whole post-2015 SoMa skyline, so Overture
// both corrects rebuilt parcels and supplies footprints DataSF never saw.

import { mkdir, rm, writeFile, readFile } from 'node:fs/promises';
import { existsSync, createReadStream } from 'node:fs';
import { createInterface } from 'node:readline';
import earcut from 'earcut';
import {
  CELL_SIZE,
  GRID,
  cellIndex,
  cellOrigin,
  hash01,
  insideBBox,
  project,
} from './lib/geo.mjs';
import { ringArea, ringBBox, ringCentroid, simplifyRing } from './lib/poly.mjs';
import { loadHeightmap } from './lib/heightmap.mjs';
import { LANDMARKS } from './lib/landmarks.mjs';
import { PALETTE, makeDistrictLookup } from './lib/districts.mjs';
import { writeBuildingsBlob } from './lib/binio.mjs';

const DATA = new URL('./data/', import.meta.url);
const OUT = new URL('./out/', import.meta.url);
const CELLS_OUT = new URL('./out/buildings/', import.meta.url);

const SIMPLIFY_TOLERANCE = 0.6;
const MIN_AREA = 10;
const MAX_HEIGHT = 340;
const OCC_RES = 5; // occupancy raster resolution in meters

const { sampleElevation } = await loadHeightmap();
const paletteAt = makeDistrictLookup(project);

const exclusions = LANDMARKS.map((l) => {
  const [x, z] = project(l.lon, l.lat);
  return { x, z, r2: l.exclude * l.exclude, id: l.id };
});

// A bridge is a kilometres-long structure, so a circle around its anchor only
// clears midspan: the towers, anchorages, approach viaducts and the shore
// structures they stand on are all far outside it. Every bespoke deck therefore
// also carries a corridor along its whole baked centreline. Only what would
// actually hit the deck is cleared: the approaches run high over Rincon Hill
// and Folsom, and the blocks underneath them are real city that has to stay.
// Near the shore a hand-made bridge is more than its deck, though: the Golden
// Gate's arch and approach steelwork come down to the ground and the deck
// height says nothing about them, so the end of an asset bridge is cleared
// outright.
const DECK_CORRIDOR = 40;
const DECK_CLEARANCE = 4;
const DECK_END_ZONE = 400;
const assetIds = new Set(
  await readFile(new URL('../app/public/sf-assets/landmarks_manifest.json', import.meta.url), 'utf8')
    .then((raw) => JSON.parse(raw).map((entry) => entry.id))
    .catch(() => [])
);
const kebab = (id) => id.replace(/([a-z0-9])([A-Z])/g, '$1-$2').toLowerCase();
const deckLines = [];
for (const [id, spec] of Object.entries(JSON.parse(await readFile(new URL('bridges.json', OUT), 'utf8')))) {
  for (const nodes of [spec.nodes, spec.east?.nodes]) {
    if (!nodes) continue;
    const pts = nodes.map(([lon, lat, y]) => {
      const [x, z] = project(lon, lat);
      return [x, z, y];
    });
    const arc = [0];
    for (let i = 1; i < pts.length; i++) {
      arc.push(arc[i - 1] + Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]));
    }
    const xs = pts.map((p) => p[0]);
    const zs = pts.map((p) => p[1]);
    deckLines.push({
      pts,
      arc,
      asset: assetIds.has(kebab(id)),
      minX: Math.min(...xs) - DECK_CORRIDOR,
      maxX: Math.max(...xs) + DECK_CORRIDOR,
      minZ: Math.min(...zs) - DECK_CORRIDOR,
      maxZ: Math.max(...zs) + DECK_CORRIDOR,
    });
  }
}

// Deck height over a point inside a corridor: 0 in an asset bridge's end zone,
// where the structure reaches the ground, and Infinity clear of every deck.
function deckHeightOver(x, z) {
  let best = Infinity;
  for (const { pts: line, arc, asset, minX, maxX, minZ, maxZ } of deckLines) {
    if (x < minX || x > maxX || z < minZ || z > maxZ) continue;
    const span = arc[arc.length - 1];
    for (let i = 1; i < line.length; i++) {
      const [ax, az, ay] = line[i - 1];
      const [bx, bz, by] = line[i];
      const dx = bx - ax;
      const dz = bz - az;
      const l2 = dx * dx + dz * dz || 1;
      const t = Math.min(1, Math.max(0, ((x - ax) * dx + (z - az) * dz) / l2));
      if ((x - (ax + dx * t)) ** 2 + (z - (az + dz * t)) ** 2 >= DECK_CORRIDOR * DECK_CORRIDOR) continue;
      const along = arc[i - 1] + (arc[i] - arc[i - 1]) * t;
      const fromEnd = Math.min(along, span - along);
      best = Math.min(best, asset && fromEnd < DECK_END_ZONE ? 0 : ay + (by - ay) * t);
    }
  }
  return best;
}

// A footprint is excluded when any part of it reaches into a bespoke landmark's
// zone, not just when its centroid does, so nothing pokes through the models.
// Along a bridge it also has to reach the deck to be in the way.
function excluded(ring, cx, cz, topY) {
  for (const e of exclusions) {
    if ((cx - e.x) ** 2 + (cz - e.z) ** 2 < e.r2) return true;
    for (let i = 0; i < ring.length; i += 2) {
      if ((ring[i] - e.x) ** 2 + (ring[i + 1] - e.z) ** 2 < e.r2) return true;
    }
  }
  let deckY = deckHeightOver(cx, cz);
  for (let i = 0; i < ring.length; i += 2) {
    deckY = Math.min(deckY, deckHeightOver(ring[i], ring[i + 1]));
  }
  return topY > deckY - DECK_CLEARANCE;
}

function projectRing(coords) {
  const out = [];
  for (const c of coords) {
    if (!Number.isFinite(c[0]) || !Number.isFinite(c[1])) continue;
    const [x, z] = project(c[0], c[1]);
    out.push(x, z);
  }
  return out;
}

// The runtime builds outward-facing walls assuming positive signed ring area.
function orientRing(ring) {
  if (ringArea(ring) < 0) {
    const out = [];
    for (let i = ring.length - 2; i >= 0; i -= 2) out.push(ring[i], ring[i + 1]);
    return out;
  }
  return ring;
}

function num(v) {
  const n = typeof v === 'number' ? v : parseFloat(v);
  return Number.isFinite(n) ? n : NaN;
}

// DataSF gives LiDAR statistics of the roof surface above ground: hgt_median_m
// is the eave-ish median, hgt_maxcm the ridge. A flat box at the median alone
// makes every pitched-roof row house too squat, so use the midpoint of the two.
function datasfHeight(p) {
  const median = num(p.hgt_median_m);
  const max = num(p.hgt_maxcm) / 100;
  if (median > 2.5) return Math.min(max > median ? (median + max) / 2 : median, MAX_HEIGHT);
  const mean = num(p.hgt_meancm) / 100;
  if (mean > 2.5) return Math.min(mean, MAX_HEIGHT);
  if (max > 3) return Math.min(max * 0.8, MAX_HEIGHT);
  return 8;
}

function overtureHeight(p) {
  const h = num(p.height);
  if (h > 2) return Math.min(h, MAX_HEIGHT);
  const floors = num(p.num_floors);
  if (floors >= 1) return Math.min(floors * 3.2 + 1, MAX_HEIGHT);
  return NaN;
}

const buildings = [];
const occCols = Math.ceil((GRID.cols * CELL_SIZE) / OCC_RES);
const occRows = Math.ceil((GRID.rows * CELL_SIZE) / OCC_RES);
const occupancy = new Uint8Array(occCols * occRows);

function markOccupied(bbox) {
  const i0 = Math.max(0, Math.floor((bbox[0] - GRID.originX) / OCC_RES));
  const i1 = Math.min(occCols - 1, Math.ceil((bbox[2] - GRID.originX) / OCC_RES));
  const j0 = Math.max(0, Math.floor((bbox[1] - GRID.originZ) / OCC_RES));
  const j1 = Math.min(occRows - 1, Math.ceil((bbox[3] - GRID.originZ) / OCC_RES));
  for (let j = j0; j <= j1; j++) {
    for (let i = i0; i <= i1; i++) occupancy[j * occCols + i] = 1;
  }
}

function occupiedFraction(bbox) {
  const i0 = Math.max(0, Math.floor((bbox[0] - GRID.originX) / OCC_RES));
  const i1 = Math.min(occCols - 1, Math.ceil((bbox[2] - GRID.originX) / OCC_RES));
  const j0 = Math.max(0, Math.floor((bbox[1] - GRID.originZ) / OCC_RES));
  const j1 = Math.min(occRows - 1, Math.ceil((bbox[3] - GRID.originZ) / OCC_RES));
  let total = 0;
  let hit = 0;
  for (let j = j0; j <= j1; j++) {
    for (let i = i0; i <= i1; i++) {
      total++;
      if (occupancy[j * occCols + i]) hit++;
    }
  }
  return total === 0 ? 1 : hit / total;
}

// Spatial hash of source-building centroids for cross-source matching.
const HASH_RES = 25;
const centroidHash = new Map();
function hashKey(x, z) {
  return `${Math.floor(x / HASH_RES)}:${Math.floor(z / HASH_RES)}`;
}
function addCentroid(x, z, index) {
  const k = hashKey(x, z);
  let list = centroidHash.get(k);
  if (!list) centroidHash.set(k, (list = []));
  list.push(index);
}
function nearbyIndices(x, z) {
  const cx = Math.floor(x / HASH_RES);
  const cz = Math.floor(z / HASH_RES);
  const out = [];
  for (let dz = -1; dz <= 1; dz++) {
    for (let dx = -1; dx <= 1; dx++) {
      const list = centroidHash.get(`${cx + dx}:${cz + dz}`);
      if (list) out.push(...list);
    }
  }
  return out;
}

function addBuilding(ringIn, height, seedSource) {
  let ring = simplifyRing(ringIn, SIMPLIFY_TOLERANCE);
  if (ring.length / 2 < 3) return null;
  const area = Math.abs(ringArea(ring));
  if (area < MIN_AREA) return null;
  if (ring.length / 2 > 200) ring = simplifyRing(ring, SIMPLIFY_TOLERANCE * 4);
  ring = orientRing(ring);

  const [cx, cz] = ringCentroid(ring);
  const cell = cellIndex(cx, cz);
  if (!cell) return null;

  // Drape: wall bottoms reach the lowest terrain under the footprint so nothing
  // floats on a hillside; the roof sits `height` above the centroid ground.
  let minGround = Infinity;
  for (let i = 0; i < ring.length; i += 2) {
    const e = sampleElevation(ring[i], ring[i + 1]);
    if (e < minGround) minGround = e;
  }
  const ground = sampleElevation(cx, cz);
  const baseY = Math.max(-3, minGround - 0.4);
  const topY = Math.max(baseY + 3, ground + height);
  if (excluded(ring, cx, cz, topY)) return null;

  const indices = earcut(ring);
  if (indices.length < 3) return null;

  const seed = Math.floor(hash01(seedSource) * 256) & 255;
  const b = {
    ring,
    indices,
    baseY,
    topY,
    palette: paletteAt(cx, cz),
    seed,
    cx,
    cz,
    height: topY - ground,
    area,
    cell,
    bbox: ringBBox(ring),
  };
  buildings.push(b);
  return b;
}

// ---------------------------------------------------------------- DataSF pass
console.log('reading DataSF footprints...');
const { streamFeatures, outerRings } = await import('./lib/geojsonStream.mjs');
let dsRead = 0;
for await (const feature of streamFeatures(new URL('buildings_datasf.geojson', DATA).pathname)) {
  dsRead++;
  const height = datasfHeight(feature.properties || {});
  for (const ring of outerRings(feature.geometry)) {
    const projected = projectRing(ring);
    if (projected.length < 6) continue;
    const b = addBuilding(projected, height, dsRead * 2654435761);
    if (b) {
      b.source = 'datasf';
      markOccupied(b.bbox);
      addCentroid(b.cx, b.cz, buildings.length - 1);
    }
  }
  if (dsRead % 40000 === 0) console.log(`  ${dsRead} features -> ${buildings.length} baked`);
}
const datasfCount = buildings.length;
console.log(`DataSF: ${dsRead} features -> ${datasfCount} buildings`);

// -------------------------------------------------------------- Overture pass
const overturePath = new URL('overture_buildings.geojsonseq', DATA).pathname;
let overtureAdded = 0;
let overtureFixed = 0;
// Missing Overture is not a "skip the optional pass" case: without it the bake
// runs to completion and quietly ships a flattened downtown (tallest procedural
// building 175.4 m instead of 244.4 m, ~3.3k buildings absent). A silent
// degradation that still produces committable tiles is worse than a crash, so
// this refuses rather than continues. `npm run download` fetches the file.
if (!existsSync(overturePath) && process.env.ALLOW_NO_OVERTURE !== '1') {
  throw new Error(
    'pipeline/data/overture_buildings.geojsonseq is missing. Run `npm run download`. ' +
      'Baking without it drops ~3,300 buildings and flattens the post-2015 skyline ' +
      '(DataSF heights date from 2010) — set ALLOW_NO_OVERTURE=1 if you really ' +
      'want a DataSF-only bake, and do not commit those tiles.'
  );
}
if (existsSync(overturePath)) {
  console.log('gap-filling from Overture Maps...');
  const rl = createInterface({
    input: createReadStream(overturePath, { encoding: 'utf8' }),
    crlfDelay: Infinity,
  });
  let read = 0;
  for await (const line of rl) {
    if (!line.trim()) continue;
    read++;
    let feature;
    try {
      feature = JSON.parse(line);
    } catch {
      continue;
    }
    const props = feature.properties || {};
    const h = overtureHeight(props);
    const geom = feature.geometry;
    if (!geom) continue;
    const polys = geom.type === 'Polygon' ? [geom.coordinates] : geom.coordinates || [];
    for (const poly of polys) {
      const outer = poly && poly[0];
      if (!outer || outer.length < 4) continue;
      if (!insideBBox(outer[0][0], outer[0][1])) continue;
      const projected = projectRing(outer);
      if (projected.length < 6) continue;
      const ring = simplifyRing(projected, SIMPLIFY_TOLERANCE);
      if (ring.length / 2 < 3) continue;
      const [cx, cz] = ringCentroid(ring);
      const bbox = ringBBox(ring);

      // Correct heights on parcels DataSF measured before the current building
      // existed (Salesforce Tower's block was a bus terminal in 2010).
      if (h >= 20) {
        let best = -1;
        let bestD = Infinity;
        for (const idx of nearbyIndices(cx, cz)) {
          const cand = buildings[idx];
          const d = (cand.cx - cx) ** 2 + (cand.cz - cz) ** 2;
          if (d < bestD) {
            bestD = d;
            best = idx;
          }
        }
        if (best >= 0 && bestD < 30 * 30) {
          const cand = buildings[best];
          if (h > cand.height * 1.4) {
            const ground = sampleElevation(cand.cx, cand.cz);
            cand.topY = Math.max(cand.baseY + 3, ground + h);
            cand.height = h;
            overtureFixed++;
          }
          continue;
        }
      }

      // Footprints DataSF never saw at all.
      if (occupiedFraction(bbox) > 0.25) continue;
      const b = addBuilding(ring, Number.isFinite(h) ? h : 8, read * 40503 + 7);
      if (b) {
        b.source = 'overture';
        markOccupied(b.bbox);
        overtureAdded++;
      }
    }
    if (read % 50000 === 0) console.log(`  ${read} overture features scanned`);
  }
  console.log(`Overture: ${overtureAdded} added, ${overtureFixed} heights corrected`);
} else {
  console.warn('! overture_buildings.geojsonseq missing — skipping gap-fill');
}

// ------------------------------------------------------------------- grouping
// Stale cells from an earlier bake would linger and desync the index.
await rm(CELLS_OUT, { recursive: true, force: true });
await mkdir(CELLS_OUT, { recursive: true });
const cells = new Map();
for (const b of buildings) {
  const key = b.cell.key;
  let cell = cells.get(key);
  if (!cell) {
    const [ox, oz] = cellOrigin(b.cell.cx, b.cell.cz);
    cells.set(key, (cell = { key, cx: b.cell.cx, cz: b.cell.cz, originX: ox, originZ: oz, buildings: [] }));
  }
  cell.buildings.push(b);
}

let bytes = 0;
const index = [];
const sortedKeys = [...cells.keys()].sort();
for (const key of sortedKeys) {
  const cell = cells.get(key);
  // Tallest first so the near-tier merge front-loads the visually dominant mass.
  cell.buildings.sort((a, b) => b.topY - a.topY);
  const blob = writeBuildingsBlob(cell);
  await writeFile(new URL(`${key}.bin`, CELLS_OUT), blob);
  bytes += blob.length;
  let maxTop = 0;
  for (const b of cell.buildings) maxTop = Math.max(maxTop, b.topY);
  index.push({
    key,
    cx: cell.cx,
    cz: cell.cz,
    originX: cell.originX,
    originZ: cell.originZ,
    count: cell.buildings.length,
    maxTop: Math.round(maxTop * 10) / 10,
    bytes: blob.length,
  });
}

// Cleaned intermediate: the toy bake re-derives its own chunky geometry from
// exactly these footprints, so neither bake re-downloads or re-cleans anything.
const round2 = (v) => Math.round(v * 100) / 100;
await writeFile(
  new URL('footprints.json', OUT),
  JSON.stringify({
    cellSize: CELL_SIZE,
    grid: GRID,
    palette: PALETTE,
    buildings: buildings.map((b) => [
      b.ring.map(round2),
      round2(b.height),
      round2(b.baseY),
      b.seed,
      b.palette,
    ]),
  })
);

const tallest = buildings.reduce((a, b) => (b.height > a.height ? b : a));
const stats = {
  total: buildings.length,
  datasf: datasfCount,
  overtureAdded,
  overtureFixed,
  cells: index.length,
  bytes,
  tallest: {
    height: Math.round(tallest.height * 10) / 10,
    x: Math.round(tallest.cx),
    z: Math.round(tallest.cz),
    source: tallest.source,
  },
};

await writeFile(
  new URL('buildings.json', OUT),
  JSON.stringify(
    {
      cellSize: CELL_SIZE,
      grid: GRID,
      palette: PALETTE,
      stats,
      cells: index,
    },
    null,
    1
  )
);

const heights = buildings.map((b) => b.height).sort((a, b) => b - a);
console.log(
  `baked ${buildings.length} buildings into ${index.length} cells, ${(bytes / 1e6).toFixed(1)} MB\n` +
    `tallest: ${heights.slice(0, 6).map((h) => h.toFixed(0)).join(', ')} m`
);
