// Offline fit-rate report.
//
// Runs the exact placement brain the tile worker runs (`src/kitplan.js`) over
// every baked toy cell on disk and prints how much of each neighbourhood the
// kit fills, plus the piece histogram and the triangle load of the worst tile.
//
//   node tools/kit-report.mjs [--json out.json]

import { readFileSync, writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';
import { catalogForWorker, createKitCatalog, planKit, KIT_STRIDE, NEIGHBORHOOD_ZONE, ZONE } from '../src/kitplan.js';
import { readBuildings } from '../src/tilebin.js';

const here = dirname(fileURLToPath(import.meta.url));
const PUBLIC = join(here, '..', 'public');
const TILES = join(PUBLIC, 'tiles');
const readJSON = (path) => JSON.parse(readFileSync(path, 'utf8'));

const manifest = readJSON(join(TILES, 'manifest.json'));
const toyIndex = readJSON(join(TILES, 'toy.json'));
const streetIndex = readJSON(join(TILES, 'streets.json'));
const neighborhoods = readJSON(join(TILES, 'context', 'neighborhoods.json'));
const catalog = createKitCatalog(readJSON(join(PUBLIC, 'sf-assets', 'kit', 'kit_index.json')));

const project = (lon, lat) => [
  (lon - manifest.projection.lon0) * manifest.projection.mPerDegLon,
  -(lat - manifest.projection.lat0) * manifest.projection.mPerDegLat,
];
const exclusions = new Float32Array(
  manifest.landmarks.flatMap((l) => {
    const [x, z] = project(l.lon, l.lat);
    return [x, z, l.exclude || 60];
  })
);

function inRings(x, z, rings) {
  for (const ring of rings) {
    let inside = false;
    for (let i = 0, j = ring.length - 2; i < ring.length; j = i, i += 2) {
      const xi = ring[i];
      const zi = ring[i + 1];
      const xj = ring[j];
      const zj = ring[j + 1];
      if (zi > z !== zj > z && x < ((xj - xi) * (z - zi)) / (zj - zi) + xi) inside = !inside;
    }
    if (inside) return true;
  }
  return false;
}

// Same 100 m raster the runtime burns, built straight from the polygons.
const CELL = 100;
const originX = Math.floor(manifest.extent.minX / CELL) * CELL;
const originZ = Math.floor(manifest.extent.minZ / CELL) * CELL;
const cols = Math.ceil((manifest.extent.maxX - originX) / CELL) + 1;
const rows = Math.ceil((manifest.extent.maxZ - originZ) / CELL) + 1;
const zones = { originX, originZ, cell: CELL, cols, rows, data: new Uint8Array(cols * rows) };
const nameGrid = new Array(cols * rows).fill(null);
for (const nhood of neighborhoods) {
  const zone = NEIGHBORHOOD_ZONE[nhood.name];
  for (let gz = 0; gz < rows; gz++) {
    const z = originZ + gz * CELL + CELL / 2;
    for (let gx = 0; gx < cols; gx++) {
      const x = originX + gx * CELL + CELL / 2;
      if (!inRings(x, z, nhood.rings)) continue;
      nameGrid[gz * cols + gx] = nhood.name;
      if (zone !== undefined && zone !== ZONE.OTHER) zones.data[gz * cols + gx] = zone;
    }
  }
}
const neighborhoodAt = (x, z) => {
  const gx = Math.floor((x - originX) / CELL);
  const gz = Math.floor((z - originZ) / CELL);
  if (gx < 0 || gz < 0 || gx >= cols || gz >= rows) return 'Outside';
  return nameGrid[gz * cols + gx] || 'Outside';
};

const cellBuffer = (kind, key) => {
  const buf = readFileSync(join(TILES, kind, `${key}.bin`));
  return { buffer: buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength) };
};

// The runtime plans one 1 km chunk at a time; mirror that so row rhythm, corner
// choice and the fit rate all come out identical.
const CHUNK = 1000;
const chunks = new Map();
for (const cell of toyIndex.cells) {
  const cx = Math.floor((cell.originX + 250 - manifest.extent.minX) / CHUNK);
  const cz = Math.floor((cell.originZ + 250 - manifest.extent.minZ) / CHUNK);
  const key = `${cx}_${cz}`;
  if (!chunks.has(key)) {
    chunks.set(key, {
      key,
      originX: manifest.extent.minX + cx * CHUNK,
      originZ: manifest.extent.minZ + cz * CHUNK,
      cells: [],
    });
  }
  chunks.get(key).cells.push(cell);
}
const streetKeys = new Set(streetIndex.cells.map((c) => c.key));
const streetSize = streetIndex.cellSize;
const gridOrigin = streetIndex.grid;

