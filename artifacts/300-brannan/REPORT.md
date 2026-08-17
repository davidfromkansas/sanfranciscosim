# 300 Brannan Street — build report

**Status:** built, approved, optimized and re-validated. The shipping file is the
stage-4 output; the pre-optimize original is archived at `optimize/input/`.

| | |
|---|---|
| Asset | `artifacts/300-brannan/300-brannan.glb` |
| Triangles | **12,964** (cap 15,000) |
| Objects / nodes | 11 shipped (362 as authored, joined per material in stage 4) |
| Dimensions | 47.531 × 49.287 × **25.200** m |
| min Z | 0.000 m — sits on the ground plane |
| XY centre offset | (−0.123, +0.001) m |
| Loader scale | `targetHeightM / measuredHeight` = 25.2 / 25.2 = **1.000** |
| File | **332.0 KB** shipped (808.8 KB pre-optimize, −59.0%) |
| Draw submeshes | **12** (363 pre-optimize) |
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

These are the **shipped** numbers, re-measured from the stage-4 output: the optimize
pass changed no triangles and no bounding box, only vertex count, node count and
encoding. See `optimize/REPORT.md`.

## Approval

Stage 3 presented on 17 August 2026 (contact sheet, aerial day and night, numbers).
Approved under the session's standing instruction, quoted verbatim:

> "APPROVE EVERYTHING DONT ASK ME FOR PERMISSION"

That is a blanket pre-approval given at the start of the run, not a judgement on
these particular renders. Recorded as such so a later reader knows no one looked at
the images before stage 4 began.

---

## Stage 5 — integration (batch mode), 17 August 2026

**Case B**, new landmark. Integrated per `docs/asset-plans/INTEGRATION-PROMPT.md`
Part 1, with Step 7 replaced by the pipeline's stop-and-ask.

### Local QA

| Item | Result | Evidence |
|---|---|---|
| Re-validation of the shipping GLB | **PASS** | fresh-scene re-import, all 15 contract checks `true` after the stage-4 swap |
| Manifest entry | **PASS** | appended as text, `+19 lines, 0 other lines touched` — `JSON.stringify` would have rewritten `11.0`→`11` across six other landmarks |
| id mapping | **PASS** | `camelId('300-brannan')` = `300Brannan`, which is the `pipeline/lib/landmarks.mjs` id |
| Case B registry entry | **PASS** | `pipeline/lib/landmarks.mjs`, `exclude: 12`, camera `{260, yaw 85, pitch 26}` |
| Exclusion radius, measured | **PASS** | safe band **2–21 m**; 12 m drops exactly the target's two rings (DataSF `SF3775008` + its Overture twin); 22 m would eat `SF3775181` on its nearest vertex at 21.42 m |
| Re-bake | **PASS** | full chain `terrain → bridges → buildings → streets → landcover → validate → lore → toy → notables → context → muni-shapes` |
| `pipeline/audit.mjs` check 1.6 | **PASS** | "no procedural footprint inside a bespoke landmark exclusion zone — 83 zones over 80 landmarks clear" |
| `pipeline/verify-rebake.mjs` | **PASS** | "584 of 585 cells unchanged; 23_13 201 → 200 ← 300Brannan"; nearest surviving footprint 21.4 m against the 12 m radius |
| Single building on site | **PASS** | one footprint dropped, no procedural twin, no baked block poking through — settled from the tile, not from a frame |
| Merge line + scale | **PASS** | `sf-assets: 300-brannan merged 12 objects / 10 materials -> batched (7715 tris body); uniform x1.0000 at 3955, -1308` — **scale exactly 1.0000**, position exactly the projected anchor |
| Orientation | **PASS** | the canted corner faces the Second/Brannan intersection; both frontages face their own streets |
| Terrain seating | **PASS** | no float, no sink (see `qa-local-day.jpg`) |
| Night glow | **PASS** | only the intended `_Glow` surfaces light: the cant stripe over its lit ground-floor band, plus the scattered frontage bays (see `qa-local-night.jpg`) |
| Draw calls (budget < 300) | **PASS** | **110** at the landmark, **123** at night, **106** at street level downtown — measured by hooking `renderer.render` and taking the per-frame max, because the stats overlay reads the post-pass quad and always says 1 |
| `npm run lint` / `npm test` / `npm run build` | **PASS** | eslint clean, 26/26 tests, build OK |
| Fallback drill | **PASS** | GLB moved aside → app boots, area renders, exactly one warning `sf-assets: 300-brannan failed to load (…)`, `failed: 1`, and the site is empty ground inside the exclusion zone, which is the expected Case B behaviour (see `qa-local-fallback.jpg`). Vite answers a missing `public/` path with the SPA `index.html` and HTTP 200, so the symptom is a parse failure rather than a 404 — a dev-server artifact, not an asset problem |

QA was run in headless Chrome over CDP against the Vite dev server, because
`preview_start` had all five dev-server slots held by parallel landmark sessions.

### Camera preset

`camera.yaw` is `180 − true bearing`. The view this building wants is straight down
the cant's outward normal, 95.1° true — which is also the bisector of the two
frontage normals — so the preset is **yaw 85**, not 95. Verified from a rendered
frame (`qa-local-day.jpg`), not from the arithmetic: yaw 95 is the mirror image and
would stare at the north-west party wall.

### Batch mode

Other landmarks are in flight in sibling worktrees, so per `ADDRESS-TO-ASSET.md`
"Batch mode" the bake was **run for the QA above and then discarded**
(`git checkout -- app/public/tiles api/_data`). This branch commits **source only**:
the GLB, its manifest entry, its `landmarks.mjs` entry, the asset plan and
`artifacts/300-brannan/`. Sanity check passes —
`git diff --name-only origin/main` lists nothing under `app/public/tiles/` or
`api/_data/`. The city is re-baked once for the whole batch by
`docs/asset-pipeline/BATCH-INTEGRATE.md`.

### Not done, deliberately

Push, PR, deploy and production QA are the user's call and have not been run.
