// The concierge's brain, kept out of the HTTP handler so it can be tested and
// reasoned about on its own.
//
// Two rules shape everything here. First, the model only ever sees data that
// came out of the bake, so it cannot invent a building. Second, it never
// touches the scene: "move the camera" is a validated intent the client applies
// itself, clamped to the city's own extent.

import { skySnapshot } from './astro.mjs';
// Imported only to enumerate the registered live feeds for the live_data tool:
// the registrations run here, but this function never fetches an upstream —
// live_data goes through the deployment's own /api/<feed> URLs, so reads hit
// the CDN/dispatcher cache and cost no extra upstream quota.
import { allFeeds } from './feedcore.mjs';
import './feeds/index.mjs';

const MODEL = 'anthropic/claude-sonnet-5';
const ENDPOINT = 'https://ai-gateway.vercel.sh/v1/messages';
const MAX_TOKENS = 1000;
const MAX_ROUNDS = 6;
const MAX_TOOL_CHARS = 6000;
const TURN_BUDGET_MS = 60000;

export const EXTENT = { minX: -7700, maxX: 7700, minZ: -7740, maxZ: 7740 };

const SYSTEM = `You are the concierge of a data-accurate 3D model of San Francisco.

Every fact you state must come from a tool result. The model is built from open
data (DataSF footprints, streets, facilities, land use, parks and
neighbourhoods; OpenStreetMap tags; Overture/Foursquare places), and building
identities carry a confidence level — say when something is inferred rather
than recorded. If the data does not say, say that it does not say. Never invent
a name, a year, a tenant or a story.

You can move the viewer: call set_camera, focus_entity or highlight. Prefer
focus_entity with a real entity id from a tool result. Coordinates are metres in
the model's own frame (x east, z south of Duboce Triangle), not latitude and
longitude.

The model's sky is the real one: it runs on San Francisco's wall clock, with the
sun and moon where they actually are. Call sky_now for anything about the time,
the light, sunrise or sunset, or the moon. You cannot change the time of day.

Transit questions — when the next bus or train comes, what stops are near a
place, which routes serve it — go to transit_nearby, never to live_data: it
answers from the same live feed but scoped to one place, where live_data would
return the whole citywide fleet and be cut off. Resolve the place first.

Some of the city is live: call live_data with exactly the feeds a question
needs — one feed, or several in a single call when the answer spans sources.
Live readings are real: report how fresh they are (from each feed's fetchedAt),
and if a feed is unavailable or stale, say so and answer from what you have.

Answer in at most four short sentences. No lists unless asked.`;

const LIVE_FEEDS = allFeeds();
const LIVE_FEED_NAMES = LIVE_FEEDS.map((f) => f.name);

