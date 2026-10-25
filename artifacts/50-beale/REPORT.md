# 50 Beale Street — build report

Miniature GLB for SF-SIM, Transbay batch (stages 1–2 of
docs/asset-pipeline/ADDRESS-TO-ASSET.md, BATCH mode), built 2026-10-25 from
`docs/asset-plans/50-beale.md` with the shared kit in `tools/landmark-kit/`.

## Result

Validation **PASS** ("all checks pass"). 5,282 triangles (budget 27,000 kit cap;
plan cap 12,000). Crest 100.0 m = target height 100.0 m (published 328 ft; LiDAR max 101.33 m).

## Deliverables

- `build_50_beale.py` — deterministic build (`blender -b --python build_50_beale.py`)
- `50-beale.glb`, `50-beale.blend`
- `validate_50_beale.py` → `validation.json`; `render_50_beale.py` → renders below
- Renders: `50-beale-aerial-night.png`, `50-beale-aerial.png`, `50-beale-contact-sheet.png`, `50-beale-east.png`, `50-beale-north.png`, `50-beale-south.png`, `50-beale-top.png`, `50-beale-west.png`
- `REFERENCE.md` (sources, dimensions, cues, uncertainties)

## Contract (from validation.json, fresh-scene re-import)

| | |
|---|---|
| Triangles | 5,282 |
| Dimensions | 90.4472 x 90.2892 x 100.0 m (world-axis bbox) |
| min Z / XY centre offset | 0.0 / (0.0, 0.0) |
| Objects | 2 (50-beale_body, 50-beale_night_glow) |
| Materials | Toy_bronze, Toy_glassd, Toy_ink, Toy_leaf, Toy_leafd, Toy_roofd, Toy_rust, Toy_sand_Glow, Toy_steel, Toy_stone |
| Anchor | [-122.396486, 37.791257] |

| Check | Result |
|---|---|
| crest_normalized_to_target | PASS |
| plausible_metre_dimensions | PASS |
| base_at_z_zero | PASS |
| centered_xy | PASS |
| under_triangle_budget | PASS |
| no_image_textures | PASS |
| no_transparency | PASS |
| materials_follow_contract | PASS |
| has_night_glow | PASS |
| no_cameras_or_lights | PASS |
| no_animation_skin_or_constraints | PASS |
| transforms_applied | PASS |
| no_negative_scales | PASS |
| normals_outward_signed_volume | PASS |
| normals_outward_ray_residual_within_tolerance | PASS |
| glow_skins_face_outward | PASS |
| no_degenerate_geometry | PASS |
| no_unexpected_objects | PASS |

## Geometry and materials

- 70 x 38 m plan at yaw −44.8°: dark glass recessed 3 m behind `Toy_ink` columns at 6.5 m (0–7.5 m).
- Shaft 7.5–93 m: one banded loft of `Toy_bronze` glass with 1.2 m `Toy_ink` spandrels at 3.9 m and ink fins at 3.3 m.
- Roof: deck and ink parapet at 93 m; ink penthouse inset 4 m to 96 m with louvre fins and cap; plant to 100 m.
- Plinth and five large trees along Beale Street (NE face).

All materials are flat `Toy_*` (roughness 0.85, no textures, no alpha); off-palette tones
are documented in REFERENCE.md.

## Night state

Scattered `Toy_sand_Glow` windows over the curtain wall and a lit base band. Glow is laid as thin outward skins over solid faces
(862 glow faces, all unobstructed outward).

## Iterations

- Iteration 1 (lead draft): massing and colour match the photo. Moved the tree row from the SW (mid-block) face to the Beale Street (NE) face.

## Gate 3 — approval

Pending: renders sent to David.
