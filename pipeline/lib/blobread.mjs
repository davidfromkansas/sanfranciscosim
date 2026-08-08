// Readers for the baked binary blobs, mirroring the writers in binio.mjs.
// Used by audit.mjs to inspect exactly what the runtime will decode.

import { readFile } from 'node:fs/promises';
import {
  MAGIC_BUILDINGS,
  MAGIC_LANDCOVER,
  MAGIC_STREETS,
} from './binio.mjs';

function alignTo(n, a) {
  return Math.ceil(n / a) * a;
}

export async function readBuildingsBlob(path) {
  const buf = await readFile(path);
  const dv = new DataView(buf.buffer, buf.byteOffset, buf.byteLength);
  if (dv.getUint32(0, true) !== MAGIC_BUILDINGS) throw new Error(`bad magic in ${path}`);
  const count = dv.getUint32(8, true);
  const vertexTotal = dv.getUint32(12, true);
  const indexTotal = dv.getUint32(16, true);
  const originX = dv.getFloat32(20, true);
  const originZ = dv.getFloat32(24, true);
  const quant = dv.getFloat32(28, true);

  let off = 32;
  const vertOffset = new Uint32Array(buf.buffer, buf.byteOffset + off, count);
  off += 4 * count;
  const idxOffset = new Uint32Array(buf.buffer, buf.byteOffset + off, count);
  off += 4 * count;
  const vertCount = new Uint16Array(buf.buffer, buf.byteOffset + off, count);
  off += 2 * count;
  const idxCount = new Uint16Array(buf.buffer, buf.byteOffset + off, count);
  off += 2 * count;
  const baseY = new Int16Array(buf.buffer, buf.byteOffset + off, count);
  off += 2 * count;
  const topY = new Int16Array(buf.buffer, buf.byteOffset + off, count);
  off += 2 * count;
  const palette = new Uint8Array(buf.buffer, buf.byteOffset + off, count);
  off += count;
  const seed = new Uint8Array(buf.buffer, buf.byteOffset + off, count);
  off += count;
  off = alignTo(off, 2);
  const verts = new Int16Array(buf.buffer, buf.byteOffset + off, vertexTotal * 2);
  off += 4 * vertexTotal;
  const indices = new Uint16Array(buf.buffer, buf.byteOffset + off, indexTotal);

  const buildings = [];
  for (let i = 0; i < count; i++) {
    const n = vertCount[i];
    const ring = new Float64Array(n * 2);
    for (let k = 0; k < n; k++) {
      ring[k * 2] = originX + verts[(vertOffset[i] + k) * 2] * quant;
      ring[k * 2 + 1] = originZ + verts[(vertOffset[i] + k) * 2 + 1] * quant;
    }
    buildings.push({
      ring,
      baseY: baseY[i] / 10,
      topY: topY[i] / 10,
      palette: palette[i],
      seed: seed[i],
      triangles: idxCount[i] / 3,
    });
  }
  return { originX, originZ, buildings, bytes: buf.length, indices };
}

export async function readStreetsBlob(path) {
  const buf = await readFile(path);
  const dv = new DataView(buf.buffer, buf.byteOffset, buf.byteLength);
  if (dv.getUint32(0, true) !== MAGIC_STREETS) throw new Error(`bad magic in ${path}`);
  const count = dv.getUint32(8, true);
  const pointTotal = dv.getUint32(12, true);
  const originX = dv.getFloat32(20, true);
  const originZ = dv.getFloat32(24, true);
  const quant = dv.getFloat32(28, true);

  let off = 32;
  const ptOffset = new Uint32Array(buf.buffer, buf.byteOffset + off, count);
  off += 4 * count;
  const ptCount = new Uint16Array(buf.buffer, buf.byteOffset + off, count);
  off += 2 * count;
  const klass = new Uint8Array(buf.buffer, buf.byteOffset + off, count);
  off += count;
  const flags = new Uint8Array(buf.buffer, buf.byteOffset + off, count);
  off += count;
  off = alignTo(off, 2);
  const xz = new Int16Array(buf.buffer, buf.byteOffset + off, pointTotal * 2);
  off += 4 * pointTotal;
  const y = new Int16Array(buf.buffer, buf.byteOffset + off, pointTotal);

  const lines = [];
  for (let i = 0; i < count; i++) {
    const n = ptCount[i];
    const pts = new Float64Array(n * 3);
    for (let k = 0; k < n; k++) {
      pts[k * 3] = originX + xz[(ptOffset[i] + k) * 2] * quant;
      pts[k * 3 + 1] = y[ptOffset[i] + k] / 10;
      pts[k * 3 + 2] = originZ + xz[(ptOffset[i] + k) * 2 + 1] * quant;
    }
    lines.push({ pts, klass: klass[i], flags: flags[i] });
  }
  return { originX, originZ, lines, bytes: buf.length };
}

// `full` also returns the draped triangles themselves, which the toy bake
// rewrites with a denser tree scatter.
export async function readLandcoverBlob(path, { full = false } = {}) {
  const buf = await readFile(path);
  const dv = new DataView(buf.buffer, buf.byteOffset, buf.byteLength);
  if (dv.getUint32(0, true) !== MAGIC_LANDCOVER) throw new Error(`bad magic in ${path}`);
  const indexWidth = dv.getUint16(6, true);
  const vertexTotal = dv.getUint32(8, true);
  const indexTotal = dv.getUint32(12, true);
  const treeTotal = dv.getUint32(16, true);
  const originX = dv.getFloat32(20, true);
  const originZ = dv.getFloat32(24, true);
  const quant = dv.getFloat32(28, true);

  let off = 32;
  const xz = new Int16Array(buf.buffer, buf.byteOffset + off, vertexTotal * 2);
  off += 4 * vertexTotal;
  const y = new Int16Array(buf.buffer, buf.byteOffset + off, vertexTotal);
  off += 2 * vertexTotal;
  const kind = new Uint8Array(buf.buffer, buf.byteOffset + off, vertexTotal);
  off += vertexTotal;
  off = alignTo(off, 4);
  const indices =
    indexWidth === 2
      ? new Uint16Array(buf.buffer, buf.byteOffset + off, indexTotal)
      : new Uint32Array(buf.buffer, buf.byteOffset + off, indexTotal);
  off += indexWidth * indexTotal;
  const treeXZ = new Int16Array(buf.buffer, buf.byteOffset + off, treeTotal * 2);
  off += 4 * treeTotal;
  const treeY = new Int16Array(buf.buffer, buf.byteOffset + off, treeTotal);
  off += 2 * treeTotal;
  const treeVariant = new Uint8Array(buf.buffer, buf.byteOffset + off, treeTotal);

  const trees = new Float64Array(treeTotal * 3);
  for (let i = 0; i < treeTotal; i++) {
    trees[i * 3] = originX + treeXZ[i * 2] * quant;
    trees[i * 3 + 1] = treeY[i] / 10;
    trees[i * 3 + 2] = originZ + treeXZ[i * 2 + 1] * quant;
  }
  const out = {
    trees,
    treeVariant,
    treeTotal,
    triangles: indexTotal / 3,
    bytes: buf.length,
    originX,
    originZ,
  };
  if (full) {
    const verts = new Float64Array(vertexTotal * 3);
    for (let i = 0; i < vertexTotal; i++) {
      verts[i * 3] = originX + xz[i * 2] * quant;
      verts[i * 3 + 1] = y[i] / 10;
      verts[i * 3 + 2] = originZ + xz[i * 2 + 1] * quant;
    }
    out.verts = verts;
    out.kinds = kind;
    out.indices = indices;
  }
  return out;
}
