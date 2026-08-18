// The live-feed dispatcher: every /api/<feed> route not claimed by a real file
// (agent.mjs stays its own function) lands here and is served from the feed
// registry. All feeds deliberately share this ONE function so their caches live
// in one process — that is what lets /api/live compose a consolidated snapshot
// from memory instead of HTTP-calling the city's own endpoints.
//
// Adding a feed touches only api/_lib/feeds/ — see the recipe in feedcore.mjs.

import {
  forceRefresh,
  getFeed,
  serveFeed,
  serveLive,
} from "./_lib/feedcore.mjs";
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
  const secret = process.env.CRON_SECRET;
  if (secret && req.headers.authorization !== `Bearer ${secret}`) {
    res.status(401).json({ error: "unauthorized" });
    return;
  }
  const entry = getFeed("feed");
  if (!entry) {
    res.status(404).json({ error: "no feed to tick" });
    return;
  }
  const started = Date.now();
  const failed = await forceRefresh(entry);
  const data = entry.data ?? {};
  res.status(failed ? 503 : 200).json({
    ticked: !failed,
    error: failed ?? null,
    ms: Date.now() - started,
    threads: data.threads?.length ?? 0,
    written: data.written ?? 0,
  });
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
