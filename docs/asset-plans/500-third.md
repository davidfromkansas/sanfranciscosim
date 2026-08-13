# 500 Third Street — SF-SIM asset plan

A 1927 five-storey reinforced-concrete industrial loft filling the quarter block
at 3rd and Bryant, and one of the purest surviving examples of the SoMa type: a
warm-grey concrete frame wrapped on every side by huge steel-sash factory
windows, a charcoal storefront base, a flat parapet with a raised signed crown at
the north corner, and a row of flagpoles along the street parapets. Where 550
Third is small and roof-led, 500 Third is a block: it is read from the street and
from the air as one chunky prism whose whole identity is the window grid.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/500-third/`. This document is the plan only: Part 1 is the runnable
task prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `500-third` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3958224, 37.7808279` (footprint AABB centre, measured) |
| Target height | **26.5 m** (rooftop bulkhead crest; main parapet 23.0 m, both measured) |
| OSM footprint | 58.6 x 47.7 m rotated block on the 45 deg SoMa grid, 2,795 m2 (OSM way/147508936, measured) |
| Triangle cap | 22,000 |
| Category | `3` (Office) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 500 Third Street GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of 500 Third Street in San Francisco and
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
8. `artifacts/550-third/` and `artifacts/375-alabama/` — the closest matches:
   the same street and the same SoMa concrete-loft type
