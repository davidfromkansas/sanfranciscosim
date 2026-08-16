# 188 South Park — SF-SIM asset plan

A 2002 four-storey live/work loft building on the north rim of the South Park
oval, designed by award-winning architect Adele Santos (Santos-Prescott) and
developed by Prism Capital on a former gas station site. Twelve units of
high-end live/work space with soaring 16+ ft floor-to-ceiling windows, a
penthouse with a private rooftop terrace, and a through-lot that runs from
the South Park frontage back toward 3rd Street with a wind-protected patio at
the rear. It is one of the taller buildings on the oval — about 4 m proud of
its two- and three-storey neighbours — and its contemporary stucco-and-stone
facade with its tall window grid is what makes it findable from above.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/188-south-park/`. This document is the plan only: Part 1 is the runnable task
prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `188-south-park` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3950794, 37.7810118` (DataSF LiDAR footprint area centroid, measured) |
| Target height | **15.93 m** to the architectural crest (penthouse/roof terrace parapet); main roof ~13.3 m (LiDAR-derived, see 2.1) |
| Footprint | 23.7 m (wide, NE–SW) x 16.1 m (deep, NW–SE); 381 m2, measured — a rectangle at bearing 45°/225° |
| Triangle cap | 9,000 |
| Category | `2` (apartments — live/work lofts) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 188 South Park GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of 188 South Park in San Francisco and deliver it
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
7. `artifacts/181-south-park/` — the closest reference implementation in scale,
   character and neighbourhood (the live/work loft building on the opposite rim
   of the same oval, by a different architect four years later). Take its detail
   budget, its facade discipline and its window rhythm; note that its roof is
   ridged metal while this one is flat with a penthouse, so take its massing
   approach, not its roof approach
