// PERF-PLAN #4 (GLB half): meshopt-compress every shipped GLB under
// app/public/sf-assets. Run once per asset intake (not at build time) and
// commit the result — the asset contract's material names (Toy_* / _Glow)
// are load-bearing for the runtime merge, so -km keeps materials unmerged
// and -kn keeps names. -noq keeps attributes float32: the kit/landmark merge
// paths bake world matrices straight into the position arrays, which int16
// KHR_mesh_quantization attributes would corrupt (verified: quantized pieces
// all fail their dims gate and fall back to procedural). No simplification: geometry is byte-authoritative,
// only the encoding changes.
//
//   node pipeline/compress-assets.mjs          # compress in place
//   node pipeline/compress-assets.mjs --check  # report only, change nothing
//
// Requires gltfpack (`npx -y gltfpack`); three's bundled MeshoptDecoder
// (wired in app/src/gltf.js) decodes at runtime — no new runtime dependency.

import { execFileSync } from 'node:child_process';
import { promises as fs } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ASSETS = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../app/public/sf-assets');
const checkOnly = process.argv.includes('--check');

async function* glbs(dir) {
  for (const entry of await fs.readdir(dir, { withFileTypes: true })) {
    const p = path.join(dir, entry.name);
    if (entry.isDirectory()) yield* glbs(p);
    else if (entry.name.endsWith('.glb')) yield p;
  }
}

// Material names from a GLB's JSON chunk — verified identical before/after.
async function materialNames(file) {
  const buf = await fs.readFile(file);
  const jsonLen = buf.readUInt32LE(12);
  const json = JSON.parse(buf.subarray(20, 20 + jsonLen).toString());
  return {
    names: (json.materials || []).map((m) => m.name).sort(),
    meshopt: (json.extensionsRequired || []).includes('EXT_meshopt_compression'),
  };
}

let files = 0;
let before = 0;
let after = 0;
const failures = [];
for await (const file of glbs(ASSETS)) {
  const src = await fs.stat(file);
  const pre = await materialNames(file);
  if (pre.meshopt) {
    console.log(`skip (already compressed): ${path.relative(ASSETS, file)}`);
    continue;
  }
  if (checkOnly) {
    files++;
    before += src.size;
    continue;
  }
  const tmp = file.replace(/\.glb$/, '.pack.glb');
  try {
    execFileSync('npx', ['-y', 'gltfpack', '-i', file, '-o', tmp, '-c', '-km', '-kn', '-noq'], {
      stdio: 'pipe',
    });
    const post = await materialNames(tmp);
    if (JSON.stringify(post.names) !== JSON.stringify(pre.names)) {
      throw new Error(`material names changed: ${pre.names} -> ${post.names}`);
    }
    if (!post.meshopt) throw new Error('output missing EXT_meshopt_compression');
    const packed = await fs.stat(tmp);
    await fs.rename(tmp, file);
    files++;
    before += src.size;
    after += packed.size;
    console.log(
      `${path.relative(ASSETS, file)}: ${(src.size / 1024).toFixed(0)} -> ${(packed.size / 1024).toFixed(0)} KB`
    );
  } catch (err) {
    failures.push(`${path.relative(ASSETS, file)}: ${err.message}`);
    await fs.rm(tmp, { force: true });
  }
}

const mb = (n) => (n / 1024 / 1024).toFixed(1);
if (checkOnly) console.log(`[compress-assets] ${files} uncompressed GLBs, ${mb(before)} MB`);
else console.log(`[compress-assets] ${files} GLBs: ${mb(before)} MB -> ${mb(after)} MB (${(before / after).toFixed(2)}x)`);
if (failures.length) {
  console.error(`[compress-assets] ${failures.length} FAILED:\n  ` + failures.join('\n  '));
  process.exit(1);
}
