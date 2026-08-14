// Live San Francisco weather, sampled as a SPATIAL FIELD rather than as one
// citywide number — the Sunset can be socked in while the Mission is clear, and
// that gradient is the whole point (docs/plans/WEATHER-PLAN.md §1).
//
// Open-Meteo answers many coordinates in one request, so a 6x6 grid over the
// city bbox costs exactly one upstream call (~17 KB). The underlying model is
// NOAA HRRR at 3 km, so 36 points resolve to ~18 distinct cells: deliberate 2x
// oversampling, which is what makes the client's bilinear interpolation smooth
// instead of blocky.
//
// Both upstreams are keyless (iron rule 4). Air quality is best-effort: it is a
// separate host and a nice-to-have, so it must never take the field down with
// it.

import { registerFeed } from '../feedcore.mjs';

const FORECAST = 'https://api.open-meteo.com/v1/forecast';
const AIR = 'https://air-quality-api.open-meteo.com/v1/air-quality';
const TIMEOUT_MS = 10_000;

// The sampling grid, in degrees. Covers the city plus a margin at the Gate.
export const GRID = { lat0: 37.705, lat1: 37.835, lon0: -122.525, lon1: -122.355, w: 6, h: 6 };

// Row-major, north row first — the same order the client uploads to the texture.
function gridPoints() {
  const lats = [];
  const lons = [];
  for (let row = 0; row < GRID.h; row++) {
    // row 0 = north = lat1.
    const lat = GRID.lat1 - ((GRID.lat1 - GRID.lat0) * row) / (GRID.h - 1);
    for (let col = 0; col < GRID.w; col++) {
      const lon = GRID.lon0 + ((GRID.lon1 - GRID.lon0) * col) / (GRID.w - 1);
      lats.push(lat.toFixed(4));
      lons.push(lon.toFixed(4));
    }
  }
  return { lats, lons };
}

const CURRENT = [
  'temperature_2m',
  'relative_humidity_2m',
  'apparent_temperature',
  'precipitation',
  'rain',
  'weather_code',
  'cloud_cover',
  'cloud_cover_low',
  'cloud_cover_mid',
  'cloud_cover_high',
  'visibility',
  'wind_speed_10m',
  'wind_direction_10m',
  'wind_gusts_10m',
].join(',');

// WMO code -> the short toy label the clock, the concierge and the storm
// trigger all read. One table, no second copy anywhere.
const WMO = [
  [0, 'Clear', 'clear'],
  [1, 'Mostly clear', 'clear'],
  [2, 'Partly cloudy', 'partly'],
  [3, 'Overcast', 'cloudy'],
  [45, 'Fog', 'fog'],
  [48, 'Freezing fog', 'fog'],
  [51, 'Light drizzle', 'drizzle'],
  [53, 'Drizzle', 'drizzle'],
  [55, 'Heavy drizzle', 'drizzle'],
  [56, 'Freezing drizzle', 'drizzle'],
  [57, 'Freezing drizzle', 'drizzle'],
  [61, 'Light rain', 'rain'],
  [63, 'Rain', 'rain'],
  [65, 'Heavy rain', 'heavy'],
  [66, 'Freezing rain', 'rain'],
  [67, 'Freezing rain', 'heavy'],
  [71, 'Light snow', 'snow'],
  [73, 'Snow', 'snow'],
  [75, 'Heavy snow', 'snow'],
  [77, 'Snow grains', 'snow'],
  [80, 'Showers', 'rain'],
  [81, 'Showers', 'rain'],
  [82, 'Heavy showers', 'heavy'],
  [85, 'Snow showers', 'snow'],
  [86, 'Snow showers', 'snow'],
  [95, 'Thunderstorm', 'storm'],
  [96, 'Thunderstorm', 'storm'],
  [99, 'Thunderstorm', 'storm'],
];

export function describeCode(code) {
  const hit = WMO.find(([c]) => c === code);
  return hit ? { code, label: hit[1], kind: hit[2] } : { code, label: 'Fair', kind: 'partly' };
}

const clamp = (v, lo, hi) => (v < lo ? lo : v > hi ? hi : v);

function median(list) {
  const sorted = list.filter((v) => Number.isFinite(v)).sort((a, b) => a - b);
  if (!sorted.length) return null;
  return sorted[sorted.length >> 1];
}

