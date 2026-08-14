// /api/flights — real aircraft over San Francisco, from community ADS-B.
//
// Every airborne aircraft within 30 NM of the projection origin, normalised to
// the city's metric contract. No key, ever: these are volunteer receiver
// networks that serve open data anonymously, which is what keeps the air layer
// inside iron rule 4.
//
// WHY NOT OPENSKY (measured 2026-08-13, not assumed):
//   - It blocks datacenter IPs. On Vercel this feed would run from exactly the
//     addresses it refuses, so it would be dead weight in production — the same
//     conclusion nycsim reached ("in production the first of these IS the
//     source").
//   - Since 2026-03-18 it requires an OAuth2 client-credentials key for its
//     usable tier (4000 credits/day; 400 anonymous). A required key for the
//     PRIMARY path collides with rule 4.
//   - /states/all carries no ICAO type designator and its numeric category
//     reads 0 for ~90% of aircraft, so airframes have to be guessed. The readsb
//     aggregators below hand us `t: "B739"` and `category: "A3"` directly,
//     which is what lets the scene put a helicopter model on a helicopter.
// If the two sources here ever both fail, adding OpenSky as a third is a small
// change — but it would not have helped on the day this was written.
//
// Sources, tried in order (identical readsb v2 schema, so one parser):
//   adsb.lol       verified 200, 85 aircraft over SF
//   adsb.fi        verified 200, same shape — independent receiver network
// (api.airplanes.live answered 403 from this network on 2026-08-13; it is left
// out rather than shipped as a fallback that has never been seen to work.)

import { registerFeed } from '../feedcore.mjs';

// Centre = the city's projection origin (AGENTS.md, "Coordinate conventions").
// 30 NM reaches SFO, OAK, SJC's north end and the whole Bay approach fan, which
// is every aircraft that can enter the 30 km scene plus context either side.
const LAT0 = 37.77;
const LON0 = -122.4375;
const RADIUS_NM = 30;

const SOURCES = [
  ['adsb.lol', `https://api.adsb.lol/v2/point/${LAT0}/${LON0}/${RADIUS_NM}`],
  ['adsb.fi', `https://opendata.adsb.fi/api/v2/lat/${LAT0}/lon/${LON0}/dist/${RADIUS_NM}`],
];

const TTL_MS = 20 * 1000; // ~180 upstream calls/h per warm instance; the CDN absorbs the rest
const STALE_MS = 5 * 60 * 1000; // aircraft move ~250 m/s — older than this is fiction
const BACKOFF_MS = 60 * 1000;
const TIMEOUT_MS = 8 * 1000;
const STALE_FIX_S = 60; // a position this old is dropped rather than dead-reckoned
const MAX_AIRCRAFT = 120; // payload bound; the scene draws far fewer

const FT = 0.3048; // ft -> m
const KT = 0.514444; // kn -> m/s
const FPM = 0.00508; // ft/min -> m/s

// ADS-B emitter categories. A1 light / A2 small / A3 large / A4 high-vortex
// large / A5 heavy / A6 high-performance / A7 rotorcraft; B* are gliders,
// balloons and skydivers; C* are SURFACE vehicles and obstacles, which is why
// the raw feed shows 48 "aircraft" on the ground at SFO that are pushback tugs.
const SURFACE = /^C/;

// Rotorcraft actually seen over the Bay: SFPD/CHP patrol, medevac to SF General
// and Stanford, news birds, PG&E line patrol, and the Coast Guard air station
// at SFO. Type designators back up the emitter category, which many older
// transponders never set.
const HELI_TYPES = new Set([
  'A109', 'A119', 'A139', 'A169', 'A189', 'AS50', 'AS55', 'AS65', 'AW09', 'AW139', 'AW169',
  'B06', 'B06T', 'B222', 'B230', 'B407', 'B412', 'B427', 'B429', 'B430', 'B505', 'BK17',
  'EC20', 'EC30', 'EC35', 'EC45', 'EC55', 'EC75', 'EXPL', 'GAZL', 'H500', 'H60', 'H47',
  'MD52', 'MD60', 'NH90', 'R22', 'R44', 'R66', 'S61', 'S70', 'S76', 'S92',
]);

