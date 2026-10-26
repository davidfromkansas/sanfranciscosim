# 180 Montgomery Street (Bank of the West Building) — SF-SIM asset plan

**Batch slug `180-montgomery-street` is mis-named:** the OSM footprint (way 132125163, no address tags) is 180 Montgomery Street, the Bank of the West Building (Booth Architects / Fee Munson Ebert, 1979, 25 storeys). DataSF assessor parcel 0289009 and the Wikipedia/CTBUH coordinates both fall on it. A plain beige precast-concrete box with deep horizontal ribbon windows between thick spandrels, a few broad piers per face and solid corners, at Montgomery × Bush.

**Deliverable:** `artifacts/180-montgomery-street/` (Financial District batch, stages 1–2, BATCH mode).

| | |
|---|---|
| Manifest id | `180-montgomery-street` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.4020113, 37.7907470` (OSM OBB centre via `tk.run`) |
| Target height | **109.8 m** — published 109.8 m (CTBUH via the Wikipedia list; LiDAR roof majority 109.5 m, median 104.2 m) |
| Footprint | OSM way 132125163: OBB 37.7 × 41.2 m, 1,511 m², long-axis bearing 171.1° |
| Triangle cap | 5,000 (tower ≥ 60 m; built: 2,848) |
| Category | `3` (Office — `CAT.office` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Height | 109.8 m (CTBUH); Wikipedia infobox gives 98 m roof | published |
| LiDAR | median 104.2 m, majority 109.5 m, peak 114.5 m | measured (DataSF 201006.0002311, MBLR SF0289009) |
| Floors / year | 25 / 1979 (assessor: 25 storeys, 1978) | published |
| Main roof 104.2 m, set-back plant penthouse to 109.8 m |  | measured + inferred |
| Address | 180 Montgomery, not 268 Bush (no 268 Bush parcel exists on this block) | verified (assessor) |

### Sources

- OSM way 132125163 — https://www.openstreetmap.org/way/132125163
- Wikipedia, 180 Montgomery Street — https://en.wikipedia.org/wiki/180_Montgomery_Street
- Wikipedia tallest list (row 78) / CTBUH — https://www.skyscrapercenter.com/building/180-montgomery-street/39286
- DataSF assessor roll (parcel 0289009) — https://data.sf.gov/resource/wv5m-vpq2.json
- DataSF 2010 LiDAR footprints — https://data.sf.gov/resource/ynuv-fyni
- Commons photo — https://commons.wikimedia.org/wiki/File:180_Montgomery_St,_San_Francisco_(full_height).jpg

### Orientation

Street grid, u = bearing 81°, v = 351°. Montgomery St = W face, Bush St = N face. Small notch at the NE corner (OSM).

### What each side shows

- W and N street faces: beige spandrels, dark ribbon glass, broad piers — photographed (from Montgomery).
- S and E: same skin assumed — inferred. Lobby treatment inferred.

### Recognition cues (ranked)

1. Strongly horizontal sandy precast grid.
2. Broad piers dividing each face into ~5 bays, solid corners.
3. Plain flat top with a set-back penthouse.

### Massing recipe

- Lobby 0–6 m: recessed `Toy_glassd` behind concrete piers at 7.6 m, lit ring.
- Shaft 6.4–104.2 m: `tk.shaft` 24 storeys of 4.08 m, `Toy_glassd` with 2.1 m `Toy_concrete` spandrels 0.45 m proud, piers 1.1 m at 7.6 m.
- Roof: concrete cap, dark deck, 22 × 16 m concrete penthouse with louvres to 109.8 m, plant.

### Palette, roof, budget

- Palette: `Toy_concrete` (off-palette, documented in the kit), `Toy_glassd`, `Toy_roofd`, `Toy_steel`, `Toy_stone`; glow `Toy_sand_Glow`, `Toy_white_Glow`.
- Roof: Concrete cap, dark deck, louvred penthouse and a small plant group; crown line at night.
- Budget: 2,848 triangles against the 5,000 cap (validated with `--budget 5000`).

### Draft manifest entry

```json
{"id": "180-montgomery-street", "file": "180-montgomery-street.glb", "anchor": [-122.4020113, 37.790747], "targetHeightM": 109.8, "cat": 3, "name": "180 Montgomery Street (Bank of the West Building)", "estimated": false, "dims": [53.325, 49.3411, 109.8], "tris": 2848, "loadRadius": 3294}
```

### Integration notes

Case B: registry entry in `pipeline/lib/landmarks.mjs`, exclusion of OSM way 132125163 from the procedural bake, batch re-bake. Consider renaming the id to `180-montgomery-street`.

### Open risks

- Slug/name mismatch: the lead should rename the manifest id (e.g. `180-montgomery-street`) or keep the slug with the corrected name.
- Penthouse size and position inferred; 109.8 m vs 98 m sources disagree (LiDAR supports ~109.5 m).
- Lobby height and piers inferred.
