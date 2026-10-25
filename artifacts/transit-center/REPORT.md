# Salesforce Transit Center — build report

## Result
A 436 m long scalloped terminal with a white wavy skin and Salesforce Park on the roof.
Validation: **PASS** (all checks).

## Deliverables
- `transit-center.glb`, `transit-center.blend`, `build_transit_center.py`
- `validate_transit_center.py` → `validation.json`
- `render_transit_center.py` → 7 renders + `transit-center-contact-sheet.png`

## Contract (from validation.json)
| Check | Value |
|---|---|
| Triangles | 6,780 / 27,000 |
| Dimensions | 342.5 x 340.3 x 30.0 m (bbox; the building runs diagonally) |
| Min z | 0.0 |
| XY centre offset | 0, 0 |
| Crest | 30.0 m (target 30) |
| Materials | flat `Toy_*`, roughness 0.85, no textures, opaque |
| Normals / volume / glow facing | pass |

## Geometry and materials
See `docs/asset-plans/transit-center.md` 2.7–2.8.

## Night state
Glazed street level and cafe glow warm (`sand_Glow`); the skin shows scattered cool light and
the light-column oculus glows white (`white_Glow`).

## Iterations
1. First draft included a bus-ramp tube; it dipped below z = 0 and was removed.
2. The park deck rendered black: its top sat exactly on the glass body's top (coplanar faces).
   The body now stops 0.6 m under the deck with no top face; deck soil changed to `leaf` and
   lawns to `mint` so the lawns read lighter than the planting.

## Gate 3 — approval
Pending: renders sent to David.