const TOOLS = [
  {
    name: 'live_data',
    description:
      `Real-time readings from the living city, one shopping-list call: request exactly the feeds the question needs. Feeds: ${LIVE_FEEDS.map((f) => `${f.name} — ${f.describe}`).join('; ')}. Each feed returns { live, fetchedAt, stale, ... }.`,
    input_schema: {
      type: 'object',
      properties: {
        feeds: {
          type: 'array',
          items: { type: 'string', enum: LIVE_FEED_NAMES },
          minItems: 1,
          maxItems: 4,
        },
      },
      required: ['feeds'],
    },
  },
  {
    name: 'search_city',
    description:
      'Search the baked index of named buildings, streets, parks, neighbourhoods and landmarks. Returns ids and model coordinates.',
    input_schema: {
      type: 'object',
      properties: {
        query: { type: 'string' },
        kind: { type: 'string', enum: ['any', 'building', 'street', 'park', 'neighborhood', 'landmark'] },
        limit: { type: 'integer' },
      },
      required: ['query'],
    },
  },
  {
    name: 'search_places',
    description:
      'Search open place records (Overture, which redistributes the Foursquare open places set) by name or category. Use for "where can I get coffee"-style questions.',
    input_schema: {
      type: 'object',
      properties: { query: { type: 'string' }, near: { type: 'array', items: { type: 'number' } }, limit: { type: 'integer' } },
      required: ['query'],
    },
  },
  {
    name: 'describe_area',
    description:
      'What is around a point: the neighbourhood, the nearest named streets, the nearest parks and the category mix of nearby buildings.',
    input_schema: {
      type: 'object',
      properties: { x: { type: 'number' }, z: { type: 'number' }, radius: { type: 'number' } },
      required: ['x', 'z'],
    },
  },
  {
    name: 'transit_nearby',
    description:
      'When the next Muni vehicles reach the stops around a point: the nearest stops by walking distance, each with the next arrivals (route, mode, minutes away, fleet number). THE tool for "when is the next bus/train", "what stops near here", "how do I get somewhere" — do not use live_data for those, it returns the whole citywide fleet and gets truncated. Resolve an address or place to x/z first with search_city or search_places.',
    input_schema: {
      type: 'object',
      properties: {
        x: { type: 'number' },
        z: { type: 'number' },
        radius: { type: 'number', description: 'metres, default 400, max 1200' },
        route: { type: 'string', description: 'optional: only this route, e.g. "38R"' },
      },
      required: ['x', 'z'],
    },
  },
  {
    name: 'sky_now',
    description:
      "The sky over San Francisco right now, computed from the wall clock — local time and date, the sun's elevation and azimuth with today's sunrise, sunset and solar noon, and the moon's elevation, azimuth, rise, set, illuminated fraction and phase name. Use it for any question about the time, the light, the sunset or the moon. It is the same sky the viewer is looking at.",
    input_schema: { type: 'object', properties: {} },
  },
  {
    name: 'city_stats',
    description: 'Citywide counts: buildings per category, streets, parks, neighbourhoods, data sources.',
    input_schema: { type: 'object', properties: {} },
  },
  {
    name: 'set_camera',
    description: 'Move the viewer to a point in the model. Returns nothing to reason about; it just moves the view.',
    input_schema: {
      type: 'object',
      properties: {
        x: { type: 'number' },
        z: { type: 'number' },
        distance: { type: 'number' },
        yaw: { type: 'number' },
        pitch: { type: 'number' },
      },
      required: ['x', 'z'],
    },
  },
  {
    name: 'focus_entity',
    description: 'Select an entity by id (from a tool result) and fly to it.',
    input_schema: {
      type: 'object',
      properties: { id: { type: 'string' }, x: { type: 'number' }, z: { type: 'number' }, title: { type: 'string' } },
      required: ['id'],
    },
  },
  {
    name: 'highlight',
    description: 'Select an entity without moving the camera.',
    input_schema: {
      type: 'object',
      properties: { id: { type: 'string' }, x: { type: 'number' }, z: { type: 'number' }, title: { type: 'string' } },
      required: ['id'],
    },
  },
];

const INTENT_TOOLS = new Set(['set_camera', 'focus_entity', 'highlight']);

const clamp = (value, min, max, fallback) =>
  Number.isFinite(value) ? Math.min(max, Math.max(min, value)) : fallback;

// Scene intents are rebuilt field by field rather than forwarded: the client
// must never receive a key the model made up.
export function validateIntent(name, input) {
  if (name === 'set_camera') {
    return {
      type: 'set_camera',
      x: clamp(input.x, EXTENT.minX, EXTENT.maxX, 0),
      z: clamp(input.z, EXTENT.minZ, EXTENT.maxZ, 0),
      distance: clamp(input.distance, 80, 12000, 800),
      yaw: clamp(input.yaw, -720, 720, 210),
      pitch: clamp(input.pitch, 8, 80, 32),
    };
  }
  if (!/^(b|street|park|nhood|landmark|view):/.test(String(input.id || ''))) return null;
  return {
    type: name === 'focus_entity' ? 'focus_entity' : 'highlight',
    id: String(input.id).slice(0, 80),
    title: typeof input.title === 'string' ? input.title.slice(0, 120) : undefined,
    x: clamp(input.x, EXTENT.minX, EXTENT.maxX, undefined),
    z: clamp(input.z, EXTENT.minZ, EXTENT.maxZ, undefined),
  };
}

