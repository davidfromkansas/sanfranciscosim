// Tile streaming + LOD. Three tiers of work:
//   * FAR  — one merged prism mesh per 2 km super-cell, built once, always on.
//   * NEAR — full footprint extrusion per 1 km chunk inside ~2.4 km, built on
//            demand, dither cross-faded against the far tier's matching quadrant.
//   * GROUND — street ribbons + landcover merged per super-cell, plus instanced
//            trees and street lamps.
// Everything is produced in workers from binary blobs; the main thread only
// uploads buffers.

import {
  BufferAttribute,
  BufferGeometry,
  Color,
  ConeGeometry,
  CylinderGeometry,
  DynamicDrawUsage,
  IcosahedronGeometry,
  InstancedBufferAttribute,
  InstancedMesh,
  Matrix4,
  Mesh,
  MeshBasicMaterial,
  Object3D,
  SphereGeometry,
  Vector3,
} from 'three';
import { mergeGeometries } from 'three/addons/utils/BufferGeometryUtils.js';
import {
  alignPoolToGround,
  createBuildingMaterial,
  createFarBuildingMaterial,
  createGroundMaterial,
  createLampPoolGeometry,
  createLampPoolMaterial,
  createToyBuildingMaterial,
  createTreeMaterial,
} from './materials.js';
import { shared } from './env.js';
import { fetchTileBin, tileUrl } from './data.js';
import { catalogForWorker } from './kitplan.js';
import { createKitLoader, loadKitIndex } from './kitassets.js';
import { createKitFleet } from './kitfleet.js';
import { landmarkExclusions, loadKitZones } from './kitzones.js';
import { GROUP_LIMIT, createStreetHints, createStreetKitFleet, loadStreetKit } from './streetkit.js';
import { loadBusStops, stopsInBounds } from './munistops.js';

const GROUP = 2000;
const CHUNK = 1000;
const NEAR_ENTER = 2400;
const NEAR_EXIT = 3100;
const TREE_RANGE = 3400;
const LAMP_RANGE = 2600;
// The pool of light a lamp throws on the road. Shorter than LAMP_RANGE: the
// lamp head still reads as a bright dot from far off, but the pool is a
// ground-level detail that stops earning its fill rate well before that.
const POOL_RANGE = 1500;
const POOL_RADIUS = 7.5; // m; a ~6.5 m lamp lights a little wider than it is tall
const POOL_LIFT = 0.08; // m above the road, clear of z-fighting with the ribbon
// Kerb faces, centre dashes and zebras: built per ground group while the camera
// is near it, dropped again behind. Sub-pixel at this range, so nothing pops.
const DETAIL_ENTER = 1800;
const DETAIL_EXIT = 2400;
const FADE_SPEED = 2.2; // per second
const STREETS_MAGIC = 0x53465301; // "SFS1", mirrored from pipeline/lib/binio.mjs
const LANDCOVER_MAGIC = 0x4c465301; // "SFL1"
const TREE_SPECIES = [
  { scale: [1, 1, 1], tint: [1, 1, 1] },
  { scale: [0.72, 1.35, 0.72], tint: [0.78, 0.5, 0.78] },
  { scale: [0.66, 1.55, 0.66], tint: [1.15, 0.7, 1] },
  { scale: [0.82, 1.2, 0.82], tint: [1.35, 0.9, 1.05] },
];

class WorkerPool {
  constructor(size) {
    this.workers = [];
    this.queue = [];
    this.pending = new Map();
    this.nextId = 1;
    for (let i = 0; i < size; i++) {
      const worker = new Worker(new URL('./city.worker.js', import.meta.url), { type: 'module' });
      worker.onmessage = (event) => {
        const entry = this.pending.get(event.data.id);
        this.pending.delete(event.data.id);
        worker.busy = false;
        if (entry) {
          if (event.data.type === 'error') entry.reject(new Error(event.data.message));
          else entry.resolve(event.data);
        }
        this.drain();
      };
      worker.busy = false;
      this.workers.push(worker);
    }
  }

  run(message, transfer = []) {
    return new Promise((resolve, reject) => {
      const id = this.nextId++;
      this.queue.push({ message: { ...message, id }, transfer, resolve, reject, id });
      this.drain();
    });
  }

  drain() {
    for (const worker of this.workers) {
      if (worker.busy || this.queue.length === 0) continue;
      const job = this.queue.shift();
      worker.busy = true;
      this.pending.set(job.id, job);
      worker.postMessage(job.message, job.transfer);
    }
  }

  get load() {
    return this.queue.length + this.pending.size;
  }
}

function groupKeyFor(x, z, extent) {
  const gx = Math.floor((x - extent.minX) / GROUP);
  const gz = Math.floor((z - extent.minZ) / GROUP);
  return `${gx}_${gz}`;
}

function makeAttributes(geometry, data) {
  geometry.setAttribute('position', new BufferAttribute(data.positions, 3));
  geometry.setAttribute('normal', new BufferAttribute(data.normals, 3));
  geometry.setAttribute('color', new BufferAttribute(data.colors, 3, true));
  geometry.setIndex(new BufferAttribute(data.indices, 1));
}

// three keeps a CPU copy of every array it uploads; for the fully-built city
// that is hundreds of MB the app never reads again — the exact duplication
// that pushes iOS Safari past its memory watchdog. Static city geometry drops
// its arrays the moment the GPU has them (bounds are computed before upload;
// picking never raycasts these meshes — context.pick works off baked cell
// data; only the SF.pick debug helper loses these tiers). Rebuilds create
// fresh geometry from blobs, so eviction and tier swaps are unaffected.
function releaseArray() {
  this.array = null;
}
function releaseAfterUpload(geometry) {
  for (const attribute of Object.values(geometry.attributes)) attribute.onUpload(releaseArray);
  if (geometry.index) geometry.index.onUpload(releaseArray);
  return geometry;
}

