# 21–29 South Park — reference dossier

Verified facts, sources and design decisions behind `21-south-park.glb`.
Compiled 16 August 2026. Where this document and
`docs/asset-plans/21-south-park.md` disagree, **this document and REPORT.md win** —
the plan is a starting point, the artifact is the record.

## 1. Identity

| Item | Value | Source / confidence |
|---|---|---|
| Address | **21–29 South Park**, San Francisco 94107; marketed and signed as **27 South Park** | DataSF parcel `3775042` (`from_address_num` 21, `to_address_num` 29, odd side); OSM `addr:housenumber` 21 and 27; the Jan 2025 Street View pano shows "21" and "27" painted on the wall — **verified** |
| Block / lot | 3775 / 042 | SF Assessor secured roll; DataSF footprint `mblr = SF3775042` — **verified** |
| Built | **1919** | SF Assessor `year_property_built`, rolls 2019 and 2022. LoopNet's listing says 1950 and is uncorroborated — **unresolved**, see §7 |
| Storeys | **2** | SF Assessor `number_of_stories = 2.0`; all 53 DataSF building permits record `number_of_existing_stories = 2`; confirmed in the pano — **verified** |
| Structure | **Unreinforced brick masonry**, wooden roof trusses, construction type 3 | DataSF permits: 1990 "parapet bracing"; 1990 "parapet corrective"; 1993 "repair to (e) wooden roof trusses"; 1993 "umb warehouse to have two party walls as per s.f. bldg. code"; 2001 "umb upgrade — plywood diaphragma & collector beams … to (e) braceframe" — **verified** |
| Use | Assessor class "Industrial"; **office in practice since 1991** | assessor roll vs. permit `existing_use`, which switches warehouse → office in 1991 and stays there — **verified** |
| Areas | lot 13,420 sq ft (1,246.7 m²); building **24,680 sq ft** (2,292.8 m²) = two floors of full-lot plate | SF Assessor; LoopNet gives the same 24,680 SF with a 10,904 SF typical floor — **verified** |
| Tenancy | **Redpoint Ventures** took the 4,200 sq ft ground floor at 27–29 in 2016 (fit-out by IwamotoScott Architecture, which preserved a brick archway from a former warehouse doorway); Transpose Platform Management and seven related LLCs registered at 27 South Park Suite 100, 2017–2024 | Architizer/IwamotoScott, bizprofile.net, DataSF permits — **verified** |
| Historic status | **none found.** Not a contributor to the South End Historic District — that nomination's only South Park entry is 1 South Park (3775/007), the 1913 Tobacco Company of California warehouse by William H. Crim Jr. | 194-page National Register nomination searched in full — **verified negative** |

## 2. Geometry, measured

| Item | Value | Source |
|---|---|---|
| Footprint (bake input) | DataSF LiDAR footprint `SF3775042`, 8 vertices, **1,115.1 m²** | `data.sfgov.org/resource/ynuv-fyni` reprojected with the app's tangent projection — **measured** |
| Footprint (cross-check) | OSM draws the same building as **three** ways — `112759863` (21, 453 m²), `112759868` (27, 408 m²), `112759865` (untagged, 253 m²) — summing to **1,114 m²**, agreeing to 0.1 % | OSM — **measured** |
| Oriented bbox | **32.749 × 40.676 m**, 83.7 % filled; depth axis bearing 315.97°/135.97° | minimum-area OBB — **measured** |
| **Anchor** | **−122.3931063, 37.7817676** — the footprint's **world-axis-aligned bbox centre** | **measured**; see §4 for why this is not the OBB centre |
| Area centroid | −122.3931097, 37.7817531 (1.63 m from the anchor) | **measured** |
| OBB centre | −122.3931361, 37.7817716 (2.63 m from the anchor) | **measured** |
| Axis-aligned XY bbox | 46.57 × 51.10 m — the expected consequence of a ~46° heading | **measured** |
| Roof deck | LiDAR median **9.60 m**, majority 9.82 m, mean 9.52 m, **σ 0.45 m** over 4,479 cells | DataSF — **measured**. Modelled at 9.50 m |
| Roof maximum | **11.73 m** | DataSF `hgt_maxcm` — **measured**; read here as the stair/lift bulkhead, see §7 |
| Cornice crest | **10.20 m** | *estimated* ±0.4 m from the Jan 2025 pano |
| Ground | 11.96 m min / 13.45 m max / 12.58 m mean NAVD88; the site falls **1.49 m** across the footprint | DataSF — **measured**. Small enough that the asset is NOT terrain-draped |

### Edges, with outward normals (Blender frame, +X east, +Y north)

