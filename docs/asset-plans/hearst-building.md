# Hearst Building — SF-SIM asset plan

The San Francisco Examiner's 13-storey office block at Market, Kearny and Third (1909, rebuilt after the 1906 fire; entrance remodelled by Julia Morgan, 1937): a pale terracotta frontage on three faces of the five-way intersection, a stone base of tall arches, an arcaded top storey and a deep cornice.

**Deliverable:** `artifacts/hearst-building/` (build script, GLB, validate/render wrappers, renders, REFERENCE.md, REPORT.md).

| | |
|---|---|
| Manifest id | `hearst-building` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.4030128, 37.7874579` (OSM way 132127809 OBB centre, recentred by `tk.run`) |
| Target height | **50.2 m** — DataSF LiDAR roof (majority 50.19 m; OSM 49 m); no published height found |
| Footprint | OSM way 132127809: 17 nodes, OBB 31.1 x 48.5 m, 928 m², with two light courts open to the east party wall |
| Triangle cap | 3,000 (built: 2,998) |
| Category | `3` (office — `CAT.office` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Storeys / year | 13 / 1909 | published (SF Assessor roll, 691–699 Market, block 3707 lot 057) |
| Roof | 50.2 m | measured (DataSF LiDAR ring 201006.0002397 majority; max 67.7 m is a neighbour) |
| Footprint | 17-node outline, 928 m² | measured (OSM) |
| Facade treatment | base arches, terracotta shaft, arcaded attic, cornice | inferred (no photo retrieved) |

### Sources

- OSM way 132127809 — https://www.openstreetmap.org/way/132127809
- SF Assessor historical rolls — https://data.sf.gov/resource/wv5m-vpq2
- DataSF LiDAR ring 201006.0002397 — https://data.sf.gov/resource/ynuv-fyni

### Orientation

Local +X = bearing 45.6° (NE along Market). **Market = NW face (19 m)**, a **23 m corner face looking W** onto the Kearny/Third junction, **Third = SW face**; the E side (two light courts) and Stevenson side are party/rear walls.

### What each side shows

- NW, W, SW street fronts: arched stone base, punched terracotta shaft, arcaded attic (inferred treatment).
- Rear (Stevenson side) and light-court walls: punched windows too; the east party walls are blank.

### Recognition cues (ranked)

1. Three-sided frontage on the Market/Kearny/Third corner.
2. Deep cornice and arcaded top.
3. Tall arched base.
4. Pale terracotta.

### Massing recipe

- Prism on the true footprint; stone base 0–8 m with arches on the fronts; `tk.punched_block` shaft 8.9–40.5 m on all but the party walls.
- Attic band, arched attic 41–46.6 m, cornice 1.2 m proud, parapet to 50.2 m, lift house and plant.

### Palette

`Toy_stone`, `Toy_cream`, `Toy_terracotta`, `Toy_glassd`, `Toy_roofd`, `Toy_steel`, trees; glow `Toy_sand_Glow`.

### Roof

Parapet, lift house on the corner wing, plant over the rear wing; the light courts read from the aerial.

### Triangle budget

2,998 tris (body 2,614, night_glow 384) against a cap of 3,000.

### Draft manifest entry

```json
{"id": "hearst-building", "file": "hearst-building.glb", "anchor": [-122.4030128, 37.7874579], "targetHeightM": 50.2, "cat": 3, "name": "Hearst Building", "estimated": false, "dims": [53.1946, 53.3389, 50.2], "tris": 2998, "loadRadius": 2500}
```

### Integration notes

Case B. Exclude this way only; Monadnock and other Market frontage neighbours are separate.

### Open risks

- No photo or description could be retrieved (Wikipedia/Commons rate-limited); facade detail is inferred from the type.
- Height from LiDAR, not published.
