# 126 South Park — SF-SIM asset plan

A 1907 two-storey wood-frame commercial building on the west arc of the South Park oval.
It is the narrowest building yet planned for this set: a **6.9 m frontage on a 29.8 m
deep lot**, party walls down both long flanks, and only two free elevations in the whole
building. What makes it worth modelling is what the plan does about that: the sliver is
**pinched to 4.0 m at its waist by two light wells cut in from opposite sides**, roughly
ten metres back from the street. That notch is the only way daylight reaches the middle
of a 30 m tube, it is exactly what the leasing agent means by "an atrium garden", and it
is the one thing about this building a camera looking down actually sees.

Unlike most of this set, the **street elevation is photographed and certain** — gray
painted horizontal wood siding under a projecting bracketed eave. The uncertainty here
sits on the roof and at the rear, not on the front.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/126-south-park/`. This document is the plan only: Part 1 is the runnable task
prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `126-south-park` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3945863, 37.7816006` (footprint area centroid, measured) |
| Target height | **7.6 m** to the front eave crest; flat roof deck 7.32 m — LiDAR-derived, see 2.1 and 2.15 |
| Footprint | 195.3 m², 16 vertices; 6.90 m frontage on South Park (SE) × 29.79 m deep; pinched to 4.01 m at the waist; measured |
| Triangle cap | 7,000 |
| Category | `3` (office) — assessor class "Commercial Office" |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 126 South Park GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of 126 South Park in San Francisco and deliver it
as a downloadable, validated GLB.

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
7. `artifacts/135-south-park/` — the closest reference implementation: same block
   (3775), same oval, same era, same 45° heading, same "memorable ordinary building"
   brief, and the same roof-first design logic
8. `docs/asset-plans/126-south-park.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Read 2.15 before you start

This dossier is **inverted relative to the rest of the set**: its street facade is
photographed and near-certain, while its roof and rear are inferred. 2.15 says exactly
which is which. Do not quietly promote the roof paragraphs to fact in `REFERENCE.md`.

## Must capture

- The extreme **proportion**: 6.9 m wide, 29.8 m deep, at the real 45° heading. This
  building is a plank on edge and it must read as one from every angle
- The **waist** — the NE light well (2.37 m long × 1.65 m deep) and the SW light well
  (3.49 m long × 1.28 m deep) that overlap for 1.99 m and squeeze the plan to
  **4.01 m** about ten metres back from the street. Both must be genuine voids cut
  through the full height, not surface dents
- The **second, shallower SW light well** further back (3.84 m long × 0.84 m deep)
- The **projecting bracketed eave** over the South Park front — a shallow hood on
  exposed rafter tails, the building's one piece of ornament
- **Gray painted horizontal wood siding** on the front, with its board rhythm implied,
  not modelled board by board
- The front's real composition: an entrance bay with a dark metal security gate on
  the **south-west** third, two tall multi-pane windows on the **north-east** two
  thirds, a belt course between floors, and a two-window group on the upper floor set
  toward the north-east
- **Blank party walls on both long flanks** apart from the light wells — no openings
- A designed flat roof: skylights over the deep plan, the light wells biting in from
  both sides, a small mechanical cluster and a hatch

## Research 126 South Park independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- **The roof.** This is the dossier's biggest gap. No usable aerial was obtained
  (2.2): the best available Esri imagery at this location is washed out at z20 and
  z21 is not served. Confirm whether the roof carries skylights (the LoopNet listing
  says it does), where they sit, and whether there is any stair bulkhead or
  mechanical penthouse
- **The rear (north-west) elevation** onto the mid-block yard — nothing was found
  showing it
- Whether the light wells are open to the ground, glazed over, or planted (the
  Hawthorne Group listing calls the result "an atrium garden", which implies at
  least one of them is a real open court at ground level)
- The exact paint colour of the siding, and whether the flanks are painted at all
  or left as bare party wall
- Day and night appearance

Prefer architect/engineer publications, owner or institutional material,
planning and permitting documents, architectural press, geolocated photography,
and aerial/satellite imagery. Never rely on a single photograph, a single
AI-generated image, or a single unsourced 3D model. Separate verified facts from
visual inference; if sources disagree, document the disagreement and decide.

**Three source conflicts are already known and resolved in 2.1 / 2.15 — re-check them,
do not silently re-inherit the wrong value:**

1. **LoopNet records "3 Stories" and 5,442 SF.** This is contradicted by 19 consecutive
   assessor rolls (2007–2025), by both building permits on the lot, and by the
   photograph. **Build 2 storeys.**
2. **Two architecture-press pages appear in search results attached to this address**
   (Perkins&Will and Office Snapshots, "South Park Venture Capital Firm", a brick-clad
   1920s building of 16,420 sq ft). **Neither page states this address anywhere.** The
   attribution is a search-summariser artefact and the building described is not this
   one — it is four times too large and the wrong material. Ignore both.
3. **The SF Planning case 2010.0959CV** surfaces in searches for this address. It is
   **147 South Park Avenue**, block 3775 **lot 031**, on the opposite side of the oval.
   Not this building.

## Create a reference dossier

Write `artifacts/126-south-park/REFERENCE.md` containing: source links and what each
establishes; verified dimensions and location; orientation; observations from all
four sides and above; the 3-5 strongest recognition cues; features to preserve;
features to simplify; uncertainties and conflicting evidence. Be explicit about which
roof statements you confirmed and which you inherited unconfirmed from this plan.
A contact sheet of attributed reference thumbnails is welcome if legally permissible —
do not commit copyrighted full-resolution imagery.

## Make your own design decisions

Follow the conversion process in `docs/styles/miniature-toy.md` §22: identify the
recognition cues, strip nonessential information, rebuild the massing from a few
confident volumes, exaggerate only the signature features, simplify the facade
into broad rhythms, deliberately design every surface visible from above,
evaluate from the app's high three-quarter aerial camera, then simplify again.

This is a **secondary building** in the style bible's detail budget (§21). Clear
massing, one strong facade rhythm, a designed roof, and exactly one identity cue
carried hard: **the pinched waist**. Resist adding hero-tier ornament, and resist
inventing facade detail — §29 says a building that lacks personality should strengthen
ONE defining characteristic, and here that characteristic is the plan shape.

The finished asset must be immediately recognizable as this building's real massing,
consistent from all four sides and above, architecturally credible, and a
premium handcrafted miniature — not photorealistic, not voxel art, not generic
low-poly, and never accurate in one view while invented in the others.

## Scope of the exported asset

Export the single 1907 building: wood-frame shell on the real footprint, both light
wells, the front eave, all openings, roof deck and roof furniture.

Do not include unrelated surrounding city geometry: South Park (the street or the
park), the neighbouring buildings at 112 and 130/134 South Park, the mid-block rear
yard, street trees, the sidewalk, the climbing ivy on the north-east party line,
people, plinths, cameras or lights. Temporary context may appear in review renders but
must not leak into the GLB.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary
`.glb`; real-world meters; origin at base center; minimum geometry Z ~ 0;
applied transforms; no negative scales; outward normals; no duplicate or foreign
geometry; no image textures; no transparency; flat-color materials named `Toy_*`
from the project palette; `_Glow` suffix only on surfaces that glow at night; no
`Toy_body`; no cameras, lights, animations, armatures or constraints; at most
7,000 triangles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model
drops into the city at its real-world heading — the loader applies no rotation
(`placeGeneric` in `app/src/assets.js` only scales and positions). The South Park
entrance front faces **south-east, outward bearing 135.3°**; the building is rotated
roughly 45° off the world axes, so build directly on the measured footprint polygon in
2.3 rather than modelling an axis-aligned box and rotating it. Record the measured
heading in `REPORT.md`.

**Height normalization:** the tallest geometry in the export (the front eave crest)
must land at exactly **7.6 m** so the loader's `targetHeightM / measuredHeight` scale
is 1.0.

## Reproducible Blender workflow

Blender 5.2 LTS. Headless: `blender -b --python script.py -- args`.

Keep `artifacts/126-south-park/build_126_south_park.py` (deterministic build script),
`artifacts/126-south-park/126-south-park.blend`, and
`artifacts/126-south-park/126-south-park.glb`. The script must rebuild the model
reliably enough for future revision. Do not modify or rename an unrelated existing GLB
to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`126-south-park-top.png`, `126-south-park-north.png`, `126-south-park-east.png`,
`126-south-park-south.png`, `126-south-park-west.png`, plus
`126-south-park-contact-sheet.png`, at least one high three-quarter aerial beauty render
`126-south-park-aerial.png`, and a night render `126-south-park-aerial-night.png`.

The four elevations must share scale, framing, lighting, exposure and
projection; use orthographic or long-lens cameras; label directions from the
researched orientation; **the top view is the important one here** and must clearly show
both light wells, the waist, the eave and the roof furniture; the aerial view uses the
style bible's camera assumptions (30-50 degrees down, long lens). Simple tabletop
lighting, neutral warm background, minimal depth of field, and every image must depict
the same exported model.

## Validate the exported GLB

Re-import `126-south-park.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture
count, camera count, light count, animation count, applied-transform status,
negative-scale status, normal-orientation status, unexpected geometry, and
per-material contract compliance. Render at least one review image from the
re-imported asset. Write `artifacts/126-south-park/validation.json` and
`artifacts/126-south-park/REPORT.md`.

