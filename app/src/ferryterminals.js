// Ferry terminal markers: the clickable layer over the berths boats actually
// tie up at, baked by pipeline/ferry-shapes.mjs.
//
// "Actually" is the bake's job, not this layer's: a berth no scheduled trip
// calls at is dropped there (owner decision, 2026-08-17), so everything that
// arrives here has service.
//
// This is the bus-stop layer's problem two orders of magnitude smaller — fourteen
// berths in the water plane against 2,976 bus stops — so almost none of
// munistoplayer.js's machinery is needed here. No declutter grid, no view-cell
// competition, no altitude ceiling: fourteen markers never crowd a frame, and a
// ferry terminal is a place worth seeing from the hero view, which is exactly
// the argument that made a bus stop's pin disappear above 1,050 m.
//
// What IS shared, because it was learned the hard way over there: gate on what
// the camera is LOOKING AT rather than where it is, scale off camera distance so
// a marker holds its size on screen, and pick against the quad as drawn rather
// than against the terminal's ground position.
//
// Draw calls: one instanced quad layer.

import {
  CanvasTexture,
  DynamicDrawUsage,
  InstancedMesh,
  MeshBasicMaterial,
  Object3D,
  PlaneGeometry,
  SRGBColorSpace,
} from 'three';

import { loadFerryNetwork } from './ferrynetwork.js';

const MARKER_W = 8.4;
const MARKER_H = 8.4;
// Metres above the water. A berth sits at the end of a pier among sheds and
// gangways, so the pin has to clear them at any drawn size.
const MARKER_Y = 13;

// Distance at which a marker draws at its authored size; apparent size is
// MARKER_W / REF_DIST, so this pair is the on-screen size dial.
const REF_DIST = 240;
const SCALE_MIN = 1.0;
// The hero view sits ~8 km out and the Bay terminals are further still, so this
// needs more headroom than the street-level layers.
const SCALE_MAX = 46;

const MAX_PICK_DISTANCE = 20000;

// Rule 2: every visual subsystem exposes a lever. Markers are never zeroed —
// the fog-bank regression is the standing lesson that a `low: 0` reads exactly
// like a deleted feature — so the low tier thins the set to the busiest berths
// instead of switching the layer off.
const QUALITY_CAP = { high: 16, medium: 16, low: 6 };

const PIN_TEX = 256;
const dummy = new Object3D();

// The pin: a toy-theme cream card with a warm-ink border and a hard offset
// shadow (no blur — the UI theme forbids gradients and soft shadows), carrying a
// ferry silhouette. Drawn procedurally rather than loaded, because there is no
// ferry glyph in sf-assets/ and a missing file would be a silent feature
// deletion of exactly the kind app/test/asset-loading.test.mjs exists to stop.
function markerTexture() {
  const canvas = document.createElement('canvas');
  canvas.width = canvas.height = PIN_TEX;
  const ctx = canvas.getContext('2d');
  const s = PIN_TEX / 256;

  const x = 26 * s;
  const y = 20 * s;
  const w = 204 * s;
  const h = 150 * s;
  const r = 34 * s;

  // Hard offset shadow first, so the card sits on top of it.
  ctx.fillStyle = 'rgba(58, 42, 30, 0.55)';
  card(ctx, x + 7 * s, y + 8 * s, w, h, r, s);
  ctx.fill();

  ctx.fillStyle = '#f6ecd8';
  ctx.strokeStyle = '#3a2a1e';
  ctx.lineWidth = 7 * s;
  card(ctx, x, y, w, h, r, s);
  ctx.fill();
  ctx.stroke();

  boat(ctx, PIN_TEX / 2, y + h * 0.47, 108 * s);

  const texture = new CanvasTexture(canvas);
  texture.colorSpace = SRGBColorSpace;
  texture.anisotropy = 4;
  return texture;
}

