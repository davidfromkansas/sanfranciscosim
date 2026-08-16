# 524 Second Street — SF-SIM asset plan

A 1923 brick warehouse on the corner of Second Street and Taber Place, three lots
southeast of Bryant. It is the **lowest building on its block face** — two storeys and
8.96 m of measured roof between a five-storey neighbour at 512 (19.7 m) and a
three-storey one at 544 (12.8 m) — and it carries one detail nothing else on the block
has: a **crenellated parapet**, a row of chunky square merlon blocks marching along the
top of the Second Street elevation.

It is also a **corner** building, which is the design problem. Taber Place runs the full
29.6 m of its northwest flank, so this asset has two real elevations, not one facade and
three blanks. The brief is "the low crenellated brick warehouse on the alley corner",
and the whole job is making the merlon row read at thumbnail size while keeping the Taber
Place flank honest.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/524-second/`. This document is the plan only: Part 1 is the runnable task
prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `524-second` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3934330, 37.7825731` |
| Target height | **9.9 m** to the merlon tops; parapet coping 9.45 m; roof membrane 8.96 m (measured) |
| Footprint | 20.92 m (Second Street frontage, NE) x 29.63 m deep; 619.9 m2, measured |
| Triangle cap | 11,000 |
| Category | `19` (industrial) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 524 Second Street GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of 524 Second Street in San Francisco and deliver
it as a downloadable, validated GLB.

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
7. `artifacts/358-brannan/` — the closest reference implementation: the same block
   (3775), the same decade, the same building type, and a build script whose footprint,
   panel and roof helpers this asset should reuse rather than reinvent
8. `artifacts/380-brannan/` — the broad-box counterpart, for its parapet and roof
   furniture helpers; 524 is a broad box, not a slot
