// Shared projection, tiling and city extent definitions.
// Every dataset in the pipeline goes through project() exactly once; the runtime
// only ever sees meters in this local tangent-plane frame.

export const LON0 = -122.4375;
export const LAT0 = 37.77;

export const BBOX = { minLon: -122.525, minLat: 37.7, maxLon: -122.35, maxLat: 37.84 };

const M_PER_DEG_LON = 111320 * Math.cos((LAT0 * Math.PI) / 180);
const M_PER_DEG_LAT = 110540;

export function project(lon, lat) {
  return [(lon - LON0) * M_PER_DEG_LON, -(lat - LAT0) * M_PER_DEG_LAT];
}

export function unproject(x, z) {
  return [x / M_PER_DEG_LON + LON0, -z / M_PER_DEG_LAT + LAT0];
}

const [minX, maxZ] = project(BBOX.minLon, BBOX.minLat);
const [maxX, minZ] = project(BBOX.maxLon, BBOX.maxLat);

export const EXTENT = { minX, maxX, minZ, maxZ };

export const CELL_SIZE = 500;
export const GRID = {
  originX: Math.floor(minX / CELL_SIZE) * CELL_SIZE,
  originZ: Math.floor(minZ / CELL_SIZE) * CELL_SIZE,
  cols: Math.ceil((maxX - Math.floor(minX / CELL_SIZE) * CELL_SIZE) / CELL_SIZE),
  rows: Math.ceil((maxZ - Math.floor(minZ / CELL_SIZE) * CELL_SIZE) / CELL_SIZE),
};

export function cellIndex(x, z) {
  const cx = Math.floor((x - GRID.originX) / CELL_SIZE);
  const cz = Math.floor((z - GRID.originZ) / CELL_SIZE);
  if (cx < 0 || cz < 0 || cx >= GRID.cols || cz >= GRID.rows) return null;
  return { cx, cz, key: `${cx}_${cz}` };
}

export function cellOrigin(cx, cz) {
  return [GRID.originX + cx * CELL_SIZE, GRID.originZ + cz * CELL_SIZE];
}

export function insideBBox(lon, lat) {
  return lon >= BBOX.minLon && lon <= BBOX.maxLon && lat >= BBOX.minLat && lat <= BBOX.maxLat;
}

// Deterministic hash -> [0,1), used for district seeds and tree scatter.
export function hash01(n) {
  let h = Math.imul(n ^ 0x9e3779b9, 0x85ebca6b);
  h = Math.imul(h ^ (h >>> 13), 0xc2b2ae35);
  h ^= h >>> 16;
  return (h >>> 0) / 4294967296;
}
