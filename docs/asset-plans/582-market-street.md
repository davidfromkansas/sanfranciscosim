# Hobart Building — SF-SIM asset plan

Willis Polk's 1914 terracotta tower at the head of Second Street: a 21-storey tan rusticated slab on an asymmetric lot whose west flank has stood sheer and blank since its neighbour came down in 1967, rising into a round-ended upper tower with arched windows, a deep Baroque cornice and a low crowning roof.

**Deliverable:** `artifacts/582-market-street/` (FiDi batch, ADDRESS-TO-ASSET stages 1–2, BATCH mode).

| | |
|---|---|
| Manifest id | `582-market-street` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.4016363, 37.7894660` (OSM OBB centre, bbox-recentred by `tk.run`) |
| Target height | **87.0 m** — 87.0 m roof (Wikipedia 285 ft, published; LiDAR 86.7, OSM 86) |
| Footprint | OSM way 32946628: OBB 49 x 23.1 m, 677 m², bearing 171.6° |
| Triangle cap | 5,000 (FiDi batch, tower ≥ 60 m); built 2,156 |
| Category | `3` (office, `CAT.office` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Roof height | 87 m (285 ft) | published (Wikipedia) |
| Floors / year / architect | 21 / 1914 / Willis Polk | published |
| LiDAR | 86.67 m | measured (DataSF 2010) |
| Footprint | OBB 49.0 x 23.1 m, 677 m², 8 nodes | measured (OSM way 32946628) |
| Slab/tower split ~58 m (14th floor) |  | estimated from the photo |
| Rear wing 32 m |  | inferred (not in the photo) |

### Sources

- https://en.wikipedia.org/wiki/Hobart_Building
- https://commons.wikimedia.org/wiki/File:2017_Hobart_Building_582-92_Market_Street_closeup.jpg
- https://www.openstreetmap.org/way/32946628
- https://data.sf.gov/resource/ynuv-fyni (2010 LiDAR building heights)

### Orientation

The lot is an irregular polygon: a trapezoid on Market (SE face, bearing ~225/45) with a narrow rear part reaching north along the east party line. Model frame: u along Market (bearing 45), v to the NW; yaw 45 deg. +Y = true north.

### What each side shows

- SE (Market): rusticated terracotta, punched windows, glazed shopfronts (photo, right face).
- W flank: sheer and blank with the painted HOBART BUILDING sign (photo, left face) — modelled as a dark sign panel.
- E and NW (rear court): windowed like Market (inferred).
- Upper tower: semicircular west end, arched top storey, deep cornice (photo).

### Recognition cues (ranked)

1. Round-ended upper tower with a heavy cornice and crowning roof.
2. Sheer blank west flank with the sign.
3. Tan rusticated terracotta, punched windows.
4. Slim, offset silhouette next to 1 Montgomery / 44 Montgomery.

### Massing recipe

- Front trapezoid (OSM split at the back of the slab) 0–58 m: terracotta prism, shopfront base, window columns under per-storey rustication quads; no windows on the west edge.
- Rear part 0–32 m: plain stone block with punched windows (height inferred).
- Upper tower 57.5–79 m: Market-frame outline flush with the Market face, east end on the party line, semicircular west end; 4 storeys of windows, cream band, arched storey, cornice 79–81.4 m, attic, verdigris hipped roof and gold finial to 87 m.

### Palette

Toy_terracotta (off-palette, warm tan), Toy_stone, Toy_cream, Toy_glassd (off-palette), Toy_ink (sign), Toy_verdigris, Toy_gold, Toy_roofd; glow Toy_sand_Glow.

### Roof

Low verdigris hipped roof with a finial over the cornice; flat dark decks on the slab and rear wing.

### Triangle budget

2,156 tris (cap 5,000). Facades are flat outward quads over solid prisms (window columns, per-storey spandrels, ribbons); night lights are hashed quads aligned with the window bays.

### Draft manifest entry

```json
{
  "id": "582-market-street",
  "file": "582-market-street.glb",
  "anchor": [-122.4016363, 37.789466],
  "targetHeightM": 87.0,
  "cat": 3,
  "name": "Hobart Building (582 Market Street)",
  "estimated": false,
  "dims": [27.5354, 55.828, 87.0],
  "tris": 2156,
  "loadRadius": 2610
}
```

### Integration notes

Case B: registry entry, exclusion of OSM way 32946628 (and its building:parts) from the procedural bake, re-bake. `dims` is the world-axis bbox including the apron. loadRadius = max(2500, 30 x 87.0) = 2610.

### Open risks

- Which OSM part carries the upper tower is read from one photo; the tower outline is fitted into the front part.
- Rear wing height (32 m) is inferred.
- The roof form above the cornice is simplified to a low hip.
