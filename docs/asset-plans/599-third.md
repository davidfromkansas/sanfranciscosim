# 599 Third Street — SF-SIM asset plan

A four-storey wood-frame artist live/work loft building of 1999–2001, holding the
north corner of 3rd and Brannan with two full street elevations and a ground-floor
corner café. Twenty-four condominium lofts in a buff stucco box with big white
industrial window grids, a dark recessed entry bay carrying a steel chevron brace
and oversized **599** numerals, and a roof that is a working landscape — per-unit
skylights, condenser boxes, private deck pads and a penthouse.

It is the tall counterpart to its two neighbours already in the scene: 550 Third
across the street (11 m, long and low) and 380 Brannan a lot to the north-east
(12.6 m). At 18.3 m this is the one that gives the corner its wall.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/599-third/`. This document is the plan only: Part 1 is the runnable
task prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `599-third` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3942739, 37.7804504` (footprint AABB centre = vertex mean, measured) |
| Target height | **18.3 m** (stair/elevator penthouse crest; main parapet 16.0 m, both LiDAR-measured) |
| OSM footprint | 36.51 x 24.01 m rectangle on the 44.8 deg SoMa grid, 876.6 m2 (OSM way/124890326, measured) |
| Triangle cap | 15,000 |
| Category | `2` (Apartments) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 599 Third Street GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of 599 Third Street in San Francisco and
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
8. `artifacts/550-third/` and `artifacts/380-brannan/` — the two immediate
   neighbours, already built; this asset must look like it came out of the same
   toy box and must not out-detail them
