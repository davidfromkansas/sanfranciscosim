# 26–28 South Park (51 Taber Place) — reference dossier

Compiled 16–17 August 2026 for `artifacts/26-south-park/`. The plan behind it is
`docs/asset-plans/26-south-park.md`; this file records what was actually verified
at build time, what was corrected, and what stayed inferred.

## 1. Identity

| | |
|---|---|
| Addresses | 26 and 28 South Park; **51 Taber Place** is the Assessor's address of record |
| APN | 3775-049 (block 3775, lot 049) |
| Built | 1907 |
| Storeys | 2 above grade, plus a basement — three occupied levels, ~6,000 sq ft |
| Use | commercial office since 2014; a hair salon 2001–2014; "1 family dwelling" on the 1984 and 2009 permits |
| Zoning | SPD (South Park District) |
| Owner | last sold 4 October 2017 |
| Architect | **none found** — see §6 |

A through-lot sliver on the north rim of the South Park oval, running clean from
South Park at the south-east to Taber Place at the north-west, with blind party
walls on both long sides: the Hotel Madrid (22–24 South Park) to the north-east
and 44–46 South Park to the south-west.

## 2. Sources and what each establishes

| Source | Establishes |
|---|---|
| DataSF Parcels `acdm-wktn`, blklot 3775049 | **the geometry**: an exact four-vertex parallelogram, 30.13 × 6.69 m, 201.5 m², long axis at bearing 315.18°/135.18° |
| SF Assessor secured roll `wv5m-vpq2` | 1907, 2 storeys, lot 2,167.22 sq ft, building 6,000 sq ft, lot depth 98.51 ft, use COMO/Office, address of record 51 Taber Place, sold Oct 2017 |
| DataSF Building Footprints `ynuv-fyni`, SF3775049 (**2010** LiDAR — the `p2010_*` fields date it) | heights: max 13.59, **median 8.35**, mean 8.95, majority 8.36, min 5.89 m, std 1.48 m, ground 11.96 m NAVD88; footprint 180.0 m² over 33 vertices |
| SF Building Permits `i98e-djp9`, block 3775 lot 049 (12 records) | 1984 fire repair + **"new garage with open deck"** ($70 k); 2001–02 salon fit-out; 2009 reroof; 2014 salon→office; 2017 office TI on 1st floor **and basement**; 2019 partition removals on all three levels + **"man doors to garage on 1st floor"**; 2019 brace frame → moment frame at the second floor |
| DataSF addresses `ramy-di5m` | 26 and 28 South Park both resolve to block 3775 lot 049 |
| The Hawthorne Group leasing listing, "28 South Park Street" | ~6,000 sq ft **across three floors**, two private restrooms, conference room, reception, 14+ workstations, **"bright natural lighting with two sides of windows, high ceilings, skylights, 2 car garage parking, 6 wall-mounted bike racks"**. Status: **Leased** |
| Compass, 51 Taber Pl | 1907, 2 stories, ~6,000 sq ft, 0.05-acre lot |
| knowthis.place / iondocs | independent transcriptions of the same permit and roll data — used only as a cross-check |
| Google Street View, **January 2025**, pano near `37.78205,-122.39356`, headings 300–305° | **the South Park elevation** — observed, but the upper floor is largely hidden by a mature street tree |
| Google Street View business photosphere, **January 2012**, "Kim Pfabe's Sugarcane" at this address | **the interior**: a double-height room with a mezzanine, a black stair and a tall multi-pane end window — direct evidence for the "high ceilings" and for a ~4.2 m storey |
| Google Street View, January 2025, pano labelled "22 Taber Pl", heading 140° | a dark-brown lap-sided two-storey face with large white-framed grid windows, a glazed garage door and a recessed personnel door — **probably this building's rear, not confirmed** (§6) |
| Google Maps satellite (Vexcel Imaging 2026, near-nadir, z21, pinned at the parcel centroid) | **the roof**: a plain pale-tan flat plane, essentially empty over the Taber Place two thirds, with darker incident toward the South Park end. Nothing tall stands on it |
| Overpass API, `way["addr:street"="South Park"]["building"]` over block 3775 | **OSM does not trace this building at all** — the housenumber sequence jumps from `22;24` to `41;43` |

## 3. Verified dimensions and location

- **Anchor (design):** `-122.3937435, 37.7822367` — the area centroid of the
  surveyed parcel. After recentring on the model's XY bbox the manifest anchor is
  `-122.3937438, 37.7822369` (a 3 cm shift).
- **Footprint:** 30.13 m deep × 6.69 m wide, 201.5 m². The parcel polygon's
  shoelace area equals its oriented bounding rectangle's to four significant
  figures, so the lot is a **true rectangle**, and it matches the Assessor's
  `lot_area` (2,167.22 sq ft = 201.3 m²) to 0.1%. This is the strongest geometry
  in the South Park series.
- **Heading:** long axis 315.18°/135.18°; the South Park elevation faces
  **135.18°**, the Taber Place rear **315.18°**, and the two party walls 45.18°
  (toward the Hotel Madrid) and 225.18° (toward 44–46).
