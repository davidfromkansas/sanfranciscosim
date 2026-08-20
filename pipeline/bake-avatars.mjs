// Bake the voxel resident rig from sf-avatar-studio into the one small file the
// city needs at runtime.
//
// The studio ships 42 glTF parts across five slots. Every primitive in every
// one of them is a 24-vertex axis-aligned box — 218 of 218, checked — so none
// of that glTF needs to reach the browser. What the diorama actually needs is
// the box list and the palette, which is a couple of kilobytes of JSON instead
// of five file fetches and a parser.
//
// Boxes are grouped by the RIGID PART they belong to, because that is what
// makes a walk cycle possible without a skeleton: legs swing about the hip,
// arms about the shoulder, everything else rides the body. Nothing in the
// studio is rigged, so the animation is procedural and the grouping is the rig.
//
//   node pipeline/bake-avatars.mjs
//   node pipeline/bake-avatars.mjs --studio ~/some/other/checkout
//
// Output (committed): app/public/sf-people/avatar-rig.json

import { promises as fs } from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.resolve(HERE, '../app/public/sf-people/avatar-rig.json');

function arg(name, fallback) {
  const i = process.argv.indexOf(`--${name}`);
  return i !== -1 && process.argv[i + 1] ? process.argv[i + 1] : fallback;
}
const SRC = path.resolve(arg('studio', path.join(os.homedir(), 'sf-avatar-studio')));
const PARTS = path.join(SRC, 'public/resident-parts');

// The studio's parts face +X: every face part puts its eyes at x = +0.102. The
// city's headings are the usual atan2(dx, dz), which assumes a model facing
// +Z, so the whole rig is rotated a quarter turn here rather than every
// instance paying for a correction every frame.
// A QUARTER TURN THE OTHER WAY. x' = z, z' = -x is +90 degrees, which sends
// the studio's +X front round to -Z and had every resident walking backwards
// with the back of their head leading. -90 degrees is x' = -z, z' = x, which
// is the one that puts the face on +Z where the headings expect it.
const faceZ = ({ size, centre }) => ({
  size: [size[2], size[1], size[0]],
  centre: [-centre[2], centre[1], centre[0]],
});

async function readBoxes(file) {
  const gltf = JSON.parse(await fs.readFile(file, 'utf8'));
  const boxes = [];
  for (const mesh of gltf.meshes ?? []) {
    for (const prim of mesh.primitives ?? []) {
      const acc = gltf.accessors[prim.attributes.POSITION];
      if (acc.count !== 24) throw new Error(`${file}: primitive is not a box (${acc.count} verts)`);
      const [mnx, mny, mnz] = acc.min;
      const [mxx, mxy, mxz] = acc.max;
      boxes.push(faceZ({
        size: [mxx - mnx, mxy - mny, mxz - mnz].map((n) => +n.toFixed(4)),
        centre: [(mxx + mnx) / 2, (mxy + mny) / 2, (mxz + mnz) / 2].map((n) => +n.toFixed(4)),
      }));
    }
  }
  const m = gltf.materials?.[0]?.pbrMetallicRoughness?.baseColorFactor ?? [1, 1, 1, 1];
  const hex = '#' + m.slice(0, 3).map((c) => {
    // glTF base colours are linear; the palette is read as sRGB in the browser.
    const s = c <= 0.0031308 ? c * 12.92 : 1.055 * Math.pow(c, 1 / 2.4) - 0.055;
    return Math.round(Math.max(0, Math.min(1, s)) * 255).toString(16).padStart(2, '0');
  }).join('');
  return { boxes, hex };
}

// The whole city wears one shape per slot and varies by colour, so these are
// not defaults — they are what every resident looks like, and picking them
// alphabetically put the entire population in a bob and a cheerful face.
// Chosen for neutrality: a silhouette that reads as "a person" at diorama
// scale rather than as a specific someone.
//
// Skin is exempt: all eight tones are the SAME mesh, checked, so its colour
// variation costs nothing and the file named here only supplies geometry.
const SHAPE = {
  skin: 'medium-brown.gltf',
  hair: 'short-waves.gltf',
  shirts: 'black-tee.gltf',
  pants: 'blue-jeans.gltf',
  faces: 'neutral.gltf',
};