9. `docs/asset-plans/500-third.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Must capture

- The near-square 58.6 x 47.7 m block sitting on the 45 deg SoMa grid, filling
  its quarter block between 3rd, Bryant, Ritch and the SE service lot
- Five storeys: one tall charcoal storefront ground floor under four identical
  upper floors, flat parapet at 23 m
- The steel-sash window grid — the identity. Every bay on 3rd, Bryant and the
  SE elevation carries one large multi-pane industrial window, framed by narrow
  concrete pilasters and spandrel panels
- The raised parapet crown at the north corner (3rd and Bryant) carrying the
  illuminated sign band on both faces
- The row of flag masts along the 3rd Street and Bryant parapets
- The plain service rear on Ritch Street: roll-up doors, a louvre, punched
  windows, no shopfront
- The roof: pale membrane field, the central bulkhead penthouse (the crest at
  26.5 m), the elevator overrun, and the mechanical cluster on the south half

## Research 500 Third Street independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- North-east (3rd Street) and north-west (Bryant Street) elevations
- South-west (Ritch Street) rear and the south-east elevation over the parking lot
- Aerial and roof views
- Ground-level views, day and night
- Publicly available drawings, plans or diagrams
- **The storey count, which the sources disagree about.** DBI permits report both
  5 and 6 existing storeys for this parcel and the assessor record says 6; every
  photograph of every elevation shows one tall ground floor plus four upper
  window bands. Resolve it, and say what you resolved it with.
- **The rooftop bulkhead, which this dossier derives from LiDAR and one aerial.**
  Its plan size and height come from the 2010 LiDAR maximum and Esri imagery,
  not from a drawing. Any better source beats them.

Prefer architect/engineer publications, owner or institutional material,
planning and permitting documents, architectural press, geolocated photography,
and aerial/satellite imagery. Never rely on a single photograph, a single
AI-generated image, or a single unsourced 3D model. Separate verified facts from
visual inference; if sources disagree, document the disagreement and decide.

## Create a reference dossier

Write `artifacts/500-third/REFERENCE.md` containing: source links and what each
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

This building is a single prism. Its charm is repetition: a disciplined grid of
big windows on three sides, a quiet service wall on the fourth, and one event —
the signed corner crown. §5 (windows as graphical rhythm) and §10 (roofs as
secondary facades) are the governing sections. Resist modelling real mullion
counts; resist inventing a roof deck it does not have.

The finished asset must be immediately recognizable as 500 Third Street,
consistent with the real building from all four sides and above, architecturally
credible, and a premium handcrafted miniature — not photorealistic, not voxel
art, not generic low-poly, and never accurate in one view while invented in the
others.

## Scope of the exported asset

Export the 500 Third Street building itself, including its parapets, corner
crown and sign band, flag masts, rooftop bulkhead, elevator overrun and
mechanical plant.

Do not include unrelated surrounding city geometry: 3rd Street, Bryant Street,
Ritch Street, the SE parking lot, neighbouring buildings, street furniture,
street trees, people, vehicles, plinths, cameras or lights. Temporary context may
appear in review renders but must not leak into the GLB.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary
`.glb`; real-world meters; origin at base center; minimum geometry Z ~ 0;
applied transforms; no negative scales; outward normals; no duplicate or foreign
geometry; no image textures; no transparency; flat-color materials named `Toy_*`
from the project palette; `_Glow` suffix only on surfaces that glow at night; no
`Toy_body`; no cameras, lights, animations, armatures or constraints; no external
dependencies; at most 22,000 triangles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model
drops into the city at its real-world heading — the loader applies no rotation
(`placeGeneric` in `app/src/assets.js` only scales and positions). The 3rd Street
front faces north-east (outward normal 44.9 deg true), so the contract's
"front faces −Y" cannot be honoured literally. Real-world orientation wins
(AGENTS rule 5). Record the decision and the measured heading in `REPORT.md`.

**Height normalization:** make the exported bounding-box top land exactly on the
verified architectural height (26.5 m, the bulkhead crest), so the loader's
`targetHeightM / measuredHeight` scale is 1.0. Nothing — flag masts included —
may rise above the bulkhead.

## Reproducible Blender workflow

Blender 4.5 LTS or newer, headless only: `blender -b --python script.py -- args`;
no GPU, so use Workbench or CPU Cycles.

Keep `artifacts/500-third/build_500_third.py` (deterministic build script),
`artifacts/500-third/500-third.blend`, and `artifacts/500-third/500-third.glb`.
The script must rebuild the model reliably enough for future revision. Do not
modify or rename an unrelated existing GLB to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`500-third-top.png`, `500-third-north.png`, `500-third-east.png`,
`500-third-south.png`, `500-third-west.png`, plus `500-third-contact-sheet.png`,
at least one high three-quarter aerial beauty render `500-third-aerial.png`, and
a night render `500-third-night.png`.

The four elevations must share scale, framing, lighting, exposure and
projection; use orthographic or long-lens cameras; label directions from the
researched orientation; the aerial view uses the style bible's camera assumptions
(30-50 degrees down, long lens). Simple tabletop lighting, neutral warm
background, minimal depth of field, and every image must depict the same exported
model.

## Validate the exported GLB

Re-import `500-third.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture
count, camera count, light count, animation count, applied-transform status,
negative-scale status, normal-orientation status, unexpected geometry, and
per-material contract compliance. Normals are checked two ways: per-object signed
volume (authoritative for a union of closed solids) and a deterministic
visibility-ray test (≤ 0.15% residual, zero for single shells). Render at least
one review image from the re-imported asset. Write
`artifacts/500-third/validation.json` and `artifacts/500-third/REPORT.md`.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "500-third",
  "file": "500-third.glb",
  "anchor": [
    -122.3958224,
    37.7808279
  ],
  "targetHeightM": 26.5,
  "cat": 3,
  "name": "500 Third Street",
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
for that, together with the integration notes in `docs/asset-plans/500-third.md`.
````

---

## Part 2 — Research and design dossier

