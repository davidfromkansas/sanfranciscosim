// Muni bus-stop markers: the clickable layer over the real stops.
//
// The shelters themselves are street furniture placed by the tile worker
// (streetplan.js) at the GTFS coordinates in munistops.js. This layer adds the
// two things furniture cannot do: a hovering marker that makes a stop findable
// and clickable from the diorama camera, and the pick that opens its card.
//
// Density follows the same rule the bus route badges settled on, because it is
// the same problem an order of magnitude worse — there are 2,976 stops against
// a few hundred buses. Markers are drawn only near the camera, capped in number,
// and scaled by their own distance so they hold a constant size on screen. The
// radius breathes: it tightens where stops crowd together and relaxes where
// they thin out.
//
// Draw calls: one instanced quad layer, whatever the fleet of stops.

import {
  CanvasTexture,
  DynamicDrawUsage,
  InstancedMesh,
  MeshBasicMaterial,
  Object3D,
  PlaneGeometry,
  SRGBColorSpace,
} from 'three';

import { loadBusStops, compareRoute } from './munistops.js';

const MARKER_W = 6.6;
const MARKER_H = 6.6;
// Metres above the pavement. This does NOT shrink with the marker: a pin has to
// clear the shelter roof, the street trees and the parked cars whatever size it
// is drawn at, and at street level a low one vanishes into the canyon.
const MARKER_Y = 11;

// Stops are static and dense, so these run tighter than the bus badges.
const RADIUS_MIN = 220;
const RADIUS_MAX = 2400;
const RADIUS_PER_M = 0.85; // radius per metre of camera height
const REF_DIST = 300; // distance at which a marker draws at its authored size
const SCALE_MIN = 1.0;
const SCALE_MAX = 16;
const MAX_MARKERS = 26;

const PICK_RADIUS = 11;
const MAX_PICK_DISTANCE = 4000;

const dummy = new Object3D();

// One marker icon for every stop, so no atlas is needed — a roundel in the toy
// UI voice (cream card stock, warm-ink border, hard offset shadow) with the
// bus-front glyph the cards already use for transit.
function markerTexture() {
  const canvas = document.createElement('canvas');
  canvas.width = 128;
  canvas.height = 128;
  const ctx = canvas.getContext('2d');
  const cx = 64;
  const cy = 56;
  const r = 40;

  ctx.beginPath();
  ctx.arc(cx + 3, cy + 5, r, 0, Math.PI * 2);
  ctx.fillStyle = 'rgba(28, 24, 20, 0.34)';
  ctx.fill();

  // Pin body: circle plus a tail dropping onto the stop itself.
  ctx.beginPath();
  ctx.arc(cx, cy, r, Math.PI * 0.18, Math.PI * 0.82, true);
  ctx.lineTo(cx, 122);
  ctx.closePath();
  ctx.fillStyle = '#fbf7ee';
  ctx.fill();
  ctx.lineWidth = 5;
  ctx.lineJoin = 'round';
  ctx.strokeStyle = '#3a3530';
  ctx.stroke();

  // Bus glyph.
  ctx.strokeStyle = '#c1272d';
  ctx.lineWidth = 5;
  ctx.lineCap = 'round';
  ctx.strokeRect(cx - 17, cy - 20, 34, 30);
  ctx.beginPath();
  ctx.moveTo(cx - 17, cy - 3);
  ctx.lineTo(cx + 17, cy - 3);
  ctx.stroke();
  ctx.fillStyle = '#3a3530';
  ctx.beginPath();
  ctx.arc(cx - 10, cy + 5, 3, 0, Math.PI * 2);
  ctx.arc(cx + 10, cy + 5, 3, 0, Math.PI * 2);
  ctx.fill();

  const texture = new CanvasTexture(canvas);
  texture.colorSpace = SRGBColorSpace;
  return texture;
}

