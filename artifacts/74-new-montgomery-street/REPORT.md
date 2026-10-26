# The Montgomery — build report

Miniature GLB for SF-SIM, Financial District batch (stages 1–2 of
docs/asset-pipeline/ADDRESS-TO-ASSET.md, BATCH mode), built 2026-10-25 from
`docs/asset-plans/74-new-montgomery-street.md` with the shared kit in `tools/landmark-kit/`.

## Result

Validation **PASS** ("all checks pass", run with `--budget 3000`). 2,068 triangles.
Crest 32.7 m = target height — LiDAR median roof 32.7 m (DataSF 2010, parcel 3707064); OSM 33 m; mode 33.2 m.

## Deliverables

- `build_74_new_montgomery_street.py` — deterministic build (`blender -b --python build_74_new_montgomery_street.py`)
- `74-new-montgomery-street.glb`, `74-new-montgomery-street.blend`
- `validate_74_new_montgomery_street.py` → `validation.json`; `render_74_new_montgomery_street.py` → renders below
- Renders: `74-new-montgomery-street-aerial-night.png`, `74-new-montgomery-street-aerial.png`, `74-new-montgomery-street-contact-sheet.png`, `74-new-montgomery-street-east.png`, `74-new-montgomery-street-north.png`, `74-new-montgomery-street-south.png`, `74-new-montgomery-street-top.png`, `74-new-montgomery-street-west.png`
- `REFERENCE.md` (sources, dimensions, cues, uncertainties)

## Contract (from validation.json, fresh-scene re-import)

| | |
|---|---|
| Triangles | 2,068 |
| Dimensions | 79.9738 x 79.9738 x 32.7 m (world-axis bbox) |
| min Z / XY centre offset | 0.0 / (0.0, 0.0) |
| Objects | 2 |
| Materials | Toy_cream, Toy_glassd, Toy_glassl, Toy_roofd, Toy_sand_Glow, Toy_steel, Toy_stone, Toy_white_Glow |
| Anchor | [-122.4013268, 37.7874752] |

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

- Rectangle 82 × 21.3 m at yaw 45°.
- Base 0–14.6 m `Toy_steel`: shop panes (lit), mezzanine and third-storey panes, five rustication bands.
- Body 14.6–29.6 m `Toy_cream` punched block (4 storeys of 3.35 m) with 1.1 m pilasters + capitals on the two street faces every 4.1 m.
- Cornice (1.25 m out) at 28 m, attic with small windows, top cornice, cream parapet to 32.7 m.

All materials are flat `Toy_*` (roughness 0.85, no textures, no alpha). Off-palette: `Toy_glassd` (shopfronts).

## Night state

Lit shopfronts on the two street faces (75%), scattered lit panes (~33%) on body and attic, white line under the cornice. Glow materials: `Toy_sand_Glow`, `Toy_white_Glow`; all laid as thin outward skins over solid faces (150 of 150 glow faces unobstructed outward).

## Iterations

- Draft roof had rooftop trees poking 2.3 m over the crest; removed and the roof rebuilt as deck + parapet.
- First render: `Toy_roofd` base read as black; changed to `Toy_steel`.
- Final: 2,068 tris, all checks pass.

## Gate 3 — approval

Approved by David on 2026-10-26 (renders sent as twelve day/night overview sheets): "approve all".

## Stage 4 — optimize

Shipped as `app/public/sf-assets/landmarks/74-new-montgomery-street.glb`, meshopt-compressed with the intake flags of `pipeline/compress-assets.mjs` (`gltfpack -c -km -kn -noq`): **114 KB → 51 KB** (55% smaller). Geometry is unchanged. Kit assets are already one body mesh and one glow mesh, so the Blender cleanup pass and the limited dissolve are skipped, as for the Transbay batch. Gate G3 (three.js GLTFLoader round-trip with MeshoptDecoder, `tools/glb-optimize/g3check`) passes.
