# 169 Steuart Street — Army & Navy YMCA Building — reference dossier

Compiled 18 August 2026 for `artifacts/169-steuart/`. The asset plan
(`docs/asset-plans/169-steuart.md`) is the head start; everything below was
re-verified for this build, and the corrections are called out explicitly.

## 1 What the building is

The **Army & Navy Y.M.C.A. Building**, completed **1924**, opened **1926**. Today it
holds two tenants inside one structure: the **Embarcadero YMCA** at **169 Steuart
Street** and the **Harbor Court Hotel** (131 rooms) at **161–165 Steuart Street**. Its
ceremonial address is **166 The Embarcadero**, which is where the entry front is.

Ten storeys of clay brick and terra cotta over a rusticated cast-stone base, Spanish
Colonial / Renaissance Revival with late Italian Gothic and Moorish detailing. A San
Francisco Point of Historical Interest and a Historic Resource — the 2013–2018 facade
restoration by McGinnis Chen Associates needed a Certificate of Appropriateness.

**Architect: disputed.** NoeHill and the AIA lists credit **Frederick H. Meyer**; the
original plans held by the YMCA are **signed by Carl Werner**. Recorded, not resolved;
it changes no geometry.

## 2 Scope — one parcel, three OSM ways, one building

This was settled before modelling and it is the most consequential decision here.

| | |
|---|---|
| DataSF parcel `3715028` | `from_address` 161, `to_address` 165 — Harbor Court |
| DataSF parcel `3715029` | `from_address` 169, `to_address` 169 — Embarcadero YMCA |
| Both | **the same `mapblklot` 3715028, the same polygon, the same building** |

OSM traces the same outline as three ways — `32862485` "Army and Navy Y.M.C.A. Building"
(810 m²), `193054138` "Harbor Court Hotel" (453 m²), `193054131` "YMCA" (200 m²) —
summing to 1,463 m² against the parcel's 1,767 m² and the DataSF LiDAR footprint's
1,619 m². They are one surveyed building drawn in pieces. **The asset is the whole
parcel.** Modelling 169 Steuart as the 200 m² OSM stub would have produced a 20 × 20 m
three-storey box where a 42 × 42 m ten-storey landmark stands, and `excluded()` in
`pipeline/buildings.mjs` could not have cleared the rest of the lot for it.

No sibling in the Embarcadero batch falls inside the parcel's 161–169 address range
(`121-steuart` and `131-steuart` are other parcels).

## 3 Measured geometry

| Quantity | Value | Source |
|---|---|---|
| Anchor | `-122.3919821, 37.7926993` | DataSF parcel polygon centroid; the minimum-area OBB centre agrees to 0.01 m |
| Footprint | 42.35 × 41.84 m OBB, 1,766.9 m² | DataSF `acdm-wktn` |
| Shape | a 45.1°-rotated square with a 5.84 m chamfer at the east corner | ibid. |
| Heading | Embarcadero front **45.1° NE**; Steuart front **225.1° SW**; party edges 134.9° SE and 314.9° NW | derived |
| Ground | 3.62 m NAVD88 median, 0.62 m range — flat | DataSF `ynuv-fyni` `gnd_*` |

Footprint in Blender metres, CCW, centred on the anchor:

```
A ( 0.15,  29.76)   north corner   — Embarcadero × Hotel Griffon line
E (-29.69, -0.17)   west corner    — Steuart × Hotel Griffon line
D (-0.15, -29.76)   south corner   — Steuart × 177 Steuart line
C ( 25.56, -3.97)   chamfer end
B ( 29.69,  0.16)   east corner
```

## 4 Height — four sources, one building

DataSF LiDAR footprint `sf16_bldgid` **201006.0001651** (2010 flight, 6,312 cells at
50 cm):

| Statistic | Value |
|---|---|
| `hgt_maxcm` | **46.64 m** |
| `hgt_majoritycm` (mode) | 28.14 m |
| `hgt_median_m` | 26.09 m |
| `hgt_meancm` | 24.90 m |
| `hgt_stdcm` | **7.40 m** |
| `peak_1st_m` | 50.35 m |

These reconcile onto one three-level building and nothing has to be discarded:

* **28.14 m** ÷ the survey's **8 storeys** = 3.52 m floor-to-floor. The wings.
* **35 m / 10 floors** (SKYDB) = 28.14 + 2 × 3.5. The tower's **eave**, not the building.
* **46.64 m** is 11.64 m above that eave. The tile roof measures ~18 m across in the z21
  aerial, so an 11.64 m rise over a ~9 m half-span is a **~52° hip** — which is what a
  Spanish tile hipped roof is, and what the photographs show.
* **50.35 m** first-return peak is 3.7 m above the crest: the **flagpole**, visible in
  every Embarcadero photograph. Not canopy — nothing overhangs this roof.

