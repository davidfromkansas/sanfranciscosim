# 181 South Park — SF-SIM asset plan

A 2002 four-storey live/work loft building on the south-west rim of South Park, and one of
the strangest lots in SoMa: a 43 m long, 13.8 m wide slab that runs the full depth of the
block from the park frontage back to the Varney Place alley, under a long ridged
standing-seam metal roof. It is the tallest thing on its side of the oval by about 5 m,
and it is the building Instagram was working out of on the day Facebook bought them. Not a
monument — a *character* building, with two things to carry: its proportion (a thin, tall
sliver seen end-on from the park and broadside from above) and the fact that it is the one
roof on this block that is not flat.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/181-south-park/`. This document is the plan only: Part 1 is the runnable task
prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `181-south-park` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3945113, 37.7807582` (oriented-bounding-box centre, measured) |
| Target height | **16.5 m** to the roof ridge; eaves ~11.8 m (derived, see 2.1) |
| Footprint | 43.31 m (deep, NW–SE) x 13.85 m (wide); 599.9 m2, measured — a plain rectangle at bearing 135.2° |
| Triangle cap | 9,000 |
| Category | `2` (apartments — live/work lofts over ground-floor commercial) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 181 South Park GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of 181 South Park in San Francisco and deliver it
as a downloadable, validated GLB.

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
7. `artifacts/380-brannan/` — the closest reference implementation in scale, character and
   neighbourhood (a secondary SoMa street building one block west, same detail tier). Note
   that its roof is flat and this one is not, so take its detail budget and its facade
   discipline, not its roof approach