Compiled 13 August 2026 from the sources in 2.2. Values marked *inferred* or
*estimated* are visual or derived, not published figures — the executing agent
must re-verify anything it relies on.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Address | 500 3rd Street (marketed as 500–520 3rd St), San Francisco, CA 94107 | OSM addr tags, DBI permits, leasing listings |
| Parcel | Block 3776, Lot 115 | DBI permits (measured) |
| Built | 1927 | assessor/commercial listing data, consistent with the concrete-frame type |
| Construction | Concrete/masonry frame; DBI records give construction type 1 and 2 across applications | DBI permits (100 records, 1990–2022) |
| Storeys | **5** — one tall ground floor plus four upper window bands, on every elevation | Street-level photography of all four sides (see 2.4); *contradicted* by the assessor's "6" and by some permits, see 2.15 |
| Footprint | 58.6 x 47.7 m rotated block, 2,795 m2 | OSM way/147508936, reprojected + oriented bbox (measured) |
| Lot | 31,929 sf (0.733 acre) | assessor record via PropertyShark |
| Floor area | ~140,375 sf assessed, marketed as ~147,000–150,000 sf | assessor + leasing listings |
| Parapet height | **23.0 m** above grade | OSM `height=23` (Bing) and SF 2010 LiDAR `SF3776115` hgt median 22.74 m / mean 23.02 m — two independent sources agreeing |
| Rooftop crest | **26.5 m** (bulkhead) | SF 2010 LiDAR `SF3776115` hgt max 26.62 m, corroborated by the bulkhead's shadow in Esri aerial imagery |
| Ground | 5.64 m NAVD88 mean over the footprint, range 0.97 m — flat made ground | SF 2010 LiDAR (measured) |
| Anchor | -122.3958224, 37.7808279 | footprint AABB centre (measured); vertex mean is 0.07 m away, so the two agree |
| Grid heading | Long axis (3rd Street frontage) 134.9 / 314.9 deg true; front normal 44.9 deg | OSM geometry (measured) |
| Lot condition | Corner block: 3rd Street (NE), Bryant Street (NW), Ritch Street (SW), a service lot / surface parking (SE). No party walls — all four elevations are exposed | OSM street geometry + photography (measured) |
| Current use | Multi-tenant creative office, class B/C; long-time tenant Organic Inc. signage on the corner crown | leasing material, photography |
| Roof plant | 4+ rooftop units; 2015 permit added two omnidirectional antennas, a weather sensor/GPS unit and an equipment cabinet on the roof | DBI PA 2015-1123, aerial imagery |
| Other fabric | Concrete parapet seismically braced 1993; reroofed 1998; a window converted to a roll-up door 2001; fire escape on the 3rd Street facade | DBI permits |

### 2.2 Sources

- https://www.openstreetmap.org/way/147508936 — footprint geometry, addr tags, `height=23` (Bing-traced)
- https://data.sfgov.org/resource/i98e-djp9.json — DBI building permits, block 3776 lot 115 (100 records, 1990–2022): storey counts (5 and 6, inconsistent), construction type, the 1993 concrete-parapet bracing, the 1998 reroof, the 2001 window-to-roll-up-door conversion, the 2014 fire-escape ladder repair, the 2015 rooftop antenna/weather-sensor/equipment-cabinet installation, and a long run of floor-by-floor office tenant improvements on floors 1–5
- https://data.sfgov.org/resource/ynuv-fyni.json — SF 2010 LiDAR building footprints, record `SF3776115`: 11,323 half-metre cells (≈2,831 m2, corroborating the OSM polygon), ground mean 5.64 m, height median 22.74 m, height mean 23.02 m, height max 26.62 m
- https://www.propertyshark.com/mason/Property/30534806/500-3-St-San-Francisco-CA-94107/ — 1927, "6" stories, 140,375 sf, class B masonry/concrete, industrial use, 31,929 sf lot
- https://www.cushmanwakefield.com/en/united-states/properties/for-lease/office/ca/san-francisco/500-third-street/ — 1927, ~150,000 sf, class C, SOMA
- Google Street View panoramas around the block (2025 imagery) — the four elevations, the corner crown, the flag masts, the storefront base; panoids `ZFJr8xIGkghVJpdM2pRWOg` (3rd St), `qpFsB9_v9E-B6X37FmAqQA` (Bryant St), `6Hg1dMtfmyUJp_yT_3roQQ` (Ritch St), `VG7suaG1CGPCMYyyOi0dmQ` (SE lot), `d6j41Ahotp0p7DDR8aQ7dg` (3rd/Bryant corner), `BNesNZmzyPdbYOhIibJ-Yg` (3rd St south end)
- Esri World Imagery (`services.arcgisonline.com/.../World_Imagery`) — roof plan: the bulkhead near the centre-north, the mechanical cluster on the south half, the flat pale membrane field