8. `docs/asset-plans/188-south-park.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Photo research is a hard gate on this one — do it before you model

The dossier below is strong on geometry and programme, has LiDAR heights, and is
weak on street-level appearance: no street-level photography could be consulted
while it was written. The roof form (2.4 "Top", 2.9) was read from LiDAR height
distributions and Bing aerial imagery and is reliable in form; the four
*elevations* in 2.4 and the palette in 2.8 are *inferred* from the architect's
known work, the permit record, the listing copy and the neighbourhood, and must
be replaced with observed fact before you build anything.

What you must still settle from imagery, in priority order:

1. **The facade material and colour.** The permit says "stone, stucco" and the
   architect is Santos-Prescott (Adele Santos), but the exact colour, the
   balance of stone and stucco, and whether there is a signature accent are
   unverified. A 2002 Santos-Prescott loft building is most likely a warm
   stucco with a stone base, but confirm from photography.
2. **The window rhythm and bay count.** The dossier's 4-bay reading on the long
   flanks is *inferred* from the 23.7 m width and the 16+ ft window claim; the
   real count and grouping must be observed.
3. **The penthouse/roof terrace element.** The LiDAR max of 15.93 m against a
   median of 13.34 m implies a ~2.6 m penthouse or parapet, and the listing
   confirms a "private rooftop terrace" on the penthouse unit. Confirm its
   form, position and extent from aerial imagery.
4. **The lower element at 6.35 m** (2.15), which the LiDAR minimum hints at but
   does not explain — a canopy, an awning, or a step in the building.

Record what you found and how in `REFERENCE.md` and `REPORT.md`.

## Must capture

- The **proportion**: a 23.7 m x 16.1 m block on the north rim of the South Park
  oval, wider than it is deep, running along the rim rather than across it
- Four storeys, standing ~4 m proud of the two- and three-storey neighbours
- Tall floor-to-ceiling loft windows in a regular bay rhythm on all faces — the
  listings' "soaring 16+ feet floor-to-ceiling windows"
- A ground-floor commercial/live-work base (State Farm office, per the geocode)
- The penthouse/roof terrace element that lifts the crest to 15.93 m — the
  building's strongest single feature from the air
- A deliberately designed roof — the camera looks down and this is a flat roof
  with a terrace, not a blank slab

## Research 188 South Park independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- All four elevations. Note that two of them are *ends*: the 16.1 m wide SE face
  onto South Park and the 16.1 m wide NW face toward 3rd Street/the patio. The
  long faces are the 23.7 m flanks running NE-SW along the rim.
- Aerial and roof views at higher resolution than 2.4 could reach — this is
  where the penthouse/roof terrace form gets settled
- Ground-level views from South Park and from 3rd Street, which is where the
  facade material, window rhythm and ground-floor treatment get settled
- Day and night appearance
- The bay count and window rhythm of the long flanks — the dossier's 4-bay
  reading is *inferred* and is the weakest number in it
- The facade material and colour, which the dossier infers from the permit and
  the architect but does not observe

Prefer architect/engineer publications, owner or institutional material,
planning and permitting documents, architectural press, geolocated photography,
and aerial/satellite imagery. Never rely on a single photograph, a single
AI-generated image, or a single unsourced 3D model. Separate verified facts from
visual inference; if sources disagree, document the disagreement and decide.

**One source conflict is already known — re-check it, do not silently
re-inherit the wrong value:** the 2018 kitchen remodel permit records
`number_of_proposed_stories = 5`, while the 1998 new-construction permit and
every other permit say 4. The 2018 figure may reflect a penthouse mezzanine
that was added or regularised, or it may be a clerical error. The LiDAR max
of 15.93 m against a median of 13.34 m is consistent with a penthouse on a
4-storey building, not a 5-storey one. Treat the building as 4 storeys with
a penthouse unless photography proves otherwise.

## Create a reference dossier

Write `artifacts/188-south-park/REFERENCE.md` containing: source links and what each
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
one identity cue carried hard — the tall window grid and the penthouse that lifts
the building above its neighbours. Resist adding hero-tier ornament.

The finished asset must be immediately recognizable as 188 South Park, consistent with
the real building from all four sides and above, architecturally credible, and a
premium handcrafted miniature — not photorealistic, not voxel art, not generic
low-poly, and never accurate in one view while invented in the others.

## Scope of the exported asset

Export the single 2002 loft block: body, all four elevations' openings, the flat
roof, the penthouse/roof terrace element, and the ground-floor commercial front.

Do not include unrelated surrounding city geometry: South Park itself, the park's
trees or lawn, 3rd Street, the patio (it is on the lot but outside the building
footprint), 166-168 South Park next door, the sidewalk, parked cars, people,
plinths, cameras or lights. Temporary context may appear in review renders but
must not leak into the GLB.

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
(`placeGeneric` in `app/src/assets.js` only scales and positions). The South Park
entrance faces **southeast, bearing 135°**; the building's long axis runs
45°/225° (NE-SW), so build directly on the measured footprint rectangle in 2.3
rather than modelling an axis-aligned box and rotating it. The contract's "front
faces −Y" cannot be honoured literally here; real-world orientation wins
(AGENTS rule 5) and the deviation goes in `REPORT.md`.

**Height normalization:** the tallest geometry in the export (the penthouse/roof
terrace parapet) must land at exactly **15.93 m** so the loader's
`targetHeightM / measuredHeight` scale is 1.0.

## Reproducible Blender workflow

Blender 5.2 LTS. Headless: `blender -b --python script.py -- args`.

Keep `artifacts/188-south-park/build_188_south_park.py` (deterministic build script),
`artifacts/188-south-park/188-south-park.blend`, and
`artifacts/188-south-park/188-south-park.glb`. The script must rebuild the model reliably
enough for future revision. Do not modify or rename an unrelated existing GLB to satisfy
the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`188-south-park-top.png`, `188-south-park-north.png`, `188-south-park-east.png`,
`188-south-park-south.png`, `188-south-park-west.png`, plus
`188-south-park-contact-sheet.png`, at least one high three-quarter aerial beauty render
`188-south-park-aerial.png`, and a night render `188-south-park-aerial-night.png`.

The four elevations must share scale, framing, lighting, exposure and
projection; use orthographic or long-lens cameras; label directions from the
researched orientation; the top view must clearly show the full 23.7 m roof —
its penthouse, its terrace and its mechanical layout; the aerial view uses the
style bible's camera assumptions (30-50 degrees down, long lens). Simple tabletop
lighting, neutral warm background, minimal depth of field, and every image must
depict the same exported model.

Because the building is rotated ~45° from the world axes, the four compass renders will
each show two faces at 45°. That is correct and expected — do not rotate the model to make
the elevations square on.

## Validate the exported GLB

Re-import `188-south-park.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture
count, camera count, light count, animation count, applied-transform status,
negative-scale status, normal-orientation status, unexpected geometry, and
per-material contract compliance. Render at least one review image from the
re-imported asset. Write `artifacts/188-south-park/validation.json` and
`artifacts/188-south-park/REPORT.md`.

