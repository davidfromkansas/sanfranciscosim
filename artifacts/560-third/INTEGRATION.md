# 560 Third Street — integration report (stage 5, batch mode)

Executed `docs/asset-plans/INTEGRATION-PROMPT.md` Part 1 with `<slug> = 560-third`,
`<Name> = 560 Third Street`, **Case B** (new landmark, needs a registry entry and a
tile re-bake). Step 7 (push / PR / deploy) is replaced by a stop, per
`docs/asset-pipeline/ADDRESS-TO-ASSET.md` stage 5.

**Batch mode.** The bake was run in full and used for the QA below, then thrown
away; this branch commits **source only**. `git diff --name-only origin/main`
lists nothing under `app/public/tiles/` or `api/_data/`.

## PASS / FAIL

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Re-validation of the shipping GLB in a fresh Blender scene | **PASS** | `validate_560_third.py` → `overall: PASS`, 16/16 checks, 2,356 tris, 23.90 × 24.06 × 7.20 m, min Z 0.0, 8 `Toy_*` materials, 2 `_Glow`, no textures / transparency / cameras / lights / animation |
| 2 | Asset dropped in | **PASS** | `app/public/sf-assets/landmarks/560-third.glb`, 67,892 bytes, byte-identical to `artifacts/560-third/560-third.glb`; already meshopt-compressed by stage 4, so `compress-assets.mjs` is a no-op on it |
| 3 | Manifest entry | **PASS** | appended textually so no other entry reformats; the diff is +19 lines and nothing else |
| 4 | id mapping | **PASS** | `camelId('560-third') === '560Third'`, which is the `pipeline/lib/landmarks.mjs` id |
| 5 | Case B registry entry | **PASS** | `560Third`, lon/lat as measured, `height: 7.2`, `exclude: 8`, `camera: { distance: 150, yaw: 135, pitch: 30 }` |
| 6 | Exclusion radius sized against the real bake input | **PASS** | see below — band `0.82 < r ≤ 11.65`, shipped 8 |
| 7 | Tile re-bake | **PASS** | full chain `terrain → bridges → buildings → streets → landcover → validate → lore → toy → notables → context → muni-shapes`, 3 min; 595 files changed, of which **exactly one** buildings tile (`23_13.bin`) |
| 8 | `verify-rebake.mjs` | **PASS** | `584 of 585 cells unchanged`; `23_13 217 -> 215 <- 560Third`; nearest surviving footprint 43.3 m vs an 8 m radius |
| 9 | `audit.mjs` check 1.6 | **PASS** | `no procedural footprint inside a bespoke landmark exclusion zone — 66 zones over 65 landmarks clear` |
| 10 | Exactly one building on the site | **PASS** | 0 surviving procedural rings overlap the asset footprint (point-in-polygon over the 3×3 cell block); nearest survivor 43.3 m away |
| 11 | Loader merge + scale factor | **PASS** | `sf-assets: 560-third merged 8 objects / 8 materials -> batched (1343 tris body); uniform x1.0000 at 3729, -1151` — scale exactly 1.0000, position exactly the projected anchor |
| 12 | Streaming | **PASS** | `SF.assets.stats()` = `{entries: 59, far: 6, loading: 0, live: 53, fading: 0, failed: 0}` with the camera on site |
| 13 | Footprint size and orientation | **PASS** | `qa/day.png` — the 9.4 m frontage sits on Third Street between 574 and 550, front normal 44.1° facing the street, no rotation applied by the loader |
| 14 | Terrain seating | **PASS** | sampled terrain 6.447 m at the anchor, range 0.424 m over the footprint; neighbouring surviving footprints have `baseY` 5.1–6.4 m. No float, no sink. |
| 15 | Night glow | **PASS** | `qa/night.png` at 22:30 — the four-pane band glows warm, the door cue glows, the two skylights read on the roof, and nothing else on the building lights |
| 16 | Draw-call budget (AGENTS rule 2) | **PASS** | 77–86 draw calls on site against the 300 iron rule; the landmark itself adds **0** — it merges into the shared `BatchedMesh` pair |
| 17 | Fallback drill (mandatory) | **PASS** | see below |
| 18 | `npm run lint` | **PASS** | eslint clean |
| 19 | `npm run build` | **PASS** | built in 1.3 s; `compress-tiles` 3,315 tiles 56.8 → 31.8 MB |
| 20 | Batch-mode source-only sanity check | **PASS** | `git diff --name-only origin/main` lists nothing under `app/public/tiles/` or `api/_data/` |

## The exclusion radius, measured

`excluded()` in `pipeline/buildings.mjs` drops a footprint when its ring
**centroid OR any ring vertex** is inside the radius. Measured from this anchor
against the two sources the bake actually reads, with the pipeline's own
`simplifyRing(0.6)` / `ringCentroid`:

