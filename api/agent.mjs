// POST /api/agent — the city concierge.
//
// Without AI_GATEWAY_API_KEY the endpoint answers 503 and the client hides the
// panel: the city itself never needs a key, and no key ever reaches the browser.

import { readFile } from 'node:fs/promises';
import { createTools, runTurn, sanitizeContext, sanitizeMessages } from './_lib/agent-core.mjs';

const WINDOW_MINUTE = 60 * 1000;
const WINDOW_DAY = 24 * 60 * 60 * 1000;
const PER_MINUTE = 8;
const PER_DAY = 60;

const hits = new Map();

function rateLimited(ip) {
  const now = Date.now();
  const record = hits.get(ip) || { minute: [], day: [] };
  record.minute = record.minute.filter((t) => now - t < WINDOW_MINUTE);
  record.day = record.day.filter((t) => now - t < WINDOW_DAY);
  if (record.minute.length >= PER_MINUTE || record.day.length >= PER_DAY) {
    hits.set(ip, record);
    return true;
  }
  record.minute.push(now);
  record.day.push(now);
  hits.set(ip, record);
  // The map is only as large as the distinct callers a warm instance sees.
  if (hits.size > 5000) hits.clear();
  return false;
}

let dataPromise = null;

// The bake, loaded once per warm instance. The place index lives beside the
// function (api/_data) so it is never served to the browser.
function loadData() {
  if (dataPromise) return dataPromise;
  const read = async (path) => JSON.parse(await readFile(new URL(path, import.meta.url), 'utf8'));
  dataPromise = Promise.all([
    read('./_data/places.json'),
    read('./_data/search-index.json'),
    read('./_data/parks.json'),
    read('./_data/neighborhoods.json'),
    read('./_data/streets.json'),
    read('./_data/stats.json'),
    // Stop index for transit_nearby. Optional: a deployment without it just
    // loses that one tool rather than failing to answer anything at all.
    read('./_data/muni-stops.json').catch(() => null),
  ]).then(([places, search, parks, neighborhoods, streets, stats, muniStops]) => ({
    places,
    search,
    parks,
    neighborhoods,
    streets,
    stats,
    muniStops: muniStops?.stops || null,
    muniRoutes: muniStops?.busRoutes || [],
  }));
  return dataPromise;
}

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    res.status(405).json({ error: 'method not allowed' });
    return;
  }
  const apiKey = process.env.AI_GATEWAY_API_KEY;
  if (!apiKey) {
    res.status(503).json({ error: 'concierge offline' });
    return;
  }
  const ip = (req.headers['x-forwarded-for'] || '').split(',')[0].trim() || 'local';
  if (rateLimited(ip)) {
    res.status(429).json({ error: 'too many questions for one minute — try again shortly' });
    return;
  }

  try {
    const body = typeof req.body === 'string' ? JSON.parse(req.body) : req.body || {};
    const messages = sanitizeMessages(body.messages);
    if (!messages.length) {
      res.status(400).json({ error: 'no message' });
      return;
    }
    const data = await loadData();
    const result = await runTurn({
      messages,
      context: sanitizeContext(body.context),
      tools: createTools(data),
      apiKey,
    });
    res.status(200).json(result);
  } catch (error) {
    res.status(502).json({ error: `concierge failed: ${error.message}` });
  }
}
