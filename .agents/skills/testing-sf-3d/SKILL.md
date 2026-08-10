---
name: testing-sf-3d
description: How to test the SF 3D WebGL city app (app/ Vite + three.js, baked tiles in app/public/tiles) locally or on a Vercel deployment, including control bindings, the debug overlay, and known environment limits of the Devin browser.
---

# Testing the SF 3D city app

## What the app is
- Static Vite app in `app/`, three.js renderer, no backend. All geometry comes from pre-baked binary
  tiles in `app/public/tiles` (`manifest.json` + `buildings/`, `streets/`, `landcover/`, `terrain.bin`).
- `vercel.json` at the repo root sets `buildCommand: cd app && npm install && npm run build`,
  `outputDirectory: app/dist`, and `Cache-Control: public, max-age=31536000, immutable` for
  `/tiles/*` and `/assets/*`. Verify those headers with `curl -sSI <host>/tiles/manifest.json`.

## Running locally
```
cd app && npm install && npm run dev      # or: npm run build && npx vite preview
```
No env vars or secrets are required. **Devin Secrets Needed:** none.

## Reaching the features (traced in code)
- Number keys fly to presets/landmarks (`app/src/main.js` keydown handler); the mapping lives in
  `app/public/tiles/manifest.json` (`viewPresets[].key`, `landmarks[].key`): `0` hero, `1` Golden Gate
  Bridge, `2` Bay Bridge, `3` Salesforce Tower, `4` Transamerica, `5` Coit, `6` Sutro, `7` Ferry
  Building, `8` Palace of Fine Arts, `9` City Hall. `H` returns home.
- Camera (`app/src/camera.js`): WASD/arrows pan, `Q`/`E` rotate, `R`/`F` or PageUp/PageDown zoom,
  wheel zooms toward the cursor, right-drag orbits (pitch+yaw), left-drag grab-pans, screen edges scroll,
  Shift boosts.
- HUD (`app/src/ui.js`): View select, "Golden hour → dusk" range slider (0–1000) with an auto checkbox,
  Quality select (Ultra/High/Medium/Low), and a `stats` button; `F3` or backtick also toggles the overlay.
  Low sets `shadow: 0` and `windows: 0`, so switching to Low must visibly drop shadows and night windows.
- Time: `env.js setTime(t)` ramps `uNight` from `t = 0.36`, which drives window ignition, lamps and
  bridge lights. Auto mode sweeps 0→1 in ~180 s, so the scene is still golden-hour for the first ~60 s.
- `window.SF` is exposed for automated checks: `SF.rig.state` (`pivot`, `yaw`, `pitch`, `distance`),
  `SF.city.stats`, `SF.agents.carCount`, `SF.setTime(t)`, `SF.goTo(lon, lat)`, `SF.pick(nx, ny)`.
  Prefer real UI interaction for the recording and use `SF.rig.state` only as numeric corroboration.

## Gotchas in the Devin browser environment
- Chrome here runs `--use-angle=swiftshader-webgl --disable-gpu` (software rasterizer): expect ~20 fps
  and 40–90 s before all ~1650 tiles finish streaming. Always wait for `tiles X/1657` to approach the
  total in the stats overlay before judging a frame; a sparse city usually just means "still loading".
- The renderer tab can die (blank/closed tab, `Browser action failed`) after ~15 min of heavy
  software-GL use. Check `curl -s http://127.0.0.1:29229/json/list` for the page; if it is gone,
  restart the browser and re-navigate. Keep each recorded run short and avoid Ultra quality when possible.
- `browser(action="scroll")` does NOT reach the canvas `wheel` handler. Use real X11 wheel clicks:
  `xdotool mousemove <x> <y>; xdotool click 4` (zoom in) / `click 5` (zoom out).
- For held drags (orbit/pan), use `xdotool mousemove X Y mousedown 3 ... mousemove_relative ... mouseup 3`
  and screenshot while the button is still held.
- Dragging the range slider with xdotool proved unreliable; `browser(action="click", coordinates="x,y")`
  on the slider track works and fires `input` (which also unchecks the auto checkbox). Slider coordinates
  in the 1024x768 tool space are roughly x 905 (0%) → 988 (100%) at y 48 when the window is 1600x1122.
- The window manager does not support `_NET_CLIENT_LIST`, so `wmctrl -r :ACTIVE:` fails; Chrome is
  already started maximized at the full screen size, so no manual maximizing is needed.
