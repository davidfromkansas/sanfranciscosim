# 345 California Center — SF-SIM asset plan

A 48-storey mid-block tower of grey granite punched by square windows. Its top 11 floors are a hotel in two towers set at 45° to the slab, joined by a stack of glazed skybridge floors, each crowned by a square concrete shaft that steps thinner — the 'Tweezer Towers'.

**Deliverable:** `artifacts/345-california-street/` (Financial District batch, stages 1–2, BATCH mode).

| | |
|---|---|
| Manifest id | `345-california-street` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.4004566, 37.7925878` (OSM OBB centre via `tk.run`) |
| Target height | **211.8 m** — published architectural top 211.8 m (695 ft, top of the twin shafts); LiDAR 212 m agrees; roof 189 m (620 ft); masts to 721 ft not modelled |
| Footprint | OSM way 588355355: OBB 84.7 × 41.3 m, 3495 m², long-axis bearing 81.2° |
| Triangle cap | 5,000 (tower ≥ 60 m; built: 4,924) |
| Category | `3` (Office — `CAT.office` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Architectural top | 211.8 m (695 ft) | published (Wikipedia) |
| Roof / tip | 189 m (620 ft) / 721 ft | published |
| LiDAR | 212 m | measured |
| Floors / year / architect | 48 / 1986 / SOM | published |
| Hotel floors 38–48 in twin towers at 45°, skybridges |  | published |
| Site footprint | OBB 84.7 × 41.3 m, 3,495 m² | measured (OSM) |
| Slab 66 × 36 m to 154 m, hotel towers 22 m square, shafts step at 199 m, podium 20 m |  | inferred (photo of the top) / estimated |

### Sources

- OSM way 588355355 — https://www.openstreetmap.org/way/588355355
- Wikipedia — https://en.wikipedia.org/wiki/345_California_Center
- DataSF building footprints + 2010 LiDAR heights — https://data.sf.gov/resource/ynuv-fyni
- Commons photo (infobox) — https://commons.wikimedia.org/wiki/File:345_California_Street.JPG (upper half, from the north-west)

### Orientation

Local +x = bearing 81.2° (along California St), +y = 351.2°. California St = north face, Pine = south; the turrets sit at the east and west ends of the slab, rotated 45°.

### What each side shows

- Upper floors: split rotated hotel towers, glazed core, twin concrete shafts — photographed (one side).
- Lower slab and podium: grey granite, square windows (**inferred** from the upper photo; the base is not visible).

### Recognition cues (ranked)

1. Twin square concrete shafts ('tweezers').
2. Split top of two rotated towers with a glazed core.
3. Grey granite slab with square windows.

### Massing recipe

- Podium: full OSM rectangle 0–20 m, `Toy_concrete` with lit windows, deck and parapet.
- Slab: 66 × 36 m chamfered rectangle 20–154 m, 32 storeys of square `Toy_glassd` windows (5.2 m bays).
- Hotel towers: 22 m squares at ±17 m rotated 45°, 154–189 m, windows, deck, parapet, plant, crown lines.
- Glazed core 10 × 8 m between them with lit faces; twin `Toy_concrete` shafts 4.2 m → 2.6 m (step at 199 m) to 211.8 m, red tip lights.

### Palette, roof, budget

- Palette: `Toy_concrete` (off-palette grey granite), `Toy_glassd`, `Toy_glassl`, `Toy_roofd`, `Toy_steel`; glow `Toy_sand_Glow`, `Toy_white_Glow`, `Toy_red_Glow`.
- Roof: Plant on each hotel tower roof beside its shaft; red lights on the shaft tops.
- Budget: 4,924 triangles against the 5,000 cap (validated with `--budget 5000`).

### Draft manifest entry

```json
{"id": "345-california-street", "file": "345-california-street.glb", "anchor": [-122.4004566, 37.7925878], "targetHeightM": 211.8, "cat": 3, "name": "345 California Center", "estimated": false, "dims": [95.6132, 59.5307, 211.8], "tris": 4924, "loadRadius": 6354}
```

### Integration notes

Case B: registry entry in `pipeline/lib/landmarks.mjs`, exclusion of OSM way 588355355 from the
procedural bake, batch re-bake. 

### Open risks

- Only the upper half is photographed; slab size, podium height and the lower facade are inferred.
- The thin masts above the shafts (to 721 ft) are omitted so the crest is the architectural top.
- Hotel tower size and shaft step height read from one photo.
