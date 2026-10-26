# 625 Market Street ("Bank of America Building") — SF-SIM asset plan

A narrow 15-storey 1907 office tower on the SE corner of Market and New Montgomery (SF Assessor: 625–631 Market), named "Bank of America Building" in OSM; its back and east side are built against 33 New Montgomery.

**Deliverable:** `artifacts/bank-of-america-building/` (build script, GLB, validate/render wrappers, renders, REFERENCE.md, REPORT.md).

| | |
|---|---|
| Manifest id | `bank-of-america-building` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.4016814, 37.7886452` (OSM way 941649434 OBB centre, recentred by `tk.run`) |
| Target height | **60.1 m** — DataSF LiDAR roof (majority 60.11 m); no published height |
| Footprint | OSM way 941649434: OBB 30.9 x 16.9 m, 522 m², 4 nodes; Market face 16.9 m, New Montgomery face 30.9 m |
| Triangle cap | 5,000 (built: 1,424) |
| Category | `3` (office — `CAT.office` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Year / storeys | 1907 / 15 | published (SF Assessor, 625–631 Market, block 3707 lot 061) |
| OSM | name 'Bank of America Building', building:levels 14 | OSM |
| Roof | 60.1 m | measured (LiDAR ring 201006.0006825 majority; max 90 m is 33 New Montgomery) |
| Facade treatment | stone base, pale brick shaft, cornice | inferred (no photo retrieved) |

### Sources

- OSM way 941649434 — https://www.openstreetmap.org/way/941649434
- SF Assessor historical rolls — https://data.sf.gov/resource/wv5m-vpq2
- DataSF LiDAR ring 201006.0006825 — https://data.sf.gov/resource/ynuv-fyni

### Orientation

Local +X = bearing 135.6° (down New Montgomery). **Market = NW face (16.9 m)**, **New Montgomery = SW face (30.9 m)**; NE and SE faces abut 33 New Montgomery (on this batch list, another helper).

### What each side shows

- NW (Market) and SW (New Montgomery): shopfronts, mezzanine, punched windows, attic, cornice (inferred).
- NE / SE: blank (against 33 New Montgomery).

### Recognition cues (ranked)

1. Narrow corner tower on Market at New Montgomery.
2. Projecting cornice.
3. Pale brick grid.

### Massing recipe

- Stone base 0–9 m with glowing shopfronts; `tk.punched_block` shaft 9.8–53 m on street faces; attic 53.6–57.2 m; cornice 1.2 m proud; parapet to 60.1 m.

### Palette

`Toy_stone`, `Toy_sand`, `Toy_cream`, `Toy_glassd`, `Toy_roofd`, `Toy_steel`, trees; glow `Toy_sand_Glow`.

### Roof

Parapet, lift house, small plant.

### Triangle budget

1,424 tris (body 1,232, night_glow 192) against a cap of 5,000.

### Draft manifest entry

```json
{"id": "bank-of-america-building", "file": "bank-of-america-building.glb", "anchor": [-122.4016814, 37.7886452], "targetHeightM": 60.1, "cat": 3, "name": "625 Market Street (\"Bank of America Building\")", "estimated": false, "dims": [40.6249, 40.8323, 60.1], "tris": 1424, "loadRadius": 2500}
```

### Integration notes

Case B. Exclude this way only; 33 New Montgomery wraps it and is a separate landmark in this batch.

### Open risks

- Identity: OSM's name could not be confirmed against any source; the assessor gives 625–631 Market, 1907, 15 storeys.
- No photo: facade treatment is generic for the period.
- Low recognisability; consider whether it merits a landmark slot.
