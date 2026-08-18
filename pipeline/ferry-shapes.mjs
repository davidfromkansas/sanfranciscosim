// Bake San Francisco Bay Ferry (WETA) GTFS static geometry for the live-ferry
// layer: every route's navigational polyline across the Bay, the terminals
// boats actually call at, and each route's official livery colour.
//
//   node pipeline/ferry-shapes.mjs            # uses cached zip if present
//   node pipeline/ferry-shapes.mjs --fresh    # re-download GTFS static
//
// Needs a 511 key at BAKE TIME only (FERRY_511_KEY or MUNI_511_KEY in the
// environment, or --key <key>); the runtime never touches GTFS static. Re-run
// when SF Bay Ferry changes service — they publish seasonal schedules, so
// roughly quarterly.
//
// Output: app/public/tiles/ferry-shapes.bin (committed like the other tiles)
// and api/_data/ferry-stops.json (the concierge runs in api/ and cannot read
// app/public).
//
// IT MUST STAY IN `npm run all`. pipeline/muni-shapes.mjs documents being
// silently deleted once by a landmark re-bake that regenerated
// app/public/tiles/ wholesale; nothing failed loudly, and every live bus fell
// back to dead reckoning in production for days. Being a step of the full bake
// is what keeps a re-bake branch carrying it.
//
// Container (same idiom as muni-shapes.bin): 16-byte header (magic 'FRY1',
// version, jsonLen, floatCount), a JSON chunk padded to a 4-byte boundary, then
// one Float32Array of [x, z, s] triplets for all shapes back to back ('s' =
// cumulative arc length in metres). The JSON chunk carries:
//
//   routes:    { routeId: { name, color, textColor, shapes: [shapeIdx] } }
//   shapes:    [ { vertexOffset, vertexCount, lengthM } ]
//   terminals: [ { id, name, x, z, parent, routes: [routeId] } ]
//
// Unlike the Muni bake, nothing here is interned or tuple-packed: this feed has
// 7 routes and 15 terminals, so the whole JSON chunk is a couple of kilobytes
// and clarity is worth more than the bytes.

import { execFileSync } from 'node:child_process';
import { existsSync, mkdirSync, readFileSync, writeFileSync, createReadStream } from 'node:fs';
import { createInterface } from 'node:readline';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

import { project } from './lib/geo.mjs';
import { simplify } from './lib/poly.mjs';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const DATA = path.join(HERE, 'data');
const zipFor = (op) => path.join(DATA, `ferry-gtfs-${op}.zip`);
const extractFor = (op) => path.join(DATA, `ferry-gtfs-${op}`);
const OUT = path.join(HERE, '../app/public/tiles/ferry-shapes.bin');
const OUT_STOPS = path.join(HERE, '../api/_data/ferry-stops.json');

// Written and read as UInt32LE, same convention as muni-shapes.bin's 'MUN1'.
const MAGIC = 0x46525931; // 'FRY1'
// ALL FOUR of 511's ferry operators, not just WETA. Baking SB alone left the
// Sausalito, Tiburon, Larkspur, Angel Island and Treasure Island crossings
// missing from a map of the Bay, which is exactly the sort of hole the "data
// accuracy is the product" rule exists to prevent.
//
// Only SB publishes live vessel positions (measured: GF, AF and TF all return
// zero vehicles from SIRI VehicleMonitoring at a weekday commute hour, when
// Golden Gate's Sausalito boats are certainly running). So the other three
// contribute route walls and terminals but never a moving hull — which is
// honest: we can say where the crossing goes without claiming to know where the
// boat is.
const OPERATORS = [
  { id: 'SB', name: 'San Francisco Bay Ferry', live: true },
  { id: 'GF', name: 'Golden Gate Ferry', live: false },
  { id: 'AF', name: 'Angel Island Tiburon Ferry', live: false },
  { id: 'TF', name: 'Treasure Island Ferry', live: false },
];
// Open water, so unlike the Muni bake there is no terrain to follow and no
// street to sit on — the shapes only need to be smooth enough to draw.
const SIMPLIFY_TOLERANCE_M = 15;
// The published shapes have segments up to ~700 m. Subdividing lets the route
// walls curve and lets a vessel snap along an alignment; 250 m over ~640 km of
// route is a few thousand vertices, which is nothing.
const SUBDIVIDE_M = 250;
// This feed is tiny. If it ever balloons past this, something is wrong.
const MAX_RAW_BYTES = 400 * 1024;

// ------------------------------------------------------------------ download

async function download(key, op) {
  mkdirSync(DATA, { recursive: true });
  const url = `https://api.511.org/transit/datafeeds?operator_id=${op}&api_key=${encodeURIComponent(key)}`;
  console.log(`[ferry-shapes] ${op}: downloading GTFS static…`);
  const res = await fetch(url);
  if (!res.ok) throw new Error(`${op} datafeeds HTTP ${res.status}`);
  writeFileSync(zipFor(op), Buffer.from(await res.arrayBuffer()));
}

