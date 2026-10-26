# 211 Main Street (Charles Schwab Building) — build report

Miniature GLB for SF-SIM, Financial District batch (stages 1–2 of docs/asset-pipeline/ADDRESS-TO-ASSET.md, BATCH mode), built 2026-10-25 from `docs/asset-plans/211-main-street.md` with the shared kit in `tools/landmark-kit/`.

## Result

Validation **PASS** ("all checks pass"). 2,152 triangles (cap 5,000). Crest 82.0 m = target 82.0 m — measured: DataSF LiDAR peak 82.0 m (penthouse); main roof = LiDAR median 73.3 m. OSM height 85 is unsourced.

## Deliverables

- `build_211_main_street.py` — deterministic build (`blender -b --python build_211_main_street.py`)
- `211-main-street.glb`, `211-main-street.blend`
- `validate_211_main_street.py` → `validation.json` (`--budget 5000`); `render_211_main_street.py` → renders
- Renders: `211-main-street-aerial-night.png`, `211-main-street-aerial.png`, `211-main-street-contact-sheet.png`, `211-main-street-east.png`, `211-main-street-north.png`, `211-main-street-south.png`, `211-main-street-top.png`, `211-main-street-west.png`
- `REFERENCE.md`

## Contract (from validation.json, fresh-scene re-import)

| | |
|---|---|
| Triangles | 2,152 |
| Dimensions | 73.2826 x 72.8776 x 82.0 m (world-axis bbox) |
| min Z / XY centre offset | 0.0 / (0.0, 0.0) |
| Objects | 2 (211-main-street_body, 211-main-street_night_glow) |
| Materials | Toy_bronze, Toy_roofd, Toy_sand, Toy_sand_Glow, Toy_steel, Toy_stone, Toy_white_Glow |
| Anchor | [-122.392854, 37.7905944] |

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

Lit lobby ring, scattered lit ribbon windows, crown line. (448 glow faces, 448 unobstructed outward).

## Iterations

- Iteration 1 passed validation; massing reads correctly.

## Gate 3 — approval

Pending: renders sent to David.
