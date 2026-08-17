# 150 South Park — build report

Asset: `artifacts/150-south-park/150-south-park.glb`, manifest id `150-south-park`.
Built 16 August 2026 from `docs/asset-plans/150-south-park.md` via
`docs/asset-pipeline/ADDRESS-TO-ASSET.md`.

**Where this report disagrees with the plan, this report is correct** — the plan's Part 2
was written before the Jan 2025 Street View frontage was measured against the survey.

---

## 1. Shipped numbers

| | |
|---|---|
| Triangles | **3,084** (cap 6,000) |
| Objects | 54 |
| Dimensions (m) | 19.852 x 17.586 x **8.000** |
| Min Z | 0.000 |
| XY centre offset | (0.292, 0.518) m |
| Materials | 9 — `Toy_ink`, `Toy_white`, `Toy_oxblood`, `Toy_glass`, `Toy_glassl`, `Toy_roofd`, `Toy_steel`, `Toy_gold_Glow`, `Toy_glass_Glow` |
| Glow groups | 2 — `Toy_gold_Glow` (shopfront), `Toy_glass_Glow` (upper windows) |
| File | 186,856 B raw / 36,622 B gzip (pre-optimize) |
| Anchor | `-122.3947673, 37.7813810` (footprint area centroid) |
| Front heading | 133.1° true (SE), authored in true-world orientation |
| Validation | `validation.json` — **overall PASS**, all 16 checks |

The 19.9 x 17.6 m axis-aligned bounding box is the expected consequence of a ~43°
real-world heading on a building nowhere wider than 9.72 m, not a scale error.

## 2. Corrections to the dossier

Every one of these came from measuring the Jan 2025 Street View frontage against the
survey's 5.54 m frontage (94.8 px/m horizontally) rather than trusting the plan's
proportional guesses.

1. **The "150" is stacked VERTICALLY**, not written across the wall. It is a 0.28 m wide,
   0.86 m tall column of thin numerals between the display window and the entrance door.
   The plan (2.6, 2.7 step 6) described three numerals in a row; the first build did that
   and the numerals overlapped both neighbouring openings, because the white gap between
   them is only 0.67 m. Rebuilt as a stacked column, exaggerated to 0.40 m wide x 1.04 m
   tall with a 60 mm stroke so a listed recognition cue survives at thumbnail size.
2. **The black/white split is at 4.55 m, not 3.80 m.** The plan derived 3.80 m from a
   two-storey count. It is not a floor line — it is a painted finish line with a projecting
   drip, and the photograph puts it at ~58% of the wall's pixel height, which after the
   pano's tan expansion is 4.5–4.9 m. Built at 4.55 m. The consequence is a taller white
   base and a shorter black band than the plan drew, which is what the photograph shows.
3. **The upper windows are 1.15 x 1.35 m at z 5.15–6.50**, centred at u 1.40 and 4.31 —
   not 1.70 x 1.60 at z 4.55–6.15 centred symmetrically. Measured.
4. **The whole ground-floor layout was re-measured**, and every element moved:

   | Element | Plan 2.7 | Built (measured) |
   |---|---|---|
   | secondary door | u 0.80, w 0.85, z 0–2.30 | u 0.66, w 0.90, z 0–2.05 |
   | display window | u 2.55, w 1.95, z 0.85–2.85 | u 2.79, w 1.89, z 0.40–2.75 |
   | "150" | u 3.75, horizontal | u 4.08, vertical column, z 1.70–2.56 |
   | entrance door | u 4.70, w 1.00, z 0–2.60 + transom 2.68–3.08 | u 4.88, w 0.90, z 0–2.75 with a transom bar at 2.10 |
   | canopy | u 3.45, w 3.70, z 3.15–3.35 | u 2.61, w 3.00, z 3.60–3.85 |
   | gooseneck lamps | u 1.30 / 5.15 | u 0.60 / 4.87 — **outboard of the canopy, one over each door**, which is what the photograph shows |

5. **The parapet runs at one height the whole way round.** The plan (2.7 step 9) proposed a
   rear parapet at 7.85 m below a front crest at 8.00 m. Neither photograph shows a step,
   and fabricating one would be invention. Uniform at 8.00 m; the coping ring sets the
   bounding-box top.
6. **The parapet carries a slim `Toy_steel` coping**, 0.09 m deep. The plan's 2.4 is right
   that the real parapet has no cornice and no decorative coping band and that its
   plainness next to 140's bracketed cornice is a recognition cue — but a painted-brick
   parapet does carry metal flashing, and it is what makes the ring read against the deck
   from the app's downward camera (2.9 asked for exactly that read and the plan's own
   material table had no way to deliver it).