// Rounded card with a tail hanging off the bottom edge, pointing at the berth.
function card(ctx, x, y, w, h, r, s) {
  const right = x + w;
  const bottom = y + h;
  const cx = x + w / 2;
  const tail = 30 * s;
  ctx.beginPath();
  ctx.moveTo(x + r, y);
  ctx.lineTo(right - r, y);
  ctx.quadraticCurveTo(right, y, right, y + r);
  ctx.lineTo(right, bottom - r);
  ctx.quadraticCurveTo(right, bottom, right - r, bottom);
  ctx.lineTo(cx + tail * 0.62, bottom);
  ctx.lineTo(cx, bottom + tail);
  ctx.lineTo(cx - tail * 0.62, bottom);
  ctx.lineTo(x + r, bottom);
  ctx.quadraticCurveTo(x, bottom, x, bottom - r);
  ctx.lineTo(x, y + r);
  ctx.quadraticCurveTo(x, y, x + r, y);
  ctx.closePath();
}

// A ferry read from above the waterline: hull, deckhouse, funnel. Semantic
// exaggeration per the style bible — this is a 40-pixel glyph at hero altitude,
// so the silhouette carries it, not the detail.
function boat(ctx, cx, cy, width) {
  const u = width / 100;
  ctx.fillStyle = '#3a2a1e';
  ctx.beginPath();
  // Hull: flat deck, raked bow to the right, transom to the left.
  ctx.moveTo(cx - 46 * u, cy + 4 * u);
  ctx.lineTo(cx + 30 * u, cy + 4 * u);
  ctx.quadraticCurveTo(cx + 50 * u, cy + 4 * u, cx + 46 * u, cy + 16 * u);
  ctx.lineTo(cx - 40 * u, cy + 16 * u);
  ctx.quadraticCurveTo(cx - 48 * u, cy + 16 * u, cx - 46 * u, cy + 4 * u);
  ctx.closePath();
  ctx.fill();
  // Deckhouse.
  ctx.fillRect(cx - 30 * u, cy - 14 * u, 56 * u, 16 * u);
  // Funnel, raked back.
  ctx.beginPath();
  ctx.moveTo(cx - 6 * u, cy - 14 * u);
  ctx.lineTo(cx + 2 * u, cy - 32 * u);
  ctx.lineTo(cx + 12 * u, cy - 32 * u);
  ctx.lineTo(cx + 10 * u, cy - 14 * u);
  ctx.closePath();
  ctx.fill();
}

