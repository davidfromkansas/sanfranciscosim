# 326 Brannan Street — reference dossier

Research compiled 16 August 2026 for the SF-SIM miniature asset. Everything below
was verified against primary sources during the build; where this dossier
disagrees with `docs/asset-plans/326-brannan.md`, this file and `REPORT.md` win.

## 1. What this is

Not a building — a **site**. A 194 m² infill slot on the north-west side of
Brannan Street, one lot southwest of Second, occupied by the **JAX Vineyards SF
tasting room**. The lot holds two things:

- a **1959 one-storey commercial shed**, 61.6 m², at the *rear* (north-west) of
  the lot, black-painted concrete masonry with a big glazed roll-up door onto
  the court — the indoor tasting room, ~600 sq ft;
- the **Wine Court**, 95.2 m² of open ground in *front* of it, on Brannan —
  formerly the building's parking apron, converted to a walled outdoor tasting
  garden in 2013–14 and renovated in 2020.

From Brannan Street none of the building is visible. The entire public elevation
is a charcoal vertical-board gate and fence carrying white wine-bottle
silhouettes and one red JAX disc, with foliage rising over it.

It is the second site-not-a-building asset in the set after `551-third`, and the
first whose subject is a garden.

## 2. Sources and what each establishes

| Source | Establishes |
|---|---|
| DataSF Parcels `acdm-wktn`, `blklot=3775012` | **authoritative lot geometry** — 7.98 × 24.32 m, 194.1 m², corners, centroid, zoning CMUO |
| DataSF Building Footprints `ynuv-fyni`, `mblr=SF3775012` | **authoritative built geometry and heights** — two polygons: shed 61.6 m² at 5.66 m median (mode 5.50, min 5.25, sd 0.91, 252 cells); court 95.2 m² whose height **mode is 0.14 m** |
| DataSF Addresses `ramy-di5m` | address → APN 3775012; point 37.781508 / −122.392896 |
| DataSF Assessor Secured Roll `wv5m-vpq2`, block 3775 lot 012 | year built **1959**; **1 storey**; class C Commercial Stores; use COMR; 1,007 sq ft building on a 2,099 sq ft lot |
| DataSF Building Permits `i98e-djp9`, block 3775 lot 012 (6 permits, 1997–2014) | the whole site history — see §6 |
| DataSF Street Centerlines `3psu-pn9h` | Brannan's centreline, used to prove which end of the lot is the street |
| [OSM way/1168876044](https://www.openstreetmap.org/way/1168876044) | address, `building=yes`, `shop=wine`, `name=JAX Tasting Room` — **geometry rejected**, see §7 |
| Google Street View, Brannan Street pano, capture **May 2025** | the gate elevation: charcoal vertical boards, five white bottle silhouettes with small `jax` wordmarks, a red disc, a solid double gate leaf at the SW end, foliage and a dark canopy above the fence, one red heat lamp, ivy blanketing 334 Brannan's flank |
| Google Maps satellite (Vexcel, 2026) | the site plan: pale rear shed roof, canopy and tree canopies mid-lot, gate at the sidewalk, the slot between two larger neighbours |
| jaxvineyards.com — SF tasting room page hero image | the shed interior and its court elevation: **black-painted CMU**, a multi-lite glazed roll-up/folding door, polished concrete floor, black bar |
| Terra Ferma Landscapes project page (photo credit Jason Liske) | the court's design program: ~1,000 sq ft, **fire table with built-in lounge seating, mature olive trees, grape vines, raised planters, dramatic evening lighting, vine-covered walls**; GC TFL Construction |
| Eventective / VenueKonnex venue listings | **600 sq ft indoor + 900 sq ft outdoor**; 100 standing / 60 seated; **18-foot olive tree**; built-in fire pit; projector; patio coverable for winter; renovated 2020 |
| Yelp photo `DXAKbTAMZk7HZKKOEvN8vA` | the court at night: warm catenary string lights, candle and fire glow, red heat lamps, neighbouring brick reading dark |
| CA ABC licences 00535821 / 00624057; SF business registry `1024047-03-151` | occupancy — location opened 2015-03-16, on-premise winegrower licence since 2021 |

No architect is recorded for the 1959 shell in any source consulted. The
**landscape designer of record for the court is Terra Ferma Landscapes.**

## 3. Verified dimensions and location

| Item | Value | Confidence |
|---|---|---|
| WGS84 anchor (parcel centroid) | `-122.3928965, 37.7815080` | measured |
| Lot | 7.98 m frontage × 24.32 m deep, 194.1 m² | measured (DataSF parcel) |
| Assessor lot area cross-check | 2,099 sq ft = 195.0 m² | agrees to 0.5 % |
| Shed footprint | 61.6 m², ~9.6 m deep × 6.9 m wide | measured (LiDAR polygon) |
| Court | 95.2 m², v 1.00–14.61 m from the street line | measured (LiDAR polygon) |
| Listing cross-check | 600 sq ft = 55.7 m² indoor; 900–1,000 sq ft = 84–93 m² outdoor | both agree with the survey to within a wall thickness |
| Shed roof deck | **5.66 m** above grade | measured (LiDAR median) |
| Shed parapet crest | **5.90 m** — the bbox top | inferred (deck + 0.24 m) |
| Olive crown crest | 5.80 m | design decision, see §8 |
| Storeys | 1 | assessor + all six permits |
| Ground elevation | 11.55–11.91 m NAVD88 (0.36 m range over 24 m) | measured — the app's terrain owns this |

**Heights that must not be used.** `hgt_maxcm` is 942 (9.42 m) on the shed and
3874 (38.74 m) on the court. Both are 0.5 m LiDAR cells sitting on party walls
shared with taller neighbours — 334 Brannan is 12.14 m. This is the Earl Warren
case in `docs/asset-plans/README.md`: *a single-cell `hgt_max` on a party wall is
unusable.* The shed is a flat-roofed one-storey box at 5.5–5.7 m.

## 4. Orientation

The lot sits at the SoMa grid's 45°, like every other asset on this block face.
Surveyed parcel corners, app-local metres re-centred on the anchor and converted
to Blender axes (+X east, +Y north); the ring A → D → C → B is CCW:

```
A ( 11.400,  -5.811)   east corner, on Brannan
B (  5.740, -11.441)   south corner, on Brannan
C (-11.410,   5.799)   west corner, at the rear
D ( -5.740,  11.429)   north corner, at the rear
```

| Edge | Length | Outward | Elevation |
|---|---|---|---|
| B–A | **7.98 m** | SE **135.15°** | **Brannan Street front** |
| A–D | 24.32 m | NE 45.15° | northeast party line — 318 Brannan (KCA Engineers, 8.11 m) |
| D–C | 7.98 m | NW 315.15° | rear property line |
| C–B | 24.32 m | SW 225.15° | southwest party line — **334 Brannan (12.14 m, ivy-covered flank)** |

The model is authored in a lot-local `(u, v)` frame derived from those corners:
`u` runs along the frontage from the SW party line to the NE one (−3.99 → +4.00),
`v` runs into the lot from the Brannan property line (0 → 24.32).

The asset is authored in true-world orientation because `placeGeneric()` in
`app/src/assets.js` scales and positions but never rotates. The contract's
"front faces −Y" rule cannot be honoured literally — the real front faces
southeast — and per `docs/asset-plans/README.md` real-world orientation wins.

Consequence: the axis-aligned XY bounding box is ~22.3 × 22.4 m for a
7.98 × 24.32 m lot. That is correct, not a scale error.

**Which end is the street was proved, not assumed**, because getting it backwards
mirrors the whole asset. The DataSF Brannan centreline runs through
`(3997, −1309) → (3950, −1263) → (3899, −1212)` in app-local metres. Perpendicular
distances: the A–B (south-east) midpoint is **12.0 m** from it — one Brannan
half-right-of-way — and the C–D midpoint is 36.3 m. The court fronts Brannan; the
shed is at the back.

## 5. What each side shows

**Southeast — Brannan Street front.** The only public elevation, and it is not a
building. A charcoal vertical-board fence and gate spans the full 7.98 m frontage
at roughly 2.8 m. The southwest third is a solid double-leaf gate with a slim
vertical pull. The remaining panels carry five large off-white wine-bottle
silhouettes, each with a small `jax` wordmark, and one red filled circle with the
`jax` mark reversed out of it. Above the fence line: foliage, the dark edge of the
court canopy, and one red heat lamp.

**Northeast — 318 Brannan party line.** Blind. The neighbour's blank white wall
is on or near the line; the asset carries only its own low court wall, planters
and a lighter vine mass. The survey leaves a ~1.0 m side passage between the
shed and this line, which is kept.

**Southwest — 334 Brannan party line.** The court's visual backdrop. 334's flank
is **blanketed in ivy for its lower two thirds**. That wall belongs to the
neighbour and is not modelled; instead the asset's own southwest court wall
carries the densest vine mass, cresting above the wall so the reading survives
before the baked neighbour loads.

**Northwest — rear.** The shed's back wall on the rear property line. **No
research exists for this elevation** — no public vantage, nothing published. It
is a blind wall by inference from the site plan.

**From above — the view that matters.** In order from Brannan: gate cap rail;
open court with raised planters down both sides; a slatted pergola; the fire
table inside its bench; the olive crown overhanging court and walls; then the
shed's flat roof filling the rear 9.6 m.

## 6. Site history from the permits

| Filed | Permit | What it says |
|---|---|---|
| 1997-09-09 | 9717507 | reroofing; existing use *office* |
| 2013-09-04 | 201309045959 | *"change use of outdoor space from existing parking lot to a wine tasting area/retail sales. **existing building not to be open to the public and not to be modified**"* |
| 2013-12-10 | 201312103834 | *"retail sales. new restrooms, change door swing, interior non structural alterations. change of use"* — `manufacturing` → `retail sales` |
| 2014-01-30 | 201401307463 | outdoor space `parking` → tasting/retail; ADA bathroom; **gas line extension** (the fire table) |
| 2014-06-02 | 201406027264 | *"to erect **front gate sign**. non electric, single faced"* |
| 2014-08-11 | 201408113522 | accessible restroom work; construction type **wood frame (5)** where earlier records say type 1 |

Read in order: a 1959 shed used for manufacturing then office, with a parking
apron on Brannan; the apron becomes the tasting garden first (September 2013,
explicitly *without* opening the building), the building follows three months
later, the fire-table gas line and the front gate sign arrive in 2014, and the
whole site is renovated in 2020.

**This is why the 2010 LiDAR describes a site that no longer exists.** Every
element that gives this lot its identity post-dates the survey by three to ten
years. The LiDAR is used here for the shed and the ground, and for nothing else.

## 7. Rejected and conflicting evidence

- **OSM geometry is wrong.** `way/1168876044` carries the right address and the
  right occupant name and a Bing-traced shape: 104.8 m², minimum-area box
  **13.18 × 7.98 m**, long axis running *along* Brannan. The lot is 7.98 m wide
  and 24.32 m deep — OSM has the proportions rotated 90°, and the ring crosses
  the southwest property line by up to 2.1 m. Same failure as `358-brannan`.
  DataSF parcel + LiDAR is the survey.
- **"Back garden" is wrong.** Several aggregator listings (corner.inc and
  others) describe a *back* garden reached through the tasting room. The survey,
  the two polygon areas and the permit history all put the court at the **front**
  on Brannan and the shed at the **rear**. The listings appear to be
  machine-written summaries; they are not evidence.
- **Construction type disagrees with itself.** The 2013–14 permits say "constr
  type 1"; the August 2014 permit says "wood frame (5)". The tasting-room
  photographs show painted **concrete masonry**. The model follows the
  photographs. No dimension depends on this.
- **The "18 foot olive tree"** is repeated verbatim across several venue
  listings — copy written once and syndicated, and dating from around 2015. A
  transplanted mature olive planted eleven years ago will have grown. See §8.

## 8. Design decisions taken during the build

- **The parapet owns the bounding box, not the tree.** `targetHeightM` is the
  shed's 5.90 m parapet crest; the olive crown is built to 5.80 m, deliberately
  0.10 m under it. The alternative — letting an un-measurable tree height set
  the scale of the entire site — was rejected.
- **Nothing on the shed roof rises above 5.90 m.** The roof has never been
  photographed. Inventing a mechanical unit tall enough to become the crest
  would have rescaled the asset off an unobserved feature, so the mechanical
  boxes, hatch and vent are all capped just under the parapet.
- **The canopy is built as a slatted pergola with a partial panel.** The real
  structure is a panelled metal canopy. Modelled solid it became a black
  rectangle over a third of the court in the downward view — the one view this
  asset exists for. The panel is kept over the half that shelters the tables.
  Recorded as a departure in `REPORT.md`.
- **The court side walls stop at 2.70 m** and the vine masses crest above them.
  They are a liner on the property line, not the neighbours' buildings: at
  2.70 m they can never reach the 8.11 m and 12.14 m baked blocks that will
  stand beside them, and letting the greenery top the wall is the only way the
  lot reads green from outside the court.
- **The olive is four separated masses, not one dome.** The first render turned
  a single smooth blob into broccoli from the app's camera.

## 9. Recognition cues (ranked)

1. The **black bottle-graphic gate wall with its red JAX disc** — the whole
   street elevation, and unmistakable.
2. A **green slot in a masonry wall** — the only opening in 200 m of 8–14 m
   warehouse boxes, and it is full of plants.
3. The **olive tree**, silver-green and overhanging the court walls.
4. The **string lights at night** — a lit garden between two dark blank party
   walls.
5. The **black CMU shed with its glazed roll-up door**, which is what makes the
   court a room rather than a vacant lot.

## 10. Uncertainties carried into the model

- The gate height (2.80 m) is **estimated** from the May 2025 pano against
  parked cars and parking meters. It is the most-seen surface on the asset but
  it does not set the scale.
- The parapet (0.24 m above the measured deck) is **inferred**, typological for
  a 1959 flat-roofed commercial shed.
- The canopy's real extent and whether it is fixed or retractable is
  **inferred** from one oblique, partly screened view.
- The rear (north-west) elevation is **entirely inferred**.
- The olive's height is a **design decision**, not a measurement (§8).
