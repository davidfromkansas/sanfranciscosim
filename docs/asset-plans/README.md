# Landmark asset plans

One plan per San Francisco landmark queued for the bespoke-GLB pipeline. Each file
contains **both** halves of the job:

1. **Part 1 — a ready-to-run task prompt.** Copy it into a fresh agent session and
   it will produce a validated GLB, renders, a reference dossier and a report under
   `artifacts/<slug>/`, exactly the way `artifacts/salesforce-tower/` was produced.
2. **Part 2 — the research and design dossier.** Sources, verified facts, the
   WGS84 anchor and architectural height, orientation, four-side and roof
   observations, recognition cues, a massing recipe, a palette map, the triangle
   budget, a draft manifest entry, integration notes and the open risks.

These are plans only. Nothing here has been modelled yet, and no app code,
manifest or pipeline data has been changed.

[**INTEGRATION-PROMPT.md**](./INTEGRATION-PROMPT.md) is the other end of the
pipeline: a reusable, runnable prompt that takes a finished GLB from
`artifacts/<slug>/` into the live scene (re-validation, manifest entry, registry +
re-bake for new landmarks, fallback drill, deployed QA), plus reference notes on how
the loader places assets and what to do when one misbehaves.

Parks are planned separately in [**`../plans/parks/`**](../plans/parks/README.md),
because a park is not a single GLB — it is landcover, terrain drape, tree
placement and paths from the pipeline, with a few hero assets inside it. Those
plans reference the landmark plans here (de Young, Cal Academy, Conservatory,
Painted Ladies, Mission Dolores Basilica, Palace of Fine Arts) rather than
duplicating them.

[**civic-center-plaza.md**](./civic-center-plaza.md) is the exception to that rule:
a designed hardscape with a fixed surveyed layout and no natural component, planned
as a single landmark GLB on the same argument that made the Palace of Fine Arts
grounds a landmark. See its §2.15 risk 5.

[**flora-kit.md**](./flora-kit.md) is the one plan here that is not a landmark:
an authored Blender kit of tree species and landscape props to replace the single
procedural lollipop that all 289,741 of the city's baked trees currently share.
It follows the street-furniture kit's architecture rather than the landmark
route, and the park plans depend on it (§E8 of the parks README).

## The set

