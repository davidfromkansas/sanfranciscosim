# 92 South Park — build report

Asset: `92-south-park.glb` — the 1996 six-unit live/work condominium at **86–96 South
Park Street** (block 3775, lots 116–121), by Toby S. Levy, FAIA. "92 South Park" is one
of its six unit addresses; see `REFERENCE.md` §1.

**Status: stage 2 gate PASS, stage 4 gate PASS.** `validation.json` is all-PASS on a
fresh-scene re-import of the **shipped** GLB — i.e. the optimized file, re-validated
after the stage-4 shipping swap. The optimize pass is reported separately in
[`optimize/REPORT.md`](./optimize/REPORT.md); the pre-optimize original is archived at
`optimize/input/92-south-park.glb`.

| | |
|---|---|
| Triangles | **7,736** (cap 12,000) |
| Objects | 17 shipped (195 as authored; joined per material at stage 4) |
| File size | **250,640 bytes** raw shipped (535,408 pre-optimize, −53.2%) |
| Draw submeshes | 19 shipped (201 pre-optimize) |
| Dimensions | 31.861 × 32.051 × **13.28** m |
| min Z | 0.0000 |
| XY centre offset | 0.0000, 0.0000 |
| Materials | 15, all `Toy_*`, two `_Glow` |
| Anchor | **`-122.3941549, 37.7819082`** |
| Front heading | 135.1° true (south-east) |
| Loader scale | `targetHeightM / measuredHeight` = 13.28 / 13.28 = **1.000** |

Build: `blender -b --python build_92_south_park.py --` (Blender 5.2.0 LTS).
Renders: `render_92_south_park.py` (EEVEE, 128 samples), `--night` for the dusk pass,
then `python3 make_contact_sheet.py` (the contact-sheet script needs Pillow and runs on
the system Python, not Blender's).
Validation: `blender -b --python validate_92_south_park.py --`.

---

## 1. Corrections this build made to the plan

`docs/asset-plans/92-south-park.md` was re-verified before modelling. Seven things
changed; this list is the authoritative log.

1. **The anchor moved 1.06 m.** The plan's anchor (`-122.3941630, 37.7819166`) is the
   union OBB centre of the two DataSF footprints. The shipped GLB's XY bounding-box
   centre is `-122.3941549, 37.7819082`, because the built form is the lot rectangle plus
   the tower's 0.40 m projection and the plinth's 0.12 m margin, not the LiDAR polygons.
   **The manifest and registry entries must use the measured anchor.** Consequence for
   stage 5: the exclusion distances in the plan's 2.13 were measured at the *plan* anchor
   and have to be re-measured at this one before a radius is committed.
2. **The raked parapet was first built as a solid prism** (`st_prism`), and the whole
   14 × 16 m front block read from the app's camera as a sloping roof rather than a flat
   deck behind a diagonal parapet. Rebuilt as `st_raked_ring`, a band, so the deck stays
   visible. This is the single largest correction in the build.
3. **The front block started at the tower's edge**, leaving a 3.9 × 12 m strip of bare
   plinth roof beside the tower on the Jack London Alley side. Fixed: mass A now runs
   `s = 0 … 9.40` and the tower is a projecting element *within* it.
4. **The court paving changed from `Toy_roofd` to a new `Toy_greige`.** In the roof
   colour the court was not a court — from directly overhead it read as one more dark
   plane. The court floor is now the lightest large surface on the asset, which is both
   more legible and closer to the warm slate chequer in the 1996 photograph.
5. **The corner tower was enlarged** from 3.90 to 4.30 m square, and its projection from
   0.30 to 0.40 m, after the first aerial review: at 3.9 m it read as a bump on the
   parapet rather than as the tower that carries the crest.
6. **An oversailing copper cube was added** on the front block's fourth floor (1996
   photograph `8912EXT`). Without it the front block's deck was a bare plate — the plan
   listed the cubic forms but put none of them on the roof, where the camera looks.
7. **Three parapet rings became two.** The plan implied a separate band over the raked
   section; in the render its inner wall drew a second line across a single roof plane.
   The rake now runs the full length of mass A, from 12.60 m at the tower down to
   11.45 m at the step.

Nothing in the plan's dossier turned out to be factually wrong. The corrections are all
modelling decisions the plan could not have anticipated without a render.

## 2. Heights: what is measured and what is not

Measured (DataSF `ynuv-fyni`, 2010 LiDAR):

