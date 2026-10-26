# San Francisco Museum of Modern Art (SFMOMA) — asset report

## Result

**PASS** — `151-3rd-street.glb` meets the landmark contract: the kit validator
(`tools/landmark-kit/validate.py`) factory-reset the scene, re-imported only the exported GLB
and printed "all checks pass" (budget 5,000 for a tower ≥ 60 m).
`validation.json` is the machine-readable authority. Not integrated: the manifest,
`pipeline/lib/landmarks.mjs` and app code are untouched.

## Deliverables

- `build_151_3rd_street.py` — deterministic build (kit helpers in `tools/landmark-kit/toykit.py`)
- `151-3rd-street.glb`, `151-3rd-street.blend` — export and authoring scene
- `validate_151_3rd_street.py`, `render_151_3rd_street.py` — thin wrappers around the kit scripts
- `validation.json`; `151-3rd-street-north.png`, `151-3rd-street-east.png`, `151-3rd-street-south.png`, `151-3rd-street-west.png`, `151-3rd-street-top.png`, `151-3rd-street-aerial.png`, `151-3rd-street-aerial-night.png`, `151-3rd-street-contact-sheet.png`
- `REFERENCE.md`; plan at `docs/asset-plans/151-3rd-street.md`

## Contract results

| Check | Result | Evidence |
|---|---|---|
| Crest = target height | PASS | max Z 60.0 m = 60.0 m |
| Plausible metre dimensions | PASS | 137.262 × 112.9403 × 60.0 m |
| Base at Z 0 | PASS | min Z 0.0 m |
| Centred in XY | PASS | offset [0.0, 0.0] m |
| Triangle budget | PASS | 2,554 / 5,000 |
| No image textures | PASS | 0 images |
| No transparency | PASS | transparent: [] |
| Flat `Toy_*` materials | PASS | 11 materials, violations [] |
| Has night glow | PASS | `Toy_sand_Glow`, `Toy_white_Glow` |
| No cameras / lights | PASS | 0 / 0 |
| No animation / skin / constraints | PASS | 0 / 0 / 0 |
| Transforms applied | PASS | 2 mesh objects at identity |
| No negative scales | PASS | none |
| Normals outward (signed volume) | PASS | inverted objects: [] |
| Normals outward (ray residual) | PASS | 0 flipped of 21,807 first hits |
| Glow skins face outward | PASS | 100 / 100 unobstructed |
| No degenerate geometry | PASS | 0 degenerate triangles |
| No unexpected objects | PASS | none |

Triangles **2,554** (body 2,454, glow 100); dimensions **[137.262, 112.9403, 60.0]** m; anchor
**[-122.4006347, 37.7859319]**; height **60.0 m** (estimated); category `16`.
Materials: `Toy_brick`, `Toy_glassd`, `Toy_glassg`, `Toy_glassl`, `Toy_ink`, `Toy_roofd`, `Toy_sand_Glow`, `Toy_steel`, `Toy_stone`, `Toy_white`, `Toy_white_Glow`.

## Night state

`Toy_white_Glow`: the oculus; `Toy_sand_Glow`: entrance, Howard St gallery, scattered windows on the wing.

## Iterations

- Roof plant first overshot the crest by 3.8 % (no normalisation); wing roof lowered to 56 m so the crest lands at 60 m. Howard gallery quad was wound inward; reversed. 2,554 tris.

## Gate 3 — approval

Approved by David on 2026-10-26 (renders sent as twelve day/night overview sheets): "approve all".

## Stage 4 — optimize

Shipped as `app/public/sf-assets/landmarks/151-3rd-street.glb`, meshopt-compressed with the intake flags of `pipeline/compress-assets.mjs` (`gltfpack -c -km -kn -noq`): **132 KB → 69 KB** (48% smaller). Geometry is unchanged. Kit assets are already one body mesh and one glow mesh, so the Blender cleanup pass and the limited dissolve are skipped, as for the Transbay batch. Gate G3 (three.js GLTFLoader round-trip with MeshoptDecoder, `tools/glb-optimize/g3check`) passes.
