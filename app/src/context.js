// The context layer: everything the city knows about itself.
//
// Per-cell sidecars (pick boxes + identity) stream alongside the geometry
// tiles; the global street, park, neighbourhood, landmark and search indexes
// load once. Picking is a CPU ray/slab test against the baked oriented boxes —
// the GPU geometry is merged per cell, so it cannot be picked directly, and a
// colour-id pass would cost a second render of the whole city.

import { tileUrl } from './data.js';

const CELL_SIZE = 500;
const TTL_MS = 15 * 60 * 1000;
const MAX_PICK_DISTANCE = 4000;
const STREET_HIT_M = 14;

export const CATEGORY_LABELS = [
  'Miscellaneous',
  'House',
  'Apartments',
  'Office',
  'Shop',
  'Restaurant or café',
  'Bar',
  'Hotel',
  'Place of worship',
  'School',
  'University',
  'Hospital',
  'Clinic',
  'Fire station',
  'Police station',
  'Library',
  'Museum',
  'Theatre or cinema',
  'Government',
  'Industrial',
  'Warehouse',
  'Gas station',
  'Supermarket',
  'Parking garage',
  'Gym',
  'Transit station',
];

const SOURCE_LABELS = {
  datasf: 'DataSF facility records',
  osm: 'OpenStreetMap',
  overture: 'Overture Places (Foursquare open records)',
  business: 'DataSF registered business locations',
  landuse: 'DataSF land use',
  heuristic: 'Inferred from height and footprint',
  511: 'Live 511.org feed (SF Bay Ferry)',
  demo: 'Simulated demo vessel',
};

const CONFIDENCE_LABELS = ['inferred', 'single source', 'two sources agree', 'three or more sources agree'];

export const humanize = (value) =>
  String(value)
    .replace(/_/g, ' ')
    .replace(/^./, (c) => c.toUpperCase());

export function sourceLabel(source) {
  return SOURCE_LABELS[source] || humanize(source);
}

export function confidenceLabel(confidence) {
  return CONFIDENCE_LABELS[Math.max(0, Math.min(3, confidence | 0))];
}

function pointInRings(x, z, rings) {
  for (const ring of rings) {
    let inside = false;
    for (let i = 0, j = ring.length - 2; i < ring.length; j = i, i += 2) {
      const xi = ring[i];
      const zi = ring[i + 1];
      const xj = ring[j];
      const zj = ring[j + 1];
      if (zi > z !== zj > z && x < ((xj - xi) * (z - zi)) / (zj - zi) + xi) inside = !inside;
    }
    if (inside) return true;
  }
  return false;
}

function distanceToSegment(x, z, ax, az, bx, bz) {
  const dx = bx - ax;
  const dz = bz - az;
  const l2 = dx * dx + dz * dz || 1;
  const t = Math.max(0, Math.min(1, ((x - ax) * dx + (z - az) * dz) / l2));
  return Math.hypot(x - (ax + dx * t), z - (az + dz * t));
}

