# 326 Brannan Street — build report

Asset: `artifacts/326-brannan/326-brannan.glb`
Plan: [`docs/asset-plans/326-brannan.md`](../../docs/asset-plans/326-brannan.md)
Dossier: [`REFERENCE.md`](./REFERENCE.md)
Built 16–17 August 2026, Blender 5.2.0 LTS, headless.

**Where this report and the plan disagree, this report wins.**

## 1. What shipped

A miniature of the whole property at 326 Brannan Street — the JAX Vineyards SoMa
tasting room — authored as a **site, not a building**: a charcoal bottle-graphic
gate wall on Brannan, an open Wine Court behind it (pale slab, terracotta
planters, a slatted pergola, a fire table inside its bench, loose tables, string
lights, vine masses on both party walls, and a multi-stem olive), and a
one-storey black-CMU shed with a glazed roll-up door filling the rear 9.6 m of
the lot.

| | |
|---|---|
| Anchor (WGS84) | `-122.3928965, 37.7815080` — DataSF parcel centroid, measured |
| Target height | **5.90 m** — shed parapet crest |
| Bounding box | 22.3069 × 22.3614 × **5.9000** m |
| Min Z | 0.000 |
| XY centre offset | (0.1884, −0.1945) m |
| Triangles | **6,148** of a 12,000 budget, in 182 objects |
| Brannan frontage heading | 135.15° true (SE) |
| Registry case | **B** — new landmark, needs a registry entry and a tile re-bake |

The 22.3 × 22.4 m axis-aligned XY box for a 7.98 × 24.32 m lot is correct, not a
scale error: the lot sits at the SoMa grid's 45° and the asset is authored in
true-world orientation because `placeGeneric()` never rotates.

## 2. Corrections to the plan

None of the plan's measurements needed correcting — the anchor, the lot geometry,
the 5.66 m LiDAR deck and the 135.15° heading all re-verified. Three of its
*design* prescriptions were changed during the build, all for reasons visible in
the review renders:

1. **The canopy is a slatted pergola with a partial panel, not a solid plate.**
   The plan specified a 6.6 × 5.0 m closed plate. Built that way it rendered as a
   **black rectangle over a third of the court** in the downward view — the one
   view this asset exists for. It is now two beams, a cross beam, seven slats,
   and a translucent-toned panel over the rear half only, stopping on the cross
   beam so the split reads as a designed edge. The real structure is a panelled
   metal canopy; this is a deliberate miniature simplification and the court plan
   is what it buys.
2. **The court side walls are 2.70 m, not 3.20 m, and the vines crest above
   them.** At 3.20 m in `Toy_plaster` they were the loudest element in every
   elevation — a big blank cream slab competing with the gate. Lowered, warmed
   (`ded4c2` → `c2b8a5`), and the vine masses now top out 0.1–0.3 m above the
   wall, which is both what the real ivy does and the only way green reads from
   outside the court. The 2.70 m ceiling also keeps the walls further from the
   8.11 m and 12.14 m baked neighbour blocks.
3. **The olive is four separated masses, not three overlapping ones, and it is
   smaller.** The plan's 5.0 m-wide crown rendered as a single smooth
   mint-green dome — broccoli — that covered the whole court width. Radii cut,
   colour taken from `93a081` to `7f8d6b`, and the crown split into four clearly
   distinct masses. Crest unchanged at 5.80 m.

## 3. Decisions that could have rescaled the asset

- **The parapet owns the bounding box, not the tree.** `targetHeightM` is the
  5.90 m shed parapet; the olive crown is built to 5.80 m, deliberately 0.10 m
  under it. The plan flagged this as the modeller's call. Letting an
  unmeasurable tree height set the scale of the whole site was rejected: the
  "18 foot olive tree" figure is syndicated marketing copy from around 2015 and
  the tree has had eleven years to grow.
- **Nothing on the shed roof rises above 5.90 m.** The roof has never been
  photographed. The first build put a 0.52 m mechanical unit on it and pushed
  the bbox to 6.18 m — i.e. it rescaled the entire site off an invented feature.
  Every roof object is now capped just under the parapet, which makes the roof
  kit shallower than it would otherwise be. That is the honest trade.
- **The 9.42 m and 38.74 m LiDAR maxima were not used.** Both are 0.5 m cells on
  party walls shared with taller neighbours (334 Brannan is 12.14 m). This is
  the Earl Warren rule in `docs/asset-plans/README.md`. The crest comes from the
  median (5.66 m) and mode (5.50 m) instead.

## 4. Other render-driven fixes

- **The roll-up door read as a hole in the shed for three passes**, and the
  third time the cause was a real bug rather than a colour choice: the panel
  helper offsets along the wall normal, so the dark `Toy_ink` reveal at
  `d ∈ [0.00, 0.18]` fully *enclosed* the panes at `d ∈ [0.02, 0.13]` and drew
  over them, and the glow shells at `d ∈ [0.005, 0.02]` were behind the panes
  rather than in front. The stack is now explicitly back-to-front — recessed
  reveal, then panes, then glow shells — and the steel surround was rebuilt as
  four frame bars instead of a slab over the opening, because a slab at any
  depth either hides the panes or is hidden by them. Panes also lightened
  `2a4d73` → `3d5f85`. This matters because the door is what makes the court a
  *room* rather than a vacant lot.
- **The shed roof kit went through two failed compositions.** Three light boxes
  scattered on a dark field read as modelling noise; grouping them on a dark
  `Toy_charcoal` housekeeping pad made it worse, because on a 6.9 m roof seen
  from directly above *any* dark rectangle reads as a hole rather than as
  equipment. The final version is one grouped kit — all `Toy_steel` — on a
  light `Toy_roofd` curb, with the roof membrane lightened `55565a` → `6a6a66`
  so the parapet ring reads against it.
