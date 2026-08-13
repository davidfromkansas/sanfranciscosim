# San Francisco Civic Center Courthouse — reference dossier

400 McAllister Street. Superior Court of California, County of San Francisco.
Everything below was gathered and re-verified for this build; where the plan
(`docs/asset-plans/civic-center-courthouse.md`) and this dossier disagree, this
dossier wins, and where the build disagrees with this dossier, `REPORT.md` wins.

## Sources and what each establishes

| Source | Establishes |
|---|---|
| OSM way/108389188 via Overpass (`amenity=courthouse`, `building=government`, `height=25`, `check_date=2026-02-23`) | The 12-node footprint polygon, including the explicit 6.1 m chamfer at one corner; the surveyed parapet height |
| Nominatim, bounded to the SF bbox | Address resolution and the building's bounding box; the OSM name "San Francisco Civic Center Courthouse" |
| DataSF `ynuv-fyni` (Building Footprints with 2010 LiDAR-derived heights), building `SF0766002` | `hgt_median` 24.67 m, `hgt_mean` 25.19 m, **`hgt_max` 29.60 m** over 12,618 50 cm cells; `gnd_min` 20.24 m NAVD88. This is the only source for the crest |
| **Mark Cavagnero Associates project page** — McAllister Street elevation (with a 0–40 ft scale bar), site plan, upper floor plan, two study-model photographs, one colour exterior photograph of the McAllister/Polk corner | The whole classical composition: bay count, arch geometry, base storeys, attic band, cornice, the corner lantern, and the contemporary north/west treatment. The single most valuable source, and it is the architect's own |
| Superior Court of California, County of San Francisco | Program (44 courtrooms), opening date (9 December 1997), that the building is at Polk and McAllister |
| Esri World Imagery z19 (~0.24 m/px), reprojected and rotated to the building axis | The roof plan: continuous parapet, a long louvered penthouse, two mechanical clusters, and the octagonal lantern at the corner |

## Verified dimensions and location

| | |
|---|---|
| Footprint (min-area oriented bbox) | **83.46 x 36.98 m**, polygon area 3,073 m² |
| Long-axis bearing | **81.22° cw from true north** |
| OBB centre / polygon centroid | (1605.13, −1159.54) and (1605.03, −1159.57) local metres — they agree to 0.1 m |
| OBB centre WGS84 | **−122.4192590, 37.7804897** |
| SE chamfer | 6.1 m across the corner, i.e. 4.31 m off each face |
| Parapet | 25.0 m (OSM tag; LiDAR median 24.67 m) |
| **Crest (target height)** | **29.6 m** (LiDAR `hgt_max`) |
| Storeys | six |

Heights read off the architect's McAllister elevation, scaled by its 0–40 ft bar
(40 ft = 178 px, so 1 m ≈ 14.6 px), and reconciled against the two measured
anchors above:

| Line | m |
|---|---|
| Rusticated base top / string course | 7.6 |
| Arcade sill | 8.6 |
| Arch springing | 15.2 |
| Arch crest | 17.9 |
| Attic band of square windows | 19.3 – 20.7 |
| Projecting cornice | 20.7 – 21.7 |
| Parapet top | 25.0 |
| Rooftop penthouse | ~27.6 |
| Corner lantern crest | 29.6 |

## Which corner carries the lantern — a resolved conflict

Two published descriptions appear to disagree. Courthouse references describe an
angled "southeast" entrance rising to a dome with round windows; a court directory
places the building "on the corner of Polk and McAllister". These are the same
corner. McAllister Street runs along the building's **south** side — the courthouse
sits north of McAllister, one block north of City Hall — and Polk Street is the
**east** side. McAllister × Polk is therefore the **south-east** corner. Three
independent checks agree:

1. the OSM polygon's 6.1 m chamfer is between its southern and eastern edges;
2. the satellite roof plan puts the octagonal drum at that corner;
3. the architect's McAllister elevation shows the lantern at the drawing's east end.

