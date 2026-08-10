// Geometry factory. Runs off the main thread: takes the baked binary blobs
// (quantised footprints, polylines, triangulated landcover) and produces merged,
// transfer-ready typed arrays. No JSON, no parsing, no allocation on the main
// thread.

import { emitProps, makeCtx } from './props.js';
import { readBuildings, readLandcover, readStreets } from './tilebin.js';
import { planKit } from './kitplan.js';

// Night lighting profile per category (0 residential, 1 commercial, 2 always-on,
// 3 dark), mirrored from pipeline/taxonomy.mjs. The bake already folds this into
// each record's night byte; the table is here only so props inherit the same
// profile as the building they sit on.
const NIGHT_PROFILE_OF = (nightByte) => Math.floor((nightByte + 0.5) / 4);

// --------------------------------------------------------------- near tier ---
// Full footprint extrusion: one quad per footprint edge plus the baked roof
// triangulation, flat-shaded, with per-vertex local height for the window/AO
// shader.
function buildNear(blobs, originX, originZ, palette) {
  let vertexEstimate = 0;
  const parsed = blobs.map((b) => {
    const d = readBuildings(b.buffer);
    for (let i = 0; i < d.count; i++) vertexEstimate += d.vertCount[i] * 4 + d.idxCount[i];
    return d;
  });

  const positions = new Float32Array(vertexEstimate * 3);
  const normals = new Float32Array(vertexEstimate * 3);
  const colors = new Uint8Array(vertexEstimate * 3);
  const meta = new Uint8Array(vertexEstimate * 2);
  const localY = new Uint16Array(vertexEstimate);
  const indices = new Uint32Array(vertexEstimate * 2);
  let v = 0;
  let ix = 0;
  let buildingCount = 0;

  for (const d of parsed) {
    for (let b = 0; b < d.count; b++) {
      const n = d.vertCount[b];
      if (n < 3) continue;
      const vo = d.vertOffset[b];
      const base = d.baseY[b] * 0.1;
      const top = d.topY[b] * 0.1;
      const pal = palette[d.palette[b]] || palette[0];
      const cr = pal[0];
      const cg = pal[1];
      const cb = pal[2];
      const seed = d.seed[b];
      buildingCount++;

      // Walls: one flat-shaded quad per edge.
      for (let e = 0; e < n; e++) {
        const i0 = vo + e;
        const i1 = vo + ((e + 1) % n);
        const x0 = d.originX + d.verts[i0 * 2] * d.quant - originX;
        const z0 = d.originZ + d.verts[i0 * 2 + 1] * d.quant - originZ;
        const x1 = d.originX + d.verts[i1 * 2] * d.quant - originX;
        const z1 = d.originZ + d.verts[i1 * 2 + 1] * d.quant - originZ;
        const dx = x1 - x0;
        const dz = z1 - z0;
        const len = Math.hypot(dx, dz);
        if (len < 0.05) continue;
        const nx = dz / len;
        const nz = -dx / len;

        const start = v;
        const corners = [
          [x0, base, z0, 0],
          [x1, base, z1, 0],
          [x1, top, z1, top - base],
          [x0, top, z0, top - base],
        ];
        for (const [cx, cy, cz, ly] of corners) {
          positions[v * 3] = cx;
          positions[v * 3 + 1] = cy;
          positions[v * 3 + 2] = cz;
          normals[v * 3] = nx;
          normals[v * 3 + 1] = 0;
          normals[v * 3 + 2] = nz;
          colors[v * 3] = cr;
          colors[v * 3 + 1] = cg;
          colors[v * 3 + 2] = cb;
          meta[v * 2] = seed;
          meta[v * 2 + 1] = 1; // wall
          localY[v] = Math.min(65535, Math.round(ly * 10));
          v++;
        }
        indices[ix++] = start;
        indices[ix++] = start + 1;
        indices[ix++] = start + 2;
        indices[ix++] = start;
        indices[ix++] = start + 2;
        indices[ix++] = start + 3;
      }

      // Roof: baked earcut triangulation at the top elevation.
      const roofStart = v;
      for (let k = 0; k < n; k++) {
        const i0 = vo + k;
        positions[v * 3] = d.originX + d.verts[i0 * 2] * d.quant - originX;
        positions[v * 3 + 1] = top;
        positions[v * 3 + 2] = d.originZ + d.verts[i0 * 2 + 1] * d.quant - originZ;
        normals[v * 3] = 0;
        normals[v * 3 + 1] = 1;
        normals[v * 3 + 2] = 0;
        colors[v * 3] = Math.min(255, cr * 0.82 + 12);
        colors[v * 3 + 1] = Math.min(255, cg * 0.82 + 12);
        colors[v * 3 + 2] = Math.min(255, cb * 0.82 + 12);
        meta[v * 2] = seed;
        meta[v * 2 + 1] = 0; // roof
        localY[v] = Math.min(65535, Math.round((top - base) * 10));
        v++;
      }
      const io = d.idxOffset[b];
      for (let k = 0; k < d.idxCount[b]; k += 3) {
        indices[ix++] = roofStart + d.indices[io + k];
        indices[ix++] = roofStart + d.indices[io + k + 2];
        indices[ix++] = roofStart + d.indices[io + k + 1];
      }
    }
  }

  return {
    positions: positions.subarray(0, v * 3),
    normals: normals.subarray(0, v * 3),
    colors: colors.subarray(0, v * 3),
    meta: meta.subarray(0, v * 2),
    localY: localY.subarray(0, v),
    indices: indices.subarray(0, ix),
    buildingCount,
  };
}

