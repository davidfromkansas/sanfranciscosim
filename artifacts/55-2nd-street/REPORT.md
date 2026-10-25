# KPMG Building (55 Second Street) — asset report

## Result

**PASS** — `55-2nd-street.glb` meets the landmark contract: the kit validator
(`tools/landmark-kit/validate.py`) factory-reset the scene, re-imported only the exported GLB
and printed "all checks pass" (budget 5,000 for a tower ≥ 60 m).
`validation.json` is the machine-readable authority. Not integrated: the manifest,
`pipeline/lib/landmarks.mjs` and app code are untouched.

## Deliverables

- `build_55_2nd_street.py` — deterministic build (kit helpers in `tools/landmark-kit/toykit.py`)
- `55-2nd-street.glb`, `55-2nd-street.blend` — export and authoring scene
- `validate_55_2nd_street.py`, `render_55_2nd_street.py` — thin wrappers around the kit scripts
- `validation.json`; `55-2nd-street-north.png`, `55-2nd-street-east.png`, `55-2nd-street-south.png`, `55-2nd-street-west.png`, `55-2nd-street-top.png`, `55-2nd-street-aerial.png`, `55-2nd-street-aerial-night.png`, `55-2nd-street-contact-sheet.png`
- `REFERENCE.md`; plan at `docs/asset-plans/55-2nd-street.md`

## Contract results

| Check | Result | Evidence |
|---|---|---|
| Crest = target height | PASS | max Z 100.6 m = 100.6 m |
| Plausible metre dimensions | PASS | 68.5501 × 67.9062 × 100.6 m |
| Base at Z 0 | PASS | min Z 0.0 m |
| Centred in XY | PASS | offset [0.0, 0.0] m |
| Triangle budget | PASS | 4,810 / 5,000 |
| No image textures | PASS | 0 images |
| No transparency | PASS | transparent: [] |
| Flat `Toy_*` materials | PASS | 7 materials, violations [] |
| Has night glow | PASS | `Toy_sand_Glow`, `Toy_white_Glow` |
| No cameras / lights | PASS | 0 / 0 |
| No animation / skin / constraints | PASS | 0 / 0 / 0 |
| Transforms applied | PASS | 2 mesh objects at identity |
| No negative scales | PASS | none |
| Normals outward (signed volume) | PASS | inverted objects: [] |
| Normals outward (ray residual) | PASS | 1 flipped of 19,827 first hits |
| Glow skins face outward | PASS | 638 / 638 unobstructed |
| No degenerate geometry | PASS | 0 degenerate triangles |
| No unexpected objects | PASS | none |

Triangles **4,810** (body 4,172, glow 638); dimensions **[68.5501, 67.9062, 100.6]** m; anchor
**[-122.4003340, 37.7888147]**; height **100.6 m**; category `3`.
Materials: `Toy_roofd`, `Toy_sand`, `Toy_sand_Glow`, `Toy_steel`, `Toy_stone`, `Toy_verdigris`, `Toy_white_Glow`.

## Night state

`Toy_sand_Glow`: lit base bays and scattered windows on every tier; `Toy_white_Glow`: crown line.

## Iterations

- Crown light line first sat over the top tier's lit panes (obstruction); moved onto the parapet. 5,114 → 4,810 tris by widening window spacing.

## Gate 3 — approval

Pending: renders sent to David.
