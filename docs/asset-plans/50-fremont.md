# 50 Fremont Center (Salesforce West) — SF-SIM asset plan

A 43-storey pale-grey precast office tower (SOM, 1985) on the Fremont × Mission corner,
now Salesforce West. A tight grid of punched square windows, serrated (notched) corner
bays that step back near the top, and a crown that Wikipedia likens to Saarinen's
Tribune Tower entry. The blue Salesforce cloud on the facade is its street identity.

**Deliverable:** `artifacts/50-fremont/`. Part 1 is the task prompt, Part 2 the dossier.

| | |
|---|---|
| Manifest id | `50-fremont` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.3972410, 37.7905100` (OSM OBB centre via `tk.run`) |
| Target height | **183.0 m** roof (Wikipedia / CTBUH 2217, published); 2010 LiDAR max 185.81 m, majority 181.68 m (measured) |
| Footprint | OSM way 288716396: OBB 52.1 × 38.2 m, 1,938 m², 36 nodes (serrated), long axis bearing 134.9° |
| Triangle cap | 27,000 (built: 7,780) |
| Category | `3` (Office — `CAT.office` in `app/src/props.js`) |

---

## Part 1 — Task prompt

````markdown
# Create the 50 Fremont Center (Salesforce West) GLB for SF-SIM

Work in artifacts/50-fremont/. Read AGENTS.md, docs/styles/miniature-toy.md and
tools/landmark-kit/toykit.py first; Part 2 of this plan is your research start.

Must capture: a notched-corner slab on the OSM heading; pale stone with a regular grid
of punched dark windows; three setbacks near the top; a dark louvred crown with a
light cap and a crown light; a granite-piered base; the blue Salesforce cloud and
street trees on the Fremont (NE) face.

Contract: binary GLB, metres, +Y = true north, origin at base centre, min Z 0, crest
exactly 183.0 m, flat Toy_* materials, `_Glow` only as outward skins, no degenerate
triangles, <= 27,000 tris (aim for under 10,000). Build with
`tk.run(SLUG, build, HERE, (-122.397241, 37.790510), 183.0)`.

Run build -> kit validate.py (--height 183 --anchor <tk.run anchor>, "all checks
pass") -> kit render.py. Write REFERENCE.md and REPORT.md. Do not edit the manifest,
landmarks.mjs or app code.
````

---

## Part 2 — Research and design dossier

### 2.1 Verified facts

| Fact | Value | Label |
|---|---|---|
| Roof height | 183 m (600 ft) | published (Wikipedia, CTBUH 2217) |
| LiDAR (2010) | max 185.81 m, majority 181.68 m, median 180.87 m | measured (DataSF 201006.0001244) |
| Floors / year / architect | 43 / 1985 / SOM | published |
| Footprint | OBB 52.1 × 38.2 m, 1,938 m², 36 nodes | measured (OSM — the many nodes are the serrated corners) |
| Heading | long axis 134.9° (along Fremont St) | measured (OSM) |
| Setbacks at 158 / 168 / 176 m | | estimated (photo proportions) |
| Corner notch ~4 m | | inferred (OSM outline + photo) |

### 2.2 Sources

- OSM way 288716396 — https://www.openstreetmap.org/way/288716396
- DataSF footprints + 2010 LiDAR, `sf16_bldgid` 201006.0001244 — https://data.sf.gov/resource/ynuv-fyni
- Wikipedia — https://en.wikipedia.org/wiki/Salesforce_West
- Commons photo (Wikipedia lead image) — https://commons.wikimedia.org/wiki/File:Salesforce_West_2021.jpg

### 2.3 Orientation

Long axis 134.9° (NW–SE). Model yaw = 90 − 134.9 = −44.9°; +Y = true north. Local +y
faces 45° = **Fremont St (NE)**, the long entrance face (the building is on the west
side of Fremont: 45 Fremont's centroid is ≈ 62 m across the street axis to the NE);
local +x faces 135° = **Mission St (SE)**; NW toward Market; SW toward First St.

### 2.4 What each side shows

The photo is a straight-on view of one long face: punched windows, the stepped corner
bays rising into the setbacks, a louvred band at mid-height and the cloud low on the
face. The cloud is placed on the Fremont face — **inferred** (the photo does not name
the street). The other faces are assumed to repeat the grid (**inferred**).

### 2.5 Recognition cues

1. Pale tower with a dense punched-window grid (reads "masonry", unlike its glass neighbours).
2. Serrated corners and the stepped, setback crown.
3. The blue Salesforce cloud.

### 2.7 Massing recipe

- Plan `tk.notch_rect(50, 36.5, 4)` on yaw −44.9°.
- Base 0–11 m: glass inset 1.5 m, `Toy_sand_Glow` ring, granite piers every 5 m, granite band.
- Three `tk.punched_block` tiers in `Toy_stone` with `Toy_glass` panes: 11–158 m
  (full plan), 158–168 m (inset 2.5 m), 168–176 m (inset 5.5 m), each with a trim cornice.
- Crown 176–181.8 m: dark glass with steel louvres, `Toy_white_Glow` crown light, trim
  cap to 183 m; roof kit on the 176 m terrace.
- Cloud (three `Toy_sky` lobes ~12 m wide + `Toy_sky_Glow` quad) at 24 m on Fremont;
  stone apron, three trees on Fremont.

### 2.8 Palette

`Toy_stone`, `Toy_glass`, `Toy_granite`, `Toy_trim`, `Toy_steel`, `Toy_sky`, `Toy_roofd`,
`Toy_leaf`, `Toy_leafd`, `Toy_rust`; glow `Toy_sand_Glow`, `Toy_sky_Glow`, `Toy_white_Glow`.
All core palette.

### 2.9 Roof

Terraces read as pale steps from above; a plant cluster on the 176 m terrace around the
louvred crown, which carries a trim cap. Not blank.

### 2.11 Triangle budget

7,780 tris (body 6,584, glow 1,196). The punched panes are the main cost.

### 2.12 Draft manifest entry

```json
{
  "id": "50-fremont",
  "file": "50-fremont.glb",
  "anchor": [-122.397241, 37.79051],
  "targetHeightM": 183,
  "cat": 3,
  "name": "Salesforce West (50 Fremont Center)",
  "estimated": false,
  "dims": [63.8784, 63.8451, 183.0],
  "tris": 7780
}
```

```js
{ id: '50Fremont', name: 'Salesforce West (50 Fremont Center)', lon: -122.397241, lat: 37.79051,
  height: 183, exclude: 26, camera: { distance: 560, yaw: 45, pitch: 20 } }
```

### 2.13 Integration notes

Case B: registry entry, exclusion, batch re-bake. 350 Mission's centroid is ≈ 61 m
away across Fremont; smaller buildings on the First St side may sit closer — confirm at
bake time that a ~26 m radius clears only this footprint. Load radius: none.

### 2.15 Open risks

- Setback heights are estimated from one photo; LiDAR (majority 181.7 m) only says most
  of the roof area is high, which fits a crown that fills much of the plan.
- The mid-height louvred band and the vertical corner glazing seen in the photo are
  simplified away.
- Cloud face (Fremont) is inferred.
