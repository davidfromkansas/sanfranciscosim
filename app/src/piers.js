// Concrete columns under every elevated freeway section. The pipeline samples
// them along the viaducts (out/piers.json -> manifest.piers) as
// [x, z, groundY, deckY]; here they become one instanced box mesh, so the whole
// city's viaduct support structure costs a single draw call.

import { BoxGeometry, InstancedMesh, Matrix4, MeshLambertMaterial } from 'three';

const COLUMN = 2.4;

export function createPiers(scene, data) {
  const piers = data.manifest.piers || [];
  if (!piers.length) return { count: 0, mesh: null };

  const geometry = new BoxGeometry(COLUMN, 1, COLUMN);
  const mesh = new InstancedMesh(geometry, new MeshLambertMaterial({ color: '#9d968a' }), piers.length);
  mesh.name = 'viaductPiers';
  mesh.castShadow = true;
  mesh.receiveShadow = true;

  const matrix = new Matrix4();
  for (let i = 0; i < piers.length; i++) {
    const [x, z, groundY, deckY] = piers[i];
    const height = Math.max(2, deckY - groundY);
    matrix.makeScale(1, height, 1);
    matrix.setPosition(x, groundY + height / 2, z);
    mesh.setMatrixAt(i, matrix);
  }
  mesh.instanceMatrix.needsUpdate = true;
  mesh.frustumCulled = false;
  scene.add(mesh);

  return { count: piers.length, mesh };
}
