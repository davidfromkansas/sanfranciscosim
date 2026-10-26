# 525 Market Street — SF-SIM asset plan

A 39-storey cream box at First and Market, scored top to bottom by hundreds of narrow dark window slits between cream piers, with solid corner piers and a blank top band with no windows. In the miniature it is the pale pinstriped monolith on Market.

**Deliverable:** `artifacts/525-market-street/` (Financial District batch, stages 1–2, BATCH mode).

| | |
|---|---|
| Manifest id | `525-market-street` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.3991580, 37.7905074` (OSM OBB centre via `tk.run`) |
| Target height | **161.0 m** — published roof 161 m (Wikipedia); LiDAR 161.76 m agrees |
| Footprint | OSM way 32946570: OBB 57.7 × 48.7 m, 2797 m², long-axis bearing 45.1° |
| Triangle cap | 5,000 (tower ≥ 60 m; built: 2,954) |
| Category | `3` (Office — `CAT.office` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Roof height | 161 m | published (Wikipedia infobox) |
| LiDAR | 161.76 m | measured (DataSF 2010) |
| Floors / year / architect | 39 / 1973 / Warnecke | published |
| Footprint | OBB 57.7 × 48.7 m, 2,797 m², rectangle | measured (OSM) |
| Blind top band ~11 m |  | inferred (photo) |

### Sources

- OSM way 32946570 — https://www.openstreetmap.org/way/32946570
- Wikipedia — https://en.wikipedia.org/wiki/First_Market_Tower
- DataSF building footprints + 2010 LiDAR heights — https://data.sf.gov/resource/ynuv-fyni
- Commons photo (infobox) — https://commons.wikimedia.org/wiki/File:First_Market_Tower.jpg

### Orientation

Local +x = bearing 45.1° (parallel to Market). NW face = Market St, NE = First St, SE/SW = mid-block.

### What each side shows

- NW (Market) and NE (First): pinstripe slits, blind top — photographed (NE face).
- SE and SW: same skin (**inferred**).

### Recognition cues (ranked)

1. Pale cream monolith with dense vertical dark slits.
2. Blank top band.
3. Solid corner piers.

### Massing recipe

- 57.4 × 48.7 m rectangle at yaw 44.9°.
- Lobby 0–8 m: inset dark glass behind 1.2 m cream columns every 4.8 m, lit ring.
- Tower: `Toy_sand` prism; full-height `Toy_glassd` slits 0.55 m wide every ~1.55 m from 8.6 to 150 m, 2.6 m solid corners.
- Blind top band 150–161 m with a stone reveal line; parapet, deck, plant.

### Palette, roof, budget

- Palette: `Toy_sand`, `Toy_glassd`, `Toy_stone`, `Toy_roofd`, `Toy_steel`, trees; glow `Toy_sand_Glow`, `Toy_white_Glow`.
- Roof: Dark deck inside a low cream parapet, low plant cluster, crown line under the parapet at night.
- Budget: 2,954 triangles against the 5,000 cap (validated with `--budget 5000`).

### Draft manifest entry

```json
{"id": "525-market-street", "file": "525-market-street.glb", "anchor": [-122.399158, 37.7905074], "targetHeightM": 161.0, "cat": 3, "name": "525 Market Street", "estimated": false, "dims": [83.3787, 83.3573, 161.0], "tris": 2954, "loadRadius": 4830}
```

### Integration notes

Case B: registry entry in `pipeline/lib/landmarks.mjs`, exclusion of OSM way 32946570 from the
procedural bake, batch re-bake. 

### Open risks

- Top band depth read from the photo.
- SE/SW faces not photographed.