// Nulls become the field median, never 0: to a shader 0 means "perfectly
// clear", which would read as a bug rather than as missing data.
function fill(values, lo, hi) {
  const mid = median(values);
  const fallback = mid === null ? lo : mid;
  return values.map((v) => (Number.isFinite(v) ? clamp(v, lo, hi) : fallback));
}

// A single coastal cell came back at 0.2 km against 12 km neighbours in
// testing. One bad cell must never punch a hole of fog into a clear city, so
// anything more than 4x from its 4-neighbourhood median is replaced by it.
function despike(values, w, h) {
  const out = values.slice();
  for (let row = 0; row < h; row++) {
    for (let col = 0; col < w; col++) {
      const i = row * w + col;
      const neighbours = [];
      if (row > 0) neighbours.push(values[i - w]);
      if (row < h - 1) neighbours.push(values[i + w]);
      if (col > 0) neighbours.push(values[i - 1]);
      if (col < w - 1) neighbours.push(values[i + 1]);
      const mid = median(neighbours);
      if (mid === null || mid === 0) continue;
      const ratio = values[i] / mid;
      if (ratio > 4 || ratio < 0.25) out[i] = mid;
    }
  }
  return out;
}

const mean = (list) => list.reduce((a, b) => a + b, 0) / (list.length || 1);

// The concierge cannot read a 36-cell grid, but "is it foggy in the Sunset?" is
// exactly the question this feed exists to answer — so the payload carries a
// named digest alongside the raw field. Bilinear, matching what the GPU does.
const DISTRICTS = [
  ['Sunset', 37.7558, -122.4869],
  ['Richmond', 37.7801, -122.4803],
  ['Presidio', 37.7989, -122.4662],
  ['Golden Gate Bridge', 37.8199, -122.4783],
  ['Downtown', 37.7897, -122.4],
  ['Mission', 37.7599, -122.4148],
  ['Twin Peaks', 37.7544, -122.4477],
  ['Bayview', 37.7299, -122.39],
];

function sample(values, lat, lon) {
  const u = clamp((lon - GRID.lon0) / (GRID.lon1 - GRID.lon0), 0, 1) * (GRID.w - 1);
  // Row 0 is the north row, so v runs southwards from lat1.
  const v = clamp((GRID.lat1 - lat) / (GRID.lat1 - GRID.lat0), 0, 1) * (GRID.h - 1);
  const c0 = Math.floor(u);
  const r0 = Math.floor(v);
  const c1 = Math.min(GRID.w - 1, c0 + 1);
  const r1 = Math.min(GRID.h - 1, r0 + 1);
  const fu = u - c0;
  const fv = v - r0;
  const top = values[r0 * GRID.w + c0] * (1 - fu) + values[r0 * GRID.w + c1] * fu;
  const bottom = values[r1 * GRID.w + c0] * (1 - fu) + values[r1 * GRID.w + c1] * fu;
  return top * (1 - fv) + bottom * fv;
}

// The word a person would actually use, from visibility AND low cloud together.
// Visibility alone was calling a 95%-low-cloud cell "clear" at 12 km while the
// citywide code said Fog -- the concierge would contradict itself inside one
// answer. In San Francisco a socked-in marine layer routinely reports double
// digit kilometres at the sensor while being unmistakably fog to anyone in it.
function fogWord(visibilityM, lowCloud) {
  if (visibilityM < 2000) return 'thick fog';
  if (visibilityM < 6000) return 'fog';
  if (lowCloud >= 90) return visibilityM < 13000 ? 'fog' : 'low cloud';
  if (lowCloud >= 70) return 'misty';
  if (visibilityM < 12000) return 'hazy';
  return 'clear';
}

function digest(fields) {
  const out = {};
  for (const [name, lat, lon] of DISTRICTS) {
    const visibility = sample(fields.visibility, lat, lon);
    const cloud = Math.round(sample(fields.cloudLow, lat, lon));
    out[name] = {
      temp: Number(sample(fields.temp, lat, lon).toFixed(1)),
      cloud,
      visibilityKm: Number((visibility / 1000).toFixed(1)),
      conditions: fogWord(visibility, cloud),
    };
  }
  return out;
}

async function getJSON(url) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), TIMEOUT_MS);
  try {
    const res = await fetch(url, { signal: controller.signal, headers: { accept: 'application/json' } });
    if (!res.ok) throw new Error(`${res.status}`);
    return await res.json();
  } finally {
    clearTimeout(timer);
  }
}

