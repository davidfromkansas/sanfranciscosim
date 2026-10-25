# Two Embarcadero Center — SF-SIM asset plan

A 30-storey pale precast slab (John Portman & Associates, 1974), the second Embarcadero Center tower: long faces N and S, short ends broken into vertical strips that step down, standing on the concrete podium over Sacramento St.

**Deliverable:** `artifacts/embarcadero-center-2/` (built in the Financial District batch, stages 1–2). Part 1 is the task prompt, Part 2 the dossier.

| | |
|---|---|
| Manifest id | `embarcadero-center-2` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.3985117, 37.7949992` (OSM OBB centre, recentred by `tk.run`) |
| Target height | **126.0 m** — 126.0 m crest (published, Wikipedia) |
| Footprint | OSM way 32612520: OBB 79.1 x 33.7 m, 2,428 m², 19 nodes, long-axis bearing 80.8° |
| Triangle cap | 5,000 (batch cap for towers ≥ 60 m; built: 4,316) |
| Category | `3` (Office — `CAT.office` in `app/src/props.js`) |

---

## Part 1 — Task prompt

````markdown
# Create the Two Embarcadero Center GLB for SF-SIM

Work in artifacts/embarcadero-center-2/. Read AGENTS.md, docs/styles/miniature-toy.md and
tools/landmark-kit/toykit.py first; Part 2 of this plan is your research start.

Must capture the ranked cues in 2.5. Contract: binary GLB, metres, +Y = true north, origin at base centre, min Z 0, crest exactly 126.0 m,
flat Toy_* materials, `_Glow` only as outward skins, no degenerate triangles, <= 5,000 tris.
Build with `tk.run(SLUG, build, HERE, (-122.3985145, 37.7949899), 126.0)`; run build ->
validate_embarcadero_center_2.py ("all checks pass") -> render_embarcadero_center_2.py -- --samples 16; write REFERENCE.md and REPORT.md.
Do not edit the manifest, landmarks.mjs or app code.
````

---

## Part 2 — Research and design dossier

### 2.1 Verified facts

| Fact | Value | Label |
|---|---|---|
| Height | 126 m | published (Wikipedia) |
| Floors / year / architect | 30 / 1974 / John Portman & Associates | published |
| OSM / 2010 LiDAR | `height=130` / 130.0 m | OSM; LiDAR equals the OSM tag exactly - treated as suspect |
| End strips | W: 5 strips (33.3 / 39.6 / 33.9 / 31.4 / 26.7 m); E: 3 strips (39.2 / 35.6 / 39.5 m) | measured (OSM) |
| Step-downs 0 / -5 / -10 storeys; podium 10 m; main roof 123 m + penthouse |  | inferred (photo) / estimated |

### 2.2 Sources

- OSM way 32612520 — https://www.openstreetmap.org/way/32612520 (footprint, tags: `height=130`, `building:levels=31`)
- Wikipedia — https://en.wikipedia.org/wiki/Two_Embarcadero_Center
- Commons photo (the Wikipedia lead photo, from Sacramento St (south side), showing the strip end) — https://commons.wikimedia.org/wiki/File:Two_Embarcadero_Center.jpg
- DataSF 2010 LiDAR building heights — https://data.sf.gov/resource/ynuv-fyni (`hgt_max` 130 m)

### 2.3 Orientation

Long axis on bearing 80.8 deg: long faces N (Clay side) and S (Sacramento St); strip ends E and W.

### 2.4 What each side shows

- N and S: the long blunt faces - fine dark slots in pale precast (photo).
- E and W: the stepped strip ends (photo shows one end; the other is from the OSM polygon, **inferred** to match).

### 2.5 Recognition cues (ranked)

1. Long pale slab, 'blunt cliff' from N/S.
2. Stepped strip ends - 'spiked outcrops' from E/W.
3. Fine dark vertical window-slot grain.
4. Sits on the Embarcadero Center podium.

### 2.7 Massing recipe

- Same recipe and helper as Three Embarcadero Center, with this polygon's strips.
- Strip ranks clamp at the lowest tier, so the 5th west strip still rises to 113 m.
- Concrete podium 0-10 m with lit shopfronts and a hedge edge; penthouse to 126 m.

### 2.8 Palette

`Toy_sand`, `Toy_cream`, `Toy_glass`, `Toy_concrete`, `Toy_glassd`, `Toy_steel`, `Toy_leafd`, `Toy_stone`; glow `Toy_sand_Glow`, `Toy_glassl_Glow`.

### 2.9 Roof

Pale steel deck, one cream penthouse and a plant cluster; lower step decks at the ends.

### 2.11 Triangle budget

4,316 tris (body 3,326, night glow 990) against the batch cap of 5,000.

### 2.12 Draft manifest entry

```json
{"id": "embarcadero-center-2", "file": "embarcadero-center-2.glb", "anchor": [-122.3985117, 37.7949992], "targetHeightM": 126.0, "cat": 3, "name": "Two Embarcadero Center", "estimated": false, "dims": [96.0272, 57.6816, 126.0], "tris": 4316, "loadRadius": 3780}
```

### 2.13 Integration notes

Case B: registry entry in `pipeline/lib/landmarks.mjs`, exclusion of OSM way 32612520 from the baked tiles, batch re-bake.
`dims` is the axis-aligned box of the rotated plan plus apron/plinth. Load radius 3780 m (max(2500, 30 x height)).
Check at bake time that the exclusion clears only this footprint.

### 2.15 Open risks

- Step heights are inferred from one photo.
- OSM/LiDAR give 130 m vs the published 126 m.