### 2.3 Orientation and placement

A full quarter block in South Beach/SoMa, at the south corner of the 3rd and
Bryant intersection. The SoMa grid here is rotated ~45 deg from true north: the
3rd Street frontage runs 134.9 / 314.9 deg and the Bryant frontage 44.9 / 224.9
deg. The block is very nearly square; the 3rd Street side is the longer of the
two by 11 m.

Measured footprint, reprojected with the app's tangent projection and recentred
on the footprint AABB centre (x east, y north, metres, CCW):

```
A  ( -4.197,  37.788)   north corner  (3rd x Bryant)
D  (-37.293,   3.465)   west corner   (Bryant x Ritch)
C  (  3.933, -37.788)   south corner  (Ritch x SE lot)
B  ( 37.293,  -3.587)   east corner   (SE lot x 3rd)
```

| Edge | Length | Outward normal (true) | What it is |
|---|---|---|---|
| A → D | 47.68 m | 314.0 deg (NW) | **Bryant Street** front |
| D → C | 58.32 m | 225.0 deg (SW) | **Ritch Street** service rear |
| C → B | 47.78 m | 134.3 deg (SE) | SE elevation over the surface parking lot |
| B → A | 58.59 m | 44.9 deg (NE) | **3rd Street** front (the address side) |

Author `+Y` = north and place the polygon exactly as measured. The contract's
"front faces −Y" cannot be met — the real front faces north-east — so real-world
orientation wins per the README orientation note and AGENTS rule 5.

### 2.4 What each side shows

**North-east (3rd Street) — the address face, 58.6 m.** A warm-grey painted
concrete frame. The ground floor is tall and charcoal: deep storefront bays with
big dark-framed glazing above a low solid base, divided by concrete pilasters
with simple moulded capitals, and a recessed main entry near the middle carrying
metal "500 THIRD" letters on its head beam. A strong horizontal band caps the
ground floor. Above it, four identical floors: each structural bay holds one
large steel-sash industrial window — a fine grid of small panes, dark charcoal
frames — recessed behind narrow pilaster strips, with a light spandrel panel
under each. A steel fire escape hangs on the southern part of the elevation. The
parapet is plain and light, with a row of slender flag masts standing on it.

**North-west (Bryant Street), 47.7 m.** The same elevation, seven bays instead of
nine, and with the ground floor treated as very tall glazed bays over a solid
base panel rather than as shopfronts. The corner crown carries the sign band on
this face as well.

**South-east (over the parking lot), 47.8 m.** The plainest of the three glazed
faces: a solid painted base, then the same four window bands, with a couple of
through-wall air-conditioning units and a wall light on the concrete. No entry.
Because the neighbouring lot is open parking, this elevation is fully visible
from the app's camera and must be modelled as a real facade, not a party wall.

**South-west (Ritch Street) — the service rear, 58.3 m.** Cream-painted concrete,
almost blind. A roll-up vehicle door (numbered 211 Ritch), a personnel door, a
big louvre panel, exposed conduit, and small punched windows rather than the big
sashes. The south corner of the block is a tall blank wall.

**Top.** A pale flat membrane field bounded by the parapet, carrying:

1. the bulkhead penthouse near the centre-north — the stair/elevator head, the
   tallest thing on the building and the crest at 26.5 m;
2. a smaller elevator overrun / plant box beside it;
3. a cluster of a dozen small mechanical units and two duct runs across the
   southern half;
4. the 2015 antenna mast and equipment cabinet;
5. the flag masts standing on the 3rd Street and Bryant parapets;
6. the raised, capped corner crown at the north corner.

