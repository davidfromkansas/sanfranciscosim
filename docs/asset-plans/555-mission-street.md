# 555 Mission Street — SF-SIM asset plan

Kohn Pedersen Fox's 2008 office tower on the south side of Mission between First and Second: a 33-storey pale blue glass prism with fine silvery mullions, notched corners, a tall glass lobby on the Mission plaza and a glass screen crown over the roof plant.

**Deliverable:** `artifacts/555-mission-street/` (FiDi batch, ADDRESS-TO-ASSET stages 1–2, BATCH mode).

| | |
|---|---|
| Manifest id | `555-mission-street` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.3985546, 37.7885452` (OSM OBB centre, bbox-recentred by `tk.run`) |
| Target height | **147.0 m** — 147.0 m roof (Wikipedia 482 ft, published; LiDAR 142.5 = main roof, OSM 148) |
| Footprint | OSM way 80296761: OBB 44.8 x 47.1 m, 1997 m², bearing 45.2° |
| Triangle cap | 5,000 (FiDi batch, tower ≥ 60 m); built 4,754 |
| Category | `3` (office, `CAT.office` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Roof height | 147 m (482 ft) | published (Wikipedia) |
| Floors / year / architect | 33 / 2008 / KPF with Heller Manus | published |
| LiDAR | 142.53 m (main roof; the screen crown sits above) | measured (DataSF 2010 — the tower was under construction; treat with care) |
| Footprint | OBB 44.8 x 47.1 m, 1,997 m², 14 nodes with notches | measured (OSM way 80296761) |

### Sources

- https://en.wikipedia.org/wiki/555_Mission_Street
- https://commons.wikimedia.org/wiki/File:555_Mission_Street_from_Salesforce_Park_02.jpg
- https://www.openstreetmap.org/way/80296761
- https://data.sf.gov/resource/ynuv-fyni (2010 LiDAR building heights)

### Orientation

SoMa grid (bearing 45.2): Mission Street = NW face. Plan used directly from OSM. +Y = true north.

### What each side shows

- NW (Mission) and SE (toward Salesforce Park): blue glass, fine mullions (photo).
- Notched corners: dark reveals (photo).
- Crown: glass screen above the roof (photo; the real top has a sloped cut that is flattened).

### Recognition cues (ranked)

1. Pale blue glass prism.
2. Notched, recessed corners.
3. Glass screen crown.

### Massing recipe

- Glass lobby 0–10 m with white mullions, lit band.
- Shaft 10.9–142.5 m: glassl prism, silvery fins every 3.1 m, thin per-storey spandrels.
- Glass screen ring to 146.4 m, white cap to 147 m, plant inside, crown light.

### Palette

Toy_glassl, Toy_glassg (off-palette), Toy_white, Toy_roofd, Toy_steel, Toy_stone, Toy_leaf/leafd, Toy_rust; glow Toy_sand_Glow, Toy_white_Glow.

### Roof

Plant cluster inside the glass screen.

### Triangle budget

4,754 tris (cap 5,000). Facades are flat outward quads over solid prisms (window columns, per-storey spandrels, ribbons); night lights are hashed quads aligned with the window bays.

### Draft manifest entry

```json
{
  "id": "555-mission-street",
  "file": "555-mission-street.glb",
  "anchor": [-122.3985546, 37.7885452],
  "targetHeightM": 147.0,
  "cat": 3,
  "name": "555 Mission Street",
  "estimated": false,
  "dims": [73.022, 70.061, 147.0],
  "tris": 4754,
  "loadRadius": 4410
}
```

### Integration notes

Case B: registry entry, exclusion of OSM way 80296761 (and its building:parts) from the procedural bake, re-bake. `dims` is the world-axis bbox including the apron. loadRadius = max(2500, 30 x 147.0) = 4410.

### Open risks

- The sloped top edge of the screen is flattened.
- LiDAR from 2010 may predate full completion of the crown (the building opened Sept 2008, so likely fine).
