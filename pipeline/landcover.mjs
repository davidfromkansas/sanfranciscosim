// Bakes OSM green space, beaches and inland water into per-cell triangulated,
// terrain-draped meshes, plus a deterministic tree scatter for runtime
// instancing.

import { mkdir, rm, writeFile, readFile } from 'node:fs/promises';
import earcut from 'earcut';
import {
  CELL_SIZE,
  EXTENT,
  GRID,
  cellIndex,
  cellOrigin,
  hash01,
  insideBBox,
  project,
} from './lib/geo.mjs';
import { ringArea, ringBBox, ringCentroid } from './lib/poly.mjs';
import { loadHeightmap } from './lib/heightmap.mjs';
import { writeLandcoverBlob } from './lib/binio.mjs';
import { loadTreeBlockers } from './lib/treeblockers.mjs';
import { NAMED_PARKS, PARK_COVER } from './lib/landmarks.mjs';
import { LAND_KINDS } from './lib/classes.mjs';

const DATA = new URL('./data/', import.meta.url);
const OUT = new URL('./out/', import.meta.url);
const CELLS_OUT = new URL('./out/landcover/', import.meta.url);

const KIND = Object.fromEntries(LAND_KINDS.map((k, i) => [k.id, i]));
const MAX_EDGE = 55; // subdivide triangles longer than this so parks follow hills
const TREE_AREA_TREES = 90;
const TREE_AREA_PARK = 200;
const MIN_OVERRIDE_HOLE_AREA = 3000;

const { sampleElevation } = await loadHeightmap();
// Trees may not stand in a building, on a roadway or in water; OSM landcover
// polygons contain all three.
const { blocked: treeBlocked, stats: blockerStats } = await loadTreeBlockers({ sampleElevation });
console.log(
  `tree blockers: ${blockerStats.footprints} footprints, ${blockerStats.segments} street segments ` +
    `on a ${blockerStats.res} m grid (${blockerStats.cols}x${blockerStats.rows})`
);

function classify(tags) {
  if (!tags) return null;
  if (tags.natural === 'water' || tags.waterway || tags.landuse === 'reservoir') return KIND.water;
  if (tags.natural === 'beach' || tags.natural === 'sand') return KIND.sand;
  if (tags.natural === 'wetland') return KIND.marsh;
  if (tags.natural === 'bare_rock' || tags.natural === 'cliff') return KIND.rock;
  if (tags.natural === 'wood' || tags.landuse === 'forest') return KIND.trees;
  if (tags.natural === 'scrub' || tags.natural === 'grassland') return KIND.scrub;
  if (tags.aeroway) return KIND.paved;
  if (tags.leisure === 'pitch') return KIND.pitch;
  if (
    tags.leisure === 'park' ||
    tags.leisure === 'garden' ||
    tags.leisure === 'golf_course' ||
    tags.leisure === 'nature_reserve' ||
    tags.leisure === 'recreation_ground' ||
    tags.landuse === 'grass' ||
    tags.landuse === 'meadow' ||
    tags.landuse === 'village_green' ||
    tags.landuse === 'cemetery' ||
    tags.landuse === 'recreation_ground'
  ) {
    return KIND.grass;
  }
  return null;
}

function stableSeed(type, id, ringIndex) {
  let hash = 2166136261;
  for (const char of `${type}:${id}:${ringIndex}`) {
    hash ^= char.charCodeAt(0);
    hash = Math.imul(hash, 16777619);
  }
  return hash >>> 0;
}

function ringFromGeometry(geometry) {
  const ring = [];
  for (const p of geometry) {
    if (!p || !insideBBox(p.lon, p.lat)) continue;
    const [x, z] = project(p.lon, p.lat);
    ring.push(x, z);
  }
  return ring;
}

function isBattery(tags) {
  return /^battery\b/i.test(tags?.name || '') || tags?.defensive_works === 'battery';
}

