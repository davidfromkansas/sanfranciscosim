# Stevenson Place (71 Stevenson Street) — asset report

## Result

**PASS** — `stevenson-place.glb` meets the landmark contract: the kit validator
(`tools/landmark-kit/validate.py`, Blender 5.2.3 LTS) factory-reset the scene, re-imported only the
exported GLB and printed "all checks pass". `validation.json` is the machine-readable authority.
Not yet integrated: the manifest, `pipeline/lib/landmarks.mjs` and app code are untouched (the lead integrates the batch).

## Deliverables

- `build_stevenson_place.py` — deterministic build (kit helpers in `tools/landmark-kit/toykit.py`)
- `stevenson-place.glb`, `stevenson-place.blend` — export and authoring scene
- `validate_stevenson_place.py`, `render_stevenson_place.py` — thin wrappers around the kit scripts with this building's arguments
- `validation.json` — full machine report
- `stevenson-place-{north,east,south,west,top,aerial,aerial-night}.png`, `stevenson-place-contact-sheet.png`
- `REFERENCE.md` — sources, dimensions, orientation, cues. Rebuild: run build, validate, render (`-- --samples 16`) with `blender -b --python` from this folder.

## Contract results

| Check | Result | Evidence |
|---|---|---|
| Crest = target height | PASS | max Z 103.0 m = 103.0 m |
| Plausible metre dimensions | PASS | 67.0601 x 58.2913 x 103.0 m |
| Base at Z 0 | PASS | min Z 0.0 m |
| Centred in XY | PASS | offset [0.0, 0.0] m |
| Triangle budget (batch cap) | PASS | 4,414 / 5,000 |
| No image textures | PASS | 0 images |
| No transparency | PASS | all alpha 1.0 |
| Flat `Toy_*` materials | PASS | 9 `Toy_*` materials, no violations |
| Has night glow | PASS | `Toy_sand_Glow`, `Toy_white_Glow` |
| No cameras / lights | PASS | 0 / 0 |
| No animation / skin / constraints | PASS | 0 / 0 / 0 |
| Transforms applied | PASS | 2 mesh objects at identity |
| No negative scales | PASS | none |
| Normals outward (signed volume) | PASS | inverted objects: 0 |
| Normals outward (ray residual) | PASS | 3 flipped of 20,597 first hits |
| Glow skins face outward | PASS | 678 / 678 unobstructed |
| No degenerate geometry | PASS | 0 degenerate triangles |
| No unexpected objects | PASS | none |

## Geometry and materials

- Triangles: **4,414** (body 3,736, night glow 678); budget 5,000 (batch cap)
- Dimensions: **[67.0601, 58.2913, 103.0] m**; anchor **[-122.3997358, 37.7893616]**; target height **103.0 m**; category `3` (Office)
- Materials: `Toy_cream`, `Toy_glassd`, `Toy_granite`, `Toy_ink`, `Toy_roofd`, `Toy_sand_Glow`, `Toy_steel`, `Toy_stone`, `Toy_white_Glow`

- Base: OSM polygon (9 nodes), `tk.punched_block` in `Toy_granite`, cream band courses.
- Shaft 19-87.4 m: `notch_rect(38, 28, 3.5)` granite prism, dark panes, cream piers every 3.4 m, lit panes.
- Upper 87.4-95 m: `notch_rect(30, 24, 4)` cream punched block.
- Crown: cream wall 95-98 m with dark louvres, frustum to a 2 x 14 m ridge at 103 m; white glow line at its foot.

## Night state

- `Toy_sand_Glow`: base and shaft panes.
- `Toy_white_Glow`: crown line.

## Iterations

- First built to the LiDAR 106 m; corrected to the published 103 m (tiers lowered 1.6-2 m). Louvres first sat inside the upper block; moved onto a taller crown wall. 4,414 tris, all checks pass.

## Gate 3 — approval

Pending: renders sent to David.
