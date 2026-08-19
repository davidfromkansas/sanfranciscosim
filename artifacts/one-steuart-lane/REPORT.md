# One Steuart Lane — build report

`artifacts/one-steuart-lane/one-steuart-lane.glb` — a miniature of SOM's 2021
condominium tower at 1 Steuart Lane / 75 Howard Street, built for the SF-SIM
toy-diorama city. Authored 18 August 2026 from
`docs/asset-plans/one-steuart-lane.md`; the dossier behind every number is
`REFERENCE.md`, which **beats the plan** wherever they differ.

## Shipped numbers

| | |
|---|---|
| File on disk | **411,648 B = 402 KB** (meshopt-compressed; budget 500 KB) |
| Triangles | **17,064** / 24,000 budget |
| Objects | 14 (the loader merges them to one body mesh + one glow set) |
| Draw primitives | 16 |
| Dimensions | 62.95 x 62.493 x **67.06** m |
| Min Z | 0.000 | 
| XY centre offset | 0.0002, −0.0007 m |
| Loader scale factor | **1.000000** (`targetHeightM / measuredHeight`) |
| Materials | 13, all `Toy_*`, 3 of them `_Glow` |
| Image textures / transparency | 0 / 0 |
| Cameras, lights, animation, armatures, constraints | 0 |
| Normals | PASS — 0 inverted signed volumes, ray residual **0.0032%** (gate 0.15%), 0 invalid loop normals |
| Anchor | `-122.3916888, 37.7915643` |
| Headings | Steuart NE **44.2°** · SE **134.8°** · SW **224.5°** · Howard NW **314.9°** |

`validation.json` records the full fresh-scene re-import report and is written
against the **shipped (stage-4 optimized) file**. **Overall: PASS**, 15 of 15
contract checks. The pre-optimize build measured the same 17,064 triangles across
1,027 objects in a 1,344 KB file; see `optimize/REPORT.md`.

The XY bounding box is 62.95 x 62.49 m even though no elevation is longer than
47.0 m: that is the 45°-heading bounding box of a 40.5 x 47.0 m lot (62.10 x
61.65 m) plus the 0.44 m travertine frame projection and the 3.4 m entrance
canopy that oversails the Steuart Lane sidewalk. Not a scale error.

## Files

| File | What |
|---|---|
| `build_one_steuart_lane.py` | deterministic build; `blender -b --python build_one_steuart_lane.py` |
| `one-steuart-lane.blend` | the authored scene |
| `one-steuart-lane.glb` | **the shipping asset** — the stage-4 optimized file |
| `optimize/` | stage-4 shrink pass: scripts, A/B renders, gates, and `input/` holding the pre-optimize original byte-for-byte |
| `render_one_steuart_lane.py` | review rig; `-- --fast` for Workbench/EEVEE, `--night`, `--only top\|aerial\|elev` |
| `validate_one_steuart_lane.py` | fresh-scene contract validation → `validation.json` |
| `make_contact_sheet.py` | composes the contact sheet from the rendered tiles |
| `one-steuart-lane-{top,north,east,south,west,aerial,aerial-night}.png` | review renders |
| `one-steuart-lane-contact-sheet.png` | all seven in one sheet |
| `REFERENCE.md` | the research dossier, sources, and every correction |

Elevation names are a quarter-turn relabelling of the true face normals, because
the building stands at 45° to the compass: `north` = Steuart Lane (NE 44.2°),
`east` = the south-east flank (134.8°), `south` = the south-west flank (224.5°),
`west` = Howard Street (NW 314.9°).

## What it captures

1. **The stack.** Five volumes of three to four storeys on a two-storey base,
   each stepping back on one pair of sides while cantilevering out over the
   volume below on the other pair, so the east corner zig-zags. On the Steuart
   elevation the successive wall planes stand at 23.49, 18.89, 22.69, 17.89 and
   21.69 m from the anchor.
2. **The travertine cage.** A cream lintel at every floor line and a cream
   pilaster at every module boundary, standing 0.44 m in front of dark recessed
   glass, with the bay module deliberately irregular (the real curtain wall
   cycles 4 / 6 / 8 ft panels).
