// /api/muni — real SFMTA (Muni) vehicle positions with per-stop predictions.
//
// Two 511.org GTFS-Realtime feeds for agency SF, decoded server-side with
// gtfs-realtime-bindings (the api layer's one dependency, owner-approved
// 2026-08-12) and joined on trip_id — the browser only ever sees the compact
// JSON below. Spec: MUNI-LIVE-PROMPT.md.
//
//   vehiclepositions   every refresh (ttl 90 s)   ~60 KB protobuf
//   tripupdates        lazily, ttl 5 min          ~1 MB protobuf
//
// Key budget (511 allows 60 req/h per key): on MUNI_511_KEY that is 40/h of
// positions + 12/h of predictions = 52/h, the same shape the ferry feed uses
// on its own key. Without MUNI_511_KEY the fetcher falls back to FERRY_511_KEY
// in a degraded mode — positions only, ttl 8 min (~8/h), fitting beside the
// ferry feed's ~52/h — so previews work with a single key. With neither key it
// answers { live: false } and the city keeps its procedural traffic (rule 4).
//
// Every vehicle ships with its `mode` (bus / trolley / lrv / streetcar /
// cable) resolved from route_id server-side, so no client ever needs a route
// table. Stop *names* deliberately do not ship: the client resolves stopIds
// against the baked GTFS static (tiles/muni-shapes.bin) — repeating names per
// vehicle per poll is pure payload bloat.

import GtfsRT from 'gtfs-realtime-bindings';

import { registerFeed } from '../feedcore.mjs';

const BASE = 'https://api.511.org/transit';
const AGENCY = 'SF';
const TIMEOUT_MS = 10 * 1000;
const STALE_FIX_MS = 10 * 60 * 1000;

const TTL_MS = 90 * 1000; // positions, own key
const TTL_SHARED_MS = 8 * 60 * 1000; // positions, borrowed ferry key
const TRIPUPDATES_TTL_MS = 5 * 60 * 1000;
const STALE_MS = 10 * 60 * 1000;
const BACKOFF_MS = 5 * 60 * 1000;
const ONWARD_STOPS = 3;

// Muni route ids to fleet mode. Rail and cable are fixed sets; trolleybus
// routes are the electrified lines (docs/asset-plans/transit/README.md "Why
// five"), including their R rapid variants which run the same wire. Everything
// else numbered is a motor coach. Express (AX/BX) and owl variants of trolley
// lines are DIESEL-operated, so only the bare number and R variant map to
// trolley.
const LRV = new Set(['J', 'K', 'L', 'M', 'N', 'T']);
const STREETCAR = new Set(['F', 'E']);
// Verified against the live feed 2026-08-12: cable route_ids are PM, PH, CA.
const CABLE = new Set(['PM', 'PH', 'CA', '59', '60', '61']);
const TROLLEY_NUMBERS = new Set([
  '1', '2', '3', '5', '6', '7', '14', '21', '22', '24', '30', '31', '33', '41', '45', '49',
]);

function modeFor(routeId) {
  if (!routeId) return 'bus';
  const id = String(routeId).toUpperCase();
  if (LRV.has(id)) return 'lrv';
  if (STREETCAR.has(id)) return 'streetcar';
  if (CABLE.has(id)) return 'cable';
  if (TROLLEY_NUMBERS.has(id)) return 'trolley';
  const rapid = id.match(/^([0-9]+)R$/);
  if (rapid && TROLLEY_NUMBERS.has(rapid[1])) return 'trolley';
  return 'bus';
}

// GTFS-RT OccupancyStatus enum, the readable subset the card shows.
const OCCUPANCY = [
  'empty',
  'manySeatsAvailable',
  'fewSeatsAvailable',
  'standingRoomOnly',
  'crushedStandingRoomOnly',
  'full',
  'notAcceptingPassengers',
];

// Module scope survives across invocations on a warm instance.
// tripId -> [{ stopId, arrivalAt }] from the last tripupdates decode.
let predictions = new Map();
let predictionsFetchedAt = 0;

function keyMode() {
  const own = (process.env.MUNI_511_KEY || '').trim();
  if (own) return { key: own, shared: false };
  const ferry = (process.env.FERRY_511_KEY || '').trim();
  if (ferry) return { key: ferry, shared: true };
  return { key: null, shared: false };
}

let warnedShared = false;

async function decodeFeed(key, endpoint) {
  const url = `${BASE}/${endpoint}?api_key=${encodeURIComponent(key)}&agency=${AGENCY}`;
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), TIMEOUT_MS);
  try {
    const res = await fetch(url, { signal: controller.signal });
    if (!res.ok) throw new Error(`${endpoint}-${res.status}`);
    const buf = new Uint8Array(await res.arrayBuffer());
    return GtfsRT.transit_realtime.FeedMessage.decode(buf);
  } catch (error) {
    throw error?.name === 'AbortError' ? new Error(`${endpoint}-timeout`) : error;
  } finally {
    clearTimeout(timer);
  }
}

