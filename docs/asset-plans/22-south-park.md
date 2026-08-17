# Hotel Madrid (22–24 South Park) — SF-SIM asset plan

A 1915 three-storey-over-basement wood-frame residential hotel on the north rim of
the South Park oval, built as the **Eimoto Hotel** to serve the Japanese community
that clustered around the park before the war. Mission Housing Development
Corporation bought and rehabilitated it in 1987 and has run it as the Hotel Madrid
ever since; it is 43–44 SRO rooms over one commercial storefront, and it is now the
third building in the **South Park Scattered Sites** rehabilitation alongside two
buildings this repo has already modelled — the Park View at 102 South Park
(`102-south-park`) and the Gran Oriente Filipino at 104–106 (`106-south-park`).

Visually it is the loudest thing on this stretch of the rim: **sage-green lap siding
with salmon-clay window casings, a deep bracketed cornice, a sage-green fire escape
on the street face, and a dark slate-blue taqueria storefront** under a rust belt
course. It is also the only building in this pair whose street facade **follows the
curve of the oval** — a 15 m frontage bowed 0.95 m, concave toward the park.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/22-south-park/`. This document is the plan only: Part 1 is the runnable
task prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `22-south-park` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3936498, 37.7822952` (DataSF surveyed parcel 3775-048 area centroid, measured — see 2.13) |
| Target height | **14.22 m** to the cornice crest; roof deck 12.39 m (LiDAR-derived, see 2.1 and 2.15) |
| Footprint | a **trapezoid**: party walls 36.28 m (north-east) and 30.13 m (south-west), Taber Place rear 13.68 m, South Park frontage a 14.99 m chord / 15.15 m arc; 444.5 m². Building 372.3 m² — the difference is a light well on the north-east flank (2.4) |
| Frontage | a **15.15 m concave arc**, sagitta 0.93 m, radius ≈ 30.8 m, sweeping 28° — the South Park oval turning |
| Triangle cap | 9,000 |
| Category | `7` (hotel — matching `102-south-park`, the other SRO on this block) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready Hotel Madrid (22–24 South Park) GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of the Hotel Madrid at 22–24 South Park in San
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
7. `artifacts/102-south-park/` and `artifacts/106-south-park/` — the two closest
   reference implementations. They are the **same building type in the same
   programme**: the Park View and the Gran Oriente Filipino are the other two SROs
   in the South Park Scattered Sites rehabilitation, on the same oval, and this
   asset must sit next to them as a sibling. Take their detail budget, their
   window-rhythm discipline and their night-glow restraint. Note the difference:
   both of those are stucco with punched openings, while this is **wood lap siding
   with a bracketed cornice and an exterior fire escape on the street face**.
