# 542 Presidio Boulevard — reference dossier

Research behind `542-presidio-blvd.glb`. Compiled 12 August 2026. Everything not
marked **measured** or **verified** is *inferred* or *estimated* and is called out
again in §8.

The plan this executes is `docs/asset-plans/542-presidio-blvd.md`. Where this
dossier and that plan disagree, this dossier is the later word and `REPORT.md`
records the correction.

## 1. What the building is

One of a row of officers' family quarters lining Presidio Boulevard where it drops
into the Presidio. Two storeys of cream stucco on a raised base, under a low
terracotta mission-tile hipped roof with deep eaves, split front-to-back by a
tiled pent roof over a full-width recessed porch. Built during the WWI-era
build-out of the post as housing for officers' families; the group is 16 duplex
units plus 4 single-family homes. Contributing structure in the Presidio of San
Francisco National Historic Landmark District.

## 2. Sources and what each establishes

| Source | Establishes |
|---|---|
| [OSM way/288361188](https://www.openstreetmap.org/way/288361188) | **Measured** footprint (12 vertices), `height=8`, `roof:shape=hipped`, `roof:colour=red`, `addr:housenumber=542` |
| OSM API `/api/0.6/way/288361188/full.json` | The raw node geometry the footprint numbers are derived from |
| [Nominatim](https://nominatim.openstreetmap.org/) | Address resolution inside the SF bounding box; confirms 94129 / Presidio |
| [pres.house](https://pres.house/) — 544 Presidio Blvd | The identical sibling next door: 1912, 4th Cavalry officers' quarters, **cream stucco**, **low terracotta roof**, arched entry, **two working chimneys**, original **casement windows**, **two floors**, **10 ft 6 in ground-floor ceiling**, 3,400 sq ft, restored 2023. Carries a street-level elevation photograph of the type. |
| [Presidio Trust — rent a home](https://presidio.gov/rent-a-home) | The Presidio Boulevard homes are **Mission Revival**, four-bedroom duplexes and single-family houses, built for officers' families during WWI |
| Address listing for 542 (via web search) | 16 duplex units + 4 single-family homes, **built 1917**, Mission Revival, officers' family housing |
| [NPS — Presidio architecture](https://www.nps.gov/prsf/learn/historyculture/presidio-architecture.htm) | 473 of ~790 Presidio buildings are contributing historic structures |
| [NPS — Queen Anne at the Presidio](https://www.nps.gov/prsf/learn/historyculture/queen-anne.htm) | The competing Queen Anne attribution for "Funston and Presidio Boulevards" quarters — see §8 |
| [NRHP #66000232](https://noehill.com/sf/landmarks/nat1966000232.aspx) | Presidio of San Francisco NHL district, designated 1962 |
| Esri World Imagery, z20, retrieved 12 Aug 2026 | **Measured** roof form: ridge orientation, equal-pitch full hips, eave overhang, terracotta tile colour |

Reference imagery was consulted, not committed: the street-level photograph is a
Google Street View frame republished by pres.house and the aerial is Esri tile
imagery, neither of which may be redistributed here.

## 3. Verified dimensions and location

| Item | Value | Confidence |
|---|---|---|
| OSM way | `way/288361188`, 12 vertices | measured |
| Oriented bounding box | **14.01 × 19.37 m**, area 271.5 m² | measured (min-area OBB over the reprojected ring) |
| Anchor (OBB centre) | **−122.4516862, 37.7971579** | derived from measured geometry |
| Local projection | x = −1248.33, z = −3002.04 (repo tangent frame, LON0 −122.4375 / LAT0 37.77) | measured |
| Long-axis / ridge bearing | **31°** (NNE–SSW) | measured from the OBB |
| Entrance front | faces **ESE, ~121°**, onto Presidio Boulevard | inferred from street layout + aerial |
| Eave height | **8.0 m** | corroborated — OSM tag and storey arithmetic agree independently |
| Crest height | **10.6 m** | estimated — see §4 |
| Nearest neighbour | 543 Presidio Blvd, **25.1 m** centre-to-centre; 541 at 29.4 m | measured |

## 4. Height, and why the OSM tag is not it

OSM carries `height=8`. That is the **eave**, not the architectural top. Two
independent lines land on the same 8 m, which is what makes the eave reading
trustworthy and the crest a separate question:

| Component | Value | Basis |
|---|---|---|
| Raised base above grade | 1.10 m | ~6 risers at 0.18 m, observed in street photography |
| Ground floor | 3.60 m | 3.20 m **verified** ceiling + 0.40 m structure |
| Second floor | 3.25 m | ~2.90 m ceiling + 0.35 m structure (*estimated*) |
| **Eave** | **7.95 ≈ 8.0 m** | sum — matches the OSM tag |
| Hip rise | 2.60 m | over the 7.55 m half-span from eave edge to ridge (*estimated*) |
| **Crest** | **10.6 m** | eave + hip rise |

Geometry cross-check: with equal pitch on all four sides, a full hip over the
roof plan (20.5 × 15.1 m including eaves) gives a ridge of 20.5 − 15.1 = **5.4 m**,
about a quarter of the length. The aerial agrees, which is what confirms equal-pitch
full hips rather than a cross-hip.

As built, the pitch is **4:12 (18.4°)** measured from the eave edge — the value that
puts the crest at exactly 10.6 m. Mission tile needs roughly 4:12 minimum, so this
sits at the shallow end of the legal range, consistent with every description of
these roofs as "low". The honest band on the crest is **10.6 ±0.6 m**.

## 5. Orientation

The long axis and roof ridge run **NNE–SSW at bearing 31°**; the entrance front
faces **ESE at bearing 121°**, onto Presidio Boulevard, which passes to the east
and below the house — pres.house describes the lot as "a rise above Presidio
Boulevard".

The asset is authored in **true-world orientation** (Blender +Y = north, +X = east)
because `placeGeneric()` applies no rotation. The front therefore does **not** face
−Y. Per the orientation note in `docs/asset-plans/README.md`, real-world orientation
wins over the contract's "front faces −Y" rule and the deviation is recorded in
`REPORT.md`.

## 6. What each side shows

**ESE (front, onto Presidio Boulevard)** — the hero elevation. Raised base with
concrete entry steps; full-width recessed porch behind four chunky square stucco
columns with simple capitals; a solid stucco balustrade wall at rail height, not
spindles; two front doors side by side; above the porch a terracotta pent roof on a
bracketed cornice; then the upper storey with tall dark multi-pane casements and
small iron balconettes; then the deep eave and the hip roof. *Verified* from
street-level photography of the sibling next door.

**WNW (rear)** — *inferred*: plainer service side facing the rise. The aerial shows a
small projection here, read as a rear porch or stair. No verified imagery.

**NNE / SSW (ends)** — *inferred*: hip ends with no gables, roughly two window bays
each, chimney breasts on the flanks. The aerial shows a small notch on each long
side, read as a chimney breast and a bay.

**Top** — *measured from the aerial*: low hipped terracotta tile roof, ridge on the
long NNE–SSW axis, ~5.4 m of ridge, four hip planes, deep overhanging eaves with a
strong shadow line, two chimneys. No rooftop plant, no dormers, no skylights.

## 7. Recognition cues, ranked

1. The low terracotta hipped tile roof with deep overhanging eaves — the Presidio's
   signature roofscape, and at 10.6 m tall on a 271 m² footprint this *is* the read
2. A quiet cream stucco two-storey box, restrained and near-symmetrical
3. The tiled pent roof splitting the two floors, capping a recessed porch
4. Chunky square porch columns over a solid stucco balustrade
5. Two chimneys, and a raised base sitting up on a green rise

**Preserved:** roof pitch, hip form, eave overhang and terracotta colour; the
two-band facade split; the porch void and its shadow; the raised base.

**Simplified:** multi-pane casements became plain recessed panes with no muntins;
balconettes dropped as sub-pixel at the app camera; the balustrade became one clean
stucco parapet; tile is flat colour plus three course lines per slope, never modelled
tiles; ornament reduced to the ridge and hip capping courses.

**Exaggerated:** only the eave overhang, and only slightly — 0.65 m where scale
suggests ~0.5 m, because the eave shadow is the single feature that stops the asset
reading as a red box from above.

## 8. Uncertainties and conflicting evidence

- **Roof pitch drives the crest.** 10.6 m is derived, not published. Band 10.0–11.2 m.
  This is the number the loader scales by and the most likely thing here to be wrong.
- **Style attribution conflicts.** NPS calls the officers' quarters at "Funston and
  Presidio Boulevards" Queen Anne (1880–1890); the Presidio Trust calls the Presidio
  Boulevard homes Mission Revival built during WWI. The physical evidence for 542 —
  hipped red tile roof, cream stucco, casements, pent belt course — is decisively
  Mission Revival. Resolved in favour of Mission Revival; the Queen Anne reference
  almost certainly points at the older Funston Avenue row.
- **Build date conflicts**: 1912 (pres.house, for 544) vs 1917 (address listing, for
  542). The row was likely built in phases. Not load-bearing for the model; no single
  year is asserted.
- **Duplex vs single-family is unverified for 542 specifically.** The group is 16
  duplex units plus 4 single-family homes. The two-front-door cue comes from
  photography of a sibling, and is modelled because it is the more common case in the
  group and the more informative silhouette. If 542 proves single-family, delete one
  door.
- **No verified imagery of the rear or the two end elevations.** 542 sits behind a
  wooded rise and is not usefully covered by street-level imagery; the neighbours are.
  Those three elevations are inferred from the type and from the aerial.
- **The porch's arched entry** described by pres.house for 544 is not modelled: the
  photographed sibling shows a square-headed opening, the sources disagree, and an
  arch at this scale would be two pixels. Recorded rather than guessed.
