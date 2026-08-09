# AGENTS.md — San Francisco Toy Diorama City

Read this first. It is the onboarding document for ANY agent (Devin, Claude, or other) working in this repo with zero context.

## What this is

A data-accurate 3D San Francisco in Three.js, rendered as a **toy diorama** (miniature tabletop-model look), deployed at **https://sf-3d.vercel.app** (Vercel project `sf-3d`). Every building stands on its real footprint at its real height; streets, parks, terrain, and landmarks are built from open data (OSM, Overture, DataSF, USGS). The owner is David (github: davidfromkansas). Claude authors specs and 3D assets locally; Devin executes integration prompts in this repo.

## Repo layout

- `app/` — Vite + three.js frontend. Static assets in `app/public/` (`tiles/` = baked city geometry, `sf-assets/` = hand-made GLB landmarks + manifest, `fonts/`).
- `api/` — zero-dependency Vercel functions (`agent.mjs` = the "concierge" LLM endpoint via Vercel AI Gateway).
- `pipeline/` — offline Node scripts that download open data and bake the binary tiles the app streams. Re-run only when data or formats change.
- `vercel.json` — build config (`cd app && npm install && npm run build`, output `app/dist`).
- `PILOT-ASSET-PROMPT.md` — the currently active integration task (single-asset pilot). If present, it is the top-priority spec.

## Iron rules (do not violate; they override any older text you find)

1. **Diorama mode is the DEFAULT AND ONLY user-facing style.** The app boots into it with no flash of any other look. The old realistic/golden style must not be reachable (`M` toggle and `?style=golden` are retired).
2. **Performance budgets are hard gates:** < 300 draw calls worst case, 60 fps on a modern laptop, `devicePixelRatio` clamped ≤ 2, no per-frame allocation, no memory growth while flying around. Verify with the in-app stats overlay at street level in the Mission and downtown (the stress cells).
3. **Procedural fallback is a guarantee, never delete it.** Baked/procedural builders remain the fallback at every level: a missing/broken GLB, an unfit kit piece, or an empty `sf-assets/` folder must degrade to the procedural version with one console warning — never a hole, never a crash.
4. **Zero required paid keys.** The only key the app uses is the Vercel AI Gateway key for the concierge (optional — without it the concierge shows a friendly offline state). `GOOGLE_PLACES_KEY` is strictly optional. Never add a service that makes the build require new billing.
5. **Data accuracy is the product.** Buildings/streets/landmarks sit at real coordinates and real heights. Never invent, move, or rescale real-world features for convenience (semantic/style exaggeration happens in ASSET AUTHORING, not in placement).
6. **Commit hygiene:** author email must be the GitHub noreply address (`<id>+davidfromkansas@users.noreply.github.com`) — plain emails are rejected by the remote. Deploy with `vercel deploy --prod`; report the production URL as the first line of any completion summary, with PASS/FAIL per QA item of the spec you executed.

## Coordinate & data conventions

- Local tangent projection centered lon −122.4375, lat 37.77: `x=(lon−LON0)·111320·cos(LAT0)`, `z=−(lat−LAT0)·110540`; +x east, −z north, y up, meters. ONE projection function — never re-derive elsewhere.
- City is streamed in **500 m cells**; binary tile format: `uint32 count` + N×9 float32 (`x,y,z,nx,ny,nz,r,g,b`), non-indexed. Toy tiles ("TOY2" magic) carry a 10th `flag` float (band-suppression / night-profile / glow bits).
- Terrain from AWS Terrarium tiles; heights sampled via `sampleElevation(x,z)`. Water level = y 0.

## The asset pipeline (hand-made GLB landmarks & kit)

Contract (guaranteed by the authoring side): GLB, real meters, origin base-center sitting on z=0 (water level for bridges/islands), front faces −Y, flat-color materials only (no textures/transparency), materials named `Toy_*`, `*_Glow` suffix = night-glow surfaces, `Toy_body` = per-instance-tintable (kit pieces only). Assets may contain many objects — the LOADER merges each to ≤ 2 draw calls (bake material colors → vertex colors, one Lambert vertexColors material + one glow set). Scale by `targetHeightM / measuredHeight` from the manifest (`app/public/sf-assets/landmarks_manifest.json`) — never trust the file's scale. Landmarks replace code-built versions where ids match, inherit presets/pick/exclusion zones, and fall back per rule 3.

Current state: a single-asset PILOT (Golden Gate Bridge) proves this loader end-to-end — see `PILOT-ASSET-PROMPT.md`. After it passes, a full pack (~200-piece tintable building kit + ~300 unique landmarks) arrives as files + manifest entries with zero code changes, plus kit instancing per its own handoff prompt.

## Art direction (for anyone touching visuals)

The look is a premium handcrafted miniature: chunky beveled massing, flat clean materials, dark blue-gray graphical windows, restrained neutral architecture with saturated accents, designed rooftops (the camera looks down), semantic exaggeration of identity features, manicured landscaping, small clusters of life. NOT photorealism, NOT generic low-poly, NOT voxel art. SF exception: painted residential rows keep their tinted facades. Asset authoring happens in Blender on David's machine (not in this repo); if you are asked to judge visuals, judge from the high three-quarter aerial camera first.

## The concierge (api/agent.mjs)

LLM agent over the city's data. Rules it must keep: answers city facts ONLY from tool results; camera/focus/highlight actions are **intent objects validated server-side and applied client-side** (the model never touches the scene directly); every tool spatially scoped through the cell grid (no citywide scans); per-IP rate limits; friendly 503 without a key; replies as plain text (`textContent`, never HTML).

## UI

All UI (cards, search, concierge panel) follows the toy theme: cream card stock, warm-ink 2px borders, HARD offset shadows (zero blur), candy accent pills, rounded chunky type, press-down button physicality. No gradients, no glassmorphism, no pure black/white. Theme tokens live in the app's ui-theme stylesheet — if a color/shadow isn't a token, it doesn't ship.

## QA norms for every change

Screenshot-verify on the DEPLOYED site, not just localhost: hero view + the affected area, day and night, cold cache-cleared load boots the diorama first-frame, budgets hold (rule 2), picking/search/cards still work, and the fallback drill passes (rename the asset/data you added → app degrades gracefully). Honest reporting: a FAIL with explanation is acceptable; a hidden one is not.

## Known gotchas

- glTF exports authored in multi-scene Blender files can leak selected objects from other scenes — if an asset contains foreign geometry, reject it back to the authoring side.
- Socrata/DataSF bulk downloads occasionally throttle — a free app token raises limits.
- The tile loader's cross-fade uses hashed-alpha discard with distance hysteresis; visible LOD pops are always a bug.
- 404s in console = missing tile/resource — root-cause them, don't ignore.