function treeArchetype() {
  const parts = [];
  const trunk = new CylinderGeometry(0.34, 0.46, 3.2, 5, 1);
  trunk.translate(0, 1.6, 0);
  const trunkColors = new Float32Array(trunk.attributes.position.count * 3);
  for (let i = 0; i < trunk.attributes.position.count; i++) {
    trunkColors[i * 3] = 0.29;
    trunkColors[i * 3 + 1] = 0.21;
    trunkColors[i * 3 + 2] = 0.15;
  }
  trunk.setAttribute('color', new BufferAttribute(trunkColors, 3));
  parts.push(trunk);

  const canopy = new ConeGeometry(3.1, 8.4, 7, 2);
  canopy.translate(0, 7.4, 0);
  const canopyColors = new Float32Array(canopy.attributes.position.count * 3);
  const pos = canopy.attributes.position;
  for (let i = 0; i < pos.count; i++) {
    const shade = 0.78 + (pos.getY(i) / 12) * 0.4;
    canopyColors[i * 3] = 0.17 * shade;
    canopyColors[i * 3 + 1] = 0.33 * shade;
    canopyColors[i * 3 + 2] = 0.16 * shade;
  }
  canopy.setAttribute('color', new BufferAttribute(canopyColors, 3));
  parts.push(canopy);

  const merged = mergeGeometries(parts, false);
  for (const part of parts) part.dispose();
  return merged;
}

// Toy trees: a lollipop. Low-detail icosahedron canopy on a stubby trunk, in
// saturated model-railway greens. The canopy is non-indexed, so the trunk is
// converted to match: mergeGeometries returns null on a mixed list.
function toyTreeArchetype() {
  const parts = [];
  const trunk = new CylinderGeometry(0.55, 0.7, 3.4, 6, 1).toNonIndexed();
  trunk.translate(0, 1.7, 0);
  const trunkColors = new Float32Array(trunk.attributes.position.count * 3);
  for (let i = 0; i < trunk.attributes.position.count; i++) {
    trunkColors[i * 3] = 0.42;
    trunkColors[i * 3 + 1] = 0.28;
    trunkColors[i * 3 + 2] = 0.18;
  }
  trunk.setAttribute('color', new BufferAttribute(trunkColors, 3));
  parts.push(trunk);

  const canopy = new IcosahedronGeometry(4.2, 1);
  canopy.scale(1, 0.92, 1);
  canopy.translate(0, 7.2, 0);
  const canopyColors = new Float32Array(canopy.attributes.position.count * 3);
  const pos = canopy.attributes.position;
  for (let i = 0; i < pos.count; i++) {
    const shade = 0.86 + (pos.getY(i) / 14) * 0.28;
    canopyColors[i * 3] = 0.24 * shade;
    canopyColors[i * 3 + 1] = 0.62 * shade;
    canopyColors[i * 3 + 2] = 0.27 * shade;
  }
  canopy.setAttribute('color', new BufferAttribute(canopyColors, 3));
  parts.push(canopy);

  const merged = mergeGeometries(parts, false);
  for (const part of parts) part.dispose();
  return merged;
}

