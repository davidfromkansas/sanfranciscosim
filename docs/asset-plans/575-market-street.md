# 575 Market Street — SF-SIM asset plan

The taller of the two Market Center towers: a 40-storey pale slab standing end-on to Market Street, its precast terra cotta wall punched by a tight grid of tall dark windows above a granite base, with a landscaped plaza shared with 555 Market.

**Deliverable:** `artifacts/575-market-street/` (Financial District batch, stages 1–2, BATCH mode).

| | |
|---|---|
| Manifest id | `575-market-street` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.4003805, 37.7895456` (OSM OBB centre via `tk.run`) |
| Target height | **174.65 m** — published roof 174.65 m (Wikipedia); LiDAR 175.39 m agrees |
| Footprint | OSM way 32963382: OBB 45.7 × 29.2 m, 1318 m², long-axis bearing 135.1° |
| Triangle cap | 5,000 (tower ≥ 60 m; built: 4,916) |
| Category | `3` (Office — `CAT.office` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Roof height | 174.65 m | published (Wikipedia, Market Center) |
| LiDAR | 175.39 m | measured |
| Floors / year / architect | 40 / 1975 / Hertzka & Knowles | published |
| Precast terra cotta over granite base |  | published |
| Footprint | OBB 45.7 × 29.2 m, 1,318 m² | measured (OSM) |
| Base 9 m, solid top band ~6 m |  | inferred (photo) |

### Sources

- OSM way 32963382 — https://www.openstreetmap.org/way/32963382
- Wikipedia — https://en.wikipedia.org/wiki/Market_Center_(San_Francisco)
- DataSF building footprints + 2010 LiDAR heights — https://data.sf.gov/resource/ynuv-fyni
- Commons photo (infobox) — https://commons.wikimedia.org/wiki/File:555-575_Market_Street.jpg (575 at right)

### Orientation

Local +x = bearing 135.1° (away from Market). NW narrow end = Market St; the long faces face NE (toward First) and SW (the shared plaza and 555 Market).

### What each side shows

- Long face and narrow end: window grid, solid top band — photographed.
- Other two faces: same (**inferred**).

### Recognition cues (ranked)

1. Tall pale slab with a tight grid of tall dark windows.
2. End-on to Market.
3. Plain solid top band.

### Massing recipe

- 45.5 × 29.2 m rectangle, yaw −45.1°.
- Base 0–9 m: inset dark lobby glass behind granite piers, lit ring; granite band.
- Shaft 10.4–167.4 m: `Toy_stone` prism, 39 storeys × one `Toy_glassd` window per 3.3 m bay.
- Top band to 174.65 m: parapet, deck, low plant; trees on the SW plaza.

### Palette, roof, budget

- Palette: `Toy_stone`, `Toy_granite`, `Toy_glassd`, `Toy_roofd`, `Toy_steel`, trees; glow `Toy_sand_Glow`, `Toy_white_Glow`.
- Roof: Dark deck inside a pale parapet with a low plant; crown line under the top band at night.
- Budget: 4,916 triangles against the 5,000 cap (validated with `--budget 5000`).

### Draft manifest entry

```json
{"id": "575-market-street", "file": "575-market-street.glb", "anchor": [-122.4003805, 37.7895456], "targetHeightM": 174.65, "cat": 3, "name": "575 Market Street", "estimated": false, "dims": [62.559, 62.5992, 174.65], "tris": 4916, "loadRadius": 5240}
```

### Integration notes

Case B: registry entry in `pipeline/lib/landmarks.mjs`, exclusion of OSM way 32963382 from the
procedural bake, batch re-bake. 

### Open risks

- The photo is at dusk: the wall reads grey-beige; published 'terra cotta' could be warmer.
- Window bay ~3.3 m is coarser than the real grid (triangle budget).
