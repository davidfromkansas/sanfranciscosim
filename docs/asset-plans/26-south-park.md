# 26–28 South Park (51 Taber Place) — SF-SIM asset plan

A 1907 two-storey-over-basement through-lot on the north rim of the South Park
oval: **6.7 m of frontage against 30.1 m of depth**, a 4.5:1 sliver wedged between
the Hotel Madrid at 22–24 and the loft at 44–46, running clean through the block
from South Park to Taber Place. It is the narrowest building yet planned for this
set — narrower even than the Gran Oriente Filipino at 104–106 — and it is the only
one whose *entire* architecture is a consequence of that shape: with both long
sides buried in party walls, every window it has is at one end or the other, and it
takes the rest of its daylight through skylights.

It is not a monument. It is a fire-damaged 1907 shed that was rebuilt in 1984 with
a garage and an open roof deck, ran as a hair salon through the 2000s, and has been
a plug-and-play office since 2014. What makes it worth modelling is the **massing**:
a near-black sliver, one clear storey lower than both its neighbours, with a
recessed timber entry and a railed open deck over its front bay. In the baked city
it is the step in the row.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/26-south-park/`. This document is the plan only: Part 1 is the runnable
task prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `26-south-park` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3937435, 37.7822367` (DataSF surveyed parcel 3775-049 area centroid, measured — see 2.13) |
| Target height | **9.05 m** to the parapet crest; roof deck 8.35 m (LiDAR-derived — and **not** the 13.59 m LiDAR maximum, see 2.15) |
| Footprint | **30.13 m (NW–SE, Taber Place to South Park) × 6.69 m (NE–SW), 201.5 m²** — an exact parallelogram, matching the Assessor's lot area to 0.1% |
| Triangle cap | 6,000 |
| Category | `3` (office) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 26–28 South Park GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of 26–28 South Park (51 Taber Place) in San
Francisco and deliver it as a downloadable, validated GLB.

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
7. `artifacts/106-south-park/` — **the closest reference implementation by shape**.
   Gran Oriente Filipino is the same problem: a sliver on this oval, 7.3 m of
   frontage against 29.7 m of depth, two blind party walls, skylights carrying the
   roof, and a roof plane that steps against both neighbours. Take its massing
   discipline, its skylight-as-roof-signature idea and its detail budget. Note the
   difference: that is a three-storey 1907 rooming house with a cornice and a
   documented history; this is a two-storey commercial sliver, one storey lower
   than everything around it, with no ornament at all.
