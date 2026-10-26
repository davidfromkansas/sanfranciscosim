# 201 Mission Street (Providian Financial / Pacific Gateway Building) — SF-SIM asset plan

A 30-storey office tower (1981, Primiani Weaver) on an odd trapezoidal mid-block lot
that runs from Mission through to Howard. A pale precast-concrete shaft on an
elongated octagonal plan, ribbed by dense full-height piers with slot windows between
them and a notched parapet, with a lower ~11-storey wing against one long face, all on
a grey concrete podium with terraced planters.

**Deliverable:** `artifacts/201-mission/`. Part 1 is the task prompt, Part 2 the dossier.

| | |
|---|---|
| Manifest id | `201-mission` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.3949073, 37.7911895` (bbox centre via `tk.run`; authored around the OSM podium OBB centre) |
| Target height | **135.9 m** crest (DataSF 2010 LiDAR max 135.89 m, measured); main roof 127.2 m (LiDAR majority; Wikipedia 417 ft = 127 m, published) |
| Footprint | OSM way 32862919: OBB 99.7 × 53.3 m, 3,541 m², bearing 136.3°; parts 616813259 (tower) / 616813260 (podium) |
| Triangle cap | 27,000 (built: 8,578) |
| Category | `3` (Office — `CAT.office` in `app/src/props.js`) |

---

## Part 1 — Task prompt

````markdown
# Create the 201 Mission Street GLB for SF-SIM

Work in artifacts/201-mission/. Read AGENTS.md, docs/styles/miniature-toy.md and
tools/landmark-kit/toykit.py first; Part 2 of this plan is your research start.

Must capture: the elongated octagonal tower plan from OSM part 616813259 on the OSM
podium (part 616813260); a pale concrete shaft with dense full-height ribs and dark
slot windows; the notched parapet; the lower ~11-storey wing; a grey concrete podium
with planted terraces; a designed roof (penthouse + plant).

Contract: binary GLB, metres, +Y = true north, origin at base centre, min Z 0, crest
exactly 135.9 m, flat Toy_* materials, `_Glow` only as outward skins, no degenerate
triangles, <= 27,000 tris (aim under 10,000). Build with
`tk.run(SLUG, build, HERE, (-122.3949072, 37.7910519), 135.9)`.

Run build -> kit validate.py (--height 135.9 --anchor <tk.run anchor>, "all checks
pass") -> kit render.py. Write REFERENCE.md and REPORT.md. Do not edit the manifest,
landmarks.mjs or app code.
````

---

## Part 2 — Research and design dossier

### 2.1 Verified facts

| Fact | Value | Label |
|---|---|---|
| Crest | 135.89 m | measured (DataSF LiDAR max, `sf16_bldgid` 201006.0000504) |
| Main roof | 127.24 m LiDAR majority; 417 ft (127 m) | measured / published (Wikipedia) |
| Floors / year / architect | 30 / 1981 / Primiani Weaver | published (Wikipedia infobox) |
| Floor area | 489,284 sq ft | published (CTBUH via Wikipedia) |
| Lot | trapezoidal mid-block, Mission through to Howard | published (Wikipedia) |
| Footprint | OBB 99.7 × 53.3 m, 3,541 m², bearing 136.3° | measured (OSM) |
| Tower plan | elongated octagon ~60 × 36 m, long axis ~ −7.8° from east | measured (OSM part 616813259) |
| OSM `height` | 138 m | unsourced tag; not used |
| Ribbed concrete facade, notched parapet, lower wing, concrete podium | | inferred (Commons photo) |
| Podium 17 m, wing top 57 m | | estimated (photo storey count) |

### 2.2 Sources

- OSM way 32862919 — https://www.openstreetmap.org/way/32862919 ; parts https://www.openstreetmap.org/way/616813259 (tower), https://www.openstreetmap.org/way/616813260 (podium)
- DataSF footprints + 2010 LiDAR, `sf16_bldgid` 201006.0000504 (MBLR SF3718026) — https://data.sf.gov/resource/ynuv-fyni
- Wikipedia — https://en.wikipedia.org/wiki/Providian_Financial_Building
- Commons photo (infobox image) — https://commons.wikimedia.org/wiki/File:201_Mission_Street.jpg

### 2.3 Orientation

The tower octagon is authored directly in OSM east/north coordinates (no yaw); its
long axis runs roughly E–W (−7.8°). The podium follows the street grid (yaw 45.4°,
local +y = NW). **NW = Mission St**, **SE = Howard St** (the podium runs through the
block); the NE and SW sides face neighbouring lots.

### 2.4 What each side shows

The Commons photo shows two faces of the shaft (identical ribbed concrete), the notched
parapet, the lower wing and the podium terraces. Which face carries the wing is not
recoverable from the photo; it is placed on the tower's south-east (Howard-facing) side —
**inferred**. The other faces are assumed identical (**inferred**). Roof not
photographed (**inferred**: penthouse + plant).

### 2.5 Recognition cues

1. A pale, finely ribbed concrete column — reads like fluting at distance.
2. The stretched octagonal plan with chamfered corners.
3. The lower wing stepping off one face.
4. Notched (crenellated) parapet line.

### 2.7 Massing recipe

- Podium (OSM part outline): dark glazed street storey 0–5 m behind concrete piers
  every 7 m with a warm lit ring; `Toy_concrete` body 5–17 m with two window rows;
  concrete deck, hedge-ring planters, a few trees.
- Tower 17–127.2 m: `Toy_stone` prism on the octagon, `Toy_glassd` slot panes
  (2.7 m bays, 3.75 m storeys), `Toy_white` ribs every 2.7 m (0.9 × 0.55 m) running
  1.8 m past the roof (the notched parapet).
- Wing 17–57 m: 18 × 11 m on the tower axis, on the podium's SE (Howard-side) lobe, same rib/slot skin, planted roof + trees.
- Roof: dark deck, 22 × 12 m concrete penthouse with steel louvres to 135.9 m, two
  plant clusters.

### 2.8 Palette

`Toy_stone`, `Toy_white`, `Toy_concrete`, `Toy_glassd`, `Toy_glass`, `Toy_trim`,
`Toy_roofd`, `Toy_steel`, `Toy_leaf`, `Toy_leafd`; glow `Toy_sand_Glow`.
Off-palette (WARN, documented): `Toy_concrete`, `Toy_glassd`, `Toy_leaf`, `Toy_leafd`.

### 2.9 Roof

Dark deck inside the rib crown, louvred concrete penthouse at the centre (the crest),
plant clusters at both ends of the long axis.

### 2.11 Triangle budget

8,578 tris (body 7,490, glow 1,088). Slot windows are single quads; ribs are boxes.

### 2.12 Draft manifest entry

```json
{
  "id": "201-mission",
  "file": "201-mission.glb",
  "anchor": [-122.3949073, 37.7911895],
  "targetHeightM": 135.9,
  "cat": 3,
  "name": "201 Mission Street",
  "estimated": false,
  "dims": [114.0744, 85.5104, 135.9],
  "tris": 8578
}
```

### 2.13 Integration notes

Case B: `pipeline/lib/landmarks.mjs` entry + exclusion + batch re-bake. The podium
fills the lot, so the exclusion must catch the DataSF ring 201006.0000504 and any
podium fragments without reaching the neighbours on Mission and Howard — verify the
radius against the real bake inputs. Default load radius rule (max(2500, 135.9 × 30)
= 4,077 m); not `alwaysLoaded`.

### 2.15 Open risks

- The wing's side and height are inferred from one photo; if Street View shows it on
  the Mission face, move it (one line in the build script).
- The photo is the only facade source; rib spacing (2.7 m) is a readability choice.
- Podium height (17 m) estimated from the photo; LiDAR majority only resolves the
  tower roof.
