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
