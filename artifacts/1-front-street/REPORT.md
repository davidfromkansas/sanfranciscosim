# One Front Street — build report

Miniature GLB for SF-SIM, Financial District batch (stages 1–2 of
docs/asset-pipeline/ADDRESS-TO-ASSET.md, BATCH mode), built 2026-10-25 from
`docs/asset-plans/1-front-street.md` with the shared kit in `tools/landmark-kit/`.

## Result

Validation **PASS** ("all checks pass", run with `--budget 5000`). 4,518 triangles.
Crest 164.0 m = target height — published roof 164 m (Wikipedia); LiDAR 158.06 m is the main roof, so the top 6 m is modelled as a white roof screen.

## Deliverables

- `build_1_front_street.py` — deterministic build (`blender -b --python build_1_front_street.py`)
- `1-front-street.glb`, `1-front-street.blend`
- `validate_1_front_street.py` → `validation.json`; `render_1_front_street.py` → renders below
- Renders: `1-front-street-aerial-night.png`, `1-front-street-aerial.png`, `1-front-street-contact-sheet.png`, `1-front-street-east.png`, `1-front-street-north.png`, `1-front-street-south.png`, `1-front-street-top.png`, `1-front-street-west.png`
- `REFERENCE.md` (sources, dimensions, cues, uncertainties)

## Contract (from validation.json, fresh-scene re-import)

| | |
|---|---|
| Triangles | 4,518 |
| Dimensions | 56.2188 x 65.0635 x 164.0 m (world-axis bbox) |
| min Z / XY centre offset | 0.0 / (0.0, 0.0) |
| Objects | 2 |
| Materials | Toy_glassd, Toy_leaf, Toy_leafd, Toy_roofd, Toy_rust, Toy_sand_Glow, Toy_steel, Toy_stone, Toy_white, Toy_white_Glow |
| Anchor | [-122.3988578, 37.7917996] |

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

- Plan: 13-node simplification of the OSM outline (rounding nodes < 1 m dropped).
- Lobby 0–8 m: inset `Toy_glassd` with white piers every 6 m and a lit ring.
- Tower 8–158 m: `Toy_white` prism (0.5 m bevel), 37 storeys of 4.05 m, one `Toy_glassd` ribbon per storey per face (panes 6.5 m with 0.35 m mullion gaps).
- Roof: white screen ring 158–164 m around a dark deck and plant cluster; crown light.

All materials are flat `Toy_*` (roughness 0.85, no textures, no alpha). Off-palette: `Toy_glassd` (dark glass), as in the Transbay batch.

## Night state

Scattered lit ribbon panes (30%), lit lobby ring, white crown line. Glow materials: `Toy_sand_Glow`, `Toy_white_Glow`; all laid as thin outward skins over solid faces (676 of 676 glow faces unobstructed outward).

## Iterations

- Draft: ribbons covered ~70% of each storey and read too dark; changed to ~half white/half glass as in the photo, dropped the screen's window panes.
- Final: 4,518 tris, all checks pass.

## Gate 3 — approval

Approved by David on 2026-10-26 (renders sent as twelve day/night overview sheets): "approve all".

## Stage 4 — optimize

Shipped as `app/public/sf-assets/landmarks/1-front-street.glb`, meshopt-compressed with the intake flags of `pipeline/compress-assets.mjs` (`gltfpack -c -km -kn -noq`): **245 KB → 99 KB** (60% smaller). Geometry is unchanged. Kit assets are already one body mesh and one glow mesh, so the Blender cleanup pass and the limited dissolve are skipped, as for the Transbay batch. Gate G3 (three.js GLTFLoader round-trip with MeshoptDecoder, `tools/glb-optimize/g3check`) passes.
