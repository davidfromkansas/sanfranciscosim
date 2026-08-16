// Bake Muni's GTFS static geometry for the live-bus layer (MUNI-LIVE-PROMPT.md
// Part 2): every motor-coach route's exact street polyline, a trip->shape
// index so a live vehicle's trip_id resolves to the exact alignment it is
// driving, trip headsigns for the card's destination line, and stop
// names/positions for the card's upcoming-stops list.
//
//   node pipeline/muni-shapes.mjs            # uses cached zip if present
//   node pipeline/muni-shapes.mjs --fresh    # re-download GTFS static
//
// Needs a 511 key at BAKE TIME only (MUNI_511_KEY or FERRY_511_KEY in the
// environment, or --key <key>); the runtime never touches GTFS static. Re-run
// when Muni shakes up service — roughly quarterly (watch for the schedule
// change notices); the QA tell is buses visibly diverging from their route
// polylines or a falling trip-match rate in the muni stats line.
//
// Output: app/public/tiles/muni-shapes.bin, committed like the other tiles.
//
// IT MUST STAY IN `npm run all`. This file was silently deleted once already:
// a landmark re-bake branch that predated it regenerated app/public/tiles/
// wholesale, and the merge resolved the absence as a deletion (PR #91). Nothing
// failed loudly — the client just warned "no route shapes" to a console nobody
// was reading and every live bus fell back to dead reckoning in production.
// Being a step of the full bake is what keeps a re-bake branch carrying it.
// GLB-style container: 16-byte header (magic 'MUN1', version, jsonLen,
// floatCount), a JSON chunk, then one Float32Array of [x, z, s] triplets for
// all shapes back to back ('s' = cumulative arc length in metres, what the
// client's follower advances along). The JSON chunk carries:
//
//   routes:    { routeId: { name, directions: { 0: shapeIdx, 1: shapeIdx } } }
//   shapes:    [ { vertexOffset, vertexCount, lengthM } ]
//   tripShape: { tripId: shapeIdx }   ONLY where it differs from the route+
//                                     direction default — most trips ride the
//                                     default, so exceptions stay small
//   tripHeadsign: { tripId: headsignIdx }  interned via `strings`
//   tripDefaults: { "route|dir": headsignIdx } the common headsign, so only
//                                     deviant trips appear in tripHeadsign
//   stops:     { stopId: { nameIdx, x, z } }  stops served by motor-coach trips
//   strings:   [ ... ]                interned headsigns and stop names
//
// Size gate: the JSON chunk plus floats must stay under ~1.2 MB raw (the wire
// is gzipped); the script fails loudly if it balloons past that so bloat is a
// decision, not an accident.

import { execFileSync } from 'node:child_process';
import { existsSync, mkdirSync, readFileSync, writeFileSync, createReadStream } from 'node:fs';
import { createInterface } from 'node:readline';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

import { project } from './lib/geo.mjs';
import { simplify } from './lib/poly.mjs';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const DATA = path.join(HERE, 'data');
const ZIP = path.join(DATA, 'muni-gtfs.zip');
const EXTRACT = path.join(DATA, 'muni-gtfs');
const OUT = path.join(HERE, '../app/public/tiles/muni-shapes.bin');
// The concierge's transit_nearby tool runs inside api/agent.mjs, which cannot
// read app/public — it gets its own copy beside the other bundled indexes.
const OUT_STOPS = path.join(HERE, '../api/_data/muni-stops.json');

const SIMPLIFY_TOLERANCE_M = 3;
const MAX_RAW_BYTES = 1.2 * 1024 * 1024;
const MAGIC = 0x4d554e31; // 'MUN1'

// Same mode table as api/_lib/feeds/muni.mjs — keep the two in sync by hand;
// they are two runtimes with no shared import path (functions vs pipeline).
// Cable route_ids verified against the live feed 2026-08-12: PM, PH, CA.
const RAIL_OR_CABLE = new Set(['J', 'K', 'L', 'M', 'N', 'T', 'F', 'E', 'PM', 'PH', 'CA', '59', '60', '61']);
const TROLLEY_NUMBERS = new Set([
  '1', '2', '3', '5', '6', '7', '14', '21', '22', '24', '30', '31', '33', '41', '45', '49',
]);

