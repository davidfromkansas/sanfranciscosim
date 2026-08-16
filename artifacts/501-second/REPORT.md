# 501 Second Street — build report

Miniature GLB of 501 Second Street, San Francisco, for the SF-SIM toy-diorama city.
Built 16 August 2026 by `build_501_second.py` (Blender 5.2.0 LTS, headless), validated by
`validate_501_second.py` into `validation.json`, rendered by `render_501_second.py`.

**REPORT beats plan.** Where this file disagrees with `docs/asset-plans/501-second.md`,
this file is what shipped, and every deviation is listed in §4.

## 1. Shipped numbers

| | |
|---|---|
| Manifest id | `501-second` |
| File | `501-second.glb` |
| File size | **487,516 B** raw, meshopt-compressed (was 1,147,244 B pre-optimize, −57.5%) |
| Triangles | **16,008** (budget 20,000) |
| Objects / draw submeshes | 11 objects, 12 primitives after stage 4 (was 564 / 565); the loader merges these to 2 draw calls |
| Dimensions (axis-aligned) | 83.107 x 82.806 x 37.700 m |
| Building along its own axes | 72.79 m x 42.24 m |
| min Z / XY centre offset | 0.000 m / (0.000, 0.000) |
| Crest | **37.700 m** — penthouse roof; loader scale = 1.000 |
| Main parapet | 33.00 m (measured) |
| Anchor (WGS84) | `-122.3929683, 37.7831785` |
| Second Street heading | **225.4° true (SW)** |
| Bryant Street heading | 315.4° true (NW) |
| Materials | 10, all `Toy_*`: cream, stone, sand, glass, glassl, roofd, steel, ink, gold_Glow, glass_Glow |
| Category | `3` (office) |

The ~83 m axis-aligned bounding box for a 72.79 x 42.24 m building is the expected
consequence of the 45.4° real-world heading, not a scale error.

## 2. Validation — `validation.json`

`overall: PASS`, all sixteen checks. Fresh factory-reset scene, re-importing the exported
GLB; the authoring `.blend` was not inspected. Re-run after the stage-4 shipping swap, so
these are the **packed** file's numbers — `invalid_or_nonunit_loop_normal_count: 0`, ray
flipped fraction 0.0 over 16,233 hits, all 11 shipped shells enclosing positive volume.

## 3. Renders

All regenerated from the final export: four orthographic elevations on one rig, plus
`-top.png`, `-aerial.png`, `-aerial-night.png` and `501-second-contact-sheet.png`.

The aerial azimuth is **due west** — the bisector of the Second Street (225.4°) and Bryant
Street (315.4°) elevations, so the corner and both public fronts are in one frame. Because
the building sits at 45.4°, every axis-aligned elevation shows it obliquely and sees two
faces at once; that is the expected consequence of the real heading.

## 4. Dossier corrections and design decisions

1. **The tripartite composition did not survive the first aerial review.** At the plan's
   `PIER_W 0.90 / PIER_PROJ 0.12 / BELT_PROJ 0.55 / CORNICE_PROJ 0.85` the shaft read as a
   flat grid of horizontal slots and the three horizontal moves — the entire identity —
   were invisible at distance. Shipped values: piers **1.30 m wide, 0.22 m proud**, belt
   cornice **0.80 m** projection, main cornice **1.20 m**. The shadow line a deep cornice
   throws is what makes the composition legible from the app's camera; this is where the
   style bible's semantic exaggeration is spent on this asset.
2. **The base is two storeys of openings, not one tall one.** The plan's §2.7 put a single
   opening per bay from 1.4 to 10.6 m. That merged the two base storeys and destroyed the
   horizontal the belt cornice exists to answer. Shipped: ground 1.20–5.20 m and second
   6.40–10.60 m.
3. **Bay counts raised from 6 / 10 / 10 to 7 / 13 / 13.** At the plan's counts the shaft
   openings were 6 m wide by 2.5 m tall and read as letterbox slots. Shipped openings are
   ~4 m by 2.8 m, which matches the panoramas and gives the piers something to do.
   Triangles went 11,448 → 16,008, still inside the 20,000 cap.
4. **The light court is a dark inset panel, not a modelled well.** The plan asked for a
   14 x 9 m well with its floor at 26 m. The first top-view review showed that the 0.25 m
   deck step alone is invisible from directly overhead, where there is no grazing light to
   throw a shadow — and a true 7 m well needs either a boolean or a much heavier annulus
   body than this budget allows. Shipped: the roof deck is four `Toy_sand` slabs forming a
   frame around the court, and the court is a `Toy_roofd` panel set 0.19 m below them. At
   the app's camera distance that is exactly what a light court looks like, for 12
   triangles. Stated plainly because it is the one place the model is not literal.
5. **A stair bulkhead was added at the Federal end**, and the vent count raised from two to
   five. 3,074 m2 is the largest roof in the bespoke SoMa set and the first review showed
   it reading as a blank tray — the style bible's worst available failure for a building
   the camera looks down on. Nothing added exceeds the penthouse.
