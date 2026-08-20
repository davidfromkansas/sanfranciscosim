// Live San Francisco Bay Ferry vessels.
//
// /api/ferries proxies 511.org's SIRI feed for agency SB (WETA); every vessel
// underway shows up here as the hand-made ferry GLB at its real position,
// dead-reckoned between the ~60 s fixes so nothing ever teleports. Without a
// key, without vessels, or on any fetch failure the two looping procedural
// ferries in agents.js come back — the Bay is never empty.
//
// Draw calls: one instanced body (+ one glow set if the asset has any) and one
// wake, so the whole live fleet costs at most three.

import {
  DynamicDrawUsage,
  InstancedMesh,
  MeshBasicMaterial,
  MeshLambertMaterial,
  Object3D,
  PlaneGeometry,
  Vector2,
} from 'three';
import { loadFerryNetwork } from './ferrynetwork.js';
import { loadFerryHull } from './ferryhull.js';
// The badge layer owns where a route bubble floats; the pick has to agree with
// it, so the height comes from there rather than from a second copy here.
import { badgeHeightAt } from './ferrybadges.js';
// Motion, freshness and scene-tenure rules live in one tested module — see its
// header before changing anything about whether a vessel moves or stays.
import {
  MAX_SPEED,
  bearingToYaw,
  deadReckonRun,
  deadReckonSeconds,
  headingFor,
  isFreshFix,
  shouldDrop,
  shouldRender,
  targetSpeedFor,
  usableBearing,
} from './ferry-motion.js';

const CAPACITY = 24;
const POLL_MS = 60 * 1000;
const POLL_JITTER_MS = 5 * 1000;
const DEMO_POLL_MS = 20 * 1000;
const EASE_S = 2.5; // seconds to absorb a position correction
const HEADING_EASE = 1.6; // rad/s cap on turn rate
const FALLBACK_AFTER_MS = 5 * 60 * 1000; // empty-but-live grace before falling back
// Dwell, speed, dead-reckon and staleness thresholds live in ferry-motion.js.

// The Bay is modelled by a single 30 km x 30 km water plane centred on the
// projection origin (app/src/water.js), i.e. x/z in [-15000, +15000]; the baked
// city tiles cover far less. Vallejo (x +15.6 km, z -36.5 km) is well outside
// it, so northbound boats sail off-scene and get culled instead of floating
// over void. A 500 m inset keeps a hull from straddling the water edge.
const SCENE_HALF_EXTENT = 15000 - 500;

function shortestAngle(from, to) {
  let d = (to - from) % (Math.PI * 2);
  if (d > Math.PI) d -= Math.PI * 2;
  if (d < -Math.PI) d += Math.PI * 2;
  return d;
}

// Three synthetic vessels for ?ferries=demo, each sailing a REAL route shape
// from the bake rather than invented waypoints.
//
// The first version of this listed hand-typed legs — the Oakland boat ran along
// a constant latitude, a dead-straight line across the Bay — which was fine when
// nothing else was drawn on the water. Now that the route walls trace the
// published alignments, a demo boat on an invented path visibly ignores them,
// which makes the preview misleading exactly where it is used to judge the work.
//
// Each spec still exercises what it was written to exercise: a published
// bearing versus one derived from motion, a vessel that stops reporting (stale
// removal), and one that sails off the edge of the water plane (culling).
const DEMO_SPECS = [
  {
    id: 'DEMO:Oakland',
    label: 'Hydrus (demo)',
    route: 'SB:OA',
    routeName: 'Oakland & Alameda',
    originName: 'Oakland Ferry Terminal',
    destination: 'San Francisco Ferry Building',
    bearings: true,
    stopsAfterMs: Infinity,
    startFrac: 0.1,
  },
  {
    id: 'DEMO:Seaplane',
    label: 'Pyxis (demo)',
    route: 'SB:SEA',
    routeName: 'Alameda Seaplane',
    originName: 'San Francisco Ferry Building',
    destination: 'Alameda Seaplane Lagoon Ferry Terminal',
    bearings: true,
    // Stops reporting, so stale removal is exercised.
    stopsAfterMs: 100 * 1000,
    startFrac: 0.35,
  },
  {
    id: 'DEMO:Vallejo',
    label: 'Vela (demo)',
    route: 'SB:VJO',
    routeName: 'Vallejo',
    originName: null, // exercises the "unknown origin" card copy
    destination: 'Vallejo Ferry Terminal',
    bearings: false, // heading must be derived from movement
    stopsAfterMs: Infinity,
    // Measured against the bake, not guessed: this shape runs Vallejo -> SF and
    // only its last 12 km (arc 34.6 km of 46.8 km) is inside the 30 km water
    // plane. 0.62 put the boat 5 km outside it, invisible for the first several
    // minutes. 0.78 starts it just inside, sailing in — and the return leg
    // still takes it back out, which is the culling path this spec exists for.
    startFrac: 0.78,
  },
];