Note that the axis-aligned XY bounding box will be roughly **26.0 × 25.9 m** even
though the building is 6.9 m wide and 29.8 m deep — that is the expected consequence of
a ~45° real-world heading, not a scale error. The front eave adds ~0.7 m to the
south-east corner of that box.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "126-south-park",
  "file": "126-south-park.glb",
  "anchor": [
    -122.3945863,
    37.7816006
  ],
  "targetHeightM": 7.6,
  "cat": 3,
  "name": "126 South Park",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a separate, explicitly requested job — run `docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in `docs/asset-plans/126-south-park.md`.
````

---

## Part 2 — Research and design dossier

Compiled 16 August 2026 from the sources in 2.2. Values marked *inferred* are visual or
derived estimates, not published figures — the executing agent must re-verify
anything it relies on. **This dossier's roof section is materially weaker than its
facade section — the reverse of the usual case here; read 2.15 before relying on it.**

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Address | 126 South Park (OSM records the street as "South Park"; the assessor writes "SOUTH PARK"; listings use "S Park Ave" and "S Park St" interchangeably) | OSM way/124884348 `addr:*` tags; assessor roll |
| Block / lot (APN) | **3775 / 061** | SF building permits on this address; DataSF footprint `mblr = SF3775061` matches the OSM ring to 0.58 m |
| Built | **1907** | SF Assessor secured roll, identical across all 19 rows 2007–2025 |
| Storeys | **2** | SF Assessor roll (`number_of_stories = 2.0`, every year); both permits on the lot (1999, 2023) record 2 existing storeys; confirmed by photograph |
| Conflicting storey count | 3, with 5,442 SF | LoopNet listing — **contradicted**, see 2.15 |
| Construction type | **D** (wood frame) | SF Assessor roll — corroborated by the 1999 permit "repair damaged dry rot siding & trim" and by the photograph |
| Assessor use class | **Commercial Office** / Office | SF Assessor roll (`use_definition`, `property_class_code_definition`) |
| Rooms | 15 | SF Assessor roll |
| Zoning | SPD (South Park District) | SF Assessor roll |
| Lot area | 2,143 SF = 199.1 m² | SF Assessor roll — the building covers essentially the whole lot (195.3 m² footprint) |
| Current use | Office; ground floor ~1,800 RSF marketed for lease as of Sept 2025 | The Hawthorne Group listing |
| Re-roofed | **2023** | permit 2023-08-28 "re-roofing" |
| Siding repaired | 1999 | permit 1999-12-20 "repair damaged dry rot siding & trim" |
| Footprint | **195.3 m²**, 16 vertices; 6.90 m frontage (SE) × 29.79 m deep; 6.99–7.02 m wide except at the waist | OSM way/124884348 geometry via Overpass, reprojected — **measured** |
| Waist (minimum width) | **4.01 m**, over a 1.99 m stretch 9.86–11.85 m back from the front | derived from the measured polygon |
| DataSF footprint (cross-check) | 178.6 m², centroid 2.19 m from the OSM centroid, nearest vertex 0.58 m | DataSF Building Footprints `SF3775061` — agrees on position and shape; smaller because its trace cuts the light wells differently |
| Roof deck height | **7.32 m** above ground (`hgt_majoritycm` and `hgt_mediancm` both 7.32 m; mean 7.34 m, σ 0.64 m over 715 cells) | DataSF LiDAR — **measured**, and unusually tight |
| Maximum feature height | 10.16 m (`hgt_maxcm`) | DataSF LiDAR — **edge contamination, not a real feature**, see 2.15 |
| Minimum height | 3.74 m (`hgt_mincm`) | DataSF LiDAR — likewise an edge artefact |
| Front eave crest | ~7.6 m | *inferred*, deck + ~0.3 m, from the photograph |
| Ground elevation | 8.25 m (NAVD88, `gnd_min_m`) | DataSF LiDAR — app terrain handles this, not the asset |
| OSM height tag | 7 | OSM way/124884348 — corroborates the LiDAR deck rather than contradicting it |
| Frontage heading | South Park front faces **135.3° (SE)**; rear faces 315.4° (NW); NE party wall outward 45.0°; SW party wall outward 224.9° | measured from the footprint polygon |
| North-east neighbour | **112 South Park** — shares a party wall, 0.6 m gap; OSM `height=6`; LiDAR majority 7.32 m, max 8.04 m | OSM way/124884354, DataSF `SF3775060` |
| South-west neighbour | **130 / 134 South Park** (lot 062, 3 storeys) — shares a party wall, ~0.6 m gap; LiDAR median 8.40 m and 11.77 m across its two parts | OSM ways/124884341 and /124884351, DataSF `SF3775062`, permits on lot 062 |
| Rear condition | mid-block yard; nearest building vertex 5.53 m from our rear | OSM way/124884351, measured |
| Row context | The west arc runs 102, 106 (Gran Oriente Filipino, h=11), 108/110 (h=8), 112 (h=6), **126**, 130/134, 140 (h=10), 150 (h=8), 156 (h=6) | OSM height tags — 126 is one of the lowest on its block face |

### 2.2 Sources

- https://www.openstreetmap.org/way/124884348 — footprint geometry, `addr:housenumber=126`, `addr:street=South Park`, `building=yes`, `height=7`
- `https://data.sfgov.org/resource/ynuv-fyni` (DataSF Building Footprints, LiDAR-derived) — footprint `SF3775061` and the 7.32 m deck, ground elevation 8.25 m NAVD88
- `https://data.sfgov.org/resource/wv5m-vpq2` (SF Assessor Historical Secured Property Tax Rolls), block 3775 lot 061 — 1907, 2 storeys, Commercial Office, construction type D, 15 rooms, SPD, lot 2,143 SF, all 19 rolls 2007–2025
- `https://data.sfgov.org/resource/i98e-djp9` (SF Building Permits), block 3775 — the 1999 siding permit and the 2023 re-roofing permit on lot 061, and the block-face storey counts used in 2.1's row context
- https://www.thgcommercial.com/project/126-south-park/ — The Hawthorne Group leasing page. **The single most valuable source in this dossier**: it carries a current (Sept 2025), unobstructed, straight-on colour photograph of the entire street elevation, and the description "NATURAL LIGHT VIA 3-SIDES OF WINDOW LINE, PLUS AN ATRIUM GARDEN" which is what the light wells in 2.3 are for. *observed (listing photo)* — the building as marketed, but the photo is recent and matches the permit history
- https://www.loopnet.com/Listing/126-S-Park-Ave-San-Francisco-CA/15125827/ — LoopNet listing. Establishes "Directly on South Park. Great Natural Light (skylights and windows on 4 sides)", "Atrium", 2 tandem parking spaces, renovated 1990. Its "3 Stories / 5,442 SF" is **rejected**, see 2.15
- Esri World Imagery (ArcGIS Online `World_Imagery`, z20 tiles 167786–167788 / 405270–405272) — attempted for the roof; **washed out at this location and unusable for roof detail**, and z21 returns "Map data not yet available". This is the reason 2.4's roof paragraph is weak
- https://commissions.sfplanning.org/hpcpackets/2016-008192SRV%20-%20Gran%20Oriente.pdf — National Register nomination for the Gran Oriente Filipino Hotel at 104-106 South Park, three lots north-east. Useful only for block-face character: it establishes that the surrounding buildings are "mainly two to four-story attached, mixed-use flats and multi-unit apartment buildings primarily constructed between 1906 and 1924" — i.e. that a 1907 two-storey wood-frame building here is typical, not anomalous
- `docs/asset-plans/135-south-park.md` — the same block, opposite arc of the oval; its 2.6/2.8 are the reference for how this set handles a plain building

