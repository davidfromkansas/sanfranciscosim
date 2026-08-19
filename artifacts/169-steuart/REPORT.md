# 169 Steuart Street (Army & Navy YMCA Building) — build report

**Deliverable:** `artifacts/169-steuart/169-steuart.glb` — a validated miniature GLB of
the 1924 Army & Navy YMCA Building (Embarcadero YMCA / Harbor Court Hotel), 169 Steuart
Street / 166 The Embarcadero, San Francisco.

**Stage 2 gate: PASS.** `validation.json` reports `"overall": "PASS"` with all 16 contract
checks true, from a fresh-scene re-import of the exported GLB.

## Numbers

| | |
|---|---|
| Triangles | **19,908** (cap 22,000) |
| Objects | 14 (600 before the stage-4 join-per-material pass) |
| File size | **575,032 bytes** meshopt-compressed (1,352,416 pre-optimize, −57.5%) |
| Draw submeshes | 15 (602 pre-optimize) |
| Dimensions (axis-aligned) | 60.14 × 60.28 × **46.64** m |
| Building along its own axes | 42.35 × 41.84 m |
| min Z | 0.0000 m |
| XY centre offset | 0.181, 0.180 m |
| Materials | 13, all `Toy_*`, flat, no textures, no alpha, no `Toy_body` |
| Glow materials | `Toy_glass_Glow`, `Toy_gold_Glow`, `Toy_white_Glow` |
| Anchor | `-122.3919821, 37.7926993` |
| Front heading | 45.1° true (NE, The Embarcadero) |

The 60.1 × 60.3 m axis-aligned bounding box is the expected consequence of a 45.1° real
heading on a 42.35 × 41.84 m building, not a scale error. The bbox top is exactly 46.64 m
so the loader's `targetHeightM / measuredHeight` scale lands at 1.000.

## Heights built

| Element | Height | Basis |
|---|---|---|
| Tile-roof apex (the crest) | **46.64 m** | DataSF LiDAR `hgt_maxcm`, corroborated photogrammetrically |
| Tower eave / arcade head | 35.00 m | SKYDB "35 m / 10 floors"; the pano independently puts the arcade at 32.1–34.6 m |
| Arcade band springing | 31.55 m | derived |
| Embarcadero crest parapet | 30.90 m | Street View photogrammetry (30.87 m) |
| Eight-storey wing roof | 28.14 m | DataSF LiDAR `hgt_majoritycm` |
| Steuart street wall / podium | 14.00 m | *estimated* — three storeys counted in Street View |
| Corbel frieze head | 10.45 m | derived |
| Cast-stone base top | 9.60 m | Street View photogrammetry |

## Massing as built

1. Podium over the **whole** pentagon to 14.00 m — the survey's "covers the width of the
   block … on the 1st 2 floors".
2. Eight-storey mass over the 29.60 m of depth nearest The Embarcadero, at 28.14 m, with a
   12 × 8 m light court notched into it at v = 24.2 m. That is 65% of the footprint at the
   modal LiDAR plane, which is what reproduces the observed distribution.
3. The remaining 12.67 m of depth is the **Steuart Street street wall** at podium height —
   cream stucco over the northwest half (161–165, Harbor Court), dark red-brown brick over
   the southeast half (169, Embarcadero YMCA), with both entrances and the YMCA blade sign.
4. Tower 18 × 16 m centred on the Embarcadero frontage: one rank of windows, the arcade
   band, an eave at 35.00 m.
5. Red clay tile **hipped** roof, 19.7 × 17.7 m at the eave with a 2.4 m ridge, to 46.64 m,
   with a finial kept below the apex.

## Corrections to the dossier (REPORT beats plan)

1. **The plan's two-parallel-wings recipe does not close.** Its own band arithmetic left
   the second "wing" 5.6 m deep, which is not a wing. Built as one 29.60 m-deep mass with
   a court notched into it. The area fractions land in the same place; the geometry is
   buildable.
2. **Blank flanks were an error, and the first review caught it.** Both wing flanks came
   back as 28 m of unbroken brick. The real flanks are fenestrated — an open yard on the
   northwest, a light well on the southeast — and a blank wall reads as an unfinished
   model from three of the app's four approach angles. Added the shaft rhythm with no
   ornament: +3,396 triangles, the cheapest improvement in the asset.
3. **The light court initially overlapped the tower** (court centred at v = 21 m against a
   tower ending at v = 19 m). Moved to v = 24.2 m.
4. **The night hero did not light on the first attempt.** The arcade glow shells were
   nested *inside* their opaque ink reveals, so nothing emitted. They now keep the
   reveal's across-wall axis 0.14 m thicker so they stand proud on the visible side. This
   is the repo's standing rule about glow shells and it is easy to lose in a band of 34
   small openings.
5. **The bevel rounds the hip apex down by ~48 mm**, which would have left the export at
   46.592 m and made the loader scale 1.001. The build corrects the roof object alone
   about its eave so the export tops out at exactly 46.64 m.
6. **The flagpole is deliberately not modelled.** It is real, and it is what the LiDAR's
   `peak_1st_m` = 50.35 m sees, but a 50.35 m bounding box would rescale the whole
   building by 7% through `targetHeightM / measuredHeight`.

## Scope decision recorded

The asset is the **whole parcel**. DataSF condo lots `3715028` (161–165) and `3715029`
(169) share one `mapblklot`, one polygon and one structure; OSM's three ways are that one
outline drawn in pieces. Building "169 Steuart" from the 200 m² OSM stub would have put a
20 × 20 m three-storey box where a 42 × 42 m ten-storey landmark stands, and no exclusion
radius could then have cleared the rest of the lot. See `REFERENCE.md` §2.

## Renders

All regenerated from the final export. `169-steuart-north/east/south/west.png` (one
orthographic rig, identical scale, framing, lighting and exposure, differing only in
azimuth — each shows the building at 45° because that is its real heading),
`169-steuart-top.png`, `169-steuart-aerial.png` (ENE, 38° down, 70 mm — the only angle
that puts the hallmark elevation and the tile hip in one frame),
`169-steuart-aerial-night.png`, and `169-steuart-contact-sheet.png`.

## Reproducing

```
blender -b --python build_169_steuart.py
blender -b --python render_169_steuart.py
blender -b --python render_169_steuart.py -- --night
python3 make_contact_sheet.py
blender -b --python validate_169_steuart.py
```

## Stage 4 — optimize

The shipping `169-steuart.glb` is the **stage-4 output**: welded, joined per material
and meshopt-packed with `gltfpack@0.24 -c -km -kn -noq`. All eight optimize gates PASS;
the pre-optimize asset is archived byte-for-byte at `optimize/input/169-steuart.glb`
and the full metrics, waste census and A/B pixel deltas are in `optimize/REPORT.md`.
Geometry is unchanged — same triangles, same bounding box to the last decimal, worst
A/B pixel delta 0.919% and that is Monte-Carlo noise on the emissive arcade.

The renders above were made from the pre-optimize export; the A/B sheet in
`optimize/renders/contact_sheet.png` shows the two are indistinguishable.

## Stage 3 — approval

Quoted verbatim from the session brief of 18 August 2026, which stands as the approval for
this asset:

> "APPROVE EVERYTHING DONT ASK ME FOR PERMISSION"

The contact sheet, the day and night aerials and the numbers above were presented under
that standing approval and the pipeline advanced to stage 4.
