# 333 Market Street — SF-SIM asset plan

A 33-storey office tower (Gin Wong Associates, 1979) on Market between Fremont and
Beale. Tall pale-bronze piers run the full height with dark glass between, so the
tower reads as a column of fine vertical pinstripes; its corners are serrated into a
small stair of re-entrant steps, which OSM traces in detail.

**Deliverable:** `artifacts/333-market/`. Part 1 is the task prompt, Part 2 the dossier.

| | |
|---|---|
| Manifest id | `333-market` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.3974030, 37.7919380` (OSM OBB centre via `tk.run`) |
| Target height | **144.0 m** roof (Wikipedia 472 ft, published); 2010 LiDAR max 146.07 m, majority 135.63 m (measured) |
| Footprint | OSM way 288505729: OBB 48.7 × 39.6 m, 1,806 m², 114 nodes (serrated corners), long axis bearing 45.3° |
| Triangle cap | 27,000 (built: 10,990) |
| Category | `3` (Office — `CAT.office` in `app/src/props.js`) |

---

## Part 1 — Task prompt

````markdown
# Create the 333 Market Street GLB for SF-SIM

Work in artifacts/333-market/. Read AGENTS.md, docs/styles/miniature-toy.md and
tools/landmark-kit/toykit.py first; Part 2 of this plan is your research start.

Must capture: a rectangle with all four corners cut into a three-step stair, on the
OSM heading; full-height pale-bronze piers every ~2.8 m over dark glass; a granite-
columned recessed base; a bronze-toned cap and a designed roof.

Contract: binary GLB, metres, +Y = true north, origin at base centre, min Z 0, crest
exactly 144.0 m, flat Toy_* materials, `_Glow` only as outward skins, no degenerate
triangles, <= 27,000 tris (aim for under 12,000). Build with
`tk.run(SLUG, build, HERE, (-122.397403, 37.791938), 144.0)`.

Run build -> kit validate.py (--height 144 --anchor <tk.run anchor>, "all checks
pass") -> kit render.py. Write REFERENCE.md and REPORT.md. Do not edit the manifest,
landmarks.mjs or app code.
````

---

## Part 2 — Research and design dossier

### 2.1 Verified facts

| Fact | Value | Label |
|---|---|---|
| Roof height | 144 m (472 ft) | published (Wikipedia) |
| LiDAR (2010) | max 146.07 m, majority 135.63 m, median 135.58 m | measured (DataSF 201006.0001373) |
| Floors / year / architect | 33 / 1979 / Gin Wong Associates | published |
| Footprint | OBB 48.7 × 39.6 m, 1,806 m², 114 nodes | measured (OSM) |
| Heading | long axis 45.3° (along Market St) | measured (OSM) |
| OSM `height` | 149 m | unsourced tag; not used |
| Corner stair 3 steps × 2.6 m | | inferred (OSM outline + photo) |

### 2.2 Sources

- OSM way 288505729 — https://www.openstreetmap.org/way/288505729
- DataSF footprints + 2010 LiDAR, `sf16_bldgid` 201006.0001373 — https://data.sf.gov/resource/ynuv-fyni
- Wikipedia — https://en.wikipedia.org/wiki/333_Market_Street
- Commons photo (Wikipedia lead image) — https://commons.wikimedia.org/wiki/File:333_Market_Street_2021.jpg

### 2.3 Orientation

Long axis 45.3° (NE–SW, along Market). Model yaw = 45.3° (local +x bearing 44.7°);
+Y = true north. Local +y faces ≈ 315° = **Market St (NW, long face)**; NE short face
toward Beale, SW short face toward Fremont; SE long face toward Mission (mid-block).

### 2.4 What each side shows

The photo (from Market at Beale) shows two faces: continuous pale piers, dark glass,
serrated corners, a recessed base. The other two faces are assumed identical
(**inferred**). Roof not photographed (**inferred** flat with plant).

### 2.5 Recognition cues

1. Fine full-height vertical pinstripes (pale piers over dark glass).
2. Serrated, stepped corners.
3. A plain flat top.

### 2.7 Massing recipe

- Plan: `sawtooth(46, 37, k=3, n=2.6)` (rectangle with stair-stepped corners) on yaw 45.3°.
- Base 0–9 m: `Toy_glassd` inset 2 m, `Toy_sand_Glow` ring, granite columns every 5 m.
- Shaft 9–142 m: `tk.shaft`, `Toy_glassd` with thin `Toy_bronze` floor lines and
  `Toy_terracotta` piers every 2.8 m (0.85 × 0.55 m); lit panes aligned to the pier bays.
- Cap 142–143.2 m `Toy_terracotta`; `tk.roof_kit` (parapet, deck, plant). `tk.run`
  scales Z by 0.985 to land the plant crest at 144 m.
- Stone apron. No trees (Market sidewalk trees belong to the street kit).

### 2.8 Palette

`Toy_terracotta` (pale bronze-tan piers), `Toy_bronze`, `Toy_glassd`, `Toy_granite`,
`Toy_trim`, `Toy_roofd`, `Toy_steel`, `Toy_stone`; glow `Toy_sand_Glow`. All core palette.

### 2.9 Roof

Parapet following the serrated outline, dark deck, one plant cluster.

### 2.11 Triangle budget

10,990 tris (body 9,776, glow 1,214). The serrated plan multiplies every loft ring and
pier row; piers were widened from 1.9 m to 2.8 m spacing to keep it lean.

### 2.12 Draft manifest entry

```json
{
  "id": "333-market",
  "file": "333-market.glb",
  "anchor": [-122.397403, 37.791938],
  "targetHeightM": 144,
  "cat": 3,
  "name": "333 Market Street",
  "estimated": false,
  "dims": [59.6849, 59.7516, 144.0],
  "tris": 10990
}
```

```js
{ id: '333Market', name: '333 Market Street', lon: -122.397403, lat: 37.791938,
  height: 144, exclude: 25, camera: { distance: 460, yaw: 315, pitch: 20 } }
```

### 2.13 Integration notes

Case B: registry entry, exclusion, batch re-bake. 45 Fremont's centroid is ≈ 81 m SSE;
the older Market St buildings either side are much closer — confirm at bake time that
a ~25 m radius clears only this footprint. Load radius: none.

### 2.15 Open risks

- Pier colour: the photo reads pale bronze/tan; `Toy_terracotta` may look warmer than
  the real cladding — compare the renders.
- Step count/size of the serrated corners is simplified from the 114-node OSM outline.
- The 0.985 Z normalization slightly compresses the storeys; harmless.
