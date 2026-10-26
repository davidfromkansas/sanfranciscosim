# Matson Building Annex — build report

Miniature GLB for SF-SIM, Financial District batch (stages 1–2 of
docs/asset-pipeline/ADDRESS-TO-ASSET.md, BATCH mode), built 2026-10-25 from
`docs/asset-plans/matson-building-annex.md` with the shared kit in `tools/landmark-kit/`.

## Result

Validation **PASS** ("all checks pass", run with `--budget 3000`). 734 triangles.
Crest 23.4 m = target height — facts-file LiDAR height 23.4 m (measured; the DataSF ring 201006.0000581 merges tower, annex and plaza, max 94.7 m, so its stats are unusable); consistent with 7 storeys (OSM building:levels).

## Deliverables

- `build_matson_building_annex.py` — deterministic build (`blender -b --python build_matson_building_annex.py`)
- `matson-building-annex.glb`, `matson-building-annex.blend`
- `validate_matson_building_annex.py` → `validation.json`; `render_matson_building_annex.py` → renders below
- Renders: `matson-building-annex-aerial-night.png`, `matson-building-annex-aerial.png`, `matson-building-annex-contact-sheet.png`, `matson-building-annex-east.png`, `matson-building-annex-north.png`, `matson-building-annex-south.png`, `matson-building-annex-top.png`, `matson-building-annex-west.png`
- `REFERENCE.md` (sources, dimensions, cues, uncertainties)

## Contract (from validation.json, fresh-scene re-import)

| | |
|---|---|
| Triangles | 734 |
| Dimensions | 43.9994 x 42.9502 x 23.4 m (world-axis bbox) |
| min Z / XY centre offset | 0.0 / (0.0, 0.0) |
| Objects | 2 |
| Materials | Toy_concrete, Toy_cream, Toy_glassd, Toy_roofd, Toy_sand_Glow, Toy_steel, Toy_terracotta |
| Anchor | [-122.3962538, 37.7924632] |

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

- Plan: OSM SE face, NE/SW ends; NW face computed from the Matson model's SE face + 0.75 m.
- 0–5.4 m `Toy_terracotta` base with arched panes (lit) on SE/NE; cream band.
- 6–21.6 m `tk.punched_block` (6 storeys of 2.6 m) `Toy_cream`, panes 2.8 m apart, SE/NE only.
- Frieze, street-side cornice, parapet to 23.4 m, dark deck, low plant.

All materials are flat `Toy_*` (roughness 0.85, no textures, no alpha). Off-palette: `Toy_terracotta`, `Toy_glassd`, `Toy_concrete` (as Matson).

## Night state

Lit arcade windows in the base and scattered lit office windows on the street faces. Glow materials: `Toy_sand_Glow`; all laid as thin outward skins over solid faces (82 of 82 glow faces unobstructed outward).

## Iterations



## Gate 3 — approval

Pending: renders sent to David.
