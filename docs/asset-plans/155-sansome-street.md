# Stock Exchange Tower — SF-SIM asset plan

The office tower of the San Francisco Stock Exchange, built with the trading hall at 301 Pine (its own artifact, against this tower's north side). A narrow twelve-storey Moderne slab of pale grey stone running west from Sansome Street, entered under Stackpole's carved relief and a gilt "155 SANSOME" panel.

**Deliverable:** `artifacts/155-sansome-street/` (Financial District batch, stages 1–2, BATCH mode).

| | |
|---|---|
| Manifest id | `155-sansome-street` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.4012628, 37.7916701` (OSM OBB centre via `tk.run`) |
| Target height | **64.05 m** — facts-file LiDAR peak 64.05 m (stepped crown); main roof 54.6 m = DataSF ring 201006.0005660 median (measured; OSM height 55). Ring max 73.5 m not modelled |
| Footprint | OSM way 256066241: OBB 48 × 10.3 m, 493 m², long-axis bearing 81.3° |
| Triangle cap | 5,000 (tower ≥ 60 m; built: 2,642) |
| Category | `3` (Office — `CAT.office` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Crest | 64.05 m | measured (facts-file LiDAR peak) |
| Main roof | 54.6 m | measured (LiDAR median/majority) |
| Year / storeys | 1929 / 12 | published (DataSF assessor roll); OSM levels 11 |
| Footprint | 48 × 10.3 m, 493 m², narrow end on Sansome | measured (OSM) |
| Entrance relief + gilt name panel |  | photographed (Commons) |
| Stepped crown toward Sansome |  | inferred from LiDAR peak; not photographed |

### Sources

- OSM way 256066241 — https://www.openstreetmap.org/way/256066241
- Wikipedia (Pacific Exchange, building history) — https://en.wikipedia.org/wiki/Pacific_Exchange
- DataSF building footprints + 2010 LiDAR heights — https://data.sf.gov/resource/ynuv-fyni
- DataSF assessor historical secured rolls (year built, storeys) — https://data.sf.gov/resource/wv5m-vpq2
- Commons photo — https://commons.wikimedia.org/wiki/File:155_Sansome_SF.JPG (entrance relief detail only)

### Orientation

Street grid: local +x = bearing 81.3° (Sansome St end, east), +y = north (301 Pine trading hall).

### What each side shows

- E (Sansome): entrance, relief, gilt panel — photographed (detail).
- S and W: stone shaft with piers and punched windows (**inferred**).
- N: against 301 Pine up to ~16 m, then the same shaft (**inferred**).

### Recognition cues (ranked)

1. Narrow pale stone slab with flat vertical piers.
2. Stackpole relief and gilt name over the Sansome door.
3. Stepped crown at the Sansome end.

### Massing recipe

- `tk.rect(48, 10.2)` on yaw 81.3°; `Toy_stone` base 0–7.6 m with panes; white portal, lit door, gold name panel, relief disc and figure.
- 8.2–54.6 m `tk.punched_block` (11 storeys of 4.22 m), white piers every 2.5 m.
- Parapet, deck; crown step 1 (22 × 8.4 m, to 59.9 m, lit windows), step 2 (9 × 6 m, to 64.05 m) with a white crown line; low plant.

### Palette, roof, budget

- Palette: `Toy_stone`, `Toy_white`, `Toy_gold`, `Toy_glassd`, `Toy_roofd`, `Toy_steel`, `Toy_concrete`; glow `Toy_sand_Glow`, `Toy_white_Glow`.
- Roof: Dark deck with a low plant cluster behind the two-step crown.
- Budget: 2,642 triangles against the 5,000 cap (validated with `--budget 5000`).

### Draft manifest entry

```json
{"id": "155-sansome-street", "file": "155-sansome-street.glb", "anchor": [-122.4012628, 37.7916701], "targetHeightM": 64.05, "cat": 3, "name": "Stock Exchange Tower", "estimated": false, "dims": [53.5496, 21.9022, 64.05], "tris": 2642, "loadRadius": 2500}
```

### Integration notes

Case B: registry entry in `pipeline/lib/landmarks.mjs`, exclusion of OSM way 256066241 from the
procedural bake, batch re-bake. 

### Open risks

- Only the entrance relief is photographed; the shaft and crown forms are inferred.
- Crown height rests on a LiDAR percentile from the facts file; the 73.5 m ring max is unexplained.
- OSM puts the tower as a 10 m-wide strip; if the Sansome frontage is wider in reality the slab is too thin.
