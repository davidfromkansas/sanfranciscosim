// Bakes DataSF street centerlines into per-cell polyline blobs, draped onto the
// terrain. The runtime turns them into road ribbons and reuses the same
// polylines as traffic paths.

import { mkdir, rm, writeFile, readFile } from 'node:fs/promises';
import { CELL_SIZE, GRID, cellIndex, cellOrigin, insideBBox, project } from './lib/geo.mjs';
import { densify, polylineLength } from './lib/poly.mjs';
import { loadHeightmap } from './lib/heightmap.mjs';
import { writeStreetsBlob } from './lib/binio.mjs';
import { CLASS_BY_CODE, STREET_CLASSES } from './lib/classes.mjs';
import { deckHeightForLayer, loadStructures } from './lib/structures.mjs';

const DATA = new URL('./data/', import.meta.url);
const OUT = new URL('./out/', import.meta.url);
const CELLS_OUT = new URL('./out/streets/', import.meta.url);

const { sampleElevation } = await loadHeightmap();
const structures = await loadStructures();
console.log(`${structures.elevatedWays} bridge-tagged OSM highway ways for elevated decks`);

const FREEWAY = STREET_CLASSES.findIndex((c) => c.id === 'freeway');
const RAMP = STREET_CLASSES.findIndex((c) => c.id === 'ramp');
const PIER_SPACING = 32;
const piers = [];

// The two bespoke bridges carry the roadway across the water themselves, so the
// DataSF ribbon that follows the same centreline rides on their deck instead of
// hovering over the bay on its own piers.
const DECK_CORRIDOR = 45;
const DECK_SURFACE = 1.5;
const DECK_BLEND_PASSES = 20;
const bridgeSpec = JSON.parse(await readFile(new URL('bridges.json', OUT), 'utf8'));
const deckLines = [];
for (const spec of Object.values(bridgeSpec)) {
  for (const nodes of [spec.nodes, spec.east?.nodes]) {
    if (!nodes) continue;
    deckLines.push(
      nodes.map(([lon, lat, y]) => {
        const [x, z] = project(lon, lat);
        return [x, z, y];
      })
    );
  }
}

// Deck surface height at (x, z) if it is inside a bespoke bridge corridor.
function deckSurfaceAt(x, z) {
  let best = null;
  let bestD = DECK_CORRIDOR;
  for (const line of deckLines) {
    for (let i = 1; i < line.length; i++) {
      const [ax, az, ay] = line[i - 1];
      const [bx, bz, by] = line[i];
      const dx = bx - ax;
      const dz = bz - az;
      const l2 = dx * dx + dz * dz || 1;
      const t = Math.min(1, Math.max(0, ((x - ax) * dx + (z - az) * dz) / l2));
      const d = Math.hypot(x - (ax + dx * t), z - (az + dz * t));
      if (d < bestD) {
        bestD = d;
        best = ay + (by - ay) * t + DECK_SURFACE;
      }
    }
  }
  return best;
}

// Deck offset above ground for every point of a freeway/ramp polyline: the OSM
// bridge tag decides where it is elevated, then the profile is blurred so the
// deck ramps up and down instead of stepping.
function deckOffsets(pts) {
  const n = pts.length / 2;
  const raw = new Float64Array(n);
  const onBridge = new Uint8Array(n);
  let any = false;
  for (let i = 0; i < n; i++) {
    const x = pts[i * 2];
    const z = pts[i * 2 + 1];
    const deck = deckSurfaceAt(x, z);
    if (deck !== null) {
      raw[i] = deck - sampleElevation(x, z);
      onBridge[i] = 1;
      any = true;
      continue;
    }
    const layer = structures.elevatedLayer(x, z);
    if (layer) {
      raw[i] = deckHeightForLayer(layer);
      any = true;
    }
  }
  if (!any) return null;
  // Points on a bespoke deck must match it exactly, so they are pinned through
  // the smoothing rather than restored after it: that way the height of a deck
  // the approach has to reach diffuses outward instead of leaving a step where
  // the corridor ends. Samples are 10 m apart, so the passes set how long the
  // approach viaduct has to climb.
  let cur = raw;
  for (let pass = 0; pass < DECK_BLEND_PASSES; pass++) {
    const next = new Float64Array(n);
    for (let i = 0; i < n; i++) {
      if (onBridge[i]) {
        next[i] = raw[i];
        continue;
      }
      const a = cur[Math.max(0, i - 1)];
      const b = cur[i];
      const c = cur[Math.min(n - 1, i + 1)];
      next[i] = a * 0.25 + b * 0.5 + c * 0.25;
    }
    cur = next;
  }
  return { offsets: cur, onBridge };
}

const geo = JSON.parse(await readFile(new URL('streets_datasf.geojson', DATA), 'utf8'));
console.log(`${geo.features.length} raw street features`);

const cells = new Map();
function cellFor(key, cx, cz) {
  let cell = cells.get(key);
  if (!cell) {
    const [ox, oz] = cellOrigin(cx, cz);
    cells.set(key, (cell = { key, cx, cz, originX: ox, originZ: oz, lines: [] }));
  }
  return cell;
}

let kept = 0;
let dropped = 0;
let totalLength = 0;
const nameHits = new Map();

