# 625 Market Street ("Bank of America Building") — build report

Miniature GLB for SF-SIM, Financial District batch (stages 1–2 of docs/asset-pipeline/ADDRESS-TO-ASSET.md, BATCH mode), built 2026-10-25 from `docs/asset-plans/bank-of-america-building.md` with the shared kit in `tools/landmark-kit/`.

## Result

Validation **PASS** ("all checks pass"). 1,424 triangles (cap 5,000). Crest 60.1 m = target 60.1 m — DataSF LiDAR roof (majority 60.11 m); no published height.

## Deliverables

- `build_bank_of_america_building.py` — deterministic build (`blender -b --python build_bank_of_america_building.py`)
- `bank-of-america-building.glb`, `bank-of-america-building.blend`
- `validate_bank_of_america_building.py` → `validation.json`; `render_bank_of_america_building.py` → renders below
- Renders: `bank-of-america-building-aerial-night.png`, `bank-of-america-building-aerial.png`, `bank-of-america-building-contact-sheet.png`, `bank-of-america-building-east.png`, `bank-of-america-building-north.png`, `bank-of-america-building-south.png`, `bank-of-america-building-top.png`, `bank-of-america-building-west.png`
- `REFERENCE.md` (sources, dimensions, cues, uncertainties)

## Contract (from validation.json, fresh-scene re-import)

| | |
|---|---|
| Triangles | 1,424 (budget passed to the validator: 5,000) |
| Dimensions | 40.6249 x 40.8323 x 60.1 m (world-axis bbox, incl. apron) |
| min Z / XY centre offset | 0.0 / (0.0, 0.0) |
| Objects | 2 (bank-of-america-building_body, bank-of-america-building_night_glow) |
| Materials | Toy_cream, Toy_glassd, Toy_leaf, Toy_leafd, Toy_roofd, Toy_rust, Toy_sand, Toy_sand_Glow, Toy_steel, Toy_stone |
| Anchor | [-122.4016814, 37.7886452] |
| Glow faces unobstructed outward | 192 / 192 |

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

Bright shopfronts, ~30% lit windows, a brighter attic.

## Iterations

- v1 passed all checks (1,424 tris).

## Gate 3 — approval

Approved by David on 2026-10-26 (renders sent as twelve day/night overview sheets): "approve all".

## Stage 4 — optimize

Shipped as `app/public/sf-assets/landmarks/bank-of-america-building.glb`, meshopt-compressed with the intake flags of `pipeline/compress-assets.mjs` (`gltfpack -c -km -kn -noq`): **83 KB → 40 KB** (52% smaller). Geometry is unchanged. Kit assets are already one body mesh and one glow mesh, so the Blender cleanup pass and the limited dissolve are skipped, as for the Transbay batch. Gate G3 (three.js GLTFLoader round-trip with MeshoptDecoder, `tools/glb-optimize/g3check`) passes.
