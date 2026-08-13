# PLAN — Live San Francisco weather: Karl, cloud, rain, wind, smoke

You are giving the toy diorama real San Francisco weather, sampled as a
**spatial field** so the Sunset can be fogged in while the Mission is sunny.
Rain falls when it is raining. Cloud shadows cross the model when there are
clouds. Karl rolls through the Gate when the marine layer is in.

Read `AGENTS.md` first. Its iron rules bind everything below — especially
rule 2 (perf budgets), rule 3 (procedural fallback), rule 4 (zero required
paid keys) and rule 6 (commit hygiene + `vercel deploy --prod`).

## 0. The decision this plan reverses

`docs/plans/REALTIME-SKY-PLAN.md` §11 says, in as many words: *"No weather, no
external APIs."* `app/src/materials.js` ends its cloud-shadow function with
`* (1.0 - uToy)` under the comment *"The diorama is lit like a model on a
table: no weather on the tabletop."* `env.js` sets `scene.fog.density = 0` the
moment diorama mode turns on.

David has decided to walk that back. Weather is now a first-class character in
the scene, Karl most of all. That is a deliberate art-direction change, not an
oversight to route around — **update the comment in `materials.js` and this
line in the sky plan as part of the work**, so the next agent does not "fix"
your change back to the old rule.

What does NOT change: the model must stay readable (§5), the palette stays the
toy palette, and no stage may cost the perf budget.

## 1. The core idea — weather as a field, not a number

A single "it is foggy in SF" number cannot produce the picture David wants.
Open-Meteo will answer many coordinates in **one** request, and SF's marine
layer is a strong west→east gradient, so we sample a **6×6 grid over the city
bbox** and hand the shaders a tiny texture they can sample by world position.

This was verified live while writing this plan — one request, 36 points,
16.8 KB, HTTP 200, `cloud_cover_low`, north row to south row, west→east:

```
  100 100  72  28  26  26
  100 100  87  55  33  26
  100 100  77  41  41  45
  100 100  83  52  52  45
  100 100 100  86  52  35
```

That wall of 100s on the Pacific side dropping to 26 over the Bay *is* Karl.
Everything in this plan exists to put that field on screen.

Grid: `lat 37.705 → 37.835`, `lon −122.525 → −122.355`, 6×6 = 36 points. The
underlying model (NOAA HRRR) is 3 km, so 36 points resolve to ~18 distinct
cells — deliberate 2× oversampling, which is what makes bilinear interpolation
across the field smooth instead of blocky.

## 2. Stages (each one ships and is reviewed on its own)

| Stage | Ships | Visual risk |
|---|---|---|
| 1 — Feed & readout | `/api/weather`, weather chip on the clock card, concierge tool | None |
| 2 — Cloud & wind | Toy cloud meshes, real cloud shadows, real wind everywhere | Moderate |
| 3a — Karl & rain | Spatial height fog, rain, wet streets, storms, smoke | High |
| 3b — Fog banks | Procedural fog bank meshes for silhouette | High, and gated |

Do not start a stage before the previous one is deployed and David has signed
it off. Stage 1 is provably-correct data with nothing to argue about; that is
the point.

Stage 3b is conditional on the depth-fade prototype in §3.1b passing the perf
budget. Run that prototype early — it is cheap, and it is the only experiment
in this plan whose result can cancel a stage.

---

# STAGE 1 — the feed and the readout

## 1.1 Files

| File | Action |
|---|---|
| `api/_lib/feeds/weather.mjs` | NEW — the fetcher + `registerFeed` line |
| `api/_lib/feeds/index.mjs` | Add `import './weather.mjs';` |
| `app/src/weather.js` | NEW — client poller, smoothing, the field texture |
| `app/src/sky-clock.js` | Add the weather line to the existing card |
| `app/src/main.js` | Create the module, tick it, extend `window.SF` |
| `api/_lib/agent-core.mjs` | Add a `weather_now` tool to `TOOLS` |

## 1.2 `api/_lib/feeds/weather.mjs`

Follow the recipe in the header of `api/_lib/feedcore.mjs` exactly — one async
fetcher that **throws** on failure, one `registerFeed` call. The registry
already owns caching, single-flight refresh, backoff, last-good stale serving
and CDN headers. Do not hand-roll any of that; `api/ferries.mjs`-era patterns
are superseded.

