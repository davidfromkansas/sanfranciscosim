// Real Muni bus stops — the 2,976 places a bus actually calls at.
//
// Baked by pipeline/muni-shapes.mjs from GTFS `stops` + `stop_times`, so a stop
// exists here only if some bus trip stops there. Both the surface bus modes are
// included: motor coaches and trolley coaches look alike to a rider and stop at
// the same kind of stop. Rail platforms and cable stops are NOT here — they are
// not bus stops and must never get a bus shelter.
//
// One parse, shared by the two consumers that need it:
//   * city.js scopes the stops to a streamed cell and sends them to the tile
//     worker, which stands a shelter at each (app/src/streetplan.js).
//   * munistoplayer.js draws the indicators and answers picks.
//
// The shapes file is fetched by muni.js too, for vehicle movement; the browser
// cache makes that one request, and this module keeps the JSON parse to one.

const SHAPES_URL = `${import.meta.env.BASE_URL}tiles/muni-shapes.bin`;
const SHAPES_MAGIC = 0x4d554e31; // 'MUN1'

let promise = null;

function parse(buf) {
  const view = new DataView(buf);
  if (view.getUint32(0, true) !== SHAPES_MAGIC) throw new Error('shapes bad magic');
  const jsonLen = view.getUint32(8, true);
  const meta = JSON.parse(new TextDecoder().decode(new Uint8Array(buf, 16, jsonLen)));

  const strings = meta.strings || [];
  const routeIds = meta.busRoutes || [];
  const routeNames = (meta.busRouteNames || []).map((i) => strings[i] ?? null);
  const stops = [];
  for (const [id, entry] of Object.entries(meta.busStops || {})) {
    const [nameIdx, x, z, routes] = entry;
    stops.push({
      id,
      name: strings[nameIdx] ?? id,
      x,
      z,
      // Route designations as a rider reads them ("38R"), sorted so a card and
      // a concierge answer list them the same way every time.
      routes: (routes || []).map((i) => routeIds[i]).filter(Boolean).sort(compareRoute),
      routeNames: (routes || []).map((i) => routeNames[i]).filter(Boolean),
    });
  }
  const byId = new Map(stops.map((s) => [s.id, s]));
  return { stops, byId, routeIds, routeNames };
}

// "5" before "5R" before "9", and letter routes last — numeric where possible so
// a stop does not list 14, 14R, 2, 22.
export function compareRoute(a, b) {
  const na = parseInt(a, 10);
  const nb = parseInt(b, 10);
  if (Number.isNaN(na) && Number.isNaN(nb)) return a.localeCompare(b);
  if (Number.isNaN(na)) return 1;
  if (Number.isNaN(nb)) return -1;
  return na - nb || a.localeCompare(b);
}

export function loadBusStops() {
  if (promise) return promise;
  promise = fetch(SHAPES_URL)
    .then((res) => {
      if (!res.ok) throw new Error(`shapes ${res.status}`);
      return res.arrayBuffer();
    })
    .then(parse)
    .catch((error) => {
      // A missing bake is not fatal anywhere: placement falls back to no
      // shelters and the indicator layer simply has nothing to draw.
      console.warn(`sf-munistops: no bus stops (${error.message}) — shelters and stop markers are off`);
      return { stops: [], byId: new Map(), routeIds: [], routeNames: [] };
    });
  return promise;
}

/** Stops inside a cell's bounds, as the flat array the tile worker is sent. */
export function stopsInBounds(table, minX, minZ, maxX, maxZ) {
  const out = [];
  for (const stop of table.stops) {
    if (stop.x < minX || stop.x >= maxX || stop.z < minZ || stop.z >= maxZ) continue;
    out.push(stop.x, stop.z);
  }
  return out;
}
