# I. Magnin & Co. Building — build report

Miniature GLB for SF-SIM, Financial District batch (stages 1–2 of
docs/asset-pipeline/ADDRESS-TO-ASSET.md, BATCH mode), built 2026-10-25 from
`docs/asset-plans/i-magnin-building.md` with the shared kit in `tools/landmark-kit/`.

## Result

Validation **PASS** ("all checks pass", run with `--budget 3000`). 1,916 triangles.
Crest 50.5 m = target height — LiDAR max 50.5 m = the rear block (DataSF 2010, parcel 0312008); main block parapet 44 m (OSM 43, LiDAR median 42.8, mode 47.3).

## Deliverables

- `build_i_magnin_building.py` — deterministic build (`blender -b --python build_i_magnin_building.py`)
- `i-magnin-building.glb`, `i-magnin-building.blend`
- `validate_i_magnin_building.py` → `validation.json`; `render_i_magnin_building.py` → renders below
- Renders: `i-magnin-building-aerial-night.png`, `i-magnin-building-aerial.png`, `i-magnin-building-contact-sheet.png`, `i-magnin-building-east.png`, `i-magnin-building-north.png`, `i-magnin-building-south.png`, `i-magnin-building-top.png`, `i-magnin-building-west.png`
- `REFERENCE.md` (sources, dimensions, cues, uncertainties)

## Contract (from validation.json, fresh-scene re-import)

| | |
|---|---|
| Triangles | 1,916 |
| Dimensions | 39.6817 x 56.519 x 50.5 m (world-axis bbox) |
| min Z / XY centre offset | 0.0 / (0.0, 0.0) |
| Objects | 2 |
| Materials | Toy_cream, Toy_glassd, Toy_ink, Toy_roofd, Toy_sand_Glow, Toy_steel, Toy_stone, Toy_white, Toy_white_Glow |
| Anchor | [-122.4047306, 37.7875148] |

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

- 7-node OSM plan (local), yaw 9°.
- Shop floor 0–6.5 m `Toy_white` with lit display windows on the street faces.
- Body 6.5–42 m `Toy_white` punched block (seven 5.07 m storeys, 5.6 m bays) + slender piers on the street faces.
- Frieze, cornice, parapet to 44 m; six `Toy_ink` fire-escape balconies on Geary.
- Rear block (5-node plan) 43–50.5 m, punched windows, parapet.

All materials are flat `Toy_*` (roughness 0.85, no textures, no alpha). Off-palette: `Toy_glassd`.

## Night state

Lit display windows (80%), ~30% lit office panes, white crown line. Glow materials: `Toy_sand_Glow`, `Toy_white_Glow`; all laid as thin outward skins over solid faces (196 of 196 glow faces unobstructed outward).

## Iterations

- Single pass; validated first time (1,916 tris).

## Gate 3 — approval

Approved by David on 2026-10-26 (renders sent as twelve day/night overview sheets): "approve all".

## Stage 4 — optimize

Shipped as `app/public/sf-assets/landmarks/i-magnin-building.glb`, meshopt-compressed with the intake flags of `pipeline/compress-assets.mjs` (`gltfpack -c -km -kn -noq`): **108 KB → 54 KB** (50% smaller). Geometry is unchanged. Kit assets are already one body mesh and one glow mesh, so the Blender cleanup pass and the limited dissolve are skipped, as for the Transbay batch. Gate G3 (three.js GLTFLoader round-trip with MeshoptDecoder, `tools/glb-optimize/g3check`) passes.
