// The live-feed dispatcher: every /api/<feed> route not claimed by a real file
// (agent.mjs stays its own function) lands here and is served from the feed
// registry. All feeds deliberately share this ONE function so their caches live
// in one process — that is what lets /api/live compose a consolidated snapshot
// from memory instead of HTTP-calling the city's own endpoints.
//
// Adding a feed touches only api/_lib/feeds/ — see the recipe in feedcore.mjs.

import { getFeed, serveFeed, serveLive } from "./_lib/feedcore.mjs";
import "./_lib/feeds/index.mjs";

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
  if (!forced && !postIsDue() && !(await stillFilling())) {
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
  if (req.method && req.method !== "GET") {
    res.status(405).json({ error: "method not allowed" });
    return;
  }
  const pathname = new URL(req.url, "http://localhost").pathname.replace(
    /\/+$/,
    "",
  );

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
    await serveFeed(res, entry);
    return;
  }
  res.status(404).json({ error: "unknown endpoint" });
}
