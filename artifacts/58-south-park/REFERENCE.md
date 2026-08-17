# 54-58 South Park (58 South Park) — reference dossier

The as-built record for `artifacts/58-south-park/`. The plan is
`docs/asset-plans/58-south-park.md`; where this file and the plan disagree, **this file
is right and the plan is stale** (repo rule: REPORT beats plan). The build log,
including everything that was tried and rejected, is `REPORT.md`.

## What this is

One building on the north-west rim of the South Park oval, holding **three condominium
lots**: `58` the ground-floor commercial condo (creative office — Custom Spaces, Creandum
and Branch have all been tenants), `56` the middle flat, and `54` the penthouse that spans
the two upper levels and the roof. It was built in **2009** on the site of a two-storey
office block demolished in 2005, as one half of a pair with 44-46 South Park next door under
the same 2005 permit set. Four storeys, 9.73 m of frontage, 30.1 m deep, party walls on both
flanks.

The asset models the **whole building**, because that is what stands on the parcel; the
manifest id keeps the requested address.

## Verified facts as built

| Fact | Value | Source |
|---|---|---|
| Block / lots | 3775 / **219** (58), **220** (56), **221** (54) — three condo lots sharing ONE polygon, mapped 2009-09-09 | DataSF Parcels `acdm-wktn` |
| Predecessor | lot 3775/218 (2007-2009), before that 3775/050; the building on it was demolished under a 2005 permit addressed **64 South Park** | DataSF Parcels; SF Building Permits |
| Built | **2009** | SF Assessor `year_property_built` on all three lots; SocketSite photographed it under construction May 2009 |
| Storeys | **4** + a roof level | SF permit `200501052622` (2005-01-05) "to erect 4 story, 2 family dwelling w/retail commercial"; three later permits record `existing_stories = 4` |
| Roof structure | an enclosed roof-level room — "roof storage area", given a window in 2013; marketed as a "private office" beside the full-floor roof deck | SF permit 2013-10-15 on lot 221; Compass listing for 54 S Park St |
| Anchor (manifest) | **−122.3938881, 37.7821223** | assessor parcel centroid — measured; agrees with Google's own place pin for 58 S Park St to 2.5 m |
| Footprint | **9.729 × 30.10 m**, 292.8 m² = 3,152 sq ft, a clean parallelogram (edges close to 10 mm) | DataSF parcel polygon reprojected — measured; the 54 listing's "lot 3,168 sq ft" agrees to 0.5% |
| Heading | front faces **135.2°** true (SE, onto the park); rear 315.1°; NE flank 45.2°; SW flank 225.2° | measured from the parcel polygon |
| Party walls | **both flanks.** 3775/217 (44-46 South Park) shares the NE edge and 3775/053 (70 South Park) shares the SW edge **vertex-for-vertex** | DataSF Parcels — measured |
| Main parapet crest | **13.6 m** | 2010 LiDAR majority 13.59 m, OSM `height=14`, and four storeys at ~3.4 m — three independent readings that agree |
| Model crest (roof office) | **16.9 m** = `targetHeightM` | 2010 LiDAR maximum 16.94 m over this footprint; *estimated*, see the caveat below |
| Rear low element | the rear **4.5 m** of the lot is a single storey at **4.0 m** | 2010 LiDAR minimum 3.97 m over ~17% of the footprint, plus 2026 imagery — see "Where the low part is" |
| Ground elevation | 11.58 m min / 11.93 m median NAVD88, 0.85 m of range across the footprint | DataSF `gnd_*` — the app's terrain handles this, not the asset |
| Net living area | 56: 2,050 sq ft. 54: 2,960 sq ft over 2 levels. 58: not recorded (commercial condo) | SF Assessor secured roll 2016-2025 |
| Gross (marketed) | 8,000 sq ft | Cityfeet/CoStar listing for 58 |
| Architect | **none credited in any source found.** Vanguard Properties appears as developer/marketer only | — |
| Triangles | **4,664** of a 10,000 cap | `validation.json` |

## Two corrections the sources force

**1. "Year Built 1907" is wrong, and it is on every commercial listing for this address.**
Cityfeet, LoopNet and the rest all describe "this charming three-story building — originally
constructed in 1907". That is CoStar data inherited from the demolished predecessor. The
permit record (demolition 2005, four-storey erection 2005, completion 2009), the assessor
roll (`year_property_built = 2009` on all three lots) and a May 2009 construction photograph
all agree. A plausible-looking 1907 South Park building would have been the wrong answer and
it was one search away.

**2. The parcel is the survey, not OSM.** OSM way `124884349` traces the same building
3% smaller (284.9 m² vs 292.8) and shifted about 2.3 m north-west of the parcel. The DataSF
LiDAR building footprint `SF3775219` is smaller again (258.9 m², 8.69 m wide) because it is
derived from the roof outline and is inset. The assessor parcel matches the marketed lot area
to 0.5% and its edges are shared vertex-for-vertex with both neighbours' parcels, which is
what a real party-wall row looks like. The asset is built on the parcel.

## Where the low part is

The 2010 LiDAR over this footprint reports a **minimum of 3.97 m** against a majority of
13.59 m, with the mean (12.01 m) well below the median (13.50 m). A two-level fit to those
moments puts roughly **17% of the lot at about 4 m** and the rest at 13.6 m. On a 30 m deep,
9.7 m wide lot with party walls on both sides, that is either the rear of the lot or a
mid-depth lightwell, and the two give visibly different silhouettes from the app's camera.

