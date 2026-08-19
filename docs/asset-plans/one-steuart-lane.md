# One Steuart Lane — SF-SIM asset plan

SOM's 2021 condominium tower on the Embarcadero, built on the site of the 75 Howard
Street parking garage. John King called it "a carefully arranged stack of skeletal
cubes", and that is exactly the brief: **five three-storey volumes stacked on a
two-storey base, each stepping back on alternating sides**, so the corner zig-zags
its way to the sky instead of running straight. Every volume is a cage of **thick
Roman travertine pilasters and lintels** with the glass held a hand's width behind
the stone face, and the gaps between the volumes are **wraparound terraces** —
open storeys with dark soffits, glass balustrades and planters.

SOM's own summary of the intent: the outdoor spaces "break down the vertical
orientation of the tower into horizontally-proportioned volumes that relate to the
panoramic waterfront landscape they face." That horizontal banding is the whole
identity, and it is what the diorama has to carry — this is not a tower with a
crown, it is a tower with a rhythm.

It matters for the scene because the Embarcadero waterfront currently has nothing
between the Ferry Building and Rincon Hill, and this is the piece that reads at the
head of that block from the app's aerial camera.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/one-steuart-lane/`. This document is the plan only: Part 1 is the
runnable task prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `one-steuart-lane` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3916888, 37.7915643` (footprint AABB centre, measured) |
| Target height | **67.06 m** = 220 ft, the architectural top — see the height dispute in 2.15 risk 1 |
| Footprint | 1,904 m2 four-vertex rectangle, 40.6 m (Steuart, NE) x 47.0 m (SE) x 40.6 m (SW) x 46.8 m (Howard, NW), rotated 44.9 deg |
| Triangle cap | 24,000 |
| Category | `2` (multi-unit residential) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready One Steuart Lane GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of One Steuart Lane — the SOM condominium
tower at 1 Steuart Lane / 75 Howard Street on San Francisco's Embarcadero — and
deliver it as a downloadable, validated GLB.

Do not integrate or deploy the model yet. Create the asset, validate it, render
review images, and commit the deliverables to your working branch.

## Read the project sources first

Before any research or modeling, read in this order:

1. `AGENTS.md`
2. `docs/styles/README.md`
3. `docs/styles/miniature-toy.md`
4. `.agents/skills/sf-miniature-style/SKILL.md`
5. `.agents/skills/sf-asset-check/SKILL.md`
6. `app/public/sf-assets/landmarks_manifest.json`
7. `artifacts/555-california/` — **the primary reference implementation.** It is the
   closest shipped asset in kind: a tall, four-square, grid-faced downtown tower
   whose whole identity is the rhythm of a repeating structural bay rather than any
   single ornament, at roughly this altitude of abstraction. Its build script's bay
   and elevation helpers are the skeleton to **adapt, not rewrite**.
8. `artifacts/300-brannan/` — secondary reference, for two specific things: the
   45-degree SoMa-grid authoring convention (build on the measured polygon, never
   an axis-aligned box that you rotate), and the designed-roof / rooftop-crest
   treatment.
9. `docs/asset-plans/one-steuart-lane.md` — this plan, whose dossier is your
   research starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules.

## Must capture

- **Five stacked three-storey volumes over a two-storey base.** Each volume is a
  simple rectangular prism; each steps back from the one below **on alternating
  sides**, so from any corner the silhouette zig-zags. This is the building. If
  only one thing survives simplification, it is this.
- The **travertine cage**: continuous cream/silver stone pilasters and lintels on
  all four elevations, deep enough to throw a real shadow, with the glass held
  **back behind the stone face** so every opening reads as a recess, not a decal.
  Six real inches on the building; exaggerate to 0.25–0.35 m in the miniature.
- The **irregular bay rhythm**. The curtain wall uses three module widths — 4, 6
  and 8 ft — deliberately syncopated. Do not build a uniform grid; alternate at
  least two widths per elevation or the building loses its "personal rhythm".
- The **wraparound terraces** at each of the four setbacks: one open storey with a
  dark recessed soffit, a clear glass balustrade set in from the slab edge, and a
  few planters. The slab edge itself is a thin bright cantilevered plate — it is
  what makes the volumes read as *stacked* rather than *carved*.
- The **deep terrace bay**: one bay-wide vertical slot of deeper terraces running
  the full height of each elevation. Visible on the Howard Street face as a
  recessed slot with glass rails and dark soffits.
- The **tall glazed base**: a double-height ground floor of dark storefront glass
  divided by clusters of **vertical travertine baguettes** (fluted stone fins), a
  travertine band above it, and a set-back second-floor amenity level with planted
  terraces.
- The **entrance on Steuart Lane (north-east)**: a bronze portal with a wood door
  under a projecting flat glass canopy that cantilevers ~3.4 m clear of the facade.
- A **designed roof**: continuous cream parapet; two large **round cooling towers**
  in a mechanical yard toward the west; a long field of **dark blue photovoltaic
  panels** in parallel strips over most of the roof; a light-toned **mechanical
  penthouse box** east of centre; a **building-maintenance-unit crane** on its
  track running diagonally across the deck. The camera looks down — this roof is a
  facade and it is the most under-modelled surface in the scene.

## Research One Steuart Lane independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor and the real-world
orientation, and gather references covering:

- All four elevations. The **north-east (Steuart Lane / Bay)** and **north-west
  (Howard Street)** faces are the two documented at street level; the south-east
  and south-west faces face the block interior and must be read from oblique
  aerials and the three-quarter panorama listed in 2.2.
- The roof, from near-nadir aerial imagery.
- The **count and heights of the stacked volumes** — the dossier reads five
  volumes of three storeys over a two-storey base from the May-2025 three-quarter
  panorama, and that is the single number most worth re-counting.
- Whether each volume steps back on **two** sides or on **all four**, and by how
  much. The dossier's setback depths are *inferred* from photographs, not measured.

**Three source traps are already known and resolved in 2.1 and 2.15 — re-check
them, do not silently re-inherit the wrong value:**

1. **The height is disputed: 220 ft vs 240 ft.** SOM, Swinerton, the developer's
   topping-out release, SF YIMBY's topping-out report and OSM's `height=67.056`
   (220.00 ft to the centimetre) all say **220 ft**. CTBUH and the SF Chronicle say
   240 ft. This plan uses **67.06 m**. Reasoning in 2.15 risk 1. If you overturn
   it, say so loudly in REPORT.md — REPORT beats plan.
2. **DataSF's LiDAR footprint layer does not contain this building.** `ynuv-fyni`
   is derived from 2010 LiDAR; the ring on this parcel (`mblr = SF3741031`, median
   height 21.55 m) is the **parking garage that used to be here**. Do not use it
   for the footprint and do not use its heights for anything. OSM way/667097308 is
   the only survey-grade footprint available, and it agrees with SOM's published
   20,595 sq ft site area to within 0.5%.
3. **Esri World Imagery at this location is construction-era.** The z20 nadir tile
   shows a tower crane, formwork and storage tanks on an unfinished deck. Use
   Google's z21 imagery for the roof (source listed in 2.2), not Esri's.

## Create a reference dossier

Write `artifacts/one-steuart-lane/REFERENCE.md` containing: source links and what
each establishes; verified dimensions and location; orientation; observations from
all four sides and above; the 3–5 strongest recognition cues; features to preserve;
features to simplify; uncertainties and conflicting evidence. Do not commit
copyrighted full-resolution imagery.

## Make your own design decisions

Follow the conversion process in `docs/styles/miniature-toy.md` §22: identify the
recognition cues, strip nonessential information, rebuild the massing from a few
confident volumes, exaggerate only the signature features, simplify the facade into
broad rhythms, deliberately design every surface visible from above, evaluate from
the app's high three-quarter aerial camera, then simplify again.

This is a **secondary building with landmark presence** in the style bible's detail
budget (§21). It is the tallest thing on its block and it stands on an otherwise
empty stretch of modelled waterfront, so it earns a real facade grid and a designed
roof — but it must not out-shout the Ferry Building to the north or the Bay Bridge
behind it. The real building was explicitly designed not to have skyline presence
("It's a tall building, but we weren't trying to have a presence on the skyline" —
SOM's design director). Honour that: this is a quiet, well-made object.

**Watch the light-value budget, which is the opposite problem from most SoMa
assets.** Roughly two-thirds of this building's visible surface is near-white
travertine. Flat cream over 67 m will blow out and lose all the modelling that
makes it legible. The stone grid must be carried by *geometry and shadow*, not by
tonal contrast: keep the frame on one cream value, let the recessed glass supply
the dark, and check the aerial render before adding any second stone tone.

Do **not** reach for `Toy_roofd` on the roof deck. It renders near-black
(rgb 9,9,12) under the app's lighting and turns a designed roof into a hole — use
`Toy_steel` for the deck and reserve the darkest values for the terrace soffits,
where a shadow is what you actually want.

The finished asset must be immediately recognizable as this building, consistent
with the real thing from all four sides and above, architecturally credible, and a
premium handcrafted miniature — not photorealistic, not voxel art, not generic
low-poly, and never accurate in one view while invented in the others.

## Scope of the exported asset

Export the single building: base, all five stacked volumes, the travertine grid on
all four elevations, terraces and balustrades, the entrance canopy, the parapet,
the roof deck and all roof furniture.

Do not include unrelated surrounding city geometry: Steuart Street, Steuart Lane,
Howard Street, The Embarcadero, the neighbouring Gap headquarters, Rincon Center or
the Towers at Rincon, the street trees on both frontages (there are many and they
are prominent in every photograph — they are the pipeline's job, not the asset's),
sidewalks, planters outside the property line, parked cars, people, plinths,
cameras or lights.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary `.glb`;
real-world meters; origin at base center; minimum geometry Z ≈ 0; applied transforms;
no negative scales; outward normals; no duplicate or foreign geometry; no image
textures; no transparency; flat-color materials named `Toy_*` from the project
palette; `_Glow` suffix only on surfaces that glow at night; no `Toy_body`; no
cameras, lights, animations, armatures or constraints; at most 24,000 triangles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model
drops into the city at its real-world heading — the loader applies no rotation
(`placeGeneric` in `app/src/assets.js` only scales and positions). The **Steuart
Lane elevation faces north-east, bearing 44.2°**; the **south-east elevation
faces 134.8°**; the **south-west elevation faces 224.5°**; the **Howard Street
elevation faces north-west, bearing 314.9°**. Build directly on the measured
footprint polygon in 2.3 rather than modelling an axis-aligned box and rotating it.
Record the measured headings in `REPORT.md`.

Deriving "outward" from the building centroid is safe here — the footprint is
convex — but the setback volumes are *not* concentric with it, so offset each
volume from its own edge loop, not from the tower's centre.

**Height normalization:** the tallest geometry in the export (the mechanical
penthouse cap, which is the crest) must land at exactly **67.06 m** so the loader's
`targetHeightM / measuredHeight` scale is 1.0.

## Reproducible Blender workflow

Blender 5.2 LTS. Headless: `blender -b --python script.py -- args`.

Keep `artifacts/one-steuart-lane/build_one_steuart_lane.py` (deterministic build
script), `artifacts/one-steuart-lane/one-steuart-lane.blend`, and
`artifacts/one-steuart-lane/one-steuart-lane.glb`. The script must rebuild the
model reliably enough for future revision.

Because the facade grid is the expensive part of this asset, build it from a
parameterised bay function driven by a per-elevation list of module widths, and
merge each volume down to a single mesh before export. Do not bevel the stone bars
— they are hairline strips, a bevel doubles their triangle count and reads as
nothing at the app's scale.

## Required review renders

Render the exact final geometry from controlled cameras:
`one-steuart-lane-top.png`, `one-steuart-lane-north.png`,
`one-steuart-lane-east.png`, `one-steuart-lane-south.png`,
`one-steuart-lane-west.png`, plus `one-steuart-lane-contact-sheet.png`, at least
one high three-quarter aerial beauty render `one-steuart-lane-aerial.png`, and a
night render `one-steuart-lane-aerial-night.png`.

The four elevations must share scale, framing, lighting, exposure and projection.
The **top view is the important one here** — it must clearly show the parapet ring,
the PV strips, the two round cooling towers, the penthouse box, the BMU crane and
the terrace levels stepping in below. Place the aerial camera to look down the
east corner so both the Steuart and south-east elevations show the zig-zag stack at
once; that view is this building's subject.

## Validate the exported GLB

Re-import `one-steuart-lane.glb` into a fresh isolated Blender scene and validate
the re-import, not the source scene. Report object count, triangle count,
dimensions, bounding-box min/max, min Z, XY center offset, material names,
image-texture count, camera count, light count, animation count, applied-transform
status, negative-scale status, normal-orientation status, unexpected geometry, and
per-material contract compliance. Write
`artifacts/one-steuart-lane/validation.json` and
`artifacts/one-steuart-lane/REPORT.md`.

The axis-aligned XY bounding box will be roughly **62.1 x 61.6 m** even though no
elevation is longer than 47.0 m — that is the expected consequence of a 45°
real-world heading, not a scale error.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "one-steuart-lane",
  "file": "one-steuart-lane.glb",
  "anchor": [
    -122.3916888,
    37.7915643
  ],
  "targetHeightM": 67.06,
  "cat": 2,
  "name": "One Steuart Lane",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a separate, explicitly requested job — run `docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in `docs/asset-plans/one-steuart-lane.md`.
