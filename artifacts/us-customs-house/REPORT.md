# U.S. Custom House — build report

Miniature GLB for SF-SIM, Financial District batch (stages 1–2 of
docs/asset-pipeline/ADDRESS-TO-ASSET.md, BATCH mode), built 2026-10-25 from
`docs/asset-plans/us-customs-house.md` with the shared kit in `tools/landmark-kit/`.

## Result

Validation **PASS** ("all checks pass", run with `--budget 3000`). 2,834 triangles.
Crest 30.46 m = target height — DataSF 2010 LiDAR max 30.46 m (sculpture group over the cornice); roof parapet 28.87 m = ring majority (measured).

## Deliverables

- `build_us_customs_house.py` — deterministic build (`blender -b --python build_us_customs_house.py`)
- `us-customs-house.glb`, `us-customs-house.blend`
- `validate_us_customs_house.py` → `validation.json`; `render_us_customs_house.py` → renders below
- Renders: `us-customs-house-aerial-night.png`, `us-customs-house-aerial.png`, `us-customs-house-contact-sheet.png`, `us-customs-house-east.png`, `us-customs-house-north.png`, `us-customs-house-south.png`, `us-customs-house-top.png`, `us-customs-house-west.png`
- `REFERENCE.md` (sources, dimensions, cues, uncertainties)

## Contract (from validation.json, fresh-scene re-import)

| | |
|---|---|
| Triangles | 2,834 |
| Dimensions | 50.8194 x 89.0101 x 30.46 m (world-axis bbox) |
| min Z / XY centre offset | 0.0 / (0.0, 0.0) |
| Objects | 2 |
| Materials | Toy_concrete, Toy_glassd, Toy_glassl, Toy_roofd, Toy_sand_Glow, Toy_steel, Toy_stone, Toy_verdigris, Toy_white, Toy_white_Glow |
| Anchor | [-122.4009459, 37.7962972] |

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

- Plan: U in local metres (wings 19–20 m deep around a 35 m court) on the OSM OBB, yaw from bearing 81.5°.
- 0–6.4 m `Toy_stone` base, one rustication band, tall ground-floor panes, lit; base course.
- 7.1–22 m `tk.punched_block` (3 storeys of 4.97 m) in `Toy_white`; 1.3 m cornice.
- 23.3–28.87 m top storey set in 1.6 m with panes, parapet, dark deck and a low plant strip.
- Battery frontispiece: proud wall, six columns, arched lit door; stepped sculpture group to 30.46 m; smaller eagle groups on the Washington and Jackson centres.
- Court: oval pavilion 0–12.6 m with arched windows, verdigris hipped roof and three lit skylights; link block to the Battery wing.

All materials are flat `Toy_*` (roughness 0.85, no textures, no alpha). Off-palette: `Toy_concrete`, `Toy_glassd` (documented in the kit).

## Night state

Lit ground-floor and office windows (30–45%), the lit Battery door, the Custom Hall's arched windows and three white-lit skylights. Glow materials: `Toy_sand_Glow`, `Toy_white_Glow`; all laid as thin outward skins over solid faces (296 of 296 glow faces unobstructed outward).

## Iterations



## Gate 3 — approval

Approved by David on 2026-10-26 (renders sent as twelve day/night overview sheets): "approve all".

## Stage 4 — optimize

Shipped as `app/public/sf-assets/landmarks/us-customs-house.glb`, meshopt-compressed with the intake flags of `pipeline/compress-assets.mjs` (`gltfpack -c -km -kn -noq`): **154 KB → 76 KB** (51% smaller). Geometry is unchanged. Kit assets are already one body mesh and one glow mesh, so the Blender cleanup pass and the limited dissolve are skipped, as for the Transbay batch. Gate G3 (three.js GLTFLoader round-trip with MeshoptDecoder, `tools/glb-optimize/g3check`) passes.