It is the **rear**. Google satellite imagery (Vexcel, z21, 2026), sampled as raw tiles and
registered against the parcel polygon, puts the roof's rear parapet about **3 m in from the
rear lot line**, with the low strip behind it in permanent shadow from the four-storey block
in front. The asset drops the rear 4.5 m to 4.0 m, which is 15% of the lot — the LiDAR moments
want 17%, and 4.5 m is the depth the imagery supports.

## What the same imagery gave the roof

The roof is a **full-floor deck**, not a membrane: 54's listing copy is explicit ("the full
floor roof deck is an oasis with city views that sparkle at night. Completing this level is a
private office"), and the 2013 permit for a window in the roof storage area confirms the
office is an enclosed structure. Registered against the parcel, the z21 imagery reads, front
to back:

| Depth from the front | What is there | In the asset |
|---|---|---|
| 4–13 m | open deck with a furniture cluster at the park end | bench, table, three seats |
| ~6–22 m along the SW parapet | a planting run | three verdigris planters |
| ~17 m | a dark glazed element mid-depth | the skylight (54's retractable kitchen skylight) |
| ~20–25 m | a dark structure ~3.8 × 3.5 m plus an adjoining raised block | the roof office + stair, one dark cluster |
| 25.6–30.1 m | below the roof plane | the single-storey rear |

Resolution at z21 is about 59 mm/px, which is marginal for a 9.7 m wide roof — the layout is
*inferred* from the imagery plus the listing copy, not surveyed.

## The height caveat

16.9 m is the LiDAR **maximum**, and the two attached neighbours report maxima of 16.15 m and
16.35 m despite being lower buildings — the signature of mature street trees overhanging all
three footprints. What rescues it here is that a real enclosed structure is *known* to stand
on this roof (the 2013 permit, the listing's "private office"), so the maximum has something
to be. The main parapet at 13.6 m is solid; the 16.9 m crest is `estimated: true` in the
manifest and carries about ±1 m.

## What the front elevation is made of

Read west to east, from the January 2025 Street View pano (ground floor, unobstructed) and
the May 2009 SocketSite photograph (upper facade, before the street trees closed over it):

- **58** (~3.0 m): a dark steel-framed glazed shopfront — glass doors with a transom — under
  a **tall mullioned window wall** that runs up through the plaster storeys. The `58`
  numerals sit on the dark spandrel above the doors.
- **56** (~3.7 m): pale plaster, a **dark vertical-slat vehicle gate** (the one secured
  parking space in 58's listing) with a narrow pedestrian door beside it, tall planters.
- **54** (~3.0 m): pale plaster, glass entry doors in a dark frame.
- **Storeys 2-3**: pale plaster with punched openings and a run of **black horizontal-bar
  balcony railings**.
- **Storey 4**: a **dark charcoal metal-panel box** with a horizontal band of tall windows —
  in the 2009 photograph a single dark cap sitting on the pale wall.

Bay widths of 3.0 / 3.7 / 3.0 m are read off the pano scaled against a 2.13 m door and are
*inferred* to about ±0.4 m; they sum to the measured 9.73 m frontage, so the reading is at
least self-consistent.

**The rear elevation is entirely inferred.** It faces the block interior toward Taber Place
and no imagery of it was found. It is visible from the app's camera.

## Recognition cues, in the order the asset spends on them

1. **The two-tone stack** — three storeys of pale plaster carrying a dark charcoal cap, the
   cap built 0.15 m proud so the split throws its own shadow line.
2. **The tall glazed bay at the west end of the front**, unbroken through all three plaster
   storeys — the only vertical element on a horizontally banded facade, and the hero night
   glow.
3. The three-address ground floor: shopfront, vehicle gate, residential door.
4. The black horizontal-bar balcony railings.
5. The designed roof deck seen from above.

## Deliberately not modelled

Both flanks. 44-46 South Park and 70 South Park are attached at 0.00 m; nothing on those
30 m walls is visible in the real world or in the app. House numbers, wall lamps, the
intercom, the door planters and the metal panel's fastener grid are all sub-pixel at the
app's camera distance and were left out (style bible §26).

## Sources

- DataSF Parcels `acdm-wktn` — the three condo lots, the shared polygon, the retired
  predecessor lots, the vertex-shared boundaries with 44-46 and 70 South Park
- DataSF Building Footprints `ynuv-fyni` (2010 LiDAR) — `SF3775219` height distribution;
  `SF3775217` and `SF3775053` used as controls
- SF Building Permits `i98e-djp9` — 29 permits on this lot: the 2005 demolition and
  four-storey erection, the 2007-2009 sprinkler and elevator permits, the 2008
  address-verification permit spelling out "54 residential / 56 residential / 58 commercial",
  the 2013 roof-storage window
- SF Assessor secured roll `wv5m-vpq2` (2016-2025) — 2009, the use classes, the net areas
- OSM way `124884349` — cross-check only
- https://socketsite.com/archives/2009/05/the_socketsite_scoop_on_5458_south_park_the_condos_comi.html
  — the May 2009 construction-stage exterior photograph and the unit programme
- https://www.compass.com/homedetails/54-S-Park-St-San-Francisco-CA-94107/1PHE91_pid/ —
  54's 2022 sale, the four levels, the roof deck and the private office
- https://www.cityfeet.com/cont/listing/58-south-park-st-san-francisco-ca-94107/cs36666880 —
  58 as creative office, 8,000 SF, the tenant list. **Its "Year Built 1907" is wrong.**
- Google Street View, pano at 56 S Park St, capture January 2025 — the ground floor
- Google satellite tiles, z21 (Vexcel, 2026), tile `x=335579 y=810539 z=21` and its
  8-neighbourhood — the roof layout and the rear parapet position

No reference imagery is committed: all of it is copyrighted and the URLs plus the tile
coordinates above are enough to re-fetch every frame this dossier is built on.
