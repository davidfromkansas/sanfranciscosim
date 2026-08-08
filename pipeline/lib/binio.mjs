// Binary blob writers. The runtime never parses text: it fetches an
// ArrayBuffer, slices typed-array views straight out of it and extrudes/ribbons
// the geometry in a worker.

export const MAGIC_BUILDINGS = 0x42465301; // "SFB1"
export const MAGIC_STREETS = 0x53465301; // "SFS1"
export const MAGIC_LANDCOVER = 0x4c465301; // "SFL1"
export const QUANT = 0.02; // meters per quantised unit for horizontal coords

function alignTo(n, a) {
  return Math.ceil(n / a) * a;
}

// Buildings: per-building footprint ring + roof triangulation + base/top
// elevations. Walls and roof geometry are generated in the runtime worker,
// which keeps the payload ~15x smaller than baking triangles.
export function writeBuildingsBlob(cell) {
  const count = cell.buildings.length;
  let vertexTotal = 0;
  let indexTotal = 0;
  for (const b of cell.buildings) {
    vertexTotal += b.ring.length / 2;
    indexTotal += b.indices.length;
  }

  const HEADER = 32;
  let off = HEADER;
  const vertOffsetAt = off;
  off += 4 * count;
  const idxOffsetAt = off;
  off += 4 * count;
  const vertCountAt = off;
  off += 2 * count;
  const idxCountAt = off;
  off += 2 * count;
  const baseYAt = off;
  off += 2 * count;
  const topYAt = off;
  off += 2 * count;
  const paletteAt = off;
  off += count;
  const seedAt = off;
  off += count;
  off = alignTo(off, 2);
  const vertsAt = off;
  off += 4 * vertexTotal;
  const indicesAt = off;
  off += 2 * indexTotal;

  const buf = Buffer.alloc(off);
  const dv = new DataView(buf.buffer, buf.byteOffset, buf.byteLength);
  dv.setUint32(0, MAGIC_BUILDINGS, true);
  dv.setUint16(4, 1, true);
  dv.setUint16(6, 0, true);
  dv.setUint32(8, count, true);
  dv.setUint32(12, vertexTotal, true);
  dv.setUint32(16, indexTotal, true);
  dv.setFloat32(20, cell.originX, true);
  dv.setFloat32(24, cell.originZ, true);
  dv.setFloat32(28, QUANT, true);

  const vertOffset = new Uint32Array(buf.buffer, buf.byteOffset + vertOffsetAt, count);
  const idxOffset = new Uint32Array(buf.buffer, buf.byteOffset + idxOffsetAt, count);
  const vertCount = new Uint16Array(buf.buffer, buf.byteOffset + vertCountAt, count);
  const idxCount = new Uint16Array(buf.buffer, buf.byteOffset + idxCountAt, count);
  const baseY = new Int16Array(buf.buffer, buf.byteOffset + baseYAt, count);
  const topY = new Int16Array(buf.buffer, buf.byteOffset + topYAt, count);
  const palette = new Uint8Array(buf.buffer, buf.byteOffset + paletteAt, count);
  const seed = new Uint8Array(buf.buffer, buf.byteOffset + seedAt, count);
  const verts = new Int16Array(buf.buffer, buf.byteOffset + vertsAt, vertexTotal * 2);
  const indices = new Uint16Array(buf.buffer, buf.byteOffset + indicesAt, indexTotal);

  let v = 0;
  let ix = 0;
  cell.buildings.forEach((b, i) => {
    const n = b.ring.length / 2;
    vertOffset[i] = v;
    vertCount[i] = n;
    idxOffset[i] = ix;
    idxCount[i] = b.indices.length;
    baseY[i] = Math.round(b.baseY * 10);
    topY[i] = Math.round(b.topY * 10);
    palette[i] = b.palette;
    seed[i] = b.seed;
    for (let k = 0; k < n; k++) {
      verts[(v + k) * 2] = Math.round((b.ring[k * 2] - cell.originX) / QUANT);
      verts[(v + k) * 2 + 1] = Math.round((b.ring[k * 2 + 1] - cell.originZ) / QUANT);
    }
    for (let k = 0; k < b.indices.length; k++) indices[ix + k] = b.indices[k];
    v += n;
    ix += b.indices.length;
  });

  return buf;
}