// Piston/turboprop singles and light twins — the Cessnas and Cirruses out of
// San Carlos, Palo Alto, Hayward and Oakland North Field that make up a quarter
// of the traffic here. They get the small propeller airframe, not an airliner.
const LIGHT_TYPES = new Set([
  'AC11', 'BE20', 'BE33', 'BE35', 'BE36', 'BE58', 'BE9L', 'C150', 'C152', 'C170', 'C172',
  'C175', 'C177', 'C180', 'C182', 'C185', 'C195', 'C206', 'C207', 'C208', 'C210', 'C310',
  'C337', 'C414', 'C421', 'CH7A', 'DA20', 'DA40', 'DA42', 'DHC2', 'DHC6', 'DR40', 'E110',
  'GLST', 'M20P', 'M20T', 'P28A', 'P28B', 'P28R', 'P28T', 'P32R', 'P46T', 'PA11', 'PA18',
  'PA23', 'PA24', 'PA25', 'PA28', 'PA30', 'PA31', 'PA32', 'PA34', 'PA44', 'PA46', 'PC12',
  'RV4', 'RV6', 'RV7', 'RV8', 'RV9', 'S22T', 'SF50', 'SR20', 'SR22', 'T206', 'TBM7', 'TBM8',
  'TBM9', 'TEX2', 'VELO',
]);

// The three airframes the scene can draw. Everything the feed can tell us
// collapses to exactly one of these, because a model it cannot draw is worse
// than an honest approximation.
function kindFor(category, type) {
  const t = (type || '').toUpperCase();
  if (category === 'A7' || HELI_TYPES.has(t)) return 'heli';
  if (LIGHT_TYPES.has(t)) return 'light';
  if (t) return 'airliner'; // a known type that is neither → jet/turboprop airliner
  // No type designator: fall back to the emitter category. A1 (light) and A2
  // (small) are the light-aircraft weight classes.
  if (category === 'A1' || category === 'A2') return 'light';
  return 'airliner';
}

// What the aircraft is doing, from vertical rate and altitude. Cheap, and it is
// what makes a card read "descending into SFO" instead of dumping numbers.
function phaseFor(altM, vrateMs) {
  if (vrateMs > 2.5) return 'climbing';
  if (vrateMs < -2.5) return altM < 2500 ? 'on approach' : 'descending';
  return altM > 7000 ? 'cruising' : 'level';
}

// Squawks that mean something is wrong: 7500 unlawful interference, 7600 radio
// failure, 7700 general emergency. Rare, and worth surfacing when it happens.
const SQUAWK_EMERGENCY = { 7500: 'hijack', 7600: 'radio failure', 7700: 'emergency' };

function emergencyFor(squawk, emergency) {
  const code = SQUAWK_EMERGENCY[Number(squawk)];
  if (code) return code;
  // readsb's own field: 'none' when nothing is declared.
  const declared = typeof emergency === 'string' ? emergency.trim().toLowerCase() : '';
  return declared && declared !== 'none' ? declared : null;
}

// ------------------------------------------------------------------ routes
//
// ADS-B carries no origin or destination — a transponder broadcasts identity
// and state, not intent. The route comes from adsbdb.com, a free no-key
// database keyed by CALLSIGN (UAL589 -> DEN-RIC), resolved here rather than in
// the browser so one warm instance's cache serves every visitor and the client
// never makes a second round trip.
//
// Two things keep this inside a free service's good graces:
//   - A callsign's route is the same all day, so resolutions cache for 12 h and
//     MISSES cache too (6 h). Without negative caching the GA fleet would be
//     re-queried forever, since those never resolve.
//   - Only NEW callsigns are looked up, at most ROUTE_BUDGET per refresh, so a
//     busy sky resolves over a couple of minutes instead of in one burst.
const ADSBDB = 'https://api.adsbdb.com/v0/callsign/';
const ROUTE_TTL_MS = 12 * 60 * 60 * 1000;
const ROUTE_MISS_TTL_MS = 6 * 60 * 60 * 1000;
const ROUTE_BUDGET = 8; // new lookups per refresh
const ROUTE_TIMEOUT_MS = 4 * 1000;
const ROUTE_CACHE_MAX = 2000;

// callsign -> { at, route: {...} | null }
const routes = new Map();

