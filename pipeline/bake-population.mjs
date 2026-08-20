// Bake the PUMS-grounded population into the two small files the city streams:
// who the residents are, and where each PUMA is on the ground.
//
// Source of truth lives OUTSIDE this repo — the personas project holds the
// Census sampling, the authored identity paragraphs and the Census records.
// None of that belongs in the browser. This script takes the thin slice the
// diorama actually needs (a name, an age, an occupation, a neighbourhood) and
// leaves the rest where it is.
//
// Run it when the persona set changes and COMMIT the output, the same way
// tiles and the landmark manifest are committed. The data changes on the order
// of weeks; a live endpoint would buy nothing and cost a function, a cold start
// and a network dependency the app currently does not have.
//
//   node pipeline/bake-population.mjs
//   node pipeline/bake-population.mjs --personas ~/some/other/repo
//
// Outputs (both committed):
//   app/public/sf-people/people.json  — one entry per resident
//   app/public/sf-people/pumas.json   — neighbourhood polygons in local metres
//
// If either file is missing the app renders the anonymous pedestrian pool
// exactly as it did before (iron rule 3 — the fallback is never deleted).

import { promises as fs } from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.resolve(HERE, '../app/public/sf-people');

function arg(name, fallback) {
  const i = process.argv.indexOf(`--${name}`);
  return i !== -1 && process.argv[i + 1] ? process.argv[i + 1] : fallback;
}

const SRC = path.resolve(
  arg('personas', path.join(os.homedir(), 'san-francisco-pums-personas')),
);

// The one projection, copied from AGENTS.md. Baking in local metres means the
// runtime never converts anything: point-in-polygon runs directly against the
// same x/z the street paths already use.
const LON0 = -122.4375;
const LAT0 = 37.77;
const toX = (lon) => (lon - LON0) * 111320 * Math.cos((LAT0 * Math.PI) / 180);
const toZ = (lat) => -(lat - LAT0) * 110540;

// PUMA names as the diorama should show them, not as the Census writes them.
const PUMA_NAMES = {
  '07507': 'Bayview & Hunters Point',
  '07508': 'Richmond & Presidio',
  '07509': 'Chinatown & North Beach',
  '07510': 'Mission & SoMa',
  '07511': 'Bernal & the Castro',
  '07512': 'The Sunset',
  '07513': 'Ingleside',
  '07514': 'Marina & Western Addition',
};

async function main() {
  const personasPath = path.join(SRC, 'public/pums-data/personas.json');
  const geoPath = path.join(SRC, 'data/geography/analysis-neighborhoods.geojson');
  const placesPath = path.join(SRC, 'scripts/sf-places.mjs');

  let personas;
  try {
    personas = JSON.parse(await fs.readFile(personasPath, 'utf8'));
  } catch {
    console.error(`No personas at ${personasPath}\nPass --personas <repo path>.`);
    process.exit(1);
  }

  const { PUMA_OF } = await import(placesPath);
  const geo = JSON.parse(await fs.readFile(geoPath, 'utf8'));

  // ---------------------------------------------------------------- people ---
  // Under-18s exist in the household record but are never written as characters
  // and never walk the city.
  const people = [];
  for (const household of personas.households) {
    for (const persona of household.personas) {
      if (persona.age < 18) continue;
      if (!PUMA_NAMES[household.puma]) continue;
      people.push({
        id: persona.id,
        name: persona.name,
        age: persona.age,
        occupation: persona.occupation || '',
        puma: household.puma,
      });
    }
  }
  people.sort((a, b) => a.id.localeCompare(b.id));

  // --------------------------------------------------------------- polygons ---
  // The 41 analysis neighborhoods, each tagged with the PUMA it belongs to.
  // Neighbourhoods rather than merged PUMA outlines: a union would need real
  // polygon arithmetic, and point-in-polygon against the parts then looking up
  // the parent gives the identical answer for free.
  //
  // Coordinates are decimated and rounded to the metre. This is a spawn test,
  // not a boundary render — a resident landing two metres inside the wrong
  // neighbourhood is invisible, and the file drops from megabytes to kilobytes.
  const areas = [];
  let droppedRings = 0;
  for (const feature of geo.features) {
    const nhood = feature.properties?.nhood;
    const puma = PUMA_OF[nhood];
    if (!puma || !PUMA_NAMES[puma]) continue;
    const polygons =
      feature.geometry.type === 'MultiPolygon'
        ? feature.geometry.coordinates
        : [feature.geometry.coordinates];

    const rings = [];
    for (const polygon of polygons) {
      // Outer ring only. The holes in these boundaries are a handful of square
      // metres of water; a resident spawning in one is not a defect worth 40 KB.
      const ring = polygon[0];
      const step = Math.max(1, Math.floor(ring.length / 120));
      const flat = [];
      for (let i = 0; i < ring.length; i += step) {
        flat.push(Math.round(toX(ring[i][0])), Math.round(toZ(ring[i][1])));
      }
      if (flat.length < 8) {
        droppedRings++;
        continue;
      }
      rings.push(flat);
    }
    if (rings.length) areas.push({ nhood, puma, rings });
  }

  // ----------------------------------------------------------------- write ---
  await fs.mkdir(OUT, { recursive: true });
  await fs.writeFile(
    path.join(OUT, 'people.json'),
    JSON.stringify({
      note: 'Baked by pipeline/bake-population.mjs from the PUMS personas project. Do not hand-edit.',
      pumaNames: PUMA_NAMES,
      people,
    }),
  );
  await fs.writeFile(
    path.join(OUT, 'pumas.json'),
    JSON.stringify({
      note: 'Analysis-neighborhood outlines in local metres (AGENTS.md projection), decimated for spawn tests.',
      areas,
    }),
  );

  const byPuma = {};
  for (const p of people) byPuma[p.puma] = (byPuma[p.puma] ?? 0) + 1;
  const sizeOf = async (f) => Math.round((await fs.stat(path.join(OUT, f))).size / 1024);

  console.log(`${people.length} residents across ${Object.keys(byPuma).length} PUMAs`);
  for (const puma of Object.keys(PUMA_NAMES)) {
    const n = byPuma[puma] ?? 0;
    console.log(`  ${puma}  ${String(n).padStart(4)}  ${PUMA_NAMES[puma]}${n ? '' : '   (no residents written yet)'}`);
  }
  console.log(`${areas.length} neighbourhood outlines${droppedRings ? `, ${droppedRings} tiny rings dropped` : ''}`);
  console.log(`people.json ${await sizeOf('people.json')} KB · pumas.json ${await sizeOf('pumas.json')} KB`);
}

main();
