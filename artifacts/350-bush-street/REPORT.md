# 350 Bush Street (with the Curb Exchange) — build report

Miniature GLB for SF-SIM, Financial District batch (stages 1–2 of docs/asset-pipeline/ADDRESS-TO-ASSET.md, BATCH mode), built 2026-10-25 from `docs/asset-plans/350-bush-street.md` with the shared kit in `tools/landmark-kit/`.

## Result

Validation **PASS** ("all checks pass"). 4,542 triangles (cap 5,000). Crest 85.0 m = target 85.0 m — ESTIMATED 85 m: 19 storeys (Wikidata, SocketSite, Bisnow) × ~4.26 m + glass crown screen. No published height; no LiDAR (built 2018, after the 2010 survey; the list's 86 m was a neighbour's LiDAR).

## Deliverables

- `build_350_bush_street.py` — deterministic build (`blender -b --python build_350_bush_street.py`)
- `350-bush-street.glb`, `350-bush-street.blend`
- `validate_350_bush_street.py` → `validation.json` (`--budget 5000`); `render_350_bush_street.py` → renders
- Renders: `350-bush-street-aerial-night.png`, `350-bush-street-aerial.png`, `350-bush-street-contact-sheet.png`, `350-bush-street-east.png`, `350-bush-street-north.png`, `350-bush-street-south.png`, `350-bush-street-top.png`, `350-bush-street-west.png`
- `REFERENCE.md`

## Contract (from validation.json, fresh-scene re-import)

| | |
|---|---|
| Triangles | 4,542 |
| Dimensions | 63.5937 x 95.1582 x 85.0 m (world-axis bbox) |
| min Z / XY centre offset | 0.0 / (0.0, 0.0) |
| Objects | 2 (350-bush-street_body, 350-bush-street_night_glow) |
| Materials | Toy_glassd, Toy_glassl, Toy_roofd, Toy_sand_Glow, Toy_steel, Toy_stone, Toy_white, Toy_white_Glow |
| Anchor | [-122.4033004, 37.7913475] |

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

Three lit tall windows in the temple's cella, lit shop windows in the stone wing, scattered office windows above 17 m, crown line. (602 glow faces, 602 unobstructed outward).

## Iterations

- Iteration 1 was 5,050 triangles (over the 5,000 cap); fin spacing widened from 3.0 to 4.2 m → 4,542.

## Gate 3 — approval

Approved by David on 2026-10-26 (renders sent as twelve day/night overview sheets): "approve all".

## Stage 4 — optimize

Shipped as `app/public/sf-assets/landmarks/350-bush-street.glb`, meshopt-compressed with the intake flags of `pipeline/compress-assets.mjs` (`gltfpack -c -km -kn -noq`): **228 KB → 105 KB** (54% smaller). Geometry is unchanged. Kit assets are already one body mesh and one glow mesh, so the Blender cleanup pass and the limited dissolve are skipped, as for the Transbay batch. Gate G3 (three.js GLTFLoader round-trip with MeshoptDecoder, `tools/glb-optimize/g3check`) passes.
