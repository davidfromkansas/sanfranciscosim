# 50 California Street — SF-SIM asset plan

A 37-storey pale grey slab at the foot of California Street: every face a close comb of deep precast vertical fins over dark glass, framed by broad solid corner piers and capped by a plain white band, over a plaza with a low pavilion on the east side of the lot.

**Deliverable:** `artifacts/50-california-street/` (Financial District batch, stages 1–2, BATCH mode).

| | |
|---|---|
| Manifest id | `50-california-street` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.3973858, 37.7940826` (OSM OBB centre via `tk.run`) |
| Target height | **148.44 m** — published roof 148.44 m (Wikipedia); LiDAR 153.71 m includes rooftop plant |
| Footprint | OSM way 32612484: OBB 61 × 41.9 m, 2289 m², long-axis bearing 171° |
| Triangle cap | 5,000 (tower ≥ 60 m; built: 3,176) |
| Category | `3` (Office — `CAT.office` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Roof height | 148.44 m | published (Wikipedia infobox) |
| LiDAR | 153.71 m | measured |
| Floors / year / architect | 37 / 1972 / Welton Becket | published |
| Floor area | 63,174 m² (≈ 1,700 m² a floor = the 31.7 × 61 m rectangle) | published / measured |
| Footprint | OBB 61 × 41.9 m, 2,289 m², 11 nodes | measured (OSM) |
| East bump = low pavilion ~7 m; white cap ~7 m |  | inferred (photo, floor area) |

### Sources

- OSM way 32612484 — https://www.openstreetmap.org/way/32612484
- Wikipedia — https://en.wikipedia.org/wiki/50_California_Street
- DataSF building footprints + 2010 LiDAR heights — https://data.sf.gov/resource/ynuv-fyni
- Commons photo (infobox) — https://commons.wikimedia.org/wiki/File:50_California_Street,_San_Francisco_(cropped).jpg

### Orientation

Local +x = bearing 81° (along California St), +y = 351°. California St = north face; the long faces run N–S; the pavilion is on the east side.

### What each side shows

- Two faces photographed: fin comb, solid corner piers, white cap.
- Other faces: same skin (**inferred**).
- Pavilion: low, glazed (**inferred**; a curved pavilion roof appears at the photo's edge).

### Recognition cues (ranked)

1. Pale ribbed box: dense vertical fins.
2. Broad solid white corner piers and blank top band.
3. Slender N–S slab proportion.

### Massing recipe

- Tower: 31.7 × 60.9 m rectangle; lobby 0–7 m inset dark glass with lit ring; concrete transfer band.
- Shaft 8–141 m: `Toy_glassd` body, `Toy_concrete` fins 0.4 × 0.6 m every 1.5 m, 2.6 m `Toy_white` corner piers.
- Cap 141–148.44 m: white band and parapet, deck, low plant.
- Pavilion: 10.2 × 35.7 m, 7 m, glazed and lit; stone plaza and four trees.

### Palette, roof, budget

- Palette: `Toy_concrete`, `Toy_white`, `Toy_glassd`, `Toy_roofd`, `Toy_steel`, `Toy_stone`, trees; glow `Toy_sand_Glow`, `Toy_white_Glow`.
- Roof: Dark deck inside a white parapet with a low plant cluster; crown line under the cap at night.
- Budget: 3,176 triangles against the 5,000 cap (validated with `--budget 5000`).

### Draft manifest entry

```json
{"id": "50-california-street", "file": "50-california-street.glb", "anchor": [-122.3973858, 37.7940826], "targetHeightM": 148.44, "cat": 3, "name": "50 California Street", "estimated": false, "dims": [57.085, 72.3941, 148.44], "tris": 3176, "loadRadius": 4453}
```

### Integration notes

Case B: registry entry in `pipeline/lib/landmarks.mjs`, exclusion of OSM way 32612484 from the
procedural bake, batch re-bake. 

### Open risks

- Cap depth and pavilion height read from the photo.
- Rooftop plant (LiDAR +5 m) kept below the crest.