// Overpass relations arrive as unordered member way fragments; stitch them into
// closed rings by matching endpoints.
function stitchRings(members) {
  const frags = members
    .filter((m) => m.type === 'way' && Array.isArray(m.geometry) && m.geometry.length > 1)
    .map((m) => ({ role: m.role || 'outer', pts: m.geometry.slice() }));
  const rings = [];
  const used = new Array(frags.length).fill(false);
  const near = (a, b) => Math.abs(a.lat - b.lat) < 1e-7 && Math.abs(a.lon - b.lon) < 1e-7;

  for (let i = 0; i < frags.length; i++) {
    if (used[i]) continue;
    used[i] = true;
    const role = frags[i].role;
    let pts = frags[i].pts.slice();
    let grew = true;
    while (grew) {
      grew = false;
      for (let j = 0; j < frags.length; j++) {
        if (used[j] || frags[j].role !== role) continue;
        const cand = frags[j].pts;
        const head = pts[0];
        const tail = pts[pts.length - 1];
        if (near(tail, cand[0])) {
          pts = pts.concat(cand.slice(1));
        } else if (near(tail, cand[cand.length - 1])) {
          pts = pts.concat(cand.slice(0, -1).reverse());
        } else if (near(head, cand[cand.length - 1])) {
          pts = cand.slice(0, -1).concat(pts);
        } else if (near(head, cand[0])) {
          pts = cand.slice(1).reverse().concat(pts);
        } else {
          continue;
        }
        used[j] = true;
        grew = true;
      }
    }
    if (pts.length >= 4) rings.push({ role, pts });
  }
  return rings;
}

function pointInRing(x, z, ring) {
  let inside = false;
  for (let i = 0, j = ring.length - 2; i < ring.length; j = i, i += 2) {
    const xi = ring[i];
    const zi = ring[i + 1];
    const xj = ring[j];
    const zj = ring[j + 1];
    if (zi > z !== zj > z && x < ((xj - xi) * (z - zi)) / (zj - zi) + xi) inside = !inside;
  }
  return inside;
}

// Triangulate outer + holes, then subdivide long edges and drape on terrain.
function triangulateDraped(outer, holes, maxEdge) {
  const flat = outer.slice();
  const holeIndices = [];
  for (const h of holes) {
    holeIndices.push(flat.length / 2);
    flat.push(...h);
  }
  const idx = earcut(flat, holeIndices);
  const tris = [];
  for (let i = 0; i < idx.length; i += 3) {
    tris.push([
      flat[idx[i] * 2],
      flat[idx[i] * 2 + 1],
      flat[idx[i + 1] * 2],
      flat[idx[i + 1] * 2 + 1],
      flat[idx[i + 2] * 2],
      flat[idx[i + 2] * 2 + 1],
    ]);
  }

  const out = [];
  let guard = 0;
  while (tris.length && guard < 400000) {
    const t = tris.pop();
    guard++;
    const [ax, az, bx, bz, cx, cz] = t;
    const ab = Math.hypot(bx - ax, bz - az);
    const bc = Math.hypot(cx - bx, cz - bz);
    const ca = Math.hypot(ax - cx, az - cz);
    const longest = Math.max(ab, bc, ca);
    if (longest > maxEdge) {
      if (longest === ab) {
        const m = [(ax + bx) / 2, (az + bz) / 2];
        tris.push([ax, az, m[0], m[1], cx, cz], [m[0], m[1], bx, bz, cx, cz]);
      } else if (longest === bc) {
        const m = [(bx + cx) / 2, (bz + cz) / 2];
        tris.push([bx, bz, m[0], m[1], ax, az], [m[0], m[1], cx, cz, ax, az]);
      } else {
        const m = [(cx + ax) / 2, (cz + az) / 2];
        tris.push([cx, cz, m[0], m[1], bx, bz], [m[0], m[1], ax, az, bx, bz]);
      }
      continue;
    }
    out.push(t);
  }
  return out;
}

const cells = new Map();
function cellFor(x, z) {
  const idx = cellIndex(x, z);
  if (!idx) return null;
  let cell = cells.get(idx.key);
  if (!cell) {
    const [ox, oz] = cellOrigin(idx.cx, idx.cz);
    cells.set(
      idx.key,
      (cell = {
        key: idx.key,
        cx: idx.cx,
        cz: idx.cz,
        originX: ox,
        originZ: oz,
        verts: [],
        kinds: [],
        indices: [],
        trees: [],
        weld: new Map(),
      })
    );
  }
  return cell;
}

