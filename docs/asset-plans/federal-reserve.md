# Federal Reserve Bank of San Francisco (101 Market Street) — SF-SIM asset plan

The Twelfth District's headquarters since 1983 (SOM), on Market Street between Spear
and Main. A long slab of alternating travertine spandrels and bronze ribbon glass,
fronted along Market by a deep two-storey colonnade whose roof is a terrace of planter
boxes, with a lower operations block behind toward Mission.

**Deliverable:** `artifacts/federal-reserve/`. Part 1 is the task prompt, Part 2 the dossier.

| | |
|---|---|
| Manifest id | `federal-reserve` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.3955200, 37.7930020` (OSM OBB centre via `tk.run`) |
| Target height | **63.1 m** crest (DataSF 2010 LiDAR max 63.14 m, measured); slab roof 60.5 m (LiDAR majority 60.52 m) |
| Footprint | OSM way 32612362: OBB 88.1 × 81.4 m, 7,128 m², bearing 135.6° |
| Triangle cap | 27,000 (built: 4,514) |
| Category | `18` (Government — as `ferry-station-post-office`; a federal agency, not a commercial office) |

---

## Part 1 — Task prompt

````markdown
# Create the Federal Reserve Bank of San Francisco GLB for SF-SIM

Work in artifacts/federal-reserve/. Read AGENTS.md, docs/styles/miniature-toy.md and
tools/landmark-kit/toykit.py first; Part 2 of this plan is your research start.

Must capture: the long Market St slab with broad travertine bands and bronze ribbon
glass; the colonnade along Market with planter boxes on its roof; the lower block
behind; a low roof plant (LiDAR allows only 2.6 m over the slab roof).

Contract: binary GLB, metres, +Y = true north, origin at base centre, min Z 0, crest
exactly 63.1 m, flat Toy_* materials, `_Glow` only as outward skins, no degenerate
triangles (use whole-storey pitches in `tk.shaft`), <= 27,000 tris. Build with
`tk.run(SLUG, build, HERE, (-122.39552, 37.793002), 63.1)`.

Run build -> kit validate.py (--height 63.1 --anchor <tk.run anchor>, "all checks
pass") -> kit render.py. Write REFERENCE.md and REPORT.md. Do not edit the manifest,
landmarks.mjs or app code.
````

---

## Part 2 — Research and design dossier

### 2.1 Verified facts

| Fact | Value | Label |
|---|---|---|
| Crest | 63.14 m | measured (LiDAR max, `sf16_bldgid` 201006.0000590) |
| Slab roof | 60.52 m | measured (LiDAR majority) |
| OSM `height` | 66 m | unsourced tag; not used |
| Occupied | 1983 (moved from 400 Sansome) | published (Wikipedia) |
| Architect | Skidmore, Owings & Merrill | published (batch research) |
| Footprint | OBB 88.1 × 81.4 m, 7,128 m², bearing 135.6° | measured (OSM) |
| Colonnade ~2 storeys with roof planters; ~12-storey banded slab | | inferred (Commons photo) |
| Rear operations block 23.9 m | | estimated (not photographed) |

### 2.2 Sources

- OSM way 32612362 — https://www.openstreetmap.org/way/32612362
- DataSF footprints + 2010 LiDAR, `sf16_bldgid` 201006.0000590 (MBLR SF3712025) — https://data.sf.gov/resource/ynuv-fyni
- Wikipedia — https://en.wikipedia.org/wiki/Federal_Reserve_Bank_of_San_Francisco
- Commons photo (infobox) — https://commons.wikimedia.org/wiki/File:Federal_Reserve_Bank,_San_Francisco.jpg

### 2.3 Orientation

Yaw +45° (local +x bearing 45°, along Market; local +y bearing 315°). +Y = true
north. **NW = Market St** (colonnade), NE = Spear St, SW = Main St, SE = toward
Mission and 60 Spear (same block).

### 2.4 What each side shows

The photo (elevated, from across Market) shows the Market front and the Main St end:
banded slab, the colonnade with a planter box per bay on its roof, Market St trees.
Spear St end assumed symmetric (**inferred**). The rear block and its height are not
photographed (**estimated**). Roof: flat; LiDAR leaves 2.6 m for plant/penthouse.

### 2.5 Recognition cues

1. Strong horizontal striping — broad pale stone bands, dark bronze glass.
2. The colonnade along Market with a row of planter boxes on its roof.
3. A long, low, flat-topped slab (much lower than its towered neighbours).

### 2.7 Massing recipe

- Slab 84 × 34 m (local y −3…31): dark `Toy_glassd` lobby 0–9 m inset 2 m with a lit
  ring; `tk.shaft` 9–60.5 m, 12 storeys of `Toy_bronze` glass under 2.2 m
  `Toy_stone` bands (0.5 m proud).
- Colonnade 84 × 12 m (y 31…43): 12 stone piers, stone roof slab at 9 m, one stone
  planter box with a `Toy_leaf` shrub mass per bay.
- Rear block 80 × 40 m (y −41…−1), 0–23.9 m, 5 storeys of the same skin, roof kit.
- Slab roof: deck, 1.2 m stone parapet, two low plant clusters, 30 × 14 m stone
  penthouse to the 63.1 m crest.
- Plinth; six street trees along Market.

### 2.8 Palette

`Toy_stone` (travertine), `Toy_bronze`, `Toy_glassd`, `Toy_roofd`, `Toy_steel`,
`Toy_leaf`, `Toy_leafd`; glow `Toy_sand_Glow`. Off-palette: `Toy_bronze`,
`Toy_glassd`, `Toy_leaf`, `Toy_leafd`.

### 2.9 Roof

Flat slab roof: parapet, penthouse, two low plant clusters capped to the LiDAR crest;
rear block roof kit; the planted colonnade terrace is the roof feature that reads.

### 2.11 Triangle budget

4,514 tris (body 3,840, glow 674).

### 2.12 Draft manifest entry

```json
{
  "id": "federal-reserve",
  "file": "federal-reserve.glb",
  "anchor": [-122.39552, 37.793002],
  "targetHeightM": 63.1,
  "cat": 18,
  "name": "Federal Reserve Bank of San Francisco",
  "estimated": false,
  "dims": [129.9662, 129.9662, 63.1],
  "tris": 4514
}
```

### 2.13 Integration notes

Case B: registry entry, exclusion, batch re-bake. Same block (3712) as `60-spear`
(anchor ~95 m ESE) — keep the two exclusions apart. Across Market are One Market /
the Hyatt (`hyatt-regency`, `one-market-plaza-towers` already landmarks); the
colonnade sits on the building line, not in the street. Default load radius 2,500 m.

### 2.15 Open risks

- The rear block's height (23.9 m) is estimated; LiDAR only resolves the slab roof.
- Plan proportions: the model is 84 × 84 m against the OSM OBB 81.4 (along Market) ×
  88.1 m — within ~3 m.
- Bands are a simplification of the real paired spandrels; the thin teal line under
  each band in the photo is omitted.
