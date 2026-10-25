# 50 Fremont Center (Salesforce West) — asset report

## Result

**PASS** — `50-fremont.glb` meets the landmark contract: the kit validator
(`tools/landmark-kit/validate.py`, Blender 5.2.3 LTS) factory-reset the scene, re-imported
only the exported GLB and printed "all checks pass". `validation.json` is the
machine-readable authority for every number below. Not yet integrated: the manifest,
`pipeline/lib/landmarks.mjs` and app code are untouched (the lead integrates the batch).

## Deliverables

- `build_50_fremont.py` — deterministic build (kit helpers in `tools/landmark-kit/toykit.py`)
- `50-fremont.glb`, `50-fremont.blend` — export and authoring scene
- `validate_50_fremont.py`, `render_50_fremont.py` — thin wrappers around the kit scripts with this building's arguments
- `validation.json` — full machine report
- `50-fremont-{north,east,south,west,top,aerial,aerial-night}.png`, `50-fremont-contact-sheet.png`
- `REFERENCE.md` — sources, dimensions, orientation, cues

Rebuild from this folder:

```bash
blender -b --python build_50_fremont.py
blender -b --python validate_50_fremont.py
blender -b --python render_50_fremont.py
```

## Contract results

| Check | Result | Evidence |
|---|---|---|
| Crest = target height | PASS | max Z 183.0 m = 183.0 m |
| Plausible metre dimensions | PASS | 63.8784 × 63.8451 × 183.0 m |
| Base at Z 0 | PASS | min Z 0.0 m |
| Centred in XY | PASS | offset [0.0, 0.0] m |
| Triangle budget | PASS | 7,780 / 27,000 |
| No image textures | PASS | 0 images |
| No transparency | PASS | all alpha 1.0 |
| Flat `Toy_*` materials | PASS | 13 `Toy_*` materials, no violations |
| Has night glow | PASS | `Toy_sand_Glow`, `Toy_sky_Glow`, `Toy_white_Glow` |
| No cameras / lights | PASS | 0 / 0 |
| No animation / skin / constraints | PASS | 0 / 0 / 0 |
| Transforms applied | PASS | 2 mesh objects at identity |
| No negative scales | PASS | none |
| Normals outward (signed volume) | PASS | inverted objects: 0 |
| Normals outward (ray residual) | PASS | 0 flipped of 19,926 first hits |
| Glow skins face outward | PASS | 1195 / 1196 unobstructed |
| No degenerate geometry | PASS | 0 degenerate triangles |
| No unexpected objects | PASS | none |

## Geometry and materials

- Triangles: **7,780** (`50-fremont_body` 6,584, `50-fremont_night_glow` 1,196); Blender vertices 15,368
- Dimensions: **[63.8784, 63.8451, 183.0] m** (axis-aligned box of the rotated plan + apron)
- Anchor: **[-122.397241, 37.79051]**, target height **183.0 m**, category `3` (Office)
- Materials: `Toy_glass`, `Toy_granite`, `Toy_leaf`, `Toy_leafd`, `Toy_roofd`, `Toy_rust`, `Toy_sand_Glow`, `Toy_sky`, `Toy_sky_Glow`, `Toy_steel`, `Toy_stone`, `Toy_trim`, `Toy_white_Glow`

- Plan: 50 × 36.5 m with 4 m corner notches (the serrated corner bays) on the OSM heading.
- Base 0–11 m: glass inset 1.5 m behind granite piers every 5 m, granite band, warm lit ring.
- Three punched-window tiers in `Toy_stone`/`Toy_glass`: 11–158 m, 158–168 m (inset 2.5 m), 168–176 m (inset 5.5 m), trim cornices at the steps.
- Crown 176–183 m: dark louvred box with steel louvres, white crown light, trim cap; roof kit on the 176 m terrace.
- Salesforce cloud (three `Toy_sky` lobes ~12 m wide + `Toy_sky_Glow`) at 24 m on the Fremont (NE) face; stone apron, three trees on Fremont.

## Night state

`_Glow` surfaces are thin outward skins over solid body geometry, so the daylight
silhouette is unchanged and only light is added at dusk:

- `Toy_sand_Glow`: base ring + scattered lit punched windows.
- `Toy_sky_Glow`: the cloud sign.
- `Toy_white_Glow`: crown light.

## Iterations

- Draft validated clean, but the cloud and street trees were on the SW face (toward First St). The building sits on the west side of Fremont, so its Fremont face is NE: cloud, its glow quad and the trees moved there (glow winding kept outward). 7,780 tris, all checks pass.

## Gate 3 — approval

Pending: renders sent to David (`50-fremont-contact-sheet.png`).
