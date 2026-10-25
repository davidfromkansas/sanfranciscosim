# 100 First Plaza (100 First Street) — SF-SIM asset plan

A 27-storey postmodern office tower (SOM, 1988; also called the Delta Dental / Andersen
Tax Tower) at First Street between Mission and Howard. Pink-cream stone with deep
blue-glass notched corners, it climbs in setbacks to a crown of glass roofs and a 19 m
spire, over a three-storey podium that runs ~40 m south-west of the tower.

**Deliverable:** `artifacts/100-first/`. Part 1 is the task prompt, Part 2 the dossier.

| | |
|---|---|
| Manifest id | `100-first` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.3977206, 37.7891952` (bbox centre via `tk.run`; authored around the tower part's OBB centre) |
| Target height | **136.25 m** spire tip (Wikipedia/CTBUH antenna-spire, published); roof 116 m (published; LiDAR majority 115.90 m, measured) |
| Footprint | OSM way 91626348 (podium, 3 levels): OBB 78.5 × 49.4 m, 3,518 m², bearing 45.2°; tower part 1410929341: OBB 35.3 × 30.4 m |
| Triangle cap | 27,000 (built: 4,800) |
| Category | `3` (Office — `CAT.office` in `app/src/props.js`) |

---

## Part 1 — Task prompt

````markdown
# Create the 100 First Plaza GLB for SF-SIM

Work in artifacts/100-first/. Read AGENTS.md, docs/styles/miniature-toy.md and
tools/landmark-kit/toykit.py first; Part 2 of this plan is your research start.

Must capture: a notched-corner square tower on the OSM part heading, cream stone with
blue-glass notches; three setbacks; a crown of blue glass roofs and a thin spire; the
three-storey podium on the full OSM outline with a planted roof.

Contract: binary GLB, metres, +Y = true north, origin at base centre, min Z 0, crest
exactly 136.25 m, flat Toy_* materials, `_Glow` only as outward skins, no degenerate
triangles, <= 27,000 tris. Do not bevel concave (notched) plans: the bevelled caps
render black. Build with `tk.run(SLUG, build, HERE, (-122.3975827, 37.7892919), 136.25)`.

Run build -> kit validate.py (--height 136.25 --anchor <tk.run anchor>, "all checks
pass") -> kit render.py. Write REFERENCE.md and REPORT.md. Do not edit the manifest,
landmarks.mjs or app code.
````

---

## Part 2 — Research and design dossier

### 2.1 Verified facts

| Fact | Value | Label |
|---|---|---|
| Spire tip | 136.25 m (446 ft); spire 19 m (62 ft) | published (Wikipedia, CTBUH) |
| Roof | 116 m | published; LiDAR majority 115.90 m (measured, `sf16_bldgid` 201006.0001162) |
| LiDAR max | 122.36 m | measured — catches the crown, not the thin spire |
| Floors / year / architect | 27 / 1988 / SOM | published |
| Floor area | 450,200 sq ft | published |
| Podium | OSM `building:levels=3`, OBB 78.5 × 49.4 m | measured |
| Tower part | OBB 35.3 × 30.4 m, bearing 135.3° | measured (OSM 1410929341) |
| Setback levels 96 / 106 / 116 m, notch 3.4 m | | estimated (photo) |

### 2.2 Sources

- OSM way 91626348 — https://www.openstreetmap.org/way/91626348 ; tower part https://www.openstreetmap.org/way/1410929341
- DataSF footprints + 2010 LiDAR, `sf16_bldgid` 201006.0001162 (MBLR SF3721003) — https://data.sf.gov/resource/ynuv-fyni
- Wikipedia — https://en.wikipedia.org/wiki/100_First_Plaza
- Commons photo (infobox) — https://commons.wikimedia.org/wiki/File:100_First_Plaza_from_Salesforce_Park.jpg

### 2.3 Orientation

Tower yaw −45.3° (local +x bearing 135.3°, along First St; local +y bearing 45.3°).
+Y = true north. The podium outline is raw OSM east/north metres; it extends ~40 m
toward local −y (SW) from the tower. NW = Mission St side, NE = First St side.

### 2.4 What each side shows

The photo (from Salesforce Park, south-east) shows two faces: cream stone bays with
punched windows, deep blue-glass slots at the notched corners and mid-faces, and the
stepped crown. The other two faces are assumed the same (**inferred**). The podium's
roof is not photographed (**inferred**: planted terrace + plant).

### 2.5 Recognition cues

1. Stepped setbacks climbing to a pointed crown and spire.
2. Two-tone: pink-cream stone against blue glass notches.
3. Square tower with notched corners.

### 2.7 Massing recipe

- Podium 0–13 m on the OSM outline (re-entrant west steps → one diagonal): `Toy_sand`,
  three window rows + lit panes; deck, trim parapet, `Toy_leaf` lawn with five trees
  on the free SW roof, a small plant cluster.
- Tower: three `punched_block` tiers on `notch_rect(34 − 2i, 29.5 − 2i, 3.4)`:
  13–96 m (inset 0), 96–106 m (inset 3), 106–116 m (inset 6); `Toy_glassl` boxes
  fill each notch; trim curbs at the setbacks.
- Crown: trim deck, `Toy_glass` pyramid 117–126 m, trim pyramid 122.5–129 m, trim
  spire to 136.25 m with a `Toy_red_Glow` tip and a `Toy_white_Glow` crown ring.

### 2.8 Palette

`Toy_sand` (pink-cream stone), `Toy_glass`, `Toy_glassl`, `Toy_trim`, `Toy_roofd`,
`Toy_steel`, `Toy_leaf`, `Toy_leafd`; glow `Toy_sand_Glow`, `Toy_white_Glow`,
`Toy_red_Glow`. Off-palette: `Toy_leaf`, `Toy_leafd`.

### 2.9 Roof

The crown is the roof. Podium roof: planted terrace + plant, so it is not blank from the
aerial camera.

### 2.11 Triangle budget

4,800 tris (body 3,924, glow 876).

### 2.12 Draft manifest entry

```json
{
  "id": "100-first",
  "file": "100-first.glb",
  "anchor": [-122.3977206, 37.7891952],
  "targetHeightM": 136.25,
  "cat": 3,
  "name": "100 First Plaza",
  "estimated": false,
  "dims": [95.4871, 91.7661, 136.25],
  "tris": 4800
}
```

### 2.13 Integration notes

Case B: registry entry, exclusion, batch re-bake. The podium is concave and long, so
its rings' centroids sit well off the anchor; size the exclusion against
`excluded()`'s min(centroid, any-vertex) test so it catches both the tower and the
podium rings but not the neighbours on First/Mission. Salesforce Transit Center's
rooftop park is next door — keep clear of the `transit-center` rings. Default load
radius rule: max(2500, 136.25 × 30) = 4,088 m.

### 2.15 Open risks

- Setback heights and notch size are photo estimates; the real crown has more gables
  than the two pyramids.
- `Toy_sand` may read less pink than the real stone.
- The podium outline's west steps are simplified to one diagonal.