8. `docs/asset-plans/181-south-park.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Photo research is a hard gate on this one — do it before you model

The dossier below is strong on geometry, has one good aerial observation, and is weak on
everything at street level: no street-level photography could be consulted while it was
written. The roof (2.4 "Top", 2.9) was read from 2026 Vexcel aerial imagery and is
reliable in form; the four *elevations* in 2.4 and the palette in 2.8 are *inferred* and
must be replaced with observed fact before you build anything.

What you must still settle from imagery, in priority order:

1. **Where the eave line actually sits.** 2.1 derives ~11.8 m from the LiDAR height
   distribution rather than measuring it, and the storey reading in 2.4 depends on it.
2. **The facade** — material, colour, window rhythm, bay count, whether there is a
   signature accent. Nothing here is observed.
3. **The lower element at the Varney end** (2.15), which the aerial hints at but does not
   confirm.

The roof's section is no longer on this list: 2.15 settles it as a straight gable from the
LiDAR height distribution. Confirm it if a photograph turns up, but do not reopen it
without one.

Record what you found and how in `REFERENCE.md` and `REPORT.md`.

## Must capture

- The **proportion**: a 43 m x 13.8 m slab, three times as deep as it is wide, running the
  full depth of the block. This is the building's whole identity and it must not be
  quietly squared up toward something more comfortable to model.
- Four storeys, standing ~5 m proud of every neighbour on its side of the oval
- Tall steel-sash loft windows in a regular bay rhythm on the long flanks
- A ground-floor commercial storefront at the South Park (NW) end and the residential entry
- The garage door at the Varney Place (SE) end
- **The ridged metal roof running the length of the building** — the one non-flat roof on
  this side of the oval, and the thing that will make the model findable from the air
- A deliberately designed roof — the camera looks down and this roof is 43 m long

## Research 181 South Park independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- All four elevations. Note that two of them are *ends*: the 13.8 m wide NW face onto
  South Park and the 13.8 m wide SE face onto Varney Place. The long faces are the
  43 m flanks.
- Aerial and roof views at higher resolution than 2.4 could reach — this is where the
  barrel-versus-gable question gets settled
- Ground-level views from South Park and from Varney Place, which is where the eave line
  and the whole facade reading get settled
- Day and night appearance
- The bay count and window rhythm of the long flanks — the dossier's 10-bay reading is
  *inferred* and is the weakest number in it
- The facade material and colour, which the dossier does not know at all

Prefer architect/engineer publications, owner or institutional material,
planning and permitting documents, architectural press, geolocated photography,
and aerial/satellite imagery. Never rely on a single photograph, a single
AI-generated image, or a single unsourced 3D model. Separate verified facts from
visual inference; if sources disagree, document the disagreement and decide.

**One source conflict is already known and resolved in 2.1 — re-check it, do not silently
re-inherit the wrong value:** OSM tags `height=14` on this building, which is the LiDAR
*median* roof height. On a ridged roof that median is a mid-slope value matching no physical
line on the building: the ridge is 16.5 m and the eave is lower still. The assessor roll is also useless
for storeys here (it records the seven condominium units separately, at 0, 1 and 2 storeys
each); the 2000 construction permit says **four storeys** and is authoritative.

## Create a reference dossier

Write `artifacts/181-south-park/REFERENCE.md` containing: source links and what each
establishes; verified dimensions and location; orientation; observations from all
four sides and above; the 3-5 strongest recognition cues; features to preserve;
features to simplify; uncertainties and conflicting evidence. A contact sheet of
attributed reference thumbnails is welcome if legally permissible — do not commit
copyrighted full-resolution imagery.

## Make your own design decisions

Follow the conversion process in `docs/styles/miniature-toy.md` §22: identify the
recognition cues, strip nonessential information, rebuild the massing from a few
confident volumes, exaggerate only the signature features, simplify the facade
into broad rhythms, deliberately design every surface visible from above,
evaluate from the app's high three-quarter aerial camera, then simplify again.

This is a **secondary building** in the style bible's detail budget (§21), not a hero
landmark: clear massing, one strong facade rhythm, a simple designed roof, and exactly
one identity cue carried hard — the slab proportion and the extra storey that lifts it
above its neighbours. Resist adding hero-tier ornament.

The finished asset must be immediately recognizable as 181 South Park, consistent with
the real building from all four sides and above, architecturally credible, and a
premium handcrafted miniature — not photorealistic, not voxel art, not generic
low-poly, and never accurate in one view while invented in the others.

## Scope of the exported asset

Export the single 2002 loft block: body, all four elevations' openings, the roof and its
furniture, the ridged roof, and the ground-floor storefront and garage door.

Do not include unrelated surrounding city geometry: South Park itself, the park's trees or
lawn, Varney Place, 171 South Park next door, the Shell station across the flank, the
sidewalk, parked cars, people, plinths, cameras or lights. Temporary context may appear in
review renders but must not leak into the GLB.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary
`.glb`; real-world meters; origin at base center; minimum geometry Z ~ 0;
applied transforms; no negative scales; outward normals; no duplicate or foreign
geometry; no image textures; no transparency; flat-color materials named `Toy_*`
from the project palette; `_Glow` suffix only on surfaces that glow at night; no
`Toy_body`; no cameras, lights, animations, armatures or constraints; no external
dependencies; at most 9,000 triangles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model
drops into the city at its real-world heading — the loader applies no rotation
(`placeGeneric` in `app/src/assets.js` only scales and positions). The South Park entrance
end faces **northwest, bearing 315.2°**; the building's long axis runs 135.2°/315.2°, so
build directly on the measured footprint rectangle in 2.3 rather than modelling an
axis-aligned box and rotating it. The contract's "front faces −Y" cannot be honoured
literally here; real-world orientation wins (AGENTS rule 5) and the deviation goes in
`REPORT.md`.

**Height normalization:** the tallest geometry in the export (the roof ridge) must
land at exactly **16.5 m** so the loader's `targetHeightM / measuredHeight` scale is 1.0.

## Reproducible Blender workflow

Blender 5.2 LTS. Headless: `blender -b --python script.py -- args`.

Keep `artifacts/181-south-park/build_181_south_park.py` (deterministic build script),
`artifacts/181-south-park/181-south-park.blend`, and
`artifacts/181-south-park/181-south-park.glb`. The script must rebuild the model reliably
enough for future revision. Do not modify or rename an unrelated existing GLB to satisfy
the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`181-south-park-top.png`, `181-south-park-north.png`, `181-south-park-east.png`,
`181-south-park-south.png`, `181-south-park-west.png`, plus
`181-south-park-contact-sheet.png`, at least one high three-quarter aerial beauty render
`181-south-park-aerial.png`, and a night render `181-south-park-aerial-night.png`.

The four elevations must share scale, framing, lighting, exposure and
projection; use orthographic or long-lens cameras; label directions from the
researched orientation; the top view must clearly show the full 43 m roof — its ridge
line, its glazing and its mechanical layout; the aerial view uses the style bible's
camera assumptions (30-50 degrees down, long lens). Simple tabletop lighting, neutral warm
background, minimal depth of field, and every image must depict the same exported model.

Because the building is rotated ~45° from the world axes, the four compass renders will
each show two faces at 45°. That is correct and expected — do not rotate the model to make
the elevations square on.

## Validate the exported GLB

Re-import `181-south-park.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture
count, camera count, light count, animation count, applied-transform status,
negative-scale status, normal-orientation status, unexpected geometry, and
per-material contract compliance. Render at least one review image from the
re-imported asset. Write `artifacts/181-south-park/validation.json` and
`artifacts/181-south-park/REPORT.md`.

