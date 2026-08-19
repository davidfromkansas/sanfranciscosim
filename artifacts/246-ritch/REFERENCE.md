# 246 Ritch Street — reference dossier

Compiled 18 August 2026 for `artifacts/246-ritch/`. Everything here was verified in this
session against primary data; where this contradicts `docs/asset-plans/246-ritch.md`, **this
file wins** and the correction is repeated in `REPORT.md`.

The plan's dossier was written in the same session as this build, so there are no inherited
errors to correct — but the plan's own §2.15 flagged four things as unverified, and this file
records what the build actually did about each.

---

## 1. What the building is

A **five-storey, nineteen-unit apartment building over a ground-floor commercial space and
garage**, completed **6 February 2014**, on the south-west side of Ritch Street mid-block
between Bryant and Brannan in East SoMa. Marketed as **"Ritch Street"**; the ground floor is
the restaurant **Wabi-Sabi SF**, permitted in 2014 as a retail bakery at *240 Ritch* and
converted to a full restaurant in 2021.

The site was a 4,130 sq ft single-storey warehouse "in very poor structural condition… does not
contain a roof or north-facing wall", demolished 2007–2011. The replacement was entitled in
2009 as nineteen SRO units of about 350 sq ft each and built as nineteen ordinary dwellings.

## 2. Sources and what each establishes

| Source | Establishes |
|---|---|
| OSM **way/1174904714** | the footprint — `building=yes`, **no address tags**. 16.68 x 22.70 m, 378.5 m2, eight vertices all within 0.05 m of a clean rectangle |
| OSM node 10874867132 | `Wabi-Sabi SF`, `amenity=restaurant`, `addr:housenumber=246`. **This is what Nominatim returns for the address** — a point, not a building |
| DataSF Addresses `ramy-di5m` | 39 rows: twenty condominium lots `#1–#20` on block 3776 lots **456–475**, and nineteen dwelling numbers `#101`, `#201–205`, `#301–305`, `#401–404`, `#501–504`. The floor prefixes are the cleanest proof of five storeys anywhere in the record |
| DataSF Parcels `acdm-wktn` | lots 456–475 all carry the *identical* polygon (16.7 x 23.9 m); lot 456 spans addresses **240–246** |
| DataSF Footprints `ynuv-fyni` | `SF3776456` / `201006.0009413`: 395.4 m2, `hgt_median_m` **15.87**, `hgt_maxcm` **18.76**, sd 3.84 m, range 3.99–18.76 m, `gnd_min_m` 4.85. `p2010_zminn88ft = p2010_zmaxn88ft = 0` — nothing stood here in the 2010 survey |
| SF Assessor `wv5m-vpq2` | 2014; one `CZ` Commercial Store Condo (477 sq ft) and nineteen `ZEU` Condominium Economic Units of 393–453 sq ft, 8,387 sq ft total |
| DBI Permits `i98e-djp9` | **`200701051074`** "to erect a new 5 story 19 dwelling unit", completed 2014-02-06; `200701051070` / `201011164996` demolition; `201308094016` "new 19-unit plus commercial space condominium"; `M475367` / `201405095355` the 240 Ritch bakery fit-out; `202111122308` the 2021 restaurant conversion |
| SocketSite, 25 Aug 2009 — quotes the preliminary mitigated negative declaration in full | 4,130 sf site; **"a new five-story, 50-foot-tall building with 19 Single Room Occupancy (SRO) residential units totalling approximately 16,442 gross square feet"**; ~350 sf per unit; 8,690 gsf common/circulation/garage/storage; ground-floor garage of four spaces + one car-share + six bicycle spaces; **three new street trees**; SLI zoning, 55-X height and bulk district |
| SocketSite, 28 Sep 2012 | lot excavated; repeats five storeys / 50 ft / 19 units |
| ritchstreet.com, marketapts.com | the building's own leasing sites: "floor to ceiling windows", "Balcony/Patio", "Covered Parking" |
| Google Street View, historical panos | the facade. **Current captures are useless** — the three project street trees have grown into a continuous canopy. Used: `1EVAdp1_sD5des1l6a3eeQ` (widest clear view), `2dq2zz3CSqlPIJQRF03q4Q` (sharpest colour, shows the "246" plate, lobby and garage door), `Ygw6B2E0AIVV9jLc04IjdQ` (oblique from the SE), `3Z7LwIFTgVxxujqZ-y0Jpw` (the vacant lot, pre-2011) |
| Google Maps satellite z22 (Vexcel, 2026) | cream membrane roof, continuous parapet, a raised light-coloured block near the roof centre casting a clear shadow, a darker cross-shaped area around it, scattered mechanical units, and the balcony boxes legible in plan along the north-east edge |
| `pipeline/data/streets_datasf.geojson` | the street-side measurement (§4) |

