# 2 Folsom Street — build report

`artifacts/2-folsom/2-folsom.glb` — a validated miniature of the Gap Inc. headquarters
(Robert A.M. Stern Architects with Gensler, 2001) at 2 Folsom Street / 250 Embarcadero,
San Francisco, for the SF-SIM toy-diorama city.

**REPORT beats plan.** Where this file disagrees with `docs/asset-plans/2-folsom.md`, this
file is what was built and verified. Corrections are listed in §4.

## 1. Shipped numbers

Updated to the **post-optimize** figures (stage 4 ran on 19 August 2026 and its output is
now the shipping file — see `optimize/REPORT.md`).

| | shipped | pre-optimize |
|---|---|---|
| Objects | **14** | 801 |
| Draw submeshes | **16** | 806 |
| Triangles | **16,996** | 16,996 |
| Dimensions (axis-aligned) | 113.92 x 113.96 x **88.00** m | identical |
| `min Z` | 0.000 m | identical |
| XY centre offset of the AABB | (1.455, 1.427) m — see §2 | identical |
| Materials | 13, all `Toy_*`, flat, no textures, no alpha | identical |
| Glow materials | `Toy_glassl_Glow`, `Toy_glass_Glow`, `Toy_gold_Glow` | identical |
| Normals | PASS — signed volume outward on every solid, ray-cast flipped fraction **0.000000** | identical |
| File | **494,180 B** raw (meshopt) / 257,150 B gzip | 1,248,312 B / 165,765 B |
| Validation | `validation.json` — **overall PASS**, all 16 checks, re-run against the shipped meshopt file | — |

494.2 KB is inside the 500 KB on-disk landmark budget. Getting there took three trims of
the build script, not a better packer — the reasoning is in `optimize/REPORT.md` §6.

Anchor `-122.390975, 37.790787`; `targetHeightM` **88.0**, so the loader's
`targetHeightM / measuredHeight` scale lands at exactly 1.0000.

## 2. Two numbers that look wrong and are not

**The axis-aligned bounding box is 113.9 m for an 84.31 x 77.14 m building.** That is the
consequence of the real 44.81 deg heading — the asset is authored in true-world
orientation because `placeGeneric()` applies no rotation. Expected, not a scale error.

**The AABB centre sits 2.04 m from the origin**, above the usual ~1 m guidance. The
footprint is genuinely asymmetric: the two Embarcadero-side corners are square and the
two Spear-side corners step in 4.7 m. The **origin** is what the loader uses — it composes
the placement matrix at the anchor and does no recentring — and the origin is the surveyed
OBB centre of the DataSF footprint. Recentring the geometry on its AABB would have moved
the building 2 m off its real site, which AGENTS rule 5 forbids. `validate_2_folsom.py`'s
`centered_xy` tolerance was widened to 2.5 m with that reasoning recorded inline.

## 3. What was built, and why

Three masses, all three heights measured from one DataSF LiDAR row (25,463 cells at 50 cm):

| Mass | Plan | Top | Source of the height |
|---|---|---|---|
| Base, whole block | 84.31 x 77.14 m | **32.30 m** | `hgt_median 32.28` |
| Brick superstructure | 34 x 44 m, set 16 m southwest of the block centre | **72.10 m** | `hgt_majority 72.11` |
| Limestone tower, two setbacks + crown | 20 x 20 m at the superstructure's northeast corner | **88.00 m** | `hgt_max 87.95` |

The area split behind those plan sizes was solved from the same row's mean and sigma and
cross-checked against a de-projected satellite and against two OSM `building:part` rings —
the derivation is in `REFERENCE.md` §3.

The **mid-block Folsom entrance recess** (13.59 x 3.02 m) and the **Embarcadero central
projecting pavilion** (15.15 m) are in the surveyed ring itself, not invented: RAMSA's
"mid block entrance on Folsom Street" and the porticoes "at its boldest facing the harbor"
are both readable in the survey.

Facades are **piers + continuous spandrel bands + glass fills**, not 235 individually
framed openings. That is a third of the triangles for a better read, and it matches
RAMSA's description of "large, simple, structural frames".

Night state: the **atrium skylight** is the hero glow — one softly lit rectangle on a dark
roof plane, which is what the building actually looks like from the Bay Bridge — supported
by a scatter of lit windows, the crown pavilion's glazing, and the 2022 ground-floor
retail sign band on both entrance porticoes. The limestone tower does not glow. All glow
surfaces are thin shells proud of the opaque surface behind them.

