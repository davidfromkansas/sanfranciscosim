# 650 California Street (Hartford Building) — SF-SIM asset plan

A 34-storey square modernist office tower (1964), briefly the tallest building in California. Every face is the same white precast-concrete square grid with floor-to-ceiling windows set deep inside it, over a tall glazed lobby behind white columns; the top storey has taller openings under a plain white parapet.

**Deliverable:** `artifacts/650-california-street/` (Financial District batch, stages 1–2, BATCH mode).

| | |
|---|---|
| Manifest id | `650-california-street` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.4052193, 37.7928669` (OSM OBB centre via `tk.run`) |
| Target height | **142.0 m** — published roof 142 m / 466 ft (Wikipedia, Wikidata, Emporis 118886); DataSF LiDAR roof median 142.8 m, max 151.3 m (rooftop plant) |
| Footprint | OSM way 260520160: OBB 38.9 × 38.6 m, 1500 m², long-axis bearing 171° |
| Triangle cap | 5,000 (tower ≥ 60 m; built: 3,398) |
| Category | `3` (Office — `CAT.office` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Roof | 142 m | published (Wikipedia, Wikidata P2048 466 ft); LiDAR median 142.8 m agrees |
| LiDAR max | 151.3 m (rooftop plant/equipment) | measured (ring 201006.0001729) — not modelled above the parapet |
| Storeys / year / architect | 34 / 1964 / SOM, Edward C. Bassett | published (Wikipedia; roll: 1963, 33) |
| Floor area | 461,000 sq ft | published (Wikipedia, assessor roll) |
| Footprint | OBB 38.9 × 38.6 m, 1,500 m², edges at 98.9° / 8.9° | measured (OSM) |
| Grid | 12 bays per face, one window per bay per storey | inferred (photo, south face) |

### Sources

- OSM way 260520160 — https://www.openstreetmap.org/way/260520160
- Wikipedia — https://en.wikipedia.org/wiki/650_California_Street
- Wikidata Q4642077 — https://www.wikidata.org/wiki/Q4642077
- DataSF building footprints + 2010 LiDAR heights — https://data.sf.gov/resource/ynuv-fyni
- DataSF assessor historical secured rolls (year built, storeys) — https://data.sf.gov/resource/wv5m-vpq2
- Commons photo (from St. Mary's Square, south) — https://commons.wikimedia.org/wiki/File:650_California_Street_02.jpg

### Orientation

Plan is the OSM polygon as-is; its edges run at 98.9° (along California St) and 8.9°; +Y = true north. **California St = S face** (lobby entrance, St. Mary's Square opposite), E toward Kearny, W toward Grant, N toward Sacramento.

### What each side shows

- S (California): photographed — white square grid, 12 bays, tall lobby behind columns, taller top storey.
- E, W, N: identical faces (the tower is a symmetric square prism; photo shows S and part of W) — N and E **inferred**.

### Recognition cues (ranked)

1. White precast square grid with deep dark windows on a plain square prism — the whitest tower on the northern FiDi skyline.
2. Tall, slender proportions (142 m on a 39 m square).
3. Tall glazed lobby behind white columns.
4. Flat top with a taller last storey and a plain parapet.

### Massing recipe

- Plan: the 4-node OSM polygon (38.7 m square, yaw 8.9°).
- Lobby 0–9 m: `glassl` set back 3 m, lit ring, 0.9 m white columns every 6.4 m, white soffit.
- Shaft 9–134 m: `tk.shaft` banded loft, dark glass 0.35 m inside the face, white 1.3 m spandrel per storey (31 storeys at 4.03 m).
- Top storey 134–140.4 m (one taller band) and a white parapet ring to 142 m.
- `tk.pier_grid` white verticals every 3.2 m (13 per face), flush with the spandrels, so the grid reads square.
- Roof: dark deck raised clear of the glass cap, low plant kept below the parapet line; sidewalk apron and three trees on California St.

### Palette, roof, budget

- Palette: `Toy_white`, `Toy_glassd`, `Toy_glassl`, `Toy_roofd`, `Toy_steel`, `Toy_stone`; glow `Toy_sand_Glow`.
- Roof: Flat dark deck inside a white parapet, low plant; LiDAR shows equipment to 151 m which is left out so the crest equals the published roof.
- Budget: 3,398 triangles against the 5,000 cap (validated with `--budget 5000`).

### Draft manifest entry

```json
{"id": "650-california-street", "file": "650-california-street.glb", "anchor": [-122.4052193, 37.7928669], "targetHeightM": 142.0, "cat": 3, "name": "650 California Street (Hartford Building)", "estimated": false, "dims": [51.0575, 51.206, 142.0], "tris": 3398, "loadRadius": 4260}
```

### Integration notes

Case B: registry entry in `pipeline/lib/landmarks.mjs`, exclusion of OSM way 260520160 from the
procedural bake, batch re-bake. 

### Open risks

- Rooftop equipment up to 151.3 m (LiDAR) not modelled; crest set to the published 142 m roof.
- N and E faces not photographed (assumed identical, which matches the building's square symmetric design).
- Lobby column rhythm (every other grid line) estimated from the photo.
