# 111 Pine Street — asset report

## Result

**PASS** — `111-pine-street.glb` meets the landmark contract: the kit validator
(`tools/landmark-kit/validate.py`) factory-reset the scene, re-imported only the exported GLB
and printed "all checks pass" (budget 5,000 for a tower ≥ 60 m).
`validation.json` is the machine-readable authority. Not integrated: the manifest,
`pipeline/lib/landmarks.mjs` and app code are untouched.

## Deliverables

- `build_111_pine_street.py` — deterministic build (kit helpers in `tools/landmark-kit/toykit.py`)
- `111-pine-street.glb`, `111-pine-street.blend` — export and authoring scene
- `validate_111_pine_street.py`, `render_111_pine_street.py` — thin wrappers around the kit scripts
- `validation.json`; `111-pine-street-north.png`, `111-pine-street-east.png`, `111-pine-street-south.png`, `111-pine-street-west.png`, `111-pine-street-top.png`, `111-pine-street-aerial.png`, `111-pine-street-aerial-night.png`, `111-pine-street-contact-sheet.png`
- `REFERENCE.md`; plan at `docs/asset-plans/111-pine-street.md`

## Contract results

| Check | Result | Evidence |
|---|---|---|
| Crest = target height | PASS | max Z 76.0 m = 76.0 m |
| Plausible metre dimensions | PASS | 52.4675 × 39.6667 × 76.0 m |
| Base at Z 0 | PASS | min Z 0.0 m |
| Centred in XY | PASS | offset [0.0, 0.0] m |
| Triangle budget | PASS | 4,548 / 5,000 |
| No image textures | PASS | 0 images |
| No transparency | PASS | transparent: [] |
| Flat `Toy_*` materials | PASS | 9 materials, violations [] |
| Has night glow | PASS | `Toy_sand_Glow`, `Toy_white_Glow` |
| No cameras / lights | PASS | 0 / 0 |
| No animation / skin / constraints | PASS | 0 / 0 / 0 |
| Transforms applied | PASS | 2 mesh objects at identity |
| No negative scales | PASS | none |
| Normals outward (signed volume) | PASS | inverted objects: [] |
| Normals outward (ray residual) | PASS | 0 flipped of 20,256 first hits |
| Glow skins face outward | PASS | 772 / 772 unobstructed |
| No degenerate geometry | PASS | 0 degenerate triangles |
| No unexpected objects | PASS | none |

Triangles **4,548** (body 3,776, glow 772); dimensions **[52.4675, 39.6667, 76.0]** m; anchor
**[-122.3989068, 37.7921569]**; height **76.0 m**; category `3`.
Materials: `Toy_concrete`, `Toy_glassd`, `Toy_granite`, `Toy_ink`, `Toy_roofd`, `Toy_sand_Glow`, `Toy_steel`, `Toy_stone`, `Toy_white_Glow`.

## Night state

`Toy_sand_Glow`: lit arches in the base and scattered panes in the grid; `Toy_white_Glow`: line at the louvred top storey.

## Iterations

- First build was 5,244 tris (louvres at 1.2 m); louvres widened to 2.4 m → 4,548 tris. Piers made 0.08 m deep so lit panes are not obstructed. Render matches the photo's grid-and-pier rhythm; no further change.

## Gate 3 — approval

Approved by David on 2026-10-26 (renders sent as twelve day/night overview sheets): "approve all".

## Stage 4 — optimize

Shipped as `app/public/sf-assets/landmarks/111-pine-street.glb`, meshopt-compressed with the intake flags of `pipeline/compress-assets.mjs` (`gltfpack -c -km -kn -noq`): **244 KB → 95 KB** (61% smaller). Geometry is unchanged. Kit assets are already one body mesh and one glow mesh, so the Blender cleanup pass and the limited dissolve are skipped, as for the Transbay batch. Gate G3 (three.js GLTFLoader round-trip with MeshoptDecoder, `tools/glb-optimize/g3check`) passes.
