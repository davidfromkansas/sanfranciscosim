// Loads the baked manifest, heightmap and landuse raster, and exposes the
// projection helpers plus sampleElevation() that everything else builds on.

const TILES = `${import.meta.env.BASE_URL}tiles/`;

async function json(path) {
  const res = await fetch(TILES + path);
  if (!res.ok) throw new Error(`failed to load ${path}: ${res.status}`);
  return res.json();
}

async function bin(path) {
  const res = await fetch(TILES + path);
  if (!res.ok) throw new Error(`failed to load ${path}: ${res.status}`);
  return res.arrayBuffer();
}

export const tileUrl = (path) => TILES + path;

export async function loadCore(onProgress = () => {}) {
  const manifest = await json('manifest.json');
  onProgress(0.1);
  const [terrainBuf, landuseBuf] = await Promise.all([bin('terrain.bin'), bin('landuse.bin')]);
  onProgress(0.45);
  const [buildings, streets, landcover] = await Promise.all([
    json('buildings.json'),
    json('streets.json'),
    json('landcover.json'),
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
    indexes: { buildings, streets, landcover },
    height,
    landuse,
    sampleElevation,
    sampleSlope,
    sampleLanduse,
    project,
  };
}