- `/favicon.ico` is served by a `vercel.json` rewrite to `/favicon.svg`, so it is 200 with
  `max-age=0, must-revalidate` (not immutable) — do not assert immutable caching on it.

## Proving animation
Take two screenshots ~5 s apart at an unchanged camera (e.g. preset `7` Ferry Building) and diff crops
with PIL; cars along the Embarcadero and boats/ferries on the bay should shift. A pixel diff of the whole
frame is not enough on its own because the water shader animates every frame.
Under software GL only ~2–5 frames render in 10 s, so allow 12–15 s between frames and accept small
diff counts (a few hundred changed pixels) as motion.

## Synthetic vs real input (important)
- Synthetic `KeyboardEvent` works only for handlers that read `event.code` (camera pan/rotate in
  `camera.js`). Handlers that read `event.key` — the backtick overlay toggle in `ui.js`, and `H`/number
  presets in `main.js` — are **missed** unless you set `key` too. Prefer real keys:
  `export DISPLAY=:0; xdotool key h` / `key 1` / `key grave` / `key F3`.
- `DISPLAY` may be unset in fresh shells and `:1` does not exist; use `:0` (`ls /tmp/.X11-unix` to confirm).
  `xdotool getactivewindow` fails (no `_NET_ACTIVE_WINDOW`) but `mousemove`/`key`/`click` still work.
- `import -window root` captures can lag the live canvas, so a pixel diff may show "no change" even when
  the UI did change. For UI toggles, assert on DOM state via console (e.g.
  `document.getElementById('debug').hidden`) rather than pixels.
- Middle-drag also orbits (`camera.js` maps right OR middle button to rotate).

## Measuring instead of trusting the overlay
- The overlay `fps` field can read a constant `20` while the renderer actually draws 0.1–0.4 frames/sec.
  Measure real cadence from deltas of `SF.renderer.info.render.frame` (or a rAF counter) over ~10 s and
  report both numbers; never quote overlay fps as measured performance.
- Long async probes: assign results to `window.__x` inside an async IIFE and read them back on a later
  console call — console evaluation does not await promises.
- Because only 2–3 frames elapse per key-hold, ratio-based control assertions (e.g. Shift boost ≈3.4×)
  are unreliable; zoom-scaled pan speed (≥10× between distance 9000 and 150) still resolves cleanly.

## Geometry/continuity probing recipes
- Landmark screen position: traverse `SF.scene` for the named object, build its world bbox centre, then
  `v.project(SF.camera)` → pixels. Note `getWorldPosition` returns the origin for landmark groups whose
  geometry carries the offset, so use the bbox.
- Deck-vs-ground continuity and freeway elevation: `SF.goTo(lon, lat, 600, 0, 88)` (near top-down) then
  `SF.pick(0, 0)`; compare the y of the street hit (`near-*`/`far-*`) against the `terrain-*`/`ground-*`
  hit. A large positive delta means an elevated deck; a `water` hit with no terrain means it ends mid-bay.
- Zoom-to-cursor tests: the wheel handler picks the **terrain** under the pointer, not buildings, so a ray
  through a tower's pixel continues to the ground far behind it — aim at the target's base, and expect the
  pivot to converge only partially (it may end >1 km away; verify with pivot-to-landmark distance in metres).

## Known findings to re-check rather than re-discover
Audited on the re-baked local build: bridge deck ends do not meet land (Golden Gate both ends, Bay Bridge
both ends), the camera has no building collision (only a terrain floor clamp, so low `distance` values put
it inside meshes), grab-pan slips tens of metres, freeway decks float without piers while some freeways are
flat on the ground, and cloud shadows are absent. Memory does **not** leak (geometries/heap plateau).
These may still be open; probe them first before assuming regressions elsewhere.

## Measuring geometry numerically (bridges, freeways, piers)

The reliable recipe for "does structure X sit at the right height above the ground?" is a near-top-down
pick, comparing hit heights:

```js
SF.goTo(lon, lat, 600, 0, 88);            // or SF.rig.set({x, z, distance:600, yaw:0, pitch:88})
await new Promise(r => setTimeout(r, 3000)); // tiles must stream in first
SF.pick(0, 0).map(h => h.name + '@' + h.point[1]);
```
Hit names identify the layer: `terrain-*` (base terrain), `ground-*`/`near-*`/`far-*` (street ribbons at
different LODs), `water`, `viaductPiers`, `goldenGateBridge`/`bayBridge` (bespoke decks). A `water` hit with
no `terrain-*` hit means the structure ends over open water.

