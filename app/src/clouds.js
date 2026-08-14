// Toy clouds: chunky cotton-ball blobs floating over the model, placed by the
// live weather field so they sit over the districts that are actually clouded.
//
// One InstancedMesh, one draw call, whatever the sky is doing. The geometry is
// a lumpy merge of a few icosahedrons — a physical diorama piece, per the style
// bible, not a gradient painted on the sky dome. Stage 3b reuses this same
// generator, flattened, for ground-level fog banks.
//
// No per-frame allocation: one scratch Matrix4 and one preallocated instance
// table, written in place.

import {
  Color,
  DynamicDrawUsage,
  IcosahedronGeometry,
  InstancedMesh,
  Matrix4,
  MeshLambertMaterial,
  Quaternion,
  Vector3,
} from 'three';
import { mergeGeometries } from 'three/addons/utils/BufferGeometryUtils.js';
import { shared } from './env.js';

// Instance caps by quality tier. The clouds are cosmetic: they go first.
export const CLOUD_CAPS = { ultra: 160, high: 160, medium: 96, low: 48 };

// Altitude bands, metres, with `scale` in geometry units — the blob is ~2.73
// units wide, so a scale of 720 is a cloud about 2 km across.
//
// These are sized for COVERAGE, not for instance count. The first cut used
// ~900 m clouds scattered over an 18 km box, which looked reasonable as a
// number (39 instances at full overcast) and read as an almost empty sky: it
// covered 8.7% of it. Real clouds are kilometres wide, and an overcast marine
// layer has to close over the city, so the low deck is both bigger and packed
// into a tighter box than the decorative layers above it.
// One ceiling, not three decks: every cloud shares an altitude, and the
// per-instance jitter is off, so this is a genuine single plane rather than a
// scatter around one. The bands still differ in size, spread and which part of
// the weather field they read.
//
// The height is pinned just UNDER the camera's own ceiling, so you can always
// climb above the deck but normally fly beneath it. Diorama mode clamps the
// orbit distance to 8000 m at a locked 42 degree pitch (see DIORAMA in
// camera.js), which puts the camera at most 8000 * sin(42) = ~5350 m over its
// pivot. 4600 leaves roughly 750 m of headroom. If that clamp ever changes,
// change this with it.
export const DECK_ALTITUDE = 4600;
const LAYERS = [
  { key: 'low', altitude: DECK_ALTITUDE, scale: 720, spread: 0.7 },
  { key: 'mid', altitude: DECK_ALTITUDE, scale: 1100, spread: 1.2 },
  { key: 'high', altitude: DECK_ALTITUDE, scale: 2000, spread: 1.6 },
];

// How squat a cloud is: 1.0 would be as tall as it is wide. Clouds are wide
// and flat, so the deck sits well under that.
const BASE_FLATTEN = 0.42;

// The city, plus margin so clouds exist beyond the visible edge.
const EXTENT = 9000;

const _matrix = new Matrix4();
const _position = new Vector3();
const _quaternion = new Quaternion();
const _scale = new Vector3();
const _hidden = new Vector3(0, -100000, 0);
const UP = new Vector3(0, 1, 0);

// A lumpy blob: several icosahedrons merged at offsets. Low poly on purpose —
// the silhouette carries the read, exactly like the toy buildings.
function blobGeometry() {
  const parts = [];
  const lobes = [
    [0, 0, 0, 1],
    [0.75, -0.1, 0.2, 0.68],
    [-0.7, -0.05, -0.15, 0.6],
    [0.15, 0.28, -0.6, 0.5],
    [-0.25, 0.2, 0.55, 0.46],
  ];
  for (const [x, y, z, r] of lobes) {
    const g = new IcosahedronGeometry(r, 1);
    g.translate(x, y, z);
    parts.push(g);
  }
  const merged = mergeGeometries(parts, false);
  for (const g of parts) g.dispose();
  // Flatten the underside: a cloud sits on its layer, it is not a ball.
  const pos = merged.getAttribute('position');
  for (let i = 0; i < pos.count; i++) {
    const y = pos.getY(i);
    if (y < 0) pos.setY(i, y * 0.45);
  }
  merged.computeVertexNormals();
  return merged;
}

