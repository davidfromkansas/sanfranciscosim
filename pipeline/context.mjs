// Context bake: turns the lore join into what the running city can answer
// questions with — one small sidecar per cell (pick boxes + identity), plus the
// global street, park, landmark, neighbourhood, stats and search indexes.
//
//   out/context/cells/{cx}_{cz}.json  pick index + per-building identity
//   out/context/{streets,parks,landmarks,neighborhoods,stats,search-index}.json
//   out/context/fsq-places.json       server-only place index for the concierge
//
// Published to app/public/tiles/ctx/ and app/public/tiles/context/ (the place
// index goes to app/api/_data/, which never reaches the browser bundle).

import { mkdir, readFile, rm, writeFile } from 'node:fs/promises';
import { CELL_SIZE, GRID, cellIndex, cellOrigin, insideBBox, project } from './lib/geo.mjs';
import { LANDMARKS, VIEW_PRESETS } from './lib/landmarks.mjs';
import { obbBox } from './lib/obb.mjs';
import { polylineLength, ringArea, ringCentroid } from './lib/poly.mjs';
import { CATS, CAT_LABELS, LABELS, NIGHT_PROFILE } from './taxonomy.mjs';

const DATA = new URL('./data/', import.meta.url);
const OUT = new URL('./out/', import.meta.url);
const CTX = new URL('./out/context/', import.meta.url);
const CTX_CELLS = new URL('./out/context/cells/', import.meta.url);
const APP_TILES = new URL('../app/public/tiles/', import.meta.url);
const API_DATA = new URL('../api/_data/', import.meta.url);

const TOY_FLOOR = 3.5;
const MIN_TOY_HEIGHT = 7;
const MAX_TOY_HEIGHT = 200;
const SIDE_CAR_LIMIT = 150 * 1024;
const STREET_STEP = 25; // metres between kept centreline points in a sidecar

const r1 = (n) => Math.round(n * 10) / 10;
const r3 = (n) => Math.round(n * 1000) / 1000;

const readJSON = async (name, base) => JSON.parse(await readFile(new URL(name, base), 'utf8'));

const fp = await readJSON('footprints.json', OUT);
const lore = await readJSON('lore.json', OUT);
const notables = await readJSON('notables.json', OUT);
const notableById = new Map(notables.map((n) => [n.id, n]));
console.log(`${fp.buildings.length} footprints, ${notables.length} notables`);

// ------------------------------------------------------------- cell sidecars
const cells = new Map();
function cellFor(x, z) {
  const idx = cellIndex(x, z);
  if (!idx) return null;
  let cell = cells.get(idx.key);
  if (!cell) {
    cells.set(
      idx.key,
      (cell = {
        key: idx.key,
        cx: idx.cx,
        cz: idx.cz,
        pick: { id: [], x: [], z: [], w: [], d: [], r: [], h: [], y: [], t: [] },
        b: {},
        s: [],
      })
    );
  }
  return cell;
}

const catCount = new Array(CATS.length).fill(0);
for (let id = 0; id < fp.buildings.length; id++) {
  const rec = lore[id];
  if (!rec) continue;
  const [ring, height, baseY] = fp.buildings[id];
  const box = obbBox(ring);
  const cell = cellFor(box.x, box.z);
  if (!cell) continue;
  const floors = Math.max(2, Math.round(height / TOY_FLOOR));
  const toyHeight = Math.min(MAX_TOY_HEIGHT, Math.max(MIN_TOY_HEIGHT, floors * TOY_FLOOR));

  cell.pick.id.push(id);
  cell.pick.x.push(r1(box.x));
  cell.pick.z.push(r1(box.z));
  cell.pick.w.push(r1(box.w));
  cell.pick.d.push(r1(box.d));
  cell.pick.r.push(r3(box.r));
  cell.pick.h.push(r1(height));
  cell.pick.y.push(r1(baseY));
  cell.pick.t.push(r1(toyHeight));

  const entry = { c: rec.cat, f: rec.floors, s: rec.source, cf: rec.confidence };
  if (rec.sub) entry.sc = rec.sub;
  if (rec.name) entry.n = rec.name;
  if (rec.addr) entry.a = rec.addr;
  if (rec.wikidata) entry.w = rec.wikidata;
  // Year built is not in any free citywide SF source, so it is omitted rather
  // than guessed; the card simply does not show a year.
  const notable = notableById.get(id);
  if (notable) entry.t = notable.tier;
  cell.b[id] = entry;
  catCount[rec.cat]++;
}

