// The SF Bay Ferry network as baked geometry: route alignments across the Bay,
// the terminals boats tie up at, and each route's official livery colour.
//
// Baked by pipeline/ferry-shapes.mjs from 511's GTFS static for ALL FOUR ferry
// operators — SB (SF Bay Ferry), GF (Golden Gate), AF (Angel Island–Tiburon)
// and TF (Treasure Island) — so Sausalito, Tiburon, Larkspur, Angel Island and
// Treasure Island are on the map alongside the WETA crossings. Route ids are
// namespaced by operator ("GF:SSSF"), because the agencies reuse each other's
// short codes and stop ids freely.
//
// Only SB publishes live vessel positions, so the other three contribute route
// walls and terminals but never a moving hull.
//
// One parse, shared by the terminal markers, the route walls and the badges:
// the browser cache makes the fetch free but a second parse of the chunk is not.

import { resolveRouteColors } from './ferry-palette.js';

const URL = `${import.meta.env.BASE_URL}tiles/ferry-shapes.bin`;
const MAGIC = 0x46525931; // 'FRY1'

// The Bay is one 30 km x 30 km water plane centred on the projection origin
// (app/src/water.js). Five berths are outside it — Harbor Bay, Larkspur,
// Richmond, Vallejo and Mare Island — and a marker out there would float over
// void. Same inset ferries.js uses for hulls, for the same reason.
export const SCENE_HALF_EXTENT = 15000 - 500;

let promise = null;

export function inScene(x, z) {
  return Math.abs(x) <= SCENE_HALF_EXTENT && Math.abs(z) <= SCENE_HALF_EXTENT;
}

function parse(buf) {
  const view = new DataView(buf);
  if (view.getUint32(0, true) !== MAGIC) throw new Error('ferry-shapes bad magic');
  const jsonLen = view.getUint32(8, true);
  const floatCount = view.getUint32(12, true);
  const meta = JSON.parse(new TextDecoder().decode(new Uint8Array(buf, 16, jsonLen)));
  // [x, z, s] triplets for every shape back to back; s = cumulative metres.
  const verts = new Float32Array(buf, 16 + jsonLen, floatCount);

  const operators = new Map(Object.entries(meta.operators || {}));
  const entries = Object.entries(meta.routes || {});
  // Golden Gate publishes ONE red for all five of its routes, so the liveries
  // alone cannot tell the crossings apart. ferry-palette.js keeps every colour
  // that is already unique and spreads only the ones that collide.
  const drawn = resolveRouteColors(
    entries.map(([id, r]) => ({ id, color: r.color || '#7f8c94' }))
  );
  const routes = new Map();
  for (const [id, r] of entries) {
    routes.set(id, {
      id,
      name: r.name || id,
      // What to draw with: unique liveries survive this untouched.
      color: drawn.get(id) || r.color || '#7f8c94',
      // What the operator actually publishes, for anything stating the truth.
      publishedColor: r.color || null,
      textColor: r.textColor || '#ffffff',
      operator: r.operator || null,
      operatorName: r.operatorName || null,
      live: Boolean(r.live),
      shapes: r.shapes || [],
    });
  }

  const shapes = (meta.shapes || []).map((s) => ({
    vertexOffset: s.vertexOffset,
    vertexCount: s.vertexCount,
    lengthM: s.lengthM,
  }));

  // Four operators serve the same water, so the same physical dock appears
  // several times: the Ferry Building is three SB gate stops (E/F/G) AND two GF
  // gates (B/C), and Tiburon is one stop in the GF feed and another in the AF
  // feed. Grouping by parent_station alone only catches the first case, because
  // parent stations never cross agencies. So berths are clustered by DISTANCE:
  // anything within MERGE_M of an existing cluster joins it and contributes its
  // routes. 250 m is measured, not guessed: SB's Ferry Building gates and the
  // GF/TF gates on the same building sit 233 m apart, so anything tighter draws
  // two pins on the flagship terminal. It does also merge Oakland Ferry
  // Terminal with the Water Shuttle dock 205 m away, which is the right answer
  // for a pin — they are both Jack London Square, two minutes' walk apart.
  const MERGE_M = 250;
  const terminals = (meta.terminals || []).map((t) => ({ ...t, routes: t.routes || [] }));
  const clusters = [];
  for (const t of terminals) {
    const hit = clusters.find((c) => Math.hypot(c.x - t.x, c.z - t.z) <= MERGE_M);
    if (hit) {
      hit.members.push(t);
      hit.x = hit.members.reduce((sum, m) => sum + m.x, 0) / hit.members.length;
      hit.z = hit.members.reduce((sum, m) => sum + m.z, 0) / hit.members.length;
    } else {
      clusters.push({ members: [t], x: t.x, z: t.z });
    }
  }

  const berths = clusters.map((c) => {
    c.title = berthName(c.members);
    const routes = new Set();
    const berthOperators = new Set();
    for (const m of c.members) {
      for (const r of m.routes) routes.add(r);
      if (m.operator) berthOperators.add(m.operator);
    }
    return {
      // Named for the stop the cluster is titled after, so an id is stable
      // across a re-bake as long as that stop exists.
      id: c.title.id,
      name: c.title.name,
      x: c.x,
      z: c.z,
      stops: c.members.length,
      operators: [...berthOperators].sort(),
      operatorNames: [...berthOperators]
        .sort()
        .map((id) => operators.get(id)?.name || id),
      routes: [...routes].sort(),
      inScene: inScene(c.x, c.z),
    };
  });
  berths.sort((a, b) => a.name.localeCompare(b.name));

  // Timetable playback data for the operators with no live feed; absent when
  // every operator publishes positions.
  const schedule = meta.schedule || { services: {}, trips: [] };

  return { routes, shapes, verts, terminals, berths, operators, schedule };
}

