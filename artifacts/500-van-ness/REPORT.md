# 500 Van Ness Avenue (The Corinthian) — build report

Stage 2 of `docs/asset-pipeline/ADDRESS-TO-ASSET.md`, run from
`docs/asset-plans/500-van-ness.md` Part 1.

Toolchain: Blender 5.2.0 LTS (headless), Cycles (Metal GPU via the review
script's opt-in `--gpu` flag; same integrator and sample count as the CPU
default), python3 + Pillow.

```
B=/Applications/Blender.app/Contents/MacOS/Blender
$B -b --python build_500_van_ness.py
$B -b --python render_500_van_ness.py -- --gpu
$B -b --python render_500_van_ness.py -- --night --gpu
$B -b --python validate_500_van_ness.py
python3 make_contact_sheet.py
```

## What shipped

| | value |
|---|---|
| Triangles | **9,512** shipped (9,522 pre-optimize; budget 14,000, landmark cap 27,000) |
| Mesh objects | 12 shipped (190 pre-optimize) |
| File size | **247,576 bytes** raw (budget 500 KB) |
| Materials | 11, all `Toy_*`, 2 of them `_Glow` |
| Bbox | **43.286 × 45.097 × 17.000 m** |
| min z | 0.000 |
| XY centre offset | (−0.0007, −0.0002) m |
| Anchor | lon −122.4199220, lat 37.7804082 |
| Target height | 17.0 m (`estimated: true`) |
| Entrance heading | 261.6° true (W) |

## Dossier corrections made while building

**REPORT beats plan.** Three numbers in `docs/asset-plans/500-van-ness.md` were
wrong or unverified when the plan was written; all three have been corrected in
the plan as well.

1. **`dims` in the draft manifest entry.** The plan predicted the footprint
   extent (40.0 × 41.8 m) as the asset bbox. The shipped bbox is
   **43.29 × 45.10 m**, because the cornice overhangs 1.45 m on every side. The
   overhang is symmetric, so the origin is unaffected; the manifest now carries
   the measured numbers.
2. **`exclude: 16` was wrong, and for an instructive reason.** The plan sized
   the exclusion radius off *OSM* neighbour geometry and landed on a 10.3–17.7 m
   window. Measured against the **committed bake**
   (`app/public/tiles/buildings/19_13.bin` + neighbours) the picture is
   different: no baked footprint covers the anchor at all, and the nearest
   surviving footprint vertex is **32.8 m** away. The shipped proposal is
   **`exclude: 28`** — enough to cover our own 25.4 m footprint on its own
   merits, 4.8 m clear of the nearest neighbour.
3. **The site is already empty.** `civicCenterCourthouse` (anchor 59.5 m away,
   `exclude: 52`) already reaches to within 7.5 m of our anchor and swallowed
   this building's procedural footprint at the last bake. So the usual Case B
   hazard — a procedural block standing inside the new GLB — does not exist
   here, and is provable from the committed tiles rather than from a re-bake.
   The registry entry is still needed for the pick box, search-index row and
   `context/landmarks.json` identity, which come from the `lore → toy → context`
   chain that the batch runs once.

## Design iterations (three review passes on the aerial)

| Pass | What was wrong | What changed |
|---|---|---|
| 1 | The eight oriels, authored at the real ~0.9 m projection, disappeared at the app's camera; 19 thin parapet finials read as noise; twelve lone vent pipes sprayed across the deck; the light well was oversized | bays to 1.30 m projection with a 1.45 m cornice to cap them; 12 chunky piers + urns + three raised pediment panels; one mechanical cluster + one skylight pair; well cut to 7.0 × 5.6 m |
| 2 | Bright hairline creases ran straight across the roof deck | the bevel helper was rounding the **interior** edges of the n-gon roof cap left by the light-well boolean. `bevel()` now filters to edges whose two faces meet at more than 18°. Side effect: 10,562 → 9,246 triangles |
| 3 | The day-state `_Glow` shells read as grey blocks among the blue windows | shells narrowed and inset (they are still visibly a different tone by day — that is what the app does, `_Glow` draws at `0.12 + 0.95·uNight` opacity, and this render honours it) |

## Deliberate deviations from the contract

- **"Front faces −Y" is not honoured.** The asset is authored in true-world
  orientation because `placeGeneric()` never rotates (AGENTS rule 5 and the
  standing note in `docs/asset-plans/README.md`). The building's real entrance
  faces 261.6° true.
- **The plinth, shopfront band and sign fascia wrap the whole ring**, including
  the two party walls, which in reality carry neither shopfront nor signage.
  This is the `ring_band` idiom used by every landmark in this repo; the east
  face is hidden by the Courthouse GLB and the north face reads as one
  continuous base band rather than a stripe that stops in mid-air. Recorded
  because it is an invention, small as it is.
- **The east and north elevations are blank painted stucco.** They are party
  walls, no photograph of them exists from public space, and inventing windows
  there would be inventing evidence.

## Known risks carried into integration

1. The 1.45 m cornice overhang crosses the east party-wall line and does
   interpenetrate the `civic-center-courthouse` GLB by about that much — the two
   buildings genuinely abut (the courthouse's nearest surveyed vertex is 17.7 m
   from our anchor, i.e. on our east wall). It should not be visible: the
   courthouse is 29.6 m tall against our 17.0 m, so our cornice and parapet at
   z 15.5–16.6 are buried inside its mass rather than crossing its silhouette.
   Confirm at the corner, where the two footprints do not align exactly; if it
   reads, the fix is in authoring (a flush cornice return on the party-wall
   edges), not in placement.
2. The 17.0 m crest is deck (LiDAR-measured 15.48 m) plus a photo-read parapet.
   `estimated: true`.
3. The second interior light well is designed from one aerial image, not
   surveyed. Only the roof reads it.

## Stage 4 — optimize

Run and reported in `optimize/REPORT.md`. All gates PASS: raw 574,548 →
**247,576 bytes** (−56.9 %), 190 → **12** objects / 13 draw primitives, vertices
−72.4 %, triangles 9,522 → 9,512, bbox and origin identical, max A/B pixel delta
0.1223 % against a 2 % gate. The optimized file is now
`artifacts/500-van-ness/500-van-ness.glb` and `validation.json` above was re-run
against it.

## Stage 3 — approval

Pre-approved by the user before the build, verbatim:

> "I approve everything -- go ahead and do your thing. you dont need to ask for
> stage 3 approval. proceed w everything"

— David, 2026-08-13. The contact sheet, day and night aerials and the numbers
above are presented in the session response rather than gated on a reply.
