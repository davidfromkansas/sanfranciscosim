// Live Muni buses.
//
// /api/muni serves the real SFMTA fleet decoded from 511's GTFS-Realtime
// feeds; every motor coach in service appears here as the hand-made
// muni-bus-40 GLB, following the EXACT street alignment of its trip — baked
// GTFS shapes in tiles/muni-shapes.bin, resolved trip -> shape — with the
// route number on a hovering badge and a click-through card. Spec and
// acceptance bar ("What the user sees"): MUNI-LIVE-PROMPT.md.
//
// The experience rules the mechanics here serve: buses drive continuously
// between the ~90 s fixes (project fix onto shape, glide along the polyline,
// never teleport), stopped means stopped (dwell easing, no creeping), and
// when data goes away the layer simply empties — procedural road traffic is
// untouched either way, so there is no fallback hand-off to manage.
//
// Draw calls: 5 instanced body + 5 glow + 1 badge + 1 route glow wall = 12.

import {
  BufferAttribute,
  BufferGeometry,
  CanvasTexture,
  Color,
  DynamicDrawUsage,
  InstancedBufferAttribute,
  InstancedMesh,
  Mesh,
  MeshBasicMaterial,
  MeshLambertMaterial,
  Object3D,
  PlaneGeometry,
  SRGBColorSpace,
} from 'three';
import { mergeGeometries } from 'three/addons/utils/BufferGeometryUtils.js';

import { createGLTFLoader } from './gltf.js';
import { shared } from './env.js';
// Whether a vehicle is moving, dwelling, or has no business being in the scene
// is decided in muni-motion.js: pure, tested rules. Read its header before
// touching anything below that calls into it — every one of those rules is a
// bug this city has already shipped, and app/test/muni-motion.test.mjs keeps
// them fixed.
import {
  DWELL_STEP_M,
  PROVISIONAL_LEAD_M,
  STALE_MS,
  deadReckonAdvance,
  dormantReason,
  seedSpeed,
  shouldDrop,
  targetSpeedFor,
} from './muni-motion.js';

const MANIFEST = `${import.meta.env.BASE_URL}sf-assets/vehicles_manifest.json`;
const SHAPES_URL = `${import.meta.env.BASE_URL}tiles/muni-shapes.bin`;
const SHAPES_MAGIC = 0x4d554e31; // 'MUN1'

const CAPACITY = 512;
const POLL_MS = 60 * 1000;
const POLL_JITTER_MS = 5 * 1000;
const DEMO_POLL_MS = 20 * 1000;

// The street fleet renders at 1.6x (agents.js carScale); the live buses must
// match it or they read as toys among toys.
const CAR_SCALE = 1.6;

// Rendering-side motion tuning (the rules that decide moving vs dwelling live
// in muni-motion.js; these only shape how that decision is animated).
const DECEL = 3.2; // m/s^2 easing into a stop (~2 s from cruise)
const ACCEL = 1.4; // m/s^2 pulling away
const CATCHUP_FACTOR = 1.3; // max overspeed while closing a gap to the fix
const SNAP_LIMIT_M = 150; // a fix further than this off-shape -> dead-reckon
const SNAP_WINDOW_M = 1200; // how far along the shape a projection may jump
const HEADING_EASE = 2.4; // rad/s toward the tangent
// Seconds a vehicle takes to sink out of / rise back into the scene, so a
// service change reads as arriving or leaving rather than as popping.
const HIDE_FADE_S = 1.2;
// Overshoot past a fresh fix that is held rather than reversed: dead reckoning
// and the provisional guess both run ahead of the data, and yanking a bus
// backwards is a visible teleport. Beyond this the guess was wrong -> snap.
const OVERSHOOT_HOLD_M = 150;

// Badges: cream route pills over each roof, one instanced quad layer fed by a
// lazily-grown canvas atlas (a draw call per route would be ~40 calls).
// Speech-bubble callouts, the idiom of the isometric city-builder the look is
// borrowed from: a cream bubble with a tail pointing down at the roof, so a
// glance from the locked 42 deg camera reads "that vehicle is saying 38R".
// Square atlas cells (bubble in the top ~2/3, tail below) at 8x8 = 64 slots;
// only motor coaches are drawn and Muni runs ~44 of those, so 64 is headroom.
const BADGE_COLS = 8;
const BADGE_ROWS = 8;
const BADGE_W = 7.2; // metres, square quad: the tail needs vertical room
const BADGE_H = 7.2;
// Where the TAIL TIP goes: just above the 5.5 m roof (3.42 m body x 1.6
// carScale). The quad centre is derived from it, not fixed, because the bubble
// grows with distance and its tail grows with it — see BADGE_TAIL_DROP.
const BADGE_TIP_Y = 6.0;
// How far the tail tip hangs below the quad centre, at scale 1. The centre is
// therefore BADGE_TIP_Y + BADGE_TAIL_DROP * scale, which at scale 1 is the 8.6 m
// this used to be pinned at.
//
// Scaling the WHOLE height by the zoom scale (the old `8.6 * scale`) is what
// detached a badge from its bus: measured on the deployed build, a bus 8.4 km
// out was 4 px wide with its bubble 150 px above it, on an 845 px viewport. The
// bubble has to scale — that is what keeps it legible from the hero view — but
// the tip it points with does not, so only the tail's own growth belongs here.
const BADGE_TAIL_DROP = 0.36 * BADGE_H;
// Badges follow the ZOOM, not a fixed distance in metres. A radius tuned for
// street level shows nothing from the air, which is where this camera spends
// most of its time; one tuned for the air carpets the Mission at street level.
// So the working radius is derived from the camera's height each frame and the
// bubbles are scaled to hold a roughly constant SIZE ON SCREEN — a bubble a
// kilometre away is drawn a kilometre-sized, which is what makes them legible
// from up high. Density is then bounded by MAX_BADGES, not by the radius.
const BADGE_RADIUS_MIN = 300;
// Reaches the far side of the city from the hero view. The camera tops out at
// 8000 m of orbit (~5350 m of height) where the visible ground spans roughly
// 15 km, so a 2600 m cap left the whole skyline unlabelled — MAX_BADGES is what
// bounds clutter, not the radius, so the radius may as well cover what is on
// screen. Desktop expanded 200% (3x) to match mobile so tags show at the hero
// view on load; both platforms use the same values now.
const BADGE_RADIUS_MAX = 33000;
const BADGE_RADIUS_PER_M = 6.6;
// Camera distance at which a bubble is drawn at its authored size; scale is
// proportional to distance either side of it, so screen size stays put.
const BADGE_REF_DIST = 420;
const BADGE_SCALE_MIN = 0.85;
// Room to stay legible all the way out to the hero view: at 8000 m a bubble
// needs ~19x its authored size to hold the same size on screen. Capping this
// at 9 was the second reason the high view looked empty — the bubbles were
// there, drawn at half the size they needed, i.e. a few pixels.
const BADGE_SCALE_MAX = 26;
// Hard ceiling on how many shout at once, whatever the radius. Raised from 18
// to 512 so the hero view on load shows tags across the whole city — every
// vehicle within the zoom radius gets a badge, not just a cluster near the
// center. Matches the InstancedMesh cap (CAPACITY).
const MAX_BADGES = 512;

// ------------------------------------------------------------------ subway

// Muni Metro spends most of each route in tunnel, and a GTFS shape is one
// polyline from terminal to terminal with nothing marking what is underground.
// Drawn on the surface like a bus, an LRV therefore climbs over Buena Vista
// Heights and through the houses on it instead of running under them — 38% of
// the N is tunnel, 64% of the L.
//
// These are the portals where Metro reaches daylight; the stretch between a
// pair is underground. Resolved against each shape's own polyline on first use
// (rather than baked as arc lengths) so a re-bake or a reroute can't leave a
// stale range behind: a portal that no longer sits on the shape is dropped and
// that stretch simply draws, which is the old behaviour.
const PORTAL = {
  embarcadero: [-122.39664, 37.79293], // east end of the Market St subway
  duboceChurch: [-122.42906, 37.7695], // N/J surface portal
  duboceFillmore: [-122.4318, 37.7695], // Sunset Tunnel, east portal
  carlCole: [-122.4497, 37.7661], // Sunset Tunnel, west portal
  westPortal: [-122.4665, 37.7405], // Twin Peaks Tunnel, west portal
  fourthBrannan: [-122.3965, 37.7773], // Central Subway, south portal
  chinatown: [-122.4066, 37.7947], // Central Subway, north end
};

// Per route, the portal pairs that bound its tunnels. K/L/M run Market and
// Twin Peaks back to back with no daylight at Castro, so that is one span.
const TUNNELS = {
  N: [['embarcadero', 'duboceChurch'], ['duboceFillmore', 'carlCole']],
  J: [['embarcadero', 'duboceChurch']],
  K: [['embarcadero', 'westPortal']],
  L: [['embarcadero', 'westPortal']],
  M: [['embarcadero', 'westPortal']],
  T: [['fourthBrannan', 'chinatown']],
};

// A portal further than this from the shape isn't on this route's alignment.
const PORTAL_MAX_OFF_M = 220;
// Distance either side of a portal over which the train eases under the
// street, so it descends into the tunnel instead of blinking out.
const PORTAL_RAMP_M = 45;

