# Bill Graham Civic Auditorium — reference dossier

99 Grove Street. Built 1913–15 as the San Francisco Exposition Auditorium for the
Panama–Pacific International Exposition. Everything below was gathered and
re-verified for this build; where the plan
(`docs/asset-plans/bill-graham-civic-auditorium.md`) and this dossier disagree, this
dossier wins, and where the build disagrees with this dossier, `REPORT.md` wins.

## Sources and what each establishes

| Source | Establishes |
|---|---|
| OSM way/25759141 via Overpass (`amenity=theatre`, `building=civic`, `height=37 m`, `wikidata=Q4909197`, `check_date=2025-11-22`) | The 45-node footprint polygon; the surveyed crest height |
| DataSF `ynuv-fyni` (2010 LiDAR-derived heights), building `SF0812001` | `hgt_median` 22.99 m, `hgt_mean` 24.26 m, **`hgt_max` 36.98 m** over 37,661 cells; `gnd_min` 16.37 m NAVD88. Confirms the OSM tag to 2 cm and gives the main roof deck |
| **Esri World Imagery z19 (~0.24 m/px), rotated to the building axis and measured photometrically** | The dome: a regular octagon **58.6 m flat-to-flat**, centred ~8 m south of the building centre, dark against a bright membrane deck; the positions of the roof plant |
| Wikipedia / Wikidata Q4909197 | Architects (John Galen Howard, Frederick H. Meyer, John W. Reid Jr.), 1915 opening, 8,500 capacity, Brooks Hall (1958) beneath the plaza to the north, the renovation history |
| noehill.com, SF Point of Historical Interest entry | Four storeys on a steel frame; grey granite to the main facade, brick to sides and rear; Beaux-Arts with French and Italian Renaissance elements |
| Wikimedia Commons — HABS `CAL,38-SANFRA,71-C-1` corner view; `Exposition Auditorium (9615942845).jpg` (near-frontal); `Bill Graham Civic Auditorium 1 2018-09-19.jpg` (night close-up of three bays); `… from Larkin and Grove St` and `… from NE` | Bay count, arch geometry, the paired columns and their entablature blocks, the frieze with wreath medallions, the end pavilions and their cartouches, the parapet sculpture and flagpoles, the marquee and its bulb band |

## Verified dimensions and location

| | |
|---|---|
| Footprint (min-area oriented bbox) | **127.95 x 78.64 m**, polygon area 9,314 m² (45 nodes) |
| Long-axis bearing | **80.69° cw from true north** |
| OBB centre WGS84 | **−122.4173272, 37.7780592** |
| Main roof deck | ~23.0 m (LiDAR median 22.99 m) |
| **Crest (target height)** | **37.0 m** (OSM 37 m; LiDAR `hgt_max` 36.98 m) |
| Dome | regular octagon, 58.6 m flat-to-flat (circumradius 31.7 m), centred ~7 m south of the building centre |
| Storeys | four |

Heights read off `Exposition Auditorium (9615942845).jpg`, scaled against the 25.8 m
parapet (≈10.5 px/m), and reconciled with the two measured anchors:

| Line | m |
|---|---|
| Rusticated base top | 5.0 |
| Marquee canopy | 4.6 – 5.4 |
| Arcade sill | 7.6 |
| Arch springing | 14.8 |
| Arch crest | 18.3 |
| Architrave / frieze with medallions | 20.0 – 22.9 |
| Projecting cornice | 22.9 – 24.3 |
| Arcade parapet | 25.8 |
| End-pavilion attic crest | ~29.8 |
| Roof deck | 23.0 |
| **Dome apex** | **37.0** |

## The bay count — three, not seven

Counted directly on the near-frontal `Exposition Auditorium` photograph and confirmed
on the 2018 night close-up: the central range carries **three** giant round-arched
windows, ~11 m wide at ~17 m pitch, separated by paired engaged columns on pedestals
carrying projecting entablature blocks. This is a low count for a 128 m frontage and
looks wrong beside the War Memorial Opera House's seven-bay colonnade, but it is
correct — the Grove Street front is mostly wall, and that is precisely what makes the
three arches monumental. The frontage divides roughly as: 24 m pavilion, 14 m
pilastered link bay, 52 m arcade, 14 m link bay, 24 m pavilion.