**Sources deliberately NOT used:**

- **Perkins&Will "South Park Venture Capital Firm"** and the matching **Office Snapshots** article. Both were returned by search with this address attached to them; **both were fetched directly and neither states this address anywhere**. They describe a 16,420 sq ft brick-clad 1920s building — four times this building's floor area and the wrong material. The address attribution was a search-summariser artefact. See 2.15.
- **SF Planning case 2010.0959CV.** Returned by search for this address; the PDF's own header reads `Project Address: 147 SOUTH PARK AVENUE` / `Block/Lot: 3775/031`. A different building on the far side of the oval, proposed for demolition in 2012. Not this building.
- No aerial or rooftop photograph of 126 South Park was located. No rear-elevation photograph was located. No architect is recorded in any source consulted, and the building carries no name.

### 2.3 Orientation and placement

The building sits on the west arc of the South Park oval, its narrow front looking
south-east across the street into the park, its long body running back north-west into
the block toward Bryant Street (which it does not reach — the rear opens onto a
mid-block yard, ~42 m short of Bryant). It is rotated about 45° from the world axes,
like the whole SoMa grid.

Measured footprint polygon, in Blender coordinates (metres, `+X` east, `+Y` north),
counter-clockwise, already centred on the anchor `-122.3945863, 37.7816006`:

```
( -6.579,   1.521)
( -5.980,   2.107)
( -3.261,  -0.602)
( -3.851,  -1.187)
( -1.352,  -3.675)
( -0.419,  -2.757)
(  2.045,  -5.222)
(  1.165,  -6.095)
(  8.143, -13.059)
( 13.053,  -8.207)
(  6.348,  -1.508)
(  5.169,  -2.669)
(  3.488,  -0.999)
(  4.667,   0.172)
( -8.004,  12.807)
(-12.976,   7.899)
```

Edges, with outward normals:

| Edge | Length | Faces | Elevation |
|---|---|---|---|
| 8 `(8.143,-13.059) -> (13.053,-8.207)` | 6.90 m | SE 135.3° | **South Park front** |
| 9 `(13.053,-8.207) -> (6.348,-1.508)` | 9.48 m | NE 45.0° | party wall with 112, front run |
| 10 `(6.348,-1.508) -> (5.169,-2.669)` | 1.65 m | NW 315.5° | **NE light well, front cheek** |
| 11 `(5.169,-2.669) -> (3.488,-0.999)` | 2.37 m | NE 44.8° | **NE light well, back** |
| 12 `(3.488,-0.999) -> (4.667,0.172)` | 1.66 m | SE 135.2° | **NE light well, rear cheek** |
| 13 `(4.667,0.172) -> (-8.004,12.807)` | 17.89 m | NE 44.9° | party wall with 112, rear run |
| 14 `(-8.004,12.807) -> (-12.976,7.899)` | 6.99 m | NW 315.4° | **rear elevation**, onto the mid-block yard |
| 15 `(-12.976,7.899) -> (-6.579,1.521)` | 9.03 m | SW 224.9° | party wall with 130/134, rear run |
| 0 `(-6.579,1.521) -> (-5.980,2.107)` | 0.84 m | SE 135.6° | **SW light well #2, rear cheek** |
| 1 `(-5.980,2.107) -> (-3.261,-0.602)` | 3.84 m | SW 224.9° | **SW light well #2, back** |
| 2 `(-3.261,-0.602) -> (-3.851,-1.187)` | 0.83 m | NW 315.2° | **SW light well #2, front cheek** |
| 3 `(-3.851,-1.187) -> (-1.352,-3.675)` | 3.53 m | SW 224.9° | party wall with 130/134, middle run |
| 4 `(-1.352,-3.675) -> (-0.419,-2.757)` | 1.31 m | SE 135.5° | **SW light well #1, rear cheek** |
| 5 `(-0.419,-2.757) -> (2.045,-5.222)` | 3.49 m | SW 225.0° | **SW light well #1, back** |
| 6 `(2.045,-5.222) -> (1.165,-6.095)` | 1.24 m | NW 315.2° | **SW light well #1, front cheek** |
| 7 `(1.165,-6.095) -> (8.143,-13.059)` | 9.86 m | SW 224.9° | party wall with 130/134, front run |

Resolved into building-local coordinates — `d` the depth back from the South Park
front, `w` the width across from the south-west party wall — the plan is a long
rectangle with three bites taken out of it:

```
  w=7.02 |======================================================|  NE party wall (112)
         |            |####|  <- NE well 1.65 deep              |
  w=5.36 |            +----+                                    |
         |                                                      |
  w=1.34 |        +------+          +--------+                  |
         |   SW#1 |######|     SW#2 |########|  0.84 deep       |
  w=0    |========+------+==========+--------+==================|  SW party wall (130/134)
         d=0    9.86  13.35      16.88   20.72              29.79
        front                                                rear
              NE well spans d = 9.48 .. 11.85
```

So: full 7.02 m width for the first 9.5 m from the street; then the two wells overlap
between **d = 9.86 and d = 11.85** and the plan narrows to **4.01 m**; it widens again,
takes a shallower 0.84 m bite on the south-west between d = 16.88 and 20.72, and runs
plain to the rear.

That waist is the building. It is why the leasing copy can promise light on three sides
of a plank wedged between two party walls, it is the "atrium garden", and it is the
silhouette a top-down camera reads first. **Extrude the polygon literally; never
approximate it with a box.**

