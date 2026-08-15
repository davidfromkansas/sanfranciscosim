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

const MARKER_W = 7.4;
const MARKER_H = 7.4;
// Metres above the pavement. This does NOT shrink with the marker: a pin has to
// clear the shelter roof, the street trees and the parked cars whatever size it
// is drawn at, and at street level a low one vanishes into the canyon.
const MARKER_Y = 11;

const RADIUS_MIN = 260;
// Wide enough to cover the ground actually in frame from the hero view: an
// 18-degree lens 5.4 km up sees a few kilometres of city.
const RADIUS_MAX = 4200;
const RADIUS_PER_M = 0.8; // radius per metre of camera height

// CEILING. A stop pin answers "can I catch a bus here" — a question you ask
// standing in a street, not surveying a city. The layer used to have no ceiling
// at all: the search radius simply saturated at RADIUS_MAX, which happens at
// RADIUS_MAX / RADIUS_PER_M = 5,250 m, so pins were still drawn from the hero
// view where a whole neighbourhood is forty pixels wide and a pin says nothing
// about which street it belongs to. Coming down to a fifth of that height is
// where a pin starts pointing at somewhere you could walk to.
//
// This is the OPPOSITE call from the bus route badges, deliberately. A badge
// tracks something moving and reads as life in the city from any height; a stop
// is a fixed label on a kerb, and a label you cannot place is just clutter.
const CEILING_Y = 1050;
// Faded out over the last stretch rather than switched off, so climbing away
// dims the layer instead of blinking it out.
const CEILING_FADE = 260;
// Distance at which a marker draws at its authored size. Apparent size is
// MARKER_W / REF_DIST, so this pair is the on-screen size dial.
const REF_DIST = 240;
const SCALE_MIN = 1.0;
// Enough headroom to hold that apparent size all the way out: the hero view is
// ~8 km from the marker, which needs ~34x. Capping lower is what made them
// shrink into nothing when zoomed out.
const SCALE_MAX = 40;
// A quarter of what this used to draw. Every stop having a pin is what the data
// says, but it is not what a city looks like: at 40 the layer read as a field of
// markers with a diorama behind it. Ten is enough to say "there is transit here,
// and here, and here" and leave the buildings visible, which is the whole point
// of only showing the ones nearby.
const MAX_MARKERS = 10;
// Declutter spacing, as a multiple of a marker's own width. Markers are drawn
// at a constant SIZE ON SCREEN, so the world distance that keeps two of them
// from overlapping grows with viewing distance — which makes this the honest
// unit. Deriving the cell from the search radius instead looked equivalent and
// merged the four corners of an intersection into a single pin at street level.
//
// Doubled along with the cut above, and that pairing is the point: density falls
// with the SQUARE of this, so doubling it is itself the quarter. Cutting the cap
// alone would have kept the old close spacing and simply stopped after ten,
// bunching every survivor around the centre of the view and leaving the edges
// bare. Widening the grid instead thins the whole frame evenly.
const DECLUTTER_SPACING = 2.8;
const DECLUTTER_MIN_M = 11;

const MAX_PICK_DISTANCE = 4000;

const dummy = new Object3D();
// Reused every frame so the declutter pass allocates nothing.
const cells = new Map();
const chosen = [];

// The Muni worm, the mark on the side of every coach in the fleet — including
// the one this scene drives. Vector, not a bitmap: the pin is drawn anywhere
// from a handful of pixels at hero altitude to a third of the screen at street
// level, and only an outline survives that range without either softening or
// showing its own pixels. The browser rasterises the SVG at whatever size we
// hand drawImage.
const WORM_URL = `${import.meta.env.BASE_URL}sf-assets/muni-worm.svg`;
const WORM_ASPECT = 260 / 126;

// Texture side. The pin is not square — it is a card with a tail — but a
// power-of-two square is what samples cleanly on every GPU, so the art is laid
// out inside it and the empty margins cost nothing.
const PIN_TEX = 256;