function cachedRoute(callsign) {
  const hit = routes.get(callsign);
  if (!hit) return undefined;
  const ttl = hit.route ? ROUTE_TTL_MS : ROUTE_MISS_TTL_MS;
  if (Date.now() - hit.at > ttl) {
    routes.delete(callsign);
    return undefined;
  }
  return hit.route;
}

function rememberRoute(callsign, route) {
  // Bounded: drop the oldest insertion when full (Map preserves insert order).
  if (routes.size >= ROUTE_CACHE_MAX) routes.delete(routes.keys().next().value);
  routes.set(callsign, { at: Date.now(), route });
}

function airport(node) {
  if (!node) return null;
  const iata = node.iata_code || null;
  const icao = node.icao_code || null;
  const city = node.municipality || null;
  const name = node.name || null;
  if (!iata && !icao && !city) return null;
  return { iata, icao, city, name, country: node.country_name || null };
}

async function lookupRoute(callsign) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), ROUTE_TIMEOUT_MS);
  try {
    const res = await fetch(ADSBDB + encodeURIComponent(callsign), {
      signal: controller.signal,
      headers: { accept: 'application/json' },
    });
    // 404 is the normal answer for a private tail number, not a failure.
    if (res.status === 404) return null;
    if (!res.ok) throw new Error(`route-${res.status}`);
    const body = await res.json();
    const leg = body?.response?.flightroute;
    if (!leg) return null;
    const from = airport(leg.origin);
    const to = airport(leg.destination);
    if (!from && !to) return null;
    return { from, to };
  } finally {
    clearTimeout(timer);
  }
}

// A callsign that IS the tail number is a private/GA flight with no scheduled
// route — the single biggest source of wasted lookups, skipped for free.
function worthLookup(a) {
  if (!a.callsign) return false;
  if (a.registration && a.callsign.toUpperCase() === a.registration.toUpperCase()) return false;
  return true;
}

// Attach cached routes to everything, then spend the budget resolving the
// unknown ones. Best-effort throughout: a route lookup must never fail or
// delay the positions, which are the actual product here.
async function attachRoutes(aircraft) {
  const pending = [];
  for (const a of aircraft) {
    if (!worthLookup(a)) continue;
    const hit = cachedRoute(a.callsign);
    if (hit !== undefined) {
      if (hit) a.route = hit;
    } else if (pending.length < ROUTE_BUDGET && !pending.includes(a.callsign)) {
      pending.push(a.callsign);
    }
  }
  if (!pending.length) return;
  const settled = await Promise.allSettled(pending.map((cs) => lookupRoute(cs)));
  settled.forEach((result, i) => {
    if (result.status !== 'fulfilled') return; // transient: leave uncached, retry next refresh
    rememberRoute(pending[i], result.value);
  });
  // Fill in what just resolved so this very response carries it.
  for (const a of aircraft) {
    if (a.route || !a.callsign) continue;
    const hit = cachedRoute(a.callsign);
    if (hit) a.route = hit;
  }
}

