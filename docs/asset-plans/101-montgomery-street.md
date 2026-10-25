# 101 Montgomery (Schwab Building) — SF-SIM asset plan

A 28-storey 1984 office slab on Montgomery Street at Sutter, former Charles Schwab headquarters: a thin north–south blade of pale cream stone whose long faces ripple with rows of curved bay windows. In the miniature it is a slim cream blade between darker towers.

**Deliverable:** `artifacts/101-montgomery-street/` (FiDi batch, stages 1–2; approval, optimize and integration by the lead).

| | |
|---|---|
| Manifest id | `101-montgomery-street` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.4024908, 37.7903643` (from `tk.run`, OSM OBB centre + recentre shift) |
| Target height | **123.1 m** — published roof 404 ft (Wikipedia); DataSF LiDAR crest 124.67 m, majority plane 120.75 m |
| Footprint | OSM way 132125159: OBB 64.4 × 17.1 m, 1,092 m², 7 nodes, long axis bearing 170.9°; used as-is |
| Triangle cap | 5,000 (built: 3,956) |
| Category | `3` (Office — `CAT.office` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Roof / crest | 123.1 m (404 ft) | published (Wikipedia) |
| LiDAR | max 124.67 m, majority 120.75 m | measured (DataSF 2010) |
| Floors / year | 28 / 1984 | published |
| Footprint | 64.4 × 17.1 m, bearing 170.9° | measured (OSM) |
| Lobby ~8 m colonnade; crown wall from 119 m |  | inferred (photo) / estimated |

### Sources

- OSM way 132125159 — https://www.openstreetmap.org/way/132125159
- Wikipedia — https://en.wikipedia.org/wiki/101_Montgomery
- Commons photo — https://commons.wikimedia.org/wiki/File:101_Montgomery_Street.jpg (May 2021)
- DataSF footprints / 2010 LiDAR — https://data.sf.gov/resource/ynuv-fyni

### Orientation

Footprint used directly (+X east, +Y north); long axis bearing 170.9° (N–S along Montgomery). East face = Montgomery St (long), north/south ends narrow; west face toward the block interior.

### What each side shows

- East (Montgomery) and west: the long rippling faces, cream stone with curved bay windows (photo shows the street face).
- North and south: narrow ends, same grid; the north end steps against older neighbours (**inferred**).
- Ground: a colonnade of square cream piers in front of dark glass (photo).

### Recognition cues (ranked)

1. A very thin, tall cream slab — the blade silhouette.
2. Fine regular window grid in pale stone.
3. Colonnaded base on Montgomery.
4. Plain flat top behind a cream crown wall.

### Massing recipe

- Plan = OSM polygon (`tk.ccw(PTS)`).
- 0–8 m dark glass lobby set 1.5 m back, cream piers every 6.4 m, cream soffit band to 9.2 m.
- 9.2–119 m `tk.shaft`: 27 storeys, `Toy_glassd` with 1.9 m `Toy_cream` sills and cream fins every 3.2 m; lit panes aligned to the fin bays.
- 119–123.1 m set-back cream crown wall with white cap, roof deck and plant inside, white light line.

### Palette

`Toy_cream`, `Toy_white`, `Toy_glassd`, `Toy_roofd`, `Toy_steel`, `Toy_stone`; glow `Toy_sand_Glow`, `Toy_white_Glow`. All core palette except `glassd`.

### Roof

A cream crown wall hides a dark deck with a row of plant boxes; white light line at night.

### Triangle budget

3,956 tris (body 3,134, night glow 822) against a 5,000 cap.

### Draft manifest entry

```json
{"id": "101-montgomery-street", "file": "101-montgomery-street.glb", "anchor": [-122.4024908, 37.7903643], "targetHeightM": 123.1, "cat": 3, "name": "101 Montgomery (Schwab Building)", "estimated": false, "dims": [33.7451, 72.9064, 123.1], "tris": 3956, "loadRadius": 3693}
```

### Integration notes

Case B. Thin slab on a tight lot: keep the exclusion to this footprint (~20 m radius from the centre clears the slab ends; check the 1908 brick neighbour at the north end survives). loadRadius 3,693 m.

### Open risks

- The undulating curved bay windows are not modelled (a wavy loft would cost ~30k tris); they read only as a fine grid.
- The rounded top shoulders seen in the photo are simplified to a flat crown wall.
- Lobby height estimated.
