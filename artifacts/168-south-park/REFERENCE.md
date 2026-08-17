# 166–168 South Park — reference dossier

Compiled 16 August 2026 for `artifacts/168-south-park/`. This is the modelling
side of `docs/asset-plans/168-south-park.md`: what was actually established, how,
and what stayed unverified. Where this file and the plan disagree, this file wins
(pipeline rule: REPORT beats plan, REFERENCE beats plan).

## 1. Sources and what each establishes

| Source | Establishes |
|---|---|
| [OSM way 124884342](https://www.openstreetmap.org/way/124884342) | The footprint. `addr:housenumber=166,168`, `addr:street=South Park`, `building=yes`, `source=Bing`, **no `height` tag**. Five nodes, one collinear. Shares ring vertices with way 124884339 (188 South Park, SW) and way 124884357 (164 South Park, NE) — i.e. it is the outline that describes the party walls. |
| `data.sfgov.org/resource/ynuv-fyni.json?mblr=SF3775070` (DataSF footprints, LiDAR) | Every height in this model. `hgt_maxcm 1044`, `hgt_mediancm 798`, `hgt_meancm 783`, `hgt_mincm 473`, `hgt_stdcm 75`, `hgt_cells50cm 806`, `gnd_min_m 6.32`. Also an outline that is inflated (7.44 × 33.94 m vs OSM's 6.10 × 29.82 m) — used for heights, not for shape. |
| `data.sfgov.org/resource/acdm-wktn.json?mapblklot=3775070` (DataSF parcels) | The lot: 6.99 × 42.06 m, 294 m², zoning SPD, block 3775 lot 070, address 166 South Park. Establishes that the building fills the lot width and 29.8 m of its 42.1 m depth, and that the front sits ~2.7 m behind the property line (the parcel runs under the sidewalk). |
| `data.sfgov.org/resource/i98e-djp9.json?street_number=166&street_name=South Park` (SF permits) | **Two storeys**, on eight permits 1983–1995, `existing`→`proposed` both 2 every time. Construction type 3 on six of them. 1983 `install new entrance doors and storefront`; 1984 `install new front & sidewalk`; 1994 `parapet` + `complete seismic upgrade`; 1995 `rear fire escape to convert 2nd flr res to office`. Use goes retail/dwelling → office around 1990. |
| `data.sfgov.org/resource/beah-shgi.json?block=3775` (DataSF unreinforced masonry) | 166 South Park is **absent**; only 45 South Park is listed on this block. Recorded because the 1994 parapet-plus-seismic permits look like a URM retrofit and the two facts sit awkwardly together. |
| LoopNet 24927521 / Showcase 24341219 | **Built 1912.** 4,600 sq ft over two floors, Class C office, land 0.07 AC (3,049 sq ft — agrees with the measured parcel). |
| Google Street View, Jan 2025 capture, pano at `37.780973, -122.394785` | **The south-east elevation, observed.** Everything in §4 below. The place record anchors this pano to "168 S Park St". |
| Esri World Imagery z20 nadir (0.118 m/px), nine tiles stitched and registered against the OSM ring, the DataSF footprint and four parcel polygons in Web-Mercator pixel space | **The roof, observed.** Flat, bright white, a loose line of small dark items along the middle. z21/z22 return the no-data placeholder here and the Clarity service has no coverage, so z20 is this source's ceiling. |
| Google Maps satellite (Vexcel Imaging US, 2026) | Sharper corroboration of the flat white roof. Not used for measurement — the map's projection was not registered. |
| Business registrations (bizprofile.net, opengovus SF) | Tenancy: Zetta Venture Partners (Floor 1, current, its vinyl lettering is on the display window), Maple VC / Maple 3 VC / Maple SPV-A (2022), Pliancy Inc. (2022–24), Thane Studio / SMW Design (2003–22). Confirms an office building, hence `cat: 3`. |

## 2. Verified dimensions and location

| | Value | How |
|---|---|---|
| Anchor | `-122.3949862, 37.7811327` | OSM ring area centroid, computed |
| Footprint (shell) | 6.10 × 29.82 m, 182 m², parallelogram | OSM ring, reprojected |
| Long axis | 135° / 315° (NW–SE) | measured |
| Front | faces SE, bearing 135° | measured; agrees with the parcel's street line and with the whole north-west rim |
| Crest | **10.44 m** | DataSF LiDAR `hgt_maxcm`; independently checked photogrammetrically, see REPORT §4 |
| Roof deck | 7.98 m | DataSF LiDAR `hgt_mediancm` |
| Storeys | 2 | SF permits |
| Ground | 6.32 m NAVD88 | DataSF LiDAR `gnd_min_m` — the app's terrain handles this, not the asset |

Cross-checks that did **not** agree, and what was done:

- **Footprint width.** OSM 6.10 m, parcel 6.99 m, DataSF LiDAR 7.44 m. Took OSM,
  because it is the only one whose ring shares nodes with both neighbours (a
  party-wall building's outline is defined by the walls it shares) and because
  it matches the visible roof edge in the registered Esri overlay. An angular
  estimate off the Street View capture (~33.6° of facade at ~10 m) gives ~6.6 m,
  between OSM and the parcel.
- **Footprint depth.** OSM 29.82 m, DataSF LiDAR 33.94 m. Took OSM, same reason;
  the LiDAR outline is inflated on both axes here.
- **Construction type.** Six permits say type 3 (ordinary/masonry), one says
  wood frame (5), and the building is not on the URM list despite a 1994 parapet
  and seismic-upgrade pair. Not resolved. It changes nothing about the model and
  no structural claim is made anywhere in this asset.

## 3. Orientation

Authored in world space, `+X` east, `+Y` north, Z up — no rotation at load. The
four corners, centred on the anchor:

```
(  8.415, -12.639)   SE front, south-west corner
( 12.735,  -8.339)   SE front, north-east corner
( -8.415,  12.631)   NW rear, north-east corner
(-12.735,   8.331)   NW rear, south-west corner
```

| Edge | Length | Faces | Elevation |
|---|---|---|---|
| front SW → front NE | 6.10 m | SE 135° | South Park — the only designed elevation |
| front NE → rear NE | 29.82 m | NE 45° | party wall with 164 South Park |
| rear NE → rear SW | 6.10 m | NW 315° | rear yard; the 1995 fire escape |
| rear SW → front SW | 29.82 m | SW 225° | party wall with 188 South Park |

The 45° heading puts the axis-aligned bounding box at ~25.7 × 25.5 m for a
6.10 × 29.82 m building. That is expected, not a scale error.

## 4. What each side shows

**Southeast (South Park front) — observed, Jan 2025 Street View.**
Red brick in running bond, warm red-brown with darker mottled headers. Brick
pilasters divide the 6.10 m front into three bays. The parapet is a single
stepped wall whose top climbs monotonically from the flank return, up one step
on each side, to a raised central panel capped by a shallow gable with a
projecting brick coping; a grey metal coping runs along the shoulders. **One
diamond (lozenge) accent in a contrasting pale material sits in each of the
three panels**, following the steps, so the three sit at two different heights.
The second floor carries tall recessed openings with dark frames — one is
clearly visible in the south-west bay, the rest are behind a street tree in this
capture, and the count of three is inferred from the three parapet panels. The
ground floor is a black-framed shopfront in a brick surround: one wide display
window carrying the tenant's vinyl lettering ("zetta"), and two dark glazed
entrance doors, with brick piers between and at both ends. The 1983/84 permits
date this shopfront.

**Northeast flank — party wall,** sharing ring vertices with 164 South Park.
Plain brick. In the Jan 2025 capture 164's frontage is a low red-painted
structure behind plywood hoarding and a graffiti-covered fence, so a strip of
this flank is momentarily exposed near the street; that is a construction-site
condition, not a designed elevation, and it is modelled plain.

**Northwest (rear) — not observed.** Faces the ~9.5 m rear yard, screened from
3rd Street by 188's block and the Taber Place buildings. No public vantage
reaches it — an attempt from 3rd Street landed in an interior photosphere. The
only recorded fact is the 1995 **rear fire escape**. Modelled as plain brick
with one door, two small openings and a simplified fire escape; all of that
except the fire escape is inference and is flagged as such.

**Southwest flank — party wall** with 188 South Park, which stands 5.5 m taller.
Plain brick, invisible in practice.

**Top — observed.** Flat, **bright white** — a membrane or cool-roof coating,
and by a wide margin the lightest roof on the block in both Esri and Vexcel
imagery. A loose line of small dark items runs along the middle third. **No
penthouse and no roof structure**: the LiDAR standard deviation of 0.75 m over
806 cells says the deck is genuinely flat, so nothing tall stands on it.

## 5. Recognition cues (ranked)

1. **The sliver proportion.** 6.10 m wide, 29.82 m deep, 10.44 m tall, between a
   15.93 m glass-and-metal loft and a low site. Nothing on the rim is this narrow.
2. **The stepped, gable-capped brick parapet** — the only ornament the building has.
3. **The bright white flat roof**, which is what the app's downward camera sees.
4. Red brick against a metal-and-glass neighbour on the party wall.
5. The three diamond accents and the black shopfront.

## 6. Preserved / simplified

**Preserved:** the measured footprint and heading; the two-storey height with the
parapet lifting the crest to 10.44 m; the monotone stepped parapet silhouette;
the roof's white value; three bays and three diamonds; the shopfront's one
window and two doors.

**Simplified:** brick becomes one flat colour (no courses, no mortar); each
window becomes one recessed opening with a single frame band; the diamonds
become inset lozenges rather than modelled reliefs; roof furniture becomes two
skylight runs, a duct, three vents and a hatch, all under 0.6 m so they stay
consistent with the LiDAR; the fire escape becomes a landing, a rail, two posts
and one stringer.

## 7. Uncertainties

1. **The second-floor bay count (three) is inferred** from the three parapet
   panels — a street tree hides the middle of the facade in the only capture
   that reaches this frontage.
2. **The rear elevation is unobserved** apart from the permit-confirmed fire
   escape.
3. **The flank parapet return height (8.60 m) is inferred.** It is not visible in
   any capture; only the two shoulders and the crest are.
4. **The roof's skylight runs are a semantic inference**, consistent with the
   dark items visible in the nadir imagery and with the fact that a 6 m wide,
   30 m deep loft has no other daylight in its middle. Their exact number and
   position are not observed.
5. **Construction type** — see §2.
6. **164 South Park is in flux.** If that lot is rebuilt, the north-east party
   wall could become an exposed elevation and this asset would need revision.
