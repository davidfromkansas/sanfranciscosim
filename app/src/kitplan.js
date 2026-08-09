// Where every kit piece goes.
//
// This is the placement brain for the 207-piece building kit: it reads the same
// baked toy records the procedural masses are extruded from, works out which
// piece belongs on each footprint, and returns one instance per fit. It is pure
// arithmetic — no three, no DOM — so the tile worker and the offline fit-rate
// report run the exact same decisions.
//
// Nothing here scales a piece in width or height: a piece is placed only when a
// hand-made model of the right size already exists for that lot. Everything it
// cannot fit is left to the procedural TOY2 extrusion, which is why the two
// always coexist on screen.

import { readBuildings, readStreets } from './tilebin.js';

export const ZONE = {
  OTHER: 0,
  SUNSET: 1,
  RICHMOND: 2,
  VICTORIAN: 3,
  MARINA: 4,
  DENSE: 5,
  DOWNTOWN: 6,
  INDUSTRIAL: 7,
};

// The context layer's 41 analysis neighbourhoods, mapped onto the eight fabric
// zones the kit is authored for.
export const NEIGHBORHOOD_ZONE = {
  'Sunset/Parkside': ZONE.SUNSET,
  'Inner Sunset': ZONE.SUNSET,
  Lakeshore: ZONE.SUNSET,
  'West of Twin Peaks': ZONE.SUNSET,
  'Twin Peaks': ZONE.SUNSET,
  'Inner Richmond': ZONE.RICHMOND,
  'Outer Richmond': ZONE.RICHMOND,
  Seacliff: ZONE.RICHMOND,
  'Lone Mountain/USF': ZONE.RICHMOND,
  'Presidio Heights': ZONE.RICHMOND,
  'Oceanview/Merced/Ingleside': ZONE.RICHMOND,
  'Western Addition': ZONE.VICTORIAN,
  'Haight Ashbury': ZONE.VICTORIAN,
  'Hayes Valley': ZONE.VICTORIAN,
  Japantown: ZONE.VICTORIAN,
  Mission: ZONE.VICTORIAN,
  'Noe Valley': ZONE.VICTORIAN,
  'Castro/Upper Market': ZONE.VICTORIAN,
  'Bernal Heights': ZONE.VICTORIAN,
  'Pacific Heights': ZONE.VICTORIAN,
  'Glen Park': ZONE.VICTORIAN,
  Excelsior: ZONE.VICTORIAN,
  'Outer Mission': ZONE.VICTORIAN,
  Portola: ZONE.VICTORIAN,
  'Visitacion Valley': ZONE.VICTORIAN,
  Marina: ZONE.MARINA,
  Tenderloin: ZONE.DENSE,
  'Nob Hill': ZONE.DENSE,
  'Russian Hill': ZONE.DENSE,
  Chinatown: ZONE.DENSE,
  'North Beach': ZONE.DENSE,
  'Financial District/South Beach': ZONE.DOWNTOWN,
  'South of Market': ZONE.INDUSTRIAL,
  'Mission Bay': ZONE.INDUSTRIAL,
  'Potrero Hill': ZONE.INDUSTRIAL,
  'Bayview Hunters Point': ZONE.INDUSTRIAL,
  'Treasure Island': ZONE.INDUSTRIAL,
};

// Residential typology by zone: the first family that has a piece for the lot
// wins, so a Sunset lot too wide for a Doelger row house lands on an apartment
// rather than on a Victorian.
const HOUSE_FAMILIES = {
  [ZONE.SUNSET]: ['sunset', 'richmond', 'edwardian', 'apt'],
  [ZONE.RICHMOND]: ['richmond', 'sunset', 'edwardian', 'marina', 'apt'],
  [ZONE.VICTORIAN]: ['italianate', 'stick', 'queenanne', 'edwardian', 'apt'],
  [ZONE.MARINA]: ['marina', 'edwardian', 'italianate', 'apt'],
  [ZONE.DENSE]: ['edwardian', 'italianate', 'aptfe', 'apt'],
  [ZONE.DOWNTOWN]: ['edwardian', 'aptfe', 'apt'],
  [ZONE.INDUSTRIAL]: ['edwardian', 'apt', 'aptfe'],
  [ZONE.OTHER]: ['edwardian', 'sunset', 'richmond', 'italianate', 'apt'],
};

