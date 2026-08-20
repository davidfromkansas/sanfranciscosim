// The ferry hull geometry, loaded and merged once and shared.
//
// Two layers draw boats — the live WETA fleet (ferries.js) and the timetable
// stand-ins for the operators with no live feed (ferryscheduled.js) — and both
// want the same model at the same scale. Loading it twice would mean a second
// merge and a second copy on the GPU for no benefit.
//
// Resolves to null on any failure, never throws: rule 3, a missing model costs
// the boats and nothing else.

import { createGLTFLoader } from './gltf.js';
import { mergeFerry } from './ferrymerge.js';

const ASSET = `${import.meta.env.BASE_URL}sf-assets/vehicles/SF_Bay_Ferry.glb`;
const MANIFEST = `${import.meta.env.BASE_URL}sf-assets/vehicles_manifest.json`;

let promise = null;

export function loadFerryHull() {
  if (promise) return promise;
  promise = (async () => {
    let entry = null;
    try {
      const res = await fetch(MANIFEST);
      if (res.ok) {
        entry = ((await res.json()).vehicles || []).find((v) => v.kind === 'ferry') || null;
      }
    } catch {
      entry = null;
    }

    let merged;
    try {
      const gltf = await createGLTFLoader().loadAsync(
        entry ? `${import.meta.env.BASE_URL}sf-assets/${entry.file}` : ASSET
      );
      merged = mergeFerry(gltf.scene);
    } catch (error) {
      console.warn(`sf-ferries: ferry model failed to load (${error.message})`);
      return null;
    }
    if (!merged.body) {
      console.warn('sf-ferries: ferry model had no geometry');
      return null;
    }

    // Never trust the file's own scale: measure and scale to the manifest length.
    merged.body.computeBoundingBox();
    const measured = merged.body.boundingBox.max.z - merged.body.boundingBox.min.z;
    const target = entry?.targetLengthM ?? entry?.dims?.[2] ?? measured;
    return { body: merged.body, glow: merged.glow, scale: measured > 0 ? target / measured : 1 };
  })();
  return promise;
}
