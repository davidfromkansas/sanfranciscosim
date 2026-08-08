// Bakes DataSF street centerlines into per-cell polyline blobs, draped onto the
// terrain. The runtime turns them into road ribbons and reuses the same
// polylines as traffic paths.

import { mkdir, writeFile, readFile } from 'node:fs/promises';
import { CELL_SIZE, GRID, cellIndex, cellOrigin, insideBBox, project } from './lib/geo.mjs';
import { densify, polylineLength } from './lib/poly.mjs';
import { loadHeightmap } from './lib/heightmap.mjs';
import { writeStreetsBlob } from './lib/binio.mjs';
import { CLASS_BY_CODE, STREET_CLASSES } from './lib/classes.mjs';

const DATA = new URL('./data/', import.meta.url);
const OUT = new URL('./out/', import.meta.url);
const CELLS_OUT = new URL('./out/streets/', import.meta.url);

const { sampleElevation } = await loadHeightmap();

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
      current.y.push(sampleElevation(x, z) + 0.15);
    }
    kept++;
  }
}

// Drop degenerate one-point fragments produced by boundary splitting.
for (const cell of cells.values()) {
  cell.lines = cell.lines.filter((l) => l.pts.length >= 4);
}

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

const spotChecks = ['MARKET ST', 'LOMBARD ST', 'COLUMBUS AVE', 'THE EMBARCADERO', 'GREAT HWY'];
const stats = {
  segments: kept,
  droppedRetired: dropped,
  totalLengthKm: Math.round(totalLength / 1000),
  cells: index.length,
  bytes,
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
