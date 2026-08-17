# 44–46 South Park — SF-SIM asset plan

A 2008 four-storey mixed-use infill house on the north-west rim of the South Park
oval: a ground-floor commercial unit at **46** (currently the venture firm MGV)
under three residential levels reached from a purple-painted door at **44**. Its
whole identity is one move — a white-painted, finely gridded steel window wall,
three bays wide, that fills almost the entire 9.5 m frontage from the pavement to
a charcoal-grey stucco parapet, and reads from the park as a lit glass lantern
between two opaque neighbours.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/46-south-park/`. This document is the plan only: Part 1 is the runnable
task prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `46-south-park` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3938249, 37.7821869` (DataSF LiDAR footprint SF3775217 area centroid, measured — see 2.3 for why not the OSM or parcel centroid) |
| Target height | **16.15 m** to the crest of the front parapet/roof screen; main roof deck 13.9 m; rear block ~8.0 m (LiDAR-derived, photogrammetrically corroborated — see 2.1 and 2.15) |
| Footprint | 9.47 m frontage (NE–SW, onto South Park) x 29.43 m depth (NW–SE); 278.7–293 m2 — a rectangle whose front face bears 45.2°/225.2° and faces **south-east, 135.2°** |
| Triangle cap | 6,000 |
| Category | `2` (apartments — four residential units over one commercial unit) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 44–46 South Park GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of 44–46 South Park in San Francisco and
deliver it as a downloadable, validated GLB.

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
7. `artifacts/106-south-park/` — the closest reference implementation in scale and
   plan geometry (the other narrow party-wall sliver on this oval: 7.32 x 29.72 m
   against this building's 9.47 x 29.43 m, same 45° heading, same two blind
   flanks). Take its massing discipline and its handling of a deep narrow lot.
   Do **not** take its facade language: 106 is a 1915 stucco SRO hotel with
   punched windows, this is a 2008 glass-and-stucco infill whose street face is
   one continuous gridded window wall.