8. `docs/asset-plans/22-south-park.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## What is already observed, and what is not

The **South Park (south-east) elevation and the Taber Place (north-west) rear were
both photographed** — Google Street View, January 2025 — and the roof was read from
2026 Vexcel near-nadir aerial. The colour scheme, the cornice, the fire escape, the
storefront and the rear's lap siding and clay trim are **observation**, not
inference (2.4). If your own research contradicts any of it, say so loudly in
`REPORT.md`.

Three things are genuinely open and you must settle them (2.15):

1. **The 14.22 m LiDAR maximum.** It is 2.9σ above the 12.39 m median on a
   footprint whose height standard deviation is only 0.63 m. Unlike most of this
   set, it **cannot** be party-wall contamination — both neighbours are shorter
   (10 South Park 11.88–12.27 m, 26–28 South Park 8.35 m), so a bleeding cell would
   pull the maximum *down*. That leaves two readings: the parapet-frieze-cornice
   assembly (this plan's choice, 1.83 m above the deck, normal for a 1915 hotel), or
   a street tree over the parapet — and there are mature street trees hard against
   this frontage. Settle it from imagery before you build.
2. **Whether the front elevation is lap siding or stucco.** The Taber Place rear is
   unambiguously lap siding. The front reads smooth at Street View resolution with
   faint horizontal banding, which is consistent with siding but not proof.
   It changes nothing about the massing and one groove pattern about the facade.
3. **The roof PV array.** The 2026 aerial shows a large dark array on this roof;
   the 2010 LiDAR that gives the heights predates it, and it is almost certainly
   from the 2019–21 rehabilitation. Confirm it, then build it — it is the dominant
   roof feature if present. Do **not** split the difference by inventing a token
   array.

## Must capture

- The **curved frontage**: 15.15 m of street face bowed 0.93 m concave toward the
  park. This is the cue that says "South Park oval" and nothing else on this
  asset does that job. Build it as three or four chamfered segments, not a
  many-segment arc.
- **Sage-green lap siding with salmon-clay window casings** — the colour pair is
  the building's signature and reads from the aerial camera.
- The **deep bracketed cornice** in rust-clay, crowning all three storeys — the
  single strongest identity feature and the thing that separates this from the
  flat-topped modern neighbours.
- The **sage-green fire escape** on the street face: landings at the 2nd and 3rd
  floors and a diagonal stair, painted the same green as the body, serving a door
  onto the 2nd-floor landing.
- The **dark slate-blue storefront** under a rust belt course: the taqueria at the
  south-west end with its round white exhaust fan, and the residential entrance at
  the north-east end under its **curved barrel awning**.
- **Three storeys of paired double-hung sash**, four bays across the street face,
  standing a clear storey above 26–28 next door and level with 10 South Park.
- A deliberately designed flat roof: the PV array, the light-well slot on the
  north-east flank, and grouped mechanical plant.

## Research Hotel Madrid independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- The two public elevations: the 13.7 m South Park front (south-east) and the
  13.7 m Taber Place rear (north-west). The two long 36.3 m sides are **party
  walls** and carry nothing.
- The roof, at higher resolution than the near-nadir aerial reached — this is where
  the PV question and the cornice-versus-tree question both get settled
- Day and night appearance
- The building's history as the **Eimoto Hotel** and its place in the pre-war
  Japanese South Park. Very little was found at plan time beyond an Alamy caption;
  a Japantown or SoMa historic context statement, a DPR 523 form, or the South Park
  Scattered Sites planning file would each be worth more than another photograph.
- The current rehabilitation (SCCS Group / Mission Housing, 106 units across three
  buildings) — it may have changed the storefront or the paint since Jan 2025

Prefer architect/engineer publications, owner or institutional material,
planning and permitting documents, architectural press, geolocated photography,
and aerial/satellite imagery. Never rely on a single photograph, a single
AI-generated image, or a single unsourced 3D model. Separate verified facts from
visual inference; if sources disagree, document the disagreement and decide.

**One source conflict is already known — re-check it, do not silently
re-inherit the wrong value:** the unit count is 55 rooms on the Assessor's roll,
"44 units" on apartments.com, "43 units" on the DAHLIA housing portal, and
"44+ units plus one commercial space" on Mission Housing's own page. They are
counting different things (rooms vs. tenanted units vs. subsidised units) and none
of them changes the model. Do not let a unit count drive the window count — the
**window count comes from the photographs**.

## Create a reference dossier

Write `artifacts/22-south-park/REFERENCE.md` containing: source links and what each
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

This is a **secondary building** in the style bible's detail budget (§21), not a hero
landmark: clear massing, one strong facade rhythm, a simple designed roof, and exactly
one identity cue carried hard — the green-and-clay cornice-over-siding front with its
fire escape. Resist adding hero-tier ornament.

The finished asset must be immediately recognizable as the Hotel Madrid, consistent
with the real building from all four sides and above, architecturally credible, and a
premium handcrafted miniature — not photorealistic, not voxel art, not generic
low-poly, and never accurate in one view while invented in the others.

## Scope of the exported asset

Export the single 1915 hotel block: body, the curved South Park elevation, the Taber
Place rear elevation, the two blind party walls, the cornice, the fire escape, the
storefront and its awning, the flat roof, the light well, the PV array (if
confirmed) and the mechanical plant.

Do not include unrelated surrounding city geometry: South Park itself, its trees or
lawn, Taber Place, the sidewalk, the street trees, the utility poles and overhead
wires, the neighbours at 10 South Park or 26–28 South Park, parked cars,
motorcycles, people, plinths, cameras or lights. **Do not model the "FOR LEASE"
banner or the taqueria's lettering** — see 2.10; tenant signage changes faster than
this model will be rebuilt. Temporary context may appear in review renders but must
not leak into the GLB.

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
entrance faces **south-east, bearing 135.2°**; the long axis runs 315.2°/135.2°
(NW–SE), so build directly on the measured footprint in 2.3 rather than modelling
an axis-aligned box and rotating it. The contract's "front faces −Y" cannot be
honoured literally here; real-world orientation wins (AGENTS rule 5) and the
deviation goes in `REPORT.md`.

**Height normalization:** the tallest geometry in the export (the cornice crest)
must land at exactly **14.22 m** so the loader's `targetHeightM / measuredHeight`
scale is 1.0.

## Reproducible Blender workflow

Blender 5.2 LTS. Headless: `blender -b --python script.py -- args`.

Keep `artifacts/22-south-park/build_22_south_park.py` (deterministic build script),
`artifacts/22-south-park/22-south-park.blend`, and
`artifacts/22-south-park/22-south-park.glb`. The script must rebuild the model reliably
enough for future revision. Do not modify or rename an unrelated existing GLB to satisfy
the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`22-south-park-top.png`, `22-south-park-north.png`, `22-south-park-east.png`,
`22-south-park-south.png`, `22-south-park-west.png`, plus
`22-south-park-contact-sheet.png`, at least one high three-quarter aerial beauty render
`22-south-park-aerial.png`, and a night render `22-south-park-aerial-night.png`.

The four elevations must share scale, framing, lighting, exposure and
projection; use orthographic or long-lens cameras; label directions from the
researched orientation; the top view must clearly show the full 36.3 × 13.7 m
roof — its PV array, light well and mechanical layout; the aerial view uses the
style bible's camera assumptions (30–50 degrees down, long lens). Simple tabletop
lighting, neutral warm background, minimal depth of field, and every image must
depict the same exported model.

Because the building is rotated 45° from the world axes, the four compass renders will
each show two faces at 45°. That is correct and expected — do not rotate the model to make
the elevations square on.

**Night renders: drive `_Glow` from Base Color, not from the imported emission.**
See `docs/asset-plans/README.md` — copy `Base Color` into `Emission Color` at
strength 1.0, or every glow surface renders as a white slab.

## Validate the exported GLB

Re-import `22-south-park.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture
count, camera count, light count, animation count, applied-transform status,
negative-scale status, normal-orientation status, unexpected geometry, and
per-material contract compliance. Render at least one review image from the
re-imported asset. Write `artifacts/22-south-park/validation.json` and
`artifacts/22-south-park/REPORT.md`.