## 4. Corrections to the plan made during the build

1. **The plan's footprint corners are the plain OBB; the build uses the real 24-vertex
   ring.** The plan's §2.3 gives four corners and says "model the jogs as 1.5-2.5 m
   chamfers". The survey is not chamfered: it has two mid-face entrance recesses ~3 m
   deep, a five-plane symmetric composition on the Embarcadero face, and 4.7 m
   rectangular steps at the two Spear-side corners only. All of that is modelled as
   surveyed; nothing was chamfered.
2. **The superstructure is 34 x 44 m, not 42 x 42.** The plan sized one box; the build
   splits the mass into a brick block (34 x 44) plus a limestone tower (20 x 20) standing
   proud of its northeast corner, whose union is 44 x 44 m. That reproduces both the LiDAR
   deck area (1,496 m2 built vs 1,467 m2 solved) and the above-72 m area (400 vs 402)
   simultaneously, which one box could not.
3. **The plan's tower shaft was to run full height from the terrace inside the
   superstructure.** Buried there it would have been invisible. It is now adjacent and
   overlapping, so the limestone reads as a distinct mass from the terrace up — which is
   what the 2010 elevation photograph shows.
4. **Bay counts are lower than planned.** The plan proposed ~6.5 m pitch (12 bays on the
   long faces); the build uses ~7.5-8.5 m. The first aerial review showed a window grid
   too fine to read at city scale, and the pitch change also paid for the triangles the
   missing northwest plane needed (§5.3).
5. **`Toy_trim` was added** to the plan's palette list as the parapet-coping and
   tower-setback-ledge colour. Without a half-tone above `Toy_stone`, the three mass
   transitions vanished when viewed from directly overhead.

## 5. Iteration log

1. **Build 1 (33,196 tris).** Over budget by 38%. Bands and rings were carrying 2-segment
   bevels worth ~7,900 triangles on features 0.12-0.28 m proud, which are sub-pixel at
   city scale. Bevels dropped on the spandrel bands and reduced to one segment on the
   24-vertex cornice/parapet/coping rings. → 23,620.
2. **Orientation bug, caught in the first aerial render.** The `(u, v) -> world` map was
   written as a rotation when the footprint's source frame has `z = -north`, so the map
   must be a **reflection**. The whole building was rotated 90 degrees — the Embarcadero
   elevation was facing Folsom Street — and, because the determinant sign also decides the
   polygon winding, every applied panel was being extruded along an inward normal. One
   sign fixed both. **This is the failure mode to look for first when a 45-degree SoMa
   asset looks subtly wrong: check the determinant of the plan-to-world map, not the
   geometry.**
3. **Second aerial review: the brick had disappeared.** Limestone piers 1.40 m wide on a
   7.5 m bay plus 0.55 m full-width spandrel bands plus 5.8 m openings left almost no
   brick, and the two-material split is half the identity. Piers to 1.15 m, bands to
   0.28 m, openings to 0.46 x bay, sill raised — brick now holds about half the wall.
   Porticoes enlarged from 9.0 x 7.4 m to 11.4 x 9.6 m; they had read as grilles.
   Crenellation reduced from an inset cluster to eight 3 m blocks on the parapet line in
   `Toy_trim`, because the crest had merged into the shaft.
4. **Third review, north elevation: a blank 33 m brick panel.** One long wall plane of the
   northwest elevation (edge 23) had been left out of the bay table — every other plane
   was articulated, so it read as a hole in an otherwise complete facade. Added at 4 bays;
   one bay each removed from the two Embarcadero flanks and one from Spear to stay under
   the cap. → **23,852**.
5. **Stage 4 sent it back three more times.** The first optimize run passed every gate and
   still produced a 721 KB file — 44% over the 500 KB landmark budget — because packing
   cannot fix geometry. The bevel policy was tightened until no applied panel carries one
   (`inspect.json` measures one screen pixel at the near landmark distance as 0.115 m, so
   a 0.05 m bevel on a 0.18 m proud pier was buying nothing), the bay pitch widened from
   ~6.2 m to ~8.5 m, the tower's window bands went 9 → 8 and its second setback 3 bays →
   2, and the skylight rib grid 6x5 → 5x4. **23,852 → 16,996 triangles**, and the same
   optimize chain then landed at 494 KB.
