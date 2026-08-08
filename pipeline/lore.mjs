// Building identity join. Reads the cleaned footprints emitted by buildings.mjs
// and every free identity source downloaded by loredata.mjs, and writes one
// record per building to out/lore.json.
//
// Source priority (highest first):
//   0 manual overrides   out/lore_overrides_manual.json (hand-audited fixes)
//   1 Google tie-break   out/lore_overrides_google.json (optional, places.mjs)
//   2 DataSF facilities  authoritative civic inventory + public schools
//   3 OSM                amenity/shop/tourism/building/office tags
//   4 Overture Places    carries the Foursquare OS Places records
//   5 Business registry  DataSF Registered Business Locations (self-reported NAICS)
//   6 Land use           DataSF per-parcel use mix
//   7 Heuristic          height/area/district default — never leaves a building blank
//
// Every building ends with a cat; sub is filled whenever a fine-grained source
// had an opinion. Confidence: 3 = two independent sources agree, 2 = single
// authoritative source, 1 = single weak source, 0 = land use or heuristic only.

import { existsSync } from 'node:fs';
import { readFile, writeFile } from 'node:fs/promises';
import { CELL_SIZE, insideBBox, project } from './lib/geo.mjs';
import { ringArea, ringBBox, ringCentroid } from './lib/poly.mjs';
import { CellIndex, inPolygonLonLat, matchFootprint } from './lib/join.mjs';
import {
  CATS,
  CAT_INDEX,
  SUBS,
  catOf,
  facilitySub,
  landuseCat,
  naicsSub,
  osmSub,
  overtureSub,
  schoolSub,
} from './taxonomy.mjs';

const DATA = new URL('./data/', import.meta.url);
const OUT = new URL('./out/', import.meta.url);

const FLOOR_M = 3.5;
const TOWER_FLOORS = 6; // a business POI may not reclassify anything taller
const TOWER_EXEMPT = new Set([CAT_INDEX.get('hotel'), CAT_INDEX.get('hospital'), CAT_INDEX.get('parking_garage')]);

const t0 = Date.now();
const readJSON = async (name, base = DATA) => JSON.parse(await readFile(new URL(name, base), 'utf8'));
const exists = (name, base = DATA) => existsSync(new URL(name, base));

// ------------------------------------------------------------------ footprints
console.log('reading footprints...');
const fp = await readJSON('footprints.json', OUT);
const buildings = fp.buildings.map((rec, id) => {
  const ring = rec[0];
  const [x, z] = ringCentroid(ring);
  return {
    id,
    ring,
    x,
    z,
    bbox: ringBBox(ring),
    height: rec[1],
    baseY: rec[2],
    seed: rec[3],
    palette: rec[4],
    area: Math.abs(ringArea(ring)),
    floors: Math.max(1, Math.round(rec[1] / FLOOR_M)),
    candidates: [],
  };
});
console.log(`  ${buildings.length} footprints`);

const fpIndex = new CellIndex(CELL_SIZE);
for (const b of buildings) fpIndex.add(b.x, b.z, b.id);

const stats = {
  sources: {},
  unmapped: new Map(),
};

function noteUnmapped(key) {
  if (!key) return;
  stats.unmapped.set(key, (stats.unmapped.get(key) || 0) + 1);
}

function sourceStat(source) {
  let s = stats.sources[source];
  if (!s) s = stats.sources[source] = { in: 0, matched: 0, nearest: 0, dropped: 0 };
  return s;
}

// One candidate = one source's opinion about one building.
function addCandidate(source, priority, lon, lat, opinion, maxDist = 30) {
  const s = sourceStat(source);
  s.in++;
  if (!insideBBox(lon, lat)) {
    s.dropped++;
    return -1;
  }
  const [x, z] = project(lon, lat);
  const hit = matchFootprint(fpIndex, buildings, x, z, maxDist);
  if (!hit) {
    s.dropped++;
    return -1;
  }
  if (hit.exact) s.matched++;
  else s.nearest++;
  buildings[hit.idx].candidates.push({ source, priority, exact: hit.exact, ...opinion });
  return hit.idx;
}

// Authoritative civic points are often digitised at the parcel centroid or the
// driveway rather than the building, so they get a wider capture radius than
// POIs, and the inventory is authoritative enough that a facility which still
// found nothing retries against the nearest footprint no other facility claims.
const FACILITY_RADIUS = 60;
const FACILITY_RETRY_RADIUS = 120;

