# 541 Presidio Boulevard — reference dossier

Research behind `541-presidio.glb`. Built from `docs/asset-plans/541-presidio.md`,
with every number in that plan re-verified here before modelling. Where this
document and the plan disagree, this document is right and `REPORT.md` records why.

## What the building is

Building 541 in the Presidio of San Francisco: a two-storey officer's family
quarters, one of **twelve near-identical houses numbered 540–551** strung along the
curve of Presidio Boulevard where it climbs a forested hill southeast of the Main
Post, in the area the Army called the East Cantonment and the Presidio Trust now
calls East Housing. Cream stucco walls, a red barrel-tile hip roof with deep
overhanging eaves, a one-storey porch across the street elevation, stucco chimneys
through the roof. Currently in the Presidio Trust's residential leasing portfolio.

It is a contributing element of the Presidio of San Francisco National Historic
Landmark District, not an individually notable building. That is the whole design
brief: it has to read as a *type*, one house in a designed military neighbourhood,
not as a monument.

## Sources and what each establishes

| Source | Establishes |
|---|---|
| [ACHP, *Section 213 Report: Presidio of San Francisco NHL District*, 6 Apr 2009](https://www.achp.gov/sites/default/files/whitepapers/2022-12/Presidio%20(of%20San%20Francisco)%20NHL%20Section%20213%20Report_2009.pdf) | **Identity, era and materials.** Names the row explicitly and dates it to the World War I period. |
| [NPS/GGNRA, *The Presidio of San Francisco: An Architectural History* (D-31D)](https://npshistory.com/publications/prsf/arch-hist.pdf) | The Mission Revival (1910–1940) vocabulary the row belongs to, and the Queen Anne passage that has to be *ruled out* (see conflicts). |
| OSM way `288361187` (Overpass `way(288361187); out geom tags`) | Footprint geometry, 12 distinct vertices. Tags `building=yes`, `height=8`, `roof:shape=hipped`, `roof:colour=red`, `addr:housenumber=541`. |
| OSM ways `288360343`/`288361184`–`288361200` etc. | The row's membership and spacing: 540–549 on Presidio Blvd at ~25 m centres, plus the Simonds Loop cluster behind. |
| [DataSF Building Footprints (2010 LiDAR), `ynuv-fyni`](https://data.sfgov.org/resource/ynuv-fyni.json), `sf16_bldgid` `201006.0016742` | **Heights and ground.** The height authority for this asset. |
| Google Maps place page + 2026 Airbus/Maxar/Vexcel aerial imagery | Roof plan, hip geometry, the row's setting in tree cover; wall colour, two-storey reading and window pattern from place photography. Not committed to this repo. |

The load-bearing quotation, from the ACHP report's World War I section:

> An imposing row of officer housing (Bldgs. 540 – 551) located along the curve of
> Presidio Boulevard, southeast of the Main Post represent the more permanent type
> of construction completed during the period. […] The designs for the housing at
> both areas exhibit white stucco walls barrel tile roof combined with the basic
> forms characteristic at the Post.

## Verified dimensions and location

All geometry measured from the OSM ring, reprojected with the project's tangent
projection (`x=(lon+122.4375)·111320·cos(37.77°)`, `z=−(lat−37.77)·110540`) and
reduced to a minimum-area oriented bounding box.

| | Value | Confidence |
|---|---|---|
| Footprint area | 250.7 m² | measured |
| Oriented bounding box | 14.27 × 19.77 m | measured |
| Main block | 19.77 × 11.65 m | measured |
| Front porch projection | 9.68 × 1.75 m | measured extent, *inferred* function |
| Rear bay projection | 4.61 × 0.86 m | measured |
| Anchor (main-block centre) | `-122.4518601, 37.7969312` | measured |
| Ring centroid (alternative) | `-122.4518566, 37.7969294` — 0.36 m away | measured |
| Ground pad | 41.05 m NAVD88 median; min 40.50, max 41.34 | measured |
| Pad slope across footprint | 0.84 m range, 0.12 m σ — effectively level | measured |
| Roof crest above ground | **10.04 m** (`hgt_maxcm` 1004) | measured |
| Median roof height | 8.16 m (`hgt_mediancm` 816) | measured |
| LiDAR roof coverage | 992 cells at 50 cm ≈ 248 m², i.e. the whole roof | measured |
| Hip ridge | ~9.6 m | *inferred* (solve below) |
| Eave | ~7.2 m | *inferred* (solve below) |
| Roof pitch | ~20° as built | *inferred* |
| Storeys | 2 over a ~0.9 m raised plinth | *inferred* |

### The height solve

Only two roof numbers are measured: the maximum (10.04 m) and the median (8.16 m)
height above ground. Modelling a uniform-pitch hip as `h = eave + pitch · d`, where
`d` is distance to the nearest footprint edge, and computing `d` over the real ring
on a 0.1 m grid (25,149 cells, 251.5 m²) gives median `d` = 2.16 m, max `d` = 6.88 m.
Restricting to the 19.77 × 11.65 m main-block rectangle (median `d` = 2.12 m, max
`d` = 5.83 m) and solving for the eave at several assumed ridges:

| assumed ridge | implied pitch | implied eave |
|---|---|---|
| 9.4 m | 18.6° | 7.44 m |
| **9.6 m** | **21.2°** | **7.34 m** |
| 9.8 m | 23.6° | 7.25 m |
| 10.04 m | 26.9° | 7.09 m |

Every solution puts the eave at 7.1–7.4 m and the pitch inside the 18–27° band that
barrel tile is actually laid at, so the pair is well-constrained even though neither
number is published. **Built values: eave 7.2 m, ridge 9.6 m, crest 10.0 m**, which
also divides cleanly into a 0.9 m plinth plus two ~3.15 m storeys. The 0.4 m between
ridge and LiDAR maximum is read as the chimney.

### The `height=8` trap

OSM's `height=8` is within 0.16 m of the LiDAR **median** (8.16 m), not the crest.
That is what you measure if you average a hip roof between eave and ridge. Using it
would have produced a house 2 m too short with a flat top. This is the same class of
error the plans set catalogues for City Hall, St Mary's and 550 Third.

## Orientation

| | Bearing |
|---|---|
| Long axis (19.77 m) | 30.68° / 210.68° |
| Front elevation faces | **120.68°** (east-southeast, toward Presidio Boulevard) — carries the porch |
| Rear elevation faces | 300.68° (west-northwest, into the hill) — carries the shallow bay |
| End elevations face | 30.68° (toward 542) and 210.68° (toward 540) |

The footprint decomposes cleanly in the OBB frame: a 19.77 × 11.65 m rectangle, a
9.68 × 1.75 m projection centred on the 120.68° face, and a 4.61 × 0.86 m projection
on the 300.68° face. Because Presidio Boulevard runs east of the house, the larger
projection is on the street side — which is what makes reading it as a front porch
the natural interpretation.

Authored in true-world orientation (Blender +Y = north, +X = east) per
`docs/asset-plans/README.md`: `placeGeneric()` scales and positions but never
rotates, so the asset's own heading is the one it lands at.

## Observations from all four sides and above

- **Front (120.68°).** The public face and the only one with relief: the one-storey
  porch across the middle half of the 19.77 m elevation, entrance within it, two
  tiers of windows either side and above. The boulevard is ~30 m away.
- **Rear (300.68°).** Plain stucco, same two-tier rhythm, interrupted by the shallow
  0.86 m bay. Heavily screened by mature cypress and eucalyptus; in the app it will
  almost always be seen against tree cover.
- **Ends (30.68° / 210.68°).** 11.65 m hip ends, two tiers, narrower rhythm. ~29 m
  of lawn to 542, ~30 m to 540.
- **Above.** One red barrel-tile hip over the main block, ridge running
  north-northeast, the porch's separate lower hip on the front slope, stucco chimneys
  piercing the slopes, and a hard eave shadow all the way round. This is the surface
  the app's camera spends nearly all its time looking at, and in aerial imagery it is
  unambiguously the building's identity: twelve of these tile hips stepping along a
  curve through dark trees *is* the East Housing hillside.

## Recognition cues (ranked)

1. The red barrel-tile hip roof with deep overhanging eaves — ~90% of the building
   at the app's viewing distance.
2. Flat cream stucco walls, unornamented, which exist to make the roof read.
3. The one-storey front porch breaking the street elevation's base.
4. Stucco chimneys through the roof — the only vertical incident, and the crest.
5. The two-tier window rhythm, as a rhythm.
6. Domestic scale: 19.8 × 11.7 m and 10 m tall.

## Preserved / simplified

**Preserved:** the 19.77 × 11.65 m main block and the 30.68° heading exactly; the
hip and its ridge; the porch's subordinate hip; deep eaves; the chimneys, thickened;
the two-tier rhythm; the raised plinth.

**Simplified:** individual barrel tiles → flat colour; eave → one chunky fascia
band; real window counts → 5 bays per long elevation and 3 per end, all identical,
recessed 0.12 m; double-hung sashes, screens and blinds → gone (sub-pixel at city
scale); porch → a solid one-storey volume with a recessed door, no balustrade or
columns; rear bay → a plain full-height pilaster of wall; chimneys exaggerated in
section (1.00 × 0.80 m) but not in height.

## Conflicting evidence and how it was resolved

1. **Queen Anne vs Mission Revival.** The NPS architectural history's Queen Anne
   (1880–1890) section says "the cluster of large officers' quarters located at
   Funston and Presidio Boulevards represent the Presidio's version of the Queen
   Anne style". Applied carelessly, that would make this house a Victorian. It does
   not: that passage describes the 1880s quarters further up Presidio Boulevard near
   the Main Post. The ACHP report is specific, later and about *this* range —
   540–551, on the boulevard curve, WWI-era, white stucco with barrel tile roofs. The
   OSM tags (`roof:shape=hipped`, `roof:colour=red`) and the aerial imagery both
   agree with the ACHP reading. **Resolved for Mission Revival.**
2. **OSM `height=8` vs LiDAR crest 10.04 m.** Resolved above: the tag is the median,
   not the crest. **Built to 10.0 m.**
3. **Which building is 541.** The row is twelve near-identical houses at ~25 m
   centres, and image search for the address readily returns 540, 542 or 543 instead.
   Every visual observation here was checked against the building's position in the
   arc (541 is second from the south end, immediately southwest of 542, with the
   Presidio Blvd / Sumner Ave junction just south of it) before being used.

## Remaining uncertainties

Carried forward from the plan's §2.15, still open after this pass:

1. **Whether the front projection is an open porch, an enclosed sun porch, or a
   full-height projecting bay.** Modelled as a one-storey porch. The 9.68 × 1.75 m
   extent is measured; the reading is not. An enclosed sun porch would be visually
   near-identical at app scale; a full-height bay would change the roof plan (the main
   hip would cross-gable over it). This is the single most consequential open item.
2. **Chimney count and position.** Two stacks, piercing the slopes 2.6 m off the
   ridge. One central stack or three fit the 10.04 m maximum equally well.
3. **Ridge, eave and pitch are inferred**, not published. A HABS survey or elevation
   drawing of any building in 540–551 would replace three inferences with one
   measurement.
4. **Window counts are designed rhythms**, not counts off a photograph.
5. **Exact construction year is not pinned** — the ACHP report gives the period
   (1915–1918), not a year for Building 541.
6. **Duplex or single-family.** Categorised as `cat: 1` (house). Affects only the
   card chip and prop garnish, not geometry.
