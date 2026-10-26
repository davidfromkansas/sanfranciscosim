# Stock Exchange Tower — build report

Miniature GLB for SF-SIM, Financial District batch (stages 1–2 of
docs/asset-pipeline/ADDRESS-TO-ASSET.md, BATCH mode), built 2026-10-25 from
`docs/asset-plans/155-sansome-street.md` with the shared kit in `tools/landmark-kit/`.

## Result

Validation **PASS** ("all checks pass", run with `--budget 5000`). 2,642 triangles.
Crest 64.05 m = target height — facts-file LiDAR peak 64.05 m (stepped crown); main roof 54.6 m = DataSF ring 201006.0005660 median (measured; OSM height 55). Ring max 73.5 m not modelled.

## Deliverables

- `build_155_sansome_street.py` — deterministic build (`blender -b --python build_155_sansome_street.py`)
- `155-sansome-street.glb`, `155-sansome-street.blend`
- `validate_155_sansome_street.py` → `validation.json`; `render_155_sansome_street.py` → renders below
- Renders: `155-sansome-street-aerial-night.png`, `155-sansome-street-aerial.png`, `155-sansome-street-contact-sheet.png`, `155-sansome-street-east.png`, `155-sansome-street-north.png`, `155-sansome-street-south.png`, `155-sansome-street-top.png`, `155-sansome-street-west.png`
- `REFERENCE.md` (sources, dimensions, cues, uncertainties)

## Contract (from validation.json, fresh-scene re-import)

| | |
|---|---|
| Triangles | 2,642 |
| Dimensions | 53.5496 x 21.9022 x 64.05 m (world-axis bbox) |
| min Z / XY centre offset | 0.0 / (0.0, 0.0) |
| Objects | 2 |
| Materials | Toy_concrete, Toy_glassd, Toy_gold, Toy_roofd, Toy_sand_Glow, Toy_steel, Toy_stone, Toy_white, Toy_white_Glow |
| Anchor | [-122.4012628, 37.7916701] |

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

- `tk.rect(48, 10.2)` on yaw 81.3°; `Toy_stone` base 0–7.6 m with panes; white portal, lit door, gold name panel, relief disc and figure.
- 8.2–54.6 m `tk.punched_block` (11 storeys of 4.22 m), white piers every 2.5 m.
- Parapet, deck; crown step 1 (22 × 8.4 m, to 59.9 m, lit windows), step 2 (9 × 6 m, to 64.05 m) with a white crown line; low plant.

All materials are flat `Toy_*` (roughness 0.85, no textures, no alpha). Off-palette: `Toy_glassd`, `Toy_concrete`.

## Night state

Lit door, scattered lit office windows, brighter City Club floors in the crown, white crown line. Glow materials: `Toy_sand_Glow`, `Toy_white_Glow`; all laid as thin outward skins over solid faces (358 of 358 glow faces unobstructed outward).

## Iterations

- First build had 12 degenerate triangles from a 0.3 m bevel on a 0.25 m relief slab; bevel 0.08 → clean.

## Gate 3 — approval

Pending: renders sent to David.