- **`RoofDuct` had zero height** for one pass: `Z_DECK + 0.08` and
  `Z_CREST − 0.16` are both exactly 5.74, which produced a flat box, eight
  degenerate triangles and a black sliver on the roof. The constant is now
  written against `Z_CREST − 0.06` with the coincidence noted in the source.
- **The pergola panel out-shouted the gate** in bright `Toy_steel`. It moved to
  a new `Toy_canopy` tone (`9a9c96`) sitting close to the court slab, and it now
  sits *under* the slats rather than above them.
- **The string-light beads were authored entirely in `Toy_bulb_Glow`.** That
  makes them primary surfaces in the app's separate unlit `_Glow` layer, which
  renders at low alpha by day — see-through bulbs. Each bead is now an opaque
  `Toy_cream` bulb with a thin glow shell proud of it, which is the pattern the
  contract actually asks for.

## 5. Night state

Four glow groups, in order of importance:

| Group | Material | Form |
|---|---|---|
| String lights (hero) | `Toy_bulb_Glow` | 24 thin shells, each proud of an opaque `Toy_cream` bead on an opaque cord |
| Roll-up door | `Toy_glass_Glow` | 12 thin shells proud of the opaque `Toy_glass` panes |
| Fire table | `Toy_fire_Glow` | one warm disc proud of the opaque `Toy_ink` burner |
| JAX disc | `Toy_coral_Glow` | one thin shell proud of the opaque `Toy_coral` disc |

Nothing else glows. The court walls, the olive, the planters and the pergola stay
dark: a garden at night is lit points in darkness, and lighting the court would
throw away the one thing this asset can do that no other building on the block
face can.

Every glow surface is a thin shell in front of an opaque surface, never a closed
shell wrapped around a whole object.

## 6. Contract compliance

`validation.json` is the machine-readable report from a **fresh-scene re-import
of the exported GLB** (not the authoring scene). **Overall: PASS**, every check
green:

| Check | Result |
|---|---|
| Triangles | 6,148 / 12,000 |
| Dimensions | 22.3069 × 22.3614 × 5.9000 m |
| `crest_normalized_to_target` | 5.9000 vs 5.9 target — loader scale 1.0 |
| `base_at_z_zero` | min Z 0.000 |
| `centered_xy` | (0.1884, −0.1945) m |
| Image textures / transparency | 0 / none |
| Cameras / lights / animation / armatures / constraints | 0 / 0 / 0 / 0 / 0 |
| Transforms applied, no negative scales | yes / yes |
| Normals — per-object signed volume | 182 outward, 0 inverted |
| Normals — deterministic ray test | 2 flipped visible faces of 31,192 first hits = **0.0064 %** (tolerance 0.15 %) |
| Degenerate triangles | 0 |
| Unexpected geometry / material violations | none / none |

The validator was adapted from `380-brannan`'s and initially inherited that
asset's hardcoded anchor, heading and 12.6 m target height, which made two
checks fail spuriously on the first run. Those constants are now 326's, and
`TARGET_HEIGHT` is a named constant rather than a literal repeated twice.

Contract detail:

- Binary GLB, real metres, Z up, +Y north, applied transforms, no negative scales
- Origin at base centre, min Z = 0, bbox top exactly 5.900 m so the loader's
  `targetHeightM / measuredHeight` scale is 1.0
- All materials `Toy_*`, flat, no image textures, no transparency, no `Toy_body`
- `_Glow` suffix only on the four groups in §5
- No cameras, lights, animations, armatures or constraints
- No people, no vehicles, no glassware, no neighbour geometry
- Every panel, plate, slat, cord and bead built as a closed box — no
  zero-thickness planes anywhere, which is what makes the per-object
  signed-volume normals test meaningful on a model that is not a union of
  closed solids in the usual sense

## 7. Renders

| File | What it shows |
|---|---|
| `326-brannan-top.png` | **hero** — the court plan: gate, planters, pergola, olive, fire ring, then the shed roof |
| `326-brannan-aerial.png` | **hero** — the high three-quarter from the SE, looking straight down the court's axis and in through the gate |
| `326-brannan-north/east/south/west.png` | the four elevations, one rig, identical everything but azimuth |
| `326-brannan-night.png` | **hero** — the lit court from the SE |
| `326-brannan-aerial-night.png` | a lower, tighter night frame through the gate |
| `326-brannan-contact-sheet.png` | all of the above |

All renders are of the re-imported exported GLB, so every image depicts exactly
the geometry that ships. Day renders fade `_Glow` materials to the app's daytime
alpha rather than showing them solid.

## 8. Approval

Stage 3 of `docs/asset-pipeline/ADDRESS-TO-ASSET.md`.

> Pending — see §9.

## 9. Known limitations carried forward

- The **gate height (2.80 m) is estimated** from the May 2025 Street View pano
  against parked cars and parking meters. It is the most-seen surface on the
  asset. It does not set the scale.
- The **parapet (0.24 m above the measured deck) is inferred**, typological for
  a 1959 flat-roofed commercial shed.
- The **pergola's real extent** and whether it is fixed or retractable is
  inferred from one oblique, partly screened view.
- The **rear (north-west) elevation has no research at all** — no public vantage,
  nothing published. It is a blind wall by inference from the site plan.
- The small `jax` wordmarks that accompany each bottle silhouette on the real
  fence are **not modelled**: at this scale they would be sub-centimetre
  geometry in a texture-free asset. The bottles and the disc carry the identity.
- **Integration is not routine.** The exclusion window for this landmark is
  1.04 m wide and closes on a vertex physically shared with the 12.14 m building
  next door. Read §2.13 of the plan before running `INTEGRATION-PROMPT.md`.