Because of the 45° heading the axis-aligned bounding box is ~26.0 × 25.9 m for a
building 6.9 m wide. That is correct, and it is worth stating in `REPORT.md` because it
looks like an error.

### 2.4 What each side shows

**South-east (South Park front)** — the hero elevation and the only one with good
evidence. From the Hawthorne Group photograph (Sept 2025), straight on and unobstructed
except by a street tree:

- **Horizontal wood siding**, wide boards (~200 mm exposure) with crisp shadow lines,
  painted a **cool mid gray with a faint green cast** — roughly `#8e9791` off the
  photograph. Every part of the front is this one colour: walls, eave, gate frame.
- A **projecting shed eave** across the full 6.9 m width at the top, carried on
  **exposed rafter tails** (six or seven are visible as dark blocks under the sloping
  soffit), with a thin light fascia along its outer edge and a plain frieze band where
  it meets the wall. This is the building's only ornament and its strongest single
  detail.
- **Upper floor:** a **two-part window group** set toward the north-east side, both
  sashes double-hung with a horizontal transom bar, light-coloured frames in a shared
  wide trim surround with a projecting sill. The south-west half of the upper wall is
  **blank siding**. There is a further narrow opening at the extreme south-west edge,
  partly hidden by the tree.
- A **belt course** — a projecting horizontal band — runs the full width at the floor
  line between the two storeys.
- **Ground floor**, south-west to north-east: a flush door panel; then a **recessed
  entrance bay closed by a tall dark expanded-metal security gate** carrying the
  number **126**; then two **tall multi-pane windows** (a grid of small lights,
  industrial in character, light frames) sitting on a continuous sill, with a plain
  siding spandrel below them down to the sidewalk.
- The whole front is **one flat plane** — no bay window, no projection except the eave.

**North-east (party wall with 112 South Park)** — 9.48 m + 17.89 m of wall shared with
the neighbour at a 0.6 m gap, interrupted only by the light well. A party wall carries
no openings; this is a **blank wall** and that is a free win. In the photograph the
party line is completely covered by a dense climbing vine growing on 112's side — **do
not model the vine**, it belongs to the neighbour.

**South-west (party wall with 130/134 South Park)** — 9.86 m + 3.53 m + 9.03 m of wall
at a ~0.6 m gap, interrupted by the two light wells. Blank, same reasoning. 130/134 is
three storeys and rises about 4.5 m above this building's roof, which is why the
photograph shows a tall pale flank wall over 126's south-west shoulder — again, the
neighbour's, not ours.

**The light wells** — the only elevations besides the front and rear that can carry
windows, and the reason the building has "3 sides of window line". Treat their inner
faces as glazed: a stacked pair of openings in each well cheek and back. Their inner
surfaces should be a **lighter** colour than the outside walls — that is what a light
well is for, and it is what makes them read as voids rather than dents from above.

**North-west (rear)** — 6.99 m onto a mid-block yard, nearest neighbour 5.53 m away.
No photograph was found. Service elevation: expect a door and a few plain openings.
*Inferred.*

**Top** — a flat roof at 7.32 m, and the LiDAR says it is genuinely flat: σ 0.64 m over
715 cells with the mode and the median both landing on 7.32. No usable aerial was
obtained (2.2), so the roof's *composition* is inferred, but its *level* is measured and
solid. The LoopNet listing's "skylights and windows on 4 sides" is the only positive
evidence of what sits on it, and skylights are exactly what a 30 m deep plan needs.

### 2.5 Recognition cues (ranked)

1. **The proportion** — 6.9 m wide, 29.8 m deep, on a 45° heading. A plank on edge.
2. **The waist** — the two opposing light wells pinching the plan to 4.01 m about ten
   metres in. Measured, unusual, and the first thing a top-down camera reads.
3. **The projecting bracketed eave** over the street front — the only ornament, and the
   thing that says "1907 wood-frame" at a glance.
4. **Gray painted horizontal siding**, low and quiet between a three-storey neighbour on
   one side and a taller storefront on the other.
5. The narrow front's own composition: dark gated entrance bay on the south-west third,
   two tall multi-pane windows on the north-east two thirds.

Cues 1 and 2 are read from above; 3, 4 and 5 from the street. That is a healthier split
than most buildings in this set get, and the asset should serve both.

### 2.6 Miniature translation

**Preserve**

- The 6.9 × 29.8 m proportion and the 45° heading, exactly
- All three notches as true full-height voids, at their measured positions
- The eave's projection and its rafter rhythm
- The front's three-part ground floor and its north-east-weighted upper window group
- Blank party walls

**Simplify / exaggerate**

- The waist is where semantic exaggeration is spent: deepen each well by ~0.15 m and
  keep their inner faces conspicuously lighter than the outer walls, so the notch reads
  as a bright slot from the aerial camera rather than as a shadow line
- Individual siding boards become a flat colour with **three or four shallow proud
  bands** implying the board rhythm on the front only — never modelled board by board,
  and never on the party walls
- The eave becomes one clean chunky slab with **five** rafter blocks, not seven
- The multi-pane ground-floor windows become two clean recessed panes with a single
  cross mullion each — the small-pane grid does not survive at this scale
- The upper window group becomes two openings in one surround
- Roof clutter becomes two skylights, one mechanical pair and one hatch — nothing else
- The security gate becomes one flat dark recessed panel with the frame proud of it;
  no mesh geometry
- Downpipes, wires, signage, the neighbour's ivy: dropped

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not
a straitjacket — adjust after the first aerial review render.

1. Body: extrude the 2.3 footprint from z=0 to **z=7.32**, `Toy_steel`. All three
   notches come free with the polygon — do not fill them.
