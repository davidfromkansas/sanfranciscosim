# Adam Grant Building — SF-SIM asset plan

A fourteen-storey post-fire office block filling most of its lot around an interior light court. No usable photograph found (Wikipedia has no article; Commons category/search pages for the building and its streets yielded none, the Commons API search was rate-limited); the miniature is an Edwardian commercial palazzo — stone base, light brick shaft of punched windows, top storey under a projecting cornice — with the light court as a dark well in the roof.

**Deliverable:** `artifacts/100-sansome-street/` (Financial District batch, stages 1–2, BATCH mode).

| | |
|---|---|
| Manifest id | `100-sansome-street` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.4004726, 37.7915113` (OSM OBB centre via `tk.run`) |
| Target height | **58.2 m** — DataSF 2010 LiDAR median 58.2 m of ring 201006.0002228 (measured; majority 58.1). The facts file's 41.46 m was a neighbouring ring; OSM height 58 agrees |
| Footprint | OSM way 260282389: OBB 41.5 × 43.9 m, 1452 m², long-axis bearing 171.3° |
| Triangle cap | 3,000 (building < 60 m; built: 2,754) |
| Category | `3` (Office — `CAT.office` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Roof | 58.2 m | measured (LiDAR median/majority) |
| Year / storeys | 1908 / 14 | published (DataSF assessor roll, 114 Sansome) |
| Floor area | 224,651 sq ft ≈ 14 × 1,490 m² | published (assessor) — matches the footprint |
| Footprint | OBB 41.5 × 43.9 m, 1,452 m², light court 11 × 16 m | measured (OSM, court from the slit-joined hole) |
| Palazzo facade, light brick |  | inferred (no photo) |

### Sources

- OSM way 260282389 — https://www.openstreetmap.org/way/260282389
- DataSF building footprints + 2010 LiDAR heights — https://data.sf.gov/resource/ynuv-fyni
- DataSF assessor historical secured rolls (year built, storeys) — https://data.sf.gov/resource/wv5m-vpq2

### Orientation

Street grid: local +x = bearing 81.3° (east), +y = north. Sansome St = west face, Bush St = south face.

### What each side shows

- All faces **inferred** (no photograph): stone two-storey base, light brick punched shaft, top storey, cornice.
- Light court: dark roof well with a rim (from the OSM hole).

### Recognition cues (ranked)

1. Big fourteen-storey Edwardian block with a heavy cornice.
2. Stone base / light shaft / top storey split.
3. Dark light-court well seen from above.

### Massing recipe

- OSM outer outline (10 nodes, court hole and its slit removed) on yaw 81.3°.
- 0–8.6 m `Toy_stone` base, tall panes, lit; base band.
- 9.4–51.4 m `tk.punched_block` (11 storeys of 3.82 m) `Toy_sand`, panes 3.4 m apart; stone band.
- 52.1–55.6 m top storey; 1.6 m cornice; parapet to 58.2 m; deck, dark court well with rim, low plant, rust water tank.

### Palette, roof, budget

- Palette: `Toy_sand`, `Toy_stone`, `Toy_glassd`, `Toy_ink` (court well), `Toy_rust`, `Toy_roofd`, `Toy_steel`, `Toy_concrete`; glow `Toy_sand_Glow`.
- Roof: Dark deck with the dark light-court well, a low plant cluster and a water tank.
- Budget: 2,754 triangles against the 3,000 cap (validated with `--budget 3000`).

### Draft manifest entry

```json
{"id": "100-sansome-street", "file": "100-sansome-street.glb", "anchor": [-122.4004726, 37.7915113], "targetHeightM": 58.2, "cat": 3, "name": "Adam Grant Building", "estimated": false, "dims": [54.2544, 51.7427, 58.2], "tris": 2754, "loadRadius": 2500}
```

### Integration notes

Case B: registry entry in `pipeline/lib/landmarks.mjs`, exclusion of OSM way 260282389 from the
procedural bake, batch re-bake. 

### Open risks

- **Facade fully inferred** — no photograph; materials and base height may differ.
- The court is drawn on the roof rather than cut through the block.
- LiDAR max 69.1 m in the ring is not modelled (possible penthouse or neighbour edge).
