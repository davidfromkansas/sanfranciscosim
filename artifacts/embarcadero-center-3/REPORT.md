# Three Embarcadero Center — asset report

## Result

**PASS** — `embarcadero-center-3.glb` meets the landmark contract: the kit validator
(`tools/landmark-kit/validate.py`, Blender 5.2.3 LTS) factory-reset the scene, re-imported only the
exported GLB and printed "all checks pass". `validation.json` is the machine-readable authority.
Not yet integrated: the manifest, `pipeline/lib/landmarks.mjs` and app code are untouched (the lead integrates the batch).

## Deliverables

- `build_embarcadero_center_3.py` — deterministic build (kit helpers in `tools/landmark-kit/toykit.py`)
- `embarcadero-center-3.glb`, `embarcadero-center-3.blend` — export and authoring scene
- `validate_embarcadero_center_3.py`, `render_embarcadero_center_3.py` — thin wrappers around the kit scripts with this building's arguments
- `validation.json` — full machine report
- `embarcadero-center-3-{north,east,south,west,top,aerial,aerial-night}.png`, `embarcadero-center-3-contact-sheet.png`
- `REFERENCE.md` — sources, dimensions, orientation, cues. Rebuild: run build, validate, render (`-- --samples 16`) with `blender -b --python` from this folder.

## Contract results

| Check | Result | Evidence |
|---|---|---|
| Crest = target height | PASS | max Z 126.0 m = 126.0 m |
| Plausible metre dimensions | PASS | 94.0973 x 58.3978 x 126.0 m |
| Base at Z 0 | PASS | min Z 0.0 m |
| Centred in XY | PASS | offset [0.0, 0.0] m |
| Triangle budget (batch cap) | PASS | 4,204 / 5,000 |
| No image textures | PASS | 0 images |
| No transparency | PASS | all alpha 1.0 |
| Flat `Toy_*` materials | PASS | 11 `Toy_*` materials, no violations |
| Has night glow | PASS | `Toy_glassl_Glow`, `Toy_sand_Glow` |
| No cameras / lights | PASS | 0 / 0 |
| No animation / skin / constraints | PASS | 0 / 0 / 0 |
| Transforms applied | PASS | 2 mesh objects at identity |
| No negative scales | PASS | none |
| Normals outward (signed volume) | PASS | inverted objects: 0 |
| Normals outward (ray residual) | PASS | 2 flipped of 21,305 first hits |
| Glow skins face outward | PASS | 998 / 998 unobstructed |
| No degenerate geometry | PASS | 0 degenerate triangles |
| No unexpected objects | PASS | none |

## Geometry and materials

- Triangles: **4,204** (body 3,206, night glow 998); budget 5,000 (batch cap)
- Dimensions: **[94.0973, 58.3978, 126.0] m**; anchor **[-122.3973647, 37.7951182]**; target height **126.0 m**; category `3` (Office)
- Materials: `Toy_concrete`, `Toy_cream`, `Toy_glass`, `Toy_glassd`, `Toy_glassl_Glow`, `Toy_leafd`, `Toy_roofd`, `Toy_sand`, `Toy_sand_Glow`, `Toy_steel`, `Toy_stone`

- Strips across the short ends measured off the OSM polygon (see `WEST`/`EAST` in the script).
- Three tiers: all strips to 123 - 10 storeys; spine + second strip to -5 storeys; spine and core to 123 m.
- Each tier: `Toy_sand` prism, dark `Toy_glass` slot rows (1.55 m pitch, five-storey groups), scattered lit panes.
- Concrete podium 0-10 m (offset 4 m) with lit shopfronts and a hedge; cream cap ring, deck, penthouse to 126 m.

## Night state

- `Toy_sand_Glow`: shopfronts and office panes.
- `Toy_glassl_Glow`: crown line (as on Four EC).

## Iterations

- First build: 3-storey steps barely read and cream caps at every tier drew false horizontal lines across the long faces. Steps deepened to 5/10 storeys, mid-tier caps removed; crest set from 125.6 to the published 126 m. 4,204 tris, all checks pass.

## Gate 3 — approval

Approved by David on 2026-10-26 (renders sent as twelve day/night overview sheets): "approve all".

## Stage 4 — optimize

Shipped as `app/public/sf-assets/landmarks/embarcadero-center-3.glb`, meshopt-compressed with the intake flags of `pipeline/compress-assets.mjs` (`gltfpack -c -km -kn -noq`): **228 KB → 95 KB** (59% smaller). Geometry is unchanged. Kit assets are already one body mesh and one glow mesh, so the Blender cleanup pass and the limited dissolve are skipped, as for the Transbay batch. Gate G3 (three.js GLTFLoader round-trip with MeshoptDecoder, `tools/glb-optimize/g3check`) passes.