9. `docs/asset-plans/524-second.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Must capture

- A **low, broad, two-storey brick box**: 20.92 m of Second Street frontage, 29.63 m
  deep, roof membrane at 8.96 m. It must read as clearly *shorter* than everything
  around it — that is half of its identity
- The **crenellated parapet**: a row of square merlon blocks standing proud of a plain
  brick parapet along the Second Street elevation, returning around the Taber Place
  corner. Nine blocks on the front is the observed count. This is the one identity cue
  carried hard, and the only thing the aerial camera will use to name this building
- **Two real elevations.** Second Street (northeast) is the hero; **Taber Place
  (northwest) is a full second elevation**, not a party wall — red brick piers with
  large steel-sash industrial windows over a grey painted base, running the whole 29.6 m
- A **two-tone facade**: warm grey painted ground-floor base and piers under bare red
  brick above. The paint line is horizontal and hard, and it is what makes the building
  read as a converted warehouse rather than a brick block
- **Large multi-light steel-sash windows** in both storeys of both elevations, set in
  brick bays. Six bays on Second Street is the observed rhythm
- The **projecting grey entrance bay** at the centre of the Second Street ground floor,
  and the recessed dark double doors two bays northwest of it
- A **flat membrane roof** with a parapet ring, three or four skylights and a scatter of
  rooftop mechanical units — the permits record two rooftop units, a condenser and three
  exhaust fans, and the aerial confirms them

## Research 524 Second Street independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world orientation,
and gather references covering:

- Both public elevations — Second Street (northeast) and Taber Place (northwest). A
  model built from the Second Street photograph alone will have an invented flank on a
  wall that thousands of people walk past
- Aerial and roof views (the parapet ring, the skylights, the mechanical scatter)
- Ground-level views, day and night
- The exact height of the parapet coping and of the merlon blocks — the weakest numbers
  in this dossier (see 2.15)
- The merlon count and spacing, and whether the row returns down the Taber Place flank
  or stops at the corner

Prefer architect/engineer publications, owner or institutional material, planning and
permitting documents, architectural press, geolocated photography, and aerial/satellite
imagery. Never rely on a single photograph, a single AI-generated image, or a single
unsourced 3D model. Separate verified facts from visual inference; if sources disagree,
document the disagreement and decide.

**Three source conflicts are already known and resolved in 2.1 — re-check them, do not
silently re-inherit the wrong value:** the OSM `height=9` tag describes the roof
membrane and **is not the architectural top**, which is the merlon row; the DataSF LiDAR
`hgt_maxcm` of **13.32 m is not this building** (see 2.15); and three footprint sources
disagree by 12% (LiDAR 570 m2, OSM 615 m2, parcel 639 m2) — the OSM trace is used and
the reasoning is in 2.3.

## Create a reference dossier

Write `artifacts/524-second/REFERENCE.md` containing: source links and what each
establishes; verified dimensions and location; orientation; observations from all four
sides and above; the 3-5 strongest recognition cues; features to preserve; features to
simplify; uncertainties and conflicting evidence. A contact sheet of attributed
reference thumbnails is welcome if legally permissible — do not commit copyrighted
full-resolution imagery.

## Make your own design decisions

Follow the conversion process in `docs/styles/miniature-toy.md` §22: identify the
recognition cues, strip nonessential information, rebuild the massing from a few
confident volumes, exaggerate only the signature features, simplify the facade into
broad rhythms, deliberately design every surface visible from above, evaluate from the
app's high three-quarter aerial camera, then simplify again.

This is a **secondary building** in the style bible's detail budget (§21), but a broad
one with two public faces. Clear massing, one strong facade rhythm repeated on both
elevations, a designed roof, and exactly one identity cue carried hard — the merlons.
Resist hero-tier ornament. The merlons are the only place semantic exaggeration is spent.

The finished asset must be immediately recognizable as 524 Second Street, consistent
with the real building from all four sides and above, architecturally credible, and a
premium handcrafted miniature — not photorealistic, not voxel art, not generic
low-poly, and never accurate in one view while invented in the others.

## Scope of the exported asset

Export the single 1923 building: both public elevations, both party walls, the parapet
and its merlons, the roof and its furniture.

Do not include unrelated surrounding city geometry: Second Street, Taber Place, the
neighbouring buildings at 512 and 544 Second Street, 10 South Park, street trees, the
sidewalk, parked cars, people, plinths, cameras or lights. Temporary context may appear
in review renders but must not leak into the GLB.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary `.glb`;
real-world meters; origin at base center; minimum geometry Z ~ 0; applied transforms;
no negative scales; outward normals; no duplicate or foreign geometry; no image
textures; no transparency; flat-color materials named `Toy_*` from the project palette;
`_Glow` suffix only on surfaces that glow at night; no `Toy_body`; no cameras, lights,
animations, armatures or constraints; no external dependencies; at most 11,000 triangles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model drops
into the city at its real-world heading — the loader applies no rotation (`placeGeneric`
in `app/src/assets.js` only scales and positions). The Second Street front faces
**northeast, bearing 45.6°**; the Taber Place flank faces **northwest, 315.4°**; the
party wall to 544 faces **southeast, 135.4°**; the rear faces **southwest, 225.6°**.
The building is rotated about 45° off the world axes, so build directly on the measured
footprint rectangle in 2.3 rather than modelling an axis-aligned box and rotating it.
Record the measured heading in `REPORT.md`.

**Height normalization:** the tallest geometry in the export (the merlon block tops)
must land at exactly **9.9 m** so the loader's `targetHeightM / measuredHeight` scale
is 1.0.

## Reproducible Blender workflow

Blender 5.2 LTS. Headless: `blender -b --python script.py -- args`.

Keep `artifacts/524-second/build_524_second.py` (deterministic build script),
`artifacts/524-second/524-second.blend`, and `artifacts/524-second/524-second.glb`.
The script must rebuild the model reliably enough for future revision. Do not modify or
rename an unrelated existing GLB to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras: `524-second-top.png`,
`524-second-north.png`, `524-second-east.png`, `524-second-south.png`,
`524-second-west.png`, plus `524-second-contact-sheet.png`, at least one high
three-quarter aerial beauty render `524-second-aerial.png`, and a night render
`524-second-aerial-night.png`.

The four elevations must share scale, framing, lighting, exposure and projection; use
orthographic or long-lens cameras; label directions from the researched orientation; the
top view must clearly show the parapet ring, the merlon row, the skylights and the
mechanical scatter; the aerial view uses the style bible's camera assumptions (30-50
degrees down, long lens). Simple tabletop lighting, neutral warm background, minimal
depth of field, and every image must depict the same exported model.

Note that the axis-aligned elevation renders will each show the building at 45°, and the
"north"/"east" views each see a public elevation and a party wall together. That is the
expected consequence of the real heading, not a camera error.

## Validate the exported GLB

Re-import `524-second.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture count,
camera count, light count, animation count, applied-transform status, negative-scale
status, normal-orientation status, unexpected geometry, and per-material contract
compliance. Render at least one review image from the re-imported asset. Write
`artifacts/524-second/validation.json` and `artifacts/524-second/REPORT.md`.

