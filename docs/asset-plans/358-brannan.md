# 358 Brannan Street — SF-SIM asset plan

A 1910 industrial through-lot in SoMa, one lot northeast of 350 Brannan and two
southwest of the big cream warehouse at 362-366. It is the **narrowest** building the
manifest has ever carried: a single 25-foot lot, 6.93 m of Brannan frontage running
25.2 m clean through the block to a second front on the Varney Place alley. Two
storeys, terracotta-red paint, and one perfect identity cue — a **canted bay window**
hanging over the roll-up freight door, with a batting-cage sign band underneath it.

It is the opposite design problem from 380 Brannan, which is a broad box that needs a
stripe to be memorable. This one is memorable by proportion: a red slot between two
pale warehouses. The brief is "the block's skinniest building", and the whole job is
protecting that slot from being widened for convenience.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/358-brannan/`. This document is the plan only: Part 1 is the runnable task
prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `358-brannan` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3936350, 37.7809258` |
| Target height | **9.6 m** to the bay's cornice cap; front parapet 9.0 m; front roof deck 8.4 m; rear roof deck 7.7 m |
| Footprint | 6.93 m (Brannan frontage, SE) x 25.20 m deep; 166.5 m2, measured |
| Triangle cap | 7,000 |
| Category | `19` (industrial) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 358 Brannan Street GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of 358 Brannan Street in San Francisco and deliver
it as a downloadable, validated GLB.

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
7. `artifacts/380-brannan/` — the closest reference implementation: the same block,
   the same era, the same secondary-building detail budget, and a build script whose
   footprint/panel/roof helpers this asset should reuse rather than reinvent
