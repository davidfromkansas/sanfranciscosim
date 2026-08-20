# 132 The Embarcadero — reference dossier

The Jewish Community Federation Building, 132 The Embarcadero / 121 Steuart
Street, San Francisco. Assessor block 3715, lot 003. Built 1984, seven storeys,
red brick, on a 13.75 x 42.95 m lot that runs the full depth of the block from
Steuart Street through to the Embarcadero waterfront.

Compiled 18 August 2026 for `artifacts/132-embarcadero/`. This dossier records
what was verified for the build; `docs/asset-plans/132-embarcadero.md` is the
plan behind it and `REPORT.md` records what the build actually did, including
where it departed from the plan. **REPORT beats plan; this file beats neither on
intent but is the authority on the numbers the model was built from.**

## 1. Identification, and the two ways to get it wrong

The address `132 The Embarcadero` resolves to **block 3715, lot 003** — the same
parcel as `121 Steuart Street`. Two independent traps sit on the way there and
both were checked:

**Trap 1 — OpenStreetMap puts the Angler restaurant in the wrong building.**
OSM node `2840137601` carries `name=Angler`, `addr:housenumber=132`,
`addr:street=The Embarcadero`, and it falls inside OSM way `193054137`, two lots
southeast on parcel 3715-025. Geocoding the address through Nominatim returns
that node first. It is a misplaced POI. The evidence for lot 003:

- DataSF EAS address point for `132 THE EMBARCADERO` is −122.3924234,
  37.7932441, which falls inside this building's footprint near its Embarcadero
  frontage (verified by point-in-polygon against OSM way 193054135).
- All twelve DBI permits filed at 132 The Embarcadero carry block 3715; ten
  carry lot **003**. The two that carry lot 004 are from 1982 and 2000, before
  lots 004 and 005 merged into today's lot 025.
- Those permits describe this building's tenancy history exactly: a
  `food/beverage hndlng` occupancy on the ground floor from 2000, an awning
  dismantled in 2017 (the Chaya Brasserie fit-out being stripped), the Angler
  wall sign in 2018, kitchen make-up air in 2019, and a pergola filed in
  January 2026.

**Trap 2 — the Street View "front" heading points down the street, not at the
building.** Google's place card for this address returns a panorama looking
northwest along the Embarcadero at the Ferry Building, not at the facade. The
facade panoramas were found instead by reading the neighbour graph out of
`https://www.google.com/maps/photometa/v1` and selecting the pano nearest the
foot of the facade's own perpendicular.

**The building identifies itself.** The Steuart Street elevation carries
`JEWISH COMMUNITY FEDERATION` in incised metal letters above the entrance, with
`121` beside the doors — read directly from panorama
`CZDneEIDtQW66UdbfLSsgw`.

## 2. Sources

| Source | What it establishes |
|---|---|
| DataSF Addresses `ramy-di5m` | the EAS point for 132 THE EMBARCADERO; 100 THE EMBARCADERO = The Audiffred Building |
| DataSF Parcels `acdm-wktn` | block 3715 lot geometry; lot 003 = 121 Steuart, lot 025 = 131–141 Steuart |
| DataSF Assessor roll `wv5m-vpq2` | 1984, 7 storeys, 44,107 sq ft, Commercial Office |
| DataSF Building Permits `i98e-djp9` | the lot-003 attribution; AT&T antenna work 2016/2018/2021; a 2024 DISH installation with a rooftop equipment platform; lift machine rooms and hoistways (2020-12-11, 2021-03-15); reroofing 2019 |
| DataSF Building Footprints `ynuv-fyni` | LiDAR footprint `201006.0005323`, MBLR `SF3715003`, and the height distribution in §4; the same for all six neighbours |
| OpenStreetMap way `193054135` | `building=office`, `building:levels=7`, `roof:shape=flat`; the footprint geometry the OBB is derived from |
| Google Street View panoramas `OLku-hi1dEEvbjsiBr8EWw`, `yo5P5pi5QKGaa2I7JTPGvQ`, `35oWNxHtxVyAvhUceWPuVA`, `CZDneEIDtQW66UdbfLSsgw` | both elevations, the entrance, the base, the crown; the photogrammetric solve in §4 |
| jewishfed.org; causeiq.com; skydb.net | the occupant; SKYDB's incorrect six-floor count |

