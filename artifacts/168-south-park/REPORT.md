# 166–168 South Park — build report

Asset: `artifacts/168-south-park/168-south-park.glb`
Plan: `docs/asset-plans/168-south-park.md`
Dossier: `REFERENCE.md` (this asset's own research; it beats the plan where they differ)
Built: 16 August 2026, Blender 5.2.0 LTS, `build_168_south_park.py`

## 1. Shipped numbers

| | |
|---|---|
| Triangles | **3,504** (budget 6,000) |
| Objects | 52 |
| Materials | 8 — `Toy_brick`, `Toy_glass`, `Toy_glass_Glow`, `Toy_ink`, `Toy_steel`, `Toy_stone`, `Toy_trim_Glow`, `Toy_white` |
| Glow groups | 2 — `Toy_glass_Glow` (two lit second-floor windows), `Toy_trim_Glow` (shopfront spill) |
| AABB dimensions | 25.703 × 25.504 × 10.440 m |
| Footprint in plan (shell) | 6.10 × 29.82 m — the modelled parallelogram |
| Footprint in plan (envelope) | 6.099 × 30.998 m measured off the exported GLB; the extra 1.18 m of depth is the front pilasters (+0.19 m) and the rear fire escape (+0.92 m), both of which are real projections and neither of which is the shell |
| min Z | 0.000 m |
| XY centre offset | (0.056, −0.060) m |
| Crest | **10.440 m** — the gable crown, exactly on target, so the loader's `targetHeightM / measuredHeight` lands at 1.0 |
| Anchor | `-122.3949862, 37.7811327` |
| Front heading | 135° true (SE), authored, no rotation at load |
| Validation | `validation.json` — **all 16 checks PASS** |

## 2. Deliverables

`build_168_south_park.py`, `render_168_south_park.py`, `validate_168_south_park.py`,
`make_contact_sheet.py`, `168-south-park.blend`, `168-south-park.glb`,
`REFERENCE.md`, `REPORT.md`, `validation.json`, and the renders:
`-north`, `-east`, `-south`, `-west`, `-front`, `-top`, `-aerial`, `-aerial-night`,
`-contact-sheet`.

`-front.png` is an extra view beyond the standard rig: the four compass
elevations each show two faces at 45° on this heading, which is correct but
useless for judging the one elevation that carries design.

## 3. Dossier corrections made while modelling

Two, both recorded in `REFERENCE.md` and both carried back into the plan's own
numbers where they moved:

1. **The parapet was built as one continuous stepped wall, not three panels.**
   The plan's §2.7 reads as three separate parapet panels over three bays. Built
   that way (first and second aerial reviews) the silhouette dipped back down to
   the flank return between the pilasters, and the three steps read as blocks
   floating off the top of the wall. The photograph shows a monotone climb —
   flank return, one step up on each side, then the raised centre — so the
   parapet is now a single wall panel with a stepped top profile, and the
   pilasters run into it flush rather than in front of it.
2. **The shoulder height moved from 9.55 m (plan, inferred) to 9.78 m
   (photogrammetric).** See §4.

One thing the plan got right that was worth re-checking: the anchor. Building on
the DataSF LiDAR centroid instead of the OSM ring centroid would have put the
model 1.08 m off its own party walls on a 6.1 m frontage and pushed the XY
centre offset to the edge of the contract's ~1 m tolerance. The shipped offset
is 0.06 m.

## 4. The height question, answered

The plan's §2.15 risk 1 asked whether the DataSF LiDAR maximum of 10.44 m is the
real parapet crest or bleed from 188 South Park (15.93 m) across the shared
party wall, and said it had to be settled before the model shipped, because it
is the number the loader divides by.

**It is the real crest.** Method: a door-scaled tangent-ratio measurement of the
Jan 2025 Street View capture (pano at `37.780973, -122.394785`, heading 316°,
tilt 98t, vertical fov 75° over a 1000 px viewport, so focal length 651.6 px and
elevation(y) = 8° − atan((y − 500) / 651.6)). Taking ratios of tangents against a
known door height cancels both the camera height and the camera distance, which
are the two things not known here:

```
h(P) = door_height x (tan e_P - tan e_base) / (tan e_doorhead - tan e_base)
```

| feature | y (px) | elevation | height above the wall base |
|---|---|---|---|
| wall base at the doors | 785 | −15.63° | 0 (datum) |
| left entrance door head | 640 | −4.13° | 2.10 m (assumed; 6'11") |
| south-west parapet shoulder | 205 | +32.35° | **9.24 m** |
| central parapet crest | 172 | +34.72° | **9.84 m** |

With a 7 ft (2.13 m) door instead: 9.37 m and 9.98 m.

So the photogrammetry lands the crest at 9.8–10.0 m against the LiDAR's 10.44 m
— about 5% low, and three independent effects all push the same way: a ±10 px
reading error is ±0.25 m at the crest; the door height is assumed; and the LiDAR
`gnd_min_m` datum is the *lowest* ground cell under an outline that is inflated
1.3 m and therefore overlaps the sidewalk and the rear yard, so it sits below
the sidewalk at the door. That is a consistent measurement, not a contradiction.
The bleed hypothesis is refuted outright: contamination from a 15.93 m neighbour
would put the maximum *above* 10.44 m, not 0.5 m below it, and there is a
physically raised parapet in the photograph exactly where the maximum has to be.

**10.44 m is kept** — it is the measured source and AGENTS rule 5 wants real
heights from measurement. What the photogrammetry *did* change is the shoulder:
the measured shoulder-to-crest ratio is 9.24 / 9.84 = 0.939, so the shoulder is
0.939 × 10.44 = 9.80 m, and the model uses 9.78 m. The plan's inferred 9.55 m
was 0.25 m low.

## 5. Deliberate deviations from the contract

- **"Front faces −Y" is not honoured.** The building's real heading is 135° and
  the loader applies no rotation, so the model is authored on its true bearing
  (AGENTS rule 5). This is the same deviation every South Park asset takes.
- **The axis-aligned bounding box is 25.7 × 25.5 m** for a 6.10 × 29.82 m
  building. That is the 45° heading, not a scale error.

## 6. What stayed inferred

Stated plainly, because it is easy to read a finished miniature as if every
surface were observed:

- **The three second-floor bays.** One opening is visible; the count of three
  comes from the three parapet panels. A street tree hides the middle of the
  facade in the only capture that reaches this frontage, and the pano's date
  picker would not open in this session, so earlier captures were not consulted.
- **The whole rear elevation** except the fire escape, which is
  permit-confirmed (9510796, 1995). The door, the two small openings and the
  fire escape's exact form are invention constrained only by plausibility.
- **The flank parapet return at 8.60 m.** Not visible in any capture; only the
  two shoulders and the crest were measurable.
- **The roof's two skylight runs.** A semantic inference: the nadir imagery
  shows a loose line of small dark items, and a 6 m wide, 30 m deep loft has no
  other daylight in its middle. Number and position are not observed. Everything
  on the roof is kept under 0.6 m so it stays consistent with the LiDAR's 0.75 m
  standard deviation, which says nothing tall stands up there.
- **The palette.** `Toy_brick` (`c96f4a`) rather than the browner `Toy_rust`, on
  the argument recorded in `artifacts/358-brannan`: this front is 6 m wide and
  has to advance against 188 South Park's cool grey-and-glass party wall. The
  brick colour was chosen for that job, not sampled from the photograph.

## 7. Iteration log

| # | Change | Why |
|---|---|---|
| 1 | First build: three separate parapet panels, 0.30 m parapet, three vents on the roof | baseline from the plan's §2.7 |
| 2 | Parapet thinned to 0.24 m; parapet panels moved flush with the pilasters; panel copings clamped to panel width; doors given glazed fills; roof given two skylight runs, a duct and a hatch | first aerial review: the grey coping ring ate ~30% of the roof's width from above, the copings overhung the building edge as grey nubs, the doors read as solid slabs, and 29.8 m of roof carried three small objects |
| 3 | Parapet rebuilt as one continuous stepped wall | second aerial review: the silhouette dipped between the panels, so the steps read as floating blocks instead of a climbing wall |
| 4 | Shoulder 9.55 → 9.78 m; side diamonds 9.03 → 9.14 m | the photogrammetry in §4 |

Triangle count across the four: 2,960 → 3,608 → 3,504 → 3,504.

## 8. Approval (gate 3)

The session's standing instruction, given with the task on 16 August 2026, was:

> "APPROVE EVERYTHING DONT ASK ME FOR PERMISSION"

That is a blanket pre-approval to run the pipeline without stopping, and it is
what advanced this asset past gate 3. It is **not** a review of these specific
renders — no one has looked at the contact sheet and said the building is right.
The renders are in this folder and the aerial, front and night views are the
three worth a minute of the owner's time before this ships to production.

## 9. Draft manifest entry

```json
{
  "id": "168-south-park",
  "file": "168-south-park.glb",
  "anchor": [
    -122.3949862,
    37.7811327
  ],
  "targetHeightM": 10.44,
  "cat": 3,
  "name": "166-168 South Park",
  "estimated": false,
  "dims": [
    25.7032,
    25.5037,
    10.44
  ],
  "tris": 3504,
  "loadRadius": 2500
}
```

`dims` and `tris` will be restated after stage 4 (optimize) if the optimizer
changes them.
