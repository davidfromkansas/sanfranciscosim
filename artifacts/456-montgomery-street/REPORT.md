# 456 Montgomery Street — build report

Miniature GLB for SF-SIM, Financial District batch (stages 1–2 of docs/asset-pipeline/ADDRESS-TO-ASSET.md, BATCH mode), built 2026-10-25 from `docs/asset-plans/456-montgomery-street.md` with the shared kit in `tools/landmark-kit/`.

## Result

Validation **PASS** ("all checks pass"). 3,296 triangles (cap 5,000). Crest 115.2 m = target 115.2 m — published roof 115.2 m (CTBUH via the Wikipedia tallest-buildings list); LiDAR median 114.5 m, peak 118.7 m.

## Deliverables

- `build_456_montgomery_street.py` — deterministic build (`blender -b --python build_456_montgomery_street.py`)
- `456-montgomery-street.glb`, `456-montgomery-street.blend`
- `validate_456_montgomery_street.py` → `validation.json` (`--budget 5000`); `render_456_montgomery_street.py` → renders
- Renders: `456-montgomery-street-aerial-night.png`, `456-montgomery-street-aerial.png`, `456-montgomery-street-contact-sheet.png`, `456-montgomery-street-east.png`, `456-montgomery-street-north.png`, `456-montgomery-street-south.png`, `456-montgomery-street-top.png`, `456-montgomery-street-west.png`
- `REFERENCE.md`

## Contract (from validation.json, fresh-scene re-import)

| | |
|---|---|
| Triangles | 3,296 |
| Dimensions | 41.8414 x 49.3577 x 115.2 m (world-axis bbox) |
| min Z / XY centre offset | 0.0 / (0.0, 0.0) |
| Objects | 2 (456-montgomery-street_body, 456-montgomery-street_night_glow) |
| Materials | Toy_glassd, Toy_roofd, Toy_sand_Glow, Toy_steel, Toy_stone, Toy_white, Toy_white_Glow |
| Anchor | [-122.402634, 37.7935913] |

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

Lit bank windows on Montgomery, lit band in the recessed transfer floor, scattered `Toy_sand_Glow` windows laid just proud of the piers, `Toy_white_Glow` crown line. (540 glow faces, 540 unobstructed outward).

## Iterations

- Iteration 1: the shaft's built-in night skin sat behind the 1.9 m pier rhythm and 35% of the glow faces were blocked (validator FAIL); replaced with panes laid proud of the piers. The bank's lit windows were moved off the column face.
- Renders read as intended (white pinstripe tower over a darker bank); no further change.

## Gate 3 — approval

Pending: renders sent to David.
