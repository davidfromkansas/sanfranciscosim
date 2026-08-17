# 27 South Park — SF-SIM asset plan

The middle third of the 1919 warehouse at **21–29 South Park Street**, a contributing
resource in the potential South Park Historic District. One building, three addresses:
a two-storey load-bearing masonry warehouse extended twice in the early 1920s (Fred
Koldenstadt, 1920; Caspar Zwierlein, 1921), its three sections originally "connected
with fire doors" and cut apart by two party walls during the 1993 UMB retrofit. 27 is
the centre section — a **12.19 m frontage on a 33.5 m deep lot**, blind on both flanks,
with exactly one public elevation.

That elevation is the whole asset. Painted brick, a run of **six segmental-arched
second-floor windows** in dark blue-green metal, and a ground floor of tall dark
joinery — transom lights over a beaded panel band over a big opening — with **one
mahogany double door** at the address number. In a district the survey describes as
"jack-arch window and door openings", this is the arcaded one.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/27-south-park/`. This document is the plan only: Part 1 is the runnable task
prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `27-south-park` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3931439, 37.7817369` (OSM way/112759868 area centroid ≡ its OBB centre, measured — see 2.13 for why not a DataSF centroid) |
| Target height | **10.20 m** to the parapet coping; roof deck 9.60 m (LiDAR-derived, see 2.1 and 2.15) |
| Footprint | 12.19 m frontage (NW, onto South Park) × 33.5 m deep (NW–SE), 408.3 m²; a parallelogram on the 134.8°/314.8° line — measured |
| Triangle cap | 7,000 |
| Category | `3` (office — office use in every permit since 2005) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 27 South Park GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of 27 South Park (the centre third of the
1919 warehouse at 21–29 South Park Street) in San Francisco and deliver it as a
downloadable, validated GLB.

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
7. `artifacts/140-south-park/` — the closest reference implementation. Same oval,
   same era, same shape class: a narrow-frontage two-storey industrial stick on the
   135°/315° line with one public elevation and blind flanks. Take its massing
   discipline, its detail budget and its treatment of party walls. Note the
   difference: 140 is wood-frame with a bracketed Italianate cornice; this is
   painted masonry with an arcade and no cornice brackets at all.
