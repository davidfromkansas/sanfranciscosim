# Union Trust Bank Building (2 Grant Avenue) — SF-SIM asset plan

A granite neoclassical banking temple at Market, Grant and O'Farrell (1910; now a Wells Fargo branch, OSM historic=building): two very tall storeys behind a giant colonnade on Grant that wraps the rounded Market corner, under a heavy entablature and plain attic.

**Deliverable:** `artifacts/2-grant-avenue/` (build script, GLB, validate/render wrappers, renders, REFERENCE.md, REPORT.md).

| | |
|---|---|
| Manifest id | `2-grant-avenue` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.4046839, 37.7871305` (OSM way 149335980 OBB centre, recentred by `tk.run`) |
| Target height | **19.5 m** — DataSF LiDAR roof (majority 19.51 m; OSM 20 m) |
| Footprint | OSM way 149335980: 10 nodes, OBB 37.5 x 23 m, 713 m², rounded SE corner on Market |
| Triangle cap | 3,000 (built: 1,126) |
| Category | `4` (retail — `CAT.retail` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Year / storeys | 1910 / 3 (assessor) | published (SF Assessor, 744 Market, block 0312 lot 006) |
| Roof | 19.5 m | measured (LiDAR ring 201006.0004280 majority) |
| Footprint | 10 nodes, rounded corner | measured (OSM) |
| Colonnade, skylit hall |  | inferred (no photo retrieved) |

### Sources

- OSM way 149335980 — https://www.openstreetmap.org/way/149335980
- SF Assessor historical rolls — https://data.sf.gov/resource/wv5m-vpq2
- DataSF LiDAR ring 201006.0004280 — https://data.sf.gov/resource/ynuv-fyni

### Orientation

Local +X = bearing 80.8° (east). **Grant = W face (36.5 m)**, **O'Farrell = S face (8 m)**, the **rounded corner faces SE onto Market**; N and E are party walls.

### What each side shows

- W, S and the rounded SE corner: colonnade and tall windows (inferred).
- N and E: blank party walls.

### Recognition cues (ranked)

1. White colonnade wrapping a rounded corner.
2. Heavy entablature.
3. Low temple bulk among towers.
4. Skylit hall.

### Massing recipe

- Stone hall prism on steps; tall windows between columns (glowing).
- White columns (8-sided) 1.3 m proud at every window pier, with capitals; entablature 2.1 m proud; attic band.
- Skylight with an upward `sand_Glow` cap.

### Palette

`Toy_stone`, `Toy_white`, `Toy_glassd`, `Toy_glassl`, `Toy_roofd`; glow `Toy_sand_Glow`.

### Roof

Dark deck inside the attic with a skylight over the banking hall.

### Triangle budget

1,126 tris (body 1,098, night_glow 28) against a cap of 3,000.

### Draft manifest entry

```json
{"id": "2-grant-avenue", "file": "2-grant-avenue.glb", "anchor": [-122.4046839, 37.7871305], "targetHeightM": 19.5, "cat": 4, "name": "Union Trust Bank Building (2 Grant Avenue)", "estimated": false, "dims": [35.6519, 46.5038, 19.5], "tris": 1126, "loadRadius": 2500}
```

### Integration notes

Case B. Exclusion radius ≈ 20 m; the entablature overhangs the party walls by ~2 m (trim at bake time if it clips a neighbour).

### Open risks

- No photo retrieved: column order, count and the rounded-corner treatment are inferred.
- Category: a bank branch, filed as retail (CAT has no bank).