function addFacility(lon, lat, opinion) {
  const idx = addCandidate('datasf', 2, lon, lat, opinion, FACILITY_RADIUS);
  if (idx >= 0) return idx;
  if (!insideBBox(lon, lat)) return -1;
  const [x, z] = project(lon, lat);
  const hit = matchFootprint(fpIndex, buildings, x, z, FACILITY_RETRY_RADIUS);
  if (!hit || buildings[hit.idx].candidates.some((c) => c.source === 'datasf')) return -1;
  sourceStat('datasf').dropped--;
  sourceStat('datasf').nearest++;
  buildings[hit.idx].candidates.push({ source: 'datasf', priority: 2, exact: false, ...opinion });
  return hit.idx;
}

function resolve(sub, catHint) {
  if (sub) {
    const cat = catOf(sub);
    if (cat === null) throw new Error(`subcategory ${sub} is not in the taxonomy`);
    return { cat, sub };
  }
  return { cat: catHint ?? null, sub: null };
}

// ------------------------------------------------------- 2. DataSF facilities
console.log('joining DataSF city facilities...');
const facilities = await readJSON('datasf_facilities.json');
const fireStations = [];
for (const f of facilities) {
  const lon = parseFloat(f.longitude);
  const lat = parseFloat(f.latitude);
  if (!Number.isFinite(lon) || !Number.isFinite(lat)) continue;
  const { sub, unmapped } = facilitySub(f);
  noteUnmapped(unmapped && `facility_dept=${unmapped}`);
  const r = resolve(sub);
  if (r.cat === null) continue;
  const idx = addFacility(lon, lat, { ...r, name: f.common_name || null, addr: f.address || null });
  if (r.sub === 'fire_station') fireStations.push({ name: f.common_name, idx });
}

console.log('joining DataSF schools...');
for (const s of await readJSON('datasf_schools.json')) {
  const lon = parseFloat(s.longitude);
  const lat = parseFloat(s.latitude);
  if (!Number.isFinite(lon) || !Number.isFinite(lat)) continue;
  addFacility(lon, lat, { ...resolve(schoolSub(s)), name: s.school || null, addr: s.street_address || null });
}

// ------------------------------------------------------------------- 3. OSM
console.log('joining OSM tags...');
const osm = await readJSON('osm_pois.json');
for (const el of osm.elements) {
  const tags = el.tags || {};
  const lon = el.lon ?? el.center?.lon;
  const lat = el.lat ?? el.center?.lat;
  if (!Number.isFinite(lon) || !Number.isFinite(lat)) continue;
  const { sub, unmapped } = osmSub(tags);
  noteUnmapped(unmapped && `osm ${unmapped}`);
  if (!sub) continue;
  addCandidate('osm', 3, lon, lat, {
    ...resolve(sub),
    name: tags.name || null,
    addr:
      tags['addr:housenumber'] && tags['addr:street']
        ? `${tags['addr:housenumber']} ${tags['addr:street']}`
        : null,
    wikidata: tags.wikidata || null,
    tourism: tags.tourism || null,
    historic: tags.historic || null,
    religion: tags.religion || null,
  });
}

// -------------------------------------------------------- 4. Overture Places
console.log('joining Overture Places...');
const overture = await readJSON('overture_places.geojson');
for (const f of overture.features) {
  const p = f.properties || {};
  const coords = f.geometry?.coordinates;
  if (!coords) continue;
  const cat = p.categories?.primary;
  const { sub, unmapped } = overtureSub(cat);
  noteUnmapped(unmapped && `overture ${unmapped}`);
  if (!sub) continue;
  const confidence = typeof p.confidence === 'number' ? p.confidence : 0;
  if (confidence < 0.3) continue;
  addCandidate('overture', 4, coords[0], coords[1], {
    ...resolve(sub),
    name: p.names?.primary || null,
    addr: p.addresses?.[0]?.freeform || null,
    wikidata: p.brand?.wikidata || null,
    weight: confidence,
  });
}

// ------------------------------------------------- 5. Registered businesses
console.log('joining registered businesses...');
for (const b of await readJSON('datasf_business.json')) {
  const coords = b.location?.coordinates;
  if (!coords) continue;
  const { sub, unmapped } = naicsSub(b.self_reported_naics_code);
  noteUnmapped(unmapped && `naics ${unmapped}`);
  if (!sub) continue;
  addCandidate('business', 5, coords[0], coords[1], {
    ...resolve(sub),
    name: b.dba_name || null,
    addr: b.full_business_address || null,
    hotelTax: b.transient_occupancy_tax === true,
  });
}

