# San Francisco Museum of Modern Art (SFMOMA) — SF-SIM asset plan

SFMOMA, 151 Third Street. Mario Botta's 1995 museum faces Yerba Buena Gardens across Third Street: symmetric, nearly windowless red-orange brick blocks stepping up toward a black-and-white striped cylinder, sliced on the bias and topped by a 130-ft elliptical skylight. Behind it, Snøhetta's 2016 expansion runs from Minna to Howard Street as a tall white mass with rippled horizontal bands. The OSM way covers both.

**Deliverable:** `artifacts/151-3rd-street/` (FiDi batch, stages 1–2; approval, optimize and integration by the lead).

| | |
|---|---|
| Manifest id | `151-3rd-street` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.4006347, 37.7859319` (from `tk.run`: OSM OBB centre + recentre shift) |
| Target height | **60.0 m, ESTIMATED** — crest of the 10-storey 2016 Snøhetta wing; no published height was found and the 2010 LiDAR predates it (the facts-file 58.4 m and ring 201006.0000183 max 79.0 m are pre-expansion/mixed). Botta's oculus top 39.6 m is published (130 ft) |
| Footprint | OSM way 41692824: 26 nodes, 6,639 m², OBB 108.5 × 84.5 m, bearing 135.2°; Botta block (65 × 49 m on Third St) and the Snøhetta wing behind (108 × 35 m) taken from the same polygon |
| Triangle cap | 5,000 (built: 2,554) |
| Category | `16` (Museum — `CAT.museum` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Botta oculus / skylight top | 39.6 m (130 ft) | published (Wikipedia, quoting NYT) |
| Snøhetta wing crest | 60 m | **estimated** (10 storeys) |
| Botta building | 5 storeys, 1995 | published |
| Expansion | 235,000 sq ft, Minna to Howard, 2016 | published (Wikipedia) |
| Botta step heights 12 / 20 / 28 m |  | inferred (photo) |

### Sources

- OSM way 41692824 — https://www.openstreetmap.org/way/41692824
- Wikipedia — https://en.wikipedia.org/wiki/San_Francisco_Museum_of_Modern_Art
- Commons photo — https://commons.wikimedia.org/wiki/File:San_Francisco_Museum_of_Modern_Art.jpg (Botta facade from Yerba Buena Gardens, pre-2016)
- DataSF 2010 LiDAR ring 201006.0000183 (mblr SF3722367) — https://data.sf.gov/resource/ynuv-fyni (pre-expansion)

### Orientation

Local axes: x along Third St (bearing 135°), y away from it (45°). SW face = Third St (Botta front, facing Yerba Buena); NW = Minna St; SE = Howard St (Snøhetta's glass gallery); NE = Natoma side (Snøhetta's rippled white facade).

### What each side shows

- SW (Third St): Botta's stepped brick front, striped cylinder, striped entrance (photo).
- NE and SE: Snøhetta's white rippled wing and Howard St glass gallery — **inferred** from published descriptions; no post-2016 photo was fetched.
- NW (Minna): brick side of Botta, white side of the wing, **inferred**.

### Recognition cues (ranked)

1. Black-and-white striped cylinder with a slanted oculus.
2. Symmetric red-orange brick blocks stepping up to it.
3. Tall white rippled Snøhetta mass behind.
4. Striped entrance on Third Street.

### Massing recipe

- Botta: `Toy_brick` blocks 0–12, 12–20, 20–28 m stepping back from the front and sides; stone string-courses; `Toy_ink` block behind the cylinder to 33.5 m.
- Cylinder r 9.5 m, 14 segments, alternating `Toy_ink`/`Toy_white` 1.9 m bands from 12 m to a bias-cut top (33 m front → 39.6 m back), `Toy_glassg` cap with a `Toy_white_Glow` oculus.
- Entrance: white portal slot with ink stripes and a lit door.
- Snøhetta wing: `tk.shaft` with `Toy_white` walls and `Toy_stone` ripple bands every 5.8 m to 56 m, sparse lit windows; Howard St glass gallery (lit); `tk.roof_kit` to 60 m.

### Palette

`Toy_brick`, `Toy_ink`, `Toy_white`, `Toy_stone`, `Toy_glassg`, `Toy_glassl`, `Toy_glassd`, `Toy_roofd`, `Toy_steel`; glow `Toy_white_Glow`, `Toy_sand_Glow`. Off-palette: `Toy_glassg` (documented).

### Roof

Botta's stepped brick roofs and the glowing oculus; the wing's deck with parapet and a plant cluster.

### Triangle budget

2,554 tris (body 2,454, night glow 100) against a 5,000 cap.

### Draft manifest entry

```json
{"id": "151-3rd-street", "file": "151-3rd-street.glb", "anchor": [-122.4006347, 37.7859319], "targetHeightM": 60.0, "cat": 16, "name": "San Francisco Museum of Modern Art (SFMOMA)", "estimated": true, "dims": [137.262, 112.9403, 60.0], "tris": 2554, "loadRadius": 2500}
```

### Integration notes

Case B (museum). The polygon is large and irregular: exclude by the OSM way, not a radius; the W hotel (south) and SFMOMA garage (Minna) must survive. Anchor includes a recentre shift of ~15 m because the model's bbox centre differs from the OBB centre. loadRadius 2,500 m.

### Open risks

- **Wing height estimated** (60 m); the whole model's crest depends on it.
- No post-2016 photo reviewed; the wing's facades are inferred.
- Split line between Botta and Snøhetta parts estimated from the footprint.
