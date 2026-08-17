# 318 Brannan Street — SF-SIM asset plan

A 1961 reinforced-concrete office building on the northwest side of Brannan Street,
one lot southwest of 300 Brannan and directly northeast of the JAX tasting-room yard
at 326. It is the **first mid-century building** in this Brannan family: everything
else on the block face — 350, 358, 362, 370, 380 — is a 1910s–20s brick-and-timber
warehouse. This one is a low, wide, pale concrete box with **two full-width dark
awnings** banding its facade, and it reads as a completely different decade at a
glance.

It is also the **freest-standing** building the manifest has carried on this block:
a 4.8 m side yard on the northeast, a 5.7 m rear yard on the northwest, and an open
neighbour's yard on the southwest. All four elevations are seen, and the roof — a
mid-grey membrane carrying a maze of white ductwork, one big square skylight and a
cluster of dark mechanical units — is the surface the app's camera actually looks at.

The brief is "the pale two-banded box": get the two dark awning bands and the low
wide proportion right, and design the roof like a facade.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/318-brannan/`. This document is the plan only: Part 1 is the runnable task
prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `318-brannan` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3927890, 37.7816014` |
| Target height | **8.6 m** to the parapet cap; roof deck 7.9 m |
| Footprint | 17.96 m (Brannan frontage, SE) x 23.87 m deep; 428.8 m2, measured |
| Triangle cap | 8,500 |
| Category | `3` (office) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 318 Brannan Street GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of 318 Brannan Street in San Francisco and deliver
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
7. `artifacts/350-brannan/` — the closest reference implementation by *size and site*:
   the same block face, a similar full-lot rectangle, and a build script whose
   footprint / panel / parapet / roof-furniture helpers this asset should reuse rather
   than reinvent
8. `artifacts/358-brannan/` — read its REPORT.md for the tight-exclusion and
   two-level-roof lessons on this same block
