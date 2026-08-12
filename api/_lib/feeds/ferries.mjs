// /api/ferries — real San Francisco Bay Ferry (WETA) vessel positions.
//
// Thin normaliser over 511.org's SIRI VehicleMonitoring feed for agency SB, plus
// the scheduled departure of each vessel's current trip from StopTimetable.
// Without FERRY_511_KEY it answers { live: false } and the client keeps its
// procedural ferries: the city never requires a key.
//
// 511 allows 60 requests an hour. Positions cache for 90 s in the feed registry
// (40/h worst case) and the CDN caches for the same, which leaves headroom for
// the per-terminal timetables — those are fetched at most one per refresh,
// capped per hour, and cached for six hours since they are a published
// schedule. An upstream failure serves the last good fix (marked stale, via the
// registry) and backs off for five minutes.

import { registerFeed } from '../feedcore.mjs';

const UPSTREAM = 'https://api.511.org/transit/VehicleMonitoring';
const TIMETABLE = 'https://api.511.org/transit/StopTimetable';
const AGENCY = 'SB'; // SB = SF Bay Ferry / WETA (SF is Muni, GF is Golden Gate).
const TTL_MS = 90 * 1000;
const STALE_MS = 10 * 60 * 1000;
const BACKOFF_MS = 5 * 60 * 1000;
const TIMEOUT_MS = 10 * 1000;
const TIMETABLE_TTL_MS = 6 * 60 * 60 * 1000;
const TIMETABLE_BUDGET = 12; // Per instance per hour, well inside the 60/h key limit.

// Module scope survives across invocations on a warm instance.
// stopRef -> { fetchedAt, departures: Map<datedVehicleJourneyRef, epochMs> }
const timetables = new Map();
let timetableSpend = { hour: 0, count: 0 };

function asArray(value) {
  if (value == null) return [];
  return Array.isArray(value) ? value : [value];
}

function stopName(value) {
  if (value == null) return null;
  const name = String(Array.isArray(value) ? value[0] : value).trim();
  return name || null;
}

function time(value) {
  const t = Date.parse(value);
  return Number.isFinite(t) ? t : null;
}

// The trip identifier, which SIRI nests differently in VehicleMonitoring
// (FramedVehicleJourneyRef) and StopTimetable (a bare DatedVehicleJourneyRef).
function tripRef(journey) {
  const ref =
    journey?.FramedVehicleJourneyRef?.DatedVehicleJourneyRef ??
    journey?.DatedVehicleJourneyRef ??
    journey?.VehicleJourneyRef ??
    null;
  return ref == null ? null : String(ref);
}

function normalise(payload, now) {
  const deliveries = asArray(payload?.Siri?.ServiceDelivery?.VehicleMonitoringDelivery);
  const vessels = [];
  for (const delivery of deliveries) {
    for (const activity of asArray(delivery?.VehicleActivity)) {
      const journey = activity?.MonitoredVehicleJourney;
      const location = journey?.VehicleLocation;
      if (!journey || !location) continue;
      const lat = Number(location.Latitude);
      const lon = Number(location.Longitude);
      if (!Number.isFinite(lat) || !Number.isFinite(lon) || (lat === 0 && lon === 0)) continue;

      const recordedAt = Date.parse(activity.RecordedAtTime);
      if (Number.isFinite(recordedAt) && now - recordedAt > STALE_MS) continue;

      const bearing = Number(journey.Bearing);
      const ref = journey.VehicleRef == null ? null : String(journey.VehicleRef);
      if (!ref) continue;

      const call = journey.MonitoredCall || {};
      const onward = asArray(journey.OnwardCalls?.OnwardCall);
      // The stop the boat is working towards: MonitoredCall when the feed gives
      // one, else the first onward call.
      const nextCall = call.StopPointName || call.StopPointRef ? call : onward[0] || null;

      vessels.push({
        id: `${AGENCY}:${ref}`,
        label: ref,
        lat,
        lon,
        // A missing bearing must stay missing: 0 would point every docked boat north.
        bearingDeg: Number.isFinite(bearing) ? bearing : null,
        routeName: journey.PublishedLineName || journey.LineRef || null,
        destination: journey.DestinationName || null,
        inService: journey.LineRef != null,
        recordedAt: Number.isFinite(recordedAt) ? recordedAt : null,
        tripRef: tripRef(journey),
        origin: {
          ref: journey.OriginRef == null ? null : String(journey.OriginRef),
          name: stopName(journey.OriginName),
          // Filled in from the terminal's published timetable, if we have it.
          departedAt: null,
        },
        next: nextCall
          ? {
              name: stopName(nextCall.StopPointName) || stopName(nextCall.StopPointRef),
              // Expected beats aimed: it is the live prediction.
              arrivalAt: time(nextCall.ExpectedArrivalTime) || time(nextCall.AimedArrivalTime),
              scheduledArrivalAt: time(nextCall.AimedArrivalTime),
              departureAt:
                time(nextCall.ExpectedDepartureTime) || time(nextCall.AimedDepartureTime),
            }
          : null,
      });
    }
  }
  return vessels;
}

