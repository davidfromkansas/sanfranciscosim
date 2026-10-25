# 100 Pine Center — SF-SIM asset plan

Hertzka & Knowles' 1972 tower at the north-west corner of Pine and Front: a 33-storey box of continuous horizontal bands, cream metal spandrels and dark bronze ribbon windows, with corners notched back in steps.

**Deliverable:** `artifacts/100-pine-center/` (FiDi batch, ADDRESS-TO-ASSET stages 1–2, BATCH mode).

| | |
|---|---|
| Manifest id | `100-pine-center` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.3990118, 37.7926485` (OSM OBB centre, bbox-recentred by `tk.run`) |
| Target height | **145.0 m** — 145.0 m roof (Wikipedia 145.09 m / 476 ft, published; LiDAR 144.4, OSM 145) |
| Footprint | OSM way 944025918: OBB 40.7 x 38.5 m, 1473 m², bearing 170.5° |
| Triangle cap | 5,000 (FiDi batch, tower ≥ 60 m); built 2,820 |
| Category | `3` (office, `CAT.office` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Roof height | 145.09 m (476 ft) | published (Wikipedia) |
| Floors / year | 33 / 1972 | published |
| LiDAR | 144.4 m | measured (DataSF 2010) |
| Footprint | OBB 40.7 x 38.5 m, 1,473 m², notched corners | measured (OSM way 944025918) |

### Sources

- https://en.wikipedia.org/wiki/100_Pine_Center
- https://commons.wikimedia.org/wiki/File:100_Pine_Center.jpg
- https://www.openstreetmap.org/way/944025918
- https://data.sf.gov/resource/ynuv-fyni (2010 LiDAR building heights)

### Orientation

FiDi grid (bearing 170.5). Pine = S face, Front = E face. +Y = true north; OSM plan cleaned of collinear nodes.

### What each side shows

- All four faces: cream bands and bronze ribbon windows (photo shows two faces and a notched corner; the others inferred identical).

### Recognition cues (ranked)

1. Strong horizontal banding.
2. Stepped/notched corners.
3. Flat top, cream colour.

### Massing recipe

- Recessed glassd lobby 0–8 m with cream columns.
- Cream shaft 8–141 m with one bronze ribbon quad per storey per face.
- Cream screen to 145 m around a deck and plant; white crown line.

### Palette

Toy_cream, Toy_bronze (off-palette), Toy_glassd (off-palette), Toy_roofd, Toy_steel, Toy_stone; glow Toy_sand_Glow, Toy_white_Glow.

### Roof

Plant cluster inside a cream screen wall.

### Triangle budget

2,820 tris (cap 5,000). Facades are flat outward quads over solid prisms (window columns, per-storey spandrels, ribbons); night lights are hashed quads aligned with the window bays.

### Draft manifest entry

```json
{
  "id": "100-pine-center",
  "file": "100-pine-center.glb",
  "anchor": [-122.3990118, 37.7926485],
  "targetHeightM": 145.0,
  "cat": 3,
  "name": "100 Pine Center",
  "estimated": false,
  "dims": [48.984, 49.0617, 145.0],
  "tris": 2820,
  "loadRadius": 4350
}
```

### Integration notes

Case B: registry entry, exclusion of OSM way 944025918 (and its building:parts) from the procedural bake, re-bake. `dims` is the world-axis bbox including the apron. loadRadius = max(2500, 30 x 145.0) = 4350.

### Open risks

- Lobby treatment inferred.
- Roof screen height assumed (crest = published roof).
