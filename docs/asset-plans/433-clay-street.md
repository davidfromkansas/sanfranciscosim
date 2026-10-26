# The Jay (former Le Méridien San Francisco) — SF-SIM asset plan

A 25-storey grey concrete hotel slab along Clay Street. A flat-faced central spine rises highest; either side the room wings fold into a saw-tooth of pointed bays, every room with a balcony, and the wings step down bay by bay so the top reads as a terraced staircase. In the miniature it is the pleated grey slab with stepped shoulders north of the Transamerica block.

**Deliverable:** `artifacts/433-clay-street/` (Financial District batch, stages 1–2, BATCH mode).

| | |
|---|---|
| Manifest id | `433-clay-street` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.4008922, 37.7946815` (OSM OBB centre via `tk.run`) |
| Target height | **81.0 m** — 81 m = OSM height and LiDAR mode 81.0 m (DataSF 2010, parcel 0229020; median 76.6, max 83.2) |
| Footprint | OSM way 35182441: OBB 30.3 × 84 m, 2361 m², long-axis bearing 170.8° |
| Triangle cap | 5,000 (tower ≥ 60 m; built: 3,006) |
| Category | `7` (Hotel — `CAT.hotel` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Opened / storeys | 1989 / 25 (assessor, hotel) | published (assessor roll) |
| Rooms | 360 | published (OSM tags) |
| Heights | median 76.6, mode 81.0, max 83.2 m | measured (DataSF LiDAR) |
| Site footprint | OBB 84 × 30.3 m, 2,361 m² | measured (OSM) |
| Slab 60 × 19 m + 1.9 m bays, 10 m podium, step pattern |  | inferred (photo) / estimated |

### Sources

- OSM way 35182441 — https://www.openstreetmap.org/way/35182441
- DataSF building footprints + 2010 LiDAR heights — https://data.sf.gov/resource/ynuv-fyni
- DataSF assessor secured roll 2023 — https://data.sf.gov/resource/wv5m-vpq2
- OSM street centrelines via Nominatim (frontage check) — https://nominatim.openstreetmap.org/
- Commons photo — https://commons.wikimedia.org/wiki/File:Le_Méridien_San_Francisco.jpg (looking up at a wing and the spine)

### Orientation

Street grid yaw: local +x = bearing 80.8° (east), +y = 350.8°. North face = Clay St (long side), east end = Battery St.

### What each side shows

- Long faces (N, S): saw-tooth balcony bays stepping down toward the ends — photographed (one wing).
- Central spine: flat concrete with vertical strips — photographed.
- Ends, podium and the other wing: **inferred** by symmetry.

### Recognition cues (ranked)

1. Pleated (saw-tooth) balconied wings in grey concrete.
2. Stepped, terraced top falling away from a taller spine.
3. Long slab along Clay.

### Massing recipe

- Podium: site polygon to 10 m, glazed and lit ground storey.
- Spine 16 × 20 m to 79.8 m with six vertical steel strips, parapet to 81 m, low plant.
- Each wing: four 5.5 m bays with pointed plans (1.9 m tooth), tops 78/75/72/69 m.
- Per storey (3 m) a dark glazed recess above a solid balcony band on the angled faces; 22% lit.

### Palette, roof, budget

- Palette: `Toy_concrete`, `Toy_steel`, `Toy_glassd`, `Toy_roofd`; glow `Toy_sand_Glow`, `Toy_white_Glow`.
- Roof: Each stepped bay has a dark deck; the spine carries a parapet, a low plant cluster and a white crown line.
- Budget: 3,006 triangles against the 5,000 cap (validated with `--budget 5000`).

### Draft manifest entry

```json
{"id": "433-clay-street", "file": "433-clay-street.glb", "anchor": [-122.4008922, 37.7946815], "targetHeightM": 81.0, "cat": 7, "name": "The Jay (former Le M\u00e9ridien San Francisco)", "estimated": false, "dims": [92.2273, 45.2796, 81.0], "tris": 3006, "loadRadius": 2500}
```

### Integration notes

Case B: registry entry in `pipeline/lib/landmarks.mjs`, exclusion of OSM way 35182441 from the
procedural bake, batch re-bake. 

### Open risks

- Slab length, depth and podium height are estimates; the photo shows only one wing and the spine.
- Step heights (one storey per bay) read from the photo.
- Balconies are a graphic band, not projecting slabs.
