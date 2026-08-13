# 165–167 South Park — SF-SIM asset plan

A 1908 two-storey, three-unit wooden flats building on the south rim of South Park, the
oval that is San Francisco's oldest planned residential square. It is not a monument and
not even a notable building — it is a *sliver*: 6.4 m of frontage, 24 m of depth, a flat
facade with no bay window, and one saturated blue steel gate that is the only thing
distinguishing it from the identically-clad house next door.

It is the first plan in this set for a **South Park rim** building and the first for the
*narrow-lot party-wall flats* type, where the subject shares walls with neighbours on both
sides and is legible only by its own width. The design brief is "the narrowest credible
building in a continuous row", not "landmark" and not "generic block".

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/165-south-park/`. This document is the plan only: Part 1 is the runnable task
prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `165-south-park` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor (manifest, placement) | `-122.3943863, 37.7808673` |
| WGS84 anchor (registry, exclusion only) | `-122.3943963, 37.7808764` — **deliberately different, see 2.13** |
| Target height | **9.0 m** to the front cornice crest (*estimated*); roof deck 8.55 m (measured, LiDAR) |
| Footprint | 6.40 m frontage narrowing to 4.27 m, 24.0 m deep; 131 m², derived from the surveyed parcel |
| Axis | front block ~157°, rear block 135.3°; front facade faces **349.7°** |
| Triangle cap | 6,000 |
| Category | `1` (residential) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 165–167 South Park GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of the flats building at 165–167 South Park,
San Francisco, and deliver it as a downloadable, validated GLB.

Do not integrate or deploy the model yet. Create the asset, validate it, render
review images, and commit the deliverables to your working branch.

## Read the project sources first

Before any research or modeling, read in this order:

1. `AGENTS.md`
2. `docs/styles/README.md`
3. `docs/styles/miniature-toy.md`
4. `.agents/skills/sf-miniature-style/SKILL.md`
5. `.agents/skills/sf-asset-check/SKILL.md`
6. `app/public/sf-assets/landmarks_manifest.json`
7. `artifacts/541-presidio/` — the closest reference implementation in scale and budget
   (small two-storey residential building, low triangle count, restrained night state)
8. `docs/asset-plans/165-south-park.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Must capture

- **The narrowness.** 6.4 m of frontage against 24 m of depth. This proportion *is* the
  building. A modeller who rounds it toward a square house has failed.
- The **flat street facade** — pale blue-gray horizontal lap siding, punched windows, and
  **no projecting bay window**. This is unusual for a San Francisco flats building and it
  is a positive fact about this one, not an omission. Do not add a bay.
- The **vivid blue steel picket gate** at the east edge of the frontage, filling a
  full-height gated passage between this building and 159 South Park. It is the only
  saturated colour on the block and the building's single strongest identity cue.
- The **dark stone-tile base band** along the sidewalk (installed 2014), roughly 0.9 m tall
  under the siding.
- A **flat roof** with a simple cornice at the street end — no gable, no hip, no pediment.
- The **taper**: the lot narrows from 6.4 m at the street to 4.27 m at the rear, and bends
  about 22° partway back. Build on the measured polygon in 2.3, not on an axis-aligned box.

## Research 165–167 South Park independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- The street (north) elevation, which is the only elevation the public ever sees
- The roof from above — flatness, the parapet or cornice profile, any stair bulkhead,
  chimney, skylight or mechanical box. This is *inferred* in this dossier and is the
  weakest part of it.
- The rear (south) elevation and the rear yard, visible only from the air
- The two party-wall flanks, which are largely blind
- Day and night appearance
- The window count and rhythm on both storeys of the street facade — the dossier's
  reading is *inferred* from a single Street View pano and must be confirmed
- Whether the building is two full storeys over its whole depth or steps down at the rear

Prefer DataSF datasets, SF Planning records, assessor data, geolocated photography and
aerial imagery. Never rely on a single photograph, a single AI-generated image, or a
single unsourced 3D model. Separate verified facts from visual inference; if sources
disagree, document the disagreement and decide.

**Four source problems are already known and resolved in 2.1–2.3 and 2.15 — re-check them,
do not silently re-inherit the wrong value:**