```js
registerFeed('weather', {
  ttl: 5 * 60_000,        // HRRR updates hourly; 5 min is generous and cheap
  staleMs: 60 * 60_000,   // an hour-old field still beats no field
  backoffMs: 2 * 60_000,
  empty: { live: false },
  describe: 'current San Francisco weather: cloud, fog, rain, wind, temperature and air quality, sampled across the city',
  fetcher: fetchWeather,
});
```

Two upstreams, both **keyless** (rule 4 holds — verified live):

1. `https://api.open-meteo.com/v1/forecast` — the 36-point grid.
   `current=temperature_2m,relative_humidity_2m,precipitation,rain,weather_code,cloud_cover,cloud_cover_low,cloud_cover_mid,cloud_cover_high,visibility,wind_speed_10m,wind_direction_10m,wind_gusts_10m`,
   `models=gfs_hrrr`, `temperature_unit=fahrenheit`, `wind_speed_unit=mph`.
2. `https://air-quality-api.open-meteo.com/v1/air-quality` — **one** point
   (downtown is fine; smoke is regional, not per-block).
   `current=us_aqi,pm2_5`.

Fetch both with `Promise.allSettled` and a 10 s `AbortController`. The forecast
failing is a throw; **air quality failing is not** — return the field with
`aqi: null` and let the client skip the smoke layer. Never let the nice-to-have
kill the main event.

Response shape — flat typed arrays, not 36 objects, so the client can drop them
straight into a texture:

```js
{
  live: true,
  grid: { lat0: 37.705, lat1: 37.835, lon0: -122.525, lon1: -122.355, w: 6, h: 6 },
  // 36 entries each, row-major, north row first
  cloudLow: [...], cloudMid: [...], cloudHigh: [...],
  visibility: [...], precip: [...], temp: [...], humidity: [...],
  windSpeed: [...], windDir: [...],
  // city-wide scalars for the UI and the concierge
  summary: { code: 3, label: 'Overcast', temp: 61, feels: 61, windSpeed: 13,
             windDir: 230, gust: 22, visibility: 12200, precip: 0,
             aqi: 30, pm25: 4.5, observedAt: 1786… },
}
```

**Outlier guard (required).** The live 36-point pull produced a single
`0.2 km` visibility cell against `12 km` neighbours — a coastal artefact. Reject
any cell more than 4× from the median of its 4-neighbourhood and replace it
with that median. One bad cell must never punch a hole of fog into a clear city.

Sanity-clamp everything on arrival: percentages to 0–100, visibility to
50–50 000 m, wind to 0–100 mph, temp to −20–130 °F. Upstream nulls become the
field median, not `0` — `0` means "perfectly clear" to a shader and would read
as a bug.

`weather_code` is the WMO table; map it to a short toy label
(`Clear`, `Fair`, `Overcast`, `Fog`, `Drizzle`, `Rain`, `Heavy rain`,
`Thunderstorm`). Keep the mapping in one exported object — the clock, the
concierge and the storm trigger in Stage 3 all read it.

## 1.3 `app/src/weather.js` — the client module

Mirrors `app/src/ferries.js` in shape: poll, degrade quietly, never throw into
the frame loop.

- Poll `/api/weather` every **5 minutes** with ~15 s jitter. Weather is not
  ferries; do not poll it fast.
- `{live:false}`, a fetch failure, or a malformed payload → hold the last good
  field, or if there never was one, a **neutral fair-weather default**
  (35 % cloud, 20 km visibility, no rain, 12 mph W wind). One `console.warn`,
  never a throw, never a black scene. This is rule 3 for weather.
- **Smoothing is mandatory.** Never snap to a new field. Keep `current` and
  `target` fields and ease `current → target` over ~60 s. A 5-minute poll that
  teleports the fog in one frame looks broken; the same change eased over a
  minute looks like weather.
- Build one `DataTexture`, 6×6, `RGBAFormat`, `LinearFilter`, `ClampToEdgeWrap`
  — the GPU's bilinear filter does the spatial interpolation for free:
  - **R** = fog density (derived from visibility, see §3.2)
  - **G** = low cloud cover 0–1
  - **B** = precipitation intensity 0–1
  - **A** = mid+high cloud cover 0–1
  Re-upload (`needsUpdate = true`) only when the eased values actually moved —
  36 texels, at most once a frame, is free, but do not do it for nothing.
