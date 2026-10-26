# Mechanics' Institute — build report

Miniature GLB for SF-SIM, Financial District batch (stages 1–2 of docs/asset-pipeline/ADDRESS-TO-ASSET.md,
BATCH mode), built from `docs/asset-plans/mechanics-institute.md` with the shared kit in `tools/landmark-kit/`.

## Result

Validation **PASS** ("all checks pass"). 1,882 triangles (batch cap 3,000). Crest 43.0 m = target.

## Deliverables

- `build_mechanics_institute.py` — deterministic build; `mechanics-institute.glb`, `mechanics-institute.blend`
- `validate_mechanics_institute.py` -> `validation.json` (`--height 43.0 --budget 3000 --anchor -122.4030408,37.7887368`)
- `render_mechanics_institute.py` -> `mechanics-institute-{aerial,aerial-night,top,north,east,south,west}.png`, `mechanics-institute-contact-sheet.png`
- `REFERENCE.md`

## Contract (validation.json, fresh-scene re-import)

| | |
|---|---|
| Triangles | 1,882 (body 1,516, glow 366) |
| Dimensions | 31.454 x 41.8278 x 43.0 m |
| min Z / XY centre offset | 0.0 / (0.0, 0.0) |
| Objects | 2 |
| Materials | Toy_concrete, Toy_glassd, Toy_ink, Toy_roofd, Toy_sand_Glow, Toy_steel, Toy_stone, Toy_trim |
| Anchor | [-122.4030408, 37.7887368] |
| Glow faces unobstructed | 360 / 366 |

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

Lit base arches and library arcade, lit portal fanlight, scattered office windows.

## Iterations

- First build passed; renders accepted.

## Gate 3 — approval

Approved by David on 2026-10-26 (renders sent as twelve day/night overview sheets): "approve all".

## Stage 4 — optimize

Shipped as `app/public/sf-assets/landmarks/mechanics-institute.glb`, meshopt-compressed with the intake flags of `pipeline/compress-assets.mjs` (`gltfpack -c -km -kn -noq`): **96 KB → 46 KB** (53% smaller). Geometry is unchanged. Kit assets are already one body mesh and one glow mesh, so the Blender cleanup pass and the limited dissolve are skipped, as for the Transbay batch. Gate G3 (three.js GLTFLoader round-trip with MeshoptDecoder, `tools/glb-optimize/g3check`) passes.
