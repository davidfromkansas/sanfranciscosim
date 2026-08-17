# 76–82 South Park — reference dossier

What was verified, what was measured, what was read off a photograph, and what was
corrected against `docs/asset-plans/76-south-park.md`. Compiled 16–17 August 2026.

**REPORT.md beats this file for build decisions; this file beats the plan for facts.**

---

## 1. Identity — settled, and it was not trivial

The address `76 S Park St` geocodes badly. Nominatim returns nothing inside the SF bbox,
OSM carries no `addr:housenumber=76` node, and Google's own place card for
"76 S Park St" shows a photograph of **70** South Park (the glass-and-rust-steel building
next door), because the geocoder snaps the address point to the nearest Street View pano.

The building was identified positively, not by elimination:

- OSM `way/124884340` is tagged `addr:housenumber = 76;78;80;82`, `addr:street = South Park`,
  `height = 13` — a 7.22 × 29.43 m rectangle sharing its long north-east edge with
  `way/124884345` (70 South Park) and its long south-west edge with `way/113545687`
  (84 South Park). Party walls, both sides, shared vertices.
- SF Assessor block 3775 lot 054, `property_location = "0082 0076 SOUTH PARK ST"`.
- Zoneomics carries an address point at `37.7819612, -122.3939021`, which falls within
  5 m of the measured street-end midpoint of that footprint — independent confirmation
  that the **south-east end is the addressed frontage**.
- Decisive visual: one January 2025 Street View frame (pano `xwBAWoi-oQKrwMaSWwutNA`,
  heading 350°, tilt 118°) has **both neighbours' numbers in shot** — "84" on the
  blue-grey building with the green living wall at the left, "70" on the glass building
  with the rust-steel exo-frame at the right — and the dark bronze-brown bay-fronted
  building between them is the subject.

An earlier reading of a narrower-field frame mistook the grey building further down the
row for the subject. The two-numbers-in-one-frame check is what corrected it, and is the
check to repeat if anyone doubts the identification.

## 2. Measured

| Quantity | Value | Source |
|---|---|---|
| Block / lot | 3775 / 054; `mblr SF3775054`; `sf16_bldgid 201006.0026693` | SF Assessor; DataSF `ynuv-fyni` |
| Built | 1906 | SF Assessor `year_property_built`; repeated by Showcase |
| Units / storeys / class | 3 units, 3 stories, `F` Flats & Duplex, `MRES`, zoning `SPD`, construction type `D` | SF Assessor secured roll |
| Lot | 2,147.2 sq ft (199.5 m²), depth 97.6 ft (29.75 m) ⇒ 22.0 ft (6.71 m) implied width | SF Assessor |
| OSM footprint OBB | **7.22 × 29.43 m** at 314.7°, polygon area 212.5 m² | OSM `way/124884340`, rotating calipers |
| DataSF LiDAR footprint OBB | **6.93 × 30.60 m** at 314.2°, polygon area 190.6 m² (763 cells × 0.25 m² = 190.8 m², consistent) | DataSF `ynuv-fyni` |
| Ground | 10.91 m min / 11.43 m median / 11.75 m max NAVD88 — the site falls 0.84 m toward the park | DataSF `ynuv-fyni` |
| Roof deck | **13.08 m** (`hgt_median_m`); majority 12.84; mean 11.86; σ 3.47; min 3.76 | DataSF `ynuv-fyni` |
| LiDAR maximum | **16.28 m** (`hgt_maxcm`) | DataSF `ynuv-fyni` |
| 70 South Park (NE) | `SF3775053`, deck 12.87 m, max 16.35 m | DataSF |
| 84 South Park (SW) | `SF3775055`, deck 11.36 m, max 13.24 m; built 1907, 2 stories | DataSF + assessor |

The two footprint sources agree on **heading** to 0.5° and disagree on **width** by
0.29 m. The OSM polygon is a clean rectangle (212.5 m² against a 212.1 m² OBB, i.e. the
"notch" vertices are collinear); the DataSF polygon is a 20-vertex raster trace whose OBB
is 212.1 m² but whose own area is 190.6 m². Taking the DataSF width and the assessor
depth gives the shipped **6.90 × 29.70 m**.

## 3. The crest — the one number that is an attribution

