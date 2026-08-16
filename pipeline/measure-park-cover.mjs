import { readFile, stat } from 'node:fs/promises';
import { cellIndex, project } from './lib/geo.mjs';

const ROOT = new URL('./', import.meta.url);
const bbox = [-122.4855, 37.7865, -122.4465, 37.8115];
const args = new Map(
  process.argv.slice(2).map((arg) => {
    const [key, value] = arg.replace(/^--/, '').split('=');
    return [key, value];
  })
);
const [minLon, minLat, maxLon, maxLat] = (args.get('bbox') || bbox.join(','))
  .split(',')
  .map(Number);
const anchor = (args.get('anchor') || `${(minLon + maxLon) / 2},${(minLat + maxLat) / 2}`)
  .split(',')
  .map(Number);
const [minX, minZ] = project(minLon, maxLat);
const [maxX, maxZ] = project(maxLon, minLat);

function touchedCells() {
  const keys = new Set();
  for (const [lon, lat] of [
    [minLon, minLat],
    [minLon, maxLat],
    [maxLon, minLat],
    [maxLon, maxLat],
  ]) {
    const [x, z] = project(lon, lat);
    const cell = cellIndex(x, z);
    if (cell) keys.add(cell.key);
  }
  const first = cellIndex(minX, minZ);
  const last = cellIndex(maxX, maxZ);
  for (let cx = first.cx; cx <= last.cx; cx++) {
    for (let cz = first.cz; cz <= last.cz; cz++) keys.add(`${cx}_${cz}`);
  }
  return [...keys].sort((a, b) => a.localeCompare(b, undefined, { numeric: true }));
}

function pointInRing(x, z, ring) {
  let inside = false;
  for (let i = 0, j = ring.length - 1; i < ring.length; j = i++) {
    const [xi, zi] = ring[i];
    const [xj, zj] = ring[j];
    if (zi > z !== zj > z && x < ((xj - xi) * (z - zi)) / (zj - zi) + xi) inside = !inside;
  }
  return inside;
}

function ringArea(ring) {
  let area = 0;
  for (let i = 0; i < ring.length; i++) {
    const j = (i + 1) % ring.length;
    area += ring[i][0] * ring[j][1] - ring[j][0] * ring[i][1];
  }
  return Math.abs(area) / 2;
}

function relationBoundary(elements) {
  const relation = elements.find((e) => e.type === 'relation' && e.id === 8346137);
  if (!relation) return null;
  const fragments = relation.members
    .filter((m) => m.type === 'way' && m.role === 'outer' && m.geometry?.length > 1)
    .map((m) => m.geometry.map((p) => project(p.lon, p.lat)));
  const rings = [];
  const used = new Set();
  const same = (a, b) => Math.abs(a[0] - b[0]) < 0.02 && Math.abs(a[1] - b[1]) < 0.02;
  for (let i = 0; i < fragments.length; i++) {
    if (used.has(i)) continue;
    used.add(i);
    let ring = fragments[i].slice();
    let changed = true;
    while (changed) {
      changed = false;
      for (let j = 0; j < fragments.length; j++) {
        if (used.has(j)) continue;
        const candidate = fragments[j];
        if (same(ring[ring.length - 1], candidate[0])) ring = ring.concat(candidate.slice(1));
        else if (same(ring[ring.length - 1], candidate[candidate.length - 1]))
          ring = ring.concat(candidate.slice(0, -1).reverse());
        else if (same(ring[0], candidate[candidate.length - 1]))
          ring = candidate.slice(0, -1).concat(ring);
        else if (same(ring[0], candidate[0])) ring = candidate.slice(1).reverse().concat(ring);
        else continue;
        used.add(j);
        changed = true;
      }
    }
    if (ring.length > 2) rings.push(ring);
  }
  return rings.length ? rings : null;
}

const keys = touchedCells();
const landcover = JSON.parse(await readFile(new URL('out/landcover.json', ROOT), 'utf8'));
const kinds = Object.fromEntries(landcover.kinds.map((kind, i) => [i, kind.id]));
const bytes = {};
for (const tier of ['landcover', 'toyland']) {
  bytes[tier] = {};
  for (const key of keys) {
    try {
      bytes[tier][key] = (await stat(new URL(`out/${tier}/${key}.bin`, ROOT))).size;
    } catch {
      bytes[tier][key] = 0;
    }
  }
}
const byteTotals = Object.fromEntries(
  Object.entries(bytes).map(([tier, entries]) => [
    tier,
    Object.values(entries).reduce((sum, value) => sum + value, 0),
  ])
);

const raster = landcover.raster;
const landuse = new Uint8Array(await readFile(new URL('out/landuse.bin', ROOT)));
const relationData = JSON.parse(await readFile(new URL('data/osm_landcover.json', ROOT), 'utf8'));
const rings = relationBoundary(relationData.elements);
const samples = {};
let total = 0;
const spacing = 22;
for (let z = minZ; z <= maxZ; z += spacing) {
  for (let x = minX; x <= maxX; x += spacing) {
    if (rings && !rings.some((ring) => pointInRing(x, z, ring))) continue;
    const col = Math.max(0, Math.min(raster.size - 1, Math.floor((x - raster.minX) / raster.cellX)));
    const row = Math.max(0, Math.min(raster.size - 1, Math.floor((z - raster.minZ) / raster.cellZ)));
    const kind = kinds[landuse[row * raster.size + col]] || 'unknown';
    samples[kind] = (samples[kind] || 0) + 1;
    total++;
  }
}
const mix = Object.fromEntries(
  Object.entries(samples).map(([kind, count]) => [kind, { count, percent: (count * 100) / total }])
);

const result = {
  anchor: { lon: anchor[0], lat: anchor[1] },
  bbox: { minLon, minLat, maxLon, maxLat },
  boundary: rings
    ? {
        source: 'relation/8346137',
        outerRings: rings.length,
        areaHa: rings.reduce((sum, ring) => sum + ringArea(ring), 0) / 10000,
      }
    : { source: 'bbox' },
  cells: keys,
  bytes: { totals: byteTotals, byCell: bytes },
  rasterSampling: { spacingMeters: spacing, samples: total, mix },
};
console.log(JSON.stringify(result, null, 2));
