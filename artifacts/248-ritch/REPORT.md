# 248–250 Ritch Street — build report

Stage 2 of `docs/asset-pipeline/ADDRESS-TO-ASSET.md`, executed 18 August 2026
against `docs/asset-plans/248-ritch.md`.

**What was built:** a validated miniature GLB of the 1915 two-flat at 248–250
Ritch Street, San Francisco — 3,572 triangles, 7.60 × 13.90 m in plan on the
45.05° SoMa grid, bounding-box top exactly 8.60 m, seven `Toy_*` materials, one
of them `_Glow`. `validation.json` is **PASS** on all seventeen contract checks.

| | |
|---|---|
| Triangles | **3,572** (cap 7,000) |
| Objects | 8 as shipped (129 before the stage-4 join) |
| Dimensions | 15.816 × 15.818 × **8.600** m |
| min Z / XY centre | 0.000 / (0.000, 0.000) |
| Materials | `Toy_cream`, `Toy_glass`, `Toy_ink`, `Toy_steel`, `Toy_stone`, `Toy_trim`, `Toy_glassl_Glow` |
| Glow faces | 16, all outward-facing single-layer quads |
| Normals | 129/129 objects positive signed volume; 0 of 31,500 rays flipped |
| Manifest anchor | **−122.3956749, 37.7801751** |
| Target height | **8.6 m** |
| Shipped file | **98,024 bytes**, 9 draw submeshes (stage 4; was 255,560 / 131) |

The XY box is 15.8 m for a 7.60 m building because the building stands at 45° to
the world axes and the two stoops project 1.20 m onto the pavement. That is
expected, not a scale error.

---

## 1. Corrections to the dossier

The plan was re-verified before modelling, as stage 2 requires. It survived
intact — every measured number in `docs/asset-plans/248-ritch.md` §2.1 was
re-derived here and none moved. Three things are recorded as clarifications
rather than corrections:

1. **The manifest anchor is 0.40 m north-east of the plan's figure.** The plan
   quotes −122.3956780, 37.7801725, the centre of the built quad. The exported
   model's XY bounding-box centre is −122.3956749, 37.7801751, because the two
   stoops project past the street wall. Contract rule 2 puts the origin at the
   bbox centre, so **the manifest must use the second number**. Both are in the
   build script (`DESIGN_ANCHOR` and the reported shift).

2. **The registry point stays where the plan put it**, −122.3957213,
   37.7801827 with `exclude: 3`. It is a different point from the manifest
   anchor on purpose; §2.13 of the plan has the measured window and the reason.

3. **The plan's 2.7 #12 gives the front parapet an inside face at 8.40 m.** In
   the model the front's parapet *is* the cornice, so there is no separate
   upstand there; the rear and both flanks carry a 8.35 m upstand and the front
   reaches 8.60 m at the crown. The intent — a deck that reads as a shallow tray
   with a taller street edge — is met.

## 2. The entry was rebuilt: layered panels, not a recess

The first pass modelled the twin entries the way the real building reads them —
a 0.35 m recess, an ink solid sunk into the wall with the doors standing inside
it. It rendered as **one black rectangle**. The wall is a closed prism and
nothing in this project cuts it, so the doors, both transoms and both glow plates
were simply buried inside the ink block.

Every opening in this codebase is built as **layered proud panels** instead: the
dark reveal stands a few millimetres in front of the wall, the door leaf a few
in front of that, the glow plate in front of that again. Rebuilt that way the
entry reads correctly.

A second pass split the reveal in two. A single 3.15 m ink panel across the whole
entry zone left a 0.75 m black band between the doors where the real building has
a wall pier, and the entry read as one dark slot rather than two front doors.
Two 1.21 m pockets with cream between them is the fix.

## 3. The stoops were inverted

`d0 = -STOOP_D * (STOOP_STEPS - 1 - s) / STOOP_STEPS` gave the **top** step the
full 1.20 m depth and the bottom step 0.30 m — an upside-down stair. Both stoops
merged into one grey plinth spanning the whole frontage. Corrected to
`depth = STOOP_D * (STOOP_STEPS - s) / STOOP_STEPS`: bottom step deepest, top
step a 0.30 m landing at the threshold.