8. `docs/asset-plans/26-south-park.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## What is already observed, and what is not

The **South Park (south-east) elevation was photographed** — Google Street View,
January 2025 — but a mature street tree stands directly in front of it and hides
most of the upper floor. The near-black colour, the recessed timber double-door
entry with its wall lantern, the white-framed ground-floor windows and the
**railed open deck over the front bay** are observation. The upper floor behind the
deck is only partly seen.

The **Taber Place (north-west) rear** was probably photographed — a dark-brown
lap-sided two-storey face with large white-framed multi-pane industrial windows on
both floors, a glazed garage door and a recessed personnel door — but the
attribution to *this* building could not be confirmed from the pano metadata, only
inferred from position and colour. Treat 2.4's rear description as **inferred** and
settle it.

Three things are genuinely open and you must settle them (2.15):

1. **The 13.59 m LiDAR maximum is almost certainly not this building.** It sits
   3.5σ above the 8.35 m median, and it matches 44–46 South Park's own 13.52 m
   median to within 7 cm — on a 7.65 m-wide raster footprint whose edges are
   dilated into both taller party-wall neighbours. This plan takes the median as
   the deck and builds a **9.05 m parapet**, not a 13.59 m crest. Verify the
   reading; do not inherit the maximum.
2. **How the front bay and the open deck actually work.** The 1984 permit is
   "repair fire damage & broken window / new garage with open deck" and the Street
   View shows a railing at second-floor level across the front. This plan reads it
   as a top floor set back ~3 m from the South Park frontage, leaving a terrace
   behind a rail over a single-storey front bay. Confirm the setback depth.
3. **Which end has the garage.** The 2019 permit adds "man doors to garage on 1st
   floor"; the leasing listing offers "2 car garage parking"; the Assessor's
   address of record is 51 **Taber Place**, the service alley. The garage is
   therefore most likely at the Taber Place end, and the South Park end is the
   office front — but the front's wide low white-framed windows could equally be a
   converted garage opening.

## Must capture

- The **sliver proportion**: 6.7 m wide, 30.1 m deep, running clean through the
  block. Everything else about this building follows from it, and if the model
  reads as anything other than a slot, it is wrong.
- The **step**: two storeys where 22–28's neighbours are three and four. This roof
  sits ~4.0 m below the Hotel Madrid's and ~5.2 m below 44–46's, so in the baked
  city it is a notch in the row — model the flanks as finished walls, because
  several metres of *both* neighbours' party walls stand exposed above this roof
  and this building's own flanks are what the camera sees below them.
- The **near-black street face** with its recessed timber double-door entry, wall
  lantern and paired white-framed windows.
- The **open roof deck behind a metal railing** over the front bay — the one piece
  of three-dimensional incident on the whole building, and clearly visible from the
  app's aerial camera.
- **Two sides of windows and nothing else**: glazed at South Park, glazed at Taber
  Place, blind for 30 m in between. Do not put a window on a party wall.
- **Skylights**: the leasing listing sells them, and on a 30 m slot with two blind
  sides they are the only daylight in the middle. They are also this roof's
  signature from above.

## Research 26–28 South Park independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- The two end elevations: the 6.7 m South Park front (south-east) and the 6.7 m
  Taber Place rear (north-west). Both long sides are party walls.
- The roof — the skylight layout, the deck, and whether anything else stands on it
- Ground-level views from South Park **taken outside leaf season or from an angle
  that clears the street tree**; the January 2025 pano does not
- Day and night appearance
- Interior imagery if it settles the section: a Google Business photosphere at this
  address (captured January 2012, when the building was the salon "Kim Pfabe's
  Sugarcane") shows a **double-height space with a mezzanine, a black stair and a
  tall multi-pane end window**, which is direct evidence for the high ceilings and
  the 4.2 m storey height this plan assumes

Prefer architect/engineer publications, owner or institutional material,
planning and permitting documents, architectural press, geolocated photography,
and aerial/satellite imagery. Never rely on a single photograph, a single
AI-generated image, or a single unsourced 3D model. Separate verified facts from
visual inference; if sources disagree, document the disagreement and decide.

**One source conflict is already known — re-check it, do not silently
re-inherit the wrong value:** the storey count is **2** on the Assessor's roll,
in every permit from 1984 to 2019, and on Compass; but the leasing agent describes
"approximately 6,000 square feet across three floors". Both are right — the third
floor is the **basement**, which the permits handle explicitly ("ti for (e) office
space on the 1st fl & basement", "removal of stair partition in basement").
Two storeys above grade, three occupied levels: 180 m² × 3 = 540 m² = 5,813 sq ft,
which is the 6,000 sq ft figure. Model two storeys.

## Create a reference dossier

Write `artifacts/26-south-park/REFERENCE.md` containing: source links and what each
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

This is a **background building** in the style bible's detail budget (§21) — one
tier below the secondary buildings around it, and deliberately so. Its job in the
scene is to be the low, dark, quiet gap between two louder neighbours. Clear
massing, one strong move (the deck), one designed roof, and no ornament. Resist the
temptation to make it more interesting than it is; a 6.7 m frontage that competes
with the Hotel Madrid next door is a worse model, not a better one.

The finished asset must be immediately recognizable as 26–28 South Park, consistent
with the real building from all four sides and above, architecturally credible, and
a premium handcrafted miniature — not photorealistic, not voxel art, not generic
low-poly, and never accurate in one view while invented in the others.

## Scope of the exported asset

Export the single block: body, the South Park elevation with its recessed entry and
windows, the Taber Place rear with its garage and windows, both blind party walls,
the parapet, the flat roof, the open deck and its railing, the skylights and the
mechanical plant.

Do not include unrelated surrounding city geometry: South Park itself, its trees or
lawn, Taber Place, the sidewalk, the street tree in front of the entry, the utility
poles and overhead wires, the neighbours at 22–24 or 44–46 South Park, parked cars,
people, plinths, cameras or lights. Temporary context may appear in review renders
but must not leak into the GLB.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary
`.glb`; real-world meters; origin at base center; minimum geometry Z ~ 0;
applied transforms; no negative scales; outward normals; no duplicate or foreign
geometry; no image textures; no transparency; flat-color materials named `Toy_*`
from the project palette; `_Glow` suffix only on surfaces that glow at night; no
`Toy_body`; no cameras, lights, animations, armatures or constraints; no external
dependencies; at most 6,000 triangles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model
drops into the city at its real-world heading — the loader applies no rotation
(`placeGeneric` in `app/src/assets.js` only scales and positions). The South Park
entrance faces **south-east, bearing 135.2°**; the long axis runs 315.2°/135.2°
(NW–SE), so build directly on the measured parallelogram in 2.3 rather than
modelling an axis-aligned box and rotating it. The contract's "front faces −Y"
cannot be honoured literally here; real-world orientation wins (AGENTS rule 5) and
the deviation goes in `REPORT.md`.

**Height normalization:** the tallest geometry in the export (the parapet crest)
must land at exactly **9.05 m** so the loader's `targetHeightM / measuredHeight`
scale is 1.0. Nothing — not the deck railing, not a skylight, not a vent — may
stand above it.

## Reproducible Blender workflow

Blender 5.2 LTS. Headless: `blender -b --python script.py -- args`.

Keep `artifacts/26-south-park/build_26_south_park.py` (deterministic build script),
`artifacts/26-south-park/26-south-park.blend`, and
`artifacts/26-south-park/26-south-park.glb`. The script must rebuild the model reliably
enough for future revision. Do not modify or rename an unrelated existing GLB to satisfy
the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`26-south-park-top.png`, `26-south-park-north.png`, `26-south-park-east.png`,
`26-south-park-south.png`, `26-south-park-west.png`, plus
`26-south-park-contact-sheet.png`, at least one high three-quarter aerial beauty render
`26-south-park-aerial.png`, and a night render `26-south-park-aerial-night.png`.

The four elevations must share scale, framing, lighting, exposure and
projection; use orthographic or long-lens cameras; label directions from the
researched orientation; the top view must clearly show the full 30.1 × 6.7 m
roof — its deck, railing, skylights and plant; the aerial view uses the style
bible's camera assumptions (30–50 degrees down, long lens). Simple tabletop
lighting, neutral warm background, minimal depth of field, and every image must
depict the same exported model.

Because the building is rotated 45° from the world axes, the four compass renders will
each show two faces at 45°. That is correct and expected — do not rotate the model to make
the elevations square on.

**Night renders: drive `_Glow` from Base Color, not from the imported emission.**
See `docs/asset-plans/README.md` — copy `Base Color` into `Emission Color` at
strength 1.0, or every glow surface renders as a white slab.

## Validate the exported GLB

Re-import `26-south-park.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture
count, camera count, light count, animation count, applied-transform status,
negative-scale status, normal-orientation status, unexpected geometry, and
per-material contract compliance. Render at least one review image from the
re-imported asset. Write `artifacts/26-south-park/validation.json` and
`artifacts/26-south-park/REPORT.md`.