8. `docs/asset-plans/46-south-park.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## What is already observed, and what is not

The south-east (South Park) elevation and the roof were observed directly — the
elevation from a Google Street View panorama 8.5 m in front of it (Jan 2025) and
the roof from near-nadir Google satellite imagery (2026). Both are described in
2.4 as **observation**, not inference, and both were measured, not eyeballed:
2.15 records the photogrammetry.

Three things are genuinely open and you must settle them (2.15):

1. **What the top 2.2 m is.** LiDAR puts the roof surface at 13.9 m and a maximum
   at 16.15 m; the Street View measurement puts the top of the grey band above the
   window wall at 15.9 ± 0.5 m. So there is definitely 2.2 m of something above the
   roof deck at the street face. The reading taken here is a solid parapet /
   terrace screen wall in the same charcoal stucco, with a roof terrace behind it.
   It could instead be a set-back top floor whose front wall is flush. **Both give
   the same 16.15 m crest, so the height is safe either way** — but the roof
   composition changes completely, so settle it from imagery before you design
   the roof.
2. **The north-west (rear) elevation.** It is a blind block-interior face with no
   Street View coverage and it sits in permanent shadow in the aerial. Everything
   2.4 says about it is inference from the LiDAR height profile.
3. **How far up the rear block steps down, and where.** The LiDAR height
   distribution says ~24% of the footprint sits at ~8 m rather than ~13.9 m
   (2.1). That is about 7 m of the 29.4 m depth, at the north-west end. The
   *fraction* is measured; the *position* is inferred from the aerial.

## Must capture

- The **window wall**: a white-painted, finely gridded steel/aluminium glazed wall,
  three structural bays wide, running the full frontage from the pavement to the
  parapet with essentially no solid spandrel between floors. It is the entire
  building. Everything else is background.
- The **charcoal-grey stucco frame** around it — a band across the top carrying
  the parapet, and a pier down the north-east side. The building reads as a pale
  grid set into a dark surround.
- The contrast with its neighbours: this is **the only glass front on its stretch
  of the rim**, standing between a pale grey stuccoed neighbour (54–58, south-west)
  and a black board-clad one (22–24, north-east).
- The **ground floor**: a tall glazed commercial front carrying the numerals `46`,
  with a white double-door bay at the south-west end and a small recessed
  **purple-painted** residential entry (`44`) at the north-east end under a purple
  awning. That purple is the building's only colour note and it must survive
  simplification.
- **Four levels over a 9.5 m frontage** — a tall, thin, vertical building on a
  low-rise oval, flat-topped, standing about 2 m above both neighbours.
- A deliberately designed flat roof: light membrane, the **solar array** on the
  north-west half, a large skylight, a tight mechanical cluster, and the step down
  to the lower rear block.
- **Two blind party walls** on the long north-east and south-west faces. This
  building has one public face, not four.

## Research 44–46 South Park independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- The south-east elevation onto the park, at ground level and from the air
- The roof, which is where the open question in 2.15 gets settled
- Any view at all of the rear, including from the buildings behind on Bryant Street
- Day and night appearance
- Whether an architect is attributable. None was found (2.15). The 2005 permit
  names no designer and the building has no press coverage.

**One attribution error is already known — do not re-inherit it.** Several
sources (an NBC Bay Area construction update; a T Magazine piece indexed under
this address) describe "the Gallery House at 44–46 South Park" by Ogrydziak
Prillinger Architects. **That is a different building.** The Gallery House is
**70 South Park**, parcel 3775-053, permit 200510064957 ("to erect 3 stories, 1
residence with gallery"), 5,418 sq ft, completed 2009 — two doors to the
south-west, and it has a latticed parametric facade this building does not have.
Do not model a lattice. See 2.15.

Prefer planning and permitting documents, the Assessor's roll, geolocated
photography, and aerial imagery. Never rely on a single photograph, a single
AI-generated image, or a single unsourced 3D model. Separate verified facts from
visual inference; if sources disagree, document the disagreement and decide.

## Create a reference dossier

Write `artifacts/46-south-park/REFERENCE.md` containing: source links and what each
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

This is a **secondary building** in the style bible's detail budget (§21), not a
hero landmark: clear massing, one strong facade rhythm, a simple designed roof,
and exactly one identity cue carried hard — the white grid in the dark surround.

The pane grid is the single biggest trap in this asset. At the app's camera a real
~120-pane sash is noise and will eat the triangle budget three times over. Read
2.6 before you model a single mullion.

The finished asset must be immediately recognizable as 44–46 South Park,
consistent with the real building from the street and from above, architecturally
credible, and a premium handcrafted miniature — not photorealistic, not voxel art,
not generic low-poly, and never accurate in one view while invented in the others.

## Scope of the exported asset

Export the single 2008 block: body, the south-east window wall and its stucco
frame, the ground-floor commercial front, the double-door bay, the purple
residential entry, the parapet, the flat roof, the solar array, the skylight, the
mechanical cluster, the two blind party walls, and the lower rear block.

Do not include unrelated surrounding city geometry: South Park itself, its lawn or
trees, the street or the pavement, the street tree that stands in front of the
south-west end, the timber utility pole and its overhead wires and transformers,
the wall-mounted streetlight bracket, parked cars, people, plinths, cameras or
lights. Do not model tenant signage — no `MGV` neon, no numerals as separate
geometry beyond a flush plate if you want them. Temporary context may appear in
review renders but must not leak into the GLB.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary
`.glb`; real-world meters; origin at base center; minimum geometry Z ~ 0; applied
transforms; no negative scales; outward normals; no duplicate or foreign geometry;
no image textures; no transparency; flat-color materials named `Toy_*` from the
project palette; `_Glow` suffix only on surfaces that glow at night; no `Toy_body`;
no cameras, lights, animations, armatures or constraints; no external
dependencies; at most 6,000 triangles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model
drops into the city at its real-world heading — the loader applies no rotation
(`placeGeneric` in `app/src/assets.js` only scales and positions). The street
front faces **south-east, bearing 135.2°**; the frontage line runs 45.2°/225.2°,
so build directly on the measured rectangle in 2.3 rather than modelling an
axis-aligned box and rotating it. The contract's "front faces −Y" cannot be
honoured literally here; real-world orientation wins (AGENTS rule 5) and the
deviation goes in `REPORT.md`.

**Height normalization:** the tallest geometry in the export (the front parapet /
roof screen) must land at exactly **16.15 m** so the loader's
`targetHeightM / measuredHeight` scale is 1.0.

## Reproducible Blender workflow

Blender 5.2 LTS. Headless: `blender -b --python script.py -- args`.

Keep `artifacts/46-south-park/build_46_south_park.py` (deterministic build script),
`artifacts/46-south-park/46-south-park.blend`, and
`artifacts/46-south-park/46-south-park.glb`. The script must rebuild the model
reliably enough for future revision. Do not modify or rename an unrelated existing
GLB to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`46-south-park-top.png`, `46-south-park-north.png`, `46-south-park-east.png`,
`46-south-park-south.png`, `46-south-park-west.png`, plus
`46-south-park-contact-sheet.png`, at least one high three-quarter aerial beauty
render `46-south-park-aerial.png`, and a night render
`46-south-park-aerial-night.png`.

Add one extra **square-on 135.2° view** of the street elevation
(`46-south-park-facade.png`). It is the only face anyone will ever see and none of
the four compass renders shows it flat.

The four elevations must share scale, framing, lighting, exposure and projection;
use orthographic or long-lens cameras; label directions from the researched
orientation; the top view must clearly show the full 9.47 x 29.43 m roof — its
solar array, skylight, mechanical layout and the step down at the rear; the aerial
view uses the style bible's camera assumptions (30–50 degrees down, long lens).
Simple tabletop lighting, neutral warm background, minimal depth of field, and
every image must depict the same exported model.

Because the building is rotated 45° from the world axes, the four compass renders
will each show two faces at 45°. That is correct and expected — do not rotate the
model to make the elevations square on.

## Validate the exported GLB

Re-import `46-south-park.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture
count, camera count, light count, animation count, applied-transform status,
negative-scale status, normal-orientation status, unexpected geometry, and
per-material contract compliance. Render at least one review image from the
re-imported asset. Write `artifacts/46-south-park/validation.json` and
`artifacts/46-south-park/REPORT.md`.