## 4. Coincident faces: the basement, twice

The raised basement was first built proud on the **street face only**, leaving
its two flanks and its rear exactly coincident with the body prism's walls. The
party-wall elevation rendered it as a dark band you could see through into the
building — the classic ambiguous-first-hit signature. Fixed by offsetting all
four sides by `BASE_PROUD`.

That fix moved the problem to the bottom: with the basement lowered to −0.04 m
to clear the body's base cap, `min Z` went negative and the bounding box grew to
8.64 m, which would have made the loader's `targetHeightM / measuredHeight`
scale 0.995 instead of 1.0. The right fix is the other way round — **lift the
body to +0.03 m** and leave the basement defining `min Z = 0`. The stoops and the
rear stair start at +0.006 m for the same reason.

The general rule this asset follows, and the reason `EMBED` exists: **nothing is
ever flush**. Every applied solid either stands clear of its host or is sunk into
it. The result is 0 flipped faces out of 31,500 rays, with no tolerance spent.

## 5. The glow plates were not being checked

The validator routes anything whose name contains `_glow` to the open-strip test
— *is this single face the first thing a ray fired along its own normal hits?* —
because signed volume is meaningless for a one-quad object. The plates were named
`bayglow0`, without the underscore, so they skipped that check entirely and were
scored as closed solids, passing **accidentally** on the sign of a degenerate
volume. Renamed to `bay_glow0` / `transom_glow0`, all 16 faces are now explicitly
tested and all 16 pass.

This is worth recording because the failure was silent and the run before it said
PASS on sixteen of seventeen checks.

## 6. The top view rendered upside down

`rz = LONG_AXIS - 90` put the bay at the bottom of the frame. For a top-down
camera image-up maps to world `(−sin rz, cos rz)`, and `LONG_AXIS` is the
front→rear bearing, so image-up must be `LONG_AXIS + 180`, giving
`rz = LONG_AXIS + 90`. Same 180° trap the review-rig notes record for track-quat
top views.

## 7. Design decisions worth defending

**The rear garden is not in the asset.** The rear third of the parcel is real
garden, and the Case B exclusion clears the whole parcel's procedural footprint,
so that ground will be bare in the app — correctly, because it *is* ground. No
ground plate was added: assets in this project that cover ground must be
terrain-draped, and the loader seats an asset from a single elevation sample at
the anchor, which over 24 m of lot with a 1.24 m LiDAR ground range would float
or sink one end.

**The roof is designed, not decorated.** A 7.6 × 13.9 m membrane deck is the
largest single surface the app's downward camera sees here. What is on it —
welded seams every 2.2 m, a walk pad from the bulkhead to the hatch, two drains
at the rear corners, a stair bulkhead, a chimney and three vent stacks — is what
a re-roofed flat deck actually carries. There is no solar, no deck furniture and
no planters, because there is no evidence for any of it.

**Chimney breasts on both flanks.** The 2008 permit removed two fireplaces and
describes their "chimneys 1/2 way back on side". A shallow pilaster on each party
wall, half the depth back, is what that sentence describes. It also solves a real
problem: 246 Ritch next door is 15.87 m against this building's 8.6, so the
north-west flank is genuinely exposed in the app, and a blank 13.9 × 8 m slab is
not a designed surface. **No property-line windows were invented** to go with
them — unlike 550 Third, no permit here records any.

**The bulkhead's top is `Toy_steel`, not `Toy_ink`.** A dark roof object on a
landmark this small reads as a black hole from the app's downward camera; the
recorded failure is a whole roof deck in `Toy_roofd` rendering rgb(9,9,12). Only
the hatch, which is genuinely a dark opening, stays dark.

**One exaggeration, and only one.** The bay projects 0.55 m where the real one is
nearer 0.40. The height is deliberately untouched: the whole point of this asset
is that it is short next to 246 Ritch, and inflating it would destroy the only
thing the building says.

## 8. Night state

Domestic, not commercial: the **six bay panes** and the **two door transoms**
only. The flat-wall upper window and the entire rear stay dark — two flats, not
an office floor. All eight are single outward-facing quads standing proud of the
opaque glazing, never closed shells, because the app draws `_Glow` in a separate
layer that is translucent by day and a closed box shows front and back and reads
at roughly twice the intended day alpha.