### 2.5 Recognition cues (ranked)

1. **The steel-sash window grid**, repeated identically across three elevations —
   a wall that is more window than wall, in a light concrete frame.
2. **The block itself**: a near-square 58 x 48 m prism, 5 storeys, flat top,
   sitting at 45 deg on its own quarter block with open ground on two sides.
3. **The charcoal storefront base** under the light frame — the single strongest
   value contrast on the building.
4. **The raised, signed corner crown** at 3rd and Bryant, lit at night.
5. **The flag-mast row** along the street parapets.

### 2.6 Miniature translation

**Preserve**

- The true footprint polygon and the 45 deg heading
- Five storeys: one tall ground floor (≈5.6 m) and four uppers of ≈4.0 m
- The bay rhythm: 9 bays on 3rd, 7 on Bryant, 7 on the SE elevation
- The parapet at 23.0 m and the bulkhead crest at 26.5 m
- The blind service character of the Ritch Street rear
- The corner crown's extra height and its sign band on both faces

**Simplify / exaggerate**

- Each steel-sash window becomes one `Toy_glass` slab in an `Toy_ink` reveal with
  a 2 x 2 mullion cross — rhythm, not mullion count (style bible §5). The real
  windows are roughly 8 x 6 panes; modelling that would cost the whole budget and
  read as noise at city distance
- Pilasters and spandrels become simple proud strips, slightly wider than scale,
  so the grid still reads at 200 m
- The ground floor becomes one continuous charcoal band with glazed bays and a
  single recessed entry — no capitals, no mouldings
- The "500" numerals over the entry become chunky extruded solids, oversized (§8)
- The corner sign band becomes a plain illuminated panel, not lettering
- Flag masts become 8 chunky square masts with small flag plates, all kept below
  the bulkhead crest so the bbox top stays at 26.5 m
- The mechanical cluster becomes eight identical beveled boxes on a low curb
- The fire escape is dropped: thin diagonal steelwork is exactly the detail the
  style bible tells us to strip

**Do not add** a roof deck, a penthouse pavilion, planting, or a crown silhouette.
This building is a disciplined box and must stay one.

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not
a straitjacket — adjust after the first aerial review render.

1. **Body:** extrude the measured footprint from z=0 to z=22.00, `Toy_stone`,
   with a `Toy_sand` roof cap.
2. **Ground floor:** a charcoal `Toy_ink` band 0 → 5.60 inset 0.10 m from the
   wall face on the three public elevations, over a `Toy_stone` plinth 0 → 0.55;
   `Toy_glass` bays inside it; a `Toy_trim` belt cornice 5.60 → 6.00 proud
   0.25 m all the way round.
3. **Pilasters:** `Toy_trim` strips 0.85 m wide, proud 0.22 m, from 6.00 to
   22.00, at every bay boundary on the NE, NW and SE elevations, plus one at each
   of the four corners.
4. **Windows:** for each bay and each of the four upper floors, a window unit at
   z = floor+0.85 to floor+3.75 with floors at 6.00, 10.00, 14.00, 18.00 —
   `Toy_ink` reveal, `Toy_glass` slab, one vertical and one horizontal mullion.
5. **Spandrels:** `Toy_stone` panels between the window bands, proud 0.08 m.
6. **Ritch Street rear:** solid `Toy_stone` wall; two `Toy_ink` roll-up door
   recesses 4.0 x 4.2 m, one `Toy_ink` personnel door, one `Toy_roofd` louvre
   panel 3.0 x 2.4 m, and three columns of small punched `Toy_glass` windows
   0.95 m square at each upper floor.
7. **Parapet:** `Toy_stone` band 22.00 → 22.85 inset 0.30 m, `Toy_trim` coping
   22.85 → 23.00 proud 0.10 m.
