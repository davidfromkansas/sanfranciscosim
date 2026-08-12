// One batch for the whole kit.
//
// Every kit instance in the city lives in a single `BatchedMesh`: one geometry
// per piece type, one draw call for all of them (two with the shadow pass), no
// matter how many chunks are streamed in. Instances are owned by the chunk that
// planned them and released when it unloads.

import { BatchedMesh, Color, Matrix4, Quaternion, Vector3, Vector4 } from 'three';
import { createKitMaterial } from './materials.js';
import { KIT_STRIDE, KIT_TINTS } from './kitplan.js';

// The densest 1 km chunk plans ~2.2k pieces and the near ring holds a couple of
// dozen chunks, so the batch is sized for the whole ring with room to spare.
const MAX_INSTANCES = 65536;
const VERTEX_SLACK = 1.15;

// `Toy_body` is authored mid-warm-grey, and the batch colour multiplies it, so
// a tint has to be divided by the body colour to land on the palette entry.
const BODY_BASE = new Color().setRGB(0.694, 0.659, 0.586);
const UP = new Vector3(0, 1, 0);

function tintVectors() {
  const out = [];
  for (const hex of KIT_TINTS) {
    const target = new Color(hex).convertSRGBToLinear();
    out.push(
      new Vector4(
        Math.min(2.5, target.r / BODY_BASE.r),
        Math.min(2.5, target.g / BODY_BASE.g),
        Math.min(2.5, target.b / BODY_BASE.b),
        1
      )
    );
  }
  return out;
}

export function createKitFleet(parent, catalog, loader) {
  const maxVertices = Math.ceil(catalog.pieces.reduce((sum, p) => sum + p.tris, 0) * 3 * VERTEX_SLACK);
  const material = createKitMaterial();
  // Merged pieces are non-indexed, so the batch never allocates an index buffer:
  // the vertex budget is the whole kit's triangle count with a little slack.
  const mesh = new BatchedMesh(MAX_INSTANCES, maxVertices, 0, material);
  mesh.name = 'kit';
  mesh.castShadow = true;
  mesh.receiveShadow = true;
  mesh.sortObjects = false;
  mesh.frustumCulled = false;
  mesh.visible = false;
  parent.add(mesh);

  const tints = tintVectors();
  const geometryIds = new Map(); // piece index -> batch geometry id
  const chunks = new Map(); // chunk key -> { ids, fade }
  const matrix = new Matrix4();
  const position = new Vector3();
  const quaternion = new Quaternion();
  const scale = new Vector3();
  const color = new Vector4();
  let live = 0;
  let triangles = 0;

  function geometryFor(index) {
    let id = geometryIds.get(index);
    if (id !== undefined) return id;
    const entry = loader.get(index);
    if (!entry || !entry.geometry) return undefined;
    id = mesh.addGeometry(entry.geometry);
    geometryIds.set(index, id);
    triangles += entry.triangles;
    // The batch now owns a copy; the loader's CPU-side arrays are dead weight.
    loader.release(index);
    return id;
  }

  function writeInstance(id, data, at, fade) {
    const index = data[at];
    const entry = loader.get(index);
    const yaw = data[at + 4];
    const depthScale = data[at + 5];
    // The piece is placed by its street-facing plane, so back it off along its
    // own forward axis by however far the model's front sits from its origin.
    const forwardX = Math.sin(yaw);
    const forwardZ = Math.cos(yaw);
    const back = entry.front * depthScale;
    position.set(data[at + 1] - forwardX * back, data[at + 2], data[at + 3] - forwardZ * back);
    quaternion.setFromAxisAngle(UP, yaw);
    // Width and height are never touched; only depth stretches, and only to the
    // planner's +20% ceiling.
    scale.set(1, 1, depthScale);
    mesh.setMatrixAt(id, matrix.compose(position, quaternion, scale));
    const tint = tints[data[at + 6]] || tints[0];
    mesh.setColorAt(id, color.set(tint.x, tint.y, tint.z, fade));
  }

  return {
    mesh,
    get count() {
      return live;
    },
    get pieceTypes() {
      return geometryIds.size;
    },
    get triangles() {
      return triangles;
    },
    /** Room for one more chunk's worth of instances? */
    canFit(instanceCount) {
      return live + instanceCount <= MAX_INSTANCES;
    },
    has(key) {
      return chunks.has(key);
    },
    /**
     * Adds one chunk's planned instances. Returns false when a piece failed to
     * load or the batch is full, and the caller re-runs the chunk procedurally.
     */
    add(key, data, fade = 1) {
      if (chunks.has(key)) return true;
      const count = data.length / KIT_STRIDE;
      if (!this.canFit(count)) return false;
      const ids = new Uint32Array(count);
      for (let i = 0; i < count; i++) {
        const at = i * KIT_STRIDE;
        const geometryId = geometryFor(data[at]);
        if (geometryId === undefined) {
          for (let k = 0; k < i; k++) mesh.deleteInstance(ids[k]);
          return false;
        }
        const id = mesh.addInstance(geometryId);
        ids[i] = id;
        writeInstance(id, data, at, fade);
      }
      chunks.set(key, { ids, fade });
      live += count;
      mesh.visible = live > 0;
      return true;
    },
    /** Drives the chunk's dither fade through the instance colour's alpha. */
    setFade(key, fade) {
      const chunk = chunks.get(key);
      if (!chunk || Math.abs(chunk.fade - fade) < 0.002) return;
      chunk.fade = fade;
      for (let i = 0; i < chunk.ids.length; i++) {
        mesh.getColorAt(chunk.ids[i], color);
        color.w = fade;
        mesh.setColorAt(chunk.ids[i], color);
      }
    },
    remove(key) {
      const chunk = chunks.get(key);
      if (!chunk) return false;
      for (const id of chunk.ids) mesh.deleteInstance(id);
      live -= chunk.ids.length;
      chunks.delete(key);
      mesh.visible = live > 0;
      return true;
    },
    clear() {
      for (const key of [...chunks.keys()]) this.remove(key);
    },
  };
}
