# 501 Third Street — reference dossier

Compiled 15 August 2026. Sources and what each establishes; verified dimensions
and location; orientation; observations from all four sides and above; the
recognition cues; features to preserve and simplify; uncertainties.

## Sources

- **OSM way/147689541** — the 4-node rhombus footprint (592 m2), `addr:housenumber=501`, `addr:street=3rd Street`, `building:levels=3`, `height=14` (Bing-traced). The footprint geometry this asset is built on.
- **DataSF parcels `acdm-wktn`** — block 3775 lot 073, address 501 03RD ST, CMUO zoning, the parallelogram polygon, published centroid -122.3954434, 37.7813151.
- **Assessor secured roll `wv5m-vpq2`** — year built 1920, 4 storeys (see open questions), construction type C, lot area 6,100 sf, building area 18,300 sf, use class Industrial.
- **DBI building permits `i98e-djp9`** (37 records, 1986–2019) — the 2002 UMB seismic retrofit, the 2006 roof deck + guardrail, the 2010 rooftop accessories/storage room, the 2011 elevator-shaft-to-mechanical-room conversion + stair/elevator shaft exterior re-surfacing, the 2019 VRF mechanical system, and a long run of floor-by-floor office TIs on floors 1–3.
- **SF 2010 LiDAR `ynuv-fyni` record `SF3775073`** — 2,273 half-metre cells (≈568 m2, corroborating the OSM polygon), ground mean 5.84 m NAVD88, height median 13.73 m, height max 16.42 m, sigma 0.92 m, peak_1st 22.38 m.
- **checkpermits.com** — aggregated permit history with full descriptions and dates, corroborating the DBI feed.
- **gallery16.com / mapquest.com** — Gallery 16 (long-time ground-floor tenant, 1993–2025, closed September 2025); confirms the gallery use and the SoMa location.

## Verified dimensions and location

| Item | Value | Source |
|---|---|---|
| Address | 501 3rd Street, San Francisco, CA 94107 | OSM, DataSF, DBI |
| Parcel | Block 3775, Lot 073 | DataSF |
| Built | 1920 | Assessor roll |
| Construction | Unreinforced masonry (UMB), type C | DBI permit 200202280352, assessor |
| Storeys | 3 above grade (OSM `levels=3`, DBI permits reference floors 1–3); assessor says 4 (likely includes basement/mezzanine) | OSM, DBI, assessor — see open questions |
| Footprint | 23.6 × 25.05 m rhombus, 592 m2 | OSM way/147689541, reprojected + measured |
| Parapet height | 14.0 m | OSM `height=14` + LiDAR hgt_median 13.73 m (two independent sources agreeing) |
| Rooftop crest | 16.4 m (bulkhead) | LiDAR hgt_max 16.42 m + DBI permits (2010 accessories room, 2011 elevator-to-mechanical-room) |
| Ground | 5.84 m NAVD88 mean | LiDAR |
| Anchor | -122.3954601, 37.7813246 | footprint vertex centroid (measured) |
| Grid heading | 3rd Street axis 45.7°/225.6° true; cross axis 315.3°/135.4° true | OSM geometry (measured) |
| 3rd Street side | SW face, outward normal 225.4° true | DataSF street centrelines (measured, stage 5) |
| Bryant Street side | NW face, outward normal 315.6° true | DataSF street centrelines (measured, stage 5) |
| Taber Place side | SE face, outward normal 135.7° true | DataSF street centrelines (measured, stage 5) |
| Party wall | NE face, against SF3775075 (h 14.90 m) | DataSF footprints (measured, stage 5) |

## Orientation — CORRECTED 18 August 2026

Authored with Blender `+Y` = true north, `+X` = east. The contract's "front faces
−Y" cannot be met — real-world orientation wins per AGENTS rule 5 and the README
orientation note.

**The plan, and the first build, had this 180° out.** They placed the 3rd Street
elevation on the NE face. The NE face is the mid-block party wall. Measured at
stage 5 against the bake's own street centrelines
(`pipeline/data/streets_datasf.geojson`, perpendicular offset of each centreline
from this anchor) and the neighbouring DataSF footprints:

| Face | Length | Outward normal | What is actually there |
|---|---|---|---|
| SW | 25.05 m | 225.4° | **3rd Street** — centreline 24.1 m out, bearing 225.2° |
| NW | 23.59 m | 315.6° | **Bryant Street** — centreline 23.5 m out, bearing 315.2° |
| SE | 23.64 m | 135.7° | **Taber Place** (alley) — centreline 17.0 m out, bearing 135.1° |
| NE | 25.09 m | 45.3° | **party wall** — DataSF SF3775075 (h 14.90 m) abuts, centroid bearing 42° at 21.8 m, nearest vertex 16.3 m |

