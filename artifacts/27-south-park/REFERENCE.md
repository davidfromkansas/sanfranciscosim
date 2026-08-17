# 27 South Park — reference dossier

Compiled 16 August 2026 for the SF-SIM miniature asset. This file records what
was verified, what was observed, and what was inferred, for the exact geometry
that ships in `27-south-park.glb`. Where it disagrees with
`docs/asset-plans/27-south-park.md`, this file and `REPORT.md` win.

## 1. What this building is

The **centre third of the 1919 warehouse at 21–29 South Park Street**, APN
3775-042, on the south-east rim of the South Park oval in SoMa. One 1919
building in three sections: additions by **Fred Koldenstadt (1920)** and
**Caspar Zwierlein (1921)**, originally "connected with fire doors" and cut
apart by two party walls in the 1993 UMB retrofit. Two storeys, load-bearing
masonry with heavy timber roof trusses, painted, flat-roofed. Office use since
the mid-2000s; the current tenants at number 27 are South Park Commons (Suite
101) and two venture firms (Suite 100).

It is a **contributing resource** to the potential South Park Historic District,
property type `HP8. Industrial`, per the district's DPR 523D — which lists it in
the contributor table as `3775042 / 21 / 27 / SOUTH PARK / HP8. Industrial`.

## 2. Sources and what each establishes

| Source | Establishes | Confidence |
|---|---|---|
| OSM way/112759868 (`addr:housenumber=27`) | the 12.19 × 33.55 m footprint and the 314.8° frontage heading — the only source that separates 27 from 21 and 29 | **measured** |
| DataSF Building Footprints `ynuv-fyni`, `SF3775042` | roof deck 9.60 m median (mean 9.52, std **0.45 m** over 4,479 cells → one continuous flat roof), maximum 11.73 m, ground 11.96 m NAVD88; covers all three sections as ONE 1,115.0 m² polygon | **measured** |
| Overture Maps `overture_buildings.geojsonseq` (16 Aug 2026), ring `w112759868`, source `USGS Lidar` | **10.2 m** for this section's own ring — the crest; also 9.5 m for 21, 9.3 m for 29, 6.7 m for 17–19 | **measured** |
| DataSF Parcels `acdm-wktn` | parcel 3775-042 = address range 21–29 South Park | **measured** |
| SF Assessor `wv5m-vpq2` | built 1919, 2 storeys, 24,680 sq ft over a 13,420 sq ft lot, zoning SPD, construction type C | **verified** |
| SF Building Permits `i98e-djp9`, 53 records on 3775-042 | 1990 parapet bracing; 1993 party walls + roof-truss repair; 2001 UMB plywood diaphragm; **2003 storefront replacement** ($500 k, all three addresses); office fit-outs 2005–2021 | **verified** |
| SF Planning / Page & Turnbull, *South Park Historic District*, DPR 523D, 30 June 2009 | 1919 date, contributor status, `HP8. Industrial`, both 1920s architects, "the three sections are connected with fire doors", and the district's warehouse description | **verified** |
| SF Planning Code §837 (SPD) | the zoning district that preserves the oval's small-scale continuous frontage | **verified** |
| Google Street View, **Jan 2025**, panoramas near `37.78192,-122.39338`, headings 135°–150° | the north-west elevation in full: painted brick, the arcade, the three-bay ground floor, the "27" numeral, the mahogany door, the plain parapet | **observed** |
| Google satellite (near-nadir, 2026), z21 tiles over `37.78174,-122.39314`, ~3 cm/px | the roof: light membrane, continuous parapet ring, plant clustered in the middle third toward the front, two glazed monitors, **no penthouse and no bulkhead** | **observed** |
| LoopNet listing, 21–29 S Park St | 24,680 SF, 2 stories, class C, brick & timber, ~10 ft ceilings, "operable windows overlook South Park". Its "built 1950" is **wrong** | *observed (listing copy)* |
| Perkins&Will, "South Park Venture Capital Firm" (2023, 16,420 sq ft) | that a 1920s brick-clad South Park building with "large, arched metal-clad windows" was renovated recently — **client and address are unpublished**; the matching permits are filed under 21, not 27 | *inference, not attributed* |

## 3. Verified dimensions and location

| | |
|---|---|
| Anchor (WGS84) | `-122.3931439, 37.7817369` — the OSM ring's area centroid, which is also its OBB centre |
| Frontage | **12.19 m**, facing **north-west, outward bearing 314.79°** |
| Depth | **33.55 m** on the 134.79°/314.79° line |
| Plan area | 408.3 m² |
| Roof deck | **9.60 m** |
| Parapet coping crest | **10.20 m** — the asset's bounding-box top, loader scale 1.0 |
| Axis-aligned XY bbox | ~32.6 × 32.5 m (the expected consequence of a ~45° heading) |

The OSM ring is a parallelogram within 0.07 m of a true 12.19 × 33.55 m
rectangle; the asset is built on the rectangle. That departure is an order of
magnitude below the bake's own 0.6 m simplify tolerance.