| Landmark | Manifest id | Target height | Runtime status |
|---|---|---|---|
| [Transamerica Pyramid](./transamerica-pyramid.md) | `transamerica` | 260 m | replaces procedural |
| [Ferry Building](./ferry-building.md) | `ferry-building` | 74.7 m | replaces procedural |
| [Coit Tower](./coit-tower.md) | `coit-tower` | 64 m | replaces procedural |
| [Palace of Fine Arts](./palace-of-fine-arts.md) | `palace-of-fine-arts` | 49.4 m | replaces procedural |
| [San Francisco City Hall](./city-hall.md) | `city-hall` | 93.73 m | replaces procedural |
| [Painted Ladies](./painted-ladies.md) | `painted-ladies` | 12.5 m | replaces procedural |
| [Sutro Tower](./sutro-tower.md) | `sutro-tower` | 297.8 m | replaces procedural |
| [Oracle Park](./oracle-park.md) | `oracle-park` | 45 m | replaces procedural |
| [Grace Cathedral](./grace-cathedral.md) | `grace-cathedral` | 53 m | replaces procedural |
| [Mission Dolores Basilica](./mission-dolores.md) | `mission-dolores` | 30 m | new landmark |
| [Columbus Tower (Sentinel Building)](./columbus-tower.md) | `columbus-tower` | 29 m | new landmark |
| [555 California Street](./555-california.md) | `555-california` | 237 m | new landmark |
| [One Rincon Hill](./one-rincon-hill.md) | `one-rincon-hill` | 195 m | new landmark |
| [Cathedral of Saint Mary of the Assumption](./st-marys-cathedral.md) | `st-marys-cathedral` | 58 m | new landmark |
| [California Academy of Sciences](./cal-academy.md) | `cal-academy` | 11 m | new landmark |
| [de Young Museum](./de-young.md) | `de-young` | 44 m | new landmark |
| [Conservatory of Flowers](./conservatory-of-flowers.md) | `conservatory-of-flowers` | 18.3 m | new landmark |
| [War Memorial Opera House](./war-memorial-opera-house.md) | `opera-house` | 44 m | new landmark |
| [Herbst Theatre (War Memorial Veterans Building)](./herbst-theatre.md) | `herbst-theatre` | ~31 m (estimated) | new landmark |
| [Fairmont San Francisco](./fairmont-san-francisco.md) | `fairmont` | 99 m | new landmark |
| [334 Brannan Street (Sherman and Clay Building)](./334-brannan.md) | `334-brannan` | 13.4 m (estimated) | new landmark |
| [350 Brannan Street](./350-brannan.md) | `350-brannan` | 13.85 m | new landmark |
| [362 Brannan Street](./362-brannan.md) | `362-brannan` | 8.6 m | new landmark |
| [370 Brannan Street](./370-brannan.md) | `370-brannan` | 7.63 m | new landmark |
| [358 Brannan Street](./358-brannan.md) | `358-brannan` | 9.6 m (estimated) | new landmark |
| [380 Brannan Street](./380-brannan.md) | `380-brannan` | 12.6 m | new landmark |
| [318 Brannan Street](./318-brannan.md) | `318-brannan` | 8.6 m (estimated) | new landmark |
| [550 Third Street](./550-third.md) | `550-third` | 11 m | new landmark |
| [551 Third Street (Shell Service Station)](./551-third.md) | `551-third` | 6.6 m | new landmark |
| [375 Alabama Street (Ames Harris Neville Co.)](./375-alabama.md) | `375-alabama` | 22.5 m | new landmark |
| [1008 General Kennedy Avenue](./1008-general-kennedy.md) | `1008-general-kennedy` | 11.9 m | new landmark |
| [Letterman Digital Arts Center](./letterman-digital-arts-center.md) | `letterman` | ~22 m (estimated) | new landmark |
| [Chase Center](./chase-center.md) | `chase-center` | 40.8 m | new landmark |
| [540 Presidio Boulevard](./540-presidio-blvd.md) | `540-presidio-blvd` | 11.5 m (estimated) | new landmark |
| [541 Presidio Boulevard](./541-presidio.md) | `541-presidio` | 10.0 m (LiDAR-derived) | new landmark |
| [542 Presidio Boulevard](./542-presidio-blvd.md) | `542-presidio-blvd` | 10.6 m (estimated) | new landmark |
| [543 Presidio Blvd](./543-presidio-blvd.md) | `543-presidio-blvd` | 9.55 m | new landmark |
| [San Francisco Civic Center Courthouse](./civic-center-courthouse.md) | `civic-center-courthouse` | 29.6 m | new landmark |
| [Bill Graham Civic Auditorium](./bill-graham-civic-auditorium.md) | `bill-graham-civic-auditorium` | 37 m | new landmark |
| [505 Van Ness Avenue (Edmund G. "Pat" Brown Building)](./505-van-ness.md) | `505-van-ness` | 27 m (estimated) | new landmark |
| [500 Van Ness Avenue (The Corinthian)](./500-van-ness.md) | `500-van-ness` | 17 m (estimated) | new landmark |
| [Louise M. Davies Symphony Hall](./davies-symphony-hall.md) | `davies-symphony-hall` | 35 m | new landmark |
| [101 Grove Street (Public Health Building)](./101-grove.md) | `101-grove` | 21.4 m | new landmark |
| [Asian Art Museum (Old Main Library)](./asian-art-museum.md) | `asian-art-museum` | 28.1 m | new landmark |
| [171 South Park Street](./171-south-park.md) | `171-south-park` | 12.6 m | new landmark |
| [101 South Park](./101-south-park.md) | `101-south-park` | 10.9 m (estimated) | new landmark |
| [155 – 157 South Park Street](./155-south-park.md) | `155-south-park` | 10.1 m | new landmark |
| [135 South Park](./135-south-park.md) | `135-south-park` | 8.5 m (LiDAR-derived) | new landmark |
| [165–167 South Park](./165-south-park.md) | `165-south-park` | 9.0 m (estimated) | new landmark |
| [181 South Park](./181-south-park.md) | `181-south-park` | 16.5 m (LiDAR-derived) | new landmark |
| [San Francisco Main Public Library](./sf-main-library.md) | `sf-main-library` | 28.98 m | new landmark |
| [234 Van Ness Avenue (The Kelsey Civic Center)](./234-van-ness.md) | `234-van-ness` | 30.12 m | new landmark |
| [500 Third Street](./500-third.md) | `500-third` | 26.5 m | new landmark |
| [599 Third Street](./599-third.md) | `599-third` | 18.3 m | new landmark |
| [Civic Center Plaza](./civic-center-plaza.md) | `civic-center-plaza` | 30.48 m (flagpole crest) | new landmark |
| [250 Van Ness Avenue (171–195 Grove Street)](./250-van-ness.md) | `250-van-ness` | 10.0 m (estimated) | new landmark |
| [Earl Warren Building](./earl-warren-building.md) | `earl-warren-building` | 27.0 m | new landmark |
| [560 Third Street](./560-third.md) | `560-third` | 7.2 m (LiDAR-derived) | new landmark |
| [574 Third Street (566–586 Third)](./574-third.md) | `574-third` | 15.4 m | new landmark |
| [590 Third Street](./590-third.md) | `590-third` | 9.5 m (estimated) | new landmark |
| [592 Third Street](./592-third.md) | `592-third` | 8.2 m (estimated) | new landmark |
| [521 Third Street (521–527 Third / Taber Place)](./521-third.md) | `521-third` | 11.4 m (estimated) | new landmark |
| [400 Brannan Street](./400-brannan.md) | `400-brannan` | 8.8 m | new landmark |
| [424 Brannan Street (Tower Valet Parking lot)](./424-brannan.md) | `424-brannan` | vertical extent, ~8.6 m (draped ground asset) | new landmark |
| [300 Brannan Street (Blinn Estate Building)](./300-brannan.md) | `300-brannan` | 25.2 m (penthouse crest; 21.34 m parapet) | new landmark |
| [188 South Park (South Park Lofts)](./188-south-park.md) | `188-south-park` | 15.93 m (LiDAR-derived) | new landmark |
| [150 South Park](./150-south-park.md) | `150-south-park` | 8.0 m | new landmark |
| [160 South Park](./160-south-park.md) | `160-south-park` | 9.4 m (LiDAR-derived) | new landmark |
| [132 South Park (130–134 South Park)](./132-south-park.md) | `132-south-park` | 12.07 m (LiDAR-derived) | new landmark |
| [104–106 South Park (Gran Oriente Filipino Hotel)](./106-south-park.md) | `106-south-park` | 11.58 m | new landmark |
| [108–110 South Park (South Park Cafe)](./108-south-park.md) | `108-south-park` | 8.45 m (estimated) | new landmark |
| [156 South Park Street (Anchor Packing Co.)](./156-south-park.md) | `156-south-park` | 8.7 m (LiDAR-derived) | new landmark |
| [166–168 South Park](./168-south-park.md) | `168-south-park` | 10.44 m (LiDAR-derived) | new landmark |
| [164 South Park (Saitowitz facade; Twitter/Instagram birthplace)](./164-south-park.md) | `164-south-park` | 5.4 m (LiDAR median — the maximum is rejected, see its §2.15) | new landmark |
| [140 South Park](./140-south-park.md) | `140-south-park` | 10.68 m (LiDAR-derived) | new landmark |
| [126 South Park](./126-south-park.md) | `126-south-park` | 7.6 m (LiDAR-derived) | new landmark |
| [102 South Park (The Park View)](./102-south-park.md) | `102-south-park` | 14.0 m (estimated) | new landmark |
| [86–96 South Park (Levy Design Partners, 1996)](./96-south-park.md) | `96-south-park` | 13.7 m (LiDAR-derived maximum) | not shipped — superseded by `92-south-park` |
| [2 South Park (544 Second Street, Kohler warehouse)](./2-south-park.md) | `2-south-park` | 17.72 m (LiDAR-derived) | new landmark |
| [27 South Park (centre of the 21–29 warehouse)](./27-south-park.md) | `27-south-park` | 10.2 m (LiDAR-derived) | not shipped — superseded by `21-south-park` |
| [South Park (64 South Park)](./64-south-park.md) | `64-south-park` | 21.04 m (vertical extent — the asset is terrain-draped; the 15.0 m elm crest is estimated) | new landmark |
| [35 South Park (Accel)](./35-south-park.md) | `35-south-park` | 13.4 m (penthouse crest, photogrammetric/estimated; parapet 10.4 m) | new landmark |
| [524 Second Street (522–524)](./524-second.md) | `524-second` | 9.9 m (estimated) | new landmark |
| [501 Second Street](./501-second.md) | `501-second` | 37.7 m | new landmark |
| [21–29 South Park](./21-south-park.md) | `21-south-park` | 11.73 m (LiDAR maximum, read as the roof bulkhead; the 10.20 m cornice crest is estimated) | new landmark |
| [Hotel Madrid (22–24 South Park)](./22-south-park.md) | `22-south-park` | 14.22 m (LiDAR-derived) | new landmark |
| [26–28 South Park (51 Taber Place)](./26-south-park.md) | `26-south-park` | 9.05 m (LiDAR-derived) | new landmark |
| [41–43 South Park](./41-south-park.md) | `41-south-park` | 10.6 m (estimated, photogrammetric) | new landmark |
| [44–46 South Park](./46-south-park.md) | `46-south-park` | 16.15 m (LiDAR-derived) | new landmark |
| [54–58 South Park](./58-south-park.md) | `58-south-park` | 16.9 m (estimated — LiDAR max; parapet 13.6 m) | new landmark |
| [76–82 South Park](./76-south-park.md) | `76-south-park` | 16.28 m (LiDAR max, attributed to the roof-stair penthouse — see its 2.15 risk 1; roof deck 13.08 m measured) | new landmark |
| [84 South Park](./84-south-park.md) | `84-south-park` | 13.2 m (LiDAR-derived, roof pergola crest; parapet 11.5 m) | new landmark |
| [92 South Park (86–96 South Park)](./92-south-park.md) | `92-south-park` | 13.28 m (LiDAR-derived) | new landmark |
| [95 Jack London Alley (Gran Oriente Filipino Masonic Temple)](./95-jack-london-alley.md) | `95-jack-london-alley` | 8.4 m (estimated — LiDAR roof deck 7.84 m plus a derived parapet) | new landmark |
| [326 Brannan Street (JAX Vineyards Wine Court)](./326-brannan.md) | `326-brannan` | 5.9 m (shed parapet; LiDAR deck 5.66 m) | new landmark |
| [340 Brannan Street](./340-brannan.md) | `340-brannan` | 17.79 m | new landmark |
| [45–49 South Park (Gran Oriente Filipino Residence)](./49-south-park.md) | `49-south-park` | 13.0 m (LiDAR-derived) | new landmark |
| [49 Zoe Street](./49-zoe.md) | `49-zoe` | 17.0 m (LiDAR max, stair/elevator penthouse crest; parapet 14.4 m) | new landmark |
| [246 Ritch Street](./246-ritch.md) | `246-ritch` | 18.76 m (LiDAR max, read as the roof stair/elevator penthouse — see its 2.15 risk 1; parapet 15.87 m) | new landmark |
| [248–250 Ritch Street](./248-ritch.md) | `248-ritch` | 8.6 m (cornice crest; measured twice — LiDAR mixture 8.65 m, rectified panorama 8.50 m) | new landmark |
| [1 South Park (One South Park)](./1-south-park.md) | `1-south-park` | 20.2 m (LiDAR `hgt_max`; penthouse roof 18.6 m, cornice crest 15.75 m) | new landmark |