7. **The canopy stays are diagonal rods, not an L-bracket.** `face_panel` cannot express a
   member that runs out and up at once; the first build modelled them as an L and they read
   as coat hooks. A `strut()` helper was added.
8. **The rear window band is 5.40 x 1.50 m**, not 4.20 x 1.35 — the Jan 2025 pano shows it
   running most of the way across the 9.72 m rear wall, and the aerial camera reads that
   face over the rear yard.
9. **`Toy_oxblood` is `#7a4034`, not the `#8c4a3c` the plan proposed.** The first render put
   a terracotta note on the building that read louder than anything else on it.

## 3. Deliberate deviations from the contract or the style bible

- **Off-palette material (WARN, not FAIL).** `Toy_oxblood` (`#7a4034`) is a palette
  extension. The window frames are a dark warm brown-red; `Toy_rust` (`#a86444`) is too
  orange and too light on a 0.17 m frame and `Toy_coral` far too saturated. Same argument
  as 155 South Park's `Toy_peach` and 380 Brannan's `Toy_slate`.
- **`Toy_ink` for the painted brick.** The real colour is a slightly cooler charcoal
  (~`#2f3338`) than `Toy_ink`'s warm near-black (`#3a3530`). `Toy_ink` was kept for palette
  discipline and because it is the same real-world "SoMa black-painted front" colour that
  155 South Park's shopfront uses — the two buildings face each other across the oval and
  sharing the black is correct family behaviour.
- **Semantic exaggeration, spent in two places only:** the window frames (0.17 m thick,
  0.09 m proud) and the address numerals (stroke 25 mm → 60 mm, column 0.86 m → 1.04 m).
  Nothing else is exaggerated.
- **Orientation:** the asset contract's "front faces −Y" cannot be honoured — the real front
  faces SE 133.1°, and `placeGeneric()` never rotates. Authored in true-world orientation
  per AGENTS rule 5 and the plans README.

## 4. Weakest surfaces, stated plainly

- **The lower rear wall is deliberately blank.** The only photograph of the rear is a Jan
  2025 pano shot through a 3.05 m fence, which hid everything below the window band. There
  is almost certainly a door down there; modelling one would be invention, so the wall is
  left plain. This is the model's weakest surface.
- **The crest, 8.00 m, is LiDAR + tag consensus, not a measurement of this model's own
  reference photograph.** Solving the Jan 2025 pano two ways gives 6.4 m and 9.2 m, and the
  same method applied to 140 South Park next door returns 6.8 m against its known 9.88 m
  LiDAR median. A zoomed Street View frame cannot do better than about ±1.5 m here. The
  DataSF modal roof-deck cell (7.48 m) plus OSM/Overture `height = 8` is the best evidence
  available and is what shipped. REFERENCE.md §7.1 carries the working.
- **The LiDAR `hgt_max` of 9.95 m was discarded** as a 3σ outlier on a σ = 0.78 m footprint
  — the corner street tree, with the 5.20 m `hgt_min` as the matching artifact. Thirteen
  permits from 1988 to 2024 record no rooftop structure.

## 5. Review renders

Regenerated from the final export (the rig re-imports the GLB, so every image depicts
exactly the geometry that ships):

`150-south-park-north.png`, `-east.png`, `-south.png`, `-west.png` (four elevations, one
orthographic rig, identical scale/framing/lighting/exposure, differing only in azimuth);
`-top.png`; `-aerial.png` (high three-quarter, 105 mm, 30° down, from the SE); 
`-aerial-night.png`; `-contact-sheet.png`.

Because the real front faces SE 133.1°, the labelled `south` and `east` elevations each
catch the frontage at ~45°. That is a property of a true-compass rig on a 43°-rotated
building, not a framing error.

## 6. Night state

Hero glow: the shopfront — display window and entrance — in `Toy_gold_Glow`, reading as the
one lit ground floor at the head of the park. Supporting accent: **both** upper windows in
`Toy_glass_Glow`, cool. Both are lit deliberately: the 2017 permits name an "upper level
unit", a "live/work bathroom" and a "residential entry", so that floor is residential
live/work, and a home with one window lit and one dark reads as an office. The rear does not
glow. All glow surfaces are thin shells standing proud of the opaque glazing behind them.

## 7. Gate 3 — approval

Pending. Presented to the user with the contact sheet, the aerial day and night renders and
the numbers above.

> *(approval quote and date to be recorded here before stage 4)*