Note that the axis-aligned XY bounding box will be roughly **35.9 x 35.6 m** even though
the building is 20.92 x 29.63 m — that is the expected consequence of a ~45° real-world
heading, not a scale error.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this draft
entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "524-second",
  "file": "524-second.glb",
  "anchor": [
    -122.3934330,
    37.7825731
  ],
  "targetHeightM": 9.9,
  "cat": 19,
  "name": "524 Second Street",
  "estimated": true,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a separate, explicitly requested job — run `docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in `docs/asset-plans/524-second.md`.
````

---

## Part 2 — Research and design dossier

Compiled 16 August 2026 from the sources in 2.2. Values marked *inferred* or *estimated*
are visual or derived, not published figures — the executing agent must re-verify
anything it relies on.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Block / lot | 3775 / 004 | DataSF parcels `acdm-wktn` — `blklot=3775004`, `from_address_num = 522`, `to_address_num = 524`, `street_name = 02ND ST`, active, mapped 1998-07-01 |
| Built | 1923 | SF Assessor secured roll, block 3775 lot 004 |
| Storeys | **2** | SF Assessor roll (`number_of_stories = 2.0`) **and** every building permit 2005-2020 (`number_of_existing_stories = 2`, `number_of_proposed_stories = 2`) — no conflict |
| Use (assessor) | Industrial | SF Assessor roll `property_class_code_definition` |
| Use (permits / actual) | Office | SF permits 2005-2020 (`existing_use = office`); tenants are venture and tech firms |
| Building area | 13,475 sq ft = 1,251.9 m2 | SF Assessor roll `property_area`. 2.02x the footprint — two full floors, confirming the storey count arithmetically |
| Lot area | 639.1 m2 = 6,879 sq ft | DataSF parcel polygon `3775004`, reprojected |
| Footprint | 619.9 m2; 20.92 m (NE frontage) x 29.63 m deep; 99.2% rectangular fill | OSM way 112926337, reprojected — **measured**; see 2.3 for why this source and not the other two |
| Roof membrane height | **8.96 m** above ground | DataSF LiDAR `hgt_mediancm = 896` over 2,293 cells, `hgt_mean 8.98`, `std 0.95` — **measured**, and an unusually tight distribution: this is a flat roof |
| Ground elevation | 14.73 m (NAVD88) | DataSF LiDAR `gnd_min_m` — app terrain handles this, not the asset |
| Corner condition | Second Street (NE) + Taber Place (NW) | OSM way 88559680 (2nd Street) and the Taber Place way; Taber Place T's into Second Street 18 m northwest of the frontage midpoint, and runs the full 29.6 m flank ~2.9 m off the wall |
| Zoning | CMUO (Central SoMa mixed use — office) | DataSF parcels |
| Frontage heading | Second Street front faces 45.6° (NE); Taber Place flank faces 315.4° (NW) | measured from the footprint OBB |
| Neighbours | 512 Second St (lot 002, 5 storeys, 1909, LiDAR 19.71 m) NW across Taber Place; 544 Second St (lot 005, 3 storeys, 1923, LiDAR 12.83 m) SE, party wall; 10 South Park (condos) at the rear | DataSF parcels + LiDAR + Assessor |
| Rooftop plant | 2 rooftop units, 1 condensing unit, 1 fan coil, 3 exhaust fans | SF permits 2006-11-27 and 2020-08-22 — the roof furniture is documented, not invented |
| Illuminated signage | electric single-faced door/window sign permitted 2012 | SF permit 2012-03-27 — the basis for the night glow choice in 2.8 |
| Current occupants | Menlo Ventures (SF office); previously Oculus VR (2014-2017) | menlovc.com/contact, SF registered-business records |

### 2.2 Sources

- `https://data.sfgov.org/resource/acdm-wktn` (DataSF Parcels) — **the address-to-lot
  link**: `3775004 = 522-524 2nd St`. Neighbours on the same block face are 001 = 500,
  002 = 512, 005 = 544
