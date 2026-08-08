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
import { NAMED_PARKS } from './lib/landmarks.mjs';
import { LAND_KINDS } from './lib/classes.mjs';

const DATA = new URL('./data/', import.meta.url);
const OUT = new URL('./out/', import.meta.url);
const CELLS_OUT = new URL('./out/landcover/', import.meta.url);

const KIND = Object.fromEntries(LAND_KINDS.map((k, i) => [k.id, i]));
const MAX_EDGE = 55; // subdivide triangles longer than this so parks follow hills
const TREE_AREA_TREES = 90;
const TREE_AREA_PARK = 200;

const { sampleElevation } = await loadHeightmap();

function classify(tags) {
  if (!tags) return null;
  if (tags.natural === 'water' || tags.waterway || tags.landuse === 'reservoir') return KIND.water;
  if (tags.natural === 'beach' || tags.natural === 'sand') return KIND.sand;
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

function ringFromGeometry(geometry) {
  const ring = [];
  for (const p of geometry) {
    if (!p || !insideBBox(p.lon, p.lat)) continue;
    const [x, z] = project(p.lon, p.lat);
    ring.push(x, z);
  }
  return ring;
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
      const mab = [(ax + bx) / 2, (az + bz) / 2];
      const mbc = [(bx + cx) / 2, (bz + cz) / 2];
      const mca = [(cx + ax) / 2, (cz + az) / 2];
      tris.push(
        [ax, az, mab[0], mab[1], mca[0], mca[1]],
        [mab[0], mab[1], bx, bz, mbc[0], mbc[1]],
        [mca[0], mca[1], mbc[0], mbc[1], cx, cz],
        [mab[0], mab[1], mbc[0], mbc[1], mca[0], mca[1]]
      );
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

function addTriangle(kind, tri, waterLevel) {
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
      const y = kind === KIND.water ? waterLevel : sampleElevation(x, z) + 0.06;
      index = cell.verts.length / 3;
      cell.verts.push(x, y, z);
      cell.kinds.push(kind);
      cell.weld.set(key, index);
    }
    cell.indices.push(index);
  }
}

function scatterTrees(kind, outer, holes, area, seedBase) {
  const per = kind === KIND.trees ? TREE_AREA_TREES : TREE_AREA_PARK;
  const target = Math.floor(area / per);
  if (target <= 0) return 0;
  const [minX, minZ, maxX, maxZ] = ringBBox(outer);
  const w = maxX - minX;
  const d = maxZ - minZ;
  let placed = 0;
  const attempts = Math.min(target * 4, 400000);
  for (let i = 0; i < attempts && placed < target; i++) {
    const x = minX + hash01(seedBase + i * 2) * w;
    const z = minZ + hash01(seedBase + i * 2 + 1) * d;
    if (!pointInRing(x, z, outer)) continue;
    let inHole = false;
    for (const h of holes) {
      if (pointInRing(x, z, h)) {
        inHole = true;
        break;
      }
    }
    if (inHole) continue;
    const cell = cellFor(x, z);
    if (!cell) continue;
    cell.trees.push(x, sampleElevation(x, z), z, Math.floor(hash01(seedBase + i * 7) * 3));
    placed++;
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

let polygons = 0;
let triangles = 0;
let trees = 0;
const areaByKind = new Array(LAND_KINDS.length).fill(0);

function handlePolygon(kind, outerRing, holeRings, seedBase) {
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
  const tris = triangulateDraped(outerRing, holeRings, kind === KIND.water ? 400 : MAX_EDGE);
  for (const t of tris) addTriangle(kind, t, waterLevel);
  triangles += tris.length;
  polygons++;
  areaByKind[kind] += area;

  if (kind === KIND.trees || kind === KIND.grass) {
    trees += scatterTrees(kind, outerRing, holeRings, area, seedBase);
  }
}

let seedCounter = 1;
for (const el of raw.elements) {
  const kind = classify(el.tags);
  if (kind === null) continue;
  seedCounter += 9176;
  if (el.type === 'way' && Array.isArray(el.geometry)) {
    handlePolygon(kind, ringFromGeometry(el.geometry), [], seedCounter);
  } else if (el.type === 'relation' && Array.isArray(el.members)) {
    const rings = stitchRings(el.members);
    const outers = rings.filter((r) => r.role !== 'inner').map((r) => ringFromGeometry(r.pts));
    const inners = rings.filter((r) => r.role === 'inner').map((r) => ringFromGeometry(r.pts));
    for (const outer of outers) {
      if (outer.length / 2 < 3) continue;
      const bbox = ringBBox(outer);
      const holes = inners.filter((h) => {
        if (h.length / 2 < 3) return false;
        const [hx, hz] = ringCentroid(h);
        return hx >= bbox[0] && hx <= bbox[2] && hz >= bbox[1] && hz <= bbox[3];
      });
      handlePolygon(kind, outer, holes, (seedCounter += 313));
    }
  }
}

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