Note that the axis-aligned XY bounding box will be roughly **27.5 x 27.6 m** even
though the building is 9.47 x 29.43 m — that is the expected consequence of a
45° real-world heading, not a scale error.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "46-south-park",
  "file": "46-south-park.glb",
  "anchor": [
    -122.3938249,
    37.7821869
  ],
  "targetHeightM": 16.15,
  "cat": 2,
  "name": "44-46 South Park",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a separate, explicitly requested job — run `docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in `docs/asset-plans/46-south-park.md`.
````

---

## Part 2 — Research and design dossier

Compiled 16 August 2026 from the sources in 2.2. Values marked *inferred* are
visual or derived estimates, not published figures — the executing agent must
re-verify anything it relies on.

**A note on the evidence quality of this dossier.** The record side is unusually
clean for an anonymous 2008 infill: the Assessor's roll, sixteen permits including
both the demolition and the new-construction permit, the surveyed parcel, and the
DataSF LiDAR footprint all agree on what this building is. The *visual* side rests
on two observations — one Street View panorama (Jan 2025) and one near-nadir
satellite frame (2026) — but both were measured rather than described: 2.15 sets
out the photogrammetry that turns the panorama into metres and shows it agreeing
with the LiDAR maximum to within 0.25 m. The genuinely weak points are the rear
elevation, which nothing sees, and what the top 2.2 m of the street face actually
is. Both are named in 2.15.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Built | **2008** | SF Assessor secured roll, `year_property_built = 2008` (all 18 roll years agree) |
| Construction permit | **200501052624**, filed 5 Jan 2005: "to erect 4 story 1 residential condo & retail", $1,000,000, block 3775 lot 050 | DataSF Building Permits — **the only source that states four storeys** |
| Predecessor | a **2-storey office building**, demolished under permit 200501052617 (filed the same day, then addressed 64 South Park) | DataSF Building Permits |
| Address split | **44 = residential, 46 = commercial** | permit M137205, 15 Oct 2008: "verify address on block 3775 lot 217 - #44 south aprk - residential #46 south park - commercial unit" |
| Storeys (Assessor) | **3** | Assessor `number_of_stories = 3.0`; every permit 2016–2017 also records 3. See 2.15 — read as three residential levels over the commercial ground floor |
| Units | 4 residential + 1 commercial | Assessor `number_of_units = 4.0`, class `FS` "Flat & Store 4 units or less"; augrented summary |
| Structure | **wood frame (Type V)** | permits 201608175251 / 201609147725 / 201611072151 / 201709259517, `proposed_construction_type_description = wood frame (5)` |
| Building area | **6,240 sq ft** (579.7 m2) | Assessor `property_area` |
| Lot area | **3,122.66 sq ft** (290.1 m2) | Assessor `lot_area` |
| Block / lot | 3775 / 217, APN 3775-217; parcel recorded **18 Dec 2007** out of former lot 050 | DataSF Parcels `acdm-wktn`, `date_rec_add` |
| Zoning | **SPD** (SoMa — South Park) | DataSF Parcels `zoning_code` / `zoning_district` |
| Neighbourhood | Financial District/South Beach; planning district South of Market; Supervisorial District 6 | DataSF Parcels |
| Solar | **4.96 kW PV array, installed 2012** | augrented building summary; the array is plainly visible in the 2026 nadir aerial — **observed** |
| Re-roofed | 2016, $42,400 | permit 201611072151 ("re-roofing") |
| Other works | fire sprinklers 2007 (18.2k); drywall + framing 2016; bathroom 2017 (50k); two combi boilers 2022 | permits 200704058150, 201608175251/201609147725, 201709259517; augrented |
| Last sale | 8 Aug 2011 | Assessor `current_sales_date` |
| Owner | Provincial Appliance Hldgs | augrented |
| Ground-floor tenant (46) | **MGV — Maschmeyer Group Ventures**, an enterprise-software venture firm; neon `MGV` sign in the window | OSM node 10874867147 (`office=company`, `addr:housenumber=46`); mgv.vc; **observed** in the Jan 2025 Street View |
| Footprint (OSM) | **29.43 m x 9.47 m, 278.7 m2**, frontage bearing 45.2°/225.2° | OSM way/124884347 (`addr:housenumber=44;46`, `height=14`), reprojected — **measured** |
| Footprint (parcel, survey) | 30.10 m x 9.74 m, 293.0 m2, same bearing | DataSF Parcels `acdm-wktn`, blklot 3775217, reprojected — **measured**, agrees to 0.3 m |
| Footprint (LiDAR) | 284.3 m2, 1,146 cells at 50 cm | DataSF `ynuv-fyni` SF3775217 — **measured**, agrees |
| Roof maximum | **16.15 m** above ground | DataSF LiDAR `hgt_maxcm = 1615` — **measured**; interpretation in 2.15 |
| Roof surface (majority) | **13.91 m**; median 13.52 m | DataSF LiDAR `hgt_majoritycm / hgt_mediancm` — **measured** |
| Height mean / std / min | 12.50 m / 2.47 m / 7.04 m | DataSF LiDAR — **measured**; the low mean and high std are the rear block, see below |
| Rear block | **~24% of the footprint at ~8.0 m**, i.e. roughly the rear 7 m of the 29.4 m depth | *derived* — the two-level mixture that reproduces mean 12.50 and std 2.47 against a 13.9 m main roof is f = 0.237 at 8.0 m (predicted std 2.51 vs measured 2.47) |
| Street-face crest (photogrammetry) | **15.9 m ± 0.5** | Google Street View pano `3UENxVRbARytZj977XeBXA`, Jan 2025, measured — see 2.15 |
| Ground elevation | 11.90 m (NAVD88) | DataSF LiDAR `gnd_min_m` — app terrain handles this, not the asset |
| Neighbour heights | 22–24 South Park (SF3775048) median **12.39 m**, max 14.22, std 0.63; 54–58 (SF3775219) median 13.50, max **16.94**, std 3.89; 70 South Park / Gallery House (SF3775053) median 12.87, max **16.35**, std 3.57 | DataSF LiDAR — **measured**; the 54–58 and 70 profiles are this building's twins, see 2.15 |

### 2.2 Sources

- https://www.openstreetmap.org/way/124884347 — footprint, `addr:housenumber=44;46`, `addr:street=South Park`, `height=14`
- https://www.openstreetmap.org/node/10874867147 — `office=company`, "Maschmeyer Group Ventures", `addr:housenumber=46`
- `https://data.sfgov.org/resource/ynuv-fyni` (DataSF Building Footprints, LiDAR-derived) — SF3775217, 1,146 cells, heights 16.15 / 13.91 / 13.52 / 7.04 m; and SF3775048, SF3775219, SF3775053 for the neighbours
- `https://data.sfgov.org/resource/acdm-wktn` (DataSF Parcels) — parcel 3775217, "44–46 SOUTH PARK", zoning SPD, recorded 18 Dec 2007
- `https://data.sfgov.org/resource/wv5m-vpq2` (SF Assessor secured roll) — built 2008, 3 storeys, 4 units, 6,240 sq ft on a 3,122.66 sq ft lot, class FS, sold Aug 2011
- `https://data.sfgov.org/resource/i98e-djp9` (SF Building Permits) — 16 permits at 44/46 South Park: the Jan 2005 demolition of the 2-storey office (200501052617), the Jan 2005 four-storey new-construction permit (200501052624), the 2007 sprinklers, the 2008 address-verification permit that split 44 from 46 (M137205), the 2016 re-roof, the 2017 bathroom; plus the 70 South Park set (200510064957 and its revisions) that identifies the Gallery House
- https://augrented.com/sf/3775217-44-46-south-park — the 4.96 kW 2012 solar system, the 2022 combi boilers, the owner, and the "three-story mixed-use, four residential units and a commercial space" summary
- https://www.mgv.vc/about — the ground-floor tenant at 46
- Google Street View, **Jan 2025**, panorama `3UENxVRbARytZj977XeBXA` at approximately `37.78206,-122.39367` — the south-east elevation, **observed and measured** (2.15)
- Google Maps satellite (2026, near-nadir, tiles at z21–z22 over `37.78220,-122.39383`) — the roof, the solar array, the mechanical cluster and the rear step, **observed**
- Attribution trap, recorded so the next researcher does not repeat it: https://www.nbcbayarea.com/local/construction_update__the_gallery_house_sf/1837917/ and the T Magazine piece hosted at https://www.inglettgallery.com/usr/documents/press/download_url/103/2010-03_gangloff_t-magazine.pdf both place Ogrydziak Prillinger's **Gallery House** at "44–46 South Park". It is at **70 South Park** — see https://architizer.com/projects/ (OPA project pages), https://www.archilovers.com/projects/44192/gallery-house.html, https://www.7x7.com/gallery-house-south-park-san-francisco-2657536663.html (all "70 South Park", 5,418 sq ft, four levels), and the permits and Assessor record for parcel 3775-053, which match that description exactly and do not match this one

