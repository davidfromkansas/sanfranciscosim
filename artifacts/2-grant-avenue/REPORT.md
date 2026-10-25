# Union Trust Bank Building (2 Grant Avenue) — build report

Miniature GLB for SF-SIM, Financial District batch (stages 1–2 of docs/asset-pipeline/ADDRESS-TO-ASSET.md, BATCH mode), built 2026-10-25 from `docs/asset-plans/2-grant-avenue.md` with the shared kit in `tools/landmark-kit/`.

## Result

Validation **PASS** ("all checks pass"). 1,126 triangles (cap 3,000). Crest 19.5 m = target 19.5 m — DataSF LiDAR roof (majority 19.51 m; OSM 20 m).

## Deliverables

- `build_2_grant_avenue.py` — deterministic build (`blender -b --python build_2_grant_avenue.py`)
- `2-grant-avenue.glb`, `2-grant-avenue.blend`
- `validate_2_grant_avenue.py` → `validation.json`; `render_2_grant_avenue.py` → renders below
- Renders: `2-grant-avenue-aerial-night.png`, `2-grant-avenue-aerial.png`, `2-grant-avenue-contact-sheet.png`, `2-grant-avenue-east.png`, `2-grant-avenue-north.png`, `2-grant-avenue-south.png`, `2-grant-avenue-top.png`, `2-grant-avenue-west.png`
- `REFERENCE.md` (sources, dimensions, cues, uncertainties)

## Contract (from validation.json, fresh-scene re-import)

| | |
|---|---|
| Triangles | 1,126 (budget passed to the validator: 3,000) |
| Dimensions | 35.6519 x 46.5038 x 19.5 m (world-axis bbox, incl. apron) |
| min Z / XY centre offset | 0.0 / (0.0, 0.0) |
| Objects | 2 (2-grant-avenue_body, 2-grant-avenue_night_glow) |
| Materials | Toy_glassd, Toy_glassl, Toy_roofd, Toy_sand_Glow, Toy_stone, Toy_white |
| Anchor | [-122.4046839, 37.7871305] |
| Glow faces unobstructed outward | 28 / 28 |

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

## Night state

Banking-hall windows lit warm (90%), glowing skylight.

## Iterations

- v1 passed all checks (1,126 tris).

## Gate 3 — approval

Pending: renders sent to David.
