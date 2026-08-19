# 132 The Embarcadero — build report

**Deliverable:** `artifacts/132-embarcadero/132-embarcadero.glb` — a validated
miniature of the Jewish Community Federation Building, 132 The Embarcadero /
121 Steuart Street, San Francisco (block 3715, lot 003).

| | |
|---|---|
| Triangles | **4,960** (cap 14,000) |
| Objects | 16 (shipped, post-optimize; 179 as authored) |
| Dimensions (AABB) | 40.437 x 40.473 x **29.570** m |
| Min Z | 0.000 |
| XY centre offset | 0.000, 0.000 |
| File | **159,340 bytes** raw (shipped, meshopt); 362,428 bytes as authored |
| Materials | 16, all `Toy_*`, 4 with `_Glow` |
| Anchor | −122.3925476, 37.7931482 |
| Target height | 29.57 m (bulkhead crest); parapet 27.40 m; roof deck 26.82 m |
| Draw submeshes | 17 (from 180) |
| Validation | **PASS** — all 16 checks on the SHIPPED file, `validation.json` |

## 1. What was built

A seven-storey red-brick slab, 13.75 m of street frontage running 42.95 m
through the block, at 44.95° off the world axes. Two public elevations and two
party walls:

- **Northeast, The Embarcadero (44.95°)** — a three-bay storefront base, a brick
  spandrel course carrying three wall lights, a full-width second-floor glazed
  ribbon at 4.37–6.11 m, and five floors of six-bay punched windows.
- **Southwest, Steuart Street (224.95°)** — a recessed dark entrance with a gold
  lettering strip under a projecting brick lintel, two service doors, a **blind
  second floor**, and the same five floors of six-bay windows above.
- **Both party walls** — plain brick, with the crown band carried across them.
- **Roof** — a pale deck at 26.82 m inside a 0.58 m parapet upstand with a dark
  coping at 27.40 m; a slate lift/stair bulkhead to 29.57 m over the Steuart
  third; three plant blocks, two vents and an antenna platform with three masts.

Every facade dimension came from the photogrammetric solve recorded in
`REFERENCE.md` §4. Nothing was eyeballed off a photograph.

## 2. Corrections and deviations from the plan

**REPORT beats plan.** Four departures, each with its reason:

1. **Roof deck is `Toy_sand`, not the plan's `Toy_roofd`.** `Toy_roofd` measures
   rgb(9,9,12) on a horizontal deck in the live app and reads as a black hole
   from the downward camera — a lesson already paid for on 358-brannan and
   524-second, and visible in this asset's first review render, where the 590 m2
   deck went solid black. `Toy_sand` is 524-second's shipped and
   live-scene-verified value. The roof plant moved from `Toy_steel` to
   `Toy_slate` in the same pass so it still reads against the pale deck.
2. **Crown band is `Toy_stone` at 1.50 m, not `Toy_trim` at 2.50 m.** The plan
   called for a 2.50 m near-white band. The first review render turned the
   building into a red box wearing a white collar — the band read as a separate
   object rather than a crown. It was also the least certain dimension in the
   dossier (asset plan §2.15 risk 4: the colour scan across the top of the
   facade was taken in shadow and returned a mixed brick/pale zone from 24.3 to
   26.9 m). Both changes move toward the conservative reading.
3. **The kerbside bollard row is not modelled.** It stands 1.6 m clear of the
   Steuart wall. Including it would extend the axis-aligned bounding box on one
   side only and move the base-centre origin about 0.34 m off the surveyed
   anchor — the loader positions by that origin, so the whole building would sit
   0.34 m out of place. AGENTS rule 5 (data accuracy) beats the detail. The
   bollards remain in `REFERENCE.md` §5 as an observed feature.
4. **The crown band runs as a continuous ring**, rather than the plan's two
   frontages with 1 m returns. The northwest party wall is exposed above ~18 m
   and reads from the aerial camera, so a wrapped crown is both more plausible
   there and cheaper than four mitred stubs.

## 3. The one inferred number

