# Millennium Tower — asset report

## Result

**PASS** — `millennium-tower.glb` meets the landmark contract: the kit validator (`tools/landmark-kit/validate.py`,
Blender 5.2.3 LTS) re-imported only the exported GLB into a fresh scene and printed "all checks pass".
`validation.json` is the machine-readable authority. Not yet integrated (the batch is integrated in one pass).

## Deliverables

- `build_millennium_tower.py`, `millennium-tower.glb`, `millennium-tower.blend`
- `validate_millennium_tower.py` → `validation.json`; `render_millennium_tower.py` → 7 renders + `millennium-tower-contact-sheet.png`
- `REFERENCE.md`; plan at `docs/asset-plans/millennium-tower.md`

## Contract results

| Check | Value |
|---|---|
| Triangles | 9,766 / 27,000 |
| Dimensions | 53.28 × 53.48 × 197.0 m |
| Min Z | 0.0 |
| XY centre offset | [0.0, 0.0] |
| Crest | 197.0 m (target 197.0) |
| Materials | flat `Toy_*`, roughness 0.85, opaque, no textures |
| Normals, volume, glow facing, degenerates | pass |

Anchor **-122.3961910, 37.7904150**, category `2`.

## Night state

Glow skins over solid geometry: `Toy_sand_Glow`, `Toy_white_Glow`.

## Iterations and notes

- Fixed 40 degenerate triangles from a 0.5 m leftover storey band: each tier now uses whole storey groups.
- Inferred: which end the terraces step toward (modelled NW / Mission end). Tier heights estimated; 2010 LiDAR (DataSF 201006.0001788) max 194.9 m vs 197 m published.

## Gate 3 — approval

Pending: renders sent to David (`millennium-tower-contact-sheet.png`).
