# 414 Brannan Street (Epic Church) — SF-SIM asset plan

The 1924 board-formed concrete industrial block on the west corner of Brannan and
Ritch, converted in 2022–2024 into Epic Church's permanent home. In a family of
plain SoMa boxes this one is the outlier: a **red clay-tile pent roof over a
vermilion frieze band** runs the whole 24.9 m Brannan parapet and returns onto
Ritch, and a **teal arched entry portal with a fan-and-medallion tympanum** holds
the northeast end. Two finished street elevations, a slate blue-gray body, three
curved wrought-iron Juliet balconies at the southwest end of Brannan, and a raised
roof monitor over the middle third that the camera sees and the street does not.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/414-brannan/`. This document is the plan only: Part 1 is the runnable task
prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `414-brannan` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3948685, 37.7799308` |
| Target height | **14.0 m** to the crest of the raised central roof monitor; street parapet / clay-tile ridge **10.4 m** |
| Footprint | 24.90 m (Brannan frontage, SE) x 21.28 m (depth); parcel 530.0 m2, built 505.6 m2 (95% coverage), measured |
| Triangle cap | 10,000 |
| Category | `8` (place of worship) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 414 Brannan Street GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of 414 Brannan Street (Epic Church San
Francisco) and deliver it as a downloadable, validated GLB.

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
7. `artifacts/400-brannan/` — the immediate neighbour up the block and the closest
   reference implementation in scale, heading and budget (two-storey SoMa box at a
   45° heading, two finished elevations, designed flat roof, restrained night
   state). Its `build_400_brannan.py` is the script skeleton to adapt, not to
   rewrite. `artifacts/380-brannan/` is the second reference for masonry character.
8. `docs/asset-plans/414-brannan.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules.

## Must capture

- The **red clay-tile pent roof** — a projecting tiled eave running the full Brannan
  parapet and returning a short way onto Ritch — sitting on a **vermilion frieze
  band**. This is the building's whole identity from the air and the one place the
  detail budget is spent.
- The **teal arched entry portal** at the northeast end of Brannan: round arch,
  moulded surround, a cream fan tympanum with a circular medallion at its centre.
- A **corner building with two finished street elevations** meeting at a sharp 90°
  corner on the city's diagonal grid — Brannan (southeast) and Ritch (southwest).
- The **slate blue-gray monolithic body**: painted board-formed concrete, one tone
  top to bottom, no base course, no cornice other than the tile eave.
- **Tall recessed ground-floor bays** filled with frosted white glazing in a 3-part
  grid over a louvred base, separated by plain piers.
- **Punched upper windows** with dark frames and light stone sills, on a regular
  rhythm, plus **three curved wrought-iron Juliet balconies** at the southwest end
  of the Brannan elevation.
- The **raised roof monitor** over the middle bay, set back from Brannan, reaching
  14.0 m — invisible from the street, but the silhouette from the app's camera.

## Research 414 Brannan Street independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- Both street elevations (Brannan and Ritch) and, if any view exists, the rear
- Aerial and roof views (the monitor, vent layout, the tile pent from above)
- Ground-level views day and night
- The **post-renovation colour scheme**, which is the thing this dossier is most
  sure about and the thing most likely to have moved again: the building was a
  warm mid-gray with a terracotta arch in 2021 and is a slate blue-gray with a
  **teal** arch in 2025. Decide from the most recent imagery you can find and
  record the decision in `REPORT.md`.
- The bay count and window rhythm of both elevations — the Brannan upper floor is
  partly hidden behind a row of mature ficus trees in every frontal Street View
  frame, so the dossier's counts on the southwest two thirds are *inferred* from
  oblique frames.

**Three source traps are already known and resolved in 2.1 — re-check them, do not
silently re-inherit the wrong value:**

1. **OSM's `414 Brannan Street` way is the wrong building.** Way `124903643` carries
   the address tag but overlaps parcel 3776011 by only 68%; it sits over the
   southwest third of the real lot. Resolve address → EAS → parcel → footprint.
2. **The parcel carries THREE LiDAR footprints, not one.** `SF3776011` returns three
   ~180 m2 strips (`hgt_median_m` 10.32 / 13.47 / 11.19). They are three structural
   bays of ONE building on ONE parcel with ONE address — not three buildings. The
   13.47 m middle strip is the roof monitor, not a neighbour.
3. **OSM's `height=11` is a Bing-traced guess** on the wrong polygon and must not be
   the target.

## Create a reference dossier

Write `artifacts/414-brannan/REFERENCE.md` containing: source links and what each
establishes; verified dimensions and location; orientation; observations from all
four sides and above; the 3–5 strongest recognition cues; features to preserve;
features to simplify; uncertainties and conflicting evidence. Do not commit
copyrighted full-resolution imagery.

## Make your own design decisions

Follow the conversion process in `docs/styles/miniature-toy.md` §22: identify the
recognition cues, strip nonessential information, rebuild the massing from a few
confident volumes, exaggerate only the signature features, simplify the facade into
broad rhythms, deliberately design every surface visible from above, evaluate from
the app's high three-quarter aerial camera, then simplify again.

This is a **secondary building with one hero feature** in the style bible's detail
budget (§21). Its spent exaggeration is the **tile pent roof**: thickened and
given a deeper projection than reality so the red line survives at thumbnail size
and reads from directly overhead. The teal arch is the second, cheaper spend — it
is small, so it must be saturated to register.

The finished asset must be immediately recognizable as this corner, consistent with
the real building from all four sides and above, architecturally credible, and a
premium handcrafted miniature — not photorealistic, not voxel art, not generic
low-poly, and never accurate in one view while invented in the others.

## Scope of the exported asset

Export the single corner block: body, both street elevations' openings, the tile
pent roof and frieze, the arched entry, the balconies, the party and rear walls,
the roof deck, the raised monitor and the roof furniture.

Do not include unrelated surrounding city geometry: Brannan Street, Ritch Street,
the 400 Brannan block to the northeast, the 566–586 Third Street complex behind,
the row of mature ficus street trees on the Brannan kerb, traffic signals, the
sidewalk, parked cars, people, plinths, cameras or lights.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary `.glb`;
real-world meters; origin at base center; minimum geometry Z ≈ 0; applied transforms;
no negative scales; outward normals; no duplicate or foreign geometry; no image
textures; no transparency; flat-color materials named `Toy_*` from the project
palette; a `_Glow` set for the night state; no cameras, lights, animations,
armatures or constraints; ≤ 10,000 triangles; bounding-box top exactly 14.0 m.

**Two rendering traps this asset is squarely inside — read them before choosing a
colour:**

- The body colour is a slate blue-gray, and **dark bodies go black in the diorama**.
  The app has far less ambient light than the stage-2 render rig. Author the body at
  the lifted value given in 2.8 (`#8a97a8`), not at the observed photographic value,
  and confirm from the running app in stage 5 rather than from the renders.
