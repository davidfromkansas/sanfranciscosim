# Orchard Garden Hotel — build report

Miniature GLB for SF-SIM, Financial District batch (stages 1–2 of
docs/asset-pipeline/ADDRESS-TO-ASSET.md, BATCH mode), built 2026-10-25 from
`docs/asset-plans/466-bush-street.md` with the shared kit in `tools/landmark-kit/`.

## Result

Validation **PASS** ("all checks pass", run with `--budget 3000`). 2,036 triangles.
Crest 34.55 m = target height — DataSF 2010 LiDAR max 34.55 m (penthouse) of ring 201006.0022502; main roof 31.0 m = ring median (measured; OSM height 31).

## Deliverables

- `build_466_bush_street.py` — deterministic build (`blender -b --python build_466_bush_street.py`)
- `466-bush-street.glb`, `466-bush-street.blend`
- `validate_466_bush_street.py` → `validation.json`; `render_466_bush_street.py` → renders below
- Renders: `466-bush-street-aerial-night.png`, `466-bush-street-aerial.png`, `466-bush-street-contact-sheet.png`, `466-bush-street-east.png`, `466-bush-street-north.png`, `466-bush-street-south.png`, `466-bush-street-top.png`, `466-bush-street-west.png`
- `REFERENCE.md` (sources, dimensions, cues, uncertainties)

## Contract (from validation.json, fresh-scene re-import)

| | |
|---|---|
| Triangles | 2,036 |
| Dimensions | 20.5618 x 47.4349 x 34.55 m (world-axis bbox) |
| min Z / XY centre offset | 0.0 / (0.0, 0.0) |
| Objects | 2 |
| Materials | Toy_bronze, Toy_concrete, Toy_cream, Toy_glassd, Toy_glassl, Toy_ink, Toy_roofd, Toy_sand_Glow, Toy_steel, Toy_trim, Toy_white_Glow |
| Anchor | [-122.4052342, 37.7908797] |

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

- OSM outline (12 nodes) as a `tk.punched_block` to 31 m, 9 guest floors of 2.89 m over a lobby storey.
- Bush front: bronze shopfront box with lit lobby, awning; two `Toy_glassl` bays with steel floor bands and lit panes.
- Projecting trim top slab, parapet, dark deck, penthouse to 34.55 m with a crown light, small plant.
- Dark sign plaque on the west wall.

All materials are flat `Toy_*` (roughness 0.85, no textures, no alpha). Off-palette: `Toy_bronze`, `Toy_glassd`, `Toy_concrete`.

## Night state

Bright lobby, scattered lit room windows, lit panes in the glass bays, crown line on the penthouse. Glow materials: `Toy_sand_Glow`, `Toy_white_Glow`; all laid as thin outward skins over solid faces (301 of 302 glow faces unobstructed outward).

## Iterations



## Gate 3 — approval

Approved by David on 2026-10-26 (renders sent as twelve day/night overview sheets): "approve all".

## Stage 4 — optimize

Shipped as `app/public/sf-assets/landmarks/466-bush-street.glb`, meshopt-compressed with the intake flags of `pipeline/compress-assets.mjs` (`gltfpack -c -km -kn -noq`): **109 KB → 49 KB** (55% smaller). Geometry is unchanged. Kit assets are already one body mesh and one glow mesh, so the Blender cleanup pass and the limited dissolve are skipped, as for the Transbay batch. Gate G3 (three.js GLTFLoader round-trip with MeshoptDecoder, `tools/glb-optimize/g3check`) passes.