9. `docs/asset-plans/599-third.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Must capture

- The four-storey buff stucco block, 36.5 m along Brannan by 24.0 m along 3rd,
  with a flat roof behind a low parapet — a corner wall, not a tower
- **Two** designed street elevations meeting at the south corner: 3rd Street
  (south-west, 24 m, the address face) and Brannan Street (south-east, 36.5 m,
  the long face). Both get windows; neither is a blind wall
- The 3rd Street entry: a full-height recess in a darker warm taupe, glass doors
  in a dark frame, white **599** numerals above them, a vertical stack of small
  square punched windows above that, and the steel chevron/inverted-V brace near
  the top of the recess
- The large white-framed multi-pane industrial window grids that repeat across
  both street faces, four storeys of them
- The ground-floor corner café (Golden Goat Coffee, a 2017 conversion of the
  original garage) as a glazed shopfront at the 3rd/Brannan corner
- The roof as a working landscape: a scatter of small skylights and condenser
  boxes roughly one cluster per loft, private timber deck pads, and the
  stair/elevator penthouse that is the true crest at 18.3 m
- The two blind interior faces (north-west party wall toward 551 3rd, north-east
  face toward 380 Brannan) as plain stucco with only sparse high openings

## Research 599 Third Street independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- South-west (3rd Street) and south-east (Brannan Street) elevations
- The two interior faces
- Aerial and roof views — the roof carries most of what the app's camera sees
- Ground-level views of the corner café
- Day and night appearance
- Publicly available drawings, plans or diagrams
- **The crest height, which this dossier takes from 2010 LiDAR `hgt_max`.** The
  main parapet at ~16 m is corroborated by the OSM `height=16` tag and the LiDAR
  median (15.62 m); the 18.34 m maximum is a single statistic and could be an
  antenna rather than the penthouse. A measured elevation, a planning drawing or
  a dated photograph against a known neighbour beats it. Document what you find.
- **Where the roof deck actually is.** DBI PA 9721085 records "roof deck open
  space layout as built" (2002) but not its extent; this dossier infers per-unit
  deck pads from aerial imagery.

Prefer architect/engineer publications, owner or institutional material,
planning and permitting documents, architectural press, geolocated photography,
and aerial/satellite imagery. Never rely on a single photograph, a single
AI-generated image, or a single unsourced 3D model. Separate verified facts from
visual inference; if sources disagree, document the disagreement and decide.

## Create a reference dossier

Write `artifacts/599-third/REFERENCE.md` containing: source links and what each
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

This building's job is to be a crisp corner. Its identity is a rhythm — four
storeys of big white window grids on two faces — interrupted once, by the dark
entry bay. §5 (facade rhythm over mullion count) and §10 (roofs as secondary
facades) both govern; §11 (landmark geometry) does not, because there is no
silhouette event here. Resist giving it a crown, a setback or a signature curve
it does not have. Spend the budget on the window rhythm, the entry bay, the
corner café, and a roof that reads as inhabited.

The finished asset must be immediately recognizable as 599 Third Street,
consistent with the real building from all four sides and above, architecturally
credible, and a premium handcrafted miniature — not photorealistic, not voxel
art, not generic low-poly, and never accurate in one view while invented in the
others.

## Scope of the exported asset

Export the 599 Third Street building itself, including its parapets, roof deck
pads, penthouse, stair and elevator overruns, skylights, mechanical plant and the
ground-floor shopfront.

Do not include unrelated surrounding city geometry: 3rd Street, Brannan Street,
Varney Place, neighbouring buildings at 551 3rd or 380 Brannan, street furniture,
street trees, people, vehicles, plinths, cameras or lights. Temporary context may
appear in review renders but must not leak into the GLB.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary
`.glb`; real-world meters; origin at base center; minimum geometry Z ~ 0;
applied transforms; no negative scales; outward normals; no duplicate or foreign
geometry; no image textures; no transparency; flat-color materials named `Toy_*`
from the project palette; `_Glow` suffix only on surfaces that glow at night; no
`Toy_body`; no cameras, lights, animations, armatures or constraints; no external
dependencies; at most 15,000 triangles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model
drops into the city at its real-world heading — the loader applies no rotation
(`placeGeneric` in `app/src/assets.js` only scales and positions). The long axis
runs 44.8 deg / 224.8 deg true; the 3rd Street front faces south-west (outward
normal 224.8 deg true), so the contract's "front faces −Y" cannot be honoured
literally. Real-world orientation wins (AGENTS rule 5). Record the decision and
the measured heading in `REPORT.md`.

**Height normalization:** make the exported bounding-box top land exactly on the
verified architectural height, so the loader's `targetHeightM / measuredHeight`
scale is 1.0.

## Reproducible Blender workflow

Blender 4.5 LTS or newer, headless only: `blender -b --python script.py -- args`;
no GPU, so use Workbench or CPU Cycles.

Keep `artifacts/599-third/build_599_third.py` (deterministic build script),
`artifacts/599-third/599-third.blend`, and `artifacts/599-third/599-third.glb`.
The script must rebuild the model reliably enough for future revision. Do not
modify or rename an unrelated existing GLB to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`599-third-top.png`, `599-third-north.png`, `599-third-east.png`,
`599-third-south.png`, `599-third-west.png`, plus `599-third-contact-sheet.png`,
at least one high three-quarter aerial beauty render `599-third-aerial.png`, and
a night render `599-third-night.png`.

The four elevations must share scale, framing, lighting, exposure and
projection; use orthographic or long-lens cameras; label directions from the
researched orientation; the aerial view uses the style bible's camera assumptions
(30-50 degrees down, long lens) and must show the south corner where the two
street faces meet — that corner is the hero view for this asset. Simple tabletop
lighting, neutral warm background, minimal depth of field, and every image must
depict the same exported model.

## Validate the exported GLB

Re-import `599-third.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture
count, camera count, light count, animation count, applied-transform status,
negative-scale status, normal-orientation status, unexpected geometry, and
per-material contract compliance. Normals are checked two ways: per-object signed
volume (authoritative for a union of closed solids) and a deterministic
visibility-ray test (≤ 0.15% residual, zero for single shells). Render at least
one review image from the re-imported asset. Write
`artifacts/599-third/validation.json` and `artifacts/599-third/REPORT.md`.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "599-third",
  "file": "599-third.glb",
  "anchor": [
    -122.3942739,
    37.7804504
  ],
  "targetHeightM": 18.3,
  "cat": 2,
  "name": "599 Third Street",
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
for that, together with the integration notes in `docs/asset-plans/599-third.md`.
````

---

## Part 2 — Research and design dossier

