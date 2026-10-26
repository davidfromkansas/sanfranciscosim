# Mechanics' Institute — build report

Miniature GLB for SF-SIM, Financial District batch (stages 1–2 of docs/asset-pipeline/ADDRESS-TO-ASSET.md,
BATCH mode), built from `docs/asset-plans/first-national-bank-building.md` with the shared kit in `tools/landmark-kit/`.

## Result

Validation **PASS** ("all checks pass"). 1,882 triangles (batch cap 3,000). Crest 43.0 m = target.

## Deliverables

- `build_first_national_bank_building.py` — deterministic build; `first-national-bank-building.glb`, `first-national-bank-building.blend`
- `validate_first_national_bank_building.py` -> `validation.json` (`--height 43.0 --budget 3000 --anchor -122.4030408,37.7887368`)
- `render_first_national_bank_building.py` -> `first-national-bank-building-{aerial,aerial-night,top,north,east,south,west}.png`, `first-national-bank-building-contact-sheet.png`
- `REFERENCE.md`

## Contract (validation.json, fresh-scene re-import)

| | |
|---|---|
| Triangles | 1,882 (body 1,516, glow 366) |
| Dimensions | 31.454 x 41.8278 x 43.0 m |
| min Z / XY centre offset | 0.0 / (0.0, 0.0) |
| Objects | 2 |
| Materials | Toy_concrete, Toy_glassd, Toy_ink, Toy_roofd, Toy_sand_Glow, Toy_steel, Toy_stone, Toy_trim |
| Anchor | [-122.4030408, 37.7887368] |
| Glow faces unobstructed | 360 / 366 |

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

Lit base arches and library arcade, lit portal fanlight, scattered office windows.

## Iterations

- First build passed; renders accepted.

## Gate 3 — approval

Pending: renders sent to David.