| Edge | Length | Outward normal | What it is |
|---|---|---|---|
| main front | **19.69 m** | NW **315.7°** | South Park frontage, straight run — **exposed** |
| angled front | **12.07 m** | WNW **286.7°** | South Park frontage, following the oval's curve — **exposed** |
| jog A | 1.25 m | 282.6° | the small step at the north corner |
| jog B | 0.68 m | 225.7° | the small step at the north corner |
| NE party | 34.12 m | 43.8° | 17–19 South Park |
| NE party (short) | 6.58 m | 45.7° | 17–19 South Park |
| rear party | 32.75 m | 136.0° | the 318/326/334 Brannan row |
| SW party | 33.32 m | 226.3° | 35 South Park |

**Only the north-west front is exposed.** The other three sides are shared planes.
35 South Park carries `height=10` in OSM against this building's 9.50 m deck, so the
SW wall is essentially invisible; 318 Brannan carries `height=8`; 17–19 South Park has
no OSM height and a DataSF LiDAR median of 6.60 m with a 16.90 m maximum.

## 3. What each side shows

**North-west front (the hero, and the only exposed elevation).** Painted warm off-white
brick, 33.7 m long, bending 29° a little past the middle, in two registers:

- *Ground floor*: wide loft bays in near-black teal joinery, each in three parts — a big
  multi-pane window, a **cast-iron spandrel panel** with a repeated rosette-and-bar motif
  above it, and a **transom row of four small panes** above that. At the re-entrant bend,
  a **tall pair of flush teal freight doors** with the same spandrel and transom carried
  over them: the surviving warehouse loading bay. Toward the north end, the **office
  entrance** — a warm timber double door with a small transom and the street number
  painted on the brick beside it.
- *Second floor*: a regular rank of **segmental-arched windows**, teal sash, set straight
  into arched brick openings with no architrave. The rank runs the whole frontage and
  **turns the bend without interruption**, which is what makes the bend read as
  deliberate rather than as damage.
- *Cornice and parapet*: a projecting **corbelled brick cornice**, painted the same
  off-white, with a flat parapet above it. No signage, no ornament, no crown.
- Vertical service runs — a downpipe and a surface conduit — are visible and modelled.

**North-east, south-east and south-west**: party walls. Blank painted brick, no openings,
by observation rather than by omission.

**Top**: a grey membrane deck at 9.50 m. The **north-west third is clear** — an empty
apron behind the cornice. Behind it a dense field of condensers, a long duct run, a plant
housing and a **stair/lift bulkhead** toward the north-east. The rear third carries
scattered units. The contrast between the empty apron and the loaded field is the roof's
composition and it is what the imagery shows.

## 4. Orientation, placement and the anchor decision

Authored **in world space at the real heading** (+Y = true north, +X = east), so the
loader applies no rotation. The contract's "front faces −Y" rule cannot be honoured
literally: the building is rotated ~46° off the world axes and has *two* front planes at
315.7° and 286.7°. Real-world orientation wins (AGENTS rule 5); the substitute assertion
is the pair of measured outward normals.

**The origin is the footprint's world-axis-aligned bbox centre, not its OBB centre.**
Every other South Park plan anchors on the OBB centre, and on those near-rectangular
footprints the two points coincide to within centimetres. This footprint is a skewed
quadrilateral — its front is cut on a 29° diagonal — and the two centres are **2.63 m
apart**. `placeGeneric()` seats the *model's origin* at the anchor, and the contract
requires the model's origin to be its XY bbox centre, so anchoring on the OBB centre
would have slid the whole building 2.63 m west of its real footprint. Centred on the AABB
centre the exported offset is **(−0.34, +0.13) m**, and all of that residual is cornice
and bulkhead overhang, not footprint error — the footprint itself is centred to
(0.003, −0.005) m.

**Mirror check.** The angled plane is at the **north-east** end of the frontage (nearer
Second Street and 17–19 South Park) and the long straight plane at the south-west end
(nearer 35 South Park). Verified in the top render.

## 5. The Z stack

| z (m) | Element |
|---|---|
| 0.00 → 9.50 | body, one volume on the measured 8-vertex footprint |
| 0.00 → 4.20 | ground-floor loft bays, freight doors, office entrance |
| 4.52 → 4.76 | beltcourse at the second-floor line, front planes only |
| 5.45 → 8.55 | segmental-arched second-floor rank (sill 5.45, springing 8.05, 0.50 m rise) |
| 9.48 → 9.55 | roof deck |
| 9.50 → 9.86 → 10.20 | corbelled cornice, two steps, front planes plus 1.1 m returns |
| 9.50 → 9.90 → 10.00 | braced parapet and its coping, all four sides |
| 9.50 → 11.73 | stair/lift bulkhead — **the bounding-box top** |
| 9.53 → 10.48 | condensers, duct run, plant housing, vents |

## 6. Palette

