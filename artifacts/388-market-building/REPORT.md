# 388 Market Street — build report

Miniature GLB for SF-SIM, FiDi batch (stages 1–2 of docs/asset-pipeline/ADDRESS-TO-ASSET.md, BATCH mode), built 2026-10-25 from `docs/asset-plans/388-market-building.md` with the shared kit in `tools/landmark-kit/`.

## Result

Validation **PASS** ("all checks pass"). 3,468 triangles (FiDi cap 5,000). Crest 111.9 m = target 111.9 m (LiDAR).

## Deliverables

- `build_388_market_building.py` — deterministic build (`blender -b --python build_388_market_building.py`)
- `388-market-building.glb`, `388-market-building.blend`
- `validate_388_market_building.py` → `validation.json`; `render_388_market_building.py` → renders
- Renders: `388-market-building-{north,east,south,west,top,aerial,aerial-night}.png`, `388-market-building-contact-sheet.png`
- `REFERENCE.md`

## Contract (from validation.json, fresh-scene re-import)

| | |
|---|---|
| Triangles | 3,468 (budget 5,000) |
| Dimensions | 64.7478 x 58.1355 x 111.9 m |
| min Z / XY centre offset | 0.0 / (0.0, 0.0) |
| Objects | 2 (388-market-building_body, 388-market-building_night_glow) |
| Materials | Toy_glass, Toy_glassd, Toy_roofd, Toy_rust, Toy_sand_Glow, Toy_steel, Toy_stone, Toy_white_Glow |
| Anchor | [-122.3980735, 37.7921812] |

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

Lit lobby glazing, hashed lit windows on the granite faces and behind the glass, a white crown line. Glow is laid as thin outward skins over solid faces (700 glow faces, 699 unobstructed outward).

## Iterations

- Iteration 1 (before the photo): continuous granite/glass ribbon stripes at 118 m (OSM).
- Iteration 2 (after the photo and Wikipedia): punched granite grid, glass Pine wall, glass veil over the upper Market face, glass bays on the prow; height set to the LiDAR roof 111.9 m after Wikipedia's 94 m proved inconsistent with the measured roof.

## Gate 3 — approval

Pending: renders sent to David.