// -------------------------------------------------------------- 6. Land use
console.log('joining land-use parcels...');
{
  const parcels = await readJSON('datasf_landuse.json');
  const parcelIndex = new CellIndex(CELL_SIZE);
  const shapes = [];
  for (const p of parcels) {
    const geom = p.the_geom;
    if (!geom) continue;
    const cat = landuseCat(p);
    if (cat === null) continue;
    const polys = geom.type === 'Polygon' ? [geom.coordinates] : geom.coordinates || [];
    let minLon = Infinity;
    let maxLon = -Infinity;
    let minLat = Infinity;
    let maxLat = -Infinity;
    const rings = [];
    for (const poly of polys) {
      const outer = poly?.[0];
      if (!outer || outer.length < 4) continue;
      rings.push(outer);
      for (const c of outer) {
        if (c[0] < minLon) minLon = c[0];
        if (c[0] > maxLon) maxLon = c[0];
        if (c[1] < minLat) minLat = c[1];
        if (c[1] > maxLat) maxLat = c[1];
      }
    }
    if (!rings.length) continue;
    const [x0, z1] = project(minLon, minLat);
    const [x1, z0] = project(maxLon, maxLat);
    const shape = { rings, resunits: parseFloat(p.resunits) || 0, cat };
    shapes.push(shape);
    parcelIndex.addBBox([x0, z0, x1, z1], shapes.length - 1);
  }
  const s = sourceStat('landuse');
  s.in = shapes.length;
  for (const b of buildings) {
    const [lon, lat] = unprojectLocal(b.x, b.z);
    let hit = null;
    for (const idx of parcelIndex.near(b.x, b.z)) {
      const shape = shapes[idx];
      for (const ring of shape.rings) {
        if (inPolygonLonLat(lon, lat, ring)) {
          hit = shape;
          break;
        }
      }
      if (hit) break;
    }
    if (!hit) continue;
    s.matched++;
    b.candidates.push({ source: 'landuse', priority: 6, cat: hit.cat, sub: null, resunits: hit.resunits });
  }
}

function unprojectLocal(x, z) {
  const M_PER_DEG_LON = 111320 * Math.cos((37.77 * Math.PI) / 180);
  return [x / M_PER_DEG_LON - 122.4375, -z / 110540 + 37.77];
}

// ----------------------------------------------------------- 0/1 overrides
for (const [file, source, priority] of [
  ['lore_overrides_manual.json', 'manual', 0],
  ['lore_overrides_google.json', 'google', 1],
]) {
  if (!exists(file, OUT)) continue;
  const overrides = await readJSON(file, OUT);
  let n = 0;
  for (const [id, o] of Object.entries(overrides)) {
    const b = buildings[Number(id)];
    if (!b) continue;
    const r = resolve(o.sub || null, o.cat ?? null);
    if (r.cat === null) continue;
    b.candidates.push({ source, priority, ...r, name: o.name || null, addr: o.addr || null });
    n++;
  }
  console.log(`  ${file}: ${n} overrides`);
  sourceStat(source).in = n;
  sourceStat(source).matched = n;
}

// --------------------------------------------------------------- resolution
console.log('resolving identities...');

const RESIDENTIAL = new Set([CAT_INDEX.get('house'), CAT_INDEX.get('apartments')]);
const CIVIC = new Set(
  ['worship', 'school', 'university', 'hospital', 'clinic', 'fire_station', 'police', 'library', 'museum', 'government']
    .map((c) => CAT_INDEX.get(c))
);

// Garages, sheds and other accessory structures share their parcel's
// residential land use but are not dwellings.
const ACCESSORY_AREA = 45;
function accessory(b) {
  return b.area < ACCESSORY_AREA && b.floors <= 2;
}

function heuristic(b) {
  const floors = b.floors;
  if (accessory(b)) return CAT_INDEX.get('misc');
  const glassy = b.palette === 0;
  const industrial = b.palette === 5;
  if (industrial && b.area > 600) return CAT_INDEX.get('warehouse');
  if (glassy && floors >= 8) return CAT_INDEX.get('office');
  if (floors >= 5) return CAT_INDEX.get('apartments');
  if (b.area > 1200 && floors <= 3) return CAT_INDEX.get('warehouse');
  if (floors >= 4 && b.area > 400) return CAT_INDEX.get('apartments');
  return CAT_INDEX.get('house');
}

