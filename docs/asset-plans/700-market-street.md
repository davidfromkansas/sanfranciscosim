# Mutual Savings Bank Building (700 Market Street) — SF-SIM asset plan

William Curlett's 1902 French Renaissance Revival bank tower at the Market / Kearny / Geary junction, one of the city's earliest skyscrapers (NRHP 2014): twelve storeys of grey granite and Colusa sandstone on a slim three-bay front — arched base, punched shaft, arcaded top storey, deep cornice — under a red-tile mansard with a pedimented oculus dormer and green cresting.

**Deliverable:** `artifacts/700-market-street/` (Financial District batch, stages 1–2 of
docs/asset-pipeline/ADDRESS-TO-ASSET.md, BATCH mode).

| | |
|---|---|
| Manifest id | `700-market-street` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.4038192, 37.7877278` (OSM OBB centre, recentred by `tk.run`) |
| Target height | **57.9 m — measured** LiDAR max 57.93 m = mansard cresting (SF0312031); median 47.7 m = balustrade. OSM `height=47` is the cornice |
| Footprint | OSM way 149335987: OBB 23.1 x 24.5 m, 432 m², 5 nodes |
| Triangle cap | 3,000 (built: 1,596) |
| Category | `3` (office, `CAT.office` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Storeys / built / architect | 12 / 1902 / William F. Curlett | published (Wikipedia, NRHP 13001107) |
| Materials | 2 storeys Raymond granite, 10 of Colusa sandstone, limestone, terracotta; mansard roof | published |
| Crest | 57.9 m | measured (LiDAR max) |
| Balustrade / cornice | 47.7 m / 45.6–46.9 m | measured (LiDAR median) / inferred (photo scale) |
| Market front width | 16.3 m, three bays | measured (OSM) / photo |

### Sources

- OSM way 149335987 — https://www.openstreetmap.org/way/149335987
- Wikipedia — https://en.wikipedia.org/wiki/Mutual_Savings_Bank_Building
- Commons photo — https://commons.wikimedia.org/wiki/File:Mutual_Savings_Bank_Building_700_Market_Street_(cropped).jpg
- DataSF 2010 LiDAR footprints — https://data.sf.gov/resource/ynuv-fyni (SF0312031)

### Orientation

Irregular 5-gon. Market St is the SE face (local edge at bearing 225°); Kearny/Geary on the N and W sides.

### What each side shows

- SE (Market): photographed — arched base, three-bay shaft, arched attic, dormer on the mansard.
- N / W (Geary, Kearny): same stone treatment (**inferred**; the brick building on the right of the photo is the neighbour).

### Recognition cues (ranked)

1. Red-tile mansard with a dormer and green cresting on a slim grey stone tower.
2. Deep cornice and balustrade over an arcaded top storey.
3. Arched two-storey base at the Lotta's Fountain junction.

### Massing recipe

- Concrete-grey base 0–12 m with 3.6 m arches at 5.4 m and lit arches; trim belt.
- Punched shaft 12.8–40.4 m (8 storeys of 3.45 m), mid cornice, arched attic 41.3–45.6 m.
- Main cornice 45.6–46.9 m, balustrade to 47.7 m, terrace deck.
- Coral mansard frustum 47–55.8 m (plan inset 1.0 -> 5.2 m), flat top, verdigris cresting to 57.9 m.
- Dormer on the Market face: stone box with paired lit windows, pediment slab, oculus arch.

### Palette

Toy_concrete (grey stone, off-palette), Toy_stone, Toy_trim, Toy_coral (tile roof), Toy_verdigris, Toy_glassd, Toy_roofd; glow Toy_sand_Glow.

### Roof

The mansard itself, with dark flat top and cresting; not blank from the aerial camera.

### Triangle budget

1,596 tris (body 1,270, night glow 326) against a cap of 3,000.

### Draft manifest entry

```json
{"id": "700-market-street", "file": "700-market-street.glb", "anchor": [-122.4038192, 37.7877278], "targetHeightM": 57.9, "cat": 3, "name": "Mutual Savings Bank Building (700 Market Street)", "estimated": false, "dims": [30.2498, 32.5953, 57.9], "tris": 1596, "loadRadius": 2500}
```

### Integration notes

Case B: registry entry, exclusion circle sized to this footprint only, batch re-bake. `dims` is the world-axis
bbox including the sidewalk apron. `loadRadius` = max(2500, 30 x 57.9) = 2500. Build:
`blender -b --python artifacts/700-market-street/build_700_market_street.py`.

### Open risks

- Mansard footprint assumed to cover the whole plan; the real roof may be shorter at the rear.
- N/W elevations not photographed.
