# One Montgomery Tower (120 Kearny Street) — SF-SIM asset plan

A 38-storey Art Deco Revival office tower at Post and Kearny: a rose-red granite prism with clipped corners, pierced by a dense grid of square windows, on a two-storey black granite base.

**Deliverable:** `artifacts/120-kearny-street/` (Financial District batch, stages 1–2, BATCH mode).

| | |
|---|---|
| Manifest id | `120-kearny-street` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.4033381, 37.7891873` (OSM OBB centre via `tk.run`) |
| Target height | **152.4 m** — published roof 152.4 m (500 ft, Wikipedia); LiDAR 155.95 m |
| Footprint | OSM way 148716020: OBB 54.9 × 38 m, 2049 m², long-axis bearing 80.1° |
| Triangle cap | 5,000 (tower ≥ 60 m; built: 4,720) |
| Category | `3` (Office — `CAT.office` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Roof height | 152.4 m (500 ft) | published (Wikipedia infobox) |
| LiDAR | 155.95 m | measured |
| Floors / year / architect | 38 / 1982 / SOM | published |
| Red granite, square windows in blocks of four; black granite first two floors |  | published |
| Footprint | OBB 54.9 × 38 m, 2,049 m², clipped corners | measured (OSM) |
| Solid granite cap ~6 m |  | inferred (photo) |

### Sources

- OSM way 148716020 — https://www.openstreetmap.org/way/148716020
- Wikipedia — https://en.wikipedia.org/wiki/One_Montgomery_Tower
- DataSF building footprints + 2010 LiDAR heights — https://data.sf.gov/resource/ynuv-fyni
- Commons photo (infobox) — https://commons.wikimedia.org/wiki/File:One_Montgomery_Tower_2021.jpg

### Orientation

Local +x = bearing 80.1° (along Post), +y = 350.1° (along Kearny). South face = Post St, west face = Kearny St.

### What each side shows

- S (Post) and W (Kearny): square-window grid, solid corner piers — photographed.
- N and E: same grid (**inferred**).

### Recognition cues (ranked)

1. Rose-red granite prism with a dense square-window grid.
2. Clipped corners, flat top.
3. Black base.

### Massing recipe

- 54.9 × 38 m rectangle with 2.8 m chamfers.
- Base 0–9 m: `Toy_ink` with lit shop glass.
- Shaft 9–152.4 m: `Toy_granite` prism; 36 storeys × one `Toy_glassd` square window per 3.75 m bay.
- Cap: granite band, parapet, small penthouse and plant.

### Palette, roof, budget

- Palette: `Toy_granite` (off-palette rose granite), `Toy_glassd`, `Toy_ink`, `Toy_roofd`, `Toy_steel`, `Toy_stone`, trees; glow `Toy_sand_Glow`, `Toy_white_Glow`.
- Roof: Dark deck inside a granite parapet, small granite penthouse and plant; crown line at night.
- Budget: 4,720 triangles against the 5,000 cap (validated with `--budget 5000`).

### Draft manifest entry

```json
{"id": "120-kearny-street", "file": "120-kearny-street.glb", "anchor": [-122.4033381, 37.7891873], "targetHeightM": 152.4, "cat": 3, "name": "One Montgomery Tower (120 Kearny Street)", "estimated": false, "dims": [65.9566, 53.2045, 152.4], "tris": 4720, "loadRadius": 4572}
```

### Integration notes

Case B: registry entry in `pipeline/lib/landmarks.mjs`, exclusion of OSM way 148716020 from the
procedural bake, batch re-bake. 

### Open risks

- Granite tone: photo reads pink-tan in sun, published 'red'; `Toy_granite` is a compromise.
- N and E faces not photographed.