// Everything that is not a house: the taxonomy category picks the family set,
// the zone only nudges it.
function familiesFor(cat, zone, height) {
  switch (cat) {
    case 1:
      return HOUSE_FAMILIES[zone] || HOUSE_FAMILIES[ZONE.OTHER];
    case 2:
      return zone === ZONE.DENSE || zone === ZONE.DOWNTOWN
        ? ['aptfe', 'apt', 'mixeduse']
        : ['apt', 'aptfe', 'mixeduse'];
    case 3:
      if (height > 58) return ['tower', 'office'];
      return zone === ZONE.DOWNTOWN || zone === ZONE.INDUSTRIAL
        ? ['office', 'tower', 'mixeduse']
        : ['office', 'mixeduse', 'apt'];
    case 4:
      return ['storefront', 'mixeduse', 'corner', 'liquor', 'bank'];
    case 5:
    case 6:
      return ['storefront', 'mixeduse', 'corner'];
    case 7:
      return ['hotel', 'apt', 'aptfe'];
    case 8:
      return ['church', 'synagogue', 'pagoda', 'chapel'];
    case 9:
    case 10:
      return ['school', 'government'];
    case 11:
      return ['hospital'];
    case 13:
      return ['firehouse'];
    case 14:
      return ['police'];
    case 15:
      return ['library'];
    case 16:
      return ['museum'];
    case 17:
      return ['theater'];
    case 18:
      return ['government'];
    case 19:
    case 20:
      return ['industrial'];
    case 24:
      return ['gym'];
    case 25:
      return ['transit'];
    case 0:
      // Unclassified: the neighbourhood's own residential fabric, or a plain
      // apartment block once the mass is too big to read as a house.
      return height > 18 ? ['apt', 'aptfe', 'office'] : HOUSE_FAMILIES[zone] || HOUSE_FAMILIES[ZONE.OTHER];
    default:
      return null;
  }
}

// A handful of pieces are one-offs whose kind says nothing about their use: the
// gas station, the supermarket, the parking deck. They are only ever placed on
// a footprint whose category actually asks for them.
const IDS_BY_CAT = {
  21: ['gas'],
  22: ['market_s', 'market_l'],
  23: ['parking_s', 'parking_l'],
  24: ['gym', 'dojo'],
  7: ['hotel_block', 'motel'],
};
// ...and are never reachable through a family, so a "shop" is never a petrol
// station and an office block never becomes a motel.
const OFF_FAMILY_IDS = new Set([
  'gas',
  'market_s',
  'market_l',
  'parking_s',
  'parking_l',
  'motel',
  'boathouse',
  'marina_shed',
  'strip',
  'datacenter',
  'senior_home',
  'dorm_slab',
  'post_office',
  'cablecar_barn',
  'dojo',
]);

const WIDE_LOT_KINDS = new Set(['tower', 'office', 'industrial', 'hospital', 'school', 'government', 'museum']);

// Corner-specific pieces: the chamfer/turret is authored on the model's front
// left, so they only make sense where a second street actually crosses.
const CORNER_RE = /(^|_)(corner|turret|wrap)(_|$)/;

// The painted-lady palette, plus plain white at roughly a fifth of the lots.
// Indices 10 and 11 are "no tint".
export const KIT_TINTS = [
  '#e8d9a8',
  '#a8c4d4',
  '#d4b0c0',
  '#c9d4c0',
  '#e6d0b8',
  '#b8d4cc',
  '#d8c8b0',
  '#cfc3de',
  '#e2b8a8',
  '#dcd3c4',
  '#ffffff',
  '#ffffff',
];
// Downtown, civic and industrial pieces stay in the calm warm-white end.
const NEUTRAL_TINTS = [10, 11, 0, 4, 6, 9, 11];
const TINTED_CATS = new Set([1, 2, 4, 5, 6, 7]);

export const KIT_STRIDE = 8;

// Mirrored from the toy bake: a pitched record stores its wall height, and the
// worker grows the ridge prism on top of it, so the mass a kit piece has to
// match is that much taller than the record says.
const TOY_FLAG_PITCHED = 1;
const TOY_ROOF_RISE = 2.5;

function hash(x, z, salt) {
  let h = Math.imul(Math.round(x * 4) | 0, 374761393) ^ Math.imul(Math.round(z * 4) | 0, 668265263);
  h = (h ^ Math.imul(salt | 0, 2246822519)) >>> 0;
  h = Math.imul(h ^ (h >>> 13), 1274126177) >>> 0;
  return (h ^ (h >>> 16)) >>> 0;
}

