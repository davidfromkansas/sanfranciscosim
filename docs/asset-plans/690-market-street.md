# Old Chronicle Building (Ritz-Carlton Club and Residences) — SF-SIM asset plan

San Francisco's first skyscraper (Burnham and Root, 1890; rebuilt by Willis Polk after 1906): a red-brick Richardsonian Romanesque block on a rusticated brownstone base with a tall arcade of round-arched windows, restored in 2005–07 with a beige residential addition stacked on top in tiers under deep dark cornices.

**Deliverable:** `artifacts/690-market-street/` (FiDi batch, ADDRESS-TO-ASSET stages 1–2, BATCH mode).

| | |
|---|---|
| Manifest id | `690-market-street` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.4032006, 37.7882605` (OSM OBB centre, bbox-recentred by `tk.run`) |
| Target height | **95.0 m** — 95.0 m roof (Wikipedia 312 ft, published; LiDAR max 100.7 / median 96.0, OSM 66 = the 1890 clock tower) |
| Footprint | OSM way 32946675: OBB 39.5 x 39.3 m, 1110 m², bearing 170.6° |
| Triangle cap | 5,000 (FiDi batch, tower ≥ 60 m); built 3,938 |
| Category | `2` (apartments, `CAT.apartments` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Roof height | 95 m (312 ft) | published (Wikipedia) |
| Floors | 24 | published |
| Built / renovated | 1890 / 1906, 1962, 2005–07 | published |
| LiDAR | 100.7 m max, 96.0 m median | measured (DataSF 2010, record SF0311016) |
| Footprint | OBB 39.5 x 39.3 m, 1,110 m², 11 nodes | measured (OSM way 32946675) |
| Historic block top ~53 m; addition tiers |  | estimated from the photo |

### Sources

- https://en.wikipedia.org/wiki/De_Young_Building
- https://commons.wikimedia.org/wiki/File:Ritz-Carlton_Club_and_Residences,_San_Francisco_2021.jpg
- https://www.openstreetmap.org/way/32946675
- https://data.sf.gov/resource/ynuv-fyni (2010 LiDAR building heights)

### Orientation

At the junction of Market (SE face), Kearny (W) and Geary (S). Plan used directly from OSM (cleaned). +Y = true north.

### What each side shows

- Market and Kearny: brick, arcade, brownstone base (photo).
- Rear/north faces: same treatment (inferred).
- Addition: beige, ribbon-ish windows, dark eaves (photo).

### Recognition cues (ranked)

1. Red brick block with the round-arched arcade.
2. Beige tiered addition with dark projecting cornices on top.
3. Brownstone rusticated base.

### Massing recipe

- Brownstone base 0–9 m with shopfronts.
- Brick block 9–53 m: punched windows, arcade of arched panes 28.6–41.5 m, verdigris cornice.
- Three sand tiers 53–93.4 m stepping in 0.8/1.8/2.8 m, each under an ink eave; roof deck and plant to 95 m.

### Palette

Toy_brick, Toy_rust, Toy_terracotta (off-palette), Toy_verdigris, Toy_sand, Toy_ink, Toy_glassd/glassl, Toy_roofd, Toy_steel, Toy_stone; glow Toy_sand_Glow.

### Roof

Flat deck with a low plant cluster inside the top eave.

### Triangle budget

3,938 tris (cap 5,000). Facades are flat outward quads over solid prisms (window columns, per-storey spandrels, ribbons); night lights are hashed quads aligned with the window bays.

### Draft manifest entry

```json
{
  "id": "690-market-street",
  "file": "690-market-street.glb",
  "anchor": [-122.4032006, 37.7882605],
  "targetHeightM": 95.0,
  "cat": 2,
  "name": "Old Chronicle Building (690 Market Street)",
  "estimated": false,
  "dims": [47.1894, 46.4498, 95.0],
  "tris": 3938,
  "loadRadius": 2850
}
```

### Integration notes

Case B: registry entry, exclusion of OSM way 32946675 (and its building:parts) from the procedural bake, re-bake. `dims` is the world-axis bbox including the apron. loadRadius = max(2500, 30 x 95.0) = 2850.

### Open risks

- Addition massing simplified to concentric tiers; the real one steps irregularly.
- Arcade floors and band heights from one photo.
