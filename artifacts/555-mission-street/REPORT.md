# 555 Mission Street — build report

Miniature GLB for SF-SIM, FiDi batch (stages 1–2 of docs/asset-pipeline/ADDRESS-TO-ASSET.md, BATCH mode), built 2026-10-25 from `docs/asset-plans/555-mission-street.md` with the shared kit in `tools/landmark-kit/`.

## Result

Validation **PASS** ("all checks pass"). 4,754 triangles (FiDi cap 5,000). Crest 147.0 m = target 147.0 m (published).

## Deliverables

- `build_555_mission_street.py` — deterministic build (`blender -b --python build_555_mission_street.py`)
- `555-mission-street.glb`, `555-mission-street.blend`
- `validate_555_mission_street.py` → `validation.json`; `render_555_mission_street.py` → renders
- Renders: `555-mission-street-{north,east,south,west,top,aerial,aerial-night}.png`, `555-mission-street-contact-sheet.png`
- `REFERENCE.md`

## Contract (from validation.json, fresh-scene re-import)

| | |
|---|---|
| Triangles | 4,754 (budget 5,000) |
| Dimensions | 73.022 x 70.061 x 147.0 m |
| min Z / XY centre offset | 0.0 / (0.0, 0.0) |
| Objects | 2 (555-mission-street_body, 555-mission-street_night_glow) |
| Materials | Toy_glassg, Toy_glassl, Toy_leaf, Toy_leafd, Toy_roofd, Toy_rust, Toy_sand_Glow, Toy_steel, Toy_stone, Toy_white, Toy_white_Glow |
| Anchor | [-122.3985546, 37.7885452] |

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

Glowing glass lobby, hashed lit panes across the curtain wall, a white crown line on the glass screen. Glow is laid as thin outward skins over solid faces (946 glow faces, 939 unobstructed outward).

## Iterations

- Iteration 1 (before the photo): white fins and steel spandrels at 148 m (OSM).
- Iteration 2 (after the photo and Wikipedia): published 147 m; fins and spandrels switched to a pale silvery tone so the facade reads as one blue glass prism with fine mullions.

## Gate 3 — approval

Pending: renders sent to David.
