# MUNI-LIVE-PROMPT.md — Live Muni hybrid buses from real-time data

Integration task spec for this repo. Read `AGENTS.md` first, then
`docs/asset-plans/transit/README.md` and `INTEGRATION-LATER.md` in the same
directory, then this file top to bottom before writing any code. When done,
deploy and report per the QA section. Where the spec says STOP, stop and ask
David.

## Mission

Put the **real Muni motor-coach fleet** on San Francisco's streets: every
40-foot hybrid bus currently in service appears as the hand-made
`muni-bus-40.glb`, at its real position, driving its real route, with a
hovering route badge (`38R`, `29`, `44`…) over its roof. Clicking a bus opens
the same kind of card a live ferry gets: route, destination, next stop with
live ETA, fleet number, and what the vehicle is. The concierge can answer
"where's the nearest 29?" from the same data.

When live data is unavailable — no key, API down, dev offline — nothing
changes: the procedural road traffic keeps flowing and the app never shows an
error. AGENTS rules 3 (procedural fallback) and 4 (zero required keys) apply to
this feature exactly as they did to the ferries.

## Data source decision (already researched — do not re-litigate)

**Use 511.org's SIRI VehicleMonitoring endpoint with `agency=SF`.** The
alternatives were evaluated and rejected:

| Source | Verdict |
|---|---|
| **511.org SIRI VehicleMonitoring, `agency=SF`** | **Use this.** The same endpoint, same JSON dialect, same key mechanics as the shipped ferry feed — `api/_lib/feeds/ferries.mjs` is a proven template for every failure mode (BOM, gzip, timeout, stale, backoff). It is the region's official open feed of SFMTA's own AVL data. |
| NextBus / UMO public XML (`webservices.umoiq.com`) | Dead — Cubic retired the public API in March 2024. Anything citing it is stale. |
| 511.org GTFS-Realtime (`/transit/vehiclepositions`, protobuf) | Same underlying SFMTA data, but protobuf needs a decoder and `api/` is zero-dependency by rule. SIRI JSON already carries positions + next-stop predictions (`MonitoredCall` / `OnwardCalls`). No advantage that pays for the complexity. |
| Swiftly (SFMTA's AVL vendor) | Not publicly keyed; partnership tier. Violates rule 4. |

So: there is no better free source — 511 *is* the city's recommended API, and
the repo already ships against it. What is genuinely new here is scale and
routing, and that is what this spec is about.

**Key budget — this matters.** A 511 key allows 60 requests/hour.
`feeds/ferries.mjs` already budgets ~40/h of positions + up to 12/h of
timetables on `FERRY_511_KEY`. A Muni feed polling every 60 s is another 60/h —
**it cannot share the ferry key.** Provision a second free key as
`MUNI_511_KEY` (Production, Preview, Development). Fetcher behaviour:

- `MUNI_511_KEY` set → use it, TTL 60 s.
- Unset but `FERRY_511_KEY` set → fall back to the ferry key **at TTL 180 s**
  (20/h, fits the shared budget) so preview deployments work without a second
  key. Log one warning.
- Neither → `{ live: false, reason: 'no-key', vehicles: [] }`, never a 500.

## Scope: motor coaches only, one model

The feed returns every SFMTA vehicle — around 400–600 across five modes at
peak. Only the hybrid-bus GLB exists today, so **this task renders motor-coach
routes only** and the server tags each vehicle with its mode so the client
never needs a route table:

- `LineRef` ∈ {J, K, L, M, N, T} → `lrv`; {F, E} → `streetcar`;
  {59, 60, 61} (Powell–Mason, Powell–Hyde, California) → `cable`;
  trolleybus numbers {1, 2, 3, 5, 6, 7, 14, 21, 22, 24, 30, 31, 33, 41, 45, 49}
  (and their letter-suffixed variants, e.g. `5R`, `14R`) → `trolley`;
  everything else numbered → **`bus`** (motor coach).
- The client instantiates **one bus per live `bus`-mode vehicle** and skips the
  rest. When the trolley/LRV/streetcar/cable GLBs land later, they are new
  entries in the same mode→model map, not a rewrite. Route designations are
  numbers with optional letter suffixes (`29`, `38R`, `8AX`) plus letter rail
  lines — the badge layer must handle 1–3 characters.

Verify the trolleybus list against `docs/asset-plans/transit/README.md` §"Why
five" at implementation time; route electrification does shift.

## Architecture

```
511 SIRI VehicleMonitoring, agency=SF (JSON, 60 req/hr/key)
        │ polled server-side, TTL 60 s
        ▼
api/_lib/feeds/muni.mjs      fetcher + normaliser, registered in feedcore
        │ GET /api/muni (CDN-cached, last-good stale serving — feedcore owns this)
        │ + automatically included in /api/live and the concierge's live_data tool
        ▼
app/src/muni.js              GLB → InstancedMesh (body + glow); route-shape
        │                    following between fixes; route-badge layer; picking
        ▼
app/public/tiles/muni-shapes.bin   baked GTFS route geometry (new pipeline step)
```

Follow the feedcore recipe at the top of `api/_lib/feedcore.mjs` — fetcher
file, `registerFeed`, one import line in `feeds/index.mjs`. That is the entire
server wiring; do not hand-roll caching that feedcore already owns.

## Part 1 — Server: `api/_lib/feeds/muni.mjs`

Model it line-for-line on `feeds/ferries.mjs` (BOM strip, 10 s abort, throw on
failure so the registry serves last-good). Differences:

1. `agency=SF`, key selection per the budget rules above.
2. **Normalise aggressively — the upstream response is large** (hundreds of
   vehicles with nested calls; expect ~1–3 MB). The client gets a compact
   shape, ~200 bytes/vehicle:

```json
{
  "live": true,
  "vehicles": [
    {
      "id": "SF:8632",
      "fleetNumber": "8632",
      "mode": "bus",
      "route": "29",
      "routeName": "29 Sunset",
      "directionRef": "IB",
      "lat": 37.7607, "lon": -122.4885,
      "bearingDeg": 87.0,
      "speedMs": 6.2,
      "occupancy": "seatsAvailable",
      "destination": "Baker Beach",
      "recordedAt": 1786550000000,
      "tripRef": "t_...",
      "next": { "name": "Judah St & 30th Ave", "arrivalAt": 1786550120000, "scheduledArrivalAt": null, "departureAt": null },
      "onward": [ { "name": "...", "arrivalAt": 0 } ]
    }
  ]
}
```

- `fleetNumber` is `VehicleRef` — a real Muni fleet number; keep it verbatim.
- `mode` from the `LineRef` table above. **Ship every mode in the payload**
  (the concierge should know about trains too); the client filters to `bus`.
- `next` from `MonitoredCall`, `onward` capped at the next 2 calls —
  that is what the card shows; more is payload bloat.
- `occupancy` if the feed carries `Occupancy`; null otherwise, and the card
  omits the chip rather than guessing.
- Drop vehicles with no `LineRef` (not in service) and fixes older than 10 min,
  as ferries do.
3. `registerFeed('muni', …)` with `ttl` per key mode, `staleMs: 10 * 60_000`,
   `backoffMs: 5 * 60_000`, `empty: { live: false, vehicles: [] }`, and a
   `describe` written for the concierge, e.g.: `'real Muni vehicle positions
   right now — route, destination, next stop with live ETA, fleet number, mode
   (bus/trolley/LRV/streetcar/cable) per vehicle'`.

**That registration is the entire concierge integration for data access** —
`agent-core.mjs` enumerates registered feeds into the `live_data` tool
automatically. Additionally, extend `focus_entity` so the agent can point the
camera at a live bus by id (`SF:8632`), the same way it can a landmark; the
client-side entity lookup in Part 3 provides the hook.

4. **Verification step (do first, report in the PR):** the ferry appendix
   verified `agency=SB`, not `SF`. Before writing the normaliser, curl the SF
   feed once with a real key (`vercel env pull`) and confirm: vehicle count at
   a weekday hour, `LineRef` spelling for rapid routes (`38R` vs `38ated`),
   whether `MonitoredCall` is populated for buses, occupancy field presence,
   and response size. Paste a redacted sample into the PR description. If
   `MonitoredCall` turns out empty for Muni, the card's ETA line degrades to
   "next stop unknown" — do not invent times.

## Part 2 — Route shapes: `pipeline/muni-shapes.mjs` + `app/public/tiles/muni-shapes.bin`

Buses must drive **streets**, not chords between GPS fixes. The ferry's
straight-line dead reckoning is correct on open water and visibly wrong in a
street grid — a bus cutting diagonally through SoMa blocks would be the first
thing anyone notices. Two candidate mechanisms were considered:

- *Map-match to the baked street graph at runtime* — no new data, but solving
  turn-by-turn routing in the client against 2,501 polylines, one-ways
  unknown, is real complexity with visible failure modes.
- **Bake the real route geometry (recommended).** 511 publishes GTFS static
  per agency (`https://api.511.org/transit/datafeeds?operator_id=SF`, a zip;
  same key). `shapes.txt` + `trips.txt` + `routes.txt` give every Muni route's
  actual street polyline per direction. This is the data-accuracy answer
  (AGENTS rule 5): the 29 drives the real 29 alignment because that is what
  the file says.

New offline pipeline script `pipeline/muni-shapes.mjs`, run rarely (schedules
shift ~quarterly; document the re-run in the script header like the other
pipeline steps):

1. Download GTFS static for SF (needs a key at bake time only).
2. For each **motor-coach** route (same mode table; skip rail/cable/trolley
   until their models exist): pick the most-used shape per direction
   (`trips.txt` frequency), project to scene metres with THE projection
   (`pipeline/lib` — never re-derive), decimate with Douglas-Peucker at ~3 m,
   and store cumulative arc length per vertex.
3. Write one compact binary (`muni-shapes.bin`, follow `tilebin.js`
   conventions: magic, counts, Float32 x/z + cumulative s per vertex; a small
   JSON index `route|direction → offset`). Target ≤ ~600 KB for ~45 routes ×
   2 directions. Commit the baked file like other tiles.
4. Heights are NOT baked: the client samples `sampleElevation(x, z)` at draw
   time like all traffic, so terrain changes never invalidate shapes.

## Part 3 — Client: `app/src/muni.js`

Mirror `app/src/ferries.js` structurally — it already solves the hard parts:
manifest-driven GLB load, **`mergeFerry`-style body+glow split** (this is what
finally lights the bus's amber destination sign at night — reuse that merge,
do not copy `agents.js`'s `mergeVehicle`, which flattens `_Glow`), instanced
draw, poll loop with jitter, dead-reckoning update, stale removal after two
missed polls, pick + entity + follow. Differences:

1. **Capacity and count.** One `InstancedMesh`, capacity 512
   (`DynamicDrawUsage`, `frustumCulled = false`), count = live motor-coach
   vehicles (expect ~200–350 peak). One bus per live vehicle — exactly as many
   as the feed reports, never synthetic extras. Scale instances by
   `carScale` (1.6) to match street traffic; `dims` from the manifest entry.
2. **Movement.** Each vehicle carries its matched shape (`route + directionRef`
   from `muni-shapes.bin`). On each fix: project the fix onto the shape
   (nearest arc-length in a window ahead of the previous position — never
   snap backwards), then advance `s` along the polyline at a speed blended
   from reported `speedMs` and the distance to the next fix's projection, so
   buses glide through corners on the real alignment and never teleport.
   Heading = shape tangent (buses drive forward along their direction; flip
   180° only when a new fix proves it). Fallbacks, in order: no shape match →
   ferry-style straight-line dead reckoning; no fix for > 3 min → fade the
   instance out. `y = sampleElevation(x, z) + lift`, per traffic.
3. **Route badges.** One additional `InstancedMesh` of camera-facing quads,
   one per drawn bus, hovering ~6 m above the roof (clear of the 3.4 m body at
   1.6×). Text via a single lazily-grown `CanvasTexture` atlas of route
   badges — a route's badge is drawn once into the atlas the first time that
   route appears (1–3 chars, chunky type), instances reference its UV window
   via an instanced attribute. Styling follows the toy UI: cream pill, warm-ink
   text, 2px ink border, hard offset shadow, no gradients. **+1 draw call
   total, one small texture.** (The extruded-TextGeometry idiom from
   `signs.js` was considered and rejected here: per-route geometry would cost
   a draw call per route in service, ~40+.) Badges fade with camera distance —
   full at < 2 km, gone by 4 km, and hidden per-instance for buses outside the
   frustum-ish range the ferries already use. This is a new *style element*;
   screenshot it for David's approval early rather than polishing it in secret
   (the STOP rule applies if the pill idiom looks wrong in the scene).
4. **Picking + card.** Copy the ferry's ray-vs-sphere pick (`PICK_RADIUS`
   ~14 m at 1.6×), `entityFor`, and `busEntity(id)` for follow-refresh. New
   entity `kind: 'transit'`; `cards.js` gets one new branch mirroring
   `vessel`'s (line ~168): title `29 Sunset · bus 8632`, chips for `Live` /
   route badge / occupancy (when present), rows for destination, next stop
   with live ETA (+ the 2 onward calls), speed, fleet number and model line
   ("New Flyer XDE40 hybrid" — derivable from the fleet-number ranges in
   `docs/asset-plans/transit/README.md`), and data age. Times that are null
   say so ("no prediction"), never fabricate. Wire into `main.js` exactly as
   ferries: import, create, `pickEntity` priority alongside `pickVessel`
   (buses win over the city, lose to ferries only where they could never
   overlap anyway), `update(dt)` in the frame loop, a `muni` line in the stats
   overlay, and `window.SF.muni` for debugging.
5. **Demo mode.** `?muni=demo` seeds ~6 synthetic buses on 2–3 real shapes
   (one rapid `38R`, one local `29`, one with no shape match to exercise the
   fallback), 20 s poll, exactly like `?ferries=demo`. This is what CI-less QA
   and offline dev use.
6. **Fallback drill (rule 3).** No key / fetch fails / empty vehicles →
   `muni.js` renders nothing and procedural traffic is untouched. The GLB
   missing → one console warn, feature disabled, nothing else changes. Delete
   `muni-shapes.bin` → buses still appear, dead-reckoned. None of these may
   crash or blank the scene.

## Part 4 — Manifest + budgets

- Add the `muni-bus-40` entry to `app/public/sf-assets/vehicles_manifest.json`
  per the draft in `artifacts/muni-bus/REPORT.md` §8 — **with `weight: 0`**,
  the ferry precedent: weight 0 keeps it out of the road spawner
  (`agents.js` filters `weight > 0`), and `muni.js` spawns it from live data
  instead. This sidesteps the round-robin spawner problem documented in
  `INTEGRATION-LATER.md` entirely — do NOT touch the road spawner in this task.
- Copy `artifacts/muni-bus/muni-bus-40.glb` into
  `app/public/sf-assets/vehicles/` and run
  `node pipeline/compress-assets.mjs` (it skips already-compressed files; the
  artifact GLB is already meshopt'd, so expect a skip — verify, don't assume).
- **Draw-call cost of this whole feature: 3** (bus bodies, glow layer, badge
  layer) against the < 300 budget. Instance updates are O(fleet) per frame
  with zero allocation — reuse the ferry's scratch-object idiom. Verify the
  perf gates of AGENTS rule 2 on the reference devices, day and night, with
  the fleet at peak (~350 buses).
- Docs: add the feed to `api/_lib/feedcore.mjs`'s registry comment if it lists
  feeds, note the second key in the README env section, and update
  `docs/asset-plans/transit/INTEGRATION-LATER.md` to mark the live-data path
  as landed (leave the parts about the other four modes).

## QA checklist (report PASS/FAIL each, production URL first line)

1. `/api/muni` with key: `live: true`, plausible vehicle count for the hour,
   every vehicle has `mode`, motor coaches have `route`/`destination`.
2. `/api/muni` without key (preview env var removed): `live: false`, HTTP 200.
3. Buses appear at real positions — spot-check three against a transit app
   (routes 29/44/43 pass through distinctive geography; screenshot one at a
   known intersection).
4. Movement: 5-minute screen recording — buses follow street alignments
   through turns, no teleports, no buses through buildings, stale buses fade.
5. Badges legible at the default camera, gone when zoomed out, styled to the
   toy UI, one draw call (stats overlay).
6. Click a bus → card with route, destination, next stop + ETA, fleet number;
   follow works (card refreshes as the bus moves); `Esc` releases.
7. Concierge: "how many Muni buses are running right now?" and "where is the
   nearest 29?" answered from `live_data`; `focus_entity` flies to a bus.
8. Night: destination-sign glow ignites with the dusk system (this is the
   first vehicle glow in the app — screenshot it).
9. Fallback drill: key removed → procedural traffic unchanged; GLB renamed →
   warn + skip; shapes deleted → dead-reckon.
10. Perf: 60 fps and < 300 draw calls at street level, Mission + downtown,
    desktop and mobile matrix per `docs/plans/PERF-PLAN.md`, with the live
    fleet up.
11. `vercel deploy --prod`, cold-load boots diorama first frame, no 404s.

## Open questions for David (answer before or during, none block starting)

1. Badge content: route only (`29`) or route + direction arrow? (Spec assumes
   route only.)
2. Should non-motor-coach vehicles appear as *anything* before their models
   exist (e.g. generic commuter-bus placeholder for trolleys), or nothing?
   (Spec assumes nothing — wrong-model vehicles are worse than absent ones.)
3. Is a second 511 key acceptable? (Free, but it's a second credential to
   manage. Spec assumes yes; the fallback keeps previews working either way.)
