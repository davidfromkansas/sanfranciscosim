# The Paramount (680 Mission Street) — asset report

## Result

**PASS** — `paramount.glb` meets the landmark contract: the kit validator
(`tools/landmark-kit/validate.py`, Blender 5.2.3 LTS) factory-reset the scene, re-imported only the
exported GLB and printed "all checks pass". `validation.json` is the machine-readable authority.
Not yet integrated: the manifest, `pipeline/lib/landmarks.mjs` and app code are untouched (the lead integrates the batch).

## Deliverables

- `build_paramount.py` — deterministic build (kit helpers in `tools/landmark-kit/toykit.py`)
- `paramount.glb`, `paramount.blend` — export and authoring scene
- `validate_paramount.py`, `render_paramount.py` — thin wrappers around the kit scripts with this building's arguments
- `validation.json` — full machine report
- `paramount-{north,east,south,west,top,aerial,aerial-night}.png`, `paramount-contact-sheet.png`
- `REFERENCE.md` — sources, dimensions, orientation, cues. Rebuild: run build, validate, render (`-- --samples 16`) with `blender -b --python` from this folder.

## Contract results

| Check | Result | Evidence |
|---|---|---|
| Crest = target height | PASS | max Z 128.0 m = 128.0 m |
| Plausible metre dimensions | PASS | 76.3795 x 70.5152 x 128.0 m |
| Base at Z 0 | PASS | min Z 0.0 m |
| Centred in XY | PASS | offset [0.0, 0.0] m |
| Triangle budget (batch cap) | PASS | 3,898 / 5,000 |
| No image textures | PASS | 0 images |
| No transparency | PASS | all alpha 1.0 |
| Flat `Toy_*` materials | PASS | 10 `Toy_*` materials, no violations |
| Has night glow | PASS | `Toy_sand_Glow`, `Toy_white_Glow` |
| No cameras / lights | PASS | 0 / 0 |
| No animation / skin / constraints | PASS | 0 / 0 / 0 |
| Transforms applied | PASS | 2 mesh objects at identity |
| No negative scales | PASS | none |
| Normals outward (signed volume) | PASS | inverted objects: 0 |
| Normals outward (ray residual) | PASS | 0 flipped of 21,240 first hits |
| Glow skins face outward | PASS | 1102 / 1102 unobstructed |
| No degenerate geometry | PASS | 0 degenerate triangles |
| No unexpected objects | PASS | none |

## Geometry and materials

- Triangles: **3,898** (body 2,796, night glow 1,102); budget 5,000 (batch cap)
- Dimensions: **[76.3795, 70.5152, 128.0] m**; anchor **[-122.4020234, 37.7867030]**; target height **128.0 m**; category `2` (Apartments)
- Materials: `Toy_concrete`, `Toy_glass`, `Toy_glassd`, `Toy_leaf`, `Toy_roofd`, `Toy_rust`, `Toy_sand_Glow`, `Toy_steel`, `Toy_stone`, `Toy_white_Glow`

- Plan = OSM polygon in the local frame (6 nodes).
- Podium 0-11 m: dark retail glass, stone piers, lit ring, stone band.
- Lower block 11-92 m: `tk.shaft` 26 storeys, `Toy_glass` ribbons + 1.45 m `Toy_stone` bands.
- Central slab to 124.6 m (10 storeys, `Toy_concrete` bands); recessed lit top storey; `Toy_concrete` cap 126.6-128 m overhanging 2.4 m.
- Plant on both shoulders; four street trees on Mission (NW).

## Night state

- `Toy_sand_Glow`: retail ring and apartment panes.
- `Toy_white_Glow`: the recessed top storey under the cap.

## Iterations

- First build (3,916 tris) put Mission on the SE face and the slab across it; the address puts Mission on the NW, so the slab was turned to run NE-SW with shoulders on the Mission and rear sides and the trees moved to Mission. 3,898 tris, all checks pass.

## Gate 3 — approval

Approved by David on 2026-10-26 (renders sent as twelve day/night overview sheets): "approve all".

## Stage 4 — optimize

Shipped as `app/public/sf-assets/landmarks/paramount.glb`, meshopt-compressed with the intake flags of `pipeline/compress-assets.mjs` (`gltfpack -c -km -kn -noq`): **195 KB → 91 KB** (53% smaller). Geometry is unchanged. Kit assets are already one body mesh and one glow mesh, so the Blender cleanup pass and the limited dissolve are skipped, as for the Transbay batch. Gate G3 (three.js GLTFLoader round-trip with MeshoptDecoder, `tools/glb-optimize/g3check`) passes.