````

---

## Part 2 — Research and design dossier

Compiled 18 August 2026 from the sources in 2.2. Values marked *inferred* are
visual or derived estimates, not published figures — the executing agent must
re-verify anything it relies on.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Building name | **One Steuart Lane** | OSM `name`; onesteuartlane.com; SOM project page — measured |
| Address resolution | `1 STEUART LN` = `75 HOWARD ST` → block **3741**, mapblklot **3741047**, base lot **045** plus ~120 condo lots | DataSF parcels (`acdm-wktn`); DBI permits (`i98e-djp9`) show both street names against lot 045 — measured |
| Architect | **Skidmore, Owings & Merrill (SOM)**. Craig W. Hartman FAIA, senior design partner; Mark Schwettmann, design director; Keith Boswell, partner (enclosure); John Kuchen, associate director | SOM project page; onesteuartlane.com; SF Chronicle — measured |
| Structural engineer | SOM | SOM project page (SEAOC / SEAONC Excellence in Structural Engineering awards 2023) |
| Interiors | SOM (residences); **Rottet Studio** (public spaces) | PRNewswire; onesteuartlane.com |
| Landscape | **Hood Design** | SOM project page |
| General contractor | **Swinerton Builders** | Swinerton project page; California Construction News |
| Facade design/build | **Enclos**; stone **Campolonghi Spa** (Roman travertine, Torano basin, Tuscany); glass **NorthGlass**; metalwork **MK Metal**; consultant Curtainwall Design Consultants | Enclos project page; The Architect's Newspaper / Facades+ — measured |
| Developer | **Paramount Group, Inc.** with **SRE Group Ltd.**; The John Buck Company in the earlier phase; owner entity **75 Howard LP** | PRNewswire; SFYIMBY; Swinerton — measured |
| Completion | Topped out **September 2020**; occupancy / completion **2021** (SOM's own page says "Completion Year 2020", meaning structural completion) | SFYIMBY 22 Sep 2020; SF Chronicle 12 Oct 2021; Facades+ 9 Jul 2021 |
| Storeys | **20** above grade (SOM, PRNewswire, California Construction News); DBI permits and OSM `building:levels` both record **21** — see 2.15 risk 3 | two source families, both consistent internally |
| **Height** | **220 ft = 67.06 m** | SOM project page ("Building Height: 220 feet"); Swinerton ("220 feet"); PRNewswire; SFYIMBY ("reached its 220-foot pinnacle"); OSM `height=67.056` = 220.00 ft — **five sources, measured**. CTBUH and SF Chronicle say 240 ft; see 2.15 risk 1 |
| Structure | All-concrete: Type-1 concrete construction, post-tensioned decks, tapered cantilevered slabs projecting up to **20 ft** from the interior columns; no large perimeter columns | Swinerton; SOM |
| Facade | Custom unitized curtain wall; **solid Roman travertine** pilasters and lintels over a concealed high-performance aluminium structure; low-iron laminated insulated glass with low-E, nominally 1¾ in; module widths **4 / 6 / 8 ft**; glass set **6 in behind** the stone face; blackened stainless steel metalwork; GFRC covering the mullions internally | Facades+ / The Architect's Newspaper (SOM enclosure team quoted directly); SF Chronicle — measured |
| Massing | "**Five masses** cantilevered over what will become private terraces for twelve larger residences"; "gradually steps back on alternating sides from the street to the sky"; "large wraparound terraces carve the massing into a series of three- and four-storey volumes"; "recessed balconies on each intervening floor" | SFYIMBY (topping out); SOM project page — measured |
| Terraces | Wraparound terraces at every zoning-mandated setback; the deep ones ~**40 ft** long and up to **16 ft** deep; a single bay of deep terraces runs up each side of the tower | SFYIMBY; SF Chronicle — measured |
| Ground floor | 24 ft tall glass main entry; point-supported glass canopy on glass fins, 17 ft 10 in wide, cantilevering **11 ft** clear of the facade; custom wood door with cast glass blocks in a bronze portal frame; blackened stainless panels; stone cladding and **stone baguettes** | Enclos project page — measured |
| Units / area | **120** condominium units (Swinerton says 118), 900–3,100 sq ft typical, four penthouses to 6,200 sq ft; **335,000 sq ft** gross; **4,500 sq ft** ground-floor retail | SOM; SFYIMBY; California Construction News |
| Parking | 3 parking levels, 2 of them underground, with a valet car elevator | Swinerton — not modelled |
| Site area | **20,595 sq ft = 1,913.3 m2** | SOM project page — measured; agrees with the OSM footprint (1,904.1 m2) to 0.5% |
| Footprint | **1,904.1 m2**, four-vertex rectangle | OSM way/667097308 — the only post-2010 survey available, see 2.15 risk 2 |
| Roof | Flat. Continuous cream parapet; large field of dark PV panels in parallel strips; two large round cooling towers in a mechanical yard toward the west; a light mechanical penthouse box east of centre; a BMU (window-washing) crane on a diagonal track | Google z21 aerial imagery, 2024–25 vintage — **observed** |
| Zoning | `C-3-O(SD)` Downtown Office (Special Development). The block's limit is 200 ft plus rooftop features; this site was raised to 220 ft after the waterfront height fights of 2013–15 | DataSF parcels; SF Chronicle |
| Sustainability | LEED BD+C NC **Gold** | SOM; PRNewswire |
| Previous use of site | A multi-storey parking garage on the "grungy edge of the Financial District", alongside the Embarcadero Freeway until its 1991 demolition | SF Chronicle; SFYIMBY |
| Frontage headings | Steuart Lane / Steuart St front faces **44.2°** (NE); south-east flank **134.8°**; south-west flank **224.5°**; Howard St front **314.9°** (NW) | measured from the OSM footprint polygon |

### 2.2 Sources

- `https://www.som.com/projects/one-steuart-lane/` — SOM's own project page. The
  **primary source** for the architect, 220 ft height, 20 storeys, 20,595 sq ft
  site, 335,000 sq ft gross, 120 units, LEED Gold, and for the design intent
  quoted in the header ("break down the vertical orientation of the tower into
  horizontally-proportioned volumes"). Also the source for the facade description:
  "an elegantly proportioned, shifting grid of roman travertine pilasters and
  lintels", "a slender, variegated grid of silver travertine sourced from Tuscany".
- `https://www.archpaper.com/2021/07/facades-som-one-steuart-lane-stacked-massing-and-travertine/`
  and its mirror `https://facadesplus.com/...` — the enclosure article, with SOM's
  Keith Boswell / Mark Schwettman / John Kuchen quoted directly on the **4/6/8 ft
  module widths**, the stone anchorage, the GFRC interior cover, and the
  "stacked square volumes, with a self-admittedly boxy massing broken up by
  wrap-around terraces placed at each zoning-mandated setback". **The single most
  useful source for the facade.**
- `https://enclos.com/project/onesteuartlane/` — the facade contractor. The only
  source with hard ground-floor numbers: the 24 ft glass entry, the 17 ft 10 in
  glass-fin canopy cantilevering 11 ft, the bronze portal and wood door, the stone
  baguettes.
- `https://www.sfchronicle.com/sf/article/There-s-a-new-tower-on-the-Embarcadero-and-16520281.php`
  — John King, 12 Oct 2021. The best written description of what the building looks
  like ("a carefully arranged stack of skeletal cubes, each of them three or four
  stories tall"; "the outer frame consists of thick bars of Roman travertine"; the
  glass "begins a full 6 inches back from the creamy stonework's outer edge";
  "a single bay of deep terraces running up each side"). **Also the source of the
  240 ft figure** — see 2.15 risk 1.
- `https://sfyimby.com/2020/09/soms-waterfront-one-steuart-lane-tops-out-soma-san-francisco.html`
  — the topping-out report. "Reached its 220-foot pinnacle"; "composed of five
  masses cantilevered over what will become private terraces for twelve larger
  residences"; "forty-foot wraparound terraces".
- `https://swinerton.com/project/one-steuart-lane/` — the general contractor. Type-1
  concrete, post-tensioned decks, 21 stories, 118 units, 3 parking levels.
- `https://www.prnewswire.com/news-releases/one-steuart-lane-san-franciscos-ultra-luxury-waterfront-condominium-tower-celebrates-official-topping-off-301111444.html`
  — developer release: 20 storeys, 220 ft, 120 units, Rottet Studio interiors.
- `https://www.skyscrapercenter.com/building/one-steuart-lane/21484` — CTBUH. Lists
  **73.2 m / 240 ft**, all-concrete, SOM, 2021. *Conflicts with the sources above*;
  see 2.15 risk 1. Its page 403s to automated fetches; read through a search
  summary or a browser.
- `https://www.openstreetmap.org/way/667097308` — the footprint. Tags:
  `building=apartments`, `building:levels=21`, `height=67.056`, `roof:shape=flat`,
  `name=One Steuart Lane`, `addr:housenumber=1`, `addr:street=Steuart Street`.
- `https://data.sfgov.org/resource/acdm-wktn` (DataSF parcels) — block 3741,
  mapblklot 3741047, zoning `C-3-O(SD)`. Note this address resolves to **~120
  condo lots that all share one mapblklot**; querying by point returns twenty rows
  that are all the same parcel.
- `https://data.sfgov.org/resource/i98e-djp9` (DBI building permits) — block 3741
  lot 045. Original construction permit **2016-0401-3681**; unit-level permits
  reference levels up to 20 and consistently record 21 stories.
- `https://data.sfgov.org/resource/3psu-pn9h` (DataSF street centrelines) — used to
  measure which elevation faces which street; see 2.3. Geometry column is `line`,
  not `shape`.
- `https://data.sfgov.org/resource/ynuv-fyni` (DataSF building footprints) — **does
  not contain this building.** The ring on this parcel (`mblr = SF3741031`,
  median 21.55 m, max 30.29 m) is the demolished parking garage, captured by the
  2010 LiDAR. Listed here so it is not mistaken for a survey of the tower.
- Google Street View, panoramas retrieved via
  `https://streetviewpixels-pa.googleapis.com/v1/thumbnail?panoid=<ID>&yaw=<h>&pitch=<p>&w=1400&h=1000`
  (requires a browser User-Agent **and** a `google.com` referer; `pitch` is
  inverted, so negative looks up):
  - `FgQeEOFiFPKjWDAfs-1pNg` — 222 The Embarcadero, **May 2025**, 70.6 m out on
    bearing 228°. The full north-east elevation head-on. *The single best
    elevation reference.*
  - `ovtx36arpx2McKDNysw2wA` — 250 The Embarcadero, **May 2025**, 68.7 m out on
    bearing 272°. The three-quarter view down the east corner showing the north-east
    and south-east elevations together. **This is the massing reference** — the
    stacked volumes, the alternating setbacks and the terraces are all legible.
  - `xXe2riqG1LYNcj4uxMyibw` — 275 Steuart Lane, **May 2025**, 37.2 m out. The base:
    storefront glazing, travertine baguettes, the level-2 amenity soffit, the street
    planters, the main entrance portal at frame left.
  - `ZUh55kQzLojQ3Ae-8Z8tPg` — 58 Howard St, **Aug 2024**, 33.3 m out on bearing
    144°. The Howard Street elevation close up: the travertine grid at full size,
    the irregular module widths, the deep terrace slot, the amenity terrace.
  - `_NsXTVXb0T8LqAa5H_NuHg` — 210 Spear St, Jan 2025. **Does not see this
    building** — 120 Spear blocks it. Recorded so the next agent does not spend the
    fetch. The south-west elevation has no street-level view.
  Panorama ids can be resolved keylessly by loading instantstreetview.com in a
  browser and calling `new google.maps.StreetViewService().getPanorama(...)` from
  the page; the Maps JS API is already present there.
- Google satellite imagery `https://mt1.google.com/vt/lyrs=s&x=&y=&z=21`, ~2024–25
  vintage — the roof: PV strips, two round cooling towers, the mechanical penthouse
  box, the BMU crane, the parapet, and the terrace levels stepping in below. The
  z20 tile at this location is a shallow oblique from the south-east rather than a
  true nadir; both are useful, and the OSM ring overlays correctly on the z21 base
  once the ~14 m parallax of the tower top is allowed for.
- Esri World Imagery z19/z20 — **construction-era at this location** (a tower crane,
  formwork and storage tanks on an unfinished deck, c. 2019–20). Do not read the
  roof from it. *Observed; recorded as a trap.*

### 2.3 Orientation and placement

The building fills its entire lot in the block bounded by **Steuart Street** to the
north-east, **Howard Street** to the north-west, **Spear Street** to the south-west
and **Folsom Street** to the south-east. The Embarcadero runs past 45 m beyond the
Steuart frontage; the Gap headquarters (Robert A.M. Stern, 2001, brick, 15 storeys
with a 275 ft crown) shares the block to the south.

Distances measured from each face midpoint to the DataSF street centrelines:

| Face | Nearest street | Distance to centreline |
|---|---|---|
| North-east | **Steuart Lane** 13.2 m / **Steuart St** 13.7 m (The Embarcadero 45.5 m) | the address frontage and the Bay elevation |
| North-west | **Howard St** 11.6 m | the 75 Howard frontage |
| South-west | Spear St 48.4 m | block interior — no street |
| South-east | Folsom St 141.5 m | block interior — no street |

Measured OSM footprint, in Blender coordinates (metres, `+X` east, `+Y` north),
already centred on the anchor `-122.3916888, 37.7915643` (the axis-aligned
bounding-box centre, which is what the loader's origin convention needs):

```
(   2.020,  30.824)   N corner — Steuart St x Howard St
(  31.049,   2.548)   E corner — Steuart St x south-east lot line
(  -2.072, -30.824)   S corner — south-east x south-west lot lines
( -31.049,  -2.338)   W corner — south-west lot line x Howard St
```

A fifth OSM node sits on the Howard edge and is collinear with it to within
0.1°; it is noise from the trace and should be dropped. The ring encloses
**1,904.1 m2** against SOM's published 20,595 sq ft (1,913.3 m2) site area, −0.5%,
which is the expected agreement for a building that covers its whole lot.

Edges, with outward normals:

| Edge | Length | Faces | Elevation |
|---|---|---|---|
| N→E | 40.52 m | NE 44.2° | **Steuart Lane / Steuart Street** — the entrance and Bay elevation |
| E→S | 47.02 m | SE 134.8° | south-east flank, block interior |
| S→W | 40.63 m | SW 224.5° | south-west flank, block interior |
| W→N | 46.83 m | NW 314.9° | **Howard Street** |

The two opposite-edge pairs differ by 0.11 m and 0.19 m — trace noise on a building
that is a true rectangle. Square it up if that is cheaper to build on; do not move
the anchor to do it.

Because of the ~45° heading, the axis-aligned bounding box is **62.10 x 61.65 m**.
That is correct.

The site is flat: ground elevations across this parcel and its neighbours run
3.19–3.86 m NAVD88 with σ 0.13 m. The app's terrain handles it; the asset does not
need a plinth.

### 2.4 What each side shows

**North-east (Steuart Lane / Steuart Street), 40.52 m** — the address elevation and
the one everyone photographs, documented head-on in May 2025 from 222 The
Embarcadero. A double-height glazed base of dark storefront divided by clusters of
slender vertical travertine baguettes, with the main entrance at the north end
under a projecting flat glass canopy and a bronze-framed wood door. A travertine
band caps the base; above it the level-2 amenity floor is set back behind its own
glass, with planters. Then five stacked volumes of travertine cage over dark
recessed glass, each stepping in from the one below, with a wraparound terrace
between every pair. The topmost volume reads noticeably more open than the rest —
close to a pure frame with sky visible through it — and it is set back on both
visible sides.

**South-east flank, 47.02 m** — no street-level view; read from the May-2025
three-quarter panorama at 250 The Embarcadero and from oblique aerials. Fully
treated with the same travertine grid and glass — this is not a party wall. Its
volumes step on the opposite beat from the north-east face, which is what produces
the zig-zag at the east corner. It carries its own deep terrace bay.

**South-west flank, 40.63 m** — the least documented elevation. Not visible from
Spear Street (120 Spear blocks it) and not covered by any Street View sequence
consulted. Oblique aerials show it is finished in the same grid, so model it as a
quieter version of the south-east face: same rhythm, fewer terraces, no entrances.
Treat its bay count as *inferred*.

**North-west (Howard Street), 46.83 m** — documented close up in Aug 2024. The best
view of the grid at full size: thick cream pilasters and lintels framing large
blue-grey panes, with the module widths visibly irregular, two narrow bays beside
one wide one. The ground floor is dark storefront behind travertine baguettes and
carries the `ONE STEUART LANE` signage and the leasing entrance; a garage/service
opening sits toward the west end. A **one-bay-wide slot of deep terraces** runs up
the elevation left of centre — recessed, with dark soffits and clear glass
balustrades — and is the most legible instance of that feature anywhere on the
building. The level-2 amenity terrace is planted and set back behind a travertine
band.

**Top** — a flat deck inside a continuous cream parapet, at the top of the fifth
volume. Google z21 imagery shows, from north-west to south-east: a mechanical yard
with **two large round cooling towers** and low equipment; a long field of **dark
blue photovoltaic panels** laid in parallel strips and divided into bays by pale
walkway strips, covering perhaps half the deck; a light-toned **mechanical
penthouse box** roughly 12 x 8 m east of centre — the crest; and a **BMU crane** on
a track running diagonally across the deck with its boom parked toward the south.
Below the parapet on the south-east and south-west sides the terrace levels step
in, paved, with square planters that read green from above. No tree canopy
overhangs the roof.

### 2.5 Recognition cues, ranked

1. **The stack of five skeletal cubes**, stepping back on alternating sides. Seen
   from any corner the silhouette is a zig-zag. Nothing else about this building
   matters as much.
2. **The travertine cage over set-back glass** — the frame is thick, continuous and
   near-white; the glass is dark and always recessed behind it.
3. **The wraparound terraces** between volumes: thin bright cantilevered slab
   edges, dark soffits, clear balustrades, planters.
4. **The irregular bay rhythm** — 4/6/8 ft modules, deliberately syncopated.
5. **The designed roof** — PV strips, two round cooling towers, the penthouse box,
   the BMU crane.

### 2.6 Massing recipe

A working decomposition, to be re-counted by the executing agent against the
250-Embarcadero three-quarter panorama. Heights are *inferred* from photographic
proportion against the measured 67.06 m total; the storey grouping is *measured*
from SFYIMBY's "five masses" and the Chronicle's "three or four stories tall".

| Element | Levels | Top (m) | Notes |
|---|---|---|---|
| Base | 1–2 | 11.5 | full lot footprint; double-height glazed ground floor, set-back amenity level above |
| Volume A | 3–5 | 20.8 | flush with the base on Steuart and Howard |
| terrace | 6 | 23.9 | wraparound |
| Volume B | 7–9 | 33.1 | set back on NE + SW |
| terrace | 10 | 36.2 | wraparound |
| Volume C | 11–13 | 45.4 | set back on NW + SE |
| terrace | 14 | 48.5 | wraparound |
| Volume D | 15–17 | 57.6 | set back on NE + SW |
| terrace | 18 | 60.7 | wraparound |
| Volume E (crown) | 19–20 | 65.5 | set back on NW + SE; the most open volume |
| Parapet + mech penthouse | — | **67.06** | the crest, and the bbox top |

Setback depth: **2.5 m typical, 4.9 m at the deep terrace bay** (*inferred* from the
"as deep as 16 feet" figure and the 40 ft wraparound length). The deep bay is one
module wide and runs the full height of each elevation.

Floor-to-floor works out at ~3.1 m, which is tight for a building with nine-foot
ceilings; that tightness is the strongest argument on the 240 ft side of the height
dispute and is discussed in 2.15 risk 1.

### 2.7 Palette map

| Surface | Material | Hex | Note |
|---|---|---|---|
| Travertine pilasters, lintels, parapet, baguettes, slab edges | `Toy_cream` | f2ede3 | the dominant surface — carry the grid with geometry, not a second tone |
| Base band and podium stone | `Toy_sand` | ece4d4 | one step down from cream, used sparingly at the base only |
| Vision glass, recessed | `Toy_glass` | 2a4d73 | supplies all the dark |
| Upper / sky-reflecting panes, balustrades | `Toy_glassl` | 6f95b8 | scatter, do not band |
| Terrace soffits, deep recesses | `Toy_stone` | d9d2c2 in shadow, or `Toy_steel` | **not** `Toy_roofd` |
| Blackened stainless mullions, rails, canopy fittings | `Toy_ink` | 3a3530 | hairline only; a little goes a long way |
| Roof deck | `Toy_steel` | 9aa0a6 | `Toy_roofd` renders near-black in the app |
| Rooftop PV array | `Toy_navy` | 2c4a70 | the one saturated dark on the roof |
| Cooling towers, penthouse box, BMU crane | `Toy_steel` | 9aa0a6 | |
| Terrace and street planting | `Toy_sage` | — | small, restrained |
| Entrance portal, wood door | `Toy_bronze` | — | one accent, at one door |

### 2.8 Night state

The real building's night signature is **light from underneath the cantilevers**:
the terrace soffits are downlit, so each setback reads as a horizontal glowing line
wrapping the tower. That is both the truest and the most restrained hero glow
available, and it reinforces the horizontal banding the whole design is about.

- **Hero:** a thin `Toy_cream_Glow` strip on the underside of each of the four
  terrace slab edges, plus the same treatment on the base cornice. Four bands
  plus one — that is the composition.
- **Supporting:** the double-height lobby as a warm `Toy_gold_Glow` band across the
  Steuart Lane base, and a sparse, irregular scatter of lit unit windows in
  `Toy_glassl_Glow` — no more than one pane in six, never a whole floor, never a
  regular pattern.
- **Nothing else glows.** No lit parapet, no roof glow, no signage glow.

Two traps from earlier assets apply directly:

- A `_Glow` material's **base colour is its night appearance** — a Blender night
  render with high emission strength will flatter a colour that is far too dark in
  the app. Judge the glow colour unlit.
- Do **not** build the glow as a closed shell around the terrace edge. A closed
  glow shell is two alpha layers and reads at ~23% by day, which will tint the
  cream travertine. Single-sided strips only.

### 2.9 Triangle budget

Cap **24,000**. Indicative split:

| Part | Triangles |
|---|---|
| Five volume shells + base | 1,500 |
| Travertine grid, four elevations, five volumes | 12,000 |
| Terrace slabs, soffits, balustrades, planters | 4,000 |
| Base: storefront, baguettes, canopy, entrance | 2,500 |
| Roof: parapet, PV strips, cooling towers, penthouse, BMU | 3,000 |
| Headroom | 1,000 |

The grid is the whole budget. Build it from a parameterised bay function, keep the
stone bars un-bevelled, and merge each volume to one mesh before export.

### 2.10 Draft manifest entry

```json
{
  "id": "one-steuart-lane",
  "file": "one-steuart-lane.glb",
  "anchor": [-122.3916888, 37.7915643],
  "targetHeightM": 67.06,
  "cat": 2,
  "name": "One Steuart Lane",
  "estimated": false,
  "dims": [62.10, 61.65, 67.06],
  "tris": 0,
  "loadRadius": 2500
}
```

`loadRadius` follows the default rule `max(2500, targetHeightM × 30)` =
`max(2500, 2012)` = **2500**. This building is explicitly not a skyline piece —
`alwaysLoaded` would be wrong for it.

### 2.13 Integration notes (Case B)

This id does not exist in `pipeline/lib/landmarks.mjs` or `app/src/landmarks.js`,
so integration is **Case B**: a registry entry plus a tile re-bake, run through
`docs/asset-plans/INTEGRATION-PROMPT.md`.

Draft registry entry:

```js
{
  id: 'oneSteuartLane',
  name: 'One Steuart Lane',
  lon: -122.3916888,
  lat: 37.7915643,
  height: 67.06,
  exclude: 24,
  camera: { distance: 420, yaw: 40, pitch: 18 },
},
```

**Sizing `exclude`.** `excluded()` in `pipeline/buildings.mjs` drops a ring when
`min(nearestVertexDistance, centroidDistance)` from the **landmark anchor** is under
`r`. Measured against DataSF's bake input from the anchor above:

| Ring | Gate (m) | Role |
|---|---|---|
| `SF3741031` — the demolished 75 Howard garage, on this parcel | ≈ 0 (centroid) | must drop |
| this building's own Overture ring (OSM-derived) | ≈ 0 (centroid) | must drop — see below |
| `SF3741032` — the 72 m neighbour to the south-west | **28.3** | must survive |

That is a wide band, not a tight one: anything from a few metres up to 28 m drops
exactly the two rings that must go. **24 m** sits comfortably in the middle and is
the proposed value.

Two things the integrator must still do rather than take on trust:

1. **Re-measure against both bake inputs**, not just DataSF. The ceiling is often
   Overture's rather than DataSF's, and the two files disagree about party-wall
   positions by a metre or more. The sweep is ~50 lines over `streamFeatures` +
   `outerRings` and takes well under a minute.
2. **Confirm the floor against this building's own Overture centroid**, not its
   DataSF one. Overture is the gap-fill source for current buildings, and since
   DataSF has no post-2010 footprint here, Overture's ring is almost certainly the
   *only* thing currently drawing a procedural block on this site — a ~67 m one,
   taller than most of its neighbours. An excluded DataSF ring never calls
   `markOccupied()`, so if Overture's ring survives the exclusion it will re-add the
   building straight through the asset.

**Expect the procedural block to be tall and obvious.** Unlike most Case B sites,
where the fallback massing is a low box, the thing being replaced here is a
full-height tower. That makes the before/after unusually easy to verify — and makes
an unbaked check useless, because the procedural block and the asset are nearly the
same size.

**Batch warning.** The shared landmark `BatchedMesh` was measured at 99% full in
SoMa at 84 landmarks, and it overflows silently: each reload drops a *different*
landmark rather than erroring. This corner of the Embarcadero has a large cluster of
sibling landmarks in flight at the same time. Whoever runs
`docs/asset-pipeline/BATCH-INTEGRATE.md` must check the reserve buffer before
blaming this asset for a neighbour that stopped rendering.

### 2.15 Open risks and conflicting evidence

**1. The height: 220 ft or 240 ft.** This is the one number worth arguing about.

- **220 ft (67.06 m)** — SOM's project page; Swinerton's project page; the
  developer's topping-out press release; California Construction News; SF YIMBY's
  topping-out report ("reached its 220-foot pinnacle"); and OSM's `height=67.056`,
  which is 220.00 ft converted to the centimetre. The architect, the general
  contractor and the developer all agree.
- **240 ft (73.2 m)** — CTBUH's Skyscraper Center entry, and John King in the SF
  Chronicle ("a 20-story, 240-foot condominium building"), who most likely took it
  from CTBUH.

The plan uses **220 ft**, on the weight of the primary sources. The reconciliation
that makes both true is that SF measures zoning height to the roof and permits
certain rooftop features above it: 220 ft is the approved envelope (this site was
raised from the block's 200 ft limit to 220 ft after the 2013–15 waterfront height
fights), and 240 ft would be the top of the mechanical penthouse. Against that: the
penthouse box in the aerial imagery does not look like it stands 20 ft proud of the
parapet, and "220-foot pinnacle" was written about a structure that had just topped
out.

The honest counter-argument is arithmetic. Twenty storeys in 220 ft, with a 24 ft
entry level, leaves ~10 ft floor-to-floor for units with nine-foot ceilings and
tapered post-tensioned slabs — tight. At 240 ft it is ~11.4 ft, which is normal for
this market. If the executing agent can rectify a facade elevation from the
222-Embarcadero panorama and get a floor-to-floor measurement, that settles it.
Until then: **67.06 m, with the mechanical penthouse cap as the bbox top**, and the
consequence of being wrong is contained — the tower body is authored at its own
absolute heights, so a bad crest moves one small box, not the whole building.

**2. The footprint has only one source.** DataSF's LiDAR footprint layer predates
the building by a decade, so OSM way/667097308 is the only survey available. It is
a clean four-vertex rectangle whose area agrees with SOM's published site area to
0.5% and which overlays correctly on 2024–25 Google imagery, so confidence is good
— but there is no second measurement, and its two opposite-edge pairs differ by
0.11 m and 0.19 m, which is trace noise.

**3. Twenty storeys or twenty-one.** SOM, the developer and the trade press say 20;
DBI permits and OSM say 21. Both are probably right about different things — 20
residential levels above a ground floor that DBI counts. Unit numbers in the permit
record run to 2004, i.e. level 20. Model 20 visible levels above grade; the count
only matters for the facade rhythm, not the height.

**4. `Toy_roofd` on the roof deck.** It renders rgb(9,9,12) under the app's
lighting — near-black — and would turn this building's best surface into a hole.
Use `Toy_steel`. Flagged here because the name is the obvious choice and it is
wrong.

**5. The dark-value budget runs the other way here.** Most SoMa assets in this
scene fight a too-dark facade. This one is two-thirds near-white stone over 67 m
and will blow out instead. The grid has to be carried by geometry and shadow; a
second stone tone is the tempting fix and it will read as dirt.

**6. The south-west elevation is undocumented at street level.** 120 Spear blocks
every approach and no Street View sequence sees it. Its bay count is *inferred*
from the oblique aerials.

**7. Esri imagery here is construction-era.** Its z19/z20 tiles show a tower crane
and formwork on an unfinished deck. Anyone reading the roof from Esri will model a
building site.

**8. Street trees dominate every ground-level photograph.** The Steuart and Howard
frontages are both heavily planted and the canopy hides the base in most frames.
Use the pitched-down panoramas listed in 2.2 for the base, and remember the trees
belong to the pipeline, not to this asset.
