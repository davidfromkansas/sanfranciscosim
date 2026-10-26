# Stevenson Place (71 Stevenson Street) — SF-SIM asset plan

A postmodern office tower (Kaplan McLaughlin Diaz, 1987) at 71 Stevenson Street between Market and Mission: a five-storey dark rose-granite base under a shaft of cream piers framing rose granite spandrels, corners that step back near the top, and a gabled, hipped crown with a dark louvred opening.

**Deliverable:** `artifacts/stevenson-place/` (built in the Financial District batch, stages 1–2). Part 1 is the task prompt, Part 2 the dossier.

| | |
|---|---|
| Manifest id | `stevenson-place` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.3997358, 37.7893616` (OSM OBB centre, recentred by `tk.run`) |
| Target height | **103.0 m** — 103.0 m crest (published, Wikipedia; OSM `height=103`); LiDAR 105.97 m |
| Footprint | OSM way 149840694: OBB 43.8 x 41.2 m, 1,630 m², 10 nodes, long-axis bearing 134.5° |
| Triangle cap | 5,000 (batch cap for towers ≥ 60 m; built: 4,414) |
| Category | `3` (Office — `CAT.office` in `app/src/props.js`) |

---

## Part 1 — Task prompt

````markdown
# Create the Stevenson Place (71 Stevenson Street) GLB for SF-SIM

Work in artifacts/stevenson-place/. Read AGENTS.md, docs/styles/miniature-toy.md and
tools/landmark-kit/toykit.py first; Part 2 of this plan is your research start.

Must capture the ranked cues in 2.5. Contract: binary GLB, metres, +Y = true north, origin at base centre, min Z 0, crest exactly 103.0 m,
flat Toy_* materials, `_Glow` only as outward skins, no degenerate triangles, <= 5,000 tris.
Build with `tk.run(SLUG, build, HERE, (-122.3997359, 37.7893242), 103.0)`; run build ->
validate_stevenson_place.py ("all checks pass") -> render_stevenson_place.py -- --samples 16; write REFERENCE.md and REPORT.md.
Do not edit the manifest, landmarks.mjs or app code.
````

---

## Part 2 — Research and design dossier

### 2.1 Verified facts

| Fact | Value | Label |
|---|---|---|
| Height | 103 m | published (Wikipedia) |
| Floors / year / architect | 24 (infobox 28) / 1987 / Kaplan McLaughlin Diaz | published |
| 2010 LiDAR | 105.97 m | measured (3 m above the published figure; not used) |
| Tower 38 x 28 m on the 43.8 x 41.2 m lot; base 19 m; step-back 87.4 m; crown base 95 m |  | inferred (photo) |

### 2.2 Sources

- OSM way 149840694 — https://www.openstreetmap.org/way/149840694 (footprint, tags: `height=103`, `building:levels=-`)
- Wikipedia — https://en.wikipedia.org/wiki/Stevenson_Place
- Commons photo (the Wikipedia lead photo, from the plaza in front of the main entrance) — https://commons.wikimedia.org/wiki/File:Stevenson_Place.jpg
- DataSF 2010 LiDAR building heights — https://data.sf.gov/resource/ynuv-fyni (`hgt_max` 105.97 m)

### 2.3 Orientation

Yaw -44.5 deg (OSM bearing 134.5): local +x faces SE, +y faces NE. The OSM lot has a stepped cut at the south corner; the tower block is pushed to the NE half (**inferred**), the remainder reads as base roof.

### 2.4 What each side shows

- Photographed face: granite base with the 71 Stevenson sign, piered shaft, stepped corners, gable crown.
- Other faces: same treatment assumed (**inferred**).

### 2.5 Recognition cues (ranked)

1. Gabled, hipped crown - a 'house roof' on a tower.
2. Cream piers on rose granite.
3. Dark granite base, stepped top corners.

### 2.7 Massing recipe

- Base: OSM polygon (9 nodes), `tk.punched_block` in `Toy_granite`, cream band courses.
- Shaft 19-87.4 m: `notch_rect(38, 28, 3.5)` granite prism, dark panes, cream piers every 3.4 m, lit panes.
- Upper 87.4-95 m: `notch_rect(30, 24, 4)` cream punched block.
- Crown: cream wall 95-98 m with dark louvres, frustum to a 2 x 14 m ridge at 103 m; white glow line at its foot.

### 2.8 Palette

`Toy_granite`, `Toy_cream`, `Toy_glassd`, `Toy_ink`, `Toy_roofd`, `Toy_steel`, `Toy_stone`; glow `Toy_sand_Glow`, `Toy_white_Glow`.

### 2.9 Roof

Hipped crown over the stepped upper storeys; plant on the lower base roof.

### 2.11 Triangle budget

4,414 tris (body 3,736, night glow 678) against the batch cap of 5,000.

### 2.12 Draft manifest entry

```json
{"id": "stevenson-place", "file": "stevenson-place.glb", "anchor": [-122.3997358, 37.7893616], "targetHeightM": 103.0, "cat": 3, "name": "Stevenson Place (71 Stevenson Street)", "estimated": false, "dims": [67.0601, 58.2913, 103.0], "tris": 4414, "loadRadius": 3090}
```

### 2.13 Integration notes

Case B: registry entry in `pipeline/lib/landmarks.mjs`, exclusion of OSM way 149840694 from the baked tiles, batch re-bake.
`dims` is the axis-aligned box of the rotated plan plus apron/plinth. Load radius 3090 m (max(2500, 30 x height)).
Check at bake time that the exclusion clears only this footprint.

### 2.15 Open risks

- Tower position on the lot and tier heights are inferred.
- Floor counts disagree (24 vs 28); published 103 m used, LiDAR says ~106 m.