Do not trust `manifest.piers.length` or `SF.piers.count` alone — an `InstancedMesh` would report the same
count with zero-scale or buried instances. Read the actual matrices instead:

```js
const m = SF.piers.mesh, M = new (Object.getPrototypeOf(m.matrixWorld).constructor)();
m.getMatrixAt(i, M); const e = M.elements;
const x = e[12], z = e[14], height = e[5], groundY = e[13] - height / 2;
```
Then pick at each `(x, z)` and confirm the street ribbon lands at `groundY + height` and the terrain at
`groundY`. Also take one low oblique shot (`distance` 220–300, `pitch` 6–10°) so the columns are proven in
pixels, not just in numbers.

## Real-input coordinate calibration (do this before any xdotool test)

The page origin is offset from the X11 screen origin (on a 1600×1122 window it was **+87 px in y**, and the
bottom of the page including the attribution is off-screen). Never assume page coords == screen coords:

```js
window.__last = null;
addEventListener('pointermove', e => { window.__last = {cx:e.clientX, cy:e.clientY, sy:e.screenY}; }, true);
```
then `xdotool mousemove 800 400` and read `__last` — the delta is your offset. Also avoid parking the cursor
within ~22 px of a window edge during wheel/drag tests: **edge scrolling** kicks in and confounds the result.

## Testing zoom-to-cursor and grab-pan quantitatively

- Zoom-to-cursor toward a landmark: build the landmark's **world bounding-box centre** (its group origin is
  not its geometry centre), project it with `SF.camera` to get the pixel, `xdotool mousemove` there, wheel in
  with `xdotool click 4`, then measure `hypot(pivot.x - target.x, pivot.z - target.z)`. Re-aim the cursor
  every 2 clicks — the target moves on screen as the camera closes, and a fixed cursor legitimately aims at
  whatever is under it now. Expect asymptotic convergence (each step roughly halves the distance); the target
  can drift off-screen before you reach a tight threshold.
- Grab-pan retention: pick the ground point under the press pixel, do a held drag with
  `xdotool mousedown 1` / `mousemove_relative` / `mouseup 1`, then pick at the release pixel and compare the
  two world points. Test both a single step and a multi-step drag — accumulation errors only show in the latter.

## Frame-rate-dependent effects are unmeasurable under SwiftShader

The render loop clamps simulation `dt` to 0.05 s. Anything advanced by that clamped `dt` (e.g. cloud drift in
`env.js updateClouds`) progresses at real speed only above 20 fps; at the 0.3–1.0 fps this environment
delivers, ~20 s of wall clock yields under 1 s of simulated motion. A two-screenshot diff will therefore show
near-zero change even when the feature works. To distinguish "absent" from "too slow here":
- prove the effect **exists** by toggling its uniform and diffing (materials expose `material.uniformsHolder`,
  which holds live references to the shared uniforms, e.g. `uCloudCover`, `uCloudDrift`, `uNight`);
- prove the **response** through a user-facing path (`SF.setTime(1)` drops `uCloudCover` to 0.32 × 0.15 = 0.048);
- label the motion check UNTESTED rather than FAIL, and note the clamped-dt coupling as a real (if minor) bug.

The debug overlay's fps is rounded to an integer, so sub-1 fps shows as `0` or `1`; compare it against
`SF.renderer.info.render.frame` deltas over ~10 s rather than expecting a decimal.

## Vercel `ERR_ABORTED` tile requests are not 404s

On a cache-cleared production load the tile streamer legitimately cancels in-flight fetches via
`AbortController` as the camera moves, so CDP `Network.loadingFailed` can report 20+
`net::ERR_ABORTED` entries for `tiles/**` and the app logs `tile group failed <cell> TypeError: Failed
to fetch` / `near chunk failed <cell>`. Do **not** report these as missing tiles. Distinguish them by
also collecting `Network.responseReceived` and counting only `status >= 400`; a clean deploy shows
`HTTP >= 400 (0)` alongside the aborts, with `window.__errs` empty and `cellsLoaded` still climbing to
its plateau.

