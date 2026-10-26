# 595 Market Street — SF-SIM asset plan

A 30-storey office tower (Skidmore, Owings & Merrill, 1979) at Market and Second: a square plan with deeply chamfered corners, wrapped in alternating bright spandrels and dark blue ribbon windows, under a tall pale louvred mechanical screen, on a low planted podium.

**Deliverable:** `artifacts/595-market-street/` (built in the Financial District batch, stages 1–2). Part 1 is the task prompt, Part 2 the dossier.

| | |
|---|---|
| Manifest id | `595-market-street` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.4007917, 37.7892292` (OSM OBB centre, recentred by `tk.run`) |
| Target height | **125.0 m** — 125.0 m crest = roof 410 ft (published) |
| Footprint | OSM way 941649701: OBB 41.7 x 41.2 m, 1,709 m², 9 nodes, long-axis bearing 135.1° |
| Triangle cap | 5,000 (batch cap for towers ≥ 60 m; built: 3,610) |
| Category | `3` (Office — `CAT.office` in `app/src/props.js`) |

---

## Part 1 — Task prompt

````markdown
# Create the 595 Market Street GLB for SF-SIM

Work in artifacts/595-market-street/. Read AGENTS.md, docs/styles/miniature-toy.md and
tools/landmark-kit/toykit.py first; Part 2 of this plan is your research start.

Must capture the ranked cues in 2.5. Contract: binary GLB, metres, +Y = true north, origin at base centre, min Z 0, crest exactly 125.0 m,
flat Toy_* materials, `_Glow` only as outward skins, no degenerate triangles, <= 5,000 tris.
Build with `tk.run(SLUG, build, HERE, (-122.4007917, 37.7892292), 125.0)`; run build ->
validate_595_market_street.py ("all checks pass") -> render_595_market_street.py -- --samples 16; write REFERENCE.md and REPORT.md.
Do not edit the manifest, landmarks.mjs or app code.
````

---

## Part 2 — Research and design dossier

### 2.1 Verified facts

| Fact | Value | Label |
|---|---|---|
| Roof | 125.0 m (410 ft) | published (Wikipedia) |
| Floors / year / architect | 30 / 1979 / SOM | published |
| OSM | `height=125`, 28 levels; plain 41.7 x 41.2 m square | OSM |
| 2010 LiDAR | 128.95 m | measured (includes roof plant above the published roof) |
| Chamfers 8 m legs; screen 117-125 m; podium 6.5 m |  | inferred (photo; Wikipedia calls it 'hexagonal') |

### 2.2 Sources

- OSM way 941649701 — https://www.openstreetmap.org/way/941649701 (footprint, tags: `height=125`, `building:levels=28`)
- Wikipedia — https://en.wikipedia.org/wiki/595_Market_Street
- Commons photo (the Wikipedia lead photo, from Market St) — https://commons.wikimedia.org/wiki/File:595_Market_Street.jpg
- DataSF 2010 LiDAR building heights — https://data.sf.gov/resource/ynuv-fyni (`hgt_max` 128.95 m)

### 2.3 Orientation

Square sides parallel to Market St (OSM bearing 135.1): the NW face looks onto Market, the NE face onto Second St.

### 2.4 What each side shows

- Market (NW) and Second (NE): photographed - striped skin, chamfers, planted podium terrace.
- SE / SW: same skin assumed (**inferred**).

### 2.5 Recognition cues (ranked)

1. Crisp horizontal white / dark-blue stripes.
2. Chamfered square plan (reads octagonal).
3. Tall pale louvred crown screen.

### 2.7 Massing recipe

- Plan `tk.chamfer_rect(41, 41, 8)` on yaw -45.1 deg.
- Podium: stone, punched dark windows, planted deck, four corner trees.
- Shaft 6.8-117 m: `tk.shaft` 27 storeys, `Toy_glass` + 1.75 m `Toy_white` bands (no fins).
- Screen 117-125 m: `Toy_trim` ring with four steel louvre lines round a dark deck and plant; white crown line.

### 2.8 Palette

`Toy_glass`, `Toy_white`, `Toy_trim`, `Toy_steel`, `Toy_stone`, `Toy_glassd`, `Toy_roofd`, `Toy_leaf(d)`, `Toy_rust`; glow `Toy_sand_Glow`, `Toy_white_Glow`.

### 2.9 Roof

Louvred screen ring around a dark deck with a plant cluster.

### 2.11 Triangle budget

3,610 tris (body 2,936, night glow 674) against the batch cap of 5,000.

### 2.12 Draft manifest entry

```json
{"id": "595-market-street", "file": "595-market-street.glb", "anchor": [-122.4007917, 37.7892292], "targetHeightM": 125.0, "cat": 3, "name": "595 Market Street", "estimated": false, "dims": [66.3268, 66.3268, 125.0], "tris": 3610, "loadRadius": 3750}
```

### 2.13 Integration notes

Case B: registry entry in `pipeline/lib/landmarks.mjs`, exclusion of OSM way 941649701 from the baked tiles, batch re-bake.
`dims` is the axis-aligned box of the rotated plan plus apron/plinth. Load radius 3750 m (max(2500, 30 x height)).
Check at bake time that the exclusion clears only this footprint.

### 2.15 Open risks

- Chamfer size is inferred.
- Crest uses the published roof (125 m) though LiDAR sees plant to ~129 m.