const lore = {};
const catHist = new Array(CATS.length).fill(0);
const subHist = new Map();
const needsCheck = {};
let disagreeOsmFsq = 0;
let comparableOsmFsq = 0;
let towerBlocked = 0;

// A business licence at a dwelling is a home office, not an office building:
// the registry alone never overrides a residential parcel.
const DESK_JOBS = new Set([CAT_INDEX.get('office')]);

for (const b of buildings) {
  const parcelCat = b.candidates.find((c) => c.source === 'landuse')?.cat;
  const residentialParcel = parcelCat !== undefined && RESIDENTIAL.has(parcelCat);
  const cands = b.candidates.filter(
    (c) =>
      !(
        c.source === 'business' &&
        residentialParcel &&
        DESK_JOBS.has(c.cat) &&
        !b.candidates.some((o) => o.source !== 'business' && o.source !== 'landuse' && DESK_JOBS.has(o.cat))
      )
  );
  // A commercial storefront POI never renames a tower.
  const usable = cands.filter((c) => {
    if (c.priority <= 2 || c.source === 'landuse') return true;
    if (b.floors <= TOWER_FLOORS) return true;
    if (TOWER_EXEMPT.has(c.cat)) return true;
    if (c.source === 'osm' && (c.cat === CAT_INDEX.get('office') || RESIDENTIAL.has(c.cat))) return true;
    towerBlocked++;
    return false;
  });

  // Cross-check: do OSM and Overture (which carries the Foursquare places)
  // agree about a building? A building can hold several businesses, so they
  // agree when any pair of their opinions shares a category.
  const osmCats = new Set(usable.filter((c) => c.source === 'osm' && c.exact).map((c) => c.cat));
  const fsqCats = new Set(usable.filter((c) => c.source === 'overture' && c.exact).map((c) => c.cat));
  if (osmCats.size && fsqCats.size && [...osmCats].some((c) => c >= 5)) {
    comparableOsmFsq++;
    if (![...osmCats].some((c) => fsqCats.has(c))) disagreeOsmFsq++;
  }

  usable.sort((a, c) => a.priority - c.priority || (c.weight || 0) - (a.weight || 0));
  const winner = usable[0];

  let cat;
  let sub = null;
  let source;
  if (winner) {
    cat = winner.cat;
    sub = winner.sub;
    source = winner.source;
    // A coarse winner (land use "retail") keeps a finer sub from a lower-priority
    // source that agrees about the parent category.
    if (!sub) {
      const finer = usable.find((c) => c.sub && c.cat === cat);
      if (finer) sub = finer.sub;
    }
  } else {
    cat = heuristic(b);
    source = 'heuristic';
  }

  if (RESIDENTIAL.has(cat) && (source === 'landuse' || source === 'heuristic') && accessory(b)) {
    cat = CAT_INDEX.get('misc');
    sub = null;
  }

  // Confidence: independent agreement at the category level.
  const agreeing = new Set(
    usable.filter((c) => c.cat === cat && c.source !== 'landuse').map((c) => c.source)
  );
  let confidence;
  if (agreeing.size >= 2) confidence = 3;
  else if (source === 'manual') confidence = 3;
  else if (source === 'datasf' || source === 'osm' || source === 'google') confidence = 2;
  else if (source === 'overture' || source === 'business') confidence = 1;
  else confidence = 0;

  // Names: authoritative sources first, tenants preserved for the card.
  const named = usable.filter((c) => c.name && c.name.trim());
  named.sort((a, c) => a.priority - c.priority);
  const primary = named.find((c) => c.cat === cat) || named[0] || null;
  const tenants = [...new Set(named.map((c) => c.name.trim()))].slice(0, 6);

  const rec = { cat, source, confidence };
  if (sub) rec.sub = sub;
  if (primary?.name) rec.name = primary.name.trim().slice(0, 80);
  const addr = usable.find((c) => c.addr)?.addr;
  if (addr) rec.addr = String(addr).trim().slice(0, 60);
  const wikidata = usable.find((c) => c.wikidata)?.wikidata;
  if (wikidata) rec.wikidata = wikidata;
  if (tenants.length > 1) rec.tenants = tenants;
  const tourism = usable.find((c) => c.tourism)?.tourism;
  if (tourism) rec.tourism = tourism;
  const historic = usable.find((c) => c.historic)?.historic;
  if (historic) rec.historic = historic;
  const religion = usable.find((c) => c.religion)?.religion;
  if (religion) rec.religion = religion;
  rec.floors = b.floors;

  lore[b.id] = rec;
  catHist[cat]++;
  if (sub) subHist.set(sub, (subHist.get(sub) || 0) + 1);

  // Single-source civic or commercial claims with no corroboration are exactly
  // what the optional Google tie-break exists to settle.
  if (confidence <= 1 && (CIVIC.has(cat) || cat >= 4) && source !== 'heuristic' && source !== 'landuse') {
    needsCheck[b.id] = {
      cat,
      sub: sub || null,
      name: rec.name || null,
      source,
      x: Math.round(b.x),
      z: Math.round(b.z),
    };
  }
}

