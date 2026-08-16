# Performance audit — 2026-08-16

Scope: why the app feels laggy when moving around, and why mobile Safari/Chrome
reload-loop and then fail. Measured on `main` @ `f8a71469`.

Evidence:

- `artifacts/perf/audit-mobile-main-2026-08-16T18-59-50-551Z.json` (this VM, software GPU — structure only, fps invalid)
- `artifacts/perf/realgpu-mac-baseline-2026-08-12T02-05-11-231Z.json` (real GPU — fps + heap valid)
- `artifacts/perf/attribution-hero.json` (new per-object triangle/VRAM attribution, fully-loaded hero)

## 1. What the numbers say

Fully-loaded hero view, high tier, everything the scene holds:

| Bucket | Objects | Triangles (authored) | GPU geometry |
|---|---:|---:|---:|
| trees (instanced, 271,684) | 53 | 28.3 M | 17 MB |
| ground / streets / landcover | 84 | 4.1 M | **151 MB** |
| terrain | 4 | 2.1 M | 64 MB |
| far city (2 km prisms) | 58 | 1.7 M | 68 MB |
| near buildings | 18 | 0.6 M | 70 MB |
| street lamps + pools (82,110) | 100 | 3.4 M | 5 MB |
| building kit (batched) | 1 | 0.2 M | 23 MB |
| **total** | **424** | **40.7 M** | **413 MB** |

Mission street level (the stress cell) adds one more heavyweight bucket:
**585 traffic vehicles at ~5,700–9,200 triangles each = 3.6 M triangles**, with no
LOD and no per-tier count cap. Ground there is 4.5 M, trees 2.3 M visible,
terrain 2.1 M, far city 1.7 M, near buildings 0.8 M. JS heap at that station on
this VM: **1.07 GB** (vs 291 MB at hero) — memory clearly grows as you move.

City state at that moment: `cellsLoaded 1728 / 1656`, `farGroups 58`,
`groundGroups 57` — i.e. **the entire city is resident regardless of where the
camera is**, and nothing is ever released.

Per-frame triangles actually drawn (after frustum culling):

| Station | Mobile profile (low tier) | Real-GPU mobile profile (high/ultra) |
|---|---:|---:|
| hero | 6.4 M | 25.1 M |
| mission street | 4.3 M | 9.0 M |
| downtown street | 3.9 M | 7.1 M |
| golden gate | 1.5 M | 4.5 M |

A 2023-class phone sustains roughly 1–2 M triangles/frame at 60 fps. We are
3–15× over, at the *lowest* quality tier.

JS heap on the real-GPU run: **1.20 GB → 2.09 GB across four stations**, rising
monotonically. iOS Safari kills a tab well below that. This is the reload loop.

Draw calls: 53–178 peak — comfortably inside the <300 budget. Draw calls are
*not* the problem; resident geometry and memory are.

## 2. Root causes

1. **`city.preload()` builds every group in the city** (`app/src/city.js`):
   both `buildFarGroup` and `buildGround` are pumped over *all* groups sorted by
   distance, and neither far meshes, ground meshes, trees nor lamps are ever
   disposed. Only near chunks and ground detail have range in/out.
2. **Trees**: 271,684 instances × 104 triangles, one full-detail archetype at
   every distance. Largest triangle source in the scene.
3. **Terrain**: fixed 1024² grid = 2.1 M triangles always drawn; the coarse
   index (÷4) only engages on `low`/`medium`. It is also built on the **main
   thread at boot** — ~1.05 M vertices × 5 elevation samples — a multi-second
   freeze on a phone before first paint.
4. **Tile vertex format**: non-indexed, 9 × float32 = 36 bytes/vertex
   (108 bytes/triangle). That is why 4.1 M ground triangles cost 151 MB.
5. **Boot fetches the whole city** (~1,656 cells, 32 MB gzipped): measured
   ~70 s to full city on Fast 4G.
6. **Startup tier + governor**: phones start at `medium` (dpr/width heuristic),
   and the governor holds off the down-step while streaming
   (`heldOff: "streaming"`) — which is exactly the window in which phones die.

## 3. Stack-ranked fixes

Ranked by (fps + crash impact) ÷ risk.

