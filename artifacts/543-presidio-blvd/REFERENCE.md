# 543 Presidio Blvd — reference dossier

Research behind `543-presidio-blvd.glb`. Compiled 12 August 2026. Everything here
was re-verified for the build; where it corrects
`docs/asset-plans/543-presidio-blvd.md`, the correction is called out and the
plan is wrong, not this file. Where this file and `REPORT.md` disagree, REPORT
wins — it records what actually shipped.

## 1. What the building is

A World War I–era officers' family residence on the west side of Presidio
Boulevard, in the Presidio of San Francisco, a few hundred metres inside Lombard
Gate. It is one of a row of near-identical Mission Revival houses — 540, 541,
542, 543, 544, 545, 546, 547, 548, 549 Presidio Boulevard — that step down the
hillside together, with the Sumner Avenue and Simonds Loop rows behind them.

Two storeys of pale stucco over a raised basement, under a low red clay-tile
hipped roof with deep eaves. Not a monument. The design brief this asset was
built to is **"the most legible house in a row of near-identical houses"**.

It is a *contributing* building type in the Presidio of San Francisco National
Historic Landmark District (National Register #66000232), which today counts 473
historic buildings; it is not individually listed or individually documented,
which is why nothing below cites a publication about *this* house specifically.

## 2. Sources, and what each establishes

| Source | Establishes |
|---|---|
| [OSM way/288361199](https://www.openstreetmap.org/way/288361199) | Footprint geometry (six vertices), address `543 Presidio Boulevard`, `building=yes`, `height=8`, `roof:shape=hipped`, `roof:colour=red` |
| [DataSF building footprints `ynuv-fyni`](https://data.sfgov.org/resource/ynuv-fyni), building `201006.0038392` | **Every height figure used.** 2010 LiDAR, 50 cm cells, 661 cells over the footprint: `gnd_min_m` 34.51, `gnd_mediancm` 3483, `hgt_maxcm` 955, `hgt_median_m` 8.21, `peak_1st_m` 44.36 |
| [Nominatim geocode](https://nominatim.openstreetmap.org/search?q=543+Presidio+Blvd) | One unambiguous result — no candidate ambiguity to resolve with the user |
| [Presidio Trust / RentCafe, Presidio Boulevard neighbourhood](https://www.rentcafe.com/apartments/ca/san-francisco/presidio-boulevard-neighborhood/default.aspx) | "Mission Revival", built for officers' families during World War I, four-bedroom duplex or single-family, basement, **detached** garage |
| [Presidio Residences, Simonds Loop neighbourhood](https://www.presidio-residences.com/apartments/ca/san-francisco/simonds-loop-neighborhood/index) | The adjacent row: Mission-style duplexes and single-family houses built as officer housing before WWII — corroborates the type |
| [NPS, Presidio architecture](https://www.nps.gov/articles/presidio-architecture.htm) | 473 historic contributing buildings; the Presidio's stucco-and-tile military vocabulary |
| [National Register #66000232](https://noehill.com/sf/landmarks/nat1966000232.aspx) | NHL District listing and its officers'-family-housing inventory |
| Google Maps aerial and street-level imagery at 37.79737, −122.45158 | Visual observation only: roof form, eave depth, entry porch, window rhythm, terracing, absence of dormers. No imagery reproduced or committed. |

## 3. Verified dimensions and location

Footprint measured from the OSM way pulled directly from the Overpass API,
reprojected with the repo's local tangent projection
(`x=(lon−LON0)·111320·cos(LAT0)`, `z=−(lat−LAT0)·110540`, LON0 −122.4375,
LAT0 37.77), then reduced to a minimum-area oriented bounding box.

| | Value | Confidence |
|---|---|---|
| Footprint OBB | 13.72 m × 12.79 m | **measured** |
| Footprint area | 165.8 m² (OSM) / 165.0 m² (DataSF) | **measured**, two independent surveys agreeing to 0.5% |
| Rear corner notch | 2.70 m × 3.45 m, cut from the NNE rear corner | **measured** |
| Footprint OBB centre | `−122.4515779, 37.7973711` | **measured** |
| Model anchor (after `recentre()`) | `−122.4515730, 37.7973711` | **measured** — see REPORT §anchor |
| Front-wall bearing | 10.7° / 190.7° true | **measured** from the six polygon edges (they agree to 0.15°) |
| Street elevation faces | 100.7° true (ESE) | **measured** — the nearest Presidio Boulevard centreline node is 32.6 m away in exactly that direction |
| Ground elevation | 34.51 m NAVD88 min, 34.83 m median | **measured** (DataSF) |
| **Crest above grade** | **9.55 m** | **measured** (DataSF `hgt_maxcm` = 955) |
| Median roof height | 8.21 m | **measured** (DataSF) |
| Eave line | 7.00 m | *inferred* — see §4 |
| Roof ridge | 9.15 m | *inferred* — see §4 |

### Identifying the right DataSF record

Four LiDAR buildings sit within 45 m. The match is unambiguous:

| DataSF id | Distance from OSM centroid | Area | `hgt_max` | Reading |
|---|---|---|---|---|
| **201006.0038392** | **0.8 m** | **165.0 m²** | **9.55 m** | **543 — this building** |
| 201006.0016579 | 26.5 m | 248.7 m² | 9.95 m | a neighbouring larger house (duplex type) |
| 201006.0016699 | 24.4 m | 247.5 m² | 9.86 m | ditto |
| 201006.0135922 | 33.3 m | 95.0 m² | 4.82 m | a garage |

The 165 m² footprint against ~248 m² for both immediate neighbours is the
evidence that 543 is the smaller *single-family* type rather than the duplex.
That is an inference, and the model does not depend on it.

## 4. The height problem, and how it was resolved

**OSM's `height=8` is not the building's height.** It reproduces DataSF's
`hgt_median_m` of 8.21 — the *median* of the LiDAR height raster over the
footprint. For a hipped roof the median surface height falls, by construction,
somewhere between the eave and the ridge. Using it as `targetHeightM` would sink
the house 1.55 m into the terrain relative to its real crest. This is the exact
failure mode `docs/asset-plans/README.md` warns about, and this building is now
its second worked example.

There is no published architectural height for an individual Presidio residence,
so the storey breakdown is inferred to fit the one hard measurement:

| Level | Height | Basis |
|---|---|---|
| Exposed raised basement | 0.90 m | *inferred* |
| Ground floor | 3.10 m → 4.00 m | *inferred* |
| Second floor | 3.00 m → **7.00 m eave** | *inferred* |
| Hip roof over the 13.89 m eave-line cross span | +2.15 m → **9.15 m ridge** | *inferred* (≈4.25:12) |
| Chimney | → **9.55 m crest** | **measured** |

**The check that makes this defensible:** a hip whose surface runs from 7.00 m to
9.15 m over this footprint has a median surface height of roughly 8.1–8.2 m.
DataSF's independently measured `hgt_median_m` is **8.21 m**. The inferred split
reproduces the one number it was not fitted to. It is still inferred and is
labelled so everywhere.

**What is *not* resolved:** whether `hgt_maxcm` = 955 is the chimney or the ridge.
The build assumes chimney. If it is the ridge, the roof is slightly steeper and
the chimney rises above it — but the *bounding-box top is 9.55 m either way*, so
`targetHeightM` and the loader's scale factor are unaffected. It is a shape
question, not a scale one.

## 5. What each side shows

Local frame: **u** along the front wall, positive toward the SSW (bearing 190.7°);
**v** across, positive toward Presidio Boulevard (bearing 100.7°). Origin at the
footprint OBB centre.

```
        rear / WNW  (v = -6.39)
   +--------------------+          notch: u -6.86..-4.16
   |                    |                 v -6.39..-2.94
   |     +--------------+
   |     |
NNE|     |              |SSW        u = -6.86  ...  u = +6.86
(u=-6.86)|              |(u=+6.86)
   |     |              |
   +-----+--------------+
        front / ESE  (v = +6.40)  -> Presidio Boulevard
              13.72 m
```

**ESE — the street front (v = +6.40).** The hero elevation. 13.72 m of
symmetrical pale stucco, two tiers of double-hung windows, a projecting
one-storey entry porch on the centre line under its own small hip, and the deep
eave shadow above. The house stands on its exposed basement above a terraced
lawn reached by a concrete stair from the sidewalk (out of scope).

**SSW flank (u = +6.86).** Full 12.79 m depth, faces 541 Presidio Blvd. Quiet:
two tiers of windows, no entrance.

**WNW — the rear (v = −6.39).** Only 11.02 m wide because of the notch. Plainer,
service side.

**NNE flank (u = −6.86).** 9.34 m of wall (the notch removes the rear 3.45 m),
faces 545 Presidio Blvd. The chimney is on this half of the roof.

**Top.** The surface that matters most, because the app's camera looks down. A
near-pyramidal red clay-tile hip: over the 14.82 × 13.89 m eave rectangle the
ridge is only 0.93 m long, so the roof reads as four large triangles meeting
almost at a point. Deep overhang all round. Ridge and hip caps. One chimney.
**No dormers** — none are visible in the aerial imagery.

## 6. Recognition cues (ranked)

1. **The near-pyramidal red tile hip.** From the app's camera, this is the building.
2. A compact, almost square pale block standing slightly proud of its ground.
3. Deep eaves throwing a hard shadow line all the way round.
4. The projecting entry porch on the street front.
5. The single chimney breaking the roof plane.

## 7. Preserve / simplify

**Preserve**

- The near-square 13.72 × 12.79 m proportion. Do not stretch it.
- The rear corner notch — 6% of the footprint, and what distinguishes this house
  from its neighbours in plan.
- The hip's four-plane geometry as real geometry, not a bevelled plane.
- Restraint. Style bible §21 "secondary building" budget, not hero.

**Simplify / exaggerate**

- Individual tiles → one flat `Toy_red` surface. The *shape* carries the read;
  the ridge and hip caps carry the material.
- ~20 double-hung windows → 17 identical recessed openings on a regular grid.
- Porch columns and rails → two chunky posts, a flat canopy, a small hip, a step.
- Eave overhang exaggerated to 0.62 m with a 0.42 m fascia so the shadow reads at
  20 px.
- Terracing, retaining wall, garage, planting → omitted entirely.

## 8. Uncertainties and conflicting evidence

- **Sources do not conflict.** OSM and DataSF agree on the footprint to 0.5% and
  on the median height to 0.01 m; the apparent OSM/DataSF "disagreement" on
  height is not a disagreement at all, it is OSM importing the median (§4).
- The eave/ridge split is *inferred*, checked against the measured median.
- Single-family vs duplex is *inferred* from footprint area.
- Whether the LiDAR maximum is the chimney or the ridge is *unresolved*, and does
  not affect the shipped height.
- Published material describes the Presidio Boulevard row's era and style but
  says nothing about this individual house. Every architectural statement here is
  either measured, type-level, or visual.
- 2010 LiDAR is 16 years old. For a contributing building in an NHL District
  under Presidio Trust stewardship, the massing is very unlikely to have changed.

## 9. Out of scope

The detached garage (a separate DataSF footprint, `201006.0135922`, 4.8 m tall),
the terraced lawn, the retaining wall and its stair, Presidio Boulevard, the
neighbouring houses at 541 and 545, all planting, vehicles, people, display
plinths, cameras and lights. The raised basement band **is** part of the building
and is in scope; it also hides the terrain seam.
