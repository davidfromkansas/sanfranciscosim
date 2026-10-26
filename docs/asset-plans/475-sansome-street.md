# 475 Sansome Street — SF-SIM asset plan

A broad 1969 late-modernist office slab of 20 storeys (~483,000 sq ft, assessor), long axis east-west, in the north Financial District; home of the Public Policy Institute of California. No photo could be fetched (Wikimedia rate-limited), so its skin is inferred.

**Deliverable:** `artifacts/475-sansome-street/` (Financial District batch, stages 1–2, BATCH mode).

| | |
|---|---|
| Manifest id | `475-sansome-street` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.4019375, 37.7945747` (OSM OBB centre via `tk.run`) |
| Target height | **89.7 m** — measured: DataSF LiDAR peak 89.7 m (penthouse); main roof = LiDAR median 82.3 m (OSM height 82) |
| Footprint | OSM way 32859284: OBB 61.6 × 33.5 m, 2,037 m², long-axis bearing 81.2° |
| Triangle cap | 5,000 (tower ≥ 60 m; built: 3,662) |
| Category | `3` (Office — `CAT.office` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Year / storeys | 1969 / 20 (assessor parcel 0228039); OSM 19 levels | published (DataSF assessor) |
| Roof | median 82.3 m, peak 89.7 m | measured (DataSF 201006.0001172) |
| Footprint | OBB 61.6 × 33.5 m, 2,037 m², long axis bearing 81° | measured (OSM way 32859284) |
| Pale piers over bronze glass, colonnaded lobby, penthouse 30 × 14 m |  | inferred (no photo) |

### Sources

- OSM way 32859284 — https://www.openstreetmap.org/way/32859284
- DataSF assessor roll — https://data.sf.gov/resource/wv5m-vpq2.json
- DataSF 2010 LiDAR footprints — https://data.sf.gov/resource/ynuv-fyni
- PPIC (tenant address) — https://en.wikipedia.org/wiki/Public_Policy_Institute_of_California

### Orientation

Street grid, u = bearing 81°, v = 351°. Sansome St = E end; long faces N and S. A small jog in the N face (OSM).

### What each side shows

- All faces: inferred (no photograph). The same skin on all four.

### Recognition cues (ranked)

1. Long pale slab at the right height in the skyline.
2. Close vertical pier rhythm.
3. Set-back penthouse.

### Massing recipe

- Lobby 0–7 m: recessed `Toy_bronze` glass behind a 6 m concrete colonnade, lit ring.
- Shaft 7.5–82.3 m: `tk.shaft` 19 storeys of 3.94 m, `Toy_bronze` glass, `Toy_concrete` bands and piers at 3 m.
- Roof: cap, deck, 30 × 14 m louvred penthouse to 89.7 m, plant cluster.

### Palette, roof, budget

- Palette: `Toy_concrete`, `Toy_bronze` (off-palette), `Toy_roofd`, `Toy_steel`, `Toy_stone`; glow `Toy_sand_Glow`, `Toy_white_Glow`.
- Roof: Cap, dark deck, louvred penthouse and plant; crown line at night.
- Budget: 3,662 triangles against the 5,000 cap (validated with `--budget 5000`).

### Draft manifest entry

```json
{"id": "475-sansome-street", "file": "475-sansome-street.glb", "anchor": [-122.4019375, 37.7945747], "targetHeightM": 89.7, "cat": 3, "name": "475 Sansome Street", "estimated": false, "dims": [72.3412, 48.6114, 89.7], "tris": 3662, "loadRadius": 2691}
```

### Integration notes

Case B: registry entry in `pipeline/lib/landmarks.mjs`, exclusion of OSM way 32859284 from the procedural bake, batch re-bake.

### Open risks

- Facade materials and rhythm are inferred — the biggest risk; check against a street photo before approval.
- Penthouse footprint inferred; the LiDAR peak could be a smaller element.
