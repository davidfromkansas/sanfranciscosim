// Conform a hand-authored aircraft GLB to the asset contract (AGENTS.md).
//
//   node tools/conform-aircraft-glb.mjs <in.glb> <out.glb>
//
// The airframes in app/src/aircraft.js are drawn by an instanced loader that
// assumes the contract: front faces -Z, flat `Toy_*` materials, `*_Glow` for
// surfaces that light up at night. A model authored nose-along-+X with
// descriptive material names is perfectly good work that simply speaks a
// different dialect, and this translates it ONCE, at intake, rather than
// teaching the loader every dialect it might meet.
//
// What it does, and nothing else:
//   1. Rotates the scene so the nose points -Z (the vehicle manifest's `front`).
//   2. Recentres X/Z on the airframe so the instance transform spins it about
//      its own axis. Y is left alone: the air layer positions aircraft by their
//      centreline, not by a ground contact point, so the authored height is
//      already right.
//   3. Renames materials `Toy_*`, suffixing `_Glow` on the ones that are lights.
//
// Geometry is untouched — the binary chunk is copied through byte for byte.

import { readFileSync, writeFileSync } from 'node:fs';

const [, , inPath, outPath] = process.argv;
if (!inPath || !outPath) {
  console.error('usage: node tools/conform-aircraft-glb.mjs <in.glb> <out.glb>');
  process.exit(1);
}

// Materials that are LIGHTS rather than paint. These are the surfaces the night
// system ignites, so they carry the `_Glow` suffix the loader splits on.
const GLOW = new Set(['Navigation Red', 'Navigation Green', 'Landing Light', 'Cockpit Iris Green']);

const toyName = (name) => {
  const base = `Toy_${String(name).trim().replace(/[^A-Za-z0-9]+/g, '_')}`;
  return GLOW.has(name) ? `${base}_Glow` : base;
};

// ---------------------------------------------------------------- glb io

function readGlb(buf) {
  if (buf.readUInt32LE(0) !== 0x46546c67) throw new Error('not a glb');
  const length = buf.readUInt32LE(8);
  let off = 12;
  let json = null;
  let bin = null;
  while (off < length) {
    const chunkLength = buf.readUInt32LE(off);
    const chunkType = buf.readUInt32LE(off + 4);
    const body = buf.subarray(off + 8, off + 8 + chunkLength);
    if (chunkType === 0x4e4f534a) json = JSON.parse(body.toString('utf8'));
    else if (chunkType === 0x004e4942) bin = body;
    off += 8 + chunkLength;
  }
  if (!json) throw new Error('glb has no JSON chunk');
  return { json, bin };
}

function writeGlb(json, bin) {
  const pad = (b, to) => {
    const extra = (to - (b.length % to)) % to;
    return extra ? Buffer.concat([b, Buffer.alloc(extra, to === 4 ? 0x20 : 0)]) : b;
  };
  const jsonChunk = pad(Buffer.from(JSON.stringify(json), 'utf8'), 4);
  const binChunk = bin ? pad(Buffer.from(bin), 4) : null;
  const total = 12 + 8 + jsonChunk.length + (binChunk ? 8 + binChunk.length : 0);
  const out = Buffer.alloc(total);
  out.writeUInt32LE(0x46546c67, 0);
  out.writeUInt32LE(2, 4);
  out.writeUInt32LE(total, 8);
  out.writeUInt32LE(jsonChunk.length, 12);
  out.writeUInt32LE(0x4e4f534a, 16);
  jsonChunk.copy(out, 20);
  if (binChunk) {
    const at = 20 + jsonChunk.length;
    out.writeUInt32LE(binChunk.length, at);
    out.writeUInt32LE(0x004e4942, at + 4);
    binChunk.copy(out, at + 8);
  }
  return out;
}

// ------------------------------------------------------------- geometry

