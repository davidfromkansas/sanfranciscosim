# 601–605 Market Street (1917 office tower) — SF-SIM asset plan

A fifteen-storey 1917 office tower on the Market x Second corner (assessor parcel 3707001, "601 Market", 15 storeys, built 1917). It is believed to be the Santa Fe Building, but that name could not be verified (no Wikipedia article; Wikimedia rate limits blocked a Commons search hit). A narrow early-skyscraper "column": two-storey base, ten-storey pier-and-spandrel shaft, ornamented two-storey top, deep cornice.

**Deliverable:** `artifacts/605-market-street/` (Financial District batch, stages 1–2 of
docs/asset-pipeline/ADDRESS-TO-ASSET.md, BATCH mode).

| | |
|---|---|
| Manifest id | `605-market-street` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.4013149, 37.7889421` (OSM OBB centre, recentred by `tk.run`) |
| Target height | **54.3 m — measured** LiDAR median 54.30 m (SF3707001); max 61.3 m (roof structure or neighbour); OSM 54 |
| Footprint | OSM way 79377175: OBB 29.1 x 15.0 m, 436 m², 5 nodes, bearing 135° |
| Triangle cap | 3,000 (built: 2,192) |
| Category | `3` (office, `CAT.office` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Storeys / built | 15 / 1917 | published (DataSF assessor, parcel 3707001) |
| Roof | 54.3 m | measured (LiDAR median) |
| Footprint | 15 m on Market x 29 m on Second | measured (OSM) |
| Name "Santa Fe Building" |  | **unverified** |
| Facade (pale terracotta piers, arched attic, cornice) |  | **inferred** — no photo |

### Sources

- OSM way 79377175 — https://www.openstreetmap.org/way/79377175
- DataSF assessor rolls — https://data.sf.gov/resource/wv5m-vpq2.json (parcel 3707001)
- DataSF 2010 LiDAR footprints — https://data.sf.gov/resource/ynuv-fyni (SF3707001)

### Orientation

Rotated 45°: Market St = NW face (15 m), Second St = NE face (29 m); neighbours on SW and SE.

### What each side shows

- All four faces drawn alike (**inferred**); SW/SE are party walls in reality.

### Recognition cues (ranked)

1. Slim pale 15-storey tower on the Market x Second corner.
2. Vertical piers and an arched top storey.
3. Deep cornice.

### Massing recipe

- Stone base 0–8 m with dark shop panes and lit shop windows; trim cornice.
- Terracotta shaft 8.8–46.8 m (10 storeys of 3.8 m) with dark panes, lit panes and trim piers every 4.8 m.
- Band, arched attic 47.4–52 m, trim cornice 52–53.4 m, parapet to 54.3 m, deck and low plant.

### Palette

Toy_terracotta (off-palette), Toy_stone, Toy_trim, Toy_glassd, Toy_roofd, Toy_steel; glow Toy_sand_Glow.

### Roof

Dark deck inside a parapet with a low plant.

### Triangle budget

2,192 tris (body 1,746, night glow 446) against a cap of 3,000.

### Draft manifest entry

```json
{"id": "605-market-street", "file": "605-market-street.glb", "anchor": [-122.4013149, 37.7889421], "targetHeightM": 54.3, "cat": 3, "name": "601\u2013605 Market Street (1917 office tower)", "estimated": false, "dims": [38.3046, 38.0379, 54.3], "tris": 2192, "loadRadius": 2500}
```

### Integration notes

Case B: registry entry, exclusion circle sized to this footprint only, batch re-bake. `dims` is the world-axis
bbox including the sidewalk apron. `loadRadius` = max(2500, 30 x 54.3) = 2500. Build:
`blender -b --python artifacts/605-market-street/build_605_market_street.py`.

### Open risks

- Identity/name unverified; the lead may want a photo check before approval.
- Facade materials and colour are a guess; LiDAR max 61.3 m suggests a rooftop structure not modelled.
