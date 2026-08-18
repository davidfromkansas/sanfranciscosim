// Stage-5 exclusion measurement for 164 South Park.
//
// Measures the safe window for `exclude` against the bake's OWN input — DataSF
// first, Overture gap-fill, both simplified at buildings.mjs's SIMPLIFY_TOLERANCE
// — rather than against the live APIs, and discounts neighbours already dropped
// by an existing landmark's zone because a GLB stands in their place.
//
//   cd pipeline && node ../artifacts/164-south-park/integration/measure-exclusion.mjs
//
// Needs pipeline/data/ present. Reads only.

import { createReadStream, existsSync } from 'node:fs';
import { createInterface } from 'node:readline';
import { project } from '../../../pipeline/lib/geo.mjs';
import { ringArea, ringBBox, ringCentroid, simplifyRing } from '../../../pipeline/lib/poly.mjs';
import { streamFeatures, outerRings } from '../../../pipeline/lib/geojsonStream.mjs';
import { LANDMARKS } from '../../../pipeline/lib/landmarks.mjs';

const TOL = 0.6;
const DATA = new URL('../../../pipeline/data/', import.meta.url);

const CANDS = {
  'parcel-union centroid': [-122.3949238, 37.7812072],
  'DataSF LiDAR centroid': [-122.3949327, 37.7812123],
  'OSM way centroid':      [-122.3949502, 37.7812178],
  'model manifest anchor': [-122.3949366, 37.7812097],
};
const A = {};
for (const [k, [lo, la]] of Object.entries(CANDS)) { const [x, z] = project(lo, la); A[k] = [x, z]; }

// existing landmark exclusions (so already-covered neighbours are discounted)
const EX = LANDMARKS.filter(l => l.exclude).map(l => { const [x, z] = project(l.lon, l.lat); return { id: l.id, x, z, r2: l.exclude * l.exclude }; });

function projectRing(coords) { const out = []; for (const c of coords) { if (!Number.isFinite(c[0]) || !Number.isFinite(c[1])) continue; const [x, z] = project(c[0], c[1]); out.push(x, z); } return out; }
function covered(ring, cx, cz) { for (const e of EX) { if ((cx - e.x) ** 2 + (cz - e.z) ** 2 < e.r2) return e.id; for (let i = 0; i < ring.length; i += 2) if ((ring[i] - e.x) ** 2 + (ring[i + 1] - e.z) ** 2 < e.r2) return e.id; } return null; }

const rows = [];
function consider(ring, src, tag) {
  const r = simplifyRing(ring, TOL);
  if (r.length / 2 < 3) return;
  if (Math.abs(ringArea(r)) < 12) return;
  const [cx, cz] = ringCentroid(r);
  // only things near us
  const [ax, az] = A['parcel-union centroid'];
  if ((cx - ax) ** 2 + (cz - az) ** 2 > 60 * 60) {
    let near = false;
    for (let i = 0; i < r.length; i += 2) if ((r[i] - ax) ** 2 + (r[i + 1] - az) ** 2 < 60 * 60) { near = true; break; }
    if (!near) return;
  }
  const d = {};
  for (const [k, [x, z]] of Object.entries(A)) {
    let v = Infinity;
    for (let i = 0; i < r.length; i += 2) v = Math.min(v, Math.hypot(r[i] - x, r[i + 1] - z));
    d[k] = { vert: v, cent: Math.hypot(cx - x, cz - z) };
  }
  rows.push({ src, tag, area: Math.abs(ringArea(r)), cx, cz, d, cov: covered(r, cx, cz) });
}

let n = 0;
for await (const f of streamFeatures(new URL('buildings_datasf.geojson', DATA).pathname)) {
  n++;
  const p = f.properties || {};
  for (const ring of outerRings(f.geometry)) { const pr = projectRing(ring); if (pr.length >= 6) consider(pr, 'datasf', p.mblr || `#${n}`); }
}
console.log('datasf features', n, 'near rows', rows.length);

const op = new URL('overture_buildings.geojsonseq', DATA).pathname;
if (existsSync(op)) {
  const rl = createInterface({ input: createReadStream(op, { encoding: 'utf8' }), crlfDelay: Infinity });
  let m = 0;
  for await (const line of rl) {
    if (!line.trim()) continue;
    let f; try { f = JSON.parse(line); } catch { continue; }
    const g = f.geometry; if (!g) continue;
    const polys = g.type === 'Polygon' ? [g.coordinates] : g.coordinates || [];
    for (const poly of polys) {
      const outer = poly && poly[0]; if (!outer || outer.length < 4) continue;
      const lon = outer[0][0], lat = outer[0][1];
      if (Math.abs(lon + 122.3949) > 0.003 || Math.abs(lat - 37.7812) > 0.003) continue;
      const pr = projectRing(outer); if (pr.length >= 6) consider(pr, 'overture', (f.id || '').slice(0, 10));
      m++;
    }
  }
  console.log('overture polys near', m);
}

const OWN = r => (r.src === 'datasf' && r.tag === 'SF3775069') || (r.src === 'overture' && r.d['parcel-union centroid'].cent < 3.2 && r.area > 400);
for (const k of Object.keys(A)) {
  let floor = 0, fl = '', ceil = Infinity, cl = '';
  for (const r of rows) {
    if (OWN(r)) { if (r.d[k].cent > floor) { floor = r.d[k].cent; fl = `${r.src} ${r.tag}`; } }
    else if (!r.cov) { if (r.d[k].vert < ceil) { ceil = r.d[k].vert; cl = `${r.src} ${r.tag}`; } }
  }
  console.log(`\n=== ${k}  (${CANDS[k]})`);
  console.log(`  floor ${floor.toFixed(2)} m  (${fl} centroid)   ceiling ${ceil.toFixed(2)} m  (${cl} vertex)   window ${(ceil - floor).toFixed(2)} m`);
  rows.slice().sort((a, b) => Math.min(a.d[k].vert, a.d[k].cent) - Math.min(b.d[k].vert, b.d[k].cent)).slice(0, 10)
    .forEach(r => console.log(`     ${(r.src + ' ' + r.tag).padEnd(22)} area ${r.area.toFixed(0).padStart(5)}  vert ${r.d[k].vert.toFixed(2).padStart(6)}  cent ${r.d[k].cent.toFixed(2).padStart(6)}  ${OWN(r) ? 'OWN' : (r.cov ? 'covered-by ' + r.cov : '-')}`));
}
