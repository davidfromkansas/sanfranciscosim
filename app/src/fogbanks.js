// Fog banks: David's hand-made fog cube, instanced wherever the weather field
// says there is fog.
//
// The shader fog (materials.js) makes the city DISSOLVE with distance. It can
// never be seen as an object, because it only tints surfaces that are already
// there. These banks are the other half: actual geometry with a silhouette, so
// a wall of vapour can sit in the air over the Sunset and read as a thing.
//
// The asset is layered alpha wisp cards — the same technique the reference
// images use — so one cube already looks volumetric from any angle. We just
// need a lot of them, in the right places.
//
// One InstancedMesh, one draw call. The GLB carries a texture and blend mode,
// which the LANDMARK contract forbids; that rule governs the landmark intake
// path in assets.js, not code-loaded effect geometry, exactly as the moon and
// the toy clouds already are. Rule 3 still applies: if the file is missing or
// broken, the banks simply do not exist and the shader fog carries the scene.

import { Color, DynamicDrawUsage, InstancedBufferAttribute, InstancedMesh, Matrix4, Quaternion, Vector3 } from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { shared } from './env.js';

const URL = `${import.meta.env.BASE_URL}sf-assets/fog-cube.glb`;

// Banks are the most expensive thing weather draws — they are big, blended and
// overlapping. They go first when the tier drops.
export const BANK_CAPS = { ultra: 120, high: 120, medium: 64, low: 0 };

// The cube is a unit volume, so this is the width of one bank in metres.
const BANK_SIZE = 900;
// Sea level to here: the marine layer's own thickness.
const BANK_BASE = 20;
const BANK_TOP = 260;
const EXTENT = 9000;

const _matrix = new Matrix4();
const _position = new Vector3();
const _quaternion = new Quaternion();
const _scale = new Vector3();
const _hidden = new Vector3(0, -100000, 0);
const UP = new Vector3(0, 1, 0);

function hash(i, salt) {
  const x = Math.sin(i * 127.1 + salt * 311.7) * 43758.5453;
  return x - Math.floor(x);
}

