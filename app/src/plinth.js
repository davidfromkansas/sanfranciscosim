// The diorama plinth: the city sits on a lifted slab of earth whose side
// faces are stratified soil cross-sections — a thin green grass lip, a
// shallow lighter-brown topsoil, then a deep chocolate-brown subsoil that
// makes up most of the face. Scattered gray rocks break up the expanse.
// Two-tone face shading (each plane orientation gets its own flat tone)
// sells the volume and makes the near corner read as a hard edge.
// The slab terminates at a clean horizontal bottom — no base, no taper —
// which gives the "tabletop terrarium" quality.
//
// The top edge follows the real terrain height at each boundary point, so
// hills meet the plinth naturally and water boundaries sit at sea level.

import { BufferAttribute, BufferGeometry, Mesh } from 'three';
import { MeshLambertMaterial } from 'three';

const DEPTH = 1000; // plinth depth below y=0, meters
const GRASS_LIP = 10; // green grass lip along the top edge
const TOPSOIL_H = 40; // lighter-brown topsoil layer
const COLS = 80; // horizontal segments per face
const ROWS = 40; // vertical segments per face
const ROCKS_PER_FACE = 70;

// Deterministic hash [0,1)
function hash(x, z) {
  const s = Math.sin(x * 12.9898 + z * 78.233) * 43758.5453;
  return s - Math.floor(s);
}

// Stratum base colors (before tone multiplier and noise).
// Measured from the top edge downward.
function stratumColor(y, topY, boundaryJitter) {
  const grassBottom = topY - GRASS_LIP + boundaryJitter * 6;
  const topsoilBottom = grassBottom - TOPSOIL_H + boundaryJitter * 14;
  if (y > grassBottom) return [0.30, 0.42, 0.22]; // grass green lip
  if (y > topsoilBottom) return [0.50, 0.38, 0.26]; // topsoil lighter brown
  return [0.28, 0.19, 0.13]; // subsoil chocolate brown
}

// Face tone multipliers — isometric shading convention.
// From the hero aerial (yaw ~210°), the two visible faces are south (right,
// lighter) and west (left, darker and more saturated). The hidden faces get
// their own tones so the plinth reads correctly from any angle.
const TONE = { south: 1.0, east: 0.86, north: 0.80, west: 0.82 };

export function createPlinth(extent, sampleElevation) {
  const { minX, maxX, minZ, maxZ } = extent;
  const positions = [];
  const normals = [];
  const colors = [];
  const indices = [];

  const faces = [
    // hAxis, hMin, hMax, fixedVal, normal, tone, wind
    { hAxis: 'x', hMin: minX, hMax: maxX, fixedVal: maxZ, normal: [0, 0, 1], tone: TONE.south, wind: 'CCW' },
    { hAxis: 'x', hMin: minX, hMax: maxX, fixedVal: minZ, normal: [0, 0, -1], tone: TONE.north, wind: 'CW' },
    { hAxis: 'z', hMin: minZ, hMax: maxZ, fixedVal: maxX, normal: [1, 0, 0], tone: TONE.east, wind: 'CW' },
    { hAxis: 'z', hMin: minZ, hMax: maxZ, fixedVal: minX, normal: [-1, 0, 0], tone: TONE.west, wind: 'CCW' },
  ];

  for (const face of faces) {
    buildFace(positions, normals, colors, indices, face, sampleElevation);
    addRocks(positions, normals, colors, indices, face, sampleElevation);
  }

  buildBottom(positions, normals, colors, indices, minX, maxX, minZ, maxZ);

  const geometry = new BufferGeometry();
  geometry.setAttribute('position', new BufferAttribute(new Float32Array(positions), 3));
  geometry.setAttribute('normal', new BufferAttribute(new Float32Array(normals), 3));
  geometry.setAttribute('color', new BufferAttribute(new Float32Array(colors), 3));
  geometry.setIndex(new BufferAttribute(new Uint32Array(indices), 1));
  geometry.computeBoundingSphere();

  const material = new MeshLambertMaterial({ vertexColors: true });
  const mesh = new Mesh(geometry, material);
  mesh.name = 'plinth';
  mesh.receiveShadow = true;
  mesh.frustumCulled = false; // always visible from the hero aerial
  return mesh;
}