| Material | Hex | Used for |
|---|---|---|
| `Toy_white` | `f7f4ec` | the painted brick body and parapet |
| `Toy_stone` | `d9d2c2` | cornice, coping, beltcourse, window sills, spandrel ribs, bulkhead cap |
| `Toy_sash` | `2f4f49` | **the near-black teal industrial joinery** — every reveal, frame, mullion, spandrel panel and the freight doors. **Off-palette, deliberate** (see REPORT.md §3) |
| `Toy_glass` | `2a4d73` | all glazing |
| `Toy_rust` | `a86444` | the timber office entrance — the one saturated accent |
| `Toy_steel` | `9aa0a6` | the roof membrane deck, downpipe, conduit |
| `Toy_roofd` | `45454a` | bulkhead, condensers, duct, plant housing, vents |
| `Toy_mustard_Glow` | `d9a441` | the lit ground-floor loft bays — the hero night state |
| `Toy_glassl_Glow` | `6f95b8` | three lit second-floor windows |

**Night state.** Four of the five loft bays carry a wide warm band; three second-floor
arches are lit cool; the office entrance transom is lit warm. Everything else goes dark.
The building reads at night as a line of lit ground-floor bays bending round a corner,
which is what a VC office block on the park actually looks like after dark. Glow surfaces
are thin shells proud of the opaque glazing, kept short in Z because a *closed* glow shell
presents two blended layers to the daylight camera, not one.

## 7. Recognition cues, ranked

1. **The bend in the street wall** — 19.69 m, then 29°, then 12.07 m. Unique in the
   manifest.
2. **The bright painted-white mass** against a block of greige and grey.
3. **The unbroken rank of segmental-arched windows** turning the corner with the wall.
4. **The three-register loft bays** with the teal freight door among them.
5. **The corbelled cornice over a low two-storey box** where the neighbours are three and
   four storeys.
6. **The roof**: clear apron on the park side, loaded field behind, one bulkhead.

## 8. Uncertainties

- **The 11.73 m crest is an interpretation.** The LiDAR maximum is measured; reading it
  as a stair/lift bulkhead rests on the rectangular structure visible in the Esri z20
  nadir. It could be a tall packaged HVAC unit. The error is contained: the loader scales
  by `targetHeightM / measuredHeight`, both are 11.73, so the scale lands on 1.0 and the
  building's real mass — the 9.50 m deck and the 10.20 m cornice — stays correct whatever
  that object is.
- **The 10.20 m cornice crest is estimated at ±0.4 m**, read off one oblique pano with a
  street tree across it.
- **Build year 1919 vs 1950 vs "the 1920s"** — assessor vs. LoopNet vs. a Perkins&Will
  project page for a South Park building that could not be identified as this one.
- **Bay and window counts** are read off two oblique January 2025 panos with a crape
  myrtle in front of them. The *rhythm* is well evidenced; the counts are the softest
  numbers in the asset. See REPORT.md §2.
- **Three of four elevations are inferred to be blank**, on the strength of the Esri
  nadir showing neighbouring roofs abutting all three.

## 9. Sources

- `https://data.sfgov.org/resource/ynuv-fyni` — DataSF LiDAR building footprints, record
  `SF3775042`: the footprint the pipeline bakes, and the full height distribution
- `https://data.sfgov.org/resource/acdm-wktn` — DataSF parcels, record `3775042`
- `https://data.sfgov.org/resource/wv5m-vpq2` — SF Assessor secured roll, block 3775 lot 042
- `https://data.sfgov.org/resource/i98e-djp9` — DataSF building permits, block 3775 lot
  042, 53 permits 1990–2021
- `https://www.openstreetmap.org/way/112759863`, `.../112759868`, `.../112759865` — the
  three OSM ways over this building
- `https://www.openstreetmap.org/way/147508663` (17;19 South Park),
  `.../112759864` (35 South Park), `.../112759869` (318 Brannan) — the party-wall neighbours
- `https://www.loopnet.com/Listing/21-29-S-Park-St-San-Francisco-CA/20707079/` — 2 storeys,
  brick and timber, 24,680 SF, operable windows on the park, Class C
- `https://architizer.com/projects/redpoint-ventures/` — IwamotoScott, Redpoint Ventures at
  27–29 South Park, 2016, "raw brick and timber ground floor", the preserved brick archway
- `https://sfplanninggis.org/docs/NatRegDistricts/2008-06-26_Final-NR-SouthEndHistDist.pdf`
  — searched in full; this parcel is not a contributor
- `https://sfcityguides.org/tour/old-south-park/` — the block's Gold Rush → Japanese and
  Filipino → warehousing → dot-com → VC arc
- Google Street View, panos at `37.7819404,-122.3934446` and `37.7818985,-122.3933928`,
  capture **January 2025** — the front elevation
- Esri World Imagery, nadir z20 (~0.15 m/px) — the roof, and the confirmation that all
  three non-street sides abut neighbouring roofs
