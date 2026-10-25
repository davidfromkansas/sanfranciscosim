# One Sansome Street — build report

Miniature GLB for SF-SIM, Financial District batch (stages 1–2 of
docs/asset-pipeline/ADDRESS-TO-ASSET.md, BATCH mode), built 2026-10-25 from
`docs/asset-plans/1-sansome-street.md` with the shared kit in `tools/landmark-kit/`.

## Result

Validation **PASS** ("all checks pass", run with `--budget 5000`). 4,202 triangles.
Crest 168.0 m = target height — published roof 168 m (Wikipedia); LiDAR 174.18 m.

## Deliverables

- `build_1_sansome_street.py` — deterministic build (`blender -b --python build_1_sansome_street.py`)
- `1-sansome-street.glb`, `1-sansome-street.blend`
- `validate_1_sansome_street.py` → `validation.json`; `render_1_sansome_street.py` → renders below
- Renders: `1-sansome-street-aerial-night.png`, `1-sansome-street-aerial.png`, `1-sansome-street-contact-sheet.png`, `1-sansome-street-east.png`, `1-sansome-street-north.png`, `1-sansome-street-south.png`, `1-sansome-street-top.png`, `1-sansome-street-west.png`
- `REFERENCE.md` (sources, dimensions, cues, uncertainties)

## Contract (from validation.json, fresh-scene re-import)

| | |
|---|---|
| Triangles | 4,202 |
| Dimensions | 84.0755 x 58.0822 x 168.0 m (world-axis bbox) |
| min Z / XY centre offset | 0.0 / (0.0, 0.0) |
| Objects | 2 |
| Materials | Toy_copper, Toy_glassd, Toy_glassl, Toy_ink, Toy_roofd, Toy_sand_Glow, Toy_steel, Toy_stone, Toy_white, Toy_white_Glow |
| Anchor | [-122.4011756, 37.7904654] |

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

- Tower: 37.5 × 33.4 m rounded rectangle (r 6.5 m), recessed glass base on stone piers 0–21 m; `Toy_stone` body to 168 m; 37 rows of `Toy_copper` windows on the flat faces.
- Crown: three dark slots (`Toy_ink`) on each face, 8.5–2.5 m below the top, lit at night.
- Bank: OSM east block, white body with arched windows, stone columns, entablature, balustrade, glass roof with lit skylight.
- West wing: 21 m punched block.

All materials are flat `Toy_*` (roughness 0.85, no textures, no alpha). Off-palette: `Toy_copper`, `Toy_glassd`.

## Night state

Lit window rows (28%), lit crown slots, lit bank arches and skylight, lit lobby ring. Glow materials: `Toy_sand_Glow`, `Toy_white_Glow`; all laid as thin outward skins over solid faces (692 of 692 glow faces unobstructed outward).

## Iterations

- Single pass; validated first time (4,202 tris).

## Gate 3 — approval

Pending: renders sent to David.
