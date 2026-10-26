# 201 Spear Street — SF-SIM asset plan

An 18-storey flat-topped office tower whose whole perimeter is folded into a fine saw-tooth — every 2.9 m the wall turns out 1.3 m, giving each office an angled window bay. No photograph could be obtained: the pleated plan is exact from OSM; materials, glazing and penthouse are inferred.

**Deliverable:** `artifacts/201-spear-street/` (Financial District batch, stages 1–2, BATCH mode).

| | |
|---|---|
| Manifest id | `201-spear-street` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.3919788, 37.7912423` (OSM OBB centre via `tk.run`) |
| Target height | **79.2 m** — LiDAR max 79.2 m = penthouse (DataSF 2010, parcel 3741032); main roof LiDAR median/mode 72.4 m; OSM 81 m not used |
| Footprint | OSM way 288645263: OBB 56.2 × 30.5 m, 1568 m², long-axis bearing 134.4° |
| Triangle cap | 5,000 (tower ≥ 60 m; built: 3,444) |
| Category | `3` (Office — `CAT.office` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Year / storeys | 1986 / 18 | published (assessor roll) |
| Roof / penthouse | 72.4 m median and mode / 79.2 m max | measured (DataSF LiDAR) |
| Footprint | OBB 56.2 × 30.5 m, 1,568 m², 123-node saw-tooth | measured (OSM) |
| Tooth pitch / depth | 2.9 m / 1.3 m | measured (OSM) |
| Materials, glazing, penthouse size |  | inferred / estimated (no photo) |

### Sources

- OSM way 288645263 — https://www.openstreetmap.org/way/288645263
- DataSF building footprints + 2010 LiDAR heights — https://data.sf.gov/resource/ynuv-fyni
- DataSF assessor secured roll 2023 — https://data.sf.gov/resource/wv5m-vpq2

### Orientation

Local +x = bearing 134.4° (along Spear, SE), +y = 44.4°. Every face is pleated the same way, so orientation affects only the penthouse and plant.

### What each side shows

- All four faces: saw-tooth bays with a window on each long leg (**inferred** from the plan; not photographed).

### Recognition cues (ranked)

1. Finely pleated saw-tooth perimeter.
2. Flat top with a central screened penthouse.
3. Light stone-coloured skin with dark windows.

### Massing recipe

- Programmatic saw-tooth plan (116 nodes) matching the OSM pattern, `Toy_stone` prism to 72.4 m (no bottom cap).
- Lobby 0–6 m: dark glass on each tooth's long leg, lit 80%.
- Offices: one dark window per tooth leg per storey pair (7.7 m bands) — per-storey panes would exceed the 5,000 cap.
- Roof deck, 22 × 13 m `Toy_stone` penthouse with steel louvres to 79.2 m, plant cluster, crown line.

### Palette, roof, budget

- Palette: `Toy_stone`, `Toy_glassd`, `Toy_steel`, `Toy_roofd`; glow `Toy_sand_Glow`, `Toy_white_Glow`.
- Roof: Dark deck, central louvred penthouse (steel cap), one plant cluster; white crown line around the penthouse.
- Budget: 3,444 triangles against the 5,000 cap (validated with `--budget 5000`).

### Draft manifest entry

```json
{"id": "201-spear-street", "file": "201-spear-street.glb", "anchor": [-122.3919788, 37.7912423], "targetHeightM": 79.2, "cat": 3, "name": "201 Spear Street", "estimated": false, "dims": [69.4837, 69.1046, 79.2], "tris": 3444, "loadRadius": 2500}
```

### Integration notes

Case B: registry entry in `pipeline/lib/landmarks.mjs`, exclusion of OSM way 288645263 from the
procedural bake, batch re-bake. 

### Open risks

- No photograph: skin colour, window proportion and penthouse size are guesses — the riskiest model in this group.
- OSM's 81 m tag disagrees with LiDAR (72.4 m roof, 79.2 m max).
- Windows read as two-storey slots.
