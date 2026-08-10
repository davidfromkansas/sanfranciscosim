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
  BufferAttribute,
  DynamicDrawUsage,
  InstancedMesh,
  MeshBasicMaterial,
  MeshLambertMaterial,
  Object3D,
  PlaneGeometry,
  Vector2,
} from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { mergeGeometries } from 'three/addons/utils/BufferGeometryUtils.js';

const ASSET = `${import.meta.env.BASE_URL}sf-assets/vehicles/SF_Bay_Ferry.glb`;
const MANIFEST = `${import.meta.env.BASE_URL}sf-assets/vehicles_manifest.json`;

const CAPACITY = 24;
const POLL_MS = 60 * 1000;
const POLL_JITTER_MS = 5 * 1000;
const DEMO_POLL_MS = 20 * 1000;
// Cap on how far a stale fix may be extrapolated forward.
const DEAD_RECKON_MAX_S = 90;
const STALE_MS = 10 * 60 * 1000;
// Two misses in a row is enough to call a vessel gone without flickering it out
// on a single truncated response.
const MISSES_TO_DROP = 2;
const MAX_SPEED = 13; // m/s — a Gemini-class boat tops out around 25 kn.
const EASE_S = 2.5; // seconds to absorb a position correction
const HEADING_EASE = 1.6; // rad/s cap on turn rate
const MOVING_M = 100; // movement between polls that counts as "underway"
const IDLE_SPEED = 0.4; // m/s below which heading is held instead of derived
const FALLBACK_AFTER_MS = 5 * 60 * 1000; // empty-but-live grace before falling back

// The Bay is modelled by a single 30 km x 30 km water plane centred on the
// projection origin (app/src/water.js), i.e. x/z in [-15000, +15000]; the baked
// city tiles cover far less. Vallejo (x +15.6 km, z -36.5 km) is well outside
// it, so northbound boats sail off-scene and get culled instead of floating
// over void. A 500 m inset keeps a hull from straddling the water edge.
const SCENE_HALF_EXTENT = 15000 - 500;

// Compass bearing (deg clockwise from true north) to scene yaw. The asset's
// front is -Z and the scene has -z = north, +x = east, so a boat's yaw is just
// the negated bearing:
//   bearing   0 (north) -> yaw  0    -> front points -z  ✔
//   bearing  90 (east)  -> yaw -pi/2 -> front points +x  ✔
//   bearing 180 (south) -> yaw  pi   -> front points +z  ✔
//   bearing 270 (west)  -> yaw  pi/2 -> front points -x  ✔
function bearingToYaw(bearingDeg) {
  return -(bearingDeg * Math.PI) / 180;
}

// The SB feed sends Bearing 0 for every vessel it has no heading for — docked
// boats and, at times, boats under way — so an exact 0 is treated as unknown
// and the heading is derived from movement instead. A genuinely north-bound
// boat loses nothing: its motion vector points north too.
function usableBearing(bearingDeg) {
  return bearingDeg != null && bearingDeg !== 0;
}

// Heading from a movement vector in scene space, same convention as above.
function motionToYaw(dx, dz) {
  return Math.atan2(-dx, -dz);
}

function shortestAngle(from, to) {
  let d = (to - from) % (Math.PI * 2);
  if (d > Math.PI) d -= Math.PI * 2;
  if (d < -Math.PI) d += Math.PI * 2;
  return d;
}

