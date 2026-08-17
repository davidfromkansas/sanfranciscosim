# 156 South Park Street — build report

Miniature GLB for SF-SIM, built from `docs/asset-plans/156-south-park.md` and the dossier
in `REFERENCE.md`. Where the plan and this report disagree, **this report wins**.

| | |
|---|---|
| Asset | `artifacts/156-south-park/156-south-park.glb` |
| Manifest id | `156-south-park` |
| Anchor (WGS84) | `-122.3948748, 37.7813535` — DataSF footprint **area centroid** |
| Front heading | **117.3°** true (ESE), onto South Park Street |
| Target height | **8.70 m** to the front parapet crest (normalised exactly) |
| Triangles | **4,020** of a 6,000 cap |
| Objects | **8** after stage 4 (77 as authored) |
| Dimensions | 29.94 × 23.72 × 8.70 m (axis-aligned; the building is a 32.3 m strip at ~45° to the world axes) |
| Min Z | 0.000 m |
| Materials | `Toy_slate`, `Toy_roofd`, `Toy_trim`, `Toy_ink`, `Toy_glass`, `Toy_warm_Glow`, `Toy_glass_Glow` |
| File | **120,132 B** shipped (meshopt); 248,120 B as authored — see `optimize/REPORT.md` |
| Draw submeshes | **9** shipped (79 as authored) |
| Validation | `validation.json` — **overall PASS**, 16 of 16 checks, re-run on the *shipped* packed file |

Build: `blender -b --python build_156_south_park.py`
Renders: `blender -b --python render_156_south_park.py [-- --night]`
Validate: `blender -b --python validate_156_south_park.py`
Contact sheet: `python3 make_contact_sheet.py` (system Python — Blender's bundled
interpreter has no PIL)

---

## 1. What was built

A two-mass building on the measured footprint: a **two-storey street bar** on South Park
(parapet crest 8.70 m) in front of a **single-storey top-lit shed** (roof deck 5.45 m,
parapet 5.70 m) running 26 m back to Taber Place.

The street elevation carries the whole design: two stacked fields of industrial steel sash
(6 × 5 panes below, 8 × 4 above) modelled as relieved mullion bars over one flat glass
plane; a recessed entrance bay with a pale flat canopy, the `156` numerals and two stacked
black sconces; and two X-shaped star tie anchors high on the parapet. Everything is the
same slate blue-grey — no base course, no cornice, no contrasting shopfront — because the
2009 survey found this the **only unaltered contributor of the district's twenty-three**
and its plainness is the thing worth modelling.

The shed roof carries a run of **seven skylight monitors** with their glazing turned
north-north-east, on a regular spacing along the lot's drifting centreline, plus one small
plant box. That roof is what the app's downward camera actually sees.

## 2. Corrections to the plan made during the build

**All three are corrections to `docs/asset-plans/156-south-park.md`, which was written by
the same session an hour earlier. They are recorded here because REPORT beats plan.**

1. **The footprint is not a wedge widening to 19 m.** The plan's first draft read the lot
   as widening from 5.9 m at the street to ~19 m at Taber Place. That is wrong: 19.0 m is
   the *sum* of the 7.94 m Taber Place end wall and the 11.09 m north-east side wall,
   which meet at a corner. Measuring perpendicular width along the lot axis gives **5.92 m
   at the street, rising to 9.8 m about two thirds back, then a 7.94 m end wall cut ~19°
   off square**. The plan was corrected before this build; the model is built on the
   corrected reading.

2. **Two sub-metre parcel slivers were dropped** from the survey ring — 0.15 m at the
   north-east street corner, 1.05 m at the Taber Place corner. Both sit between party
   walls, are invisible in the city, and cost triangles the window grids need.

3. **The bar/shed split was set at 10 m of depth, not the 6 m the LiDAR mean-inversion
   suggests.** See §4 — this is the model's biggest deliberate judgement call.

## 3. Palette extension (WARN)

`Toy_slate` (`#77828e`) is a **deliberate palette extension**, documented here the same way
380 Brannan's `Toy_slate` and 155 South Park's `Toy_peach` were. Nothing in the existing
palette reads as painted grey concrete. `Toy_warm_Glow` (`#cbbb96`) is likewise new.

The real building is *darker* than `#77828e`. It was lightened deliberately: at the first
iteration the wall, the glass and the roof all sat within a few percent of each other and
the model rendered as a solid dark object with no facade at all. The value split between
wall, roof and glazing is what makes it read as a building at diorama scale; the hue is
faithful, the value is not, and that is a style-bible trade (semantic exaggeration in
authoring, never in placement).

## 4. Open risks carried forward

1. **The bar/shed split depth is derived, not observed.** Solving the LiDAR statistics
   (`A_front × 8.74 + (260.3 − A_front) × 5.66 = 260.3 × 6.14`) puts only ~41 m2 at the
   taller level — a bar ~6 m deep. The median independently caps it at under half the
   footprint, ~15 m. The model splits at **10 m**, between the two, because a 6 m bar is
   implausibly thin behind a 3 m-tall ground-floor window and the aerial imagery shows the
   roof tone changing about a third of the way back. **Re-verify from a better oblique
   aerial before this asset is treated as final.** The 8.70 m target height does not
   depend on this.
2. **The Taber Place elevation is unverified** — see REFERENCE.md §4. The alley end has one
   vehicle door recess and nothing else, deliberately.
3. **The pane counts (6 × 5 and 8 × 4) are read off one oblique pano** and may be out by a
   column or a row. They matter, because the grid is the facade.
