# 150 California Street — build report

Miniature GLB for SF-SIM, Financial District batch (stages 1–2 of docs/asset-pipeline/ADDRESS-TO-ASSET.md, BATCH mode), built 2026-10-25 from `docs/asset-plans/150-california-street.md` with the shared kit in `tools/landmark-kit/`.

## Result

Validation **PASS** ("all checks pass"). 3,464 triangles (cap 5,000). Crest 100.6 m = target 100.6 m — published (Wikipedia/Emporis roof 100.59 m) as the glass-bay crest; LiDAR roof plane 96.9 m.

## Deliverables

- `build_150_california_street.py` — deterministic build (`blender -b --python build_150_california_street.py`)
- `150-california-street.glb`, `150-california-street.blend`
- `validate_150_california_street.py` → `validation.json`; `render_150_california_street.py` → renders below
- Renders: `150-california-street-aerial-night.png`, `150-california-street-aerial.png`, `150-california-street-contact-sheet.png`, `150-california-street-east.png`, `150-california-street-north.png`, `150-california-street-south.png`, `150-california-street-top.png`, `150-california-street-west.png`
- `REFERENCE.md` (sources, dimensions, cues, uncertainties)

## Contract (from validation.json, fresh-scene re-import)

| | |
|---|---|
| Triangles | 3,464 (budget passed to the validator: 5,000) |
| Dimensions | 51.1677 x 52.7719 x 100.6 m (world-axis bbox, incl. apron) |
| min Z / XY centre offset | 0.0 / (0.0, 0.0) |
| Objects | 2 (150-california-street_body, 150-california-street_night_glow) |
| Materials | Toy_concrete, Toy_glassd, Toy_glassl, Toy_leaf, Toy_leafd, Toy_roofd, Toy_rust, Toy_sand_Glow, Toy_sky_Glow, Toy_steel, Toy_stone |
| Anchor | [-122.3985069, 37.7936972] |
| Glow faces unobstructed outward | 626 / 626 |

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

Lit base windows, 30% lit tower panes, lit glass-bay floors and a sky-blue band at the bay's top.

## Iterations

- v1 passed all checks (3,464 tris); render reviewed against the photo.

## Gate 3 — approval

Pending: renders sent to David.
