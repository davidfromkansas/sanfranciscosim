# Two Embarcadero Center — asset report

## Result

**PASS** — `embarcadero-center-2.glb` meets the landmark contract: the kit validator
(`tools/landmark-kit/validate.py`, Blender 5.2.3 LTS) factory-reset the scene, re-imported only the
exported GLB and printed "all checks pass". `validation.json` is the machine-readable authority.
Not yet integrated: the manifest, `pipeline/lib/landmarks.mjs` and app code are untouched (the lead integrates the batch).

## Deliverables

- `build_embarcadero_center_2.py` — deterministic build (kit helpers in `tools/landmark-kit/toykit.py`)
- `embarcadero-center-2.glb`, `embarcadero-center-2.blend` — export and authoring scene
- `validate_embarcadero_center_2.py`, `render_embarcadero_center_2.py` — thin wrappers around the kit scripts with this building's arguments
- `validation.json` — full machine report
- `embarcadero-center-2-{north,east,south,west,top,aerial,aerial-night}.png`, `embarcadero-center-2-contact-sheet.png`
- `REFERENCE.md` — sources, dimensions, orientation, cues. Rebuild: run build, validate, render (`-- --samples 16`) with `blender -b --python` from this folder.

## Contract results

| Check | Result | Evidence |
|---|---|---|
| Crest = target height | PASS | max Z 126.0 m = 126.0 m |
| Plausible metre dimensions | PASS | 96.0272 x 57.6816 x 126.0 m |
| Base at Z 0 | PASS | min Z 0.0 m |
| Centred in XY | PASS | offset [0.0, 0.0] m |
| Triangle budget (batch cap) | PASS | 4,316 / 5,000 |
| No image textures | PASS | 0 images |
| No transparency | PASS | all alpha 1.0 |
| Flat `Toy_*` materials | PASS | 11 `Toy_*` materials, no violations |
| Has night glow | PASS | `Toy_glassl_Glow`, `Toy_sand_Glow` |
| No cameras / lights | PASS | 0 / 0 |
| No animation / skin / constraints | PASS | 0 / 0 / 0 |
| Transforms applied | PASS | 2 mesh objects at identity |
| No negative scales | PASS | none |
| Normals outward (signed volume) | PASS | inverted objects: 0 |
| Normals outward (ray residual) | PASS | 3 flipped of 21,318 first hits |
| Glow skins face outward | PASS | 990 / 990 unobstructed |
| No degenerate geometry | PASS | 0 degenerate triangles |
| No unexpected objects | PASS | none |

## Geometry and materials

- Triangles: **4,316** (body 3,326, night glow 990); budget 5,000 (batch cap)
- Dimensions: **[96.0272, 57.6816, 126.0] m**; anchor **[-122.3985117, 37.7949992]**; target height **126.0 m**; category `3` (Office)
- Materials: `Toy_concrete`, `Toy_cream`, `Toy_glass`, `Toy_glassd`, `Toy_glassl_Glow`, `Toy_leafd`, `Toy_roofd`, `Toy_sand`, `Toy_sand_Glow`, `Toy_steel`, `Toy_stone`

- Same recipe and helper as Three Embarcadero Center, with this polygon's strips.
- Strip ranks clamp at the lowest tier, so the 5th west strip still rises to 113 m.
- Concrete podium 0-10 m with lit shopfronts and a hedge edge; penthouse to 126 m.

## Night state

- `Toy_sand_Glow`: shopfronts and office panes.
- `Toy_glassl_Glow`: crown line.

## Iterations

- First build dropped the fourth-ranked west strip entirely (rank > 2); ranks now clamp to the lowest tier. Steps deepened to 5/10 storeys and mid-tier caps removed as on Three EC. 4,316 tris, all checks pass.

## Gate 3 — approval

Approved by David on 2026-10-26 (renders sent as twelve day/night overview sheets): "approve all".

## Stage 4 — optimize

Shipped as `app/public/sf-assets/landmarks/embarcadero-center-2.glb`, meshopt-compressed with the intake flags of `pipeline/compress-assets.mjs` (`gltfpack -c -km -kn -noq`): **233 KB → 97 KB** (58% smaller). Geometry is unchanged. Kit assets are already one body mesh and one glow mesh, so the Blender cleanup pass and the limited dissolve are skipped, as for the Transbay batch. Gate G3 (three.js GLTFLoader round-trip with MeshoptDecoder, `tools/glb-optimize/g3check`) passes.