The glow colour is `Toy_glassl_Glow` (`6f95b8`), **not** `Toy_glass_Glow`
(`2a4d73`). The app shows a `_Glow` surface's raw base colour at night, so the
dark navy of unlit glass would render as a dark window pretending to be a lit
one.

**The glow colour was changed from `Toy_glassl_Glow` (`6f95b8`) to
`Toy_gold_Glow` (`caa64a`) at stage 5, and it should have been warm from the
start.** The first build used the project's glazing blue, which is what the
glass-fronted landmarks use and what the closest analogue (49 South Park) ships.
In the stage-5 night QA, against 246 Ritch next door and the procedural
residential windows all around — all of them warm yellow — this house read
COLD: two occupied flats looking like an empty office. §2.8 of the plan asked
for a domestic night state, "warm, partial, uneven", and the build did not
deliver it until this change. `caa64a` is a palette colour already used by 35
shipped assets and is both warmer and brighter (luma 167 against 143).

The lesson is the one already recorded for this project: a `_Glow` material's
BASE colour **is** its night appearance, there is no emission multiplier to warm
it later, and the check that catches the mistake is looking at the building at
night **next to its neighbours** — not at a Blender night render, where the
emission strength flatters everything.

**The night render's emission was dropped from 3.2 to 2.2.** At the reference
implementations' 3.2 the six bay panes blew to flat white — six large panes on a
7.6 m front are a far bigger share of the frame than seven narrow bays on a
12.9 m one. That matters beyond looks: the app does not multiply a `_Glow`
surface at all, it shows the raw base colour, so a render brighter than the base
value is exactly the flattery that has previously hidden a too-dark glow colour
until local QA at 22:30. At 2.2 the render sits near what the app will actually
draw.

## 8b. The fallback drill's first run was inconclusive, not passing

Worth recording because the failure looks exactly like a pass. The first Step-6
run reported `entries: 91, far: 73, live: 18, loading: 0, fading: 0, failed: 0`
with the GLB moved aside, the app alive and the city rendering — which reads as
"the asset is missing and nothing broke".

It is not. The 18 live entries are the **resident** manifest rows, the ones with
no `loadRadius` that `load()` places during boot. `far: 73` says the streaming
scan never reached this entry, so the loader never **attempted** the missing
file. `failed: 0` there means *never tried*, not *degraded gracefully*. The
machine was at load average 478 with eighteen headless Chrome instances from
sibling pipeline sessions, and the app's frame loop was not ticking, so
`assets.update()` never ran.

Hand-pumping the scan on a 200 ms interval was the obvious fix and it did not
help: the second run reported `attempted: false` too. Adding diagnostics found
the real cause, and it was in the rig, not the app — **`SF is not defined`**. The
drill slept a fixed 8 s after navigation before calling `SF.goTo`; at this load
the app takes minutes to boot, so `goTo` threw into a swallowed exception, the
camera never left its default position, and the streaming scan was correctly
reporting that a landmark 2.5 km away was out of range.

Three fixes, all of which belong in any rig that drives this app:

1. **Gate on the app existing**, never on a fixed sleep — poll
   `typeof SF !== 'undefined' && SF.assets && SF.goTo` before touching anything,
   and report `INCONCLUSIVE` rather than a result if it never becomes true.
2. **Refuse to report a pass until `failed > 0`** proves the loader actually
   reached for the file.
3. **Recover a stale `.drill-aside` on startup.** A crashed predecessor left the
   GLB moved, and the next run died on `ENOENT` trying to move an absent file.

The restore guard earned its keep along the way: killing the stale run with
`SIGTERM` fired its handler and put the GLB back byte-identical. Wiring restore
to `exit`/`SIGINT`/`SIGTERM` and not only to `finally` is what made that safe.

**The conclusive run:**

```
app booted: true
rig pivot: {x: 3680.43, y: 5.85, z: -1124.76}     <- the model's own location
pump ticks: 15, pump error: null
asset was actually attempted (failed>0): true
stats: entries 91, far 6, loading 0, live 84, fading 0, failed 1
app still alive (city stats present): true
sf-assets: 248-ritch failed to load (Unexpected token '<', "<!doctype "...)
restored
```