6. Re-rendered all six day views, the night view and the contact sheet from the final
   export; revalidated in a fresh scene, then again against the shipped meshopt file.
   **PASS both times.**

## 6. Deliverables

```
artifacts/2-folsom/
  build_2_folsom.py        deterministic build (Blender 5.2 LTS, headless)
  render_2_folsom.py       controlled review renders, re-imports the GLB
  validate_2_folsom.py     fresh-scene contract validation
  make_contact_sheet.py
  2-folsom.blend
  2-folsom.glb             the shipping asset
  2-folsom-{north,east,south,west,top,aerial}.png
  2-folsom-aerial-night.png
  2-folsom-contact-sheet.png
  validation.json
  REFERENCE.md             sources and verified facts
  REPORT.md                this file
```

Rebuild end to end:

```bash
cd artifacts/2-folsom && /Applications/Blender.app/Contents/MacOS/Blender -b --python build_2_folsom.py && /Applications/Blender.app/Contents/MacOS/Blender -b --python render_2_folsom.py && /Applications/Blender.app/Contents/MacOS/Blender -b --python render_2_folsom.py -- --night && python3 make_contact_sheet.py && /Applications/Blender.app/Contents/MacOS/Blender -b --python validate_2_folsom.py
```

## 7. Draft manifest entry

```json
{
  "id": "2-folsom",
  "file": "2-folsom.glb",
  "anchor": [-122.390975, 37.790787],
  "targetHeightM": 88.0,
  "cat": 3,
  "name": "2 Folsom Street (Gap Inc. headquarters)",
  "estimated": false,
  "dims": [113.9196, 113.9579, 88.0],
  "tris": 16996,
  "loadRadius": 2640
}
```

`"estimated": false`: all three roof planes are LiDAR measurements over 25,463 cells and
the crown is independently corroborated by OSM's `height` tag. `loadRadius` is the default
formula, `max(2500, 88.0 * 30) = 2640`. `dims` and `tris` are the **shipped** figures.

## 8. Approval

Approved 19 August 2026. The user's instruction opening this pipeline session was, quoted
verbatim:

> "APPROVE EVERYTHING DONT ASK ME FOR PERMISSION"

The stage-3 gate was therefore granted in advance rather than after the fact. The contact
sheet, the aerial day and night renders and the numbers in §1 were still presented before
the pipeline advanced, so the evidence exists even though no confirmation was waited for.

## 9. Stage 5 — integration (batch mode)

Run of `docs/asset-plans/INTEGRATION-PROMPT.md` Part 1 with `<slug> 2-folsom`,
`<Name> 2 Folsom Street (Gap Inc. headquarters)`, **Case B**. Batch mode: the re-bake was
run and QA'd, then discarded, and this branch carries source only.

### 9.1 What went in

| File | Change |
|---|---|
| `app/public/sf-assets/landmarks/2-folsom.glb` | the shipped meshopt asset, byte-identical to `artifacts/2-folsom/2-folsom.glb` |
| `app/public/sf-assets/landmarks_manifest.json` | one appended entry, **19 insertions, 0 deletions** — appended as TEXT, never re-serialised, because `JSON.stringify` rewrites `11.0` to `11` across six other landmarks' `targetHeightM` and `dims` |
| `pipeline/lib/landmarks.mjs` | one `LANDMARKS` entry, `id: '2Folsom'`, `exclude: 60`, camera preset |
| `artifacts/2-folsom/qa_local.mjs` | the stage-5 QA harness for this asset |

`camelId('2-folsom')` = `2Folsom`, which is the registry id — verified, so the loader
finds the landmark it is meant to replace. There is no procedural builder for it in
`app/src/landmarks.js` (Case B), so nothing is being hidden and the fallback state is bare
ground inside the exclusion zone.

`loadRadius: 2640` = the default `max(2500, 88.0 * 30)`. **Not** `alwaysLoaded`: at 88 m
this is well below skyline scale, and the shared batch is the scarce resource (§9.4).

### 9.2 The exclusion, measured

`exclude: 60` m, chosen against the real bake inputs and then verified against the baked
tile rather than against a count.

| | distance from the anchor |
|---|---|
| this footprint, DataSF `201006.0000175` | centroid **0.10 m**, vertices 35.64-57.04 m |
| this footprint, Overture `d31f359f` | centroid 2.26 m, vertices 34.98-56.83 m |
| the asset's own furthest corner | 57.14 m |
| **nearest neighbour vertex** | **66.93 m** (Overture `98232020`, the 17.2 m block across Folsom) |
| then | 69.53 m (MIRA), 70.10 m, 71.23 m (201 Spear) |

