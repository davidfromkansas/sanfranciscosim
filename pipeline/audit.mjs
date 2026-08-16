// Verification audit over the BAKED tiles (not the sources): counts, height
// distribution, georeference/mirror checks, terrain draping, landmark
// exclusion, buildings standing in open water, and bespoke-structure alignment
// against real OSM centerlines. Prints a findings table and writes
// out/audit.json. Read-only: it never modifies the bake.

import { readFile, readdir, writeFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { EXTENT, hash01, project, unproject } from './lib/geo.mjs';
import { loadHeightmap } from './lib/heightmap.mjs';
import { LANDMARKS, NAMED_PARKS, exclusionZones } from './lib/landmarks.mjs';
import { STREET_CLASSES } from './lib/classes.mjs';
import { readBuildingsBlob, readLandcoverBlob, readStreetsBlob } from './lib/blobread.mjs';
import { loadTreeBlockers } from './lib/treeblockers.mjs';
import { ringArea, ringCentroid, polylineLength } from './lib/poly.mjs';

const OUT = new URL('./out/', import.meta.url);
const DATA = new URL('./data/', import.meta.url);
const APP_SRC = new URL('../app/src/', import.meta.url);

const rows = [];
function check(id, label, ok, evidence) {
  rows.push({ id, label, status: ok ? 'PASS' : 'FAIL', evidence });
}
function note(id, label, evidence) {
  rows.push({ id, label, status: 'INFO', evidence });
}

const freewayClass = STREET_CLASSES.findIndex((c) => c.id === 'freeway');
const rampClass = STREET_CLASSES.findIndex((c) => c.id === 'ramp');

const { desc: terrainDesc, sampleElevation } = await loadHeightmap();
const buildingsIndex = JSON.parse(await readFile(new URL('buildings.json', OUT), 'utf8'));
const streetsIndex = JSON.parse(await readFile(new URL('streets.json', OUT), 'utf8'));
const landcoverIndex = JSON.parse(await readFile(new URL('landcover.json', OUT), 'utf8'));

// --------------------------------------------------------------- load blobs --
const buildings = [];
for (const cell of buildingsIndex.cells) {
  const blob = await readBuildingsBlob(new URL(`buildings/${cell.key}.bin`, OUT));
  for (const b of blob.buildings) {
    const [cx, cz] = ringCentroid(b.ring);
    buildings.push({ ...b, cx, cz, area: Math.abs(ringArea(b.ring)), cell: cell.key });
  }
}

const streetLines = [];
let streetLengthM = 0;
let streetPoints = 0;
for (const cell of streetsIndex.cells) {
  const blob = await readStreetsBlob(new URL(`streets/${cell.key}.bin`, OUT));
  for (const l of blob.lines) {
    const flat = [];
    for (let i = 0; i < l.pts.length; i += 3) flat.push(l.pts[i], l.pts[i + 2]);
    streetLengthM += polylineLength(flat);
    streetPoints += l.pts.length / 3;
    streetLines.push({ ...l, cell: cell.key });
  }
}

let treeTotal = 0;
let landcoverTris = 0;
const treeSamples = [];
for (const cell of landcoverIndex.cells) {
  const blob = await readLandcoverBlob(new URL(`landcover/${cell.key}.bin`, OUT));
  treeTotal += blob.treeTotal;
  landcoverTris += blob.triangles;
  for (let i = 0; i < blob.treeTotal; i += 400) {
    treeSamples.push([blob.trees[i * 3], blob.trees[i * 3 + 1], blob.trees[i * 3 + 2]]);
  }
}

// ------------------------------------------------------------- 1.1 counts ----
check('1.1a', 'baked buildings >= 150,000', buildings.length >= 150000, `${buildings.length} decoded from ${buildingsIndex.cells.length} cells`);
const streetKm = streetLengthM / 1000;
check('1.1b', 'street ribbon length 1,500-2,500 km', streetKm >= 1500 && streetKm <= 2500, `${streetKm.toFixed(0)} km over ${streetLines.length} baked polylines / ${streetPoints} points`);
check('1.1c', 'tree instances > 30,000', treeTotal > 30000, `${treeTotal} trees, ${landcoverTris} landcover triangles`);

// ------------------------------------------------------------- 1.2 heights ---
const heights = buildings.map((b) => b.topY - sampleElevation(b.cx, b.cz)).sort((a, b) => a - b);
const pct = (p) => heights[Math.min(heights.length - 1, Math.floor((p / 100) * heights.length))];
const tallestProcedural = heights[heights.length - 1];
const bespokeTallest = Math.max(...LANDMARKS.filter((l) => l.height).map((l) => l.height));
check('1.2a', 'tallest structure 320-330 m (Salesforce Tower)', bespokeTallest >= 320 && bespokeTallest <= 330, `bespoke ${bespokeTallest} m; tallest procedural ${tallestProcedural.toFixed(1)} m`);
// The source itself does not support a 25 m p95: DataSF LiDAR roof statistics
// over all 177,023 footprints give p95 12.4 m at the median roof and 15.7 m at
// the ridge, because 95% of San Francisco is one- to three-storey housing.
check('1.2b', '95th percentile height 25-120 m', pct(95) >= 25 && pct(95) <= 120, `p95 ${pct(95).toFixed(1)} m (p99 ${pct(99).toFixed(1)} m) — DataSF source p95 is 12.4 m (median roof) / 15.7 m (ridge)`);
check('1.2c', 'median height 6-15 m', pct(50) >= 6 && pct(50) <= 15, `median ${pct(50).toFixed(1)} m`);

// ------------------------------------------- 1.3 georeference spot checks ----
const salesforce = LANDMARKS.find((l) => l.id === 'salesforceTower');
const [sfx, sfz] = project(-122.3966, 37.7897);
const [slx, slz] = project(salesforce.lon, salesforce.lat);
const salesforceErr = Math.hypot(sfx - slx, sfz - slz);
check('1.3a', 'Salesforce Tower ~326 m within 50 m of -122.3966,37.7897', salesforceErr <= 50 && salesforce.height >= 320 && salesforce.height <= 330, `bespoke model ${salesforce.height} m at ${salesforceErr.toFixed(0)} m from the reference coordinate`);

const [fbx, fbz] = project(-122.3937, 37.7955);
const ferryElev = sampleElevation(fbx, fbz);
check('1.3b', "Ferry Building terrain < 10 m", ferryElev < 10, `${ferryElev.toFixed(1)} m`);

const [ctx_, ctz] = project(-122.4058, 37.8024);
const coitElev = sampleElevation(ctx_, ctz);
// Terrarium reads 90.5-91.3 m at the Coit Tower base across zooms 13-15; the
// surveyed summit is 84 m, so the DEM is 6.5 m high here, not mis-georeferenced.
check('1.3c', 'Telegraph Hill terrain 60-85 m', coitElev >= 60 && coitElev <= 85, `${coitElev.toFixed(1)} m (Terrarium DEM; surveyed summit 84 m)`);

const [tpx, tpz] = project(-122.4477, 37.7544);
const twinElev = sampleElevation(tpx, tpz);
check('1.3d', 'Twin Peaks terrain 250-285 m', twinElev >= 250 && twinElev <= 285, `${twinElev.toFixed(1)} m`);

const [obx, obz] = project(-122.509, 37.759);
const oceanElev = sampleElevation(obx, obz);
// "West of Ocean Beach" only means anything at the same latitude: the coastline
// swings west again at Fort Funston and Lands End, so buildings there are south
// or north of this line, not in the surf.
const westOfBeach = buildings.filter((b) => b.cx < obx - 60 && Math.abs(b.cz - obz) < 400);
check(
  '1.3e',
  'Ocean Beach terrain 0-8 m and no buildings west of it',
  oceanElev >= 0 && oceanElev <= 8 && westOfBeach.length === 0,
  `${oceanElev.toFixed(1)} m; ${westOfBeach.length} buildings west of x=${obx.toFixed(0)} m within 400 m of the beach latitude`
);

// ---------------------------------------------------- 1.4 mirror/flip test ---
const [coitX, coitZ] = project(-122.4058, 37.8024);
const [marketX, marketZ] = project(-122.4079, 37.7864);
const [ggbX, ggbZ] = project(-122.4783, 37.8199);
const [dtX, dtZ] = project(-122.4014, 37.7899);
check('1.4a', 'Coit Tower north of Market Street (-z is north)', coitZ < marketZ, `Coit z=${coitZ.toFixed(0)}, Market z=${marketZ.toFixed(0)}`);
check('1.4b', 'Golden Gate Bridge northwest of downtown', ggbX < dtX && ggbZ < dtZ, `GGB (${ggbX.toFixed(0)}, ${ggbZ.toFixed(0)}) vs downtown (${dtX.toFixed(0)}, ${dtZ.toFixed(0)})`);
// From the Ferry Building looking west along Market, Twin Peaks must be ahead:
// dead west means decreasing x with only a small z drift.
// Real bearing Ferry Building -> Twin Peaks is 233° true (west-southwest to
// southwest), so anything in the western half turning south is correct.
const bearing = (Math.atan2(tpx - fbx, -(tpz - fbz)) * 180) / Math.PI;
check('1.4c', 'Twin Peaks bears west-southwest from the Ferry Building', bearing < -70 && bearing > -150, `bearing ${bearing.toFixed(0)}° from north (west = -90°, real bearing -127°)`);
const roundTrip = unproject(...project(-122.4058, 37.8024));
check('1.4d', 'projection round-trips', Math.abs(roundTrip[0] + 122.4058) < 1e-9 && Math.abs(roundTrip[1] - 37.8024) < 1e-9, `unproject(project(p)) = ${roundTrip[0].toFixed(6)}, ${roundTrip[1].toFixed(6)}`);

// ------------------------------------------------- 1.5 terrain draping -------
const sampleCount = 200;
// The bake drapes wall bottoms to the lowest terrain under the footprint (that
// is what stops a hillside house from floating on its downhill corner), so the
// tolerance is measured against that low point; the centroid delta is reported
// alongside because on Castro-grade slopes it is the real terrain drop across
// the footprint, not an error.
let worstBuilding = 0;
const buildingDeltas = [];
const centroidDeltas = [];
for (let i = 0; i < sampleCount; i++) {
  const b = buildings[Math.floor(hash01(i * 7919 + 13) * buildings.length)];
  let minGround = Infinity;
  for (let k = 0; k < b.ring.length; k += 2) minGround = Math.min(minGround, sampleElevation(b.ring[k], b.ring[k + 1]));
  const delta = Math.abs(b.baseY - minGround);
  buildingDeltas.push(delta);
  centroidDeltas.push(Math.abs(b.baseY - sampleElevation(b.cx, b.cz)));
  worstBuilding = Math.max(worstBuilding, delta);
}
buildingDeltas.sort((a, b) => a - b);
centroidDeltas.sort((a, b) => a - b);
check(
  '1.5a',
  'sampled building bases within 2 m of the lowest terrain under the footprint',
  worstBuilding <= 2,
  `${sampleCount} samples: median ${buildingDeltas[100].toFixed(2)} m, p95 ${buildingDeltas[189].toFixed(2)} m, worst ${worstBuilding.toFixed(2)} m (at centroid: median ${centroidDeltas[100].toFixed(2)} m, worst ${centroidDeltas[199].toFixed(2)} m of real slope drop)`
);

// Surface streets only: freeway and ramp ribbons are deliberately up on decks.
const groundLines = streetLines.filter((l) => l.klass !== freewayClass && l.klass !== rampClass);
let worstStreet = 0;
const streetDeltas = [];
for (let i = 0; i < sampleCount; i++) {
  const l = groundLines[Math.floor(hash01(i * 104729 + 7) * groundLines.length)];
  const k = Math.floor(hash01(i * 31 + 3) * (l.pts.length / 3));
  const x = l.pts[k * 3];
  const y = l.pts[k * 3 + 1];
  const z = l.pts[k * 3 + 2];
  const delta = Math.abs(y - 0.15 - sampleElevation(x, z));
  streetDeltas.push(delta);
  worstStreet = Math.max(worstStreet, delta);
}
streetDeltas.sort((a, b) => a - b);
check('1.5b', 'sampled surface-street points within 0.5 m of terrain', worstStreet <= 0.5, `${sampleCount} samples: median ${streetDeltas[100].toFixed(3)} m, worst ${worstStreet.toFixed(3)} m`);

// ------------------------------------------------ 1.6 landmark exclusion -----
const intrusions = [];
const zones = exclusionZones();
for (const zone of zones) {
  const [lx, lz] = project(zone.lon, zone.lat);
  let worst = null;
  for (const b of buildings) {
    // Footprint intrusion, not just centroid: nearest ring vertex to the anchor.
    let nearest = Infinity;
    for (let i = 0; i < b.ring.length; i += 2) {
      const d = Math.hypot(b.ring[i] - lx, b.ring[i + 1] - lz);
      if (d < nearest) nearest = d;
    }
    if (nearest < zone.r && (!worst || nearest < worst.d)) worst = { d: nearest, cell: b.cell, height: (b.topY - b.baseY).toFixed(0) };
  }
  if (worst) intrusions.push(`${zone.name}: footprint ${worst.d.toFixed(0)} m from zone centre (r=${zone.r} m, ${worst.height} m tall, cell ${worst.cell})`);
}
check('1.6', 'no procedural footprint inside a bespoke landmark exclusion zone', intrusions.length === 0, intrusions.length ? intrusions.join('; ') : `${zones.length} zones over ${LANDMARKS.length} landmarks clear`);

// --------------------------------------- 1.7 buildings in open water sweep ---
// Same definition the runtime terrain uses: elevation below sea level AND
// connected to the map edge by a flood fill, so Mission Bay's dry flats and
// inland lakes are not treated as ocean.
const MASK = 1024;
const SEA_LEVEL = 1.2;
const stepX = (EXTENT.maxX - EXTENT.minX) / (MASK - 1);
const stepZ = (EXTENT.maxZ - EXTENT.minZ) / (MASK - 1);
const low = new Uint8Array(MASK * MASK);
for (let j = 0; j < MASK; j++) {
  for (let i = 0; i < MASK; i++) {
    low[j * MASK + i] = sampleElevation(EXTENT.minX + i * stepX, EXTENT.minZ + j * stepZ) < SEA_LEVEL ? 1 : 0;
  }
}
const water = new Uint8Array(MASK * MASK);
const queue = [];
const seed = (i, j) => {
  const k = j * MASK + i;
  if (low[k] && !water[k]) {
    water[k] = 1;
    queue.push(k);
  }
};
for (let i = 0; i < MASK; i++) {
  seed(i, 0);
  seed(i, MASK - 1);
}
for (let j = 0; j < MASK; j++) {
  seed(0, j);
  seed(MASK - 1, j);
}
while (queue.length) {
  const k = queue.pop();
  const i = k % MASK;
  const j = (k - i) / MASK;
  if (i > 0) seed(i - 1, j);
  if (i < MASK - 1) seed(i + 1, j);
  if (j > 0) seed(i, j - 1);
  if (j < MASK - 1) seed(i, j + 1);
}

// Chamfer distance transform: meters of open water between a point and the
// nearest land pixel.
const INF = 1e9;
const dist = new Float64Array(MASK * MASK);
for (let k = 0; k < dist.length; k++) dist[k] = water[k] ? INF : 0;
const dxm = stepX;
const dzm = stepZ;
const diag = Math.hypot(dxm, dzm);
for (let j = 0; j < MASK; j++) {
  for (let i = 0; i < MASK; i++) {
    const k = j * MASK + i;
    if (dist[k] === 0) continue;
    let best = dist[k];
    if (i > 0) best = Math.min(best, dist[k - 1] + dxm);
    if (j > 0) best = Math.min(best, dist[k - MASK] + dzm);
    if (i > 0 && j > 0) best = Math.min(best, dist[k - MASK - 1] + diag);
    if (i < MASK - 1 && j > 0) best = Math.min(best, dist[k - MASK + 1] + diag);
    dist[k] = best;
  }
}
for (let j = MASK - 1; j >= 0; j--) {
  for (let i = MASK - 1; i >= 0; i--) {
    const k = j * MASK + i;
    if (dist[k] === 0) continue;
    let best = dist[k];
    if (i < MASK - 1) best = Math.min(best, dist[k + 1] + dxm);
    if (j < MASK - 1) best = Math.min(best, dist[k + MASK] + dzm);
    if (i < MASK - 1 && j < MASK - 1) best = Math.min(best, dist[k + MASK + 1] + diag);
    if (i > 0 && j < MASK - 1) best = Math.min(best, dist[k + MASK - 1] + diag);
    dist[k] = best;
  }
}
function waterDepthFromShore(x, z) {
  // Clamped, not rejected: a footprint a few metres outside the sampled extent
  // is on the map edge, not a kilometre out to sea.
  const i = Math.min(MASK - 1, Math.max(0, Math.round((x - EXTENT.minX) / stepX)));
  const j = Math.min(MASK - 1, Math.max(0, Math.round((z - EXTENT.minZ) / stepZ)));
  const k = j * MASK + i;
  return water[k] ? dist[k] : 0;
}

// Pier allowlist: OSM man_made=pier geometry, per Appendix B.1.
const piers = [];
if (existsSync(new URL('osm_features.json', DATA))) {
  const features = JSON.parse(await readFile(new URL('osm_features.json', DATA), 'utf8'));
  for (const el of features.elements || []) {
    if (el.tags?.man_made !== 'pier' || !Array.isArray(el.geometry)) continue;
    for (const p of el.geometry) {
      const [x, z] = project(p.lon, p.lat);
      piers.push([x, z]);
    }
  }
}
const PIER_RADIUS = 250;
const PIER_CELL = 250;
const pierGrid = new Map();
for (const [x, z] of piers) {
  const key = `${Math.floor(x / PIER_CELL)}:${Math.floor(z / PIER_CELL)}`;
  let list = pierGrid.get(key);
  if (!list) pierGrid.set(key, (list = []));
  list.push([x, z]);
}
function nearPier(x, z) {
  const ci = Math.floor(x / PIER_CELL);
  const cj = Math.floor(z / PIER_CELL);
  for (let dj = -1; dj <= 1; dj++) {
    for (let di = -1; di <= 1; di++) {
      const list = pierGrid.get(`${ci + di}:${cj + dj}`);
      if (!list) continue;
      for (const [px, pz] of list) if (Math.hypot(px - x, pz - z) <= PIER_RADIUS) return true;
    }
  }
  return false;
}

const floating = [];
for (const b of buildings) {
  const depth = waterDepthFromShore(b.cx, b.cz);
  if (depth <= 30) continue;
  if (nearPier(b.cx, b.cz)) continue;
  const [lon, lat] = unproject(b.cx, b.cz);
  floating.push({ lon: +lon.toFixed(5), lat: +lat.toFixed(5), x: Math.round(b.cx), z: Math.round(b.cz), depth: Math.round(depth), area: Math.round(b.area), cell: b.cell });
}
floating.sort((a, b) => b.depth - a.depth);
check('1.7', 'zero buildings floating in open water (pier zones allowed)', floating.length === 0, floating.length ? `${floating.length} buildings >30 m offshore, worst ${floating[0].depth} m at ${floating[0].lon},${floating[0].lat} (cell ${floating[0].cell})` : `${piers.length} pier vertices allowlisted, 0 offenders`);

const floatingTrees = treeSamples.filter(([x, , z]) => waterDepthFromShore(x, z) > 30).length;
check('1.7b', 'zero sampled trees in open water', floatingTrees === 0, `${floatingTrees} of ${treeSamples.length} sampled trees >30 m offshore`);

// ------------------------------------------- 1.10 tree placement cleanup ----
// The same veto oracle the bake used, re-derived here: a ground tree may not
// stand inside a footprint or on a roadway, and a variant-3 roof tree must sit
// on a building.
const { inBuilding, inStreet } = await loadTreeBlockers({ sampleElevation, out: OUT });

const toyLandDir = new URL('toyland/', OUT);
const toyLandFiles = existsSync(toyLandDir)
  ? (await readdir(toyLandDir)).filter((f) => f.endsWith('.bin')).sort()
  : [];
let groundSamples = 0;
let roofSamples = 0;
let groundInBuilding = 0;
let groundInStreet = 0;
let roofOffBuilding = 0;
for (const file of toyLandFiles) {
  const blob = await readLandcoverBlob(new URL(`toyland/${file}`, OUT));
  for (let i = 0; i < blob.treeTotal; i += 200) {
    const x = blob.trees[i * 3];
    const z = blob.trees[i * 3 + 2];
    if (blob.treeVariant[i] === 3) {
      roofSamples++;
      if (!inBuilding(x, z)) roofOffBuilding++;
    } else {
      groundSamples++;
      if (inBuilding(x, z)) groundInBuilding++;
      if (inStreet(x, z)) groundInStreet++;
    }
  }
}
check('1.10a', 'zero sampled ground trees inside a building footprint', groundInBuilding === 0, `${groundInBuilding} of ${groundSamples} sampled toyland ground trees in the occupancy grid`);
check('1.10b', 'zero sampled ground trees inside a street corridor', groundInStreet === 0, `${groundInStreet} of ${groundSamples} sampled toyland ground trees on a roadway`);
check('1.10c', 'every sampled roof tree stands on a building', roofOffBuilding === 0, `${roofOffBuilding} of ${roofSamples} sampled variant-3 trees off a footprint`);

const waterStreets = streetLines.filter((l) => {
  let n = 0;
  let wet = 0;
  for (let i = 0; i < l.pts.length; i += 3) {
    n++;
    if (waterDepthFromShore(l.pts[i], l.pts[i + 2]) > 30) wet++;
  }
  return n > 0 && wet === n;
});
const bridgeClasses = new Set([0, 5]); // freeway, ramp
const waterStreetsNonBridge = waterStreets.filter((l) => !bridgeClasses.has(l.klass));
note('1.7c', 'street polylines entirely over open water', `${waterStreets.length} total, ${waterStreetsNonBridge.length} of them non-freeway classes`);

// ------------------------------------ 1.8 bespoke structure alignment -------
// Real centerlines from OSM (cached), then compare with the coordinates the
// bespoke builders actually use, parsed out of app/src/landmarks.js.
const BRIDGE_QUERY = `[out:json][timeout:60];
(
  way["name"="Golden Gate Bridge"]["highway"](37.70,-122.55,37.90,-122.30);
  way["highway"]["bridge"]["ref"~"I 80"](37.77,-122.40,37.84,-122.30);
);
out geom;`;

const bridgePath = new URL('bridges_osm.json', DATA);
if (!existsSync(bridgePath)) {
  const res = await fetch('https://overpass-api.de/api/interpreter', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      'User-Agent': 'sf-3d-pipeline/1.0 (audit)',
    },
    body: new URLSearchParams({ data: BRIDGE_QUERY }),
  });
  const text = await res.text();
  JSON.parse(text);
  await writeFile(bridgePath, text);
}
const bridgeOsm = JSON.parse(await readFile(bridgePath, 'utf8'));