// Coarse landuse raster: lets the terrain shader tint distant parks, beaches
// and water without loading any landcover geometry, so Golden Gate Park still
// reads as a dark green rectangle from the 9 km hero view.
const RASTER = 1024;
const landuse = new Uint8Array(RASTER * RASTER).fill(255);
const rasterCellX = (EXTENT.maxX - EXTENT.minX) / RASTER;
const rasterCellZ = (EXTENT.maxZ - EXTENT.minZ) / RASTER;

function rasterizeTriangle(kind, tri) {
  const xs = [tri[0], tri[2], tri[4]];
  const zs = [tri[1], tri[3], tri[5]];
  const i0 = Math.max(0, Math.floor((Math.min(...xs) - EXTENT.minX) / rasterCellX));
  const i1 = Math.min(RASTER - 1, Math.ceil((Math.max(...xs) - EXTENT.minX) / rasterCellX));
  const j0 = Math.max(0, Math.floor((Math.min(...zs) - EXTENT.minZ) / rasterCellZ));
  const j1 = Math.min(RASTER - 1, Math.ceil((Math.max(...zs) - EXTENT.minZ) / rasterCellZ));
  const ring = [tri[0], tri[1], tri[2], tri[3], tri[4], tri[5]];
  for (let j = j0; j <= j1; j++) {
    const z = EXTENT.minZ + (j + 0.5) * rasterCellZ;
    for (let i = i0; i <= i1; i++) {
      const x = EXTENT.minX + (i + 0.5) * rasterCellX;
      if (pointInRing(x, z, ring)) landuse[j * RASTER + i] = kind;
    }
  }
}

function addTriangle(kind, tri, waterLevel, lift = 0) {
  const cx = (tri[0] + tri[2] + tri[4]) / 3;
  const cz = (tri[1] + tri[3] + tri[5]) / 3;
  const cell = cellFor(cx, cz);
  if (!cell) return;
  rasterizeTriangle(kind, tri);
  // Weld shared corners: the terrain-following subdivision generates midpoints
  // that neighbouring triangles reuse, so welding cuts the blob size ~4x.
  for (let k = 0; k < 3; k++) {
    const x = tri[k * 2];
    const z = tri[k * 2 + 1];
    const key = `${kind}:${Math.round(x * 20)}:${Math.round(z * 20)}`;
    let index = cell.weld.get(key);
    if (index === undefined) {
      const y = kind === KIND.water ? waterLevel : sampleElevation(x, z) + 0.06 + lift;
      index = cell.verts.length / 3;
      cell.verts.push(x, y, z);
      cell.kinds.push(kind);
      cell.weld.set(key, index);
    }
    cell.indices.push(index);
  }
}

function pickSpecies(weights, seed) {
  const entries = Object.entries(weights || { broadleaf: 1 });
  const total = entries.reduce((sum, [, weight]) => sum + weight, 0);
  let roll = hash01(seed) * total;
  for (const [species, weight] of entries) {
    roll -= weight;
    if (roll < 0) return species === 'cypress' ? 1 : species === 'eucalyptus' ? 2 : species === 'palm' ? 3 : 0;
  }
  return 0;
}

function treeVariant(species, seed) {
  return species * 4 + Math.floor(hash01(seed) * 3);
}

function inTreeArea(x, z, outer, holes) {
  if (!pointInRing(x, z, outer)) return false;
  for (const h of holes) if (pointInRing(x, z, h)) return false;
  return true;
}

