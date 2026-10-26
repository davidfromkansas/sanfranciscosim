# Mills Building — build report

Miniature GLB for SF-SIM, Financial District batch (stages 1–2 of
docs/asset-pipeline/ADDRESS-TO-ASSET.md, BATCH mode), built 2026-10-26 from
`docs/asset-plans/mills-building.md` with the shared kit in `tools/landmark-kit/`.

## Result

Validation **PASS** ("all checks pass", run with `--budget 3000`). 2,929 triangles.
Crest 47.0 m = target height — published 47 m (Wikipedia text; infobox roof 46.94 m). DataSF 2010 LiDAR: majority 43.65 m, median 44.8 m = the roof deck inside the cornice/parapet (measured).

## Deliverables

- `build_mills_building.py` — deterministic build (`blender -b --python build_mills_building.py`)
- `mills-building.glb`, `mills-building.blend`
- `validate_mills_building.py` → `validation.json`; `render_mills_building.py` → renders below
- Renders: `mills-building-aerial-night.png`, `mills-building-aerial.png`, `mills-building-contact-sheet.png`, `mills-building-east.png`, `mills-building-north.png`, `mills-building-south.png`, `mills-building-top.png`, `mills-building-west.png`
- `REFERENCE.md` (sources, dimensions, cues, uncertainties)

## Contract (from validation.json, fresh-scene re-import)

| | |
|---|---|
| Triangles | 2,929 |
| Dimensions | 95.6553 x 60.2391 x 47.0 m (world-axis bbox) |
| min Z / XY centre offset | 0.0 / (0.0, 0.0) |
| Objects | 2 |
| Materials | Toy_cream, Toy_glassd, Toy_ink, Toy_leaf, Toy_leafd, Toy_roofd, Toy_rust, Toy_sand_Glow, Toy_steel, Toy_stone, Toy_terracotta, Toy_white |
| Anchor | [-122.4018804, 37.7913406] |

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

- Plan: `tk.ccw` of the OSM outer ring, clipped 8 cm west of the Mills Tower party line.
- 0–10.4 m `Toy_white` marble base with storefront and second-floor panes (lit storefronts at night); `Toy_cream` belt course.
- 10.4–43.8 m `Toy_terracotta` shaft, eight storeys of 4.175 m; panes every 3.6 m on S/W/N.
- Arcade on S and W: `Toy_stone` colonnettes every 3.6 m from storey 4 to the arches; round-headed `Toy_glassd` arches in storey 8.
- `Toy_cream` frieze band, attic band, two-step cornice at 43.8–45.4 m; `Toy_terracotta` parapet to 47.0 m.
- Montgomery entrance: `Toy_cream` surround 9 m wide × 11.4 m with a dark round arch and a lit inner arch.
- Roof: dark deck at 45.5 m, the two light courts as `Toy_ink` wells with brick coping, a low plant cluster and stair house.
- Sidewalk on Bush and Montgomery only, two street trees on Montgomery.

All materials are flat `Toy_*` (roughness 0.85, no textures, no alpha). Off-palette: `Toy_glassd`, `Toy_terracotta` (documented in the kit).

## Night state

Lit storefronts (70%), scattered lit offices (25–30%), lit inner entrance arch, some lit arcade arches and a warm wash line under the cornice on the street faces. Glow materials: `Toy_sand_Glow`; all laid as thin outward skins over solid faces (372 of 374 glow faces unobstructed outward).

## Iterations

- Draft: 3 degenerate triangles and 12 bad loop normals — the frieze/attic bands had zero width along the clipped party wall; outer loops now stop 2 cm short of the line instead of 8 cm. 2,963 tris, PASS.
- Render 1: the Montgomery entrance arch was hidden (coplanar with the portal face, and `tk.edges` re-ordered the helper triangle); arch moved 6 cm proud and picked by normal. Roof plant enlarged, base panes limited to the street faces. 2,929 tris, PASS.

## Gate 3 — approval

Pending: renders sent to David.
