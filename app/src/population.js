// The residents. Every sphere on these sidewalks is one adult sampled from the
// 2024 ACS PUMS microdata for San Francisco and written up as a character —
// a real name, a real age, a real occupation, living in the PUMA the Census
// actually recorded them in. Nobody is invented and nobody wanders out of
// their own neighbourhood.
//
// This layer REPLACES the anonymous pedestrians inside the PUMAs that have
// residents written for them; `containsResidents` is handed to the traffic
// layer so it stops seeding faceless walkers on those streets. PUMAs still
// being written keep the procedural crowd, so the city is never emptier than
// it was (AGENTS iron rule 3 — and if the baked file is missing entirely this
// module renders nothing and the old crowd runs everywhere, unchanged).
//
// Draw calls: 1 instanced sphere + 1 instanced badge quad = 2.
//
// Data comes from app/public/sf-people/, baked by pipeline/bake-population.mjs
// out of the persona project. No key, no endpoint, no cold start.

import {
  CanvasTexture,
  Color,
  DynamicDrawUsage,
  Group,
  InstancedMesh,
  MeshBasicMaterial,
  Matrix4,
  MeshLambertMaterial,
  Object3D,
  PlaneGeometry,
  SRGBColorSpace,
  Vector3,
} from 'three';
import { mergeGeometries } from 'three/addons/utils/BufferGeometryUtils.js';
import { BoxGeometry } from 'three';
import { shared } from './env.js';

const DATA = `${import.meta.env.BASE_URL}sf-people/`;

// Hard ceiling on simulated residents. The baked file is well under this today;
// the cap is what keeps a future 10,000-persona bake from silently costing a
// frame. Residents past it are not loaded at all rather than loaded and hidden.
const MAX_RESIDENTS = 1500;
const LOW_CAP = 400;

// How many written residents a PUMA needs before it takes its sidewalks back
// from the anonymous crowd. Four personas do not populate the Marina — handing
// a half-written PUMA its streets empties them, which looks like a bug and is
// worse than the placeholder it replaced. A PUMA below this keeps the
// procedural pedestrians AND shows the residents it does have, so writing more
// personas only ever adds people to the city.
const HANDOVER_MIN = 50;

// A spread-out index per resident per slot. The salt keeps skin, hair and
// trousers from correlating — without it every resident with dark hair would
// also be wearing the same trousers, and a crowd of four hundred would visibly
// repeat.
function pickIndex(i, salt, n) {
  let h = Math.imul(i + salt, 2654435761) >>> 0;
  h ^= h >>> 15;
  h = Math.imul(h, 2246822519) >>> 0;
  return (h >>> 13) % n;
}

const WALK_SPEED = 1.25; // m/s, an unhurried pace

// Residents are voxel people from sf-avatar-studio rather than spheres. The rig
// is baked to app/public/sf-people/avatar-rig.json — see pipeline/bake-avatars.mjs
// for why none of that project's glTF reaches the browser.
const RIG_URL = `${DATA}avatar-rig.json`;
// The studio's model is 0.62 units tall and the city is in metres. This is not
// a real person's height — it is deliberately half again over it, because a
// resident scaled to life size disappears against a four-storey building in a
// toy diorama. The buses and cars are exaggerated for the same reason.
const PERSON_HEIGHT = 2.58;

// The walk. Nothing in the studio is rigged, so the cycle is procedural: legs
// hinge at the hip, arms at the shoulder, arms opposite the leg on their own
// side. Phase advances with DISTANCE, not time, so stride matches speed and a
// resident never moonwalks.
const STRIDE = 1.55;        // radians of phase per metre walked
const LEG_SWING = 0.62;     // radians
const ARM_SWING = 0.42;
const BOB = 0.035;          // metres, twice a step — the body rises on each stride

// Badges follow the ZOOM, not a fixed distance in metres — the same reasoning
// as the Muni route bubbles (see muni.js): this camera spends most of its life
// in the air, so a radius tuned for street level would label nothing, and the
// bubbles are scaled with distance to hold a roughly constant size on screen.
// Clutter is bounded by MAX_BADGES, not by the radius.
const MAX_BADGES = 140;
const LOW_BADGES = 45;
const BADGE_W = 5.2;
const BADGE_H = 5.2;
// Height of the QUAD CENTRE; the tail tip drops ~0.36 x H. Raised with the
// residents when they grew: the tail is meant to just kiss the top of a head,
// and left at 4.4 it hung inside their chest instead.
const BADGE_Y = 5.77;
const BADGE_RADIUS_MIN = 220;
const BADGE_RADIUS_MAX = 33000;
const BADGE_RADIUS_PER_M = 6.6;
const BADGE_REF_DIST = 340;
const BADGE_SCALE_MIN = 0.85;
const BADGE_SCALE_MAX = 26;

