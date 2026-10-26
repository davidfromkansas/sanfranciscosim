# Palace Hotel — build report

Miniature GLB for SF-SIM, Financial District batch (stages 1–2 of
docs/asset-pipeline/ADDRESS-TO-ASSET.md, BATCH mode), built 2026-10-25 from
`docs/asset-plans/palace-hotel.md` with the shared kit in `tools/landmark-kit/`.

## Result

Validation **PASS** ("all checks pass", run with `--budget 3000`). 2,220 triangles.
Crest 40.0 m = target height — DataSF 2010 LiDAR majority 40.0 m of ring 201006.0000105 (measured; median 37.0, max 50.2). Wikipedia gives 35 m; the LiDAR roof surface is used because the lead asked for LiDAR heights and 9 storeys + cornice fit 38–40 m.

## Deliverables

- `build_palace_hotel.py` — deterministic build (`blender -b --python build_palace_hotel.py`)
- `palace-hotel.glb`, `palace-hotel.blend`
- `validate_palace_hotel.py` → `validation.json`; `render_palace_hotel.py` → renders below
- Renders: `palace-hotel-aerial-night.png`, `palace-hotel-aerial.png`, `palace-hotel-contact-sheet.png`, `palace-hotel-east.png`, `palace-hotel-north.png`, `palace-hotel-south.png`, `palace-hotel-top.png`, `palace-hotel-west.png`
- `REFERENCE.md` (sources, dimensions, cues, uncertainties)

## Contract (from validation.json, fresh-scene re-import)

| | |
|---|---|
| Triangles | 2,220 |
| Dimensions | 136.8422 x 136.663 x 40.0 m (world-axis bbox) |
| min Z / XY centre offset | 0.0 / (0.0, 0.0) |
| Objects | 2 |
| Materials | Toy_concrete, Toy_glassd, Toy_glassl, Toy_granite, Toy_ink, Toy_roofd, Toy_sand_Glow, Toy_steel, Toy_stone |
| Anchor | [-122.4019446, 37.7879687] |

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

- `tk.rect(102.8, 78.6)` on yaw from 134.7°; `Toy_stone` base 0–9 m with shop panes (lit).
- 9.7–31.6 m `Toy_granite` (tan) punched shaft, 6 storeys of 3.65 m, panes 4.6 m apart; stone corner quoins.
- Stone band; top storey 32.3–36.4 m with round-headed panes; 1.6 m cornice band; parapet to 40 m.
- Roof: dark deck, Garden Court (34 × 26 m) glass slab + `Toy_sand_Glow` cap with a stone rim, two dark light wells, a plant cluster on the Market side.

All materials are flat `Toy_*` (roughness 0.85, no textures, no alpha). Off-palette: `Toy_granite`, `Toy_glassd`, `Toy_concrete`.

## Night state

Lit shop and lobby windows, scattered lit rooms, the glowing Garden Court roof. Glow materials: `Toy_sand_Glow`; all laid as thin outward skins over solid faces (372 of 372 glow faces unobstructed outward).

## Iterations



## Gate 3 — approval

Approved by David on 2026-10-26 (renders sent as twelve day/night overview sheets): "approve all".

## Stage 4 — optimize

Shipped as `app/public/sf-assets/landmarks/palace-hotel.glb`, meshopt-compressed with the intake flags of `pipeline/compress-assets.mjs` (`gltfpack -c -km -kn -noq`): **119 KB → 49 KB** (59% smaller). Geometry is unchanged. Kit assets are already one body mesh and one glow mesh, so the Blender cleanup pass and the limited dissolve are skipped, as for the Transbay batch. Gate G3 (three.js GLTFLoader round-trip with MeshoptDecoder, `tools/glb-optimize/g3check`) passes.
