# KPMG Building (55 Second Street) — SF-SIM asset plan

The KPMG Building, 55 Second Street (Heller Manus with HKS, 2002): a 25-storey postmodern office tower in warm beige granite with tall green-glass window strips. A three-storey base and an eleven-storey podium fill the site to a strong cornice, and the tower above rises with notched, stepped corners and two setbacks to a small crowned top.

**Deliverable:** `artifacts/55-2nd-street/` (FiDi batch, stages 1–2; approval, optimize and integration by the lead).

| | |
|---|---|
| Manifest id | `55-2nd-street` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.4003340, 37.7888147` (from `tk.run`: OSM OBB centre + recentre shift) |
| Target height | **100.6 m** — published (Wikipedia tallest list 100.6 m; infobox 100 m). DataSF LiDAR ring 201006.0001193 majority 107.6 m, max 110.4 m (measured) is higher — probably crown screens and masts; recorded, not used |
| Footprint | OSM way 79377189: 15 nodes (3 collinear dropped), 1,825 m², OBB 50.5 × 36.5 m, bearing 134.1°, with two small re-entrant notches |
| Triangle cap | 5,000 (built: 4,810) |
| Category | `3` (Office — `CAT.office` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Roof | 100.6 m | published; LiDAR majority 107.6 m (higher) |
| Floors / year / architects | 25 / 2002 / Heller Manus, HKS | published (Wikipedia) |
| Footprint | 50.5 × 36.5 m, 1,825 m² | measured (OSM) |
| Podium cornice ≈ 44 m (11 storeys), setbacks ≈ 84 and 92 m |  | inferred (photo) |

### Sources

- OSM way 79377189 — https://www.openstreetmap.org/way/79377189
- Wikipedia — https://en.wikipedia.org/wiki/KPMG_Building; https://en.wikipedia.org/wiki/List_of_tallest_buildings_in_San_Francisco
- Commons photo — https://commons.wikimedia.org/wiki/File:KPMG_Building_from_the_street_level.jpg
- DataSF 2010 LiDAR ring 201006.0001193 (mblr SF3708096) — https://data.sf.gov/resource/ynuv-fyni
- DataSF https://data.sf.gov/resource/wv5m-vpq2.json (assessor roll): 0055 2nd St, 2002, 24 storeys

### Orientation

Long axis 134° along Second Street. SW face = Second St; NW toward Stevenson/Market; SE toward Jessie St; NE party side.

### What each side shows

- SW (Second St) and NW corner: base, podium cornice, notched tower (photo).
- Other faces **inferred** the same.

### Recognition cues (ranked)

1. Warm beige granite with green-glass vertical window strips.
2. Strong cornice at the eleventh floor over a full-site podium.
3. Notched corners and two setbacks to a small crowned top.

### Massing recipe

- 0–12.6 m `Toy_sand` base, large `Toy_verdigris` window bays (lit); stone cornice.
- 13.4–44 m podium `tk.punched_block` (3.9 m storeys, panes 3.4 m); 1.2 m cornice.
- Tower `notch_rect(46, 32, 3)` 45.2–84 m; tier `notch_rect(40, 26, 3)` 84–92 m; top `notch_rect(30, 18, 2.5)` 92–97.4 m; stone bands at each setback.
- Crown cornice, sand parapet with white light line, plant to 100.6 m; dark decks on every setback.

### Palette

`Toy_sand`, `Toy_stone`, `Toy_verdigris`, `Toy_roofd`, `Toy_steel`; glow `Toy_sand_Glow`, `Toy_white_Glow`. All core palette.

### Roof

Three dark setback decks; the top deck has a parapet, light line and plant.

### Triangle budget

4,810 tris (body 4,172, night glow 638) against a 5,000 cap.

### Draft manifest entry

```json
{"id": "55-2nd-street", "file": "55-2nd-street.glb", "anchor": [-122.400334, 37.7888147], "targetHeightM": 100.6, "cat": 3, "name": "KPMG Building (55 Second Street)", "estimated": false, "dims": [68.5501, 67.9062, 100.6], "tris": 4810, "loadRadius": 3018}
```

### Integration notes

Case B. Exclusion radius ~28 m; neighbours on Second St (595 Market behind, the Stevenson St buildings) should survive. loadRadius 3,018 m.

### Open risks

- Published 100.6 m vs LiDAR roof plane 107.6 m: the model may sit ~7 m low against the LiDAR city mesh.
- Setback heights read from one upward-looking photo.
- Party faces not photographed.
