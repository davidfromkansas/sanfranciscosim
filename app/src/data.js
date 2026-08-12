// Loads the baked manifest, heightmap and landuse raster, and exposes the
// projection helpers plus sampleElevation() that everything else builds on.

const TILES = `${import.meta.env.BASE_URL}tiles/`;
// Injected from the bake timestamp at build time; busts the long-lived tile
// cache whenever the data is re-baked under the same file names.
const VERSION = `?v=${encodeURIComponent(__TILES_VERSION__)}`;

export const tileUrl = (path) => TILES + path + VERSION;

async function json(path) {
  const res = await fetch(tileUrl(path));
  if (!res.ok) throw new Error(`failed to load ${path}: ${res.status}`);
  return res.json();
}

// Binary tiles ship as .bin.gz alongside the raw .bin (written by
// scripts/compress-tiles.mjs at build time) and inflate off the wire with the
// native DecompressionStream — no dependency, no worker change. The raw file
// is the guaranteed fallback: a browser without the API, a dev server without
// the archives, or one missing file all degrade to exactly the old behaviour
// (rule 3), with a single console warning when compressed delivery is off
// entirely.
let gzTiles = typeof DecompressionStream === 'function' ? 'probe' : 'off';

// Some static servers send .gz files with `content-encoding: gzip` (the
// browser inflates them on the wire — vite preview does this), others send the
// raw archive bytes (Vercel). Sniffing the gzip magic covers both: a baked
// tile can never start 0x1f 0x8b (every blob opens with its own format magic).
async function inflateIfGzip(buffer) {
  const head = new Uint8Array(buffer, 0, 2);
  if (head[0] !== 0x1f || head[1] !== 0x8b) return buffer;
  const stream = new Blob([buffer]).stream().pipeThrough(new DecompressionStream('gzip'));
  return new Response(stream).arrayBuffer();
}

export async function fetchTileBin(path) {
  if (gzTiles !== 'off') {
    try {
      const res = await fetch(tileUrl(path + '.gz'));
      // A server with an SPA fallback answers a missing archive with 200 +
      // index.html — that is a miss, not a tile.
      const isTile = res.ok && !(res.headers.get('content-type') || '').includes('text/html');
      if (isTile) {
        const buffer = await inflateIfGzip(await res.arrayBuffer());
        gzTiles = 'on';
        return buffer;
      }
      if (gzTiles === 'probe') {
        gzTiles = 'off';
        console.warn(`compressed tiles unavailable (${path}.gz: ${res.status}) — using raw .bin`);
      }
    } catch (err) {
      if (gzTiles === 'probe') {
        gzTiles = 'off';
        console.warn('compressed tiles unavailable — using raw .bin', err);
      }
    }
  }
  const res = await fetch(tileUrl(path));
  if (!res.ok) throw new Error(`failed to load ${path}: ${res.status}`);
  return res.arrayBuffer();
}

const bin = fetchTileBin;

export async function loadCore(onProgress = () => {}) {
  const manifest = await json('manifest.json');
  onProgress(0.1);
  const [terrainBuf, landuseBuf] = await Promise.all([bin('terrain.bin'), bin('landuse.bin')]);
  onProgress(0.45);
  const [buildings, streets, landcover, context] = await Promise.all([
    json('buildings.json'),
    json('streets.json'),
    json('landcover.json'),
    // Only ~600 of the 1024 grid cells have a context sidecar; the rest are
    // water or empty. Everyone who streams `ctx/<cell>.json` consults this set
    // first, so an empty cell costs no request and logs no 404.
    json('context.json'),
  ]);
  onProgress(0.6);

  const t = manifest.terrain;
  const height = new Int16Array(terrainBuf);
  const landuse = new Uint8Array(landuseBuf);
  const lu = manifest.landuse;

  function sampleElevation(x, z) {
    const fx = (x - t.minX) / t.cellX;
    const fz = (z - t.minZ) / t.cellZ;
    const ix = Math.min(t.size - 2, Math.max(0, Math.floor(fx)));
    const iz = Math.min(t.size - 2, Math.max(0, Math.floor(fz)));
    const tx = Math.min(1, Math.max(0, fx - ix));
    const tz = Math.min(1, Math.max(0, fz - iz));
    const row = iz * t.size + ix;
    const a = height[row];
    const b = height[row + 1];
    const c = height[row + t.size];
    const d = height[row + t.size + 1];
    const top = a + (b - a) * tx;
    const bot = c + (d - c) * tx;
    return (top + (bot - top) * tz) * t.scale;
  }

  function sampleSlope(x, z) {
    const d = 12;
    const ex = sampleElevation(x + d, z) - sampleElevation(x - d, z);
    const ez = sampleElevation(x, z + d) - sampleElevation(x, z - d);
    return Math.hypot(ex, ez) / (2 * d);
  }

  // 255 = no landcover feature (plain urban ground).
  function sampleLanduse(x, z) {
    const i = Math.round((x - lu.minX) / lu.cellX);
    const j = Math.round((z - lu.minZ) / lu.cellZ);
    if (i < 0 || j < 0 || i >= lu.size || j >= lu.size) return 255;
    return landuse[j * lu.size + i];
  }

  const project = (lon, lat) => [
    (lon - manifest.projection.lon0) * manifest.projection.mPerDegLon,
    -(lat - manifest.projection.lat0) * manifest.projection.mPerDegLat,
  ];

  return {
    manifest,
    indexes: { buildings, streets, landcover, context },
    contextCells: new Set(context.cells.map((cell) => cell.key)),
    height,
    landuse,
    sampleElevation,
    sampleSlope,
    sampleLanduse,
    project,
  };
}