async function fetchAir() {
  const url = `${AIR}?latitude=37.7897&longitude=-122.4000&current=us_aqi,pm2_5`;
  const payload = await getJSON(url);
  const current = payload?.current || {};
  const aqi = Number(current.us_aqi);
  return {
    aqi: Number.isFinite(aqi) ? clamp(Math.round(aqi), 0, 1000) : null,
    pm25: Number.isFinite(Number(current.pm2_5)) ? Number(current.pm2_5) : null,
  };
}

async function fetchField() {
  const { lats, lons } = gridPoints();
  const url =
    `${FORECAST}?latitude=${lats.join(',')}&longitude=${lons.join(',')}` +
    `&current=${CURRENT}&models=gfs_hrrr&temperature_unit=fahrenheit&wind_speed_unit=mph`;
  const payload = await getJSON(url);
  // One coordinate returns an object, many return an array. We always send many.
  const points = Array.isArray(payload) ? payload : [payload];
  if (points.length !== GRID.w * GRID.h) throw new Error(`expected ${GRID.w * GRID.h} cells, got ${points.length}`);
  return points;
}

async function fetchWeather() {
  // The field is the feature; air quality is a garnish. allSettled so a failure
  // of the garnish cannot throw away the meal.
  const [field, air] = await Promise.allSettled([fetchField(), fetchAir()]);
  if (field.status === 'rejected') throw field.reason;
  const points = field.value;
  const at = (key) => points.map((p) => Number(p?.current?.[key]));

  const cloudLow = despike(fill(at('cloud_cover_low'), 0, 100), GRID.w, GRID.h);
  const cloudMid = fill(at('cloud_cover_mid'), 0, 100);
  const cloudHigh = fill(at('cloud_cover_high'), 0, 100);
  const cloud = fill(at('cloud_cover'), 0, 100);
  const visibility = despike(fill(at('visibility'), 50, 50_000), GRID.w, GRID.h);
  const precip = fill(at('precipitation'), 0, 200);
  const temp = fill(at('temperature_2m'), -20, 130);
  const humidity = fill(at('relative_humidity_2m'), 0, 100);
  const windSpeed = fill(at('wind_speed_10m'), 0, 100);
  const windDir = fill(at('wind_direction_10m'), 0, 360);

  // The citywide scalars the UI and the concierge read. Downtown is the
  // reference point for "the weather in San Francisco"; the field carries the
  // nuance for anyone who asks about a district.
  const codes = at('weather_code');
  const worst = codes.filter(Number.isFinite).sort((a, b) => b - a)[0];
  const air2 = air.status === 'fulfilled' ? air.value : { aqi: null, pm25: null };

  const round = (v, p = 0) => Number(v.toFixed(p));
  // Order matters: the concierge's live_data tool clamps a feed to a character
  // budget and truncates the tail, so the parts a language model can actually
  // use — the citywide summary and the named districts — go first, and the raw
  // field (which only the shaders read) goes last.
  return {
    live: true,
    summary: {
      ...describeCode(worst),
      temp: round(mean(temp), 1),
      humidity: round(mean(humidity)),
      windSpeed: round(mean(windSpeed), 1),
      windDir: round(mean(windDir)),
      visibility: round(mean(visibility)),
      precip: round(mean(precip), 2),
      cloud: round(mean(cloud)),
      aqi: air2.aqi,
      pm25: air2.pm25,
    },
    districts: digest({ visibility, temp, cloudLow }),
    grid: GRID,
    cloudLow: cloudLow.map((v) => round(v)),
    cloudMid: cloudMid.map((v) => round(v)),
    cloudHigh: cloudHigh.map((v) => round(v)),
    cloud: cloud.map((v) => round(v)),
    visibility: visibility.map((v) => round(v)),
    precip: precip.map((v) => round(v, 2)),
    temp: temp.map((v) => round(v, 1)),
    humidity: humidity.map((v) => round(v)),
    windSpeed: windSpeed.map((v) => round(v, 1)),
    windDir: windDir.map((v) => round(v)),
  };
}

registerFeed('weather', {
  describe:
    'current San Francisco weather sampled across the city on a 6x6 grid — cloud cover, visibility (fog), rain, wind, temperature, humidity and air quality, so per-neighbourhood questions like "is it foggy in the Sunset?" can be answered',
  // HRRR updates hourly; 5 minutes is generous, cheap and kind to a free API.
  ttl: 5 * 60_000,
  // An hour-old field still beats no field at all.
  staleMs: 60 * 60_000,
  backoffMs: 2 * 60_000,
  fetcher: fetchWeather,
  empty: { live: false },
});