- Export `shared.uWeatherField`, `uWeatherOrigin`/`uWeatherScale` (world-space
  bbox → UV), `uWind` (a `Vector2`, m/s), `uRain`, `uSmoke` into `env.js`'s
  `shared` object, so every material picks them up the same way it already
  picks up `uNight` and `uCloudCover`.

Add the world↔UV helper next to the projection in `data.js` and **use the one
projection function** (`AGENTS.md` coordinate conventions) to convert the grid
bbox corners — do not re-derive the projection here.

## 1.4 The clock card

`app/src/sky-clock.js` already owns the top-left toy card and builds its DOM
once, writing only `textContent` afterwards. Add a fourth line in exactly that
style, tokens from `ui-theme.css` only:

`⛅ 61° · Overcast · 13 mph W`

with a drawn 2 px-stroke SVG glyph per condition class (sun / part-cloud /
cloud / fog / rain / storm), matching the existing `sunGlyph()` / `moonGlyph()`
construction. Reuse the accent pills: `--mustard` clear, `--navy` cloud/fog,
`--teal` rain, `--coral` storm or AQI > 100. When AQI > 100 append a small
`AQI 132` pill. Below 480 px the line drops the wind term, not the temperature.

If the feed is not live, the line is simply absent — no error state, no
"weather unavailable" in a diorama.

## 1.5 Concierge

Add `weather_now` to `TOOLS` in `api/_lib/agent-core.mjs`, copying the schema
style of the existing `sky_now`. No arguments; returns `summary` plus a short
per-district digest (name → cloud/visibility/temp for ~6 named neighbourhoods
sampled from the field), so the model can answer *"is it foggy in the Sunset?"*
— which is the whole point of building a field instead of a number. Same iron
rules as every other tool: it returns data, the model answers in plain text,
and it must not be able to set the weather.

## 1.6 Stage 1 QA (deployed)

1. `/api/weather` returns `live:true`, 36 cells per array, plausible values;
   cross-check the summary against weather.gov for SF (temp ± 3 °F, condition
   class matching).
2. Kill the network in devtools → card keeps the last reading, one warning, no
   crash. Reload with the network still dead → neutral default, still no crash.
3. Clock card renders correctly at 1280×800 and 375×700, day and night, no
   overlap with cards/search.
4. Concierge answers "what's the weather?" and "is it foggy in the Sunset?".
5. Perf unchanged — this stage adds one 36-texel texture and no draw calls.

---

# STAGE 2 — cloud and wind

## 2.1 Real cloud shadows, back on the tabletop

In `app/src/materials.js`, `cloudShadow()` currently multiplies by
`(1.0 - uToy)` — delete that factor and drive the term from the field instead:
sample `uWeatherField.g` at the fragment's world position for local cover, and
keep the existing drifting noise as the *shape* of the shadow. Cover now comes
from the sky, shape from the noise.

Two guards, both required:
- Shadow strength maxes at **0.45** even at 100 % cover. A fully shadowed toy
  city is a grey city; the model must keep its painted look.
- Cover still fades out at night (`uNight`) as it does today — cloud shade is
  only meaningful while there is sun to block.

Advance `uCloudDrift` by the **real** wind vector rather than the hardcoded
`CLOUD_WIND`, scaled so it reads at diorama scale (real m/s is imperceptibly
slow across a 500 m cell — tune by eye, target roughly a shadow crossing a
neighbourhood in 20–40 s at 15 mph).

## 2.2 Toy cloud meshes

Chunky low-poly cotton-ball clouds above the model — a physical diorama piece,
per the style bible, not a gradient.

- **One** `InstancedMesh`, one geometry (a lumpy blob of 3–5 merged
  icosahedrons, ~120 tris), one flat two-tone Lambert-ish material: cream lit
  top, cool `#c9d2e4`-ish underside via a world-normal-up term in an
  `onBeforeCompile` — the same trick the moon already uses. **One draw call**,
  which is the entire perf budget for this feature.
- Cap **64 instances**. Count = `round(64 * cloudCover)` where cover is the
  field mean; instances beyond the count are scaled to zero, never re-allocated.
- Placement: scattered over the city bbox with a large margin, at altitude by
  layer — low cloud ≈ 600 m, mid ≈ 2000 m, high ≈ 6000 m — and **positioned by
  the field**, so an instance only appears where its cell is actually clouded.
  This is what makes clouds sit over the Sunset and not over the Mission.
