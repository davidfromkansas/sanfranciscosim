# Neiman Marcus Union Square (City of Paris rotunda) — asset report

## Result

**PASS** — `150-stockton-street.glb` meets the landmark contract: the kit validator
(`tools/landmark-kit/validate.py`) factory-reset the scene, re-imported only the exported GLB
and printed "all checks pass" (budget 3,000 for a building < 60 m).
`validation.json` is the machine-readable authority. Not integrated: the manifest,
`pipeline/lib/landmarks.mjs` and app code are untouched.

## Deliverables

- `build_150_stockton_street.py` — deterministic build (kit helpers in `tools/landmark-kit/toykit.py`)
- `150-stockton-street.glb`, `150-stockton-street.blend` — export and authoring scene
- `validate_150_stockton_street.py`, `render_150_stockton_street.py` — thin wrappers around the kit scripts
- `validation.json`; `150-stockton-street-north.png`, `150-stockton-street-east.png`, `150-stockton-street-south.png`, `150-stockton-street-west.png`, `150-stockton-street-top.png`, `150-stockton-street-aerial.png`, `150-stockton-street-aerial-night.png`, `150-stockton-street-contact-sheet.png`
- `REFERENCE.md`; plan at `docs/asset-plans/150-stockton-street.md`

## Contract results

| Check | Result | Evidence |
|---|---|---|
| Crest = target height | PASS | max Z 33.9 m = 33.9 m |
| Plausible metre dimensions | PASS | 104.715 × 63.0629 × 33.9 m |
| Base at Z 0 | PASS | min Z 0.0 m |
| Centred in XY | PASS | offset [0.0, 0.0] m |
| Triangle budget | PASS | 1,528 / 3,000 |
| No image textures | PASS | 0 images |
| No transparency | PASS | transparent: [] |
| Flat `Toy_*` materials | PASS | 9 materials, violations [] |
| Has night glow | PASS | `Toy_gold_Glow`, `Toy_sand_Glow` |
| No cameras / lights | PASS | 0 / 0 |
| No animation / skin / constraints | PASS | 0 / 0 / 0 |
| Transforms applied | PASS | 2 mesh objects at identity |
| No negative scales | PASS | none |
| Normals outward (signed volume) | PASS | inverted objects: [] |
| Normals outward (ray residual) | PASS | 3 flipped of 21,451 first hits |
| Glow skins face outward | PASS | 118 / 118 unobstructed |
| No degenerate geometry | PASS | 0 degenerate triangles |
| No unexpected objects | PASS | none |

Triangles **1,528** (body 1,410, glow 118); dimensions **[104.715, 63.0629, 33.9]** m; anchor
**[-122.4059211, 37.7873699]**; height **33.9 m**; category `4`.
Materials: `Toy_glassd`, `Toy_glassl`, `Toy_gold_Glow`, `Toy_granite`, `Toy_roofd`, `Toy_rust`, `Toy_sand_Glow`, `Toy_steel`, `Toy_stone`.

## Night state

`Toy_sand_Glow`: storefront ring, lit rotunda panes, upper-storey windows; `Toy_gold_Glow`: the dome.

## Iterations

- Checkerboard first used two pane sets that lined up instead of alternating; replaced with a checker helper. Rotunda glow restricted to arcs outside the box so no lit pane is buried. 1,528 tris.

## Gate 3 — approval

Approved by David on 2026-10-26 (renders sent as twelve day/night overview sheets): "approve all".

## Stage 4 — optimize

Shipped as `app/public/sf-assets/landmarks/150-stockton-street.glb`, meshopt-compressed with the intake flags of `pipeline/compress-assets.mjs` (`gltfpack -c -km -kn -noq`): **88 KB → 41 KB** (54% smaller). Geometry is unchanged. Kit assets are already one body mesh and one glow mesh, so the Blender cleanup pass and the limited dissolve are skipped, as for the Transbay batch. Gate G3 (three.js GLTFLoader round-trip with MeshoptDecoder, `tools/glb-optimize/g3check`) passes.
