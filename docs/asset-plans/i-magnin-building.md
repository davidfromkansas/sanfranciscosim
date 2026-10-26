# I. Magnin & Co. Building — SF-SIM asset plan

I. Magnin's pre-Union Square store: an eight-storey block at Grant and Geary faced in white glazed terracotta, a tight grid of slender piers around very large dark multi-pane windows, a fine frieze and a flat cornice, with iron fire-escape balconies on Geary and a plainer taller white block rising behind. In the miniature it is the white gridded box on the Geary corner.

**Deliverable:** `artifacts/i-magnin-building/` (Financial District batch, stages 1–2, BATCH mode).

| | |
|---|---|
| Manifest id | `i-magnin-building` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.4047306, 37.7875148` (OSM OBB centre via `tk.run`) |
| Target height | **50.5 m** — LiDAR max 50.5 m = the rear block (DataSF 2010, parcel 0312008); main block parapet 44 m (OSM 43, LiDAR median 42.8, mode 47.3) |
| Footprint | OSM way 149335991: OBB 46.8 × 30.7 m, 1285 m², long-axis bearing 171° |
| Triangle cap | 3,000 (building < 60 m; built: 1,916) |
| Category | `3` (Office — `CAT.office` (former department store; assessor: commercial office) in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Store at 50 Grant Avenue | 1912–1948 | published (Wikipedia: I. Magnin) |
| Storeys / year | 10 / 1929 (assessor; main block 8 by photo and OSM levels) | published / inferred |
| Heights | median 42.8, mode 47.3, max 50.5 m | measured (DataSF LiDAR) |
| Footprint | OBB 46.8 × 30.7 m, 1,285 m² (lot 13,625 sq ft) | measured (OSM, assessor) |
| Rear block extent and height | ~11 × 16 m, 50.5 m | inferred (photo + LiDAR max) |

### Sources

- OSM way 149335991 — https://www.openstreetmap.org/way/149335991
- Wikipedia — https://en.wikipedia.org/wiki/I._Magnin
- DataSF building footprints + 2010 LiDAR heights — https://data.sf.gov/resource/ynuv-fyni
- DataSF assessor secured roll 2023 — https://data.sf.gov/resource/wv5m-vpq2
- OSM street centrelines via Nominatim (frontage check) — https://nominatim.openstreetmap.org/
- Commons photo — https://commons.wikimedia.org/wiki/File:I._Magnin_building,_50_Grant_Avenue_-_San_Francisco,_CA_-_DSC03327.jpg (Geary/Grant corner)

### Orientation

Street grid yaw: local +x = bearing 81°, +y = 351°. West face = Grant Avenue (46 m), north face = Geary Street (31 m); the SE corner is cut by lot lines; east and south are party walls.

### What each side shows

- W (Grant) and N (Geary): white pier grid, big windows, fire escapes on Geary — photographed.
- E and S: same grid without piers (**inferred**; mostly party walls).
- Rear block: plain white with smaller windows — photographed from afar; footprint inferred.

### Recognition cues (ranked)

1. Bright white terracotta box with a tight grid of very large dark windows.
2. Corner at Grant and Geary with fire-escape balconies on Geary.
3. Taller plain white block rising behind.

### Massing recipe

- 7-node OSM plan (local), yaw 9°.
- Shop floor 0–6.5 m `Toy_white` with lit display windows on the street faces.
- Body 6.5–42 m `Toy_white` punched block (seven 5.07 m storeys, 5.6 m bays) + slender piers on the street faces.
- Frieze, cornice, parapet to 44 m; six `Toy_ink` fire-escape balconies on Geary.
- Rear block (5-node plan) 43–50.5 m, punched windows, parapet.

### Palette, roof, budget

- Palette: `Toy_white`, `Toy_cream`, `Toy_glassd`, `Toy_ink`, `Toy_roofd`, `Toy_steel`; glow `Toy_sand_Glow`, `Toy_white_Glow`.
- Roof: Dark deck inside a white parapet with a plant cluster; the rear block carries its own parapet; white crown line.
- Budget: 1,916 triangles against the 3,000 cap (validated with `--budget 3000`).

### Draft manifest entry

```json
{"id": "i-magnin-building", "file": "i-magnin-building.glb", "anchor": [-122.4047306, 37.7875148], "targetHeightM": 50.5, "cat": 3, "name": "I. Magnin & Co. Building", "estimated": false, "dims": [39.6817, 56.519, 50.5], "tris": 1916, "loadRadius": 2500}
```

### Integration notes

Case B: registry entry in `pipeline/lib/landmarks.mjs`, exclusion of OSM way 149335991 from the
procedural bake, batch re-bake. 

### Open risks

- The rear block's extent and height are inferred (photo + LiDAR max); it may be lower or larger.
- Main parapet 44 m sits between OSM 43 m and the LiDAR mode 47.3 m.
- Category: office chosen from the assessor use; retail (4) is defensible for the shops below.
