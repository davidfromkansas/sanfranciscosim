// Bucketed point -> footprint join (Appendix E). Every POI resolves against the
// footprints in its own 500 m cell plus the eight neighbours, never the whole
// city, which keeps the full multi-source join in the tens of seconds.

import { CELL_SIZE, GRID } from '../lib/geo.mjs';

export function inRing(x, z, ring) {
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

export function inPolygonLonLat(lon, lat, ring) {
  let inside = false;
  for (let i = 0, j = ring.length - 1; i < ring.length; j = i++) {
    const [xi, yi] = ring[i];
    const [xj, yj] = ring[j];
    if (yi > lat !== yj > lat && lon < ((xj - xi) * (lat - yi)) / (yj - yi) + xi) inside = !inside;
  }
  return inside;
}

// A uniform grid over the projected city, keyed on the tile grid so the join and
// the tile bake agree about which cell anything belongs to.
export class CellIndex {
  constructor(size = CELL_SIZE) {
    this.size = size;
    this.map = new Map();
  }

  key(x, z) {
    return `${Math.floor((x - GRID.originX) / this.size)}:${Math.floor((z - GRID.originZ) / this.size)}`;
  }

  add(x, z, value) {
    const k = this.key(x, z);
    let list = this.map.get(k);
    if (!list) this.map.set(k, (list = []));
    list.push(value);
  }

  addBBox(bbox, value) {
    const i0 = Math.floor((bbox[0] - GRID.originX) / this.size);
    const i1 = Math.floor((bbox[2] - GRID.originX) / this.size);
    const j0 = Math.floor((bbox[1] - GRID.originZ) / this.size);
    const j1 = Math.floor((bbox[3] - GRID.originZ) / this.size);
    for (let j = j0; j <= j1; j++) {
      for (let i = i0; i <= i1; i++) {
        const k = `${i}:${j}`;
        let list = this.map.get(k);
        if (!list) this.map.set(k, (list = []));
        list.push(value);
      }
    }
  }

  near(x, z) {
    const ci = Math.floor((x - GRID.originX) / this.size);
    const cj = Math.floor((z - GRID.originZ) / this.size);
    const out = [];
    for (let dj = -1; dj <= 1; dj++) {
      for (let di = -1; di <= 1; di++) {
        const list = this.map.get(`${ci + di}:${cj + dj}`);
        if (list) out.push(...list);
      }
    }
    return out;
  }
}

// Containing footprint first, then the nearest centroid within `maxDist`.
export function matchFootprint(index, buildings, x, z, maxDist = 30) {
  const candidates = index.near(x, z);
  let nearest = -1;
  let nearestD = maxDist * maxDist;
  for (const idx of candidates) {
    const b = buildings[idx];
    const bb = b.bbox;
    if (x >= bb[0] && x <= bb[2] && z >= bb[1] && z <= bb[3] && inRing(x, z, b.ring)) {
      return { idx, exact: true };
    }
    const d = (b.x - x) ** 2 + (b.z - z) ** 2;
    if (d < nearestD) {
      nearestD = d;
      nearest = idx;
    }
  }
  return nearest >= 0 ? { idx: nearest, exact: false } : null;
}
