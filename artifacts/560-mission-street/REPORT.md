# JPMorgan Chase Building (560 Mission Street) — asset report

## Result

**PASS** — `560-mission-street.glb` meets the landmark contract: the kit validator
(`tools/landmark-kit/validate.py`, Blender 5.2.3 LTS) factory-reset the scene, re-imported only the
exported GLB and printed "all checks pass". `validation.json` is the machine-readable authority.
Not yet integrated: the manifest, `pipeline/lib/landmarks.mjs` and app code are untouched (the lead integrates the batch).

## Deliverables

- `build_560_mission_street.py` — deterministic build (kit helpers in `tools/landmark-kit/toykit.py`)
- `560-mission-street.glb`, `560-mission-street.blend` — export and authoring scene
- `validate_560_mission_street.py`, `render_560_mission_street.py` — thin wrappers around the kit scripts with this building's arguments
- `validation.json` — full machine report
- `560-mission-street-{north,east,south,west,top,aerial,aerial-night}.png`, `560-mission-street-contact-sheet.png`
- `REFERENCE.md` — sources, dimensions, orientation, cues. Rebuild: run build, validate, render (`-- --samples 16`) with `blender -b --python` from this folder.

## Contract results

| Check | Result | Evidence |
|---|---|---|
| Crest = target height | PASS | max Z 128.02 m = 128.02 m |
| Plausible metre dimensions | PASS | 85.1472 x 84.5771 x 128.02 m |
| Base at Z 0 | PASS | min Z 0.0 m |
| Centred in XY | PASS | offset [0.0, 0.0] m |
| Triangle budget (batch cap) | PASS | 4,832 / 5,000 |
| No image textures | PASS | 0 images |
| No transparency | PASS | all alpha 1.0 |
| Flat `Toy_*` materials | PASS | 11 `Toy_*` materials, no violations |
| Has night glow | PASS | `Toy_sand_Glow`, `Toy_white_Glow` |
| No cameras / lights | PASS | 0 / 0 |
| No animation / skin / constraints | PASS | 0 / 0 / 0 |
| Transforms applied | PASS | 2 mesh objects at identity |
| No negative scales | PASS | none |
| Normals outward (signed volume) | PASS | inverted objects: 0 |
| Normals outward (ray residual) | PASS | 1 flipped of 18,920 first hits |
| Glow skins face outward | PASS | 820 / 828 unobstructed |
| No degenerate geometry | PASS | 0 degenerate triangles |
| No unexpected objects | PASS | none |

## Geometry and materials

- Triangles: **4,832** (body 4,004, night glow 828); budget 5,000 (batch cap)
- Dimensions: **[85.1472, 84.5771, 128.02] m**; anchor **[-122.3995478, 37.7888279]**; target height **128.02 m**; category `3` (Office)
- Materials: `Toy_glassd`, `Toy_glassl`, `Toy_ink`, `Toy_leaf`, `Toy_roofd`, `Toy_rust`, `Toy_sand_Glow`, `Toy_sky`, `Toy_steel`, `Toy_stone`, `Toy_white_Glow`

- Plan `tk.rect(54.6, 37.6)` on yaw -44.3 deg.
- Base 0-9 m: recessed `Toy_glassd` lobby, `Toy_ink` columns every 9 m, lit ring; black transfer band.
- Shaft 9.6-122 m in two `tk.shaft` runs (9 + 19 storeys) split by an `Toy_ink` ledge; `Toy_glassl` glass, ink bands and fins every 4.1 m.
- Crown: ink posts, a rail and a top frame ring to 128.02 m round a deck and plant; white crown light.
- Plaza (NW, Mission side): stone paving, sky pool, steel ring sculpture, bamboo trees.

## Night state

- `Toy_sand_Glow`: lobby ring and office panes.
- `Toy_white_Glow`: crown light inside the frame.

## Iterations

- Draft 5,414 tris with fins every 3.1 m; widened to 4.1 m: 4,832 tris, all checks pass.

## Gate 3 — approval

Approved by David on 2026-10-26 (renders sent as twelve day/night overview sheets): "approve all".

## Stage 4 — optimize

Shipped as `app/public/sf-assets/landmarks/560-mission-street.glb`, meshopt-compressed with the intake flags of `pipeline/compress-assets.mjs` (`gltfpack -c -km -kn -noq`): **252 KB → 118 KB** (53% smaller). Geometry is unchanged. Kit assets are already one body mesh and one glow mesh, so the Blender cleanup pass and the limited dissolve are skipped, as for the Transbay batch. Gate G3 (three.js GLTFLoader round-trip with MeshoptDecoder, `tools/glb-optimize/g3check`) passes.
