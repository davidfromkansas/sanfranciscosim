# Galleria Park Hotel — SF-SIM asset plan

An eight-storey 1911 hotel: a two-storey base re-clad in grey granite with a red-awninged restaurant and a flat metal hotel canopy, six storeys of tan brick with deep-set windows and a few iron balconies, a deep dark bracketed cornice and a tall vertical 'GALLERIA PARK HOTEL' blade sign.

**Deliverable:** `artifacts/191-sutter-street/` (Financial District batch, stages 1–2, BATCH mode).

| | |
|---|---|
| Manifest id | `191-sutter-street` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.4035145, 37.7896065` (OSM OBB centre via `tk.run`) |
| Target height | **32.1 m** — LiDAR median roof 32.1 m (DataSF 2010, parcel 0292009); OSM 32 m; the list's 35.2 m was a LiDAR peak |
| Footprint | OSM way 132125160: OBB 37.4 × 30.7 m, 1138 m², long-axis bearing 171° |
| Triangle cap | 3,000 (building < 60 m; built: 1,214) |
| Category | `7` (Hotel — `CAT.hotel` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Opened | December 1911 (as Hotel Sutter) | published (OSM start_date / old_name) |
| Storeys | 8 visible (assessor: 9, built 1911, hotel) | photo / assessor |
| Roof | 32.1 m median, 32.0 m mode, 38.4 m max | measured (DataSF LiDAR) |
| Footprint | OBB 37.4 × 30.7 m, 1,138 m² (lot 11,944 sq ft) | measured (OSM, assessor) |
| Sutter frontage = north face | OSM centreline 10 m off the north edge | measured (OSM) |

### Sources

- OSM way 132125160 — https://www.openstreetmap.org/way/132125160
- Wikidata — https://www.wikidata.org/wiki/Q111393381
- DataSF building footprints + 2010 LiDAR heights — https://data.sf.gov/resource/ynuv-fyni
- DataSF assessor secured roll 2023 — https://data.sf.gov/resource/wv5m-vpq2
- OSM street centrelines via Nominatim (frontage check) — https://nominatim.openstreetmap.org/
- Commons photo — https://commons.wikimedia.org/wiki/File:Galleria_Park_Hotel_San_Francisco.jpg (looking west along Sutter)

### Orientation

Street grid yaw: local +x = bearing 81°, +y = 351°. North face = Sutter St; east and west are party walls (Crocker Galleria to the east); south is the rear.

### What each side shows

- N (Sutter): granite base, awning, canopy, brick shaft, balconies, cornice, blade sign — photographed (oblique).
- S (rear): punched brick wall (**inferred**).
- E and W: blank party walls (**inferred**).

### Recognition cues (ranked)

1. Tan brick hotel block with a deep dark bracketed cornice.
2. Vertical 'GALLERIA PARK HOTEL' blade sign (lit at night).
3. Grey granite two-storey base with red awning and flat canopy.

### Massing recipe

- Rectangle 30.7 × 37.2 m at yaw 9°.
- Base 0–8.6 m `Toy_stone`, with a `Toy_steel` granite skin on the Sutter face (lit shop panes, mezzanine panes), granite band.
- `Toy_red` awning and `Toy_steel` canopy boxes.
- Shaft 8.8–29.6 m `Toy_stone` punched block (six 3.43 m storeys, windows on street and rear faces only), five `Toy_ink` balconies.
- Frieze, `Toy_roofd` cornice 1.5 m out, deck, parapet, low plant to 32.1 m.
- Blade sign: navy fin 9.5–18.5 m with white glow faces both sides.

### Palette, roof, budget

- Palette: `Toy_stone`, `Toy_steel`, `Toy_red`, `Toy_navy`, `Toy_ink`, `Toy_glassd`, `Toy_roofd`; glow `Toy_sand_Glow`, `Toy_white_Glow`.
- Roof: Dark deck inside a stone parapet with a low plant cluster; warm crown line under the cornice at night.
- Budget: 1,214 triangles against the 3,000 cap (validated with `--budget 3000`).

### Draft manifest entry

```json
{"id": "191-sutter-street", "file": "191-sutter-street.glb", "anchor": [-122.4035145, 37.7896065], "targetHeightM": 32.1, "cat": 7, "name": "Galleria Park Hotel", "estimated": false, "dims": [41.8307, 47.2339, 32.1], "tris": 1214, "loadRadius": 2500}
```

### Integration notes

Case B: registry entry in `pipeline/lib/landmarks.mjs`, exclusion of OSM way 132125160 from the
procedural bake, batch re-bake. 

### Open risks

- Only one oblique photo; window rhythm and rear wall are estimated.
- Real brick is warmer/darker than `Toy_stone`.
- Blade sign position (west end) read from the photo.
