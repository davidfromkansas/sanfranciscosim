# 181 Fremont — asset report

## Result

**PASS** — `181-fremont.glb` meets the landmark contract: the kit validator (`tools/landmark-kit/validate.py`,
Blender 5.2.3 LTS) re-imported only the exported GLB into a fresh scene and printed "all checks pass".
`validation.json` is the machine-readable authority. Not yet integrated (the batch is integrated in one pass).

## Deliverables

- `build_181_fremont.py`, `181-fremont.glb`, `181-fremont.blend`
- `validate_181_fremont.py` → `validation.json`; `render_181_fremont.py` → 7 renders + `181-fremont-contact-sheet.png`
- `REFERENCE.md`; plan at `docs/asset-plans/181-fremont.md`

## Contract results

| Check | Value |
|---|---|
| Triangles | 3,346 / 27,000 |
| Dimensions | 50.43 × 50.43 × 244.4 m |
| Min Z | 0.0 |
| XY centre offset | [0.0, 0.0] |
| Crest | 244.4 m (target 244.4) |
| Materials | flat `Toy_*`, roughness 0.85, opaque, no textures |
| Normals, volume, glow facing, degenerates | pass |

Anchor **-122.3953090, 37.7897660**, category `3`.

## Night state

Glow skins over solid geometry: `Toy_red_Glow`, `Toy_sand_Glow`, `Toy_white_Glow`.

## Iterations and notes

- Braces rebuilt as stacked X braces on every face (a tall diamond round each corner), per the photo; the draft had one 'A' per face.
- Lit panes hidden behind braces and mullions removed (glow-outward check was failing); window density raised to 0.5.
- Inferred: crown slope, roof heights (206–220 m) and the two faces the photo does not show.

## Gate 3 — approval

Pending: renders sent to David (`181-fremont-contact-sheet.png`).