The LiDAR maximum is 16.28 m over this footprint and 16.35 m over 70's, while 70's deck
(12.87 m) is *lower* than this building's (13.08 m). So the tall element is real, it is
not a taller neighbour bleeding across the party wall (the argument that killed
104–106's maximum does not apply here), and the LiDAR alone cannot say which of the two
buildings owns it.

Two independent things point at this building:

1. Both rental listings document a **common roof deck** — furnished, with a barbecue,
   "open nights and weekends". A deck needs a stair bulkhead and 2.4–3.0 m is what one
   measures.
2. The Hawthorne Group exterior photograph shows a **dark box standing above the
   roofline**, plus a smaller vent at the south-west edge.

Photogrammetry on that photograph, in its 1067 × 800 original: horizon ≈ y 660,
roofline y 318 (13.08 m), box top y 290, camera ≈ 45 m out in the park. That calibrates
to ≈ 23.8 px/° and puts the box top at 15.55° of elevation. Solving for height against
setback:

| Setback | Camera distance | Implied crest |
|---|---|---|
| 0 m | 45 m | 14.0 m |
| 6 m | 51 m | 15.7 m |
| 10 m | 55 m | 16.8 m |

A bulkhead standing on the facade plane would be very unusual; 8–11 m back on a 29.7 m
roof is normal, and that band brackets 16.28 m. **Kept, at 16.28 m, as a single
deletable object** (`roof_penthouse`) — see REPORT.md §3.

Caveat that survives: the box in the photograph is centred on or just past the party
wall (x ≈ 570–668 where this building's right edge is near x ≈ 610), so it may be shared
or mirrored, and the photograph is undated.

## 4. Elevations

**South-east (street, faces 135.0°).** Rusticated cast-stone base in mottled warm
tan-grey, covering the ground floor and the first level, with a **tall arched opening**
on the south-west half. A **full-height stone pier** at the centre. Out of it, a
**two-storey canted bay** on the north-east half, clad in dark bronze-brown board on a
stone corbel. On the south-west half above the base, a **large multi-pane industrial grid
window** with a shallow soffit over it and two small windows above. At ground level, dark
storefront glazing to the north-east and a recessed entry under the pier. A **slim metal
juliet railing** crosses at roughly 37% of the facade height.

**The mural.** The Hawthorne photograph shows a tall painted figure in ochre and gold
running down the stone pier from the first level to the ground. In the January 2025 pano
the pier is largely bare stone with only a small patch of colour surviving near the top.
**Treated as gone; not modelled.** If it is current, the building's most memorable
feature is missing from the asset.

**North-east flank (toward 70, faces 45°).** Not visible. 70's deck is 0.21 m lower, so
this edge reads as a continuous roofline. **No exposed band, deliberately.**

**South-west flank (toward 84, faces 225°).** A 1.72 m band of plain wall above 84's
11.36 m roofline, running the full 29.70 m. The only place the building's depth is
legible from the ground.

**North-west (rear, faces 315°).** **Unobserved.** No photograph found. The DBI record
says there are rear stairs (repaired 2002–04, worked on again 2007) and the 311 record
says the rear yard is parked in. Modelled plainly: flat face, a 3 × 3 window grid, a
service door, and a simple external stair to level 2.

**Roof.** Flat at 13.08 m with a 0.35 m parapet. Deck on the street third with railing
and festoon lamps; stair penthouse behind it toward the north-east; two mechanical
boxes on the rear two-thirds. The deck position is argued from what the listings say the
views are ("views of South Park", "downtown views"), not observed — the best available
nadir imagery is Google/Vexcel at 20z ≈ 0.12 m per CSS pixel, enough to show the roof is
occupied and not enough to lay it out.

## 5. What could not be obtained

- **Any oblique aerial.** Bing Bird's Eye returns blank tiles; Google Maps' 3D tilt
  parameters did not apply from a URL; Google Earth web would not finish streaming on
  this machine. Three attempts, all recorded. The roof layout and the penthouse
  attribution both remain open because of this.
- **Any architect, name, historic-resource listing, or published architectural
  description.** Exa searches on the address, address + "architect", and address +
  "rooftop" returned only listing and data-aggregator pages. This building has no
  documentary record beyond a tax roll and three rental listings.
- **The rear elevation and the rear yard**, in any image.
- **The garage.** Both listings document a two-car garage. No roll-up door is legible
  within this building's 6.9 m of frontage in either available image (the shutter in the
  Hawthorne photograph is on a neighbour, well to the south-west), and the 311 record
  points at the rear yard. Modelled as a neutral dark service bay so either answer is a
  small edit.

## 6. Sources

- SF Assessor Historical Secured Property Tax Roll — `https://data.sfgov.org/resource/wv5m-vpq2`, `block='3775' AND lot='054'`
- DataSF Building Footprints (LiDAR-derived, 2010 survey) — `https://data.sfgov.org/resource/ynuv-fyni`, `mblr=SF3775054`, plus `SF3775053` and `SF3775055`
- OpenStreetMap `way/124884340` (and `way/124884345`, `way/113545687`)
- The Hawthorne Group — `https://www.thgcommercial.com/project/76-82-south-park-street/`; exterior photograph `https://www.thgcommercial.com/wp-content/uploads/2024/03/76-82_South-Park.jpg` *(observed, listing photo, undated)*
- Showcase — `https://www.showcase.com/76-82-s-park-st-san-francisco-ca-94107/37902715/` *(6,100 SF total, class C, 1906, land 2,178 SF)*
- Zumper — `https://www.zumper.com/address/76-s-park-ave-san-francisco-ca-94107-usa` *(common roof deck with furnishings and barbecue, open nights and weekends)*
- Augrented — `https://augrented.com/sf/3775054-76-82-south-park` *(secondary: DBI complaint / violation record, 2007 renovation scope)*
- Zoneomics — address point `37.7819612, -122.3939021`
- Google Street View, January 2025, panos `xwBAWoi-oQKrwMaSWwutNA` (`37.7818698, -122.3939012`) and `VNjTSqMURh5c_TFZCV6J3Q` (`37.7819313, -122.3938256`, labelled 70 S Park St)
- Google Maps satellite `@37.782035,-122.394045,20z` (Airbus / Vexcel 2026)

## 7. Corrections made to `docs/asset-plans/76-south-park.md`

Made **before** building, and folded back into the plan (commit `fe6da2dd`):

1. **The crest photogrammetry was replaced** with the setback table in §3 above. The
   plan's first version quoted a naive same-plane reading of "about 1.0 m" and then
   hand-waved the setback correction; the calibrated version is both stronger and
   falsifiable.
2. **The garage was downgraded** from "a roll-up garage door at the south-west end of
   the ground floor" to an unresolved question with a neutral service bay, because no
   such door is legible on this building's frontage and the shutter that suggested it is
   a neighbour's.
3. **A first-floor juliet railing was added** to the street elevation — visible in the
   Hawthorne photograph, missed on the first pass.
