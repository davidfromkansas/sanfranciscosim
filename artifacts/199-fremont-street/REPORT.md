# 199 Fremont Street — asset report

## Result

**PASS** — `199-fremont-street.glb` meets the landmark contract: the kit validator
(`tools/landmark-kit/validate.py`) factory-reset the scene, re-imported only the exported GLB
and printed "all checks pass" (budget 5,000 for a tower ≥ 60 m).
`validation.json` is the machine-readable authority. Not integrated: the manifest,
`pipeline/lib/landmarks.mjs` and app code are untouched.

## Deliverables

- `build_199_fremont_street.py` — deterministic build (kit helpers in `tools/landmark-kit/toykit.py`)
- `199-fremont-street.glb`, `199-fremont-street.blend` — export and authoring scene
- `validate_199_fremont_street.py`, `render_199_fremont_street.py` — thin wrappers around the kit scripts
- `validation.json`; `199-fremont-street-{north,east,south,west,top,aerial,aerial-night}.png`, `199-fremont-street-contact-sheet.png`
- `REFERENCE.md`; plan at `docs/asset-plans/199-fremont-street.md`

## Contract results

| Check | Result | Evidence |
|---|---|---|
| Crest = target height | PASS | max Z 110.9 m = 110.9 m |
| Plausible metre dimensions | PASS | 74.2273 × 69.6048 × 110.9 m |
| Base at Z 0 | PASS | min Z 0.0 m |
| Centred in XY | PASS | offset [0.0, 0.0] m |
| Triangle budget | PASS | 4,814 / 5,000 |
| No image textures / transparency | PASS | 0 images, all alpha 1.0 |
| Flat `Toy_*` materials | PASS | 6 materials, no violations |
| Has night glow | PASS | `Toy_sand_Glow`, `Toy_white_Glow` |
| No cameras / lights / animation | PASS | 0 / 0 / 0 |
| Transforms applied, no negative scale | PASS | 2 mesh objects at identity |
| Normals outward (signed volume) | PASS | inverted objects: [] |
| Normals outward (ray residual) | PASS | 0 flipped of 20,291 first hits |
| Glow skins face outward | PASS | 754 / 754 unobstructed |
| No degenerate geometry | PASS | 0 degenerate triangles |
| No unexpected objects | PASS | none |

Triangles **4,814** (body 4,060, glow 754); dimensions **[74.2273, 69.6048, 110.9]** m; anchor
**[-122.3948792, 37.7900023]**; height **110.9 m**; category `3`.
Materials: `Toy_glass`, `Toy_roofd`, `Toy_sand_Glow`, `Toy_steel`, `Toy_stone`, `Toy_white_Glow`.

## Night state

`Toy_sand_Glow`: lit storefronts, scattered office panes, the corner column and the top tier; `Toy_white_Glow`: crown line.

## Iterations

- First render: the set-back top was offset off-centre and the corner glass column stood out as a thin slab beside the building; recentred the top tier on the footprint and set the column 1.3 m into the corner. 4,814 tris, all checks pass. A second pass shrank the top tier to 49 × 31 m because it overhung the jogged south-east face.

## Gate 3 — approval

Approved by David on 2026-10-26 (renders sent as twelve day/night overview sheets): "approve all".

## Stage 4 — optimize

Shipped as `app/public/sf-assets/landmarks/199-fremont-street.glb`, meshopt-compressed with the intake flags of `pipeline/compress-assets.mjs` (`gltfpack -c -km -kn -noq`): **256 KB → 110 KB** (57% smaller). Geometry is unchanged. Kit assets are already one body mesh and one glow mesh, so the Blender cleanup pass and the limited dissolve are skipped, as for the Transbay batch. Gate G3 (three.js GLTFLoader round-trip with MeshoptDecoder, `tools/glb-optimize/g3check`) passes.
