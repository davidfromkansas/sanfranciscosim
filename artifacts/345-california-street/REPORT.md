# 345 California Center — build report

Miniature GLB for SF-SIM, Financial District batch (stages 1–2 of
docs/asset-pipeline/ADDRESS-TO-ASSET.md, BATCH mode), built 2026-10-25 from
`docs/asset-plans/345-california-street.md` with the shared kit in `tools/landmark-kit/`.

## Result

Validation **PASS** ("all checks pass", run with `--budget 5000`). 4,924 triangles.
Crest 211.8 m = target height — published architectural top 211.8 m (695 ft, top of the twin shafts); LiDAR 212 m agrees; roof 189 m (620 ft); masts to 721 ft not modelled.

## Deliverables

- `build_345_california_street.py` — deterministic build (`blender -b --python build_345_california_street.py`)
- `345-california-street.glb`, `345-california-street.blend`
- `validate_345_california_street.py` → `validation.json`; `render_345_california_street.py` → renders below
- Renders: `345-california-street-aerial-night.png`, `345-california-street-aerial.png`, `345-california-street-contact-sheet.png`, `345-california-street-east.png`, `345-california-street-north.png`, `345-california-street-south.png`, `345-california-street-top.png`, `345-california-street-west.png`
- `REFERENCE.md` (sources, dimensions, cues, uncertainties)

## Contract (from validation.json, fresh-scene re-import)

| | |
|---|---|
| Triangles | 4,924 |
| Dimensions | 95.6132 x 59.5307 x 211.8 m (world-axis bbox) |
| min Z / XY centre offset | 0.0 / (0.0, 0.0) |
| Objects | 2 |
| Materials | Toy_concrete, Toy_glassd, Toy_glassl, Toy_red_Glow, Toy_roofd, Toy_sand_Glow, Toy_steel, Toy_stone, Toy_white_Glow |
| Anchor | [-122.4004566, 37.7925878] |

| Check | Result |
|---|---|
| Crest = target height | PASS |
| Plausible metre dimensions | PASS |
| Base at Z 0 | PASS |
| Centred in XY | PASS |
| Triangle budget (5,000 cap) | PASS |
| No image textures | PASS |
| No transparency | PASS |
| Flat `Toy_*` materials | PASS |
| Has night glow | PASS |
| No cameras / lights | PASS |
| No animation / skin / constraints | PASS |
| Transforms applied | PASS |
| No negative scales | PASS |
| Normals outward (signed volume) | PASS |
| Normals outward (ray residual) | PASS |
| Glow skins face outward | PASS |
| No degenerate geometry | PASS |
| No unexpected objects | PASS |

## Geometry and materials

- Podium: full OSM rectangle 0–20 m, `Toy_concrete` with lit windows, deck and parapet.
- Slab: 66 × 36 m chamfered rectangle 20–154 m, 32 storeys of square `Toy_glassd` windows (5.2 m bays).
- Hotel towers: 22 m squares at ±17 m rotated 45°, 154–189 m, windows, deck, parapet, plant, crown lines.
- Glazed core 10 × 8 m between them with lit faces; twin `Toy_concrete` shafts 4.2 m → 2.6 m (step at 199 m) to 211.8 m, red tip lights.

All materials are flat `Toy_*` (roughness 0.85, no textures, no alpha). Off-palette: `Toy_concrete`, `Toy_glassd`.

## Night state

Lit office window pairs (30%), lit hotel windows (45%), lit glass core, white hotel crown lines, red shaft tips. Glow materials: `Toy_red_Glow`, `Toy_sand_Glow`, `Toy_white_Glow`; all laid as thin outward skins over solid faces (674 of 680 glow faces unobstructed outward).

## Iterations

- Draft (before the photo arrived) had small turrets with pyramid roofs and thin spires; the photo shows wide rotated hotel towers with square concrete shafts and a glazed core, so the top was rebuilt and the colour changed from rose to grey.
- First rebuild was 5,418 tris; window bays widened. Final 4,924 tris, all checks pass.

## Gate 3 — approval

Approved by David on 2026-10-26 (renders sent as twelve day/night overview sheets): "approve all".

## Stage 4 — optimize

Shipped as `app/public/sf-assets/landmarks/345-california-street.glb`, meshopt-compressed with the intake flags of `pipeline/compress-assets.mjs` (`gltfpack -c -km -kn -noq`): **267 KB → 105 KB** (61% smaller). Geometry is unchanged. Kit assets are already one body mesh and one glow mesh, so the Blender cleanup pass and the limited dissolve are skipped, as for the Transbay batch. Gate G3 (three.js GLTFLoader round-trip with MeshoptDecoder, `tools/glb-optimize/g3check`) passes.
