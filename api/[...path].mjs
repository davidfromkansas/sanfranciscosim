// The live-feed dispatcher: every /api/<feed> route not claimed by a real file
// (agent.mjs stays its own function) lands here and is served from the feed
// registry. All feeds deliberately share this ONE function so their caches live
// in one process — that is what lets /api/live compose a consolidated snapshot
// from memory instead of HTTP-calling the city's own endpoints.
//
// Adding a feed touches only api/_lib/feeds/ — see the recipe in feedcore.mjs.

import { getFeed, publish, serveFeed, serveLive } from "./_lib/feedcore.mjs";
import "./_lib/feeds/index.mjs";
// serveTick calls into the subreddit directly. index.mjs only registers feeds;
// it exports nothing, so these have to be named here.
import {
  advanceSubreddit,
  postIsDue,
  readSubreddit,
  submitHumanPost,
} from "./_lib/feeds/residents.mjs";
import { autocomplete, resolvePlace } from "./_lib/places.mjs";

const COMPOSE_WINDOW_MINUTE = 60 * 1000;
const COMPOSE_WINDOW_DAY = 24 * 60 * 60 * 1000;
const COMPOSE_PER_MINUTE = 3;
const COMPOSE_PER_DAY = 24;
const composeHits = new Map();
const PLACES_WINDOW_MINUTE = 60 * 1000;
const PLACES_WINDOW_DAY = 24 * 60 * 60 * 1000;
const PLACES_PER_MINUTE = 30;
const PLACES_PER_DAY = 500;
const placesHits = new Map();

function composeRateLimited(ip) {
  const now = Date.now();
  const record = composeHits.get(ip) || { minute: [], day: [] };
  record.minute = record.minute.filter(
    (at) => now - at < COMPOSE_WINDOW_MINUTE,
  );
  record.day = record.day.filter((at) => now - at < COMPOSE_WINDOW_DAY);
  if (
    record.minute.length >= COMPOSE_PER_MINUTE ||
    record.day.length >= COMPOSE_PER_DAY
  ) {
    composeHits.set(ip, record);
    return true;
  }
  record.minute.push(now);
  record.day.push(now);
  composeHits.set(ip, record);
  if (composeHits.size > 5000) composeHits.clear();
  return false;
}

function requestIp(req) {
  return (
    (req.headers["x-forwarded-for"] || "").split(",")[0].trim() || "local"
  );
}

function placesRateLimited(ip) {
  const now = Date.now();
  const record = placesHits.get(ip) || { minute: [], day: [] };
  record.minute = record.minute.filter((at) => now - at < PLACES_WINDOW_MINUTE);
  record.day = record.day.filter((at) => now - at < PLACES_WINDOW_DAY);
  if (
    record.minute.length >= PLACES_PER_MINUTE ||
    record.day.length >= PLACES_PER_DAY
  ) {
    placesHits.set(ip, record);
    return true;
  }
  record.minute.push(now);
  record.day.push(now);
  placesHits.set(ip, record);
  if (placesHits.size > 5000) placesHits.clear();
  return false;
}

async function servePlaces(req, res) {
  if (placesRateLimited(requestIp(req))) {
    res.status(429).json({ error: "too many place searches — try again shortly" });
    return;
  }
  let body;
  try {
    body = typeof req.body === "string" ? JSON.parse(req.body) : req.body || {};
  } catch {
    res.status(400).json({ error: "request body must be valid JSON" });
    return;
  }
  let result;
  if (body.action === "autocomplete") {
    result = await autocomplete({ input: body.input });
  } else if (body.action === "resolve") {
    result = await resolvePlace({ query: body.query });
  } else {
    res.status(400).json({ error: "unknown places action" });
    return;
  }
  res.status(result.error ? 503 : 200).json(result);
}

async function serveCompose(req, res) {
  const credential =
    process.env.AI_GATEWAY_API_KEY || process.env.VERCEL_OIDC_TOKEN;
  if (!credential) {
    res.status(503).json({ error: "cannot review posts right now" });
    return;
  }
  if (composeRateLimited(requestIp(req))) {
    res
      .status(429)
      .json({ error: "too many posts for now — try again shortly" });
    return;
  }

  let body;
  try {
    body = typeof req.body === "string" ? JSON.parse(req.body) : req.body || {};
  } catch {
    res.status(400).json({ error: "request body must be valid JSON" });
    return;
  }

  try {
    const result = await submitHumanPost({
      title: body.title,
      body: body.body,
    });
    if (result.payload) {
      const entry = getFeed("feed");
      if (entry) publish(entry, result.payload);
    }
    res.status(result.status).json(result.body);
  } catch (error) {
    res
      .status(502)
      .json({ error: `post review failed: ${error?.message || error}` });
  }
}

