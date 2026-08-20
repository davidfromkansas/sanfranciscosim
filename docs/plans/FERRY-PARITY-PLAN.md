# Ferry parity plan — bringing the live ferries up to the Muni layer

The ferries were the city's FIRST live feed and have not been touched since.
Muni has since gained route geometry, real stops, badges, per-mode vehicles and a
tested motion kernel. This plan closes that gap. It is four workstreams; W1 is a
bug fix and should land first.

**STATUS 2026-08-17: all four workstreams are built and committed on
`docs/ferry-parity`, unpushed.** W1 `509658fd2`, W3 `4291c48c9`, W2 `565b210ce`,
W4 `92fa2e690`. Outstanding follow-ups, both flagged in code: migrate `muni.js`
onto the shared `app/src/routewall.js` (its own copy of the ribbon shader is
still there, unverifiable here because `vite preview` serves no `/api/muni`),
and QA the whole set on the DEPLOYED site — everything below was verified in
headless Chrome against a local build, which cannot exercise the live feeds.

**What shipped before this work:** `/api/ferries` (511 SIRI VehicleMonitoring, agency `SB` =
WETA), `app/src/ferries.js` — 15 live vessels as one instanced GLB with wakes,
bobbing, clickable cards, and procedural fallback. No route lines, no terminals,
no badge, no tested motion rules.

---

## W1 — Motion kernel (`ferry-motion.js` + tests)

**This is a live bug, not just missing polish.** `ferries.js` has one clock,
`lastFixAt`, bumped on every poll including repeats. The browser polls every 60 s;
the server caches for 90 s; so a large fraction of polls return a byte-identical
payload. On a repeat, `step` is 0, so `speed` is set to 0 (`ferries.js:315`), so
`update()` switches dead reckoning off (`run = speed > IDLE_SPEED ? … : 0`) and
the boat freezes until the next genuinely new fix. It also loses its wake (length
is derived from speed) and its card reports 0 kn while underway.

This is exactly invariant 4 in `app/src/muni-motion.js`, which the buses already
learned the hard way:

> Liveness and freshness are different clocks. `lastFixAt` (bumped on EVERY poll,
> stale ones included) decides whether a vehicle still exists; `lastFreshFixAt`
> (bumped only by a new fix) drives speed and the dead-reckon cap.

**Measured, production, 2026-08-17:** two polls 60 s apart returned identical
`fetchedAt` (the cache serving a repeat, as predicted). All 15 vessels carry the
*same* `recordedAt` — 511 publishes one fleet-wide snapshot rather than per-vessel
timestamps — and across the two upstream refreshes sampled it was 4.7 s and 11.3 s
old when our server fetched it. Two samples is thin, but both say the upstream is
far fresher than our 60/90 s cadence, and `recordedAt` is a reliable freshness key.
Worth re-measuring over a longer window before tuning any interval to it.

**Do:**

1. Extract the motion rules from `ferries.js` into `app/src/ferry-motion.js` —
   pure functions, no three.js, no closure state, mirroring `muni-motion.js`.
2. Add `lastFreshFixAt`. Dedupe on the fleet-wide `recordedAt`: unchanged ⇒ bump
   liveness only, leave speed, heading and the dead-reckon clock alone.
3. Cover it with `app/test/ferry-motion.test.mjs`, encoding the freeze bug as a
   regression test. `npm run build` runs `npm test`, so it fails the Vercel build.

**Adapt, don't copy:** a boat has no shape to follow, so dead reckoning runs along
heading rather than along a polyline (until W2 lands, after which it can follow
the alignment). Muni's `DWELL_STEP_M` is a bus length; a ferry needs its own.
Keep the existing bearing-0-means-unknown rule — it is correct and hard-won.

**Acceptance:** `cd app && npm test`; on the deployed site a boat underway keeps
moving across at least three consecutive polls, and its card shows a non-zero
speed.

---

## W2 — Bay route lines

**Source:** 511 GTFS static, same endpoint as Muni with the operator swapped —
`https://api.511.org/transit/datafeeds?operator_id=SB`. Bake-time key only
(`FERRY_511_KEY`), runtime never touches GTFS static, so rule 4 holds.

**Do:** a `pipeline/ferry-shapes.mjs` mirroring `muni-shapes.mjs` — same container
idiom, output `app/public/tiles/ferry-shapes.bin`, committed like the other tiles.
**It must be added to `npm run all`**: `muni-shapes.mjs` documents being silently
deleted once by a landmark re-bake that regenerated `app/public/tiles/` wholesale,
and nothing failed loudly.

**Shape quality — VERIFIED 2026-08-17, risk closed.** Downloaded and inspected the
real SB feed. The shapes are genuine navigational polylines, not the straight
terminal-to-terminal stubs this plan feared:

- **43 distinct shapes** across **7 routes**, 22–80 points each, mean segment
  50–723 m. The Vallejo run is 46.3 km over 65–80 points and traces the actual
  course up the Bay. Only the two Oakland water-shuttle hops are 2-point lines,
  which is correct — they are a 300 m crossing.
