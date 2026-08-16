// Every shipped GLB under sf-assets is meshopt-compressed on intake
// (pipeline/compress-assets.mjs), so every loader needs the decoder wired.
// three bundles it — no new dependency. Plain uncompressed GLBs still load
// through the same loader, so a raw drop-in during authoring keeps working.
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { MeshoptDecoder } from 'three/addons/libs/meshopt_decoder.module.js';

export function createGLTFLoader() {
  const loader = new GLTFLoader();
  loader.setMeshoptDecoder(MeshoptDecoder);
  return loader;
}
