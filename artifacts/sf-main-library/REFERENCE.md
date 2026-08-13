# San Francisco Main Public Library — reference dossier

Research behind `sf-main-library.glb`. Compiled 13 August 2026. The plan
(`docs/asset-plans/sf-main-library.md`) was the starting point; everything below
was re-verified against primary sources before modelling, and the corrections
this pass made are listed in §8 and repeated in `REPORT.md`.

100 Larkin Street, San Francisco CA 94102 — Marshall Square, the full block
bounded by **Larkin (west), Fulton (north), Hyde (east), Grove (south)**.

## 1. Sources and what each establishes

| Source | Establishes |
|---|---|
| [OSM way/24446086](https://www.openstreetmap.org/way/24446086) | footprint geometry (9 nodes, `check_date=2025-04-10`), address, `building=civic`, `building:levels=5`, and the misleading `height=46` / `ele=18` pair |
| [DataSF Building Footprints `ynuv-fyni`](https://data.sfgov.org/resource/ynuv-fyni.json), `area_id=186`, `mblr=SF0354001` | 2010 LiDAR: `hgt_maxcm` 2898, `hgt_mediancm` 2402, `median_1st_m` 42.31, `peak_1st_m` 46.91, ground median 18.34 m NAVD88, 24,696 half-metre cells (≈ 6,174 m2) |
| [SFPL — Architecture of the Main Library](https://sfpl.org/locations/main-library/about/architecture-main-library) | Sierra White granite from the same quarry as the other Civic Center buildings; **Grove and Hyde "have a more contemporary feel, compatible with the commercial activity on Market Street"**; skylight over the five-storey atrium; 142 base isolators |
| [SFPL — Other facts about the building](https://sfpl.org/locations/main-library/about/other-facts-about-building) | 376,000 sq ft; six floors above ground, one below; groundbreaking 1992, construction from 15 March 1993, complete 1995, opened 18 April 1996; $104.5 M construction on a $109.5 M 1988 bond; Marshall Square bounded by Larkin/Fulton/Hyde/Grove |
| [Pei Cobb Freed & Partners project page](https://www.pcf-p.com/projects/san-francisco-main-public-library/) | full-block 2.65-acre site; "Fronting on the Civic Center with two symmetrical facades, the exterior echoes in a modernist way the materials and massing of the neighboring Beaux-Arts institutions"; 60-ft-diameter five-storey atrium; roof garden in the programme; 377,000 sq ft gross |
| [Wikipedia — Main Library (San Francisco)](https://en.wikipedia.org/wiki/Main_Library_(San_Francisco)) | James Ingo Freed (PCF&P) with Cathy Simon (SMWM); opening date; floor count; the atrium/shelving controversy |
| [Commons: exterior from Larkin Street](https://commons.wikimedia.org/wiki/File:San_Francisco_Public_Library_-_Main_Branch,_exterior,_from_Larkin_Street.jpg) (CC BY 2.0) | the hero west elevation: giant order of flat pilasters, diamond-lattice glazing, incised SAN FRANCISCO PUBLIC LIBRARY frieze over three double doors, attic of small squares, cresting studs along the parapet |
| [Commons: SFPL Main Library Full Exterior](https://commons.wikimedia.org/wiki/File:SFPL_Main_Library_Full_Exterior.jpg) (CC BY-SA) | the whole west end from Civic Center Plaza — the raised centre pavilion against lower flanks, and the glazed skylight sheds standing clear above the parapet |
| [Commons: exterior from Grove Street](https://commons.wikimedia.org/wiki/File:San_Francisco_Public_Library_-_Main_Branch,_exterior,_from_Grove_Street.jpg) (CC BY 2.0) | the south modern face: flat granite panel grid, scattered punched windows, one dark spandrel band, banded base |
| [Commons: from Grove & Hyde](https://commons.wikimedia.org/wiki/File:SFPL_Main_Branch_Exterior_from_Grove_%26_Hyde_St.jpg) (CC BY-SA) | the tall square granite corner pier at Grove/Hyde and the stepped modern massing |
| [Commons: from Market Street](https://commons.wikimedia.org/wiki/File:San_Francisco_Public_Library_-_Main_Branch,_exterior,_from_Market_Street.jpg) (CC BY 2.0) | how the corner pier reads on the skyline from the south-east |
| Esri World Imagery nadir aerial, rectified into the street-grid frame | the roof layout: oculus, pyramid, two skylight sheds, mechanical enclosure, pale north strip, linear slot, roof terrace |

No copyrighted imagery is committed here; the links above are the record.

## 2. Verified dimensions and location

Footprint measured from the OSM way via the API, reprojected with the repo's
local tangent projection (LON0 −122.4375, LAT0 37.77) and reduced to a
minimum-area oriented bounding box.

| Quantity | Value | How |
|---|---|---|
| Polygon area | 6,027 m2 | shoelace over the reprojected ring (measured) |
| Oriented bounding box | **106.42 x 56.88 m** | min-area OBB (measured) |
| Squareness | every corner within 0.25 m of the OBB | the plan is a rectangle; no outline machinery needed |
| Long-axis bearing | **80.94 deg** (9.06 deg north of due east) | derived from the OBB (measured) |
| OBB centre | **−122.4157709, 37.7791281** | derived (measured) — the manifest anchor |
| Polygon centroid | −122.4157712, 37.7791276 | derived — 0.07 m from the OBB centre, so the two candidate anchors coincide |
| Crest above grade | **28.98 m** | DataSF `hgt_maxcm` = 2898 |
| Main roof plane | **24.02 m** | DataSF `hgt_mediancm` = 2402 |
| DataSF footprint area cross-check | ≈ 6,174 m2 (24,696 half-metre cells) | within 2.5% of the OSM polygon — the two sources agree the polygon is the whole building |

### The height trap

OSM and Overture both carry `height=46` for this footprint. **It is not a
height.** It is the NAVD88 roof *elevation*, 153.78 ft = 46.87 m, which appears
verbatim as `p2010_zmaxn88ft` in the DataSF LiDAR record. The same tag also
carries `ele=18`, the site grade, and 46.87 − 18.34 = 28.5 m, which is the real
building. The Asian Art Museum one block north carries the *identical* `height=46`
for the identical reason (see `docs/asset-plans/asian-art-museum.md` §2.3); this
tag has now caught two adjacent Civic Center blocks. The baked city currently
renders this building 46 m tall because of it, which is why the integration
exclusion matters as much as the asset.

## 3. Orientation

The long axis runs east–west at bearing 80.94 deg. Authored axis-aligned in a
grid frame (E from the Larkin face, S from the Fulton face), then rotated
**+9.06 deg about Z** with Blender `+Y` = true north, `+X` = east.

The ceremonial entrance faces **west** onto Larkin, across Civic Center Plaza
from City Hall. The asset contract's "front faces −Y" cannot be honoured
literally; real-world orientation wins (AGENTS rule 5) because `placeGeneric()`
in `app/src/assets.js` scales and positions but never rotates.

## 4. What each side shows

**West (Larkin), 57 m — the hero.** Pale Sierra White granite in a large ashlar
grid. A raised centre pavilion carries a giant order of flat, slightly rounded
pilasters on a plinth, tall windows between them filled with a diagonal
diamond-lattice glazing. Below the order an incised frieze — SAN FRANCISCO PUBLIC
LIBRARY — over three sets of double doors on a shallow flight of steps, flanked by
dark lamp standards. Above: a plain entablature, an attic of small square punched
windows, a flat parapet finished with a **cresting of small vertical studs**. The
flanking bays north and south of the pavilion are lower and plainer with the same
tall windows.

**North (Fulton), 106 m.** The second Civic Center face, on axis with the Old Main
across Fulton Mall. Same granite, same cornice datum, same cresting, a longer and
quieter pilaster-and-window rhythm, no raised centre.

**South (Grove), 106 m — the modern face.** Same stone, opposite grammar: a flat
granite panel grid with no order and no projecting cornice, **scattered punched
rectangular windows** placed asymmetrically, one continuous **dark grey spandrel
band** at roughly the third-floor line, and a banded granite base about 2 m tall.

**East (Hyde), 57 m — the modern face's front.** Dominated by the **tall square
granite corner pier at Grove & Hyde**, which rises above the neighbouring parapets
and carries the same dark bands and sparse punched windows.

**Top — the design event.** Inside a pale parapet and a pale raised strip along
the Fulton edge (carrying the rooftop plant): a dark low-slope deck holding the
**circular atrium oculus**, a **glazed pyramid set at 45 deg to the block** just
west of it, **two big pitched glazed skylight sheds** over the eastern half set at
a shallow angle to each other, a **mechanical enclosure with three round units**,
a long **linear skylight slot** near the Larkin edge, and a small **roof garden**
at the south-west.

Roof feature positions were read off a nadir aerial rectified into the grid frame
(so E/S coordinates come off the image directly). The oculus measures ≈ 22 m
across the outer glazing, which brackets the published 60 ft (18.3 m) atrium well.

## 5. Recognition cues (ranked)

1. The circular oculus with the pyramid beside it — from the app's camera this is
   the building, and nothing else in the city looks like it
2. The two-grammar facade: ordered pilastered granite on Larkin and Fulton, flat
   punched granite with dark bands on Grove and Hyde
3. The raised Larkin centre pavilion with its frieze over three doors
4. The tall square corner pier at Grove & Hyde
5. The cresting of studs along the classical parapets
6. Two big pitched glazed sheds on the eastern roof

## 6. Preserved

- The 106 x 57 m proportion and the 9.06 deg grid rotation
- **The classical/modern split**, which is the only thing separating this asset
  from the Asian Art Museum 90 m north: same size, same stone, same grid. In the
  model it lives in three places at once — the parapet projects 0.7 m on the north
  and west and is flush and 0.4 m lower on the south and east; the order exists
  only on the north and west; the cresting exists only on the north and west.
- The roof as a composition rather than a lid
- The two places the silhouette breaks: the raised Larkin pavilion and the corner pier

## 7. Simplified

- The giant order becomes 6 pilasters on Larkin and 14 pilaster strips on Fulton
- The diamond-lattice glazing becomes a flat `Toy_glass` panel — the pattern is a
  texture in reality and must not become geometry
- The incised inscription becomes one proud `Toy_trim` course, not letterforms
- The parapet cresting becomes 48 + 26 small studs at 2.2 m pitch, reading as a
  dotted line from the air rather than the real ~200 pins
- The scattered modern windows become 18 on Grove and 7 on Hyde, in a deliberately
  irregular but designed arrangement, plus one continuous dark spandrel band
- The oculus becomes a glazed drum and a faceted cone; the spiral stair inside is
  **dropped**, because the toy's glass is an opaque flat colour and nothing behind
  it would ever be seen
- The two sheds keep their splayed pair reading but are sized and placed to clear
  the oculus and the 27 m corner pier

## 8. Corrections this pass made to the plan

1. **The crest is the shed ridge, not the pyramid apex.** The plan's §2.8 put the
   28.98 m crest on the pyramid. The Civic Center Plaza photograph shows the
   glazed sheds standing clear above the parapet as the tallest things on the
   roof, and they are the larger structures, so the crest moved to shed 0's ridge.
   The pyramid apex sits at 28.20 m. This remains *inferred* from photography, not
   from drawings — see §9.
2. **The roof glazing is `Toy_glassl_Glow` (#6f95b8), not `Toy_white_Glow`.** The
   plan's §2.9 chose a near-white so the skylights would read as frosted glazing.
   At diorama scale a white cone on a white drum rendered as a blank disc. Pale
   blue glass reads as a skylight by day and as the lit atrium by night, which is
   what it is, and it separates the glazed events from the trim.
3. **Shed geometry and placement were re-solved.** The plan's §2.8 sizes
   (30 x 20 m and 26 x 17 m at 52 deg) overhang the south parapet and bury a ridge
   inside the corner pier. Solved numerically against the deck, the oculus circle
   and the pier footprint; the shipped values are 22 x 12 m at 38 deg and
   17 x 9 m at 34 deg.
4. **The mechanical enclosure moved** from the Grove/Hyde corner (where it sat
   inside the 27 m corner pier) to the deck north of the pier.
5. **The footprint is a rectangle.** The plan did not say so; the reprojected OSM
   ring is square to within 0.25 m, so none of the sibling assets' outline-offset
   machinery is used.

## 9. Uncertainties and conflicting evidence

- **Which roof object makes the 28.98 m crest** is *inferred* from a nadir aerial
  and one oblique photograph. The sheds, the pyramid and the mechanical enclosure
  are all plausible; the sheds were chosen for the reason in §8.1. If drawings
  ever surface and say otherwise, the fix is one constant.
- **The pale strip along the Fulton edge.** The rectified aerial shows the
  northern ~7 m of the footprint as a darker, apparently lower band; it could be a
  set-back lower roof or simply the Fulton Mall tree allée in shadow crossing the
  parapet line. The model treats the envelope as one height and the strip as a
  raised pale roof band, which is what the imagery supports at diorama scale.
- **The Grove and Hyde window arrangement** was read from photography, not
  drawings. It is *inferred* and chosen for rhythm, not census.
- **The pyramid's plan size and the sheds' pitch** are scaled off the nadir
  aerial — *estimated*, ±15%.
- Site grade falls across the block (DataSF ground 13.73–19.50 m NAVD88, median
  18.34); the 13.73 minimum is a below-grade artefact. The app seats assets on
  sampled terrain at a single anchor, so the model's base is level. Accepted; no
  stepped base is modelled.
- PCF&P give 377,000 sq ft gross where SFPL give 376,000. Immaterial here.