Consulted and **not used**: Nominatim's geocode (returns the restaurant node); Accela planning
records `08HIS-0229P` and `13HIS-0032X` (no design content online); permit-aggregator sites
naming "Edmund Lai" and "D and S Leong Associates" — **no primary source confirms an architect
and none is claimed here.**

## 3. Verified dimensions and location

| Item | Value | Confidence |
|---|---|---|
| WGS84 anchor | `-122.3958481, 37.7802253` | **measured** — OSM oriented-bounding-box centre; the area centroid agrees to 1 cm |
| Footprint | 16.68 m (Ritch frontage) x 22.70 m (depth), 378.5 m2 | **measured** |
| Parapet / roof deck | **15.87 m** | **measured** (DataSF LiDAR median; modal cell 15.72 m) |
| Crest | **18.76 m** | **measured** (DataSF LiDAR maximum); *attributed* to the stair/elevator penthouse — see §7 |
| Entitled height | 50 ft = 15.24 m to the roof | published (2009 MND) |
| Photogrammetric parapet | 15.0 ± 1.0 m | **independently measured**, §4 |
| Floor-to-floor | 3.115 m over four residential floors; 3.40 m ground floor | *derived*: 3.40 + 4 x 3.115 = 15.87 exactly |
| Ground elevation | 4.85 m min / 5.43 m median NAVD88 | measured — the app's terrain handles this, not the asset |

## 4. Orientation, measured twice

**Street sides**, from perpendicular offsets of the DataSF street centrelines:

| Street | Distance | Bearing from the anchor |
|---|---|---|
| **Ritch St** | **17.9 m** | **45.1°** (north-east) |
| Zoe St | 39.6 m | 225.1° |
| Bryant St | 86.9 m | 315.2° |

**Control:** the same script pointed at the shipped `500-third` anchor returned 3rd Street
45.2°, Bryant 315.3°, **Ritch 225.1°** — exactly what `artifacts/500-third/build_500_third.py`'s
`E_THIRD` / `E_BRYANT` / `E_RITCH` comments say. 500 Third and 246 Ritch face each other across
the alley and therefore carry opposite normals; that is agreement, not contradiction.

Footprint edges, in build coordinates (metres from the anchor, +X east, +Y north), CCW:

```
north (2.18, 13.87) -> west (-13.98, -2.07) -> south (-2.19, -13.87) -> east (13.97, 2.07)
```

| Edge | Length | Outward normal | Elevation |
|---|---|---|---|
| east -> north | 16.68 m | **45.0° NE** | **Ritch Street front** |
| north -> west | 22.70 m | 315.0° NW | party wall, 230/236 Ritch |
| west -> south | 16.68 m | 225.0° SW | rear, over the yard |
| south -> east | 22.70 m | 135.0° SE | party wall, 248–250 Ritch |

**Photogrammetric check.** Pano `1EVAdp1_sD5des1l6a3eeQ` sits 7.86 m out from the facade plane
and 9.14 m along it from the north corner. Reprojecting its equirectangular tiles onto the
facade plane (horizon = centre row, camera 2.5 m) gives a metric elevation on which the parapet
lands at **15.0 m**, the base band at **3.3 m**, and the three balcony rows at deck heights of
roughly 3.5, 6.6 and 10.4 m. `dh/dD = tan θ ≈ 1.8` at the parapet, so the assumed camera
distance dominates the error — quote 15.0 ± 1.0 m. It brackets both the 15.24 m entitlement and
the 15.87 m LiDAR median, which is why the model takes the LiDAR value.

## 5. What each side shows

**North-east — Ritch Street, the hero elevation, 16.68 m wide.**

- a **charcoal ground-floor base band to ~3.4 m**, one constant height across the whole
  frontage. Within it, from the south-east end: a **white sectional garage door** scored into a
  3 x 3 grid of square panels; the **recessed residential lobby**, a glazed door set back in a
  charcoal reveal; the white **"246"** plate on the pier; and the **restaurant shopfront**, a
  tall glazed bay with a pale surround;
