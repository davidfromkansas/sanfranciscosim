// Bootstrap: load the baked city, build the scene, and open on the hero frame —
// the whole of San Francisco as a diorama. The boot curtain (boot.js) covers
// the load with fog and lifts onto the finished frame; behind it the city has
// always been building, and there is still no style transition of any kind.

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
import { createLiveFerries } from './ferries.js';
import { createLiveMuni } from './muni.js';
import { createCameraRig } from './camera.js';
import { createSigns } from './signs.js';
import { createToyPost } from './toypost.js';
import { QUALITY, QUALITY_LADDER, createUI } from './ui.js';
import { createBootScreen } from './boot.js';
import { createGovernor } from './governor.js';
import { createContext } from './context.js';
import { createFocusOverlay } from './focus.js';
import { createContextCard, createSearch } from './cards.js';
import { createConcierge } from './concierge.js';
import { createSkyClock } from './sky-clock.js';
import { createWeather } from './weather.js';
import { createClouds } from './clouds.js';
import { createRain } from './rain.js';
import { createFogBanks } from './fogbanks.js';
import { localDayStart, moonPosition, skySnapshot, sunPosition } from '../../api/_lib/astro.mjs';

const canvas = document.getElementById('view');
const bootScreen = createBootScreen();

// antialias: false is deliberate (PERF-PLAN #7): the diorama always renders
// through the post pass's offscreen target, so canvas MSAA smoothed a buffer
// nobody sees. The samples live on the post target instead (toypost.js).
const renderer = new WebGLRenderer({ canvas, antialias: false, powerPreference: 'high-performance' });
renderer.outputColorSpace = SRGBColorSpace;
renderer.toneMapping = ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.06;
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = PCFShadowMap;
renderer.setSize(window.innerWidth, window.innerHeight, false);

// Mobile browsers confiscate the GL context under memory pressure or after an
// app switch. preventDefault on the lost event is what makes the context
// restorable at all; three re-uploads everything it owns on the restored
// event, and the frame loop sits out the gap so the governor and simulation
// never see the dead time.
let contextLost = false;
canvas.addEventListener('webglcontextlost', (event) => {
  event.preventDefault();
  contextLost = true;
  console.warn('WebGL context lost — pausing until the browser restores it');
});
canvas.addEventListener('webglcontextrestored', () => {
  contextLost = false;
  console.warn('WebGL context restored — resuming');
});

const scene = new Scene();
const camera = new PerspectiveCamera(52, window.innerWidth / window.innerHeight, 4, 60000);

