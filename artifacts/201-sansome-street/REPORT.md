# Royal Insurance Building — build report

Miniature GLB for SF-SIM, Financial District batch (stages 1–2 of
docs/asset-pipeline/ADDRESS-TO-ASSET.md, BATCH mode), built 2026-10-25 from
`docs/asset-plans/201-sansome-street.md` with the shared kit in `tools/landmark-kit/`.

## Result

Validation **PASS** ("all checks pass", run with `--budget 3000`). 2,138 triangles.
Crest 41.3 m = target height — LiDAR median roof 41.3 m (DataSF 2010, parcel 0260017); OSM 41 m agrees; the list's 44.7 m was a higher LiDAR percentile.

## Deliverables

- `build_201_sansome_street.py` — deterministic build (`blender -b --python build_201_sansome_street.py`)
- `201-sansome-street.glb`, `201-sansome-street.blend`
- `validate_201_sansome_street.py` → `validation.json`; `render_201_sansome_street.py` → renders below
- Renders: `201-sansome-street-aerial-night.png`, `201-sansome-street-aerial.png`, `201-sansome-street-contact-sheet.png`, `201-sansome-street-east.png`, `201-sansome-street-north.png`, `201-sansome-street-south.png`, `201-sansome-street-top.png`, `201-sansome-street-west.png`
- `REFERENCE.md` (sources, dimensions, cues, uncertainties)

## Contract (from validation.json, fresh-scene re-import)

| | |
|---|---|
| Triangles | 2,138 |
| Dimensions | 35.2254 x 30.0658 x 41.3 m (world-axis bbox) |
| min Z / XY centre offset | 0.0 / (0.0, 0.0) |
| Objects | 2 |
| Materials | Toy_cream, Toy_glassd, Toy_gold, Toy_roofd, Toy_rust, Toy_sand_Glow, Toy_steel, Toy_stone, Toy_white_Glow |
| Anchor | [-122.4012641, 37.7922609] |

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

- Plan: 6-node OSM L (local), yaw 8.5°.
- Base 0–12.6 m `Toy_stone` with tall ground openings and two window rows, cornice band.
- Shaft 13.4–32.4 m `Toy_rust` punched block, 3.27 m storeys, white quoin piers at the three street corners.
- Top 33.1–39.6 m `Toy_cream` punched block, five `Toy_stone` cartouches, deep cornice, parapet to 41.3 m.
- Arms: cream relief block with a gold clock disc over the Sansome entrance.

All materials are flat `Toy_*` (roughness 0.85, no textures, no alpha). Off-palette: `Toy_glassd`.

## Night state

Lit shop windows on the two street faces (80%), scattered lit panes on shaft and top (~32%), white crown line. Glow materials: `Toy_sand_Glow`, `Toy_white_Glow`; all laid as thin outward skins over solid faces (244 of 250 glow faces unobstructed outward).

## Iterations

- Single pass; validated first time (2,138 tris).

## Gate 3 — approval

Pending: renders sent to David.
