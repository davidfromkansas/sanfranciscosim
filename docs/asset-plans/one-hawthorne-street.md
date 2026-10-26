# One Hawthorne — SF-SIM asset plan

EHDD's 24-storey, 165-unit condominium tower (2010) at Howard × Hawthorne in SoMa: "a simple, eight-story pre-cast concrete and limestone base" with a glassy residential shaft and a panoramic roof garden. No photo could be fetched (Wikimedia rate-limited).

**Deliverable:** `artifacts/one-hawthorne-street/` (Financial District batch, stages 1–2, BATCH mode).

| | |
|---|---|
| Manifest id | `one-hawthorne-street` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.3989026, 37.7857768` (OSM OBB centre via `tk.run`) |
| Target height | **83.9 m** — measured: DataSF LiDAR peak 83.9 m (crown); main roof = LiDAR majority 72.9 m / median 74.0 m. The 2010 survey post-dates the 2009 topping-out. OSM height 93 m is unsourced |
| Footprint | OSM way 260318176: OBB 49.8 × 30 m, 1,172 m², long-axis bearing 134.8° |
| Triangle cap | 5,000 (tower ≥ 60 m; built: 3,272) |
| Category | `2` (Apartments — `CAT.apartments` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Storeys / units / year | 24 / 165 / 2010 | published (EHDD, SocketSite) |
| Eight-storey precast + limestone base; roof garden |  | published (EHDD) |
| Roof | majority 72.9 m, median 74.0 m, peak 83.9 m | measured (DataSF 201006.0002860) |
| Footprint | L-shaped, OBB 49.8 × 30 m, 1,172 m² | measured (OSM way 260318176) |
| Tower over the main rectangle, 8-storey east wing, glass colours, crown |  | inferred |

### Sources

- OSM way 260318176 — https://www.openstreetmap.org/way/260318176
- EHDD project page — https://ehdd.com/project/one-hawthorne-luxury-condominiums/
- SocketSite topping-out — https://socketsite.com/?p=4072
- DataSF assessor roll (3735A, 2010 condominiums) — https://data.sf.gov/resource/wv5m-vpq2.json
- DataSF 2010 LiDAR footprints — https://data.sf.gov/resource/ynuv-fyni

### Orientation

SoMa grid, u = bearing 45° (NE), v = 315° (NW). Hawthorne St runs along v; Howard St along u. The L's short wing points SE-NE (inferred street sides).

### What each side shows

- All faces: inferred (no photograph). Base/shaft split follows EHDD's description.

### Recognition cues (ranked)

1. Pale limestone base, glassy light shaft with white slab edges.
2. Roof garden and a glazed crown block.
3. L-shaped footprint.

### Massing recipe

- Base 0–26 m: `Toy_stone` tall ground floor + seven punched storeys of 3.0 m, cream cap.
- Shaft 26.8–73 m over the 21.4 × 49.5 m main rectangle: `tk.shaft` 16 storeys of 2.89 m, `Toy_glassl` with `Toy_white` slab edges and mullions at 3.2 m.
- Roof: white parapet, two `Toy_leaf` garden beds, glazed crown 10 × 14 m to 83.9 m with a white frame; garden on the east wing roof.

### Palette, roof, budget

- Palette: `Toy_stone`, `Toy_cream`, `Toy_glassl`, `Toy_glassd`, `Toy_white`, `Toy_roofd`, `Toy_leaf`, `Toy_leafd`; glow `Toy_sand_Glow`, `Toy_white_Glow`.
- Roof: Roof garden beds with lamp glow, glazed crown block, white parapet.
- Budget: 3,272 triangles against the 5,000 cap (validated with `--budget 5000`).

### Draft manifest entry

```json
{"id": "one-hawthorne-street", "file": "one-hawthorne-street.glb", "anchor": [-122.3989026, 37.7857768], "targetHeightM": 83.9, "cat": 2, "name": "One Hawthorne", "estimated": false, "dims": [64.7939, 58.3946, 83.9], "tris": 3272, "loadRadius": 2517}
```

### Integration notes

Case B: registry entry in `pipeline/lib/landmarks.mjs`, exclusion of OSM way 260318176 from the procedural bake, batch re-bake.

### Open risks

- Facade colours and crown form are inferred — check against a photo before approval.
- The 11 m crown (LiDAR peak) may be a smaller lift/plant element; footprint of the crown inferred.
- Tower vs wing split inferred from the L footprint and the LiDAR majority.
