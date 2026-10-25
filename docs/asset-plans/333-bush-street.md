# 333 Bush Street — SF-SIM asset plan

SOM's 1986 rose granite tower on Bush near Kearny: 43 storeys of punched windows with greenish glass on an L-shaped plan whose south-west corner steps back in a staircase, a dark louvred band where the offices stop, and a terraced "ziggurat" of setback boxes over the condominium floors.

**Deliverable:** `artifacts/333-bush-street/` (FiDi batch, ADDRESS-TO-ASSET stages 1–2, BATCH mode).

| | |
|---|---|
| Manifest id | `333-bush-street` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.4030673, 37.7905789` (OSM OBB centre, bbox-recentred by `tk.run`) |
| Target height | **151.0 m** — 151.0 m roof (Wikipedia 495 ft, published; LiDAR 150.45, OSM 151) |
| Footprint | OSM way 132125167: OBB 51.9 x 46.3 m, 1956 m², bearing 170.6° |
| Triangle cap | 5,000 (FiDi batch, tower ≥ 60 m); built 4,464 |
| Category | `3` (office, `CAT.office` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Roof height | 151 m (495 ft) | published (Wikipedia) |
| Floors / year / architect | 43 / 1986 / SOM | published |
| Use | offices + seven condominium floors | published |
| LiDAR | 150.45 m | measured (DataSF 2010) |
| Footprint | OBB 51.9 x 46.3 m, 1,956 m², 38 nodes (cleaned to the staircase corners) | measured (OSM way 132125167) |
| Terraces start ~117 m (louvre band 113–117) |  | estimated from the photo |

### Sources

- https://en.wikipedia.org/wiki/333_Bush_Street
- https://commons.wikimedia.org/wiki/File:555_California_Street_and_333_Bush_Street_from_One_Montgomery,_San_Francisco.jpg
- https://www.openstreetmap.org/way/132125167
- https://data.sf.gov/resource/ynuv-fyni (2010 LiDAR building heights)

### Orientation

FiDi grid, OBB axis bearing 170.6. Bush Street = N face; the staircase steps cut the SW corner. Tiers are notched rectangles in the tower frame, biased NE (photo). +Y = true north.

### What each side shows

- N (Bush) and E: rose granite, punched windows (photo shows two faces).
- SW stepped corner: the staircase plan, same skin.
- Top: terraced setbacks on all sides (photo; rear inferred).

### Recognition cues (ranked)

1. Terraced ziggurat top.
2. Rose granite with a dense punched-window grid.
3. Stepped (sawtooth) corner.
4. Dark louvre band at the transition.

### Massing recipe

- Granite base 0–9 m with glazed shopfronts.
- Shaft 9–117 m on the cleaned OSM plan: glassd window columns + per-storey granite spandrel quads.
- Bronze louvre band 113–117 m.
- Four notch-rect tiers 117–147 m stepping in, each with decks and rails; crown box to 151 m.

### Palette

Toy_granite (off-palette), Toy_glassd (off-palette), Toy_bronze (off-palette), Toy_stone, Toy_roofd, Toy_steel; glow Toy_sand_Glow.

### Roof

Stepped terrace decks with stone rails; small crown box with a light band.

### Triangle budget

4,464 tris (cap 5,000). Facades are flat outward quads over solid prisms (window columns, per-storey spandrels, ribbons); night lights are hashed quads aligned with the window bays.

### Draft manifest entry

```json
{
  "id": "333-bush-street",
  "file": "333-bush-street.glb",
  "anchor": [-122.4030673, 37.7905789],
  "targetHeightM": 151.0,
  "cat": 3,
  "name": "333 Bush Street",
  "estimated": false,
  "dims": [58.7734, 57.6589, 151.0],
  "tris": 4464,
  "loadRadius": 4530
}
```

### Integration notes

Case B: registry entry, exclusion of OSM way 132125167 (and its building:parts) from the procedural bake, re-bake. `dims` is the world-axis bbox including the apron. loadRadius = max(2500, 30 x 151.0) = 4530.

### Open risks

- Tier sizes and positions from one oblique photo.
- OSM levels 43 matches published; tier storey count simplified.
