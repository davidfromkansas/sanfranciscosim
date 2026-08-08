// Sky, sun and the golden-hour -> dusk time-of-day system. One directional sun
// plus one hemisphere light; every other light in the city (windows, street
// lamps, headlights, bridge necklaces) is an emissive shader term driven by the
// shared uniforms exported here.

import {
  BackSide,
  Color,
  DirectionalLight,
  FogExp2,
  HemisphereLight,
  Mesh,
  ShaderMaterial,
  SphereGeometry,
  Vector2,
  Vector3,
} from 'three';

// Shared uniform objects: materials hold references to these exact objects, so
// setTime() only has to write them once.
export const shared = {
  uTime: { value: 0 },
  uSunDir: { value: new Vector3(-0.8, 0.26, 0.2).normalize() },
  uSunColor: { value: new Color(1.0, 0.78, 0.5) },
  uSkyColor: { value: new Color(0.42, 0.56, 0.72) },
  uNight: { value: 0 },
  // Drifting cloud shadows: cover fades out as night falls, drift is advanced
  // every frame by the prevailing westerly.
  uCloudCover: { value: 0.32 },
  uCloudDrift: { value: new Vector2(0, 0) },
  // 1 in diorama mode: materials go bright and flat and drop the weather.
  uToy: { value: 0 },
};

const CLOUD_WIND = [0.0042, 0.0016];

const SKY_VERT = /* glsl */ `
  varying vec3 vDir;
  void main() {
    vDir = normalize(position);
    vec4 mv = modelViewMatrix * vec4(position, 1.0);
    gl_Position = projectionMatrix * mv;
  }
`;

const SKY_FRAG = /* glsl */ `
  uniform vec3 uSunDir;
  uniform vec3 uHorizonDay;
  uniform vec3 uZenithDay;
  uniform vec3 uHorizonNight;
  uniform vec3 uZenithNight;
  uniform float uNight;
  varying vec3 vDir;

  void main() {
    vec3 dir = normalize(vDir);
    float h = clamp(dir.y * 1.15 + 0.06, 0.0, 1.0);
    vec3 horizon = mix(uHorizonDay, uHorizonNight, uNight);
    vec3 zenith = mix(uZenithDay, uZenithNight, uNight);
    vec3 col = mix(horizon, zenith, pow(h, 0.72));

    // Warm glow wrapped around the sun, strongest right at the horizon.
    float sun = max(dot(dir, normalize(uSunDir)), 0.0);
    float halo = pow(sun, 8.0) * (1.0 - uNight * 0.45);
    float wide = pow(sun, 2.0) * 0.34 * (1.0 - uNight * 0.3);
    vec3 glow = mix(vec3(1.0, 0.72, 0.42), vec3(1.0, 0.45, 0.3), uNight);
    col += glow * (halo * 1.5 + wide);
    col += vec3(1.0, 0.86, 0.66) * pow(sun, 220.0) * 3.0 * (1.0 - uNight * 0.8);

    // Sparse stars once the sun is down.
    if (uNight > 0.55 && dir.y > 0.02) {
      vec3 q = floor(dir * 340.0);
      float n = fract(sin(dot(q, vec3(12.9898, 78.233, 45.164))) * 43758.5453);
      float star = smoothstep(0.9985, 1.0, n) * (uNight - 0.55) / 0.45;
      col += vec3(star) * 0.9 * smoothstep(0.02, 0.35, dir.y);
    }
    gl_FragColor = vec4(col, 1.0);
  }
`;

const DAY = {
  horizon: new Color(0.96, 0.72, 0.47),
  zenith: new Color(0.29, 0.5, 0.78),
  sun: new Color(1.0, 0.79, 0.52),
  hemiSky: new Color(0.58, 0.7, 0.85),
  hemiGround: new Color(0.36, 0.3, 0.24),
  sunIntensity: 2.7,
  hemiIntensity: 0.85,
  fog: new Color(0.83, 0.73, 0.62),
};

const NIGHT = {
  horizon: new Color(0.16, 0.13, 0.2),
  zenith: new Color(0.02, 0.03, 0.08),
  sun: new Color(0.24, 0.28, 0.48),
  hemiSky: new Color(0.1, 0.13, 0.22),
  hemiGround: new Color(0.05, 0.05, 0.07),
  sunIntensity: 0.16,
  hemiIntensity: 0.3,
  fog: new Color(0.09, 0.1, 0.15),
};

// Toy mode key/fill: #fff2df sun at 2.4, #bfd9f2 over #d8cfc0 sky fill at 1.1.
const TOY = {
  sun: new Color(1.0, 0.949, 0.874),
  sunIntensity: 2.4,
  hemiSky: new Color(0.749, 0.851, 0.949),
  hemiGround: new Color(0.847, 0.812, 0.753),
  hemiIntensity: 1.1,
};

