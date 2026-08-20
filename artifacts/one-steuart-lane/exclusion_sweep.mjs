// Size One Steuart Lane's `exclude` radius against BOTH bake inputs, applying
// excluded()'s real test: a ring is dropped when its centroid OR ANY vertex
// falls inside r of the landmark ANCHOR. Overture is newline-delimited JSON and
// must be read the way buildings.mjs reads it — streamFeatures() silently
// yields zero features from a .geojsonseq.
//   node artifacts/one-steuart-lane/exclusion_sweep.mjs
// Needs pipeline/data/ populated (npm run download).
import { createReadStream } from 'node:fs';
import { createInterface } from 'node:readline';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { streamFeatures, outerRings } from '../../pipeline/lib/geojsonStream.mjs';

const DATA = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../pipeline/data');
const at = (f) => path.join(DATA, f);

const LON0 = -122.4375, LAT0 = 37.77;
const K = 111320 * Math.cos(LAT0 * Math.PI / 180);
const project = (lon, lat) => [(lon - LON0) * K, -(lat - LAT0) * 110540];
const [AX, AZ] = project(-122.3916888, 37.7915643);
const rows = [];

function consider(src, outer, props) {
  let near = Infinity, cx = 0, cz = 0, n = 0;
  for (const c of outer) {
    if (!Number.isFinite(c[0]) || !Number.isFinite(c[1])) continue;
    const [x, z] = project(c[0], c[1]);
    const d = Math.hypot(x - AX, z - AZ);
    if (d > 500) return;
    if (d < near) near = d;
    cx += x; cz += z; n++;
  }
  if (!n) return;
  cx /= n; cz /= n;
  const centroid = Math.hypot(cx - AX, cz - AZ);
  const gate = Math.min(near, centroid);
  if (gate < 60) rows.push({ src, gate, near, centroid, verts: n, props });
}

for await (const f of streamFeatures(at('buildings_datasf.geojson'))) {
  for (const ring of outerRings(f.geometry)) {
    const p = f.properties ?? {};
    consider('datasf', ring, `mblr=${p.mblr ?? '?'} medh=${p.hgt_median_m ?? '?'}`);
  }
}

const rl = createInterface({ input: createReadStream(at('overture_buildings.geojsonseq'), { encoding: 'utf8' }), crlfDelay: Infinity });
for await (const line of rl) {
  if (!line.trim()) continue;
  let f; try { f = JSON.parse(line); } catch { continue; }
  const g = f.geometry; if (!g) continue;
  const polys = g.type === 'Polygon' ? [g.coordinates] : g.coordinates || [];
  for (const poly of polys) {
    const outer = poly && poly[0];
    if (!outer || outer.length < 4) continue;
    const p = f.properties ?? {};
    consider('overture', outer, `h=${p.height ?? p.num_floors ?? '?'} names=${JSON.stringify(p.names ?? '')}`.slice(0, 90));
  }
}

rows.sort((a, b) => a.gate - b.gate);
console.log('rings whose GATE (= min(nearest vertex, centroid) from the anchor) is under 60 m:\n');
for (const r of rows)
  console.log(`${r.gate.toFixed(2).padStart(7)}  [near ${r.near.toFixed(2).padStart(6)} / centroid ${r.centroid.toFixed(2).padStart(6)}]  ${r.src.padEnd(9)} v=${String(r.verts).padStart(4)}  ${r.props}`);

console.log('\nradius sweep:');
let prev = -1;
for (let r = 1; r <= 45; r++) {
  const d = rows.filter(x => x.gate < r);
  if (d.length !== prev) {
    console.log(`  r=${String(r).padStart(2)}  drops ${d.length}:  ${d.map(x => `${x.src}@${x.gate.toFixed(1)}`).join(', ') || '(nothing)'}`);
    prev = d.length;
  }
}
