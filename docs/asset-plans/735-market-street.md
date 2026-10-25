# 735 Market Street — SF-SIM asset plan

A six-storey 1907 commercial office block on the south side of Market between Third and Fourth (SF Assessor), a three-bay front on Market running 52 m through to Stevenson.

**Deliverable:** `artifacts/735-market-street/` (build script, GLB, validate/render wrappers, renders, REFERENCE.md, REPORT.md).

| | |
|---|---|
| Manifest id | `735-market-street` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.4041285, 37.7865717` (OSM way 149332505 OBB centre, recentred by `tk.run`) |
| Target height | **27.4 m** — DataSF LiDAR roof (majority 27.44 m; OSM height 28 m). The list's 77.4 m was the ring's max, a neighbour |
| Footprint | OSM way 149332505: 10 nodes, OBB 52.5 x 18.7 m, 902 m², light well on the east flank |
| Triangle cap | 3,000 (built: 1,042) |
| Category | `3` (office — `CAT.office` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Year / storeys | 1907 / 6 | published (SF Assessor, block 3706 lot 061) |
| Roof | 27.4 m | measured (LiDAR ring 201006.0003504 majority; max 127 m is a neighbour) |
| Footprint | 18.7 m front x 52.5 m deep, light well | measured (OSM) |
| Facade treatment | shopfronts, three bays of paired windows, cornice | inferred (no photo retrieved) |

### Sources

- OSM way 149332505 — https://www.openstreetmap.org/way/149332505
- SF Assessor historical rolls — https://data.sf.gov/resource/wv5m-vpq2
- DataSF LiDAR ring 201006.0003504 — https://data.sf.gov/resource/ynuv-fyni

### Orientation

Local +X = bearing 45.1° (NE along Market). **Market = NW face (18.7 m)**, **Stevenson = SE face**; both flanks are party walls.

### What each side shows

- NW (Market) and SE (Stevenson): shopfronts and windows (inferred).
- Flanks: blank.

### Recognition cues (ranked)

1. Narrow six-storey Market front with a cornice.
2. Glowing shopfronts.

### Massing recipe

- Sand prism on the OSM outline; shop panes with glow; five floors of 2.3 m windows; four piers; cornice; parapet; plant and a lit skylight.

### Palette

`Toy_sand`, `Toy_cream`, `Toy_glassd`, `Toy_roofd`, `Toy_steel`, trees; glow `Toy_sand_Glow`.

### Roof

Parapet, plant over the rear, a lit skylight.

### Triangle budget

1,042 tris (body 964, night_glow 78) against a cap of 3,000.

### Draft manifest entry

```json
{"id": "735-market-street", "file": "735-market-street.glb", "anchor": [-122.4041285, 37.7865717], "targetHeightM": 27.4, "cat": 3, "name": "735 Market Street", "estimated": false, "dims": [57.272, 56.9981, 27.4], "tris": 1042, "loadRadius": 2500}
```

### Integration notes

Case B. Exclude this way only (radius ≈ 26 m along the lot).

### Open risks

- Not a recognised landmark: no name, article or photo found; the selection's 77.4 m height was a LiDAR max from a neighbour, so it was picked by mistake. Consider dropping it at Gate 3.
- Facade entirely inferred.