- `https://data.sfgov.org/resource/ynuv-fyni` (DataSF Building Footprints, LiDAR-derived)
  — polygon `SF3775004`, the 8.96 m median roof, the 14.73 m ground, and the neighbours'
  heights used for the "lowest on the block" claim
- `https://data.sfgov.org/resource/wv5m-vpq2` (SF Assessor Historical Secured Property
  Tax Rolls) — 1923, 2 storeys, 13,475 sq ft, Industrial
- `https://data.sfgov.org/resource/i98e-djp9` (SF Building Permits) — 29 permits;
  **2006-11-27** one new rooftop HVAC unit plus three exhaust fans; **2012-03-27**
  electric single-faced door/window sign; **2020-08-22** one new fan coil, one condensing
  unit, one rooftop unit; every permit records 2 existing and 2 proposed storeys
- https://www.openstreetmap.org/way/112926337 — the footprint used (see 2.3);
  `addr:housenumber=524`, `addr:street=2nd Street`, `building=yes`, `height=9`
- Google Street View, Second Street pano (capture **May 2025**) — the crenellated
  parapet and its nine merlons, the two-tone facade, the six window bays, the projecting
  grey entrance bay, the recessed dark doors, the "524" plate at the Taber Place end, and
  the Taber Place street sign that establishes the corner
- Google Street View, Taber Place pano (capture **Jan 2025**) — the northwest flank: red
  brick piers, continuous multi-light steel sash, grey painted base, security mesh
- Google Maps satellite (Vexcel imagery, 2026) — the flat light membrane roof, the
  parapet ring, three to four skylights, the mechanical scatter, a diagonal conduit run
- https://menlovc.com/contact/ — "524 2nd Street, San Francisco, CA 94107", current
  tenant
- SF registered-business records (opengovus mirror) — `524 2nd St. Bldg.` owned by
  L Myers Company since 1968; Oculus VR at this address 2014-2017; Health Technology
  Center at "524 Second St, 2nd Floor", which independently confirms a second floor

### 2.3 Orientation and placement

The building sits on the southeast corner of Second Street and Taber Place, mid-block
between Bryant and Brannan. It is rotated about 45° from the world axes, like the whole
SoMa grid.

**Three footprint sources disagree and the choice matters:**

| Source | Dimensions | Area | Note |
|---|---|---|---|
| DataSF LiDAR `SF3775004` | 19.3 x 29.5 m | 569.7 m2 | roof-level extent; undercounts, and its northeast edge is 2 m short of the property line |
| **OSM way 112926337** | **20.92 x 29.63 m** | **619.9 m2** | a clean 6-node rectangle; **used** |
| DataSF parcel `3775004` | 21.5 x 29.8 m | 639.1 m2 | the lot, not the building |

OSM is used because it sits between the other two exactly where a real wall sits: a
lot-line warehouse fills its lot, inset from the property line by the thickness of the
wall and the sidewalk tolerance — about 0.3 m per side, which is the whole discrepancy.
The LiDAR polygon is the outlier here, and it is short specifically on the Second Street
edge where a 19.7 m neighbour across a 6 m alley casts the scan into shadow. Note that
this is the **opposite** call from `358-brannan.md`, where OSM was demonstrably wrong and
DataSF right — the lesson is to reconcile all three every time, not to trust one source
by habit.

Footprint rectangle, in Blender coordinates (metres, `+X` east, `+Y` north),
counter-clockwise, already centred on the anchor `-122.3934330, 37.7825731`:

```
(  17.929,   2.918)     east corner
(  -3.240, -17.813)     south corner
( -17.929,  -2.918)     west corner
(   3.240,  17.813)     north corner
```

Edges, with outward normals:

| Edge | Length | Faces | Elevation |
|---|---|---|---|
| `(3.240,17.813) -> (17.929,2.918)` | 20.92 m | NE 45.6° | **Second Street front** |
| `(17.929,2.918) -> (-3.240,-17.813)` | 29.63 m | SE 135.4° | party wall to 544 Second St |
| `(-3.240,-17.813) -> (-17.929,-2.918)` | 20.92 m | SW 225.6° | rear, to 10 South Park |
| `(-17.929,-2.918) -> (3.240,17.813)` | 29.63 m | NW 315.4° | **Taber Place flank** |

Because of the 45° heading the axis-aligned bounding box is ~35.9 x 35.6 m for a
building that is 20.92 x 29.63 m. That is correct.

### 2.4 What each side shows

**Northeast (Second Street front)** — The hero elevation, 20.9 m of it. Top to bottom:
a **crenellated parapet** — a plain brick parapet with a row of **nine chunky square
merlon blocks** standing about 0.45 m proud of it, evenly spaced across the frontage and
reading as pale grey-tan against the brick. Below the parapet, a shallow brick band and
a row of short recessed vertical brick panels, one under each merlon. Then the second
storey: **six bays** of large multi-light steel-sash window, dark framed, separated by
plain red brick piers, each under a flat brick lintel. Then a hard horizontal line where
the paint starts, and the ground floor: warm **grey painted** piers and plinth with tall
multi-light steel storefront glazing between them; a **projecting grey entrance bay** at
the centre carrying its own window and a small cornice cap; **recessed dark glazed
double doors** in a grey reveal two bays northwest of it; and a painted **"524"** high on
the brick at the Taber Place end.

**Northwest (Taber Place flank)** — A full second elevation, 29.6 m long, and the reason
this asset is not a one-facade job. Bare red brick piers at the same rhythm as the front,
with continuous **large multi-light steel sash** between them on both storeys, some of it
behind security mesh, over a **grey painted stucco base band** about 1.5 m high. No
ornament, no merlon return visible in the January 2025 pano at the point it was shot —
whether the merlon row turns the corner is listed as an open question in 2.15. The alley
is narrow, so this wall is seen close-up and obliquely, and from directly above.

**Southeast flank** — Party wall, 29.6 m, hard against 544 Second Street, which is 3.9 m
taller. Blind. Only the top ~1 m is ever visible, and only from the air. Do **not**
invent windows here.

**Southwest (rear)** — 20.9 m against the 10 South Park block. Blind or nearly so, and
never seen from the street. Plain brick.

**Top** — 620 m2 of flat light membrane roof at 8.96 m inside a parapet ring, and it is
what the app's camera actually looks at. The Vexcel aerial shows: the parapet ring
darker than the deck on its inner face; **three to four pale skylights** scattered across
the middle; a **cluster of mechanical units** toward the Second Street end and a second
loose row across the centre — consistent with the permitted two rooftop units, condenser,
fan coil and three exhaust fans; and a straight diagonal run of small fixtures crossing
the roof. Nothing tall: the whole roof reads flat from above, which is why the merlon row
is the only silhouette this building has.

### 2.5 Recognition cues (ranked)

1. **The crenellated parapet** — a row of square merlon blocks along the top. Nothing
   else on this block face has it, and it is the only thing that breaks the silhouette.
   If the merlons do not read at thumbnail size, the asset has failed
2. **Lowest on the block** — 8.96 m between a 19.7 m and a 12.8 m neighbour. The
   building is a notch in the street wall
3. **The two-tone facade** — grey painted ground floor under bare red brick, on a hard
   horizontal line
4. **Two glazed elevations turning a corner** — the same brick-pier-and-steel-sash
   rhythm on Second Street and Taber Place, which is what makes it a corner warehouse
   rather than a storefront
5. The projecting grey entrance bay at the centre of the front

### 2.6 Miniature translation

**Preserve**

- The 20.92 x 29.63 m proportion and the real 45.6° heading, exactly
- The merlon row as **discrete blocks with visible gaps** — a continuous raised band
  would destroy the only cue this building has
- The corner condition: Taber Place is a designed elevation with the same bay rhythm as
  the front, not a blank flank