Note that the axis-aligned XY bounding box will be roughly **35.3 × 35.3 m** even
though the building is 36.3 × 13.7 m — that is the expected consequence of a 315°
real-world heading, not a scale error.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "22-south-park",
  "file": "22-south-park.glb",
  "anchor": [
    -122.3936498,
    37.7822952
  ],
  "targetHeightM": 14.22,
  "cat": 7,
  "name": "Hotel Madrid (22–24 South Park)",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a separate, explicitly requested job — run `docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in `docs/asset-plans/22-south-park.md`.
````

---

## Part 2 — Research and design dossier

Compiled 16 August 2026 from the sources in 2.2. Values marked *inferred* are visual or
derived estimates, not published figures — the executing agent must re-verify
anything it relies on.

**A note on the evidence quality of this dossier.** The geometry is strong: the
surveyed parcel, the LiDAR footprint and the OSM trace agree, and the parcel's
polygon area matches the Assessor's `lot_area` to 2%. Both public elevations were
photographed in January 2025 and the roof was read from 2026 near-nadir aerial, so
2.4 is observation rather than inference. The weak points are the **history** —
"Eimoto Hotel, 1915, serving the Japanese community" rests on a single Alamy
caption and a Wikipedia summary, with no primary source found — and the **14.22 m
crest**, discussed in 2.15.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Built | **1915** | SF Assessor secured roll, `year_property_built = 1915`; Alamy caption "Madrid Hotel, built 1915"; apartments.com "built in 1915" |
| Original name / use | **Eimoto Hotel**, serving the Japanese community around South Park | Alamy stock caption; Wikipedia *South Park, San Francisco* — **single-thread, see 2.15** |
| Storeys | **3** over a basement | Assessor `number_of_stories = 3.0`; every permit from 1976 to 2023 records 3 |
| Structure | Type V wood frame with lap siding | SCCS Group project text ("Type V Wood Framed"); Assessor `construction_type = D`; permit 202305248516 ("removing bottom of siding"); **observed** on the Taber Place elevation |
| Rooms / units | **55 rooms**, 16 bathrooms, 3 units on the roll; 43–44 tenanted SRO units + 1 commercial space | Assessor; DAHLIA portal "43 units, 80–290 sq ft"; Mission Housing "44+ units"; apartments.com "44 units" — see 2.15 |
| Owner / operator | **Mission Housing Development Corporation**, acquired and rehabilitated **1987**; DBA "Hotel Madrid" registered 1988-07-01 | missionhousing.org/madrid; opengovus SF business registration 0955172-02-001 |
| Current programme | **South Park Scattered Sites** — this building with the Park View (102 South Park) and Gran Oriente Filipino (104–106 South Park); 106 units total at ≤ 80% AMI, ground floors reserved for restaurant tenants | SCCS Group project page; DAHLIA listing a0W4U00000KnGxgUAF |
| Soft-storey retrofit | 2017, both a residential and a commercial permit, to NOV 201642251 | permits 201707242768 and 201707242771 |
| Rehabilitation | **$2.1 M SRO rehab, filed Dec 2019** — new interiors, new MEP, roof drains and gutters repaired and replaced, exterior paint repaired in kind | permit 201912189908 |
| Awning | repaired 2023 with new paint and laminated safety glass | permit 202303284538; **observed** as a curved barrel awning over the residential entrance |
| Light well | **exists** — 2023 waterproofing of a light well leaking into the basement | permit 202305248516; corroborated by the DataSF footprint's 372 m² against a 444 m² lot |
| Roof, historic | solar **hot-water** collector panels installed 1985 | permit 8501207 — probably long gone; the modern PV is a separate question, see 2.15 |
| Reroofing | 1996 ($44 k), roof repairs 1984 | permits 9621246, 8413281 |
| Elevator | residential elevator serving ground floor and basement only, 1997 | permit 9707488 — **so there is no elevator overrun on the roof** |
| Ground-floor tenant | a taqueria (Mexican grill), with a "FOR LEASE" banner in Jan 2025; a deli occupied it in 1985 | **observed**; permit 8508287 ("remodel on existing deli") |
| Block / lot | 3775 / 048, APN 3775-048 | DataSF parcels, SF Assessor |
| Addresses | 22 South Park (business and tenant address) = 24 South Park (storefront number) | DataSF EAS addresses; Assessor `property_location = 0024 0022 SOUTH PARK` |
| Lot area | 4,893.3 sq ft (454.6 m²) | SF Assessor `lot_area`; the parcel polygon measures 444.5 m² (4,785 sq ft) |
| Building area | 12,729 sq ft (1,182 m²) | SF Assessor `property_area` — 372.3 m² × 3 storeys = 1,117 m², consistent |
| Footprint (parcel, survey) | a trapezoid, **444.5 m²**; party walls 36.28 / 30.13 m at bearing 315.18°, rear 13.68 m, frontage a 14.99 m chord. Bounding rectangle 36.28 × 13.68 m | DataSF parcels `acdm-wktn`, blklot 3775048, reprojected — **measured** |
| Footprint (LiDAR, building) | 35.92 × 13.49 m bounding rectangle, **372.3 m² actual** | DataSF `ynuv-fyni` SF3775048 — **measured**; the 72 m² shortfall is the light well |
| Frontage curvature | **concave arc, chord 14.99 m, arc 15.15 m, sagitta 0.93 m, radius ≈ 30.8 m, sweep 28°** | measured from the 25-vertex parcel arc — **measured**, and reproduced by the LiDAR ring at 0.5–0.6 m |
| Roof crest | **14.22 m** above ground | DataSF LiDAR `hgt_maxcm = 1422` — **measured**, interpretation open (2.15) |
| Roof deck | **12.39 m** (median), 12.35 m (mean), 12.52 m (majority) | DataSF LiDAR `hgt_mediancm/meancm/majoritycm` — **measured**; three statistics within 13 cm |
| Height std dev | **0.63 m** | DataSF LiDAR `hgt_stdcm = 62.6` — a very flat roof |
| LiDAR minimum | 9.31 m | DataSF LiDAR `hgt_mincm = 931` — **the light well**, not an artifact (2.15) |
| OSM height tag | 12 | OSM way/112926338 — 0.4 m below the LiDAR median; read as a rounded storey estimate |
| Ground elevation | 12.36 m (NAVD88) | DataSF LiDAR `gnd_min_m` — app terrain handles this, not the asset |
| Zoning | **SPD** (South Park District) | DataSF parcels; Assessor |
| Neighbourhood | Financial District/South Beach; Assessor neighbourhood 9B, Financial District South | DataSF parcels |
| Neighbour heights | 10 South Park (SF3775106) 11.88 m and 12.27 m median across two footprints; 26–28 South Park (SF3775049) **8.35 m**; 44–46 (SF3775217) 13.52 m | DataSF LiDAR — **both direct party-wall neighbours are shorter than this building** |
| Last sale | 29 May 2020 (transfer into the Scattered Sites partnership) | SF Assessor `current_sales_date`; the Mission Housing business registration closes 2020-05-31 |

### 2.2 Sources

- https://www.openstreetmap.org/way/112926338 — footprint, `addr:housenumber=22;24`, `addr:street=South Park`, `height=12`
- `https://data.sfgov.org/resource/ynuv-fyni` (DataSF Building Footprints, LiDAR-derived, **2010 survey** — the `p2010_*` fields date it) — footprint SF3775048, heights 14.22 / 12.39 / 9.31 m, std 0.63 m
- `https://data.sfgov.org/resource/acdm-wktn` (DataSF Parcels) — parcel 3775-048, 22–24 SOUTH PARK, zoning SPD — the surveyed footprint used as this plan's geometry
- `https://data.sfgov.org/resource/wv5m-vpq2` (SF Assessor secured roll) — 1915, 3 storeys, 55 rooms, use code COMH / Commercial Hotel, welfare exemption, sold May 2020
- `https://data.sfgov.org/resource/i98e-djp9` (SF Building Permits) — 30 permits on block 3775 lot 048: the 1983–85 rehabilitation ($492 k) and community-kitchen expansion, the 1985 solar hot-water panels, the 1996 reroof, the 1997 elevator, the 2011 fire-alarm upgrade, the 2017 soft-storey retrofit, the 2019 $2.1 M SRO rehab, the 2023 awning repair and light-well waterproofing
- `https://data.sfgov.org/resource/ramy-di5m` (DataSF addresses) — 22 and 24 South Park, block 3775 lot 048
- https://www.missionhousing.org/madrid — Hotel Madrid, SRO acquired and rehabbed 1987, permanent housing for formerly homeless and very low-income adults, 44+ units plus one commercial space
- https://www.sccsgroupllc.com/projects/south-park-scattered-sites — the current rehabilitation: Hotel Madrid with the Parkview (102) and Gran Oriente (106), Type V wood framed, 106 units at ≤ 80% AMI, ground-floor restaurant tenancies
- https://housing.sfgov.org/listings/a0W4U00000KnGxgUAF — DAHLIA listing: 43 SRO units, 80–290 sq ft, community room, shared kitchens, 24-hour desk
- https://www.apartments.com/hotel-madrid-san-francisco-ca/syxvkv6/ — "22-26 S Park St", built 1915, 3 stories, 44 units
- https://www.alamy.com/stock-photo-madrid-hotel-built-1915-south-park-san-francisco-142428598.html — "Madrid Hotel, built 1915" and the **Eimoto Hotel** attribution
- https://en.wikipedia.org/wiki/South_Park,_San_Francisco — the oval's 1852 assembly, its London-square model, and the Madrid/Eimoto succession
- https://www.foundsf.org/RESIDENTIAL_vs._TOURIST_HOTELS — the Madrid as a residential (not tourist) hotel through the 1980s conversion fights
- https://opengovus.com/san-francisco-business/0955172-02-001 — Mission Housing Dev Corp DBA Hotel Madrid, 22 S Park St, 1988-07-01 to 2020-05-31
- Google Street View, **January 2025**, panorama near `37.78205,-122.39356` (the South Park elevation, headings 300–360°) and near `37.78249,-122.39391` (the Taber Place rear) — **observed**
- Google Maps satellite (Vexcel Imaging 2026, near-nadir, `37.7822952,-122.3936498` at z21) — the flat roof, the PV array and the light well, **observed**

