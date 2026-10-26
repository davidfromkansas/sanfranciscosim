# 715–719 Market Street (Digital Garage) — SF-SIM asset plan

715–719 Market Street (assessor parcel 3706064: commercial office, built 1908, 7 storeys), today the Digital Garage coworking building, between the Central Tower and Third Street. A post-1906 masonry commercial block on a deep L-shaped lot: shop base, punched shaft, bracketed cornice. No photo could be fetched, so the facade is a period-typical inference.

**Deliverable:** `artifacts/715-market-street/` (Financial District batch, stages 1–2 of
docs/asset-pipeline/ADDRESS-TO-ASSET.md, BATCH mode).

| | |
|---|---|
| Manifest id | `715-market-street` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.4037015, 37.7868764` (OSM OBB centre, recentred by `tk.run`) |
| Target height | **32.6 m — measured** LiDAR median 32.58 m (SF3706064); max 41.4 m (neighbour/roof structure); OSM 33 |
| Footprint | OSM way 149332501: OBB 52.6 x 25.4 m, 1,045 m², 7-node L, bearing 135° |
| Triangle cap | 3,000 (built: 1,290) |
| Category | `3` (office, `CAT.office` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Storeys / built | 7 / 1908 | published (DataSF assessor, parcel 3706064) |
| Roof | 32.6 m | measured (LiDAR median) |
| Footprint | L: 16 m on Market, 52 m deep, second leg toward Third | measured (OSM) |
| Cream walls, shop base, cornice, sign band |  | **inferred** — no photo |

### Sources

- OSM way 149332501 — https://www.openstreetmap.org/way/149332501
- DataSF assessor rolls — https://data.sf.gov/resource/wv5m-vpq2.json (parcel 3706064)
- DataSF 2010 LiDAR footprints — https://data.sf.gov/resource/ynuv-fyni (SF3706064)

### Orientation

Market St = NW face (16 m); the lot runs 52 m SE; the long SW side is a party wall (left blank).

### What each side shows

- NW (Market) and NE/SE faces: windows (**inferred**).
- SW long side: blank party wall.

### Recognition cues (ranked)

1. A light 7-storey masonry block with a cornice on Market near Third.
2. Lit sign band on Market.

### Massing recipe

- Stone base 0–5.6 m with shopfront panes and lit shop windows; belt.
- Cream punched shaft 6.2–30.2 m (6 storeys of 4.0 m); cornice 30.2–31.6 m; parapet to 32.6 m.
- Ink sign band with a white glow strip on the Market face; deck and low plant.

### Palette

Toy_cream, Toy_stone, Toy_trim, Toy_ink, Toy_glassd, Toy_roofd, Toy_steel; glow Toy_sand_Glow, Toy_white_Glow.

### Roof

Dark deck inside a parapet with a plant cluster.

### Triangle budget

1,290 tris (body 1,086, night glow 204) against a cap of 3,000.

### Draft manifest entry

```json
{"id": "715-market-street", "file": "715-market-street.glb", "anchor": [-122.4037015, 37.7868764], "targetHeightM": 32.6, "cat": 3, "name": "715\u2013719 Market Street (Digital Garage)", "estimated": false, "dims": [62.0963, 55.4454, 32.6], "tris": 1290, "loadRadius": 2500}
```

### Integration notes

Case B: registry entry, exclusion circle sized to this footprint only, batch re-bake. `dims` is the world-axis
bbox including the sidewalk apron. `loadRadius` = max(2500, 30 x 32.6) = 2500. Build:
`blender -b --python artifacts/715-market-street/build_715_market_street.py`.

### Open risks

- Low notability: an ordinary 1908 commercial block. Kept because its height is verified and it fills the Market St wall next to Central Tower; the lead may prefer to drop it.
- Facade material and colour unknown.
