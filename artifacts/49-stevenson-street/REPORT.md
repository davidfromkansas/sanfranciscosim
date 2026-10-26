# 49 Stevenson Street — build report

Miniature GLB for SF-SIM, Financial District batch (stages 1–2 of
docs/asset-pipeline/ADDRESS-TO-ASSET.md, BATCH mode), built 2026-10-25 from
`docs/asset-plans/49-stevenson-street.md` with the shared kit in `tools/landmark-kit/`.

## Result

Validation **PASS** ("all checks pass", run with `--budget 5000`). 2,356 triangles.
Crest 64.44 m = target height — DataSF 2010 LiDAR max 64.44 m of ring 201006.0003248 (screened plant crown, majority 63.9); main roof 60.0 m = ring median (measured).

## Deliverables

- `build_49_stevenson_street.py` — deterministic build (`blender -b --python build_49_stevenson_street.py`)
- `49-stevenson-street.glb`, `49-stevenson-street.blend`
- `validate_49_stevenson_street.py` → `validation.json`; `render_49_stevenson_street.py` → renders below
- Renders: `49-stevenson-street-aerial-night.png`, `49-stevenson-street-aerial.png`, `49-stevenson-street-contact-sheet.png`, `49-stevenson-street-east.png`, `49-stevenson-street-north.png`, `49-stevenson-street-south.png`, `49-stevenson-street-top.png`, `49-stevenson-street-west.png`
- `REFERENCE.md` (sources, dimensions, cues, uncertainties)

## Contract (from validation.json, fresh-scene re-import)

| | |
|---|---|
| Triangles | 2,356 |
| Dimensions | 53.7203 x 53.7598 x 64.44 m (world-axis bbox) |
| min Z / XY centre offset | 0.0 / (0.0, 0.0) |
| Objects | 2 |
| Materials | Toy_concrete, Toy_glassd, Toy_granite, Toy_roofd, Toy_sand_Glow, Toy_steel, Toy_stone, Toy_white_Glow |
| Anchor | [-122.3993904, 37.789706] |

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

- OSM outline (14 nodes, saw-tooth kept) on yaw from 44.9°.
- 0–8.6 m `Toy_granite` base with tall panes and a lit lobby; stone cap.
- 9.3–60 m `tk.shaft`: 13 storeys of 3.9 m, `Toy_glassd` with granite bands, 30% lit.
- Parapet, dark deck, set-back granite screen around a steel plant core to 64.44 m; white crown line.

All materials are flat `Toy_*` (roughness 0.85, no textures, no alpha). Off-palette: `Toy_granite`, `Toy_glassd`, `Toy_concrete`.

## Night state

Lit lobby, scattered lit ribbon panes, white crown line. Glow materials: `Toy_sand_Glow`, `Toy_white_Glow`; all laid as thin outward skins over solid faces (302 of 302 glow faces unobstructed outward).

## Iterations



## Gate 3 — approval

Approved by David on 2026-10-26 (renders sent as twelve day/night overview sheets): "approve all".

## Stage 4 — optimize

Shipped as `app/public/sf-assets/landmarks/49-stevenson-street.glb`, meshopt-compressed with the intake flags of `pipeline/compress-assets.mjs` (`gltfpack -c -km -kn -noq`): **110 KB → 49 KB** (55% smaller). Geometry is unchanged. Kit assets are already one body mesh and one glow mesh, so the Blender cleanup pass and the limited dissolve are skipped, as for the Transbay batch. Gate G3 (three.js GLTFLoader round-trip with MeshoptDecoder, `tools/glb-optimize/g3check`) passes.
