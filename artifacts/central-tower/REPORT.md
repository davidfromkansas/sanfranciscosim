# Central Tower — build report

Miniature GLB for SF-SIM, FiDi batch (stages 1–2 of docs/asset-pipeline/ADDRESS-TO-ASSET.md, BATCH mode), built 2026-10-25 from `docs/asset-plans/central-tower.md` with the shared kit in `tools/landmark-kit/`.

## Result

Validation **PASS** ("all checks pass"). 1,570 triangles (FiDi cap 5,000). Crest 91.0 m = target 91.0 m (published).

## Deliverables

- `build_central_tower.py` — deterministic build (`blender -b --python build_central_tower.py`)
- `central-tower.glb`, `central-tower.blend`
- `validate_central_tower.py` → `validation.json`; `render_central_tower.py` → renders
- Renders: `central-tower-{north,east,south,west,top,aerial,aerial-night}.png`, `central-tower-contact-sheet.png`
- `REFERENCE.md`

## Contract (from validation.json, fresh-scene re-import)

| | |
|---|---|
| Triangles | 1,570 (budget 5,000) |
| Dimensions | 39.9676 x 39.4503 x 91.0 m |
| min Z / XY centre offset | 0.0 / (0.0, 0.0) |
| Objects | 2 (central-tower_body, central-tower_night_glow) |
| Materials | Toy_concrete, Toy_glassd, Toy_granite, Toy_roofd, Toy_sand_Glow, Toy_steel, Toy_stone, Toy_white, Toy_white_Glow |
| Anchor | [-122.4035852, 37.7871882] |

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

Lit shopfronts, hashed lit windows in the bay system on both shaft sections, a white light line under the top parapet. Glow is laid as thin outward skins over solid faces (282 glow faces, 282 unobstructed outward).

## Iterations

- Iteration 1 (before the photo arrived): cream punched tower with a two-step crown; the rear chamfer made the offset roof deck self-intersect (black sliver in the top view).
- Iteration 2 (after the photo): rebuilt as the 1938 Moderne tower — rose granite base, white piers with recessed grey window columns, single setback at ~62 m, flat-topped upper shaft; setbacks offset from a clean square.

## Gate 3 — approval

Pending: renders sent to David.
