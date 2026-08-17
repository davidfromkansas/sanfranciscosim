# AGENTS.md — San Francisco Toy Diorama City

Read this first. It is the onboarding document for ANY agent (Devin, Claude, or other) working in this repo with zero context.

## What this is

A data-accurate 3D San Francisco in Three.js, rendered as a **toy diorama** (miniature tabletop-model look), deployed at **https://sf-3d.vercel.app** (Vercel project `sf-3d`). Every building stands on its real footprint at its real height; streets, parks, terrain, and landmarks are built from open data (OSM, Overture, DataSF, USGS). The owner is David (github: davidfromkansas). Claude authors specs and 3D assets locally; Devin executes integration prompts in this repo.

## Repo layout

- `app/` — Vite + three.js frontend. Static assets in `app/public/` (`tiles/` = baked city geometry, `sf-assets/` = hand-made GLB landmarks + manifest, `fonts/`).
- `api/` — Vercel functions with exactly ONE dependency (`gtfs-realtime-bindings`, decoding the Muni feed's protobuf — owner-approved 2026-08-12; adding another needs an owner decision; protobuf never reaches the browser). `agent.mjs` = the "concierge" LLM endpoint via Vercel AI Gateway. All live data feeds (`/api/ferries`, `/api/live`, future feeds) share ONE function — `api/[...path].mjs` dispatching into the feed registry (`api/_lib/feedcore.mjs`); adding a feed = one fetcher module in `api/_lib/feeds/` + one import line (the full recipe is in feedcore's header). Feeds share a process on purpose: it is what lets `/api/live` compose a consolidated snapshot from memory.
- `pipeline/` — offline Node scripts that download open data and bake the binary tiles the app streams. Re-run only when data or formats change.
- `docs/styles/` — the canonical style bibles (see `docs/styles/README.md`); `.agents/skills/` — agent procedures (asset intake, testing, style pointer).
- `vercel.json` — build config (`cd app && npm install && npm run build`, output `app/dist`).
- `*-PROMPT.md` files at the root — integration task specs. `KIT-INTEGRATION-PROMPT.md` (building kit v2) is the currently active one; `PILOT-ASSET-PROMPT.md` (Golden Gate pilot) is complete and kept as the loader's reference spec.

## Skills & docs — which to read for which task

Reusable knowledge lives in two places; read the right one BEFORE starting, don't rediscover it:

- **Touching visuals, authoring/reviewing/conforming any 3D asset** → `docs/styles/miniature-toy.md` (the canonical style bible, in full) plus `docs/styles/README.md` (style index + where the style is implemented in code).
- **Intaking/validating a GLB** (new landmark, kit piece, vehicle) → `.agents/skills/sf-asset-check/SKILL.md`: the contract checklist, the Blender inspection script, conform workflow, leak-proof export, manifest-entry format. Follow it step by step.
- **Testing the app** (locally or deployed) → `.agents/skills/testing-sf-3d/SKILL.md`: dev commands, key bindings, the `window.SF` debug API, measurement recipes, and environment gotchas.
- `.agents/skills/sf-miniature-style/SKILL.md` is only a pointer to `docs/styles/` for skill auto-discovery.

Rules for maintaining these: they are the single source of truth — update them (reviewed commits) when the style or contract evolves; never fork their content into prompts or other docs, cite the file instead. Copies under `~/.claude/skills/` on David's machine are thin stubs pointing here.

## Iron rules (do not violate; they override any older text you find)

1. **Diorama mode is the DEFAULT AND ONLY user-facing style.** The app boots into it with no flash of any other look. The old realistic/golden style must not be reachable (`M` toggle and `?style=golden` are retired).
2. **Performance budgets are hard gates:** < 300 draw calls worst case, 60 fps in the popular browsers on desktop (Chrome, Safari, Edge, Firefox) AND mobile (Chrome, Safari) reference devices, `devicePixelRatio` clamped ≤ 2, no per-frame allocation, no memory growth while flying around. Verify with the in-app stats overlay at street level in the Mission and downtown (the stress cells). The full guardrail — browser matrix, reference devices, measurement cadence — is defined in `docs/plans/PERF-PLAN.md` (THE GUARDRAIL section); a change that holds 60 fps in desktop Chrome but drops any matrix browser below 60 is a FAIL. Every visual subsystem exposes `setQuality(tier)` and is fanned out from `applyQuality` in `main.js` (the `QUALITY` table in `ui.js` documents what each tier means) — a new visual feature ships its lever in the same PR.
3. **Procedural fallback is a guarantee, never delete it.** Baked/procedural builders remain the fallback at every level: a missing/broken GLB, an unfit kit piece, or an empty `sf-assets/` folder must degrade to the procedural version with one console warning — never a hole, never a crash.
4. **Zero required paid keys.** The only key the app uses is the Vercel AI Gateway key for the concierge (optional — without it the concierge shows a friendly offline state). `GOOGLE_PLACES_KEY` is strictly optional. Never add a service that makes the build require new billing.
5. **Data accuracy is the product.** Buildings/streets/landmarks sit at real coordinates and real heights. Never invent, move, or rescale real-world features for convenience (semantic/style exaggeration happens in ASSET AUTHORING, not in placement). ONE approved exception exists: live **aircraft** are drawn at compressed altitude AND compressed horizontally onto the city (`app/src/aircraft.js`), because SF's airspace is mostly not over SF — literal placement showed an empty sky (measured: 0 of 23 aircraft over the city). Bearing is exact, the card reports the true distance, `?airscale=off` restores literal positions. This covers transient live aircraft ONLY — buildings, streets, landmarks and terrain remain untouchable.
6. **Commit hygiene:** author email must be the GitHub noreply address (`<id>+davidfromkansas@users.noreply.github.com`) — plain emails are rejected by the remote. Deploy with `vercel deploy --prod`; report the production URL as the first line of any completion summary, with PASS/FAIL per QA item of the spec you executed.