Note that the axis-aligned XY bounding box will be roughly **40 x 40 m** even though the
building is 43.3 x 13.9 m — that is the expected consequence of a ~45° real-world heading,
not a scale error.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "181-south-park",
  "file": "181-south-park.glb",
  "anchor": [
    -122.3945113,
    37.7807582
  ],
  "targetHeightM": 16.5,
  "cat": 2,
  "name": "181 South Park",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a separate, explicitly requested job — run `docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in `docs/asset-plans/181-south-park.md`.
````

---

## Part 2 — Research and design dossier

Compiled 12 August 2026 from the sources in 2.2. Values marked *inferred* are visual or
derived estimates, not published figures — the executing agent must re-verify
anything it relies on.

**A warning specific to this dossier.** Its evidence is uneven and it says so line by line.
Everything geometric is measured from survey data and is solid. The **roof** was read from
2026 Vexcel aerial imagery (Bing Maps satellite) and is an observation. Everything at
street level — facade material, colour, window rhythm, bay count, storey line — is
inference from permit records and listing copy, because no street-level imagery could be
reached from the authoring session: Google Maps and Street View were blocked and no open
substitute covered the block. The four elevations in 2.4 and the palette in 2.8 are
hypotheses, not observations. Treat street-level photo research as gate zero of stage 2.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Built | 2000–2002; construction permit completed 24 Dec 2002 | SF building permit 200005099501 |
| Storeys | **4** | permit 200005099501 "erect a four story, five unit live/work loft"; permit 200112145293 "a new 4-story live/work bldng"; every permit 2006–2022 records `number_of_existing_stories = 4` |
| Assessor storey count | 0, 1 and 2 across the seven condo lots | SF Assessor roll — **not a building storey count**, see 2.15 |
| Replaced | a two-storey warehouse/office building, demolished under permit 200005099504 | SF building permits |
| Construction | wood frame (Type V) over a garage level | permits (`wood frame (5)`; the 2002 exit revision records `constr type 4`) |
| Programme | 5 live/work loft units above ground-floor office/retail, plus a garage | permits 200005099501, 200209106108, 200211131341 |
| Condominium lots | 7 (block 3775, lots 172–178), all addressed 181 South Park | SF Assessor secured roll 2025, DataSF parcels |
| Floor area | 15,516 sq ft total across the seven lots (8,631 commercial + 6,885 residential) | SF Assessor secured roll 2025 |
| Construction cost | $2,300,000 | permit 200005099501 |
| Roof | **unoccupied** — a roof deck was designed and then removed by revision | permit 200108166212 "change roof deck to unoccupied roof" |
| Garage | exits to Varney Place at the SE end | permit 200211131341 "exit from garage to varney" |
| Block / lot | 3775 / 172 (map block lot) | SF Assessor, DataSF parcels, DataSF footprint `mblr = SF3775172` |
| Footprint | 43.31 m x 13.85 m, 599.9 m2, a plain rectangle at bearing 135.2° | OSM way/124889463, reprojected — **measured** |
| DataSF footprint (cross-check) | 42.35 x 13.66 m OBB, 535.3 m2 polygon | DataSF LiDAR footprint SF3775172 — agrees within ~1 m per side; its 42 vertices are LiDAR edge jitter on the same rectangle |
| Roof form | ridged standing-seam metal roof, ridge along the long NW–SE axis, running most of the length; sloped/hipped toward the NW end | Vexcel 2026 aerial imagery — **observed**; barrel vs low gable unresolved, see 2.15 |
| Roof ridge height | 16.54 m above ground | DataSF LiDAR `hgt_maxcm` — **measured** |
| Median / modal roof height | 14.18 m (median), 14.28 m (majority of cells) | DataSF LiDAR — **measured**; on a ridged roof these are mid-slope values, not the eave and not the ridge |
| Eave height | ~11.8 m | **derived**: a symmetric ridged roof gives a height distribution roughly uniform between eave and ridge, so eave ≈ 2 × median − ridge = 2(14.18) − 16.54 = 11.82 m. Consistent with the modal 14.28 m. Not measured — see 2.15 |
| Ground elevation | 6.84 m (NAVD88) | DataSF LiDAR `gnd_min_m` — app terrain handles this, not the asset |
| Height above neighbours | ~5 m: 171 South Park 11 m, 167 unknown, 159 5 m, Shell canopy 4 m, 147 12 m | OSM `height` tags on the neighbouring ways |
| Notable occupant | Instagram, 2012 — the office they were in when Facebook announced the acquisition on 9 April 2012 | Getty Images news photo, 9 April 2012; commercial listing copy |
| Zoning | SPD (SoMa — South Park) | DataSF parcels |
| Architect | not recorded in any source consulted | — |

### 2.2 Sources

- https://www.openstreetmap.org/way/124889463 — footprint rectangle, address, `height=14`
- `https://data.sfgov.org/resource/ynuv-fyni` (DataSF Building Footprints, LiDAR-derived) — cross-check footprint and the 14.18 m / 16.54 m heights
- `https://data.sfgov.org/resource/acdm-wktn` (DataSF Parcels) — the seven 181 South Park condo lots, zoning
- `https://data.sfgov.org/resource/wv5m-vpq2` (SF Assessor Historical Secured Property Tax Rolls) — 2002 build year, per-unit use and floor area
- `https://data.sfgov.org/resource/i98e-djp9` (SF Building Permits) — the 2000 four-storey five-unit construction permit, the demolition it replaced, the roof-deck-to-unoccupied-roof revision, the Varney garage exit, the ground-floor change of use, and the 2006–2022 four-storey record
- https://www.gettyimages.com/detail/news-photo/instagrams-new-office-is-seen-at-181-south-park-avenue-on-news-photo/142617135 — Instagram at this address, 9 April 2012
- Commercial and residential listing copy (Zillow, Redfin, Homes.com "Park 181", ApartmentList) — 5 loft units, 2002, "arched hardwood high ceilings", "towering steel-framed windows", downtown skyline views, former Instagram offices
- Bing Maps satellite, Vexcel 2026 imagery, nadir, ~0.1 m/px — the only imagery consulted:
  the ridged metal roof, its ridge line and hipped NW end, the roof monitors and the
  mechanical grouping. Street-level and oblique imagery were **not** available

