# Old Saint Mary's Cathedral — SF-SIM asset plan

California's first cathedral: red brick Gothic Revival with a square brick tower centred on the California Street front — stepped corner buttresses, clock faces over the "Son, observe the time and fly from evil" plaque, louvred lancet belfry openings, four pinnacles and a central cross — before a gabled nave whose Grant Avenue side is buttressed and crenellated.

**Deliverable:** `artifacts/old-saint-marys-cathedral/` (Financial District batch, stages 1–2, BATCH mode).

| | |
|---|---|
| Manifest id | `old-saint-marys-cathedral` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.4057137, 37.7928426` (OSM OBB centre via `tk.run`) |
| Target height | **33.65 m** — DataSF 2010 LiDAR max 33.65 m (tower cross) of ring 201006.0002205; tower parapet 26.5 m = facts-file LiDAR peak; nave ridge 20.5 m between ring median 19.3 and majority 21.4 (measured) |
| Footprint | OSM way 260520154: OBB 46.3 × 42.2 m, 1270 m², long-axis bearing 171° |
| Triangle cap | 3,000 (building < 60 m; built: 1,694) |
| Category | `8` (Worship — `CAT.worship` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Crest (tower cross) | 33.65 m | measured (LiDAR max) |
| Tower parapet | 26.5 m | measured (facts-file LiDAR) |
| Nave ridge | 20.5 m | measured range (ring median 19.3 / majority 21.4) |
| Built / architects | 1853–54 Craine & England; 1908–09 Welsh & Carey | published (Wikipedia) |
| Front | south (California St) | published (infobox facade_direction) |
| Footprint | OBB 46.3 × 42.2 m incl. parish buildings, 1,270 m² | measured (OSM) |

### Sources

- OSM way 260520154 — https://www.openstreetmap.org/way/260520154
- Wikipedia — https://en.wikipedia.org/wiki/Old_St._Mary%27s_Cathedral
- DataSF building footprints + 2010 LiDAR heights — https://data.sf.gov/resource/ynuv-fyni
- Commons photo — https://commons.wikimedia.org/wiki/File:Old_St._Mary%27s_Cathedral_(San_Francisco)_(1a).jpg (from California × Grant)

### Orientation

Street grid: local +x = bearing 81° (east along California), +y = north (up Grant). Tower front faces California St (south); the long crenellated nave side faces Grant Ave (west).

### What each side shows

- S (California): tower with door, clock and plaque; nave gable with west door and paired windows — photographed.
- W (Grant): buttressed brick nave wall with lancets and crenellations, side chapel — photographed in part.
- E: parish hall/rectory block (3 storeys) — **inferred** from the OSM outline.
- N: rear, not photographed.

### Recognition cues (ranked)

1. Square red-brick tower with clock faces, pinnacles and a cross.
2. Steep gabled nave behind it with a crenellated, buttressed side.
3. Pointed (lancet) windows and the deep-set Gothic door in the tower base.

### Massing recipe

- Nave 21.1 × 42.5 m brick prism to 13 m with buttresses every 5.3 m, lancets (lit), parapet and merlons; slate-dark gable roof to 20.5 m; brick gable wall.
- Tower 6.9 × 6.9 m to 26.5 m: corner buttresses, stone bands, louvred belfry arches, door; clock discs (S, W) with glow and plaques.
- Stone parapet, four brick pinnacles with stone caps, a gablet and the cross to 33.65 m.
- Parish hall L-block (11 m) to the east, porches, side chapel on Grant.

### Palette, roof, budget

- Palette: `Toy_brick`, `Toy_stone`, `Toy_cream` (clock faces), `Toy_ink`, `Toy_glassd`, `Toy_roofd`, `Toy_concrete`; glow `Toy_mustard_Glow`, `Toy_cream_Glow`, `Toy_sand_Glow`.
- Roof: Dark gabled nave roof; flat dark parish-hall roof; tower parapet with pinnacles.
- Budget: 1,694 triangles against the 3,000 cap (validated with `--budget 3000`).

### Draft manifest entry

```json
{"id": "old-saint-marys-cathedral", "file": "old-saint-marys-cathedral.glb", "anchor": [-122.4057137, 37.7928426], "targetHeightM": 33.65, "cat": 8, "name": "Old Saint Mary's Cathedral", "estimated": false, "dims": [53.2554, 56.5804, 33.65], "tris": 1694, "loadRadius": 2500}
```

### Integration notes

Case B: registry entry in `pipeline/lib/landmarks.mjs`, exclusion of OSM way 260520154 from the
procedural bake, batch re-bake. 

### Open risks

- Nave ridge and eave heights are read from LiDAR statistics of a ring that also covers the parish buildings.
- Parish/rectory massing east of the nave is inferred from the OSM outline only.
- The cross is thin; LiDAR max may belong to a pinnacle instead.
