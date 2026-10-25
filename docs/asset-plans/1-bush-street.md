# Crown Zellerbach Building (One Bush Plaza) — SF-SIM asset plan

San Francisco's first International Style tower (SOM with Hertzka & Knowles, 1959) at Bush, Battery and Market: a 20-storey slab of green-tinted glass in a fine aluminium mullion grid, lifted on dark granite columns over a recessed lobby, with its elevator and service core pulled out into a separate solid tower. A city landmark (SFDL 183). In the miniature it is the pure glass slab on stilts with a solid tower clipped to its side.

**Deliverable:** `artifacts/1-bush-street/` (FiDi batch, stages 1–2; approval, optimize and integration by the lead).

| | |
|---|---|
| Manifest id | `1-bush-street` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.4000600, 37.7909563` (from `tk.run`, OSM OBB centre + recentre shift) |
| Target height | **93.9 m** — published roof 308 ft = 93.9 m (Wikipedia) = core-tower crest; DataSF LiDAR max 93.78 m; slab roof 86.7 m = LiDAR majority plane (measured) |
| Footprint | OSM way 93817367: 14 nodes, 1,745 m², bearing 80.8° — slab 64 × 22 m plus the core tower (≈23 × 14 m) on its south side; used as-is |
| Triangle cap | 5,000 (built: 3,618) |
| Category | `3` (Office — `CAT.office` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Crest (core tower) | 93.9 m (308 ft) | published; LiDAR max 93.78 m |
| Slab roof | 86.7 m | measured (LiDAR majority plane 86.68 m) |
| Floors / year / architects | 20 / 1959 / SOM, Hertzka & Knowles | published |
| Footprint | slab ≈ 64 × 22 m + core ≈ 23 × 14 m, bearing 80.8° | measured (OSM) |
| Lobby / stilts ≈ 7.6 m |  | inferred (photo) |
| Core cladding colour (pale green mosaic) |  | inferred / estimated |

### Sources

- OSM way 93817367 — https://www.openstreetmap.org/way/93817367
- Wikipedia — https://en.wikipedia.org/wiki/One_Bush_Plaza
- Commons photo — https://commons.wikimedia.org/wiki/File:One_Bush_Plaza.jpg (2021, from Bush × Sansome)
- DataSF footprints / 2010 LiDAR — https://data.sf.gov/resource/ynuv-fyni

### Orientation

Footprint used directly; slab long axis bearing 80.8°. North face = Bush St (the building famously faces Bush, not Market); the core tower projects from the south face toward Market; west end toward Sansome, east end toward Battery.

### What each side shows

- North (Bush) and east/west ends: glass curtain wall on dark granite stilts (photo from Bush × Sansome).
- South: the solid core tower against the slab; the plaza toward Market (**inferred** from OSM).
- The low circular former bank pavilion on the plaza is a separate building and is not modelled.

### Recognition cues (ranked)

1. Pure green glass slab with a fine vertical mullion grid.
2. Lifted on dark columns over a recessed glass lobby.
3. Separate solid core tower rising a storey-and-a-half above the slab.
4. Granite plaza toward Market.

### Massing recipe

- Slab = OSM nodes 0, 1, 12, 13; core = nodes 3–10.
- 0–7.6 m `Toy_glassd` lobby set 3 m in, `Toy_ink` columns every ~6.9 m, dark soffit.
- 8–85.5 m `tk.shaft`: 19 storeys of `Toy_teal` glass, thin `Toy_glassd` spandrel lines, `Toy_steel` mullions every 2.1 m; lit panes per mullion bay.
- 85.5–86.7 m dark roof band, deck and plant.
- Core: `Toy_verdigris` prism to 93.3 m with slit windows on its long faces, steel cap to 93.9 m, white light line.

### Palette

`Toy_teal`, `Toy_glassd`, `Toy_steel`, `Toy_ink`, `Toy_verdigris`, `Toy_roofd`, `Toy_granite` (plaza), `Toy_leaf`/`Toy_leafd`/`Toy_rust` (trees); glow `Toy_sand_Glow`, `Toy_white_Glow`.

### Roof

Slab: dark deck with a three-box plant cluster at the east end. Core: plain deck under a steel cap with a white light line.

### Triangle budget

3,618 tris (body 2,800, night glow 818) against a 5,000 cap.

### Draft manifest entry

```json
{"id": "1-bush-street", "file": "1-bush-street.glb", "anchor": [-122.40006, 37.7909563], "targetHeightM": 93.9, "cat": 3, "name": "Crown Zellerbach Building (One Bush Plaza)", "estimated": false, "dims": [75.5086, 53.3574, 93.9], "tris": 3618, "loadRadius": 2817}
```

### Integration notes

Case B. The building occupies its own block; exclusion radius ~38 m around the anchor clears slab and core (check the separate bank pavilion and the Shell Building across Bush survive). loadRadius 2,817 m.

### Open risks

- Core cladding colour and slit-window pattern are not photographed (core faces south).
- OSM footprint includes the core; if a separate core way exists the plan is unaffected.
- Glass is a saturated toy teal; the real glass is a paler blue-green.