// One terminal's published departures, keyed by trip. Best-effort: any failure
// just means vessels report no scheduled departure time.
async function loadTimetable(key, stopRef, now) {
  const hour = Math.floor(now / (60 * 60 * 1000));
  if (timetableSpend.hour !== hour) timetableSpend = { hour, count: 0 };
  if (timetableSpend.count >= TIMETABLE_BUDGET) return;
  timetableSpend.count += 1;

  const url = `${TIMETABLE}?api_key=${encodeURIComponent(key)}&OperatorRef=${AGENCY}&MonitoringRef=${encodeURIComponent(stopRef)}&format=json`;
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), TIMEOUT_MS);
  try {
    const response = await fetch(url, { signal: controller.signal });
    if (!response.ok) return;
    const text = await response.text();
    const payload = JSON.parse(text.replace(/^\uFEFF/, ''));
    const visits = asArray(payload?.Siri?.ServiceDelivery?.StopTimetableDelivery).flatMap((d) =>
      asArray(d?.TimetabledStopVisit),
    );
    const departures = new Map();
    for (const visit of visits) {
      const journey = visit?.TargetedVehicleJourney;
      const ref = tripRef(journey);
      const call = asArray(journey?.TargetedCall)[0];
      const departure = time(call?.AimedDepartureTime);
      // Only a trip that starts here counts: the same trip visits later stops too.
      if (!ref || departure == null) continue;
      if (String(journey.OriginRef ?? '') !== String(stopRef)) continue;
      departures.set(ref, departure);
    }
    timetables.set(String(stopRef), { fetchedAt: now, departures });
  } catch {
    // Leave the stop uncached; the next refresh may retry within budget.
  } finally {
    clearTimeout(timer);
  }
}

function scheduledDeparture(stopRef, tripRef) {
  const entry = stopRef == null ? null : timetables.get(String(stopRef));
  if (!entry || tripRef == null) return null;
  return entry.departures.get(String(tripRef)) ?? null;
}

function staleTimetableStops(vessels, now) {
  const wanted = new Set();
  for (const vessel of vessels) {
    const stopRef = vessel.origin?.ref;
    if (stopRef == null) continue;
    const entry = timetables.get(String(stopRef));
    if (!entry || now - entry.fetchedAt > TIMETABLE_TTL_MS) wanted.add(String(stopRef));
  }
  return [...wanted];
}

async function fetchFerries() {
  const key = (process.env.FERRY_511_KEY || '').trim();
  if (!key) return { live: false, reason: 'no-key', vessels: [] };

  const now = Date.now();
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), TIMEOUT_MS);
  try {
    const url = `${UPSTREAM}?api_key=${encodeURIComponent(key)}&agency=${AGENCY}&format=json`;
    const upstream = await fetch(url, { signal: controller.signal });
    if (!upstream.ok) throw new Error(`upstream-${upstream.status}`);
    // 511 serves this feed as UTF-8 with a BOM, which JSON.parse rejects.
    const text = await upstream.text();
    const payload = JSON.parse(text.replace(/^\uFEFF/, ''));
    const vessels = normalise(payload, now);
    // One terminal per refresh: enough to warm every terminal within a couple
    // of minutes without crowding the hourly request budget.
    const missing = staleTimetableStops(vessels, now);
    if (missing.length) await loadTimetable(key, missing[0], now);
    for (const vessel of vessels) {
      vessel.origin.departedAt = scheduledDeparture(vessel.origin.ref, vessel.tripRef);
    }
    return { live: true, vessels };
  } catch (error) {
    throw error?.name === 'AbortError' ? new Error('timeout') : error;
  } finally {
    clearTimeout(timer);
  }
}

registerFeed('ferries', {
  describe:
    'real San Francisco Bay Ferry (WETA) vessel positions on the Bay right now — lat/lon, bearing, route, destination, next stop with live ETA',
  ttl: TTL_MS,
  staleMs: STALE_MS,
  backoffMs: BACKOFF_MS,
  fetcher: fetchFerries,
  empty: { live: false, vessels: [] },
});
