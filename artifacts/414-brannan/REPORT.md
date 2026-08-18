# 414 Brannan Street (Epic Church) — build report

Stage 2 of `docs/asset-pipeline/ADDRESS-TO-ASSET.md`, executed 18 August 2026 from
Part 1 of `docs/asset-plans/414-brannan.md`. **REPORT beats plan**: where this
document and the plan disagree, this document is what shipped.

## Shipped numbers

| | |
|---|---|
| File | `414-brannan.glb` |
| Triangles | **8,312** (cap 10,000) |
| Objects | 155 (pre-optimize; stage 4 merges these) |
| Dimensions | 33.163 x 33.073 x **14.000** m |
| bbox min / max | `[-16.310, -16.810, 0.000]` / `[16.853, 16.263, 14.000]` |
| XY centre offset | `[0.272, -0.274]` m |
| Raw / gzipped | 512,896 B / 96,845 B (pre-optimize) |
| Materials | 14, all `Toy_*`, flat, opaque |
| Glow materials | `Toy_glass_Glow`, `Toy_trim_Glow` (+ `Toy_gold_Glow` authored but folded into the medallion set) |
| Anchor | `-122.3948685, 37.7799308` |
| Brannan front heading | 135.2° true |
| `validation.json` | **PASS** on all 16 checks |

The 33 x 33 m footprint bbox is correct: a 24.90 x 21.28 m parallelogram sitting
45.2° off the world axes, plus the 0.68 m tile pent on two faces.

## Dossier re-verification

Everything in the plan's §2.1 was re-checked before modelling. All of it held.
Specifically confirmed independently:

- The anchor. The parcel AABB centre, the parcel centroid, the EAS address point
  and the assessor's `the_geom` all land within 0.02 m of each other.
- The three-strips-one-building reading. `mblr = SF3776011` returns three ~180 m2
  LiDAR strips; the parcel carries exactly one address, one assessor record and one
  owner. They are structural bays.
- The 10.39 m street parapet, by photogrammetry (`REFERENCE.md` §5), against the
  northeast bay's 10.32 m LiDAR median — 0.07 m apart from two unrelated
  instruments.
- The 2025 colour scheme (slate body, teal arch), by sampling the current Street
  View frames rather than the 2021 ones the first search returned.

No dossier value had to be corrected. The changes below are all authoring
decisions made against the renders.

## Deviations from the plan, and why

1. **Roof deck at 9.85 m, wall top at 10.20 m** (plan: deck 10.32, parapet above).
   The measured tile ridge at 10.39 m is the number that had to survive, and with
   the deck at 10.32 the pent had only 0.07 m of relief — from the app's downward
   camera it read as a painted stripe, not a roof. Dropping the deck 0.47 m (well
   inside LiDAR noise, and the LiDAR median *includes* the pent) lets the hood
   stand proud without moving the crest.

2. **Tile pent projects 0.68 m, not 0.50 m**, with a rippled top face. This is
   where the plan said to spend the exaggeration budget; the first build at 0.50 m
   with a flat top read as an awning from the aerial.

3. **Frieze underside at 9.05 m, not the measured 9.22 m.** A 0.17 m semantic
   exaggeration so the vermilion band survives at thumbnail size. Measured against
   the reference photograph the red band (tile + frieze together) now occupies
   11.4% of the facade height against the real building's ~12.5% — so the
   *combined* band is if anything slightly conservative.

4. **Roof decks are `Toy_stone`, copings `Toy_steel`** (plan: decks `Toy_steel`).
   `Toy_steel` decks measured almost the same value as the `Toy_slate` walls from
   the aerial, so the whole roof read as one blue-gray sheet and the three levels
   disappeared. The nadir imagery shows a light membrane anyway, so this is both
   more legible and more accurate. `Toy_roofd` is used only on louvre bands and the
   roof hatch — never on a deck (it measures rgb(9,9,12) in the running diorama).

5. **Upper-window frames are `Toy_trim`, not `Toy_ink`.** An ink frame around
   `Toy_glass` fill is two dark values touching; every window read as one flat hole.
   The shipped light frame is also what 400 Brannan uses next door.