Safe window (0.10, 66.93). 60 m sits 2.9 m outside the asset's own corners and 6.9 m
inside the nearest neighbour. `excluded()` in `pipeline/buildings.mjs` fires on the
centroid **or** any ring vertex, so both were measured.

**Only one footprint was ever baked here, not two.** Both sources trace this building, but
`buildings.mjs` takes Overture as gap-fill, so a footprint DataSF already has is not added
again. Measured origin/main → this branch across cells `23_11` + `24_11`: **98 → 97**
footprints, a delta of exactly one. The plan's §2.13 and the first draft of the registry
comment both assumed two; corrected.

**The dropped block topped out at 94.5 m** — 6.5 m taller than the 88.0 m asset. That is
why a Case B landmark cannot be judged without its re-bake applied: unexcluded, the
procedural building swallows the GLB whole and the asset simply never appears. It is also
why the exclusion was verified by decoding the tile, not by `verify-rebake.mjs`'s per-cell
counts alone.

After the bake, in cells `23_11` + `24_11`:

- footprints with any vertex inside r=60: **0**
- nearest surviving footprint vertex to the anchor: **67.86 m**

### 9.3 What the re-bake touched

Ran `terrain, bridges, buildings, streets, landcover, validate, lore, toy, notables,
context, muni-shapes` — the whole chain, because `context.mjs` imports `LANDMARKS` and
owns this landmark's pick box, its search-index entry and its `context/landmarks.json`
row, and `validate.mjs`'s publish step drops `app/public/tiles/ctx/` and `context/`.

`pipeline/data/` was not re-downloaded: it was hardlinked from an existing worktree's
identical snapshot, so the bake ran against the same inputs as `origin/main` and nothing
churned for data-vintage reasons. That is visible in the diff — only the cells this
landmark touches moved.

### 9.4 Shared BatchedMesh headroom — a note for the batch integrator

Measured from the GLB accessor counts across all 104 manifest entries, no browser needed:

| reserve | used | headroom |
|---|---|---|
| `BODY_VERTS` 1,600,000 | **1,468,496 (91.8%)** | 131,504 |
| `GLOW_VERTS` 250,000 | 78,614 (31.4%) | 171,386 |
| `BODY_INDICES` 3,600,000 | 2,457,606 (68.3%) | — |
| `GLOW_INDICES` 750,000 | 127,326 (17.0%) | — |

This asset contributes 33,732 body and 2,253 glow vertices — 2.3% of the body reserve. It
fits. But the body reserve is at 91.8% with roughly four more landmarks of this size left
in it, and an overflow is not a crash: `addGeometry` throws, that landmark drops to its
procedural stand-in, and the symptom is **one arbitrary landmark quietly missing on each
reload**. Raise `BODY_VERTS` in `app/src/assets.js` before the next batch, not after.

### 9.5 Local QA (INTEGRATION-PROMPT Step 5)

Driven by `artifacts/2-folsom/qa_local.mjs` against the BUILT app (`app/dist`) in real
headless Chrome over CDP, not the in-editor Browser pane: parallel landmark sessions hold
the preview slots, and a hidden pane throttles `requestAnimationFrame` to nothing, which
makes a healthy streaming landmark look broken.

| Check | Result | Evidence |
|---|---|---|
| Manifest entry loads | **PASS** | `sf-assets: 2-folsom merged 16 objects / 13 materials -> batched (11244 tris body)` |
| Uniform scale ~ 1.0 | **PASS** | **x1.0000** — the authored crown and `targetHeightM` agree exactly |
| Placed at the projected anchor | **PASS** | loader `4094, -2298` vs the tangent projection's `4094.00, -2297.79` |
| Draw calls < 300 | **PASS** | avg **99**/frame over 30 frames at the landmark |
| Atrium skylight is the night hero | **PASS** | median luminance **68** on the skylight vs **8** on the terrace beside it, same material, same moon |
| No asset warnings | **PASS** | none |
| Exactly one building on the block | **PASS** | `plan.png`, `wide.png`; and §9.2's tile decode — 0 survivors inside r=60 |
| Terrain seating | **PASS** | `low-from-embarcadero.png`, `low-from-spear.png` — no float, no sink; the site is dead-flat made ground (sigma 0.07 m) |
| Orientation | **PASS** | `wide.png` — the Embarcadero elevation faces the water, the Folsom front faces the street |

