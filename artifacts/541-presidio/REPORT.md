# 541 Presidio Boulevard — build report

A validated miniature GLB of Building 541, Presidio of San Francisco — a
World War I–era officer's family quarters, one of the row 540–551 on the curve of
Presidio Boulevard. Cream stucco, red barrel-tile hip roof, one-storey front porch,
two stucco chimneys. **`validation.json` overall: PASS** (16/16 checks).

Built from `docs/asset-plans/541-presidio.md`; research re-verified in
`REFERENCE.md`. Where this report and the plan disagree, **this report is right**.

## Shipped numbers

| | |
|---|---|
| File | `541-presidio.glb` — **100,200 B** raw (post-optimize; see `optimize/REPORT.md`) |
| Triangles | **3,404** (cap 8,000) |
| Mesh objects | **8** (77 as authored, joined per material by the stage-4 pass) |
| Draw submeshes | **8** |
| Dimensions (axis-aligned) | 22.259 × 25.099 × 10.000 m |
| Building dimensions (own axes) | 19.77 × 11.65 m main block + 9.68 × 1.75 m porch |
| Min Z | 0.000 |
| XY centre offset | 0.000, 0.000 |
| Crest | exactly 10.000 m (loader scale = 1.0) |
| Eave / ridge | 7.20 m / 9.60 m, pitch ≈ 20° |
| Plinth | 0.90 m |
| Long axis heading | 30.68° true; front elevation faces 120.68° |
| Anchor | `-122.4518601, 37.7969312` |
| Materials | 8, all `Toy_*`; 2 `_Glow` |
| Textures / transparency / cameras / lights / animation | none |

## Sources re-verified before modelling

| Item | Plan said | Verified | Result |
|---|---|---|---|
| Footprint | 250.7 m², OBB 14.27 × 19.77 m | OSM way `288361187` re-pulled via Overpass, reprojected, min-area OBB refitted | confirmed |
| Anchor | `-122.4518601, 37.7969312` | main-block centre recomputed | confirmed |
| Crest | 10.0 m | DataSF LiDAR `201006.0016742`, `hgt_maxcm` 1004 | confirmed (10.04 → shipped 10.0) |
| Median roof | 8.16 m | same, `hgt_mediancm` 816 | confirmed |
| Ground pad | level | `gnd_rangecm` 84, σ 12 cm over 992 cells | confirmed — flat base, no stepped plinth |
| Orientation | long axis 30.68°, front at 120.68° | OBB principal direction; Presidio Blvd lies east of the house | confirmed |
| Style | Mission Revival, white stucco + barrel tile | ACHP Section 213 report, Bldgs. 540–551 | confirmed |
| OSM `height=8` | not the crest | equals the LiDAR **median** to within 0.16 m | confirmed as a trap; not used |

No dossier value had to be corrected. The plan's research held up; the corrections
below are all *design and rig* changes made during review, plus two predicted
numbers that came out differently.

## Deviations from the plan, and why

1. **Chimneys pierce the roof slopes instead of sitting on the ridge**
   (plan §2.7 step 10). On the ridge, a stack capped at the 10.0 m crest shows only
   **0.4 m** of stucco and rendered as a pair of tiny white blocks in the first
   aerial review — invisible at app scale, which defeats the point of cue #4. Moved
   to `(u, v) = (−3.60, +2.60)` and `(+3.60, −2.60)`, where the roof surface is at
   8.64 m, so the same stack reads as a **1.36 m** chimney and still tops out at
   exactly 10.0 m. Piercing the slope is also the commoner real configuration, and
   diagonally opposed placement means both read from any orbit azimuth. Section
   enlarged 0.90 × 0.70 → **1.00 × 0.80 m** for the same reason.
