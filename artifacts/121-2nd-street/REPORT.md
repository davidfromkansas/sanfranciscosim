# The Rapp Building — build report

Miniature GLB for SF-SIM, Financial District batch (stages 1–2 of docs/asset-pipeline/ADDRESS-TO-ASSET.md, BATCH mode), built 2026-10-25 from `docs/asset-plans/121-2nd-street.md` with the shared kit in `tools/landmark-kit/`.

## Result

Validation **PASS** ("all checks pass"). 598 triangles (cap 3,000). Crest 27.5 m = target 27.5 m — measured: DataSF LiDAR median roof 27.46 m (majority 27.37 m); OSM height 27. The list's 99 m was the 101 Second Street tower's LiDAR.

## Deliverables

- `build_121_2nd_street.py` — deterministic build (`blender -b --python build_121_2nd_street.py`)
- `121-2nd-street.glb`, `121-2nd-street.blend`
- `validate_121_2nd_street.py` → `validation.json` (`--budget 3000`); `render_121_2nd_street.py` → renders
- Renders: `121-2nd-street-aerial-night.png`, `121-2nd-street-aerial.png`, `121-2nd-street-contact-sheet.png`, `121-2nd-street-east.png`, `121-2nd-street-north.png`, `121-2nd-street-south.png`, `121-2nd-street-top.png`, `121-2nd-street-west.png`
- `REFERENCE.md`

## Contract (from validation.json, fresh-scene re-import)

| | |
|---|---|
| Triangles | 598 |
| Dimensions | 36.2117 x 35.4245 x 27.5 m (world-axis bbox) |
| min Z / XY centre offset | 0.0 / (0.0, 0.0) |
| Objects | 2 (121-2nd-street_body, 121-2nd-street_night_glow) |
| Materials | Toy_concrete, Toy_cream, Toy_glassd, Toy_roofd, Toy_sand_Glow, Toy_steel, Toy_stone |
| Anchor | [-122.3992003, 37.7878349] |

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

Lit shopfronts and scattered upper windows on the 2nd Street front. (30 glow faces, 30 unobstructed outward).

## Iterations

- Iteration 1 failed `no_degenerate_geometry`: a 0.2 m bevelled sidewalk collapsed; raised to 0.25 m. Roof first had a 1.1 m dark block above the cornice; replaced with a cream parapet.

## Gate 3 — approval

Pending: renders sent to David.
