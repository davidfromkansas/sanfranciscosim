# Hobart Building — build report

Miniature GLB for SF-SIM, FiDi batch (stages 1–2 of docs/asset-pipeline/ADDRESS-TO-ASSET.md, BATCH mode), built 2026-10-25 from `docs/asset-plans/582-market-street.md` with the shared kit in `tools/landmark-kit/`.

## Result

Validation **PASS** ("all checks pass"). 2,156 triangles (FiDi cap 5,000). Crest 87.0 m = target 87.0 m (published).

## Deliverables

- `build_582_market_street.py` — deterministic build (`blender -b --python build_582_market_street.py`)
- `582-market-street.glb`, `582-market-street.blend`
- `validate_582_market_street.py` → `validation.json`; `render_582_market_street.py` → renders
- Renders: `582-market-street-{north,east,south,west,top,aerial,aerial-night}.png`, `582-market-street-contact-sheet.png`
- `REFERENCE.md`

## Contract (from validation.json, fresh-scene re-import)

| | |
|---|---|
| Triangles | 2,156 (budget 5,000) |
| Dimensions | 27.5354 x 55.828 x 87.0 m |
| min Z / XY centre offset | 0.0 / (0.0, 0.0) |
| Objects | 2 (582-market-street_body, 582-market-street_night_glow) |
| Materials | Toy_cream, Toy_glassd, Toy_gold, Toy_ink, Toy_roofd, Toy_sand_Glow, Toy_stone, Toy_terracotta, Toy_verdigris |
| Anchor | [-122.4016363, 37.7894660] |

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

Lit shopfronts, a hashed scatter of lit windows on every windowed face, lit arched top storey, a warm line under the cornice; the blank west flank stays dark. Glow is laid as thin outward skins over solid faces (497 glow faces, 497 unobstructed outward).

## Iterations

- Iteration 1: the upper tower outline overhung the slab's east party line and the sign panel faced inward (invisible). Refitted the tower to the front part (flush with Market, east end on the party line) and flipped the sign normal to the west.
- Iteration 2: renders checked against the Commons photo; round end, cornice and blank flank read. Left as is.

## Gate 3 — approval

Pending: renders sent to David.
