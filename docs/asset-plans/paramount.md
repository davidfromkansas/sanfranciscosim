# The Paramount (680 Mission Street) — SF-SIM asset plan

A 40-storey rental-apartment tower (Kwan Henmi Architecture/Planning, 2001) at Mission and Third, once the tallest concrete-framed building in Seismic Zone 4: pale precast with long ribbon windows, a broad lower block with stepped shoulders, and a central slab rising ten more storeys to a thin, boldly overhanging flat roof cap.

**Deliverable:** `artifacts/paramount/` (built in the Financial District batch, stages 1–2). Part 1 is the task prompt, Part 2 the dossier.

| | |
|---|---|
| Manifest id | `paramount` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.4020234, 37.7867030` (OSM OBB centre, recentred by `tk.run`) |
| Target height | **128.0 m** — 128.0 m crest = 420 ft (published); OSM 127 |
| Footprint | OSM way 160673823: OBB 50.6 x 47.8 m, 2,296 m², 8 nodes, long-axis bearing 45.4° |
| Triangle cap | 5,000 (batch cap for towers ≥ 60 m; built: 3,898) |
| Category | `2` (Apartments — `CAT.apartments` in `app/src/props.js`) |

---

## Part 1 — Task prompt

````markdown
# Create the Paramount (680 Mission Street) GLB for SF-SIM

Work in artifacts/paramount/. Read AGENTS.md, docs/styles/miniature-toy.md and
tools/landmark-kit/toykit.py first; Part 2 of this plan is your research start.

Must capture the ranked cues in 2.5. Contract: binary GLB, metres, +Y = true north, origin at base centre, min Z 0, crest exactly 128.0 m,
flat Toy_* materials, `_Glow` only as outward skins, no degenerate triangles, <= 5,000 tris.
Build with `tk.run(SLUG, build, HERE, (-122.4020234, 37.7867294), 128.0)`; run build ->
validate_paramount.py ("all checks pass") -> render_paramount.py -- --samples 16; write REFERENCE.md and REPORT.md.
Do not edit the manifest, landmarks.mjs or app code.
````

---

## Part 2 — Research and design dossier

### 2.1 Verified facts

| Fact | Value | Label |
|---|---|---|
| Height | 128 m (420 ft) | published (Wikipedia) |
| Floors / year / architect | 40 / 2001 / Kwan Henmi Architecture/Planning | published |
| 2010 LiDAR | 91.67 m | measured - the shoulder roofs; used for the lower block (92 m) |
| Use | rental apartments | published -> category 2 |
| Central slab 40 x 24 m (long axis NE-SW); cap overhang 2.4 m; podium 11 m |  | inferred (photo) / estimated |

### 2.2 Sources

- OSM way 160673823 — https://www.openstreetmap.org/way/160673823 (footprint, tags: `height=127`, `building:levels=40`)
- Wikipedia — https://en.wikipedia.org/wiki/The_Paramount,_San_Francisco
- Commons photo (the Wikipedia lead photo, from Yerba Buena Gardens, looking NE at the SW (Third St) face) — https://commons.wikimedia.org/wiki/File:The_Paramount,_San_Francisco_from_Yerba_Buena_Gardens.jpg
- DataSF 2010 LiDAR building heights — https://data.sf.gov/resource/ynuv-fyni (`hgt_max` 91.67 m)

### 2.3 Orientation

Yaw 44.6 deg (OSM bearing 45.4): local +x faces NE, +y faces NW = **Mission St** (the tower is on its south side), -x faces SW = **Third St**. OSM notch at the north corner. The photo, from Yerba Buena Gardens across Third, shows the SW face.

### 2.4 What each side shows

- SW (Third): photographed - ribbon windows, shoulders either side, central slab, overhanging cap.
- Other faces: same skin assumed (**inferred**); the right-hand balcony column in the photo is not modelled.

### 2.5 Recognition cues (ranked)

1. Thin overhanging flat roof cap.
2. Central slab rising above two lower shoulders.
3. Pale banded ribbon-window skin.

### 2.7 Massing recipe

- Plan = OSM polygon in the local frame (6 nodes).
- Podium 0-11 m: dark retail glass, stone piers, lit ring, stone band.
- Lower block 11-92 m: `tk.shaft` 26 storeys, `Toy_glass` ribbons + 1.45 m `Toy_stone` bands.
- Central slab to 124.6 m (10 storeys, `Toy_concrete` bands); recessed lit top storey; `Toy_concrete` cap 126.6-128 m overhanging 2.4 m.
- Plant on both shoulders; four street trees on Mission (NW).

### 2.8 Palette

`Toy_stone`, `Toy_concrete`, `Toy_glass`, `Toy_glassd`, `Toy_roofd`, `Toy_steel`, `Toy_leaf(d)`, `Toy_rust`; glow `Toy_sand_Glow`, `Toy_white_Glow`.

### 2.9 Roof

The overhanging cap reads from above as a clean slab; shoulder roofs carry plant.

### 2.11 Triangle budget

3,898 tris (body 2,796, night glow 1,102) against the batch cap of 5,000.

### 2.12 Draft manifest entry

```json
{"id": "paramount", "file": "paramount.glb", "anchor": [-122.4020234, 37.786703], "targetHeightM": 128.0, "cat": 2, "name": "The Paramount (680 Mission Street)", "estimated": false, "dims": [76.3795, 70.5152, 128.0], "tris": 3898, "loadRadius": 3840}
```

### 2.13 Integration notes

Case B: registry entry in `pipeline/lib/landmarks.mjs`, exclusion of OSM way 160673823 from the baked tiles, batch re-bake.
`dims` is the axis-aligned box of the rotated plan plus apron/plinth. Load radius 3840 m (max(2500, 30 x height)).
Check at bake time that the exclusion clears only this footprint.

### 2.15 Open risks

- Slab size/position on the lot is inferred from one photo.
- The 2010 LiDAR (91.7 m) only sees the shoulders.