## Coordinate & data conventions

- Local tangent projection centered lon −122.4375, lat 37.77: `x=(lon−LON0)·111320·cos(LAT0)`, `z=−(lat−LAT0)·110540`; +x east, −z north, y up, meters. ONE projection function — never re-derive elsewhere.
- City is streamed in **500 m cells**; binary tile format: `uint32 count` + N×9 float32 (`x,y,z,nx,ny,nz,r,g,b`), non-indexed. Toy tiles ("TOY2" magic) carry a 10th `flag` float (band-suppression / night-profile / glow bits).
- Terrain from AWS Terrarium tiles; heights sampled via `sampleElevation(x,z)`. Water level = y 0.

## The asset pipeline (hand-made GLB landmarks & kit)

Contract (guaranteed by the authoring side): GLB, real meters, origin base-center sitting on z=0 (water level for bridges/islands), front faces −Y, flat-color materials only (no textures/transparency), materials named `Toy_*`, `*_Glow` suffix = night-glow surfaces, `Toy_body` = per-instance-tintable (kit pieces only). Assets may contain many objects — the LOADER merges each down (bake material colors → vertex colors, one Lambert vertexColors material + one glow set). Scale by `targetHeightM / measuredHeight` from the manifest (`app/public/sf-assets/landmarks_manifest.json`) — never trust the file's scale. Landmarks replace code-built versions where ids match, inherit presets/pick/exclusion zones, and fall back per rule 3.

**Streaming & batching (how landmarks scale — every integration must follow this):**

- All generic landmarks render out of one shared `BatchedMesh` pair (bodies + glow): **2 draw calls total no matter how many landmarks exist.** Bridges keep their own meshes and are always resident. Never add a whole-city batched/instanced object without `frustumCulled = false` (see `kitfleet.js` and `assets.js` — batch bounds cover the reserved buffer and cull on-screen content otherwise; this bug has shipped twice).
- **Every new manifest entry declares its streaming decision** (see `docs/asset-plans/INTEGRATION-PROMPT.md`): `loadRadius` metres (default rule `max(2500, targetHeightM × 30)`) makes the GLB fetch on approach and release past 1.25×; `alwaysLoaded: true` is reserved for skyline-scale pieces — that list is the only one that still grows boot cost, keep it short.
- **Budgets per landmark:** ≤ 30k triangles standard, ≤ 60k for `alwaysLoaded` skyline pieces; ≤ 500 KB compressed on disk. The shared batch holds ~400k triangles of *simultaneously loaded* landmarks — streaming keeps that to the camera's neighborhood, so only clustering many heavy assets in one district can hit it.
- **Ship step:** every GLB entering `app/public/sf-assets/` is meshopt-compressed once at intake with `node pipeline/compress-assets.mjs` (it enforces the flags that keep material names and float32 attributes — the defaults silently corrupt the merge paths). After a batch of integrations, run `node pipeline/landmark-streaming-check.mjs` against a build: the procedural fallback hides loader failures from the eye, and this is what catches them.