### 2.3 Orientation and placement

The building occupies its whole lot on the **north-west rim of the South Park
oval**, mid-block between 22–24 South Park (north-east) and 54–58 South Park
(south-west). Both long sides are party walls; the block interior lies behind it
to the north-west. The rim runs north-east/south-west here, so the frontage line
bears **45.2°/225.2°** and the street face looks **south-east, 135.2°**, across
the pavement and the roadway into the park.

This is a **narrow, deep lot**: 9.47 m of frontage against 29.43 m of depth, a
3.1:1 ratio. Everything about the design follows from that — one public face, two
blind flanks, a light court or a lower block at the back, and a section that goes
up rather than back.

Three independent surveys agree on the shape: the OSM trace (29.43 x 9.47 m,
278.7 m2), the DataSF surveyed parcel (30.10 x 9.74 m, 293.0 m2) and the DataSF
LiDAR footprint (284.3 m2). Their centroids sit within 2.31 m of one another
(OSM↔parcel 2.31 m, OSM↔LiDAR 1.22 m, LiDAR↔parcel 1.37 m). **This plan takes the
DataSF LiDAR footprint centroid** as the anchor: it is the middle of the three
opinions, and it is the centroid of the ring the bake actually reads and deletes,
which is what opens the exclusion window in 2.13.

Rectangle corners in Blender coordinates (metres, `+X` east, `+Y` north),
centred on the anchor `-122.3938249, 37.7821869`, using the OSM dimensions on the
survey bearing:

```
(  7.01, -13.78)   South corner   (front x the south-west party wall)
( 13.73,  -7.10)   East corner    (front x the north-east party wall)
( -7.01,  13.78)   North corner   (rear  x the north-east party wall)
(-13.73,   7.10)   West corner    (rear  x the south-west party wall)
```

in ring order: `(7.01, -13.78) → (13.73, -7.10) → (-7.01, 13.78) → (-13.73, 7.10)`.

Edges, with outward normals:

| Edge | Length | Faces | Elevation |
|---|---|---|---|
| South corner → East corner | 9.47 m | SE 135.2° | **South Park front** — the only public face |
| East corner → North corner | 29.43 m | NE 45.2° | **party wall** (blind), against 22–24 |
| North corner → West corner | 9.47 m | NW 315.2° | **rear** (block interior, blind) |
| West corner → South corner | 29.43 m | SW 225.2° | **party wall** (blind), against 54–58 |

Because of the 45° heading the axis-aligned bounding box is ~27.5 x 27.6 m. That
is correct.

### 2.4 What each side shows

**South-east (South Park) — observed and measured, Jan 2025.** The whole building,
9.47 m wide and four levels tall, is one composition: a white-painted glazed grid
set into a charcoal-grey stucco surround.

The **window wall** is three structural bays wide (a wide centre bay flanked by
two narrower ones) and runs from the pavement to just under the parapet with no
solid spandrel anywhere — the floors read only as slightly heavier white
horizontal mullions. Within the bays the glass is subdivided by a fine grid of
near-square panes roughly 1.0 m across, four to five panes wide overall. It reads
like an industrial steel sash blown up to the height of a house, and it is
white — not black, not bronze. The wall projects a few tens of centimetres in
front of the stucco plane, so the stucco returns are visible down its
north-east side: a shallow bay, not a flush curtain wall.

At the **top** of the window wall, the last two pane rows are **frosted/obscure
white** rather than clear — a distinct pale band that caps the grid.

The **stucco** is a medium-dark neutral grey, close to the value of wet pavement.
It forms (a) a band across the whole frontage above the window wall, carrying the
parapet and pierced by three small dark recessed vents or louvres, and (b) a pier
roughly 1.5–2 m wide down the north-east edge. There is no cornice, no moulding
and no ornament of any kind; the parapet is a straight top edge against the sky.

The **ground floor** is a tall glazed commercial front — the MGV office, glazed
floor to head with the same white grid, carrying the numerals `46` on the glass
and a small neon sign inside. At the **south-west** end of the frontage is a
separate bay of white-framed **double doors** (a garage or service entry) with
three white brackets mounted on the wall above them. At the **north-east** end,
tucked against the stucco pier, is a shallow recessed **residential entry painted
aubergine purple**, with a small purple awning over it and a white door — the
`44` address. The purple is the only saturated colour on the building.

Measured heights on this face (2.15): pavement 0, storefront head ≈ 4.0–4.3 m,
top of the window wall ≈ 13.0 m, crest of the stucco parapet ≈ 15.9 m.

**North-east and south-west (party walls) — observed indirectly.** Blind. 22–24
South Park to the north-east has a 12.39 m roof and 54–58 to the south-west a
13.50 m roof, so both neighbours stand about 1.5 m below this building's 13.9 m
deck and roughly 2.5 m below its parapet crest. Both party walls therefore show a
thin strip of this building above the neighbouring roofs and nothing else. Model
them as plain stucco with no openings, and carry the parapet across.

