# Aronson Building (706 Mission Street) — SF-SIM asset plan

The 1903 ten-storey Aronson Building at the NW corner of Third and Mission: a warm brick commercial block with a two-storey shopfront base, punched shaft, arcaded top storey and deep bracketed cornice. Since 2020 it is the restored base of the 43-storey Four Seasons Private Residences tower (Handel / TEN Arquitectos), which is a separate OSM way and is NOT modelled here.

**Deliverable:** `artifacts/706-mission-street/` (Financial District batch, stages 1–2 of
docs/asset-pipeline/ADDRESS-TO-ASSET.md, BATCH mode).

| | |
|---|---|
| Manifest id | `706-mission-street` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.4024839, 37.7862352` (OSM OBB centre, recentred by `tk.run`) |
| Target height | **44.0 m — measured** LiDAR median 43.9 m, max 49.4 m (SF3706093, 2010, before the tower). OSM `height=55 m` is unsourced |
| Footprint | OSM way 112878589: OBB 34.4 x 26.0 m, 885 m², 4 nodes, bearing 46° |
| Triangle cap | 3,000 (built: 1,814) |
| Category | `3` (office, `CAT.office` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Storeys / built | 10 / 1903 | OSM tags + photo |
| Roof | 44.0 m | measured (LiDAR median 43.9 m) |
| Footprint | 34.4 m on Mission x 26 m on Third | measured (OSM) |
| Brick walls, arcaded top, deep cornice |  | inferred (photo, building at right of the tower) |
| Wikidata Q23016604 | describes the 2020 tower, not this block | checked |

### Sources

- OSM way 112878589 — https://www.openstreetmap.org/way/112878589
- Wikipedia (tower) — https://en.wikipedia.org/wiki/Four_Seasons_Private_Residences_at_706_Mission_Street
- Commons photo — https://commons.wikimedia.org/wiki/File:706_Mission_Street_2021_02.jpg
- DataSF 2010 LiDAR footprints — https://data.sf.gov/resource/ynuv-fyni (SF3706093)
- DataSF assessor rolls — https://data.sf.gov/resource/wv5m-vpq2.json

### Orientation

Square-ish plan at 46° / 136°. Mission St = SE face (34 m), Third St = NE face (26 m); the tower abuts NW/SW.

### What each side shows

- NE / SE (Third, Mission): photographed brick front, arcaded attic, cornice.
- NW / SW: now against the new tower and its podium; drawn with the same treatment (**inferred**).

### Recognition cues (ranked)

1. Warm brick block with a heavy cornice on the Third x Mission corner, under the new glass tower.
2. Arcaded top storey.
3. Glassy two-storey shop base.

### Massing recipe

- Terracotta base 0–8 m with dark shopfront panes and lit shop windows; base cornice.
- Brick punched shaft 8.8–35.4 m (7 storeys of 3.8 m, paired windows at 2.15 m).
- Band, brick attic 36–41.8 m with 3.0 m arches at 4.3 m (lit), cornice 41.8–43.4 m, parapet to 44 m.
- Roof deck with a low plant.

### Palette

Toy_brick, Toy_terracotta (off-palette trim), Toy_glassd, Toy_roofd, Toy_stone, Toy_steel; glow Toy_sand_Glow.

### Roof

Dark deck inside a terracotta parapet with a low plant; the tower's podium is not included.

### Triangle budget

1,814 tris (body 1,380, night glow 434) against a cap of 3,000.

### Draft manifest entry

```json
{"id": "706-mission-street", "file": "706-mission-street.glb", "anchor": [-122.4024839, 37.7862352], "targetHeightM": 44.0, "cat": 3, "name": "Aronson Building (706 Mission Street)", "estimated": false, "dims": [49.901, 49.239, 44.0], "tris": 1814, "loadRadius": 2500}
```

### Integration notes

Case B: registry entry, exclusion circle sized to this footprint only, batch re-bake. `dims` is the world-axis
bbox including the sidewalk apron. `loadRadius` = max(2500, 30 x 44.0) = 2500. Build:
`blender -b --python artifacts/706-mission-street/build_706_mission_street.py`.

### Open risks

- When the tower is integrated, its own landmark will overlap the Aronson's NW/SW walls; exclusions must be coordinated.
- Brick tone from one sunlit photo.
