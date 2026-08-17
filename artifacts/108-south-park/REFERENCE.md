# 108-110 South Park — reference dossier

Research behind `artifacts/108-south-park/`. The plan is
`docs/asset-plans/108-south-park.md`; this file records what was verified during
the build, what changed from the plan, and what remains inferred.

## 1. Identity

| | |
|---|---|
| Address | 108-110 South Park (South Park Street), San Francisco CA 94107 |
| Block / lot | 3775 / 059 |
| Built | 1914 |
| Storeys / units | 2 / 2 |
| Assessor use | Commercial Retail; LoopNet subtype "Storefront Retail/Residential" |
| Areas | lot 2,145 sq ft (199.3 m2); building 4,268 sq ft |
| Historic identity | former **Omiya Shoten souvenir shop and Biwako Baths**, in South Park's pre-1942 Japanese quarter |
| Recent tenant | **South Park Cafe**; ground floor papered over and vacant in the Jan 2025 pano |
| Neighbours | 104-106 South Park (Gran Oriente Filipino Hotel, 11 m, NR-nominated) attached north-east; 112 South Park (6 m) attached south-west |

## 2. Sources and what each establishes

| Source | Establishes |
|---|---|
| OSM way/124884358 | footprint (4-corner parallelogram), `addr:housenumber=108;110`, `height=8` |
| OSM way/124884343, way/124884354 | the two attached neighbours and their heights (11 m, 6 m); **both share vertices with this footprint at 0.00 m** |
| DataSF Building Footprints `SF3775059` (`data.sfgov.org/resource/ynuv-fyni`) | LiDAR roof heights: median 7.76 m, majority 7.47 m, mean 8.63 m, σ 1.46 m, max 11.88 m, min 6.22 m over 853 cells; ground 8.77 m NAVD88. Also `SF3775058` = 11.02 m and `SF3775060` = 5.73 m for the neighbours |
| SF Assessor secured roll (`data.sfgov.org/resource/wv5m-vpq2`), block 3775 lot 059 | 1914, 2 storeys, 2 units, Commercial Retail, lot and building areas |
| SF Planning case 2016-008192SRV, National Register nomination for the Gran Oriente Filipino Hotel | names 108-110 as the Omiya Shoten souvenir shop and Biwako Baths (fig. 4, c. 1915, "all three buildings extant"); the Morino family's Omiya Hotel at 108; a 1960 fire "in the adjacent building at 108 South Park Street"; and the block's building type — "two to four-story attached, mixed-use flats and multi-unit apartment buildings primarily constructed between 1906 and 1924" |
| LoopNet listing 31654148 | year built 1914; 4,000 SF gross leasable; retail/residential — *observed (listing)* |
| opengovus SF registered business 1243777-01-201 | South Park Cafe registered at 108 South Park St |
| Google Street View, South Park pano, **Jan 2025** | the entire front elevation description in §4 |
| Google Street View, Taber Place pano, **Jan 2025** | the entire rear elevation description in §4; the utility box on the rear wall is stencilled `W110 SP`, which is what confirms the rear identity |
| Google Maps satellite, 2026 Vexcel | the roof: flat, light membrane, a run of dark rectangles along the spine, no solar (the solar array visible nearby belongs to 102, The Park View) |

**No historic-resource survey, DPR 523 form or published architectural
description of this building was found.** Everything in §4 below the assessor
row is read off photographs.

## 3. Geometry, verified

Local tangent projection per `AGENTS.md` (`LON0 −122.4375, LAT0 37.77`).

- Footprint area **191.37 m2**, an exact parallelogram: **6.433 m** frontage x
  **29.750 m** depth.
- Area centroid = OBB centre = **−122.3944841, 37.7816792**.
- Corners, metres east/north from that centroid:
  `A(−12.812, +8.252)` rear-SW · `B(−8.236, +12.773)` rear-NE ·
  `C(+12.812, −8.252)` front-NE · `D(+8.236, −12.773)` front-SW.
- Front (shopfront) outward normal **135.35° true**; rear **315.35°**.
- After `recentre()` the model origin sits 0.209 m east / 0.029 m south of the
  area centroid (the awnings pull the bbox centre forward), so the
  **manifest anchor is −122.3944817, 37.7816789**.

### Height — how it was derived

The plan's 8.45 m crest survived verification and is unchanged.

- The LiDAR **median** 7.76 m over 853 cells is the roof deck. The model uses
  **7.80 m**, rounded up by 4 cm so the storey heights come out clean.
- OSM independently tags the way `height=8`, and the assessor independently
  records 2 storeys. Three sources agree on ~7.8-8 m.
- The LiDAR **maximum** 11.88 m is **not** used. It sits 2.2σ above the mean,
  and the attached Gran Oriente next door has a LiDAR median of 11.02 m — a
  party-wall cell bleeding across the shared line explains it exactly. A 4.1 m
  element above a 7.8 m deck on a 6.4 m-wide plate would be an implausible
  bulkhead, and no photograph shows one.
- The **cornice crest at 8.45 m** is `deck + 0.65 m` of boxed cornice, read off
  the Jan 2025 pano at ±0.4 m. It remains the one *estimated* number in the
  asset, and it is the bbox top.

