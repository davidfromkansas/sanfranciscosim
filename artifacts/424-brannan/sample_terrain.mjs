// Sample the baked terrain under the 424 Brannan lot, in the lot's (u, v) frame.
//
//     node sample_terrain.mjs          # writes data/terrain_uv.json
//
// Why this exists. `placeGeneric()` in app/src/assets.js seats a landmark with
// ONE terrain sample, taken at the anchor:
//
//     const y = Math.max(0, data.sampleElevation(x, z));
//
// Right for a building — a compact footprint on a slope buries its base uphill,
// which is what a real building does. Wrong for an asset that IS the ground.
// This lot falls 1.47 m across an 88.7 x 59.6 m bounding box, so a flat plate
// seated at the anchor would be ~0.78 m under the terrain at the Zoe end and
// ~0.69 m above it at the Brannan corner. That is invisible in every Blender
// render and obvious in the running app. See artifacts/64-south-park/REFERENCE.md,
// "The terrain drape", where this failure was found the first time.
//
// Output is a regular (u, v) GRID of dy rather than South Park's 1-D profile,
// because this site falls in two directions at once (2.18% toward bearing 250).
// A plane fit is ALSO reported — it comes out good to ~0.1 m — but the build
// interpolates the grid, not the plane, so the plate hugs the same bilinear
// surface the runtime's sampleElevation() evaluates and the residual is nil.
//
// dy is relative to the anchor's elevation, so dy(0,0) = 0 by construction: the
// asset's z = 0 plane is the anchor's ground, which is where the loader puts it.
//
// Source: app/public/tiles/terrain.bin + the `terrain` block of
// app/public/tiles/manifest.json. That is the SAME baked heightmap as
// pipeline/out/terrain.bin (pipeline/lib/heightmap.mjs reads the latter with the
// identical descriptor fields); the committed app copy is used here so the
// artifact rebuilds without a 700 MB pipeline/data checkout.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const REPO = path.resolve(HERE, '../..');
const site = JSON.parse(fs.readFileSync(path.join(HERE, 'data', 'site_uv.json'), 'utf8'));

const M = JSON.parse(fs.readFileSync(path.join(REPO, 'app/public/tiles/manifest.json'), 'utf8'));
const T = M.terrain;
const buf = fs.readFileSync(path.join(REPO, 'app/public/tiles/terrain.bin'));
const data = new Int16Array(buf.buffer, buf.byteOffset, buf.byteLength / 2);

function sampleElevation(x, z) {
  const fx = (x - T.minX) / T.cellX;
  const fz = (z - T.minZ) / T.cellZ;
  const ix = Math.min(T.size - 2, Math.max(0, Math.floor(fx)));
  const iz = Math.min(T.size - 2, Math.max(0, Math.floor(fz)));
  const tx = Math.min(1, Math.max(0, fx - ix));
  const tz = Math.min(1, Math.max(0, fz - iz));
  const a = data[iz * T.size + ix];
  const b = data[iz * T.size + ix + 1];
  const c = data[(iz + 1) * T.size + ix];
  const d = data[(iz + 1) * T.size + ix + 1];
  const top = a + (b - a) * tx;
  const bot = c + (d - c) * tx;
  return (top + (bot - top) * tz) * T.scale;
}

const [ax, az] = site.anchor_world;
const R = (d) => (d * Math.PI) / 180;
const U = [Math.sin(R(site.heading_u_deg)), Math.cos(R(site.heading_u_deg))];
const V = [Math.sin(R(site.heading_v_deg)), Math.cos(R(site.heading_v_deg))];
// (u, v) -> blender (X east, Y north) -> world (x east, z south)
const toWorld = (u, v) => [ax + u * U[0] + v * V[0], az - (u * U[1] + v * V[1])];

const base = sampleElevation(ax, az);

const ring = site.ring_uv;
const U_MIN = Math.floor(Math.min(...ring.map((p) => p[0])) - 4);
const U_MAX = Math.ceil(Math.max(...ring.map((p) => p[0])) + 4);
const V_MIN = Math.floor(Math.min(...ring.map((p) => p[1])) - 4);
const V_MAX = Math.ceil(Math.max(...ring.map((p) => p[1])) + 4);
const STEP = 2.0;
const NU = Math.round((U_MAX - U_MIN) / STEP) + 1;
const NV = Math.round((V_MAX - V_MIN) / STEP) + 1;

