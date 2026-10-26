# 100 Montgomery Street (Equitable Life Building) — SF-SIM asset plan

A 25-storey slab (William Peugh / Irwin Clavan, 1955), one of San Francisco's first post-war office towers: broad white marble piers in a steady vertical rhythm between bays of aluminium-framed windows, solid marble corners, a two-storey marble base and a flat roof.

**Deliverable:** `artifacts/100-montgomery-street/` (built in the Financial District batch, stages 1–2). Part 1 is the task prompt, Part 2 the dossier.

| | |
|---|---|
| Manifest id | `100-montgomery-street` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.4018706, 37.7903435` (OSM OBB centre, recentred by `tk.run`) |
| Target height | **107.9 m** — 107.9 m crest = 354 ft (published); taken as the top including the plant penthouse |
| Footprint | OSM way 132125166: OBB 52 x 33.7 m, 1,745 m², 6 nodes, long-axis bearing 81.7° |
| Triangle cap | 5,000 (batch cap for towers ≥ 60 m; built: 2,156) |
| Category | `3` (Office — `CAT.office` in `app/src/props.js`) |

---

## Part 1 — Task prompt

````markdown
# Create the 100 Montgomery Street (Equitable Life Building) GLB for SF-SIM

Work in artifacts/100-montgomery-street/. Read AGENTS.md, docs/styles/miniature-toy.md and
tools/landmark-kit/toykit.py first; Part 2 of this plan is your research start.

Must capture the ranked cues in 2.5. Contract: binary GLB, metres, +Y = true north, origin at base centre, min Z 0, crest exactly 107.9 m,
flat Toy_* materials, `_Glow` only as outward skins, no degenerate triangles, <= 5,000 tris.
Build with `tk.run(SLUG, build, HERE, (-122.4018706, 37.7903435), 107.9)`; run build ->
validate_100_montgomery_street.py ("all checks pass") -> render_100_montgomery_street.py -- --samples 16; write REFERENCE.md and REPORT.md.
Do not edit the manifest, landmarks.mjs or app code.
````

---

## Part 2 — Research and design dossier

### 2.1 Verified facts

| Fact | Value | Label |
|---|---|---|
| Height | 107.9 m (354 ft) | published (Wikipedia); OSM `height=108` |
| Floors / year / architects | 25 / 1955 / Peugh, Clavan; renovation Robert A.M. Stern | published |
| Facade | white marble against aluminium window framing | published |
| 2010 LiDAR | 101.1 m | measured (main roof; consistent with the 104.3 m parapet + plant) |
| Main parapet 104.3 m, penthouse to 107.9 m |  | estimated |

### 2.2 Sources

- OSM way 132125166 — https://www.openstreetmap.org/way/132125166 (footprint, tags: `height=108`, `building:levels=25`)
- Wikipedia — https://en.wikipedia.org/wiki/100_Montgomery_Street
- Commons photo (the Wikipedia lead photo, looking up at the Montgomery x Sutter corner) — https://commons.wikimedia.org/wiki/File:100_Montgomery_Street.jpg
- DataSF 2010 LiDAR building heights — https://data.sf.gov/resource/ynuv-fyni (`hgt_max` 101.1 m)

### 2.3 Orientation

Long axis on bearing 81.7 deg: the long faces look N and S (**Sutter St** on the N, per the OSM address tag), the short faces E and W (**Montgomery St** side **inferred** E).

### 2.4 What each side shows

- Photographed corner: marble piers + window bays on both faces, marble base.
- Other faces: same rhythm assumed (**inferred**).

### 2.5 Recognition cues (ranked)

1. White marble slab with broad vertical piers.
2. Silvery window bays between them.
3. Flat, plain roofline.

### 2.7 Massing recipe

- Plan `tk.rect(51.8, 33.4)` on yaw 8.3 deg.
- Base 0-9 m `Toy_white` with two rows of big punched windows.
- Shaft 9-103.1 m: `tk.shaft` 23 storeys, `Toy_glassg` with thin `Toy_steel` spandrels and 2 m `Toy_white` piers every 6.4 m.
- Marble parapet ring, dark deck, `Toy_stone` penthouse 22 x 14 m to the crest, small plant cluster.

### 2.8 Palette

`Toy_white`, `Toy_glassg`, `Toy_steel`, `Toy_glassd`, `Toy_stone`, `Toy_roofd`; glow `Toy_sand_Glow`, `Toy_white_Glow`.

### 2.9 Roof

Parapet ring round a dark deck with a pale penthouse and plant cluster.

### 2.11 Triangle budget

2,156 tris (body 1,708, night glow 448) against the batch cap of 5,000.

### 2.12 Draft manifest entry

```json
{"id": "100-montgomery-street", "file": "100-montgomery-street.glb", "anchor": [-122.4018706, 37.7903435], "targetHeightM": 107.9, "cat": 3, "name": "100 Montgomery Street (Equitable Life Building)", "estimated": false, "dims": [61.7195, 46.1684, 107.9], "tris": 2156, "loadRadius": 3237}
```

### 2.13 Integration notes

Case B: registry entry in `pipeline/lib/landmarks.mjs`, exclusion of OSM way 132125166 from the baked tiles, batch re-bake.
`dims` is the axis-aligned box of the rotated plan plus apron/plinth. Load radius 3237 m (max(2500, 30 x height)).
Check at bake time that the exclusion clears only this footprint.

### 2.15 Open risks

- Whether 354 ft is the main roof or the penthouse top is unclear; crest chosen = 107.9 m.
- Street-face naming is inferred from the OSM address and the photo.