8. `docs/asset-plans/27-south-park.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## What is already observed, and what is not

The **north-west (South Park) elevation is observed** in detail — Google Street
View, Jan 2025, from three headings (2.2). The **roof is observed** at ~3 cm/px
from Google's 2026 nadir aerial (2.2, 2.9). The geometry is measured from the OSM
trace and cross-checked against the DataSF surveyed parcel and the DataSF LiDAR
footprint (2.3).

Three things are genuinely open and you must settle what you can (2.15):

1. **The crest.** 10.20 m is the USGS-LiDAR height for this building's own ring
   (Overture), read here as the parapet coping over a 9.60 m roof deck. The
   DataSF footprint for this parcel reports a 11.73 m maximum, which the nadir
   aerial says is rooftop mechanical plant, not architecture. Build to 10.20 m
   and keep the plant below the coping — see "Height normalization" below and
   2.15 for the full argument, which is the same one that excluded 2 South
   Park's flagpole.
2. **Where 27 stops and 21 and 29 start.** The frontage is 12.19 m by
   measurement and the address numeral "27" is visible on the facade beside a
   mahogany double door, but the row is continuous painted brick and the joints
   are not obvious in photographs. The bay rhythm in 2.7 is derived from the
   measured width, not counted off a photograph of a known 27-only extent.
3. **The rear (south-east) elevation was not observed at all.** It faces a
   2.5–6 m service gap behind Brannan Street and no photograph reaches it.

## Must capture

- **The arcade.** Six segmental-arched second-floor windows in dark blue-green
  metal, close-spaced on narrow painted-brick piers. This is the single loudest
  feature and the only arcade on this stretch of the oval — carry it hard.
- **The tall dark ground floor**: three bays of joinery, each a transom light row
  over a beaded panel band over a big opening, set in deep painted-brick reveals.
  The ground floor is nearly as tall as the storey above it.
- **The one mahogany door** at the address number — the single warm accent in a
  run of dark blue-green joinery, and the thing that says *27* rather than
  *21–29*.
- **A narrow, deep, two-storey stick**: 12.19 m of frontage against 33.5 m of
  depth, standing level with its neighbours, not above them.
- **Two blind party walls** carried full height with the parapet run across
  them. These will be VISIBLE in the app — see "Scope" below; do not leave them
  as raw untreated faces.
- **A flat roof designed to be looked down on**: light membrane inside a parapet
  ring, a tight cluster of white mechanical boxes and round fans in the middle
  third, and two low glazed skylight monitors.

## Research 27 South Park independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
crest height, the footprint, the WGS84 anchor, and the real-world orientation,
and gather references covering:

- The north-west (South Park) elevation at higher resolution than Jan 2025
  Street View reached, and from earlier capture dates — the shopfronts were
  replaced under permit in 2003 and the current joinery post-dates that
- Any view that resolves the party-wall joints, so bay 1 and bay 3 can be
  assigned to 27 rather than to 21 or 29
- The roof, ideally oblique rather than nadir, which is where the 11.73 m
  question gets settled
- The rear elevation, if anything reaches it
- Day and night appearance
- The DPR 523A form for APN 3775-042, if one exists — the district-level 523D
  (cited in 2.2) confirms contributor status and the 1919/1920/1921 build
  sequence but does not describe this facade

Prefer architect/engineer publications, owner or institutional material,
planning and permitting documents, architectural press, geolocated photography,
and aerial/satellite imagery. Never rely on a single photograph, a single
AI-generated image, or a single unsourced 3D model. Separate verified facts from
visual inference; if sources disagree, document the disagreement and decide.

**One attribution is already known to be unresolved — do not silently promote
it:** Perkins&Will's "South Park Venture Capital Firm" (completed 2023, 16,420
sq ft) renovated a 1920s brick-clad building on South Park with "large, arched
metal-clad windows". That description fits this warehouse and nothing else
nearby, but the practice publishes the client as confidential and no address,
and the 2020–2021 permits worth ~$2.4 M on this parcel are all filed under **21**
South Park. Treat it as evidence about the row's window language, not as a fact
about number 27.

## Create a reference dossier

Write `artifacts/27-south-park/REFERENCE.md` containing: source links and what each
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
one identity cue carried hard — the six-arch arcade over a tall dark shopfront band.
A 1919 utility warehouse had no ornament beyond its openings; do not invent any.

The finished asset must be immediately recognizable as 27 South Park, consistent with
the real building from all four sides and above, architecturally credible, and a
premium handcrafted miniature — not photorealistic, not voxel art, not generic
low-poly, and never accurate in one view while invented in the others.

## Scope of the exported asset

Export the single centre section: body, the north-west elevation with its arcade
and shopfront band, the two blind party walls, the rear elevation, the parapet
and coping, the flat roof, the mechanical cluster and the two skylight monitors.

**The party walls are public here and must be finished.** The re-bake at
integration removes the procedural mass of 21 and 29 along with this building's
own (2.13) — they share one polygon in the bake input and cannot be separated.
Until those two get their own GLBs, both flanks of this model are exposed to the
camera. Model them as plain painted brick with the parapet carried across and no
openings. Do not model 21 or 29 themselves.

Do not include unrelated surrounding city geometry: South Park itself, its lawn
or trees, South Park Street, the sidewalk, parked cars, the street trees, the
overhead wires and their poles, the wall-mounted lamps and cameras, the
neighbours at 21, 29, 17–19 or 33–35 South Park, people, plinths, cameras or
lights. Temporary context may appear in review renders but must not leak into
the GLB.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary
`.glb`; real-world meters; origin at base center; minimum geometry Z ~ 0;
applied transforms; no negative scales; outward normals; no duplicate or foreign
geometry; no image textures; no transparency; flat-color materials named `Toy_*`
from the project palette; `_Glow` suffix only on surfaces that glow at night; no
`Toy_body`; no cameras, lights, animations, armatures or constraints; no external
dependencies; at most 7,000 triangles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model
drops into the city at its real-world heading — the loader applies no rotation
(`placeGeneric` in `app/src/assets.js` only scales and positions). The South Park
entrance faces **north-west, bearing 314.8°**; the long axis runs 134.8°/314.8°,
so build directly on the measured parallelogram in 2.3 rather than modelling an
axis-aligned box and rotating it. The contract's "front faces −Y" cannot be
honoured literally here; real-world orientation wins (AGENTS rule 5) and the
deviation goes in `REPORT.md`.

**Height normalization:** the tallest geometry in the export must be the
**parapet coping at exactly 10.20 m**, so the loader's
`targetHeightM / measuredHeight` scale is 1.0. Keep every rooftop unit below the
coping. The real plant reaches ~11.7 m; 2.15 explains why it does not set the
crest, and `REPORT.md` must repeat that reasoning.

## Reproducible Blender workflow

Blender 5.2 LTS. Headless: `blender -b --python script.py -- args`.

Keep `artifacts/27-south-park/build_27_south_park.py` (deterministic build script),
`artifacts/27-south-park/27-south-park.blend`, and
`artifacts/27-south-park/27-south-park.glb`. The script must rebuild the model reliably
enough for future revision. Do not modify or rename an unrelated existing GLB to satisfy
the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`27-south-park-top.png`, `27-south-park-north.png`, `27-south-park-east.png`,
`27-south-park-south.png`, `27-south-park-west.png`, plus
`27-south-park-contact-sheet.png`, at least one high three-quarter aerial beauty render
`27-south-park-aerial.png`, and a night render `27-south-park-aerial-night.png`.

The four elevations must share scale, framing, lighting, exposure and
projection; use orthographic or long-lens cameras; label directions from the
researched orientation; the top view must clearly show the full 12.19 × 33.5 m
roof — its parapet ring, mechanical cluster and skylights; the aerial view uses
the style bible's camera assumptions (30-50 degrees down, long lens). Simple
tabletop lighting, neutral warm background, minimal depth of field, and every
image must depict the same exported model.

Because the building is rotated ~45° from the world axes, the four compass renders will
each show two faces at 45°, and the axis-aligned XY bounding box will be roughly
**32.4 × 32.2 m** even though the building is 12.19 × 33.5 m. That is the expected
consequence of a 314.8° real-world heading, not a scale error. Add one extra
face-on render of the north-west elevation — it is the only public face and the
compass set never shows it square.

## Validate the exported GLB

Re-import `27-south-park.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture
count, camera count, light count, animation count, applied-transform status,
negative-scale status, normal-orientation status, unexpected geometry, and
per-material contract compliance. Render at least one review image from the
re-imported asset. Write `artifacts/27-south-park/validation.json` and
`artifacts/27-south-park/REPORT.md`.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "27-south-park",
  "file": "27-south-park.glb",
  "anchor": [
    -122.3931439,
    37.7817369
  ],
  "targetHeightM": 10.2,
  "cat": 3,
  "name": "27 South Park",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a separate, explicitly requested job — run `docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in `docs/asset-plans/27-south-park.md`.
````

---

## Part 2 — Research and design dossier

Compiled 16 August 2026 from the sources in 2.2. Values marked *inferred* are visual or
derived estimates, not published figures — the executing agent must re-verify
anything it relies on.

**A note on the evidence quality of this dossier.** The history is unusually
good: this parcel has its own paragraph in the South Park Historic District DPR
523D, which names the 1919 warehouse, both 1920s additions and both of their
architects, and states that the three sections were connected with fire doors.
The geometry is measured from three surveys that agree on the parcel. The one
public elevation and the roof were both directly observed. The weak points are
all about the *division* of a continuous row: which bays are 27's, where its
crest sits within a merged LiDAR footprint, and what the unobserved rear does.
All three are named in 2.15.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Built | **1919** (warehouse); **1920 addition** by Fred Koldenstadt; **1921 addition** by Caspar Zwierlein | SF Planning / Page & Turnbull, South Park Historic District DPR 523D, 30 June 2009; SF Assessor `year_property_built = 1919` |
| Original architect | **unknown** | DPR 523D: "The architect of the original portion is unknown" |
| Address range / parcel | 21–29 South Park Street = APN **3775-042** (Assessor `property_location` "0029 0021 SOUTH PARK"); the DPR contributor table lists it as 21–27 | DataSF parcels `acdm-wktn`; SF Assessor `wv5m-vpq2`; DPR 523D contributor table |
| Historic status | **Contributing resource**, potential South Park Historic District; property type **`HP8. Industrial`** | DPR 523D contributor table, row `3775042 / 21 / 27 / SOUTH PARK / HP8. Industrial` — **verified**. No Article 10 landmark designation found; the district is survey-identified, not adopted |
| Three sections | one 1919 warehouse in three parts, **"connected with fire doors"**; two party walls inserted 1993 | DPR 523D; SF permit 9313186 (1993, #21): "umb warehouse to have two party walls as per s.f. bldg. code" |
| Storeys | **2** | Assessor `number_of_stories = 2.0`; every permit 1990–2021 records 2 existing / 2 proposed |
| Structure | unreinforced load-bearing masonry with heavy timber roof trusses (Type III) | Assessor `construction_type = C`; permit 200301034562 revised to "type 3-n"; permit 9312874 (1993, #27): "repair to (e) wooden roof trusses" |
| Seismic retrofit | UMB compliance work 1990–2001 | permits 9012234 (1990, parapet bracing, $22k), 9011786 (1990, "parapet corrective"), 9313186 (1993, party walls, $73k), 200102157519 (2001, "umb upgrade — plywood diaphragm & collector beams", $200k) |
| Storefronts | **replaced 2003** — "improvements: toilet rms, exit corridors, stair, elevator, replace (e) storefronts & sidewalk", $500k, filed under all three addresses | permit 200301034562 |
| Elevator | installed 2003 (above); machine room worked on 2016 at #27 | permits 200301034562; 201602293743 ("new closet and soundproofing at (e) elevator machine room") |
| Current use | **office** throughout; formerly manufacturing (to 2003), retail (2000–05), warehouse (to 1993) | permits 201702076142, 201702138536 (2017, #27, office TI); Assessor roll still codes the parcel Industrial — see 2.15 |
| Building area (parcel) | 24,680 sq ft (2,293 m²) over two floors; lot 13,420 sq ft (1,247 m²) | SF Assessor `property_area`, `lot_area`; LoopNet listing for 21–29 S Park St (24,680 SF, 2 stories, class C, brick & timber, ~10 ft ceilings) |
| Footprint, 27 only (OSM) | **12.19 m × 33.5 m, 408.3 m²**, parallelogram on the 134.79°/314.79° line | OSM way/112759868, `addr:housenumber=27`, `addr:street=South Park`, reprojected — **measured** |
| Footprint, whole parcel (DataSF LiDAR) | 1,115.0 m² — 21 + 27 + 29 merged into ONE polygon `SF3775042` | DataSF `ynuv-fyni` — **measured**; equals 408.3 + 455.5 + 252.7 from the three OSM rings to within 0.2% |
| Roof deck | **9.60 m** median (mean 9.52, majority 9.82, **std 0.45 m** over 4,479 cells) | DataSF `ynuv-fyni` SF3775042 — **measured**; the tight std says one continuous flat roof across all three sections |
| Crest (this section) | **10.20 m** | Overture Maps building `db50f6d6-…`, source `OpenStreetMap:w112759868 + USGS Lidar`, `height = 10.2` — **measured**, per-ring; read as the parapet coping (2.15) |
| Parcel LiDAR maximum | 11.73 m | DataSF SF3775042 `hgt_maxcm` — **measured**; read as rooftop mechanical plant, see 2.9 and 2.15 |
| LiDAR minimum | 5.31 m | DataSF SF3775042 `hgt_mincm` — an edge artifact |
| Ground elevation | 11.96 m (NAVD88) | DataSF SF3775042 `gnd_min_m` — the app's terrain handles this, not the asset |
| Zoning | **SPD** (South Park District) | SF Assessor `zoning_code`; SF Planning Code §837 — the district exists to preserve "small-scale, continuous-frontage" buildings around the oval |
| Neighbourhood | Financial District/South Beach; planning district South of Market | DataSF parcels |
| Neighbour crests (Overture, USGS LiDAR) | 21 South Park **9.5 m**; 29 South Park **9.3 m**; 17–19 South Park **6.7 m**; 33–35 South Park 10.0 m (OSM tag); 318 Brannan 8 m; 326 Brannan 5.3 m; 334 Brannan 12 m | Overture `overture_buildings.geojsonseq`, 16 Aug 2026 vintage — **measured** |
| Tenants | South Park Commons (Ste 101), Core Innovation Capital and TI Platform / Transpose Platform (Ste 100) | SF Treasurer registered-business records via OpenGovUS; CA SoS filings via bizprofile.net; SEC Form D filings |

### 2.2 Sources

- https://www.openstreetmap.org/way/112759868 — the footprint, `addr:housenumber=27`, `addr:street=South Park`; no `height` tag
- `https://data.sfgov.org/resource/ynuv-fyni` (DataSF Building Footprints, LiDAR-derived) — footprint `SF3775042` covering the whole 21–29 parcel, heights 11.73 / 9.60 / 5.31 m, 4,479 cells at 50 cm
- `https://data.sfgov.org/resource/acdm-wktn` (DataSF Parcels) — parcel 3775-042, address range 21–29 SOUTH PARK
- `https://data.sfgov.org/resource/wv5m-vpq2` (SF Assessor secured roll) — year built 1919, 2 storeys, 24,680 sq ft over a 13,420 sq ft lot, zoning SPD, use Industrial
- `https://data.sfgov.org/resource/i98e-djp9` (SF Building Permits) — 53 permits on block 3775 lot 042: the 1990 parapet bracing, the 1993 party walls and roof-truss repair, the 2001 UMB diaphragm upgrade, the 2003 storefront/stair/elevator job, the 2005–2017 office fit-outs at #27, the 2018–2021 fit-outs at #21
- `pipeline/data/overture_buildings.geojsonseq` (Overture Maps, 16 Aug 2026 vintage as downloaded by `npm run download`) — per-ring USGS-LiDAR heights for this building and every neighbour
- SF Planning / Page & Turnbull, **South Park Historic District, DPR 523D continuation sheets, 30 June 2009** — `https://default.sfplanning.org/GIS/SouthSoMa/Docs/2009-06-30_South%20Park%20Dform.pdf`. Establishes: the 1919 build date and APN; contributor status and `HP8. Industrial`; the Koldenstadt 1920 and Zwierlein 1921 additions; "The three sections are connected with fire doors"; and the district-wide warehouse description (load-bearing masonry, minimal corbelled detailing, flat roofs, flat or stepped parapets, large steel-sash industrial windows, roll-up metal garage doors, never more than two storeys here)
- SF Planning Code **§837 SPD – South Park District** via `https://codelibrary.amlegal.com/codes/san_francisco/latest/sf_planning/0-0-0-67797` — the zoning district's purpose: preserve the small-scale continuous frontage around the oval
- https://socketsite.com/archives/2011/02/south_of_market_resource_survey_saysfive_new_historic_d.html — the 2011 SoMa survey that proposed the South Park Historic District among five new SoMa districts
- **Google Street View, Jan 2025**, panoramas on South Park Street north-west of the building (near `37.78192,-122.39338` and `37.78193,-122.39340`), headings 135°–150° — the north-west elevation, **observed**: painted brick, the six-arch second floor, the dark joinery shopfront band, the "27" numeral and the mahogany door
- **Google satellite (Vexcel/Airbus 2026, near-nadir), z21 tiles over `37.78174,-122.39314`** — the flat roof, its parapet ring, the mechanical cluster and the skylight monitors, at ~3 cm/px, **observed**
- https://www.loopnet.com/Listing/21-29-S-Park-St-San-Francisco-CA/20707079/ — 21–29 S Park St: 24,680 SF, 2 stories, class C, brick & timber, ~10 ft unfinished ceilings, "operable windows overlook South Park". *Observed (listing copy)*; its "year built 1950" contradicts both the Assessor and the DPR and is wrong
- https://perkinswill.com/project/south-park-venture-capital-firm/ and https://officesnapshots.com/2026/02/03/south-park-venture-capital-firm-offices-san-francisco/ — a 2023, 16,420 sq ft renovation of a 1920s brick-clad South Park building with "large, arched metal-clad windows". Client confidential, **no address published** — see 2.15
- https://opengovus.com/san-francisco-business/1344123-10-231 (South Park Commons Management LLC, 27 S Park St Ste 101) and https://www.bizprofile.net/principal-address/27-south-park-suite-100-san-francisco-ca-94107 — current tenancy