// One ordered polyline per matching OSM way, so distances are measured to the
// centreline itself and not just to its (sometimes 500 m apart) nodes.
function centerlineFor(test) {
  const ways = [];
  for (const el of bridgeOsm.elements || []) {
    if (!Array.isArray(el.geometry) || !test(el.tags || {})) continue;
    const pts = el.geometry.filter(Boolean).map((p) => project(p.lon, p.lat));
    if (pts.length >= 2) ways.push(pts);
  }
  return ways;
}

function distanceToSegment(ax, az, bx, bz, x, z) {
  const dx = bx - ax;
  const dz = bz - az;
  const l2 = dx * dx + dz * dz || 1;
  const t = Math.min(1, Math.max(0, ((x - ax) * dx + (z - az) * dz) / l2));
  return Math.hypot(x - (ax + dx * t), z - (az + dz * t));
}

function distanceToWays(ways, x, z) {
  let best = Infinity;
  for (const pts of ways) {
    for (let i = 1; i < pts.length; i++) {
      best = Math.min(best, distanceToSegment(pts[i - 1][0], pts[i - 1][1], pts[i][0], pts[i][1], x, z));
    }
  }
  return best;
}

// Deck nodes exactly as the app consumes them: out/bridges.json, published into
// the manifest and read by app/src/landmarks.js.
const bakedBridges = JSON.parse(await readFile(new URL('bridges.json', OUT), 'utf8'));
function deckNodes(id, includeEast = false) {
  const spec = bakedBridges[id];
  if (!spec) return [];
  const lists = includeEast && spec.east ? [spec.nodes, spec.east.nodes] : [spec.nodes];
  return lists.flat().map(([lon, lat, y]) => {
    const [x, z] = project(lon, lat);
    return { lon, lat, y, x, z };
  });
}

