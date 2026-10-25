# Park Tower at Transbay — SF-SIM asset plan

The 43-storey office tower at 250 Howard Street (Goettsch Partners with Solomon Cordwell
Buenz, 2018) on the corner of Beale and Howard, at the east end of Salesforce Park: a
crisp blue-glass prism whose upper third is **carved open at two opposite corners into
stacks of two-storey outdoor terraces**, with a glass screen that carries the slab
above the 168 m roof to 183 m.

**Deliverable:** `artifacts/park-tower/`. Part 1 is the task prompt, Part 2 the dossier.

| | |
|---|---|
| Manifest id | `park-tower` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.3942790, 37.7904360` (OSM OBB centre via `tk.run`) |
| Target height | **183.0 m** architectural (Wikipedia 605 ft = 184.4 m; batch uses 183); roof 168 m (550 ft) |
| Footprint | OSM way 611390934: OBB 56.7 × 54.9 m, 2,766 m² (site incl. podium), bearing 45.0° |
| Triangle cap | 27,000 (built: 5,054) |
| Category | `3` (office) |

---

## Part 1 — Task prompt

````markdown
# Create the Park Tower at Transbay GLB for SF-SIM

Work in artifacts/park-tower/. Read AGENTS.md, docs/styles/miniature-toy.md and
tools/landmark-kit/toykit.py first; Part 2 of this plan is your research start.

Must capture: the blue-glass prism on the SoMa grid; the terrace stacks carved out of
the EAST corner (Howard x Main side) and the WEST corner from ~116 m to the roof, one
open terrace every two floors with planting; the glass crown screen rising over the
slab (not the terrace corners) to 183 m; the low glazed podium with a planted edge.

Contract: binary GLB, metres, +Y = true north, origin at base centre, min Z 0, crest
exactly 183.0 m, flat Toy_* materials, `_Glow` only as outward skins, <= 27,000 tris.
Build with `tk.run(SLUG, build, HERE, (-122.394279, 37.790436), 183.0)`.

Run build -> kit validate.py (--height 183 --anchor <tk.run anchor>, "all checks
pass") -> kit render.py. Write REFERENCE.md and REPORT.md. Do not edit the manifest,
landmarks.mjs or app code.
````

---

## Part 2 — Research and design dossier

### 2.1 Verified facts

| Fact | Value | Label |
|---|---|---|
| Architectural height | 605 ft (184.4 m); 183 m used | published (Wikipedia infobox); batch value |
| Roof | 550 ft = 168 m | published |
| Floors / year | 43 / 2018 | published |
| Architects | Goettsch Partners, Solomon Cordwell Buenz | published |
| Site | Block 5, Beale x Howard (Howard, Main, Beale, Natoma) | published |
| Terraces | "large outdoor terraces on both the northwest and southeast corners" | published (Wikipedia; grid directions) |
| Footprint | OBB 56.7 × 54.9 m, 2,766 m² | measured (OSM, includes podium) |
| Tower plan 44 × 35 m, podium 54 × 50 m × 17 m | | estimated |
| Terrace stacks start ~116 m | | inferred (photo: about two thirds up) |
| LiDAR | none (2010 survey predates the tower) | — |

### 2.2 Sources

- OSM way 611390934 — https://www.openstreetmap.org/way/611390934
- Wikipedia — https://en.wikipedia.org/wiki/Park_Tower_at_Transbay
- Commons — https://commons.wikimedia.org/wiki/File:Park_Tower_at_Transbay.jpg (March 2021,
  the Wikipedia infobox image)
- DataSF footprints (https://data.sf.gov/resource/ynuv-fyni): no usable LiDAR (pre-construction).

### 2.3 Orientation

Prism rotated 45°: faces at 45/135/225/315°. Local +X runs along Howard (bearing 45°).
Howard St frontage = SE face; Beale St = SW face. In SoMa's street-grid parlance
Howard runs "east–west", so the published "NW and SE corners" are the true **west**
and **east** corners. +Y = true north.

### 2.4 What each side shows

The Commons photo is taken from across Howard St (the former temporary terminal
block) looking north-west: the Howard (SE) face square-on, the Beale (SW) face
foreshortened on the left. It shows (a) a stack of open two-storey terraces cut into
the **right-hand = east** corner of the Howard face from about two thirds of the
height to the roof, and (b) the **far-left = west** corner set back over the same
range. Both match the published "NW and SE corners" in grid terms. The NE and NW
faces are not photographed; they are inferred plain glass. The draft's single notch on
the true north corner contradicted both sources and was moved.

### 2.5 Recognition cues

1. Two opposite corner terrace stacks in the upper third. 2. Crisp blue prism.
3. Glass crown screen above the roof. 4. Planted podium.

### 2.7 Massing recipe

- Podium 54 × 50 m, 0–17 m, glass behind trim columns, stone roof, trees.
- Shaft 44 × 35 m, 17–116 m (`tk.shaft`, `Toy_glassl`, steel fins every 3 m).
- Upper 116–168 m on the plan minus two 11 × 11 m corner bays (local (+X,−Y) = E and
  (−X,+Y) = W); terrace slab + tree + lamp in each bay every 7.8 m; trim roof on each bay.
- Roof kit at 168 m; glass screen + white cap 168–183 m on the notched plan.

### 2.8 Palette

`Toy_glassl`, `Toy_glass`, `Toy_steel`, `Toy_trim`, `Toy_stone`, `Toy_white`,
`Toy_roofd`, `Toy_leaf`, `Toy_leafd` (off-palette extra, foliage); glow
`Toy_sand_Glow`, `Toy_white_Glow`.

### 2.9 Roof

Roof deck with plant inside the crown screen; the two terrace stacks are the
signature seen from above. No blank cap.

### 2.11 Triangle budget

5,054 tris (786 glow faces). Lean.

### 2.12 Draft manifest entry

```json
{
  "id": "park-tower",
  "file": "park-tower.glb",
  "anchor": [-122.394279, 37.790436],
  "targetHeightM": 183,
  "cat": 3,
  "name": "Park Tower at Transbay",
  "estimated": false,
  "dims": [81.883, 81.883, 183.0],
  "tris": 5054
}
```

```js
{ id: 'parkTower', name: 'Park Tower at Transbay', lon: -122.394279, lat: 37.790436,
  height: 183, exclude: 30, camera: { distance: 560, yaw: 135, pitch: 20 } }
```

### 2.13 Integration notes

Case B: registry entry, exclusion covering the podium (OBB half-diagonal ≈ 39 m;
201 Mission's driveway and neighbours must survive — check the centroid window),
batch re-bake. Load radius: none suggested (skyline tower).

### 2.15 Open risks

- Only one photo; the west-corner treatment (terraces vs. plain setback) and the stack
  start height (~116 m) are inferred. An aerial would confirm both.
- Height: Wikipedia 605 ft = 184.4 m vs the batch's 183 m (1.4 m low); the lead may
  want 184.4.
- Podium extent and height are estimated from the OSM site polygon.
