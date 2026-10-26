# Folger Coffee Company Building — SF-SIM asset plan

J. A. Folger & Company's five-storey Renaissance Revival headquarters, which survived both 1906 and 1989 on wooden piles driven into bay fill. Red-brown brick throughout: round-arched ground storey, a band course, three storeys of tall windows between brick piers, a top-floor arcade of round-headed windows and a deep corbelled cornice.

**Deliverable:** `artifacts/folger-coffee-building/` (Financial District batch, stages 1–2, BATCH mode).

| | |
|---|---|
| Manifest id | `folger-coffee-building` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.3925976, 37.7909315` (OSM OBB centre via `tk.run`) |
| Target height | **26.74 m** — facts-file LiDAR peak 26.74 m (roof bulkhead); main roof 24.6 m = DataSF ring 201006.0001608 majority (measured) |
| Footprint | OSM way 192305909: OBB 42.9 × 28.4 m, 1214 m², long-axis bearing 45.4° |
| Triangle cap | 3,000 (building < 60 m; built: 2,152) |
| Category | `3` (Office — `CAT.office` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Crest | 26.74 m | measured (facts-file LiDAR peak) |
| Main roof | 24.6 m | measured (LiDAR majority; median 24.5) |
| Storeys / year / architect | 5 + basement / 1904 / Henry A. Schulze | published (Wikipedia, NRHP) |
| Footprint | 42.9 × 28.4 m, 1,214 m² | measured (OSM) |
| Bay rhythm 4.3 m, two arched windows per bay at the top |  | inferred (photo) |

### Sources

- OSM way 192305909 — https://www.openstreetmap.org/way/192305909
- Wikipedia — https://en.wikipedia.org/wiki/Folger_Coffee_Company_Building
- DataSF building footprints + 2010 LiDAR heights — https://data.sf.gov/resource/ynuv-fyni
- DataSF assessor historical secured rolls (year built, storeys) — https://data.sf.gov/resource/wv5m-vpq2
- Commons photo (infobox) — https://commons.wikimedia.org/wiki/File:Folger_Coffee_Company_Building,_San_Francisco_2023-07-18.jpg (Howard × Spear corner)

### Orientation

Plan on the 45.4° grid: local +x = NE along Howard St, +y = NW. Howard (long side) and Spear are the photographed street faces.

### What each side shows

- Howard and Spear: arched ground floor, piered middle, arched top arcade, corbelled cornice — photographed.
- The two back faces: assumed to repeat the treatment (**inferred**; the photo shows a lower brick wing beside it, outside the OSM outline).

### Recognition cues (ranked)

1. Red-brown brick block with a deep corbelled cornice.
2. Row of round-headed top-floor windows.
3. Round-arched ground storey; brick piers between tall windows.

### Massing recipe

- `tk.rect(42.9, 28.4)` on yaw from 45.4°, `Toy_brick` to 23.4 m.
- Ground arches (4.3 m bays) with lit shopfronts; stone band course.
- `Toy_rust` brick piers 6.3–19.6 m; three storeys of panes; sill band.
- Top arcade of round-headed panes (2.15 m), sparse lit; corbel cornice + parapet; deck, bulkhead to 26.74 m, low plant.
- Five clipped street trees on Howard.

### Palette, roof, budget

- Palette: `Toy_brick`, `Toy_rust`, `Toy_stone`, `Toy_glassd`, `Toy_roofd`, `Toy_steel`, `Toy_concrete`, `Toy_leaf`; glow `Toy_sand_Glow`.
- Roof: Parapeted dark deck with a brick stair bulkhead (crest) and a low plant cluster.
- Budget: 2,152 triangles against the 3,000 cap (validated with `--budget 3000`).

### Draft manifest entry

```json
{"id": "folger-coffee-building", "file": "folger-coffee-building.glb", "anchor": [-122.3925976, 37.7909315], "targetHeightM": 26.74, "cat": 3, "name": "Folger Coffee Company Building", "estimated": false, "dims": [57.558, 57.4148, 26.74], "tris": 2152, "loadRadius": 2500}
```

### Integration notes

Case B: registry entry in `pipeline/lib/landmarks.mjs`, exclusion of OSM way 192305909 from the
procedural bake, batch re-bake. 

### Open risks

- Lower brick wing seen in the photo is not in the OSM outline and is not modelled.
- Back faces not photographed; bulkhead position inferred.