- Drift on the real wind vector; wrap around the bbox when they exit. No
  per-frame allocation — one preallocated `Matrix4` and instance array, updated
  in place.
- Clouds do **not** cast real shadow-map shadows (that would cost a second
  shadow pass) — §2.1's shader term is the shadow.
- At Quality=Low, cap 24 instances. At night, tint them to the night palette
  and drop opacity — a cloudy night sky is darker, not full of white blobs.

## 2.3 Wind everywhere — CUT

David cut this section on 2026-08-13: wind drives the clouds and their shadows
(§2.1, §2.2) and nothing else. Water chop, ferry wakes, flag flutter and tree
sway are all **not** part of this work. Tree sway in particular was judged the
riskiest item for the least return — a windy day very easily reads as an
earthquake — so if it is ever revisited it starts as its own reviewed change.

The original scope, kept only so nobody re-derives it from scratch:

The wind vector is live; spend it on things that already animate:

- `water.js` — chop amplitude and direction from wind speed/direction. It has
  `uTime` and a wave term already; add `uWind` and scale.
- Ferry wakes align to wind-influenced heading (cosmetic, cheap).
- Flags/flagpoles in `props.js` (offices, schools, government buildings) get a
  flutter amplitude and a heading from the wind.
- Trees in `flora.js` sway — vertex-shader sway keyed to `uTime` and `uWind`,
  amplitude by height, **zero CPU cost**. Guard it: sway must be off at
  Quality=Low and must not exceed a few degrees, or a windy day looks like an
  earthquake.

## 2.4 Stage 2 QA

Cloud count and position visibly track the field (compare against the
`/api/weather` response and against a satellite view). Draw calls still < 300 —
report the exact number before and after. 60 fps holds in the Mission and
downtown stress cells, day and night, on the full browser matrix per
`PERF-PLAN.md`. Fallback drill: force `{live:false}` → neutral clouds, no
crash. Screenshot the same hero view at 0 %, 50 % and 100 % cover via the
debug hook.

---

# STAGE 3 — Karl, rain, storms, smoke

## 3.1 Karl the Fog — two layers, both procedural

The headline. Real marine layer, spatially placed, genuinely swallowing the
west side while downtown stays clear.

Karl is **two systems**, because fog does two visually distinct things and no
single technique does both:

| Layer | Job | Technique | Stage |
|---|---|---|---|
| **3.1a Dissolution** | The city fades to grey with distance | Spatial height fog in the material fragment stage | 3a |
| **3.1b Form** | A wall of fog pours through the Gate and over the hills | Procedural fog bank meshes, instanced, field-driven | 3b |

Shader fog has no silhouette — it can only be seen *through*, never seen. That
gets you an atmospheric grey-out but never the rolling wall, which is the image
that makes Karl a character rather than a visibility number. The banks supply
the edge; the shader supplies the depth. Ship 3a first, judge it, then 3b.

**Both layers are generated in code. Blender is not in the loop.** This was
considered and rejected, and the reasoning matters enough to record so nobody
re-opens it: glTF has no volume primitive, so Blender's Principled Volume,
smoke sims and OpenVDB cannot be exported to GLB at all — the exporter drops
volume objects silently. (`KHR_materials_volume` is refraction through glass,
not participating media.) The remaining Blender option — hand-sculpted bank
*meshes* — would need a transparent material, which the asset contract bans
(`.agents/skills/sf-asset-check/SKILL.md` rule 4) and the loader rejects
outright (`app/src/assets.js`, the `material.transparent || material.map`
violation check). That ban applies only to imported GLBs; code-built meshes
have never been subject to it, and `env.js` already ships two transparent
custom-shader meshes (the moon and its additive halo). Generating the banks in
JS therefore costs a contract exception of zero, a new loader path of zero, and
an authoring round-trip of zero — and a fog bank is lumpy, soft-edged and
near-featureless, the one class of object where procedural generation gives up
nothing to hand-modelling. Unlike a landmark, no real-world information is
being carried.

### 3.1a Dissolution — spatial height fog

Implement as **height fog in the materials' fragment stage**, not as
`scene.fog`. `FogExp2` is uniform and global — it cannot do "fogged Sunset,
clear Mission", which is the entire feature. Add to the shared material chunk:

