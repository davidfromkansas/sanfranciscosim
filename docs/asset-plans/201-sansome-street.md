# Royal Insurance Building — SF-SIM asset plan

An eleven-storey 1907 office block at Sansome and Pine: a three-storey white marble base with the Royal coat of arms (lion, unicorn, clock) over the Sansome entrance, a shaft of dark red-brown brick with white-trimmed windows, and a white terracotta top of two storeys with cartouches under a deep cornice. In the miniature it is the brick-and-white sandwich on the corner.

**Deliverable:** `artifacts/201-sansome-street/` (Financial District batch, stages 1–2, BATCH mode).

| | |
|---|---|
| Manifest id | `201-sansome-street` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.4012641, 37.7922609` (OSM OBB centre via `tk.run`) |
| Target height | **41.3 m** — LiDAR median roof 41.3 m (DataSF 2010, parcel 0260017); OSM 41 m agrees; the list's 44.7 m was a higher LiDAR percentile |
| Footprint | OSM way 256067738: OBB 27.7 × 20.5 m, 480 m², long-axis bearing 81.5° |
| Triangle cap | 3,000 (building < 60 m; built: 2,138) |
| Category | `2` (Apartments — `CAT.apartments` (office converted to condominiums) in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Completed / architect | 1907 / Howells & Stokes | published (Wikipedia, Wikidata Q26001132) |
| Storeys | 11 (condo unit numbers run to 11xx) | published (assessor roll) |
| Roof | 41.3 m median, 40.9 m mode, 48.0 m max | measured (DataSF LiDAR) |
| Footprint | OBB 27.7 × 20.5 m, 480 m², L with NW light-court notch | measured (OSM) |
| Storey split 3 marble / 6 brick / 2 white |  | inferred (photo) |

### Sources

- OSM way 256067738 — https://www.openstreetmap.org/way/256067738
- Wikipedia — https://en.wikipedia.org/wiki/Royal_Insurance_Building_(San_Francisco)
- Wikidata — https://www.wikidata.org/wiki/Q26001132
- DataSF building footprints + 2010 LiDAR heights — https://data.sf.gov/resource/ynuv-fyni
- DataSF assessor secured roll 2023 — https://data.sf.gov/resource/wv5m-vpq2
- Commons photo — https://commons.wikimedia.org/wiki/File:Royal_Insurance_Building,_SF_corner.JPG (the Sansome/Pine corner)

### Orientation

Street grid yaw: local +x = bearing 81.5°, +y = 351.5°. East face = Sansome St (20.5 m, entrance and coat of arms), south face = Pine St (27.7 m); north and west are party walls, the NW notch a light court.

### What each side shows

- E (Sansome): marble base with the arms over the entrance, brick shaft, white top — photographed.
- S (Pine): same, longer — photographed.
- N and W: same treatment carried round (**inferred**; mostly party walls in reality).

### Recognition cues (ranked)

1. Dark red brick shaft between a white marble base and a white terracotta top.
2. Deep white cornice with cartouches below it.
3. Coat of arms with clock over the Sansome entrance.

### Massing recipe

- Plan: 6-node OSM L (local), yaw 8.5°.
- Base 0–12.6 m `Toy_stone` with tall ground openings and two window rows, cornice band.
- Shaft 13.4–32.4 m `Toy_rust` punched block, 3.27 m storeys, white quoin piers at the three street corners.
- Top 33.1–39.6 m `Toy_cream` punched block, five `Toy_stone` cartouches, deep cornice, parapet to 41.3 m.
- Arms: cream relief block with a gold clock disc over the Sansome entrance.

### Palette, roof, budget

- Palette: `Toy_stone`, `Toy_cream`, `Toy_rust`, `Toy_glassd`, `Toy_gold`, `Toy_roofd`, `Toy_steel`; glow `Toy_sand_Glow`, `Toy_white_Glow`.
- Roof: Dark deck inside a cream parapet with a low flat plant box; a white crown line under the cornice at night.
- Budget: 2,138 triangles against the 3,000 cap (validated with `--budget 3000`).

### Draft manifest entry

```json
{"id": "201-sansome-street", "file": "201-sansome-street.glb", "anchor": [-122.4012641, 37.7922609], "targetHeightM": 41.3, "cat": 2, "name": "Royal Insurance Building", "estimated": false, "dims": [35.2254, 30.0658, 41.3], "tris": 2138, "loadRadius": 2500}
```

### Integration notes

Case B: registry entry in `pipeline/lib/landmarks.mjs`, exclusion of OSM way 256067738 from the
procedural bake, batch re-bake. 

### Open risks

- The LiDAR maximum (48 m) suggests a small rooftop structure not modelled.
- Brick tone is approximated by `Toy_rust` (the real brick is darker).
- Party-wall faces are given the street treatment.
