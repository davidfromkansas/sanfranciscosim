// Validation gate: hard-fails if the baked city is not the real city.
// Run this before touching the renderer.

import { readFile, readdir, mkdir, writeFile, copyFile, rm } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { LANDMARKS, NAMED_PARKS, VIEW_PRESETS } from './lib/landmarks.mjs';
import { CELL_SIZE, EXTENT, GRID, LAT0, LON0, project } from './lib/geo.mjs';
import { loadHeightmap } from './lib/heightmap.mjs';
import { LAND_KINDS, STREET_CLASSES } from './lib/classes.mjs';
import { PALETTE } from './lib/districts.mjs';

const OUT = new URL('./out/', import.meta.url);
const APP_TILES = new URL('../app/public/tiles/', import.meta.url);
const API_DATA = new URL('../api/_data/', import.meta.url);

const failures = [];
const notes = [];

function check(label, ok, detail) {
  if (ok) notes.push(`  ok   ${label} — ${detail}`);
  else failures.push(`  FAIL ${label} — ${detail}`);
}

const buildings = JSON.parse(await readFile(new URL('buildings.json', OUT), 'utf8'));
const streets = JSON.parse(await readFile(new URL('streets.json', OUT), 'utf8'));
const landcover = JSON.parse(await readFile(new URL('landcover.json', OUT), 'utf8'));
const bridges = JSON.parse(await readFile(new URL('bridges.json', OUT), 'utf8'));
const piers = JSON.parse(await readFile(new URL('piers.json', OUT), 'utf8'));
const { desc: terrain, sampleElevation } = await loadHeightmap();

// --- buildings -------------------------------------------------------------
check(
  'building count >= 150000',
  buildings.stats.total >= 150000,
  `${buildings.stats.total} baked (${buildings.stats.datasf} DataSF + ${buildings.stats.overtureAdded} Overture)`
);

const proceduralTallest = buildings.stats.tallest.height;
check(
  'tallest procedural building 200-340 m',
  proceduralTallest >= 200 && proceduralTallest <= 340,
  `${proceduralTallest} m (heights in meters, not feet)`
);

// Salesforce Tower and the other silhouettes on the exclusion list are bespoke
// models, so the skyline peak is asserted against the landmark registry.
const salesforce = LANDMARKS.find((l) => l.id === 'salesforceTower');
check(
  'Salesforce Tower height 320-330 m',
  salesforce.height >= 320 && salesforce.height <= 330,
  `${salesforce.height} m bespoke model`
);

// --- streets ---------------------------------------------------------------
check(
  'street length 1500-2500 km',
  streets.stats.totalLengthKm >= 1500 && streets.stats.totalLengthKm <= 2500,
  `${streets.stats.totalLengthKm} km over ${streets.stats.segments} segments`
);
for (const [name, hits] of Object.entries(streets.stats.spotChecks)) {
  check(`street present: ${name}`, hits > 0, `${hits} segments`);
}

// --- terrain ---------------------------------------------------------------
check(
  'terrain max elevation 250-300 m',
  terrain.maxElev >= 250 && terrain.maxElev <= 300,
  `${terrain.maxElev.toFixed(1)} m`
);
const [fx, fz] = project(-122.3937, 37.7955);
const ferry = sampleElevation(fx, fz);
check('Ferry Building elevation < 10 m', ferry < 10, `${ferry.toFixed(1)} m`);
const [tx, tz] = project(-122.4477, 37.7544);
const twin = sampleElevation(tx, tz);
check('Twin Peaks elevation > 200 m', twin > 200, `${twin.toFixed(1)} m`);
const [ox, oz] = project(-122.5094, 37.7597); // Ocean Beach
check('Ocean Beach elevation < 15 m', sampleElevation(ox, oz) < 15, `${sampleElevation(ox, oz).toFixed(1)} m`);

// --- bridges and viaducts --------------------------------------------------
// Both bespoke bridges must be built from real OSM geometry, and their decks
// must meet the land (or the viaduct) at the abutments rather than stopping in
// mid-air over the water.
for (const [id, spec] of Object.entries(bridges)) {
  const ends = [spec.nodes[0], spec.nodes[spec.nodes.length - 1]];
  for (const [i, node] of ends.entries()) {
    const [x, z] = project(node[0], node[1]);
    const ground = sampleElevation(x, z);
    const clearance = node[2] - ground;
    check(
      `${id} abutment ${i === 0 ? 'A' : 'B'} sits on land`,
      ground > 0 && clearance >= 0 && clearance <= 25,
      `deck ${node[2].toFixed(1)} m over ground ${ground.toFixed(1)} m`
    );
  }
  check(`${id} deck nodes from OSM centreline`, spec.nodes.length >= 20, `${spec.nodes.length} nodes, ${spec.towers.length} towers`);
}
check('elevated freeway sections carry piers', piers.piers.length > 50, `${piers.piers.length} piers every ${piers.spacing} m`);

