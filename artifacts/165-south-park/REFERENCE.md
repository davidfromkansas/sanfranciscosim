# 165–167 South Park — reference dossier

Research behind `165-south-park.glb`. Compiled 12 August 2026. The plan
(`docs/asset-plans/165-south-park.md`) was the starting point; this file records what
was re-verified, what changed, and what remains inferred.

**REPORT.md beats the plan wherever they disagree.**

---

## 1. What the building is

A 1908 two-storey, three-unit wooden flats building on the south rim of South Park —
the oval laid out 1852–54 by George Gordon and designed by George Goddard on the model
of a London crescent, San Francisco's oldest planned residential square. It is not a
monument and not architecturally notable. It is a *sliver*: 6.2 m of frontage against
24 m of depth, a flat facade with no bay window, and one saturated blue steel gate.

Both `165 SOUTH PARK` and `167 SOUTH PARK` resolve to block 3775, lot 028, and the
parcel record carries `from_address_num 165` / `to_address_num 167`. That is the
authoritative confirmation that the two numbers are one building, and it is why the
asset covers both.

## 2. Sources, and what each establishes

| Source | Establishes |
|---|---|
| DataSF **Parcels** `acdm-wktn`, `blklot=3775028` | the surveyed lot polygon; the 165→167 address range; zoning `SPD` (SOMA–South Park). **The geometric backbone of the model.** |
| DataSF **Addresses** `ramy-di5m`, `street_name=SOUTH PARK` | 165 and 167 → lot 028; the neighbours 159 (lot 029), 171 (lots 137–139), 181 (lots 172–178) |
| DataSF **Building Footprints** `ynuv-fyni`, `sf16_bldgid 201006.0116627` (`mblr` SF3775028) | LiDAR footprint (109 m², 433 cells at 50 cm); ground 7.78 m NAVD88 median; **height median 8.55 m**, majority 8.50 m, maximum 9.90 m; first-return peak 10.00 m |
| [augrented.com/sf/3775028-165-167-south-park](https://augrented.com/sf/3775028-165-167-south-park) (assessor-derived) | 1908; 2 storeys; 3 units; "flats and duplex"; 2,680 sq ft gross; Dolch 1990 Trust, last sale May 1992; permit history |
| Same, permit history | **2014, $50k exterior**: "replacement of siding, installation of a new metal gate, and stone tile work". 1999 and **May 2024** reroofing (flat roof). 2012 interior. 1997 windows. |
| Google Street View pano `tRhqK_-aiVsKi23dOxYSeg` (©2025), yaws 158°–196°, pitches 8°–26° | the street elevation: pale blue-gray lap siding, dark stone base band, the blue steel picket gate with "165 167" painted in red beside it, white-trimmed punched windows, surface conduit and meters, a street tree |
| Same pano, yaw 196° | **the pedimented entry is 171's, not this building's** — the number "171" is legible beside it |
| OSM `way/124889480` | tagged `addr:housenumber=167`; a Bing trace, 31.7 × 7.8 m, overlapping 159. **Used only as a negative check.** |
| Google/Airbus/Vexcel aerial imagery (2026) | flat roof; rear yard; the continuity of the row along the south rim |
| [Wikipedia: South Park, San Francisco](https://en.wikipedia.org/wiki/South_Park,_San_Francisco), [TCLF](https://www.tclf.org/south-park-ca) | the oval's 1852–54 origin and its two-storey row-house character |

No SF Planning historic survey record for this address was located. No architect is
recorded, and none would be expected for a speculative flats building of this kind.

## 3. Verified dimensions and location

| Item | Value | Confidence |
|---|---|---|
| Lot | 168.1 m²; 6.2 m frontage (chord) narrowing to 4.27 m; 32.7 m deep | **measured**, DataSF parcel |
| Built footprint | **131.2 m²**, 6.205 m frontage, 24.0 m deep | **derived** — parcel truncated at the LiDAR rear extent; see §4 |
| Roof deck | **8.55 m** above grade | **measured**, LiDAR height median over 433 cells (sd 0.65 m); the roof is flat, so the median is the deck |
| Cornice crest | **9.0 m** | *inferred* — deck + ~0.45 m cornice. The shipped target height. |
| Street elevation faces | **349.73°** | **measured** from the parcel's front edge (mean bearing 79.7°) |
| Long axis | front block ~157° for ~10 m, then **135.3°** to the rear | **measured** from the parcel side lines, which bend with the oval |
| Manifest anchor | **-122.3943766, 37.7808600** | derived: design-footprint area centroid, shifted to the model's XY bbox centre |

## 4. Three geometries, and how they were reconciled

No single source gives this building's footprint, and the three that touch it disagree.

| Source | What it is | Verdict |
|---|---|---|
| DataSF **parcel** `3775028` | surveyed lot boundary, 168.1 m² | **authoritative for shape and position** |
| DataSF **LiDAR footprint** `201006.0116627` | 2010 raster-derived built area, 109 m² | **authoritative for built depth only** |
| OSM `way/124889480` | Bing trace tagged `167` | **rejected** |

Reprojected into the project's tangent frame and measured along the lot axis (135.3°,
depth 0 at the parcel's front line), the LiDAR footprint runs from **−3.67 m to
+24.14 m**. The rear extent is credible and is what sets the built depth. The 3.67 m
of front overshoot is not: it would put the building well out into the sidewalk. It is
raster registration error plus cornice capture, and it is discarded.

The built volume is therefore the parcel truncated at **24.0 m**: 131.2 m². That depth
is chosen because it reproduces the assessor's 2,680 sq ft over two storeys to within
5% (2 × 131.2 m² = 262 m² = 2,824 sq ft). The LiDAR's own 109 m² would give only 2,346
sq ft, which is 12% short.

The 11-segment street arc is collapsed to its chord in the model: the bulge is 0.14 m,
below the 0.10 m bevel radius, so modelling it would be false precision.

## 5. What each side shows

**North — street elevation, 349.73°.** The only elevation anyone ever sees. Two storeys
of pale blue-gray horizontal lap siding over a dark charcoal stone-tile base band about
0.9 m tall. Windows are punched and flat in plain white trim with a modest projecting
sill. **No bay window and no ornament** — no brackets, no cornice returns, no pediment.
At the east edge of the frontage a tall blue-painted steel picket gate, roughly 1.1 m
wide and 2.6 m tall, closes a full-height passage between this building and 159; the
house numbers "165" and "167" are painted in red on the siding beside it. Surface
conduit, gas and electrical meters and a downpipe are mounted on the siding.

**East and west — party flanks.** Blind. The east flank abuts the gated passage for the
first few metres and then 159's wall; the west flank abuts 171. **159 is only 5.48 m
tall against this building's 8.55 m**, so the upper third of the east flank is
genuinely visible in the city — which is why the model carries its base course and
floor line all the way round rather than only across the facade.

**South — rear elevation.** Faces a rear yard shared with the neighbouring light wells,
seen only from directly above. One recessed door; otherwise plain.

**Top — the flat roof.** The surface the app's camera actually sees. Flat at 8.55 m for
the full 24 m, reroofed 2024, with the cornice lifting to 9.0 m at the street end only.
The LiDAR maximum of 9.90 m indicates one raised object — a stair bulkhead, a chimney,
or a tree return from the street tree overhanging the roof edge. **It could not be
resolved from available imagery and is not modelled.** See REPORT.md.

## 6. Recognition cues (ranked)

1. **The proportion** — 6.2 m of frontage against 24 m of depth, narrowing to 4.27 m
   and bending 22° partway back. From the aerial camera this is the whole silhouette.
2. **The blue steel gate** — the only saturated colour on the building or its
   neighbours, and the single feature that tells 165–167 apart from 171, which wears
   identical siding and shares an unbroken roofline with it in every photograph.
3. **The flat, bay-less facade** with punched windows — unusual for a 1908 SF flats
   building and therefore diagnostic.
4. **The dark stone-tile base band**, which grounds the pale siding and reads as a
   crisp dark line at thumbnail size.
5. **The flat roof and the taper** seen together from above: a pale sliver that narrows
   and bends as it runs back from the oval.

## 7. Preserved / simplified

**Preserved:** the 6.205 → 4.27 m taper, the 24.0 m depth, the 135.3° / 157° bend, and
the 349.73° facade heading, exactly; the gate's position at the east edge of the
frontage; the base band as a distinct dark value; the roof as a genuinely flat plane
with the cornice lift at the street end only.

**Simplified:** individual clapboards → flat colour with one proud floor-line band;
window openings → four recessed rectangles with proud sills; the gate → a solid slab
with four shallow vertical bars, widened to 1.3 m (the real 1.1 m and the picket gaps
are both sub-pixel at city scale); surface conduit, meters, downpipes and house numbers
→ gone; the rear yard → not modelled at all.

## 8. Uncertainties and conflicting evidence

- **The 9.0 m crest is inferred and everything scales off it.** The 8.55 m deck is a
  real measurement; the 0.45 m cornice on top is not. The unexplained 9.90 m LiDAR
  maximum is the strongest argument that something taller exists up there.
- **The built depth is a reconciliation, not a survey.** The rear wall's position is
  the part of the footprint most likely to be wrong.
- **The window count (two bays per storey) is a designed rhythm**, not a reading off a
  photograph — the single Street View pano is partly behind a street tree. It is the
  weakest facade number here.
- **The present facade is 2014 work, not 1908 fabric.** The siding, the gate and the
  stone base all date from one permit. The model depicts the building as it stands.
- **171 South Park looks like this building** and its pedimented entry is the single
  most likely thing for a modeller to copy onto it by mistake. It is not modelled.
