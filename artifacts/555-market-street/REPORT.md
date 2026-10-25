# 555 Market Street (Market Center) — asset report

## Result

**PASS** — `555-market-street.glb` meets the landmark contract: the kit validator
(`tools/landmark-kit/validate.py`) factory-reset the scene, re-imported only the exported GLB
and printed "all checks pass" (budget 5,000 for a tower ≥ 60 m).
`validation.json` is the machine-readable authority. Not integrated: the manifest,
`pipeline/lib/landmarks.mjs` and app code are untouched.

## Deliverables

- `build_555_market_street.py` — deterministic build (kit helpers in `tools/landmark-kit/toykit.py`)
- `555-market-street.glb`, `555-market-street.blend` — export and authoring scene
- `validate_555_market_street.py`, `render_555_market_street.py` — thin wrappers around the kit scripts
- `validation.json`; `555-market-street-{north,east,south,west,top,aerial,aerial-night}.png`, `555-market-street-contact-sheet.png`
- `REFERENCE.md`; plan at `docs/asset-plans/555-market-street.md`

## Contract results

| Check | Result | Evidence |
|---|---|---|
| Crest = target height | PASS | max Z 94.8 m = 94.8 m |
| Plausible metre dimensions | PASS | 62.1833 × 62.1261 × 94.8 m |
| Base at Z 0 | PASS | min Z 0.0 m |
| Centred in XY | PASS | offset [0.0, 0.0] m |
| Triangle budget | PASS | 3,580 / 5,000 |
| No image textures / transparency | PASS | 0 images, all alpha 1.0 |
| Flat `Toy_*` materials | PASS | 11 materials, no violations |
| Has night glow | PASS | `Toy_sand_Glow`, `Toy_white_Glow` |
| No cameras / lights / animation | PASS | 0 / 0 / 0 |
| Transforms applied, no negative scale | PASS | 2 mesh objects at identity |
| Normals outward (signed volume) | PASS | inverted objects: [] |
| Normals outward (ray residual) | PASS | 0 flipped of 20,841 first hits |
| Glow skins face outward | PASS | 1012 / 1012 unobstructed |
| No degenerate geometry | PASS | 0 degenerate triangles |
| No unexpected objects | PASS | none |

Triangles **3,580** (body 2,568, glow 1,012); dimensions **[62.1833, 62.1261, 94.8]** m; anchor
**[-122.3999542, 37.7899805]**; height **94.8 m**; category `3`.
Materials: `Toy_glassd`, `Toy_granite`, `Toy_leaf`, `Toy_leafd`, `Toy_roofd`, `Toy_rust`, `Toy_sand_Glow`, `Toy_steel`, `Toy_stone`, `Toy_white`, `Toy_white_Glow`.

## Night state

`Toy_sand_Glow`: lobby ring and scattered panes between the ribs; `Toy_white_Glow`: crown line under the attic.

## Iterations

- Trees moved to the SW plaza strip (first draft put the plaza on the SE). 3,580 tris, all checks pass; render reads as intended, no further change.

## Gate 3 — approval

Pending: renders sent to David.
