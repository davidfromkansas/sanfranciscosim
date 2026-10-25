# Matson Building (215 Market Street) — build report

Miniature GLB for SF-SIM, Transbay batch (stages 1–2 of
docs/asset-pipeline/ADDRESS-TO-ASSET.md, BATCH mode), built 2026-10-25 from
`docs/asset-plans/matson-building.md` with the shared kit in `tools/landmark-kit/`.

## Result

Validation **PASS** ("all checks pass"). 4,114 triangles (budget 27,000 kit cap;
plan cap 12,000). Crest 73.0 m = target height 73.0 m — ESTIMATED (16 storeys scaled from the PG&E twin; no published or measurable height).

## Deliverables

- `build_matson_building.py` — deterministic build (`blender -b --python build_matson_building.py`)
- `matson-building.glb`, `matson-building.blend`
- `validate_matson_building.py` → `validation.json`; `render_matson_building.py` → renders below
- Renders: `matson-building-aerial-night.png`, `matson-building-aerial.png`, `matson-building-contact-sheet.png`, `matson-building-east.png`, `matson-building-north.png`, `matson-building-south.png`, `matson-building-top.png`, `matson-building-west.png`
- `REFERENCE.md` (sources, dimensions, cues, uncertainties)

## Contract (from validation.json, fresh-scene re-import)

| | |
|---|---|
| Triangles | 4,114 |
| Dimensions | 68.4374 x 68.4571 x 73.0 m (world-axis bbox) |
| min Z / XY centre offset | 0.0 / (0.0, 0.0) |
| Objects | 2 (matson-building_body, matson-building_night_glow) |
| Materials | Toy_cream, Toy_glassd, Toy_roofd, Toy_sand_Glow, Toy_steel, Toy_stone, Toy_terracotta |
| Anchor | [-122.396508, 37.792655] |

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

## Geometry and materials

- 43.5 x 41.5 m plan at yaw −45.4°: terracotta arcaded base 0–11 m (3.0 m arches at 4.6 m), cream cornice.
- Grand entrance: cream portal frame proud of the Market (NW) face to 12.5 m with a 6.2 m arch.
- Cream punched shaft 12–62 m; terracotta band and arched top storey 62.4–68 m; cream cornice 68–70 m (1.6 m projection); terracotta balustrade to 71.4 m.
- Roof: dark deck at 70 m, cream arcaded penthouse 10 x 18 m set toward Market with a cornice to 73.0 m, small plant cluster.

All materials are flat `Toy_*` (roughness 0.85, no textures, no alpha); off-palette tones
are documented in REFERENCE.md.

## Night state

Lit arcade and portal arch, lit top-storey arches and penthouse arches, scattered `Toy_sand_Glow` windows. Glow is laid as thin outward skins over solid faces
(1092 glow faces, all unobstructed outward).

## Iterations

- Iteration 1 (lead draft): the entrance portal was on the NE (Main St) face and its arch faced inward (coplanar with the portal box, invisible). Moved it to the Market (NW) face and fixed the arch winding; added a lit arch.
- Added the arcaded rooftop penthouse seen in the Commons photo; the crest is now the penthouse cornice at 73.0 m instead of a plant cluster.

## Gate 3 — approval

Approved by David on 2026-10-25 (contact sheets sent in four batches of five): "approve all".

## Stage 4 — optimize

Shipped as `app/public/sf-assets/landmarks/matson-building.glb`, meshopt-compressed with the intake flags of `pipeline/compress-assets.mjs` (`gltfpack -c -km -kn -noq`): **208 KB → 85 KB** (59% smaller). Geometry is unchanged. The kit merges every landmark into one body mesh and one glow mesh, so the Phase B cleanup in `tools/glb-optimize/` finds nothing to join or weld; a trial run saved 0 triangles and grew the file 1–5%, so it was not applied. The limited dissolve is skipped as GLB-OPTIMIZE-PROMPT §3 step 3 requires for assets with ring bands and parapets. Gate G3 (three.js GLTFLoader round-trip with MeshoptDecoder, `tools/glb-optimize/g3check`) passes.