Compiled 12 August 2026 from the sources in 2.2. Values marked *inferred* or
*estimated* are visual or derived, not published figures — the executing agent
must re-verify anything it relies on.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Address | 599 3rd Street, San Francisco, CA 94107 | OSM `addr:*` (survey-sourced), DBI permits |
| Parcel | Block 3775, map lot 140, subdivided into 24 condominium lots 140–163 | DataSF parcels `acdm-wktn` (measured) |
| Zoning | CMUO — Central SoMa Mixed Use Office | DataSF parcels |
| Built | 1999–2001 (permits run 1998–2002 under PA 9721085; condo map recorded 2003-08-22) | DBI permits + parcel record; listing aggregators say "2001" |
| Construction | Type V wood frame, 4 storeys | DBI permits, every application 1999–2022 |
| Use | Artist live/work lofts, 24 condominium units, plus one ground-floor café | DBI permits; unit numbers seen: 101–120, 204–208, 301–310, 401 |
| Footprint | 36.51 x 24.01 m rectangle, 876.6 m2 | OSM way/124890326, reprojected + oriented bbox (measured) |
| Anchor | -122.3942739, 37.7804504 | footprint AABB centre; the polygon is a true rectangle, so this equals the vertex mean exactly (measured) |
| Long-axis heading | 44.8 deg / 224.8 deg true | OSM geometry (measured) |
| Main roof / parapet | ~15.6 m median, ~16 m at the parapet | SF 2010 LiDAR footprint `SF3775140`, `hgt_median_m` 15.62, `hgt_mean` 15.81 (measured); OSM `height=16` agrees independently |
| Crest | **18.34 m** | same LiDAR record, `hgt_maxcm` 1834 (measured, but a single maximum — see 2.15) |
| Ground | 7.90 m NAVD88 mean over the footprint | same LiDAR record (measured) |
| LiDAR footprint area | 3,515 cells x 0.25 m2 = 879 m2 | corroborates the OSM polygon to 0.3% |
| Lot condition | Corner lot: 3rd Street front (SW), Brannan Street front (SE), interior faces NW and NE | OSM street geometry (measured) |
| Roof deck | "roof deck open space layout as built", 2002, under PA 9721085 | DBI permit 200212176688 |
| Roof-level penthouse | Unit #401 "created from penthouse space and adjacent storage areas at roof level" | DBI PA 202204147248 (2022 legalization) |
| Ground-floor café | Original garage converted to a 351 sf coffee shop, occupancy S2 → B, 2017 | DBI PA 201712074719; the tenant today is Golden Goat Coffee (OSM node 13765490836) |
| Neighbours already in the scene | 380 Brannan (`380-brannan`, 12.6 m) 33 m to the NE; 550 Third (`550-third`, 11 m) 93 m to the W | repo manifest + measured bearings |

### 2.2 Sources

- https://www.openstreetmap.org/way/124890326 — footprint geometry, `addr:housenumber=599` (survey), `height=16` (Bing-traced)
- https://data.sfgov.org/resource/acdm-wktn.json — DataSF parcels: map lot 3775140 with 24 active condominium lots 3775140–3775163 all sharing one polygon, CMUO zoning, condo map recorded 2003-08-22. The 24-lot condo structure is what explains the small commercial listings at this address: they are individual lofts, not the building.
- https://data.sfgov.org/resource/i98e-djp9.json — DBI building permits, block 3775 (17 records at 599 3rd, 1998–2022): 4 storeys, Type V wood frame, artist live/work use, the 2002 as-built roof deck, the 2017 garage-to-café conversion, the 2022 round of unit legalizations that names unit #401 at roof level
- https://data.sfgov.org/resource/ynuv-fyni.json — SF 2010 LiDAR building footprints, record `SF3775140`: 3,515 half-metre cells (879 m2), ground mean 7.90 m, height median 15.62 m, height mean 15.81 m, height max 18.34 m
- Google Street View, imagery capture **May 2025**, from 3rd Street opposite the entry — the primary elevation reference and the basis of §2.4's 3rd Street paragraph
- Google Maps / Vexcel aerial imagery, 2026 — roof reading in §2.4 "Top"; the building leans in this imagery, so roof-object positions from it are approximate
- https://www.loopnet.com/Listing/599-3rd-St-San-Francisco-CA/21052251/ and https://www.propertyshark.com/cre/commercial-property/us/ca/san-francisco/599-3rd-st-203/ — build year 2001; the "6,400 sf" figure on these pages is one condo unit, not the building, and must not be used to derive massing

