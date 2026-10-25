# Omni San Francisco Hotel (Financial Center Building) — asset report

## Result

**PASS** — `500-california-street.glb` meets the landmark contract: the kit validator
(`tools/landmark-kit/validate.py`) factory-reset the scene, re-imported only the exported GLB
and printed "all checks pass" (budget 5,000 for a tower ≥ 60 m).
`validation.json` is the machine-readable authority. Not integrated: the manifest,
`pipeline/lib/landmarks.mjs` and app code are untouched.

## Deliverables

- `build_500_california_street.py` — deterministic build (kit helpers in `tools/landmark-kit/toykit.py`)
- `500-california-street.glb`, `500-california-street.blend` — export and authoring scene
- `validate_500_california_street.py`, `render_500_california_street.py` — thin wrappers around the kit scripts
- `validation.json`; `500-california-street-north.png`, `500-california-street-east.png`, `500-california-street-south.png`, `500-california-street-west.png`, `500-california-street-top.png`, `500-california-street-aerial.png`, `500-california-street-aerial-night.png`, `500-california-street-contact-sheet.png`
- `REFERENCE.md`; plan at `docs/asset-plans/500-california-street.md`

## Contract results

| Check | Result | Evidence |
|---|---|---|
| Crest = target height | PASS | max Z 65.3 m = 65.3 m |
| Plausible metre dimensions | PASS | 54.0911 × 54.1823 × 65.3 m |
| Base at Z 0 | PASS | min Z 0.0 m |
| Centred in XY | PASS | offset [0.0, 0.0] m |
| Triangle budget | PASS | 3,630 / 5,000 |
| No image textures | PASS | 0 images |
| No transparency | PASS | transparent: [] |
| Flat `Toy_*` materials | PASS | 9 materials, violations [] |
| Has night glow | PASS | `Toy_sand_Glow` |
| No cameras / lights | PASS | 0 / 0 |
| No animation / skin / constraints | PASS | 0 / 0 / 0 |
| Transforms applied | PASS | 2 mesh objects at identity |
| No negative scales | PASS | none |
| Normals outward (signed volume) | PASS | inverted objects: [] |
| Normals outward (ray residual) | PASS | 0 flipped of 20,945 first hits |
| Glow skins face outward | PASS | 891 / 892 unobstructed |
| No degenerate geometry | PASS | 0 degenerate triangles |
| No unexpected objects | PASS | none |

Triangles **3,630** (body 2,738, glow 892); dimensions **[54.0911, 54.1823, 65.3]** m; anchor
**[-122.4031981, 37.7931217]**; height **65.3 m**; category `7`.
Materials: `Toy_glassd`, `Toy_leaf`, `Toy_leafd`, `Toy_roofd`, `Toy_rust`, `Toy_sand_Glow`, `Toy_steel`, `Toy_stone`, `Toy_terracotta`.

## Night state

`Toy_sand_Glow`: lit ground arches, scattered guest-room windows, lit arched top storey and penthouse windows.

## Iterations

- Built and validated in one pass (3,630 tris; 891/892 glow faces unobstructed — one pane behind a street tree, within tolerance).

## Gate 3 — approval

Pending: renders sent to David.
