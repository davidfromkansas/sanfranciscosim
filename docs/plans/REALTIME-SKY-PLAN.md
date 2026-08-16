# PLAN — Real-time sun & moon, live SF clock, and concierge sky data

You are implementing a real-time sky for the SF toy diorama. The scene currently
runs a fake 0→1 "golden hour → dusk" sweep. You will replace it with the REAL
sun and moon, computed astronomically for San Francisco from the real wall
clock, plus a diorama-styled clock in the top-left of the screen, and a
concierge tool so the LLM agent can answer questions about it.

Read `AGENTS.md` first. Its iron rules apply to everything below — especially
rule 2 (perf budgets), rule 3 (procedural fallback), rule 4 (zero required paid
keys: everything here is computed locally, NO astronomy APIs, NO new
dependencies), and rule 6 (commit hygiene + `vercel deploy --prod`).

## 0. Prior art and why we're doing it differently

The owner's `nycsim` repo (github.com/davidfromkansas/nycsim,
`public/index.html`, section "26b. LIVE NYC") drives lighting from a NOAA-style
`solarPos(ms)` function and mixes lighting modes by solar elevation. Borrow its
good ideas; improve on its gaps:

| nycsim | This implementation (better) |
|---|---|
| Sun position only; no moon trajectory, no phase | Real moon position AND phase; the moon is the night key light |
| Astronomy math inline in a 12k-line HTML file | One shared, tested module used by BOTH the app and the concierge API |
| Time scrub offset kept | Live time ONLY (owner's decision) — no scrub UI |
| Manual `-0.22` clamp keeps night barely lit | Explicit usability floor: minimum light + navy sky so the city is always readable at night |
| Weather integration | OUT OF SCOPE **for this plan** — superseded by `WEATHER-PLAN.md`, which added live weather deliberately. This plan still adds none. |
| Clock chip with weather | Diorama-styled clock: time + date + sunrise/sunset + moon phase |

## 1. Files you will touch

| File | Action |
|---|---|
| `api/_lib/astro.mjs` | NEW — the single shared astronomy module |
| `app/src/sky-clock.js` | NEW — the top-left clock UI component |
| `app/src/env.js` | Rework `setTime(t)` into sun/moon-driven `setSky(...)`; real moon placement + phase |
| `app/src/main.js` | Replace the 180 s auto-sweep with a 1 Hz real-time tick; wire the clock; extend `window.SF` |
| `app/src/ui.js` | Remove the time slider + auto checkbox from the HUD |
| `api/_lib/agent-core.mjs` | Add a `sky_now` tool to `TOOLS` |
| `.agents/skills/testing-sf-3d/SKILL.md` | Update the notes about time controls (see §9) |

Do NOT touch the pipeline, tiles, or any GLB.

## 2. `api/_lib/astro.mjs` — the shared astronomy module

One module, plain ESM, zero dependencies, no `three` import (the API functions
must load it). It lives in `api/_lib/` so the Vercel function can use it; the
app imports it with a relative path (`import ... from '../../api/_lib/astro.mjs'`)
— Vite bundles across the app root boundary without extra config. If the build
rejects the import, add a Vite `resolve.alias` for it; do NOT copy-paste the
module into two places.

Export (all angles in RADIANS, all times in ms epoch):

```js
export const SF = { lat: 37.77, lon: -122.4375 };            // matches the projection center in AGENTS.md
export function sunPosition(ms)  // -> { elevation, azimuth }  azimuth from true north, clockwise
export function moonPosition(ms) // -> { elevation, azimuth, phase, illumination }
                                 // phase: 0..1 (0 = new, 0.5 = full), illumination: 0..1 lit fraction
export function sunTimes(ms)    // -> { sunrise, sunset, solarNoon } (ms) for the SF calendar day containing ms
export function moonTimes(ms)   // -> { moonrise, moonset } (ms, either may be null on days without one)
export function skySnapshot(ms) // -> one object with all of the above in DEGREES plus
                                //    { localTime, localDate, isDay, phaseName } — the concierge payload
```

Implementation notes:

- Sun: the same NOAA low-accuracy algorithm nycsim uses (days since J2000 →
  mean longitude/anomaly → ecliptic longitude → declination + right ascension →
  equation of time → true solar time → hour angle → elevation/azimuth). Accuracy
  well under 1° — plenty for lighting.
- Moon: use the standard low-precision lunar ephemeris (Astronomical Almanac /
  the widely used "suncalc" formulation): compute the Moon's ecliptic longitude
  L, mean anomaly M, mean distance F from three linear polynomials in days
  since J2000, apply the main perturbation terms, convert to right
  ascension/declination, then to azimuth/elevation via the same hour-angle math
  as the sun. Phase from the sun–moon elongation. Do not chase arcsecond
  accuracy; ±1° is fine.
- Rise/set: scan the day in 5-minute steps for elevation zero-crossings, then
  refine each crossing with 3 rounds of bisection. Simple and robust; runs at
  most a few times per session so cost is irrelevant.
- Time zone: derive local SF wall-clock strings ONLY via
  `Intl.DateTimeFormat('en-US', { timeZone: 'America/Los_Angeles', ... })`.
  Never add or subtract a fixed UTC offset anywhere — that breaks on DST.
- `phaseName`: new moon / waxing crescent / first quarter / waxing gibbous /
  full moon / waning gibbous / last quarter / waning crescent (thresholds at
  0.0625 steps around the canonical phase points).
- The module must not allocate per call in a way that matters, but it is only
  called ~1×/second, so clarity beats micro-optimization.

Write a small self-check you can run with `node`: print `skySnapshot(Date.now())`
and sanity-check against timeanddate.com for San Francisco (sunrise/sunset
within ~2 minutes, sun azimuth/elevation within ~1°, moon phase matching).
Include the check as a comment or a `scripts/`-style snippet in the PR
description, not as a shipped test framework.

## 3. Coordinate conversion (get this right or shadows point the wrong way)

World frame per AGENTS.md: **+x = east, −z = north, +y = up.** Astronomical
azimuth is measured from true north, clockwise (east = 90°). Therefore:

```js
dir.x = Math.sin(az) * Math.cos(el);   // east
dir.y = Math.sin(el);                  // up
dir.z = -Math.cos(az) * Math.cos(el);  // north is -z
```

Sanity checks you MUST do on the deployed build:
- Around 12–1 pm PT the sun is roughly south (+z direction), so building
  shadows point roughly north (−z, i.e. "up" when yaw = 0).
- In the evening the sun sets over the Pacific (−x, west): the Golden Gate side
  of the scene gets the warm horizon glow.

## 4. `app/src/env.js` — from fake sweep to real sky

Current state: `setTime(t)` maps a 0→1 slider to a hardcoded sun path
(elevation +15°→−8°, azimuth 256°→270°) and a `night` value
`(t - 0.36) / 0.5` that every emissive system reads via `shared.uNight`.

Keep the SHAPE of the system — one directional light, one hemisphere light,
`shared.uNight` driving windows/lamps/glow — and change only what feeds it:

1. Add `setSky({ sunEl, sunAz, moonEl, moonAz, moonIllum })` (radians). Keep
   `setTime(t)` as a thin adapter during development if convenient, but the
   shipped code path is `setSky`.
2. **Sun direction:** from §3. When the sun is below the horizon, do NOT let
   the directional light vector sink fully — clamp effective `dir.y` to ≥ −0.20
   so the shadow camera stays sane (nycsim does the same with −0.22).
3. **Lighting mix by solar elevation** (degrees), replacing the `night` ramp.
   Define four toy lighting states and blend piecewise-linearly:
   - `elev ≥ 25°` → TOY_NOON (current `TOY` values — the shipped daytime look
     stays exactly as-is at high sun)
   - `25° → 8°` → blend TOY_NOON → TOY_GOLDEN (new: warm key ~#ffe3c0,
     slightly lower intensity, hemisphere warms)
   - `8° → −4°` → blend TOY_GOLDEN → TOY_DUSK (new: coral-amber horizon,
     key drops toward 0.9, `uNight` climbs 0 → 0.55)
   - `−4° → −10°` → blend TOY_DUSK → TOY_NIGHT (existing `TOY_NIGHT` palette;
     `uNight` climbs 0.55 → 1.0)
   - `elev < −10°` → full TOY_NIGHT.
   Pick TOY_GOLDEN / TOY_DUSK values by eye against the current slider
   mid-points so the familiar look survives; they are new named constants next
   to `TOY` and `TOY_NIGHT`.
   `shared.uNight` MUST still reach exactly 0 by day and exactly 1 at night —
   the whole city (window ignition, lamps, glow materials, kit `Toy_glass`)
   reads it.
4. **The moon becomes real.** Today `nightSky` (moon mesh + halo + stars) sits
   at a fixed offset riding the camera. Change `updateNightSky(camera)` to
   place the moon along its REAL direction vector at the same radius class
   (~16 km out, y from elevation, never below y = 900 so it stays visually
   above the hills), still camera-relative so it never parallaxes behind
   terrain. Halo follows it; stars unchanged.
5. **Moon phase:** shade the moon mesh with a tiny shader (or a second darker
   hemisphere mesh rotated by the phase angle) so illumination reads correctly
   — full disc at `illumination ≈ 1`, crescent at low values. Keep it toy-flat:
   two colors (cream lit side, deep navy dark side), no craters, no textures.
   The halo + moonlight intensity scale with `illumination` (see §5).
6. **Moonlight drives the night key.** At night the directional light's
   direction follows the MOON (converted per §3, same y-clamp), its color is
   `TOY_NIGHT.sun` (pale blue), and its intensity scales
   `0.25 + 0.35 * illumination`. When the moon is below the horizon at night,
   fall back to a fixed high-northeast direction at the floor intensity —
   never zero (see §5). Blend sun-key → moon-key across the dusk band so there
   is no pop.
7. Everything already budgeted stays budgeted: no new lights, no new
   per-frame allocation, shadow logic (`updateShadow`) unchanged apart from
   receiving whichever direction (sun or moon) currently owns the key.

## 5. The usability floor (hard requirement)

At NO real-world time may the city become hard to read. After the full
TOY_NIGHT blend, enforce minimums:

- Directional (moon) intensity ≥ 0.25, hemisphere intensity ≥ 0.42
  (the current `TOY_NIGHT` value — do not go below it even at new moon).
- Sky zenith never darker than `TOY_NIGHT.zenith` (#1a2340) — deep navy, not
  black, per the style bible's "painted object in a dark room" note.
- The tilt-shift/grade post pass (`toypost.js`) is NOT a lever for this —
  don't touch it.

QA this at a simulated 2 AM new-moon time (see the debug override in §8):
street-level Mission and downtown must both clearly show building massing,
streets, and picking targets with windows glowing.

## 6. The clock — `app/src/sky-clock.js`

A new top-LEFT fixed panel (the existing HUD sits elsewhere; keep clear of the
stats overlay). Diorama-styled per the UI iron rules — use ONLY tokens from
`app/src/ui-theme.css` (`--paper`, `--ink`, `--shadow`, `--mustard`, `--navy`,
`--radius`...). No gradients, no glassmorphism, hard offset shadow, 2px ink
border, rounded chunky type.

Content, three stacked lines on cream card stock:

1. **Time** — large, `font-variant-numeric: tabular-nums`, e.g. `3:42 PM`,
   with the AM/PM as a small candy accent pill (mustard by day, navy at night).
2. **Date** — small caps ink-soft, e.g. `MON · AUG 10`.
3. **Sky line** — a small sun or moon glyph (inline SVG, flat toy colors)
   plus context: by day `☀ sets 8:14 PM`, by night `☾ waxing gibbous · rises 9:02 PM`
   (use the actual glyph drawings, not emoji — 2px-stroke SVG circles/arcs in
   ink + mustard/cream, matching the card style).

Behavior:

- Update via `setInterval` at 1 Hz; write only `textContent` of prepared nodes
  (build the DOM once, no innerHTML churn, no layout thrash).
- All strings from `Intl.DateTimeFormat` with `timeZone: 'America/Los_Angeles'`.
- The panel is part of the permanent UI: visible on load, day and night, but
  must not overlap the context cards or search — check both.
- Mobile: it may shrink (drop the date line below 480 px width) but stays
  top-left.

## 7. `app/src/main.js` and `app/src/ui.js` — removing the fake time system

- Delete the HUD time slider and the auto checkbox (`ui.js` — the whole
  `timePanel`), and the `autoTime` sweep in `main.js` (`timeOfDay + dt / 180`).
- Replace with a 1 Hz tick (piggyback on the existing rAF loop with a
  time-accumulator — do NOT add a second rAF): every second compute
  `sunPosition(now)` / `moonPosition(now)` and call `env.setSky(...)` and the
  clock update. Positions change slowly; 1 Hz is generous and free.
- Keep `env.updateNightSky(camera)` per-frame as today (it only repositions
  meshes relative to the camera).
- The "Golden hour → dusk" HUD copy and any help text mentioning the slider
  must be removed/updated.

## 8. Debug & test surface (`window.SF`)

The testing skill and QA rely on `window.SF`. Provide:

- `SF.sky` → the latest `skySnapshot` object (refreshed each tick).
- `SF.setClock(msOrIsoOrNull)` → debug override: freezes the scene clock at the
  given moment (everything — lights, moon, clock panel — follows it);
  `null` returns to live. This replaces the old `SF.setTime(t)`; keep a
  `SF.setTime` alias that maps 0→sunset-ish and logs a deprecation warning so
  old test recipes fail loudly rather than silently.
- No user-facing URL parameter for time — this is a debug hook only.

## 9. Concierge: the `sky_now` tool (`api/_lib/agent-core.mjs`)

Add to `TOOLS` (read the existing entries and copy their exact schema style):

```
name: 'sky_now'
description: 'Current San Francisco date, time, sun and moon positions,
  sunrise/sunset, moonrise/moonset and moon phase. Use for any question about
  the time of day, lighting, sun, moon, sunrise or sunset in the scene.'
parameters: {} (no arguments)
```

Handler: `import { skySnapshot } from './astro.mjs'` and return
`skySnapshot(Date.now())`. It is pure computation — no network, no key, no
rate-limit concerns beyond the existing per-IP limits, and it must work in the
keyless-503 path exactly like other tools (i.e., it's only reachable when the
concierge itself is up).

Keep the concierge iron rules: the tool returns data; the model answers from
the tool result as plain text. Do not let the model set the scene time — there
is no intent for that (live time only).

Concierge QA: ask "what time is it in the city?", "when does the sun set?",
"what phase is the moon?" on the deployed site and confirm sensible plain-text
answers.

## 10. Update the testing skill

`.agents/skills/testing-sf-3d/SKILL.md` documents the old slider, the
"Golden hour → dusk" range control, the ~180 s auto sweep, and `SF.setTime(t)`.
Update those paragraphs to describe: live real time, `SF.setClock(...)`,
`SF.sky`, and the clock panel. Keep the rest of the skill intact.

## 11. What NOT to do

> **Superseded in part (see `WEATHER-PLAN.md`).** The "no weather, no external
> APIs" rule below was correct for THIS plan and is still the rule for the
> astronomy module: `astro.mjs` remains pure local computation with no network
> call and no key. Live weather now exists, but it arrives through its own feed
> (`/api/weather`) and its own module — it never reaches into the sun/moon maths.


- No weather, no external APIs, no npm packages (`suncalc` etc. — write the
  math in `astro.mjs` instead; it is ~120 lines).
- No user-facing time travel (no slider, no URL param, no concierge intent).
- No touching `toypost.js`, the camera rig, tiles, pipeline, or GLBs.
- No second render pass, no new lights beyond the existing sun + hemi pair.
- Do not remove or weaken the procedural fallback paths.
- Do not break Quality=Low behavior (shadows 0 / windows 0 must still work —
  windows-off at night is exactly why the §5 floor matters; verify Low at
  night is still readable).

## 12. QA checklist (run on the DEPLOYED site; report PASS/FAIL per item)

1. Cold cache-cleared load boots the diorama first-frame with the sky matching
   the real current SF time (verify against your local clock ± time zone).
2. Clock panel top-left: correct time ticking every second, correct date,
   correct sunrise/sunset for today (cross-check timeanddate.com ± 2 min),
   correct moon phase name. Toy-styled: tokens only, hard shadow, no overlap
   with cards/search at 1280×800 and 375×700.
3. `SF.setClock` sweep: step through 6 AM / 9 AM / 1 PM / 5 PM / sunset /
   9 PM / 2 AM. Screenshot each. Lighting transitions are continuous (no pops),
   shadows track the sun azimuth plausibly (§3 sanity checks), the moon rises
   and sets on the correct side of the sky, and its phase shading matches
   `SF.sky.illumination`.
4. Usability floor: at 2 AM with `SF.setClock` (and again with Quality=Low),
   street level in the Mission and downtown clearly readable; navy (not black)
   sky; windows/lamps lit.
5. Perf: stats overlay at street level Mission + downtown, day AND night —
   draw calls < 300, no memory growth over 3 minutes of flying, fps unchanged
   vs. before the change (± noise).
6. Concierge: the three questions from §9 answered correctly; concierge still
   degrades to the friendly offline state without a key.
7. Fallback drill: temporarily break `astro.mjs` import in the served bundle
   is not testable post-build — instead unit-drill it locally: make
   `skySnapshot` throw, confirm the app catches it, logs ONE warning, and
   falls back to a fixed pleasant golden-hour sky (hardcode the current
   `setTime(0)` equivalent as the fallback state). Never a black scene, never
   a crash loop.
8. Old controls gone: no time slider in the HUD, `SF.setTime(0.5)` logs the
   deprecation warning and still changes the scene (via the alias), help text
   updated.
9. `vercel deploy --prod`; production URL is the FIRST line of the completion
   summary, followed by this checklist with PASS/FAIL and screenshots.