function scatterTrees(kind, outer, holes, area, seedBase, cover = null) {
  const per = cover?.treeArea || (kind === KIND.trees ? TREE_AREA_TREES : TREE_AREA_PARK);
  const species = cover?.species || { broadleaf: 1 };
  const mode = cover?.mode || 'random';
  const target = Math.floor(area / per);
  if (target <= 0) return 0;
  const [minX, minZ, maxX, maxZ] = ringBBox(outer);
  let placed = 0;
  const addTree = (x, z, seed) => {
    if (!inTreeArea(x, z, outer, holes) || treeBlocked(x, z)) return;
    const cell = cellFor(x, z);
    if (!cell) return;
    const kind = pickSpecies(species, seed);
    cell.trees.push(x, sampleElevation(x, z), z, treeVariant(kind, seed + 1));
    placed++;
  };
  if (mode === 'grid') {
    const spacing = Math.sqrt(per);
    const jitter = spacing * 0.3;
    let row = 0;
    for (let z = minZ; z <= maxZ && placed < target; z += spacing, row++) {
      for (let x = minX; x <= maxX && placed < target; x += spacing) {
        const seed = seedBase + row * 100003 + Math.round((x - minX) / spacing) * 31337;
        addTree(x + (hash01(seed) - 0.5) * jitter, z + (hash01(seed + 1) - 0.5) * jitter, seed);
      }
    }
    return placed;
  }
  const w = maxX - minX;
  const d = maxZ - minZ;
  const attempts = Math.min(target * 4, 400000);
  for (let i = 0; i < attempts && placed < target; i++) {
    addTree(
      minX + hash01(seedBase + i * 2) * w,
      minZ + hash01(seedBase + i * 2 + 1) * d,
      seedBase + i * 7
    );
  }
  return placed;
}

const parkHits = Object.fromEntries(NAMED_PARKS.map((p) => [p.id, 0]));
const parkAnchors = NAMED_PARKS.map((p) => {
  const [x, z] = project(p.lon, p.lat);
  return { ...p, x, z };
});

function recordParkMatch(outer, holes) {
  for (const anchor of parkAnchors) {
    if (parkHits[anchor.id]) continue;
    if (pointInRing(anchor.x, anchor.z, outer)) {
      let inHole = false;
      for (const h of holes) if (pointInRing(anchor.x, anchor.z, h)) inHole = true;
      if (!inHole) parkHits[anchor.id] = 1;
    }
  }
}

const raw = JSON.parse(await readFile(new URL('osm_landcover.json', DATA), 'utf8'));
console.log(`${raw.elements.length} OSM landcover elements`);
let featureSource = null;
try {
  featureSource = JSON.parse(await readFile(new URL('osm_features.json', DATA), 'utf8'));
} catch {
  console.warn('osm_features.json missing — skipping battery platforms');
}

let polygons = 0;
let triangles = 0;
let trees = 0;
const areaByKind = new Array(LAND_KINDS.length).fill(0);

function handlePolygon(kind, outerRing, holeRings, seedBase, cover = null, lift = 0) {
  if (outerRing.length / 2 < 3) return;
  const area = Math.abs(ringArea(outerRing));
  if (area < 60) return;
  recordParkMatch(outerRing, holeRings);

  let waterLevel = 0.25;
  if (kind === KIND.water) {
    let min = Infinity;
    for (let i = 0; i < outerRing.length; i += 2) {
      const e = sampleElevation(outerRing[i], outerRing[i + 1]);
      if (e < min) min = e;
    }
    waterLevel = Math.max(0.25, min + 0.25);
  }

  // Water surfaces are flat, so they never need the terrain-following subdivision.
  const maxEdge = kind === KIND.water ? 400 : MAX_EDGE;
  let tris = triangulateDraped(outerRing, holeRings, maxEdge);
  const expectedArea =
    Math.abs(ringArea(outerRing)) - holeRings.reduce((sum, hole) => sum + Math.abs(ringArea(hole)), 0);
  const actualArea = tris.reduce((sum, tri) => {
    return (
      sum +
      Math.abs(
        (tri[2] - tri[0]) * (tri[5] - tri[1]) - (tri[4] - tri[0]) * (tri[3] - tri[1])
      ) /
        2
    );
  }, 0);
  if (holeRings.length && Math.abs(actualArea - expectedArea) > Math.max(1, expectedArea * 1e-4)) {
    console.warn(`invalid cover holes for ${seedBase}: expected ${expectedArea}, actual ${actualArea}; dropping holes`);
    tris = triangulateDraped(outerRing, [], maxEdge);
    holeRings = [];
  }
  for (const t of tris) addTriangle(kind, t, waterLevel, lift);
  triangles += tris.length;
  polygons++;
  areaByKind[kind] += area;

  if (kind === KIND.trees || kind === KIND.grass) {
    trees += scatterTrees(kind, outerRing, holeRings, area, seedBase, cover);
  }
}

