# 60 Spear Street ("The Spear") — SF-SIM asset plan

A 13-storey office block on Spear Street between Market and Mission, sharing its block
with the Federal Reserve Bank. Square to the street grid, a stone-gridded shaft over a
glazed base, crowned by a set-back glass top storey. Massing and height are measured;
**the facade is inferred** — no Wikipedia article and no photo could be obtained in
this batch (Commons searches were rate-limited, HTTP 429).

**Deliverable:** `artifacts/60-spear/`. Part 1 is the task prompt, Part 2 the dossier.

| | |
|---|---|
| Manifest id | `60-spear` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.3945850, 37.7925660` (OSM OBB centre via `tk.run`) |
| Target height | **57.9 m** crest (DataSF 2010 LiDAR max 57.93 m, measured); roof plane 55.4 m (LiDAR majority) |
| Footprint | OSM way 32863010: OBB 40.4 × 31.6 m, 1,271 m², 4 nodes, bearing 134.8° |
| Triangle cap | 27,000 (built: 2,238) |
| Category | `3` (Office — `CAT.office` in `app/src/props.js`) |

---

## Part 1 — Task prompt

````markdown
# Create the 60 Spear Street GLB for SF-SIM

Work in artifacts/60-spear/. Read AGENTS.md, docs/styles/miniature-toy.md and
tools/landmark-kit/toykit.py first; Part 2 of this plan is your research start.

Must capture: a 39.5 × 31 m block on the OSM heading; a glazed base behind stone
piers; a stone-gridded shaft; a set-back glazed top storey with a terrace ring; a
designed roof. FIRST try to find a photo (Street View / Commons "60 Spear Street") —
the facade in this plan is inferred; replace it if a photo contradicts it.

Contract: binary GLB, metres, +Y = true north, origin at base centre, min Z 0, crest
exactly 57.9 m, flat Toy_* materials, `_Glow` only as outward skins, no degenerate
triangles, <= 27,000 tris. Build with
`tk.run(SLUG, build, HERE, (-122.394585, 37.792566), 57.9)`.

Run build -> kit validate.py (--height 57.9 --anchor <tk.run anchor>, "all checks
pass") -> kit render.py. Write REFERENCE.md and REPORT.md. Do not edit the manifest,
landmarks.mjs or app code.
````

---

## Part 2 — Research and design dossier

### 2.1 Verified facts

| Fact | Value | Label |
|---|---|---|
| Crest | 57.93 m | measured (DataSF LiDAR max, `sf16_bldgid` 201006.0002083) |
| Roof plane | 55.38 m | measured (LiDAR majority) |
| Floors | 13 | OSM `building:levels` (unsourced tag) |
| OSM `height` | 60 m | unsourced tag; not used |
| Footprint | OBB 40.4 × 31.6 m, 1,271 m², 4 nodes, bearing 134.8° | measured (OSM) |
| Name | "The Spear" | OSM `name` |
| Year / architect | unknown | — |
| Stone grid facade, glazed base, set-back glass top storey | | **inferred** (no photo) |

### 2.2 Sources

- OSM way 32863010 — https://www.openstreetmap.org/way/32863010
- DataSF footprints + 2010 LiDAR, `sf16_bldgid` 201006.0002083 (MBLR SF3712023) — https://data.sf.gov/resource/ynuv-fyni
- Wikipedia — no article ("60 Spear Street" is missing)
- Commons — none obtained (searches returned HTTP 429)

### 2.3 Orientation

Long axis bearing 134.8°, so the model yaw is −44.8° (local +x toward SE, +y toward
NE). +Y = true north. **NE face = Spear St** (long face); SE short face toward
Mission; NW short face toward the Federal Reserve Bank's block interior; SW face
mid-block.

### 2.4 What each side shows

All **inferred**: the four sides share one skin (glazed base behind piers, banded
stone grid with fins, set-back glass top). The LiDAR gap of 2.5 m between majority and
max reads as rooftop plant, which the roof carries.

### 2.5 Recognition cues

1. A compact, regular mid-rise block square to Spear St.
2. The set-back glass top storey with a terrace ring.
3. Stone grid over a dark glazed base.

### 2.7 Massing recipe

- Plan 39.5 × 31 m rectangle on yaw −44.8°.
- Base 0–6 m: `Toy_glass` inset 1.5 m, `Toy_sand_Glow` ring, `Toy_stone` piers every 4 m.
- Shaft 6–51.2 m: `tk.shaft`, 11 storeys of `Toy_glass` with `Toy_stone` bands and stone fins every 4 m.
- Terrace slab 51.2–51.8 m; `Toy_glassl` top storey inset 2.2 m to 55.4 m with a lit ring; parapet; two terrace trees.
- Roof plant to the 57.9 m crest; plaza apron with three street trees on the Spear St (NE) sidewalk.

### 2.8 Palette

`Toy_stone`, `Toy_glass`, `Toy_glassl`, `Toy_trim`, `Toy_roofd`, `Toy_steel`,
`Toy_leaf`, `Toy_leafd`; glow `Toy_sand_Glow`. Off-palette: `Toy_leaf`, `Toy_leafd`.

### 2.9 Roof

Dark roof over the glass top storey, trim parapet, one plant cluster to the crest.

### 2.11 Triangle budget

2,238 tris (body 1,976, glow 262). Deliberately lean — a background mid-rise.

### 2.12 Draft manifest entry

```json
{
  "id": "60-spear",
  "file": "60-spear.glb",
  "anchor": [-122.394585, 37.792566],
  "targetHeightM": 57.9,
  "cat": 3,
  "name": "60 Spear Street",
  "estimated": false,
  "dims": [58.216, 58.174, 57.9],
  "tris": 2238
}
```

`estimated: false` refers to the height (measured); the facade is inferred — say so in
the card text if the app shows one.

### 2.13 Integration notes

Case B: registry entry, exclusion, batch re-bake. Same assessor block (3712) as the
Federal Reserve Bank (`federal-reserve`, anchor ~95 m WNW); the two exclusions must
not overlap each other's rings. A small radius (~15–20 m) should catch only this
4-node footprint — verify against bake inputs. Default load radius 2,500 m.

### 2.15 Open risks

- **Facade entirely inferred.** A photo may show something quite different (e.g. a
  precast or brick 1920s–80s block). Low cost to redo: the build script is ~50 lines.
- Year and architect unknown.
- Set-back top storey is inferred from the 2.5 m LiDAR max/majority gap, which could
  equally be plain rooftop plant.
