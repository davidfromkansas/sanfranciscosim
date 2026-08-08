// Bootstrap: load the baked city, build the scene, and open on the hero frame —
// the whole of San Francisco at golden hour, no title card, no fade-in.

import {
  ACESFilmicToneMapping,
  PCFShadowMap,
  PerspectiveCamera,
  Raycaster,
  Scene,
  SRGBColorSpace,
  Vector2,
  Vector3,
  WebGLRenderer,
} from 'three';
import { loadCore } from './data.js';
import { createEnvironment, shared } from './env.js';
import { createTerrain } from './terrain.js';
import { createWater } from './water.js';
import { createCity } from './city.js';
import { createLandmarks } from './landmarks.js';
import { createPiers } from './piers.js';
import { createAgents } from './agents.js';
import { createCameraRig } from './camera.js';
import { createSigns } from './signs.js';
import { createToyPost } from './toypost.js';
import { QUALITY, createLoader, createUI } from './ui.js';

const canvas = document.getElementById('view');
const loader = createLoader();

const renderer = new WebGLRenderer({ canvas, antialias: true, powerPreference: 'high-performance' });
renderer.outputColorSpace = SRGBColorSpace;
renderer.toneMapping = ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.06;
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = PCFShadowMap;
renderer.setSize(window.innerWidth, window.innerHeight, false);

const scene = new Scene();
const camera = new PerspectiveCamera(52, window.innerWidth / window.innerHeight, 4, 60000);