### 2.3 Orientation and placement

The lot runs the full depth of the block, from the south-west rim of the South Park oval
back to the Varney Place alley. It shares its north-east long wall with 171 South Park;
its south-west long wall faces the open forecourt of the Shell station on Third Street and
is therefore an exposed elevation, not a party wall.

Measured distances from the footprint edge: the South Park sidewalk 1.9 m off the NW end,
the South Park roadway centreline 10.6 m, the park boundary 15.1 m; Varney Place 2.7 m off
the SE end.

The footprint is a clean rectangle. OSM way/124889463 records it with eight nodes, but six
of them are collinear — the real shape is four corners:

Rectangle corners in Blender coordinates (metres, `+X` east, `+Y` north),
centred on the anchor `-122.3945113, 37.7807582`:

```
( -20.255,  10.322)   NW corner, west side
( -10.443,  20.082)   NW corner, north side
(  20.250, -10.327)   SE corner, east side
(  10.438, -20.088)   SE corner, south side
```

in ring order: `(-10.443, 20.082) → (-20.255, 10.322) → (10.438, -20.088) → (20.250, -10.327)`.

Edges, with outward normals:

| Edge | Length | Faces | Elevation |
|---|---|---|---|
| `(-10.443,20.082) -> (-20.255,10.322)` | 13.85 m | NW 315.2° | **South Park front** |
| `(-20.255,10.322) -> (10.438,-20.088)` | 43.31 m | SW 225.2° | **exposed south-west flank** |
| `(10.438,-20.088) -> (20.250,-10.327)` | 13.85 m | SE 135.2° | **Varney Place end (garage)** |
| `(20.250,-10.327) -> (-10.443,20.082)` | 43.31 m | NE 45.2° | north-east flank, party wall with 171 |

