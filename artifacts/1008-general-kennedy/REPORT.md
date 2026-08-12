# 1008 General Kennedy Avenue — build report

**`1008-general-kennedy.glb` — validated, all 16 contract checks PASS.** A miniature of
the 1930s concrete Mission Revival hospital ward at 1008 General Kennedy Avenue in the
Presidio's Letterman complex, now part of the Thoreau Center for Sustainability.

Where this report and `docs/asset-plans/1008-general-kennedy.md` disagree, **this report
wins** — it describes what was built and why.

## Numbers

| | |
|---|---|
| File | `1008-general-kennedy.glb`, 371,992 bytes |
| Triangles | **5,688** (budget 9,000) |
| Objects | 148 |
| Dimensions | 55.131 × 35.473 × 11.900 m |
| Bounding box | min `[-27.565, -17.736, 0.0]`, max `[27.565, 17.736, 11.9]` |
| min Z | 0.000 m |
| XY centre offset | `[0.0, 0.0]` |
| Materials | `Toy_brick`, `Toy_glass`, `Toy_glass_Glow`, `Toy_ink`, `Toy_red`, `Toy_steel`, `Toy_stone`, `Toy_trim`, `Toy_trim_Glow`, `Toy_white` — all flat, all on-palette |
| Glow materials | `Toy_glass_Glow` (9 lit windows), `Toy_trim_Glow` (head landing soffit) |
| Textures / cameras / lights / animation | 0 / 0 / 0 / 0 |
| Transforms | applied; no negative scales |
| Normals | outward — 148/148 objects pass per-object signed volume; 31,500 visibility rays, 0 flipped visible faces (0.00% residual) |
| Degenerate triangles | 0 |

**The XY bounding box is 55.1 × 35.5 m for a building that is 55.14 × 12.02 m.** That is
the axis-aligned box of a long thin bar rotated 26.85° off the world axes, not a scale
error. The validator asserts all three dimensions explicitly so this cannot be mistaken
for one later.

## Orientation

Authored in true-world orientation: Blender `+Y` = north, `+X` = east, so the loader
(`placeGeneric` in `app/src/assets.js`, which only scales and positions) drops it in at its
real heading.

- Long axis: **116.85°** true, east head facing General Kennedy Avenue; **296.85°** at the
  arcade end
- Long elevations face **26.85°** (northeast, toward the 1007 courtyard) and **206.85°**
  (southwest, toward 1009)

The contract's "front faces −Y" rule cannot be honoured literally — this building's public
face points east-southeast. Per the plans README, real-world orientation wins (AGENTS rule
5). Recorded here as required.

## The anchor is not the footprint centre — deliberately

The building is not symmetric about its own footprint: the head block's roof overhangs
0.6 m past the east wall while the arcade's flat slab stops dead at the west end. Authoring
on the true footprint therefore left the model's XY bounding-box centre 0.668 m east and
0.999 m north of the origin, which fails the contract's "centered in x/y" rule.

Resolution: the geometry was translated by `(−0.668, +0.999)` m so the bbox centre is
exactly the origin, and the manifest anchor was moved by the same vector in the opposite
sense, so the building still lands on its real footprint.

| | lon | lat |
|---|---|---|
| Footprint OBB centre | −122.4514885 | 37.8007968 |
| **Manifest anchor (use this)** | **−122.4514809** | **37.8007878** |

## Height normalization

The chimney crest is the tallest geometry and lands at exactly **11.900 m**, so the
loader's `targetHeightM / measuredHeight` scale is 1.0.

| Level | Height | Source |
|---|---|---|
| Plinth top | 1.0 m | inferred |
| Eave (bar and head) | 7.8 m | inferred: base + two 3.4 m storeys |
| Main ridge | 10.9 m | Overture 2026-07-22, parent polygon — complex-wide |
| Head cross-hip ridge | 11.17 m | derived: the bar's pitch over the wider head span |
| **Chimney crest** | **11.9 m** | inferred: ridge + 1.0 m stack — **the manifest target** |

Because the crest is inferred rather than published, the manifest entry sets
`"estimated": true`.

## Corrections made to the plan's dossier

The plan is a head start, not a citation, and re-verification found five substantive
errors. All are described in `REFERENCE.md`; the largest:

1. **The roof form was wrong in the plan.** It called for a separate hip over the head
   block at a higher eave. Aerial imagery shows bar and head sharing one eave line and one
   unbroken ridge, with the head's extra width producing a higher splayed cross-hip at the
   same pitch. Rebuilt. This changed the model's whole silhouette from above, which for a
   building the camera looks down on is the entire recognition.
