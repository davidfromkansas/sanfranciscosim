# 180 Montgomery Street (Bank of the West Building) — build report

Miniature GLB for SF-SIM, Financial District batch (stages 1–2 of docs/asset-pipeline/ADDRESS-TO-ASSET.md, BATCH mode), built 2026-10-25 from `docs/asset-plans/180-montgomery-street.md` with the shared kit in `tools/landmark-kit/`.

## Result

Validation **PASS** ("all checks pass"). 2,848 triangles (cap 5,000). Crest 109.8 m = target 109.8 m — published 109.8 m (CTBUH via the Wikipedia list; LiDAR roof majority 109.5 m, median 104.2 m).

## Deliverables

- `build_180_montgomery_street.py` — deterministic build (`blender -b --python build_180_montgomery_street.py`)
- `180-montgomery-street.glb`, `180-montgomery-street.blend`
- `validate_180_montgomery_street.py` → `validation.json` (`--budget 5000`); `render_180_montgomery_street.py` → renders
- Renders: `180-montgomery-street-aerial-night.png`, `180-montgomery-street-aerial.png`, `180-montgomery-street-contact-sheet.png`, `180-montgomery-street-east.png`, `180-montgomery-street-north.png`, `180-montgomery-street-south.png`, `180-montgomery-street-top.png`, `180-montgomery-street-west.png`
- `REFERENCE.md`

## Contract (from validation.json, fresh-scene re-import)

| | |
|---|---|
| Triangles | 2,848 |
| Dimensions | 53.325 x 49.3411 x 109.8 m (world-axis bbox) |
| min Z / XY centre offset | 0.0 / (0.0, 0.0) |
| Objects | 2 (180-montgomery-street_body, 180-montgomery-street_night_glow) |
| Materials | Toy_concrete, Toy_glassd, Toy_roofd, Toy_sand_Glow, Toy_steel, Toy_stone, Toy_white_Glow |
| Anchor | [-122.4020113, 37.790747] |

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

Lit lobby ring, scattered lit ribbon windows laid just proud of the spandrels, crown line on the parapet. (616 glow faces, 616 unobstructed outward).

## Iterations

- Iteration 1 passed validation and the renders match the photo's horizontal grid; no change.

## Gate 3 — approval

Approved by David on 2026-10-26 (renders sent as twelve day/night overview sheets): "approve all".

## Stage 4 — optimize

Shipped as `app/public/sf-assets/landmarks/180-montgomery-street.glb`, meshopt-compressed with the intake flags of `pipeline/compress-assets.mjs` (`gltfpack -c -km -kn -noq`): **143 KB → 67 KB** (53% smaller). Geometry is unchanged. Kit assets are already one body mesh and one glow mesh, so the Blender cleanup pass and the limited dissolve are skipped, as for the Transbay batch. Gate G3 (three.js GLTFLoader round-trip with MeshoptDecoder, `tools/glb-optimize/g3check`) passes.
