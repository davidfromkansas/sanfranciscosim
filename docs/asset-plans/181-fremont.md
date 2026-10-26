# 181 Fremont — SF-SIM asset plan

The slender 244 m mixed-use tower on Fremont Street beside Salesforce Park (Heller
Manus, 2018): pale aqua glass on a chamfered, slightly tapering plan, wrapped in a
white exterior **mega-brace** that draws stacked X's — a tall diamond around every
corner — up all four faces, ending in a sloped crown and a spire. It is the
second-tallest building in the Transbay cluster and stands immediately north-east of
Salesforce Tower, so it is always seen next to it.

**Deliverable:** `artifacts/181-fremont/`. Part 1 is the task prompt, Part 2 the dossier.

| | |
|---|---|
| Manifest id | `181-fremont` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.3953090, 37.7897660` (OSM OBB centre via `tk.run`) |
| Target height | **244.4 m** to the spire tip (published 802 ft; OSM `height=244.4`); roof/crown 206–220 m (estimated) |
| Footprint | OSM way 445566153: OBB 40.6 × 35.5 m, 1,289 m², bearing 45.1° |
| Triangle cap | 27,000 (built: 3,346) |
| Category | `3` (office — offices on the lower floors, condominiums above; office chosen as the dominant use) |

---

## Part 1 — Task prompt

````markdown
# Create the 181 Fremont GLB for SF-SIM

Work in artifacts/181-fremont/. Read AGENTS.md, docs/styles/miniature-toy.md and
tools/landmark-kit/toykit.py first; this plan's Part 2 is your research start.

Must capture: the white exterior mega-braces as stacked X's on every face (each brace
runs corner-to-opposite-corner over half the shaft height, so a tall diamond wraps each
corner), the chamfered corners, the pale aqua glass with fine white mullions, the
gentle taper, the sloped crown and the spire at 244.4 m.

Contract: binary GLB, metres, +Y = true north, origin at base centre, min Z 0, crest
exactly 244.4 m, flat Toy_* materials, `_Glow` only as skins over solid body and not
hidden behind braces or mullions, <= 27,000 tris (aim lean). Build with
`tk.run(SLUG, build, HERE, (-122.395309, 37.789766), 244.4)`.

Run build -> kit validate.py (--height 244.4 --anchor <tk.run anchor>, "all checks
pass") -> kit render.py. Write REFERENCE.md and REPORT.md. Do not edit the manifest,
landmarks.mjs or app code.
````

---

## Part 2 — Research and design dossier

### 2.1 Verified facts

| Fact | Value | Label |
|---|---|---|
| Height to spire tip | 244.4 m (802 ft) | published; OSM `height=244.4` |
| Floors / year / architect | 57 / 2018 / Heller Manus | published (Wikipedia, via batch facts) |
| Footprint | OBB 40.6 × 35.5 m, 1,289 m², 10-node polygon | measured (OSM) |
| Heading | faces at 45° / 135° | measured (OSM bearing 45.1°) |
| Brace pattern | stacked X's / corner diamonds | inferred (Commons photo) |
| Crown 206–220 m sloped, spire on the high side | | estimated (photo + height budget) |
| LiDAR | none (2010 survey predates the tower) | — |

### 2.2 Sources

- OSM way 445566153 — https://www.openstreetmap.org/way/445566153
- Wikipedia — https://en.wikipedia.org/wiki/181_Fremont (height, floors, architect, use)
- Commons lead photo of the Wikipedia article (upward view of two faces from the
  Fremont/Mission side) — the brace geometry was read from it; file at
  https://commons.wikimedia.org/wiki/Category:181_Fremont
- DataSF footprints (https://data.sf.gov/resource/ynuv-fyni): no usable LiDAR (pre-construction).

### 2.3 Orientation

Chamfered rectangle rotated 45°: faces at 45°/135°/225°/315°. Local +X runs along
Mission/Howard (bearing 45°). The crown slopes down to the SE, spire on the NW side
(estimated). +Y = true north; no loader rotation.

### 2.4 What each side shows

All four faces carry the same brace system and curtain wall (photo shows two faces;
the other two are **inferred** by symmetry, which the published design supports). The
base is a tall glazed lobby behind white columns on all sides (inferred from the photo's
base). The Salesforce Park bridge connection on the SW side is not modelled.

### 2.5 Recognition cues

1. White mega-braces (stacked X's, corner diamonds). 2. Slender chamfered taper.
3. Pale aqua glass with white vertical grain. 4. Sloped crown + spire.

### 2.7 Massing recipe

- `plan_at(z)`: chamfered rect 39 × 34 m (chamfer 6.5) at grade → 29 × 25 m (4.5) at
  220 m, rotated 45°.
- Shaft: `tk.banded_loft` 12–206 m (pitch 7.6) in `Toy_verdigris`, white mullion fins
  every 4.5 m (`tk.loft_fins`).
- Braces: per face, two X's (12–109 m and 109–204 m), 2.0 × 1.0 m white bars standing
  0.35 m proud; horizontal ties at mid-height and under the crown.
- Crown: sloped glass wedge 206→220 m with a white rim; spire to 244.4 m with a red
  glow tip. Lobby 0–12 m set back 1.6 m behind white columns; stone apron, 2 trees.

### 2.8 Palette

`Toy_verdigris` glass, `Toy_white` braces/rim/spire, `Toy_trim` mullions/bands,
`Toy_glassl` lobby, `Toy_stone` apron; glow `Toy_sand_Glow` (panes, lobby),
`Toy_white_Glow` (crown band), `Toy_red_Glow` (spire tip). All core palette.

### 2.9 Roof

The sloped crown plane is the roof seen from above: pale glass inside a white rim with
the spire at its high edge. No plant is visible on the real top (it is screened).

### 2.11 Triangle budget

3,346 tris (night glow 422 faces). Cheapest tower in the set; no need to spend more.

### 2.12 Draft manifest entry

```json
{
  "id": "181-fremont",
  "file": "181-fremont.glb",
  "anchor": [-122.395309, 37.789766],
  "targetHeightM": 244.4,
  "cat": 3,
  "name": "181 Fremont",
  "estimated": false,
  "dims": [50.4264, 50.4264, 244.4],
  "tris": 3346
}
```

Draft `pipeline/lib/landmarks.mjs` entry (exclusion to be checked against
`excluded()`'s centroid test at bake time):

```js
{ id: '181Fremont', name: '181 Fremont', lon: -122.395309, lat: 37.789766,
  height: 244.4, exclude: 26, camera: { distance: 700, yaw: 40, pitch: 18 } }
```

### 2.13 Integration notes

Case B: needs the registry entry above, an exclusion that removes the baked procedural
block on this footprint (OBB half-diagonal ≈ 27 m; the neighbours 50 Fremont and
Salesforce Tower must survive — check the centroid window), and the batch re-bake.
Load radius: none suggested (skyline tower, like `555-california`).

### 2.15 Open risks

- Brace geometry is read from one upward photo; exact node heights are estimated.
- The OSM polygon is irregular (10 nodes); the model is a symmetric chamfered rect.
- Crown slope direction and roof heights are estimated; only the spire tip is published.
- Category is a judgement call for a mixed office/residential tower.