async function boot() {
  const data = await loadCore((p) => loader.set(p * 0.55));

  const env = createEnvironment(scene);
  for (const mesh of createTerrain(data)) scene.add(mesh);
  loader.set(0.75);
  const water = createWater(scene);
  const landmarks = createLandmarks(scene, data);
  const piers = createPiers(scene, data);
  loader.set(0.9);

  const city = createCity(scene, data);
  const agents = createAgents(scene, data, city);
  const signs = createSigns(scene, data);
  const post = createToyPost(renderer);

  const presets = [
    ...data.manifest.viewPresets.map((preset) => ({
      id: preset.id,
      name: preset.name,
      key: preset.key,
      ...toCameraTarget(preset, data),
    })),
    ...data.manifest.landmarks.map((landmark) => ({
      id: landmark.id,
      name: landmark.name,
      key: landmark.key,
      ...toCameraTarget(landmark, data),
    })),
  ];

  const rig = createCameraRig(camera, canvas, data.sampleElevation, data.manifest.extent);
  rig.set(presets[0]);

  let quality = QUALITY.high;
  let qualityKey = 'high';
  // Small screens and integrated GPUs start a tier down; the user can override.
  if (window.devicePixelRatio > 1.9 || window.innerWidth < 900) {
    qualityKey = 'medium';
    quality = QUALITY.medium;
  }

  function applyQuality(key) {
    qualityKey = key;
    quality = QUALITY[key];
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, quality.pixelRatio));
    env.setShadowQuality(quality.shadow);
    renderer.shadowMap.enabled = quality.shadow > 0;
    city.setQuality(quality);
    water.setGlitter(key === 'low' ? 0.6 : 1);
    renderer.setSize(window.innerWidth, window.innerHeight, false);
    post.setSize();
  }

  let autoTime = true;
  let timeOfDay = 0;

  const ui = createUI({
    presets,
    onPreset(index) {
      rig.flyTo(presets[index]);
    },
    onTime(t) {
      timeOfDay = t;
      env.setTime(t);
    },
    onQuality(key) {
      applyQuality(key);
      ui.setQuality(key);
    },
    onAuto(value) {
      autoTime = value;
    },
  });
  ui.setQuality(qualityKey);
  applyQuality(qualityKey);

  // Number keys fly to presets, H goes home.
  window.addEventListener('keydown', (event) => {
    if (event.metaKey || event.ctrlKey || event.altKey) return;
    if (event.key === 'h' || event.key === 'H') {
      rig.flyTo(presets[0]);
      ui.setPresetIndex(0);
      return;
    }
    if (event.key === 'm' || event.key === 'M') {
      setStyle(style === 'toy' ? 'base' : 'toy').catch((err) =>
        console.warn('style switch failed', err)
      );
      return;
    }
    const index = presets.findIndex((preset) => preset.key && preset.key === event.key);
    if (index >= 0) {
      rig.flyTo(presets[index]);
      ui.setPresetIndex(index);
    }
  });

  window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight, false);
    post.setSize();
  });

  // Diorama mode. One switch drives every subsystem: tiles, materials, lights,
  // fog, camera rig, lens and the toy-only life. Leaving restores the exact
  // camera and the normal city, both via the ordinary streaming paths.
  const NORMAL_FOV = camera.fov;
  let style = 'base';

  async function setStyle(next) {
    if (next === style) return;
    style = next;
    const toy = next === 'toy';
    camera.fov = toy ? 18 : NORMAL_FOV;
    camera.updateProjectionMatrix();
    rig.setDiorama(toy);
    env.setToy(toy);
    agents.setToy(toy);
    signs.setVisible(toy);
    post.setEnabled(toy);
    ui.setStyle(toy);
    await city.setTier(toy ? 'toy' : 'base');
  }

  city.preload(rig.state.pivot.clone());

  // Handle for automated checks and for jumping to arbitrary coordinates.
  window.SF = {
    scene,
    camera,
    renderer,
    rig,
    city,
    agents,
    landmarks,
    piers,
    presets,
    goTo(lon, lat, distance = 900, yaw = 210, pitch = 24) {
      const [x, z] = data.project(lon, lat);
      rig.set({ x, z, distance, yaw, pitch });
    },
    // Screen-space pick, for automated inspection of what is on screen.
    pick(nx, ny) {
      const raycaster = new Raycaster();
      raycaster.setFromCamera(new Vector2(nx, ny), camera);
      return raycaster
        .intersectObjects(scene.children, true)
        .slice(0, 4)
        .map((hit) => ({
          name: hit.object.name || hit.object.parent?.name || hit.object.type,
          distance: Math.round(hit.distance),
          point: hit.point.toArray().map((v) => Math.round(v)),
        }));
    },
    setTime(t) {
      autoTime = false;
      timeOfDay = t;
      env.setTime(t);
      ui.setTime(t);
    },
    setStyle,
    get style() {
      return style;
    },
  };

  const pivotWorld = new Vector3();
  let last = performance.now();
  let frames = 0;
  let fpsAccumulator = 0;
  let fps = 0;
  let loaderDone = false;

  function frame(now) {
    // Simulation dt is clamped so a stall cannot teleport the city, but the fps
    // readout must use real wall time or it reports the clamp (20) forever.
    const elapsed = (now - last) / 1000;
    const dt = Math.min(0.05, elapsed);
    last = now;
    shared.uTime.value += dt;

    if (autoTime) {
      // A full golden-hour-to-night sweep takes about three minutes.
      timeOfDay = Math.min(1, timeOfDay + dt / 180);
      env.setTime(timeOfDay);
      ui.setTime(timeOfDay);
      if (timeOfDay >= 1) autoTime = false;
    }

    rig.update(dt);
    pivotWorld.copy(rig.state.pivot);
    city.update(dt, pivotWorld, camera.position, quality);
    agents.update(dt, pivotWorld, camera.position);
    landmarks.update();
    water.update(camera.position);
    // Clouds drift on wall time so the sky moves at the same rate whatever the
    // frame rate; the simulation clamp would slow them to a crawl below 20 fps.
    env.updateClouds(Math.min(1, elapsed));
    env.updateShadow(pivotWorld, rig.state.distance);

    signs.update(rig.state.distance, rig.state.yaw);
    // Tilt-shift + grade in diorama mode; a straight canvas render otherwise.
    post.render(scene, camera);

    frames++;
    fpsAccumulator += elapsed;
    if (fpsAccumulator > 0.5) {
      fps = frames / fpsAccumulator;
      frames = 0;
      fpsAccumulator = 0;
    }

    const progress = 0.9 + city.progress * 0.1;
    loader.set(progress);
    if (!loaderDone && city.progress > 0.985) {
      loaderDone = true;
      loader.finish();
    }

    if (ui.debugVisible) {
      const info = renderer.info;
      ui.setDebug(
        [
          `fps        ${fps.toFixed(0)}`,
          `draw calls ${info.render.calls}`,
          `triangles  ${(info.render.triangles / 1e6).toFixed(2)} M`,
          `geometries ${info.memory.geometries}`,
          `tiles      ${city.stats.cellsLoaded}/${city.stats.cellsTotal}`,
          `far groups ${city.stats.farGroups}  near ${city.stats.nearChunks}`,
          `trees      ${city.stats.trees}  lamps ${city.stats.lamps}`,
          `cars       ${agents.carCount}`,
          `altitude   ${(camera.position.y - rig.state.pivot.y).toFixed(0)} m`,
          `zoom       ${rig.state.distance.toFixed(0)} m`,
          `time       ${(timeOfDay * 100).toFixed(0)}%`,
          `style      ${style}`,
        ].join('\n')
      );
    }

    requestAnimationFrame(frame);
  }

  requestAnimationFrame(frame);
}

function toCameraTarget(preset, data) {
  const [x, z] = data.project(preset.lon, preset.lat);
  return {
    x,
    z,
    yaw: preset.camera.yaw,
    pitch: preset.camera.pitch,
    distance: preset.camera.distance,
  };
}

boot().catch((error) => {
  console.error(error);
  const message = document.createElement('div');
  message.className = 'panel';
  message.style.position = 'fixed';
  message.style.left = '50%';
  message.style.top = '50%';
  message.style.transform = 'translate(-50%,-50%)';
  message.textContent = `Failed to load the city: ${error.message}`;
  document.body.appendChild(message);
});
