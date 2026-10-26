# Adam Grant Building — build report

Miniature GLB for SF-SIM, Financial District batch (stages 1–2 of
docs/asset-pipeline/ADDRESS-TO-ASSET.md, BATCH mode), built 2026-10-25 from
`docs/asset-plans/100-sansome-street.md` with the shared kit in `tools/landmark-kit/`.

## Result

Validation **PASS** ("all checks pass", run with `--budget 3000`). 2,754 triangles.
Crest 58.2 m = target height — DataSF 2010 LiDAR median 58.2 m of ring 201006.0002228 (measured; majority 58.1). The facts file's 41.46 m was a neighbouring ring; OSM height 58 agrees.

## Deliverables

- `build_100_sansome_street.py` — deterministic build (`blender -b --python build_100_sansome_street.py`)
- `100-sansome-street.glb`, `100-sansome-street.blend`
- `validate_100_sansome_street.py` → `validation.json`; `render_100_sansome_street.py` → renders below
- Renders: `100-sansome-street-aerial-night.png`, `100-sansome-street-aerial.png`, `100-sansome-street-contact-sheet.png`, `100-sansome-street-east.png`, `100-sansome-street-north.png`, `100-sansome-street-south.png`, `100-sansome-street-top.png`, `100-sansome-street-west.png`
- `REFERENCE.md` (sources, dimensions, cues, uncertainties)

## Contract (from validation.json, fresh-scene re-import)

| | |
|---|---|
| Triangles | 2,754 |
| Dimensions | 54.2544 x 51.7427 x 58.2 m (world-axis bbox) |
| min Z / XY centre offset | 0.0 / (0.0, 0.0) |
| Objects | 2 |
| Materials | Toy_concrete, Toy_glassd, Toy_ink, Toy_roofd, Toy_rust, Toy_sand, Toy_sand_Glow, Toy_steel, Toy_stone |
| Anchor | [-122.4004726, 37.7915113] |

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

- OSM outer outline (10 nodes, court hole and its slit removed) on yaw 81.3°.
- 0–8.6 m `Toy_stone` base, tall panes, lit; base band.
- 9.4–51.4 m `tk.punched_block` (11 storeys of 3.82 m) `Toy_sand`, panes 3.4 m apart; stone band.
- 52.1–55.6 m top storey; 1.6 m cornice; parapet to 58.2 m; deck, dark court well with rim, low plant, rust water tank.

All materials are flat `Toy_*` (roughness 0.85, no textures, no alpha). Off-palette: `Toy_glassd`, `Toy_concrete`.

## Night state

Lit ground storey and scattered office windows. Glow materials: `Toy_sand_Glow`; all laid as thin outward skins over solid faces (424 of 424 glow faces unobstructed outward).

## Iterations

- First build 3,140 tris (over the 3,000 cap); widened pane spacing to 3.4 m and replaced the base cornice with a band → 2,754.

## Gate 3 — approval

Pending: renders sent to David.