**North-west (rear) — not observed.** A blind block-interior face. From the LiDAR
profile it is the low end: roughly the rear 7 m of the plan sits at about 8 m
rather than 13.9 m, so the rear elevation is a two-level block with the main
four-level mass rising behind — from the north-west you would see a low wall with
a tall one above and behind it. Whether the step is a full-width rear block, a
light court open to the sky, or a stepped roof terrace is not determinable from
any source found. Marked *inferred*.

**Top — observed, Google satellite 2026, near-nadir.** A flat light-grey membrane
roof, deliberately laid out along the long axis:

- A **solar photovoltaic array** occupies the north-west half of the main roof — a
  clean rectangular grid of dark blue-black panels, roughly four to five panels
  across by five to six along, aligned with the building's long axis. This is the
  4.96 kW 2012 system and it is the single loudest thing on the roof from above.
- Immediately **south-east of the array** sits a large flat rectangle roughly
  4.5 x 4.5 m in a mid grey-brown, distinctly different in value from the
  membrane — read as a big skylight or roof hatch over the stair, not as a
  penthouse box (no side face or cast shadow is visible at this sun angle).
- The **south-east half** of the roof is mostly clean membrane, punctuated by
  a dozen small round penetrations (drains, vents, PV anchors), one dark
  rectangular mechanical unit, and a tight cluster of four to six pale
  condenser/fan units near the north-east parapet.
- The **north-west end** steps down into the low rear block and is in permanent
  shadow in the imagery.
- Nothing tall stands on the roof. Whatever accounts for the 2.2 m between the
  13.9 m deck and the 16.15 m maximum is at the **street edge**, not in the middle
  (2.15).

### 2.5 Recognition cues (ranked)

1. **The white grid in the dark surround.** A finely gridded white glazed wall
   filling a 9.5 m frontage, framed by charcoal stucco. Nothing else on this rim
   of the oval does it, and at the app's camera it is the whole building.
2. **Glass to the ground.** The commercial front is not a shopfront band under a
   solid facade — the grid runs continuously from the pavement to the parapet, so
   the building reads as one lit column rather than as a base and a body.
3. **Tall and thin.** Four levels over 9.5 m of frontage, flat-topped, standing
   about 2 m above both neighbours on a low-rise residential oval.
4. **The purple entry.** A small aubergine recess and awning at the north-east
   end — the only colour on an otherwise white-and-grey building.
5. The solar array on the roof, which is what the aerial camera sees first.

### 2.6 Miniature translation

**Preserve**

- The 9.47 x 29.43 m footprint and the real 45.2°/225.2° heading, exactly
- One public face and two blind party walls — do not decorate the flanks
- The three-bay division of the window wall and its projection in front of the
  stucco plane
- The stucco frame: band above, pier to the north-east
- The tall glazed ground floor, the double-door bay south-west, the purple entry
  north-east
- The flat roof with the solar array on the north-west half and the step down at
  the rear
- The height relationship to the neighbours: this one stands above both

**Simplify / exaggerate**

- **The pane grid becomes a coarse grid, not a fine one.** Model the three
  structural bays with their heavy white mullions, and inside each bay **one
  horizontal mullion per floor plus one vertical per bay** — a 3-wide x 4-tall
  grid over the whole wall, not the real ~5 x 12. The cue is "finely gridded
  white glazing"; at 30–50° down and a long lens the *count* is invisible and the
  *whiteness and regularity* is everything. Anything finer will not read and will
  cost the budget three times over.
- Represent the mullions as **shallow raised bands on a single recessed glass
  plane**, not as individual box frames around individual panes. One glass slab,
  one grid of bands.
- The frosted top band becomes **one row of `Toy_trim` panels** across the top of
  the window wall — flat opaque, no glass.
- The three small vents in the stucco band become **three shallow recesses**, or
  drop them; they are a 0.3 m detail.
- The ground floor keeps its glazing but gets **only two openings broken out**:
  the double-door bay (one recessed `Toy_ink` panel with a white frame) and the
  purple entry (one recess). No door leaves, no handles, no brackets.
- The purple may be pushed **more saturated than reality** — this is the one place
  to spend semantic exaggeration, because the building otherwise has no colour and
  the miniature palette wants an accent.
- The solar array becomes **one dark slab with a shallow grid scored into it** (or
  a 4 x 5 arrangement of flat tiles at most) on a low frame, not individual panels
  on individual rails.
- Roof clutter becomes a composed set: the array, one skylight box, one mechanical
  box and one tight group of three cylinders. Nothing else.
- Stucco texture becomes flat colour; the grey reads through massing and value
  contrast with the white grid.

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not a
straitjacket — adjust after the first aerial review render. Heights are the
reading argued in 2.15; if you settle that question differently, keep the 16.15 m
crest and move what is under it.

1. **Main body:** extrude the front 22.4 m of the 2.3 rectangle from z=0 to the
   roof deck z=13.90, `Toy_steel`.
2. **Rear block:** extrude the remaining rear 7.0 m from z=0 to z=8.00,
   `Toy_steel`. Give it a thin `Toy_roofd` cap and a 0.4 m parapet upstand.
3. **Party walls:** carry the main body's stucco unbroken across both 29.43 m
   faces to z=13.90, no openings, and up to the parapet on the front 2 m only.
4. **Front parapet / roof screen:** on the south-east face only, continue the
   stucco from z=13.90 to **z=16.15** as a solid wall ~0.35 m thick, returning
   about 2 m down each party wall so it reads as a screen and not as a billboard.
   **This is the crest and must land at exactly 16.15 m.**
5. **Stucco pier:** a 1.8 m wide band of `Toy_steel` standing 0.10 m proud of the
   front face at its north-east end, from z=0 to the parapet.
6. **Window-wall recess:** inset the remaining ~7.5 m of the front face by 0.35 m
   from z=0.15 to z=13.00 and fill it with one `Toy_glass` plane.
7. **Window-wall frame:** a `Toy_trim` border 0.25 m wide around that opening,
   standing 0.20 m **proud of the original front plane** (the wall projects).
