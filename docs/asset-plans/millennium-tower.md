# Millennium Tower — SF-SIM asset plan

The 58-storey residential tower at 301 Mission Street (Handel Architects, 2009): a long,
round-ended plan of deep blue glass pinstriped by fine white vertical mullions, whose
top **steps down in terraces** along its length. Best known for having settled and
tilted, which the miniature does not show. It stands one block north-east of
Salesforce Tower on the Mission/Fremont corner and is seen with it in every
Transbay frame.

**Deliverable:** `artifacts/millennium-tower/`. Part 1 is the task prompt, Part 2 the dossier.

| | |
|---|---|
| Manifest id | `millennium-tower` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.3961910, 37.7904150` (OSM OBB centre via `tk.run`) |
| Target height | **197.0 m** architectural (published 645 ft); 2010 LiDAR max 194.91 m, majority roof 184.31 m (measured) |
| Footprint | OSM way 72963089: OBB 47.9 × 33.1 m, 1,481 m², long axis bearing 135.5° |
| Triangle cap | 27,000 (built: 9,766) |
| Category | `2` (apartments — residential condominium tower) |

---

## Part 1 — Task prompt

````markdown
# Create the Millennium Tower GLB for SF-SIM

Work in artifacts/millennium-tower/. Read AGENTS.md, docs/styles/miniature-toy.md and
tools/landmark-kit/toykit.py first; Part 2 of this plan is your research start.

Must capture: the long round-ended plan on the OSM heading, the deep-blue glass with a
dense white vertical pinstripe, the terraced top stepping down along the long axis,
the white mechanical screen on the highest tier, a glazed lobby with a canopy.

Contract: binary GLB, metres, +Y = true north, origin at base centre, min Z 0, crest
exactly 197.0 m, flat Toy_* materials, `_Glow` only as outward skins, no degenerate
triangles, <= 27,000 tris. Build with
`tk.run(SLUG, build, HERE, (-122.396191, 37.790415), 197.0)`.

Run build -> kit validate.py (--height 197 --anchor <tk.run anchor>, "all checks
pass") -> kit render.py. Write REFERENCE.md and REPORT.md. Do not edit the manifest,
landmarks.mjs or app code.
````

---

## Part 2 — Research and design dossier

### 2.1 Verified facts

| Fact | Value | Label |
|---|---|---|
| Architectural height | 197 m (645 ft) | published |
| LiDAR (2010) | max 194.91 m, majority 184.31 m, median 175.88 m | measured (DataSF 201006.0001788) |
| Floors / year / architect | 58 / 2009 / Handel Architects | published |
| Footprint | OBB 47.9 × 33.1 m, 1,481 m², 12 nodes | measured (OSM) |
| Heading | long axis 135.5° (along Fremont St) | measured |
| Terrace steps 171 / 179 / 187 / 193.5 m | | estimated (photo + LiDAR spread) |

The LiDAR spread (majority 184 m, max 195 m) confirms a large stepped roof region well
below the crest; the published 197 m is used for the crest because the loader scales
on it and the 2010 survey misses the thin screen top.

### 2.2 Sources

- OSM way 72963089 — https://www.openstreetmap.org/way/72963089
- DataSF footprints + 2010 LiDAR, `sf16_bldgid` 201006.0001788 — https://data.sf.gov/resource/ynuv-fyni
- Wikipedia — https://en.wikipedia.org/wiki/Millennium_Tower_(San_Francisco)
- Commons: the Wikipedia lead photo (upward view, two faces and the stepped top),
  https://commons.wikimedia.org/wiki/Category:Millennium_Tower_(San_Francisco)

### 2.3 Orientation

Rounded plan, long axis 135.5° (NW–SE, along Fremont St). Mission St frontage = NW
end, Fremont St = SW long face. Model yaw = 90 − 135.5 = −45.5°. +Y = true north.

### 2.4 What each side shows

Long faces (SW/NE): blue glass with white pinstripes, full height. Ends (NW/SE):
rounded, same skin. The terraces step down toward the **NW (Mission) end** in the
model — **inferred** from the photo's stepped mullion tops; the photo does not fix the
compass side with certainty. The mid-rise wing of the complex on Fremont is a separate
building and is not modelled.

### 2.5 Recognition cues

1. Deep-blue glass column with white pinstripes. 2. Terraced, stepped top.
3. Long rounded plan. 4. Pale mechanical screen crowning the top tier.

### 2.7 Massing recipe

- `plan(length)`: rounded rect 46 × 30 m, r = 9 m, shortened from the NW end per tier
  (100 / 82 / 64 / 46% of the length).
- Four `tk.shaft` tiers 10→171→179→187→193.5 m in `Toy_navy` with thin `Toy_glass`
  bands and white fins every 3 m; per-tier pitch chosen as a whole number of ~6 m
  storey-groups (avoids a zero-height loft row).
- Terrace slabs in `Toy_trim` at each setback; roof kit + white screen to 197 m.
- Lobby 0–10 m in `Toy_glassl` with a projecting white canopy; stone apron, 3 trees.

### 2.8 Palette

`Toy_navy`, `Toy_glass`, `Toy_white`, `Toy_trim`, `Toy_glassl`, `Toy_roofd`,
`Toy_steel`, `Toy_stone`, `Toy_leaf`; glow `Toy_sand_Glow`, `Toy_white_Glow`.
All core palette.

### 2.9 Roof

Stepped terraces read from the aerial camera as pale steps; the top tier carries a
roof kit (parapet, deck, plant) inside the white screen. No blank cap.

### 2.11 Triangle budget

9,766 tris (902 glow faces). The fins are the main cost; fine as is.

### 2.12 Draft manifest entry

```json
{
  "id": "millennium-tower",
  "file": "millennium-tower.glb",
  "anchor": [-122.396191, 37.790415],
  "targetHeightM": 197,
  "cat": 2,
  "name": "Millennium Tower",
  "estimated": false,
  "dims": [53.2833, 53.4808, 197.0],
  "tris": 9766
}
```

```js
{ id: 'millenniumTower', name: 'Millennium Tower', lon: -122.396191, lat: 37.790415,
  height: 197, exclude: 26, camera: { distance: 600, yaw: 220, pitch: 20 } }
```

### 2.13 Integration notes

Case B: registry entry, exclusion (OBB half-diagonal ≈ 29 m; the separate mid-rise
wing on Fremont must survive — check the centroid window at bake time), batch re-bake.
Load radius: none suggested (skyline tower).

### 2.15 Open risks

- Which end the terraces step toward is inferred; check an aerial before Gate 3.
- The real plan is irregular (OSM 12 nodes, partly triangular); the model is a rounded
  rectangle on the OBB.
- Tier heights are estimated between the LiDAR majority (184 m) and the crest.
