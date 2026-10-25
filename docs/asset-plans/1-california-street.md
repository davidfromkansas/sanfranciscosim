# One California Street — SF-SIM asset plan

Welton Becket Associates' 1969 tower where California Street meets Market and Drumm: a chamfered-corner square of tall white piers running unbroken from the base to a solid white crown band, dark glass between them, and one of the few rooftop company signs left downtown.

**Deliverable:** `artifacts/1-california-street/` (FiDi batch, ADDRESS-TO-ASSET stages 1–2, BATCH mode).

| | |
|---|---|
| Manifest id | `1-california-street` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.3971792, 37.7932326` (OSM OBB centre, bbox-recentred by `tk.run`) |
| Target height | **133.5 m** — 133.5 m roof (Wikipedia 438 ft, published; LiDAR 135.2, OSM 140) |
| Footprint | OSM way 32612471: OBB 44.2 x 42.7 m, 1841 m², bearing 170.5° |
| Triangle cap | 5,000 (FiDi batch, tower ≥ 60 m); built 2,762 |
| Category | `3` (office, `CAT.office` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Roof height | 133.5 m (438 ft) | published (Wikipedia) |
| Floors / year / architect | 32 / 1969 / Welton Becket Associates | published |
| LiDAR | 135.19 m | measured (DataSF 2010) |
| Footprint | OBB 44.2 x 42.7 m, 1,841 m², 9 nodes, chamfered corners | measured (OSM way 32612471) |
| Crown band ~126–133.5 m |  | estimated from the photo |

### Sources

- https://en.wikipedia.org/wiki/One_California_Street
- https://commons.wikimedia.org/wiki/File:One_California_2021_Front.jpg
- https://www.openstreetmap.org/way/32612471
- https://data.sf.gov/resource/ynuv-fyni (2010 LiDAR building heights)

### Orientation

FiDi grid (bearing 170.5): faces bear ~80, 170, 260, 350; chamfered corners. Sign panels on the S and E faces (toward Market). +Y = true north.

### What each side shows

- All faces: white piers, dark glass, white crown (photo shows two faces; others inferred).
- Sign: red + navy panel high on the S and E faces (generic, no lettering).

### Recognition cues (ranked)

1. White pinstripe piers over dark glass.
2. Solid white crown band with the sign.
3. Chamfered corners.

### Massing recipe

- Recessed glassd lobby 0–9 m, white transfer band.
- Glass shaft to 126 m with white pier boxes every 3.6 m (deep, from the ground), thin per-storey mullion lines.
- Hollow white crown ring 126–133.5 m around a deck and plant; sign panels with glow.

### Palette

Toy_white, Toy_glass, Toy_glassd (off-palette), Toy_red, Toy_navy, Toy_roofd, Toy_steel, Toy_stone; glow Toy_sand_Glow, Toy_white_Glow, Toy_red_Glow, Toy_navy_Glow.

### Roof

Plant inside the crown ring (visible from above).

### Triangle budget

2,762 tris (cap 5,000). Facades are flat outward quads over solid prisms (window columns, per-storey spandrels, ribbons); night lights are hashed quads aligned with the window bays.

### Draft manifest entry

```json
{
  "id": "1-california-street",
  "file": "1-california-street.glb",
  "anchor": [-122.3971792, 37.7932326],
  "targetHeightM": 133.5,
  "cat": 3,
  "name": "One California",
  "estimated": false,
  "dims": [54.3742, 54.8593, 133.5],
  "tris": 2762,
  "loadRadius": 4005
}
```

### Integration notes

Case B: registry entry, exclusion of OSM way 32612471 (and its building:parts) from the procedural bake, re-bake. `dims` is the world-axis bbox including the apron. loadRadius = max(2500, 30 x 133.5) = 4005.

### Open risks

- Sign faces inferred; the current tenant sign is shown as plain coloured panels, no brand.
- Lobby treatment simplified.