// A rider calls both of these "the bus": motor coaches and trolley coaches look
// alike, stop at the same kind of stop, and between them are the whole surface
// bus network. Rail and cable are excluded — they have platforms, not bus stops.
function isBusRoute(routeId) {
  const id = String(routeId).toUpperCase();
  return !RAIL_OR_CABLE.has(id);
}

// All Muni routes get shapes baked — motor coaches, trolley coaches, LRV,
// streetcar, and cable car. The mode split is resolved at runtime from the
// route_id (same table as api/_lib/feeds/muni.mjs); the bake just needs to
// include every route's shape so the client can snap any vehicle to its
// alignment. Previously only motor coaches were baked, leaving trolleys,
// LRVs, streetcars, and cable cars to dead-reckon in straight lines through
// buildings.
function isMuniRoute(routeId) {
  return Boolean(routeId);
}

// ------------------------------------------------------------------ download

async function download(key) {
  mkdirSync(DATA, { recursive: true });
  const url = `https://api.511.org/transit/datafeeds?operator_id=SF&api_key=${encodeURIComponent(key)}`;
  console.log('[muni-shapes] downloading GTFS static…');
  const res = await fetch(url);
  if (!res.ok) throw new Error(`datafeeds HTTP ${res.status}`);
  writeFileSync(ZIP, Buffer.from(await res.arrayBuffer()));
  console.log(`[muni-shapes] ${ZIP} (${(readFileSync(ZIP).length / 1e6).toFixed(1)} MB)`);
}

function extract() {
  mkdirSync(EXTRACT, { recursive: true });
  // macOS/Linux system unzip; the pipeline already assumes a POSIX toolchain.
  execFileSync('unzip', ['-o', '-q', ZIP, '-d', EXTRACT]);
}

// ------------------------------------------------------------------ csv

// Minimal RFC-4180 line splitter (GTFS uses quoted fields with commas).
function splitCsv(line) {
  const out = [];
  let field = '';
  let quoted = false;
  for (let i = 0; i < line.length; i++) {
    const c = line[i];
    if (quoted) {
      if (c === '"' && line[i + 1] === '"') {
        field += '"';
        i++;
      } else if (c === '"') quoted = false;
      else field += c;
    } else if (c === '"') quoted = true;
    else if (c === ',') {
      out.push(field);
      field = '';
    } else field += c;
  }
  out.push(field);
  return out;
}

async function eachRow(file, fn) {
  const rl = createInterface({ input: createReadStream(path.join(EXTRACT, file)), crlfDelay: Infinity });
  let header = null;
  for await (const raw of rl) {
    const line = raw.replace(/^﻿/, '');
    if (!line) continue;
    const cols = splitCsv(line);
    if (!header) {
      header = Object.fromEntries(cols.map((name, i) => [name.trim(), i]));
      continue;
    }
    fn(cols, header);
  }
}

// ------------------------------------------------------------------ bake

