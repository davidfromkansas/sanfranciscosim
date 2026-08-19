# 424 Brannan Street (Tower Valet Parking lot) — reference dossier

Research behind `424-brannan.glb`. Compiled 18 August 2026, re-verifying
`docs/asset-plans/424-brannan.md` before modelling rather than trusting it.
Three of that plan's readings were corrected here first; all three are also
restated in `REPORT.md`.

**This asset has no building in it, and that is not an error.** 424 Brannan is a
2,026 m2 Z-shaped through-block surface parking lot. The subject is the void.

## 1. Sources and what each establishes

| Source | Establishes |
|---|---|
| [DataSF EAS Addresses](https://data.sfgov.org/resource/ramy-di5m.json) `address_number=424&street_name=BRANNAN` | the address resolves to exactly one parcel, **3776455** (block 3776, lot 455); one address on the lot |
| [DataSF Parcels](https://data.sfgov.org/resource/acdm-wktn.json) `blklot=3776455` | the 12-vertex lot polygon (committed verbatim as `data/parcel_3776455.json`), zoning CMUO, address range 424–424 |
| [DataSF Building Footprints](https://data.sfgov.org/resource/ynuv-fyni.json) `mblr=3776455` | **zero records.** This is the single most important fact in the dossier: the pipeline's own building source has nothing on this parcel, so there is no procedural building for the asset to replace and no LiDAR height to target |
| [SF Assessor secured roll](https://data.sfgov.org/resource/wv5m-vpq2.json) block 3776 lot 455 | class **V — Vacant Lot**; 0 stories, 0 units, property (improvement) area 0.0; lot area 21,348 sq ft. Identical in the 2023, 2024 and 2025 rolls |
| [DataSF DBI permits](https://data.sfgov.org/resource/i98e-djp9.json) block 3776 lot 455 | exactly two records, both filed 2019-12-23 (201912230246, 201912230259) for a 7-storey office with basement parking, both still at status `filed` — **never issued, never built** |
| [OSM way 124889469](https://www.openstreetmap.org/way/124889469) | `amenity=parking`, `parking=surface`, `surface=asphalt`, `fee=yes`, `access=yes`, `operator=Tower Valet Parking`, `addr:housenumber=424`; 1,911.9 m2 |
| [OSM way 1504713558](https://www.openstreetmap.org/way/1504713558) | a **separate** 407 m2 `access=private` surface lot filling the notch north of this parcel. Visually continuous on the ground, deliberately excluded from this asset |
| [SFPD permit 500106](https://www.sanfranciscopolice.org/get-service/permits/hearing-calendar-results/permit-500106-2026-06-24) and the January 2024 SFPD hearing-results PDF | commercial parking lot, DBA Tower Valet Parking Inc, **60 stalls**, renewal granted **2026-06-24** — the lot was still trading two months before this dossier |
| [Colliers offering via LoopNet](https://www.loopnet.com/Listing/424-Brannan-St-San-Francisco-CA/29453110/) | "currently improved as a surface parking lot with ±60 striped stalls, leased to Tower Valet Parking, Inc. on a month-to-month basis"; land assessed $24,541,417, **improvements $0** |
| [SFYIMBY, Dec 2021](https://sfyimby.com/2021/12/new-renderings-for-som-designed-offices-at-424-brannan-street-soma-san-francisco.html) | the entitled SOM scheme — 288 Ritch St + 55 Zoe St, 126,600 sq ft, 74 ft, for DECA Companies — and the site's three-frontage geometry |
| [SocketSite, Oct 2019](https://socketsite.com/archives/2019/10/hotel-plans-scrapped-office-buildings-now-on-the-boards.html) | the earlier 239-room hotel and the Heller Manus office pair; the lot-split manoeuvre behind the two-building scheme |
| Google satellite tiles z20/z21 (`mt1.google.com/vt/lyrs=s`), stitched and registered against the parcel ring | the stall rows, the spine aisle, the booth, the box trailer, the two green masses, the surface patching and its pale warm-grey tone |
| Google Street View panoramas `WXVXu81elVTxkdR3rXr1Zw`, `TUpIDbEopCNF5mypbXJ5aA` (Brannan), `SAz7nIhGlLCIhM4mORH_HQ` (Ritch), `c--Aph5B6JJAhIFghHOESA` (Zoe) | the chain-link fence and its barbed topping, the Brannan rolling gate, the Zoe swing gate, the red PUBLIC PARKING pole sign, the yellow striping, the concrete wheel stops, the attendant's booth |
| `app/public/tiles/terrain.bin` + the `terrain` block of `app/public/tiles/manifest.json` | the ground under the lot: 5.11–6.58 m, fall 1.469 m, planar to 0.102 m. Sampled by `sample_terrain.mjs` |

No copyrighted imagery is committed. The panorama ids and tile URLs are recorded
so the geometry can be re-derived; the pixels are not redistributed.

## 2. Verified dimensions and location

| Item | Value | Confidence |
|---|---|---|
| Anchor | `-122.3954857, 37.7798744` | **measured** — the parcel's axis-aligned bbox centre, which is what `placeGeneric()` means by "anchor" |
| Lot area | **2,026.1 m2** | **measured** from the parcel polygon; the assessor's 21,348 sq ft (1,983 m2) is 2.1% lower, normal rounding on an irregular lot |
| World bbox | 88.72 x 59.59 m | **measured** — the consequence of a 45.2 deg heading on a site that is 68.4 x 46.8 m |
| Ritch frontage | **68.40 m**, faces 45.2 deg | **measured** |
| Zoe frontage | **25.63 m**, faces 225.2 deg | **measured** |
| Brannan frontage | **15.84 m**, faces 135.2 deg | **measured** |
| Stalls | **60** | **measured** (SFPD permit; Colliers offering agrees) |
| Ground | 5.11–6.58 m NAVD88-ish; anchor 5.889 m | **measured** from the baked heightmap |
| Terrain fall | **1.469 m**, 2.18% downhill toward bearing 250 deg | **measured**, 8,104 samples |
| Terrain planarity | max residual **0.102 m** from a least-squares plane | **measured** — see s.4 |
| Sign crest | 6.80 m above the plate | ***inferred*** — see s.7 risk 2 |

The parcel ring in the site's own frame, as `extract_site.mjs` writes it into
`data/site_uv.json`. `u` runs north-east along Brannan, `v` runs south-east
toward Brannan; the origin is the anchor.

```
        u        v      edge to next    what the edge is
 V0   -5.73   -31.57     7.60 m         north notch
 V1   -5.71   -23.97    23.91 m         party line along the notch
 V2   18.20   -23.92    68.40 m         RITCH STREET fence
 V3   18.34   +44.48    15.84 m         BRANNAN STREET frontage (gate + sign)
 V4    2.51   +44.48    22.80 m         party line, rear of 426 Brannan
 V5    2.46   +21.67     7.60 m         party line jog
 V6   -5.14   +21.67    30.25 m         party line, rear of 434 Brannan
 V7   -5.52    -8.58    22.96 m         party line; Row C1 backs onto it
 V8  -28.48    -8.59    25.63 m         ZOE STREET frontage (swing gate)
 V9  -28.54   -34.21    22.80 m         party line, rear of the Zoe Street row
 V10  -5.74   -34.16     2.58 m         north notch
```

Every edge is axis-aligned in (u, v) to within 0.15 m over its length. That is
what makes the lot **v-simple** — every v-slice is a single u-interval — and it
is what `build_plate()` relies on to slice the draped plate into bands.

Features standing on the lot, measured off z21 nadir imagery with the parcel
ring overlaid:

| Feature | u, v | Blender X, Y |
|---|---|---|
| Attendant's booth | 14.88, −12.40 | 1.82, 19.29 |
| White box trailer | 10.96, −15.23 | −2.96, 18.53 |
| Volunteer thicket | −2.00, −30.82 | −23.14, 20.46 |
| Brannan-corner shrub | 3.76, +43.18 | 33.10, −27.99 |

## 3. Orientation

The lot is a through-block Z. Its long boundary is the 68.4 m Ritch Street
fence; a 15.8 m neck reaches south-east to Brannan between the Brickhouse
restaurant at 426 Brannan and the block corner; a 22.8 m tail reaches
south-west to Zoe. The south-west boundary is a party line against the backs of
426 and 434 Brannan, one of which carries a large teal-and-pink mural facing into
the lot. **The mural belongs to the neighbour and is not in this asset.**

Authoring frame is (u, v) with `+Y` = true north in Blender, so the model drops
into the city at its real heading and the loader applies no rotation. The frame
is left-handed in world, so every ring goes through `orient_for_world()`.

## 4. The terrain drape — read this before changing anything

**This asset is draped on the baked terrain, and that is why `min_z` is negative
and `targetHeightM` is 8.5649 m.** Both are deliberate, both are asserted by
`validate_424_brannan.py` as checks D1–D4, and neither is a contract slip.

`placeGeneric()` in `app/src/assets.js` seats a landmark from a single terrain
sample:

```js
const y = Math.max(0, data.sampleElevation(x, z));   // at the anchor, once
```

Correct for a building. Wrong for an asset that IS the ground. This lot falls
**1.469 m** across its 88.7 x 59.6 m bounding box — 5.11 m at the Zoe corner,
6.58 m at the Brannan corner — so a flat plate seated at the anchor's 5.889 m
would be 0.78 m buried at one end and 0.69 m airborne at the other. That is
invisible in every Blender render. `artifacts/64-south-park/REFERENCE.md`
records the first time this was found, in the running app, with half a park
under the landcover.

Two things differ from South Park and are worth stating:

- **The fall is two-dimensional.** South Park's cross-axis was flat to 0.30 m so
  its `dy` is a 1-D profile of `u`. This site falls 2.18% toward bearing 250,
  which is neither of its own axes, so `sample_terrain.mjs` emits a 29 x 45 grid
  at 2 m and the build interpolates it bilinearly.
- **The terrain here is very nearly a plane** — a least-squares fit gives
  `dy = 0.0205*X + 0.0074*Y + 0.0061` with a maximum residual of **0.102 m**
  over 8,104 in-lot samples. The plane is reported because it is the honest
  one-line description of the site, but the build does **not** use it: 0.102 m
  of residual against 0.12 m of plate clearance would have left the slab 18 mm
  above the terrain at the worst point. Interpolating the same grid the runtime
  samples instead puts the measured clearance spread at 0.0000 m.

Consequences:

- **z = 0 is the anchor's ground**, not the bottom of the model, because that is
  where the loader puts it. `min_z` is **−1.0844 m** (the plate's skirt at the
  Zoe corner). The check that replaces "min_z ~ 0" is that the plate's top face
  stands a constant height above the sampled terrain across its whole area;
  measured spread **0.0000 m** over 424 top-cap vertices.
- **`targetHeightM` is the vertical extent**, 8.5649 m, because the loader's
  scale is `targetHeightM / bbox height` and it has to land on 1.0.

## 5. What each side shows

**Brannan (south-east, 15.8 m)** — the public face. A gap in the street wall
between the low timber-clad Brickhouse restaurant and the corner, closed by
chain-link with a **wide rolling gate** parked open against the fence, razor
topping on the fixed runs, and a **tall red-and-white pole sign**: dark header
band (TOWER VALET PARKING), PUBLIC PARKING in white on red, small print, a red
"Enter Here" flash. A leggy shrub fills the corner just inside V4.

**Ritch (north-east, 68.4 m)** — the long side. Chain-link with barbed topping
on a regular post pitch, and behind it the lot's densest row: cars nose-in to
the fence on yellow stalls with concrete wheel stops at each bay head. The
attendant's booth stands in this row about a third of the way along, with a
white box trailer beside it in the aisle.

**Zoe (south-west, 25.6 m)** — chain-link with a braced **swing gate** standing
open into the lot. Beyond it the western belly, the rows against the party
walls, and the brick warehouse on Ritch closing the view.

**Party boundaries (north-west and south-west)** — blank painted masonry of the
neighbours. Not in this asset; the fence runs the full ring instead, which is
the one place the model is more continuous than the site.

**Top — the subject.** A pale, warm-grey slab, patched and map-cracked, with
five rows of yellow stalls around a spine aisle running from the Brannan gate
north-west into the belly and out at Zoe. Half to two-thirds occupied. Two green
masses, at the north notch and the Brannan corner. No structure of any size
except the booth.

## 6. Recognition cues, ranked

1. **The void** — a large pale ordered rectangle punched through a block of
   otherwise continuous roofs. This asset's silhouette is the shape of what is
   missing
2. The **stripe rhythm** — five rows of yellow bays around one spine aisle
3. The **continuous chain-link line** with its two gates, drawing the parcel
   outline hard in a district of soft edges
4. The **red PUBLIC PARKING pole sign** at the Brannan neck
5. **Parked cars** — the only thing that says "working lot" rather than "hole"

## 7. Uncertainties and conflicting evidence

1. **The row layout is a reconstruction.** The 60-stall count is measured; the
   row positions and the aisle are observed from z21 nadir imagery; the per-row
   bay allocation (R 23, M 11, C1 8, C2 6, Z 7, A 5) is chosen to total exactly
   60 against the measured parcel. Treat the bay counts as *inferred*.
2. **The sign's height is *inferred*** at 6.80 m, from comparing the board
   against the second-floor window heads of the building across Ritch in
   panorama `TUpIDbEopCNF5mypbXJ5aA`. Worth ±0.5 m. Because it sets the model's
   crest it also sets `targetHeightM` — but the loader scale still lands on
   1.0000 either way, since `targetHeightM` is taken from the measured bbox. A
   wrong crest makes the sign wrong, not the lot.
3. **The sign is pulled ~2 m inside the fence.** The real pole stands at the
   kerb, in the public right of way, which this asset does not own.
4. **The thicket is pulled wholly inside the boundary.** Measured at
   (u −2.0, v −30.8) it straddles the parcel line into the private lot next
   door; the model puts its three crowns at u −8.3…−11.9, which also required
   dropping Row C2 from seven bays to six.
5. **The fence runs the full ring**, including the two party boundaries where
   the real edge is the neighbours' masonry. Without it the lot's outline stops
   halfway round and reads as an unfinished model.
6. **The surface colour will be argued about.** Every reference reads pale warm
   grey — worn concrete and old asphalt — and style bible s.13 reaches for
   "clean charcoal asphalt". The references win: the paleness is what makes the
   void read from the air, and the city's darker streets do the contrast work.
7. **The site is entitled and could be built at any time.** Re-check the DBI
   permit status before any future revision; this asset has a shorter shelf life
   than its neighbours.