// A squircle, not a circle: the mark inside is a wide, short block, and a round
// card wastes its corners and squeezes the worm to fit the chord. The straight
// runs of a superellipse give the glyph its full width at the same visual size.
function pinPath(ctx, x, y, w, h, radius, tailHalf, tailTip) {
  const r = Math.min(radius, w / 2, h / 2);
  const cx = x + w / 2;
  const right = x + w;
  const bottom = y + h;
  ctx.beginPath();
  ctx.moveTo(x + r, y);
  ctx.arcTo(right, y, right, y + r, r);
  ctx.arcTo(right, bottom, right - r, bottom, r);
  // The tail is cut into the bottom edge rather than pasted on underneath, so
  // the whole pin is one closed outline and the border strokes round it once.
  ctx.lineTo(cx + tailHalf, bottom);
  ctx.lineTo(cx, tailTip);
  ctx.lineTo(cx - tailHalf, bottom);
  ctx.arcTo(x, bottom, x, bottom - r, r);
  ctx.arcTo(x, y, x + r, y, r);
  ctx.closePath();
}

// One marker icon for every stop, so no atlas is needed — a squircle in the toy
// UI voice (cream card stock, warm-ink border, hard offset shadow) carrying the
// worm.
//
// The worm arrives asynchronously, so the card is drawn now and the mark is
// composited on top when the image lands, at which point the texture is marked
// dirty. Until then the pin is a blank card — visible, clickable, just wearing
// no badge — rather than nothing at all.
function markerTexture() {
  const canvas = document.createElement('canvas');
  canvas.width = PIN_TEX;
  canvas.height = PIN_TEX;
  const ctx = canvas.getContext('2d');
  const cardX = 50;
  const cardY = 28;
  const cardW = 156;
  const cardH = 150;
  const cardR = 52; // a third of the side: reads as a squircle, not a rounded box
  const cx = cardX + cardW / 2;
  const cy = cardY + cardH / 2;

  pinPath(ctx, cardX + 6, cardY + 10, cardW, cardH, cardR, 26, 244);
  ctx.fillStyle = 'rgba(28, 24, 20, 0.34)';
  ctx.fill();

  pinPath(ctx, cardX, cardY, cardW, cardH, cardR, 26, 234);
  ctx.fillStyle = '#fbf7ee';
  ctx.fill();
  ctx.lineWidth = 10;
  ctx.lineJoin = 'round';
  ctx.strokeStyle = '#3a3530';
  ctx.stroke();

  const texture = new CanvasTexture(canvas);
  texture.colorSpace = SRGBColorSpace;

  const worm = new Image();
  worm.onload = () => {
    // Across the card's straight run, inside the border and the corner arcs.
    const w = cardW * 0.72;
    ctx.drawImage(worm, cx - w / 2, cy - w / WORM_ASPECT / 2, w, w / WORM_ASPECT);
    texture.needsUpdate = true;
  };
  worm.onerror = () => {
    console.warn('sf-munistops: muni-worm.svg missing — stop pins draw blank');
  };
  worm.src = WORM_URL;
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

    // Above the ceiling there is nothing to draw and nothing to pick — clearing
    // `visible` is what makes the second true, so a pin cannot be clicked from a
    // height it is not shown at.
    const fade = Math.min(1, Math.max(0, (CEILING_Y - camY) / CEILING_FADE));
    mesh.material.opacity = fade;
    if (fade <= 0) {
      mesh.count = 0;
      visible = [];
      return;
    }

    // ONE MARKER PER VIEW CELL, nearest the centre of the view winning. An
    // earlier version instead shrank the radius until few enough stops were in
    // range, which sounds equivalent and behaves very differently: downtown it
    // collapsed to a ~380 m circle and stacked every marker in the middle of a
    // whole-city view, so from altitude the layer read as empty. Spreading over
    // a grid keeps the same budget but puts a marker where each part of the
    // city is, at every zoom.
    // How wide a marker is in world metres at this viewing distance.
    const viewDist = Math.hypot(camera.position.x - camX, camera.position.y, camera.position.z - camZ);
    const markerWorldW = MARKER_W * Math.max(SCALE_MIN, Math.min(SCALE_MAX, viewDist / REF_DIST));
    const cellSize = Math.max(DECLUTTER_MIN_M, markerWorldW * DECLUTTER_SPACING);
    cells.clear();
    chosen.length = 0;
    for (const stop of table.stops) {
      const dx = stop.x - camX;
      const dz = stop.z - camZ;
      const d2 = dx * dx + dz * dz;
      if (d2 > radius * radius) continue;
      const key = `${Math.floor(stop.x / cellSize)}_${Math.floor(stop.z / cellSize)}`;
      const held = cells.get(key);
      if (!held || d2 < held.d2) cells.set(key, { stop, d2 });
    }
    for (const { stop, d2 } of cells.values()) chosen.push({ stop, d2 });
    // Nearest the view centre first, so the cap trims the far edges rather than
    // whatever the map happened to iterate last.
    chosen.sort((a, b) => a.d2 - b.d2);

    let count = 0;
    visible = [];
    for (const { stop } of chosen) {
      if (count >= MAX_MARKERS) break;
      const y = data.sampleElevation ? data.sampleElevation(stop.x, stop.z) : 0;
      // Scale off the CAMERA distance (not the pivot distance) so apparent size
      // stays put; the pivot only decides which stops are shown.
      const camDist = Math.hypot(stop.x - camera.position.x, stop.z - camera.position.z, y - camera.position.y);
      const scale = Math.max(SCALE_MIN, Math.min(SCALE_MAX, camDist / REF_DIST));
      const markerY = y + MARKER_Y * Math.max(1, scale * 0.35);
      dummy.position.set(stop.x, markerY, stop.z);
      dummy.quaternion.copy(camQ);
      dummy.scale.setScalar(scale);
      dummy.updateMatrix();
      mesh.setMatrixAt(count, dummy.matrix);
      // Where the pin was actually DRAWN, and how big. The pick reads these
      // rather than recomputing from the stop, so the hit target is the art on
      // screen and cannot drift from it.
      visible.push({ stop, y, markerY, scale });
      count++;
    }
    mesh.count = count;
    mesh.instanceMatrix.needsUpdate = true;

    // The radius now just follows the zoom; density is the grid's job.
    radius += (zoomRadius - radius) * Math.min(1, dt * 2);
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

  // Distance from a ray to a point, and how far along the ray the closest
  // approach is. Returns null behind the camera or past the reach.
  function rayHit(origin, direction, x, y, z, reach) {
    const px = x - origin.x;
    const py = y - origin.y;
    const pz = z - origin.z;
    const t = px * direction.x + py * direction.y + pz * direction.z;
    if (t <= 0 || t > MAX_PICK_DISTANCE) return null;
    const away = Math.hypot(px - direction.x * t, py - direction.y * t, pz - direction.z * t);
    return away > reach ? null : t;
  }

  function pickStop(origin, direction) {
    // THE PIN IS THE TARGET, and nothing else is. It floats MARKER_Y above the
    // pavement and is the only part of a stop a viewer can see or aim at, but
    // this used to test a point 3 m off the ground with a radius that grew with
    // viewing distance. Two things were wrong with that: the click landed where
    // the art is not, so the pin — which looks exactly like a button — did
    // nothing when pressed; and the radius reached 88 m at altitude, which
    // measured 180 px wide on screen against art 70 px wide, so the cursor lit
    // up over half a block of empty road.
    //
    // The test is now the drawn quad itself: its centre, and its own half-width
    // at the size it was drawn. The tail needs no special case — it is inside
    // that quad, which is the whole of the art.
    let best = null;
    for (const { stop, markerY, scale } of visible) {
      const t = rayHit(origin, direction, stop.x, markerY, stop.z, (MARKER_W / 2) * scale);
      if (t === null || (best && t >= best.distance)) continue;
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
