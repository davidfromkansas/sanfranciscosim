# Central Plaza (455 Market Street) — SF-SIM asset plan

Central Plaza, 455 Market Street / 21–29 First Street (Kaplan McLaughlin Diaz, 1987–88): a 23-storey beige stone office tower on First Street between Market and Stevenson, with a nine-storey wing reaching forward to Market. The tower's corners are cut into sawtooth notches with dark glass bays and its top steps back. The batch list called it "First & Market tower (USPS building)"; the assessor roll and Wikipedia identify it as Central Plaza. The slug is kept.

**Deliverable:** `artifacts/first-and-market-usps/` (FiDi batch, stages 1–2; approval, optimize and integration by the lead).

| | |
|---|---|
| Manifest id | `first-and-market-usps` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.3984381, 37.7908114` (from `tk.run`: OSM OBB centre + recentre shift) |
| Target height | **96.9 m** — published roof 96.93 m (Wikipedia); DataSF LiDAR ring 201006.0001940 (tower lot) majority 96.45 m, max 100.74 m (measured, agrees). Market wing 36.5 m = majority of ring 201006.0002725 (measured) |
| Footprint | OSM way 159280395: 14 nodes, 2,404 m², OBB 83.8 × 35.7 m, bearing 135.1°; split at the DataSF lot boundary into the tower (SE, ≈ 41 × 30 m) and the Market wing (NW, ≈ 42 × 25 m) |
| Triangle cap | 5,000 (built: 4,770) |
| Category | `3` (Office — `CAT.office` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Roof / crest | 96.9 m | published; LiDAR majority 96.45 m |
| Market wing roof | 36.5 m | measured (LiDAR majority 36.56 m) |
| Floors / year / architect | 23 / 1987–88 / Kaplan McLaughlin Diaz | published (Wikipedia; assessor lots 3709/011–012) |
| Footprint | 83.8 × 35.7 m L-plan, 2,404 m² | measured (OSM) |
| Sawtooth corners with glass bays; stepped crown |  | inferred (photo) |

### Sources

- OSM way 159280395 — https://www.openstreetmap.org/way/159280395
- Wikipedia — https://en.wikipedia.org/wiki/Central_Plaza_(San_Francisco); https://en.wikipedia.org/wiki/List_of_tallest_buildings_in_San_Francisco
- Commons photo — https://commons.wikimedia.org/wiki/File:Central_Plaza_(San_Francisco)_2013-05-07_18-18.jpg (from First St, 425 Market behind)
- DataSF 2010 LiDAR rings 201006.0001940 (SF3709011) and 201006.0002725 (SF3709012) — https://data.sf.gov/resource/ynuv-fyni
- DataSF https://data.sf.gov/resource/wv5m-vpq2.json (assessor roll): 0455 Market and 0021 1st St, 1988, 23 storeys

### Orientation

Long axis bearing 135° along First Street. NW end = Market St (the lower wing); SW face = First St; SE end = Stevenson St; NE = party side toward 425 Market (the notches are on this face).

### What each side shows

- SW (First St) and SE: stone grid with punched windows, notched corners (photo).
- NW (Market): the nine-storey wing — **inferred** same cladding.
- NE: party side with two notches; treatment **inferred**.

### Recognition cues (ranked)

1. Beige stone tower with a flat punched-window grid.
2. Sawtooth notched corners with dark glass corner bays.
3. Stepped, set-back dark glass crown.
4. Lower wing in front on Market Street.

### Massing recipe

- Tower = OSM nodes on the SE side of the lot line; wing = the NW four.
- 0–6 m dark glass ground storey with `Toy_sand` piers and a lit lobby ring (both parts).
- Wing 6–35.3 m `Toy_sand` punched block (no windows on the seam face), parapet to 36.5 m, plant.
- Tower 6–36.5 m punched (seam and notch faces skipped), 36.5–88 m punched on all long faces; full-height `Toy_glassd` quads on the four short notch faces.
- 88 m stone band and terrace ring; set-back (2.5 m) `Toy_glassd` crown storeys with lit panes to 95.5 m; sand parapet to 96.9 m; plant.

### Palette

`Toy_sand`, `Toy_stone`, `Toy_glassd`, `Toy_roofd`, `Toy_steel`; glow `Toy_sand_Glow`, `Toy_white_Glow`. All core palette.

### Roof

Set-back glass crown with a sand parapet, dark deck and low plant; the wing has its own deck and plant cluster; a white light line rings the crown.

### Triangle budget

4,770 tris (body 4,044, night glow 726) against a 5,000 cap.

### Draft manifest entry

```json
{"id": "first-and-market-usps", "file": "first-and-market-usps.glb", "anchor": [-122.3984381, 37.7908114], "targetHeightM": 96.9, "cat": 3, "name": "Central Plaza (455 Market Street)", "estimated": false, "dims": [91.3512, 83.4028, 96.9], "tris": 4770, "loadRadius": 2907}
```

### Integration notes

Case B. The OSM way covers two DataSF rings; exclude by this way (radius ~45 m along the long axis is too big — use the polygon) and make sure 425 Market (NE neighbour) and First Market Tower survive. loadRadius from the 96.9 m height. loadRadius 2,907 m.

### Open risks

- "USPS" in the list name is not explained by any source found; identity rests on the assessor roll and Wikipedia coordinates (24 m from the OBB centre).
- The wing's height and cladding are from LiDAR and inference only.
- Crown setback depth estimated.
