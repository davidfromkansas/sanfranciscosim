# PLAN — Performance program: hold 60 fps on desktop AND mobile while the city keeps growing

This is a program of ranked workstreams, not one integration task. Each numbered
item below is sized to be executed as its own session/PR, in rank order unless
stated otherwise. Read `AGENTS.md` first — iron rule 2 (perf budgets) is the
subject of this entire plan; rules 3 (procedural fallback), 4 (zero required
keys) and 5 (data accuracy) constrain every solution here.

## THE GUARDRAIL (owner mandate — governs everything below)

**The app must render at 60 fps in the popular browsers on BOTH desktop web
and mobile web.** Not "60 in Chrome on a modern laptop, best-effort
elsewhere" — 60 fps is a shipping requirement across the browser matrix below,
on the same footing as the < 300 draw-call budget.

**The browser matrix (where 60 fps is required):**

| Platform | Browsers |
|---|---|
| Desktop web | Google Chrome, Apple Safari, Microsoft Edge, Mozilla Firefox |
| Mobile web | Google Chrome (Android), Apple Safari (iOS) |

(Chromium-derived browsers — Edge, Brave, Arc, iOS/Android WebViews — are
covered by the Chrome/Edge entries; anything not in the table is best-effort.)

Operationally:

- Every feature, asset, and PR is judged against 60 fps on the reference
  devices across this matrix. A change that holds 60 in desktop Chrome but
  drops any matrix browser below 60 (with the governor's adaptation
  exhausted) is a FAIL. iOS Safari and Firefox are the usual divergents
  (different GPU/ANGLE backends, different GC and shader-compile behavior) —
  never assume a Chrome result transfers.
