// Gate G3, the half a Blender re-import cannot prove: the shipped GLB has to
// load through the APP'S OWN loader with the meshopt decoder wired, and then
// survive `mergeVehicle()` in app/src/agents.js.
//
//   node loader_roundtrip.mjs [path/to/f-line-pcc.glb]
//
// mergeVehicle bakes each mesh's material colour into vertex colours and
// reverses any part whose signed volume is negative, so this script reproduces
// both: it reports the merged triangle count, the baked colour set, and - the
// thing that actually matters for this asset - which vertex colour `Toy_body`
// contributed, because that is the value kitfleet.js's per-instance tint
// multiplies. A Toy_body that arrives as anything other than #d8d3c8 means the
// liveries land on the wrong colours.

import { promises as fs } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

// Imported by path rather than by bare specifier: this script lives in
// artifacts/, and `three` is a dependency of app/. These two files ARE
// `three/addons/...` - the same modules app/src/gltf.js pulls in.
import { GLTFLoader } from '../../app/node_modules/three/examples/jsm/loaders/GLTFLoader.js';
import { MeshoptDecoder } from '../../app/node_modules/three/examples/jsm/libs/meshopt_decoder.module.js';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const file = process.argv[2] || path.join(HERE, 'f-line-pcc.glb');

const loader = new GLTFLoader();
loader.setMeshoptDecoder(MeshoptDecoder);

const buffer = await fs.readFile(file);
const gltf = await loader.parseAsync(
  buffer.buffer.slice(buffer.byteOffset, buffer.byteOffset + buffer.byteLength),
  ''
);

function signedVolume(geometry) {
  const p = geometry.attributes.position;
  const index = geometry.index;
  const count = index ? index.count : p.count;
  let v = 0;
  for (let t = 0; t < count; t += 3) {
    const a = index ? index.getX(t) : t;
    const b = index ? index.getX(t + 1) : t + 1;
    const c = index ? index.getX(t + 2) : t + 2;
    v +=
      (p.getX(a) * (p.getY(b) * p.getZ(c) - p.getZ(b) * p.getY(c)) -
        p.getY(a) * (p.getX(b) * p.getZ(c) - p.getZ(b) * p.getX(c)) +
        p.getZ(a) * (p.getX(b) * p.getY(c) - p.getY(b) * p.getX(c))) /
      6;
  }
  return v;
}

const toHex = (c) => {
  const s = (v) =>
    Math.round(255 * (v <= 0.0031308 ? 12.92 * v : 1.055 * v ** (1 / 2.4) - 0.055));
  return '#' + [s(c.r), s(c.g), s(c.b)].map((x) => x.toString(16).padStart(2, '0')).join('');
};

gltf.scene.updateMatrixWorld(true);
const parts = [];
let tris = 0;
let negative = 0;
const box = { min: [Infinity, Infinity, Infinity], max: [-Infinity, -Infinity, -Infinity] };

gltf.scene.traverse((o) => {
  if (!o.isMesh) return;
  const g = o.geometry.clone();
  g.applyMatrix4(o.matrixWorld);
  const n = g.index ? g.index.count / 3 : g.attributes.position.count / 3;
  tris += n;
  if (signedVolume(g) < 0) negative++;
  const p = g.attributes.position;
  for (let i = 0; i < p.count; i++) {
    box.min[0] = Math.min(box.min[0], p.getX(i));
    box.min[1] = Math.min(box.min[1], p.getY(i));
    box.min[2] = Math.min(box.min[2], p.getZ(i));
    box.max[0] = Math.max(box.max[0], p.getX(i));
    box.max[1] = Math.max(box.max[1], p.getY(i));
    box.max[2] = Math.max(box.max[2], p.getZ(i));
  }
  const mats = Array.isArray(o.material) ? o.material : [o.material];
  for (const m of mats) parts.push({ name: m.name, hex: toHex(m.color), tris: n });
});

const byMaterial = {};
for (const p of parts) {
  byMaterial[p.name] = byMaterial[p.name] || { hex: p.hex, meshes: 0 };
  byMaterial[p.name].meshes++;
}

const round = (v) => Number(v.toFixed(4));
const result = {
  file: path.basename(file),
  loader: 'app/src/gltf.js createGLTFLoader() (GLTFLoader + MeshoptDecoder)',
  meshopt_extension: (gltf.parser.json.extensionsUsed || []).includes('EXT_meshopt_compression'),
  meshes: parts.length,
  triangles: tris,
  bbox_min: box.min.map(round),
  bbox_max: box.max.map(round),
  dimensions: box.max.map((v, i) => round(v - box.min[i])),
  min_y: round(box.min[1]),
  xz_center: [round((box.min[0] + box.max[0]) / 2), round((box.min[2] + box.max[2]) / 2)],
  negative_volume_meshes_mergeVehicle_would_reverse: negative,
  baked_vertex_colours_by_material: byMaterial,
  toy_body_present: 'Toy_body' in byMaterial,
  toy_body_baked_hex: byMaterial.Toy_body?.hex ?? null,
  toy_body_expected_hex: '#d8d3c8',
};
result.pass =
  result.meshopt_extension &&
  result.toy_body_present &&
  result.toy_body_baked_hex === result.toy_body_expected_hex &&
  Math.abs(result.min_y) < 0.001;

const out = process.argv[3] || path.join(HERE, 'loader-roundtrip.json');
await fs.writeFile(out, JSON.stringify(result, null, 2) + '\n');
console.log(JSON.stringify(result, null, 2));
if (!result.pass) process.exit(1);
