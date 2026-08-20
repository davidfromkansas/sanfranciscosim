// Timetable ferries: boats for the operators that publish no live positions.
//
// Golden Gate, Angel Island–Tiburon and Treasure Island file their timetables
// with 511 and broadcast nothing about where their vessels are (measured: an
// empty feed in BOTH of 511's live formats, while Muni returns 626 vehicles on
// the same call). Their lanes were drawn on the water with no boat that could
// ever appear on them.
//
// So these are drawn from the published timetable: where a boat is SUPPOSED to
// be, moving along its own route at the pace the schedule implies. It is a
// simulation and it is labelled one — the card says "Scheduled", never live,
// and never invents a vessel name. The precedent is the aircraft layer, whose
// altitude is compressed while the card keeps the true number.
//
// Placement logic lives in ferryschedule.js (pure, tested). This module is only
// the drawing: where those positions become hulls on the Bay.
//
// Draw calls: one body (+ one glow set if the model has any) and one wake.

import {
  DynamicDrawUsage,
  InstancedMesh,
  MeshBasicMaterial,
  MeshLambertMaterial,
  Object3D,
  PlaneGeometry,
} from 'three';

import { loadFerryHull } from './ferryhull.js';
import { inScene, loadFerryNetwork } from './ferrynetwork.js';
import { sailingsAt } from './ferryschedule.js';
import { localDayStart } from '../../api/_lib/astro.mjs';

// Ninety-odd sailings run across a whole day, but only a handful overlap at any
// instant. The cap is headroom, not a target.
const CAPACITY = 24;
// The timetable does not change between frames; recomputing it every frame
// would be pure waste. Two seconds is finer than the eye can see at these
// speeds and coarse enough to cost nothing.
const RECOMPUTE_MS = 2000;
// Rule 2. Never zero — a disabled layer and a broken one look identical, which
// is the fog-bank lesson — so low draws fewer boats rather than none.
const QUALITY_CAP = { high: CAPACITY, medium: CAPACITY, low: 6 };

const dummy = new Object3D();