const PICK_RADIUS = 16;
// Angular slack on top of PICK_RADIUS: ~2.2 m per 100 m of range, so a tag holds
// a roughly constant click target on screen the same way it holds a constant
// drawn size. Shared value with the resident tags in population.js.
const PICK_ANGLE = 0.022;
const MAX_PICK_DISTANCE = 9000;

// Route glow: a vertical wall of light tracing each active route's shape,
// rising from the ground to this height. Visible at the hero view without
// dominating the skyline.
const ROUTE_GLOW_HEIGHT = 50;
// Per-mode neon colors for the route glow walls (RGB 0-1, saturated). Read as
// emitted light, so they are tuned bright for additive blending after dark.
const ROUTE_GLOW_COLORS = {
  bus: [1.0, 0.2, 0.05], // neon red-orange
  trolley: [0.1, 0.95, 0.4], // neon green
  lrv: [0.6, 0.1, 1.0], // neon purple
  streetcar: [1.0, 0.1, 0.6], // neon pink
  cable: [1.0, 0.95, 0.1], // neon yellow
};
// Daytime palette. Additive light cannot beat sunlight, so by day the wall is
// alpha-blended paint instead — and paint needs the opposite treatment from
// neon: deeper, denser hues that contrast against pale streets and rooftops,
// where the night colours (especially the yellow and green) wash straight out.
// Contrast here is against the DIORAMA, not against black, so each hue is
// picked to be what the city underneath is not — the transit green in
// particular is pulled toward teal, because forest green over Golden Gate
// Park is a route you cannot find.
const ROUTE_GLOW_DAY_COLORS = {
  bus: [0.88, 0.04, 0.02], // deep vermillion
  trolley: [0.0, 0.42, 0.44], // deep teal — reads against park green
  lrv: [0.33, 0.03, 0.78], // deep violet
  streetcar: [0.82, 0.0, 0.42], // magenta
  cable: [0.92, 0.52, 0.0], // amber
};
// The toy theme's warm ink, used to outline the daylight ribbon. A coloured
// edge only contrasts where the city behind it happens to be a different
// colour; an ink line contrasts everywhere, which is exactly why the UI cards
// are drawn this way.
const ROUTE_GLOW_INK = [0.13, 0.09, 0.07];
// Overall alpha of the ribbon, per palette. These multiply the shader's own
// profile (see ROUTE_GLOW_PROFILE), which already spends most of its alpha on
// the two edges, so they are far higher than the flat-curtain values they
// replaced — at the old night 0.125 the white core simply wasn't white.
const ROUTE_GLOW_DAY_OPACITY = 0.8;
const ROUTE_GLOW_NIGHT_OPACITY = 0.62;
// uNight below this counts as day: the palette and blend mode swap here.
const ROUTE_GLOW_NIGHT_AT = 0.5;

// How the ribbon is shaped across its height. A Tron light trail is not a
// tinted pane: it is a blown-out WHITE core with the colour living in the
// falloff around it, bounded by a hard clean edge. So the wall spends its
// alpha at the two edges — a crisp lit rim along the top and a contact flare
// where it meets the street — and stays nearly clear through the middle,
// which is also what lets you see the city through it.
//   coreWhite: how far the edges wash out to white (the "hot" core)
//   body:      alpha of the transparent interior
//   bodyFall:  how fast the interior thins with height (1 = linear, 2+ = only
//              a skirt near the street)
//   topEdge:   width of the top rim, as a fraction of wall height
//   baseEdge:  width of the ground flare
//   ink:       width of the dark outline along the top (0 = none)
const ROUTE_GLOW_PROFILE = {
  // After dark the core goes properly white-hot and the interior nearly
  // vanishes, so the route reads as a drawn line of light over the city.
  // No ink: the wall is emitted light against a dark city, and additive
  // blending cannot draw a dark line anyway.
  night: { coreWhite: 0.92, body: 0.27, bodyFall: 2.2, topEdge: 0.075, baseEdge: 0.16, ink: 0 },
  // By day the same ribbon has to survive sunlight (this is what PR #141/#143
  // were about) AND be findable from the hero altitude, where a rim alone is
  // a hairline. So daylight fills the interior nearly to the top (bodyFall 1
  // instead of 2.2, i.e. a linear fade rather than a skirt), whitens the core
  // less — a white edge on a pale street is an invisible edge — and outlines
  // the whole thing in warm ink.
  day: { coreWhite: 0.3, body: 1.0, bodyFall: 1.0, topEdge: 0.05, baseEdge: 0.13, ink: 0.05 },
};

// Module-scope scratch: the update loop and the picker must not allocate.
const dummy = new Object3D();

function shortestAngle(from, to) {
  let d = (to - from) % (Math.PI * 2);
  if (d > Math.PI) d -= Math.PI * 2;
  if (d < -Math.PI) d += Math.PI * 2;
  return d;
}

// ------------------------------------------------------------- baked shapes

// tiles/muni-shapes.bin — see pipeline/muni-shapes.mjs for the layout. Wraps
// resolution (trip -> shape), projection (fix -> arc length) and sampling
// (arc length -> position + tangent).
class ShapeSet {
  constructor(meta, floats) {
    this.meta = meta;
    this.floats = floats;
  }

  static async load() {
    const res = await fetch(SHAPES_URL);
    if (!res.ok) throw new Error(`shapes ${res.status}`);
    const buf = await res.arrayBuffer();
    const view = new DataView(buf);
    if (view.getUint32(0, true) !== SHAPES_MAGIC) throw new Error('shapes bad magic');
    const jsonLen = view.getUint32(8, true);
    const floatCount = view.getUint32(12, true);
    const meta = JSON.parse(new TextDecoder().decode(new Uint8Array(buf, 16, jsonLen)));
    // The bake pads the JSON chunk to a 4-byte boundary because a Float32Array
    // VIEW must start on one; copy instead of viewing if an older file doesn't.
    const at = 16 + jsonLen;
    const floats =
      at % 4 === 0
        ? new Float32Array(buf, at, floatCount)
        : new Float32Array(buf.slice(at, at + floatCount * 4));
    return new ShapeSet(meta, floats);
  }

  resolve(tripId, route, directionId) {
    const exact = this.meta.tripShape[tripId];
    if (exact !== undefined) return exact;
    const dirs = this.meta.routes[route]?.directions;
    if (!dirs) return -1;
    const byDir = dirs[directionId ?? 0];
    return byDir ?? dirs[0] ?? dirs[1] ?? -1;
  }

  headsign(tripId, route, directionId) {
    const idx =
      this.meta.tripHeadsign[tripId] ?? this.meta.tripDefaults[`${route}|${directionId ?? 0}`];
    return idx === undefined ? null : this.meta.strings[idx];
  }

  routeName(route) {
    return this.meta.routes[route]?.name ?? null;
  }

  stopName(stopId) {
    const stop = this.meta.stops[stopId];
    return stop ? this.meta.strings[stop.nameIdx] : null;
  }

  // Project (x, z) onto shape `idx`, searching only arc lengths within
  // `window` of `sHint` when given (so a bus can never snap backwards or onto
  // the return leg of a loop). Returns { s, dist }.
  project(idx, x, z, sHint = null, window = SNAP_WINDOW_M) {
    const shape = this.meta.shapes[idx];
    const F = this.floats;
    let bestS = 0;
    let bestD = Infinity;
    for (let i = 0; i < shape.vertexCount - 1; i++) {
      const o = (shape.vertexOffset + i) * 3;
      const q = o + 3;
      const s0 = F[o + 2];
      if (sHint != null && (s0 < sHint - 60 || s0 > sHint + window)) continue;
      const ax = F[o];
      const az = F[o + 1];
      const dx = F[q] - ax;
      const dz = F[q + 1] - az;
      const len2 = dx * dx + dz * dz;
      const t = len2 ? Math.max(0, Math.min(1, ((x - ax) * dx + (z - az) * dz) / len2)) : 0;
      const d = Math.hypot(ax + t * dx - x, az + t * dz - z);
      if (d < bestD) {
        bestD = d;
        bestS = s0 + Math.sqrt(len2) * t;
      }
    }
    return { s: bestS, dist: bestD };
  }

  // Position + forward tangent at arc length `s` (clamped to the shape).
  sample(idx, s, out) {
    const shape = this.meta.shapes[idx];
    const F = this.floats;
    const base = shape.vertexOffset * 3;
    const last = (shape.vertexOffset + shape.vertexCount - 1) * 3;
    const sClamped = Math.max(0, Math.min(shape.lengthM, s));
    // Binary search the cumulative arc lengths.
    let lo = 0;
    let hi = shape.vertexCount - 1;
    while (hi - lo > 1) {
      const mid = (lo + hi) >> 1;
      if (F[(shape.vertexOffset + mid) * 3 + 2] <= sClamped) lo = mid;
      else hi = mid;
    }
    const o = base + lo * 3;
    const q = Math.min(o + 3, last);
    const s0 = F[o + 2];
    const s1 = F[q + 2];
    const t = s1 > s0 ? (sClamped - s0) / (s1 - s0) : 0;
    out.x = F[o] + (F[q] - F[o]) * t;
    out.z = F[o + 1] + (F[q + 1] - F[o + 1]) * t;
    const dx = F[q] - F[o];
    const dz = F[q + 1] - F[o + 1];
    out.yaw = dx || dz ? Math.atan2(dx, dz) : out.yaw || 0;
    out.end = shape.lengthM;
    return out;
  }
}

