// Readers for the baked binary tiles. Shared by the tile worker and by the
// offline reports, so there is exactly one description of each record layout.

export function readBuildings(buffer) {
  const dv = new DataView(buffer);
  const version = dv.getUint16(4, true);
  const count = dv.getUint32(8, true);
  const vertexTotal = dv.getUint32(12, true);
  const indexTotal = dv.getUint32(16, true);
  const originX = dv.getFloat32(20, true);
  const originZ = dv.getFloat32(24, true);
  const quant = dv.getFloat32(28, true);

  let off = 32;
  const vertOffset = new Uint32Array(buffer, off, count);
  off += 4 * count;
  const idxOffset = new Uint32Array(buffer, off, count);
  off += 4 * count;
  const vertCount = new Uint16Array(buffer, off, count);
  off += 2 * count;
  const idxCount = new Uint16Array(buffer, off, count);
  off += 2 * count;
  const baseY = new Int16Array(buffer, off, count);
  off += 2 * count;
  const topY = new Int16Array(buffer, off, count);
  off += 2 * count;
  const palette = new Uint8Array(buffer, off, count);
  off += count;
  const seed = new Uint8Array(buffer, off, count);
  off += count;
  // Version 2 (toy tier) carries a per-record flag byte and a roof colour.
  let flags = null;
  let roofPalette = null;
  if (version >= 2) {
    flags = new Uint8Array(buffer, off, count);
    off += count;
    roofPalette = new Uint8Array(buffer, off, count);
    off += count;
  }
  // Version 3 adds the lore bytes: category, street heading and night flag.
  let cat = null;
  let yaw = null;
  let night = null;
  if (version >= 3) {
    cat = new Uint8Array(buffer, off, count);
    off += count;
    yaw = new Uint8Array(buffer, off, count);
    off += count;
    night = new Uint8Array(buffer, off, count);
    off += count;
  }
  off = Math.ceil(off / 2) * 2;
  const verts = new Int16Array(buffer, off, vertexTotal * 2);
  off += 4 * vertexTotal;
  const indices = new Uint16Array(buffer, off, indexTotal);

  return {
    version,
    flags,
    roofPalette,
    cat,
    yaw,
    night,
    count,
    originX,
    originZ,
    quant,
    vertOffset,
    idxOffset,
    vertCount,
    idxCount,
    baseY,
    topY,
    palette,
    seed,
    verts,
    indices,
  };
}

export function readStreets(buffer) {
  const dv = new DataView(buffer);
  const count = dv.getUint32(8, true);
  const pointTotal = dv.getUint32(12, true);
  const originX = dv.getFloat32(20, true);
  const originZ = dv.getFloat32(24, true);
  const quant = dv.getFloat32(28, true);
  let off = 32;
  const ptOffset = new Uint32Array(buffer, off, count);
  off += 4 * count;
  const ptCount = new Uint16Array(buffer, off, count);
  off += 2 * count;
  const klass = new Uint8Array(buffer, off, count);
  off += count;
  const flags = new Uint8Array(buffer, off, count);
  off += count;
  off = Math.ceil(off / 2) * 2;
  const xz = new Int16Array(buffer, off, pointTotal * 2);
  off += 4 * pointTotal;
  const y = new Int16Array(buffer, off, pointTotal);
  return { count, originX, originZ, quant, ptOffset, ptCount, klass, flags, xz, y };
}

export function readLandcover(buffer) {
  const dv = new DataView(buffer);
  const indexWidth = dv.getUint16(6, true) || 4;
  const vertexTotal = dv.getUint32(8, true);
  const indexTotal = dv.getUint32(12, true);
  const treeTotal = dv.getUint32(16, true);
  const originX = dv.getFloat32(20, true);
  const originZ = dv.getFloat32(24, true);
  const quant = dv.getFloat32(28, true);
  let off = 32;
  const xz = new Int16Array(buffer, off, vertexTotal * 2);
  off += 4 * vertexTotal;
  const y = new Int16Array(buffer, off, vertexTotal);
  off += 2 * vertexTotal;
  const kind = new Uint8Array(buffer, off, vertexTotal);
  off += vertexTotal;
  off = Math.ceil(off / 4) * 4;
  const indices =
    indexWidth === 2
      ? new Uint16Array(buffer, off, indexTotal)
      : new Uint32Array(buffer, off, indexTotal);
  off += indexWidth * indexTotal;
  const treeXZ = new Int16Array(buffer, off, treeTotal * 2);
  off += 4 * treeTotal;
  const treeY = new Int16Array(buffer, off, treeTotal);
  off += 2 * treeTotal;
  const treeVar = new Uint8Array(buffer, off, treeTotal);
  return {
    vertexTotal,
    indexTotal,
    treeTotal,
    originX,
    originZ,
    quant,
    xz,
    y,
    kind,
    indices,
    treeXZ,
    treeY,
    treeVar,
  };
}