- The hard horizontal paint line between the grey base and the brick above
- The building's lowness relative to its neighbours — never raise it "so it reads better"

**Simplify / exaggerate**

- The merlons are **thickened and lifted** to 0.45 m proud so the silhouette survives at
  distance. This is the one place semantic exaggeration is spent
- Roughly thirty small panes per window become one glazed panel per opening with a light
  frame and, at most, one horizontal and one vertical mullion; individual muntins
  disappear
- Six bays on the front and nine on the flank are kept as *rhythm*, not counted panes
- The recessed vertical brick panels under the merlons become a single shallow reveal
  band, or are dropped if they cost more than 400 triangles
- The security mesh, downpipes, conduit, wall boxes, the banner bracket and the street
  signs are dropped — all sub-pixel at city scale
- Roof clutter becomes three skylight boxes, two mechanical blocks, one condenser and one
  hatch. Nothing more, and nothing over 1.6 m tall

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not a
straitjacket — adjust after the first aerial review render.

1. Body: extrude the 2.3 rectangle from z=0 to z=8.96 (`Toy_brick` walls), cap
   `Toy_roofd` — the roof membrane.
2. Parapet: ring on all four edges, z=8.96 to **z=9.45**, 0.35 m thick, `Toy_brick`
   outer face with a `Toy_stone` coping on top. On the two party sides drop the ring to
   z=9.15 so the aerial reads the front and flank as the designed ones.
3. **Merlons**: nine blocks on the Second Street edge, 0.85 m wide x 0.35 m deep x
   **0.45 m** tall, `Toy_stone`, sitting on the coping, evenly spaced with the outermost
   two at the corners; land their tops on **z=9.90** exactly — this sets the bounding-box
   top. Return three blocks around the Taber Place corner (see 2.15).
4. Ground-floor paint band: 0.06 m proud panel on the NE and NW faces, z=0 to z=4.60,
   `Toy_stone` — the warm grey base. The paint line at 4.60 m is the strongest horizontal
   in the asset; keep it dead level on both elevations.
5. Second Street bays: six openings, each 2.55 m wide, at both levels. Ground floor
   z=1.10 to z=4.20 (`Toy_glass` in `Toy_stone` frames); second floor z=5.55 to z=8.10
   (`Toy_glass` in `Toy_roofd` frames, dark steel). Brick piers 0.9 m wide between them.
6. Entrance bay: a shallow rectangular oriel projecting 0.35 m from the front skin at the
   centre bay, 3.10 m wide, z=0 to z=5.05, `Toy_stone`, with one `Toy_glass` panel and a
   flat cap. Two bays northwest of it, a recessed `Toy_ink` double door 2.20 m wide,
   z=0 to z=3.30, set 0.25 m back in a `Toy_stone` reveal.
7. Taber Place flank: nine bays on the same rhythm, openings 2.30 m wide; ground floor
   z=1.60 to z=4.20, second floor z=5.55 to z=8.10, all `Toy_glass` in `Toy_roofd`
   frames, brick piers between. Grey base band z=0 to z=1.60 in `Toy_stone`.
8. Party walls (SE, SW): plain `Toy_brick`, no openings, no reveals.
9. Roof: three skylight boxes 2.2 x 1.6 x 0.30 m (`Toy_glassl` on `Toy_stone` kerbs)
   spread across the middle third; two mechanical blocks 1.8 x 1.4 x 1.1 m and
   1.4 x 1.2 x 0.9 m (`Toy_steel`) grouped toward the Second Street end; one condenser
   1.1 x 1.1 x 0.8 m (`Toy_steel`); one hatch 1.2 x 1.0 x 0.45 m (`Toy_roofd`) near the
   southeast party wall. Keep the middle of the deck open.