## Deployment caching gotcha

`/tiles/manifest.json` is served `public, max-age=31536000, immutable` under a **non-hashed** name. After a
redeploy, a browser that visited before keeps the old manifest and silently renders old data (e.g.
`SF.piers.count === 0` with the previous bridge geometry). Always hard-reload
(`xdotool key ctrl+shift+r`) before verifying deployed data changes, and check
`performance.getEntriesByType('resource')` for the manifest's `transferSize`/`encodedBodySize` to tell a cache
hit from a fresh fetch. Worth flagging as a product bug, not just a test workaround.

## Testing the lore / context layer (context cards, search, toy props, night sky)

Runtime handles: `SF.context`, `SF.pickEntity(nx,ny)`, `SF.select(e)`, `SF.focus`, `SF.search(q)`,
`SF.setTime(t)`, `SF.setStyle('toy'|'base')`. Note `SF.env` is **not** exposed — reach the night-sky kit
by traversing the scene instead (see below).

### Keyboard focus steals the single-letter shortcuts
After typing in the search box (`/`), the input keeps focus, so `M`/`Q`/`E`/`F3` go to the input and
nothing happens (`SF.style` stays unchanged). Click the canvas once (or press Escape) before sending
single-letter keys. Verify with `SF.style` rather than assuming the keypress landed.

### The time slider is easiest to drive with the keyboard
`input[type=range]` (0..1000). Click it once, then `xdotool key End` for full night and `Home` for
day — clicking the track only jumps part-way and dragging is flaky. Clicking it also unchecks "auto".

Two things that repeatedly cost time here (re-measure, do not assume the exact number):
- **X11 clicks need a Y offset relative to page coordinates.** With the 1600×1122 Chrome window used in
  this environment the browser chrome adds about **+88 px in y**, so `xdotool mousemove <rect.x> <rect.y>`
  computed from `getBoundingClientRect()` lands above the element and the click silently does nothing
  (e.g. the "Golden hour → dusk" auto checkbox stays checked and daylight shots drift to dusk mid-run).
  Calibrate first with a `pointermove` listener (see "Real-input coordinate calibration") or by locating
  the widget in an `import -window root` screenshot, then add the measured offset to every click.
- **`Home` does not always reset the time slider.** On some builds only `End` (night) is honoured while
  `Home` leaves `input[type=range].value` unchanged; verify the value after the keypress and, if it did
  not move, click near the left end of the slider track instead. Always assert on the slider's `value`
  (and `input[type=checkbox].checked` for auto-advance) rather than assuming the key landed.

### Probing traffic / agents (app/src/agents.js)
`SF.agents` only exposes `group`, `update`, `setToy` and `carCount`, so per-car state is not reachable
from the console. Two ways in:
- Read world positions out of the vehicle `InstancedMesh`es: `SF.agents.group.children` contains
  `vehicle-<id>` meshes (one per fleet GLB, `carMesh` is hidden once the fleet loads). Instance `i`'s
  position is `matrix.elements[12/13/14]` via `mesh.getMatrixAt(i, m)`; `mesh.count` is the live count.
  Good enough for "are there cars here" and for height-above-deck checks.
- Individual-car tracking (does a car actually traverse?) needs a temporary one-line instrumentation such
  as `window.__cars = cars;` inside `createAgents`, then sample `__cars[i].d` / `.path.meta.total` over
  time. Back the file up, restore it afterwards, and disclose it in the report.
Height gotcha worth checking on any traffic change: bridge deck cars are placed at
`manifest.bridges.*.nodes[i][2] + 0.35 + 0.2`, while the procedural deck box in `landmarks.js deckRibbon`
is centred on the node y with thickness 2.6 (top = node y + 1.3) and the Golden Gate GLB deck is level at
~67.2 m. So cars can legitimately end up sunk into or floating above a deck — measure the gap with a
downward raycast at several points along the span before calling it fine.

#### Measuring "do cars sit ON the deck?" correctly
A naive downward ray from `carY + 60` takes the **first** bridge hit, which is often a tower crossbeam,
suspender or hanger *above* the deck — that produced spurious gaps of −25 m and −15 m. Two fixes:
- filter the bridge hits to `h.point.y <= carY + 0.4` and take the highest remaining one;
- confirm what the surface actually is with a **deck cross-section**: take two adjacent manifest nodes,
  compute the perpendicular `(-dz, dx)/L`, and raycast down at lateral offsets −16…+16 m, reporting
  `hitY - nodeY`. If the top surface is a constant `nodeY + 1.3` across the whole `deckWidth`, that is
  the procedural `deckRibbon` roadway, so cars placed at `nodeY + 0.55` are genuinely embedded 0.75 m.
