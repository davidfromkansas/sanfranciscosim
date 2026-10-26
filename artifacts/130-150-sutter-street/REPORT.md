# Hallidie Building — build report

Miniature GLB for SF-SIM, Financial District batch (stages 1–2 of
docs/asset-pipeline/ADDRESS-TO-ASSET.md, BATCH mode), built 2026-10-25 from
`docs/asset-plans/130-150-sutter-street.md` with the shared kit in `tools/landmark-kit/`.

## Result

Validation **PASS** ("all checks pass", run with `--budget 3000`). 1,182 triangles.
Crest 30.3 m = target height — LiDAR median roof 30.3 m (DataSF 2010, parcel 0288027); OSM 30 m; the list's 34.2 m was a LiDAR peak.

## Deliverables

- `build_130_150_sutter_street.py` — deterministic build (`blender -b --python build_130_150_sutter_street.py`)
- `130-150-sutter-street.glb`, `130-150-sutter-street.blend`
- `validate_130_150_sutter_street.py` → `validation.json`; `render_130_150_sutter_street.py` → renders below
- Renders: `130-150-sutter-street-aerial-night.png`, `130-150-sutter-street-aerial.png`, `130-150-sutter-street-contact-sheet.png`, `130-150-sutter-street-east.png`, `130-150-sutter-street-north.png`, `130-150-sutter-street-south.png`, `130-150-sutter-street-top.png`, `130-150-sutter-street-west.png`
- `REFERENCE.md` (sources, dimensions, cues, uncertainties)

## Contract (from validation.json, fresh-scene re-import)

| | |
|---|---|
| Triangles | 1,182 |
| Dimensions | 47.1872 x 55.7648 x 30.3 m (world-axis bbox) |
| min Z / XY centre offset | 0.0 / (0.0, 0.0) |
| Objects | 2 |
| Materials | Toy_glassd, Toy_glassl, Toy_gold, Toy_navy, Toy_roofd, Toy_sand, Toy_sand_Glow, Toy_steel, Toy_stone, Toy_white_Glow |
| Anchor | [-122.4030681, 37.790212] |

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

- Body: `Toy_sand` prism on the 6-node plan to 28.3 m, rear-court windows only.
- Front: `Toy_navy` frame slab 5.0–27.6 m with `Toy_glassl` panes on a 1.75 m grid (mezzanine, four office floors, top floor).
- Storefront: inset `Toy_glassd` with a warm lit band.
- Four `Toy_gold` bands, a navy cornice with gold cresting and 15 pyramid finials (centre one to 30.3 m).
- Eight gold cylinder balconies (two stacks of four) and gold side jambs.

All materials are flat `Toy_*` (roughness 0.85, no textures, no alpha). Off-palette: `Toy_glassd` (storefront only).

## Night state

Lit panes behind the glass grid (45%, clear of the balconies), lit storefront, white cornice strip. Glow materials: `Toy_sand_Glow`, `Toy_white_Glow`; all laid as thin outward skins over solid faces (60 of 60 glow faces unobstructed outward).

## Iterations

- Draft had the glass front on the north face; the Sutter centreline check moved it to the south face.
- Lit panes behind the balconies failed the glow-outward check: the lit area was narrowed to clear them and the cornice glow quad flipped.
- Final: 1,182 tris, all checks pass.

## Gate 3 — approval

Pending: renders sent to David.