10. Bevel 0.10 m, 2 segments on the masses; 0.04/1 on applied panels and merlons.

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_brick` | `#c96f4a` | all brick — both elevations above the paint line, both party walls, the parapet |
| `Toy_stone` | `#d9d2c2` | the grey painted base, the merlons, the parapet coping, the entrance bay, window frames on the front, skylight kerbs |
| `Toy_glass` | `#2a4d73` | all windows and storefront glazing |
| `Toy_glassl` | `#6f95b8` | skylights |
| `Toy_roofd` | `#45454a` | roof membrane, the dark steel window frames on both elevations |
| `Toy_steel` | `#9aa0a6` | rooftop mechanical blocks and condenser |
| `Toy_ink` | `#3a3530` | the recessed double doors and their reveal shadow |
| `Toy_glass_Glow` | `#6f95b8` | three lit second-floor windows on Second Street, two on Taber Place |
| `Toy_gold_Glow` | `#caa64a` | **the entrance bay's lit sign panel** — the night hero |

Note on the base colour: the real paint is a warm mid-grey, greyer than `Toy_stone`
(`#d9d2c2`) and lighter than `Toy_steel` (`#9aa0a6`). `Toy_stone` is used because the
asset's job at distance is a light base under dark brick, and `Toy_steel` would read as
metal next to the rooftop plant. `358-brannan` two blocks away spends `Toy_stone` on its
*flanks* and `Toy_brick` on its front; here the split is horizontal instead of
front-to-back, which is what keeps the two SoMa warehouses from reading as one building
twice.

**Night state (required).** Glow surfaces must be thin shells proud of the opaque surface
behind them — the app renders `_Glow` in a separate layer that is ~12% alpha by day, so a
primary surface must never be authored as glow. Hero glow: the **entrance bay's sign
panel** in `Toy_gold_Glow`, which is exactly what the 2012 electric door/window sign
permit describes. Supporting accents: three of six second-floor windows lit on Second
Street and two of nine on Taber Place, in `Toy_glass_Glow` — an office building with
people still in it, not a lit-up box. The ground floor does not glow; the party walls do
not glow.

### 2.9 Top surface

620 m2 of roof, flat, seen constantly from above, and with no height variation at all to
help it. The composition is therefore: the **parapet ring** must read clearly — coping
lighter than the deck, and the merlon row visible from directly overhead as nine
detached blocks on one edge; the mechanical units grouped toward the Second Street third
so the middle stays open; the skylights spread as a loose diagonal, matching the aerial.
Nothing on this roof should exceed 1.6 m — the building is only 8.96 m tall, and one
oversized HVAC box would read as a third storey.

### 2.10 Scope

**In the GLB:** the single 1923 building — body, parapet and merlons, both public
elevations with their bays and glazing, the entrance bay and the recessed doors, both
party walls, the roof membrane and its furniture

**Not in the GLB:** Second Street, Taber Place, 512 and 544 Second Street, 10 South Park,
street trees, sidewalk, vehicles, people, plinths, cameras or lights

### 2.11 Triangle budget

Cap 11,000 — larger than 358 Brannan's 7,000 because this building has 3.7x the footprint
and two fully glazed public elevations, and smaller than a hero because it has one
ornament and a flat roof. Suggested split: body, parapet and coping ~1.5k; merlons ~1.2k;
Second Street bays and glazing ~2.5k; Taber Place bays and glazing ~3.0k; entrance bay and
doors ~0.8k; roof furniture ~1.4k.

### 2.12 Draft manifest entry

