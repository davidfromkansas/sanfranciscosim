// Bakes AWS Open Data Terrarium elevation tiles into a single Int16 heightmap
// covering the city extent. Output:
//   out/terrain.bin   Int16 elevation in decimeters, row-major, north row first
//   out/terrain.json  descriptor (origin, size, resolution)

import { mkdir, writeFile, readFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { PNG } from 'pngjs';
import { BBOX, EXTENT, project, unproject } from './lib/geo.mjs';

const Z = 14;
const SIZE = 2048; // heightmap resolution over the extent (~7.6 m/px)
const OUT = new URL('./out/', import.meta.url);
const CACHE = new URL('./data/terrarium/', import.meta.url);

function lon2tile(lon, z) {
  return ((lon + 180) / 360) * 2 ** z;
}
function lat2tile(lat, z) {
  const rad = (lat * Math.PI) / 180;
  return ((1 - Math.log(Math.tan(rad) + 1 / Math.cos(rad)) / Math.PI) / 2) * 2 ** z;
}
function tile2lon(x, z) {
  return (x / 2 ** z) * 360 - 180;
}
function tile2lat(y, z) {
  const n = Math.PI - (2 * Math.PI * y) / 2 ** z;
  return (180 / Math.PI) * Math.atan(0.5 * (Math.exp(n) - Math.exp(-n)));
}

async function fetchTile(z, x, y) {
  const file = new URL(`${z}_${x}_${y}.png`, CACHE);
  if (existsSync(file)) return await readFile(file);
  const url = `https://s3.amazonaws.com/elevation-tiles-prod/terrarium/${z}/${x}/${y}.png`;
  for (let attempt = 0; attempt < 5; attempt++) {
    const res = await fetch(url);
    if (res.ok) {
      const buf = Buffer.from(await res.arrayBuffer());
      await writeFile(file, buf);
      return buf;
    }
    if (res.status === 404) return null;
    await new Promise((r) => setTimeout(r, 1000 * (attempt + 1)));
  }
  throw new Error(`failed to fetch ${url}`);
}

await mkdir(OUT, { recursive: true });
await mkdir(CACHE, { recursive: true });

// Pad the tile range a little so bilinear sampling at the edges is defined.
const x0 = Math.floor(lon2tile(BBOX.minLon, Z)) - 1;
const x1 = Math.ceil(lon2tile(BBOX.maxLon, Z)) + 1;
const y0 = Math.floor(lat2tile(BBOX.maxLat, Z)) - 1;
const y1 = Math.ceil(lat2tile(BBOX.minLat, Z)) + 1;
const tilesX = x1 - x0;
const tilesY = y1 - y0;
console.log(`terrarium z=${Z} tiles: x ${x0}..${x1} y ${y0}..${y1} (${tilesX * tilesY} tiles)`);

const TS = 256;
const mosaicW = tilesX * TS;
const mosaicH = tilesY * TS;
const mosaic = new Float32Array(mosaicW * mosaicH);
mosaic.fill(NaN);

let fetched = 0;
for (let ty = y0; ty < y1; ty++) {
  const row = [];
  for (let tx = x0; tx < x1; tx++) row.push(fetchTile(Z, tx, ty));
  const bufs = await Promise.all(row);
  bufs.forEach((buf, i) => {
    if (!buf) return;
    const png = PNG.sync.read(buf);
    const ox = i * TS;
    const oy = (ty - y0) * TS;
    for (let py = 0; py < TS; py++) {
      for (let px = 0; px < TS; px++) {
        const s = (py * png.width + px) * 4;
        const elev = png.data[s] * 256 + png.data[s + 1] + png.data[s + 2] / 256 - 32768;
        mosaic[(oy + py) * mosaicW + ox + px] = elev;
      }
    }
    fetched++;
  });
  console.log(`  row ${ty - y0 + 1}/${tilesY} (${fetched} tiles decoded)`);
}

function sampleMosaic(lon, lat) {
  const fx = (lon2tile(lon, Z) - x0) * TS;
  const fy = (lat2tile(lat, Z) - y0) * TS;
  const ix = Math.min(mosaicW - 2, Math.max(0, Math.floor(fx)));
  const iy = Math.min(mosaicH - 2, Math.max(0, Math.floor(fy)));
  const tx = fx - ix;
  const ty = fy - iy;
  const a = mosaic[iy * mosaicW + ix];
  const b = mosaic[iy * mosaicW + ix + 1];
  const c = mosaic[(iy + 1) * mosaicW + ix];
  const d = mosaic[(iy + 1) * mosaicW + ix + 1];
  const top = a + (b - a) * tx;
  const bot = c + (d - c) * tx;
  const v = top + (bot - top) * ty;
  return Number.isFinite(v) ? v : 0;
}

// Resample the mosaic onto the local projected grid.
const cellX = (EXTENT.maxX - EXTENT.minX) / (SIZE - 1);
const cellZ = (EXTENT.maxZ - EXTENT.minZ) / (SIZE - 1);
const height = new Int16Array(SIZE * SIZE);
let maxElev = -Infinity;
let minElev = Infinity;
for (let j = 0; j < SIZE; j++) {
  const z = EXTENT.minZ + j * cellZ;
  for (let i = 0; i < SIZE; i++) {
    const x = EXTENT.minX + i * cellX;
    const [lon, lat] = unproject(x, z);
    let e = sampleMosaic(lon, lat);
    if (e < 0) e = 0; // clamp bathymetry: everything at/below sea level reads as 0
    if (e > maxElev) maxElev = e;
    if (e < minElev) minElev = e;
    height[j * SIZE + i] = Math.round(e * 10);
  }
}

// Light 3x3 smoothing to remove Terrarium quantisation stair-stepping without
// flattening the ridgelines.
const smoothed = new Int16Array(height);
for (let j = 1; j < SIZE - 1; j++) {
  for (let i = 1; i < SIZE - 1; i++) {
    let sum = 0;
    for (let dj = -1; dj <= 1; dj++) {
      for (let di = -1; di <= 1; di++) sum += height[(j + dj) * SIZE + i + di];
    }
    smoothed[j * SIZE + i] = Math.round(sum / 9);
  }
}

await writeFile(new URL('terrain.bin', OUT), Buffer.from(smoothed.buffer));
const descriptor = {
  size: SIZE,
  minX: EXTENT.minX,
  minZ: EXTENT.minZ,
  maxX: EXTENT.maxX,
  maxZ: EXTENT.maxZ,
  cellX,
  cellZ,
  scale: 0.1, // decimeters -> meters
  minElev,
  maxElev,
  zoom: Z,
};
await writeFile(new URL('terrain.json', OUT), JSON.stringify(descriptor, null, 2));

const [fbX, fbZ] = project(-122.3937, 37.7955); // Ferry Building
const ferry = smoothed[
  Math.round((fbZ - EXTENT.minZ) / cellZ) * SIZE + Math.round((fbX - EXTENT.minX) / cellX)
] * 0.1;
const [tpX, tpZ] = project(-122.4477, 37.7544); // Twin Peaks
const twin = smoothed[
  Math.round((tpZ - EXTENT.minZ) / cellZ) * SIZE + Math.round((tpX - EXTENT.minX) / cellX)
] * 0.1;

console.log(
  `terrain baked ${SIZE}x${SIZE}, elevation ${minElev.toFixed(1)}..${maxElev.toFixed(1)} m; ` +
    `Ferry Building ${ferry.toFixed(1)} m, Twin Peaks ${twin.toFixed(1)} m`
);
