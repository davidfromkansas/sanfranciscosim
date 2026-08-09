// Hand-made landmark assets. A manifest lists GLBs; each one is loaded after
// the first paint, merged down to at most two draw calls (opaque body + night
// glow) and placed on the real geodata the pipeline already baked.
//
// The asset contract the authoring side guarantees, and this loader relies on:
// real metres, origin at base-centre, flat-colour materials named `Toy_*`, no
// textures, no transparency, and `_Glow` on anything that lights up at night.
// Everything else — hundreds of objects, several materials — is this module's
// problem, not the renderer's.
//
// If an asset is missing or breaks the contract, one warning is logged and the
// code-built landmark stays exactly as it was.

import {
  Box3,
  BufferAttribute,
  Group,
  Mesh,
  MeshBasicMaterial,
  MeshLambertMaterial,
  Vector3,
} from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { mergeGeometries } from 'three/addons/utils/BufferGeometryUtils.js';
import { updateLandmarkGlow } from './kit.js';

const ASSETS = `${import.meta.env.BASE_URL}sf-assets/`;
const GLOW_SUFFIX = '_Glow';

// kebab-case asset ids to the camelCase landmark ids the pipeline bakes.
function camelId(id) {
  return id.replace(/-([a-z])/g, (_, c) => c.toUpperCase());
}

// Every mesh in the default scene, flattened with its world matrix already
// applied, split by whether its material glows.
function collect(root) {
  const body = [];
  const glow = [];
  const materials = new Set();
  let objects = 0;
  let violation = null;

  root.updateMatrixWorld(true);
  root.traverse((object) => {
    if (!object.isMesh) return;
    objects++;
    const material = object.material;
    if (!material || !material.name || !material.name.startsWith('Toy_')) {
      violation = violation || `material "${material?.name || 'unnamed'}" is not a Toy_* flat colour`;
      return;
    }
    if (material.transparent || material.map) {
      violation = violation || `material "${material.name}" uses transparency or a texture`;
      return;
    }
    materials.add(material.name);

    const geometry = object.geometry.clone();
    geometry.applyMatrix4(object.matrixWorld);
    geometry.deleteAttribute('uv');
    geometry.deleteAttribute('uv1');
    geometry.deleteAttribute('tangent');
    if (!geometry.attributes.normal) geometry.computeVertexNormals();

    // The flat material colour becomes vertex colour, which is what lets every
    // object in the file collapse into one buffer under one material.
    const count = geometry.attributes.position.count;
    const colors = new Float32Array(count * 3);
    for (let i = 0; i < count; i++) {
      colors[i * 3] = material.color.r;
      colors[i * 3 + 1] = material.color.g;
      colors[i * 3 + 2] = material.color.b;
    }
    geometry.setAttribute('color', new BufferAttribute(colors, 3));

    (material.name.endsWith(GLOW_SUFFIX) ? glow : body).push(geometry);
  });

  return { body, glow, materials, objects, violation };
}

// One buffer per bucket: `body` shaded like every other landmark, `glow`
// registered with the dusk system so it ignites at night.
function build(parts) {
  const group = new Group();
  const bodyGeometry = mergeGeometries(parts.body, false);
  if (!bodyGeometry) return null;
  for (const g of parts.body) g.dispose();
  const bodyMesh = new Mesh(bodyGeometry, new MeshLambertMaterial({ vertexColors: true }));
  bodyMesh.castShadow = true;
  bodyMesh.receiveShadow = true;
  group.add(bodyMesh);

  if (parts.glow.length) {
    const glowGeometry = mergeGeometries(parts.glow, false);
    for (const g of parts.glow) g.dispose();
    const material = new MeshBasicMaterial({ vertexColors: true, transparent: true, opacity: 1 });
    const mesh = new Mesh(glowGeometry, material);
    mesh.userData.nightOnly = true;
    group.add(mesh);
    group.userData.glow = material;
  }
  return group;
}