// Streets: polylines with per-line class and pre-sampled terrain elevation.
// The worker turns them into draped ribbons and the traffic system reuses the
// same polylines as car paths.
export function writeStreetsBlob(cell) {
  const count = cell.lines.length;
  let pointTotal = 0;
  for (const l of cell.lines) pointTotal += l.pts.length / 2;

  const HEADER = 32;
  let off = HEADER;
  const ptOffsetAt = off;
  off += 4 * count;
  const ptCountAt = off;
  off += 2 * count;
  const classAt = off;
  off += count;
  const flagsAt = off;
  off += count;
  off = alignTo(off, 2);
  const xzAt = off;
  off += 4 * pointTotal;
  const yAt = off;
  off += 2 * pointTotal;

  const buf = Buffer.alloc(off);
  const dv = new DataView(buf.buffer, buf.byteOffset, buf.byteLength);
  dv.setUint32(0, MAGIC_STREETS, true);
  dv.setUint16(4, 1, true);
  dv.setUint32(8, count, true);
  dv.setUint32(12, pointTotal, true);
  dv.setFloat32(20, cell.originX, true);
  dv.setFloat32(24, cell.originZ, true);
  dv.setFloat32(28, QUANT, true);

  const ptOffset = new Uint32Array(buf.buffer, buf.byteOffset + ptOffsetAt, count);
  const ptCount = new Uint16Array(buf.buffer, buf.byteOffset + ptCountAt, count);
  const klass = new Uint8Array(buf.buffer, buf.byteOffset + classAt, count);
  const flags = new Uint8Array(buf.buffer, buf.byteOffset + flagsAt, count);
  const xz = new Int16Array(buf.buffer, buf.byteOffset + xzAt, pointTotal * 2);
  const y = new Int16Array(buf.buffer, buf.byteOffset + yAt, pointTotal);

  let p = 0;
  cell.lines.forEach((l, i) => {
    const n = l.pts.length / 2;
    ptOffset[i] = p;
    ptCount[i] = n;
    klass[i] = l.klass;
    flags[i] = l.flags || 0;
    for (let k = 0; k < n; k++) {
      xz[(p + k) * 2] = Math.round((l.pts[k * 2] - cell.originX) / QUANT);
      xz[(p + k) * 2 + 1] = Math.round((l.pts[k * 2 + 1] - cell.originZ) / QUANT);
      y[p + k] = Math.round(l.y[k] * 10);
    }
    p += n;
  });

  return buf;
}

// Landcover: pre-triangulated draped polygons plus deterministic tree scatter.
export function writeLandcoverBlob(cell) {
  const vertexTotal = cell.verts.length / 3;
  const indexTotal = cell.indices.length;
  const treeTotal = cell.trees.length / 4;
  const indexWidth = vertexTotal < 65536 ? 2 : 4;

  const HEADER = 32;
  let off = HEADER;
  const xzAt = off;
  off += 4 * vertexTotal;
  const yAt = off;
  off += 2 * vertexTotal;
  const kindAt = off;
  off += vertexTotal;
  off = alignTo(off, 4);
  const indicesAt = off;
  off += indexWidth * indexTotal;
  const treeXZAt = off;
  off += 4 * treeTotal;
  const treeYAt = off;
  off += 2 * treeTotal;
  const treeVarAt = off;
  off += treeTotal;
  off = alignTo(off, 4);

  const buf = Buffer.alloc(off);
  const dv = new DataView(buf.buffer, buf.byteOffset, buf.byteLength);
  dv.setUint32(0, MAGIC_LANDCOVER, true);
  dv.setUint16(4, 1, true);
  dv.setUint16(6, indexWidth, true);
  dv.setUint32(8, vertexTotal, true);
  dv.setUint32(12, indexTotal, true);
  dv.setUint32(16, treeTotal, true);
  dv.setFloat32(20, cell.originX, true);
  dv.setFloat32(24, cell.originZ, true);
  dv.setFloat32(28, QUANT, true);

  const xz = new Int16Array(buf.buffer, buf.byteOffset + xzAt, vertexTotal * 2);
  const y = new Int16Array(buf.buffer, buf.byteOffset + yAt, vertexTotal);
  const kind = new Uint8Array(buf.buffer, buf.byteOffset + kindAt, vertexTotal);
  const indices =
    indexWidth === 2
      ? new Uint16Array(buf.buffer, buf.byteOffset + indicesAt, indexTotal)
      : new Uint32Array(buf.buffer, buf.byteOffset + indicesAt, indexTotal);
  const treeXZ = new Int16Array(buf.buffer, buf.byteOffset + treeXZAt, treeTotal * 2);
  const treeY = new Int16Array(buf.buffer, buf.byteOffset + treeYAt, treeTotal);
  const treeVar = new Uint8Array(buf.buffer, buf.byteOffset + treeVarAt, treeTotal);

  for (let i = 0; i < vertexTotal; i++) {
    xz[i * 2] = Math.round((cell.verts[i * 3] - cell.originX) / QUANT);
    xz[i * 2 + 1] = Math.round((cell.verts[i * 3 + 2] - cell.originZ) / QUANT);
    y[i] = Math.round(cell.verts[i * 3 + 1] * 10);
    kind[i] = cell.kinds[i];
  }
  indices.set(cell.indices);
  for (let i = 0; i < treeTotal; i++) {
    treeXZ[i * 2] = Math.round((cell.trees[i * 4] - cell.originX) / QUANT);
    treeXZ[i * 2 + 1] = Math.round((cell.trees[i * 4 + 2] - cell.originZ) / QUANT);
    treeY[i] = Math.round(cell.trees[i * 4 + 1] * 10);
    treeVar[i] = cell.trees[i * 4 + 3];
  }

  return buf;
}
