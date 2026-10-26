# 45 Fremont Street — SF-SIM asset plan

A 34-storey cream office tower (SOM, 1978) between Market and Mission, often called
the Bechtel Building. It is a plain chamfered-corner slab wrapped in continuous cream
spandrels and dark ribbon windows: the most strongly *horizontal* tower in the
Transbay cluster, which is exactly what makes it read in the miniature.

**Deliverable:** `artifacts/45-fremont/`. Part 1 is the task prompt, Part 2 the dossier.

| | |
|---|---|
| Manifest id | `45-fremont` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.3971490, 37.7912310` (OSM OBB centre via `tk.run`) |
| Target height | **145.0 m** roof (Wikipedia 476 ft, published); 2010 LiDAR max 146.02 m, majority 135.42 m (measured) |
| Footprint | OSM way 32946535: OBB 46.8 × 37.5 m, 1,746 m², 5 nodes, long axis bearing 134.4° |
| Triangle cap | 27,000 (built: 4,064) |
| Category | `3` (Office — `CAT.office` in `app/src/props.js`) |

---

## Part 1 — Task prompt

````markdown
# Create the 45 Fremont Street GLB for SF-SIM

Work in artifacts/45-fremont/. Read AGENTS.md, docs/styles/miniature-toy.md and
tools/landmark-kit/toykit.py first; Part 2 of this plan is your research start.

Must capture: a chamfered-corner slab on the OSM heading; strong cream/dark
horizontal striping, one proud cream spandrel per floor; a cream roof band and a
designed roof (parapet, deck, plant); a recessed glass base behind cream columns,
street trees on Fremont (SW).

Contract: binary GLB, metres, +Y = true north, origin at base centre, min Z 0, crest
exactly 145.0 m, flat Toy_* materials, `_Glow` only as outward skins, no degenerate
triangles, <= 27,000 tris (aim for under 6,000). Build with
`tk.run(SLUG, build, HERE, (-122.397149, 37.791231), 145.0)`.

Run build -> kit validate.py (--height 145 --anchor <tk.run anchor>, "all checks
pass") -> kit render.py. Write REFERENCE.md and REPORT.md. Do not edit the manifest,
landmarks.mjs or app code.
````

---

## Part 2 — Research and design dossier

### 2.1 Verified facts

| Fact | Value | Label |
|---|---|---|
| Roof height | 145 m (476 ft) | published (Wikipedia, CTBUH 12690) |
| LiDAR (2010) | max 146.02 m, majority 135.42 m, median 132.14 m | measured (DataSF 201006.0001422) |
| Floors / year / architect | 34 / 1978 / SOM | published |
| Footprint | OBB 46.8 × 37.5 m, 1,746 m², 5 nodes | measured (OSM) |
| Heading | long axis 134.4° (along Fremont St) | measured (OSM) |
| OSM `height` | 149 | unsourced tag; not used |
| Chamfered / rounded corners | ~4.5 m legs | inferred (photo shows softened corners) |

The LiDAR majority (135 m) sits well under the published roof; the most common return
is likely a lower roof level inside a parapet/plant zone. The published 145 m is used
for the crest; the LiDAR max (146 m) confirms it.

### 2.2 Sources

- OSM way 32946535 — https://www.openstreetmap.org/way/32946535
- DataSF footprints + 2010 LiDAR, `sf16_bldgid` 201006.0001422 — https://data.sf.gov/resource/ynuv-fyni
- Wikipedia — https://en.wikipedia.org/wiki/45_Fremont_Street
- Commons photo (Wikipedia lead image) — https://commons.wikimedia.org/wiki/File:45_Fremont_Center,_San_Francisco.jpg

### 2.3 Orientation

Long axis 134.4° (NW–SE, along Fremont). Model yaw = 90 − 134.4 = −44.4°; +Y = true
north. Local −y faces ≈ 225° = **Fremont St (SW)**, the address front; local +x faces
SE toward Mission; NW toward Market; NE toward 50 Beale (Bechtel).

### 2.4 What each side shows

All four faces share the same ribbon-window skin in the photo (two faces seen; the
others **inferred**). The photo also shows a louvred mechanical band about two-thirds
up; it is not modelled (it barely reads from the aerial camera). Base: glazed lobby
behind columns (**inferred** from typical SOM base; not in the photo).

### 2.5 Recognition cues

1. Bold cream/dark horizontal stripes, one per floor.
2. Softened (chamfered) corners — the stripes wrap round them.
3. A plain flat top with a cream band.

### 2.7 Massing recipe

- Plan `tk.chamfer_rect(45.5, 36.5, 4.5)` on yaw −44.4°.
- Base 0–8 m: `Toy_glass` core inset 2.5 m, `Toy_sand_Glow` ring, cream columns every 7 m.
- Shaft 8–142 m: `tk.shaft` with 33 whole storeys (4.06 m), `Toy_glassd` with 2.3 m
  `Toy_cream` spandrels 0.45 m proud; scattered lit panes.
- Roof band 142–144.4 m in `Toy_cream`; `tk.roof_kit` (parapet, deck, plant). `tk.run`
  scales Z by 0.979 to land the plant crest at 145 m.
- Stone apron, three street trees on Fremont.

### 2.8 Palette

`Toy_cream`, `Toy_glassd`, `Toy_glass`, `Toy_trim`, `Toy_roofd`, `Toy_steel`, `Toy_stone`,
`Toy_leaf`, `Toy_leafd`, `Toy_rust`; glow `Toy_sand_Glow`. All core palette.

### 2.9 Roof

Parapet, dark deck and one tidy plant cluster — a designed but quiet roof.

### 2.11 Triangle budget

4,064 tris (body 3,096, glow 968). Lean; the loft is the bulk.

### 2.12 Draft manifest entry

```json
{
  "id": "45-fremont",
  "file": "45-fremont.glb",
  "anchor": [-122.397149, 37.791231],
  "targetHeightM": 145,
  "cat": 3,
  "name": "45 Fremont Street",
  "estimated": false,
  "dims": [57.7729, 57.6396, 145.0],
  "tris": 4064
}
```

```js
{ id: '45Fremont', name: '45 Fremont Street', lon: -122.397149, lat: 37.791231,
  height: 145, exclude: 24, camera: { distance: 460, yaw: 220, pitch: 20 } }
```

### 2.13 Integration notes

Case B: registry entry, exclusion, batch re-bake. Neighbours are close: 350 Mission's
centroid is ≈ 55 m SE, 333 Market ≈ 81 m N, and 50 Beale abuts on the NE. A ~24 m
radius clears this footprint only — confirm at bake time. Load radius: none.

### 2.15 Open risks

- Corner chamfer size is read from one photo.
- The mid-height louvred mechanical band is omitted.
- The 0.979 Z normalization slightly compresses the storeys (≈ 3 m over 145 m); harmless.
