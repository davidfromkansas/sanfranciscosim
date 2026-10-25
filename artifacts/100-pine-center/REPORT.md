# 100 Pine Center — build report

Miniature GLB for SF-SIM, FiDi batch (stages 1–2 of docs/asset-pipeline/ADDRESS-TO-ASSET.md, BATCH mode), built 2026-10-25 from `docs/asset-plans/100-pine-center.md` with the shared kit in `tools/landmark-kit/`.

## Result

Validation **PASS** ("all checks pass"). 2,820 triangles (FiDi cap 5,000). Crest 145.0 m = target 145.0 m (published).

## Deliverables

- `build_100_pine_center.py` — deterministic build (`blender -b --python build_100_pine_center.py`)
- `100-pine-center.glb`, `100-pine-center.blend`
- `validate_100_pine_center.py` → `validation.json`; `render_100_pine_center.py` → renders
- Renders: `100-pine-center-{north,east,south,west,top,aerial,aerial-night}.png`, `100-pine-center-contact-sheet.png`
- `REFERENCE.md`

## Contract (from validation.json, fresh-scene re-import)

| | |
|---|---|
| Triangles | 2,820 (budget 5,000) |
| Dimensions | 48.984 x 49.0617 x 145.0 m |
| min Z / XY centre offset | 0.0 / (0.0, 0.0) |
| Objects | 2 (100-pine-center_body, 100-pine-center_night_glow) |
| Materials | Toy_bronze, Toy_cream, Toy_glassd, Toy_roofd, Toy_sand_Glow, Toy_steel, Toy_stone, Toy_white_Glow |
| Anchor | [-122.3990118, 37.7926485] |

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

Lit lobby band behind the columns, hashed lit panes in the ribbon windows, a white crown line on the roof screen. Glow is laid as thin outward skins over solid faces (700 glow faces, 700 unobstructed outward).

## Iterations

- Iteration 1: built from the Commons photo; bands, notched corners and the flat screened roof read. No changes needed.

## Gate 3 — approval

Pending: renders sent to David.
