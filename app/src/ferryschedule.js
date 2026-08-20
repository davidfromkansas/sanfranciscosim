// Timetable playback for the ferry operators that publish no live positions.
//
// WHY THIS EXISTS
//
// Golden Gate Ferry, Angel Island–Tiburon and Treasure Island register their
// TIMETABLES with 511 but broadcast no vehicle positions at all. Measured in
// both of 511's live formats, SIRI and GTFS-Realtime, each returns an empty
// feed — 15 bytes, header only — while Muni returns 626 vehicles on the same
// call. So seven of the Bay's fourteen crossings had a lane drawn on the water
// and no boat that could ever appear on it.
//
// This module places a boat where the published timetable says one should be.
// That is a SIMULATION, not a position, and it is labelled as one everywhere it
// surfaces: the card says scheduled, never live. It is the same distinction the
// app already draws for aircraft, whose altitude is compressed and whose card
// still reports the true number.
//
// Pure functions — no three.js, no DOM, no clock of its own — so the awkward
// parts are testable: which services run on a given day, and where a boat is
// partway through a leg. Covered by app/test/ferry-schedule.test.mjs.

// GTFS service days do not end at midnight. A 00:40 sailing is published as
// "24:40:00" on the PREVIOUS day's service, so the current instant has to be
// tested against yesterday's timetable too, with the clock wound past 24 h.
const DAY_S = 86400;

// Local calendar parts for an instant, in the city's own timezone. Intl is the
// only thing that gets daylight saving right without a table.
const PARTS = new Intl.DateTimeFormat('en-CA', {
  timeZone: 'America/Los_Angeles',
  year: 'numeric',
  month: '2-digit',
  day: '2-digit',
  weekday: 'short',
});

const WEEKDAY_INDEX = { Mon: 0, Tue: 1, Wed: 2, Thu: 3, Fri: 4, Sat: 5, Sun: 6 };

// -> { ymd: 20260819, weekday: 2 } where weekday 0 is Monday, matching the
// order GTFS calendar.txt lists its columns in.
export function localDay(ms) {
  const parts = Object.fromEntries(PARTS.formatToParts(new Date(ms)).map((p) => [p.type, p.value]));
  return {
    ymd: Number(`${parts.year}${parts.month}${parts.day}`),
    weekday: WEEKDAY_INDEX[parts.weekday] ?? 0,
  };
}

// Does this service run on this local day? calendar_dates exceptions win over
// the weekly pattern in both directions, which is how a holiday timetable is
// published.
export function serviceRuns(service, { ymd, weekday }) {
  if (!service) return false;
  if (service.removed?.includes(ymd)) return false;
  if (service.added?.includes(ymd)) return true;
  if (ymd < service.start || ymd > service.end) return false;
  return service.days?.[weekday] === 1;
}

export function activeServices(services, day) {
  const out = new Set();
  for (const [id, service] of Object.entries(services || {})) {
    if (serviceRuns(service, day)) out.add(id);
  }
  return out;
}

// How far along its shape a trip is at `seconds` past the service day's local
// midnight, in metres — or null if the trip is not running then.
//
// `legs` are [timeSeconds, metresAlongShape] pairs, one per stop, baked from
// the trip's own stop_times. Interpolating between consecutive pairs is what
// places a three-stop run like the Triangle correctly, rather than assuming it
// is halfway along at the halfway time.
export function metresAt(trip, seconds) {
  const legs = trip?.legs;
  if (!legs || legs.length < 2) return null;
  const start = legs[0][0];
  const end = legs[legs.length - 1][0];
  if (seconds < start || seconds > end) return null;
  for (let i = 0; i < legs.length - 1; i++) {
    const [t0, m0] = legs[i];
    const [t1, m1] = legs[i + 1];
    if (seconds > t1) continue;
    // A dwell at a berth (two stops sharing a time) leaves the boat put rather
    // than dividing by zero.
    if (t1 <= t0) return m1;
    const f = (seconds - t0) / (t1 - t0);
    return m0 + (m1 - m0) * f;
  }
  return legs[legs.length - 1][1];
}

// Every scheduled sailing under way at `ms`, as { trip, metres, seconds }.
//
// Both today's timetable and yesterday's are consulted — the latter with the
// clock wound past 24 h — because that is where a sailing after midnight lives.
export function sailingsAt(schedule, ms, localDayStart) {
  if (!schedule?.trips?.length) return [];
  const dayStart = localDayStart(ms);
  const today = localDay(ms);
  const yesterday = localDay(dayStart - 12 * 3600 * 1000);
  const secondsToday = (ms - dayStart) / 1000;

  const running = [
    { services: activeServices(schedule.services, today), seconds: secondsToday },
    { services: activeServices(schedule.services, yesterday), seconds: secondsToday + DAY_S },
  ];

  const out = [];
  for (const trip of schedule.trips) {
    for (const { services, seconds } of running) {
      if (!services.has(trip.service)) continue;
      const metres = metresAt(trip, seconds);
      if (metres == null) continue;
      out.push({ trip, metres, seconds });
      break; // a trip cannot be running on two service days at once
    }
  }
  return out;
}
