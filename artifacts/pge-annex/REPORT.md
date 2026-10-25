# PG&E General Office Building Annex — asset report

## Result

**PASS** — `pge-annex.glb` meets the landmark contract: the kit validator
(`tools/landmark-kit/validate.py`) factory-reset the scene, re-imported only the exported GLB
and printed "all checks pass" (budget 3,000 for a building < 60 m).
`validation.json` is the machine-readable authority. Not integrated: the manifest,
`pipeline/lib/landmarks.mjs` and app code are untouched.

## Deliverables

- `build_pge_annex.py` — deterministic build (kit helpers in `tools/landmark-kit/toykit.py`)
- `pge-annex.glb`, `pge-annex.blend` — export and authoring scene
- `validate_pge_annex.py`, `render_pge_annex.py` — thin wrappers around the kit scripts
- `validation.json`; `pge-annex-north.png`, `pge-annex-east.png`, `pge-annex-south.png`, `pge-annex-west.png`, `pge-annex-top.png`, `pge-annex-aerial.png`, `pge-annex-aerial-night.png`, `pge-annex-contact-sheet.png`
- `REFERENCE.md`; plan at `docs/asset-plans/pge-annex.md`

## Contract results

| Check | Result | Evidence |
|---|---|---|
| Crest = target height | PASS | max Z 55.8 m = 55.8 m |
| Plausible metre dimensions | PASS | 65.7542 × 65.3062 × 55.8 m |
| Base at Z 0 | PASS | min Z 0.0 m |
| Centred in XY | PASS | offset [0.0, 0.0] m |
| Triangle budget | PASS | 2,200 / 3,000 |
| No image textures | PASS | 0 images |
| No transparency | PASS | transparent: [] |
| Flat `Toy_*` materials | PASS | 7 materials, violations [] |
| Has night glow | PASS | `Toy_sand_Glow` |
| No cameras / lights | PASS | 0 / 0 |
| No animation / skin / constraints | PASS | 0 / 0 / 0 |
| Transforms applied | PASS | 2 mesh objects at identity |
| No negative scales | PASS | none |
| Normals outward (signed volume) | PASS | inverted objects: [] |
| Normals outward (ray residual) | PASS | 0 flipped of 21,334 first hits |
| Glow skins face outward | PASS | 338 / 338 unobstructed |
| No degenerate geometry | PASS | 0 degenerate triangles |
| No unexpected objects | PASS | none |

Triangles **2,200** (body 1,862, glow 338); dimensions **[65.7542, 65.3062, 55.8]** m; anchor
**[-122.3965063, 37.7921155]**; height **55.8 m**; category `3`.
Materials: `Toy_cream`, `Toy_glassd`, `Toy_roofd`, `Toy_sand_Glow`, `Toy_steel`, `Toy_stone`, `Toy_terracotta`.

## Night state

`Toy_sand_Glow`: lit arches in the base, scattered shaft and attic windows.

## Iterations

- First build kept OSM's collinear nodes and produced one degenerate triangle; the plan was reduced to its four real corners → 2,200 tris, all checks pass.

## Gate 3 — approval

Pending: renders sent to David.
