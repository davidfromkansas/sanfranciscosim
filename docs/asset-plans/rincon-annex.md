# Rincon Annex (Rincon Center, 101 Spear Street) — SF-SIM asset plan

The 1940 Rincon Annex post office by Gilbert Stanley Underwood — the historic half of
Rincon Center, on Mission Street between Spear and Steuart. A three-storey Streamline
Moderne block in white plaster on a blue-grey base, with tall two-storey windows, blue
dolphin reliefs over the openings, a blue cornice line, and the Rincon Center atrium
skylight rising behind. The residential half, The Towers at Rincon, is already a
landmark (`towers-at-rincon`) and is **not** part of this asset.

**Deliverable:** `artifacts/rincon-annex/`. Part 1 is the task prompt, Part 2 the dossier.

| | |
|---|---|
| Manifest id | `rincon-annex` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.3931571, 37.7925049` (bbox centre via `tk.run`; authored around the OSM OBB centre) |
| Target height | **29.7 m** crest = the atrium skylight (DataSF 2010 LiDAR max 29.74 m, measured); parapet 18.1 m (LiDAR majority 18.08 m) |
| Footprint | OSM way 44106213: OBB 82.6 × 91.5 m, 7,357 m², 15 nodes, bearing 45.7° |
| Triangle cap | 27,000 (built: 1,546) |
| Category | `3` (Office — Rincon Center is offices, shops and a food hall; `18` Government would only fit its post-office past) |

---

## Part 1 — Task prompt

````markdown
# Create the Rincon Annex GLB for SF-SIM

Work in artifacts/rincon-annex/. Read AGENTS.md, docs/styles/miniature-toy.md and
tools/landmark-kit/toykit.py first; Part 2 of this plan is your research start.

Must capture: the OSM outline (way 44106213) as a white Streamline Moderne block on a
blue-grey base; rows of tall dark windows with blue dolphin friezes above; a blue
cornice band; the atrium skylight (the 29.7 m crest) on the SE side; a designed roof.
Do NOT model The Towers at Rincon (landmark `towers-at-rincon`).

Contract: binary GLB, metres, +Y = true north, origin at base centre, min Z 0, crest
exactly 29.7 m, flat Toy_* materials, `_Glow` only as outward skins, no degenerate
triangles, <= 27,000 tris. Build with
`tk.run(SLUG, build, HERE, (-122.3931459, 37.7925002), 29.7)`.

Run build -> kit validate.py (--height 29.7 --anchor <tk.run anchor>, "all checks
pass") -> kit render.py. Write REFERENCE.md and REPORT.md. Do not edit the manifest,
landmarks.mjs or app code.
````

---

## Part 2 — Research and design dossier

### 2.1 Verified facts

| Fact | Value | Label |
|---|---|---|
| Crest | 29.74 m (atrium skylight) | measured (LiDAR max, `sf16_bldgid` 201006.0000121) |
| Parapet / main roof | 18.08 m | measured (LiDAR majority) |
| OSM `height` | 33 m | unsourced tag; not used |
| Built | 1939–40, opened 26 Oct 1940; NRHP 1979 | published (Wikipedia) |
| Architect / style | Gilbert Stanley Underwood / Streamline Moderne | published |
| Size | 330 × 266 ft (101 × 81 m), 3 floors + half basement; 25 ft ground-floor ceilings | published |
| Dolphin reliefs over doors and windows | | published + photo |
| Footprint | OBB 82.6 × 91.5 m, 7,357 m², bearing 45.7° | measured (OSM) |
| Atrium skylight position (SE side, ~34 × 22 m) | | inferred (LiDAR crest inside this footprint; Rincon Center atrium) |

### 2.2 Sources

- OSM way 44106213 — https://www.openstreetmap.org/way/44106213
- DataSF footprints + 2010 LiDAR, `sf16_bldgid` 201006.0000121 (MBLR SF3716021) — https://data.sf.gov/resource/ynuv-fyni
- Wikipedia — https://en.wikipedia.org/wiki/Rincon_Center
- Commons photo (infobox) — https://commons.wikimedia.org/wiki/File:IMG_2185_Rincon_Center_San_Francisco.JPG

### 2.3 Orientation

Yaw +45.7° (local +x bearing 44.3°, along Mission St; local +y bearing 314.3°).
+Y = true north. **NW = Mission St** (the dolphin front), NE = Steuart St,
SW = Spear St, SE = the Rincon Center atrium and The Towers at Rincon.

### 2.4 What each side shows

The Commons photo shows the Mission St front: blue-grey base, white plaster, tall
gridded windows, dolphins in threes above them, a black-granite entry, a blue cornice
line and a third storey. Spear/Steuart sides are assumed to continue the same rhythm
(**inferred**, consistent with the published L-shaped lobby along Mission and Spear).
The SE side abuts the atrium (**inferred**). Roof: LiDAR shows a flat roof at 18.1 m
with the 29.7 m atrium skylight; roof skylight strips and plant are **inferred**.

### 2.5 Recognition cues

1. Long white Moderne front with tall dark windows.
2. Blue dolphin friezes over every window (exaggerated to blue panels).
3. Blue-grey base and blue cornice line.
4. The glass atrium pyramid behind.

### 2.7 Massing recipe

- Plan: OSM outline simplified to 8 points (tiny jogs dropped), yaw 45.7°.
- Base 0–2.4 m `Toy_glassl` (blue-grey); body 2.4–16.9 m `Toy_white`.
- Tall `Toy_ink` windows 3.0–11.0 m every 6.5 m; `Toy_sky` dolphin panels 10.9–12.3 m
  above them; small `Toy_ink` third-storey windows 12.4–15.2 m.
- `Toy_glassl` cornice band 16.9–18.1 m; dark roof deck.
- Atrium: 34 × 22 m `Toy_white` drum to 23.5 m, `Toy_glassl` pyramid to 29.7 m.
- Roof: four long `Toy_glassl` skylight strips, one plant cluster.
- Sidewalk apron; five street trees along Mission St.

### 2.8 Palette

`Toy_white`, `Toy_glassl`, `Toy_sky`, `Toy_ink`, `Toy_roofd`, `Toy_steel`, `Toy_stone`,
`Toy_leaf`, `Toy_leafd`; glow `Toy_sand_Glow`. Off-palette: `Toy_leaf`, `Toy_leafd`.

### 2.9 Roof

Flat dark roof with long skylight strips, a plant cluster and the atrium pyramid (the
crest).

### 2.11 Triangle budget

1,546 tris (body 1,474, glow 72). Very lean — a low, broad building.

### 2.12 Draft manifest entry

```json
{
  "id": "rincon-annex",
  "file": "rincon-annex.glb",
  "anchor": [-122.3931571, 37.7925049],
  "targetHeightM": 29.7,
  "cat": 3,
  "name": "Rincon Center (Rincon Annex)",
  "estimated": false,
  "dims": [129.4039, 130.5617, 29.7],
  "tris": 1546
}
```

### 2.13 Integration notes

Case B: registry entry, exclusion, batch re-bake. **Same block as `towers-at-rincon`**
(anchor ~81 m SE): the exclusion must catch the annex ring 201006.0000121 without
reaching the towers' rings (which the existing landmark already excludes). Check at
bake time that no atrium ring falls between the two exclusions and is left as a
procedural block. Default load radius 2,500 m.

### 2.15 Open risks

- The atrium skylight's exact plan and position are inferred from the LiDAR crest;
  check against an aerial image and against the `towers-at-rincon` GLB so the two
  don't overlap.
- Side and rear elevations inferred from the Mission front.
- Dolphins are flat blue panels — legible from the aerial camera, not sculpted.
