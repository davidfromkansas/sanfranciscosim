# Old Federal Reserve Bank — build report

Miniature GLB for SF-SIM, Financial District batch (stages 1–2 of docs/asset-pipeline/ADDRESS-TO-ASSET.md,
BATCH mode), built from `docs/asset-plans/301-battery-street.md` with the shared kit in `tools/landmark-kit/`.

## Result

Validation **PASS** ("all checks pass"). 2,814 triangles (batch cap 3,000). Crest 47.6 m = target.

## Deliverables

- `build_301_battery_street.py` — deterministic build; `301-battery-street.glb`, `301-battery-street.blend`
- `validate_301_battery_street.py` -> `validation.json` (`--height 47.6 --budget 3000 --anchor -122.4008159,37.7943076`)
- `render_301_battery_street.py` -> `301-battery-street-{aerial,aerial-night,top,north,east,south,west}.png`, `301-battery-street-contact-sheet.png`
- `REFERENCE.md`

## Contract (validation.json, fresh-scene re-import)

| | |
|---|---|
| Triangles | 2,814 (body 2,654, glow 160) |
| Dimensions | 82.5657 x 51.3874 x 47.6 m |
| min Z / XY centre offset | 0.0 / (0.0, 0.0) |
| Objects | 2 |
| Materials | Toy_concrete, Toy_glassd, Toy_glassl, Toy_roofd, Toy_sand_Glow, Toy_stone |
| Anchor | [-122.4008159, 37.7943076] |
| Glow faces unobstructed | 160 / 160 |

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

Lit banking hall behind the colonnade, lit court skylight, scattered office windows.

## Iterations

- First validate failed (26 degenerate triangles) — the setback offset collapsed two short jogs; used a jog-free outline for it.
- North elevation showed a blank court face; added windows and lit panes to it.

## Gate 3 — approval

Pending: renders sent to David.
