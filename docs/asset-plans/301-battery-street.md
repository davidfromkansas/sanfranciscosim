# Old Federal Reserve Bank (Bently Reserve) — SF-SIM asset plan

George W. Kelham's 1924 Federal Reserve Bank at 400 Sansome / 301 Battery (NRHP 1989, SF Landmark 158), now the Bently Reserve: grey granite, a giant eight-column Ionic colonnade on Sansome under an eagle-studded entablature, three storeys of tall pilaster-framed windows, an attic and cornice. A U-shaped office block wraps the lower banking-hall court; a one-storey annex closes the Battery end.

**Deliverable:** `artifacts/301-battery-street/` (Financial District batch, stages 1–2 of
docs/asset-pipeline/ADDRESS-TO-ASSET.md, BATCH mode).

| | |
|---|---|
| Manifest id | `301-battery-street` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.4008159, 37.7943076` (OSM OBB centre, recentred by `tk.run`) |
| Target height | **47.6 m — measured** LiDAR majority 47.64 m (SF0229003); median 45.05, max 50.64 m |
| Footprint | OSM way 32947510 + parts 940071571 / 1285793212 / 940071563: OBB 72.4 x 37.0 m, 2,608 m², bearing 81.5° |
| Triangle cap | 3,000 (built: 2,814) |
| Category | `3` (office, `CAT.office` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Built / architect | 1924 / George W. Kelham | published (Wikipedia) |
| Lot | 119.5 x 275 ft, bounded by Sacramento, Sansome, Battery, Commercial | published |
| Assessor | 325 Battery, built 1924, 8 storeys | published (DataSF) |
| Roof | 47.6 m (majority), 45.0 m median | measured (LiDAR) |
| Colonnade 8 columns to ~15 m, entablature to ~17.6 m |  | inferred (photo) |
| Setback upper floor 40.4–47.6 m |  | **inferred** from LiDAR (photo does not show the top) |

### Sources

- OSM way 32947510 and parts — https://www.openstreetmap.org/way/32947510
- Wikipedia — https://en.wikipedia.org/wiki/Old_Federal_Reserve_Bank_Building_(San_Francisco)
- Commons photo — https://commons.wikimedia.org/wiki/File:Federal_Reserve_Bank_(San_Francisco).JPG
- DataSF 2010 LiDAR footprints — https://data.sf.gov/resource/ynuv-fyni (SF0229003)
- DataSF assessor rolls — https://data.sf.gov/resource/wv5m-vpq2.json

### Orientation

Long axis 81.5° (E–W). Sansome = W end (37 m, colonnade); Battery = E end (annex); Sacramento S; Commercial N.

### What each side shows

- W (Sansome): photographed colonnade, steps, entablature, pilastered upper storeys.
- S (Sacramento): photographed in part — the same pilaster order continues.
- N (Commercial): U arms with the lower court face between them (**inferred**).
- E (Battery): one-storey annex in front of the block (OSM part).

### Recognition cues (ranked)

1. Giant Ionic colonnade on Sansome.
2. Pale granite block with tall pilaster-framed windows.
3. U-plan around a lower court seen from above.

### Massing recipe

- U block 0–39 m stone with base panes, concrete entablature at 16 m, pilaster grid 17.6–33.2 m with tall panes, attic band and panes, cornice 39–40.4 m, roof deck.
- Setback upper floor (U inset 3.2 m) 40.4–46.6 m with parapet to 47.6 m.
- Court 0–18 m with a glassl skylight and sand-glow cap; panes on its Commercial St face.
- Annex 0–5 m. Colonnade: steps, 8 cylinders 0.85 m radius to 14.6 m, caps, entablature box, lit hall behind.

### Palette

Toy_stone, Toy_concrete (off-palette), Toy_glassd, Toy_glassl, Toy_roofd; glow Toy_sand_Glow.

### Roof

Two dark decks (main and setback), the lit court skylight; not blank from above.

### Triangle budget

2,814 tris (body 2,654, night glow 160) against a cap of 3,000.

### Draft manifest entry

```json
{"id": "301-battery-street", "file": "301-battery-street.glb", "anchor": [-122.4008159, 37.7943076], "targetHeightM": 47.6, "cat": 3, "name": "Old Federal Reserve Bank (Bently Reserve)", "estimated": false, "dims": [82.5657, 51.3874, 47.6], "tris": 2814, "loadRadius": 2500}
```

### Integration notes

Case B: registry entry, exclusion circle sized to this footprint only, batch re-bake. `dims` is the world-axis
bbox including the sidewalk apron. `loadRadius` = max(2500, 30 x 47.6) = 2500. Build:
`blender -b --python artifacts/301-battery-street/build_301_battery_street.py`.

### Open risks

- The setback top floor is inferred from LiDAR only.
- Embarcadero Center West / Le Méridien abuts to the north-east; check exclusions do not clip it.
