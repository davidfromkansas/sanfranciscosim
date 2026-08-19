# 10 South Park (South Park Lofts) — reference dossier

Compiled 18 August 2026 for `artifacts/10-south-park/`. Everything below is
either measured from a named public dataset, quoted from a named source, or
labelled *estimated* / *inferred*. The plan behind it is
`docs/asset-plans/10-south-park.md`; where this file and that plan disagree,
**this file is the record of what was actually built** and the disagreements are
listed in `REPORT.md` §5.

## 1. Identity

| | |
|---|---|
| Address | 10 South Park (also 10 South Park Avenue, 10 S Park St), San Francisco CA 94107 |
| Marketing name | South Park Lofts |
| Block / lot | 3775 / **106–115** — ten condominium lots on one parcel |
| Built | **March 1993**; permit 9123974 filed 19 Dec 1991, "erect a three story ten unit reisdential bldg" [sic] |
| Architect | **Ramon Zambrano** (single source — see §6) |
| Use | 10 live/work loft condominiums, Assessor class **LZ**, 929–1,196 ft² per unit |
| Style label | "Contemporary Mediterranean" (the developer's own term); the broker who sold the units called the stucco "reminiscent of the South West" |
| Neighbours | 22–24 South Park (SW, 14.22 m, the Hotel Madrid) and 2 South Park (NE, 17.72 m, the Kohler warehouse) — **both taller than this building** |
| Manifest id | `10-south-park` |

## 2. Sources and what each establishes

**Survey and public record**

- **DataSF building footprints `ynuv-fyni`** — the bake's own primary input, and
  the authority for depth and roof height. `201006.0015438` (front block, 262 m²,
  `hgt_median_m` 12.27, `hgt_maxcm` 1467, `hgt_mincm` 1014, `hgt_stdcm` 78.4,
  1,044 cells) and `201006.0030231` (rear block, 181 m², median 11.88, max 1427,
  min 849, σ 79.6, 717 cells). Ground elevations differ — `gnd_meancm` 1424.6
  front against 1472.1 rear — so **the site rises 0.47 m from South Park to Taber
  Place and the two roof planes are level in absolute terms** (26.52 m and
  26.60 m). That is why the model builds both decks at one height.
- **DataSF parcels `acdm-wktn`, blklot 3775106** (identical for 107–115) —
  585.0 m², 20 vertices including the 15-vertex densified front arc. **The
  authority for the lot lines**; the LiDAR outlines chord the frontage.
- **DataSF addresses `ramy-di5m`** — ten records, `10 SOUTH PARK #1` … `#10`.
- **DataSF assessor `wv5m-vpq2`** (2024 roll) — class LZ, 1993, unit areas 929,
  931, 1065×5, 1069, 1145, 1196 ft².
- **DataSF permits `i98e-djp9`** — 48 records. The load-bearing ones: **9123974**
  (1991, complete) the original three-storey ten-unit permit; **9711232** (1997)
  seismic repair with stucco replacement; **201211274894** (2012, complete)
  "remove (e) stucco to correct waterproofing @ windows entire facade, replace
  stucco in kind @ entire facade @ south park st elevation w/ expansion joints";
  **201108263429** / **201210182300** reroofing; **202109279232** (2021) fire
  alarm "garage, 1/f & 2/f" — three levels named, matching the 1991 permit's
  "three story". No permit after 2012 touches the exterior.
- **`artifacts/22-south-park/REFERENCE.md`** — the south-west neighbour's dossier.
  It measures the **shared party wall at 36.28 m on bearing 45.19°** and records
  this building from the outside as "11.88–12.27 m", which is an independent read
  of our roof deck.

**Published description**

- `http://www.somapro.com/db/loft.html` — the SOMA loft database. Establishes the
  architect, the March 1993 completion, "16 foot ceilings", the 930–1,195 ft²
  range, and the developer's "Contemporary Mediterranean" label.
- `http://www.somapro.com/San%20Francisco%20Lofts%20South%20Park.html` —
  establishes the **pond**: "Mediterranean style architecture built around a Pond
  and recently restored landscaped courtyard".
- `https://www.bayareamodern.com/lofts/south-park-lofts/` — establishes the
  two-building courtyard plan, 1993, 10 units, "stucco-finished Mediterranean
  exterior", "most units have small patios or French balconies".
- Listing copy (Vanguard, Compass, KW, BHHS, cchp.com, 2024–25), *observed
  (listing photo)* — "boutique courtyard building", two-level lofts, "a wall of
  windows", "French doors to a shared courtyard", skylights, one garage space per
  unit.

**Imagery (keyless, re-fetchable)**

- Google Street View pano **`aFRDCNG9w0lcHJ9ngJI8LQ`**, © 2025, labelled
  "10 S Park St" by Google's own metadata; camera 37.78215707, −122.39335946,
  pano heading 290.854°, standing ~5 m off the frontage. **The equirectangular's
  column 0 is bearing (heading − 180) = 110.854°**, verified against the surveyed
  party-wall corner. Every facade measurement in §3 and §4 comes from this pano.
- Google Street View pano **`q6hwZn8Ks9tq4nSLfTZuDw`** (Taber Place, 5.8 m out)
  and **`8nlV6lfftmnNN_DPOQEuTw`** (19 m out) for the rear elevation.
- **Google satellite z21** (`mt1.google.com/vt/lyrs=s`, 0.059 m/px) for the roofs
  and courtyard; Bing z20 and Esri z20 fetched as cross-checks. **All three lean:**
  2 South Park's 17.7 m roof overhangs our surveyed parcel line in every one.
- Tile recipe (403s without both a browser UA and a `https://www.google.com/`
  referer):
  `https://streetviewpixels-pa.googleapis.com/v1/tile?cb_client=maps_sv.tactile&panoid=<ID>&x=<0-7>&y=<0-3>&zoom=3&nbt=1&fover=2`

**And one source that does not exist**

- **No OSM way carries this address.** Nominatim resolves "10 South Park" by TIGER
  interpolation onto the South Park *roadway* (way 8916551) and returns
  `osm_type: way`, which looks exactly like a building hit — the 350 Brannan
  failure mode. Overture does carry both blocks (`…79f82d14b81c` 251 m² front,
  `…e716f25d7e5b` 150 m² rear) but neither ring is addressed. Every route into
  this lot runs address → `ramy-di5m` → APN → `acdm-wktn` → footprint.

## 3. Verified dimensions, location and orientation

Lot-local frame: **+u = 44.8° north-east** along the party walls, **+v = 134.8°
south-east** toward the park, origin at the parcel's vertex mean
(−122.393446, 37.782262).

| lot edge | length | outward normal | elevation |
|---|---|---|---|
| South Park front, north-east third | **8.13 m** | **135.2° SE** | hero, straight |
| South Park front, south-west two-thirds | **8.64 m of arc** (chord 8.62, R 35.3 m, sweep 14.1°, sagitta 0.26 m) | chord normal **179.7°, due south** | hero, bowed |
| south-west boundary | **36.28 m** | 225.2° | party wall, blind |
| Taber Place rear | **14.29 m** | 315.2° NW | secondary, finished |
| north-east boundary | **42.34 m** (21.43 + 20.91) | 45.2° | party wall, blind |

The two front segments meet at a **~30° corner**; with the arc's own 14.1° sweep
that is **44.5° of total turn across 16.77 m of frontage** — the oval turning its
east end, and the reason the north-east boundary is 6.06 m longer than the
south-west one. (22–24 South Park records the same asymmetry, 6.15 m, one lot
along.) A single circle fitted through all sixteen surveyed front vertices does
not close — residuals to 0.67 m, nonsense radius — so the break is real and the
survey is not describing one smooth curve.

Built extents, from the two DataSF footprints:

- **front block** v +8.53 → −12.14 (20.67 m deep), full width, 262 m²
- **courtyard** v −12.14 → −22.12 (9.98 m), full width less the wing, ≈ 142 m²
- **rear block** v −22.12 → −33.34 (11.22 m) full width, **plus** a wing at
  u +7.48 → +10.52 reaching forward to v −17.69; 181 m²

The LiDAR front edge sits 1.2–1.3 m behind the surveyed front property line —
LiDAR erosion plus a probable balcony overhang, not a setback. The model builds
the front wall **on the parcel line** and uses the LiDAR outline for depth only,
which is the 165–167 South Park rule for dense narrow SoMa lots.

**Heights**

| feature | value | how |
|---|---|---|
| roof deck | **12.27 m** front (LiDAR median = LiDAR mode over 1,044 cells, σ 0.78); 11.88 m rear over ground 0.47 m higher | measured |
| parapet crest | **13.10 m ± 0.15** | photogrammetric — see below |
| roof bulkhead crest | **14.67 m** front (LiDAR max); 14.27 m rear | measured |
| **model target height** | **14.67 m** | the crest of the tallest modelled geometry |
| garage / ground floor | 0 → 3.30 m | *estimated* |
| loft tier 1 | 3.30 → 8.20 m | *estimated* |
| loft tier 2 | 8.20 → 13.10 m | *estimated* |

**The photogrammetric parapet.** From pano `aFRDCNG9w0lcHJ9ngJI8LQ`, stitched to
4096 × 2048, the sky/stucco edge detected per column, elevation converted with
`h = h_cam + D·tan(θ)` at `h_cam` = 2.5 m and `D` solved by intersecting each
bearing with the measured footprint polyline:

| bearing | 314° | 320° | 326° | 332° | 338° | 344° | 350° | 354° |
|---|---|---|---|---|---|---|---|---|
| D (m) | 10.48 | 9.53 | 8.83 | 8.32 | 7.94 | 7.67 | 7.50 | 7.44 |
| crest (m) | 13.14 | 13.08 | 13.10 | 13.09 | 13.10 | 13.04 | 13.05 | 13.03 |

Flat to **±0.06 m while the range varies 41 %**. A wrong `D` drifts
systematically with range; a wrong camera height shifts the whole column but
stays flat — so this confirms the footprint polyline and leaves camera height
(±0.15 m) as the only unshared error term. 13.10 m sits 0.83 m above the LiDAR
deck, which is an ordinary parapet.

**The storey arithmetic is a third, independent confirmation.** The garage-door
head measures 2.3 m and the first balcony deck 3.3 m. Subtracting that ground
floor from the 13.10 m parapet leaves **9.80 m for two loft tiers = 4.90 m each =
16.07 feet.** The broker's "16 foot ceilings", the 1991 permit's "three story"
(garage plus two loft storeys), and the photographed facade (four window rows
above the garage, alternating French-door-and-balcony with wide window band,
exactly two of each) all land on the same number from different directions.

**Why the LiDAR maximum is believed here.** 14.67 m sits 2.40 m above its own
median at 3.1σ — the band where 592 Third Street's street-tree artifact lived and
where 22–24 South Park's parapet was believed. Three things settle it:

1. *Position rules out the tree.* The only large tree touching this building is
   the sidewalk magnolia at the north-east front corner; a canopy there cannot
   raise the maximum without disturbing the front parapet cells, and the median is
   undisturbed.
2. *Direction rules out party-wall bleed.* Both neighbours are **taller**, so a
   bleeding cell could only pull the maximum toward 14.22 m or 17.72 m from
   outside — yet the same 2.4 m step appears on the **rear** block, whose
   neighbours are different buildings. Two independent footprints reporting the
   same step is a building feature.
3. *The aerial shows the thing itself* — a hard-edged rectangle about 5.7 × 2.4 m
   at the rear edge of the front block's roof, casting its own shadow. A stair
   bulkhead is what a 2.4 m step over a 12.27 m deck is.

**Anchor.** The model's own bbox centre, reported by the build:
**−122.3935162, 37.7823704**. It is *not* the Assessor's condo point
(−122.393411, 37.782262), which sits 4.4 m away, and it is not the lot-frame
centre either — the 45° heading moves it.

## 4. What each side shows

**South-east (South Park) — observed, Street View Jan 2025. The hero elevation.**
Apricot stucco, four levels, no cornice, a plain parapet with a thin pale cap.
Metric station layout along the bowed plane, read off the panorama by mapping
bearings through the surveyed front polyline (t from the south-west party wall):

| t (m) | element |
|---|---|
| 0.0 – 0.6 | plain return against the party wall |
| 0.6 – 5.5 | the **wide window band**, once per tier |
| 0.6 – 1.9 | square window, lower row of each tier |
| 1.95 – 3.05 | round-arched wood **French door** on a juliet balcony |
| 5.5 – 7.9 | the **recessed loggia**, both tiers, ~1.2 m deep |
| 7.9 – 9.0 | solid return |
| 2.6 – 7.2 | the garage door, ground floor |
| 0.6 – 2.0 | the recessed pedestrian entry, ground floor |

Each wide band is glazed as a grid of small panes in near-black bars inside a
broad flat pale surround, with **a long flattened oval drawn across the middle in
heavy mullion, its south-west end curling into a small circle.** That motif is
the building's only ornament and the strongest recognition cue on this rim.

The straight north-east third carries two narrower window bands per tier and then
runs into the party wall with 2 South Park. It stands behind a large sidewalk
magnolia in every available capture; the photogrammetric crest drops from 13.10 m
to about 11.6 m across bearings 356°–2°, which reads as a set-back or lower top
level at that end — but could equally be the edge detector finding a loggia
soffit through foliage. **Modelled flush.** See §6.

**North-west (Taber Place) — observed, Street View Jan 2025.** A finished
elevation, not a service back: same apricot stucco, dark-framed multi-pane
windows in pairs (some with internal blinds), a dark door behind an ornate iron
security gate at the south-west end, a garage opening at the north-east end with
a **"10 SOUTH PARK" plaque** beside it, wall-mounted lights and a camera, and a
vertical expansion joint running the height of the wall.

**North-east and south-west — party walls, blind.** 22–24 South Park is 14.22 m
and 2 South Park is 17.72 m. **Both are taller than this building's 13.10 m
parapet**, so — unlike 22–24, whose own flank stands 4 m proud of its neighbour —
neither of this building's flanks is ever seen from the app's camera. Flat stucco,
no geometry spent.

**Courtyard — inferred from aerial and listing copy.** ~10 × 14 m, open to the
sky, enclosed on four sides. Paved, planting beds along both party walls, a
specimen tree with purple-bronze foliage near the centre, and the pond every
broker mentions (a pale kidney shape in the aerial's shadow). Both blocks open
onto it through what the listings call "a wall of windows with French doors".

**Top — read off Google z21, and the least certain part of this dossier.** Front
block: a pale membrane deck inside a plain parapet, a grey bulkhead ~5.7 × 2.4 m
at the courtyard edge, a cluster of small mechanical units and one dark panel
(skylight or PV) along the north-east parapet, nothing on the south-west half.
Rear block: a terracotta-coloured surface over much of it — possibly a tile roof,
possibly a paver terrace — with a pale band along the Taber Place edge.

## 5. Recognition cues (ranked)

1. **The oval window motif** — a long flattened ellipse with a curled tail in
   heavy mullion across each wide band. Nothing else on the oval wears it.
2. **Apricot stucco** on a rim of sage clapboard, cream ashlar and red brick.
3. **The two-block plan with an open courtyard** — a pentagon with a hole in it,
   where every other lot on the rim is one solid mass wall to wall.
4. **The bowed front**: 44.5° of turn across 16.8 m, sharp enough that the two
   planes catch the sun differently.
5. **The stacked loggias** — two deep shadow recesses one above the other, the
   only real depth in the elevation.

## 6. Uncertainties and conflicting evidence

- **The bulkhead is inferred, and it is the target height.** See §3. If it were
  ever disproved, the fallback is the photogrammetric parapet at 13.10 m, and the
  model would have to be rebuilt to that crest rather than scaled to it.
- **The north-east end of the front elevation is guessed.** The magnolia hides the
  last ~4 m of frontage plus the corner with 2 South Park in every capture from
  either direction. Modelled flush and full height; the alternative reading is a
  set-back top level about 1.5 m lower.
- **The roof is read from imagery that leans.** Whether the rear block is tiled,
  whether the two tan hipped shapes near the courtyard are ours or the
  neighbours', and where exactly the bulkhead sits all carry that error. The model
  takes the conservative reading — flat membrane on both blocks — because a tile
  roof invented from a 2 cm/px oblique would be a bigger error than omitting one.
- **The colour is one capture under mixed light.** Sunlit stucco medians to
  `#b58f70` in the raw pano pixels; the model uses `#dda87b`. The 2012–13 permit
  confirms the current coat is a full replacement of the South Park elevation, so
  it is recent, but nothing dates the colour itself.
- **The architect is a single source.** Ramon Zambrano appears on somapro.com's
  loft database and nowhere else found. Plausible — a broker who sold the units
  new — and uncontradicted, but one page.
- **The frontage: break or bow?** The survey resolves a straight segment, a ~30°
  corner and a 14° arc; the photographs read as a continuous curve. The model
  builds the arc as four facets and keeps the corner, because the survey is the
  survey. At 0.26 m of sagitta the difference is invisible at the app's camera;
  the corner is not.
- **The two loft tiers are assumed identical.** They photograph identically on the
  bowed plane, and the model repeats them exactly. Unit areas vary 929–1,196 ft²,
  so the interiors certainly do not.
