# 735 Market Street — build report

Miniature GLB for SF-SIM, Financial District batch (stages 1–2 of docs/asset-pipeline/ADDRESS-TO-ASSET.md, BATCH mode), built 2026-10-25 from `docs/asset-plans/735-market-street.md` with the shared kit in `tools/landmark-kit/`.

## Result

Validation **PASS** ("all checks pass"). 1,042 triangles (cap 3,000). Crest 27.4 m = target 27.4 m — DataSF LiDAR roof (majority 27.44 m; OSM height 28 m). The list's 77.4 m was the ring's max, a neighbour.

## Deliverables

- `build_735_market_street.py` — deterministic build (`blender -b --python build_735_market_street.py`)
- `735-market-street.glb`, `735-market-street.blend`
- `validate_735_market_street.py` → `validation.json`; `render_735_market_street.py` → renders below
- Renders: `735-market-street-aerial-night.png`, `735-market-street-aerial.png`, `735-market-street-contact-sheet.png`, `735-market-street-east.png`, `735-market-street-north.png`, `735-market-street-south.png`, `735-market-street-top.png`, `735-market-street-west.png`
- `REFERENCE.md` (sources, dimensions, cues, uncertainties)

## Contract (from validation.json, fresh-scene re-import)

| | |
|---|---|
| Triangles | 1,042 (budget passed to the validator: 3,000) |
| Dimensions | 57.272 x 56.9981 x 27.4 m (world-axis bbox, incl. apron) |
| min Z / XY centre offset | 0.0 / (0.0, 0.0) |
| Objects | 2 (735-market-street_body, 735-market-street_night_glow) |
| Materials | Toy_cream, Toy_glassd, Toy_leaf, Toy_leafd, Toy_roofd, Toy_rust, Toy_sand, Toy_sand_Glow, Toy_steel, Toy_stone |
| Anchor | [-122.4041285, 37.7865717] |
| Glow faces unobstructed outward | 78 / 78 |

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

Shopfronts lit, ~35% windows, a lit skylight.

## Iterations

- v1 passed all checks (1,042 tris).

## Gate 3 — approval

Approved by David on 2026-10-26 (renders sent as twelve day/night overview sheets): "approve all".

## Stage 4 — optimize

Shipped as `app/public/sf-assets/landmarks/735-market-street.glb`, meshopt-compressed with the intake flags of `pipeline/compress-assets.mjs` (`gltfpack -c -km -kn -noq`): **60 KB → 32 KB** (48% smaller). Geometry is unchanged. Kit assets are already one body mesh and one glow mesh, so the Blender cleanup pass and the limited dissolve are skipped, as for the Transbay batch. Gate G3 (three.js GLTFLoader round-trip with MeshoptDecoder, `tools/glb-optimize/g3check`) passes.
