# Hearst Building — build report

Miniature GLB for SF-SIM, Financial District batch (stages 1–2 of docs/asset-pipeline/ADDRESS-TO-ASSET.md, BATCH mode), built 2026-10-25 from `docs/asset-plans/hearst-building.md` with the shared kit in `tools/landmark-kit/`.

## Result

Validation **PASS** ("all checks pass"). 2,998 triangles (cap 3,000). Crest 50.2 m = target 50.2 m — DataSF LiDAR roof (majority 50.19 m; OSM 49 m); no published height found.

## Deliverables

- `build_hearst_building.py` — deterministic build (`blender -b --python build_hearst_building.py`)
- `hearst-building.glb`, `hearst-building.blend`
- `validate_hearst_building.py` → `validation.json`; `render_hearst_building.py` → renders below
- Renders: `hearst-building-aerial-night.png`, `hearst-building-aerial.png`, `hearst-building-contact-sheet.png`, `hearst-building-east.png`, `hearst-building-north.png`, `hearst-building-south.png`, `hearst-building-top.png`, `hearst-building-west.png`
- `REFERENCE.md` (sources, dimensions, cues, uncertainties)

## Contract (from validation.json, fresh-scene re-import)

| | |
|---|---|
| Triangles | 2,998 (budget passed to the validator: 3,000) |
| Dimensions | 53.1946 x 53.3389 x 50.2 m (world-axis bbox, incl. apron) |
| min Z / XY centre offset | 0.0 / (0.0, 0.0) |
| Objects | 2 (hearst-building_body, hearst-building_night_glow) |
| Materials | Toy_cream, Toy_glassd, Toy_leaf, Toy_roofd, Toy_rust, Toy_sand_Glow, Toy_steel, Toy_stone, Toy_terracotta |
| Anchor | [-122.4030128, 37.7874579] |
| Glow faces unobstructed outward | 383 / 384 |

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

Lit arched base, ~25% lit punched windows, lit attic arches on the fronts.

## Iterations

- v1 (2,398 tris) passed, but the render showed the 23 m corner face and the rear blank (edge filter too tight).
- v2: windows on every face but the east party walls; storey pitch 3.95 m, 2.9 m window rhythm, no bevels on the 17-node prisms to stay under the cap: 2,998 tris, all checks pass.

## Gate 3 — approval

Approved by David on 2026-10-26 (renders sent as twelve day/night overview sheets): "approve all".

## Stage 4 — optimize

Shipped as `app/public/sf-assets/landmarks/hearst-building.glb`, meshopt-compressed with the intake flags of `pipeline/compress-assets.mjs` (`gltfpack -c -km -kn -noq`): **150 KB → 68 KB** (55% smaller). Geometry is unchanged. Kit assets are already one body mesh and one glow mesh, so the Blender cleanup pass and the limited dissolve are skipped, as for the Transbay batch. Gate G3 (three.js GLTFLoader round-trip with MeshoptDecoder, `tools/glb-optimize/g3check`) passes.