- **Roof deck:** 8.35 m. **Parapet crest / `targetHeightM`:** 9.05 m.
- **Second floor / open deck:** 4.30 m.
- The frontage is **straight**. The oval's curvature over a 6.69 m chord is a
  0.19 m sagitta, below the model's 0.12 m bevel radius; the survey does not
  record it. (Its neighbour at 22–24, with a 15 m frontage, does curve — see
  `docs/asset-plans/22-south-park.md`.)

## 4. Observations, side by side

**South-east (South Park) — observed, Jan 2025, upper floor tree-obscured.**
Near-black to very dark charcoal, flat and unornamented; no storefront band, no
belt course and no base plinth — the wall runs to the pavement in one colour.
Ground floor, from the south-west: a pair of white-framed windows sitting low and
wide, then a recessed entry bay with a dark timber-panelled double door beside a
narrower glazed door, a small wall lantern, and a notice board on the return; a
shallow step up. At second-floor level a **metal railing runs across the front**
with the wall set back behind it and warm point lights visible under the
setback. A large white-framed window with a horizontal transom serves the second
floor behind the tree.

**North-west (Taber Place) — inferred.** Two storeys in dark-brown horizontal lap
siding, large white-framed multi-pane industrial windows filling most of both
floors, a glazed garage door at ground level and a recessed personnel door beside
it.

**North-east and south-west — party walls.** Blind for the full 30.13 m. Both
neighbours are much taller (22–24 at 12.39 m, 44–46 at 13.52 m), so this
building's flanks are the bottom of a 4–5 m canyon: seen from directly above and
from the three-quarter aerial, never from the street.

**Top — observed, Vexcel 2026 near-nadir.** A plain pale-tan flat roof at 8.35 m,
empty over the Taber Place two thirds, with darker incident toward the South Park
end (the open deck, and most likely the skylights). No penthouse, no plant tower,
nothing that could produce a 13.59 m reading.

## 5. Recognition cues (ranked)

1. **The slot** — 6.69 m against 30.13 m, running clean through the block.
2. **The step** — two storeys between a three-storey hotel and a four-storey
   loft; a 4–5 m notch in an otherwise continuous roofline.
3. **The near-black front**, unusual on a rim where the Madrid is sage green and
   44–46 is pale.
4. **The railed open deck** over the front bay.
5. The recessed timber double-door entry with its wall lantern.

## 6. Uncertainties and conflicting evidence

- **The 13.59 m LiDAR maximum is rejected.** It matches 44–46 South Park's own
  roof-plane median (13.52 m) to 7 cm; the distribution is right-skewed
  (mean 8.95 > median 8.35 = majority 8.36) which is the signature of a minority
  of contaminated cells; and the 2026 aerial shows nothing on the roof that could
  produce it. This is `docs/asset-plans/README.md`'s Earl Warren case — "treat a
  single-cell `hgt_max` on a party wall as unusable" — on a 7.65 m-wide raster
  footprint dilated into *both* taller neighbours. See REPORT.md §1.
- **Storey count, 2 vs 3.** The roll, every permit and Compass say 2; the leasing
  agent says "three floors". Both are right: the third is the basement, which the
  2017 and 2019 permits name explicitly. 180 m² × 3 = 540 m² = 5,813 sq ft, which
  is the listing's 6,000. **Two storeys above grade.**
- **The Taber Place elevation is inferred.** The pano it came from is labelled
  "22 Taber Pl" and the panorama that resolves cleanly onto *this* lot could not
  be isolated. If it is the wrong building, the likely correction is that the rear
  is plainer and the garage is at the South Park end instead.
- **Which end has the garage** follows from the above and is unsettled. Modelled
  at Taber Place, on the strength of the Assessor's address of record.
- **The front setback depth (3.0 m) is inferred**, not measured. It is what makes
  a plausible terrace on a 6.69 m frontage.
- **No architect, no builder, no historic finding.** SF Planning's Property
  Information Map shows the historic-resource status as "tentative". A DPR 523
  form for block 3775, if one exists, would settle both the original form and the
  extent of the 1984 rebuild.
- **OSM has no trace of this building**, so the geometry rests on two surveys
  (parcel and LiDAR footprint) rather than the usual three. They agree on heading
  to 0.9° and on area to 10%, and the parcel matches the roll to 0.1%.

## 7. Features preserved, simplified and omitted

**Preserved:** the 30.13 × 6.69 m rectangle and the 315.18° heading exactly; two
storeys with the deck at 8.35 m; two blind finished party walls; the setback top
floor and its railed terrace; glazing at both ends only; skylights.

**Simplified:** the front window pair → one recessed glazed opening; the multi-pane
rear industrial windows → one glazed panel per floor with a single frame band; the
garage door → one recessed panel; the deck railing → a solid 0.90 m slab; lap
siding → three shallow grooves per storey on the rear only.

**Omitted deliberately:** the entry wall lantern, the notice board, the six bike
racks, the security camera, and all signage. Each is real and each is under a
pixel at the app's camera.
