# Hyatt Regency San Francisco Downtown SOMA — build report

Miniature GLB for SF-SIM, FiDi batch (stages 1–2 of docs/asset-pipeline/ADDRESS-TO-ASSET.md, BATCH mode), built 2026-10-25 from `docs/asset-plans/50-3rd-street.md` with the shared kit in `tools/landmark-kit/`.

## Result

Validation **PASS** ("all checks pass"). 3,570 triangles (FiDi cap 5,000). Crest 114.0 m = target 114.0 m (published).

## Deliverables

- `build_50_3rd_street.py` — deterministic build (`blender -b --python build_50_3rd_street.py`)
- `50-3rd-street.glb`, `50-3rd-street.blend`
- `validate_50_3rd_street.py` → `validation.json`; `render_50_3rd_street.py` → renders
- Renders: `50-3rd-street-{north,east,south,west,top,aerial,aerial-night}.png`, `50-3rd-street-contact-sheet.png`
- `REFERENCE.md`

## Contract (from validation.json, fresh-scene re-import)

| | |
|---|---|
| Triangles | 3,570 (budget 5,000) |
| Dimensions | 86.8477 x 84.8809 x 114.0 m |
| min Z / XY centre offset | 0.0 / (0.0, 0.0) |
| Objects | 2 (50-3rd-street_body, 50-3rd-street_night_glow) |
| Materials | Toy_glass, Toy_glassd, Toy_roofd, Toy_sand, Toy_sand_Glow, Toy_steel, Toy_stone, Toy_trim |
| Anchor | [-122.4030905, 37.7865616] |

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

Lit podium shopfronts, hashed lit hotel windows on the tower and wings, a warm band on the penthouse. Glow is laid as thin outward skins over solid faces (1298 glow faces, 1298 unobstructed outward).

## Iterations

- Iteration 1: 5,926 tris (per-storey punched panes) and a glow-orientation failure where lit panes sat behind the long-face piers.
- Iteration 2: windows redrawn as full-height columns under per-storey spandrel quads (3,570 tris); lit panes moved in front of the piers; height corrected to the published 114 m (the batch facts' 67.2 m LiDAR value belongs to another record; this footprint's LiDAR max is 118.6 m with roof plant).

## Gate 3 — approval

Approved by David on 2026-10-26 (renders sent as twelve day/night overview sheets): "approve all".

## Stage 4 — optimize

Shipped as `app/public/sf-assets/landmarks/50-3rd-street.glb`, meshopt-compressed with the intake flags of `pipeline/compress-assets.mjs` (`gltfpack -c -km -kn -noq`): **193 KB → 74 KB** (62% smaller). Geometry is unchanged. Kit assets are already one body mesh and one glow mesh, so the Blender cleanup pass and the limited dissolve are skipped, as for the Transbay batch. Gate G3 (three.js GLTFLoader round-trip with MeshoptDecoder, `tools/glb-optimize/g3check`) passes.