Also read the vehicle geometry's bounding box (`mesh.geometry.boundingBox.min.y ≈ 0`) to establish that
the models are **base-origin** — without that, a 0.75 m offset cannot be called "sunk" vs "centred".
Visually a 0.75 m sink on a ~1.9 m car reads as "missing wheels / bottom flush with the road", not as an
obvious hole, so the numbers matter more than the screenshot here.

#### Whole-span coverage without trusting the code
Project every `vehicle-*` instance onto the manifest deck polyline, keep those within ~20 m of the
centreline, and bucket by arc length into thirds. Cars are only simulated within `CAR_RANGE * 1.6` of the
camera, so frame the **whole** span (`SF.goTo(<mid lon>, <mid lat>, 3000, 150, 42)`) before counting, or
the far third will read empty for purely environmental reasons.
For the best visual proof of on-deck traffic, aim at the deck's own mid node rather than a hand-picked
lon/lat: `nodes[Math.floor(nodes.length/2)]` at `distance 600–800` — hand-guessed coordinates frequently
frame open water beside the span.

#### Probe pitfall: reset your own globals after every reload
If a probe selects its target deck from a `window.__deck` global, a page reload clears it and the probe
silently measures the default deck (e.g. the Bay Bridge east span while the camera is at the Golden
Gate), reporting a false `onDeck: 0`. Re-set such globals immediately after each navigation/reload and
echo the deck name in the probe's own output so a mismatch is visible.

### Verifying toy props (app/src/props.js) without a GPU-quality screenshot
The 42° locked diorama pitch plus 150 m zoom clamp means street-level props (retail awnings, fire-station
bay doors) are often occluded by the mass or a neighbour, and golden-hour shading leaves the street face
dark. Corroborate numerically, then hunt for a view:
- Every toy mesh carries `aFlag` (`flag = profile*4 + glowProp*2 + suppressBands`). **Bit 0 is
  `suppressBands`, not "is a prop"** — do not report it as a prop count.
- Prop recipes use exact literal colours, and the merged geometry stores them unconverted in the `color`
  attribute, so you can find a specific prop by colour match (±2): fire-station bay door `188,62,52`,
  its apron plate `118,116,114`, gas canopy `236,232,222` / lit slab `255,250,236`, pumps `214,74,66`,
  retail awning is one of `214,90,74 / 64,132,132 / 226,176,70 / 92,106,168`, blade sign `250,248,244`.
  Walk the scene, apply `matrixWorld` manually, filter to the target's `SF.focus.x/z`, and check the world
  Y range against the recipe (e.g. apron at `base+0.06`, bay doors `base+0.2..4.4`) to prove the prop is
  *attached* at grade/roof rather than floating.
- Cluster the matches on a ~60 m grid to find *other* instances of the same category, then convert to
  lon/lat (`lon = -122.4375 + x/87995.768`, `lat = 37.77 - z/110540`) and fly there. Wide-street districts
  (SoMa) give a far more legible screenshot than dense hills (Nob Hill).
- Project the matched vertices with `SF.camera` to get the exact pixel box, then crop the root screenshot
  to it — otherwise a 4 m prop is invisible in a 1600 px frame.

### Night sky kit
`createEnvironment` must export `updateNightSky` (the frame loop calls it every frame); if it is missing
the whole render loop throws and the canvas goes black — a good smoke test after any env.js change.
The objects are unnamed, so identify them by shape: moon = `Mesh` with `IcosahedronGeometry`,
halo = `PlaneGeometry` 4200×4200 additive, stars = `Points` with 2000 positions. All three appear only
once `night > 0.25` and ride with the camera.
The moon sits ~19° above the horizon at azimuth ≈ (+x, −z); base FOV is 52°, so use `pitch <= 4` and
`yaw ≈ 314` to bring it into frame — in toy mode the 42° pitch lock makes it unreachable.
Known issue to re-check: the halo plane has no radial falloff, so it reads as a hard-edged quad around
the moon rather than a soft glow.
