// Where the street kit stands. Pure geometry, no three.js: the tile worker runs
// this over the street polylines it has already parsed for a ground group, and
// hands the main thread a flat anchor list.
//
// Every decision comes from data that is already streamed — the baked street
// centrelines and classes, the sidewalk ribbons layer 1 bakes (which is also
// the authority on where a sidewalk exists at all: none over a bridge deck,
// none on a freeway), plus two small hint arrays the main thread derives from
// the context layer (Market Street's centreline, commercial front doors) and
// the landmark exclusion discs.
//
// Placement is a pure function of world position, so a cell laid out on one
// load is laid out identically on the next, whatever order it streamed in.

export const PIECES = [
  'sl_standard',
  'sl_pathofgold',
  'sl_residential',
  'traffic_signal',
  'hydrant',
  'mailbox',
  'muni_shelter',
  'bench',
  'trashcan',
  'newsboxes',
  'planter',
  'bikerack',
  'cafe_set',
  'market_stall',
  'parklet',
];
const P = Object.fromEntries(PIECES.map((id, i) => [id, i]));

export const ANCHOR_STRIDE = 5; // piece, x, y, z, yaw

const LAMP_SPACING = 40;
const LAMP_INSET = 0.8; // from the kerb edge, per plan §2.2
const SHELTER_SPACING = 250;
const NODE_CLEAR = 9; // keep furniture off the corner itself
// Mirrors the bake (pipeline/lib/streetscape.mjs): a zebra band starts this far
// past the intersection box and runs this far up the approach. The planner has
// no access to the baked markings, so it reconstructs where they landed and
// treats the painted rectangle as ground no piece may stand on.
const ZEBRA_SETBACK = 1.2;
const ZEBRA_BAND = 5 * 0.8 + 4 * 0.9;
const CROSSING_REACH = 30; // beyond this no zebra can reach, whatever the class
const SIDEWALK_PROOF = 5; // a baked sidewalk vertex must be this close
const CLUSTER_STEP = 20;
const CLUSTER_SPAN = 40; // ≤2 special pieces per 40 m of frontage
const MARKET_REACH = 22;
const COMMERCIAL_REACH = 32;

// Deterministic and position-based: the same metre of street hashes the same
// way in every session, on every machine, regardless of streaming order.
function hash(x, z, salt) {
  let h = Math.imul(Math.round(x * 4) | 0, 374761393);
  h = (h + Math.imul(Math.round(z * 4) | 0, 668265263)) | 0;
  h = (h + Math.imul(salt, 2246822519)) | 0;
  h = Math.imul(h ^ (h >>> 13), 1274126177);
  return ((h ^ (h >>> 16)) >>> 0) / 4294967296;
}

function grid(cell) {
  const map = new Map();
  return {
    add(x, z, value) {
      const key = `${Math.floor(x / cell)}_${Math.floor(z / cell)}`;
      const bucket = map.get(key);
      if (bucket) bucket.push(value);
      else map.set(key, [value]);
    },
    near(x, z, radius, visit) {
      const reach = Math.ceil(radius / cell);
      const gx = Math.floor(x / cell);
      const gz = Math.floor(z / cell);
      for (let dz = -reach; dz <= reach; dz++) {
        for (let dx = -reach; dx <= reach; dx++) {
          const bucket = map.get(`${gx + dx}_${gz + dz}`);
          if (!bucket) continue;
          for (const value of bucket) if (visit(value)) return true;
        }
      }
      return false;
    },
  };
}

function segmentDistance(x, z, ax, az, bx, bz) {
  const dx = bx - ax;
  const dz = bz - az;
  const l2 = dx * dx + dz * dz || 1;
  const t = Math.max(0, Math.min(1, ((x - ax) * dx + (z - az) * dz) / l2));
  return Math.hypot(x - (ax + dx * t), z - (az + dz * t));
}

// Walks a polyline at a fixed spacing, reporting position, elevation and unit
// tangent. Vertices are not resampled onto a curve: streets are dense enough
// that linear interpolation between them is the road.
function walk(line, spacing, phase, visit) {
  const { px, py, pz, n } = line;
  let target = phase;
  let arc = 0;
  for (let k = 1; k < n; k++) {
    const dx = px[k] - px[k - 1];
    const dz = pz[k] - pz[k - 1];
    const len = Math.hypot(dx, dz);
    if (len < 1e-4) continue;
    while (target <= arc + len) {
      const t = (target - arc) / len;
      visit(
        px[k - 1] + dx * t,
        py[k - 1] + (py[k] - py[k - 1]) * t,
        pz[k - 1] + dz * t,
        dx / len,
        dz / len,
        target
      );
      target += spacing;
    }
    arc += len;
  }
  return arc;
}

