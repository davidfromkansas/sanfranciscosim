# Hunter-Dulin Building (111 Sutter Street) — asset report

## Result

**PASS** — `hunter-dulin-building.glb` meets the landmark contract: the kit validator
(`tools/landmark-kit/validate.py`) factory-reset the scene, re-imported only the exported GLB
and printed "all checks pass" (budget 5,000 for a tower ≥ 60 m).
`validation.json` is the machine-readable authority. Not integrated: the manifest,
`pipeline/lib/landmarks.mjs` and app code are untouched.

## Deliverables

- `build_hunter_dulin_building.py` — deterministic build (kit helpers in `tools/landmark-kit/toykit.py`)
- `hunter-dulin-building.glb`, `hunter-dulin-building.blend` — export and authoring scene
- `validate_hunter_dulin_building.py`, `render_hunter_dulin_building.py` — thin wrappers around the kit scripts
- `validation.json`; `hunter-dulin-building-{north,east,south,west,top,aerial,aerial-night}.png`, `hunter-dulin-building-contact-sheet.png`
- `REFERENCE.md`; plan at `docs/asset-plans/hunter-dulin-building.md`

## Contract results

| Check | Result | Evidence |
|---|---|---|
| Crest = target height | PASS | max Z 93.88 m = 93.88 m |
| Plausible metre dimensions | PASS | 61.058 × 47.4516 × 93.88 m |
| Base at Z 0 | PASS | min Z 0.0 m |
| Centred in XY | PASS | offset [0.0, 0.0] m |
| Triangle budget | PASS | 4,190 / 5,000 |
| No image textures / transparency | PASS | 0 images, all alpha 1.0 |
| Flat `Toy_*` materials | PASS | 9 materials, no violations |
| Has night glow | PASS | `Toy_sand_Glow` |
| No cameras / lights / animation | PASS | 0 / 0 / 0 |
| Transforms applied, no negative scale | PASS | 2 mesh objects at identity |
| Normals outward (signed volume) | PASS | inverted objects: [] |
| Normals outward (ray residual) | PASS | 0 flipped of 20,769 first hits |
| Glow skins face outward | PASS | 710 / 710 unobstructed |
| No degenerate geometry | PASS | 0 degenerate triangles |
| No unexpected objects | PASS | none |

Triangles **4,190** (body 3,480, glow 710); dimensions **[61.058, 47.4516, 93.88]** m; anchor
**[-122.4025497, 37.7897258]**; height **93.88 m**; category `3`.
Materials: `Toy_cream`, `Toy_glassd`, `Toy_roofd`, `Toy_rust`, `Toy_sand_Glow`, `Toy_steel`, `Toy_stone`, `Toy_terracotta`, `Toy_verdigris`.

## Night state

`Toy_sand_Glow`: lit shopfront base, scattered office panes, and a floodlight band under each pavilion roof.

## Iterations

- Draft: hipped roofs had long ridges and read as gables; ridge shortened to 22 % of depth so each roof reads as a steep chateau pyramid. 4,190 tris, all checks pass.

## Gate 3 — approval

Approved by David on 2026-10-26 (renders sent as twelve day/night overview sheets): "approve all".

## Stage 4 — optimize

Shipped as `app/public/sf-assets/landmarks/hunter-dulin-building.glb`, meshopt-compressed with the intake flags of `pipeline/compress-assets.mjs` (`gltfpack -c -km -kn -noq`): **229 KB → 95 KB** (59% smaller). Geometry is unchanged. Kit assets are already one body mesh and one glow mesh, so the Blender cleanup pass and the limited dissolve are skipped, as for the Transbay batch. Gate G3 (three.js GLTFLoader round-trip with MeshoptDecoder, `tools/glb-optimize/g3check`) passes.