2. **Porch ridge raised 4.05 → 4.35 m** (≈30°, against the main roof's ≈20°). Over
   a 2.3 m span the main pitch renders as a flat awning from above; the porch hip is
   a named identity cue (§2.9, "do not delete it to save triangles") and has to be
   legible in the top view.
3. **Aerial camera radius 2.15 → 3.20 × span.** The 2.15 multiplier was inherited
   from `1008-general-kennedy`, where the subject is 55 m long; on a 25 m house it
   cropped the beauty render into an architectural close-up rather than a diorama
   view.
4. **Axis-aligned bbox is 22.26 × 25.10 m, not the plan's predicted ~21.6 × 24.3 m.**
   The plan's estimate under-counted: the main roof's eave rectangle
   (21.17 × 13.05 m, i.e. the block plus 0.70 m overhang on all four sides) sets
   *both* world extremes, and its corners are further out than the walls. Not a scale
   error — the validator's dimension check was written to this figure.
5. **Anchor shift came out as 0.000, 0.000**, where the plan expected the porch to
   pull the bbox centre ~0.7 m toward the boulevard. Because the main roof's eave
   rectangle is symmetric about the main-block centre and its corners dominate the
   AABB in both axes, the porch and rear bay both fall *inside* it. So the shipped
   anchor is the measured main-block centre unchanged — which is the better outcome:
   the manifest anchor is a directly measured quantity, not a derived one.
6. **Elevation cameras are aligned to the building's axes, not to compass north.**
   The house sits 30.68° off the world axes, so true-compass elevations would all be
   oblique three-quarters and a reviewer could not compare opposite faces. Filenames
   keep the nearest compass name for each face: `-east` = front (120.68°, the porch),
   `-west` = rear (300.68°, the bay), `-north` = end toward 542 (30.68°), `-south` =
   end toward 540 (210.68°). Stated here and in the render script's docstring so the
   labels are not read as true bearings.
7. **The triangle cap did not bind.** The plan said it should; at 3,404 of 8,000 it
   does not. The massing is genuinely simple (six volumes and two hip solids) and the
   window rhythm is modest (31 openings). Nothing was cut to reach this number and
   nothing was padded to approach the cap. Headroom is available if the open question
   about the front projection (below) resolves toward a full-height bay.
8. **Chimney material is `Toy_stone`, not `Toy_brick`.** Already argued in plan
   §2.8: these stacks are stuccoed to match the walls, so terracotta would be wrong
   here even though 1008 uses it. `Toy_stone` keeps them a half-value darker than
   `Toy_white` so they still separate from directly above.
9. **Roof stays `Toy_red` (`#c4453c`).** Cooler and more saturated than real
   weathered barrel tile, as the plan flagged, but kept for consistency with
   `1008-general-kennedy`. The plan's rule was "change both assets or neither"; this
   pass changes neither.

## Review iterations

| # | What the aerial showed | Change |
|---|---|---|
| 1 | Framing cropped to a close-up; chimneys read as 0.4 m stubs; porch roof read as a flat awning | Camera radius 2.15 → 3.20 × span; chimneys onto the slopes and enlarged; porch ridge 4.05 → 4.35 |
| 2 | Chimneys read as real stacks with shadows; porch hip legible in top view; hip lines crisp; eave shadow deep | accepted |

## Night state

Three lit windows plus the porch soffit, all on the front elevation: two upper-tier
windows (bays 1 and 3) and one porch window beside the entrance, in
`Toy_glass_Glow`, plus a `Toy_trim_Glow` shell under the porch eave. Glow surfaces
are thin shells **proud of** the opaque glazing, so the app's day pass (≈12% alpha)
reads the solid `Toy_glass` behind them. The roof does not glow.

Three of 31 openings is deliberate: this is a single-family house on a quiet Presidio
street, and a fully lit twelve-window box would read as an institution.

## Stage 4 — optimize (shipped numbers)

`541-presidio.glb` in this directory is now the **optimized** build; the
pre-optimize original is archived at `optimize/input/541-presidio.glb`. Full detail
in [`optimize/REPORT.md`](./optimize/REPORT.md). Headlines:

| | Authored | Shipped |
|---|---|---|
| File, raw | 220,396 B | **100,200 B** (−54.5%) |
| File, gzip −9 | 32,615 B | 64,888 B (+99% — meshopt resists gzip) |
| Triangles | 3,404 | 3,404 (unchanged) |
| Objects / draw submeshes | 77 | **8** (−89.6%) |
| Materials | 8 | 8 |
| BBox / origin | — | identical to 1e-5 m |

All eight optimize gates pass (G7 N/A, G6 PASS-with-note at −54.5% against a 60%
aspiration). Appearance delta ≤ 0.11% mean across day/night × near/far. The shipped
file carries `EXT_meshopt_compression` with **no** quantization and 0 node
transforms, which is what keeps the runtime merge working — and it is byte-for-byte
the output `pipeline/compress-assets.mjs` would produce, so the mandatory intake
compression is already done. **Do not re-compress at integration.**

`validation.json` in this directory has been regenerated against the shipped file:
`overall: PASS`, 16/16.

## Deliverables

```
artifacts/541-presidio/
  541-presidio.glb                 the asset
  541-presidio.blend               source scene
  build_541_presidio.py            deterministic build
  render_541_presidio.py           review render rig (day; --night)
  validate_541_presidio.py         fresh-scene contract validation
  make_contact_sheet.py            contact sheet composition
  validation.json                  PASS, 16/16
  REFERENCE.md                     research dossier
  REPORT.md                        this file
  541-presidio-east.png            front elevation (120.68°)
  541-presidio-west.png            rear elevation (300.68°)
  541-presidio-north.png           end toward 542 (30.68°)
  541-presidio-south.png           end toward 540 (210.68°)
  541-presidio-top.png             roof plan, building-aligned
  541-presidio-aerial.png          three-quarter aerial, day
  541-presidio-aerial-night.png    three-quarter aerial, night
  541-presidio-contact-sheet.png   all seven views
```

Rebuild: `blender -b --python build_541_presidio.py`
Re-render: `blender -b --python render_541_presidio.py` (then `-- --night`)
Re-validate: `blender -b --python validate_541_presidio.py`

## Manifest draft

Not applied here — integration is a separate stage.

```json
{
  "id": "541-presidio",
  "file": "541-presidio.glb",
  "anchor": [
    -122.4518601,
    37.7969312
  ],
  "targetHeightM": 10.0,
  "cat": 1,
  "name": "541 Presidio Boulevard",
  "estimated": true,
  "dims": [
    22.259,
    25.099,
    10.0
  ],
  "tris": 3404,
  "loadRadius": 2500
}
```

`"estimated": true` because the crest is derived from 2010 city LiDAR rather than
published, and the eave, ridge and pitch are inferred from it.

## Stage 5 — integration (local)

Case **B** (new landmark: no procedural builder, no registry entry existed).

Files changed: `app/public/sf-assets/landmarks/541-presidio.glb` (new),
`app/public/sf-assets/landmarks_manifest.json` (+1 entry),
`pipeline/lib/landmarks.mjs` (+1 `LANDMARKS` entry, `id: '541Presidio'`).

### Verified headlessly

| Item | Result |
|---|---|
| Re-validation of the shipped GLB (fresh scene) | **PASS** — 16/16, 3,404 tris, crest 10.000 m |
| GLB parses via pinned three + MeshoptDecoder | **PASS** — 8 meshes, 8 materials, no decode errors |
| id round-trip `camelId('541-presidio')` → `541Presidio` | **PASS** — matches the registry id exactly |
| Loader scale `targetHeightM / size.y` | **PASS** — exactly **1.0000** |
| Manifest `dims`/`tris` vs the GLB | **PASS** — match to 1e-2 m / exact |
| Under the 30k landmark triangle cap | **PASS** — 3,404 |
| Glow set separate after meshopt | **PASS** — `Toy_glass_Glow`, `Toy_trim_Glow` |
| `loadRadius` decision | **PASS** — 2500, the `max(2500, 10 × 30)` floor; **not** `alwaysLoaded` (a 10 m house never should be) |
| Exclusion radius sized against the real baked tile | **PASS** — see below |
| `npm run lint` | **PASS** — clean |
| `npm run build` | **PASS** — built in 3.3 s |
| No generated tiles hand-edited | **PASS** — `git status app/public/tiles/` empty |

### The exclusion radius, verified against the baked tile

Rather than trust the plan's arithmetic, the committed tile that contains this site
(`app/public/tiles/buildings/13_10.bin`, cell origin −1500, −3000, 65 footprints) was
parsed directly and every footprint measured against the anchor:

| Footprint | Nearest ring vertex | Centroid | Height | Inside `exclude: 12`? |
|---|---|---|---|---|
| idx 39 — **the baked 541 twin** (12-vertex ring, matches the OSM ring) | 6.70 m | **1.15 m** | 10.7 m | **yes** — dropped |
| idx 33 — the 540 twin | **18.40 m** | 29.45 m | 9.7 m | no — survives, 6.4 m clear |
| idx 22 | 26.75 m | 31.64 m | 13.3 m | no |
| idx 35 | 46.40 m | 58.20 m | 10.1 m | no |

`excluded()` in `pipeline/buildings.mjs` drops a footprint whose centroid **or any ring
vertex** is inside the radius, so `exclude: 12` removes exactly one footprint — the
541 twin, on its 1.15 m centroid — and the nearest survivor is 6.4 m clear. The
measurement also confirms the OSM-derived prediction (18.86 m predicted for 540 vs
18.40 m in the bake: 0.46 m agreement).

This corrected the plan's original `exclude: 14`, which had been sized on
centroid distance only; §2.13 of the plan is updated with the right metric.

### Case B re-bake — DONE

Run after the first pass of this report claimed it could not be. The full chain
(`download`, `loredata`, `terrain`, `bridges`, `buildings`, `streets`, `landcover`,
`validate`, `lore`, `toy`, `notables`, `context`) was re-run against Overture release
**2026-07-22.0** — the same release the previous bake used, so nothing drifted.

Scope, verified by sha256 over all 3,922 tile files before and after:

| | |
|---|---|
| Buildings | **174,769 vs 174,770** — exactly one footprint dropped |
| Overture contribution | unchanged: 3,351 added, 263 heights corrected |
| Cells / tallest | unchanged: 585 cells, 244 m |
| Binary tiles changed | **only cell `13_10`**, in `buildings/`, `landcover/`, `toy/`, `toyland/` |
| `ctx/*.json` changed | 584 of 596 — a **pure global-index renumber** (see below) |
| `api/_data/search-index.json` | +1 entry: 541 Presidio Boulevard is now searchable |
| `audit.mjs` check **1.6** | **PASS** — 29 landmarks clear |
| `pipeline validate` | **PASS** — lists "541 Presidio Boulevard — cell 13_10" |

**Why 584 sidecars changed, and why it is benign.** `ctx/*.json` keys buildings by
*global* index, so removing one footprint shifts every later index down by 1. Verified
shift-aware on a cell far from the Presidio (SoMa `23_13`): of 233 buildings, 34 keep
their index and 199 shift by exactly 1, and **zero have any content difference**. A
naive key-wise diff appears to show two buildings with changed fields; that is an
artifact of comparing index *N* across the renumber (old #N+1 became new #N), not real
drift.

**Three audit checks fail, and they are pre-existing:** 1.2b (95th-percentile height
outside a 25–120 m band, measured 13.9 m — the check's own message notes the DataSF
source p95 is 12.4 m median-roof / 15.7 m ridge, so the band does not match the source
at all), 1.3c (Telegraph Hill 90.5 m from the Terrarium DEM against a surveyed 84 m),
and 1.7b (1 of 793 sampled trees more than 30 m offshore). None touches the Presidio,
and removing one 10.7 m building cannot move a city-wide p95 by 11 m. Reported rather
than hidden.

### NOT verified — outstanding

| Item | Status | Why |
|---|---|---|
| In-app QA: single-building check, orientation on terrain, terrain seating, night glow sweep, draw calls < 300, console merge line | **NOT RUN** | The browser-preview tool caps dev servers at 5 per folder and 5 are already held by parallel sessions in this repo. |
| Mandatory fallback drill | **NOT RUN** | Same reason — it requires observing the app's console warning. |
| Deployed production QA | **NOT RUN** | Correctly gated behind the user's ship decision. |

### Note for whoever merges

A parallel session in this repo is working on **540 Presidio Boulevard** — the
immediate neighbour in the same row (a `sf-3d-540-presidio` dev server is registered
against `.claude/worktrees/540-presidio-blvd`). Expect textual merge conflicts with
this branch in `landmarks_manifest.json` and `pipeline/lib/landmarks.mjs`, both of
which are append-at-the-end. The two exclusion zones do not overlap: 12 m radii
around anchors ~30 m apart, and each measured clear of the other's footprint by 6+ m.

## Open questions carried forward

Unchanged from plan §2.15 and `REFERENCE.md`; none of them blocks this asset, and
all of them would be settled by one elevation drawing of any house in the row:

1. **Whether the front projection is a porch, an enclosed sun porch, or a
   full-height bay.** Modelled as a one-storey porch. The extent is measured; the
   reading is not. A full-height bay would change the roof plan (cross hip) and is
   the only one of these that would need a rebuild rather than a tweak.
2. Chimney count and position — two, on the slopes, is inferred.
3. Ridge, eave and pitch are inferred from the LiDAR crest/median pair.
4. Window counts (5/5/3/3 per tier) are designed rhythms, not photographic counts.
5. Construction year within 1915–1918 is not pinned to Building 541.
6. Duplex vs single-family; shipped as `cat: 1` (house).

## Gate 2

`validation.json` `overall: PASS`, all 16 checks true, fresh-scene re-import of the
exported GLB. Triangles 3,404 / 8,000. Crest 10.000 m. Normals outward by
per-object signed volume (77/77) with a 0.0000 ray residual.

## Gate 3 — approval

Approval was given in advance for every stage of the pipeline run, 2026-08-12.
Quoted verbatim:

> Do it on a new branch and PR -- i approve all stages just proceed

Presented at the time of approval: the contact sheet (all seven views), the day and
night three-quarter aerials, and the shipped numbers table above. No revision was
requested, so there is one build iteration on record (the two-step review in
"Review iterations", both self-directed).

Because the approval was blanket and given before the renders existed, the open
questions in the section below — chiefly whether the front projection is a porch or
a full-height bay — have **not** been ruled on by a human. They remain open.
