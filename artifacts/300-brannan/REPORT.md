# 300 Brannan Street — build report

**Status:** built, validated, all contract checks PASS. Pre-optimize.

| | |
|---|---|
| Asset | `artifacts/300-brannan/300-brannan.glb` |
| Triangles | **12,964** (cap 15,000) |
| Objects | 362 |
| Dimensions | 47.531 × 49.287 × **25.200** m |
| min Z | 0.000 m — sits on the ground plane |
| XY centre offset | (−0.123, +0.001) m |
| Loader scale | `targetHeightM / measuredHeight` = 25.2 / 25.2 = **1.000** |
| File | 808.8 KB raw, 123.6 KB gzip (pre-optimize) |
| Materials | 10, all `Toy_*`, flat, no textures, no alpha, no `Toy_body` |
| Glow materials | `Toy_glassl_Glow`, `Toy_trim_Glow` |
| Normals | every object positive signed volume; ray-cast residual **0.000%** |

## Contract checks (fresh-scene re-import of the exported GLB)

All fifteen checks in `validation.json` are `true`; `overall: PASS`.

meters_and_plausible_dimensions · base_at_z_zero · crest_is_target_height ·
centered_xy · under_triangle_budget · no_image_textures · no_transparency ·
materials_follow_contract · no_cameras_or_lights · no_animation_skin_or_constraints ·
transforms_applied · no_negative_scales · normals_outward · no_degenerate_geometry ·
no_unexpected_objects

## Measured headings (recorded per the task prompt)

| Elevation | Length | Outward normal, true |
|---|---|---|
| Second Street (NE front) | 28.18 m | 45.2° |
| The canted corner (E) | 5.05 m | 95.1° |
| Brannan Street (SE front) | 27.73 m | 135.5° |
| south-corner setback | 5.14 + 1.14 m | 135.6° / 224.1° |
| Stanford Street flank (SW) | 30.03 m | 225.5° |
| north-west lot-line wall | 36.60 m | 315.1° |

The axis-aligned XY bounding box is 47.53 × 49.29 m although no elevation exceeds
36.60 m. That is the expected consequence of the 45° SoMa heading plus the 0.74 m
cornice projection, not a scale error.

## Heights

| | |
|---|---|
| Ground storey | 0 → 5.00 m |
| Base cornice | 4.80 → 5.58 m, projecting 0.74 m |
| Upper floors | five of 3.052 m, 5.58 → 20.84 m |
| Roof deck | 20.84 m — DataSF LiDAR `hgt_median_m`, **measured** |
| Parapet coping top | 21.34 m — the surveyed **70 ft**, Page & Turnbull, **measured** |
| Secondary bulkhead | 23.40 m |
| Penthouse crest | **25.20 m** — the bounding-box top and the manifest target |

## Corrections made to the plan's dossier during the build

**REPORT beats plan.** Two things changed, and one bug was found and fixed:

1. **The cant is built at its flush 5.05 m chord, not the DataSF ring's raw 8.09 m
   edge.** The plan already derived both; this build confirms the 5.05 m reading is
   the one that matches the nadir parapet and Street View (one window bay wide), and
   that building the 8.09 m edge would have pushed the corner ~2 m into Second Street.
2. **The ground-storey base is `Toy_roofd` (#45454a), not `Toy_ink` (#3a3530).** The
   real base is near-black charcoal, but the first review renders confirmed the
   plan's own value-budget warning: a full storey of `Toy_ink` under five storeys of
   dark recessed bays reads as a hole rather than a mass. `Toy_ink` is kept for the
   base cornice, the entrance canopy and the fire escape, so the cornice still reads
   as a distinct dark shelf against the base. Fidelity is preserved (base darker than
   the upper wall); only the value is lifted.
3. **`arch_plate()` had a de-duplication bug** that dropped both springing points of
   the segmental arch, so the Second Street openings rendered as tapered
   "tombstones" instead of an arcade. Fixed by removing the dedupe (the springing
   points are not duplicates of the base corners) and the arch rise was reduced from
   0.58 m to 0.42 m so the heads read as properly *flattened* arches, which is the
   district's documented detail.

Two other build decisions worth recording:

- **The south-corner setback carries the facade.** The 5.14 m panel that steps back
  1.19 m from the Brannan wall plane was initially left blank and read as a dead slab
  in the aerial; it now gets one bay of the same treatment without pilasters.
- **`Toy_stone` (#d9d2c2) is used for the pilaster and wall field**, although the real
  building's post-2008 paint is a cooler, more neutral gray. This is a deliberate
  palette-cohesion choice: the SF palette has no light cool gray, the six Brannan
  Street neighbours already in the manifest all use `Toy_stone`/`Toy_sand`, and the
  style bible's set cohesion outranks paint-chip fidelity. Recorded here so a future
  pass can revisit it rather than rediscover it.

## Night state

Hero glow is the **canted corner**: its single bay lit on all five upper floors over
a lit ground-floor band that returns round the cant, so the building reads at night
as one vertical stripe of light on the corner of a dark block. Supporting accents are
six scattered lit bays on Second Street and six on Brannan, differently placed per
floor, plus one lit storefront bay on each frontage. Nothing is lit on the Stanford
flank or the party wall. All glow surfaces are thin plates standing 0.13–0.16 m proud
of the opaque glazing, never primary surfaces.

## Renders

Regenerated from the final export with Cycles (Metal GPU, 40 samples, denoised):
`-top`, `-aerial`, `-north` (Second Street), `-east` (square on the cant), `-south`
(Brannan), `-west` (Stanford), `-party` (the lot-line wall), `-night`, and
`-contact-sheet`. The four-plus-one elevations share one orthographic rig and differ
only in azimuth.

## Draft manifest entry

```json
{
  "id": "300-brannan",
  "file": "300-brannan.glb",
  "anchor": [
    -122.3925543,
    37.7818313
  ],
  "targetHeightM": 25.2,
  "cat": 3,
  "name": "300 Brannan Street",
  "estimated": false,
  "dims": [
    47.531,
    49.2868,
    25.2
  ],
  "tris": 12964,
  "loadRadius": 2500
}
```

`dims` and `tris` are the pre-optimize numbers and must be refreshed from the
stage-4 output before the manifest entry ships.

## Approval

_(stage 3)_