// Bridges get their alignment from the OSM centreline the pipeline already
// baked: the span axis follows the real deck, and the two tower tops in the
// model are pinned to the two real tower positions.
function placeBridge(group, box, entry, spec, data) {
  const size = box.getSize(new Vector3());
  const uniform = entry.targetHeightM / size.y;

  const nodes = spec.nodes.map(([lon, lat, y]) => {
    const [x, z] = data.project(lon, lat);
    return new Vector3(x, y, z);
  });
  const lengths = [0];
  for (let i = 1; i < nodes.length; i++) {
    lengths.push(lengths[i - 1] + Math.hypot(nodes[i].x - nodes[i - 1].x, nodes[i].z - nodes[i - 1].z));
  }
  const total = lengths[lengths.length - 1];
  const pointAt = (target) => {
    for (let i = 1; i < nodes.length; i++) {
      if (lengths[i] < target) continue;
      const t = (target - lengths[i - 1]) / (lengths[i] - lengths[i - 1] || 1);
      return nodes[i - 1].clone().lerp(nodes[i], t);
    }
    return nodes[nodes.length - 1].clone();
  };

  // Tower tops in model space: the vertices within 2% of the model's ceiling.
  const position = group.children[0].geometry.attributes.position;
  const ceiling = box.max.y - size.y * 0.02;
  let towerMin = Infinity;
  let towerMax = -Infinity;
  for (let i = 0; i < position.count; i++) {
    if (position.getY(i) < ceiling) continue;
    towerMin = Math.min(towerMin, position.getX(i));
    towerMax = Math.max(towerMax, position.getX(i));
  }

  // The suspended span is the part of the centreline that is actually straight,
  // so its two towers define the alignment. The full polyline curves onto the
  // approach roads at both ends and would twist the model by a couple of
  // degrees. Fall back to the polyline chord if the bake has no towers.
  const towers = (spec.towers || []).map((t) => {
    const [x, z] = data.project(t[0], t[1]);
    return new Vector3(x, 0, z);
  });
  const head = nodes[0];
  const tail = nodes[nodes.length - 1];
  const usable = towers.length === 2 && towerMax - towerMin > 1;
  // `southEnd: "+X"` means the model's +X carries the San Francisco end, so the
  // axis runs from Marin toward San Francisco — the first baked node.
  if (usable && Math.hypot(towers[1].x - head.x, towers[1].z - head.z) < Math.hypot(towers[0].x - head.x, towers[0].z - head.z)) {
    towers.reverse();
  }
  const from = usable ? towers[1] : tail;
  const to = usable ? towers[0] : head;
  const len = Math.hypot(to.x - from.x, to.z - from.z) || 1;
  const dirX = (to.x - from.x) / len;
  const dirZ = (to.z - from.z) / len;
  const yaw = Math.atan2(-dirZ, dirX);

  // Non-uniform X is allowed for bridges alone: the span stretches so the two
  // model towers land exactly on the two OSM towers.
  const spanScale = usable ? len / (towerMax - towerMin) : uniform;
  const center = usable ? from.clone().lerp(to, 0.5) : pointAt(total / 2);
  const centerAlong = -((towerMin + towerMax) / 2) * spanScale;
  const originX = center.x + dirX * centerAlong;
  const originZ = center.z + dirZ * centerAlong;

  // The deck also has to carry past both shorelines; if the fitted span stops
  // short of dry land, stretch further along X only.
  const shoreline = (sign) => {
    for (let d = 0; d < total; d += 5) {
      if (data.sampleElevation(originX + dirX * sign * d, originZ + dirZ * sign * d) > 0.5) return d;
    }
    return 0;
  };
  const short = Math.max(
    shoreline(1) / Math.max(1, box.max.x * spanScale),
    shoreline(-1) / Math.max(1, -box.min.x * spanScale)
  );
  const finalSpan = short > 1 ? spanScale * short : spanScale;

  group.scale.set(finalSpan, uniform, uniform);
  group.rotation.y = yaw;
  // Water level, never terrain-sampled: this bridge crosses the strait.
  group.position.set(originX, 0, originZ);

  // Where the model's deck ends sit, so the approach ramps can start exactly
  // there instead of guessing.
  const deckTop = deckTopY(position, box) * uniform;
  const ends = [box.max.x, box.min.x].map((x) => {
    const d = x * finalSpan;
    return {
      x: originX + dirX * d,
      z: originZ + dirZ * d,
      y: deckTop,
      along: d,
      toward: d > 0 ? 'south' : 'north',
    };
  });

  const residual = usable
    ? [towerMin, towerMax]
        .map((x, i) => {
          const d = x * finalSpan;
          return Math.hypot(originX + dirX * d - towers[1 - i].x, originZ + dirZ * d - towers[1 - i].z);
        })
        .reduce((a, b) => Math.max(a, b), 0)
    : null;

  return {
    ends,
    log:
      `span x${finalSpan.toFixed(4)} (uniform x${uniform.toFixed(4)}), yaw ${((yaw * 180) / Math.PI).toFixed(2)}°, ` +
      `towers ${residual === null ? 'n/a' : `${residual.toFixed(2)} m`} off the OSM pair, ` +
      `tower top ${(box.max.y * uniform).toFixed(1)} m, deck top ${deckTop.toFixed(1)} m`,
  };
}

