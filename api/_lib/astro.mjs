// Sun and moon for San Francisco, computed locally. Zero dependencies, no
// network, no `three` import: the Vercel function and the browser bundle both
// load this exact file, so the concierge and the scene can never disagree.
//
// Angles are RADIANS everywhere except `skySnapshot`, which reports degrees for
// the LLM. Times are ms since epoch. Accuracy is the standard low-precision
// ephemeris: well under a degree for the sun, about a degree for the moon,
// which is far more than lighting or a clock chip needs.

export const SF = { lat: 37.77, lon: -122.4375 };
export const TZ = 'America/Los_Angeles';

const RAD = Math.PI / 180;
const DEG = 180 / Math.PI;
const DAY_MS = 86400000;
const J1970 = 2440588;
const J2000 = 2451545;
const OBLIQUITY = 23.4397 * RAD;
// Sunrise/sunset are quoted for the upper limb with refraction, not for a
// geometric zero crossing; the moon's own semidiameter is much smaller.
const SUN_HORIZON = -0.833 * RAD;
const MOON_HORIZON = 0.125 * RAD;

const PHI = SF.lat * RAD;
const LW = -SF.lon * RAD; // west-positive longitude, as the hour-angle math wants

const toDays = (ms) => ms / DAY_MS - 0.5 + J1970 - J2000;

const rightAscension = (l, b) => Math.atan2(Math.sin(l) * Math.cos(OBLIQUITY) - Math.tan(b) * Math.sin(OBLIQUITY), Math.cos(l));
const declination = (l, b) => Math.asin(Math.sin(b) * Math.cos(OBLIQUITY) + Math.cos(b) * Math.sin(OBLIQUITY) * Math.sin(l));
const siderealTime = (d, lw) => RAD * (280.16 + 360.9856235 * d) - lw;

// Horizontal coordinates from the hour angle. Azimuth is returned measured from
// TRUE NORTH, clockwise (east = 90 deg) — the convention the scene converts.
function altitude(H, dec) {
  return Math.asin(Math.sin(PHI) * Math.sin(dec) + Math.cos(PHI) * Math.cos(dec) * Math.cos(H));
}
function azimuthFromNorth(H, dec) {
  const south = Math.atan2(Math.sin(H), Math.cos(H) * Math.sin(PHI) - Math.tan(dec) * Math.cos(PHI));
  const north = south + Math.PI;
  return north < 0 ? north + 2 * Math.PI : north % (2 * Math.PI);
}

// ------------------------------------------------------------------- the sun

function solarMeanAnomaly(d) {
  return RAD * (357.5291 + 0.98560028 * d);
}

function eclipticLongitude(M) {
  const center = RAD * (1.9148 * Math.sin(M) + 0.02 * Math.sin(2 * M) + 0.0003 * Math.sin(3 * M));
  const perihelion = RAD * 102.9372;
  return M + center + perihelion + Math.PI;
}

function sunEquatorial(d) {
  const M = solarMeanAnomaly(d);
  const L = eclipticLongitude(M);
  return { ra: rightAscension(L, 0), dec: declination(L, 0) };
}

export function sunPosition(ms) {
  const d = toDays(ms);
  const { ra, dec } = sunEquatorial(d);
  const H = siderealTime(d, LW) - ra;
  return { elevation: altitude(H, dec), azimuth: azimuthFromNorth(H, dec) };
}

// ------------------------------------------------------------------ the moon

// The Astronomical Almanac's low-precision moon: linear polynomials in the
// centuries since J2000 for the mean longitude, anomaly, argument of latitude
// and the main perturbations (equation of the centre, evection, variation,
// annual equation). Good to roughly a third of a degree, which is a tenth of
// the moon's own apparent size.
const EARTH_RADIUS_KM = 6378.14;

function moonEcliptic(d) {
  const T = d / 36525;
  const A1 = RAD * (134.9 + 477198.85 * T); // mean anomaly
  const A2 = RAD * (259.2 - 413335.38 * T); // ascending node
  const A3 = RAD * (235.7 + 890534.23 * T); // twice the elongation less anomaly
  const A4 = RAD * (269.9 + 954397.7 * T); // variation
  const A5 = RAD * (357.5 + 35999.05 * T); // solar anomaly (annual equation)
  const A6 = RAD * (186.6 + 966404.05 * T);
  const B1 = RAD * (93.3 + 483202.03 * T); // argument of latitude
  const B2 = RAD * (228.2 + 960400.87 * T);
  const B3 = RAD * (318.3 + 6003.18 * T);
  const B4 = RAD * (217.6 - 407332.2 * T);

  const lon =
    RAD *
    (218.32 +
      481267.881 * T +
      6.29 * Math.sin(A1) -
      1.27 * Math.sin(A2) +
      0.66 * Math.sin(A3) +
      0.21 * Math.sin(A4) -
      0.19 * Math.sin(A5) -
      0.11 * Math.sin(A6));
  const lat =
    RAD * (5.13 * Math.sin(B1) + 0.28 * Math.sin(B2) - 0.28 * Math.sin(B3) - 0.17 * Math.sin(B4));
  const parallax =
    RAD * (0.9508 + 0.0518 * Math.cos(A1) + 0.0095 * Math.cos(A2) + 0.0078 * Math.cos(A3) + 0.0028 * Math.cos(A4));
  const dist = EARTH_RADIUS_KM / Math.sin(parallax); // km, geocentric
  return { lon, lat, dist, parallax };
}

