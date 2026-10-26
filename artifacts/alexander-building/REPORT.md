# Alexander Building — build report

Miniature GLB for SF-SIM, Financial District batch (stages 1–2 of
docs/asset-pipeline/ADDRESS-TO-ASSET.md, BATCH mode), built 2026-10-25 from
`docs/asset-plans/alexander-building.md` with the shared kit in `tools/landmark-kit/`.

## Result

Validation **PASS** ("all checks pass", run with `--budget 5000`). 2,426 triangles.
Crest 60.13 m = target height — DataSF 2010 LiDAR median 60.13 m of ring 201006.0009912 (measured; majority 59.6). The facts file's 76.6 m and the ring max 93 m look like a taller neighbour's wall and are not modelled.

## Deliverables

- `build_alexander_building.py` — deterministic build (`blender -b --python build_alexander_building.py`)
- `alexander-building.glb`, `alexander-building.blend`
- `validate_alexander_building.py` → `validation.json`; `render_alexander_building.py` → renders below
- Renders: `alexander-building-aerial-night.png`, `alexander-building-aerial.png`, `alexander-building-contact-sheet.png`, `alexander-building-east.png`, `alexander-building-north.png`, `alexander-building-south.png`, `alexander-building-top.png`, `alexander-building-west.png`
- `REFERENCE.md` (sources, dimensions, cues, uncertainties)

## Contract (from validation.json, fresh-scene re-import)

| | |
|---|---|
| Triangles | 2,426 |
| Dimensions | 24.9303 x 29.3465 x 60.13 m (world-axis bbox) |
| min Z / XY centre offset | 0.0 / (0.0, 0.0) |
| Objects | 2 |
| Materials | Toy_concrete, Toy_cream, Toy_glassd, Toy_roofd, Toy_sand_Glow, Toy_stone, Toy_terracotta |
| Anchor | [-122.4025768, 37.7907411] |

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

- `tk.rect(17.1, 22.4)` on yaw 81.1°; `Toy_stone` base 0–8.4 m, street-side panes and lit shopfronts.
- 9–55.8 m `Toy_terracotta` shaft, 12 storeys of 3.9 m, panes every 2.15 m, `Toy_cream` piers 0.55 m proud.
- Top storey with arched panes; cream cornice and parapet; pinnacles to 60.13 m; stair bulkhead.

All materials are flat `Toy_*` (roughness 0.85, no textures, no alpha). Off-palette: `Toy_terracotta`, `Toy_glassd`, `Toy_concrete`.

## Night state

Lit shopfronts and scattered office windows. Glow materials: `Toy_sand_Glow`; all laid as thin outward skins over solid faces (282 of 282 glow faces unobstructed outward).

## Iterations



## Gate 3 — approval

Pending: renders sent to David.