No architectural publication exists for the 1984 building. Exa searches over
architecture and real-estate domains returned the restaurant's press coverage
and the occupant's contact pages, and nothing about the building. **No architect
is attributed.** That is a finding, not an omission.

## 3. Geometry

Minimum-area oriented bounding box of OSM way `193054135`, projected with the
app's tangent projection (`x=(lon+122.4375)·111320·cos 37.77°`,
`z=−(lat−37.77)·110540`):

| | |
|---|---|
| Street frontage | **13.75 m**, along bearing 134.95° |
| Depth | **42.95 m**, along bearing 44.95° |
| OBB centre (the anchor) | **−122.3925476, 37.7931482** |

Three surveys, and they agree: OSM ring 590.6 m2, DataSF LiDAR ring 617 m2,
Assessor floor area 44,107 sq ft over 7 storeys = 585 m2 per floor. The OSM ring
is used because its corners sit on the party walls this row actually shares.
The OBB centre was taken over any ring centroid because the OSM ring carries two
sub-metre jogs at its Embarcadero end that pull a vertex mean 6.8 m off the true
rectangle centre; the DataSF ring's area centroid lands 1.42 m from the OBB
centre and the OSM ring's 0.17 m.

**Face bearings** (outward normals, true):

| Face | Bearing | Condition |
|---|---|---|
| Northeast | 44.95° | The Embarcadero — the address, the storefront, the glazed ribbon |
| Southwest | 224.95° | Steuart Street — the institutional entrance |
| Southeast | 134.95° | party wall, Steuart Place (131 Steuart). Concealed |
| Northwest | 314.95° | party wall, 110–116 The Embarcadero. Exposed above ~18 m |

The Embarcadero frontage sits 16.5 m from the Embarcadero centreline and 54.5 m
from Steuart's; the Steuart frontage sits 11.7 m from Steuart's centreline.
Neither elevation is set back.

## 4. Heights — how each number was obtained

**Measured — the parapet, 27.4 m ± 0.4.** Panorama `OLku-hi1dEEvbjsiBr8EWw`
stands at −122.3922925, 37.7934067: 15.2 m from the Embarcadero frontage, 17°
off its normal. Detecting the sky/building boundary column by column and
intersecting each ray with the measured facade plane gives the parapet crest at
40 sample points spanning 0.3–13.9 m along the 13.22 m frontage with a standard
deviation of **0.08 m** — the parapet is dead level. Camera height was
calibrated against the facade's base line in a second, pitched-down view of the
same panorama and brackets at 1.9–2.5 m; that bracket is the dominant residual
and is what the ±0.4 represents.

**Measured — the facade's horizontal lines.** The same rig, run against the
window glazing rather than the sky, gives (metres above grade):

| Element | Sill | Head |
|---|---|---|
| Storefront (Embarcadero) | 0.30 | 3.10 |
| Brick spandrel course | 3.10 | 3.55 |
| Second-floor glazed ribbon | 4.37 | 6.11 |
| Floor 3 | 7.45 | 9.03 |
| Floor 4 | 10.70 | 12.28 |
| Floor 5 | 14.37 | 15.95 |
| Floor 6 | 17.87 | 19.45 |
| Floor 7 | 21.37 | 22.95 |

Sill-to-sill spacings are 3.08, 3.25, 3.67, 3.50, 3.50 m — mean floor-to-floor
**3.40 m**. Openings are 1.58 m tall on a **2.292 m bay**, six bays across the
13.75 m frontage.

**Verified — the roof deck, 26.82 m.** DataSF LiDAR for this footprint: median
26.82, mode 26.68, mean 26.38, sigma 3.85, minimum 0.20, maximum 29.57, ground
3.46 m NAVD88. Mean below median with a 0.20 m minimum is edge bleed — the 50 cm
raster mask covers 625 m2 against a 617 m2 ring, so its rim cells catch the
sidewalk. That accounts for the low tail and the large sigma. The median and the
mode agree to 0.14 m, which is the roof deck.

The photogrammetric parapet sits 0.6 m above that deck. Two methods, not tuned
to each other, agreeing: that is what turns "estimated" into "measured".

