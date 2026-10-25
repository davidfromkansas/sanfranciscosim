# 60 Spear Street — asset report

## Result

**PASS** — `60-spear.glb` meets the landmark contract: the kit validator
(`tools/landmark-kit/validate.py`, Blender 5.2.3 LTS) factory-reset the scene, re-imported
only the exported GLB and printed "all checks pass". `validation.json` is the
machine-readable authority for every number below. Not yet integrated: the manifest,
`pipeline/lib/landmarks.mjs` and app code are untouched (the lead integrates the batch).

## Deliverables

- `build_60_spear.py` — deterministic build (kit helpers in `tools/landmark-kit/toykit.py`)
- `60-spear.glb`, `60-spear.blend` — export and authoring scene
- `validate_60_spear.py`, `render_60_spear.py` — thin wrappers around the kit scripts with this building's arguments
- `validation.json` — full machine report
- `60-spear-{north,east,south,west,top,aerial,aerial-night}.png`, `60-spear-contact-sheet.png`
- `REFERENCE.md` — sources, dimensions, orientation, cues

Rebuild from this folder:

```bash
blender -b --python build_60_spear.py
blender -b --python validate_60_spear.py
blender -b --python render_60_spear.py
```

## Contract results

| Check | Result | Evidence |
|---|---|---|
| Crest = target height | PASS | max Z 57.9 m = 57.9 m |
| Plausible metre dimensions | PASS | 58.216 × 58.174 × 57.9 m |
| Base at Z 0 | PASS | min Z 0.0 m |
| Centred in XY | PASS | offset [0.0, 0.0] m |
| Triangle budget | PASS | 2,238 / 27,000 |
| No image textures | PASS | 0 images |
| No transparency | PASS | all alpha 1.0 |
| Flat `Toy_*` materials | PASS | 10 `Toy_*` materials, no violations |
| Has night glow | PASS | `Toy_sand_Glow` |
| No cameras / lights | PASS | 0 / 0 |
| No animation / skin / constraints | PASS | 0 / 0 / 0 |
| Transforms applied | PASS | 2 mesh objects at identity |
| No negative scales | PASS | none |
| Normals outward (signed volume) | PASS | inverted objects: 0 |
| Normals outward (ray residual) | PASS | 0 flipped of 20,400 first hits |
| Glow skins face outward | PASS | 262 / 262 unobstructed |
| No degenerate geometry | PASS | 0 degenerate triangles |
| No unexpected objects | PASS | none |

## Geometry and materials

- Triangles: **2,238** (`60-spear_body` 1,976, `60-spear_night_glow` 262)
- Dimensions: **[58.216, 58.174, 57.9] m** (axis-aligned box of the rotated plan + apron)
- Anchor: **[-122.394585, 37.792566]**, target height **57.9 m**, category `3` (Office)
- Materials: `Toy_glass`, `Toy_glassl`, `Toy_leaf`, `Toy_leafd`, `Toy_roofd`, `Toy_rust`, `Toy_sand_Glow`, `Toy_steel`, `Toy_stone`, `Toy_trim`

- Plan: 39.5 × 31 m rectangle (OSM OBB 40.4 × 31.6 m) on the OSM heading (long axis 134.8°, along Spear St).
- Base 0–6 m: `Toy_glass` inset 1.5 m behind `Toy_stone` piers every 4 m, warm lit ring.
- Shaft 6–51.2 m: 11 equal storeys of `Toy_glass` with `Toy_stone` floor bands and stone fins every 4 m (a stone grid).
- Terrace slab at 51.2 m; `Toy_glassl` top storey set back 2.2 m to the 55.4 m roof plane, with a lit ring, trim parapet and two terrace trees.
- Roof plant cluster to the 57.9 m crest; stone apron; three street trees on the Spear St sidewalk.
- **The whole facade is inferred** (no photo, no Wikipedia article). Massing and heights are measured.
- Off-palette tones (WARN, not fail): `Toy_leaf`, `Toy_leafd`.

## Night state

`_Glow` surfaces are thin outward skins over solid body geometry, so the daylight
silhouette is unchanged and only light is added at dusk:

- `Toy_sand_Glow`: base ring, ~30% lit shaft panes and the top-storey ring (262 faces).

## Iterations

- Draft reviewed against the aerial: proportions match the OSM block and LiDAR heights; kept.
- First validation failed `no_degenerate_geometry` (8 sliver triangles): the 4.1 m storey pitch left a zero-height final band at the shaft top. Pitch set to exactly 1/11 of the shaft. Street trees moved from the mid-block SW side to the Spear St sidewalk. 2,238 tris, all checks pass.
- One Commons search for a photo was attempted (twice); both returned HTTP 429, so the facade stays inferred.

## Gate 3 — approval

Pending: renders sent to David (`60-spear-contact-sheet.png`).