Exactly one failed entry, exactly one warning line for this asset, the app boots
and the rest of the city renders. The warning is a parse failure rather than a
404 because Vite answers a missing `public/` path with the SPA `index.html` at
HTTP 200 — a dev-server artifact, not a defect. Case B, so the site is bare
ground inside the exclusion zone with the asset gone, which is expected.

## 9. Files

```
artifacts/248-ritch/
  build_248_ritch.py       deterministic build (Blender 5.2 LTS, headless)
  render_248_ritch.py      review renders; --fast swaps Cycles for Workbench
  validate_248_ritch.py    fresh-scene contract validation
  make_contact_sheet.py    composes the sheet
  248-ritch.blend          authoring scene
  248-ritch.glb            THE ASSET (stage-4 optimized; the pre-optimize
                           original is archived at optimize/input/)
  optimize/                stage 4 - scripts, stats, A/B renders, REPORT.md
  248-ritch-{east,west,north,south,top,aerial,facade}.png
  248-ritch-aerial-night.png
  248-ritch-contact-sheet.png
  REFERENCE.md             the research dossier
  REPORT.md                this file
  validation.json          machine-readable contract report
```

`--fast` renders in Workbench rather than Cycles. It exists because iteration
passes on this shared machine were taking 60–90 s a frame at load 90+, and
Workbench does the same eight views in under three seconds. It is **not** what
ships: every committed render is Cycles. Workbench reads `diffuse_color` rather
than the Principled base colour, so the fast path copies one to the other — the
first attempt without that came out entirely grey.

## 10. Draft manifest entry

```json
{
  "id": "248-ritch",
  "file": "248-ritch.glb",
  "anchor": [
    -122.3956749,
    37.7801751
  ],
  "targetHeightM": 8.6,
  "cat": 2,
  "name": "248-250 Ritch Street",
  "estimated": false,
  "dims": [
    15.8158,
    15.8177,
    8.6
  ],
  "tris": 3572,
  "loadRadius": 2500
}
```

