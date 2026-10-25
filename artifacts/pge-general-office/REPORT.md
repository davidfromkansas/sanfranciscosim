# PG&E General Office Building (245 Market Street) — build report

Miniature GLB for SF-SIM, Transbay batch (stages 1–2 of
docs/asset-pipeline/ADDRESS-TO-ASSET.md, BATCH mode), built 2026-10-25 from
`docs/asset-plans/pge-general-office.md` with the shared kit in `tools/landmark-kit/`.

## Result

Validation **PASS** ("all checks pass"). 3,936 triangles (budget 27,000 kit cap;
plan cap 12,000). Crest 79.8 m = target height 79.8 m (DataSF LiDAR crest 79.77 m, measured).

## Deliverables

- `build_pge_general_office.py` — deterministic build (`blender -b --python build_pge_general_office.py`)
- `pge-general-office.glb`, `pge-general-office.blend`
- `validate_pge_general_office.py` → `validation.json`; `render_pge_general_office.py` → renders below
- Renders: `pge-general-office-aerial-night.png`, `pge-general-office-aerial.png`, `pge-general-office-contact-sheet.png`, `pge-general-office-east.png`, `pge-general-office-north.png`, `pge-general-office-south.png`, `pge-general-office-top.png`, `pge-general-office-west.png`
- `REFERENCE.md` (sources, dimensions, cues, uncertainties)

## Contract (from validation.json, fresh-scene re-import)

| | |
|---|---|
| Triangles | 3,936 |
| Dimensions | 67.7332 x 67.748 x 79.8 m (world-axis bbox) |
| min Z / XY centre offset | 0.0 / (0.0, 0.0) |
| Objects | 2 (pge-general-office_body, pge-general-office_night_glow) |
| Materials | Toy_cream, Toy_glassd, Toy_leaf, Toy_leafd, Toy_roofd, Toy_rust, Toy_sand_Glow, Toy_steel, Toy_stone, Toy_terracotta |
| Anchor | [-122.396849, 37.792385] |

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

- 43 x 41 m plan at yaw −45.3°: terracotta arcaded base 0–10 m (3.6 m arches at 5.4 m) with a cream cornice.
- Cream punched shaft 11–60 m; arched storey 60.5–67 m (3.0 m round-headed windows at 4.6 m) flush with the shaft.
- Terracotta cornice 67–68.6 m (1.2 m projection) with balustrade band; attic 68.6–72.5 m inset 1.5 m; set-back top block 72.5–77 m, cornice to 78 m, plant to 79.8 m.
- Plinth and three street trees on the Market (NW) face.

All materials are flat `Toy_*` (roughness 0.85, no textures, no alpha); off-palette tones
are documented in REFERENCE.md.

## Night state

Lit arcade, lit arched-window row, scattered `Toy_sand_Glow` windows on shaft, attic and top block. Glow is laid as thin outward skins over solid faces
(852 glow faces, all unobstructed outward).

## Iterations

- Iteration 1 (lead draft): setback tiers sat directly over the shaft with the arches on the top tier; the Commons photo shows the arched row flush with the shaft under the main cornice, then an attic and a smaller top block. Rebuilt the crown in that order.
- Moved the street trees from the SW (Beale) face to the Market (NW) face, as in the photo.

## Gate 3 — approval

Pending: renders sent to David.
