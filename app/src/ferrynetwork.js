// The SF Bay Ferry network as baked geometry: route alignments across the Bay,
// the terminals boats tie up at, and each route's official livery colour.
//
// Baked by pipeline/ferry-shapes.mjs from 511's GTFS static for agency SB
// (WETA). One parse, shared by everything that needs it — the terminal markers
// and, when the route walls land, those too — because the browser cache makes
// the fetch free but a second JSON parse of the chunk is not.
//
// Golden Gate Ferry (agency GF, Sausalito and Larkspur) is a DIFFERENT feed and
// is not in here; its boats are legitimately absent from the Bay today.

const URL = `${import.meta.env.BASE_URL}tiles/ferry-shapes.bin`;
const MAGIC = 0x46525931; // 'FRY1'

// The Bay is one 30 km x 30 km water plane centred on the projection origin
// (app/src/water.js). Four of the fifteen terminals are outside it — Harbor Bay,
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

  const routes = new Map();
  for (const [id, r] of Object.entries(meta.routes || {})) {
    routes.set(id, {
      id,
      name: r.name || id,
      // Never null downstream: an unpainted route still has to draw as
      // something, and the toy palette's neutral is the honest choice.
      color: r.color || '#7f8c94',
      textColor: r.textColor || '#ffffff',
      shapes: r.shapes || [],
    });
  }

  const shapes = (meta.shapes || []).map((s) => ({
    vertexOffset: s.vertexOffset,
    vertexCount: s.vertexCount,
    lengthM: s.lengthM,
  }));

  // The Ferry Building is three separate gate stops (E/F/G) about 30 m apart
  // sharing parent_station 7201. Three markers there would collide into an
  // unreadable smear, so gates are grouped onto their parent and drawn once, at
  // the mean of the gates. Everything else is its own group of one.
  const terminals = (meta.terminals || []).map((t) => ({ ...t, routes: t.routes || [] }));
  const groups = new Map();
  for (const t of terminals) {
    const key = t.parent || t.id;
    let g = groups.get(key);
    if (!g) {
      groups.set(key, (g = { id: key, name: t.name, x: 0, z: 0, members: [], routes: new Set() }));
    }
    g.members.push(t);
    for (const r of t.routes) g.routes.add(r);
  }
  const berths = [];
  for (const g of groups.values()) {
    g.x = g.members.reduce((sum, t) => sum + t.x, 0) / g.members.length;
    g.z = g.members.reduce((sum, t) => sum + t.z, 0) / g.members.length;
    // A grouped berth is named for the shared place, not for whichever gate
    // happened to sort first: "San Francisco Ferry Building Gate E" is the wrong
    // label for a pin standing over all three.
    if (g.members.length > 1) g.name = commonName(g.members.map((t) => t.name)) || g.name;
    berths.push({
      id: g.id,
      name: g.name,
      x: g.x,
      z: g.z,
      gates: g.members.length,
      routes: [...g.routes].sort(),
      inScene: inScene(g.x, g.z),
    });
  }
  berths.sort((a, b) => a.name.localeCompare(b.name));

  return { routes, shapes, verts, terminals, berths };
}

// Longest shared leading words of a set of gate names — "San Francisco Ferry
// Building Gate E/F/G" collapses to "San Francisco Ferry Building".
//
// The trailing qualifier has to go with it: the shared run of those three names
// ends in "Gate", because only the letter after it differs, and a pin labelled
// "…Ferry Building Gate" reads as a truncation bug rather than a place.
const QUALIFIER = /^(gate|berth|slip|dock|pier|terminal)$/i;

function commonName(names) {
  if (!names.length) return null;
  const split = names.map((n) => n.split(/\s+/));
  const head = [];
  for (let i = 0; i < split[0].length; i++) {
    const word = split[0][i];
    if (!split.every((parts) => parts[i] === word)) break;
    head.push(word);
  }
  // Only when the shared run actually stops short of a member's full name: if
  // every gate is called the same thing, "Terminal" is the name, not a dangling
  // qualifier, and stripping it would rename the place.
  const truncates = split.some((parts) => parts.length > head.length);
  if (truncates) {
    while (head.length > 1 && QUALIFIER.test(head[head.length - 1])) head.pop();
  }
  return head.join(' ').replace(/[\s,-]+$/, '') || null;
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