// Deterministic scatter: the same seed always lays the sky out the same way, so
// a screenshot is reproducible and clouds do not teleport between reloads.
function hash(i, salt) {
  const x = Math.sin(i * 127.1 + salt * 311.7) * 43758.5453;
  return x - Math.floor(x);
}

export function createClouds(scene, { sampleAt }) {
  const geometry = blobGeometry();

  // Two flat tones split by the world-up normal: cream lit top, cool underside.
  // The same trick the moon uses — no texture, no second light.
  // Tuned down twice from the 0.95 the deck first shipped with: halved, then
  // another quarter off. Instances overlap heavily at high cover and do not
  // write depth, so alpha compounds where clouds stack — an overcast deck still
  // reads solid through its middle while the edges stay airy.
  const CLOUD_OPACITY = 0.356;
  const material = new MeshLambertMaterial({ color: 0xffffff, transparent: true, opacity: CLOUD_OPACITY, depthWrite: false });
  const lit = new Color(0xfdf8ef);
  const shade = new Color(0xb9c4d8);
  material.onBeforeCompile = (shader) => {
    shader.uniforms.uLit = { value: lit };
    shader.uniforms.uShade = { value: shade };
    shader.uniforms.uNight = shared.uNight;
    shader.vertexShader = shader.vertexShader
      .replace('#include <common>', '#include <common>\n        varying vec3 vCloudNormal;')
      .replace(
        '#include <defaultnormal_vertex>',
        `#include <defaultnormal_vertex>
        vCloudNormal = normalize(mat3(modelMatrix) * objectNormal);`
      );
    shader.fragmentShader = shader.fragmentShader
      .replace(
        '#include <common>',
        `#include <common>
        uniform vec3 uLit;
        uniform vec3 uShade;
        uniform float uNight;
        varying vec3 vCloudNormal;`
      )
      .replace(
        '#include <color_fragment>',
        `#include <color_fragment>
        float up = clamp(vCloudNormal.y * 0.5 + 0.5, 0.0, 1.0);
        vec3 cloud = mix(uShade, uLit, smoothstep(0.35, 0.75, up));
        // A cloudy night is dark, not a sky full of white blobs.
        cloud = mix(cloud, cloud * 0.28, uNight);
        diffuseColor.rgb = cloud;`
      );
  };

  const cap = CLOUD_CAPS.high;
  const mesh = new InstancedMesh(geometry, material, cap);
  mesh.instanceMatrix.setUsage(DynamicDrawUsage);
  mesh.name = 'toy-clouds';
  mesh.frustumCulled = false;
  mesh.castShadow = false;
  mesh.receiveShadow = false;
  mesh.renderOrder = -800;
  scene.add(mesh);

  // Per-instance home: which layer it belongs to and where it scatters.
  // Weighted, not round-robin: in San Francisco the low deck is the whole
  // story, and splitting instances evenly left an overcast marine layer looking
  // like scattered fair-weather puffs.
  const LAYER_MIX = [0.6, 0.25, 0.15];
  const slots = [];
  for (let i = 0; i < cap; i++) {
    const share = i / cap;
    const layer = share < LAYER_MIX[0] ? LAYERS[0] : share < LAYER_MIX[0] + LAYER_MIX[1] ? LAYERS[1] : LAYERS[2];
    slots.push({
      layer,
      key: layer.key,
      shown: false,
      lastSize: 0,
      // Base position, drifted every frame and wrapped at the extent.
      x: (hash(i, 1) - 0.5) * 2 * EXTENT * layer.spread,
      z: (hash(i, 2) - 0.5) * 2 * EXTENT * layer.spread,
      size: 0.65 + hash(i, 3) * 0.7,
      spin: hash(i, 4) * Math.PI * 2,
      // Vertical jitter is 0: a single ceiling means a single ceiling.
      lift: 0,
    });
  }

  let activeCap = cap;
  // Live tuning knobs. Cloud size and density are pure art calls that can only
  // be judged against the running scene, so they are adjustable at runtime
  // rather than only by redeploying: SF.clouds.tune({ size: 1.4 }).
  const tuning = { size: 1, density: 1, opacity: CLOUD_OPACITY, thickness: 1, altitude: 1 };

  function setQuality(key) {
    activeCap = CLOUD_CAPS[key] ?? cap;
  }

  function tune(patch = {}) {
    if (Number.isFinite(patch.size)) tuning.size = Math.max(0.1, patch.size);
    if (Number.isFinite(patch.density)) tuning.density = Math.max(0, Math.min(1.5, patch.density));
    if (Number.isFinite(patch.thickness)) tuning.thickness = Math.max(0.05, Math.min(4, patch.thickness));
    if (Number.isFinite(patch.altitude)) tuning.altitude = Math.max(0.1, Math.min(5, patch.altitude));
    if (Number.isFinite(patch.opacity)) {
      tuning.opacity = Math.max(0.02, Math.min(1, patch.opacity));
      material.opacity = tuning.opacity;
    }
    return { ...tuning };
  }

  // How much of the sky the current instances actually cover, as a fraction of
  // the low layer's scatter box. This is the number that matters for "does it
  // look overcast", and counting instances hides it entirely.
  function coverage() {
    geometry.computeBoundingBox();
    const unit = geometry.boundingBox.max.x - geometry.boundingBox.min.x;
    let area = 0;
    for (let i = 0; i < cap; i++) {
      const slot = slots[i];
      if (slot.key !== 'low' || !slot.shown) continue;
      const w = unit * slot.lastSize;
      area += Math.PI * (w / 2) ** 2;
    }
    const box = (2 * EXTENT * LAYERS[0].spread) ** 2;
    return +(area / box).toFixed(3);
  }

  function update(dt) {
    const wind = shared.uWind.value;
    const limit = Math.min(activeCap, cap);
    let drawn = 0;

    for (let i = 0; i < cap; i++) {
      const slot = slots[i];
      const bound = EXTENT * slot.layer.spread;

      // Drift with the real wind, and wrap so the sky never empties.
      slot.x += wind.x * dt;
      slot.z += wind.y * dt;
      if (slot.x > bound) slot.x -= bound * 2;
      else if (slot.x < -bound) slot.x += bound * 2;
      if (slot.z > bound) slot.z -= bound * 2;
      else if (slot.z < -bound) slot.z += bound * 2;

      // The field decides whether there IS a cloud here — this is what puts
      // cloud over the Sunset and not over the Mission.
      const key = slot.layer.key === 'low' ? 'cloudLow' : 'cloudHigh';
      const cover = i < limit ? sampleAt(slot.x, slot.z, key) : 0;
      // Each instance owns a slice of the 0..1 cover range, so raising cover
      // brings clouds in a few at a time instead of all at once.
      const threshold = hash(i, 6) * 0.9 * (2 - tuning.density);
      const presence = Math.max(0, Math.min(1, (cover - threshold) * 4));

      slot.shown = presence > 0.01;
      if (presence <= 0.01) {
        // Park it far below the world rather than reallocating the table.
        _matrix.compose(_hidden, _quaternion, _scale.set(0.0001, 0.0001, 0.0001));
        mesh.setMatrixAt(i, _matrix);
        continue;
      }

      drawn++;
      const size = slot.layer.scale * slot.size * (0.55 + 0.45 * presence) * tuning.size;
      slot.lastSize = size;
      _position.set(slot.x, slot.layer.altitude * tuning.altitude + slot.lift, slot.z);
      _quaternion.setFromAxisAngle(UP, slot.spin);
      _scale.set(size, size * BASE_FLATTEN * tuning.thickness, size);
      _matrix.compose(_position, _quaternion, _scale);
      mesh.setMatrixAt(i, _matrix);
    }

    mesh.instanceMatrix.needsUpdate = true;
    mesh.count = cap;
    return drawn;
  }

  return {
    mesh,
    update,
    setQuality,
    tune,
    coverage,
    get material() {
      return material;
    },
    dispose() {
      scene.remove(mesh);
      geometry.dispose();
      material.dispose();
    },
  };
}

