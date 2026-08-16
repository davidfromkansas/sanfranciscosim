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
// Draw calls: one instanced body + one glow set + one badge layer = 3.

import {
  BufferAttribute,
  CanvasTexture,
  DynamicDrawUsage,
  InstancedBufferAttribute,
  InstancedMesh,
  MeshBasicMaterial,
  MeshLambertMaterial,
  Object3D,
  PlaneGeometry,
  SRGBColorSpace,
} from 'three';
import { mergeGeometries } from 'three/addons/utils/BufferGeometryUtils.js';

import { createGLTFLoader } from './gltf.js';
import { shared } from './env.js';

const MANIFEST = `${import.meta.env.BASE_URL}sf-assets/vehicles_manifest.json`;
const SHAPES_URL = `${import.meta.env.BASE_URL}tiles/muni-shapes.bin`;
const SHAPES_MAGIC = 0x4d554e31; // 'MUN1'

const CAPACITY = 512;
const POLL_MS = 60 * 1000;
const POLL_JITTER_MS = 5 * 1000;
const DEMO_POLL_MS = 20 * 1000;
const STALE_MS = 3 * 60 * 1000; // no fix for this long -> the bus fades out
const MISSES_TO_DROP = 2;

// The street fleet renders at 1.6x (agents.js carScale); the live buses must
// match it or they read as toys among toys.
const CAR_SCALE = 1.6;

// Movement tuning against the acceptance bar: stopped must read as stopped.
// Displacement across one fix gap below which a bus is standing still. A
// speed READING of 0 means nothing here — see the note in apply().
const DWELL_STEP_M = 14; // ~one 40-foot coach at 1.6x
const DECEL = 3.2; // m/s^2 easing into a stop (~2 s from cruise)
const ACCEL = 1.4; // m/s^2 pulling away
const CATCHUP_FACTOR = 1.3; // max overspeed while closing a gap to the fix
const MAX_SPEED = 20; // m/s hard cap (45 mph); transit never exceeds it
const SNAP_LIMIT_M = 150; // a fix further than this off-shape -> dead-reckon
const SNAP_WINDOW_M = 1200; // how far along the shape a projection may jump
const HEADING_EASE = 2.4; // rad/s toward the tangent
// Cap on how far past the last fresh fix a bus may extrapolate along its
// shape (seconds). The poll interval is 60 s and the server TTL is 90 s, so
// fresh fixes arrive at most ~120 s apart in normal mode; 120 s of dead-reckon
// bridges that gap. Beyond it the bus eases to a stop and waits for real data
// (or drops at STALE_MS). Same pattern as ferries' DEAD_RECKON_MAX_S.
const DEAD_RECKON_MAX_S = 120;

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
// Height of the QUAD CENTRE. The tail tip sits ~0.36 x BADGE_H below centre, so
// this lands the point just above the 5.5 m roof (3.42 m body x 1.6 carScale).
const BADGE_Y = 8.6;
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
// screen.
const BADGE_RADIUS_MAX = 11000;
const BADGE_RADIUS_PER_M = 2.2; // radius per metre of camera height
// Camera distance at which a bubble is drawn at its authored size; scale is
// proportional to distance either side of it, so screen size stays put.
const BADGE_REF_DIST = 420;
const BADGE_SCALE_MIN = 0.85;
// Room to stay legible all the way out to the hero view: at 8000 m a bubble
// needs ~19x its authored size to hold the same size on screen. Capping this
// at 9 was the second reason the high view looked empty — the bubbles were
// there, drawn at half the size they needed, i.e. a few pixels.
const BADGE_SCALE_MAX = 26;
// Hard ceiling on how many shout at once, whatever the radius.
const MAX_BADGES = 18;

