# 535 Mission Street — SF-SIM asset plan

A 27-storey blue glass office tower (HOK, 2014) on the south side of Mission between First and Second, next to the Transit Center. A plain slab in a four-sided structural-silicone skin whose one flourish is a folded corner: a tall triangular facet, a sliver at the base and a full chamfer at the roof, so each face reads as a single blue pane.

**Deliverable:** `artifacts/535-mission-street/` (build script, GLB, validate/render wrappers, renders, REFERENCE.md, REPORT.md).

| | |
|---|---|
| Manifest id | `535-mission-street` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.3981560, 37.7888721` (OSM way 127460048 OBB centre, recentred by `tk.run`) |
| Target height | **115 m** — published (Wikipedia/Emporis roof 378 ft); DataSF LiDAR ring 112.2 m majority, 115.7 m max agrees |
| Footprint | OSM way 127460048: OBB 45.4 x 28.7 m, 1,241 m², 12 nodes (a rectangle with small kinks), long axis 135.5° |
| Triangle cap | 5,000 (built: 2,282) |
| Category | `3` (office — `CAT.office` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Roof height | 115 m (378 ft) | published (Wikipedia infobox, Emporis 286156) |
| Floors / year / architect | 27 / 2014 / HOK | published |
| Footprint | OBB 45.4 x 28.7 m, 1,241 m² | measured (OSM) |
| Heading | long axis 135.5° (perpendicular to Mission) | measured (OSM) |
| LiDAR ring 201006.0001901 | majority 112.2 m, max 115.7 m | measured (DataSF) |
| Folded corner on the north (Mission x First side) corner |  | inferred (photo does not show which corner) |
| Lobby ~8 m |  | estimated |

### Sources

- OSM way 127460048 — https://www.openstreetmap.org/way/127460048
- Wikipedia, 535 Mission Street — https://en.wikipedia.org/wiki/535_Mission_Street
- Wikidata Q14681523 — https://www.wikidata.org/wiki/Q14681523
- Commons photo, 535 Mission Street, San Francisco.jpg — https://commons.wikimedia.org/wiki/File:535_Mission_Street,_San_Francisco.jpg
- DataSF LiDAR ring 201006.0001901 — https://data.sf.gov/resource/ynuv-fyni

### Orientation

Plan rectangle 45 x 28.4 m, local +X = bearing 135.5° (away from Mission), model yaw = 90 − 135.5. **Mission St = NW face (local −X, 28 m wide)**; Minna St = SE face; the long SW and NE faces are party walls to the Transit Center block neighbours (both visible above them).

### What each side shows

- NW (Mission): blue glass over the recessed lobby; street trees.
- N corner: the folded facet, dark glass, widening from 0.8 m at the lobby to a 10 m chamfer at the roof (corner choice inferred).
- SW / NE / SE: the same flush blue glass (inferred continuous, as published: four-sided SSG facade).

### Recognition cues (ranked)

1. Flush, light-blue glass slab, darker facet.
2. The folded corner growing with height.
3. Clear lobby with steel mullions.
4. Flat glass-screened roof.

### Massing recipe

- `tk.banded_loft` on a 5-point plan whose chamfered corner grows linearly with z (two storeys per band, flush glassl skin with thin glass lines).
- Dark `Toy_glass` quad laid on the facet plane (it is planar: the chamfer edge keeps its direction).
- Lobby 0–8 m: inset `glassl`, steel mullions, `sand_Glow` band, steel canopy.
- Parapet: glass screen ring to 115 m round a dark deck and a low plant cluster; `white_Glow` crown line.
- Lit windows via `tk.lit_loop_windows`, 0.24 m out so none sit behind the facet.

### Palette

`Toy_glassl`, `Toy_glass`, `Toy_steel`, `Toy_roofd`, `Toy_stone`, `Toy_leaf`, `Toy_rust`; glow `Toy_sand_Glow`, `Toy_white_Glow`. All core palette.

### Roof

Glass parapet screen (2.4 m) around a dark deck with five plant boxes; the crown light outlines it at night.

### Triangle budget

2,282 tris (body 1,808, night_glow 474) against a cap of 5,000.

### Draft manifest entry

```json
{"id": "535-mission-street", "file": "535-mission-street.glb", "anchor": [-122.398156, 37.7888721], "targetHeightM": 115.0, "cat": 3, "name": "535 Mission Street", "estimated": false, "dims": [60.142, 58.6236, 115.0], "tris": 2282, "loadRadius": 3450}
```

### Integration notes

Case B: registry entry, exclusion and re-bake. Neighbours 555 Mission (on this batch list) and 100 First share the block; keep the exclusion to this footprint (radius ≈ 26 m from the anchor).

### Open risks

- Which corner is folded is inferred (north); the photo's viewpoint is not recorded.
- LiDAR attributes are labelled 2010, but the tower opened 2014 — the ring's values match the finished tower, so the dataset evidently postdates the survey label.
- Lobby height estimated.