### 2.3 Orientation and placement

27 South Park sits on the **south-east rim of the South Park oval**, mid-row, with
South Park Street 24 m to its north-west and the park itself 29 m beyond that. It
is a narrow, deep lot: 12.19 m of frontage running back 33.5 m toward Brannan
Street, where a 2.5–6 m service gap separates it from 318, 326 and 334 Brannan.
Both long flanks are party walls — 21 South Park to the north-east, 29 South Park
to the south-west — and the three rings share vertices exactly (measured gap
0.00 m), which is what the 1993 party-wall permit describes.

Ring corners in Blender coordinates (metres, `+X` east, `+Y` north), centred on
the anchor `-122.3931439, 37.7817369`, from OSM way/112759868:

```
(  -7.57,  +16.09)   North corner   (South Park x the 21 party wall)
( +16.22,   -7.51)   East corner    (rear x the 21 party wall)
(  +7.57,  -16.09)   South corner   (rear x the 29 party wall)
( -16.21,   +7.51)   West corner    (South Park x the 29 party wall)
```

in ring order: `North → East → South → West`.

Edges, with outward normals:

| Edge | Length | Faces | Elevation |
|---|---|---|---|
| West corner → North corner | 12.18 m | NW 314.8° | **South Park front** — the only public face |
| North corner → East corner | 33.51 m | NE 45.2° | **party wall** with 21 South Park (blind) |
| East corner → South corner | 12.19 m | SE 134.8° | **rear**, onto the Brannan service gap |
| South corner → West corner | 33.50 m | SW 225.2° | **party wall** with 29 South Park (blind) |