`targetHeightM` = **29.57 m** is the DataSF LiDAR maximum, read as a lift/stair
bulkhead. The roof was never observed — no orthophoto reachable for this work
resolves a 27 m roof here (Google's z22 tiles lean too far to attribute the roof
to the footprint; Esri's z20 is worse). The reading rests on three things: the
2.75 m offset above the measured deck, which is exactly a lift overrun; the DBI
permits recording traction-lift machine rooms and hoistways; and the fact that
neither party-wall neighbour can account for the return (Steuart Place peaks at
27.77 m, 110–116 at 24.43 m, and that 24.43 is itself edge bleed from this
building's own wall).

**If it is wrong, the damage is contained.** The parapet at 27.40 m was measured
independently — 40 sky-boundary samples across the frontage, sigma 0.08 m — and
it carries the entire silhouette. A wrong bulkhead adds a phantom box on a roof
that nothing else looks at; it cannot mis-scale the building. The correction, if
an aerial ever settles it, is to drop `targetHeightM` to 27.40 and put the plant
below the parapet.

## 4. Build iterations

| Pass | Change | Why |
|---|---|---|
| 1 | first geometry, 180 objects, 4,960 tris | — |
| 2 | roof deck `Toy_roofd` → `Toy_sand`; plant `Toy_steel` → `Toy_slate`; crown `Toy_trim` 2.50 m → `Toy_stone` 1.50 m; window openings 1.50 → 1.62 m wide | the aerial review in §2.1–2.2; the wider opening gives the grid a horizontal read at the 1.58 m measured head height |
| 3 | the crown's underside chamfer rebuilt as a closed ring solid (`ring_profile`) instead of an open sloped skirt | the validator's signed-volume gate flagged `crown_chamfer` as inverted. An **open surface has no signed volume**, so it can never pass — the fix is to close it, not to flip it. 180 objects → 179, triangle count unchanged |

## 5. Validation

`validation.json`, produced by re-importing the exported GLB into a fresh
isolated Blender scene — the re-import is what was measured, not the source
scene.

```
overall PASS
  meters_and_plausible_dimensions                      PASS
  crest_normalized_to_target                           PASS  (29.570, target 29.57)
  base_at_z_zero                                       PASS  (min Z 0.000)
  centered_xy                                          PASS  (offset 0.000, 0.000)
  under_triangle_budget                                PASS  (4,960 / 14,000)
  no_image_textures                                    PASS  (0 images)
  no_transparency                                      PASS
  materials_follow_contract                            PASS  (0 violations)
  no_cameras_or_lights                                 PASS  (0 / 0)
  no_animation_skin_or_constraints                     PASS
  transforms_applied                                   PASS
  no_negative_scales                                   PASS
  normals_outward_signed_volume                        PASS  (0 inverted objects)
  normals_outward_ray_residual_within_tolerance        PASS
  no_degenerate_geometry                               PASS
  no_unexpected_objects                                PASS
```

The 40.4 x 40.5 m axis-aligned bounding box is the expected consequence of a
44.95° real-world heading on a 13.75 x 42.95 m building, not a scale error.

Materials: `Toy_brick`, `Toy_glass`, `Toy_glass_Glow`, `Toy_glassl`,
`Toy_glassl_Glow`, `Toy_gold`, `Toy_gold_Glow`, `Toy_ink`, `Toy_navy`,
`Toy_roofd`, `Toy_sand`, `Toy_slate`, `Toy_steel`, `Toy_stone`, `Toy_trim`,
`Toy_trim_Glow`.

## 6. Night state

Hero: the Embarcadero storefront and second-floor glazed ribbon, lit as one
continuous horizontal at the waterfront. Supports: the Steuart gold lettering
strip, ten of the sixty upper windows scattered rather than banded, and three
small wall lights on the spandrel course. The crown band does not glow.

All glow shells are thin panels whose back faces sit inside the opaque fill
behind them, so only one alpha layer is visible by day — a closed glow box reads
about 23% by day and would tint the brick.

## 7. Renders

`132-embarcadero-north.png`, `-east.png`, `-south.png`, `-west.png` (one
orthographic rig, identical scale/framing/lighting/exposure, azimuth only
varying), `-top.png` (north up), `-aerial.png` (70 mm, 38° down, 15° azimuth —
the Embarcadero front plus the 43 m depth that defines the building),
`-aerial-night.png`, and `-contact-sheet.png`. Every image depicts the exported
GLB, re-imported.

Because the building sits at 44.95°, each compass elevation shows two faces at
45°: NORTH and EAST show the Embarcadero front with a party wall, SOUTH and WEST
the Steuart front with a party wall. That is correct and expected.

## 8. Approval

Quoted verbatim from the session brief, 18 August 2026:

> APPROVE EVERYTHING DONT ASK ME FOR PERMISSION

Recorded as a standing pre-approval covering the pipeline's stage-3 gate. It was
not a response to these renders — no reviewer has seen them — so §2 and §3 above
are written to be the record a reviewer would need.

## 9. Optimize pass (stage 4)

The shipping file is the optimized one. Full record in
`optimize/REPORT.md`; the pre-optimize original is archived byte-for-byte at
`optimize/input/132-embarcadero.glb`.

| | Authored | Shipped |
|---|---|---|
| File, raw | 362,428 B | **159,340 B** (−56.0%) |
| Triangles | 4,960 | 4,960 |
| Objects | 179 | 16 |
| Draw submeshes | 180 | 17 |
| Materials | 16 | 16 |
| Bounding box | 40.43706 x 40.47308 x 29.57 | identical |

All eight optimize gates pass. Worst A/B pixel delta across day and night, near
and far, is 0.09% against a 2% gate. The limited-dissolve step was skipped on
purpose: this asset has three stacked coplanar ring bands (crown, parapet,
coping) and dissolving annuli manufactures the 20 m slivers that fail the
contract validator after the swap.

The numbers in the table at the top of this report are the SHIPPED numbers.
`validation.json` was re-run against the optimized file and passes all 16 checks.

## 10. Reproducing

```
blender -b --python build_132_embarcadero.py
blender -b --python render_132_embarcadero.py -- --glb $PWD/132-embarcadero.glb --out $PWD --prefix 132-embarcadero
blender -b --python render_132_embarcadero.py -- --glb $PWD/132-embarcadero.glb --out $PWD --prefix 132-embarcadero --night
blender -b --python validate_132_embarcadero.py -- --glb $PWD/132-embarcadero.glb --out $PWD/validation.json
python3 make_contact_sheet.py
```

Then stage 4, from `optimize/`:

```
blender -b --python inspect.py  -- $PWD/input/132-embarcadero.glb $PWD/inspect.json
blender -b --python optimize.py -- $PWD/input/132-embarcadero.glb $PWD/mid.glb $PWD/phaseb_stats.json
npx gltfpack@0.24 -i mid.glb -o 132-embarcadero.optimized.glb -c -km -kn -noq
blender -b --python validate.py -- $PWD/input/132-embarcadero.glb $PWD/132-embarcadero.optimized.glb $PWD/validation.json
(cd g3check && npm install && node check.mjs ../132-embarcadero.optimized.glb)
blender -b --python render_ab.py -- $PWD/input/132-embarcadero.glb $PWD/renders/in
blender -b --python render_ab.py -- $PWD/132-embarcadero.optimized.glb $PWD/renders/out
python3 diff_ab.py
```

The render and validate scripts take absolute paths; Blender's working directory
is not the script's directory.