- **floors 2–5** in warm off-white stucco, articulated as **cream piers and spandrels
  alternating with charcoal-grey recessed window bays**. The recesses do **not** line up floor
  to floor: they step sideways, so the wall reads as an interlocking patchwork;
- **balcony boxes** on floors 2, 3 and 4 — cantilevered ~1 m, with a near-black perforated
  metal screen about 1.1–1.3 m high. The perforation is a scatter of short horizontal slots;
- **floor 5 carries no balconies**, so the top of the building is a clean band;
- a **dark coping band** ~0.4 m deep caps the parapet. No cornice, no step, no ornament.

**South-east** — party wall against 248–250 Ritch (`SF3776105`, 7.95 m median / 14.27 m max).
The lower ~8 m is buried; the upper ~8 m stands clear and carries a punched window rank.

**North-west** — party wall against 230/236 Ritch (`SF3776144`, 10.75 m median / 17.87 m max).
Mostly covered; blind.

**South-west (rear)** — faces a ~1.2 m rear yard and then the Zoe Street lots (`SF3776128`,
14.42 m, 19.3 m away). Windows; balconies unconfirmed (§7).

**Top** — flat cream membrane inside a continuous parapet. A **stair/elevator penthouse** near
the centre standing ~2.9 m proud and casting a clear shadow in the 2026 aerial; a darker
cross-shaped **lightwell / roof-deck** area around it; scattered **mechanical units**.

## 6. Recognition cues, ranked

1. **The staggered grid of near-black balcony boxes** on a pale front — dark rectangles that
   step sideways floor to floor. Survives to thumbnail size; exists nowhere else on the alley
2. **Cream body over a charcoal base**, the base band at one constant height — a hard
   horizontal shadow line at 3.4 m
3. **Being the tallest and newest thing on the block face** at 15.87 m: eight metres above
   248–250 (7.95 m) and 252–254 (8.04 m), five above 230 Ritch (10.75 m)
4. The **cream/charcoal interlocking panel patchwork** of the upper wall — offset, not gridded
5. The **rooftop penthouse** at 18.76 m, the only break in an otherwise dead-flat parapet

## 7. Uncertainties and what the build did about them

1. **The 18.76 m crest is a penthouse — attributed, not observed at street level.** What is
   measured is the LiDAR maximum. It is read as a stair/elevator bulkhead because the 2026
   nadir aerial shows a raised light block near the roof centre with a shadow, a five-storey
   19-unit building has an elevator and therefore an overrun, and 2.9 m above the roof is
   exactly a bulkhead. It is **not** vegetation: `peak_1st_m` (23.96) minus `gnd_min_m` (4.85)
   is 19.11 m, within 0.35 m of `hgt_max`, so there is no canopy over this footprint.
   **Built as a penthouse**; it sets the bounding-box top and therefore `targetHeightM`.
2. **~13% of the LiDAR ring is at ~4.5 m.** sd 3.84 m and a 3.99 m minimum say roughly 50 m2
   of that ring is one storey high. A three-level fit (15.87 over 82%, 18.76 over 5%, 4.5 over
   13%) reproduces the published mean (14.61) and sd (3.88) almost exactly. What it *is* is
   unresolved — a low rear portion, or the LiDAR ring over-reaching onto the rear yard and the
   neighbours' low roofs. **The build sides with OSM (378.5 m2) and the surveyed lot
   (383.7 m2), which agree with each other against the LiDAR ring (395.4 m2), and models no
   step.** If a photograph of the rear ever surfaces showing one, model it then.
3. **Rear balconies: not built.** The nadir aerial shows a second row of dark rectangles along
   the south-west edge. They are plausibly balconies matching the front's, but the rear is not
   photographable from any street and the aerial is off-nadir enough that they could be roof
   equipment. Windows only.
4. **The balcony grid: three rows of three, floors 2–4.** This is the metric reprojection of
   `1EVAdp1_sD5des1l6a3eeQ`, which shows balcony decks at ~3.5, 6.6 and 10.4 m and a clean
   band of wall with windows and no balconies across the whole frontage at 12.4–14.6 m. The
   obliques are consistent. The uncertainty is the right-hand ~2 m of the frontage, behind a
   tree in every capture. **Nine balconies built**, each floor skipping a different bay.
5. **No architect is named.** Two names recur in permit-agent aggregations and neither has a
   primary source. `REFERENCE.md` names none.
6. **No unobstructed photograph of the facade exists after ~2019.** Every facade fact here comes
   from the 2015–2019 historical panoramas.