// ---------------------------------------------------------------- toy tier ---
// The diorama tier. Same streaming path as the near tier, but the records are
// the toy bake's chunky masses: storefront darkening is a real geometry band at
// 3.5 m, small houses carry a ridge prism, and rooftop garnish rides along as
// extra records flagged so the window-band shader leaves it alone.
const TOY_FLAG_PITCHED = 1;
const TOY_FLAG_GARNISH = 2;
const TOY_PROP_MASK = 0xf8; // bits 3..7 of the record flag byte carry PROP.*
const TOY_FLOOR = 3.5;
const TOY_ROOF_RISE = 2.5;

function buildToy(blobs, originX, originZ, palette, kitJob = null) {
  let vertexEstimate = 0;
  const parsed = blobs.map((b) => {
    const d = readBuildings(b.buffer);
    // 9 vertices per ring point covers the two wall bands and the roof; the
    // constant is the pitched-roof prism plus the lore props' worst case.
    for (let i = 0; i < d.count; i++) vertexEstimate += d.vertCount[i] * 9 + d.idxCount[i] + 420;
    return d;
  });

  // Kit first: every footprint a hand-made piece can stand on drops out of the
  // procedural extrusion below. Everything the kit cannot fit — and everything
  // in this chunk if the kit is unavailable — is still extruded exactly as
  // before, which is what keeps the two tiers seamless.
  const plan = kitJob ? planKit({ parsed, originX, originZ, ...kitJob }) : null;
  const kitFilled = plan ? plan.filled : null;
  const kitBoxes = plan ? plan.boxes : null;
  const insideKit = (x, z) => {
    if (!kitBoxes) return false;
    for (let i = 0; i < kitBoxes.length; i += 4) {
      if (x >= kitBoxes[i] && x <= kitBoxes[i + 2] && z >= kitBoxes[i + 1] && z <= kitBoxes[i + 3]) return true;
    }
    return false;
  };

  const positions = new Float32Array(vertexEstimate * 3);
  const normals = new Float32Array(vertexEstimate * 3);
  const colors = new Uint8Array(vertexEstimate * 3);
  const meta = new Uint8Array(vertexEstimate * 2);
  const localY = new Uint16Array(vertexEstimate);
  const flagAttr = new Uint8Array(vertexEstimate);
  const indices = new Uint32Array(vertexEstimate * 2);
  let v = 0;
  let ix = 0;
  let buildingCount = 0;
  let propTriangles = 0;
  let vertexFlag = 0;

  // One flat-shaded polygon. `ref` orients the face: the winding is flipped if
  // the computed normal points the wrong way, so nothing is inside-out.
  function face(points, ref, col, isWall, seed, base) {
    if (v + points.length > vertexEstimate) return;
    let nx = 0;
    let ny = 0;
    let nz = 0;
    {
      const [p0, p1, p2] = points;
      const ax = p1[0] - p0[0];
      const ay = p1[1] - p0[1];
      const az = p1[2] - p0[2];
      const bx = p2[0] - p0[0];
      const by = p2[1] - p0[1];
      const bz = p2[2] - p0[2];
      nx = ay * bz - az * by;
      ny = az * bx - ax * bz;
      nz = ax * by - ay * bx;
    }
    const len = Math.hypot(nx, ny, nz);
    if (len < 1e-9) return;
    nx /= len;
    ny /= len;
    nz /= len;
    let ordered = points;
    if (nx * ref[0] + ny * ref[1] + nz * ref[2] < 0) {
      ordered = [...points].reverse();
      nx = -nx;
      ny = -ny;
      nz = -nz;
    }
    const start = v;
    for (const p of ordered) {
      positions[v * 3] = p[0];
      positions[v * 3 + 1] = p[1];
      positions[v * 3 + 2] = p[2];
      normals[v * 3] = nx;
      normals[v * 3 + 1] = ny;
      normals[v * 3 + 2] = nz;
      colors[v * 3] = col[0];
      colors[v * 3 + 1] = col[1];
      colors[v * 3 + 2] = col[2];
      meta[v * 2] = seed;
      meta[v * 2 + 1] = isWall ? 1 : 0;
      localY[v] = Math.min(65535, Math.round(Math.max(0, p[1] - base) * 10));
      flagAttr[v] = vertexFlag;
      v++;
    }
    for (let k = 2; k < ordered.length; k++) {
      indices[ix++] = start;
      indices[ix++] = start + k - 1;
      indices[ix++] = start + k;
    }
  }

  for (let bi = 0; bi < parsed.length; bi++) {
    const d = parsed[bi];
    for (let b = 0; b < d.count; b++) {
      const n = d.vertCount[b];
      if (n < 3) continue;
      if (kitFilled && kitFilled[bi][b]) continue;
      const vo = d.vertOffset[b];
      const base = d.baseY[b] * 0.1;
      const top = d.topY[b] * 0.1;
      const flags = d.flags ? d.flags[b] : 0;
      const garnish = (flags & TOY_FLAG_GARNISH) !== 0;
      const pitched = (flags & TOY_FLAG_PITCHED) !== 0;
      const pal = palette[d.palette[b]] || palette[0];
      const seed = d.seed[b];
      const nightByte = d.night ? d.night[b] : 12; // 12 = dark profile, no glow
      if (!garnish) buildingCount++;
      // Walls carry the building's own night flag; props override it per face.
      vertexFlag = nightByte;

      const ring = new Float64Array(n * 2);
      let cx = 0;
      let cz = 0;
      for (let k = 0; k < n; k++) {
        ring[k * 2] = d.originX + d.verts[(vo + k) * 2] * d.quant - originX;
        ring[k * 2 + 1] = d.originZ + d.verts[(vo + k) * 2 + 1] * d.quant - originZ;
        cx += ring[k * 2];
        cz += ring[k * 2 + 1];
      }
      cx /= n;
      cz /= n;

      // Rooftop garnish belongs to a mass that no longer exists once its lot is
      // kit-filled, so it goes with it rather than floating over the piece.
      if (garnish && insideKit(cx, cz)) continue;

      // Storefront band: the bottom 3.5 m of every wall is a separate strip of
      // geometry, darkened at bake-time intent (x0.82) instead of in a shader.
      const dark = [
        Math.round(pal[0] * 0.82),
        Math.round(pal[1] * 0.82),
        Math.round(pal[2] * 0.82),
      ];
      const bandTop = garnish ? base : Math.min(top, base + TOY_FLOOR);

      for (let e = 0; e < n; e++) {
        const x0 = ring[e * 2];
        const z0 = ring[e * 2 + 1];
        const x1 = ring[((e + 1) % n) * 2];
        const z1 = ring[((e + 1) % n) * 2 + 1];
        if (Math.hypot(x1 - x0, z1 - z0) < 0.05) continue;
        const ref = [(x0 + x1) / 2 - cx, 0, (z0 + z1) / 2 - cz];
        if (bandTop > base + 0.01) {
          face(
            [
              [x0, base, z0],
              [x1, base, z1],
              [x1, bandTop, z1],
              [x0, bandTop, z0],
            ],
            ref,
            dark,
            true,
            seed,
            base
          );
        }
        if (top > bandTop + 0.01) {
          face(
            [
              [x0, bandTop, z0],
              [x1, bandTop, z1],
              [x1, top, z1],
              [x0, top, z0],
            ],
            ref,
            pal,
            !garnish,
            seed,
            base
          );
        }
      }

      if (pitched && n === 4) {
        // A.2 ridge prism along the OBB's long axis.
        const c = [];
        for (let k = 0; k < 4; k++) c.push([ring[k * 2], top, ring[k * 2 + 1]]);
        const e0 = Math.hypot(c[1][0] - c[0][0], c[1][2] - c[0][2]);
        const e1 = Math.hypot(c[2][0] - c[1][0], c[2][2] - c[1][2]);
        // Rotate the corner order so c0 -> c1 is always the long axis.
        const q = e0 >= e1 ? c : [c[1], c[2], c[3], c[0]];
        const shortLen = Math.min(e0, e1);
        const lx = q[1][0] - q[0][0];
        const lz = q[1][2] - q[0][2];
        const ll = Math.hypot(lx, lz) || 1;
        const inset = shortLen * 0.1;
        const ridgeY = top + TOY_ROOF_RISE;
        const mid = (a, bb) => [(a[0] + bb[0]) / 2, ridgeY, (a[2] + bb[2]) / 2];
        const rA = mid(q[3], q[0]);
        const rB = mid(q[1], q[2]);
        rA[0] += (lx / ll) * inset;
        rA[2] += (lz / ll) * inset;
        rB[0] -= (lx / ll) * inset;
        rB[2] -= (lz / ll) * inset;
        const roofPal = palette[d.roofPalette ? d.roofPalette[b] : 0] || pal;
        const up = [0, 1, 0];
        face([q[0], q[1], rB, rA], up, roofPal, false, seed, base);
        face([q[2], q[3], rA, rB], up, roofPal, false, seed, base);
        face([q[1], q[2], rB], [q[1][0] - cx, 0, q[1][2] - cz], roofPal, false, seed, base);
        face([q[3], q[0], rA], [q[3][0] - cx, 0, q[3][2] - cz], roofPal, false, seed, base);
      } else {
        // Flat roof: the baked triangulation, one flat face colour.
        const roofStart = v;
        const roofCol = [
          Math.min(255, Math.round(pal[0] * 0.94 + 8)),
          Math.min(255, Math.round(pal[1] * 0.94 + 8)),
          Math.min(255, Math.round(pal[2] * 0.94 + 8)),
        ];
        for (let k = 0; k < n; k++) {
          positions[v * 3] = ring[k * 2];
          positions[v * 3 + 1] = top;
          positions[v * 3 + 2] = ring[k * 2 + 1];
          normals[v * 3] = 0;
          normals[v * 3 + 1] = 1;
          normals[v * 3 + 2] = 0;
          colors[v * 3] = roofCol[0];
          colors[v * 3 + 1] = roofCol[1];
          colors[v * 3 + 2] = roofCol[2];
          meta[v * 2] = seed;
          meta[v * 2 + 1] = 0;
          localY[v] = Math.min(65535, Math.round((top - base) * 10));
          flagAttr[v] = vertexFlag;
          v++;
        }
        const io = d.idxOffset[b];
        for (let k = 0; k < d.idxCount[b]; k += 3) {
          indices[ix++] = roofStart + d.indices[io + k];
          indices[ix++] = roofStart + d.indices[io + k + 2];
          indices[ix++] = roofStart + d.indices[io + k + 1];
        }
      }

      // ------------------------------------------------------------ lore props
      // The category recipes. They read the same record the mass came from, so a
      // fire station's engine bays line up with its own street face, and they
      // write into the same merged buffers: no extra draw call, no new mesh.
      if (d.cat && !garnish) {
        const profile = NIGHT_PROFILE_OF(nightByte);
        const before = ix;
        const propFace = (points, ref, col, glow) => {
          // Props never grow window bands (aMeta.y = 0) and carry their own glow
          // bit, so a marquee lights up while the wall behind it does not.
          vertexFlag = profile * 4 + (glow ? 2 : 0) + 1;
          face(points, ref, col, false, seed, base);
        };
        const angle = (d.yaw[b] / 256) * Math.PI * 2;
        const ux = Math.cos(angle);
        const uz = Math.sin(angle);
        // Half-extents of this footprint measured in the street frame.
        let hu = 0;
        let hv = 0;
        for (let k = 0; k < n; k++) {
          const dx = ring[k * 2] - cx;
          const dz = ring[k * 2 + 1] - cz;
          hu = Math.max(hu, Math.abs(dx * ux + dz * uz));
          hv = Math.max(hv, Math.abs(-dx * uz + dz * ux));
        }
        const ctx = makeCtx({ cx, cz, ux, uz, vx: -uz, vz: ux }, propFace);
        const roofPal = palette[d.roofPalette ? d.roofPalette[b] : 0] || pal;
        emitProps(ctx, {
          cat: d.cat[b],
          props: (flags & TOY_PROP_MASK) >> 3,
          hu,
          hv,
          base,
          top: pitched && n === 4 ? top + TOY_ROOF_RISE : top,
          seed,
          wall: pal,
          roof: roofPal,
        });
        propTriangles += (ix - before) / 3;
        vertexFlag = nightByte;
      }
    }
  }

  return {
    positions: positions.subarray(0, v * 3),
    normals: normals.subarray(0, v * 3),
    colors: colors.subarray(0, v * 3),
    meta: meta.subarray(0, v * 2),
    localY: localY.subarray(0, v),
    flag: flagAttr.subarray(0, v),
    indices: indices.subarray(0, ix),
    buildingCount,
    propTriangles,
    kit: plan ? plan.instances : null,
    kitPieces: plan ? plan.used : null,
    kitPlaced: plan ? plan.placed : 0,
    kitConsidered: plan ? plan.considered : 0,
  };
}