// One hue per PUMA, carried on the instance colour so all eight neighbourhoods
// still cost a single draw call. Warm-to-cool around the toy palette; adjacent
// PUMAs deliberately do not get adjacent hues.
const PUMA_COLORS = {
  '07507': '#d9762f', // Bayview & Hunters Point
  '07508': '#3f8f6b', // Richmond & Presidio
  '07509': '#c8442f', // Chinatown & North Beach
  '07510': '#4a6bb5', // Mission & SoMa
  '07511': '#8a5bb0', // Bernal & the Castro
  '07512': '#2f8fa8', // The Sunset
  '07513': '#b0873a', // Ingleside
  '07514': '#c4508c', // Marina & Western Addition
};
const DEFAULT_COLOR = '#6b7280';

// ------------------------------------------------------------------ geometry

function polylineLengths(points) {
  const cumulative = new Float32Array(points.length / 3);
  let total = 0;
  for (let i = 1; i < cumulative.length; i++) {
    total += Math.hypot(points[i * 3] - points[(i - 1) * 3], points[i * 3 + 2] - points[(i - 1) * 3 + 2]);
    cumulative[i] = total;
  }
  return { cumulative, total };
}

function samplePolyline(points, cumulative, total, distance, out, tangent) {
  const d = Math.max(0, Math.min(total, distance));
  let i = 1;
  while (i < cumulative.length - 1 && cumulative[i] < d) i++;
  const d0 = cumulative[i - 1];
  const d1 = cumulative[i];
  const t = d1 - d0 > 1e-4 ? (d - d0) / (d1 - d0) : 0;
  const ax = points[(i - 1) * 3];
  const ay = points[(i - 1) * 3 + 1];
  const az = points[(i - 1) * 3 + 2];
  const bx = points[i * 3];
  const by = points[i * 3 + 1];
  const bz = points[i * 3 + 2];
  out.set(ax + (bx - ax) * t, ay + (by - ay) * t, az + (bz - az) * t);
  if (tangent) tangent.set(bx - ax, by - ay, bz - az).normalize();
}

// Baked rings are flat [x, z, x, z, ...] in local metres, so the crossing test
// reads them two at a time rather than through a point object.
function inRing(ring, x, z) {
  let inside = false;
  for (let i = 0, j = ring.length - 2; i < ring.length; j = i, i += 2) {
    const zi = ring[i + 1];
    const zj = ring[j + 1];
    if (zi > z !== zj > z) {
      const t = (z - zi) / (zj - zi);
      if (x < ring[i] + t * (ring[j] - ring[i])) inside = !inside;
    }
  }
  return inside;
}

function boxOf(rings) {
  let west = Infinity;
  let east = -Infinity;
  let south = Infinity;
  let north = -Infinity;
  for (const ring of rings) {
    for (let i = 0; i < ring.length; i += 2) {
      if (ring[i] < west) west = ring[i];
      if (ring[i] > east) east = ring[i];
      if (ring[i + 1] < south) south = ring[i + 1];
      if (ring[i + 1] > north) north = ring[i + 1];
    }
  }
  return { west, east, south, north };
}

// ------------------------------------------------------------------- badges

// A cream speech bubble with a person in it, in the toy UI voice: card stock,
// warm-ink border, a hard tail pointing at whoever is speaking. One cell, so
// one 256 px texture rather than the lazily-grown atlas the route pills need —
// every resident says the same thing today. When the tags start carrying names
// and posts this becomes an atlas; the quad layer above it does not change.
// The four moods, mirrored from api/_lib/feeds/residents.mjs. Duplicated on
// purpose: the browser never talks to that module, and a fetch to learn four
// emoji would put a network dependency in front of the diorama for nothing.
// The KEYS have to match; the check below fails loudly if they drift.
const MOOD_BADGES = [
  { key: 'grumpy', emoji: '\u{1F621}' },
  { key: 'sad', emoji: '\u{1F614}' },
  { key: 'neutral', emoji: '\u{1F610}' },
  { key: 'cheerful', emoji: '\u{1F929}' },
];

