# Orchard Garden Hotel — SF-SIM asset plan

A ten-storey cream hotel on a deep, narrow lot just east of the Chinatown Gate. On Bush Street two full-height bays of blue-grey glass rise between cream piers over a dark bronze ground storey with an awning and flags, under a thin projecting top; the tall west party wall shows the hotel's name over its low Chinatown neighbour.

**Deliverable:** `artifacts/466-bush-street/` (Financial District batch, stages 1–2, BATCH mode).

| | |
|---|---|
| Manifest id | `466-bush-street` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.4052342, 37.7908797` (OSM OBB centre via `tk.run`) |
| Target height | **34.55 m** — DataSF 2010 LiDAR max 34.55 m (penthouse) of ring 201006.0022502; main roof 31.0 m = ring median (measured; OSM height 31) |
| Footprint | OSM way 260279404: OBB 14.8 × 42.6 m, 474 m², long-axis bearing 81.1° |
| Triangle cap | 3,000 (building < 60 m; built: 2,036) |
| Category | `7` (Hotel — `CAT.hotel` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Crest (penthouse) | 34.55 m | measured (LiDAR max) |
| Main roof | 31.0 m | measured (LiDAR median) |
| Year / storeys | 2007 / 10 | published (DataSF assessor roll) |
| Footprint | 42.6 × 14.8 m, 474 m², light wells both sides | measured (OSM) |

### Sources

- OSM way 260279404 — https://www.openstreetmap.org/way/260279404
- Wikidata Q111393383 — https://www.wikidata.org/wiki/Q111393383
- DataSF building footprints + 2010 LiDAR heights — https://data.sf.gov/resource/ynuv-fyni
- DataSF assessor historical secured rolls (year built, storeys) — https://data.sf.gov/resource/wv5m-vpq2
- Commons photo (Wikidata P18) — https://commons.wikimedia.org/wiki/File:Orchard_Garden_Hotel.jpg (down Bush St from Grant)

### Orientation

Street grid: local +x = bearing 81.1° (east along Bush), +y = north. Bush St front at local y = −21.3 (south).

### What each side shows

- S (Bush): bronze ground storey, two glass bays, projecting top — photographed.
- W: tall cream party wall with the hotel's name — photographed.
- E and N: plain cream with punched windows (**inferred**).

### Recognition cues (ranked)

1. Narrow cream ten-storey block with two vertical glass bays.
2. Hotel name high on the cream west wall.
3. Dark bronze shopfront storey.

### Massing recipe

- OSM outline (12 nodes) as a `tk.punched_block` to 31 m, 9 guest floors of 2.89 m over a lobby storey.
- Bush front: bronze shopfront box with lit lobby, awning; two `Toy_glassl` bays with steel floor bands and lit panes.
- Projecting trim top slab, parapet, dark deck, penthouse to 34.55 m with a crown light, small plant.
- Dark sign plaque on the west wall.

### Palette, roof, budget

- Palette: `Toy_cream`, `Toy_trim`, `Toy_glassl`, `Toy_glassd`, `Toy_steel`, `Toy_bronze`, `Toy_ink`, `Toy_roofd`, `Toy_concrete`; glow `Toy_sand_Glow`, `Toy_white_Glow`.
- Roof: Parapeted dark deck with a cream penthouse (crest) and a small plant cluster.
- Budget: 2,036 triangles against the 3,000 cap (validated with `--budget 3000`).

### Draft manifest entry

```json
{"id": "466-bush-street", "file": "466-bush-street.glb", "anchor": [-122.4052342, 37.7908797], "targetHeightM": 34.55, "cat": 7, "name": "Orchard Garden Hotel", "estimated": false, "dims": [20.5618, 47.4349, 34.55], "tris": 2036, "loadRadius": 2500}
```

### Integration notes

Case B: registry entry in `pipeline/lib/landmarks.mjs`, exclusion of OSM way 260279404 from the
procedural bake, batch re-bake. 

### Open risks

- Penthouse size/position inferred (LiDAR max only).
- Rear elevations not photographed.