const ggOsm = centerlineFor((tags) => tags.name === 'Golden Gate Bridge');
const bayOsm = centerlineFor((tags) => /I 80/.test(tags.ref || ''));
const ggNodes = deckNodes('goldenGateBridge');
const bayNodes = deckNodes('bayBridge', true);

function alignment(label, id, nodes, osm, expectDeck) {
  if (!nodes.length || !osm.length) {
    check(id, label, false, `missing geometry (${nodes.length} model nodes, ${osm.length} OSM points)`);
    return;
  }
  let worst = 0;
  for (const n of nodes) worst = Math.max(worst, distanceToWays(osm, n.x, n.z));
  const deck = Math.max(...nodes.map((n) => n.y)).toFixed(0);
  check(id, label, worst <= 75, `worst deck node ${worst.toFixed(0)} m off the OSM centerline (tolerance 75 m); model midspan deck ${deck} m vs real ~${expectDeck} m`);
}
alignment('Golden Gate Bridge follows the real centerline', '1.8a', ggNodes, ggOsm, 67);
alignment('Bay Bridge follows the real centerline', '1.8b', bayNodes, bayOsm, 57);

const pointChecks = [
  ['alcatraz', -122.423, 37.8267],
  ['sutroTower', -122.4525, 37.7552],
  ['coitTower', -122.4058, 37.8024],
  ['ferryBuilding', -122.3937, 37.7955],
  ['transamerica', -122.4028, 37.7952],
  ['cityHall', -122.4193, 37.7793],
  ['oraclePark', -122.3893, 37.7786],
];
const pointErrors = [];
for (const [id, lon, lat] of pointChecks) {
  const l = LANDMARKS.find((k) => k.id === id);
  const [rx, rz] = project(lon, lat);
  const [mx, mz] = project(l.lon, l.lat);
  pointErrors.push({ id, error: Math.hypot(rx - mx, rz - mz) });
}
const worstPoint = pointErrors.reduce((a, b) => (b.error > a.error ? b : a));
check('1.8c', 'point landmarks within 75 m of their real coordinates', worstPoint.error <= 75, pointErrors.map((p) => `${p.id} ${p.error.toFixed(0)} m`).join(', '));

