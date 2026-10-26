# Savings Union Bank Building — build report

Miniature GLB for SF-SIM, Financial District batch (stages 1–2 of
docs/asset-pipeline/ADDRESS-TO-ASSET.md, BATCH mode), built 2026-10-25 from
`docs/asset-plans/1-grant-avenue.md` with the shared kit in `tools/landmark-kit/`.

## Result

Validation **PASS** ("all checks pass", run with `--budget 3000`). 858 triangles.
Crest 30.22 m = target height — DataSF 2010 LiDAR max 30.22 m (dome) of ring 201006.0004905; attic roof 25.6 m = ring median (measured; OSM height 26).

## Deliverables

- `build_1_grant_avenue.py` — deterministic build (`blender -b --python build_1_grant_avenue.py`)
- `1-grant-avenue.glb`, `1-grant-avenue.blend`
- `validate_1_grant_avenue.py` → `validation.json`; `render_1_grant_avenue.py` → renders below
- Renders: `1-grant-avenue-aerial-night.png`, `1-grant-avenue-aerial.png`, `1-grant-avenue-contact-sheet.png`, `1-grant-avenue-east.png`, `1-grant-avenue-north.png`, `1-grant-avenue-south.png`, `1-grant-avenue-top.png`, `1-grant-avenue-west.png`
- `REFERENCE.md` (sources, dimensions, cues, uncertainties)

## Contract (from validation.json, fresh-scene re-import)

| | |
|---|---|
| Triangles | 858 |
| Dimensions | 35.71 x 33.612 x 30.22 m (world-axis bbox) |
| min Z / XY centre offset | 0.0 / (0.0, 0.0) |
| Objects | 2 |
| Materials | Toy_concrete, Toy_glassd, Toy_roofd, Toy_sand_Glow, Toy_stone, Toy_white |
| Anchor | [-122.4051939, 37.786999] |

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

- Plinth 0–1.4 m; `Toy_white` walls to 20 m with 2.6 m colonnade recesses on S and E; tall panes (lit) in the recesses.
- Four columns on O'Farrell, three on Grant (tapered 8-sided, `Toy_stone`); capital band, entablature, cornice.
- Attic to 25.6 m; stone drum; four-ring `Toy_white` dome; pediment over the O'Farrell colonnade; lantern with a lit oculus at 30.22 m.

All materials are flat `Toy_*` (roughness 0.85, no textures, no alpha). Off-palette: `Toy_glassd`, `Toy_concrete`.

## Night state

Lit tall windows behind the colonnades and a lit oculus. Glow materials: `Toy_sand_Glow`; all laid as thin outward skins over solid faces (22 of 22 glow faces unobstructed outward).

## Iterations

- Built first from the LiDAR alone (verdigris dome, no pediment); the Phelan photo then showed a white dome and a pediment on O'Farrell, both added.

## Gate 3 — approval

Approved by David on 2026-10-26 (renders sent as twelve day/night overview sheets): "approve all".

## Stage 4 — optimize

Shipped as `app/public/sf-assets/landmarks/1-grant-avenue.glb`, meshopt-compressed with the intake flags of `pipeline/compress-assets.mjs` (`gltfpack -c -km -kn -noq`): **48 KB → 27 KB** (44% smaller). Geometry is unchanged. Kit assets are already one body mesh and one glow mesh, so the Blender cleanup pass and the limited dissolve are skipped, as for the Transbay batch. Gate G3 (three.js GLTFLoader round-trip with MeshoptDecoder, `tools/glb-optimize/g3check`) passes.