2. Light-well linings: inset faces on the three notch backs and cheeks, `Toy_stone`,
   0.1 m proud so they read separately from the body colour. Two stacked openings
   (0.9 × 1.4 m, `Toy_glass`, recessed 0.15 m) in each well back.
3. Ground floor, z=0 to z=3.6, **south-east front only**: a 2.2 m wide recessed
   entrance bay at the south-west end (recess 0.25 m, `Toy_roofd` gate panel, `Toy_trim`
   frame proud 0.1 m, `Toy_ink` reveal); then two windows 1.5 × 2.0 m on a continuous
   sill at z=1.0, `Toy_glass`, recessed 0.2 m, each with one 0.08 m `Toy_trim` cross
   mullion.
4. Belt course at z=3.6: a 0.18 m proud, 0.25 m tall `Toy_trim` band across the front
   only.
5. Upper floor, z=4.5 to z=6.3, front only: a two-part window group in one 3.4 m wide
   `Toy_trim` surround set toward the north-east, openings 1.3 × 1.8 m, `Toy_glass`,
   recessed 0.15 m, on a 0.12 m proud sill. One narrow 0.7 × 1.6 m opening at the
   south-west edge. The rest of the upper front is plain.
6. Siding rhythm: three 0.05 m proud, 0.6 m tall `Toy_steel` bands across the front
   between the belt and the frieze — just enough to catch light. Front only.
7. Frieze band at z=6.7, 0.35 m tall, 0.1 m proud, `Toy_trim`, full width of the front.
8. **Front eave**: a slab across the full 6.90 m front, projecting **1.0 m** out over
   the sidewalk, from z=7.1 at its outer edge rising to **z=7.6** where it meets the
   wall. Top face `Toy_roofd`, soffit `Toy_ink`, outer fascia 0.15 m `Toy_trim`.
   Five 0.12 × 0.2 m `Toy_ink` rafter blocks under the soffit, evenly spaced. **This
   sets the bounding-box top and must land exactly on 7.6.**
9. Roof deck at z=7.32, `Toy_roofd`, with a 0.25 m `Toy_steel` upstand around the whole
   ring except where the eave meets it.
10. Roof furniture, **all of it below 7.6 m** — the eave crest is the bounding-box top
    and nothing on the deck may exceed it: two skylights over the deep plan at roughly
    d = 17 m and d = 24 m (1.6 × 1.2 m, `Toy_trim` kerb z 7.32–7.40, `Toy_glassl`
    glazing z 7.40–7.54); one roof hatch 1.0 × 0.9 m `Toy_roofd` to z 7.52 at d ≈ 21 m;
    one vent cowl r 0.3 m `Toy_steel` to z 7.54 at d ≈ 14 m.

    **No rooftop mechanical plant.** The 0.7 m HVAC blocks this recipe carried in its
    first draft would have stood at 8.02 m, above the crest — and more to the point,
    nothing in the evidence supports them. The LiDAR argues the other way: σ 0.64 m
    over 715 cells with the mode and median both pinned at 7.32 m is what a *clean*
    roof measures, and a pair of 0.7 m units on a 6.9 m wide deck would have widened
    that distribution visibly. Inventing plant here would be inventing detail on the
    one elevation the dossier admits it cannot see (2.15). The roof composition is
    carried by the two light wells biting in at the waist, which is where it belongs.
11. Rear elevation: one 1.0 × 2.2 m door (`Toy_roofd`, recessed 0.15 m) and two small
    0.8 × 1.0 m `Toy_glass` openings on the upper floor. Nothing else.
12. Bevel 0.12 m, 2 segments.

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_steel` | `#9aa0a6` | all four walls, siding bands, roof upstand |
| `Toy_stone` | `#d9d2c2` | **light-well linings** — the value contrast that makes the wells read from above |
| `Toy_trim` | `#f3efe6` | window surrounds, sills, belt course, frieze, eave fascia, skylight kerbs |
| `Toy_glass` | `#2a4d73` | all windows, front and rear and in the wells |
| `Toy_glassl` | `#6f95b8` | **the two roof skylights** |
| `Toy_roofd` | `#45454a` | roof deck, eave top face, security gate panel, rear door, roof hatch |
| `Toy_ink` | `#3a3530` | eave soffit and rafter blocks, all window and door reveals |
| `Toy_glassl_Glow` | `#6f95b8` | **the lit skylights at night** |
| `Toy_glass_Glow` | `#2a4d73` | the light-well openings and two front windows, lit |

The siding is `Toy_steel` (`#9aa0a6`) rather than `Toy_verdigris` (`#9fb8a8`) even
though the real paint has a faint green cast, for the reason the style bible's §7 gives
and 380 Brannan and 135 South Park both applied: a whole building rendered in a
saturated hue becomes an accent rather than a neutral. `#9aa0a6` is the palette's
nearest true neutral to the measured `#8e9791` and it keeps this building reading as
background fabric between its louder neighbours. Record the choice in `REPORT.md`. If
the aerial review render shows it reading too cold beside the warm SoMa roofs,
`Toy_verdigris` on the front plane only is the correction — not a whole-body swap.

**Night state (required).** Glow surfaces must be thin shells proud of the opaque
glazing — the app renders `_Glow` in a separate layer that is ~12% alpha by day, so a
primary surface must never be authored as glow.

**Hero glow: the waist.** Light the two skylights and the openings inside the light
wells, so that from the app's aerial camera at night this building reads as a long dark
plank with a **bright slot burning across its middle** — the night statement of exactly
the same identity cue that carries the day. Supporting accent: two lit windows on the
South Park front, not all of them. Nothing else glows.

This is the whole argument for building this asset. A 7.3 m gray box on a SoMa block is
invisible; a 7.3 m gray box with a lit notch through its waist is a thing you can point
at from the air.