export function createFogBanks(scene, { sampleAt }) {
  let mesh = null;
  let alphaAttribute = null;
  let activeCap = BANK_CAPS.high;
  let ready = false;
  const tuning = { size: 1, opacity: 1, density: 1 };
  const cap = BANK_CAPS.ultra;

  const slots = [];
  for (let i = 0; i < cap; i++) {
    slots.push({
      x: (hash(i, 1) - 0.5) * 2 * EXTENT,
      z: (hash(i, 2) - 0.5) * 2 * EXTENT,
      y: BANK_BASE + hash(i, 5) * (BANK_TOP - BANK_BASE),
      size: 0.6 + hash(i, 3) * 0.9,
      spin: hash(i, 4) * Math.PI * 2,
      // Each bank appears at its own point on the density ramp, so fog thickens
      // by gaining banks rather than by everything fading up together.
      threshold: hash(i, 6) * 0.85,
    });
  }

  new GLTFLoader().load(
    URL,
    (gltf) => {
      let source = null;
      gltf.scene.traverse((o) => {
        if (!source && o.isMesh) source = o;
      });
      if (!source) {
        console.warn('fog banks: no mesh in fog-cube.glb — shader fog only');
        return;
      }

      const material = source.material;
      // The asset's own note: layered transparency only sorts correctly with
      // depth writes off.
      material.depthWrite = false;
      material.transparent = true;
      material.toneMapped = false;
      material.fog = false;

      // Per-instance alpha, so a bank can fade in with the field instead of
      // popping. instanceColor would tint but not fade, so this is its own
      // attribute multiplied into the fragment's alpha.
      const alphas = new Float32Array(cap);
      alphaAttribute = new InstancedBufferAttribute(alphas, 1);
      alphaAttribute.setUsage(DynamicDrawUsage);

      material.onBeforeCompile = (shader) => {
        shader.uniforms.uBankTint = { value: new Color(0xffffff) };
        shader.uniforms.uNight = shared.uNight;
        shader.vertexShader = shader.vertexShader
          .replace('#include <common>', '#include <common>\n        attribute float aFogAlpha;\n        varying float vFogAlpha;')
          .replace('#include <begin_vertex>', '#include <begin_vertex>\n        vFogAlpha = aFogAlpha;');
        shader.fragmentShader = shader.fragmentShader
          .replace('#include <common>', '#include <common>\n        uniform float uNight;\n        varying float vFogAlpha;')
          .replace(
            '#include <dithering_fragment>',
            `#include <dithering_fragment>
            gl_FragColor.a *= vFogAlpha;
            // A bank at night is dark vapour lit by the city, not a white sheet.
            gl_FragColor.rgb = mix(gl_FragColor.rgb, gl_FragColor.rgb * 0.35, uNight);`
          );
      };

      mesh = new InstancedMesh(source.geometry, material, cap);
      mesh.geometry.setAttribute('aFogAlpha', alphaAttribute);
      mesh.instanceMatrix.setUsage(DynamicDrawUsage);
      mesh.name = 'fog-banks';
      mesh.frustumCulled = false;
      mesh.castShadow = false;
      mesh.receiveShadow = false;
      // After the opaque city, before the clouds above it.
      mesh.renderOrder = 850;
      scene.add(mesh);
      ready = true;
    },
    undefined,
    (error) => {
      // Rule 3: no banks is a perfectly good city. The shader fog is untouched.
      console.warn('fog banks: fog-cube.glb unavailable — shader fog only', error);
    }
  );

  function setQuality(key) {
    activeCap = BANK_CAPS[key] ?? BANK_CAPS.high;
  }

  function tune(patch = {}) {
    if (Number.isFinite(patch.size)) tuning.size = Math.max(0.1, patch.size);
    if (Number.isFinite(patch.opacity)) tuning.opacity = Math.max(0, Math.min(2, patch.opacity));
    if (Number.isFinite(patch.density)) tuning.density = Math.max(0, Math.min(2, patch.density));
    return { ...tuning };
  }

  function update(dt) {
    if (!ready || !mesh) return 0;
    const limit = Math.min(activeCap, cap);
    const wind = shared.uWind.value;
    let drawn = 0;

    for (let i = 0; i < cap; i++) {
      const slot = slots[i];
      // Banks ride the wind, at a fraction of its speed: a fog bank is a mass,
      // not a leaf.
      slot.x += wind.x * dt * 0.45;
      slot.z += wind.y * dt * 0.45;
      if (slot.x > EXTENT) slot.x -= EXTENT * 2;
      else if (slot.x < -EXTENT) slot.x += EXTENT * 2;
      if (slot.z > EXTENT) slot.z -= EXTENT * 2;
      else if (slot.z < -EXTENT) slot.z += EXTENT * 2;

      // A clear day has a residual density of a few percent, and an instance
      // whose threshold happened to land near zero would sit there as a lone
      // bank in a blue sky. Nothing below this counts as fog at all.
      const raw = i < limit ? sampleAt(slot.x, slot.z, 'fog') * tuning.density : 0;
      const local = raw < 0.08 ? 0 : raw;
      const presence = Math.max(0, Math.min(1, (local - slot.threshold) * 3));

      if (presence <= 0.02) {
        alphaAttribute.array[i] = 0;
        _matrix.compose(_hidden, _quaternion, _scale.set(0.0001, 0.0001, 0.0001));
        mesh.setMatrixAt(i, _matrix);
        continue;
      }

      drawn++;
      const size = BANK_SIZE * slot.size * tuning.size * (0.7 + 0.3 * presence);
      _position.set(slot.x, slot.y, slot.z);
      _quaternion.setFromAxisAngle(UP, slot.spin);
      // Wide and flat: a marine layer spreads, it does not tower.
      _scale.set(size, size * 0.32, size);
      _matrix.compose(_position, _quaternion, _scale);
      mesh.setMatrixAt(i, _matrix);
      alphaAttribute.array[i] = presence * tuning.opacity;
    }

    mesh.instanceMatrix.needsUpdate = true;
    alphaAttribute.needsUpdate = true;
    mesh.count = cap;
    return drawn;
  }

  return {
    update,
    setQuality,
    tune,
    get mesh() {
      return mesh;
    },
    get ready() {
      return ready;
    },
    dispose() {
      if (mesh) scene.remove(mesh);
    },
  };
}