// Street segments near the chunk, in a coarse grid so the nearest-street query
// for a few thousand footprints stays linear.
const SEGMENT_CELL = 80;

function buildSegmentGrid(streetBlobs, originX, originZ) {
  const ax = [];
  const az = [];
  const bx = [];
  const bz = [];
  const klass = [];
  for (const blob of streetBlobs) {
    const d = readStreets(blob.buffer);
    for (let l = 0; l < d.count; l++) {
      const n = d.ptCount[l];
      const po = d.ptOffset[l];
      for (let k = 1; k < n; k++) {
        const x0 = d.originX + d.xz[(po + k - 1) * 2] * d.quant - originX;
        const z0 = d.originZ + d.xz[(po + k - 1) * 2 + 1] * d.quant - originZ;
        const x1 = d.originX + d.xz[(po + k) * 2] * d.quant - originX;
        const z1 = d.originZ + d.xz[(po + k) * 2 + 1] * d.quant - originZ;
        if (Math.hypot(x1 - x0, z1 - z0) < 1) continue;
        ax.push(x0);
        az.push(z0);
        bx.push(x1);
        bz.push(z1);
        klass.push(d.klass[l]);
      }
    }
  }

  const cells = new Map();
  const put = (cx, cz, i) => {
    const key = cx * 8192 + cz;
    let list = cells.get(key);
    if (!list) cells.set(key, (list = []));
    list.push(i);
  };
  for (let i = 0; i < ax.length; i++) {
    const c0x = Math.floor(Math.min(ax[i], bx[i]) / SEGMENT_CELL);
    const c1x = Math.floor(Math.max(ax[i], bx[i]) / SEGMENT_CELL);
    const c0z = Math.floor(Math.min(az[i], bz[i]) / SEGMENT_CELL);
    const c1z = Math.floor(Math.max(az[i], bz[i]) / SEGMENT_CELL);
    for (let cx = c0x; cx <= c1x; cx++) for (let cz = c0z; cz <= c1z; cz++) put(cx, cz, i);
  }
  return { ax, az, bx, bz, klass, cells, count: ax.length };
}

function closestOn(grid, i, x, z) {
  const dx = grid.bx[i] - grid.ax[i];
  const dz = grid.bz[i] - grid.az[i];
  const l2 = dx * dx + dz * dz || 1;
  const t = Math.max(0, Math.min(1, ((x - grid.ax[i]) * dx + (z - grid.az[i]) * dz) / l2));
  const px = grid.ax[i] + dx * t;
  const pz = grid.az[i] + dz * t;
  return { px, pz, dist: Math.hypot(x - px, z - pz), dirX: dx / Math.sqrt(l2), dirZ: dz / Math.sqrt(l2) };
}

// The two streets a lot can front: the nearest one, and the nearest one running
// across it. Corner pieces need both.
function streetsAt(grid, x, z, radius) {
  const span = Math.ceil(radius / SEGMENT_CELL);
  const cx = Math.floor(x / SEGMENT_CELL);
  const cz = Math.floor(z / SEGMENT_CELL);
  let best = null;
  let cross = null;
  for (let gz = cz - span; gz <= cz + span; gz++) {
    for (let gx = cx - span; gx <= cx + span; gx++) {
      const list = grid.cells.get(gx * 8192 + gz);
      if (!list) continue;
      for (const i of list) {
        const hit = closestOn(grid, i, x, z);
        if (hit.dist > radius) continue;
        if (!best || hit.dist < best.dist) best = hit;
      }
    }
  }
  if (!best) return { best: null, cross: null };
  for (let gz = cz - span; gz <= cz + span; gz++) {
    for (let gx = cx - span; gx <= cx + span; gx++) {
      const list = grid.cells.get(gx * 8192 + gz);
      if (!list) continue;
      for (const i of list) {
        const hit = closestOn(grid, i, x, z);
        if (hit.dist > radius) continue;
        // "Across" means the run turns at least 35° away from the frontage.
        if (Math.abs(hit.dirX * best.dirX + hit.dirZ * best.dirZ) > 0.82) continue;
        if (!cross || hit.dist < cross.dist) cross = hit;
      }
    }
  }
  return { best, cross };
}

