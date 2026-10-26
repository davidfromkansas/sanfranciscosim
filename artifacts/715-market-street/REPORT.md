# 715–719 Market Street — build report

Miniature GLB for SF-SIM, Financial District batch (stages 1–2 of docs/asset-pipeline/ADDRESS-TO-ASSET.md,
BATCH mode), built from `docs/asset-plans/715-market-street.md` with the shared kit in `tools/landmark-kit/`.

## Result

Validation **PASS** ("all checks pass"). 1,290 triangles (batch cap 3,000). Crest 32.6 m = target.

## Deliverables

- `build_715_market_street.py` — deterministic build; `715-market-street.glb`, `715-market-street.blend`
- `validate_715_market_street.py` -> `validation.json` (`--height 32.6 --budget 3000 --anchor -122.4037015,37.7868764`)
- `render_715_market_street.py` -> `715-market-street-{aerial,aerial-night,top,north,east,south,west}.png`, `715-market-street-contact-sheet.png`
- `REFERENCE.md`

## Contract (validation.json, fresh-scene re-import)

| | |
|---|---|
| Triangles | 1,290 (body 1,086, glow 204) |
| Dimensions | 62.0963 x 55.4454 x 32.6 m |
| min Z / XY centre offset | 0.0 / (0.0, 0.0) |
| Objects | 2 |
| Materials | Toy_cream, Toy_glassd, Toy_ink, Toy_roofd, Toy_sand_Glow, Toy_steel, Toy_stone, Toy_trim, Toy_white_Glow |
| Anchor | [-122.4037015, 37.7868764] |
| Glow faces unobstructed | 204 / 204 |

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

Lit shopfronts, white sign band on Market, scattered upper windows.

## Iterations

- First build passed; renders accepted (no photo to compare).

## Gate 3 — approval

Pending: renders sent to David.