```json
{
  "id": "524-second",
  "file": "524-second.glb",
  "anchor": [
    -122.3934330,
    37.7825731
  ],
  "targetHeightM": 9.9,
  "cat": 19,
  "name": "524 Second Street",
  "estimated": true,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

`dims` and `tris` are placeholders until the asset is built and validated.
`"estimated": true` because the target height is photogrammetric, not published — the
roof membrane is measured but the parapet and merlons above it are not. See 2.15.

### 2.13 Integration notes (for later, not this task)

- **New landmark.** Add a `pipeline/lib/landmarks.mjs` entry (`id: '524-second'`) and
  re-bake the affected tiles, or the baked procedural building on this footprint will
  intersect the GLB.
- **Exclusion radius.** Size it from neighbour *vertices*, not centroids, and measure it
  against the real bake input. The southeast party wall is shared with 544 Second Street
  and the rear wall with the 10 South Park block, so those neighbours' footprints have
  vertices *on* this building's outline — some collateral is unavoidable, exactly as
  documented for the other infill sites on this block. The half-diagonal of the footprint
  is 18.1 m; start near the half-width (10.5 m) plus a small margin, verify by eye in the
  re-baked tiles, and record the number in `REPORT.md`. Taber Place gives free clearance
  on the northwest side, so the risk is entirely southeast and southwest.
- `loadRadius`: the skill's default formula gives `max(2500, 9.9 * 30) = 2500` m. Take
  the default; at 2.5 km a 9.9 m building is far below a pixel.
- This is now the **third** landmark on block 3775 (with 358 and 370-380 Brannan) and one
  of a growing set of one-off SoMa warehouses in a manifest designed for monuments. Judge
  it in the aerial next to 358 Brannan: if the two read as the same building at different
  widths, the merlon row is not doing enough work.
- 501 Second Street is being built in the same batch, 70 m northwest across Bryant. They
  are opposite problems — a 33 m seven-storey block against a 9 m two-storey one — and
  should be judged together once both land.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Bounding-box top exactly 9.9 m (loader scale lands at 1.0)
- [ ] Dimensions plausible in meters and consistent with 2.1 (XY bbox ~35.9 x 35.6 m is expected)
- [ ] Footprint proportion preserved: the building must measure 20.92 x 29.63 m along its own axes
- [ ] Merlons are nine discrete blocks with visible gaps, tops coplanar at 9.9 m
- [ ] Triangles at or under 11,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the sign panel and the named windows; glow shells proud of the opaque surface
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (per-object signed volume for the union of solids; ray test residual <= 0.15%)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + contact sheet + night render regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

- **The target height is estimated, and it is the weakest number here.** The roof
  membrane at 8.96 m is a real LiDAR measurement over 2,293 cells with a 0.95 m standard
  deviation — trustworthy. Everything above it is photogrammetric: the May 2025 Second
  Street panorama, rectified against the measured 20.92 m frontage and a 2.35 m camera
  height derived from the same image, puts the parapet coping at 9.43 m and the merlon
  tops at 9.87 m, with roughly ±0.6 m of uncertainty. 9.45 and 9.90 are taken. The
  manifest entry is therefore `"estimated": true`.
- **The OSM `height=9` tag is the roof, not the architectural top.** It agrees with the
  LiDAR membrane to 0.04 m, which is reassuring about the membrane and says nothing about
  the parapet. The plans README's standing warning applies: an OSM `height` tag describes
  a low shell and must never be the target height.
- **DataSF `hgt_maxcm` = 13.32 m is almost certainly not this building.** The same record
  gives `hgt_median 8.96`, `hgt_mean 8.98`, `std 0.95` over 2,293 cells. A 13.3 m maximum
  against a 0.95 m standard deviation is a handful of cells, and 512 Second Street — 19.7
  m tall — stands across a 6 m alley on that side. Treat it as polygon-edge bleed, not a
  penthouse. `hgt_mincm` of 2.29 m is the same artefact at the other end. (The identical
  13.32 m figure appears in `358-brannan.md` for a different record on the same block;
  that is a coincidence of two edge-bleed maxima, not a shared source.)
- **Whether the merlon row returns around the Taber Place corner is inferred.** The May
  2025 front pano shows the row running the full frontage and a block at the corner
  itself; the January 2025 Taber pano was shot too close and too low to see the parapet.
  Three blocks are returned in 2.7 as the conservative reading. Confirm from an oblique
  aerial before committing, and say what was found in `REPORT.md`.
- **The merlon count of nine is read from one photograph** partly occluded by four street
  trees. It is consistent with the 20.92 m frontage at ~2.3 m centres. If the executing
  agent's own references show eight or ten, use theirs and record the change.
- **The bay rhythm on Taber Place is inferred from a single close-range pano** that shows
  three piers. Nine bays over 29.63 m is extrapolated from the pier spacing observed
  there and from the front's rhythm. This is the most likely place for the model to be
  wrong in a way the aerial camera will see.
- **The rear (southwest) elevation has no reference at all.** It is assumed blind brick.
  The building is hard against the 10 South Park block, so this is safe, but it is an
  assumption, not an observation.
- No architect is recorded for the 1923 building in any source consulted. The owner of
  record, L Myers Company, has held the property since at least 1968.
