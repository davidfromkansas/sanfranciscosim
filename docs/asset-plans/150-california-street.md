# 150 California Street — SF-SIM asset plan

A 24-storey office tower (HOK, 2000) at California x Front: a warm grey granite grid of square windows over a five-storey base, an open trellis along the roof line, and a column of stacked faceted blue glass bays climbing the Front St corner and rising above the roof.

**Deliverable:** `artifacts/150-california-street/` (build script, GLB, validate/render wrappers, renders, REFERENCE.md, REPORT.md).

| | |
|---|---|
| Manifest id | `150-california-street` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.3985069, 37.7936972` (OSM way 1279447597 OBB centre, recentred by `tk.run`) |
| Target height | **100.6 m** — published (Wikipedia/Emporis roof 100.59 m) as the glass-bay crest; LiDAR roof plane 96.9 m |
| Footprint | OSM way 1279447597: 19 nodes, OBB 41 x 41.1 m, 1,341 m² (41 x 29 m block + 13 x 12 m NE wing) |
| Triangle cap | 5,000 (built: 3,464) |
| Category | `3` (office — `CAT.office` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Roof height | 100.59 m | published (Wikipedia infobox, Emporis 118722) |
| Floors / year / architect | 24 / 2000 / HOK | published |
| LiDAR ring 201006.0001958 | majority 96.9 m, median 69 m, max 98.7 m | measured (DataSF) |
| Tower over the SW 32 x 22 m only, the rest a ~22 m base |  | inferred (LiDAR median says about half the footprint is low) |
| Glass bay column on the California x Front corner |  | photo + inferred corner |

### Sources

- OSM way 1279447597 — https://www.openstreetmap.org/way/1279447597
- Wikipedia, 150 California Street — https://en.wikipedia.org/wiki/150_California_Street
- Commons photo, 150 California, San Francisco.jpg — https://commons.wikimedia.org/wiki/File:150_California,_San_Francisco.jpg
- DataSF LiDAR ring 201006.0001958 — https://data.sf.gov/resource/ynuv-fyni

### Orientation

Local +X = bearing 80.4° (east along California). **California = S face**, **Front = W face**; the glass bay stands on the SW corner.

### What each side shows

- S (California) and W (Front): granite grid and the glass bay at their corner (photo shows one of them).
- N and E: same grid (inferred); the low base fills the rest of the lot.

### Recognition cues (ranked)

1. Faceted glass bay column on the corner, poking above the roof.
2. Granite grid of square windows.
3. Roof-line trellis frame.
4. Five-storey base.

### Massing recipe

- Base prism on the OSM block (0–22 m), large punched windows.
- Tower prism 32 x 22.4 m on the SW part (22–97 m), panes 3.45 m, lit 30%.
- Glass bay: `tk.banded_loft` on a chamfered 5-point corner loop, steel ledges every other floor, crest 100.6 m with a `sky_Glow` lantern band.
- Trellis: slim posts and a 1.2 m-proud frame ring over the roof deck; plant.

### Palette

`Toy_concrete`, `Toy_glassd`, `Toy_glassl`, `Toy_steel`, `Toy_roofd`, trees; glow `Toy_sand_Glow`, `Toy_sky_Glow`.

### Roof

Dark deck under the trellis frame, plant cluster, the glass bay's lit top.

### Triangle budget

3,464 tris (body 2,838, night_glow 626) against a cap of 5,000.

### Draft manifest entry

```json
{"id": "150-california-street", "file": "150-california-street.glb", "anchor": [-122.3985069, 37.7936972], "targetHeightM": 100.6, "cat": 3, "name": "150 California Street", "estimated": false, "dims": [51.1677, 52.7719, 100.6], "tris": 3464, "loadRadius": 3018}
```

### Integration notes

Case B. Exclude the whole OSM way (base included); radius ≈ 29 m.

### Open risks

- Split between tower and base is inferred from the LiDAR median, not observed.
- Which corner carries the glass bay is inferred (SW, the street corner).
- Published 100.59 m treated as the glass-bay crest; the main roof follows LiDAR 97 m.
