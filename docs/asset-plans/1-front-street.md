# One Front Street — SF-SIM asset plan

A 38-storey office tower at Front and Market whose white aluminium spandrels run in continuous round-nosed bands between dark ribbon windows, wrapping a plan that steps down to Market Street in four saw-tooth notches — SOM's echo of Fahrenkamp's 1931 Shell-Haus in Berlin. In the miniature it is the white-and-black zebra tower on the Market corner.

**Deliverable:** `artifacts/1-front-street/` (Financial District batch, stages 1–2, BATCH mode).

| | |
|---|---|
| Manifest id | `1-front-street` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.3988578, 37.7917996` (OSM OBB centre via `tk.run`) |
| Target height | **164.0 m** — published roof 164 m (Wikipedia); LiDAR 158.06 m is the main roof, so the top 6 m is modelled as a white roof screen |
| Footprint | OSM way 148710877: OBB 54.6 × 43.6 m, 1945 m², long-axis bearing 171.2° |
| Triangle cap | 5,000 (tower ≥ 60 m; built: 4,518) |
| Category | `3` (Office — `CAT.office` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Roof height | 164 m | published (Wikipedia infobox) |
| Main roof | 158.06 m | measured (DataSF 2010 LiDAR) |
| Floors / year / architect | 38 / 1979 / SOM | published |
| Footprint | OBB 54.6 × 43.6 m, 1,945 m², 29 nodes | measured (OSM) |
| Saw-tooth Market frontage | 4 steps of ~6 × 4.5 m | measured (OSM outline) |
| Lobby height 8 m |  | estimated |

### Sources

- OSM way 148710877 — https://www.openstreetmap.org/way/148710877
- Wikipedia — https://en.wikipedia.org/wiki/One_Front_Street
- DataSF building footprints + 2010 LiDAR heights — https://data.sf.gov/resource/ynuv-fyni
- Commons photo (infobox) — https://commons.wikimedia.org/wiki/File:Shaklee_Terraces.jpg (looking up the stepped corner)

### Orientation

Street grid yaw: local +x = bearing 81.2°, +y = 351.2°; +Y = true north. West face = Front St; the SW chamfer = Front × Market corner; the four saw-tooth steps = Market St (SE); north and east faces are party walls toward the block.

### What each side shows

- SE (Market): the four saw-tooth steps, each a narrow banded 'column' — photographed.
- W (Front) and SW chamfer: the same white/dark banding — photographed in part.
- N and E: assumed to repeat the banding (**inferred**).

### Recognition cues (ranked)

1. Alternating white spandrel and dark ribbon-window bands, roughly half and half.
2. Saw-tooth stepped Market corner (reads from above and from Market).
3. Flat white-screened top.

### Massing recipe

- Plan: 13-node simplification of the OSM outline (rounding nodes < 1 m dropped).
- Lobby 0–8 m: inset `Toy_glassd` with white piers every 6 m and a lit ring.
- Tower 8–158 m: `Toy_white` prism (0.5 m bevel), 37 storeys of 4.05 m, one `Toy_glassd` ribbon per storey per face (panes 6.5 m with 0.35 m mullion gaps).
- Roof: white screen ring 158–164 m around a dark deck and plant cluster; crown light.

### Palette, roof, budget

- Palette: `Toy_white`, `Toy_glassd` (off-palette dark glass), `Toy_roofd`, `Toy_steel`, `Toy_stone`, trees; glow `Toy_sand_Glow`, `Toy_white_Glow`.
- Roof: A white parapet screen hides a dark deck with a tidy plant cluster; a white crown line outlines it at night.
- Budget: 4,518 triangles against the 5,000 cap (validated with `--budget 5000`).

### Draft manifest entry

```json
{"id": "1-front-street", "file": "1-front-street.glb", "anchor": [-122.3988578, 37.7917996], "targetHeightM": 164.0, "cat": 3, "name": "One Front Street", "estimated": false, "dims": [56.2188, 65.0635, 164.0], "tris": 4518, "loadRadius": 4920}
```

### Integration notes

Case B: registry entry in `pipeline/lib/landmarks.mjs`, exclusion of OSM way 148710877 from the
procedural bake, batch re-bake. 

### Open risks

- Published 164 m vs LiDAR 158 m: the 6 m difference is modelled as a roof screen; its exact form is not photographed.
- The rounded spandrel noses are flat in the model.
- N and E elevations not photographed.
