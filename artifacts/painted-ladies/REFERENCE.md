# Painted Ladies reference dossier

Research checked 10–11 August 2026 for the six-house SF-SIM asset at **710, 712, 714, 716, 718 and 720 Steiner Street**. The larger corner house at 722 and the building at 700 are context only and are excluded.

## Adopted facts

| Item | Adopted value | Evidence / confidence |
|---|---:|---|
| Six addresses | 710–720 Steiner Street, even numbers | OSM individual building ways; ASNA and SF Planning identify the row |
| Per-house footprint | 15.85–16.14 m deep × 6.85–7.14 m wide | Recomputed from OSM node coordinates in a local metric projection |
| Six-house span | about 41.7 m including half-widths at the ends | Recomputed from the six OSM front-edge centres |
| Individual architectural height | 12 m mapped; **12.5 m adopted to main ridge** | Each OSM way has `height=12`; the extra 0.5 m is a conservative ridge/miniature allowance |
| Ground fall | about **2.9 m across the six**, south/high to north/low | USGS NED 10 m samples via OpenTopodata: 65.56 m at 710 to 62.66 m at 720; approximately 0.58 m per house |
| Anchor | **[-122.432740, 37.776228]** | Centre of the combined OSM six-way bounding box; longitude agrees with the plan, latitude is about 4.8 m north of its draft value |
| Row bearing | **350.87° toward the north end / 170.87° toward the south end** | Least-squares line through the six measured front-edge centres |
| Front outward normal | **260.87° (west-southwest)** | Perpendicular to the measured row line and checked against Steiner Street and Alamo Square geometry |
| Authoring axes | Blender +X east, +Y true north, +Z up | SF-SIM asset convention; heading is baked into vertices |

## Important orientation correction

The task plan says the facades face east and places the houses on the west side of Steiner Street. Independent map geometry shows the opposite: the six footprints are **east of the Steiner Street centreline**, while Alamo Square is west of it. The famous postcard photograph is therefore taken from the park looking generally east, toward facade surfaces whose outward normal is west-southwest (260.87°). The model follows the measured geography rather than repeating the plan's east-facing statement. In the controlled review set, `painted-ladies-west.png` is the postcard/front elevation because the camera stands west of the asset.

## Sources and what they establish

### Institutional and neighborhood history

