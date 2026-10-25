# Shell Building (100 Bush Street) — SF-SIM asset plan

A 28-storey Art Deco / Gothic Moderne office tower (George W. Kelham, 1929) at Bush and Battery, all pale cream terracotta: a three-storey arched base, lower side wings, and a slender tower of continuous piers between dark window strips that steps back in tiers into a finialed crown.

**Deliverable:** `artifacts/100-bush-street/` (built in the Financial District batch, stages 1–2). Part 1 is the task prompt, Part 2 the dossier.

| | |
|---|---|
| Manifest id | `100-bush-street` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.3999801, 37.7915717` (OSM OBB centre, recentred by `tk.run`) |
| Target height | **115.22 m** — 115.22 m crest (published: Wikipedia infobox and OSM `height`) |
| Footprint | OSM way 260282390: OBB 37.1 x 41.7 m, 1,542 m², 9 nodes, long-axis bearing 81.3° |
| Triangle cap | 5,000 (batch cap for towers ≥ 60 m; built: 2,760) |
| Category | `3` (Office — `CAT.office` in `app/src/props.js`) |

---

## Part 1 — Task prompt

````markdown
# Create the Shell Building (100 Bush Street) GLB for SF-SIM

Work in artifacts/100-bush-street/. Read AGENTS.md, docs/styles/miniature-toy.md and
tools/landmark-kit/toykit.py first; Part 2 of this plan is your research start.

Must capture the ranked cues in 2.5. Contract: binary GLB, metres, +Y = true north, origin at base centre, min Z 0, crest exactly 115.22 m,
flat Toy_* materials, `_Glow` only as outward skins, no degenerate triangles, <= 5,000 tris.
Build with `tk.run(SLUG, build, HERE, (-122.3999801, 37.7915717), 115.22)`; run build ->
validate_100_bush_street.py ("all checks pass") -> render_100_bush_street.py -- --samples 16; write REFERENCE.md and REPORT.md.
Do not edit the manifest, landmarks.mjs or app code.
````

---

## Part 2 — Research and design dossier

### 2.1 Verified facts

| Fact | Value | Label |
|---|---|---|
| Height | 115.22 m | published (Wikipedia; same as OSM `height`) |
| Floors / year / architect | 28 (infobox says 29) / 1929 / George W. Kelham | published |
| Style | Art Deco, Gothic Moderne; shell castings on the upper cornices | published |
| 2010 LiDAR | 84.08 m | measured - well below the crown; probably a wing roof hit |
| Wing height ~76 m, base 13.5 m, tower tiers 96 / 104 / 110 m |  | inferred (photo) |

### 2.2 Sources

- OSM way 260282390 — https://www.openstreetmap.org/way/260282390 (footprint, tags: `height=115.22`, `building:levels=28`)
- Wikipedia — https://en.wikipedia.org/wiki/Shell_Building_(San_Francisco)
- Commons photo (the Wikipedia lead photo, from the Bush x Battery corner) — https://commons.wikimedia.org/wiki/File:Shell_Building_corner_2021.jpg
- DataSF 2010 LiDAR building heights — https://data.sf.gov/resource/ynuv-fyni (`hgt_max` 84.08 m)

### 2.3 Orientation

Plan axes on bearing 81.3 deg (the FiDi grid): local +x faces ~E (Battery St side), +y faces ~N (Bush St). The tower is pushed 4-5 m toward the Bush x Battery (NE) corner - **inferred** from the photo, which shows the tower rising over that corner with lower wings behind.

### 2.4 What each side shows

- N (Bush) and E (Battery): the photographed street faces - arched base, cream piers, dark strips.
- S and W: party walls toward neighbours; same skin assumed (**inferred**).

### 2.5 Recognition cues (ranked)

1. Pale cream terracotta tower among dark glass.
2. Tiered Art Deco setback crown with finials.
3. Continuous vertical piers / dark window strips.
4. Lower wings and the three-storey arched base.

### 2.7 Massing recipe

- Plan `tk.rect(36.8, 41.4)` on yaw 8.7 deg.
- Base 0-13.5 m `Toy_terracotta`: dark shopfronts, round-headed upper windows, cream cornice.
- Wings to 76 m on the full plan; tower 28 x 30 m to 96 m; chamfered tiers to 104 and 110 m; lantern to 115.22 m.
- Each block: terracotta prism + full-height `Toy_glassd` window strips every 2.5 m + scattered lit panes.
- Finials (6-sided cones) at the tier corners; sand glow rings floodlight the two upper tiers.

### 2.8 Palette

`Toy_terracotta`, `Toy_cream`, `Toy_glassd`, `Toy_roofd`, `Toy_steel`, `Toy_stone`; glow `Toy_sand_Glow`. Off-palette `terracotta`/`glassd` are kit EXTRA tones (WARN only).

### 2.9 Roof

Stepped tiers each with a deck, finials at the corners, a cream lantern with dark slots and a capped top; plant cluster on the wing roof.

### 2.11 Triangle budget

2,760 tris (body 1,908, night glow 852) against the batch cap of 5,000.

### 2.12 Draft manifest entry

```json
{"id": "100-bush-street", "file": "100-bush-street.glb", "anchor": [-122.3999801, 37.7915717], "targetHeightM": 115.22, "cat": 3, "name": "Shell Building (100 Bush Street)", "estimated": false, "dims": [48.3073, 52.1586, 115.22], "tris": 2760, "loadRadius": 3457}
```

### 2.13 Integration notes

Case B: registry entry in `pipeline/lib/landmarks.mjs`, exclusion of OSM way 260282390 from the baked tiles, batch re-bake.
`dims` is the axis-aligned box of the rotated plan plus apron/plinth. Load radius 3457 m (max(2500, 30 x height)).
Check at bake time that the exclusion clears only this footprint.

### 2.15 Open risks

- Tower position and wing height are read from one photo.
- Floor count disagrees (28 text vs 29 infobox); height unaffected.