1. **No OSM way carries the address 165.** OpenStreetMap maps this building inside
   `way/124889480`, tagged `addr:housenumber=167`, a coarse Bing trace that overlaps its
   neighbour at 159 and is 31.7 × 7.8 m — larger than the whole lot. **Do not use OSM
   geometry for this building.** The footprint in 2.3 comes from the surveyed DataSF
   parcel, cross-checked against the DataSF LiDAR building footprint.
2. **The DataSF LiDAR footprint is offset ~3.7 m streetward** from the surveyed parcel
   line: its depth range along the lot axis runs −3.68 m to +24.22 m where the parcel front
   line is 0. The +24.22 m rear extent is trustworthy and sets the built depth; the −3.68 m
   front overshoot is raster registration error plus cornice capture and must be discarded.
3. **The pedimented entry porch a few metres west belongs to 171 South Park, not to this
   building.** 171 wears the same pale blue-gray lap siding and reads continuously with
   165–167 in every photograph. Model the gate, not the pediment.
4. **The published 2,680 sq ft is the assessor's gross floor area**, not a footprint. Over
   two storeys it implies ~124.5 m² per floor, which is why the built depth in 2.3 is 24 m
   and not the 26 m the LiDAR blob suggests.

## Create a reference dossier

Write `artifacts/165-south-park/REFERENCE.md` containing: source links and what each
establishes; verified dimensions and location; orientation; observations from all
four sides and above; the 3–5 strongest recognition cues; features to preserve;
features to simplify; uncertainties and conflicting evidence. A contact sheet of
attributed reference thumbnails is welcome if legally permissible — do not commit
copyrighted full-resolution imagery.

## Make your own design decisions

Follow the conversion process in `docs/styles/miniature-toy.md` §22: identify the
recognition cues, strip nonessential information, rebuild the massing from a few
confident volumes, exaggerate only the signature features, simplify the facade
into broad rhythms, deliberately design every surface visible from above,
evaluate from the app's high three-quarter aerial camera, then simplify again.

This is a **background building** in the style bible's detail budget (§21) — one step below
even the secondary tier. Clear massing, one facade rhythm, a flat designed roof, and
exactly one identity cue carried hard: the blue gate. Resist adding ornament of any kind.
The correct outcome is a building that is obviously *this* sliver and obviously *not* its
neighbour, achieved with under 6,000 triangles.

The finished asset must be immediately recognizable as this building, consistent with the
real one from all four sides and above, architecturally credible, and a premium
handcrafted miniature — not photorealistic, not voxel art, not generic low-poly, and never
accurate in one view while invented in the others.

## Scope of the exported asset

Export the single building: the two-storey clapboard volume on the measured footprint, the
stone-tile base band, the street facade's openings, the blue gate and its passage opening,
the flat roof with its cornice, and whatever roof incident the research confirms.

Do not include unrelated surrounding city geometry: 159 South Park, 171 South Park, the
South Park oval or its lawn and trees, the street, the sidewalk, the street tree in front,
parked cars, people, plinths, cameras or lights. Temporary context may appear in review
renders but must not leak into the GLB.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary
`.glb`; real-world meters; origin at base center; minimum geometry Z ~ 0;
applied transforms; no negative scales; outward normals; no duplicate or foreign
geometry; no image textures; no transparency; flat-color materials named `Toy_*`
from the project palette; `_Glow` suffix only on surfaces that glow at night; no
`Toy_body`; no cameras, lights, animations, armatures or constraints; at most
6,000 triangles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model
drops into the city at its real-world heading — the loader applies no rotation
(`placeGeneric` in `app/src/assets.js` only scales and positions). The street facade faces
**349.7°**, the front block runs back at ~157° and the rear block at 135.3°. Build directly
on the measured polygon in 2.3 rather than modelling an axis-aligned bar and rotating it.
Record the measured heading in `REPORT.md`.

**Height normalization:** the tallest geometry in the export (the front cornice crest) must
land at exactly **9.0 m** so the loader's `targetHeightM / measuredHeight` scale is 1.0.

## Reproducible Blender workflow

Blender 5.2 LTS. Headless: `blender -b --python script.py -- args`.

