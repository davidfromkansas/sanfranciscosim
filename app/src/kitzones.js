// The fabric map the kit is placed against.
//
// The context layer's 41 neighbourhood polygons are burned once into a 100 m
// raster of zone ids, so the tile worker can answer "what does this block look
// like in real life?" for a few thousand footprints without shipping polygons
// or doing point-in-polygon per building.

import { tileUrl } from './data.js';
import { NEIGHBORHOOD_ZONE, ZONE } from './kitplan.js';

const CELL = 100;

function ringsBounds(rings) {
  let minX = Infinity;
  let maxX = -Infinity;
  let minZ = Infinity;
  let maxZ = -Infinity;
  for (const ring of rings) {
    for (let i = 0; i < ring.length; i += 2) {
      if (ring[i] < minX) minX = ring[i];
      if (ring[i] > maxX) maxX = ring[i];
      if (ring[i + 1] < minZ) minZ = ring[i + 1];
      if (ring[i + 1] > maxZ) maxZ = ring[i + 1];
    }
  }
  return { minX, maxX, minZ, maxZ };
}

function inRings(x, z, rings) {
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

/** Rasterises the neighbourhood polygons into a transferable zone grid. */
export async function loadKitZones(extent) {
  const res = await fetch(tileUrl('context/neighborhoods.json'));
  if (!res.ok) throw new Error(`neighborhoods: ${res.status}`);
  const neighborhoods = await res.json();

  const originX = Math.floor(extent.minX / CELL) * CELL;
  const originZ = Math.floor(extent.minZ / CELL) * CELL;
  const cols = Math.ceil((extent.maxX - originX) / CELL) + 1;
  const rows = Math.ceil((extent.maxZ - originZ) / CELL) + 1;
  const grid = { originX, originZ, cell: CELL, cols, rows, data: new Uint8Array(cols * rows) };

  for (const nhood of neighborhoods) {
    const zone = NEIGHBORHOOD_ZONE[nhood.name];
    if (zone === undefined || zone === ZONE.OTHER) continue;
    const box = ringsBounds(nhood.rings);
    const x0 = Math.max(0, Math.floor((box.minX - originX) / CELL));
    const x1 = Math.min(cols - 1, Math.ceil((box.maxX - originX) / CELL));
    const z0 = Math.max(0, Math.floor((box.minZ - originZ) / CELL));
    const z1 = Math.min(rows - 1, Math.ceil((box.maxZ - originZ) / CELL));
    for (let gz = z0; gz <= z1; gz++) {
      const z = originZ + gz * CELL + CELL / 2;
      for (let gx = x0; gx <= x1; gx++) {
        const x = originX + gx * CELL + CELL / 2;
        if (inRings(x, z, nhood.rings)) grid.data[gz * cols + gx] = zone;
      }
    }
  }
  return grid;
}

/**
 * Landmarks win: a disc around every hand-made or code-built landmark where no
 * kit piece is allowed to stand.
 */
export function landmarkExclusions(manifest, project) {
  const out = [];
  for (const landmark of manifest.landmarks || []) {
    const [x, z] = project(landmark.lon, landmark.lat);
    out.push(x, z, landmark.exclude || Math.max(60, (landmark.height || 60) * 0.6));
  }
  return new Float32Array(out);
}
