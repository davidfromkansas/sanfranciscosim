# 380 Brannan Street — build report

Miniature GLB for SF-SIM, built 12 August 2026 from `docs/asset-plans/380-brannan.md`
via the address-to-asset pipeline (`docs/asset-pipeline/ADDRESS-TO-ASSET.md`).

**This report beats the plan.** Where the dossier in the plan file and this report
disagree, this report and `REFERENCE.md` are correct.

## 1. Headline numbers

Both columns are real: the asset was built, approved, then optimized in stage 4
(`optimize/REPORT.md`). **The shipped column is what the manifest describes.**

| | As built | **Shipped (post-optimize)** |
|---|---|---|
| Triangles | 7,832 (cap 9,000) | **7,760** |
| Objects | 115 | 12 |
| Draw submeshes | 116 | **13** |
| Dimensions (AABB) | 31.3134 x 31.5872 x 12.60 m | 31.3134 x 31.5872 x 12.60 m |
| Min Z | 0.0 | 0.0 |
| XY centre offset | (0.186, 0.019) m | (0.186, 0.019) m |
| Materials | 11, all `Toy_*`, flat, opaque | 11, identical set |
| Glow materials | `Toy_glass_Glow`, `Toy_trim_Glow` | identical |
| File, raw | 461,728 B | **222,516 B** (−51.8%) |
| Contract validation | PASS on all 16 checks | **PASS on all 16 checks** |
| Anchor | `-122.3940217, 37.7806308` | unchanged |
| Target height | 12.6 m (bbox top normalized exactly, so loader scale = 1.0) | unchanged |

Compression is `EXT_meshopt_compression` without `KHR_mesh_quantization`, matching
`pipeline/compress-assets.mjs` — see `optimize/REPORT.md` §4 for why the optimize
prompt's own recipe was overridden.

Note the AABB is ~31 x 31 m for a 20.2 x 23.9 m building. That is the expected
consequence of authoring at the real 45.6° SoMa heading, not a scale error.

## 2. Dossier corrections made during the build

Three source conflicts were resolved before modelling. All three are the kind that
silently produce a wrong building.

1. **Storeys: 2, not 3.** The SF Assessor roll records 3.0 storeys in every year
   2007-2025. Every building permit 1990-2015 records 2, and both street-level
   photographs show two floors. 11,560 sq ft over a 480 m2 footprint is ~2.24
   floors — two full floors plus a mezzanine, which is the likely source of the
   assessor's third storey.

2. **OSM `height=11` is the roof deck, not the crest.** It coincides almost exactly
   with the LiDAR median (11.02 m), which makes it look trustworthy. The parapet
   crest is ~11.9 m and the tallest feature 12.64 m. Target height is 12.6 m.

3. **The front is painted, not exposed brick.** Listings describe a "brick and
   timber building", true of the structure and of the rear and flanks, but the
   Brannan Street elevation is painted slate gray with a coral band. Building from
   listing copy alone would have produced the wrong hero elevation.

## 3. Design decisions

- **Coral band as the sole identity.** The building's one memorable feature is the
  full-width coral stripe under the parapet cap. It was thickened to 1.1 m so it
  survives at thumbnail scale — the only place semantic exaggeration was spent — and
  it returns 1.1 m onto each flank so it reads from three-quarter angles. It does
  **not** glow: it is a daylight identity feature, and lighting it would misread as
  signage.

- **Palette extension: `Toy_slate` `#6f7883`.** The painted front is a medium slate
  blue-gray with no palette match; `Toy_stone` is far too warm and `Toy_steel` too
  light. Off-palette is a WARN, not a FAIL, and the style bible's §7 architectural
  base explicitly includes medium gray. Recorded here as a deliberate extension.

- **`Toy_rust` rather than `Toy_brick` for the masonry.** The first render proved
  `Toy_brick` (`#c96f4a`) sits in the same hue family as `Toy_coral` (`#e8735a`):
  the flanks and the identity band merged into one colour and the building lost its
  only accent. `Toy_rust` (`#a86444`) is browner and restores the separation.

- **Stone coping over the parapet.** Without it the whole parapet ring read as one
  saturated band from the app's downward camera — the single worst problem in the
  first aerial. A stone coping is also what a real brick parapet is finished with.

- **Corbel band in wall colour.** Rendered in the lighter `Toy_brick` the rear/flank
  corbel read as a *second* coral stripe wrapping the building and stole the front's
  cue. It is now the same rust as the wall and reads on its 0.22 m projection alone.