3. **The terraces.** A thin bright cantilevered slab plate with a dark soffit at
   every junction, a pale balustrade and planters where the volume above is set
   back, and one module-wide slot of deep terraces running up each elevation.
4. **The base.** A double-height dark storefront divided by clusters of vertical
   travertine baguettes, the Steuart Lane entrance in a bronze portal under a
   projecting glass canopy, and a planted set-back amenity level above.
5. **The roof.** Cream parapet, a field of dark PV strips in two bays split by a
   pale walkway, two round cooling towers with a row of plant boxes, the
   mechanical penthouse box (the crest at 67.06 m), and a BMU crane on its track.

## Night state

The real building is downlit from beneath its cantilevers, so the hero glow is a
thin cream line under each of the four terrace slabs plus the base cornice —
**five horizontal bands that restate the horizontal massing** — supported by a
warm gold lobby patch on Steuart Lane and a sparse scatter of pale blue lit
units (never a whole floor, never a regular pattern). Nothing else glows.

Glow materials: `Toy_cream_Glow` (f2ede3), `Toy_gold_Glow` (caa64a),
`Toy_glassl_Glow` (6f95b8). All three are thin single plates, never closed
shells — a closed glow shell stacks two alpha layers and tints the surface it
wraps by day.

## Dossier corrections made during the build

Full detail in `REFERENCE.md` §7. In short:

1. **The massing is not a ziggurat.** The first build used monotonically
   shrinking concentric setbacks and read as a wedding cake. The published
   description is "five masses **cantilevered** over ... private terraces" —
   they alternate. Rebuilt with alternating per-edge insets.
2. **Recessed plates are invisible.** The glass was first authored at a negative
   offset, i.e. inside the solid volume shell, and the whole tower rendered blank
   cream. Every surface stands proud of the shell; the recess comes from the
   frame standing in front of the glass.
3. **Roof furniture belongs inside volume E's plan, not the lot's** — E is 27.1 m
   across against the lot's 47 m, and the first roof hung cooling towers in
   mid-air.
4. **The night rig was rendering white.** glTF writes `emissiveFactor = 0` when
   the authored emission strength is 0, so raising `Emission Strength` on a
   re-imported `_Glow` material gives it a default white emission.
   `light_glow()` now copies Base Color into Emission Color at strength 1.0,
   which is what the app does. Fixed before the night render was judged.
5. **`Toy_roofd` is not used.** It renders near-black under the app's lighting;
   the roof deck is `Toy_steel`.
6. **The vision glass was re-valued from navy to mid-blue.** `Toy_glass`
   behind a 35%-coverage frame averages mid-dark at city distance; every
   street-level reference shows sky-reflecting mid-blue. Tower glazing is now
   `Toy_glassl`, the base storefront keeps `Toy_glass`. Noticed at stage-5 QA,
   but justified by the references — the app wide shot that raised it has the
   site in a cast shadow, and measures luma 57 before / 60 after, i.e. nothing.
   See REFERENCE.md §7.6.
7. **The hero night band was widened 0.14 m → 0.38 m** (base cornice 0.36 m).
   At 0.14 m it read in the Blender rig and was sub-pixel at the registry
   camera's 400 m in the app. Judge glow thickness from an app screenshot.

Both were caught by the local QA and fixed by a rebuild + a full re-run of the
stage-4 gates, not patched at integration.

Two plan values were *confirmed*, not corrected: the 67.06 m height (the plan's
reasoning holds — see the open risk below) and the four face headings.

## Open risk carried forward

**The height is disputed and was not independently measured.** SOM, Swinerton,
the developer's release, SF YIMBY and OSM all say 220 ft = 67.06 m, and that is
what shipped. CTBUH and the SF Chronicle say 240 ft. The arithmetic mildly
favours 240 (20 storeys in 220 ft with a 24 ft entry level leaves ~10 ft
floor-to-floor). A rectified facade elevation from Street View panorama
`FgQeEOFiFPKjWDAfs-1pNg` would settle it and was **not attempted**. If 240 ft
turns out to be right, the fix is a one-line change to `H_CREST` and a rebuild —
the tower body is authored at absolute heights, so nothing else moves.