function moonEquatorial(d) {
  const { lon, lat, dist, parallax } = moonEcliptic(d);
  return { ra: rightAscension(lon, lat), dec: declination(lon, lat), dist, parallax };
}

// Sun-moon elongation gives both the lit fraction and which limb is lit.
function moonIllumination(d) {
  const s = sunEquatorial(d);
  const m = moonEquatorial(d);
  const sdist = 149598000; // km, mean earth-sun distance
  const elongation = Math.acos(
    Math.sin(s.dec) * Math.sin(m.dec) + Math.cos(s.dec) * Math.cos(m.dec) * Math.cos(s.ra - m.ra)
  );
  const inc = Math.atan2(sdist * Math.sin(elongation), m.dist - sdist * Math.cos(elongation));
  const limb = Math.atan2(
    Math.cos(s.dec) * Math.sin(s.ra - m.ra),
    Math.sin(s.dec) * Math.cos(m.dec) - Math.cos(s.dec) * Math.sin(m.dec) * Math.cos(s.ra - m.ra)
  );
  return {
    illumination: (1 + Math.cos(inc)) / 2,
    phase: 0.5 + (0.5 * inc * (limb < 0 ? -1 : 1)) / Math.PI,
    limbAngle: limb,
  };
}

export function moonPosition(ms) {
  const d = toDays(ms);
  const m = moonEquatorial(d);
  const H = siderealTime(d, LW) - m.ra;
  const { illumination, phase, limbAngle } = moonIllumination(d);
  // The moon is close enough that an observer on the surface sees it up to a
  // degree lower than a geocentric observer would; every published almanac
  // altitude is topocentric, so correct for it.
  const geocentric = altitude(H, m.dec);
  return {
    elevation: geocentric - m.parallax * Math.cos(geocentric),
    azimuth: azimuthFromNorth(H, m.dec),
    distance: m.dist,
    phase,
    illumination,
    limbAngle,
  };
}

// ------------------------------------------------------- rise and set times
// Coarse 5-minute scan for zero crossings, then bisection. Called a handful of
// times per session, so simple beats clever.

function crossings(startMs, endMs, horizon, positionAt) {
  const step = 5 * 60 * 1000;
  const out = [];
  let prevMs = startMs;
  let prev = positionAt(startMs).elevation - horizon;
  for (let t = startMs + step; t <= endMs; t += step) {
    const cur = positionAt(t).elevation - horizon;
    if (prev <= 0 !== cur <= 0) {
      let lo = prevMs;
      let hi = t;
      let loValue = prev;
      for (let i = 0; i < 24; i++) {
        const mid = (lo + hi) / 2;
        const midValue = positionAt(mid).elevation - horizon;
        if (loValue <= 0 !== midValue <= 0) hi = mid;
        else {
          lo = mid;
          loValue = midValue;
        }
      }
      out.push({ ms: Math.round((lo + hi) / 2), rising: prev <= 0 });
    }
    prev = cur;
    prevMs = t;
  }
  return out;
}

// The local SF midnight that starts the calendar day containing `ms`. Derived
// from Intl parts only — never from a hardcoded UTC offset, which breaks on DST.
export function localDayStart(ms) {
  const parts = partsOf(ms);
  const utcGuess = Date.UTC(parts.year, parts.month - 1, parts.day);
  // Two passes converge because the offset changes by at most an hour.
  let guess = utcGuess + offsetMs(utcGuess);
  guess = utcGuess + offsetMs(guess);
  return guess;
}

const PART_FORMAT = new Intl.DateTimeFormat('en-US', {
  timeZone: TZ,
  year: 'numeric',
  month: '2-digit',
  day: '2-digit',
  hour: '2-digit',
  minute: '2-digit',
  second: '2-digit',
  hour12: false,
});

function partsOf(ms) {
  const out = {};
  for (const part of PART_FORMAT.formatToParts(new Date(ms))) {
    if (part.type !== 'literal') out[part.type] = Number(part.value);
  }
  // 'en-US' hour12:false can report hour 24 for midnight.
  if (out.hour === 24) out.hour = 0;
  return out;
}

// How far SF local time is ahead of UTC at this instant (negative all year).
function offsetMs(ms) {
  const p = partsOf(ms);
  const asUTC = Date.UTC(p.year, p.month - 1, p.day, p.hour, p.minute, p.second);
  return ms - asUTC;
}

// Rise and set only change once a day, and the scans below are the only part
// of this module that is not trivially cheap; the app calls skySnapshot every
// second, so remember the last day's answers.
const dayCache = new Map();

