// The hills. One displaced grid over the whole extent, split into quadrants so
// the frustum can cull half the city, vertex-coloured from elevation, slope and
// the baked landuse raster (which is what makes Golden Gate Park read as a dark
// green rectangle from the hero view without loading any park geometry).

import { BufferAttribute, BufferGeometry, Mesh, MeshLambertMaterial } from 'three';

const SEGMENTS = 512; // per quadrant -> 1024 across the city, ~15 m spacing
const MASK = 512; // bathymetry mask resolution over the whole extent
const SEA_LEVEL = 1.2; // Terrarium reads ~0 m over the Bay and the Pacific
const SEA_FLOOR = -7;

const KIND_COLORS = {
  0: [0.33, 0.44, 0.23], // grass
  1: [0.18, 0.31, 0.16], // trees
  2: [0.79, 0.73, 0.56], // sand
  3: [0.11, 0.25, 0.31], // water
  4: [0.29, 0.43, 0.26], // pitch
  5: [0.42, 0.45, 0.27], // scrub
  6: [0.4, 0.4, 0.41], // paved
};

// Bare urban ground between the buildings: warm grey, drifting sandier towards
// the ocean side and greyer on the ridges.
function urbanColor(x, elevation, slope, out) {
  const west = Math.min(1, Math.max(0, (-x - 2000) / 5000));
  const rock = Math.min(1, slope * 2.4);
  const high = Math.min(1, Math.max(0, (elevation - 60) / 180));
  out[0] = 0.44 + west * 0.16 - high * 0.05 - rock * 0.04;
  out[1] = 0.41 + west * 0.13 - high * 0.03 - rock * 0.02;
  out[2] = 0.37 + west * 0.08 + high * 0.02;
}

// Terrarium gives the Bay and the ocean an elevation of ~0 m, which would leave
// the water plane hidden inside the terrain. Flood-fill inwards from the edges
// of the extent to find everything that is actually connected open water, then
// drop it below sea level — so Mission Bay's 3 m flats stay dry land but the
// shoreline lands exactly where the real coastline is.
function waterMask(sampleElevation, extent) {
  const { minX, maxX, minZ, maxZ } = extent;
  const stepX = (maxX - minX) / (MASK - 1);
  const stepZ = (maxZ - minZ) / (MASK - 1);
  const low = new Uint8Array(MASK * MASK);
  for (let j = 0; j < MASK; j++) {
    for (let i = 0; i < MASK; i++) {
      low[j * MASK + i] = sampleElevation(minX + i * stepX, minZ + j * stepZ) < SEA_LEVEL ? 1 : 0;
    }
  }
  const mask = new Uint8Array(MASK * MASK);
  const queue = [];
  const push = (i, j) => {
    const k = j * MASK + i;
    if (low[k] && !mask[k]) {
      mask[k] = 1;
      queue.push(k);
    }
  };
  for (let i = 0; i < MASK; i++) {
    push(i, 0);
    push(i, MASK - 1);
  }
  for (let j = 0; j < MASK; j++) {
    push(0, j);
    push(MASK - 1, j);
  }
  while (queue.length) {
    const k = queue.pop();
    const i = k % MASK;
    const j = (k - i) / MASK;
    if (i > 0) push(i - 1, j);
    if (i < MASK - 1) push(i + 1, j);
    if (j > 0) push(i, j - 1);
    if (j < MASK - 1) push(i, j + 1);
  }
  return function isWater(x, z) {
    const i = Math.round((x - minX) / stepX);
    const j = Math.round((z - minZ) / stepZ);
    if (i < 0 || j < 0 || i >= MASK || j >= MASK) return true;
    return mask[j * MASK + i] === 1;
  };
}

export function createTerrain(data) {
  const { manifest, sampleElevation, sampleLanduse } = data;
  const { minX, maxX, minZ, maxZ } = manifest.extent;
  const isWater = waterMask(sampleElevation, manifest.extent);
  const halfW = (maxX - minX) / 2;
  const halfD = (maxZ - minZ) / 2;
  const meshes = [];
  const tmp = [0, 0, 0];

  for (let qz = 0; qz < 2; qz++) {
    for (let qx = 0; qx < 2; qx++) {
      const ox = minX + qx * halfW;
      const oz = minZ + qz * halfD;
      const stepX = halfW / SEGMENTS;
      const stepZ = halfD / SEGMENTS;
      const side = SEGMENTS + 1;
      const count = side * side;
      const positions = new Float32Array(count * 3);
      const normals = new Float32Array(count * 3);
      const colors = new Float32Array(count * 3);

      for (let j = 0; j < side; j++) {
        const z = oz + j * stepZ;
        for (let i = 0; i < side; i++) {
          const x = ox + i * stepX;
          const submerged = isWater(x, z);
          const ground = sampleElevation(x, z);
          const y = submerged ? Math.min(ground, 0) + SEA_FLOOR : ground;
          const p = (j * side + i) * 3;
          positions[p] = x;
          positions[p + 1] = y;
          positions[p + 2] = z;

          // Analytic normals from the heightmap: smoother and much faster than
          // computeVertexNormals over a million vertices.
          const ex = sampleElevation(x + stepX, z) - sampleElevation(x - stepX, z);
          const ez = sampleElevation(x, z + stepZ) - sampleElevation(x, z - stepZ);
          const nx = -ex / (2 * stepX);
          const nz = -ez / (2 * stepZ);
          const len = Math.hypot(nx, 1, nz);
          normals[p] = nx / len;
          normals[p + 1] = 1 / len;
          normals[p + 2] = nz / len;

          const slope = Math.hypot(ex / (2 * stepX), ez / (2 * stepZ));
          const kind = submerged ? 3 : sampleLanduse(x, z);
          const preset = KIND_COLORS[kind];
          if (preset) {
            tmp[0] = preset[0];
            tmp[1] = preset[1];
            tmp[2] = preset[2];
          } else {
            urbanColor(x, ground, slope, tmp);
          }
          // Deterministic per-vertex mottling so large flats never look flat.
          const n = Math.sin(x * 0.031 + z * 0.017) * Math.sin(z * 0.043 - x * 0.011);
          const jitter = 1 + n * 0.05;
          colors[p] = tmp[0] * jitter;
          colors[p + 1] = tmp[1] * jitter;
          colors[p + 2] = tmp[2] * jitter;
        }
      }

      const indices = new Uint32Array(SEGMENTS * SEGMENTS * 6);
      let k = 0;
      for (let j = 0; j < SEGMENTS; j++) {
        for (let i = 0; i < SEGMENTS; i++) {
          const a = j * side + i;
          indices[k++] = a;
          indices[k++] = a + side;
          indices[k++] = a + 1;
          indices[k++] = a + 1;
          indices[k++] = a + side;
          indices[k++] = a + side + 1;
        }
      }

      const geometry = new BufferGeometry();
      geometry.setAttribute('position', new BufferAttribute(positions, 3));
      geometry.setAttribute('normal', new BufferAttribute(normals, 3));
      geometry.setAttribute('color', new BufferAttribute(colors, 3));
      geometry.setIndex(new BufferAttribute(indices, 1));
      geometry.computeBoundingSphere();

      const mesh = new Mesh(geometry, new MeshLambertMaterial({ vertexColors: true }));
      mesh.receiveShadow = true;
      mesh.name = `terrain-${qx}-${qz}`;
      meshes.push(mesh);
    }
  }

  return meshes;
}