// Roadway height in model units: the deck is by far the widest horizontal slab
// below the towers, so the modal vertex height in that band is the surface the
// approach ramps have to meet.
function deckTopY(position, box) {
  const BUCKET = 0.5;
  const low = box.max.y * 0.1;
  const high = box.max.y * 0.45;
  const counts = new Map();
  const tops = new Map();
  for (let i = 0; i < position.count; i++) {
    const y = position.getY(i);
    if (y < low || y > high) continue;
    const key = Math.floor(y / BUCKET);
    counts.set(key, (counts.get(key) || 0) + 1);
    tops.set(key, Math.max(tops.get(key) ?? -Infinity, y));
  }
  let best = null;
  let bestCount = 0;
  for (const [key, count] of counts) {
    if (count > bestCount) {
      bestCount = count;
      best = key;
    }
  }
  return best === null ? box.max.y * 0.3 : tops.get(best);
}

// Anything that is not a bridge: anchor lon/lat, uniform scale to the target
// height, grounded on the baked terrain.
function placeGeneric(group, box, entry, data) {
  const size = box.getSize(new Vector3());
  const scale = entry.targetHeightM / size.y;
  const [x, z] = data.project(entry.anchor[0], entry.anchor[1]);
  group.scale.setScalar(scale);
  group.position.set(x, Math.max(0, data.sampleElevation(x, z)), z);
  return { ends: [], log: `uniform x${scale.toFixed(4)} at ${x.toFixed(0)}, ${z.toFixed(0)}` };
}

export function createAssets(scene, data, { onPlaced } = {}) {
  const group = new Group();
  group.name = 'landmark-assets';
  scene.add(group);
  const placed = new Map();
  let warned = false;

  const warn = (message) => {
    if (warned) return;
    warned = true;
    console.warn(`sf-assets: ${message} — keeping the code-built landmark`);
  };

  async function load() {
    let manifest;
    try {
      const res = await fetch(`${ASSETS}landmarks_manifest.json`);
      if (!res.ok) throw new Error(`manifest ${res.status}`);
      manifest = await res.json();
    } catch (error) {
      warn(`no landmark manifest (${error.message})`);
      return;
    }

    const loader = new GLTFLoader();
    for (const entry of manifest) {
      try {
        await place(loader, entry);
      } catch (error) {
        warn(`${entry.id} failed to load (${error.message})`);
      }
    }
  }

  async function place(loader, entry) {
    const gltf = await loader.loadAsync(`${ASSETS}landmarks/${entry.file}`);
    const parts = collect(gltf.scene);
    if (!parts.body.length) throw new Error(parts.violation || 'no Toy_* geometry in the file');
    if (parts.violation) throw new Error(parts.violation);

    const model = build(parts);
    if (!model) throw new Error('nothing to merge');
    model.name = entry.id;

    // Bounds are measured off the merged result, never read from the file.
    const box = new Box3().setFromObject(model);
    if (!Number.isFinite(box.max.y - box.min.y) || box.max.y - box.min.y < 1) {
      throw new Error('merged bounds have no usable height');
    }

    const landmarkId = camelId(entry.id);
    const spec = data.manifest.bridges?.[landmarkId];
    const placement = spec
      ? placeBridge(model, box, entry, spec, data)
      : placeGeneric(model, box, entry, data);

    group.add(model);
    placed.set(landmarkId, { entry, model, ...placement });
    onPlaced?.(landmarkId, placement);

    const draws = model.children.length;
    console.log(
      `sf-assets: ${entry.id} merged ${parts.objects} objects / ${parts.materials.size} materials -> ` +
        `${draws} draw call${draws === 1 ? '' : 's'} ` +
        `(${(model.children[0].geometry.attributes.position.count / 3).toFixed(0)} tris body` +
        `${model.children[1] ? `, ${(model.children[1].geometry.attributes.position.count / 3).toFixed(0)} tris glow` : ''}); ` +
        placement.log
    );
  }

  return {
    group,
    placed,
    load,
    update() {
      for (const object of group.children) updateLandmarkGlow(object);
    },
  };
}