8. **Bay mullions:** two vertical `Toy_trim` bands 0.18 m wide dividing the
   glazing into three bays — centre bay ~3.3 m, flankers ~2.0 m.
9. **Floor mullions:** horizontal `Toy_trim` bands 0.22 m deep at z=4.30, 7.50 and
   10.70, full width of the glazing.
10. **Frosted band:** `Toy_trim` panels filling the glazing between z=11.9 and
    z=13.00, flush with the glass plane.
11. **Ground floor, z=0.15 to z=4.30:** at the south-west end of the frontage, a
    2.4 m wide `Toy_ink` recessed panel (the double doors) inside the white frame;
    at the north-east end against the pier, a 1.4 m wide, 0.4 m deep recess in
    `Toy_plum` with a `Toy_plum` awning slab 1.6 x 0.9 x 0.12 m at z=3.0; the rest
    is glazing.
12. **Base:** a 0.15 m `Toy_ink` plinth across the frontage.
13. **Roof deck, z=13.90 to z=14.02:** a thin slab in `Toy_stone` covering the main
    body inside the parapet, plus a 0.45 m `Toy_steel` parapet upstand on the two
    party-wall edges and the rear edge (the front already has the tall screen).
14. **Solar array:** a 5.6 x 8.0 m slab at z=14.30, 0.12 m thick, `Toy_navy`, on
    four low `Toy_steel` rails, sitting on the north-west half of the main roof
    with its long axis along the building's, scored into a 4 x 5 grid by 0.06 m
    `Toy_steel` bands.
15. **Skylight:** one 4.2 x 4.2 x 0.45 m raised monitor immediately south-east of
    the array, `Toy_glass` on a `Toy_trim` kerb.
16. **Mechanical:** one `Toy_steel` box 1.8 x 1.2 x 0.8 m and three 0.8 m diameter
    10-segment cylinders 0.6 m tall, grouped against the north-east parapet on
    the south-east third of the roof.
17. Bevel 0.12 m, 2 segments.

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette except where noted.

| Material | Hex | Used for |
|---|---|---|
| `Toy_steel` | `9aa0a6` | stucco body, party walls, parapet/screen, pier, mechanical, PV rails |
| `Toy_trim` | `f3efe6` | window-wall frame, bay and floor mullions, frosted top band, skylight kerb |
| `Toy_glass` | `2a4d73` | the glazed wall and ground floor, skylight |
| `Toy_stone` | `d9d2c2` | roof membrane |
| `Toy_navy` | `2c4a70` | solar panels |
| `Toy_ink` | `3a3530` | base plinth, double-door panel, stucco vent recesses |
| `Toy_plum` | `6b4270` | **off-palette, deliberate** — the residential entry recess and its awning |
| `Toy_trim_Glow` | `f3efe6` | the lit commercial ground floor at night |
| `Toy_glass_Glow` | `6f95b8` | a few lit residential panes |

`Toy_steel` at `9aa0a6` is the palette's lightest neutral grey and reads a little
paler than the real stucco. That is the right direction for a miniature: the
building's whole trick is a *white* grid against a *darker* surround, and the
contrast survives better at `9aa0a6` than at `45454a`, which turns the facade into
a black hole at the app's camera. If the aerial render shows the surround reading
as another white building, darken toward `Toy_roofd` and say so in `REPORT.md`.

`Toy_plum` is not in the palette and is a knowing WARN, not an oversight. The
building has exactly one colour and it is this door; dropping it to `Toy_ink`
loses the fifth recognition cue, and no palette entry is anywhere near purple. Log
it in `REPORT.md` as an intentional off-palette accent under the style bible's
"saturated accents" clause.

**Night state (required).** Glow surfaces must be thin shells proud of the opaque
glazing — the app renders `_Glow` in a separate layer, and a closed shell reads at
roughly twice the nominal day alpha, so a primary surface must never be authored
as glow. Hero glow: **the commercial ground floor**, the full width of the
frontage in `Toy_trim_Glow` — an office lit behind a wall of glass, and by some way
the brightest thing on this stretch of the rim at night. Supporting accent: three
or four lit panes scattered over the upper three levels in `Toy_glass_Glow`, never
a full row, never the whole wall. The party walls, the rear and the roof stay
dark; the solar array especially must not glow.

### 2.9 Top surface

9.47 x 29.43 m of flat roof in a district the camera flies over constantly, and
one of the taller roofs on its stretch of the oval, so it is looked *into* rather
than *down onto* from far above. Two things carry it. First, the **solar array**,
which is the only strongly dark element and should sit as one clean rectangle with
its long axis along the building's — it does the same job the pier grid does on the
front, which is to say it makes the building legible from the one angle the app
actually uses. Second, the **step down to the rear block**, which gives the plan
depth and stops a 29 m strip of membrane from reading as a blank lid. Keep the
south-east third clean so the array and the skylight sit as a pair; group all the
mechanical hard against the north-east parapet. The front screen wall's inner face
and the shadow it throws across the deck at low sun are worth more than any
additional roof object.

### 2.10 Scope

**In the GLB:** the single 2008 block — body, the south-east window wall with its
frame, mullions and frosted band, the stucco surround and pier, the tall front
parapet/screen, the ground-floor commercial front, the double-door bay, the purple
entry and awning, both blind party walls, the lower rear block, the flat roof, the
solar array, the skylight and the mechanical cluster

**Not in the GLB:** South Park, its lawn or trees, the street and pavement, the
street tree in front of the south-west end, the timber utility pole with its
transformers and overhead wires, the wall-mounted streetlight bracket, the
neighbours at 22–24 or 54–58, vehicles, people, plinths, cameras or lights

**Deliberately excluded: tenant signage.** The `MGV` neon and the `46` numerals on
the glass are a tenant fitout on a building that has changed hands once already
and will again. Model the storefront as architecture. Record the omission in
`REPORT.md`.

### 2.11 Triangle budget

Cap 6,000 — a secondary building with one face, and the cap should bind. Suggested
split: main body, rear block, party walls and parapet ~1.1k; the front screen and
pier ~0.4k; the window-wall frame and its five mullions ~0.9k; the glass plane and
frosted band ~0.3k; ground-floor recesses, awning and plinth ~0.8k; roof deck and
upstands ~0.4k; solar array with its scored grid and rails ~1.1k; skylight ~0.2k;
mechanical cluster ~0.6k.