Note that the axis-aligned XY bounding box will be roughly **26.0 × 26.0 m** even
though the building is 30.1 × 6.7 m — that is the expected consequence of a 315°
real-world heading, not a scale error.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "26-south-park",
  "file": "26-south-park.glb",
  "anchor": [
    -122.3937435,
    37.7822367
  ],
  "targetHeightM": 9.05,
  "cat": 3,
  "name": "26–28 South Park",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a separate, explicitly requested job — run `docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in `docs/asset-plans/26-south-park.md`.
````

---

## Part 2 — Research and design dossier

Compiled 16 August 2026 from the sources in 2.2. Values marked *inferred* are visual or
derived estimates, not published figures — the executing agent must re-verify
anything it relies on.

**A note on the evidence quality of this dossier.** The **geometry is the strongest
in this set**: the surveyed parcel is an exact four-vertex parallelogram whose
polygon area (201.5 m²) matches the Assessor's `lot_area` (2,167.22 sq ft =
201.3 m²) to 0.1%, so there is no ambiguity at all about shape, size or heading.
The **history is the weakest**: no architect, no builder, no historic-resource
finding, and nothing published beyond a permit trail and a leasing listing. The
**height** is a judgement call rather than a reading, and 2.15 explains why the
LiDAR maximum has to be thrown away.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Built | **1907** | SF Assessor secured roll, `year_property_built = 1907`; iondocs and Compass both repeat it |
| Storeys | **2** above grade, plus a basement — three occupied levels | Assessor `number_of_stories = 2.0`; every permit 1984–2019 records 2; Compass "Stories 2"; The Hawthorne Group "approximately 6,000 square feet across three floors"; permits 201710110892 and 201901049689 name the basement explicitly |
| Use | **Commercial office** since 2014; a hair salon 2001–2014; "1 family dwelling" on the 1984 and 2009 permits | Assessor `use_code = COMO`, `property_class_code = O`; permit 201410280096 ("change of use from a salon to a office space on first floor") |
| Fire and rebuild | **1984: repair fire damage & broken window / new garage with open deck**, $70,000 | permit 8413539 — the single most consequential permit on this building |
| Salon fit-out | 2001–02: shampoo-sink counter, stairway handrails and visual striping | permits 200112185518, 200201086464 |
| Reroofing | 2009, $12,992 | permit 200909176992 |
| Office fit-outs | 2017 (1st floor + basement, $30 k); 2019 (partitions removed in basement, 1st and 2nd; **man doors added to the garage on the 1st floor**, $12 k) | permits 201710110892, 201901049689 |
| Structure | a braced frame at the second floor replaced by a **moment frame**, 2019 | permit 201904047119 — implies a wide clear opening wanted at that level |
| Amenities (as leased) | fibre, 2 private restrooms, conference room, reception, open area for 14+ workstations, **bright natural lighting with two sides of windows, high ceilings, skylights, 2-car garage parking, 6 wall-mounted bike racks** | The Hawthorne Group listing, "28 South Park Street" — status **Leased** |
| Block / lot | 3775 / 049, APN 3775-049 | DataSF parcels, SF Assessor, iondocs |
| Addresses | 26 and 28 South Park; Assessor's address of record is **51 Taber Place** | DataSF EAS addresses; Assessor `property_location = 0000 0051 TABER PL` |
| Lot area | **2,167.22 sq ft (201.3 m²)** | SF Assessor `lot_area`; the parcel polygon measures 201.5 m² — a 0.1% match |
| Building area | 6,000 sq ft (557 m²) over three levels | SF Assessor `property_area`; 180 m² × 3 = 540 m², consistent |
| Lot depth | 98.51 ft (30.03 m) | SF Assessor `lot_depth` — matches the measured 30.13 m |
| Footprint (parcel, survey) | **30.13 m × 6.69 m, 201.5 m², an exact parallelogram** at bearing 315.18°/135.18° | DataSF parcels `acdm-wktn`, blklot 3775049, reprojected — **measured**; OBB area equals shoelace area to 4 significant figures, i.e. the lot is a true rectangle |
| Footprint (LiDAR, building) | 31.19 × 7.65 m bounding rectangle, **180.0 m² actual**, 33 vertices | DataSF `ynuv-fyni` SF3775049 — **measured**, but noisy: a raster trace of a 7 m sliver, dilated at both party walls |
| Roof deck | **8.35 m** (median), 8.36 m (majority), 8.95 m (mean) | DataSF LiDAR `hgt_mediancm/majoritycm/meancm` — **measured**; median and majority agree to 1 cm |
| Height std dev | 1.48 m | DataSF LiDAR `hgt_stdcm = 148` — high for a flat roof, and the tell (2.15) |
| LiDAR maximum | 13.59 m | DataSF LiDAR `hgt_maxcm = 1359` — **rejected as party-wall contamination**, see 2.15 |
| LiDAR minimum | 5.89 m | DataSF LiDAR `hgt_mincm = 589` — the front bay, or an edge artifact |
| Ground elevation | 11.96 m (NAVD88) | DataSF LiDAR `gnd_min_m` — app terrain handles this, not the asset |
| Zoning | **SPD** (South Park District) | DataSF parcels; Assessor |
| Neighbourhood | Financial District/South Beach | DataSF parcels |
| Neighbour heights | 22–24 South Park (SF3775048) **12.39 m** median, 14.22 m max; 44–46 South Park (SF3775217) **13.52 m** median, 16.15 m max | DataSF LiDAR — **both party-wall neighbours are 4–5 m taller than this building** |
| Last sale | 4 October 2017 | SF Assessor `current_sales_date` |
| OSM | **not traced** — no OSM building carries `addr:housenumber=26` or `28` on South Park | Overpass, `way["addr:street"="South Park"]["building"]` over the block: the sequence runs 22;24 then 41;43, skipping this lot |

### 2.2 Sources

- `https://data.sfgov.org/resource/acdm-wktn` (DataSF Parcels) — parcel 3775-049, 26–28 SOUTH PARK, zoning SPD — the surveyed footprint used as this plan's geometry, and an exact parallelogram
- `https://data.sfgov.org/resource/ynuv-fyni` (DataSF Building Footprints, LiDAR-derived, **2010 survey**) — footprint SF3775049, heights 13.59 / 8.35 / 5.89 m, std 1.48 m
- `https://data.sfgov.org/resource/wv5m-vpq2` (SF Assessor secured roll) — 1907, 2 storeys, 6,000 sq ft over a 2,167.22 sq ft lot, Commercial Office, address of record 51 Taber Place, sold Oct 2017
- `https://data.sfgov.org/resource/i98e-djp9` (SF Building Permits) — 12 permits on block 3775 lot 049: the 1984 fire repair and garage-with-open-deck, the 2001–02 salon fit-out, the 2009 reroof, the 2014 change of use, the 2017 and 2019 office TIs, the 2019 moment frame
- `https://data.sfgov.org/resource/ramy-di5m` (DataSF addresses) — 26 and 28 South Park, block 3775 lot 049
- https://www.thgcommercial.com/project/28-south-park-street/ — The Hawthorne Group leasing listing: ~6,000 sq ft over three floors, two sides of windows, high ceilings, skylights, 2-car garage, 6 bike racks. **Leased.**
- https://www.compass.com/homedetails/51-Taber-Pl-San-Francisco-CA-94107/1P6DCT_pid/ — 51 Taber Place, 1907, 2 stories, ~6,000 sq ft, 0.05-acre lot
- https://knowthis.place/san-francisco/east-cut/south-park/26/ — an independent transcription of the same permit history, useful as a cross-check
- https://www.iondocs.com/properties/28-south-park-san-francisco-ca-94107/qMl3qdUDEJZp — APN 3775049, 1907, 6,000 sq ft, Commercial Office, 21 permits
- Google Street View, **January 2025**, panorama near `37.78205,-122.39356` (headings 300–305°) — the South Park elevation, **observed but tree-obscured above the ground floor**
- Google Street View business photosphere, **January 2012**, "Kim Pfabe's Sugarcane" at this address — the interior: a double-height room with a mezzanine, a black stair and a tall multi-pane end window
- Google Street View, January 2025, panorama near `37.78243,-122.39400` (heading 140°) — a dark-brown lap-sided two-storey face with large white-framed grid windows, a glazed garage door and a recessed personnel door, **probably this building's Taber Place rear but not confirmed** (2.15)
- Google Maps satellite (Vexcel Imaging 2026, near-nadir, `37.7822367,-122.3937435` at z21) — a plain pale-tan flat roof with dark incident toward the South Park end, **observed**
- Overpass API, `way["addr:street"="South Park"]["building"]` over the block — establishes that OSM has **no** trace of this building