- **Never use `Toy_roofd` on the roof deck** — it measures rgb(9,9,12) in-app.
  `Toy_steel` is the project's roof-membrane default and is what 2.8 specifies.

## Deliverables

Under `artifacts/414-brannan/`: `REFERENCE.md`, the deterministic
`build_414_brannan.py` / `render_414_brannan.py` / `validate_414_brannan.py`
scripts, `414-brannan.glb`, six review renders plus a night render, a contact
sheet, `validation.json` (all-PASS), and `REPORT.md` documenting every dossier
correction you made.

Draft manifest entry for the report (do not write it into the repo yet):

```json
{
  "id": "414-brannan",
  "file": "414-brannan.glb",
  "anchor": [
    -122.3948685,
    37.7799308
  ],
  "targetHeightM": 14.0,
  "cat": 8,
  "name": "414 Brannan Street (Epic Church)",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a separate, explicitly requested job — run `docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in `docs/asset-plans/414-brannan.md`.
````

---

## Part 2 — Research and design dossier

Compiled 18 August 2026 from the sources in 2.2. Values marked *inferred* are visual
or derived estimates, not published figures — the executing agent must re-verify
anything it relies on.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Address resolution | `414 BRANNAN ST` → parcel **3776011** (block 3776, lot 011) | DataSF EAS address layer (`ramy-di5m`) — **measured** |
| Other addresses on the parcel | **none** — 414 is the only one; parcel address range 414–414 | DataSF Parcels (`acdm-wktn`) |
| Built | **1924** | SF Assessor secured roll 2025; corroborated by FTF Engineering's project page ("Constructed in 1924 as an industrial building") |
| Structure | Unreinforced **board-formed concrete** walls, **exposed timber roof trusses** | FTF Engineering (structural engineer of record for the 2022–24 retrofit) — **measured, primary source** |
| Storeys | **3** on the assessor roll; the street elevations read as **2** (a double-height ground floor over a mezzanine) | SF Assessor (`number_of_stories = 3`); street-level photography |
| Use | Commercial Office (`COMO`), class `OCH`; fully welfare-exempt since the 2022 sale | SF Assessor roll — the exemption is the church |
| Current occupant | **Epic Church San Francisco.** Bought 4 Aug 2022 for ~$12M, renovated ~$5M by **Quezada Architecture** (19,840 sf), opened **8 Dec 2024** | SF Standard 10 Jul 2023; epicsf.com; qa-us.com; SF business registry (D04 Places of Public Assembly) |
| Earlier occupants | Lera Electric Company (trade shop, the pre-existing "general office" use), then Hattery, 1776, OnePiece Work co-working (127 desks), General Assembly | SocketSite 2017; SF business registry |
| Lot area | 5,880 sq ft (546 m2) roll / **530.0 m2 surveyed** | SF Assessor roll; DataSF parcel polygon — agree within 3% |
| Building footprint | **505.6 m2** (three LiDAR strips clipped to the parcel) — 95% lot coverage | DataSF Building Footprints (`ynuv-fyni`, `mblr = SF3776011`), reprojected — **measured** |
| Frontage / depth | **24.90 m** on Brannan x **21.28 m** deep | parcel polygon — **measured** |
| Roof deck heights | NE bay **10.32 m**, middle bay **13.47 m**, SW bay **11.19 m** above ground | DataSF LiDAR `hgt_median_m` over 761 / 718 / 704 cells — **measured** |
| LiDAR maxima | 12.84 / **14.00** / 14.09 m | `hgt_maxcm`; the middle bay's 14.00 is only +0.74σ over its own median (σ 0.72 m) and is **accepted** as the monitor crest, see 2.15 |
| Street parapet / tile ridge | **10.39 m** | independent Street View photogrammetry, 2.16 — agrees with the NE bay's LiDAR median to 0.07 m |
| Ground elevation | 5.43–6.10 m (NAVD88) | DataSF LiDAR `gnd_min_m` — the app's terrain handles this, not the asset |
| Frontage headings | Brannan front faces **135.2°** (SE); Ritch front faces **225.2°** (SW) | measured from the parcel polygon |
| OSM cross-check | way `124903643` tagged `addr:housenumber=414`, `height=11`, `source=Bing`, 184 m2 | **rejected** — 68% overlap with the parcel, wrong polygon, traced height. See 2.15 |
| Zoning | CMUO (Central SoMa – Mixed Use Office); assessor records the older SLI | DataSF Parcels |

