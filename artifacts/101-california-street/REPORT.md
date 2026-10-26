# 101 California Street — build report

Miniature GLB for SF-SIM, Financial District batch (stages 1–2 of
docs/asset-pipeline/ADDRESS-TO-ASSET.md, BATCH mode), built 2026-10-25 from
`docs/asset-plans/101-california-street.md` with the shared kit in `tools/landmark-kit/`.

## Result

Validation **PASS** ("all checks pass", run with `--budget 5000`). 4,308 triangles.
Crest 183.0 m = target height — published roof 183 m (Wikipedia); LiDAR 175.24 m is the main roof, the stepped crown tiers rise to 183 m.

## Deliverables

- `build_101_california_street.py` — deterministic build (`blender -b --python build_101_california_street.py`)
- `101-california-street.glb`, `101-california-street.blend`
- `validate_101_california_street.py` → `validation.json`; `render_101_california_street.py` → renders below
- Renders: `101-california-street-aerial-night.png`, `101-california-street-aerial.png`, `101-california-street-contact-sheet.png`, `101-california-street-east.png`, `101-california-street-north.png`, `101-california-street-south.png`, `101-california-street-top.png`, `101-california-street-west.png`
- `REFERENCE.md` (sources, dimensions, cues, uncertainties)

## Contract (from validation.json, fresh-scene re-import)

| | |
|---|---|
| Triangles | 4,308 |
| Dimensions | 94.9862 x 95.1195 x 183.0 m (world-axis bbox) |
| min Z / XY centre offset | 0.0 / (0.0, 0.0) |
| Objects | 2 |
| Materials | Toy_glass, Toy_glassd, Toy_glassl, Toy_leaf, Toy_leafd, Toy_roofd, Toy_rust, Toy_sand_Glow, Toy_steel, Toy_stone, Toy_white_Glow |
| Anchor | [-122.3981206, 37.792957] |

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

- Tower: 28-gon r 27.7 m; 0–28 m colonnade of 14 square stone columns around a recessed lit lobby; stone soffit; `Toy_glass` shaft 29.5–175 m with a pale `Toy_glassl` line every two storeys.
- Crown: two setback tiers (−2.5 m, −6 m) to 183 m, pale ledges, crown light.
- Annex: OSM SW triangle, `Toy_stone` punched block 0–36 m (4 m storeys), roof garden.
- Atrium: sloped `Toy_glassl` lean-to on the annex diagonal (28 m high, 16 m run) with 7 steel ribs and a lit skin.
- Plaza: stone apron over the site, three stepped planting terraces, five trees.

All materials are flat `Toy_*` (roughness 0.85, no textures, no alpha). Off-palette: `Toy_glassd`, `Toy_leafd`.

## Night state

Lit pane groups (30%) on the tower, lit lobby, lit atrium skin, annex windows, crown line. Glow materials: `Toy_sand_Glow`, `Toy_white_Glow`; all laid as thin outward skins over solid faces (647 of 650 glow faces unobstructed outward).

## Iterations

- Draft modelled the tower as banded granite (from memory); the photo shows a blue glass grid on a tall colonnade, so the tower, colonnade, crown and annex colour were rebuilt.
- Atrium ribs started below Z 0; raised.
- First render: the tower's mullion lines and lit panes were silently skipped (pane spacing longer than the 6.2 m facets, line band under the kit's 0.5 m minimum) — blank glass by day and dark at night. Fixed spacing and band height. Final 4,308 tris, all checks pass.

## Gate 3 — approval

Approved by David on 2026-10-26 (renders sent as twelve day/night overview sheets): "approve all".

## Stage 4 — optimize

Shipped as `app/public/sf-assets/landmarks/101-california-street.glb`, meshopt-compressed with the intake flags of `pipeline/compress-assets.mjs` (`gltfpack -c -km -kn -noq`): **224 KB → 89 KB** (60% smaller). Geometry is unchanged. Kit assets are already one body mesh and one glow mesh, so the Blender cleanup pass and the limited dissolve are skipped, as for the Transbay batch. Gate G3 (three.js GLTFLoader round-trip with MeshoptDecoder, `tools/glb-optimize/g3check`) passes.
