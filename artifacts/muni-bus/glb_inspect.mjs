// Raw glTF inspector — reports geometry in TRUE glTF space (Y-up), with no
// Blender axis conversion in the way. This is what three.js and
// app/src/agents.js actually see, so it is the authoritative check for the
// vehicle contract's "front faces -Z" and "min y = 0" rules.
//
//   node glb_inspect.mjs <file.glb> [more.glb ...]
//
// Handles both plain GLBs and EXT_meshopt_compression ones: for compressed
// files the accessor min/max in the JSON chunk are still authoritative for
// bounds, and primitive/material/triangle counts come from the JSON.

import { promises as fs } from 'node:fs';

function parseGLB(buf) {
  if (buf.readUInt32LE(0) !== 0x46546c67) throw new Error('not a GLB');
  const jsonLen = buf.readUInt32LE(12);
  const json = JSON.parse(buf.subarray(20, 20 + jsonLen).toString('utf8'));
  return json;
}

// World matrix of a node, walking the scene graph from the roots.
function nodeMatrices(json) {
  const out = new Map();
  const mul = (a, b) => {
    const r = new Array(16).fill(0);
    for (let i = 0; i < 4; i++)
      for (let j = 0; j < 4; j++)
        for (let k = 0; k < 4; k++) r[j * 4 + i] += a[k * 4 + i] * b[j * 4 + k];
    return r;
  };
  const trs = (n) => {
    if (n.matrix) return n.matrix.slice();
    const [tx, ty, tz] = n.translation || [0, 0, 0];
    const [qx, qy, qz, qw] = n.rotation || [0, 0, 0, 1];
    const [sx, sy, sz] = n.scale || [1, 1, 1];
    const x2 = qx + qx, y2 = qy + qy, z2 = qz + qz;
    const xx = qx * x2, xy = qx * y2, xz = qx * z2;
    const yy = qy * y2, yz = qy * z2, zz = qz * z2;
    const wx = qw * x2, wy = qw * y2, wz = qw * z2;
    return [
      (1 - (yy + zz)) * sx, (xy + wz) * sx, (xz - wy) * sx, 0,
      (xy - wz) * sy, (1 - (xx + zz)) * sy, (yz + wx) * sy, 0,
      (xz + wy) * sz, (yz - wx) * sz, (1 - (xx + yy)) * sz, 0,
      tx, ty, tz, 1,
    ];
  };
  const walk = (idx, parent) => {
    const n = json.nodes[idx];
    const m = mul(parent, trs(n));
    out.set(idx, m);
    for (const c of n.children || []) walk(c, m);
  };
  const ident = [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1];
  for (const s of json.scenes || []) for (const r of s.nodes || []) walk(r, ident);
  return out;
}

function xform(m, p) {
  return [
    m[0] * p[0] + m[4] * p[1] + m[8] * p[2] + m[12],
    m[1] * p[0] + m[5] * p[1] + m[9] * p[2] + m[13],
    m[2] * p[0] + m[6] * p[1] + m[10] * p[2] + m[14],
  ];
}

export function inspect(json) {
  const mats = nodeMatrices(json);
  const min = [Infinity, Infinity, Infinity];
  const max = [-Infinity, -Infinity, -Infinity];
  // Per-half-of-Z bounds, so we can say which end carries the tall/short mass.
  let tris = 0;
  let prims = 0;
  const materials = new Set();
  const perMesh = [];

  for (const [idx, m] of mats) {
    const node = json.nodes[idx];
    if (node.mesh === undefined) continue;
    const mesh = json.meshes[node.mesh];
    const lmin = [Infinity, Infinity, Infinity];
    const lmax = [-Infinity, -Infinity, -Infinity];
    for (const p of mesh.primitives) {
      prims++;
      if (p.material !== undefined) materials.add(json.materials[p.material].name);
      const acc = json.accessors[p.attributes.POSITION];
      const count = p.indices !== undefined ? json.accessors[p.indices].count : acc.count;
      tris += count / 3;
      // 8 corners of the accessor AABB through the node matrix
      for (let i = 0; i < 8; i++) {
        const c = [
          i & 1 ? acc.max[0] : acc.min[0],
          i & 2 ? acc.max[1] : acc.min[1],
          i & 4 ? acc.max[2] : acc.min[2],
        ];
        const w = xform(m, c);
        for (let k = 0; k < 3; k++) {
          min[k] = Math.min(min[k], w[k]);
          max[k] = Math.max(max[k], w[k]);
          lmin[k] = Math.min(lmin[k], w[k]);
          lmax[k] = Math.max(lmax[k], w[k]);
        }
      }
    }
    perMesh.push({
      name: node.name || mesh.name,
      materials: mesh.primitives.map((p) => (p.material !== undefined ? json.materials[p.material].name : null)),
      min: lmin.map((v) => +v.toFixed(3)),
      max: lmax.map((v) => +v.toFixed(3)),
    });
  }

  return {
    meshNodes: perMesh.length,
    primitives: prims,
    triangles: tris,
    materials: [...materials].sort(),
    images: (json.images || []).length,
    cameras: (json.cameras || []).length,
    animations: (json.animations || []).length,
    skins: (json.skins || []).length,
    extensionsRequired: json.extensionsRequired || [],
    min: min.map((v) => +v.toFixed(4)),
    max: max.map((v) => +v.toFixed(4)),
    dims: [0, 1, 2].map((i) => +(max[i] - min[i]).toFixed(4)),
    minY: +min[1].toFixed(4),
    centreXZ: [+((min[0] + max[0]) / 2).toFixed(4), +((min[2] + max[2]) / 2).toFixed(4)],
    perMesh,
  };
}

if (import.meta.url === `file://${process.argv[1]}`) {
  for (const f of process.argv.slice(2)) {
    const json = parseGLB(await fs.readFile(f));
    const r = inspect(json);
    const { perMesh, ...head } = r;
    console.log(`\n=== ${f}`);
    console.log(JSON.stringify(head, null, 2));
    if (process.argv.includes('--meshes')) console.log(JSON.stringify(perMesh, null, 2));
  }
}