// The scheduled tick (vercel.json → crons). Without it the subreddit only
// advances when somebody is looking at it: generation was tied to a visitor
// arriving after the ttl had lapsed, so a quiet night produced a feed that had
// not moved since the last person left. Now the city talks to itself.
//
// Vercel signs cron requests with CRON_SECRET when it is set. If it is not set
// the route still works — the worst a stranger can do is make the subreddit
// generate early, which is exactly what it does on its own schedule anyway —
// but it should be set in production so nobody can spend the budget for you.
async function serveTick(req, res) {
  // Vercel sends `Authorization: Bearer <CRON_SECRET>` automatically whenever
  // that variable is set on the project. Refusing when the secret is MISSING
  // too — not just when it mismatches — means deleting the variable turns the
  // endpoint off rather than throwing it open. Cron runs against production
  // only, and local dev goes through the vite plugin, so nothing legitimate
  // depends on the unauthenticated path.
  const secret = process.env.CRON_SECRET;
  if (!secret || req.headers.authorization !== `Bearer ${secret}`) {
    res.status(401).json({ error: "unauthorized" });
    return;
  }
  const entry = getFeed("feed");
  if (!entry) {
    res.status(404).json({ error: "no feed to tick" });
    return;
  }
  // The cron fires every minute; the feed decides which minute is its own. Most
  // invocations do nothing and return immediately — that is the mechanism, not
  // a fault. `?force=1` skips the check for testing.
  const forced = new URL(req.url, "http://localhost").searchParams.get("force");
  if (!forced && !postIsDue()) {
    res.status(200).json({ ticked: false, reason: "not this minute" });
    return;
  }
  // Generation happens HERE and nowhere else. /api/feed only reads, so a
  // visitor never waits on a language model and never times out behind one.
  const started = Date.now();
  try {
    const data = await advanceSubreddit();
    publish(entry, data);
    res.status(200).json({
      ticked: true,
      ms: Date.now() - started,
      threads: data.threads.length,
      written: data.written,
    });
  } catch (error) {
    res
      .status(503)
      .json({ ticked: false, error: String(error?.message || error) });
  }
}

export default async function handler(req, res) {
  const pathname = new URL(req.url, "http://localhost").pathname.replace(
    /\/+$/,
    "",
  );

  if (pathname === "/api/compose" && req.method === "POST") {
    await serveCompose(req, res);
    return;
  }
  if (pathname === "/api/places") {
    if (req.method !== "POST") {
      res.status(405).json({ error: "method not allowed" });
      return;
    }
    await servePlaces(req, res);
    return;
  }
  if (req.method && req.method !== "GET") {
    res.status(405).json({ error: "method not allowed" });
    return;
  }

  if (pathname === "/api/live") {
    await serveLive(res);
    return;
  }
  if (pathname === "/api/tick") {
    await serveTick(req, res);
    return;
  }
  const entry = getFeed(pathname.replace(/^\/api\//, ""));
  if (entry) {
    // Page one is every visitor's first request and is identical for all of
    // them, so it goes through the registry and the CDN like everything else.
    // A request carrying a cursor is somebody scrolling — rarer, and a
    // different payload per cursor, which the registry cannot cache because it
    // holds ONE payload per feed. Those read straight through.
    const before = Number(
      new URL(req.url, "http://localhost").searchParams.get("before") || 0,
    );
    if (entry.name === "feed" && before > 0) {
      const limit = Number(
        new URL(req.url, "http://localhost").searchParams.get("limit") || 0,
      );
      try {
        const page = await readSubreddit({ before, limit });
        // Pages of the past do not change, so they cache hard — but only at the
        // edge, and only a page that actually found something.
        res.setHeader(
          "Cache-Control",
          page.threads.length
            ? "public, max-age=0, s-maxage=300, stale-while-revalidate=600"
            : "no-store",
        );
        res.status(200).json(page);
      } catch (error) {
        res.status(503).json({ error: String(error?.message || error) });
      }
      return;
    }
    await serveFeed(res, entry);
    return;
  }
  res.status(404).json({ error: "unknown endpoint" });
}
