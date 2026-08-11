# Ferry Building reference dossier

Research checked 10 August 2026. Published facts are kept separate from measured or visual inference.

## Sources and what they establish

### Primary / institutional

- [Historic American Buildings Survey CA-1910, Library of Congress](https://www.loc.gov/item/ca0641/) — identifies the classicizing Baroque/Beaux-Arts building and modified Giralda-inspired tower; records a foundation platform about 166 × 670 ft and Colusa sandstone over a steel/brick core.
- [1978 National Register nomination, NPS](https://npgallery.nps.gov/GetAsset/c61103ba-92dd-401a-9fce-439251eda839) — contemporary historic description: 659 ft length; 235 ft tower; 23 ft clock faces; slender square tower; Ionic-column openings, bracketed/dentillated cornices, central pavilion, three-storey arcade wings, west sandstone facade, rear/end brick and galvanized iron, and the 48 ft wide × 42 ft high nave. This is also the strongest source for the original west/east material difference.
- [OpenStreetMap way 558731934](https://www.openstreetmap.org/way/558731934) — current mapped footprint, address and body `height=15`. I downloaded its 50-node geometry independently through Overpass and measured it below.
- [Perkins&Will restoration project](https://perkinswill.com/project/ferry-building/) — 2003 adaptive reuse, 238,000 sq ft, restoration of the nave/skylights and five-bay openings on each side of the central nave.
- [American Planning Association Great Places](https://www.planning.org/greatplaces/spaces/2010/ferrybuilding.htm) — 660 ft skylit nave; 245 ft clock tower; 22 ft dials; restoration quantities including 11 monumental brick/terracotta arches, 34 tall clathri windows and 12 steel arched trusses.

### Secondary factual cross-checks

- [San Francisco Ferry Building](https://en.wikipedia.org/wiki/San_Francisco_Ferry_Building) — 245 ft / 75 m tower, four 22 ft / 6.7 m dials, 660 ft / 200 m Great Nave, 1898 opening, A. Page Brown and Beaux-Arts design. The page is useful as a summary, but the HABS/NRHP records above are preferred where figures conflict.
- [Emperor Norton Trust: Ferry Building and the Giralda](https://emperornortontrust.org/blog/2022/11/15/sf-ferry-building-clock-tower-and-the-giralda-of-spain) — traces the Giralda claim through historic newspaper drawings and preservation nominations, and documents the recurring historic 235 ft figure.

### Attributed visual references

All listed images are hosted on Wikimedia Commons; they were inspected but are not committed to this repository.

- [JaGa, west elevation, CC BY-SA 4.0](https://commons.wikimedia.org/wiki/File:San_Francisco_Ferry_Building_(cropped).jpg) — strongest straight-on west reference: central three-bay pavilion, symmetrical long wings, tower proportions, upper and ground arcade rhythms, roof lantern and clock/crown detail.
- [Daniel Lu, west elevation from Hyatt, CC BY-SA 4.0](https://commons.wikimedia.org/wiki/File:Ferry_Building_San_Francisco_from_Hyatt_Regency_with_R-Evolution_and_Bay_Bridge_2026_dllu.jpg) — entire front in one frame; confirms the tower/body scale and end conditions.
- [Daniel Lu, east/bay side at night, CC BY-SA 4.0](https://commons.wikimedia.org/wiki/File:View_of_the_Ferry_Building_from_Pier_1,_San_Francisco_dllu.jpg) — east gables, lit large nave arches, illuminated clocks/crown and red roof signs; ferry gates are visually attached but separate.
- [Daniel Lu, north-oblique clock tower, CC BY-SA 4.0](https://commons.wikimedia.org/wiki/File:Ferry_Building_clock_tower_as_seen_from_the_North.jpg) — north/east tower faces, deep cornice stages, paired belvederes and clock projections.
- [King of Hearts, south/east oblique, CC BY-SA 4.0](https://commons.wikimedia.org/wiki/File:San_Francisco_Ferry_Building_January_2014_panorama.jpg) — bay-side end pavilion/gable and long roof profile.
- [Daniel Lu, night skyline from Treasure Island, CC BY-SA 4.0](https://commons.wikimedia.org/wiki/File:View_of_the_Ferry_Building_from_Treasure_Island,_San_Francisco_dllu.jpg) — the clocks and upper crown are the dominant night identity; the body stays subordinate.
- [Eric Chan, aerial city view, CC BY 2.0](https://commons.wikimedia.org/wiki/File:Embarcadero_%26_Market_(5028667417).jpg) — high oblique context and roof reading.
- Esri World Imagery satellite tile, inspected 10 August 2026 — top plan, roof ridge, footprint heading and relationship to Market Street/ferry aprons. It is not redistributed here.

## Verified dimensions and location

| Item | Decision | Evidence / treatment |
|---|---:|---|
| Long body | **201.0 m** | Independent minimum-area oriented bounding box of OSM way 558731934: 201.00 × 56.08 m; HABS platform 670 ft and NRHP 659 ft bracket the same ~201–204 m overall scale. |
| Width | **56.1 m** | OSM oriented bound. The HABS 166 ft / 50.6 m platform dimension is smaller; current mapped additions/end geometry plausibly explain the difference. The asset uses 56 m. |
| Body cornice | **15 m** | Current OSM body height tag, visually consistent with the long wings. |
| Architectural height | **74.7 m / 245 ft** | APA and current published summaries. The 1978 NRHP nomination says 235 ft. The model/manifest follows the currently requested and commonly published 245 ft architectural height; disagreement is recorded. |
| Clock dial | **6.7 m / 22 ft diameter** | APA/current summary. NRHP says 23 ft. The model uses 6.7 m. |
| WGS84 asset anchor | **[-122.3933697, 37.7955227]** | This point lands on the central tower/body centerline and is more appropriate for model placement than the whole irregular polygon centroid. Independently computed OSM polygon centroid is [-122.3934398, 37.7955325], about 6.2 m west; the difference is documented rather than silently substituted. |
| Footprint area | **9,846.9 m²** | Shoelace area from downloaded OSM geometry; corroborates the plan's 9,847 m². |

## Orientation

Blender coordinates are authored as `+X = east`, `+Y = true north`, `+Z = up`.

A minimum-area oriented rectangle fitted to OSM way 558731934 gives:

- long axis bearing **143.6° / 323.6° clockwise from true north** (southeast–northwest);
- short axis bearing **53.6° / 233.6°**;
- the Market Street/west front outward normal points approximately **233.6°** (southwest).

The asset's local 201 m axis is therefore yawed **-53.6° from world +X**, making its local `-Y` side the west/Market elevation while retaining the real-world heading. This is why the generic `front = -Y` convention cannot be interpreted as world south for this landmark.

## Elevation and roof observations

### West / Market Street front

The ceremonial elevation is strongly symmetrical. A three-bay monumental central pavilion projects slightly from the long wings and uses giant arches with paired columns. Each wing is a continuous two-level rhythm: small round-arched ground openings, a strong belt course, then tall pilastered upper windows with semicircular heads. Counting from the strongest straight-on image yields roughly 15 upper arch bays per wing; several ground bays are altered or visually obscured. For a readable miniature, the model uses **14 upper bays and 12 ground arcade openings per wing**, plus three monumental center arches.

### East / bay side

The bay elevation is more utilitarian and has acquired ferry-gate structures, gangways and waterside additions that are explicitly out of scope. Historic evidence says the rear was brick/galvanized iron rather than the west sandstone facade. Modern views show a continuous roof-level arcade, a glazed lower waterside strip and prominent gabled end/central nave faces. The asset keeps the same broad rhythm and cream architecture so it reads coherently at city scale, but differentiates the east with larger dark upper arch glazing and simplified ground openings. No gangways or ferry-gate sheds are exported.

### North and south ends

The ends terminate in broad gables over large arched windows, with smaller side arches and the cornice returning around the corners. Both ends must read as designed faces, not capped boxes. The miniature uses a centered tall arched window, paired smaller arches and a triangular gable on each short end.

### Roof / above

The roof is a dominant 200 m-long surface from the app camera: dark hipped planes, a long raised clerestory/skylight ridge, the central tower penetrating the ridge, orderly roof plant clusters and a strong parapet/cornice edge. The west `PORT OF SAN FRANCISCO` roof signage and ferry infrastructure are recognizable in photography but omitted: text would be too fine and surrounding attachments are outside scope.

### Tower and crown

The tower is slender and square, not a fat campanile. Its lower shaft rises largely unornamented above the main cornice, with one oversized clock on every side. Above the clock is a layered sequence: perforated/frieze band; deep cornice; open square Ionic belvedere; stepped pyramidal setbacks with corner finials; another open square stage; circular colonnaded lantern; small copper/bronze-toned domed cap; flagpole. The model preserves this vertical rhythm with chunky bands and open stages rather than literal capitals, dentils or balusters.

### Day and night

By day the building reads as pale warm stone with dark graphite roof and dark blue-grey openings. At night the four clocks and upper crown are visibly illuminated and dominate the identity. The exported miniature therefore uses `_Glow` only on the four clock dials; the crown remains pale material rather than becoming a large emissive lantern, avoiding excessive night glare in the app.

## Recognition cues

1. Extreme horizontal/vertical contrast: a ~201 m low ribbon punctuated by one 74.7 m central tower.
2. Four oversized circular clock faces on a slender square shaft.
3. Long repeated round-arch rhythm and monumental three-arch west entrance pavilion.
4. Stepped Giralda-derived crown: open belvederes, circular lantern, domed cap and flagpole.
5. Cream stone against a long dark roof/clerestory.

## Features preserved

- True footprint proportions and measured world heading.
- Symmetrical west facade with central three-bay pavilion.
- Repeated arcade rhythm on all visible sides.
- Four 6.7 m clock faces, rings, ticks and chunky hands.
- Layered open crown silhouette and flagpole.
- Designed roof ridge, skylight/clerestory and grouped plant.
- End gables and arched glazing.

## Features simplified

- 14 upper + 12 lower bays per wing rather than reproducing every altered real bay.
- Flat dark recessed arch fields instead of literal sash, clathri tracery or interiors.
- Cornices reduced to a few substantial projecting bands.
- Classical columns and capitals reduced to clean beveled piers.
- Crown balustrades/dentils/finials grouped into broad readable forms.
- Roof mechanical equipment grouped into four tidy clusters.
- No signage, market fixtures, people, palms, roads, platforms, gates or gangways.

## Uncertainties and conflicts

- **Tower height:** current/APA sources give 245 ft; the NRHP nomination gives 235 ft. Use 245 ft / 74.7 m because it is the project contract and current architectural figure.
- **Clock diameter:** current/APA sources give 22 ft; NRHP gives 23 ft. Use 22 ft / 6.7 m.
- **Overall width:** HABS foundation platform is about 166 ft / 50.6 m, while the current OSM oriented envelope is 56.08 m. Use the current footprint envelope.
- **Anchor:** OSM whole-polygon centroid is not exactly the tower center. Use the supplied tower-centered anchor and report the measured centroid offset.
- **Bay count:** facade bays have been altered and photographs include occlusions. The chosen count is an art-directed abstraction derived from straight-on imagery, not a survey claim.
- **East elevation:** modern ferry facilities obscure significant portions. The asset uses historic description plus unobscured upper-level photography and deliberately excludes later ferry structures.