const kitJob = catalogForWorker(catalog);
const debug = {};
const perNeighborhood = new Map();
const pieceUse = new Map();
let considered = 0;
let placed = 0;
let worst = { key: null, instances: 0, triangles: 0, pieceTypes: 0 };

for (const chunk of chunks.values()) {
  const parsed = chunk.cells.map((cell) => readBuildings(cellBuffer('toy', cell.key).buffer));
  const streets = [];
  const x0 = Math.floor((chunk.originX - 80 - gridOrigin.originX) / streetSize);
  const x1 = Math.floor((chunk.originX + CHUNK + 80 - gridOrigin.originX) / streetSize);
  const z0 = Math.floor((chunk.originZ - 80 - gridOrigin.originZ) / streetSize);
  const z1 = Math.floor((chunk.originZ + CHUNK + 80 - gridOrigin.originZ) / streetSize);
  for (let cz = z0; cz <= z1; cz++) {
    for (let cx = x0; cx <= x1; cx++) {
      if (streetKeys.has(`${cx}_${cz}`)) streets.push(cellBuffer('toystreets', `${cx}_${cz}`));
    }
  }

  const plan = planKit({
    parsed,
    originX: chunk.originX,
    originZ: chunk.originZ,
    kit: kitJob,
    zones,
    streets,
    exclusions,
    debug,
  });
  considered += plan.considered;
  placed += plan.placed;

  // Attribute every footprint to its neighbourhood, filled or not.
  for (let bi = 0; bi < parsed.length; bi++) {
    const d = parsed[bi];
    for (let b = 0; b < d.count; b++) {
      if (d.vertCount[b] < 3) continue;
      if (d.flags && d.flags[b] & 2) continue;
      const vo = d.vertOffset[b];
      let cx = 0;
      let cz = 0;
      for (let k = 0; k < d.vertCount[b]; k++) {
        cx += d.originX + d.verts[(vo + k) * 2] * d.quant;
        cz += d.originZ + d.verts[(vo + k) * 2 + 1] * d.quant;
      }
      cx /= d.vertCount[b];
      cz /= d.vertCount[b];
      const name = neighborhoodAt(cx, cz);
      let row = perNeighborhood.get(name);
      if (!row) perNeighborhood.set(name, (row = { total: 0, filled: 0 }));
      row.total++;
      if (plan.filled[bi][b]) row.filled++;
    }
  }

  let triangles = 0;
  const types = new Set();
  for (let i = 0; i < plan.instances.length; i += KIT_STRIDE) {
    const piece = catalog.pieces[plan.instances[i]];
    pieceUse.set(piece.id, (pieceUse.get(piece.id) || 0) + 1);
    triangles += piece.tris;
    types.add(piece.i);
  }
  if (triangles > worst.triangles) {
    worst = { key: chunk.key, instances: plan.placed, triangles, pieceTypes: types.size };
  }
}

const table = [...perNeighborhood.entries()]
  .filter(([, v]) => v.total >= 25)
  .sort((a, b) => b[1].total - a[1].total)
  .map(([name, v]) => ({ name, total: v.total, filled: v.filled, rate: v.filled / v.total }));

const unused = catalog.pieces.filter((p) => !pieceUse.has(p.id)).map((p) => p.id);
const summary = {
  footprints: considered,
  kitFilled: placed,
  rate: placed / considered,
  pieceTypesUsed: pieceUse.size,
  pieceTypesTotal: catalog.pieces.length,
  worstChunk: worst,
  neighborhoods: table,
  unused,
};

const pct = (v) => `${(v * 100).toFixed(1)}%`;
console.log(`footprints ${considered}, kit-filled ${placed} (${pct(summary.rate)})`);
console.log(`piece types used ${pieceUse.size}/${catalog.pieces.length}`);
console.log(
  `worst chunk ${worst.key}: ${worst.instances} instances, ${worst.triangles} kit triangles, ${worst.pieceTypes} piece types`
);
console.log('');
for (const row of table) {
  console.log(`${row.name.padEnd(34)} ${String(row.filled).padStart(6)}/${String(row.total).padEnd(6)} ${pct(row.rate)}`);
}
if (unused.length) console.log(`\nnever placed (${unused.length}): ${unused.join(', ')}`);
console.log(
  `\nskipped: ${Object.entries(debug)
    .sort((a, b) => b[1] - a[1])
    .map(([k, v]) => `${k} ${v}`)
    .join(', ')}`
);

const jsonAt = process.argv.indexOf('--json');
if (jsonAt > -1 && process.argv[jsonAt + 1]) {
  writeFileSync(process.argv[jsonAt + 1], `${JSON.stringify(summary, null, 2)}\n`);
}