// Merge the GLB into one geometry per surface class, baking material colour
// (times any authored vertex colour) into COLOR_0 — the same idiom the landmark
// and vehicle loaders use, so the fleet renders with one Lambert material.
function mergeFerry(root) {
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

// Three synthetic vessels for ?ferries=demo: a normal Oakland loop, an Alameda
// loop that stops reporting (exercising stale removal) and a Vallejo run that
// reports no bearing and sails north off-scene (heading derivation + culling).
const DEMO_ROUTES = [
  {
    id: 'DEMO:Oakland',
    label: 'Hydrus (demo)',
    routeName: 'Oakland',
    originName: 'Oakland Ferry Terminal',
    destination: 'San Francisco Ferry Building Gate B',
    bearings: true,
    stopsAfterMs: Infinity,
    legs: [
      [-122.3931, 37.7955],
      [-122.3505, 37.7955],
      [-122.3341, 37.7955],
    ],
  },
  {
    id: 'DEMO:Alameda',
    label: 'Pyxis (demo)',
    routeName: 'Alameda Seaplane',
    originName: 'San Francisco Ferry Building Gate F',
    destination: 'Alameda Seaplane Lagoon',
    bearings: true,
    stopsAfterMs: 100 * 1000,
    legs: [
      [-122.3931, 37.7948],
      [-122.3720, 37.7855],
      [-122.3416, 37.7823],
    ],
  },
  {
    id: 'DEMO:Vallejo',
    label: 'Vela (demo)',
    routeName: 'Vallejo',
    originName: null, // exercises the "unknown origin" card copy
    destination: 'Vallejo Ferry Terminal',
    bearings: false, // heading must be derived from movement
    stopsAfterMs: Infinity,
    legs: [
      [-122.3931, 37.7960],
      [-122.3700, 37.8300],
      [-122.3200, 37.9200],
      [-122.2600, 38.1000], // off-scene: culled, not floated over void
    ],
  },
];

// Module-scope scratch: the update loop and the picker must not allocate.
const dummy = new Object3D();
const scratch = new Vector2();
// Pick radius around a hull's centre, in metres: a little wider than the boat so
// a click near it from the aerial camera still lands.
const PICK_RADIUS = 34;
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

  function setFallback(fallback) {
    if (live === !fallback) return;
    live = !fallback;
    agents?.setProceduralFerriesVisible?.(fallback);
  }

  async function load() {
    let entry = null;
    try {
      const res = await fetch(MANIFEST);
      if (res.ok) {
        entry = ((await res.json()).vehicles || []).find((v) => v.kind === 'ferry') || null;
      }
    } catch {
      entry = null;
    }

    let merged;
    try {
      const gltf = await new GLTFLoader().loadAsync(entry ? `${import.meta.env.BASE_URL}sf-assets/${entry.file}` : ASSET);
      merged = mergeFerry(gltf.scene);
    } catch (error) {
      console.warn(`sf-ferries: ferry model failed to load (${error.message}) — keeping procedural ferries`);
      return;
    }
    if (!merged.body) {
      console.warn('sf-ferries: ferry model had no geometry — keeping procedural ferries');
      return;
    }

    // Never trust the file's own scale: measure and scale to the manifest length.
    merged.body.computeBoundingBox();
    const measured = merged.body.boundingBox.max.z - merged.body.boundingBox.min.z;
    const target = entry?.targetLengthM ?? entry?.dims?.[2] ?? measured;
    scale = measured > 0 ? target / measured : 1;

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
      const [x, z] = data.project(vessel.lon, vessel.lat);
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
          lastFixAt: now,
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

      const dx = x - state.targetX;
      const dz = z - state.targetZ;
      const step = Math.hypot(dx, dz);
      const gap = Math.max(1, (now - state.lastFixAt) / 1000);
      state.prevX = state.targetX;
      state.prevZ = state.targetZ;
      state.targetX = x;
      state.targetZ = z;
      state.moved = step;
      state.fixGap = gap;
      state.speed = Math.min(MAX_SPEED, Math.max(0, step / gap));
      state.lastFixAt = now;
      state.inService = vessel.inService;
      state.label = vessel.label;
      state.routeName = vessel.routeName ?? null;
      state.destination = vessel.destination ?? null;
      state.origin = vessel.origin ?? null;
      state.next = vessel.next ?? null;
      state.recordedAt = vessel.recordedAt ?? now;
      state.seen = true;

      if (usableBearing(vessel.bearingDeg)) {
        state.targetYaw = bearingToYaw(vessel.bearingDeg);
      } else if (state.speed > IDLE_SPEED) {
        state.targetYaw = motionToYaw(dx, dz);
      }
      // else: a docked boat with no bearing keeps the heading it had, so it
      // never spins on the spot.
    }

    for (const [id, state] of vessels) {
      if (state.seen) {
        state.misses = 0;
        continue;
      }
      state.misses = (state.misses || 0) + 1;
      if (state.misses >= MISSES_TO_DROP || now - state.lastFixAt > STALE_MS) {
        vessels.delete(id);
      }
    }
  }

  function renderable(state, now) {
    if (now - state.lastFixAt > STALE_MS) return false;
    if (!inScene(state.x, state.z) && !inScene(state.targetX, state.targetZ)) return false;
    // Out-of-service boats only count if they are actually going somewhere.
    return state.inService || state.moved > MOVING_M;
  }

  function demoFixes(now) {
    const elapsed = now - demoStart;
    const list = [];
    for (const route of DEMO_ROUTES) {
      if (elapsed > route.stopsAfterMs) continue;
      // 260 s out, 260 s back, so a full leg is walked in either direction.
      const cycle = 520 * 1000;
      const t = (elapsed % cycle) / cycle;
      const along = t < 0.5 ? t * 2 : (1 - t) * 2;
      const span = route.legs.length - 1;
      const seg = Math.min(span - 1, Math.floor(along * span));
      const local = along * span - seg;
      const a = route.legs[seg];
      const b = route.legs[seg + 1];
      const lon = a[0] + (b[0] - a[0]) * local;
      const lat = a[1] + (b[1] - a[1]) * local;
      let bearingDeg = null;
      if (route.bearings) {
        const dir = t < 0.5 ? 1 : -1;
        const east = (b[0] - a[0]) * dir;
        const north = (b[1] - a[1]) * dir;
        bearingDeg = ((Math.atan2(east, north) * 180) / Math.PI + 360) % 360;
      }
      list.push({
        id: route.id,
        label: route.label,
        lat,
        lon,
        bearingDeg,
        routeName: route.routeName,
        destination: route.destination,
        inService: true,
        recordedAt: now,
        origin: {
          ref: null,
          name: route.originName,
          departedAt: route.originName ? now - 11 * 60 * 1000 : null,
        },
        next: {
          name: route.destination,
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
      const since = Math.min(DEAD_RECKON_MAX_S, (now - state.lastFixAt) / 1000);
      const run = state.speed > IDLE_SPEED ? state.speed * since : 0;
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
      demo,
      source: demo ? 'demo' : '511',
      confidence: 3,
    };
  }

  // Nearest drawn hull whose centre lies within PICK_RADIUS of the ray. Sphere
  // tests against at most CAPACITY boats, so a click costs nothing measurable
  // and the fleet keeps its single instanced draw call.
  function pickVessel(origin, direction) {
    if (!ready) return null;
    let best = null;
    const now = Date.now();
    for (const state of vessels.values()) {
      if (state.index < 0 || !renderable(state, now)) continue;
      const px = state.x - origin.x;
      const py = 6 - origin.y; // roughly the deckhouse, not the waterline
      const pz = state.z - origin.z;
      const t = px * direction.x + py * direction.y + pz * direction.z;
      if (t <= 0 || t > MAX_PICK_DISTANCE) continue;
      const away = Math.hypot(px - direction.x * t, py - direction.y * t, pz - direction.z * t);
      if (away > PICK_RADIUS || (best && t >= best.distance)) continue;
      best = { ...entityFor(state), distance: t };
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