Because of the 45° heading the axis-aligned bounding box is ~40 x 40 m. That is correct.

### 2.4 What each side shows

**Top** is observed from aerial imagery. **The four elevations are not observed** — they
are the most probable reading of a 2002 SoMa live/work loft building given the permit
record, the programme and the neighbourhood, and they exist so that stage 2 has something
specific to confirm or overturn.

**Northwest (South Park front)** — The address elevation and the only one the park sees:
13.85 m wide and 16.5 m tall, so a distinctly vertical face. Expect a ground-floor
commercial storefront (the 8,631 sq ft commercial condo) with a large glazed shopfront and
a separate recessed residential entry door, then three loft levels of tall steel-sash
windows — the listings' "towering steel-framed windows", probably two wide bays per floor
on a face this narrow. This is the face that would carry the street number.

**Southeast (Varney Place end)** — The service end. A vehicle garage door (permits confirm
the garage exits here), a pedestrian exit door, and a plainer, more closed upper wall than
the park front. Alleys in SoMa are working faces.

**Southwest flank** — 43 m long, four storeys, and *exposed*: the Shell station forecourt
means there is no neighbour against it. Expect the building's main window rhythm here —
a long regular run of loft windows, probably with a lightwell or setback somewhere along
its length, because a 43 m deep floor plate cannot be lit from its two ends alone. From
the app's aerial camera this is the largest single surface the asset presents.

**Northeast flank** — Party wall against 171 South Park for most of its length, so in the
real world it is largely blind and only its upper storey clears the neighbour's 11 m roof.
The app's camera sees it plainly from the north-east, so it must be built as a finished
wall with a sparse, honest window scatter in the part that clears 171 — not a full grid,
and not a blank slab either.

**Top — observed.** Not a flat roof. A light-grey **standing-seam metal roof, ridged along
the building's long NW–SE axis**, with the seams running across the width and a clear ridge
line carried most of the length; it slopes or hips down toward the NW (South Park) end
rather than ending in a flat gable wall. Sitting on it: two or three raised roof
monitors / skylight boxes along the ridge, a white cylindrical or box plant unit and a
group of darker mechanical units in the SE (Varney) third, and what appears to be a lower,
flatter roof section at the extreme Varney end. No roof deck (permit 200108166212), so no
railings, planters or paving. This is the most-seen surface in the app, it is 43 m long,
and it is the building's strongest single feature from the air — every other roof on this
side of the oval is flat.

### 2.5 Recognition cues (ranked)

1. **The proportion** — a 43 x 13.8 m slab, 3.1:1, running the whole depth of the block
   from the park to the alley. Nothing else on this side of South Park is shaped like it.
2. **The long ridged metal roof** — the only non-flat roof on this side of the oval, and
   the cue the app's aerial camera will actually read.
3. **The extra storey** — four storeys where the neighbours are two and three, standing
   about 5 m proud of the roofline on both sides.
4. Tall steel-sash loft windows in a regular bay rhythm along the long flanks.
5. Ground-floor commercial storefront on the park end; garage door on the alley end.

### 2.6 Miniature translation

**Preserve**

- The 3.1:1 slab proportion and the real 135.2° heading, exactly
- The ridged roof running the full length, and its seam direction across the width
- The four-storey height standing proud of the neighbours — this is what makes it findable
- The two-different-ends story: shopfront and entry at the park, garage at the alley
- The long flanks' window rhythm as a rhythm, not as individual windows

**Simplify / exaggerate**

- The real window count on each 43 m flank becomes ~10 identical bays, all the same size
- Steel sashes become a single chunky frame band per opening; no mullion grids
- The storefront becomes one wide glazed opening plus one recessed entry, not a shopfitted
  facade
- Roof clutter becomes a small, composed set: two HVAC blocks, one vent cluster and two
  roof monitors on the ridge
