# 501 Third Street — build report

## What was built

A stylized miniature GLB of 501 Third Street, San Francisco — a 1920
unreinforced-masonry industrial loft on the 45° SoMa grid. The asset is a
three-storey rhombus prism (23.6 × 25.05 m, 592 m2 footprint) with a dark
storefront base, a two-band industrial window grid on the 3rd Street face,
punched windows on the three rear faces, a flat parapet at 14 m, and a rooftop
bulkhead at 16.4 m (the crest). Authored in true-world orientation (3rd Street
front faces NE, 45.2° true).

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
- **Rear faces modelled with punched windows (conservative).** The LiDAR
  footprint (568 m2) matches the parcel (567 m2), suggesting the building fills
  its lot — two or three faces may be blind party walls. Modelled with punched
  windows on all three rear faces; if they are blind party walls, the windows
  are buried in the neighbour and invisible from the street, and the 3rd Street
  face (the only one the camera sees clearly) carries the identity.

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

## Numbers

| Metric | Value |
|---|---|
| Triangles | 2,636 |
| Dimensions (bbox) | 34.70 × 34.54 × 16.40 m (rhombus diagonal span) |
| Footprint | 23.6 × 25.05 m rhombus, 592 m2 |
| Min Z | 0.0 m |
| Max Z (crest) | 16.4 m (rooftop bulkhead) |
| Loader scale factor | 1.0 (targetHeightM / measuredHeight = 16.4 / 16.4) |
| Object count | 86 |
| Materials | Toy_sand, Toy_ink, Toy_glass, Toy_trim, Toy_roofd, Toy_steel, Toy_white_Glow |
| Glow materials | Toy_white_Glow (storefront uplight + 2 lit upper windows) |
| Normal ray residual | 0.000032 (gate 0.0015) |
| Inverted signed-volume objects | 0 |

## Orientation

Authored with Blender `+Y` = true north, `+X` = east. The 3rd Street front faces
north-east (outward normal 45.2° true). The contract's "front faces −Y" cannot
be met — real-world orientation wins per AGENTS rule 5 and the README
orientation note. The loader applies no rotation (`placeGeneric` only scales and
positions).

## Night state

`Toy_white_Glow` on the storefront band (5 bays of uplight) and two lit
upper-floor windows on the 3rd Street face. A working SoMa loft reads as
quietly lit at night, not as a beacon. Glow surfaces are thin shells proud of
opaque glazing — the app renders `_Glow` in a separate layer at ~12% alpha by
day.

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
  "tris": 2636,
  "loadRadius": 2500
}
```