// ---------------------------------------------------------------- far tier ---
// Height prisms from the footprint bounding box: 8 vertices per building with
// rounded-ish normals, plus a quadrant id so the shader can dither away the
// quarter of the super-cell that the near tier has taken over.
function buildFar(blobs, originX, originZ, palette, groupSize) {
  let total = 0;
  const parsed = blobs.map((b) => {
    const d = readBuildings(b.buffer);
    total += d.count;
    return d;
  });

  const positions = new Float32Array(total * 8 * 3);
  const normals = new Float32Array(total * 8 * 3);
  const colors = new Uint8Array(total * 8 * 3);
  const quads = new Uint8Array(total * 8);
  const indices = new Uint32Array(total * 36);
  let v = 0;
  let ix = 0;
  const half = groupSize / 2;

  for (const d of parsed) {
    for (let b = 0; b < d.count; b++) {
      const n = d.vertCount[b];
      if (n < 3) continue;
      const vo = d.vertOffset[b];
      let minX = Infinity;
      let maxX = -Infinity;
      let minZ = Infinity;
      let maxZ = -Infinity;
      for (let k = 0; k < n; k++) {
        const x = d.originX + d.verts[(vo + k) * 2] * d.quant - originX;
        const z = d.originZ + d.verts[(vo + k) * 2 + 1] * d.quant - originZ;
        if (x < minX) minX = x;
        if (x > maxX) maxX = x;
        if (z < minZ) minZ = z;
        if (z > maxZ) maxZ = z;
      }
      // Shrink slightly so the block reads as separate masses, not one slab.
      const insetX = Math.min(1.2, (maxX - minX) * 0.12);
      const insetZ = Math.min(1.2, (maxZ - minZ) * 0.12);
      minX += insetX;
      maxX -= insetX;
      minZ += insetZ;
      maxZ -= insetZ;
      const base = d.baseY[b] * 0.1;
      const top = d.topY[b] * 0.1;
      const cxMid = (minX + maxX) / 2;
      const czMid = (minZ + maxZ) / 2;
      const quad = (cxMid >= half ? 1 : 0) + (czMid >= half ? 2 : 0);
      const pal = palette[d.palette[b]] || palette[0];

      const start = v;
      for (let corner = 0; corner < 8; corner++) {
        const isTop = corner >= 4;
        const cx = corner % 4 === 0 || corner % 4 === 3 ? minX : maxX;
        const cz = corner % 4 < 2 ? minZ : maxZ;
        positions[v * 3] = cx;
        positions[v * 3 + 1] = isTop ? top : base;
        positions[v * 3 + 2] = cz;
        const nx = cx - cxMid;
        const nz = cz - czMid;
        const ny = isTop ? Math.max(6, (maxX - minX + maxZ - minZ) * 0.35) : -1;
        const len = Math.hypot(nx, ny, nz) || 1;
        normals[v * 3] = nx / len;
        normals[v * 3 + 1] = ny / len;
        normals[v * 3 + 2] = nz / len;
        const shade = isTop ? 1.0 : 0.86;
        colors[v * 3] = Math.min(255, pal[0] * shade);
        colors[v * 3 + 1] = Math.min(255, pal[1] * shade);
        colors[v * 3 + 2] = Math.min(255, pal[2] * shade);
        quads[v] = quad;
        v++;
      }
      // corners 0..3 = bottom ring (minX/minZ, maxX/minZ, maxX/maxZ, minX/maxZ)
      const q = [
        [0, 1, 5, 4],
        [1, 2, 6, 5],
        [2, 3, 7, 6],
        [3, 0, 4, 7],
        [4, 5, 6, 7],
      ];
      for (const [a, b2, c, dd] of q) {
        indices[ix++] = start + a;
        indices[ix++] = start + b2;
        indices[ix++] = start + c;
        indices[ix++] = start + a;
        indices[ix++] = start + c;
        indices[ix++] = start + dd;
      }
    }
  }

  return {
    positions: positions.subarray(0, v * 3),
    normals: normals.subarray(0, v * 3),
    colors: colors.subarray(0, v * 3),
    quads: quads.subarray(0, v),
    indices: indices.subarray(0, ix),
  };
}