9. `docs/asset-plans/318-brannan.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Must capture

- A **low, wide, pale two-storey concrete box**: 17.96 m of street frontage, 23.87 m
  deep, 8.6 m tall. It is markedly *lower* than 334/340 Brannan next door (12.1 m) and
  much lower than 300 Brannan behind it — the squatness is part of the identity
- **The two full-width dark awnings** — the single strongest cue. One at the
  second-floor head carrying the tenant sign band, one over the ground-floor
  storefront. Two horizontal dark bands across a cream box, seen from any distance
- **The continuous second-floor ribbon window** trapped between the two awnings:
  two groups of horizontal aluminium sash split by one broad pale pier
- **The ground-floor storefront** — large plate-glass bays in slim pale frames over a
  low pale bulkhead
- **The northeast end bay of the front**: a broad pale pier, a dark sign panel
  carrying the street number, and a recessed glass entrance door
- **All four elevations are exposed** — this building is free-standing on three sides
  and nearly so on the fourth. There are no party walls to hide behind. The northeast
  flank is blank pale concrete (service rooms inside), the southwest flank carries a
  restrained row of punched windows, the northwest rear is a utilitarian back with a
  roll-up freight door
- **The roof, which is the hero surface**: a mid-grey membrane, a white parapet coping
  ring, one ~2.6 m square skylight northeast of centre, a ladder-and-comb network of
  raised white ducts across the southwest two-thirds, and a cluster of dark mechanical
  units on the southwest side

## Research 318 Brannan Street independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world orientation,
and gather references covering:

- The Brannan Street elevation, day and night, and the current awning graphics
- The northeast and southwest flanks — both are exposed and both will be rendered
- The northwest rear and its yard
- Aerial and roof views: the duct network, the skylight, the mechanical cluster. The
  camera looks down; this roof is 429 m2 of visible surface
- The exact parapet height — the weakest number in this dossier (see 2.15)

Prefer architect/engineer publications, owner or institutional material, planning and
permitting documents, architectural press, geolocated photography, and aerial/satellite
imagery. Never rely on a single photograph, a single AI-generated image, or a single
unsourced 3D model. Separate verified facts from visual inference; if sources disagree,
document the disagreement and decide.

**Three source conflicts are already known and resolved in 2.1 — re-check them, do not
silently re-inherit the wrong value:** the build year is **1961** per the National
Register district report and **1962** per the Assessor (2.15 risk 4); the DataSF LiDAR
`hgt_maxcm` of **42.02 m is not this building** and must never be used as a height
(2.15 risk 2); and the parcel is 23.64 m wide on Brannan while the *building* is only
17.96 m wide — the remaining 4.8 m is a low entry/side-yard strip that is **not** part
of the modelled mass (2.15 risk 1).

## Create a reference dossier

Write `artifacts/318-brannan/REFERENCE.md` containing: source links and what each
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

This is a **secondary building** in the style bible's detail budget (§21). Clear
massing, one strong facade rhythm, a deliberately designed roof, and exactly one
identity idea carried hard — the two dark bands. Resist hero-tier ornament. The single
biggest risk to this asset is that a pale box with two dark stripes gets *fussy*
instead of crisp.

The finished asset must be immediately recognizable as 318 Brannan Street, consistent
with the real building from all four sides and above, architecturally credible, and a
premium handcrafted miniature — not photorealistic, not voxel art, not generic
low-poly, and never accurate in one view while invented in the others.

## Scope of the exported asset

Export the single 1961 building: four elevations, the two awnings, the parapet, the
roof and its furniture.

Do not include unrelated surrounding city geometry: Brannan Street, the side-yard
driveway and its parked cars, the rear yard, the neighbours at 326 and 300 Brannan,
South Park, street trees, the sidewalk, parking meters, the fire hydrant, overhead
utility wires, people, plinths, cameras or lights. Temporary context may appear in
review renders but must not leak into the GLB.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary `.glb`;
real-world meters; origin at base center; minimum geometry Z ~ 0; applied transforms;
no negative scales; outward normals; no duplicate or foreign geometry; no image
textures; no transparency; flat-color materials named `Toy_*` from the project palette;
`_Glow` suffix only on surfaces that glow at night; no `Toy_body`; no cameras, lights,
animations, armatures or constraints; no external dependencies; at most 8,500 triangles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model drops
into the city at its real-world heading — the loader applies no rotation (`placeGeneric`
in `app/src/assets.js` only scales and positions). The Brannan Street front faces
**southeast, bearing 135.8°**; the rear faces **northwest, 315.8°**; the flanks face
**northeast 45.8°** and **southwest 225.8°**. The building is rotated about 45° off the
world axes, so build directly on the measured footprint rectangle in 2.3 rather than
modelling an axis-aligned box and rotating it.
Record the measured heading in `REPORT.md`.

**Height normalization:** the tallest geometry in the export (the parapet cap) must land
at exactly **8.6 m** so the loader's `targetHeightM / measuredHeight` scale is 1.0.

## Reproducible Blender workflow

Blender 5.2 LTS. Headless: `blender -b --python script.py -- args`.

Keep `artifacts/318-brannan/build_318_brannan.py` (deterministic build script),
`artifacts/318-brannan/318-brannan.blend`, and `artifacts/318-brannan/318-brannan.glb`.
The script must rebuild the model reliably enough for future revision. Do not modify or
rename an unrelated existing GLB to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras: `318-brannan-top.png`,
`318-brannan-north.png`, `318-brannan-east.png`, `318-brannan-south.png`,
`318-brannan-west.png`, plus `318-brannan-contact-sheet.png`, at least one high
three-quarter aerial beauty render `318-brannan-aerial.png`, and a night render
`318-brannan-aerial-night.png`.

The four elevations must share scale, framing, lighting, exposure and projection; use
orthographic or long-lens cameras; label directions from the researched orientation; the
top view must clearly show the parapet ring, the skylight, the duct network and the
mechanical cluster; the aerial view uses the style bible's camera assumptions (30-50
degrees down, long lens). Simple tabletop lighting, neutral warm background, minimal
depth of field, and every image must depict the same exported model.

Note that the axis-aligned elevation renders will each show the building at 45°, and the
"north"/"south" views see a flank and a front together. That is the expected consequence
of the real heading, not a camera error.

## Validate the exported GLB

Re-import `318-brannan.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture count,
camera count, light count, animation count, applied-transform status, negative-scale
status, normal-orientation status, unexpected geometry, and per-material contract
compliance. Render at least one review image from the re-imported asset. Write
`artifacts/318-brannan/validation.json` and `artifacts/318-brannan/REPORT.md`.

