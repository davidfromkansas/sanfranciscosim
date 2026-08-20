# 1 Market Street — Southern Pacific Building — reference dossier

Compiled 19 August 2026 for `artifacts/1-market/`. This dossier records what was
verified independently before modelling, and **where the asset plan
(`docs/asset-plans/1-market.md`) turned out to be wrong**. Where the two
disagree, this file and `REPORT.md` win.

## 1. Identity

| Item | Value | Source |
|---|---|---|
| Name | Southern Pacific Building; `alt_name` "The Landmark @ One Market" | OSM way/132238425; Wikidata Q7570276 |
| Address | 1 Market Street, San Francisco CA 94105 — block **3713**, lot **006** | DataSF EAS (`ramy-di5m`); SF Planning ZA letter for 1 Market Street |
| Built | started 1916, completed **1917** | Wikipedia; SF Assessor roll `year_property_built = 1917` |
| Architects | Walter Danforth Bliss and William Baker Faville | Wikipedia; noehill Bliss & Faville index |
| Storeys | **11** | SF Assessor `number_of_stories = 11.0`; SF Planning ZA letter |
| Building area | 434,396 sq ft = 40,357 m2 | SF Assessor roll 2023–2025 |
| Lot area | 38,051.62 sq ft = 3,535 m2 | SF Assessor roll |
| Use | Commercial office over ground-floor retail | SF Assessor; OSM POI node/8748507817 (Autodesk) |
| Material | Roman brick over a terra-cotta base; Italian Renaissance | Wikipedia; Street View |

**Not this building:** Spear Tower (43 storeys, 172 m) and Steuart Tower
(27 storeys, 111 m) over a 6-storey podium, both 1976–79, Welton Becket
Associates, on the neighbouring lot 3713/007. They dominate nearly all
photography captioned "1 Market Street" and are explicitly out of scope.

## 2. Height — the number the sources disagree about

Wikipedia's infobox says **65 m (213 ft)**. It is wrong, and so is OSM's
`height=60.05`. Three independent lines put the crowning cornice at **46.1 m**:

1. **DataSF LiDAR (`ynuv-fyni`, `mblr = SF3713006`, `sf16_bldgid`
   201006.0000435)** — `hgt_median` **46.12 m**, mean 45.71, modal 48.69,
   σ **5.57 m** over 15,524 cells, min 6.22 m, max 114.92 m.
   *The instrument is validated inside its own tile:* the footprint immediately
   south-east (201006.0001309) is **Spear Tower**, and its `hgt_median` is
   **172.41 m** against a published 172 m. A 0.4 m error next door is not a 19 m
   error here.
   The **maximum of 114.92 m is rejected** — σ 5.57 m over 15,524 cells cannot
   contain a 69 m step, and Spear Tower's footprint shares boundary geometry with
   this one. `peak_1st_m` 118.52 − `gnd_min_m` 3.29 reproduces it exactly, i.e. a
   first-return artefact over the shared edge.
2. **Street View photogrammetry, independent of the LiDAR.** Equirect panorama
   `9Ik_FfJfikwHnE_YlMOsRQ` on Market Street, zoom 3 (4096 x 2048). The cornice
   silhouette across the whole Market frontage fits `tan θ = K·cos φ` with
   **K = 4.0755** and a perpendicular foot at column **3096**, residual **±0.05°**
   over 1,650 columns. The two silhouette corners are **1,735 columns** apart, so
   `d = L_c / (tan φ_N − tan φ_W) = 87.5 / 8.19 = 10.68 m` to the cornice line and
   `H = 2.5 + 10.68 × 4.0755 = ` **46.03 m**. The panorama's own reported position
   is not used anywhere in that solve — only the measured frontage length.
3. **Arithmetic.** 434,396 sq ft over 11 storeys is a 3,669 m2 floor plate on a
   3,535 m2 lot. 46.1 m over 11 storeys is 4.19 m per floor, right for a 1916
   Class-A office with a two-storey giant-order base. 213 ft would be 5.90 m.

**What the asset ships at.** `targetHeightM` **48.70 m** = the rooftop plant
crest, taken from the LiDAR modal 48.69 m and corroborated by nadir imagery
showing two large fan enclosures on the Market wing. The crowning cornice sits at
46.10 m and the roof deck at 44.10 m. This follows the `300-brannan` /
`599-third` convention: the export's bounding-box top is the rooftop plant, not
the architectural height.

## 3. Plan — a U, not a box, and not an E

Wikipedia calls the plan "E-shaped". The DataSF survey is a clean **U**: one
straight court face 55.49 m long, no middle wing. Two checks agree with the U and
not with the E or with OSM:

- ring area **3,879 m2** (survey, incl. cornice overhang) against the assessor's
  **3,669 m2** per-floor plate — 5% apart, which is the overhang;
- OSM way/132238425 traces a **solid diamond of 5,544 m2 with no courtyard**. That
  is 51% more floor area than the assessor records. OSM is wrong about the plan.