### 2.3 Orientation and placement

The building is a through-lot on the north rim of the South Park oval, running from
South Park at the south-east to Taber Place at the north-west. Both long sides are
party walls: the Hotel Madrid at 22–24 to the north-east, 44–46 South Park to the
south-west. The oval's rim runs at bearing 45.2°/225.2°, so the lot runs
315.2°/135.2°.

Rectangle corners in Blender coordinates (metres, `+X` east, `+Y` north), centred on
the anchor `-122.3937435, 37.7822367`, from the surveyed parcel — these are the four
measured vertices, not an idealisation:

```
(  12.99,  -8.33)   East corner    (South Park x the 22-24 party wall)
(   8.24, -13.04)   South corner   (South Park x the 44-46 party wall)
( -12.99,   8.32)   West corner    (Taber Place x the 44-46 party wall)
(  -8.25,  13.04)   North corner   (Taber Place x the 22-24 party wall)
```

in ring order: `E → S → W → N`.

Edges, with outward normals:

| Edge | Length | Faces | Elevation |
|---|---|---|---|
| E corner → S corner | 6.69 m | SE 135.2° | **South Park front** |
| S corner → W corner | 30.13 m | SW 225.2° | **party wall** with 44–46 (blind) |
| W corner → N corner | 6.69 m | NW 315.2° | **Taber Place rear** |
| N corner → E corner | 30.13 m | NE 45.2° | **party wall** with 22–24 (blind) |