## What each side shows (observations)

- **North — Grove Street, 128 m, the front, facing Civic Center Plaza and City Hall.**
  Rusticated granite base; a continuous flat **marquee canopy** at ~4.6 m running the
  length of the arcade, with a band of bulbs along its soffit; above it the three
  giant arched windows in fine gridded glazing; between them paired columns; above,
  an architrave and frieze carrying the incised name and circular wreath medallions
  over each pier; a modillioned cornice; a parapet with sculptural groups and a row of
  tall flagpoles. Two end pavilions flank the arcade, rising past the arcade parapet
  and each crowned by a large oval cartouche flanked by figures.
- **West — Larkin Street.** The pavilion turns the corner in the same granite:
  pedimented upper windows, balustraded balconies on consoles, a heavy cornice, a tall
  attic. Behind it the great hall's flank is a long, much plainer wall with sparse
  punched openings.
- **East — Polk Street.** Mirrors the west.
- **South — rear.** The plainest elevation: a flat wall, service doors and loading.
- **Above.** A bright flat membrane deck inside the parapet, with the **dark octagonal
  dome** filling the southern two-thirds and a small circular lantern at its apex;
  compact clusters of plant on the wide deck outside the octagon's corners.

## Recognition cues (ranked)

1. The dark octagonal dome, ~58 m across — unmistakable from above and unique in the
   city. It is also the reason this building is worth an asset.
2. Three giant arched windows, monumentally spaced, over a granite front.
3. The end pavilions with their oval cartouches, taller than the range between them.
4. The unbroken marquee canopy at street level.
5. The long low horizontality: 128 m of front, only ~26 m to the arcade parapet.

## Features to preserve / simplify

**Preserve:** the dome's octagon, its span, its offset south of centre, and its dark
value against a light deck; three arches at their real pitch; the paired columns and
their cap blocks; the frieze medallions; the two pavilions and their cartouches; the
marquee; the granite-vs-flank value step.

**Simplify:** the mullion grid inside each arch (one flat `Toy_glass` pane); column
fluting and capitals (a pair of plain shafts with a cap block); the modillion teeth
(one clean cornice slab); the incised inscription; the pavilion balcony balustrades;
the figure sculpture (chunky pedestal blocks in its place); the row of separate street
openings under the marquee (one continuous dark recess with a door band on it).

**Exaggerate** (style bible §9): the dome's facet crispness, the marquee's projection,
and the depth of the arch reveals.

**Omit: the flagpoles.** They are a genuine identity cue, but they rise to ~39 m —
above the dome — so keeping them would make the model's crest something other than the
measured 37.0 m, and at ~0.1 m thick they are sub-pixel at the app's camera and would
read as noise rather than as flags. If a future revision wants them, the target height
has to be re-decided first.

## Night appearance

The real building floodlights its three arched windows, frequently in saturated
colour, and the marquee soffit carries a band of bulbs. The glow set mirrors exactly
that and nothing else: `Toy_mustard_Glow` panes behind the three arches, one
`Toy_white_Glow` band along the marquee. The dome stays dark, as it does in life.

## Uncertainties / conflicts

- **The dome's profile is inferred.** Its plan geometry is measured; whether it rises
  as a straight-sided octagonal pyramid or a curved dome is a judgement from satellite
  shading. The build uses a four-segment saucer, which is the more legible choice at
  this scale.
- **Flank cladding.** Sources say brick; every photograph reads as painted grey-beige.
  The build follows the photographs (`Toy_sand`) and treats "brick" as describing the
  substrate, not the finish.
- **Pavilion attic height (29.8 m) is inferred** from photographs scaled against the
  parapet; no drawing was found.
- **Roof plant heights are inferred.** The 2010 LiDAR predates the 2010 renovation's
  rooftop work; positions come from more recent imagery.