export async function createContext(data) {
  const grid = data.manifest.grid;
  const [streets, parks, landmarkFile, neighborhoods] = await Promise.all([
    fetch(tileUrl('context/streets.json')).then((r) => r.json()),
    fetch(tileUrl('context/parks.json')).then((r) => r.json()),
    fetch(tileUrl('context/landmarks.json')).then((r) => r.json()),
    fetch(tileUrl('context/neighborhoods.json')).then((r) => r.json()),
  ]);
  const streetByName = new Map(streets.map((s) => [s.name, s]));

  // One promise per cell, so a burst of picks and prefetches during a fly-in
  // never issues the same request twice.
  const cellPromises = new Map();
  const cellData = new Map();

  function cellKeyAt(x, z) {
    const cx = Math.floor((x - grid.originX) / CELL_SIZE);
    const cz = Math.floor((z - grid.originZ) / CELL_SIZE);
    if (cx < 0 || cz < 0 || cx >= grid.cols || cz >= grid.rows) return null;
    return `${cx}_${cz}`;
  }

  function loadCell(key) {
    const cached = cellData.get(key);
    if (cached && performance.now() - cached.at < TTL_MS) return Promise.resolve(cached.value);
    // A cell the bake never wrote has nothing to say; asking for it is a 404.
    if (!data.contextCells.has(key)) {
      cellData.set(key, { at: performance.now(), value: null });
      return Promise.resolve(null);
    }
    let promise = cellPromises.get(key);
    if (promise) return promise;
    promise = fetch(tileUrl(`ctx/${key}.json`))
      .then((res) => (res.ok ? res.json() : null))
      .catch(() => null)
      .then((value) => {
        cellData.set(key, { at: performance.now(), value });
        cellPromises.delete(key);
        return value;
      });
    cellPromises.set(key, promise);
    return promise;
  }

  function loadedCell(key) {
    const cached = cellData.get(key);
    return cached ? cached.value : null;
  }

  // Sidecars for the cells the camera can plausibly click, refreshed as it moves.
  let lastPrefetch = null;
  function prefetch(pivot, radius = 900) {
    const key = cellKeyAt(pivot.x, pivot.z);
    if (!key || key === lastPrefetch) return;
    lastPrefetch = key;
    const span = Math.ceil(radius / CELL_SIZE);
    const [cx, cz] = key.split('_').map(Number);
    for (let dz = -span; dz <= span; dz++) {
      for (let dx = -span; dx <= span; dx++) {
        const k = `${cx + dx}_${cz + dz}`;
        if (cx + dx < 0 || cz + dz < 0 || cx + dx >= grid.cols || cz + dz >= grid.rows) continue;
        loadCell(k);
      }
    }
  }

  // Every cell the ray crosses within the pick range, near to far.
  function cellsAlongRay(origin, direction) {
    const keys = [];
    const seen = new Set();
    const step = CELL_SIZE / 3;
    for (let t = 0; t <= MAX_PICK_DISTANCE; t += step) {
      const key = cellKeyAt(origin.x + direction.x * t, origin.z + direction.z * t);
      if (!key || seen.has(key)) continue;
      seen.add(key);
      keys.push(key);
    }
    return keys;
  }

  // Ray against an oriented box: rotate the ray into the box's frame, then a
  // plain slab test. Boxes are axis-aligned in that frame by construction.
  function rayBox(origin, direction, x, z, w, d, y0, y1, r) {
    const cos = Math.cos(-r);
    const sin = Math.sin(-r);
    const ox = origin.x - x;
    const oz = origin.z - z;
    const lox = ox * cos - oz * sin;
    const loz = ox * sin + oz * cos;
    const ldx = direction.x * cos - direction.z * sin;
    const ldz = direction.x * sin + direction.z * cos;

    let tMin = 0;
    let tMax = MAX_PICK_DISTANCE;
    const slab = (o, dir, min, max) => {
      if (Math.abs(dir) < 1e-6) return o >= min && o <= max;
      const t1 = (min - o) / dir;
      const t2 = (max - o) / dir;
      tMin = Math.max(tMin, Math.min(t1, t2));
      tMax = Math.min(tMax, Math.max(t1, t2));
      return tMax >= tMin;
    };
    if (!slab(lox, ldx, -w, w)) return -1;
    if (!slab(loz, ldz, -d, d)) return -1;
    if (!slab(origin.y, direction.y, y0, y1)) return -1;
    return tMin > 0 ? tMin : -1;
  }

  function pickBuilding(origin, direction, toy) {
    let best = null;
    for (const key of cellsAlongRay(origin, direction)) {
      const cell = loadedCell(key);
      if (!cell) continue;
      const p = cell.pick;
      for (let i = 0; i < p.id.length; i++) {
        const height = toy ? p.t[i] : p.h[i];
        const t = rayBox(origin, direction, p.x[i], p.z[i], p.w[i], p.d[i], p.y[i], p.y[i] + height, p.r[i]);
        if (t < 0 || (best && t >= best.t)) continue;
        best = { t, key, index: i, id: p.id[i] };
      }
    }
    if (!best) return null;
    const cell = loadedCell(best.key);
    return buildingEntity(best.id, cell, best.index, best.t);
  }

  function buildingEntity(id, cell, index, t = 0) {
    const p = cell.pick;
    const info = cell.b[id] || { c: 0, f: 1, s: 'heuristic', cf: 0 };
    return {
      kind: 'building',
      id: `b:${id}`,
      buildingId: id,
      name: info.n || null,
      title: info.n || CATEGORY_LABELS[info.c] || 'Building',
      cat: info.c,
      sub: info.sc || null,
      address: info.a || null,
      floors: info.f,
      source: info.s,
      confidence: info.cf,
      wikidata: info.w || null,
      tier: info.t || null,
      x: p.x[index],
      z: p.z[index],
      w: p.w[index],
      d: p.d[index],
      r: p.r[index],
      baseY: p.y[index],
      height: p.h[index],
      toyHeight: p.t[index],
      distance: t,
    };
  }

  function findBuilding(id) {
    for (const [, cached] of cellData) {
      const cell = cached.value;
      if (!cell || !cell.b[id]) continue;
      const index = cell.pick.id.indexOf(Number(id));
      if (index >= 0) return buildingEntity(Number(id), cell, index);
    }
    return null;
  }

  async function loadBuilding(id, x, z) {
    const key = cellKeyAt(x, z);
    if (key) await loadCell(key);
    return findBuilding(id);
  }

  function pickStreet(point) {
    const key = cellKeyAt(point.x, point.z);
    if (!key) return null;
    const cell = loadedCell(key);
    if (!cell) return null;
    let best = null;
    for (const run of cell.s) {
      for (let i = 2; i < run.p.length; i += 2) {
        const dist = distanceToSegment(point.x, point.z, run.p[i - 2], run.p[i - 1], run.p[i], run.p[i + 1]);
        if (dist > STREET_HIT_M || (best && dist >= best.dist)) continue;
        best = { dist, name: run.n };
      }
    }
    if (!best) return null;
    const record = streetByName.get(best.name);
    return {
      kind: 'street',
      id: `street:${best.name}`,
      title: humanize(best.name.toLowerCase()),
      name: best.name,
      nhood: record?.nhood || null,
      length: record?.len || null,
      x: point.x,
      z: point.z,
      source: 'datasf',
      confidence: 3,
    };
  }

  function pickPark(point) {
    for (const park of parks) {
      if (!pointInRings(point.x, point.z, park.rings)) continue;
      return {
        kind: 'park',
        id: park.id,
        title: park.name,
        name: park.name,
        type: park.type,
        acres: park.acres,
        x: park.x,
        z: park.z,
        // The real boundary, so the selection traces the park instead of
        // dropping a fixed 160 m circle somewhere near it.
        rings: park.rings || null,
        source: 'datasf',
        confidence: 3,
      };
    }
    return null;
  }

  function pickNeighborhood(point) {
    for (const nhood of neighborhoods) {
      if (!pointInRings(point.x, point.z, nhood.rings)) continue;
      return {
        kind: 'neighborhood',
        id: nhood.id,
        title: nhood.name,
        name: nhood.name,
        x: nhood.x,
        z: nhood.z,
        source: 'datasf',
        confidence: 3,
      };
    }
    return null;
  }

  function pickLandmark(origin, direction) {
    let best = null;
    for (const landmark of landmarkFile.landmarks) {
      const height = landmark.height || 60;
      const radius = Math.max(60, height * 0.5);
      // Distance from the landmark's mid-height point to the ray.
      const px = landmark.x - origin.x;
      const py = height * 0.5 - origin.y;
      const pz = landmark.z - origin.z;
      const t = px * direction.x + py * direction.y + pz * direction.z;
      if (t <= 0 || t > MAX_PICK_DISTANCE) continue;
      const dist = Math.hypot(px - direction.x * t, py - direction.y * t, pz - direction.z * t);
      if (dist > radius || (best && t >= best.distance)) continue;
      best = {
        kind: 'landmark',
        id: landmark.id,
        title: landmark.name,
        name: landmark.name,
        x: landmark.x,
        z: landmark.z,
        height,
        camera: landmark.camera,
        distance: t,
        source: 'osm',
        confidence: 3,
      };
    }
    return best;
  }

  // The cascade: a click resolves to the thing under it, or to NOTHING. It is
  // allowed to answer "nothing here" — see the water note at the bottom.
  async function pick(origin, direction, groundPoint, { toy = false } = {}) {
    await Promise.all(cellsAlongRay(origin, direction).slice(0, 12).map(loadCell));
    const landmark = pickLandmark(origin, direction);
    const building = pickBuilding(origin, direction, toy);
    if (landmark && (!building || landmark.distance < building.distance + 40)) return landmark;
    if (building) return building;
    if (!groundPoint) return null;
    // Streets are deliberately NOT picked. Every click over open ground used to
    // land on whichever road was nearest, which is noise: a road is not what
    // anyone is pointing at, and the card churned on every stray click. They
    // remain in search and available to the concierge — this is only about
    // clicking in the 3D scene. A click on a road now resolves to the
    // neighbourhood it is in.
    // Neighbourhoods are no longer PICKED either: they are named continuously by
    // the floating labels (signs.js), which say the same thing without a click
    // and without a 420 m ring drawn round the answer. neighborhoodAt stays for
    // the concierge and for building cards.
    // Open water is NOT the answer to a click that hit nothing. It used to be
    // the final fallback, so every stray click anywhere in the city — over a
    // pavement, a rooftop gap, a park path — opened a card announcing "San
    // Francisco Bay · Open water", which is both wrong and the loudest possible
    // way to say nothing was there. Same reasoning that already removed streets
    // and neighbourhoods from this cascade: a click that lands on nothing should
    // resolve to nothing, and the card simply stays as it was.
    //
    // Note this removes the ONLY way to select the Bay: nothing else in the app
    // produces a `water` entity, and the search index has no row for it either.
    // That is the intended trade — a label nobody asked for on every stray click
    // is worse than no label — but it does leave the `water` branches in
    // cards.js and main.js's focusTarget unreachable until something picks water
    // deliberately, which is where they are waiting.
    return pickPark(groundPoint);
  }

  // The search index is only needed once the user actually searches.
  let searchIndex = null;
  let searchPromise = null;
  function loadSearch() {
    if (searchIndex) return Promise.resolve(searchIndex);
    if (!searchPromise) {
      searchPromise = fetch(tileUrl('context/search-index.json'))
        .then((r) => r.json())
        .then((list) => (searchIndex = list));
    }
    return searchPromise;
  }

  const GROUP_ORDER = ['landmark', 'view', 'neighborhood', 'park', 'street', 'building'];

  async function search(query, limit = 8) {
    const list = await loadSearch();
    const q = query.trim().toLowerCase();
    if (!q) return [];
    const hits = [];
    for (const entry of list) {
      const at = entry.q.indexOf(q);
      if (at < 0) continue;
      const rank = (at === 0 ? 0 : 1) * 10 + GROUP_ORDER.indexOf(entry.t) + (entry.tier === 'A' ? -0.5 : 0);
      hits.push({ entry, rank, at });
      if (hits.length > 400) break;
    }
    hits.sort((a, b) => a.rank - b.rank || a.entry.n.length - b.entry.n.length);
    return hits.slice(0, limit).map((h) => h.entry);
  }

  let statsPromise = null;
  function stats() {
    if (!statsPromise) statsPromise = fetch(tileUrl('context/stats.json')).then((r) => r.json());
    return statsPromise;
  }

  return {
    pick,
    prefetch,
    search,
    stats,
    loadBuilding,
    findBuilding,
    landmarks: landmarkFile.landmarks,
    views: landmarkFile.views,
    neighborhoods,
    parks,
    streets,
    neighborhoodAt: (x, z) => pickNeighborhood({ x, z }),
    // Streets left the CLICK cascade (they were noise on every stray click) but
    // the lookup stays: search and the concierge still answer about them.
    streetAt: (x, z) => pickStreet({ x, z }),
    parkAt: (x, z) => pickPark({ x, z }),
  };
}