function normalise(payload, now) {
  const out = [];
  for (const a of payload?.ac || payload?.aircraft || []) {
    const lat = Number(a.lat);
    const lon = Number(a.lon);
    if (!Number.isFinite(lat) || !Number.isFinite(lon)) continue;
    if (!a.hex) continue;

    // 'ground' is a legitimate alt_baro value; so is a missing one for an
    // aircraft with no barometric encoder. Either way it is not airborne data.
    if (a.alt_baro === 'ground') continue;
    const altFt = Number(a.alt_baro ?? a.alt_geom);
    if (!Number.isFinite(altFt)) continue;

    const category = typeof a.category === 'string' ? a.category.toUpperCase() : null;
    if (category && SURFACE.test(category)) continue; // pushback tugs, not aircraft

    // seen_pos is how many seconds ago this POSITION was received (as opposed
    // to `seen`, any message). A fix a minute old has moved 15 km at cruise.
    const seenPos = Number(a.seen_pos);
    if (Number.isFinite(seenPos) && seenPos > STALE_FIX_S) continue;

    const type = typeof a.t === 'string' ? a.t.trim().toUpperCase() : null;
    const altM = altFt * FT;
    const vrateMs = (Number(a.baro_rate ?? a.geom_rate) || 0) * FPM;
    const track = Number(a.track ?? a.true_heading ?? a.mag_heading);
    const hex = String(a.hex).trim().toLowerCase();
    const callsign = typeof a.flight === 'string' ? a.flight.trim() : '';

    out.push({
      id: `AC:${hex}`,
      hex,
      // The callsign is the airline's flight number over the air (UAL1577).
      // Registration is the tail number (N74856) — the only label a light
      // aircraft or helicopter usually has, so it stands in when there is no
      // callsign, and the client never has to invent one.
      callsign: callsign || null,
      registration: typeof a.r === 'string' ? a.r.trim() || null : null,
      type,
      kind: kindFor(category, type),
      category,
      lat,
      lon,
      altM,
      // 0 is a real track. Absent must stay absent so the client derives
      // heading from motion instead of pointing every aircraft due north.
      bearingDeg: Number.isFinite(track) ? track : null,
      groundSpeedMs: (Number(a.gs) || 0) * KT,
      verticalRateMs: vrateMs,
      phase: phaseFor(altM, vrateMs),
      squawk: typeof a.squawk === 'string' ? a.squawk : null,
      emergency: emergencyFor(a.squawk, a.emergency),
      // dbFlags bit 0 is the aggregators' military marker.
      military: Number(a.dbFlags) & 1 ? true : undefined,
      recordedAt: Number.isFinite(seenPos) ? now - Math.round(seenPos * 1000) : now,
    });
  }

  // Lowest first: the approaches over the Bay are the show, and if anything has
  // to be dropped it should be a cruiser at FL350 rather than a helicopter over
  // the Embarcadero.
  out.sort((p, q) => p.altM - q.altM);
  if (out.length > MAX_AIRCRAFT) out.length = MAX_AIRCRAFT;
  return out;
}

// Scalars survive the concierge's 6 KB tool-result clamp (which halves arrays),
// so the model's counts stay right even when the aircraft list is trimmed —
// the same reasoning as the muni feed's summary.
function summarise(aircraft) {
  const byKind = {};
  let lowest = null;
  for (const a of aircraft) {
    byKind[a.kind] = (byKind[a.kind] || 0) + 1;
    if (lowest === null || a.altM < lowest) lowest = a.altM;
  }
  return {
    total: aircraft.length,
    byKind,
    lowestAltM: lowest === null ? null : Math.round(lowest),
    radiusNm: RADIUS_NM,
    withRoute: aircraft.filter((a) => a.route).length,
  };
}

async function fetchOne(url) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), TIMEOUT_MS);
  try {
    const res = await fetch(url, { signal: controller.signal, headers: { accept: 'application/json' } });
    if (!res.ok) throw new Error(`http-${res.status}`);
    return await res.json();
  } catch (error) {
    throw error?.name === 'AbortError' ? new Error('timeout') : error;
  } finally {
    clearTimeout(timer);
  }
}

async function fetchFlights() {
  const now = Date.now();
  const failures = [];
  for (const [name, url] of SOURCES) {
    try {
      const aircraft = normalise(await fetchOne(url), now);
      // An empty list from a reachable source is not proof of empty skies over
      // a Class B airport — it means that network lost its receivers. Try the
      // next one; the registry serves last-good if they all come up empty.
      if (!aircraft.length) throw new Error('no aircraft');
      // Origin/destination, best-effort — never lets a route lookup break the
      // positions.
      try {
        await attachRoutes(aircraft);
      } catch (error) {
        console.warn(`[feed:flights] route lookup failed: ${error?.message || error}`);
      }
      if (failures.length) console.warn(`[feed:flights] ${failures.join('; ')} → served ${name}`);
      return { live: true, source: name, summary: summarise(aircraft), aircraft };
    } catch (error) {
      failures.push(`${name} ${error?.message || error}`);
    }
  }
  // Throwing is the contract: feedcore keeps last-good and backs off.
  throw new Error(failures.join('; '));
}

registerFeed('flights', {
  describe:
    'real aircraft in the sky over San Francisco right now, from community ADS-B receivers — per aircraft: callsign, tail number, ICAO type (B739, C172, EC35), airframe kind (airliner/light/heli), lat/lon, altitude in metres, ground speed, heading, climb or descent rate, flight phase, and for scheduled flights the route it is flying (origin and destination airport)',
  ttl: TTL_MS,
  staleMs: STALE_MS,
  backoffMs: BACKOFF_MS,
  fetcher: fetchFlights,
  empty: { live: false, aircraft: [] },
});