**Inferred — the crest, 29.57 m.** The LiDAR maximum is 2.75 m above the deck,
and neither party-wall neighbour can account for it (Steuart Place peaks at
27.77, 110–116 at 24.43, and that 24.43 is itself bleed from *our* wall). The
building is a 1984 seven-storey office with traction lifts — DBI records "machine
room & hoist ways" and "elevator machine rooms" — and a lift/stair bulkhead 2.75 m
above the deck is exactly what that produces. It is invisible from both frontages
because the sight line to the parapet is 60° at 15 m and 34° at 37 m.

**This is the one inferred number in the model, and it is the one that sets
`targetHeightM`.** If it is wrong — if 29.57 m is an antenna mast rather than a
bulkhead — the correction is to drop `targetHeightM` to 27.4 and put the plant
below the parapet. The parapet is measured independently, so a wrong bulkhead
cannot mis-scale the building; it can only add a phantom box on the roof.

## 5. What each side shows

**Northeast, The Embarcadero (13.75 m).** Brick piers with three blue-grey
framed glazed storefront bays; a brick spandrel course above them carrying three
small square wall lights; a **full-width second-floor glazed ribbon** deeply
reveal-set; five floors of six-bay punched windows in light metal frames; plain
brick; a pale crown band; a thin dark coping.

**Southwest, Steuart Street (13.75 m).** The same brick, grid, crown and coping,
on a completely different base. A deeply recessed entrance under a projecting
brick lintel with a soldier course; `JEWISH COMMUNITY FEDERATION` incised above
it and `121` beside the doors; aluminium-framed glass entrance doors flanked by
two blue-grey steel service doors with planters; a continuous row of steel
security bollards along the kerb. **The second floor on this side is blind
brick** — no ribbon. The ground floor reads as a double-height lobby.

**Southeast, party wall to Steuart Place.** Concealed. The neighbour's LiDAR
mode is 24.99 m and its maximum 27.77 m, within 2.4 m of our deck.

**Northwest, party wall to 110–116 The Embarcadero.** Partly exposed, and by an
uncertain amount. The Assessor and the 2010 LiDAR say three storeys and 10.5 m;
current Street View shows a glass building of roughly 18 m. The reading adopted
here is that the neighbour was rebuilt or reclad after 2010 and now stands at
about 18 m, leaving the top ~9 m of this wall bare.

**Above.** Not observed. No orthophoto reachable for this dossier resolves a 27 m
roof here: Google's z22 tiles lean far enough that the roof cannot be attributed
to the footprint, and Esri's z20 is worse. §4 explains what was inferred instead.

## 6. Recognition cues, ranked

1. **Red brick between cream/glass and a darker block** — the only brick in its
   stretch of the row, and the whole identification from the aerial camera.
2. **The narrow deep slab** — 13.75 m wide, 42.95 m deep, one storey above both
   party-wall neighbours, pointed at the water.
3. **The pale crown band** under a dark coping, wrapping the building.
4. **The six-bay punched grid**, even and regular on both fronts.
5. **The Embarcadero glazed ribbon** — the one horizontal cut in the brick, and
   the night hero.

## 7. Preserve / simplify

**Preserve:** the 1:3.1 proportion; the brick; the crown band; the six-bay
rhythm; the ribbon; the asymmetry between an open Embarcadero base and a blind,
lettered Steuart base.

**Simplify:** brick coursing (flat colour); window frames (one recess, one pane);
the incised lettering (one gold strip, semantic scale); the storefront mullions;
the roof plant (a handful of blocks, one antenna platform); the bollards (see
REPORT — they were dropped entirely).

## 8. Uncertainties carried into the build

1. The roof composition is inferred, not observed (§4). The bulkhead's plan
   position is a design decision, not a survey.
2. The northwest neighbour's height, and therefore how much of that party wall
   is bare (§5).
3. The crown band's depth. The colour scan across the top of the facade was
   taken in shadow and returned a mixed brick/pale zone between 24.3 and 26.9 m.
   The build uses 25.40–26.90 m — the conservative end — for the reason recorded
   in REPORT §2.
4. No architect, and no drawing. Every facade dimension in §4 is photogrammetric.
