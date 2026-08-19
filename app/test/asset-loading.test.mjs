// Guards the "a visual feature quietly stopped existing" class of bug.
//
// The fog banks were invisible for two days because an unrelated intake pass
// meshopt-compressed fog-cube.glb while fogbanks.js was still building a bare
// GLTFLoader. Rule 3 (procedural fallback, never a crash) did its job and the
// shader fog carried the scene, which is exactly why nobody saw a red light:
// the failure mode of every asset-backed effect here is silence.
//
// So these tests assert the two things that silence can hide:
//   1. every module that loads a shipped GLB goes through createGLTFLoader,
//      the only loader in the app with the meshopt decoder wired;
//   2. every GLB path a module hard-codes actually exists on disk.
//
// They read source text rather than importing the modules because the visual
// systems are Vite modules (import.meta.env, WebGL) and cannot boot in node.

import test from 'node:test';
import assert from 'node:assert/strict';
import { readdirSync, readFileSync, existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const SRC = path.join(ROOT, 'src');
const PUBLIC = path.join(ROOT, 'public');

const sources = readdirSync(SRC)
  .filter((f) => f.endsWith('.js'))
  .map((f) => ({ file: f, text: readFileSync(path.join(SRC, f), 'utf8') }));

test('createGLTFLoader is the only GLTF loader in the app', () => {
  for (const { file, text } of sources) {
    if (file === 'gltf.js') continue;
    assert.ok(
      !/from 'three\/addons\/loaders\/GLTFLoader\.js'/.test(text),
      `${file} imports GLTFLoader directly. A bare loader has no meshopt decoder and every shipped GLB is compressed, so it will fail the file, not the app — import createGLTFLoader from ./gltf.js instead.`
    );
  }
});

test('the shared loader wires the meshopt decoder', () => {
  const text = readFileSync(path.join(SRC, 'gltf.js'), 'utf8');
  assert.match(text, /setMeshoptDecoder\(MeshoptDecoder\)/);
});

test('every module that loads a GLB uses the shared loader', () => {
  for (const { file, text } of sources) {
    if (file === 'gltf.js') continue;
    if (!/\.glb\b/.test(text)) continue;
    assert.match(
      text,
      /import \{ createGLTFLoader \} from '\.\/gltf\.js'/,
      `${file} references a shipped GLB but does not import createGLTFLoader`
    );
  }
});

test('hard-coded GLB paths point at files that exist', () => {
  const misses = [];
  for (const { file, text } of sources) {
    for (const [, asset] of text.matchAll(/\$\{import\.meta\.env\.BASE_URL\}(sf-assets\/[\w./-]+\.glb)/g)) {
      if (!existsSync(path.join(PUBLIC, asset))) misses.push(`${file} -> ${asset}`);
    }
  }
  assert.deepEqual(misses, [], `missing assets (the loader warns and the feature silently disappears):\n${misses.join('\n')}`);
});

// The fog banks specifically: this is the asset that went missing, and the one
// whose absence is hardest to notice because shader fog looks like weather.
test('the fog cube ships and is a readable GLB', () => {
  const file = path.join(PUBLIC, 'sf-assets/fog-cube.glb');
  assert.ok(existsSync(file), 'fog-cube.glb is missing — the visible fog banks cannot exist without it');
  const buf = readFileSync(file);
  assert.equal(buf.subarray(0, 4).toString('ascii'), 'glTF', 'fog-cube.glb is not a GLB');

  // If it is meshopt-compressed (it is, and every future re-intake will be),
  // only a decoder-aware loader can read it. Assert the pairing holds.
  const jsonLength = buf.readUInt32LE(12);
  const gltf = JSON.parse(buf.subarray(20, 20 + jsonLength).toString('utf8'));
  const needsDecoder = (gltf.extensionsRequired ?? []).includes('EXT_meshopt_compression');
  const banks = readFileSync(path.join(SRC, 'fogbanks.js'), 'utf8');
  if (needsDecoder) {
    assert.match(
      banks,
      /createGLTFLoader\(\)\.load\(/,
      'fog-cube.glb is meshopt-compressed but fogbanks.js is not loading it with createGLTFLoader'
    );
  }
});

// Fog is the headline effect on a foggy day, so it is the LAST thing the
// performance governor may cut. A zero here made the fog vanish outright the
// moment a loaded machine got demoted, which reads as "fog is broken again".
test('no quality tier drops the fog banks to zero', () => {
  const banks = readFileSync(path.join(SRC, 'fogbanks.js'), 'utf8');
  const caps = banks.match(/export const BANK_CAPS = \{([^}]*)\}/);
  assert.ok(caps, 'BANK_CAPS not found in fogbanks.js');
  const entries = [...caps[1].matchAll(/(\w+):\s*(\d+)/g)];
  assert.deepEqual(
    entries.map((e) => e[1]).sort(),
    ['high', 'low', 'medium', 'ultra'],
    'every quality tier needs a fog bank cap'
  );
  for (const [, tier, count] of entries) {
    assert.ok(Number(count) > 0, `BANK_CAPS.${tier} is 0 — fog must thin out with the tier, never disappear`);
  }
});