The measured ring is a parallelogram to within 0.07 m of a true 33.59 × 12.19 m
rectangle; the departure is not worth modelling. Because of the ~45° heading the
axis-aligned bounding box is ~32.4 × 32.2 m. That is correct.

Three surveys agree on the parcel as a whole and none of them resolves 27 alone:
the DataSF LiDAR footprint `SF3775042` (1,115.0 m²) and the DataSF parcel both
cover 21–29 as one polygon, and only OSM splits the row into three rings whose
areas sum to the LiDAR polygon within 0.2%. **This plan therefore takes the OSM
ring** for both shape and anchor. That is a departure from the DataSF-centroid
convention used by 140 and 168 South Park, and 2.13 shows it is also the only
choice that produces a workable exclusion.

**The frontage is a chord, not a line.** South Park Street curves, and the row's
facade follows it — the Street View panoramas show a visible plane change at each
party wall. Over a 12.19 m chord the sagitta is well under 0.2 m. Build it
straight; the neighbours' angles are not this asset's problem.

### 2.4 What each side shows

One of these four is **observed**. The others are marked.

**North-west (South Park) — observed, Google Street View, Jan 2025.** The 12.19 m
address elevation and the only public face. The wall is **painted brick** in a
warm off-white — light enough to read as white in sun, warm enough to go greige
in shade — laid flush, with no corbelling, no cornice brackets and no string
courses. Two storeys:

- **Ground floor**, very tall — close to half the facade height. Three bays of
  dark blue-green joinery set in deep painted reveals. Each bay is composed the
  same way from the top down: a **row of small square transom lights**, then a
  **beaded/reeded panel band with a single rosette medallion at its centre**,
  then the main opening. The openings differ: a pair of tall flush **double
  doors** (freight-scale, no glazing) at one end; a wide **divided-light
  shopfront window** in the middle; and at the other end, beside the painted
  numeral **"27"**, a **mahogany double door with a glazed upper half**, set in
  a dark blue-green surround. A wall-mounted lamp and a small camera flank the
  27 door. A low painted base runs under the joinery.
- **Second floor**: **six segmental-arched windows**, dark blue-green metal
  frames, roughly 2.9 m tall, each a large lower light with a horizontal transom
  bar and an arched top light. They sit close together on narrow painted-brick
  piers, springing from a continuous impost line, and they nearly fill the wall
  between the ground-floor cornice band and the parapet. This is an arcade, and
  it is the building.
- **Parapet**: plain, flat-topped, with a thin projecting band at the coping and
  no ornament. It stands roughly 0.6 m above the roof deck.

**North-east (21 South Park party wall) — inferred.** Blind painted brick,
carried full height with the parapet run across. 21's roof deck is 0.7 m below
this one (Overture 9.5 m vs 10.2 m), so a shallow step is expected at the joint.

**South-west (29 South Park party wall) — inferred.** The same, against a 9.3 m
neighbour.

**South-east (rear) — not observed.** 12.19 m onto a service gap 2.5–6 m wide
behind the Brannan Street buildings. Nothing photographs it. For a warehouse of
this type the expected treatment is plain painted brick with a small number of
square openings and possibly a loading door; the district survey notes roll-up
metal garage doors "on the primary or secondary façades" generally. Marked
*inferred* and deliberately kept plain — see 2.15.

**Top — observed, Google nadir aerial 2026, ~3 cm/px.** A flat, light warm-grey
membrane roof running the full 12.19 × 33.5 m inside a continuous white parapet
ring that is shared with both neighbours. The plant is concentrated in the
**middle third, toward the front half**: five or six white rectangular units, two
or three low round fans or condensers, and flexible ducting snaking between them.
Two **low glazed monitors with a visible pane grid** sit among them — skylights,
not penthouses. The rear third of the roof is essentially empty membrane. There
is **no penthouse, no stair bulkhead and no roof deck** inside this ring.

### 2.5 Recognition cues (ranked)

1. **The six-arch arcade** — segmental-arched second-floor windows in dark metal,
   close-spaced, filling the wall. Nothing else on this stretch of the oval has
   an arcade, and it survives simplification better than any other feature here.
2. **The tall dark ground floor** — three deep bays of joinery, each transom
   band over panel band over opening, nearly as tall as the storey above. The
   glass-to-wall ratio at street level is extreme for 1919.
3. **The white-painted brick** — this row is painted, and the district's other
   warehouses are not. From the aerial camera the pale wall is what separates it
   from its red-brick and grey-concrete neighbours.
4. **The one mahogany door** — a single warm timber accent in an otherwise dark
   blue-green run, at the address numeral.
5. **The proportion** — 12 m wide, 33 m deep, two storeys, level with its
   neighbours: a stick, not a block.

### 2.6 Miniature translation

**Preserve**

- The 12.19 × 33.5 m parallelogram and the real 134.8°/314.8° heading, exactly
- Two storeys, flat-topped, level with the row — never taller than 21 or 29 by
  more than the measured 0.7 m
- The six-arch rhythm on the front, at its measured spacing
- The three-bay ground floor with its transom / panel-band / opening stack
- The mahogany door as the one warm accent
- Both party walls as finished blind faces with the parapet carried across

**Simplify / exaggerate**

- Each arched window becomes **one recessed arched panel with a single frame
  band and one transom bar** — no muntin grid. At the app's camera the
  subdivision is noise; the *arch* is the cue and may be pushed slightly taller
  and slightly wider than reality so it survives.
- The beaded panel band becomes **one flat recessed strip per bay** with the
  rosette omitted or reduced to a single small disc — it is under a pixel at the
  app camera and costs triangles that the arcade needs.
- The transom lights become **one continuous glazed strip** per bay, not
  individual panes.
- The divided-light shopfront becomes one glazed panel behind its frame.
- The wall-mounted lamp, the camera, the downpipe and the overhead wires are
  omitted.
- Roof clutter becomes a composed set: one tight group of four boxes, two round
  fans, two low skylight monitors, and nothing else.
- Painted brick becomes flat colour; the masonry reads through the reveal depths
  and the pier widths, not through texture.

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not
a straitjacket — adjust after the first aerial review render.

1. Body: extrude the 2.3 parallelogram from z=0 to the roof deck z=9.60,
   `Toy_sand`.