6. **Ground-floor bays moved 0.8 m southwest** (to u = 12.2 / 14.8 / 17.4 / 20.0)
   so the northeast-most bay clears the arch's left jamb, whose outer radius reaches
   u = 21.28.

7. **Blank recessed panels are four proud reveal bars**, not a proud pad with an
   inset fill. The plan's construction buries the inset fill inside the pad and
   renders as a featureless slab.

8. **Bevel budget**: the pent, the balconies and the louvre bands get 0.04 m / 1
   segment instead of 0.12 m / 2. At the full budget the four balconies alone cost
   2,850 triangles.

## Build-loop iterations

| # | What the render showed | Fix |
|---|---|---|
| 1 | 11,162 tris, over the 10,000 cap | rib pitch 0.83 → 1.25 m, arch 12 → 9 segments, balcony 8 → 6, light bevels on curved parts. 7,352 tris. |
| 1 | Every glazed panel invisible | The frame prism was proud of its fill, burying it. Depth order inverted: frame 0→0.06, fill 0→0.12, glow shell 0.09→0.16. |
| 1 | Roof was two enormous cream slabs | The copings were solid `roof_box` lids capping the whole raised volume. Rebuilt as `roof_coping()` **rings** so the deck shows inside them. |
| 2 | Roof read as one blue sheet | Deck palette → `Toy_stone`, copings → `Toy_steel`, mech pad → `Toy_steel` with `Toy_trim` units. |
| 2 | Windows read as flat holes | Frames → `Toy_trim`. |
| 3 | Vermilion frieze swallowed by the pent soffit | Wall top 10.05 → 10.20, pent inner soffit raised, frieze underside 9.20 → 9.05. |
| 3 | Northeast bay clashing with the arch jamb | Bay row shifted 0.8 m southwest. |
| 4 | `validation.json` FAIL on `meters_and_plausible_dimensions` | The script was copied from 400 Brannan with its 8.6–9.0 m height window and its anchor/heading constants; retargeted to this asset. All 16 checks PASS. |
| 5 | Both raised roof decks rendered **pure black** in Cycles (fine in EEVEE) | A separate 0.02 m deck slab sat flush on each raised volume, so two coplanar top faces coincided exactly and every camera ray terminated inside the closed box. Dropped the slabs and gave `roof_box()` a `mat_caps` argument, capping each volume directly the way the body prism does. |
| 5 | Night glow clipping to pure white | Preview emission 3.2 → 2.0. |

## Night state

Hero glow: the frosted ground-floor bays on Brannan and the one on Ritch — they are
translucent panels by day and lit boxes at night, and this ground floor is the
lobby and café. Shells cover the middle 1.05–3.00 m of each 4.28 m bay, not the
full height, because a closed `_Glow` shell crosses two faces and reads ~23% opaque
in the day pass; a full-height shell would tint the whole ground floor in daylight.

Supporting accents: two upper windows on Brannan and one on Ritch (glow shells at
62% of the opening height), the **monitor clerestory** — a lit sanctuary that only
the aerial camera can see, which is the payoff for modelling the monitor at all —
and the tympanum medallion.

`fade_glow()` in `render_414_brannan.py` zeroes `Emission Strength` as well as
`Alpha`, so the day renders show what the app shows. Night emission is 2.0.

## Known risks carried into integration

- The **body colour** `#8a97a8` is lifted from the photographic value (`#6a798b` in
  shade) because the diorama has far less ambient light than the render rig. Its
  relative luminance is ~149, against `Toy_roofd`'s ~69 (which measures rgb(9,9,12)
  in-app) and `Toy_steel`'s ~159 (which measures rgb(94,105,111)). **Verify this
  from the running app at stage 5, not from these renders.**
- The **roof monitor's form is inferred.** Its existence and height are measured;
  whether it is a daylight monitor, a stair penthouse or a plain raised block is
  not. If better aerial imagery settles it as a plain box, delete the clerestory
  band and keep the massing.
- The **southwest two thirds of the Brannan upper floor is reconstructed** from one
  oblique frame, because a row of mature ficus hides it in every frontal view.

## Approval

Stage 3 of the pipeline. Recorded below when given.

> _(pending)_
