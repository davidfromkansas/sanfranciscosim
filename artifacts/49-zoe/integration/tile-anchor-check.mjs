// Settle the 49 Zoe exclusion FROM THE TILE, not from verify-rebake's per-cell
// count. That count is unreliable when the pipeline/data snapshot differs in
// vintage from the one origin/main was baked with — one dropped and one added
// cancel out (sf3d-verify-rebake-count-blindspot, 164-south-park 2026-08-18).
//
// The question is not "did the count move" but "does any baked ring still cover
// the anchor, or penetrate the exclusion circle?" — because a procedural block
// taller than the asset would swallow it entirely, and no inspection of the GLB
// could ever reveal that.
//
//   node artifacts/49-zoe/integration/tile-anchor-check.mjs
//
// Decoder lifted from pipeline/verify-rebake.mjs (buildings blob v3 layout).
import { execFileSync } from 'node:child_process';
import { readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const REPO = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..');
const CELL_FILE = 'app/public/tiles/buildings/23_13.bin';
const LON = -122.3960338, LAT = 37.7800764, RADIUS = 9.5;

const LON0 = -122.4375, LAT0 = 37.77;
const K = 111320 * Math.cos((LAT0 * Math.PI) / 180);
const project = (lon, lat) => [(lon - LON0) * K, -(lat - LAT0) * 110540];

function footprints(buf) {
  const dv = new DataView(buf.buffer, buf.byteOffset, buf.byteLength);
  const version = dv.getUint16(4, true);
  const count = dv.getUint32(8, true);
  const vertexTotal = dv.getUint32(12, true);
  const originX = dv.getFloat32(20, true);
  const originZ = dv.getFloat32(24, true);
  const quant = dv.getFloat32(28, true);
  let off = 32;
  const vertOffsetAt = off; off += 4 * count; off += 4 * count;
  const vertCountAt = off; off += 2 * count; off += 2 * count;
  const baseYAt = off; off += 2 * count;
  const topYAt = off; off += 2 * count;
  off += 2 * count;
  if (version >= 2) off += 2 * count;
  if (version >= 3) off += 3 * count;
  off = Math.ceil(off / 2) * 2;
  const vertsAt = off;
  const out = [];
  for (let i = 0; i < count; i++) {
    const vo = dv.getUint32(vertOffsetAt + 4 * i, true);
    const vc = dv.getUint16(vertCountAt + 2 * i, true);
    const ring = [];
    for (let k = 0; k < vc; k++) {
      const p = vertsAt + (vo + k) * 4;
      ring.push([originX + dv.getInt16(p, true) * quant, originZ + dv.getInt16(p + 2, true) * quant]);
    }
    out.push({ ring, height: (dv.getInt16(topYAt + 2 * i, true) - dv.getInt16(baseYAt + 2 * i, true)) / 10 });
  }
  return out;
}

const covers = (ring, [px, pz]) => {
  let inside = false;
  for (let i = 0, j = ring.length - 1; i < ring.length; j = i++) {
    const [xi, zi] = ring[i], [xj, zj] = ring[j];
    if ((zi > pz) !== (zj > pz) && px < ((xj - xi) * (pz - zi)) / (zj - zi) + xi) inside = !inside;
  }
  return inside;
};

function report(label, buf) {
  const a = project(LON, LAT);
  const rings = footprints(buf);
  const covering = rings.filter((r) => covers(r.ring, a));
  let nearest = Infinity, nearestH = null;
  let intruding = 0;
  for (const r of rings) {
    let d = Math.hypot(
      r.ring.reduce((s, p) => s + p[0], 0) / r.ring.length - a[0],
      r.ring.reduce((s, p) => s + p[1], 0) / r.ring.length - a[1]
    );
    for (const [x, z] of r.ring) d = Math.min(d, Math.hypot(x - a[0], z - a[1]));
    if (d < RADIUS) intruding++;
    if (d < nearest) { nearest = d; nearestH = r.height; }
  }
  console.log(`${label.padEnd(14)} rings ${String(rings.length).padStart(4)}` +
    `  covering anchor ${covering.length}${covering.length ? ' (h ' + covering.map((c) => c.height.toFixed(1)).join(', ') + ' m)' : ''}` +
    `  inside r=${RADIUS} ${intruding}` +
    `  nearest ${nearest.toFixed(2)} m (h ${nearestH?.toFixed(1)} m)`);
  return { rings: rings.length, covering: covering.length, intruding, nearest, nearestH };
}

const before = report('origin/main', execFileSync('git', ['show', `origin/main:${CELL_FILE}`], { cwd: REPO, maxBuffer: 1 << 28 }));
const after = report('re-baked', readFileSync(path.join(REPO, CELL_FILE)));

const ok = after.covering === 0 && after.intruding === 0 && after.nearest > RADIUS;
console.log(`\n${ok ? 'PASS' : 'FAIL'}  nothing covers the anchor and nothing penetrates the ${RADIUS} m circle`);
console.log(`      before: ${before.covering} ring(s) covering at ${before.covering ? before.nearestH.toFixed(1) + ' m tall' : '-'};` +
  ` the asset is 17.0 m, so an un-excluded ${before.covering ? 'block' : 'site'} would have ${before.covering && before.nearestH > 17 ? 'SWALLOWED it' : 'clashed with it'}`);
process.exit(ok ? 0 : 1);