Note that the axis-aligned XY bounding box will be roughly **29.5 x 29.6 m** even though
the building is 17.96 x 23.87 m — that is the expected consequence of a ~45° real-world
heading, not a scale error.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this draft
entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "318-brannan",
  "file": "318-brannan.glb",
  "anchor": [
    -122.3927890,
    37.7816014
  ],
  "targetHeightM": 8.6,
  "cat": 3,
  "name": "318 Brannan Street",
  "estimated": true,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a separate, explicitly requested job — run `docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in `docs/asset-plans/318-brannan.md`.
````

---

## Part 2 — Research and design dossier

Compiled 16 August 2026 from the sources in 2.2. Values marked *inferred* or *estimated*
are visual or derived, not published figures — the executing agent must re-verify
anything it relies on.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Block / lot | 3775 / 100 | DataSF parcels `acdm-wktn` — `blklot=3775100`, `from_address_num = to_address_num = 318 BRANNAN`, active, mapped 1998-07-01 |
| Built | **1961** (NR district report) / 1962 (Assessor) | National Register South End Historic District case report; SF Assessor secured roll 2007-2025 (identical every year). See 2.15 risk 4 |
| Structure | Reinforced concrete, concrete exterior | National Register South End Historic District case report |
| Storeys | **2** | SF Assessor roll (`number_of_stories = 2.0`), every year 2007-2025; NR report ("2-story office structure") |
| Use | Commercial Office (Assessor class `O`, 0 dwelling units) | SF Assessor roll, every year 2007-2025 |
| Historic status | **Not evaluated / non-contributory** within the South End Historic District | NR district report — it is a modern intrusion in a 1900s-20s warehouse district, which is exactly why it looks different |
| Lot area | 6,769 sq ft = 628.9 m2 (Assessor); 627.7 m2 measured from the parcel polygon | SF Assessor roll; DataSF parcels — agree to 0.2% |
| Building area | 9,600 sq ft = 891.9 m2 | SF Assessor roll. 2 x 428.8 m2 = 857.6 m2 = 9,232 sq ft — **independently confirms the 429 m2 footprint and 2 storeys** |
| Ground floor lettable | ±4,500 sq ft = 418 m2 | THG Commercial listing + floor plan (scale 1" = 10') |
| Footprint | 428.8 m2; 17.96 m (SE frontage) x 23.87 m deep; a clean 4-vertex rectangle | DataSF LiDAR building footprint `SF3775100` (`mblr` matches the parcel), reprojected — **measured**. The THG floor plan's depth:width ratio is 1.32 against a measured 1.329 |
| Roof height (mode) | **7.78 m** above ground | DataSF LiDAR `hgt_majoritycm` — **measured**, the modal roof plane |
| Roof height (median) | 8.11 m | DataSF LiDAR `hgt_median_m` — measured, but pulled up by the extensive rooftop ductwork |
| Ground elevation | 11.56 m (NAVD88) min, 12.00 m modal | DataSF LiDAR `gnd_min_m` / `gnd_majoritycm` — app terrain handles this, not the asset |
| Zoning | CMUO (Central SoMa mixed use — office) | DataSF parcels; THG listing |
| Frontage heading | Brannan front faces 135.8° (SE); rear 315.8° (NW); flanks 45.8° (NE) and 225.8° (SW) | measured from the DataSF footprint rectangle |
| Site condition | Free-standing: 4.75 m side yard NE, 5.7 m rear yard NW, ~0.9 m to the SW property line with an open neighbour's yard beyond | measured, parcel polygon vs footprint polygon |
| Current occupants | KCA Engineers, Inc. (2nd floor, "318 Brannan St #2", est. 1960); ground floor marketed vacant 2024-25, previously Zephyr Real Estate | kcaengineers.com; THG Commercial listing (Sept 2025); Google Street View May 2025 |
| Prior tenants | Botrista Technology, Funomena, ScoutRFP, Izmocars — a multi-tenant address | SF business registrations via opengovus |
| Permits | 1982 "bldg use: office"; 2004 reroofing ($32k) | DataSF building permits `i98e-djp9`, block 3775 lot 100 — no facade alteration on record |

### 2.2 Sources

- `https://data.sfgov.org/resource/acdm-wktn` (DataSF Parcels) — **the address-to-lot link**: `3775100 = 318 Brannan St`, and the parcel polygon that establishes the side and rear yards. Neighbours on this block face are 012 = 326, 101 = 334, 015 = 340, 016 = 350, 017 = 358
- `https://data.sfgov.org/resource/ynuv-fyni` (DataSF Building Footprints, LiDAR-derived) — polygon `SF3775100` / `sf16_bldgid 201006.0008516`: the 4-vertex 428.8 m2 rectangle, `hgt_majoritycm 778`, `hgt_median_m 8.11`, `gnd_min_m 11.56`, 1,730 cells at 50 cm
- `https://data.sfgov.org/resource/wv5m-vpq2` (SF Assessor Historical Secured Property Tax Rolls) — 1962, 2 storeys, 9,600 sq ft on a 6,769 sq ft lot, Commercial Office, class O, 19 consecutive years unchanged
- `https://data.sfgov.org/resource/i98e-djp9` (SF Building Permits) — 1982-05-13 #8203762 "bldg use: office"; 2004-05-18 #200405184153 reroofing
- `https://sfplanninggis.org/docs/NatRegDistricts/2008-06-26_Final-NR-SouthEndHistDist.pdf` — National Register certification, South End Historic District: 318 Brannan listed as APN 3775/104-105 (formerly 3775 100), **"1961, 2-story reinforced-concrete office structure with concrete exterior"**, Not Evaluated / Non-contributory
- `https://www.thgcommercial.com/project/318-brannan-street/` and its flyer `318-Brannan-Ken-20250909_compressed.pdf` (Sept 2025) — a near-orthographic **front elevation photograph**, the **ground-floor plan at 1" = 10'**, two interior photographs, and the attribute list (roll-up door, high ceilings, two sides of windows, dedicated reception, six private offices, two conference rooms, data room, kitchenette)
- `https://www.kcaengineers.com/location.html` — occupancy and the useful locational sentence: "the second building on the north side of Brannan Street west of the intersection of Brannan and Second Street"
- Google Street View, Brannan Street panos — capture **May 2025** (straight-on and close obliques: the two awnings, the ribbon window, the storefront, the number bay, the entrance) and **Dec 2024** (oblique from the southwest: the parapet line, and 318 read against 334/340 next door)
- Bing/Vexcel aerial imagery at z20 — the roof: membrane, parapet coping, the square skylight, the duct network, the mechanical cluster, and the side-yard parking
- https://www.openstreetmap.org/way/112759869 — address and `height=8` confirmation; its 6-vertex geometry (451 m2) agrees with DataSF's rectangle to 5% and is *not* used for measurement