## 4. What each side shows

**Southeast (South Park front)** — the only designed elevation, and the only one
the city sees. Bottom to top: a green bulkhead; two large plate-glass display
bays in heavy green frames with a **recessed entry at the south-west end**
(dark door, coloured leaded panel over); two **flat black awnings**; a band of
**pale leaded transom lights** with an oval motif per panel; the **gold serif
sign fascia** reading SOUTH P[ARK] CAFE across the full frontage; a belt course;
**three tall upper windows** in a shallow recessed field between flat pilaster
strips; and a **boxed cornice with a small modillion course**. No parapet above
the cornice — the cornice is the crest.

**Northwest (Taber Place rear)** — utilitarian, same paint. A wide pair of
**multi-pane glazed carriage doors** at grade, a small louvered vent above, a
galvanised downspout at the south-west edge, a security camera, and the `W110 SP`
utility box. Upper storey: a **paired double-hung window group** with light sash,
roughly centred. Flat top, plain boxed cornice.

**Northeast flank** — blind party wall against 104-106 (11 m). Never seen.

**Southwest flank** — blind party wall against 112 (~6 m), so roughly the top
1.8 m plus the parapet show from the aerial camera. No openings.

**Roof** — flat, light membrane, a run of dark rectangles (skylights) down the
spine. No solar.

## 5. Recognition cues (ranked)

1. **It is the dark green one** — the only dark object on a rim of greige, white
   and pale grey.
2. **The gold sign band** across the full frontage; the only saturated colour.
3. **The narrow-deep proportion**, 6.4 m over 29.8 m.
4. **The two black awnings**, which read as a café even in silhouette.
5. **Three tall upper windows** under a boxed cornice.

## 6. Preserved / simplified

**Preserved:** the colour on all four elevations; the frontage-to-depth ratio;
the full shopfront stack (bulkhead / glass / awnings / transom / sign); the
recessed entry at the south-west end; three upper windows in a pilastered field;
the cornice projection and its modillion course; the belt course carried round
the whole perimeter (the south-west flank shows above 112); the rear carriage
door and paired window.

**Simplified:** the sign lettering is gone (flat-colour contract, and sub-pixel
from the app's camera) — the fascia is a plain gold band. The oval leaded motifs
collapse to one pale stripe. The clapboard boards are not modelled; the belt
course is all the horizontality the walls get. The carriage door's divided
lights become one pane. The downspout, camera, utility box and vent stack detail
are dropped. The colour value is lifted two steps and the roof deck is light
(see §7).

## 7. Deliberate departures from the reference

| Departure | Why |
|---|---|
| Body green authored at **#587a66**, two steps lighter than the real paint | the real paint photographs near-black. A near-black 6.4 m sliver between an 11 m pale neighbour and a navy one reads from the air as a **gap in the row**, not a building — and at one step up (#35493e) it still rendered as a literal black slab in the running app, measured at `rgb(5,5,6)`. Style bible §7 SF exception + §29 (readability over realism) |
| `Toy_verdigris` and `Toy_mint` carry off-palette hexes | the palette has no dark green. Both keep the palette NAME so the contract check and the loader's merge path are unaffected — the precedent is 165 South Park's `Toy_steel`. **WARN, not FAIL** |
| Cornice / belt / casings in a *lighter green*, not cream | the real trim is green too. A cream cornice would be a lie that happens to be in the palette; one step lighter is what makes the crown read as articulation |
| Skylights and roof furniture sized up | §9 semantic scale — at real size they vanish from the app's camera |
| Roof deck authored as a **light** membrane (`Toy_stone` #d9d2c2) | matches the 2026 satellite imagery of this row, which the plan's original dark `Toy_roofd` deck did not. It was also what turned the asset into a silhouette in the app — reference error and rendering failure in one |
| Night state shows the shopfront lit although the unit was vacant in Jan 2025 | §16 storytelling on a building whose whole identity is its shopfront. Recorded so it is not mistaken for a research error |

## 8. Uncertainties

- **The 0.65 m cornice height is estimated** from one pano at ±0.4 m. The deck
  is measured; the crest is not.
- **The third upper window is inferred.** Two are clearly visible in the Jan 2025
  pano; the third is placed on the bay rhythm behind the large ficus that stands
  in front of this building in every recent capture.
- **The roof is a light membrane, established late.** The satellite read was only
  checked properly during stage-5 QA, after the dark deck failed visually. It is
  now the shipped roof, but it rests on one imagery source.
- **The roof skylight count and spacing are read off satellite imagery only** —
  four evenly spaced is the graphic simplification of a run of dark rectangles,
  not a survey.
- **Two footprints disagree by 14%** — OSM 191.4 m2 vs DataSF `SF3775059`
  218.8 m2 over a ragged 14-vertex ring. The assessor's 199.3 m2 lot sits between
  and much nearer OSM, and a 21 x 100 ft parcel is what a 1914 South Park lot
  should be, so the model is authored on OSM. **This matters enormously at
  integration: the bake reads DataSF, so the exclusion radius must be measured
  against the DataSF ring, not this one.**
- **The rear upper window pair is read from one very close-range pano** shot from
  ~3 m away in a 6 m alley; the count is certain, the proportions are not.