### 2.9 Top surface

A flat roof 7.3 m up in a district the camera flies over constantly, and one of this
asset's two primary elevations. Composition, front to rear: the eave's darker slab
oversailing the street edge; the deck running back as a long clean dark plane inside its
light upstand ring; the two wells biting in from opposite sides at the waist, their
`Toy_stone` linings catching light where the deck does not; the vent cowl; the first
skylight; the hatch; the second skylight; and the shallower third well taking its bite
from the south-west near the rear. Keep the deck value clearly darker than the upstand,
the well linings and the skylights, so all four read separately from above.

The roof is deliberately **sparse** — see 2.7 step 10. On a plan this narrow the two
wells are the composition, and adding plant to fill the deck would both break the 7.6 m
crest and invent detail the evidence does not support.

### 2.10 Scope

**In the GLB:** the single 1907 building — wood-frame shell on the measured footprint,
all three notches, the front eave, all openings, roof deck and roof furniture

**Not in the GLB:** South Park (street or park), 112 and 130/134 South Park, the
neighbour's climbing vine on the north-east party line, the mid-block rear yard, street
trees, sidewalk, vehicles, people, plinths, cameras or lights

### 2.11 Triangle budget

Cap 7,000 — below 135 South Park's 8,000, because this building has a simpler shell and
only one decorated elevation, though the 16-vertex polygon and three notches cost more
than a plain box. Suggested split: body, notches and upstand ~2.5k; front ground floor
~1k; front upper floor and siding bands ~1k; eave and rafters ~800; light-well linings
and their openings ~800; roof furniture ~700; rear ~200.

### 2.12 Draft manifest entry

