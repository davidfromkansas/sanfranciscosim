# Merchants Exchange Building — SF-SIM asset plan

465 California Street (D. H. Burnham & Co. with Willis Polk, 1903–04), the Beaux-Arts Merchants Exchange; California Bank & Trust occupies its ground-floor banking hall, which is how the batch list named it. Fifteen storeys of pale granite and terracotta: a two-storey base whose California Street entrance is a deep portal between two giant Ionic columns under the carved name, a plain punched shaft, and an attic storey under a heavy cornice.

**Deliverable:** `artifacts/california-bank-and-trust/` (FiDi batch, stages 1–2; approval, optimize and integration by the lead).

| | |
|---|---|
| Manifest id | `california-bank-and-trust` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.4021502, 37.7925691` (from `tk.run`: OSM OBB centre + recentre shift) |
| Target height | **59.4 m** — published roof 195 ft (Wikipedia infobox); DataSF LiDAR ring majority 60.36 m, median 61.0 m (measured, agrees). The facts file's 66.7 m and ring max 72.4 m were not used (rooftop spill/plant) |
| Footprint | OSM way 256067740: 9 nodes, 1,983 m², OBB 36.6 × 54.5 m, bearing 80.8°; used as-is |
| Triangle cap | 3,000 (built: 2,806) |
| Category | `3` (Office — `CAT.office` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Roof / crest | 59.4 m (195 ft) | published; LiDAR majority 60.4 m |
| Floors / year / architects | 15 / 1904 / D. H. Burnham & Co., Willis Polk | published (Wikipedia, Wikidata Q6818435) |
| Footprint | 36.6 × 54.5 m, 1,983 m² | measured (OSM) |
| Portal: two giant Ionic columns, ≈ 9 m |  | inferred (photo) |
| Base 2 storeys ≈ 10 m |  | inferred (photo) |

### Sources

- OSM way 256067740 — https://www.openstreetmap.org/way/256067740 (`name=California Bank and Trust`, `wikidata=Q6818435`)
- Wikipedia — https://en.wikipedia.org/wiki/Merchants_Exchange_Building_(San_Francisco)
- Commons photo — https://commons.wikimedia.org/wiki/File:465_California_St_-_Merchants_Exchange_Building.jpg (California St base)
- DataSF 2010 LiDAR ring 201006.0001786 (mblr SF0260015) — https://data.sf.gov/resource/ynuv-fyni

### Orientation

Footprint used directly. North face = California St (portal and columns); east = Leidesdorff Street; west toward 425 California; south toward the block interior.

### What each side shows

- North (California): portal with two Ionic columns flanked by tall banking-hall windows (photo).
- East (Leidesdorff), west and south: plain punched stone walls **inferred**; the upper shaft is the same on all sides.

### Recognition cues (ranked)

1. Pale stone Beaux-Arts block among towers.
2. Two giant columns in the California St portal.
3. Heavy top cornice over an attic storey.
4. Even grid of punched windows.

### Massing recipe

- 0–10 m `Toy_stone` base with tall `Toy_glassd` windows (lit) on the side faces.
- California face: an 11 m `Toy_glassd` portal bay (lit) between two `Toy_white` columns (r 1.0 m, 8.4 m tall) with block capitals; flanking glass bays.
- 10–11 m white cornice; 11–52 m `tk.punched_block` (12 storeys, 3.42 m, panes at 4.2 m).
- 52–56.6 m attic with band; 56.6–58.2 m white cornice (1.3 m projection); stone parapet to 59.4 m; low plant.

### Palette

`Toy_stone`, `Toy_white`, `Toy_glassd`, `Toy_roofd`, `Toy_steel`; glow `Toy_sand_Glow`. All core palette.

### Roof

Dark deck inside a stone parapet over the cornice, with a few low plant boxes.

### Triangle budget

2,806 tris (body 2,422, night glow 384) against a 3,000 cap.

### Draft manifest entry

```json
{"id": "california-bank-and-trust", "file": "california-bank-and-trust.glb", "anchor": [-122.4021502, 37.7925691], "targetHeightM": 59.4, "cat": 3, "name": "Merchants Exchange Building", "estimated": false, "dims": [50.2966, 64.9855, 59.4], "tris": 2806, "loadRadius": 2500}
```

### Integration notes

Case B. Exclusion radius ~26 m; 425 California Street is the next lot west and the Bank of California across Leidesdorff/Sansome — check both survive. loadRadius 2,500 m.

### Open risks

- Rear and side elevations not photographed.
- Facts-file height 66.7 m conflicts with the published 59.4 m; the published figure and the LiDAR majority agree.