- [SF Planning, *Alamo Square* historic walking tour](https://default.sfplanning.org/Preservation/walking_tours/Walking_Tour_ALAMO_SQUARE.pdf) — identifies 710–722 Steiner as “The Painted Ladies,” dates the Queen Anne houses to 1892–1895, and describes projecting bays as a defining district feature. Its typology distinguishes angled Italianate bays, rectangular Eastlake/Stick bays, and more ornate/asymmetrical Queen Anne bays.
- [SF Planning, Article 10 and Article 11 Districts](https://sfplanning.org/resource/article-10-and-article-11-districts) — confirms the Alamo Square Article 10 Historic District and its official extent.
- [Alamo Square Neighborhood Association, Explore](https://alamosquare.org/explore/) — identifies the famous row as 710–720 Steiner and attributes its 1892–1896 construction to Matthew Kavanaugh.
- [Victorian Alliance of San Francisco, Shannon–Kavanaugh House history](https://victorianalliance.org/the-kavanaugh-house-history/) — distinguishes Kavanaugh's larger 722 Steiner corner house from the six gabled cottages; useful for enforcing the requested scope boundary.

### Survey geometry, height, colour and grade

- OpenStreetMap ways [710 / 261412896](https://www.openstreetmap.org/way/261412896), [712 / 261412895](https://www.openstreetmap.org/way/261412895), [714 / 261412900](https://www.openstreetmap.org/way/261412900), [716 / 261412894](https://www.openstreetmap.org/way/261412894), [718 / 261412879](https://www.openstreetmap.org/way/261412879), [720 / 261412899](https://www.openstreetmap.org/way/261412899) — individual footprints, address identity, `height=12`, roof tags and mapped exterior/roof colours. Measurements were independently recomputed from raw way-node coordinates rather than copied from the asset plan.
- [OpenStreetMap Steiner Street](https://www.openstreetmap.org/way/112408723) and [Alamo Square](https://www.openstreetmap.org/way/745183964) — establish that the houses lie east of the street and the park lies west, resolving the facing direction.
- [OpenTopodata API](https://www.opentopodata.org/) using the `ned10m` dataset — terrain samples at each footprint centre: approximately 65.56, 64.97, 64.33, 63.81, 63.45 and 62.66 m from 710 through 720. The model simplifies the irregular samples to a deterministic 0.58 m step.
- [Esri World Imagery](https://www.arcgis.com/home/item.html?id=10df2279f9684e4a9f6a7f08febac2a9) — top-view cross-check: six parallel steep main roofs, narrow party-wall rhythm, chimneys, and smaller/lower rear roof extensions. Imagery was used for observation only and is not committed.

### Elevation and appearance references

- [Wikimedia Commons category: Painted Ladies (San Francisco)](https://commons.wikimedia.org/wiki/Category:Painted_Ladies_(San_Francisco)) — multiple attributed dates and viewpoints, including the canonical park-facing front, oblique end views, wider ground context, and changing paint schemes. No source photographs are committed.
- [Wikimedia Commons, broad 2022 view](https://commons.wikimedia.org/wiki/File:San_Francisco_(CA,_USA),_Painted_Ladies_--_2022_--_3059.jpg) — recent front rhythm, gables, bay returns, stoops, roof/chimney silhouette and muted contemporary colours.
- [SFGate, Alamo Square Historic District](https://www.sfgate.com/travel/streetdate/article/street-date-alamo-square-historic-district-3936933.php) — secondary corroboration for the six 710–720 houses and their relationship to 722.
- [Coldwell Banker, 714 Steiner listing](https://www.coldwellbankerhomes.com/ca/san-francisco/714-steiner-st/pid_34245600/) — confirms three levels, raised garage/basement, Victorian wood-frame construction and bay-window views at 714. Listing material is used only as a dimensional/interior-level cross-check.
- [New York Post, 714 Steiner permit/listing report](https://nypost.com/2022/05/23/san-francisco-home-from-full-house-intro-lists-for-3-55m/) — reports approved architectural plans and oversized front bays on all three levels; useful as a corroborating diagram/level source, not as primary geometry.
- [Jim Corwin dusk photograph listing](https://jimcorwin.photoshelter.com/gallery-image/Retro-Images-Of-San-Francisco/G0000WLK7PWEZcxI/I0000pi1SoZbT5zA) and [Eric Bowers dusk photograph listing](https://www.ericbowersphoto.com/image/I0000CrmJAtOQKqE) — establish that the row remains predominantly a dark residential silhouette at dusk with sparse warm interior lights, not a luminous landmark. Consequently only tiny doorway lamps use `_Glow`; windows do not.

## Elevation observations

### West / street front

This is the recognition elevation. Six nearly equal-width Queen Anne fronts repeat a two-storey canted bay, a narrow entry strip, raised basement/garage, steep front gable, heavy pale cornice and a long stair. The trim reads as a shared horizontal cadence while paint colour and small gable details distinguish each house. The bay fronts are broad and the canted side returns are visible in oblique photographs.

### East / rear

Aerial imagery and oblique photography show plainer rear masses rather than six ornamental fronts. Main roof ridges continue toward the rear, then terminate above varied lower extensions/decks. Rear walls have smaller paired windows, simple doors and shallow parapet/rail conditions. The asset preserves this broad organization but does not reconstruct undocumented porches or lot landscaping.

### North end

The north end of 720 exposes a long, mostly plain flank beneath the gable/hip profile. A few vertically aligned windows are credible, while the adjacent 722 house is explicitly excluded. The north end is lower because Steiner Street descends toward this end of the six-house run.

### South end

The south end of 710 exposes the opposite long flank and the highest base/roof position in the six-house group. The nearby 700 building is excluded. End-wall windows are simplified to two stacked pairs so the surface is not blank from SF-SIM's aerial camera.

### Above

The strongest top cue is six parallel steep roof ridges running approximately east–west (80.87°/260.87°), with narrow separators, one slender chimney per house, a single rust-coloured roof accent, front gable caps and smaller/lower rear roofs. The exact skylights, vents, pipes and later alterations vary across imagery and are omitted.

## Address-by-address design mapping

The OSM colour tags are useful survey evidence but are not a calibrated paint specification and photographs show repainting over time. They are translated to the nearest approved SF-SIM palette colour rather than eyedropped.

| Address | OSM wall / roof tag | Observed front type | Miniature mapping |
|---|---|---|---|
| 710 | `#c9b085` / `#515151` | gabled; repeated canted bay | `Toy_sand`, dark roof, gold gable accent |
| 712 | `#cad8d5` / `#4a4a4a` | gabled; repeated canted bay | `Toy_sky`, dark roof |
| 714 | `#dadbde` / `#8c543d` | gabled; repeated canted bay | `Toy_cream`, `Toy_rust` roof |
| 716 | `#e4c78b` / `#8f7d67` | gabled; repeated canted bay | `Toy_mustard`, dark roof, red gable panels |
| 718 | `#d4ceb0` / `#4a4a4a` | gabled; repeated canted bay | `Toy_verdigris`, dark roof |
| 720 | `#d5c09d` / `#4a4a4a` | gabled front; roof classification varies by source | `Toy_mint`, dark roof |

All six are modeled with canted bay returns. Photographs make the projecting, canted geometry clear; no source supported replacing one with a wholly square bay. All six receive a steep triangular street gable because this is visible in current broad front photographs. OSM's roof classification describes the larger roof mass and does not reliably encode the decorative street-front gable.

## Recognition cues, ranked

1. Six tightly packed, equal-width houses forming one stepped row.
2. Six individually tinted fronts united by pale trim and a shared silhouette.
3. Repeated two-storey projecting canted bays plus long front stoops.
4. Six steep front gables and parallel main roof ridges.
5. The downhill step and chimney rhythm visible from the park and from above.

## Preserve

- Exactly six 710–720 units and their party-wall rhythm.
- Real measured heading and west-facing fronts.
- Approximately 16 × 7 m per-house massing.
- Baked 2.9 m grade difference across the row.
- Two-storey canted bays, raised entries and eight-step stoops.
- Heavy cornice, chunky corbels, gable trim and dark graphical windows.
- Designed rear extensions and roof/chimney silhouette for aerial credibility.

## Simplify

- Carved brackets, spindlework, shingle patterns and tiny moulding become broad trim bands and seven chunky corbels per house.
- Window muntins, curtains and reflections become flat `Toy_glass` panels.
- Stoop balusters become solid beveled rails.
- Rear porches, fences, utilities and later additions become low roof/rail masses.
- Roof shingles and flashing are represented by flat roof colours.
- Trees, cars, sidewalk, street, park, people and neighboring buildings are omitted from the GLB.

## Uncertainty and conflicts

- **Facing direction:** the plan says east; measured street/park/footprint geometry proves west-southwest. The measured geography is adopted.
- **Grade wording:** the prompt asks to investigate “~1 m per house.” NED10m gives an average 0.58 m over these six centres, with irregular individual changes and a total near 2.9 m. The model uses the measured average, not 1 m per house.
- **Anchor:** the plan latitude `37.776185` is south of the combined six-footprint centre. `37.776228` is adopted for an asset whose origin is the six-house bounding-box centre.
- **Dates:** SF Planning says 1892–1895; ASNA and common secondary sources say 1892–1896. This does not affect geometry; both are recorded.
- **Colours:** current photography, historic paint schemes and OSM tags do not perfectly agree. The model follows the address order and broad current muted family, translated into the approved palette.
- **Roof tags:** OSM roof-shape tags and visible decorative gables describe different layers of the roof. Broad photographs and aerial imagery govern the modeled silhouette.
- **Exact rear elevations:** public views are limited and obscured by vegetation. Rear window/door placement is a restrained visual inference built around verified main-depth and roof-extension evidence.
