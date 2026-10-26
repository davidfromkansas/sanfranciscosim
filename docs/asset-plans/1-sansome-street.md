# One Sansome Street — SF-SIM asset plan

A 41-storey pale grey granite tower with generously rounded corners and rows of green-tinted windows, raised on tall piers behind the 1910 Anglo and London Paris National Bank — a granite temple with 38 ft columns and a balustrade at the Sutter × Sansome corner, kept as the tower's conservatory.

**Deliverable:** `artifacts/1-sansome-street/` (Financial District batch, stages 1–2, BATCH mode).

| | |
|---|---|
| Manifest id | `1-sansome-street` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.4011756, 37.7904654` (OSM OBB centre via `tk.run`) |
| Target height | **168.0 m** — published roof 168 m (Wikipedia); LiDAR 174.18 m |
| Footprint | OSM way 32963344: OBB 42.1 × 73 m, 2613 m², long-axis bearing 171.5° |
| Triangle cap | 5,000 (tower ≥ 60 m; built: 4,202) |
| Category | `3` (Office — `CAT.office` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Roof height | 168 m | published (Wikipedia) |
| LiDAR | 174.18 m | measured |
| Floors / year / architect | 41–42 / 1984 / Pereira | published |
| Bank: 1910, Pissis, 38 ft Doric columns, now a conservatory |  | published |
| Site footprint | OBB 42.1 × 73 m, 2,613 m², 11 nodes | measured (OSM) |
| Tower 37.5 × 33.4 m on the west part, bank on the east part, pier base 21 m |  | inferred (photo + OSM outline) |

### Sources

- OSM way 32963344 — https://www.openstreetmap.org/way/32963344
- Wikipedia — https://en.wikipedia.org/wiki/One_Sansome_Street
- DataSF building footprints + 2010 LiDAR heights — https://data.sf.gov/resource/ynuv-fyni
- Commons photo (infobox) — https://commons.wikimedia.org/wiki/File:One_Sansome_Street.jpg (from Sutter × Sansome)

### Orientation

Local +x = bearing 81.5° (along Sutter), +y = 351.5°. East face = Sansome St, south = Sutter St; the bank holds the east part of the lot, the tower the west, a low wing the far west.

### What each side shows

- SE corner: the bank's columns and balustrade, the tower rising behind — photographed.
- Tower S and E faces: rounded corners, window rows, crown slots on the long face — photographed.
- N and W: same skin (**inferred**); crown slots repeated on all four faces (inferred; photographed on one).

### Recognition cues (ranked)

1. Pale tower with big rounded corners and green window rows.
2. Classical bank temple at its foot.
3. Deep slots in the top storeys.
4. Tower lifted on piers.

### Massing recipe

- Tower: 37.5 × 33.4 m rounded rectangle (r 6.5 m), recessed glass base on stone piers 0–21 m; `Toy_stone` body to 168 m; 37 rows of `Toy_copper` windows on the flat faces.
- Crown: three dark slots (`Toy_ink`) on each face, 8.5–2.5 m below the top, lit at night.
- Bank: OSM east block, white body with arched windows, stone columns, entablature, balustrade, glass roof with lit skylight.
- West wing: 21 m punched block.

### Palette, roof, budget

- Palette: `Toy_stone`, `Toy_white`, `Toy_copper` (off-palette green glass), `Toy_ink`, `Toy_glassd`, `Toy_glassl`, `Toy_roofd`, `Toy_steel`; glow `Toy_sand_Glow`, `Toy_white_Glow`.
- Roof: Dark deck inside a stone parapet with a low plant; the bank's glass roof glows from above at night.
- Budget: 4,202 triangles against the 5,000 cap (validated with `--budget 5000`).

### Draft manifest entry

```json
{"id": "1-sansome-street", "file": "1-sansome-street.glb", "anchor": [-122.4011756, 37.7904654], "targetHeightM": 168.0, "cat": 3, "name": "One Sansome Street", "estimated": false, "dims": [84.0755, 58.0822, 168.0], "tris": 4202, "loadRadius": 5040}
```

### Integration notes

Case B: registry entry in `pipeline/lib/landmarks.mjs`, exclusion of OSM way 32963344 from the
procedural bake, batch re-bake. 

### Open risks

- Split of the lot between tower and bank is inferred from the photo and outline.
- Pier-base height and the crown slots are read from one photo (slots shown on all four faces).
- West wing height unknown (21 m assumed).