Note that the axis-aligned XY bounding box will be roughly **28 x 28 m** even though the
building is 23.7 x 16.1 m — that is the expected consequence of a ~45° real-world heading,
not a scale error.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "188-south-park",
  "file": "188-south-park.glb",
  "anchor": [
    -122.3950794,
    37.7810118
  ],
  "targetHeightM": 15.93,
  "cat": 2,
  "name": "188 South Park",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a separate, explicitly requested job — run `docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in `docs/asset-plans/188-south-park.md`.
````

---

## Part 2 — Research and design dossier

Compiled 14 August 2026 from the sources in 2.2. Values marked *inferred* are visual or
derived estimates, not published figures — the executing agent must re-verify
anything it relies on.

**A warning specific to this dossier.** Its evidence is uneven and it says so line by line.
Everything geometric is measured from survey data (OSM, DataSF LiDAR, DataSF parcels) and
is solid. The **roof form** was read from the LiDAR height distribution and Bing Maps
aerial imagery and is an observation. Everything at street level — facade material, colour,
window rhythm, bay count, ground-floor treatment — is inference from the permit record,
the architect's known work, the listing copy and the neighbourhood, because no street-level
imagery could be reached from the authoring session: Google Maps and Street View were
blocked and no open substitute covered the block. The four elevations in 2.4 and the palette
in 2.8 are hypotheses, not observations. Treat street-level photo research as gate zero of
stage 2.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Built | 1999–2002; construction permit issued 20 Oct 1999, HOA filed 10 Aug 2001, completed ~2002 | SF building permit 9823199S; CA Secretary of State filing 2354555 |
| Storeys | **4** (with a penthouse/roof terrace) | permit 9823199S "erect a four story twelve unit live work bldg"; every permit 2005–2023 records 4 storeys; the 2018 permit says 5 — see 2.15 |
| Programme | 12 artist live/work loft units | permit 9823199S `proposed_use = artist live/work`, `proposed_units = 12` |
| Construction | wood frame (Type V) | permit 9823199S `proposed_construction_type_description = wood frame (5)` |
| Exterior materials | stone, stucco | Compass listing `Construction Materials: Stone, Stucco` — **not independently verified from photos** |
| Architect | Santos-Prescott (Adele Santos) | Compass listing "designed by award-winning architect Adele Santos"; Curbed SF (7 Sep 2010) "designed by Santos-Prescott" |
| Developer | Prism Capital (Jeff Handwerger) | Prism Capital portfolio page |
| Former site use | gas station, environmentally cleaned with a Superfund grant | Prism Capital portfolio page |
| Condominium lots | 12 units on APN 3775-132 (mapblklot 3775125) | SF Assessor, DataSF parcels |
| Floor area | ~16,800 sq ft (12 units × ~1,400 sq ft) | Compass listing 1,456 sqft for a 3-level unit; *inferred* total |
| Construction cost | $1,200,000 (estimated), $1,400,000 (revised) | permit 9823199S |
| Sale prices | $800,000–$1,200,000; ~$1,000/sqft | Prism Capital portfolio; Curbed SF |
| Block / lot | 3775 / 132 (mapblklot 3775125) | SF Assessor, DataSF parcels |
| Through-lot | 188 South Park (SE front) / 549 3rd St (NW rear) | DataSF parcels `from_address_num=549, street_name=03RD`; Compass "private entrance from 3rd street" |
| Footprint | 23.7 m (wide, NE–SW) x 16.1 m (deep, NW–SE), 381 m2, rectangle at bearing 45°/225° | OSM way/124884339, reprojected — **measured** |
| DataSF footprint (cross-check) | 23.8 m wide matches OSM; depth inflated to 28.1 m by 42-vertex LiDAR edge jitter | DataSF LiDAR footprint SF3775125 — width agrees, depth overestimated |
| Parcel | 27.4 m x 23.1 m, 634 m2 — the building fills the lot width (23.7 vs 23.1 m) but only 16.1 m of the 27.6 m depth; the remaining ~11.5 m is the patio/courtyard toward 3rd St | DataSF parcels acdm-wktn — **measured** |
| Roof form | flat roof at ~13.3 m with a penthouse/roof terrace element reaching 15.93 m | LiDAR height distribution + Bing aerial — **observed from above** |
| Roof crest height | 15.93 m above ground | DataSF LiDAR `hgt_maxcm = 1593` — **measured** |
| Median roof height | 13.34 m (median), 13.59 m (mean) | DataSF LiDAR `hgt_mediancm = 1334`, `hgt_meancm = 1359` — **measured** |
| Minimum height | 6.35 m | DataSF LiDAR `hgt_mincm = 635` — possibly a canopy, awning, or lower section; see 2.15 |
| Height std dev | 1.40 m | DataSF LiDAR `hgt_stdcm = 140` — moderate, consistent with a flat roof + penthouse |
| Ground elevation | 6.03 m (NAVD88) | DataSF LiDAR `gnd_min_m` — app terrain handles this, not the asset |
| Height above neighbours | ~4 m: 166-168 South Park ~10.4 m (DataSF SF3775070), 164 South Park 5 m (OSM), 521-527 3rd St 11 m (OSM) | DataSF LiDAR + OSM `height` tags |
| Notable feature | penthouse with private rooftop terrace | Curbed SF (7 Sep 2010) "private rooftop terrace"; Compass listing |
| Notable feature | wind-protected patio at the rear (toward 3rd St) | Compass listing "peaceful & well-appointed, wind-protected patio in the back" |
| Notable feature | private entrance from 3rd Street (at least one unit) | Compass listing "its own private entrance from 3rd street" |
| Notable feature | 16+ ft floor-to-ceiling windows | Compass listing "soaring 16+ feet floor-to-ceiling windows" |
| Zoning | CMUO (Central SoMa Mixed Use Office) | DataSF parcels — was SLI when built |
| Neighbourhood | Financial District/South Beach (Rincon/South Beach) | DataSF parcels, LoopNet |

### 2.2 Sources

- https://www.openstreetmap.org/way/124884339 — footprint rectangle, no height tag
- `https://data.sfgov.org/resource/ynuv-fyni` (DataSF Building Footprints, LiDAR-derived) — footprint SF3775125, heights 15.93 m / 13.34 m / 6.35 m
- `https://data.sfgov.org/resource/acdm-wktn` (DataSF Parcels) — parcel 3775-132, through-lot 549 3rd St / 188 South Park, zoning CMUO
- `https://data.sfgov.org/resource/i98e-djp9` (SF Building Permits) — the 1998 four-storey twelve-unit live/work construction permit, the 2005 interior alterations, the 2018 kitchen remodel (5 storeys — see 2.15), the 2023 fire alarm upgrade
- https://www.prismcapitalsf.com/portfolio/188-south-park/ — developer's project page: 12-unit high-end live/work loft on a former gas station site, Superfund cleanup
- https://sf.curbed.com/2010/9/7/10504628/your-own-private-rooftop-terrace-in-south-park — penthouse loft with private rooftop terrace, designed by Santos-Prescott
- https://www.compass.com/listing/188-south-park-street-unit-6-san-francisco-ca-94107/ — 3-level live/work condo, architect Adele Santos, 16+ ft floor-to-ceiling windows, stone/stucco construction, private entrance from 3rd St, wind-protected patio, 12 units built 2002
- https://www.bizprofile.net/ca/san-francisco/south-park-lofts-homeowners — South Park Lofts HOA, filed 10 Aug 2001
- https://www.loopnet.com/property/188-s-park-st-san-francisco-ca-94107/ — APN 3775-132, mixed-use, 0.16 AC
- https://openpermitdata.com/sf/address/188-south-park — permit history (14 permits since 2017)
- Bing Maps satellite, Vexcel 2026 imagery, nadir — the roof form, the penthouse position, the flat roof. Street-level and oblique imagery were **not** available

