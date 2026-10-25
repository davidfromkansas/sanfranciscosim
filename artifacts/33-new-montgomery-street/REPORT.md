# 33 New Montgomery — asset report

## Result

**PASS** — `33-new-montgomery-street.glb` meets the landmark contract: the kit validator
(`tools/landmark-kit/validate.py`) factory-reset the scene, re-imported only the exported GLB
and printed "all checks pass" (budget 5,000 for a tower ≥ 60 m).
`validation.json` is the machine-readable authority. Not integrated: the manifest,
`pipeline/lib/landmarks.mjs` and app code are untouched.

## Deliverables

- `build_33_new_montgomery_street.py` — deterministic build (kit helpers in `tools/landmark-kit/toykit.py`)
- `33-new-montgomery-street.glb`, `33-new-montgomery-street.blend` — export and authoring scene
- `validate_33_new_montgomery_street.py`, `render_33_new_montgomery_street.py` — thin wrappers around the kit scripts
- `validation.json`; `33-new-montgomery-street-{north,east,south,west,top,aerial,aerial-night}.png`, `33-new-montgomery-street-contact-sheet.png`
- `REFERENCE.md`; plan at `docs/asset-plans/33-new-montgomery-street.md`

## Contract results

| Check | Result | Evidence |
|---|---|---|
| Crest = target height | PASS | max Z 101.8 m = 101.8 m |
| Plausible metre dimensions | PASS | 55.2705 × 71.5069 × 101.8 m |
| Base at Z 0 | PASS | min Z 0.0 m |
| Centred in XY | PASS | offset [0.0, 0.0] m |
| Triangle budget | PASS | 3,450 / 5,000 |
| No image textures / transparency | PASS | 0 images, all alpha 1.0 |
| Flat `Toy_*` materials | PASS | 7 materials, no violations |
| Has night glow | PASS | `Toy_sand_Glow`, `Toy_white_Glow` |
| No cameras / lights / animation | PASS | 0 / 0 / 0 |
| Transforms applied, no negative scale | PASS | 2 mesh objects at identity |
| Normals outward (signed volume) | PASS | inverted objects: [] |
| Normals outward (ray residual) | PASS | 0 flipped of 20,667 first hits |
| Glow skins face outward | PASS | 684 / 684 unobstructed |
| No degenerate geometry | PASS | 0 degenerate triangles |
| No unexpected objects | PASS | none |

Triangles **3,450** (body 2,766, glow 684); dimensions **[55.2705, 71.5069, 101.8]** m; anchor
**[-122.4014689, 37.7886469]**; height **101.8 m**; category `3`.
Materials: `Toy_glassd`, `Toy_granite`, `Toy_roofd`, `Toy_sand_Glow`, `Toy_steel`, `Toy_stone`, `Toy_white_Glow`.

## Night state

`Toy_sand_Glow`: lit shopfronts and scattered office panes; `Toy_white_Glow`: corner-element crown line.

## Iterations

- Single pass: plant cluster first placed outside the L (moved onto the NE arm). 3,450 tris, all checks pass. Not iterated further without a reference photo.

## Gate 3 — approval

Pending: renders sent to David.