Setback depths are inferred, sized only by a gross-floor-area cross-check
(~29,600 m2 modelled against 335,000 sq ft = 31,120 m2 published, −5%).

## Stage 4 — optimize

1,344 KB → **402 KB raw (−70.1%)**, 1,027 objects → 14, 1,033 draw primitives →
16, triangles and bounding box unchanged, all eight gates PASS, worst A/B pixel
delta 0.0056% against a 2% gate. Full metrics, the waste census, the two
deliberate skips (limited dissolve, interior-face deletion) and the one
documented toolchain substitution are in `optimize/REPORT.md`.

## Renders

Reviewed from the high three-quarter aerial first, iterated three times, then the
formal rig. Rendered with the Workbench/EEVEE fast path rather than Cycles: this
machine was carrying 97 parallel Blender sessions at load 67 while this asset was
built, and a Cycles frame was not going to finish. The flat-colour toy palette
survives the swap; the night pass runs on EEVEE, which is emission-capable.

`one-steuart-lane-contact-sheet.png` carries all seven tiles.

## Manifest draft

Do **not** apply this here — integration is a separate job
(`docs/asset-plans/INTEGRATION-PROMPT.md`).

```json
{
  "id": "one-steuart-lane",
  "file": "one-steuart-lane.glb",
  "anchor": [-122.3916888, 37.7915643],
  "targetHeightM": 67.06,
  "cat": 2,
  "name": "One Steuart Lane",
  "estimated": false,
  "dims": [62.95, 62.493, 67.06],
  "tris": 17064,
  "loadRadius": 2500
}
```

