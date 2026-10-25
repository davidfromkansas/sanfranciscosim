# Federal Reserve Bank of San Francisco — asset report

## Result

**PASS** — `federal-reserve.glb` meets the landmark contract: the kit validator
(`tools/landmark-kit/validate.py`, Blender 5.2.3 LTS) factory-reset the scene, re-imported
only the exported GLB and printed "all checks pass". `validation.json` is the
machine-readable authority for every number below. Not yet integrated: the manifest,
`pipeline/lib/landmarks.mjs` and app code are untouched (the lead integrates the batch).

## Deliverables

- `build_federal_reserve.py` — deterministic build (kit helpers in `tools/landmark-kit/toykit.py`)
- `federal-reserve.glb`, `federal-reserve.blend` — export and authoring scene
- `validate_federal_reserve.py`, `render_federal_reserve.py` — thin wrappers around the kit scripts with this building's arguments
- `validation.json` — full machine report
- `federal-reserve-{north,east,south,west,top,aerial,aerial-night}.png`, `federal-reserve-contact-sheet.png`
- `REFERENCE.md` — sources, dimensions, orientation, cues

Rebuild from this folder:

```bash
blender -b --python build_federal_reserve.py
blender -b --python validate_federal_reserve.py
blender -b --python render_federal_reserve.py
```

## Contract results

| Check | Result | Evidence |
|---|---|---|
| Crest = target height | PASS | max Z 63.1 m = 63.1 m |
| Plausible metre dimensions | PASS | 129.9662 × 129.9662 × 63.1 m |
| Base at Z 0 | PASS | min Z 0.0 m |
| Centred in XY | PASS | offset [0.0, 0.0] m |
| Triangle budget | PASS | 4,514 / 27,000 |
| No image textures | PASS | 0 images |
| No transparency | PASS | all alpha 1.0 |
| Flat `Toy_*` materials | PASS | 9 `Toy_*` materials, no violations |
| Has night glow | PASS | `Toy_sand_Glow` |
| No cameras / lights | PASS | 0 / 0 |
| No animation / skin / constraints | PASS | 0 / 0 / 0 |
| Transforms applied | PASS | 2 mesh objects at identity |
| No negative scales | PASS | none |
| Normals outward (signed volume) | PASS | inverted objects: 0 |
| Normals outward (ray residual) | PASS | 0 flipped of 21,246 first hits |
| Glow skins face outward | PASS | 663 / 674 unobstructed |
| No degenerate geometry | PASS | 0 degenerate triangles |
| No unexpected objects | PASS | none |

## Geometry and materials

- Triangles: **4,514** (`federal-reserve_body` 3,840, `federal-reserve_night_glow` 674)
- Dimensions: **[129.9662, 129.9662, 63.1] m** (axis-aligned box of the rotated plan + apron)
- Anchor: **[-122.39552, 37.793002]**, target height **63.1 m**, category `18` (Government)
- Materials: `Toy_bronze`, `Toy_glassd`, `Toy_leaf`, `Toy_leafd`, `Toy_roofd`, `Toy_rust`, `Toy_sand_Glow`, `Toy_steel`, `Toy_stone`

- Slab 84 × 34 m along Market (yaw 45°): `Toy_glassd` lobby 0–9 m inset 2 m; 9–60.5 m in 12 equal storeys of `Toy_bronze` ribbon glass under 2.2 m `Toy_stone` travertine bands standing 0.5 m proud.
- Colonnade along Market, 84 × 12 m: 12 stone piers, stone roof slab at 9 m, and one stone planter box (5 × 4 m) with a `Toy_leaf` shrub mass per bay — the photo's signature terrace.
- Rear operations block 80 × 40 m toward Mission, 0–23.9 m (height **estimated**), same banded skin, roof kit.
- Slab roof: deck, 1.2 m stone parapet, two low plant clusters capped under the crest, 30 × 14 m stone penthouse to the 63.1 m crest.
- Plinth; six street trees along Market.
- Off-palette tones (WARN, not fail): `Toy_bronze`, `Toy_glassd`, `Toy_leaf`, `Toy_leafd`.

## Night state

`_Glow` surfaces are thin outward skins over solid body geometry, so the daylight
silhouette is unchanged and only light is added at dusk:

- `Toy_sand_Glow`: lobby ring + ~32% lit slab panes + ~22% on the rear block (674 faces; 663 unobstructed, within tolerance).

## Iterations

- Draft: the slab roof kit's plant rose to 64.5 m, so `tk.run` squashed the whole model by 0.979 to land the crest. Replaced with a parapet + plant capped at the LiDAR crest (no Z normalization now).
- First validation failed `no_degenerate_geometry` (16 sliver triangles): the 4.25 / 4.6 m storey pitches left zero-height bands at the shaft tops. Pitches set to whole storeys (12 and 5).
- The colonnade was deepened (10 → 12 m) and its isolated terrace trees became a planter box + shrub per bay, as in the photo. 4,514 tris, all checks pass.

## Gate 3 — approval

Pending: renders sent to David (`federal-reserve-contact-sheet.png`).
