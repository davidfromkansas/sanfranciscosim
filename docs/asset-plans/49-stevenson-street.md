# 49 Stevenson Street — SF-SIM asset plan

A fifteen-storey late-1980s office building fronting Stevenson Street on the alley block between Market and Mission. Its OSM outline is a 41.6 × 25.7 m slab whose north (Market-side) corner is cut into a saw-tooth of small steps. No usable photograph found (Wikipedia has no article; Commons category/search pages for the building and its streets yielded none, the Commons API search was rate-limited), so the facade treatment is inferred from the period and the measured roof.

**Deliverable:** `artifacts/49-stevenson-street/` (Financial District batch, stages 1–2, BATCH mode).

| | |
|---|---|
| Manifest id | `49-stevenson-street` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.3993904, 37.7897060` (OSM OBB centre via `tk.run`) |
| Target height | **64.44 m** — DataSF 2010 LiDAR max 64.44 m of ring 201006.0003248 (screened plant crown, majority 63.9); main roof 60.0 m = ring median (measured) |
| Footprint | OSM way 149837256: OBB 41.6 × 25.7 m, 1040 m², long-axis bearing 44.9° |
| Triangle cap | 5,000 (tower ≥ 60 m; built: 2,356) |
| Category | `3` (Office — `CAT.office` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Crest | 64.44 m | measured (LiDAR max; majority 63.9) |
| Main roof | 60.0 m | measured (LiDAR median) |
| Year / storeys | 1989 / 15 | published (DataSF assessor roll) |
| Footprint | 41.6 × 25.7 m, 1,040 m², saw-tooth north corner | measured (OSM) |
| Granite base, ribbon windows, screened crown |  | inferred (no photo) |

### Sources

- OSM way 149837256 — https://www.openstreetmap.org/way/149837256
- DataSF building footprints + 2010 LiDAR heights — https://data.sf.gov/resource/ynuv-fyni
- DataSF assessor historical secured rolls (year built, storeys) — https://data.sf.gov/resource/wv5m-vpq2

### Orientation

Plan on the 44.9° grid: local +x = NE along Stevenson, +y = NW toward Market. Stevenson St front = SE face (local −y).

### What each side shows

- All four faces: **inferred** (no photograph) — granite base, banded ribbon-window shaft, the stepped north corner running full height.

### Recognition cues (ranked)

1. Mid-height (64 m) granite-and-glass slab with a saw-tooth corner.
2. Screened plant crown above a 60 m roof.
3. Horizontal granite spandrel bands.

### Massing recipe

- OSM outline (14 nodes, saw-tooth kept) on yaw from 44.9°.
- 0–8.6 m `Toy_granite` base with tall panes and a lit lobby; stone cap.
- 9.3–60 m `tk.shaft`: 13 storeys of 3.9 m, `Toy_glassd` with granite bands, 30% lit.
- Parapet, dark deck, set-back granite screen around a steel plant core to 64.44 m; white crown line.

### Palette, roof, budget

- Palette: `Toy_granite`, `Toy_stone`, `Toy_glassd`, `Toy_steel`, `Toy_roofd`, `Toy_concrete`; glow `Toy_sand_Glow`, `Toy_white_Glow`.
- Roof: Dark deck with a granite-screened plant crown (crest).
- Budget: 2,356 triangles against the 5,000 cap (validated with `--budget 5000`).

### Draft manifest entry

```json
{"id": "49-stevenson-street", "file": "49-stevenson-street.glb", "anchor": [-122.3993904, 37.789706], "targetHeightM": 64.44, "cat": 3, "name": "49 Stevenson Street", "estimated": false, "dims": [53.7203, 53.7598, 64.44], "tris": 2356, "loadRadius": 2500}
```

### Integration notes

Case B: registry entry in `pipeline/lib/landmarks.mjs`, exclusion of OSM way 149837256 from the
procedural bake, batch re-bake. 

### Open risks

- **Facade fully inferred** — no photograph; colours and window pattern may be wrong.
- Crown footprint/position inferred from the LiDAR median/majority split.
- Notability: an anonymous 1989 office tower; kept because it is a 15-storey FiDi presence, but the lead may prefer to drop it.
