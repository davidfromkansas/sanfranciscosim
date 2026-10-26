# One Post Street — build report

Miniature GLB for SF-SIM, Financial District batch (stages 1–2 of
docs/asset-pipeline/ADDRESS-TO-ASSET.md, BATCH mode), built 2026-10-25 from
`docs/asset-plans/1-post-street.md` with the shared kit in `tools/landmark-kit/`.

## Result

Validation **PASS** ("all checks pass", run with `--budget 5000`). 2,866 triangles.
Crest 161.0 m = target height — published roof 161 m (529 ft, Wikipedia); LiDAR 166.04 m.

## Deliverables

- `build_1_post_street.py` — deterministic build (`blender -b --python build_1_post_street.py`)
- `1-post-street.glb`, `1-post-street.blend`
- `validate_1_post_street.py` → `validation.json`; `render_1_post_street.py` → renders below
- Renders: `1-post-street-aerial-night.png`, `1-post-street-aerial.png`, `1-post-street-contact-sheet.png`, `1-post-street-east.png`, `1-post-street-north.png`, `1-post-street-south.png`, `1-post-street-top.png`, `1-post-street-west.png`
- `REFERENCE.md` (sources, dimensions, cues, uncertainties)

## Contract (from validation.json, fresh-scene re-import)

| | |
|---|---|
| Triangles | 2,866 |
| Dimensions | 46.8054 x 49.6789 x 161.0 m (world-axis bbox) |
| min Z / XY centre offset | 0.0 / (0.0, 0.0) |
| Objects | 2 |
| Materials | Toy_bronze, Toy_glassd, Toy_glassl, Toy_ink, Toy_leaf, Toy_roofd, Toy_rust, Toy_sand_Glow, Toy_steel, Toy_stone, Toy_white_Glow |
| Anchor | [-122.4026603, 37.7887621] |

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

- 8-node OSM octagon.
- Lobby 0–8 m `Toy_glassl` with lit ring; bronze transfer band.
- Shaft: `Toy_glassd` body, `Toy_bronze` piers 0.8 × 0.75 m every ~2.25 m to the roof, faint `Toy_ink` spandrel line every ~4 storeys.
- Flat top: deck, bronze parapet, low plant. Plaza with octagonal BART well and trees.

All materials are flat `Toy_*` (roughness 0.85, no textures, no alpha). Off-palette: `Toy_bronze`, `Toy_glassd`.

## Night state

Lit pane groups (30%) over the piers, lit lobby, crown line. Glow materials: `Toy_sand_Glow`, `Toy_white_Glow`; all laid as thin outward skins over solid faces (376 of 376 glow faces unobstructed outward).

## Iterations

- Single pass; validated first time (2,866 tris).

## Gate 3 — approval

Approved by David on 2026-10-26 (renders sent as twelve day/night overview sheets): "approve all".

## Stage 4 — optimize

Shipped as `app/public/sf-assets/landmarks/1-post-street.glb`, meshopt-compressed with the intake flags of `pipeline/compress-assets.mjs` (`gltfpack -c -km -kn -noq`): **158 KB → 61 KB** (61% smaller). Geometry is unchanged. Kit assets are already one body mesh and one glow mesh, so the Blender cleanup pass and the limited dissolve are skipped, as for the Transbay batch. Gate G3 (three.js GLTFLoader round-trip with MeshoptDecoder, `tools/glb-optimize/g3check`) passes.
