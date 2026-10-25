# 222 Second Street (LinkedIn) — asset report

## Result

**PASS** — `222-2nd-street.glb` meets the landmark contract: the kit validator
(`tools/landmark-kit/validate.py`, Blender 5.2.3 LTS) factory-reset the scene, re-imported only the
exported GLB and printed "all checks pass". `validation.json` is the machine-readable authority.
Not yet integrated: the manifest, `pipeline/lib/landmarks.mjs` and app code are untouched (the lead integrates the batch).

## Deliverables

- `build_222_2nd_street.py` — deterministic build (kit helpers in `tools/landmark-kit/toykit.py`)
- `222-2nd-street.glb`, `222-2nd-street.blend` — export and authoring scene
- `validate_222_2nd_street.py`, `render_222_2nd_street.py` — thin wrappers around the kit scripts with this building's arguments
- `validation.json` — full machine report
- `222-2nd-street-{north,east,south,west,top,aerial,aerial-night}.png`, `222-2nd-street-contact-sheet.png`
- `REFERENCE.md` — sources, dimensions, orientation, cues. Rebuild: run build, validate, render (`-- --samples 16`) with `blender -b --python` from this folder.

## Contract results

| Check | Result | Evidence |
|---|---|---|
| Crest = target height | PASS | max Z 112.8 m = 112.8 m |
| Plausible metre dimensions | PASS | 76.7918 x 72.6906 x 112.8 m |
| Base at Z 0 | PASS | min Z 0.0 m |
| Centred in XY | PASS | offset [0.0, 0.0] m |
| Triangle budget (batch cap) | PASS | 4,502 / 5,000 |
| No image textures | PASS | 0 images |
| No transparency | PASS | all alpha 1.0 |
| Flat `Toy_*` materials | PASS | 13 `Toy_*` materials, no violations |
| Has night glow | PASS | `Toy_sand_Glow`, `Toy_sky_Glow`, `Toy_white_Glow` |
| No cameras / lights | PASS | 0 / 0 |
| No animation / skin / constraints | PASS | 0 / 0 / 0 |
| Transforms applied | PASS | 2 mesh objects at identity |
| No negative scales | PASS | none |
| Normals outward (signed volume) | PASS | inverted objects: 0 |
| Normals outward (ray residual) | PASS | 0 flipped of 19,871 first hits |
| Glow skins face outward | PASS | 586 / 592 unobstructed |
| No degenerate geometry | PASS | 0 degenerate triangles |
| No unexpected objects | PASS | none |

## Geometry and materials

- Triangles: **4,502** (body 3,910, night glow 592); budget 5,000 (batch cap)
- Dimensions: **[76.7918, 72.6906, 112.8] m**; anchor **[-122.3982516, 37.7863336]**; target height **112.8 m**; category `3` (Office)
- Materials: `Toy_glass`, `Toy_glassd`, `Toy_glassl`, `Toy_leaf`, `Toy_leafd`, `Toy_roofd`, `Toy_rust`, `Toy_sand_Glow`, `Toy_sky`, `Toy_sky_Glow`, `Toy_steel`, `Toy_stone`, `Toy_white_Glow`

- Plan = OSM polygon in the local frame (6 nodes).
- Base 0-16.4 m `Toy_glassd` inset 0.8 m with `Toy_glass` fins every 3.7 m and a lit ring.
- Lower block to 65.6 m: `tk.shaft` 12 storey-groups, `Toy_glassd` + `Toy_glass` bands, `Toy_glassl` fins 3.7 m.
- Upper square 36 m to 106.7 m (10 storeys), then a glass screen ring to 112.8 m round a deck and plant.
- Sky-blue sign + `Toy_sky_Glow` on the NE face at the north corner; terrace plant on the setback; trees on Second.

## Night state

- `Toy_sand_Glow`: lobby ring and office panes.
- `Toy_sky_Glow`: LinkedIn sign.
- `Toy_white_Glow`: crown line.

## Iterations

- Draft 6,074 tris (fins every 1.9 m on the base and 1.8 m on the screen) - over the 5,000 cap.
- Fins thinned to 3.7 m and screen fins dropped: 4,502 tris, all checks pass.

## Gate 3 — approval

Pending: renders sent to David.
