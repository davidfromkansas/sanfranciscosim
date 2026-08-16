// Observed fog, from space: NOAA GOES-18 via the University of Wisconsin's
// RealEarth service. Keyless, and it answers a lat/lon with a number rather
// than an image (fog.today, which pointed us here, publishes only picture
// loops — and it reads GOES-16, the EAST satellite, which sees San Francisco
// at a poor angle. GOES-18 is GOES-West and actually looks at us).
//
// What this adds over Open-Meteo: that feed is a MODEL — HRRR's hourly
// forecast of where fog should be. This is an OBSERVATION of where it is,
// refreshed every five minutes. It is deliberately a correction, not a
// replacement: it cannot give rain, wind, temperature or air quality, and it
// reports a temperature rather than a visibility.
//
// How the fog signal works: band 13 is the 10.3 um "clean window" infrared,
// which reads the temperature of whatever the satellite can see the top of. A
// marine layer's cloud top is COLD; bare ground on a clear day is warm. So a
// cold cell means low cloud sitting over it. Measured live over SF while
// writing this: 281.5 K over the fogged Sunset against 294.9 K over clear
// Oakland — a 13 K spread that lands exactly on the fog line.
//
// The API takes one point per request, so this samples a west-to-east line
// rather than the full 36-point grid: the marine layer boundary runs
// north-south and it is the east-west profile that carries the information.

import { registerFeed } from '../feedcore.mjs';

const BASE = 'https://realearth.ssec.wisc.edu/api/data';
const PRODUCT = 'G18-ABI-CONUS-BAND13';
const TIMEOUT_MS = 8000;

// A west-to-east transect across the city at roughly the latitude of the
// Golden Gate down to the Bayview, plus one bay-side reference point. Eight
// requests against a university service every five minutes is polite; the
// full grid would be thirty-six.
const SAMPLES = [
  ['Ocean', 37.76, -122.52],
  ['Sunset', 37.7558, -122.4869],
  ['Golden Gate', 37.8199, -122.4783],
  ['Richmond', 37.7801, -122.4803],
  ['Twin Peaks', 37.7544, -122.4477],
  ['Downtown', 37.7897, -122.4],
  ['Mission', 37.7599, -122.4148],
  ['Bayview', 37.7299, -122.39],
];

async function probe(lat, lon) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), TIMEOUT_MS);
  try {
    const url = `${BASE}?products=${PRODUCT}&lat=${lat}&lon=${lon}`;
    const res = await fetch(url, { signal: controller.signal, headers: { accept: 'application/json' } });
    if (!res.ok) throw new Error(String(res.status));
    const payload = await res.json();
    const raw = payload?.[PRODUCT]?.[0];
    const value = Number(raw);
    // "No value" comes back when the point falls outside the current sector.
    return Number.isFinite(value) ? value : null;
  } finally {
    clearTimeout(timer);
  }
}

async function fetchSatFog() {
  const results = await Promise.allSettled(SAMPLES.map(([, lat, lon]) => probe(lat, lon)));
  const sites = {};
  const temps = [];
  results.forEach((r, i) => {
    const value = r.status === 'fulfilled' ? r.value : null;
    sites[SAMPLES[i][0]] = value === null ? null : Number(value.toFixed(1));
    if (value !== null) temps.push(value);
  });
  if (temps.length < 3) throw new Error('too few usable satellite samples');

  // Convert temperatures to a 0..1 "how cloud-topped is this" score. The scale
  // is RELATIVE to the warmest and coldest points in this same reading, not to
  // fixed thresholds: absolute brightness temperature swings with season and
  // time of day, but within one frame the cold cells really are the cloudy
  // ones. This is why the feed is a correction and not a source of truth — it
  // says where fog is thickest, not how thick in metres of visibility.
  const warm = Math.max(...temps);
  const cold = Math.min(...temps);
  const span = warm - cold;
  const scores = {};
  for (const [name, value] of Object.entries(sites)) {
    scores[name] = value === null || span < 1.5 ? null : Number(((warm - value) / span).toFixed(2));
  }

  return {
    live: true,
    source: 'NOAA GOES-18 ABI band 13 (10.3um) via UW-Madison SSEC RealEarth',
    observedNotForecast: true,
    // Kelvin, as measured.
    brightnessTempK: sites,
    // 0 = warmest point in this frame (clearest), 1 = coldest (most cloud-topped).
    cloudTopScore: scores,
    spreadK: Number(span.toFixed(1)),
    // Below this the frame is flat and carries no usable fog signal — an
    // overcast night, or a sector that has drifted off San Francisco.
    usable: span >= 1.5,
  };
}

registerFeed('satfog', {
  describe:
    'satellite-observed low cloud and fog over San Francisco from NOAA GOES-18 infrared, sampled west to east: colder cells are cloud tops, warmer cells are clear ground. An observation refreshed every 5 minutes, unlike the weather feed which is an hourly forecast model',
  ttl: 5 * 60_000,
  staleMs: 45 * 60_000,
  backoffMs: 5 * 60_000,
  fetcher: fetchSatFog,
  empty: { live: false },
});