8. `docs/asset-plans/358-brannan.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Must capture

- A **very narrow, deep** two-storey box: 6.93 m of street frontage, 25.2 m of depth.
  The slenderness IS the building — never widen it to make the facade easier to compose
- The **canted bay window** projecting from the second floor of the Brannan elevation,
  centred over the freight opening: two windows on the flat face, one on each angled
  cheek, and a small cornice cap that rides slightly proud of the parapet
- **Terracotta / brick-red painted** Brannan front against pale party-wall flanks
- The dark **sign band** immediately under the bay (the batting-cage tenant's board)
- Ground floor on Brannan: a wide grey roll-up freight door plus a narrow pedestrian
  door at the northeast end
- A **second front on Varney Place**: a full-width slate blue-gray timber storefront of
  multi-light industrial glazing with a pedestrian door and a roll-up freight door, under
  a brown horizontal wood-sided upper storey
- A **two-level roof**: the rear roof deck sits about 0.7 m lower than the front block,
  and it is a used roof deck (railing), not a blank tray

## Research 358 Brannan Street independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world orientation,
and gather references covering:

- Both fronts — Brannan (southeast) and Varney Place (northwest). This is a through-lot;
  a model built from the Brannan photograph alone will have an invented rear
- Aerial and roof views (the two-level roof, the roof deck, skylights)
- Ground-level views, day and night
- The exact height of the Brannan parapet and of the bay cap — the weakest numbers in
  this dossier (see 2.15)
- Whether the bay is three-sided canted or a square oriel

Prefer architect/engineer publications, owner or institutional material, planning and
permitting documents, architectural press, geolocated photography, and aerial/satellite
imagery. Never rely on a single photograph, a single AI-generated image, or a single
unsourced 3D model. Separate verified facts from visual inference; if sources disagree,
document the disagreement and decide.

**Three source conflicts are already known and resolved in 2.1 — re-check them, do not
silently re-inherit the wrong value:** the OSM footprint (way 124890324, `source=Bing`)
is **wrong** and must not be used — it traces a 115 m2 stub that never reaches Varney
Place, where the DataSF LiDAR footprint and the Assessor's 1,760 sq ft lot area agree on
166 m2 through the block; the DataSF LiDAR `hgt_maxcm` of **13.32 m is not this
building** (see 2.15); and the Assessor calls the use "Industrial" while every building
permit since 2012 calls it a "1 family dwelling" — both are true of a live/work
conversion, and the *form* is industrial.

## Create a reference dossier

Write `artifacts/358-brannan/REFERENCE.md` containing: source links and what each
establishes; verified dimensions and location; orientation; observations from all four
sides and above; the 3-5 strongest recognition cues; features to preserve; features to
simplify; uncertainties and conflicting evidence. A contact sheet of attributed
reference thumbnails is welcome if legally permissible — do not commit copyrighted
full-resolution imagery.

## Make your own design decisions

Follow the conversion process in `docs/styles/miniature-toy.md` §22: identify the
recognition cues, strip nonessential information, rebuild the massing from a few
confident volumes, exaggerate only the signature features, simplify the facade into
broad rhythms, deliberately design every surface visible from above, evaluate from the
app's high three-quarter aerial camera, then simplify again.

This is a **secondary building** in the style bible's detail budget (§21), and a small
one. Clear massing, one strong facade rhythm, a simple designed roof, and exactly one
identity cue carried hard — the bay. Resist adding hero-tier ornament, and resist the
temptation to compensate for the small footprint with extra detail.

The finished asset must be immediately recognizable as 358 Brannan Street, consistent
with the real building from all four sides and above, architecturally credible, and a
premium handcrafted miniature — not photorealistic, not voxel art, not generic
low-poly, and never accurate in one view while invented in the others.

## Scope of the exported asset

Export the single 1910 building: both fronts, both flanks, the bay, the roof and its
furniture.

Do not include unrelated surrounding city geometry: Brannan Street, Varney Place, the
neighbouring buildings at 350 and 362-366, South Park, street trees, the sidewalk,
parked cars, people, plinths, cameras or lights. Temporary context may appear in review
renders but must not leak into the GLB.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary `.glb`;
real-world meters; origin at base center; minimum geometry Z ~ 0; applied transforms;
no negative scales; outward normals; no duplicate or foreign geometry; no image
textures; no transparency; flat-color materials named `Toy_*` from the project palette;
`_Glow` suffix only on surfaces that glow at night; no `Toy_body`; no cameras, lights,
animations, armatures or constraints; no external dependencies; at most 7,000 triangles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model drops
into the city at its real-world heading — the loader applies no rotation (`placeGeneric`
in `app/src/assets.js` only scales and positions). The Brannan Street front faces
**southeast, bearing 135.3°**; the Varney Place rear faces **northwest, 315.3°**. The
building is rotated about 45° off the world axes, so build directly on the measured
footprint rectangle in 2.3 rather than modelling an axis-aligned box and rotating it.
Record the measured heading in `REPORT.md`.

**Height normalization:** the tallest geometry in the export (the bay's cornice cap)
must land at exactly **9.6 m** so the loader's `targetHeightM / measuredHeight` scale
is 1.0.

## Reproducible Blender workflow

Blender 5.2 LTS. Headless: `blender -b --python script.py -- args`.

Keep `artifacts/358-brannan/build_358_brannan.py` (deterministic build script),
`artifacts/358-brannan/358-brannan.blend`, and `artifacts/358-brannan/358-brannan.glb`.
The script must rebuild the model reliably enough for future revision. Do not modify or
rename an unrelated existing GLB to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras: `358-brannan-top.png`,
`358-brannan-north.png`, `358-brannan-east.png`, `358-brannan-south.png`,
`358-brannan-west.png`, plus `358-brannan-contact-sheet.png`, at least one high
three-quarter aerial beauty render `358-brannan-aerial.png`, and a night render
`358-brannan-aerial-night.png`.

The four elevations must share scale, framing, lighting, exposure and projection; use
orthographic or long-lens cameras; label directions from the researched orientation; the
top view must clearly show the two roof levels, the parapet ring, the roof deck railing
and the skylights; the aerial view uses the style bible's camera assumptions (30-50
degrees down, long lens). Simple tabletop lighting, neutral warm background, minimal
depth of field, and every image must depict the same exported model.

Note that the axis-aligned elevation renders will each show the building at 45°, and the
"north"/"south" views see a flank and a front together. That is the expected consequence
of the real heading, not a camera error.

## Validate the exported GLB

Re-import `358-brannan.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture count,
camera count, light count, animation count, applied-transform status, negative-scale
status, normal-orientation status, unexpected geometry, and per-material contract
compliance. Render at least one review image from the re-imported asset. Write
`artifacts/358-brannan/validation.json` and `artifacts/358-brannan/REPORT.md`.

