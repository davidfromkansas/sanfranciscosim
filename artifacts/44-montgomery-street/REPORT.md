# 44 Montgomery Street — build report

Miniature GLB for SF-SIM, Financial District batch (stages 1–2 of
docs/asset-pipeline/ADDRESS-TO-ASSET.md, BATCH mode), built 2026-10-25 from
`docs/asset-plans/44-montgomery-street.md` with the shared kit in `tools/landmark-kit/`.

## Result

Validation **PASS** ("all checks pass", run with `--budget 5000`). 4,806 triangles.
Crest 172.2 m = target height — published roof 172.2 m (Wikipedia); antenna 180.7 m not modelled. LiDAR 90.12 m is unusable for this ring.

## Deliverables

- `build_44_montgomery_street.py` — deterministic build (`blender -b --python build_44_montgomery_street.py`)
- `44-montgomery-street.glb`, `44-montgomery-street.blend`
- `validate_44_montgomery_street.py` → `validation.json`; `render_44_montgomery_street.py` → renders below
- Renders: `44-montgomery-street-aerial-night.png`, `44-montgomery-street-aerial.png`, `44-montgomery-street-contact-sheet.png`, `44-montgomery-street-east.png`, `44-montgomery-street-north.png`, `44-montgomery-street-south.png`, `44-montgomery-street-top.png`, `44-montgomery-street-west.png`
- `REFERENCE.md` (sources, dimensions, cues, uncertainties)

## Contract (from validation.json, fresh-scene re-import)

| | |
|---|---|
| Triangles | 4,806 |
| Dimensions | 63.5031 x 96.3661 x 172.2 m (world-axis bbox) |
| min Z / XY centre offset | 0.0 / (0.0, 0.0) |
| Objects | 2 |
| Materials | Toy_glassd, Toy_leaf, Toy_roofd, Toy_rust, Toy_sand_Glow, Toy_steel, Toy_stone, Toy_white, Toy_white_Glow |
| Anchor | [-122.4017708, 37.789628] |

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

- Two slabs on the OSM L: main (6-node) to 172.2 m, east to 150.6 m.
- Each: inset dark glass lobby 0–9 m with lit ring, `Toy_glassd` body, `Toy_white` fins 0.45 × 0.65 m every ~1.65 m from the pavement to 1.6 m above the roof deck.
- Night: lit panes on two-storey bands (7.6 m) laid 0.75 m out, over the fins.

All materials are flat `Toy_*` (roughness 0.85, no textures, no alpha). Off-palette: `Toy_glassd`.

## Night state

Lit two-storey pane groups (30%) over both slabs, lit lobby rings, white crown line. Glow materials: `Toy_sand_Glow`, `Toy_white_Glow`; all laid as thin outward skins over solid faces (1198 of 1198 glow faces unobstructed outward).

## Iterations

- Single pass; validated first time (4,806 tris).

## Gate 3 — approval

Approved by David on 2026-10-26 (renders sent as twelve day/night overview sheets): "approve all".

## Stage 4 — optimize

Shipped as `app/public/sf-assets/landmarks/44-montgomery-street.glb`, meshopt-compressed with the intake flags of `pipeline/compress-assets.mjs` (`gltfpack -c -km -kn -noq`): **263 KB → 122 KB** (54% smaller). Geometry is unchanged. Kit assets are already one body mesh and one glow mesh, so the Blender cleanup pass and the limited dissolve are skipped, as for the Transbay batch. Gate G3 (three.js GLTFLoader round-trip with MeshoptDecoder, `tools/glb-optimize/g3check`) passes.