### 2.3 Orientation and placement

The building is a through-lot on the north rim of the South Park oval, running from
South Park at the south-east to Taber Place at the north-west. Both long sides are
party walls: 10 South Park to the north-east, 26–28 South Park to the south-west.
The oval's rim runs at bearing 45.2°/225.2°, so the lot runs 315.2°/135.2°.

**The lot is a trapezoid, not a rectangle.** Corners in Blender coordinates
(metres, `+X` east, `+Y` north), centred on the anchor `-122.3936498, 37.7822952`,
read off the surveyed parcel's own vertices:

```
(  18.78,  -9.51)   East corner    (South Park x the 10 South Park party wall)
(   4.75, -14.79)   South corner   (South Park x the 26-28 party wall)
( -16.49,   6.58)   West corner    (Taber Place x the 26-28 party wall)
(  -6.79,  16.23)   North corner   (Taber Place x the 10 South Park party wall)
```

in ring order: `E → S → W → N`.

Edges, with outward normals:

| Edge | Length | Faces | Elevation |
|---|---|---|---|
| E corner → S corner | 14.99 m chord, 15.15 m of arc | SE, chord bearing 249.4° | **South Park front** — curved |
| S corner → W corner | 30.13 m | SW 225.2° | **party wall** with 26–28 (blind) |
| W corner → N corner | 13.68 m | NW 315.2° | **Taber Place rear** |
| N corner → E corner | 36.28 m | NE 45.2° | **party wall** with 10 South Park (blind) |

The two party walls are parallel (315.18°/135.18°) and the Taber Place rear is
square to them, but **the South Park frontage is not** — its chord runs at 249.4°,
24° off square, because the oval turns through this lot. That is what makes the
north-east party wall 36.28 m and the south-west one only 30.13 m, and it is why
the frontage chord is 14.99 m against a 13.68 m rear. The 36.28 × 13.68 m
oriented bounding rectangle quoted elsewhere is the *bounding box*, not the lot.

Chord-quad area 454.2 m²; the concave arc removes a 9.7 m² segment, giving the
measured 444.5 m². The Assessor's `lot_area` of 4,893.3 sq ft (454.6 m²) matches
the chord quad, as lot areas from straight-line dimensions always will.

**The front is an arc, not a chord.** The 25 measured vertices along the South Park
edge fit a circle of radius ≈ 30.8 m concave toward the park, sweeping 28°; the
mid-face sits 0.93 m further from the park than the chord between the corners.
Build it as four segments, which reproduces the sagitta to within 6 cm, costs
almost nothing, and conveniently gives **one segment per facade bay**:

```
(  18.78,  -9.51)      E corner          segment 1 = 3.68 m
(  15.16, -10.17)                        segment 2 = 3.68 m
(  11.63, -11.21)      mid-face, 0.93 m behind the chord
(   8.22, -12.61)                        segment 3 = 3.69 m
(   4.75, -14.79)      S corner          segment 4 = 4.10 m
```

Total arc 15.15 m. The tangent swings from ~263° at the East corner to ~225° at
the South corner, where it meets 26–28 South Park's straight frontage square —
the neighbour is on the part of the rim that has stopped turning.

Because of the 315° heading the axis-aligned bounding box is ~35.3 × 35.3 m. That
is correct.

### 2.4 What each side shows

Two of these four are **observed** from Google Street View, January 2025. The two
long sides are party walls and are not visible from anywhere.

**South-east (South Park) — observed, Jan 2025.** The address elevation, 13.7 m
wide (15.0 m of curved face), three storeys over a storefront. The body is
**sage/sea-green** — a muted grey-green — in what reads as lap siding. The upper two
floors carry **paired double-hung sash windows** set in single wide openings with
**flat salmon-clay casings** roughly 150 mm wide, the sashes white, several with
venetian blinds. Four bays across: reading south-west to north-east, a window pair,
a window pair, the **fire-escape bay** (a door onto the landing rather than a
window), and a window pair. The rhythm is identical on the 2nd and 3rd floors.

The **fire escape** is painted the same sage green as the body and is the loudest
object on the elevation: cantilevered landings at both upper floors with
horizontal-bar railings, a diagonal stair between them, and a drop ladder. It sits
over the north-east half of the face.

A **deep bracketed cornice** in rust-clay crowns the wall — a projecting crown with
a soffit and widely spaced square brackets. It is the only classical gesture on the
building and it is what makes it read as 1915 rather than 1975.

A **rust-clay belt course** separates the storefront from the upper floors, running
the full width and returning at both ends.

The **ground floor is a dark slate-blue storefront band**. South-west half: the
taqueria — plate glass in white frames, a recessed glazed entrance, "24" above the
door, a transom sign band, and a **round white louvered exhaust fan** at the
south-west end of that band. North-east half: the residential entrance, its frame
picked out in rust-clay, under a **curved barrel awning**, with a further glazed bay
beside it. A low bulkhead runs beneath the glazing.

**North-west (Taber Place) — observed, Jan 2025.** A finished elevation, not a
service back: the same **sage-green lap siding** (clearly readable as horizontal
boards here) with the same **salmon-clay trim**. It carries a shallow canted **bay
window** at the upper floors, two tall **arched-headed ground-floor windows behind
ornate clay-painted security grilles**, a flush clay door beside them, and a wide
clay panelled service door at the south-west end. The green fire escape returns
onto this face at the top. A security camera and a wall light are fixed to the
siding.

**North-east and south-west — party walls.** Blind. 10 South Park to the north-east
is 11.9–12.3 m, and 26–28 South Park to the south-west is 8.35 m — so **roughly
4 m of this building's south-west flank stands exposed above its neighbour's roof**
and will be seen from the aerial camera. Model that strip as plain siding carried
up to the cornice; the north-east flank is effectively buried.

**Top — observed, Vexcel 2026 near-nadir.** A flat roof at 12.39 m carrying a
**large dark PV array** over most of its area, laid out in long bands running
north-west to south-east — consistent with the 2019–21 rehabilitation and with the
arrays visible on the other rehabilitated SRO roofs on this block (see
`docs/asset-plans/106-south-park.md` §2.9). A **light-well slot** is notched into
the north-east flank around mid-depth — the DataSF ring traces it as a slit roughly
16 m long and under 2 m wide, and it is what puts the LiDAR minimum at 9.31 m.
Mechanical plant is grouped toward the Taber Place end. The cornice reads as a
bright edge along the South Park end.

### 2.5 Recognition cues (ranked)

1. **Sage green and salmon clay.** The colour pair — green body, clay window
   casings, clay cornice and belt course — is unique on this block and survives
   every simplification. Nothing else identifies this building faster.
2. **The bracketed cornice**, a deep projecting crown over three storeys, on a rim
   where the immediate neighbours are flat-topped.
3. **The green fire escape on the street face** — most SF fire escapes are black;
   this one is painted out in the body colour and reads as part of the facade.
4. **The curved frontage** following the oval, 0.93 m of bow over 15.15 m — and a lot that is 6 m deeper on one side than the other because of it.
5. The dark slate-blue storefront with its round white fan and the curved barrel
   awning over the residential entrance.

### 2.6 Miniature translation

**Preserve**

- The trapezoid footprint (36.28 / 30.13 m party walls) and the real 315.2° heading, exactly
- The **curved front**, as four chamfered segments
- The sage/clay colour pair, on both public elevations
- The cornice as a real projecting volume, not a painted stripe
- The fire escape as a green object on the street face
- Three storeys standing one clear storey above 26–28 and level with 10 South Park
- The flat roof with its PV array and its light-well slot

**Simplify / exaggerate**

- **Paired sash becomes one glazed panel per opening** with a single clay casing
  band — no meeting rails, no muntins. The casing is the cue, not the sash.
- The window openings may be pushed slightly larger so the clay casings stay
  legible from the aerial camera — this is the one place to spend semantic
  exaggeration
- The **cornice is exaggerated**: give it a deeper projection and fewer, chunkier
  brackets (five or six across the face, not the real dozen). At the app's camera a
  correctly-scaled bracket course is grey mush; a chunky one reads as "1915".
- The fire escape becomes two solid-sided landings and one diagonal stair slab,
  no individual balusters and no drop ladder
- The storefront becomes one dark band with three openings broken out (taqueria
  glazing, taqueria entry, residential entry under its awning) plus the round fan
  as a single low cylinder