### 2.3 Orientation and placement

The north corner of 3rd and Brannan, in South Beach at the edge of SoMa. The
grid here is rotated ~45 deg from true north: 3rd Street runs 134.8 / 314.8 deg,
Brannan Street runs 44.8 / 224.8 deg, and the building fills its corner squarely.
Varney Place, a short alley, runs behind it to the north.

Measured footprint, reprojected with the app's tangent projection and recentred
on the footprint AABB centre (x east, y north, metres, CCW). It is a clean
rectangle — four vertices, no kink — and every vertex is 21.8–21.9 m from the
anchor:

```
v0 ( -4.435, -21.323)
v1 ( 21.471,   4.411)
v2 (  4.426,  21.323)
v3 (-21.471,  -4.411)
```

| Edge | Length | Outward normal (true) | What it is |
|---|---|---|---|
| v0 → v1 | 36.51 m | 135.2 deg (SE) | **Brannan Street front** — the long face |
| v1 → v2 | 24.01 m | 44.8 deg (NE) | interior face toward 380 Brannan / Varney Place |
| v2 → v3 | 36.51 m | 315.2 deg (NW) | party wall toward 551 3rd Street |
| v3 → v0 | 24.01 m | 224.8 deg (SW) | **3rd Street front** — the address face and entry |

The south corner, where v0 sits, is the corner of 3rd and Brannan and the
building's hero point. Author `+Y` = north and place the polygon exactly as
measured. The contract's "front faces −Y" cannot be met — the entry faces
south-west — so real-world orientation wins per the README orientation note and
AGENTS rule 5.

### 2.4 What each side shows

**South-west (3rd Street) — the address face.** 24 m wide, four storeys of buff /
pale-yellow stucco under a plain flat parapet. The composition is symmetrical
about a **full-height recess in a darker warm taupe** at the centre: glass entry
doors in a dark metal frame at the base, white **599** numerals directly above
them, then a narrow vertical stack of small square punched windows, and near the
top a **steel chevron — an inverted-V brace** spanning the recess, the one piece
of structural drama on the whole building. Either side of the recess, a broad
buff pilaster strip frames a bay carrying large **white-framed multi-pane window
grids**, two per bay per storey, sitting almost flush in the stucco. Ground floor
windows are taller than the ones above. Street trees stand in front but belong to
the city, not the asset. *(Observed directly, Street View May 2025.)*

**South-east (Brannan Street) — the long face.** 36.5 m, same four storeys, same
buff stucco and same white window grids continuing round the corner in a longer
run — roughly half again as many bays as the 3rd Street face. No entry recess and
no chevron; this face is pure rhythm. At the south corner the ground floor opens
into the **café shopfront** (the 2017 garage conversion): a glazed corner bay at
street level, darker and more transparent than anything above it. *(Massing and
material observed from aerial imagery and the corner of the Street View frame;
the bay count is* inferred *from the face length and the 3rd Street spacing.)*

**North-west (party wall, 36.5 m).** Faces 551 3rd Street across a property line.
Plain buff stucco, effectively blind, with at most a sparse row of small high
openings. *Inferred.*

**North-east (interior face, 24 m).** Faces the 380 Brannan lot and Varney Place
beyond. Plain, with service doors and a few punched openings. *Inferred.*

**Top — the working roof.** A flat grey membrane field behind a low parapet,
densely inhabited, which is what a 24-loft wood-frame building's roof looks like
from above:

1. a scatter of **small skylights** — roughly one per loft, in a loose grid down
   the long axis;
2. an equally dense scatter of **condenser / vent boxes**, generally paired with
   the skylights;
3. several **light timber deck pads** — the 2002 as-built private open space;
4. the **stair and elevator penthouse** near the middle-north of the roof, the
   tallest thing on the building at ~18.3 m, and the roof-level penthouse space
   that became unit #401;