## Shared contract (all 107)
| [252–254 Ritch Street](./254-ritch.md) | `254-ritch` | 8.8 m (LiDAR maximum, the roof flue; cornice crest 8.05 m estimated) | new landmark |
| [434 Brannan Street (Art Deco loft, 1929)](./434-brannan.md) | `434-brannan` | 13.79 m (LiDAR maximum, read as the rooftop mechanical penthouse; roof deck 11.46 m measured, parapet crest ~12.4 m estimated) | new landmark |
| [226 Ritch Street (226 Ritch Street Condominiums)](./226-ritch.md) | `226-ritch` | 18.1 m (roof crest, LiDAR-derived; 16.0 m parapet) | new landmark |
| [414 Brannan Street (Epic Church)](./414-brannan.md) | `414-brannan` | 14.0 m (monitor crest; 10.4 m street parapet) | new landmark |
| [501 Third Street](./501-third.md) | `501-third` | 16.4 m (LiDAR-derived) | new landmark |
| [10 South Park (South Park Lofts)](./10-south-park.md) | `10-south-park` | 14.67 m (roof bulkhead, LiDAR maximum; parapet crest 13.10 m photogrammetric) | new landmark |
| [50 United Nations Plaza (Federal Office Building)](./50-united-nations-plaza.md) | `50-united-nations-plaza` | 33.0 m (metal-roof crest, derived; 29.0 m parapet, 24.7 m north wing) | new landmark |