Keep `artifacts/165-south-park/build_165_south_park.py` (deterministic build script),
`artifacts/165-south-park/165-south-park.blend`, and
`artifacts/165-south-park/165-south-park.glb`. The script must rebuild the model reliably
enough for future revision. Do not modify or rename an unrelated existing GLB to satisfy
the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`165-south-park-top.png`, `-north.png`, `-east.png`, `-south.png`, `-west.png`, plus
`165-south-park-contact-sheet.png`, at least one high three-quarter aerial beauty
render `165-south-park-aerial.png`, and a night render
`165-south-park-aerial-night.png`.

The four elevations must share scale, framing, lighting, exposure and projection; use
orthographic or long-lens cameras; label directions from the researched orientation; the
top view must clearly show the roof plane, the cornice, the taper and the bend; the aerial
view uses the style bible's camera assumptions (30–50 degrees down, long lens). Simple
tabletop lighting, neutral warm background, minimal depth of field, and every image must
depict the same exported model.

Because the building is nearly 4× deeper than it is wide, frame the elevations to the long
dimension and accept empty frame on the north and south views rather than zooming each
view to fit — the reviewer needs to be able to compare them.

## Validate the exported GLB

Re-import `165-south-park.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture
count, camera count, light count, animation count, applied-transform status,
negative-scale status, normal-orientation status, unexpected geometry, and
per-material contract compliance. Render at least one review image from the
re-imported asset. Write `artifacts/165-south-park/validation.json` and
`artifacts/165-south-park/REPORT.md`.

Note that the axis-aligned XY bounding box will be roughly **18.8 × 21.8 m** even though
the building is 6.4 × 24.0 m — that is the expected consequence of the ~145° real-world
heading, not a scale error.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "165-south-park",
  "file": "165-south-park.glb",
  "anchor": [
    -122.3943863,
    37.7808673
  ],
  "targetHeightM": 9.0,
  "cat": 1,
  "name": "165–167 South Park",
  "estimated": true,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

`"estimated": true` is deliberate — the crest height is LiDAR-derived, not published. See 2.15.

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a separate, explicitly requested job — run `docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in `docs/asset-plans/165-south-park.md`.
````

---

## Part 2 — Research and design dossier

Compiled 12 August 2026 from the sources in 2.2. Values marked *inferred* are visual or
derived estimates, not published figures — the executing agent must re-verify
anything it relies on.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Address | 165 and 167 South Park, San Francisco CA 94107 | DataSF address dataset `ramy-di5m`: both numbers resolve to block 3775, lot 028 |
| Parcel | `3775028`, `from_address_num` 165, `to_address_num` 167, zoning `SPD` (SOMA–South Park) | DataSF parcels `acdm-wktn` — **this is the authoritative confirmation that 165 and 167 are one property** |
| Build year | **1908** | Augrented property record (assessor-derived) — post-earthquake reconstruction |
| Storeys | **2** | assessor record; corroborated by Street View |
| Units | **3** | assessor record, classified "flats and duplex", multi-family residential |
| Gross floor area | 2,680 sq ft (249 m²) | assessor record — ~124.5 m² per floor over two storeys |
| Lot | 168.1 m², 6.2 m frontage (chord) narrowing to 4.27 m, 32.7 m deep | DataSF parcel polygon — **measured** |
| Built footprint | ~131 m², 24.0 m deep | parcel truncated at the LiDAR rear extent; see 2.3 — **derived** |
| LiDAR building | `201006.0116627` (`mblr` SF3775028), 109 m², 433 cells at 50 cm | DataSF Building Footprints `ynuv-fyni` — **measured, but offset, see 2.3** |
| Ground | 7.78 m NAVD88 (median), 7.17 m minimum | same |
| Roof deck | **8.55 m** above grade (LiDAR height median); majority 8.50 m | same — **measured**; a flat roof, so median ≈ deck |
| LiDAR maximum | 9.90 m above grade; peak first return 10.00 m | same — parapet, chimney or rear stair bulkhead, unresolved |
| Cornice crest | **9.0 m** | *estimated*: roof deck 8.55 + ~0.45 m cornice. See 2.15 |
| Front facade heading | faces **349.7°** | measured from the parcel's curved front edge (mean bearing 79.7°) |
| Lot axis | front ~157° for ~10 m, then 135.3° to the rear | measured from the parcel side lines, which bend with the oval |
| Siding | wood lap siding, replaced 2014 ($50k exterior permit, "replacement of siding, installation of a new metal gate, and stone tile work") | Augrented permit history — this permit explains all three of the facade's present features |
| Roof | flat; reroofed 1999 and May 2024 ($10k) | Augrented permit history |
| Owner | Dolch 1990 Trust; last sale May 1992 | Augrented / assessor |
| Neighbours | 159 South Park (lot 029, east) and 171 South Park (lot 137–139, west), both party-wall | DataSF parcels + address dataset |
| Neighbourhood | South Park, laid out 1852–54 by George Gordon, designed by George Goddard on the model of a London crescent; SF's oldest planned residential square | Wikipedia, TCLF |

