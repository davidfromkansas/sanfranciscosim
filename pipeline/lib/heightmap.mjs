// Loads the baked heightmap so every other pipeline step can drape geometry
// onto the real terrain.

import { readFile } from 'node:fs/promises';

const OUT = new URL('../out/', import.meta.url);

export async function loadHeightmap() {
  const desc = JSON.parse(await readFile(new URL('terrain.json', OUT), 'utf8'));
  const buf = await readFile(new URL('terrain.bin', OUT));
  const data = new Int16Array(buf.buffer, buf.byteOffset, buf.byteLength / 2);
  const { size, minX, minZ, cellX, cellZ, scale } = desc;

  function sampleElevation(x, z) {
    const fx = (x - minX) / cellX;
    const fz = (z - minZ) / cellZ;
    const ix = Math.min(size - 2, Math.max(0, Math.floor(fx)));
    const iz = Math.min(size - 2, Math.max(0, Math.floor(fz)));
    const tx = Math.min(1, Math.max(0, fx - ix));
    const tz = Math.min(1, Math.max(0, fz - iz));
    const a = data[iz * size + ix];
    const b = data[iz * size + ix + 1];
    const c = data[(iz + 1) * size + ix];
    const d = data[(iz + 1) * size + ix + 1];
    const top = a + (b - a) * tx;
    const bot = c + (d - c) * tx;
    return (top + (bot - top) * tz) * scale;
  }

  return { desc, data, sampleElevation };
}