- Style: `docs/styles/miniature-toy.md` (authoritative for artistic decisions)
- Technical contract: `.agents/skills/sf-asset-check/SKILL.md` (authoritative for the GLB)
- Repo rules: `AGENTS.md` — in particular rule 3 (never delete the procedural
  fallback) and rule 5 (real coordinates, real heights; exaggerate in authoring, not
  in placement)
- Reference implementation: `artifacts/salesforce-tower/`
- Binary GLB, real meters, origin at base centre, geometry sitting on z=0, applied
  transforms, flat `Toy_*` colours from the project palette, `_Glow` only for
  night-glow surfaces, no textures, no transparency, no cameras/lights/animation,
  landmark budget <= 27,000 triangles

## Orientation note that applies to every plan

`placeGeneric()` in `app/src/assets.js` scales and positions an asset but never
rotates it, so each GLB must be authored in **true-world orientation** (Blender
`+Y` = north, `+X` = east). The asset contract's "front faces `-Y`" rule can only
be honoured literally for buildings whose real front happens to face south. Where
the two conflict, real-world orientation wins (AGENTS rule 5) and the deviation is
recorded in that asset's `REPORT.md`.

## Runtime status column

- **replaces procedural** — the id already exists in `app/src/landmarks.js` and in
  `pipeline/lib/landmarks.mjs`, so the GLB hides the procedural version on load and
  the existing exclusion zone already clears the baked city. No pipeline change.