const grid = [];
for (let j = 0; j < NV; j++) {
  const row = [];
  for (let i = 0; i < NU; i++) {
    const dy = sampleElevation(...toWorld(U_MIN + i * STEP, V_MIN + j * STEP)) - base;
    row.push(Math.round(dy * 10000) / 10000);
  }
  grid.push(row);
}

// Least-squares plane over the samples that actually lie inside the lot, in
// BLENDER XY so the coefficients are quotable in the plan and the report.
function inside(u, v) {
  let c = false;
  for (let i = 0, n = ring.length; i < n; i++) {
    const [u1, v1] = ring[i];
    const [u2, v2] = ring[(i + 1) % n];
    if ((v1 > v) !== (v2 > v) && u < ((u2 - u1) * (v - v1)) / (v2 - v1) + u1) c = !c;
  }
  return c;
}
const P = [];
for (let u = U_MIN; u <= U_MAX; u += 0.5) {
  for (let v = V_MIN; v <= V_MAX; v += 0.5) {
    if (!inside(u, v)) continue;
    const X = u * U[0] + v * V[0];
    const Y = u * U[1] + v * V[1];
    P.push([X, Y, sampleElevation(...toWorld(u, v)) - base]);
  }
}
const S = [[0, 0, 0], [0, 0, 0], [0, 0, 0]];
const Tv = [0, 0, 0];
for (const [X, Y, D] of P) {
  const r = [X, Y, 1];
  for (let i = 0; i < 3; i++) {
    for (let j = 0; j < 3; j++) S[i][j] += r[i] * r[j];
    Tv[i] += r[i] * D;
  }
}
function solve3(A, b) {
  const m = A.map((r, i) => [...r, b[i]]);
  for (let i = 0; i < 3; i++) {
    let p = i;
    for (let k = i + 1; k < 3; k++) if (Math.abs(m[k][i]) > Math.abs(m[p][i])) p = k;
    [m[i], m[p]] = [m[p], m[i]];
    for (let k = i + 1; k < 3; k++) {
      const f = m[k][i] / m[i][i];
      for (let j = i; j <= 3; j++) m[k][j] -= f * m[i][j];
    }
  }
  const x = [0, 0, 0];
  for (let i = 2; i >= 0; i--) {
    let s = m[i][3];
    for (let j = i + 1; j < 3; j++) s -= m[i][j] * x[j];
    x[i] = s / m[i][i];
  }
  return x;
}
const [gx, gy, c0] = solve3(S, Tv);
let planeResidual = 0;
let mn = Infinity;
let mx = -Infinity;
for (const [X, Y, D] of P) {
  planeResidual = Math.max(planeResidual, Math.abs(D - (gx * X + gy * Y + c0)));
  mn = Math.min(mn, D);
  mx = Math.max(mx, D);
}

const r4 = (n) => Math.round(n * 10000) / 10000;
const out = {
  _: 'GENERATED by sample_terrain.mjs — do not hand-edit',
  source: 'app/public/tiles/terrain.bin + manifest.json terrain block (AWS Terrarium, the sampler the runtime uses)',
  anchor_lonlat: site.anchor_lonlat,
  anchor_elevation_m: r4(base),
  u_min: U_MIN, v_min: V_MIN, step: STEP, nu: NU, nv: NV,
  fall_m: r4(mx - mn),
  dy_min: r4(mn),
  dy_max: r4(mx),
  plane: { gx: r4(gx), gy: r4(gy), c: r4(c0), max_residual_m: r4(planeResidual),
           slope_pct: r4(Math.hypot(gx, gy) * 100),
           downhill_bearing_deg: Math.round(((Math.atan2(-gx, -gy) * 180) / Math.PI + 360) % 360) },
  samples_in_lot: P.length,
  grid,
};
fs.writeFileSync(path.join(HERE, 'data', 'terrain_uv.json'), JSON.stringify(out, null, 1));

console.log(`anchor elevation   ${out.anchor_elevation_m} m`);
console.log(`fall under the lot ${out.fall_m} m   (dy ${out.dy_min} .. ${out.dy_max})`);
console.log(`best-fit plane     dy = ${out.plane.gx}*X + ${out.plane.gy}*Y + ${out.plane.c}`);
console.log(`                   ${out.plane.slope_pct}% downhill toward ${out.plane.downhill_bearing_deg} deg`);
console.log(`plane residual     ${out.plane.max_residual_m} m  <- why the build drapes the GRID, not the plane`);
console.log(`grid               ${NU} x ${NV} at ${STEP} m from (u ${U_MIN}, v ${V_MIN})`);
console.log('wrote data/terrain_uv.json');