// --------------------------------------------------------------- street index
const streetsGeo = await readJSON('streets_datasf.geojson', DATA);
const streetsByName = new Map();
let streetPoints = 0;
for (const f of streetsGeo.features) {
  const p = f.properties || {};
  if (p.date_dropped) continue;
  if (p.layer && /PAPER|PROPOSED/i.test(p.layer)) continue;
  const name = (p.streetname || '').trim();
  if (!name) continue;
  const geom = f.geometry;
  if (!geom) continue;
  const lines = geom.type === 'LineString' ? [geom.coordinates] : geom.coordinates || [];
  for (const coords of lines) {
    const pts = [];
    for (const c of coords) {
      if (!insideBBox(c[0], c[1])) continue;
      const [x, z] = project(c[0], c[1]);
      pts.push(x, z);
    }
    if (pts.length < 4) continue;
    const len = polylineLength(pts);
    let rec = streetsByName.get(name);
    if (!rec) {
      streetsByName.set(
        name,
        (rec = { name, nhood: p.analysis_neighborhood || p.nhood || null, len: 0, x: 0, z: 0, n: 0, cells: new Set() })
      );
    }
    rec.len += len;

    // Split into per-cell runs, decimated: the client only needs enough points
    // to measure the distance from a ray hit to the nearest centreline.
    let run = null;
    let runCell = null;
    let since = STREET_STEP;
    for (let i = 0; i < pts.length; i += 2) {
      const x = pts[i];
      const z = pts[i + 1];
      rec.x += x;
      rec.z += z;
      rec.n++;
      const cell = cellFor(x, z);
      if (!cell) continue;
      rec.cells.add(cell.key);
      if (cell !== runCell) {
        run = { n: name, p: [] };
        cell.s.push(run);
        runCell = cell;
        since = STREET_STEP;
      }
      const last = run.p.length;
      if (last >= 2) since += Math.hypot(x - run.p[last - 2], z - run.p[last - 1]);
      if (since < STREET_STEP && i + 2 < pts.length) continue;
      since = 0;
      run.p.push(r1(x), r1(z));
      streetPoints++;
    }
  }
}
// Runs that ended up with a single point cannot be measured against.
for (const cell of cells.values()) cell.s = cell.s.filter((run) => run.p.length >= 4);

const streets = [...streetsByName.values()]
  .filter((s) => s.n > 0)
  .map((s) => ({
    name: s.name,
    nhood: s.nhood,
    len: Math.round(s.len),
    x: r1(s.x / s.n),
    z: r1(s.z / s.n),
    cells: [...s.cells],
  }))
  .sort((a, b) => b.len - a.len);
console.log(`streets: ${streets.length} named, ${streetPoints} sidecar centreline points`);

// ----------------------------------------------------------------- park index
function projectRings(geom) {
  const polys = geom.type === 'Polygon' ? [geom.coordinates] : geom.coordinates || [];
  const rings = [];
  for (const poly of polys) {
    const outer = poly?.[0];
    if (!outer || outer.length < 4) continue;
    const ring = [];
    let inside = false;
    for (const c of outer) {
      if (insideBBox(c[0], c[1])) inside = true;
      const [x, z] = project(c[0], c[1]);
      ring.push(r1(x), r1(z));
    }
    if (inside) rings.push(ring);
  }
  return rings;
}

// Douglas-Peucker would be overkill for click testing: keep every nth vertex,
// which preserves the outline well enough at 1 m tolerance.
function decimate(ring, keep = 4) {
  if (ring.length / 2 <= 8) return ring;
  const out = [];
  for (let i = 0; i < ring.length; i += 2 * keep) out.push(ring[i], ring[i + 1]);
  if (out[0] !== ring[ring.length - 2] || out[1] !== ring[ring.length - 1]) {
    out.push(ring[ring.length - 2], ring[ring.length - 1]);
  }
  return out;
}

const parksRaw = await readJSON('datasf_parks.json', DATA);
const parks = [];
for (const p of parksRaw) {
  if (!p.shape) continue;
  const rings = projectRings(p.shape).map((r) => decimate(r));
  if (!rings.length) continue;
  const lon = parseFloat(p.longitude);
  const lat = parseFloat(p.latitude);
  if (!Number.isFinite(lon) || !Number.isFinite(lat) || !insideBBox(lon, lat)) continue;
  const [x, z] = project(lon, lat);
  parks.push({
    id: `park:${p.property_id || p.objectid}`,
    name: p.property_name,
    type: p.propertytype || null,
    nhood: p.psa || null,
    acres: Math.round(parseFloat(p.acres) || 0),
    x: r1(x),
    z: r1(z),
    rings,
  });
}
console.log(`parks: ${parks.length}`);