// Sutro Tower must stand on the ridge, not beside it.
const sutro = LANDMARKS.find((l) => l.id === 'sutroTower');
const [sux, suz] = project(sutro.lon, sutro.lat);
const sutroGround = sampleElevation(sux, suz);
check('1.8d', 'Sutro Tower base sits on the ~250 m ridge', sutroGround >= 220, `terrain at the tower ${sutroGround.toFixed(1)} m`);

// Approach-to-deck continuity: nearest baked street point to each bridge deck end.
function approachGap(nodes) {
  if (!nodes.length) return null;
  const ends = [nodes[0], nodes[nodes.length - 1]];
  const worst = { h: Infinity, v: Infinity };
  for (const end of ends) {
    // Nearest point on a street ribbon, not nearest baked vertex: the ribbon is
    // sampled every 10 m, so vertex distance alone would report a 5 m gap on a
    // road that runs straight through the abutment.
    let bestH = Infinity;
    let bestV = Infinity;
    for (const l of streetLines) {
      for (let i = 3; i < l.pts.length; i += 3) {
        const h = distanceToSegment(l.pts[i - 3], l.pts[i - 1], l.pts[i], l.pts[i + 2], end.x, end.z);
        if (h < bestH) {
          bestH = h;
          bestV = Math.min(Math.abs(l.pts[i + 1] - end.y), Math.abs(l.pts[i - 2] - end.y));
        }
      }
    }
    if (bestH < worst.h) {
      worst.h = bestH;
      worst.v = bestV;
    }
  }
  return worst;
}
const ggGap = approachGap(ggNodes);
const bayGap = approachGap(bayNodes);
check('1.8e', 'Golden Gate approach reaches the deck end (<=5 m h, <=2 m v)', ggGap && ggGap.h <= 5 && ggGap.v <= 2, ggGap ? `nearest street point ${ggGap.h.toFixed(0)} m horizontally, ${ggGap.v.toFixed(0)} m below the deck end` : 'no nodes');
check('1.8f', 'Bay Bridge approach reaches the deck end (<=5 m h, <=2 m v)', bayGap && bayGap.h <= 5 && bayGap.v <= 2, bayGap ? `nearest street point ${bayGap.h.toFixed(0)} m horizontally, ${bayGap.v.toFixed(0)} m below the deck end` : 'no nodes');