8. **Corner crown:** the parapet raised to 24.70 for 13.0 m along the 3rd Street
   edge and 11.0 m along the Bryant edge from the north corner, `Toy_stone` with
   an `Toy_ink` cap; a `Toy_white_Glow` sign panel 1.10 m tall proud 0.14 m on
   each of the two outer faces.
9. **Entry:** on 3rd Street, a 4.6 m wide recess 0.45 m deep in the charcoal
   band, an `Toy_ink` door, a `Toy_glassl` transom, and extruded `Toy_ink`
   **500** numerals 0.95 m tall on the beam above it.
10. **Flag masts:** five on the 3rd Street parapet, three on Bryant, `Toy_steel`
    0.18 m square, from 23.00 to 26.20, each with a small `Toy_red` or
    `Toy_navy` flag plate.
11. **Bulkhead:** `Toy_white` box 16.0 x 11.0 m centred 4.0 m north-east of the
    plan centre, 22.00 → 26.30, with a `Toy_roofd` cap 26.30 → **26.50** — the
    crest.
12. **Elevator overrun:** `Toy_white` box 5.2 x 4.6 m beside it, top at 25.20.
13. **Mechanical cluster:** eight `Toy_roofd` boxes 1.7 x 1.2 x 0.95 m on a
    0.15 m curb across the southern third, plus two low duct runs and a short
    `Toy_steel` antenna mast with an equipment cabinet.
14. Bevel 0.10 m, 2 segments, on the massing solids; window mullions unbeveled.

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_stone` | `#d9d2c2` | painted concrete walls, spandrels, parapet, corner crown, plinth |
| `Toy_trim` | `#f3efe6` | pilaster strips, belt cornice, parapet coping |
| `Toy_sand` | `#ece4d4` | roof membrane field |
| `Toy_white` | `#f7f4ec` | rooftop bulkhead and elevator overrun |
| `Toy_ink` | `#3a3530` | storefront band, window reveals and mullions, doors, crown cap, 500 numerals |
| `Toy_glass` | `#2a4d73` | steel-sash window glazing, storefront glazing, punched rear windows |
| `Toy_glassl` | `#6f95b8` | entry transom, the lit bays' day colour |
| `Toy_steel` | `#9aa0a6` | flag masts, antenna mast, roof curbs |
| `Toy_roofd` | `#45454a` | mechanical units, ducts, equipment cabinet, louvre |
| `Toy_red` | `#c4453c` | flag plates (one accent) |
| `Toy_navy` | `#2c4a70` | flag plates (the other) |
| `Toy_white_Glow` | `#f7f4ec` | the corner sign band at night |
| `Toy_glassl_Glow` | `#6f95b8` | the lit window bays and the entry transom at night |

**Night state.** A dark grey block with a lit corner. The sign band on the crown
is the hero glow — it is what the corner is for. The supporting rhythm is a
restrained scatter of lit upper bays (about one bay in four, never a whole floor)
plus the entry transom and two lobby bays at street level; everything else stays
dark. Glow shells are thin surfaces proud of the opaque glazing behind them — the
app renders `_Glow` in a separate layer at ~12% alpha by day, so a primary
surface must never be authored as glow.

### 2.9 Top surface

At 26.5 m this is a low building under a camera that looks down, so the roof is a
large part of its screen area — but unlike 550 Third it has no designed roof.
Honesty is the right call: a pale membrane field, the bulkhead as the one strong
object, the mechanical cluster as texture on the south half, and the flag masts
and crown breaking the parapet line. The composition is deliberately
asymmetric — bulkhead north, plant south — so the roof reads as a real working
roof rather than a blank lid.

### 2.10 Scope

**In the GLB:** the building, its parapets and corner crown, the sign band, the
flag masts, the entry and its numerals, the rooftop bulkhead, elevator overrun,
mechanical plant, ducts and antenna

**Not in the GLB:** 3rd Street, Bryant Street, Ritch Street, the SE parking lot,
neighbouring buildings, street trees, street furniture, people, vehicles,
plinths, cameras or lights

### 2.11 Triangle budget

