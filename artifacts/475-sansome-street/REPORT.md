# 475 Sansome Street — build report

Miniature GLB for SF-SIM, Financial District batch (stages 1–2 of docs/asset-pipeline/ADDRESS-TO-ASSET.md, BATCH mode), built 2026-10-25 from `docs/asset-plans/475-sansome-street.md` with the shared kit in `tools/landmark-kit/`.

## Result

Validation **PASS** ("all checks pass"). 3,662 triangles (cap 5,000). Crest 89.7 m = target 89.7 m — measured: DataSF LiDAR peak 89.7 m (penthouse); main roof = LiDAR median 82.3 m (OSM height 82).

## Deliverables

- `build_475_sansome_street.py` — deterministic build (`blender -b --python build_475_sansome_street.py`)
- `475-sansome-street.glb`, `475-sansome-street.blend`
- `validate_475_sansome_street.py` → `validation.json` (`--budget 5000`); `render_475_sansome_street.py` → renders
- Renders: `475-sansome-street-aerial-night.png`, `475-sansome-street-aerial.png`, `475-sansome-street-contact-sheet.png`, `475-sansome-street-east.png`, `475-sansome-street-north.png`, `475-sansome-street-south.png`, `475-sansome-street-top.png`, `475-sansome-street-west.png`
- `REFERENCE.md`

## Contract (from validation.json, fresh-scene re-import)

| | |
|---|---|
| Triangles | 3,662 |
| Dimensions | 72.3412 x 48.6114 x 89.7 m (world-axis bbox) |
| min Z / XY centre offset | 0.0 / (0.0, 0.0) |
| Objects | 2 (475-sansome-street_body, 475-sansome-street_night_glow) |
| Materials | Toy_bronze, Toy_concrete, Toy_roofd, Toy_sand_Glow, Toy_steel, Toy_stone, Toy_white_Glow |
| Anchor | [-122.4019375, 37.7945747] |

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

Lit lobby ring, scattered lit windows proud of the piers, crown line. (374 glow faces, 374 unobstructed outward).

## Iterations

- Iteration 1 passed validation; massing reads correctly.

## Gate 3 — approval

Approved by David on 2026-10-26 (renders sent as twelve day/night overview sheets): "approve all".

## Stage 4 — optimize

Shipped as `app/public/sf-assets/landmarks/475-sansome-street.glb`, meshopt-compressed with the intake flags of `pipeline/compress-assets.mjs` (`gltfpack -c -km -kn -noq`): **185 KB → 88 KB** (53% smaller). Geometry is unchanged. Kit assets are already one body mesh and one glow mesh, so the Blender cleanup pass and the limited dissolve are skipped, as for the Transbay batch. Gate G3 (three.js GLTFLoader round-trip with MeshoptDecoder, `tools/glb-optimize/g3check`) passes.
