// Streetscape geometry for the toy street bake: raised sidewalk plinths, the
// trimmed centrelines the runtime chops into dashes, and crosswalk zebras at
// intersection nodes. Everything here is a polyline in the existing street-blob
// format — the ribbon builder in the runtime turns it into geometry, so a
// sidewalk costs one line, not a mesh.

// A street riding a bespoke bridge deck gets no sidewalk: the deck brings its
// own edges, and a plinth draped on the corridor would hover over the bay.
export const DECK_CORRIDOR = 45;

export const NODE_SNAP = 1; // endpoints this close share a node
const STRAIGHT = 0.45; // rad; two arms this close to a straight line just continue
export const DASH_CLEARANCE = 8; // dashes stop this far short of a node
export const ZEBRA_BARS = 5;
export const ZEBRA_BAR = 0.8;
export const ZEBRA_GAP = 0.9;
export const ZEBRA_SETBACK = 1.2; // clear of the intersection box
export const ZEBRA_MAX_GRADE = 0.12; // bars shear on anything steeper

// --------------------------------------------------------------- polylines ---

// Cumulative arclength for a flat [x, y, z, ...] polyline.
function cumulative(pts) {
  const n = pts.length / 3;
  const acc = new Float64Array(n);
  for (let i = 1; i < n; i++) {
    acc[i] = acc[i - 1] + Math.hypot(pts[i * 3] - pts[(i - 1) * 3], pts[i * 3 + 2] - pts[(i - 1) * 3 + 2]);
  }
  return acc;
}

// Position, elevation and unit tangent at arclength `s`.
function sampleAt(pts, acc, s) {
  const n = acc.length;
  const clamped = Math.max(0, Math.min(acc[n - 1], s));
  let i = 1;
  while (i < n - 1 && acc[i] < clamped) i++;
  const span = acc[i] - acc[i - 1] || 1;
  const t = (clamped - acc[i - 1]) / span;
  const ax = pts[(i - 1) * 3];
  const ay = pts[(i - 1) * 3 + 1];
  const az = pts[(i - 1) * 3 + 2];
  const bx = pts[i * 3];
  const by = pts[i * 3 + 1];
  const bz = pts[i * 3 + 2];
  const dx = bx - ax;
  const dz = bz - az;
  const len = Math.hypot(dx, dz) || 1;
  return {
    x: ax + dx * t,
    y: ay + (by - ay) * t,
    z: az + dz * t,
    tx: dx / len,
    tz: dz / len,
  };
}

// Parallel offset of a street centreline. The tangent is averaged across each
// vertex so the offset mitres instead of gapping on a bend.
export function offsetLine(pts, offset) {
  const n = pts.length / 3;
  const out = { pts: [], y: [] };
  for (let k = 0; k < n; k++) {
    let tx;
    let tz;
    if (k === 0) {
      tx = pts[3] - pts[0];
      tz = pts[5] - pts[2];
    } else if (k === n - 1) {
      tx = pts[(n - 1) * 3] - pts[(n - 2) * 3];
      tz = pts[(n - 1) * 3 + 2] - pts[(n - 2) * 3 + 2];
    } else {
      tx = pts[(k + 1) * 3] - pts[(k - 1) * 3];
      tz = pts[(k + 1) * 3 + 2] - pts[(k - 1) * 3 + 2];
    }
    const tl = Math.hypot(tx, tz) || 1;
    out.pts.push(pts[k * 3] + (tz / tl) * offset, pts[k * 3 + 2] - (tx / tl) * offset);
    out.y.push(pts[k * 3 + 1]);
  }
  return out;
}

// Keep only the runs of a polyline whose points pass `keep`, so a sidewalk can
// stop at a bridge corridor and pick up again on the far side.
export function splitRuns(line, keep) {
  const runs = [];
  let current = null;
  for (let k = 0; k < line.y.length; k++) {
    if (keep(line.pts[k * 2], line.pts[k * 2 + 1])) {
      if (!current) runs.push((current = { pts: [], y: [] }));
      current.pts.push(line.pts[k * 2], line.pts[k * 2 + 1]);
      current.y.push(line.y[k]);
    } else {
      current = null;
    }
  }
  return runs.filter((r) => r.y.length >= 2);
}

// ------------------------------------------------------------------- decks ---

