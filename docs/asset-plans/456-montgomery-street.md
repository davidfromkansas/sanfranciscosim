# 456 Montgomery Street — SF-SIM asset plan

A 26-storey white office tower (1986) ribbed with close-set vertical piers, cantilevered over a dark recessed floor on top of a preserved two-storey granite Beaux-Arts bank at the Montgomery × Sacramento corner.

**Deliverable:** `artifacts/456-montgomery-street/` (Financial District batch, stages 1–2, BATCH mode).

| | |
|---|---|
| Manifest id | `456-montgomery-street` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.4026340, 37.7935913` (OSM OBB centre via `tk.run`) |
| Target height | **115.2 m** — published roof 115.2 m (CTBUH via the Wikipedia tallest-buildings list); LiDAR median 114.5 m, peak 118.7 m |
| Footprint | OSM way 151183779: OBB 41.9 × 29 m, 1,064 m², long-axis bearing 171.2° |
| Triangle cap | 5,000 (tower ≥ 60 m; built: 3,296) |
| Category | `3` (Office — `CAT.office` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Roof height | 115.2 m | published (CTBUH, Wikipedia list) |
| LiDAR | median 114.5 m, peak 118.7 m | measured (DataSF 201006.0002986) |
| Floors / year | 26 / 1986 | published (Wikipedia list; assessor 26 storeys, 1986) |
| Granite bank base with columns and balustrade, tower cantilevered over it |  | photographed |
| Bank identity (the old bank at Montgomery × Sacramento) |  | inferred, not sourced |
| Bank 15 m + balustrade; dark transfer floor 17–21 m |  | estimated from the photo |

### Sources

- OSM way 151183779 — https://www.openstreetmap.org/way/151183779
- Wikipedia, List of tallest buildings in San Francisco (row 69) — https://en.wikipedia.org/wiki/List_of_tallest_buildings_in_San_Francisco
- CTBUH — https://www.skyscrapercenter.com/building/456-montgomery-street/17630
- DataSF assessor roll (parcels 0239012-14) — https://data.sf.gov/resource/wv5m-vpq2.json
- DataSF 2010 LiDAR footprints — https://data.sf.gov/resource/ynuv-fyni
- Commons photo — https://commons.wikimedia.org/wiki/File:456_Montgomery_Street.jpg

### Orientation

Street grid, local u = bearing 81° (east), v = 351° (north). Montgomery St = W face, Sacramento St = N face (assumed from the address range; the colonnaded corner is NW). The OSM outline has a small notch at the SE.

### What each side shows

- W (Montgomery) and N: granite bank with tall windows, columns in antis on N; white pier-grid tower above — photographed (one corner view).
- S and E: party walls of the bank; the tower skin repeats — inferred.

### Recognition cues (ranked)

1. White tower with dense vertical pinstripe piers.
2. Tower floating over a dark recessed floor.
3. Grey granite bank with columns and balustrade at its foot.
4. Plain parapet crown with dark slots.

### Massing recipe

- Bank: OSM outline (7 nodes) `Toy_stone` 0–15 m, two rows of tall `Toy_glassd` windows on the street faces, cornice and balustrade to 17.2 m, four columns on the N face.
- Gap: `Toy_glassd` floor inset 2.5 m, 17.2–21 m, with a lit band; white soffit slab 21–22.6 m.
- Shaft: 29.4 × 38.4 m rectangle, `tk.shaft` 25 storeys of 3.56 m, `Toy_glassd` with `Toy_white` piers every 1.9 m.
- Crown: white storey 111.5–115.2 m with dark slots, parapet hiding the plant, crown light line.

### Palette, roof, budget

- Palette: `Toy_white`, `Toy_stone`, `Toy_glassd`, `Toy_roofd`, `Toy_steel`; glow `Toy_sand_Glow`, `Toy_white_Glow`. All core palette.
- Roof: Dark deck inside a white parapet, tidy plant cluster; crown light line at night.
- Budget: 3,296 triangles against the 5,000 cap (validated with `--budget 5000`).

### Draft manifest entry

```json
{"id": "456-montgomery-street", "file": "456-montgomery-street.glb", "anchor": [-122.402634, 37.7935913], "targetHeightM": 115.2, "cat": 3, "name": "456 Montgomery Street", "estimated": false, "dims": [41.8414, 49.3577, 115.2], "tris": 3296, "loadRadius": 3456}
```

### Integration notes

Case B: registry entry in `pipeline/lib/landmarks.mjs`, exclusion of OSM way 151183779 from the procedural bake, batch re-bake.

### Open risks

- Tower plan is read from the photo as the OSM rectangle; the true cantilever overhang may differ.
- Columns shown only on the N face; the bank's exact elevations are inferred from one photo.
- Street-name assignment of the N face (Sacramento vs Commercial) is inferred from the address.