async function boot() {
  const data = await loadCore((p) => bootScreen.core(p * 0.82));

  const env = createEnvironment(scene);
  const terrain = createTerrain(data);
  for (const mesh of terrain.meshes) scene.add(mesh);
  bootScreen.core(0.9);
  const water = createWater(scene);
  const landmarks = createLandmarks(scene, data);
  const piers = createPiers(scene, data);
  bootScreen.core(1);

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
    onUnloaded(landmarkId) {
      landmarks.restoreCodeBuilt(landmarkId);
    },
  });
  const agents = createAgents(scene, data, city);
  // Real WETA vessels from /api/ferries; falls back to the procedural ferries.
  const ferries = createLiveFerries(scene, data, agents);
  // The live weather field. Created before the clock so the card can read it
  // on its very first render.
  const weather = createWeather({ project: data.project });
  // ?weather=<preset> pins a showcase state at load, so a dramatic view can be
  // linked to rather than typed into a console. Live weather is still the
  // default and there is no control in the UI for this — the city's promise is
  // that what you see is real, and only an explicit URL opts out of it.
  // Unknown values are ignored rather than erroring: a bad link shows the real
  // city, which is the right failure.
  function applyWeatherFromUrl() {
    let requested = null;
    try {
      requested = new URLSearchParams(window.location.search).get('weather');
    } catch {
      return null;
    }
    if (!requested) return null;
    const name = String(requested).toLowerCase();
    if (!weather.presetNames.includes(name)) {
      console.warn(`?weather=${requested} is not a known preset (${weather.presetNames.join(', ')}) — showing live weather`);
      return null;
    }
    weather.setOverride({ preset: name });
    // A linked state should be there on arrival, not ease in over a minute.
    weather.settle();
    return name;
  }

  // Toy clouds read the same field the shadows do, so what floats overhead and
  // what darkens the ground always agree.
  const clouds = createClouds(scene, { sampleAt: weather.sampleAt });
  // Rain falls where the field says it is raining, in a box around the camera.
  const rain = createRain(scene, { sampleAt: weather.sampleAt });
  // Karl with a silhouette. The shader fog dissolves the city with distance;
  // these are the vapour you can actually see, placed by the same field.
  const fogBanks = createFogBanks(scene, { sampleAt: weather.sampleAt });
  // Real Muni buses from /api/muni; when the feed is away this layer is simply
  // empty — the procedural road traffic never depended on it.
  const muni = createLiveMuni(scene, data);
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

  function readQualityPreference() {
    try {
      const saved = window.localStorage.getItem('sf.quality');
      if (saved === 'auto' || QUALITY[saved]) return saved;
    } catch {
      // Safari private windows can reject both reads and writes.
    }
    return 'auto';
  }

  function writeQualityPreference(key) {
    try {
      window.localStorage.setItem('sf.quality', key);
    } catch {
      // A pinned quality still applies for this session when storage is unavailable.
    }
  }

  function applyQuality(key) {
    qualityKey = key;
    quality = QUALITY[key];
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, quality.pixelRatio));
    env.setShadowQuality(quality.shadow);
    renderer.shadowMap.enabled = quality.shadow > 0;
    // Every visual subsystem answers to the tier (PERF-PLAN #6): the governor
    // pulls one lever and the whole frame gets cheaper, not just the pixels.
    city.setQuality(quality, key);
    water.setGlitter(key === 'low' ? 0.6 : 1);
    water.setQuality(key);
    agents.setQuality(key);
    terrain.setQuality(key);
    clouds.setQuality(key);
    rain.setQuality(key);
    fogBanks.setQuality(key);
    post.setSamples(quality.samples);
    renderer.setSize(window.innerWidth, window.innerHeight, false);
    post.setSize();
  }

  const qualityPreference = readQualityPreference();
  const governor = createGovernor({
    tiers: QUALITY,
    ladder: QUALITY_LADDER,
    initialTier: qualityPreference === 'auto' ? qualityKey : qualityPreference,
    mode: qualityPreference,
    apply: applyQuality,
    isFlying: () => rig.flying,
    readStreaming: () => city.stats,
  });
  if (qualityPreference !== 'auto') qualityKey = qualityPreference;
  quality = QUALITY[qualityKey];

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

  // --------------------------------------------------------------------- sky
  // The scene runs on San Francisco's wall clock: no sweep, no slider. The
  // astronomy is recomputed once a second from the render loop's own timer.
  // `clockOverride` freezes that clock for screenshots and QA; `skyBroken`
  // latches the one-warning fallback if the maths ever throws.
  let clockOverride = null;
  let skyBroken = false;
  let sky = null;
  let skyAccumulator = 0;

  function tickSky() {
    if (skyBroken) return;
    const ms = clockOverride === null ? Date.now() : clockOverride;
    try {
      const sunAt = sunPosition(ms);
      const moonAt = moonPosition(ms);
      env.setSky({
        sunEl: sunAt.elevation,
        sunAz: sunAt.azimuth,
        moonEl: moonAt.elevation,
        moonAz: moonAt.azimuth,
        moonIllum: moonAt.illumination,
      });
      sky = skySnapshot(ms);
    } catch (error) {
      // Rule 3: degrade to something pleasant, warn once, never a black scene.
      skyBroken = true;
      sky = null;
      console.warn('sky: astronomy unavailable, holding a fixed golden hour', error);
      env.setTime(0.12);
    }
  }
  tickSky();
  const skyClock = createSkyClock({ read: () => sky, readWeather: () => weather });
  // After the first poll has had a moment: an override set before any payload
  // arrives would be overwritten by it.
  let urlWeather = applyWeatherFromUrl();
  if (urlWeather) setTimeout(() => { urlWeather = applyWeatherFromUrl(); skyClock.update(); }, 2500);

  const ui = createUI({
    presets,
    onPreset(index) {
      rig.flyTo(presets[index]);
    },
    onQuality(key) {
      writeQualityPreference(key);
      governor.setMode(key);
      if (key !== 'auto') applyQuality(key);
      ui.setQuality(key);
    },
  });
  ui.setQuality(qualityPreference);
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
    if (entity.kind === 'vessel') {
      return { x: entity.x, z: entity.z, y: 20, yaw: 210, pitch: style === 'toy' ? 30 : 22, distance: 300 };
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
        // Live-fleet ids from the muni feed ("SF:8632"): the concierge saw them
        // in live_data and the bus layer has the current position.
        if (typeof intent.id === 'string' && intent.id.startsWith('SF:')) {
          const bus = muni.busEntity(intent.id);
          if (bus) {
            selectEntity(bus, { fly: intent.type === 'focus_entity' });
            return;
          }
        }
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

  // A selected ferry keeps sailing, so the highlight follows it every frame and
  // the card re-reads the feed a few times a minute instead of freezing the
  // arrival time it was opened with.
  let vesselCardAge = 0;
  function trackVessel(dt) {
    const selected = focus.entity;
    if (selected?.kind !== 'vessel' && selected?.kind !== 'transit') return;
    const fresh =
      selected.kind === 'vessel' ? ferries.vesselEntity(selected.id) : muni.busEntity(selected.id);
    if (!fresh) return;
    focus.entity = fresh;
    overlay.show(fresh, { toy: style === 'toy', groundY: 0 });
    vesselCardAge += dt;
    if (vesselCardAge < 5) return;
    vesselCardAge = 0;
    if (card.entity?.id === fresh.id) card.show(fresh, { recent: focus.history.slice(1) });
  }

  // Live ferries win over the city behind them: they are small, they move, and
  // the water pick underneath is the least interesting answer on screen.
  async function pickAt(nx, ny, hasGround) {
    pickPointer.set(nx, ny);
    pickRay.setFromCamera(pickPointer, camera);
    const vessel = ferries.pickVessel(pickRay.ray.origin, pickRay.ray.direction);
    if (vessel) return vessel;
    const bus = muni.pickBus(pickRay.ray.origin, pickRay.ray.direction);
    if (bus) return bus;
    return context.pick(pickRay.ray.origin, pickRay.ray.direction, hasGround ? groundPoint : null, {
      toy: style === 'toy',
    });
  }

  canvas.addEventListener('pointerdown', (event) => {
    // A second finger means a pinch/twist, not a tap — whatever this press was,
    // it must not pick on release.
    if (event.pointerType === 'touch' && press) {
      press = null;
      return;
    }
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
    const entity = await pickAt(pickPointer.x, pickPointer.y, hasGround);
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
    ferries,
    clouds,
    rain,
    fogBanks,
    muni,
    governor,
    boot: bootScreen,
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
    get sky() {
      return sky;
    },
    // The eased weather state. Debug only, exactly like setClock: no UI, no
    // URL parameter, and the model can never set it.
    get weather() {
      return weather.snapshot();
    },
    // Read the eased field at a world position, the same way the shaders do.
    // The orientation of that lookup is the easiest thing in this feature to
    // get silently wrong, so it is checkable: sampleWeather at the Sunset and
    // at Bayview must disagree the way the feed's districts do.
    sampleWeather(x, z, key = 'fog') {
      return weather.sampleAt(x, z, key);
    },
    // Skip the 60 s ease and jump to the incoming field — for screenshots and
    // automated checks, which have no time (or no frame loop) to wait it out.
    // Dial cloud size and density against the running scene:
    //   SF.tuneClouds({ size: 1.4, density: 1.2 })  ->  then SF.cloudCoverage()
    // Dial the fog banks: size, opacity and how readily they appear.
    tuneBanks(patch) {
      return fogBanks.tune(patch);
    },
    // Fraction of the ground the fog banks actually cover. Counting them hides
    // the only number that matters.
    bankCoverage() {
      return fogBanks.coverage();
    },
    tuneClouds(patch) {
      return clouds.tune(patch);
    },
    // The fraction of sky the low deck actually covers. Counting instances
    // hides this: 39 clouds sounded fine while covering 8.7% of the sky.
    cloudCoverage() {
      return clouds.coverage();
    },
    settleWeather() {
      weather.settle();
      skyClock.update();
      return weather.snapshot();
    },
    // A partial patch merges onto the live field; null returns to live.
    // SF.setWeather({ preset: 'karl' | 'storm' | 'clear' | 'smoke' }) gives the
    // canonical demo states, which is how the rare ones get QA'd at all.
    setWeather(patch) {
      weather.setOverride(patch === undefined ? null : patch);
      skyClock.update();
      return weather.snapshot();
    },
    // null resumes live San Francisco time; a number is epoch ms, a string is
    // anything Date.parse understands ('2026-08-10T02:00:00-07:00').
    setClock(value) {
      if (value === null || value === undefined) clockOverride = null;
      else {
        const ms = typeof value === 'number' ? value : Date.parse(value);
        if (!Number.isFinite(ms)) throw new Error(`SF.setClock: cannot read ${value}`);
        clockOverride = ms;
      }
      skyBroken = false;
      tickSky();
      skyClock.update();
      return sky;
    },
    // Deprecated: the old 0 to 1 golden-hour sweep. Kept so older scripts keep
    // running; it now just freezes the clock around sunset.
    setTime(t) {
      console.warn('SF.setTime is deprecated — use SF.setClock(msOrIso), or SF.setClock(null) for live time');
      // Midnight in San Francisco, not in whatever zone the browser is in.
      const midnight = localDayStart(clockOverride === null ? Date.now() : clockOverride);
      // t = 0 is the golden hour, t = 1 is a couple of hours after sunset.
      return this.setClock(midnight + (19 + Math.min(1, Math.max(0, t)) * 2.5) * 3600 * 1000);
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
      return pickAt(nx, ny, rig.screenToGround(nx, ny, groundPoint));
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
  let assetsRequested = false;

  function frame(now) {
    if (contextLost) {
      // Keep the loop alive but idle: rendering into a lost context is a
      // no-op at best, and simulation/governor time must not accumulate.
      last = now;
      requestAnimationFrame(frame);
      return;
    }
    // Simulation dt is clamped so a stall cannot teleport the city, but the fps
    // readout must use real wall time or it reports the clamp (20) forever.
    const elapsed = (now - last) / 1000;
    const dt = Math.min(0.05, elapsed);
    last = now;
    shared.uTime.value += dt;

    // One astronomy update a second, on this loop's own clock: no second rAF,
    // and no work at all in the other frames.
    skyAccumulator += elapsed;
    if (skyAccumulator >= 1) {
      skyAccumulator = 0;
      if (clockOverride === null) tickSky();
    }

    rig.update(dt);
    governor.update(elapsed * 1000);
    pivotWorld.copy(rig.state.pivot);
    context.prefetch(pivotWorld);
    overlay.update(dt);
    city.update(dt, pivotWorld, camera.position, quality);
    agents.update(dt, pivotWorld, camera.position);
    ferries.update(dt);
    // Weather eases on wall time for the same reason the clouds do: the
    // simulation clamp would stall the transition below 20 fps.
    weather.update(Math.min(1, elapsed));
    clouds.update(Math.min(1, elapsed));
    // The pivot, not the camera: rain has to fall where the camera is looking.
    rain.update(dt, pivotWorld);
    fogBanks.update(Math.min(1, elapsed));
    muni.update(dt, camera);
    trackVessel(dt);
    landmarks.update();
    assets.update(camera.position, dt);
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

    // The curtain owns its own phase weighting and reveal gate (boot.js); this
    // is both its proof that the renderer is painting and its stream numbers.
    bootScreen.rendered(city.stats);

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
          `ferries    ${ferries.count}${ferries.live ? ' live' : ' procedural'}`,
          `muni       ${muni.count}${muni.live ? ` live (${muni.onShapeCount} on-route${muni.degraded ? ', degraded' : ''})` : ' off'}`,
          `altitude   ${(camera.position.y - rig.state.pivot.y).toFixed(0)} m`,
          `zoom       ${rig.state.distance.toFixed(0)} m`,
          `time       ${sky ? sky.localTime : 'fallback'}${clockOverride === null ? '' : ' (held)'}`,
          `sun        ${sky ? `${sky.sun.elevationDeg.toFixed(0)}° el ${sky.sun.azimuthDeg.toFixed(0)}° az` : '—'}`,
          `night      ${shared.uNight.value.toFixed(2)}`,
          `style      ${style}`,
          `quality    ${governor.mode === 'auto' ? `Auto (${governor.tier})` : governor.tier}`,
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
  // Never leave the user behind the fog: the curtain reports the failure on its
  // own bar and then lifts, so the message below is readable.
  bootScreen.fail(error.message);
  const message = document.createElement('div');
  message.className = 'panel';
  message.style.position = 'fixed';
  message.style.left = '50%';
  message.style.top = '50%';
  message.style.transform = 'translate(-50%,-50%)';
  message.textContent = `Failed to load the city: ${error.message}`;
  document.body.appendChild(message);
});