// Same weights as the writer uses, so the crowd overhead and the crowd in the
// feed are the same city. Grumpy 18, sad 12, neutral 40, cheerful 30.
const MOOD_BADGE_WEIGHTS = [180, 120, 400, 300];

// Which mood a resident is in, from their id alone — the same hash the feed
// runs, so the face over somebody's head matches the voice in their posts.
function moodIndexFor(id) {
  let h = 2166136261;
  for (let i = 0; i < id.length; i++) {
    h ^= id.charCodeAt(i);
    h = Math.imul(h, 16777619) >>> 0;
  }
  const total = MOOD_BADGE_WEIGHTS.reduce((a, b) => a + b, 0);
  let roll = (h >>> 8) % total;
  for (let i = 0; i < MOOD_BADGE_WEIGHTS.length; i++) {
    roll -= MOOD_BADGE_WEIGHTS[i];
    if (roll < 0) return i;
  }
  return 2;
}

function buildBadgeTexture(emoji) {
  const canvas = document.createElement('canvas');
  canvas.width = 256;
  canvas.height = 256;
  const ctx = canvas.getContext('2d');

  // Bubble body and tail as ONE path so the outline runs around the joint.
  const bx = 14;
  const by = 12;
  const bw = canvas.width - 28;
  const bh = 164;
  const r = 40;
  const tailL = 96;
  const tailR = 160;
  const tipX = 112;
  const tipY = 236;
  ctx.beginPath();
  ctx.moveTo(bx + r, by);
  ctx.lineTo(bx + bw - r, by);
  ctx.quadraticCurveTo(bx + bw, by, bx + bw, by + r);
  ctx.lineTo(bx + bw, by + bh - r);
  ctx.quadraticCurveTo(bx + bw, by + bh, bx + bw - r, by + bh);
  ctx.lineTo(tailR, by + bh);
  ctx.lineTo(tipX, tipY);
  ctx.lineTo(tailL, by + bh);
  ctx.lineTo(bx + r, by + bh);
  ctx.quadraticCurveTo(bx, by + bh, bx, by + bh - r);
  ctx.lineTo(bx, by + r);
  ctx.quadraticCurveTo(bx, by, bx + r, by);
  ctx.closePath();

  ctx.shadowColor = 'rgba(28, 24, 20, 0.34)';
  ctx.shadowBlur = 10;
  ctx.shadowOffsetY = 6;
  ctx.fillStyle = '#fbf7ee';
  ctx.fill();
  ctx.shadowColor = 'transparent';
  ctx.lineWidth = 9;
  ctx.lineJoin = 'round';
  ctx.strokeStyle = '#3a3530';
  ctx.stroke();

  // Half again over the 104 the standing figure used. A mood only works if it
  // can be read, and these are drawn a few dozen pixels across on screen — at
  // 104 the difference between a scowl and a flat line was gone.
  ctx.font = '156px "Apple Color Emoji", "Segoe UI Emoji", "Noto Color Emoji", sans-serif';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillText(emoji, bx + bw / 2, by + bh / 2 + 6);

  const texture = new CanvasTexture(canvas);
  texture.colorSpace = SRGBColorSpace;
  return texture;
}

// --------------------------------------------------------------------- layer

