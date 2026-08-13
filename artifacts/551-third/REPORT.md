# 551 Third Street (Shell Service Station) — build report

`551-third.glb` — a miniature of the Shell filling station at 551 3rd Street,
San Francisco. Built 12 August 2026 from `docs/asset-plans/551-third.md`,
stage 2 of `docs/asset-pipeline/ADDRESS-TO-ASSET.md`.

**REPORT beats plan.** Where this file and the plan disagree, this file is right.

## Shipped numbers

| | |
|---|---|
| File | `551-third.glb` (post-stage-4, meshopt) |
| Objects / draw submeshes | 14 (147 before optimize) |
| Triangles | **9,541** / 12,000 cap (10,100 before optimize) |
| File size | 252,408 B raw · 168,664 B gzip |
| Dimensions (world AABB) | 41.81 x 41.81 x 6.60 m |
| min Z | 0.0000 |
| XY centre offset | 0.000, 0.000 |
| Crest | **6.600 m** exactly — loader scale factor 1.0 |
| Materials | 14, all `Toy_*`, all on palette |
| Glow set | `Toy_trim_Glow`, `Toy_mustard_Glow`, `Toy_glassl_Glow` |
| Validation | **PASS**, 19/19 checks (`validation.json`), re-run against the shipped file |

The 41.81 m square AABB is the 39.7 x 20.4 m lot standing on the 45-degree SoMa
grid: a rotated rectangle's world-axis bounding box is necessarily square-ish and
larger than either side. The asset itself is lot-sized.

## Dossier corrections made before modelling

The plan's dossier was re-verified against a 2025-08-29 aerial (Esri World
Imagery / Vantor Vivid Premium, 0.34 m) reprojected into the site frame and
registered against the OSM, parcel and LiDAR geometry. Two readings were wrong:

1. **The canopy is not two rectangular wings.** It is **two octagonal umbrella
   canopies**, each ~11 m across, each with radial ribs converging on a **single
   central column**, touching at a pinched waist. The plan had decomposed the
   16-vertex OSM outline into two axis-aligned rectangles with a 5 m slot between
   them; the outline is actually the union of two octagons. This is the asset's
   entire character, so it was worth catching before modelling rather than after.

2. **The kiosk is at the south-east end of the lot, toward Brannan** — not the
   north-west. The plan's coordinates were right (`u -21.5 .. -14.3`, and
   positive u is north-west); its prose said the opposite.

Both corrections are folded back into `docs/asset-plans/551-third.md`.

A third plan claim was corrected during review rather than research:

3. **The lit canopy soffit is not the night hero.** The plan called it "one big
   hero plane". A canopy soffit is only visible from below its own underside —
   4.30 m here — and the app's camera sits 30-50 degrees above the horizon, so
   it never sees one. The soffit glow shell is still in the model and is correct
   at grazing angles, but the night identity that actually reaches the player is
   the **fascia lightbar ring read from above**, plus the pecten. The night
   render is framed to show that, not a soffit the app will never display.

Two plan risks were *resolved* by the same aerial: the island count (two, one
under each umbrella) and the hydrogen-demolition trap — the imagery post-dates
the demolition's completion by four days, so it shows the current station.

Two remain open and are called out in `REFERENCE.md` §7: the crest's attribution
to a pecten/lightbar crown (the 6.64 m height is measured; what is up there is
inferred), and two-dispensers-per-island (assumed, not observed).

## Orientation decision

Authored in true-world orientation: Blender `+Y` = true north, `+X` = east, so
`placeGeneric()` — which scales and positions but never rotates — drops the lot
onto its real heading. The lot's long axis runs 315.1 / 135.1 deg true and the
3rd Street frontage faces **225.1 deg**, so the contract's "front faces −Y"
cannot be honoured literally. Real-world orientation wins under AGENTS rule 5 and
the orientation note in `docs/asset-plans/README.md`. Recorded here as required.

## Elevation-camera deviation

The required renders are named `north` / `east` / `south` / `west`, but a
true-cardinal orthographic camera on a 45-degree grid sees every face of this
site obliquely and none square on. The four elevations are therefore **aimed
along the site axes** and labelled with the bearing they look from:

| File | Looks from | What it is |
|---|---|---|
| `551-third-south.png` | 225 deg SW | 3rd Street front |
| `551-third-north.png` | 45 deg NE | rear, toward 181 South Park |
| `551-third-west.png` | 315 deg NW | side toward South Park |
| `551-third-east.png` | 135 deg SE | side toward Brannan |