function buildFace(positions, normals, colors, indices, face, sampleElevation) {
  const { hAxis, hMin, hMax, fixedVal, normal, tone, wind } = face;
  const stepH = (hMax - hMin) / COLS;
  const base = positions.length / 3;

  // Per-column top Y follows the terrain, clamped to >= 0 (sea level) so
  // water boundaries sit at the surface and land hills rise to meet the edge.
  const topYs = [];
  for (let i = 0; i <= COLS; i++) {
    const h = hMin + i * stepH;
    const ground = sampleElevation(h, fixedVal);
    topYs.push(Math.max(0, ground));
  }

  for (let j = 0; j <= ROWS; j++) {
    for (let i = 0; i <= COLS; i++) {
      const h = hMin + i * stepH;
      const topY = topYs[i];
      const stepY = (topY + DEPTH) / ROWS;
      const y = topY - j * stepY;

      if (hAxis === 'x') {
        positions.push(h, y, fixedVal);
      } else {
        positions.push(fixedVal, y, h);
      }
      normals.push(normal[0], normal[1], normal[2]);

      const bj = hash(h * 0.08, fixedVal * 0.08);
      const [r, g, b] = stratumColor(y, topY, bj);
      const cn = (hash(h * 0.3 + y * 0.1, fixedVal * 0.3) - 0.5) * 0.08;
      colors.push(
        Math.max(0, r * tone + cn),
        Math.max(0, g * tone + cn),
        Math.max(0, b * tone + cn)
      );
    }
  }

  for (let j = 0; j < ROWS; j++) {
    for (let i = 0; i < COLS; i++) {
      const a = base + j * (COLS + 1) + i;
      const b = a + 1;
      const c = a + (COLS + 1);
      const d = c + 1;
      if (wind === 'CCW') {
        indices.push(a, c, b, b, c, d);
      } else {
        indices.push(a, b, c, b, d, c);
      }
    }
  }
}

function addRocks(positions, normals, colors, indices, face, sampleElevation) {
  const { hAxis, hMin, hMax, fixedVal, normal, tone, wind } = face;
  const offset = 1.5; // proud of the face surface along the normal
  const fOff = fixedVal + (normal[0] + normal[2]) * offset;

  for (let r = 0; r < ROCKS_PER_FACE; r++) {
    const h = hMin + hash(r * 7.3, fixedVal * 3.1) * (hMax - hMin);
    const ground = sampleElevation(h, fixedVal);
    const topY = Math.max(0, ground);
    // Rocks sit in the topsoil and subsoil bands, below the grass lip.
    const y = topY - GRASS_LIP - 8 - hash(r * 11.7, fixedVal * 5.3) * (DEPTH - GRASS_LIP - 20);
    const rw = 7 + hash(r * 13.1, h) * 16;
    const rh = 5 + hash(r * 17.9, y) * 10;

    const h0 = h - rw / 2;
    const h1 = h + rw / 2;
    const y0 = y - rh / 2;
    const y1 = y + rh / 2;

    const base = positions.length / 3;

    for (const [hh, yy] of [[h0, y0], [h1, y0], [h0, y1], [h1, y1]]) {
      if (hAxis === 'x') {
        positions.push(hh, yy, fOff);
      } else {
        positions.push(fOff, yy, hh);
      }
      normals.push(normal[0], normal[1], normal[2]);
    }

    const grayBase = 0.38 + (hash(h * 0.7, y * 0.7) - 0.5) * 0.18;
    const gray = Math.max(0.2, grayBase * tone);
    for (let k = 0; k < 4; k++) {
      colors.push(gray, gray * 0.95, gray * 0.90);
    }

    if (wind === 'CCW') {
      indices.push(base, base + 2, base + 1, base + 1, base + 2, base + 3);
    } else {
      indices.push(base, base + 1, base + 2, base + 1, base + 3, base + 2);
    }
  }
}

function buildBottom(positions, normals, colors, indices, minX, maxX, minZ, maxZ) {
  const y = -DEPTH;
  const base = positions.length / 3;

  // 4 corners — winding gives -Y normal (downward)
  positions.push(minX, y, minZ, maxX, y, minZ, minX, y, maxZ, maxX, y, maxZ);
  for (let i = 0; i < 4; i++) normals.push(0, -1, 0);
  for (let i = 0; i < 4; i++) colors.push(0.20, 0.14, 0.10);

  indices.push(base, base + 1, base + 2, base + 1, base + 3, base + 2);
}
