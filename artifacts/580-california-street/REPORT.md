# 580 California Street — build report

Miniature GLB for SF-SIM, Financial District batch (stages 1–2 of docs/asset-pipeline/ADDRESS-TO-ASSET.md, BATCH mode), built 2026-10-25 from `docs/asset-plans/580-california-street.md` with the shared kit in `tools/landmark-kit/`.

## Result

Validation **PASS** ("all checks pass"). 3,794 triangles (cap 5,000). Crest 107 m = target 107 m — published (Wikipedia/Emporis roof 107 m / 351 ft); LiDAR roof plane 97.3 m, mansard crest 104.8 m.

## Deliverables

- `build_580_california_street.py` — deterministic build (`blender -b --python build_580_california_street.py`)
- `580-california-street.glb`, `580-california-street.blend`
- `validate_580_california_street.py` → `validation.json`; `render_580_california_street.py` → renders below
- Renders: `580-california-street-aerial-night.png`, `580-california-street-aerial.png`, `580-california-street-contact-sheet.png`, `580-california-street-east.png`, `580-california-street-north.png`, `580-california-street-south.png`, `580-california-street-top.png`, `580-california-street-west.png`
- `REFERENCE.md` (sources, dimensions, cues, uncertainties)

## Contract (from validation.json, fresh-scene re-import)

| | |
|---|---|
| Triangles | 3,794 (budget passed to the validator: 5,000) |
| Dimensions | 50.0296 x 51.0103 x 107 m (world-axis bbox, incl. apron) |
| min Z / XY centre offset | 0.0 / (0.0, 0.0) |
| Objects | 2 (580-california-street_body, 580-california-street_night_glow) |
| Materials | Toy_concrete, Toy_copper, Toy_glassd, Toy_glassl, Toy_leaf, Toy_leafd, Toy_roofd, Toy_rust, Toy_sand_Glow, Toy_stone, Toy_white, Toy_white_Glow |
| Anchor | [-122.404152, 37.7929843] |
| Glow faces unobstructed outward | 817 / 826 |

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

Lit arched base, scattered office panes in bays and corner zones, a lit attic storey and a glowing lantern on the mansard.

## Iterations

- v1: 9,020 tris (bay spandrel rings) — replaced by flat spandrel quads every other storey and fewer corner windows: 3,794.
- v1 render: statues too small to read from the aerial; v2 enlarged them (1.3 m radius, 6.1 m tall) and set them proud on the cornice.

## Gate 3 — approval

Pending: renders sent to David.
