# 77 Beale Street (Pacific Gas & Electric Building) — build report

Miniature GLB for SF-SIM, Transbay batch (stages 1–2 of
docs/asset-pipeline/ADDRESS-TO-ASSET.md, BATCH mode), built 2026-10-25 from
`docs/asset-plans/77-beale.md` with the shared kit in `tools/landmark-kit/`.

## Result

Validation **PASS** ("all checks pass"). 8,186 triangles (budget 27,000 kit cap;
plan cap 12,000). Crest 150.0 m = target height 150.0 m (published 149.96 m; LiDAR roof plane 144.66 m).

## Deliverables

- `build_77_beale.py` — deterministic build (`blender -b --python build_77_beale.py`)
- `77-beale.glb`, `77-beale.blend`
- `validate_77_beale.py` → `validation.json`; `render_77_beale.py` → renders below
- Renders: `77-beale-aerial-night.png`, `77-beale-aerial.png`, `77-beale-contact-sheet.png`, `77-beale-east.png`, `77-beale-north.png`, `77-beale-south.png`, `77-beale-top.png`, `77-beale-west.png`
- `REFERENCE.md` (sources, dimensions, cues, uncertainties)

## Contract (from validation.json, fresh-scene re-import)

| | |
|---|---|
| Triangles | 8,186 |
| Dimensions | 74.1048 x 74.1048 x 150.0 m (world-axis bbox) |
| min Z / XY centre offset | 0.0 / (0.0, 0.0) |
| Objects | 2 (77-beale_body, 77-beale_night_glow) |
| Materials | Toy_concrete, Toy_glassd, Toy_ink, Toy_leaf, Toy_roofd, Toy_rust, Toy_sand_Glow, Toy_steel, Toy_stone |
| Anchor | [-122.395754, 37.791782] |

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

- Notched 56 x 41 m plan at yaw 45°: dark-glass lobby recessed 2 m behind 1.5 m concrete piers (0–10 m).
- Shaft 10–145 m: `Toy_concrete` punched block (3.95 m storeys, 2.9 m pitch) with proud 0.7 x 0.55 m piers on the same 2.9 m rhythm.
- Crown 145–150 m: solid screen wall slotted (`Toy_ink`) between the piers; roof deck at 145 m and a plant cluster below the crest.
- Plinth and four trees on the Mission (SE) side.

All materials are flat `Toy_*` (roughness 0.85, no textures, no alpha); off-palette tones
are documented in REFERENCE.md.

## Night state

Scattered `Toy_sand_Glow` windows (~30 %) on all faces and a lit lobby band. Glow is laid as thin outward skins over solid faces
(1378 glow faces, all unobstructed outward).

## Iterations

- Iteration 1 (lead draft) reviewed against the Commons photo: pier rhythm, notches and crown slots read; no geometry change needed.

## Gate 3 — approval

Pending: renders sent to David.
