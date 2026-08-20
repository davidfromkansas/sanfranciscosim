// Size the shared landmark BatchedMesh straight from the GLB accessors — no
// browser needed. Run from the repo root:
//
//   node artifacts/one-steuart-lane/batch_reserve_check.mjs
//
// The reserve overflows SILENTLY — each reload drops a different landmark rather
// than erroring — so this is the check that catches it before a batch ships. The loader merges each landmark to one body mesh + one glow
// set, so the body reserve must hold the sum of every simultaneously-loaded
// landmark's non-glow POSITION count.
import { readFileSync, existsSync } from 'node:fs';
const DIR = 'app/public/sf-assets/landmarks/';
const manifest = JSON.parse(readFileSync('app/public/sf-assets/landmarks_manifest.json', 'utf8'));

function glbJson(buf) {
  const dv = new DataView(buf.buffer, buf.byteOffset, buf.byteLength);
  let off = 12;
  while (off < buf.length) {
    const len = dv.getUint32(off, true), type = dv.getUint32(off + 4, true);
    if (type === 0x4e4f534a) return JSON.parse(buf.toString('utf8', off + 8, off + 8 + len));
    off += 12 + len - 4;
  }
  throw new Error('no JSON chunk');
}

let body = 0, glow = 0, missing = 0;
const rows = [];
for (const e of manifest) {
  const f = DIR + e.file;
  if (!existsSync(f)) { missing++; continue; }
  const j = glbJson(readFileSync(f));
  let b = 0, g = 0;
  for (const mesh of j.meshes ?? []) {
    for (const p of mesh.primitives ?? []) {
      const n = j.accessors[p.attributes.POSITION].count;
      const name = j.materials?.[p.material]?.name ?? '';
      if (name.endsWith('_Glow')) g += n; else b += n;
    }
  }
  body += b; glow += g;
  rows.push({ id: e.id, b, g });
}
rows.sort((a, x) => x.b - a.b);
console.log(`manifest entries: ${manifest.length}  (GLBs missing locally: ${missing})`);
console.log(`ALL landmarks resident at once: body ${body.toLocaleString()} verts / 1,600,000 reserve  (${(body/1.6e6*100).toFixed(1)}%)`);
console.log(`                                glow ${glow.toLocaleString()} verts / 250,000 reserve  (${(glow/2.5e5*100).toFixed(1)}%)`);
console.log('\nheaviest bodies:');
for (const r of rows.slice(0, 6)) console.log(`  ${r.id.padEnd(28)} ${r.b.toLocaleString().padStart(9)} body  ${r.g.toLocaleString().padStart(7)} glow`);
const mine = rows.find(r => r.id === 'one-steuart-lane');
console.log(`\none-steuart-lane: ${mine.b.toLocaleString()} body + ${mine.g.toLocaleString()} glow = ${((mine.b+mine.g)/(body+glow)*100).toFixed(1)}% of the total`);
