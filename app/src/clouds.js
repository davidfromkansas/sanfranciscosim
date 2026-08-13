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
export const CLOUD_CAPS = { ultra: 64, high: 64, medium: 40, low: 24 };

// Altitude bands, metres. Low cloud is the marine layer's ceiling and the one
// that matters in San Francisco; the others are scenery.
const LAYERS = [
  { key: 'low', altitude: 620, scale: 340, spread: 1.0 },
  { key: 'mid', altitude: 2000, scale: 620, spread: 1.35 },
  { key: 'high', altitude: 6000, scale: 1500, spread: 1.9 },
];

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
  const material = new MeshLambertMaterial({ color: 0xffffff, transparent: true, opacity: 0.95, depthWrite: false });
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
      // Base position, drifted every frame and wrapped at the extent.
      x: (hash(i, 1) - 0.5) * 2 * EXTENT * layer.spread,
      z: (hash(i, 2) - 0.5) * 2 * EXTENT * layer.spread,
      size: 0.65 + hash(i, 3) * 0.7,
      spin: hash(i, 4) * Math.PI * 2,
      lift: (hash(i, 5) - 0.5) * 140,
    });
  }

  let activeCap = cap;

  function setQuality(key) {
    activeCap = CLOUD_CAPS[key] ?? cap;
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
      const threshold = hash(i, 6) * 0.9;
      const presence = Math.max(0, Math.min(1, (cover - threshold) * 4));

      if (presence <= 0.01) {
        // Park it far below the world rather than reallocating the table.
        _matrix.compose(_hidden, _quaternion, _scale.set(0.0001, 0.0001, 0.0001));
        mesh.setMatrixAt(i, _matrix);
        continue;
      }

      drawn++;
      const size = slot.layer.scale * slot.size * (0.55 + 0.45 * presence);
      _position.set(slot.x, slot.layer.altitude + slot.lift, slot.z);
      _quaternion.setFromAxisAngle(UP, slot.spin);
      _scale.set(size, size * 0.42, size);
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

