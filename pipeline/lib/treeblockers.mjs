// Tree-placement veto oracle, shared by the landcover scatter and the toy
// densifier. A tree may not stand inside a building footprint, on a roadway or
// in water — OSM landcover polygons contain all three (park drives are separate
// ways, not holes, and forest polygons overlap the Presidio's housing).
//
// One flat occupancy grid over the whole city extent: bit 1 = building
// footprint (dilated by one cell so a canopy cannot clip a wall), bit 2 =
// street corridor (ribbon half-width + 1.5 m, every class including the
// elevated ones).

import { readdir } from 'node:fs/promises';
import { CELL_SIZE, GRID } from './geo.mjs';
import { STREET_CLASSES } from './classes.mjs';
import { readBuildingsBlob, readStreetsBlob } from './blobread.mjs';

export const BLOCK_RES = 2.5; // grid resolution in meters
export const CORRIDOR_MARGIN = 1.5; // meters of shoulder beyond the road ribbon
export const WATER_ELEVATION = 0.35; // landcover sits at +0.06, water at >= 0.25
// Tree coordinates are quantised to 2 cm when the blob is written, so a
// candidate sitting exactly on a grid seam could decode into the neighbouring
// (blocked) cell. Test the quantisation neighbourhood, not the bare point.
const EPS = 0.05;

const BIT_BUILDING = 1;
const BIT_STREET = 2;

const COLS = Math.ceil((GRID.cols * CELL_SIZE) / BLOCK_RES);
const ROWS = Math.ceil((GRID.rows * CELL_SIZE) / BLOCK_RES);

const colOf = (x) => Math.floor((x - GRID.originX) / BLOCK_RES);
const rowOf = (z) => Math.floor((z - GRID.originZ) / BLOCK_RES);
const centerX = (i) => GRID.originX + (i + 0.5) * BLOCK_RES;
const centerZ = (j) => GRID.originZ + (j + 0.5) * BLOCK_RES;

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

function distanceToSegment(ax, az, bx, bz, x, z) {
  const dx = bx - ax;
  const dz = bz - az;
  const l2 = dx * dx + dz * dz || 1;
  const t = Math.min(1, Math.max(0, ((x - ax) * dx + (z - az) * dz) / l2));
  return Math.hypot(x - (ax + dx * t), z - (az + dz * t));
}

function rasterizeRing(grid, ring) {
  let minX = Infinity;
  let maxX = -Infinity;
  let minZ = Infinity;
  let maxZ = -Infinity;
  for (let i = 0; i < ring.length; i += 2) {
    if (ring[i] < minX) minX = ring[i];
    if (ring[i] > maxX) maxX = ring[i];
    if (ring[i + 1] < minZ) minZ = ring[i + 1];
    if (ring[i + 1] > maxZ) maxZ = ring[i + 1];
  }
  const i0 = Math.max(0, colOf(minX));
  const i1 = Math.min(COLS - 1, colOf(maxX));
  const j0 = Math.max(0, rowOf(minZ));
  const j1 = Math.min(ROWS - 1, rowOf(maxZ));
  let marked = 0;
  for (let j = j0; j <= j1; j++) {
    const z = centerZ(j);
    for (let i = i0; i <= i1; i++) {
      if (!pointInRing(centerX(i), z, ring)) continue;
      grid[j * COLS + i] |= BIT_BUILDING;
      marked++;
    }
  }
  // A footprint smaller than one grid cell still deserves a veto.
  if (marked === 0) {
    const i = Math.min(COLS - 1, Math.max(0, colOf((minX + maxX) / 2)));
    const j = Math.min(ROWS - 1, Math.max(0, rowOf((minZ + maxZ) / 2)));
    grid[j * COLS + i] |= BIT_BUILDING;
  }
}

function dilateBuildings(grid) {
  const src = grid.slice();
  for (let j = 0; j < ROWS; j++) {
    for (let i = 0; i < COLS; i++) {
      const k = j * COLS + i;
      if (!(src[k] & BIT_BUILDING)) continue;
      for (let dj = -1; dj <= 1; dj++) {
        const jj = j + dj;
        if (jj < 0 || jj >= ROWS) continue;
        for (let di = -1; di <= 1; di++) {
          const ii = i + di;
          if (ii < 0 || ii >= COLS) continue;
          grid[jj * COLS + ii] |= BIT_BUILDING;
        }
      }
    }
  }
}

function rasterizeSegment(grid, x0, z0, x1, z1, radius) {
  const i0 = Math.max(0, colOf(Math.min(x0, x1) - radius));
  const i1 = Math.min(COLS - 1, colOf(Math.max(x0, x1) + radius));
  const j0 = Math.max(0, rowOf(Math.min(z0, z1) - radius));
  const j1 = Math.min(ROWS - 1, rowOf(Math.max(z0, z1) + radius));
  for (let j = j0; j <= j1; j++) {
    const z = centerZ(j);
    for (let i = i0; i <= i1; i++) {
      if (distanceToSegment(x0, z0, x1, z1, centerX(i), z) <= radius) grid[j * COLS + i] |= BIT_STREET;
    }
  }
}

// `out` is the pipeline's out/ directory URL; the buildings and streets bakes
// must already have run.
export async function loadTreeBlockers({ sampleElevation, out = new URL('../out/', import.meta.url) }) {
  const grid = new Uint8Array(COLS * ROWS);

  let footprints = 0;
  const buildingFiles = (await readdir(new URL('buildings/', out))).filter((f) => f.endsWith('.bin'));
  for (const file of buildingFiles.sort()) {
    const blob = await readBuildingsBlob(new URL(`buildings/${file}`, out));
    for (const b of blob.buildings) {
      rasterizeRing(grid, b.ring);
      footprints++;
    }
  }
  dilateBuildings(grid);

  let segments = 0;
  const streetFiles = (await readdir(new URL('streets/', out))).filter((f) => f.endsWith('.bin'));
  for (const file of streetFiles.sort()) {
    const blob = await readStreetsBlob(new URL(`streets/${file}`, out));
    for (const line of blob.lines) {
      const radius = STREET_CLASSES[line.klass].width / 2 + CORRIDOR_MARGIN;
      for (let i = 0; i + 5 < line.pts.length; i += 3) {
        rasterizeSegment(grid, line.pts[i], line.pts[i + 2], line.pts[i + 3], line.pts[i + 5], radius);
        segments++;
      }
    }
  }

  const cellAt = (x, z) => {
    const i = colOf(x);
    const j = rowOf(z);
    if (i < 0 || j < 0 || i >= COLS || j >= ROWS) return 0;
    return grid[j * COLS + i];
  };

  const cellFlags = (x, z) =>
    cellAt(x - EPS, z - EPS) | cellAt(x + EPS, z - EPS) | cellAt(x - EPS, z + EPS) | cellAt(x + EPS, z + EPS);

  // A roof tree must sit on the footprint itself, so it tests the bare cell.
  const onBuilding = (x, z) => (cellAt(x, z) & BIT_BUILDING) !== 0;
  const inBuilding = (x, z) => (cellFlags(x, z) & BIT_BUILDING) !== 0;
  const inStreet = (x, z) => (cellFlags(x, z) & BIT_STREET) !== 0;
  const inWater = (x, z) => sampleElevation(x, z) < WATER_ELEVATION;
  const blocked = (x, z) => cellFlags(x, z) !== 0 || inWater(x, z);

  return {
    blocked,
    onBuilding,
    inBuilding,
    inStreet,
    inWater,
    stats: { res: BLOCK_RES, cols: COLS, rows: ROWS, footprints, segments },
  };
}