The anchor `-122.3948685, 37.7799308` is not a choice: the parcel polygon's
axis-aligned bounding-box centre, the parcel centroid, the EAS address point and the
assessor's `the_geom` point all land within 0.02 m of each other. Three independent
layers agree, which is unusual on this block face and worth keeping.

### 2.2 Sources

- `https://data.sfgov.org/resource/ramy-di5m` (DataSF EAS Addresses) — address → parcel 3776011, single address on the lot
- `https://data.sfgov.org/resource/acdm-wktn` (DataSF Parcels) — the 530.0 m2 parallelogram, address range 414–414, CMUO zoning
- `https://data.sfgov.org/resource/ynuv-fyni` (DataSF Building Footprints, LiDAR-derived) — the three bay strips and their 10.32 / 13.47 / 11.19 m heights
- `https://data.sfgov.org/resource/wv5m-vpq2` (SF Assessor Historical Secured Property Tax Rolls) — 1924, 3 storeys, 19,548 sq ft, welfare exemption, 4 Aug 2022 sale
- `https://ftfengineering.com/portfolio_page/epic-church/` — **the best single source**: 1924 industrial building, 19,840 sf, ASCE 41 seismic retrofit, board-formed concrete preserved, original wood roof structure on timber trusses kept exposed, added concrete shear walls "on the blind sides of the building, maintaining all existing openings"
- `https://qa-us.com/project/epic-church` (Quezada Architecture) — the renovation programme: 300-person assembly, Sunday school, bike/stroller parking, baptismal pool, café
- `https://sfstandard.com/2023/07/10/epic-church-bets-on-a-better-future-for-soma/` — ~$12M purchase, ~$5M renovation, a floor dedicated to youth programming
- `https://socketsite.com/archives/2017/05/popular-coworking-space-could-be-shut-down-others-at-risk.html` — the Lera Electric Company legacy use and the OnePiece Work co-working history
- `https://www.epicsf.com/from-pastor-ben/get-inside-the-story` — purchase 4 Aug 2022, building opened 8 Dec 2024
- Google Street View, pano `zPv7IB2PjEsWarb0iZ412A` (2021, Brannan looking NW) — the near-orthogonal frontal elevation used for the photogrammetry in 2.16, and the pre-renovation colour scheme
- Google Street View, panos `7K6Zh27rKJrFXkI8GmGICw` and `moQcOx7ROM7r7vcRJw04_g` (2025, Brannan) — the current teal arch and slate body
- Google Street View, pano `Ow9JzQw5-zEmgIHf_Qk3zw` (2025, Brannan/Ritch corner) — the oblique that shows the three Juliet balconies the ficus trees hide from the front
- Google Street View, panos `auyEb77HUzoro0gQF5UIYg` and `SAz7nIhGlLCIhM4mORH_HQ` (Ritch Street) — the southwest elevation, the stepped parapet and the tile return
- Google satellite tiles `https://mt1.google.com/vt/lyrs=s&z=21` stitched over the parcel and footprint rings — the roof, the tile pent seen from above, and the ficus canopy that covers the southeast corner of the lot

