# 450 Sutter Street (Four Fifty Sutter Building) — SF-SIM asset plan

A 26-storey Art Deco medical-dental office tower of 1929, faced in pinkish-tan terracotta moulded with "Neo-Mayan" relief. Slim cream piers run the full height on every face and break the skyline as a toothed crest; the corners are rounded; the Sutter Street mass stands about three storeys above the rear mass, with a higher central block over both.

**Deliverable:** `artifacts/450-sutter-street/` (Financial District batch, stages 1–2, BATCH mode).

| | |
|---|---|
| Manifest id | `450-sutter-street` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.4078718, 37.7896331` (OSM OBB centre via `tk.run`) |
| Target height | **105.0 m** — published roof 105 m / 344 ft (Wikipedia, Emporis 118820); DataSF LiDAR max 103.3 m, majority 95.0 m, median 88.5 m |
| Footprint | OSM way 1186086081: OBB 49.4 × 41.3 m, 1959 m², long-axis bearing 170.9° |
| Triangle cap | 5,000 (tower ≥ 60 m; built: 4,172) |
| Category | `3` (Office — `CAT.office` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Crest (central block) | 105 m | published (Wikipedia infobox); LiDAR max 103.3 m corroborates |
| Sutter wing roof | 95.0 m | measured (LiDAR ring 201006.0001056 majority) |
| Rear wing roof | 84.1 m (3 storeys lower) | inferred (photo) + estimated |
| Storeys / year / architect | 26 / 1929 / Miller & Pflueger | published (Wikipedia; assessor roll: 1929, 26) |
| Floor area | 294,416 sq ft (~27,350 m²) | published (assessor roll) |
| Footprint | OBB 49.4 × 41.3 m, 1,959 m², edges at 98.6° / 8.6° | measured (OSM) |
| Two wings + link + central block plan | light courts between the wings on E and W | inferred (photo from the east) |

### Sources

- OSM way 1186086081 — https://www.openstreetmap.org/way/1186086081
- Wikipedia — https://en.wikipedia.org/wiki/450_Sutter_Street
- Wikidata Q4638113 — https://www.wikidata.org/wiki/Q4638113
- DataSF building footprints + 2010 LiDAR heights — https://data.sf.gov/resource/ynuv-fyni
- DataSF assessor historical secured rolls (year built, storeys) — https://data.sf.gov/resource/wv5m-vpq2
- Commons photo (infobox, from the east) — https://commons.wikimedia.org/wiki/File:450_Sutter_Street.jpg

### Orientation

Local +x = bearing 98.6° (along Sutter St), +y = 8.6° (north); +Y = true north. **Sutter St = S face** (main entrance, arched base), E face toward Stockton, N face toward Bush, W toward Powell.

### What each side shows

- E: photographed — the taller Sutter wing (left) with rounded corners, a recess, the lower rear wing (right), the central block above.
- S (Sutter): wing face with piers, arched bronze base with the lit entrance — base detail **inferred** from the description and HABS title.
- W and N: assumed to mirror the E face (**inferred**); OSM shows only a podium edge on the north lot line.
- Rear part of the lot (north ~10 m) is a 2-storey podium only (**inferred** from floor area vs. lot area).

### Recognition cues (ranked)

1. Dense rhythm of slim cream piers the full height, poking above the roof as a toothed crest.
2. Pinkish-tan terracotta skin with dark window strips between storey spandrels.
3. Two stepped masses with rounded corners and a higher central block.
4. Arched bronze base on Sutter St.

### Massing recipe

- Podium: the true OSM polygon (13 nodes), 0–7.5 m terracotta, arched bronze openings + lit arches on the Sutter face, cream band.
- Sutter wing 40.8 × 18.2 m and rear wing 40.4 × 17 m (local frame, yaw 8.6°): `tk.shaft` with dark glass and recessed terracotta spandrels, 24 / 21 storeys at 3.646 m.
- `tk.pier_grid` cream piers every 3 m, 0.85 m deep, running 1.8 m past each roof; 6-sided terracotta corner drums (rounded corners).
- Link 24 × 5 m between the wings (light courts E and W); central block 15 × 9 m to 101.5 m with piers, windows, a crown light band and a cap to 105 m.
- Roofs: terracotta parapet ring and a dark deck raised 0.1 m clear of the glass cap.

### Palette, roof, budget

- Palette: `Toy_terracotta`, `Toy_cream`, `Toy_glassd`, `Toy_bronze`, `Toy_roofd`; glow `Toy_sand_Glow`, `Toy_white_Glow`.
- Roof: Dark decks inside terracotta parapets on both wings with the pier crest around them; the central block caps the composition (no plant).
- Budget: 4,172 triangles against the 5,000 cap (validated with `--budget 5000`).

### Draft manifest entry

```json
{"id": "450-sutter-street", "file": "450-sutter-street.glb", "anchor": [-122.4078718, 37.7896331], "targetHeightM": 105.0, "cat": 3, "name": "450 Sutter Street (Four Fifty Sutter Building)", "estimated": false, "dims": [55.4222, 58.9497, 105.0], "tris": 4172, "loadRadius": 3150}
```

### Integration notes

Case B: registry entry in `pipeline/lib/landmarks.mjs`, exclusion of OSM way 1186086081 from the
procedural bake, batch re-bake. 

### Open risks

- Plan of the tower above the podium (two wings, link, central block) is inferred from one photo from the east and the floor area; no aerial or plan drawing checked.
- Rear wing height (84 m) estimated from the photo (~3 storeys below the Sutter wing).
- Published 105 m sits 1.7 m above the LiDAR max (103.3 m); model follows the published figure (rule: published > LiDAR).
- Mayan relief and the faceted bays reduced to colour + pier rhythm.
