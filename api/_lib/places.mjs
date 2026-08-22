// Optional Google Places (New) access. This module deliberately has no
// dependencies: the key stays server-side and the keyless path is a normal
// graceful result rather than an exception.

const AUTOCOMPLETE_URL = 'https://places.googleapis.com/v1/places:autocomplete';
const SEARCH_URL = 'https://places.googleapis.com/v1/places:searchText';
const AUTOCOMPLETE_FIELDS = 'suggestions.placePrediction.{place,text,structuredFormat}';
const SEARCH_FIELDS =
  'places.displayName,places.formattedAddress,places.location,places.types,places.businessStatus';

// The rectangle is intentionally the city and immediate shoreline, not the
// Bay Area. Both endpoints use this same hard geographic fence.
export const SF_RECTANGLE = {
  low: { latitude: 37.70, longitude: -122.525 },
  high: { latitude: 37.84, longitude: -122.35 },
};

const DAILY_CAP = 150;
const CACHE_TTL = 24 * 60 * 60 * 1000;
const MAX_CACHE = 500;
const NO_KEY = 'place search is not configured';
const OVER_BUDGET = 'place search is over its daily budget — try again tomorrow';

const cache = new Map();
let day = '';
let count = 0;
let exhaustedUntil = 0;

export function placesKey() {
  return process.env.GOOGLE_PLACES_KEY || null;
}

function cleanQuery(value) {
  return String(value || '').trim().replace(/\s+/g, ' ').slice(0, 120);
}

function today() {
  return new Date().toISOString().slice(0, 10);
}

function nextUtcMidnight() {
  const next = new Date();
  next.setUTCHours(24, 0, 0, 0);
  return next.getTime();
}

function resetDay() {
  const current = today();
  if (day !== current) {
    day = current;
    count = 0;
    exhaustedUntil = 0;
  }
}

function budgetAvailable() {
  resetDay();
  if (Date.now() < exhaustedUntil) return false;
  if (count >= DAILY_CAP) {
    exhaustedUntil = nextUtcMidnight();
    return false;
  }
  count += 1;
  return true;
}

function cached(key) {
  const hit = cache.get(key);
  if (!hit) return null;
  if (Date.now() - hit.at >= CACHE_TTL) {
    cache.delete(key);
    return null;
  }
  return hit.value;
}

function store(key, value) {
  cache.set(key, { at: Date.now(), value });
  while (cache.size > MAX_CACHE) cache.delete(cache.keys().next().value);
  return value;
}

async function post(url, key, fields, body) {
  try {
    const response = await fetch(url, {
      method: 'POST',
      signal: AbortSignal.timeout(4000),
      headers: {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': key,
        'X-Goog-FieldMask': fields,
      },
      body: JSON.stringify(body),
    });
    if (response.status === 429) {
      exhaustedUntil = nextUtcMidnight();
      return { error: OVER_BUDGET };
    }
    if (!response.ok) return { error: `place search failed (${response.status})` };
    return await response.json();
  } catch {
    return { error: 'place search unavailable right now' };
  }
}

export async function autocomplete({ input } = {}) {
  const key = placesKey();
  if (!key) return { error: NO_KEY };
  const query = cleanQuery(input);
  if (query.length < 3) return { predictions: [] };
  const cacheKey = `autocomplete:${query.toLowerCase()}`;
  const hit = cached(cacheKey);
  if (hit) return hit;
  if (!budgetAvailable()) return { error: OVER_BUDGET };

  const body = await post(AUTOCOMPLETE_URL, key, AUTOCOMPLETE_FIELDS, {
    input: query,
    includedRegionCodes: ['us'],
    locationRestriction: { rectangle: SF_RECTANGLE },
  });
  if (body.error) return body;
  const predictions = (body.suggestions || [])
    .map((suggestion) => suggestion.placePrediction)
    .filter(Boolean)
    .slice(0, 5)
    .map((prediction) => ({
      placeId: String(prediction.place || '').replace(/^places\//, ''),
      text: prediction.text?.text || '',
      mainText: prediction.structuredFormat?.mainText?.text || '',
      secondaryText: prediction.structuredFormat?.secondaryText?.text || '',
    }))
    .filter((prediction) => prediction.text);
  return store(cacheKey, { predictions });
}

export async function findPlace({ query: input } = {}) {
  const key = placesKey();
  if (!key) return { error: NO_KEY };
  const query = cleanQuery(input);
  if (!query) return { error: 'place query is required' };
  const cacheKey = `search:${query.toLowerCase()}`;
  const hit = cached(cacheKey);
  if (hit) return hit;
  if (!budgetAvailable()) return { error: OVER_BUDGET };

  const body = await post(SEARCH_URL, key, SEARCH_FIELDS, {
    textQuery: query,
    maxResultCount: 5,
    regionCode: 'US',
    locationRestriction: { rectangle: SF_RECTANGLE },
  });
  if (body.error) return body;
  const results = (body.places || [])
    .slice(0, 5)
    .map((place) => {
      const lat = Number(place.location?.latitude);
      const lon = Number(place.location?.longitude);
      if (!Number.isFinite(lat) || !Number.isFinite(lon)) return null;
      if (
        lat < SF_RECTANGLE.low.latitude ||
        lat > SF_RECTANGLE.high.latitude ||
        lon < SF_RECTANGLE.low.longitude ||
        lon > SF_RECTANGLE.high.longitude
      ) {
        return null;
      }
      return {
        name: String(place.displayName?.text || query).slice(0, 80),
        address: place.formattedAddress
          ? String(place.formattedAddress).slice(0, 120)
          : null,
        lat: Number(lat.toFixed(6)),
        lon: Number(lon.toFixed(6)),
        types: Array.isArray(place.types) ? place.types.slice(0, 4) : [],
        status: place.businessStatus
          ? String(place.businessStatus).toLowerCase().replace(/_/g, ' ')
          : null,
      };
    })
    .filter(Boolean);
  return store(cacheKey, { query, results });
}

export async function resolvePlace({ query } = {}) {
  const result = await findPlace({ query });
  if (result.error) return result;
  return { query: result.query, place: result.results[0] || null };
}

// Kept out of the production API surface; unit tests use it to isolate cache
// and budget behavior without waiting for UTC midnight.
export function resetPlacesForTests() {
  cache.clear();
  day = '';
  count = 0;
  exhaustedUntil = 0;
}