### 2.3 Orientation and placement

The building holds the **west corner of Brannan and Ritch**. Ritch Street's
centreline is 6.3 m from the parcel boundary (OSM), so the southwest side is a
**street elevation, not a party wall** — that is the single biggest difference
between this asset and its Brannan siblings, and the reason for the raised triangle
budget.

Measured parcel polygon, in Blender coordinates (metres, `+X` east, `+Y` north),
already centred on the anchor `-122.3948685, 37.7799308`:

```
(  16.353,   1.237)   E corner  — Brannan frontage, northeast end (party wall with 400 Brannan)
(   1.325,  16.306)   N corner  — rear, northeast end
( -16.353,  -1.237)   W corner  — rear, southwest end (Ritch)
(  -1.325, -16.306)   S corner  — the Brannan / Ritch street corner
```

A true parallelogram, four vertices, no jogs. Build on it directly; the LiDAR strips
spill ~1 m past its northeast edge and should be clipped back to the parcel, not
followed.

Edges, with outward normals:

| Edge | Length | Faces | Elevation |
|---|---|---|---|
| S→E | 24.90 m | SE 135.2° | **Brannan Street front** |
| E→N | 21.28 m | NE 45.2° | party wall against 400 Brannan |
| N→W | 24.90 m | NW 315.2° | rear, block interior (566–586 Third behind) |
| W→S | 21.28 m | SW 225.2° | **Ritch Street front** |

Because of the 45° heading the axis-aligned bounding box is ~32.7 x 32.6 m. That is
correct and expected — compare 400 Brannan's ~31 x 33 m.

The three structural bays run **perpendicular to Brannan**, each ~8.3 m of frontage
by the full 21.28 m depth. Their centres, in the same Blender coordinates:

| Bay | Centre | LiDAR deck | Role |
|---|---|---|---|
| NE | ( 5.08,  5.99) | 10.32 m | the arched entry, lobby / café; low the whole way back |
| Middle | (-1.15, -0.08) | **13.47 m** | the sanctuary; the raised roof monitor |
| SW | (-7.28, -5.73) | 11.19 m | Ritch side; steps up toward the rear (`hgt_max` 14.09 m) |

### 2.4 What each side shows

**Southeast (Brannan Street), 24.90 m** — The primary elevation. Top to bottom: a
**projecting clay-tile pent roof** in barrel tile, running the full width with a
visible eave overhang; below it a **vermilion frieze band** roughly 1.1 m tall,
flush with the wall; then the slate blue-gray field. The **upper floor** carries
punched rectangular windows on a regular rhythm — charcoal frames, a large upper
light over a two-light lower row, light stone sills. Toward the **southwest third**
three of those upper windows have **curved wrought-iron Juliet balconies** bellying
out over the sidewalk (invisible in every frontal Street View frame because a row of
mature ficus stands in front of them; clearly visible in the oblique from the Ritch
corner). The **ground floor** is tall — its openings head at 4.58 m — and is
composed as deep recessed bays: a dark bronze frame around a 3-part **frosted white
glazed panel**, with a **louvred grille** across the base of each bay, separated by
plain slate piers. Toward the southwest the bays give way to large flat **recessed
blank panels** with no glazing at all. At the **northeast end**, the **teal arched
entry**: a round arch with a moulded surround and base plinths, a cream fan
tympanum carrying a circular medallion at its centre, and a recessed dark doorway
behind a diamond-lattice security gate. There is **no base course and no cornice** —
the concrete runs from sidewalk to frieze in one plane, which is exactly what makes
the red band read.

**Southwest (Ritch Street), 21.28 m** — A real elevation, quieter than Brannan. The
tile pent **returns around the corner** for a short run and then the parapet
**steps up** toward the rear in two stages, the rearmost being the tallest part of
the Ritch wall. Along it: a rhythm of small punched upper windows (steel sash, white
lights), a **round medallion or plaque** set high on the wall, one more curved iron
balcony at the Brannan end, the **Epic Church sign** (a dark navy panel with a gold
mark) beside a frosted storefront window, and at ground level **two roll-up doors**
— a wide grey one toward the rear and a lighter one near the corner — plus a large
**louvred vent grille**. Same slate body, same charcoal frames.

