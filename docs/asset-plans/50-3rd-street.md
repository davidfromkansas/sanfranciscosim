# Hyatt Regency San Francisco Downtown SOMA — SF-SIM asset plan

The 36-storey 1983 hotel at 50 Third Street (Meridien, ANA, Argent, Westin, Park Central; Hyatt Regency since 2022): a pale precast slab on an elongated hexagonal plan, 13-storey triangular wings at its ends and a three-storey podium filling the diamond-shaped lot, overlooking Yerba Buena Gardens.

**Deliverable:** `artifacts/50-3rd-street/` (FiDi batch, ADDRESS-TO-ASSET stages 1–2, BATCH mode).

| | |
|---|---|
| Manifest id | `50-3rd-street` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.4030905, 37.7865616` (OSM OBB centre, bbox-recentred by `tk.run`) |
| Target height | **114.0 m** — 114.0 m roof (Wikipedia 374 ft, published; LiDAR max 118.6 incl. roof plant; OSM part 129) |
| Footprint | OSM way 118480404: OBB 58.5 x 56.5 m, 3275 m², bearing 45.1° |
| Triangle cap | 5,000 (FiDi batch, tower ≥ 60 m); built 3,570 |
| Category | `7` (hotel, `CAT.hotel` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Height | 114 m (374 ft) | published (Wikipedia infobox) |
| Floors / opened / architect | 36 / 1983 / Hornberger + Worstell | published |
| LiDAR | 118.6 m max, 14.3 m majority (podium) | measured (DataSF 2010, record SF3706074); the per-building facts value 67.2 m is a different record and is wrong |
| Massing | tower 36 levels, wings 13 levels, podium 3 levels | OSM building:parts 436648856, 1240818460–463 |
| Wing height 46 m |  | estimated from 13 levels |
| Footprint | OBB 58.5 x 56.5 m, 3,275 m² | measured (OSM way 118480404) |

### Sources

- https://en.wikipedia.org/wiki/Hyatt_Regency_San_Francisco_Downtown_SOMA
- https://commons.wikimedia.org/wiki/File:San_Francisco_skyscrapers_seen_from_Yerba_Buena_gardens.jpg
- https://www.openstreetmap.org/way/118480404
- https://data.sf.gov/resource/ynuv-fyni (2010 LiDAR building heights)

### Orientation

The lot is a diamond on the SoMa grid (bearing 45); the tower part is an E–W hexagon across it. Third Street = SW edges, Jessie/Mission side = N. +Y = true north; parts used directly from OSM.

### What each side shows

- Long N and S tower faces: pale precast, punched windows, vertical piers (photo shows the Yerba Buena side at a distance).
- Wings and podium: same skin (inferred detail).

### Recognition cues (ranked)

1. Tall pale slab with flat top among the Yerba Buena towers.
2. Hexagonal plan with lower triangular wings.
3. Punched hotel windows.

### Massing recipe

- Podium parts 0–13 m (stone, shopfront + window rows).
- Wings 0–46 m.
- Tower 0–108 m: window columns + per-storey spandrels, trim piers on long faces.
- Parapet, deck, penthouse to 114 m with a light band.

### Palette

Toy_sand, Toy_stone, Toy_trim, Toy_glass, Toy_glassd (off-palette), Toy_roofd, Toy_steel; glow Toy_sand_Glow.

### Roof

Dark deck with trim parapet and a central penthouse; podium and wing roofs in steel/trim.

### Triangle budget

3,570 tris (cap 5,000). Facades are flat outward quads over solid prisms (window columns, per-storey spandrels, ribbons); night lights are hashed quads aligned with the window bays.

### Draft manifest entry

```json
{
  "id": "50-3rd-street",
  "file": "50-3rd-street.glb",
  "anchor": [-122.4030905, 37.7865616],
  "targetHeightM": 114.0,
  "cat": 7,
  "name": "Hyatt Regency Downtown SOMA (50 Third Street)",
  "estimated": false,
  "dims": [86.8477, 84.8809, 114.0],
  "tris": 3570,
  "loadRadius": 3420
}
```

### Integration notes

Case B: registry entry, exclusion of OSM way 118480404 (and its building:parts) from the procedural bake, re-bake. `dims` is the world-axis bbox including the apron. loadRadius = max(2500, 30 x 114.0) = 3420.

### Open risks

- Only a distant photo; facade detail is generic.
- OSM part height 129 m disagrees with published 114 m and LiDAR 118.6 m.
- Wing heights estimated.
