# Phelan Building — build report

Miniature GLB for SF-SIM, Financial District batch (stages 1–2 of
docs/asset-pipeline/ADDRESS-TO-ASSET.md, BATCH mode), built 2026-10-25 from
`docs/asset-plans/phelan-building.md` with the shared kit in `tools/landmark-kit/`.

## Result

Validation **PASS** ("all checks pass", run with `--budget 3000`). 2,748 triangles.
Crest 47.0 m = target height — DataSF 2010 LiDAR median 47.0 m of ring 201006.0000308 (measured; the ring, 4,620 m², also covers lower neighbours — majority 21.7, max 56.3). OSM height 42 (survey) is lower; 11 storeys published.

## Deliverables

- `build_phelan_building.py` — deterministic build (`blender -b --python build_phelan_building.py`)
- `phelan-building.glb`, `phelan-building.blend`
- `validate_phelan_building.py` → `validation.json`; `render_phelan_building.py` → renders below
- Renders: `phelan-building-aerial-night.png`, `phelan-building-aerial.png`, `phelan-building-contact-sheet.png`, `phelan-building-east.png`, `phelan-building-north.png`, `phelan-building-south.png`, `phelan-building-top.png`, `phelan-building-west.png`
- `REFERENCE.md` (sources, dimensions, cues, uncertainties)

## Contract (from validation.json, fresh-scene re-import)

| | |
|---|---|
| Triangles | 2,748 |
| Dimensions | 96.6113 x 82.16 x 47.0 m (world-axis bbox) |
| min Z / XY centre offset | 0.0 / (0.0, 0.0) |
| Objects | 2 |
| Materials | Toy_concrete, Toy_cream, Toy_glassd, Toy_ink, Toy_roofd, Toy_sand_Glow, Toy_steel, Toy_trim |
| Anchor | [-122.4054628, 37.7863863] |

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

- Tall block = OSM ring east of x = −30 m (prow thinned to 5 nodes); `Toy_ink` shop storey 0–5.2 m with lit shopfronts.
- 5.8–40 m `Toy_cream` punched shaft (9 storeys of 3.8 m, panes 3.1 m apart; west face unwindowed where the wing covers it).
- Frieze, arched top storey 40.6–44.2 m, trim cornice band, balustrade to 47 m; dark deck, small penthouse and plant.
- West wing: 11 m cream block with arched panes on the Market side.

All materials are flat `Toy_*` (roughness 0.85, no textures, no alpha). Off-palette: `Toy_glassd`, `Toy_concrete`.

## Night state

Bright shopfronts all round the base, scattered lit office windows. Glow materials: `Toy_sand_Glow`; all laid as thin outward skins over solid faces (462 of 462 glow faces unobstructed outward).

## Iterations

- First draft 4,332 tris (over the 3,000 cap): wider window spacing, plain cornice band, prow thinned from 12 to 5 nodes, no bevels on stacked prisms → 2,748.

## Gate 3 — approval

Pending: renders sent to David.
