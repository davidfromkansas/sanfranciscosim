# 550 Third Street — SF-SIM asset plan

A 1921 two-storey brick-and-timber SoMa warehouse gut-renovated in 2022–25 into
a single-tenant trophy office at the foot of South Park's venture row. The
smallest, lowest landmark in the set — and the first whose identity lives almost
entirely on its roof: five big skylights, a paver walk, and a glass penthouse
pavilion sitting over a garden deck. The app's camera looks down; this building
is designed for that camera.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/550-third/`. This document is the plan only: Part 1 is the runnable
task prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `550-third` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3953409, 37.7804407` (footprint AABB centre, measured) |
| Target height | **11.0 m** (penthouse roof slab; main roof 7.3 m measured, penthouse *estimated*) |
| OSM footprint | 48.4 x 23.0 m bar on the 45.3 deg SoMa grid, 1,070 m2 (OSM way/124889472, measured) |
| Triangle cap | 14,000 |
| Category | `3` (Office) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 550 Third Street GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of 550 Third Street in San Francisco and
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
7. `artifacts/salesforce-tower/` — the reference implementation of this exact
   deliverable (dossier, deterministic build script, validator, renders, report)
8. `artifacts/columbus-tower/` — the closest match in scale and detail budget
9. `docs/asset-plans/550-third.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Must capture

- The long, low warehouse bar running the full depth of the lot from 3rd Street
  back to Ritch Street — 48 m deep, 23 m wide, only two storeys
- The row of five big rectangular roof skylights, the single strongest cue from
  the app's downward camera
- The glass rooftop penthouse pavilion with its thin cantilevered flat roof slab
- The rooftop garden deck at the 3rd Street end: hedge planters, lawn, lounge,
  fire pit, long table
- The 3rd Street elevation: tall solid parapet, painted masonry, two large
  industrial steel-sash window grids either side of a recessed entry, the "550"
  numerals
- The blind party walls with their punched square property-line windows
- Roll-up garage doors reinstated on the Ritch Street rear

## Research 550 Third Street independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- North-east (3rd Street) and south-west (Ritch Street) elevations
- The two long party walls
- Aerial and roof views — the roof is the primary facade here
- Ground-level views
- Day and night appearance
- Publicly available drawings, plans or diagrams
- **The penthouse crest height, which this dossier only estimates.** The main
  roof at 7.3 m is measured (2010 city LiDAR); the 2023–25 penthouse above it is
  inferred from the permit's 2-to-3-storey change and one-storey massing. Any
  better source — planning drawings, a measured elevation, a dated photograph
  against a known neighbour — beats the estimate. Document what you find.
- Which long wall carries the property-line windows (this dossier infers the
  south-east wall from one axonometric)

Prefer architect/engineer publications, owner or institutional material,
planning and permitting documents, architectural press, geolocated photography,
and aerial/satellite imagery. Never rely on a single photograph, a single
AI-generated image, or a single unsourced 3D model. Separate verified facts from
visual inference; if sources disagree, document the disagreement and decide.

## Create a reference dossier

Write `artifacts/550-third/REFERENCE.md` containing: source links and what each
establishes; verified dimensions and location; orientation; observations from all
four sides and above; the 3-5 strongest recognition cues; features to preserve;
features to simplify; uncertainties and conflicting evidence. A contact sheet of
attributed reference thumbnails is welcome if legally permissible — do not commit
copyrighted full-resolution imagery.

## Make your own design decisions

Follow the conversion process in `docs/styles/miniature-toy.md` §22: identify the
recognition cues, strip nonessential information, rebuild the massing from a few
confident volumes, exaggerate only the signature features, simplify the facade
into broad rhythms, deliberately design every surface visible from above,
evaluate from the app's high three-quarter aerial camera, then simplify again.

This building has no skyline silhouette. Its whole job is to be a beautifully
designed roof plane with one crisp glass object on it — §10 (roofs as secondary
facades) is the governing section, not §11 (landmark geometry). Resist adding
tower-like drama it does not have; spend the budget on the skylight rhythm, the
paver walk, the penthouse, and the deck's small clusters of life.

The finished asset must be immediately recognizable as 550 Third Street,
consistent with the real building from all four sides and above, architecturally
credible, and a premium handcrafted miniature — not photorealistic, not voxel
art, not generic low-poly, and never accurate in one view while invented in the
others.

## Scope of the exported asset

Export the 550 Third Street building itself, including its parapets, roof deck,
penthouse, rooftop landscaping and mechanical plant, and the fixed rooftop
furniture that gives the deck its life.

Do not include unrelated surrounding city geometry: 3rd Street, Ritch Street,
South Park, neighbouring buildings at 560 3rd and 521–527 3rd, street furniture,
street trees, people, vehicles, plinths, cameras or lights. Temporary context may
appear in review renders but must not leak into the GLB.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary
`.glb`; real-world meters; origin at base center; minimum geometry Z ~ 0;
applied transforms; no negative scales; outward normals; no duplicate or foreign
geometry; no image textures; no transparency; flat-color materials named `Toy_*`
from the project palette; `_Glow` suffix only on surfaces that glow at night; no
`Toy_body`; no cameras, lights, animations, armatures or constraints; no external
dependencies; at most 14,000 triangles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model
drops into the city at its real-world heading — the loader applies no rotation
(`placeGeneric` in `app/src/assets.js` only scales and positions). The building's
long axis runs 45.3 deg / 225.3 deg true; the 3rd Street front faces north-east
(outward normal 44.6 deg true), so the contract's "front faces −Y" cannot be
honoured literally. Real-world orientation wins (AGENTS rule 5). Record the
decision and the measured heading in `REPORT.md`.

**Height normalization:** make the exported bounding-box top land exactly on the
verified architectural height, so the loader's `targetHeightM / measuredHeight`
scale is 1.0.

## Reproducible Blender workflow

Blender 4.5 LTS or newer, headless only: `blender -b --python script.py -- args`;
no GPU, so use Workbench or CPU Cycles.

Keep `artifacts/550-third/build_550_third.py` (deterministic build script),
`artifacts/550-third/550-third.blend`, and `artifacts/550-third/550-third.glb`.
The script must rebuild the model reliably enough for future revision. Do not
modify or rename an unrelated existing GLB to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`550-third-top.png`, `550-third-north.png`, `550-third-east.png`,
`550-third-south.png`, `550-third-west.png`, plus `550-third-contact-sheet.png`,
at least one high three-quarter aerial beauty render `550-third-aerial.png`, and
a night render `550-third-night.png`.

The four elevations must share scale, framing, lighting, exposure and
projection; use orthographic or long-lens cameras; label directions from the
researched orientation; **the top view is the hero image for this asset** and must
clearly show the skylight row, the paver walk, the penthouse and deck, the stair
and elevator penthouses and the mechanical plant; the aerial view uses the style
bible's camera assumptions (30-50 degrees down, long lens). Simple tabletop
lighting, neutral warm background, minimal depth of field, and every image must
depict the same exported model.

## Validate the exported GLB

Re-import `550-third.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture
count, camera count, light count, animation count, applied-transform status,
negative-scale status, normal-orientation status, unexpected geometry, and
per-material contract compliance. Normals are checked two ways: per-object signed
volume (authoritative for a union of closed solids) and a deterministic
visibility-ray test (≤ 0.15% residual, zero for single shells). Render at least
one review image from the re-imported asset. Write
`artifacts/550-third/validation.json` and `artifacts/550-third/REPORT.md`.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "550-third",
  "file": "550-third.glb",
  "anchor": [
    -122.3953409,
    37.7804407
  ],
  "targetHeightM": 11.0,
  "cat": 3,
  "name": "550 Third Street",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`,
`pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a
separate, explicitly requested job — run `docs/asset-plans/INTEGRATION-PROMPT.md`
for that, together with the integration notes in `docs/asset-plans/550-third.md`.
````