4. **The star anchors' cause is not asserted.** They are modelled as observed; the DPR form
   calls this reinforced concrete, which does not normally need tie-rod washers, while a
   1990 "parapet reinforcing" permit would explain them exactly.

## 5. Iteration log

| # | Change | Why |
|---|---|---|
| 1 | First build, 4,240 tris | Mass, step and monitor run read correctly from the aerial; the facade did not read at all |
| 2 | Lightened `Toy_slate`, darkened `Toy_glass`, deepened mullion relief, monitors changed from roof colour to wall colour | Everything was within a few percent of the same value; the monitors vanished into the dark deck |
| 3 | Rewrote the opening helper | **Bug:** the "reveal" was a solid wall-coloured slab standing proud of each window, hiding the glass entirely, and the door and vehicle door were modelled *inside* the wall where nothing can see them. There are no booleans here, so an opening has to be a fill just proud of the wall inside a ring of proud jambs — the way 155 South Park's `rect_opening` does it |
| 4 | Clamped side jambs to z ≥ 0 | Openings starting at the pavement carried their jambs below it; min Z went to −0.20 and would have failed the contract |
| 5 | Glow shells cut to the lower 46% of each field, warm off-white instead of gold, planes de-coplanarised | The day pass left the whole window tinted milk-chocolate. Diagnosed by re-rendering the same GLB with the `_glow` objects deleted: a **closed** shell is two alpha layers, so 0.12 alpha reads as ~23%, not 12%. A lower-band shell also happens to be what a lit studio looks like |
| 6 | Canopy lowered to just above the door head; numerals moved above it | The canopy was floating a metre clear of the door and read as a diving board |
| 7 | Roof plant box moved from (0.9, 8.6) to (4.55, 6.05) | It was overlapping the first skylight monitor — visible in the top render |

Final: **4,020 triangles**, validation PASS.

## 6. Validation summary

All 16 checks in `validation.json` pass, on a **fresh-scene re-import of the exported
GLB**, not the authoring scene:

meters and plausible dimensions · crest normalised to 8.70 m · base at z = 0 ·
centred in XY · under the triangle budget · no image textures · no transparency ·
materials follow the contract · no cameras or lights · no animation, skin or constraints ·
transforms applied · no negative scales · normals outward by per-object signed volume ·
normals outward by ray cast (**0.000000 flipped fraction**, 0 of 31,500 rays) ·
no degenerate geometry · no unexpected objects.

**On the XY centre offset (1.05, 1.27 m).** The origin is the footprint **area centroid** —
the point the manifest anchor names and where the loader must put the building. On a lot
that tapers from 5.9 m at the street to 9.8 m two thirds back, that centroid sits ~1.6 m
from the axis-aligned bounding-box centre. The validator's tolerance is set to 1.7 m for
this asset with that reason recorded in `validation.json` (`centering_note`); it is a
property of the plan shape, not a placement error.

## 7. Draft manifest entry

```json
{
  "id": "156-south-park",
  "file": "156-south-park.glb",
  "anchor": [-122.3948748, 37.7813535],
  "targetHeightM": 8.7,
  "cat": 3,
  "name": "156 South Park",
  "estimated": false,
  "dims": [29.94, 23.72, 8.7],
  "tris": 4020,
  "loadRadius": 2500
}
```

`dims` and `tris` are the **shipped** figures: stage 4 changed neither (it removed node
overhead, not geometry).
`cat: 3` is Office (`CATEGORY_LABELS` in `app/src/context.js`) — the building's use since
the 2019 change of use.

## 8. Stage 4 — optimize

Run per `docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md`; full detail in
`optimize/REPORT.md`. Headline: **248,120 → 120,132 raw bytes (−51.6%)**, **79 → 9 draw
submeshes**, triangles and bbox unchanged, all applicable gates G1–G6 and G8 PASS, worst
A/B pixel delta 0.027% against a 2%/4% gate. The limited-dissolve step was deliberately
skipped because this asset has three coplanar parapet ring bands — the 350-brannan sliver
trap. The packed file was then re-run through the stage-2 contract validator: PASS, 16 of
16.

## 9. Stage 5 — integration values (measured, not from the plan)

Two numbers in the plan's §2.13 were wrong on paper and were corrected against the code
and the bake input during integration:

- **`exclude: 3`, window [2.6, 3.4).** The plan reasoned from OSM neighbour vertices. The
  bake reads DataSF *and* Overture, and in Overture this footprint's centroid is 2.48 m
  from the anchor while the party-wall vertex shared with 150 South Park is only 3.40 m.
  Below 2.6 the Overture block survives *inside* the model; at 3.4 the shared vertex takes
  150 South Park out. A drop simulation over both sources confirms r = 3 removes exactly
  one footprint per source.
- **`camera: { distance: 180, yaw: 63, pitch: 26 }`.** The plan suggested yaw 297 from
  `bearing − 180`. That is the wrong sign: `apply()` in `app/src/camera.js` offsets by
  `(sin yaw, ·, cos yaw)` with +z south, so **app yaw = 180 − true bearing** = 62.7 for a
  front at 117.3°. Yaw 297 would have parked the camera behind the building on Taber Place.

## 10. Approval

Standing approval given by the user at the start of the session, quoted verbatim,
16 August 2026:

> APPROVE EVERYTHING DONT ASK ME FOR PERMISSION

This is a **blanket pre-authorisation to run the pipeline without stopping**, not a review
of these particular renders — the user has not seen them. It satisfies the pipeline's
gate-3 requirement to proceed, and the renders are presented alongside this report. The
open risks in §4 stand regardless, and the bar/shed split in particular is a judgement
this asset should not be considered final on until someone looks at a better aerial.