function lineLength(line) {
  let arc = 0;
  for (let k = 1; k < line.n; k++) {
    arc += Math.hypot(line.px[k] - line.px[k - 1], line.pz[k] - line.pz[k - 1]);
  }
  return arc;
}

// Intersection nodes from shared endpoints, mirroring the bake's rule: two arms
// that leave in opposite directions are one street crossing a cell boundary,
// not a junction.
export function junctionNodes(roads) {
  const buckets = new Map();
  const nodes = [];
  const at = (x, z) => {
    const gx = Math.floor(x / 4);
    const gz = Math.floor(z / 4);
    for (let dz = -1; dz <= 1; dz++) {
      for (let dx = -1; dx <= 1; dx++) {
        for (const node of buckets.get(`${gx + dx}_${gz + dz}`) || []) {
          if (Math.hypot(node.x - x, node.z - z) <= 1.5) return node;
        }
      }
    }
    const node = { x, z, arms: [], boxHalf: 0 };
    nodes.push(node);
    const key = `${gx}_${gz}`;
    if (!buckets.has(key)) buckets.set(key, []);
    buckets.get(key).push(node);
    return node;
  };

  for (const line of roads) {
    const { px, pz, n } = line;
    for (const fromStart of [true, false]) {
      const e = fromStart ? 0 : n - 1;
      const i = fromStart ? Math.min(n - 1, 3) : Math.max(0, n - 4);
      const dx = px[i] - px[e];
      const dz = pz[i] - pz[e];
      const len = Math.hypot(dx, dz);
      if (len < 1e-3) continue;
      const node = at(px[e], pz[e]);
      node.arms.push({ line, dirX: dx / len, dirZ: dz / len });
      node.boxHalf = Math.max(node.boxHalf, (line.width || 0) / 2);
    }
  }

  return nodes.filter((node) => {
    for (let i = 0; i < node.arms.length; i++) {
      for (let j = i + 1; j < node.arms.length; j++) {
        const dot = node.arms[i].dirX * node.arms[j].dirX + node.arms[i].dirZ * node.arms[j].dirZ;
        if (Math.abs(dot) < 0.9) return true;
      }
    }
    return false;
  });
}

/**
 * Plans the furniture for one ground group.
 *
 * @param {object} job
 * @param {Array} job.roads      road centrelines: {px, py, pz, n, klass, width, sidewalk}
 * @param {Array} job.sidewalks  baked sidewalk ribbon centrelines: {px, py, pz, n}
 * @param {Array} job.haloRoads  centrelines from the ring of cells around the
 *   group, used only to complete junctions that straddle its edge — nothing is
 *   ever placed along them
 * @param {Array} job.bounds     [minX, minZ, maxX, maxZ] this group owns
 * @param {Float32Array} job.market      Market St segments [x0,z0,x1,z1,…]
 * @param {Float32Array} job.commercial  shopfront points [x,z,…]
 * @param {Float32Array} job.exclusions  landmark discs [x,z,r,…]
 * @param {number} job.limit     hard cap on anchors for this group
 * @returns {Float32Array} anchors, ANCHOR_STRIDE floats each
 */
