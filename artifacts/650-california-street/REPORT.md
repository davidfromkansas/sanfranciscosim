# 650 California Street (Hartford Building) — build report

Miniature GLB for SF-SIM, Financial District batch (stages 1–2 of
docs/asset-pipeline/ADDRESS-TO-ASSET.md, BATCH mode), built 2026-10-26 from
`docs/asset-plans/650-california-street.md` with the shared kit in `tools/landmark-kit/`.

## Result

Validation **PASS** ("all checks pass", run with `--budget 5000`). 3,398 triangles.
Crest 142.0 m = target height — published roof 142 m / 466 ft (Wikipedia, Wikidata, Emporis 118886); DataSF LiDAR roof median 142.8 m, max 151.3 m (rooftop plant).

## Deliverables

- `build_650_california_street.py` — deterministic build (`blender -b --python build_650_california_street.py`)
- `650-california-street.glb`, `650-california-street.blend`
- `validate_650_california_street.py` → `validation.json`; `render_650_california_street.py` → renders below
- Renders: `650-california-street-aerial-night.png`, `650-california-street-aerial.png`, `650-california-street-contact-sheet.png`, `650-california-street-east.png`, `650-california-street-north.png`, `650-california-street-south.png`, `650-california-street-top.png`, `650-california-street-west.png`
- `REFERENCE.md` (sources, dimensions, cues, uncertainties)

## Contract (from validation.json, fresh-scene re-import)

| | |
|---|---|
| Triangles | 3,398 |
| Dimensions | 51.0575 x 51.206 x 142.0 m (world-axis bbox) |
| min Z / XY centre offset | 0.0 / (0.0, 0.0) |
| Objects | 2 |
| Materials | Toy_glassd, Toy_glassl, Toy_leaf, Toy_roofd, Toy_rust, Toy_sand_Glow, Toy_steel, Toy_stone, Toy_white |
| Anchor | [-122.4052193, 37.7928669] |

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

- Plan: the 4-node OSM polygon (38.7 m square, yaw 8.9°).
- Lobby 0–9 m: `glassl` set back 3 m, lit ring, 0.9 m white columns every 6.4 m, white soffit.
- Shaft 9–134 m: `tk.shaft` banded loft, dark glass 0.35 m inside the face, white 1.3 m spandrel per storey (31 storeys at 4.03 m).
- Top storey 134–140.4 m (one taller band) and a white parapet ring to 142 m.
- `tk.pier_grid` white verticals every 3.2 m (13 per face), flush with the spandrels, so the grid reads square.
- Roof: dark deck raised clear of the glass cap, low plant kept below the parapet line; sidewalk apron and three trees on California St.

All materials are flat `Toy_*` (roughness 0.85, no textures, no alpha). Off-palette: `Toy_glassd` (kit EXTRA_HEX).

## Night state

Scattered lit office panes (30%, 50% on the top storey) laid just in front of the grid, and a lit lobby band. Glow materials: `Toy_sand_Glow`; all laid as thin outward skins over solid faces (954 of 954 glow faces unobstructed outward).

## Iterations

- v1: 3,398 tris, all checks pass first time; renders read as intended (white square grid, dark recessed glass, lit lobby, clean roof) — no rework.

## Gate 3 — approval

Approved by David on 2026-10-26 (renders sent as twelve day/night overview sheets): "approve all".

## Stage 4 — optimize

Shipped as `app/public/sf-assets/landmarks/650-california-street.glb`, meshopt-compressed with the intake flags of `pipeline/compress-assets.mjs` (`gltfpack -c -km -kn -noq`): **174 KB → 81 KB** (54% smaller). Geometry is unchanged. Kit assets are already one body mesh and one glow mesh, so the Blender cleanup pass and the limited dissolve are skipped, as for the Transbay batch. Gate G3 (three.js GLTFLoader round-trip with MeshoptDecoder, `tools/glb-optimize/g3check`) passes.