### 2.3 Orientation and placement

The building sits on the north rim of the South Park oval, facing southeast onto
the park. The lot is a through-lot that runs from the South Park frontage (SE)
back toward 3rd Street (NW), with a wind-protected patio occupying the rear
~11.5 m of the lot between the building and 3rd St. The building fills the lot
width (23.7 m vs the parcel's 23.1 m — essentially the same) but only 16.1 m of
the lot's 27.6 m depth.

The footprint is a clean rectangle. OSM way/124884339 records it with six nodes,
one of which is collinear — the real shape is four corners:

Rectangle corners in Blender coordinates (metres, `+X` east, `+Y` north),
centred on the anchor `-122.3950794, 37.7810118` (DataSF LiDAR footprint area
centroid — chosen because it opens the widest exclusion window, see 2.13):

```
( -3.6,  11.3)   SE corner, south side  (South Park front)
(  7.5,  -2.5)   SE corner, east side
(-11.3,  -3.6)   NW corner, west side   (3rd St / patio rear)
( -7.5,   7.5)   NW corner, north side
```

in ring order: `(7.5, -2.5) → (-3.6, 11.3) → (-7.5, 7.5) → (-11.3, -3.6)`.

Edges, with outward normals:

| Edge | Length | Faces | Elevation |
|---|---|---|---|
| `(7.5,-2.5) -> (-3.6,11.3)` | 16.1 m | SE 135.0° | **South Park front** |
| `(-3.6,11.3) -> (-7.5,7.5)` | 5.0 m | NE 45.0° | NE flank (short) |
| `(-7.5,7.5) -> (-11.3,-3.6)` | 23.7 m | NW 315.0° | **3rd St / patio rear** |
| `(-11.3,-3.6) -> (7.5,-2.5)` | 18.8 m | SW 225.0° | SW flank (long) |

*Correction:* the rectangle is 23.7 m x 16.1 m but the edges above don't reflect
that cleanly because the OBB center and the rectangle corners need to be computed
from the actual OSM geometry, not estimated. The executing agent must recompute
the corners from the OSM way coordinates reprojected around the chosen anchor.
The bearing is 45°/225° for the long axis and 135°/315° for the short axis.

Because of the 45° heading the axis-aligned bounding box is ~28 x 28 m. That is correct.

### 2.4 What each side shows

**Top** is observed from LiDAR and aerial imagery. **The four elevations are not
observed** — they are the most probable reading of a 2002 Santos-Prescott live/work
loft building given the permit record, the listing copy and the neighbourhood,
and they exist so that stage 2 has something specific to confirm or overturn.

**Southeast (South Park front)** — The address elevation and the one the park sees:
16.1 m wide and ~15.9 m tall (to the penthouse), so a distinctly vertical face.
Expect a ground-floor commercial/live-work base (State Farm office per the geocode,
with a glazed shopfront), then three loft levels of tall floor-to-ceiling windows
— the listings' "soaring 16+ feet floor-to-ceiling windows", probably three or four
bays per floor on a face this wide. This is the face that would carry the street
number. The penthouse level may set back slightly from this face.

**Northwest (3rd St / patio rear)** — The service/private entrance end. The
Compass listing confirms at least one unit has "its own private entrance from
3rd street." Expect a plainer, more residential face — individual unit entries,
a garage door, and the same tall window rhythm but perhaps less regular. The
patio/courtyard sits between this face and 3rd Street.

**Northeast flank** — 23.7 m long, four storeys. This is the longer of the two
flanks and faces the neighbour at 166-168 South Park (DataSF SF3775070, ~10.4 m
tall). Expect the building's main window rhythm here — a long regular run of
tall loft windows, probably four bays. From the app's aerial camera this is a
major surface.

**Southwest flank** — Also 23.7 m long, four storeys. This flank faces the open
South Park oval and is the most exposed elevation. Expect the same tall window
rhythm as the NE flank, perhaps with more glazing since it faces the park. This
is the face the park's visitors see most.

**Top — observed.** A flat roof at ~13.3 m with a penthouse/roof terrace element
reaching 15.93 m. The Curbed article confirms a "private rooftop terrace" on the
penthouse unit (#11). The LiDAR min of 6.35 m suggests a lower element somewhere
on the footprint — possibly a canopy over the ground-floor entrance, a roof
skylight, or a step in the building massing. The roof is the most-seen surface
in the app and must be deliberately designed: the penthouse, the terrace, and
a small mechanical grouping.

### 2.5 Recognition cues (ranked)

1. **The penthouse/roof terrace** — the element that lifts the crest to 15.93 m,
   ~2.6 m above the main roof. This is the building's strongest single feature
   from the air and the thing that makes it findable.
2. **Four storeys with tall windows** — standing ~4 m proud of the two- and
   three-storey neighbours, with a grid of floor-to-ceiling loft windows that
   reads as a rhythm from above.
3. **The through-lot position** — on the north rim of the oval, facing the park,
   with the patio/courtyard toward 3rd St. The building's siting is part of its
   identity.
4. The contemporary stucco-and-stone facade — clean, modern, 2002.
5. The ground-floor commercial base — a glazed shopfront on the park front.

### 2.6 Miniature translation

**Preserve**

- The 23.7 x 16.1 m footprint and the real 45°/225° heading, exactly
- The four-storey height standing proud of the neighbours
- The tall window grid as a rhythm, not as individual windows
- The penthouse/roof terrace element — the building's aerial signature
- The two-different-ends story: commercial front on the park, residential/patio
  rear toward 3rd St

**Simplify / exaggerate**

- The real window count on each 23.7 m flank becomes ~4 identical bays, all the
  same size, with tall proportions
- The 16+ ft floor-to-ceiling windows become a single tall recessed opening per
  bay — no mullion grids, no individual sashes
- The storefront becomes one wide glazed opening, not a shopfitted facade
- The penthouse may be slightly exaggerated in height to read from the air, but
  the crest must still land on 15.93 m — take the exaggeration out of the main
  roof, not out of the target height
- Roof clutter becomes a small, composed set: one penthouse volume, one terrace
  railing, one or two HVAC blocks

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not
a straitjacket — adjust after the first aerial review render.

1. Body: extrude the 2.3 rectangle from z=0 to the main roof z=13.3, `Toy_sand`
   (warm stucco — *inferred, confirm from photography*).
2. Ground floor, z=0 to z=4.0: on the SE end, one 6.0 m wide glazed storefront
   (`Toy_glass`) and one 1.2 m recessed entry (`Toy_ink`); on the NW end, one
   3.0 m garage door (`Toy_ink`) and one 1.0 m residential entry; on the flanks,
   two or three small openings only.
3. Floor band: 0.18 m `Toy_trim` course at z=4.0, carried around all four faces —
   it separates the commercial base from the lofts.
4. Wall levels, three of them, z=4.6 to z=12.8: on each long flank, 4 bays of
   2.0 x 3.5 m openings recessed 0.18 m, `Toy_glass`, with a 0.12 m `Toy_trim`
   frame band. On the SE end, 3 bays per floor, same size. On the NW end, 3 bays
   per floor with one entry door per floor at the ground level.
5. Eave: a 0.3 m `Toy_trim` parapet band at z=12.8 to z=13.3, all four faces.
6. **Roof, z=13.3 to z=13.5** — a thin flat roof slab, `Toy_roofd`, with a
   slight parapet upstand. This is the main roof surface.
7. **Penthouse, z=13.5 to z=15.93** — a setback volume on the SE third of the
   roof (overlooking South Park), `Toy_sand` walls with one or two glazed
   openings, and a terrace railing (`Toy_steel`) around its perimeter. This is
   the building's aerial signature and must read clearly from above.
8. Roof furniture: one or two HVAC units (`Toy_steel`, 1.5 x 1.0 x 0.6 m) grouped
   on the NW third of the roof, away from the penthouse.
9. Bevel 0.12 m, 2 segments.

### 2.8 Materials and palette — *inferred, confirm from photography*

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_sand` | `#ece4d4` | main body walls (warm stucco — *inferred*) |
| `Toy_stone` | `#d9d2c2` | ground-floor base (stone — *inferred*) |
| `Toy_trim` | `#f3efe6` | floor band, parapet, window frames, entry surround |
| `Toy_glass` | `#2a4d73` | loft windows, storefront glazing |
| `Toy_roofd` | `#45454a` | flat roof slab |
| `Toy_steel` | `#9aa0a6` | penthouse railing, HVAC units, window frame bands |
| `Toy_ink` | `#3a3530` | garage door, door recesses |
| `Toy_glass_Glow` | `#2a4d73` | lit loft windows at night |
| `Toy_trim_Glow` | `#f3efe6` | storefront spill at the park end |

The body colour is the single largest unknown in this plan. `Toy_sand` is a safe
warm neutral that will sit correctly next to the neighbourhood's palette, but a
2002 Santos-Prescott loft building could equally be a cooler stucco (`Toy_stone`)
or carry a material accent. Decide from photography, and if the real building has
a signature accent colour, say so in `REPORT.md` and spend one palette slot on it
— this plan deliberately does not invent one.

**Night state (required).** Glow surfaces must be thin shells proud of the opaque
glazing — the app renders `_Glow` in a separate layer that is ~12% alpha by day,
so a primary surface must never be authored as glow. Hero glow: a scatter of lit
windows on the exposed southwest flank, where the long rhythm reads best — four
or five of the twelve, not all — plus one or two on the SE (park) end. Supporting
accent: the storefront glazing at the South Park end. The penthouse may carry one
lit window. The patio/northwest end stays dark; a service alley that glows would
misread. The roof itself does not glow.

### 2.9 Top surface

23.7 x 16.1 m of flat roof at 13.3 m with a penthouse/roof terrace reaching 15.93 m,
in a district the camera flies over constantly. The composition problem is
restraint: the penthouse does the work, so the furniture should stay quiet and
grouped on the opposite end. Keep the roof value clearly darker than the walls
so the penthouse reads as a distinct volume from above. The terrace railing is
the one place semantic exaggeration is spent — make it readable but not heavy.

### 2.10 Scope

**In the GLB:** the single 2002 loft block — body, all four elevations' openings,
storefront and residential entries, garage door, parapet, the flat roof, the
penthouse/roof terrace with its railing, and the roof furniture

**Not in the GLB:** South Park, its trees or lawn, 3rd Street, the patio/courtyard,
166-168 South Park, the sidewalk, vehicles, people, plinths, cameras or lights

### 2.11 Triangle budget

Cap 9,000 — a secondary building, and the cap should bind. Suggested split: body,
parapet and floor band ~1.5k; the two 4-bay flanks ~2.5k; the SE end's storefront,
entry and bays ~1.2k; the NW end's garage, entries and bays ~1k; the roof slab
~0.5k; penthouse and railing ~1.5k; roof furniture ~0.8k.

Two places this budget can run away. The long flanks: keep each bay to a simple
recessed box with one frame band — eight bays of a fussy window will not fit and
will not read. And the penthouse: a railing modelled as individual balusters will
eat the budget for no aerial benefit — use a solid panel or a low lattice instead.

### 2.12 Draft manifest entry

```json
{
  "id": "188-south-park",
  "file": "188-south-park.glb",
  "anchor": [
    -122.3950794,
    37.7810118
  ],
  "targetHeightM": 15.93,
  "cat": 2,
  "name": "188 South Park",
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

- **New landmark.** Add a `pipeline/lib/landmarks.mjs` entry (`id: '188-south-park'`,
  `lon: -122.3950794`, `lat: 37.7810118`, `height: 15.93`, `exclude: 5`) and re-bake
  the affected tiles, or the baked procedural building on this exact footprint will
  intersect the GLB.
- **The anchor is the DataSF LiDAR footprint's area centroid, not the OSM OBB
  center.** This is the same choice made for 165-167 South Park (q.v. in
  `landmarks.mjs`): on a party-wall site, centring the exclusion circle on the
  DataSF area centroid opens the widest viable window, because it coincides with
  the bake input's own ring centroid (distance ~0 m) while maximising the distance
  to the nearest neighbour vertex. Measured from this anchor against the DataSF
  footprints `excluded()` consumes:

  | | trigger distance |
  |---|---|
  | 188 South Park's own footprint (SF3775125, via centroid) | **0.00 m** |
  | SF3775070 (166-168 South Park, nearest ring vertex) | **12.95 m** |
  | OSM way 124884355 (untagged, nearest vertex — may not be in DataSF/Overture) | 8.76 m |
  | 164 South Park (way 124884357, nearest vertex) | 21.53 m |
  | 521-527 3rd St (way 124884350, nearest vertex) | 17.50 m |

  The safe window is (0.1, 8.76) m if the untagged OSM way exists as a separate
  Overture footprint, or (0.1, 12.95) m if it does not. `exclude: 5` sits in the
  middle of the conservative window with ~3.8 m of margin at both ends. **Verify
  with `pipeline/audit.mjs` check 1.6 after the re-bake** and confirm visually
  that 166-168 South Park is still standing before committing.
- `loadRadius`: the skill's default formula gives `max(2500, 15.93 * 30) = 2500` m.
  Take the default. Beyond it the site is a gap rather than a procedural stand-in,
  but at 2.5 km a 16 m building is far below a pixel.
- This is the eighth South Park-area building in the landmark manifest. The same
  question applies as for 181: a manifest of one-off SoMa blocks will not stream
  well forever. If the intent is to keep doing individual buildings around this
  oval, the kit/instancing route (`KIT-INTEGRATION-PROMPT.md`) is the better
  long-term home for buildings of this class.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Bounding-box top exactly 15.93 m — the penthouse parapet, not a roof element (loader scale lands at 1.0)
- [ ] Dimensions plausible in meters and consistent with 2.1 (XY bbox ~28 x 28 m is expected)
- [ ] The footprint is still 23.7 x 16.1 m in plan — measure it, do not eyeball it
- [ ] Triangles at or under 9,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the lit loft windows and the storefront; glow shells proud of opaque glazing
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (per-object signed volume for the union of solids; ray test residual <= 0.15%)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + contact sheet + night render regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed
- [ ] The 2.15 five-storey question answered in `REPORT.md`, with the source that answered it
- [ ] The facade material either observed or, if it stayed inferred, said so plainly in `REPORT.md`

### 2.15 Open questions and risks

- **Four storeys or five?** The 1998 new-construction permit and every permit
  2005–2023 (except one) say 4 storeys. The 2018 kitchen remodel permit says
  `number_of_proposed_stories = 5`. The LiDAR max of 15.93 m against a median of
  13.34 m is consistent with a penthouse on a 4-storey building (a 2.6 m
  penthouse above a 13.3 m main roof), not a 5-storey building (which would put
  the median at ~12.7 m for a 15.93 m crest). The 2018 figure may reflect a
  penthouse mezzanine that was added or regularised, or it may be a clerical
  error. Treat the building as 4 storeys with a penthouse unless photography
  proves otherwise.
- **The facade material and colour are unverified.** The permit says "stone,
  stucco" and the architect is Santos-Prescott, but no street-level imagery was
  available. The palette in 2.8 is a best guess from the materials list and the
  architect's known work. One street-level photograph settles it.
- **The window rhythm is inferred.** The 4-bay reading on the 23.7 m flanks comes
  from dividing the width by a plausible loft bay width (~5.9 m centres). The real
  count and grouping must be observed.
- **The LiDAR min of 6.35 m is unexplained.** It could be a canopy over the
  ground-floor entrance, a roof skylight, an awning, or a step in the building
  massing (a one- or two-storey section). The aerial imagery was not detailed
  enough to settle it. If it is a canopy or awning, it does not affect the
  massing; if it is a step, the building is L-shaped and 2.7 needs revision.
- **The penthouse position is inferred.** The LiDAR max tells us the height but
  not where on the roof the penthouse sits. The Curbed article says the
  penthouse (#11) has a "private rooftop terrace," which implies it overlooks
  South Park (the SE end), but this is not confirmed. Aerial imagery should
  settle it.
- **The four elevations in 2.4 and the palette in 2.8 are unverified.** Only nadir
  aerial imagery and LiDAR were available to the author. Facade material, colour,
  window rhythm, bay count, and whether there is a signature accent are all open.
- **The through-lot patio is outside the building footprint.** The lot extends
  27.6 m from South Park to 3rd St, but the building is only 16.1 m deep. The
  remaining ~11.5 m is a patio/courtyard that is NOT part of the building and
  must not be modelled in the GLB. The Compass listing confirms it: "peaceful &
  well-appointed, wind-protected patio in the back."
- **OSM way 124884339 has no height tag.** Unlike 181 South Park (which has a
  misleading `height=14`), this building has no OSM height at all, so there is
  no wrong number to inherit. The LiDAR is the only height source, and it is
  measured.
- **The assessor roll may not be useful for storeys here.** The 2018 permit's
  5-storey figure is a reminder that the assessor/permit storey count can be
  inconsistent. The 1998 construction permit is authoritative for the original
  design; the LiDAR is authoritative for the as-built height.
