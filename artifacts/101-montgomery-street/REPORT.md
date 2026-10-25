# 101 Montgomery (Schwab Building) — asset report

## Result

**PASS** — `101-montgomery-street.glb` meets the landmark contract: the kit validator
(`tools/landmark-kit/validate.py`) factory-reset the scene, re-imported only the exported GLB
and printed "all checks pass" (budget 5,000 for a tower ≥ 60 m).
`validation.json` is the machine-readable authority. Not integrated: the manifest,
`pipeline/lib/landmarks.mjs` and app code are untouched.

## Deliverables

- `build_101_montgomery_street.py` — deterministic build (kit helpers in `tools/landmark-kit/toykit.py`)
- `101-montgomery-street.glb`, `101-montgomery-street.blend` — export and authoring scene
- `validate_101_montgomery_street.py`, `render_101_montgomery_street.py` — thin wrappers around the kit scripts
- `validation.json`; `101-montgomery-street-{north,east,south,west,top,aerial,aerial-night}.png`, `101-montgomery-street-contact-sheet.png`
- `REFERENCE.md`; plan at `docs/asset-plans/101-montgomery-street.md`

## Contract results

| Check | Result | Evidence |
|---|---|---|
| Crest = target height | PASS | max Z 123.1 m = 123.1 m |
| Plausible metre dimensions | PASS | 33.7451 × 72.9064 × 123.1 m |
| Base at Z 0 | PASS | min Z 0.0 m |
| Centred in XY | PASS | offset [0.0, 0.0] m |
| Triangle budget | PASS | 3,956 / 5,000 |
| No image textures / transparency | PASS | 0 images, all alpha 1.0 |
| Flat `Toy_*` materials | PASS | 8 materials, no violations |
| Has night glow | PASS | `Toy_sand_Glow`, `Toy_white_Glow` |
| No cameras / lights / animation | PASS | 0 / 0 / 0 |
| Transforms applied, no negative scale | PASS | 2 mesh objects at identity |
| Normals outward (signed volume) | PASS | inverted objects: [] |
| Normals outward (ray residual) | PASS | 0 flipped of 21,400 first hits |
| Glow skins face outward | PASS | 822 / 822 unobstructed |
| No degenerate geometry | PASS | 0 degenerate triangles |
| No unexpected objects | PASS | none |

Triangles **3,956** (body 3,134, glow 822); dimensions **[33.7451, 72.9064, 123.1]** m; anchor
**[-122.4024908, 37.7903643]**; height **123.1 m**; category `3`.
Materials: `Toy_cream`, `Toy_glassd`, `Toy_roofd`, `Toy_sand_Glow`, `Toy_steel`, `Toy_stone`, `Toy_white`, `Toy_white_Glow`.

## Night state

`Toy_sand_Glow`: lobby ring and scattered office panes; `Toy_white_Glow`: crown line.

## Iterations

- Draft roof plant stood above the crest; the crown became a hollow wall with the deck dropped to 119 m. 3,956 tris, all checks pass; reviewed against the photo, no further change.

## Gate 3 — approval

Pending: renders sent to David.
