// Rain, ported from the owner's nycsim (public/index.html — makePrecip and
// precipOverlay). That codebase had already solved the problem this one kept
// failing at, and its comment says it plainly: in-world particles "only read
// from near street level, so from aerial/hero views you couldn't tell it was
// raining".
//
// So there are TWO systems, handing off by altitude:
//
//   1. In-world streaks — an InstancedMesh in a cylinder around the camera. All
//      motion happens in the VERTEX SHADER: the CPU writes a centre and a wind
//      vector once a frame and nothing else. Each quad billboards around the
//      FALL direction, so a streak always turns its face to the eye while
//      staying aligned with the way the rain is going — it reads as a line, not
//      a rectangle. Fades OUT as the camera climbs.
//
//   2. A screen-space veil — one fullscreen shader with three layers of slanted
//      streaks, drawn after the scene. Fades IN as the camera climbs.
//
// The implementation this replaces moved two thousand instances on the CPU
// every frame and still rendered nothing from the hero view. This does less
// work and is visible from every camera.

import {
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

// Rain thins with the quality tier but never switches off: a storm that renders
// dry because the governor demoted is worse than a slow one.
export const RAIN_CAPS = { ultra: 3000, high: 3000, medium: 1600, low: 700 };

// The cylinder the streaks live in, metres. Larger than nycsim's because this
// camera pulls much further out.
const RADIUS = 320;
const HEIGHT = 420;
// Above this the in-world streaks are gone and the veil carries it alone.
const STREAK_CEILING = 2600;

const _size = new Vector2();
const clamp01 = (v) => (v < 0 ? 0 : v > 1 ? 1 : v);

export function createRain(scene, { sampleAt, renderer }) {
  const cap = RAIN_CAPS.ultra;

  // --------------------------------------------------------- in-world streaks
  const geometry = new PlaneGeometry(0.09, 2.6);
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
    uSpeed: { value: 34 },
  };

  const material = new ShaderMaterial({
    transparent: true,
    depthWrite: false,
    uniforms,
    vertexShader: /* glsl */ `
      attribute vec3 aRnd;
      uniform vec3 uCenter;
      uniform vec2 uWind;
      uniform float uTime, uSpeed, uOn;
      varying float vA;
      void main() {
        // Scatter over a disc. sqrt keeps the density even instead of crowding
        // everything into the middle.
        float r = sqrt(aRnd.x) * ${RADIUS.toFixed(1)};
        float ang = aRnd.y * 6.28318;
        float speed = uSpeed * (0.8 + aRnd.z * 0.5);
        float H = ${HEIGHT.toFixed(1)};
        // Distance fallen grows with time, so the drop descends and recycles.
        float fy = mod(aRnd.z * 977.0 + uTime * speed, H);
        vec2 base = uCenter.xz + vec2(cos(ang), sin(ang)) * r;
        vec2 carry = uWind * (fy / max(speed, 0.1));
        vec3 wp = vec3(base.x + carry.x, uCenter.y + H * 0.62 - fy, base.y + carry.y);

        // Billboard around the fall direction rather than around the camera.
        vec3 fall = normalize(vec3(uWind.x, -uSpeed, uWind.y));
        vec3 vd = normalize(wp - cameraPosition);
        vec3 rt = normalize(cross(fall, vd));
        vec3 p = wp + rt * position.x - fall * position.y;

        vA = uOn * 0.3;
        gl_Position = projectionMatrix * viewMatrix * vec4(p, 1.0);
      }
    `,
    fragmentShader: /* glsl */ `
      varying float vA;
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

  // ------------------------------------------------------------- screen veil
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
      precision highp float;
      varying vec2 vUv;
      uniform float uTime, uOpacity, uAspect, uSlant;
      float hash(vec2 p){ return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453); }
      void main(){
        if (uOpacity <= 0.001) discard;
        vec2 uv = vUv; uv.x *= uAspect;
        float acc = 0.0;
        // Three layers at different densities and speeds: the parallax between
        // them is what keeps it from reading as one flat texture.
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
      }
    `,
  });
  veilScene.add(new Mesh(new PlaneGeometry(2, 2), veilMaterial));

  let activeCap = cap;
  let intensity = 0;

  const setQuality = (key) => {
    activeCap = RAIN_CAPS[key] ?? cap;
  };

  function update(dt, focus, cameraPosition) {
    // Local rain, not the citywide mean: stand in the shower, not near it.
    intensity = clamp01(sampleAt(focus.x, focus.z, 'precip'));
    const count = Math.floor(activeCap * intensity);
    mesh.visible = count > 0;
    mesh.count = count;
    if (!count) {
      veilUniforms.uOpacity.value = 0;
      return 0;
    }

    const wind = shared.uWind.value;
    uniforms.uCenter.value.copy(cameraPosition);
    uniforms.uWind.value.copy(wind);
    // Height above the ground being framed — this decides the hand-off between
    // the streaks and the veil.
    const altitude = Math.max(0, cameraPosition.y - focus.y);
    uniforms.uOn.value = clamp01((STREAK_CEILING - altitude) / 900);

    // The veil ramps the other way: barely there up close, carrying it from high.
    const size = renderer.getSize(_size);
    veilUniforms.uAspect.value = size.x / Math.max(1, size.y);
    veilUniforms.uSlant.value = 0.14 + Math.min(0.35, Math.abs(wind.x) * 0.02);
    veilUniforms.uOpacity.value = intensity * clamp01(0.3 + altitude / 2600) * 0.55;
    return count;
  }

  // Drawn after the scene AND after the post pass, straight onto the canvas —
  // the veil sits in front of the tilt-shift rather than being blurred by it.
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
