// The Bay and the Pacific: one big plane animated from a single repeating
// texture sampled in two independently scrolling layers. Their interference
// creates the broken highlights; the original procedural water remains in the
// shader as the guaranteed fallback when the image is missing or unusable.

import {
  DataTexture,
  LinearFilter,
  LinearMipmapLinearFilter,
  Mesh,
  PlaneGeometry,
  RepeatWrapping,
  RGBAFormat,
  ShaderMaterial,
  SRGBColorSpace,
  TextureLoader,
  UnsignedByteType,
  Vector3,
} from 'three';
import { shared } from './env.js';

const TEXTURE_URL = '/textures/ocean-sunshine-inspired.png';
const TEXTURE_SETTINGS = Object.freeze({
  speed: 2.37,
  scale: 1,
  threshold: 0.75,
  brightness: 1.1,
  distanceSheen: 0.65,
});

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
  uniform float uCheap;
  uniform vec3 uFogColor;
  uniform float uFogDensity;
  uniform sampler2D uWater;
  uniform float uHasTexture;
  uniform float uSpeed;
  uniform float uScale;
  uniform float uThreshold;
  uniform float uBrightness;
  uniform float uDistance;
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

  float waterLuminance(vec3 color) {
    return dot(color, vec3(0.2126, 0.7152, 0.0722));
  }

  mat2 rotate2d(float angle) {
    float s = sin(angle);
    float c = cos(angle);
    return mat2(c, -s, s, c);
  }

  void main() {
    vec3 view = uCameraPos - vWorld;
    float dist = length(view);
    vec3 V = view / dist;

    float detail = clamp(1.0 - dist / 9000.0, 0.08, 1.0);
    vec3 L = normalize(uSunDir);
    vec2 lightH = normalize(L.xz + vec2(0.00001));
    vec2 viewH = normalize(V.xz + vec2(0.00001));
    float streak = pow(max(dot(lightH, viewH), 0.0), 6.0);
    vec3 col;

    if (uHasTexture > 0.5) {
      // The exported demo scale is converted to world space here: one source
      // repeat covers about 500 m before the configured multiplier. Its visible
      // wave cells therefore land in the tens-of-metres range at city scale.
      vec2 baseUv = vWorld.xz * (uScale / 500.0);
      float t = uTime * uSpeed;
      vec2 uvA = baseUv + vec2(0.020, 0.013) * t;
      vec2 uvB = rotate2d(0.31) * (baseUv * 1.17) + vec2(-0.011, 0.024) * t;

      // Keep both counter-drifting samples on every quality tier. Collapsing
      // Layer B onto Layer A in low mode made the whole surface appear to
      // travel in one direction, which removed the demo's defining motion.
      vec3 layerA = texture2D(uWater, uvA).rgb;
      vec3 layerB = texture2D(uWater, uvB).rgb;
      float a = waterLuminance(layerA);
      float b = waterLuminance(layerB);
      float interference = (a + b * 2.0) / 3.0;
      float glints = smoothstep(
        uThreshold,
        min(0.999, uThreshold + 0.085),
        interference
      );
      glints *= smoothstep(0.42, 0.82, max(a, b));

      // Modern equivalent of the article's custom mip chain: nearby water is
      // clearer, while a middle-distance band carries the strongest sheen.
      float nearClarity = smoothstep(250.0, 1400.0, dist);
      float sheenBand = exp(-pow((dist - 4200.0) / 1800.0, 2.0));
      float distanceResponse = mix(
        1.0,
        0.35 + 0.65 * nearClarity + sheenBand * 0.75,
        uDistance
      );

      vec3 deep = mix(vec3(0.018, 0.25, 0.34), vec3(0.01, 0.02, 0.045), uNight);
      vec3 aqua = mix(vec3(0.025, 0.58, 0.64), vec3(0.02, 0.055, 0.095), uNight);
      vec3 baseTexture = mix(layerA, layerB, 0.46);
      col = mix(deep, aqua, smoothstep(0.24, 0.82, waterLuminance(baseTexture)));
      col = mix(col, baseTexture, 0.20 * (1.0 - uNight * 0.8));

      float fres = pow(1.0 - max(V.y, 0.0), 4.0);
      col = mix(col, uSkyColor * 0.72, fres * 0.72);
      vec3 glintColor = mix(vec3(0.58, 0.96, 1.0), uSunColor, 0.35);
      col += glintColor * glints * uBrightness * uGlitter * distanceResponse * (1.0 - uNight * 0.72);
      col += uSunColor * streak * 0.08 * (1.0 - uNight * 0.6);
    } else {
      // Original procedural path: required fallback for a missing/broken PNG.
      vec2 p = vWorld.xz * 0.035;
      float t = uTime * 0.35;
      float n1 = noise(p + vec2(t, t * 0.6));
      float n2 = 0.0;
      float n3 = 0.0;
      if (uCheap < 0.5) {
        n2 = noise(p * 2.7 - vec2(t * 0.8, t * 0.4));
        n3 = noise(p * 0.31 + vec2(t * 0.15, -t * 0.1));
      }
      vec3 N = normalize(vec3(
        (n1 * 0.55 + n2 * 0.3) * detail,
        1.0,
        (n2 * 0.5 - n1 * 0.35 + n3 * 0.4) * detail
      ));
      vec3 H = normalize(L + V);
      float spec = pow(max(dot(N, H), 0.0), mix(220.0, 48.0, uCheap));
      float sparkle = pow(max(n1 * 0.5 + n2 * 0.5, 0.0), 5.0) * streak * detail;
      float fres = pow(1.0 - max(dot(N, V), 0.0), 4.0);
      vec3 deep = mix(vec3(0.035, 0.10, 0.135), vec3(0.01, 0.02, 0.045), uNight);
      vec3 shallow = mix(vec3(0.09, 0.22, 0.26), vec3(0.02, 0.05, 0.09), uNight);
      col = mix(deep, shallow, clamp(dist / 6000.0, 0.0, 1.0));
      col = mix(col, uSkyColor * 0.75, fres * 0.85);
      col += uSunColor * (spec * 2.4 + sparkle * 3.4) * uGlitter * (1.0 - uNight * 0.55);
      col += uSunColor * streak * 0.14 * (1.0 - uNight * 0.6);
    }

    float fogFactor = 1.0 - exp(-uFogDensity * uFogDensity * dist * dist);
    col = mix(col, uFogColor, clamp(fogFactor, 0.0, 1.0));

    gl_FragColor = vec4(col, 1.0);
  }