---

## Part 2 — Research and design dossier

Compiled 12 August 2026 from the sources in 2.2. Values marked *inferred* or
*estimated* are visual or derived, not published figures — the executing agent
must re-verify anything it relies on.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Address | 550 3rd Street, San Francisco, CA 94107 | DBI permits |
| Parcel | Block 3776, Lot 005 | DBI permits (measured) |
| Built | 1921 | commercial listing data; consistent with construction type and the 1992 parapet-bracing permit |
| Construction | Type 3 (masonry exterior walls, combustible interior) — brick-and-timber warehouse | DBI permits, all applications 1992–2025 |
| Storeys | 2, plus a rooftop penthouse level added 2023–25 (permit changes 2 → 3) | DBI PA 202302061449 |
| Footprint | 48.4 x 23.0 m bar, 1,070 m2 | OSM way/124889472, reprojected + oriented bbox (measured) |
| Floor area | ~11,520 sf/floor x 2 + ~2,600 sf penthouse ≈ 25,600 sf | derived; matches the leasing figure of "25,000 sf" |
| Main roof height | 7.2 m above grade | SF 2010 LiDAR building footprint SF3776005, `hgt_median_m` 7.23 (measured) |
| OSM `height` tag | 7 m | OSM (source: Bing) — describes the pre-2023 shell, NOT the architectural top |
| Anchor | -122.3953409, 37.7804407 | footprint AABB centre (measured) |
| Long-axis heading | 45.3 deg / 225.3 deg true | OSM geometry (measured) |
| Lot condition | Through lot: 3rd Street front (NE), Ritch Street rear (SW), party walls both long sides | OSM street geometry (measured) |
| 2023–25 scope | New elevator and stairs to the roof, new roof deck and penthouse; windows and garage doors reinstated on the rear facade; fixed property-line windows added | DBI PA 202302061449, issued 2023-11-01, **completed 2025-02-25** |
| Interior | Two floors joined by a ~1,400 sf double-height atrium with tiered seating; four walkable skylights at 2nd floor | DBI PA 202306140080, 202303244396; leasing copy |
| Rooftop plant | 4 roof-mounted heat pumps (2024 replacement) | DBI PA 202405212549 |
| Current use | Single-tenant creative office ("trophy HQ"), marketed as StartupHQ "550 3rd v2" | leasing material |