// ------------------------------------------------------------------ ground ---
// Street ribbons + landcover polygons merged into one indexed, vertex-coloured
// mesh per super-cell: the whole city's ground detail in ~64 draw calls.
//
// Two passes over the same street blobs:
//   `detail: false` — the resident tier. Roads, sidewalk tops and landcover.
//   `detail: true`  — the near tier, built and dropped as the camera moves.
//     Kerb faces, centre dashes and crosswalk zebras: the things worth a
//     draw call within a few hundred metres and worth nothing beyond that.
// The sidewalk's pale top stays in the resident tier deliberately — it carries
// the road's contrast at any distance, so unloading the near tier can't pop the
// overall tone of a neighbourhood.
const PATH_LIFT = 0.35;
const KIND_ASPHALT = 64;
const KIND_SIDEWALK = 65;
const KIND_MARKING = 66;

// Chop a baked centre-dash line into its dashes. The bake ships one trimmed
// polyline per street and the rhythm rides on the class, which keeps a dashed
// street the price of one ribbon in the tile.
function chopDashes(px, py, pz, n, rhythm) {
  const cycle = rhythm.length + rhythm.gap;
  const dashes = [];
  let travelled = 0;
  let dash = null;
  const point = (x, y, z) => {
    if (!dash) dashes.push((dash = { px: [], py: [], pz: [] }));
    dash.px.push(x);
    dash.py.push(y);
    dash.pz.push(z);
  };
  for (let k = 0; k < n - 1; k++) {
    const segLen = Math.hypot(px[k + 1] - px[k], pz[k + 1] - pz[k]);
    if (segLen < 1e-4) continue;
    let s = 0;
    while (s < segLen) {
      const phase = (travelled + s) % cycle;
      const painting = phase < rhythm.length;
      const until = Math.min(segLen, s + (painting ? rhythm.length - phase : cycle - phase));
      if (painting) {
        const at = (d) => {
          const t = d / segLen;
          point(
            px[k] + (px[k + 1] - px[k]) * t,
            py[k] + (py[k + 1] - py[k]) * t,
            pz[k] + (pz[k + 1] - pz[k]) * t
          );
        };
        // A dash carried over a vertex already has its start point.
        if (!dash || s > 0) at(s);
        at(until);
        // Ending inside this segment closes the dash; ending on the vertex
        // lets it carry on into the next one.
        if (until < segLen) dash = null;
      }
      s = until;
    }
    travelled += segLen;
  }
  return dashes.filter((d) => d.px.length >= 2);
}

