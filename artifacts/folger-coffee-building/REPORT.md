# Folger Coffee Company Building — build report

Miniature GLB for SF-SIM, Financial District batch (stages 1–2 of
docs/asset-pipeline/ADDRESS-TO-ASSET.md, BATCH mode), built 2026-10-25 from
`docs/asset-plans/folger-coffee-building.md` with the shared kit in `tools/landmark-kit/`.

## Result

Validation **PASS** ("all checks pass", run with `--budget 3000`). 2,152 triangles.
Crest 26.74 m = target height — facts-file LiDAR peak 26.74 m (roof bulkhead); main roof 24.6 m = DataSF ring 201006.0001608 majority (measured).

## Deliverables

- `build_folger_coffee_building.py` — deterministic build (`blender -b --python build_folger_coffee_building.py`)
- `folger-coffee-building.glb`, `folger-coffee-building.blend`
- `validate_folger_coffee_building.py` → `validation.json`; `render_folger_coffee_building.py` → renders below
- Renders: `folger-coffee-building-aerial-night.png`, `folger-coffee-building-aerial.png`, `folger-coffee-building-contact-sheet.png`, `folger-coffee-building-east.png`, `folger-coffee-building-north.png`, `folger-coffee-building-south.png`, `folger-coffee-building-top.png`, `folger-coffee-building-west.png`
- `REFERENCE.md` (sources, dimensions, cues, uncertainties)

## Contract (from validation.json, fresh-scene re-import)

| | |
|---|---|
| Triangles | 2,152 |
| Dimensions | 57.558 x 57.4148 x 26.74 m (world-axis bbox) |
| min Z / XY centre offset | 0.0 / (0.0, 0.0) |
| Objects | 2 |
| Materials | Toy_brick, Toy_concrete, Toy_glassd, Toy_leaf, Toy_roofd, Toy_rust, Toy_sand_Glow, Toy_steel, Toy_stone |
| Anchor | [-122.3925976, 37.7909315] |

| Check | Result |
|---|---|
| Crest = target height | PASS |
| Plausible metre dimensions | PASS |
| Base at Z 0 | PASS |
| Centred in XY | PASS |
| Triangle budget (batch cap) | PASS |
| No image textures | PASS |
| No transparency | PASS |
| Flat `Toy_*` materials | PASS |
| Has night glow | PASS |
| No cameras / lights | PASS |
| No animation / skin / constraints | PASS |
| Transforms applied | PASS |
| No negative scales | PASS |
| Normals outward (signed volume) | PASS |
| Normals outward (ray residual) | PASS |
| Glow skins face outward | PASS |
| No degenerate geometry | PASS |
| No unexpected objects | PASS |

## Geometry and materials

- `tk.rect(42.9, 28.4)` on yaw from 45.4°, `Toy_brick` to 23.4 m.
- Ground arches (4.3 m bays) with lit shopfronts; stone band course.
- `Toy_rust` brick piers 6.3–19.6 m; three storeys of panes; sill band.
- Top arcade of round-headed panes (2.15 m), sparse lit; corbel cornice + parapet; deck, bulkhead to 26.74 m, low plant.
- Five clipped street trees on Howard.

All materials are flat `Toy_*` (roughness 0.85, no textures, no alpha). Off-palette: `Toy_glassd`, `Toy_concrete`, `Toy_leaf`.

## Night state

Lit arched shopfronts, scattered lit office windows and top-arcade windows. Glow materials: `Toy_sand_Glow`; all laid as thin outward skins over solid faces (315 of 320 glow faces unobstructed outward).

## Iterations



## Gate 3 — approval

Approved by David on 2026-10-26 (renders sent as twelve day/night overview sheets): "approve all".

## Stage 4 — optimize

Shipped as `app/public/sf-assets/landmarks/folger-coffee-building.glb`, meshopt-compressed with the intake flags of `pipeline/compress-assets.mjs` (`gltfpack -c -km -kn -noq`): **107 KB → 50 KB** (53% smaller). Geometry is unchanged. Kit assets are already one body mesh and one glow mesh, so the Blender cleanup pass and the limited dissolve are skipped, as for the Transbay batch. Gate G3 (three.js GLTFLoader round-trip with MeshoptDecoder, `tools/glb-optimize/g3check`) passes.
