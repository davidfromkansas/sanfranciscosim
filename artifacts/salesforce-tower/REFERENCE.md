# Salesforce Tower reference dossier

Research checked 2026-08-10. Dimensions and history below distinguish published facts from visual inference. No third-party reference imagery is committed with the model; the model and review renders are original.

## Verified facts

| Item | Value | Confidence / source |
|---|---:|---|
| Address | 415 Mission Street, San Francisco | Architect and building-owner pages |
| WGS84 anchor | **-122.3969270512, 37.7897756184** | OpenStreetMap building centroid; suitable as the future manifest anchor |
| Architectural height | **326 m / 1,070 ft** | CTBUH / Skyscraper Center and architect page |
| Roof / occupied-tower height | approximately **296 m** | CTBUH data; crown accounts for roughly the upper 30 m |
| Floors | 61 | Architect, owner, and CTBUH |
| Completion | 2018 | Architect / CTBUH |
| Architect | Pelli Clarke Pelli Architects | Architect page |
| Published site area | 50,514 ft² / 4,692.9 m² | Architect / property descriptions |
| Mapped tower footprint | approximately 2,656 m²; roughly 54.1 × 55.3 m facade-aligned | OpenStreetMap polygon; used as the shaft footprint, not the full site |
| Crown lighting | `Day for Night`, a six-floor LED installation using about 11,000 LEDs | Jim Campbell and building-owner art pages |

The overall-height conflict is mostly definitional. CTBUH and the architect publish 1,070 ft / 326 m architectural height; some general sources round the tower to 1,070 ft while roof-height datasets describe the occupied roof around 296 m. The asset preserves 326 m overall and treats the upper portion as the crown/topper.

## Source list and what each establishes

