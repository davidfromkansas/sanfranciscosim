// The mood table lives twice: once in the writer (api/_lib/feeds/moods.mjs)
// and once in the diorama (app/src/population.js). The browser never talks to
// the writer, so duplicating four emoji beats putting a network fetch in front
// of the city — but duplicated tables drift, and the failure would be silent
// and awful: the face over somebody's head disagreeing with the voice in their
// posts. This is the check that stops that.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';

const root = new URL('../../', import.meta.url);
const writerSrc = await readFile(new URL('api/_lib/feeds/moods.mjs', root), 'utf8');
const cityStr = await readFile(new URL('app/src/population.js', root), 'utf8');

const keys = (src, re) => [...src.matchAll(re)].map((m) => m[1]);
const nums = (src, re) => {
  const m = src.match(re);
  return m ? m[1].split(',').map((n) => Number(n.trim())) : null;
};

test('both files list the same moods in the same order', () => {
  const writer = keys(writerSrc, /\{ at: -?\d+, key: "([a-z-]+)"/g);
  const city = keys(cityStr, /\{ key: '([a-z-]+)', emoji:/g);
  assert.ok(writer.length >= 3, 'found no moods in the writer');
  assert.deepEqual(city, writer, 'population.js and residents.mjs disagree about the moods');
});

test('both files weight the moods identically', () => {
  const writer = nums(writerSrc, /const MOOD_WEIGHTS = \[([^\]]+)\]/);
  const city = nums(cityStr, /const MOOD_BADGE_WEIGHTS = \[([^\]]+)\]/);
  assert.ok(writer, 'no MOOD_WEIGHTS in the writer');
  assert.deepEqual(city, writer, 'the badge weights and the writer weights disagree');
});

test('the two hashes put the same resident in the same mood', async () => {
  const { moodFor } = await import(new URL('api/_lib/feeds/moods.mjs', root).href);
  // Re-implement the city's lookup from its own source so a change there fails
  // here rather than being quietly compensated for.
  const weights = nums(cityStr, /const MOOD_BADGE_WEIGHTS = \[([^\]]+)\]/);
  const cityKeys = keys(cityStr, /\{ key: '([a-z-]+)', emoji:/g);
  const cityMood = (id) => {
    let h = 2166136261;
    for (let i = 0; i < id.length; i++) {
      h ^= id.charCodeAt(i);
      h = Math.imul(h, 16777619) >>> 0;
    }
    let roll = (h >>> 8) % weights.reduce((a, b) => a + b, 0);
    for (let i = 0; i < weights.length; i++) {
      roll -= weights[i];
      if (roll < 0) return cityKeys[i];
    }
    return cityKeys[2];
  };
  for (let i = 0; i < 2000; i++) {
    const id = `2024HU${i}-0${i % 4}`;
    assert.equal(cityMood(id), moodFor(id).key, `mood disagrees for ${id}`);
  }
});