5. a low parapet cap running the whole perimeter, stepping nowhere.

*(Item counts and positions are* inferred *from 2026 Vexcel aerial imagery, in
which a 16 m building leans noticeably; treat the pattern as real and the exact
placement as free.)*

### 2.5 Recognition cues (ranked)

1. **The corner itself** — two fully-glazed-and-gridded street faces meeting at a
   sharp 90 deg on the diagonal grid, four storeys of continuous rhythm. Nothing
   else on this block turns a corner this squarely.
2. **The dark entry bay with the chevron brace and the 599 numerals**, dead centre
   of the 3rd Street face — the single strongest close-range cue.
3. **The white multi-pane window grids on buff stucco** — the building's colour
   signature, and the thing that distinguishes it from the grey and brick
   warehouses either side.
4. **The inhabited roof** — skylights, condensers and deck pads scattered like a
   small settlement. From the app's camera this is most of the building.
5. **The corner café shopfront** — the one dark, transparent, ground-level event.

### 2.6 Miniature translation

**Preserve**

- The true rectangular footprint and its 44.8 deg heading
- Four storeys to a 16.0 m parapet, penthouse crest at 18.3 m
- Two designed street faces; two quiet interior faces
- The centred dark entry bay on 3rd Street, with the chevron and the numerals
- The buff/white colour pairing — it is the identity

**Simplify / exaggerate**

- Window grids become 3x2 `Toy_glass` panes in a `Toy_trim` (white) frame, one
  per bay per storey — rhythm, not mullion count (style bible §5). Four bays on
  3rd Street, six on Brannan
- The **599** numerals become chunky extruded solids, oversized (§8)
- The chevron becomes a single beveled `Toy_steel` inverted-V, thickened well
  past its real section so it survives at city distance (§9)
- The café shopfront becomes one recessed `Toy_glass` corner bay with a
  `Toy_ink` frame and a single `Toy_coral` awning — the one saturated accent
- Roof skylights and condensers become two repeated primitives placed on a loose
  grid: ~10 `Toy_glassl` skylight caps and ~12 `Toy_roofd` boxes. Do not model 24
  of each; the reading is "many", not a census
- Deck pads become three flat `Toy_sand` rectangles
- Interior faces get flat stucco and a sparse row of small punched windows only

**Do not add** a crown, a setback, a cornice or a corner turret. The building is a
plain, well-mannered box whose whole charm is repetition plus one interruption.

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not
a straitjacket — adjust after the first aerial review render.

1. **Body:** extrude the measured footprint from z=0 to z=15.60, `Toy_sand`
   (buff stucco).
2. **Parapet:** 0.30 m thick, `Toy_sand`, from z=15.60 to **z=16.00**, capped
   with a 0.10 m `Toy_ink` band, running the full perimeter.
3. **Roof field:** `Toy_stone` slab inset 0.30 m from the parapet inner face, top
   at z=15.70.
4. **Storey datum:** floors at z=0.00 / 4.20 / 8.00 / 11.80, parapet at 15.60 —
   a taller ground floor (4.2 m) under three 3.8 m loft levels.
5. **3rd Street face (SW, 24 m):** two bays each side of a central recess.
   - Central recess 5.0 m wide, 0.40 m deep, `Toy_ink` back face, full height
     from grade to 14.6 m.
   - Entry: `Toy_glass` doors 2.6 x 3.0 m in a `Toy_ink` frame.
   - **599** numerals, extruded `Toy_trim`, 0.75 m tall, at z=4.6.
   - Stack of four 0.7 m square `Toy_glass` punched windows on the recess
     centreline at z=6.2, 8.0, 9.8, 11.6.
   - Chevron: `Toy_steel` inverted-V, 0.28 m section, apex at z=14.2, feet at
     z=12.2 on the recess jambs.
   - Bays: 3x2 `Toy_glass` grids in 0.16 m `Toy_trim` frames, 3.4 x 2.2 m at
     each upper storey, 3.4 x 3.0 m at ground.
   - Pilaster strips 0.6 m wide proud 0.15 m at the two bay divisions and both
     corners.
