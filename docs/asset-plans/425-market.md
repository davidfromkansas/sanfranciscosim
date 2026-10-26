# 425 Market Street — SF-SIM asset plan

A 38-storey office slab (SOM, 1973; built as Metropolitan Life's "1 Metropolitan
Plaza") on the Market × Fremont corner. A long flat-topped prism of blue-grey glass set
deep in a crisp silver aluminium grid, raised on a colonnade. One of the cleanest
International Style slabs downtown, and the widest tower in the Transbay batch.

**Deliverable:** `artifacts/425-market/`. Part 1 is the task prompt, Part 2 the dossier.

| | |
|---|---|
| Manifest id | `425-market` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.3981530, 37.7912040` (OSM OBB centre via `tk.run`) |
| Target height | **160.0 m** (Wikipedia, published); 2010 LiDAR max 157.70 m, majority 151.40 m (measured) |
| Footprint | OSM way 32946526: OBB 61.3 × 38.5 m, 2,347 m², 4 nodes, long axis bearing 134.9° |
| Triangle cap | 27,000 (built: 6,756) |
| Category | `3` (Office — `CAT.office` in `app/src/props.js`) |

---

## Part 1 — Task prompt

````markdown
# Create the 425 Market Street GLB for SF-SIM

Work in artifacts/425-market/. Read AGENTS.md, docs/styles/miniature-toy.md and
tools/landmark-kit/toykit.py first; Part 2 of this plan is your research start.

Must capture: a long rectangular slab on the OSM heading; blue-grey glass in a silver
grid (thin steel bands every floor + steel fins every 3 m); a recessed glass base behind
a steel colonnade; a recessed louvred mechanical penthouse with plant above the 152 m
roof; street trees on the Fremont (NE) face.

Contract: binary GLB, metres, +Y = true north, origin at base centre, min Z 0, crest
exactly 160.0 m, flat Toy_* materials, `_Glow` only as outward skins, no degenerate
triangles, <= 27,000 tris (aim for under 10,000). Build with
`tk.run(SLUG, build, HERE, (-122.398153, 37.791204), 160.0)`.

Run build -> kit validate.py (--height 160 --anchor <tk.run anchor>, "all checks
pass") -> kit render.py. Write REFERENCE.md and REPORT.md. Do not edit the manifest,
landmarks.mjs or app code.
````

---

## Part 2 — Research and design dossier

### 2.1 Verified facts

| Fact | Value | Label |
|---|---|---|
| Height | 160 m (520 ft) | published (Wikipedia infobox `roof`) |
| LiDAR (2010) | max 157.70 m, majority 151.40 m, median 151.41 m | measured (DataSF 201006.0000852) |
| Floors / year / architect | 38 / 1973 / SOM | published |
| Footprint | OBB 61.3 × 38.5 m, 2,347 m², 4 nodes | measured (OSM) |
| Heading | long axis 134.9° (along Fremont St) | measured (OSM) |
| OSM `height` | 156 | unsourced tag; not used |
| Main roof ≈ 152 m | | estimated from the LiDAR majority (151.4 m) |

The 160 m published figure is 2.3 m above the LiDAR max; it is kept as the crest (the
batch facts table chose it) and the penthouse fills 152–160 m.

### 2.2 Sources

- OSM way 32946526 — https://www.openstreetmap.org/way/32946526
- DataSF footprints + 2010 LiDAR, `sf16_bldgid` 201006.0000852 — https://data.sf.gov/resource/ynuv-fyni
- Wikipedia — https://en.wikipedia.org/wiki/425_Market_Street
- Commons photo (Wikipedia lead image) — https://commons.wikimedia.org/wiki/File:425_Market_Street_2021_corner.jpg

### 2.3 Orientation

Long axis 134.9° (NW–SE, along Fremont). Model yaw −44.9°; +Y = true north. Local −x
faces 315° = **Market St (NW, short face)**; local +y faces 45° = **Fremont St (NE, long
face)** — the tower is at the SW corner of Market × Fremont (333 Market is across
Fremont to the east). SW long face toward First St; SE short face toward Mission.

### 2.4 What each side shows

The photo shows the Market × Fremont corner: both faces carry the same deep silver grid
with a flush solid band at the very top and a two-storey colonnade at the base with
street trees on both streets. The SW and SE faces are assumed identical (**inferred**).

### 2.5 Recognition cues

1. A long, wide, flat-topped blue-grey slab — the broadest tower in the cluster.
2. The crisp silver aluminium grid.
3. The colonnaded base set back from the sidewalk.

### 2.7 Massing recipe

- Plan `tk.rect(60, 37.5)` on yaw −44.9°.
- Base 0–9 m: glass inset 3 m, `Toy_sand_Glow` ring, steel colonnade every 6 m.
- Shaft 9–152 m: `tk.shaft`, `Toy_glass` with 1.1 m `Toy_steel` bands per 4.1 m storey
  and steel fins every 3 m; scattered lit panes.
- Roof 152 m: steel parapet base + a low plant row; penthouse inset 2 m, 152–155.2 m
  `Toy_glassd` with steel louvres, steel cap, plant cluster up to 160 m.
- Stone apron (4 m), four trees on Fremont.

### 2.8 Palette

`Toy_glass`, `Toy_glassd`, `Toy_steel`, `Toy_roofd`, `Toy_stone`, `Toy_leaf`, `Toy_leafd`,
`Toy_rust`; glow `Toy_sand_Glow`. All core palette.

### 2.9 Roof

A two-level roof: main roof with a plant row, then the louvred penthouse cap with a
plant cluster. Reads as a designed mechanical top from the aerial camera.

### 2.11 Triangle budget

6,756 tris (body 5,440, glow 1,316). The fin grid is the main cost.

### 2.12 Draft manifest entry

```json
{
  "id": "425-market",
  "file": "425-market.glb",
  "anchor": [-122.398153, 37.791204],
  "targetHeightM": 160,
  "cat": 3,
  "name": "425 Market Street",
  "estimated": false,
  "dims": [80.1431, 80.0876, 160.0],
  "tris": 6756
}
```

```js
{ id: '425Market', name: '425 Market Street', lon: -122.398153, lat: 37.791204,
  height: 160, exclude: 30, camera: { distance: 520, yaw: 0, pitch: 20 } }
```

### 2.13 Integration notes

Case B: registry entry, exclusion, batch re-bake. The OBB half-diagonal is ≈ 36 m;
333 Market's centroid is ≈ 105 m away, but low buildings on the First St side may be
closer — confirm at bake time that a ~30 m radius clears only this footprint. Load
radius: none.

### 2.15 Open risks

- The photo shows a flush solid band at the top, not an obviously recessed penthouse;
  the model's recessed louvred penthouse is a readability choice and the 152 m main
  roof is estimated from LiDAR.
- Published 160 m vs LiDAR max 157.7 m (2.3 m apart).
