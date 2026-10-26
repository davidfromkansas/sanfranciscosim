# 225 Bush Street (Standard Oil Building) — SF-SIM asset plan

The Standard Oil Building (George W. Kelham, 1922; 1950s wing), modelled on the Federal Reserve Bank of New York: a 22-storey pale-stone palazzo filling a long block, with a two-storey arcade of round-headed openings, an ornamented band course, a tall shaft of evenly punched windows and a colonnaded loggia under a deep cornice.

**Deliverable:** `artifacts/225-bush-street/` (built in the Financial District batch, stages 1–2). Part 1 is the task prompt, Part 2 the dossier.

| | |
|---|---|
| Manifest id | `225-bush-street` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.4013094, 37.7908371` (OSM OBB centre, recentred by `tk.run`) |
| Target height | **100.0 m** — 100.0 m crest = 328 ft (published); LiDAR 98.68 m agrees |
| Footprint | OSM way 942665601: OBB 83.9 x 43.2 m, 3,621 m², 9 nodes, long-axis bearing 81.2° |
| Triangle cap | 5,000 (batch cap for towers ≥ 60 m; built: 4,804) |
| Category | `3` (Office — `CAT.office` in `app/src/props.js`) |

---

## Part 1 — Task prompt

````markdown
# Create the 225 Bush Street (Standard Oil Building) GLB for SF-SIM

Work in artifacts/225-bush-street/. Read AGENTS.md, docs/styles/miniature-toy.md and
tools/landmark-kit/toykit.py first; Part 2 of this plan is your research start.

Must capture the ranked cues in 2.5. Contract: binary GLB, metres, +Y = true north, origin at base centre, min Z 0, crest exactly 100.0 m,
flat Toy_* materials, `_Glow` only as outward skins, no degenerate triangles, <= 5,000 tris.
Build with `tk.run(SLUG, build, HERE, (-122.4013094, 37.7908371), 100.0)`; run build ->
validate_225_bush_street.py ("all checks pass") -> render_225_bush_street.py -- --samples 16; write REFERENCE.md and REPORT.md.
Do not edit the manifest, landmarks.mjs or app code.
````

---

## Part 2 — Research and design dossier

### 2.1 Verified facts

| Fact | Value | Label |
|---|---|---|
| Height | 100.0 m (328 ft) | published (Wikipedia); OSM `height=100` |
| Floors / year / architect | 22 (25 incl. basements) / 1922 + 1950s wing / George W. Kelham | published |
| 2010 LiDAR | 98.68 m | measured |
| Footprint | one 83.9 x 43.2 m block | measured (OSM); the two wings are not separated in OSM |
| Loggia 88-95 m, cornice to 97.6 m, penthouses to 100 m |  | inferred (photo) / estimated |

### 2.2 Sources

- OSM way 942665601 — https://www.openstreetmap.org/way/942665601 (footprint, tags: `height=100`, `building:levels=22`)
- Wikipedia — https://en.wikipedia.org/wiki/225_Bush_Street
- Commons photo (the Wikipedia lead photo, looking up at a street corner) — https://commons.wikimedia.org/wiki/File:225_Bush_Street.jpg
- DataSF 2010 LiDAR building heights — https://data.sf.gov/resource/ynuv-fyni (`hgt_max` 98.68 m)

### 2.3 Orientation

Long axis on bearing 81.2 deg: long faces N (**Bush St**, inferred) and S, short faces E and W.

### 2.4 What each side shows

- Photographed corner: arcade, band course, punched shaft, loggia + cornice.
- Rear / court faces: same treatment assumed (**inferred**); light courts, if any, are not modelled.

### 2.5 Recognition cues (ranked)

1. Long pale stone block with a uniform punched-window grid.
2. Colonnaded loggia under a deep cornice.
3. Arched two-storey arcade at the street.

### 2.7 Massing recipe

- Plan `tk.rect(83.6, 43.0)` on yaw 8.8 deg.
- Arcade 0-9.5 m: `Toy_stone` with round-headed `Toy_glassd` openings and lit arches.
- Mezzanine to 17 m + cream band course; shaft to 88 m: `tk.punched_block`, 18 storeys, windows every 4.6 m.
- Loggia 88-95 m: dark recess, lit ring, cream columns every 4.2 m; cornice to 97.6 m; terracotta tile edge.
- Two stone plant penthouses to 100 m and a plant cluster between them.

### 2.8 Palette

`Toy_stone`, `Toy_cream`, `Toy_glassd`, `Toy_terracotta`, `Toy_roofd`, `Toy_steel`; glow `Toy_sand_Glow`.

### 2.9 Roof

Dark deck inside the cornice edge with two pale penthouses and a plant cluster.

### 2.11 Triangle budget

4,804 tris (body 3,964, night glow 840) against the batch cap of 5,000.

### 2.12 Draft manifest entry

```json
{"id": "225-bush-street", "file": "225-bush-street.glb", "anchor": [-122.4013094, 37.7908371], "targetHeightM": 100.0, "cat": 3, "name": "225 Bush Street (Standard Oil Building)", "estimated": false, "dims": [94.8698, 60.9589, 100.0], "tris": 4804, "loadRadius": 3000}
```

### 2.13 Integration notes

Case B: registry entry in `pipeline/lib/landmarks.mjs`, exclusion of OSM way 942665601 from the baked tiles, batch re-bake.
`dims` is the axis-aligned box of the rotated plan plus apron/plinth. Load radius 3000 m (max(2500, 30 x height)).
Check at bake time that the exclusion clears only this footprint.

### 2.15 Open risks

- Light courts / wing split unknown (no aerial photo).
- Penthouse sizes are estimated.