- The governor (#1) and quality levers (#6) exist to hold this line: the
  visual tier may step down on weak hardware or a slower browser, but the
  frame rate may not.
- The harness (#0) measures a desktop profile and a mobile-class profile on
  every run (real device where available, else CPU/GPU-throttled emulation
  documented in the testing skill). The full four-browser desktop sweep plus
  both mobile browsers runs per release and whenever a workstream touches
  shaders, the render loop, or the post pipeline; day-to-day PR runs may use
  Chrome desktop + mobile profile as the fast proxy.
- **Reference devices** (to pin exact models when #0 lands): desktop = a
  current mainstream laptop (the existing rule-2 bar) running each of the four
  browsers; mobile = a ~3-year-old mainstream phone per OS (mid-range Android
  for Chrome, the iPhone of that vintage for Safari) — if the median phone
  holds 60, the fleet does.
- On approval of this plan, `AGENTS.md` iron rule 2 is amended in the same
  commit to read "60 fps in the popular browsers on desktop (Chrome, Safari,
  Edge, Firefox) **and mobile (Chrome, Safari) reference devices**", so every
  future agent inherits the guardrail from onboarding.

## 0. Why this plan exists

The app's architecture is already strong: 3-tier LOD with hysteresis, worker-pool
geometry building, one `BatchedMesh` for the whole building kit, instanced
agents, dithered cross-fades, zero per-frame allocation, four quality tiers.
None of that is being reworked. What's missing is:

1. **Nothing adapts at runtime.** Quality is guessed once at boot
   (`main.js`: `devicePixelRatio > 1.9 || innerWidth < 900 → medium`) and never
   corrects itself. Devices that can't hold 60 fps just don't, forever — and
   Retina desktops that could run Ultra boot at Medium.
2. **Mobile is unsupported.** No pinch/rotate/tilt gestures (wheel-only zoom,
   right-drag orbit), no WebGL context-loss recovery, unbounded caches on a
   platform that kills hungry tabs.
3. **Scale is arriving faster than governance.** The landmark wave has started
   (6 manifest assets, 19 asset plans + 10 park plans committed); the loader
   still loads every manifest GLB eagerly at up to 2 draw calls each, forever.
   At ~300 landmarks that alone is ~600 draw calls — double the entire budget.
   Meanwhile new systems land weekly (street furniture: up to +30 draw calls,
   no quality hooks) with nothing machine-checking the budget.

## 1. Metrics (the scoreboard)

All estimates below get verified against these by workstream #0's harness.

| Metric | Definition | Baseline (measured/estimated Aug 2026) | Target |
|---|---|---|---|
| **M1 frame rate** | fps at street level in the Mission and downtown stress cells, day and night, across the guardrail browser matrix (see THE GUARDRAIL) | 60 in Chrome on modern desktop; other browsers unmeasured; est. 20–40 on phones / weak laptops | **60 on desktop (Chrome, Safari, Edge, Firefox) AND mobile (Chrome, Safari)**; governor may lower the visual tier, never the frame rate |
| **M2 time to full city** | transfer size + wall time until `tiles ≈ total` on 4G | ~57 MB uncompressed (96 MB tiles on disk, toy tier ~32 MB streamed + 25 MB sf-assets); est. 40–60 s on 4G | ≤ ~19 MB, 12–18 s |
| **M3 mobile session survival** | behavior on GL context loss / memory pressure | permanent freeze; caches grow unboundedly (tile blobs ~30–50 MB, kit geometries, streetkit context cells) | auto-recovery ≤ 2 s; bounded memory |
| **M4 draw calls** | worst case at stress views (iron-rule budget < 300) | ~100–150 today; **~700 projected at 300 eagerly-loaded landmarks** | < 300 at any landmark count |
| **M5 mobile usability** | can a touch user pan / zoom / rotate / tilt | pan only | full navigation parity |

Verified facts behind the baseline: production serves `/tiles/**/*.bin` with
**no** `content-encoding` even when the client offers `br, gzip` (checked
against sf-3d.vercel.app); GLBs ship without meshopt/Draco (kit 15 MB,
landmarks 6.1 MB, vehicles 2.8 MB); `assets.js` loads every manifest entry
after first paint and keeps all of them resident; `blobCache` in `city.js` and
the streetkit context-cell cache never evict; `index.html` sets
`user-scalable=no` and `camera.js` has no touch gestures; no
`webglcontextlost` handler exists anywhere in `app/src`.

## 2. Ranked workstreams

Execution order = rank order, except #0 ships first and #2/#3 may run in
parallel with #1 (they touch disjoint files).

---

### #0 — Measurement harness (ships first; everything else is graded by it)

*Plain English: a smoke detector. Before and after every change, a script flies
the camera to the busiest spots and records fps, draw calls and load time, so
every claim in this plan becomes a number and no future PR can silently spend
the budget.*

- Runs against BOTH guardrail profiles: desktop, and the mobile reference
  device (real device where available, else documented CPU/GPU-throttled
  emulation) — a run without the mobile numbers is incomplete. The scripted
  fast path targets Chrome; the skill documents the manual `window.SF` recipe
  for the Safari / Edge / Firefox sweep (per-release, and after any
  shader/render-loop/post change), since those can't be driven headlessly the
  same way.
- A script (Node + headless Chrome, or a documented manual recipe using
  `window.SF`) that visits: hero view, Mission street level, downtown street
  level, Golden Gate — each at day and night — and records
  `renderer.info.render.calls`, real frame cadence (rAF deltas, NOT the overlay
  fps — see `.agents/skills/testing-sf-3d/SKILL.md` on why), triangle count,
  JS heap, and time-to-N-tiles on a throttled connection.
- Output: one JSON + console table per run, committed under `artifacts/perf/`
  per release (small files only).
- Wire into the QA norms: the deploy report's PASS/FAIL table includes the
  harness numbers. Add the recipe to `.agents/skills/testing-sf-3d/SKILL.md`.
- Files: new `pipeline/perf-harness.mjs` (or `scripts/`), skill update.
  No app code changes.

**Acceptance:** two consecutive runs on the same build agree within noise;
the numbers for today's main are recorded as the canonical baseline.

---

### #1 — Adaptive quality governor (biggest M1 lever)

*Plain English: an autopilot. The app watches its own smoothness every second
and turns settings down (or back up) to hold 60 fps — like streaming video
adjusting to your internet. Strong machines drift up to Ultra; weak phones
drift down until they're smooth. The Quality dropdown becomes a manual
override.*

- New module `app/src/governor.js`: keeps an EMA of real frame time (wall-time
  rAF deltas). If sustained > ~19 ms, step down one rung; if sustained
  < ~12 ms for ~10 s, step up one rung. Hysteresis + cooldown so it never
  oscillates; never adapts during camera fly-tos or while tiles are still
  streaming (loading ≠ rendering slow).
- The rungs are the existing `QUALITY` tiers first (pixelRatio → shadow →
  nearScale/treeScale → windows), extended by #6's finer levers later.
- HUD: quality select gains an "Auto" default entry; choosing a named tier
  pins it (governor off). Persist the pin in `localStorage`.
- `window.SF.governor` exposes state for the harness and QA.
- Files: new `governor.js`; `main.js` (wire + remove the one-shot boot
  heuristic's finality); `ui.js` (Auto entry).

**Estimated impact:** devices below budget go from est. 25–40 fps to a held
55–60 (resolution step High→Medium alone cuts pixel work ~2.25×; shadows-off
is another ~30–40%). Desktop at 60 fps sees no change except Retina machines
drifting UP to their true tier.

**Acceptance (harness):** on the mobile reference profile AND a CPU-throttled
desktop profile the governor settles within 30 s and the settled fps meets the
guardrail (60, ≥ 55 tolerated as measurement noise) at both stress cells; no
tier oscillation over 5 minutes; manual pin is respected across reloads.

---

### #2 — Touch navigation (gates the entire mobile audience)

*Plain English: on a phone today you can drag the map and nothing else. This
adds what everyone expects from a maps app: pinch to zoom, two-finger twist to
rotate, two-finger drag to tilt.*

- `camera.js`: track active pointers by `pointerId` (the rig already uses
  Pointer Events, so no separate touch path). One pointer = existing grab-pan.
  Two pointers: pinch distance ratio → `distance` (zoom toward the midpoint's
  ground point, reusing the wheel handler's zoom-to-cursor logic); twist angle
  → yaw; average vertical travel → pitch. Respect the diorama rig's existing
  pitch coupling and clamps.
- Keep `touch-action: none` on the canvas so the browser never steals the
  gesture; leave page-level `user-scalable=no` as is.
- No behavior change for mouse users. Ship with a QA recording on a real
  phone (or at minimum DevTools touch emulation for each gesture).
- Files: `camera.js` only (plus `style.css` if `touch-action` isn't set).

**Estimated impact:** M5 goes from "pan only" to full parity — this is the
difference between having and not having a mobile product. No fps effect.

**Acceptance:** on a touch device: pinch zooms toward fingers, twist rotates,
two-finger drag tilts, one-finger pans, tap still picks (the existing
moved>6px / held>400ms guard must still suppress accidental picks).

---

### #3 — Landmark streaming & batching (removes the 300-landmark cliff)

*Plain English: today every hand-made landmark is downloaded at boot and kept
at full detail forever. Perfect at 6 landmarks; at the planned ~300 it doubles
our entire rendering budget and adds 25–50 MB to page load. Landmarks should
work like buildings already do: full detail near the camera, the baked stand-in
far away. Doing it now means the 19 landmark integrations already specced
inherit it for free.*

- `assets.js` gains distance-based lifecycle, reusing the exact hysteresis
  pattern from `city.js` (enter/exit radii, dithered fade via the existing
  loader-merged materials):
  - **Far:** the GLB is not loaded (or is unloaded); the baked/procedural
    version stays visible — rule 3's fallback IS the far LOD, so there is
    never a hole. Bridges and skyline-scale landmarks (Golden Gate, Salesforce,
    Transamerica…) are flagged `alwaysLoaded` in the manifest — they are the
    skyline and must never swap.
  - **Near:** GLB fetched (browser-cached thereafter), merged as today,
    cross-faded in; the code-built version hidden as today.
- Batching: merged landmark bodies within a streaming cell share one
  vertex-color Lambert; fold bodies into per-area static batches or a landmark
  `BatchedMesh` (same pattern as `kitfleet.js`) so N near landmarks cost O(1)
  draws, not 2N. Glow sets likewise.
- Manifest schema addition: `alwaysLoaded: bool`, optional `loadRadius`.
  Default radius chosen so today's 6 landmarks behave exactly as now.
- Fallback drill per AGENTS.md: rename a GLB → baked version persists,
  one warning.
- Files: `assets.js`, `landmarks_manifest.json` (schema), possibly a small
  new `assetfleet.js` if BatchedMesh is chosen; `PILOT-ASSET-PROMPT.md` /
  landmark integration prompt updated to document the new manifest fields.

**Estimated impact:** M4 at 300 landmarks: ~700 → < 150 draw calls. M2: boot
downloads stop growing with the library (today +6.1 MB and climbing;
projected +25–50 MB avoided). At the current 6 landmarks: no visible change.

**Acceptance (harness):** with a synthetic manifest of 100 dummy entries
pointing at existing GLBs, draw calls at the hero view stay < 300 and boot
network stays within 2 MB of the 6-landmark baseline; flying to any dummy
landmark swaps it in without a hole or pop.

---

### #4 — Compress delivery: tiles + GLBs (biggest M2 lever)

*Plain English: the city's map data and 3D models are shipped unzipped. Zipping
them in the bake and compressing the models makes the first visit ~3× faster,
especially on cellular — and every future asset ships cheaper.*

- **Tiles:** pipeline writes gzip-compressed `.bin` (or `.bin.gz` alongside);
  the tile worker inflates with the native `DecompressionStream` API before
  parsing (zero new dependencies — rule 4 safe; it's a web platform API).
  Float32 tile data typically compresses 2.5–3×. Alternative worth a spike in
  the same PR: quantize positions/normals to int16 in the bake (lossless at
  toy scale) for ~2× before compression even starts.
- **GLBs:** run gltfpack/meshopt over `sf-assets/**` in a pipeline script
  (`three` already ships the `MeshoptDecoder` addon — no new runtime
  dependency). Kit 15 MB + landmarks 6.1 MB + vehicles 2.8 MB → est. 5–8 MB
  total. The asset intake skill gains a "compressed on ship" step; source GLBs
  stay uncompressed in authoring.
- Keep `Cache-Control: immutable` semantics; the bake-timestamp cache key from
  `data.js` already busts correctly.
- Files: `pipeline/` (bake output + a compress script), `city.worker.js` /
  `tilebin.js` (inflate), `kitassets.js`/`assets.js`/`agents.js` loaders
  (meshopt decoder wiring), `.agents/skills/sf-asset-check/SKILL.md`.

**Estimated impact:** M2 first-visit transfer ~57 MB → ~16–19 MB; 4G full-city
time est. 40–60 s → 12–18 s. No runtime fps change (decompression happens in
workers, off the render thread).

**Acceptance (harness):** byte-identical parsed geometry vs. uncompressed
tiles (checksum in the worker during the spike); Network panel shows the
reduced totals; cold-load time on a throttled "Fast 4G" profile hits target;
fallback drill — a missing compressed file degrades per rule 3.

---

### #5 — Mobile survival: context-loss recovery + bounded memory

*Plain English: phone browsers sometimes confiscate a page's 3D engine (e.g.
switching apps and back). Today that permanently freezes the city. Recover
automatically — and stop holding onto data we no longer need, which is what
gets the page killed in the first place.*

- `webglcontextlost` (preventDefault) + `webglcontextrestored` on the canvas:
  on restore, re-upload static resources and let the streaming loop rebuild
  the tiers; show the toy-theme loader during the 1–2 s rebuild. Pause the
  rAF loop and ferry polling on `visibilitychange: hidden`.
- Bound the caches (all three verified unbounded today):
  - `city.js blobCache`: LRU-cap (~200 blobs); tiles are `immutable`-cached by
    the browser, so eviction costs one near-free refetch.
  - `kitassets.js ready` map: release merged piece geometry when no loaded
    chunk references the piece (refcount from `kitfleet`).
  - `streetkit.js cells` context-hint cache: evict with the same LRU.
- Files: `main.js` (context handlers, visibility), `city.js`, `kitassets.js`,
  `kitfleet.js` (refcount), `streetkit.js`.

**Estimated impact:** M3: −30–60 MB steady-state heap on long sessions;
context loss goes from permanent freeze to ≤ 2 s auto-recovery. Indirectly
reduces the iOS tab-kill rate (less memory pressure).

**Acceptance:** DevTools "lose context" extension test recovers to an
interactive city ≤ 2 s; 10-minute fly-around shows a heap plateau (the
testing skill already documents the plateau recipe); fallback drill intact.

---

### #6 — Universal quality levers (every subsystem answers to the governor)

*Plain English: several systems always run at full blast no matter the quality
setting — the water sparkle, the cloud shadows, the 720 cars, and the new
street furniture (15 types, up to ~30 draw calls). Give every system a
standard "turn down" knob the autopilot can pull, and require the same knob
from every future feature.*

- Define one convention: every visual subsystem exposes
  `setQuality(tier /* 'ultra'|'high'|'medium'|'low' */)`. The governor (#1)
  fans out to all of them; `QUALITY` tiers in `ui.js` become the single table
  of what each tier means.
- Initial levers (each individually small):
  - **water.js:** low tier = 1 noise octave instead of 3, specular power
    220 → ~48 (also fixes mediump shimmer on mobile GPUs), fresnel kept.
  - **materials.js:** low tier = cloud-shadow noise off (flat cover term),
    single-hash window ignition.
  - **agents.js:** low tier ≈ half counts (cars 720→320, peds 420→160,
    birds 90→45) — pools are fixed-size, so this is a live-instance cap,
    not a rebuild.
  - **streetkit.js:** medium = drop the "clutter" classes (newsboxes,
    bikerack, planter…); low = lamps + signals only. Capacity caps scale.
  - **terrain.js:** medium/low = 256-per-quadrant index buffer (half
    resolution; same heightmap, swap is an index buffer, not a rebake).
- Document the convention in `AGENTS.md` (one line under iron rule 2) so
  every future feature PR ships its lever.
- Files: the five modules above, `governor.js`/`main.js` fan-out, `ui.js`
  tier table, `AGENTS.md`.

**Estimated impact:** M1 on low-tier devices: −10–25% GPU frame time
(view-dependent; largest in bay-heavy views) plus ~1–2 ms/frame CPU from agent
caps; M4: street-level draw-call creep capped instead of growing with every
feature. On High/Ultra: zero visual change.

**Acceptance (harness):** low tier at both stress cells shows the frame-time
drop vs. #1-only; screenshots at High are pixel-identical to before this
workstream.

---

### #7 — Anti-aliasing correction (small, strictly positive)

*Plain English: we currently pay for edge-smoothing on a buffer the diorama
never shows, and the image we DO show gets no smoothing. Move it to the right
place: crisper picture, slightly cheaper.*

- `toypost.js`: create the render target with `samples: 4` (WebGL2 MSAA);
  `main.js`: construct the renderer with `antialias: false` (post is always
  on in the shipped diorama mode). Governor may drop samples 4→2→0 as a rung.
- Files: `toypost.js`, `main.js`.

**Estimated impact:** M1 −0–5%; GPU memory back from the unused canvas MSAA
buffer; visibly crisper edges (QA screenshots will show it).

**Acceptance:** screenshot diff shows smoother building edges; harness shows
frame time ≤ baseline.

---

### #8 — Smarter startup guess (polish once #1 exists)

*Plain English: the current first guess demotes every high-resolution screen —
so new MacBooks boot at Medium while old low-res laptops boot at High. Make a
better first guess; the autopilot fixes the rest within seconds.*

- Replace the boot heuristic: coarse pointer / `maxTouchPoints` → start
  medium-low on mobile; `WEBGL_debug_renderer_info` GPU string heuristics for
  the desktop tier; screen resolution alone never demotes.
- Files: `main.js` (or fold into `governor.js`).

**Estimated impact:** first-seconds experience only (the governor converges
regardless): Retina desktops boot High/Ultra; low-end phones skip the
30-seconds-of-jank before the governor's first correction.

---

### #9 — Asset budget rules in intake (insurance)

*Plain English: add hard size/complexity limits to the asset checklist so every
new model "pays its way", and the intake skill rejects what would break the
budget — the same way it already rejects wrong materials.*

- `.agents/skills/sf-asset-check/SKILL.md` gains numeric gates: max tris per
  landmark (proposed: 30k standard / 60k `alwaysLoaded` skyline pieces — the
  ferry's 27k is the current high-water mark), max compressed file size
  (proposed 500 KB standard), mandatory meshopt step (#4), mandatory manifest
  `loadRadius`/`alwaysLoaded` decision (#3).
- Files: skill doc only. Numbers to be confirmed against #0's baseline data.

---

## 3. What this plan deliberately does NOT do

- No rewrite of the LOD/streaming core, materials system, or agents — they are
  the good part.
- No new runtime dependencies beyond `three`'s own addons (meshopt decoder);
  no paid services (rule 4); no data simplification (rule 5).
- No visual change at High/Ultra on capable hardware: the diorama look on a
  good machine is pixel-identical after every workstream except #7 (which
  makes it crisper).

## 4. QA norms

Every workstream lands with: harness numbers before/after (from #0) **on both
guardrail profiles — desktop and the mobile reference device**, the standard
deployed-site screenshot QA from `AGENTS.md`, the fallback drill where loaders
were touched, and PASS/FAIL per its acceptance list with the production URL
first — honest FAILs welcome, hidden ones not. A change that holds 60 fps in
desktop Chrome but drops any browser in the guardrail matrix (desktop Chrome /
Safari / Edge / Firefox, mobile Chrome / Safari) below 60 is a FAIL (see THE
GUARDRAIL). Workstreams that touch shaders, the render loop, or the post
pipeline (#1, #4, #6, #7) additionally run the full browser sweep before
merging, not just the Chrome fast path.