- **Every route carries an official `route_color`**, so each wall can be its real
  SF Bay Ferry livery colour rather than an invented palette: Vallejo `#008c99`,
  Oakland & Alameda `#4fab47`, Richmond `#004576`, South SF `#851f83`, Harbor Bay
  `#c74a5d`, Alameda Seaplane `#df7a1c`, Oakland-Alameda Shuttle `#ffd400`.

**Visual — OWNER DECISION: walls, same styling as Muni.** I had recommended flat
surface lanes on the argument that a wall standing on open water reads as a fence;
David has overruled that and wants the Muni glow-wall idiom. Build the walls. The
per-route colours above are what will make them read as seven distinct services
instead of one glowing mass. Per rule 2 this ships its `setQuality(tier)` lever in
the same PR, and the wall geometry is the thing to watch: these spans are far
longer than any bus route, so subdivide by arc length rather than per shape point.

**Clipping is real work.** The water plane is 30 km across (±15 km,
`SCENE_HALF_EXTENT` 14 500 m) and four terminals fall outside it — Harbor Bay
(x 15 890), Richmond (z −15 421), Vallejo and Mare Island (z ≈ −36 500). So the
Vallejo, Richmond and Harbor Bay walls all run off the edge of the world and must
terminate gracefully at the boundary rather than into void. Boats already get
culled there, so the wall and the vessel need to agree about where the scene ends.

---

## W3 — Ferry terminals

**Source:** `stops.txt` from the same SB feed, plus the SIRI feed already carrying
`origin` and `next` stop refs and names per vessel.

**VERIFIED 2026-08-17.** 23 rows, but only **15 are real terminals**
(`location_type` 0). The rest are the Ferry Building's parent station (`7201`,
type 1) and four building entrances (type 2) — filter on `location_type` or you
will plant pins in the middle of the Embarcadero. The Ferry Building itself is
**three separate gate stops** (E `72011`, F `72013`, G `72012`, ~30 m apart), so
it needs one marker treatment, not three colliding pins.

**11 of the 15 sit inside the water plane** and can carry a marker: the three
Ferry Building gates, Pier 41, Pier 48, Oakland (+ its Jack London Square shuttle
dock), Alameda Main Street, Alameda Bohol Circle, Alameda Seaplane, and South San
Francisco. **Four are outside** and get nothing: Harbor Bay, Richmond, Vallejo and
Mare Island. Note the Alameda/Oakland cluster sits at x ≈ 12 200–14 100, i.e.
right against the 14 500 m edge — worth eyeballing before assuming they render.

**Do:** mirror the Muni stop layer — `app/src/ferrystops.js` for the parse, marker
+ clickable pins following `munistoplayer.js`, and an `api/_data/ferry-stops.json`
beside `muni-stops.json` so the concierge can answer terminal questions (the agent
runs in `api/` and cannot read `app/public`).

Only the SF-side terminals sit inside the modeled city — the Ferry Building is
already a landmark asset, so its gates need to cohere with it rather than plant a
generic pin through it. Cross-bay terminals inside the water plane (Oakland,
Alameda) can carry a marker; those outside it get none.

**Do NOT** give a ferry terminal a bus shelter. `munistops.js` is explicit that
rail platforms and cable stops are excluded for exactly this reason.

---

## W4 — Route badge on the vessel

Cheapest of the four and depends on nothing. Reuse the badge-hugging-vehicle work
from PR #139 (`Keep a route badge on its vehicle`), fed by `routeName`, which the
feed already returns per vessel. Boats are far more spread out than buses, so the
declutter rules that badge work needed will be slack here.

---

## Order and cross-cutting gates

W1 → W3 → W2 → W4. W1 is a bug and cheap. W3 is small and buys the most
legibility per unit of work. W2 is the largest and is the one with a real unknown
in it. W4 can slot in anywhere.

Every workstream: procedural/graceful fallback preserved (rule 3), a
`setQuality(tier)` lever for anything visual (rule 2), no new runtime key (rule 4),
`cd app && npm test` before shipping, and deployed screenshot QA day and night.
Verify with `pipeline/health-probe.mjs` that draw calls and heap have not moved —
the current prod baseline is in `docs/plans/PERF-BASELINE-2026-08-17.md`.

## Open questions for the owner

1. **How the three long routes end.** Vallejo, Richmond and Harbor Bay all run
   past the edge of the water plane. A hard cut at 14 500 m is honest but reads as
   unfinished; fading the wall out over the last few hundred metres costs little
   and suggests the route continues. Recommend the fade. (The walls themselves are
   decided — David wants the Muni styling.)
2. **Do terminals get assets or markers?** A marker is a day of work; a hand-made
   terminal GLB per SF-side berth is a landmark-pipeline job.
3. **Golden Gate Ferry (agency `GF`, Sausalito/Larkspur) is a separate feed** and
   is not in scope here. Sausalito boats are visibly absent from the Bay today.
