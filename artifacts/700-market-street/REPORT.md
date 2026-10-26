# Mutual Savings Bank Building — build report

Miniature GLB for SF-SIM, Financial District batch (stages 1–2 of docs/asset-pipeline/ADDRESS-TO-ASSET.md,
BATCH mode), built from `docs/asset-plans/700-market-street.md` with the shared kit in `tools/landmark-kit/`.

## Result

Validation **PASS** ("all checks pass"). 1,596 triangles (batch cap 3,000). Crest 57.9 m = target.

## Deliverables

- `build_700_market_street.py` — deterministic build; `700-market-street.glb`, `700-market-street.blend`
- `validate_700_market_street.py` -> `validation.json` (`--height 57.9 --budget 3000 --anchor -122.4038192,37.7877278`)
- `render_700_market_street.py` -> `700-market-street-{aerial,aerial-night,top,north,east,south,west}.png`, `700-market-street-contact-sheet.png`
- `REFERENCE.md`

## Contract (validation.json, fresh-scene re-import)

| | |
|---|---|
| Triangles | 1,596 (body 1,270, glow 326) |
| Dimensions | 30.2498 x 32.5953 x 57.9 m |
| min Z / XY centre offset | 0.0 / (0.0, 0.0) |
| Objects | 2 |
| Materials | Toy_concrete, Toy_coral, Toy_glassd, Toy_roofd, Toy_sand_Glow, Toy_stone, Toy_trim, Toy_verdigris |
| Anchor | [-122.4038192, 37.7877278] |
| Glow faces unobstructed | 326 / 326 |

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

Lit base arches and attic arches, scattered shaft windows, lit dormer windows.

## Iterations

- Validate failed on 10 degenerate triangles in the bevelled `plinth` on this small 5-gon; replaced by an unbevelled sidewalk prism.
- Walls changed from cream `stone` to grey `concrete` to match the photo's grey granite/sandstone.

## Gate 3 — approval

Approved by David on 2026-10-26 (renders sent as twelve day/night overview sheets): "approve all".

## Stage 4 — optimize

Shipped as `app/public/sf-assets/landmarks/700-market-street.glb`, meshopt-compressed with the intake flags of `pipeline/compress-assets.mjs` (`gltfpack -c -km -kn -noq`): **84 KB → 40 KB** (52% smaller). Geometry is unchanged. Kit assets are already one body mesh and one glow mesh, so the Blender cleanup pass and the limited dissolve are skipped, as for the Transbay batch. Gate G3 (three.js GLTFLoader round-trip with MeshoptDecoder, `tools/glb-optimize/g3check`) passes.
