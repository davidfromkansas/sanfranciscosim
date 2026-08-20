# Ferry Station Post Office Building — stage 5 integration report (batch mode)

`docs/asset-plans/INTEGRATION-PROMPT.md` Part 1, executed 18 August 2026 against
`artifacts/ferry-station-post-office/`. **Case B** — new landmark, so a registry
entry and a full tile re-bake were required.

`BATCH: yes`, so per `ADDRESS-TO-ASSET.md` the bake was run and used for the
Step 5/6 QA and then **thrown away**; this branch commits source only.

## Step 1 — re-validation of the shipped GLB

Fresh isolated Blender scene, re-importing the exported file, not the source
`.blend` (`validate_ferry_station_post_office.py`, `validation.json`
`overall: PASS`):

| Check | Measured |
|---|---|
| Triangles | 11,596 (cap 27,000; this asset's own cap 15,000) |
| Objects / draw primitives | 13 / 15 |
| min Z | 0.0 |
| XY centre offset | (−0.158, −0.253) m |
| Dimensions | 69.8386 × 65.2024 × **12.650** m |
| `targetHeightM / measuredHeight` | **1.000000** |
| Materials | 11, all `Toy_*`, flat, no texture, no transparency, no `Toy_body` |
| `_Glow` | 2 — `Toy_gold_Glow` (entrance), `Toy_glassl_Glow` (4 first-floor bays) |
| Cameras / lights / animation / armatures / foreign geometry | 0 / 0 / 0 / 0 / none |
| Normals | 0 inverted signed volumes; ray residual 0.0% over 31,500 rays |

## Step 2 — asset in place

`app/public/sf-assets/landmarks/ferry-station-post-office.glb`, byte-identical to
`artifacts/ferry-station-post-office/ferry-station-post-office.glb` (309,136
bytes, already meshopt-compressed by stage 4 — not re-exported, not re-compressed).

## Step 3 — manifest entry

Appended as **text**, not by re-serialising the JSON: a `JSON.stringify` /
`json.dump` round trip rewrites `11.0` to `11` across other landmarks' entries and
turns a one-entry change into a whole-file diff. The result is a pure 19-line
append, 0 deletions.

```json
{
  "id": "ferry-station-post-office",
  "file": "ferry-station-post-office.glb",
  "anchor": [-122.3921505, 37.7941368],
  "targetHeightM": 12.65,
  "cat": 18,
  "name": "Ferry Station Post Office Building (Agriculture Building)",
  "estimated": false,
  "dims": [69.8386, 65.2024, 12.65],
  "tris": 11596,
  "loadRadius": 2500
}
```

- **`loadRadius: 2500`, explicitly decided.** The default rule is
  `max(2500, targetHeightM × 30) = max(2500, 380) = 2500`. This is a 12.65 m
  building, nowhere near skyline scale, so `alwaysLoaded` would be wrong. Beyond
  2.5 km the site is empty ground (Case B) — at that range, 39 m of missing
  footprint on the Embarcadero edge is well under a pixel and illegible.
- **`estimated: false`.** The shipped height is the DataSF LiDAR maximum, a
  measurement, and it is corroborated by the same record's `peak_1st_m` minus
  ground. The *cornice* is photogrammetric and the two flat decks are inferred,
  but neither is the number in the manifest.
- **`cat: 18` = Government** (`CATEGORY_LABELS` in `app/src/context.js`). The
  building is Port of San Francisco property housing state offices; it was the
  California Department of Agriculture's from 1933.
- **id round trip verified**: `camelId('ferry-station-post-office')` →
  `ferryStationPostOffice`, which is the id added to `pipeline/lib/landmarks.mjs`.
  A mismatch here is what leaves two buildings on one site.

## Step 4 — Case B: registry + re-bake

Registry entry added to `LANDMARKS` in `pipeline/lib/landmarks.mjs` with
`exclude: 39` and `camera: { distance: 260, yaw: 290, pitch: 22 }`.

**A correction to the plan's camera:** `yaw` is *not* the frontage bearing. The
rig sets the eye to `pivot + (sin yaw, sin pitch, cos yaw)·distance` with `+z`
south, so the camera's compass bearing from the building is `180 − yaw`. Standing
the eye at bearing 250° — just off the frontage's 234° normal, so the SE flank and
the 1918 wing rake away behind the front — needs `yaw: 290`. The plan had said
234, which would have parked the camera on the north-west flank.

### Sizing `exclude`, measured against the bake's own source files

`excluded()` in `pipeline/buildings.mjs` drops a footprint whose centroid **or any
ring vertex** falls within the radius of the registry anchor. Measured directly
from `pipeline/data/buildings_datasf.geojson` and
`pipeline/data/overture_buildings.geojsonseq`, not from the Socrata API:

| Distance from anchor | Ring |
|---|---|
| 18.24 – **37.34 m** | this building's own DataSF ring, `mblr SF9900278` — the radius must clear 37.34 |
| 20.83 – 35.31 m | Overture's duplicate of the same building (`commercial`, height 15) |
| 29.93 m / 32.87 m | Overture's two ferry-gangway canopies (`outbuilding`, heights 8.7 m and 6.9 m) |
| **41.45 m** | nearest vertex of the next DataSF footprint, `CN9900002`, the Downtown Ferry Terminal kiosk — must survive |

Safe window **(37.34, 41.45) m**; **39** sits in it with 1.7 m below and 2.5 m
above.

### The collateral I predicted did not happen — and only the tile showed that

On the source data the two canopy rings sit *inside* any workable radius, so the
plan recorded them as unavoidable collateral. Decoding
`app/public/tiles/buildings/23_10.bin` and `24_10.bin` before and after says
otherwise: neither canopy reaches the baked city at all, because the cross-source
gap-fill never emits them.

| Cell | origin/main | this branch |
|---|---|---|
| `23_10` | 49 footprints, **1 penetrating the asset ring** (12.2 m tall), nearest vertex 18.25 m | 48 footprints, **0 penetrating**, nearest vertex 80.31 m |
| `24_10` | 4 footprints, 0 penetrating, nearest 41.45 m | identical |
| `23_11`, `22_10`, `22_11` | 72 / 164 / 127, 0 penetrating | identical |

**The exclusion drops exactly one baked footprint: this building's own.** No
collateral. This is why the check is *which* rings disappear rather than *how
many* — `verify-rebake.mjs` compares per-cell counts and reported `24_10`
"exclusion dropped nothing", which is true and would have been ambiguous on its
own.

### Audit and re-bake verification

`node pipeline/verify-rebake.mjs` → **PASS**

```
new since origin/main: ferryStationPostOffice @ 23_10+24_10
  584 of 585 cells unchanged
  23_10     49 -> 48   <- ferryStationPostOffice
  ok   ferryStationPostOffice 41.4 m vs 39 m radius  (nearest is 6.9 m tall)
PASS  only the new landmarks' cells moved, and every asset has clear ground under it
```

`node pipeline/audit.mjs` → check **1.6 PASS**: "no procedural footprint inside a
bespoke landmark exclusion zone — 100 zones over 97 landmarks clear".

The audit's three standing failures are **pre-existing and structurally
unrelated** to this change, and are reported rather than hidden:

- **1.2b** 95th-percentile height 25–120 m — reads 13.9 m. The check's own message
  says the DataSF *source* p95 is 12.4 m, i.e. the threshold is miscalibrated
  against the data. Removing one 12.65 m footprint from 174,695 cannot move a
  citywide p95.
- **1.3c** Telegraph Hill terrain 60–85 m — reads 90.5 m from the Terrarium DEM
  against a surveyed 84 m summit. Terrain is baked by `terrain.mjs` and is
  untouched by a buildings exclusion.
- **1.7b** one of 792 sampled trees more than 30 m offshore. Trees come from
  `landcover`/`toy`, not from the buildings tier.

The full chain was run in order — `terrain`, `bridges`, `buildings`, `streets`,
`landcover`, `validate`, `lore`, `toy`, `notables`, `context`, `muni-shapes` —
because `context.mjs` imports `LANDMARKS` and owns this landmark's pick box,
search-index row and `context/landmarks.json` identity, and `validate.mjs`'s
publish step drops `tiles/ctx/` and `tiles/context/` wholesale. `muni-shapes`
found no 511 key and correctly left the committed `muni-shapes.bin` alone.

### What the bake actually rewrote

593 generated files: 578 `tiles/ctx/*.json`, 3 `tiles/context/*`, 2 `api/_data/*`,
the four index JSONs, **1** `tiles/buildings/*.bin` (`23_10`) and **2**
`tiles/toy/*.bin` (`23_10`, `24_10`). The ~578 `ctx` files are expected and
correct: dropping one procedural footprint renumbers the global building ids their
pick lists reference. Only the three `.bin` files changed geometrically.

## Step 5 — local verification

Driven by `artifacts/ferry-station-post-office/qa_local.mjs`: the **built** app
(`app/dist`) served from a throwaway `node:http` server and driven in real
headless Chrome over CDP. The in-editor Browser pane was not used — a hidden pane
throttles `requestAnimationFrame` to nothing, which makes a perfectly healthy
streamed landmark look exactly like a broken `loadRadius`. Evidence in
`artifacts/ferry-station-post-office/qa/qa.json`.

| Check | Result | Evidence |
|---|---|---|
| Manifest entry loads and merges | **PASS** | `sf-assets: ferry-station-post-office merged 15 objects / 11 materials -> batched (6726 tris body); uniform x1.0000 at 3991, -2668` |
| Uniform scale ≈ 1.0 | **PASS** | **x1.0000** — the authored height and `targetHeightM` agree exactly |
| Placed at the real anchor | **PASS** | local (3991, −2668) against the computed anchor (3990.56, −2668.08) |
| Exactly one building on the site | **PASS** | no procedural twin and no baked block in the day frame; independently settled from the tile — 0 footprints penetrate the asset ring (was 1) |
| Footprint size against reality | **PASS** | the wide frame reads the 50.74 m frontage correctly against the Ferry Building and the Embarcadero carriageway |
| Orientation | **PASS** | the three-pavilion front faces the Embarcadero; `rig.yawDeg = 290`, i.e. the eye at bearing 250°, and the entrance is square to the street |
| Terrain seating | **PASS** | sits on the wharf edge, no floating, no sinking, water behind the rear as it should be |
| Night glow | **PASS** | only the intended surfaces light: the gold entrance transom (the hero) and four scattered first-floor bays. Roof, trim and rear stay dark |
| Draw calls | **PASS** | **87/frame** at the landmark, against the 300 budget (AGENTS rule 2) |
| Asset warnings | **PASS** | none |
| Streaming | **PASS** | `entries: 91, live: 62, loading: 1, fading: 0, failed: 0` |

Screenshots: `qa/day.png` (14:30 pinned with `SF.setClock`, not the live wall
clock), `qa/night.png` (21:45), `qa/wide.png` (900 m, showing the building as the
Ferry Building's low neighbour rather than a competitor to it).

The one console error in the run — `weather: feed unavailable, holding the last
known sky` — is the static dist server having no `/api`, not a defect.

## Step 6 — fallback drill (mandatory)

Run with `qa_local.mjs --drill`, which serves a **real 404** for
`/sf-assets/landmarks/ferry-station-post-office.glb` rather than renaming the
file. The rename trick cannot produce a fetch failure at all: Vite's dev server
and a dumb dist server both answer a missing public path with `index.html` and
HTTP 200. Serving a 404 is also reversible by construction — nothing on disk
moves, so a killed run cannot leave the asset displaced.

| Check | Result | Evidence |
|---|---|---|
| The loader actually reached for the file | **PASS** | `failed: 1`. This gate matters: `failed: 0` is meaningless if the camera never got within `loadRadius`, and an untouched entry reports far/live/failed exactly like a healthy miss |
| App still boots and the district renders | **PASS** | `entries: 91, far: 17, loading: 0, live: 73, fading: 0, failed: 1` — the other 73 landmarks merged normally |
| Exactly one fallback warning | **PASS** | `sf-assets: ferry-station-post-office failed to load (fetch for ".../ferry-station-post-office.glb" responded with 404: Not Found)` |
| Case B site is empty ground | **PASS** | `qa/drill-day.png` — the wharf surface, the Embarcadero, the streets, vehicles and residents all render; the footprint is bare, which is the expected Case B behaviour, not a hole |
| Budgets hold in the degraded state | **PASS** | 90 draw calls/frame |

**A note on the warning's wording, because the prompt is out of date here.**
`INTEGRATION-PROMPT.md` Step 6 says to expect one
`sf-assets: … — keeping the code-built landmark` line. That is the **resident**
path — `warn()` in `app/src/assets.js`, the single-shot helper. This landmark is
**streamed** (it has a `loadRadius`), and a streamed failure goes through `scan()`
instead, which deliberately does not use `warn()` and emits
`sf-assets: <id> failed to load (…)` with no "keeping" suffix. It is still
exactly once structurally: `place()` sets `status = 'failed'`, and no branch in
`scan()` matches `'failed'`, so the entry can never be retried or re-warned.
**Match the drill's filter on the asset id, not on the prompt's wording.**

Screenshots: `qa/drill-day.png`, `qa/drill-night.png`, results in
`qa/drill.json`.

## Batch mode — the bake was thrown away

`ADDRESS-TO-ASSET.md` "Batch mode": the re-bake was run and used for the Step 5/6
QA — a Case B landmark cannot be judged without its exclusion applied, because
the procedural block is often taller than the asset and an unbaked check shows
nothing wrong with a building that is in fact invisible — and then discarded:

```
git checkout -- app/public/tiles api/_data
```

This branch therefore commits **source only**: the GLB, its
`landmarks_manifest.json` entry, its `pipeline/lib/landmarks.mjs` entry, the asset
plan and `artifacts/ferry-station-post-office/`. Those are the only files a
landmark shares with its siblings, and all three shared ones are append-only lists
that merge mechanically. A bake rewrites ~600 generated files whatever landmark
triggered it, so two landmark branches that each commit one cannot be merged; the
batch is baked once by `docs/asset-pipeline/BATCH-INTEGRATE.md`, which is also
where the single PR is opened.

## Step 7 — replaced by a stop

Per `ADDRESS-TO-ASSET.md` stage 5, Step 7 (push, PR, deploy, production QA) is
replaced by a stop. `npm run lint` clean, `npm test` 26/26 passing, `npm run build`
succeeded. Committed locally. **Nothing pushed, no PR opened, no deploy.**

## Gate 5 — local QA table

| Item | Result |
|---|---|
| Step 1 re-validation (fresh scene, shipped GLB) | **PASS** |
| Manifest entry + explicit `loadRadius` decision | **PASS** |
| id ↔ `camelId` ↔ registry round trip | **PASS** |
| Case B registry entry | **PASS** |
| Case B re-bake | **PASS** — 584/585 cells unchanged, 1 buildings tile + 2 toy tiles changed geometrically |
| `audit.mjs` check 1.6 | **PASS** — 100 zones over 97 landmarks clear |
| `verify-rebake.mjs` | **PASS** — nearest surviving footprint 41.4 m vs the 39 m radius |
| Exactly one building on the site | **PASS** — settled from the tile: penetrating rings 1 → 0 |
| Uniform scale ≈ 1.0 | **PASS** — x1.0000 |
| Orientation | **PASS** |
| Terrain seating | **PASS** |
| Night glow | **PASS** |
| Draw calls < 300 | **PASS** — 87/frame (90 in the drill) |
| Fallback drill | **PASS** — `failed: 1`, app boots, one warning, empty ground |
| `npm run lint` / `npm test` / `npm run build` | **PASS** / 26 of 26 / **PASS** |
| Batch sanity: nothing under `app/public/tiles/` or `api/_data/` | **PASS** |

## Branch state at hand-off

`pipeline/ferry-station-post-office`, branched from `origin/main` at `335cb9ac1`.

**`origin/main` advanced to `2c14d5f9f` while this ran** (another batch merged).
A dry-run merge reports three conflicts, all of them the expected
both-sides-appended kind in the append-only lists:

- `app/public/sf-assets/landmarks_manifest.json`
- `pipeline/lib/landmarks.mjs`
- `docs/asset-plans/README.md`

They are textual tail collisions, not semantic ones — each side adds a distinct
entry — and resolving them is the batch-integrate step's job, not this branch's.

## Not done, by design

Push, PR, deploy and production QA on https://sf-3d.vercel.app are **not** done
and are waiting on an explicit instruction. So is the batch bake — this branch
carries no generated tiles.