### 2.2 Sources

- https://www.openstreetmap.org/way/124889472 — footprint geometry, addr tags, `height=7` (Bing-traced)
- https://data.sfgov.org/resource/i98e-djp9.json — DBI building permits, block 3776 lot 005 (36 records, 1992–2025): storey counts, construction type, the 2023 roof-deck/penthouse/elevator scope and its 2025-02-25 completion, the rear garage doors and property-line windows, the atrium tiered platform and walkable skylights, the four rooftop heat pumps
- https://data.sfgov.org/resource/ynuv-fyni.json — SF 2010 LiDAR building footprints, record `SF3776005`: 4,151 half-metre cells (≈1,038 m2, corroborating the OSM polygon), ground mean 6.41 m, first-return median 13.60 m, height median 7.23 m
- https://www.startuphq.com/southpark — the leasing site, which publishes frames of the architect's December 2022 Design Development set: the roof axonometric ("Aerial pic NE corner"), a cut axonometric through the 3rd Street end ("NE Cross section aerial"), the penthouse interior, and the atrium. These are the strongest massing references available and the basis of §2.4 and §2.9.
- https://www.loopnet.com/Listing/550-3rd-St-San-Francisco-CA/24966380/ and related listing aggregators — 1921 build year, 25,000 sf, two-storey creative office, 2,600 sf rooftop penthouse, 1,400 sf atrium
- Google Maps satellite imagery (Airbus / Maxar / Vexcel, 2026) — footprint and context confirmation; the visible roof predates the 2025 works

### 2.3 Orientation and placement

A through lot in South Beach/SoMa, on the south-west side of 3rd Street between
South Park and Brannan, running the full block depth back to Ritch Street. The
SoMa grid here is rotated ~45 deg from true north: 3rd Street and Ritch Street
both run 134.8 deg / 314.8 deg, and the building's long axis is perpendicular to
them at 45.3 deg.

Measured footprint, reprojected with the app's tangent projection and recentred
on the footprint AABB centre (x east, y north, metres, CCW):

```
(-24.507,  -8.943)
( -9.891, -25.104)
(  7.515,  -7.915)
( 24.507,   8.932)
(  8.087,  25.104)
```

| Edge | Length | Outward normal (true) | What it is |
|---|---|---|---|
| v3 → v4 | 23.05 m | 44.6 deg (NE) | **3rd Street front** |
| v4 → v0 | 47.13 m | 313.8 deg (NW) | party wall, faces 521–527 3rd / South Park side |
| v0 → v1 | 21.79 m | 227.9 deg (SW) | **Ritch Street rear** |
| v1 → v2 → v3 | 24.46 + 23.93 m | 135.4 deg (SE) | party wall with a small kink at v2, faces 560 3rd |

Author `+Y` = north and place the polygon exactly as measured. The contract's
"front faces −Y" cannot be met — the real front faces north-east — so real-world
orientation wins per the README orientation note and AGENTS rule 5.

### 2.4 What each side shows