**Northeast (party wall with 400 Brannan)** — Blank. The two buildings share the
line; nothing of this face is visible from any street. Build it as a finished, quiet
wall plane. It IS visible from the app's aerial camera, so no invented window grid,
but no holes either.

**Northwest (rear)** — Blank painted concrete against the interior of block 3776 and
the 566–586 Third Street complex behind. Same treatment as the party wall.

**Top** — Three flat membrane decks at 10.32 / 13.47 / 11.19 m, with the middle
bay's **raised monitor** dominating: a full-bay-width volume, set back from the
Brannan parapet, its crest at 14.0 m. Nadir imagery shows a light membrane, a
scatter of small vents and units, and one squarish skylight-sized element; the large
dark blob over the southeast corner of the lot is the ficus canopy, not a roof
feature. The **tile pent is visible from directly overhead** as a red line along the
Brannan edge — from the app's camera it is the single most identifying thing about
this building, which is why it gets the exaggeration budget.

### 2.5 Recognition cues (ranked)

1. **The red clay-tile pent roof over a vermilion frieze**, running the full Brannan
   parapet and returning onto Ritch — a red line on a slate box, legible from
   directly above
2. The **teal arched entry** with its cream fan-and-medallion tympanum
3. The **slate blue-gray monolithic body** — no base, no cornice, one tone
4. The **corner condition**: two finished elevations at a sharp 90° on the diagonal grid
5. The **three curved iron Juliet balconies** at the southwest end of Brannan
6. The **raised roof monitor** over the middle third

### 2.6 Miniature translation

**Preserve**

- The single-volume box, the real 45° heading, the true parallelogram footprint
- The tile pent + frieze as one continuous two-tone red band, mitred round the corner
- The teal arch's position hard against the northeast party wall
- The tall-ground-floor / short-upper-floor proportion (4.58 m head vs 2.35 m windows)
- The monitor's setback — it must not touch the Brannan parapet

**Simplify / exaggerate**

- The tile pent is **thickened and deepened**: ~0.5 m projection and ~0.45 m tall,
  its barrel profile implied by a ribbed strip rather than modelled tile by tile.
  This is the one place semantic exaggeration is spent.
- The upper window rhythm becomes 7 bays on Brannan (3 of them balconied at the
  southwest end) and 5 on Ritch
- The ground floor becomes 4 glazed recessed bays at the northeast end of Brannan
  and 2 blank recessed panels at the southwest end; on Ritch, one roll-up door, one
  frosted window, one louvred panel
- The arch keeps its surround, its fan and its medallion, and loses its mouldings,
  its plinths and its lattice gate
- The Juliet balconies become simple half-cylinder rails — three arcs, no ironwork
  pattern
- The Epic Church sign, the wall medallion, gooseneck lamps, downpipes, meters and
  signage lettering all disappear
- The roof scatter becomes three small units, one hatch and one skylight

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not a
straitjacket — adjust after the first aerial review render.

1. Body: extrude the 2.3 parcel polygon from z=0 to z=9.95, `Toy_slate`.
2. Frieze band: the top 1.10 m of the Brannan and Ritch faces, z=8.85 to z=9.95,
   `Toy_ioorange`, flush with the wall (a material change, not a projection).
3. Parapet + tile pent: from z=9.95 to **z=10.39**, following the footprint,
   0.35 m thick, `Toy_slate`; on the Brannan and Ritch edges cap it with a
   `Toy_brick` tiled pent projecting 0.50 m outboard and 0.10 m above the parapet,
   its underside at z=9.95, four shallow ribs implying barrel tile. Mitre the
   corner; end the Ritch return 6 m from the corner.
4. Roof decks at z=10.32 (NE bay) and z=11.19 (SW bay), `Toy_steel`, each inside its
   own share of the parapet ring.
5. **Roof monitor**: over the middle bay only, inset 6.0 m from the Brannan parapet
   and running to the rear wall, 8.3 m wide. Walls `Toy_slate` from z=10.0 to
   z=13.55; deck `Toy_steel` at z=13.55; a `Toy_stone` coping z=13.55 to **z=14.0**
   — this sets the bounding-box top and must land exactly on 14.0. Give its long
   sides a band of four small `Toy_glass` clerestory lights: it is a daylight
   monitor over a sanctuary, and that is what the timber trusses are lit by.
6. Ground floor, z=0 to z=4.58, Brannan: four recessed bays at the northeast end,
   inset 0.22 m, `Toy_ink` frame around a `Toy_trim` 3-part panel with a
   `Toy_roofd` louvre band in the bottom 0.55 m; two blank recessed panels at the
   southwest end, inset 0.14 m, `Toy_slate`. Piers 0.55 m, `Toy_slate`.
