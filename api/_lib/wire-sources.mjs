// The wire's non-newsroom tiers: earthquakes, transit alerts, weather, city
// records, and what the city's own residents are talking about online.
//
// Everything here returns the same shape the news fetcher does — title, link,
// published, source — plus two fields the newsroom items lack: a PRIORITY, so
// a quake outranks a stop closure which outranks a Reddit thread, and for the
// structured tiers a finished BODY, because a fact assembled from a dataset
// needs no model call to compress and must not pass through one that could
// embellish it.
//
// Every gatherer fails to an empty list. One dead API must never take the
// others down, and the wire itself falls back to plain news.

import { getFeed, ensureFresh } from "./feedcore.mjs";

const day = (ms = Date.now()) => new Date(ms).toISOString().slice(0, 10);

// ------------------------------------------------------------------ quakes
//
// USGS, no key. The one event category that outranks everything: even a small
// shake is instantly the only thing the city is talking about.
const SF = { lon: -122.4194, lat: 37.7749 };
const QUAKE_RADIUS_KM = 120;
const QUAKE_MIN_MAG = 2.5;

async function quakes() {
  const res = await fetch(
    "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_day.geojson",
  );
  if (!res.ok) return [];
  const d = await res.json();
  return (d.features ?? [])
    .filter((f) => {
      const [lon, lat] = f.geometry?.coordinates ?? [0, 0];
      const km = Math.hypot((lon - SF.lon) * 88, (lat - SF.lat) * 111);
      return km < QUAKE_RADIUS_KM && (f.properties?.mag ?? 0) >= QUAKE_MIN_MAG;
    })
    .map((f) => {
      const p = f.properties;
      const mag = p.mag.toFixed(1);
      const when = new Date(p.time).toLocaleTimeString("en-US", {
        hour: "numeric",
        minute: "2-digit",
        timeZone: "America/Los_Angeles",
      });
      return {
        kind: "quake",
        priority: 0,
        title: `Magnitude ${mag} earthquake ${p.place}`,
        body: `USGS reports a M${mag} quake ${p.place} at ${when}. Depth ${Math.round(f.geometry.coordinates[2])} km.`,
        link: p.url,
        published: p.time,
        source: "USGS",
      };
    });
}

// ----------------------------------------------------------- transit alerts
//
// 511.org, the key the Muni feed already uses. Most alerts are routine stop
// moves; the filter keeps the ones a rider would actually tell somebody about.
// Stop-level notices are the least interesting true things the city says —
// "board on the far side of the street" is not a conversation. Only alerts
// about SERVICE make the wire: lines not running, reroutes, subway problems.
const ALERT_WORDS = /delay|reroute|re-route|suspend|no service|not running|subway|shuttle|major|switch back/i;

async function transitAlerts() {
  const key = process.env.MUNI_511_KEY || process.env.FERRY_511_KEY;
  if (!key) return [];
  const res = await fetch(
    `https://api.511.org/transit/servicealerts?api_key=${key}&agency=SF&format=json`,
  );
  if (!res.ok) return [];
  const text = (await res.text()).replace(/^﻿/, "");
  const d = JSON.parse(text);
  const out = [];
  for (const e of d.Entities ?? []) {
    const a = e.Alert ?? {};
    const pick = (field) =>
      (a[field]?.Translations ?? a[field]?.Translation ?? [])[0]?.Text ?? "";
    const header = pick("HeaderText").trim();
    const detail = pick("DescriptionText").trim();
    if (!header || !ALERT_WORDS.test(`${header} ${detail}`)) continue;
    out.push({
      kind: "transit",
      // Below the newsrooms (4), not above them. A service alert is worth one
      // post, but a morning where the wire reads like an SFMTA changelog is a
      // failure — reporting beats notices whenever both are on offer.
      priority: 4.5,
      title: `Muni alert: ${header.slice(0, 100)}`,
      body: (detail || header).slice(0, 200),
      // 511 alerts carry no public URL; SFMTA's alert page is where a rider
      // would go to see the same thing.
      link: `https://www.sfmta.com/alerts#${e.Id ?? header.slice(0, 40)}`,
      published: (a.ActivePeriods?.[0]?.Start ?? 0) * 1000 || Date.now(),
      source: "SFMTA via 511",
    });
  }
  return out.slice(0, 3);
}