// ------------------------------------------------------------------- merge

// Same idiom as the ferry: one geometry per surface class, material colour
// baked into COLOR_0, and the _Glow set kept separate so the destination sign
// and lights ignite at night instead of being flattened the way the road
// fleet's merge flattens them.
function mergeBus(root) {
  root.updateMatrixWorld(true);
  const body = [];
  const glow = [];
  root.traverse((object) => {
    if (!object.isMesh) return;
    const material = object.material;
    const geometry = object.geometry.clone();
    geometry.applyMatrix4(object.matrixWorld);
    geometry.deleteAttribute('uv');
    geometry.deleteAttribute('uv1');
    geometry.deleteAttribute('tangent');
    if (!geometry.attributes.normal) geometry.computeVertexNormals();
    const count = geometry.attributes.position.count;
    const source = geometry.attributes.color;
    const colors = new Float32Array(count * 3);
    const base = material?.color;
    for (let i = 0; i < count; i++) {
      const r = base ? base.r : 1;
      const g = base ? base.g : 1;
      const b = base ? base.b : 1;
      colors[i * 3] = source ? source.getX(i) * r : r;
      colors[i * 3 + 1] = source ? source.getY(i) * g : g;
      colors[i * 3 + 2] = source ? source.getZ(i) * b : b;
    }
    geometry.setAttribute('color', new BufferAttribute(colors, 3));
    (material?.name?.endsWith('_Glow') ? glow : body).push(geometry);
  });
  const join = (parts) => {
    if (!parts.length) return null;
    const merged = mergeGeometries(parts, false);
    for (const part of parts) part.dispose();
    return merged;
  };
  return { body: join(body), glow: join(glow) };
}

// ------------------------------------------------------------------- badges

// Route pills in the toy UI voice: cream card stock, warm-ink 2 px border and
// type, one HARD offset shadow, no gradients (AGENTS "UI" section). One canvas
// atlas, one instanced quad layer; each instance selects its route's cell via
// an instanced uv-rect attribute patched into the material.
class BadgeAtlas {
  constructor() {
    this.canvas = document.createElement('canvas');
    this.canvas.width = 1024;
    this.canvas.height = 1024;
    this.ctx = this.canvas.getContext('2d');
    this.texture = new CanvasTexture(this.canvas);
    this.texture.colorSpace = SRGBColorSpace;
    this.slots = new Map(); // route -> [u, v, w, h]
  }

  // One cell: a rounded bubble with a tail dropping from its underside, drawn
  // once the first time a route appears on screen.
  rect(route) {
    let slot = this.slots.get(route);
    if (slot) return slot;
    const index = this.slots.size;
    if (index >= BADGE_COLS * BADGE_ROWS) return [0, 0, 0, 0];
    const cell = this.canvas.width / BADGE_COLS; // 128 px, square
    const x = (index % BADGE_COLS) * cell;
    const y = Math.floor(index / BADGE_COLS) * cell;

    const ctx = this.ctx;
    ctx.clearRect(x, y, cell, cell);
    ctx.save();
    ctx.translate(x, y);

    // Bubble body + tail as ONE path, so the outline runs around the joint
    // instead of drawing a seam across the bubble's underside.
    const bx = 7;
    const by = 6;
    const bw = cell - 14;
    const bh = 82;
    const r = 20;
    const tailL = 48;
    const tailR = 80;
    const tipX = 56; // a touch left of centre, as the reference does it
    const tipY = 118;
    ctx.beginPath();
    ctx.moveTo(bx + r, by);
    ctx.lineTo(bx + bw - r, by);
    ctx.quadraticCurveTo(bx + bw, by, bx + bw, by + r);
    ctx.lineTo(bx + bw, by + bh - r);
    ctx.quadraticCurveTo(bx + bw, by + bh, bx + bw - r, by + bh);
    ctx.lineTo(tailR, by + bh);
    ctx.lineTo(tipX, tipY); // the point, aimed at the roof below
    ctx.lineTo(tailL, by + bh);
    ctx.lineTo(bx + r, by + bh);
    ctx.quadraticCurveTo(bx, by + bh, bx, by + bh - r);
    ctx.lineTo(bx, by + r);
    ctx.quadraticCurveTo(bx, by, bx + r, by);
    ctx.closePath();

    // Soft drop shadow lifts the bubble off whatever roof is behind it.
    ctx.shadowColor = 'rgba(28, 24, 20, 0.34)';
    ctx.shadowBlur = 7;
    ctx.shadowOffsetY = 4;
    ctx.fillStyle = '#fbf7ee';
    ctx.fill();
    ctx.shadowColor = 'transparent';
    ctx.lineWidth = 5;
    ctx.lineJoin = 'round';
    ctx.strokeStyle = '#3a3530';
    ctx.stroke();

    ctx.fillStyle = '#3a3530';
    const size = route.length > 3 ? 36 : route.length > 2 ? 44 : 54;
    ctx.font = `800 ${size}px ui-rounded, "SF Pro Rounded", -apple-system, system-ui, sans-serif`;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(route, bx + bw / 2, by + bh / 2 + 1);
    ctx.restore();

    const u = cell / this.canvas.width;
    slot = [x / this.canvas.width, 1 - (y + cell) / this.canvas.height, u, u];
    this.slots.set(route, slot);
    this.texture.needsUpdate = true;
    return slot;
  }
}

function buildBadgeMesh(atlas) {
  const geometry = new PlaneGeometry(BADGE_W, BADGE_H);
  const uvRect = new InstancedBufferAttribute(new Float32Array(CAPACITY * 4), 4);
  uvRect.setUsage(DynamicDrawUsage);
  geometry.setAttribute('uvRect', uvRect);
  const material = new MeshBasicMaterial({
    map: atlas.texture,
    transparent: true,
    depthWrite: false,
    alphaTest: 0.02,
  });
  // Remap each instance's unit uv into its atlas cell.
  material.onBeforeCompile = (shader) => {
    shader.vertexShader = shader.vertexShader
      .replace('#include <common>', '#include <common>\nattribute vec4 uvRect;')
      .replace('#include <uv_vertex>', '#include <uv_vertex>\n  vMapUv = uvRect.xy + vMapUv * uvRect.zw;');
  };
  const mesh = new InstancedMesh(geometry, material, CAPACITY);
  mesh.name = 'live-muni-badges';
  mesh.instanceMatrix.setUsage(DynamicDrawUsage);
  mesh.frustumCulled = false;
  mesh.renderOrder = 4;
  mesh.count = 0;
  return { mesh, uvRect };
}

// -------------------------------------------------------------------- layer