`loadRadius` follows the default rule `max(2500, targetHeightM × 30)` =
`max(2500, 2012)` = 2500. This building was explicitly designed not to have
skyline presence ("It's a tall building, but we weren't trying to have a presence
on the skyline" — SOM's design director), so `alwaysLoaded` would be wrong for it.

Case B integration notes, including the `exclude` sizing, are in
`docs/asset-plans/one-steuart-lane.md` §2.13.

## Approval

**18 August 2026.** Approval was given in advance, for the whole pipeline run, in
the session's opening instruction — quoted verbatim:

> APPROVE EVERYTHING DONT ASK ME FOR PERMISSION

The stage-3 evidence (contact sheet, aerial day and night renders, and the
numbers at the head of this report) was presented at the gate rather than
withheld, and the pipeline advanced on that standing approval rather than on a
fresh one. Recorded here explicitly because gate 3 normally requires a specific
approval of *this asset*, and a blanket pre-authorisation is not the same thing:
if any of the design calls above are wrong, they were not individually reviewed.

---

## Stage 5 — integration (Case B)

Run per `docs/asset-plans/INTEGRATION-PROMPT.md` on 18–19 August 2026, in
**batch mode**: the bake was run and QA'd, then discarded, and the branch ships
source only. The city is baked once for the whole batch by
`docs/asset-pipeline/BATCH-INTEGRATE.md`.

### The exclusion radius, measured

`excluded()` drops a ring when `min(nearestVertex, centroid)` from the landmark
**anchor** is under `r`. Swept over both real bake inputs
(`artifacts/one-steuart-lane/exclusion_sweep.mjs`):

| Gate | Source | Ring | |
|---|---|---|---|
| **0.92 m** | Overture | "One Steuart Lane" — this building's own ring | must drop |
| **11.41 m** | DataSF | `SF3741031` — the demolished 75 Howard garage | must drop |
| 28.14 m | Overture | "201 Spear" | must survive |
| 28.29 m | DataSF | `SF3741032` (72 m) | must survive |

Band `11.41 < r <= 28.14`. **Shipped `exclude: 20`**, the middle of it.

**The first sweep was wrong and would have shipped quietly.**
`streamFeatures()` yields **zero** features from a `.geojsonseq` — Overture is
newline-delimited JSON and `buildings.mjs` reads it with `readline` — so a sweep
that uses the GeoJSON streamer for both inputs returns a DataSF-only answer and
reports it as though both were scanned. The binding neighbour here is Overture's,
0.15 m tighter than DataSF's.

**What is actually being replaced is the 2010 parking garage at ~21.6 m, not a
tower.** Overture carries this building at `height = 25.16`, which is wrong (it
is 67 m), and 25.16 is not greater than the garage's `21.55 x 1.4`, so
`buildings.mjs`'s height-correction branch declines to raise the garage and then
`continue`s past the Overture ring entirely.

### Proof in the baked tile

`artifacts/one-steuart-lane/exclusion_check.mjs` decodes cell `24_11` with the
pipeline's own `readBuildingsBlob`:

| | rings in cell | rings intruding into r=20 | nearest survivor |
|---|---|---|---|
| origin/main | 26 | **1**, reaching 10.06 m past the edge, topY 27.4 m | 9.94 m |
| after re-bake | 25 | **0** | 28.28 m |

### The stray-cell diagnosis

`verify-rebake` first reported cell `23_13` changing 169 → **182** outside my
landmark. An exclusion can only remove footprints, never add 13, so this was not
the radius. `origin/main` had moved: the `soma-thirteen` batch merged after this
branch was cut, and **all thirteen of its landmarks project into cell `23_13`**
— the +13 were the footprints their exclusions removed on main and this
pre-rebase tree still carried. Rebased onto `2c14d5f9f` and re-baked; the stray
cell disappeared.

### Local QA (INTEGRATION-PROMPT Step 5)

Driven by `artifacts/one-steuart-lane/qa_local.mjs` — the built app in real
headless Chrome over CDP, because a hidden Browser pane throttles
`requestAnimationFrame` to nothing and makes a healthy streaming landmark look
broken.

| Check | Result |
|---|---|
| manifest entry loads | PASS — `sf-assets: one-steuart-lane merged 16 objects / 13 materials -> batched (10100 tris body); uniform x1.0000 at 4031, -2384` |
| uniform scale ≈ 1.0 | PASS — **x1.0000** |
| placed at the real anchor | PASS — x 4031, z −2384, matching the projected anchor |
| exactly one building on the site | PASS — no procedural twin, no baked block through the asset (day/wide screenshots) |
| orientation | PASS — the Steuart Lane face looks across to the Embarcadero and the Bay (wide screenshot) |
| terrain seating | PASS — no floating, no sinking |
| night glow | PASS — under-slab bands, lobby patch and scattered units light; nothing else |
| draw calls < 300 | PASS — **96/frame** averaged over 30 frames |
| asset warnings | PASS — none |

Screenshots in `artifacts/one-steuart-lane/qa/` (`day.png`, `night.png`,
`wide.png`) with the raw numbers in `qa.json`.

### Case B gates

| Check | Result |
|---|---|
| `pipeline/audit.mjs` check 1.6 | **PASS** — "114 zones over 110 landmarks clear" |
| `pipeline/verify-rebake.mjs` | **PASS** — "584 of 585 cells unchanged"; only `24_11` moved, 26 → 25; "every asset has clear ground under it" |
| nearest surviving footprint vs radius | 28.3 m vs 20 m |
| `context` tier picked up the landmark | `landmark:oneSteuartLane` at x 4031.2, z −2383.7, height 67.06, camera preset intact |
| search index | `One Steuart Lane` present, 7,905 entries |
| `muni-shapes.bin` | unmodified (the wipe trap avoided) |
| `app && npm run lint` | PASS |
| `app && npm test` | PASS, 26/26 |
| `app && npm run build` | PASS |

Three audit checks fail — 1.2b (citywide 95th-percentile height), 1.3c (Telegraph
Hill terrain 90.5 m against an 85 m gate) and 1.7b (1 sampled tree of 792 more
than 30 m offshore). All three are properties of the source data and the terrain
DEM, none is a building tile this change touches, and `verify-rebake` proves only
cell `24_11` differs from `origin/main`. They are pre-existing, not caused here.

### Fallback drill (INTEGRATION-PROMPT Step 6) — NOT COMPLETED

**This mandatory step did not run to completion and is not claimed as a pass.**

`node artifacts/one-steuart-lane/qa_local.mjs --drill` serves a real 404 for the
landmark GLB and asserts that the app still boots, that exactly one
`sf-assets: … — keeping the code-built landmark` warning appears, and that the
site is empty ground inside the exclusion zone (the expected Case B outcome).

Three attempts, all defeated by machine contention rather than by anything in
the asset:

| Attempt | Outcome |
|---|---|
| 1 | `boot timed out` at the harness's 120 s default |
| 2 | reached the app, then `manifest timed out` after 600 s — `stats().entries` never left 0 |
| 3 | ran ~40 min, then the process was killed during a background-task teardown; empty log, no result written |

The machine carried a load average between 150 and 736 throughout (366 at the
last check), with up to 144 headless Chrome instances belonging to parallel
landmark sessions; the built app runs at a fraction of a frame per second in
software rendering under that. A fourth attempt was not made because conditions
had not improved and the failure mode was already understood.
The boot allowance in `qa_local.mjs` was raised from 120 s to 600 s as part of
attempt 2 and that change is committed.

**What IS verified about the fallback, and what is not.** `app/test/asset-loading.test.mjs`
passes 6/6 and the single-warning fallback path is present in `app/src/assets.js`.
That establishes the code path exists and its rules are locked by tests; it does
**not** establish the runtime behaviour, which is precisely what the drill is
for. Re-run it on a quiet machine before this asset is considered fully signed
off:

```
node artifacts/one-steuart-lane/qa_local.mjs --drill
```

### Shared batch reserve — measured, and a warning for the batch

`main` raised the body reserve to 1,600,000 vertices (49b8d19). Summing the
non-glow POSITION accessors of every manifest GLB
(`artifacts/one-steuart-lane/batch_reserve_check.mjs`):

```
104 landmarks:  body 1,465,064 / 1,600,000  (91.6%)
                glow    77,446 /   250,000  (31.0%)
```

One Steuart Lane contributes 30,300 body + 1,085 glow, ~2% of the total.
**~135,000 vertices of headroom remain, and this corner of the Embarcadero has
about a dozen sibling landmarks in flight at ~30k each — they do not all fit.**
The overflow is silent (each reload drops a different landmark rather than
erroring), so the batch integrator must re-run that check over the merged
manifest and raise `BODY_VERTS` again if it crosses.

---

## Final stage table

| Stage | Gate | Result |
|---|---|---|
| 0 RESOLVE | building confirmed | **PASS** — One Steuart Lane, OSM way 667097308, Case B |
| 1 PLAN | plan committed with sources | **PASS** — `docs/asset-plans/one-steuart-lane.md` |
| 2 BUILD | validation all-PASS | **PASS** — 15/15, normals residual 0 |
| 3 APPROVE | approval quoted | **PASS** — standing approval, recorded above |
| 4 OPTIMIZE | G1–G8 | **PASS** — all eight, re-run in full after the stage-5 rebuild |
| 5 INTEGRATE | local QA + fallback drill | **PARTIAL** — QA 4/4, audit 1.6, verify-rebake all PASS; **fallback drill did not complete** |

Shipped numbers: **17,064 triangles · 411,752 B (402 KB) · loader scale
×1.000000 · 96 draw calls/frame · 62.95 × 62.493 × 67.06 m**, anchor
`-122.3916888, 37.7915643`, `exclude: 20`, `loadRadius: 2500`, `cat: 2`.

Dossier corrections made along the way: six, listed above and in REFERENCE.md §7
— the ziggurat massing, the buried (invisible) facade plates, roof furniture
sized to the lot instead of the top volume, a night rig that rendered every glow
white, navy glazing that read too dark at city distance, and a hero glow band
that was sub-pixel in the app.

Open risks carried forward: the **220 ft vs 240 ft height dispute** (220
shipped, on the architect, the general contractor, the developer's release,
SF YIMBY and OSM; CTBUH and the SF Chronicle say 240) and the **shared landmark
batch reserve at 91.6%** with roughly a dozen Embarcadero siblings still in
flight.

Nothing has been pushed, no PR opened and no deploy run — per
`docs/asset-pipeline/ADDRESS-TO-ASSET.md` stage 5, that decision is the owner's.