export function createEnvironment(scene) {
  const skyUniforms = {
    uSunDir: shared.uSunDir,
    uNight: shared.uNight,
    uHorizonDay: { value: DAY.horizon.clone() },
    uZenithDay: { value: DAY.zenith.clone() },
    uHorizonNight: { value: NIGHT.horizon.clone() },
    uZenithNight: { value: NIGHT.zenith.clone() },
  };

  const sky = new Mesh(
    // Stay comfortably inside the 60 km camera far plane even when the camera
    // is near a corner of the city; clipping the sky sphere reveals black wedges.
    new SphereGeometry(30000, 32, 20),
    new ShaderMaterial({
      uniforms: skyUniforms,
      vertexShader: SKY_VERT,
      fragmentShader: SKY_FRAG,
      side: BackSide,
      depthWrite: false,
      depthTest: false,
      fog: false,
    })
  );
  sky.frustumCulled = false;
  sky.renderOrder = -1000;
  scene.add(sky);

  const sun = new DirectionalLight(DAY.sun.clone(), DAY.sunIntensity);
  sun.castShadow = true;
  sun.shadow.mapSize.set(4096, 4096);
  sun.shadow.bias = -0.0006;
  sun.shadow.normalBias = 1.2;
  const cam = sun.shadow.camera;
  cam.near = 10;
  cam.far = 9000;
  scene.add(sun);
  scene.add(sun.target);

  const hemi = new HemisphereLight(DAY.hemiSky.clone(), DAY.hemiGround.clone(), DAY.hemiIntensity);
  scene.add(hemi);

  scene.fog = new FogExp2(DAY.fog.clone().getHex(), 0.000019);

  const state = { time: 0, shadowsEnabled: true };

  // t: 0 = golden hour (sun ~15 deg over the western horizon), 1 = night.
  function setTime(t) {
    state.time = Math.min(1, Math.max(0, t));
    const k = state.time;
    // Sun drops from +15 deg to -8 deg and swings slightly north as it sets.
    const elevation = (15 - 23 * k) * (Math.PI / 180);
    const azimuth = (256 + 14 * k) * (Math.PI / 180);
    shared.uSunDir.value
      .set(Math.cos(elevation) * Math.sin(azimuth), Math.sin(elevation), Math.cos(elevation) * Math.cos(azimuth))
      .normalize();

    // Night ramps in over the last part of the sweep: this is what drives the
    // window ignition, street lights and bridge necklaces.
    const night = Math.min(1, Math.max(0, (k - 0.36) / 0.5));
    shared.uNight.value = night;

    sun.color.copy(DAY.sun).lerp(NIGHT.sun, night);
    sun.intensity = DAY.sunIntensity + (NIGHT.sunIntensity - DAY.sunIntensity) * night;
    hemi.color.copy(DAY.hemiSky).lerp(NIGHT.hemiSky, night);
    hemi.groundColor.copy(DAY.hemiGround).lerp(NIGHT.hemiGround, night);
    hemi.intensity = DAY.hemiIntensity + (NIGHT.hemiIntensity - DAY.hemiIntensity) * night;

    if (state.toy) {
      sun.color.copy(TOY.sun);
      sun.intensity = TOY.sunIntensity;
      hemi.color.copy(TOY.hemiSky);
      hemi.groundColor.copy(TOY.hemiGround);
      hemi.intensity = TOY.hemiIntensity;
    }

    shared.uSunColor.value.copy(sun.color);
    shared.uSkyColor.value.copy(hemi.color);
    scene.fog.color.copy(DAY.fog).lerp(NIGHT.fog, night);
    // Overcast reads as shade only while there is sun to block.
    shared.uCloudCover.value = 0.32 * (1 - night * 0.85);
  }

  function updateClouds(dt) {
    shared.uCloudDrift.value.x += CLOUD_WIND[0] * dt;
    shared.uCloudDrift.value.y += CLOUD_WIND[1] * dt;
  }

  // Keep the shadow frustum tight around the camera pivot: at street level it
  // covers a few blocks, at god view the whole downtown mass.
  function updateShadow(pivot, distance) {
    const extent = Math.min(2600, Math.max(320, distance * 0.85));
    const dir = shared.uSunDir.value;
    sun.target.position.copy(pivot);
    sun.position.copy(pivot).addScaledVector(dir, Math.max(2500, extent * 2.4));
    cam.left = -extent;
    cam.right = extent;
    cam.top = extent;
    cam.bottom = -extent;
    cam.far = Math.max(6000, extent * 6);
    cam.updateProjectionMatrix();
  }

  function setShadowQuality(size) {
    if (size === 0) {
      sun.castShadow = false;
      return;
    }
    sun.castShadow = true;
    if (sun.shadow.mapSize.x !== size) {
      sun.shadow.mapSize.set(size, size);
      if (sun.shadow.map) {
        sun.shadow.map.dispose();
        sun.shadow.map = null;
      }
    }
  }

  // Diorama lighting: a bright tabletop key light, soft sky fill and no fog, so
  // the model reads as a physical object rather than an atmosphere.
  const savedFog = scene.fog;
  function setToy(on) {
    shared.uToy.value = on ? 1 : 0;
    scene.fog = on ? null : savedFog;
    sun.shadow.radius = on ? 3 : 1;
    state.toy = on;
    setTime(state.time);
  }

  setTime(0);
  return { sky, sun, hemi, setTime, setToy, updateClouds, updateShadow, setShadowQuality, state };
}
