// The live-feed dispatcher: every /api/<feed> route not claimed by a real file
// (agent.mjs stays its own function) lands here and is served from the feed
// registry. All feeds deliberately share this ONE function so their caches live
// in one process — that is what lets /api/live compose a consolidated snapshot
// from memory instead of HTTP-calling the city's own endpoints.
//
// Adding a feed touches only api/_lib/feeds/ — see the recipe in feedcore.mjs.

import { getFeed, serveFeed, serveLive } from './_lib/feedcore.mjs';
import './_lib/feeds/index.mjs';

export default async function handler(req, res) {
  if (req.method && req.method !== 'GET') {
    res.status(405).json({ error: 'method not allowed' });
    return;
  }
  const pathname = new URL(req.url, 'http://localhost').pathname.replace(/\/+$/, '');

  if (pathname === '/api/live') {
    await serveLive(res);
    return;
  }
  const entry = getFeed(pathname.replace(/^\/api\//, ''));
  if (entry) {
    await serveFeed(res, entry);
    return;
  }
  res.status(404).json({ error: 'unknown endpoint' });
}