- [Pelli Clarke & Partners — Salesforce Tower](https://pcparch.com/work/salesforce-tower): architect, address, 1,070 ft height, completion, sustainability, elliptical/rounded tapered form, exterior sunshades, and the relationship to the transit center.
- [CTBUH / Skyscraper Center — building 290](https://www.skyscrapercenter.com/building/building/290): architectural height, roof-height distinction, floor count, construction dates, structural use, and authoritative tall-building nomenclature.
- [Salesforce Tower](https://salesforcetower.com/): owner information, address, tower/public-space context, and project identity.
- [Salesforce Tower — Artwork](https://salesforcetower.com/artwork/): the crown as a media surface and the official description of `Day for Night`.
- [Jim Campbell — Day for Night](https://www.jimcampbell.tv/portfolio/day-for-night): six upper floors, roughly 11,000 LEDs, imagery sourced from cameras around San Francisco, and day/night behavior.
- [Architectural Record — Salesforce Tower by Pelli Clarke Pelli](https://www.architecturalrecord.com/articles/13511-salesforce-tower-by-pelli-clarke-pelli): critical architectural description of the taper, rounded plan, curtain wall, exterior shading and ground condition.
- [OpenStreetMap](https://www.openstreetmap.org/way/119890395): geospatial anchor, footprint, street-grid orientation and mapped building tags. The polygon was measured locally for the model plan.
- [Wikimedia Commons — Salesforce Tower category](https://commons.wikimedia.org/wiki/Category:Salesforce_Tower): geolocated day, street-level, distant and roof/aerial photography used to cross-check all elevations. Representative pages include [street level](https://commons.wikimedia.org/wiki/File:Salesforce_Tower_Street_Level.png), [facing south](https://commons.wikimedia.org/wiki/File:Salesforce_tower_facing_south.jpg), [from Salesforce Park](https://commons.wikimedia.org/wiki/File:Salesforce_Tower_from_Salesforce_Park.jpg), [Sacramento and Davis](https://commons.wikimedia.org/wiki/File:Salesforce_Tower_from_Sacramento_and_Davis_Street_2021.jpg), and [2021 street canyon view](https://commons.wikimedia.org/wiki/File:Salesforce_Tower_2021.jpg).

## Orientation

OpenStreetMap geometry places the tower on the SoMa grid. The mapped facade axes are about **45.9° / 135.9° clockwise from true north**. The model therefore rotates its rounded-square plan **44.13° around +Z**, with Blender `+Y` treated as true north and `+X` as east. Because the tower is nearly four-way symmetric and the asset contract requires one canonical front, the simplified entrance/cloud-sign cue is placed on Blender **`-Y`**. This preserves the measured shell orientation while making front direction mechanically unambiguous; it should not be used as a survey of the real entrance's exact face position.

## Directional observations

### North

- Read from the financial-district / Market Street side.
- Rounded corners make the plan appear softer than a rectangular office slab.
- Dense pale horizontal sunshade lines dominate over the blue glass.
- The shaft narrows continuously, with the strongest curvature toward the upper third.
- The crown reads as a white, partially open/perforated veil rather than a separate antenna.

### East

- Viewed from the waterfront / Embarcadero direction, the full-height taper is especially clear against the skyline.
- The rounded corner and even facade module make the elevation visually similar to the north side.
- Lower floors are often obscured by the transit center; that context is deliberately excluded from the GLB.
- The upper facade/crown is brighter and more opaque than the occupied shaft in daytime.

### South

- The southern view from SoMa shows the broad shaft and strong rounded shoulders.
- The facade rhythm remains continuous: dark blue-gray glazing crossed by light projecting horizontal shades.
- No large side annex or setback changes the main silhouette.
- Ground-level entries and mullions are simplified into one recessed lobby volume and chunky perimeter piers.

### West

- The west / downtown-canyon view confirms the same rounded-square plan and continuous taper.
- A few broader pale vertical zones are visible in photos, but they are secondary to the horizontal floor/sunshade rhythm and are omitted at city scale.
- The north-west / Mission Street quadrant informs the ground-level massing research; the miniature moves its one abstract entrance cue to canonical `-Y` to satisfy the asset front contract.

### Top / crown

- Aerial photography shows an **open roof**, not a sealed dome: plant decks, two long central mechanical clusters, circulation/walkway geometry, perimeter rails/screens and BMU equipment.
- The white crown is a perforated exterior screen continuing above and around the upper floors. The real perforation is fine and layered; the miniature reduces it to broad separated hoops that expose the dark roof plant below.
- Night imagery is displayed across the upper six LED floors, producing a luminous crown. Only the crown/upper-light materials use `_Glow` in the asset.

## Ground level

- The tower rises from a transparent, double-height lobby condition with pale structural/mullion elements and projecting canopies.
- The transit center, Salesforce Park, plaza landscaping, roads, neighboring towers and people are not physical parts of the exported tower and are excluded.
- The model includes only a recessed lobby, perimeter piers, one oversized entrance canopy, and an abstract blue cloud sign for one-second recognition.

## Day and night appearance

- **Day:** cool blue-gray curtain wall; pale warm-white mullions and perforated sunshades; white crown against the sky.
- **Night:** most shaft glass remains non-emissive; the upper crown/media zone becomes the identity feature. The Campbell artwork changes with captured city imagery, so no literal image is baked into the asset. Flat `Toy_white_Glow` marks only the media/crown surfaces and `Toy_red_Glow` marks the small aviation beacon.

## Strongest recognition cues

1. **Very tall, continuously tapering rounded-square silhouette** with a compact base and strongly softened corners.
2. **Dense pale horizontal sunshade rhythm** wrapped over a blue-gray glass curtain wall.
3. **White perforated crown / topper** continuing the taper above the occupied roof.
4. **Luminous media crown at night**, represented without textures by contract-compliant glow materials.
5. **Blue Salesforce cloud at the entrance**, selectively enlarged as a semantic identity cue.

## Translation to the SF-SIM miniature style

### Preserved

- Real 326 m overall height and plausible ~55 m footprint.
- SoMa-grid orientation and base-center origin.
- Rounded-square plan, continuous taper and compact high-rise proportion.
- Broad facade rhythm and projecting sunshade relief.
- Hollow crown silhouette, visible roof plant and nighttime crown designation.
- Glazed double-height base and entrance canopy.

### Simplified / exaggerated

- Roughly 61 real floor lines are grouped into about 30 chunky readable bands; each stands farther proud than scale accuracy would permit.
- Fine perforated aluminum mesh is reduced to six broad open crown hoops.
- Thousands of LEDs become one flat `_Glow` material; no texture, animation or transparency.
- Roof systems become four plant blocks, a ring walkway/rail and a compact BMU.
- Ground-level complexity becomes eight piers, one lobby shell, one canopy and a simple three-lobed cloud sign.
- Material response is matte painted-resin rather than photoreal glass/metal.

## Uncertainties and decisions

- Public sources provide consistent overall height but do not expose a simple surveyed shaft cross-section. The footprint comes from OSM and the changing corner radius/taper comes from multi-direction photography.
- The exact face that should map to a single canonical "front" is ambiguous because the tower is nearly symmetric. The measured shell keeps its true-north orientation, while the simplified identity entrance is deliberately placed on Blender `-Y` to satisfy the technical contract; true-north review cameras remain independent.
- The topper is variously described as nine crown floors and as an LED artwork spanning six floors. The model reserves the upper six-floor-equivalent zone for glow while treating the larger upper enclosure as the architectural crown.
- The real roof photo shows more plant complexity than is legible in SF-SIM. The chosen roof is intentionally a designed abstraction, not a plan reproduction.