**The sd test passes rather than fails.** 7.40 m of spread over a 46.2 m range is a
genuinely multi-level building, unlike 592 Third (0.64 m sd, max was a street tree) or
250 Van Ness. An illustrative three-level fit — 28% of cells at ~14 m, 65% at 28.14 m,
7% spread across a 35 → 46.64 m pyramid — reproduces the observed mean (24.90 m) and sd
(7.40 m) to two decimals. That is a consistency check on the massing, **not** a
measurement: three moments do not uniquely invert to area fractions.

### Street View photogrammetry (independent)

Levelled equirectangular panorama **`FWxuTLcC1ZB4mrrB42U-3w`** on The Embarcadero.
Solving the perpendicular distance to the entry facade from the surveyed parcel gives
**34.65 m**; the sidewalk line then falls **47 px below the equirect centre row**, which
for a 2.5 m camera puts the horizon at **exactly row 1024 of 2048**. Panorama and parcel
agree to ~5 cm, so the elevation angles are trustworthy. Read off that calibration:

| Feature | Pano row | Height |
|---|---|---|
| sidewalk at the facade | 1071 | 0 m |
| top of the cast-stone base / corbel frieze springing | 896 | **9.60 m** |
| Embarcadero crest parapet | 581 | **30.87 m** |
| arcade band, sills → head (tower front wall, v ≈ 3 m) | 598 → 573 | 32.1 → 34.6 m |
| tile-roof ridge (tower centre, v ≈ 11 m) | 544 | **44.9 m** |

The arcade result independently lands SKYDB's 35 m eave; the ridge result brackets the
LiDAR's 46.64 m to 1.7 m. **The LiDAR number is the one shipped.**

**The Steuart-side panorama does not calibrate.** `G8fvDCDD0sBmDoPfbEjThA` puts its own
horizon ~34 px off the centre row and disagrees with the surveyed geometry by a factor of
two on distance. Its reported lat/lon cannot be trusted — the failure mode the repo's
Street View recipe warns about. Every metric statement here comes from the Embarcadero
panorama. Steuart heights are storey counts, not measurements.

## 5 What each side shows

The 1976-era survey text (quoted in the sftrajan Flickr caption) is the authority:

> "This structure covers the width of the block from the Embarcadero to Steuart Street on
> the 1st 2 floors. In its higher elevations it is divided into 2 wings, each 8 stories
> high. The entry wing, facing the bay, is the hallmark of the structure with its handsome
> brick facade, arched windows, and ornate balconies and decorative concrete crests.
> Decorative details abound at the base and at the 8th floor. … A typical renaissance
> feature is the 10 story arcaded tower, with red tiled roof, that tops the building's
> middle portion."

**Northeast — The Embarcadero (41.81 m).** Two-storey rusticated light cast-stone base to
9.60 m with tall shopfront-scale openings and a round-headed main portal flanked by
polychrome terra-cotta shields; small round-headed windows at the second level; a
**corbelled bracket frieze** carrying the "ARMY AND NAVY Y.M.C.A." inscription; five brick
storeys of regular punched windows on shallow piers; a taller **eighth storey of tall
arched windows** with terra-cotta archivolts and a balustraded balcony across the centre;
a cornice; and a **decorative crest parapet at 30.90 m** over the end bays and the centre.

**Centre of that wing — the tower.** Rising above the 28.14 m wing roof: one rank of
windows, then the **arcade band** (small round-headed openings) to an eave at **35.00 m**,
then the **red clay tile hipped roof** to **46.64 m** with a finial and a flagpole.

**Southwest — Steuart Street (41.81 m, the 169 address).** A **three-storey street wall
only**, ~14 m. Northwest half (161–165, Harbor Court): cream stucco, gently curved
parapet, large round-arched second-storey openings, projecting bay windows, small paired
arched attic windows, a dark restaurant frontage and a canopied hotel entrance. Southeast
half (169, Embarcadero YMCA): dark red-brown brick, bay windows in deep square reveals, a
flat parapet, the "Embarcadero YMCA" entrance under a black fascia and a projecting YMCA
blade sign. **The eight-storey mass sits 12.7 m behind this wall.**

**Southeast (36.42 m + a 5.84 m chamfer).** Party edge to 177 Steuart / 188 The
Embarcadero — a 1986 blue-glass office block at 32.9 m. Brick, sparse windows onto the
light well. *Inferred.*

**Northwest (42.27 m).** Party edge to the 26.4 m Hotel Griffon, but **an open yard with
surface parking interrupts it**, leaving real brick wall exposed to the full 28 m for part
of its length. Visible in the z20 aerial. Brick with a sparse window rhythm. *Inferred.*

**Roof.** The tile hip over the middle of the bay-facing wing; light grey flat roofs on
the two eight-storey wings; a light court between them; a lower podium roof across the
Steuart third with mechanical plant, a stair bulkhead and a panel array; crest parapets
standing proud along the Embarcadero edge.

## 6 Recognition cues, ranked

1. The **red clay tile hipped roof**, 18 m above every parapet on the block. The only
   sloped roof and the only saturated red for two blocks.