### 2.2 Sources

- DataSF `acdm-wktn` (Parcels), `blklot=3775028` — the surveyed lot polygon, the
  165→167 address range, and the SPD zoning. This is the geometric backbone of the plan.
- DataSF `ramy-di5m` (Addresses with Units), `street_name=SOUTH PARK` — the mapping of
  both 165 and 167 to block 3775 lot 028, and the neighbour lots at 159, 171 and 181.
- DataSF `ynuv-fyni` (Building Footprints, LiDAR-derived, 2010 survey, refreshed
  2023-09-11), building `201006.0116627` — footprint, ground elevation and the height
  statistics used for the roof deck.
- https://augrented.com/sf/3775028-165-167-south-park — assessor-derived build year,
  storeys, units, gross floor area, ownership, and the permit history that explains the
  present siding, gate and stone base.
- https://www.openstreetmap.org/way/124889480 — the only OSM way covering this building,
  tagged `167`. Used **only** as a negative check; see 2.15.
- Google Street View, South Park pano `tRhqK_-aiVsKi23dOxYSeg` (©2025 capture), yaws
  158°–196° — the street elevation: pale blue-gray lap siding, dark stone base band, the
  blue steel picket gate with the painted numerals "165 167" beside it, white-trimmed
  punched windows, and the neighbouring pedimented entry at 171 that must not be copied.
- Google/Airbus/Vexcel aerial imagery of the block (2026) — the flat roof, the rear yard,
  and the continuity of the row along the south rim.
- https://en.wikipedia.org/wiki/South_Park,_San_Francisco and https://www.tclf.org/south-park-ca
  — the oval's 1852–54 origin and its two-storey row-house character.

### 2.3 Orientation and placement

The building occupies the whole width of its lot on the south rim of the South Park oval.
Its street facade sits on the oval's curve and therefore faces **349.7°** — very slightly
west of due north. The lot runs back from the curve as a narrow wedge that bends about 22°
partway along, because South Park's lots are radial at the street and orthogonal at the
rear.

Three separate geometries exist for this building and they do not agree. The plan resolves
them as follows:

| Source | What it is | Verdict |
|---|---|---|
| DataSF **parcel** `3775028` | surveyed lot boundary, 168.1 m² | **authoritative for shape and position** |
| DataSF **LiDAR footprint** `201006.0116627` | 2010 raster-derived built area, 109 m² | **authoritative for built depth only** — its rear extent is +24.22 m from the parcel front line; its front extent of −3.68 m is registration error and cornice capture, and is discarded |
| OSM `way/124889480` | Bing trace tagged `167`, 31.7 × 7.8 m | **rejected** — larger than the lot and overlapping the neighbour at 159 |

The design footprint is therefore the parcel polygon truncated at 24.0 m depth: **131 m²**,
6.40 m wide at the street, 4.27 m wide over the rear 15 m, with a ~7 m rear yard behind it.
That depth is chosen because it reproduces the assessor's 2,680 sq ft over two storeys to
within 5%.

Measured design polygon, in Blender coordinates (metres, `+X` east, `+Y` north), already
centred on the manifest anchor `-122.3943863, 37.7808673`. The eleven short segments across
the top are the oval's curve and may be simplified to three:

```
(  7.246, -11.712)     rear-east corner
( -6.120,   1.787)     west party line, rear segment
( -8.559,   8.949)     west party line, front segment
( -7.948,   9.011)  ─┐
( -7.338,   9.083)   │
( -6.730,   9.166)   │
( -6.123,   9.260)   │
( -5.518,   9.364)   ├─ street frontage, on the oval's curve (6.40 m)
( -4.915,   9.479)   │
( -4.314,   9.605)   │
( -3.715,   9.741)   │
( -3.119,   9.887)   │
( -2.454,  10.064)  ─┘
(  3.775,  -2.136)     east party line, front segment
( 10.282,  -8.707)     east party line, rear segment
```

Read as two pieces:

| Piece | Extent | Notes |
|---|---|---|
| Front block | 6.40 m wide × ~10 m deep, running back at ~157° | carries the whole public elevation |
| Rear block | 4.27 m wide × ~14 m deep, running back at 135.3° | party walls parallel; blind on both flanks |

Because of the ~145° mean heading the axis-aligned bounding box is ~18.8 × 21.8 m. That is
correct and is not a scale error.

### 2.4 What each side shows

**North (street elevation, the only public face)** — Two storeys of pale blue-gray
horizontal lap siding over a dark charcoal stone-tile base band roughly 0.9 m tall. The
windows are punched, flat, and set in plain white trim with a modest projecting sill; there
is **no bay window and no ornament of any kind** — no brackets, no cornice returns, no
pediment. At the east edge of the frontage a tall blue-painted steel picket gate, roughly
1.1 m wide and rising to about 2.6 m, closes a full-height passage between this building
and 159 next door; the house numbers "165" and "167" are painted in red on the siding
beside it. Electrical and gas service boxes and a downpipe are surface-mounted on the
siding. The window rhythm is *inferred* as two openings per storey and must be confirmed.

**East and west (party flanks)** — Blind or nearly blind. The east flank abuts the gated
passage for the first few metres and then 159's wall; the west flank abuts 171. Neither is
visible from the app's camera at any useful angle. Build them as flat siding planes with no
openings.

**South (rear elevation)** — Faces a small rear yard shared with the light wells of the
neighbouring lots, visible only from directly above. Expect a plainer treatment: siding,
a rear door, a stair. Unverified; keep it simple and consistent.

**Top** — This is the surface the app's camera actually sees, and the recognition rests on
it more than on the facade. A **flat roof**, reroofed in 2024, running the full 24 m at a
constant 8.55 m, with the cornice edge lifting to 9.0 m at the street end only. The LiDAR
maximum of 9.90 m indicates one raised object — most plausibly a rear stair bulkhead or a
chimney. Its presence, position and height are *inferred* and are the most valuable thing
to confirm from aerial imagery before building, because in a flat-roofed building it is the
only incident the roof has.

### 2.5 Recognition cues (ranked)

1. **The proportion** — 6.4 m of frontage against 24 m of depth. From the aerial camera
   this is the whole silhouette, and it is what separates the South Park rim from every
   other block in SoMa.
2. **The blue steel gate** — the only saturated colour on the building or its neighbours,
   and the single feature that tells 165–167 apart from 171, which wears identical siding.
3. **The flat, bay-less facade** with punched windows — genuinely unusual for a 1908 SF
   flats building and therefore diagnostic.
4. **The dark stone-tile base band**, which grounds the pale siding and reads as a crisp
   dark line at thumbnail size.
5. **The flat roof and the taper**, seen together from above: a pale sliver that narrows
   and bends as it runs back from the oval.

### 2.6 Miniature translation

**Preserve**

- The 6.40 → 4.27 m taper, the 24.0 m depth, the 135.3° / 157° bend, and the 349.7° facade
  heading, exactly
- The gate's position at the east edge of the frontage and its full height
- The stone base band as a distinct value, wrapping only the street elevation
- The flat roof as a genuinely flat plane, with the cornice lift at the street end only

**Simplify / exaggerate**

- Individual clapboards become flat colour; the siding's horizontality is carried by a
  single shallow shadow groove at each floor line, not by modelled boards
- Window openings become four clean recessed rectangles (two per storey), recessed 0.12 m,
  with a 0.10 m proud sill
- The gate is exaggerated: model it as one solid slab in the gate colour with a shallow
  vertical grooving, roughly 1.3 m wide rather than the real 1.1 m, so it survives at
  thumbnail size. The picket gaps are sub-pixel and must not be modelled as real openings.
