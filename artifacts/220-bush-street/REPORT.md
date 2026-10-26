# Mills Tower (220 Bush Street) — build report

Miniature GLB for SF-SIM, Financial District batch (stages 1–2 of docs/asset-pipeline/ADDRESS-TO-ASSET.md, BATCH mode), built 2026-10-25 from `docs/asset-plans/220-bush-street.md` with the shared kit in `tools/landmark-kit/`.

## Result

Validation **PASS** ("all checks pass"). 2,226 triangles (cap 5,000). Crest 92 m = target 92 m — published (Wikipedia infobox roof 92 m); LiDAR roof 93.1 m majority.

## Deliverables

- `build_220_bush_street.py` — deterministic build (`blender -b --python build_220_bush_street.py`)
- `220-bush-street.glb`, `220-bush-street.blend`
- `validate_220_bush_street.py` → `validation.json`; `render_220_bush_street.py` → renders below
- Renders: `220-bush-street-aerial-night.png`, `220-bush-street-aerial.png`, `220-bush-street-contact-sheet.png`, `220-bush-street-east.png`, `220-bush-street-north.png`, `220-bush-street-south.png`, `220-bush-street-top.png`, `220-bush-street-west.png`
- `REFERENCE.md` (sources, dimensions, cues, uncertainties)

## Contract (from validation.json, fresh-scene re-import)

| | |
|---|---|
| Triangles | 2,226 (budget passed to the validator: 5,000) |
| Dimensions | 25.6872 x 50.3996 x 92 m (world-axis bbox, incl. apron) |
| min Z / XY centre offset | 0.0 / (0.0, 0.0) |
| Objects | 2 (220-bush-street_body, 220-bush-street_night_glow) |
| Materials | Toy_cream, Toy_glassd, Toy_leaf, Toy_leafd, Toy_roofd, Toy_rust, Toy_sand_Glow, Toy_steel, Toy_stone, Toy_terracotta |
| Anchor | [-122.4013027, 37.7914191] |
| Glow faces unobstructed outward | 658 / 658 |

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

Lit storefronts on Bush, ~28% lit strips, lit attic arches and a warm penthouse band.

## Iterations

- v1 passed all checks (2,226 tris); render reviewed against the photo.

## Gate 3 — approval

Approved by David on 2026-10-26 (renders sent as twelve day/night overview sheets): "approve all".

## Stage 4 — optimize

Shipped as `app/public/sf-assets/landmarks/220-bush-street.glb`, meshopt-compressed with the intake flags of `pipeline/compress-assets.mjs` (`gltfpack -c -km -kn -noq`): **110 KB → 52 KB** (52% smaller). Geometry is unchanged. Kit assets are already one body mesh and one glow mesh, so the Blender cleanup pass and the limited dissolve are skipped, as for the Transbay batch. Gate G3 (three.js GLTFLoader round-trip with MeshoptDecoder, `tools/glb-optimize/g3check`) passes.
