# One Post Street — SF-SIM asset plan

A 38-storey octagonal tower on the Market/Post/Montgomery flatiron. A close comb of dark bronze-brown stone piers runs unbroken from a tall glass lobby to a flat top over dark glass, and the plaza holds the octagonal two-tier BART entrance.

**Deliverable:** `artifacts/1-post-street/` (Financial District batch, stages 1–2, BATCH mode).

| | |
|---|---|
| Manifest id | `1-post-street` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.4026603, 37.7887621` (OSM OBB centre via `tk.run`) |
| Target height | **161.0 m** — published roof 161 m (529 ft, Wikipedia); LiDAR 166.04 m |
| Footprint | OSM way 32946671: OBB 33.3 × 35.2 m, 1130 m², long-axis bearing 171.3° |
| Triangle cap | 5,000 (tower ≥ 60 m; built: 2,866) |
| Category | `3` (Office — `CAT.office` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Roof height | 161 m (529 ft) | published (Wikipedia) |
| LiDAR | 166.04 m | measured |
| Floors / year / architect | 38 / 1969 / Welton Becket | published |
| Octagonal BART opening in the plaza |  | published |
| Footprint | OBB 33.3 × 35.2 m, 1,130 m², octagon | measured (OSM) |
| Lobby 8 m |  | inferred (photo) |

### Sources

- OSM way 32946671 — https://www.openstreetmap.org/way/32946671
- Wikipedia — https://en.wikipedia.org/wiki/McKesson_Plaza
- DataSF building footprints + 2010 LiDAR heights — https://data.sf.gov/resource/ynuv-fyni
- Commons photo (infobox) — https://commons.wikimedia.org/wiki/File:McKesson_Plaza_2021.jpg (from Post St)

### Orientation

Local +x = bearing 81.3°, +y = 351.3°. Post St = north face; Market St runs past the SE plaza; Montgomery to the east.

### What each side shows

- N (Post): pier comb, glass lobby — photographed.
- Other faces: same comb (**inferred**); BART well position on the plaza inferred.

### Recognition cues (ranked)

1. Slim dark octagonal prism.
2. Dense dark bronze piers.
3. Glass lobby and plaza.

### Massing recipe

- 8-node OSM octagon.
- Lobby 0–8 m `Toy_glassl` with lit ring; bronze transfer band.
- Shaft: `Toy_glassd` body, `Toy_bronze` piers 0.8 × 0.75 m every ~2.25 m to the roof, faint `Toy_ink` spandrel line every ~4 storeys.
- Flat top: deck, bronze parapet, low plant. Plaza with octagonal BART well and trees.

### Palette, roof, budget

- Palette: `Toy_bronze`, `Toy_glassd`, `Toy_glassl`, `Toy_ink`, `Toy_roofd`, `Toy_stone`, `Toy_steel`, trees; glow `Toy_sand_Glow`, `Toy_white_Glow`.
- Roof: Dark deck within a bronze parapet; low plant cluster.
- Budget: 2,866 triangles against the 5,000 cap (validated with `--budget 5000`).

### Draft manifest entry

```json
{"id": "1-post-street", "file": "1-post-street.glb", "anchor": [-122.4026603, 37.7887621], "targetHeightM": 161.0, "cat": 3, "name": "One Post Street", "estimated": false, "dims": [46.8054, 49.6789, 161.0], "tris": 2866, "loadRadius": 4830}
```

### Integration notes

Case B: registry entry in `pipeline/lib/landmarks.mjs`, exclusion of OSM way 32946671 from the
procedural bake, batch re-bake. 

### Open risks

- LiDAR 166 vs published 161 m (crest set to published).
- BART well position on the plaza approximate.