2. Chimneys: 4 → 6, section 0.9 m → 0.75 m, counted off Esri z20 imagery.
3. The head block's flanks were left blank by the plan's massing recipe; the real building
   has windows there. Four added per flank.
4. The exterior stair in `Toy_ink` read as a black smear at the app's camera. Changed to
   `Toy_steel`, which is also closer to the real galvanised stair.
5. The night state was confined to one long elevation, leaving the building unlit through
   half the app's orbit. Redistributed across both flanks.

## Iterations

| Pass | Change | Why |
|---|---|---|
| 1 | First build, 4,988 tris | Baseline |
| 2 | Origin moved to the XY bbox centre; anchor shifted to match | XY offset was `[0.668, −0.999]`, at the edge of the 1 m tolerance |
| 3 | Aerial camera azimuth 117° → 158° | At 117° the camera looked straight down the ridge and the 55 m bar collapsed to a roof plane — the review render was useless for judging the building |
| 4 | Roof rebuilt: continuous ridge + splayed cross-hip; chimneys 3 → 6; fascia 0.25 → 0.40 m; stair to `Toy_steel` | Correction 1, 2 and 4 above; the deeper fascia is what makes the eave read as a shadow line rather than vanishing into the white wall |
| 5 | Windows added to the head block's flanks | Correction 3 |
| 6 | Night state redistributed across both flanks; landing soffit glow shrunk | Correction 5; the soffit shell read as a bright bracket |

## Design decisions worth recording

- **`Toy_red` for the tile, `Toy_brick` for the chimneys.** `Toy_brick` (`#c96f4a`) is
  closer to real weathered barrel tile than `Toy_red` (`#c4453c`), but using it for both
  would flatten the stacks into the roof from above — and from above is where this
  building is seen. The stacks keep the browner colour so they read as separate objects on
  a saturated field.
- **The roof is real hip geometry**, with a genuine ridge and four hip edges, not a
  bevelled plane. The style bible's rule that the camera looks down and roofs are facades
  makes this the one place on this building where geometry is worth spending.
- **The bar's 60 mm off-centre position within the envelope was kept.** It is what both
  surveys say; correcting it to "tidy" would be inventing.
- **Nine lit windows out of 44.** This is a non-profit office campus, not a working
  hospital. A fully lit 40 m ward bar would read as the wrong building.

## Renders

All regenerated from the final export, and all depicting the same GLB (the render script
re-imports the exported file into an empty scene rather than rendering the authoring
scene).

`1008-general-kennedy-north.png`, `-east.png`, `-south.png`, `-west.png` (one orthographic
rig, identical scale/lighting/exposure, differing only in azimuth), `-top.png`,
`-aerial.png` (78 mm lens, 31° down, from the southwest flank), `-aerial-night.png`, and
`-contact-sheet.png`.

Note that all four elevations show the building obliquely: it runs ESE–WNW, so no compass
direction is square onto a face. The aerial is the view to judge from.

## Manifest entry

```json
{
  "id": "1008-general-kennedy",
  "file": "1008-general-kennedy.glb",
  "anchor": [
    -122.4514809,
    37.8007878
  ],
  "targetHeightM": 11.9,
  "cat": 3,
  "name": "1008 General Kennedy Avenue",
  "estimated": true,
  "dims": [
    55.131,
    35.473,
    11.9
  ],
  "tris": 5688,
  "loadRadius": 2500
}
```

## Reproducing

```
blender -b --python build_1008_general_kennedy.py
blender -b --python render_1008_general_kennedy.py
blender -b --python render_1008_general_kennedy.py -- --night
python3 make_contact_sheet.py
blender -b --python validate_1008_general_kennedy.py
```

## Known limitations

- The ridge height is a complex-wide figure, not a measurement of this ward. Everything
  above the eave is therefore proportionally right but not surveyed.
- The west arcade stub is modelled as open single-storey. Whether this particular ward's
  connector is open, enclosed or two-storey was not resolved.
- The window rhythm is 11 bays, inferred from oblique photography.
- **The integration exclusion zone is the open problem, not the asset.** The procedural
  source polygon is the entire Thoreau Center, not this ward. See §2.13 of the plan: a
  radius large enough to clear this building will also delete 1007 and 1009. This is
  addressed in the integration commit; it is called out here so it is not lost.