// Deck centrelines of the bespoke bridges, in the same shape streets.mjs uses.
export function deckCorridor(bridgeSpec, project) {
  const lines = [];
  for (const spec of Object.values(bridgeSpec)) {
    for (const nodes of [spec.nodes, spec.east?.nodes]) {
      if (!nodes) continue;
      lines.push(nodes.map(([lon, lat]) => project(lon, lat)));
    }
  }
  return (x, z) => {
    for (const line of lines) {
      for (let i = 1; i < line.length; i++) {
        const [ax, az] = line[i - 1];
        const [bx, bz] = line[i];
        const dx = bx - ax;
        const dz = bz - az;
        const l2 = dx * dx + dz * dz || 1;
        const t = Math.min(1, Math.max(0, ((x - ax) * dx + (z - az) * dz) / l2));
        if (Math.hypot(x - (ax + dx * t), z - (az + dz * t)) < DECK_CORRIDOR) return true;
      }
    }
    return false;
  };
}

// ------------------------------------------------------------------- nodes ---

// Intersection nodes: endpoints shared by street polylines within NODE_SNAP.
// Cell splitting duplicates a vertex on every cell boundary, so two arms that
// leave in opposite directions are a continuation, not a junction.
export function collectNodes(lines) {
  const buckets = new Map();
  const nodes = [];
  const bucketKey = (x, z) => `${Math.floor(x / 2)}_${Math.floor(z / 2)}`;

  const nodeAt = (x, z) => {
    for (let dx = -1; dx <= 1; dx++) {
      for (let dz = -1; dz <= 1; dz++) {
        const bucket = buckets.get(bucketKey(x + dx * 2, z + dz * 2));
        if (!bucket) continue;
        for (const node of bucket) {
          if (Math.hypot(node.x - x, node.z - z) <= NODE_SNAP) return node;
        }
      }
    }
    const node = { x, z, arms: [] };
    nodes.push(node);
    const key = bucketKey(x, z);
    if (!buckets.has(key)) buckets.set(key, []);
    buckets.get(key).push(node);
    return node;
  };

  for (const line of lines) {
    const n = line.pts.length / 3;
    if (n < 2) continue;
    const acc = cumulative(line.pts);
    if (acc[n - 1] < 2) continue;
    for (const fromStart of [true, false]) {
      const end = fromStart ? 0 : acc[n - 1];
      const inward = sampleAt(line.pts, acc, fromStart ? Math.min(5, acc[n - 1]) : Math.max(0, acc[n - 1] - 5));
      const px = fromStart ? line.pts[0] : line.pts[(n - 1) * 3];
      const pz = fromStart ? line.pts[2] : line.pts[(n - 1) * 3 + 2];
      const dx = inward.x - px;
      const dz = inward.z - pz;
      const len = Math.hypot(dx, dz) || 1;
      nodeAt(px, pz).arms.push({
        line,
        acc,
        fromStart,
        end,
        dirX: dx / len,
        dirZ: dz / len,
      });
    }
  }

  // An arm pair that is neither parallel (a duplicate) nor anti-parallel (the
  // same street continuing into the next cell) means streets actually cross.
  return nodes.filter((node) => {
    const { arms } = node;
    if (arms.length < 2) return false;
    for (let i = 0; i < arms.length; i++) {
      for (let j = i + 1; j < arms.length; j++) {
        const dot = arms[i].dirX * arms[j].dirX + arms[i].dirZ * arms[j].dirZ;
        const angle = Math.acos(Math.max(-1, Math.min(1, dot)));
        if (angle > STRAIGHT && angle < Math.PI - STRAIGHT) return true;
      }
    }
    return false;
  });
}

// Nodes hashed into a 20 m grid so the dash trimmer can ask "is there a
// junction near this dash" without scanning the city.
export function nodeIndex(nodes) {
  const grid = new Map();
  const key = (x, z) => `${Math.floor(x / 20)}_${Math.floor(z / 20)}`;
  for (const node of nodes) {
    const k = key(node.x, node.z);
    if (!grid.has(k)) grid.set(k, []);
    grid.get(k).push(node);
  }
  return (x, z, radius) => {
    const gx = Math.floor(x / 20);
    const gz = Math.floor(z / 20);
    const reach = Math.ceil(radius / 20);
    for (let dx = -reach; dx <= reach; dx++) {
      for (let dz = -reach; dz <= reach; dz++) {
        for (const node of grid.get(`${gx + dx}_${gz + dz}`) || []) {
          if (Math.hypot(node.x - x, node.z - z) <= radius) return true;
        }
      }
    }
    return false;
  };
}

