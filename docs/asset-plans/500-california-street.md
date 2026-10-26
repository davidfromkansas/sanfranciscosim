# Omni San Francisco Hotel (Financial Center Building) — SF-SIM asset plan

The Omni San Francisco Hotel, formerly the Financial Center Building, at the northwest corner of California and Montgomery (Frederick H. Meyer and Albin R. Johnson, 1926–27; hotel conversion and raised roof 2001–02). A Florentine Renaissance block: five storeys of rusticated tan cast stone with round-arched openings, a red-brick shaft of punched windows, and a top storey of arched windows under a corbelled cornice.

**Deliverable:** `artifacts/500-california-street/` (FiDi batch, stages 1–2; approval, optimize and integration by the lead).

| | |
|---|---|
| Manifest id | `500-california-street` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.4031981, 37.7931217` (from `tk.run`: OSM OBB centre + recentre shift) |
| Target height | **65.3 m** — LiDAR crest from the batch facts file (measured); DataSF ring 201006.0001979 majority 61.68 m (main roof), max 68.26 m; OSM `height=62`. No published height |
| Footprint | OSM way 1279459281: 7 nodes (3 collinear dropped), 1,791 m², OBB 42.5 × 42.2 m, bearing 171.1° |
| Triangle cap | 5,000 (built: 3,630) |
| Category | `7` (Hotel — `CAT.hotel` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Crest | 65.3 m | measured (facts-file LiDAR); main roof ≈ 62 m (LiDAR majority) |
| Storeys | 15 (1927) → 17 after the 2002 raised roof | published (Wikipedia) / assessor roll |
| Year / architects | 1926–27 / Frederick H. Meyer, Albin R. Johnson | published (Wikipedia) |
| Footprint | 42.5 × 42.2 m, 1,791 m² | measured (OSM) |
| Base 5 storeys ≈ 20 m; arched top storey |  | published (Wikipedia) + photo |

### Sources

- OSM way 1279459281 — https://www.openstreetmap.org/way/1279459281 (`wikidata=Q26699326`)
- Wikipedia — https://en.wikipedia.org/wiki/Omni_San_Francisco_Hotel
- Commons photo — https://commons.wikimedia.org/wiki/File:Omni_San_Francisco_Hotel.jpg (California St face)
- DataSF 2010 LiDAR ring 201006.0001979 (mblr SF0240003) — https://data.sf.gov/resource/ynuv-fyni
- DataSF https://data.sf.gov/resource/wv5m-vpq2.json (assessor roll): block 0240 lot 003, hotel, 17 storeys

### Orientation

Plan rotated ~9° from north. South face = California St; east = Montgomery St; west and north abut neighbours (the 2002 rear addition is on the north).

### What each side shows

- South (California) and east (Montgomery): cast-stone base with arches and the big arched entrance, brick shaft, arched top storey (photo of the California face).
- West and north: same treatment **inferred** (largely party walls in reality).

### Recognition cues (ranked)

1. Red-brick shaft on a tall tan rusticated base.
2. Round-arched ground storey and arched top-floor windows.
3. Deep corbelled cornice.

### Massing recipe

- 0–20 m `Toy_terracotta` base: arches (3.6 m at 5.2 m, lit), two rows of punched windows, band, top row; cornice.
- 21–54 m `Toy_rust` brick `tk.punched_block` (10 storeys, 3.3 m).
- 54–59.6 m arched-window storey (lit arches); 59.6–62 m terracotta cornice (1.3 m projection).
- Set-back (3 m) stone penthouse 62–64.5 m for the 2002 raised roof; low plant to 65.3 m; three small trees on California.

### Palette

`Toy_terracotta`, `Toy_rust`, `Toy_stone`, `Toy_glassd`, `Toy_roofd`, `Toy_steel`, `Toy_leaf`/`Toy_leafd`; glow `Toy_sand_Glow`. Off-palette: `Toy_terracotta` (documented).

### Roof

Parapet and dark deck around a set-back penthouse storey with a few low plant boxes.

### Triangle budget

3,630 tris (body 2,738, night glow 892) against a 5,000 cap.

### Draft manifest entry

```json
{"id": "500-california-street", "file": "500-california-street.glb", "anchor": [-122.4031981, 37.7931217], "targetHeightM": 65.3, "cat": 7, "name": "Omni San Francisco Hotel (Financial Center Building)", "estimated": false, "dims": [54.0911, 54.1823, 65.3], "tris": 3630, "loadRadius": 2500}
```

### Integration notes

Case B. Exclusion radius ~24 m; keep the neighbours on California (west) and Montgomery (north). loadRadius 2,500 m.

### Open risks

- Crest from the facts-file LiDAR value; the ring spans 61.7–68.3 m.
- The 2002 penthouse form is inferred (Wikipedia says only that the roof was raised).
- West/north faces are party walls in reality.
