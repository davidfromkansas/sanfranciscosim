# 222 Second Street (LinkedIn) — SF-SIM asset plan

A 26-storey dark-glass office tower (Thomas Phifer with Gensler, 2016) at the south corner of Second and Howard, LinkedIn's San Francisco office. John King: "a form that begins as a squat 16-story rectangle and concludes as a 10-story square", skinned in overlapping 6 x 13 ft shingled glass panes over a four-storey glass base.

**Deliverable:** `artifacts/222-2nd-street/` (built in the Financial District batch, stages 1–2). Part 1 is the task prompt, Part 2 the dossier.

| | |
|---|---|
| Manifest id | `222-2nd-street` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.3982516, 37.7863336` (OSM OBB centre, recentred by `tk.run`) |
| Target height | **112.8 m** — 112.8 m crest = architectural top 370 ft (published); roof 350 ft = 106.7 m |
| Footprint | OSM way 80296717: OBB 49.9 x 46.9 m, 2,200 m², 6 nodes, long-axis bearing 135° |
| Triangle cap | 5,000 (batch cap for towers ≥ 60 m; built: 4,502) |
| Category | `3` (Office — `CAT.office` in `app/src/props.js`) |

---

## Part 1 — Task prompt

````markdown
# Create the 222 Second Street (LinkedIn) GLB for SF-SIM

Work in artifacts/222-2nd-street/. Read AGENTS.md, docs/styles/miniature-toy.md and
tools/landmark-kit/toykit.py first; Part 2 of this plan is your research start.

Must capture the ranked cues in 2.5. Contract: binary GLB, metres, +Y = true north, origin at base centre, min Z 0, crest exactly 112.8 m,
flat Toy_* materials, `_Glow` only as outward skins, no degenerate triangles, <= 5,000 tris.
Build with `tk.run(SLUG, build, HERE, (-122.3982516, 37.786315), 112.8)`; run build ->
validate_222_2nd_street.py ("all checks pass") -> render_222_2nd_street.py -- --samples 16; write REFERENCE.md and REPORT.md.
Do not edit the manifest, landmarks.mjs or app code.
````

---

## Part 2 — Research and design dossier

### 2.1 Verified facts

| Fact | Value | Label |
|---|---|---|
| Roof / architectural top | 106.7 m (350 ft) / 112.8 m (370 ft) | published (Wikipedia infobox) |
| Floors / year / architect | 26 / 2016 / Thomas Phifer & Partners, Gensler | published |
| Massing | 16-storey rectangle + 10-storey square | published (SF Chronicle, John King) |
| OSM | `height=106`, `building:levels=27` | OSM |
| 2010 LiDAR | 139.84 m | measured, but **not usable**: the survey predates construction (crane or neighbour hit) |
| Upper square 36 x 36 m, flush with the NE and SE faces |  | inferred (photo) |

### 2.2 Sources

- OSM way 80296717 — https://www.openstreetmap.org/way/80296717 (footprint, tags: `height=106`, `building:levels=27`)
- Wikipedia — https://en.wikipedia.org/wiki/222_Second_Street
- Commons photo (the Wikipedia lead photo, looking up at the Second x Howard corner) — https://commons.wikimedia.org/wiki/File:222_Second_Street.jpg
- DataSF 2010 LiDAR building heights — https://data.sf.gov/resource/ynuv-fyni (`hgt_max` 139.84 m)

### 2.3 Orientation

Yaw -45 deg (OSM bearing 135): local +x faces SE, +y faces NE (**Second St**), -x faces NW (**Howard St**). The 22.7 x 5.8 m OSM notch sits at the south (rear) corner.

### 2.4 What each side shows

- NE (Second) and NW (Howard): the photographed corner - dark shingled glass, four-storey glass base, LinkedIn sign.
- SE / SW: toward neighbours; same skin assumed (**inferred**). The upper square's set-back side is **inferred** as Howard.

### 2.5 Recognition cues (ranked)

1. Two-step dark glass mass: wide 16-storey block, 10-storey square on top.
2. Fine vertical shingle rhythm (fins) and dark grey glass.
3. Glass base with the blue LinkedIn "in" at the corner.

### 2.7 Massing recipe

- Plan = OSM polygon in the local frame (6 nodes).
- Base 0-16.4 m `Toy_glassd` inset 0.8 m with `Toy_glass` fins every 3.7 m and a lit ring.
- Lower block to 65.6 m: `tk.shaft` 12 storey-groups, `Toy_glassd` + `Toy_glass` bands, `Toy_glassl` fins 3.7 m.
- Upper square 36 m to 106.7 m (10 storeys), then a glass screen ring to 112.8 m round a deck and plant.
- Sky-blue sign + `Toy_sky_Glow` on the NE face at the north corner; terrace plant on the setback; trees on Second.

### 2.8 Palette

`Toy_glassd`, `Toy_glass`, `Toy_glassl`, `Toy_roofd`, `Toy_steel`, `Toy_sky`, `Toy_stone`, `Toy_leaf(d)`, `Toy_rust`; glow `Toy_sand_Glow`, `Toy_sky_Glow`, `Toy_white_Glow`.

### 2.9 Roof

Glass screen ring hiding a deck and plant cluster on the square; dark deck with low plant on the 16-storey setback; white crown line at night.

### 2.11 Triangle budget

4,502 tris (body 3,910, night glow 592) against the batch cap of 5,000.

### 2.12 Draft manifest entry

```json
{"id": "222-2nd-street", "file": "222-2nd-street.glb", "anchor": [-122.3982516, 37.7863336], "targetHeightM": 112.8, "cat": 3, "name": "222 Second Street (LinkedIn)", "estimated": false, "dims": [76.7918, 72.6906, 112.8], "tris": 4502, "loadRadius": 3384}
```

### 2.13 Integration notes

Case B: registry entry in `pipeline/lib/landmarks.mjs`, exclusion of OSM way 80296717 from the baked tiles, batch re-bake.
`dims` is the axis-aligned box of the rotated plan plus apron/plinth. Load radius 3384 m (max(2500, 30 x height)).
Check at bake time that the exclusion clears only this footprint.

### 2.15 Open risks

- Which side the upper square is set back from is inferred from one photo.
- Crest uses the 370 ft architectural top (screen); the roof proper is 350 ft.
