// Rain: a faithful port of nycsim's precipitation (public/index.html —
// makePrecip('rain') and precipOverlay), constants included.
//
// This repo re-derived those numbers several times and got them wrong in both
// directions every time, so they are copied rather than reasoned about. They
// only make sense TOGETHER, which is the part that kept being missed:
//
//   1. In-world streaks. Tiny — 3.5 cm x 95 cm — in a 120 m cylinder around the
//      camera, gated to `camY < 1600` so they fade out as you climb. They are a
//      CLOSE-UP effect and were never meant to be visible from altitude.
//
//   2. A screen-space veil that ramps the other way, `0.3 + camY / 1600`, and
//      carries the effect from high up. Without it there is no rain at all
//      above the streak ceiling — which is exactly the hole this repo kept
//      falling into while trying to make the streaks alone do everything.
//
// All streak motion is in the VERTEX shader: the CPU writes a centre and a wind
// vector per frame and nothing else. Each quad billboards around the FALL
// direction, so it turns its face to the eye while staying aligned with the way
// the rain is going — a line, never a rectangle. DoubleSide is required: that
// billboard flips its winding depending on which side of the camera a drop is
// on, and without it half of them are silently culled.

import {
  DoubleSide,
  InstancedBufferAttribute,
  InstancedMesh,
  Mesh,
  OrthographicCamera,
  PlaneGeometry,
  Scene,
  ShaderMaterial,
  Vector2,
  Vector3,
} from 'three';
import { shared } from './env.js';

// nycsim's N. Instancing makes this nearly free either way.
const N = 3000;
// The one deliberate departure. nycsim's camera lives near street level; this
// one orbits between 150 and 8000 m, so the whole in-world system is scaled up
// BODILY — cylinder, fall height, streak size and the altitude gate together —
// rather than any single number being re-tuned on its own. Piecemeal re-tuning
// of these values is precisely what went wrong repeatedly before.
const SCALE = 26;

const _size = new Vector2();
const clamp01 = (v) => (v < 0 ? 0 : v > 1 ? 1 : v);