The contact sheet carries the same labels. All four share scale, framing,
lighting, exposure and projection.

## Renders

All frames are rendered from a **fresh re-import of the exported GLB**, never
from the authoring scene. Engine: EEVEE, 32 samples, 1100 x 1100, one sun plus a
flat warm world, no depth of field.

`551-third-top.png` (hero plan) · `551-third-aerial.png` (high three-quarter,
the style bible's judging camera) · the four elevations above ·
`551-third-night.png` · `551-third-contact-sheet.png`.

Night renders follow the note in `docs/asset-plans/README.md`: `Base Color` is
copied into `Emission Color` at strength 1.0, because glTF writes
`emissiveFactor = 0` and a re-imported `_Glow` material would otherwise render
as a white slab.

## Iteration log

1. **First build** — 8,880 tris. Top view showed three faults: the `Toy_ink`
   parapet cap was a solid lid covering the whole kiosk roof rather than a ring;
   the ribs were `Toy_white` on a `Toy_white` deck and did not read; the
   north-west third of the apron was bare.
2. **Fix pass** — parapet cap rebuilt as four slabs so the roof reads; deck
   changed to `Toy_stone` with `Toy_white` ribs; apron gained a painted edge
   line, a chevron at each curb cut, and a bin/vacuum/bollard group in the empty
   north-west third. 10,100 tris.
3. **Camera pass** — elevations re-aimed along the site axes (above); night
   camera re-framed once the soffit-visibility finding landed.
4. **Validator pass** — the first ray test scored only 22 first hits out of 234
   casts, because the fan offsets were scaled to the cast distance and this asset
   is a wide flat plate, so most rays flew past it. Offsets are now scaled to the
   model's own half-extent on a 7 x 7 fan: 1,274 casts, **292 hits, 0
   back-facing**. The weak first result was a measurement artefact, not a normals
   problem — the per-object signed-volume test read clean at both densities.

## Normals

Two independent checks, both clean:

- **Per-object signed volume** — authoritative for a union of closed solids.
  147 / 147 objects positive. Every plate in this model, including the apron,
  the lane markings and the thin `_Glow` shells, is built as a closed box; there
  are no zero-thickness planes.
- **Deterministic visibility ray test** — 26-direction lattice x 7 x 7 fan,
  1,274 rays, 292 first hits, **0 back-facing, residual 0.0000%** against a
  0.15% threshold.

## Draft manifest entry

Do not apply this here — integration is stage 5.

```json
{
  "id": "551-third",
  "file": "551-third.glb",
  "anchor": [
    -122.3946431,
    37.7806625
  ],
  "targetHeightM": 6.6,
  "cat": 21,
  "name": "551 Third Street (Shell Station)",
  "estimated": false,
  "dims": [
    41.81,
    41.81,
    6.6
  ],
  "tris": 9541,
  "loadRadius": 2500
}
```

`cat: 21` is `Gas station` in `CATEGORY_LABELS`; `CAT_TONE` already carries index
21 (`mustard`), so no app change is needed, but nothing in the manifest has
exercised that row before and the card should be looked at once.

## Carried forward to integration

`docs/asset-plans/551-third.md` §2.13 describes an exclusion-zone problem this
site does not share with any other landmark in the set: the bake draws **two**
DataSF footprints on this lot, and no single exclusion circle can remove both
without also deleting 181 South Park. Do not start stage 5 assuming it is
routine.

## Gate 2

`validation.json` — **PASS**, all 19 checks.

## Gate 4 — optimize

Stage 4 ran per `docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md`; full write-up in
`optimize/REPORT.md`. Headline: **613,056 → 252,408 bytes (−58.8%)** and
**147 → 14 draw submeshes**, all eight gates PASS, pixel deltas 0.02% by day and
1.2–1.4% at night (sampling noise in a dark frame). The optimized file is now the
shipping `551-third.glb`; the pre-optimize original is archived at
`optimize/input/551-third.glb`. The stage-2 contract validator was re-run against
the shipped file and still passes 19/19.

## Gate 3 — approval

Approved by David on **13 August 2026**, verbatim:

> approved, continue

Presented at approval: the contact sheet, the aerial and night renders, and the
shipped numbers above. No revision iterations were requested.