// Epoch millis from a GTFS-RT int64 seconds field (Long or number).
function epochMs(value) {
  const s = value == null ? 0 : Number(value);
  return s > 0 ? s * 1000 : null;
}

function refreshPredictions(message) {
  const next = new Map();
  for (const entity of message.entity || []) {
    const tu = entity.tripUpdate;
    const tripId = tu?.trip?.tripId;
    if (!tripId) continue;
    const stops = [];
    for (const stu of tu.stopTimeUpdate || []) {
      const at = epochMs(stu.arrival?.time) ?? epochMs(stu.departure?.time);
      if (!stu.stopId || at == null) continue;
      stops.push({ stopId: String(stu.stopId), arrivalAt: at });
    }
    if (stops.length) next.set(String(tripId), stops);
  }
  predictions = next;
  predictionsFetchedAt = Date.now();
}

// The next ONWARD_STOPS stops still ahead of now for a trip, or [].
function upcoming(tripId, now) {
  const stops = tripId == null ? null : predictions.get(String(tripId));
  if (!stops) return [];
  const ahead = [];
  for (const stop of stops) {
    if (stop.arrivalAt < now - 30 * 1000) continue;
    ahead.push(stop);
    if (ahead.length === ONWARD_STOPS) break;
  }
  return ahead;
}

function normalise(message, now, sharedKey) {
  const vehicles = [];
  for (const entity of message.entity || []) {
    const v = entity.vehicle;
    const pos = v?.position;
    if (!v || !pos) continue;
    const lat = Number(pos.latitude);
    const lon = Number(pos.longitude);
    if (!Number.isFinite(lat) || !Number.isFinite(lon) || (lat === 0 && lon === 0)) continue;

    // Deadheading / not-in-service vehicles carry no trip; skip them — they are
    // not on a route and the scene has nothing truthful to do with them.
    const trip = v.trip;
    if (!trip?.routeId || !trip?.tripId) continue;

    const recordedAt = epochMs(v.timestamp);
    if (recordedAt != null && now - recordedAt > STALE_FIX_MS) continue;

    const fleetNumber = v.vehicle?.id != null ? String(v.vehicle.id) : null;
    if (!fleetNumber) continue;

    const bearing = Number(pos.bearing);
    const speed = Number(pos.speed);
    const occupancy =
      v.occupancyStatus != null && OCCUPANCY[v.occupancyStatus] ? OCCUPANCY[v.occupancyStatus] : null;

    vehicles.push({
      id: `${AGENCY}:${fleetNumber}`,
      fleetNumber,
      mode: modeFor(trip.routeId),
      route: String(trip.routeId),
      directionId: trip.directionId != null ? Number(trip.directionId) : null,
      tripId: String(trip.tripId),
      lat,
      lon,
      // 0 is a real heading in GTFS-RT (unlike SIRI's 0-means-unknown), but an
      // absent field decodes as 0 too; the client derives from motion either way.
      bearingDeg: Number.isFinite(bearing) ? bearing : null,
      speedMs: Number.isFinite(speed) ? speed : null,
      occupancy,
      recordedAt,
      stops: sharedKey ? [] : upcoming(trip.tripId, now),
    });
  }
  return vehicles;
}

async function fetchMuni() {
  const { key, shared } = keyMode();
  if (!key) return { live: false, reason: 'no-key', vehicles: [] };
  if (shared && !warnedShared) {
    warnedShared = true;
    console.warn('[feed:muni] MUNI_511_KEY unset — degraded mode on FERRY_511_KEY (positions only, slow poll)');
  }

  const now = Date.now();
  // Predictions on their own longer ttl, and never on the borrowed ferry key —
  // best-effort exactly like the ferry timetables: a failure only nulls ETAs.
  if (!shared && now - predictionsFetchedAt > TRIPUPDATES_TTL_MS) {
    try {
      refreshPredictions(await decodeFeed(key, 'tripupdates'));
    } catch (error) {
      console.warn(`[feed:muni] tripupdates refresh failed: ${error?.message || error}`);
    }
  }

  const message = await decodeFeed(key, 'vehiclepositions');
  return { live: true, degraded: shared || undefined, vehicles: normalise(message, now, shared) };
}

registerFeed('muni', {
  describe:
    'real Muni (SFMTA) vehicle positions right now — per vehicle: route, mode (bus/trolley/lrv/streetcar/cable), lat/lon, bearing, speed, occupancy, fleet number, and the next stops with live ETAs',
  ttl: keyMode().shared ? TTL_SHARED_MS : TTL_MS,
  staleMs: STALE_MS,
  backoffMs: BACKOFF_MS,
  fetcher: fetchMuni,
  empty: { live: false, vehicles: [] },
});