Registry entry for `pipeline/lib/landmarks.mjs` (Case B — the point is
deliberately **not** the manifest anchor; see the plan's §2.13):

```js
{
  id: '248Ritch',
  name: '248-250 Ritch Street',
  lon: -122.3957213,
  lat: 37.7801827,
  height: 8.6,
  exclude: 3,
  camera: { distance: 120, yaw: 135, pitch: 28 },
}
```

## 11. Approval

Gate 3 was satisfied by a **blanket pre-authorisation given at the start of the
session**, quoted verbatim:

> APPROVE EVERYTHING DONT ASK ME FOR PERMISSION

18 August 2026, David (repo owner), in the session's opening message.

Recorded honestly: this instruction **predates the renders**, so it is a standing
authorisation to run the pipeline without stopping, not a design review of these
eight images. The contact sheet, both aerials and the night state were presented
before advancing, and the reviewable concerns are named in `REFERENCE.md` §7 —
the rear and both party walls are inferred, and nothing in the record observes
them. If a later reader wants a real design review of this asset, that has not
happened.

---

# Stage 5 — integration (batch mode)

Run 18 August 2026. **Batch mode**: sibling sessions were building 246 Ritch,
252–254 Ritch and 49 Zoe on the same machine at the same time, so the bake was
run for QA and then discarded, and this branch commits **source only**.

## Local QA

| Check | Result | Evidence |
|---|---|---|
| Re-validation before touching `app/` | PASS | 17/17 contract checks on the shipped GLB |
| Manifest entry | PASS | appended as text; 19 insertions, no diff on the other 90 entries |
| `camelId` round trip | PASS | `camelId('248-ritch')` → `248Ritch`, matches the registry |
| Case B registry entry | PASS | in `LANDMARKS` (97 total), `VIEW_PRESETS` untouched at 6 |
| Re-bake | PASS | full chain `terrain … muni-shapes`, 6.5 min |
| `muni-shapes.bin` survived | PASS | unmodified, no `shapes bad magic` |
| `audit.mjs` check 1.6 | PASS | 100 zones over 97 landmarks clear |
| `verify-rebake.mjs` | PASS | only cell `23_13` moved, 182 → 181 |
| Merge line / loader scale | PASS | `248-ritch merged 9 objects / 7 materials → batched (2141 tris body); uniform x1.0000 at 3680, -1125` |
| Orientation | PASS | bay and both entries face Ritch Street |
| Terrain seating | PASS | no float, no sink |
| Night glow | PASS **after a fix** | see §8 — the first build's glow was cold and was changed |
| Failed entries | PASS | `failed: 0` with the asset present |
| Single building on the site | **PASS with a caveat** | see below |
| Fallback drill | see §8b | first run inconclusive; re-run pumped |

Screenshots from the live app are committed as `248-ritch-app-day.png`,
`248-ritch-app-night.png` and `248-ritch-app-wide.png`.

## The one real caveat: a 1.28 m overhang from 252–254

`verify-rebake` reports the nearest surviving footprint at 6.1 m against a 3 m
radius, which passes. But that check measures from the registry point, and its
per-cell count has a known blind spot, so the site was settled **from the tile**:
`app/public/tiles/buildings/23_13.bin` decoded, and every surviving ring
point-in-polygon'd against the model's built quad.

One survives inside it — a 9.0 m block covering **12.8%** of the quad, reaching
**1.28 m** over the south-east party line along the full 13.9 m depth. It is
252–254 Ritch.

This is not the exclusion failing. Both of this building's own rings were
dropped. It is a registration disagreement between two DataSF layers. In the lot
frame (t across the frontage, 0 = the surveyed party line):

| Source | this building | 252–254 |
|---|---|---|
| surveyed parcel (`acdm-wktn`) | t 0 → 7.60 | t −7.60 → 0 |
| LiDAR footprints (`ynuv-fyni`) | t **1.22 → 8.93** | t −6.70 → **1.28** |
| OSM / Overture | t 2.24 → 10.18 | t −5.57 → 2.33 |

All three are internally consistent — each layer tiles the two lots cleanly and
the two DataSF footprints do not overlap **each other** at all. They simply
disagree with the survey by +1.25 m, and OSM by +2.3 m. The bake reads the
footprint layer, so the neighbour's baked block sits 1.25 m north-west of where
the survey puts its wall.

**Why the anchor was not moved.** Shifting this model 1.25 m north-west would
align it with the footprint layer and remove the overlap entirely. That is
exactly what `INTEGRATION-PROMPT.md` Step 3 forbids — "never nudge them to make
the model sit better; if the model looks wrong at its real anchor, the model is
wrong" — and AGENTS rule 5 with it. The surveyed parcel is the real position.

**Why `exclude` was not raised.** The ceiling is 5.04 m (252–254's Overture ring)
and its DataSF ring goes at 6.07 m. Reaching either deletes 252–254 outright, and
on this branch nothing replaces it: that trades a 1.28 m overhang for a hole in
the alley wall.

**What it actually looks like.** Nothing. At the camera preset the two read as
adjacent buildings, which is what they are — the neighbour genuinely stands
there and is genuinely about that height. The block is 9.0 m against this
building's 8.6, so 0.4 m of it stands above the cornice along a 1.28 m strip at
the party line. It is visible in principle and not visible in practice.

**The clean fix belongs to the batch.** A `254-ritch` session was in flight while
this ran. Its own exclusion drops `SF3776106`, and the overhang disappears with
no change here. Flagged rather than depended on.

## Batch handoff

The bake was discarded with `git checkout -- app/public/tiles api/_data`.
`git diff --name-only origin/main` lists nothing under either path.

Two notes for whoever runs `BATCH-INTEGRATE.md`:

1. **The `pipeline/data` snapshot reproduced main's tiles exactly** — exactly one
   building tile changed, the cell this landmark drops. There is no citywide
   jitter to explain in the PR body.
2. **Check the `254-ritch` session's scope.** 252 and 254 are one parcel
   (3776-106), one building, two flats — the same shape as this one. If that
   session scoped 254 as separate from 252, only one of the two can own the
   exclusion and the other leaves a hole. This is the failure that produced the
   21/27 and 92/96 South Park duplicates.
