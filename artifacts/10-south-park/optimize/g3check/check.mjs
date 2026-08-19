// Gate G3: three.js GLTFLoader round-trip (node, three@0.185.1)
//   node check.mjs <file.glb> [--no-meshopt]
import { readFileSync, writeFileSync } from "node:fs";
import * as THREE from "three";
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader.js";
import { MeshoptDecoder } from "three/examples/jsm/libs/meshopt_decoder.module.js";

const file = process.argv[2];
const allowMeshopt = !process.argv.includes("--no-meshopt");
const buf = readFileSync(file);
const ab = buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength);

const loader = new GLTFLoader();
if (allowMeshopt) loader.setMeshoptDecoder(MeshoptDecoder);

loader.parse(ab, "", (gltf) => {
  const mats = new Set(), meshes = [];
  let tris = 0;
  gltf.scene.traverse((o) => {
    if (o.isMesh) {
      meshes.push(o.name);
      const m = Array.isArray(o.material) ? o.material : [o.material];
      m.forEach((x) => mats.add(x.name));
      const g = o.geometry;
      tris += (g.index ? g.index.count : g.attributes.position.count) / 3;
    }
  });
  const box = new THREE.Box3().setFromObject(gltf.scene);
  const size = new THREE.Vector3(); box.getSize(size);
  const out = {
    ok: true, meshes: meshes.length, tris,
    materials: [...mats].sort(),
    bbox_dims: [size.x, size.y, size.z].map((v) => +v.toFixed(4)),
    bbox_min: [box.min.x, box.min.y, box.min.z].map((v) => +v.toFixed(4)),
  };
  console.log("G3-OK", JSON.stringify(out));
  writeFileSync("g3.json", JSON.stringify(out, null, 1));
}, (err) => {
  console.error("G3-FAIL", err.message || err);
  writeFileSync("g3.json", JSON.stringify({ ok: false, error: String(err) }, null, 1));
  process.exit(1);
});