| source | ring | centroid | nearest vertex | gate |
|---|---|---:|---:|---:|
| DataSF | `SF3776007` — **this building** | 0.82 m | 12.64 m | **0.82 m** |
| Overture | `…68dff3fc7081` — this building's twin | 0.17 m | 12.86 m | **0.17 m** |
| Overture | `…76897c93769c` — 574 Third | 17.51 m | 11.65 m | 11.65 m |
| DataSF | `SF3776008` — 574 Third | 24.36 m | 12.55 m | 12.55 m |
| DataSF | `SF3776005` — 550 Third | 18.81 m | 14.02 m | 14.02 m |

```
r =  2–11 m -> drops 1 building  (correct: this one, both its rings)
r = 12 m    -> drops 2           (eats 574 Third's Overture ring)
r = 13 m    -> drops 3           (eats 574 Third proper)
r = 15 m    -> drops 4           (eats 550 Third)
```

The safe band is `0.82 < r ≤ 11.65`. **Shipped 8** — the value `550Third` and
`551Third` already carry on this block, with 3.6 m of headroom to the nearest
neighbour. Unusually for a party-wall site the band is wide, because the gate
that catches this footprint is its own *centroid* (a 246 m² ring puts its
centroid within a metre of the anchor), not a vertex.

The re-bake confirmed it: cell `23_13` went 217 → 215, i.e. both of this
building's rings and nothing else.

## Fallback drill (Step 6)

Served `/sf-assets/landmarks/560-third.glb` as a real 404 and reloaded:

- the app booted and the whole area rendered normally;
- **exactly one** warning: `sf-assets: 560-third failed to load (fetch … responded with 404: Not Found)`;
- `SF.assets.stats()` → `failed: 1, live: 52` — no other landmark affected;
- draw calls unchanged at 86;
- Case B behaviour as documented: the site is **empty ground** inside the
  exclusion zone (`qa/drill-day.png`, right-hand side of the A/B) — expected,
  because there is no procedural twin to fall back to.

Restored afterwards; the drill never touched the file on disk (the QA server
returns 404 for that path under `--drill`).

## How the QA was run, and the one thing that was not

The in-app Browser pane could not be used: `preview_start` refuses with
*"Maximum 5 dev servers per folder reached; 5 belong to other chats"*, and those
belong to parallel sessions this run must not stop.

Instead the QA above drove the **built** app (`app/dist`) in real headless Chrome
over CDP, served from an ephemeral in-process static server — the same technique
`pipeline/landmark-streaming-check.mjs` uses, and for the same reason: rAF runs
continuously in headless Chrome, where a hidden preview pane throttles it to
nothing and makes a working streamer look broken. Every number and screenshot
above comes from that run.

What that does **not** cover, and is left for the user:

- a human look at the landmark in the interactive preview,
- keyboard/mouse interaction (this landmark has no preset key, by design),
- the deployed production QA — which stage 5 defers anyway until the user says
  ship.

## Corrections made during integration

1. **The camera preset yaw was wrong on the first pass and was fixed by
   rendering it.** `camera.js` places the eye at
   `pivot + (sin yaw, sin pitch, cos yaw) · distance` with **+z south**, so
   `yaw: 45` puts the eye south-*east* — staring at the blind south-east party
   wall. The eye has to be north-east, on Third Street: `yaw: 135`. Caught by
   rendering the preset rather than by arithmetic on paper.
2. `SF.goTo(lon, lat, distance, yaw, pitch)` takes **degrees** — `rig.set()`
   multiplies by `DEG`. Passing radians silently produced a yaw of 2.4°.
3. The manifest entry is appended as text rather than by
   `JSON.parse`/`JSON.stringify`: a round trip rewrites `11.0` as `11` in six
   unrelated entries, which is exactly the "do not edit any other manifest
   entry" rule.

## Pre-existing failures, not caused by this change

- `audit.mjs` 1.2b (p95 height band), 1.3c (Telegraph Hill DEM), 1.7b (1 of 793
  sampled trees offshore) — all three fail on `main`.
- Console: `fog banks: fog-cube.glb unavailable — setMeshoptDecoder must be
  called before loading compressed files`. This is the fog-bank loader path, not
  the landmark path, and `fog-cube.glb` is unchanged on this branch.
- Console: `weather: feed unavailable` — there is no `/api` behind a static
  server.

## Files this branch touches

```
docs/asset-plans/560-third.md                      (new)
docs/asset-plans/README.md                         (+1 row)
artifacts/560-third/                               (new — asset, scripts, renders, optimize pass, QA)
app/public/sf-assets/landmarks/560-third.glb       (new)
app/public/sf-assets/landmarks_manifest.json       (+19 lines, appended)
pipeline/lib/landmarks.mjs                         (+1 entry)
```

All three shared files are append-only lists, so the branch merges mechanically
alongside its siblings. The city is re-baked once for the whole batch by
`docs/asset-pipeline/BATCH-INTEGRATE.md`.