const PICK_RADIUS = 16;
const MAX_PICK_DISTANCE = 9000;

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
  let bodyMesh = null;
  let glowMesh = null;
  let badge = null;
  let atlas = null;
  let scale = 1;
  let ready = false;
  let live = false;
  let degraded = false;
  let nextPollAt = 0;
  let polling = false;
  let warnedFetch = false;
  let demoStart = 0;
  let arrivalsByStop = new Map();
  let lastFetchedAt = 0; // server-side fetchedAt of the last non-stale /api/muni payload
  // Adaptive badge radius, within whatever the zoom allows. A dense corridor
  // pulls it in, a quiet neighbourhood lets it back out. O(1) per frame, no
  // sorting, no allocation, and slow enough that bubbles fade rather than blink.
  let badgeRadius = BADGE_RADIUS_MAX;

  async function load() {
    // The shapes bake is an enhancement, not a requirement: without it every
    // bus falls back to straight-line dead reckoning (spec fallback ladder).
    try {
      shapes = await ShapeSet.load();
    } catch (error) {
      shapes = null;
      console.warn(`sf-muni: no route shapes (${error.message}) — buses will dead-reckon`);
    }

    let entry = null;
    try {
      const res = await fetch(MANIFEST);
      if (res.ok) entry = ((await res.json()).vehicles || []).find((v) => v.id === 'muni-bus-40') || null;
    } catch {
      entry = null;
    }
    if (!entry) {
      console.warn('sf-muni: no muni-bus-40 manifest entry — live buses disabled');
      return;
    }

    let merged;
    try {
      const gltf = await createGLTFLoader().loadAsync(`${import.meta.env.BASE_URL}sf-assets/${entry.file}`);
      merged = mergeBus(gltf.scene);
    } catch (error) {
      console.warn(`sf-muni: bus model failed to load (${error.message}) — live buses disabled`);
      return;
    }
    if (!merged.body) {
      console.warn('sf-muni: bus model had no geometry — live buses disabled');
      return;
    }

    merged.body.computeBoundingBox();
    const measured = merged.body.boundingBox.max.z - merged.body.boundingBox.min.z;
    const target = entry.dims?.[2] ?? measured;
    scale = (measured > 0 ? target / measured : 1) * CAR_SCALE;

    bodyMesh = new InstancedMesh(merged.body, new MeshLambertMaterial({ vertexColors: true }), CAPACITY);
    bodyMesh.name = 'live-muni-fleet';
    if (merged.glow) {
      glowMesh = new InstancedMesh(merged.glow, new MeshBasicMaterial({ vertexColors: true, transparent: true }), CAPACITY);
      glowMesh.name = 'live-muni-glow';
    }
    atlas = new BadgeAtlas();
    badge = buildBadgeMesh(atlas);
    for (const mesh of [bodyMesh, glowMesh, badge.mesh]) {
      if (!mesh) continue;
      if (mesh !== badge.mesh) {
        mesh.instanceMatrix.setUsage(DynamicDrawUsage);
        mesh.frustumCulled = false;
        mesh.castShadow = false;
        mesh.count = 0;
      }
      scene.add(mesh);
    }
    ready = true;
  }

  // ---------------------------------------------------------------- fixes

  function apply(list, now, stale) {
    for (const state of buses.values()) state.seen = false;

    for (const bus of list) {
      if (bus.mode !== 'bus') continue; // other modes wait for their models

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
          directionId: bus.directionId,
          tripId: bus.tripId,
          x,
          z,
          yaw: 0,
          // Seeded from the fix, not zero: otherwise every bus stands still for
          // a full poll after it appears, and a page load shows a frozen fleet.
          speed: Number.isFinite(bus.speedMs) ? Math.min(MAX_SPEED, bus.speedMs) : 0,
          targetSpeed: Number.isFinite(bus.speedMs) ? Math.min(MAX_SPEED, bus.speedMs) : 0,
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
          sample: { x, z, yaw: 0, end: 0 },
        };
        placeOnShape(state, true);
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
        }
      }

      // How fast to run so the bus covers the ground it actually covered.
      //
      // DWELL IS A DISPLACEMENT TEST, NOT A SPEED READING. GTFS-RT's `speed` is
      // an instantaneous sample at the fix moment, and 260 of 507 Muni vehicles
      // report exactly 0 at any given instant — every one sitting at a light or
      // a stop when the sample was taken. Reading that as "parked" froze half
      // the fleet on every poll even though those buses had plainly moved
      // hundreds of metres since their previous fix. Only a bus that has not
      // MOVED between two fixes is dwelling; the reported speed merely biases
      // how fast it runs once we know it has.
      const reported = Number.isFinite(bus.speedMs) ? bus.speedMs : null;
      const fixStep = Math.hypot(x - prevFixX, z - prevFixZ);
      if (state.shapeIdx >= 0) {
        const gapS = Math.max(0, state.targetS - state.s);
        // One bus length of slack: less than that across a whole fix gap is
        // genuinely standing still, and the dwell easing takes it to a stop.
        state.targetSpeed = gapS < DWELL_STEP_M ? 0 : Math.min(MAX_SPEED, Math.max(gapS / gap, (reported ?? 0) * 0.6));
      } else {
        state.targetSpeed = fixStep < DWELL_STEP_M ? 0 : Math.min(MAX_SPEED, fixStep / gap);
        state.deadYaw = fixStep > 4 ? Math.atan2(x - prevFixX, z - prevFixZ) : state.deadYaw;
      }
    }

    for (const [id, state] of buses) {
      if (state.seen) {
        state.misses = 0;
        continue;
      }
      state.misses += 1;
      if (state.misses >= MISSES_TO_DROP || now - state.lastFixAt > STALE_MS) buses.delete(id);
    }
  }

  function placeOnShape(state, fresh) {
    state.shapeIdx = shapes ? shapes.resolve(state.tripId, state.route, state.directionId) : -1;
    if (state.shapeIdx < 0) return;
    const hit = shapes.project(state.shapeIdx, state.fixX, state.fixZ, fresh ? null : state.s);
    if (hit.dist > SNAP_LIMIT_M) {
      state.shapeIdx = -1; // genuinely off-route -> dead-reckon this bus
      return;
    }
    state.targetS = hit.s;
    if (fresh || Math.abs(hit.s - state.s) > SNAP_WINDOW_M) state.s = hit.s;
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
    const runs = [
      { id: 'DEMO:8801', route: '38R', dir: 0, speed: 9, offset: 0 },
      { id: 'DEMO:8802', route: '38R', dir: 0, speed: 9, offset: 900 },
      { id: 'DEMO:8632', route: '29', dir: 1, speed: 7, offset: 300 },
      { id: 'DEMO:8641', route: '29', dir: 1, speed: 0, offset: 2200 }, // dwells forever
      { id: 'DEMO:8899', route: '44', dir: 0, speed: 8, offset: 1500 },
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
        mode: 'bus',
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

  // ---------------------------------------------------------------- frame

  function update(dt, camera) {
    const now = Date.now();
    tick(now);
    if (!ready) return;

    // The landmark glow formula (kit.js updateLandmarkGlow): near-invisible
    // by day, ignited at night — the first vehicle in the app to use it.
    const nightOpacity = Math.min(1, 0.12 + (shared.uNight.value ?? 0) * 0.95);
    if (glowMesh) glowMesh.material.opacity = nightOpacity;

    const camQ = camera.quaternion;
    const camX = camera.position.x;
    const camZ = camera.position.z;
    let count = 0;
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
        if (lead < DWELL_STEP_M && state.targetSpeed > 0) {
          const sinceFresh = (now - state.lastFreshFixAt) / 1000;
          if (sinceFresh < DEAD_RECKON_MAX_S) {
            state.targetS += state.targetSpeed * dt;
            lead = state.targetS - state.s;
          }
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

      state.index = count;
      const y = data.sampleElevation ? data.sampleElevation(state.x, state.z) : 0;

      dummy.position.set(state.x, y + 0.35, state.z);
      dummy.rotation.set(0, state.yaw + Math.PI, 0); // model front is -Z; +Z is travel after the flip
      dummy.scale.setScalar(scale);
      dummy.updateMatrix();
      bodyMesh.setMatrixAt(count, dummy.matrix);
      if (glowMesh) glowMesh.setMatrixAt(count, dummy.matrix);

      // Badge: a speech bubble billboarded to the camera, only for buses close
      // enough to be worth calling out. Counted separately from the body so a
      // skipped bubble costs an instance rather than leaving a hole.
      const dist = Math.hypot(state.x - camX, state.z - camZ);
      const near = badgeRadius * 0.72; // fade over the outer quarter of the ring
      if (dist < badgeRadius) {
        eligible++;
        if (badgeCount < MAX_BADGES) {
          const fade = dist < near ? 1 : Math.max(0, 1 - (dist - near) / Math.max(1, badgeRadius - near));
          const rect = atlas.rect(state.route);
          // Proportional to THIS bubble's distance => constant size on screen,
          // which is the whole point: a bubble 6 km away is drawn 6 km-sized.
          const scaleAt = Math.max(BADGE_SCALE_MIN, Math.min(BADGE_SCALE_MAX, dist / BADGE_REF_DIST));
          dummy.position.set(state.x, y + BADGE_Y * scaleAt, state.z);
          dummy.quaternion.copy(camQ);
          dummy.scale.setScalar(scaleAt * fade);
          dummy.updateMatrix();
          badge.mesh.setMatrixAt(badgeCount, dummy.matrix);
          badge.uvRect.setXYZW(badgeCount, rect[0], rect[1], rect[2], rect[3]);
          badgeCount++;
        }
      }

      count++;
      if (count >= CAPACITY) break;
    }

    bodyMesh.count = count;
    bodyMesh.instanceMatrix.needsUpdate = true;
    if (glowMesh) {
      glowMesh.count = count;
      glowMesh.instanceMatrix.needsUpdate = true;
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
    return {
      kind: 'transit',
      id: state.id,
      title: routeName ? `${state.route} ${routeName}` : `Route ${state.route}`,
      name: `Bus ${state.fleetNumber}`,
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

  function pickBus(origin, direction) {
    if (!ready) return null;
    let best = null;
    const now = Date.now();
    for (const state of buses.values()) {
      if (state.index < 0 || now - state.lastFixAt > STALE_MS) continue;
      const px = state.x - origin.x;
      const py = 4 - origin.y;
      const pz = state.z - origin.z;
      const t = px * direction.x + py * direction.y + pz * direction.z;
      if (t <= 0 || t > MAX_PICK_DISTANCE) continue;
      const away = Math.hypot(px - direction.x * t, py - direction.y * t, pz - direction.z * t);
      if (away > PICK_RADIUS || (best && t >= best.distance)) continue;
      best = { ...entityFor(state), distance: t };
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
      return bodyMesh ? bodyMesh.count : 0;
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
  };
}
