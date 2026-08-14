// Rain: shafts falling from the cloud deck down to the city.
//
// The vertex-shader motion and the fall-aligned billboard come from the owner's
// nycsim (public/index.html, makePrecip) and are the good parts of it. Its
// screen-space veil is deliberately NOT used here: a fullscreen overlay slides
// across the frame no matter where the clouds are, and in a diorama you are
// looking down at the weather from outside it, so rain has to visibly come OUT
// of the cloud deck and land on the city. Screen rain reads as a filter on the
// picture; world rain reads as weather happening to the model.
//
// So the column spans the real distance from DECK_ALTITUDE (the cloud ceiling,
// shared with clouds.js so they can never drift apart) down to the ground, and
// it is centred on the patch of city being framed rather than on the camera.
//
// All motion is in the VERTEX SHADER: the CPU writes a centre, a radius and a
// wind vector once a frame and nothing else. Each quad billboards around the
// FALL direction, so a streak turns its face to the eye while staying aligned
// with the way the rain is going — it reads as a line, never a rectangle.

import { InstancedBufferAttribute, InstancedMesh, PlaneGeometry, ShaderMaterial, Vector2, Vector3 } from 'three';
import { shared } from './env.js';
import { DECK_ALTITUDE } from './clouds.js';

// Rain thins with the quality tier but never switches off: a storm that renders
// dry because the governor demoted is worse than a slow one.
export const RAIN_CAPS = { ultra: 3000, high: 3000, medium: 1600, low: 700 };

// The rain column runs the full height from the cloud deck to the ground, so
// the shafts visibly hang off the clouds that are producing them.
const RAIN_TOP = DECK_ALTITUDE;
// How wide the column is, as a multiple of the camera's orbit distance: the
// rain has to cover what is on screen, so it grows as you pull back.
const RADIUS_PER_DISTANCE = 1.15;
const RADIUS_MIN = 700;
const RADIUS_MAX = 9000;

const clamp01 = (v) => (v < 0 ? 0 : v > 1 ? 1 : v);

export function createRain(scene, { sampleAt }) {
  const cap = RAIN_CAPS.ultra;

  // --------------------------------------------------------- in-world streaks
  // A long, thin shaft. These are hundreds of metres tall in world units --
  // at diorama distances a life-sized raindrop is far under a pixel.
  const geometry = new PlaneGeometry(2.2, 150);
  const seeds = new Float32Array(cap * 3);
  for (let i = 0; i < cap * 3; i++) {
    const x = Math.sin(i * 127.1 + 311.7) * 43758.5453;
    seeds[i] = x - Math.floor(x);
  }
  geometry.setAttribute('aRnd', new InstancedBufferAttribute(seeds, 3));

  const uniforms = {
    uCenter: { value: new Vector3() },
    uWind: { value: new Vector2() },
    uTime: shared.uTime,
    uOn: { value: 0 },
    uSpeed: { value: 620 },
    uRadius: { value: RADIUS_MIN },
    uTop: { value: RAIN_TOP },
  };

  const material = new ShaderMaterial({
    transparent: true,
    depthWrite: false,
    uniforms,
    vertexShader: /* glsl */ `
      attribute vec3 aRnd;
      uniform vec3 uCenter;
      uniform vec2 uWind;
      uniform float uTime, uSpeed, uOn, uRadius, uTop;
      varying float vA;
      varying float vFall;
      void main() {
        // Scatter over a disc. sqrt keeps the density even instead of crowding
        // everything into the middle.
        float r = sqrt(aRnd.x) * uRadius;
        float ang = aRnd.y * 6.28318;
        float speed = uSpeed * (0.8 + aRnd.z * 0.5);
        // Falls the WHOLE way from the cloud deck to the ground, then recycles.
        float fy = mod(aRnd.z * 977.0 + uTime * speed, uTop);
        vec2 base = uCenter.xz + vec2(cos(ang), sin(ang)) * r;
        vec2 carry = uWind * (fy / max(speed, 0.1));
        vec3 wp = vec3(base.x + carry.x, uCenter.y + uTop - fy, base.y + carry.y);
        // How far down the shaft has come, 0 at the cloud base and 1 at street
        // level: used to fade it in just under the deck so shafts appear to be
        // emerging from the cloud rather than starting in clear air.
        vFall = fy / uTop;

        // Billboard around the fall direction rather than around the camera.
        vec3 fall = normalize(vec3(uWind.x, -uSpeed, uWind.y));
        vec3 vd = normalize(wp - cameraPosition);
        vec3 rt = normalize(cross(fall, vd));
        vec3 p = wp + rt * position.x - fall * position.y;

        vA = uOn * 0.30 * smoothstep(0.0, 0.09, vFall);
        gl_Position = projectionMatrix * viewMatrix * vec4(p, 1.0);
      }
    `,
    fragmentShader: /* glsl */ `
      varying float vA;
      varying float vFall;
      void main() { gl_FragColor = vec4(0.78, 0.85, 0.95, vA); }
    `,
  });

  const mesh = new InstancedMesh(geometry, material, cap);
  mesh.count = 0;
  mesh.visible = false;
  mesh.frustumCulled = false;
  mesh.renderOrder = 900;
  mesh.name = 'rain';
  scene.add(mesh);

  let activeCap = cap;
  let intensity = 0;

  const setQuality = (key) => {
    activeCap = RAIN_CAPS[key] ?? cap;
  };

  function update(dt, focus, cameraDistance = 900) {
    // Local rain, not the citywide mean: stand in the shower, not near it.
    intensity = clamp01(sampleAt(focus.x, focus.z, 'precip'));
    const count = Math.floor(activeCap * intensity);
    mesh.visible = count > 0;
    mesh.count = count;
    if (!count) return 0;

    // Centred on the ground being framed, and running from there up to the
    // cloud deck -- so the shafts hang off the clouds and land on the city.
    uniforms.uCenter.value.set(focus.x, focus.y, focus.z);
    uniforms.uWind.value.copy(shared.uWind.value);
    uniforms.uRadius.value = Math.max(RADIUS_MIN, Math.min(RADIUS_MAX, cameraDistance * RADIUS_PER_DISTANCE));
    uniforms.uOn.value = 1;
    return count;
  }

  return {
    mesh,
    update,
    setQuality,
    get intensity() {
      return intensity;
    },
    dispose() {
      scene.remove(mesh);
      geometry.dispose();
      material.dispose();
    },
  };
}
