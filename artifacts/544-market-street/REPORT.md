# Flatiron Building (540–544 Market Street) — build report

Miniature GLB for SF-SIM, Financial District batch (stages 1–2 of docs/asset-pipeline/ADDRESS-TO-ASSET.md, BATCH mode), built 2026-10-25 from `docs/asset-plans/544-market-street.md` with the shared kit in `tools/landmark-kit/`.

## Result

Validation **PASS** ("all checks pass"). 1,358 triangles (cap 3,000). Crest 36.6 m = target 36.6 m — published (Wikipedia/Emporis roof 36.58 m / 120 ft); LiDAR roof 38.1 m majority.

## Deliverables

- `build_544_market_street.py` — deterministic build (`blender -b --python build_544_market_street.py`)
- `544-market-street.glb`, `544-market-street.blend`
- `validate_544_market_street.py` → `validation.json`; `render_544_market_street.py` → renders below
- Renders: `544-market-street-aerial-night.png`, `544-market-street-aerial.png`, `544-market-street-contact-sheet.png`, `544-market-street-east.png`, `544-market-street-north.png`, `544-market-street-south.png`, `544-market-street-top.png`, `544-market-street-west.png`
- `REFERENCE.md` (sources, dimensions, cues, uncertainties)

## Contract (from validation.json, fresh-scene re-import)

| | |
|---|---|
| Triangles | 1,358 (budget passed to the validator: 3,000) |
| Dimensions | 27.2539 x 32.456 x 36.6 m (world-axis bbox, incl. apron) |
| min Z / XY centre offset | 0.0 / (0.0, 0.0) |
| Objects | 2 (544-market-street_body, 544-market-street_night_glow) |
| Materials | Toy_concrete, Toy_cream, Toy_glassd, Toy_leaf, Toy_roofd, Toy_rust, Toy_sand_Glow, Toy_steel, Toy_stone, Toy_terracotta |
| Anchor | [-122.400786, 37.7900167] |
| Glow faces unobstructed outward | 228 / 228 |

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

Glowing storefronts on Market and Sutter, ~30% lit office panes, lit top-floor arches and prow bays.

## Iterations

- v1: 11 lit panes hidden behind piers (glow check 233/244) — piers realigned to the window gaps; all checks pass.

## Gate 3 — approval

Approved by David on 2026-10-26 (renders sent as twelve day/night overview sheets): "approve all".

## Stage 4 — optimize

Shipped as `app/public/sf-assets/landmarks/544-market-street.glb`, meshopt-compressed with the intake flags of `pipeline/compress-assets.mjs` (`gltfpack -c -km -kn -noq`): **76 KB → 36 KB** (53% smaller). Geometry is unchanged. Kit assets are already one body mesh and one glow mesh, so the Blender cleanup pass and the limited dissolve are skipped, as for the Transbay batch. Gate G3 (three.js GLTFLoader round-trip with MeshoptDecoder, `tools/glb-optimize/g3check`) passes.
