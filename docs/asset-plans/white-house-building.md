# The White House (Raphael Weill & Co.) — SF-SIM asset plan

San Francisco's first department store (1854–1965); its post-1906 home at Sutter × Grant (255 Sutter / 256 Grant) by Albert Pissis, clad in white terra cotta: a five-storey palazzo with a sweeping rounded corner, tall glazed shop base, heavy cornice, attic storey and roof balustrade. The upper floors became a parking garage after 1965; Banana Republic has the street floor.

**Deliverable:** `artifacts/white-house-building/` (Financial District batch, stages 1–2, BATCH mode).

| | |
|---|---|
| Manifest id | `white-house-building` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.4047770, 37.7894367` (OSM OBB centre via `tk.run`) |
| Target height | **32.1 m** — measured: DataSF LiDAR median roof 32.15 m (majority 31.6 m); OSM height 32 |
| Footprint | OSM way 333827281: OBB 84.4 × 42.6 m, 3,560 m², long-axis bearing 81.1° |
| Triangle cap | 3,000 (building < 60 m; built: 1,712) |
| Category | `4` (Retail — `CAT.retail` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Architect / material | Albert Pissis, white terra cotta | published (Wikipedia, NYT 1967) |
| Year / storeys | 1908 / 5 (assessor parcel 0293009, 241,918 sq ft) | published (DataSF assessor) |
| Roof | 32.15 m median, peak 44.6 m (a neighbour) | measured (DataSF 201006.0000542) |
| Footprint | OBB 84.4 × 42.6 m, 3,560 m², rounded NW corner | measured (OSM way 333827281) |
| Upper floors a garage; Banana Republic at street level |  | published (Wikipedia) |

### Sources

- OSM way 333827281 — https://www.openstreetmap.org/way/333827281
- Wikipedia, The White House (department store) — https://en.wikipedia.org/wiki/The_White_House_(department_store)
- Wikidata Q108044442 — https://www.wikidata.org/wiki/Q108044442
- DataSF assessor roll — https://data.sf.gov/resource/wv5m-vpq2.json
- DataSF 2010 LiDAR footprints — https://data.sf.gov/resource/ynuv-fyni
- Commons photo — https://commons.wikimedia.org/wiki/File:Chinatown,_San_Francisco,_CA,_USA_-_panoramio_(17).jpg

### Orientation

Street grid, u = bearing 81°, v = 351°. Sutter St = N face, Grant Ave = W face, the rounded corner = NW.

### What each side shows

- N, W and the curved corner: shopfronts, three storeys of windows, cornice, attic, balustrade — photographed (corner view).
- S and E: party walls, modelled blank — inferred.

### Recognition cues (ranked)

1. White curved corner at Sutter × Grant.
2. Heavy cornice with attic storey and balustrade.
3. Tall dark shop windows at street level.

### Massing recipe

- Plan: 84.2 × 42.4 m rectangle with a 10 m radius NW corner (6 segments).
- Base 0–9.5 m `Toy_white`, shop panes on the street faces; cream band.
- Body 10.3–24.5 m: three punched storeys on the street faces; cornice 24.5–26.3 m (1.2 m projection).
- Attic 26.3–30.6 m, balustrade to 32.1 m, dark garage deck with bay stripes, stair house and lamp strips.

### Palette, roof, budget

- Palette: `Toy_white`, `Toy_cream`, `Toy_glassd`, `Toy_roofd`, `Toy_steel`, `Toy_stone`; glow `Toy_sand_Glow`. All core palette.
- Roof: Garage deck behind the balustrade: white bay stripes, a cream stair house, lamp strips lit at night (inferred).
- Budget: 1,712 triangles against the 3,000 cap (validated with `--budget 3000`).

### Draft manifest entry

```json
{"id": "white-house-building", "file": "white-house-building.glb", "anchor": [-122.404777, 37.7894367], "targetHeightM": 32.1, "cat": 4, "name": "The White House (Raphael Weill & Co.)", "estimated": false, "dims": [94.6486, 61.8832, 32.1], "tris": 1712, "loadRadius": 2500}
```

### Integration notes

Case B: registry entry in `pipeline/lib/landmarks.mjs`, exclusion of OSM way 333827281 from the procedural bake, batch re-bake.

### Open risks

- Columns and window pairing simplified to punched windows.
- Rear elevations and the roof contents inferred.
- Category retail chosen for the ground-floor store; most floor area is now a garage.