7. Ground floor, Ritch: one 3.6 m `Toy_stone` roll-up door, one frosted bay as
   above, one blank recessed panel, one louvred panel.
8. Upper floor, z=5.75 to z=8.10: 7 openings on Brannan and 5 on Ritch, 1.55 x 2.35 m,
   recessed 0.18 m, `Toy_glass` fill with `Toy_ink` frames and a `Toy_stone` sill
   projecting 0.06 m. On the three southwest-most Brannan openings, add a
   half-cylinder `Toy_ink` balcony rail, radius 0.55 m, 0.95 m tall, floor at z=5.70.
9. Arched entry, Brannan, centred 3.4 m from the northeast corner: a 2.6 m wide
   `Toy_teal` surround 0.16 m proud of the wall, springing at z=3.35, arch crown at
   z=4.70; a `Toy_trim` fan in the tympanum with a `Toy_gold` medallion disc 0.55 m
   across; a `Toy_ink` recessed door 1.9 x 3.2 m.
10. Bevel 0.12 m, 2 segments on the chunky solids; 0.05 m / 1 segment on window
    frames and the tile ribs; none on fills and glow shells.

### 2.8 Materials and palette

Flat colors only. One deliberate off-palette colour, justified below.

| Material | Hex | Used for |
|---|---|---|
| `Toy_slate` | `#8a97a8` | body, parapet, piers, monitor walls, blank recessed panels |
| `Toy_ioorange` | `#c0402a` | the frieze band |
| `Toy_brick` | `#c96f4a` | the clay-tile pent roof |
| `Toy_teal` | `#3fa8a0` | the arched entry surround |
| `Toy_trim` | `#f3efe6` | frosted glazed panels, the arch fan |
| `Toy_gold` | `#caa64a` | the medallion in the tympanum |
| `Toy_ink` | `#3a3530` | window frames, bay frames, balcony rails, the recessed door |
| `Toy_glass` | `#2a4d73` | upper-window glazing, monitor clerestory |
| `Toy_stone` | `#d9d2c2` | sills, the monitor coping, the Ritch roll-up door |
| `Toy_steel` | `#9aa0a6` | roof decks and membranes |
| `Toy_roofd` | `#45454a` | louvre bands and small roof props only |
| `Toy_trim_Glow` | `#f3efe6` | the frosted ground-floor bays at night (hero) |
| `Toy_glass_Glow` | `#6f95b8` | three or four lit upper windows, and the monitor clerestory |
| `Toy_gold_Glow` | `#caa64a` | the tympanum medallion |

**On `Toy_slate` being off-palette.** The building's identity is that it is the one
blue-gray box on a block of cream and white ones; there is no blue-gray in the
project palette, and off-palette is a WARN, not a fail. The hex is *not* the observed
value. Street View measures the sunlit wall at `#b0b7bd` and the shadowed wall at
`#6a798b`; `#8a97a8` sits between them and, critically, has a relative luminance of
~149 against `Toy_roofd`'s ~69. `Toy_roofd` measures **rgb(9,9,12)** on a real roof
deck in the running app, and `108-south-park` shipped only after its body was lifted
~3x to `#587a66` (luminance ~113) for exactly this reason. `#8a97a8` is above both
and sits beside `Toy_steel` (~159), which measures rgb(94,105,111) in-app. Do not
darken it toward the photograph without re-checking in the app.

**Night state (required).** Glow surfaces must be thin shells proud of the opaque
fills — the app renders `_Glow` in a separate layer, and because the shells are
closed solids a ray crosses two faces, so the *day* opacity is ~23%, not the 12% the
app applies. Keep the shells small and desaturated. Hero glow: the **frosted
ground-floor bays** on Brannan — they are translucent panels in daylight and read as
lit boxes at night, and this is a building whose ground floor is a café and lobby.
Supporting accents: three or four upper windows (never the whole rhythm), the
**monitor clerestory** (a lit sanctuary seen only from the air — the payoff for
modelling the monitor at all), and the **tympanum medallion**. Cover only the lower
two thirds of each frosted bay; a full-height shell will tint the whole ground floor
in the day pass. When copying `render_400_brannan.py`, add
`bsdf.inputs["Emission Strength"].default_value = 0.0` to `fade_glow()` — the
inherited version only drops Alpha and washes a wide shell to flat pale grey in the
day render.

### 2.9 Top surface

A 506 m2 roof only 10–14 m up, in the district the camera flies over most. Three
things have to read from directly overhead:

1. The **red tile line** along the Brannan edge, returning onto Ritch. Give it enough
   projection and enough saturation that it survives at 40 px.
2. The **monitor** as a distinct raised volume with its own coping — keep the coping
   in `Toy_stone` so the ring separates from the `Toy_steel` deck below it.
