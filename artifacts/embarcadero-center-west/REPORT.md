# Embarcadero Center West (275 Battery Street) — asset report

## Result

**PASS** — `embarcadero-center-west.glb` meets the landmark contract: the kit validator
(`tools/landmark-kit/validate.py`) factory-reset the scene, re-imported only the exported GLB
and printed "all checks pass" (budget 5,000 for a tower ≥ 60 m).
`validation.json` is the machine-readable authority. Not integrated: the manifest,
`pipeline/lib/landmarks.mjs` and app code are untouched.

## Deliverables

- `build_embarcadero_center_west.py` — deterministic build (kit helpers in `tools/landmark-kit/toykit.py`)
- `embarcadero-center-west.glb`, `embarcadero-center-west.blend` — export and authoring scene
- `validate_embarcadero_center_west.py`, `render_embarcadero_center_west.py` — thin wrappers around the kit scripts
- `validation.json`; `embarcadero-center-west-{north,east,south,west,top,aerial,aerial-night}.png`, `embarcadero-center-west-contact-sheet.png`
- `REFERENCE.md`; plan at `docs/asset-plans/embarcadero-center-west.md`

## Contract results

| Check | Result | Evidence |
|---|---|---|
| Crest = target height | PASS | max Z 123.1 m = 123.1 m |
| Plausible metre dimensions | PASS | 51.7243 × 47.9189 × 123.1 m |
| Base at Z 0 | PASS | min Z 0.0 m |
| Centred in XY | PASS | offset [0.0, 0.0] m |
| Triangle budget | PASS | 4,460 / 5,000 |
| No image textures / transparency | PASS | 0 images, all alpha 1.0 |
| Flat `Toy_*` materials | PASS | 7 materials, no violations |
| Has night glow | PASS | `Toy_sand_Glow`, `Toy_white_Glow` |
| No cameras / lights / animation | PASS | 0 / 0 / 0 |
| Transforms applied, no negative scale | PASS | 2 mesh objects at identity |
| Normals outward (signed volume) | PASS | inverted objects: [] |
| Normals outward (ray residual) | PASS | 0 flipped of 20,310 first hits |
| Glow skins face outward | PASS | 540 / 540 unobstructed |
| No degenerate geometry | PASS | 0 degenerate triangles |
| No unexpected objects | PASS | none |

Triangles **4,460** (body 3,920, glow 540); dimensions **[51.7243, 47.9189, 123.1]** m; anchor
**[-122.4004675, 37.7938599]**; height **123.1 m**; category `3`.
Materials: `Toy_glassd`, `Toy_granite`, `Toy_roofd`, `Toy_sand_Glow`, `Toy_steel`, `Toy_stone`, `Toy_white_Glow`.

## Night state

`Toy_sand_Glow`: lit storefronts and scattered office panes between the fins; `Toy_white_Glow`: crown line.

## Iterations

- Draft per-storey loft with 3 m fins was 6,584 tris (over the 5,000 cap); switched to 13 two-storey groups and 4 m fins with lit panes still per storey: 4,460 tris, all checks pass. Render matches the photo's dark ribbed shaft and stepped corners.

## Gate 3 — approval

Approved by David on 2026-10-26 (renders sent as twelve day/night overview sheets): "approve all".

## Stage 4 — optimize

Shipped as `app/public/sf-assets/landmarks/embarcadero-center-west.glb`, meshopt-compressed with the intake flags of `pipeline/compress-assets.mjs` (`gltfpack -c -km -kn -noq`): **220 KB → 98 KB** (56% smaller). Geometry is unchanged. Kit assets are already one body mesh and one glow mesh, so the Blender cleanup pass and the limited dissolve are skipped, as for the Transbay batch. Gate G3 (three.js GLTFLoader round-trip with MeshoptDecoder, `tools/glb-optimize/g3check`) passes.