- The Taber Place bay window becomes one shallow canted box; the arched grille
  windows become two plain recessed openings
- Lap siding becomes flat colour with, at most, two or three shallow horizontal
  grooves per storey — never a board-by-board groove pattern

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not
a straitjacket — adjust after the first aerial review render.

1. Body: extrude the 2.3 polygon (with the four-segment curved front) from z=0 to
   the roof deck z=12.39, `Toy_verdigris`.
2. Storefront band, z=0 to z=4.30: `Toy_navy`, on the South Park face only, carried
   3 m around neither flank (the flanks are party walls).
3. Storefront openings, z=0.55 to z=3.95: on the curved face, three recesses 0.18 m
   deep in `Toy_glass` behind a 0.12 m `Toy_trim` frame — a 5.2 m taqueria window,
   a 1.4 m taqueria entry, a 2.2 m residential entry. The residential entry's frame
   is `Toy_rust`, not `Toy_trim`.
4. Round exhaust fan: a 0.55 m diameter, 0.12 m deep 12-segment cylinder in
   `Toy_trim` on the storefront band at the south-west end, z≈3.55.
5. Barrel awning: a quarter-cylinder (8 segments) 2.6 m wide, 1.0 m projection,
   `Toy_rust`, over the residential entry at z=3.95.
6. Belt course: a 0.35 m `Toy_rust` band projecting 0.15 m at z=4.30, across the
   South Park face and returning 0.4 m onto both flanks.
7. Second floor, z=4.75 to z=8.45: four openings on the curved face at ~3.5 m
   centres — three glazed (`Toy_glass`, recessed 0.16 m, framed by a 0.22 m
   `Toy_sand` casing band) and one door onto the fire escape (`Toy_ink`).
8. Third floor, z=8.75 to z=12.15: the same four openings, all four glazed.
9. Taber Place rear, same two floor bands: one shallow canted bay 2.6 m wide
   projecting 0.5 m at the upper two floors, two glazed openings beside it, and at
   ground level two recessed openings and one `Toy_sand` door.
10. Cornice, z=12.39 to **z=14.22**: a `Toy_rust` frieze from 12.39 to 13.30, then a
    crown projecting 0.55 m from 13.30 to 14.22, with **six** `Toy_rust` brackets
    0.35 m wide dropped 0.6 m below the crown across the South Park face and three
    across Taber Place. This is the crest and must land at exactly 14.22 m.
11. Roof deck, z=12.39 to z=12.51: a thin flat slab in `Toy_stone` inside the
    cornice line.
12. Light well: a 15.0 × 1.8 m slot cut into the roof on the north-east flank at
    mid-depth, floor at z=9.31, walls `Toy_verdigris`, floor `Toy_ink`.
13. PV array: two bands of flat panels, `Toy_navy`, 0.25 m above the deck on
    `Toy_steel` rails, running north-west to south-east over the south-west two
    thirds of the roof, clear of the light well and set back 1.2 m from the cornice.
14. Mechanical: three `Toy_steel` boxes (~1.4 × 1.0 × 0.7 m) and one 0.9 m
    10-segment cylinder grouped at the Taber Place end.
15. Fire escape: on the South Park face over the north-east half — two 3.0 × 1.0 m
    landings at z=4.75 and z=8.75 with 1.0 m solid side panels and one diagonal
    stair slab between them, all `Toy_verdigris`.
