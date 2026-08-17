# 126 South Park — build report

Miniature GLB for the SF-SIM toy-diorama city. Built from
`docs/asset-plans/126-south-park.md`, re-verified against the sources in `REFERENCE.md`.
**Where this report and the plan disagree, this report is authoritative.**

| | |
|---|---|
| Asset | `126-south-park.glb` |
| Manifest id | `126-south-park` |
| Anchor (WGS84) | -122.3945863, 37.7816006 |
| Target height | **7.60 m** (front eave crest) |
| Front heading | **135.3° true (SE)** |
| Blender | 5.2.0 LTS |
| Validation | **PASS** (all 18 checks, re-run against the shipped meshopt file) |

## Shipped numbers

| Metric | Value | Budget / expected |
|---|---|---|
| Triangles | **4,560** | ≤ 7,000 |
| Objects (shipped, post-optimize) | **9** | joined per material at stage 4 |
| Objects (as built, pre-optimize) | 82 | — |
| Dimensions (m) | **26.738 × 26.587 × 7.600** | ~26.7 × 26.6 at a 45° heading |
| bbox min / max | (-12.979, -13.776, 0.000) / (13.759, 12.810, 7.600) | — |
| min Z | **0.0000** | ≤ 0.5 |
| XY centre offset | (0.390, -0.483) | ≤ 1.0 |
| **Waist (ray-cast section)** | **4.007 m** | 4.01 m surveyed |
| Light-well notches | 2 south-west + 1 north-east | 2 + 1 |
| Materials | 9, all `Toy_*` | no `Toy_body` |
| Glow materials | `Toy_glass_Glow`, `Toy_glassl_Glow` | — |
| Image textures / cameras / lights | 0 / 0 / 0 | 0 |
| Animations / armatures / constraints | 0 / 0 / 0 | 0 |
| Degenerate triangles | 0 | 0 |
| Signed-volume outward objects | 9 / 9 | all |
| Normal ray test | 0 flipped of 31,500 first hits (0.000%) | ≤ 0.15% |
| File size (as built) | 286 KB raw | — |
| **File size (shipped, meshopt)** | **124 KB raw**, 85 KB gzip | ≤ 500 KB compressed |
| Draw submeshes (shipped) | **10** (from 83) | ≤ input |

Scale check: the bounding-box top lands on **7.600 m exactly**, so the loader's
`targetHeightM / measuredHeight` is 1.0.

## Deliverables

```
artifacts/126-south-park/
  build_126_south_park.py      deterministic build (Blender 5.2, headless)
  render_126_south_park.py     controlled review renders from the EXPORTED GLB
  validate_126_south_park.py   fresh-scene contract validation
  make_contact_sheet.py        composes the contact sheet
  126-south-park.blend         authoring scene
  126-south-park.glb           THE ASSET
  126-south-park-{north,east,south,west,top}.png
  126-south-park-aerial.png    high three-quarter aerial (day)
  126-south-park-aerial-night.png
  126-south-park-contact-sheet.png
  validation.json
  REFERENCE.md                 research dossier
  REPORT.md                    this file
```

Rebuild: `blender -b --factory-startup --python build_126_south_park.py`

## Dossier corrections made during this build

Five research-level corrections, all carried into `REFERENCE.md`:

1. **The parcel is block 3775 lot 061.** The plan asserted it; this pass proved it, by
   matching the SF permit records for "126 South Park" to lot 061 and confirming that
   DataSF footprint `SF3775061` sits 0.58 m from the OSM ring at the nearest vertex.

2. **LoopNet's "3 Stories / 5,442 SF" is rejected.** Against it: 19 consecutive assessor
   rolls (2007–2025) recording `number_of_stories = 2.0`, both building permits on the lot
   recording 2 existing storeys, and a photograph showing two storeys under one eave.
   Built as **2 storeys**.

3. **Two architecture-press pages are falsely attached to this address by search.** The
   Perkins&Will and Office Snapshots "South Park Venture Capital Firm" pages are returned
   for queries naming 126 South Park and were summarised as being at it. Both were fetched
   directly and **neither contains this address, or any address**; they describe a
   16,420 sq ft brick-clad 1920s building. Ignored, and recorded so the next agent does
   not re-inherit them.

4. **SF Planning case 2010.0959CV is 147 South Park**, block 3775 lot 031 — its own header
   says so. Not this building, and its demolition proposal does not apply here.

