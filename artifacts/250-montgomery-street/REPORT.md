# 250 Montgomery Street — build report

Miniature GLB for SF-SIM, Financial District batch (stages 1–2 of
docs/asset-pipeline/ADDRESS-TO-ASSET.md, BATCH mode), built 2026-10-25 from
`docs/asset-plans/250-montgomery-street.md` with the shared kit in `tools/landmark-kit/`.

## Result

Validation **PASS** ("all checks pass", run with `--budget 5000`). 2,170 triangles.
Crest 69.88 m = target height — DataSF 2010 LiDAR max 69.88 m of ring 201006.0004020 (roof screen); main roof 68.0 m = ring median (measured; OSM height 68).

## Deliverables

- `build_250_montgomery_street.py` — deterministic build (`blender -b --python build_250_montgomery_street.py`)
- `250-montgomery-street.glb`, `250-montgomery-street.blend`
- `validate_250_montgomery_street.py` → `validation.json`; `render_250_montgomery_street.py` → renders below
- Renders: `250-montgomery-street-aerial-night.png`, `250-montgomery-street-aerial.png`, `250-montgomery-street-contact-sheet.png`, `250-montgomery-street-east.png`, `250-montgomery-street-north.png`, `250-montgomery-street-south.png`, `250-montgomery-street-top.png`, `250-montgomery-street-west.png`
- `REFERENCE.md` (sources, dimensions, cues, uncertainties)

## Contract (from validation.json, fresh-scene re-import)

| | |
|---|---|
| Triangles | 2,170 |
| Dimensions | 33.7097 x 43.1404 x 69.88 m (world-axis bbox) |
| min Z / XY centre offset | 0.0 / (0.0, 0.0) |
| Objects | 2 |
| Materials | Toy_concrete, Toy_glassd, Toy_granite, Toy_roofd, Toy_sand, Toy_sand_Glow, Toy_steel, Toy_stone, Toy_white_Glow |
| Anchor | [-122.4023007, 37.7916998] |

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

- `tk.rect(22.8, 35.2)` on yaw 80.8°; `Toy_granite` base 0–9 m with panes and lit lobby; stone cap.
- 9.7–60.6 m `tk.punched_block` (12 storeys of 4.24 m) `Toy_stone`, `Toy_sand` piers every 5.8 m.
- Granite cornice; 1.5 m set-back top 61.6–68 m (2 storeys, 40% lit); deck; granite screen around a steel plant core to 69.88 m; white crown line.

All materials are flat `Toy_*` (roughness 0.85, no textures, no alpha). Off-palette: `Toy_granite`, `Toy_glassd`, `Toy_concrete`.

## Night state

Lit lobby, scattered lit windows, brighter top storeys, white crown line. Glow materials: `Toy_sand_Glow`, `Toy_white_Glow`; all laid as thin outward skins over solid faces (402 of 402 glow faces unobstructed outward).

## Iterations



## Gate 3 — approval

Pending: renders sent to David.
