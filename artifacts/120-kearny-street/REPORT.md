# One Montgomery Tower (120 Kearny Street) — build report

Miniature GLB for SF-SIM, Financial District batch (stages 1–2 of
docs/asset-pipeline/ADDRESS-TO-ASSET.md, BATCH mode), built 2026-10-25 from
`docs/asset-plans/120-kearny-street.md` with the shared kit in `tools/landmark-kit/`.

## Result

Validation **PASS** ("all checks pass", run with `--budget 5000`). 4,720 triangles.
Crest 152.4 m = target height — published roof 152.4 m (500 ft, Wikipedia); LiDAR 155.95 m.

## Deliverables

- `build_120_kearny_street.py` — deterministic build (`blender -b --python build_120_kearny_street.py`)
- `120-kearny-street.glb`, `120-kearny-street.blend`
- `validate_120_kearny_street.py` → `validation.json`; `render_120_kearny_street.py` → renders below
- Renders: `120-kearny-street-aerial-night.png`, `120-kearny-street-aerial.png`, `120-kearny-street-contact-sheet.png`, `120-kearny-street-east.png`, `120-kearny-street-north.png`, `120-kearny-street-south.png`, `120-kearny-street-top.png`, `120-kearny-street-west.png`
- `REFERENCE.md` (sources, dimensions, cues, uncertainties)

## Contract (from validation.json, fresh-scene re-import)

| | |
|---|---|
| Triangles | 4,720 |
| Dimensions | 65.9566 x 53.2045 x 152.4 m (world-axis bbox) |
| min Z / XY centre offset | 0.0 / (0.0, 0.0) |
| Objects | 2 |
| Materials | Toy_glassd, Toy_granite, Toy_ink, Toy_leaf, Toy_roofd, Toy_rust, Toy_sand_Glow, Toy_steel, Toy_stone, Toy_white_Glow |
| Anchor | [-122.4033381, 37.7891873] |

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

- 54.9 × 38 m rectangle with 2.8 m chamfers.
- Base 0–9 m: `Toy_ink` with lit shop glass.
- Shaft 9–152.4 m: `Toy_granite` prism; 36 storeys × one `Toy_glassd` square window per 3.75 m bay.
- Cap: granite band, parapet, small penthouse and plant.

All materials are flat `Toy_*` (roughness 0.85, no textures, no alpha). Off-palette: `Toy_granite`, `Toy_glassd`.

## Night state

Lit window pairs (30%), lit base glass, white crown line. Glow materials: `Toy_sand_Glow`, `Toy_white_Glow`; all laid as thin outward skins over solid faces (368 of 368 glow faces unobstructed outward).

## Iterations

- Draft used 2 × 2 window blocks in `Toy_rust`; the photo shows individual square windows in a pinker granite — rebuilt with one window per bay per storey in `Toy_granite`.
- First render showed a blank granite roof (the shaft prism ran to the crest over the deck and penthouse); the shaft now stops under the parapet. Final 4,720 tris, all checks pass.
- Deck raised 0.1 m above the shaft top to avoid a coplanar (black) roof.

## Gate 3 — approval

Pending: renders sent to David.