- The metal roof's seams become a low-frequency rhythm or nothing at all — do not model
  individual standing seams, they are far below a pixel
- The roof's rise is the one place semantic exaggeration is spent: the real ridge is a
  shallow 4.7 m over a 13.85 m span, and it may need a little help to read from the air.
  Push it if the aerial render demands it, but the ridge must still land on 16.5 m — take
  the exaggeration out of the eave line, not out of the target height, and record it

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not
a straitjacket — adjust after the first aerial review render, and after the 2.15
barrel-versus-gable question is settled.

1. Body: extrude the 2.3 rectangle from z=0 to the eave line z=11.8, `Toy_stone`.
2. Ground floor, z=0 to z=4.0: on the NW end, one 6.0 m wide glazed storefront and one
   1.4 m recessed residential entry; on the SE end, one 3.6 m garage door (`Toy_ink`) and
   one 1.0 m pedestrian door; on the SW flank, two or three small openings only.
3. Floor band: 0.18 m `Toy_trim` course at z=4.0, carried around all four faces — it is
   what separates the commercial base from the lofts at a glance.
4. Wall levels, two of them, z=4.6 to z=11.5: on each long flank, 10 bays of
   1.5 x 2.6 m openings recessed 0.18 m, `Toy_glass`, with a 0.12 m `Toy_steel` frame band.
   On the NW end, 2 bays per floor, same size. On the NE flank, use the same rhythm but
   only above z=11 (below that it is a party wall against 171) — below, leave it blind.
5. Eave: a 0.3 m `Toy_trim` fascia band at z=11.5 to z=11.8, all four faces.
6. **Roof, z=11.8 to z=16.5** — the top-floor lofts live inside it, which is what the
   listings' "arched hardwood high ceilings" describes. Its section depends on 2.15:
   - barrel: a 10-to-12-segment arc spanning the 13.85 m width, springing at z=11.8 and
     crowning at z=16.5;
   - low gable: two straight slopes from z=11.8 to a ridge at z=16.5 (a ~34° pitch).

   Either way it runs the full 43.31 m length, `Toy_steel` (light grey standing-seam),
   with the NW end sloped or hipped down rather than closed by a flat gable wall, and the
   ridge must land exactly on 16.5.
7. Dormer glazing: on each long roof slope, 4 flush glazed panels 1.6 x 1.2 m, `Toy_glass`,
   in line with the wall bays below — this is what lights lofts that sit inside a roof, and
   it gives the night state somewhere to live above the eave.
8. Roof furniture: two roof monitors on the ridge (2.4 x 1.4 x 0.5 m, `Toy_glassl`), one
   HVAC pair (2.2 x 1.6 x 0.9 m and 1.6 x 1.2 x 0.7 m, `Toy_steel`) and one vent cluster,
   all grouped in the SE third as observed.
9. Bevel 0.12 m, 2 segments.

### 2.8 Materials and palette — *inferred, confirm from photography*

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_stone` | `#d9d2c2` | main body walls |
| `Toy_trim` | `#f3efe6` | floor band, eave fascia, entry surround |
| `Toy_glass` | `#2a4d73` | loft windows, roof glazing and storefront glazing |
| `Toy_glassl` | `#6f95b8` | roof monitors (lighter, reads as up-facing glazing) |
| `Toy_steel` | `#9aa0a6` | **the standing-seam metal roof** (observed light grey), window frame bands, HVAC blocks |
| `Toy_roofd` | `#45454a` | the lower roof section at the Varney end, if it is confirmed |
| `Toy_ink` | `#3a3530` | garage door, door recesses |
| `Toy_glass_Glow` | `#2a4d73` | lit loft windows at night |
| `Toy_trim_Glow` | `#f3efe6` | storefront spill at the park end |

The body colour is the single largest unknown in this plan. `Toy_stone` is a safe neutral
that will sit correctly next to the neighbourhood's palette, but a 2002 SoMa loft building
is as likely to be a warmer stucco (`Toy_sand`, `#ece4d4`) or to carry a metal-panel
element. Decide from photography, and if the real building has a signature accent colour,
say so in `REPORT.md` and spend one palette slot on it — this plan deliberately does not
invent one.

