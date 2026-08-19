// Conform the authored Muni LRV4 GLB to the vehicle contract (AGENTS.md).
//
//   node tools/conform-lrv-glb.mjs <in.glb> <out.glb> [--keep-interior]
//
// Sibling of tools/conform-aircraft-glb.mjs, same reasoning: the source is a
// photoreal Siemens S200 authored nose-along-+X with descriptive PBR material
// names, and app/src/muni.js draws live vehicles through an instanced loader
// that assumes front = -Z, min y = 0, and the `*_Glow` suffix for surfaces the
// night system ignites. Translate the dialect ONCE at intake.
//
// What it does:
//   1. Rotates the scene so the A-end cab points -Z (vehicles_manifest `front`).
//   2. Recentres X/Z and drops min y onto 0 — the wheel contact patch is the
//      street, there are no rails in this scene.
//   3. Renames materials `Toy_*`, suffixing `_Glow` on the lit surfaces so
//      mergeBus() splits them into the night layer instead of flattening them.
//   4. Drops the cabin interior (unless --keep-interior). mergeBus() bakes every
//      material into ONE opaque vertex-coloured geometry, so the BLEND glazing
//      merges opaque and nothing behind it can ever be seen: the seats, poles,
//      floor and lining are 17,032 triangles that render nothing. Materials left
//      unreferenced by the strip are pruned so the material list stays honest
//      (pipeline/compress-assets.mjs refuses output whose names changed).
//
// Feed it the PLAIN export, not sf_muni_lrv4_meshopt.glb: that one carries
// KHR_mesh_quantization, and mergeBus() bakes world matrices straight into the
// position arrays, which int16 attributes corrupt. Compression is the repo's
// job — run pipeline/compress-assets.mjs after this.
//
// Geometry is untouched; the binary chunk is copied through byte for byte.

import { readFileSync, writeFileSync } from 'node:fs';

const args = process.argv.slice(2);
const keepInterior = args.includes('--keep-interior');
const [inPath, outPath] = args.filter((a) => !a.startsWith('--'));
if (!inPath || !outPath) {
  console.error('usage: node tools/conform-lrv-glb.mjs <in.glb> <out.glb> [--keep-interior]');
  process.exit(1);
}

// Surfaces that are LIGHTS rather than paint — the set the night layer ignites.
const GLOW = new Set(['led_white', 'led_red', 'led_amber', 'cab_light', 'route_green']);

// Cabin interior: invisible once the glazing merges opaque.
const INTERIOR = new Set(['int_dark', 'int_floor', 'seat', 'pole']);

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

// World-space AABB and drawn-triangle count, walked through the node hierarchy.
function survey(json) {
  const lo = [Infinity, Infinity, Infinity];
  const hi = [-Infinity, -Infinity, -Infinity];
  let tris = 0;
  const walk = (index, parent) => {
    const node = json.nodes[index];
    const M = mul(parent, local(node));
    if (node.mesh !== undefined) {
      for (const prim of json.meshes[node.mesh].primitives) {
        const count = prim.indices !== undefined
          ? json.accessors[prim.indices].count
          : json.accessors[prim.attributes.POSITION].count;
        tris += count / 3;
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
  return { lo, hi, tris };
}

// ------------------------------------------------------------------ run

const { json, bin } = readGlb(readFileSync(inPath));
if ((json.extensionsRequired || []).includes('KHR_mesh_quantization'))
  throw new Error('input is quantized — mergeBus() bakes matrices into positions; feed the plain export');

const before = survey(json);

// 1. Strip the cabin interior, then prune materials the strip orphaned.
let stripped = 0;
if (!keepInterior) {
  for (const mesh of json.meshes) {
    mesh.primitives = mesh.primitives.filter((prim) => {
      if (!INTERIOR.has(json.materials[prim.material]?.name)) return true;
      const count = prim.indices !== undefined
        ? json.accessors[prim.indices].count
        : json.accessors[prim.attributes.POSITION].count;
      stripped += count / 3;
      return false;
    });
  }
  const used = new Set();
  for (const mesh of json.meshes) for (const prim of mesh.primitives) used.add(prim.material);
  const remap = new Map();
  json.materials = json.materials.filter((_, index) => {
    if (!used.has(index)) return false;
    remap.set(index, remap.size);
    return true;
  });
  for (const mesh of json.meshes) for (const prim of mesh.primitives) prim.material = remap.get(prim.material);
}

// 2. Material dialect.
for (const material of json.materials) material.name = toyName(material.name);

// 3. One wrapper node carries the correction rather than rewriting every root:
// +90 deg about Y sends +X to -Z, putting the A-end cab (2002A) at the front.
const scene = json.scenes[json.scene ?? 0];
const HALF = Math.SQRT1_2;
const centreX = (before.lo[0] + before.hi[0]) / 2;
const centreZ = (before.lo[2] + before.hi[2]) / 2;
json.nodes.push({
  name: 'Toy_Conform',
  children: [...scene.nodes],
  rotation: [0, HALF, 0, HALF],
  // Expressed in POST-rotation axes: the turn sends the old centre (cx, cz) to
  // (cz, -cx), so undoing it is (-cz, +cx). Y drops the wheel flanges onto the
  // street (authored min y is -0.032, the flange below railhead).
  translation: [-centreZ, -before.lo[1], centreX],
});
scene.nodes = [json.nodes.length - 1];

const after = survey(json);
writeFileSync(outPath, writeGlb(json, bin));

const f = (n) => n.toFixed(3).padStart(8);
console.log(`in   tris ${before.tris}   span X${f(before.hi[0] - before.lo[0])} Y${f(before.hi[1] - before.lo[1])} Z${f(before.hi[2] - before.lo[2])}`);
console.log(`out  tris ${after.tris}   span X${f(after.hi[0] - after.lo[0])} Y${f(after.hi[1] - after.lo[1])} Z${f(after.hi[2] - after.lo[2])}`);
// Stored vs drawn: the B half re-uses the A half's mesh datablock, so one
// stripped primitive removes triangles from two nodes.
if (stripped) console.log(`stripped interior: ${stripped} stored tris, ${before.tris - after.tris} drawn`);
console.log(`out  min y ${f(after.lo[1])}   centre X${f((after.lo[0] + after.hi[0]) / 2)} Z${f((after.lo[2] + after.hi[2]) / 2)}`);
console.log(`length ${(after.hi[2] - after.lo[2]).toFixed(2)} m along Z (front -Z), width ${(after.hi[0] - after.lo[0]).toFixed(2)} m`);
console.log('materials:', json.materials.map((m) => m.name).join(', '));
