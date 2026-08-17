# 84 South Park — build report

Miniature GLB for the SF-SIM toy diorama city, built from
`docs/asset-plans/84-south-park.md` (stage 2 of `docs/asset-pipeline/ADDRESS-TO-ASSET.md`).

**Status: validation all-PASS on the shipped, stage-4-optimized asset.**

| | |
|---|---|
| Asset | `artifacts/84-south-park/84-south-park.glb` |
| Build | `build_84_south_park.py` (deterministic, Blender 5.2.0 LTS, headless) |
| Objects / triangles | **11** / **6,900** (cap 7,000) — 65 objects before stage 4 joined them per material |
| Dimensions | **26.086 × 26.292 × 13.200 m** — the XY box is the exact 45° rotation of a 6.99 × 30.07 m sliver, not a 26 m building |
| Min Z / XY centre | 0.000 m / (0.000, 0.000) |
| Bounding-box top | **13.200 m** — the pergola beams; loader scale = 1.0 |
| Footprint | 6.99 × 30.07 m = 210.2 m² |
| Street elevation faces | **135.18°** true; long axis 315.18° |
| Manifest anchor | **-122.3940683, 37.7819794** (design anchor -122.3940683, 37.7819798; recentring shift −0.003 m E, −0.013 m N) |
| Materials | 12, all `Toy_*`, flat, no textures, no alpha, no `Toy_body` |
| Glow | `Toy_glassl_Glow` (2 windows), `Toy_trim_Glow` (entrance spill) |
| File | **185,352 bytes raw / 126,473 gzip** (shipped, meshopt-packed). Pre-optimize: 383,108 / 62,116, archived at `optimize/input/` |
| Draw submeshes | **12** (67 before stage 4) |

## Validation (fresh-scene re-import of the exported GLB)

`validate_84_south_park.py` → `validation.json`, **overall PASS**. Re-run against
the **shipped, stage-4-packed** file after the optimize swap — that re-run is what
catches dissolve slivers, which are invisible until gltfpack re-emits stored
normals. Every one of the 16 gates passes:

meters and plausible dimensions · crest normalized to target · base at z=0 ·
centred XY · under triangle budget · no image textures · no transparency ·
materials follow contract · no cameras or lights · no animation/skin/constraints ·
transforms applied · no negative scales · normals outward (signed volume) ·
normals outward (ray residual) · no degenerate geometry · no unexpected objects.

Normals: per-object signed volume positive for **all 11** objects (authoritative
for a union of interpenetrating solids); the secondary 31,500-ray visibility test
returns a flipped fraction of **0.000159** against a 0.0015 tolerance;
`invalid_or_nonunit_loop_normal_count` **0**. Degenerate triangles: 0. Image
textures: 0. Cameras/lights: 0.

## Dossier corrections

The plan's Part 1 requires re-verifying the dossier before modelling and says
REPORT beats plan. Four things changed.

**1. The body colour went off-palette, exactly as the plan's §2.8 anticipated.**
The plan specified `Toy_verdigris` (`#9fb8a8`) as the palette's nearest hue while
recording that the real facade is around `#6d8188` and that an off-palette move was
allowed if the first aerial render read chalky. **It did.** Built in
`Toy_verdigris`, the model read as pale sage against the warm tabletop and would
have been near-indistinguishable from the cream and taupe neighbours in the baked
city — which destroys the *only* recognition cue this building has at the app's
viewing distance. The shipped body is **`Toy_slate` `#6d8188`**, off-palette and
deliberate. `sf-asset-check` scores an off-palette colour as a WARN, not a FAIL,
and the style bible's SF exception explicitly covers painted residential facades.
`validation.json` reports it under `off_palette_materials` rather than gating it.

**2. The plan's roof design was wrong about the rear, and the aerial corrected it.**
Plan §2.7 step 4 called for a **4.6 × 4.6 m light well cut into the roof plane**
dropping to a floor at 8.10 m. Re-reading the Bing z20 imagery rotated onto the
building's long axis shows something simpler and better: the rear **7.17 m of the
building is a two-storey wing**, capped at 8.10 m with a pale planted terrace and
a glazed bay at the very back — a clean two-level step, not a hole. That reading
also explains the DataSF numbers better: the LiDAR main footprint's 8.18 m
minimum, its 27.31 m OBB length (2.8 m short of the 30.07 m lot, because the wing's
terrace is not roof), and the separate 16 m² footprint at a 7.99 m median. Built as
the wing.

**3. The entrance slot had to be authored proud, not deep — twice.** There is no
boolean subtraction in this build, so a "recess" is a dark inset field with
everything that should read inside it standing *proud* of that field. The first
build put the door and rails at negative `d` (deeper than the slot solid) and
buried both: the bay rendered as a flat dark stripe. The second put the slot's own
outer face just *behind* the wall and hid the dark field instead, leaving two
rails and a door apparently floating on slate. The shipped version puts the slot
face 0.03 m proud, the door 0.17 m, the rails 0.20 m. Recorded because it is the
same trap for any recessed bay authored this way.