**North-east (3rd Street) — the public face.** 23 m wide, two storeys of painted
masonry under a tall solid parapet that screens the roof deck behind it. Broad
pilaster strips divide the wall into bays; each of the two main bays carries a
large industrial steel-sash window grid (many small panes, dark frames) at both
levels. Between them a recessed entry with a dark full-height door and the
numerals **550** set on the pilaster beside it. Street trees stand in front but
belong to the city, not the asset.

**South-east (long, ~48 m).** A blind painted party wall for most of its length,
with a regular rhythm of small punched square windows high up where the
neighbouring roof drops away — the "fixed property line windows" the 2023 permit
added — and a dark cap line along the parapet. *Which of the two long walls
carries these is inferred from a single axonometric; verify.*

**South-west (Ritch Street) — the service face.** 21.8 m wide, two storeys, the
plainest elevation: roll-up garage doors reinstated at ground level with a band
of windows above, per the 2023 permit. Lower parapet than the street front.

**North-west (long, ~47 m).** Blind painted party wall, essentially featureless.

**Top — the primary facade.** A long light roof field carrying, front (NE) to
back (SW):

1. the roof deck behind the tall street parapet: bluestone pavers, a small lawn
   patch, clipped hedge planters, lounge seating, a masonry fire pit, a long
   picnic table, glass guardrails;
2. the penthouse pavilion — a glass box on the deck's inboard edge under a thin
   flat white roof slab that cantilevers past the glass on all sides;
3. a sloped-roof stair penthouse with a long linear skylight in its slope, and a
   taller plain elevator-overrun box beside it;
4. five large rectangular skylights in a row down the length of the roof, with
   substantial frames;
5. a paver walkway snaking between the skylights;
6. two low sculptural built-in bench forms mid-roof;
7. the mechanical cluster at the Ritch Street end: four heat-pump units and a
   pair of low ducting runs.

### 2.5 Recognition cues (ranked)

1. **The skylight row** — five big glazed rectangles marching down a long low
   white roof. Nothing else on the block reads like it from above.
2. **The glass penthouse under its thin floating slab**, set at the street end
   with a green deck around it.
3. **The proportion**: a 48 m long, 23 m wide, 2-storey bar — long and low where
   its neighbours are short and tall.
4. **The 3rd Street front**: tall blank parapet over two big steel-sash window
   grids and a small dark recessed entry with oversized 550 numerals.
5. **The punched property-line window rhythm** on the long blind wall.

### 2.6 Miniature translation

**Preserve**

- The true footprint polygon, including the kink at v2
- 2-storey proportion; main roof at 7.3 m, penthouse crest at 11.0 m
- The five-skylight rhythm and its spacing down the roof
- The penthouse's floating-slab profile — thin roof, glass under it, cantilever
- The green deck at the street end as a distinct colour zone
- The tall street parapet screening the deck

**Simplify / exaggerate**

- Steel-sash window grids become 3x3 `Toy_glass` panes in an `Toy_ink` frame,
  two per storey per bay — rhythm, not mullion count (style bible §5)
- Skylights become simple frames with a single raised `Toy_glassl` pane; keep
  them ~15% larger than measured so they still read at city distance (§9)
- The **550** numerals become chunky extruded solids, oversized (§8) — this is
  the building's only signage and its cheapest identity cue
- Roof furniture becomes a handful of chunky primitives: three lounge blocks,
  one table with two benches, one fire-pit cube, four hedge boxes, one lawn pad
- Hedges and lawn are single flat volumes, not foliage
- The mechanical cluster becomes four identical beveled boxes on a low curb
- Garage doors become two recessed `Toy_ink` panels with a `Toy_steel` lintel

**Do not add** a tower, a crown, a signature curve, or any silhouette drama. The
building's charm is that it is long, low and quiet with one jewel on top.

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not
a straitjacket — adjust after the first aerial review render.

1. **Body:** extrude the measured footprint from z=0 to z=7.30 (main roof
   structure), `Toy_white`.
2. **Roof field:** a `Toy_stone` slab inset 0.35 m from the parapet inner face,
   top at z=7.45 (the deck build-up).
3. **Parapets:** 0.35 m thick, `Toy_white`, capped with a 0.12 m `Toy_ink` band —
   z=9.00 on the 3rd Street front (it screens the deck), z=8.20 on the two party
   walls and the Ritch Street rear.
