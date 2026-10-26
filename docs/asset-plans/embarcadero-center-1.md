# One Embarcadero Center — SF-SIM asset plan

John Portman's 1971 first and westernmost Embarcadero Center tower, between Sacramento, Battery, Clay and Front: a 45-storey pale precast slab whose narrow ends break into staggered vertical fins, with a fine even grid of dark punched windows and a glazed band just under its flat roof.

**Deliverable:** `artifacts/embarcadero-center-1/` (FiDi batch, ADDRESS-TO-ASSET stages 1–2, BATCH mode).

| | |
|---|---|
| Manifest id | `embarcadero-center-1` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.3996222, 37.7944829` (OSM OBB centre, bbox-recentred by `tk.run`) |
| Target height | **173.4 m** — 173.4 m roof (Wikipedia/CTBUH 569 ft, published; antenna spire 187 m not modelled; LiDAR 167.9, OSM 173) |
| Footprint | OSM way 32612608: OBB 75.2 x 32.8 m, 1889 m², bearing 81.2° |
| Triangle cap | 5,000 (FiDi batch, tower ≥ 60 m); built 4,696 |
| Category | `3` (office, `CAT.office` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Roof height | 173.4 m (569 ft) | published (Wikipedia) |
| Antenna | 187 m (614 ft) | published — not modelled |
| Floors / year / architect | 45 / 1971 / John Portman & Associates | published |
| LiDAR | 167.9 m | measured (DataSF 2010) |
| Footprint | OBB 75.2 x 32.8 m, 1,889 m², staggered ends | measured (OSM way 32612608) |
| Glazed band ~160 m |  | estimated from the photo |

### Sources

- https://en.wikipedia.org/wiki/One_Embarcadero_Center
- https://en.wikipedia.org/wiki/Embarcadero_Center
- https://commons.wikimedia.org/wiki/File:Embarcadero_Center_1.jpg
- https://www.openstreetmap.org/way/32612608
- https://data.sf.gov/resource/ynuv-fyni (2010 LiDAR building heights)

### Orientation

Long axis bearing 81.2 (FiDi grid). Long faces N (Clay) and S (Sacramento); stepped ends E and W. Plan built from six N–S strips measured off OSM (as for artifacts/4-embarcadero-center). +Y = true north.

### What each side shows

- N and S: dense grid of dark punched windows in pale precast (photo).
- E and W ends: staggered fins (OSM plan; photo shows the cliff face).

### Recognition cues (ranked)

1. Tall pale slab with a fine window grid.
2. Sawtooth ends.
3. Glazed band under the flat roof.
4. Family resemblance to 4 Embarcadero Center.

### Massing recipe

- Base 0–12 m on the footprint +0.8 m: stone with glazed rows (the shared podium and bridges are separate OSM buildings and are not modelled).
- Slab 12–172.2 m: bronze window columns + per-storey sand spandrels; glassl band 159–161.6 m.
- Cream parapet to 173.4 m, steel deck, four cooling towers, cream penthouse, glassl crown light.

### Palette

Toy_sand, Toy_cream, Toy_bronze (off-palette), Toy_glassl, Toy_glassd (off-palette), Toy_stone, Toy_steel, Toy_ink; glow Toy_sand_Glow, Toy_glassl_Glow.

### Roof

Steel deck with four circular cooling towers and a penthouse box (positions inferred, after 4 Embarcadero Center).

### Triangle budget

4,696 tris (cap 5,000). Facades are flat outward quads over solid prisms (window columns, per-storey spandrels, ribbons); night lights are hashed quads aligned with the window bays.

### Draft manifest entry

```json
{
  "id": "embarcadero-center-1",
  "file": "embarcadero-center-1.glb",
  "anchor": [-122.3996222, 37.7944829],
  "targetHeightM": 173.4,
  "cat": 3,
  "name": "One Embarcadero Center",
  "estimated": false,
  "dims": [84.9689, 45.1028, 173.4],
  "tris": 4696,
  "loadRadius": 5202
}
```

### Integration notes

Case B: registry entry, exclusion of OSM way 32612608 (and its building:parts) from the procedural bake, re-bake. `dims` is the world-axis bbox including the apron. loadRadius = max(2500, 30 x 173.4) = 5202.

### Open risks

- Unlike 4 EC, no stepped tops at the ends were modelled: the photo shows a flat top; confirm.
- Roof plant layout inferred.
- Antenna omitted.
