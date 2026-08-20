// Decode a buildings tile and measure what is still standing on Four Embarcadero
// Center's site. Truth from the tile, not from the exclusion radius.
//
// Two metrics, because on this site the usual one lies:
//
//   overlap AREA  -- the headline. The DataSF ring here (3,142 m2) is LARGER
//     than the OSM footprint (2,170 m2) and encloses it, so every one of its
//     vertices sits OUTSIDE the 4EC ring and a vertex-penetration test reports
//     -0.30 m, "nothing inside", while a 168.6 m procedural block stands on the
//     exact site. Area is measured by sampling a 0.25 m grid over the footprint
//     and counting cells inside both rings, which is shape-agnostic: the 4EC
//     plan is a staircase, so no OBB or convex-clip test would work either.
//
//   penetration DEPTH -- kept as the secondary reading, because a party wall
//     shares a survey vertex and a containment boolean would flag it. Signed:
//     + inside the footprint, - outside.
//
//   node tilecheck.mjs <app/public/tiles/buildings/23_10.bin>
import { readFileSync } from 'node:fs';

const FILE = process.argv[2];
const buf = readFileSync(FILE);
const dv = new DataView(buf.buffer, buf.byteOffset, buf.byteLength);
const version = dv.getUint16(4, true);
const count = dv.getUint32(8, true);
const vertexTotal = dv.getUint32(12, true);
const originX = dv.getFloat32(20, true), originZ = dv.getFloat32(24, true);
const QUANT = dv.getFloat32(28, true);
let off = 32;
const vertOffsetAt = off; off += 4 * count;
off += 4 * count;                                  // idxOffset
const vertCountAt = off;  off += 2 * count;
off += 2 * count;                                  // idxCount
const baseYAt = off;      off += 2 * count;
const topYAt = off;       off += 2 * count;
off += count; off += count;                        // palette, seed
if (version >= 2) off += 2 * count;
if (version >= 3) off += 3 * count;
off = Math.ceil(off / 2) * 2;
const vertOffset = new Uint32Array(buf.buffer, buf.byteOffset + vertOffsetAt, count);
const vertCount = new Uint16Array(buf.buffer, buf.byteOffset + vertCountAt, count);
const baseY = new Int16Array(buf.buffer, buf.byteOffset + baseYAt, count);
const topY = new Int16Array(buf.buffer, buf.byteOffset + topYAt, count);
const verts = new Int16Array(buf.buffer, buf.byteOffset + off, vertexTotal * 2);

// OSM way/616812910, projected into app metres (x east, z south).
const LON0 = -122.4375, LAT0 = 37.77;
const project = (lon, lat) => [
  (lon - LON0) * 111320 * Math.cos((LAT0 * Math.PI) / 180),
  -(lat - LAT0) * 110540,
];
const RING_LL = [
  [-122.3965598, 37.7953758], [-122.3965472, 37.7953133], [-122.3965669, 37.7953109],
  [-122.396556, 37.7952574], [-122.3965391, 37.7952595], [-122.3965297, 37.7952131],
  [-122.396519, 37.7951569], [-122.3965061, 37.7950909], [-122.3958691, 37.7951704],
  [-122.3958825, 37.7952371], [-122.3958547, 37.7952406], [-122.395866, 37.7952969],
  [-122.3958349, 37.7953008], [-122.3958455, 37.7953534], [-122.3958727, 37.7953499],
  [-122.3958823, 37.7953974], [-122.3958889, 37.7953966], [-122.3959015, 37.795459],
  [-122.3959215, 37.7954557], [-122.3959311, 37.795504], [-122.3960688, 37.7954869],
  [-122.3965073, 37.7954327], [-122.3964977, 37.7953843],
];
const RING = RING_LL.map(([lo, la]) => project(lo, la));
const [AX, AZ] = project(-122.3961998, 37.7953001);