**Night state (required).** Glow surfaces must be thin shells proud of the opaque glazing —
the app renders `_Glow` in a separate layer that is ~12% alpha by day, so a primary surface
must never be authored as glow. Hero glow: a scatter of lit windows on the exposed
south-west flank, where the long rhythm reads best — five or six of the twenty, not all —
plus one or two of that flank's roof glazing panels, which is the payoff for putting lofts
inside the roof. Supporting accent: the storefront glazing at the South Park end. The
north-east flank stays dark below 11 m (it is a party wall) and the alley end stays dark
entirely; a service alley that glows would misread. The metal roof itself does not glow.

### 2.9 Top surface

43 x 13.8 m of ridged standing-seam metal roof rising from an ~11.8 m eave to a 16.5 m
ridge, in a district the camera flies over constantly. This is the asset's best feature and
the composition problem is restraint, not invention: the ridge does the work, so the
furniture should stay quiet and grouped where it was observed — monitors on the ridge, the
mechanical cluster in the SE third, nothing scattered down the middle. Keep the roof value
clearly lighter than the walls so the ridge line reads as a highlight from above, which is
how it reads in the real aerial. No deck furniture — the roof-deck permit was revoked by
revision in 2001, and railings or planters would be a fabrication.

### 2.10 Scope

**In the GLB:** the single 2002 loft block — body, all four elevations' openings, storefront
and residential entry, garage door, eave fascia, the ridged roof with its glazing, and the
roof furniture

**Not in the GLB:** South Park, its trees or lawn, Varney Place, 171 South Park, the Shell
station, the sidewalk, vehicles, people, plinths, cameras or lights

### 2.11 Triangle budget

Cap 9,000 — a secondary building, and the cap should bind. Suggested split: body, eave and
floor band ~1.5k; the two 10-bay flanks ~3k; the NW end's storefront, entry and bays ~1.2k;
the SE end's garage and door ~0.5k; the roof shell ~1.5k; roof glazing and furniture ~1.3k.

Two places this budget can run away. The long flanks: keep each bay to a simple recessed box
with one frame band — twenty bays of a fussy window will not fit and will not read. And the
roof, if it is a barrel: a 43 m sweep at 12 segments with a bevel is already ~1.5k
triangles, and going to 20 segments to make the curve smoother buys nothing at the app's
camera distance while costing most of the flanks' budget.

### 2.12 Draft manifest entry

