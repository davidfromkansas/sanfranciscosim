# JPMorgan Chase Building (560 Mission Street) — SF-SIM asset plan

A 31-storey office tower (Cesar Pelli & Associates, 2002), "a minimalist tower wrapped in black steel": a clean rectangular slab of pale glass behind a black steel grid, a slim ledge partway up, the grid running past the roof as an open crown frame, and a tall black-columned base on a landscaped plaza with George Rickey's ring sculpture.

**Deliverable:** `artifacts/560-mission-street/` (built in the Financial District batch, stages 1–2). Part 1 is the task prompt, Part 2 the dossier.

| | |
|---|---|
| Manifest id | `560-mission-street` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.3995478, 37.7888279` (OSM OBB centre, recentred by `tk.run`) |
| Target height | **128.02 m** — 128.02 m crest (published, Wikipedia); LiDAR 127.81 m agrees |
| Footprint | OSM way 79377216: OBB 54.9 x 37.9 m, 2,035 m², 4 nodes, long-axis bearing 134.3° |
| Triangle cap | 5,000 (batch cap for towers ≥ 60 m; built: 4,832) |
| Category | `3` (Office — `CAT.office` in `app/src/props.js`) |

---

## Part 1 — Task prompt

````markdown
# Create the JPMorgan Chase Building (560 Mission Street) GLB for SF-SIM

Work in artifacts/560-mission-street/. Read AGENTS.md, docs/styles/miniature-toy.md and
tools/landmark-kit/toykit.py first; Part 2 of this plan is your research start.

Must capture the ranked cues in 2.5. Contract: binary GLB, metres, +Y = true north, origin at base centre, min Z 0, crest exactly 128.02 m,
flat Toy_* materials, `_Glow` only as outward skins, no degenerate triangles, <= 5,000 tris.
Build with `tk.run(SLUG, build, HERE, (-122.3994826, 37.7887773), 128.02)`; run build ->
validate_560_mission_street.py ("all checks pass") -> render_560_mission_street.py -- --samples 16; write REFERENCE.md and REPORT.md.
Do not edit the manifest, landmarks.mjs or app code.
````

---

## Part 2 — Research and design dossier

### 2.1 Verified facts

| Fact | Value | Label |
|---|---|---|
| Height | 128.02 m | published (Wikipedia); LiDAR 127.81, OSM 128 |
| Floors / year / architect | 31 / 2002 / Cesar Pelli & Associates | published |
| Plaza | bamboo, maples, a pool and Rickey's 'Annular Eclipse' | published |
| Base 9 m, ledge ~46 m, roof deck 122 m, open frame to 128 m |  | inferred (photo) |
| Plaza on the NW (Mission) side, ~16 m deep |  | inferred (photo) / estimated depth |

### 2.2 Sources

- OSM way 79377216 — https://www.openstreetmap.org/way/79377216 (footprint, tags: `height=128`, `building:levels=30`)
- Wikipedia — https://en.wikipedia.org/wiki/JPMorgan_Chase_Building_(San_Francisco)
- Commons photo (the Wikipedia lead photo, from a neighbouring tower looking down at the plaza side) — https://commons.wikimedia.org/wiki/File:560_Mission_Street,_San_Francisco.jpg
- DataSF 2010 LiDAR building heights — https://data.sf.gov/resource/ynuv-fyni (`hgt_max` 127.81 m)

### 2.3 Orientation

Yaw -44.3 deg (OSM bearing 134.3): local +x faces SE, +y faces NE. The building stands on the south side of Mission, so the NW short face fronts **Mission St**, with the plaza between tower and street (photo shows 71 Stevenson across Mission beyond it; **inferred**).

### 2.4 What each side shows

- NW (Mission, plaza) and NE: black grid on pale glass, columned base (photo).
- SE / SW: same skin assumed (**inferred**).

### 2.5 Recognition cues (ranked)

1. Black steel grid over pale glass.
2. Open steel frame crown above the roof.
3. Columned base and the plaza ring sculpture.

### 2.7 Massing recipe

- Plan `tk.rect(54.6, 37.6)` on yaw -44.3 deg.
- Base 0-9 m: recessed `Toy_glassd` lobby, `Toy_ink` columns every 9 m, lit ring; black transfer band.
- Shaft 9.6-122 m in two `tk.shaft` runs (9 + 19 storeys) split by an `Toy_ink` ledge; `Toy_glassl` glass, ink bands and fins every 4.1 m.
- Crown: ink posts, a rail and a top frame ring to 128.02 m round a deck and plant; white crown light.
- Plaza (NW, Mission side): stone paving, sky pool, steel ring sculpture, bamboo trees.

### 2.8 Palette

`Toy_glassl`, `Toy_ink`, `Toy_glassd`, `Toy_roofd`, `Toy_steel`, `Toy_stone`, `Toy_sky`, `Toy_leaf(d)`, `Toy_rust`; glow `Toy_sand_Glow`, `Toy_white_Glow`.

### 2.9 Roof

Visible deck and plant inside an open black frame - not blank from above.

### 2.11 Triangle budget

4,832 tris (body 4,004, night glow 828) against the batch cap of 5,000.

### 2.12 Draft manifest entry

```json
{"id": "560-mission-street", "file": "560-mission-street.glb", "anchor": [-122.3995478, 37.7888279], "targetHeightM": 128.02, "cat": 3, "name": "JPMorgan Chase Building (560 Mission Street)", "estimated": false, "dims": [85.1472, 84.5771, 128.02], "tris": 4832, "loadRadius": 3841}
```

### 2.13 Integration notes

Case B: registry entry in `pipeline/lib/landmarks.mjs`, exclusion of OSM way 79377216 from the baked tiles, batch re-bake.
`dims` is the axis-aligned box of the rotated plan plus apron/plinth. Load radius 3841 m (max(2500, 30 x height)).
Check at bake time that the exclusion clears only this footprint.

### 2.15 Open risks

- Plaza side and ledge height are inferred.
- The plaza apron enlarges the bbox; the anchor shifts ~8 m to keep it centred (tk.run handles this).
