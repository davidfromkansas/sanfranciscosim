# 333 Market Street — asset report

## Result

**PASS** — `333-market.glb` meets the landmark contract: the kit validator
(`tools/landmark-kit/validate.py`, Blender 5.2.3 LTS) factory-reset the scene, re-imported
only the exported GLB and printed "all checks pass". `validation.json` is the
machine-readable authority for every number below. Not yet integrated: the manifest,
`pipeline/lib/landmarks.mjs` and app code are untouched (the lead integrates the batch).

## Deliverables

- `build_333_market.py` — deterministic build (kit helpers in `tools/landmark-kit/toykit.py`)
- `333-market.glb`, `333-market.blend` — export and authoring scene
- `validate_333_market.py`, `render_333_market.py` — thin wrappers around the kit scripts with this building's arguments
- `validation.json` — full machine report
- `333-market-{north,east,south,west,top,aerial,aerial-night}.png`, `333-market-contact-sheet.png`
- `REFERENCE.md` — sources, dimensions, orientation, cues

Rebuild from this folder:

```bash
blender -b --python build_333_market.py
blender -b --python validate_333_market.py
blender -b --python render_333_market.py
```

## Contract results

| Check | Result | Evidence |
|---|---|---|
| Crest = target height | PASS | max Z 144.0 m = 144.0 m |
| Plausible metre dimensions | PASS | 59.6849 × 59.7516 × 144.0 m |
| Base at Z 0 | PASS | min Z 0.0 m |
| Centred in XY | PASS | offset [0.0, 0.0] m |
| Triangle budget | PASS | 10,990 / 27,000 |
| No image textures | PASS | 0 images |
| No transparency | PASS | all alpha 1.0 |
| Flat `Toy_*` materials | PASS | 9 `Toy_*` materials, no violations |
| Has night glow | PASS | `Toy_sand_Glow` |
| No cameras / lights | PASS | 0 / 0 |
| No animation / skin / constraints | PASS | 0 / 0 / 0 |
| Transforms applied | PASS | 2 mesh objects at identity |
| No negative scales | PASS | none |
| Normals outward (signed volume) | PASS | inverted objects: 0 |
| Normals outward (ray residual) | PASS | 0 flipped of 20,327 first hits |
| Glow skins face outward | PASS | 1214 / 1214 unobstructed |
| No degenerate geometry | PASS | 0 degenerate triangles |
| No unexpected objects | PASS | none |

## Geometry and materials

- Triangles: **10,990** (`333-market_body` 9,776, `333-market_night_glow` 1,214); Blender vertices 16,924
- Dimensions: **[59.6849, 59.7516, 144.0] m** (axis-aligned box of the rotated plan + apron)
- Anchor: **[-122.397403, 37.791938]**, target height **144.0 m**, category `3` (Office)
- Materials: `Toy_bronze`, `Toy_glassd`, `Toy_granite`, `Toy_roofd`, `Toy_sand_Glow`, `Toy_steel`, `Toy_stone`, `Toy_terracotta`, `Toy_trim`

- Plan: 46 × 37 m rectangle with each corner cut into three 2.6 m re-entrant steps, on the OSM heading.
- Base 0–9 m: dark glass inset 2 m behind granite columns every 5 m, warm lit ring.
- Shaft 9–142 m: `Toy_glassd` with thin `Toy_bronze` floor lines and `Toy_terracotta` piers every 2.8 m (0.85 × 0.55 m).
- Cap 142–143.2 m in `Toy_terracotta`; roof kit following the serrated outline. `tk.run` scales Z by 0.985 to land the plant crest at 144 m.
- Stone apron; no trees (Market sidewalk trees are the street kit's).

## Night state

`_Glow` surfaces are thin outward skins over solid body geometry, so the daylight
silhouette is unchanged and only light is added at dusk:

- `Toy_sand_Glow`: base ring + lit panes aligned to the pier bays (1,214 faces).

## Iterations

- Draft (11,718 tris) validated clean, but the 1.9 m pier rhythm read as a fuzzy texture at aerial distance. Piers widened to 2.8 m spacing (0.85 m wide) with lit panes aligned to the bays: crisper pinstripes, 10,990 tris, all checks pass.

## Gate 3 — approval

Pending: renders sent to David (`333-market-contact-sheet.png`).
