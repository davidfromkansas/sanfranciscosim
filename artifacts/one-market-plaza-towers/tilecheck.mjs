// Prove from the TILE, not from the radius, that nothing procedural is left
// standing under the One Market Plaza towers asset — and report penetration DEPTH, because a
// party-wall neighbour legitimately shares a survey vertex and a boolean test
// flags it while a depth test shows the truth.
import { readFileSync, existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
const TILES = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../app/public/tiles/buildings');
import { gunzipSync } from 'node:zlib';
import { project, cellIndex, cellOrigin, CELL_SIZE } from '../../pipeline/lib/geo.mjs';

const LON = -122.3941803, LAT = 37.7933169;
const [ax, az] = project(LON, LAT);

// the asset's own lot-007 envelope, model-space, from build_one_market_plaza_towers.py ENVELOPE
const FOOT = [
  [-50.850, 13.450], [-60.350, 4.150], [-22.950, -32.650], [-18.550, -38.150],
  [6.350, -63.250], [31.650, -38.350], [25.550, -32.150], [35.050, -23.050],
  [60.350, 2.150], [28.650, 33.150], [-1.350, 63.250], [-34.750, 29.050],
].map(([bx, by]) => [ax + bx, az - by]);   // Blender +Y north -> local -z north

function inside(px, pz, poly) {
  let hit = false;
  for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) {
    const [xi, zi] = poly[i], [xj, zj] = poly[j];
    if ((zi > pz) !== (zj > pz) && px < ((xj - xi) * (pz - zi)) / (zj - zi) + xi) hit = !hit;
  }
  return hit;
}
function distToEdge(px, pz, poly) {
  let best = Infinity;
  for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) {
    const [xi, zi] = poly[i], [xj, zj] = poly[j];
    const dx = xj - xi, dz = zj - zi;
    const t = Math.max(0, Math.min(1, ((px - xi) * dx + (pz - zi) * dz) / (dx * dx + dz * dz || 1)));
    best = Math.min(best, Math.hypot(px - (xi + t * dx), pz - (zi + t * dz)));
  }
  return best;
}

const cells = new Set();
for (let dx = -1; dx <= 1; dx++) for (let dz = -1; dz <= 1; dz++) {
  const c = cellIndex(ax + dx * CELL_SIZE, az + dz * CELL_SIZE);
  if (c) cells.add(c.key);
}
let total = 0, hits = [];
for (const key of cells) {
  let p = path.join(TILES, `${key}.bin`);
  let raw;
  if (existsSync(p)) raw = readFileSync(p);
  else if (existsSync(p + '.gz')) raw = gunzipSync(readFileSync(p + '.gz'));
  else { console.log('  (no tile', key + ')'); continue; }
  const dv = new DataView(raw.buffer, raw.byteOffset, raw.byteLength);
  const version = dv.getUint16(4, true);
  const count = dv.getUint32(8, true);
  const vertexTotal = dv.getUint32(12, true);
  const indexTotal = dv.getUint32(16, true);
  const originX = dv.getFloat32(20, true), originZ = dv.getFloat32(24, true);
  const QUANT = dv.getFloat32(28, true);
  let off = 32;
  const vertOffset = new Uint32Array(raw.buffer, raw.byteOffset + off, count); off += 4 * count;
  off += 4 * count;                                   // idxOffset
  const vertCount = new Uint16Array(raw.buffer, raw.byteOffset + off, count); off += 2 * count;
  off += 2 * count;                                   // idxCount
  const baseY = new Int16Array(raw.buffer, raw.byteOffset + off, count); off += 2 * count;
  const topY = new Int16Array(raw.buffer, raw.byteOffset + off, count); off += 2 * count;
  off += count * 2;                                   // palette + seed
  if (version >= 2) off += count * 2;
  if (version >= 3) off += count * 3;
  off = off + (off % 2);
  const verts = new Int16Array(raw.buffer, raw.byteOffset + off, vertexTotal * 2);
  total += count;
  for (let b = 0; b < count; b++) {
    let deepest = 0, anyIn = false;
    for (let k = 0; k < vertCount[b]; k++) {
      const px = originX + verts[(vertOffset[b] + k) * 2] * QUANT;
      const pz = originZ + verts[(vertOffset[b] + k) * 2 + 1] * QUANT;
      if (inside(px, pz, FOOT)) { anyIn = true; deepest = Math.max(deepest, distToEdge(px, pz, FOOT)); }
    }
    if (anyIn) hits.push({ cell: key, idx: b, depth: +deepest.toFixed(2), top: topY[b] / 10, base: baseY[b] / 10 });
  }
}
console.log(`cells ${[...cells].join(',')}  buildings scanned ${total}`);
if (!hits.length) console.log('PASS: no surviving procedural footprint has any vertex inside the asset footprint');
else { console.log(`${hits.length} footprint(s) with vertices inside:`); for (const h of hits.sort((a,b)=>b.depth-a.depth)) console.log('   ', JSON.stringify(h)); }