- Surface conduit, meters, downpipes and house numbers all disappear
- The stone base band is thickened to a clean 0.9 m and given a 0.06 m proud edge
- The rear yard is not modelled at all — the asset stops at the rear wall

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not
a straitjacket — adjust after the first aerial review render.

1. Main volume: extrude the 2.3 polygon from z=0 to z=8.55, `Toy_steel`.
2. Base band: inset the same polygon's street-facing edges and extrude z=0 to z=0.9 in
   `Toy_ink`, 0.06 m proud of the siding plane. Wrap only the north elevation and ~0.5 m
   around each front corner.
3. Cornice: a 0.45 m band along the north elevation only, from z=8.55 to **z=9.0**,
   0.15 m proud, `Toy_trim`. This sets the bounding-box top and must land exactly on 9.0.
4. Roof plane: flat cap at z=8.55, `Toy_roofd`.
5. Street windows: four openings, 1.0 × 1.7 m, two per storey, sills at z=1.5 and z=5.1,
   recessed 0.12 m, `Toy_glass`; 0.10 m proud `Toy_trim` sill and surround on each.
6. Gate: a 1.3 × 2.6 m slab at the east edge of the frontage in `Toy_sky`, set 0.10 m back
   from the siding plane, with four shallow vertical grooves. Behind it, a 0.6 m deep
   recess in `Toy_ink` so the passage reads as a hole rather than a painted panel.
7. Floor line: a 0.04 m shadow groove around the north elevation at z=4.3.
8. Rear elevation: one 1.0 × 2.1 m recessed door in `Toy_ink`, centred.
9. Roof incident (only if research confirms one): a 0.8 × 0.8 m bulkhead near the rear,
   rising to z=9.9, `Toy_steel`. **If it is confirmed, it becomes the tallest geometry and
   the target height changes to 9.9 m — flag that to the reviewer rather than clipping it.**
10. Bevel 0.10 m, 2 segments.

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_steel` | `#9aa0a6` | the lap siding — all four elevations |
| `Toy_ink` | `#3a3530` | stone base band, gate recess, rear door |
| `Toy_trim` | `#f3efe6` | cornice, window trim and sills |
| `Toy_glass` | `#2a4d73` | all windows |
| `Toy_sky` | `#6db3d9` | **the gate** |
| `Toy_roofd` | `#45454a` | the flat roof plane |
| `Toy_glass_Glow` | `#2a4d73` | the two lit upper windows at night |
| `Toy_sky_Glow` | `#6db3d9` | a thin light spill in the gate recess at night |

Note on the siding: the real colour is a desaturated blue-gray around `#a9b5bd`.
`Toy_steel` (`#9aa0a6`) is the nearest palette entry but reads slightly greener and more
metallic. The style bible's SF exception — painted residential rows keep their tinted
facades — sanctions a tinted deviation here, so if the aerial render says `Toy_steel` looks
dead, an off-palette `#a9b5bd` is a WARN not a FAIL. Justify whichever you pick in
`REPORT.md`. Do **not** reach for `Toy_sky` on the siding: it must stay unique to the gate,
which is the whole point of the gate.

**Night state (required).** Glow surfaces must be thin shells proud of the opaque glazing —
the app renders `_Glow` in a separate layer that is ~12% alpha by day, so a primary surface
must never be authored as glow. Hero glow: **two** lit windows on the upper storey of the
street facade — this is a three-unit house on a quiet residential oval, and a fully lit
facade would read as an office. Supporting accent: a thin warm spill in the gate recess,
which is also what tells the eye at night that the gate is a passage and not a panel. The
roof does not glow.

### 2.9 Top surface

A flat 24 m sliver, seen constantly from above and from almost no other angle. Its quality
comes from three things and nothing else: the crispness of the taper and the bend, the
cornice lift at the street end reading as a bright edge against the darker roof plane, and
whatever single roof incident the research confirms. Keep the roof value clearly darker
than the cornice and the siding so the outline reads from directly overhead. Do not add
invented rooftop clutter to make it "interesting" — the emptiness is accurate and the
neighbours' roofs supply the texture.

### 2.10 Scope

