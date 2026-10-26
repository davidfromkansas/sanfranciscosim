# Mechanics' Institute (57 Post Street) — SF-SIM asset plan

The slug comes from an OSM name tag for a ground-floor tenant ("First National Bank of Northern California"). Assessor parcel 0311013 (57–65 Post St, 1909, 9 storeys) and the LiDAR ring identify the building as the Mechanics' Institute, Albert Pissis's 1910 Beaux-Arts home of the institute's library and chess room: light stone, a rusticated base with a round-arched entrance, a double-height arcade of library windows, a punched office shaft and a deep cornice.

**Deliverable:** `artifacts/mechanics-institute/` (Financial District batch, stages 1–2 of
docs/asset-pipeline/ADDRESS-TO-ASSET.md, BATCH mode).

| | |
|---|---|
| Manifest id | `mechanics-institute` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.4030408, 37.7887368` (OSM OBB centre, recentred by `tk.run`) |
| Target height | **43.0 m — measured** LiDAR median 42.97 m (SF0311013); OSM `height=43`. The list's 73.5 m was the LiDAR peak of a neighbour (McKesson Plaza / 1 Post) |
| Footprint | OSM way 32946665: OBB 32.4 x 23.0 m, 663 m², 5 nodes, bearing 171° |
| Triangle cap | 3,000 (built: 1,882) |
| Category | `15` (library, `CAT.library` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Building | 57 Post St, parcel 0311013, built 1909, 9 storeys | published (DataSF assessor) |
| Roof | 43.0 m | measured (LiDAR median) |
| Entrance arch, double-height arched windows |  | photo (base only) |
| Upper shaft and cornice |  | **inferred** (no photo of the upper floors) |

### Sources

- OSM way 32946665 — https://www.openstreetmap.org/way/32946665
- Commons photo (base) — https://commons.wikimedia.org/wiki/File:MechanicsInstituteSanFrancisco.jpg
- DataSF assessor rolls — https://data.sf.gov/resource/wv5m-vpq2.json (parcel 0311013)
- DataSF 2010 LiDAR footprints — https://data.sf.gov/resource/ynuv-fyni (SF0311013)

### Orientation

Post St is the north face (23 m); the lot runs ~32 m south toward Market; plan rotated ~8.6° from true N.

### What each side shows

- N (Post): rusticated base, cream portal arch, double-height library arcade (photo).
- E / W / S: party walls in reality; drawn with the same windows (**inferred**).

### Recognition cues (ranked)

1. Pale Beaux-Arts block with tall arched library windows over a rusticated base.
2. Round-arched entrance on Post.
3. Deep cornice.

### Massing recipe

- Stone base 0–6 m with rustication bands and arched openings; trim cornice.
- Library storey 6.8–14.6 m with 4 m arches (lit).
- Punched shaft 15.2–38.4 m (6 storeys of 3.87 m); top storey 38.9–41.2 m; cornice to 42.4 m; parapet to 43.
- Post portal: cream frame with dark arched door and lit fanlight.

### Palette

Toy_stone, Toy_concrete, Toy_trim, Toy_glassd, Toy_ink, Toy_roofd, Toy_steel; glow Toy_sand_Glow.

### Roof

Deck inside a stone parapet with a low plant.

### Triangle budget

1,882 tris (body 1,516, night glow 366) against a cap of 3,000.

### Draft manifest entry

```json
{"id": "mechanics-institute", "file": "mechanics-institute.glb", "anchor": [-122.4030408, 37.7887368], "targetHeightM": 43.0, "cat": 15, "name": "Mechanics' Institute (57 Post Street)", "estimated": false, "dims": [31.454, 41.8278, 43.0], "tris": 1882, "loadRadius": 2500}
```

### Integration notes

Case B: registry entry, exclusion circle sized to this footprint only, batch re-bake. `dims` is the world-axis
bbox including the sidewalk apron. `loadRadius` = max(2500, 30 x 43.0) = 2500. Build:
`blender -b --python artifacts/mechanics-institute/build_mechanics_institute.py`.

### Open risks

- Slug/name mismatch: manifest name should be the Mechanics' Institute, not the bank tenant.
- Upper facade is inferred; party-wall faces get windows they do not have.
