# 350 Bush Street (with the Curb Exchange) — SF-SIM asset plan

Heller Manus's 19-storey glass office tower (2018), a through-block site from Bush to Pine, built around the 1923 San Francisco Mining / Curb Exchange (Miller & Pflueger). The Exchange's temple front — eight fluted columns in pairs under a sculpted pediment — is kept as the Bush Street entrance. Twitch's former headquarters.

**Deliverable:** `artifacts/350-bush-street/` (Financial District batch, stages 1–2, BATCH mode).

| | |
|---|---|
| Manifest id | `350-bush-street` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.4033004, 37.7913475` (OSM OBB centre via `tk.run`) |
| Target height | **85.0 m — ESTIMATED** — ESTIMATED 85 m: 19 storeys (Wikidata, SocketSite, Bisnow) × ~4.26 m + glass crown screen. No published height; no LiDAR (built 2018, after the 2010 survey; the list's 86 m was a neighbour's LiDAR) |
| Footprint | OSM way 151185876: OBB 83.3 × 43.5 m, 3,070 m², long-axis bearing 170° |
| Triangle cap | 5,000 (tower ≥ 60 m; built: 4,542) |
| Category | `3` (Office — `CAT.office` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Floors / completed | 19 / 2018 | published (Wikidata Q137643241, SocketSite, Bisnow) |
| Height | 85 m | ESTIMATED (no published figure) |
| Exchange | 1923, Miller & Pflueger, OSM way 151185875 height 16 m | published (Wikidata Q137643186) / OSM |
| Pediment apex ~20 m |  | estimated from the photo |
| Tower footprint | OSM way 151185876, 23 nodes, 3,070 m² | measured (OSM) |
| Assessor | 441-465 Pine parcel 0269028: 2018, 19 storeys, 385,000 sq ft | published (DataSF) |

### Sources

- OSM way 151185876 (tower), 151185875 (Exchange) — https://www.openstreetmap.org/way/151185876
- Wikidata Q137643241 / Q137643186 — https://www.wikidata.org/wiki/Q137643241
- SocketSite 2014 — https://socketsite.com/archives/2014/04/19story_tower_to_rise_over_sfs_mining_exchange_building.html
- Bisnow, completion — https://www.bisnow.com/news/san-francisco/office/after-40-years-san-franciscos-350-bush-completed-90250
- DataSF assessor roll — https://data.sf.gov/resource/wv5m-vpq2.json
- Commons photos — https://commons.wikimedia.org/wiki/File:350_Bush_Street.jpg ; https://commons.wikimedia.org/wiki/File:California_State_Chamber_of_Commerce_02.JPG

### Orientation

Street grid, u = bearing 81°, v = 351°. Bush St = S face (v = −41), Pine St = N face. The Exchange takes the SW of the site; a stone-clad low wing sits east of it on Bush.

### What each side shows

- S (Bush): temple front, stone wing to its east, glass tower rising behind — photographed.
- N (Pine), E, W: glass tower skin — inferred (not photographed); the tower is modelled as one height over the whole site.

### Recognition cues (ranked)

1. White classical temple front with paired columns and pediment.
2. Dark green-glass tower rising right behind it.
3. Thin vertical mullion rhythm.
4. Glass crown screen.

### Massing recipe

- Tower: OSM outline minus the Exchange hall, `tk.shaft` 19 storeys of 4.26 m to 81 m in `Toy_glassd`, steel bands and fins at 4.2 m; glass screen 81–85 m.
- Stone wing: 20.8 m × 0.8 m stone face 0–14 m with punched windows on Bush.
- Exchange: stone hall 16 m; portico with stylobate, cella wall with three tall windows, antae, eight `Toy_white` columns in pairs, entablature 13.6–16 m, pediment to 20.2 m.

### Palette, roof, budget

- Palette: `Toy_glassd`, `Toy_glassl`, `Toy_steel`, `Toy_stone`, `Toy_white`, `Toy_roofd`; glow `Toy_sand_Glow`, `Toy_white_Glow`. All core palette.
- Roof: Glass screen around a dark deck with a plant cluster; Exchange hall roof dark at 16 m.
- Budget: 4,542 triangles against the 5,000 cap (validated with `--budget 5000`).

### Draft manifest entry

```json
{"id": "350-bush-street", "file": "350-bush-street.glb", "anchor": [-122.4033004, 37.7913475], "targetHeightM": 85.0, "cat": 3, "name": "350 Bush Street (with the Curb Exchange)", "estimated": true, "dims": [63.5937, 95.1582, 85.0], "tris": 4542, "loadRadius": 2550}
```

### Integration notes

Case B: registry entry in `pipeline/lib/landmarks.mjs`, exclusion of OSM way 151185876 and of the Curb Exchange way 151185875 from the procedural bake, batch re-bake.

### Open risks

- Height is an estimate (±8 m).
- Tower stepping/setbacks seen in the photo are simplified to one prism.
- The Exchange is a separate OSM way: integration must exclude both 151185876 and 151185875.
- Pine-side and side elevations not photographed.
