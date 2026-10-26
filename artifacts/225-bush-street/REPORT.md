# 225 Bush Street (Standard Oil Building) — asset report

## Result

**PASS** — `225-bush-street.glb` meets the landmark contract: the kit validator
(`tools/landmark-kit/validate.py`, Blender 5.2.3 LTS) factory-reset the scene, re-imported only the
exported GLB and printed "all checks pass". `validation.json` is the machine-readable authority.
Not yet integrated: the manifest, `pipeline/lib/landmarks.mjs` and app code are untouched (the lead integrates the batch).

## Deliverables

- `build_225_bush_street.py` — deterministic build (kit helpers in `tools/landmark-kit/toykit.py`)
- `225-bush-street.glb`, `225-bush-street.blend` — export and authoring scene
- `validate_225_bush_street.py`, `render_225_bush_street.py` — thin wrappers around the kit scripts with this building's arguments
- `validation.json` — full machine report
- `225-bush-street-{north,east,south,west,top,aerial,aerial-night}.png`, `225-bush-street-contact-sheet.png`
- `REFERENCE.md` — sources, dimensions, orientation, cues. Rebuild: run build, validate, render (`-- --samples 16`) with `blender -b --python` from this folder.

## Contract results

| Check | Result | Evidence |
|---|---|---|
| Crest = target height | PASS | max Z 100.0 m = 100.0 m |
| Plausible metre dimensions | PASS | 94.8698 x 60.9589 x 100.0 m |
| Base at Z 0 | PASS | min Z 0.0 m |
| Centred in XY | PASS | offset [0.0, 0.0] m |
| Triangle budget (batch cap) | PASS | 4,804 / 5,000 |
| No image textures | PASS | 0 images |
| No transparency | PASS | all alpha 1.0 |
| Flat `Toy_*` materials | PASS | 7 `Toy_*` materials, no violations |
| Has night glow | PASS | `Toy_sand_Glow` |
| No cameras / lights | PASS | 0 / 0 |
| No animation / skin / constraints | PASS | 0 / 0 / 0 |
| Transforms applied | PASS | 2 mesh objects at identity |
| No negative scales | PASS | none |
| Normals outward (signed volume) | PASS | inverted objects: 0 |
| Normals outward (ray residual) | PASS | 0 flipped of 21,025 first hits |
| Glow skins face outward | PASS | 840 / 840 unobstructed |
| No degenerate geometry | PASS | 0 degenerate triangles |
| No unexpected objects | PASS | none |

## Geometry and materials

- Triangles: **4,804** (body 3,964, night glow 840); budget 5,000 (batch cap)
- Dimensions: **[94.8698, 60.9589, 100.0] m**; anchor **[-122.4013094, 37.7908371]**; target height **100.0 m**; category `3` (Office)
- Materials: `Toy_cream`, `Toy_glassd`, `Toy_roofd`, `Toy_sand_Glow`, `Toy_steel`, `Toy_stone`, `Toy_terracotta`

- Plan `tk.rect(83.6, 43.0)` on yaw 8.8 deg.
- Arcade 0-9.5 m: `Toy_stone` with round-headed `Toy_glassd` openings and lit arches.
- Mezzanine to 17 m + cream band course; shaft to 88 m: `tk.punched_block`, 18 storeys, windows every 4.6 m.
- Loggia 88-95 m: dark recess, lit ring, cream columns every 4.2 m; cornice to 97.6 m; terracotta tile edge.
- Two stone plant penthouses to 100 m and a plant cluster between them.

## Night state

- `Toy_sand_Glow`: arcade arches, office panes, the loggia ring.

## Iterations

- Draft 5,070 tris; shaft window spacing widened 4.2 -> 4.6 m: 4,804 tris, all checks pass.

## Gate 3 — approval

Approved by David on 2026-10-26 (renders sent as twelve day/night overview sheets): "approve all".

## Stage 4 — optimize

Shipped as `app/public/sf-assets/landmarks/225-bush-street.glb`, meshopt-compressed with the intake flags of `pipeline/compress-assets.mjs` (`gltfpack -c -km -kn -noq`): **251 KB → 100 KB** (60% smaller). Geometry is unchanged. Kit assets are already one body mesh and one glow mesh, so the Blender cleanup pass and the limited dissolve are skipped, as for the Transbay batch. Gate G3 (three.js GLTFLoader round-trip with MeshoptDecoder, `tools/glb-optimize/g3check`) passes.