## What each side shows (observations)

- **South — McAllister Street, 83.5 m, the ceremonial front.** Two-storey rusticated
  granite base carrying two rows of square punched windows. Above it a giant order of
  **five round-arched windows**, ~6.0 m wide at ~9.5 m pitch, the arcade sitting
  roughly a third in from the west end, with a narrow slot window splitting each pier.
  East of the arcade a stretch of wall with tall narrow windows. Above: a plain
  frieze, an attic band of small square openings, a projecting cornice, a plain
  parapet, and a louvered mechanical penthouse set back behind it.
- **East — Polk Street, 37 m.** The same language compressed: rusticated base, two
  giant arches, attic band, cornice. Cavagnero's own text puts the traditional
  materials and detailing on the south and east.
- **North — Golden Gate Avenue.** The contemporary face. The study-model photographs
  show no arcade at all: a flat granite wall with a regular grid of banded/louvered
  ribbon windows over four storeys above the base, and service and loading openings
  at grade.
- **West.** Contemporary and plainest, partly blind where it meets the mid-block
  neighbour.
- **SE corner.** Chamfered at 45° for the building's full height. At grade a recessed
  glazed entrance under a tall flat head, flanked by flagpoles; above it a projecting
  three-storey glazed bay; above the cornice a square chamfered attic block, then an
  **octagonal drum carrying large circular oculi**, then a shallow segmental dome.
- **Above.** A bright flat membrane roof inside a continuous parapet; a long louvered
  penthouse running roughly east–west near the middle; one mechanical cluster
  centre-west and a second toward the east end; the lantern standing clear of
  everything at the SE.

## Recognition cues (ranked)

1. The octagonal lantern — round oculi under a shallow dome — on the chamfered corner.
2. The giant round-arched arcade over a heavy rusticated base.
3. Near-white granite: the coldest, lightest wall value in the Civic Center set.
4. The attic band of small square windows under a projecting cornice.
5. The two-faced parti: classical south and east, flat modern north and west.

## Features to preserve / simplify

**Preserve:** the chamfer; the lantern's octagon, its oculi and its dome; five arches
on McAllister and two on Polk; the two-row rusticated base; the attic band; the
cornice projection; the ribbon-banded north and west; the roof's penthouse-plus-plant
layout.

**Simplify:** the Albert Paley entrance doors (a flat dark recess instead); the
granite panel joint pattern (gone); the mullion grid inside each arch (one flat
`Toy_glass` pane); the punched-window count in the base (20 per row → 10) and in the
attic band (17 → 11) — at the app's camera the real counts read as a checkerboard,
which is exactly the failure mode §26 of the style bible warns about; the sixth-floor
setback on the north.

**Exaggerate** (style bible §9): the drum, whose ~10.6 m measured diameter is drawn
~15 % larger so the lantern still reads from the aerial camera; the cornice
projection; the depth of the rustication.

## Night appearance

The building is not a floodlit monument. The glow set is therefore deliberately
small: the lantern's eight oculi and the seven arcade windows, plus a single thin
warm strip over the corner entrance canopy. The lantern is the hero — at dusk the
asset should read as a lit crown on a dark corner, which is what the corner does in
photographs.

## Uncertainties / conflicts

- **No published architectural height exists.** 29.6 m is 2010 LiDAR. The independent
  OSM survey (`height=25`, 2026) agrees with the same dataset's median, which is a
  useful cross-check on the parapet but not on the crest.
- The **north and west elevations are inferred** from study-model photographs; band
  positions and counts there are design decisions.
- The **arch count on Polk (two) is inferred** from the corner photograph; the
  architect publishes only the McAllister elevation.
- The **penthouse height (27.6 m) is inferred** to sit below the 29.6 m crest; 2010
  LiDAR cannot distinguish it from the lantern.
- **Wall colour.** Photographs are bright-sun exposures; the real granite may read
  greyer than `Toy_trim` (f3efe6). Recorded as an artistic call.