6. **Brannan face (SE, 36.5 m):** six bays of the same window unit at every
   storey, same pilaster rhythm, no recess. At the south corner, a ground-floor
   café bay: 6.0 m of `Toy_glass` recessed 0.35 m in a `Toy_ink` frame, with a
   `Toy_coral` awning 0.9 m deep at z=3.6.
7. **NW party wall and NE face:** flat `Toy_sand`; one row of 0.7 m square
   `Toy_glass` punched windows at z=13.0, spaced 4.5 m.
8. **Roof penthouse:** `Toy_trim` box 7.5 x 5.0 m, from z=15.70 to **z=18.30**,
   set roughly 6 m in from the north-east end, with a `Toy_ink` cap band and one
   `Toy_glassl` window per visible side.
9. **Skylights:** ten `Toy_glassl` caps 1.4 x 1.0 m, 0.25 m proud, on a loose
   2-across grid down the long axis.
10. **Condensers:** twelve `Toy_roofd` boxes 0.9 x 0.7 x 0.6 m on a 0.10 m curb,
    generally paired with the skylights.
11. **Deck pads:** three `Toy_sand` rectangles 4.0 x 3.0 m, 0.08 m proud.
12. Bevel 0.1 m, 2 segments, on everything.

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_sand` | `#ece4d4` | buff stucco walls, parapet, pilasters, deck pads |
| `Toy_trim` | `#f3efe6` | window frames, 599 numerals, roof penthouse |
| `Toy_glass` | `#2a4d73` | window panes, entry doors, punched windows, café glazing |
| `Toy_glassl` | `#6f95b8` | roof skylight caps, penthouse windows |
| `Toy_ink` | `#3a3530` | entry recess back face, parapet cap, frames, shopfront frame |
| `Toy_steel` | `#9aa0a6` | the chevron brace |
| `Toy_stone` | `#d9d2c2` | roof membrane field |
| `Toy_roofd` | `#45454a` | condenser boxes and curbs |
| `Toy_coral` | `#e8735a` | café awning (the one saturated accent) |
| `Toy_glass_Glow` | `#2a4d73` | a scattered subset of the loft windows at night |
| `Toy_glassl_Glow` | `#6f95b8` | roof skylights at night |
| `Toy_trim_Glow` | `#f3efe6` | the entry doors and the café shopfront at night |

