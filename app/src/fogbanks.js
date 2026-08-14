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

// Banks thin out as the tier drops, but they NEVER go to zero. Setting the
// low tier to 0 meant that the moment the governor demoted the scene — which
// it does readily on a loaded machine — the fog vanished completely and the
// city looked like the feature was broken. Fog is the headline here; it is the
// last thing to cut, not the first.
export const BANK_CAPS = { ultra: 625, high: 625, medium: 340, low: 150 };

// The cube is a unit volume, so this is the width of one bank in metres.
//
// Coverage matters, but so does SHAPE, and 2.1 km banks bought coverage by
// turning each instance into a flat slab the width of a district -- the frame
// filled with straight-edged translucent sheets instead of fog. The asset is a
// cluster: a discrete clump. So: much smaller clumps, many more of them, which
// is also how a real marine layer is built.
const BANK_SIZE = 820;
// Sea level to here: the marine layer's own thickness.
const BANK_BASE = 30;
const BANK_TOP = 340;
// Tighter than the cloud scatter: fog sits ON the city, not out at sea.
const EXTENT = 6000;

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
  // Opacity well under 1: these overlap heavily, and alpha compounds where
  // they stack, so a per-instance 1.0 stacked into an opaque wall.
  // Per-instance alpha. The banks overlap heavily by design (they have to, to
  // read as one mass rather than as separate puffs), and alpha compounds where
  // they stack, so this number is far more sensitive than it looks:
  //   0.16 -> a thin veil, too sparse
  //   0.26 -> fog you can still see the city through   <- shipped
  //   0.38 -> a full white-out, the city essentially gone
  const tuning = { size: 1, opacity: 0.26, density: 1 };
  const cap = BANK_CAPS.ultra;

  // A JITTERED GRID, not a random scatter. Random positions clump and leave
  // holes at any density -- which is why the fog read as a field of separate
  // puffs rather than one mass. On a grid every bank has neighbours a fixed
  // distance away, and because a bank is wider than a grid cell they overlap
  // into a continuous sheet. The jitter is what stops it looking like a grid.
  const GRID = Math.ceil(Math.sqrt(cap));
  const CELL = (2 * EXTENT) / GRID;
  const slots = [];
  for (let i = 0; i < cap; i++) {
    const gx = i % GRID;
    const gz = Math.floor(i / GRID);
    slots.push({
      x: -EXTENT + (gx + 0.5) * CELL + (hash(i, 1) - 0.5) * CELL * 0.85,
      z: -EXTENT + (gz + 0.5) * CELL + (hash(i, 2) - 0.5) * CELL * 0.85,
      y: BANK_BASE + hash(i, 5) * (BANK_TOP - BANK_BASE),
      size: 0.6 + hash(i, 3) * 0.9,
      spin: hash(i, 4) * Math.PI * 2,
      shown: false,
      lastSize: 0,
      // Each bank appears at its own point on the density ramp, so fog thickens
      // by gaining banks rather than by everything fading up together. The
      // range is deliberately well under 1: at 0.85 the higher-threshold banks
      // never switched on anywhere except the very thickest cells, which left
      // the fog bunched into one corner of the city instead of spread over it.
      threshold: hash(i, 6) * 0.22,
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
        shader.uniforms.uNight = shared.uNight;
        shader.uniforms.uSmoke = shared.uSmoke;
        shader.uniforms.uSmokeColor = { value: new Color(0xd8823c) };
        shader.vertexShader = shader.vertexShader
          .replace('#include <common>', '#include <common>\n        attribute float aFogAlpha;\n        varying float vFogAlpha;')
          .replace('#include <begin_vertex>', '#include <begin_vertex>\n        vFogAlpha = aFogAlpha;');
        shader.fragmentShader = shader.fragmentShader
          .replace('#include <common>', '#include <common>\n        uniform float uNight;\n        uniform float uSmoke;\n        uniform vec3 uSmokeColor;\n        varying float vFogAlpha;')
          .replace(
            '#include <dithering_fragment>',
            `#include <dithering_fragment>
            gl_FragColor.a *= vFogAlpha;
            // A bank at night is dark vapour lit by the city, not a white sheet.
            gl_FragColor.rgb = mix(gl_FragColor.rgb, gl_FragColor.rgb * 0.35, uNight);
            // Wildfire smoke: the same banks go amber rather than a second
            // system existing. September 2020 was orange, not grey.
            gl_FragColor.rgb = mix(gl_FragColor.rgb, uSmokeColor, clamp(uSmoke, 0.0, 1.0) * 0.6);`
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

  // Fraction of the bank box the visible banks actually cover. Counting
  // instances hides the only thing that matters -- 71 banks sounded fine while
  // covering 14% of the ground and reading as nothing.
  function coverage() {
    let area = 0;
    for (const slot of slots) if (slot.shown) area += Math.PI * (slot.lastSize / 2) ** 2;
    return +(area / (2 * EXTENT) ** 2).toFixed(3);
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
      // Thin the set by STRIDE, not by taking the first N: the low indices are
      // an arbitrary corner of the scatter, so slicing them left the survivors
      // clumped and off camera.
      const stride = Math.max(1, Math.ceil(cap / Math.max(1, limit)));
      const inTier = i % stride === 0;
      // Smoke fills the sky whether or not there is fog: a wildfire pall is
      // not damp, but it is very much in the air.
      // Smoke is a THIN haze, not thick ground fog. The light carries this
      // effect now (env.js turns the sun to an ember and the sky brown), so the
      // banks only need to hint at particulate in the air. At 0.45 they were as
      // dense as a pea-souper and the orange sky had nothing left to light.
      const smokeFloor = shared.uSmoke.value * 0.14;
      const raw = inTier ? Math.max(sampleAt(slot.x, slot.z, 'fog'), smokeFloor) * tuning.density : 0;
      const local = raw < 0.08 ? 0 : raw;
      const presence = Math.max(0, Math.min(1, (local - slot.threshold) * 3));

      slot.shown = presence > 0.02;
      if (presence <= 0.02) {
        alphaAttribute.array[i] = 0;
        _matrix.compose(_hidden, _quaternion, _scale.set(0.0001, 0.0001, 0.0001));
        mesh.setMatrixAt(i, _matrix);
        continue;
      }

      drawn++;
      const size = BANK_SIZE * slot.size * tuning.size * (0.7 + 0.3 * presence);
      slot.lastSize = size;
      _position.set(slot.x, slot.y, slot.z);
      _quaternion.setFromAxisAngle(UP, slot.spin);
      // Flattened, but nowhere near as hard as before: squashing a voxel
      // cluster to a third of its height is what made each one read as a sheet
      // rather than as a clump of vapour.
      _scale.set(size, size * 0.85, size);
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
    coverage,
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