Cap 22,000 — higher than 550 Third's 14,000 because this building is four times
the wall area and its identity is a repeated window unit rather than a handful of
roof objects. Suggested split: shell, parapet, crown and roof field ~2.5k; the
92 upper-floor window units ~11k; pilasters and spandrels ~2.5k; ground floor,
entry and numerals ~1.5k; Ritch Street rear ~1k; bulkhead, overrun, plant, masts
~2k; spare ~1.5k.

### 2.12 Draft manifest entry

```json
{
  "id": "500-third",
  "file": "500-third.glb",
  "anchor": [
    -122.3958224,
    37.7808279
  ],
  "targetHeightM": 26.5,
  "cat": 3,
  "name": "500 Third Street",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

`dims` and `tris` are placeholders until the asset is built and validated.
`loadRadius` is the skill's default `max(2500, targetHeightM * 30)`; at 26.5 m
that floor of 2,500 m applies.

### 2.13 Integration notes (for later, not this task)

- **New landmark.** Add a `pipeline/lib/landmarks.mjs` entry (`id: '500Third'`,
  lon/lat as above, `height: 26.5`) and re-bake the affected tiles, or the baked
  OSM block will sit inside the model.
- **The exclusion radius is unusually forgiving here, but must still be
  measured.** `excluded()` in `pipeline/buildings.mjs` drops a footprint when its
  ring centroid *or* any of its vertices falls inside the radius. This building's
  ring centroid sits within ~1 m of the anchor, so the centroid test alone will
  drop it at any radius above ~1 m. The nearest *neighbour* geometry is across
  the ~12 m SE service lot, whose closest vertices should be ~36 m from the
  anchor — but that is inferred from OSM, not from the bake input. Measure the
  window against the pipeline's own simplified DataSF footprints before choosing,
  exactly as `docs/asset-plans/550-third.md` §2.13 describes, and start from a
  provisional `exclude: 12`.
- Manifest id `500-third` maps to registry id `500Third`.
- No camera preset key. At 26.5 m this is a block in the SoMa fabric, not a
  destination.
- The site is flat made ground (LiDAR ground mean 5.64 m NAVD88, range 0.97 m
  over the whole footprint). Terrain seating should be uneventful; check it
  anyway.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] bbox top exactly 26.5 m so the loader's scale factor is 1.0
- [ ] Dimensions plausible in meters and consistent with 2.1
- [ ] Triangles at or under 22,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the crown sign band, the scattered lit bays and the entry
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (per-object signed
      volume + deterministic ray test)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + night render + contact sheet regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

- **Storey count.** The assessor record says 6 and DBI permits say 5 in some
  applications and 6 in others; every photograph of every elevation shows one
  tall ground floor plus four upper window bands, and 5 x ~4.4 m plus a parapet
  is exactly the measured 23 m. This dossier models 5 and treats the "6" as a
  count that includes the ground floor's mezzanine (permits do reference
  mezzanine work at the first floor). If a drawing says otherwise, the window
  bands change but the height does not.
- **The bulkhead's plan size is inferred from one aerial** and its height from a
  single LiDAR maximum cell. If it is smaller or lower, `targetHeightM` moves
  with it — nothing else in the model depends on it.
- OSM `height=23` and the LiDAR median agree at ~22.8 m, which is the *parapet*,
  not the crest. Do not use it as the target height, and do not "correct" the
  bulkhead away to make the model match it.
- The 2015 rooftop antenna/weather-sensor permit means the roof carries thin
  vertical clutter that no aerial resolves. It is modelled as one short mast and
  a cabinet; that is a design decision, not a measurement.
- Bay counts (9 / 7 / 7) are counted from oblique Street View frames, not from a
  drawing. If a straight-on elevation contradicts them, the pilaster spacing
  changes but nothing else does.
- The building's paint reads warm grey on 3rd and Bryant and cream on Ritch in
  the available imagery; that may be lighting rather than a real colour change.
  This dossier treats the whole shell as one warm grey.
