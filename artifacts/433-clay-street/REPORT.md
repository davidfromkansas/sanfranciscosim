# The Jay (former Le Méridien San Francisco) — build report

Miniature GLB for SF-SIM, Financial District batch (stages 1–2 of
docs/asset-pipeline/ADDRESS-TO-ASSET.md, BATCH mode), built 2026-10-25 from
`docs/asset-plans/433-clay-street.md` with the shared kit in `tools/landmark-kit/`.

## Result

Validation **PASS** ("all checks pass", run with `--budget 5000`). 3,006 triangles.
Crest 81.0 m = target height — 81 m = OSM height and LiDAR mode 81.0 m (DataSF 2010, parcel 0229020; median 76.6, max 83.2).

## Deliverables

- `build_433_clay_street.py` — deterministic build (`blender -b --python build_433_clay_street.py`)
- `433-clay-street.glb`, `433-clay-street.blend`
- `validate_433_clay_street.py` → `validation.json`; `render_433_clay_street.py` → renders below
- Renders: `433-clay-street-aerial-night.png`, `433-clay-street-aerial.png`, `433-clay-street-contact-sheet.png`, `433-clay-street-east.png`, `433-clay-street-north.png`, `433-clay-street-south.png`, `433-clay-street-top.png`, `433-clay-street-west.png`
- `REFERENCE.md` (sources, dimensions, cues, uncertainties)

## Contract (from validation.json, fresh-scene re-import)

| | |
|---|---|
| Triangles | 3,006 |
| Dimensions | 92.2273 x 45.2796 x 81.0 m (world-axis bbox) |
| min Z / XY centre offset | 0.0 / (0.0, 0.0) |
| Objects | 2 |
| Materials | Toy_concrete, Toy_glassd, Toy_roofd, Toy_sand_Glow, Toy_steel, Toy_stone, Toy_white_Glow |
| Anchor | [-122.4008922, 37.7946815] |

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

- Podium: site polygon to 10 m, glazed and lit ground storey.
- Spine 16 × 20 m to 79.8 m with six vertical steel strips, parapet to 81 m, low plant.
- Each wing: four 5.5 m bays with pointed plans (1.9 m tooth), tops 78/75/72/69 m.
- Per storey (3 m) a dark glazed recess above a solid balcony band on the angled faces; 22% lit.

All materials are flat `Toy_*` (roughness 0.85, no textures, no alpha). Off-palette: `Toy_concrete`, `Toy_glassd`.

## Night state

Lit rooms (22%) on the angled bay faces, lit podium, white crown line on the spine. Glow materials: `Toy_sand_Glow`, `Toy_white_Glow`; all laid as thin outward skins over solid faces (392 of 392 glow faces unobstructed outward).

## Iterations

- Single pass; validated first time (3,006 tris).

## Gate 3 — approval

Approved by David on 2026-10-26 (renders sent as twelve day/night overview sheets): "approve all".

## Stage 4 — optimize

Shipped as `app/public/sf-assets/landmarks/433-clay-street.glb`, meshopt-compressed with the intake flags of `pipeline/compress-assets.mjs` (`gltfpack -c -km -kn -noq`): **165 KB → 70 KB** (58% smaller). Geometry is unchanged. Kit assets are already one body mesh and one glow mesh, so the Blender cleanup pass and the limited dissolve are skipped, as for the Transbay batch. Gate G3 (three.js GLTFLoader round-trip with MeshoptDecoder, `tools/glb-optimize/g3check`) passes.