Note that the axis-aligned XY bounding box will be roughly **22.7 x 22.8 m** even though
the building is 6.93 x 25.20 m — that is the expected consequence of a ~45° real-world
heading, not a scale error.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this draft
entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "358-brannan",
  "file": "358-brannan.glb",
  "anchor": [
    -122.3936350,
    37.7809258
  ],
  "targetHeightM": 9.6,
  "cat": 19,
  "name": "358 Brannan Street",
  "estimated": true,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a separate, explicitly requested job — run `docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in `docs/asset-plans/358-brannan.md`.
````

---

## Part 2 — Research and design dossier

Compiled 12 August 2026 from the sources in 2.2. Values marked *inferred* or *estimated*
are visual or derived, not published figures — the executing agent must re-verify
anything it relies on.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Block / lot | 3775 / 017 | DataSF parcels `acdm-wktn` — `blklot=3775017`, `from_address_num = to_address_num = 358 BRANNAN ST`, active, mapped 1998-07-01 |
| Built | 1910 | SF Assessor secured roll, block 3775 lot 017 (identical in every year 2007-2025) |
| Storeys | **2** | SF Assessor roll (`number_of_stories = 2.0`) **and** all three building permits (`number_of_existing_stories = 2`) — no conflict here, unlike 380 |
| Use (assessor) | Industrial | SF Assessor roll `use_definition` |
| Use (permits) | "1 family dwelling" | SF permits 2012/2014/2022 — a live/work conversion inside an industrial shell |
| Lot area | 1,760 sq ft = 163.5 m2 | SF Assessor roll |
| Building area | 2,860 sq ft = 265.7 m2 | SF Assessor roll; commercial listings agree. 1.63x the footprint — two floors over most of the lot |
| Footprint | 166.5 m2; 6.93 m (SE frontage) x 25.20 m deep; 95.3% rectangular fill | DataSF LiDAR building footprint `SF3775017`, reprojected — **measured**; agrees with the 163.5 m2 lot area to 1.8% |
| Rear roof height | 7.74 m above ground | DataSF LiDAR `hgt_median_m` — **measured** |
| Ground elevation | 10.27 m (NAVD88) | DataSF LiDAR `gnd_min_m` — app terrain handles this, not the asset |
| Through-lot | Brannan Street front, Varney Place rear | SF permit 2022-10-21 ("remove storefront & brannan facade, legalize varney place facade"); tenant site ("ENTRANCE IN BACK ALLEY ON VARNEY"); both Street View panoramas |
| Zoning | CMUO (Central SoMa mixed use — office) | DataSF parcels |
| Frontage heading | Brannan front faces 135.3° (SE); Varney rear faces 315.3° (NW) | measured from the footprint OBB |
| Current occupants | The Natural (batting cage & bullpen, ground floor); Goff Photography | tenant website, Google Maps "At this place", OSM node 13765490841 |
| Marketed features | roof deck/patio, two breakout spaces, rear loading access, one roll-up door, full kitchen | LoopNet / Showcase listing copy |

### 2.2 Sources

- `https://data.sfgov.org/resource/acdm-wktn` (DataSF Parcels) — **the address-to-lot link**: `3775017 = 358 Brannan St`. This is what makes lot 017 the right footprint; neighbours are 016 = 350, 018 = 362-366, 020 = 370, 021 = 372-374, 022 = 376-380
- `https://data.sfgov.org/resource/ynuv-fyni` (DataSF Building Footprints, LiDAR-derived) — polygon `SF3775017`, the 7.74 m median height, the 10.27 m ground
- `https://data.sfgov.org/resource/wv5m-vpq2` (SF Assessor Historical Secured Property Tax Rolls) — 1910, 2 storeys, 2,860 sq ft on a 1,760 sq ft lot, Industrial
- `https://data.sfgov.org/resource/i98e-djp9` (SF Building Permits) — 2012-12-12 kitchen/powder-room remodel; 2014-02-28 final inspection; **2022-10-21** planning-enforcement permit #2020088enf, "remove storefront & brannan facade, legalize varney place facade"
- https://www.openstreetmap.org/way/124890324 — address confirmation only; its geometry is `source=Bing` and **wrong** (see 2.15)
- Google Street View, Brannan Street pano (capture **May 2025**) — the terracotta front, the canted bay, the sign band, the roll-up door, the "358" plate, the parapet lower than both neighbours
- Google Street View, Varney Place pano (capture **Jan 2025**) — the rear: slate blue-gray multi-light timber storefront, pedestrian door, roll-up freight door, steel header with conduit and floodlights, brown horizontal wood siding above, light posts at the roof line
- Google Maps satellite (Vexcel imagery, 2026) — the two-level roof, the light membrane deck, scattered roof furniture
- https://www.thenaturalsf.com/ — "358 Brannan St… ENTRANCE IN BACK ALLEY ON VARNEY", establishing the through-lot independently of the permit
- LoopNet / Showcase listing "358 Brannan St" — 2,860 sq ft, 1910, 2 storeys, roof deck, roll-up door, rear loading

