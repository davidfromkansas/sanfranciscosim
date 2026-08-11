# San Francisco City Hall reference dossier

## Research method

This dossier separates published dimensions from visual inference. The model is based on institutional and engineering descriptions, OpenStreetMap geometry measured in a local tangent plane, public aerial imagery, historic drawings, and multiple geolocated photographs. No source photograph is embedded in this repository.

## Sources

- [City and County of San Francisco — City Hall history](https://www.sfcityhallevents.org/history/): owner-operated overview of the 1915 building, architects Bakewell & Brown, Beaux-Arts character, and the dome's civic prominence.
- [National Park Service — San Francisco Civic Center National Historic Landmark](https://www.nps.gov/places/san-francisco-civic-center.htm): institutional context for the Civic Center ensemble and the City Hall axis facing the plaza.
- [National Register of Historic Places registration form, San Francisco Civic Center](https://npgallery.nps.gov/GetAsset/0d5fb50d-f9b1-46f5-ad50-9e58ab67a860): architectural descriptions of the principal facades and the axial Beaux-Arts composition.
- [Wiss, Janney, Elstner Associates — Investigation of San Francisco City Hall Dome](https://www.wje.com/assets/pdfs/articles/Investigation-of-San-Francisco-City-Hall-Dome.pdf): engineering dimensions and construction: approximately 92 m × 122 m base, three-story drum, exterior Doric granite colonnade, approximately 15 m drum height, approximately 34 m dome diameter, and structural/ornamental dome details.
- [Wikipedia — San Francisco City Hall](https://en.wikipedia.org/wiki/San_Francisco_City_Hall): secondary cross-check for published plan dimensions (390 ft × 273 ft), 307 ft 6 in / 93.73 m architectural height, and general building history. Used only where consistent with stronger sources.
- [OpenStreetMap relation 7261820](https://www.openstreetmap.org/relation/7261820): georeferenced building outline. The relation was measured locally rather than copied as an artistic plan.
- [OpenStreetMap Overpass API](https://overpass-api.de/): queried relation geometry and nearby named streets to verify location and orientation.
- [Wikimedia Commons — Category: San Francisco City Hall](https://commons.wikimedia.org/wiki/Category:San_Francisco_City_Hall): multiple independently authored, geolocated photographs covering east and west facades, oblique sides, dome details, day/night appearance, and aerial views. Especially useful files include [aerial view](https://commons.wikimedia.org/wiki/File:San_Francisco_City_Hall,_aerial_shot.jpg), [east/front elevation](https://commons.wikimedia.org/wiki/File:San_Francisco_City_Hall_(front).jpg), [west elevation from the Pioneer Monument](https://commons.wikimedia.org/wiki/File:2017_City_Hall_from_Pioneer_Monument.jpg), [dome detail](https://commons.wikimedia.org/wiki/File:San_Francisco_City_Hall_dome.jpg), and [historic Civic Center overview](https://commons.wikimedia.org/wiki/File:General_View_of_Civic_Center_and_New_City_Hall_(Engineering_News-Record,_vol_75_no_26_p_1222_fig_2).jpg).
- [Esri World Imagery](https://www.arcgis.com/home/item.html?id=10df2279f9684e4a9f6a7f08febac2a9): current overhead cross-check for the rectangular perimeter, two inner courts, roof bands, dome base, central east/west projections, and corner roof structures.

## Verified location, dimensions, and orientation

- **Requested WGS84 anchor:** `[-122.4192838, 37.7793223]`. It falls within the central building/dome footprint and is appropriate as the placement anchor.
- **Architectural height:** **93.73 m** (307 ft 6 in). This is the target asset height.
- **Published plan:** **390 ft × 273 ft**, approximately **118.9 m × 83.2 m**.
- **Engineering base:** approximately **122 m × 92 m**.
- **Measured OSM relation:** approximately **126.6 m north-south × 97.8 m east-west**, about **11,033 m²**. This outline includes facade projections, porticos, and irregular perimeter details, so it is expected to exceed the simpler published plan rectangle.
- **Dome:** approximately **33–34 m diameter**; the exterior drum is approximately **15 m high**.
- **World orientation:** the long building axis is nearly north-south. A least-squares/edge measurement of the OSM outline gives a long-axis heading of approximately **350.4° / 170.4° true**, i.e. about **9.6° west of true north**. The authored asset therefore keeps Blender `+X = east`, `+Y = true north`, `+Z = up` and rotates the building mass about `-9.6°` from the `+Y` axis.
- **Ceremonial front:** **east**, toward Polk Street and Civic Center Plaza. It carries the dominant pedimented portico and grand entrance steps.

### Dimension decision for modeling

The sources describe different boundaries, not necessarily contradictory structures. The 390 ft × 273 ft figure is a simple published plan; WJE describes an engineering base; the OSM outline follows projections and perimeter articulation. The model will use an approximately **98 m × 127 m overall architectural envelope**, preserving the OSM aspect ratio and portico projections, while using a simpler main block inside that envelope. The height remains exactly 93.73 m. This favors correct map fit and silhouette without reproducing every plan jog.

## Elevation and roof observations

### East — Polk Street / Civic Center Plaza

- The primary, rigorously symmetrical civic front.
- A tall central projection has a broad triangular pediment, giant-order columns, three tall upper openings, three arched entrance portals, and a wide staircase/terrace.
- Long wings continue north and south with repeated two-story column/pilaster rhythm and strong horizontal cornice bands.
- Smaller pedimented end pavilions terminate the facade.
- The drum and dome align directly above the central portico and dominate the full composition.

### West — Van Ness Avenue / Memorial Court

- Also formal and axial, but the central portico reads as a more compact garden/court-facing composition.
- A pedimented giant-order center with tall arched openings sits between projecting corner/side pavilions.
- The west entrance is framed by Memorial Court rather than the broad Civic Center Plaza approach.
- The dome remains centered and highly visible; the west silhouette must therefore be designed, not treated as a blank rear wall.

### North — McAllister Street

- A long secondary elevation with consistent classical bay rhythm and a strong rusticated base/cornice stack.
- The center and ends project slightly; the dome is visible behind the roof line rather than sitting directly on the facade.
- Repetition is more important than individual window accuracy: paired vertical bays, shallow pilasters, and a clear terminal pavilion establish identity.

### South — Grove Street

- Broadly mirrors the north side in mass, bay rhythm, projecting ends, and roof profile.
- The central zone and end pavilions create shallow depth changes along the long wall.
- The dome rises behind the perimeter roof, with central roof structures helping bridge the scale from the low block to the dome.

### Above / roof

- The perimeter reads as a large rectangular ring around two substantial inner courts, interrupted by the central dome/cross-axis mass.
- A pale blue-green/oxidized-metal roof band traces much of the perimeter behind the parapet.
- Four lower roof/pavilion masses cluster around the central dome base and make the transition to the long wings.
- The dome has a strongly ribbed, segmented surface; gold trim follows the ribs and highlights ornamental medallions.
- The lantern is multi-stage and open, with a dark tapering cap/spire and gold accents.
- The courts and roof setbacks are major aerial recognition features even when rooftop equipment is omitted.

### Day and night

- By day the building is restrained cream/white stone with dark blue-gray openings; the dome reads as dark gray metal with warm gold ribs and ornaments.
- At night the stone facade and dome are externally floodlit. The building does not read as a glass-emissive landmark, so this asset should not misuse `_Glow`; graphic dark windows remain non-emissive.

## Strongest recognition cues

1. The oversized ribbed dark-metal dome with gold ribs and an elaborate tiered lantern/spire.
2. The symmetrical east facade: giant central pedimented portico, classical columns, three entrance arches, and a broad staircase.
3. The long, low cream Beaux-Arts perimeter block with repeated giant-order facade rhythm and pedimented end pavilions.
4. The cylindrical colonnaded/windowed drum below the dome, clearly distinct from the square building base.
5. The designed aerial composition: rectangular ring, inner courts, perimeter roof band, and four lower pavilion masses around the dome.

## Preserve

- True-world orientation and rectangular north-south footprint.
- Exact 93.73 m target height and plausible 98 m × 127 m overall envelope.
- Strong east/west symmetry and credible north/south secondary elevations.
- Grand east staircase and low balustraded terrace.
- Layered rusticated base, column zone, entablature/cornice, and parapet.
- Major portico columns, triangular pediments, dark graphical openings, and end pavilions.
- Drum colonnade/opening rhythm, 16-part dome impression, gold ribs, lantern, and spire.
- Inner-court/roof-ring read from the high three-quarter camera.

## Simplify

- Reduce dozens of facade bays to broad repeated rhythms while retaining proportions and hierarchy.
- Represent sculpture, garlands, capitals, balusters, and gold ornament as chunky geometric motifs rather than literal carving.
- Omit rooftop mechanical equipment, flags, lamps, statuary, fences, landscaping, and all neighboring/plaza objects.
- Use a small flat-color `Toy_*` material set with no image textures or transparency.
- Use shallow inset or applied dark window shapes rather than modeled glazing interiors.
- Keep columns low-sided and pediments bevel-friendly; spend triangles on dome silhouette, porticos, and aerial roof design.

## Uncertainties and conflicts

- **Footprint dimensions:** published, engineering, and OSM values use different boundary definitions. The OSM envelope is selected for map fit; its detailed jogs will be simplified.
- **Anchor meaning:** the supplied coordinate is accepted as the landmark placement anchor, but it is not asserted to be a surveyed dome center. Export origin remains the modeled base center; later integration may position it at the verified anchor per the manifest contract.
- **Heading:** the approximately 9.6° rotation is measured from open geodata and street/building edges; minor survey/generalization error is possible. It is materially better than assuming a cardinally aligned block.
- **Dome segmentation:** engineering descriptions and photographs support a 16-part structural/visual rhythm. The miniature may use 16 principal ribs while simplifying secondary ornaments.
- **Facade bay counts and court geometry:** photographs and aerial imagery establish overall rhythm and massing, but not every hidden court wall. Inner walls will be architecturally consistent rather than treated as survey-grade reconstruction.
- **Color:** photographs vary with weather and floodlighting. The asset follows the project palette: restrained cream/stone architecture, dark blue-gray windows/roof, and muted warm gold accents.
