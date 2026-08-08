// Bakes the two bespoke bridges from their real OSM centrelines instead of
// hand-picked coordinates: deck node lists with an elevation profile that meets
// the land (or the viaduct) at both abutments, tower positions derived from the
// published main-span lengths, and the east-span column line.
//
// Inputs : data/osm_structures.json, out/terrain.bin
// Outputs: out/bridges.json (merged into manifest.json by validate.mjs)

import { readFile, writeFile } from 'node:fs/promises';
import { project, unproject } from './lib/geo.mjs';
import { densify } from './lib/poly.mjs';
import { loadHeightmap } from './lib/heightmap.mjs';
import { deckHeightForLayer, loadStructures } from './lib/structures.mjs';

const OUT = new URL('./out/', import.meta.url);
const DATA = new URL('./data/', import.meta.url);

const { sampleElevation } = await loadHeightmap();
const structures = await loadStructures();

// Published clearances above mean high water at midspan.
const GOLDEN_GATE_CLEARANCE = 67;
const BAY_WEST_CLEARANCE = 67;
const BAY_EAST_CLEARANCE = 57;
const TOWER_CORRIDOR = 120;
const APPROACH_SNAP = 25;

// DataSF freeway/ramp centrelines near the abutments. OSM and DataSF digitise
// the same roadway a few metres apart, so the deck is extended onto the DataSF
// line the app actually bakes as the approach ribbon.
const APPROACH_CLASSES = new Set([1, 2]); // DataSF classcode: freeway, major
const approaches = [];
for (const f of JSON.parse(await readFile(new URL('streets_datasf.geojson', DATA), 'utf8')).features) {
  const code = parseInt(f.properties?.classcode, 10);
  if (!APPROACH_CLASSES.has(code) || f.properties?.date_dropped) continue;
  const geom = f.geometry;
  if (!geom) continue;
  const lines = geom.type === 'LineString' ? [geom.coordinates] : geom.coordinates || [];
  for (const coords of lines) {
    if (!coords || coords.length < 2) continue;
    approaches.push(coords.map(([lon, lat]) => project(lon, lat)));
  }
}

// Projected and resampled every ~40 m so the deck arch is smooth even where OSM
// only stores the span endpoints.
function toMeters(lonLat) {
  const flat = [];
  for (const [lon, lat] of lonLat) {
    const [x, z] = project(lon, lat);
    flat.push(x, z);
  }
  const dense = densify(flat, 40);
  const pts = [];
  for (let i = 0; i < dense.length; i += 2) pts.push([dense[i], dense[i + 1]]);
  return pts;
}

function arcLengths(pts) {
  const s = [0];
  for (let i = 1; i < pts.length; i++) s.push(s[i - 1] + Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]));
  return s;
}

function pointAt(pts, s, target) {
  for (let i = 1; i < pts.length; i++) {
    if (s[i] < target) continue;
    const t = (target - s[i - 1]) / (s[i] - s[i - 1] || 1);
    return [pts[i - 1][0] + (pts[i][0] - pts[i - 1][0]) * t, pts[i - 1][1] + (pts[i][1] - pts[i - 1][1]) * t];
  }
  return pts[pts.length - 1];
}

// Deck height at an abutment: whatever the road just past the end of the bridge
// is riding on. At grade it meets the ground; on a viaduct it stays up there.
function abutmentHeight(pts, endIndex, inwardIndex) {
  const [ex, ez] = pts[endIndex];
  const [ix, iz] = pts[inwardIndex];
  const len = Math.hypot(ex - ix, ez - iz) || 1;
  const ax = ex + ((ex - ix) / len) * 60;
  const az = ez + ((ez - iz) / len) * 60;
  const layer = structures.elevatedLayer(ax, az, 45);
  const ground = Math.max(0, sampleElevation(ex, ez));
  return layer ? ground + deckHeightForLayer(layer) : ground + 0.6;
}

// Deck profile: linear between the two abutment heights plus a sine arch so
// midspan lands on the published clearance.
function deckProfile(pts, clearance) {
  const s = arcLengths(pts);
  const total = s[s.length - 1] || 1;
  const yStart = abutmentHeight(pts, 0, 1);
  const yEnd = abutmentHeight(pts, pts.length - 1, pts.length - 2);
  const arch = Math.max(0, clearance - (yStart + yEnd) / 2);
  return pts.map((p, i) => {
    const t = s[i] / total;
    const y = yStart + (yEnd - yStart) * t + Math.sin(Math.PI * t) * arch;
    return [p[0], y, p[1]];
  });
}

// Nearest point on any approach centreline, if one is close enough to be the
// road this abutment is supposed to hand over to.
function approachFoot(x, z) {
  let best = null;
  for (const pts of approaches) {
    for (let i = 1; i < pts.length; i++) {
      const [ax, az] = pts[i - 1];
      const [bx, bz] = pts[i];
      const dx = bx - ax;
      const dz = bz - az;
      const l2 = dx * dx + dz * dz || 1;
      const t = Math.min(1, Math.max(0, ((x - ax) * dx + (z - az) * dz) / l2));
      const fx = ax + dx * t;
      const fz = az + dz * t;
      const d = Math.hypot(x - fx, z - fz);
      if (d < APPROACH_SNAP && (!best || d < best.d)) best = { d, x: fx, z: fz };
    }
  }
  return best;
}

