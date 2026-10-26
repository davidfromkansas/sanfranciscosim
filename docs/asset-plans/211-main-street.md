# 211 Main Street (Charles Schwab Building) — SF-SIM asset plan

The Charles Schwab Building (1973, Corwin Booth & Associates per PCAD; 17 storeys, ~417,000 sq ft), Schwab's San Francisco headquarters, on Main Street south of Howard. A near-square 1970s office block; no photo could be fetched, so the skin is inferred from the period and Booth's contemporary 180 Montgomery.

**Deliverable:** `artifacts/211-main-street/` (Financial District batch, stages 1–2, BATCH mode).

| | |
|---|---|
| Manifest id | `211-main-street` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.3928540, 37.7905944` (OSM OBB centre via `tk.run`) |
| Target height | **82.0 m** — measured: DataSF LiDAR peak 82.0 m (penthouse); main roof = LiDAR median 73.3 m. OSM height 85 is unsourced |
| Footprint | OSM way 154217696: OBB 50 × 41.9 m, 2,082 m², long-axis bearing 135° |
| Triangle cap | 5,000 (tower ≥ 60 m; built: 2,152) |
| Category | `3` (Office — `CAT.office` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Year / storeys | 1973 / 17 (assessor parcel 3740033); OSM 18 levels | published (DataSF assessor) |
| Architect | Corwin L. Booth & Associates | published (PCAD 24017; unconfirmed elsewhere) |
| Roof | median 73.3 m, peak 82.0 m | measured (DataSF 201006.0001029) |
| Footprint | OBB 50 × 41.9 m, 2,082 m², bearing 135° | measured (OSM way 154217696) |
| Bronze ribbon windows, sandy spandrels, penthouse 20 × 26 m |  | inferred (no photo) |

### Sources

- OSM way 154217696 — https://www.openstreetmap.org/way/154217696
- PCAD 24017 — https://pcad.lib.washington.edu/building/24017
- Commercial Observer 2024 — https://commercialobserver.com/2024/04/blackstone-schwab-building-special-servicing/
- DataSF assessor roll — https://data.sf.gov/resource/wv5m-vpq2.json
- DataSF 2010 LiDAR footprints — https://data.sf.gov/resource/ynuv-fyni

### Orientation

SoMa grid, u = bearing 45° (NE), v = 315° (NW). Main St runs along v; Howard St along u.

### What each side shows

- All faces: inferred (no photograph), same skin on all four.

### Recognition cues (ranked)

1. Squat square block at the right height.
2. Horizontal bronze ribbons between sandy spandrels.
3. Set-back penthouse.

### Massing recipe

- Lobby 0–6 m: recessed `Toy_bronze` behind sand piers at 8.3 m, lit ring.
- Shaft 6.5–73.3 m: `tk.shaft` 16 storeys of 4.18 m, 1.9 m `Toy_sand` spandrels, broad piers at 8.3 m.
- Roof: cap, deck, 20 × 26 m louvred penthouse to 82.0 m, plant.

### Palette, roof, budget

- Palette: `Toy_sand`, `Toy_bronze` (off-palette), `Toy_roofd`, `Toy_steel`, `Toy_stone`; glow `Toy_sand_Glow`, `Toy_white_Glow`.
- Roof: Cap, dark deck, louvred penthouse, plant; crown line at night.
- Budget: 2,152 triangles against the 5,000 cap (validated with `--budget 5000`).

### Draft manifest entry

```json
{"id": "211-main-street", "file": "211-main-street.glb", "anchor": [-122.392854, 37.7905944], "targetHeightM": 82.0, "cat": 3, "name": "211 Main Street (Charles Schwab Building)", "estimated": false, "dims": [73.2826, 72.8776, 82.0], "tris": 2152, "loadRadius": 2500}
```

### Integration notes

Case B: registry entry in `pipeline/lib/landmarks.mjs`, exclusion of OSM way 154217696 from the procedural bake, batch re-bake.

### Open risks

- Facade is inferred — check against a street photo before approval.
- Penthouse size inferred.