function coverForElement(outers) {
  for (const [id, cover] of Object.entries(PARK_COVER)) {
    const park = NAMED_PARKS.find((entry) => entry.id === id);
    if (!park) continue;
    const [x, z] = project(park.lon, park.lat);
    if (outers.some((outer) => pointInRing(x, z, outer))) return cover;
  }
  return null;
}

const records = [];
const elements = raw.elements
  .slice()
  .sort((a, b) => a.type.localeCompare(b.type) || Number(a.id) - Number(b.id));
for (const el of elements) {
  const kind = classify(el.tags);
  if (kind === null) continue;
  let outers = [];
  let innerRings = [];
  if (el.type === 'way' && Array.isArray(el.geometry)) {
    outers = [ringFromGeometry(el.geometry)];
  } else if (el.type === 'relation' && Array.isArray(el.members)) {
    const rings = stitchRings(el.members);
    outers = rings.filter((r) => r.role !== 'inner').map((r) => ringFromGeometry(r.pts));
    innerRings = rings.filter((r) => r.role === 'inner').map((r) => ringFromGeometry(r.pts));
  }
  const cover = coverForElement(outers);
  for (let ringIndex = 0; ringIndex < outers.length; ringIndex++) {
    const outer = outers[ringIndex];
    if (outer.length / 2 < 3) continue;
    const bbox = ringBBox(outer);
    const holes = innerRings.filter((h) => {
      if (h.length / 2 < 3) return false;
      const [hx, hz] = ringCentroid(h);
      return hx >= bbox[0] && hx <= bbox[2] && hz >= bbox[1] && hz <= bbox[3];
    });
    const area = Math.abs(ringArea(outer));
    if (area < 60) continue;
    records.push({
      kind,
      outer,
      holes,
      area,
      bbox,
      centroid: ringCentroid(outer),
      cover,
      seed: stableSeed(el.type, el.id, ringIndex),
    });
  }
}

const batteryNodes = [];
const batteries = [];
for (const el of featureSource?.elements || []) {
  if (!isBattery(el.tags)) continue;
  if (el.type !== 'way' || !Array.isArray(el.geometry)) {
    batteryNodes.push(el.tags?.name || `${el.type}/${el.id}`);
    continue;
  }
  const outer = ringFromGeometry(el.geometry);
  if (outer.length / 2 < 3) continue;
  batteries.push({
    id: el.id,
    name: el.tags?.name || `Battery ${el.id}`,
    outer,
    bbox: ringBBox(outer),
    centroid: ringCentroid(outer),
    seed: stableSeed(el.type, el.id, 0),
  });
}

