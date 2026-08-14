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
// Instancing makes count nearly free -- these are two triangles each -- so the
// shaft count is high. At 3000 spread through a column kilometres wide the rain
// read as scattered showers rather than a downpour.
export const RAIN_CAPS = { ultra: 26000, high: 26000, medium: 13000, low: 5000 };

// The rain column runs the full height from the cloud deck to the ground, so
// the shafts visibly hang off the clouds that are producing them.
const RAIN_TOP = DECK_ALTITUDE;
// How wide the column is, as a multiple of the camera's orbit distance: the
// rain has to cover what is on screen, so it grows as you pull back.
// Tighter than the view, deliberately. The column has to cover what is on
// screen, but every extra metre of radius thins the rain out over the square of
// it -- at a 9 km radius the shafts were spread through 250 square kilometres.
const RADIUS_PER_DISTANCE = 0.85;
const RADIUS_MIN = 600;
const RADIUS_MAX = 5200;

const clamp01 = (v) => (v < 0 ? 0 : v > 1 ? 1 : v);

export function createRain(scene, { sampleAt }) {
  const cap = RAIN_CAPS.ultra;

  // --------------------------------------------------------- in-world streaks
  // Long enough to read at diorama distance, short enough to read as RAIN. At
  // 150 m each streak was a vertical pole standing over the city; the length
  // has to stay well under the height it falls through or the eye sees columns
  // instead of weather.
  // WIDTH is what decides whether a streak exists on screen at all: at diorama
  // range anything under ~3 m is sub-pixel and renders as nothing, however many
  // there are. Length decides whether it reads as rain or as a pole. Both have
  // been wrong in both directions here; these are the values that survived
  // looking at the frame.
  const geometry = new PlaneGeometry(3.4, 95);
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

        vA = uOn * 0.5 * smoothstep(0.0, 0.07, vFall);
        gl_Position = projectionMatrix * viewMatrix * vec4(p, 1.0);
      }
    `,
    fragmentShader: /* glsl */ `
      varying float vA;
      varying float vFall;
      // Darker and cooler than the sky, not paler. Storms come with heavy fog
      // that washes the whole frame pale blue, and pale rain over a pale
      // background is invisible however much of it there is -- which is exactly
      // how 22,000 shafts managed to render nothing. Rain needs to be DARKER
      // than what is behind it.
      void main() { gl_FragColor = vec4(0.42, 0.50, 0.62, vA); }
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
