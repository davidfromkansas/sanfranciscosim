# 45 Fremont Street — asset report

## Result

**PASS** — `45-fremont.glb` meets the landmark contract: the kit validator
(`tools/landmark-kit/validate.py`, Blender 5.2.3 LTS) factory-reset the scene, re-imported
only the exported GLB and printed "all checks pass". `validation.json` is the
machine-readable authority for every number below. Not yet integrated: the manifest,
`pipeline/lib/landmarks.mjs` and app code are untouched (the lead integrates the batch).

## Deliverables

- `build_45_fremont.py` — deterministic build (kit helpers in `tools/landmark-kit/toykit.py`)
- `45-fremont.glb`, `45-fremont.blend` — export and authoring scene
- `validate_45_fremont.py`, `render_45_fremont.py` — thin wrappers around the kit scripts with this building's arguments
- `validation.json` — full machine report
- `45-fremont-{north,east,south,west,top,aerial,aerial-night}.png`, `45-fremont-contact-sheet.png`
- `REFERENCE.md` — sources, dimensions, orientation, cues

Rebuild from this folder:

```bash
blender -b --python build_45_fremont.py
blender -b --python validate_45_fremont.py
blender -b --python render_45_fremont.py
```

## Contract results

| Check | Result | Evidence |
|---|---|---|
| Crest = target height | PASS | max Z 145.0 m = 145.0 m |
| Plausible metre dimensions | PASS | 57.7729 × 57.6396 × 145.0 m |
| Base at Z 0 | PASS | min Z 0.0 m |
| Centred in XY | PASS | offset [0.0, 0.0] m |
| Triangle budget | PASS | 4,064 / 27,000 |
| No image textures | PASS | 0 images |
| No transparency | PASS | all alpha 1.0 |
| Flat `Toy_*` materials | PASS | 11 `Toy_*` materials, no violations |
| Has night glow | PASS | `Toy_sand_Glow` |
| No cameras / lights | PASS | 0 / 0 |
| No animation / skin / constraints | PASS | 0 / 0 / 0 |
| Transforms applied | PASS | 2 mesh objects at identity |
| No negative scales | PASS | none |
| Normals outward (signed volume) | PASS | inverted objects: 0 |
| Normals outward (ray residual) | PASS | 0 flipped of 21,639 first hits |
| Glow skins face outward | PASS | 968 / 968 unobstructed |
| No degenerate geometry | PASS | 0 degenerate triangles |
| No unexpected objects | PASS | none |

## Geometry and materials

- Triangles: **4,064** (`45-fremont_body` 3,096, `45-fremont_night_glow` 968); Blender vertices 7,016
- Dimensions: **[57.7729, 57.6396, 145.0] m** (axis-aligned box of the rotated plan + apron)
- Anchor: **[-122.397149, 37.791231]**, target height **145.0 m**, category `3` (Office)
- Materials: `Toy_cream`, `Toy_glass`, `Toy_glassd`, `Toy_leaf`, `Toy_leafd`, `Toy_roofd`, `Toy_rust`, `Toy_sand_Glow`, `Toy_steel`, `Toy_stone`, `Toy_trim`

- Plan: 45.5 × 36.5 m with 4.5 m chamfered corners on the OSM heading.
- Base 0–8 m: dark glass core inset 2.5 m behind cream columns every 7 m, warm lit ring.
- Shaft 8–142 m: 33 whole storeys (4.06 m), `Toy_glassd` ribbon windows between 2.3 m `Toy_cream` spandrels 0.45 m proud.
- Cream roof band 142–144.4 m; roof kit (parapet, deck, plant). `tk.run` scales Z by 0.979 to land the plant crest at 145 m.
- Stone apron, three trees on Fremont (SW).

## Night state

`_Glow` surfaces are thin outward skins over solid body geometry, so the daylight
silhouette is unchanged and only light is added at dusk:

- `Toy_sand_Glow`: base ring + scattered lit office panes in the ribbon windows (968 faces).

## Iterations

- Draft failed validation: 16 degenerate triangles — 4.0 m did not divide the 134 m shaft, so the loft ended in a zero-height sliver ring.
- Fix: pitch = shaft / 33 (whole storeys). Massing otherwise unchanged; aerial read against the photo was already right. 4,064 tris, all checks pass.

## Gate 3 — approval

Pending: renders sent to David (`45-fremont-contact-sheet.png`).