- **new landmark** — no procedural builder and no registry entry. Integration needs
  a new entry in `pipeline/lib/landmarks.mjs` (id, lon/lat, height, exclusion
  radius, optional camera preset) **and a re-bake of the affected tiles**, or the
  baked procedural building will intersect the new GLB. Each plan's section 2.13
  spells this out.

## Research method and confidence

Anchors and footprints were measured from OSM geometry pulled directly from the
OSM API (`/api/0.6/way|relation`), reprojected locally, and reduced to a
minimum-area oriented bounding box — those numbers are marked as measured. Heights,
dates, architects and dimensions come from Wikidata claims and Wikipedia infoboxes
with the source named in each row. **Building photos and street-level visual
research** use the `exa` MCP server (`web_search_advanced_exa`) to find
elevation photos, rooftop/aerial views, real estate listing photos, and
architecture articles — see `docs/asset-pipeline/ADDRESS-TO-ASSET.md` Stage 1
for the exact search recipe. Anything visual, derived or unconfirmed is
labelled *inferred* or *estimated* and is called out again in each plan's section
2.15. Several OSM `height` tags describe only a low shell (City Hall 30 m, St
Mary's 18.9 m, Cal Academy 11 m, de Young 13 m) and must never be used as the
architectural target height. 550 Third Street is the sharpest case: its OSM
`height=7` and the 2010 city LiDAR agree, and both are wrong, because they
predate the rooftop penthouse that gives the building its crest. Chase Center is
the inverse case — three published figures (structural 31.755 m, OSM 38.1 m,
facade crest 40.84 m) each measure a different thing; see that plan's 2.1. 543
Presidio Blvd is a third variety: its OSM `height=8` is neither eave nor crest but
the LiDAR *median* height over a hipped roof, which by construction falls between
the two — the crest is 9.55 m. The Asian Art Museum is a fourth: its OSM
`height=46` is not a height at all but the NAVD88 roof *elevation* (152.93 ft),
1.6x the real 28.1 m crest — see that plan's 2.3 before trusting any `height` tag
that could plausibly be a sea-level datum. 101 South Park is a fifth variety and the
nastiest so far: its OSM `height=6` and the 2010 LiDAR median (5.56 m) agree with each
other and are both *correct for 2010* — they simply predate the second storey the building
has today, so every published height for that lot is stale rather than mismeasured. Check
the LiDAR's vintage against the permit history before believing a small number.

The new Main Library across Fulton Street carries the *same* `height=46` as the Asian
Art Museum, for the same reason, and is really 28.98 m — so that tag has now caught two
adjacent Civic Center blocks.

350 Brannan Street is a different kind of failure: not a wrong height but a missing
*building*. Nominatim resolves the address onto the Brannan Street roadway by TIGER
interpolation, and no footprint on that block is tagged `addr:housenumber=350`. The
resolution runs address -> DataSF parcel APN -> parcel centroid -> the footprint containing
it. When a geocoder returns `osm_type: way` for an address, check whether that way is a
building before believing it.
that could plausibly be a sea-level datum. 135 South Park is the opposite problem — no
`height` tag at all and no photograph of its street elevation anywhere, so its height is
LiDAR-only and its facade is openly a typological reconstruction; that plan's 2.15 leads
with the admission rather than burying it, and its Part 1 tells the executing agent to
read 2.15 before starting.
that could plausibly be a sea-level datum. 362 Brannan Street is a fifth variety and the
most ordinary-looking one: its OSM `height=6` is neither eave nor crest nor datum, it is
simply the *other part of the building* — the one-storey block that covers about four
fifths of the plan — while the crest, on a set-back sloped roof over a two-storey front
bay, is 8.58 m. A tag can be an honest measurement of the wrong feature.

165–167 South Park is the one plan here whose footprint is **not** measured from OSM, and
it is the case that shows why the default has limits. No OSM way carries its address at
all: the building sits inside a Bing trace tagged `167` that is larger than the whole lot
and overlaps its neighbour. That plan's geometry comes from the surveyed DataSF parcel
(`acdm-wktn`), with the DataSF LiDAR footprint (`ynuv-fyni`) supplying only the built depth
— and even those two disagree by 3.7 m, which its 2.3 reconciles. On dense narrow-lot
blocks, prefer the parcel layer and treat OSM as a cross-check.

358 Brannan Street breaks the pattern: there the bad number is not a height but the
**footprint**. Its OSM way (`source=Bing`) traces a 115 m2 stub, wide and shallow,
where the building is in fact a 166 m2 through-lot 6.9 m wide and 25.2 m deep — the
DataSF LiDAR footprint and the Assessor's lot area agree with each other against OSM.
Where a plan cites a DataSF `mblr`/`sf16_bldgid` footprint, that is the survey; OSM
geometry on small SoMa lots is a Bing trace and should be treated as a cross-check
only. Getting from an address to the right DataSF polygon goes through the parcels
dataset (`acdm-wktn`, `blklot` -> address range), not through a spatial guess.

10 South Park is the set's hardest *resolution* case, and it fails in two ways at once.
First, no OSM way carries its address at all, so Nominatim TIGER-interpolates onto the
South Park roadway and returns `osm_type: way` — the 350 Brannan failure mode, and it
looks like a building hit. Second, it is a **condominium**: the address exists ten
times over, on lots 3775/106 through 3775/115, all sharing one parcel polygon. Only the
address -> DataSF address table -> APN -> parcel -> footprint route survives both. It
is also the set's clearest case of a lot with **two** baked buildings and an open
courtyard between them, so like 132 South Park it needs one exclusion zone per
structure plus a guard zone at the anchor; the difference is that here both buildings
are traced twice, by DataSF and by Overture, so a correct exclusion drops four rings.
that could plausibly be a sea-level datum. 181 South Park is a fifth: its `height=14`
matches the LiDAR median to within 0.2 m, which makes it look corroborated rather than
merely repeated, and the crest is still 2.3 m above it.

One plan, [181 South Park](./181-south-park.md), was written with nadir aerial imagery but
no street-level imagery available to its author. Its geometry is measured, its roof is
observed, and its four elevations are explicitly marked as inference; street-level photo
research is written into Part 1 as a gate that must clear before modelling starts. It is
also the set's clearest case of an OSM `height` tag that is neither eave nor crest: on a
ridged roof the LiDAR median it matches corresponds to no physical line on the building.
Read that plan's Part 2 preamble before executing it.

551 Third Street is the odd one out in a different way: it is a *site*, not a
building — a service-station forecourt whose asset is a canopy, two pump islands,
a kiosk and the asphalt they stand on. Its `targetHeightM` is a thin crest above
a measured canopy deck, and its exclusion zone cannot be solved with one circle;
see that plan's 2.13 and 2.15 before treating it as routine.

599 Third Street is the reassuring counter-example: its OSM `height=16` and the LiDAR
median (15.62 m) agree on the parapet and both are right — the tag is only untrustworthy
by default, not always wrong. There the open question is the other end, the LiDAR
`hgt_max` of 18.34 m, which is a single maximum and could be a mast rather than the
penthouse.

250 Van Ness is a different trap again: OSM and the LiDAR *mode* agree on ~10 m while
Overture — the pipeline's own bake input — carries 12.4 m, because both the LiDAR max
(13.0 m) and the LiDAR min (2.5 m) on that footprint are street-tree canopy, not
building. A height read off a raster statistic is only as good as the raster's edges.
592 Third Street is the same trap at a larger ratio: its LiDAR `hgt_max` of 11.65 m is
3.8 m above a roof-deck mode of 7.82 m on a footprint whose height standard deviation is
0.64 m — a 6σ outlier that is simply the two street trees overhanging the 3rd Street
parapet, with the 2.40 m `hgt_min` as the matching artifact at the other end. Where 370
Brannan could legitimately take `hgt_max` as its crest (0.6 m above the median), doing
the same here would build a three-storey building. Check the max against the standard
deviation before believing it.

The Earl Warren Building is another variety again: its OSM `height` is fine, but the
LiDAR record's `hgt_maxcm` (46.39 m) sits 19 m above its own roof plane, because the
footprint shares a party wall with the 54 m Hiram W. Johnson slab and a 0.5 m cell on
that boundary samples the tower. Treat a single-cell `hgt_max` on a party wall as
unusable. That plan's 2.14 is also the set's clearest exclusion-radius trap: the usual
half-diagonal would have deleted the neighbour.

150 South Park is the tightest exclusion case in the set and the one that shows *why* the
half-diagonal rule is wrong rather than merely risky. Its own footprint has to be cleared
by its **centroid** (3.24 m from the anchor), because its nearest ring vertex — 6.10 m — is
a party-wall node it **shares with 156 South Park**, whose nearest vertex is therefore also
6.10 m. Any radius that reaches our corner reaches the neighbour's, so the safe window is
3.24 < r < 6.10 and the half-diagonal (~9.5 m) would have taken out both neighbours. Size
the radius from `excluded()`'s actual test — centroid **or** any vertex — against both bake
sources, not from the building's own dimensions.

434 Brannan Street is the set's clearest case of a measurement that simply refused to
close. Its roof deck is one of the best-pinned numbers in the whole collection (LiDAR mode
11.43, median 11.46, mean 11.36, sd 0.92 m over 3,086 cells, with OSM's `height=11`
agreeing), and its LiDAR maximum of 13.79 m is a believable +2.5σ with no canopy over the
footprint. What could not be settled is the parapet in between: an equirect
elevation-angle solve off the Street View pano returned a wall crest *below* the measured
deck, and a rectilinear width-and-pitch solve off the same pano returned answers 20% apart
depending on which row was measured. That plan's 2.15 leads with the failure rather than
quoting the more flattering of the two. It also records why the failure is survivable —
the body is normalised to the measured deck and `targetHeightM` is by definition the
export's own top — which is the general reason to prefer "deck measured, crest inferred"
over "crest measured badly".

The executing agent is expected to re-verify height, anchor, footprint and
orientation before modelling — the dossier is a head start, not a citation.

## Night renders: drive `_Glow` from Base Color, not from the imported emission

A review rig that re-imports the exported GLB (which is the required way to
render — always render the file that ships) cannot simply raise
`Emission Strength` on the `_Glow` materials. glTF writes
`emissiveFactor = 0` when the authored emission strength is 0, so a re-imported
`_Glow` material carries a **default white** emission and every glow surface
renders as a white slab. Copy `Base Color` into `Emission Color` and use
strength 1.0 — that is also exactly what the app does, since its night layer is
an unlit overlay drawn at the material's own baked colour. Caught on
`chase-center` (its blue video board rendered pure white);
`tools/glb-optimize/render_ab.py` already does it correctly.
