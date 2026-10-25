# 50 California Street — build report

Miniature GLB for SF-SIM, Financial District batch (stages 1–2 of
docs/asset-pipeline/ADDRESS-TO-ASSET.md, BATCH mode), built 2026-10-25 from
`docs/asset-plans/50-california-street.md` with the shared kit in `tools/landmark-kit/`.

## Result

Validation **PASS** ("all checks pass", run with `--budget 5000`). 3,176 triangles.
Crest 148.44 m = target height — published roof 148.44 m (Wikipedia); LiDAR 153.71 m includes rooftop plant.

## Deliverables

- `build_50_california_street.py` — deterministic build (`blender -b --python build_50_california_street.py`)
- `50-california-street.glb`, `50-california-street.blend`
- `validate_50_california_street.py` → `validation.json`; `render_50_california_street.py` → renders below
- Renders: `50-california-street-aerial-night.png`, `50-california-street-aerial.png`, `50-california-street-contact-sheet.png`, `50-california-street-east.png`, `50-california-street-north.png`, `50-california-street-south.png`, `50-california-street-top.png`, `50-california-street-west.png`
- `REFERENCE.md` (sources, dimensions, cues, uncertainties)

## Contract (from validation.json, fresh-scene re-import)

| | |
|---|---|
| Triangles | 3,176 |
| Dimensions | 57.085 x 72.3941 x 148.44 m (world-axis bbox) |
| min Z / XY centre offset | 0.0 / (0.0, 0.0) |
| Objects | 2 |
| Materials | Toy_concrete, Toy_glassd, Toy_leaf, Toy_leafd, Toy_roofd, Toy_rust, Toy_sand_Glow, Toy_steel, Toy_stone, Toy_white, Toy_white_Glow |
| Anchor | [-122.3973858, 37.7940826] |

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

- Tower: 31.7 × 60.9 m rectangle; lobby 0–7 m inset dark glass with lit ring; concrete transfer band.
- Shaft 8–141 m: `Toy_glassd` body, `Toy_concrete` fins 0.4 × 0.6 m every 1.5 m, 2.6 m `Toy_white` corner piers.
- Cap 141–148.44 m: white band and parapet, deck, low plant.
- Pavilion: 10.2 × 35.7 m, 7 m, glazed and lit; stone plaza and four trees.

All materials are flat `Toy_*` (roughness 0.85, no textures, no alpha). Off-palette: `Toy_concrete`, `Toy_glassd`.

## Night state

Lit two-storey pane groups (30%) over the fins, lit lobby and pavilion, white crown line. Glow materials: `Toy_sand_Glow`, `Toy_white_Glow`; all laid as thin outward skins over solid faces (696 of 696 glow faces unobstructed outward).

## Iterations

- Single pass after the photo arrived; validated first time (3,176 tris).

## Gate 3 — approval

Pending: renders sent to David.