```json
{
  "id": "181-south-park",
  "file": "181-south-park.glb",
  "anchor": [
    -122.3945113,
    37.7807582
  ],
  "targetHeightM": 16.5,
  "cat": 2,
  "name": "181 South Park",
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

- **New landmark.** Add a `pipeline/lib/landmarks.mjs` entry (`id: '181-south-park'`,
  `lon: -122.3945113`, `lat: 37.7807582`, `height: 16.5`, `exclude: 5`) and re-bake the
  affected tiles, or the baked procedural building on this exact footprint will intersect
  the GLB.
- **The exclusion radius has an unusually narrow safe window, and 5 is near its middle.**
  `excluded()` in `pipeline/buildings.mjs` drops a procedural footprint when its centroid
  *or any of its ring vertices* falls inside the radius, so the constraint is two-sided.
  Measured against the anchor above:

  | | trigger distance |
  |---|---|
  | 181 South Park's own footprint (via its centroid) | **2.02 m** |
  | 171 South Park (nearest ring vertex — a shared party-wall node) | **7.00 m** |
  | the Shell canopy at 551 (nearest ring vertex) | 9.17 m |
  | 167 South Park | 12.32 m |

  Anything in `(2.1, 7.0)` clears this building and keeps its neighbours. Below ~2.1 the
  procedural slab survives and pokes through the model; at or above 7.0 the re-bake punches
  a hole where 171 South Park should be. `exclude: 5` leaves ~3 m of tolerance for the
  difference between these OSM rings and the Overture footprints the pipeline actually
  bakes from — but that difference is exactly the risk, so **verify with `pipeline/audit.mjs`
  check 1.6 after the re-bake** and confirm visually that 171 is still standing before
  committing.
- `loadRadius`: the skill's default formula gives `max(2500, 16.5 * 30) = 2500` m. Take the
  default. Beyond it the site is a gap rather than a procedural stand-in, but at 2.5 km a
  16 m building is far below a pixel.
- This is the second South Park-area building in the landmark manifest after 380 Brannan,
  and the same question applies: a manifest of one-off SoMa blocks will not stream well
  forever. If the intent is to keep doing individual buildings around this oval, the
  kit/instancing route (`KIT-INTEGRATION-PROMPT.md`) is the better long-term home for
  buildings of this class.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Bounding-box top exactly 16.5 m — the roof ridge, not a roof monitor (loader scale lands at 1.0)
- [ ] Dimensions plausible in meters and consistent with 2.1 (XY bbox ~40 x 40 m is expected)
- [ ] The slab is still 3.1:1 in plan — measure it, do not eyeball it
- [ ] Triangles at or under 9,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the lit loft windows, the roof glazing and the storefront; glow shells proud of opaque glazing
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (per-object signed volume for the union of solids; ray test residual <= 0.15%)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + contact sheet + night render regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed
- [ ] The 2.15 barrel-versus-gable question answered in `REPORT.md`, with the source that answered it
- [ ] The eave line either measured or, if it stayed derived, said so plainly in `REPORT.md`

### 2.15 Open questions and risks

- **Barrel or low gable? Resolved: gable.** Settled during stage 2 from the LiDAR
  height distribution rather than from imagery, and worth recording because the
  method generalises. A roof's height distribution over its footprint has a shape
  set by its section, so the gap between the median height and the maximum
  identifies the section: a straight gable puts the median at half the rise, a
  parabolic arc at 0.75 of it, a circular barrel at 0.866. Working backwards from
  the measured median (14.18 m) and ridge (16.54 m), the implied eave is 11.82 m
  for a gable, 7.10 m for a parabola and −1.07 m for a circle. A curved roof
  drags the median toward the crown, so only the straight slope closes on a
  possible eave for a four-storey building. The listings' "arched hardwood high
  ceilings" is an interior ceiling hung inside that roof, not the roof's section
  — both facts hold at once.
- **The eave line is derived, not measured.** ~11.8 m comes from treating the LiDAR height
  distribution as uniform between eave and ridge (2 × 14.18 − 16.54). That is a sound model
  for a symmetric ridged roof and it is corroborated by the modal 14.28 m, but it is
  arithmetic, not observation, and it drives the whole storey layout in 2.7: it implies two
  full storeys of wall above the commercial ground floor with the top-floor lofts living
  inside the roof. If the eave is really at 13 m, the building has three wall storeys and a
  shallower roof, and 2.7 is wrong. One street-level photograph settles it.
- **A low element probably exists at the Varney end.** LiDAR mean 13.15 m against median
  14.18 m and minimum 0.04 m says roughly a sixth of the footprint sits well below the main
  roof, and the aerial shows what looks like a lower flat roof section at the extreme SE
  end. Other candidates that would change the massing more: a lightwell breaking the 43 m
  depth, or LiDAR shadow cast by 171 South Park along the party wall. Confirm which.
- **OSM `height=14` is neither eave nor ridge.** It matches the LiDAR median almost exactly,
  which makes it look trustworthy — the same trap the plans README documents, and worse
  here, because on a ridged roof the median is a mid-slope value that corresponds to no
  physical line on the building at all. The ridge is 16.5 m.
- **The assessor roll cannot be used for storeys here.** It records the seven condominium
  lots separately at 0, 1 and 2 storeys each; none of those is the building. The 2000
  construction permit and every permit since say four.
- **The four elevations in 2.4 and the palette in 2.8 are unverified.** Only nadir aerial
  imagery was available to the author, so the roof is observed and nothing below it is.
  Facade material, colour, window rhythm, bay count, and whether there is a signature
  accent are all open. The one wall colour with any evidence behind it is the roof's, and
  that is the roof.
- The 10-bay flank rhythm is a proportion guess (43.31 m / 10 ≈ 4.3 m centres, which is a
  plausible loft bay) and nothing more.
- No architect is recorded for the 2002 building in any source consulted, so there is no
  design-intent document to check the reading against.
- The Instagram association is well sourced for April 2012 and is worth carrying in the
  building's card copy, but it must not become a visual instruction — there is no reason to
  think the building looked different then, and nothing about it should be styled to
  reference the tenant.
