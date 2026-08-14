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

import { DoubleSide, InstancedBufferAttribute, InstancedMesh, PlaneGeometry, ShaderMaterial, Vector2, Vector3 } from 'three';
import { shared } from './env.js';
import { DECK_ALTITUDE } from './clouds.js';

// Rain thins with the quality tier but never switches off: a storm that renders
// dry because the governor demoted is worse than a slow one.
// Instancing makes count nearly free -- these are two triangles each -- so the
// shaft count is high. At 3000 spread through a column kilometres wide the rain
// read as scattered showers rather than a downpour.
// Both ends of this have now been measured against real frames:
//   26k over a 1.4 km radius -> readable shafts, but sparse
//   64k over a 350 m radius  -> a dense dither speckle, reads as noise
// This sits between them.
export const RAIN_CAPS = { ultra: 44000, high: 44000, medium: 22000, low: 9000 };

// The rain column runs the full height from the cloud deck to the ground, so
// the shafts visibly hang off the clouds that are producing them.
const RAIN_TOP = DECK_ALTITUDE;
// How wide the column is, as a multiple of the camera's orbit distance: the
// rain has to cover what is on screen, so it grows as you pull back.
// SMALL, and centred on the camera rather than on the city. This is the lesson
// that took longest here: spreading drops evenly across the whole view puts
// almost all of them far away, where a streak is under a pixel and contributes
// nothing -- 64,000 of them rendered as about eight visible lines. Rain reads
// as rain when it is CLOSE to the eye and dense. nycsim uses a 120 m radius for
// exactly this reason; this is wider only because the camera sits further out.
const RADIUS_PER_DISTANCE = 0.5;
const RADIUS_MIN = 300;
const RADIUS_MAX = 2200;

const clamp01 = (v) => (v < 0 ? 0 : v > 1 ? 1 : v);

export function createRain(scene, { sampleAt }) {
  const cap = RAIN_CAPS.ultra;

  // --------------------------------------------------------- in-world streaks
  // Long enough to read at diorama distance, short enough to read as RAIN. At
  // 150 m each streak was a vertical pole standing over the city; the length
  // has to stay well under the height it falls through or the eye sees columns
  // instead of weather.
  // Short and thin and MANY. Width has to clear about a pixel at the working
  // camera distance or the streak renders as nothing; length is what decides
  // whether the result reads as rain or as a picket fence. At 3.4 x 95 m these
  // were unmistakably vertical poles standing over the city, spaced far enough
  // apart to count. Rain is dense and small: the density has to come from the
  // NUMBER of streaks, not the size of them.
  const geometry = new PlaneGeometry(3.4, 72);
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
    // DoubleSide is NOT optional here, and dropping it when porting from nycsim
    // is what made 64,000 streaks render as nothing. The quad billboards around
    // the fall direction using cross(fall, viewDir), so its winding flips
    // depending on which side of the camera the drop is on -- with the default
    // FrontSide, every streak on the wrong side is silently culled.
    side: DoubleSide,
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

        vA = uOn * 0.55 * smoothstep(0.0, 0.05, vFall);
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

  function update(dt, focus, cameraPosition, cameraDistance = 900) {
    // Local rain, not the citywide mean: stand in the shower, not near it.
    intensity = clamp01(sampleAt(focus.x, focus.z, 'precip'));
    const count = Math.floor(activeCap * intensity);
    mesh.visible = count > 0;
    mesh.count = count;
    if (!count) return 0;

    // Centred on the CAMERA in xz so the drops are near the eye and read, but
    // running from the GROUND up to the cloud deck in y, so they still visibly
    // fall the whole way from the clouds rather than appearing at eye level.
    uniforms.uCenter.value.set(cameraPosition.x, focus.y, cameraPosition.z);
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
