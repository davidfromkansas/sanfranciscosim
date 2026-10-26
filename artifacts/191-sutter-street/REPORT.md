# Galleria Park Hotel — build report

Miniature GLB for SF-SIM, Financial District batch (stages 1–2 of
docs/asset-pipeline/ADDRESS-TO-ASSET.md, BATCH mode), built 2026-10-25 from
`docs/asset-plans/191-sutter-street.md` with the shared kit in `tools/landmark-kit/`.

## Result

Validation **PASS** ("all checks pass", run with `--budget 3000`). 1,214 triangles.
Crest 32.1 m = target height — LiDAR median roof 32.1 m (DataSF 2010, parcel 0292009); OSM 32 m; the list's 35.2 m was a LiDAR peak.

## Deliverables

- `build_191_sutter_street.py` — deterministic build (`blender -b --python build_191_sutter_street.py`)
- `191-sutter-street.glb`, `191-sutter-street.blend`
- `validate_191_sutter_street.py` → `validation.json`; `render_191_sutter_street.py` → renders below
- Renders: `191-sutter-street-aerial-night.png`, `191-sutter-street-aerial.png`, `191-sutter-street-contact-sheet.png`, `191-sutter-street-east.png`, `191-sutter-street-north.png`, `191-sutter-street-south.png`, `191-sutter-street-top.png`, `191-sutter-street-west.png`
- `REFERENCE.md` (sources, dimensions, cues, uncertainties)

## Contract (from validation.json, fresh-scene re-import)

| | |
|---|---|
| Triangles | 1,214 |
| Dimensions | 41.8307 x 47.2339 x 32.1 m (world-axis bbox) |
| min Z / XY centre offset | 0.0 / (0.0, 0.0) |
| Objects | 2 |
| Materials | Toy_glassd, Toy_ink, Toy_navy, Toy_red, Toy_roofd, Toy_sand_Glow, Toy_steel, Toy_stone, Toy_white_Glow |
| Anchor | [-122.4035145, 37.7896065] |

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

- Rectangle 30.7 × 37.2 m at yaw 9°.
- Base 0–8.6 m `Toy_stone`, with a `Toy_steel` granite skin on the Sutter face (lit shop panes, mezzanine panes), granite band.
- `Toy_red` awning and `Toy_steel` canopy boxes.
- Shaft 8.8–29.6 m `Toy_stone` punched block (six 3.43 m storeys, windows on street and rear faces only), five `Toy_ink` balconies.
- Frieze, `Toy_roofd` cornice 1.5 m out, deck, parapet, low plant to 32.1 m.
- Blade sign: navy fin 9.5–18.5 m with white glow faces both sides.

All materials are flat `Toy_*` (roughness 0.85, no textures, no alpha). Off-palette: `Toy_glassd`.

## Night state

Lit shopfront (85%), ~33% lit rooms, glowing blade sign, warm crown line. Glow materials: `Toy_sand_Glow`, `Toy_white_Glow`; all laid as thin outward skins over solid faces (102 of 102 glow faces unobstructed outward).

## Iterations

- Single pass; validated first time (1,214 tris).

## Gate 3 — approval

Approved by David on 2026-10-26 (renders sent as twelve day/night overview sheets): "approve all".

## Stage 4 — optimize

Shipped as `app/public/sf-assets/landmarks/191-sutter-street.glb`, meshopt-compressed with the intake flags of `pipeline/compress-assets.mjs` (`gltfpack -c -km -kn -noq`): **72 KB → 37 KB** (48% smaller). Geometry is unchanged. Kit assets are already one body mesh and one glow mesh, so the Blender cleanup pass and the limited dissolve are skipped, as for the Transbay batch. Gate G3 (three.js GLTFLoader round-trip with MeshoptDecoder, `tools/glb-optimize/g3check`) passes.
