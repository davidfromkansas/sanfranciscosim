// Ferry route walls: a ribbon of light along each SF Bay Ferry alignment,
// drawn in the same Tron light-trail idiom as the Muni route glow
// (app/src/routewall.js), in each service's own livery colour.
//
// Three things differ from the bus walls, all of them because this is open
// water rather than a street grid:
//
// 1. THE WALLS ARE ALWAYS ON. A bus wall lights only where a live vehicle is
//    working, because a beam over a street with no service on it is a lie about
//    the timetable. A ferry alignment is not a street — it is the crossing
//    itself, and nothing else in the Bay marks it. Drawing all fourteen keeps the
//    network legible at 3 a.m. and keeps the geometry static, so there is no
//    rebuild when the fleet changes and no cost to a quiet night.
// 2. ONE SHAPE PER ROUTE. The feeds publish 67 shapes for 14 routes — the same
//    crossing appears up to four times as separate trip patterns. Drawing them
//    all would stack four coincident walls on one corridor and blow it out to
//    four times the intended brightness, so each route contributes its longest
//    shape and the duplicates are dropped.
// 3. THEY END AT THE EDGE OF THE WORLD, GENTLY. Vallejo is 36 km north and
//    Richmond and Harbor Bay are just outside too, while the Bay is modelled as
//    one 30 km water plane. A wall that simply stopped at the boundary would
//    read as an unfinished asset, so the last stretch tapers to nothing (aFade)
//    and anything past the edge is dropped — which is also the honest picture:
//    the route continues, our water does not.
//
// The base sits at water level (y 0) rather than sampling terrain: every metre
// of these alignments is over the Bay.
//
// Draw calls: one.

import { BufferAttribute, BufferGeometry, Color, Mesh } from 'three';

import { shared } from './env.js';
import { loadFerryNetwork, SCENE_HALF_EXTENT } from './ferrynetwork.js';
import { applyRouteWallDay, createRouteWallMaterial, ROUTE_WALL_NIGHT_AT } from './routewall.js';

// TALLER than the Muni walls (50 m), not shorter. The first pass here reasoned
// that open water needs less, and the screenshot said the opposite: a bus wall
// is read from a few hundred metres over a street, while a ferry wall is read
// from kilometres out across the Bay, where 42 m aliased down to a hairline.
// This is roughly the Bay Bridge's deck height, which is the one thing out
// there that gives the eye a scale to compare against.
const WALL_HEIGHT = 90;
// The last stretch before the water plane's edge, over which a wall tapers out.
const EDGE_FADE_M = 1200;

// Quality lever (rule 2). Never zero — a switched-off feature and a broken one
// look identical from the outside, which is the fog-bank lesson. The low tier
// drops the wall height and skips the routes that mostly run off-scene.
const QUALITY = {
  high: { height: WALL_HEIGHT, all: true },
  medium: { height: WALL_HEIGHT, all: true },
  low: { height: WALL_HEIGHT * 0.7, all: false },
};
// Routes whose crossing mostly leaves the water plane; the low tier keeps the
// ones you can follow end to end. Ids are operator-namespaced, because the
// agencies reuse each other's short codes.
const OFF_SCENE_ROUTES = new Set(['SB:VJO', 'SB:RCH', 'SB:HB', 'GF:LSSF']);

// A livery colour is picked for a printed timetable, not for emitted light, so
// each one is read twice: brightened to neon for the additive night pass, and
// deepened for the alpha-blended day pass where it has to hold against a pale
// city and bright water.
function neon(hex) {
  const c = new Color(hex);
  const peak = Math.max(c.r, c.g, c.b) || 1;
  // Normalise the brightest channel to 1 so every livery reads as lit, then
  // lift the darker channels slightly so a navy does not go black.
  return [
    Math.min(1, (c.r / peak) * 0.92 + 0.08),
    Math.min(1, (c.g / peak) * 0.92 + 0.08),
    Math.min(1, (c.b / peak) * 0.92 + 0.08),
  ];
}

function paint(hex) {
  const c = new Color(hex);
  // Deepened, so the ribbon is denser than the livery rather than washed out
  // by daylight over bright water.
  return [c.r * 0.82, c.g * 0.82, c.b * 0.82];
}

// How much of a wall survives at this point: 1 well inside the water plane,
// easing to 0 at its boundary.
function edgeFade(x, z) {
  const margin = Math.min(SCENE_HALF_EXTENT - Math.abs(x), SCENE_HALF_EXTENT - Math.abs(z));
  if (margin <= 0) return 0;
  if (margin >= EDGE_FADE_M) return 1;
  const t = margin / EDGE_FADE_M;
  return t * t * (3 - 2 * t); // smoothstep
}