6. **The roof membrane is `Toy_sand` from the first build**, not `Toy_steel`. This was
   settled empirically on `524-second` in the same session, where `Toy_steel` shipped and
   the live scene then measured its lit deck at (90, 98, 107) against (146, 133, 104) on
   the baked neighbours — 27% darker, the darkest roof on its block. This roof is three
   times bigger, so the lesson was applied up front rather than re-learned.
7. **The main cornice returns on the party wall**, unlike the belt cornice and frieze which
   run on the three public faces only. It is the top of the building and the aerial camera
   sees all four edges of it; a cornice that stops at a party wall reads as a modelling
   error from above, where the wall itself is invisible.
8. **Footprint: no adjudication needed.** OSM (72.79 x 42.24 m, 3,074 m2) and DataSF LiDAR
   (72.67 x 42.39 m, 3,107 m2) agree to 1%. This is the opposite situation from
   `524-second`, where three sources disagreed by 12% and the choice changed the building.
   Both were checked anyway.

## 5. Height provenance

| Level | Value | Basis |
|---|---|---|
| Main parapet | 33.00 m | DataSF LiDAR modal plane 33.26 m / median 32.72 m over 12,467 cells, **and** OSM `height=33` independently — **measured** |
| Penthouse crest | **37.70 m** | DataSF LiDAR `hgt_max` 37.66 — **measured** |
| Belt cornice 11.60 m, main cornice 30.85 m | photogrammetric | derived by dividing the measured 33.0 m across the permits' 2 + 5 storey split |

`"estimated": false` in the manifest entry: unusually for this batch, both the parapet and
the crest are measurements, not photogrammetry.

**`hgt_max` = 37.66 m is real here, and that is the opposite call from `524-second`.** At
524 the equivalent figure was polygon-edge bleed — a 13.32 m maximum against a 0.95 m
standard deviation on a small roof beside a 19.7 m neighbour. Here the standard deviation
is **6.41 m** over 12,467 cells with a modal plane at 33.26 m, the aerial shows a distinct
raised block on the roof, and the nearest taller neighbour is 60 m away, well outside bleed
range. Reconcile per building, never by habit.

**The Assessor's "8 storeys, built 1985" is not a contradiction.** Every one of 100+
building permits gives 7 existing storeys, and the listings give "built 1925, renovated
1985". The Assessor's year records the renovation and its storey count includes the
penthouse the LiDAR maximum also sees. Seven occupied storeys plus a penthouse is what was
built.

## 6. Approval (stage 3)

Approved by the owner in advance for this batch, quoted verbatim from the session
instruction of 16 August 2026:

> "APPROVE EVERYTHING DONT ASK ME FOR PERMISSION"

No revision round was requested; the six review-driven corrections in §4 (items 1–5, 7)
were made by the modeller before presentation.

## 7. Draft manifest entry

```json
{
  "id": "501-second",
  "file": "501-second.glb",
  "anchor": [
    -122.3929683,
    37.7831785
  ],
  "targetHeightM": 37.7,
  "cat": 3,
  "name": "501 Second Street",
  "estimated": false,
  "dims": [
    83.11,
    82.81,
    37.7
  ],
  "tris": 16008,
  "loadRadius": 2500
}
```

`loadRadius`: the default formula gives `max(2500, 37.7 * 30) = 2500` m. Default taken.

## 8. Stage 4 — optimize

Full detail in `optimize/REPORT.md`. Headline: 1,147,244 B → **487,516 B** raw (−57.5%,
the best result in the SoMa set), 565 → 12 draw submeshes, triangles and bounding box
unchanged, worst A/B pixel delta 0.0076% against 2–4% gates, all gates G1–G8 PASS. Phase
B's limited-dissolve step was deliberately skipped — this asset has three stacked coplanar
ring bands (main cornice, parapet, coping) following the full 230 m perimeter, the
documented sliver trap — and the stage-2 contract validator was re-run against the
**packed** file afterwards, returning `overall: PASS` with zero invalid loop normals.

**487.5 KB is inside the 500 KB on-disk landmark budget by only 12.5 KB.** This is the
first asset in the set where that budget is a live constraint; any future detail increase
must re-check it, and the lever is bay count.

## 9. Integration notes

- **New landmark (Case B).** Needs a `pipeline/lib/landmarks.mjs` entry (`id: '501Second'`)
  and a tile re-bake.
- **Exclusion radius.** Size it from the bake input's ring **vertices**, not centroids, and
  measure it against the real `pipeline/data/overture_buildings.geojsonseq`.
- Judge it against `524-second`, 78 m away and built in the same batch. They are deliberate
  opposites — a 9.9 m red brick shed and a 37.7 m cream office block — and if the pair does
  not read that way from the aerial, the tripartite composition here has collapsed into a
  plain box.