// ------------------------------------------------------------------ dashes ---

// The centreline runs the runtime is allowed to dash: the whole street minus a
// DASH_CLEARANCE gap around every junction, so intersection boxes stay clean.
// The street's own vertices are reused — only the two ends of a gap are new
// points — so a dashed street costs about what its road ribbon costs.
export function dashRuns(line, nearNode) {
  const n = line.pts.length / 3;
  if (n < 2) return [];
  const acc = cumulative(line.pts);
  const total = acc[n - 1];
  if (total < DASH_CLEARANCE * 2 + 12) return [];

  const clear = new Array(n);
  for (let k = 0; k < n; k++) {
    clear[k] = !nearNode(line.pts[k * 3], line.pts[k * 3 + 2], DASH_CLEARANCE);
  }
  // Where the clearance boundary falls between two vertices, bisect for it so
  // the dash run stops at the gap rather than at the nearest vertex.
  const edge = (insideK, outsideK) => {
    let lo = acc[insideK];
    let hi = acc[outsideK];
    for (let i = 0; i < 5; i++) {
      const mid = (lo + hi) / 2;
      const p = sampleAt(line.pts, acc, mid);
      if (nearNode(p.x, p.z, DASH_CLEARANCE)) hi = mid;
      else lo = mid;
    }
    return sampleAt(line.pts, acc, lo);
  };

  const runs = [];
  let current = null;
  for (let k = 0; k < n; k++) {
    if (!clear[k]) {
      if (current) {
        const p = edge(k - 1, k);
        current.pts.push(p.x, p.z);
        current.y.push(p.y);
        current = null;
      }
      continue;
    }
    if (!current) {
      runs.push((current = { pts: [], y: [] }));
      if (k > 0) {
        const p = edge(k, k - 1);
        current.pts.push(p.x, p.z);
        current.y.push(p.y);
      }
    }
    current.pts.push(line.pts[k * 3], line.pts[k * 3 + 2]);
    current.y.push(line.pts[k * 3 + 1]);
  }
  // A run shorter than one dash cycle would only produce a stub.
  return runs.filter((r) => r.y.length >= 2 && runLength(r) > 12);
}

function runLength(run) {
  let len = 0;
  for (let k = 1; k < run.y.length; k++) {
    len += Math.hypot(run.pts[k * 2] - run.pts[(k - 1) * 2], run.pts[k * 2 + 1] - run.pts[(k - 1) * 2 + 1]);
  }
  return len;
}

// --------------------------------------------------------------- crosswalks ---

// One zebra band per approach: bars spanning the roadway, set back clear of the
// intersection box. Each bar is a two-point polyline across the street; the
// ribbon builder gives it its width.
export function crosswalkBars(node, widthOf) {
  const bars = [];
  let boxHalf = 0;
  for (const arm of node.arms) boxHalf = Math.max(boxHalf, widthOf(arm.line.klass) / 2);
  const seen = [];
  for (const arm of node.arms) {
    const halfW = widthOf(arm.line.klass) / 2;
    if (halfW <= 0) continue;
    // Two arms leaving along the same heading are duplicate centrelines; one
    // zebra between them is enough.
    if (seen.some((d) => d[0] * arm.dirX + d[1] * arm.dirZ > 0.98)) continue;
    seen.push([arm.dirX, arm.dirZ]);

    const total = arm.acc[arm.acc.length - 1];
    const start = boxHalf + ZEBRA_SETBACK;
    const band = ZEBRA_BARS * ZEBRA_BAR + (ZEBRA_BARS - 1) * ZEBRA_GAP;
    if (total < start + band) continue;
    const at = (s) => sampleAt(arm.line.pts, arm.acc, arm.fromStart ? s : total - s);

    const first = at(start);
    const last = at(start + band);
    if (Math.abs(last.y - first.y) / band > ZEBRA_MAX_GRADE) continue;

    for (let i = 0; i < ZEBRA_BARS; i++) {
      const s = start + i * (ZEBRA_BAR + ZEBRA_GAP) + ZEBRA_BAR / 2;
      const p = at(s);
      // Bars sit flat across the roadway, exactly like the road ribbon, so a
      // cross-slope cannot shear them apart.
      bars.push({
        pts: [p.x + p.tz * halfW, p.z - p.tx * halfW, p.x - p.tz * halfW, p.z + p.tx * halfW],
        y: [p.y, p.y],
        cx: p.x,
        cz: p.z,
      });
    }
  }
  return bars;
}
