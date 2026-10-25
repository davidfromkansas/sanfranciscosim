# Shell Building (100 Bush Street) — asset report

## Result

**PASS** — `100-bush-street.glb` meets the landmark contract: the kit validator
(`tools/landmark-kit/validate.py`, Blender 5.2.3 LTS) factory-reset the scene, re-imported only the
exported GLB and printed "all checks pass". `validation.json` is the machine-readable authority.
Not yet integrated: the manifest, `pipeline/lib/landmarks.mjs` and app code are untouched (the lead integrates the batch).

## Deliverables

- `build_100_bush_street.py` — deterministic build (kit helpers in `tools/landmark-kit/toykit.py`)
- `100-bush-street.glb`, `100-bush-street.blend` — export and authoring scene
- `validate_100_bush_street.py`, `render_100_bush_street.py` — thin wrappers around the kit scripts with this building's arguments
- `validation.json` — full machine report
- `100-bush-street-{north,east,south,west,top,aerial,aerial-night}.png`, `100-bush-street-contact-sheet.png`
- `REFERENCE.md` — sources, dimensions, orientation, cues. Rebuild: run build, validate, render (`-- --samples 16`) with `blender -b --python` from this folder.

## Contract results

| Check | Result | Evidence |
|---|---|---|
| Crest = target height | PASS | max Z 115.22 m = 115.22 m |
| Plausible metre dimensions | PASS | 48.3073 x 52.1586 x 115.22 m |
| Base at Z 0 | PASS | min Z 0.0 m |
| Centred in XY | PASS | offset [0.0, 0.0] m |
| Triangle budget (batch cap) | PASS | 2,760 / 5,000 |
| No image textures | PASS | 0 images |
| No transparency | PASS | all alpha 1.0 |
| Flat `Toy_*` materials | PASS | 7 `Toy_*` materials, no violations |
| Has night glow | PASS | `Toy_sand_Glow` |
| No cameras / lights | PASS | 0 / 0 |
| No animation / skin / constraints | PASS | 0 / 0 / 0 |
| Transforms applied | PASS | 2 mesh objects at identity |
| No negative scales | PASS | none |
| Normals outward (signed volume) | PASS | inverted objects: 0 |
| Normals outward (ray residual) | PASS | 0 flipped of 20,832 first hits |
| Glow skins face outward | PASS | 851 / 852 unobstructed |
| No degenerate geometry | PASS | 0 degenerate triangles |
| No unexpected objects | PASS | none |

## Geometry and materials

- Triangles: **2,760** (body 1,908, night glow 852); budget 5,000 (batch cap)
- Dimensions: **[48.3073, 52.1586, 115.22] m**; anchor **[-122.3999801, 37.7915717]**; target height **115.22 m**; category `3` (Office)
- Materials: `Toy_cream`, `Toy_glassd`, `Toy_roofd`, `Toy_sand_Glow`, `Toy_steel`, `Toy_stone`, `Toy_terracotta`

- Plan `tk.rect(36.8, 41.4)` on yaw 8.7 deg.
- Base 0-13.5 m `Toy_terracotta`: dark shopfronts, round-headed upper windows, cream cornice.
- Wings to 76 m on the full plan; tower 28 x 30 m to 96 m; chamfered tiers to 104 and 110 m; lantern to 115.22 m.
- Each block: terracotta prism + full-height `Toy_glassd` window strips every 2.5 m + scattered lit panes.
- Finials (6-sided cones) at the tier corners; sand glow rings floodlight the two upper tiers.

## Night state

- `Toy_sand_Glow`: lit shopfronts, scattered office panes, floodlit crown tiers.

## Iterations

- First build passed validation at 2,760 tris; no changes needed after review.

## Gate 3 — approval

Pending: renders sent to David.