Screenshots in `artifacts/2-folsom/qa/`.

**Two harness bugs found here, both worth recording because they fail SILENTLY and would
pass a careless asset just as happily as a good one.**

1. **Diorama mode hard-locks the camera pitch to 42 degrees.** `camera.js` line 50 sets
   `DIORAMA.pitch = 42 * DEG` and its `update()` reassigns `state.pitch = DIORAMA.pitch`
   every frame while diorama is on — which, by AGENTS rule 1, is always. So
   `SF.goTo(lon, lat, distance, yaw, pitch)` sets the pitch and the next frame takes it
   straight back. The first version of this QA tried to prove the three-mass step-up from
   a 10-degree view and reported "no building in any column"; the asset was fine and the
   view did not exist. There is no sky-behind-the-tower shot to be had in this app. (The
   proof was a `silhouette.png` byte-identical to `day.png` — the camera had not moved at
   all. It is not kept here, being a duplicate of a shot that is.)
2. **Reading pixels back off `SF.renderer.domElement` returns all zeroes.** The renderer
   runs without `preserveDrawingBuffer`, so by the time a `Runtime.evaluate` runs, the
   presented frame's drawing buffer is gone and `drawImage` copies nothing. The night
   check first reported skylight 0 / terrace 0 — identical to what a completely unlit
   asset would report. `Page.captureScreenshot` samples at composite time and does not
   have the problem, so the harness now measures the PNG it just wrote.

### 9.6 Fallback drill (INTEGRATION-PROMPT Step 6, mandatory)

Run as `node artifacts/2-folsom/qa_local.mjs --drill`, which serves a real **404** for the
landmark GLB rather than renaming the file — Vite answers a missing public path with
`index.html` and HTTP 200, so the usual rename trick cannot produce a fetch failure at all.

| Check | Result |
|---|---|
| App still boots with the GLB missing | **PASS** — 104 entries, 83 live, 1 failed |
| Exactly one fallback warning | **PASS** |
| `2Folsom` absent from `placed` | **PASS** |
| Draw calls < 300 | **PASS** — avg 99/frame |
| Site degrades to empty ground inside the exclusion zone | **PASS** — `qa/drill-day.png` |

The warning is:

```
sf-assets: 2-folsom failed to load (fetch for ".../sf-assets/landmarks/2-folsom.glb" responded with 404: Not Found)
```

**Not** the `... — keeping the code-built landmark` text INTEGRATION-PROMPT Step 6 quotes.
That wording belongs to the RESIDENT path (`assets.js` `warn()`); a STREAMED entry — which
this is, it has a `loadRadius` — fails through `scan()` instead, which does not use the
single-shot `warn()`. It is still exactly once: `place()` sets `status = 'failed'` and no
branch in `scan()` matches `'failed'`, so it can never be retried or re-warned. Match on
the id, not on the prompt's wording.

Empty ground is the CORRECT Case B outcome and not a defect: there is no procedural
builder for `2Folsom` in `app/src/landmarks.js` to reappear, and the exclusion has cleared
the baked footprint by design. `drill-day.png` shows bare terrain with the streets,
sidewalks and neighbours intact — no hole, no crash, city renders normally.

### 9.7 Batch mode — what this branch carries

Per `ADDRESS-TO-ASSET.md` "Batch mode": the re-bake was run and fully QA'd, then discarded.
Other landmark sessions were confirmed in flight on this machine during the run, so the
assumption is not hypothetical.

```
git checkout -- app/public/tiles api/_data
```

Source committed: the GLB, the manifest entry, the registry entry, the asset plan, the
`artifacts/2-folsom/` tree and this QA harness. All three shared files are append-only
lists that merge mechanically. The city is rebuilt once for the whole batch by
`docs/asset-pipeline/BATCH-INTEGRATE.md`.

Sanity check required by the pipeline doc — `git diff --name-only origin/main` must list
nothing under `app/public/tiles/` or `api/_data/`: **0 files**, confirmed after the
discard.

One unrelated path does show in that diff, `api/_lib/feeds/residents.mjs`, and it is not a
leak: `origin/main` advanced during this session (PR #159, "Strip the weak-etag marker,
merge on write conflicts, never rewind the window"), so this branch is one commit behind on
a file it never touched. It will merge cleanly. No rebase was done — a batch branch should
touch as little as possible.

