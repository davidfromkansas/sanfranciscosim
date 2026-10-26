# 575 Market Street — build report

Miniature GLB for SF-SIM, Financial District batch (stages 1–2 of
docs/asset-pipeline/ADDRESS-TO-ASSET.md, BATCH mode), built 2026-10-25 from
`docs/asset-plans/575-market-street.md` with the shared kit in `tools/landmark-kit/`.

## Result

Validation **PASS** ("all checks pass", run with `--budget 5000`). 4,916 triangles.
Crest 174.65 m = target height — published roof 174.65 m (Wikipedia); LiDAR 175.39 m agrees.

## Deliverables

- `build_575_market_street.py` — deterministic build (`blender -b --python build_575_market_street.py`)
- `575-market-street.glb`, `575-market-street.blend`
- `validate_575_market_street.py` → `validation.json`; `render_575_market_street.py` → renders below
- Renders: `575-market-street-aerial-night.png`, `575-market-street-aerial.png`, `575-market-street-contact-sheet.png`, `575-market-street-east.png`, `575-market-street-north.png`, `575-market-street-south.png`, `575-market-street-top.png`, `575-market-street-west.png`
- `REFERENCE.md` (sources, dimensions, cues, uncertainties)

## Contract (from validation.json, fresh-scene re-import)

| | |
|---|---|
| Triangles | 4,916 |
| Dimensions | 62.559 x 62.5992 x 174.65 m (world-axis bbox) |
| min Z / XY centre offset | 0.0 / (0.0, 0.0) |
| Objects | 2 |
| Materials | Toy_glassd, Toy_granite, Toy_leaf, Toy_leafd, Toy_roofd, Toy_rust, Toy_sand_Glow, Toy_steel, Toy_stone, Toy_white_Glow |
| Anchor | [-122.4003805, 37.7895456] |

| Check | Result |
|---|---|
| Crest = target height | PASS |
| Plausible metre dimensions | PASS |
| Base at Z 0 | PASS |
| Centred in XY | PASS |
| Triangle budget (5,000 cap) | PASS |
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

- 45.5 × 29.2 m rectangle, yaw −45.1°.
- Base 0–9 m: inset dark lobby glass behind granite piers, lit ring; granite band.
- Shaft 10.4–167.4 m: `Toy_stone` prism, 39 storeys × one `Toy_glassd` window per 3.3 m bay.
- Top band to 174.65 m: parapet, deck, low plant; trees on the SW plaza.

All materials are flat `Toy_*` (roughness 0.85, no textures, no alpha). Off-palette: `Toy_granite`, `Toy_glassd`.

## Night state

Lit window pairs (30%), lit lobby ring, white crown line. Glow materials: `Toy_sand_Glow`, `Toy_white_Glow`; all laid as thin outward skins over solid faces (320 of 320 glow faces unobstructed outward).

## Iterations

- Draft modelled cream fins (from memory); the photo shows a punched window grid, so the shaft was rebuilt as a pale wall with windows.
- First grid (2.9 m bays) was 5,384 tris; widened to 3.3 m. Final 4,916 tris, all checks pass.

## Gate 3 — approval

Approved by David on 2026-10-26 (renders sent as twelve day/night overview sheets): "approve all".

## Stage 4 — optimize

Shipped as `app/public/sf-assets/landmarks/575-market-street.glb`, meshopt-compressed with the intake flags of `pipeline/compress-assets.mjs` (`gltfpack -c -km -kn -noq`): **267 KB → 105 KB** (61% smaller). Geometry is unchanged. Kit assets are already one body mesh and one glow mesh, so the Blender cleanup pass and the limited dissolve are skipped, as for the Transbay batch. Gate G3 (three.js GLTFLoader round-trip with MeshoptDecoder, `tools/glb-optimize/g3check`) passes.
