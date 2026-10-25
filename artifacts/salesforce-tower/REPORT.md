# Salesforce Tower (v2) — asset report

## Result

**PASS** — `salesforce-tower.glb` meets the landmark contract: the kit validator (`tools/landmark-kit/validate.py`,
Blender 5.2.3 LTS) re-imported only the exported GLB into a fresh scene and printed "all checks pass".
`validation.json` is the machine-readable authority. Not yet integrated (the batch is integrated in one pass).

## Deliverables

- `build_salesforce_tower.py`, `salesforce-tower.glb`, `salesforce-tower.blend`
- `validate_salesforce_tower.py` → `validation.json`; `render_salesforce_tower.py` → 7 renders + `salesforce-tower-contact-sheet.png`
- `REFERENCE.md`; plan at `docs/asset-plans/salesforce-tower.md`

## Contract results

| Check | Value |
|---|---|
| Triangles | 17,508 / 27,000 |
| Dimensions | 79.00 × 79.00 × 326.0 m |
| Min Z | 0.0 |
| XY centre offset | [0.0, 0.0] |
| Crest | 326.0 m (target 326.0) |
| Materials | flat `Toy_*`, roughness 0.85, opaque, no textures |
| Normals, volume, glow facing, degenerates | pass |

Anchor **-122.3969300, 37.7897750**, category `3`.

## Night state

Glow skins over solid geometry: `Toy_red_Glow`, `Toy_sand_Glow`, `Toy_white_Glow`.

## Iterations and notes

- v2 rebuild on the shared kit: `main()` is now `tk.run(...)`; build no longer resets/merges itself.
- Shaft glass changed from `Toy_glassl` to the paler `Toy_glassg` to match the Sacramento & Davis photo.
- Old render/validate scripts replaced by kit wrappers; obsolete `make_contact_sheet.py` removed.
- Category: the live manifest has cat 16 (museum), a v1 slip; v2 proposes 3 (office).
- v1 (2026-08, Blender 4.5) report is superseded by this one; see git history.

## Gate 3 — approval

Pending: renders sent to David (`salesforce-tower-contact-sheet.png`).
