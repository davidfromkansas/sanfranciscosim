# Merchants Exchange Building — asset report

## Result

**PASS** — `california-bank-and-trust.glb` meets the landmark contract: the kit validator
(`tools/landmark-kit/validate.py`) factory-reset the scene, re-imported only the exported GLB
and printed "all checks pass" (budget 3,000 for a building < 60 m).
`validation.json` is the machine-readable authority. Not integrated: the manifest,
`pipeline/lib/landmarks.mjs` and app code are untouched.

## Deliverables

- `build_california_bank_and_trust.py` — deterministic build (kit helpers in `tools/landmark-kit/toykit.py`)
- `california-bank-and-trust.glb`, `california-bank-and-trust.blend` — export and authoring scene
- `validate_california_bank_and_trust.py`, `render_california_bank_and_trust.py` — thin wrappers around the kit scripts
- `validation.json`; `california-bank-and-trust-north.png`, `california-bank-and-trust-east.png`, `california-bank-and-trust-south.png`, `california-bank-and-trust-west.png`, `california-bank-and-trust-top.png`, `california-bank-and-trust-aerial.png`, `california-bank-and-trust-aerial-night.png`, `california-bank-and-trust-contact-sheet.png`
- `REFERENCE.md`; plan at `docs/asset-plans/california-bank-and-trust.md`

## Contract results

| Check | Result | Evidence |
|---|---|---|
| Crest = target height | PASS | max Z 59.4 m = 59.4 m |
| Plausible metre dimensions | PASS | 50.2966 × 64.9855 × 59.4 m |
| Base at Z 0 | PASS | min Z 0.0 m |
| Centred in XY | PASS | offset [0.0, 0.0] m |
| Triangle budget | PASS | 2,806 / 3,000 |
| No image textures | PASS | 0 images |
| No transparency | PASS | transparent: [] |
| Flat `Toy_*` materials | PASS | 6 materials, violations [] |
| Has night glow | PASS | `Toy_sand_Glow` |
| No cameras / lights | PASS | 0 / 0 |
| No animation / skin / constraints | PASS | 0 / 0 / 0 |
| Transforms applied | PASS | 2 mesh objects at identity |
| No negative scales | PASS | none |
| Normals outward (signed volume) | PASS | inverted objects: [] |
| Normals outward (ray residual) | PASS | 0 flipped of 20,675 first hits |
| Glow skins face outward | PASS | 384 / 384 unobstructed |
| No degenerate geometry | PASS | 0 degenerate triangles |
| No unexpected objects | PASS | none |

Triangles **2,806** (body 2,422, glow 384); dimensions **[50.2966, 64.9855, 59.4]** m; anchor
**[-122.4021502, 37.7925691]**; height **59.4 m**; category `3`.
Materials: `Toy_glassd`, `Toy_roofd`, `Toy_sand_Glow`, `Toy_steel`, `Toy_stone`, `Toy_white`.

## Night state

`Toy_sand_Glow`: lit portal, flanking banking-hall windows, scattered office windows and attic windows.

## Iterations

- Front glass quads were not named `_panes`, so the normal recalc flipped them (ray residual 0.16 %, FAIL); renamed and re-validated → PASS.
- Shaft windows widened to 4.2 m to bring 3,224 → 2,806 tris.
- After the first contact sheet the columns were too thin to read; thickened (r 0.75 → 1.0 m) and moved 0.2 m forward, then re-rendered.

## Gate 3 — approval

Approved by David on 2026-10-26 (renders sent as twelve day/night overview sheets): "approve all".

## Stage 4 — optimize

Shipped as `app/public/sf-assets/landmarks/california-bank-and-trust.glb`, meshopt-compressed with the intake flags of `pipeline/compress-assets.mjs` (`gltfpack -c -km -kn -noq`): **151 KB → 66 KB** (56% smaller). Geometry is unchanged. Kit assets are already one body mesh and one glow mesh, so the Blender cleanup pass and the limited dissolve are skipped, as for the Transbay batch. Gate G3 (three.js GLTFLoader round-trip with MeshoptDecoder, `tools/glb-optimize/g3check`) passes.