Unlike its neighbour at 22–24, **this frontage is straight**. The oval's curvature
over a 6.7 m chord is a 0.19 m sagitta, the survey does not record it, and it is
below the bevel radius — build the front flat.

Because of the 315° heading the axis-aligned bounding box is ~26.0 × 26.0 m. That
is correct.

### 2.4 What each side shows

**South-east (South Park) — observed, Jan 2025, upper floor tree-obscured.** A
6.7 m face, **near-black to very dark charcoal**, flat and unornamented. The ground
floor carries, from the south-west: a pair of white-framed windows sitting low and
wide in the dark wall, then a **recessed entry bay** with a dark timber-panelled
double door beside a narrower glazed door, a small **wall lantern** to its right,
and a notice board on the return. A shallow step up to the entry. There is no
storefront band, no belt course and no base plinth — the wall runs to the pavement
in one colour.

Above, at second-floor level, a **metal railing runs across the front**, with the
wall behind it set back. Warm point lights are visible under the setback. Read
together with the 1984 permit — "new garage with open deck" — this is a top floor
held back from the frontage, leaving an open terrace over a single-storey front
bay. Behind the tree, a large white-framed window with a horizontal transom serves
the second floor.

**North-west (Taber Place) — *inferred*, from a January 2025 pano whose attribution
was not confirmed.** A two-storey face in dark-brown horizontal lap siding, with
**large white-framed multi-pane industrial windows filling most of both floors**, a
**glazed garage door** at ground level and a recessed personnel door beside it. If
this is the right building it settles both the garage question and the "two sides of
windows" claim in one image. Marked *inferred* — see 2.15.

**North-east and south-west — party walls.** Blind for the full 30.1 m. Both
neighbours are 4–5 m taller (22–24 at 12.39 m, 44–46 at 13.52 m), so this
building's flanks are only seen as the lower part of a canyon — but they *are*
seen, from directly above and from the three-quarter aerial, and they must be
finished walls in the body colour, not raw extrusion sides.

**Top — observed, Vexcel 2026 near-nadir.** A plain **pale-tan flat roof** at
8.35 m, essentially empty over the Taber Place two-thirds, with darker incident
toward the South Park end — the open deck and, most likely, the skylights the
leasing listing sells. Nothing tall stands on it: no penthouse, no plant tower,
nothing that could produce the 13.59 m LiDAR maximum (2.15). It is the lowest roof
on this stretch of the rim and is overlooked by everything around it.

### 2.5 Recognition cues (ranked)

1. **The slot.** 6.7 m against 30.1 m, running clean through the block. At the
   app's camera this reads before anything else, and it is the whole building.
2. **The step.** Two storeys between a three-storey hotel and a four-storey loft —
   a 4–5 m notch in an otherwise continuous roofline. In the baked city this is
   free, because the neighbours are really there, and it is the reason this asset
   is worth having at all.
3. **The near-black front**, which is unusual on this rim: the Madrid is sage
   green, 44–46 is pale, 10 South Park is cream.
4. **The railed open deck** over the front bay — the only three-dimensional move.
5. The recessed timber double-door entry with its wall lantern.

### 2.6 Miniature translation

**Preserve**

- The 30.13 × 6.69 m parallelogram and the real 315.2°/135.2° heading, exactly
- Two storeys, deck at 8.35 m — the step is the point
- Two blind party walls, finished in the body colour, carried to the parapet
- The setback top floor and its railed terrace at the South Park end
- Glazing at both ends only
- Skylights on the roof

**Simplify / exaggerate**

- The front's pair of white-framed windows becomes **one recessed glazed opening**
  with a single frame band; the recessed entry becomes one 1.6 m-deep notch with a
  dark door panel
- The Taber Place multi-pane industrial windows become **one glazed panel per
  floor**, full width less a margin, with a single frame band — no mullion grid.
  On a 6.7 m face at 60 m the grid is noise; the *size* of the opening is the cue.
- The garage door becomes one recessed panel in a lighter value, no panel lines
- The deck railing becomes a **solid 1.0 m parapet-rail slab**, not balusters —
  and it must stay below 9.05 m
- Skylights become three raised boxes on a common line, `Toy_glass` on a
  `Toy_steel` kerb
- Lap siding on the rear becomes flat colour with two or three shallow horizontal
  grooves per storey
- The wall lantern, the notice board, the bike racks and the camera are all below
  the threshold — omit them

**One deliberate exaggeration is licensed:** push the **darkness** of the body a
little further than the photograph, toward `Toy_ink`. The real building is a very
dark charcoal; at the app's aerial camera, under a bright key, a literal mid-charcoal
would wash out to the same value as the Madrid's storefront and the step would stop
reading. The contrast against its two pale neighbours is this building's job.

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not
a straitjacket — adjust after the first aerial review render.

1. Main body: extrude the 2.3 parallelogram from z=0 to the roof deck z=8.35,
   `Toy_ink`. This is the whole building; everything below modifies it.
2. Front bay: cut the top floor back **3.0 m** from the South Park edge, leaving the
   front bay at one storey — its roof (the open deck) at z=4.30, `Toy_stone`.