2. Base band, z=0 to z=0.35: `Toy_stone`, carried around all four faces.
3. **Ground floor, z=0.35 to z=4.55** — on the north-west face only, three bays
   on **4.06 m centres**, each a recess 0.20 m deep and 3.30 m wide:
   - opening z=0.35 to z=3.30, `Toy_glass` behind a 0.14 m `Toy_navy` frame;
     bay 1 (north-east end) is a pair of flush doors, `Toy_navy`, no glazing;
     bay 2 (centre) is the shopfront window; bay 3 (south-west end) is the
     **mahogany door**, `Toy_rust`, with a glazed upper half in `Toy_glass`
   - panel band z=3.30 to z=3.70, `Toy_navy`, recessed a further 0.06 m
   - transom strip z=3.70 to z=4.35, `Toy_glass` in a `Toy_navy` frame
   Every other face is plain wall here.
4. Ground-floor cornice band: 0.30 m `Toy_stone` course at z=4.55, north-west
   face only, projecting 0.10 m.
5. **Second floor, z=4.85 to z=9.10** — on the north-west face, six arched
   openings on **2.03 m centres**, each 1.55 m wide: a rectangular light from
   z=5.20 to z=7.35, a transom bar at z=7.35, and a **segmental arch head** from
   z=7.50 to z=8.05 (8-segment arc, rise ~0.55 m). Recess 0.16 m; `Toy_glass`
   behind a 0.12 m `Toy_navy` frame that follows the arch. The 0.48 m of wall
   between openings is the pier and stays `Toy_sand`.
6. Parapet: `Toy_sand` from z=9.60 to z=10.05, capped by a 0.15 m `Toy_stone`
   coping to **z=10.20**, carried around all four faces including both party
   walls. **This is the crest and must land at exactly 10.20 m.**
7. **Roof, z=9.60 to z=9.72** — a thin flat slab, `Toy_steel`, sitting inside the
   parapet ring.
8. Mechanical: four boxes (`Toy_trim`, ~1.5 × 1.0 × 0.40 m, `Toy_roofd` caps) and
   two low cylinders (10-segment, 0.85 m diameter, 0.35 m tall, `Toy_steel`),
   grouped in the middle third toward the front half so the rear third stays
   clean. Nothing exceeds z=10.15.
9. Skylights: two 2.0 × 1.2 × 0.30 m monitors, `Toy_glass` on a `Toy_steel` kerb,
   set among the plant.
10. Rear (south-east) face: two small square openings, 1.1 m, `Toy_glass` in a
    0.10 m `Toy_navy` frame, at z=5.6; otherwise plain.