5. **The LiDAR maximum of 10.16 m is edge contamination, not a feature.** Mean 7.34 m,
   σ 0.64 m, mode and median both 7.32 m over 715 cells puts 10.16 m at 4.4σ (and the
   3.74 m minimum at −5.6σ). A 6.9 m wide building with taller neighbours 0.6 m away on
   *both* flanks has almost no cells that are not edge cells. **The roof is flat at
   7.32 m** and the model is built to it.

## Design revisions during this build

Reviewed from the high three-quarter aerial first, as the pipeline requires, and iterated
before running the formal rig.

**Revision 1 — roof furniture cut to fit the crest, and then cut further.** The plan's
first draft specified 0.7 m and 0.5 m HVAC blocks. On a 7.32 m deck under a 7.60 m crest
those would have stood at 8.02 m, above the bounding-box top. Rather than raise the target
height, the plant was removed: nothing in the evidence supports rooftop mechanical, and
the roof composition is carried by the light wells. The plan (§2.7 step 10, §2.9) was
amended to match before the build ran, so plan and asset agree.

**Revision 2 — the roof value hierarchy was inverted, and it was inverted the wrong way.**
The first aerial render had a dark `Toy_roofd` deck with pale `Toy_stone` light-well
linings, following 135 South Park. It read badly: **the wells looked like raised bright
blocks rather than holes**, which inverts the one cue this asset exists to carry. From
above, a void reads as a dark slot.

Both were changed, and the change turned out to be better evidenced as well as better
looking. The deck is now pale `Toy_stone` and the well linings dark `Toy_roofd`, because
the 2023-08-28 re-roofing permit covers the whole ~2,100 sq ft roof and therefore clears
Title 24 Part 6 §141.0(b)2Bi's "more than 50 percent or 2,000 square feet, whichever is
less" trigger — which requires an aged solar reflectance of 0.63 on a low-slope
nonresidential re-roof in every California climate zone. That is a pale roof. 135 South
Park is dark because an aerial was actually read for it; here the aerial is unusable
(Esri is washed out at z20 and z21 is not served) and the building code is the better
source.

Three smaller fixes in the same pass:

- The **eave top face** moved from `Toy_roofd` to the siding gray. The photograph shows
  the hood painted with the rest of the front, and a dark slab there fought the pale deck.
- The **entrance gate** was rendering as a blank white slab: its trim frame had been
  extruded further than the gate panel behind it, so the frame simply covered it. Relayered
  frame → reveal → panel, outermost last, matching `rect_opening`.
- The **skylight glow shells** were a pair of thin bars flanking each skylight, which lit
  the flanks and read at night as two white dashes. Replaced with one flat shell just proud
  of the glazing cap.

**Revision 3 — the vent cowl** moved forward to d ≈ 6.5 m so the front half of a 30 m deck
is not empty, and darkened to `Toy_ink`.

## Two build-script notes worth keeping

**The crest needs an explicit normalization pass.** This building's highest point is an
*edge* — the crease where the sloping eave meets the wall — not a face. The 0.12 m bevel
that gives every other solid its miniature softness rounds that crease off by ~42 mm, so
authoring the eave at 7.60 m exported a 7.558 m asset. Flat-topped landmarks do not hit
this, because a bevel leaves the interior of a flat top face untouched. `normalize()`
therefore lands min Z on 0 and scales Z about the base so the crest is exactly 7.60. The
correction is a **Z-only** scale of ×1.00396, so the measured footprint is left bit-exact
and only vertical dimensions move — 3 cm on the building's height, under 2 cm on any
storey.

**The validator measures the waist by ray-cast section, not by binning vertices.** Two
earlier attempts failed and both failures are instructive. The first binned vertices along
the wrong axis: at +45° it is `x·cos − y·sin` that carries the 29.79 m depth and
`x·sin + y·cos` the 6.99 m width, and swapping them bins the building across its 7 m face.
The second got the axis right and still failed, because **the structural shell is a
16-corner prism with no vertices along its long walls at all** — a vertex histogram
samples almost none of its length and reports whatever two corners happen to share a bin.
The shipped check fires rays inward from both flanks at z = 1.0 m every 0.25 m and measures
the wall faces directly, which is why it can report 4.007 m against a surveyed 4.01 m.

It also counts notches **per flank**: the north-east well and the first south-west well
overlap for 1.99 m, so counting notched slices without regard to side merges them and
reports two wells instead of three.