3. Deck parapet-rail: a 1.0 m slab from z=4.30 to z=5.30 around the three open
   sides of the deck, `Toy_steel`, 0.14 m thick.
4. South Park elevation, ground floor: one recessed glazed opening 2.6 m wide from
   z=0.9 to z=3.2 (`Toy_glass` behind a 0.12 m `Toy_trim` frame), and a 1.8 m-wide,
   1.6 m-deep entry notch beside it with a `Toy_roofd` door panel and a 0.25 m
   `Toy_trim` head band.
5. South Park elevation, second floor (3.0 m behind the frontage): one glazed
   opening 4.2 m wide from z=5.1 to z=7.6, `Toy_glass` with a 0.14 m `Toy_trim`
   frame — this is what the deck looks into.
6. Taber Place elevation: two glazed openings, 5.0 m wide, z=4.9–7.9 (upper) and
   z=1.5–4.0 (lower), `Toy_glass` with 0.14 m `Toy_trim` frames; a 3.0 × 2.6 m
   recessed garage panel in `Toy_steel` at ground level beside them and a 1.0 m
   `Toy_roofd` personnel door.
7. Rear siding grooves: three shallow 0.06 m grooves per storey across the Taber
   Place face only, `Toy_roofd`.
8. Party walls: plain `Toy_ink`, no openings, carried to the parapet.
9. Parapet: `Toy_ink` from z=8.35 to **z=9.05** around all four sides. This is the
   crest and must land at exactly 9.05 m.
10. Roof deck: a thin slab z=8.35 to z=8.47 inside the parapet, `Toy_stone`.
11. Skylights: three 2.0 × 1.2 × 0.35 m raised boxes on the centre line, evenly
    spaced over the Taber Place two-thirds, `Toy_glass` on a `Toy_steel` kerb.
12. Mechanical: two `Toy_steel` boxes (~1.1 × 0.8 × 0.55 m) at the Taber Place end.
13. Bevel 0.12 m, 2 segments.