4. **3rd Street front:** two window bays, each a 3x3 `Toy_glass` grid in an
   `Toy_ink` frame recessed 0.18 m, at z=1.30–3.30 and z=4.10–6.10; three
   pilaster strips proud 0.20 m; a 2.4 m wide entry recess 0.35 m deep with a
   `Toy_ink` door and `Toy_glass` transom; extruded `Toy_ink` **550** numerals
   0.85 m tall on the pilaster at 3.6 m.
5. **South-east party wall:** eight punched square windows, 0.9 m, at z=5.6,
   spaced 4.8 m, `Toy_glass` in a shallow `Toy_ink` reveal.
6. **Ritch Street rear:** two roll-up door recesses 3.6 x 3.4 m with `Toy_ink`
   leaves and a `Toy_steel` lintel; a `Toy_glass` window band at z=4.4–5.8.
7. **Skylights:** five, 5.6 x 3.4 m, spaced 7.6 m along the long axis on the roof
   centreline, `Toy_steel` frames 0.35 m proud, `Toy_glassl` pane on top.
8. **Paver walk:** a 1.6 m wide `Toy_steel` ribbon 0.05 m proud, dog-legging
   between the skylights from the deck to the mechanical cluster.
9. **Roof deck (NE end, ~12 m of the roof):** `Toy_steel` paver pad; a
   `Toy_mint` lawn pad; four `Toy_mint` hedge boxes 0.9 m tall on `Toy_ink`
   planters; three `Toy_teal` lounge blocks; a `Toy_trim` table with two benches;
   a `Toy_brick` fire-pit cube 0.5 m tall.
10. **Penthouse:** glass box 9.5 x 7.0 m, `Toy_glassl` walls with `Toy_ink`
    corner mullions, from z=7.45 to z=10.45; a `Toy_trim` roof slab 0.55 m thick
    cantilevering 0.9 m all round, top at **z=11.00** — the crest.
11. **Stair penthouse:** 4.2 x 3.6 m, `Toy_white`, mono-pitch from z=9.2 to
    z=10.4, with a `Toy_glassl` linear skylight strip in the slope.
12. **Elevator overrun:** 2.6 x 2.6 m `Toy_white` box, top at z=11.00.
13. **Mechanical cluster (SW end):** four `Toy_roofd` boxes 1.6 x 1.1 x 0.9 m on
    a 0.15 m `Toy_roofd` curb, plus two low duct runs.
14. Bevel 0.1 m, 2 segments, on everything.

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_white` | `#f7f4ec` | painted masonry walls, parapets, stair penthouse, elevator overrun |
| `Toy_stone` | `#d9d2c2` | main roof membrane field |
| `Toy_trim` | `#f3efe6` | penthouse roof slab, deck table and benches |
| `Toy_glass` | `#2a4d73` | steel-sash window grids, property-line windows, rear window band |
| `Toy_glassl` | `#6f95b8` | skylight panes, penthouse glazing, stair skylight |
| `Toy_ink` | `#3a3530` | window frames, parapet cap, entry door, 550 numerals, garage doors, planters |
| `Toy_steel` | `#9aa0a6` | skylight frames, paver walk and deck paving, garage lintel |
| `Toy_roofd` | `#45454a` | mechanical units, curb, ducts |
| `Toy_mint` | `#8fd0a8` | hedge boxes, lawn pad |
| `Toy_teal` | `#3fa8a0` | deck lounge seating (the one saturated accent) |
| `Toy_brick` | `#c96f4a` | fire pit |
| `Toy_glassl_Glow` | `#6f95b8` | penthouse glazing + the five skylights at night |
| `Toy_white_Glow` | `#f7f4ec` | the 3rd Street entry transom at night |

**Night state.** The composition is a dark low bar with a lit lantern on top:
the penthouse pavilion is the hero glow, the five skylights glowing from the
office below are the supporting rhythm (and the one thing that identifies this
building from the air at night), and the street entry is a single small ground
cue. Nothing else lights. Glow shells must be thin surfaces proud of the opaque
glazing behind them — the app renders `_Glow` in a separate layer at ~12% alpha
by day, so a primary surface must never be authored as glow.

### 2.9 Top surface

This is the asset. The building is 11 m tall and 48 m long: from the app's
camera the roof is roughly 80% of what anyone ever sees of it, and a blank roof
would make it indistinguishable from the baked warehouses around it. Every item
in §2.7 steps 7–13 exists because it is visible and identifying. The skylight row
and the paver walk are the graphical repetition the style bible §10 asks for; the
green deck at the street end is the colour event; the mechanical cluster at the
far end keeps the composition from being front-loaded.

### 2.10 Scope

