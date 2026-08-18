// Bake the feed OUTLINE the API writes words into.
//
// The personas project decides the hard part offline: which real event each
// resident would speak about, who replies to whom, and the Census fact that
// makes them care (a rent of $5,600 against their income is why this person,
// and not the one next door, talks about evictions). None of that is a
// judgement call for the writer at request time — by the time /api/feed runs,
// the cast and the running order are fixed and the only open question is what
// the words are.
//
// Only residents with an authored identity paragraph appear. The paragraph IS
// the voice, and a resident without one would get filled in from demographics,
// which is the failure the whole format exists to avoid.
//
//   node pipeline/bake-feed-seed.mjs
//   node pipeline/bake-feed-seed.mjs --personas ~/some/other/repo
//
// Output (committed): api/_data/feed-seed.json

import { promises as fs } from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.resolve(HERE, '../api/_data/feed-seed.json');

function arg(name, fallback) {
  const i = process.argv.indexOf(`--${name}`);
  return i !== -1 && process.argv[i + 1] ? process.argv[i + 1] : fallback;
}

const SRC = path.resolve(arg('personas', path.join(os.homedir(), 'san-francisco-pums-personas')));

async function main() {
  const base = path.join(SRC, 'public/pums-data');
  let feed;
  let personas;
  try {
    [feed, personas] = await Promise.all([
      fs.readFile(path.join(base, 'feed.json'), 'utf8').then(JSON.parse),
      fs.readFile(path.join(base, 'personas.json'), 'utf8').then(JSON.parse),
    ]);
  } catch (error) {
    console.error(`Cannot read the personas project at ${base}\nPass --personas <repo path>.\n${error.message}`);
    process.exit(1);
  }

  const byId = new Map();
  for (const household of personas.households) {
    for (const persona of household.personas) byId.set(persona.id, { ...persona, puma: household.puma });
  }

  // Speakers are listed once and referenced by id: the identity paragraph is
  // ~900 characters and the same people recur across threads.
  const speakers = {};
  const threads = [];
  let dropped = 0;

  for (const thread of feed.threads) {
    const slots = [];
    for (const c of thread.contributions) {
      const persona = byId.get(c.author.id);
      if (!persona?.iss) {
        dropped++;
        continue;
      }
      speakers[persona.id] ??= {
        id: persona.id,
        name: persona.name,
        age: persona.age,
        occupation: persona.occupation,
        puma: persona.puma,
        iss: persona.iss,
      };
      slots.push({
        id: c.id,
        speaker: persona.id,
        // Why this person and not another. Handed to the writer as the ONE
        // thing they are allowed to be pointed about, so the post lands on a
        // real detail of their life instead of a general opinion.
        because: (c.because ?? []).map((b) => ({
          topic: b.topic,
          strength: b.strength,
          fact: b.basis?.value ?? null,
        })),
      });
    }
    if (slots.length < 2) continue; // a post with nobody to answer it is not a thread
    threads.push({
      id: thread.id,
      event: {
        headline: thread.event.headline,
        // A URL is not a description of what happened. Older event files stored
        // the article link here, which reached the writer as a base64 Google
        // News redirect under the words "WHAT HAPPENED" — noise it paid tokens
        // to read. Real summaries pass through; links are dropped and the
        // headline stands alone.
        detail: /^https?:\/\//.test(thread.event.detail ?? '') ? '' : (thread.event.detail ?? ''),
        source: thread.event.source,
        where: thread.event.place?.neighbourhoods?.[0] ?? 'San Francisco',
        scope: thread.event.place?.scope ?? 'citywide',
      },
      slots,
    });
  }

  await fs.writeFile(
    OUT,
    JSON.stringify({
      note: 'Baked by pipeline/bake-feed-seed.mjs. The running order; /api/feed writes the words. Do not hand-edit.',
      day: feed.summary?.day ?? null,
      label: feed.summary?.label ?? null,
      threads,
      speakers,
    })
  );

  const slots = threads.reduce((n, t) => n + t.slots.length, 0);
  const size = Math.round((await fs.stat(OUT)).size / 1024);
  console.log(`${threads.length} threads · ${slots} slots · ${Object.keys(speakers).length} speakers · ${size} KB`);
  if (dropped) console.log(`${dropped} slots dropped — no identity paragraph for that resident`);
}

main();