Nothing in steps 10–12 may exceed z=9.05.

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_ink` | `3a3530` | the body — all four elevations, both party walls, the parapet |
| `Toy_roofd` | `45454a` | the entry door panel, the personnel door, the rear siding grooves |
| `Toy_steel` | `9aa0a6` | the deck parapet-rail, the garage panel, skylight kerbs, mechanical plant |
| `Toy_trim` | `f3efe6` | every window frame band and the entry head band |
| `Toy_glass` | `2a4d73` | all glazing and the skylight tops |
| `Toy_stone` | `d9d2c2` | the flat roof deck and the open deck floor |
| `Toy_glassl_Glow` | `6f95b8` | two lit windows at night |
| `Toy_trim_Glow` | `f3efe6` | a thin warm spill in the entry notch at night |

One note on colour: **the palette has no true black and this building should not
have one either.** `Toy_ink` at `3a3530` is a warm near-black and is the right
answer; do not reach for a custom darker value. The `Toy_stone` roof and the
`Toy_steel` rail are what keep the mass from reading as a hole punched in the row.

**Night state (required).** Glow surfaces must be thin shells proud of the opaque
glazing — the app renders `_Glow` in a separate layer that is ~12% alpha by day,
so a primary surface must never be authored as glow, and a closed shell counts
twice (keep every glow surface a single open face). This building gets the
**quietest night state in the South Park set**, on purpose: it is a small leased
office on a residential oval, and at night it should be the dark gap. Hero glow:
a thin warm spill (`Toy_trim_Glow`) inside the entry notch — which is also what
tells the eye at night that the notch is a door. Supporting accent: **two** lit
windows, the second-floor South Park opening and the upper Taber Place opening,
in `Toy_glassl_Glow`. The ground floor, the garage, the party walls, the deck, the
skylights and the roof stay dark.

### 2.9 Top surface

30.1 × 6.7 m of flat roof at 8.35 m — the lowest on this stretch of the rim, and
therefore the one the camera looks *down into* rather than across. Three things
carry it:

1. **The open deck at the South Park end**, a 6.7 × 3.0 m floor 4 m below the main
   roof plane behind a `Toy_steel` rail. A hole in the roof plane is worth more
   than any number of objects sitting on it, and this one is documented.
2. **The three skylights** on the centre line — the only daylight the middle of a
   30 m slot with two blind sides can get, and the reason to believe they are
   really there. Same idea as the Gran Oriente's roof
   (`docs/asset-plans/106-south-park.md` §2.9), at a smaller count.
3. **The two canyon walls.** This roof's edges are not silhouette; they are the
   bottom of a 4–5 m slot between the Hotel Madrid and 44–46. Keep the deck a clear
   value *above* the body colour so the plane reads as a floor down there, not as
   shadow.

Resist adding plant. The aerial shows an essentially empty roof and an empty roof
next to two busy ones is a compositional asset, not a gap to fill.

### 2.10 Scope

**In the GLB:** the single block — body, the South Park elevation with its recessed
entry and windows, the setback top floor, the open deck and its rail, the Taber
Place rear with its garage and windows, both blind party walls, the parapet, the
flat roof, the skylights and the mechanical plant

**Not in the GLB:** South Park, its trees or lawn, Taber Place, the sidewalk, the
street tree standing directly in front of the entry, the utility pole and overhead
wires, the neighbours at 22–24 or 44–46 South Park, vehicles, people, plinths,
cameras or lights

**Deliberately excluded: the entry lantern, the notice board, the bike racks and the
security camera.** All four are real and all four are under a pixel at the app's
camera. Record the omission in `REPORT.md`.

### 2.11 Triangle budget

Cap 6,000 — a background building, and the cap should not bind; aim for 3,000–4,000.
Suggested split: body, party walls and parapet ~0.9k; the front-bay setback and the
open deck ~0.4k; the deck parapet-rail ~0.5k; the South Park openings and entry
notch ~0.6k; the Taber Place openings, garage and door ~0.7k; the rear grooves
~0.3k; roof deck ~0.2k; three skylights ~0.4k; mechanical ~0.3k.

The one place this budget can run away is the **rear industrial windows**. The real
ones are a fine multi-pane grid across nearly the whole face; modelled honestly they
are 200-plus quads on a 6.7 m elevation that is only ever seen from an alley the
camera does not fly down. One glazed panel with one frame band, per floor.

### 2.12 Draft manifest entry

```json
{
  "id": "26-south-park",
  "file": "26-south-park.glb",
  "anchor": [
    -122.3937435,
    37.7822367
  ],
  "targetHeightM": 9.05,
  "cat": 3,
  "name": "26–28 South Park",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

`dims` and `tris` are placeholders until the asset is built and validated.

### 2.13 Integration notes (for later, not this task)

- **New landmark.** Add a `pipeline/lib/landmarks.mjs` entry (`lon: -122.3937435`,
  `lat: 37.7822367`, `height: 9.05`, `exclude: 3.4`) and re-bake the affected tiles,
  or the baked procedural building on this exact footprint will intersect the GLB.
  Note that the procedural mass here is **taller** than the asset (the bake reads
  the DataSF LiDAR record, whose maximum is 13.59 m), so shipping the manifest entry
  without the exclusion produces a landmark that is completely invisible — not a
  cosmetic defect, a nothing-to-look-at defect.
- **This is the tightest exclusion band in the South Park set so far.** It was
  measured against both bake inputs — `pipeline/data/buildings_datasf.geojson` and
  `pipeline/data/overture_buildings.geojsonseq` — applying `excluded()`'s real test
  (centroid **or** any ring vertex inside the radius). From the anchor above:

  | ring | trigger distance |
  |---|---|
  | **own** DataSF `SF3775049` (via its centroid; nearest vertex 1.47 m) | **0.41 m** |
  | **own** Overture `5bdb7723-…-b2c6-` (via its nearest vertex) | **2.21 m** — the floor |
  | **44–46 South Park**, DataSF `SF3775217` (nearest vertex) | **4.62 m** — the ceiling |
  | 22–24 South Park, Overture `638a2a32-…-b99c-` | 5.77 m |
  | 22–24 South Park, DataSF `SF3775048` | 7.28 m |
  | an Overture ring at `…-8374-` | 8.85 m |

  The safe window is **(2.21, 4.62) m** — 2.41 m wide. `exclude: 3.4` sits at its
  midpoint with 1.19 m of margin below and 1.22 m above. **The floor is the Overture
  ring, not the DataSF one**, exactly as at 104–106 South Park: `addBuilding()`
  returns null on exclusion so `markOccupied()` never runs, and a radius under
  2.21 m lets the Overture gap-fill re-add this building on top of the asset.
- **Expect the re-bake to drop exactly two rings, both this building's** — DataSF
  `SF3775049` and its Overture twin. Do not count drops, check *which*: every
  dropped ring's centroid must sit within a couple of metres of the anchor. If
  `SF3775217` disappears, 44–46 South Park has been demolished by this entry and the
  radius must come down.
- **44–46 South Park is itself in flight** on `pipeline/46-south-park`. It is the
  binding constraint here and the margin above it is 1.22 m, which is thin. If that
  branch lands first, its own exclusion will already have removed `SF3775217` and
  this check becomes untestable by inspection — so **verify the drop list against
  `origin/main`'s registry, not against whatever is in the tree**, and re-check
  after any merge.
- **22–24 South Park is being built in the same batch**
  (`docs/asset-plans/22-south-park.md`, `exclude: 4.5`). The two radii do not reach
  each other's footprints: 3.4 m here stops 2.4 m short of the Madrid's Overture
  ring, and 4.5 m there stops 2.4 m short of this building's DataSF ring. Whichever
  lands first, the other still bakes correctly.
- `loadRadius`: the skill's default formula gives `max(2500, 9.05 × 30) = 2500` m.
  Take the default.
- **Verify with `pipeline/audit.mjs` check 1.6 after the re-bake** and confirm
  visually that 22–24 and 44–46 South Park are both still standing before
  committing.
- **This building is a strong argument for the kit route rather than the manifest
  route.** It is a 6.7 m unornamented two-storey box; the case for it is entirely
  contextual — it is the notch between two modelled neighbours. If
  `KIT-INTEGRATION-PROMPT.md`'s instancing ever grows a "narrow dark infill" piece,
  this is the first entry that should move.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Bounding-box top exactly 9.05 m — the parapet, and **not** the deck rail, a skylight or a vent (loader scale lands at 1.0)
- [ ] Dimensions plausible in meters and consistent with 2.1 (XY bbox ~26.0 × 26.0 m is expected)
- [ ] The footprint is still 30.1 × 6.7 m in plan — measure it, do not eyeball it
- [ ] The roof deck sits at 8.35 m and the open deck floor at 4.30 m
- [ ] Triangles at or under 6,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the two lit windows and the entry notch; every glow surface a single open face proud of the opaque glazing
- [ ] Both party walls have no openings and are finished walls, not raw extrusion sides
- [ ] No lantern, notice board, bike racks or camera in the export
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (per-object signed volume for the union of solids; ray test residual ≤ 0.15%)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + contact sheet + night render regenerated from the final export
- [ ] The 2.15 height question answered in `REPORT.md`, with the evidence that answered it
- [ ] The Taber Place elevation either observed and confirmed, or, if it stayed inferred, said so plainly in `REPORT.md`

### 2.15 Open questions and risks

- **The 13.59 m LiDAR maximum must be thrown away, and this is the plan's single
  most consequential judgement.** It sits 5.24 m above the 8.35 m median on a
  footprint whose height standard deviation is 1.48 m — a 3.5σ outlier. Three
  independent arguments say it is not this building:
  1. **It matches the neighbour.** 44–46 South Park's LiDAR *median* is 13.52 m.
     The maximum here is 13.59 m. A 7 cm agreement between a sliver's maximum and
     its party-wall neighbour's roof plane is not a coincidence — it is
     `docs/asset-plans/README.md`'s Earl Warren case ("treat a single-cell
     `hgt_max` on a party wall as unusable") on a 7.65 m-wide raster footprint whose
     50 cm cells are dilated into *both* taller neighbours.
  2. **The distribution is right-skewed.** Mean 8.95 m against median 8.35 m and
     majority 8.36 m: the mean is dragged 0.6 m above the median by a minority of
     high cells, which is the signature of contamination rather than of a real
     raised structure. Median and majority agreeing to 1 cm says the true roof
     plane is very well determined.
  3. **The aerial shows nothing there.** The 2026 near-nadir imagery of this roof
     is a plain pale plane. There is no penthouse, no plant tower and no second
     storey-and-a-half that could put a real reading at 13.59 m.

  This plan therefore takes **8.35 m as the roof deck and 9.05 m as the parapet
  crest**, i.e. a conventional 0.70 m parapet on a measured deck. Two storeys at
  ~4.2 m each is consistent with 8.35 m, with the "high ceilings" the leasing
  listing advertises, and with the double-height interior in the 2012 photosphere.
  **If this is wrong the model is badly wrong** — a 9 m building where a 13.5 m one
  belongs is a hole in the row, not a deep cornice — so unlike most height questions
  in this set, the risk here is *not* contained by the loader's scale-to-1.0. Settle
  it before building: a single clear photograph of this frontage from across the
  park, outside leaf season, ends the argument.
- **The front bay, the setback and the open deck are a reading, not a measurement.**
  The 1984 permit says "new garage with open deck"; the January 2025 Street View
  shows a railing at second-floor level with the wall set back behind it and warm
  lights under the setback. The 3.0 m setback depth in 2.7 is *inferred* — it is
  what makes a plausible terrace on a 6.7 m frontage, not a measured figure. The
  5.89 m LiDAR minimum is weakly consistent with a lower front section but is just
  as likely an edge artifact. Confirm the depth, and if the front turns out to be
  full-height with a balcony rather than a setback with a terrace, say so loudly and
  rebuild step 2 — the deck is this roof's best feature and its geometry matters.
- **The Taber Place elevation is inferred.** The dark-brown lap-sided face with the
  grid windows and the glazed garage door is at the right place on the right side of
  the alley and its colour is consistent with the near-black front, but the Street
  View pano it came from is labelled "22 Taber Pl" and the panorama that resolves
  cleanly onto *this* lot could not be isolated. If it is the wrong building, the
  most likely correction is that the rear is plainer and the garage is at the South
  Park end instead — which would also re-read the front's wide low windows as a
  converted garage opening. This is the most valuable single observation left to
  make about this building.
- **Which end has the garage.** Related to the above and not settled. The Assessor's
  address of record is 51 Taber Place, which favours the alley; the 2019 permit's
  "man doors to garage on 1st floor" does not say which end. Model it at Taber Place
  and record the assumption.
- **There is no architect and no history.** No architect, builder, designer or
  historic-resource finding was found for this building — only a 1907 build date, a
  fire, and a permit trail. The SF Planning Property Information Map shows the
  historic-resource status as "tentative" and directs enquiries to a Preservation
  Technical Specialist. This affects nothing about the model; it is flagged so the
  next researcher does not repeat the search blind. If a SoMa survey DPR 523 form
  exists for block 3775, it would settle both the original form and the extent of
  the 1984 rebuild.
- **OSM does not know this building exists.** No OSM way carries 26 or 28 South
  Park, and the block's `addr:housenumber` sequence jumps from `22;24` to `41;43`.
  That is why the geometry in this plan rests on the DataSF parcel and the DataSF
  LiDAR footprint alone, with no third opinion — unusually for this set, there are
  only two surveys, not three. The two agree on heading to 0.9° and on area to 10%,
  and the parcel matches the Assessor's `lot_area` to 0.1%, so the shape is safe;
  but there is no cross-check available on the *building* outline as distinct from
  the lot.
- **The building has changed use three times in twenty-five years** — dwelling,
  salon, office — and is currently marked Leased with the tenancy unknown. Model it
  as architecture: a dark box, one entry, glazing at both ends. Do not model
  signage, and do not let the "office" category pull the night state toward a lit
  workplace (2.8).
