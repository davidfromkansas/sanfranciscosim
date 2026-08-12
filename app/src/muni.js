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
const DWELL_SPEED = 0.7; // m/s reported below this counts as dwelling
const DECEL = 3.2; // m/s^2 easing into a stop (~2 s from cruise)
const ACCEL = 1.4; // m/s^2 pulling away
const CATCHUP_FACTOR = 1.3; // max overspeed while closing a gap to the fix
const MAX_SPEED = 20; // m/s hard cap (45 mph); transit never exceeds it
const SNAP_LIMIT_M = 150; // a fix further than this off-shape -> dead-reckon
const SNAP_WINDOW_M = 1200; // how far along the shape a projection may jump
const HEADING_EASE = 2.4; // rad/s toward the tangent

// Badges: cream route pills over each roof, one instanced quad layer fed by a
// lazily-grown canvas atlas (a draw call per route would be ~40 calls).
const BADGE_COLS = 8;
const BADGE_ROWS = 16;
const BADGE_W = 9; // metres on screen-facing quad
const BADGE_H = 4.5;
const BADGE_Y = 12; // metres above the street (roof is ~5.5 m at 1.6x)
const BADGE_NEAR = 2000; // full opacity inside this camera distance...
const BADGE_FAR = 4000; // ...gone past this

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

  rect(route) {
    let slot = this.slots.get(route);
    if (slot) return slot;
    const index = this.slots.size;
    if (index >= BADGE_COLS * BADGE_ROWS) return [0, 0, 0, 0];
    const cw = this.canvas.width / BADGE_COLS;
    const ch = this.canvas.height / BADGE_ROWS;
    const x = (index % BADGE_COLS) * cw;
    const y = Math.floor(index / BADGE_COLS) * ch;

    const ctx = this.ctx;
    const pad = 6;
    const r = 16;
    const bx = x + pad;
    const by = y + pad;
    const bw = cw - pad * 2;
    const bh = ch - pad * 2;
    ctx.clearRect(x, y, cw, ch);
    // Hard offset shadow first, then the pill, then the border — the press-down
    // physicality the HUD cards use, at diorama scale.
    ctx.beginPath();
    ctx.roundRect(bx + 4, by + 5, bw - 4, bh - 5, r);
    ctx.fillStyle = 'rgba(58, 53, 48, 0.85)';
    ctx.fill();
    ctx.beginPath();
    ctx.roundRect(bx, by, bw - 4, bh - 5, r);
    ctx.fillStyle = '#f7f1e3';
    ctx.fill();
    ctx.lineWidth = 3;
    ctx.strokeStyle = '#3a3530';
    ctx.stroke();
    ctx.fillStyle = '#3a3530';
    ctx.font = `700 ${route.length > 2 ? 34 : 40}px ui-rounded, -apple-system, system-ui, sans-serif`;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(route, bx + (bw - 4) / 2, by + (bh - 5) / 2 + 2);

    slot = [x / this.canvas.width, 1 - (y + ch) / this.canvas.height, cw / this.canvas.width, ch / this.canvas.height];
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

  function apply(list, now) {
    for (const state of buses.values()) state.seen = false;

    for (const bus of list) {
      if (bus.mode !== 'bus') continue; // other modes wait for their models
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
          misses: 0,
          seen: true,
          index: -1,
          sample: { x, z, yaw: 0, end: 0 },
        };
        placeOnShape(state, true);
        buses.set(bus.id, state);
        continue;
      }

      const gap = Math.max(1, (now - state.lastFixAt) / 1000);
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

      // The speed the follower should hold to arrive at the new projection in
      // about one fix gap, informed by the reported speed. A reported crawl or
      // an unmoved projection means dwell — target zero and STOP (the "stopped
      // means stopped" rule); the distance stays banked in targetS and is paid
      // out when the bus reports moving again.
      const reported = Number.isFinite(bus.speedMs) ? bus.speedMs : null;
      const fixStep = Math.hypot(x - prevFixX, z - prevFixZ);
      const dwelling = (reported != null && reported < DWELL_SPEED) || (reported == null && fixStep < 8);
      if (state.shapeIdx >= 0) {
        const gapS = Math.max(0, state.targetS - state.s);
        state.targetSpeed = dwelling ? 0 : Math.min(MAX_SPEED, Math.max(reported ?? 0, gapS / gap) );
      } else {
        state.targetSpeed = dwelling ? 0 : Math.min(MAX_SPEED, reported ?? fixStep / gap);
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
    apply(payload.vehicles, now);
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
        const lead = state.targetS - state.s;
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

      // Badge: billboarded to the camera, faded by distance, atlas cell by route.
      const dist = Math.hypot(state.x - camX, state.z - camZ);
      const fade = dist < BADGE_NEAR ? 1 : dist > BADGE_FAR ? 0 : 1 - (dist - BADGE_NEAR) / (BADGE_FAR - BADGE_NEAR);
      const rect = atlas.rect(state.route);
      dummy.position.set(state.x, y + BADGE_Y, state.z);
      dummy.quaternion.copy(camQ);
      const badgeScale = fade > 0 ? 1 + dist / 2600 : 0; // grow a little with distance so pills stay legible
      dummy.scale.setScalar(badgeScale * fade);
      dummy.updateMatrix();
      badge.mesh.setMatrixAt(count, dummy.matrix);
      badge.uvRect.setXYZW(count, rect[0], rect[1], rect[2], rect[3]);

      count++;
      if (count >= CAPACITY) break;
    }

    bodyMesh.count = count;
    bodyMesh.instanceMatrix.needsUpdate = true;
    if (glowMesh) {
      glowMesh.count = count;
      glowMesh.instanceMatrix.needsUpdate = true;
    }
    badge.mesh.count = count;
    badge.mesh.instanceMatrix.needsUpdate = true;
    badge.uvRect.needsUpdate = true;
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