```json
{
  "id": "126-south-park",
  "file": "126-south-park.glb",
  "anchor": [
    -122.3945863,
    37.7816006
  ],
  "targetHeightM": 7.6,
  "cat": 3,
  "name": "126 South Park",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

`dims` and `tris` are placeholders until the asset is built and validated.

### 2.13 Integration notes (for later, not this task)

- **New landmark, Case B.** Add a `pipeline/lib/landmarks.mjs` entry
  (`id: '126SouthPark'`) and re-bake the affected tiles, or the baked procedural
  building on this exact footprint will intersect the GLB.

- **`exclude: 3.5`.** Sized against the metric `excluded()` in `pipeline/buildings.mjs`
  actually uses — *the ring centroid **or** any ring vertex inside the circle*.
  Measured from this anchor:

  | | nearest vertex | centroid |
  |---|---|---|
  | own footprint (OSM way/124884348) | 2.78 m | 0.01 m |
  | own footprint (DataSF `SF3775061`) | 2.32 m | 2.19 m |
  | **nearest neighbour (OSM way/124884354, 112 South Park)** | **4.67 m** | 6.36 m |
  | nearest neighbour (DataSF `SF3775060`, 112 South Park) | 4.85 m | 6.27 m |
  | next nearest (DataSF `SF3775062`, 130/134) | 4.97 m | 10.42 m |
  | next nearest (OSM way/124884351, 130/134) | 5.53 m | 11.92 m |

  The bake reads DataSF first and gap-fills from Overture (which carries OSM geometry),
  so both rows bind. Our own ring is caught by the **centroid** test in both sources
  (0.01 m and 2.19 m), so the radius only has to clear 2.19 m — and it must stay under
  **4.67 m** or it starts eating 112 South Park. **3.5 m sits in the middle** of that
  window, with 1.31 m of headroom over our own DataSF centroid and 1.17 m below the
  nearest neighbour vertex.

  Note the happy accident that makes this possible: on a 29.8 m long sliver the area
  centroid sits ~15 m from either end, so the party-wall neighbours' *vertices* stay
  4.7 m away even though their *walls* are 0.6 m away. A squarer building wedged between
  the same two neighbours would have had no valid window at all.

  **Verify empirically during the re-bake**: procedural footprints dropped must be
  **exactly one**, and audit 1.6 must report no intrusion. If the count is 0 the radius
  is under our own ring and must go up; if it is 2 or more it is eating a neighbour and
  must come down.

- `loadRadius`: the skill's default formula gives `max(2500, 7.6 * 30) = 2500` m. Take
  the default.

- **`camera` is not optional** — `context.mjs` bakes it straight into
  `context/landmarks.json` and `camera.js` reads `preset.yaw` unconditionally, so
  omitting it stops the whole city booting. `camera.js` places the eye at
  `target + distance * (sin yaw, ., cos yaw)` with `+x` east and `+z` south, so to face
  the south-east front the camera must stand to the south-east: **yaw 45**. Suggested
  `{ distance: 130, yaw: 45, pitch: 26 }` — the building is 7.6 m tall but 29.8 m long,
  so it needs more distance than its height alone implies.

- **This is the eighth South Park address in the manifest.** The concern first raised in
  380 Brannan's 2.13 and repeated in 135 South Park's is now unavoidable: a manifest of
  individually authored SoMa row buildings will not stream well, and this one — 195 m²,
  two storeys, one decorated elevation — is squarely a kit candidate rather than a
  landmark. It is being built as a landmark for consistency with the seven siblings
  already in flight. **The kit/instancing route (`KIT-INTEGRATION-PROMPT.md`) should be
  decided before a ninth is planned**, and this note should be the last time it is
  raised as a suggestion rather than a decision.

- **Batch mode applies.** Seven other South Park addresses are in flight on their own
  branches. Follow "Batch mode" in `docs/asset-pipeline/ADDRESS-TO-ASSET.md`: run the
  bake and the full QA on it, then `git checkout -- app/public/tiles api/_data` before
  committing, and hand off a source-only branch.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Bounding-box top exactly 7.6 m (loader scale lands at 1.0)
- [ ] Dimensions plausible in meters and consistent with 2.1 (XY bbox ~26.0 × 25.9 m is expected for a 6.9 m wide building at 45°)
- [ ] All three notches are real voids in the exported geometry, not filled recesses
- [ ] The waist measures 4.0 m ± 0.1 m at its narrowest
- [ ] No openings anywhere on either party wall outside the light wells
- [ ] Triangles at or under 7,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the skylights, the light-well openings and two front windows; glow shells proud of opaque glazing
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (per-object signed volume for the union of solids; ray test residual <= 0.15%)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + contact sheet + night render regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed, with the roof's
      confirmed/unconfirmed status stated explicitly

### 2.15 Open questions and risks

- **The roof is unverified, and that is this dossier's dominant risk.** Its *level* is
  measured and unusually solid — DataSF LiDAR puts the mode and the median both at
  7.32 m with σ 0.64 m over 715 cells, and the OSM `height=7` tag agrees independently.
  Its *composition* is not. No usable aerial was obtained: Esri World Imagery is washed
  out to near-white at this location at z20 and returns "Map data not yet available" at
  z21. Everything in 2.7 steps 9–10 — the two skylights, their positions, the
  mechanical pair, the hatch — is a reasonable furnishing of a deep plan, not an
  observation. The one piece of positive evidence is the LoopNet listing's "skylights
  and windows on 4 sides", which establishes that skylights exist but not where or how
  many. **Find an aerial before committing the roof, and say in `REPORT.md` what you
  confirmed.** Note that this matters more than usual here, because the roof carries the
  night state.

- **The LiDAR maximum of 10.16 m is not a feature — do not model to it.** The
  distribution rules it out: mean 7.34 m, σ 0.64 m, so 10.16 m sits 4.4σ above the mean
  with the mode and median both pinned at 7.32. The minimum of 3.74 m is 5.6σ below and
  is equally spurious. Both are what 50 cm LiDAR cells do at a polygon edge when the
  neighbours on *both* long flanks are taller — 130/134 South Park reaches 11.77 m
  0.6 m away on one side, and 112 reaches 8.04 m 0.6 m away on the other. A 6.9 m wide
  building squeezed between two taller ones has almost no cells that are not edge cells.
  **The roof is flat at 7.32 m.**

- **The eave crest at 7.6 m is inferred, and it is the number the whole asset is
  normalized to.** The deck is measured at 7.32 m; the +0.28 m is read off the
  photograph's proportions, where the eave clearly rises above the roof line as it meets
  the wall. A photograph taken from the sidewalk looking up cannot settle whether a
  shed hood slopes down-and-out (crest at the wall, as assumed here) or up-and-out
  (crest at the fascia). The assumption chosen is the commoner detail and the one that
  sheds water to the street. **If a better source settles it the other way, the crest
  stays at 7.6 m and only the slope direction flips** — the target height does not move.

- **LoopNet's "3 Stories, 5,442 SF" is rejected.** Against it: 19 consecutive assessor
  rolls 2007–2025 all recording `number_of_stories = 2.0`; both building permits on lot
  061 (1999, 2023) recording 2 existing storeys; and a photograph showing two storeys
  under a single eave. 5,442 SF over a 2,143 SF lot needs three full floors, which is
  not what the building is. The likeliest explanation is that the listing counts a
  basement or an above-garage mezzanine, or is simply stale — the same listing dates the
  renovation to 1990. **Build 2 storeys.** This conflict is recorded rather than buried
  because a future agent will hit the same listing.

- **Two architecture-press pages are falsely attached to this address by search.** A
  Perkins&Will project page and an Office Snapshots article, both titled "South Park
  Venture Capital Firm", are returned for queries naming 126 South Park and were
  summarised by the search tool as being at this address. **Both were fetched directly
  and neither contains this address, or any address.** They describe a 16,420 sq ft
  brick-clad 1920s building — roughly four times this building's floor area, and the
  wrong material for a type-D wood frame. Do not let them back in.

- **SF Planning case 2010.0959CV is a different building.** It is returned for this
  address but its own header reads `Project Address: 147 SOUTH PARK AVENUE`,
  `Block/Lot: 3775/031` — the far side of the oval. Its "demolish the existing
  two-storey single family dwelling" does **not** apply here.

- **The light wells are measured in plan but not in section.** Whether they run the full
  two storeys, are roofed over at ground level, or are planted courts is unresolved.
  The Hawthorne Group's phrase "an atrium garden" implies at least one is open and
  planted at the ground. Modelling both as full-height voids is the safe choice: it is
  right at the roof, which is what the camera sees, and defensible at ground level.
  **Do not model planting inside them** — it would be the only vegetation in the asset
  and would break the scope rule in 2.10.

- **DataSF and OSM disagree about the footprint area** (178.6 m² vs 195.3 m²), while
  agreeing on position to 2.19 m at the centroid and 0.58 m at the nearest vertex. The
  difference is concentrated at the notches: DataSF's 2010 trace cuts them more
  generously. **Model the OSM footprint** — it is the later trace, it matches the
  assessor's 2,143 SF lot much more closely than DataSF's 1,922 SF equivalent, and a
  building that covers its whole lot is what the block face shows.

- **This building is a kit candidate being built as a landmark.** See 2.13. It is not a
  risk to the asset, but it is a risk to the manifest, and it is the eighth time.

- No architect is recorded for the 1907 building in any source consulted, and the
  building carries no name. The registered entities at this address run back to
  "Maxwell Myers Co." in 1948, which is colour but not evidence.
