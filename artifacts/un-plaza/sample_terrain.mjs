// Sample the baked terrain under United Nations Plaza, in the plaza's (e, n) frame.
//
//     node sample_terrain.mjs          # writes data/terrain_en.json
//
// Why this exists. `placeGeneric()` in app/src/assets.js seats a landmark with
// ONE terrain sample, taken at the anchor:
//
//     const y = Math.max(0, data.sampleElevation(x, z));
//
// Right for a building — a compact footprint on a slope buries its base uphill,
// which is what a real building does. Wrong for an asset that IS the ground.
//
// Measured on the committed bake, over 2,811 samples inside the real plaza ring:
// the terrain runs 13.06..16.64 m while the anchor sits at 15.119 m, so a FLAT
// plate seated at the anchor is buried 1.52 m at the Hyde end and floats 2.06 m
// over the south side of the promenade. That is invisible in every Blender
// render and obvious in the running app. Same failure the 64 South Park and
// 424 Brannan ground assets hit; this file follows 424 Brannan's remedy.
//
// Output carries BOTH a regular (e, n) grid of dy and a least-squares PLANE fit
// restricted to samples inside the real plaza ring. The build uses the PLANE.
//
// Why the plane and not the grid, which hugs the heightmap exactly: a
// piecewise-bilinear grid is not affine, so draping a thin slab's vertices on it
// folds the slab — a 0.06 m paving inlay spanning 50 m gets its corners offset
// by more than its own thickness, its side quads go non-planar, and the signed
// volume inverts. That was measured, not guessed: the grid build produced
// `skate_pad` with a negative signed volume and a 0.37 m spread in paving
// clearance. A plane shear maps planes to planes, so every prism stays valid.
//
// The cost is the plane's residual, and it is worth stating exactly where it
// goes. Inside the ring the fit is good to 0.368 m RMS, with 616 of 706 sampled
// points inside 0.5 m — but 30 points reach 1.9 m in a single ~20 m dip centred
// near (e -24, n -33). That dip is a Terrarium DEM artefact over the Civic
// Center station excavation, not topography: the real plaza has no crater in it.
// Draping to the plane therefore tracks the ground everywhere the ground is
// real, and ignores a hole in the elevation data.
//
// dy is relative to the anchor's elevation, so dy(0,0) = 0 by construction: the
// asset's z = 0 plane is the anchor's ground, which is where the loader puts it.
//
// Source: app/public/tiles/terrain.bin + the `terrain` block of
// app/public/tiles/manifest.json — the SAME baked heightmap the runtime reads,
// so the plate hugs exactly the bilinear surface sampleElevation() evaluates.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const REPO = path.resolve(HERE, '../..');

const M = JSON.parse(fs.readFileSync(path.join(REPO, 'app/public/tiles/manifest.json'), 'utf8'));
const T = M.terrain;
const buf = fs.readFileSync(path.join(REPO, 'app/public/tiles/terrain.bin'));
const grid = new Int16Array(buf.buffer, buf.byteOffset, buf.byteLength / 2);

function sampleElevation(x, z) {
  const fx = (x - T.minX) / T.cellX;
  const fz = (z - T.minZ) / T.cellZ;
  const ix = Math.min(T.size - 2, Math.max(0, Math.floor(fx)));
  const iz = Math.min(T.size - 2, Math.max(0, Math.floor(fz)));
  const tx = Math.min(1, Math.max(0, fx - ix));
  const tz = Math.min(1, Math.max(0, fz - iz));
  const row = iz * T.size + ix;
  const a = grid[row];
  const b = grid[row + 1];
  const c = grid[row + T.size];
  const d = grid[row + T.size + 1];
  const top = a + (b - a) * tx;
  const bot = c + (d - c) * tx;
  return (top + (bot - top) * tz) * T.scale;
}

const frame = JSON.parse(fs.readFileSync(path.join(HERE, 'data', 'frame.json'), 'utf8'));
const E = (frame.E_BRG * Math.PI) / 180;
const N = (frame.N_BRG * Math.PI) / 180;
const [CX, CY] = frame.world_centre;
// world_centre is in (x east, y north); the runtime's z axis is -y.
const toXZ = (e, n) => [
  CX + e * Math.sin(E) + n * Math.sin(N),
  -(CY + e * Math.cos(E) + n * Math.cos(N)),
];

// The grid covers the model's full (e, n) extent with a margin, at 4 m — half
// the terrain heightmap's own 7.5 m cell, so bilinear interpolation of this
// grid reproduces the heightmap rather than smoothing it.
const STEP = 4;
const E0 = -116, E1 = 120, N0 = -86, N1 = 82;
const cols = Math.round((E1 - E0) / STEP) + 1;
const rows = Math.round((N1 - N0) / STEP) + 1;
const anchor = sampleElevation(...toXZ(0, 0));

