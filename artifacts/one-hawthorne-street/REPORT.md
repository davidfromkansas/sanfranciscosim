# One Hawthorne — build report

Miniature GLB for SF-SIM, Financial District batch (stages 1–2 of docs/asset-pipeline/ADDRESS-TO-ASSET.md, BATCH mode), built 2026-10-25 from `docs/asset-plans/one-hawthorne-street.md` with the shared kit in `tools/landmark-kit/`.

## Result

Validation **PASS** ("all checks pass"). 3,272 triangles (cap 5,000). Crest 83.9 m = target 83.9 m — measured: DataSF LiDAR peak 83.9 m (crown); main roof = LiDAR majority 72.9 m / median 74.0 m. The 2010 survey post-dates the 2009 topping-out. OSM height 93 m is unsourced.

## Deliverables

- `build_one_hawthorne_street.py` — deterministic build (`blender -b --python build_one_hawthorne_street.py`)
- `one-hawthorne-street.glb`, `one-hawthorne-street.blend`
- `validate_one_hawthorne_street.py` → `validation.json` (`--budget 5000`); `render_one_hawthorne_street.py` → renders
- Renders: `one-hawthorne-street-aerial-night.png`, `one-hawthorne-street-aerial.png`, `one-hawthorne-street-contact-sheet.png`, `one-hawthorne-street-east.png`, `one-hawthorne-street-north.png`, `one-hawthorne-street-south.png`, `one-hawthorne-street-top.png`, `one-hawthorne-street-west.png`
- `REFERENCE.md`

## Contract (from validation.json, fresh-scene re-import)

| | |
|---|---|
| Triangles | 3,272 |
| Dimensions | 64.7939 x 58.3946 x 83.9 m (world-axis bbox) |
| min Z / XY centre offset | 0.0 / (0.0, 0.0) |
| Objects | 2 (one-hawthorne-street_body, one-hawthorne-street_night_glow) |
| Materials | Toy_cream, Toy_glassd, Toy_glassl, Toy_leaf, Toy_leafd, Toy_roofd, Toy_sand_Glow, Toy_stone, Toy_white, Toy_white_Glow |
| Anchor | [-122.3989026, 37.7857768] |

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

Lit lobby/ground windows, scattered warm residential windows, lit garden beds, crown line. (886 glow faces, 886 unobstructed outward).

## Iterations

- Iteration 1 passed validation.

## Gate 3 — approval

Approved by David on 2026-10-26 (renders sent as twelve day/night overview sheets): "approve all".

## Stage 4 — optimize

Shipped as `app/public/sf-assets/landmarks/one-hawthorne-street.glb`, meshopt-compressed with the intake flags of `pipeline/compress-assets.mjs` (`gltfpack -c -km -kn -noq`): **174 KB → 76 KB** (56% smaller). Geometry is unchanged. Kit assets are already one body mesh and one glow mesh, so the Blender cleanup pass and the limited dissolve are skipped, as for the Transbay batch. Gate G3 (three.js GLTFLoader round-trip with MeshoptDecoder, `tools/glb-optimize/g3check`) passes.