**In the GLB:** the single building — two-storey clapboard volume on the measured
footprint, stone base band, street facade openings, the blue gate and its recess, flat roof
with street-end cornice, rear door, and a roof bulkhead only if confirmed

**Not in the GLB:** 159 South Park, 171 South Park, the South Park oval, its lawn, paths or
trees, the street tree in front of the building, the street, the sidewalk, the rear yard,
fences, vehicles, people, plinths, cameras or lights

### 2.11 Triangle budget

Cap 6,000 — a background building, and the cap should bind hard. Suggested split: main
volume and taper ~800, base band ~400, cornice ~400, roof plane ~200, four window bays with
trim ~1,600, gate and recess ~700, rear door ~200, bevel overhead ~1,000. If the first
build lands above 6,000 the answer is fewer window subdivisions, not a raised cap.

### 2.12 Draft manifest entry

```json
{
  "id": "165-south-park",
  "file": "165-south-park.glb",
  "anchor": [
    -122.3943863,
    37.7808673
  ],
  "targetHeightM": 9.0,
  "cat": 1,
  "name": "165–167 South Park",
  "estimated": true,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

`dims` and `tris` are placeholders until the asset is built and validated.

### 2.13 Integration notes (for later, not this task)

- **New landmark.** Add a `pipeline/lib/landmarks.mjs` entry (`id: '165SouthPark'`) and
  re-bake the affected tiles, or the baked procedural building will intersect the GLB.

- **The manifest anchor and the registry `lon`/`lat` must differ, deliberately.** These are
  independent fields: `placeGeneric` in `app/src/assets.js` positions the GLB from the
  **manifest** `anchor` alone, while `pipeline/lib/landmarks.mjs` `lon`/`lat` is only the
  centre of the bake-time exclusion circle. On this site they cannot be the same point:

  | Field | Value | Why |
  |---|---|---|
  | manifest `anchor` | `-122.3943863, 37.7808673` | area centroid of the design footprint — where the building actually stands |
  | registry `lon`/`lat` | `-122.3943963, 37.7808764` | area centroid of the **DataSF LiDAR footprint** — the only point from which an exclusion radius exists that drops this building and nothing else |

  They are 1.34 m apart.

- **The exclusion radius is the hard part of this integration and the workable band is
  0.4 m wide.** `excluded()` in `pipeline/buildings.mjs` drops a footprint when its centroid
  **or any vertex** falls inside the circle. Measured from the registry point above:

  | Polygon | Triggers at | Source |
  |---|---|---|
  | this building | **0.00 m** (its own centroid) | DataSF |
  | this building | **1.09 m** (its centroid) | OSM `way/124889480`, as a proxy for Overture |
  | 159 South Park | **1.49 m** (nearest vertex) | DataSF |
  | 159 South Park | 2.33 m | OSM `way/124889491` |
  | 171 South Park | 3.36 m | DataSF |
  | 171 South Park | 4.15 m | OSM `way/124889458` |

  So the radius must be **greater than 1.09 m** (to also drop the Overture gap-fill version)
  and **less than 1.49 m** (to spare 159). **Use `exclude: 1.3`** — 0.21 m of margin on each
  side. Measured from the manifest anchor instead, no such radius exists at all: 159's
  footprint shares a party-wall vertex 0.50 m away, identical to this building's nearest
  vertex, which is exactly why the two fields differ.

- **Verify the Overture gap-fill explicitly.** `pipeline/buildings.mjs` only calls
  `markOccupied` for footprints that survive exclusion, so removing this building's DataSF
  footprint leaves its bbox unoccupied and the Overture pass may re-add a wrong-shaped
  building in its place. It may equally be blocked by the `occupiedFraction(bbox) > 0.25`
  test, since the Overture polygon here is oversized and overlaps 159 and 171 — whose
  footprints do survive. Which of the two happens cannot be determined without
  `pipeline/data/overture_buildings.geojsonseq`, so **re-measure against the real Overture
  polygon at integration time** and confirm with `pipeline/verify-rebake.mjs` that the
  affected cell loses exactly one building and no neighbour.

- **`exclude` is also the tree-clear and street-furniture radius.** At 1.3 m it clears
  neither, which is the right outcome here: the crape myrtle in front of the building is
  real and should stay, and South Park's furniture is placed along the street, outside the
  lot. Do **not** set `clearTrees: true`.

- `loadRadius`: the default formula gives `max(2500, 9.0 × 30) = 2500` m. Take the default.

- Camera preset: the building is only legible from the park side, so fly to it from the
  north — `camera: { distance: 160, yaw: 350, pitch: 26 }` as a starting point, tuned
  against the live scene.

- **This is the third non-monument building in the landmark manifest, and the case against
  doing more of them by hand is now strong.** 380 Brannan raised it and 1008 General Kennedy
  sharpened it; a row of near-identical narrow flats on a residential oval is precisely what
  `KIT-INTEGRATION-PROMPT.md` exists for. If the South Park rim is going to be built out,
  build the *rim house* as a kit piece with a tintable body and place a dozen of it, and
  keep the bespoke-landmark route for buildings that earn it. This asset is worth building
  as a one-off only because it is the pilot for the type.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Bounding-box top exactly 9.0 m (loader scale lands at 1.0) — or 9.9 m if a roof
      bulkhead is confirmed, flagged explicitly rather than clipped
- [ ] Dimensions plausible in meters and consistent with 2.1 (XY bbox ~18.8 × 21.8 m is expected)
- [ ] Frontage 6.4 m and rear width 4.27 m, not rounded toward a square plan
- [ ] The facade carries no bay window and no pediment
- [ ] Triangles at or under 6,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the two upper windows and the gate recess; glow shells proud of opaque glazing
- [ ] `Toy_sky` used on the gate and nowhere else
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (per-object signed volume for the union of solids; ray test residual <= 0.15%)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + contact sheet + night render regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

- **The crest height is the weakest number in the dossier and everything scales off it.**
  The 8.55 m roof deck is a real LiDAR measurement over 433 cells with a 0.65 m standard
  deviation, and for a flat roof that is trustworthy. The 9.0 m crest is not measured: it
  adds an *estimated* 0.45 m cornice. The LiDAR maximum of 9.90 m is a fourth number again,
  and it is unexplained — it could be the cornice (in which case the target should be 9.9 m,
  not 9.0), a chimney, a rear stair bulkhead, or a tree return from the street tree
  overhanging the roof edge. Resolving this from aerial imagery, and deciding whether the
  bulkhead in 2.7 step 9 exists, is the single highest-value verification before modelling.
- **No source isolates this building's built footprint.** The parcel is surveyed and
  trustworthy; the LiDAR footprint is offset 3.7 m streetward and 109 m² against an
  assessor-implied 124.5 m² per floor; OSM is unusable. The 24.0 m built depth in 2.3 is a
  reconciliation of the three, not a survey, and the rear wall's position is the part of it
  most likely to be wrong.
- **The window count and rhythm are inferred from a single Street View pano** partly
  obscured by a street tree, and are the weakest facade numbers here. Two openings per
  storey is a reasonable reading of a 6.4 m frontage but is not confirmed.
- **171 South Park looks like this building.** Same pale blue-gray lap siding, same two
  storeys, continuous roofline in every photograph. Its entry has a white classical
  surround with a triangular pediment; 165–167's does not — 165–167 has the blue gate.
  A modeller working from a wide-angle photo will very plausibly build 171's door onto this
  building. Do not.
- **The 1908 date and the unit count come from assessor data via a third-party aggregator**,
  not from a primary record. They are consistent with the building's type and with South
  Park's post-earthquake rebuilding, but no SF Planning survey record for this address was
  located. No architect is recorded, and none would be expected for a speculative flats
  building of this kind.
- **The present facade is 2014 work, not 1908 fabric.** The siding, the gate and the stone
  base all date from one $50k permit. The model should depict the building as it stands,
  which is what the app renders — but the plan's "1908 Edwardian flats" framing describes
  its form, not its surfaces.
- **The exclusion band is 0.4 m wide** (2.13). That is the narrowest in the registry and it
  rests on OSM standing in for Overture. If the real Overture polygon differs materially the
  band may vanish, in which case the fallback is a radius under 1.49 m that spares 159 and
  accepts that a procedural building may be re-added on top of the asset — which must be
  reported as a known FAIL, not hidden.
