# Crown Zellerbach Building (One Bush Plaza) — asset report

## Result

**PASS** — `1-bush-street.glb` meets the landmark contract: the kit validator
(`tools/landmark-kit/validate.py`) factory-reset the scene, re-imported only the exported GLB
and printed "all checks pass" (budget 5,000 for a tower ≥ 60 m).
`validation.json` is the machine-readable authority. Not integrated: the manifest,
`pipeline/lib/landmarks.mjs` and app code are untouched.

## Deliverables

- `build_1_bush_street.py` — deterministic build (kit helpers in `tools/landmark-kit/toykit.py`)
- `1-bush-street.glb`, `1-bush-street.blend` — export and authoring scene
- `validate_1_bush_street.py`, `render_1_bush_street.py` — thin wrappers around the kit scripts
- `validation.json`; `1-bush-street-{north,east,south,west,top,aerial,aerial-night}.png`, `1-bush-street-contact-sheet.png`
- `REFERENCE.md`; plan at `docs/asset-plans/1-bush-street.md`

## Contract results

| Check | Result | Evidence |
|---|---|---|
| Crest = target height | PASS | max Z 93.9 m = 93.9 m |
| Plausible metre dimensions | PASS | 75.5086 × 53.3574 × 93.9 m |
| Base at Z 0 | PASS | min Z 0.0 m |
| Centred in XY | PASS | offset [0.0, 0.0] m |
| Triangle budget | PASS | 3,618 / 5,000 |
| No image textures / transparency | PASS | 0 images, all alpha 1.0 |
| Flat `Toy_*` materials | PASS | 11 materials, no violations |
| Has night glow | PASS | `Toy_sand_Glow`, `Toy_white_Glow` |
| No cameras / lights / animation | PASS | 0 / 0 / 0 |
| Transforms applied, no negative scale | PASS | 2 mesh objects at identity |
| Normals outward (signed volume) | PASS | inverted objects: [] |
| Normals outward (ray residual) | PASS | 0 flipped of 21,067 first hits |
| Glow skins face outward | PASS | 818 / 818 unobstructed |
| No degenerate geometry | PASS | 0 degenerate triangles |
| No unexpected objects | PASS | none |

Triangles **3,618** (body 2,800, glow 818); dimensions **[75.5086, 53.3574, 93.9]** m; anchor
**[-122.4000600, 37.7909563]**; height **93.9 m**; category `3`.
Materials: `Toy_glassd`, `Toy_granite`, `Toy_ink`, `Toy_leaf`, `Toy_roofd`, `Toy_rust`, `Toy_sand_Glow`, `Toy_steel`, `Toy_teal`, `Toy_verdigris`, `Toy_white_Glow`.

## Night state

`Toy_sand_Glow`: lobby ring and scattered panes between mullions; `Toy_white_Glow`: core crown line.

## Iterations

- First render used `Toy_copper` glass, which read as a dull sage and merged with the core; switched to `Toy_teal` so the glass slab and the solid core separate. 3,618 tris, all checks pass.

## Gate 3 — approval

Pending: renders sent to David.