### 2.3 Orientation and placement

The building sits mid-block on the northwest side of Brannan Street and runs clean
through to Varney Place. It is rotated about 45° from the world axes, like the whole
SoMa grid.

The DataSF LiDAR polygon has 18 vertices, but they are scan noise on what is plainly a
rectangle: the minimum-area OBB has **95.3% fill** and matches the assessor's lot area to
1.8%. Build the clean rectangle, not the noise — and say so in `REPORT.md`.

Footprint rectangle, in Blender coordinates (metres, `+X` east, `+Y` north),
counter-clockwise, already centred on the anchor `-122.3936350, 37.7809258`:

```
( -6.406,  11.391)
(-11.328,   6.517)
(  6.406, -11.391)
( 11.328,  -6.517)
```

Edges, with outward normals:

| Edge | Length | Faces | Elevation |
|---|---|---|---|
| `(-6.406,11.391) -> (-11.328,6.517)` | 6.93 m | NW 315.3° | **Varney Place rear** |
| `(-11.328,6.517) -> (6.406,-11.391)` | 25.20 m | SW 225.3° | southwest flank (party wall to 350) |
| `(6.406,-11.391) -> (11.328,-6.517)` | 6.93 m | SE 135.3° | **Brannan Street front** |
| `(11.328,-6.517) -> (-6.406,11.391)` | 25.20 m | NE 45.3° | northeast flank (party wall to 362-366) |

Because of the 45° heading the axis-aligned bounding box is ~22.7 x 22.8 m for a
building that is 6.93 x 25.20 m. That is correct.

### 2.4 What each side shows

**Southeast (Brannan Street front)** — The hero elevation, and only about seven metres
of it. A **terracotta / brick-red painted** wall two storeys high, noticeably lower than
the pale warehouses on both sides, so it reads as a red slot in a cream wall. Top to
bottom: a plain flat parapet with a slight rise at the centre; a **canted bay window**
projecting from the second floor — a flat face carrying two tall windows, plus one
window on each angled cheek, all in light frames, capped by a small cornice; a dark
**sign band** running the width of the bay immediately below it, carrying the tenant's
name; then the ground floor — a wide grey **roll-up freight door** occupying most of the
frontage, a small diamond-shaped hanging sign to its right, a narrow **pedestrian door**
at the northeast end, and the "358" number plate above it.

