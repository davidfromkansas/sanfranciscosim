// Bake the cast of r/simfrancisco: one paragraph per person, nothing else.
//
// The simulation needs exactly two things — who someone is, and what the
// community is for. So this emits the identity paragraph and the few fields the
// panel prints beside a name. No topics, no interests, no Census columns, no
// events: whatever a resident decides to post about has to come out of the
// paragraph, because the paragraph is all the writer will ever see.
//
// Only people with an authored paragraph appear. Without one there is no voice
// to write in, and the model would fill the gap from demographics — the exact
// failure the format exists to prevent.
//
//   node pipeline/bake-personas.mjs
//   node pipeline/bake-personas.mjs --personas ~/some/other/repo
//
// Output (committed): api/_data/personas.json
//                     app/public/sf-people/personas/<puma>.json

import { promises as fs } from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.resolve(HERE, '../api/_data/personas.json');
// Per-PUMA paragraph shards the app fetches when a resident is clicked.
const SHARDS = path.resolve(HERE, '../app/public/sf-people/personas');

// Where each PUMA is, in the words a resident would use. The writer is told
// this because the paragraphs mostly do not say: 79% of them never name a
// neighbourhood, so a model asked for a post that needs a place invented one,
// and residents were writing "it's quiet here in the Sunset" from Bayview.
const PUMA_NAMES = {
  '07507': 'Bayview & Hunters Point',
  '07508': 'the Richmond',
  '07509': 'Chinatown & North Beach',
  '07510': 'the Mission & SoMa',
  '07511': 'Bernal Heights & the Castro',
  '07512': 'the Sunset',
  '07513': 'Ingleside',
  '07514': 'the Marina & Western Addition',
};

function arg(name, fallback) {
  const i = process.argv.indexOf(`--${name}`);
  return i !== -1 && process.argv[i + 1] ? process.argv[i + 1] : fallback;
}

const SRC = path.resolve(arg('personas', path.join(os.homedir(), 'san-francisco-pums-personas')));

async function main() {
  const source = path.join(SRC, 'public/pums-data/personas.json');
  let data;
  try {
    data = JSON.parse(await fs.readFile(source, 'utf8'));
  } catch (error) {
    console.error(`Cannot read ${source}\nPass --personas <repo path>.\n${error.message}`);
    process.exit(1);
  }

  const people = [];
  let skipped = 0;
  let minors = 0;
  for (const household of data.households) {
    for (const person of household.personas) {
      if (!person.iss) {
        skipped++;
        continue;
      }
      // Adults only, the same cut bake-population.mjs makes. Children exist in
      // the household records and now have paragraphs — the authoring packets
      // list every person in a household, because a parent's paragraph has to
      // name their kids consistently. But a three-year-old is not a poster on
      // a city subreddit, and the cast this file feeds is the cast that writes.
      // They stay in the source, out of the cast.
      if (typeof person.age === 'number' && person.age < 18) {
        minors++;
        continue;
      }
      people.push({
        id: person.id,
        // The paragraph. This is the ONLY thing the writer is given about them.
        persona: person.iss,
        // Where they live. The ONE fact the writer gets beyond the paragraph,
        // because the paragraph usually omits it and a resident who does not
        // know their own neighbourhood makes one up.
        neighbourhood: PUMA_NAMES[household.puma] ?? 'San Francisco',
        // Printed beside the name in the panel; never shown to the model.
        name: person.name,
        occupation: person.occupation ?? '',
        puma: household.puma,
      });
    }
  }
  people.sort((a, b) => a.id.localeCompare(b.id));

  await fs.writeFile(
    OUT,
    JSON.stringify({
      note: 'Baked by pipeline/bake-personas.mjs. The cast of r/simfrancisco. Do not hand-edit.',
      people,
    })
  );

  // The same paragraphs, sharded for the CITY to read on demand. The boot bake
  // (bake-population.mjs) deliberately carries no prose: 856 KB of paragraphs
  // for 829 residents, on every visit, to show the one a viewer clicks. So the
  // paragraphs ship separately, one file per PUMA, fetched only when somebody
  // opens a resident — and the first click in a neighbourhood pays for every
  // other resident in it.
  //
  // Sharded by PUMA rather than one file per person because a resident is
  // reached by walking a neighbourhood: 8 files of ~100 KB beats 829 of 1 KB
  // for exactly the access pattern the city has.
  await fs.mkdir(SHARDS, { recursive: true });
  const shards = new Map();
  for (const p of people) {
    if (!shards.has(p.puma)) shards.set(p.puma, {});
    shards.get(p.puma)[p.id] = p.persona;
  }
  for (const [puma, entries] of shards) {
    await fs.writeFile(path.join(SHARDS, `${puma}.json`), JSON.stringify(entries));
  }

  const byPuma = {};
  for (const p of people) byPuma[p.puma] = (byPuma[p.puma] ?? 0) + 1;
  const size = Math.round((await fs.stat(OUT)).size / 1024);
  const shardKB = Math.round(
    (await Promise.all([...shards.keys()].map(async (puma) =>
      (await fs.stat(path.join(SHARDS, `${puma}.json`))).size))).reduce((a, b) => a + b, 0) / 1024
  );
  console.log(`${shards.size} persona shards for the city · ${shardKB} KB total`);
  console.log(`${people.length} people with a paragraph · ${size} KB`);
  console.log(`  by PUMA: ${Object.entries(byPuma).map(([k, v]) => `${k} ${v}`).join(', ')}`);
  if (skipped) console.log(`  ${skipped} skipped — no identity paragraph written yet`);
  if (minors) console.log(`  ${minors} skipped — under 18, not part of the cast`);
}

main();
