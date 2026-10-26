# 201 Spear Street — build report

Miniature GLB for SF-SIM, Financial District batch (stages 1–2 of
docs/asset-pipeline/ADDRESS-TO-ASSET.md, BATCH mode), built 2026-10-25 from
`docs/asset-plans/201-spear-street.md` with the shared kit in `tools/landmark-kit/`.

## Result

Validation **PASS** ("all checks pass", run with `--budget 5000`). 3,444 triangles.
Crest 79.2 m = target height — LiDAR max 79.2 m = penthouse (DataSF 2010, parcel 3741032); main roof LiDAR median/mode 72.4 m; OSM 81 m not used.

## Deliverables

- `build_201_spear_street.py` — deterministic build (`blender -b --python build_201_spear_street.py`)
- `201-spear-street.glb`, `201-spear-street.blend`
- `validate_201_spear_street.py` → `validation.json`; `render_201_spear_street.py` → renders below
- Renders: `201-spear-street-aerial-night.png`, `201-spear-street-aerial.png`, `201-spear-street-contact-sheet.png`, `201-spear-street-east.png`, `201-spear-street-north.png`, `201-spear-street-south.png`, `201-spear-street-top.png`, `201-spear-street-west.png`
- `REFERENCE.md` (sources, dimensions, cues, uncertainties)

## Contract (from validation.json, fresh-scene re-import)

| | |
|---|---|
| Triangles | 3,444 |
| Dimensions | 69.4837 x 69.1046 x 79.2 m (world-axis bbox) |
| min Z / XY centre offset | 0.0 / (0.0, 0.0) |
| Objects | 2 |
| Materials | Toy_glassd, Toy_roofd, Toy_sand_Glow, Toy_steel, Toy_stone, Toy_white_Glow |
| Anchor | [-122.3919788, 37.7912423] |

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

- Programmatic saw-tooth plan (116 nodes) matching the OSM pattern, `Toy_stone` prism to 72.4 m (no bottom cap).
- Lobby 0–6 m: dark glass on each tooth's long leg, lit 80%.
- Offices: one dark window per tooth leg per storey pair (7.7 m bands) — per-storey panes would exceed the 5,000 cap.
- Roof deck, 22 × 13 m `Toy_stone` penthouse with steel louvres to 79.2 m, plant cluster, crown line.

All materials are flat `Toy_*` (roughness 0.85, no textures, no alpha). Off-palette: `Toy_glassd`.

## Night state

30% of window slots lit, lit lobby, white crown line on the penthouse. Glow materials: `Toy_sand_Glow`, `Toy_white_Glow`; all laid as thin outward skins over solid faces (738 of 738 glow faces unobstructed outward).

## Iterations

- First build with per-storey windows and a bottom cap: 6,074 tris; dropped the hidden bottom cap and paired the storeys.
- Final: 3,444 tris, all checks pass.

## Gate 3 — approval

Pending: renders sent to David.
