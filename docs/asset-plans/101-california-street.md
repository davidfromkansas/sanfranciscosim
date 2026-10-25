# 101 California Street — SF-SIM asset plan

A 48-storey faceted cylinder of blue glass standing on a seven-storey colonnade over a sloping glass atrium lobby, beside a pale granite triangular annex, with a granite plaza at California and Davis. The only round tower downtown.

**Deliverable:** `artifacts/101-california-street/` (Financial District batch, stages 1–2, BATCH mode).

| | |
|---|---|
| Manifest id | `101-california-street` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.3981206, 37.7929570` (OSM OBB centre via `tk.run`) |
| Target height | **183.0 m** — published roof 183 m (Wikipedia); LiDAR 175.24 m is the main roof, the stepped crown tiers rise to 183 m |
| Footprint | OSM way 1279505488: OBB 83.1 × 83.2 m, 4489 m², long-axis bearing 171.3° |
| Triangle cap | 5,000 (tower ≥ 60 m; built: 4,308) |
| Category | `3` (Office — `CAT.office` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Roof height | 183 m | published (Wikipedia infobox) |
| Main roof | 175.24 m | measured (DataSF 2010 LiDAR) |
| Floors / year | 48 / 1982 | published |
| Seven-storey glass lobby; triangular annex |  | published (Wikipedia description) |
| Site footprint | OBB 83.1 × 83.2 m, 4,489 m², 114 nodes | measured (OSM) |
| Tower circle | centre (13.1, −10.9) m local, r 27.7 m (25.7–30.6 serrations) | measured (circle fit to OSM arc) |
| Colonnade 28 m, annex 36 m |  | inferred (photo) |

### Sources

- OSM way 1279505488 — https://www.openstreetmap.org/way/1279505488
- Wikipedia — https://en.wikipedia.org/wiki/101_California_Street
- DataSF building footprints + 2010 LiDAR heights — https://data.sf.gov/resource/ynuv-fyni
- Commons photo (infobox) — https://commons.wikimedia.org/wiki/File:101_California_Street_2021.jpg (from Front St: colonnade, atrium, annex)

### Orientation

Local +x = bearing 81.3° (California St), +y = 351.3°. The tower stands in the east half; the triangular annex fills the SW (Front × Pine); the open plaza is NE (California × Davis) and the atrium leans against the annex's diagonal face toward it.

### What each side shows

- Front St (W): annex granite wall with deep windows, the colonnade and atrium beyond — photographed.
- Plaza (NE): sloping atrium glass and the round tower — partly photographed.
- Davis (E) and Pine (S): the round tower and annex walls (**inferred**).

### Recognition cues (ranked)

1. Round faceted blue glass tower (unique downtown).
2. Tower lifted on a tall colonnade.
3. Sloping glass atrium at its foot.
4. Stepped crown.
5. Pale granite triangular annex.

### Massing recipe

- Tower: 28-gon r 27.7 m; 0–28 m colonnade of 14 square stone columns around a recessed lit lobby; stone soffit; `Toy_glass` shaft 29.5–175 m with a pale `Toy_glassl` line every two storeys.
- Crown: two setback tiers (−2.5 m, −6 m) to 183 m, pale ledges, crown light.
- Annex: OSM SW triangle, `Toy_stone` punched block 0–36 m (4 m storeys), roof garden.
- Atrium: sloped `Toy_glassl` lean-to on the annex diagonal (28 m high, 16 m run) with 7 steel ribs and a lit skin.
- Plaza: stone apron over the site, three stepped planting terraces, five trees.

### Palette, roof, budget

- Palette: `Toy_glass`, `Toy_glassl`, `Toy_stone`, `Toy_glassd`, `Toy_steel`, `Toy_roofd`, `Toy_leafd`, trees; glow `Toy_sand_Glow`, `Toy_white_Glow`.
- Roof: Stepped glass crown with pale ledges and a dark top deck; crown line between the tiers at night.
- Budget: 4,308 triangles against the 5,000 cap (validated with `--budget 5000`).

### Draft manifest entry

```json
{"id": "101-california-street", "file": "101-california-street.glb", "anchor": [-122.3981206, 37.792957], "targetHeightM": 183.0, "cat": 3, "name": "101 California Street", "estimated": false, "dims": [94.9862, 95.1195, 183.0], "tris": 4308, "loadRadius": 5490}
```

### Integration notes

Case B: registry entry in `pipeline/lib/landmarks.mjs`, exclusion of OSM way 1279505488 from the
procedural bake, batch re-bake. 

### Open risks

- Colonnade and annex heights read from one photo.
- The tower's flat 'cut' face seen in the photo is not modelled.
- Atrium extent along the diagonal is simplified to one straight lean-to.
