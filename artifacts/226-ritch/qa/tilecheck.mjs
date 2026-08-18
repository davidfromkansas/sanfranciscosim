// Decode a buildings tile and measure penetration of every surviving footprint
// into 226 Ritch's real footprint. Truth from the tile, not from the radius.
import { readFileSync } from 'node:fs';
const FILE = process.argv[2];
const buf = readFileSync(FILE);
const dv = new DataView(buf.buffer, buf.byteOffset, buf.byteLength);
const count = dv.getUint32(8, true);
const vertexTotal = dv.getUint32(12, true);
const indexTotal = dv.getUint32(16, true);
const originX = dv.getFloat32(20, true), originZ = dv.getFloat32(24, true);
const QUANT = dv.getFloat32(28, true);
const version = dv.getUint16(4, true);
let off = 32;
const vertOffsetAt = off; off += 4 * count;
const idxOffsetAt = off;  off += 4 * count;
const vertCountAt = off;  off += 2 * count;
const idxCountAt = off;   off += 2 * count;
const baseYAt = off;      off += 2 * count;
const topYAt = off;       off += 2 * count;
off += count; off += count;                       // palette, seed
if (version >= 2) off += 2 * count;
if (version >= 3) off += 3 * count;
off = Math.ceil(off / 2) * 2;
const vertsAt = off;
const vertOffset = new Uint32Array(buf.buffer, buf.byteOffset + vertOffsetAt, count);
const vertCount = new Uint16Array(buf.buffer, buf.byteOffset + vertCountAt, count);
const topY = new Int16Array(buf.buffer, buf.byteOffset + topYAt, count);
const baseY = new Int16Array(buf.buffer, buf.byteOffset + baseYAt, count);
const verts = new Int16Array(buf.buffer, buf.byteOffset + vertsAt, vertexTotal * 2);

// 226 Ritch: DataSF OBB rectangle, app metres (x east, z south)
const CX = 3643.92, CZ = -1153.78;
const B = 135.6 * Math.PI / 180;
const F = [Math.sin(B), -Math.cos(B)];                    // along frontage (SE)
const D = [Math.sin(B + Math.PI / 2), -Math.cos(B + Math.PI / 2)]; // toward rear (SW)
const HF = 12.13 / 2, HD = 22.80 / 2;
function local(x, z) {
  const dx = x - CX, dz = z - CZ;
  return [dx * F[0] + dz * F[1], dx * D[0] + dz * D[1]];
}
// penetration depth of a point into the rectangle (>0 inside)
function pen(x, z) {
  const [u, v] = local(x, z);
  return Math.min(HF - Math.abs(u), HD - Math.abs(v));
}
let worst = null, nearest = Infinity;
for (let i = 0; i < count; i++) {
  const n = vertCount[i], v0 = vertOffset[i];
  let maxPen = -Infinity, cx = 0, cz = 0, minD = Infinity;
  for (let k = 0; k < n; k++) {
    const x = originX + verts[(v0 + k) * 2] * QUANT;
    const z = originZ + verts[(v0 + k) * 2 + 1] * QUANT;
    cx += x; cz += z;
    const p = pen(x, z);
    if (p > maxPen) maxPen = p;
    const d = Math.hypot(x - CX, z - CZ);
    if (d < minD) minD = d;
  }
  cx /= n; cz /= n;
  if (minD < nearest) nearest = minD;
  if (maxPen > (worst?.maxPen ?? -Infinity)) worst = { i, maxPen, cx, cz, n, top: topY[i] / 10, base: baseY[i] / 10, minD };
}
console.log(`tile ${FILE}`);
console.log(`  version ${version}  footprints ${count}  origin ${originX},${originZ}`);
console.log(`  nearest surviving vertex to the anchor: ${nearest.toFixed(2)} m`);
console.log(`  deepest penetration into the 226 Ritch footprint: ${worst.maxPen.toFixed(2)} m`);
console.log(`    (that ring: centroid ${worst.cx.toFixed(1)},${worst.cz.toFixed(1)}  ${worst.n} verts  base ${worst.base} top ${worst.top} m  nearest vertex ${worst.minD.toFixed(2)} m)`);
console.log(worst.maxPen > 0 ? '  RESULT: a footprint reaches INSIDE the asset footprint' : '  RESULT: no surviving footprint reaches inside the asset footprint');