**4. Night emission needed retuning down, not up.** The 106 South Park rig used
emission strength 3.2 for four lit windows on a 7.3 m front. This building has
**two** lit openings and they are the largest on it; at 3.2 both blew to flat
white and swallowed the entrance spill. Shipped at **2.1**.

## The pergola — the decision this asset turns on

The bounding-box top, and therefore `targetHeightM`, is the roof pergola at
**13.20 m**. The alternative reading puts it at the **11.50 m** parapet — a 15%
scale difference across the whole asset. The evidence is set out in full in
`REFERENCE.md` §7.1. Summarised:

- **For:** January 2025 Street View from the south-west shows an open slatted
  frame standing against the sky above this building's parapet; the Bing aerial
  shows a regularly slatted dark rectangle at the corresponding position on the
  roof (≈2.5 × 3.5 m, +5.1 to +7.6 m from the anchor toward the street); the
  DataSF LiDAR maximum of 13.24 m sits 1.88 m above the 11.36 m median, which a
  ~2 m trellis explains exactly; and the permit record has a 1994 "garden area to
  south deck" and a 2009 roof-deck membrane replacement.
- **Against:** 76–82 South Park shares the north-east party wall and has a LiDAR
  median of **13.08 m**, so party-wall bleed would produce the same maximum — the
  failure mode the Earl Warren and Gran Oriente plans both document. At 0.118 m/px
  a flush PV array and a slatted pergola are not cleanly separable.
- **What tipped it:** 86–96 South Park on the *other* side has its own LiDAR
  maximum of 13.28 m against an 11.15 m median, with no taller neighbour to bleed
  from. A ~13.2 m rooftop structure is normal on this row, so 84's maximum does
  not need a bleed explanation — and the Street View frame is direct evidence.

**Decided: real, and modelled open** — four posts, two side rails, five cross
beams, with the deck visible between them from directly above. If it is ever
disproved, the fix is: delete the pergola, set the bounding-box top and
`targetHeightM` to 11.50, and re-render. Nothing else in the model changes.

## Iteration log

| # | Change | Why |
|---|---|---|
| 1 | first build: `Toy_verdigris` body, 4.6 m roof light well, plan-spec slot | plan §2.7 as written |
| 2 | 7,224 → 6,900 tris (terrace planters 3→2, roof planters 3→2, pergola beams 6→5) | over the 7,000 cap |
| 3 | body → `Toy_slate` `#6d8188`; slot re-authored proud; projecting box 0.35 → 0.45 m proud with a larger window; tree canopy lifted so the trunk reads; ground-floor window widened | first aerial review: pale-sage body, buried door and rails, box not reading as projecting |
| 4 | slot outer face pushed from −0.02 to +0.03 m; door and rails pushed further proud | second facade review: the dark field was itself hidden behind the wall |
| 5 | night emission 3.2 → 2.1 | both lit windows blown to flat white |

Every render in this folder was regenerated from the final export after change 5,
and the contact sheet is composed from those files.

## Renders

`-facade.png` (square-on at 135.18°, the frame the facade is judged from) ·
`-south.png` (street) · `-north.png` (rear) · `-west.png` / `-east.png` (the two
blind party flanks, for completeness) · `-top.png` · `-roof.png` (tight top-down,
3× the contact-sheet tile — both flanks are blind so the roof is the entire
silhouette) · `-aerial.png` (high three-quarter, the app's camera) ·
`-aerial-night.png` · `-contact-sheet.png`.

The two end elevations carry a lot of empty frame. That is deliberate: the four
elevations share one orthographic scale so opposite faces can be compared.

## Draft manifest entry

Not applied here — stage 5 owns the manifest.

```json
{
  "id": "84-south-park",
  "file": "84-south-park.glb",
  "anchor": [
    -122.3940683,
    37.7819794
  ],
  "targetHeightM": 13.2,
  "cat": 1,
  "name": "84 South Park",
  "estimated": true,
  "dims": [
    26.0856,
    26.2918,
    13.2
  ],
  "tris": 6900,
  "loadRadius": 2500
}
```

`"estimated": true` — no height for this building is published anywhere. 13.20 m
is the DataSF LiDAR maximum read as the pergola crest and 11.50 m is the LiDAR
majority read as the parapet; both are derived, neither is a source.

`dims` and `tris` are the **shipped** post-stage-4 values. Stage 4 joined 65
objects into 11 and 67 draw submeshes into 12 without touching a triangle, so
`tris` is unchanged and `dims` is identical to 5 decimal places. Full metrics and
gate results: `optimize/REPORT.md`.

## Approval

**16 August 2026 — standing session authorisation, quoted verbatim:**

> APPROVE EVERYTHING DONT ASK ME FOR PERMISSION

Recorded honestly for the audit trail: this is a **blanket up-front
authorisation given at the start of the session**, before any render existed. It
is not a review of these specific images. The stage-3 evidence (contact sheet,
aerial day and night, and the numbers above) was presented to the user at this
point and the pipeline advanced under that authorisation rather than pausing.
A later "change X" from the user re-opens stage 2 in the normal way.