The method was checked against a control before it was trusted: run on shipped
`500-third`'s anchor it returns 3rd Street at 45.2°, Bryant at 315.3°, Ritch at
225.1°, exactly what that asset's own build script documents. 500 Third and 501
Third face each other across 3rd Street, so their 3rd Street elevations point in
opposite directions — which is what makes the two results consistent rather than
contradictory.

**Consequence for the design.** 501 Third is a CORNER building on 3rd and Bryant
with an alley flank, not a one-street building with three party walls. It has
three exposed elevations, not one. The asset was rebuilt accordingly: the
shopfront and the steel-sash window grid run the 3rd Street front and turn the
corner onto Bryant; Taber Place gets punched windows and the re-surfaced
stair/elevator shaft bump (an alley is where a shaft is re-surfaced from the
outside, a party wall is not); the NE face is blind painted masonry, because
anything modelled there would be buried inside a 14.9 m neighbour.

*The four "observations from each side" below were written against the WRONG face
assignment and are kept only as the record of what was believed. Read them as:
"north-east" = the 3rd Street front, now built on the SOUTH-WEST face;
"south-east" = now Taber Place; "north-west" = now Bryant Street; "south-west" =
now the blind NE party wall.*

## Observations from each side

**North-east (3rd Street, 25.09 m) — the address face.** A painted masonry
industrial loft front. Tall ground floor with a dark storefront/gallery base.
Two upper floors carry large steel-sash industrial windows — the identity. Painted
masonry pilasters and spandrel panels frame the windows. Plain light parapet.

**South-east (23.64 m) — rear/party wall.** Plainer painted masonry with punched
windows rather than the big sashes. Less designed than the 3rd Street face.

**North-west (23.59 m) — rear/party wall.** Same plain treatment as SE.

**South-west (25.05 m) — service rear.** Plainer still; the stair/elevator shaft
bump (resurfaced 2011) projects slightly. Fewer windows.

**Top.** Pale flat membrane field, the central rooftop bulkhead (the crest at
16.4 m — the stair/elevator head converted to a mechanical room), a smaller
accessories box (2010 permit), a roof deck with guardrail (2006 permit), and one
mechanical unit (2019 VRF).

## Recognition cues (ranked)

1. The 45° rhombus footprint — a diamond on the SoMa grid
2. The steel-sash industrial window grid on the 3rd Street face
3. The two-tone base/body split — dark storefront ground floor under light painted upper block
4. The small rooftop bulkhead — the only silhouette event
5. The 1920 SoMa loft type — three storeys, tall floors, big windows, flat parapet

## Features to preserve

- The true rhombus footprint and 45° heading
- The three-storey proportion: tall ground floor + two upper window bands
- The window grid as the dominant facade language on the 3rd Street face
- The two-tone base/body value split
- The flat parapet with one small bulkhead

## Features to simplify

- The window grid becomes a clean recessed grid of identical bays (5 per band)
- Ornament becomes two horizontal bands: a base cap and a parapet cap
- The stair/elevator shaft bump becomes one small projection on the rear
- The roof becomes a membrane field, one bulkhead, one accessories box, a deck guardrail, one mechanical unit
- The membrane is `Toy_steel` (`9aa0a6`), not `Toy_roofd` (`45454a`): the dark
  value measures rgb(9,9,12) on an up-facing plane in the running app and would
  read as a black hole from the aerial camera. `Toy_roofd` stays on the small
  dark rooftop props.

## Uncertainties and conflicting evidence

- **Storey count: 3 or 4?** Assessor says 4; OSM says 3; DBI permits reference
  floors 1–3 only. With hgt_median 13.73 m and 3 storeys, that is ~4.6 m per
  storey — typical for a 1920 industrial loft with tall floors. With 4 storeys
  it would be 3.4 m per storey, unusually short for the type. Modelled as 3
  above-grade floors (ground + 2 upper); the assessor's 4 likely includes a
  basement or mezzanine.
- **LiDAR `peak_1st_m` of 22.38 m** is almost certainly a neighbour bleed (8.6 m
  above the median, sigma 0.92 m — a 9σ outlier). Not used; the credible crest
  is the `hgt_max` of 16.42 m.
- **RESOLVED — which faces are party walls.** The LiDAR footprint (568 m2)
  matches the parcel (567 m2), so the building does fill its lot; the open
  question was which faces that leaves blind. Measured at stage 5 (see
  Orientation): exactly ONE face is a party wall, the NE, against DataSF
  SF3775075 (h 14.90 m). The other three are exposed — two to streets (3rd,
  Bryant) and one to the Taber Place alley. The asset is modelled that way: NE
  blind, everything else glazed.
- **No published architectural height was found.** The 14 m parapet and 16.4 m
  crest are LiDAR-derived (corroborated by the OSM `height=14` tag and the DBI
  rooftop-structure permits).
