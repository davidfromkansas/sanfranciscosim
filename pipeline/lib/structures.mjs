// OSM highway structures: which freeway sections ride a viaduct (bridge/layer
// tags) and the real centrelines of the two bespoke bridges. Shared by
// streets.mjs (elevated decks + piers) and bridges.mjs (deck geometry).

import { readFile } from 'node:fs/promises';
import { project } from './geo.mjs';
import { densify } from './poly.mjs';

const DATA = new URL('../data/', import.meta.url);

// Deck height above ground for an OSM layer value. Layer 1 is a normal viaduct,
// each further layer is another structure stacked on top of it.
export function deckHeightForLayer(layer) {
  return 7 + 5 * (Math.max(1, layer) - 1);
}

const LOOKUP_CELL = 40;

export async function loadStructures() {
  const osm = JSON.parse(await readFile(new URL('osm_structures.json', DATA), 'utf8'));
  const ways = (osm.elements || []).filter((el) => Array.isArray(el.geometry) && el.geometry.length >= 2);

  // ---- elevated freeway lookup -------------------------------------------
  // Every bridge-tagged motorway/trunk way, densified to 8 m so a nearest-point
  // lookup is dense enough for the 10 m street sampling.
  const grid = new Map();
  const add = (x, z, layer) => {
    const key = `${Math.floor(x / LOOKUP_CELL)}:${Math.floor(z / LOOKUP_CELL)}`;
    let list = grid.get(key);
    if (!list) grid.set(key, (list = []));
    list.push([x, z, layer]);
  };
  let elevatedWays = 0;
  for (const way of ways) {
    if (!way.tags?.bridge) continue;
    elevatedWays++;
    const layer = Math.abs(parseInt(way.tags.layer ?? '1', 10)) || 1;
    const flat = [];
    for (const p of way.geometry) {
      if (!p) continue;
      const [x, z] = project(p.lon, p.lat);
      flat.push(x, z);
    }
    const dense = densify(flat, 8);
    for (let i = 0; i < dense.length; i += 2) add(dense[i], dense[i + 1], layer);
  }

  // Returns the OSM layer of the viaduct under (x, z), or 0 when at grade.
  function elevatedLayer(x, z, radius = 22) {
    const ci = Math.floor(x / LOOKUP_CELL);
    const cj = Math.floor(z / LOOKUP_CELL);
    let best = 0;
    let bestDist = radius * radius;
    for (let dj = -1; dj <= 1; dj++) {
      for (let di = -1; di <= 1; di++) {
        const list = grid.get(`${ci + di}:${cj + dj}`);
        if (!list) continue;
        for (const [px, pz, layer] of list) {
          const d = (px - x) ** 2 + (pz - z) ** 2;
          if (d < bestDist) {
            bestDist = d;
            best = layer;
          }
        }
      }
    }
    return best;
  }

  // ---- bespoke bridge centrelines ----------------------------------------
  // Golden Gate: the two long carriageway ways, ordered south to north.
  const ggWays = ways
    .filter((w) => w.tags?.name === 'Golden Gate Bridge')
    .sort((a, b) => b.geometry.length - a.geometry.length);
  const goldenGate = ggWays.length ? orderSouthNorth(ggWays[0].geometry) : [];

  // Bay Bridge: one carriageway per span, picked as the longest bridge-tagged
  // I 80 way on each side of the Yerba Buena tunnel (the tunnel itself is not a
  // bridge, so the two spans never share a way).
  const bayWays = ways.filter((w) => /I 80/.test(w.tags?.ref || '') && w.tags?.bridge && w.geometry.every((p) => p && p.lat > 37.77));
  const bayWest = longestWay(bayWays, (lon) => lon < -122.365);
  const bayEast = longestWay(bayWays, (lon) => lon > -122.366);

  // ---- real bridge tower positions ---------------------------------------
  // OSM maps each tower as several stacked building:part ways (one per height
  // band) plus one way per leg, so cluster them and keep the tallest height.
  const towerParts = [];
  for (const way of ways) {
    const tags = way.tags || {};
    if (tags.man_made !== 'tower' || !(tags['bridge:support'] || tags['tower:type'] === 'bridge')) continue;
    let sx = 0;
    let sz = 0;
    let n = 0;
    for (const p of way.geometry) {
      if (!p) continue;
      const [x, z] = project(p.lon, p.lat);
      sx += x;
      sz += z;
      n++;
    }
    if (!n) continue;
    towerParts.push({ x: sx / n, z: sz / n, height: parseFloat(tags.height) || 0 });
  }
  const towers = [];
  for (const part of towerParts) {
    const near = towers.find((t) => Math.hypot(t.x - part.x, t.z - part.z) < 70);
    if (near) {
      near.x = (near.x * near.n + part.x) / (near.n + 1);
      near.z = (near.z * near.n + part.z) / (near.n + 1);
      near.n++;
      near.height = Math.max(near.height, part.height);
    } else {
      towers.push({ x: part.x, z: part.z, height: part.height, n: 1 });
    }
  }

  return { elevatedLayer, elevatedWays, goldenGate, bayWest, bayEast, towers };
}

// Longest way (in metres) whose points all satisfy the longitude predicate,
// returned west to east.
function longestWay(ways, lonTest) {
  let best = [];
  let bestLen = 0;
  for (const way of ways) {
    const pts = way.geometry.filter(Boolean).map((p) => [p.lon, p.lat]);
    if (pts.length < 2 || !pts.every((p) => lonTest(p[0]))) continue;
    let len = 0;
    for (let i = 1; i < pts.length; i++) {
      const [ax, az] = project(pts[i - 1][0], pts[i - 1][1]);
      const [bx, bz] = project(pts[i][0], pts[i][1]);
      len += Math.hypot(bx - ax, bz - az);
    }
    if (len > bestLen) {
      bestLen = len;
      best = pts;
    }
  }
  if (best.length > 1 && best[0][0] > best[best.length - 1][0]) best.reverse();
  return dedupe(best);
}

function orderSouthNorth(geometry) {
  const pts = geometry.filter(Boolean).map((p) => [p.lon, p.lat]);
  if (pts.length > 1 && pts[0][1] > pts[pts.length - 1][1]) pts.reverse();
  return dedupe(pts);
}

function dedupe(pts) {
  const out = [];
  for (const p of pts) {
    const last = out[out.length - 1];
    if (last && Math.abs(last[0] - p[0]) < 1e-6 && Math.abs(last[1] - p[1]) < 1e-6) continue;
    out.push(p);
  }
  return out;
}