### P0 — Camera-radius residency for the whole city
Build/keep ground groups, trees and lamps only within ~4–6 km of the camera;
release beyond 1.25× with the existing fade. Keep the cheap far-prism tier as
the always-resident skyline so nothing ever holes.
*Impact*: 413 MB → ~120–150 MB resident; heap plateaus; kills the mobile crash.
*Tradeoff*: brief pop-in on very fast cross-city flights (masked by the existing
cross-fade); skyline silhouette stays intact.

### P1 — Tree LOD + count cap
Full lollipop under ~600 m, a 12-triangle blob to ~1.5 km, a 2-triangle imposter
beyond; hard cap instances per frame by tier.
*Impact*: −3 to −4 M triangles/frame at hero, the single biggest frame-time win.
*Tradeoff*: distant foliage reads as coloured mass, which is on-style for a
diorama; near views unchanged.

### P2 — Vehicle triangle budget
44 taxis cost 406 k triangles today. Decimate the 14 fleet GLBs to a toy budget
(~600–1,200 triangles each, they are 5–15 mm on screen), add a distance cull and
a per-tier count cap.
*Impact*: −3 M triangles/frame at street level, where the complaints come from.
*Tradeoff*: none visible at diorama scale; requires a one-off asset re-bake.

### P3 — Terrain LOD
Add a stride-4 index (131 k triangles), default phones to coarse at all tiers,
and pick the index by camera height.
*Impact*: −1.5 to −2 M triangles/frame everywhere.
*Tradeoff*: 15 m → 30/60 m hill resolution on mobile; visible only on bare
hillsides at grazing angles.

### P4 — Load only the camera's neighborhood at boot
Fetch/build the ~100 cells around the opening camera first, stream the rest on
approach (falls out of P0).
*Impact*: first interactive view in single-digit seconds on 4G instead of ~70 s;
peak memory during boot drops with it.
*Tradeoff*: the far skyline fills in over the first seconds.

### P5 — Compact tile format
Indexed geometry with quantized attributes (int16 position, int8 normal/colour)
≈ 8–12 bytes/vertex.
*Impact*: tiles ~57 MB → ~20 MB raw, VRAM roughly −3×, faster GPU upload.
*Tradeoff*: pipeline re-bake + a format version bump; one-time validation pass.

### P6 — Move terrain build off the main thread (or bake it)
*Impact*: removes the multi-second startup freeze / watchdog risk on phones.
*Tradeoff*: terrain appears one frame after the rest, or a new baked artifact.

### P7 — Mobile-first startup tier + governor emergency step
Start `low` on coarse-pointer devices; let the governor step *down* even while
streaming (keep the hold-off for step-*up* only).
*Impact*: phones never spend the dangerous first 60 s at medium/high.
*Tradeoff*: phones look slightly softer until the governor promotes them.

### P8 — Texture memory
The two 1254² PNGs decode to ~6 MB RGBA each; 512² or KTX2/Basis.
*Impact*: −8 to −10 MB VRAM, faster load.
*Tradeoff*: slightly softer water/grass detail.

### P9 — Night overdraw + agents on mobile
82 k lamp instances / 3.4 M triangles at night, plus additive light pools.
Range-limit lamps with the same radius rule as P0 and scale agent counts by tier.
*Tradeoff*: fewer visible street lights far from the camera at night.

### P10 — Context-loss recovery + hidden-tab pause
Rebuild on `webglcontextrestored` (today it only pauses) and stop the loop and
feed polls on `visibilitychange`.
*Tradeoff*: none.

## 4. Targets after P0–P4

| Metric | Now (mobile) | Target |
|---|---:|---:|
| triangles/frame | 4–6 M | < 1.5 M |
| resident geometry | 413 MB | < 150 MB |
| JS heap after 10 min flight | 1.2–2.1 GB | < 500 MB, flat |
| first interactive view (4G) | ~70 s | < 10 s |
| draw calls | 53–178 | unchanged, < 300 |

## 5. Verification plan

The dev VM renders in software (SwiftShader), so fps here is not evidence. After
each landed change: `node pipeline/perf-harness.mjs --profile mobile` for
structure (triangles, draw calls, heap, resident counts), then real-device runs
on the deployed URL for the 60 fps guardrail — desktop Chrome/Safari/Edge/Firefox
and mobile Chrome/Safari, at hero, Mission street level and downtown street
level, day and night.
