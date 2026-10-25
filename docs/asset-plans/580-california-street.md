# 580 California Street — SF-SIM asset plan

A 23-storey postmodern office tower (Johnson/Burgee, 1987) at California x Kearny: pale granite with columns of round glass bay windows, crowned by a steep dark mansard and the twelve hooded, faceless "Corporate Goddesses" by Muriel Castanis on the top storey, three a side.

**Deliverable:** `artifacts/580-california-street/` (build script, GLB, validate/render wrappers, renders, REFERENCE.md, REPORT.md).

| | |
|---|---|
| Manifest id | `580-california-street` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.4041520, 37.7929843` (OSM way 148741786 OBB centre, recentred by `tk.run`) |
| Target height | **107 m** — published (Wikipedia/Emporis roof 107 m / 351 ft); LiDAR roof plane 97.3 m, mansard crest 104.8 m |
| Footprint | OSM way 148741786: OBB 39.0 x 37.7 m, 1,471 m², 4 nodes, edges 170.3° / 80.3° |
| Triangle cap | 5,000 (built: 3,794) |
| Category | `3` (office — `CAT.office` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Height | 107 m (351 ft) | published (Wikipedia infobox, Emporis 118856) |
| Floors / year / architect | 23 / 1987 / Johnson/Burgee | published |
| Statues | 12 figures, 12 ft (3.7 m), three per side on the 23rd floor | published |
| Footprint | OBB 39.0 x 37.7 m, 1,471 m² | measured (OSM) |
| LiDAR ring 201006.0001751 | majority 97.3 m (roof), max 104.8 m | measured (DataSF) |
| Bays per face, mansard pitch, corner pavilions | 4 bays, ~7 m mansard | estimated from the photo |

### Sources

- OSM way 148741786 — https://www.openstreetmap.org/way/148741786
- Wikipedia, 580 California Street — https://en.wikipedia.org/wiki/580_California_Street
- Wikidata Q2817725 — https://www.wikidata.org/wiki/Q2817725
- Commons photo, 580 California Street.jpg — https://commons.wikimedia.org/wiki/File:580_California_Street.jpg
- DataSF LiDAR ring 201006.0001751 — https://data.sf.gov/resource/ynuv-fyni

### Orientation

Near-square plan; local +X = bearing 170.3° (toward California St). **California = S face (local +X)**, **Kearny = W face**; the N face looks toward Sacramento over lower neighbours; the E face is a party wall but stands clear above its neighbour, so it is treated like the others.

### What each side shows

- All four faces (photo shows S and W; N and E inferred identical): flat granite corner zones with punched windows, four round glass bays between, a goddess triple at the top.
- Base: arched openings, lit at night; trees on California.

### Recognition cues (ranked)

1. The hooded white goddesses on the top storey (semantically enlarged to ~5 m).
2. Steep dark mansard with corner pavilions and a lantern.
3. Vertical columns of round glass bays in pale granite.
4. Arched base.

### Massing recipe

- Granite prism; corner zones carry punched windows on their outer faces only.
- 16 half-hexagon bay prisms (`glassl`) with granite spandrel quads every other storey and lit panes.
- Shaft cornice at 89 m, inset attic 89.9–95 m with windows, 12 two-part white cones (statues).
- Eave cornice; `tk.frustum` mansard 96.5–103 m; four corner pavilions with copper pyramids; glass lantern with `white_Glow` and a copper cap to 107 m.

### Palette

`Toy_stone`, `Toy_concrete`, `Toy_glassl`, `Toy_glassd`, `Toy_white`, `Toy_roofd`, `Toy_copper`; glow `Toy_sand_Glow`, `Toy_white_Glow`. Off-palette `concrete`, `copper` (kit EXTRA_HEX).

### Roof

Dark mansard, corner pavilions, lit lantern — the whole roof is designed; no plant needed.

### Triangle budget

3,794 tris (body 2,968, night_glow 826) against a cap of 5,000.

### Draft manifest entry

```json
{"id": "580-california-street", "file": "580-california-street.glb", "anchor": [-122.404152, 37.7929843], "targetHeightM": 107.0, "cat": 3, "name": "580 California Street", "estimated": false, "dims": [50.0296, 51.0103, 107.0], "tris": 3794, "loadRadius": 3210}
```

### Integration notes

Case B. Free-standing on its block corner; exclusion radius ≈ 27 m.

### Open risks

- Published 107 m sits 2.2 m above the LiDAR crest (104.8 m); the model follows the published figure (rule: published > LiDAR).
- Bay count and mansard proportions from one upward photo.
- Statues enlarged for readability (a deliberate toy liberty).