const dy = [];
for (let j = 0; j < rows; j++) {
  const row = [];
  for (let i = 0; i < cols; i++) {
    row.push(+(sampleElevation(...toXZ(E0 + i * STEP, N0 + j * STEP)) - anchor).toFixed(4));
  }
  dy.push(row);
}

// Plane fit, restricted to samples INSIDE the real plaza ring — the build uses
// this. A fit over the full grid rectangle is meaningless here because the
// rectangle covers the Federal Building's block and the far side of Market.
const frameRing = frame.ring_en;
function inRing(p) {
  let c = false;
  for (let i = 0; i < frameRing.length - 1; i++) {
    const [x0, y0] = frameRing[i];
    const [x1, y1] = frameRing[i + 1];
    if (y0 > p[1] !== y1 > p[1] && p[0] < ((x1 - x0) * (p[1] - y0)) / (y1 - y0) + x0) c = !c;
  }
  return c;
}
let sxx = 0, syy = 0, sxy = 0, sxz = 0, syz = 0, sx = 0, sy = 0, sz = 0, n = 0;
for (let j = 0; j < rows; j++) {
  for (let i = 0; i < cols; i++) {
    const e = E0 + i * STEP, nn = N0 + j * STEP, v = dy[j][i];
    if (!inRing([e, nn])) continue;
    sxx += e * e; syy += nn * nn; sxy += e * nn;
    sxz += e * v; syz += nn * v; sx += e; sy += nn; sz += v; n++;
  }
}
const A = [[sxx, sxy, sx], [sxy, syy, sy], [sx, sy, n]];
const B = [sxz, syz, sz];
for (let c = 0; c < 3; c++) {
  let p = c;
  for (let r = c + 1; r < 3; r++) if (Math.abs(A[r][c]) > Math.abs(A[p][c])) p = r;
  [A[c], A[p]] = [A[p], A[c]]; [B[c], B[p]] = [B[p], B[c]];
  for (let r = 0; r < 3; r++) {
    if (r === c) continue;
    const f = A[r][c] / A[c][c];
    for (let k = c; k < 3; k++) A[r][k] -= f * A[c][k];
    B[r] -= f * B[c];
  }
}
const [ca, cb, cc] = [B[0] / A[0][0], B[1] / A[1][1], B[2] / A[2][2]];
let resid = 0, sq = 0, k = 0, over = 0;
for (let j = 0; j < rows; j++) {
  for (let i = 0; i < cols; i++) {
    const e = E0 + i * STEP, nn = N0 + j * STEP;
    if (!inRing([e, nn])) continue;
    const r = dy[j][i] - (ca * e + cb * nn + cc);
    resid = Math.max(resid, Math.abs(r));
    sq += r * r; k++;
    if (Math.abs(r) > 0.5) over++;
  }
}

const flat = dy.flat();
const out = {
  note:
    'dy(e, n) in metres, relative to the terrain at the anchor. Bilinear-interpolate ' +
    'this grid; do not use the plane fit, which is reported only to show the residual.',
  anchor_elevation_m: +anchor.toFixed(4),
  e0: E0, n0: N0, step: STEP, cols, rows,
  min_dy: +Math.min(...flat).toFixed(4),
  max_dy: +Math.max(...flat).toFixed(4),
  // THE BUILD USES THIS.
  plane_in_ring: {
    a_per_e: +ca.toFixed(6), b_per_n: +cb.toFixed(6), c: +cc.toFixed(4),
    samples: k,
    rms_residual_m: +Math.sqrt(sq / k).toFixed(4),
    max_residual_m: +resid.toFixed(4),
    samples_over_half_metre: over,
    residual_note:
      'the maximum sits in a single ~20 m dip near (e -24, n -33), a Terrarium ' +
      'DEM artefact over the Civic Center station excavation, not topography',
  },
  dy,
};
fs.writeFileSync(path.join(HERE, 'data', 'terrain_en.json'), JSON.stringify(out) + '\n');
console.log(`anchor elevation ${anchor.toFixed(3)} m`);
console.log(`grid ${cols} x ${rows} at ${STEP} m, dy ${out.min_dy} .. ${out.max_dy} m`);
console.log(`in-ring plane dy = ${ca.toFixed(5)}*e + ${cb.toFixed(5)}*n + ${cc.toFixed(4)}   (${k} samples)`);
console.log(`  rms residual ${Math.sqrt(sq / k).toFixed(3)} m, max ${resid.toFixed(3)} m, ` +
  `${over} of ${k} samples over 0.5 m`);
console.log(`  fall along the Fulton axis: ${(ca * 220).toFixed(2)} m over 220 m ` +
  `(${(ca * 100).toFixed(2)}%)`);