export function createRain(scene, { sampleAt, renderer }) {
  // ------------------------------------------------- in-world streaks (nycsim)
  const geometry = new PlaneGeometry(0.035 * SCALE, 0.95 * SCALE);
  const seeds = new Float32Array(N * 3);
  for (let i = 0; i < N * 3; i++) {
    const x = Math.sin(i * 127.1 + 311.7) * 43758.5453;
    seeds[i] = x - Math.floor(x);
  }
  geometry.setAttribute('aRnd', new InstancedBufferAttribute(seeds, 3));

  const uniforms = {
    uCenter: { value: new Vector3() },
    uWind: { value: new Vector2() },
    uTime: shared.uTime,
    uOn: { value: 0 },
    uSpeed: { value: 15 * SCALE },
  };

  const material = new ShaderMaterial({
    transparent: true,
    depthWrite: false,
    side: DoubleSide,
    uniforms,
    vertexShader: /* glsl */ `
      attribute vec3 aRnd;
      uniform vec3 uCenter; uniform vec2 uWind; uniform float uTime, uSpeed, uOn;
      varying float vA;
      void main(){
        float r = sqrt(aRnd.x) * ${(120 * SCALE).toFixed(1)};
        float ang = aRnd.y * 6.28318;
        float speed = uSpeed * (0.8 + aRnd.z * 0.5);
        float H = ${(150 * SCALE).toFixed(1)};
        float fy = mod(aRnd.z * 977.0 + uTime * speed, H);
        vec2 base = uCenter.xz + vec2(cos(ang), sin(ang)) * r;
        vec2 carry = uWind * (fy / max(speed, 0.1));
        vec3 wp = vec3(base.x + carry.x, uCenter.y + ${(90 * SCALE).toFixed(1)} - fy, base.y + carry.y);
        vec3 fall = normalize(vec3(uWind.x, -uSpeed, uWind.y));
        vec3 vd = normalize(wp - cameraPosition);
        vec3 rt = normalize(cross(fall, vd));
        vec3 p = wp + rt * position.x - fall * position.y;
        vA = uOn * 0.25;
        gl_Position = projectionMatrix * viewMatrix * vec4(p, 1.0);
      }`,
    fragmentShader: 'varying float vA; void main(){ gl_FragColor = vec4(0.75, 0.82, 0.92, vA); }',
  });

  const mesh = new InstancedMesh(geometry, material, N);
  mesh.count = 0;
  mesh.visible = false;
  mesh.frustumCulled = false;
  mesh.renderOrder = 5;
  mesh.name = 'rain';
  scene.add(mesh);

  // ----------------------------------------------------- screen veil (nycsim)
  const veilScene = new Scene();
  const veilCamera = new OrthographicCamera(-1, 1, 1, -1, 0, 1);
  const veilUniforms = {
    uTime: shared.uTime,
    uOpacity: { value: 0 },
    uAspect: { value: 1 },
    uSlant: { value: 0.18 },
  };
  const veilMaterial = new ShaderMaterial({
    transparent: true,
    depthTest: false,
    depthWrite: false,
    uniforms: veilUniforms,
    vertexShader: 'varying vec2 vUv; void main(){ vUv = uv; gl_Position = vec4(position.xy, 0.0, 1.0); }',
    fragmentShader: /* glsl */ `
      precision highp float; varying vec2 vUv;
      uniform float uTime, uOpacity, uAspect, uSlant;
      float hash(vec2 p){ return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453); }
      void main(){
        if (uOpacity <= 0.001) discard;
        vec2 uv = vUv; uv.x *= uAspect;
        float acc = 0.0;
        for (int i = 0; i < 3; i++){
          float fi = float(i);
          float dens = 85.0 + fi * 55.0, sp = 1.1 + fi * 0.7;
          vec2 p = uv; p.x += p.y * uSlant;
          float colf = p.x * dens, ci = floor(colf), cf = fract(colf);
          float seed = hash(vec2(ci, fi * 7.0));
          float y = fract(p.y * (1.6 + seed) + uTime * sp + seed * 9.0);
          float streak = smoothstep(0.0, 0.04, y) * smoothstep(0.32, 0.0, y);
          float thin = smoothstep(0.5, 0.46, abs(cf - 0.5));
          acc += streak * thin * step(0.58, seed) * (0.5 + 0.5 * seed);
        }
        gl_FragColor = vec4(vec3(0.82, 0.87, 0.96), acc * 0.5 * uOpacity);
      }`,
  });
  veilScene.add(new Mesh(new PlaneGeometry(2, 2), veilMaterial));

  // nycsim's altitude gates, in this scene's units.
  const CEILING = 1600 * (SCALE / 6);
  const FADE = 500 * (SCALE / 6);

  let intensity = 0;
  let cap = 1;

  const setQuality = (key) => {
    // nycsim scales the fleet by a quality factor; same idea, never to zero.
    cap = key === 'low' ? 0.4 : key === 'medium' ? 0.7 : 1;
  };

  function update(dt, focus, cameraPosition) {
    // Local rain, not the citywide mean: stand in the shower, not near it.
    intensity = clamp01(sampleAt(focus.x, focus.z, 'precip')) * cap;
    const count = Math.floor(N * intensity);
    mesh.visible = count > 0;
    mesh.count = count;
    if (!count) {
      veilUniforms.uOpacity.value = 0;
      return 0;
    }

    // Streaks ride the camera and fade out with altitude; the veil takes over.
    uniforms.uCenter.value.copy(cameraPosition);
    uniforms.uWind.value.copy(shared.uWind.value);
    const camY = Math.max(0, cameraPosition.y - focus.y);
    uniforms.uOn.value = clamp01((CEILING - camY) / FADE);

    const size = renderer.getSize(_size);
    veilUniforms.uAspect.value = size.x / Math.max(1, size.y);
    veilUniforms.uOpacity.value = intensity * Math.min(0.85, Math.max(0.3, 0.3 + camY / CEILING));
    return count;
  }

  // After the scene and after the post pass, straight onto the canvas.
  function renderVeil() {
    if (veilUniforms.uOpacity.value <= 0.001) return;
    const auto = renderer.autoClear;
    renderer.autoClear = false;
    renderer.setRenderTarget(null);
    renderer.render(veilScene, veilCamera);
    renderer.autoClear = auto;
  }

  return {
    mesh,
    update,
    renderVeil,
    setQuality,
    get intensity() {
      return intensity;
    },
    get veilOpacity() {
      return veilUniforms.uOpacity.value;
    },
    dispose() {
      scene.remove(mesh);
      geometry.dispose();
      material.dispose();
      veilMaterial.dispose();
    },
  };
}