// Realistic hull speed for the stand-ins, so they read like the real fleet
// rather than skating across the Bay.
const DEMO_SPEED_MS = 12;
// Module-scope scratch: the update loop and the picker must not allocate.
const dummy = new Object3D();
const scratch = new Vector2();
// Pick radius around a hull's centre, in metres: a little wider than the boat so
// a click near it from the aerial camera still lands.
const PICK_RADIUS = 34;
// Angular slack, matching muni.js and population.js: ~2.2 m per 100 m of range,
// so a tag keeps a roughly constant click target the way it keeps a constant
// drawn size.
const PICK_ANGLE = 0.022;
const MAX_PICK_DISTANCE = 9000;

export function createLiveFerries(scene, data, agents) {
  const params = new URLSearchParams(window.location.search);
  const demo = params.get('ferries') === 'demo';

  // Bounded vessel table: at most CAPACITY entries survive a poll, and drawn
  // instances are packed from 0 each frame so a removal is a swap-with-last.
  const vessels = new Map(); // id -> state

  let bodyMesh = null;
  let glowMesh = null;
  let wakeMesh = null;
  let scale = 1;
  let ready = false;
  let disposed = false;

  let live = false;
  let lastVesselAt = 0;
  let nextPollAt = 0;
  let polling = false;
  let warnedFetch = false;
  let demoStart = 0;
  // The baked route shapes the demo vessels sail along (demo mode only).
  let demoNetwork = null;

  function setFallback(fallback) {
    if (live === !fallback) return;
    live = !fallback;
    agents?.setProceduralFerriesVisible?.(fallback);
  }

  if (demo) {
    loadFerryNetwork().then((n) => {
      demoNetwork = n;
      if (!n) console.warn('sf-ferries: ?ferries=demo needs the route bake — no shapes, no demo boats');
    });
  }

  async function load() {
    const hull = await loadFerryHull();
    if (!hull) {
      console.warn('sf-ferries: no ferry model — keeping procedural ferries');
      return;
    }
    const merged = { body: hull.body, glow: hull.glow };
    scale = hull.scale;

    bodyMesh = new InstancedMesh(merged.body, new MeshLambertMaterial({ vertexColors: true }), CAPACITY);
    bodyMesh.name = 'live-ferry-fleet';
    if (merged.glow) {
      glowMesh = new InstancedMesh(
        merged.glow,
        new MeshBasicMaterial({ vertexColors: true }),
        CAPACITY
      );
      glowMesh.name = 'live-ferry-glow';
    }
    wakeMesh = new InstancedMesh(
      new PlaneGeometry(1, 1),
      new MeshBasicMaterial({ color: '#dfeaf0', transparent: true, opacity: 0.28, depthWrite: false }),
      CAPACITY
    );
    wakeMesh.name = 'live-ferry-wake';
    wakeMesh.renderOrder = 3;

    for (const mesh of [bodyMesh, glowMesh, wakeMesh]) {
      if (!mesh) continue;
      mesh.instanceMatrix.setUsage(DynamicDrawUsage);
      mesh.frustumCulled = false;
      mesh.castShadow = false;
      mesh.count = 0;
      scene.add(mesh);
    }
    ready = true;
  }

  function inScene(x, z) {
    return Math.abs(x) <= SCENE_HALF_EXTENT && Math.abs(z) <= SCENE_HALF_EXTENT;
  }

  function apply(list, now) {
    for (const state of vessels.values()) state.seen = false;

    for (const vessel of list) {
      // Demo fixes arrive already in scene space (they are read straight off
      // the baked shapes); live ones arrive as lon/lat and are projected here.
      const [x, z] =
        vessel.x != null && vessel.z != null
          ? [vessel.x, vessel.z]
          : data.project(vessel.lon, vessel.lat);
      let state = vessels.get(vessel.id);
      if (!state) {
        // WETA runs ~15 boats; the table is capped anyway so a runaway feed
        // cannot grow it without bound.
        if (vessels.size >= CAPACITY) continue;
        state = {
          id: vessel.id,
          label: vessel.label,
          x,
          z,
          targetX: x,
          targetZ: z,
          prevX: x,
          prevZ: z,
          yaw: usableBearing(vessel.bearingDeg) ? bearingToYaw(vessel.bearingDeg) : 0,
          targetYaw: usableBearing(vessel.bearingDeg) ? bearingToYaw(vessel.bearingDeg) : 0,
          speed: 0,
          bob: Math.random() * 6.28,
          // Two clocks, deliberately (invariant 4): lastFixAt = "still exists",
          // lastFreshFixAt = "was last actually located".
          lastFixAt: now,
          lastFreshFixAt: now,
          fixGap: POLL_MS / 1000,
          moved: 0,
          inService: vessel.inService,
          routeName: vessel.routeName ?? null,
          destination: vessel.destination ?? null,
          origin: vessel.origin ?? null,
          next: vessel.next ?? null,
          recordedAt: vessel.recordedAt ?? now,
          seen: true,
          index: -1,
        };
        vessels.set(vessel.id, state);
        continue;
      }

      // A repeated payload proves the vessel still exists but carries no new
      // position (invariant 4). Bump liveness and refresh the card metadata,
      // then leave position, speed, heading and the dead-reckon clock alone:
      // reading a repeat as "it did not move" is what froze the fleet mid-Bay.
      const fresh = isFreshFix(state.recordedAt, vessel.recordedAt);
      state.lastFixAt = now;
      state.seen = true;
      state.inService = vessel.inService;
      state.label = vessel.label;
      state.routeName = vessel.routeName ?? null;
      state.destination = vessel.destination ?? null;
      state.origin = vessel.origin ?? null;
      state.next = vessel.next ?? null;
      if (!fresh) continue;

      const dx = x - state.targetX;
      const dz = z - state.targetZ;
      const step = Math.hypot(dx, dz);
      // Measured fresh-fix to fresh-fix (invariant 2): timing this from the
      // last poll instead would shrink the gap on every repeat and inflate the
      // speed of a boat that had simply been waiting for real data.
      const gap = Math.max(1, (now - state.lastFreshFixAt) / 1000);
      state.prevX = state.targetX;
      state.prevZ = state.targetZ;
      state.targetX = x;
      state.targetZ = z;
      state.moved = step;
      state.fixGap = gap;
      state.speed = targetSpeedFor({ fixStep: step, gapSeconds: gap });
      state.lastFreshFixAt = now;
      state.recordedAt = vessel.recordedAt ?? now;

      // null = keep the heading it had, so a docked boat never spins on the spot.
      const yaw = headingFor({ bearingDeg: vessel.bearingDeg, speed: state.speed, dx, dz });
      if (yaw != null) state.targetYaw = yaw;
    }

    for (const [id, state] of vessels) {
      if (state.seen) {
        state.misses = 0;
        continue;
      }
      state.misses = (state.misses || 0) + 1;
      if (shouldDrop(state, now)) vessels.delete(id);
    }
  }

  function renderable(state, now) {
    return shouldRender(
      {
        lastFixAt: state.lastFixAt,
        inService: state.inService,
        moved: state.moved,
        inScene: inScene(state.x, state.z) || inScene(state.targetX, state.targetZ),
      },
      now
    );
  }

  // Position along a baked shape at a given arc length, in SCENE coordinates.
  // Returns the point and the direction of travel there.
  function alongShape(shape, metres) {
    const F = demoNetwork.verts;
    const base = shape.vertexOffset * 3;
    const last = shape.vertexCount - 1;
    const target = Math.max(0, Math.min(shape.lengthM, metres));
    for (let i = 0; i < last; i++) {
      const o = base + i * 3;
      const q = o + 3;
      const s0 = F[o + 2];
      const s1 = F[q + 2];
      if (target > s1 && i < last - 1) continue;
      const span = Math.max(1e-6, s1 - s0);
      const t = Math.max(0, Math.min(1, (target - s0) / span));
      const x = F[o] + (F[q] - F[o]) * t;
      const z = F[o + 1] + (F[q + 1] - F[o + 1]) * t;
      return { x, z, dx: F[q] - F[o], dz: F[q + 1] - F[o + 1] };
    }
    return { x: F[base], z: F[base + 1], dx: 1, dz: 0 };
  }

  // Compass bearing (deg cw from north) for a scene-space direction. The
  // inverse of motionToYaw's convention in ferry-motion.js: -z is north.
  function directionToBearing(dx, dz) {
    return ((Math.atan2(dx, -dz) * 180) / Math.PI + 360) % 360;
  }

  function demoFixes(now) {
    if (!demoNetwork) return []; // shapes not in yet; boats appear a beat later
    const elapsed = now - demoStart;
    const list = [];
    for (const spec of DEMO_SPECS) {
      if (elapsed > spec.stopsAfterMs) continue;
      const route = demoNetwork.routes.get(spec.route);
      if (!route) continue;
      // Longest shape, the same one the wall for this route is drawn from, so
      // the boat and its lane cannot disagree.
      let shapeIdx = null;
      for (const idx of route.shapes) {
        const shape = demoNetwork.shapes[idx];
        if (!shape) continue;
        if (shapeIdx === null || shape.lengthM > demoNetwork.shapes[shapeIdx].lengthM) shapeIdx = idx;
      }
      const shape = demoNetwork.shapes[shapeIdx];
      if (!shape || !shape.lengthM) continue;

      // Ping-pong along the route at a constant speed, so a leg is walked in
      // both directions and the heading logic sees a reversal.
      const run = shape.lengthM;
      const travelled = spec.startFrac * run + (elapsed / 1000) * DEMO_SPEED_MS;
      const cycle = travelled % (run * 2);
      const outbound = cycle <= run;
      const metres = outbound ? cycle : run * 2 - cycle;
      const point = alongShape(shape, metres);
      const dx = outbound ? point.dx : -point.dx;
      const dz = outbound ? point.dz : -point.dz;

      list.push({
        id: spec.id,
        label: spec.label,
        // Scene coordinates straight from the bake — no projection needed, and
        // deliberately no INVERSE projection invented (AGENTS: one projection
        // function, never re-derived).
        x: point.x,
        z: point.z,
        bearingDeg: spec.bearings ? directionToBearing(dx, dz) : null,
        routeName: spec.routeName,
        destination: spec.destination,
        inService: true,
        recordedAt: now,
        origin: {
          ref: null,
          name: spec.originName,
          departedAt: spec.originName ? now - 11 * 60 * 1000 : null,
        },
        next: {
          name: spec.destination,
          arrivalAt: now + 7 * 60 * 1000,
          scheduledArrivalAt: now + 6 * 60 * 1000,
          departureAt: null,
        },
      });
    }
    return list;
  }

  async function poll(now) {
    if (demo) {
      if (!demoStart) demoStart = now;
      apply(demoFixes(now), now);
      lastVesselAt = now;
      setFallback(false);
      return;
    }

    let payload;
    try {
      const res = await fetch('/api/ferries', { headers: { accept: 'application/json' } });
      if (!res.ok) throw new Error(`api ${res.status}`);
      payload = await res.json();
    } catch (error) {
      if (!warnedFetch) {
        warnedFetch = true;
        // Expected in `vite dev`, where no functions run.
        console.warn(`sf-ferries: /api/ferries unavailable (${error.message}) — procedural ferries stay`);
      }
      setFallback(true);
      return;
    }

    if (!payload?.live || !Array.isArray(payload.vessels)) {
      setFallback(true);
      vessels.clear();
      return;
    }

    apply(payload.vessels, now);
    let visible = 0;
    for (const state of vessels.values()) if (renderable(state, now)) visible++;
    if (visible > 0) lastVesselAt = now;
    // A live feed that reports nothing for five minutes (night, or the whole
    // fleet tied up) hands the Bay back to the procedural ferries.
    setFallback(!(visible > 0 || now - lastVesselAt < FALLBACK_AFTER_MS));
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
    // Regaining focus refreshes immediately: a hidden tab's fixes are stale.
    if (!document.hidden) nextPollAt = 0;
  });

  setFallback(true);
  load();

  function update(dt) {
    if (disposed) return;
    const now = Date.now();
    tick(now);
    if (!ready) return;

    let count = 0;
    for (const state of vessels.values()) {
      // Dead-reckon the last fix forward along its course, then ease the drawn
      // position towards that estimate: corrections are absorbed over a couple
      // of seconds, so a boat never teleports when a new fix lands.
      // Extrapolate from the last FRESH fix, never the last poll: bumping this
      // clock on a repeat made the boat under-run its own course, because a fix
      // that was already 90 s old got treated as brand new.
      const since = deadReckonSeconds({ now, lastFreshFixAt: state.lastFreshFixAt });
      const run = deadReckonRun({ speed: state.speed, sinceFreshS: since });
      const predictedX = state.targetX - Math.sin(state.targetYaw) * run;
      const predictedZ = state.targetZ - Math.cos(state.targetYaw) * run;
      const catchUp = Math.min(1, dt / EASE_S);
      state.x += (predictedX - state.x) * catchUp;
      state.z += (predictedZ - state.z) * catchUp;

      const turn = shortestAngle(state.yaw, state.targetYaw);
      state.yaw += Math.sign(turn) * Math.min(Math.abs(turn), HEADING_EASE * dt);

      if (!renderable(state, now)) {
        state.index = -1;
        continue;
      }
      state.index = count;

      state.bob += dt * 1.6;
      dummy.position.set(state.x, Math.sin(state.bob) * 0.18, state.z);
      dummy.rotation.set(Math.sin(state.bob * 0.7) * 0.012, state.yaw, Math.cos(state.bob) * 0.012);
      dummy.scale.setScalar(scale);
      dummy.updateMatrix();
      bodyMesh.setMatrixAt(count, dummy.matrix);
      if (glowMesh) glowMesh.setMatrixAt(count, dummy.matrix);

      // Wake trails astern, longer the faster the boat is running.
      const wakeLength = 40 + (state.speed / MAX_SPEED) * 110;
      scratch.set(-Math.sin(state.yaw), -Math.cos(state.yaw));
      dummy.position.set(
        state.x - scratch.x * wakeLength * 0.5,
        0.25,
        state.z - scratch.y * wakeLength * 0.5
      );
      dummy.rotation.set(-Math.PI / 2, 0, -Math.atan2(scratch.x, scratch.y));
      dummy.scale.set(12, wakeLength, 1);
      dummy.updateMatrix();
      wakeMesh.setMatrixAt(count, dummy.matrix);

      count++;
      if (count >= CAPACITY) break;
    }

    bodyMesh.count = count;
    bodyMesh.instanceMatrix.needsUpdate = true;
    if (glowMesh) {
      glowMesh.count = count;
      glowMesh.instanceMatrix.needsUpdate = true;
    }
    wakeMesh.count = count;
    wakeMesh.instanceMatrix.needsUpdate = true;
  }

  // A drawn vessel as a pickable entity, in the same shape the context cards and
  // the focus overlay already consume. Times come straight from the feed and stay
  // null when 511 does not publish them — the card says so rather than guessing.
  function entityFor(state) {
    return {
      kind: 'vessel',
      id: state.id,
      title: state.label,
      name: state.label,
      x: state.x,
      z: state.z,
      routeName: state.routeName,
      destination: state.destination,
      origin: state.origin ?? null,
      next: state.next ?? null,
      speedKn: state.speed * 1.94384,
      inService: state.inService,
      recordedAt: state.recordedAt ?? state.lastFixAt,
      // Whether this vessel has an instance on screen right now, so the badge
      // layer labels only hulls that are actually drawn.
      drawn: state.index >= 0,
      demo,
      source: demo ? 'demo' : '511',
      confidence: 3,
    };
  }

  // Nearest drawn hull whose centre lies within PICK_RADIUS of the ray. Sphere
  // tests against at most CAPACITY boats, so a click costs nothing measurable
  // and the fleet keeps its single instanced draw call.
  // Hull OR route badge, with tolerance that grows with range — see the note on
  // pickBus in muni.js. From the air a 34 m boat is a speck while its badge is
  // drawn at a constant size on screen, so the badge is what a viewer actually
  // aims at and it has to be what answers.
  function pickVessel(origin, direction) {
    if (!ready) return null;
    let best = null;
    const now = Date.now();
    for (const state of vessels.values()) {
      if (state.index < 0 || !renderable(state, now)) continue;
      const px = state.x - origin.x;
      const pz = state.z - origin.z;
      const flat = Math.hypot(px, pz);
      const radius = Math.max(PICK_RADIUS, flat * PICK_ANGLE);
      // The badge layer measures its distance from the camera in 3D, including
      // altitude, so this has to match or the badge is picked at a height it is
      // not drawn at.
      const camDist = Math.hypot(px, pz, origin.y);
      for (const hy of [6 /* deckhouse, not waterline */, badgeHeightAt(camDist)]) {
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

  // A drawn vessel by id, so an open selection can follow it as it sails and
  // pick up each new fix. Null once the boat is gone from the feed or the scene.
  function vesselEntity(id) {
    const state = vessels.get(id);
    return state && state.index >= 0 ? entityFor(state) : null;
  }

  return {
    update,
    pickVessel,
    vesselEntity,
    get live() {
      return live;
    },
    get demo() {
      return demo;
    },
    get count() {
      return bodyMesh ? bodyMesh.count : 0;
    },
    // Live vessels in the same entity shape a pick produces. The terminal
    // markers need route, origin and next-call to say "there is a boat inbound",
    // which the debug `vessels` view below deliberately omits.
    liveEntities() {
      return [...vessels.values()].map(entityFor);
    },
    // Vessel table for debugging / automated checks.
    get vessels() {
      return [...vessels.values()].map((state) => ({
        id: state.id,
        label: state.label,
        x: Math.round(state.x),
        z: Math.round(state.z),
        yawDeg: Math.round((state.yaw * 180) / Math.PI),
        speed: Number(state.speed.toFixed(2)),
        inService: state.inService,
        index: state.index,
      }));
    },
    dispose() {
      disposed = true;
      for (const mesh of [bodyMesh, glowMesh, wakeMesh]) {
        if (!mesh) continue;
        scene.remove(mesh);
        mesh.geometry.dispose();
        mesh.material.dispose();
      }
    },
  };
}
