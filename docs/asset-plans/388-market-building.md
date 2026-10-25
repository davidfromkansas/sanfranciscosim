# 388 Market Street — SF-SIM asset plan

SOM's 1987 flatiron on the triangle of Market, Pine and Front: a red granite wedge with a fully rounded west end, a slim rounded prow of stacked glass bays at the east tip, a sheer dark glass wall on Pine that sweeps over the upper floors of the Market face, and a two-storey pavilion at the Market/Front corner.

**Deliverable:** `artifacts/388-market-building/` (FiDi batch, ADDRESS-TO-ASSET stages 1–2, BATCH mode).

| | |
|---|---|
| Manifest id | `388-market-building` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.3980735, 37.7921812` (OSM OBB centre, bbox-recentred by `tk.run`) |
| Target height | **111.9 m** — 111.9 m roof (DataSF LiDAR; Wikipedia's 94 m / 308 ft conflicts, OSM 118) |
| Footprint | OSM way 1279504526: OBB 78.4 x 33.5 m, 1590 m², bearing 48° |
| Triangle cap | 5,000 (FiDi batch, tower ≥ 60 m); built 3,468 |
| Category | `3` (office, `CAT.office` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Roof height | 111.9 m | measured (DataSF 2010 LiDAR, per-building facts; footprint query max 114.5, median 109.3) |
| Published height | 94 m (308 ft) | published (Wikipedia) — rejected: 24 storeys at 94 m is plausible on paper but the LiDAR roof over the whole footprint is ~109–112 m |
| Floors / year / architect | 24 / 1987 / SOM | published |
| Cladding | red granite | published (Wikipedia) |
| Footprint | OBB 78.4 x 33.5 m, 1,590 m²; tower part 24 levels + 2-level corner part | measured (OSM way 1279504526, parts 288505730 / 288505726) |
| Glass sheath starts ~66 m on Market |  | estimated from the photo |

### Sources

- https://en.wikipedia.org/wiki/388_Market_Street
- https://commons.wikimedia.org/wiki/File:388_Market_Street,_San_Francisco_2021.jpg
- https://www.openstreetmap.org/way/1279504526
- https://data.sf.gov/resource/ynuv-fyni (2010 LiDAR building heights)

### Orientation

Long axis bearing 48 deg along Market. Market = SE face, Pine = N face (bearing ~81 edge), Front = W rounded end; the east prow points to Battery/Market. +Y = true north; plan used directly from OSM (arcs thinned).

### What each side shows

- SE (Market): granite with punched windows, upper floors under the glass sheath (photo).
- N (Pine): sheer dark glass (photo, right face).
- E prow: stacked glass bays between thin granite bands (photo).
- W rounded end at Front/Pine: granite punched windows (inferred).

### Recognition cues (ranked)

1. Flatiron wedge with a slim rounded prow.
2. Red granite against dark glass.
3. Rounded west end.
4. Glass sheath sweeping over the Market face.

### Massing recipe

- Corner pavilion (OSM part) 0–9 m, granite with shopfronts.
- Tower part: granite prism 0–110.4 m; window columns + per-storey granite spandrels on granite faces; glass quad on the Pine face; glass veil on the Market face 66 m–roof; per-storey glass bays on the prow.
- Granite parapet to 111.9 m, dark deck, small plant, white crown line.

### Palette

Toy_rust (red granite), Toy_glass, Toy_glassd (off-palette), Toy_roofd, Toy_steel, Toy_stone; glow Toy_sand_Glow, Toy_white_Glow.

### Roof

Flat dark deck inside a granite parapet, low plant cluster along the spine.

### Triangle budget

3,468 tris (cap 5,000). Facades are flat outward quads over solid prisms (window columns, per-storey spandrels, ribbons); night lights are hashed quads aligned with the window bays.

### Draft manifest entry

```json
{
  "id": "388-market-building",
  "file": "388-market-building.glb",
  "anchor": [-122.3980735, 37.7921812],
  "targetHeightM": 111.9,
  "cat": 3,
  "name": "388 Market Street",
  "estimated": false,
  "dims": [64.7478, 58.1355, 111.9],
  "tris": 3468,
  "loadRadius": 3357
}
```

### Integration notes

Case B: registry entry, exclusion of OSM way 1279504526 (and its building:parts) from the procedural bake, re-bake. `dims` is the world-axis bbox including the apron. loadRadius = max(2500, 30 x 111.9) = 3357.

### Open risks

- Height: published 94 m vs LiDAR ~112 m vs OSM 118 m — LiDAR chosen; the lead may want to confirm.
- The diagonal edge of the glass sheath is simplified to a horizontal start at 66 m.
- West end treatment inferred.