`;

export function createWater(scene, extent) {
  // A complete sampler is bound from frame one. The shader does not use it
  // until the real texture is decoded, and it remains harmless if loading
  // fails and the procedural fallback stays active.
  const placeholder = new DataTexture(
    new Uint8Array([5, 72, 96, 255]),
    1,
    1,
    RGBAFormat,
    UnsignedByteType
  );
  placeholder.needsUpdate = true;

  const uniforms = {
    uSunDir: shared.uSunDir,
    uSunColor: shared.uSunColor,
    uSkyColor: shared.uSkyColor,
    uNight: shared.uNight,
    uTime: shared.uTime,
    uCameraPos: { value: new Vector3() },
    uGlitter: { value: 1 },
    uCheap: { value: 0 },
    uFogColor: { value: scene.fog.color },
    uFogDensity: { value: scene.fog.density },
    uWater: { value: placeholder },
    uHasTexture: { value: 0 },
    uSpeed: { value: TEXTURE_SETTINGS.speed },
    uScale: { value: TEXTURE_SETTINGS.scale },
    uThreshold: { value: TEXTURE_SETTINGS.threshold },
    uBrightness: { value: TEXTURE_SETTINGS.brightness },
    uDistance: { value: TEXTURE_SETTINGS.distanceSheen },
  };

  // Clip the water to the city extent so it stays inside the plinth — the
  // bay is a depression in the slab, not an endless ocean. The plane is
  // centered at the origin, which is also the center of the extent.
  const w = extent ? extent.maxX - extent.minX : 30000;
  const d = extent ? extent.maxZ - extent.minZ : 30000;
  const mesh = new Mesh(
    new PlaneGeometry(w, d, 8, 8),
    new ShaderMaterial({ uniforms, vertexShader: VERT, fragmentShader: FRAG })
  );
  mesh.rotation.x = -Math.PI / 2;
  mesh.position.y = 0.1;
  mesh.frustumCulled = false;
  mesh.renderOrder = -10;
  mesh.name = 'water';
  scene.add(mesh);

  new TextureLoader().load(
    TEXTURE_URL,
    (texture) => {
      texture.wrapS = RepeatWrapping;
      texture.wrapT = RepeatWrapping;
      texture.minFilter = LinearMipmapLinearFilter;
      texture.magFilter = LinearFilter;
      texture.generateMipmaps = true;
      texture.colorSpace = SRGBColorSpace;
      texture.needsUpdate = true;
      uniforms.uWater.value = texture;
      uniforms.uHasTexture.value = 1;
      placeholder.dispose();
    },
    undefined,
    () => {
      console.warn('water texture unavailable — keeping the procedural fallback');
    }
  );

  return {
    mesh,
    update(cameraPos) {
      uniforms.uCameraPos.value.copy(cameraPos);
      uniforms.uFogDensity.value = scene.fog.density;
    },
    setGlitter(v) {
      uniforms.uGlitter.value = v;
    },
    setQuality(tier) {
      uniforms.uCheap.value = tier === 'low' ? 1 : 0;
    },
    get textured() {
      return uniforms.uHasTexture.value > 0.5;
    },
  };
}