**Why the OSM ring and not a DataSF footprint.** DataSF has no polygon for 27
alone — its only polygon here is the merged 21–29 parcel, whose centroid falls
3.45 m away, inside 21. Anchoring on it would place the model a third of a
building off its own lot.

## 4. What each side shows

**North-west (South Park) — observed, Jan 2025.** The only public elevation.
Painted brick in a warm off-white, flush, with no corbelling and no cornice
brackets. Two storeys:

- **Ground floor**, 4.55 m tall — nearly half the facade. Three bays of dark
  blue-green joinery in deep reveals, each stacked identically: a row of small
  transom lights, a beaded panel band with a central rosette, then the main
  opening. Bay 1 (north-east) is a pair of tall flush double doors,
  freight-scale, unglazed. Bay 2 is a wide divided-light shopfront window. Bay 3
  carries the painted numeral **"27"** and a **mahogany double door with a
  glazed upper half**, set in a dark blue-green surround. A low painted base
  runs beneath.
- **Second floor**: **six segmental-arched windows**, dark blue-green metal
  frames, ~2.9 m tall, each a large lower light with a transom bar and an arched
  top light, springing from a continuous impost line onto ~0.48 m painted-brick
  piers.
- **Parapet**: plain and flat-topped with a thin coping band, ~0.6 m above deck.

**North-east and south-west (party walls) — inferred.** Blind. 21 South Park is
hard against one flank (Overture deck 9.5 m) and 29 South Park against the other
(9.3 m), both at a measured 0.00 m vertex gap. Modelled as plain painted brick
with the parapet carried across.

**South-east (rear) — NOT OBSERVED.** 12.19 m onto a 2.5–6 m service gap behind
318/326/334 Brannan Street. No Street View reaches it and the nadir aerial only
shows its roof edge. Modelled as plain painted brick with two small service
windows, on the strength of the type. A roll-up loading door would be entirely
unsurprising here — the district survey names them as a warehouse feature "on
the primary or secondary façades" — and is the most likely correction to this
dossier.

**Top — observed, 2026 nadir aerial at ~3 cm/px.** Light warm-grey membrane
inside a continuous white parapet ring shared with both neighbours. Plant is
packed into the **middle third toward the front half**: five or six white
rectangular units, two or three low round fans, flexible ducting between them,
and two low glazed monitors with a visible pane grid. **The rear third is bare
membrane.** No penthouse, no stair bulkhead, no roof deck.

## 5. Recognition cues (ranked)

1. **The six-arch arcade** — the only arcaded facade on this stretch of the oval
2. **The tall dark three-bay ground floor**, nearly as tall as the storey above
3. **The white-painted brick** — this row is painted and its neighbours are not
4. **The one mahogany door** at the numeral, warm against dark blue-green
5. **The proportion** — 12 m wide, 33 m deep, two storeys, level with the row

## 6. Preserved / simplified

**Preserved:** the measured parallelogram and 314.8° heading; two storeys at the
row's height; the six-arch rhythm at its measured 2.03 m spacing; the three-bay
ground floor and its transom / panel / opening stack; the mahogany door; both
party walls as finished blind faces; the front-loaded roof plant.

**Simplified:** each arched window is one recessed arched panel with a frame
band and one transom bar, no muntin grid (the arch is the cue, not its
subdivision); the beaded panel band is one recessed strip plus a single stud in
place of the reeding and rosette; the transom lights are one continuous strip;
the divided-light shopfront is one glazed panel; roof clutter is four boxes, two
fans, two monitors and one vent pipe; painted brick is flat colour, read through
reveal depth and pier width rather than texture. The wall lamp, camera,
downpipe, overhead wires, street trees and bike racks are all omitted.

## 7. Uncertainties

- **The bay assignment.** The frontage is 12.19 m by measurement and the "27"
  numeral sits beside the mahogany door, but 21, 27 and 29 are one continuous
  painted wall and the party-wall joints do not read reliably in the Jan 2025
  capture. The six-arch / three-bay rhythm is *derived from the measured width*
  (12.19/6 = 2.032 m; 12.19/3 = 4.063 m) and matches what the photograph shows
  around the numeral. If better imagery contradicts the count, the count loses;
  the width does not.
- **The 11.73 m DataSF maximum.** Taken over the whole 21–29 parcel, whose
  height standard deviation is 0.45 m — an exceptionally flat single roof. The
  nadir aerial shows no structure inside this ring that could account for it and
  no permit in 53 records adds one. Read as rooftop mechanical plant, and
  excluded from the crest for the same reason 2 South Park's flagpole was.
- **The 0.60 m parapet** is derived (Overture's per-ring 10.20 m minus DataSF's
  9.60 m parcel median), not measured. The 1990 permits confirm a parapet
  exists; nothing states its height.
- **The rear elevation** was never observed.
- **The joinery colour.** Observed as a dark blue-green with no exact palette
  entry; shipped as `Toy_navy 2c4a70`, the closest on-palette value.