// Extend both ends of the deck onto their approach centreline so the deck and
// the baked street ribbon actually touch.
function meetApproaches(nodes) {
  const out = nodes.slice();
  const head = approachFoot(out[0][0], out[0][2]);
  if (head && head.d > 0.5) out.unshift([head.x, out[0][1], head.z]);
  const tail = approachFoot(out[out.length - 1][0], out[out.length - 1][2]);
  if (tail && tail.d > 0.5) out.push([tail.x, out[out.length - 1][1], tail.z]);
  return out;
}

function toLonLatNodes(nodes) {
  return nodes.map(([x, y, z]) => {
    const [lon, lat] = unproject(x, z);
    return [+lon.toFixed(6), +lat.toFixed(6), +y.toFixed(2)];
  });
}

function distanceToPolyline(pts, x, z) {
  let best = Infinity;
  for (let i = 1; i < pts.length; i++) {
    const [ax, az] = pts[i - 1];
    const [bx, bz] = pts[i];
    const dx = bx - ax;
    const dz = bz - az;
    const l2 = dx * dx + dz * dz || 1;
    const t = Math.min(1, Math.max(0, ((x - ax) * dx + (z - az) * dz) / l2));
    best = Math.min(best, Math.hypot(x - (ax + dx * t), z - (az + dz * t)));
  }
  return best;
}

// The real towers, straight out of OSM: whichever mapped bridge towers sit on
// this centreline, ordered along the deck.
function towersOn(pts) {
  const s = arcLengths(pts);
  const picked = structures.towers
    .filter((t) => distanceToPolyline(pts, t.x, t.z) < TOWER_CORRIDOR)
    .map((t) => {
      let bestS = 0;
      let bestD = Infinity;
      for (let i = 0; i < pts.length; i++) {
        const d = Math.hypot(pts[i][0] - t.x, pts[i][1] - t.z);
        if (d < bestD) {
          bestD = d;
          bestS = s[i];
        }
      }
      const [lon, lat] = unproject(t.x, t.z);
      return { at: [+lon.toFixed(6), +lat.toFixed(6)], height: Math.round(t.height), s: bestS };
    })
    .sort((a, b) => a.s - b.s);
  return picked;
}

// ----------------------------------------------------------- Golden Gate ----
if (structures.goldenGate.length < 4) throw new Error('no Golden Gate centreline in osm_structures.json');
const ggPts = toMeters(structures.goldenGate);
const ggNodes = meetApproaches(deckProfile(ggPts, GOLDEN_GATE_CLEARANCE));
const ggTowers = towersOn(ggPts);
if (ggTowers.length !== 2) throw new Error(`expected 2 Golden Gate towers in OSM, found ${ggTowers.length}`);
const goldenGate = {
  nodes: toLonLatNodes(ggNodes),
  towers: ggTowers.map((t) => t.at),
  towerHeight: Math.max(227, ...ggTowers.map((t) => t.height)),
  deckWidth: 27,
  sag: 120,
};

// -------------------------------------------------------------- Bay Bridge --
if (structures.bayWest.length < 2 || structures.bayEast.length < 2) throw new Error('no Bay Bridge centreline in osm_structures.json');
const westPts = toMeters(structures.bayWest);
const eastPts = toMeters(structures.bayEast);
const westNodes = meetApproaches(deckProfile(westPts, BAY_WEST_CLEARANCE));
const eastNodes = meetApproaches(deckProfile(eastPts, BAY_EAST_CLEARANCE));
const bayTowers = towersOn(westPts);
if (bayTowers.length < 2) throw new Error(`expected Bay Bridge west-span towers in OSM, found ${bayTowers.length}`);
const eastMid = eastNodes[Math.floor(eastNodes.length / 2)];
const bayBridge = {
  nodes: toLonLatNodes(westNodes),
  towers: bayTowers.map((t) => t.at),
  towerHeight: Math.max(160, ...bayTowers.map((t) => t.height)),
  deckWidth: 24,
  sag: 78,
  east: {
    nodes: toLonLatNodes(eastNodes),
    tower: toLonLatNodes([eastMid])[0].slice(0, 2),
    towerHeight: 160,
    deckWidth: 28,
  },
  portal: toLonLatNodes([eastNodes[0]])[0],
};

const bridges = { goldenGateBridge: goldenGate, bayBridge };
await writeFile(new URL('bridges.json', OUT), JSON.stringify(bridges, null, 1));

const ggEnds = `${goldenGate.nodes[0][2]} m -> ${goldenGate.nodes[goldenGate.nodes.length - 1][2]} m`;
const bayEnds = `${bayBridge.nodes[0][2]} m -> ${bayBridge.nodes[bayBridge.nodes.length - 1][2]} m`;
console.log(`Golden Gate: ${goldenGate.nodes.length} deck nodes, abutments ${ggEnds}, ${goldenGate.towers.length} OSM towers ${JSON.stringify(goldenGate.towers)} at ${goldenGate.towerHeight} m`);
console.log(`Bay Bridge west: ${bayBridge.nodes.length} nodes, abutments ${bayEnds}, ${bayBridge.towers.length} OSM towers at ${bayBridge.towerHeight} m; east span ${bayBridge.east.nodes.length} nodes`);