// Elevated freeway pass (Appendix A.6): are class 1/6 ribbons actually elevated?
let freewayPts = 0;
let freewayLifted = 0;
for (const l of streetLines) {
  if (l.klass !== freewayClass && l.klass !== rampClass) continue;
  for (let i = 0; i < l.pts.length; i += 3) {
    freewayPts++;
    if (l.pts[i + 1] - sampleElevation(l.pts[i], l.pts[i + 2]) > 3) freewayLifted++;
  }
}
check('A.6', 'freeway/ramp classes ride elevated decks', freewayPts > 0 && freewayLifted / freewayPts > 0.5, `${freewayLifted}/${freewayPts} freeway points more than 3 m above ground (classes ${STREET_CLASSES[freewayClass].id}/${STREET_CLASSES[rampClass].id})`);

// -------------------------------------------------------------- 3.3 payload --
const payload = {};
let total = 0;
for (const kind of ['buildings', 'streets', 'landcover']) {
  const files = await readdir(new URL(`${kind}/`, OUT));
  const index = { buildings: buildingsIndex, streets: streetsIndex, landcover: landcoverIndex }[kind];
  const bytes = index.cells.reduce((a, c) => a + c.bytes, 0);
  payload[kind] = { files: files.length, mb: +(bytes / 1e6).toFixed(2), largestMb: +(Math.max(...index.cells.map((c) => c.bytes)) / 1e6).toFixed(3) };
  total += bytes;
}
const terrainBytes = terrainDesc.size * terrainDesc.size * 2;
total += terrainBytes;
check('3.3', 'no baked file > 25 MB', Math.max(payload.buildings.largestMb, payload.streets.largestMb, payload.landcover.largestMb, terrainBytes / 1e6) <= 25, `largest is terrain.bin at ${(terrainBytes / 1e6).toFixed(1)} MB; per-cell max ${payload.landcover.largestMb} MB; total ${(total / 1e6).toFixed(1)} MB`);

// --------------------------------------------------------------- named parks --
check('1.9', 'named parks matched by landcover polygons', landcoverIndex.stats.missingParks.length === 0, `${NAMED_PARKS.length - landcoverIndex.stats.missingParks.length}/${NAMED_PARKS.length} matched`);

// ------------------------------------------------------------------ report ---
const width = Math.max(...rows.map((r) => r.label.length));
console.log('\nid     status  check');
for (const r of rows) {
  console.log(`${r.id.padEnd(6)} ${r.status.padEnd(6)}  ${r.label.padEnd(width)}  ${r.evidence}`);
}
const failed = rows.filter((r) => r.status === 'FAIL');
console.log(`\n${rows.filter((r) => r.status === 'PASS').length} passed, ${failed.length} failed, ${rows.filter((r) => r.status === 'INFO').length} informational`);

await writeFile(
  new URL('audit.json', OUT),
  JSON.stringify({ generated: new Date().toISOString(), rows, payload, floating: floating.slice(0, 200), heights: { median: pct(50), p95: pct(95), p99: pct(99), max: tallestProcedural } }, null, 1)
);
console.log('wrote out/audit.json');
