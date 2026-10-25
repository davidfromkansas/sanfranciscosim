# 123 Mission Street — build report

Miniature GLB for SF-SIM, Transbay batch (stages 1–2 of
docs/asset-pipeline/ADDRESS-TO-ASSET.md, BATCH mode), built 2026-10-25 from
`docs/asset-plans/123-mission.md` with the shared kit in `tools/landmark-kit/`.

## Result

Validation **PASS** ("all checks pass"). 5,742 triangles (budget 27,000 kit cap;
plan cap 12,000). Crest 124.0 m = target height 124.0 m (published; LiDAR max 127.19 m, majority 112.56 m).

## Deliverables

- `build_123_mission.py` — deterministic build (`blender -b --python build_123_mission.py`)
- `123-mission.glb`, `123-mission.blend`
- `validate_123_mission.py` → `validation.json`; `render_123_mission.py` → renders below
- Renders: `123-mission-aerial-night.png`, `123-mission-aerial.png`, `123-mission-contact-sheet.png`, `123-mission-east.png`, `123-mission-north.png`, `123-mission-south.png`, `123-mission-top.png`, `123-mission-west.png`
- `REFERENCE.md` (sources, dimensions, cues, uncertainties)

## Contract (from validation.json, fresh-scene re-import)

| | |
|---|---|
| Triangles | 5,742 |
| Dimensions | 56.2261 x 56.1397 x 124.0 m (world-axis bbox) |
| min Z / XY centre offset | 0.0 / (0.0, 0.0) |
| Objects | 2 (123-mission_body, 123-mission_night_glow) |
| Materials | Toy_glassd, Toy_leaf, Toy_leafd, Toy_roofd, Toy_rust, Toy_sand, Toy_sand_Glow, Toy_steel, Toy_stone |
| Anchor | [-122.394447, 37.791824] |

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

## Geometry and materials

- Notched 40.5 x 33.5 m plan at yaw −44.5°: dark glass recessed 1.6 m behind stone piers at 4.5 m (0–10 m).
- Shaft 10–114 m: `Toy_sand` punched block (3.95 m storeys, 2.6 m pitch), stone cornice.
- Crown: 3 m inset with 2.4 m notches, punched block to 120 m, stone parapet, plant to 124 m (normalised x1.004 by `tk.run`).
- Plinth and three trees on the Mission (NW) face.

All materials are flat `Toy_*` (roughness 0.85, no textures, no alpha); off-palette tones
are documented in REFERENCE.md.

## Night state

Scattered `Toy_sand_Glow` windows (30 % shaft, 40 % crown) and a lit base band. Glow is laid as thin outward skins over solid faces
(954 glow faces, all unobstructed outward).

## Iterations

- Iteration 1 (lead draft): reads correctly against the photo. Moved the tree row from the NE face to the Mission Street (NW) face.

## Gate 3 — approval

Pending: renders sent to David.
