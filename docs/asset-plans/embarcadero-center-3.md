# Three Embarcadero Center — SF-SIM asset plan

A 31-storey pale precast slab (John Portman & Associates, 1977), part of the Embarcadero Center: long faces N and S, and short ends that split into vertical strips whose tops step down - the same family as Four Embarcadero Center, already a landmark.

**Deliverable:** `artifacts/embarcadero-center-3/` (built in the Financial District batch, stages 1–2). Part 1 is the task prompt, Part 2 the dossier.

| | |
|---|---|
| Manifest id | `embarcadero-center-3` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.3973647, 37.7951182` (OSM OBB centre, recentred by `tk.run`) |
| Target height | **126.0 m** — 126.0 m crest (published, Wikipedia) |
| Footprint | OSM way 32612538: OBB 78.9 x 34.6 m, 2,529 m², 17 nodes, long-axis bearing 81.4° |
| Triangle cap | 5,000 (batch cap for towers ≥ 60 m; built: 4,204) |
| Category | `3` (Office — `CAT.office` in `app/src/props.js`) |

---

## Part 1 — Task prompt

````markdown
# Create the Three Embarcadero Center GLB for SF-SIM

Work in artifacts/embarcadero-center-3/. Read AGENTS.md, docs/styles/miniature-toy.md and
tools/landmark-kit/toykit.py first; Part 2 of this plan is your research start.

Must capture the ranked cues in 2.5. Contract: binary GLB, metres, +Y = true north, origin at base centre, min Z 0, crest exactly 126.0 m,
flat Toy_* materials, `_Glow` only as outward skins, no degenerate triangles, <= 5,000 tris.
Build with `tk.run(SLUG, build, HERE, (-122.3973532, 37.7951239), 126.0)`; run build ->
validate_embarcadero_center_3.py ("all checks pass") -> render_embarcadero_center_3.py -- --samples 16; write REFERENCE.md and REPORT.md.
Do not edit the manifest, landmarks.mjs or app code.
````

---

## Part 2 — Research and design dossier

### 2.1 Verified facts

| Fact | Value | Label |
|---|---|---|
| Height | 126 m | published (Wikipedia) |
| Floors / year / architect | 31 / 1977 / John Portman & Associates | published |
| OSM / 2010 LiDAR | `height=130` / 130.0 m | OSM; the LiDAR value equals the OSM tag exactly - treated as suspect |
| End strips | W: 3 strips (extents 39.1 / 36.5 / 39.5 m); E: 4 strips (28.5 / 33.1 / 39.5 / 31.1 m) | measured (OSM) |
| Step-downs 0 / -5 / -10 storeys; podium 10 m; main roof 123 m + penthouse |  | inferred (photo) / estimated |

### 2.2 Sources

- OSM way 32612538 — https://www.openstreetmap.org/way/32612538 (footprint, tags: `height=130`, `building:levels=31`)
- Wikipedia — https://en.wikipedia.org/wiki/Three_Embarcadero_Center
- Commons photo (the Wikipedia lead photo, from the north-west (Sue Bierman Park side)) — https://commons.wikimedia.org/wiki/File:Three_Embarcadero_Center_front.jpg
- DataSF 2010 LiDAR building heights — https://data.sf.gov/resource/ynuv-fyni (`hgt_max` 130 m)

### 2.3 Orientation

Long axis on bearing 81.4 deg: long faces N (Clay St / Sue Bierman Park) and S (podium plaza); strip ends E and W.

### 2.4 What each side shows

- N and S: the long blunt faces - fine dark slots in pale precast (photo).
- E and W: the stepped strip ends (photo shows one end; the other is from the OSM polygon, **inferred** to match).

### 2.5 Recognition cues (ranked)

1. Long pale slab, 'blunt cliff' from N/S.
2. Stepped strip ends - 'spiked outcrops' from E/W.
3. Fine dark vertical window-slot grain.
4. Sits on the Embarcadero Center podium.

### 2.7 Massing recipe

- Strips across the short ends measured off the OSM polygon (see `WEST`/`EAST` in the script).
- Three tiers: all strips to 123 - 10 storeys; spine + second strip to -5 storeys; spine and core to 123 m.
- Each tier: `Toy_sand` prism, dark `Toy_glass` slot rows (1.55 m pitch, five-storey groups), scattered lit panes.
- Concrete podium 0-10 m (offset 4 m) with lit shopfronts and a hedge; cream cap ring, deck, penthouse to 126 m.

### 2.8 Palette

`Toy_sand`, `Toy_cream`, `Toy_glass`, `Toy_concrete`, `Toy_glassd`, `Toy_steel`, `Toy_leafd`, `Toy_stone`; glow `Toy_sand_Glow`, `Toy_glassl_Glow`.

### 2.9 Roof

Pale steel deck, one cream penthouse and a plant cluster; lower step decks at the ends.

### 2.11 Triangle budget

4,204 tris (body 3,206, night glow 998) against the batch cap of 5,000.

### 2.12 Draft manifest entry

```json
{"id": "embarcadero-center-3", "file": "embarcadero-center-3.glb", "anchor": [-122.3973647, 37.7951182], "targetHeightM": 126.0, "cat": 3, "name": "Three Embarcadero Center", "estimated": false, "dims": [94.0973, 58.3978, 126.0], "tris": 4204, "loadRadius": 3780}
```

### 2.13 Integration notes

Case B: registry entry in `pipeline/lib/landmarks.mjs`, exclusion of OSM way 32612538 from the baked tiles, batch re-bake.
`dims` is the axis-aligned box of the rotated plan plus apron/plinth. Load radius 3780 m (max(2500, 30 x height)).
Check at bake time that the exclusion clears only this footprint.

### 2.15 Open risks

- Step heights are read from the photo, not measured.
- OSM/LiDAR give 130 m vs the published 126 m.
