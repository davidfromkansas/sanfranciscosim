# Old Chronicle Building (Ritz-Carlton Club and Residences) — build report

Miniature GLB for SF-SIM, FiDi batch (stages 1–2 of docs/asset-pipeline/ADDRESS-TO-ASSET.md, BATCH mode), built 2026-10-25 from `docs/asset-plans/690-market-street.md` with the shared kit in `tools/landmark-kit/`.

## Result

Validation **PASS** ("all checks pass"). 3,938 triangles (FiDi cap 5,000). Crest 95.0 m = target 95.0 m (published).

## Deliverables

- `build_690_market_street.py` — deterministic build (`blender -b --python build_690_market_street.py`)
- `690-market-street.glb`, `690-market-street.blend`
- `validate_690_market_street.py` → `validation.json`; `render_690_market_street.py` → renders
- Renders: `690-market-street-{north,east,south,west,top,aerial,aerial-night}.png`, `690-market-street-contact-sheet.png`
- `REFERENCE.md`

## Contract (from validation.json, fresh-scene re-import)

| | |
|---|---|
| Triangles | 3,938 (budget 5,000) |
| Dimensions | 47.1894 x 46.4498 x 95.0 m |
| min Z / XY centre offset | 0.0 / (0.0, 0.0) |
| Objects | 2 (690-market-street_body, 690-market-street_night_glow) |
| Materials | Toy_brick, Toy_glassd, Toy_glassl, Toy_ink, Toy_roofd, Toy_rust, Toy_sand, Toy_sand_Glow, Toy_steel, Toy_stone, Toy_terracotta, Toy_verdigris |
| Anchor | [-122.4032006, 37.7882605] |

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

Lit shopfronts, a lit round-arched arcade, hashed lit windows on the brick block and the addition tiers, a warm line under the top eave. Glow is laid as thin outward skins over solid faces (719 glow faces, 719 unobstructed outward).

## Iterations

- Iteration 1: built from the Commons photo; brick block, arcade and tiered addition read. No changes needed.

## Gate 3 — approval

Approved by David on 2026-10-26 (renders sent as twelve day/night overview sheets): "approve all".

## Stage 4 — optimize

Shipped as `app/public/sf-assets/landmarks/690-market-street.glb`, meshopt-compressed with the intake flags of `pipeline/compress-assets.mjs` (`gltfpack -c -km -kn -noq`): **209 KB → 95 KB** (54% smaller). Geometry is unchanged. Kit assets are already one body mesh and one glow mesh, so the Blender cleanup pass and the limited dissolve are skipped, as for the Transbay batch. Gate G3 (three.js GLTFLoader round-trip with MeshoptDecoder, `tools/glb-optimize/g3check`) passes.