const inside = (x, z) => {
  let c = false;
  for (let i = 0, j = RING.length - 1; i < RING.length; j = i++) {
    const [xi, zi] = RING[i], [xj, zj] = RING[j];
    if ((zi > z) !== (zj > z) && x < ((xj - xi) * (z - zi)) / (zj - zi) + xi) c = !c;
  }
  return c;
};
const distToEdge = (x, z) => {
  let best = Infinity;
  for (let i = 0, j = RING.length - 1; i < RING.length; j = i++) {
    const [x1, z1] = RING[j], [x2, z2] = RING[i];
    const dx = x2 - x1, dz = z2 - z1;
    const t = Math.max(0, Math.min(1, ((x - x1) * dx + (z - z1) * dz) / (dx * dx + dz * dz || 1)));
    best = Math.min(best, Math.hypot(x - (x1 + t * dx), z - (z1 + t * dz)));
  }
  return best;
};
// signed penetration: + inside the footprint, - outside
const pen = (x, z) => (inside(x, z) ? distToEdge(x, z) : -distToEdge(x, z));

// 0.25 m sample grid over the 4EC footprint, precomputed once
const STEP = 0.25;
const xs = RING.map((p) => p[0]), zs = RING.map((p) => p[1]);
const GX0 = Math.min(...xs), GX1 = Math.max(...xs);
const GZ0 = Math.min(...zs), GZ1 = Math.max(...zs);
const SAMPLES = [];
for (let x = GX0 + STEP / 2; x < GX1; x += STEP) {
  for (let z = GZ0 + STEP / 2; z < GZ1; z += STEP) if (inside(x, z)) SAMPLES.push([x, z]);
}
const FOOTPRINT_AREA = SAMPLES.length * STEP * STEP;

const insidePoly = (x, z, poly) => {
  let c = false;
  for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) {
    const [xi, zi] = poly[i], [xj, zj] = poly[j];
    if ((zi > z) !== (zj > z) && x < ((xj - xi) * (z - zi)) / (zj - zi) + xi) c = !c;
  }
  return c;
};

let worstArea = null, worstPen = null, nearest = Infinity;
for (let i = 0; i < count; i++) {
  const n = vertCount[i], v0 = vertOffset[i];
  const poly = [];
  let maxPen = -Infinity, cx = 0, cz = 0, minD = Infinity;
  for (let k = 0; k < n; k++) {
    const x = originX + verts[(v0 + k) * 2] * QUANT;
    const z = originZ + verts[(v0 + k) * 2 + 1] * QUANT;
    poly.push([x, z]); cx += x; cz += z;
    const p = pen(x, z);
    if (p > maxPen) maxPen = p;
    minD = Math.min(minD, Math.hypot(x - AX, z - AZ));
  }
  cx /= n; cz /= n;
  nearest = Math.min(nearest, minD);
  const row = { i, maxPen, cx, cz, n, base: baseY[i] / 10, top: topY[i] / 10, minD };

  // cheap reject: a ring whose nearest vertex is beyond the footprint's reach
  // and whose centroid is outside cannot overlap
  let area = 0;
  if (minD < 80 || insidePoly(AX, AZ, poly)) {
    let hits = 0;
    for (const [x, z] of SAMPLES) if (insidePoly(x, z, poly)) hits++;
    area = hits * STEP * STEP;
  }
  row.area = area;
  if (area > (worstArea?.area ?? -1)) worstArea = row;
  if (maxPen > (worstPen?.maxPen ?? -Infinity)) worstPen = row;
}

const fmt = (r) => `centroid ${r.cx.toFixed(1)},${r.cz.toFixed(1)}  ${r.n} verts  base ${r.base} top ${r.top} m  nearest vertex ${r.minD.toFixed(2)} m`;
console.log(`tile ${FILE}`);
console.log(`  version ${version}  footprints ${count}  origin ${originX},${originZ}`);
console.log(`  4EC footprint area (sampled): ${FOOTPRINT_AREA.toFixed(0)} m2`);
console.log(`  nearest surviving vertex to the anchor: ${nearest.toFixed(2)} m`);
console.log(`  LARGEST OVERLAP: ${worstArea.area.toFixed(1)} m2 (${((100 * worstArea.area) / FOOTPRINT_AREA).toFixed(1)}% of the footprint)`);
console.log(`    ${fmt(worstArea)}`);
console.log(`  deepest vertex penetration: ${worstPen.maxPen.toFixed(2)} m`);
console.log(`    ${fmt(worstPen)}`);
console.log(worstArea.area > 1
  ? `  RESULT: a procedural footprint still covers ${((100 * worstArea.area) / FOOTPRINT_AREA).toFixed(1)}% of the asset site`
  : '  RESULT: the asset site is clear — no surviving footprint overlaps it');