function perDay(key, ms, compute) {
  const start = localDayStart(ms);
  const id = `${key}:${start}`;
  const hit = dayCache.get(id);
  if (hit) return hit;
  const value = compute(start);
  if (dayCache.size > 8) dayCache.clear();
  dayCache.set(id, value);
  return value;
}

export function sunTimes(ms) {
  return perDay('sun', ms, computeSunTimes);
}

export function moonTimes(ms) {
  return perDay('moon', ms, computeMoonTimes);
}

function computeSunTimes(start) {
  const end = start + DAY_MS + 2 * 3600 * 1000; // cover a DST-short/long day
  const events = crossings(start, end, SUN_HORIZON, sunPosition);

  const rise = events.find((e) => e.rising);
  const set = events.find((e) => !e.rising);
  // Solar noon: the highest elevation of the day, to the minute.
  let solarNoon = null;
  let best = -Infinity;
  for (let t = start; t < start + DAY_MS; t += 60 * 1000) {
    const el = sunPosition(t).elevation;
    if (el > best) {
      best = el;
      solarNoon = t;
    }
  }
  return { sunrise: rise ? rise.ms : null, sunset: set ? set.ms : null, solarNoon };
}

function computeMoonTimes(start) {
  const end = start + DAY_MS + 2 * 3600 * 1000;
  const events = crossings(start, end, MOON_HORIZON, moonPosition);
  const rise = events.find((e) => e.rising);
  const set = events.find((e) => !e.rising);
  return { moonrise: rise ? rise.ms : null, moonset: set ? set.ms : null };
}

// --------------------------------------------------------------- formatting

const PHASE_NAMES = [
  'new moon',
  'waxing crescent',
  'first quarter',
  'waxing gibbous',
  'full moon',
  'waning gibbous',
  'last quarter',
  'waning crescent',
];

// The four named instants (new, quarters, full) only own a narrow band — about
// half a day each side — so a 37 %-lit moon reads "waxing crescent" the way an
// almanac writes it, not "first quarter".
const NAMED_BAND = 0.02; // of a 29.53-day cycle

export function phaseName(phase) {
  const p = ((phase % 1) + 1) % 1;
  const quarter = Math.round(p * 4) % 4; // nearest canonical point, 0..3
  if (Math.abs(p - quarter / 4) < NAMED_BAND || Math.abs(p - 1) < NAMED_BAND) return PHASE_NAMES[quarter * 2];
  return PHASE_NAMES[Math.floor(p * 4) * 2 + 1];
}

const TIME_FORMAT = new Intl.DateTimeFormat('en-US', {
  timeZone: TZ,
  hour: 'numeric',
  minute: '2-digit',
});
const DATE_FORMAT = new Intl.DateTimeFormat('en-US', {
  timeZone: TZ,
  weekday: 'short',
  month: 'short',
  day: 'numeric',
  year: 'numeric',
});

export const formatTime = (ms) => (ms == null ? null : TIME_FORMAT.format(new Date(ms)));
export const formatDate = (ms) => (ms == null ? null : DATE_FORMAT.format(new Date(ms)));

const round = (value, digits = 2) => (value == null ? null : Number(value.toFixed(digits)));

// The concierge payload: everything above in degrees and local strings.
export function skySnapshot(ms = Date.now()) {
  const sun = sunPosition(ms);
  const moon = moonPosition(ms);
  const st = sunTimes(ms);
  const mt = moonTimes(ms);
  return {
    timezone: TZ,
    localTime: formatTime(ms),
    localDate: formatDate(ms),
    epochMs: ms,
    isDay: sun.elevation > SUN_HORIZON,
    sun: {
      elevationDeg: round(sun.elevation * DEG),
      azimuthDeg: round(sun.azimuth * DEG),
      sunrise: formatTime(st.sunrise),
      sunset: formatTime(st.sunset),
      solarNoon: formatTime(st.solarNoon),
    },
    moon: {
      elevationDeg: round(moon.elevation * DEG),
      azimuthDeg: round(moon.azimuth * DEG),
      phase: round(moon.phase, 3),
      illumination: round(moon.illumination, 3),
      phaseName: phaseName(moon.phase),
      moonrise: formatTime(mt.moonrise),
      moonset: formatTime(mt.moonset),
      isUp: moon.elevation > MOON_HORIZON,
    },
    // Kept flat as well: the clock UI and the model both read these a lot.
    phaseName: phaseName(moon.phase),
    illumination: round(moon.illumination, 3),
    sunriseMs: st.sunrise,
    sunsetMs: st.sunset,
    moonriseMs: mt.moonrise,
    moonsetMs: mt.moonset,
  };
}

// Self-check (not shipped as a test framework — run it by hand):
//   node -e "import('./api/_lib/astro.mjs').then(m=>console.log(m.skySnapshot(Date.now())))"
// Compare sunrise/sunset (±2 min), sun azimuth/elevation (±1°) and the moon
// phase name against timeanddate.com/astronomy/usa/san-francisco.
