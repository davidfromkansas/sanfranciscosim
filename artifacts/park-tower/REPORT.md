# Park Tower at Transbay — asset report

## Result

**PASS** — `park-tower.glb` meets the landmark contract: the kit validator (`tools/landmark-kit/validate.py`,
Blender 5.2.3 LTS) re-imported only the exported GLB into a fresh scene and printed "all checks pass".
`validation.json` is the machine-readable authority. Not yet integrated (the batch is integrated in one pass).

## Deliverables

- `build_park_tower.py`, `park-tower.glb`, `park-tower.blend`
- `validate_park_tower.py` → `validation.json`; `render_park_tower.py` → 7 renders + `park-tower-contact-sheet.png`
- `REFERENCE.md`; plan at `docs/asset-plans/park-tower.md`

## Contract results

| Check | Value |
|---|---|
| Triangles | 5,054 / 27,000 |
| Dimensions | 81.88 × 81.88 × 183.0 m |
| Min Z | 0.0 |
| XY centre offset | [0.0, 0.0] |
| Crest | 183.0 m (target 183.0) |
| Materials | flat `Toy_*`, roughness 0.85, opaque, no textures |
| Normals, volume, glow facing, degenerates | pass |

Anchor **-122.3942790, 37.7904360**, category `3`.

## Night state

Glow skins over solid geometry: `Toy_sand_Glow`, `Toy_white_Glow`.

## Iterations and notes

- Notch corner corrected from the photo: terraces on the true EAST corner of the Howard face, and the WEST corner steps back at the same height (Wikipedia's 'NW and SE corners' uses street-grid directions).
- Two notches (east and west) starting at ~116 m instead of one at 136 m; crown screen follows the notched plan.
- Doubtful: whether the west corner is terraces or a plain setback; the 116 m start. Height 183 m (Wikipedia 605 ft = 184.4 m).

## Gate 3 — approval

Pending: renders sent to David (`park-tower-contact-sheet.png`).