- front block roof deck **11.15 m** (median, 837 cells)
- rear bar roof deck **12.32 m** (median, 324 cells)
- **crest 13.28 m** (front block maximum) — the target height; see `REFERENCE.md` §6 for
  why this and not the rear bar's 13.73 m

Inferred (1996 frontage photographs scaled against the LiDAR deck): the plinth top at
3.55 m and the two intermediate floor lines at 6.15 and 8.75 m. Four levels in 11.15 m
gives 3.55 / 2.60 / 2.60 / 2.40 — a tall commercial ground floor under three ordinary
residential ones, which is what the photographs show and what a live/work condominium
over two shops is.

## 3. Orientation

The asset is authored in true-world orientation (Blender +Y = north, +X = east), as
`docs/asset-plans/README.md` requires, so the South Park front faces **135.1° true
(south-east)** rather than the contract's nominal −Y. Real-world orientation wins
(AGENTS rule 5). Consequence: a 14.45 × 30.04 m lot standing at 45° has a near-square
world-axis AABB of **31.86 × 32.05 m**, which is expected and not a scale error.

## 4. WARN — two palette extensions

| Name | Hex | Why |
|---|---|---|
| `Toy_bluestone` | `2f3a44` | The ground-floor glazed tile is blue-black. `Toy_ink` (`3a3530`) is warm near-black and folds the plinth into the window frames; `Toy_navy` (`2c4a70`) is within 3% of `Toy_glass` (`2a4d73`) and the shopfronts disappear into the wall around them. `2f3a44` is darker than the glazing and bluer than the ink |
| `Toy_greige` | `b0aa9e` | The court paving — see correction 4. The name already exists elsewhere in the shipped set at this value; this is the first landmark to use it |

Both are recorded here rather than silently added, following the precedent of
`Toy_olive` (140 South Park) and `Toy_peach` (155 South Park). If a reviewer would rather
not extend the palette, `Toy_ink` and `Toy_stone` are the fallbacks, and the plinth loses
its blue and the court its separation.

## 5. Night state

Two warm shopfronts and a warm entry strip in the plinth, five cool upper windows
scattered across three floors and three bays, and two warm patches at the foot of the
external stair inside the court. Every glow surface is a thin shell proud of the opaque
glazing it sits over — none is a closed box, so nothing reads as a double alpha layer by
day. The court glow is not visible from the review aerial's azimuth, which is correct:
it is meant to be seen only when the camera is over the building.

## 6. Iteration log

| Pass | Change | Verdict |
|---|---|---|
| 1 | First build, 7,692 tris | Raked parapet read as a sloping roof; a strip of bare plinth beside the tower; the court read as another roof plane |
| 2 | `st_raked_ring`, mass A extended to s = 0 | Deck visible, plinth strip gone. Tower still weak; deck still a bare plate |
| 3 | Tower 4.30 m / 0.40 m proud; oversailing copper cube added | Tower reads; deck has a subject. Court still dark from above |
| 4 | Court paving → `Toy_greige`; redundant parapet ring merged | 7,720 tris, all-PASS |
| 5 | **Every plinth-level opening re-based from the plinth face** (`base_d = PLINTH_PROJ`). The stage-4 A/B render caught the two garage doors as solid z-fight speckle *in the input*; the same defect had the shopfront and entry frames buried inside the plinth on all three street elevations | **Accepted.** 7,736 tris, all-PASS; elevation pixel deltas fell from 0.18%/0.32% to 0.0005%/0.0001%. See `optimize/REPORT.md` |

## 7. Known gaps carried forward

- The **rear (north-west) elevation** is unobserved by any source and is authored as a
  blunt service face.
- The **material positions** come from 1996–97 photographs; only the weathered appearance
  comes from 2025. A re-clad since would not show in the permit record consulted.
- A pale object over part of the court in 2026 aerial imagery is unexplained by any
  source and is deliberately not modelled.
- **A sibling branch, `pipeline/96-south-park`, resolves to this same parcel.** Both
  branches produce a GLB, a manifest entry and an exclusion zone for one building; only
  one can be merged. Flagged again here so it is not lost between the plan's 2.15 and the
  batch integrator.

## 8. Stage 3 — approval

Pre-authorised by David at the top of the session, quoted verbatim:

> APPROVE EVERYTHING DONT ASK ME FOR PERMISSION

Recorded 2026-08-16. The pipeline's stage-3 human gate is therefore satisfied by a
standing instruction rather than by a per-asset review; the contact sheet, the day and
night aerials and the numbers above are presented in the session's final report so the
approval can be withdrawn retrospectively if the asset does not hold up.
