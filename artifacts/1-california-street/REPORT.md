# One California Street — build report

Miniature GLB for SF-SIM, FiDi batch (stages 1–2 of docs/asset-pipeline/ADDRESS-TO-ASSET.md, BATCH mode), built 2026-10-25 from `docs/asset-plans/1-california-street.md` with the shared kit in `tools/landmark-kit/`.

## Result

Validation **PASS** ("all checks pass"). 2,762 triangles (FiDi cap 5,000). Crest 133.5 m = target 133.5 m (published).

## Deliverables

- `build_1_california_street.py` — deterministic build (`blender -b --python build_1_california_street.py`)
- `1-california-street.glb`, `1-california-street.blend`
- `validate_1_california_street.py` → `validation.json`; `render_1_california_street.py` → renders
- Renders: `1-california-street-{north,east,south,west,top,aerial,aerial-night}.png`, `1-california-street-contact-sheet.png`
- `REFERENCE.md`

## Contract (from validation.json, fresh-scene re-import)

| | |
|---|---|
| Triangles | 2,762 (budget 5,000) |
| Dimensions | 54.3742 x 54.8593 x 133.5 m |
| min Z / XY centre offset | 0.0 / (0.0, 0.0) |
| Objects | 2 (1-california-street_body, 1-california-street_night_glow) |
| Materials | Toy_glass, Toy_glassd, Toy_navy, Toy_navy_Glow, Toy_red, Toy_red_Glow, Toy_roofd, Toy_sand_Glow, Toy_steel, Toy_stone, Toy_white, Toy_white_Glow |
| Anchor | [-122.3971792, 37.7932326] |

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

Lit lobby, hashed lit panes between the piers, a white line under the crown, and the red/navy sign panels glow. Glow is laid as thin outward skins over solid faces (818 glow faces, 818 unobstructed outward).

## Iterations

- Iteration 1: the crown was a solid prism that buried the roof deck, and the east sign sat on half the east face.
- Iteration 2: crown made a hollow ring around a sunken deck and plant; east sign spans the whole east face.

## Gate 3 — approval

Approved by David on 2026-10-26 (renders sent as twelve day/night overview sheets): "approve all".

## Stage 4 — optimize

Shipped as `app/public/sf-assets/landmarks/1-california-street.glb`, meshopt-compressed with the intake flags of `pipeline/compress-assets.mjs` (`gltfpack -c -km -kn -noq`): **154 KB → 67 KB** (57% smaller). Geometry is unchanged. Kit assets are already one body mesh and one glow mesh, so the Blender cleanup pass and the limited dissolve are skipped, as for the Transbay batch. Gate G3 (three.js GLTFLoader round-trip with MeshoptDecoder, `tools/glb-optimize/g3check`) passes.