function extract(op) {
  mkdirSync(extractFor(op), { recursive: true });
  execFileSync('unzip', ['-o', '-q', zipFor(op), '-d', extractFor(op)]);
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

async function eachRow(op, file, fn) {
  const full = path.join(extractFor(op), file);
  if (!existsSync(full)) return;
  const rl = createInterface({ input: createReadStream(full), crlfDelay: Infinity });
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

const hex = (value) => {
  const v = (value || '').trim().replace(/^#/, '');
  return /^[0-9a-fA-F]{6}$/.test(v) ? `#${v.toLowerCase()}` : null;
};

// ------------------------------------------------------------------ bake

async function main() {
  const argv = process.argv.slice(2);
  const key =
    (argv.includes('--key') ? argv[argv.indexOf('--key') + 1] : null) ||
    (process.env.FERRY_511_KEY || '').trim() ||
    (process.env.MUNI_511_KEY || '').trim();

  const cached = OPERATORS.every((op) => existsSync(zipFor(op.id)));
  if (argv.includes('--fresh') || !cached) {
    if (!key) {
      // Part of `npm run all`, which must not fail for want of an optional key.
      // The committed .bin is the shipped artifact; leaving it alone is correct.
      console.warn(
        '[ferry-shapes] no 511 key and no cached GTFS zips — leaving the committed ' +
          'app/public/tiles/ferry-shapes.bin as is. Set FERRY_511_KEY to re-bake.',
      );
      return;
    }
    for (const op of OPERATORS) await download(key, op.id);
  } else {
    console.log('[ferry-shapes] using cached zips (pass --fresh to re-download)');
  }

  // Everything is namespaced by operator: SB stop 7201 and a GF stop could
  // otherwise collide, and four agencies serve the same Ferry Building.
  const routesOut = {};
  const shapeMeta = [];
  const floats = [];
  const terminals = [];

  for (const op of OPERATORS) {
    extract(op.id);

    const routes = new Map(); // raw routeId -> { name, color, textColor }
    await eachRow(op.id, 'routes.txt', (cols, h) => {
      const id = cols[h.route_id];
      if (!id) return;
      routes.set(id, {
        name: cols[h.route_long_name] || cols[h.route_short_name] || id,
        color: hex(cols[h.route_color]),
        textColor: hex(cols[h.route_text_color]),
      });
    });

    const trips = new Map(); // tripId -> { routeId, shapeId }
    const shapeUse = new Map(); // shapeId -> raw routeId
    await eachRow(op.id, 'trips.txt', (cols, h) => {
      const routeId = cols[h.route_id];
      const tripId = cols[h.trip_id];
      const shapeId = cols[h.shape_id];
      if (!routes.has(routeId) || !tripId) return;
      trips.set(tripId, { routeId, shapeId: shapeId || null });
      if (shapeId) shapeUse.set(shapeId, routeId);
    });

    const rawShapes = new Map(); // shapeId -> [[seq, x, z], ...]
    await eachRow(op.id, 'shapes.txt', (cols, h) => {
      const id = cols[h.shape_id];
      if (!shapeUse.has(id)) return;
      const [x, z] = project(Number(cols[h.shape_pt_lon]), Number(cols[h.shape_pt_lat]));
      let arr = rawShapes.get(id);
      if (!arr) rawShapes.set(id, (arr = []));
      arr.push([Number(cols[h.shape_pt_sequence]), x, z]);
    });

    const shapeIndex = new Map(); // shapeId -> index into the GLOBAL shapeMeta
    for (const [id, pts] of rawShapes) {
      pts.sort((a, b) => a[0] - b[0]);
      const flat = [];
      for (const [, x, z] of pts) flat.push(x, z);
      const slim = simplify(flat, SIMPLIFY_TOLERANCE_M);
      const sub = [];
      for (let i = 0; i < slim.length; i += 2) {
        if (i > 0) {
          const px = slim[i - 2];
          const pz = slim[i - 1];
          const cx = slim[i];
          const cz = slim[i + 1];
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
      if (sub.length < 4) continue; // a one-point "shape" draws nothing
      const vertexOffset = floats.length / 3;
      let arc = 0;
      for (let i = 0; i < sub.length; i += 2) {
        if (i > 0) arc += Math.hypot(sub[i] - sub[i - 2], sub[i + 1] - sub[i - 1]);
        floats.push(sub[i], sub[i + 1], arc);
      }
      shapeIndex.set(id, shapeMeta.length);
      shapeMeta.push({ vertexOffset, vertexCount: sub.length / 2, lengthM: Math.round(arc) });
    }

    for (const [routeId, r] of routes) {
      const shapes = [];
      for (const [shapeId, owner] of shapeUse) {
        if (owner !== routeId) continue;
        const idx = shapeIndex.get(shapeId);
        if (idx !== undefined && !shapes.includes(idx)) shapes.push(idx);
      }
      routesOut[`${op.id}:${routeId}`] = {
        name: r.name,
        color: r.color,
        textColor: r.textColor,
        operator: op.id,
        operatorName: op.name,
        // Only SB has AVL, so only SB routes can ever carry a moving hull.
        live: op.live,
        shapes,
      };
    }

    const stopRoutes = new Map(); // raw stopId -> Set(namespaced routeId)
    await eachRow(op.id, 'stop_times.txt', (cols, h) => {
      const trip = trips.get(cols[h.trip_id]);
      if (!trip) return;
      const stopId = cols[h.stop_id];
      let set = stopRoutes.get(stopId);
      if (!set) stopRoutes.set(stopId, (set = new Set()));
      set.add(`${op.id}:${trip.routeId}`);
    });

    // THE TRAP: stops.txt mixes real terminals with parent stations and street
    // entrances. Only location_type 0 is a place a boat ties up; the rest would
    // plant pins inland.
    let skipped = 0;
    await eachRow(op.id, 'stops.txt', (cols, h) => {
      const id = cols[h.stop_id];
      if ((cols[h.location_type] || '0').trim() !== '0') {
        skipped++;
        return;
      }
      const [x, z] = project(Number(cols[h.stop_lon]), Number(cols[h.stop_lat]));
      terminals.push({
        id: `${op.id}:${id}`,
        name: cols[h.stop_name] || id,
        operator: op.id,
        x: +x.toFixed(1),
        z: +z.toFixed(1),
        parent: (cols[h.parent_station] || '').trim() ? `${op.id}:${cols[h.parent_station].trim()}` : null,
        routes: [...(stopRoutes.get(id) || [])].sort(),
      });
    });
    const opRoutes = Object.keys(routesOut).filter((k) => k.startsWith(`${op.id}:`)).length;
    console.log(
      `[ferry-shapes] ${op.id} ${op.name}: ${opRoutes} routes, ` +
        `${terminals.filter((t) => t.operator === op.id).length} terminals` +
        `${skipped ? ` (skipped ${skipped} station/entrance rows)` : ''}` +
        `${op.live ? '' : ', no live positions'}`,
    );
  }

  terminals.sort((a, b) => a.name.localeCompare(b.name));
  const totalKm = shapeMeta.reduce((sum, sh) => sum + sh.lengthM, 0) / 1000;
  console.log(
    `[ferry-shapes] TOTAL: ${Object.keys(routesOut).length} routes, ${shapeMeta.length} shapes, ` +
      `${floats.length / 3} vertices, ${totalKm.toFixed(0)} km, ${terminals.length} terminals`,
  );

  // ------------------------------------------------------------- serialise
  const jsonRaw = Buffer.from(
    JSON.stringify({
      generated: new Date().toISOString(),
      operators: Object.fromEntries(OPERATORS.map((op) => [op.id, { name: op.name, live: op.live }])),
      routes: routesOut,
      shapes: shapeMeta,
      terminals,
    }),
  );
  // Pad to a 4-byte boundary: the client builds a Float32Array VIEW at
  // 16 + jsonLen, and a typed-array view whose byteOffset is not a multiple of
  // 4 throws. Without this the format works or fails depending on JSON length.
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
      `ferry-shapes.bin is ${(blob.length / 1024).toFixed(0)} KB > budget — trim before shipping`,
    );
  }

  mkdirSync(path.dirname(OUT), { recursive: true });
  writeFileSync(OUT, blob);
  mkdirSync(path.dirname(OUT_STOPS), { recursive: true });
  writeFileSync(
    OUT_STOPS,
    JSON.stringify({
      generated: new Date().toISOString(),
      operators: Object.fromEntries(OPERATORS.map((op) => [op.id, { name: op.name, live: op.live }])),
      routes: Object.fromEntries(
        Object.entries(routesOut).map(([id, r]) => [id, { name: r.name, color: r.color }]),
      ),
      terminals,
    }),
  );
  console.log(
    `[ferry-shapes] wrote ${OUT}: ${(blob.length / 1024).toFixed(0)} KB ` +
      `(json ${(json.length / 1024).toFixed(1)} KB + ${shapeMeta.length} shapes)`,
  );
  console.log(`[ferry-shapes] wrote ${OUT_STOPS}: ${terminals.length} terminals`);
}

main().catch((error) => {
  console.error(`[ferry-shapes] FAILED: ${error.message}`);
  process.exit(1);
});