This matters beyond bookkeeping. The asset's 45° heading makes its axis-aligned bounding
box near-square (26.74 × 26.59 m), so **the bounding box cannot tell this model from one
rotated 90°.** The waist measurement is what actually pins the plan shape and the
orientation, and it is the check to trust if this asset is ever revised.

## Palette

| Material | Hex | Used for |
|---|---|---|
| `Toy_steel` | `9aa0a6` | all walls, siding bands, roof upstand, eave top |
| `Toy_stone` | `d9d2c2` | **roof deck** (the Title 24 cool roof) |
| `Toy_roofd` | `45454a` | **light-well linings**, gate panel, roof hatch, rear door |
| `Toy_trim` | `f3efe6` | window surrounds, sills, belt course, frieze, eave fascia, skylight kerbs |
| `Toy_glass` | `2a4d73` | all windows — front, rear, and in the wells |
| `Toy_glassl` | `6f95b8` | the two roof skylights |
| `Toy_ink` | `3a3530` | eave soffit and rafter blocks, reveals, vent cowl |
| `Toy_glass_Glow` | `6f95b8` | light-well heads and two front windows, lit |
| `Toy_glassl_Glow` | `6f95b8` | the lit skylights |

The siding is `Toy_steel` rather than `Toy_verdigris`, which is closer in hue to the
measured `#8e9791` of the real paint. A whole building rendered in a saturated hue becomes
an accent rather than a neutral, and the style bible §7 reserves saturation for identity —
here the identity is the plan shape, not the colour. Same reasoning 380 Brannan and 135
South Park used for their brick → rust swap.

**Night state.** Hero glow is the **waist**: thin shells at the head of each light well,
so from the app's aerial camera the building reads as a long dark plank with a bright notch
burning across its middle — the night statement of the cue that carries the day. Supported
by the two lit skylights and two lit front windows. Nothing else glows. All glow surfaces
are thin shells proud of the opaque geometry, never primary surfaces.

## Validation checklist

| Check | Result |
|---|---|
| Fresh-scene re-import of the exported GLB | PASS |
| Meters and plausible dimensions | PASS |
| **Waist pinches to 4.0 m ± 0.15** | **PASS (4.007 m)** |
| **Three light wells (2 SW + 1 NE)** | **PASS** |
| Crest normalized to target (7.6 m ± 0.02) | PASS |
| Base at z = 0 | PASS |
| Centered in XY | PASS |
| Under triangle budget (4,560 / 7,000) | PASS |
| No image textures | PASS |
| No transparency | PASS |
| Materials follow contract | PASS |
| No cameras or lights | PASS |
| No animation, skinning or constraints | PASS |
| Transforms applied | PASS |
| No negative scales | PASS |
| Normals outward — per-object signed volume | PASS (82/82) |
| Normals outward — ray residual | PASS (0.000%) |
| No degenerate geometry | PASS |
| No unexpected objects | PASS |
| **Overall** | **PASS** |

## Draft manifest entry

```json
{
  "id": "126-south-park",
  "file": "126-south-park.glb",
  "anchor": [
    -122.3945863,
    37.7816006
  ],
  "targetHeightM": 7.6,
  "cat": 3,
  "name": "126 South Park",
  "estimated": false,
  "dims": [
    26.7382,
    26.5868,
    7.6
  ],
  "tris": 4560,
  "loadRadius": 2500
}
```

## Integration notes