for (const f of geo.features) {
  const p = f.properties || {};
  // "Streets – Active and Retired": retired segments carry a date_dropped.
  if (p.date_dropped) {
    dropped++;
    continue;
  }
  if (p.layer && /PAPER|PROPOSED/i.test(p.layer)) {
    dropped++;
    continue;
  }
  const geom = f.geometry;
  if (!geom) continue;
  const lines = geom.type === 'LineString' ? [geom.coordinates] : geom.coordinates || [];
  const code = parseInt(p.classcode, 10);
  const klass = CLASS_BY_CODE[Number.isFinite(code) ? code : 0] ?? 6;
  const name = (p.streetname || '').toUpperCase();
  if (name) nameHits.set(name, (nameHits.get(name) || 0) + 1);

  for (const coords of lines) {
    if (!coords || coords.length < 2) continue;
    const projected = [];
    for (const c of coords) {
      if (!insideBBox(c[0], c[1])) continue;
      const [x, z] = project(c[0], c[1]);
      projected.push(x, z);
    }
    if (projected.length < 4) continue;
    const len = polylineLength(projected);
    if (len < 4) continue;
    totalLength += len;

    // Sample terrain every ~10 m so ribbons follow the hills.
    const pts = densify(projected, 10);
    const deck = klass === FREEWAY || klass === RAMP ? deckOffsets(pts) : null;
    const elevated = deck?.offsets ?? null;

    // Support columns under every elevated stretch (the bespoke bridges bring
    // their own towers and columns).
    if (elevated) {
      let sinceLast = PIER_SPACING;
      for (let i = 0; i < pts.length; i += 2) {
        const x = pts[i];
        const z = pts[i + 1];
        if (i > 0) sinceLast += Math.hypot(x - pts[i - 2], z - pts[i - 1]);
        const offset = elevated[i / 2];
        if (deck.onBridge[i / 2] || offset < 4 || sinceLast < PIER_SPACING) continue;
        sinceLast = 0;
        const ground = sampleElevation(x, z);
        piers.push([Math.round(x * 10) / 10, Math.round(z * 10) / 10, Math.round(ground * 10) / 10, Math.round((ground + offset) * 10) / 10]);
      }
    }

    // Split the polyline at cell boundaries, duplicating the crossing vertex so
    // ribbons stay continuous across cells.
    let current = null;
    let currentKey = null;
    for (let i = 0; i < pts.length; i += 2) {
      const x = pts[i];
      const z = pts[i + 1];
      const idx = cellIndex(x, z);
      if (!idx) {
        current = null;
        currentKey = null;
        continue;
      }
      if (idx.key !== currentKey) {
        const prev = current;
        current = { pts: [], y: [], klass, flags: 0 };
        currentKey = idx.key;
        cellFor(idx.key, idx.cx, idx.cz).lines.push(current);
        if (prev && prev.pts.length >= 2) {
          const n = prev.pts.length;
          current.pts.push(prev.pts[n - 2], prev.pts[n - 1]);
          current.y.push(prev.y[prev.y.length - 1]);
        }
      }
      current.pts.push(x, z);
      current.y.push(sampleElevation(x, z) + 0.15 + (elevated ? elevated[i / 2] : 0));
    }
    kept++;
  }
}

// Drop degenerate one-point fragments produced by boundary splitting.
for (const cell of cells.values()) {
  cell.lines = cell.lines.filter((l) => l.pts.length >= 4);
}

// Stale cells from an earlier bake would linger and desync the index.
await rm(CELLS_OUT, { recursive: true, force: true });
await mkdir(CELLS_OUT, { recursive: true });
let bytes = 0;
const index = [];
for (const key of [...cells.keys()].sort()) {
  const cell = cells.get(key);
  if (cell.lines.length === 0) continue;
  const blob = writeStreetsBlob(cell);
  await writeFile(new URL(`${key}.bin`, CELLS_OUT), blob);
  bytes += blob.length;
  index.push({
    key,
    cx: cell.cx,
    cz: cell.cz,
    originX: cell.originX,
    originZ: cell.originZ,
    lines: cell.lines.length,
    bytes: blob.length,
  });
}

await writeFile(new URL('piers.json', OUT), JSON.stringify({ spacing: PIER_SPACING, piers }));

const spotChecks = ['MARKET ST', 'LOMBARD ST', 'COLUMBUS AVE', 'THE EMBARCADERO', 'GREAT HWY'];
const stats = {
  segments: kept,
  droppedRetired: dropped,
  totalLengthKm: Math.round(totalLength / 1000),
  cells: index.length,
  bytes,
  piers: piers.length,
  spotChecks: Object.fromEntries(spotChecks.map((n) => [n, nameHits.get(n) || 0])),
};

await writeFile(
  new URL('streets.json', OUT),
  JSON.stringify({ cellSize: CELL_SIZE, grid: GRID, classes: STREET_CLASSES, stats, cells: index }, null, 1)
);

console.log(
  `baked ${kept} segments (${stats.totalLengthKm} km) into ${index.length} cells, ${(bytes / 1e6).toFixed(1)} MB`
);
console.log('spot checks:', stats.spotChecks);
console.log(`${piers.length} viaduct piers`);