export function createLiveMuni(scene, data) {
  const params = new URLSearchParams(window.location.search);
  const demo = params.get('muni') === 'demo';

  const buses = new Map(); // id -> state
  let shapes = null; // ShapeSet | null (null => dead-reckon everything)
  // Fleet: one entry per mode that has a model. Each entry carries its own
  // InstancedMesh pair and scale, so a bus/trolley/LRV/streetcar/cable car
  // each render with their own geometry. Modes without a dedicated model fall
  // back to the bus entry (the "placeholder" fleet).
  const fleets = []; // { key, bodyMesh, glowMesh, scale, sinkM, count }
  let fleetByKey = {}; // mode -> fleet entry (resolved at load time)
  const tunnelRanges = new Map(); // `${shapeIdx}|${route}` -> [[s0, s1], ...]
  let badge = null;
  let atlas = null;
  let ready = false;
  let live = false;
  let degraded = false;
  let nextPollAt = 0;
  let polling = false;
  let warnedFetch = false;
  let demoStart = 0;
  let arrivalsByStop = new Map();
  // Is the feed predicting stop times at all this poll? On the shared ferry key
  // it isn't (degraded mode), and then "no predictions" says nothing about a
  // single vehicle — only when other vehicles do have them is an empty list
  // evidence that this one isn't working yet.
  let predictionsSeen = false;
  let lastFetchedAt = 0; // server-side fetchedAt of the last non-stale /api/muni payload
  // Adaptive badge radius, within whatever the zoom allows. A dense corridor
  // pulls it in, a quiet neighbourhood lets it back out. O(1) per frame, no
  // sorting, no allocation, and slow enough that bubbles fade rather than blink.
  let badgeRadius = BADGE_RADIUS_MAX;

  // Route glow: active route shape indices -> mode, rebuilt each poll.
  // The glow mesh is a single BufferGeometry rebuilt when the active set
  // changes, rendered as one transparent additive draw call.
  const activeRouteShapes = new Map(); // shapeIdx -> mode
  let routeGlowMesh = null;
  let routeGlowDirty = false;
  // Both vertex-colour palettes for the current geometry, and which one is
  // bound right now (starts on the day palette — setRouteGlowDay corrects it
  // on the first frame if the city boots after dark).
  let routeGlowPalettes = null;
  let routeGlowUniforms = null;
  let routeGlowIsDay = true;

  // ------------------------------------------------------------- subway

  // Arc length of a portal along `shapeIdx`, or null when that portal is not on
  // this shape (a route that never enters that tunnel, or a shape that no
  // longer runs past it).
  function portalS(shapeIdx, key) {
    const [lon, lat] = PORTAL[key];
    const [x, z] = data.project(lon, lat);
    const hit = shapes.project(shapeIdx, x, z, null, Infinity);
    return hit.dist <= PORTAL_MAX_OFF_M ? hit.s : null;
  }

  // The underground arc-length ranges of one shape, resolved once and memoised.
  // A route with no tunnels resolves to an empty list and costs one lookup.
  function undergroundFor(shapeIdx, route) {
    const key = `${shapeIdx}|${route}`;
    const cached = tunnelRanges.get(key);
    if (cached) return cached;
    const ranges = [];
    for (const [a, b] of TUNNELS[String(route).toUpperCase()] || []) {
      const sa = portalS(shapeIdx, a);
      const sb = portalS(shapeIdx, b);
      if (sa == null || sb == null) continue;
      ranges.push([Math.min(sa, sb), Math.max(sa, sb)]);
    }
    tunnelRanges.set(key, ranges);
    return ranges;
  }

  // 0 at street level, 1 once fully under, ramped either side of the portal.
  function tunnelDepth(ranges, s) {
    for (const [s0, s1] of ranges) {
      if (s <= s0 || s >= s1) continue;
      return Math.min(1, Math.min(s - s0, s1 - s) / PORTAL_RAMP_M);
    }
    return 0;
  }

  async function load() {
    // The shapes bake is an enhancement, not a requirement: without it every
    // bus falls back to straight-line dead reckoning (spec fallback ladder).
    try {
      shapes = await ShapeSet.load();
    } catch (error) {
      shapes = null;
      console.warn(`sf-muni: no route shapes (${error.message}) — buses will dead-reckon`);
    }

    // Manifest entries for every mode we want to render. The bus model is the
    // minimum — without it, nothing renders. The others are best-effort: a
    // missing streetcar or cable car GLB degrades that mode to the bus model
    // (placeholder), not to nothing.
    let manifest = null;
    try {
      const res = await fetch(MANIFEST);
      if (res.ok) manifest = (await res.json()).vehicles || [];
    } catch {
      manifest = null;
    }
    if (!manifest) {
      console.warn('sf-muni: no vehicle manifest — live buses disabled');
      return;
    }

    // Mode -> manifest id. Trolley still uses the bus model as a placeholder
    // until a dedicated GLB is built (owner decision).
    const MODE_ENTRIES = [
      { mode: 'bus', id: 'muni-bus-40' },
      { mode: 'trolley', id: 'muni-bus-40' }, // placeholder: shares bus body
      { mode: 'lrv', id: 'muni-lrv' },
      { mode: 'streetcar', id: 'muni-streetcar-pcc' },
      { mode: 'cable', id: 'cable-car-powell' },
    ];

    const loader = createGLTFLoader();
    const loadedByMode = {}; // mode -> { body, glow, scale } | null

    for (const { mode, id } of MODE_ENTRIES) {
      if (loadedByMode[mode]) continue; // already loaded (bus reused for trolley/lrv)
      const entry = manifest.find((v) => v.id === id);
      if (!entry) {
        console.warn(`sf-muni: no ${id} manifest entry — ${mode} will use bus model`);
        continue;
      }
      try {
        const gltf = await loader.loadAsync(`${import.meta.env.BASE_URL}sf-assets/${entry.file}`);
        const merged = mergeBus(gltf.scene);
        if (!merged.body) {
          console.warn(`sf-muni: ${id} had no geometry — ${mode} will use bus model`);
          continue;
        }
        merged.body.computeBoundingBox();
        const measured = merged.body.boundingBox.max.z - merged.body.boundingBox.min.z;
        const target = entry.dims?.[2] ?? measured;
        const scale = (measured > 0 ? target / measured : 1) * CAR_SCALE;
        const height = merged.body.boundingBox.max.y - merged.body.boundingBox.min.y;
        loadedByMode[mode] = { body: merged.body, glow: merged.glow, scale, height };
      } catch (error) {
        console.warn(`sf-muni: ${id} failed to load (${error.message}) — ${mode} will use bus model`);
      }
    }

    // The bus model is the floor — without it, nothing renders at all.
    if (!loadedByMode.bus) {
      console.warn('sf-muni: bus model unavailable — live buses disabled');
      return;
    }

    // Build one fleet entry per mode that successfully loaded. Modes that
    // didn't get their own model fall back to the bus fleet entry.
    for (const { mode } of MODE_ENTRIES) {
      const loaded = loadedByMode[mode] || loadedByMode.bus;
      const bodyMesh = new InstancedMesh(loaded.body, new MeshLambertMaterial({ vertexColors: true }), CAPACITY);
      bodyMesh.name = `live-muni-${mode}`;
      bodyMesh.instanceMatrix.setUsage(DynamicDrawUsage);
      bodyMesh.frustumCulled = false;
      bodyMesh.castShadow = false;
      bodyMesh.count = 0;
      let glowMesh = null;
      if (loaded.glow) {
        glowMesh = new InstancedMesh(loaded.glow, new MeshBasicMaterial({ vertexColors: true, transparent: true }), CAPACITY);
        glowMesh.name = `live-muni-${mode}-glow`;
        glowMesh.instanceMatrix.setUsage(DynamicDrawUsage);
        glowMesh.frustumCulled = false;
        glowMesh.castShadow = false;
        glowMesh.count = 0;
      }
      // How far to drop a vehicle for it to be wholly under the street, plus a
      // metre so a crowned road can't leave a roof showing.
      const sinkM = (loaded.height || 4) * loaded.scale + 1;
      const fleet = { key: mode, bodyMesh, glowMesh, scale: loaded.scale, sinkM, count: 0 };
      fleets.push(fleet);
      fleetByKey[mode] = fleet;
      scene.add(bodyMesh);
      if (glowMesh) scene.add(glowMesh);
    }

    atlas = new BadgeAtlas();
    badge = buildBadgeMesh(atlas);
    scene.add(badge.mesh);

    // Route glow mesh: a single dynamic BufferGeometry rendered as one
    // transparent wall. Rebuilt when the active route set changes; the blend
    // mode starts where routeGlowIsDay does and setRouteGlowDay flips it.
    routeGlowMesh = new Mesh(
      new BufferGeometry(),
      routeGlowMaterial(),
    );
    routeGlowMesh.name = 'live-muni-route-glow';
    routeGlowMesh.frustumCulled = false;
    routeGlowMesh.renderOrder = 2;
    scene.add(routeGlowMesh);

    ready = true;
  }

  // ---------------------------------------------------------------- fixes

  // Everything that keeps a vehicle out of the scene. Demo runs are exempt:
  // they exist to exercise the dwell and dead-reckon paths.
  function hiddenReason(state) {
    if (demo) return null;
    return dormantReason(state, predictionsSeen) ?? (state.shapeIdx < 0 ? 'offRoute' : null);
  }

  function apply(list, now, stale) {
    for (const state of buses.values()) state.seen = false;

    for (const bus of list) {
      // Resolve the fleet for this vehicle's mode. Unknown modes fall back to
      // the bus fleet (the first entry), which is always present.
      const fleet = fleetByKey[bus.mode] || fleets[0];

      // Stale payload (CDN cache hit): mark everyone seen so they aren't
      // dropped, and keep lastFixAt current so the stale-drop check in the
      // frame loop doesn't evict a bus that is still being reported. Don't
      // touch positions or speeds — the frame loop's dead-reckon extrapolation
      // keeps them moving along their shapes.
      if (stale) {
        const state = buses.get(bus.id);
        if (state) { state.seen = true; state.lastFixAt = now; }
        continue;
      }

      const [x, z] = data.project(bus.lon, bus.lat);
      let state = buses.get(bus.id);
      if (!state) {
        if (buses.size >= CAPACITY) continue;
        state = {
          id: bus.id,
          fleetNumber: bus.fleetNumber,
          route: bus.route,
          mode: bus.mode,
          fleet,
          directionId: bus.directionId,
          tripId: bus.tripId,
          x,
          z,
          yaw: 0,
          // Seeded from the fix, not zero: otherwise every bus stands still for
          // a full poll after it appears, and a page load shows a frozen fleet.
          // A reported 0 is not evidence of standing still — seedSpeed().
          speed: seedSpeed(bus, now, predictionsSeen),
          targetSpeed: seedSpeed(bus, now, predictionsSeen),
          shapeIdx: -1,
          s: 0,
          targetS: 0,
          fixX: x,
          fixZ: z,
          occupancy: bus.occupancy,
          stops: bus.stops || [],
          recordedAt: bus.recordedAt ?? now,
          lastFixAt: now,
          lastFreshFixAt: now,
          misses: 0,
          seen: true,
          index: -1,
          // Last fix at which this vehicle had actually moved: the clock every
          // parked/layover decision is made against.
          movedAt: now,
          // Running on a guess until a second fix confirms it, so the guess is
          // capped (provisionalCap) and cannot reverse the bus when it lands.
          provisional: !(Number.isFinite(bus.speedMs) && bus.speedMs > 0),
          provisionalCap: Infinity,
          hide: 0,
          hidden: null,
          sample: { x, z, yaw: 0, end: 0 },
        };
        placeOnShape(state, true);
        state.provisionalCap = state.s + PROVISIONAL_LEAD_M;
        // Off every one of its route's alignments: start it already sunk, so it
        // never flashes on the street before being hidden.
        state.hide = hiddenReason(state) === 'offRoute' ? 1 : 0;
        buses.set(bus.id, state);
        continue;
      }

      // Same fix as the previous poll (server re-fetched from 511 but this
      // vehicle hasn't reported a new position)? Keep dead-reckoning — don't
      // reset target/speed, which would freeze the bus at the stale target.
      // Update lastFixAt so the stale-drop check doesn't evict it.
      if (bus.recordedAt != null && state.recordedAt === bus.recordedAt) {
        state.seen = true;
        state.misses = 0;
        state.lastFixAt = now;
        continue;
      }

      const gap = Math.max(1, (now - state.lastFreshFixAt) / 1000);
      const prevFixX = state.fixX;
      const prevFixZ = state.fixZ;
      state.fixX = x;
      state.fixZ = z;
      state.route = bus.route;
      state.mode = bus.mode;
      state.fleet = fleet;
      state.directionId = bus.directionId;
      state.occupancy = bus.occupancy;
      state.stops = bus.stops || [];
      state.recordedAt = bus.recordedAt ?? now;
      state.lastFixAt = now;
      state.lastFreshFixAt = now;
      state.seen = true;

      const tripChanged = state.tripId !== bus.tripId;
      state.tripId = bus.tripId;
      if (tripChanged || state.shapeIdx < 0) {
        placeOnShape(state, tripChanged);
      } else {
        const hit = shapes.project(state.shapeIdx, x, z, state.s);
        if (hit.dist > SNAP_LIMIT_M) {
          // Off its known alignment (detour, or our resolution missed):
          // re-resolve from scratch, else drop to dead reckoning.
          placeOnShape(state, true);
        } else {
          state.targetS = hit.s;
          // Dead-reckon (or a provisional first-fix guess) may have driven the
          // bus past where the fresh fix says it is. Hold it there and let the
          // next fix pull it forward rather than reversing it — a bus sliding
          // backwards up the street is the one artefact the eye always catches.
          // Only a wrong guess, not a few seconds of drift, snaps back.
          if (state.s > state.targetS) {
            if (state.s - state.targetS <= OVERSHOOT_HOLD_M) state.targetS = state.s;
            else state.s = state.targetS;
          }
        }
      }

      // How fast to run so the bus covers the ground it actually covered:
      // targetSpeedFor() owns the dwell rule (invariants 1 and 2 — displacement
      // between FIXES, never the reported speed, never gapS).
      const reported = Number.isFinite(bus.speedMs) ? bus.speedMs : null;
      const fixStep = Math.hypot(x - prevFixX, z - prevFixZ);
      const onShape = state.shapeIdx >= 0;
      // Two fixes in hand: the guess is over, and this is the only place that
      // can honestly say the vehicle moved.
      state.provisional = false;
      if (fixStep >= DWELL_STEP_M) state.movedAt = now;
      state.targetSpeed = targetSpeedFor({
        fixStep,
        gapSeconds: gap,
        gapS: state.targetS - state.s,
        reported,
        onShape,
      });
      if (!onShape) {
        state.deadYaw = fixStep > 4 ? Math.atan2(x - prevFixX, z - prevFixZ) : state.deadYaw;
      }
    }

    for (const [id, state] of buses) {
      if (state.seen) {
        state.misses = 0;
        continue;
      }
      state.misses += 1;
      if (shouldDrop(state, now)) buses.delete(id);
    }

    // Rebuild the active route set for the glow walls. Only routes with at
    // least one live vehicle on them get a wall — this is called once per
    // poll (not per frame), so the cost is negligible.
    if (!stale) {
      const next = new Map();
      for (const state of buses.values()) {
        // Only routes that are actually RUNNING light up. A single coach parked
        // in a yard used to switch on its whole route's wall, which reads as
        // "the 5 is running" at an hour when it isn't.
        if (state.shapeIdx >= 0 && state.seen && !hiddenReason(state)) {
          // The route rides along so the wall builder can ask which stretches
          // of this shape are tunnel; mode alone only picks the colour.
          if (!next.has(state.shapeIdx))
            next.set(state.shapeIdx, { mode: state.mode || 'bus', route: state.route });
        }
      }
      if (next.size !== activeRouteShapes.size || [...next.keys()].some((k) => !activeRouteShapes.has(k))) {
        activeRouteShapes.clear();
        for (const [k, v] of next) activeRouteShapes.set(k, v);
        routeGlowDirty = true;
      }
    }
  }

  function placeOnShape(state, fresh) {
    state.shapeIdx = shapes ? shapes.resolve(state.tripId, state.route, state.directionId) : -1;
    if (state.shapeIdx >= 0) {
      const hit = shapes.project(state.shapeIdx, state.fixX, state.fixZ, fresh ? null : state.s);
      if (hit.dist <= SNAP_LIMIT_M) {
        state.targetS = hit.s;
        if (fresh || Math.abs(hit.s - state.s) > SNAP_WINDOW_M) state.s = hit.s;
        return;
      }
    }
    // The default shape was too far — try all shapes for this route. Routes
    // often have variant shapes (e.g. route 14 has 4 shapes), and the direction
    // default is just the most-used one, not necessarily the right one.
    const routeShapeList = shapes?.meta.routeShapes?.[state.route];
    if (routeShapeList) {
      let bestIdx = -1, bestDist = SNAP_LIMIT_M, bestS = 0;
      for (const idx of routeShapeList) {
        if (idx === state.shapeIdx) continue;
        const hit = shapes.project(idx, state.fixX, state.fixZ, null);
        if (hit.dist < bestDist) { bestDist = hit.dist; bestIdx = idx; bestS = hit.s; }
      }
      if (bestIdx >= 0) {
        state.shapeIdx = bestIdx;
        state.targetS = bestS;
        if (fresh || Math.abs(bestS - state.s) > SNAP_WINDOW_M) state.s = bestS;
        return;
      }
    }
    // Nowhere on its own route. This used to fall back to searching ALL 298
    // baked shapes for one the vehicle happened to sit on, which is how a coach
    // deadheading to a yard ended up driving down someone else's route: being
    // near a line is not being on it. A vehicle we cannot place on its OWN
    // alignment is left off the map instead of invented onto another one.
    state.shapeIdx = -1;
  }

  // ----------------------------------------------------------------- demo

  // data.js exports project() but not its inverse; the projection is affine,
  // so two probes recover it. Demo-only.
  let inverse = null;
  function unproject(x, z) {
    if (!inverse) {
      const [x0, z0] = data.project(0, 0);
      const [x1] = data.project(1, 0);
      const [, z1] = data.project(0, 1);
      inverse = { x0, z0, mx: x1 - x0, mz: z1 - z0 };
    }
    return [(x - inverse.x0) / inverse.mx, (z - inverse.z0) / inverse.mz];
  }

  function demoFixes(now) {
    if (!shapes) return [];
    const elapsed = (now - demoStart) / 1000;
    const list = [];
    // Each mode that owns a distinct GLB needs a run here, or the only way to
    // see it is to wait for the live feed to put one in shot.
    const runs = [
      { id: 'DEMO:8801', route: '38R', dir: 0, speed: 9, offset: 0, mode: 'bus' },
      { id: 'DEMO:8802', route: '38R', dir: 0, speed: 9, offset: 900, mode: 'bus' },
      { id: 'DEMO:8632', route: '29', dir: 1, speed: 7, offset: 300, mode: 'bus' },
      { id: 'DEMO:8641', route: '29', dir: 1, speed: 0, offset: 2200, mode: 'bus' }, // dwells forever
      { id: 'DEMO:8899', route: '44', dir: 0, speed: 8, offset: 1500, mode: 'bus' },
      // One N out on the surface in the Sunset, one starting inside the Sunset
      // Tunnel (s 7375-8972 on the outbound shape) so every demo run exercises
      // the underground path and the portal ramp.
      { id: 'DEMO:2002', route: 'N', dir: 0, speed: 10, offset: 8600, mode: 'lrv' },
      { id: 'DEMO:2014', route: 'N', dir: 0, speed: 10, offset: 10500, mode: 'lrv' },
      { id: 'DEMO:1051', route: 'F', dir: 0, speed: 6, offset: 400, mode: 'streetcar' },
    ];
    for (const run of runs) {
      const idx = shapes.resolve(null, run.route, run.dir);
      if (idx < 0) continue;
      const shape = shapes.meta.shapes[idx];
      const s = (run.offset + elapsed * run.speed) % shape.lengthM;
      const out = { x: 0, z: 0, yaw: 0, end: 0 };
      shapes.sample(idx, s, out);
      const [lon, lat] = unproject(out.x, out.z);
      list.push({
        id: run.id,
        fleetNumber: run.id.slice(5),
        mode: run.mode,
        route: run.route,
        directionId: run.dir,
        tripId: `demo-${run.route}-${run.dir}`,
        lat,
        lon,
        bearingDeg: null,
        speedMs: run.speed,
        occupancy: run.speed ? 'fewSeatsAvailable' : 'manySeatsAvailable',
        recordedAt: now,
        stops: [],
      });
    }
    // One bus far off any shape: exercises the dead-reckon fallback.
    list.push({
      id: 'DEMO:9999',
      fleetNumber: '9999',
      mode: 'bus',
      route: '77X',
      directionId: 0,
      tripId: 'demo-none',
      lat: 37.826,
      lon: -122.422,
      bearingDeg: 45,
      speedMs: 6,
      occupancy: null,
      recordedAt: now,
      stops: [],
    });
    return list;
  }

  // ----------------------------------------------------------------- poll

  async function poll(now) {
    if (demo) {
      if (!demoStart) demoStart = now;
      apply(demoFixes(now), now);
      live = true;
      return;
    }
    let payload;
    try {
      const res = await fetch('/api/muni', { headers: { accept: 'application/json' } });
      if (!res.ok) throw new Error(`api ${res.status}`);
      payload = await res.json();
    } catch (error) {
      if (!warnedFetch) {
        warnedFetch = true;
        console.warn(`sf-muni: /api/muni unavailable (${error.message}) — no live buses`);
      }
      live = false;
      return;
    }
    if (!payload?.live || !Array.isArray(payload.vehicles)) {
      live = false;
      buses.clear();
      return;
    }
    live = true;
    degraded = !!payload.degraded;
    predictionsSeen = payload.vehicles.some((v) => v.stops?.length);
    // CDN cache hit? The server's fetchedAt is identical to the previous poll's
    // — every vehicle in this payload is the same fix. Skip position updates so
    // buses keep dead-reckoning along their shapes instead of freezing at the
    // stale target. The per-vehicle recordedAt check in apply() catches the
    // rarer case where the server re-fetched but individual vehicles haven't
    // reported a new position.
    const stalePayload = payload.fetchedAt && payload.fetchedAt === lastFetchedAt;
    if (payload.fetchedAt) lastFetchedAt = payload.fetchedAt;
    // Index the predictions by stop so the stop layer's card can answer "what
    // is coming here" from the same poll — a second fetch would double the
    // spend against a 60-request-an-hour key for data already in hand.
    // Skipped on a stale payload: the arrivals map is unchanged.
    if (!stalePayload) {
      const byStop = new Map();
      for (const vehicle of payload.vehicles) {
        for (const stop of vehicle.stops || []) {
          let list = byStop.get(stop.stopId);
          if (!list) byStop.set(stop.stopId, (list = []));
          list.push({ route: vehicle.route, mode: vehicle.mode, at: stop.arrivalAt, fleetNumber: vehicle.fleetNumber });
        }
      }
      for (const list of byStop.values()) list.sort((a, b) => a.at - b.at);
      arrivalsByStop = byStop;
    }
    apply(payload.vehicles, now, stalePayload);
  }

  function schedule() {
    nextPollAt = Date.now() + (demo ? DEMO_POLL_MS : POLL_MS + Math.random() * POLL_JITTER_MS);
  }

  function tick(now) {
    if (polling || document.hidden || now < nextPollAt) return;
    polling = true;
    poll(now).finally(() => {
      polling = false;
      schedule();
    });
  }

  document.addEventListener('visibilitychange', () => {
    if (!document.hidden) nextPollAt = 0;
  });

  load();

  // ------------------------------------------------------- route glow walls

  // The ribbon shader. MeshBasicMaterial carries the vertex colours, the
  // blend mode and the day/night opacity exactly as before; onBeforeCompile
  // only reshapes the alpha across the wall's height (aRibbon: 0 at the
  // street, 1 at the top) and burns the edges toward white.
  function routeGlowMaterial() {
    const material = new MeshBasicMaterial({
      vertexColors: true,
      transparent: true,
      blending: 1, // NormalBlending (day); AdditiveBlending after dark
      depthWrite: false,
      side: 2, // DoubleSide — visible from both sides of the wall
      toneMapped: false, // a light trail is emitted light, not a lit surface
    });
    const profile = ROUTE_GLOW_PROFILE[routeGlowIsDay ? 'day' : 'night'];
    routeGlowUniforms = {
      uCoreWhite: { value: profile.coreWhite },
      uBody: { value: profile.body },
      uBodyFall: { value: profile.bodyFall },
      uTopEdge: { value: profile.topEdge },
      uBaseEdge: { value: profile.baseEdge },
      uInk: { value: profile.ink },
      uInkColor: { value: new Color(...ROUTE_GLOW_INK) },
    };
    material.onBeforeCompile = (shader) => {
      Object.assign(shader.uniforms, routeGlowUniforms);
      shader.vertexShader = shader.vertexShader
        .replace('#include <common>', '#include <common>\n        attribute float aRibbon;\n        varying float vRibbon;')
        .replace('#include <begin_vertex>', '#include <begin_vertex>\n        vRibbon = aRibbon;');
      shader.fragmentShader = shader.fragmentShader
        .replace(
          '#include <common>',
          `#include <common>
          uniform float uCoreWhite;
          uniform float uBody;
          uniform float uBodyFall;
          uniform float uTopEdge;
          uniform float uBaseEdge;
          uniform float uInk;
          uniform vec3 uInkColor;
          varying float vRibbon;`
        )
        .replace(
          '#include <dithering_fragment>',
          `#include <dithering_fragment>
          // Two hot edges and a near-clear interior.
          float top = exp(-pow((1.0 - vRibbon) / uTopEdge, 2.0));
          float base = exp(-pow(vRibbon / uBaseEdge, 2.0));
          // The interior is brightest where the light spills off the street
          // and thins upward, so the wall has a direction: it is lit FROM the
          // route, not uniformly filled.
          float body = uBody * pow(1.0 - vRibbon, uBodyFall);
          float edge = clamp(top + base * 0.85, 0.0, 1.0);
          gl_FragColor.rgb = mix(gl_FragColor.rgb, vec3(1.0), edge * uCoreWhite);
          float alpha = clamp(body * 0.55 + top + base * 0.8, 0.0, 1.0);
          // Ink outline (day only): a dark line capping the ribbon, so it is
          // legible over a white rooftop and a dark street alike.
          float ink = uInk > 0.0 ? smoothstep(1.0 - uInk, 1.0 - uInk * 0.35, vRibbon) : 0.0;
          gl_FragColor.rgb = mix(gl_FragColor.rgb, uInkColor, ink);
          gl_FragColor.a = max(alpha, ink) * opacity;`
        );
    };
    return material;
  }

  function rebuildRouteGlow() {
    if (!shapes || !routeGlowMesh) return;
    const F = shapes.floats;
    const meta = shapes.meta;

    // Collect vertices for all active route walls. Each shape polyline segment
    // becomes a quad (4 vertices, 2 triangles): bottom-left, top-left,
    // bottom-right, top-right. Vertex colors carry the mode color.
    const positions = [];
    const colors = [];
    const dayColors = [];
    // Height of each vertex within the ribbon, 0 at the street and 1 at the
    // top. The shader shapes the trail along this, so it is not derivable
    // from world y: the wall follows the terrain up and down the hills.
    const ribbon = [];
    const indices = [];

    for (const [shapeIdx, { mode, route }] of activeRouteShapes) {
      const shape = meta.shapes[shapeIdx];
      if (!shape) continue;
      const color = ROUTE_GLOW_COLORS[mode] || ROUTE_GLOW_COLORS.bus;
      const dayColor = ROUTE_GLOW_DAY_COLORS[mode] || ROUTE_GLOW_DAY_COLORS.bus;
      const base = shape.vertexOffset * 3;
      const count = shape.vertexCount;
      // A wall marks where you can catch this route, so it ends at the portal
      // for the same reason the train does: the tunnelled stretch isn't on the
      // surface, and a beam over Buena Vista Heights says it is.
      const tunnel = TUNNELS[String(route).toUpperCase()] ? undergroundFor(shapeIdx, route) : null;

      for (let i = 0; i < count - 1; i++) {
        const o = base + i * 3;
        const q = o + 3;
        if (tunnel?.length) {
          const mid = (F[o + 2] + F[q + 2]) / 2;
          if (tunnel.some(([s0, s1]) => mid > s0 && mid < s1)) continue;
        }
        const x0 = F[o], z0 = F[o + 1];
        const x1 = F[q], z1 = F[q + 1];

        // Sample terrain elevation so walls sit on the ground, not through hills.
        const y0 = data.sampleElevation ? data.sampleElevation(x0, z0) : 0;
        const y1 = data.sampleElevation ? data.sampleElevation(x1, z1) : 0;

        // Four corners of the wall segment: bottom and top at each end.
        const v = positions.length / 3;
        // bottom-left (x0, y0, z0)
        positions.push(x0, y0, z0);
        // top-left (x0, y0 + height, z0)
        positions.push(x0, y0 + ROUTE_GLOW_HEIGHT, z0);
        // bottom-right (x1, y1, z1)
        positions.push(x1, y1, z1);
        // top-right (x1, y1 + height, z1)
        positions.push(x1, y1 + ROUTE_GLOW_HEIGHT, z1);

        // Color all four vertices with the mode color, in both palettes
        for (let j = 0; j < 4; j++) {
          colors.push(color[0], color[1], color[2]);
          dayColors.push(dayColor[0], dayColor[1], dayColor[2]);
        }
        // Matches the corner order pushed above: bottom, top, bottom, top.
        ribbon.push(0, 1, 0, 1);

        // Two triangles: (v, v+1, v+2) and (v+1, v+3, v+2)
        indices.push(v, v + 1, v + 2, v + 1, v + 3, v + 2);
      }
    }

    const geo = routeGlowMesh.geometry;
    geo.setAttribute('position', new BufferAttribute(new Float32Array(positions), 3));
    // Both palettes are baked once here; the frame loop only swaps which
    // attribute is bound, so the day/night flip allocates nothing.
    routeGlowPalettes = {
      night: new BufferAttribute(new Float32Array(colors), 3),
      day: new BufferAttribute(new Float32Array(dayColors), 3),
    };
    geo.setAttribute('color', routeGlowPalettes[routeGlowIsDay ? 'day' : 'night']);
    geo.setAttribute('aRibbon', new BufferAttribute(new Float32Array(ribbon), 1));
    geo.setIndex(indices);
    geo.computeVertexNormals();
    routeGlowMesh.visible = positions.length > 0;
  }

  // Swap palette + blend mode when the scene crosses dusk/dawn. Additive keeps
  // the neon beam glowing after dark; NormalBlending makes the same wall an
  // opaque painted curtain by day, which is the only way it survives sunlight.
  function setRouteGlowDay(isDay) {
    if (isDay === routeGlowIsDay) return;
    routeGlowIsDay = isDay;
    if (!routeGlowMesh) return;
    const mat = routeGlowMesh.material;
    mat.blending = isDay ? 1 : 2; // NormalBlending : AdditiveBlending
    mat.needsUpdate = true;
    if (routeGlowPalettes) {
      routeGlowMesh.geometry.setAttribute('color', routeGlowPalettes[isDay ? 'day' : 'night']);
    }
    // Same ribbon, different fire: see ROUTE_GLOW_PROFILE.
    if (routeGlowUniforms) {
      const profile = ROUTE_GLOW_PROFILE[isDay ? 'day' : 'night'];
      routeGlowUniforms.uCoreWhite.value = profile.coreWhite;
      routeGlowUniforms.uBody.value = profile.body;
      routeGlowUniforms.uBodyFall.value = profile.bodyFall;
      routeGlowUniforms.uTopEdge.value = profile.topEdge;
      routeGlowUniforms.uBaseEdge.value = profile.baseEdge;
      routeGlowUniforms.uInk.value = profile.ink;
    }
  }

  // ---------------------------------------------------------------- frame

  function update(dt, camera) {
    const now = Date.now();
    tick(now);
    if (!ready) return;

    // The landmark glow formula (kit.js updateLandmarkGlow): near-invisible
    // by day, ignited at night — the first vehicle in the app to use it.
    const nightOpacity = Math.min(1, 0.12 + (shared.uNight.value ?? 0) * 0.95);
    for (const f of fleets) {
      if (f.glowMesh) f.glowMesh.material.opacity = nightOpacity;
      f.count = 0;
    }

    // Route glow walls: rebuild when the active route set changes, and
    // modulate opacity by day/night. An active route is always drawn — a
    // curtain against the daylight, a vivid beam once the city goes dark.
    if (routeGlowDirty) {
      rebuildRouteGlow();
      routeGlowDirty = false;
    }
    if (routeGlowMesh) {
      // Slow pulse: 0.75-1.0 brightness factor over ~4 seconds.
      const pulse = 0.75 + 0.25 * Math.sin(now * 0.0015);
      const night = shared.uNight.value ?? 0;
      setRouteGlowDay(night < ROUTE_GLOW_NIGHT_AT);
      const baseOpacity = routeGlowIsDay ? ROUTE_GLOW_DAY_OPACITY : nightOpacity * ROUTE_GLOW_NIGHT_OPACITY;
      routeGlowMesh.material.opacity = baseOpacity * pulse;
    }

    const camQ = camera.quaternion;
    const camX = camera.position.x;
    const camZ = camera.position.z;
    let badgeCount = 0;
    let eligible = 0;
    // Camera height stands in for zoom: the rig is pitch-locked, so height and
    // orbit distance move together and this needs no extra plumbing.
    const camY = camera.position.y;
    const zoomRadius = Math.max(BADGE_RADIUS_MIN, Math.min(BADGE_RADIUS_MAX, camY * BADGE_RADIUS_PER_M));

    for (const state of buses.values()) {
      if (now - state.lastFixAt > STALE_MS) {
        state.index = -1;
        continue;
      }

      // In the scene only while the data says this vehicle is working: parked
      // in a yard, waiting out a layover before its first trip, or off its own
      // alignment -> it sinks under the street (the tunnel idiom) and rises
      // again the moment it reports movement.
      state.hidden = hiddenReason(state);
      state.hide = Math.max(0, Math.min(1, state.hide + (state.hidden ? dt : -dt) / HIDE_FADE_S));
      if (state.hide >= 1) {
        state.index = -1;
        continue;
      }

      // Speed easing: decelerate hard into dwells, pull away gently, and only
      // ever overspeed a little to close a gap (the acceptance bar's "catches
      // up gently rather than lurching").
      const accel = state.targetSpeed < state.speed ? DECEL : ACCEL;
      state.speed += Math.sign(state.targetSpeed - state.speed) * Math.min(accel * dt, Math.abs(state.targetSpeed - state.speed));

      if (state.shapeIdx >= 0) {
        // Spend the banked distance to the latest fix's projection, never
        // overrunning it by more than a bus length, and only overspeeding a
        // little while well behind — "catches up gently, never lurches".
        let lead = state.targetS - state.s;
        // Dead-reckon: if the bus has reached its projected target but was
        // still moving at the last fresh fix, extrapolate the target forward
        // along the shape so the bus keeps driving instead of freezing. This
        // is what keeps buses moving between ~90 s fixes and on CDN cache
        // hits — without it, the bus reaches targetS, lead hits zero, and
        // the advance clamp freezes it in place. Capped at DEAD_RECKON_MAX_S
        // seconds since the last fresh fix (ferries use the same pattern).
        const extra = deadReckonAdvance({
          lead,
          targetSpeed: state.targetSpeed,
          sinceFreshS: (now - state.lastFreshFixAt) / 1000,
          provisional: state.provisional,
          targetS: state.targetS,
          provisionalCap: state.provisionalCap,
          dt,
        });
        if (extra > 0) {
          state.targetS += extra;
          lead = state.targetS - state.s;
        }
        const boost = lead > 200 ? CATCHUP_FACTOR : 1;
        const advance = Math.min(Math.max(0, lead + 12), state.speed * boost * dt);
        state.s += advance;
        shapes.sample(state.shapeIdx, state.s, state.sample);
        state.x = state.sample.x;
        state.z = state.sample.z;
        const turn = shortestAngle(state.yaw, state.sample.yaw);
        state.yaw += Math.sign(turn) * Math.min(Math.abs(turn), HEADING_EASE * dt * (1 + state.speed * 0.2));
      } else {
        // Dead reckoning, ferry-style, for the rare off-shape bus.
        const run = state.speed * dt;
        state.x += Math.sin(state.deadYaw ?? 0) * run;
        state.z += Math.cos(state.deadYaw ?? 0) * run;
        const catchUp = Math.min(1, dt / 3);
        state.x += (state.fixX - state.x) * catchUp * 0.2;
        state.z += (state.fixZ - state.z) * catchUp * 0.2;
        if (state.deadYaw != null) {
          const turn = shortestAngle(state.yaw, state.deadYaw);
          state.yaw += Math.sign(turn) * Math.min(Math.abs(turn), HEADING_EASE * dt);
        }
      }

      const f = state.fleet || fleets[0];
      if (f.count >= CAPACITY) { state.index = -1; continue; }

      // In tunnel? Ease it under the street across the portal and stop drawing
      // once it is wholly below. The road is opaque, so the descent reads as
      // entering the tunnel rather than as a vehicle winking out — and while it
      // is under, it costs nothing to draw.
      let sink = state.hide * f.sinkM;
      if (shapes && state.shapeIdx >= 0 && TUNNELS[String(state.route).toUpperCase()]) {
        const depth = tunnelDepth(undergroundFor(state.shapeIdx, state.route), state.s);
        if (depth >= 1) { state.index = -1; continue; }
        sink = Math.max(sink, depth * f.sinkM);
      }

      state.index = f.count;
      const y = data.sampleElevation ? data.sampleElevation(state.x, state.z) : 0;

      dummy.position.set(state.x, y + 0.35 - sink, state.z);
      dummy.rotation.set(0, state.yaw + Math.PI, 0); // model front is -Z; +Z is travel after the flip
      dummy.scale.setScalar(f.scale);
      dummy.updateMatrix();
      f.bodyMesh.setMatrixAt(f.count, dummy.matrix);
      if (f.glowMesh) f.glowMesh.setMatrixAt(f.count, dummy.matrix);

      // Badge: a speech bubble billboarded to the camera, only for buses close
      // enough to be worth calling out. Counted separately from the body so a
      // skipped bubble costs an instance rather than leaving a hole.
      const dist = Math.hypot(state.x - camX, state.z - camZ);
      const near = badgeRadius * 0.72; // fade over the outer quarter of the ring
      // A bubble left hovering over the street while its train is on the way
      // down reads as a label pinned to nothing, so it goes at the portal.
      if (dist < badgeRadius && sink === 0) {
        eligible++;
        if (badgeCount < MAX_BADGES) {
          const fade = dist < near ? 1 : Math.max(0, 1 - (dist - near) / Math.max(1, badgeRadius - near));
          const rect = atlas.rect(state.route);
          // Proportional to THIS bubble's distance => constant size on screen,
          // which is the whole point: a bubble 6 km away is drawn 6 km-sized.
          const scaleAt = Math.max(BADGE_SCALE_MIN, Math.min(BADGE_SCALE_MAX, dist / BADGE_REF_DIST));
          // Pin the TIP, derive the centre: the bubble scales, the point it
          // aims with does not drift up off the roof.
          dummy.position.set(state.x, y + BADGE_TIP_Y + BADGE_TAIL_DROP * scaleAt, state.z);
          dummy.quaternion.copy(camQ);
          dummy.scale.setScalar(scaleAt * fade);
          dummy.updateMatrix();
          badge.mesh.setMatrixAt(badgeCount, dummy.matrix);
          badge.uvRect.setXYZW(badgeCount, rect[0], rect[1], rect[2], rect[3]);
          badgeCount++;
        }
      }

      f.count++;
    }

    for (const f of fleets) {
      f.bodyMesh.count = f.count;
      f.bodyMesh.instanceMatrix.needsUpdate = true;
      if (f.glowMesh) {
        f.glowMesh.count = f.count;
        f.glowMesh.instanceMatrix.needsUpdate = true;
      }
    }
    badge.mesh.count = badgeCount;
    badge.mesh.instanceMatrix.needsUpdate = true;
    badge.uvRect.needsUpdate = true;

    // Breathe the radius toward whatever keeps roughly MAX_BADGES on screen,
    // bounded by what the current zoom allows.
    const target = eligible > MAX_BADGES ? badgeRadius * 0.94 : badgeRadius * 1.06;
    badgeRadius = Math.max(140, Math.min(zoomRadius, badgeRadius + (target - badgeRadius) * Math.min(1, dt * 1.5)));
  }

  // ------------------------------------------------------------- entities

  function entityFor(state) {
    const routeName = shapes?.routeName(state.route);
    const headsign = shapes?.headsign(state.tripId, state.route, state.directionId);
    const modeLabel = state.mode === 'cable' ? 'Cable Car' : state.mode === 'streetcar' ? 'Streetcar' : state.mode === 'lrv' ? 'Muni Metro' : state.mode === 'trolley' ? 'Trolley' : 'Bus';
    return {
      kind: 'transit',
      id: state.id,
      title: routeName ? `${state.route} ${routeName}` : `Route ${state.route}`,
      name: `${modeLabel} ${state.fleetNumber}`,
      mode: state.mode || 'bus',
      x: state.x,
      z: state.z,
      route: state.route,
      routeName,
      destination: headsign,
      fleetNumber: state.fleetNumber,
      occupancy: state.occupancy,
      speedKmh: state.speed * 3.6,
      stops: (state.stops || []).map((stop) => ({
        name: shapes?.stopName(stop.stopId) ?? `Stop ${stop.stopId}`,
        arrivalAt: stop.arrivalAt,
      })),
      onShape: state.shapeIdx >= 0,
      recordedAt: state.recordedAt,
      demo,
      degraded,
      source: demo ? 'demo' : '511 GTFS-RT',
      confidence: 3,
    };
  }

  // The ROUTE BUBBLE is clickable, not just the vehicle under it — and the
  // tolerance grows with range. A fixed 16 m radius is most of a bus at street
  // level and less than a pixel from the air, while the bubble overhead is drawn
  // at a constant size ON SCREEN. So from the altitude this camera actually
  // lives at, the one thing plainly visible and worth aiming at was the one
  // thing the pick ignored, and clicking it selected whatever was behind it.
  function pickBus(origin, direction) {
    if (!ready) return null;
    let best = null;
    const now = Date.now();
    for (const state of buses.values()) {
      if (state.index < 0 || now - state.lastFixAt > STALE_MS) continue;
      const px = state.x - origin.x;
      const pz = state.z - origin.z;
      const flat = Math.hypot(px, pz);
      const radius = Math.max(PICK_RADIUS, flat * PICK_ANGLE);
      const ground = data.sampleElevation ? data.sampleElevation(state.x, state.z) : 0;
      const scaleAt = Math.max(BADGE_SCALE_MIN, Math.min(BADGE_SCALE_MAX, flat / BADGE_REF_DIST));
      // The same two numbers the badge loop draws with, so the bubble you can
      // see is the bubble you can hit.
      for (const hy of [4, ground + BADGE_TIP_Y + BADGE_TAIL_DROP * scaleAt]) {
        const py = hy - origin.y;
        const t = px * direction.x + py * direction.y + pz * direction.z;
        if (t <= 0 || t > MAX_PICK_DISTANCE) continue;
        const away = Math.hypot(px - direction.x * t, py - direction.y * t, pz - direction.z * t);
        if (away > radius || (best && t >= best.distance)) continue;
        best = { ...entityFor(state), distance: t };
      }
    }
    return best;
  }

  function busEntity(id) {
    const state = buses.get(id);
    return state && state.index >= 0 ? entityFor(state) : null;
  }

  return {
    update,
    pickBus,
    busEntity,
    /** Live arrivals at a stop, soonest first — [] when nothing is predicted. */
    arrivalsAt(stopId) {
      return arrivalsByStop.get(String(stopId)) || [];
    },
    get live() {
      return live;
    },
    get degraded() {
      return degraded;
    },
    get demo() {
      return demo;
    },
    get count() {
      return fleets.reduce((sum, f) => sum + f.count, 0);
    },
    get onShapeCount() {
      let n = 0;
      for (const state of buses.values()) if (state.index >= 0 && state.shapeIdx >= 0) n++;
      return n;
    },
    // Bus table for debugging / automated checks.
    get buses() {
      return [...buses.values()].map((state) => ({
        id: state.id,
        mode: state.mode || 'bus',
        route: state.route,
        x: Math.round(state.x),
        z: Math.round(state.z),
        s: Math.round(state.s),
        targetS: Math.round(state.targetS),
        speed: +state.speed.toFixed(1),
        targetSpeed: +state.targetSpeed.toFixed(1),
        onShape: state.shapeIdx >= 0,
        drawn: state.index >= 0,
      }));
    },
    // Detailed diagnostic dump for debugging movement issues. Call
    // SF.muni.debug() from the console and paste the output back.
    debug() {
      const now = Date.now();
      const all = [...buses.values()];
      const summary = {
        total: all.length,
        drawn: all.filter((s) => s.index >= 0).length,
        onShape: all.filter((s) => s.shapeIdx >= 0).length,
        moving: all.filter((s) => s.speed > 0.5).length,
        targetMoving: all.filter((s) => s.targetSpeed > 0.5).length,
        frozen: all.filter((s) => s.index >= 0 && s.speed < 0.5 && s.targetSpeed < 0.5).length,
        // Why the rest aren't drawn — the counts to read when the scene looks
        // emptier or busier than the street does.
        parked: all.filter((s) => s.hidden === 'parked').length,
        layover: all.filter((s) => s.hidden === 'layover').length,
        offRoute: all.filter((s) => s.hidden === 'offRoute').length,
        provisional: all.filter((s) => s.provisional).length,
        predictionsSeen,
        live,
        degraded,
        demo,
        lastFetchedAt: lastFetchedAt ? new Date(lastFetchedAt).toLocaleTimeString() : null,
      };
      const rows = all.slice(0, 20).map((s) => ({
        id: s.id,
        route: s.route,
        mode: s.mode,
        speed: +s.speed.toFixed(1),
        targetSpeed: +s.targetSpeed.toFixed(1),
        s: Math.round(s.s),
        targetS: Math.round(s.targetS),
        lead: Math.round(s.targetS - s.s),
        freshAgeS: Math.round((now - s.lastFreshFixAt) / 1000),
        fixAgeS: Math.round((now - s.lastFixAt) / 1000),
        onShape: s.shapeIdx >= 0,
        drawn: s.index >= 0,
        hidden: s.hidden ?? null,
        stillS: Math.round((s.lastFreshFixAt - s.movedAt) / 1000),
        provisional: !!s.provisional,
        // Distinguishes "in tunnel" from the other reasons a vehicle isn't
        // drawn (stale fix, fleet at capacity).
        inTunnel:
          shapes && s.shapeIdx >= 0 && !!TUNNELS[String(s.route).toUpperCase()]
            ? tunnelDepth(undergroundFor(s.shapeIdx, s.route), s.s) >= 1
            : false,
        deadReckon: s.shapeIdx >= 0 && s.targetS - s.s < DWELL_STEP_M && s.targetSpeed > 0,
      }));
      console.log('=== SF.muni.debug ===');
      console.log('summary:', summary);
      console.table(rows);
      return { summary, rows };
    },
  };
}