```
density  = texture(uWeatherField, worldToUV(worldPos)).r   // spatial
height   = smoothstep(uFogTop, uFogBase, worldPos.y)       // a layer, not a soup
camera   = smoothstep(0.0, uFogClear, distanceToCamera)    // the clear bubble
factor   = 1 - exp(-density * height * dist * dist * k)
color    = mix(color, uFogColor, factor * camera * uFogMax)
```

- **`uFogBase` / `uFogTop`**: the marine layer is a *layer* — roughly sea level
  to ~300 m. Twin Peaks (~280 m) and Sutro Tower poke out the top of a real
  marine layer, and that shot is the single best image this feature can
  produce. Get the height falloff right and you get it for free.
- **The clear bubble (David's explicit call).** `uFogClear` ≈ 150 m: fog
  contribution ramps from 0 at the camera to full at 150 m out. Fly into the
  bank and your immediate surroundings stay readable while the city dissolves
  into grey behind them. Fog reads as depth, never as a blindfold.
- **`uFogMax` ≈ 0.92**, so the deepest pea-souper still leaves a ghost of
  silhouette rather than a flat grey rectangle.
- Fog colour is not white — a warm-grey by day (`#dfe3e6`-ish), shifting to the
  existing `TOY_NIGHT.fog` navy at night via `uNight`, so a foggy night is
  still the painted-object-in-a-dark-room look.
- Density from **visibility**, not humidity: `density ≈ k / visibility_m`,
  calibrated so 20 km reads as clean air and 1 km is a genuine white-out.

Apply the same chunk to buildings, terrain, streets and water so nothing
floats out of the fog unfogged — water especially, since it has its own
hand-rolled fog uniforms in `water.js` that must be switched to the field.

**Readability floor, per rule 2 and the §5 precedent in the sky plan:** at
Quality=Low, and at night, verify street level in the Mission and downtown
stays readable at 100 % fog. If it does not, `uFogMax` comes down. The
tilt-shift grade in `toypost.js` is not the lever — do not touch it.

### 3.1b Form — procedural fog banks

Ground-level cousins of the Stage 2 cloud meshes, and they **reuse that
generator**: the same lumpy merged-icosahedron blob, flattened hard on Y and
scaled wide, so there is one shape generator in the codebase and not two.

- **One** `InstancedMesh`, one draw call, cap **48 instances** (24 at
  Quality=Medium, **0 at Quality=Low** — the banks are the first thing to go).
- Soft, near-flat, translucent toy material: a flat cream-grey, opacity ~0.5,
  `depthWrite: false`, sorted back-to-front. No texture, no noise sampling in
  the fragment stage — the *silhouette* carries the read, exactly as the toy
  clouds do.
- Placement is driven by the field: an instance spawns only where local
  visibility is low, sits between `uFogBase` and `uFogTop`, and scales with
  local density. They drift on the real wind vector and wrap at the bbox, the
  same code path as the clouds.
- Because they are placed by the same field that drives 3.1a, the two layers
  agree automatically — banks appear exactly where the shader is already
  thickening. If they ever disagree visually, the bug is in the world→UV
  mapping, not in the art.

**The depth-fade gate.** A bank intersecting Twin Peaks or a tower produces a
hard geometric seam that instantly reads as a bug. The fix is a soft-particle
depth fade: fade the bank's alpha as its fragment approaches the depth already
in the buffer. That needs a **readable depth texture**, and `toypost.js`
currently allocates its render target with `depthBuffer: true` but no
`DepthTexture` — and it is an MSAA target, so attaching one costs a resolve.

This is the single highest technical risk in the whole plan, and it is the only
thing that could force a rethink of 3.1b. **Prototype it before building any of
Stage 3b**: attach a `DepthTexture` to the post target, measure the resolve
cost against the `PERF-PLAN.md` matrix, and confirm a test blob fades cleanly
against terrain. If the cost fails the budget, 3.1b is cancelled and 3.1a ships
alone — which is a perfectly good feature on its own. Do not build the banks
and then discover this.

## 3.2 Rain

- Instanced streak quads in a **camera-following box** (~300 m), not city-wide
  — you only ever see rain near you. One `InstancedMesh`, one draw call, count
  scaled by local precipitation sampled from the field (`.b`), capped ~2000 at
  High and 0 at Low.
- Streaks are toy: short, soft, slightly translucent, tilted by the wind
  vector. Not photoreal drops.
- **Wet streets sell rain more than the drops do.** When local precip > 0,
  darken and gloss road/sidewalk materials (a specular boost + a downward
  colour multiply in the existing material chunk) and ease it over ~90 s so
  streets dry out slowly after the rain stops. This is cheap and high payoff.
- Ripples on `water.js` scale with precip.
- Rain is spatially sampled too — a passing shower over the Richmond is real SF.

## 3.3 Storms

Trigger on WMO thunderstorm codes (95/96/99) or precip above a heavy threshold:
sky dome darkens, rain to maximum, and occasional **lightning** — a 2-frame
flash on the hemisphere light plus a brief sky-dome brightening, randomised
every 8–25 s. No lightning bolt geometry; the flash is the effect.

Storms are rare, so they must be testable on demand: `SF.setWeather` (§3.5)
must be able to produce a full storm on a clear August afternoon, and the QA
for this section is done through it.

## 3.4 Wildfire smoke

`us_aqi` drives an orange-brown haze: above AQI 100, tint the fog colour and
the sun colour toward amber and lift a low-altitude haze term; above 200, push
it to the September-2020 orange. This shares the fog machinery entirely — it is
a colour and a floor on density, not a new system. Keep it firmly bounded: the
sky may go orange, the city must stay readable.

## 3.5 Debug hook

`SF.setWeather(patch | null)` — merge a partial override onto the live field,
`null` returns to live. Debug only: **no UI, no URL parameter**, exactly
matching how `SF.setClock` works today. Also expose `SF.weather` returning the
current eased state, and make `SF.setWeather({ preset: 'karl' | 'storm' |
'clear' | 'smoke' })` produce the canonical demo states — QA and screenshots
both depend on it.

## 3.6 Stage 3 QA

0. **(3b only, run first)** Depth-fade prototype passes: `DepthTexture` on the
   MSAA post target, resolve cost inside the `PERF-PLAN.md` budget, a test blob
   fading cleanly against terrain with no seam. FAIL here cancels 3b and ships
   3a alone — that is an acceptable outcome, not a defeat.
1. `SF.setWeather({preset:'karl'})` — fog sits over the west side, downtown
   clear, Twin Peaks and Sutro above the layer. Screenshot from the hero aerial
   and from the Golden Gate.
2. Fly the camera into the bank — surroundings readable, city dissolves. Never
   a flat grey frame. With 3b in, no bank clips visibly through terrain or a
   tower from any angle.
3. 100 % fog × Quality=Low × night × street level in the Mission and downtown:
   readable. This is the gate; if it fails, lower `uFogMax` and re-run.
4. Rain: streaks visible, streets wet and drying slowly after
   `setWeather({precip:0})`, ripples on the Bay.
5. Storm and smoke presets screenshot correctly.
6. Perf: draw calls < 300 worst case with fog + rain + clouds all at maximum;
   60 fps across the `PERF-PLAN.md` matrix; no memory growth over 3 minutes.
7. Fallback drill: break the feed → neutral weather, one warning, city intact.
8. Live check: leave it on the real feed for a day and confirm it matches
   reality out the window. This is the only test that really matters.

---

## 4. What NOT to do

- No paid keys, no npm packages, no `three/examples` post-processing additions.
- No `scene.fog` for Karl — it cannot be spatial (§3.1a).
- **No Blender assets for weather.** Clouds, fog banks and rain are all
  generated in code. See §3.1 for why; do not re-open it by authoring a GLB.
- No second render pass, no volumetric raymarching, no baking OpenVDB to a
  `Data3DTexture`, no new shadow-casting lights. One extra draw call each for
  clouds, fog banks and rain. That is the budget.
- No user-facing weather control (no picker, no URL parameter) — debug only.
- No touching `toypost.js`, the camera rig, tiles, the pipeline or any GLB.
- Do not weaken the night usability floor in `env.js` — fog stacks *on top of*
  it, and the two together are the worst case you must QA.
- Do not let weather change the toy palette. Overcast desaturates the *light*,
  never the paint.

## 5. Open question for David

Temperature and humidity were in scope, but they are the weakest lever here:
the honest visual for "it is 68° instead of 58°" is a slight warm shift in the
light grade, and the style bible is strict about the light. Recommendation:
implement temperature as the clock-card readout and a concierge field only
(Stage 1), and revisit a grade shift after Stage 3 lands, when there is a real
scene to judge it against. Flagging rather than silently dropping it.
