# St. Regis Museum Tower — build report

Miniature GLB for SF-SIM, Financial District batch (stages 1–2 of docs/asset-pipeline/ADDRESS-TO-ASSET.md,
BATCH mode), built from `docs/asset-plans/3rd-street-tower.md` with the shared kit in `tools/landmark-kit/`.

## Result

Validation **PASS** ("all checks pass"). 3,632 triangles (batch cap 5,000). Crest 147.5 m = target.

## Deliverables

- `build_3rd_street_tower.py` — deterministic build; `3rd-street-tower.glb`, `3rd-street-tower.blend`
- `validate_3rd_street_tower.py` -> `validation.json` (`--height 147.5 --budget 5000 --anchor -122.4013679,37.7863061`)
- `render_3rd_street_tower.py` -> `3rd-street-tower-{aerial,aerial-night,top,north,east,south,west}.png`, `3rd-street-tower-contact-sheet.png`
- `REFERENCE.md`

## Contract (validation.json, fresh-scene re-import)

| | |
|---|---|
| Triangles | 3,632 (body 2,994, glow 638) |
| Dimensions | 68.5944 x 81.3845 x 147.5 m |
| min Z / XY centre offset | 0.0 / (0.0, 0.0) |
| Objects | 2 |
| Materials | Toy_glass, Toy_glassd, Toy_glassg, Toy_glassl, Toy_roofd, Toy_sand, Toy_sand_Glow, Toy_sky_Glow, Toy_steel, Toy_stone, Toy_trim, Toy_white_Glow |
| Anchor | [-122.4013679, 37.7863061] |
| Glow faces unobstructed | 638 / 638 |

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

Lit lobby/museum base, scattered sand-glow panes on both blocks, a sky-blue strip in the glass slot, lit penthouse panes and a white crown line.

## Iterations

- First validate failed `glow_skins_face_outward` (24 faces): lobby glow on the wing edge buried by the low strip, and the crown light line hidden inside the rail. Added an edge filter and pushed the line out.
- Renders checked against the photo: proportions and stone grid read; accepted.

## Gate 3 — approval

Pending: renders sent to David.
