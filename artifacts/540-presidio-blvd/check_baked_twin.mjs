// Does the SHIPPED baked tile still contain a procedural building on this
// landmark's footprint? Reads app/public/tiles/buildings/<cell>.bin directly,
// so it needs no pipeline/out/ and no re-bake — which is exactly the situation
// it exists to diagnose.
//
//   node artifacts/540-presidio-blvd/check_baked_twin.mjs
//
// Exit 0 = clear (the re-bake has landed). Exit 1 = a baked footprint is still
// inside the exclusion zone, so the GLB will intersect it.
//
// This is the same question `node pipeline/audit.mjs` check 1.6 answers, but
// audit.mjs loads pipeline/out/terrain.json and therefore cannot run on a
// checkout that has never baked.

import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const TILES = path.join(ROOT, 'app/public/tiles');

const ID = '540PresidioBlvd';
const LON = -122.4519224;
const LAT = 37.7966667;
const EXCLUDE = 15; // must match pipeline/lib/landmarks.mjs

const LON0 = -122.4375;
const LAT0 = 37.77;
const project = (lon, lat) => [
  (lon - LON0) * 111320 * Math.cos((LAT0 * Math.PI) / 180),
  -(lat - LAT0) * 110540,
];

const manifest = JSON.parse(readFileSync(path.join(TILES, 'buildings.json'), 'utf8'));
const { grid, cellSize } = manifest;
const [ax, az] = project(LON, LAT);
const cx = Math.floor((ax - grid.originX) / cellSize);
const cz = Math.floor((az - grid.originZ) / cellSize);
const key = `${cx}_${cz}`;

const buf = readFileSync(path.join(TILES, 'buildings', `${key}.bin`));
const dv = new DataView(buf.buffer, buf.byteOffset, buf.byteLength);
const version = dv.getUint16(4, true);
const count = dv.getUint32(8, true);
const vertexTotal = dv.getUint32(12, true);
const originX = dv.getFloat32(20, true);
const originZ = dv.getFloat32(24, true);
const QUANT = dv.getFloat32(28, true);

// Header layout mirrors writeBuildingsBlob() in pipeline/lib/binio.mjs.
let off = 32;
const vertOffsetAt = off; off += 4 * count;
off += 4 * count;                       // idxOffset
const vertCountAt = off; off += 2 * count;
off += 2 * count;                       // idxCount
off += 2 * count;                       // baseY
const topYAt = off; off += 2 * count;
off += count; off += count;             // palette, seed
if (version >= 2) off += 2 * count;     // flags, roofPalette
if (version >= 3) off += 3 * count;     // cat, yaw, night
off = off + (off % 2);
const vertsAt = off;

const vertOffset = new Uint32Array(buf.buffer, buf.byteOffset + vertOffsetAt, count);
const vertCount = new Uint16Array(buf.buffer, buf.byteOffset + vertCountAt, count);
const topY = new Int16Array(buf.buffer, buf.byteOffset + topYAt, count);
const verts = new Int16Array(buf.buffer, buf.byteOffset + vertsAt, vertexTotal * 2);

// excluded() in pipeline/buildings.mjs drops a footprint if ANY vertex is
// inside the radius, so test vertices, not centroids.
const intruders = [];
for (let i = 0; i < count; i++) {
  let nearest = Infinity;
  for (let k = 0; k < vertCount[i]; k++) {
    const x = originX + verts[(vertOffset[i] + k) * 2] * QUANT;
    const z = originZ + verts[(vertOffset[i] + k) * 2 + 1] * QUANT;
    nearest = Math.min(nearest, Math.hypot(x - ax, z - az));
  }
  if (nearest < EXCLUDE) {
    intruders.push({ index: i, nearestVertexM: +nearest.toFixed(2), topY: topY[i] / 10, verts: vertCount[i] });
  }
}

console.log(`${ID}: cell ${key}, ${count} baked buildings, exclusion radius ${EXCLUDE} m`);
if (!intruders.length) {
  console.log('PASS — no baked footprint inside the exclusion zone. The re-bake has landed.');
  process.exit(0);
}
console.log(`FAIL — ${intruders.length} baked footprint(s) still inside the exclusion zone:`);
for (const b of intruders) console.log(' ', JSON.stringify(b));
console.log('Re-bake the tiles (see artifacts/540-presidio-blvd/REPORT.md, "The outstanding step").');
process.exit(1);