// -------------------------------------------------------- neighbourhood index
const nhoodRaw = await readJSON('datasf_neighborhoods.json', DATA);
const neighborhoods = [];
for (const n of nhoodRaw) {
  const rings = projectRings(n.the_geom).map((r) => decimate(r, 6));
  if (!rings.length) continue;
  let area = 0;
  let cx = 0;
  let cz = 0;
  for (const ring of rings) {
    const a = Math.abs(ringArea(ring));
    const [rx, rz] = ringCentroid(ring);
    area += a;
    cx += rx * a;
    cz += rz * a;
  }
  neighborhoods.push({
    id: `nhood:${n.nhood}`,
    name: n.nhood,
    x: r1(cx / (area || 1)),
    z: r1(cz / (area || 1)),
    rings,
  });
}
console.log(`neighborhoods: ${neighborhoods.length}`);

// ------------------------------------------------------------ landmark index
const landmarks = LANDMARKS.map((l) => {
  const [x, z] = project(l.lon, l.lat);
  return { id: `landmark:${l.id}`, name: l.name, x: r1(x), z: r1(z), height: l.height ?? null, camera: l.camera };
});
const views = VIEW_PRESETS.map((v) => {
  const [x, z] = project(v.lon, v.lat);
  return { id: `view:${v.id}`, name: v.name, x: r1(x), z: r1(z), camera: v.camera };
});

// ------------------------------------------------------------- search index
// One flat, pre-normalised list: the client lowercases the query and does a
// prefix/substring scan over it, so search never touches the network.
const search = [];
const pushSearch = (entry) => search.push({ ...entry, q: entry.n.toLowerCase() });
for (const l of landmarks) pushSearch({ n: l.name, t: 'landmark', id: l.id, x: l.x, z: l.z });
for (const v of views) pushSearch({ n: v.name, t: 'view', id: v.id, x: v.x, z: v.z });
for (const n of neighborhoods) pushSearch({ n: n.name, t: 'neighborhood', id: n.id, x: n.x, z: n.z });
for (const p of parks) pushSearch({ n: p.name, t: 'park', id: p.id, x: p.x, z: p.z });
for (const s of streets) pushSearch({ n: s.name, t: 'street', id: `street:${s.name}`, x: s.x, z: s.z });
for (const n of notables) {
  if (n.needs_review) continue;
  const [ring, height, baseY] = fp.buildings[n.id];
  const box = obbBox(ring);
  pushSearch({
    n: n.name,
    t: 'building',
    id: `b:${n.id}`,
    x: r1(box.x),
    z: r1(box.z),
    c: n.cat,
    h: r1(baseY + height),
    tier: n.tier,
  });
}
console.log(`search index: ${search.length} entries`);

// ----------------------------------------------------------------- city stats
const stats = {
  generated: new Date().toISOString(),
  buildings: Object.keys(lore).length,
  cells: cells.size,
  categories: CATS.map((c, i) => ({ cat: i, id: c, label: CAT_LABELS[i], count: catCount[i], night: NIGHT_PROFILE[i] })),
  subcategories: (() => {
    const h = new Map();
    for (const rec of Object.values(lore)) if (rec.sub) h.set(rec.sub, (h.get(rec.sub) || 0) + 1);
    return [...h.entries()]
      .sort((a, b) => b[1] - a[1])
      .map(([sub, count]) => ({ sub, label: LABELS[sub] || sub, count }));
  })(),
  sources: (() => {
    const h = new Map();
    for (const rec of Object.values(lore)) h.set(rec.source, (h.get(rec.source) || 0) + 1);
    return Object.fromEntries(h);
  })(),
  confidence: (() => {
    const h = [0, 0, 0, 0];
    for (const rec of Object.values(lore)) h[rec.confidence]++;
    return h;
  })(),
  streets: { named: streets.length, km: Math.round(streets.reduce((a, s) => a + s.len, 0) / 1000) },
  parks: parks.length,
  neighborhoods: neighborhoods.length,
  notables: { total: notables.length, tierA: notables.filter((n) => n.tier === 'A').length },
  attribution: [
    'Building footprints, streets, facilities, schools, business registry, land use, parks and neighbourhoods: DataSF (data.sfgov.org)',
    'Tags and names: OpenStreetMap contributors (ODbL)',
    'Places: Overture Maps Foundation (which distributes the Foursquare open places records)',
  ],
};

// ---------------------------------------------- server-only place index (FSQ)
// Names, categories and addresses for the concierge's place lookups. It stays
// out of app/public so it never ships in the browser bundle.
const places = [];
{
  const overture = await readJSON('overture_places.geojson', DATA);
  for (const f of overture.features) {
    const p = f.properties || {};
    const coords = f.geometry?.coordinates;
    const name = p.names?.primary;
    if (!coords || !name || !insideBBox(coords[0], coords[1])) continue;
    if ((p.confidence ?? 0) < 0.5) continue;
    const [x, z] = project(coords[0], coords[1]);
    places.push({
      n: name,
      c: p.categories?.primary || null,
      a: p.addresses?.[0]?.freeform || null,
      x: Math.round(x),
      z: Math.round(z),
    });
  }
}
console.log(`server place index: ${places.length}`);

