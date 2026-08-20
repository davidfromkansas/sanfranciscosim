// The live-feed registry — every live data source in the city goes through here.
//
// ADDING A NEW FEED — the whole recipe, nothing else:
//   1. Write one async fetcher in api/_lib/feeds/<name>.mjs that returns plain
//      JSON (fetch upstream, normalise, return the payload). Fetchers THROW on
//      failure — never return partial garbage; the registry serves last-good.
//   2. Register it in the same file:
//        registerFeed('muni', { ttl: 30_000, fetcher: fetchMuni, empty: { live: false, vehicles: [] } });
//   3. Import the file once from api/_lib/feeds/index.mjs.
//   The feed is now served at /api/<name> and included in /api/live.
//
// The registry owns: in-memory cache, lazy single-flight refresh, last-good
// stale serving with a per-feed horizon, failure backoff, fetchedAt/stale
// stamping, and CDN cache headers derived from the ttl. Keys load server-side
// only, inside fetchers, and never reach the browser.
//
// Accepted limits (deliberate, do not over-engineer): the cache is per warm
// instance and dies on cold start — a cold refetch is fine, and Fluid Compute
// reuses instances so it mostly survives. Real upstream rate is therefore
// (calls per hour) × (warm instances); a feed with a hard upstream quota should
// budget for a few instances, and the CDN layer absorbs most traffic anyway.

const feeds = new Map();

export function registerFeed(
  name,
  {
    ttl,
    fetcher,
    empty = {},
    backoffMs = 60_000,
    staleMs = 10 * 60_000,
    swrMs,
    describe,
  },
) {
  feeds.set(name, {
    name,
    describe: describe || "live city data", // one line for the concierge's live_data tool
    ttl,
    fetcher,
    empty,
    backoffMs, // after a failed refresh, don't hit the upstream again for this long
    staleMs, // serve last-good data up to this age; beyond it, serve `empty`
    swrMs: swrMs ?? Math.min(ttl * 4, 600_000),
    data: null,
    fetchedAt: 0,
    refreshing: null,
    backoffUntil: 0,
    lastError: null,
  });
}

export const getFeed = (name) => feeds.get(name);
export const allFeeds = () => [...feeds.values()];

// Refresh-if-stale, single-flight: concurrent requests share one upstream call.
// Resolves even on upstream failure — callers then serve last-good via payload().
// Force a refresh regardless of ttl, for the scheduled tick. Shares the same
// single-flight promise as ensureFresh, so a cron firing while a visitor's
// refresh is already running joins it rather than starting a second one — and
// paying for the same generation twice.
// Hand the registry a payload produced elsewhere. The subreddit generates on
// the cron rather than inside its fetcher, because a visitor must never wait on
// a language model — this is how the result of that work gets served.
export function publish(entry, data) {
  entry.data = data;
  entry.fetchedAt = Date.now();
  entry.lastError = null;
}

export async function forceRefresh(entry) {
  entry.fetchedAt = 0;
  entry.backoffUntil = 0;
  await ensureFresh(entry);
  return entry.lastError;
}

export async function ensureFresh(entry) {
  const now = Date.now();
  if (entry.data !== null && now - entry.fetchedAt < entry.ttl) return;
  if (now < entry.backoffUntil) return;
  if (!entry.refreshing) {
    entry.refreshing = entry
      .fetcher()
      .then((data) => {
        entry.data = data;
        entry.fetchedAt = Date.now();
        entry.lastError = null;
      })
      .catch((error) => {
        entry.backoffUntil = Date.now() + entry.backoffMs;
        entry.lastError = String(error?.message || error);
        console.error(
          `[feed:${entry.name}] refresh failed: ${entry.lastError}`,
        );
      })
      .finally(() => {
        entry.refreshing = null;
      });
  }
  await entry.refreshing;
}

// The response body for one feed: last-good data (marked stale past its ttl),
// or the feed's `empty` shape once last-good is older than staleMs. Always
// stamped so clients can dead-reckon from fetchedAt and detect staleness.
export function feedPayload(entry) {
  const now = Date.now();
  const age = now - entry.fetchedAt;
  const usable = entry.data !== null && age <= entry.staleMs;
  const stale = !usable || age >= entry.ttl + 5000;
  const body = usable ? entry.data : entry.empty;
  return {
    now,
    fetchedAt: entry.fetchedAt,
    stale,
    ...(stale && entry.lastError ? { reason: entry.lastError } : {}),
    ...body,
  };
}

export async function serveFeed(res, entry) {
  await ensureFresh(entry);
  // Feeds are identical for every user → let the CDN serve them: s-maxage tracks
  // the feed's own ttl, SWR bounds worst-case staleness. Browsers still
  // revalidate (max-age=0). Never cache a not-yet-warmed empty response — it
  // would pin emptiness at the edge for the whole window.
  if (entry.data !== null) {
    const ttlS = Math.max(10, Math.round(entry.ttl / 1000));
    const swrS = Math.max(ttlS, Math.round(entry.swrMs / 1000));
    res.setHeader(
      "Cache-Control",
      `public, max-age=0, s-maxage=${ttlS}, stale-while-revalidate=${swrS}`,
    );
  } else {
    res.setHeader("Cache-Control", "no-store");
  }
  res.status(200).json(feedPayload(entry));
}

// One consolidated snapshot of every registered feed, composed purely from the
// per-feed caches (this is why all feeds share one function). A slow upstream
// must not stall the snapshot: each refresh gets a bounded wait, and a feed
// that isn't ready ships its last-good (or empty) state with its own fetchedAt.
export async function serveLive(res, { waitMs = 6000 } = {}) {
  const bounded = (p) =>
    Promise.race([p, new Promise((r) => setTimeout(r, waitMs))]);
  const entries = allFeeds();
  await Promise.all(entries.map((entry) => bounded(ensureFresh(entry))));
  const out = {};
  for (const entry of entries) out[entry.name] = feedPayload(entry);
  res.setHeader(
    "Cache-Control",
    "public, max-age=0, s-maxage=15, stale-while-revalidate=60",
  );
  res.status(200).json({ now: Date.now(), feeds: out });
}
