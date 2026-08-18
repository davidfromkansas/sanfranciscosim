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
| Objects | 129 |
| Dimensions | 15.816 × 15.818 × **8.600** m |
| min Z / XY centre | 0.000 / (0.000, 0.000) |
| Materials | `Toy_cream`, `Toy_glass`, `Toy_ink`, `Toy_steel`, `Toy_stone`, `Toy_trim`, `Toy_glassl_Glow` |
| Glow faces | 16, all outward-facing single-layer quads |
| Normals | 129/129 objects positive signed volume; 0 of 31,500 rays flipped |
| Manifest anchor | **−122.3956749, 37.7801751** |
| Target height | **8.6 m** |

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

**The night render's emission was dropped from 3.2 to 2.2.** At the reference
implementations' 3.2 the six bay panes blew to flat white — six large panes on a
7.6 m front are a far bigger share of the frame than seven narrow bays on a
12.9 m one. That matters beyond looks: the app does not multiply a `_Glow`
surface at all, it shows the raw base colour, so a render brighter than the base
value is exactly the flattery that has previously hidden a too-dark glow colour
until local QA at 22:30. At 2.2 the render sits near what the app will actually
draw.

## 9. Files

```
artifacts/248-ritch/
  build_248_ritch.py       deterministic build (Blender 5.2 LTS, headless)
  render_248_ritch.py      review renders; --fast swaps Cycles for Workbench
  validate_248_ritch.py    fresh-scene contract validation
  make_contact_sheet.py    composes the sheet
  248-ritch.blend          authoring scene
  248-ritch.glb            THE ASSET
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

_Stage 3 pending._