// -------------------------------------------------------------------- write
await rm(CTX, { recursive: true, force: true });
await mkdir(CTX_CELLS, { recursive: true });

let sidecarBytes = 0;
let largest = { key: null, bytes: 0 };
const cellIndexOut = [];
for (const key of [...cells.keys()].sort()) {
  const cell = cells.get(key);
  const body = JSON.stringify({ v: 1, pick: cell.pick, b: cell.b, s: cell.s });
  await writeFile(new URL(`${key}.json`, CTX_CELLS), body);
  sidecarBytes += body.length;
  if (body.length > largest.bytes) largest = { key, bytes: body.length };
  const [originX, originZ] = cellOrigin(cell.cx, cell.cz);
  cellIndexOut.push({
    key,
    cx: cell.cx,
    cz: cell.cz,
    originX,
    originZ,
    buildings: cell.pick.id.length,
    streets: cell.s.length,
    bytes: body.length,
  });
}

await writeFile(new URL('streets.json', CTX), JSON.stringify(streets));
await writeFile(new URL('parks.json', CTX), JSON.stringify(parks));
await writeFile(new URL('landmarks.json', CTX), JSON.stringify({ landmarks, views }));
await writeFile(new URL('neighborhoods.json', CTX), JSON.stringify(neighborhoods));
await writeFile(new URL('stats.json', CTX), JSON.stringify(stats, null, 1));
await writeFile(new URL('search-index.json', CTX), JSON.stringify(search));
await writeFile(new URL('fsq-places.json', CTX), JSON.stringify(places));
await writeFile(
  new URL('context.json', OUT),
  JSON.stringify(
    { cellSize: CELL_SIZE, grid: GRID, stats: { sidecarBytes, cells: cellIndexOut.length }, cells: cellIndexOut },
    null,
    1
  )
);

// ------------------------------------------------------------------ publish
const ctxDst = new URL('ctx/', APP_TILES);
const contextDst = new URL('context/', APP_TILES);
await rm(ctxDst, { recursive: true, force: true });
await rm(contextDst, { recursive: true, force: true });
await mkdir(ctxDst, { recursive: true });
await mkdir(contextDst, { recursive: true });
await mkdir(API_DATA, { recursive: true });
for (const entry of cellIndexOut) {
  await writeFile(new URL(`${entry.key}.json`, ctxDst), await readFile(new URL(`${entry.key}.json`, CTX_CELLS)));
}
for (const name of ['streets.json', 'parks.json', 'landmarks.json', 'neighborhoods.json', 'stats.json', 'search-index.json']) {
  await writeFile(new URL(name, contextDst), await readFile(new URL(name, CTX)));
}
await writeFile(new URL('context.json', APP_TILES), await readFile(new URL('context.json', OUT)));
// The concierge reads these from disk beside the function; the place index in
// particular must not be reachable from the browser.
await writeFile(new URL('places.json', API_DATA), await readFile(new URL('fsq-places.json', CTX)));
for (const name of ['streets.json', 'parks.json', 'neighborhoods.json', 'stats.json', 'search-index.json']) {
  await writeFile(new URL(name, API_DATA), await readFile(new URL(name, CTX)));
}

// ------------------------------------------------------------------ validate
const failures = [];
function check(label, ok, detail) {
  console.log(`  ${ok ? 'ok  ' : 'FAIL'} ${label} — ${detail}`);
  if (!ok) failures.push(label);
}
console.log('\ncontext validation');
check('every sidecar <= 150 KB', largest.bytes <= SIDE_CAR_LIMIT, `largest ${largest.key} at ${(largest.bytes / 1024).toFixed(1)} KB`);
check(
  'every building has a pick box and an identity',
  cellIndexOut.reduce((a, c) => a + c.buildings, 0) === Object.keys(lore).length,
  `${cellIndexOut.reduce((a, c) => a + c.buildings, 0)} / ${Object.keys(lore).length}`
);
check('41 analysis neighbourhoods', neighborhoods.length === 41, `${neighborhoods.length}`);
check('search index covers every notable', search.filter((s) => s.t === 'building').length === notables.filter((n) => !n.needs_review).length, `${search.filter((s) => s.t === 'building').length}`);
console.log(
  `\ncontext: ${cellIndexOut.length} sidecars, ${(sidecarBytes / 1e6).toFixed(1)} MB total, avg ${(
    sidecarBytes /
    cellIndexOut.length /
    1024
  ).toFixed(1)} KB`
);
if (failures.length) {
  console.error(`\nCONTEXT VALIDATION FAILED: ${failures.join(', ')}`);
  process.exit(1);
}