11. Party walls: plain `Toy_sand`, no openings, parapet carried across.
12. Bevel 0.12 m, 2 segments.

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_sand` | `ece4d4` | painted brick — body walls, piers, parapet, party walls |
| `Toy_stone` | `d9d2c2` | base band, ground-floor cornice band, parapet coping |
| `Toy_navy` | `2c4a70` | all joinery — shopfront frames, panel bands, arched window frames, the flush double doors |
| `Toy_glass` | `2a4d73` | glazing at both floors, skylights |
| `Toy_rust` | `a86444` | the mahogany door at number 27 |
| `Toy_steel` | `9aa0a6` | roof membrane, skylight kerbs, round fans |
| `Toy_trim` | `f3efe6` | rooftop mechanical boxes |
| `Toy_roofd` | `45454a` | mechanical box caps |
| `Toy_glass_Glow` | `6f95b8` | lit second-floor windows at night |
| `Toy_trim_Glow` | `f3efe6` | ground-floor lobby spill on the South Park front |

The observed joinery is a dark blue-green that has no exact palette entry;
`Toy_navy` is the closest on-palette value and is what this plan specifies. If it
reads too blue against `Toy_sand` at the app camera, `Toy_ink 3a3530` is the
sanctioned fallback — say which you used in `REPORT.md`. Do **not** reach for
`Toy_teal 3fa8a0`: it is a mid-tone accent and would turn the building into a
seaside kiosk.

`Toy_sand` rather than `Toy_cream` or `Toy_white` for the wall: the paint is warm
and slightly grey in every capture, and the `Toy_stone` bands need a value to sit
below.

**Night state (required).** Glow surfaces must be **thin single-sided plates
proud of the opaque glazing**, never closed shells — the app renders `_Glow` in a
separate layer that reads through by day, and a closed shell doubles that
contribution. Hero glow: the ground-floor bays on the South Park front, warm
`Toy_trim_Glow`, lit across bays 2 and 3 — an office lobby is the one thing on
this facade that is genuinely bright after dark, and the tall shopfront band is
where it belongs. Supporting accent: **two or three** of the six arched windows
lit in `Toy_glass_Glow`, scattered rather than in a row. The party walls, the
rear and the roof stay dark.

### 2.9 Top surface

12.19 × 33.5 m of flat roof at 9.60 m, mid-row on the oval's south-east rim, with
the camera looking down on it constantly and the taller Brannan Street block
(334 Brannan, 12 m) looking over its rear parapet. The composition problem is a
long thin rectangle with all its events in one place: the nadir aerial shows the
plant packed into the middle third toward the front, and the rear third bare.
Keep that. It is the honest reading and it is also the better composition — a
long clean run of membrane behind a busy cluster, with the continuous parapet
ring drawing the outline.

Give the membrane a clear value below the painted brick so the parapet reads as a
rim from above; let the parapet's inner face and its shadow give the roof depth.
Do not model membrane seams. Do not add a stair bulkhead or a roof deck — this
building has neither.

### 2.10 Scope

**In the GLB:** the single centre section — body, the north-west elevation with
its arcade and shopfront band, both blind party walls, the plain rear elevation,
the parapet and coping, the flat roof, the mechanical cluster and the two
skylight monitors

**Not in the GLB:** South Park, its lawn or trees, South Park Street, the
sidewalk, the street trees and their guards, the overhead wires and poles, the
wall-mounted lamp and camera, the downpipe, parked cars, people, the neighbours
at 21, 29, 17–19 or 33–35 South Park, plinths, cameras or lights

**Deliberately excluded: the rooftop mechanical plant above the parapet line.**
The real units reach ~11.7 m (2.1). Modelling them at true height would make an
air handler the bounding-box top, so `targetHeightM` would describe a condenser
rather than a building and the loader would rescale the whole model against it —
the same argument that removed 2 South Park's flagpole. The plant is modelled,
grouped and legible, but sized to sit under the 10.20 m coping. Record the
departure in `REPORT.md`.

### 2.11 Triangle budget

Cap 7,000 — a secondary building with one public elevation, and the cap should
bind. Suggested split: body, parapet, coping and base ~0.9k; the six arched
openings with their arc heads ~2.4k (the arcs are the expensive part: 8 segments
each, frame and reveal); the three ground-floor bays with their transom strips
and panel bands ~1.6k; the two cornice/base bands ~0.4k; roof slab ~0.2k;
mechanical cluster and fans ~0.9k; skylights ~0.3k; rear openings and party walls
~0.3k.

Two places this budget can run away. **The arches**: six of them, each with a
frame band that follows the curve and a recess behind it, is the single largest
line item — hold the arc to 8 segments and resist a muntin grid inside the head.
**The panel bands**: one flat recessed strip per bay, not a run of beads; the
reeding and the rosette are sub-pixel at the app camera and would triple the
ground floor's cost.

### 2.12 Draft manifest entry

```json
{
  "id": "27-south-park",
  "file": "27-south-park.glb",
  "anchor": [
    -122.3931439,
    37.7817369
  ],
  "targetHeightM": 10.2,
  "cat": 3,
  "name": "27 South Park",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

`dims` and `tris` are placeholders until the asset is built and validated.
`loadRadius`: the default formula gives `max(2500, 10.2 * 30) = 2500` m. Take the
default.

### 2.13 Integration notes (for later, not this task)

**New landmark.** Add a `pipeline/lib/landmarks.mjs` entry and re-bake the
affected tiles, or the baked procedural mass on this lot will swallow the GLB
whole:

```js
{
  id: '27SouthPark',
  name: '27 South Park',
  lon: -122.3931439,
  lat: 37.7817369,
  height: 10.2,
  exclude: 15,
  camera: { distance: 170, yaw: 225, pitch: 26 },
}
```

**The exclusion is unusual and the reasoning must not be lost.** `excluded()` in
`pipeline/buildings.mjs` drops a footprint when its area centroid OR any ring
vertex falls inside the circle, and the bake reads DataSF first, then gap-fills
from Overture wherever `occupiedFraction(bbox) <= 0.25`. Measured from this
anchor against the two files the bake actually reads
(`pipeline/data/buildings_datasf.geojson` and `overture_buildings.geojsonseq`,
16 Aug 2026 vintage), and confirmed by replaying the DataSF→Overture handoff at
several radii:

| polygon | trigger distance | via |
|---|---|---|
| Overture w112759868 (this building) | **0.00 m** | own centroid |
| **DataSF SF3775042 (21 + 27 + 29 merged)** | **3.45 m** | its centroid — **the lower bound** |
| Overture w112759865 (29 South Park) | 9.86 m | its centroid |
| Overture w112759863 (21 South Park) | 12.60 m | its centroid |
| Overture w112759869 (318 Brannan) | 19.13 m | nearest vertex |
| **DataSF SF3775102 (33–35 South Park)** | **20.07 m** | nearest vertex — **the upper bound** |
| DataSF SF3775100 (318 Brannan) | 20.78 m | nearest vertex |
| DataSF SF3775046 (17–19 South Park) | 22.63 m | nearest vertex |

So the safe window is **(3.45, 20.07) m**, and a replay confirms exactly one
footprint drops anywhere inside it. **15 m** is chosen rather than something
nearer the floor for one specific reason: dropping `SF3775042` means
`addBuilding()` returns null, so `markOccupied()` never runs for it, and the
Overture gap-fill becomes free to re-add 21, 27 and 29 as three separate
procedural blocks straight through the asset. Today `occupiedFraction` still
reads 0.86–0.93 for all three from the *neighbours'* bounding boxes and blocks
them, but that is a side effect of other buildings' geometry, not a guarantee.
At 15 m all three Overture rings are excluded outright and the outcome no longer
depends on it. This is the failure mode documented at `106SouthPark`; here the
guard is cheap because the DataSF polygon that would otherwise protect the
neighbours is already gone.

**The collateral is real and unavoidable — say so at integration.** DataSF traces
21, 27 and 29 as ONE 1,115 m² polygon, so removing this building's procedural
mass necessarily removes 21's (455 m²) and 29's (253 m²) as well. No radius
avoids it: the merged polygon has a single centroid 3.45 m from this anchor, and
below that distance nothing is excluded at all and the 10.67 m procedural block
(`datasfHeight` = (9.60 + 11.73)/2) buries the 10.20 m asset entirely. The
choice is between a hole and an invisible landmark.

Consequences to plan for:

- `pipeline/pipeline/lib/landmarks.mjs` aside: **21 South Park is a sibling in the
  same batch** (branch `pipeline/21-south-park`). If it lands, its GLB fills 455 m²
  of the hole and only 29 South Park (253 m², a 7.7 m-wide slot) is left bare.
- **29 South Park has no GLB and no branch.** Until it gets one, the bake leaves
  a 7.7 × 33.5 m gap on this building's south-west flank. That is why 2.10
  requires both party walls to be finished faces — they are exposed.
- Both siblings' exclusions will target the same merged polygon. That is
  idempotent; two zones dropping the same footprint is not a conflict.
- **Verify with `pipeline/audit.mjs` check 1.6 after the re-bake** and confirm
  visually that 33–35 South Park and 17–19 South Park are both still standing
  before committing.

**Anchor.** The OSM ring centroid, not a DataSF centroid, because DataSF has no
polygon for 27 alone — its only polygon here is the merged parcel, whose centroid
sits 3.45 m away inside 21. Anchoring on the merged centroid would put the model
a third of a building off its own lot for no benefit (AGENTS rule 5).

**Camera.** `app/src/camera.js` places the eye at `target + distance * (sin yaw,
., cos yaw)` with `+x` east and `+z` south, so camera bearing = `180 - yaw`. The
only public elevation faces north-west (314.8°), so `yaw: 225` stands the camera
over the park looking south-east, square onto the arcade. No `key`: at 10 m this
is texture in the row, not a destination.

**Batch mode.** This session runs under `BATCH: yes`, so stage 5 still runs the
re-bake and the full QA on it, then throws the bake away
(`git checkout -- app/public/tiles api/_data`) and commits source only. See
"Batch mode" in `docs/asset-pipeline/ADDRESS-TO-ASSET.md`.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Bounding-box top exactly **10.20 m** — the parapet coping, not a mechanical unit (loader scale lands at 1.0)
- [ ] Dimensions plausible in meters and consistent with 2.1 (XY bbox ~32.4 × 32.2 m is expected)
- [ ] The footprint is still 12.19 × 33.5 m in plan on the 314.8° line — measure it, do not eyeball it
- [ ] The roof deck sits at 9.60 m; no rooftop unit exceeds 10.15 m
- [ ] Six arched openings on the north-west face; none on any other face
- [ ] Both party walls blind, finished, parapet carried across
- [ ] Triangles at or under 7,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the lit second-floor windows and the ground-floor bays; glow plates single-sided and proud of the opaque glazing, never closed shells
- [ ] No penthouse, no stair bulkhead, no roof deck in the export
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (per-object signed volume for the union of solids; ray test residual <= 0.15%)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + the extra face-on north-west elevation + contact sheet + night render regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed
- [ ] The 2.15 crest question answered in `REPORT.md`, with the evidence that answered it
- [ ] The bay assignment (2.15) either resolved from imagery or stated plainly as unresolved
- [ ] The rear elevation stated plainly as inferred

### 2.15 Open questions and risks

- **Which bays belong to 27?** The frontage is 12.19 m by measurement and the
  numeral "27" is on the wall beside the mahogany door, but 21, 27 and 29 are one
  continuous painted wall and the party-wall joints do not read reliably in the
  Jan 2025 capture. The six-arch / three-bay rhythm in 2.7 is *derived from the
  measured width* — 12.19 / 6 = 2.03 m for the arches and 12.19 / 3 = 4.06 m for
  the ground floor — and it matches what the photograph shows around the numeral,
  but it is not counted off a photograph of a confirmed 27-only extent. If better
  imagery contradicts the count, the count loses; the width does not.
- **How much of the 11.73 m LiDAR maximum is architecture?** None, on the
  evidence. The DataSF maximum is taken over the whole 21–29 parcel, whose height
  standard deviation is 0.45 m over 4,479 cells — an exceptionally flat single
  roof. The nadir aerial shows no penthouse, no bulkhead and no roof deck inside
  this ring, only a mechanical cluster with two low glazed monitors, and no permit
  in 53 records adds a rooftop structure. So the plan reads 9.60 m as the deck,
  10.20 m (Overture's per-ring USGS-LiDAR value for way/112759868) as the parapet
  coping, and 11.73 m as an air handler somewhere on the parcel. **The risk is
  contained:** the model is authored with the coping at exactly 10.20 m, so the
  loader's scale is 1.0 and an error here makes the parapet wrong, not the
  building.
- **The 0.60 m parapet is derived, not measured.** It is the difference between
  Overture's per-ring 10.20 m and DataSF's whole-parcel 9.60 m median. The 1990
  permits ("parapet bracing", "parapet corrective") confirm there is one; nothing
  states its height. A 0.6 m parapet is at the low end of normal for the type.
- **The rear elevation was never observed.** No Street View, no aerial oblique.
  The plan models it plain because that is what the type does on a service gap,
  but a roll-up loading door would be entirely unsurprising — the district survey
  names them as a warehouse feature "on the primary or secondary façades". This is
  the most likely correction to this dossier.
- **The Perkins&Will attribution is unresolved.** A 2023, 16,420 sq ft renovation
  of a 1920s brick-clad South Park building with "large, arched metal-clad
  windows" fits this warehouse and nothing else near the oval, but the client is
  published as confidential, no address is given, and the ~$2.4 M of 2020–2021
  permits on this parcel are filed under **21** South Park, not 27. The safe
  reading — and the one this plan uses — is that it confirms the arched metal
  windows are a real, current feature of this row. Do not write "27 South Park by
  Perkins&Will" anywhere.
- **The storefronts are not original.** Permit 200301034562 (2003) replaced them
  across all three addresses. The joinery observed in 2025 is therefore a
  ~2003–2005 sympathetic replacement, not 1919 fabric. That does not change the
  model — it is what the building looks like — but it should stop anyone
  researching 1919 shopfront precedent.
- **LoopNet says the building was built in 1950.** It is wrong. The Assessor roll
  and the DPR 523D both say 1919, and the DPR names the 1920 and 1921 additions
  and their architects. Do not re-inherit the 1950 figure.
- **The Assessor still codes this parcel `I` / Industrial with `use_definition`
  "Industrial".** It is a stale roll code for a 1919 warehouse whose permits have
  recorded office use since 2005. The manifest entry uses `cat: 3` (office) on
  that basis, not `cat: 20` (warehouse).
- **The exclusion leaves a hole that this asset cannot fill.** See 2.13. It is
  the one genuinely unsatisfying thing about integrating this building alone, and
  it is a property of the bake's input data, not of any choice made here.