export function createScheduledFerries(scene) {
  let network = null;
  let bodyMesh = null;
  let glowMesh = null;
  let wakeMesh = null;
  let hullScale = 1;
  let cap = QUALITY_CAP.high;
  // When the timetable was last evaluated, on the APP's clock.
  let lastComputeAt = null;
  // What is drawn right now, so a pick tests exactly what is on screen.
  let drawn = [];

  const ready = (async () => {
    const [net, hull] = await Promise.all([loadFerryNetwork(), loadFerryHull()]);
    // rule 3: without either piece there are simply no timetable boats, and the
    // live fleet and the rest of the city are untouched.
    if (!net || !hull || !net.schedule?.trips?.length) return;
    network = net;
    hullScale = hull.scale;

    bodyMesh = new InstancedMesh(hull.body, new MeshLambertMaterial({ vertexColors: true }), CAPACITY);
    bodyMesh.name = 'scheduled-ferry-fleet';
    if (hull.glow) {
      glowMesh = new InstancedMesh(hull.glow, new MeshBasicMaterial({ vertexColors: true }), CAPACITY);
      glowMesh.name = 'scheduled-ferry-glow';
    }
    wakeMesh = new InstancedMesh(
      new PlaneGeometry(1, 1),
      new MeshBasicMaterial({ color: '#dfeaf0', transparent: true, opacity: 0.22, depthWrite: false }),
      CAPACITY
    );
    wakeMesh.name = 'scheduled-ferry-wake';
    wakeMesh.renderOrder = 3;

    for (const mesh of [bodyMesh, glowMesh, wakeMesh]) {
      if (!mesh) continue;
      mesh.instanceMatrix.setUsage(DynamicDrawUsage);
      // Bounds cover the whole Bay; a frustum test on the reserved buffer culls
      // on-screen content (this bug has shipped twice elsewhere in the repo).
      mesh.frustumCulled = false;
      mesh.castShadow = false;
      mesh.count = 0;
      scene.add(mesh);
    }
  })();

  // Scene position at a given arc length along a shape, plus the direction of
  // travel there.
  function pointAt(shapeIdx, metres) {
    const shape = network.shapes[shapeIdx];
    if (!shape) return null;
    const F = network.verts;
    const base = shape.vertexOffset * 3;
    const target = Math.max(0, Math.min(shape.lengthM, metres));
    for (let i = 0; i < shape.vertexCount - 1; i++) {
      const o = base + i * 3;
      const q = o + 3;
      const s1 = F[q + 2];
      if (target > s1 && i < shape.vertexCount - 2) continue;
      const s0 = F[o + 2];
      const span = Math.max(1e-6, s1 - s0);
      const f = Math.max(0, Math.min(1, (target - s0) / span));
      return {
        x: F[o] + (F[q] - F[o]) * f,
        z: F[o + 1] + (F[q + 1] - F[o + 1]) * f,
        dx: F[q] - F[o],
        dz: F[q + 1] - F[o + 1],
      };
    }
    return { x: F[base], z: F[base + 1], dx: 1, dz: 0 };
  }

  function recompute(ms) {
    const sailings = sailingsAt(network.schedule, ms, localDayStart);
    const out = [];
    for (const { trip, metres, seconds } of sailings) {
      const point = pointAt(trip.shape, metres);
      if (!point) continue;
      if (!inScene(point.x, point.z)) continue; // off the water plane: not drawn
      // Heading from a short step along the same shape, so a boat rounding a
      // headland turns with it instead of pointing at its destination.
      // 60 m further along the same shape — far enough to give a stable
      // direction, short enough that a boat rounding a headland turns with it.
      const ahead = pointAt(trip.shape, metres + 60);
      const dx = ahead ? ahead.x - point.x : point.dx;
      const dz = ahead ? ahead.z - point.z : point.dz;
      const route = network.routes.get(trip.route);
      out.push({
        id: `${trip.route}|${trip.legs[0][0]}`,
        x: point.x,
        z: point.z,
        // Scene yaw: the model's front is -Z and -z is north, same convention
        // as the live fleet.
        yaw: Math.atan2(-dx, -dz),
        routeId: trip.route,
        routeName: route?.name || trip.route,
        color: route?.color || null,
        operator: route?.operatorName || null,
        from: trip.from,
        to: trip.to,
        departsAt: trip.legs[0][0],
        arrivesAt: trip.legs[trip.legs.length - 1][0],
        seconds,
      });
    }
    // Nearest the middle of the run first is meaningless here; sort by id so a
    // capped set is stable frame to frame rather than flickering.
    out.sort((a, b) => a.id.localeCompare(b.id));
    drawn = out.slice(0, cap);
  }

  function update(dt, camera, ms) {
    if (!bodyMesh || !network) return;
    const now = ms ?? Date.now();
    // Recompute on ANY jump of the app clock, not just a forward one. SF.setClock
    // can wind time backwards for QA and screenshots, and gating on
    // `now >= nextComputeAt` left the layer frozen showing the old hour's boats
    // — 4 sailings at 3:30 a.m., when nothing runs.
    if (lastComputeAt === null || Math.abs(now - lastComputeAt) >= RECOMPUTE_MS) {
      lastComputeAt = now;
      recompute(now);
    }

    let count = 0;
    for (const boat of drawn) {
      dummy.position.set(boat.x, 0, boat.z);
      dummy.rotation.set(0, boat.yaw, 0);
      dummy.scale.setScalar(hullScale);
      dummy.updateMatrix();
      bodyMesh.setMatrixAt(count, dummy.matrix);
      glowMesh?.setMatrixAt(count, dummy.matrix);
      // A short wake behind the hull, flat on the water.
      dummy.position.set(boat.x, 0.4, boat.z);
      dummy.rotation.set(-Math.PI / 2, 0, -boat.yaw);
      dummy.scale.set(9, 90, 1);
      dummy.updateMatrix();
      wakeMesh.setMatrixAt(count, dummy.matrix);
      count++;
    }
    for (const mesh of [bodyMesh, glowMesh, wakeMesh]) {
      if (!mesh) continue;
      mesh.count = count;
      mesh.instanceMatrix.needsUpdate = true;
    }
  }

  function setQuality(key) {
    cap = QUALITY_CAP[key] ?? QUALITY_CAP.high;
    lastComputeAt = null; // re-slice on the next frame
  }

  const clock = (seconds) => {
    const s = ((seconds % 86400) + 86400) % 86400;
    const h = Math.floor(s / 3600);
    const m = Math.floor((s % 3600) / 60);
    return `${((h + 11) % 12) + 1}:${String(m).padStart(2, '0')} ${h < 12 ? 'am' : 'pm'}`;
  };

  function entityFor(boat) {
    return {
      kind: 'ferry-scheduled',
      id: `ferry-scheduled:${boat.id}`,
      title: boat.routeName,
      name: boat.routeName,
      x: boat.x,
      z: boat.z,
      operator: boat.operator,
      routeName: boat.routeName,
      color: boat.color,
      from: boat.from,
      to: boat.to,
      departs: clock(boat.departsAt),
      arrives: clock(boat.arrivesAt),
      source: 'gtfs-schedule',
      confidence: 2,
    };
  }

  function pickVessel(origin, direction) {
    let best = null;
    for (const boat of drawn) {
      const px = boat.x - origin.x;
      const py = -origin.y;
      const pz = boat.z - origin.z;
      const t = px * direction.x + py * direction.y + pz * direction.z;
      if (t <= 0 || t > 9000) continue;
      const away = Math.hypot(px - direction.x * t, py - direction.y * t, pz - direction.z * t);
      if (away > 34) continue;
      if (best && t >= best.distance) continue;
      best = { ...entityFor(boat), distance: t };
    }
    return best;
  }

  return {
    ready,
    update,
    setQuality,
    pickVessel,
    get count() {
      return bodyMesh ? bodyMesh.count : 0;
    },
    // Timetable boats as entities, for the badge layer and automated checks.
    entities() {
      return drawn.map(entityFor);
    },
  };
}
