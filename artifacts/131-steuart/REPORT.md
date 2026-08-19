# 131 Steuart Street (Steuart Place) — build report

**Asset:** `artifacts/131-steuart/131-steuart.glb` — a validated miniature of the
1907 red-brick block at 131 Steuart Street, San Francisco, with its 1983
cast-stone Embarcadero elevation and its barrel-roofed penthouse crest.

Plan of record: `docs/asset-plans/131-steuart.md`. Research dossier:
`REFERENCE.md` (which beats the plan wherever they disagree).

## Numbers

| | |
|---|---|
| Triangles | **6,842** (cap 12,000) |
| Objects | **13** after the stage-4 join (196 as authored) |
| Dimensions (axis-aligned) | 41.221 × 41.346 × **27.700** m |
| Real dimensions | 14.16 × 42.07 m footprint, 27.7 m to the barrel crown |
| Min Z / max Z | 0.000 / 27.700 |
| Loader scale (`targetHeightM / measuredHeight`) | **1.000000** |
| XY centre offset | (0.0017, 0.0008) m |
| Materials | 11, all `Toy_*` |
| Glow materials | `Toy_glassl_Glow`, `Toy_gold_Glow` |
| File | **191,416 B** raw, meshopt (pre-optimize 448,708 B; see `optimize/REPORT.md`) |
| Normals — ray-cast residual | 0.000127 (gate 0.0015) |
| Normals — inverted signed-volume objects | 0 |
| Anchor | `-122.3924386, 37.7930568` |
| Heading | Steuart front 224.9° true; Embarcadero front 44.8° |

The axis-aligned bounding box is ~41.2 × 41.3 m even though the building is
14.16 × 42.07 m: the footprint sits at 44.8° to the world axes and the model is
authored at its real heading, so this is expected, not a scale error.

## Validation

`validate_131_steuart.py` re-imports the exported GLB into a fresh isolated
scene and validates the re-import. `validation.json` — **overall PASS**, every
check green:

| Check | Result |
|---|---|
| meters_and_plausible_dimensions | PASS |
| base_at_z_zero | PASS |
| crest_is_target_height (27.7 ± 0.01) | PASS |
| centered_xy | PASS |
| under_triangle_budget (6,842 ≤ 12,000) | PASS |
| no_image_textures | PASS |
| no_transparency | PASS |
| materials_follow_contract | PASS |
| no_cameras_or_lights | PASS |
| no_animation_skin_or_constraints | PASS |
| transforms_applied | PASS |
| no_negative_scales | PASS |
| normals_outward | PASS |
| no_degenerate_geometry | PASS |
| no_unexpected_objects | PASS |

## Renders

`131-steuart-contact-sheet.png` collects all seven:

- `131-steuart-top.png` — roof plan: cornice ring, monitor spine, plant, skylight, barrel penthouse at the NE end
- `131-steuart-aerial.png` — high three-quarter from the bay (NE), 40° down, 62 mm
- `131-steuart-night.png` — the same camera, night state
- `131-steuart-south.png` — Steuart Street elevation (SW, 224.9°)
- `131-steuart-north.png` — The Embarcadero elevation (NE, 44.8°)
- `131-steuart-east.png` — SE party wall with 141 Steuart (135.0°)
- `131-steuart-west.png` — NW party wall with 121 Steuart (314.6°)

Rendered from the **exported GLB**, re-imported into an empty scene, so every
image depicts exactly what ships. The review rig ran in its `--fast` mode
(Workbench day / EEVEE night) because this machine was carrying a load average
above 100 from parallel sessions; the flat-colour toy palette survives the swap
intact.

## Corrections made during the build

1. **Anchor moved 7.6 cm**, from the plan's polygon centroid
   (`-122.3924393, 37.7930564`) to the footprint AABB centre
   (`-122.3924386, 37.7930568`), so the exported XY offset is exactly zero.
   **The manifest and registry must use the AABB centre.**
2. **`Toy_slate` → `Toy_sash`.** The plan specified `Toy_slate` `6f7883` for the
   cornice, string course and shopfront joinery. That is a blue-grey and it read
   wrong against the brick; the real metalwork is a near-black green. Shipped
   with `Toy_sash` `2f4f49` (precedent `artifacts/21-south-park`).
3. **Party walls simplified.** The plan's flank treatment (three horizontal floor
   lines plus three vertical strips per flank) rendered as blurry smudges and one
   vertical strip straddled the cast-stone band. The verticals were dropped and
   the horizontals confined to the brick run.
4. **Roof rebalanced.** The monitor spine's first cap was `Toy_ink` and read as a
   black bar down the middle of the roof — the same failure mode as
   `Toy_roofd`. It ships as `Toy_cream` over a `Toy_steel` body, with the plant
   in cream and the skylight in `Toy_glass`.

## Traps hit, for the next asset

1. **A 2013-era Street View panorama stitches to 3584 × 1664, not 4096 × 2048.**
   Measure the non-black extent of the stitched equirect before using it; the
   modern geometry made every height read ~10 % low.
2. **Re-imported `_Glow` materials carry a default WHITE emission**, because
   glTF writes `emissiveFactor = 0` when the authored strength is 0. The first
   night render was a slab of pure white. The render script now copies Base
   Color into Emission Color at strength 1.0 before rendering — which is also
   exactly what the app does, since its night layer is unlit at the baked colour.
   (Already documented in `docs/asset-plans/README.md`; hit anyway.)
3. **Workbench's MATERIAL colour mode reads `material.diffuse_color`**, which the
   glTF importer leaves at the 0.8 grey default. The `--fast` review renders
   showed a maroon building until the render script started syncing
   `diffuse_color` from the BSDF after import.

## Stage 4 — optimize

Run and reported in `optimize/REPORT.md`. All gates G1–G6 and G8 PASS (G7 n/a,
bake mode off): 196 objects → 13, 199 draw primitives → 16, 13,712 verts →
13,444, raw bytes 448,708 → **191,416** (−57.3 %), worst A/B pixel delta
0.1995 % against 2 %/4 % gates. Triangles unchanged at 6,842. The optimized file
is now the shipping GLB; the pre-optimize original is archived at
`optimize/input/131-steuart.glb`. The limited-dissolve step was deliberately
skipped — this asset has four full-footprint coplanar ring bands and that step
is the only one that can manufacture degenerate geometry.

Post-swap re-validation: **overall PASS**, all 15 checks, numbers above.

## Approval

> "APPROVE EVERYTHING DONT ASK ME FOR PERMISSION"
> — David, 18 August 2026 (given up front, covering every gate in this run)

Stage 3 gate satisfied by that standing approval; no revision round was
requested. Recorded here verbatim as the pipeline requires.