3. The **height step** between the three bays. The NE bay is 0.9 m below the SW bay;
   that is small but it is real, and flattening it loses the only asymmetry the roof
   has.

Group the mechanical units on the NE bay's deck toward the rear and leave the
Brannan third of every deck clean — the real roof is empty there.

### 2.10 Scope

**In the GLB:** the single corner block — body, both street elevations, the tile
pent and frieze, the arch, the balconies, party and rear walls, three roof decks,
the monitor and the roof furniture

**Not in the GLB:** Brannan Street, Ritch Street, 400 Brannan, the 566–586 Third
complex behind, the ficus street trees, traffic signals, sidewalk, vehicles, people,
plinths, cameras or lights

### 2.11 Triangle budget

Cap 10,000 — higher than 400 Brannan's 8,000 because this asset has two finished
street elevations, an arched entry, three curved balconies, a ribbed tile pent on
two faces and a separate roof monitor. Suggested split: body, parapet and monitor
~2.0k, tile pent and frieze ~1.2k, upper window bays (12) ~2.5k, ground-floor bays
and louvres ~2.0k, arch ~0.9k, balconies (3) ~0.6k, roof furniture ~0.8k.

### 2.12 Draft manifest entry

```json
{
  "id": "414-brannan",
  "file": "414-brannan.glb",
  "anchor": [
    -122.3948685,
    37.7799308
  ],
  "targetHeightM": 14.0,
  "cat": 8,
  "name": "414 Brannan Street (Epic Church)",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

`dims` and `tris` are placeholders until the asset is built and validated.
`loadRadius`: the default rule gives `max(2500, 14.0 × 30) = 2500` m. Take the default.

### 2.13 Integration notes (for later, not this task)

- **New landmark (Case B).** Add a `pipeline/lib/landmarks.mjs` entry
  (`id: '414Brannan'` — `camelId()` in `app/src/assets.js` is
  `id.replace(/-([a-z])/g, upper)`, and digits do not start a segment, so
  `414-brannan` → `414Brannan`), `lon`/`lat` as above, `height: 14`, and re-bake the
  affected tiles, or the three baked procedural bays on this exact footprint will
  intersect the GLB.
- **Exclusion radius: 12 m, and the safe band is unusually wide.** Measured against
  the DataSF footprint layer at the anchor (`excluded()` in `pipeline/buildings.mjs`
  tests the centroid *and* every ring vertex):

  ```
  exclude  6-8 m  -> drops 2  (the middle bay + one Overture ring)
  exclude 10 m    -> drops 4  (two bays)
  exclude 11-13 m -> drops 6  (correct: all three bays + all three Overture rings,
                               zero collateral)
  exclude 14 m    -> drops 8  (eats 566-586 Third, SF3776008, nearest vertex 13.73 m)
  exclude 16 m    -> drops 10 (eats 400 Brannan / 590 Third, SF3776114, vertex 15.78 m)
  ```

  Measured at stage 5 against the real bake input, both sources — the numbers
  hold across DataSF and the Overture gap-fill, which carries three more rings
  over the same lot. The band is wide because all three of this building's own
  centroids sit within 10.71 m of the anchor while the nearest neighbour *vertex*
  is 13.73 m away — the centroid test does the work and the radius never has to
  reach this building's own ring (its corners are 16.4 m out). **12 m is the
  middle of the band, and that is what shipped.**
- 400 Brannan's shipped `exclude: 11` was sized in the knowledge that 16 m would eat
  this building (see its registry comment). Nothing there needs to change; check
  after the re-bake that neither exclusion has grown into the other's site.
- This is the **ninth** asset in the Brannan family and the third on this block face
  (with `400-brannan` and `574-third`). Batch mode applies — see the pipeline doc's
  "Batch mode" section.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Bounding-box top exactly 14.0 m (loader scale lands at 1.0)
- [ ] Dimensions plausible in meters and consistent with 2.1 (XY bbox ~32.7 x 32.6 m is expected)
- [ ] Triangles at or under 10,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `Toy_roofd` used only on louvres and small props — **never on a roof deck**
- [ ] Body luminance checked against the app, not the render rig (2.8)
- [ ] `_Glow` only on the frosted bays, a few upper windows, the clerestory and the medallion; shells proud of the opaque fills and covering only part of each opening
- [ ] `fade_glow()` zeroes Emission Strength as well as Alpha
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (per-object signed volume for the union of solids; ray test residual ≤ 0.15%)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + contact sheet + night render regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

- **The OSM way tagged "414 Brannan Street" is the wrong polygon.** Way `124903643`
  carries the address but overlaps parcel 3776011 by 68% and sits over the southwest
  third of the lot; OSM has split this single building into several unaddressed ways
  and hung the number on one of them. Its `height=11` is a Bing trace of that wrong
  polygon. This is the mirror image of 400 Brannan's failure (an address with no
  parcel) and of the 350 Brannan failure (a geocoder returning a roadway): resolve
  address → EAS → parcel → footprint, every time.
- **Three LiDAR footprints, one building.** `mblr = SF3776011` returns three strips.
  They are structural bays of one 1924 concrete building on one lot with one address
  and one assessor record, and all three have to be excluded at integration or the
  GLB shares its site with a procedural triplet.
- **The 13.47 m middle bay is the weakest link in the height chain.** It is
  supported by two independent readings — a LiDAR median over 718 cells (so more
  than half that bay's area really is at 13.47 m, not an outlier) and a Street View
  measurement of a raised mass spanning the middle 8.45 m of the frontage with its
  top at 13.0–14.1 m depending on assumed setback. What is *not* established is its
  shape: monitor, stair penthouse, or a plain raised block. The plan models a
  daylight monitor because the building has exposed timber trusses over a sanctuary
  and that is what such a roof is normally lit by, but this is *inferred*. Aerial
  imagery at a better angle would settle it, and if it turns out to be a plain box,
  drop the clerestory and keep the massing.
- **The colour scheme changed with the renovation and may change again.** 2021:
  warm mid-gray body (`#9ea19b` sunlit), terracotta arch. 2025: slate blue-gray body,
  **teal** arch. The frieze and tile stayed red through both. Model the 2025 state
  and re-check for anything newer.
