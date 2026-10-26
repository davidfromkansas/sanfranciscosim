# 425 California Street — asset report

## Result

**PASS** — `425-california-street.glb` meets the landmark contract: the kit validator
(`tools/landmark-kit/validate.py`) factory-reset the scene, re-imported only the exported GLB
and printed "all checks pass" (budget 5,000 for a tower ≥ 60 m).
`validation.json` is the machine-readable authority. Not integrated: the manifest,
`pipeline/lib/landmarks.mjs` and app code are untouched.

## Deliverables

- `build_425_california_street.py` — deterministic build (kit helpers in `tools/landmark-kit/toykit.py`)
- `425-california-street.glb`, `425-california-street.blend` — export and authoring scene
- `validate_425_california_street.py`, `render_425_california_street.py` — thin wrappers around the kit scripts
- `validation.json`; `425-california-street-north.png`, `425-california-street-east.png`, `425-california-street-south.png`, `425-california-street-west.png`, `425-california-street-top.png`, `425-california-street-aerial.png`, `425-california-street-aerial-night.png`, `425-california-street-contact-sheet.png`
- `REFERENCE.md`; plan at `docs/asset-plans/425-california-street.md`

## Contract results

| Check | Result | Evidence |
|---|---|---|
| Crest = target height | PASS | max Z 109.4 m = 109.4 m |
| Plausible metre dimensions | PASS | 34.2478 × 33.0283 × 109.4 m |
| Base at Z 0 | PASS | min Z 0.0 m |
| Centred in XY | PASS | offset [0.0, 0.0] m |
| Triangle budget | PASS | 2,834 / 5,000 |
| No image textures | PASS | 0 images |
| No transparency | PASS | transparent: [] |
| Flat `Toy_*` materials | PASS | 8 materials, violations [] |
| Has night glow | PASS | `Toy_gold_Glow`, `Toy_sand_Glow` |
| No cameras / lights | PASS | 0 / 0 |
| No animation / skin / constraints | PASS | 0 / 0 / 0 |
| Transforms applied | PASS | 2 mesh objects at identity |
| No negative scales | PASS | none |
| Normals outward (signed volume) | PASS | inverted objects: [] |
| Normals outward (ray residual) | PASS | 0 flipped of 20,437 first hits |
| Glow skins face outward | PASS | 538 / 538 unobstructed |
| No degenerate geometry | PASS | 0 degenerate triangles |
| No unexpected objects | PASS | none |

Triangles **2,834** (body 2,296, glow 538); dimensions **[34.2478, 33.0283, 109.4]** m; anchor
**[-122.4013729, 37.7928108]**; height **109.4 m**; category `3`.
Materials: `Toy_glassd`, `Toy_gold`, `Toy_gold_Glow`, `Toy_ink`, `Toy_roofd`, `Toy_sand_Glow`, `Toy_steel`, `Toy_stone`.

## Night state

`Toy_sand_Glow`: lobby ring and scattered panes between fins; `Toy_gold_Glow`: crown line under the gold caps.

## Iterations

- First build had the gold crown line inside the fin caps (would have been obstructed); moved it outside before validation. Roof lowered 1.4 m so the plant lands on the published crest. Renders read correctly against the photo; no further changes.

## Gate 3 — approval

Approved by David on 2026-10-26 (renders sent as twelve day/night overview sheets): "approve all".

## Stage 4 — optimize

Shipped as `app/public/sf-assets/landmarks/425-california-street.glb`, meshopt-compressed with the intake flags of `pipeline/compress-assets.mjs` (`gltfpack -c -km -kn -noq`): **146 KB → 69 KB** (52% smaller). Geometry is unchanged. Kit assets are already one body mesh and one glow mesh, so the Blender cleanup pass and the limited dissolve are skipped, as for the Transbay batch. Gate G3 (three.js GLTFLoader round-trip with MeshoptDecoder, `tools/glb-optimize/g3check`) passes.
