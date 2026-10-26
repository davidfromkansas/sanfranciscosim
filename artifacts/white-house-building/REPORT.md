# The White House (Raphael Weill & Co.) — build report

Miniature GLB for SF-SIM, Financial District batch (stages 1–2 of docs/asset-pipeline/ADDRESS-TO-ASSET.md, BATCH mode), built 2026-10-25 from `docs/asset-plans/white-house-building.md` with the shared kit in `tools/landmark-kit/`.

## Result

Validation **PASS** ("all checks pass"). 1,712 triangles (cap 3,000). Crest 32.1 m = target 32.1 m — measured: DataSF LiDAR median roof 32.15 m (majority 31.6 m); OSM height 32.

## Deliverables

- `build_white_house_building.py` — deterministic build (`blender -b --python build_white_house_building.py`)
- `white-house-building.glb`, `white-house-building.blend`
- `validate_white_house_building.py` → `validation.json` (`--budget 3000`); `render_white_house_building.py` → renders
- Renders: `white-house-building-aerial-night.png`, `white-house-building-aerial.png`, `white-house-building-contact-sheet.png`, `white-house-building-east.png`, `white-house-building-north.png`, `white-house-building-south.png`, `white-house-building-top.png`, `white-house-building-west.png`
- `REFERENCE.md`

## Contract (from validation.json, fresh-scene re-import)

| | |
|---|---|
| Triangles | 1,712 |
| Dimensions | 94.6486 x 61.8832 x 32.1 m (world-axis bbox) |
| min Z / XY centre offset | 0.0 / (0.0, 0.0) |
| Objects | 2 (white-house-building_body, white-house-building_night_glow) |
| Materials | Toy_cream, Toy_glassd, Toy_roofd, Toy_sand_Glow, Toy_stone, Toy_white |
| Anchor | [-122.404777, 37.7894367] |

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

Brightly lit shop windows on Sutter and Grant, scattered lit upper windows. (142 glow faces, 142 unobstructed outward).

## Iterations

- Iteration 1 passed validation, but the aerial (from the SW, over the blank party walls) showed a featureless dark roof. Added the rooftop parking deck: bay stripes, a stair house and three lamp strips that glow at night; re-rendered.

## Gate 3 — approval

Approved by David on 2026-10-26 (renders sent as twelve day/night overview sheets): "approve all".

## Stage 4 — optimize

Shipped as `app/public/sf-assets/landmarks/white-house-building.glb`, meshopt-compressed with the intake flags of `pipeline/compress-assets.mjs` (`gltfpack -c -km -kn -noq`): **94 KB → 44 KB** (52% smaller). Geometry is unchanged. Kit assets are already one body mesh and one glow mesh, so the Blender cleanup pass and the limited dissolve are skipped, as for the Transbay batch. Gate G3 (three.js GLTFLoader round-trip with MeshoptDecoder, `tools/glb-optimize/g3check`) passes.