// What to call a cluster of stops, and which stop lends it its id.
//
// The feeds name the same dock several ways, and two of those names carry
// service caveats rather than places: Golden Gate calls Angel Island "Angel
// Island-No Service to Tiburon" and Tiburon "Tiburon-No Service to Angel
// Island". Those belong on a timetable, not on a pin — and a pin is not
// claiming anything about service, so trimming them is legible, not inaccurate.
// Gate suffixes go the same way, since the pin stands over all the gates.
const CAVEAT = /\s*[-–—]\s*no service.*$/i;
const GATE_SUFFIX = /\s*[-–—]?\s*\bgate\s+\w+$/i;

function tidyName(name) {
  return String(name).replace(CAVEAT, '').replace(GATE_SUFFIX, '').replace(/[\s,–—-]+$/, '').trim();
}

function berthName(members) {
  const tallies = new Map();
  for (const m of members) {
    const name = tidyName(m.name) || m.name;
    const entry = tallies.get(name) || { name, count: 0, id: m.id };
    entry.count++;
    tallies.set(name, entry);
  }
  let candidates = [...tallies.values()];
  // A name that EXTENDS another candidate is the more specific one, and wins
  // outright: the Ferry Building cluster offers both "San Francisco" (Golden
  // Gate's and Treasure Island's word for it) and "San Francisco Ferry
  // Building", and the vaguer one would otherwise win on a count tie.
  const extended = candidates.filter((c) =>
    candidates.some((other) => other !== c && c.name.startsWith(`${other.name} `))
  );
  if (extended.length) candidates = extended;
  // Otherwise most-used wins, and ties go to the shortest, which is reliably
  // the plain place name ("Angel Island" over "Ayala Cove Pier - Angel Island").
  const best = candidates.sort((a, b) => b.count - a.count || a.name.length - b.name.length)[0];
  return { id: best.id, name: best.name };
}

// Resolves to the parsed network, or null if the bake is missing or malformed.
// Never throws: rule 3 — a missing bake costs the terminals and the route
// walls, not the city.
export function loadFerryNetwork() {
  if (promise) return promise;
  promise = (async () => {
    try {
      const res = await fetch(URL);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return parse(await res.arrayBuffer());
    } catch (error) {
      console.warn(`sf-ferries: no ferry route data (${error.message}) — terminals and route lines stay off`);
      return null;
    }
  })();
  return promise;
}