2. The **arcaded tower storey** under it.
3. **Red-brown brick over a pale two-storey stone base**, split by the corbel frieze.
4. The **42 × 42 m block-through square** — no other asset in this batch fills its parcel.
5. The **three-storey Steuart street wall** stepping down from the eight-storey mass,
   split cream stucco / dark brick between the two entrances.

## 7 Simplified deliberately

* Individual corbel brackets → one rank of 24 blocks under a moulded band.
* Arcade arches → a recessed band with square-cut reveals. At the app's camera distance a
  notched band *is* an arcade, at a tenth of the triangles.
* Terra-cotta shield heraldry, balustrade balusters, brick diaper panels, the inscription
  and the Moorish lobby → colour and 2–3 cm of relief at most.
* The light court → a recessed dark panel between roof deck slabs. No booleans anywhere in
  this asset.
* **The flagpole is not modelled.** It is real and it is what `peak_1st_m` = 50.35 m sees,
  but a 50.35 m bounding box would make the loader's `targetHeightM / measuredHeight`
  scale 0.93 and shrink the whole building by 7%.

## 8 Corrections and uncertainties

**Corrected during this build (REPORT beats plan):**

* The plan's massing recipe listed the eight-storey mass as two parallel bars separated by
  a full-width court band; the arithmetic in it left a 5.6 m-deep "wing", which is not a
  wing. Built instead as **one 29.6 m-deep mass with a rectangular court notched into
  it** — 65% of the footprint at 28.14 m, which is what the LiDAR distribution actually
  supports.
* The first build left both wing flanks as 28 m of unbroken brick. They are fenestrated in
  reality (an open yard on one side, a light well on the other) and blank walls read as an
  unfinished model from three of the app's four approach angles. Added the shaft rhythm
  without ornament.
* The court initially overlapped the tower footprint (court at v = 21 m against a tower
  ending at v = 19 m). Moved to v = 24.2 m.

**Still estimated, in descending order of risk:**

1. **The podium at 14.0 m.** Three storeys counted on the Steuart street wall in Street
   View plus the LiDAR's low mode; no published figure. The survey's "1st 2 floors"
   suggests 10–11 m, the built condition today is unambiguously three storeys.
2. **The light court's size and position** (12 × 8 m at v = 24.2 m). "Divided into 2
   wings" is published; the dimensions are read off a nadir tile in which the tall walls
   are parallax-displaced.
3. **The tower's plan size** (18 × 16 m). The z21 tile suggests ~18 m across; inverting
   the LiDAR moments suggests 11–13 m. Parallax inflates the first and three moments
   cannot uniquely invert the second. Imagery won.
4. **Bay counts** — 11 on the Embarcadero, 9 on Steuart — are read off obliquely-shot
   panoramas partly occluded by palms. The most likely place for the model to be visibly
   wrong.
5. **Both party elevations** are inferred in detail.

## 9 Sources

| Source | Establishes |
|---|---|
| DataSF EAS `ramy-di5m` | 155 / 161 / 165 / 169 / 177 Steuart and their parcel numbers |
| DataSF parcels `acdm-wktn` | one `mapblklot`, one polygon, address range 161–169 |
| DataSF footprints `ynuv-fyni` (`201006.0001651`) | every height and the ground plane |
| DataSF assessor `wv5m-vpq2` | **nothing** — lots 028/029 are tax-exempt and record 0 storeys, 0 area |
| OSM ways `32862485`, `193054138`, `193054131`, `193054133`, `32862467` | the three sub-outlines and the neighbours; `roof:shape=pyramidal` |
| `mcaia.com/portfolio/embarcadero-ymca/` | "10-story structure clad in clay brick masonry and terra cotta", 1924, Historic Resource, the 2013–2018 restoration scope |
| `noehill.com/architects/meyer/embarcadero_ymca.asp`, `.../poi_embarcadero_ymca.asp` | 1924, 165 Steuart, Meyer attribution, Point of Historical Interest |
| `flickr.com/photos/sftrajan/14300648310` | the survey description quoted in §5; the Carl Werner attribution |
| `historichotels.org/us/hotels-resorts/harbor-court-hotel/history` | opened 1926, Spanish Colonial Revival, arched entries, terracotta carvings, clay tile roofing, 400 original rooms — *marketing copy, dates conflict* |
| `skydb.net/building/340008031/` | 35 m, 10 floors, 1924, Spanish Revival |
| `ymcasf.org/about/history/` | the Army Navy YMCA lineage (its 1908 date is the predecessor institution) |
| Street View `FWxuTLcC1ZB4mrrB42U-3w`, `TuYMi4-QojLiDd-oC9Dv0Q`, `NDWWz4KU4P14-5Ai7OfXPw`, `22UuCDNweuX1HZv-SgvwxQ`, `G8fvDCDD0sBmDoPfbEjThA` | the four elevations and the photogrammetry |
| Google satellite z20/z21 over `37.79265,-122.39195` | tile-roof plan shape, light court, podium step-down |

Research was run through the `exa` MCP server (`web_search_advanced_exa`) in three
passes — building history, facade/roof photography, architect attribution. Photographs
were not downloaded; the URLs above are recorded so the imagery can be reopened.