export function createKitCatalog(index) {
  const renames = index.renames_v2 || {};
  const pieces = index.pieces.map((p, i) => ({
    i,
    id: p.id,
    file: p.file,
    kind: p.kind,
    cat: p.cat,
    w: p.w ?? null,
    dx: p.dims[0],
    dy: p.dims[1],
    dz: p.dims[2],
    tris: p.tris,
    corner: CORNER_RE.test(p.id),
    offFamily: OFF_FAMILY_IDS.has(p.id),
  }));
  const byId = new Map(pieces.map((p) => [p.id, p]));
  const byKind = new Map();
  for (const p of pieces) {
    if (!byKind.has(p.kind)) byKind.set(p.kind, []);
    byKind.get(p.kind).push(p);
  }
  // renames_v2 is load-bearing: 67 v1 ids no longer exist as files, and any id
  // written down before this pack has to keep resolving.
  const resolve = (id) => byId.get(renames[id] || id) || null;
  return { pieces, byId, byKind, renames, resolve };
}

// The worker only needs the numbers, and structured-cloning 207 small records
// per tile job is cheaper than keeping worker state in sync. `disabled` carries
// the pieces whose GLB turned out to be missing or off-contract, so a re-run of
// the same chunk plans around them instead of leaving a hole.
export function catalogForWorker(catalog, disabled = []) {
  return {
    disabled: [...disabled],
    pieces: catalog.pieces.map((p) => ({
      i: p.i,
      id: p.id,
      kind: p.kind,
      cat: p.cat,
      dx: p.dx,
      dy: p.dy,
      dz: p.dz,
      corner: p.corner,
      offFamily: p.offFamily,
    })),
  };
}

function hydrate(plain) {
  const disabled = new Set(plain.disabled || []);
  const pieces = plain.pieces.filter((p) => !disabled.has(p.i));
  const byId = new Map(pieces.map((p) => [p.id, p]));
  const byKind = new Map();
  for (const p of pieces) {
    if (!byKind.has(p.kind)) byKind.set(p.kind, []);
    byKind.get(p.kind).push(p);
  }
  return { pieces, byId, byKind };
}

function zoneAt(zones, worldX, worldZ) {
  if (!zones) return ZONE.OTHER;
  const gx = Math.floor((worldX - zones.originX) / zones.cell);
  const gz = Math.floor((worldZ - zones.originZ) / zones.cell);
  if (gx < 0 || gz < 0 || gx >= zones.cols || gz >= zones.rows) return ZONE.OTHER;
  return zones.data[gz * zones.cols + gx];
}

// One footprint's candidates, best first. `cost` mixes how much frontage the
// piece leaves empty with how far its fixed height is from the real one.
function candidatesFor(kit, cat, zone, frontage, depth, height, corner, debug = null) {
  const ids = IDS_BY_CAT[cat];
  const families = familiesFor(cat, zone, height);
  const out = [];
  const note = (why) => {
    if (debug) debug[why] = (debug[why] || 0) + 1;
  };
  const consider = (piece, rank) => {
    if (piece.dx > frontage + 0.6) return note('wide');
    // A house has to hold its whole frontage or the row gaps; a tower or an
    // office block is allowed to stand on a lot bigger than itself, the way the
    // real ones sit back from the pavement behind a plaza.
    if (piece.dx < frontage * (WIDE_LOT_KINDS.has(piece.kind) ? 0.42 : 0.58)) return note('narrow');
    if (piece.dy > depth * 2.2 + 6) return note('deep');
    const dh = Math.abs(piece.dz - height);
    if (dh > Math.max(4, height * 0.42)) return note('height');
    if (piece.corner !== corner) return note('corner');
    out.push({
      piece,
      cost: rank * 0.4 + (frontage - piece.dx) / Math.max(6, frontage) + (dh / Math.max(6, height)) * 1.3,
    });
  };

  if (ids) {
    for (const id of ids) {
      const piece = kit.byId.get(id);
      if (piece) consider(piece, 0);
    }
  }
  if (families) {
    for (let rank = 0; rank < families.length; rank++) {
      const list = kit.byKind.get(families[rank]);
      if (!list) continue;
      for (const piece of list) {
        if (piece.offFamily) continue;
        consider(piece, rank);
      }
    }
  }
  out.sort((a, b) => a.cost - b.cost);
  return out;
}

/**
 * Plans every kit instance for one 1 km chunk.
 *
 * @param {object} job - parsed tile blobs plus the catalog, zone raster,
 *   street blobs and landmark exclusion discs.
 * @returns {{instances: Float32Array, used: number[], filled: Uint8Array[],
 *   boxes: Float32Array, considered: number, placed: number}}
 */
