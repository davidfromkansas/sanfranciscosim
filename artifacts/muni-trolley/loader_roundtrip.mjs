// Gate G3, the half a Blender re-import cannot prove: the shipped GLB has to
// load through the app's OWN loader — `createGLTFLoader()` in app/src/gltf.js,
// i.e. three's GLTFLoader with the meshopt decoder wired — and survive
// `mergeVehicle()`'s merge path in app/src/agents.js.
//
//   node loader_roundtrip.mjs muni-trolley-40.glb [more.glb ...]
//
// Run from artifacts/muni-trolley/ with `npm install` done in app/ (three is a
// dependency there already; nothing new is added).
//
// What this catches that Blender does not: `mergeVehicle()` FLIPS any primitive
// whose signed volume is negative. A pole that shipped with inverted winding
// would re-import in Blender without complaint and then be silently reversed at
// runtime. Thin swept cylinders are the likeliest object in this asset to have
// that problem, so the signed volume is recomputed here through three's own
// attribute arrays rather than trusted from the Blender side.

import { promises as fs } from 'node:fs';
import { createRequire } from 'node:module';
import path from 'node:path';

const require = createRequire(path.join(process.cwd(), '../../app/'));
const THREE = require('three');
const { GLTFLoader } = require('three/examples/jsm/loaders/GLTFLoader.js');
const { MeshoptDecoder } = require('three/examples/jsm/libs/meshopt_decoder.module.js');

function signedVolume(geometry) {
  const pos = geometry.attributes.position;
  const index = geometry.index;
  const a = new THREE.Vector3();
  const b = new THREE.Vector3();
  const c = new THREE.Vector3();
  let total = 0;
  const n = index ? index.count : pos.count;
  for (let i = 0; i < n; i += 3) {
    const [i0, i1, i2] = index
      ? [index.getX(i), index.getX(i + 1), index.getX(i + 2)]
      : [i, i + 1, i + 2];
    a.fromBufferAttribute(pos, i0);
    b.fromBufferAttribute(pos, i1);
    c.fromBufferAttribute(pos, i2);
    total += a.dot(b.clone().cross(c)) / 6;
  }
  return total;
}

const loader = new GLTFLoader();
loader.setMeshoptDecoder(MeshoptDecoder);

let allPass = true;
for (const file of process.argv.slice(2)) {
  const buf = await fs.readFile(file);
  const gltf = await loader.parseAsync(
    buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength),
    ''
  );
  gltf.scene.updateMatrixWorld(true);

  const parts = [];
  const negatives = [];
  const box = new THREE.Box3();
  gltf.scene.traverse((o) => {
    if (!o.isMesh) return;
    const g = o.geometry.clone();
    g.applyMatrix4(o.matrixWorld);
    const v = signedVolume(g);
    if (v < 0) negatives.push(o.material?.name ?? o.name);
    parts.push({ name: o.material?.name ?? o.name, tris: (g.index ?? g.attributes.position).count / 3, volume: v });
    box.expandByObject(new THREE.Mesh(g));
  });

  const size = new THREE.Vector3();
  const centre = new THREE.Vector3();
  box.getSize(size);
  box.getCenter(centre);
  const tris = parts.reduce((s, p) => s + p.tris, 0);
  const ok = parts.length > 0 && negatives.length === 0 && Math.abs(box.min.y) < 0.05;
  allPass &&= ok;

  console.log(`\n=== ${path.basename(file)}  ${ok ? 'PASS' : 'FAIL'}`);
  console.log(`  meshes ${parts.length}  triangles ${tris}`);
  console.log(`  dims   ${[size.x, size.y, size.z].map((v) => v.toFixed(4)).join(' x ')}`);
  console.log(`  minY   ${box.min.y.toFixed(4)}`);
  console.log(`  centre X/Z ${centre.x.toFixed(4)} / ${centre.z.toFixed(4)}`);
  console.log(`  primitives with negative signed volume (mergeVehicle would flip these): ` +
    (negatives.length ? negatives.join(', ') : 'none'));
}

process.exit(allPass ? 0 : 1);