export function createFerryTerminals(scene, data, ferries) {
  let network = null;
  let berths = [];
  let mesh = null;
  let cap = QUALITY_CAP.high;
  // Markers drawn this frame, so a pick tests only what is on screen.
  let visible = [];

  loadFerryNetwork().then((n) => {
    if (!n) return; // rule 3: no bake, no terminals, city unaffected.
    network = n;
    berths = n.berths.filter((b) => b.inScene);
    if (!berths.length) return;
    mesh = new InstancedMesh(
      new PlaneGeometry(MARKER_W, MARKER_H),
      new MeshBasicMaterial({
        map: markerTexture(),
        transparent: true,
        depthWrite: false,
        alphaTest: 0.02,
        // A marker hidden behind a pier shed is one you can neither find nor
        // click, which is the whole job of this layer.
        depthTest: false,
      }),
      QUALITY_CAP.high,
    );
    mesh.name = 'ferry-terminal-markers';
    mesh.instanceMatrix.setUsage(DynamicDrawUsage);
    // Every whole-city instanced object in this repo gets this: batch bounds
    // cover the reserved buffer and cull on-screen content otherwise. This bug
    // has shipped twice (kitfleet.js, assets.js).
    mesh.frustumCulled = false;
    mesh.renderOrder = 4;
    mesh.count = 0;
    scene.add(mesh);
  });

  function setQuality(tier) {
    cap = QUALITY_CAP[tier] ?? QUALITY_CAP.high;
  }

  // `pivot` is what the viewer is looking at; the rig sits back from it on a
  // narrow lens, so gating on the camera's own position shows the berths behind
  // the view instead of the ones on screen (measured in munistoplayer.js).
  function update(dt, camera, pivot) {
    if (!mesh || !berths.length) return;
    const camX = pivot ? pivot.x : camera.position.x;
    const camZ = pivot ? pivot.z : camera.position.z;
    const camQ = camera.quaternion;

    // Nearest what the viewer is looking at first, so the low tier's cap trims
    // the far side of the Bay rather than whatever sorted last.
    const ranked = berths
      .map((berth) => ({ berth, d2: (berth.x - camX) ** 2 + (berth.z - camZ) ** 2 }))
      .sort((a, b) => a.d2 - b.d2);

    let count = 0;
    visible = [];
    for (const { berth } of ranked) {
      if (count >= cap) break;
      // A berth is at the water's edge; the pier deck is above the waterline and
      // the terrain sample can dip below it, so never seat a pin under the Bay.
      const y = Math.max(0, data.sampleElevation ? data.sampleElevation(berth.x, berth.z) : 0);
      const camDist = Math.hypot(
        berth.x - camera.position.x,
        berth.z - camera.position.z,
        y - camera.position.y
      );
      const scale = Math.max(SCALE_MIN, Math.min(SCALE_MAX, camDist / REF_DIST));
      const markerY = y + MARKER_Y * Math.max(1, scale * 0.35);
      dummy.position.set(berth.x, markerY, berth.z);
      dummy.quaternion.copy(camQ);
      dummy.scale.setScalar(scale);
      dummy.updateMatrix();
      mesh.setMatrixAt(count, dummy.matrix);
      // Where the pin was actually drawn and how big: the pick reads these so
      // the hit target is the art on screen and cannot drift from it.
      visible.push({ berth, y, markerY, scale });
      count++;
    }
    mesh.count = count;
    mesh.instanceMatrix.needsUpdate = true;
  }

  // Boats currently working a route that calls at this berth. The live fleet is
  // the only thing that can say "there is a boat on its way"; the baked routes
  // say what calls here at all, which is true even when nothing is sailing.
  function vesselsFor(berth) {
    const out = [];
    for (const vessel of ferries?.liveEntities?.() || []) {
      const bound = vessel.next?.name || vessel.destination || null;
      const from = vessel.origin?.name || null;
      if (!bound && !from) continue;
      if (bound === berth.name || from === berth.name) {
        out.push({
          label: vessel.label,
          routeName: vessel.routeName,
          arrivingAt: bound === berth.name ? vessel.next?.arrivalAt ?? null : null,
        });
      }
    }
    return out;
  }

  function entityFor(berth) {
    const routes = berth.routes.map((id) => {
      const route = network?.routes.get(id);
      return { id, name: route?.name || id, color: route?.color || null };
    });
    return {
      kind: 'ferry-terminal',
      id: `ferry-terminal:${berth.id}`,
      terminalId: berth.id,
      title: berth.name,
      name: berth.name,
      x: berth.x,
      z: berth.z,
      // Every route that calls here, from the GTFS bake — true whether or not a
      // boat is sailing right now, which a live-vessel list alone cannot say.
      routes,
      stops: berth.stops,
      operators: berth.operators,
      operatorNames: berth.operatorNames || [],
      vessels: vesselsFor(berth),
      source: 'weta',
      confidence: 3,
    };
  }

  // Distance from a ray to a point; null behind the camera or past the reach.
  function rayHit(origin, direction, x, y, z, reach) {
    const px = x - origin.x;
    const py = y - origin.y;
    const pz = z - origin.z;
    const t = px * direction.x + py * direction.y + pz * direction.z;
    if (t <= 0 || t > MAX_PICK_DISTANCE) return null;
    const away = Math.hypot(px - direction.x * t, py - direction.y * t, pz - direction.z * t);
    return away > reach ? null : t;
  }

  // The pin as drawn is the target — its centre and its own half-width at the
  // size it was drawn, not the berth's position on the water.
  function pickTerminal(origin, direction) {
    let best = null;
    for (const { berth, markerY, scale } of visible) {
      const t = rayHit(origin, direction, berth.x, markerY, berth.z, (MARKER_W / 2) * scale);
      if (t === null || (best && t >= best.distance)) continue;
      best = { ...entityFor(berth), distance: t };
    }
    return best;
  }

  function terminalEntity(id) {
    const key = String(id).replace(/^ferry-terminal:/, '');
    const berth = berths.find((b) => b.id === key);
    return berth ? entityFor(berth) : null;
  }

  return {
    update,
    setQuality,
    pickTerminal,
    terminalEntity,
    // Names of every berth inside the water plane — for automated checks and
    // for answering "is Sausalito on the map" without a pick.
    berthNames() {
      return berths.map((b) => b.name);
    },
    get count() {
      return mesh ? mesh.count : 0;
    },
    get total() {
      return berths.length;
    },
  };
}
