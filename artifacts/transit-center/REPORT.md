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

Approved by David on 2026-10-25 (contact sheets sent in four batches of five): "approve all".

## Stage 4 — optimize

Shipped as `app/public/sf-assets/landmarks/transit-center.glb`, meshopt-compressed with the intake flags of `pipeline/compress-assets.mjs` (`gltfpack -c -km -kn -noq`): **346 KB → 154 KB** (56% smaller). Geometry is unchanged. The kit merges every landmark into one body mesh and one glow mesh, so the Phase B cleanup in `tools/glb-optimize/` finds nothing to join or weld; a trial run saved 0 triangles and grew the file 1–5%, so it was not applied. The limited dissolve is skipped as GLB-OPTIMIZE-PROMPT §3 step 3 requires for assets with ring bands and parapets. Gate G3 (three.js GLTFLoader round-trip with MeshoptDecoder, `tools/glb-optimize/g3check`) passes.