**Night state.** A residential building at night is a scatter, not a display:
about a third of the loft windows lit in an irregular pattern (the hero), the
roof skylights glowing faintly from the lofts below (the supporting rhythm, and
the thing that identifies it from the air), and the entry and café shopfront as
two warm ground-level cues. The chevron, the numerals and the stucco stay dark.
Glow shells must be thin surfaces proud of the opaque glazing behind them — the
app renders `_Glow` in a separate layer at ~12% alpha by day, so a primary
surface must never be authored as glow. Drive `_Glow` emission from Base Color at
strength 1.0 in the render rig (see the README's note on re-imported GLBs).

### 2.9 Top surface

At 18.3 m with a 36.5 x 24 m plan, the roof is the largest single surface the
app's camera ever sees of this building, and a blank one would sink it into the
baked block. But the composition must stay quieter than 550 Third's across the
street: that building's roof is a designed rooftop with a glass pavilion, this
one is a working roof that residents use. The distinction is the point of having
both — repetition and utility here, a jewel object there. The skylight/condenser
scatter is the graphical repetition the style bible §10 asks for; the penthouse
is the only vertical event; the deck pads are the colour break.

### 2.10 Scope

**In the GLB:** the building, parapet, roof field, skylights, condensers, deck
pads, stair/elevator penthouse, entry recess with numerals and chevron, café
shopfront and awning

**Not in the GLB:** 3rd Street, Brannan Street, Varney Place, neighbouring
buildings, street trees, street furniture, people, vehicles, plinths, cameras or
lights

### 2.11 Triangle budget

Cap 15,000 — above 550 Third's 14,000 because this building has two fully
articulated street elevations and twice the storey count, and below the 27,000
contract ceiling because the massing is a single box. Suggested split: shell,
parapet and roof field ~2k; 3rd Street face (windows, pilasters, recess,
numerals, chevron) ~3.5k; Brannan face (windows, pilasters, café bay) ~4k;
interior faces ~1k; roof objects (skylights, condensers, decks, penthouse) ~3.5k;
spare ~1k.

### 2.12 Draft manifest entry

```json
{
  "id": "599-third",
  "file": "599-third.glb",
  "anchor": [
    -122.3942739,
    37.7804504
  ],
  "targetHeightM": 18.3,
  "cat": 2,
  "name": "599 Third Street",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

`dims` and `tris` are placeholders until the asset is built and validated.
`loadRadius` is the skill's default `max(2500, targetHeightM * 30)` = 2500; at
18.3 m the building is illegible long before 2,500 m, so the carved hole left
beyond the radius costs nothing.

### 2.13 Integration notes (for later, not this task)

- **New landmark.** Add a `pipeline/lib/landmarks.mjs` entry (`id: '599Third'`,
  lon/lat as above, `height: 18.3`) and re-bake the affected tiles, or the baked
  OSM block will sit inside the model.
- **Exclusion radius.** `excluded()` in `pipeline/buildings.mjs` drops a footprint
  when *any* of its vertices falls inside the radius. This footprint is an
  unusually regular case: all four of its own vertices are 21.78–21.92 m from the
  anchor, so the radius must be at least ~21.9 m to drop this building, and the
  neighbours must all be further than that. **Verify against the actual bake-side
  geometry before committing a number** — DataSF footprints simplified at the
  pipeline's 0.6 m tolerance, `ringCentroid` for the anchor test — exactly as was
  done for 550 Third and 375 Alabama. Both street frontages help: 3rd and Brannan
  are wide, so a radius in the low-to-mid 20s reaches open roadway on two of four
  sides. The party wall to 551 3rd (NW) is the tight one, and 380 Brannan to the
  NE is an already-integrated landmark whose own baked footprint must not be
  taken as collateral. Start the check at `exclude: 22`.
- Manifest id `599-third` maps to registry id `599Third`.
- No camera preset key. At 18.3 m this is a block texture, not a destination.
- The building sits on flat made ground (LiDAR ground mean 7.90 m NAVD88).
  Terrain seating should be uneventful; check it anyway.
- **Batch note.** 380 Brannan and 550 Third are already in the manifest; this
  landmark completes the 3rd/Brannan corner. If it is built alongside other
  landmarks, follow batch mode in `docs/asset-pipeline/ADDRESS-TO-ASSET.md` —
  commit source only and let `BATCH-INTEGRATE.md` bake the city once.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] bbox top exactly 18.3 m so the loader's scale factor is 1.0
- [ ] Dimensions plausible in meters and consistent with 2.1
- [ ] Triangles at or under 15,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the lit loft windows, the roof skylights, the entry and the
      café shopfront
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (per-object signed
      volume + deterministic ray test)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + night render + contact sheet regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

- **The 18.34 m crest is one LiDAR statistic.** `hgt_max` over the footprint is
  the highest first return anywhere on the roof — a mast, a parapet corner or a
  survey artefact would produce the same number as a penthouse. The 16 m parapet
  is safe: OSM's independent `height=16` and the LiDAR median (15.62 m) agree.
  If the crest moves, only `targetHeightM` and the top of the penthouse volume
  move with it.
- **The 2010 LiDAR predates the 2017 café conversion and the 2022 unit
  legalizations,** but both were interior/ground-floor work; the massing it
  measured is still the massing that stands.
- **The Brannan bay count is inferred** from the face length and the 3rd Street
  spacing, not counted from a photograph. Getting it wrong changes the rhythm on
  the building's longest face.
- **Roof-object placement is inferred from leaning aerial imagery.** The pattern
  (skylight + condenser clusters, a few deck pads, one penthouse) is well
  supported; the coordinates are not. Do not chase pixel positions.
- **Do not take the commercial listings' floor areas as massing evidence.** The
  parcel is 24 condominium lots; a "6,400 sf" listing at this address is one
  loft. The building is ~876 m2 per floor over four floors.
- This is the first residential landmark in the set whose night state is a
  *scatter* rather than a designed display. Resist lighting it evenly — an
  evenly-lit grid reads as an office block and destroys the one thing that says
  "people live here".