export function sanitizeContext(context) {
  if (!context || typeof context !== 'object') return null;
  const camera = context.camera || {};
  const focus = context.focus || null;
  return {
    camera: {
      x: clamp(camera.x, EXTENT.minX, EXTENT.maxX, 0),
      z: clamp(camera.z, EXTENT.minZ, EXTENT.maxZ, 0),
      distance: clamp(camera.distance, 10, 20000, 900),
      yaw: clamp(camera.yaw, -720, 720, 0),
    },
    style: context.style === 'toy' ? 'toy' : 'base',
    neighborhood: typeof context.neighborhood === 'string' ? context.neighborhood.slice(0, 60) : null,
    focus: focus
      ? {
          kind: String(focus.kind || '').slice(0, 20),
          id: String(focus.id || '').slice(0, 80),
          title: String(focus.title || '').slice(0, 120),
          x: clamp(focus.x, EXTENT.minX, EXTENT.maxX, 0),
          z: clamp(focus.z, EXTENT.minZ, EXTENT.maxZ, 0),
        }
      : null,
  };
}

export function sanitizeMessages(messages) {
  if (!Array.isArray(messages)) return [];
  return messages
    .slice(-12)
    .filter((m) => m && (m.role === 'user' || m.role === 'assistant') && typeof m.content === 'string')
    .map((m) => ({ role: m.role, content: m.content.slice(0, 2000) }));
}

const distance = (ax, az, bx, bz) => Math.hypot(ax - bx, az - bz);