async function main() {
  const argv = process.argv.slice(2);
  const key =
    (argv.includes('--key') ? argv[argv.indexOf('--key') + 1] : null) ||
    (process.env.MUNI_511_KEY || '').trim() ||
    (process.env.FERRY_511_KEY || '').trim();

  if (argv.includes('--fresh') || !existsSync(ZIP)) {
    if (!key) {
      // Part of `npm run all`, which must not fail for want of an optional key.
      // The committed .bin is the shipped artifact; leaving it untouched is the
      // right outcome here, not an error.
      console.warn(
        '[muni-shapes] no 511 key and no cached GTFS zip — leaving the committed ' +
          'app/public/tiles/muni-shapes.bin as is. Set MUNI_511_KEY to re-bake.',
      );
      return;
    }
    await download(key);
  } else {
    console.log('[muni-shapes] using cached zip (pass --fresh to re-download)');
  }
  extract();

  // routes.txt: all Muni route ids + display names (motor coach, trolley,
  // LRV, streetcar, cable car — every route in the SF agency feed).
  const routes = new Map(); // routeId -> { name }
  await eachRow('routes.txt', (cols, h) => {
    const id = cols[h.route_id];
    if (!isMuniRoute(id)) return;
    routes.set(id, { name: cols[h.route_long_name] || cols[h.route_short_name] || id });
  });
  console.log(`[muni-shapes] Muni routes: ${routes.size}`);

  // trips.txt: shape usage, headsigns.
  const shapeUse = new Map(); // shapeId -> count
  const trips = new Map(); // tripId -> { routeId, dir, shapeId, headsign }
  await eachRow('trips.txt', (cols, h) => {
    const routeId = cols[h.route_id];
    if (!routes.has(routeId)) return;
    const tripId = cols[h.trip_id];
    const shapeId = cols[h.shape_id];
    if (!tripId || !shapeId) return;
    trips.set(tripId, {
      routeId,
      dir: Number(cols[h.direction_id] || 0),
      shapeId,
      headsign: (cols[h.trip_headsign] || '').trim(),
    });
    shapeUse.set(shapeId, (shapeUse.get(shapeId) || 0) + 1);
  });
  console.log(`[muni-shapes] Muni trips: ${trips.size}, shapes used: ${shapeUse.size}`);

  // shapes.txt: project + simplify + arc length, only for used shapes.
  const rawShapes = new Map(); // shapeId -> [[x, z], ...] in sequence order
  await eachRow('shapes.txt', (cols, h) => {
    const id = cols[h.shape_id];
    if (!shapeUse.has(id)) return;
    const seq = Number(cols[h.shape_pt_sequence]);
    const [x, z] = project(Number(cols[h.shape_pt_lon]), Number(cols[h.shape_pt_lat]));
    let arr = rawShapes.get(id);
    if (!arr) rawShapes.set(id, (arr = []));
    arr.push([seq, x, z]);
  });

  const shapeIndex = new Map(); // shapeId -> idx
  const shapeMeta = [];
  const floats = [];
  // Subdivide any segment longer than this so vehicles can snap and walls
  // can follow terrain. The GTFS shapes have long straight jumps (up to 3.5km)
  // that leave no intermediate points for projection — 1299 segments over 500m
  // in the original bake. 100m is fine enough for snapping and terrain without
  // bloating the file.
  const SUBDIVIDE_M = 100;
  for (const [id, pts] of rawShapes) {
    pts.sort((a, b) => a[0] - b[0]);
    const flat = [];
    for (const [, x, z] of pts) flat.push(x, z);
    const slim = simplify(flat, SIMPLIFY_TOLERANCE_M);
    // Subdivide long segments: insert interpolated points every SUBDIVIDE_M.
    const sub = [];
    for (let i = 0; i < slim.length; i += 2) {
      if (i > 0) {
        const px = slim[i - 2], pz = slim[i - 1];
        const cx = slim[i], cz = slim[i + 1];
        const segLen = Math.hypot(cx - px, cz - pz);
        if (segLen > SUBDIVIDE_M) {
          const steps = Math.ceil(segLen / SUBDIVIDE_M);
          for (let j = 1; j < steps; j++) {
            const t = j / steps;
            sub.push(px + (cx - px) * t, pz + (cz - pz) * t);
          }
        }
      }
      sub.push(slim[i], slim[i + 1]);
    }
    const vertexOffset = floats.length / 3;
    let s = 0;
    for (let i = 0; i < sub.length; i += 2) {
      if (i > 0) s += Math.hypot(sub[i] - sub[i - 2], sub[i + 1] - sub[i - 1]);
      floats.push(sub[i], sub[i + 1], s);
    }
    shapeIndex.set(id, shapeMeta.length);
    shapeMeta.push({ vertexOffset, vertexCount: sub.length / 2, lengthM: Math.round(s) });
  }

  // Per route+direction: the most-used shape is the default; trips on any
  // other shape become explicit exceptions. Same trick for headsigns.
  const strings = [];
  const stringIdx = new Map();
  const intern = (text) => {
    if (!stringIdx.has(text)) {
      stringIdx.set(text, strings.length);
      strings.push(text);
    }
    return stringIdx.get(text);
  };

  const byRouteDir = new Map(); // "route|dir" -> Map(shapeId -> n) / headsign tally
  for (const t of trips.values()) {
    const k = `${t.routeId}|${t.dir}`;
    let e = byRouteDir.get(k);
    if (!e) byRouteDir.set(k, (e = { shapes: new Map(), signs: new Map() }));
    e.shapes.set(t.shapeId, (e.shapes.get(t.shapeId) || 0) + 1);
    if (t.headsign) e.signs.set(t.headsign, (e.signs.get(t.headsign) || 0) + 1);
  }
  const top = (m) => [...m.entries()].sort((a, b) => b[1] - a[1])[0]?.[0];

  const routesOut = {};
  const tripDefaults = {};
  for (const [routeId, r] of routes) {
    const directions = {};
    for (const dir of [0, 1]) {
      const e = byRouteDir.get(`${routeId}|${dir}`);
      if (!e) continue;
      directions[dir] = shapeIndex.get(top(e.shapes));
      const sign = top(e.signs);
      if (sign) tripDefaults[`${routeId}|${dir}`] = intern(sign);
    }
    routesOut[routeId] = { name: r.name, directions };
  }
  // Build route -> all shape indices map. The direction default is just the
  // most-used shape, but a route can have many variant shapes. The client uses
  // this to try all shapes for a route when the default is too far from the
  // vehicle's GPS position — without it, vehicles on variant shapes can't snap.
  const routeShapes = {};
  for (const [routeId, r] of routes) {
    const shapes = new Set();
    for (const dir of [0, 1]) {
      const e = byRouteDir.get(`${routeId}|${dir}`);
      if (!e) continue;
      for (const shapeId of e.shapes.keys()) {
        const idx = shapeIndex.get(shapeId);
        if (idx !== undefined) shapes.add(idx);
      }
    }
    if (shapes.size > 0) routeShapes[routeId] = [...shapes];
  }
  const tripShape = {};
  const tripHeadsign = {};
  for (const [tripId, t] of trips) {
    const defShape = routesOut[t.routeId]?.directions?.[t.dir];
    const idx = shapeIndex.get(t.shapeId);
    if (idx !== defShape) tripShape[tripId] = idx;
    if (t.headsign && intern(t.headsign) !== tripDefaults[`${t.routeId}|${t.dir}`]) {
      tripHeadsign[tripId] = intern(t.headsign);
    }
  }
  console.log(
    `[muni-shapes] trip exceptions: shape ${Object.keys(tripShape).length}/${trips.size}, ` +
      `headsign ${Object.keys(tripHeadsign).length}/${trips.size}`,
  );

  // Every BUS trip (motor coach + trolley coach), for the stop layer. The shape
  // machinery above now covers all Muni routes (motor coach, trolley, LRV,
  // streetcar, cable car) for vehicle movement; the stop layer stays bus-only
  // since rail and cable have platforms, not bus stops.
  const busTrips = new Map(); // tripId -> routeId
  const busRouteNames = new Map(); // routeId -> display name
  await eachRow('routes.txt', (cols, h) => {
    const id = cols[h.route_id];
    if (!isBusRoute(id)) return;
    busRouteNames.set(id, cols[h.route_long_name] || cols[h.route_short_name] || id);
  });
  await eachRow('trips.txt', (cols, h) => {
    const routeId = cols[h.route_id];
    if (busRouteNames.has(routeId)) busTrips.set(cols[h.trip_id], routeId);
  });
  console.log(`[muni-shapes] bus routes (motor + trolley): ${busRouteNames.size}`);

  // stop_times.txt is the big one (~1M rows): stream it once, recording the stops
  // motor-coach trips serve (the bus card's "next stops"), every stop with any
  // service (the concierge), and — the new part — which BUS ROUTES serve each
  // stop, which is what "which buses stop here" is answered from.
  const wantedStops = new Set();
  const servedStops = new Set();
  const stopRoutes = new Map(); // stopId -> Set(routeId)
  await eachRow('stop_times.txt', (cols, h) => {
    const stopId = cols[h.stop_id];
    servedStops.add(stopId);
    const tripId = cols[h.trip_id];
    if (trips.has(tripId)) wantedStops.add(stopId);
    const busRoute = busTrips.get(tripId);
    if (busRoute) {
      let set = stopRoutes.get(stopId);
      if (!set) stopRoutes.set(stopId, (set = new Set()));
      set.add(busRoute);
    }
  });
  console.log(`[muni-shapes] stops served by a bus route: ${stopRoutes.size}`);
  // Route ids are interned into a flat list so a stop's routes cost one small
  // integer each instead of repeating "38R" a few thousand times.
  const busRouteList = [...busRouteNames.keys()].sort();
  const busRouteIdx = new Map(busRouteList.map((id, i) => [id, i]));

  const stops = {};
  const allStops = {};
  const busStops = {};
  await eachRow('stops.txt', (cols, h) => {
    const id = cols[h.stop_id];
    if (!servedStops.has(id)) return;
    const [x, z] = project(Number(cols[h.stop_lon]), Number(cols[h.stop_lat]));
    const name = cols[h.stop_name] || id;
    const routes = stopRoutes.get(id);
    // [name, x, z, routeIdx...] as a tuple, not an object: 3,500 stops of
    // {"name":...} keys is a megabyte of repeated property names.
    allStops[id] = [name, Math.round(x), Math.round(z),
                    ...[...(routes || [])].map((r) => busRouteIdx.get(r)).filter((i) => i !== undefined)];
    if (wantedStops.has(id)) {
      stops[id] = { nameIdx: intern(name), x: +x.toFixed(1), z: +z.toFixed(1) };
    }
    // THE BUS-STOP LAYER: only stops a bus actually calls at. This is what puts
    // a shelter on the ground, so it must never include a rail-only platform.
    if (routes && routes.size) {
      busStops[id] = [
        intern(name),
        Math.round(x * 10) / 10,
        Math.round(z * 10) / 10,
        [...routes].map((r) => busRouteIdx.get(r)).sort((a, b) => a - b),
      ];
    }
  });
  console.log(`[muni-shapes] BUS STOPS (shelter sites): ${Object.keys(busStops).length}`);
  console.log(`[muni-shapes] stops kept: ${Object.keys(stops).length}, strings: ${strings.length}`);

  // ------------------------------------------------------------- serialise
  const jsonRaw = Buffer.from(
    JSON.stringify({
      generated: new Date().toISOString(),
      routes: routesOut,
      routeShapes,
      shapes: shapeMeta,
      tripShape,
      tripHeadsign,
      tripDefaults,
      stops,
      busStops,
      busRoutes: busRouteList,
      busRouteNames: busRouteList.map((id) => intern(busRouteNames.get(id))),
      strings,
    }),
  );
  // Pad the JSON chunk to a 4-byte boundary (GLB does the same): the client
  // builds a Float32Array VIEW at 16 + jsonLen, and a typed-array view whose
  // byteOffset is not a multiple of 4 throws. Without this the format works or
  // fails depending on how long the JSON happens to be.
  const pad = (4 - ((16 + jsonRaw.length) % 4)) % 4;
  const json = Buffer.concat([jsonRaw, Buffer.alloc(pad, 0x20)]);

  const header = Buffer.alloc(16);
  header.writeUInt32LE(MAGIC, 0);
  header.writeUInt32LE(1, 4);
  header.writeUInt32LE(json.length, 8);
  header.writeUInt32LE(floats.length, 12);
  const blob = Buffer.concat([header, json, Buffer.from(new Float32Array(floats).buffer)]);

  if (blob.length > MAX_RAW_BYTES) {
    throw new Error(
      `muni-shapes.bin is ${(blob.length / 1e6).toFixed(2)} MB > budget — trim before shipping ` +
        `(json ${(json.length / 1e6).toFixed(2)} MB, floats ${((floats.length * 4) / 1e6).toFixed(2)} MB)`,
    );
  }
  writeFileSync(OUT, blob);
  mkdirSync(path.dirname(OUT_STOPS), { recursive: true });
  writeFileSync(
    OUT_STOPS,
    JSON.stringify({
      generated: new Date().toISOString(),
      // Entries are [name, x, z, ...routeIdx] — routeIdx indexes `busRoutes`.
      busRoutes: busRouteList,
      stops: allStops,
    }),
  );
  console.log(
    `[muni-shapes] wrote ${OUT_STOPS}: ${Object.keys(allStops).length} stops, ` +
      `${(readFileSync(OUT_STOPS).length / 1024).toFixed(0)} KB`,
  );
  console.log(
    `[muni-shapes] wrote ${OUT}: ${(blob.length / 1024).toFixed(0)} KB ` +
      `(json ${(json.length / 1024).toFixed(0)} KB + ${shapeMeta.length} shapes, ${floats.length / 3} vertices)`,
  );
}

main().catch((error) => {
  console.error(`[muni-shapes] FAILED: ${error.message}`);
  process.exit(1);
});