// --- landcover -------------------------------------------------------------
check(
  'all named parks matched',
  landcover.stats.missingParks.length === 0,
  landcover.stats.missingParks.length ? landcover.stats.missingParks.join(', ') : `${NAMED_PARKS.length} parks`
);
check('tree instances > 50000', landcover.stats.trees > 50000, `${landcover.stats.trees} trees`);

// --- landmark coverage ----------------------------------------------------
const buildingCells = new Set(buildings.cells.map((c) => c.key));
for (const l of LANDMARKS) {
  const [x, z] = project(l.lon, l.lat);
  const key = `${Math.floor((x - GRID.originX) / CELL_SIZE)}_${Math.floor((z - GRID.originZ) / CELL_SIZE)}`;
  const inExtent = x >= EXTENT.minX && x <= EXTENT.maxX && z >= EXTENT.minZ && z <= EXTENT.maxZ;
  check(`landmark in extent: ${l.name}`, inExtent, `cell ${key}${buildingCells.has(key) ? '' : ' (no procedural buildings — exclusion zone applied)'}`);
}

// --- blob integrity -------------------------------------------------------
for (const [name, index] of [
  ['buildings', buildings],
  ['streets', streets],
  ['landcover', landcover],
]) {
  const files = await readdir(new URL(`${name}/`, OUT));
  const bins = files.filter((f) => f.endsWith('.bin'));
  check(
    `${name} blobs match index`,
    bins.length === index.cells.length,
    `${bins.length} files / ${index.cells.length} index entries`
  );
  const oversize = index.cells.filter((c) => c.bytes > 90 * 1e6);
  check(`${name} blobs < 90 MB each`, oversize.length === 0, `largest ${(Math.max(...index.cells.map((c) => c.bytes)) / 1e6).toFixed(2)} MB`);
}

console.log(notes.join('\n'));
if (failures.length) {
  console.error('\nVALIDATION FAILED:\n' + failures.join('\n'));
  process.exit(1);
}
console.log('\nvalidation passed');

// --- publish to the app ---------------------------------------------------
const manifest = {
  generated: new Date().toISOString(),
  projection: { lon0: LON0, lat0: LAT0, mPerDegLon: 111320 * Math.cos((LAT0 * Math.PI) / 180), mPerDegLat: 110540 },
  extent: EXTENT,
  grid: GRID,
  cellSize: CELL_SIZE,
  terrain,
  palette: PALETTE,
  streetClasses: STREET_CLASSES,
  landKinds: LAND_KINDS,
  landuse: landcover.raster,
  landmarks: LANDMARKS,
  bridges,
  piers: piers.piers,
  parks: NAMED_PARKS,
  viewPresets: VIEW_PRESETS,
  stats: {
    buildings: buildings.stats,
    streets: streets.stats,
    landcover: landcover.stats,
  },
};

// Clear only the tiers this stage republishes, so a cell that no longer exists
// cannot survive as a stale file. It used to wipe app/public/tiles/ wholesale,
// which also deleted output this stage does not own: `toy`/`context` re-publish
// theirs later in the chain and so never noticed, but `muni-shapes.bin` has no
// later stage to restore it — `muni-shapes.mjs` needs MUNI_511_KEY and no-ops
// without one, by which point this had already removed the committed file. The
// symptom was a `sf-muni: no route shapes (shapes bad magic)` warning and buses
// that dead-reckon, and it took a hand-restore twice (e7ed9a46, and again
// during the five-landmark batch in #113) before the cause was found here.
await mkdir(APP_TILES, { recursive: true });
await mkdir(API_DATA, { recursive: true });
await writeFile(new URL('manifest.json', APP_TILES), JSON.stringify(manifest));
await writeFile(
  new URL('projection.json', API_DATA),
  JSON.stringify(manifest.projection),
);
await copyFile(new URL('terrain.bin', OUT), new URL('terrain.bin', APP_TILES));
await copyFile(new URL('landuse.bin', OUT), new URL('landuse.bin', APP_TILES));
for (const name of ['buildings', 'streets', 'landcover']) {
  const src = new URL(`${name}/`, OUT);
  const dst = new URL(`${name}/`, APP_TILES);
  await rm(dst, { recursive: true, force: true });
  await mkdir(dst, { recursive: true });
  const files = await readdir(src);
  for (const f of files) await copyFile(new URL(f, src), new URL(f, dst));
  const index = { buildings, streets, landcover }[name];
  await writeFile(new URL(`${name}.json`, APP_TILES), JSON.stringify(index));
}
if (!existsSync(new URL('manifest.json', APP_TILES))) throw new Error('publish failed');
console.log(`published baked tiles to app/public/tiles/`);
