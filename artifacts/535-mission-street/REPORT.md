# 535 Mission Street — build report

Miniature GLB for SF-SIM, Financial District batch (stages 1–2 of docs/asset-pipeline/ADDRESS-TO-ASSET.md, BATCH mode), built 2026-10-25 from `docs/asset-plans/535-mission-street.md` with the shared kit in `tools/landmark-kit/`.

## Result

Validation **PASS** ("all checks pass"). 2,282 triangles (cap 5,000). Crest 115 m = target 115 m — published (Wikipedia/Emporis roof 378 ft); DataSF LiDAR ring 112.2 m majority, 115.7 m max agrees.

## Deliverables

- `build_535_mission_street.py` — deterministic build (`blender -b --python build_535_mission_street.py`)
- `535-mission-street.glb`, `535-mission-street.blend`
- `validate_535_mission_street.py` → `validation.json`; `render_535_mission_street.py` → renders below
- Renders: `535-mission-street-aerial-night.png`, `535-mission-street-aerial.png`, `535-mission-street-contact-sheet.png`, `535-mission-street-east.png`, `535-mission-street-north.png`, `535-mission-street-south.png`, `535-mission-street-top.png`, `535-mission-street-west.png`
- `REFERENCE.md` (sources, dimensions, cues, uncertainties)

## Contract (from validation.json, fresh-scene re-import)

| | |
|---|---|
| Triangles | 2,282 (budget passed to the validator: 5,000) |
| Dimensions | 60.142 x 58.6236 x 115 m (world-axis bbox, incl. apron) |
| min Z / XY centre offset | 0.0 / (0.0, 0.0) |
| Objects | 2 (535-mission-street_body, 535-mission-street_night_glow) |
| Materials | Toy_glass, Toy_glassl, Toy_leaf, Toy_roofd, Toy_rust, Toy_sand_Glow, Toy_steel, Toy_stone, Toy_white_Glow |
| Anchor | [-122.398156, 37.7888721] |
| Glow faces unobstructed outward | 470 / 474 |

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

Warm lobby band, scattered `sand_Glow` office panes on every face (28% of bays), a white crown line round the parapet.

## Iterations

- v1: dark `glass` skin read too heavy against the photo's sky-blue reflection; lit panes behind the facet failed the glow check (388/474).
- v2: skin switched to `glassl` with `glass` bands and facet; panes moved 0.24 m out. All checks pass.

## Gate 3 — approval

Approved by David on 2026-10-26 (renders sent as twelve day/night overview sheets): "approve all".

## Stage 4 — optimize

Shipped as `app/public/sf-assets/landmarks/535-mission-street.glb`, meshopt-compressed with the intake flags of `pipeline/compress-assets.mjs` (`gltfpack -c -km -kn -noq`): **121 KB → 60 KB** (50% smaller). Geometry is unchanged. Kit assets are already one body mesh and one glow mesh, so the Blender cleanup pass and the limited dissolve are skipped, as for the Transbay batch. Gate G3 (three.js GLTFLoader round-trip with MeshoptDecoder, `tools/glb-optimize/g3check`) passes.
