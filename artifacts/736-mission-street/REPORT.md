# Contemporary Jewish Museum — build report

Miniature GLB for SF-SIM, Financial District batch (stages 1–2 of docs/asset-pipeline/ADDRESS-TO-ASSET.md,
BATCH mode), built from `docs/asset-plans/736-mission-street.md` with the shared kit in `tools/landmark-kit/`.

## Result

Validation **PASS** ("all checks pass"). 638 triangles (batch cap 3,000). Crest 24.0 m = target.

## Deliverables

- `build_736_mission_street.py` — deterministic build; `736-mission-street.glb`, `736-mission-street.blend`
- `validate_736_mission_street.py` -> `validation.json` (`--height 24.0 --budget 3000 --anchor -122.4036821,37.7860166`)
- `render_736_mission_street.py` -> `736-mission-street-{aerial,aerial-night,top,north,east,south,west}.png`, `736-mission-street-contact-sheet.png`
- `REFERENCE.md`

## Contract (validation.json, fresh-scene re-import)

| | |
|---|---|
| Triangles | 638 (body 580, glow 58) |
| Dimensions | 81.9536 x 83.2589 x 24.0 m |
| min Z / XY centre offset | 0.0 / (0.0, 0.0) |
| Objects | 2 |
| Materials | Toy_brick, Toy_cream, Toy_glassd, Toy_glassl, Toy_ink, Toy_leaf, Toy_leafd, Toy_roofd, Toy_rust, Toy_sand_Glow, Toy_sky, Toy_stone, Toy_white_Glow |
| Anchor | [-122.4036821, 37.7860166] |
| Glow faces unobstructed | 58 / 58 |

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

Lit arched window and portal, lit upper hall windows on the side faces, lit lobby panes in the dark wing, white squares on the cube.

## Iterations

- Iteration 1: arched window and portal were invisible (glass coplanar/inside the frame box). Rebuilt them as panes on the frame's front face and added upper hall glow; four buried glow faces fixed by an edge filter.

## Gate 3 — approval

Approved by David on 2026-10-26 (renders sent as twelve day/night overview sheets): "approve all".

## Stage 4 — optimize

Shipped as `app/public/sf-assets/landmarks/736-mission-street.glb`, meshopt-compressed with the intake flags of `pipeline/compress-assets.mjs` (`gltfpack -c -km -kn -noq`): **43 KB → 26 KB** (40% smaller). Geometry is unchanged. Kit assets are already one body mesh and one glow mesh, so the Blender cleanup pass and the limited dissolve are skipped, as for the Transbay batch. Gate G3 (three.js GLTFLoader round-trip with MeshoptDecoder, `tools/glb-optimize/g3check`) passes.
