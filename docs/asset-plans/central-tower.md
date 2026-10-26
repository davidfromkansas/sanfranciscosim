# Central Tower — SF-SIM asset plan

The 1898 Call (Spreckels) Building at Market and Third, stripped of its Baroque dome and raised to 21 storeys in the 1937–38 Art Moderne remodel: a slim square tower of white piers and recessed grey window columns on a rose granite base, with one setback at the fifteenth floor.

**Deliverable:** `artifacts/central-tower/` (FiDi batch, ADDRESS-TO-ASSET stages 1–2, BATCH mode).

| | |
|---|---|
| Manifest id | `central-tower` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.4035852, 37.7871882` (OSM OBB centre, bbox-recentred by `tk.run`) |
| Target height | **91.0 m** — 91.0 m roof (Wikipedia 299 ft, published; LiDAR 88.6, OSM 91) |
| Footprint | OSM way 132127810: OBB 24.4 x 22.2 m, 538 m², bearing 45.4° |
| Triangle cap | 5,000 (FiDi batch, tower ≥ 60 m); built 1,570 |
| Category | `3` (office, `CAT.office` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Roof height | 91 m (299 ft) | published (Wikipedia) |
| Floors / built / remodel | 21 / 1898 / 1938 (Albert Roller) | published |
| LiDAR | 88.58 m | measured (DataSF 2010) |
| Footprint | OBB 24.4 x 22.2 m, 538 m², 5 nodes, bearing 45.4 | measured (OSM way 132127810) |
| Setback at ~62 m, ~3.5 m deep |  | estimated from the photo |

### Sources

- https://en.wikipedia.org/wiki/Central_Tower_(San_Francisco)
- https://commons.wikimedia.org/wiki/File:Central_Tower_San_Francisco.jpg
- https://www.openstreetmap.org/way/132127810
- https://data.sf.gov/resource/ynuv-fyni (2010 LiDAR building heights)

### Orientation

Square turned to the SoMa grid: faces bear 315 (Market), 45 (Third St), 135 and 225. Yaw 45 deg; +Y = true north. Small chamfer on the rear (south) corner kept in the base and shaft.

### What each side shows

- Market (NW) and Third (NE): white piers, recessed grey window columns, granite base with shopfronts (photo).
- Rear faces (SE/SW): same treatment (photo shows the side face matching; rear inferred).

### Recognition cues (ranked)

1. Slim square tower with one clean setback.
2. Strong vertical white piers / grey window columns.
3. Rose granite base.
4. Flat top over the narrower upper shaft.

### Massing recipe

- Granite base 0–12 m: shopfronts and a row of small windows.
- White shaft 12–62 m on the OSM plan: recessed concrete column quads, one glassd window per storey per column.
- Setback deck and rail at 62 m; upper shaft (square inset 3.5 m) to 89 m with the same bay system; parapet to 91 m.

### Palette

Toy_white, Toy_concrete (off-palette), Toy_glassd (off-palette), Toy_granite (off-palette), Toy_roofd, Toy_steel, Toy_stone; glow Toy_sand_Glow, Toy_white_Glow.

### Roof

Flat deck inside a white parapet with a small plant cluster; white crown light line.

### Triangle budget

1,570 tris (cap 5,000). Facades are flat outward quads over solid prisms (window columns, per-storey spandrels, ribbons); night lights are hashed quads aligned with the window bays.

### Draft manifest entry

```json
{
  "id": "central-tower",
  "file": "central-tower.glb",
  "anchor": [-122.4035852, 37.7871882],
  "targetHeightM": 91.0,
  "cat": 3,
  "name": "Central Tower (703 Market Street)",
  "estimated": false,
  "dims": [39.9676, 39.4503, 91.0],
  "tris": 1570,
  "loadRadius": 2730
}
```

### Integration notes

Case B: registry entry, exclusion of OSM way 132127810 (and its building:parts) from the procedural bake, re-bake. `dims` is the world-axis bbox including the apron. loadRadius = max(2500, 30 x 91.0) = 2730.

### Open risks

- Setback height and depth from one photo.
- The rooftop flagpole/mast is omitted (crest = roof parapet).
