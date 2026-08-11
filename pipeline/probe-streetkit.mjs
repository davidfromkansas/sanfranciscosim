// Dry-runs the layer 2 furniture planner over real toy street tiles, without a
// browser: same module the tile worker imports, same blobs the app streams.
//
//   node pipeline/probe-streetkit.mjs 9_21 12_16
//
// Prints the piece mix and the sanity numbers that are awkward to eyeball in
// the app: distance from the kerb, spacing, and anything placed off a sidewalk.

import { readFile } from 'node:fs/promises';
import { PIECES, planStreetFurniture, ANCHOR_STRIDE } from '../app/src/streetplan.js';
import { readStreets } from '../app/src/tilebin.js';

const TILES = new URL('../app/public/tiles/', import.meta.url);
const toy = JSON.parse(await readFile(new URL('toy.json', TILES), 'utf8'));
const ctxCells = process.argv.slice(2);
if (!ctxCells.length) {
  console.error('usage: node pipeline/probe-streetkit.mjs <cell> [cell…]');
  process.exit(2);
}

const roads = [];
const sidewalks = [];
for (const key of ctxCells) {
  const buf = await readFile(new URL(`toystreets/${key}.bin`, TILES));
  const d = readStreets(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength));
  for (let l = 0; l < d.count; l++) {
    const n = d.ptCount[l];
    if (n < 2) continue;
    const cls = toy.streetClasses[d.klass[l]] || toy.streetClasses[6];
    const isSidewalk = cls.profile === 'curb';
    if (!isSidewalk && (cls.detail || !cls.sidewalk)) continue;
    const po = d.ptOffset[l];
    const px = new Float64Array(n);
    const py = new Float64Array(n);
    const pz = new Float64Array(n);
    for (let k = 0; k < n; k++) {
      px[k] = d.originX + d.xz[(po + k) * 2] * d.quant;
      pz[k] = d.originZ + d.xz[(po + k) * 2 + 1] * d.quant;
      py[k] = d.y[po + k] * 0.1;
    }
    if (isSidewalk) sidewalks.push({ px, py, pz, n });
    else roads.push({ px, py, pz, n, klass: d.klass[l], width: cls.width, sidewalk: cls.sidewalk });
  }
}

// Market Street and the shopfronts, exactly as the app derives them.
const market = [];
const commercial = [];
const SHOPS = new Set([4, 5, 6, 7, 15, 16, 17, 22, 24]);
for (const key of ctxCells) {
  const cell = JSON.parse(await readFile(new URL(`ctx/${key}.json`, TILES), 'utf8'));
  for (const run of cell.s || []) {
    if (run.n !== 'MARKET ST') continue;
    for (let i = 2; i < run.p.length; i += 2) {
      market.push(run.p[i - 2], run.p[i - 1], run.p[i], run.p[i + 1]);
    }
  }
  for (let i = 0; i < cell.pick.id.length; i++) {
    const info = cell.b[cell.pick.id[i]];
    if (info && SHOPS.has(info.c)) commercial.push(cell.pick.x[i], cell.pick.z[i]);
  }
}

const t0 = performance.now();
const anchors = planStreetFurniture({
  roads,
  sidewalks,
  market: new Float32Array(market),
  commercial: new Float32Array(commercial),
  exclusions: new Float32Array(0),
  limit: 100000,
});
const ms = performance.now() - t0;

const counts = new Map();
for (let i = 0; i < anchors.length; i += ANCHOR_STRIDE) {
  const id = PIECES[anchors[i]];
  counts.set(id, (counts.get(id) || 0) + 1);
}

// Determinism: the same inputs must give a byte-identical layout.
const again = planStreetFurniture({
  roads,
  sidewalks,
  market: new Float32Array(market),
  commercial: new Float32Array(commercial),
  exclusions: new Float32Array(0),
  limit: 100000,
});
const stable = again.length === anchors.length && again.every((v, i) => v === anchors[i]);

// Nearest baked sidewalk vertex per anchor: how far a piece stands from proven
// footway. The parklet is meant to be off it, in the parking lane.
let worst = 0;
let worstId = '';
for (let i = 0; i < anchors.length; i += ANCHOR_STRIDE) {
  if (PIECES[anchors[i]] === 'parklet') continue;
  let best = Infinity;
  for (const line of sidewalks) {
    for (let k = 0; k < line.n; k++) {
      const d = Math.hypot(line.px[k] - anchors[i + 1], line.pz[k] - anchors[i + 3]);
      if (d < best) best = d;
    }
  }
  if (best > worst) {
    worst = best;
    worstId = PIECES[anchors[i]];
  }
}

console.log(`[probe] cells ${ctxCells.join(',')}: ${roads.length} roads, ${sidewalks.length} sidewalk runs`);
console.log(`[probe] ${anchors.length / ANCHOR_STRIDE} anchors in ${ms.toFixed(1)} ms, deterministic=${stable}`);
for (const id of PIECES) console.log(`[probe]   ${id.padEnd(15)} ${counts.get(id) || 0}`);
console.log(`[probe] furthest piece from a baked sidewalk vertex: ${worst.toFixed(2)} m (${worstId})`);
