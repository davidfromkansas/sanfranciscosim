# 101 South Park — reference dossier

Research behind `artifacts/101-south-park/`. Compiled 12 August 2026 as part of the
`docs/asset-pipeline/ADDRESS-TO-ASSET.md` run for `BUILDING: 101 S Park St, San Francisco,
CA 94107`. The plan at `docs/asset-plans/101-south-park.md` is the design brief; this file
records what was actually verified before modelling, and `REPORT.md` records what the build
decided where the evidence ran out.

**Where this dossier is weak, in one line:** the front elevation and the roof are
well-evidenced; the height is a photogrammetric estimate; the other three elevations are
inferred.

## 1. Identity

| | |
|---|---|
| Address | 101 South Park, San Francisco CA 94107 (the street is signed "SOUTH PARK") |
| Block / lot | 3775 / 038 |
| DataSF footprint id | `mblr = SF3775038` |
| OSM way | [113545689](https://www.openstreetmap.org/way/113545689) |
| Occupant | Kleiner Perkins |
| Interior architect | Perkins&Will (Jaclyn Guasco, Stephanie Kwan), completed 2023 |
| Assessor "year built" | 1947 (contested — see §6) |

## 2. Sources and what each establishes

| Source | Establishes |
|---|---|
| DataSF Building Footprints, LiDAR-derived (`data.sfgov.org/resource/ynuv-fyni`) | The authoritative footprint polygon (380.1 m2), the 2010 LiDAR height statistics, ground elevation 10.09 m NAVD88 |
| OSM way 113645689 → [113545689](https://www.openstreetmap.org/way/113545689) | Independent footprint (377.2 m2, agrees within 1%), `addr:housenumber=101`, `addr:street=South Park`, `height=6` |
| OSM node [10874867174](https://www.openstreetmap.org/node/10874867174) | The Kleiner Perkins POI at this address |
| SF Assessor Historical Secured Property Tax Rolls (`wv5m-vpq2`) | `property_location = 0000 0101 SOUTH PARK`, block/lot, `year_property_built = 1947`, `number_of_stories = 2`, `use_definition = Commercial Retail` |
| SF Building Permits (`i98e-djp9`), 28 permits 1988–2024 | Storey count over time; the 1989–1992 restaurant era; the 2012–2016 office fit-out including a new flat skylight; the 2014 four-ply "cool" Title-24 roof over the entire building; the 2018 "kleiner perkins" sign; the 2024 conference-room remodel |
| [Office Snapshots, "South Park Venture Capital Firm Offices"](https://officesnapshots.com/2026/02/03/south-park-venture-capital-firm-offices-san-francisco/) | Perkins&Will, 2023, 16,420 sq ft, and the exterior sentences that do **not** match the photographs (§6) |
| Google Street View, South Park pano, capture **January 2025**; Google place record "101 S Park St" | The front elevation in §4, and the address confirmation |
| Google Maps satellite (Vexcel imagery, 2026) | The roof layout in §4 |
| [Kleiner Perkins brand assets](https://www.kleinerperkins.com/brand-assets/) | The published logo set is white / black / stacked / wordmark only — the identity is **monochrome**, with no brand colour to apply |
| OSM way [24052083](https://www.openstreetmap.org/way/24052083) (South Park) | Which way the building faces: the park's long axis runs at bearing 45.0° and its centroid lies 41 m to the north-northwest |

## 3. Verified dimensions, location and orientation

Footprint measured from the DataSF polygon, reprojected with the app's tangent projection
(lon0 −122.4375, lat0 37.77) and reduced to a minimum-area oriented bounding box.

| Quantity | Value | Confidence |
|---|---|---|
| Footprint area | 380.1 m2 (OSM cross-check 377.2 m2) | measured |
| Oriented bounding box | 13.07 m x 29.70 m | measured |
| Anchor (OBB centre) | lon −122.3937582, lat 37.7812624 | measured |
| Front (South Park) outward normal | 318.3° — northwest | measured |
| Northeast flank outward normal | 44.3° | measured |
| Rear outward normal | 134.5° | measured |
| Southwest flank outward normal | 224.9° | measured |
| Ground elevation | 10.09 m NAVD88 | measured (the app's terrain handles this, not the asset) |
| Parapet crest | ~10.0 m | **estimated** — photogrammetric, ±0.8 m |
| Tallest roof feature | ~10.9 m | **estimated** — reconciled with the 2010 LiDAR maximum of 10.92 m |

Footprint polygon as built, in Blender coordinates (metres, +X east, +Y north), CCW,
centred on the anchor:

```
(  6.037, -15.039)   south corner
( 15.195,  -5.708)   east corner
( -5.419,  14.435)   north corner
(-14.967,   5.868)   west corner
```

The survey draws the southwest boundary as four segments and puts a 0.077 m chamfer at the
west corner; those points are collinear to within 0.18 m and are merged here into a single
wall and a single vertex. The resulting quadrilateral is 378.2 m2 against the survey's
380.1 m2 — 0.5% — which is far inside the contract's tolerances and much healthier for the
bevel pass than four near-parallel walls.

## 4. What each side shows

**Northwest — South Park front (12.83 m).** The hero elevation and the only one with usable
ground-level photography. Flat charcoal / dark warm-gray stucco in two clearly separated
registers:

- Ground floor: a row of tall window bays in **warm natural oak frames**, each three narrow
  vertical lights under a horizontal transom, in a plain reveal, with frosted or shaded
  glazing behind. Four such bays are visible. At the northeast end of the front there is a
  single oak-framed glazed entrance door in a shallow recess, with a small dark `101` plate
  above it and a discreet sign beside it. Two slim black gooseneck lamps are mounted on the
  wall above the openings.
- Upper floor: the wall runs blank for a deep band, then a **continuous ribbon window in
  dark metal frames, recessed roughly half a metre behind the front plane**, so the parapet
  and the two end piers read as a thin frame around a rectangle of shadow.
- Parapet: a plain flat coping. No cornice, no ornament, no signage.

One colour and one accent: charcoal, and oak.

**Northeast flank (28.82 m), toward Jack London Alley.** Faces an open paved strip, so it is
genuinely visible in the real world and unavoidably visible to the app's camera. No usable
ground-level photography was found — Street View coverage on the alley could not be reached
during this pass. *Inferred*: the same charcoal stucco with a sparse, regular scatter of
openings.

**Southwest flank (29.63 m).** Shares a boundary with 117 South Park; effectively a party
wall for its whole length. *Inferred*: blank charcoal stucco.

**Southeast — rear (13.07 m), toward Varney Place.** No usable photography. *Inferred*: a
service elevation, blank apart from a door and a few openings.

**Top.** The best-evidenced surface after the front, and the one the app's camera sees most.
2026 satellite imagery shows a light, near-white membrane roof — consistent with the 2014
four-ply "cool" Title-24 re-roof permit — inside a continuous parapet, with a dense cluster
of dark mechanical units and bright skylights grouped toward the **northwest (front) third**
and a thinner scatter down the rest of the length. The neighbouring roof to the southwest is
a distinctly different terracotta red, which is a useful check that the pale roof really is
this building.

## 5. Recognition cues, ranked

0. **It is the Kleiner Perkins office**, and the wall sign is the thing a person points at.
   SF permit 2018 records exactly one single-faced, non-illuminated wall sign reading
   "kleiner perkins"; the January 2025 pano shows it as a small plaque beside the entrance,
   alongside a `101` street-number plate over the door.
1. The row of **warm-oak shopfront windows on a charcoal wall** — the only warmth on the
   building and what identifies it at a glance
2. The **recessed dark upper storey** behind a plain parapet frame: solid band, shadow band,
   cap
3. The narrow 13 m front on a 29.7 m deep plan, on the ~45° SoMa heading
4. Total absence of ornament, colour or signage — deliberate restraint next to noisier
   neighbours
5. The big pale flat roof with its skylight and mechanical cluster, seen from above

## 6. Uncertainties and conflicting evidence

**Height — the weakest number here.** Three measurements exist and none of them is today's
crest:

| Measurement | Value | What it actually is |
|---|---|---|
| OSM `height` tag | 6 m | matches the 2010 LiDAR median; describes the pre-renovation building |
| DataSF LiDAR median (2010) | 5.56 m | mean 5.80, std 0.87, majority 5.39 — i.e. **almost the whole roof was at ~5.5 m in 2010** |
| DataSF LiDAR maximum (2010) | 10.92 m | a small element standing about a metre above where the parapet is today |

Every current photograph shows a full two-storey building, so the second storey as it stands
postdates the 2010 LiDAR and every LiDAR-derived *median* for this lot is stale. The build
adopts a parapet crest of 10.0 m (photogrammetric, ±0.8 m) with the tallest roof feature at
10.9 m, which makes the LiDAR maximum meaningful again instead of forcing a choice between
the two figures. See `REPORT.md` §"Corrections to the dossier".

**Storey count over time.** Permits record 1 existing storey through 1994 and 2 from 2002
onward. The assessor roll says 2 storeys, built 1947. The architect's copy says "originally
built in the 1920's". Two storeys is what gets built; none of the dates is treated as
established.

**The Office Snapshots exterior description does not match the photographs.** It calls the
building "brick-clad" with "large, arched metal-clad windows". The January 2025 front
elevation is charcoal stucco with rectangular oak-framed windows and no arches at all. The
most likely reading is that the copy describes the interior's salvaged brick and its
internal arched openings. No brick and no arches were modelled on that sentence's authority.

**16,420 sq ft does not fit on this lot.** Two storeys on 380 m2 is about 8,200 sq ft — half
the published area. Either the tenancy spans the neighbouring structure to the southeast
(DataSF records separate, taller footprints `SF3775179` and `SF3775016` on that side) or the
figure counts something else. AGENTS rule 5 settles the response: the addressed building is
modelled on its own measured footprint, and the discrepancy is recorded rather than resolved
by guessing.

**Does the second storey run the full depth?** Unresolved. The 2010 LiDAR says one small
element was tall and the rest was low; the 2026 satellite roof appears to change level
partway along, but not clearly enough at the resolution available to place a step. The build
takes the conservative reading — one clean volume at full height — and records it as a
decision, not a finding. This is the item most worth a second look before integration.

**Three of the four elevations are inferred**, and the four-bay rhythm on the front is read
from a single pano with part of the elevation outside the frame.
