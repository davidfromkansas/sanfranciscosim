# 425 Market Street — asset report

## Result

**PASS** — `425-market.glb` meets the landmark contract: the kit validator
(`tools/landmark-kit/validate.py`, Blender 5.2.3 LTS) factory-reset the scene, re-imported
only the exported GLB and printed "all checks pass". `validation.json` is the
machine-readable authority for every number below. Not yet integrated: the manifest,
`pipeline/lib/landmarks.mjs` and app code are untouched (the lead integrates the batch).

## Deliverables

- `build_425_market.py` — deterministic build (kit helpers in `tools/landmark-kit/toykit.py`)
- `425-market.glb`, `425-market.blend` — export and authoring scene
- `validate_425_market.py`, `render_425_market.py` — thin wrappers around the kit scripts with this building's arguments
- `validation.json` — full machine report
- `425-market-{north,east,south,west,top,aerial,aerial-night}.png`, `425-market-contact-sheet.png`
- `REFERENCE.md` — sources, dimensions, orientation, cues

Rebuild from this folder:

```bash
blender -b --python build_425_market.py
blender -b --python validate_425_market.py
blender -b --python render_425_market.py
```

## Contract results

| Check | Result | Evidence |
|---|---|---|
| Crest = target height | PASS | max Z 160.0 m = 160.0 m |
| Plausible metre dimensions | PASS | 80.1431 × 80.0876 × 160.0 m |
| Base at Z 0 | PASS | min Z 0.0 m |
| Centred in XY | PASS | offset [0.0, 0.0] m |
| Triangle budget | PASS | 6,756 / 27,000 |
| No image textures | PASS | 0 images |
| No transparency | PASS | all alpha 1.0 |
| Flat `Toy_*` materials | PASS | 9 `Toy_*` materials, no violations |
| Has night glow | PASS | `Toy_sand_Glow` |
| No cameras / lights | PASS | 0 / 0 |
| No animation / skin / constraints | PASS | 0 / 0 / 0 |
| Transforms applied | PASS | 2 mesh objects at identity |
| No negative scales | PASS | none |
| Normals outward (signed volume) | PASS | inverted objects: 0 |
| Normals outward (ray residual) | PASS | 0 flipped of 20,160 first hits |
| Glow skins face outward | PASS | 1316 / 1316 unobstructed |
| No degenerate geometry | PASS | 0 degenerate triangles |
| No unexpected objects | PASS | none |

## Geometry and materials

- Triangles: **6,756** (`425-market_body` 5,440, `425-market_night_glow` 1,316); Blender vertices 13,032
- Dimensions: **[80.1431, 80.0876, 160.0] m** (axis-aligned box of the rotated plan + apron)
- Anchor: **[-122.398153, 37.791204]**, target height **160.0 m**, category `3` (Office)
- Materials: `Toy_glass`, `Toy_glassd`, `Toy_leaf`, `Toy_leafd`, `Toy_roofd`, `Toy_rust`, `Toy_sand_Glow`, `Toy_steel`, `Toy_stone`

- Plan: 60 × 37.5 m rectangle on the OSM heading.
- Base 0–9 m: glass inset 3 m behind a steel colonnade every 6 m, warm lit ring.
- Shaft 9–152 m: `Toy_glass` with 1.1 m `Toy_steel` bands per 4.1 m storey and steel fins every 3 m (the silver grid).
- Roof 152 m: steel parapet base + plant row; penthouse inset 2 m with steel louvres over dark glass, steel cap and plant cluster to 160 m.
- Stone apron (4 m), four trees on Fremont (NE).

## Night state

`_Glow` surfaces are thin outward skins over solid body geometry, so the daylight
silhouette is unchanged and only light is added at dusk:

- `Toy_sand_Glow`: base ring + scattered lit office panes (1,316 faces).

## Iterations

- Draft validated clean; aerial read against the photo was right. The street trees were on the SW (First St) face; moved to Fremont (NE), the photographed street side. 6,756 tris, all checks pass.

## Gate 3 — approval

Approved by David on 2026-10-25 (contact sheets sent in four batches of five): "approve all".

## Stage 4 — optimize

Shipped as `app/public/sf-assets/landmarks/425-market.glb`, meshopt-compressed with the intake flags of `pipeline/compress-assets.mjs` (`gltfpack -c -km -kn -noq`): **361 KB → 160 KB** (56% smaller). Geometry is unchanged. The kit merges every landmark into one body mesh and one glow mesh, so the Phase B cleanup in `tools/glb-optimize/` finds nothing to join or weld; a trial run saved 0 triangles and grew the file 1–5%, so it was not applied. The limited dissolve is skipped as GLB-OPTIMIZE-PROMPT §3 step 3 requires for assets with ring bands and parapets. Gate G3 (three.js GLTFLoader round-trip with MeshoptDecoder, `tools/glb-optimize/g3check`) passes.
