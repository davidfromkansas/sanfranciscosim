# 318 Brannan Street — build report

Miniature GLB for the SF-SIM toy diorama city, built from
`docs/asset-plans/318-brannan.md` under `docs/asset-pipeline/ADDRESS-TO-ASSET.md`.
Where this report disagrees with the plan, **the report is authoritative** — the
plan was written before the geometry existed.

## Shipping numbers

| | |
|---|---|
| File | `318-brannan.glb` — **shipped = the stage-4 optimized build** |
| File size | 94,884 B raw / 57,242 B gzip −9 (pre-optimize: 195,376 / 33,126) |
| Triangles | **2,972** (cap 8,500) |
| Objects / draw submeshes | 12 / **13** (pre-optimize: 69 / 70) |
| Dimensions (m) | 29.647 x 30.177 x **8.600** |
| Footprint along its own axes | 17.96 m (Brannan, SE) x 23.87 m deep |
| min Z | 0.000 |
| XY centre offset | (0.000, −0.202) m |
| Materials | 11, all `Toy_*`, flat, no textures, no alpha |
| Glow groups | 3 (`Toy_glassl_Glow`, `Toy_glass_Glow`, `Toy_gold_Glow`) |
| Anchor (WGS84) | −122.3927890, 37.7816014 |
| Brannan front heading | 135.8° true (SE) |
| Loader scale | `targetHeightM / measuredHeight` = 8.6 / 8.6 = **1.000** |

`validation.json` — **overall PASS**, all 16 contract checks green, from a
fresh-scene re-import of the shipped GLB (not the authoring scene). It was
re-run against the meshopt-packed file after the stage-4 shipping swap, which
is where 350 Brannan's invisible parapet slivers would have surfaced as
`invalid_or_nonunit_loop_normal_count`; they do not, because the limited
dissolve stays disabled for this asset too.

The 30.18 m Y dimension against 29.65 m X is expected: a 17.96 x 23.87 m
rectangle at a 45.8° heading gives a ~29.6 m axis-aligned box, and the awnings
project up to 1.2 m off the SE face. The −0.202 m Y centre offset has the same
cause and is well inside the ±1 m gate.

## Dossier corrections made during the build

Every one of these was re-derived from the references listed in `REFERENCE.md`,
not inherited from the plan.

1. **The awnings are `Toy_ink`, not `Toy_navy`.** Plan §2.8 chose `Toy_navy`
   (`2c4a70`) over `Toy_ink` on the strength of the listing photograph, arguing
   two black bands would go dead at miniature scale. The **first aerial render
   killed it**: `Toy_navy` and `Toy_glass` (`2a4d73`) are two hex points apart,
   so the awnings and the glazing they band merged into one navy mass and the
   three-stripe composition — the building's entire identity — disappeared. That
   is precisely the failure the plan's own §2.6 warned about, arriving from the
   direction the plan did not expect. `Toy_ink` also reads truer against the May
   2025 Street View, where both awnings are effectively black. Reversed, and the
   reasoning is in the build script beside the palette.
2. **The awnings stop at the broad pier; they do not run across the number bay.**
   Plan §2.7 steps 5 and 9 said "full width". Every photograph shows both awnings
   ending at the pier, with the number bay carrying its own separate dark panel.
   Corrected.
3. **The storefront pier and the ribbon pier are at different `u`** (7.85 m and
   9.40 m along the frontage), as photographed, rather than stacked. The plan
   implied a single vertical division.
4. **The awnings are shed canopies, not slabs.** The first build extruded them as
   plain boxes and let the 0.12 m mass bevel round them off; from the aerial they
   read as pipes bolted to the facade. They are now a proper profile — vertical
   valance at the outer edge, flat underside, top raking back *up* to the wall —
   with a 0.06/1 bevel. The rake also gives the app's downward camera a dark
   sloped plane instead of a flat stripe.
5. **The upper awning projects 0.85 m, not 1.10 m.** At 1.10 m it occluded almost
   the whole ribbon window from a 38°-down camera, which would have hidden the
   night hero. 0.85 m keeps roughly half the ribbon visible from directly above
   and all of it from the lower camera angles the app actually spends its time
   at, without stopping the awning from reading as an awning.
6. **The southwest flank's ground-floor windows sit under two of the upper bays,
   not between them.** The first build scattered them and the flank read as
   sprinkled portholes rather than a designed elevation. Bays also widened from
   2.0 m to 2.4 m.

## Iteration log

| Pass | What changed | Why |
|---|---|---|
| 1 | First build: 71 objects, 4,084 tris. Aerial preview at 40 samples. | Pipeline requires judging the high three-quarter aerial before the formal rig |
| 2 | Awnings `Toy_navy` → `Toy_ink`; awnings reprofiled as shed canopies; awning/roof-furniture bevel 0.12/2 → 0.06/1; SW flank windows widened and re-aligned. 69 objects, 2,972 tris. | Corrections 1, 4, 6 above. The tri count *fell* because the awnings became four-sided profiles instead of bevelled boxes |
| 3 | Upper awning projection 1.10 → 0.85 m; SW windows 2.0 → 2.4 m. | Corrections 5, 6 |
| 4 | Formal rig: four elevations, top, aerial, night, contact sheet. Validator retargeted from the 350-brannan constants (crest 13.85 → 8.6, tri budget 10,000 → 8,500, anchor). | Gate 2 |

## What the asset is

