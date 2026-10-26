# 601–605 Market Street — build report

Miniature GLB for SF-SIM, Financial District batch (stages 1–2 of docs/asset-pipeline/ADDRESS-TO-ASSET.md,
BATCH mode), built from `docs/asset-plans/605-market-street.md` with the shared kit in `tools/landmark-kit/`.

## Result

Validation **PASS** ("all checks pass"). 2,192 triangles (batch cap 3,000). Crest 54.3 m = target.

## Deliverables

- `build_605_market_street.py` — deterministic build; `605-market-street.glb`, `605-market-street.blend`
- `validate_605_market_street.py` -> `validation.json` (`--height 54.3 --budget 3000 --anchor -122.4013149,37.7889421`)
- `render_605_market_street.py` -> `605-market-street-{aerial,aerial-night,top,north,east,south,west}.png`, `605-market-street-contact-sheet.png`
- `REFERENCE.md`

## Contract (validation.json, fresh-scene re-import)

| | |
|---|---|
| Triangles | 2,192 (body 1,746, glow 446) |
| Dimensions | 38.3046 x 38.0379 x 54.3 m |
| min Z / XY centre offset | 0.0 / (0.0, 0.0) |
| Objects | 2 |
| Materials | Toy_glassd, Toy_roofd, Toy_sand_Glow, Toy_steel, Toy_stone, Toy_terracotta, Toy_trim |
| Anchor | [-122.4013149, 37.7889421] |
| Glow faces unobstructed | 434 / 446 |

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

Bright shop base, lit attic arches, scattered shaft windows.

## Iterations

- First build passed; renders accepted as a period-typical column (no photo to compare).

## Gate 3 — approval

Approved by David on 2026-10-26 (renders sent as twelve day/night overview sheets): "approve all".

## Stage 4 — optimize

Shipped as `app/public/sf-assets/landmarks/605-market-street.glb`, meshopt-compressed with the intake flags of `pipeline/compress-assets.mjs` (`gltfpack -c -km -kn -noq`): **112 KB → 49 KB** (56% smaller). Geometry is unchanged. Kit assets are already one body mesh and one glow mesh, so the Blender cleanup pass and the limited dissolve are skipped, as for the Transbay batch. Gate G3 (three.js GLTFLoader round-trip with MeshoptDecoder, `tools/glb-optimize/g3check`) passes.