In the building's own axes (u along Market toward Steuart, v from Market into the
block), origin at the surveyed west corner:

| Element | u | v |
|---|---|---|
| overall | 0 → 87.5 | 0 → 68.4 |
| Market wing | full length | 0 → 31.4 (30.25 m deep) |
| Spear wing | 0 → 15.5 | to 67.5 |
| Steuart wing | 71.0 → 87.9 | to 68.4 |
| **courtyard** | 15.53 → 71.02 | 31.40 → 68.5, **open to the south-east** |

The courtyard belongs to the **neighbouring parcel** — the atrium footprint is
`mblr = SF3713007` (201006.0001118, 2,112 m2), not SF3713006. It is roofed by the
glazed atrium of One Market Plaza.

## 4. Orientation and anchor

Anchor **-122.3948075, 37.7938412** — the axis-aligned bounding-box centre of the
simplified wall ring, which is what the loader's origin convention needs. Note the
DataSF **address point** for `1 MARKET ST` is `-122.394986, 37.793984`, about 11 m
north-west of this; it is the doorway, not the building centre, and must not be
used as the anchor.

| Elevation | Length | Outward normal |
|---|---|---|
| Market Street (front) | 85.20 m | **315.2°** NW |
| Steuart Street (flank) | 66.15 m | **45.2°** NE |
| Spear Street (flank) | 66.15 m | **225.2°** SW |
| Mission Street returns | 15.33 m + 14.38 m | **135.2°** SE |

## 5. What each face shows

Read from a **rectified elevation**: the Market pano resampled onto the wall plane
at 8 px/m using the fitted perpendicular foot and distance above, so positions
along the facade and storey bands are metric.

- **Market (NW)** — a two-storey cream terra-cotta arcade of tall round-arched
  openings between piers; a monumental arched portal at the centre with a balcony
  on scrolled brackets over it; a base entablature with balustrade; eight storeys
  of red Roman brick with small punched windows on a **2.25 m** bay; a light
  string course around the seventh floor; a colonnaded attic storey; a very deep
  bracketed crowning cornice.
- **Steuart (NE)** and **Spear (SW)** — the same treatment wrapped continuously,
  without the portal.
- **Mission (SE)** — two short returns with the courtyard opening between them.
- **Courtyard** — no photograph found. Modelled as a plainer version of the
  street elevations: the same brick and window rhythm, no terra-cotta base
  articulation, no colonnade.
- **Above** — the U-shaped deck inside the cornice parapet; two large plant
  enclosures with fan banks on the Market wing; stair bulkheads, vents, walkways;
  the glazed hip roof of the atrium filling the court.

**Bay rhythm.** The **2.25 m pitch is measured** — an autocorrelation over the
rectified elevation returns 2.25 m at two independent storey bands (2.20/2.34 m
raw peaks), and a direct peak count found 32–34 openings where street trees leave
the frontage visible. **38 / 29 / 29 / 7 / 6 follow by division** and are
*inferred*.

## 6. Sources

- `https://en.wikipedia.org/wiki/Southern_Pacific_Building` — name, architects,
  1916–17. **Infobox height 65 m and floor count 12 are both wrong.**
- `https://en.wikipedia.org/wiki/One_Market_Plaza` — the towers, i.e. what is not
  in scope.
- `https://sfplanning.org/sites/default/files/za/1%20Market%20Street.pdf` — the
  lot split and the 11 storeys.
- `https://data.sfgov.org/resource/ynuv-fyni` — footprint and every height.
- `https://data.sfgov.org/resource/wv5m-vpq2` — assessor roll, block 3713 lots
  006 and 007.
- `https://data.sfgov.org/resource/ramy-di5m` — address → parcel.
- `https://www.openstreetmap.org/way/132238425` — cross-check only.
- Google Street View pano `9Ik_FfJfikwHnE_YlMOsRQ`, zoom-3 equirect tiles
  (browser User-Agent **and** a `https://www.google.com/` referer are both
  required, or the endpoint 403s).
- Google satellite tiles z20/z21 — roof furniture and the atrium. **Markedly
  off-nadir over this block** (Steuart Tower shows its facade), so used for
  identification only; all plan geometry comes from the DataSF polygon.

No copyrighted imagery is committed here; the URLs and the derived measurements
are the record.

## 7. Uncertainties carried into the model

- **The atrium glazing height is a design decision**, not a measurement. The
  atrium's own LiDAR record (median 39.71 m, min 25.25 m, modal 27.20 m) covers
  both the glazed court and the 6-storey podium beside it, so none of those is the
  glazing alone. The asset uses eaves **35.20 m**, apex **43.50 m**, constrained
  by "clearly below the 46.10 m cornice, clearly above the 27 m podium".
- **The courtyard elevations are unphotographed.**
- **The 48.70 m plant crest** rests on the LiDAR mode being rooftop plant. If a
  roof photograph contradicts it, re-normalize to the 46.10 m cornice.
- **The bay counts are derived from a measured pitch**, not counted in a photo.