export function planKit(job) {
  const { parsed, originX, originZ, zones, streets = [], exclusions = null, debug = null } = job;
  const kit = hydrate(job.kit);
  const reject = (reason) => {
    if (debug) debug[reason] = (debug[reason] || 0) + 1;
  };
  const grid = buildSegmentGrid(streets, originX, originZ);
  const filled = parsed.map((d) => new Uint8Array(d.count));
  const boxes = [];
  const rows = new Map();
  const placements = [];
  let considered = 0;

  for (let bi = 0; bi < parsed.length; bi++) {
    const d = parsed[bi];
    for (let b = 0; b < d.count; b++) {
      const n = d.vertCount[b];
      if (n < 3) continue;
      const flags = d.flags ? d.flags[b] : 0;
      if (flags & 2) continue; // rooftop garnish rides on its parent
      considered++;
      const vo = d.vertOffset[b];
      let cx = 0;
      let cz = 0;
      let minX = Infinity;
      let maxX = -Infinity;
      let minZ = Infinity;
      let maxZ = -Infinity;
      const ring = new Float64Array(n * 2);
      for (let k = 0; k < n; k++) {
        const x = d.originX + d.verts[(vo + k) * 2] * d.quant - originX;
        const z = d.originZ + d.verts[(vo + k) * 2 + 1] * d.quant - originZ;
        ring[k * 2] = x;
        ring[k * 2 + 1] = z;
        cx += x;
        cz += z;
        if (x < minX) minX = x;
        if (x > maxX) maxX = x;
        if (z < minZ) minZ = z;
        if (z > maxZ) maxZ = z;
      }
      cx /= n;
      cz /= n;

      const worldX = cx + originX;
      const worldZ = cz + originZ;
      if (exclusions) {
        let blocked = false;
        for (let e = 0; e < exclusions.length; e += 3) {
          const dx = worldX - exclusions[e];
          const dz = worldZ - exclusions[e + 1];
          if (dx * dx + dz * dz < exclusions[e + 2] * exclusions[e + 2]) {
            blocked = true;
            break;
          }
        }
        if (blocked) {
          reject('landmark');
          continue;
        }
      }

      const base = d.baseY[b] * 0.1;
      const height = d.topY[b] * 0.1 - base + (flags & TOY_FLAG_PITCHED ? TOY_ROOF_RISE : 0);
      if (height < 3) {
        reject('tooShort');
        continue;
      }

      // Fronting street. Without one there is no way to orient a piece, so the
      // lot stays procedural.
      const { best, cross } = streetsAt(grid, cx, cz, 70);
      if (!best) {
        reject('noStreet');
        continue;
      }
      let front = { dirX: best.dirX, dirZ: best.dirZ, px: best.px, pz: best.pz };
      let corner = false;
      if (cross) {
        // Corner pieces carry their chamfer on the front-left, so the street
        // that crosses has to end up on that side; if it does not, the crossing
        // street becomes the frontage instead.
        const leftX = -(best.pz - cz);
        const leftZ = best.px - cx;
        const leftLen = Math.hypot(leftX, leftZ) || 1;
        const toCrossX = cross.px - cx;
        const toCrossZ = cross.pz - cz;
        const crossLen = Math.hypot(toCrossX, toCrossZ) || 1;
        const onLeft = (leftX / leftLen) * (toCrossX / crossLen) + (leftZ / leftLen) * (toCrossZ / crossLen);
        corner = cross.dist < 34;
        if (corner && onLeft < 0.35) front = { dirX: cross.dirX, dirZ: cross.dirZ, px: cross.px, pz: cross.pz };
      }

      // Street frame: u along the kerb, v from the lot out to the street.
      const ux = front.dirX;
      const uz = front.dirZ;
      let vx = front.px - cx;
      let vz = front.pz - cz;
      const vlen = Math.hypot(vx, vz);
      if (vlen < 0.5) {
        reject('onKerb');
        continue;
      }
      vx /= vlen;
      vz /= vlen;

      let minU = Infinity;
      let maxU = -Infinity;
      let minV = Infinity;
      let maxV = -Infinity;
      for (let k = 0; k < n; k++) {
        const dx = ring[k * 2] - cx;
        const dz = ring[k * 2 + 1] - cz;
        const u = dx * ux + dz * uz;
        const v = dx * vx + dz * vz;
        if (u < minU) minU = u;
        if (u > maxU) maxU = u;
        if (v < minV) minV = v;
        if (v > maxV) maxV = v;
      }
      const frontage = maxU - minU;
      const depth = maxV - minV;
      if (frontage < 5 || depth < 4) {
        reject('tinyLot');
        continue;
      }

      const cat = d.cat ? d.cat[b] : 0;
      const zone = zoneAt(zones, worldX, worldZ);
      let list = candidatesFor(kit, cat, zone, frontage, depth, height, corner, debug);
      // A lot on a corner that has no corner piece its size still deserves a
      // building: fall back to the plain frontage pieces.
      if (!list.length && corner) list = candidatesFor(kit, cat, zone, frontage, depth, height, false);
      if (!list.length) {
        reject(`noPiece:cat${cat}:w${Math.round(frontage / 2) * 2}:h${Math.round(height / 3) * 3}`);
        continue;
      }

      const h = hash(worldX, worldZ, 17);
      // Anything within a whisker of the best fit is equally right, so the lot's
      // own hash picks between them: neighbouring lots get different bays,
      // gables and setbacks instead of one variant repeating down the block.
      let band = 1;
      while (band < list.length && list[band].cost <= list[0].cost + 0.12) band++;
      const choice = h % band;
      const tint = TINTED_CATS.has(cat)
        ? h % KIT_TINTS.length
        : NEUTRAL_TINTS[h % NEUTRAL_TINTS.length];

      // Rows abut, so a piece is centred on its own frontage and pushed up
      // against the kerb: the gap to the neighbour is whatever the lot has
      // spare, never a setback difference.
      const midU = (minU + maxU) / 2;
      const frontX = cx + ux * midU + vx * maxV;
      const frontZ = cz + uz * midU + vz * maxV;

      placements.push({
        blob: bi,
        record: b,
        list,
        choice,
        tint,
        frontX,
        frontZ,
        base,
        yaw: Math.atan2(vx, vz),
        depth,
        hash: h,
        box: [minX, minZ, maxX, maxZ],
        rowKey: `${Math.round(front.dirX * 8)}_${Math.round(front.dirZ * 8)}_${Math.round(
          (cx * -uz + cz * ux) / 24
        )}`,
        along: cx * ux + cz * uz,
      });
    }
  }

  // Rhythm pass. SF rows never repeat the same house twice in a row, and two
  // neighbours are never the same colour, so walk each row along the kerb and
  // nudge whatever collides onto its next-best variant.
  for (const p of placements) {
    let row = rows.get(p.rowKey);
    if (!row) rows.set(p.rowKey, (row = []));
    row.push(p);
  }
  for (const row of rows.values()) {
    row.sort((a, b) => a.along - b.along);
    for (let i = 1; i < row.length; i++) {
      const prev = row[i - 1];
      const here = row[i];
      if (here.list[here.choice].piece.i === prev.list[prev.choice].piece.i) {
        for (let alt = 1; alt < Math.min(6, here.list.length); alt++) {
          if (here.list[alt].piece.i === prev.list[prev.choice].piece.i) continue;
          here.choice = alt;
          break;
        }
      }
      if (here.tint === prev.tint) here.tint = (here.tint + 1 + (here.hash % 3)) % KIT_TINTS.length;
    }
  }

  const instances = new Float32Array(placements.length * KIT_STRIDE);
  const used = new Set();
  let at = 0;
  for (const p of placements) {
    const piece = p.list[p.choice].piece;
    const ds = Math.max(1, Math.min(1.2, p.depth / piece.dy));
    instances[at] = piece.i;
    // World space: the batch is one object for the whole city, not per chunk.
    instances[at + 1] = p.frontX + originX;
    instances[at + 2] = p.base;
    instances[at + 3] = p.frontZ + originZ;
    instances[at + 4] = p.yaw;
    instances[at + 5] = ds;
    instances[at + 6] = p.tint;
    instances[at + 7] = p.hash % 1024;
    at += KIT_STRIDE;
    used.add(piece.i);
    filled[p.blob][p.record] = 1;
    boxes.push(p.box[0], p.box[1], p.box[2], p.box[3]);
  }

  return {
    instances,
    used: [...used],
    filled,
    boxes: new Float32Array(boxes),
    considered,
    placed: placements.length,
  };
}

// Re-exported for the offline report, which parses tiles straight off disk.
export { readBuildings };
