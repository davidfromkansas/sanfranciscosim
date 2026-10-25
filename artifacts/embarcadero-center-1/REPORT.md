# One Embarcadero Center — build report

Miniature GLB for SF-SIM, FiDi batch (stages 1–2 of docs/asset-pipeline/ADDRESS-TO-ASSET.md, BATCH mode), built 2026-10-25 from `docs/asset-plans/embarcadero-center-1.md` with the shared kit in `tools/landmark-kit/`.

## Result

Validation **PASS** ("all checks pass"). 4,696 triangles (FiDi cap 5,000). Crest 173.4 m = target 173.4 m (published).

## Deliverables

- `build_embarcadero_center_1.py` — deterministic build (`blender -b --python build_embarcadero_center_1.py`)
- `embarcadero-center-1.glb`, `embarcadero-center-1.blend`
- `validate_embarcadero_center_1.py` → `validation.json`; `render_embarcadero_center_1.py` → renders
- Renders: `embarcadero-center-1-{north,east,south,west,top,aerial,aerial-night}.png`, `embarcadero-center-1-contact-sheet.png`
- `REFERENCE.md`

## Contract (from validation.json, fresh-scene re-import)

| | |
|---|---|
| Triangles | 4,696 (budget 5,000) |
| Dimensions | 84.9689 x 45.1028 x 173.4 m |
| min Z / XY centre offset | 0.0 / (0.0, 0.0) |
| Objects | 2 (embarcadero-center-1_body, embarcadero-center-1_night_glow) |
| Materials | Toy_bronze, Toy_cream, Toy_glassd, Toy_glassl, Toy_glassl_Glow, Toy_ink, Toy_sand, Toy_sand_Glow, Toy_steel, Toy_stone |
| Anchor | [-122.3996222, 37.7944829] |

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

Lit base glazing, hashed lit window groups up the slab, a pale blue crown line under the parapet. Glow is laid as thin outward skins over solid faces (754 glow faces, 754 unobstructed outward).

## Iterations

- Iteration 1 (before the photo): vertical window slots like 4 Embarcadero Center, a wide podium box (removed: it overlapped neighbouring OSM buildings), 173 m.
- Iteration 2 (after the photo and Wikipedia): 173.4 m published roof; an even grid of punched windows (columns + per-storey spandrels) and the glazed band near the top seen in the photo; flat top kept.

## Gate 3 — approval

Pending: renders sent to David.