export function createPopulation(scene, data, city) {
  const group = new Group();
  group.name = 'population';
  scene.add(group);

  const dummy = new Object3D();
  const position = new Vector3();
  const tangent = new Vector3();
  const tint = new Color();

  let residents = [];
  let areas = []; // { puma, rings, box }
  let livePumas = new Set(); // PUMAs with any residents at all — these need streets
  let ownedPumas = new Set(); // PUMAs written densely enough to drop the anonymous crowd
  let ready = false;

  let bodyMesh = null;
  let badgeMeshes = [];
  let badgeCapacity = 0;
  const badgeFill = new Array(MOOD_BADGES.length).fill(0);
  let cap = MAX_RESIDENTS;
  let badgeCap = MAX_BADGES;
  let badgeRadius = BADGE_RADIUS_MAX;
  let eligibleLast = 0;
  let bodyScale = 1;
  let rigScale = 1;
  let rig = null;
  let partMeshes = [];
  // Reused every frame for every part, so the walk costs no allocation.
  const bodyM = new Matrix4();
  const limbM = new Matrix4();
  const outM = new Matrix4();
  let focused = null; // resident id the viewer was sent to
  // Reused each frame: everyone inside the badge radius, before the nearest are
  // picked off it. Allocating this per frame would be 432 objects of garbage
  // sixty times a second.
  const shortlist = [];

  // Street centrelines that fall inside a PUMA we have residents for, pooled by
  // PUMA. The city streams tiles in, so this grows over the first few seconds;
  // each new batch is classified once and the answer cached on the path itself.
  const pathsByPuma = new Map();
  let classified = 0;

  function classify(paths) {
    if (!ready) return;
    // A rebuild empties the array and refills it with fresh objects, so anyone
    // still pacing a discarded polyline has to be turned loose.
    if (paths.length < classified) {
      pathsByPuma.clear();
      for (const resident of residents) {
        resident.placed = false;
        resident.path = null;
      }
      classified = 0;
    }
    for (let i = classified; i < paths.length; i++) {
      const path = paths[i];
      const puma = pumaOfPath(path);
      if (!puma || !livePumas.has(puma)) continue;
      if (!path.meta) path.meta = polylineLengths(path.points);
      let pool = pathsByPuma.get(puma);
      if (!pool) pathsByPuma.set(puma, (pool = []));
      pool.push(path);
    }
    classified = paths.length;
  }

  city.onPaths(classify);

  // A street belongs to a PUMA only if the whole of it does. Classifying by the
  // first point alone let residents pace right across a boundary — a Richmond
  // nurse ended up walking Chinatown — because the centreline a path is drawn
  // from does not stop where the neighbourhood does. Boundary streets simply go
  // unused; there is always another block.
  function pumaOfPath(path) {
    const p = path.points;
    const last = p.length - 3;
    const mid = Math.floor(p.length / 6) * 3;
    const puma = pumaAt(p[0], p[2]);
    if (!puma) return null;
    if (pumaAt(p[mid], p[mid + 2]) !== puma) return null;
    if (pumaAt(p[last], p[last + 2]) !== puma) return null;
    return puma;
  }

  function pumaAt(x, z) {
    for (const area of areas) {
      if (x < area.box.west || x > area.box.east || z < area.box.south || z > area.box.north) continue;
      for (const ring of area.rings) if (inRing(ring, x, z)) return area.puma;
    }
    return null;
  }

  // Handed to the traffic layer: true means "this neighbourhood's residents are
  // written, do not seed an anonymous pedestrian here".
  function containsResidents(x, z) {
    if (!ready || !ownedPumas.size) return false;
    const puma = pumaAt(x, z);
    return puma !== null && ownedPumas.has(puma);
  }

  // One InstancedMesh per (garment colour x rigid body part). Ten of them, so
  // the whole animated city is ten draw calls — two more than the spheres cost,
  // for people with arms and legs. A part's boxes are merged into one geometry
  // and shifted so the group's PIVOT is at the origin, which is what lets a
  // limb be swung by writing a rotation into the instance matrix; without a
  // skeleton there is nowhere else to put the joint.
  function buildPart(part) {
    const pivotY =
      part.group === 'armL' || part.group === 'armR' ? rig.pivots.arm
      : part.group === 'legL' || part.group === 'legR' ? rig.pivots.leg
      : 0;
    const geos = part.boxes.map((b) => {
      const g = new BoxGeometry(b.size[0], b.size[1], b.size[2]);
      g.translate(b.centre[0], b.centre[1] - pivotY, b.centre[2]);
      return g;
    });
    const geo = geos.length === 1 ? geos[0] : mergeGeometries(geos, false);
    const mesh = new InstancedMesh(geo, new MeshLambertMaterial({}), residents.length);
    mesh.name = `pums-${part.id}`;
    mesh.instanceMatrix.setUsage(DynamicDrawUsage);
    mesh.frustumCulled = false;
    mesh.count = 0;
    mesh.userData.part = part;
    mesh.userData.pivotY = pivotY;
    group.add(mesh);
    return mesh;
  }

  // Colours are cached as Color objects once, because setColorAt is called ten
  // times per resident per frame and parsing a hex string there would be the
  // most expensive thing in the loop.
  let palette = null;
  const shirtTint = new Color();
  function cachePalette() {
    palette = {};
    for (const [role, list] of Object.entries(rig.palette)) {
      palette[role] = list.map((hex) => new Color().setStyle(hex, SRGBColorSpace));
    }
  }

  // What each part is painted. Skin, hair, trousers and face come from the
  // studio's own palettes; the SHIRT carries the neighbourhood hue that the
  // spheres used to carry on their whole body, so the eight PUMAs stay legible
  // from the air — which was the point of colouring residents at all.
  function paintFor(resident, role, puma, isFocused) {
    if (role === 'shirt') return puma;
    const list = palette[role];
    if (!list || !list.length) return puma;
    const c = shirtTint.copy(list[resident.look[role] % list.length]);
    return isFocused ? c.offsetHSL(0, 0.15, 0.25) : c;
  }

  function build() {
    cachePalette();
    // The studio models a person 0.62 units tall; the city is in metres.
    rigScale = PERSON_HEIGHT / rig.modelHeight;
    partMeshes = rig.parts.map(buildPart);
    // Kept as the anchor the rest of the loop counts against; the body group is
    // the one part every resident always has.
    bodyMesh = partMeshes[0];

    // One mesh per mood, because an InstancedMesh carries ONE texture and the
    // whole point is that the faces differ. Four draw calls where there was
    // one; the alternative is an atlas and a custom shader for no visible gain.
    // Each is sized for the worst case of every visible badge being one mood.
    const room = Math.min(residents.length, MAX_BADGES);
    badgeMeshes = MOOD_BADGES.map(({ key, emoji }) => {
      const mesh = new InstancedMesh(
        new PlaneGeometry(BADGE_W, BADGE_H),
        new MeshBasicMaterial({
          map: buildBadgeTexture(emoji),
          transparent: true,
          depthWrite: false,
          alphaTest: 0.02,
        }),
        room
      );
      mesh.name = `pums-resident-badges-${key}`;
      mesh.instanceMatrix.setUsage(DynamicDrawUsage);
      mesh.frustumCulled = false;
      mesh.renderOrder = 4;
      mesh.count = 0;
      group.add(mesh);
      return mesh;
    });
    badgeCapacity = room;
  }

  async function load() {
    let people;
    let pumas;
    try {
      const [a, b, c] = await Promise.all([
        fetch(`${DATA}people.json`),
        fetch(`${DATA}pumas.json`),
        fetch(RIG_URL),
      ]);
      if (!a.ok || !b.ok || !c.ok) throw new Error(`${a.status}/${b.status}/${c.status}`);
      [people, pumas, rig] = await Promise.all([a.json(), b.json(), c.json()]);
    } catch (error) {
      // No bake, no residents. The anonymous crowd keeps the city populated and
      // nothing downstream notices, which is the whole point of the fallback.
      console.warn('sf-people: no baked population, keeping the procedural crowd', error);
      return;
    }

    areas = (pumas.areas ?? []).map((area) => ({
      puma: area.puma,
      rings: area.rings.map((ring) => Float32Array.from(ring)),
      box: boxOf(area.rings),
    }));

    const list = (people.people ?? []).slice(0, MAX_RESIDENTS);
    residents = list.map((person, i) => ({
      ...person,
      // A stable per-resident phase, so the bob is not in lockstep across a
      // block and does not change between reloads.
      phase: ((i * 2654435761) % 6283) / 1000,
      // Which of the studio's colours this person wears. Deterministic from the
      // index, so somebody you flew to yesterday looks the same today. The
      // shirt is NOT in here — it carries the neighbourhood hue, which is what
      // keeps eight PUMAs readable from the air.
      // Which face floats over them. Same hash the feed's writer uses, so the
      // badge and the voice in their posts are the same person's mood.
      moodIdx: moodIndexFor(person.id),
      look: {
        skin: pickIndex(i, 11, rig.palette.skin.length),
        hair: pickIndex(i, 23, rig.palette.hair.length),
        pants: pickIndex(i, 37, rig.palette.pants.length),
        face: pickIndex(i, 53, rig.palette.face.length),
      },
      path: null,
      d: 0,
      dir: 1,
      side: i % 2 ? 1 : -1,
      x: 0,
      y: 0,
      z: 0,
      heading: 0,
      placed: false,
      seatedPool: 0,
      dist: 0,
    }));
    const byPuma = {};
    for (const r of residents) byPuma[r.puma] = (byPuma[r.puma] ?? 0) + 1;
    livePumas = new Set(Object.keys(byPuma));
    ownedPumas = new Set(Object.keys(byPuma).filter((puma) => byPuma[puma] >= HANDOVER_MIN));
    ready = residents.length > 0;
    if (!ready) return;

    build();
    // The fetch almost always lands after the first street tiles, and `classify`
    // refuses to run before the polygons exist — so catch up on whatever the
    // city has already streamed in.
    classify(city.paths);

    console.log(
      `sf-people: ${residents.length} residents — ` +
        Object.entries(byPuma)
          .map(
            ([puma, n]) =>
              `${people.pumaNames?.[puma] ?? puma} ${n}${ownedPumas.has(puma) ? '' : ' (still sharing with the procedural crowd)'}`
          )
          .join(', ')
    );
  }

  // Seat a resident somewhere on a street inside their own PUMA. Returns false
  // when that PUMA has no streets loaded yet, which is normal for the first few
  // seconds and permanent for a viewer who never flies there.
  //
  // The pool grows as tiles stream in, so the first seating is drawn from
  // whatever handful of blocks arrived first — left alone, a whole
  // neighbourhood ends up strung along one street. Each resident therefore
  // remembers how much street existed when they picked, and re-picks once the
  // pool has doubled. Streaming stops, the doubling stops, and everybody has
  // settled somewhere in their own PUMA.
  function seat(resident) {
    const pool = pathsByPuma.get(resident.puma);
    if (!pool || !pool.length) return false;
    const path = pool[Math.floor(Math.random() * pool.length)];
    resident.path = path;
    resident.d = Math.random() * path.meta.total;
    resident.dir = Math.random() < 0.5 ? -1 : 1;
    resident.placed = true;
    resident.seatedPool = pool.length;
    return true;
  }

  function needsReseat(resident) {
    const pool = pathsByPuma.get(resident.puma);
    return pool ? pool.length >= resident.seatedPool * 2 : false;
  }

  function update(dt, cameraPos, cameraQuaternion) {
    if (!ready || !bodyMesh) return;

    const camX = cameraPos.x;
    const camZ = cameraPos.z;
    // Radius from the camera's HEIGHT, so what is labelled tracks what is on
    // screen instead of a distance that only reads right at one altitude.
    badgeRadius = Math.max(
      BADGE_RADIUS_MIN,
      Math.min(BADGE_RADIUS_MAX, Math.max(0, cameraPos.y) * BADGE_RADIUS_PER_M)
    );

    let bodies = 0;
    let badges = 0;
    // Per-mood write cursors, reset every frame alongside the shared counter.
    badgeFill.fill(0);
    let eligible = 0;
    const limit = Math.min(cap, residents.length);

    for (let i = 0; i < limit; i++) {
      const resident = residents[i];
      if (resident.placed && needsReseat(resident)) resident.placed = false;
      if (!resident.placed && !seat(resident)) continue;

      const path = resident.path;
      resident.d += resident.dir * WALK_SPEED * dt;
      // Turn round at the end of the block rather than teleport: a resident
      // belongs to their neighbourhood, so they pace it instead of respawning.
      if (resident.d <= 0 || resident.d >= path.meta.total) {
        resident.dir *= -1;
        resident.d = Math.max(0, Math.min(path.meta.total, resident.d));
      }
      samplePolyline(path.points, path.meta.cumulative, path.meta.total, resident.d, position, tangent);
      // Down the middle of the sidewalk, standing on the plinth top where the
      // street has one. Path points carry the traffic lift, which the kerb
      // height replaces rather than stacks on.
      const walk = path.sidewalk;
      const out = path.width / 2 + (walk ? walk.width / 2 : 1.9);
      resident.x = position.x + tangent.z * out * resident.side;
      resident.y = position.y - (path.lift || 0) + (walk ? walk.curb : 0);
      resident.z = position.z - tangent.x * out * resident.side;
      resident.heading = Math.atan2(tangent.x * resident.dir, tangent.z * resident.dir);

      // Phase from distance walked, so the feet keep up with the body. The
      // half-step offset per resident stops four hundred people marching.
      const phase = resident.phase + resident.d * STRIDE;
      const swing = Math.sin(phase);
      // The body rises twice per stride, at the top of each step.
      const bob = Math.abs(Math.cos(phase)) * BOB;
      const isFocused = focused === resident.id;
      const scale =
        (isFocused ? bodyScale * (2.1 + Math.sin(shared.uTime.value * 3) * 0.25) : bodyScale) *
        rigScale;

      // The character's own frame: on the pavement, facing along the path.
      dummy.position.set(resident.x, resident.y + bob, resident.z);
      dummy.rotation.set(0, resident.heading, 0);
      dummy.scale.setScalar(scale);
      dummy.updateMatrix();
      bodyM.copy(dummy.matrix);

      tint.set(PUMA_COLORS[resident.puma] ?? DEFAULT_COLOR);
      if (isFocused) tint.offsetHSL(0, 0.15, 0.25);

      for (let m = 0; m < partMeshes.length; m++) {
        const mesh = partMeshes[m];
        const { group: limb, role } = mesh.userData.part;
        const pivotY = mesh.userData.pivotY;
        if (limb === 'body') {
          outM.copy(bodyM);
        } else {
          // Swing about the joint. A limb's geometry was baked with its pivot at
          // the origin, so this is a bare rotation — then it is lifted back to
          // where the joint actually sits before the body transform is applied.
          const side = limb === 'armL' || limb === 'legL' ? 1 : -1;
          // Arms lead the leg on the OTHER side, which is what makes a walk
          // read as a walk rather than a shuffle.
          const arm = limb === 'armL' || limb === 'armR';
          const angle = swing * side * (arm ? -ARM_SWING : LEG_SWING);
          limbM.makeRotationX(angle);
          limbM.elements[13] = pivotY; // translate the joint back up
          outM.multiplyMatrices(bodyM, limbM);
        }
        mesh.setMatrixAt(bodies, outM);
        mesh.setColorAt(bodies, paintFor(resident, role, tint, isFocused));
      }
      bodies++;

      const dist = Math.hypot(resident.x - camX, resident.z - camZ);
      if (dist >= badgeRadius) continue;
      eligible++;
      shortlist.push(resident);
      resident.dist = dist;
    }

    // Sort by distance, then take an evenly-strided sample of that order. Two
    // failure modes this is threading between: handing slots out in FILE order
    // leaves the person under the camera untagged while somebody across town
    // gets the bubble, and handing them all to the NEAREST collapses the whole
    // set into one corner of a city view — which is exactly what a low tier
    // did, 45 bubbles in a knot instead of scattered over San Francisco.
    // Striding the sorted list keeps index 0 (the nearest) and spreads the rest
    // across the full distance range, at every altitude.
    shortlist.sort((a, b) => a.dist - b.dist);
    const stride = Math.max(1, Math.ceil(shortlist.length / badgeCap));
    const near = badgeRadius * 0.72; // fade over the outer quarter of the ring
    for (let i = 0; i < shortlist.length; i += stride) {
      const resident = shortlist[i];
      // The cap is on the TOTAL across all four meshes, not per mood — each is
      // allocated for the worst case of every visible badge being the same one.
      if (badges >= badgeCapacity) break;
      const dist = resident.dist;
      const fade = dist < near ? 1 : Math.max(0, 1 - (dist - near) / Math.max(1, badgeRadius - near));
      // Proportional to THIS resident's distance => constant size on screen.
      const scaleAt = Math.max(BADGE_SCALE_MIN, Math.min(BADGE_SCALE_MAX, dist / BADGE_REF_DIST));
      dummy.position.set(resident.x, resident.y + BADGE_Y * scaleAt, resident.z);
      dummy.quaternion.copy(cameraQuaternion);
      dummy.scale.setScalar(scaleAt * fade);
      dummy.updateMatrix();
      // Into the mesh for THIS resident's mood. `badges` still counts the total
      // so the cap and the eligibility maths are unchanged; each mesh keeps its
      // own running index.
      const moodIdx = resident.moodIdx;
      badgeMeshes[moodIdx].setMatrixAt(badgeFill[moodIdx]++, dummy.matrix);
      badges++;
    }
    shortlist.length = 0;

    // Every part, not just one: they are ten separate InstancedMeshes and each
    // carries its own instance buffers. Flushing only the body left the arms
    // and legs frozen wherever they were on the first frame.
    for (let m = 0; m < partMeshes.length; m++) {
      const mesh = partMeshes[m];
      mesh.count = bodies;
      mesh.instanceMatrix.needsUpdate = true;
      if (mesh.instanceColor) mesh.instanceColor.needsUpdate = true;
    }
    for (let m = 0; m < badgeMeshes.length; m++) {
      badgeMeshes[m].count = badgeFill[m];
      badgeMeshes[m].instanceMatrix.needsUpdate = true;
    }
    eligibleLast = eligible;
  }

  load();

  return {
    group,
    update,
    containsResidents,
    setToy(toy) {
      bodyScale = toy ? 1.35 : 1;
    },
    setQuality(tier) {
      const low = tier === 'low';
      cap = low ? LOW_CAP : MAX_RESIDENTS;
      badgeCap = low ? LOW_BADGES : MAX_BADGES;
    },
    // Whether this id is in the cast at all. Distinct from locate() returning
    // null, which only means "not standing anywhere YET" — one is a dead end
    // and the other is a wait, and the caller has to be able to tell them
    // apart to say anything true about it.
    knows(id) {
      return residents.some((r) => r.id === id);
    },

    // The middle of a resident's neighbourhood, in world metres, whether or not
    // a single street of it has streamed. This comes from the PUMA polygons,
    // which are loaded up front with the cast — which is what makes fetching
    // somebody possible: the city has to be told where to go BEFORE it can load
    // the ground they are standing on, and their own position is exactly what
    // is not known yet.
    neighbourhoodOf(id) {
      const resident = residents.find((r) => r.id === id);
      if (!resident) return null;
      const mine = areas.filter((a) => a.puma === resident.puma);
      if (!mine.length) return null;
      // Area centroids averaged, so a PUMA made of several neighbourhoods aims
      // at the middle of the whole thing rather than at whichever one happens
      // to be first.
      let x = 0;
      let z = 0;
      let n = 0;
      for (const area of mine) {
        for (const ring of area.rings) {
          for (let i = 0; i < ring.length; i += 2) {
            x += ring[i];
            z += ring[i + 1];
            n++;
          }
        }
      }
      return n ? { x: x / n, z: z / n, puma: resident.puma, name: resident.name } : null;
    },

    // Where a named resident is standing right now, for "take me to this
    // person". Returns null when they have not been seated — their PUMA's
    // streets may not have streamed in yet, or they may not be in the cast at
    // all — and the caller is expected to say so rather than fly somewhere
    // arbitrary.
    locate(id) {
      const resident = residents.find((r) => r.id === id);
      if (!resident || !resident.placed) return null;
      return {
        x: resident.x,
        y: resident.y,
        z: resident.z,
        name: resident.name,
        puma: resident.puma,
      };
    },

    // Ring the person you flew to, so they are findable among four hundred
    // identical spheres. One id at a time; null clears it.
    focus(id) {
      focused = id;
    },

    // The whole cast: every resident the bake carries, seated on a street or
    // not. This is what the feed's header states, so it must not fall as
    // neighbourhoods unload — how many are actually walking right now is
    // `stats.seated`.
    get castCount() {
      return residents.length;
    },

    get residentCount() {
      return bodyMesh ? bodyMesh.count : 0;
    },
    // Console-side diagnosis: how many residents found a street to walk, and
    // how much street each PUMA has streamed in so far.
    get stats() {
      const streets = {};
      for (const [puma, pool] of pathsByPuma) streets[puma] = pool.length;
      let seated = 0;
      for (const resident of residents) if (resident.placed) seated++;
      return {
        ready,
        total: residents.length,
        seated,
        drawn: this.residentCount,
        owned: [...ownedPumas],
        shared: [...livePumas].filter((puma) => !ownedPumas.has(puma)),
        streets,
        badgeRadius: Math.round(badgeRadius),
        inBadgeRange: eligibleLast,
        badgesDrawn: badgeMeshes.reduce((n, m) => n + m.count, 0),
        badgesByMood: Object.fromEntries(
          badgeMeshes.map((m, i) => [MOOD_BADGES[i].key, m.count])
        ),
      };
    },
  };
}
