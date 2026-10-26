# 525 Market Street — build report

Miniature GLB for SF-SIM, Financial District batch (stages 1–2 of
docs/asset-pipeline/ADDRESS-TO-ASSET.md, BATCH mode), built 2026-10-25 from
`docs/asset-plans/525-market-street.md` with the shared kit in `tools/landmark-kit/`.

## Result

Validation **PASS** ("all checks pass", run with `--budget 5000`). 2,954 triangles.
Crest 161.0 m = target height — published roof 161 m (Wikipedia); LiDAR 161.76 m agrees.

## Deliverables

- `build_525_market_street.py` — deterministic build (`blender -b --python build_525_market_street.py`)
- `525-market-street.glb`, `525-market-street.blend`
- `validate_525_market_street.py` → `validation.json`; `render_525_market_street.py` → renders below
- Renders: `525-market-street-aerial-night.png`, `525-market-street-aerial.png`, `525-market-street-contact-sheet.png`, `525-market-street-east.png`, `525-market-street-north.png`, `525-market-street-south.png`, `525-market-street-top.png`, `525-market-street-west.png`
- `REFERENCE.md` (sources, dimensions, cues, uncertainties)

## Contract (from validation.json, fresh-scene re-import)

| | |
|---|---|
| Triangles | 2,954 |
| Dimensions | 83.3787 x 83.3573 x 161.0 m (world-axis bbox) |
| min Z / XY centre offset | 0.0 / (0.0, 0.0) |
| Objects | 2 |
| Materials | Toy_glassd, Toy_leaf, Toy_roofd, Toy_rust, Toy_sand, Toy_sand_Glow, Toy_steel, Toy_stone, Toy_white_Glow |
| Anchor | [-122.399158, 37.7905074] |

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

- 57.4 × 48.7 m rectangle at yaw 44.9°.
- Lobby 0–8 m: inset dark glass behind 1.2 m cream columns every 4.8 m, lit ring.
- Tower: `Toy_sand` prism; full-height `Toy_glassd` slits 0.55 m wide every ~1.55 m from 8.6 to 150 m, 2.6 m solid corners.
- Blind top band 150–161 m with a stone reveal line; parapet, deck, plant.

All materials are flat `Toy_*` (roughness 0.85, no textures, no alpha). Off-palette: `Toy_glassd`.

## Night state

Lit slit groups (32%), lit lobby ring, white crown line. Glow materials: `Toy_sand_Glow`, `Toy_white_Glow`; all laid as thin outward skins over solid faces (1290 of 1290 glow faces unobstructed outward).

## Iterations

- Draft (2,020 tris): the tower prism ran to the crest and hid the roof deck and plant (blank cream roof in the aerial); lit windows were chunky three-storey blocks. Tower now stops under the parapet; night lights are single slits two storeys tall.
- Second render: the deck top was coplanar with the tower top and rendered black; deck raised 0.1 m. Final 2,954 tris, all checks pass.

## Gate 3 — approval

Approved by David on 2026-10-26 (renders sent as twelve day/night overview sheets): "approve all".

## Stage 4 — optimize

Shipped as `app/public/sf-assets/landmarks/525-market-street.glb`, meshopt-compressed with the intake flags of `pipeline/compress-assets.mjs` (`gltfpack -c -km -kn -noq`): **164 KB → 72 KB** (56% smaller). Geometry is unchanged. Kit assets are already one body mesh and one glow mesh, so the Blender cleanup pass and the limited dissolve are skipped, as for the Transbay batch. Gate G3 (three.js GLTFLoader round-trip with MeshoptDecoder, `tools/glb-optimize/g3check`) passes.
