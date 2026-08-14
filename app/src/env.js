// Sky, sun and moon: the real ones, for San Francisco, at the real wall clock.
// One directional key light (the sun by day, the moon at night) plus one
// hemisphere light; every other light in the city (windows, street lamps,
// headlights, bridge necklaces) is an emissive shader term driven by the shared
// uniforms exported here.

import {
  AdditiveBlending,
  BackSide,
  BufferAttribute,
  BufferGeometry,
  Color,
  DirectionalLight,
  DoubleSide,
  FogExp2,
  HemisphereLight,
  IcosahedronGeometry,
  Mesh,
  PlaneGeometry,
  Points,
  PointsMaterial,
  Quaternion,
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
  // Drifting cloud shadows. Cover now comes from the live weather field (see
  // weather.js); this is only the scroll offset of the shadow noise, advanced
  // every frame by the real wind.
  uCloudDrift: { value: new Vector2(0, 0) },
  // 1 in diorama mode: materials go bright and flat and drop the weather.
  uToy: { value: 0 },
  // Live weather, sampled as a field rather than as one citywide number, so the
  // Sunset can be socked in while the Mission is clear. Written by weather.js;
  // see docs/plans/WEATHER-PLAN.md. R fog, G low cloud, B rain, A high cloud.
  uWeatherField: { value: null },
  // World-space bbox of that field: uv = (worldXZ - origin) * scale.
  uWeatherOrigin: { value: new Vector2() },
  uWeatherScale: { value: new Vector2(1, 1) },
  // Where the wind is blowing TO, in m/s, in world axes.
  uWind: { value: new Vector2() },
  // Citywide means, for the systems that do not need the whole field.
  uRain: { value: 0 },
  // How wet the ground is. Follows the rain up quickly and down slowly -- a
  // street that dries the instant the shower stops looks wrong, and the slow
  // dry-out is most of what sells rain in the first place.
  uWetness: { value: 0 },
  // One-frame lightning flash, 0..1. Storms only.
  uFlash: { value: 0 },
  uSmoke: { value: 0 },
  // NOTE: there are deliberately no fog uniforms here. Fog in this city is the
  // fog-cube GLB instanced by fogbanks.js and nothing else — David's call, so
  // there is exactly one fog system to reason about. Do not add a shader fog
  // term back.
};

// Noise-space drift per (m/s of wind) per second. The shadow noise samples
// world * 0.00055, so this is calibrated to reproduce the old hand-tuned drift
// rate at a typical San Francisco westerly (~6.7 m/s), and to scale from there.
const CLOUD_DRIFT_PER_MS = 0.00067;

const SKY_VERT = /* glsl */ `
  varying vec3 vDir;
  void main() {
    vDir = normalize(position);
    vec4 mv = modelViewMatrix * vec4(position, 1.0);
    gl_Position = projectionMatrix * mv;
  }
`;