A low, wide, pale painted-concrete box on the measured DataSF footprint, at its
real 45.8° heading, with:

- **two full-width dark awning bands** — the identity — and the second-floor
  ribbon window trapped between them, over a four-bay glazed storefront on a
  pale bulkhead;
- a **northeast end bay** past a broad pier, carrying the dark number panel and a
  recessed glass entrance door;
- **four designed elevations**, because the site has no party wall: blank service
  flank northeast, five punched window bays southwest, a working rear with a
  roll-up freight door northwest;
- a **designed roof** — mid-grey membrane, white coping ring, one 2.6 m square
  skylight northeast of centre, a white duct ladder (two trunks, four branches,
  one spur) across the southwest two-thirds, a dark mechanical cluster on the
  southwest side, three vent cans, and a deliberately empty northeast third.

It is the first mid-century building in this Brannan family and the only
non-contributor to the South End Historic District among them. Judged beside
350 and 358 Brannan in the aerial, it reads as a different decade — which was
the brief.

## Night state

Hero: the **second-floor ribbon**, lit end to end in `Toy_glassl_Glow` — a
bright band between two dark awnings. Supporting: two of the four storefront
bays (`Toy_glass_Glow`), two of the five southwest flank bays, and a small warm
strip over the entrance (`Toy_gold_Glow`). The awnings, the northeast flank and
the rear do not glow. All glow surfaces are thin shells proud of the opaque
glazing behind them, per the app's separate ~12%-alpha day layer.

`318-brannan-aerial-night.png` clips the glow colours to white under the
Standard view transform at the preview strength — it judges *which* surfaces
glow and how restrained the scatter is, not the night palette. The app draws
`_Glow` as an unlit overlay at each material's own baked colour.

## Stage 4 — optimize

Full metrics, census, judgment calls and gate results in
[`optimize/REPORT.md`](optimize/REPORT.md). Summary: raw 195,376 → 94,884 B
(−51.4%), draw submeshes 70 → 13 (−81.4%), triangles and bbox unchanged, all of
G1–G6 and G8 PASS. The limited-dissolve step stays disabled — this asset's
parapet and coping ring bands are exactly the coplanar-annulus case that
manufactures invisible slivers. Meshopt raises the gzip figure (33.1 → 57.2 KB),
which is the repo's standing trade for one consistent encoding, not a
regression.

## Deliverables

```
artifacts/318-brannan/
  318-brannan.glb                    the SHIPPED asset (stage-4 optimized)
  optimize/                          stage-4 pass: scripts, stats, A/B renders,
                                     REPORT.md, and input/ (byte-exact archive
                                     of the pre-optimize GLB)
  318-brannan.blend
  build_318_brannan.py               deterministic rebuild
  render_318_brannan.py              controlled review rig
  validate_318_brannan.py            fresh-scene contract validator
  make_contact_sheet.py
  validation.json                    overall PASS, 16/16 checks
  REFERENCE.md                       sources, measurements, uncertainties
  REPORT.md                          this file
  318-brannan-{north,east,south,west}.png    four elevations, one rig
  318-brannan-top.png
  318-brannan-aerial.png
  318-brannan-aerial-night.png
  318-brannan-contact-sheet.png
```

The four elevation renders each show the building at 45° and the "north"/"south"
frames each see a flank and a front together. That is the consequence of the real
heading, not a camera error.

## Draft manifest entry

```json
{
  "id": "318-brannan",
  "file": "318-brannan.glb",
  "anchor": [
    -122.3927890,
    37.7816014
  ],
  "targetHeightM": 8.6,
  "cat": 3,
  "name": "318 Brannan Street",
  "estimated": true,
  "dims": [
    29.6469,
    30.1767,
    8.6
  ],
  "tris": 2972,
  "loadRadius": 2500
}
```

`"estimated": true` because the 8.6 m parapet cap is derived from the LiDAR
modal roof plane (7.78 m) plus an inferred 0.7 m parapet, not published.
`dims` and `tris` are the **shipped** numbers — the optimize pass changed
neither (it cut draw submeshes 70 → 13 and file bytes 51%, not geometry).

## Integration note carried forward

`pipeline/lib/landmarks.mjs` entry `id: '318Brannan'`, **`exclude: 8`**, measured
against the real bake input (DataSF *and* Overture) from this anchor:

```
own DataSF ring SF3775100      centroid  0.01 m
own Overture twin (451 m2)     centroid  4.68 m   <- lower bound
326 Brannan, Overture rings    vertex   10.93 m   <- binding constraint
326 Brannan, DataSF SF3775012  vertex   11.07 m

exclude 5-10 m  -> drops 2 rings (correct: this building, traced twice)
exclude 11 m    -> drops 4 (eats 326 Brannan, which has no GLB to replace it)
```

This building is traced by both DataSF and Overture with centroids 4.68 m apart,
so a radius under 5 m leaves the Overture copy standing inside the GLB. Do not
raise past 10 m.

## Approval

**Gate 3 — 17 August 2026.** Advance authorisation given by the owner at the top
of the session, quoted verbatim:

> APPROVE EVERYTHING DONT ASK ME FOR PERMISSION

The contact sheet, the day aerial and the night aerial were delivered to the
owner before the pipeline advanced, so the review material exists and is on the
record; the standing instruction above is what carried the asset past this gate
rather than a per-asset "approved". Any objection on review reopens stage 2 and
the iteration log continues above.
</content>