// This deployment's own base URL for live_data's self-fetch. VERCEL_URL is the
// per-deployment host (works on production and previews alike); locally under
// `vercel dev` it is a localhost origin. Absent both (plain vite dev, tests),
// live_data reports itself unavailable instead of erroring the turn.
function selfBase() {
  const host = process.env.VERCEL_URL || process.env.VERCEL_PROJECT_PRODUCTION_URL || '';
  if (!host) return null;
  if (/^https?:\/\//.test(host)) return host;
  return /^(localhost|127\.)/.test(host) ? `http://${host}` : `https://${host}`;
}

const LIVE_FETCH_TIMEOUT_MS = 5000;

// Shrink one feed's payload to its share of the tool budget by halving its
// largest array (vessels, vehicles, …) until it fits, recording what was cut.
// Generic on purpose: future feeds inherit it without per-feed code.
function fitBudget(payload, budget) {
  let out = payload;
  let json = JSON.stringify(out);
  while (json.length > budget) {
    const arrays = Object.entries(out)
      .filter(([, v]) => Array.isArray(v) && v.length > 1)
      .sort((a, b) => JSON.stringify(b[1]).length - JSON.stringify(a[1]).length);
    if (!arrays.length) break; // nothing left to trim; the global cap still applies
    const [key, arr] = arrays[0];
    const keep = Math.ceil(arr.length / 2);
    out = { ...out, [key]: arr.slice(0, keep), [`${key}_omitted`]: (out[`${key}_omitted`] || 0) + (arr.length - keep) };
    json = JSON.stringify(out);
  }
  return out;
}

// The read-only tools. `data` is the loaded bake; only live_data fetches, and
// only from the city's own feed endpoints.
export function createTools(data) {
  const { search, places, parks, neighborhoods, streets, stats, muniStops } = data;

  function pointInRings(x, z, rings) {
    for (const ring of rings) {
      let inside = false;
      for (let i = 0, j = ring.length - 2; i < ring.length; j = i, i += 2) {
        const xi = ring[i];
        const zi = ring[i + 1];
        const xj = ring[j];
        const zj = ring[j + 1];
        if (zi > z !== zj > z && x < ((xj - xi) * (z - zi)) / (zj - zi) + xi) inside = !inside;
      }
      if (inside) return true;
    }
    return false;
  }

  return {
    // The one async tool: fetches the requested feeds concurrently from the
    // deployment's own /api/<feed> endpoints (CDN-cached — no extra upstream
    // quota). Each feed fails soft, so a dead source never sinks the answer.
    async live_data({ feeds }) {
      const wanted = [...new Set(Array.isArray(feeds) ? feeds.map(String) : [])].slice(0, 4);
      const known = wanted.filter((name) => LIVE_FEED_NAMES.includes(name));
      if (!known.length) {
        return { error: `no known feeds requested; available: ${LIVE_FEED_NAMES.join(', ')}` };
      }
      const base = selfBase();
      if (!base) {
        return { error: 'live data is unavailable in this environment' };
      }
      const budget = Math.floor(MAX_TOOL_CHARS / known.length) - 40;
      const out = {};
      await Promise.all(
        known.map(async (name) => {
          const controller = new AbortController();
          const timer = setTimeout(() => controller.abort(), LIVE_FETCH_TIMEOUT_MS);
          try {
            const res = await fetch(`${base}/api/${name}`, {
              signal: controller.signal,
              headers: { accept: 'application/json' },
            });
            if (!res.ok) throw new Error(`http ${res.status}`);
            const payload = await res.json();
            delete payload.now; // redundant with fetchedAt for the model
            out[name] = fitBudget(payload, budget);
          } catch {
            out[name] = { error: 'unavailable' };
          } finally {
            clearTimeout(timer);
          }
        }),
      );
      return out;
    },

    // Stop-centric view of the live fleet. The vehicle feed carries, per
    // vehicle, the next few stops it is predicted to reach; inverting that
    // against the baked stop index turns "where is every bus" into the question
    // people actually ask: "what is coming, here, soon". Filtering by place
    // BEFORE returning is the point — the result is a few hundred bytes, so the
    // 6 KB tool-result clamp never truncates a transit answer.
    async transit_nearby({ x, z, radius = 400, route = null }) {
      if (!Number.isFinite(x) || !Number.isFinite(z)) return { error: 'x and z are required' };
      if (!muniStops) return { error: 'transit stop index unavailable' };
      const r = Math.min(1200, Math.max(100, radius));
      const base = selfBase();
      if (!base) return { error: 'live data is unavailable in this environment' };

      let payload;
      const controller = new AbortController();
      const timer = setTimeout(() => controller.abort(), LIVE_FETCH_TIMEOUT_MS);
      try {
        const res = await fetch(`${base}/api/muni`, {
          signal: controller.signal,
          headers: { accept: 'application/json' },
        });
        if (!res.ok) throw new Error(`http ${res.status}`);
        payload = await res.json();
      } catch {
        return { error: 'the live Muni feed is unavailable right now' };
      } finally {
        clearTimeout(timer);
      }
      if (!payload?.live) {
        return { live: false, reason: payload?.reason || 'feed offline', stops: [] };
      }

      const wanted = route ? String(route).toUpperCase() : null;
      const now = Date.now();
      // stopId -> arrivals, built only for stops inside the radius.
      const inRange = new Map();
      for (const vehicle of payload.vehicles || []) {
        if (wanted && String(vehicle.route).toUpperCase() !== wanted) continue;
        for (const stop of vehicle.stops || []) {
          const entry = muniStops[stop.stopId];
          if (!entry) continue;
          const d = distance(x, z, entry[1], entry[2]);
          if (d > r) continue;
          let bucket = inRange.get(stop.stopId);
          if (!bucket) inRange.set(stop.stopId, (bucket = { name: entry[0], x: entry[1], z: entry[2], walk_m: Math.round(d), arrivals: [] }));
          bucket.arrivals.push({
            route: vehicle.route,
            mode: vehicle.mode,
            direction: vehicle.directionId,
            minutes: Math.max(0, Math.round((stop.arrivalAt - now) / 60000)),
            at: stop.arrivalAt,
            fleet_number: vehicle.fleetNumber,
          });
        }
      }

      const ranked = [...inRange.values()]
        .map((stop) => {
          stop.arrivals.sort((a, b) => a.at - b.at);
          stop.arrivals = stop.arrivals.slice(0, 3);
          return stop;
        })
        .sort((a, b) => (a.arrivals[0]?.at ?? Infinity) - (b.arrivals[0]?.at ?? Infinity) || a.walk_m - b.walk_m);

      // Pick for ROUTE VARIETY, not just for the soonest times. A busy corridor
      // puts six consecutive stops of one line at the top of a time sort, which
      // reads as "only the 31 runs here" when the 38 is a block away. So: the
      // best stop for each distinct route first, then fill by proximity.
      const stops = [];
      const seenRoutes = new Set();
      for (const stop of ranked) {
        const route = stop.arrivals[0]?.route;
        if (route == null || seenRoutes.has(route)) continue;
        seenRoutes.add(route);
        stops.push(stop);
        if (stops.length >= 6) break;
      }
      for (const stop of [...ranked].sort((a, b) => a.walk_m - b.walk_m)) {
        if (stops.length >= 6) break;
        if (!stops.includes(stop)) stops.push(stop);
      }

      return {
        live: true,
        degraded: payload.degraded || undefined,
        fetchedAt: payload.fetchedAt,
        stale: payload.stale,
        searched_radius_m: r,
        // Said explicitly so the model never reads an empty result as "no service".
        horizon_note: 'Only arrivals within roughly the next 12 minutes are predicted; an empty result means nothing is due that soon, not that the stop has no service.',
        stops,
      };
    },

    search_city({ query, kind = 'any', limit = 8 }) {
      const q = String(query || '').toLowerCase().trim();
      if (!q) return [];
      const out = [];
      for (const entry of search) {
        if (kind !== 'any' && entry.t !== kind) continue;
        if (!entry.q.includes(q)) continue;
        out.push({ id: entry.id, name: entry.n, kind: entry.t, x: entry.x, z: entry.z });
        if (out.length >= Math.min(20, Math.max(1, limit))) break;
      }
      return out;
    },

    search_places({ query, near, limit = 8 }) {
      const q = String(query || '').toLowerCase().trim();
      if (!q) return [];
      const [nx, nz] = Array.isArray(near) && near.length === 2 ? near : [null, null];
      const hits = [];
      for (const place of places) {
        const name = place.n.toLowerCase();
        const category = (place.c || '').toLowerCase();
        if (!name.includes(q) && !category.includes(q)) continue;
        const d = nx === null ? 0 : distance(nx, nz, place.x, place.z);
        hits.push({ name: place.n, category: place.c, address: place.a, x: place.x, z: place.z, distance_m: Math.round(d) });
      }
      hits.sort((a, b) => a.distance_m - b.distance_m);
      return hits.slice(0, Math.min(20, Math.max(1, limit)));
    },

    describe_area({ x, z, radius = 400 }) {
      const r = Math.min(2000, Math.max(80, radius));
      const nhood = neighborhoods.find((n) => pointInRings(x, z, n.rings));
      const nearStreets = streets
        .map((s) => ({ name: s.name, d: distance(x, z, s.x, s.z) }))
        .filter((s) => s.d < r * 4)
        .sort((a, b) => a.d - b.d)
        .slice(0, 6)
        .map((s) => s.name);
      const nearParks = parks
        .map((p) => ({ name: p.name, d: distance(x, z, p.x, p.z) }))
        .filter((p) => p.d < r * 3)
        .sort((a, b) => a.d - b.d)
        .slice(0, 4)
        .map((p) => `${p.name} (${Math.round(p.d)} m)`);
      const nearPlaces = places
        .map((p) => ({ name: p.n, category: p.c, d: distance(x, z, p.x, p.z) }))
        .filter((p) => p.d < r)
        .sort((a, b) => a.d - b.d)
        .slice(0, 10);
      return {
        neighborhood: nhood ? nhood.name : null,
        streets: nearStreets,
        parks: nearParks,
        places: nearPlaces.map((p) => `${p.name}${p.category ? ` — ${p.category}` : ''} (${Math.round(p.d)} m)`),
      };
    },

    // No arguments and no network: the astronomy is computed here, and the
    // browser runs the very same module to light the scene.
    sky_now() {
      return skySnapshot(Date.now());
    },

    city_stats() {
      return {
        buildings: stats.buildings,
        categories: stats.categories.filter((c) => c.count > 0).map((c) => `${c.label}: ${c.count}`),
        streets_km: stats.streets.km,
        named_streets: stats.streets.named,
        parks: stats.parks,
        neighborhoods: stats.neighborhoods,
        notables: stats.notables,
        sources: stats.sources,
        attribution: stats.attribution,
      };
    },
  };
}

// One turn: tool rounds until the model answers, or the budget runs out.
export async function runTurn({ messages, context, tools, apiKey, fetchImpl = fetch }) {
  const intents = [];
  const started = Date.now();
  const history = [...messages];
  if (context) {
    history.unshift({
      role: 'user',
      content: `[viewer state] ${JSON.stringify(context)}`,
    });
  }

  for (let round = 0; round < MAX_ROUNDS; round++) {
    if (Date.now() - started > TURN_BUDGET_MS) break;
    const res = await fetchImpl(ENDPOINT, {
      method: 'POST',
      headers: {
        'content-type': 'application/json',
        authorization: `Bearer ${apiKey}`,
        'anthropic-version': '2023-06-01',
      },
      body: JSON.stringify({
        model: MODEL,
        max_tokens: MAX_TOKENS,
        system: SYSTEM,
        tools: TOOLS,
        messages: history,
      }),
    });
    if (!res.ok) {
      const detail = await res.text();
      throw new Error(`gateway ${res.status}: ${detail.slice(0, 300)}`);
    }
    const body = await res.json();
    const blocks = Array.isArray(body.content) ? body.content : [];
    const text = blocks
      .filter((b) => b.type === 'text')
      .map((b) => b.text)
      .join('\n')
      .trim();
    const calls = blocks.filter((b) => b.type === 'tool_use');
    if (!calls.length) return { text, intents };

    history.push({ role: 'assistant', content: blocks });
    const results = [];
    for (const call of calls) {
      if (INTENT_TOOLS.has(call.name)) {
        const intent = validateIntent(call.name, call.input || {});
        if (intent) intents.push(intent);
        results.push({
          type: 'tool_result',
          tool_use_id: call.id,
          content: intent ? 'done' : 'rejected: unknown entity id',
        });
        continue;
      }
      const tool = tools[call.name];
      if (!tool) {
        results.push({ type: 'tool_result', tool_use_id: call.id, content: 'no such tool', is_error: true });
        continue;
      }
      try {
        const value = JSON.stringify(await tool(call.input || {}));
        results.push({ type: 'tool_result', tool_use_id: call.id, content: value.slice(0, MAX_TOOL_CHARS) });
      } catch (error) {
        results.push({ type: 'tool_result', tool_use_id: call.id, content: `error: ${error.message}`, is_error: true });
      }
    }
    history.push({ role: 'user', content: results });
  }

  return { text: 'That took too many steps — try asking something narrower.', intents };
}

export const AGENT_LIMITS = { MAX_ROUNDS, MAX_TOOL_CHARS, TURN_BUDGET_MS, MODEL, ENDPOINT };
