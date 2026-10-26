# 595 Market Street — asset report

## Result

**PASS** — `595-market-street.glb` meets the landmark contract: the kit validator
(`tools/landmark-kit/validate.py`, Blender 5.2.3 LTS) factory-reset the scene, re-imported only the
exported GLB and printed "all checks pass". `validation.json` is the machine-readable authority.
Not yet integrated: the manifest, `pipeline/lib/landmarks.mjs` and app code are untouched (the lead integrates the batch).

## Deliverables

- `build_595_market_street.py` — deterministic build (kit helpers in `tools/landmark-kit/toykit.py`)
- `595-market-street.glb`, `595-market-street.blend` — export and authoring scene
- `validate_595_market_street.py`, `render_595_market_street.py` — thin wrappers around the kit scripts with this building's arguments
- `validation.json` — full machine report
- `595-market-street-{north,east,south,west,top,aerial,aerial-night}.png`, `595-market-street-contact-sheet.png`
- `REFERENCE.md` — sources, dimensions, orientation, cues. Rebuild: run build, validate, render (`-- --samples 16`) with `blender -b --python` from this folder.

## Contract results

| Check | Result | Evidence |
|---|---|---|
| Crest = target height | PASS | max Z 125.0 m = 125.0 m |
| Plausible metre dimensions | PASS | 66.3268 x 66.3268 x 125.0 m |
| Base at Z 0 | PASS | min Z 0.0 m |
| Centred in XY | PASS | offset [0.0, 0.0] m |
| Triangle budget (batch cap) | PASS | 3,610 / 5,000 |
| No image textures | PASS | 0 images |
| No transparency | PASS | all alpha 1.0 |
| Flat `Toy_*` materials | PASS | 12 `Toy_*` materials, no violations |
| Has night glow | PASS | `Toy_sand_Glow`, `Toy_white_Glow` |
| No cameras / lights | PASS | 0 / 0 |
| No animation / skin / constraints | PASS | 0 / 0 / 0 |
| Transforms applied | PASS | 2 mesh objects at identity |
| No negative scales | PASS | none |
| Normals outward (signed volume) | PASS | inverted objects: 0 |
| Normals outward (ray residual) | PASS | 0 flipped of 20,842 first hits |
| Glow skins face outward | PASS | 674 / 674 unobstructed |
| No degenerate geometry | PASS | 0 degenerate triangles |
| No unexpected objects | PASS | none |

## Geometry and materials

- Triangles: **3,610** (body 2,936, night glow 674); budget 5,000 (batch cap)
- Dimensions: **[66.3268, 66.3268, 125.0] m**; anchor **[-122.4007917, 37.7892292]**; target height **125.0 m**; category `3` (Office)
- Materials: `Toy_glass`, `Toy_glassd`, `Toy_leaf`, `Toy_leafd`, `Toy_roofd`, `Toy_rust`, `Toy_sand_Glow`, `Toy_steel`, `Toy_stone`, `Toy_trim`, `Toy_white`, `Toy_white_Glow`

- Plan `tk.chamfer_rect(41, 41, 8)` on yaw -45.1 deg.
- Podium: stone, punched dark windows, planted deck, four corner trees.
- Shaft 6.8-117 m: `tk.shaft` 27 storeys, `Toy_glass` + 1.75 m `Toy_white` bands (no fins).
- Screen 117-125 m: `Toy_trim` ring with four steel louvre lines round a dark deck and plant; white crown line.

## Night state

- `Toy_sand_Glow`: podium windows and office panes.
- `Toy_white_Glow`: line under the screen.

## Iterations

- Screen first built as an open-topped prism (inside faces visible from above); rebuilt as a solid ring around a raised deck. 3,610 tris, all checks pass.

## Gate 3 — approval

Approved by David on 2026-10-26 (renders sent as twelve day/night overview sheets): "approve all".

## Stage 4 — optimize

Shipped as `app/public/sf-assets/landmarks/595-market-street.glb`, meshopt-compressed with the intake flags of `pipeline/compress-assets.mjs` (`gltfpack -c -km -kn -noq`): **178 KB → 80 KB** (55% smaller). Geometry is unchanged. Kit assets are already one body mesh and one glow mesh, so the Blender cleanup pass and the limited dissolve are skipped, as for the Transbay batch. Gate G3 (three.js GLTFLoader round-trip with MeshoptDecoder, `tools/glb-optimize/g3check`) passes.
