// The concierge's brain, kept out of the HTTP handler so it can be tested and
// reasoned about on its own.
//
// Two rules shape everything here. First, the model only ever sees data that
// came out of the bake, so it cannot invent a building. Second, it never
// touches the scene: "move the camera" is a validated intent the client applies
// itself, clamped to the city's own extent.

import { skySnapshot } from './astro.mjs';

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

Answer in at most four short sentences. No lists unless asked.`;

const TOOLS = [
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

// The read-only tools. `data` is the loaded bake: nothing is fetched per call.
export function createTools(data) {
  const { search, places, parks, neighborhoods, streets, stats } = data;

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
        const value = JSON.stringify(tool(call.input || {}));
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
