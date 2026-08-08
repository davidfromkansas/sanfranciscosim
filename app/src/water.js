// The Bay and the Pacific: one big plane with a procedural glitter shader —
// scrolling noise normals plus a specular streak toward the sun, which is what
// makes the water sparkle in the hero shot.

import { Mesh, PlaneGeometry, ShaderMaterial, Vector3 } from 'three';
import { shared } from './env.js';

const VERT = /* glsl */ `
  varying vec3 vWorld;
  void main() {
    vec4 world = modelMatrix * vec4(position, 1.0);
    vWorld = world.xyz;
    gl_Position = projectionMatrix * viewMatrix * world;
  }
`;

const FRAG = /* glsl */ `
  uniform vec3 uSunDir;
  uniform vec3 uSunColor;
  uniform vec3 uSkyColor;
  uniform vec3 uCameraPos;
  uniform float uTime;
  uniform float uNight;
  uniform float uGlitter;
  uniform vec3 uFogColor;
  uniform float uFogDensity;
  varying vec3 vWorld;

  vec2 hash2(vec2 p) {
    p = vec2(dot(p, vec2(127.1, 311.7)), dot(p, vec2(269.5, 183.3)));
    return -1.0 + 2.0 * fract(sin(p) * 43758.5453123);
  }

  float noise(vec2 p) {
    vec2 i = floor(p);
    vec2 f = fract(p);
    vec2 u = f * f * (3.0 - 2.0 * f);
    return mix(
      mix(dot(hash2(i + vec2(0.0, 0.0)), f - vec2(0.0, 0.0)), dot(hash2(i + vec2(1.0, 0.0)), f - vec2(1.0, 0.0)), u.x),
      mix(dot(hash2(i + vec2(0.0, 1.0)), f - vec2(0.0, 1.0)), dot(hash2(i + vec2(1.0, 1.0)), f - vec2(1.0, 1.0)), u.x),
      u.y);
  }

  void main() {
    vec3 view = uCameraPos - vWorld;
    float dist = length(view);
    vec3 V = view / dist;

    // Two scrolling noise octaves shape the ripple normal; scale falls off with
    // distance so the far Bay stays calm instead of aliasing into static.
    float detail = clamp(1.0 - dist / 9000.0, 0.08, 1.0);
    vec2 p = vWorld.xz * 0.035;
    float t = uTime * 0.35;
    float n1 = noise(p + vec2(t, t * 0.6));
    float n2 = noise(p * 2.7 - vec2(t * 0.8, t * 0.4));
    float n3 = noise(p * 0.31 + vec2(t * 0.15, -t * 0.1));
    vec3 N = normalize(vec3((n1 * 0.55 + n2 * 0.3) * detail, 1.0, (n2 * 0.5 - n1 * 0.35 + n3 * 0.4) * detail));

    vec3 L = normalize(uSunDir);
    vec3 H = normalize(L + V);
    float spec = pow(max(dot(N, H), 0.0), 220.0);
    // Broad sun streak along the sun azimuth, the classic golden-hour glitter.
    // Safe horizontal vectors: normalize(vec3(0)) is undefined and some GPU
    // drivers spread that NaN across an entire large plane triangle.
    vec2 lightH = normalize(L.xz + vec2(0.00001));
    vec2 viewH = normalize(V.xz + vec2(0.00001));
    float streak = pow(max(dot(lightH, viewH), 0.0), 6.0);
    float sparkle = pow(max(n1 * 0.5 + n2 * 0.5, 0.0), 5.0) * streak * detail;

    float fres = pow(1.0 - max(dot(N, V), 0.0), 4.0);
    vec3 deep = mix(vec3(0.035, 0.10, 0.135), vec3(0.01, 0.02, 0.045), uNight);
    vec3 shallow = mix(vec3(0.09, 0.22, 0.26), vec3(0.02, 0.05, 0.09), uNight);
    vec3 col = mix(deep, shallow, clamp(dist / 6000.0, 0.0, 1.0));
    col = mix(col, uSkyColor * 0.75, fres * 0.85);
    col += uSunColor * (spec * 2.4 + sparkle * 3.4) * uGlitter * (1.0 - uNight * 0.55);
    col += uSunColor * streak * 0.14 * (1.0 - uNight * 0.6);

    float fogFactor = 1.0 - exp(-uFogDensity * uFogDensity * dist * dist);
    col = mix(col, uFogColor, clamp(fogFactor, 0.0, 1.0));
    gl_FragColor = vec4(col, 1.0);
  }
`;

export function createWater(scene) {
  const uniforms = {
    uSunDir: shared.uSunDir,
    uSunColor: shared.uSunColor,
    uSkyColor: shared.uSkyColor,
    uNight: shared.uNight,
    uTime: shared.uTime,
    uCameraPos: { value: new Vector3() },
    uGlitter: { value: 1 },
    uFogColor: { value: scene.fog.color },
    uFogDensity: { value: scene.fog.density },
  };

  // Keep the mesh only a little larger than the baked city extent. A giant
  // 120 km quad exceeds the camera's 60 km far plane at its corners; WebGL then
  // clips it into a conspicuous black triangular wedge on the horizon.
  const mesh = new Mesh(
    new PlaneGeometry(30000, 30000, 8, 8),
    new ShaderMaterial({ uniforms, vertexShader: VERT, fragmentShader: FRAG })
  );
  mesh.rotation.x = -Math.PI / 2;
  mesh.position.y = 0.1;
  mesh.frustumCulled = false;
  mesh.renderOrder = -10;
  mesh.name = 'water';
  scene.add(mesh);

  return {
    mesh,
    update(cameraPos) {
      uniforms.uCameraPos.value.copy(cameraPos);
      uniforms.uFogDensity.value = scene.fog.density;
    },
    setGlitter(v) {
      uniforms.uGlitter.value = v;
    },
  };
}