// ------------------------------------------------------------------- output
await writeFile(new URL('lore.json', OUT), JSON.stringify(lore));
await writeFile(new URL('needs_check.json', OUT), JSON.stringify(needsCheck));

const total = buildings.length;
const pct = (n) => `${((100 * n) / total).toFixed(1)}%`;
console.log('\ncategory histogram');
CATS.forEach((c, i) => {
  if (catHist[i]) console.log(`  ${String(i).padStart(2)} ${c.padEnd(16)} ${String(catHist[i]).padStart(7)}  ${pct(catHist[i])}`);
});

const subs = [...subHist.entries()].sort((a, b) => b[1] - a[1]);
console.log(`\nsubcategory histogram (${subs.length} of ${Object.keys(SUBS).length} subs present)`);
for (const [sub, n] of subs.slice(0, 30)) console.log(`  ${sub.padEnd(20)} ${String(n).padStart(6)}`);

console.log('\nper-source join');
for (const [name, s] of Object.entries(stats.sources)) {
  console.log(
    `  ${name.padEnd(10)} in ${String(s.in).padStart(7)}  in-footprint ${String(s.matched).padStart(6)}  nearest ${String(
      s.nearest
    ).padStart(6)}  dropped ${String(s.dropped).padStart(6)}`
  );
}

const unmapped = [...stats.unmapped.entries()].sort((a, b) => b[1] - a[1]);
console.log(`\nunmapped source values: ${unmapped.length} distinct`);
for (const [k, n] of unmapped.slice(0, 20)) console.log(`  ${k} × ${n}`);

const conf = [0, 0, 0, 0];
for (const r of Object.values(lore)) conf[r.confidence]++;
console.log(`\nconfidence 3/2/1/0: ${conf[3]} / ${conf[2]} / ${conf[1]} / ${conf[0]}`);
console.log(
  `OSM vs Overture disagreement on cats 5–25: ${
    comparableOsmFsq ? ((100 * disagreeOsmFsq) / comparableOsmFsq).toFixed(1) : '0'
  }% (${disagreeOsmFsq}/${comparableOsmFsq}); tower rule blocked ${towerBlocked} POI opinions`
);

// ---------------------------------------------------------------- sanity gates
const gates = [];
const share = (name) => catHist[CAT_INDEX.get(name)];
const residential = share('house') + share('apartments');
gates.push([
  'houses + apartments 60–80%',
  residential / total >= 0.6 && residential / total <= 0.8,
  pct(residential),
]);
gates.push(['worship 300–800', share('worship') >= 300 && share('worship') <= 800, share('worship')]);
gates.push([
  'fire stations 40–60',
  share('fire_station') >= 40 && share('fire_station') <= 60,
  share('fire_station'),
]);
gates.push(['zero unclassified', Object.keys(lore).length === total, `${Object.keys(lore).length}/${total}`]);

// Every DataSF fire station must have found a footprint.
let fireMatched = 0;
for (const f of fireStations) {
  if (f.idx >= 0 && lore[buildings[f.idx].id].cat === CAT_INDEX.get('fire_station')) fireMatched++;
  else console.log(`  ! unjoined fire station: ${f.name}`);
}
gates.push([
  'every DataSF fire station joined',
  fireMatched === fireStations.length,
  `${fireMatched}/${fireStations.length}`,
]);

console.log('\nsanity gates');
let failed = 0;
for (const [name, ok, value] of gates) {
  if (!ok) failed++;
  console.log(`  ${ok ? 'PASS' : 'FAIL'} ${name} — ${value}`);
}
console.log(`\nlore.json written in ${((Date.now() - t0) / 1000).toFixed(1)}s`);
if (failed) {
  console.error(`${failed} sanity gate(s) failed`);
  process.exitCode = 1;
}
