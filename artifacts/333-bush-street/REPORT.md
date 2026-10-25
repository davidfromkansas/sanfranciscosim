# 333 Bush Street — build report

Miniature GLB for SF-SIM, FiDi batch (stages 1–2 of docs/asset-pipeline/ADDRESS-TO-ASSET.md, BATCH mode), built 2026-10-25 from `docs/asset-plans/333-bush-street.md` with the shared kit in `tools/landmark-kit/`.

## Result

Validation **PASS** ("all checks pass"). 4,464 triangles (FiDi cap 5,000). Crest 151.0 m = target 151.0 m (published).

## Deliverables

- `build_333_bush_street.py` — deterministic build (`blender -b --python build_333_bush_street.py`)
- `333-bush-street.glb`, `333-bush-street.blend`
- `validate_333_bush_street.py` → `validation.json`; `render_333_bush_street.py` → renders
- Renders: `333-bush-street-{north,east,south,west,top,aerial,aerial-night}.png`, `333-bush-street-contact-sheet.png`
- `REFERENCE.md`

## Contract (from validation.json, fresh-scene re-import)

| | |
|---|---|
| Triangles | 4,464 (budget 5,000) |
| Dimensions | 58.7734 x 57.6589 x 151.0 m |
| min Z / XY centre offset | 0.0 / (0.0, 0.0) |
| Objects | 2 (333-bush-street_body, 333-bush-street_night_glow) |
| Materials | Toy_bronze, Toy_glassd, Toy_granite, Toy_roofd, Toy_sand_Glow, Toy_stone |
| Anchor | [-122.4030673, 37.7905789] |

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

Lit lobby, hashed lit windows over the shaft and every terrace tier, a warm band around the crown box. Glow is laid as thin outward skins over solid faces (1432 glow faces, 1432 unobstructed outward).

## Iterations

- Iteration 1: terrace tiers centred on the plan overhung the stepped south-west corner in the top view.
- Iteration 2: tiers moved over the full-width Bush Street half of the plan (notched rectangles, 30 x 42 m stepping to 14 x 17 m) so they sit on the shaft.

## Gate 3 — approval

Pending: renders sent to David.