**In the GLB:** the building, parapets, roof deck and its fixed furniture and
landscaping, penthouse, stair and elevator penthouses, skylights, mechanical
plant, the 550 numerals

**Not in the GLB:** 3rd Street, Ritch Street, South Park, neighbouring buildings,
street trees, street furniture, people, vehicles, plinths, cameras or lights

### 2.11 Triangle budget

Cap 14,000 — higher than Columbus Tower's 12,000 despite the simpler massing,
because the detail here lives in roof objects rather than in the shell. Suggested
split: shell, parapets and roof field ~2.5k; 3rd Street front (windows,
pilasters, entry, numerals) ~3k; party-wall and rear openings ~1.5k; five
skylights ~1.5k; penthouse + stair + elevator ~2k; deck landscaping and furniture
~2k; mechanical cluster ~0.8k; spare ~0.7k.

### 2.12 Draft manifest entry

```json
{
  "id": "550-third",
  "file": "550-third.glb",
  "anchor": [
    -122.3953409,
    37.7804407
  ],
  "targetHeightM": 11.0,
  "cat": 3,
  "name": "550 Third Street",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

`dims` and `tris` are placeholders until the asset is built and validated.
`loadRadius` is the skill's default `max(2500, targetHeightM * 30)`; at 11 m the
building is illegible long before 2,500 m, so the carved hole left beyond the
radius costs nothing.

### 2.13 Integration notes (for later, not this task)

- **New landmark.** Add a `pipeline/lib/landmarks.mjs` entry (`id: '550Third'`,
  lon/lat as above, `height: 11`) and re-bake the affected tiles, or the baked
  OSM block will sit inside the model.
- **The exclusion radius is the real risk here, and it is not a normal case.**
  `excluded()` in `pipeline/buildings.mjs` drops a footprint when *any* of its
  vertices falls inside the radius. 550 Third is a through lot with party walls
  on both long sides, so its neighbours' vertices sit *on* its own boundary.
  Distances from the anchor to this building's own vertices are 26.1, 27.0,
  **10.9**, 26.1 and 26.4 m — the 10.9 m vertex is the kink at v2. An `exclude`
  of ~12 m therefore removes this building's baked footprint while staying well
  inside the two long party walls; anything approaching 26 m would take the
  neighbours at 560 3rd and 521–527 3rd with it and open holes in the block.
  **Start at `exclude: 12` and verify visually** that (a) the baked 550 Third is
  gone and (b) both neighbours survive intact. If 12 is not enough to clear the
  bake, raise it in 1 m steps and re-check the neighbours rather than jumping.
- Manifest id `550-third` maps to registry id `550Third`.
- No camera preset key. At 11 m this is a texture in the block, not a destination
  — quiet placement is correct, and the key row should stay reserved for
  skyline landmarks.
- The building sits on near-flat made ground (LiDAR ground mean 6.4 m NAVD88 over
  the footprint, range 1.45 m). Terrain seating should be uneventful; check it
  anyway.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] bbox top exactly 11.0 m so the loader's scale factor is 1.0
- [ ] Dimensions plausible in meters and consistent with 2.1
- [ ] Triangles at or under 14,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the penthouse glazing, the five skylights, and the entry transom
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (per-object signed
      volume + deterministic ray test)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + night render + contact sheet regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

- **The penthouse crest height is estimated, not measured.** 7.3 m to the main
  roof is measured from 2010 city LiDAR; the penthouse was built 2023–25, after
  every height source available here. 11.0 m assumes one ~3.6 m storey above the
  roof deck. A measured elevation, a planning drawing, or a dated photograph
  against a known neighbour would replace the estimate. If it moves, only
  `targetHeightM` and the top of the penthouse volume move with it — the shell is
  measured.
- OSM `height=7` and the LiDAR median agree at ~7.2 m, but both describe the
  pre-2023 building. Neither is the architectural top. Never use them as the
  target height.
- Which long wall carries the property-line windows is inferred from one
  axonometric. Getting it backwards puts the only articulation on the wrong side.
- The Design Development frames on the leasing site date from December 2022;
  the permit completed February 2025. As-built details may differ from the DD
  renderings — the massing is safe, the furniture layout less so.
- Google's satellite imagery of the roof predates the 2025 works and shows the
  old plain roof. Do not "correct" the model against it.
- This is the first asset in the set with no skyline presence at all. Judge it
  from the top-down and high-aerial cameras first; a street-level review will
  make it look like an unremarkable box, because from the street it is one.
