// Bootstrap: load the baked city, build the scene, and open on the hero frame —
// the whole of San Francisco as a diorama, no title card, no fade-in.

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
import { createAssets } from './assets.js';
import { createPiers } from './piers.js';
import { createAgents } from './agents.js';
import { createCameraRig } from './camera.js';
import { createSigns } from './signs.js';
import { createToyPost } from './toypost.js';
import { QUALITY, createLoader, createUI } from './ui.js';
import { createContext } from './context.js';
import { createFocusOverlay } from './focus.js';
import { createContextCard, createSearch } from './cards.js';
import { createConcierge } from './concierge.js';

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

  const context = await createContext(data);
  const city = createCity(scene, data);
  // Hand-made landmark GLBs; loaded after the first paint, so the city is on
  // screen before a single byte of asset is fetched.
  const assets = createAssets(scene, data, {
    onPlaced(landmarkId, placement) {
      const gaps = landmarks.useBridgeAsset(landmarkId, placement);
      if (gaps) {
        // Traffic follows the asset's own deck, not the baked ribbon it hid.
        agents.useBridgeDeckTop(landmarkId, placement.ends);
        for (const gap of gaps) {
          console.log(
            `sf-assets: ${landmarkId} ${gap.end} approach — deck joint ` +
              `${gap.deck.horizontal.toFixed(2)} m horizontal / ${gap.deck.vertical.toFixed(2)} m vertical, ` +
              `road joint ${gap.road.horizontal.toFixed(2)} m / ${gap.road.vertical.toFixed(2)} m, ` +
              `ramp ${gap.rampLength.toFixed(0)} m from ${gap.deckTop.toFixed(1)} m deck to ` +
              `${gap.abutment.toFixed(1)} m abutment`
          );
        }
      }
    },
  });
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

  // Visual style. The diorama is the only one the app ships: it is applied
  // before the first frame and there is no key, control or URL parameter that
  // leaves it. The realistic golden-hour tier below it still exists — the tile
  // bake, the materials and the camera rig all keep both paths — but nothing
  // user-facing can select it, so `?style=golden` and friends are simply not
  // read.
  const DEFAULT_STYLE = 'toy';
  const NORMAL_FOV = camera.fov;
  let style = 'base';

  // One switch drives every subsystem: tiles, materials, lights, fog, camera
  // rig, lens and the toy-only life.
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

  // Diorama is the only style this app ships. It is applied here, before the
  // first frame is ever requested, so there is no realistic-city flash and no
  // URL parameter or key can reach the golden-hour look.
  await setStyle(DEFAULT_STYLE);

  // Number keys fly to presets, H goes home, / opens search.
  window.addEventListener('keydown', (event) => {
    if (event.metaKey || event.ctrlKey || event.altKey) return;
    const target = event.target;
    if (target instanceof HTMLInputElement || target instanceof HTMLTextAreaElement) return;
    if (event.key === '/') {
      search.focus();
      event.preventDefault();
      return;
    }
    if (event.key === 'Escape') {
      card.hide();
      overlay.clear();
      focus.entity = null;
      return;
    }
    if (event.key === 'h' || event.key === 'H') {
      rig.flyTo(presets[0]);
      ui.setPresetIndex(0);
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


  // ------------------------------------------------------------- context layer
  // One focus state drives the overlay, the card and what the concierge is told
  // the user is looking at, plus a three-deep history of what came before.

  const overlay = createFocusOverlay(scene);
  const focus = { entity: null, history: [] };

  function focusTarget(entity) {
    const ground = Math.max(0, data.sampleElevation(entity.x, entity.z));
    if (entity.kind === 'building') {
      const height = Math.max(6, style === 'toy' ? entity.toyHeight : entity.height);
      return {
        x: entity.x,
        z: entity.z,
        y: entity.baseY + height / 2,
        yaw: 210,
        pitch: style === 'toy' ? 42 : 26,
        distance: Math.max(rig.diorama ? 180 : 90, height * 2.4 + Math.max(entity.w, entity.d) * 3),
      };
    }
    if (entity.kind === 'landmark' && entity.camera) {
      return { x: entity.x, z: entity.z, y: ground + (entity.height || 60) / 2, ...entity.camera };
    }
    const distance =
      entity.kind === 'neighborhood' ? 2200 : entity.kind === 'park' ? 900 : entity.kind === 'water' ? 3000 : 500;
    return { x: entity.x, z: entity.z, yaw: 210, pitch: style === 'toy' ? 42 : 34, distance };
  }

  // The one fly-to every caller uses: presets, search hits, card buttons and the
  // concierge's camera intents all land here.
  function flyTo(target, { duration = 2.2 } = {}) {
    rig.flyTo(target, duration);
  }

  function selectEntity(entity, { fly = false } = {}) {
    if (!entity) return;
    focus.entity = entity;
    focus.history = [entity, ...focus.history.filter((e) => e.id !== entity.id)].slice(0, 3);
    overlay.show(entity, {
      toy: style === 'toy',
      groundY: Math.max(0, data.sampleElevation(entity.x, entity.z)),
    });
    card.show(entity, {
      neighborhood: context.neighborhoodAt(entity.x, entity.z),
      recent: focus.history.slice(1),
    });
    if (fly) flyTo(focusTarget(entity));
  }

  const card = createContextCard({
    onFly: (entity) => flyTo(focusTarget(entity)),
    onAsk: (entity) => concierge.ask(`Tell me about ${entity.title}.`),
    onSelectHistory: (entity) => selectEntity(entity),
  });

  const search = createSearch({
    onPick: async (entry) => {
      if (entry.t === 'building') {
        const entity = await context.loadBuilding(Number(entry.id.slice(2)), entry.x, entry.z);
        if (entity) {
          selectEntity(entity, { fly: true });
          return;
        }
      }
      const entity = {
        kind: entry.t === 'view' ? 'landmark' : entry.t,
        id: entry.id,
        title: entry.n,
        name: entry.n,
        x: entry.x,
        z: entry.z,
        source: 'datasf',
        confidence: 3,
      };
      selectEntity(entity, { fly: true });
    },
    onEmpty: (query) => concierge.ask(query),
  });

  search.input.addEventListener('input', async () => {
    const query = search.input.value.trim();
    if (!query) {
      search.close();
      return;
    }
    search.render(await context.search(query), query);
  });

  const concierge = createConcierge({
    viewerContext() {
      const nhood = context.neighborhoodAt(rig.state.pivot.x, rig.state.pivot.z);
      return {
        camera: {
          x: Math.round(rig.state.pivot.x),
          z: Math.round(rig.state.pivot.z),
          distance: Math.round(rig.state.distance),
          yaw: Math.round((rig.state.yaw * 180) / Math.PI),
        },
        style,
        neighborhood: nhood?.name || null,
        focus: focus.entity
          ? {
              kind: focus.entity.kind,
              id: focus.entity.id,
              title: focus.entity.title,
              cat: focus.entity.cat ?? null,
              x: Math.round(focus.entity.x),
              z: Math.round(focus.entity.z),
            }
          : null,
      };
    },
    // Intents are data, never scene access: the client decides what each one is
    // allowed to move.
    async applyIntent(intent) {
      if (intent.type === 'set_camera') {
        flyTo({
          x: clampCoord(intent.x, data.manifest.extent.minX, data.manifest.extent.maxX),
          z: clampCoord(intent.z, data.manifest.extent.minZ, data.manifest.extent.maxZ),
          yaw: Number.isFinite(intent.yaw) ? intent.yaw : 210,
          pitch: Math.min(80, Math.max(8, Number.isFinite(intent.pitch) ? intent.pitch : 32)),
          distance: Math.min(12000, Math.max(80, Number.isFinite(intent.distance) ? intent.distance : 700)),
        });
        return;
      }
      if (intent.type === 'focus_entity' || intent.type === 'highlight') {
        if (typeof intent.id === 'string' && intent.id.startsWith('b:')) {
          const entity = await context.loadBuilding(Number(intent.id.slice(2)), intent.x, intent.z);
          if (entity) {
            selectEntity(entity, { fly: intent.type === 'focus_entity' });
            return;
          }
        }
        if (Number.isFinite(intent.x) && Number.isFinite(intent.z)) {
          selectEntity(
            {
              kind: intent.kind || 'landmark',
              id: intent.id || `point:${intent.x}_${intent.z}`,
              title: intent.title || 'Selected place',
              x: intent.x,
              z: intent.z,
              source: intent.source || 'osm',
              confidence: 2,
            },
            { fly: intent.type === 'focus_entity' }
          );
        }
      }
    },
  });

  // Click to inspect: a press that neither travels nor lingers is a pick, so
  // grab-panning the ground never opens a card.
  const pickRay = new Raycaster();
  const pickPointer = new Vector2();
  const groundPoint = new Vector3();
  let press = null;

  canvas.addEventListener('pointerdown', (event) => {
    if (event.button !== 0) return;
    press = { x: event.clientX, y: event.clientY, at: performance.now() };
  });

  canvas.addEventListener('pointerup', async (event) => {
    if (event.button !== 0 || !press) return;
    const moved = Math.hypot(event.clientX - press.x, event.clientY - press.y);
    const held = performance.now() - press.at;
    press = null;
    if (moved > 6 || held > 400) return;
    const rect = canvas.getBoundingClientRect();
    pickPointer.set(
      ((event.clientX - rect.left) / rect.width) * 2 - 1,
      -((event.clientY - rect.top) / rect.height) * 2 + 1
    );
    pickRay.setFromCamera(pickPointer, camera);
    const hasGround = rig.screenToGround(pickPointer.x, pickPointer.y, groundPoint);
    const entity = await context.pick(pickRay.ray.origin, pickRay.ray.direction, hasGround ? groundPoint : null, {
      toy: style === 'toy',
    });
    if (entity) selectEntity(entity);
  });

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
    assets,
    get style() {
      return style;
    },
    context,
    // Pick whatever is under a normalised screen point, the same way a click does.
    async pickEntity(nx = 0, ny = 0) {
      pickPointer.set(nx, ny);
      pickRay.setFromCamera(pickPointer, camera);
      const hasGround = rig.screenToGround(nx, ny, groundPoint);
      return context.pick(pickRay.ray.origin, pickRay.ray.direction, hasGround ? groundPoint : null, {
        toy: style === 'toy',
      });
    },
    select: selectEntity,
    search: (query) => context.search(query),
    get focus() {
      return focus.entity;
    },
  };

  const pivotWorld = new Vector3();
  let last = performance.now();
  let frames = 0;
  let fpsAccumulator = 0;
  let fps = 0;
  let loaderDone = false;
  let assetsRequested = false;

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
    context.prefetch(pivotWorld);
    overlay.update(dt);
    city.update(dt, pivotWorld, camera.position, quality);
    agents.update(dt, pivotWorld, camera.position);
    landmarks.update();
    assets.update();
    water.update(camera.position);
    // Clouds drift on wall time so the sky moves at the same rate whatever the
    // frame rate; the simulation clamp would slow them to a crawl below 20 fps.
    env.updateClouds(Math.min(1, elapsed));
    env.updateShadow(pivotWorld, rig.state.distance);
    env.updateNightSky(camera);

    signs.update(rig.state.distance, rig.state.yaw);
    // Tilt-shift + grade in diorama mode; a straight canvas render otherwise.
    post.render(scene, camera);

    // Landmark assets are fetched only once the city is actually on screen.
    if (!assetsRequested) {
      assetsRequested = true;
      assets.load();
    }

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

function clampCoord(value, min, max) {
  if (!Number.isFinite(value)) return (min + max) / 2;
  return Math.min(max, Math.max(min, value));
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
