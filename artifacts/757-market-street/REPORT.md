# Four Seasons Hotel and Residences (757 Market Street) — asset report

## Result

**PASS** — `757-market-street.glb` meets the landmark contract: the kit validator
(`tools/landmark-kit/validate.py`) factory-reset the scene, re-imported only the exported GLB
and printed "all checks pass" (budget 5,000 for a tower ≥ 60 m).
`validation.json` is the machine-readable authority. Not integrated: the manifest,
`pipeline/lib/landmarks.mjs` and app code are untouched.

## Deliverables

- `build_757_market_street.py` — deterministic build (kit helpers in `tools/landmark-kit/toykit.py`)
- `757-market-street.glb`, `757-market-street.blend` — export and authoring scene
- `validate_757_market_street.py`, `render_757_market_street.py` — thin wrappers around the kit scripts
- `validation.json`; `757-market-street-{north,east,south,west,top,aerial,aerial-night}.png`, `757-market-street-contact-sheet.png`
- `REFERENCE.md`; plan at `docs/asset-plans/757-market-street.md`

## Contract results

| Check | Result | Evidence |
|---|---|---|
| Crest = target height | PASS | max Z 130.1 m = 130.1 m |
| Plausible metre dimensions | PASS | 108.8653 × 109.8358 × 130.1 m |
| Base at Z 0 | PASS | min Z 0.0 m |
| Centred in XY | PASS | offset [0.0, 0.0] m |
| Triangle budget | PASS | 4,738 / 5,000 |
| No image textures / transparency | PASS | 0 images, all alpha 1.0 |
| Flat `Toy_*` materials | PASS | 9 materials, no violations |
| Has night glow | PASS | `Toy_sand_Glow`, `Toy_white_Glow` |
| No cameras / lights / animation | PASS | 0 / 0 / 0 |
| Transforms applied, no negative scale | PASS | 2 mesh objects at identity |
| Normals outward (signed volume) | PASS | inverted objects: [] |
| Normals outward (ray residual) | PASS | 0 flipped of 18,332 first hits |
| Glow skins face outward | PASS | 890 / 890 unobstructed |
| No degenerate geometry | PASS | 0 degenerate triangles |
| No unexpected objects | PASS | none |

Triangles **4,738** (body 3,848, glow 890); dimensions **[108.8653, 109.8358, 130.1]** m; anchor
**[-122.4042447, 37.7862212]**; height **130.1 m**; category `7`.
Materials: `Toy_glass`, `Toy_glassd`, `Toy_leafd`, `Toy_roofd`, `Toy_sand`, `Toy_sand_Glow`, `Toy_steel`, `Toy_stone`, `Toy_white_Glow`.

## Night state

`Toy_sand_Glow`: lit shopfronts and scattered hotel/residence windows; `Toy_white_Glow`: crown line.

## Iterations

- First build was 5,206 tris (over the cap); coarser pane spacing gave 4,738 tris, all checks pass.
- First render: podium plant cluster sat in the tower's re-entrant notch; plant and garden moved onto the open podium roof.

## Gate 3 — approval

Approved by David on 2026-10-26 (renders sent as twelve day/night overview sheets): "approve all".

## Stage 4 — optimize

Shipped as `app/public/sf-assets/landmarks/757-market-street.glb`, meshopt-compressed with the intake flags of `pipeline/compress-assets.mjs` (`gltfpack -c -km -kn -noq`): **254 KB → 105 KB** (59% smaller). Geometry is unchanged. Kit assets are already one body mesh and one glow mesh, so the Blender cleanup pass and the limited dissolve are skipped, as for the Transbay batch. Gate G3 (three.js GLTFLoader round-trip with MeshoptDecoder, `tools/glb-optimize/g3check`) passes.
