# Savings Union Bank Building — SF-SIM asset plan

A white granite banking temple at the foot of Grant Avenue, across O'Farrell from the Phelan Building's prow. The only view found is a distant aerial one in the Phelan Building's Commons photo: colossal Ionic columns under a pediment facing O'Farrell/Market and a large white dome. The miniature: near-square block on a plinth, colonnades between corner piers on the two street faces, entablature, pediment, attic, dome.

**Deliverable:** `artifacts/1-grant-avenue/` (Financial District batch, stages 1–2, BATCH mode).

| | |
|---|---|
| Manifest id | `1-grant-avenue` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.4051939, 37.7869990` (OSM OBB centre via `tk.run`) |
| Target height | **30.22 m** — DataSF 2010 LiDAR max 30.22 m (dome) of ring 201006.0004905; attic roof 25.6 m = ring median (measured; OSM height 26) |
| Footprint | OSM way 32946683: OBB 26.7 × 24.2 m, 646 m², long-axis bearing 81.4° |
| Triangle cap | 3,000 (building < 60 m; built: 858) |
| Category | `3` (Office — `CAT.office` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Crest (dome) | 30.22 m | measured (LiDAR max) |
| Attic roof | 25.6 m | measured (LiDAR median) |
| Year | 1910 | published (DataSF assessor roll) |
| Footprint | 26.7 × 24.2 m, 646 m² | measured (OSM) |
| Columns + pediment on O'Farrell, white dome |  | photographed (distant, in the Phelan photo) |
| Colonnade on Grant, column counts |  | inferred |

### Sources

- OSM way 32946683 — https://www.openstreetmap.org/way/32946683
- DataSF building footprints + 2010 LiDAR heights — https://data.sf.gov/resource/ynuv-fyni
- DataSF assessor historical secured rolls (year built, storeys) — https://data.sf.gov/resource/wv5m-vpq2
- Commons photo — https://commons.wikimedia.org/wiki/File:Phelan_Building_in_San_Francisco.JPG (1 Grant at lower right, from Central Tower)

### Orientation

Street grid: local +x = bearing 81.4° (Grant Ave, east face), +y = north; O'Farrell/Market = south face. Neighbours: Union Trust (2 Grant) across Grant, Phelan Building across O'Farrell.

### What each side shows

- S (O'Farrell): columns under a pediment — photographed (distant). E (Grant): colonnade — **inferred**.
- N and W: plain granite party walls (**inferred**).

### Recognition cues (ranked)

1. White granite temple-bank block with colossal columns.
2. Shallow dome on a drum above the attic.
3. Deep entablature and cornice.

### Massing recipe

- Plinth 0–1.4 m; `Toy_white` walls to 20 m with 2.6 m colonnade recesses on S and E; tall panes (lit) in the recesses.
- Four columns on O'Farrell, three on Grant (tapered 8-sided, `Toy_stone`); capital band, entablature, cornice.
- Attic to 25.6 m; stone drum; four-ring `Toy_white` dome; pediment over the O'Farrell colonnade; lantern with a lit oculus at 30.22 m.

### Palette, roof, budget

- Palette: `Toy_white`, `Toy_stone`, `Toy_glassd`, `Toy_roofd`, `Toy_concrete`; glow `Toy_sand_Glow`.
- Roof: Attic roof around a stone drum and a white dome with a lantern.
- Budget: 858 triangles against the 3,000 cap (validated with `--budget 3000`).

### Draft manifest entry

```json
{"id": "1-grant-avenue", "file": "1-grant-avenue.glb", "anchor": [-122.4051939, 37.786999], "targetHeightM": 30.22, "cat": 3, "name": "Savings Union Bank Building", "estimated": false, "dims": [35.71, 33.612, 30.22], "tris": 858, "loadRadius": 2500}
```

### Integration notes

Case B: registry entry in `pipeline/lib/landmarks.mjs`, exclusion of OSM way 32946683 from the
procedural bake, batch re-bake. 

### Open risks

- Only a distant aerial view: column counts and the Grant Avenue treatment are inferred.
- Dome height limited to the LiDAR max (30.22 m); its true radius may be larger.
