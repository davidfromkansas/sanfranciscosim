# Central Plaza (455 Market Street) — asset report

## Result

**PASS** — `first-and-market-usps.glb` meets the landmark contract: the kit validator
(`tools/landmark-kit/validate.py`) factory-reset the scene, re-imported only the exported GLB
and printed "all checks pass" (budget 5,000 for a tower ≥ 60 m).
`validation.json` is the machine-readable authority. Not integrated: the manifest,
`pipeline/lib/landmarks.mjs` and app code are untouched.

## Deliverables

- `build_first_and_market_usps.py` — deterministic build (kit helpers in `tools/landmark-kit/toykit.py`)
- `first-and-market-usps.glb`, `first-and-market-usps.blend` — export and authoring scene
- `validate_first_and_market_usps.py`, `render_first_and_market_usps.py` — thin wrappers around the kit scripts
- `validation.json`; `first-and-market-usps-north.png`, `first-and-market-usps-east.png`, `first-and-market-usps-south.png`, `first-and-market-usps-west.png`, `first-and-market-usps-top.png`, `first-and-market-usps-aerial.png`, `first-and-market-usps-aerial-night.png`, `first-and-market-usps-contact-sheet.png`
- `REFERENCE.md`; plan at `docs/asset-plans/first-and-market-usps.md`

## Contract results

| Check | Result | Evidence |
|---|---|---|
| Crest = target height | PASS | max Z 96.9 m = 96.9 m |
| Plausible metre dimensions | PASS | 91.3512 × 83.4028 × 96.9 m |
| Base at Z 0 | PASS | min Z 0.0 m |
| Centred in XY | PASS | offset [0.0, 0.0] m |
| Triangle budget | PASS | 4,770 / 5,000 |
| No image textures | PASS | 0 images |
| No transparency | PASS | transparent: [] |
| Flat `Toy_*` materials | PASS | 7 materials, violations [] |
| Has night glow | PASS | `Toy_sand_Glow`, `Toy_white_Glow` |
| No cameras / lights | PASS | 0 / 0 |
| No animation / skin / constraints | PASS | 0 / 0 / 0 |
| Transforms applied | PASS | 2 mesh objects at identity |
| No negative scales | PASS | none |
| Normals outward (signed volume) | PASS | inverted objects: [] |
| Normals outward (ray residual) | PASS | 20 flipped of 18,924 first hits |
| Glow skins face outward | PASS | 726 / 726 unobstructed |
| No degenerate geometry | PASS | 0 degenerate triangles |
| No unexpected objects | PASS | none |

Triangles **4,770** (body 4,044, glow 726); dimensions **[91.3512, 83.4028, 96.9]** m; anchor
**[-122.3984381, 37.7908114]**; height **96.9 m**; category `3`.
Materials: `Toy_glassd`, `Toy_roofd`, `Toy_sand`, `Toy_sand_Glow`, `Toy_steel`, `Toy_stone`, `Toy_white_Glow`.

## Night state

`Toy_sand_Glow`: lobby rings, scattered windows on wing, tower and crown; `Toy_white_Glow`: crown line.

## Iterations

- First build used a single tower block and window graphics on the seam with the wing (would have hidden lit panes); split the tower at the wing roof and filtered the seam and notch faces. 5,056 → 4,770 tris by widening window spacing.

## Gate 3 — approval

Approved by David on 2026-10-26 (renders sent as twelve day/night overview sheets): "approve all".

## Stage 4 — optimize

Shipped as `app/public/sf-assets/landmarks/first-and-market-usps.glb`, meshopt-compressed with the intake flags of `pipeline/compress-assets.mjs` (`gltfpack -c -km -kn -noq`): **257 KB → 108 KB** (58% smaller). Geometry is unchanged. Kit assets are already one body mesh and one glow mesh, so the Blender cleanup pass and the limited dissolve are skipped, as for the Transbay batch. Gate G3 (three.js GLTFLoader round-trip with MeshoptDecoder, `tools/glb-optimize/g3check`) passes.