16. Bevel 0.12 m, 2 segments.

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_verdigris` | `9fb8a8` | body walls on both public elevations and both party walls; the fire escape |
| `Toy_sand` | `ece4d4` | window casings on the upper floors, the Taber Place bay and door |
| `Toy_rust` | `a86444` | the cornice, its brackets, the belt course, the barrel awning, the residential entry frame |
| `Toy_navy` | `2c4a70` | the storefront band; the PV array |
| `Toy_glass` | `2a4d73` | all windows and the storefront glazing |
| `Toy_trim` | `f3efe6` | storefront window frames, the round exhaust fan |
| `Toy_stone` | `d9d2c2` | the flat roof deck |
| `Toy_steel` | `9aa0a6` | PV rails, mechanical plant |
| `Toy_ink` | `3a3530` | the fire-escape door, the light-well floor, the storefront bulkhead |
| `Toy_glassl_Glow` | `6f95b8` | five lit upper windows at night |
| `Toy_mustard_Glow` | `d9a441` | the taqueria storefront spill at night |

Two notes on colour:

- **`Toy_verdigris` at `9fb8a8` is the closest palette entry to the observed sage.**
  The real green is a shade darker and greyer; do not reach outside the palette for
  it, and do not substitute `Toy_teal` (`3fa8a0`), which is far too saturated and
  would make the building read as a novelty.
- **`Toy_sand` over `Toy_verdigris` reproduces the observed casing contrast**, which
  is a warm pale clay against a cool grey-green. `Toy_brick` and `Toy_coral` are both
  too saturated for a window casing at this scale; keep the saturated clay
  (`Toy_rust`) for the cornice, the belt course and the awning, where the larger
  areas can carry it.

**Night state (required).** Glow surfaces must be thin **closed** shells proud of
the opaque glazing — the app renders `_Glow` in a separate layer that is ~12%
alpha by day, so a primary surface must never be authored as glow. Author them
closed, not as open faces: the normals contract runs a per-object signed-volume
test and an open plane has none. A closed shell is two alpha layers, so it reads
~23% by day rather than 12% — cover only part of each opening, in a desaturated
colour, and keep the fill, glow and frame planes at distinct offsets so no two
are coplanar. Hero glow: the **taqueria storefront**, warm (`Toy_mustard_Glow`),
across the south-west half of the ground floor — this is the one genuinely lit and
busy thing on this stretch of the rim at night. Supporting accent: **five** of the
eight upper windows lit, unevenly and never a full row — this is 43 rooms of
supportive housing, so a fully lit grid would read as an office and an evenly lit
one as an institution. The residential entrance gets nothing; the Taber Place rear,
the party walls, the fire escape and the roof stay dark.

### 2.9 Top surface

36.3 × 13.7 m of flat roof at 12.39 m, one of the lower roofs on a block the camera
flies over constantly, and overlooked from 2 South Park and the taller Second Street
blocks. Three things carry it:

1. **The PV array** — if confirmed (2.15), it is the dominant feature and the roof
   should be composed around it: two clean bands running with the long axis, tight
   and rectilinear, leaving the Taber Place end for plant.
2. **The light-well slot** on the north-east flank, a genuine dark incision in an
   otherwise flat plane and the only thing on this roof that is not a rectangle
   lying flat. It is also honest — the permit record proves it.
3. **The cornice edge**, reading as a bright `Toy_rust` band along the curved South
   Park end against the pale `Toy_stone` deck, and as the one curved line in the
   composition.

The **stepped neighbours** do the rest for free: this roof sits ~4 m above 26–28's
and ~0.2–0.5 m above 10 South Park's, so in the baked city it is a distinct plane
rather than part of a continuous surface.

### 2.10 Scope

**In the GLB:** the single 1915 hotel block — body, the curved South Park elevation
with its storefront, belt course, windows, fire escape and cornice; the Taber Place
rear with its bay, windows and doors; both blind party walls carried to the cornice;
the flat roof, the light well, the PV array and the mechanical plant

**Not in the GLB:** South Park, its trees or lawn, Taber Place, the sidewalk, street
trees, the utility pole and overhead wires, the neighbours at 10 or 26–28 South
Park, vehicles, motorcycles, people, plinths, cameras or lights

**Deliberately excluded: all tenant signage.** The "MEXICAN GRILL • TAQUERIA •
BURRITOS • TACOS" transom lettering, the "TCP TOUCHSTONE FOR LEASE" banner and the
"24" address numeral are real in the January 2025 capture and all three will
outlive this model by less time than the model will live. Model the storefront as
architecture — a dark band, three openings, one fan, one awning — and record the
omission in `REPORT.md`. The same applies to the wall-mounted security camera and
lantern on Taber Place.

### 2.11 Triangle budget

Cap 9,000 — a secondary building, and the cap should bind. Suggested split: body,
party walls and the four-segment curved front ~0.9k; the storefront band and its
three openings ~0.8k; the fan and the barrel awning ~0.4k; the belt course ~0.3k;
the sixteen upper-floor openings across two elevations ~2.4k; the cornice, frieze
and nine brackets ~1.6k; roof deck and light well ~0.5k; the PV array ~0.7k;
mechanical ~0.5k; fire escape ~0.6k.

Two places this budget can run away. **The cornice brackets**: nine chunky boxes
with a 0.12 m bevel is ~1.6k on its own, and modelling the real dozen-per-face at
correct scale triples it while reading worse. **The PV array**: model it as two
solid slabs with a rail underneath, never as individual panels — a real array here
is 40-plus modules and would eat the entire budget for something that reads as one
dark rectangle at 60 m.

### 2.12 Draft manifest entry

```json
{
  "id": "22-south-park",
  "file": "22-south-park.glb",
  "anchor": [
    -122.3936498,
    37.7822952
  ],
  "targetHeightM": 14.22,
  "cat": 7,
  "name": "Hotel Madrid (22–24 South Park)",
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

- **New landmark.** Add a `pipeline/lib/landmarks.mjs` entry (`id: '22SouthPark'`
  in the registry's own naming, `lon: -122.3936498`, `lat: 37.7822952`,
  `height: 14.22`, `exclude: 4.5`) and re-bake the affected tiles, or the baked
  procedural building on this exact footprint will intersect the GLB.
- **The exclusion band was measured against both bake inputs**, not reasoned from
  the building's dimensions — `pipeline/data/buildings_datasf.geojson` and
  `pipeline/data/overture_buildings.geojsonseq`, applying `excluded()`'s real test
  (centroid **or** any ring vertex inside the radius). From the anchor above:

  | ring | trigger distance |
  |---|---|
  | **own** DataSF `SF3775048` (via its centroid) | **0.63 m** |
  | **own** Overture `638a2a32-…-b99c-` (via its nearest vertex) | **2.21 m** — the floor |
  | 26–28 South Park, DataSF `SF3775049` | **6.90 m** — the ceiling |
  | 26–28 South Park, Overture `5bdb7723-…-b2c6-` | 7.02 m |
  | 10 South Park, DataSF `SF3775106` | 9.10 m |
  | 10 South Park, Overture `d364994a-…-b5e3-` | 9.13 m |

  The safe window is **(2.21, 6.90) m** and `exclude: 4.5` sits near its middle with
  2.3 m of margin below and 2.4 m above. **The floor is the Overture ring, not the
  DataSF one** — `addBuilding()` returns null on exclusion so `markOccupied()` never
  runs, and a radius under 2.21 m lets the Overture gap-fill re-add this building on
  top of the asset.
- **Expect the re-bake to drop exactly two rings, both this building's** — the
  DataSF footprint and its Overture twin. Do not count drops, check *which*: every
  dropped ring's centroid must sit within a couple of metres of the anchor. See
  `docs/asset-plans/126-south-park.md` and the two-rings note in
  `docs/asset-plans/README.md`.
- **26–28 South Park is being built in the same batch** (`docs/asset-plans/26-south-park.md`,
  `exclude: 3.4`). The two radii do not overlap each other's footprints: at 4.5 m
  this entry stops 2.4 m short of 26–28's DataSF ring, and at 3.4 m that entry stops
  2.4 m short of this one's Overture ring (5.77 m) and 3.9 m short of its DataSF
  ring (7.28 m). Whichever lands first, the other still bakes correctly.
- `loadRadius`: the skill's default formula gives `max(2500, 14.22 × 30) = 2500` m.
  Take the default.
- **Verify with `pipeline/audit.mjs` check 1.6 after the re-bake** and confirm
  visually that 10 South Park and 26–28 South Park are both still standing before
  committing.
- This is the twenty-first South Park-area building in the landmark manifest. The
  same standing question applies as for 181 and 188: a manifest of one-off SoMa
  blocks will not stream well forever, and the kit/instancing route
  (`KIT-INTEGRATION-PROMPT.md`) is the better long-term home for buildings of this
  class. This one has a better claim to landmark status than most of the row — a
  named 1915 residential hotel with a documented ethnic history and a live
  affordable-housing programme — but the argument is about the row, not this file.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Bounding-box top exactly 14.22 m — the cornice crest, not a mechanical unit and not the PV (loader scale lands at 1.0)
- [ ] Dimensions plausible in meters and consistent with 2.1 (XY bbox ~35.3 × 35.3 m is expected)
- [ ] The footprint is still the measured trapezoid in plan (36.28 / 30.13 m party walls, 13.68 m rear) — measure it, do not eyeball it
- [ ] **The front face is curved**, sagitta 0.90–0.96 m over the 15.15 m arc — measure it
- [ ] The roof deck sits at 12.39 m and the light-well floor at 9.31 m
- [ ] Triangles at or under 9,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the five lit windows and the taqueria; each a thin closed shell proud of the opaque glazing, covering at most the lower half of its opening
- [ ] Both party walls have no openings; the south-west flank is finished up to the cornice (4 m of it is exposed above 26–28)
- [ ] No tenant signage, no address numeral, no banner in the export
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (per-object signed volume for the union of solids; ray test residual ≤ 0.15%)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + contact sheet + night render regenerated from the final export
- [ ] The 2.15 cornice question answered in `REPORT.md`, with the evidence that answered it
- [ ] The PV question answered in `REPORT.md` — present and modelled, or absent and omitted, never split

### 2.15 Open questions and risks

- **How much of the 14.22 m LiDAR maximum is cornice?** The maximum sits 1.83 m
  above a 12.39 m median on a footprint whose height standard deviation is 0.63 m —
  a 2.9σ outlier. `docs/asset-plans/README.md` records the two traps this could be:
  592 Third Street, where a 6σ maximum was street-tree canopy over a parapet, and
  the Earl Warren Building, where a maximum 19 m above the roof plane was a single
  0.5 m cell sampling a party-wall neighbour's tower. **The party-wall trap is ruled
  out here** — both neighbours are *shorter* than this building (10 South Park
  11.88–12.27 m, 26–28 South Park 8.35 m), so a bleeding cell can only pull the
  maximum down. The street-tree trap is not ruled out: mature trees stand hard
  against this frontage in every Street View capture. Against that, a 1915
  three-storey residential hotel with the bracketed cornice visible in the January
  2025 photographs will carry a frieze-and-crown assembly of very nearly this depth,
  and the matching 9.31 m *minimum* is explained by a permit-confirmed light well
  rather than by an edge artifact — which raises confidence in the record as a
  whole. The reading taken here is a 1.83 m parapet-frieze-cornice assembly.
  **The risk is contained:** because the model is authored with the cornice crest at
  exactly 14.22 m, the loader's scale is 1.0 and an error in this number makes the
  cornice deeper, not the building taller. But settle it from imagery if you can.
- **The Eimoto Hotel attribution rests on one source.** "Built 1915 as the Eimoto
  Hotel to serve the Japanese community around South Park" comes from an Alamy
  stock-photo caption and a Wikipedia summary of the same claim. It is highly
  plausible — pre-war South Park had a substantial Japanese population and the
  neighbouring Gran Oriente Filipino at 104–106 was itself the Hotel Maruichi/Omiya
  in the 1920s (see `docs/asset-plans/106-south-park.md`) — but no primary source
  was found. It affects nothing about the model and everything about how the
  building is described. Flagged so the next researcher does not repeat the search
  blind; a SoMa or Japantown historic context statement is the place to look.
- **Is the PV array real, and is it this roof's?** The 2026 Vexcel aerial shows a
  large dark array on the roof at this anchor. The heights come from the **2010**
  LiDAR, which predates it, so the array cannot be cross-checked against the height
  record — and the near-nadir imagery has enough parallax at this zoom that
  attributing an array to one of two adjacent 13 m roofs is not free. The 2019–21
  $2.1 M rehabilitation and the pattern across the other rehabilitated SRO roofs on
  this block both point the same way. Confirm before building; if it is absent, the
  light well and the cornice carry the roof alone and the roof stays deliberately
  sparse.
- **Front cladding: siding or stucco?** The Taber Place rear is unambiguously
  horizontal lap siding. The South Park front reads smooth at Street View resolution
  with faint horizontal banding. A 1915 wood-frame building is very unlikely to have
  a stuccoed front and a sided back, but a mid-century re-cladding of the street
  face would not be unusual either. It changes one groove pattern and nothing else.
- **The storefront changes tenants faster than the model will be rebuilt.** A deli
  in 1985, a taqueria and a "FOR LEASE" banner in January 2025, and a restaurant
  tenancy reserved under the current rehabilitation. Model the band as architecture
  and do not model signage (2.10).
- **The current rehabilitation may have changed the exterior since Jan 2025.** SCCS
  Group's South Park Scattered Sites work is live. The 2019 permit repaired the
  exterior paint "in kind" and the 2023 permit repainted the awning, so the scheme
  in the January 2025 capture is recent — but check for newer imagery before
  building, and record the capture date you modelled from in `REPORT.md`.
- **The Assessor still codes this parcel `COMH` / Commercial Hotel** with a welfare
  exemption. That is accurate for a nonprofit-owned residential hotel and the
  manifest entry uses `cat: 7` (hotel) on that basis, matching `102-south-park`
  (the Park View, the other SRO on this block). `cat: 2` (apartments) — as used by
  `106-south-park`, which converted to studios — is the defensible alternative if
  the current rehabilitation re-tenures this building the same way.
