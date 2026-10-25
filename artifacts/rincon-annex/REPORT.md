# Rincon Annex (Rincon Center) — asset report

## Result

**PASS** — `rincon-annex.glb` meets the landmark contract: the kit validator
(`tools/landmark-kit/validate.py`, Blender 5.2.3 LTS) factory-reset the scene, re-imported
only the exported GLB and printed "all checks pass". `validation.json` is the
machine-readable authority for every number below. Not yet integrated: the manifest,
`pipeline/lib/landmarks.mjs` and app code are untouched (the lead integrates the batch).

## Deliverables

- `build_rincon_annex.py` — deterministic build (kit helpers in `tools/landmark-kit/toykit.py`)
- `rincon-annex.glb`, `rincon-annex.blend` — export and authoring scene
- `validate_rincon_annex.py`, `render_rincon_annex.py` — thin wrappers around the kit scripts with this building's arguments
- `validation.json` — full machine report
- `rincon-annex-{north,east,south,west,top,aerial,aerial-night}.png`, `rincon-annex-contact-sheet.png`
- `REFERENCE.md` — sources, dimensions, orientation, cues

Rebuild from this folder:

```bash
blender -b --python build_rincon_annex.py
blender -b --python validate_rincon_annex.py
blender -b --python render_rincon_annex.py
```

## Contract results

| Check | Result | Evidence |
|---|---|---|
| Crest = target height | PASS | max Z 29.7 m = 29.7 m |
| Plausible metre dimensions | PASS | 129.4039 × 130.5617 × 29.7 m |
| Base at Z 0 | PASS | min Z 0.0 m |
| Centred in XY | PASS | offset [0.0, 0.0] m |
| Triangle budget | PASS | 1,546 / 27,000 |
| No image textures | PASS | 0 images |
| No transparency | PASS | all alpha 1.0 |
| Flat `Toy_*` materials | PASS | 11 `Toy_*` materials, no violations |
| Has night glow | PASS | `Toy_sand_Glow` |
| No cameras / lights | PASS | 0 / 0 |
| No animation / skin / constraints | PASS | 0 / 0 / 0 |
| Transforms applied | PASS | 2 mesh objects at identity |
| No negative scales | PASS | none |
| Normals outward (signed volume) | PASS | inverted objects: 0 |
| Normals outward (ray residual) | PASS | 0 flipped of 20,807 first hits |
| Glow skins face outward | PASS | 72 / 72 unobstructed |
| No degenerate geometry | PASS | 0 degenerate triangles |
| No unexpected objects | PASS | none |

## Geometry and materials

- Triangles: **1,546** (`rincon-annex_body` 1,474, `rincon-annex_night_glow` 72)
- Dimensions: **[129.4039, 130.5617, 29.7] m** (axis-aligned box of the rotated plan + apron)
- Anchor: **[-122.3931571, 37.7925049]**, target height **29.7 m**, category `3` (Office)
- Materials: `Toy_glassl`, `Toy_ink`, `Toy_leaf`, `Toy_leafd`, `Toy_roofd`, `Toy_rust`, `Toy_sand_Glow`, `Toy_sky`, `Toy_steel`, `Toy_stone`, `Toy_white`

- Plan: OSM way 44106213 simplified to 8 points, on yaw 45.7° (Mission St front to the NW).
- `Toy_glassl` blue-grey base 0–2.4 m; `Toy_white` plaster body to 16.9 m; `Toy_glassl` cornice band to the 18.1 m parapet; dark roof deck.
- Windows: tall `Toy_ink` openings 3.0–11.0 m every 6.5 m, `Toy_sky` dolphin-frieze panels 10.9–12.3 m above each, small third-storey windows 12.4–15.2 m.
- Rincon Center atrium skylight on the SE side: 34 × 22 m white drum to 23.5 m and a `Toy_glassl` pyramid to the 29.7 m crest (position **inferred** from the LiDAR crest).
- Roof: four long skylight strips over the old sorting floor (**inferred**), one plant cluster.
- Sidewalk apron with five street trees along Mission St. The Towers at Rincon are not modelled.
- Off-palette tones (WARN, not fail): `Toy_leaf`, `Toy_leafd`.

## Night state

`_Glow` surfaces are thin outward skins over solid body geometry, so the daylight
silhouette is unchanged and only light is added at dusk:

- `Toy_sand_Glow`: ~60% of the tall windows lit + a ring round the atrium drum (72 faces).

## Iterations

- Draft reviewed against the aerial and the Commons photo: massing, base/cornice colours and window rhythm match. Fixes: the Mission St trees sat inside the building (local y 36 m; the NW face is at ~45–47 m) and were moved onto the sidewalk; the dolphin panels were enlarged (1 → 1.4 m tall) and kept clear of the third-storey windows. 1,546 tris, all checks pass.

## Gate 3 — approval

Pending: renders sent to David (`rincon-annex-contact-sheet.png`).
