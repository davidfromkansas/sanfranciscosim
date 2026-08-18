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

import { promises as fs } from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.resolve(HERE, '../api/_data/personas.json');

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
  for (const household of data.households) {
    for (const person of household.personas) {
      if (!person.iss) {
        skipped++;
        continue;
      }
      people.push({
        id: person.id,
        // The paragraph. This is the ONLY thing the writer is given about them.
        persona: person.iss,
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

  const byPuma = {};
  for (const p of people) byPuma[p.puma] = (byPuma[p.puma] ?? 0) + 1;
  const size = Math.round((await fs.stat(OUT)).size / 1024);
  console.log(`${people.length} people with a paragraph · ${size} KB`);
  console.log(`  by PUMA: ${Object.entries(byPuma).map(([k, v]) => `${k} ${v}`).join(', ')}`);
  if (skipped) console.log(`  ${skipped} skipped — no identity paragraph written yet`);
}

main();
