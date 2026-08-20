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
  BatchedMesh,
  BufferAttribute,
  Group,
  Matrix4,
  Mesh,
  MeshBasicMaterial,
  MeshLambertMaterial,
  Quaternion,
  Vector3,
  Vector4,
} from 'three';
import { createGLTFLoader } from './gltf.js';
import { MeshoptDecoder } from 'three/addons/libs/meshopt_decoder.module.js';
import { mergeGeometries } from 'three/addons/utils/BufferGeometryUtils.js';
import { shared } from './env.js';
import { createBatchFadeLambert } from './materials.js';
import { updateLandmarkGlow } from './kit.js';

const ASSETS = `${import.meta.env.BASE_URL}sf-assets/`;
const GLOW_SUFFIX = '_Glow';

// kebab-case asset ids to the camelCase landmark ids the pipeline bakes.
function camelId(id) {
  return id.replace(/-([a-z])/g, (_, c) => c.toUpperCase());
}

function floatAttribute(attribute) {
  if (!attribute || attribute.array instanceof Float32Array) return attribute;
  const values = new Float32Array(attribute.count * attribute.itemSize);
  for (let i = 0; i < attribute.count; i++) {
    for (let j = 0; j < attribute.itemSize; j++) {
      values[i * attribute.itemSize + j] = attribute.getComponent(i, j);
    }
  }
  return new BufferAttribute(values, attribute.itemSize, false);
}