const SKY_FRAG = /* glsl */ `
  // The horizon glow follows the true sun even after it has set, so the warm
  // band stays over the Pacific at dusk while the key light has moved to the moon.
  uniform vec3 uGlowDir;
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
    float sun = max(dot(dir, normalize(uGlowDir)), 0.0);
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

// Toy mode key/fill: #fff2df sun over a #bfd9f2/#d8cfc0 sky fill. The key is the
// diorama's shipped 2.4 lifted by a quarter — every state below carries the same
// 1.25 on the key only, so the sun and the moon gained a stop of presence
// without the ambient fill flattening the shading.
const TOY = {
  sun: new Color(1.0, 0.949, 0.874),
  sunIntensity: 3.0,
  hemiSky: new Color(0.749, 0.851, 0.949),
  hemiGround: new Color(0.847, 0.812, 0.753),
  hemiIntensity: 1.1,
};

// Low sun: the key warms and softens, the fill picks up the ground bounce.
const TOY_GOLDEN = {
  sun: new Color(0xffe3c0),
  sunIntensity: 2.63,
  hemiSky: new Color(0xc6d6ec),
  hemiGround: new Color(0xd8c3a2),
  hemiIntensity: 1.12,
};

// Sun on the horizon: coral-amber key, the fill cooling towards the navy night.
// The fill carries this band deliberately — a key light grazing at 0° puts
// almost nothing on a roof or a street, so leaning on it here reads as a power
// cut rather than a sunset.
const TOY_DUSK = {
  sun: new Color(0xffb489),
  sunIntensity: 2.25,
  hemiSky: new Color(0xc0a4bd),
  hemiGround: new Color(0xb5906b),
  hemiIntensity: 1.3,
};

// Toy night: deep navy rather than black, so the model still reads as a painted
// object sitting on a table in a dark room. Moonlight is pale blue and weak
// enough that the warm windows carry the picture — but the fill is deliberately
// generous, because a diorama nobody can see is not a diorama.
const TOY_NIGHT = {
  horizon: new Color(0x2c3a5c),
  zenith: new Color(0x1a2340),
  sun: new Color(0xb8c8e8),
  sunIntensity: 0.63,
  hemiSky: new Color(0x7688c2),
  hemiGround: new Color(0x7a6a54),
  hemiIntensity: 1.15,
  fog: new Color(0x1e2740),
};
const STAR_COUNT = 2000;

// The usability floor. The plan asks for at least 0.25 key and 0.42 hemisphere;
// on the actual model those left a Quality=Low new-moon street unreadable, so
// the floor sits well above the minimum. The tilt-shift grade is not the lever.
const NIGHT_KEY_FLOOR = 0.63;
const NIGHT_HEMI_FLOOR = TOY_NIGHT.hemiIntensity;
// A shadow camera pointed at a key light far below the horizon is degenerate.
const KEY_Y_FLOOR = -0.2;
const DEG = Math.PI / 180;

// Scratch: setSky runs once a second and must not allocate.
const _sunDir = new Vector3();
const _moonDir = new Vector3();
const _keyDir = new Vector3();
const _up = new Vector3(0, 1, 0);
const _qa = new Quaternion();
const _qb = new Quaternion();
const _qm = new Quaternion();

// AGENTS.md world frame: +x east, -z north, +y up. Astronomical azimuth is
// measured from true north, clockwise, so east (90 deg) must land on +x.
function directionFrom(elevation, azimuth, out) {
  const c = Math.cos(elevation);
  return out.set(Math.sin(azimuth) * c, Math.sin(elevation), -Math.cos(azimuth) * c).normalize();
}

const clamp01 = (v) => (v < 0 ? 0 : v > 1 ? 1 : v);
const lerp = (a, b, t) => a + (b - a) * t;
// 1 at `from`, 0 at `to`, linear in between — the piecewise blend of §4.
const ramp = (value, from, to) => clamp01((value - to) / (from - to));

// Blend two lighting states into the live lights.
function applyState(a, b, t, sun, hemi) {
  sun.color.copy(a.sun).lerp(b.sun, t);
  sun.intensity = lerp(a.sunIntensity, b.sunIntensity, t);
  hemi.color.copy(a.hemiSky).lerp(b.hemiSky, t);
  hemi.groundColor.copy(a.hemiGround).lerp(b.hemiGround, t);
  hemi.intensity = lerp(a.hemiIntensity, b.hemiIntensity, t);
}

export function createEnvironment(scene) {
  const skyUniforms = {
    // Its own vector, not shared.uSunDir: that one carries whichever body owns
    // the key light, which at night is the moon.
    uGlowDir: { value: new Vector3(0, 1, 0) },
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

  // ------------------------------------------------------------- night sky kit
  // A low-poly cream moon, one soft halo quad behind it, and a field of stars.
  // All three live on a single group that is only shown once night is under way,
  // so the daytime scene graph is untouched.
  // Two flat colours split by the real terminator: the fragment compares its
  // own world normal against the direction of the sun, so the crescent is the
  // phase, not a texture. No craters, no gradient — a painted paper moon.
  const moonUniforms = {
    uOpacity: { value: 0 },
    uSunW: { value: new Vector3(1, 0, 0) },
    uLit: { value: new Color(0xf6eede) },
    uDark: { value: new Color(0x2a3350) },
  };
  const nightSky = new Mesh(
    new IcosahedronGeometry(700, 3),
    new ShaderMaterial({
      uniforms: moonUniforms,
      vertexShader: /* glsl */ `
        varying vec3 vNormalW;
        void main() {
          vNormalW = normalize(mat3(modelMatrix) * normal);
          gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
        }
      `,
      fragmentShader: /* glsl */ `
        uniform float uOpacity;
        uniform vec3 uSunW;
        uniform vec3 uLit;
        uniform vec3 uDark;
        varying vec3 vNormalW;
        void main() {
          float d = dot(normalize(vNormalW), normalize(uSunW));
          gl_FragColor = vec4(mix(uDark, uLit, smoothstep(-0.04, 0.04, d)), uOpacity);
        }
      `,
      transparent: true,
      depthWrite: false,
      depthTest: false,
      fog: false,
    })
  );
  nightSky.position.set(9000, 7000, -14000);
  nightSky.renderOrder = -900;
  nightSky.frustumCulled = false;
  nightSky.visible = false;
  scene.add(nightSky);

  // A radial falloff, not a flat panel: an additive quad with a constant colour
  // reads as a rectangle in the sky, which is exactly what a halo must not do.
  const halo = new Mesh(
    new PlaneGeometry(4200, 4200),
    new ShaderMaterial({
      uniforms: { uOpacity: { value: 0 }, uColor: { value: new Color(0xdfe6f6) } },
      vertexShader: /* glsl */ `
        varying vec2 vUv;
        void main() {
          vUv = uv;
          gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
        }
      `,
      fragmentShader: /* glsl */ `
        uniform float uOpacity;
        uniform vec3 uColor;
        varying vec2 vUv;
        void main() {
          float r = length(vUv - 0.5) * 2.0;
          // Bright close to the moon, gone well before the quad's edge.
          float glow = pow(clamp(1.0 - r, 0.0, 1.0), 2.6);
          gl_FragColor = vec4(uColor * glow, glow * uOpacity);
        }
      `,
      transparent: true,
      blending: AdditiveBlending,
      depthWrite: false,
      depthTest: false,
      side: DoubleSide,
      fog: false,
    })
  );
  halo.position.copy(nightSky.position);
  halo.renderOrder = -950;
  halo.frustumCulled = false;
  halo.visible = false;
  scene.add(halo);

  const starPositions = new Float32Array(STAR_COUNT * 3);
  for (let i = 0; i < STAR_COUNT; i++) {
    // Uniform over the upper hemisphere of a 24 km shell.
    const u = (i * 2654435761) % 4096;
    const a = ((i * 7919) % 10007) / 10007;
    const theta = (u / 4096) * Math.PI * 2;
    const y = 0.06 + a * 0.94;
    const r = Math.sqrt(Math.max(0, 1 - y * y));
    starPositions[i * 3] = Math.cos(theta) * r * 24000;
    starPositions[i * 3 + 1] = y * 24000;
    starPositions[i * 3 + 2] = Math.sin(theta) * r * 24000;
  }
  const starGeometry = new BufferGeometry();
  starGeometry.setAttribute('position', new BufferAttribute(starPositions, 3));
  const stars = new Points(
    starGeometry,
    new PointsMaterial({
      color: 0xdce6ff,
      size: 90,
      sizeAttenuation: true,
      transparent: true,
      opacity: 0,
      depthWrite: false,
      depthTest: false,
      fog: false,
    })
  );
  stars.renderOrder = -960;
  stars.frustumCulled = false;
  stars.visible = false;
  scene.add(stars);

  const FOG_DENSITY = 0.000019;
  scene.fog = new FogExp2(DAY.fog.clone().getHex(), FOG_DENSITY);

  const state = {
    shadowsEnabled: true,
    toy: false,
    // Radians, as handed in by the astronomy module.
    sunElevation: 45 * DEG,
    sunAzimuth: 240 * DEG,
    moonElevation: -30 * DEG,
    moonAzimuth: 60 * DEG,
    moonIllumination: 1,
    night: 0,
    // 0 = the sun owns the key light, 1 = the moon does.
    moonKey: 0,
  };

  // Where the real moon is, kept for updateNightSky; the key light may be using
  // the fallback direction instead when the moon is down.
  const moonWorld = new Vector3(0, 1, 0);
  const moonPlace = new Vector3();

  // The whole time-of-day system: give it where the sun and the moon actually
  // are, and it produces the diorama's lighting for that moment.
  function setSky({ sunEl, sunAz, moonEl = -Math.PI / 2, moonAz = 0, moonIllum = 1 }) {
    state.sunElevation = sunEl;
    state.sunAzimuth = sunAz;
    state.moonElevation = moonEl;
    state.moonAzimuth = moonAz;
    state.moonIllumination = clamp01(moonIllum);

    const elevation = sunEl / DEG;
    directionFrom(sunEl, sunAz, _sunDir);
    directionFrom(moonEl, moonAz, moonWorld);
    skyUniforms.uGlowDir.value.copy(_sunDir);
    moonUniforms.uSunW.value.copy(_sunDir);

    // The three blend bands of the plan, as descending-elevation ramps:
    // 0 at the first angle's start, 1 once the sun has dropped to the second.
    const golden = ramp(elevation, 8, 25);
    const dusk = ramp(elevation, -4, 8);
    const nightfall = ramp(elevation, -10, -4);

    // uNight is the city's own switch — windows, lamps, bridge lights. It keys
    // off the horizon rather than off the blend bands: exactly 0 while the sun
    // is up, exactly 1 once the sun is 10° under, and a smooth fade in between,
    // so lamps come on as the sun goes down and never before.
    const night = ramp(elevation, -10, 0);
    state.night = night;
    shared.uNight.value = night;

    if (state.toy) {
      if (elevation >= 8) applyState(TOY, TOY_GOLDEN, golden, sun, hemi);
      else if (elevation >= -4) applyState(TOY_GOLDEN, TOY_DUSK, dusk, sun, hemi);
      else applyState(TOY_DUSK, TOY_NIGHT, nightfall, sun, hemi);
      sun.shadow.radius = 3 + night * 3;
    } else {
      applyState(DAY, NIGHT, night, sun, hemi);
    }

    // ---------------------------------------------------------- the key light
    // Below the horizon the moon takes over, and the vector is never allowed to
    // sink far enough to make the shadow camera degenerate.
    state.moonKey = nightfall;
    const moonUp = moonEl > -0.5 * DEG;
    if (moonUp) _moonDir.copy(moonWorld);
    // No moon in the sky: a fixed high north-easterly fill, so the city is lit
    // from somewhere plausible rather than from nowhere.
    else directionFrom(40 * DEG, 45 * DEG, _moonDir);

    if (nightfall <= 0) _keyDir.copy(_sunDir);
    else if (nightfall >= 1) _keyDir.copy(_moonDir);
    else {
      // Sun and moon are often near-antipodal, so a straight lerp would pass
      // through the origin. Rotate one onto the other instead.
      _qa.setFromUnitVectors(_up, _sunDir);
      _qb.setFromUnitVectors(_up, _moonDir);
      _qm.copy(_qa).slerp(_qb, nightfall);
      _keyDir.copy(_up).applyQuaternion(_qm);
    }
    if (_keyDir.y < KEY_Y_FLOOR) {
      _keyDir.y = KEY_Y_FLOOR;
      _keyDir.normalize();
    }
    shared.uSunDir.value.copy(_keyDir);

    // The usability floor, and only where it belongs — after dusk. Moonlight
    // scales with the lit fraction but never falls through the floor: a new
    // moon is not an excuse for an unreadable city.
    if (state.toy && nightfall > 0) {
      const moonIntensity = NIGHT_KEY_FLOOR + (moonUp ? 0.44 * state.moonIllumination : 0);
      sun.intensity = Math.max(lerp(sun.intensity, moonIntensity, nightfall), NIGHT_KEY_FLOOR * nightfall);
      hemi.intensity = Math.max(hemi.intensity, NIGHT_HEMI_FLOOR * nightfall);
    }

    // ------------------------------------------------------ moon, halo, stars
    const lift = Math.max(0, (night - 0.25) / 0.75);
    const moonLift = moonUp ? lift : 0;
    nightSky.visible = moonLift > 0.001;
    halo.visible = nightSky.visible;
    stars.visible = lift > 0.001;
    moonUniforms.uOpacity.value = moonLift;
    // A crescent throws far less glow than a full moon.
    halo.material.uniforms.uOpacity.value = moonLift * 0.85 * (0.25 + 0.75 * state.moonIllumination);
    stars.material.opacity = lift * 0.9;
    skyUniforms.uHorizonNight.value.copy(state.toy ? TOY_NIGHT.horizon : NIGHT.horizon);
    skyUniforms.uZenithNight.value.copy(state.toy ? TOY_NIGHT.zenith : NIGHT.zenith);

    shared.uSunColor.value.copy(sun.color);
    shared.uSkyColor.value.copy(hemi.color);
    scene.fog.color.copy(DAY.fog).lerp(state.toy ? TOY_NIGHT.fog : NIGHT.fog, night);
  }

  // The deprecated 0 to 1 sweep, kept only so the old SF.setTime alias and the
  // astronomy-failure fallback have something to call: t = 0 is a golden hour
  // over the Pacific, t = 1 is night with a full moon in the east.
  function setTime(t) {
    const k = clamp01(t);
    setSky({
      sunEl: (15 - 23 * k) * DEG,
      sunAz: (256 + 14 * k) * DEG,
      moonEl: (-10 + 45 * k) * DEG,
      moonAz: (76 + 14 * k) * DEG,
      moonIllum: 1,
    });
  }

  // The moon sits along its real direction at a fixed radius that rides with
  // the camera, so it never parallaxes behind a hill; the floor on y keeps it
  // clear of the terrain silhouette when it has only just risen.
  function updateNightSky(camera) {
    if (!stars.visible) return;
    stars.position.set(camera.position.x, 0, camera.position.z);
    if (!nightSky.visible) return;
    moonPlace.copy(moonWorld).multiplyScalar(16000);
    nightSky.position.set(camera.position.x + moonPlace.x, Math.max(900, moonPlace.y), camera.position.z + moonPlace.z);
    halo.position.copy(nightSky.position);
    halo.lookAt(camera.position);
  }

  // Shadows travel downwind. The noise is sampled as `world * k + drift`, so a
  // feature sits where world = (p - drift) / k: the offset must DECREASE along
  // the wind for the blanket to move with it, not against it.
  function updateClouds(dt) {
    const wind = shared.uWind.value;
    shared.uCloudDrift.value.x -= wind.x * CLOUD_DRIFT_PER_MS * dt;
    shared.uCloudDrift.value.y -= wind.y * CLOUD_DRIFT_PER_MS * dt;
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
  // the model reads as a physical object rather than an atmosphere. The fog is
  // switched off by density, not by nulling scene.fog: everything that reads
  // scene.fog (water's fog uniforms, every material's compiled fog chunk) keeps
  // working, and no shader is recompiled on the toggle.
  function setToy(on) {
    shared.uToy.value = on ? 1 : 0;
    scene.fog.density = on ? 0 : FOG_DENSITY;
    sun.shadow.radius = on ? 3 : 1;
    state.toy = on;
    setSky({
      sunEl: state.sunElevation,
      sunAz: state.sunAzimuth,
      moonEl: state.moonElevation,
      moonAz: state.moonAzimuth,
      moonIllum: state.moonIllumination,
    });
  }

  setSky({ sunEl: state.sunElevation, sunAz: state.sunAzimuth });
  return {
    sky,
    sun,
    hemi,
    moon: nightSky,
    stars,
    setSky,
    setTime,
    setToy,
    updateClouds,
    updateShadow,
    updateNightSky,
    setShadowQuality,
    state,
  };
}