export function planStreetFurniture(job) {
  const {
    roads,
    sidewalks,
    haloRoads = [],
    bounds = null,
    market,
    commercial,
    exclusions,
    limit = 4000,
  } = job;
  // A junction is only whole once every arm is in hand, and a group's blobs stop
  // at its edge: without the neighbours' centrelines a crossing on the seam
  // looks like a dead end, and the crosswalk box it should have protected goes
  // unguarded. The halo is for reading junctions only — see `owns` below.
  const owns = (x, z) =>
    !bounds || (x >= bounds[0] && x < bounds[2] && z >= bounds[1] && z < bounds[3]);
  const out = [];

  // Layer 1 is the authority on where a sidewalk exists: a road whose ribbon was
  // suppressed (bridge deck, freeway, water) simply has no proof points, so
  // nothing can stand beside it.
  const proof = grid(16);
  for (const line of sidewalks) {
    for (let k = 0; k < line.n; k++) proof.add(line.px[k], line.pz[k], k * 4 + (line.id | 0));
  }
  const sidewalkPoints = [];
  for (const line of sidewalks) {
    for (let k = 0; k < line.n; k++) sidewalkPoints.push(line.px[k], line.pz[k]);
  }
  const paved = grid(16);
  for (let i = 0; i < sidewalkPoints.length; i += 2) paved.add(sidewalkPoints[i], sidewalkPoints[i + 1], i);
  const onSidewalk = (x, z) =>
    paved.near(x, z, SIDEWALK_PROOF, (i) =>
      Math.hypot(sidewalkPoints[i] - x, sidewalkPoints[i + 1] - z) <= SIDEWALK_PROOF
    );

  const shops = grid(32);
  for (let i = 0; i < commercial.length; i += 2) shops.add(commercial[i], commercial[i + 1], i);
  const shopScore = (x, z) => {
    let hits = 0;
    shops.near(x, z, COMMERCIAL_REACH, (i) => {
      if (Math.hypot(commercial[i] - x, commercial[i + 1] - z) <= COMMERCIAL_REACH) hits++;
      return false;
    });
    return hits;
  };

  const marketGrid = grid(64);
  for (let i = 0; i < market.length; i += 4) marketGrid.add((market[i] + market[i + 2]) / 2, (market[i + 1] + market[i + 3]) / 2, i);
  const onMarket = (x, z) =>
    marketGrid.near(x, z, MARKET_REACH + 60, (i) =>
      segmentDistance(x, z, market[i], market[i + 1], market[i + 2], market[i + 3]) <= MARKET_REACH
    );

  const excluded = (x, z) => {
    for (let i = 0; i < exclusions.length; i += 3) {
      const dx = x - exclusions[i];
      const dz = z - exclusions[i + 1];
      if (dx * dx + dz * dz < exclusions[i + 2] * exclusions[i + 2]) return true;
    }
    return false;
  };

  const nodes = junctionNodes(haloRoads.length ? roads.concat(haloRoads) : roads);
  const nodeGrid = grid(32);
  for (const node of nodes) nodeGrid.add(node.x, node.z, node);
  const nearNode = (x, z, radius) =>
    nodeGrid.near(x, z, radius, (node) => Math.hypot(node.x - x, node.z - z) <= radius);

  // Inside the intersection box, or inside the painted band of one of its
  // crossings. The band is a rectangle across the roadway, so a piece standing
  // on the footway beside it is clear and a piece in the parking lane is not.
  const onCrossing = (x, z) =>
    nodeGrid.near(x, z, CROSSING_REACH, (node) => {
      const dx = x - node.x;
      const dz = z - node.z;
      const near = node.boxHalf + ZEBRA_SETBACK;
      if (dx * dx + dz * dz <= near * near) return true;
      for (const arm of node.arms) {
        const along = dx * arm.dirX + dz * arm.dirZ;
        if (along < near || along > near + ZEBRA_BAND) continue;
        const across = Math.abs(dx * arm.dirZ - dz * arm.dirX);
        if (across <= arm.line.width / 2) return true;
      }
      return false;
    });

  // Everything funnels through here, so one rule set covers every piece: on a
  // real sidewalk, clear of the crosswalk box, clear of the landmarks.
  function place(
    piece,
    x,
    y,
    z,
    yaw,
    { needSidewalk = true, clear = NODE_CLEAR, crossing = true } = {}
  ) {
    if (out.length / ANCHOR_STRIDE >= limit) return false;
    if (needSidewalk && !onSidewalk(x, z)) return false;
    if (clear > 0 && nearNode(x, z, clear)) return false;
    if (crossing && onCrossing(x, z)) return false;
    if (excluded(x, z)) return false;
    out.push(piece, x, y, z, yaw);
    return true;
  }

  // A piece's front is -Y in Blender, which the yup export turns into +Z here,
  // so yaw is the angle that swings +Z onto the facing direction.
  const facing = (fx, fz) => Math.atan2(fx, fz);

  // ----------------------------------------------------------- signals ---
  // Signals go down before anything else: they carry meaning (this crossing is
  // controlled), so if a dense group runs into its instance cap it should lose
  // a trash can, not a signal head.
  // Both crossing streets have to be arterial or better, one head per corner,
  // each facing the traffic it stops.
  for (const node of nodes) {
    // Seam junctions are read by both groups but owned by one, so a signalled
    // crossing gets one set of heads rather than two stacked sets.
    if (!owns(node.x, node.z)) continue;
    const arms = [];
    for (const arm of node.arms) {
      if (arm.line.klass > 2 || !arm.line.sidewalk) continue;
      if (arms.some((a) => Math.abs(a.dirX * arm.dirX + a.dirZ * arm.dirZ) > 0.9)) continue;
      arms.push(arm);
    }
    if (arms.length < 2) continue;
    const [a, b] = arms;
    const alongA = b.line.width / 2 + 2.2;
    const alongB = a.line.width / 2 + 2.2;
    let heads = 0;
    for (const sa of [1, -1]) {
      for (const sb of [1, -1]) {
        if (heads >= 4) break;
        const x = node.x + a.dirX * alongA * sa + b.dirX * alongB * sb;
        const z = node.z + a.dirZ * alongA * sa + b.dirZ * alongB * sb;
        const y = nodeElevation(node) + (a.line.sidewalk ? a.line.sidewalk.curb : 0);
        // A signal head belongs on the corner it controls: the crossing test is
        // the one rule it is exempt from.
        const opts = { clear: 0, crossing: false };
        if (place(P.traffic_signal, x, y, z, facing(-a.dirX * sa, -a.dirZ * sa), opts)) heads++;
      }
    }
  }

  // ------------------------------------------------------------- lamps ---
  for (const road of roads) {
    const sw = road.sidewalk;
    if (!sw) continue;
    const halfW = road.width / 2;
    const reach = halfW + Math.min(LAMP_INSET, sw.width * 0.3);
    const total = lineLength(road);
    if (total < 12) continue;
    const phase = 6 + hash(road.px[0], road.pz[0], 11) * LAMP_SPACING;
    let step = 0;
    walk(road, LAMP_SPACING, phase, (x, y, z, tx, tz) => {
      const side = step++ % 2 === 0 ? 1 : -1;
      const nx = tz * side;
      const nz = -tx * side;
      const lx = x + nx * reach;
      const lz = z + nz * reach;
      const piece = onMarket(lx, lz)
        ? P.sl_pathofgold
        : road.klass === 4
          ? P.sl_residential
          : P.sl_standard;
      place(piece, lx, y + sw.curb, lz, facing(-nx, -nz));
    });
  }

  // Then the pieces that carry meaning: hydrants, shelters and the shopfront
  // clusters. The lamp rhythm is
  // what a viewer reads as "this street is finished", so it is laid down for
  // every road before any street gets its clutter.
  for (const road of roads) {
    const sw = road.sidewalk;
    if (!sw) continue;
    const halfW = road.width / 2;
    const total = lineLength(road);
    if (total < 12) continue;

    // ----------------------------------------------------- hydrants ---
    // About one per block face, near the corner where the real ones sit — SF
    // runs roughly a hydrant every other corner, not one per kerb.
    if (total >= 34 && hash(road.px[0], road.pz[0], 19) < 0.55) {
      const fromStart = hash(road.px[0], road.pz[0], 21) < 0.5;
      const arc = fromStart ? 13 : total - 13;
      let done = false;
      walk(road, total + 1, arc, (x, y, z, tx, tz) => {
        if (done) return;
        done = true;
        const side = hash(x, z, 23) < 0.5 ? 1 : -1;
        const nx = tz * side;
        const nz = -tx * side;
        const reachH = halfW + Math.min(0.9, sw.width * 0.32);
        place(P.hydrant, x + nx * reachH, y + sw.curb, z + nz * reachH, facing(-nx, -nz));
      });
    }

    // ------------------------------------------- shelters and mailboxes ---
    if (road.klass <= 2 && sw.width >= 4) {
      walk(road, SHELTER_SPACING, 60 + hash(road.px[0], road.pz[0], 31) * 80, (x, y, z, tx, tz) => {
        const side = hash(x, z, 37) < 0.5 ? 1 : -1;
        const nx = tz * side;
        const nz = -tx * side;
        // Centred on the footway so the shelter's back is off the shopfronts.
        const off = halfW + sw.width / 2;
        const sx = x + nx * off;
        const sz = z + nz * off;
        if (shopScore(sx, sz) >= 1 || hash(x, z, 41) < 0.45) {
          place(P.muni_shelter, sx, y + sw.curb, sz, facing(-nx, -nz), { clear: 16 });
        }
      });
    }

    // ------------------------------------------- commercial frontage ---
    // Clusters, not scatter: a stretch that scores as a shopping street gets a
    // small designed group, then 40 m of quiet before the next one.
    let cooldown = 0;
    walk(road, CLUSTER_STEP, 10 + hash(road.px[0], road.pz[0], 67) * CLUSTER_STEP, (x, y, z, tx, tz) => {
      if (cooldown > 0) {
        cooldown -= CLUSTER_STEP;
        return;
      }
      const side = hash(x, z, 71) < 0.5 ? 1 : -1;
      const nx = tz * side;
      const nz = -tx * side;
      const kerb = halfW;
      const front = kerb + Math.min(1.5, sw.width * 0.45);
      const cx = x + nx * front;
      const cz = z + nz * front;
      if (shopScore(cx, cz) < 3) return;
      const yaw = facing(-nx, -nz);
      const y0 = y + sw.curb;
      const roll = hash(x, z, 73);
      let placed = 0;
      if (roll < 0.34) {
        placed += place(P.cafe_set, cx + tx * 2.2, y0, cz + tz * 2.2, yaw) ? 1 : 0;
        placed += place(P.newsboxes, cx - tx * 3.4, y0, cz - tz * 3.4, yaw) ? 1 : 0;
      } else if (sw.width >= 4 && roll < 0.52) {
        placed += place(P.market_stall, cx, y0, cz, yaw) ? 1 : 0;
        placed += place(P.bikerack, cx - tx * 4.2, y0, cz - tz * 4.2, yaw) ? 1 : 0;
      } else if (roll < 0.68 && shopScore(cx, cz) >= 4) {
        placed += place(P.bikerack, cx, y0, cz, yaw) ? 1 : 0;
        placed += place(P.newsboxes, cx - tx * 3.2, y0, cz - tz * 3.2, yaw) ? 1 : 0;
      } else if (roll >= 0.74 && road.klass >= 3) {
        // A parklet takes the parking lane, which is why it sits at road level
        // just outside the kerb rather than on the footway.
        const deck = kerb - 1.05;
        placed += place(P.parklet, x + nx * deck, y, z + nz * deck, yaw, {
          needSidewalk: false,
          clear: 14,
        })
          ? 1
          : 0;
      }
      if (placed) cooldown = CLUSTER_SPAN + (placed > 1 ? CLUSTER_SPAN : 0);
    });
  }

  // Last, the everyday clutter. It is the least meaningful furniture on the
  // street, so it is also the first thing a group at its instance cap drops.
  for (const road of roads) {
    const sw = road.sidewalk;
    if (!sw) continue;
    const halfW = road.width / 2;
    if (lineLength(road) < 12) continue;

    // ------------------------------------- everyday street-corner pieces ---
    walk(road, 60, 22 + hash(road.px[0], road.pz[0], 53) * 40, (x, y, z, tx, tz) => {
      const roll = hash(x, z, 59);
      const side = hash(x, z, 61) < 0.5 ? 1 : -1;
      const nx = tz * side;
      const nz = -tx * side;
      const off = halfW + Math.min(1.0, sw.width * 0.34);
      const px = x + nx * off;
      const pz = z + nz * off;
      const yaw = facing(-nx, -nz);
      const y0 = y + sw.curb;
      if (roll < 0.26) place(P.trashcan, px, y0, pz, yaw);
      else if (roll < 0.36 && road.klass <= 3) place(P.mailbox, px, y0, pz, yaw);
      else if (roll < 0.5 && sw.width >= 4) {
        // Benches and planters read as a designed pair on the wide footways.
        const along = 1.6;
        place(P.bench, px + tx * along, y0, pz + tz * along, yaw);
        place(P.planter, px - tx * along, y0, pz - tz * along, yaw);
      }
    });

  }

  return new Float32Array(out);
}

// A node's elevation is the road surface at the endpoint that made it.
function nodeElevation(node) {
  const arm = node.arms[0];
  const { px, py, pz, n } = arm.line;
  return Math.hypot(px[0] - node.x, pz[0] - node.z) < Math.hypot(px[n - 1] - node.x, pz[n - 1] - node.z)
    ? py[0]
    : py[n - 1];
}