Current state: the manifest-driven loader is live with streaming + batching; the 207-piece building kit and 14-vehicle fleet are integrated and instanced; live WETA ferries render from `/api/ferries` (511.org SIRI, optional `FERRY_511_KEY`, `live:false` fallback); live Muni buses render from `/api/muni` (511.org GTFS-Realtime, optional `MUNI_511_KEY` — falls back to a degraded positions-only poll on the ferry key, then to `live:false`; the two keys each carry a 60 req/h budget so they must not share at full rate); live air traffic renders from `/api/flights` (community ADS-B — adsb.lol then adsb.fi, NO key at all; `app/src/aircraft.js` draws three procedural airframes chosen by ICAO type, at COMPRESSED display altitude since real cruise is twice the camera's ceiling — the cards keep the true numbers). ~300 unique landmarks can now land as files + manifest entries with zero code changes and O(1) render cost.

## Art direction (for anyone touching visuals)

The full, canonical style bible is `docs/styles/miniature-toy.md` — read it before authoring or judging any visual work; this paragraph is only the condensed version. The look is a premium handcrafted miniature: chunky beveled massing, flat clean materials, dark blue-gray graphical windows, restrained neutral architecture with saturated accents, designed rooftops (the camera looks down), semantic exaggeration of identity features, manicured landscaping, small clusters of life. NOT photorealism, NOT generic low-poly, NOT voxel art. SF exception: painted residential rows keep their tinted facades. Asset authoring happens in Blender on David's machine (not in this repo); if you are asked to judge visuals, judge from the high three-quarter aerial camera first.

## The concierge (api/agent.mjs)

LLM agent over the city's data. Rules it must keep: answers city facts ONLY from tool results; live conditions come through ONE `live_data` tool that requests exactly the feeds a question needs (names and descriptions derive from the feed registry — a newly registered feed reaches the concierge with zero concierge changes) and self-fetches the deployment's own `/api/<feed>` URLs so reads hit the CDN, never the upstreams; camera/focus/highlight actions are **intent objects validated server-side and applied client-side** (the model never touches the scene directly); every tool spatially scoped through the cell grid (no citywide scans); per-IP rate limits; friendly 503 without a key; replies as plain text (`textContent`, never HTML).

## UI

All UI (cards, search, concierge panel) follows the toy theme: cream card stock, warm-ink 2px borders, HARD offset shadows (zero blur), candy accent pills, rounded chunky type, press-down button physicality. No gradients, no glassmorphism, no pure black/white. Theme tokens live in the app's ui-theme stylesheet — if a color/shadow isn't a token, it doesn't ship.

## Live vehicle motion (the regression that keeps coming back)

"The buses are frozen" and "parked coaches are cluttering the city" have each been fixed several times (9e9accd8, 10b388aa, 5f0ea041, 73bb2a96, 4cd32464) and each fix was later undone by an unrelated pass through `app/src/muni.js`. The rules therefore no longer live inline in the renderer: they are pure functions in **`app/src/muni-motion.js`**, locked by **`app/test/muni-motion.test.mjs`** (`cd app && npm test`, and `npm run build` runs it first, so a broken rule fails the Vercel build). Read that file's header before touching anything that decides whether a vehicle moves or leaves the scene, and never inline a copy of one of its rules back into `muni.js`.

The four invariants a live-feed layer must keep (they apply to ferries and aircraft too):

1. **Dwell is a displacement test, never a speed reading.** GTFS-RT `speed` is an instantaneous sample — 260 of 507 Muni vehicles report exactly 0 at any instant. `fixStep` (metres between consecutive fixes) is the only dwell evidence; the reported speed may only bias how fast an already-moving vehicle runs.
2. **Measure that displacement fix-to-fix, never render-position-to-target.** Dead reckoning legitimately drives a vehicle past its target, so `targetS - s` goes negative on a bus that just covered 900 m.
3. **Vehicles keep moving between fixes.** Fresh fixes are up to ~120 s apart (60 s poll vs 90 s TTL, worse in degraded mode) and identical payloads are normal, so a moving vehicle extrapolates along its shape (`DEAD_RECKON_MAX_S`) instead of stopping at the last target.
4. **Liveness and freshness are different clocks.** `lastFixAt` (bumped by every poll that mentions the vehicle, stale payloads included) decides whether it still exists; `lastFreshFixAt` (bumped only by a new fix) drives speed, dormancy and the dead-reckon cap. Merging them evicted the whole fleet every 3 minutes.

The flip side is removal: a vehicle the data says is parked, on layover, or off its alignment sinks out of the scene, and one the feed stops reporting is dropped. If you change any threshold here, change it in `muni-motion.js` with a test, and verify on the deployed site that vehicles both MOVE and DISAPPEAR when they should.

## QA norms for every change

Screenshot-verify on the DEPLOYED site, not just localhost: hero view + the affected area, day and night, cold cache-cleared load boots the diorama first-frame, budgets hold (rule 2), picking/search/cards still work, and the fallback drill passes (rename the asset/data you added → app degrades gracefully). Honest reporting: a FAIL with explanation is acceptable; a hidden one is not.

## Known gotchas

- glTF exports authored in multi-scene Blender files can leak selected objects from other scenes — if an asset contains foreign geometry, reject it back to the authoring side.
- Socrata/DataSF bulk downloads occasionally throttle — a free app token raises limits.
- The tile loader's cross-fade uses hashed-alpha discard with distance hysteresis; visible LOD pops are always a bug.
- 404s in console = missing tile/resource — root-cause them, don't ignore.
- Anything touching live vehicles: run `cd app && npm test` before shipping. A failure there means you are re-introducing a bug the city has already shipped once (see "Live vehicle motion").
