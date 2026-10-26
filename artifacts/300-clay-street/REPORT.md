# One Maritime Plaza (Alcoa Building) — asset report

## Result

**PASS** — `300-clay-street.glb` meets the landmark contract: the kit validator
(`tools/landmark-kit/validate.py`) factory-reset the scene, re-imported only the exported GLB
and printed "all checks pass" (budget 5,000 for a tower ≥ 60 m).
`validation.json` is the machine-readable authority. Not integrated: the manifest,
`pipeline/lib/landmarks.mjs` and app code are untouched.

## Deliverables

- `build_300_clay_street.py` — deterministic build (kit helpers in `tools/landmark-kit/toykit.py`)
- `300-clay-street.glb`, `300-clay-street.blend` — export and authoring scene
- `validate_300_clay_street.py`, `render_300_clay_street.py` — thin wrappers around the kit scripts
- `validation.json`; `300-clay-street-{north,east,south,west,top,aerial,aerial-night}.png`, `300-clay-street-contact-sheet.png`
- `REFERENCE.md`; plan at `docs/asset-plans/300-clay-street.md`

## Contract results

| Check | Result | Evidence |
|---|---|---|
| Crest = target height | PASS | max Z 121.3 m = 121.3 m |
| Plausible metre dimensions | PASS | 62.7108 × 88.4797 × 121.3 m |
| Base at Z 0 | PASS | min Z 0.0 m |
| Centred in XY | PASS | offset [0.0, 0.0] m |
| Triangle budget | PASS | 4,622 / 5,000 |
| No image textures / transparency | PASS | 0 images, all alpha 1.0 |
| Flat `Toy_*` materials | PASS | 12 materials, no violations |
| Has night glow | PASS | `Toy_sand_Glow`, `Toy_white_Glow` |
| No cameras / lights / animation | PASS | 0 / 0 / 0 |
| Transforms applied, no negative scale | PASS | 2 mesh objects at identity |
| Normals outward (signed volume) | PASS | inverted objects: [] |
| Normals outward (ray residual) | PASS | 0 flipped of 20,713 first hits |
| Glow skins face outward | PASS | 598 / 598 unobstructed |
| No degenerate geometry | PASS | 0 degenerate triangles |
| No unexpected objects | PASS | none |

Triangles **4,622** (body 4,024, glow 598); dimensions **[62.7108, 88.4797, 121.3]** m; anchor
**[-122.3992506, 37.7956183]**; height **121.3 m**; category `3`.
Materials: `Toy_bronze`, `Toy_glassd`, `Toy_glassg`, `Toy_ink`, `Toy_leaf`, `Toy_leafd`, `Toy_roofd`, `Toy_rust`, `Toy_sand_Glow`, `Toy_steel`, `Toy_stone`, `Toy_white_Glow`.

## Night state

`Toy_sand_Glow`: lobby ring and scattered panes behind the lattice; `Toy_white_Glow`: crown line on the fascia.

## Iterations

- Draft (before the photo arrived) used 6 × 3 bays × 6 tiers without columns; rebuilt to the photo's 4 × 2 bays × 7 tiers with bay columns and tier ties.
- Two drafts were over the 5,000 cap (5,110; 5,294); trimmed plaza trees and dropped a louvre pier grid: 4,622 tris, all checks pass.
- First render: bronze glass behind the dark lattice read as one dark mass; the glass became pale `Toy_glassg` (the photo's reflective panes) so the Xs stand out.

## Gate 3 — approval

Approved by David on 2026-10-26 (renders sent as twelve day/night overview sheets): "approve all".

## Stage 4 — optimize

Shipped as `app/public/sf-assets/landmarks/300-clay-street.glb`, meshopt-compressed with the intake flags of `pipeline/compress-assets.mjs` (`gltfpack -c -km -kn -noq`): **243 KB → 114 KB** (53% smaller). Geometry is unchanged. Kit assets are already one body mesh and one glow mesh, so the Blender cleanup pass and the limited dissolve are skipped, as for the Transbay batch. Gate G3 (three.js GLTFLoader round-trip with MeshoptDecoder, `tools/glb-optimize/g3check`) passes.