- **The southwest two thirds of the Brannan upper floor is inferred.** A row of
  mature ficus stands directly in front of it in every frontal frame; the three
  Juliet balconies are read from a single oblique at the Ritch corner, and the
  7-bay rhythm is a reconstruction from that oblique plus the Ritch elevation's
  spacing. It is the weakest number in this dossier.
- **The assessor says 3 storeys and the street says 2.** 19,548 sq ft of property
  area over a 5,880 sq ft lot with a 5,852 sq ft basement is consistent with a
  double-height ground floor plus a mezzanine plus an upper floor. The exterior only
  ever shows two window lines, which is what the model builds; the discrepancy is
  interior and does not affect the asset.
- **The whole building is a nonprofit's home, freshly renovated, with permits still
  open** (a $3.0M Quezada alterations permit and a $1.1M Gary Bell permit were open
  as of the last permit scrape). Rooftop equipment in particular may have moved
  since the 2010 LiDAR.
- **Batch:** this asset is being built alongside its Brannan siblings. Stage 5 must
  run in batch mode (source-only branch, bake discarded) or the tile re-bakes will
  collide.

### 2.16 Photogrammetric height measurement

Independent of the LiDAR, using the method in the repo's Street View recipe on pano
`zPv7IB2PjEsWarb0iZ412A` (Brannan, 2021), rendered at `pitch=0`, `thumbfov=90`,
1024 x 640, so `f = 512 px` and the facade is parallel to the image plane.

**Solving the camera distance.** The pano's own reported position puts the lens
15.78 m from the facade plane. That is not used. Both ends of the 24.90 m frontage
are visible — the Ritch corner at image `x = 155`, the 400 Brannan party line at
`x = 862` — which gives two equations in the perpendicular distance `D` and the
along-facade offset `s`:

```
tan(atan((155-512)/512)) = (-12.45 - s)/D
tan(atan((862-512)/512)) = ( 12.45 - s)/D
=>  D = 18.03 m,  s = 0.12 m
```

a 2.25 m disagreement with the pano's own metadata, in the direction that recipe
warns about.

**Heights.** For a facade parallel to the image plane the horizontal position drops
out entirely and `h = D · (y_ground − y)/f`, anchored on the ground line at
`y = 396.7` so the camera height never enters:

| Feature | image `y` | height |
|---|---|---|
| clay-tile ridge (crest of the street parapet) | 101.7 | **10.39 m** |
| underside of the frieze band | 135 | 9.22 m |
| head of the upper windows | 166.7 | 8.10 m |
| sill of the upper windows | 233.3 | 5.75 m |
| head of the ground-floor bays | 266.7 | 4.58 m |
| ground | 396.7 | 0 |

The 10.39 m tile ridge agrees with the northeast bay's LiDAR median of 10.32 m to
0.07 m, which is what licenses the rest of the table as the facade's dimension set.
The raised mass behind the parapet measures 8.45 m wide, centred 0.3 m southwest of
the facade centre — i.e. the middle bay — with its top between 13.0 m (assuming it
stands in the facade plane) and 14.1 m (assuming a 2 m setback). The 14.0 m target
takes the LiDAR maximum, which sits inside that range.