// ----------------------------------------------------------------- weather
//
// The simulation's own telemetry — the same feed that drives the sky. No
// memory of yesterday is kept; instead each condition can fire at most once
// per day, which is what the date in the link key is for.
async function weatherEvents() {
  const entry = getFeed("weather");
  if (!entry) return [];
  try {
    await ensureFresh(entry);
  } catch {
    return [];
  }
  const s = entry.data?.summary;
  if (!s) return [];
  const out = [];
  const today = day();
  const add = (slug, title, body) =>
    out.push({
      kind: "weather",
      priority: 2,
      title,
      body,
      link: `sfsim://weather/${slug}/${today}`,
      published: Date.now(),
      source: "SF Sim weather grid",
    });
  if (s.visibility != null && s.visibility < 6000)
    add(
      "fog",
      "Dense fog across the city this morning",
      `Citywide visibility is averaging about ${Math.round(s.visibility / 100) * 100} metres on the simulation's weather grid. The west side will feel it most.`,
    );
  if ((s.precip ?? 0) >= 0.5)
    add(
      "rain",
      "Rain moving through San Francisco",
      `The city's weather grid is measuring steady rain — about ${s.precip} mm in the last hour — with ${s.label?.toLowerCase() ?? "wet"} conditions citywide.`,
    );
  if ((s.temp ?? 0) >= 85)
    add(
      "heat",
      `San Francisco hits ${Math.round(s.temp)}°F`,
      `A hot one by this city's standards: the grid is averaging ${Math.round(s.temp)}°F with ${s.humidity ?? "?"}% humidity.`,
    );
  if ((s.windSpeed ?? 0) >= 30)
    add(
      "wind",
      "High winds across the city",
      `Sustained winds around ${Math.round(s.windSpeed)} mph on the city grid. Hold onto your hat on the hills.`,
    );
  return out;
}

// ------------------------------------------------------------------ DataSF
//
// City records, straight from Socrata — the datasets and thresholds ported
// from the personas project's event pipeline. Only low-volume signals a
// resident would genuinely notice: a cluster of eviction filings, a run of
// business closures. High-volume feeds (311, police) need baselines to mean
// anything and stay out until they earn their place.
// DataSF is OFF for launch. Eviction clusters and closure runs qualify
// CONTINUOUSLY — the same five filings stay newsworthy for ten days, unlike a
// news item which is consumed once — so at priority 3.5 they outranked every
// newsroom and the wire posted two eviction notices inside twenty minutes of
// going live. Reporting is what this is meant to surface first.
//
// The gatherers below are kept whole and still tested. Before they come back
// they need a rate rule of their own — at most one city-record post an hour —
// because the priority system alone cannot express "important but repetitive".
const DATASF = false;

const SODA = "https://data.sfgov.org/resource";
const iso = (ms) => new Date(ms).toISOString().slice(0, 10);
const weekKey = () => {
  const d = new Date();
  return `${d.getUTCFullYear()}w${Math.ceil((d.getUTCDate() + new Date(Date.UTC(d.getUTCFullYear(), d.getUTCMonth(), 1)).getUTCDay()) / 7)}m${d.getUTCMonth()}`;
};

async function soda(dataset, params) {
  const url = `${SODA}/${dataset}.json?${new URLSearchParams(params)}`;
  const res = await fetch(url, { headers: { Accept: "application/json" } });
  if (!res.ok) return [];
  return res.json();
}