The one place this budget can run away is **the grid**. A faithful ~5 x 12 pane
subdivision modelled as individual framed openings is 60 recesses and roughly 4k
triangles on its own, and none of it resolves. 2.6 specifies a 3 x 4 grid of
raised bands on a single glass plane for exactly this reason; if you find yourself
above 6,000 triangles, that is the first thing to check and it is almost certainly
the cause.

### 2.12 Draft manifest entry

```json
{
  "id": "46-south-park",
  "file": "46-south-park.glb",
  "anchor": [
    -122.3938249,
    37.7821869
  ],
  "targetHeightM": 16.15,
  "cat": 2,
  "name": "44-46 South Park",
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

- **New landmark.** Add a `pipeline/lib/landmarks.mjs` entry (`id: '46SouthPark'`,
  `lon: -122.3938249`, `lat: 37.7821869`, `height: 16.15`, `exclude: 3`) and re-bake
  the affected tiles, or the baked procedural building on this exact footprint will
  intersect the GLB. This is the Case B path in
  `docs/asset-plans/INTEGRATION-PROMPT.md`.

- **The exclusion window, measured against the real bake input.** `excluded()` in
  `pipeline/buildings.mjs` drops a footprint when its centroid **or any ring
  vertex** falls inside the circle. The bake reads `buildings_datasf.geojson`
  first and gap-fills from `overture_buildings.geojsonseq`, and because
  `addBuilding()` returns null on exclusion, `markOccupied()` never runs — so the
  Overture twin of an excluded DataSF footprint is re-attempted and must be caught
  by the same circle. Measured from the manifest anchor:

  | Polygon | Triggers at | Via |
  |---|---|---|
  | this building, DataSF SF3775217 | **0.00 m** | its own centroid |
  | this building, Overture/OSM way 124884347 (`height=14`) | **1.21 m** | its centroid — **the FLOOR** |
  | 26–28 South Park, DataSF SF3775049 (h 8.35) | **4.99 m** | nearest ring vertex — **the CEILING**, and a point it *shares* with this building's ring |
  | 22–24 South Park rear wing, Overture (h 7.7) | 8.85 m | centroid |
  | 54–58 South Park, DataSF SF3775219 (h 13.5) | 9.16 m | centroid |
  | 54–58 South Park, Overture (h 14) | 9.23 m | centroid |
  | 22–24 South Park, Overture (h 12) | 13.72 m | nearest vertex |
  | 22–24 South Park, DataSF SF3775048 | 14.54 m | nearest vertex |

  The safe window is **(1.21, 4.99) m**. **Use `exclude: 3`** — 1.79 m of margin
  below and 1.99 m above, near the middle of the band. A correct exclusion here
  drops **exactly two rings**, not one (the DataSF footprint and its Overture
  twin); if `verify-rebake.mjs` reports one or three, something is wrong. Do not
  raise past 4.5: at 4.99 this starts deleting 26–28 South Park, whose LiDAR ring
  shares a party-wall vertex with this one, and leaves a hole two doors up the
  street wall.

  Measuring from the OSM ring centroid instead gives the window (1.21, 4.47) and
  from the parcel centroid (1.37, 4.66); both work, but the DataSF centroid is the
  most comfortable and is also the middle of the three surveys, so the manifest
  anchor and the registry point can be the **same** here.

- **`exclude` is also the tree-clear and street-furniture radius.** At 3 m it
  clears neither, which is correct: the street tree in front of the south-west end
  of this frontage is real and belongs to the park's rim planting. Do **not** set
  `clearTrees: true`.

- `loadRadius`: the default formula gives `max(2500, 16.15 x 30) = 2500` m. Take
  the default.

- **Camera preset.** `app/src/camera.js` places the camera at
  `(sin(yaw), sin(pitch), cos(yaw)) x distance` from the pivot and the project's
  `+z` is south, so app yaw = 180 − true bearing. This building's one public face
  looks 135.2°, giving **`yaw: 45`** — camera to the south-east, over the park,
  looking north-west at the window wall. That is the only view of this building
  worth flying to. Start from `camera: { distance: 130, yaw: 45, pitch: 24 }` and
  tune against the live scene. Note the standing disagreement recorded in
  `106-south-park.md` §2.13: `165SouthPark`'s preset reads as the opposite
  convention. Settle it by render, not on paper.

- **This is the twentieth South Park building to enter the manifest by hand, and
  the argument against doing it again keeps getting stronger.** A row of narrow
  party-wall buildings on a residential oval is what `KIT-INTEGRATION-PROMPT.md`
  exists for. This one has a better claim than most of the remaining row — it is
  the only glass front on the rim, it is 2 m taller than both neighbours, and its
  night state is genuinely different from theirs — but the claim is about
  *contrast within the row*, which is exactly the kind of thing a kit with a
  handful of facade variants ought to be able to deliver. Say so again when the
  next one comes up.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Bounding-box top exactly 16.15 m — the front parapet/screen, not a mechanical
      unit and not the solar array (loader scale lands at 1.0)
- [ ] Dimensions plausible in meters and consistent with 2.1 (XY bbox ~27.5 x 27.6 m
      is expected for a 9.47 x 29.43 m building at 45°)
- [ ] Frontage 9.47 m and depth 29.43 m, measured in plan, not eyeballed, and not
      rounded toward a squarer building
- [ ] The main roof deck sits at 13.90 m and the rear block at ~8.0 m over roughly
      the rear quarter of the plan
- [ ] The window wall projects in front of the stucco plane; the stucco returns are
      visible on its north-east side
- [ ] The glazing grid is 3 bays x 4 rows of raised bands on one glass plane — not
      an individually framed pane grid
- [ ] The frosted band exists at the top of the glazing and is opaque `Toy_trim`
- [ ] The purple entry and awning are at the **north-east** end of the frontage and
      the double-door bay at the **south-west** end (not mirrored)
- [ ] Both party walls and the rear are blind — no openings anywhere but the front
- [ ] Solar array present, on the north-west half, aligned to the long axis
- [ ] Triangles at or under 6,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`; `Toy_plum`
      logged in `REPORT.md` as a deliberate off-palette accent