- **Roof designed, not decorated.** Three clusters spread over the whole deck — a
  five-skylight field over the second floor (the listing's "skylights on the second
  floor"), a three-unit mechanical row plus duct along the NE flank, and a
  penthouse/hatch/vent group at the back. The first roof clustered everything in one
  half and read as an empty tray.

- **Twin roof mast dropped.** Visible in the street photograph, but a hairline at the
  app's camera, and including it would have put the bounding-box top — and therefore
  `targetHeightM` — on a feature that reads as nothing.

- **Fire escape rehung at the sill.** At 5.00-5.75 m it crossed the bottom of the
  window behind it and read as a dark smudge; at 5.35-6.15 m it reads as a balcony.

## 4. Orientation deviation from the contract (recorded, per plans README)

The asset contract says "front faces −Y". 380 Brannan's front faces **southeast,
bearing 135.6°**, and `placeGeneric()` in `app/src/assets.js` applies no rotation, so
the model is authored in true-world orientation (`+Y` north, `+X` east) and the
contract rule is deliberately not honoured literally. Real-world orientation wins
(AGENTS rule 5). The building is built directly on its measured footprint polygon
rather than as an axis-aligned box that is then rotated.

## 5. Iteration log

| Pass | Change | Reason |
|---|---|---|
| 1 | initial build | 21,176 tris, roof furniture projected outside the footprint (v ran along the outward normal instead of into the block) |
| 2 | inward roof axis; adaptive bevel budget; arch segments 6 → 4 | fixed placement; 21,176 → 6,896 tris, under the 9,000 cap |
| 3 | `Toy_rust` masonry; stone coping; roof furniture redistributed; wider/shorter upper windows; smaller canopy; chunkier fire escape; landscape render framing | first aerial: parapet read as a saturated ring, roof read as an empty tray, elevations overflowed the portrait frame |
| 4 | corbel band to wall colour; fire escape rehung at the sill | second render: corbel read as a second coral stripe; fire escape smudged its window |
| 5 | bevel width capped at 0.30 x thinnest dimension + `remove_doubles`/`dissolve_degenerate` | validation FAIL: 132 degenerate triangles and 65 undefined loop normals from `clamp_overlap` pinching thin panels shut |

## 6. Validation

Fresh factory-reset Blender 5.2.0 LTS scene, re-importing the exported GLB — the
authoring scene was not inspected. `validation.json` holds the full record.

| Check | Result |
|---|---|
| Fresh isolated scene, re-imported final GLB | PASS |
| Dimensions plausible in real metres | PASS |
| Crest normalized to 12.6 m (loader scale 1.0) | PASS |
| Base at z = 0 | PASS (0.0) |
| Centred in XY | PASS (0.186, 0.019) |
| Triangles ≤ 9,000 | PASS (7,832) |
| No image textures | PASS |
| No transparency | PASS |
| Materials follow contract (`Toy_*`, no `Toy_body`) | PASS |
| No cameras or lights | PASS |
| No animation, skinning or constraints | PASS |
| Transforms applied, no negative scales | PASS |
| Normals outward — per-object signed volume | PASS (115/115 positive, 0 inverted) |
| Normals outward — ray residual ≤ 0.15% | PASS (0.0% of 31,500 first hits) |
| No degenerate geometry | PASS (0) |
| No unexpected or foreign objects | PASS |

Per-object signed volume is the authoritative normals test here because the asset is
a union of interpenetrating closed solids; the 31,500-ray visibility test is the
secondary check and returned a zero residual.

## 7. Renders

All generated from the exported GLB, not the authoring scene:
`380-brannan-north.png`, `-east.png`, `-south.png`, `-west.png` (one shared
orthographic rig, identical scale/framing/lighting/exposure, differing only in
azimuth), `-top.png`, `-aerial.png` (105 mm lens, 38° down, from the southeast onto
the Brannan front), `-aerial-night.png`, and `-contact-sheet.png`.

Day renders show `_Glow` shells at 12% alpha to mimic the app's day pass, so the
building is judged as the app actually shows it.

## 8. Manifest entry

Values measured from the validated export.

```json
{
  "id": "380-brannan",
  "file": "380-brannan.glb",
  "anchor": [
    -122.3940217,
    37.7806308
  ],
  "targetHeightM": 12.6,
  "cat": 3,
  "name": "380 Brannan Street",
  "estimated": false,
  "dims": [
    31.3134,
    31.5872,
    12.6
  ],
  "tris": 7832,
  "loadRadius": 2500
}
```

`cat` 3 = `office` in `pipeline/taxonomy.mjs` (an incubator in a converted
warehouse; `20` = `warehouse` was the alternative). `estimated: false` — the anchor
and footprint are measured and the height is the measured LiDAR maximum.

**Streaming decision (mandatory).** `loadRadius: 2500`, the skill's default
`max(2500, 12.6 * 30)`. Because this is a Case B landmark whose baked procedural
building is carved out, beyond the radius the site is a gap — but a 12.6 m building
at 2.5 km is far below one pixel, so the absence is illegible. Default taken
deliberately, not by omission.

## 9. Gate 3 — approval

Approved by David on 12 August 2026, verbatim:

> "hey just checking in -- this model looks great -- please proceed to finish the
> entire pipeline. i approve it all. dont wait for me"

## 10. Rebuild

```
blender -b --python build_380_brannan.py
blender -b --python render_380_brannan.py
blender -b --python render_380_brannan.py -- --night
python3 make_contact_sheet.py
blender -b --python validate_380_brannan.py
```

Blender 5.2.0 LTS, Pillow 11.3.0. The build script is deterministic; re-running it
reproduces the same 7,832-triangle export.