async function slot(name) {
  const dir = path.join(PARTS, name);
  const files = (await fs.readdir(dir)).filter((f) => f.endsWith('.gltf')).sort();
  const pick = SHAPE[name];
  if (!files.includes(pick)) throw new Error(`${name}: ${pick} is gone from the studio`);
  const read = await Promise.all(files.map((f) => readBoxes(path.join(dir, f))));
  return { files, read, shape: read[files.indexOf(pick)].boxes, shapeName: pick };
}

// Which rigid group a box belongs to, from where it sits. Sides are read off
// the z sign because the parts are mirrored about the spine.
const LEG_TOP = 0.215;    // top of the thigh — the hip
const SHOULDER = 0.385;   // top of the sleeve — the shoulder
// Lateral axis is X, not Z. faceZ() above turned the whole rig a quarter turn
// so it faces +Z, which moved left-and-right onto X — classifying on Z after
// that rotation put the legs in the body group and found no arms at all.
const ARM_OUT = 0.13;     // arms sit at |x| 0.18, legs at 0.07
function groupFor(box) {
  const [x, y] = box.centre;
  // Arms first: a hand sits at y 0.205, below the hip line, and would otherwise
  // be read as a leg.
  if (Math.abs(x) > ARM_OUT) return x < 0 ? 'armL' : 'armR';
  if (y < LEG_TOP && Math.abs(x) > 0.03) return x < 0 ? 'legL' : 'legR';
  return 'body';
}

async function main() {
  const [skin, hair, shirts, pants, faces] = await Promise.all(
    ['skin', 'hair', 'shirts', 'pants', 'faces'].map(slot)
  );

  // One representative shape per slot; variation is colour only, which is what
  // keeps this to ten draw calls for the whole city. The palettes below carry
  // every colour the studio ships, so the crowd still reads as varied.
  const shape = {
    skin: skin.shape,
    hair: hair.shape,
    shirt: shirts.shape,
    pants: pants.shape,
    face: faces.shape,
  };

  // Clothing boxes are drawn slightly larger than the skin they cover — shirt
  // torso 0.205 against a 0.20 torso, pants thigh 0.165 against a 0.16 leg — so
  // the skin underneath is never visible and never worth drawing. Only the head,
  // neck and hands survive from the skin part.
  const covered = (b) => {
    const [x, y] = b.centre;
    if (Math.abs(x) > ARM_OUT) return y > 0.24;          // upper arm -> sleeve; the hand shows
    if (y < LEG_TOP && Math.abs(x) > 0.03) return true;  // leg -> trouser
    return y > 0.19 && y < 0.39;                         // torso -> shirt; head and neck show
  };
  shape.skin = shape.skin.filter((b) => !covered(b));

  const parts = [];
  for (const [role, boxes] of Object.entries(shape)) {
    const byGroup = {};
    for (const b of boxes) (byGroup[groupFor(b)] ??= []).push(b);
    for (const [group, list] of Object.entries(byGroup)) {
      parts.push({ id: `${role}-${group}`, role, group, boxes: list });
    }
  }

  const palette = {
    skin: skin.read.map((r) => r.hex),
    hair: hair.read.map((r) => r.hex),
    shirt: shirts.read.map((r) => r.hex),
    pants: pants.read.map((r) => r.hex),
    face: faces.read.map((r) => r.hex),
  };

  const height = Math.max(...Object.values(shape).flat().map((b) => b.centre[1] + b.size[1] / 2));
  const rig = {
    source: 'sf-avatar-studio',
    license: 'CC0-1.0',
    // Pivots the app rotates about. Without a skeleton these two numbers ARE
    // the rig: legs hinge at the hip, arms at the shoulder, in counterphase.
    pivots: { leg: LEG_TOP, arm: SHOULDER },
    modelHeight: +height.toFixed(4),
    parts,
    palette,
  };
  await fs.mkdir(path.dirname(OUT), { recursive: true });
  await fs.writeFile(OUT, JSON.stringify(rig, null, 1));
  const boxes = parts.reduce((n, p) => n + p.boxes.length, 0);
  console.log(`${parts.length} instanced parts · ${boxes} boxes per resident · model height ${rig.modelHeight}`);
  for (const p of parts) console.log(`   ${p.id.padEnd(12)} ${p.boxes.length} box(es)`);
  console.log('shape:', [skin, hair, shirts, pants, faces].map((s) => s.shapeName.replace('.gltf', '')).join(' · '));
  console.log('palette:', Object.entries(palette).map(([k, v]) => `${k} ${v.length}`).join(' · '));
  console.log(`avatar-rig.json ${(JSON.stringify(rig).length / 1024).toFixed(1)} KB`);
}

main();