function buildGround(
  streetBlobs,
  landcoverBlobs,
  originX,
  originZ,
  streetClasses,
  landKinds,
  detail = false
) {
  const positions = [];
  const colors = [];
  const kinds = [];
  const indices = [];
  const paths = [];
  const trees = [];
  const lamps = [];

  const jitter = (seed) => {
    const s = Math.sin(seed * 12.9898) * 43758.5453;
    return s - Math.floor(s);
  };

  // Averaged tangent at a vertex: mitres the join so a bend has no gap.
  const tangent = (px, pz, k, n, out) => {
    let tx;
    let tz;
    if (k === 0) {
      tx = px[1] - px[0];
      tz = pz[1] - pz[0];
    } else if (k === n - 1) {
      tx = px[n - 1] - px[n - 2];
      tz = pz[n - 1] - pz[n - 2];
    } else {
      tx = px[k + 1] - px[k - 1];
      tz = pz[k + 1] - pz[k - 1];
    }
    const tl = Math.hypot(tx, tz) || 1;
    out[0] = tx / tl;
    out[1] = tz / tl;
  };

  const t2 = [0, 0];

  // Flat strip of half-width `halfW` centred on a polyline, lifted by `lift`.
  const strip = (px, py, pz, n, halfW, lift, rgb, kind) => {
    const startVertex = positions.length / 3;
    for (let k = 0; k < n; k++) {
      tangent(px, pz, k, n, t2);
      const nx = t2[1];
      const nz = -t2[0];
      positions.push(px[k] + nx * halfW, py[k] + lift, pz[k] + nz * halfW);
      colors.push(rgb[0], rgb[1], rgb[2]);
      kinds.push(kind);
      positions.push(px[k] - nx * halfW, py[k] + lift, pz[k] - nz * halfW);
      colors.push(rgb[0], rgb[1], rgb[2]);
      kinds.push(kind);
    }
    for (let k = 0; k < n - 1; k++) {
      const a = startVertex + k * 2;
      indices.push(a, a + 1, a + 2, a + 1, a + 3, a + 2);
    }
  };

  // The two vertical faces of a sidewalk plinth. Each face keeps its own
  // vertices so the normals stay flat and the kerb reads as a hard edge.
  const kerbFaces = (px, py, pz, n, halfW, height, rgb) => {
    for (const side of [1, -1]) {
      const startVertex = positions.length / 3;
      for (let k = 0; k < n; k++) {
        tangent(px, pz, k, n, t2);
        const nx = t2[1] * side * halfW;
        const nz = -t2[0] * side * halfW;
        positions.push(px[k] + nx, py[k], pz[k] + nz);
        colors.push(rgb[0], rgb[1], rgb[2]);
        kinds.push(KIND_SIDEWALK);
        positions.push(px[k] + nx, py[k] + height, pz[k] + nz);
        colors.push(rgb[0], rgb[1], rgb[2]);
        kinds.push(KIND_SIDEWALK);
      }
      for (let k = 0; k < n - 1; k++) {
        const low = startVertex + k * 2;
        const high = low + 1;
        if (side > 0) {
          indices.push(low, high + 2, low + 2, low, high, high + 2);
        } else {
          indices.push(low, low + 2, high + 2, low, high + 2, high);
        }
      }
    }
  };

  for (const blob of streetBlobs) {
    const d = readStreets(blob.buffer);
    for (let l = 0; l < d.count; l++) {
      const n = d.ptCount[l];
      if (n < 2) continue;
      const cls = streetClasses[d.klass[l]] || streetClasses[6];
      const isRoad = !cls.profile && !cls.detail;
      // A resident-tier build skips the near-tier ribbons and vice versa; the
      // sidewalk contributes to both (top strip below, kerb faces near).
      if (detail !== Boolean(cls.detail) && !cls.profile) continue;
      const po = d.ptOffset[l];
      const halfW = cls.width / 2;
      const px = new Float64Array(n);
      const py = new Float64Array(n);
      const pz = new Float64Array(n);
      for (let k = 0; k < n; k++) {
        px[k] = d.originX + d.xz[(po + k) * 2] * d.quant - originX;
        pz[k] = d.originZ + d.xz[(po + k) * 2 + 1] * d.quant - originZ;
        py[k] = d.y[po + k] * 0.1;
      }

      // Street lamps every ~42 m, standing on the sidewalk where there is one.
      if (isRoad && !detail) {
        const curb = cls.sidewalk ? cls.sidewalk.curb : 0;
        const reach = cls.sidewalk ? halfW + cls.sidewalk.width / 2 : halfW + 1.6;
        let travelled = 0;
        let side = l % 2 === 0 ? 1 : -1;
        for (let k = 0; k < n; k++) {
          if (k > 0) travelled += Math.hypot(px[k] - px[k - 1], pz[k] - pz[k - 1]);
          if (travelled < 42 && !(k === 0 && l % 3 === 0)) continue;
          travelled = 0;
          side = -side;
          tangent(px, pz, k, n, t2);
          lamps.push(
            px[k] + t2[1] * side * reach + originX,
            py[k] + curb + 6.5,
            pz[k] - t2[0] * side * reach + originZ
          );
        }
      }

      const tone = isRoad ? 0.94 + jitter(l * 3.7 + d.originX) * 0.12 : 1;
      const rgb = [
        Math.round(Math.min(255, cls.color[0] * 255 * tone)),
        Math.round(Math.min(255, cls.color[1] * 255 * tone)),
        Math.round(Math.min(255, cls.color[2] * 255 * tone)),
      ];

      if (cls.profile === 'curb') {
        if (detail) kerbFaces(px, py, pz, n, halfW, cls.lift, rgb);
        else strip(px, py, pz, n, halfW, cls.lift, rgb, KIND_SIDEWALK);
      } else if (cls.detail && cls.dash) {
        for (const dash of chopDashes(px, py, pz, n, cls.dash)) {
          strip(dash.px, dash.py, dash.pz, dash.px.length, halfW, cls.lift, rgb, KIND_MARKING);
        }
      } else {
        strip(px, py, pz, n, halfW, cls.lift || 0, rgb, cls.detail ? KIND_MARKING : KIND_ASPHALT);
      }

      // Freeways/majors/arterials double as traffic paths.
      if (isRoad && d.klass[l] <= 2) {
        const path = new Float32Array(n * 3);
        for (let k = 0; k < n; k++) {
          path[k * 3] = px[k] + originX;
          path[k * 3 + 1] = py[k] + PATH_LIFT;
          path[k * 3 + 2] = pz[k] + originZ;
        }
        paths.push({
          points: path,
          klass: d.klass[l],
          width: cls.width,
          speed: cls.speed,
          lift: PATH_LIFT,
          // Pedestrians on this street walk on the plinth top, not the asphalt.
          sidewalk: cls.sidewalk || null,
        });
      }
    }
  }

  // The near tier is markings and kerbs only; the ground it sits on is already
  // resident.
  for (const blob of detail ? [] : landcoverBlobs) {
    const d = readLandcover(blob.buffer);
    const base = positions.length / 3;
    for (let i = 0; i < d.vertexTotal; i++) {
      positions.push(
        d.originX + d.xz[i * 2] * d.quant - originX,
        d.y[i] * 0.1,
        d.originZ + d.xz[i * 2 + 1] * d.quant - originZ
      );
      const kind = d.kind[i];
      const col = landKinds[kind] ? landKinds[kind].color : [0.4, 0.4, 0.4];
      const t = 0.9 + jitter(i * 0.37 + kind) * 0.2;
      colors.push(
        Math.round(Math.min(255, col[0] * 255 * t)),
        Math.round(Math.min(255, col[1] * 255 * t)),
        Math.round(Math.min(255, col[2] * 255 * t))
      );
      kinds.push(kind);
    }
    for (let i = 0; i < d.indexTotal; i++) indices.push(base + d.indices[i]);
    for (let i = 0; i < d.treeTotal; i++) {
      trees.push(
        d.originX + d.treeXZ[i * 2] * d.quant,
        d.treeY[i] * 0.1,
        d.originZ + d.treeXZ[i * 2 + 1] * d.quant,
        d.treeVar[i]
      );
    }
  }

  const pos = new Float32Array(positions);
  const col = new Uint8Array(colors);
  const kindArr = new Uint8Array(kinds);
  const idx = new Uint32Array(indices);
  const nrm = new Float32Array(pos.length);

  // Accumulate face normals so parks and roads are lit by the slope they lie on.
  for (let i = 0; i < idx.length; i += 3) {
    const a = idx[i] * 3;
    const b = idx[i + 1] * 3;
    const c = idx[i + 2] * 3;
    const ax = pos[b] - pos[a];
    const ay = pos[b + 1] - pos[a + 1];
    const az = pos[b + 2] - pos[a + 2];
    const bx = pos[c] - pos[a];
    const by = pos[c + 1] - pos[a + 1];
    const bz = pos[c + 2] - pos[a + 2];
    const nx = ay * bz - az * by;
    const ny = az * bx - ax * bz;
    const nz = ax * by - ay * bx;
    nrm[a] += nx;
    nrm[a + 1] += ny;
    nrm[a + 2] += nz;
    nrm[b] += nx;
    nrm[b + 1] += ny;
    nrm[b + 2] += nz;
    nrm[c] += nx;
    nrm[c + 1] += ny;
    nrm[c + 2] += nz;
  }
  for (let i = 0; i < nrm.length; i += 3) {
    const len = Math.hypot(nrm[i], nrm[i + 1], nrm[i + 2]);
    if (len > 1e-6) {
      nrm[i] /= len;
      nrm[i + 1] /= len;
      nrm[i + 2] /= len;
    } else {
      nrm[i + 1] = 1;
    }
  }

  return {
    positions: pos,
    normals: nrm,
    colors: col,
    kinds: kindArr,
    indices: idx,
    trees: new Float32Array(trees),
    lamps: new Float32Array(lamps),
    paths,
  };
}

