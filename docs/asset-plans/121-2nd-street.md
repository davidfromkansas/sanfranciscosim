# The Rapp Building — SF-SIM asset plan

A 1907 seven-storey Chicago-school commercial loft at 121 Second Street, a contributor to the Second and Howard Streets historic district, its name carved over the entrance. Pale grey-cream front of four bays of paired windows between plain piers, a darker two-storey base, keystoned sixth-floor window heads and a deep bracketed cornice, beside the 101 Second Street tower.

**Deliverable:** `artifacts/121-2nd-street/` (Financial District batch, stages 1–2, BATCH mode).

| | |
|---|---|
| Manifest id | `121-2nd-street` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.3992003, 37.7878349` (OSM OBB centre via `tk.run`) |
| Target height | **27.5 m** — measured: DataSF LiDAR median roof 27.46 m (majority 27.37 m); OSM height 27. The list's 99 m was the 101 Second Street tower's LiDAR |
| Footprint | OSM way 80296751: OBB 18.9 × 22.5 m, 414 m², long-axis bearing 135.2° |
| Triangle cap | 3,000 (building < 60 m; built: 598) |
| Category | `3` (Office — `CAT.office` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Year / storeys | 1907 / 7 (assessor parcel 3721071) | published (DataSF assessor) |
| Roof | 27.46 m median, 50.1 m peak (neighbour) | measured (DataSF 201006.0007591) |
| Footprint | OBB 18.9 × 22.5 m, 414 m², bearing 135° | measured (OSM way 80296751) |
| Four bays of paired windows, deep cornice |  | photographed |

### Sources

- OSM way 80296751 — https://www.openstreetmap.org/way/80296751
- DataSF assessor roll — https://data.sf.gov/resource/wv5m-vpq2.json
- DataSF 2010 LiDAR footprints — https://data.sf.gov/resource/ynuv-fyni
- Commons photo — https://commons.wikimedia.org/wiki/File:Rapp_Building,_121_Second_St.,_Second_and_Howard_Streets_District,_San_Francisco,_CA_9-3-2012_5-42-43_PM.JPG

### Orientation

SoMa grid, u = bearing 45° (NE), v = 315° (NW). 2nd Street front = SW face (−u); NW side abuts 101 Second Street, SE side a 4-storey neighbour.

### What each side shows

- SW (2nd St): photographed — base, four bays, cornice.
- NE rear: plain punched windows — inferred. NW/SE: blank party walls — inferred.

### Recognition cues (ranked)

1. Cream loft front with four bays and paired windows.
2. Deep bracketed cornice.
3. Darker two-storey base.

### Massing recipe

- OSM 4-node plan. Base 0–8.2 m `Toy_concrete` with two rows of shop panes; cream belt.
- Upper 8.6–25 m: `tk.punched_block` five storeys of 3.28 m, paired windows (2.3 m) on the front, three proud piers at the bay joints, sill band.
- Cornice 25–26.6 m (1.1 m projection), parapet to 27.5 m, dark deck, small plant.

### Palette, roof, budget

- Palette: `Toy_cream`, `Toy_concrete` (off-palette), `Toy_glassd`, `Toy_roofd`, `Toy_steel`, `Toy_stone`; glow `Toy_sand_Glow`.
- Roof: Dark deck behind a cream parapet with one low plant box.
- Budget: 598 triangles against the 3,000 cap (validated with `--budget 3000`).

### Draft manifest entry

```json
{"id": "121-2nd-street", "file": "121-2nd-street.glb", "anchor": [-122.3992003, 37.7878349], "targetHeightM": 27.5, "cat": 3, "name": "The Rapp Building", "estimated": false, "dims": [36.2117, 35.4245, 27.5], "tris": 598, "loadRadius": 2500}
```

### Integration notes

Case B: registry entry in `pipeline/lib/landmarks.mjs`, exclusion of OSM way 80296751 from the procedural bake, batch re-bake.

### Open risks

- Notability is modest (district contributor, not an individual landmark).
- Rear and side treatment inferred.