let overrideHoles = 0;
const acceptedBatteries = new Set();
const skippedBatteries = [];
for (const record of records) {
  let holes = record.holes.slice();
  let cover = null;
  if (record.cover) {
    cover = record.cover;
    record.kind = KIND[cover.base];
    const accepted = [];
    for (const battery of batteries) {
      if (!pointInRing(battery.centroid[0], battery.centroid[1], record.outer)) continue;
      let fullyInside = true;
      for (let i = 0; i < battery.outer.length; i += 2) {
        if (!pointInRing(battery.outer[i], battery.outer[i + 1], record.outer)) {
          fullyInside = false;
          break;
        }
      }
      if (!fullyInside) continue;
      const overlaps = accepted.some(
        (bbox) =>
          battery.bbox[0] <= bbox[2] &&
          battery.bbox[2] >= bbox[0] &&
          battery.bbox[1] <= bbox[3] &&
          battery.bbox[3] >= bbox[1]
      );
      if (overlaps) continue;
      accepted.push(battery.bbox);
      holes.push(battery.outer);
      acceptedBatteries.add(battery);
    }
    for (const candidate of records) {
      if (candidate === record || candidate.kind === record.kind || candidate.area < MIN_OVERRIDE_HOLE_AREA) {
        continue;
      }
      if (!pointInRing(candidate.centroid[0], candidate.centroid[1], record.outer)) continue;
      let fullyInside = true;
      for (let i = 0; i < candidate.outer.length; i += 2) {
        if (!pointInRing(candidate.outer[i], candidate.outer[i + 1], record.outer)) {
          fullyInside = false;
          break;
        }
      }
      if (!fullyInside) continue;
      const overlaps = accepted.some(
        (bbox) =>
          candidate.bbox[0] <= bbox[2] &&
          candidate.bbox[2] >= bbox[0] &&
          candidate.bbox[1] <= bbox[3] &&
          candidate.bbox[3] >= bbox[1]
      );
      if (overlaps) continue;
      accepted.push(candidate.bbox);
      holes.push(candidate.outer);
    }
    overrideHoles += accepted.length;
  }
  record.parkHoles = holes;
  handlePolygon(record.kind, record.outer, holes, record.seed, cover);
}
for (const battery of batteries) {
  if (!acceptedBatteries.has(battery)) {
    skippedBatteries.push(battery.name);
    continue;
  }
  handlePolygon(KIND.rock, battery.outer, [], battery.seed, null, 0.12);
}
console.log(`park cover overrides: ${records.filter((record) => record.cover).length} polygons, ${overrideHoles} holes`);
console.log(
  `battery platforms: ${acceptedBatteries.size} baked (${[...acceptedBatteries].map((b) => b.name).join(', ') || 'none'}); ` +
    `${batteryNodes.length} node-only skipped (${batteryNodes.join(', ') || 'none'}); ` +
    `${skippedBatteries.length} geometry skipped outside cover (${skippedBatteries.join(', ') || 'none'})`
);

// Stale cells from an earlier bake would linger and desync the index.
await rm(CELLS_OUT, { recursive: true, force: true });
await mkdir(CELLS_OUT, { recursive: true });
let bytes = 0;
const index = [];
for (const key of [...cells.keys()].sort()) {
  const cell = cells.get(key);
  if (cell.indices.length === 0 && cell.trees.length === 0) continue;
  const blob = writeLandcoverBlob(cell);
  await writeFile(new URL(`${key}.bin`, CELLS_OUT), blob);
  bytes += blob.length;
  index.push({
    key,
    cx: cell.cx,
    cz: cell.cz,
    originX: cell.originX,
    originZ: cell.originZ,
    tris: cell.indices.length / 3,
    trees: cell.trees.length / 4,
    bytes: blob.length,
  });
}

const missingParks = NAMED_PARKS.filter((p) => !parkHits[p.id]).map((p) => p.name);
const stats = {
  polygons,
  triangles,
  trees,
  cells: index.length,
  bytes,
  areaByKindKm2: areaByKind.map((a, i) => ({ kind: LAND_KINDS[i].id, km2: Math.round(a / 1e4) / 100 })),
  parkHits,
  missingParks,
};

await writeFile(new URL('landuse.bin', OUT), Buffer.from(landuse.buffer));

await writeFile(
  new URL('landcover.json', OUT),
  JSON.stringify(
    {
      cellSize: CELL_SIZE,
      grid: GRID,
      kinds: LAND_KINDS,
      raster: {
        size: RASTER,
        minX: EXTENT.minX,
        minZ: EXTENT.minZ,
        cellX: rasterCellX,
        cellZ: rasterCellZ,
      },
      stats,
      cells: index,
    },
    null,
    1
  )
);

console.log(
  `baked ${polygons} polygons / ${triangles} tris / ${trees} trees into ${index.length} cells, ` +
    `${(bytes / 1e6).toFixed(1)} MB`
);
if (missingParks.length) console.warn('! parks with no matching polygon:', missingParks.join(', '));
else console.log('all named parks matched');
