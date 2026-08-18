# 501 Third Street — build report

## What was built

A stylized miniature GLB of 501 Third Street, San Francisco — a 1920
unreinforced-masonry industrial loft holding the corner of 3rd and Bryant on the
45° SoMa grid. The asset is a three-storey rhombus prism (23.6 × 25.05 m,
592 m2 footprint) with a dark storefront base that wraps the corner, a two-band
steel-sash industrial window grid on both street elevations, punched windows on
the Taber Place alley flank, a blind party wall on the fourth (NE) face, a flat
parapet at 14 m, and a rooftop bulkhead at 16.4 m (the crest). Authored in
true-world orientation: the 3rd Street front faces SW, 225.4° true.

## Dossier corrections (REPORT beats plan)

- **Storey count resolved as 3 above grade.** The plan flagged the assessor's
  "4 storeys" vs OSM's `building:levels=3` vs DBI permits referencing floors
  1–3. Resolved as 3 above-grade floors (ground + 2 upper): with hgt_median
  13.73 m and 3 storeys that is ~4.6 m per storey, typical for a 1920 industrial
  loft with tall floors. With 4 storeys it would be 3.4 m per storey, unusually
  short for the type. The assessor's 4 likely includes a basement or mezzanine.
  No street-level photo was available to confirm the window band count
  independently; the decision is documented in REFERENCE.md §Uncertainties.
- **LiDAR `peak_1st_m` of 22.38 m rejected as neighbour bleed.** 8.6 m above the
  median with sigma 0.92 m — a 9σ outlier on a roof whose own `hgt_max` is
  16.42 m. The 16.42 m bulkhead crest is corroborated by DBI permits (2010
  accessories room, 2011 elevator-shaft-to-mechanical-room conversion).
- **Which faces are party walls: resolved, and it is only one.** The LiDAR
  footprint (568 m2) matches the parcel (567 m2), so the building does fill its
  lot; the plan left open how many faces that blinds and modelled all three
  non-street faces as punched-window rear walls. Measured against the DataSF
  footprints at stage 5: exactly one face abuts anything — the NE, against
  SF3775075 (h 14.90 m, centroid bearing 42° at 21.8 m). The other three are
  exposed, two of them to streets. See the orientation correction above.

## Revision log

**2026-08-18 — orientation corrected 180°, rebuilt as a corner building.**
The single biggest correction in this asset's history, and the plan was the
source of it. Both the plan and the first build put the 3rd Street elevation —
the storefront and the steel-sash window grid, i.e. the whole identity — on the
NE face. The NE face is the mid-block party wall. Measured against the bake's own
street centrelines (`pipeline/data/streets_datasf.geojson`) and the neighbouring
DataSF footprints, and cross-checked by running the same method on shipped
`500-third` as a control (it reproduces that asset's documented 45.2° / 315.3° /
225.1° exactly):

| Face | Was modelled as | Actually is |
|---|---|---|
| SW, normal 225.4° | "service rear" | **3rd Street** (centreline 24.1 m out) |
| NW, normal 315.6° | party wall | **Bryant Street** (centreline 23.5 m out) |
| SE, normal 135.7° | party wall | **Taber Place** alley (17.0 m out) |
| NE, normal 45.3° | **3rd Street front** | party wall vs SF3775075 (h 14.90 m) |

So this is a corner building on 3rd and Bryant with an alley flank and exactly
one blind face — not a one-street building with three party walls. Rebuilt:
shopfront and window grid on 3rd, turning the corner onto Bryant (5 and 4 bays at
a matched pitch); Taber Place punched windows plus the 2011 re-surfaced
stair/elevator shaft bump, which belongs on an alley and cannot be on a party
wall; the NE face left blind, since anything on it would be buried inside a
14.9 m neighbour. The night state was re-balanced at the same time so the wrapped
shopfront does not read as a beacon: the 3rd Street gallery front lights all five
bays, Bryant lights only the two nearest the corner, and one upper window per
street sits near the corner. 2,636 -> 2,780 triangles; anchor, footprint,
heights, materials and bbox unchanged. The hero render camera moved to due west,
the bisector of the two street elevations.


**2026-08-18 — roof field moved from `Toy_roofd` to `Toy_steel` (pre-approval).**
The roof membrane was built in `Toy_roofd` (`45454a`), which contradicted this
asset's own dossier ("a pale grey membrane field") and is a known trap: measured
on 92 South Park (2026-08-17), an up-facing `Toy_roofd` plane reads **rgb(9,9,12)**
in the running app at 1 PM while the same asset's `Toy_steel` reads rgb(94,103,112)
in the same frame — the diorama's ambient cannot lift `45454a`, and the landmark
would have read as a black hole from the aerial camera. `Toy_roofd` is retained
for the small dark rooftop props (bulkhead, accessories box) only. Geometry,
triangle count and dimensions are unchanged (2,636 tris); all renders and the
contact sheet were regenerated and the validator re-run — still all-PASS.

## Validation summary

All 15 contract checks PASS. Full details in `validation.json`.