### 2.3 Orientation and placement

The building sits mid-block on the northwest side of Brannan Street, on the Brannan
property line, hard against the southwest lot line, with a 4.75 m side yard on the
northeast and a 5.7 m rear yard on the northwest. It is rotated about 45° from the
world axes, like the whole SoMa grid.

The DataSF LiDAR polygon has exactly **four vertices** and is a true rectangle to within
3 mm on each pair of opposite edges — no OBB fitting or noise reduction is needed here,
unlike 358 and 362 Brannan. Build it as measured.

Footprint rectangle, in Blender coordinates (metres, `+X` east, `+Y` north),
counter-clockwise, already centred on the anchor `-122.3927890, 37.7816014`:

```
(  1.867, -14.819)
( 14.756,  -2.312)
( -1.867,  14.819)
(-14.756,   2.312)
```

(listed front-SW, front-NE, rear-NE, rear-SW)

Edges, with outward normals:

| Edge | Length | Faces | Elevation |
|---|---|---|---|
| `(1.867,-14.819) -> (14.756,-2.312)` | 17.96 m | SE 135.8° | **Brannan Street front** |
| `(14.756,-2.312) -> (-1.867,14.819)` | 23.87 m | NE 45.8° | northeast flank (side yard / parking) |
| `(-1.867,14.819) -> (-14.756,2.312)` | 17.96 m | NW 315.8° | rear (rear yard) |
| `(-14.756,2.312) -> (1.867,-14.819)` | 23.87 m | SW 225.8° | southwest flank (326 Brannan's yard) |

Because of the 45° heading the axis-aligned bounding box is ~29.5 x 29.6 m for a
building that is 17.96 x 23.87 m. That is correct.

### 2.4 What each side shows

**Southeast (Brannan Street front)** — The hero elevation and a genuinely composed one.
An off-white painted concrete wall, 17.96 m wide and 8.6 m to the parapet, organised
into five horizontal layers. Bottom to top: a low pale **bulkhead**; a run of large
**plate-glass storefront bays** in slim pale frames, divided by one broader pale pier
near the centre; a **full-width dark awning** projecting about 1.2 m over the whole
storefront, carrying the ground-floor tenant's name; a plain pale **spandrel band**; a
continuous **second-floor ribbon window** — horizontal aluminium sash in pale frames,
two rows of lights, split into two groups by one broad pale pier; a second
**full-width dark awning** at the second-floor head, carrying the upper tenant's sign
band; then a thin strip of pale wall and the flat **parapet cap**. At the northeast end
of the frontage, past a broad pale pier: a dark **number panel** carrying large white
numerals and, below it, a **recessed glass entrance door**.

The two dark awnings are the building. They are what makes a cream box read at 200 m.

**Northeast flank** — Exposed the full 23.87 m to the side-yard driveway, where cars
park right against it. Blank pale concrete with a shallow horizontal reveal at the
second-floor line and a service door near the rear. **Do not invent windows here** —
the ground-floor plan puts the lobby, stairs, restrooms, copy room and electrical room
along this wall, and it is a blind service elevation in every reference.

**Southwest flank** — Exposed above 326 Brannan's low fenced yard and single-storey
tasting room, so it is seen from Brannan Street and from above. The listing's "two
sides of windows" and the ground-floor plan's openings both put daylight on this side:
a restrained, evenly spaced **row of punched windows at the second floor** and two or
three at ground level, in pale frames. Nothing more; the wall is pale concrete.

**Northwest (rear)** — A working back onto the rear yard, not a designed elevation.
Pale concrete, a wide grey **roll-up freight door** (the listing's "Roll Up Door"; the
interior photograph shows it at the rear of the open floor), a pedestrian service door
at the northeast end, and a small group of second-floor windows.

**Top** — 429 m2 of flat roof and the single most-seen surface in the app. A **mid-grey
membrane** inside a **white parapet coping ring**. Northeast of centre, a **square
skylight about 2.6 m on a side** on a raised white curb — the brightest thing on the
roof. Across the southwest two-thirds, a **ladder-and-comb network of raised white
ducts** roughly 0.6-0.8 m wide: two long trunk runs parallel to Brannan with four or
five branches running back from them. On the southwest side, a **cluster of dark
mechanical units** — two or three boxes plus small condensers. A handful of small round
vents scattered over the rest. The northeast third of the roof is deliberately clear
membrane.

### 2.5 Recognition cues (ranked)

1. **Two full-width dark awning bands on a pale box** — the whole identity, and the only
   cue that survives to thumbnail size
2. **Low and wide** — 8.6 m against 334/340 Brannan's 12.1 m two doors away. If it is
   not visibly the shortest thing on the block face, it is wrong
3. **The mid-century concrete character** — flat pale planes, a continuous horizontal
   ribbon window, no brick, no cornice, no ornament. It is the one modern building among
   1910s warehouses
4. **The roof's duct maze + one bright square skylight**
5. The northeast number-panel bay with its recessed glass door

### 2.6 Miniature translation

**Preserve**

- The 17.96 x 23.87 m proportion and the real 45° heading, exactly
- The two dark bands' full width and their vertical positions relative to each other —
  the gap of pale spandrel between the lower awning and the ribbon window is what makes
  the composition read as three stripes rather than one blob
- The free-standing condition: four designed elevations, no invented party walls
- The flat parapet as a clean unbroken line on all four sides

**Simplify / exaggerate**

- The awnings are thickened and given a slightly deeper projection than reality so the
  bands cast a real shadow line from the aerial camera. This is the one place semantic
  exaggeration is spent
- The ribbon window's two rows of many small lights become one glazed panel per group
  with a single horizontal transom reveal; individual mullions disappear
- The storefront's several bays become four glazed panels in a pale frame
- Awning lettering, the number plate's numerals, the door hardware, the utility wires,
  the parking meters, the hydrant and the street trees are all dropped — sub-pixel at
  city scale. The number panel stays as a dark rectangle; it is the shape that reads
- Roof clutter becomes: one skylight box, two duct trunks with four branches, two
  mechanical boxes, one small condenser, three vent cans. Nothing more — this roof is
  busy in reality and will turn to noise if modelled literally

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not a
straitjacket — adjust after the first aerial review render.

1. Body: extrude the 2.3 rectangle from z=0 to z=7.9 (`Toy_cream` walls), cap
   `Toy_steel` — the roof membrane.
2. Parapet: ring on all four edges, z=7.9 to **z=8.6**, 0.30 m thick, `Toy_white`
   coping. This sets the bounding-box top and must land exactly on 8.6.
3. Brannan bulkhead: `Toy_stone` band, z=0 to z=0.55, full 17.96 m, 0.08 m proud.
4. Brannan storefront: `Toy_glass` glazing z=0.55 to z=3.35 in four bays, `Toy_white`
   mullions 0.18 m wide between them and one broader 0.55 m `Toy_cream` pier at the
   centre. Reserve the northeast 3.2 m of the frontage for step 8.
5. Lower awning: `Toy_navy` slab, z=3.35 to z=4.35, projecting 1.20 m from the wall,
   full width across steps 4 and 8, with a 0.10 m `Toy_ink` shadow reveal on its
   underside.
6. Spandrel: plain `Toy_cream` wall z=4.35 to z=4.90.
7. Second-floor ribbon: `Toy_glass` panels z=4.90 to z=6.35 in two groups split by one
   0.65 m `Toy_cream` pier, in `Toy_white` frames, with a single 0.10 m `Toy_white`
   transom reveal across each group at z=5.75.
8. Northeast end bay of the front: a 0.55 m `Toy_cream` pier, then a `Toy_ink` number
   panel z=4.35 to z=5.60 set 0.06 m proud, and below it a recessed `Toy_glass`
   entrance door z=0 to z=2.60 in a `Toy_white` frame, set back 0.35 m.
9. Upper awning: `Toy_navy` slab, z=6.40 to z=7.60, projecting 1.10 m, full width,
   same `Toy_ink` underside reveal. Leave pale wall from z=7.60 to the parapet.
10. Southwest flank: five `Toy_glass` punched windows z=4.90 to z=6.20, 1.4 m wide,
    evenly spaced, in `Toy_white` frames; two more at z=1.0 to z=2.6 toward the rear.
11. Rear: a 3.6 m `Toy_roofd` roll-up door z=0 to z=3.4 toward the southwest end, a
    1.0 m `Toy_ink` pedestrian door at the northeast end, and one `Toy_glass` window
    group z=4.90 to z=6.20 across the centre.
12. Northeast flank: blank `Toy_cream`, with one 0.06 m `Toy_stone` horizontal reveal at
    z=4.35 running the full length, and a single 1.0 m `Toy_ink` service door near the
    rear.
13. Roof furniture, on the membrane at z=7.9: one skylight 2.6 x 2.6 x 0.35 m
    (`Toy_glassl` on a `Toy_white` kerb) placed northeast of centre; two duct trunks
    0.70 m wide x 0.55 m tall running parallel to Brannan, with four branches running
    back from them (`Toy_white`); two mechanical boxes 1.8 x 1.3 x 1.0 m and one
    1.0 x 0.8 x 0.7 m condenser (`Toy_roofd`) grouped on the southwest side; three vent
    cans 0.4 m diameter x 0.5 m (`Toy_steel`).
14. Bevel 0.10 m, 2 segments on the masses; 0.04/1 on applied panels and awnings.

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_cream` | `#f2ede3` | the painted concrete walls on all four elevations, the piers, the spandrel |
| `Toy_white` | `#f7f4ec` | parapet coping, window and storefront frames, transom reveals, skylight kerb, the roof ducts |
| `Toy_stone` | `#d9d2c2` | the Brannan bulkhead and the northeast flank's reveal |
| `Toy_navy` | `#2c4a70` | **both awnings** — the identity surface |
| `Toy_glass` | `#2a4d73` | storefront glazing, the second-floor ribbon, flank and rear windows, the entrance door |
| `Toy_glassl` | `#6f95b8` | the roof skylight |
| `Toy_steel` | `#9aa0a6` | the roof membrane, the vent cans |
| `Toy_roofd` | `#45454a` | the rear roll-up door, the roof mechanical units |
| `Toy_ink` | `#3a3530` | the number panel, pedestrian and service doors, awning underside reveals |
| `Toy_glassl_Glow` | `#6f95b8` | **the lit second-floor ribbon window** — the night hero |
| `Toy_glass_Glow` | `#2a4d73` | two lit ground-floor storefront bays |
| `Toy_gold_Glow` | `#caa64a` | a small warm strip over the recessed entrance |

Note on the awning colour: the real awnings read near-black in the May 2025 Street View
and dark navy in the listing photograph. `Toy_navy` is chosen over `Toy_ink` because two
pure-black bands on a cream box go dead and heavy at miniature scale, and because navy
is truthful to the better-lit reference. It also keeps this building distinct from 380
Brannan's `Toy_ink` sign band 100 m southwest. Record the choice in `REPORT.md`.

Note on the roof membrane: `Toy_steel` (mid grey) rather than the usual `Toy_roofd`
(near-black). The aerial imagery shows a genuinely pale grey membrane, and a mid grey is
what lets the white ducts and the white coping ring read against it. A dark deck here
would be both untrue and illegible.

**Night state (required).** Glow surfaces must be thin shells proud of the opaque
surface behind them — the app renders `_Glow` in a separate layer that is roughly 12%
alpha per layer by day, so a closed shell reads at about 23% and a primary surface must
never be authored as glow. Hero glow: the **second-floor ribbon window**, lit end to
end — an engineering office that works late, and a continuous bright band trapped
between two dark awnings is the single best night image this building can give.
Supporting accents: two of the four ground-floor storefront bays lit, and a small warm
strip over the entrance. The awnings, the flanks and the rear do **not** glow.

### 2.9 Top surface

429 m2 of roof, seen constantly from above, and the reason this asset is worth building
carefully. The composition is: a clear white coping ring; a mid-grey field; one bright
skylight placed off-centre toward the northeast so the roof is not symmetrical; a
white duct ladder occupying the southwest two-thirds; and a dark mechanical cluster
anchoring the southwest corner. Keep the northeast third *empty* — the contrast between
the busy half and the clear half is what makes the roof read as designed rather than
sprinkled. Nothing on this roof should exceed 2 m in plan except the duct runs, and no
piece should be taller than 1.0 m; the parapet is only 0.7 m above the deck and
anything taller breaks the silhouette.

### 2.10 Scope

**In the GLB:** the single 1961 building — body, parapet, all four elevations, both
awnings, the number-panel bay and entrance, the roof and its furniture

**Not in the GLB:** Brannan Street, the northeast side-yard driveway and its parked
cars, the rear yard, 326 and 300 Brannan, South Park, street trees, sidewalk, parking
meters, the fire hydrant, overhead utility wires, vehicles, people, plinths, cameras or
lights

### 2.11 Triangle budget

Cap 8,500 — between 358 Brannan's 7,000 and 380 Brannan's 9,000. The massing is the
simplest on the block (one box) but the roof carries more furniture than either.
Suggested split: body and parapet ~1.2k, Brannan front (storefront, ribbon, spandrel,
number bay) ~2.2k, the two awnings ~0.8k, southwest flank and rear openings ~1.3k,
roof furniture ~2.5k, margin ~0.5k.

### 2.12 Draft manifest entry

```json
{
  "id": "318-brannan",
  "file": "318-brannan.glb",
  "anchor": [
    -122.3927890,
    37.7816014
  ],
  "targetHeightM": 8.6,
  "cat": 3,
  "name": "318 Brannan Street",
  "estimated": true,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

`dims` and `tris` are placeholders until the asset is built and validated.
`"estimated": true` because the parapet height is derived from the LiDAR roof plane
rather than published — see 2.15.

### 2.13 Integration notes (for later, not this task)

- **New landmark.** Add a `pipeline/lib/landmarks.mjs` entry (`id: '318Brannan'`,
  `exclude: 8`) and re-bake the affected tiles, or the baked procedural building on this
  footprint will intersect the GLB.
- **The exclusion radius is already measured** against the real bake input (DataSF
  `buildings_datasf.geojson` *and* Overture `overture_buildings.geojsonseq`), from this
  plan's anchor. `excluded()` in `pipeline/buildings.mjs` drops a footprint when its
  centroid **or any ring vertex** falls inside the radius:

  ```
  own DataSF ring SF3775100      centroid  0.01 m   (nearest own vertex 14.91 m)
  own Overture twin (451 m2)     centroid  4.68 m   <- the lower bound
  326 Brannan, Overture rings    vertex   10.93 m   <- the binding constraint
  326 Brannan, DataSF SF3775012  vertex   11.07 m

  exclude 5-10 m  -> drops 2 rings (correct: this building, traced twice)
  exclude 11 m    -> drops 4 (eats 326 Brannan, which has no GLB to replace it)
  ```

  **8 m** sits in the middle of the (4.68, 10.93) window. Note that this building is
  traced by *both* DataSF and Overture with centroids 4.68 m apart, so a radius under
  5 m leaves the Overture copy standing inside the GLB. Do not raise past 10 m and do
  not drop below 5 m without re-running that measurement.
- `loadRadius`: the skill's default formula gives `max(2500, 8.6 * 30) = 2500` m. Take
  the default.
- The baked procedural block here is 8.11 m (DataSF median) against an 8.6 m asset, so
  an unbaked local check will show the GLB *clashing* rather than *hidden* — unlike 358
  Brannan. Judge it only after the exclusion is applied, per the batch-mode rule.
- 318 is now the seventh Brannan Street landmark and the first that is not a
  warehouse. Judge it in the same aerial render as 350 and 358 — if it reads as another
  brick box, the mid-century character has been lost.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Bounding-box top exactly 8.6 m (loader scale lands at 1.0)
- [ ] Dimensions plausible in meters and consistent with 2.1 (XY bbox ~29.5 x 29.6 m is expected)
- [ ] Footprint proportion preserved: the building must measure 17.96 x 23.87 m along its own axes
- [ ] Triangles at or under 8,500
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the ribbon window, two storefront bays and the entrance strip; glow shells proud of the opaque surface
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (per-object signed volume for the union of solids; ray test residual <= 0.15%)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + contact sheet + night render regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

1. **The parcel is 23.64 m wide on Brannan; the building is 17.96 m. The missing 4.8 m
   is deliberately not modelled, and that is the biggest judgement call in this plan.**
   Projected onto the Brannan property line, the building occupies from 4.75 m to
   22.70 m of a 23.64 m frontage. The northeast 4.75 m is a low entry / side-yard strip
   carrying the number panel, the recessed front door and the driveway to the parking
   along the flank. Three things say it is *not* part of the two-storey mass: the DataSF
   LiDAR footprint excludes it; the aerial shows no roof at 7.8 m over it; and the
   Assessor's 9,600 sq ft building area matches 2 x 428.8 m2 (9,232 sq ft) but not
   2 x 564 m2 (12,100 sq ft). Its depth and height are genuinely unverified, so this
   plan folds its *identity* — the number panel and the recessed entrance — onto the
   northeast end of the main block's own front (2.7 step 8) rather than inventing a
   wing. **If the executing agent can verify the strip's real depth and height, model
   it, and re-derive the anchor from the combined geometry** — the bounding box would
   grow to about 33 x 29.6 m and its centre would move roughly 1.7 m northeast, which
   the manifest anchor must then follow.
2. **DataSF `hgt_maxcm` = 42.02 m is not this building.** The same record gives
   `hgt_median 8.11`, `hgt_majority 7.78`, `hgt_min 3.22`, `std 3.51` over 1,730 cells,
   and the first-return statistics (`median_1st_m 19.98`, `peak_1st_m 54.07`) are plainly
   vegetation and neighbouring structures. A 42 m maximum on a 429 m2 two-storey roof is
   scan bleed. This is the same trap 358 Brannan documented at 13.32 m, one order of
   magnitude worse. **Do not build a tower here.**
3. **The parapet height is the weakest number in this dossier.** The measured values are
   the roof plane: modal 7.78 m, median 8.11 m — and the median is inflated because the
   ducts occupy a real share of the 1,730 cells. This plan takes 7.9 m for the roof deck
   and **8.6 m for the parapet cap**, i.e. a 0.7 m parapet, which is typical for a 1961
   flat-roofed office and consistent with the Street View reading where the upper awning
   sits just below the roofline with only a thin strip of wall above it. Uncertainty is
   roughly ±0.4 m and the manifest entry is therefore `"estimated": true`. Do not attempt
   to re-derive this from a wide-angle Street View frame: the panoramas that show this
   facade are all steeply oblique (the nearest camera is 10 m from one corner and 20 m
   from the other), and a naive height/width ratio off them overstates the building by
   30-40%.
4. **Build year: 1961 or 1962.** The National Register district report says 1961; the
   Assessor says 1962 in all nineteen roll years. Both are plausible (permit vs.
   completion). Nothing in the model depends on it; state both in `REFERENCE.md`.
5. **The awning graphics change and the references disagree by date.** The THG listing
   photograph shows the ground-floor awning blank with an "AVAILABLE" sign in the window;
   the May 2025 Street View shows it lettered "ZEPHYR REAL ESTATE" with a large logo; the
   Sept 2025 flyer markets the ground floor as vacant again. The upper "KCA ENGINEERS,
   INC." awning is constant across every reference. Model the *bands*, not the lettering
   — that is what makes this asset survive the next tenant.
6. **The southwest flank's windows are the least-documented surface.** The listing's "two
   sides of windows" and the ground-floor plan's wall openings establish that this flank
   has daylight, and one interior photograph shows a frosted window on that side, but no
   reference photograph shows the flank itself. The five-window rhythm in 2.7 step 10 is
   *inferred*. Keep it restrained; an over-fenestrated flank is the failure mode.
7. **The rear has never been photographed in any source consulted.** The roll-up freight
   door is established by the listing's attribute list and by the interior photograph
   (a roll-up is visible at the rear of the open floor), but its position and width are
   *inferred*. The rear is visible from the app's aerial camera; build it as a plain
   working elevation and say in `REPORT.md` that it is inferred.
8. **The building is a non-contributor in a National Register historic district.** That
   is a fact worth keeping in the concierge's reach and worth remembering while
   modelling: it looks wrong for this block *on purpose*, and softening it toward its
   warehouse neighbours would be the one unforgivable error.
</content>
</invoke>
