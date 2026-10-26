# Yerba Buena Center for the Arts — Galleries — build report

Miniature GLB for SF-SIM, Financial District batch (stages 1–2 of
docs/asset-pipeline/ADDRESS-TO-ASSET.md, BATCH mode), built 2026-10-25 from
`docs/asset-plans/ybca-galleries.md` with the shared kit in `tools/landmark-kit/`.

## Result

Validation **PASS** ("all checks pass", run with `--budget 3000`). 1,222 triangles.
Crest 17.3 m = target height — LiDAR max 17.3 m (DataSF 2010, parcel 3723115; median 10.3 m); the OSM '28 m' tag is rejected.

## Deliverables

- `build_ybca_galleries.py` — deterministic build (`blender -b --python build_ybca_galleries.py`)
- `ybca-galleries.glb`, `ybca-galleries.blend`
- `validate_ybca_galleries.py` → `validation.json`; `render_ybca_galleries.py` → renders below
- Renders: `ybca-galleries-aerial-night.png`, `ybca-galleries-aerial.png`, `ybca-galleries-contact-sheet.png`, `ybca-galleries-east.png`, `ybca-galleries-north.png`, `ybca-galleries-south.png`, `ybca-galleries-top.png`, `ybca-galleries-west.png`
- `REFERENCE.md` (sources, dimensions, cues, uncertainties)

## Contract (from validation.json, fresh-scene re-import)

| | |
|---|---|
| Triangles | 1,222 |
| Dimensions | 83.8882 x 113.4626 x 17.3 m (world-axis bbox) |
| min Z / XY centre offset | 0.0 / (0.0, 0.0) |
| Objects | 2 |
| Materials | Toy_glassd, Toy_glassl, Toy_roofd, Toy_sand_Glow, Toy_sky, Toy_steel, Toy_stone, Toy_white |
| Anchor | [-122.4021445, 37.7855959] |

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

- Two masses from the 19-node OSM outline: gallery block (12 m) and forum wing (9 m), `Toy_steel` with white coping.
- Ground storey glazing (`Toy_glassd`) with lit panes, except on the shared wall.
- Gardens face: full-height `Toy_sky` glass panes (4.4–11.2 m) crossed by a white tube stair band rising from 2.2 to 10 m.
- Raised hall 24 × 32 m to 17.3 m with lit clerestory panes; white canopy; flat dark roofs, low plant.

All materials are flat `Toy_*` (roughness 0.85, no textures, no alpha). Off-palette: `Toy_glassd`.

## Night state

Lit ground storey (60%), lit gardens glass (50%), glowing clerestory (90%). Glow materials: `Toy_sand_Glow`; all laid as thin outward skins over solid faces (204 of 210 glow faces unobstructed outward).

## Iterations

- Collinear plan vertex and beveled plinths on the notched plans produced slivers (degenerate check); plan jogged 0.5 m and plinths made unbeveled.
- Street trees in front of lit glass failed the glow-outward check; removed.
- First render: roof decks sat under the top caps so the roofs read pale and blank; decks raised to show dark with white coping.
- Final: 1,222 tris, all checks pass.

## Gate 3 — approval

Approved by David on 2026-10-26 (renders sent as twelve day/night overview sheets): "approve all".

## Stage 4 — optimize

Shipped as `app/public/sf-assets/landmarks/ybca-galleries.glb`, meshopt-compressed with the intake flags of `pipeline/compress-assets.mjs` (`gltfpack -c -km -kn -noq`): **69 KB → 34 KB** (51% smaller). Geometry is unchanged. Kit assets are already one body mesh and one glow mesh, so the Blender cleanup pass and the limited dissolve are skipped, as for the Transbay batch. Gate G3 (three.js GLTFLoader round-trip with MeshoptDecoder, `tools/glb-optimize/g3check`) passes.
