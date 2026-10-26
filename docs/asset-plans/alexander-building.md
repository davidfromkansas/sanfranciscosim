# Alexander Building — SF-SIM asset plan

A slender fifteen-storey office tower on a small corner lot at Montgomery and Bush. No usable photograph found (Wikipedia has no article; Commons category/search pages for the building and its streets yielded none, the Commons API search was rate-limited); the miniature follows the period's San Francisco high-rise type with a vertical accent: stone base, continuous cream piers over recessed spandrels, an arcaded top storey and a pinnacle parapet.

**Deliverable:** `artifacts/alexander-building/` (Financial District batch, stages 1–2, BATCH mode).

| | |
|---|---|
| Manifest id | `alexander-building` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.4025768, 37.7907411` (OSM OBB centre via `tk.run`) |
| Target height | **60.13 m** — DataSF 2010 LiDAR median 60.13 m of ring 201006.0009912 (measured; majority 59.6). The facts file's 76.6 m and the ring max 93 m look like a taller neighbour's wall and are not modelled |
| Footprint | OSM way 132125157: OBB 22.4 × 17.1 m, 381 m², long-axis bearing 171.1° |
| Triangle cap | 5,000 (tower ≥ 60 m; built: 2,426) |
| Category | `3` (Office — `CAT.office` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Roof | 60.13 m | measured (LiDAR median) |
| Year / storeys | 1921 / 15 | published (DataSF assessor roll) |
| Footprint | 22.4 × 17.1 m, 381 m² | measured (OSM) |
| Pier-and-spandrel terracotta facade, arcaded top |  | inferred (no photo) |

### Sources

- OSM way 132125157 — https://www.openstreetmap.org/way/132125157
- DataSF building footprints + 2010 LiDAR heights — https://data.sf.gov/resource/ynuv-fyni
- DataSF assessor historical secured rolls (year built, storeys) — https://data.sf.gov/resource/wv5m-vpq2

### Orientation

Street grid: local +x = bearing 81.1° (east), +y = north. Montgomery St = west face, Bush St = south face; N and E are party walls.

### What each side shows

- W (Montgomery) and S (Bush): stone base with shopfronts, piered shaft, arcaded top — **inferred**.
- N and E: same shaft above the neighbours (**inferred**; base windows omitted).

### Recognition cues (ranked)

1. Thin corner tower with strong vertical piers.
2. Arcaded top storey and pinnacle parapet.
3. Stone two-storey base.

### Massing recipe

- `tk.rect(17.1, 22.4)` on yaw 81.1°; `Toy_stone` base 0–8.4 m, street-side panes and lit shopfronts.
- 9–55.8 m `Toy_terracotta` shaft, 12 storeys of 3.9 m, panes every 2.15 m, `Toy_cream` piers 0.55 m proud.
- Top storey with arched panes; cream cornice and parapet; pinnacles to 60.13 m; stair bulkhead.

### Palette, roof, budget

- Palette: `Toy_terracotta`, `Toy_cream`, `Toy_stone`, `Toy_glassd`, `Toy_roofd`, `Toy_concrete`; glow `Toy_sand_Glow`.
- Roof: Dark deck inside a cream parapet with pinnacles and a stair bulkhead.
- Budget: 2,426 triangles against the 5,000 cap (validated with `--budget 5000`).

### Draft manifest entry

```json
{"id": "alexander-building", "file": "alexander-building.glb", "anchor": [-122.4025768, 37.7907411], "targetHeightM": 60.13, "cat": 3, "name": "Alexander Building", "estimated": false, "dims": [24.9303, 29.3465, 60.13], "tris": 2426, "loadRadius": 2500}
```

### Integration notes

Case B: registry entry in `pipeline/lib/landmarks.mjs`, exclusion of OSM way 132125157 from the
procedural bake, batch re-bake. 

### Open risks

- **Facade fully inferred** — no photograph; the Gothic accent is a guess.
- Rejected the facts-file 76.6 m; if a real crown tower exists above 60 m it is missing.
