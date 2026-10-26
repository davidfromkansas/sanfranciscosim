# 33 New Montgomery — SF-SIM asset plan

A 20-storey office tower on an L-shaped lot at New Montgomery and Stevenson, just off Market beside the Palace Hotel. No Wikipedia article or retrievable photo exists, so this is the least certain model of the batch: footprint and roof heights are measured (OSM, DataSF LiDAR), while the skin and the position of the taller roof element are inferred. In the miniature it fills the gap between Market Street and 140 New Montgomery with a plausible granite block.

**Deliverable:** `artifacts/33-new-montgomery-street/` (FiDi batch, stages 1–2; approval, optimize and integration by the lead).

| | |
|---|---|
| Manifest id | `33-new-montgomery-street` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.4014689, 37.7886469` (from `tk.run`, OSM OBB centre + recentre shift) |
| Target height | **101.8 m** — DataSF 2010 LiDAR max 101.80 m (measured crest); main roof 80 m = LiDAR majority 79.98 m and OSM height=80 (20 levels). No published height found |
| Footprint | OSM way 79377223: 9 nodes, 1,293 m², L-shaped, OBB 51 × 38.3 m, bearing 45.8°; used as-is |
| Triangle cap | 5,000 (built: 3,450) |
| Category | `3` (Office — `CAT.office` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Crest | 101.8 m | measured (LiDAR max) |
| Main roof | 80.0 m | measured (LiDAR majority 79.98 m; OSM height=80, 20 levels) |
| Upper-percentile LiDAR | ≈91 m (facts file lidarH 90.97) | measured: a minority of the roof is well above 80 m |
| Footprint | L, 1,293 m², bearing 45.8° | measured (OSM) |
| Taller element: 12 × 12 m at the L's outer (east) corner |  | inferred — position and size guessed |
| Skin: granite with punched windows |  | estimated (no photo) |

### Sources

- OSM way 79377223 — https://www.openstreetmap.org/way/79377223
- DataSF footprints / 2010 LiDAR (record SF3707062) — https://data.sf.gov/resource/ynuv-fyni
- No Wikipedia article; no Commons photo retrieved (HTTP 429 throughout the batch)

### Orientation

Footprint used directly; long axis bearing 45.8°. The NE arm runs along New Montgomery (inferred); the SE arm runs back along Stevenson (inferred). +Y = true north.

### What each side shows

- All faces: granite with punched windows over a glazed base (**inferred**, no photo).
- Taller corner element at the L's outer east corner (**inferred** from LiDAR statistics only).

### Recognition cues (ranked)

1. L-shaped 20-storey granite block next to the Palace Hotel.
2. A taller element rising above the 80 m roof.

### Massing recipe

- Plan = OSM polygon.
- 0–7 m granite base with glazed shopfronts; band to 7.8 m.
- 7.8–80 m `punched_block` in `Toy_granite`, 18 storeys of 4 m, panes every 3.6 m; parapet; plant.
- 12 × 12 m corner element 80–98.8 m (5 storeys) with a stone cap to 101.8 m and a white light line.

### Palette

`Toy_granite`, `Toy_stone`, `Toy_glassd`, `Toy_roofd`, `Toy_steel`; glow `Toy_sand_Glow`, `Toy_white_Glow`. Off-palette: `granite`, `glassd`.

### Roof

Parapet round a dark deck with a two-box plant cluster; the taller corner element has its own capped roof.

### Triangle budget

3,450 tris (body 2,766, night glow 684) against a 5,000 cap.

### Draft manifest entry

```json
{"id": "33-new-montgomery-street", "file": "33-new-montgomery-street.glb", "anchor": [-122.4014689, 37.7886469], "targetHeightM": 101.8, "cat": 3, "name": "33 New Montgomery", "estimated": true, "dims": [55.2705, 71.5069, 101.8], "tris": 3450, "loadRadius": 3054}
```

### Integration notes

Case B but **flag for review**: `estimated: true` in the draft entry. Tight lot between Market St buildings and the Palace Hotel; clear only this footprint (~32 m radius at the arm ends) and check the Palace Hotel survives. loadRadius 3,054 m.

### Open risks

- **No photo and no published data**: materials, window pattern and the taller element are guesses.
- The LiDAR max (101.8 m) may be a neighbour's edge, a mast or a crown; if David has a photo, the corner element should be checked first.
- Consider dropping this building from the batch if a photo shows it is a plain 80 m block (then crest = 80 m).
