# Pacific Coast Stock Exchange — build report

Miniature GLB for SF-SIM, Financial District batch (stages 1–2 of
docs/asset-pipeline/ADDRESS-TO-ASSET.md, BATCH mode), built 2026-10-25 from
`docs/asset-plans/301-pine-street.md` with the shared kit in `tools/landmark-kit/`.

## Result

Validation **PASS** ("all checks pass", run with `--budget 3000`). 1,226 triangles.
Crest 15.9 m = target height — DataSF 2010 LiDAR median roof 15.9 m of ring 201006.0002868 (measured; OSM height 16). The facts file's 32 m and the ring max 48 m come from the abutting 155 Sansome tower.

## Deliverables

- `build_301_pine_street.py` — deterministic build (`blender -b --python build_301_pine_street.py`)
- `301-pine-street.glb`, `301-pine-street.blend`
- `validate_301_pine_street.py` → `validation.json`; `render_301_pine_street.py` → renders below
- Renders: `301-pine-street-aerial-night.png`, `301-pine-street-aerial.png`, `301-pine-street-contact-sheet.png`, `301-pine-street-east.png`, `301-pine-street-north.png`, `301-pine-street-south.png`, `301-pine-street-top.png`, `301-pine-street-west.png`
- `REFERENCE.md` (sources, dimensions, cues, uncertainties)

## Contract (from validation.json, fresh-scene re-import)

| | |
|---|---|
| Triangles | 1,226 |
| Dimensions | 48.0994 x 36.0449 x 15.9 m (world-axis bbox) |
| min Z / XY centre offset | 0.0 / (0.0, 0.0) |
| Objects | 2 |
| Materials | Toy_concrete, Toy_glassd, Toy_glassl, Toy_roofd, Toy_sand_Glow, Toy_steel, Toy_stone, Toy_white |
| Anchor | [-122.4013037, 37.7918447] |

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

- Hall prism with a 4.2 m colonnade recess on Pine, 0–13 m `Toy_stone`, base course.
- Eight tapered `Toy_white` columns on a three-step stair; tall lit windows on the recessed wall.
- Entablature with a dark name band; cornice; attic and parapet to 15.9 m; trading-hall skylight (lit) and low plant.
- Figure groups: pedestal + three blocky figures + heads on each side.

All materials are flat `Toy_*` (roughness 0.85, no textures, no alpha). Off-palette: `Toy_concrete`, `Toy_glassd`.

## Night state

Tall lit windows behind the colonnade (the gym) and the lit trading-hall skylight. Glow materials: `Toy_sand_Glow`; all laid as thin outward skins over solid faces (18 of 18 glow faces unobstructed outward).

## Iterations



## Gate 3 — approval

Pending: renders sent to David.