**Northwest (Varney Place rear)** — A second full front, not a back. The ground floor is
a full-width **slate blue-gray painted timber storefront**: a grid of multi-light
industrial sash (three rows of small panes), a pedestrian door left of centre, and a
roll-up freight door filling the right half — this is the batting cage's actual entrance.
A steel header with conduit and floodlights caps it. Above sits a second storey clad in
**brown horizontal wood siding**, and above that, light-coloured posts at the roof line
(the listing's roof deck railing).

**Northeast / southwest flanks** — Party walls, 25 m long, hard against the neighbours at
362-366 and 350. Blind. Pale stucco where any of them is visible at all. Do **not**
invent windows here; the app's aerial camera will see them, and a blank pale wall is the
truthful and the calmer answer.

**Top** — Two levels. The rear (Varney) two-thirds is a light membrane deck at about
7.7 m — the LiDAR median — with the roof-deck railing at its Varney end. The front
(Brannan) third steps up about 0.7 m to 8.4 m inside a parapet at 9.0 m. Scattered roof
furniture: a small skylight run over the second floor, one mechanical block, a hatch.
The camera sees this far more than it sees either front — design it.

### 2.5 Recognition cues (ranked)

1. **Extreme narrowness** — a 6.9 m frontage next to a 20 m and a 25 m one. If the
   silhouette is not startlingly thin, nothing else matters
2. **The canted bay window** over the freight door — the one piece of shape on the
   facade, and the only bay on this side of the block
3. **Terracotta red between two pale warehouses** — the colour contrast does the work at
   thumbnail size
4. The dark sign band under the bay
5. The two-level roof and its used roof deck

### 2.6 Miniature translation

**Preserve**

- The 6.93 x 25.20 m proportion and the real 45° heading, exactly
- The bay's three-sided canted geometry — a flat square oriel would lose the cue
- The two-front condition: Varney is a designed elevation, not a blank end
- The step between the two roof levels

**Simplify / exaggerate**

- The bay is thickened and its cornice cap lifted proud of the parapet (to 9.6 m) so the
  silhouette has one deliberate high point. This is the one place semantic exaggeration
  is spent
- Roughly a dozen small panes per storefront bay become one glazed panel per opening with
  a light frame; individual muntins disappear
- The brown wood siding becomes a flat colour with one shadow reveal at its base, not
  modelled boards
- The diamond hanging sign, the conduit, the floodlights and the drainpipes are dropped —
  all sub-pixel at city scale
- Roof clutter becomes two skylight boxes, one mechanical block, one hatch, and the deck
  railing. Nothing more; this roof is 166 m2 in total

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not a
straitjacket — adjust after the first aerial review render.

1. Body: extrude the 2.3 rectangle from z=0 to z=7.7 (`Toy_stone` walls; this is the
   pale party-wall shell the flanks show), cap `Toy_roofd` — the rear roof deck.
2. Front block: the first 8.5 m of depth measured back from the Brannan edge, z=0 to
   z=8.4, same materials, cap `Toy_roofd` — the upper roof deck.
3. Front parapet: ring around the front block only, z=8.4 to z=9.0, 0.30 m thick, with a
   `Toy_stone` coping.
4. Brannan skin: 0.10 m proud panel on the SE edge, z=0 to z=9.0, `Toy_brick` — the
   terracotta paint. This is the only saturated surface in the asset.
5. Ground floor, Brannan: a 4.4 m wide roll-up door (`Toy_roofd`) from z=0 to z=3.4
   toward the southwest end, and a 1.1 m pedestrian door (`Toy_ink`) at the northeast
   end; a `Toy_stone` lintel band at z=3.6.
6. Sign band: `Toy_ink` panel, full bay width, z=3.9 to z=4.7, with a `Toy_gold_Glow`
   strip inset in it — the night hero.
7. **The bay**: a five-sided canted prism projecting 0.65 m from the front skin, 4.6 m
   wide at the wall and 3.4 m on the flat face, z=4.7 to z=8.9, `Toy_brick`, with two
   `Toy_glass` windows on the flat face and one on each cheek in `Toy_stone` frames;
   cornice cap `Toy_stone` from z=8.9 to **z=9.6** — this sets the bounding-box top and
   must land exactly on 9.6.
8. Varney front: `Toy_slate` storefront panel z=0 to z=4.0 across the full 6.93 m, with a
   3.2 m roll-up door (`Toy_roofd`), a 1.0 m pedestrian door (`Toy_ink`), and two
   `Toy_glass` glazed panels; a `Toy_steel` header band at z=4.0 to z=4.25; above it a
   `Toy_rust` wood-siding panel z=4.25 to z=7.7 with one shadow reveal.
9. Roof: on the rear deck, a railing at z=7.7 to z=8.7 (`Toy_steel` posts and rail) along
   the Varney end and 3 m down each flank; two skylight boxes 2.0 x 1.4 x 0.35 m
   (`Toy_glassl` on `Toy_stone` kerbs); one mechanical block 1.6 x 1.2 x 0.9 m
   (`Toy_steel`); one hatch 1.2 x 1.0 x 0.5 m (`Toy_roofd`).
10. Bevel 0.10 m, 2 segments on the masses; 0.04/1 on applied panels.

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_brick` | `#c96f4a` | the terracotta Brannan front and the bay — **the only saturated surface** |
| `Toy_stone` | `#d9d2c2` | flanks and body, parapet coping, bay cap, window and door frames, skylight kerbs |
| `Toy_slate` | `#6f7883` | the Varney Place timber storefront (palette extension, precedent `380-brannan`) |
| `Toy_rust` | `#a86444` | the Varney upper storey's brown wood siding |
| `Toy_glass` | `#2a4d73` | all windows and glazed storefront panels |
| `Toy_glassl` | `#6f95b8` | skylights |
| `Toy_roofd` | `#45454a` | both roof decks, both roll-up doors |
| `Toy_steel` | `#9aa0a6` | Varney header band, mechanical block, roof-deck railing |
| `Toy_ink` | `#3a3530` | sign band, pedestrian doors, door recesses |
| `Toy_gold_Glow` | `#caa64a` | **the sign band's lit strip** — the night hero |
| `Toy_glass_Glow` | `#6f95b8` | two lit bay windows at night |

Note on the front colour: the real paint is a muted terracotta, between the palette's
`Toy_brick` (`#c96f4a`) and `Toy_rust` (`#a86444`). `Toy_brick` is used because this
building needs its front to *advance* against pale neighbours, which is the opposite of
380 Brannan's problem two lots away — there `Toy_brick` had to be abandoned because it
merged with the coral band. Both choices are recorded so the block reads as two related
but distinct buildings.

**Night state (required).** Glow surfaces must be thin shells proud of the opaque
surface behind them — the app renders `_Glow` in a separate layer that is ~12% alpha by
day, so a primary surface must never be authored as glow. Hero glow: the **sign band
strip** in `Toy_gold_Glow` — a lit sign is exactly what a batting cage open until 20:00
has, and it is the only warm light on this stretch of Brannan. Supporting accent: two of
the four bay windows lit. The Varney front does **not** glow; it is a back alley.

### 2.9 Top surface

166 m2 of roof in two levels, seen constantly from above. The step between them is the
composition: keep the front deck's parapet coping clearly lighter than either deck so the
ring reads, put the railing at the Varney end so the rear deck reads as *used*, and group
the skylights and the mechanical block against the northeast flank so the middle of the
deck stays open. Nothing on this roof should be larger than 2 m — at 6.9 m wide, one
oversized HVAC box would swallow the building.

### 2.10 Scope

**In the GLB:** the single 1910 building — body, front block and parapet, the Brannan
skin and bay, the Varney storefront and wood-sided upper storey, both roof decks and
their furniture

**Not in the GLB:** Brannan Street, Varney Place, 350 and 362-366 Brannan, South Park,
street trees, sidewalk, vehicles, people, plinths, cameras or lights

### 2.11 Triangle budget

Cap 7,000 — smaller than 380 Brannan's 9,000 because the building is a third of the
volume and has one facade of consequence. Suggested split: body, front block and parapet
~1.5k, the bay ~1.5k, Brannan ground floor ~0.8k, Varney front ~1.5k, roof furniture and
railing ~1.2k.

### 2.12 Draft manifest entry

```json
{
  "id": "358-brannan",
  "file": "358-brannan.glb",
  "anchor": [
    -122.3936350,
    37.7809258
  ],
  "targetHeightM": 9.6,
  "cat": 19,
  "name": "358 Brannan Street",
  "estimated": true,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

`dims` and `tris` are placeholders until the asset is built and validated.
`"estimated": true` because the target height is photogrammetric, not published — see
2.15.

### 2.13 Integration notes (for later, not this task)

- **New landmark.** Add a `pipeline/lib/landmarks.mjs` entry (`id: '358-brannan'`,
  `exclude: ~9`) and re-bake the affected tiles, or the baked procedural building on this
  footprint will intersect the GLB. **The exclusion radius must be tighter here than for
  any landmark so far**: the lot is 6.93 m wide and the neighbours' walls are *touching*
  it. A radius sized to the 25 m depth would delete 350 and 362-366 Brannan from the
  baked city and leave two holes in the block. Size it to the half-width plus a small
  margin, verify by eye in the re-baked tiles, and record the number in `REPORT.md`.
- `loadRadius`: the skill's default formula gives `max(2500, 9.6 * 30) = 2500` m. Take
  the default; at 2.5 km a 9.6 m building is far below a pixel.
- 358 and 380 Brannan are now both in the manifest, 100 m apart on the same block face,
  from the same decade and the same building type. Judge them side by side in the aerial
  render — if they read as the same building twice, the narrow one has been widened.
- The kit/instancing question raised in `380-brannan.md` §2.13 applies with more force
  here: this is the second one-off SoMa warehouse in a manifest designed for monuments.
  Two is a pattern worth a decision before it becomes ten.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Bounding-box top exactly 9.6 m (loader scale lands at 1.0)
- [ ] Dimensions plausible in meters and consistent with 2.1 (XY bbox ~22.7 x 22.8 m is expected)
- [ ] Footprint proportion preserved: the building must measure 6.93 x 25.20 m along its own axes
- [ ] Triangles at or under 7,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the sign strip and two bay windows; glow shells proud of the opaque surface
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (per-object signed volume for the union of solids; ray test residual <= 0.15%)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + contact sheet + night render regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

- **The OSM footprint is wrong, and it is the trap in this dossier.** Way 124890324
  (`source=Bing`) traces a 115 m2 stub, 16.7 x 7.2 m, oriented as if the building were
  *wide and shallow* — the opposite of the truth. DataSF's LiDAR footprint (166.5 m2,
  6.93 x 25.20 m) and the Assessor's 1,760 sq ft lot area agree with each other and with
  the through-lot evidence from the 2022 permit and the tenant's own directions. An agent
  that starts from OSM will build a building rotated 90° from reality on a footprint that
  does not reach Varney Place. **Use DataSF.**
- **The target height is estimated, and it is the weakest number here.** No published
  height exists. It is derived by scaling the May 2025 Brannan panorama against the
  measured 6.93 m frontage: parapet ≈ 8.4-9.2 m, roll-up door ≈ 3.4 m. 9.0 m is taken for
  the parapet and 9.6 m for the bay cap, with roughly ±0.6 m of uncertainty. The manifest
  entry is therefore `"estimated": true`.
- **DataSF `hgt_maxcm` = 13.32 m is almost certainly not this building.** The same record
  gives `hgt_median 7.74`, `hgt_mean 8.52`, `hgt_min 4.18`, `std 2.28` over 674 cells. A
  13.3 m maximum with a 7.7 m median on a 166 m2 roof means a few cells, and the taller
  neighbour at 362-366 has a wall directly on the shared boundary. Treat it as
  polygon-edge bleed, not a penthouse. **This is the mirror image of the trap the plans
  README documents** — there, OSM `height` tags *understated* a crest; here a LiDAR
  maximum *overstates* one. Do not build a 13 m tower on a 25-foot lot because of it.
- The 7.74 m median is a real measurement of the *rear* roof, so the two-level roof in
  2.7 is well founded; the 8.4 m front deck that reconciles the median with the mean is
  *inferred*.
- **The 2022 facade permit means photographs disagree by date.** Permit #2020088enf
  ordered the Brannan storefront and facade removed and the Varney facade legalized. The
  May 2025 Brannan pano and the Jan 2025 Varney pano both post-date it, so both show the
  current condition — but any older photograph of this building may show a facade that no
  longer exists. Date every reference.
- Whether the bay is a true three-sided canted bay or a squared oriel is read from a
  single frontal photograph and is *inferred*. It reads canted (visible angled cheeks with
  their own windows); confirm from an oblique view before committing.
- The flanks are assumed blind party walls. The building is hard against both neighbours,
  so this is safe, but the pale colour chosen for them is *inferred* — nothing in the
  references shows either flank.
- No architect is recorded for the 1910 building in any source consulted.
</content>
