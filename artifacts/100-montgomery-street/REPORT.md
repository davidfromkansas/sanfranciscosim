# 100 Montgomery Street (Equitable Life Building) — asset report

## Result

**PASS** — `100-montgomery-street.glb` meets the landmark contract: the kit validator
(`tools/landmark-kit/validate.py`, Blender 5.2.3 LTS) factory-reset the scene, re-imported only the
exported GLB and printed "all checks pass". `validation.json` is the machine-readable authority.
Not yet integrated: the manifest, `pipeline/lib/landmarks.mjs` and app code are untouched (the lead integrates the batch).

## Deliverables

- `build_100_montgomery_street.py` — deterministic build (kit helpers in `tools/landmark-kit/toykit.py`)
- `100-montgomery-street.glb`, `100-montgomery-street.blend` — export and authoring scene
- `validate_100_montgomery_street.py`, `render_100_montgomery_street.py` — thin wrappers around the kit scripts with this building's arguments
- `validation.json` — full machine report
- `100-montgomery-street-{north,east,south,west,top,aerial,aerial-night}.png`, `100-montgomery-street-contact-sheet.png`
- `REFERENCE.md` — sources, dimensions, orientation, cues. Rebuild: run build, validate, render (`-- --samples 16`) with `blender -b --python` from this folder.

## Contract results

| Check | Result | Evidence |
|---|---|---|
| Crest = target height | PASS | max Z 107.9 m = 107.9 m |
| Plausible metre dimensions | PASS | 61.7195 x 46.1684 x 107.9 m |
| Base at Z 0 | PASS | min Z 0.0 m |
| Centred in XY | PASS | offset [0.0, 0.0] m |
| Triangle budget (batch cap) | PASS | 2,156 / 5,000 |
| No image textures | PASS | 0 images |
| No transparency | PASS | all alpha 1.0 |
| Flat `Toy_*` materials | PASS | 8 `Toy_*` materials, no violations |
| Has night glow | PASS | `Toy_sand_Glow`, `Toy_white_Glow` |
| No cameras / lights | PASS | 0 / 0 |
| No animation / skin / constraints | PASS | 0 / 0 / 0 |
| Transforms applied | PASS | 2 mesh objects at identity |
| No negative scales | PASS | none |
| Normals outward (signed volume) | PASS | inverted objects: 0 |
| Normals outward (ray residual) | PASS | 0 flipped of 19,919 first hits |
| Glow skins face outward | PASS | 448 / 448 unobstructed |
| No degenerate geometry | PASS | 0 degenerate triangles |
| No unexpected objects | PASS | none |

## Geometry and materials

- Triangles: **2,156** (body 1,708, night glow 448); budget 5,000 (batch cap)
- Dimensions: **[61.7195, 46.1684, 107.9] m**; anchor **[-122.4018706, 37.7903435]**; target height **107.9 m**; category `3` (Office)
- Materials: `Toy_glassd`, `Toy_glassg`, `Toy_roofd`, `Toy_sand_Glow`, `Toy_steel`, `Toy_stone`, `Toy_white`, `Toy_white_Glow`

- Plan `tk.rect(51.8, 33.4)` on yaw 8.3 deg.
- Base 0-9 m `Toy_white` with two rows of big punched windows.
- Shaft 9-103.1 m: `tk.shaft` 23 storeys, `Toy_glassg` with thin `Toy_steel` spandrels and 2 m `Toy_white` piers every 6.4 m.
- Marble parapet ring, dark deck, `Toy_stone` penthouse 22 x 14 m to the crest, small plant cluster.

## Night state

- `Toy_sand_Glow`: base windows and office panes.
- `Toy_white_Glow`: line under the parapet.

## Iterations

- First build passed at 2,156 tris (crest first set at 111.5 m with the penthouse on top; lowered so the crest equals the published 107.9 m).

## Gate 3 — approval

Approved by David on 2026-10-26 (renders sent as twelve day/night overview sheets): "approve all".

## Stage 4 — optimize

Shipped as `app/public/sf-assets/landmarks/100-montgomery-street.glb`, meshopt-compressed with the intake flags of `pipeline/compress-assets.mjs` (`gltfpack -c -km -kn -noq`): **112 KB → 54 KB** (52% smaller). Geometry is unchanged. Kit assets are already one body mesh and one glow mesh, so the Blender cleanup pass and the limited dissolve are skipped, as for the Transbay batch. Gate G3 (three.js GLTFLoader round-trip with MeshoptDecoder, `tools/glb-optimize/g3check`) passes.
