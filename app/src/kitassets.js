// The building kit's asset side: the v2 index, and one merged geometry per
// piece.
//
// Each GLB is authored as hundreds of little objects with a handful of flat
// `Toy_*` materials. This module flattens a piece into a single non-indexed
// buffer whose vertices carry the material colour plus one `aKit` channel that
// says what the vertex is: fixed palette, tintable `Toy_body`, or glass. That
// channel is what lets the whole kit render out of one batched buffer while
// only the body takes the per-lot tint and only the glass lights up at night.
//
// A piece that is missing or breaks the contract resolves to null: the planner
// drops it and the lot goes back to the procedural mass with one warning.

import { BufferAttribute, Vector3 } from 'three';
import { createGLTFLoader } from './gltf.js';
import { mergeGeometries } from 'three/addons/utils/BufferGeometryUtils.js';
import { createKitCatalog } from './kitplan.js';

const KIT_DIR = `${import.meta.env.BASE_URL}sf-assets/kit/`;

export const KIT_FIXED = 0;
export const KIT_BODY = 1;
export const KIT_GLASS = 2;

const CHANNEL = { Toy_body: KIT_BODY, Toy_glass: KIT_GLASS, Toy_glassl: KIT_GLASS };

export async function loadKitIndex() {
  const res = await fetch(`${KIT_DIR}kit_index.json`);
  if (!res.ok) throw new Error(`kit_index.json: ${res.status}`);
  const index = await res.json();
  if (!index || !Array.isArray(index.pieces)) throw new Error('kit_index.json: no pieces');
  return createKitCatalog(index);
}

function mergePiece(root) {
  const parts = [];
  let objects = 0;
  root.updateMatrixWorld(true);
  root.traverse((object) => {
    if (!object.isMesh) return;
    objects++;
    const material = object.material;
    if (!material?.name?.startsWith('Toy_')) throw new Error(`material "${material?.name}" is not Toy_*`);
    if (material.transparent || material.map) throw new Error(`material "${material.name}" is textured or transparent`);

    const geometry = object.geometry.clone().applyMatrix4(object.matrixWorld).toNonIndexed();
    geometry.deleteAttribute('uv');
    geometry.deleteAttribute('uv1');
    geometry.deleteAttribute('tangent');
    if (!geometry.attributes.normal) geometry.computeVertexNormals();

    const count = geometry.attributes.position.count;
    const colors = new Float32Array(count * 3);
    const channel = new Float32Array(count);
    const kind = CHANNEL[material.name] ?? KIT_FIXED;
    for (let i = 0; i < count; i++) {
      colors[i * 3] = material.color.r;
      colors[i * 3 + 1] = material.color.g;
      colors[i * 3 + 2] = material.color.b;
      channel[i] = kind;
    }
    geometry.setAttribute('color', new BufferAttribute(colors, 3));
    geometry.setAttribute('aKit', new BufferAttribute(channel, 1));
    parts.push(geometry);
  });

  const merged = mergeGeometries(parts, false);
  for (const part of parts) part.dispose();
  if (!merged) throw new Error('nothing to merge');
  merged.computeBoundingBox();
  return { geometry: merged, objects };
}

/**
 * Lazily loads and merges kit pieces. Only the piece types a streamed tile
 * actually asks for are ever fetched.
 */
export function createKitLoader(catalog, { onWarn = console.warn } = {}) {
  const loader = createGLTFLoader();
  const pending = new Map();
  const ready = new Map();
  const failed = new Set();

  async function load(piece) {
    const res = await fetch(KIT_DIR + piece.file);
    if (!res.ok) throw new Error(`${piece.file}: ${res.status}`);
    const gltf = await loader.parseAsync(await res.arrayBuffer(), KIT_DIR);
    const { geometry, objects } = mergePiece(gltf.scene);

    // The index's dims are what the planner fitted the lot against, so a model
    // that disagrees with them would place wrong: reject it to the fallback.
    const size = geometry.boundingBox.getSize(new Vector3());
    const claimed = [piece.dx, piece.dy, piece.dz];
    const actual = [size.x, size.z, size.y];
    for (let i = 0; i < 3; i++) {
      if (Math.abs(claimed[i] - actual[i]) > 0.3) {
        throw new Error(
          `dims disagree with the model: index ${claimed.map((v) => v.toFixed(2))} vs ${actual.map((v) => v.toFixed(2))}`
        );
      }
    }
    return {
      piece,
      geometry,
      objects,
      // Local Z of the street-facing face; the piece is placed by this plane,
      // not by its origin, because bays and awnings push the front out.
      front: geometry.boundingBox.max.z,
      triangles: geometry.attributes.position.count / 3,
    };
  }

  return {
    get(index) {
      return ready.get(index) || null;
    },
    failed(index) {
      return failed.has(index);
    },
    /** Resolves once every requested piece is merged (or known broken). */
    async ensure(indices) {
      const jobs = [];
      for (const index of indices) {
        if (ready.has(index) || failed.has(index)) continue;
        let job = pending.get(index);
        if (!job) {
          const piece = catalog.pieces[index];
          job = load(piece)
            .then((entry) => {
              ready.set(index, entry);
              pending.delete(index);
            })
            .catch((error) => {
              failed.add(index);
              pending.delete(index);
              onWarn(`kit piece "${piece.id}" unusable, falling back to procedural: ${error.message}`);
            });
          pending.set(index, job);
        }
        jobs.push(job);
      }
      if (jobs.length) await Promise.all(jobs);
      return indices.filter((index) => failed.has(index));
    },
  };
}
