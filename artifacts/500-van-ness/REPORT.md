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

## Stage 5 — integration (batch mode)

Run of `docs/asset-plans/INTEGRATION-PROMPT.md` Part 1 with the batch-mode
amendment from `ADDRESS-TO-ASSET.md`: the branch ships **source only**, and the
city is baked once for the whole batch by `BATCH-INTEGRATE.md`.

| Check | Result | Evidence |
|---|---|---|
| Re-validation of the shipped GLB | **PASS** | `validation.json` all-PASS, 9,512 tris, 43.286 × 45.097 × 17.000 m, min z 0, 11 `Toy_*` materials |
| GLB dropped in | **PASS** | `app/public/sf-assets/landmarks/500-van-ness.glb`, 247,576 bytes, byte-identical to the artifacts copy; already meshopt-compressed, so `compress-assets.mjs` skips it |
| Manifest entry | **PASS** | appended; served correctly (`fetch` from the running app returns the entry) |
| id round trip | **PASS** | `camelId('500-van-ness')` → `500VanNess`, matching the registry entry |
| Registry entry (Case B) | **PASS** | `pipeline/lib/landmarks.mjs`, `exclude: 28`, camera preset `{320, 232, 24}` |
| Exclusion re-measured after the batch re-bake | **PASS** | re-run against `origin/main` **after** PR #117's re-bake: still no footprint covering the anchor, nearest surviving vertex **32.8 m** vs `exclude: 28` — 4.8 m margin, and the entry removes nothing |
| Single building on the site | **PASS** | one building in the frame, no procedural twin, no baked block poking through |
| Scale factor | **PASS** | console: `uniform x1.0000`; placement matrix diagonal is exactly 1 |
| Position | **PASS** | placed at 1547, −1151 = the projected anchor |
| Orientation | **PASS** | placement matrix has no rotation; the long show face runs along McAllister and the two-pavilion front along Van Ness, as built |
| Terrain seating | **PASS** | placement y = 22.06 m = `sampleElevation` at the anchor; no float, no sink |
| Night glow | **PASS** | at `night 1.00` only the sign fascia (cyan line along the plinth) and the scattered warm apartment windows light; walls, roof and parapet stay dark |
| Draw calls | **PASS (architectural)** | the merge line reports `batched` — the asset joins the shared `landmark-bodies` / `landmark-glow` pair (28 instances each), so it adds **zero** draw calls. A live fps / draw-call reading was **not obtainable**: the QA ran in a background browser pane where rAF is throttled, so the stats overlay reads `fps 0 / draw calls 1` between forced frames. Flagged rather than hidden. |
| Fallback drill | **PASS** | with the GLB renamed away: app boots, area renders, **exactly one** warning — `sf-assets: 500-van-ness failed to load (Unexpected token '<', "<!doctype "... is not valid JSON)` — and the site is empty ground, which is the expected Case B outcome here. (Vite answers a missing GLB with `200 text/html`, so the failure surfaces as a parse error, not a 404.) File restored byte-identical afterwards. |
| lint / build | **PASS** | `npm run lint` clean; `npm run build` succeeded |
| Batch-mode sanity | **PASS** | `git diff --name-only origin/main` lists nothing under `app/public/tiles/` or `api/_data/` from this branch |

**Not done, deliberately:** no bake was run on this branch, and no push / PR /
deploy. Per batch mode the bake and the single PR belong to
`docs/asset-pipeline/BATCH-INTEGRATE.md`. The one thing the batch bake still owes
this landmark is its identity data — pick box, `search-index` row and
`context/landmarks.json` entry — which come from the `lore → toy → context`
chain. The building itself is already visible without it, because the site was
cleared long ago by the Courthouse exclusion.

**Note for the batch:** `origin/main` moved during this session (PR #117 re-baked
the city for five Civic Center / SoMa landmarks, taking the registry from 47 to
57 entries). This branch is still based on 82252e5d. `landmarks.mjs` and
`landmarks_manifest.json` are both append-only lists, so the merge is mechanical,
but it has not been performed here.

## Stage 3 — approval

Pre-approved by the user before the build, verbatim:

> "I approve everything -- go ahead and do your thing. you dont need to ask for
> stage 3 approval. proceed w everything"

— David, 2026-08-13. The contact sheet, day and night aerials and the numbers
above are presented in the session response rather than gated on a reply.
