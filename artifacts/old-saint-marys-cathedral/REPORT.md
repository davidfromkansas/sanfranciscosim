# Old Saint Mary's Cathedral — build report

Miniature GLB for SF-SIM, Financial District batch (stages 1–2 of
docs/asset-pipeline/ADDRESS-TO-ASSET.md, BATCH mode), built 2026-10-25 from
`docs/asset-plans/old-saint-marys-cathedral.md` with the shared kit in `tools/landmark-kit/`.

## Result

Validation **PASS** ("all checks pass", run with `--budget 3000`). 1,694 triangles.
Crest 33.65 m = target height — DataSF 2010 LiDAR max 33.65 m (tower cross) of ring 201006.0002205; tower parapet 26.5 m = facts-file LiDAR peak; nave ridge 20.5 m between ring median 19.3 and majority 21.4 (measured).

## Deliverables

- `build_old_saint_marys_cathedral.py` — deterministic build (`blender -b --python build_old_saint_marys_cathedral.py`)
- `old-saint-marys-cathedral.glb`, `old-saint-marys-cathedral.blend`
- `validate_old_saint_marys_cathedral.py` → `validation.json`; `render_old_saint_marys_cathedral.py` → renders below
- Renders: `old-saint-marys-cathedral-aerial-night.png`, `old-saint-marys-cathedral-aerial.png`, `old-saint-marys-cathedral-contact-sheet.png`, `old-saint-marys-cathedral-east.png`, `old-saint-marys-cathedral-north.png`, `old-saint-marys-cathedral-south.png`, `old-saint-marys-cathedral-top.png`, `old-saint-marys-cathedral-west.png`
- `REFERENCE.md` (sources, dimensions, cues, uncertainties)

## Contract (from validation.json, fresh-scene re-import)

| | |
|---|---|
| Triangles | 1,694 |
| Dimensions | 53.2554 x 56.5804 x 33.65 m (world-axis bbox) |
| min Z / XY centre offset | 0.0 / (0.0, 0.0) |
| Objects | 2 |
| Materials | Toy_brick, Toy_concrete, Toy_cream, Toy_cream_Glow, Toy_glassd, Toy_ink, Toy_mustard_Glow, Toy_roofd, Toy_sand_Glow, Toy_stone |
| Anchor | [-122.4057137, 37.7928426] |

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

- Nave 21.1 × 42.5 m brick prism to 13 m with buttresses every 5.3 m, lancets (lit), parapet and merlons; slate-dark gable roof to 20.5 m; brick gable wall.
- Tower 6.9 × 6.9 m to 26.5 m: corner buttresses, stone bands, louvred belfry arches, door; clock discs (S, W) with glow and plaques.
- Stone parapet, four brick pinnacles with stone caps, a gablet and the cross to 33.65 m.
- Parish hall L-block (11 m) to the east, porches, side chapel on Grant.

All materials are flat `Toy_*` (roughness 0.85, no textures, no alpha). Off-palette: `Toy_concrete`, `Toy_glassd`.

## Night state

Warm (mustard) lit lancets and tower door, glowing clock faces, lit parish-hall windows. Glow materials: `Toy_cream_Glow`, `Toy_mustard_Glow`, `Toy_sand_Glow`; all laid as thin outward skins over solid faces (124 of 124 glow faces unobstructed outward).

## Iterations



## Gate 3 — approval

Pending: renders sent to David.