function prepareGeometryForTransforms(geometry) {
  for (const name of ['position', 'normal', 'tangent']) {
    const attribute = geometry.getAttribute(name);
    if (attribute && !(attribute.array instanceof Float32Array)) {
      geometry.setAttribute(name, floatAttribute(attribute));
    }
  }
  return geometry;
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
    prepareGeometryForTransforms(geometry);
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
function mergeParts(parts) {
  const bodyGeometry = mergeGeometries(parts.body, false);
  if (!bodyGeometry) return null;
  for (const g of parts.body) g.dispose();
  let glowGeometry = null;
  if (parts.glow.length) {
    glowGeometry = mergeGeometries(parts.glow, false);
    for (const g of parts.glow) g.dispose();
  }
  return { bodyGeometry, glowGeometry };
}

// Bridges keep their own meshes: non-uniform span scaling and the approach
// logic act on a Group, and they are always resident anyway.
function buildGroup(merged) {
  const group = new Group();
  const bodyMesh = new Mesh(merged.bodyGeometry, new MeshLambertMaterial({ vertexColors: true }));
  bodyMesh.castShadow = true;
  bodyMesh.receiveShadow = true;
  group.add(bodyMesh);

  if (merged.glowGeometry) {
    const material = new MeshBasicMaterial({ vertexColors: true, transparent: true, opacity: 1 });
    const mesh = new Mesh(merged.glowGeometry, material);
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
  // Arc length of the point on the centreline closest to a world position.
  const arcOf = (p) => {
    let best = Infinity;
    let arc = 0;
    for (let i = 1; i < nodes.length; i++) {
      const dx = nodes[i].x - nodes[i - 1].x;
      const dz = nodes[i].z - nodes[i - 1].z;
      const lengthSq = dx * dx + dz * dz || 1;
      const t = Math.min(1, Math.max(0, ((p.x - nodes[i - 1].x) * dx + (p.z - nodes[i - 1].z) * dz) / lengthSq));
      const distance = Math.hypot(nodes[i - 1].x + dx * t - p.x, nodes[i - 1].z + dz * t - p.z);
      if (distance < best) {
        best = distance;
        arc = lengths[i - 1] + Math.hypot(dx, dz) * t;
      }
    }
    return arc;
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

  // The model is centred on the real towers along the route, then both of its
  // deck ends are pinned onto the baked centreline itself. Aligning to the
  // towers alone leaves the ends metres off the road, because the centreline
  // curves where it runs onto the approach viaducts — and a road that does not
  // meet the deck is worse than a tower a few metres out.
  const towers = (spec.towers || []).map((t) => {
    const [x, z] = data.project(t[0], t[1]);
    return new Vector3(x, 0, z);
  });
  const usable = towers.length === 2 && towerMax - towerMin > 1;
  // Arc runs from the first baked node, which is the San Francisco end, so the
  // south tower is the one with the smaller arc.
  if (usable && arcOf(towers[0]) > arcOf(towers[1])) towers.reverse();
  const towerSpacing = usable ? Math.hypot(towers[0].x - towers[1].x, towers[0].z - towers[1].z) : 0;
  // `southEnd: "+X"` means the model's +X carries the San Francisco end, and
  // arc length is measured from the first baked node, which is that same end.
  const centerArc = usable ? (arcOf(towers[0]) + arcOf(towers[1])) / 2 : total / 2;
  const modelLength = box.max.x - box.min.x;
  const towerCenter = (towerMin + towerMax) / 2;

  // Non-uniform X is allowed for bridges alone. Start from the scale that would
  // put the two model towers on the two OSM towers, then settle on the scale at
  // which the deck ends land on the centreline: the chord they subtend is
  // slightly shorter than the arc between them.
  let span = usable ? towerSpacing / (towerMax - towerMin) : uniform;
  let south = pointAt(centerArc);
  let north = south;
  for (let pass = 0; pass < 6; pass++) {
    south = pointAt(centerArc - (box.max.x - towerCenter) * span);
    north = pointAt(centerArc + (towerCenter - box.min.x) * span);
    span = Math.hypot(south.x - north.x, south.z - north.z) / modelLength;
  }

  const chord = Math.hypot(south.x - north.x, south.z - north.z) || 1;
  const dirX = (south.x - north.x) / chord;
  const dirZ = (south.z - north.z) / chord;
  const yaw = Math.atan2(-dirZ, dirX);
  const originX = south.x - dirX * box.max.x * span;
  const originZ = south.z - dirZ * box.max.x * span;

  group.scale.set(span, uniform, uniform);
  group.rotation.y = yaw;
  // Water level, never terrain-sampled: this bridge crosses the strait.
  group.position.set(originX, 0, originZ);

  // Where the model's deck ends sit, so the approach ramps can start exactly
  // there instead of guessing.
  const deckTop = deckTopY(position, box) * uniform;
  const ends = [box.max.x, box.min.x].map((x) => {
    const d = x * span;
    return {
      x: originX + dirX * d,
      z: originZ + dirZ * d,
      y: deckTop,
      along: d,
      toward: d > 0 ? 'south' : 'north',
    };
  });

  const residual = usable
    ? Math.max(
        ...[towerMax, towerMin].map((x, i) => {
          const d = x * span;
          return Math.hypot(originX + dirX * d - towers[i].x, originZ + dirZ * d - towers[i].z);
        })
      )
    : null;

  return {
    ends,
    log:
      `span x${span.toFixed(4)} (uniform x${uniform.toFixed(4)}), yaw ${((yaw * 180) / Math.PI).toFixed(2)}°, ` +
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
// height, grounded on the baked terrain. Returned as a matrix so the batch can
// place an instance without a Group in the graph.
//
// `seaLevel: true` in the manifest seats the asset on the water plane instead —
// the same datum the bridges use. It exists for structures that STAND IN THE BAY,
// where the Terrarium DEM is not ground truth and sampling it is actively wrong:
// at 7.5 m per sample the raster carries spurious 2+ m bumps over open water
// (moored vessels and the pier decks themselves bleed into the source), so at
// Pier 3's anchor it returns 2.23 m while reading 0.00 m thirty metres either
// side. Seating on that lifts a 213 m pier two metres clear of the water with
// daylight under its piles. The alternative — sliding the anchor until the
// raster happens to read zero — is forbidden (INTEGRATION-PROMPT "Do not": move
// the real anchor to make the model fit) and would break again on the next
// terrain bake. Declaring the datum is the honest fix, and it is the same kind
// of per-asset, data-visible placement decision as `yawDeg` and `loadRadius`.
const UP = new Vector3(0, 1, 0);
function placeGeneric(box, entry, data) {
  const size = box.getSize(new Vector3());
  const scale = entry.targetHeightM / size.y;
  const [x, z] = data.project(entry.anchor[0], entry.anchor[1]);
  const y = entry.seaLevel ? 0 : Math.max(0, data.sampleElevation(x, z));
  const yaw = entry.yawDeg !== undefined ? (entry.yawDeg * Math.PI) / 180 : 0;
  const matrix = new Matrix4().compose(
    new Vector3(x, y, z),
    new Quaternion().setFromAxisAngle(UP, yaw),
    new Vector3(scale, scale, scale)
  );
  const datum = entry.seaLevel ? ' on the water plane' : '';
  return {
    matrix,
    ends: [],
    log: `uniform x${scale.toFixed(4)} at ${x.toFixed(0)}, ${z.toFixed(0)}${datum}`,
  };
}

// Streaming + batching (PERF-PLAN #3).
//
// Every generic landmark lives as one geometry + one instance in a shared
// BatchedMesh pair (opaque bodies, night glow): N landmarks cost 2 draw calls,
// not 2N. Bridges keep their own meshes — non-uniform span scaling and the
// approach-ramp logic act on a Group, and a bridge is the skyline, so it is
// always resident.
//
// A manifest entry may declare `loadRadius` (metres): the GLB is then fetched
// only when the camera comes within it, dither-faded in, and released again
// past 1.25x the radius — the code-built landmark (where one exists) returns
// as the far stand-in. Entries without `loadRadius`, or with
// `alwaysLoaded: true`, load at boot and never unload, exactly the old
// behaviour, so streaming is a per-asset decision made at integration time.
// The meshopt pass reindexes every GLB, so merged landmark geometry arrives
// indexed: the batch needs index space too (a zero maxIndexCount rejects the
// very first indexed addGeometry).
// Body reserve sized against the WHOLE manifest resident at once, not against
// the worst camera: streaming keeps the live set below that, but the ceiling
// then does not move when a batch lands in one district. An overflow is not a
// crash: the addGeometry throw drops that landmark to its procedural stand-in,
// so it reads as one arbitrary landmark quietly missing on each reload, and
// nothing in the standard gates catches it.
//   103 landmarks (before the Embarcadero batch)  1,434,764 body verts
//   131 landmarks (after it)                      2,072,002 body verts
// which is 129.5% of the previous 1,600,000 reserve, and its indices reached
// 94.7% of 3,600,000 — both had to move. Measured from GLB accessor counts,
// which survive meshopt: sum POSITION.count per primitive, split by material
// (/_Glow$/ -> glow batch, everything else -> body); mergeGeometries(.., false)
// concatenates without welding, so that sum is what addGeometry consumes.
//   2,400,000 verts x 36 B (position+normal+color) = 86 MB, up 28 MB.
// Post-batch occupancy, all-resident: body 86.3% verts / 65.6% indices,
// glow 44.9% verts / 23.3% indices — so the glow reserve is untouched.
const BODY_VERTS = 2_400_000;
const BODY_INDICES = 5_200_000;
const GLOW_VERTS = 250_000;
const GLOW_INDICES = 750_000;
const MAX_BATCHED = 512;
const EXIT_FACTOR = 1.25;
const SCAN_EVERY_S = 0.4;
const FADE_S = 0.35;

export function createAssets(scene, data, { onPlaced, onUnloaded } = {}) {
  const group = new Group();
  group.name = 'landmark-assets';
  scene.add(group);
  const placed = new Map();
  const states = new Map(); // entry.id -> lifecycle record
  let warned = false;
  let loader = null;
  let bodyBatch = null;
  let glowBatch = null;
  let glowMaterial = null;
  let scanCooldown = 0;
  const color = new Vector4();

  const warn = (message) => {
    if (warned) return;
    warned = true;
    console.warn(`sf-assets: ${message} — keeping the code-built landmark`);
  };

  function batches() {
    if (bodyBatch) return true;
    try {
      bodyBatch = new BatchedMesh(MAX_BATCHED, BODY_VERTS, BODY_INDICES, createBatchFadeLambert());
      bodyBatch.name = 'landmark-bodies';
      bodyBatch.castShadow = true;
      bodyBatch.receiveShadow = true;
      bodyBatch.sortObjects = false;
      // Same lesson kitfleet already carries: the batch's own bounds cover the
      // reserved (mostly empty) buffer, so whole-batch and per-instance frustum
      // tests cull landmarks that are plainly on screen. The batch spans the
      // whole city anyway — culling it is never a win at 2 draw calls.
      bodyBatch.frustumCulled = false;
      bodyBatch.perObjectFrustumCulled = false;
      glowMaterial = new MeshBasicMaterial({ vertexColors: true, transparent: true, opacity: 1 });
      glowBatch = new BatchedMesh(MAX_BATCHED, GLOW_VERTS, GLOW_INDICES, glowMaterial);
      glowBatch.name = 'landmark-glow';
      glowBatch.sortObjects = false;
      glowBatch.frustumCulled = false;
      glowBatch.perObjectFrustumCulled = false;
      group.add(bodyBatch, glowBatch);
      return true;
    } catch (error) {
      warn(`landmark batch unavailable (${error.message})`);
      bodyBatch = null;
      return false;
    }
  }

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

    loader = createGLTFLoader();
    loader.setMeshoptDecoder(MeshoptDecoder);
    for (const entry of manifest) {
      const landmarkId = camelId(entry.id);
      const bridge = Boolean(data.manifest.bridges?.[landmarkId]);
      const resident = bridge || entry.alwaysLoaded || !(entry.loadRadius > 0);
      const [x, z] = entry.anchor ? data.project(entry.anchor[0], entry.anchor[1]) : [0, 0];
      states.set(entry.id, {
        entry,
        landmarkId,
        bridge,
        resident,
        x,
        z,
        status: 'far', // far | loading | live | fading-in | fading-out
        wanted: resident,
        fade: 0,
        bodyGeomId: -1,
        glowGeomId: -1,
        bodyInstId: -1,
        glowInstId: -1,
      });
    }
    for (const state of states.values()) {
      if (!state.resident) continue;
      try {
        await place(state);
      } catch (error) {
        state.status = 'failed';
        warn(`${state.entry.id} failed to load (${error.message})`);
      }
    }
  }

  async function place(state) {
    const entry = state.entry;
    state.status = 'loading';
    const gltf = await loader.loadAsync(`${ASSETS}landmarks/${entry.file}`);
    const parts = collect(gltf.scene);
    if (!parts.body.length) {
      state.status = 'far';
      throw new Error(parts.violation || 'no Toy_* geometry in the file');
    }
    if (parts.violation) {
      state.status = 'far';
      throw new Error(parts.violation);
    }
    const merged = mergeParts(parts);
    if (!merged) {
      state.status = 'far';
      throw new Error('nothing to merge');
    }

    // Bounds are measured off the merged result, never read from the file.
    merged.bodyGeometry.computeBoundingBox();
    const box = merged.bodyGeometry.boundingBox.clone();
    if (merged.glowGeometry) {
      merged.glowGeometry.computeBoundingBox();
      box.union(merged.glowGeometry.boundingBox);
    }
    if (!Number.isFinite(box.max.y - box.min.y) || box.max.y - box.min.y < 1) {
      state.status = 'far';
      throw new Error('merged bounds have no usable height');
    }

    const tris = (merged.bodyGeometry.attributes.position.count / 3).toFixed(0);
    let placement;
    let draws;
    if (state.bridge) {
      const model = buildGroup(merged);
      model.name = entry.id;
      placement = placeBridge(model, box, entry, data.manifest.bridges[state.landmarkId], data);
      group.add(model);
      state.model = model;
      draws = `${model.children.length}`;
    } else if (batches()) {
      placement = placeGeneric(box, entry, data);
      state.bodyGeomId = bodyBatch.addGeometry(merged.bodyGeometry);
      state.bodyInstId = bodyBatch.addInstance(state.bodyGeomId);
      bodyBatch.setMatrixAt(state.bodyInstId, placement.matrix);
      if (merged.glowGeometry) {
        state.glowGeomId = glowBatch.addGeometry(merged.glowGeometry);
        state.glowInstId = glowBatch.addInstance(state.glowGeomId);
        glowBatch.setMatrixAt(state.glowInstId, placement.matrix);
      }
      // The geometry now lives in the batch's own buffers.
      merged.bodyGeometry.dispose();
      merged.glowGeometry?.dispose();
      state.fade = state.resident ? 1 : 0;
      setFade(state, state.fade);
      draws = 'batched';
    } else {
      // Batch allocation failed (tiny GL limits): per-landmark meshes, the
      // pre-streaming behaviour — and no lifecycle, so it can never be placed
      // twice.
      const model = buildGroup(merged);
      model.name = entry.id;
      const generic = placeGeneric(box, entry, data);
      model.applyMatrix4(generic.matrix);
      placement = generic;
      group.add(model);
      state.model = model;
      state.resident = true;
      draws = `${model.children.length}`;
    }

    state.status = state.resident || state.bridge || state.model ? 'live' : 'fading-in';
    if (!state.wanted && !state.resident) {
      // The camera left while the file was in flight.
      state.status = 'fading-out';
    }
    placed.set(state.landmarkId, { entry, ...placement });
    onPlaced?.(state.landmarkId, placement);

    console.log(
      `sf-assets: ${entry.id} merged ${parts.objects} objects / ${parts.materials.size} materials -> ` +
        `${draws} (${tris} tris body); ${placement.log}`
    );
  }

  function setFade(state, alpha) {
    if (state.bodyInstId >= 0) bodyBatch.setColorAt(state.bodyInstId, color.set(1, 1, 1, alpha));
    if (state.glowInstId >= 0) glowBatch.setColorAt(state.glowInstId, color.set(1, 1, 1, alpha));
  }

  function release(state) {
    if (state.bodyInstId >= 0) {
      bodyBatch.deleteInstance(state.bodyInstId);
      if (state.bodyGeomId >= 0) bodyBatch.deleteGeometry(state.bodyGeomId);
    }
    if (state.glowInstId >= 0) {
      glowBatch.deleteInstance(state.glowInstId);
      if (state.glowGeomId >= 0) glowBatch.deleteGeometry(state.glowGeomId);
    }
    state.bodyGeomId = state.glowGeomId = state.bodyInstId = state.glowInstId = -1;
    state.status = 'far';
    placed.delete(state.landmarkId);
    // deleteGeometry leaves a hole; without this the buffer only ever grows
    // and a session of streaming in and out eventually rejects every load.
    bodyBatch.optimize();
    glowBatch.optimize();
    onUnloaded?.(state.landmarkId);
  }

  function scan(cameraPos) {
    for (const state of states.values()) {
      if (state.resident || !loader) continue;
      const r = state.entry.loadRadius;
      const d = Math.hypot(cameraPos.x - state.x, cameraPos.z - state.z);
      if (state.status === 'far' && d < r) {
        state.wanted = true;
        place(state).catch((error) => {
          state.status = 'failed';
          // Not the single-shot warn: each streamed asset that fails is its
          // own finding, and the procedural stand-in covers the hole.
          console.warn(`sf-assets: ${state.entry.id} failed to load (${error.message})`);
        });
      } else if ((state.status === 'live' || state.status === 'fading-in') && d > r * EXIT_FACTOR) {
        state.wanted = false;
        state.status = 'fading-out';
      } else if (state.status === 'fading-out' && d < r) {
        // Came back before the fade finished.
        state.wanted = true;
        state.status = 'fading-in';
      } else if (state.status === 'loading') {
        state.wanted = d < r * EXIT_FACTOR;
      }
    }
  }

  return {
    group,
    placed,
    load,
    // For the harness and QA: how many entries sit in each lifecycle state.
    stats() {
      const out = { entries: states.size, far: 0, loading: 0, live: 0, fading: 0, failed: 0 };
      for (const s of states.values()) {
        if (s.status === 'far') out.far++;
        else if (s.status === 'loading') out.loading++;
        else if (s.status === 'live') out.live++;
        else if (s.status === 'failed') out.failed++;
        else out.fading++;
      }
      return out;
    },
    update(cameraPos, dt = 0) {
      for (const object of group.children) updateLandmarkGlow(object);
      if (glowMaterial) glowMaterial.opacity = Math.min(1, 0.12 + shared.uNight.value * 0.95);

      for (const state of states.values()) {
        if (state.status === 'fading-in') {
          state.fade = Math.min(1, state.fade + dt / FADE_S);
          setFade(state, state.fade);
          if (state.fade >= 1) state.status = 'live';
        } else if (state.status === 'fading-out') {
          state.fade = Math.max(0, state.fade - dt / FADE_S);
          setFade(state, state.fade);
          if (state.fade <= 0) release(state);
        }
      }

      if (cameraPos) {
        scanCooldown -= dt;
        if (scanCooldown <= 0) {
          scanCooldown = SCAN_EVERY_S;
          scan(cameraPos);
        }
      }
    },
  };
}