Case B — new landmark. Needs a `pipeline/lib/landmarks.mjs` entry and a tile re-bake.
`exclude: 3.5` (window 2.19 < r < 4.67 m; see the plan's §2.13), `camera: { distance: 130,
yaw: 45, pitch: 26 }`. Batch mode applies — seven other South Park addresses are in
flight, so the bake is run and QA'd but discarded before committing.

## Stage 4 — optimize (shipped numbers)

The shipping file is the stage-4 output: **292,460 → 126,664 bytes (−56.7%)**,
**83 → 10 draw submeshes**, 82 → 9 objects, triangles unchanged at 4,560,
appearance identical (max mean pixel delta 0.0751%). All gates G1–G6 and G8 pass;
G7 is N/A (no bake). Full detail, including why limited dissolve was skipped for
this asset's coplanar ring band, is in `optimize/REPORT.md`. The pre-optimize
original is archived at `optimize/input/126-south-park.glb`.

The numbers in the tables above are the **shipped** ones — `validation.json` was
re-run against the packed file and passes every check, with the waist still
measuring 4.007 m and the light wells still counting 2 south-west + 1 north-east.

## Stage 5 — integration (local QA, batch mode)

Case B. Registry entry `126SouthPark` added to `pipeline/lib/landmarks.mjs`
(`exclude: 3.5`, `camera: { distance: 130, yaw: 45, pitch: 26 }`), manifest entry
appended, GLB copied to `app/public/sf-assets/landmarks/`. `camelId()` maps
`126-south-park` -> `126SouthPark`, matching the registry id, so the procedural version
is hidden rather than doubled. `node pipeline/compress-assets.mjs` reports
`skip (already compressed)` — the stage-4 output is the shipped asset and was not
re-encoded.

| QA item | Result | Evidence |
|---|---|---|
| Re-validation before touching the app | PASS | fresh-scene re-import, all 18 checks, waist 4.007 m |
| Manifest entry / id mapping | PASS | `126-south-park` -> `126SouthPark`; 59 manifest entries, no duplicate ids |
| Registry entry parses | PASS | `LANDMARKS` imports clean, 65 entries, no duplicate ids |
| **Case B re-bake** | PASS | full chain terrain -> ... -> context -> muni-shapes, exit 0 |
| **Exclusion drops only this building** | PASS | 2 rings dropped, both ours (DataSF `SF3775061` 178.6 m² at 2.19 m; Overture 195.3 m² at 0.01 m); first survivor 112 South Park at 4.67 m |
| **Audit check 1.6** | PASS | "no procedural footprint inside a bespoke landmark exclusion zone — 66 zones over 65 landmarks clear" |
| **verify-rebake** | PASS | 584 of 585 cells unchanged; only 23_13 moved (217 -> 215); nearest surviving footprint 5.0 m vs 3.5 m radius |
| Loader merge line | PASS | `sf-assets: 126-south-park merged 10 objects / 9 materials -> batched (2600 tris body); uniform x1.0000 at 3776, -1282` |
| **Scale factor** | PASS | **x1.0000** — authored height and `targetHeightM` agree exactly |
| Exactly one building on the site | PASS | no procedural twin, no baked block poking through, no z-fighting |
| Orientation | PASS | the 6.90 m front faces South Park; the long axis runs back into the block at 45° |
| Terrain seating | PASS | no float, no sink |
| Night glow | PASS | only the skylights, light-well heads and the two intended front windows light |
| Draw calls | PASS | **92** against the 300 budget; the landmark joins the shared `BatchedMesh` and adds none |
| **Fallback drill** | PASS | GLB renamed -> exactly one warning, `sf-assets: 126-south-park failed to load`; 52 other landmarks still live; app boots, area renders, site is empty ground inside the exclusion zone (expected for Case B); file restored byte-identical |
| Lint / build | PASS | `eslint src` clean; `vite build` OK |
| **Batch-mode source-only branch** | PASS | `git diff --name-only origin/main` lists nothing under `app/public/tiles/` or `api/_data/` |

**Two notes on the local QA rig**, both environmental rather than asset defects:

- The Browser pane runs hidden, which throttles `requestAnimationFrame` to a stop, so
  the streaming pump and the LOD cross-fade had to be driven by hand
  (`SF.assets.update(SF.camera.position, dt)` — note it takes a *position*, not the
  camera; passing the camera makes every distance `NaN` and silently releases every
  landmark). One frame renders per screenshot, so the hashed-alpha tile cross-fade never
  finishes settling and the QA screenshots carry a dither haze that the real app does
  not.
- Under Vite the missing GLB returns `index.html` with a 200 rather than a 404, so the
  fallback warning reads `Unexpected token '<'` instead of a clean fetch error. The
  degradation path is the same and it fired exactly once.

**Dossier correction from the re-bake:** the plan predicted "exactly one" procedural
footprint dropped, inheriting 135 South Park's rule. It is **two**, and both are this
building — 126 reaches the bake as two overlapping rings because the Overture gap-fill
did not dedupe it against DataSF. The plan's §2.13 has been corrected to test *which*
rings are dropped (every one within ~2.2 m of the anchor) rather than how many.

## Approval

Presented at pipeline stage 3 on 16 August 2026.

> "APPROVE EVERYTHING DONT ASK ME FOR PERMISSION" — David, 16 August 2026

Blanket pre-approval given with the task, covering gate 0 and gate 3. The contact sheet,
aerial day and night renders and the numbers above were still produced and presented
before advancing, so the decision remains reviewable.
