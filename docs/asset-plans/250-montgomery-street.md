# 250 Montgomery Street — SF-SIM asset plan

A mid-1980s sixteen-storey office tower on the east side of Montgomery between Bush and Pine. No usable photograph found (Wikipedia has no article; Commons category/search pages for the building and its streets yielded none, the Commons API search was rate-limited); the miniature is a downtown-plan-era treatment: rose-granite base, pale stone shaft with paired punched windows in shallow vertical recesses, a set-back two-storey top and a screened roof.

**Deliverable:** `artifacts/250-montgomery-street/` (Financial District batch, stages 1–2, BATCH mode).

| | |
|---|---|
| Manifest id | `250-montgomery-street` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.4023007, 37.7916998` (OSM OBB centre via `tk.run`) |
| Target height | **69.88 m** — DataSF 2010 LiDAR max 69.88 m of ring 201006.0004020 (roof screen); main roof 68.0 m = ring median (measured; OSM height 68) |
| Footprint | OSM way 256066242: OBB 22.8 × 35.2 m, 799 m², long-axis bearing 80.8° |
| Triangle cap | 5,000 (tower ≥ 60 m; built: 2,170) |
| Category | `3` (Office — `CAT.office` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Crest | 69.88 m | measured (LiDAR max) |
| Main roof | 68.0 m | measured (LiDAR median) |
| Year / storeys | 1986 / 17 (assessor), 16 (OSM) | published / OSM |
| Footprint | 35.2 × 22.8 m, 799 m² | measured (OSM) |
| Granite base, stone punched shaft, set-back top |  | inferred (no photo) |

### Sources

- OSM way 256066242 — https://www.openstreetmap.org/way/256066242
- DataSF building footprints + 2010 LiDAR heights — https://data.sf.gov/resource/ynuv-fyni
- DataSF assessor historical secured rolls (year built, storeys) — https://data.sf.gov/resource/wv5m-vpq2

### Orientation

Street grid: local +x = bearing 80.8° (east, Petrarch Place side), +y = north. Montgomery St = west face.

### What each side shows

- All faces **inferred** (no photograph).

### Recognition cues (ranked)

1. Pale stone 70 m slab with a darker granite base.
2. Set-back top storeys under a cornice.
3. Roof screen.

### Massing recipe

- `tk.rect(22.8, 35.2)` on yaw 80.8°; `Toy_granite` base 0–9 m with panes and lit lobby; stone cap.
- 9.7–60.6 m `tk.punched_block` (12 storeys of 4.24 m) `Toy_stone`, `Toy_sand` piers every 5.8 m.
- Granite cornice; 1.5 m set-back top 61.6–68 m (2 storeys, 40% lit); deck; granite screen around a steel plant core to 69.88 m; white crown line.

### Palette, roof, budget

- Palette: `Toy_granite`, `Toy_stone`, `Toy_sand`, `Toy_glassd`, `Toy_steel`, `Toy_roofd`, `Toy_concrete`; glow `Toy_sand_Glow`, `Toy_white_Glow`.
- Roof: Dark deck with a granite-screened plant core.
- Budget: 2,170 triangles against the 5,000 cap (validated with `--budget 5000`).

### Draft manifest entry

```json
{"id": "250-montgomery-street", "file": "250-montgomery-street.glb", "anchor": [-122.4023007, 37.7916998], "targetHeightM": 69.88, "cat": 3, "name": "250 Montgomery Street", "estimated": false, "dims": [33.7097, 43.1404, 69.88], "tris": 2170, "loadRadius": 2500}
```

### Integration notes

Case B: registry entry in `pipeline/lib/landmarks.mjs`, exclusion of OSM way 256066242 from the
procedural bake, batch re-bake. 

### Open risks

- **Facade fully inferred** — no photograph.
- Storey count differs between OSM (16) and the assessor (17).
