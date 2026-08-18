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
  MeshLambertMaterial,
  Object3D,
  PlaneGeometry,
  SphereGeometry,
  SRGBColorSpace,
  Vector3,
} from 'three';

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

const WALK_SPEED = 1.25; // m/s, an unhurried pace
const BODY_RADIUS = 0.85;

// Badges follow the ZOOM, not a fixed distance in metres — the same reasoning
// as the Muni route bubbles (see muni.js): this camera spends most of its life
// in the air, so a radius tuned for street level would label nothing, and the
// bubbles are scaled with distance to hold a roughly constant size on screen.
// Clutter is bounded by MAX_BADGES, not by the radius.
const MAX_BADGES = 140;
const LOW_BADGES = 45;
const BADGE_W = 5.2;
const BADGE_H = 5.2;
const BADGE_Y = 4.4; // height of the QUAD CENTRE; the tail tip drops ~0.36 x H
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
function buildBadgeTexture() {
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

  ctx.font = '104px "Apple Color Emoji", "Segoe UI Emoji", "Noto Color Emoji", sans-serif';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillText('🧍', bx + bw / 2, by + bh / 2 + 4);

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
  let badgeMesh = null;
  let cap = MAX_RESIDENTS;
  let badgeCap = MAX_BADGES;
  let badgeRadius = BADGE_RADIUS_MAX;
  let bodyScale = 1;
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

  function build() {
    bodyMesh = new InstancedMesh(
      new SphereGeometry(BODY_RADIUS, 10, 7),
      new MeshLambertMaterial({}),
      residents.length
    );
    bodyMesh.name = 'pums-residents';
    bodyMesh.instanceMatrix.setUsage(DynamicDrawUsage);
    bodyMesh.frustumCulled = false;
    bodyMesh.count = 0;
    group.add(bodyMesh);

    badgeMesh = new InstancedMesh(
      new PlaneGeometry(BADGE_W, BADGE_H),
      new MeshBasicMaterial({ map: buildBadgeTexture(), transparent: true, depthWrite: false, alphaTest: 0.02 }),
      Math.min(residents.length, MAX_BADGES)
    );
    badgeMesh.name = 'pums-resident-badges';
    badgeMesh.instanceMatrix.setUsage(DynamicDrawUsage);
    badgeMesh.frustumCulled = false;
    badgeMesh.renderOrder = 4;
    badgeMesh.count = 0;
    group.add(badgeMesh);
  }

  async function load() {
    let people;
    let pumas;
    try {
      const [a, b] = await Promise.all([fetch(`${DATA}people.json`), fetch(`${DATA}pumas.json`)]);
      if (!a.ok || !b.ok) throw new Error(`${a.status}/${b.status}`);
      [people, pumas] = await Promise.all([a.json(), b.json()]);
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
    const zoomRadius = Math.max(
      BADGE_RADIUS_MIN,
      Math.min(BADGE_RADIUS_MAX, Math.max(0, cameraPos.y) * BADGE_RADIUS_PER_M)
    );
    badgeRadius = Math.min(badgeRadius, zoomRadius);

    let bodies = 0;
    let badges = 0;
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

      const bob = Math.abs(Math.sin(resident.phase + resident.d * 1.6)) * 0.12;
      dummy.position.set(resident.x, resident.y + BODY_RADIUS + bob, resident.z);
      dummy.rotation.set(0, resident.heading, 0);
      dummy.scale.setScalar(bodyScale);
      dummy.updateMatrix();
      bodyMesh.setMatrixAt(bodies, dummy.matrix);
      bodyMesh.setColorAt(bodies, tint.set(PUMA_COLORS[resident.puma] ?? DEFAULT_COLOR));
      bodies++;

      const dist = Math.hypot(resident.x - camX, resident.z - camZ);
      if (dist >= badgeRadius) continue;
      eligible++;
      shortlist.push(resident);
      resident.dist = dist;
    }

    // Nearest first, then hand out the slots. Iteration order would otherwise
    // spend all of them on whoever happens to sit early in the file — with 432
    // residents and 140 badges that reliably meant the person under the camera
    // went untagged while somebody across town got the bubble.
    if (shortlist.length > badgeCap) {
      shortlist.sort((a, b) => a.dist - b.dist);
      shortlist.length = badgeCap;
    }
    const near = badgeRadius * 0.72; // fade over the outer quarter of the ring
    for (const resident of shortlist) {
      if (badges >= badgeMesh.instanceMatrix.count) break;
      const dist = resident.dist;
      const fade = dist < near ? 1 : Math.max(0, 1 - (dist - near) / Math.max(1, badgeRadius - near));
      // Proportional to THIS resident's distance => constant size on screen.
      const scaleAt = Math.max(BADGE_SCALE_MIN, Math.min(BADGE_SCALE_MAX, dist / BADGE_REF_DIST));
      dummy.position.set(resident.x, resident.y + BADGE_Y * scaleAt, resident.z);
      dummy.quaternion.copy(cameraQuaternion);
      dummy.scale.setScalar(scaleAt * fade);
      dummy.updateMatrix();
      badgeMesh.setMatrixAt(badges, dummy.matrix);
      badges++;
    }
    shortlist.length = 0;

    bodyMesh.count = bodies;
    bodyMesh.instanceMatrix.needsUpdate = true;
    if (bodyMesh.instanceColor) bodyMesh.instanceColor.needsUpdate = true;
    badgeMesh.count = badges;
    badgeMesh.instanceMatrix.needsUpdate = true;

    // Breathe the radius toward whatever keeps roughly badgeCap on screen,
    // bounded by what the current zoom allows.
    const target = eligible > badgeCap ? badgeRadius * 0.94 : badgeRadius * 1.06;
    badgeRadius = Math.max(120, Math.min(zoomRadius, badgeRadius + (target - badgeRadius) * Math.min(1, dt * 1.5)));
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
        badgeRadius,
      };
    },
  };
}
