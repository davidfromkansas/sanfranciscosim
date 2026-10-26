# U.S. Custom House — SF-SIM asset plan

A six-storey Beaux-Arts federal block faced in pale Raymond granite, filling the block between Battery, Washington and Jackson. Its U-shaped plan wraps a two-storey oval pavilion holding the Custom Hall with three skylights. Three zones: a rusticated ground storey, smooth middle storeys with pedimented windows, and a top storey above a deep modillioned cornice, with sculpted eagle groups standing on the cornice.

**Deliverable:** `artifacts/us-customs-house/` (Financial District batch, stages 1–2, BATCH mode).

| | |
|---|---|
| Manifest id | `us-customs-house` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.4009459, 37.7962972` (OSM OBB centre via `tk.run`) |
| Target height | **30.46 m** — DataSF 2010 LiDAR max 30.46 m (sculpture group over the cornice); roof parapet 28.87 m = ring majority (measured) |
| Footprint | OSM way 32859013: OBB 79.3 × 33.8 m, 2499 m², long-axis bearing 171.5° |
| Triangle cap | 3,000 (building < 60 m; built: 2,834) |
| Category | `18` (Government — `CAT.government` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Crest (sculpture group) | 30.46 m | measured (LiDAR ring 201006.0000710 max) |
| Roof parapet | 28.87 m | measured (LiDAR majority; median 24.6) |
| Storeys / year / architect | 6 / 1911 / Eames & Young | published (Wikipedia, GSA) |
| Plan | U around an oval two-storey Custom Hall pavilion | published (GSA) |
| Footprint | OBB 79.3 × 33.8 m, 2,499 m², light courts on the west side | measured (OSM) |
| Main entrance + sculpture group | Battery St (east) face | published (GSA); position on the face inferred |

### Sources

- OSM way 32859013 — https://www.openstreetmap.org/way/32859013
- Wikipedia — https://en.wikipedia.org/wiki/United_States_Customhouse_(San_Francisco)
- GSA — https://www.gsa.gov/historic-buildings/us-custom-house-san-francisco-ca (via Wikipedia)
- DataSF building footprints + 2010 LiDAR heights — https://data.sf.gov/resource/ynuv-fyni
- Commons photo (infobox) — https://commons.wikimedia.org/wiki/File:U._S._Customhouse_(San_Francisco).JPG (Washington × Battery corner)

### Orientation

Street grid: local +x = bearing 81.5° (Battery St face, east), +y = 351.5° (Jackson St, north); +Y = true north. South = Washington St, west = the court side toward Sansome.

### What each side shows

- S (Washington) and E (Battery): rusticated base, three smooth storeys, cornice, top storey — photographed.
- E (Battery): projecting frontispiece with columns, arched door and the main sculpture group — **inferred** placement from the GSA text.
- N (Jackson): assumed to mirror Washington (**inferred**).
- W: the U's open side with the oval Custom Hall pavilion in the court (OSM light courts; pavilion form from GSA text).

### Recognition cues (ranked)

1. Long pale-granite federal block with a deep cornice and attic storey.
2. U plan with the low oval Custom Hall and its skylights in the court (reads from above).
3. Sculpted eagle/figure groups breaking the roofline, the biggest over the Battery entrance.
4. Heavily rusticated ground storey.

### Massing recipe

- Plan: U in local metres (wings 19–20 m deep around a 35 m court) on the OSM OBB, yaw from bearing 81.5°.
- 0–6.4 m `Toy_stone` base, one rustication band, tall ground-floor panes, lit; base course.
- 7.1–22 m `tk.punched_block` (3 storeys of 4.97 m) in `Toy_white`; 1.3 m cornice.
- 23.3–28.87 m top storey set in 1.6 m with panes, parapet, dark deck and a low plant strip.
- Battery frontispiece: proud wall, six columns, arched lit door; stepped sculpture group to 30.46 m; smaller eagle groups on the Washington and Jackson centres.
- Court: oval pavilion 0–12.6 m with arched windows, verdigris hipped roof and three lit skylights; link block to the Battery wing.

### Palette, roof, budget

- Palette: `Toy_white`, `Toy_stone`, `Toy_concrete` (rustication, sidewalk), `Toy_glassd`, `Toy_glassl`, `Toy_verdigris`, `Toy_roofd`, `Toy_steel`; glow `Toy_sand_Glow`, `Toy_white_Glow`.
- Roof: Dark deck with a low plant strip inside the top-storey parapet; the pavilion's verdigris roof and three lit skylights in the court.
- Budget: 2,834 triangles against the 3,000 cap (validated with `--budget 3000`).

### Draft manifest entry

```json
{"id": "us-customs-house", "file": "us-customs-house.glb", "anchor": [-122.4009459, 37.7962972], "targetHeightM": 30.46, "cat": 18, "name": "U.S. Custom House", "estimated": false, "dims": [50.8194, 89.0101, 30.46], "tris": 2834, "loadRadius": 2500}
```

### Integration notes

Case B: registry entry in `pipeline/lib/landmarks.mjs`, exclusion of OSM way 32859013 from the
procedural bake, batch re-bake. 

### Open risks

- Exact shape of the oval pavilion and the court is read from OSM's light-court notches and the GSA text, not a plan drawing.
- Sculpture groups are block abstractions; only the Washington group is photographed; Battery group placement inferred.
- N and W elevations not photographed.