// World-space AABB of the scene, walked through the node hierarchy so a model
// that parks its geometry under transformed nodes still measures correctly.
function bounds(json) {
  const lo = [Infinity, Infinity, Infinity];
  const hi = [-Infinity, -Infinity, -Infinity];
  const mul = (a, b) => {
    const m = new Array(16).fill(0);
    for (let i = 0; i < 4; i++)
      for (let j = 0; j < 4; j++) for (let k = 0; k < 4; k++) m[i * 4 + j] += a[i * 4 + k] * b[k * 4 + j];
    return m;
  };
  const local = (node) => {
    if (node.matrix) {
      const m = node.matrix; // glTF stores column-major
      return [m[0], m[4], m[8], m[12], m[1], m[5], m[9], m[13], m[2], m[6], m[10], m[14], m[3], m[7], m[11], m[15]];
    }
    const [tx, ty, tz] = node.translation || [0, 0, 0];
    const [x, y, z, w] = node.rotation || [0, 0, 0, 1];
    const [sx, sy, sz] = node.scale || [1, 1, 1];
    const R = [
      1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w), 0,
      2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w), 0,
      2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y), 0,
      0, 0, 0, 1,
    ];
    const S = [sx, 0, 0, 0, 0, sy, 0, 0, 0, 0, sz, 0, 0, 0, 0, 1];
    const T = [1, 0, 0, tx, 0, 1, 0, ty, 0, 0, 1, tz, 0, 0, 0, 1];
    return mul(T, mul(R, S));
  };
  const walk = (index, parent) => {
    const node = json.nodes[index];
    const M = mul(parent, local(node));
    if (node.mesh !== undefined) {
      for (const prim of json.meshes[node.mesh].primitives) {
        const acc = json.accessors[prim.attributes.POSITION];
        if (!acc?.min || !acc?.max) continue;
        for (const cx of [acc.min[0], acc.max[0]])
          for (const cy of [acc.min[1], acc.max[1]])
            for (const cz of [acc.min[2], acc.max[2]]) {
              const p = [
                M[0] * cx + M[1] * cy + M[2] * cz + M[3],
                M[4] * cx + M[5] * cy + M[6] * cz + M[7],
                M[8] * cx + M[9] * cy + M[10] * cz + M[11],
              ];
              for (let i = 0; i < 3; i++) {
                lo[i] = Math.min(lo[i], p[i]);
                hi[i] = Math.max(hi[i], p[i]);
              }
            }
      }
    }
    for (const child of node.children || []) walk(child, M);
  };
  const identity = [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1];
  for (const root of json.scenes[json.scene ?? 0].nodes) walk(root, identity);
  return { lo, hi };
}

// ------------------------------------------------------------------ run

const { json, bin } = readGlb(readFileSync(inPath));
const before = bounds(json);
const spanBefore = before.hi.map((v, i) => v - before.lo[i]);

for (const material of json.materials || []) material.name = toyName(material.name);

// Wrap the whole scene in one node that carries the correction, rather than
// rewriting every root: +90 deg about Y sends +X to -Z, which also sends the
// port wing (+Z, the red light) to +X — port stays port.
const scene = json.scenes[json.scene ?? 0];
const HALF = Math.SQRT1_2;
const centreX = (before.lo[0] + before.hi[0]) / 2;
const centreZ = (before.lo[2] + before.hi[2]) / 2;
json.nodes.push({
  name: 'Toy_Conform',
  children: [...scene.nodes],
  rotation: [0, HALF, 0, HALF],
  // Recentre, expressed in POST-rotation axes: the +90 deg turn sends the old
  // centre (cx, cz) to (cz, -cx), so undoing it is (-cz, +cx). Getting this
  // sign wrong offsets the model instead of centring it.
  translation: [-centreZ, 0, centreX],
});
scene.nodes = [json.nodes.length - 1];

const after = bounds(json);
const spanAfter = after.hi.map((v, i) => v - after.lo[i]);
writeFileSync(outPath, writeGlb(json, bin));

const f = (n) => n.toFixed(2).padStart(7);
console.log(`in  span  X${f(spanBefore[0])} Y${f(spanBefore[1])} Z${f(spanBefore[2])}`);
console.log(`out span  X${f(spanAfter[0])} Y${f(spanAfter[1])} Z${f(spanAfter[2])}`);
console.log(`out centre X${f((after.lo[0] + after.hi[0]) / 2)} Z${f((after.lo[2] + after.hi[2]) / 2)}`);
console.log(`length ${spanAfter[2].toFixed(2)} m along Z, span ${spanAfter[0].toFixed(2)} m along X`);
console.log('materials:', (json.materials || []).map((m) => m.name).join(', '));