self.onmessage = (event) => {
  const msg = event.data;
  try {
    if (msg.type === 'near' || msg.type === 'toy') {
      const out =
        msg.type === 'toy'
          ? buildToy(msg.blobs, msg.originX, msg.originZ, msg.palette, msg.kit || null)
          : buildNear(msg.blobs, msg.originX, msg.originZ, msg.palette);
      const transfer = [
        out.positions.buffer,
        out.normals.buffer,
        out.colors.buffer,
        out.meta.buffer,
        out.localY.buffer,
        out.indices.buffer,
      ];
      if (out.flag) transfer.push(out.flag.buffer);
      if (out.kit) transfer.push(out.kit.buffer);
      self.postMessage({ id: msg.id, type: msg.type, key: msg.key, ...out }, transfer);
    } else if (msg.type === 'far') {
      const out = buildFar(msg.blobs, msg.originX, msg.originZ, msg.palette, msg.groupSize);
      self.postMessage({ id: msg.id, type: 'far', key: msg.key, ...out }, [
        out.positions.buffer,
        out.normals.buffer,
        out.colors.buffer,
        out.quads.buffer,
        out.indices.buffer,
      ]);
    } else if (msg.type === 'ground' || msg.type === 'grounddetail') {
      const out = buildGround(
        msg.streets,
        msg.landcover,
        msg.originX,
        msg.originZ,
        msg.streetClasses,
        msg.landKinds,
        msg.type === 'grounddetail'
      );
      self.postMessage({ id: msg.id, type: msg.type, key: msg.key, ...out }, [
        out.positions.buffer,
        out.normals.buffer,
        out.colors.buffer,
        out.kinds.buffer,
        out.indices.buffer,
        out.trees.buffer,
        out.lamps.buffer,
      ]);
    }
  } catch (err) {
    self.postMessage({ id: msg.id, type: 'error', key: msg.key, message: String(err && err.message) });
  }
};
