# Matson Building Annex — SF-SIM asset plan

A seven-storey strip built along the Matson Building's south-east wall, running from Main Street back to the PG&E annex. The miniature reuses the Matson landmark's cream terracotta language at a lower, plainer scale so the two read as one ensemble.

**Deliverable:** `artifacts/matson-building-annex/` (Financial District batch, stages 1–2, BATCH mode).

| | |
|---|---|
| Manifest id | `matson-building-annex` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.3962538, 37.7924632` (OSM OBB centre via `tk.run`) |
| Target height | **23.4 m** — facts-file LiDAR height 23.4 m (measured; the DataSF ring 201006.0000581 merges tower, annex and plaza, max 94.7 m, so its stats are unusable); consistent with 7 storeys (OSM building:levels) |
| Footprint | OSM way 260291407: OBB 42.2 × 14.9 m, 606 m², long-axis bearing 45.9° |
| Triangle cap | 3,000 (building < 60 m; built: 734) |
| Category | `3` (Office — `CAT.office` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Crest | 23.4 m | measured (facts-file LiDAR) |
| Storeys | 7 | OSM building:levels |
| Date | 1945–47, designed to match | published (Wikipedia Matson Building, via the Matson plan) |
| Footprint | 42.2 × 14.9 m, 606 m² | measured (OSM) |
| Gap to the Matson model | 0.75 m (past its 0.6 m base cornice) | estimated (modelling choice) |

### Sources

- OSM way 260291407 — https://www.openstreetmap.org/way/260291407
- Wikipedia — https://en.wikipedia.org/wiki/Matson_Building
- DataSF building footprints + 2010 LiDAR heights — https://data.sf.gov/resource/ynuv-fyni
- Commons photo — https://commons.wikimedia.org/wiki/File:Matson_Building_%26_Annex_(San_Francisco).jpg (Market front of the main building; the annex is not visible)
- Lead's existing landmark: artifacts/matson-building/ and docs/asset-plans/matson-building.md

### Orientation

Plan on the 45.9° grid: local +x = NE (Main St end), +y = NW (toward Matson). The NW face runs parallel to Matson's SE face 0.75 m clear; the SW end is a party wall against the PG&E annex.

### What each side shows

- SE and NE (Main St): terracotta arcaded base storey, cream punched shaft, terracotta cornice — **inferred** from "designed to match".
- NW: against the Matson Building (no windows).
- SW: party wall to the PG&E annex (no windows).

### Recognition cues (ranked)

1. Same cream terracotta as Matson, a 7-storey block tucked against its flank.
2. Arcaded terracotta base and punched-window rhythm (2.8 m) carried over from Matson.
3. Terracotta cornice on the street sides.

### Massing recipe

- Plan: OSM SE face, NE/SW ends; NW face computed from the Matson model's SE face + 0.75 m.
- 0–5.4 m `Toy_terracotta` base with arched panes (lit) on SE/NE; cream band.
- 6–21.6 m `tk.punched_block` (6 storeys of 2.6 m) `Toy_cream`, panes 2.8 m apart, SE/NE only.
- Frieze, street-side cornice, parapet to 23.4 m, dark deck, low plant.

### Palette, roof, budget

- Palette: `Toy_cream`, `Toy_terracotta`, `Toy_glassd`, `Toy_roofd`, `Toy_steel`, `Toy_concrete` — the Matson set.
- Roof: Dark deck with a low plant cluster inside a cream parapet.
- Budget: 734 triangles against the 3,000 cap (validated with `--budget 3000`).

### Draft manifest entry

```json
{"id": "matson-building-annex", "file": "matson-building-annex.glb", "anchor": [-122.3962538, 37.7924632], "targetHeightM": 23.4, "cat": 3, "name": "Matson Building Annex", "estimated": false, "dims": [43.9994, 42.9502, 23.4], "tris": 734, "loadRadius": 2500}
```

### Integration notes

Case B: registry entry in `pipeline/lib/landmarks.mjs`, exclusion of OSM way 260291407 from the
procedural bake, batch re-bake. 

### Open risks

- **No photograph of the annex**: every facade is inferred from "designed to match"; a 1945 annex may be plainer.
- Height rests on the facts-file LiDAR sample; DataSF has no separate ring.
- Matson's 3 m ground plinth (0.25 m) runs under the annex's NW edge at ground level.