// No `data` handle: unlike the Muni walls this one never samples terrain.
export function createFerryRoutes(scene) {
  let mesh = null;
  let palettes = null;
  let material = null;
  let uniforms = null;
  let isDay = true;
  let tier = 'high';
  let network = null;
  let routeCount = 0;

  loadFerryNetwork().then((n) => {
    if (!n) return; // rule 3: no bake, no walls, city unaffected.
    network = n;
    const created = createRouteWallMaterial({ isDay });
    material = created.material;
    uniforms = created.uniforms;
    mesh = new Mesh(new BufferGeometry(), material);
    mesh.name = 'ferry-route-walls';
    // Every whole-city object here gets this: bounds cover geometry that spans
    // the whole Bay and a frustum test on it culls on-screen content.
    mesh.frustumCulled = false;
    mesh.renderOrder = 3;
    scene.add(mesh);
    rebuild();
  });

  // Longest shape per route: the fullest version of that crossing.
  function chosenShapes() {
    const out = [];
    for (const route of network.routes.values()) {
      let best = null;
      for (const idx of route.shapes) {
        const shape = network.shapes[idx];
        if (!shape) continue;
        if (!best || shape.lengthM > network.shapes[best].lengthM) best = idx;
      }
      if (best != null) out.push({ route, shapeIdx: best });
    }
    return out;
  }

  function rebuild() {
    if (!mesh || !network) return;
    const height = QUALITY[tier].height;
    const drawAll = QUALITY[tier].all;
    const F = network.verts;

    const positions = [];
    const nightColors = [];
    const dayColors = [];
    const ribbon = [];
    const fade = [];
    const indices = [];
    routeCount = 0;

    for (const { route, shapeIdx } of chosenShapes()) {
      if (!drawAll && OFF_SCENE_ROUTES.has(route.id)) continue;
      const shape = network.shapes[shapeIdx];
      const nightColor = neon(route.color);
      const dayColor = paint(route.color);
      const base = shape.vertexOffset * 3;
      let drew = false;

      for (let i = 0; i < shape.vertexCount - 1; i++) {
        const o = base + i * 3;
        const q = o + 3;
        const x0 = F[o];
        const z0 = F[o + 1];
        const x1 = F[q];
        const z1 = F[q + 1];
        const f0 = edgeFade(x0, z0);
        const f1 = edgeFade(x1, z1);
        // Wholly outside the water plane: there is no sea under it to draw on.
        if (f0 <= 0 && f1 <= 0) continue;

        const v = positions.length / 3;
        // Base at water level; these alignments are over the Bay end to end.
        positions.push(x0, 0, z0);
        positions.push(x0, height, z0);
        positions.push(x1, 0, z1);
        positions.push(x1, height, z1);
        for (let j = 0; j < 4; j++) {
          nightColors.push(nightColor[0], nightColor[1], nightColor[2]);
          dayColors.push(dayColor[0], dayColor[1], dayColor[2]);
        }
        // Matches the corner order pushed above: bottom, top, bottom, top.
        ribbon.push(0, 1, 0, 1);
        fade.push(f0, f0, f1, f1);
        indices.push(v, v + 1, v + 2, v + 1, v + 3, v + 2);
        drew = true;
      }
      if (drew) routeCount++;
    }

    const geo = mesh.geometry;
    geo.setAttribute('position', new BufferAttribute(new Float32Array(positions), 3));
    // Both palettes are baked once; the frame loop only swaps which attribute
    // is bound, so the day/night flip allocates nothing.
    palettes = {
      night: new BufferAttribute(new Float32Array(nightColors), 3),
      day: new BufferAttribute(new Float32Array(dayColors), 3),
    };
    geo.setAttribute('color', palettes[isDay ? 'day' : 'night']);
    geo.setAttribute('aRibbon', new BufferAttribute(new Float32Array(ribbon), 1));
    geo.setAttribute('aFade', new BufferAttribute(new Float32Array(fade), 1));
    geo.setIndex(indices);
    mesh.visible = positions.length > 0;
  }

  function setDay(day) {
    if (day === isDay || !material) return;
    isDay = day;
    applyRouteWallDay({ material, uniforms }, day);
    if (palettes) mesh.geometry.setAttribute('color', palettes[day ? 'day' : 'night']);
  }

  function setQuality(key) {
    const next = QUALITY[key] ? key : 'high';
    if (next === tier) return;
    tier = next;
    rebuild();
  }

  function update() {
    if (!mesh || !material) return;
    // Same signal the Muni walls read, so the whole city crosses dusk together.
    const night = shared.uNight.value ?? 0;
    setDay(night < ROUTE_WALL_NIGHT_AT);
    // The night ribbon rides the same ramp the landmark glow does, so the Bay
    // lights up with the city rather than snapping on.
    material.opacity = isDay ? 0.8 : Math.min(1, 0.12 + night * 0.95) * 0.62;
  }

  return {
    update,
    setQuality,
    get routes() {
      return routeCount;
    },
    get visible() {
      return Boolean(mesh && mesh.visible);
    },
    dispose() {
      if (!mesh) return;
      scene.remove(mesh);
      mesh.geometry.dispose();
      material.dispose();
    },
  };
}