export function createMuniStopLayer(scene, data, muni) {
  let table = null;
  let mesh = null;
  let radius = RADIUS_MAX;
  // Stops drawn this frame, so a pick tests only what is on screen.
  let visible = [];

  loadBusStops().then((t) => {
    table = t;
    if (!t.stops.length) return;
    mesh = new InstancedMesh(
      new PlaneGeometry(MARKER_W, MARKER_H),
      new MeshBasicMaterial({
        map: markerTexture(),
        transparent: true,
        depthWrite: false,
        alphaTest: 0.02,
        // Pins, not geometry: a marker hidden behind the building on the near
        // side of the street is a marker you can neither find nor click, which
        // is the whole job. Only ~26 are ever on screen, so floating them above
        // the city costs nothing in clutter.
        depthTest: false,
      }),
      MAX_MARKERS,
    );
    mesh.name = 'muni-stop-markers';
    mesh.instanceMatrix.setUsage(DynamicDrawUsage);
    mesh.frustumCulled = false;
    mesh.renderOrder = 4;
    mesh.count = 0;
    scene.add(mesh);
  });

  // `pivot` is what the viewer is LOOKING AT, and that is what proximity has to
  // mean here. Gating on the camera's own position looks equivalent and is not:
  // the rig sits ~200 m back from its pivot on an 18-degree lens, so the stops
  // nearest the camera are behind and beside the view while the ones actually on
  // screen get culled. Measured before this fix: all four drawn markers
  // projected to NDC x of 3 to 44 — every one off-screen.
  function update(dt, camera, pivot) {
    if (!mesh || !table) return;
    const camX = pivot ? pivot.x : camera.position.x;
    const camZ = pivot ? pivot.z : camera.position.z;
    const camY = camera.position.y;
    const camQ = camera.quaternion;
    const zoomRadius = Math.max(RADIUS_MIN, Math.min(RADIUS_MAX, camY * RADIUS_PER_M));

    let count = 0;
    let eligible = 0;
    visible = [];
    for (const stop of table.stops) {
      const dist = Math.hypot(stop.x - camX, stop.z - camZ);
      if (dist > radius) continue;
      eligible++;
      if (count >= MAX_MARKERS) continue;
      const y = data.sampleElevation ? data.sampleElevation(stop.x, stop.z) : 0;
      const scale = Math.max(SCALE_MIN, Math.min(SCALE_MAX, dist / REF_DIST));
      dummy.position.set(stop.x, y + MARKER_Y, stop.z);
      dummy.quaternion.copy(camQ);
      dummy.scale.setScalar(scale);
      dummy.updateMatrix();
      mesh.setMatrixAt(count, dummy.matrix);
      visible.push(stop);
      count++;
    }
    mesh.count = count;
    mesh.instanceMatrix.needsUpdate = true;

    const target = eligible > MAX_MARKERS ? radius * 0.94 : radius * 1.06;
    radius = Math.max(120, Math.min(zoomRadius, radius + (target - radius) * Math.min(1, dt * 1.5)));
  }

  // Upcoming buses at a stop, grouped by route — the shape the card wants:
  // "38R in 4, 11 min" rather than a flat list of vehicles.
  function arrivalsByRoute(stop) {
    const now = Date.now();
    const groups = new Map();
    for (const a of muni?.arrivalsAt?.(stop.id) || []) {
      let g = groups.get(a.route);
      if (!g) groups.set(a.route, (g = { route: a.route, minutes: [] }));
      if (g.minutes.length < 3) g.minutes.push(Math.max(0, Math.round((a.at - now) / 60000)));
    }
    return [...groups.values()].sort((a, b) => compareRoute(a.route, b.route));
  }

  function entityFor(stop) {
    return {
      kind: 'transit-stop',
      id: `stop:${stop.id}`,
      stopId: stop.id,
      title: stop.name,
      name: stop.name,
      x: stop.x,
      z: stop.z,
      // Every route that calls here, from the GTFS bake — true whether or not
      // anything is due, which a live-arrivals list alone could never say.
      routes: stop.routes,
      arrivals: arrivalsByRoute(stop),
      source: 'sfmta',
      confidence: 3,
    };
  }

  function pickStop(origin, direction) {
    // Unlike the draw gate above, this one is genuinely camera-relative: it is
    // testing a ray that starts at the camera.
    let best = null;
    for (const stop of visible) {
      const y = data.sampleElevation ? data.sampleElevation(stop.x, stop.z) : 0;
      const px = stop.x - origin.x;
      const py = y + 3 - origin.y;
      const pz = stop.z - origin.z;
      const t = px * direction.x + py * direction.y + pz * direction.z;
      if (t <= 0 || t > MAX_PICK_DISTANCE) continue;
      // Pick radius grows with distance so a marker stays as easy to hit as it
      // looks — it is drawn at constant screen size, so its target should match.
      const reach = PICK_RADIUS * Math.max(1, t / REF_DIST);
      const away = Math.hypot(px - direction.x * t, py - direction.y * t, pz - direction.z * t);
      if (away > reach || (best && t >= best.distance)) continue;
      best = { ...entityFor(stop), distance: t };
    }
    return best;
  }

  function stopEntity(id) {
    const stop = table?.byId.get(String(id).replace(/^stop:/, ''));
    return stop ? entityFor(stop) : null;
  }

  return {
    update,
    pickStop,
    stopEntity,
    get count() {
      return mesh ? mesh.count : 0;
    },
    get total() {
      return table ? table.stops.length : 0;
    },
  };
}