- [ ] `_Glow` only on the commercial ground floor and three or four upper panes;
      glow shells proud of the opaque glazing, never a closed shell around it
- [ ] No tenant signage, no `MGV` neon, no street tree, no utility pole
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (per-object signed
      volume for the union of solids; ray test residual <= 0.15%)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + the extra square-on 135.2° facade view + contact sheet +
      night render, all regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed
- [ ] The 2.15 parapet-versus-top-floor question answered in `REPORT.md`, with the
      evidence that answered it

### 2.15 Open questions and risks

- **The Gallery House attribution is wrong and will be offered to you again.** An
  NBC Bay Area construction update and a T Magazine article indexed under this
  address both call this "the Gallery House" by Ogrydziak Prillinger Architects,
  with a latticed parametric facade derived from a reading of the bay-window code.
  The Gallery House is **70 South Park**, two doors south-west: parcel 3775-053,
  permit 200510064957 "to erect 3 stories, 1 residence with gallery", Assessor
  `property_area` 5,418 sq ft — the exact figure the architecture press quotes for
  the Gallery House — built 2009, with permits that explicitly reconfigure a roof
  penthouse and add three skylights. This building is parcel 3775-217, permit
  200501052624 "4 story 1 residential condo & retail", 6,240 sq ft, built 2008,
  with a plain white gridded window wall and no lattice at all. **If you find
  yourself modelling a woven triangular screen, you are modelling the wrong
  building.**

- **What the top 2.2 m is: parapet or top floor?** This is the one thing that
  changes the design. LiDAR gives a roof surface at 13.91 m (majority) / 13.52 m
  (median) and a maximum of 16.15 m. Independently, the Street View panorama puts
  the top of the grey stucco band at **15.9 ± 0.5 m** — so the street face really
  does continue about 2.2 m above the roof deck. The reading taken here is a solid
  parapet / terrace screen wall with a roof terrace behind it, because (a) the
  near-nadir aerial shows nothing tall standing anywhere on the roof, so the extra
  height is at the edge, and (b) **both immediate neighbours have the identical
  LiDAR signature** — 54–58 South Park median 13.50 / max 16.94 / std 3.89, and 70
  South Park median 12.87 / max 16.35 / std 3.57, against this building's 13.52 /
  16.15 / 2.47. Three consecutive 2005–2009 infill houses with the same bimodal
  profile is a typology, not three coincidences, and 70 South Park's permits
  confirm a roof-level penthouse serving a terrace. The alternative reading — a
  set-back fourth level whose front wall is flush with the facade — is not
  excluded by anything observed. **The risk is contained:** because the model is
  authored with the crest at exactly 16.15 m, the loader's scale is 1.0 either
  way, and an error here makes the parapet too tall without making the building
  too tall. But it changes what the roof is, so settle it from imagery.

- **The photogrammetry, so you can check it rather than trust it.** The Jan 2025
  panorama `3UENxVRbARytZj977XeBXA` is a levelled equirectangular image, so the
  horizon is exactly the centre row and elevation angles are read directly from
  pixel rows. The camera's *reported* position puts it 6.9 m from the OSM front
  edge and 3.8 m from the parcel front edge — a 3.1 m disagreement that shows the
  reported position is itself unreliable, which is normal for Street View GPS in a
  street this narrow. So distance was solved from the panorama instead: the 9.47 m
  frontage subtends **56.9°**, which by the sine rule against the known 45.2°
  frontage bearing puts the camera **8.5 m** from the facade plane. At that
  distance, with a 2.5 m camera height, the top of the stucco band sits at
  **15.92 m** and the top of the window wall at **13.0 m**. The 0.23 m agreement
  with the LiDAR maximum is the strongest single result in this dossier; the
  weakest link in it is the camera height, and a ±0.3 m error there moves the
  crest ±0.3 m.

- **The storey count has a real conflict, and both sides are probably right.** The
  2005 construction permit says **4 story**; the Assessor's roll and every permit
  from 2016 on say **3**. The reading taken here — a commercial ground floor plus
  three residential levels — satisfies both, because a residential roll routinely
  counts only the dwelling levels, and it is the only reading consistent with a
  13.9 m deck (4.3 m commercial floor plus three at 3.2 m). Do not model two
  4.8 m loft levels: 6,240 sq ft of building area over a 3,000 sq ft footprint
  needs more than two floors even before the rear block steps down.

- **The rear elevation is unobserved.** No Street View, no clear aerial (permanent
  shadow), no listing photograph. The 8 m rear block described in 2.4 and 2.7 is
  *derived from the LiDAR height distribution*, which fixes the low fraction at
  ~24% of the footprint but says nothing about where the step is or whether it is
  a block, a court or a terrace. It faces nothing but the block interior, so the
  cost of being wrong is low — but do not present it as observed.

- **The solar array postdates the LiDAR.** The height data was captured in 2010
  and the array installed in 2012, so the array contributes nothing to the 16.15 m
  maximum. That is convenient: the crest question above cannot be explained away
  as PV.

- **`Toy_plum` is off-palette on purpose.** See 2.8. It is a WARN in
  `sf-asset-check`, not a failure, and it must be logged rather than quietly
  dropped or quietly kept.

- **The tenant will change before the model is rebuilt.** MGV took the commercial
  unit some time after 2018; before that the address hosted others, and the roll
  has changed hands once since 2011. Model the storefront as architecture — glazed
  grid, one recessed entry, one service bay — and no signage.

- **No architect was found.** Sixteen permits, the Assessor's roll and the parcel
  record name a contractor for none of the work and a designer for none of it, and
  there is no press coverage of this building — every South Park architecture
  story that mentions it is actually about 70 South Park. It is possible that the
  same period's designers worked on it, and it is possible it is a developer
  building. Do not attribute it to anyone in `REFERENCE.md` without a source.