export function createCity(scene, data) {
  const { manifest, indexes } = data;
  const extent = manifest.extent;
  const palette = manifest.palette.map((p) => p.color.map((c) => Math.round(c * 255)));
  const pool = new WorkerPool(Math.max(2, Math.min(6, (navigator.hardwareConcurrency || 4) - 1)));

  // LRU: tile blobs are only inputs to geometry builds, and the browser's
  // immutable HTTP cache makes a refetch near-free — holding every cell's raw
  // buffer forever is what grows long sessions toward the mobile tab-kill
  // threshold. `blobsSeen` keeps the tiles readout monotonic under eviction.
  const blobCache = new Map(); // `${kind}:${cellKey}` -> ArrayBuffer, oldest first
  const BLOB_CACHE_MAX = 200;
  const blobsSeen = new Set();
  const brokenStreets = new Set(); // warned once per unusable street tile
  const brokenLandcover = new Set(); // warned once per unusable landcover tile
  const groups = new Map();
  const chunks = new Map();
  const stats = {
    cellsLoaded: 0,
    cellsTotal: 0,
    nearChunks: 0,
    // Groups in the grid. farGroups/groundGroups count the meshes actually in
    // the scene, so the ratio against this is "how much of the frame is built"
    // — which is what the boot curtain's reveal gate watches. Cell counts
    // cannot answer that: most cells belong to tiers the opening view never
    // draws.
    groupsTotal: 0,
    farGroups: 0,
    groundGroups: 0,
    groundDetail: 0,
    trees: 0,
    lamps: 0,
    kitInstances: 0,
    kitPieceTypes: 0,
    kitPlaced: 0,
    kitConsidered: 0,
    furniture: 0,
    furnitureDraws: 0,
  };
  const paths = [];
  // Two layers walk the street centrelines now — procedural traffic and the
  // resident population — so this is a broadcast rather than a single slot.
  const pathListeners = [];
  const onPathsReady = (list) => {
    for (const listener of pathListeners) listener(list);
  };

  const groundMaterial = createGroundMaterial();
  const quality = { windows: 1, poolScale: 1, poolStrength: 1 };
  const treeMaterial = createTreeMaterial();
  const lampMaterial = new MeshBasicMaterial({ color: new Color(1.0, 0.82, 0.55), transparent: true, opacity: 0 });
  const lampPoolMaterial = createLampPoolMaterial();
  const treeGeometry = treeArchetype();
  const toyTreeGeometry = toyTreeArchetype();
  const lampGeometry = new SphereGeometry(0.9, 6, 4);
  const lampPoolGeometry = createLampPoolGeometry();

  // Diorama tier. `toy` holds the lazily fetched toy index (palette + street
  // classes); the cell grid, hysteresis and bookkeeping are shared with the base
  // tier — only the URLs, the worker job and the materials change.
  let tier = 'base';
  let toy = null;
  let toyPalette = null;
  const TIERS = {
    base: { buildings: 'buildings', streets: 'streets', landcover: 'landcover' },
    toy: { buildings: 'toy', streets: 'toystreets', landcover: 'toyland' },
  };
  const kinds = () => TIERS[tier];

  // --------------------------------------------------------------- the kit ---
  // The hand-made building kit rides on the diorama tier: the worker plans which
  // footprints a piece fits, this side batches them, and every footprint it does
  // not claim is still extruded procedurally by the same worker pass. If the kit
  // index, the zone raster or a piece fails to load, `kit.enabled` stays false
  // and the city is exactly the procedural one, with one warning.
  const kit = {
    enabled: false,
    catalog: null,
    loader: null,
    fleet: null,
    zones: null,
    exclusions: null,
    disabled: new Set(),
    warned: false,
  };
  const kitGroup = new Object3D();
  kitGroup.name = 'kit-fleet';
  scene.add(kitGroup);

  // ------------------------------------------------------- the street kit ---
  // Layer 2 furniture. Lives on the near tier only: it is built with the kerb
  // and marking detail for a ground group and dropped with it. If anything in
  // the kit fails to load, `streetkit.fleet` stays null and the streets are the
  // layer 1 streets, with one warning.
  const streetkit = { fleet: null, hints: null, exclusions: null, warned: false };
  // One fetch+parse of the baked stop table, shared with the marker layer.
  const busStopsReady = loadBusStops();
  const streetkitReady = (async () => {
    try {
      const loaded = await loadStreetKit();
      streetkit.fleet = createStreetKitFleet(scene, loaded, data.sampleElevation);
      // The governor may already have picked a tier before the kit finished
      // loading; a fresh fleet starts at whatever is current.
      if (quality.tier) streetkit.fleet.setQuality(quality.tier);
      streetkit.hints = createStreetHints(manifest, data.contextCells);
      streetkit.exclusions = landmarkExclusions(manifest, data.project);
    } catch (error) {
      streetkit.warned = true;
      console.warn(`[streetkit] unavailable, streets stay bare: ${error.message}`);
    }
  })();

  const kitReady = (async () => {
    try {
      const [catalog, zones] = await Promise.all([loadKitIndex(), loadKitZones(extent)]);
      kit.catalog = catalog;
      kit.zones = zones;
      kit.exclusions = landmarkExclusions(manifest, data.project);
      kit.loader = createKitLoader(catalog, {
        onWarn: (message) => console.warn(`[kit] ${message}`),
      });
      kit.fleet = createKitFleet(kitGroup, catalog, kit.loader);
      kit.enabled = true;
    } catch (error) {
      console.warn(`[kit] unavailable, using procedural buildings only: ${error.message}`);
    }
  })();

  // Street cells covering a chunk plus a margin: the planner needs the kerb a
  // footprint fronts, including the one just over the chunk edge.
  const streetCellIndex = new Map(indexes.streets.cells.map((cell) => [cell.key, cell]));
  function streetCellsFor(c) {
    const grid = manifest.grid;
    const size = indexes.streets.cellSize;
    const out = [];
    const x0 = Math.floor((c.originX - 80 - grid.originX) / size);
    const x1 = Math.floor((c.originX + CHUNK + 80 - grid.originX) / size);
    const z0 = Math.floor((c.originZ - 80 - grid.originZ) / size);
    const z1 = Math.floor((c.originZ + CHUNK + 80 - grid.originZ) / size);
    for (let cz = z0; cz <= z1; cz++) {
      for (let cx = x0; cx <= x1; cx++) {
        if (streetCellIndex.has(`${cx}_${cz}`)) out.push(`${cx}_${cz}`);
      }
    }
    return out;
  }

  // The ring of street cells just outside a group. Their centrelines complete
  // the junctions that sit on the group's seam; nothing is ever placed on them.
  function haloCellsFor(g) {
    const grid = manifest.grid;
    const size = indexes.streets.cellSize;
    const own = new Set(g.streetCells.map((cell) => cell.key));
    const x0 = Math.floor((g.originX - grid.originX) / size) - 1;
    const x1 = Math.floor((g.originX + GROUP - grid.originX) / size);
    const z0 = Math.floor((g.originZ - grid.originZ) / size) - 1;
    const z1 = Math.floor((g.originZ + GROUP - grid.originZ) / size);
    const out = [];
    for (let cz = z0; cz <= z1; cz++) {
      for (let cx = x0; cx <= x1; cx++) {
        const key = `${cx}_${cz}`;
        if (own.has(key)) continue;
        const cell = streetCellIndex.get(key);
        if (cell) out.push(cell);
      }
    }
    return out;
  }

  function group(key) {
    let g = groups.get(key);
    if (!g) {
      const [gx, gz] = key.split('_').map(Number);
      g = {
        key,
        gx,
        gz,
        originX: extent.minX + gx * GROUP,
        originZ: extent.minZ + gz * GROUP,
        buildingCells: [],
        streetCells: [],
        landcoverCells: [],
        farMesh: null,
        groundMesh: null,
        trees: null,
        lamps: null,
        lampPools: null,
        quadFade: [1, 1, 1, 1],
        requested: false,
        groundRequested: false,
      };
      g.center = new Vector3(g.originX + GROUP / 2, 0, g.originZ + GROUP / 2);
      groups.set(key, g);
    }
    return g;
  }

  function chunk(key) {
    let c = chunks.get(key);
    if (!c) {
      const [cx, cz] = key.split('_').map(Number);
      const originX = extent.minX + cx * CHUNK;
      const originZ = extent.minZ + cz * CHUNK;
      c = {
        key,
        cx,
        cz,
        originX,
        originZ,
        cells: [],
        mesh: null,
        material: null,
        hasKit: false,
        fade: 0,
        active: false,
        requested: false,
        center: new Vector3(originX + CHUNK / 2, 0, originZ + CHUNK / 2),
        group: null,
        quadrant: 0,
      };
      chunks.set(key, c);
    }
    return c;
  }

  // Index the baked cells into runtime groups/chunks.
  for (const cell of indexes.buildings.cells) {
    const cx = cell.originX + 250;
    const cz = cell.originZ + 250;
    const g = group(groupKeyFor(cx, cz, extent));
    g.buildingCells.push(cell);
    const chunkKey = `${Math.floor((cx - extent.minX) / CHUNK)}_${Math.floor((cz - extent.minZ) / CHUNK)}`;
    const c = chunk(chunkKey);
    c.cells.push(cell);
    c.group = g;
    c.quadrant =
      (c.originX - g.originX >= CHUNK ? 1 : 0) + (c.originZ - g.originZ >= CHUNK ? 2 : 0);
  }
  for (const cell of indexes.streets.cells) {
    group(groupKeyFor(cell.originX + 250, cell.originZ + 250, extent)).streetCells.push(cell);
  }
  for (const cell of indexes.landcover.cells) {
    group(groupKeyFor(cell.originX + 250, cell.originZ + 250, extent)).landcoverCells.push(cell);
  }
  stats.cellsTotal =
    indexes.buildings.cells.length + indexes.streets.cells.length + indexes.landcover.cells.length;
  stats.groupsTotal = groups.size;

  const inflight = new Map();
  function cacheBlob(id, buffer) {
    blobCache.set(id, buffer);
    if (!blobsSeen.has(id)) {
      blobsSeen.add(id);
      stats.cellsLoaded++;
    }
    while (blobCache.size > BLOB_CACHE_MAX) {
      blobCache.delete(blobCache.keys().next().value);
    }
  }

  async function blob(kind, cellKey) {
    const id = `${kind}:${cellKey}`;
    const cached = blobCache.get(id);
    if (cached) {
      // Refresh recency so the working set survives and only stale cells fall out.
      blobCache.delete(id);
      blobCache.set(id, cached);
      return cached;
    }
    const existing = inflight.get(id);
    if (existing) return existing;

    while (inflight.size >= 28) await new Promise((resolve) => setTimeout(resolve, 8));
    // A matching request may have started while this one waited for capacity.
    const afterWait = blobCache.get(id);
    if (afterWait) return afterWait;
    const concurrent = inflight.get(id);
    if (concurrent) return concurrent;

    const request = (async () => {
      const buffer = await fetchTileBin(`${kind}/${cellKey}.bin`);
      cacheBlob(id, buffer);
      return buffer;
    })();
    inflight.set(id, request);
    try {
      return await request;
    } finally {
      inflight.delete(id);
    }
  }

  async function buildFarGroup(g) {
    if (g.requested || g.buildingCells.length === 0) return;
    g.requested = true;
    const blobs = await Promise.all(
      g.buildingCells.map(async (cell) => ({ buffer: await blob('buildings', cell.key) }))
    );
    const result = await pool.run(
      {
        type: 'far',
        key: g.key,
        originX: g.originX,
        originZ: g.originZ,
        groupSize: GROUP,
        palette,
        blobs,
      },
      []
    );
    if (result.positions.length === 0) return;
    const geometry = new BufferGeometry();
    makeAttributes(geometry, result);
    geometry.setAttribute('aQuad', new BufferAttribute(result.quads, 1));
    geometry.computeBoundingSphere();
    releaseAfterUpload(geometry);
    const material = createFarBuildingMaterial();
    const mesh = new Mesh(geometry, material);
    mesh.position.set(g.originX, 0, g.originZ);
    mesh.castShadow = true;
    mesh.receiveShadow = true;
    mesh.name = `far-${g.key}`;
    scene.add(mesh);
    g.farMesh = mesh;
    g.farUniforms = material.uniformsHolder;
    stats.farGroups++;
  }

  // Street tiles, cell by cell, with the base tier as the safety net: a toy
  // street tile that is missing or corrupt costs that cell its streetscape and
  // nothing more — the road keeps its real geometry, and the group is not lost.
  // A dev server answers a missing tile with index.html at 200, so the blob is
  // checked for its magic rather than trusted to the fetch status.
  async function streetBlobs(cells) {
    const loaded = await Promise.all(
      cells.map(async (cell) => {
        const usable = (buf) =>
          buf && buf.byteLength > 32 && new DataView(buf).getUint32(0, true) === STREETS_MAGIC;
        // One retry first: a saturated tile server drops a fetch now and then,
        // and that is not a reason to serve a whole cell from the other tier.
        let buffer = await blob(kinds().streets, cell.key).catch(() => null);
        if (!buffer) buffer = await blob(kinds().streets, cell.key).catch(() => null);
        if (usable(buffer)) return { buffer };
        const id = `${kinds().streets}:${cell.key}`;
        if (!brokenStreets.has(id)) {
          brokenStreets.add(id);
          console.warn(`street tile ${id} unusable — falling back to base streets`);
        }
        if (kinds().streets === TIERS.base.streets) return null;
        const fallback = await blob(TIERS.base.streets, cell.key).catch(() => null);
        return fallback ? { buffer: fallback } : null;
      })
    );
    return loaded.filter(Boolean);
  }

  // Same guarantee for landcover: a renamed/missing diorama tile falls back to
  // the base-tier landcover with one warning, no hole.
  async function landcoverBlobs(cells) {
    const loaded = await Promise.all(
      cells.map(async (cell) => {
        const usable = (buf) =>
          buf && buf.byteLength > 32 && new DataView(buf).getUint32(0, true) === LANDCOVER_MAGIC;
        let buffer = await blob(kinds().landcover, cell.key).catch(() => null);
        if (!buffer) buffer = await blob(kinds().landcover, cell.key).catch(() => null);
        if (usable(buffer)) return { buffer };
        const id = `${kinds().landcover}:${cell.key}`;
        if (!brokenLandcover.has(id)) {
          brokenLandcover.add(id);
          console.warn(`landcover tile ${id} unusable — falling back to base landcover`);
        }
        if (kinds().landcover === TIERS.base.landcover) return null;
        const fallback = await blob(TIERS.base.landcover, cell.key).catch(() => null);
        return fallback ? { buffer: fallback } : null;
      })
    );
    return loaded.filter(Boolean);
  }

  async function buildGround(g) {
    if (g.groundRequested) return;
    g.groundRequested = true;
    if (g.streetCells.length === 0 && g.landcoverCells.length === 0) return;
    const toyTier = tier === 'toy';
    const [streets, landcover] = await Promise.all([
      streetBlobs(g.streetCells),
      landcoverBlobs(g.landcoverCells),
    ]);
    const result = await pool.run({
      type: 'ground',
      key: g.key,
      originX: g.originX,
      originZ: g.originZ,
      streets,
      landcover,
      streetClasses: toyTier ? toy.streetClasses : manifest.streetClasses,
      landKinds: manifest.landKinds,
    });

    if (result.positions.length > 0) {
      const geometry = new BufferGeometry();
      makeAttributes(geometry, result);
      geometry.setAttribute('aKind', new BufferAttribute(result.kinds, 1));
      geometry.computeBoundingSphere();
    releaseAfterUpload(geometry);
      const mesh = new Mesh(geometry, groundMaterial);
      mesh.position.set(g.originX, 0, g.originZ);
      mesh.receiveShadow = true;
      mesh.name = `ground-${g.key}`;
      scene.add(mesh);
      g.groundMesh = mesh;
      stats.groundGroups++;
    }

    if (result.trees.length > 0) {
      const count = result.trees.length / 4;
      const trees = new InstancedMesh(toyTier ? toyTreeGeometry : treeGeometry, treeMaterial, count);
      const matrix = new Matrix4();
      const dummy = new Object3D();
      const instanceColors = new Float32Array(count * 3);
      for (let i = 0; i < count; i++) {
        const x = result.trees[i * 4];
        const y = result.trees[i * 4 + 1];
        const z = result.trees[i * 4 + 2];
        const variant = result.trees[i * 4 + 3];
        const size = variant & 3;
        const profile = TREE_SPECIES[variant >> 2] || TREE_SPECIES[0];
        dummy.position.set(x, y, z);
        // Variant 3 is a rooftop-garden tree: shrub-scale so it reads as
        // planting, not a lollipop standing on the roof.
        const s =
          size === 3
            ? 0.34 + ((x * 7.3 + z * 3.1) % 1) * 0.12
            : 0.62 + size * 0.26 + ((x * 7.3 + z * 3.1) % 1) * 0.35;
        dummy.scale.set(
          s * profile.scale[0],
          size === 3 ? s : s * (0.85 + size * 0.2) * profile.scale[1],
          s * profile.scale[2]
        );
        dummy.rotation.y = ((x * 13.7 + z * 5.3) % 1) * Math.PI * 2;
        dummy.updateMatrix();
        matrix.copy(dummy.matrix);
        trees.setMatrixAt(i, matrix);
        instanceColors[i * 3] = profile.tint[0];
        instanceColors[i * 3 + 1] = profile.tint[1];
        instanceColors[i * 3 + 2] = profile.tint[2];
      }
      trees.instanceMatrix.needsUpdate = true;
      trees.instanceColor = new InstancedBufferAttribute(instanceColors, 3);
      trees.instanceColor.needsUpdate = true;
      trees.castShadow = false;
      trees.receiveShadow = false;
      trees.frustumCulled = true;
      trees.name = `trees-${g.key}`;
      trees.visible = false;
      scene.add(trees);
      g.trees = trees;
      g.treeCount = count;
      stats.trees += count;
    }

    if (result.lamps.length > 0) {
      const count = result.lamps.length / 4;
      const lamps = new InstancedMesh(lampGeometry, lampMaterial, count);
      const pools = new InstancedMesh(lampPoolGeometry, lampPoolMaterial, count);
      const dummy = new Object3D();
      for (let i = 0; i < count; i++) {
        const x = result.lamps[i * 4];
        const y = result.lamps[i * 4 + 1];
        const z = result.lamps[i * 4 + 2];
        const roadY = result.lamps[i * 4 + 3];
        dummy.position.set(x, y, z);
        dummy.scale.setScalar(1);
        dummy.updateMatrix();
        lamps.setMatrixAt(i, dummy.matrix);
        // The pool lies on the road under the head, not at the head, and tilts
        // with the grade so it stays on the tarmac instead of hovering.
        dummy.position.set(x, roadY + POOL_LIFT, z);
        alignPoolToGround(dummy.quaternion, x, z, data.sampleElevation);
        dummy.scale.set(POOL_RADIUS, 1, POOL_RADIUS);
        dummy.updateMatrix();
        pools.setMatrixAt(i, dummy.matrix);
        dummy.quaternion.identity();
      }
      lamps.instanceMatrix.needsUpdate = true;
      lamps.instanceMatrix.setUsage(DynamicDrawUsage);
      lamps.visible = false;
      lamps.name = `lamps-${g.key}`;
      scene.add(lamps);
      pools.instanceMatrix.needsUpdate = true;
      pools.instanceMatrix.setUsage(DynamicDrawUsage);
      pools.visible = false;
      pools.name = `lamp-pools-${g.key}`;
      // After the road ribbon, so the additive wash lands on top of it.
      pools.renderOrder = 3;
      scene.add(pools);
      g.lamps = lamps;
      g.lampPools = pools;
      g.lampCount = count;
      stats.lamps += count;
    }

    if (result.paths.length) {
      for (const path of result.paths) paths.push(path);
      onPathsReady(paths);
    }
  }

  // Near-tier streetscape for one ground group. Same blobs, same material and
  // the same one-mesh-per-group shape as the resident ground, so a group in
  // range costs exactly one extra draw call.
  async function buildGroundDetail(g) {
    if (g.detailRequested || g.streetCells.length === 0) return;
    const streetClasses = tier === 'toy' ? toy.streetClasses : manifest.streetClasses;
    if (!streetClasses.some((cls) => cls.detail || cls.profile)) return;
    g.detailRequested = true;
    const streets = await streetBlobs(g.streetCells);
    // Market Street and the shopfronts come from the context layer; the worker
    // only ever sees geometry, so the hints ride along with the job.
    let plan = null;
    if (tier === 'toy') {
      await streetkitReady;
      if (streetkit.fleet) {
        const [hints, halo] = await Promise.all([
          streetkit.hints(g.originX, g.originZ, g.originX + GROUP, g.originZ + GROUP),
          streetBlobs(haloCellsFor(g)),
        ]);
        // Real bus stops for this cell. The worker cannot fetch, so the slice
        // rides along with the job the same way the streetkit hints do.
        const stopTable = await busStopsReady;
        plan = {
          ...hints,
          halo,
          bounds: [g.originX, g.originZ, g.originX + GROUP, g.originZ + GROUP],
          exclusions: streetkit.exclusions,
          busStops: stopsInBounds(
            stopTable,
            g.originX,
            g.originZ,
            g.originX + GROUP,
            g.originZ + GROUP,
          ),
          limit: GROUP_LIMIT,
        };
      }
    }
    const result = await pool.run({
      type: 'grounddetail',
      key: g.key,
      originX: g.originX,
      originZ: g.originZ,
      streets,
      landcover: [],
      streetClasses,
      landKinds: manifest.landKinds,
      plan,
    });
    // The camera may have left while the worker was busy.
    if (!g.detailRequested) return;
    if (plan && result.furniture && result.furniture.length) {
      g.furniture = streetkit.fleet.add(g.key, result.furniture) > 0;
      stats.furniture = streetkit.fleet.instances;
      stats.furnitureDraws = streetkit.fleet.drawCalls;
    }
    if (result.positions.length === 0) return;
    const geometry = new BufferGeometry();
    makeAttributes(geometry, result);
    geometry.setAttribute('aKind', new BufferAttribute(result.kinds, 1));
    geometry.computeBoundingSphere();
    releaseAfterUpload(geometry);
    const mesh = new Mesh(geometry, groundMaterial);
    mesh.position.set(g.originX, 0, g.originZ);
    mesh.receiveShadow = true;
    mesh.name = `streetscape-${g.key}`;
    scene.add(mesh);
    g.detailMesh = mesh;
    stats.groundDetail++;
  }

  function disposeGroundDetail(g) {
    g.detailRequested = false;
    if (g.furniture) {
      streetkit.fleet.remove(g.key);
      g.furniture = false;
      stats.furniture = streetkit.fleet.instances;
      stats.furnitureDraws = streetkit.fleet.drawCalls;
    }
    if (!g.detailMesh) return;
    scene.remove(g.detailMesh);
    g.detailMesh.geometry.dispose();
    g.detailMesh = null;
    stats.groundDetail--;
  }

  // One planning + batching round for a chunk. Returns null when the kit could
  // not be honoured, so the caller retries with the offending pieces disabled
  // and the lots go back to procedural masses rather than leaving a hole.
  async function runNearJob(c, toyTier, blobs, useKit) {
    const kitJob =
      useKit && toyTier && kit.enabled
        ? {
            kit: catalogForWorker(kit.catalog, kit.disabled),
            zones: kit.zones,
            exclusions: kit.exclusions,
            streets: await streetBlobs(streetCellsFor(c).map((key) => ({ key }))),
          }
        : null;
    const result = await pool.run({
      type: toyTier ? 'toy' : 'near',
      key: c.key,
      originX: c.originX,
      originZ: c.originZ,
      palette: toyTier ? toyPalette : palette,
      blobs,
      kit: kitJob,
    });
    if (!result.kit || result.kit.length === 0) return { result, kit: false };

    // Merge every piece this chunk asked for before anything is shown, so the
    // batch and the procedural mesh always appear in the same frame.
    const broken = await kit.loader.ensure(result.kitPieces);
    if (broken.length) {
      for (const index of broken) kit.disabled.add(index);
      return null;
    }
    if (!kit.fleet.canFit(result.kit.length / 8)) {
      if (!kit.warned) {
        console.warn('[kit] instance budget reached, remaining chunks stay procedural');
        kit.warned = true;
      }
      return null;
    }
    return { result, kit: true };
  }

  async function buildNearChunk(c) {
    if (c.requested || c.cells.length === 0) return;
    c.requested = true;
    const toyTier = tier === 'toy';
    if (toyTier) await kitReady;
    const blobs = await Promise.all(
      c.cells.map(async (cell) => ({ buffer: await blob(kinds().buildings, cell.key) }))
    );
    let attempt = await runNearJob(c, toyTier, blobs, true);
    if (!attempt) attempt = await runNearJob(c, toyTier, blobs, true);
    if (!attempt) attempt = await runNearJob(c, toyTier, blobs, false);
    const { result } = attempt;
    if (!c.active) {
      c.requested = false;
      return;
    }
    if (attempt.kit) {
      c.hasKit = kit.fleet.add(c.key, result.kit, 0);
      stats.kitInstances = kit.fleet.count;
      stats.kitPieceTypes = kit.fleet.pieceTypes;
      stats.kitPlaced += result.kitPlaced;
      stats.kitConsidered += result.kitConsidered;
    }
    if (result.positions.length === 0) return;
    const geometry = new BufferGeometry();
    makeAttributes(geometry, result);
    geometry.setAttribute('aMeta', new BufferAttribute(result.meta, 2));
    geometry.setAttribute('aLocalY', new BufferAttribute(result.localY, 1));
    // The lore flag byte: night profile, glow and band suppression per vertex.
    if (result.flag) geometry.setAttribute('aFlag', new BufferAttribute(result.flag, 1));
    geometry.computeBoundingSphere();
    releaseAfterUpload(geometry);
    const material = toyTier
      ? createToyBuildingMaterial()
      : createBuildingMaterial({ windows: quality.windows });
    material.uniformsHolder.uFade.value = 0;
    const mesh = new Mesh(geometry, material);
    mesh.position.set(c.originX, 0, c.originZ);
    mesh.castShadow = true;
    mesh.receiveShadow = true;
    mesh.name = `near-${c.key}`;
    scene.add(mesh);
    c.mesh = mesh;
    c.material = material;
    stats.nearChunks++;
  }

  function disposeChunk(c) {
    if (kit.fleet && kit.fleet.remove(c.key)) stats.kitInstances = kit.fleet.count;
    c.hasKit = false;
    if (c.mesh) {
      scene.remove(c.mesh);
      c.mesh.geometry.dispose();
      c.material.dispose();
      c.mesh = null;
      c.material = null;
      stats.nearChunks--;
    }
    c.fade = 0;
    c.requested = false;
  }

  function disposeGround(g) {
    disposeGroundDetail(g);
    if (g.groundMesh) stats.groundGroups--;
    stats.trees -= g.treeCount || 0;
    stats.lamps -= g.lampCount || 0;
    g.treeCount = 0;
    g.lampCount = 0;
    for (const key of ['groundMesh', 'trees', 'lamps', 'lampPools']) {
      const obj = g[key];
      if (!obj) continue;
      scene.remove(obj);
      // Geometry is per-group for the ground mesh, shared for trees and lamps;
      // the instanced meshes still own their per-instance matrix buffers.
      if (key === 'groundMesh') obj.geometry.dispose();
      else obj.dispose();
      g[key] = null;
    }
    g.groundRequested = false;
  }

  // Style toggle. Both tiers use the same cells, the same hysteresis and the same
  // eviction path: switching just drops the loaded geometry and lets the normal
  // streaming loop refetch it from the other tier's URLs.
  async function setTier(name) {
    if (name === tier) return;
    if (name === 'toy' && !toy) {
      const res = await fetch(tileUrl('toy.json'));
      if (!res.ok) throw new Error(`toy index: ${res.status}`);
      toy = await res.json();
      toyPalette = toy.palette.map((p) => p.color.map((c) => Math.round(c * 255)));
    }
    const previous = kinds();
    tier = name;

    for (const c of chunks.values()) {
      c.active = false; // the normal hysteresis re-enters them from the new tier
      disposeChunk(c);
    }
    if (kit.fleet) {
      kit.fleet.clear();
      stats.kitInstances = 0;
      stats.kitPlaced = 0;
      stats.kitConsidered = 0;
    }
    if (streetkit.fleet) {
      streetkit.fleet.clear();
      stats.furniture = 0;
      stats.furnitureDraws = 0;
    }
    const reload = [];
    for (const g of groups.values()) {
      if (g.groundRequested) reload.push(g);
      disposeGround(g);
    }
    paths.length = 0;
    onPathsReady(paths);

    // Drop the outgoing tier's blobs so repeated toggles do not grow the cache.
    const dropped = (id) => {
      const kind = id.slice(0, id.indexOf(':'));
      return kind === previous.streets || kind === previous.landcover || kind === previous.buildings;
    };
    for (const id of [...blobCache.keys()]) if (dropped(id)) blobCache.delete(id);
    for (const id of [...blobsSeen]) if (dropped(id)) blobsSeen.delete(id);

    // cellsLoaded counts cells fetched for the current tier, so the tile
    // readout stays coherent instead of accumulating across swaps.
    stats.cellsLoaded = blobsSeen.size;

    for (const g of reload) buildGround(g).catch((err) => console.warn('ground reload failed', g.key, err));
  }

  // Load order: nearest to the hero pivot first, so the city fills in from the
  // middle of the frame outward.
  function preload(origin) {
    const ordered = [...groups.values()].sort(
      (a, b) => a.center.distanceToSquared(origin) - b.center.distanceToSquared(origin)
    );
    // Four pipelines in flight: enough to keep every worker fed and the fetch
    // queue saturated without starving the render loop of main-thread time.
    async function pump(items, work, lanes = 4) {
      let cursor = 0;
      const lane = async () => {
        while (cursor < items.length) {
          const item = items[cursor++];
          await work(item).catch((err) => console.warn('tile group failed', item.key, err));
        }
      };
      await Promise.all(Array.from({ length: lanes }, lane));
    }

    // Stream silhouette and ground together. Streets, trees, lamps, and traffic
    // paths become alive near the opening view while distant skyline groups keep
    // filling in behind them.
    Promise.all([pump(ordered, buildFarGroup, 3), pump(ordered, buildGround, 3)]);
  }

  const tmp = new Vector3();

  function update(dt, cameraTarget, cameraPos, quality) {
    // Near tier activation with hysteresis so cells never thrash on the boundary.
    for (const c of chunks.values()) {
      tmp.copy(c.center);
      tmp.y = cameraTarget.y;
      const dist = Math.min(cameraPos.distanceTo(tmp), cameraTarget.distanceTo(tmp));
      const wantNear = dist < NEAR_ENTER * quality.nearScale;
      const dropNear = dist > NEAR_EXIT * quality.nearScale;
      if (wantNear && !c.active) {
        c.active = true;
        buildNearChunk(c).catch((err) => console.warn('near chunk failed', c.key, err));
      } else if (dropNear && c.active) {
        c.active = false;
        if (c.mesh || c.hasKit) c.fade = Math.min(c.fade, 1);
      }

      const target = c.active && (c.mesh || c.hasKit) ? 1 : 0;
      if (c.fade !== target) {
        const step = FADE_SPEED * dt;
        c.fade = target > c.fade ? Math.min(target, c.fade + step) : Math.max(target, c.fade - step);
        if (c.material) c.material.uniformsHolder.uFade.value = c.fade;
        if (kit.fleet) kit.fleet.setFade(c.key, c.fade);
      }
      if (!c.active && c.fade <= 0 && (c.mesh || c.hasKit)) disposeChunk(c);

      // The far tier's matching quadrant is the inverse of the near fade.
      if (c.group) c.group.quadFade[c.quadrant] = 1 - c.fade;
    }

    for (const g of groups.values()) {
      if (g.farUniforms) g.farUniforms.uQuadFade.value.set(...g.quadFade);
      tmp.copy(g.center);
      tmp.y = cameraTarget.y;
      const dist = cameraTarget.distanceTo(tmp);
      if (g.trees) g.trees.visible = dist < TREE_RANGE * quality.treeScale;
      // The procedural glow sphere is the stand-in for a lamp this group has no
      // kit lamps for. Where kit lamps stand, they are the lamp — two glows in
      // one place read as a bloom bug.
      if (g.lamps) {
        const lit = shared.uNight.value > 0.08 && !g.furniture;
        g.lamps.visible = lit && dist < LAMP_RANGE;
        // Same either/or as the head: where the kit's real lamps stand, their
        // own pools light the road and this group must not double them.
        if (g.lampPools) g.lampPools.visible = lit && dist < POOL_RANGE * quality.poolScale;
      }
      if (dist < DETAIL_ENTER && !g.detailRequested) {
        buildGroundDetail(g).catch((err) => console.warn('streetscape failed', g.key, err));
      } else if (dist > DETAIL_EXIT && g.detailRequested) {
        disposeGroundDetail(g);
      }
    }
    lampMaterial.opacity = Math.min(0.85, shared.uNight.value * 0.95);
    lampPoolMaterial.opacity = Math.min(1, shared.uNight.value * 1.1) * quality.poolStrength;
    if (streetkit.fleet) streetkit.fleet.update();
  }

  return {
    update,
    preload,
    setTier,
    get tier() {
      return tier;
    },
    stats,
    paths,
    onPaths(cb) {
      pathListeners.push(cb);
      if (paths.length) cb(paths);
    },
    get progress() {
      return stats.cellsTotal ? stats.cellsLoaded / stats.cellsTotal : 0;
    },
    setQuality(q, tier) {
      quality.windows = q.windows;
      quality.tier = tier;
      // Lamp pools are fill rate, so the tier scales both how far they reach
      // and how hard they hit.
      quality.poolScale = q.poolScale;
      quality.poolStrength = q.poolStrength;
      for (const c of chunks.values()) {
        // The toy tier has no procedural window grid to turn down.
        const windows = c.material?.uniformsHolder.uWindows;
        if (windows) windows.value = q.windows;
      }
      // Street furniture answers to the same knob: the placement stays
      // planned, only the per-class meshes hide (PERF-PLAN #6).
      if (tier && streetkit.fleet) {
        // Hand over the tier's own pool numbers rather than only its name: the
        // kit used to re-derive them from the name, so editing the QUALITY
        // table had no effect on the lamps.
        streetkit.fleet.setQuality(tier, q);
        stats.furnitureDraws = streetkit.fleet.drawCalls;
      }
    },
  };
}