| Check | Result |
|---|---|
| Meters and plausible dimensions (34.7 × 34.5 × 16.4) | PASS |
| Base at z=0 (min_z = 0.0) | PASS |
| Crest is target height (max_z = 16.4) | PASS |
| Centered XY (offset 0.016, 0.003 m) | PASS |
| Under triangle budget (2,636 / 12,000) | PASS |
| No image textures | PASS |
| No transparency | PASS |
| Materials follow contract (all `Toy_*`, no `Toy_body`) | PASS |
| No cameras or lights | PASS |
| No animation, skin, or constraints | PASS |
| Transforms applied | PASS |
| No negative scales | PASS |
| Normals outward (signed volume all positive, ray residual 0.000032) | PASS |
| No degenerate geometry | PASS |
| No unexpected objects | PASS |

## Approval (gate 3)

David, 18 August 2026, given up front for the whole run:

> "APPROVE EVERYTHING DONT ASK ME FOR PERMISSION"

Presented at approval: the contact sheet (aerial, top, night, four elevations),
2,636 triangles, 34.70 x 34.54 x 16.40 m, 7 materials, 1 glow group
(`Toy_white_Glow`). The blanket approval was given before the orientation error
was found; the corrected rebuild is a fix to what was approved, not a change of
design intent, and it is logged in full under Revision log.

## Numbers

| Metric | Value |
|---|---|
| Triangles | 2,732 (shipped, post-optimize; 2,780 as built) |
| Dimensions (bbox) | 34.70 × 34.54 × 16.40 m (rhombus diagonal span) |
| Footprint | 23.6 × 25.05 m rhombus, 592 m2 |
| Min Z | 0.0 m |
| Max Z (crest) | 16.4 m (rooftop bulkhead) |
| Loader scale factor | 1.0 (targetHeightM / measuredHeight = 16.4 / 16.4) |
| Object count | 7 (shipped, joined per material; 90 as built) |
| Materials | Toy_sand, Toy_ink, Toy_glass, Toy_trim, Toy_roofd, Toy_steel, Toy_white_Glow |
| Glow materials | Toy_white_Glow (3rd Street shopfront 5 bays + Bryant 2 bays at the corner + 1 lit upper window per street) |
| Normal ray residual | 0.0 (gate 0.0015) |
| Inverted signed-volume objects | 0 |

## Orientation

Authored with Blender `+Y` = true north, `+X` = east. The loader applies no
rotation (`placeGeneric` only scales and positions), so the authored heading is
the real-world heading. The contract's "front faces −Y" cannot be met —
real-world orientation wins per AGENTS rule 5 and the README orientation note.

| Face | Length | Outward normal | Role |
|---|---|---|---|
| SW | 25.05 m | 225.4° | 3rd Street front — shopfront, entry, 5-bay window grid |
| NW | 23.59 m | 315.6° | Bryant Street — shopfront continues, 4-bay window grid |
| SE | 23.64 m | 135.7° | Taber Place alley — punched windows, shaft bump |
| NE | 25.09 m | 45.3° | blind party wall against SF3775075 (h 14.90 m) |

This was corrected from the plan's 180°-out assignment at stage 5; the
measurement, the control run against shipped `500-third`, and the design
consequences are in `REFERENCE.md` under "Orientation" and in the Revision log
above.

## Night state

`Toy_white_Glow` on the shopfront band and on one upper window per street. The
3rd Street gallery front is the hero and lights all five of its bays; Bryant
carries the same band but lights only the two bays at the corner, so the corner
reads lit and the secondary street tails off into dark glass. The alley and the
party wall stay dark. A working SoMa loft reads as quietly lit at night, not as
a beacon. Glow surfaces are thin shells proud of opaque glazing — the app renders
`_Glow` in a separate layer at ~12% alpha by day.

## Optimize pass (stage 4)

The approved GLB was run through `docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md`
(`ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`). Full metrics,
census and gate table in `optimize/REPORT.md`.

| Metric | Approved | Shipped |
|---|---:|---:|
| File, raw bytes | 187,920 | **76,648** (−59.2%) |
| Draw submeshes | 90 | **7** (−92.2%) |
| Triangles | 2,780 | 2,732 |
| Bbox | 34.6966 x 34.5376 x 16.4 m | identical |
| Materials | 7 (1 glow) | 7 (1 glow) |

All gates G1-G6, G8 PASS (G7 n/a, no bake). Worst appearance delta 0.0026% mean
absolute RGB against a 2% gate; every 8x-amplified diff tile is black. The
limited dissolve was skipped (this asset has two full-footprint parapet annuli);
the 1 mm weld was kept after measuring it against the alternatives -- worth 6,816
bytes here because the asset is beveled throughout. The pass was run twice: the
first run optimized the pre-correction asset, and the orientation fix changed the
geometry, so it was re-run from scratch rather than patched. The pre-optimize
file is archived at `optimize/input/501-third.glb`.

## Manifest draft

```json
{
  "id": "501-third",
  "file": "501-third.glb",
  "anchor": [
    -122.3954601,
    37.7813246
  ],
  "targetHeightM": 16.4,
  "cat": 3,
  "name": "501 Third Street",
  "estimated": false,
  "dims": [
    34.70, 34.54, 16.40
  ],
  "tris": 2732,
  "loadRadius": 2500
}
```