async function evictionClusters() {
  const rows = await soda("5cei-gny5", {
    $where: `file_date > '${iso(Date.now() - 10 * 86400_000)}'`,
    $select: "eviction_id,neighborhood,file_date",
    $limit: "500",
  });
  const by = new Map();
  for (const r of rows) {
    const n = r.neighborhood;
    if (n) by.set(n, (by.get(n) ?? 0) + 1);
  }
  const out = [];
  for (const [place, n] of by) {
    if (n < 3) continue;
    out.push({
      kind: "evictions",
      priority: 3.5,
      title: `${n} eviction notices filed in ${place} over the past ten days`,
      body: `City records show ${n} eviction filings in ${place} since ${iso(Date.now() - 10 * 86400_000)}. Each filing is a household served notice, not yet an eviction.`,
      link: `https://data.sfgov.org/Housing-and-Buildings/Eviction-Notices/5cei-gny5#${place}-${weekKey()}`,
      published: Date.now(),
      source: "DataSF eviction notices",
    });
  }
  return out.slice(0, 2);
}

async function businessClosures() {
  const rows = await soda("g8m3-pdis", {
    $where: `location_end_date > '${iso(Date.now() - 10 * 86400_000)}'`,
    $select: "dba_name,neighborhoods_analysis_boundaries,location_end_date",
    $limit: "500",
  });
  const by = new Map();
  for (const r of rows) {
    const n = r.neighborhoods_analysis_boundaries;
    if (!n || !r.dba_name) continue;
    (by.get(n) ?? by.set(n, []).get(n)).push(r.dba_name);
  }
  const out = [];
  for (const [place, names] of by) {
    if (names.length < 3) continue;
    const shown = names.slice(0, 3).join(", ");
    out.push({
      kind: "closures",
      priority: 3.5,
      title: `${names.length} businesses closed their ${place} locations this week`,
      body: `City registrations ended for ${shown}${names.length > 3 ? ` and ${names.length - 3} more` : ""} in ${place} over the past ten days.`,
      link: `https://data.sfgov.org/Economy-and-Community/Registered-Business-Locations-San-Francisco/g8m3-pdis#${place}-${weekKey()}`,
      published: Date.now(),
      source: "DataSF business registrations",
    });
  }
  return out.slice(0, 2);
}

// ------------------------------------------------------------------ reddit
//
// What the real city is talking about, as TOPICS. The title is the poster's
// own and the link goes to their thread — the same verbatim-plus-credit rule
// the newsrooms get. Lowest priority: it is conversation about the city, not
// something that happened in it.
async function redditTopics() {
  const res = await fetch(
    "https://www.reddit.com/r/sanfrancisco/top/.rss?t=day&limit=10",
    { headers: { "User-Agent": "sanfranciscosim/1.0 (+https://www.sfsim.net)" } },
  );
  if (!res.ok) return [];
  const xml = await res.text();
  const out = [];
  for (const block of xml.split(/<entry[\s>]/).slice(1)) {
    const title = block.match(/<title>([\s\S]*?)<\/title>/)?.[1]?.trim() ?? "";
    const link = block.match(/<link[^>]*href="([^"]+)"/)?.[1] ?? "";
    const published = Date.parse(block.match(/<published>([^<]+)</)?.[1] ?? "") || 0;
    if (!title || !link) continue;
    out.push({
      kind: "reddit",
      priority: 5,
      title: title.replace(/&amp;/g, "&").replace(/&#39;|&apos;/g, "'").replace(/&quot;/g, '"').slice(0, 120),
      description: "",
      link: link.split("?")[0],
      published,
      source: "r/sanfrancisco",
    });
  }
  return out.slice(0, 2);
}

// One list, best first. Priority beats recency: a quake from forty minutes ago
// outranks a Reddit thread from four.
export async function gatherWire() {
  const tiers = await Promise.all([
    quakes().catch(() => []),
    transitAlerts().catch(() => []),
    weatherEvents().catch(() => []),
    ...(DATASF ? [evictionClusters().catch(() => []), businessClosures().catch(() => [])] : []),
    redditTopics().catch(() => []),
  ]);
  return tiers.flat().sort((a, b) => a.priority - b.priority || b.published - a.published);
}
