# 35 South Park (Accel) — SF-SIM asset plan

A 1920 industrial building on the north-east arc of the South Park oval, wearing the
**grandest street elevation on the park**: five giant round-arched bays in smooth
ashlar cast stone, plain roundels in the spandrels, a rope-enriched cornice, a
lettered frieze whose raised letters have been stripped back to ghosts, and a tall
blank parapet. Behind it the building is a plain 22.7 × 35.8 m box, and since a
ground-up renovation completed in 2023 it carries two things no neighbour has: a
**continuous clipped hedge running the full length of the parapet** and a **set-back
penthouse** behind it. It is Accel's San Francisco office.

The design brief is the opposite of `135-south-park`: here the **street elevation is
the identity**, and it is the one elevation on this row that a miniature can carry with
pure geometry — five arches, five roundels, one cornice band. The roof still has to be
designed, because the camera looks down, and the roof has an unusually good answer: a
green line.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/35-south-park/`. This document is the plan only: Part 1 is the runnable task
prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `35-south-park` |
| Registry id | `35SouthPark` (`camelId()` in `app/src/assets.js` maps one to the other) |
| Existing procedural builder | none — new landmark (**Case B**: needs a `pipeline/lib/landmarks.mjs` entry and a tile re-bake, see 2.13) |
| WGS84 anchor | `-122.3933378, 37.7815714` (oriented-bounding-box centre, measured from OSM way `112759864`) |
| Target height | **13.4 m** to the penthouse crest — *estimated*, photogrammetric; front parapet crest **10.4 m**, roof-hedge crest **11.3 m**, cornice 7.9 m. Read 2.15 risk 1 before using any of these |
| Footprint | 22.72 m frontage on South Park (NW) × 35.80 m deep, 791.2 m², one 7.96 × 2.44 m notch out of the rear south-west corner; measured |
| Axis-aligned XY bbox | 41.31 × 39.55 m — expected, not a scale error: the SoMa grid puts this building at 45.5° to the world axes |
| Triangle cap | 9,000 |
| Category | `3` (office) — the assessor still classes it Industrial, see 2.1 |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 35 South Park GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of **35 South Park** in San Francisco (the Accel
office, on the north-east arc of the South Park oval) and deliver it as a downloadable,
validated GLB.

Do not integrate or deploy the model yet. Create the asset, validate it, render review
images, and commit the deliverables to your working branch.

## Read the project sources first

Before any research or modeling, read in this order:

1. `AGENTS.md`
2. `docs/styles/README.md`
3. `docs/styles/miniature-toy.md`
4. `.agents/skills/sf-miniature-style/SKILL.md`
5. `.agents/skills/sf-asset-check/SKILL.md`
6. `app/public/sf-assets/landmarks_manifest.json`
7. `artifacts/2-south-park/` — the closest reference implementation: the other
   monumental masonry warehouse on this oval, same era, same 45° heading, same
   "one strong order carried across a plain box" brief.
8. `artifacts/168-south-park/` and `artifacts/181-south-park/` — the nearest
   neighbours in palette and bevel terms. This asset has to look like it came out of
   the same toy box as the eighteen South Park landmarks already shipped.
9. `docs/asset-plans/35-south-park.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification.

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules.

## Read 2.15 before you start

This dossier is **asymmetric in the opposite direction from most of the set**: the
street elevation is photographically confirmed in detail, and the **heights are the
weak part** — the DataSF LiDAR is from 2010 and this building grew a penthouse level
between 2020 and 2023. Section 2.15 risk 1 says exactly what is measured, what is
photogrammetric and what is assumed. **The target height is the number the loader
divides by. Settle it before you export.**

## Must capture

1. **Five giant round-arched bays** across the 22.72 m north-west frontage, in smooth
   pale ashlar. This is the recognition cue and the reason to build the asset.
2. **A plain circular roundel** in each spandrel between the arches — five of them,
   one per pier, sitting just under the cornice.
3. **The cornice band with its rope/cable enrichment**, then the plain lettered frieze,
   then a **tall blank parapet** above it. The parapet is roughly as deep as the
   frieze; do not shrink it to a coping.
4. **The continuous clipped hedge running the full length of the parapet** — a green
   line on top of a pale wall. The single most distinctive thing about this roof.
5. **The set-back penthouse** behind the hedge, on the south-west half of the roof,
   with its band of roof lights.
6. A dark recessed opening in the end bay at each end of the frontage — a
   service/garage opening at the north-east end, the main entrance at the south-west.
7. The **blank south-west party wall** shared with 41–43 South Park: no openings at all.

## Research 35 South Park independently

Verify the dossier rather than trusting it. Re-check at minimum the architectural
height, the footprint, the WGS84 anchor and the real-world orientation, and gather
references covering:

- **The penthouse crest.** 2.15 risk 1. The 2010 LiDAR maximum (12.44 m) predates the
  penthouse; the 13.4 m in this plan is a photogrammetric estimate whose largest error
  term is the penthouse's setback from the front parapet, which was estimated from a
  nadir aerial. A tilted aerial (Google 45°/3D, Bing Bird's Eye, Apple Flyover) or a
  more recent LiDAR product settles it in one look. **If you settle it, say so in
  REPORT.md and change the constant.**
- **The bay count.** Five is counted off the Jan 2025 Street View captures listed in
  2.2 through winter foliage. Confirm it.
- **The frieze inscription.** The raised letters have been removed and only their
  shadows remain; "C…O…O" is as much as the 2025 capture resolves. An older Street
  View capture (use "See more dates" — coverage goes back to ~2007, i.e. before the
  2020–23 renovation) may show the letters still in place, and would also show what the
  building looked like before the hedge and penthouse arrived.
- The rear (south-east) and north-east elevations, which nothing consulted shows.
- Day and night appearance. The night state matters here (2.8).

Prefer architect/owner publications, permitting records, geolocated photography and
aerial imagery. Separate verified facts from visual inference; if sources disagree,
document the disagreement and decide. Record every correction prominently in
`REFERENCE.md` and `REPORT.md`. **REPORT beats plan, always.**

## Create a reference dossier

Write `artifacts/35-south-park/REFERENCE.md` containing: source links and what each
establishes; verified dimensions and location; orientation; observations from all four
sides and above; the recognition cues; features to preserve; features to simplify;
uncertainties and conflicting evidence; and every correction made to this plan. Be
explicit about which height statements you confirmed and which you inherited.

## Make your own design decisions

Follow the conversion process in `docs/styles/miniature-toy.md` §22. This is a
**secondary building** in the style bible's detail budget (§21) with one hero move:
the arcade. Spend the exaggeration budget on the arches and the roundels, keep
everything else quiet, and design the roof.

What is NOT negotiable: the measured footprint and heading, the style bible, the asset
contract, and a designed night state.

## Scope of the exported asset

**In:** the single building — masonry shell on the measured footprint including the
rear notch, the five-bay arcade, roundels, cornice, frieze, parapet, roof deck, roof
hedge, penthouse and roof furniture, the two end openings, and the wall sconces if
they survive simplification.

**Out:** South Park (the street or the park), 27 South Park, 41–43 South Park, the rear
courtyard and its cars, street trees, the sidewalk, vehicles, people, plinths, cameras
or lights. Temporary context may appear in review renders but must not leak into the GLB.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary `.glb`;
real-world metres; origin at base centre; minimum geometry Z ≈ 0; applied transforms;
no negative scales; outward normals; no duplicate or foreign geometry; no image
textures; no transparency; flat-colour materials named `Toy_*` from the project
palette; `_Glow` suffix only on surfaces that glow at night; no `Toy_body`; no cameras,
lights, animations, armatures or constraints; at most **9,000** triangles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model drops
into the city at its real-world heading — the loader applies no rotation
(`placeGeneric` in `app/src/assets.js` only scales and positions). The South Park front
faces **north-west, outward bearing 315.9°**. Build directly on the measured footprint
polygon in 2.3; do not model an axis-aligned box and rotate it. Record the measured
heading in `REPORT.md`.

**Height normalization:** the tallest geometry in the export (the penthouse) must land
at exactly the verified crest so the loader's `targetHeightM / measuredHeight` scale is
1.0. Drive it from a single named constant so a corrected height is a one-line change.

## Reproducible Blender workflow

Blender 5.2 LTS, headless: `blender -b --python script.py -- args`.

Keep `artifacts/35-south-park/build_35_south_park.py` (deterministic build script),
`artifacts/35-south-park/35-south-park.blend` and
`artifacts/35-south-park/35-south-park.glb`. No interactive modelling, no random
numbers.

## Required review renders

`35-south-park-top.png`, `-north.png`, `-east.png`, `-south.png`, `-west.png`, plus
`-front.png` (a true elevation of the north-west arcade — the four compass elevations
each show two faces at 45° on this heading, which is correct and useless for judging
the one elevation that carries the design), `-contact-sheet.png`, at least one high
three-quarter aerial `-aerial.png`, and a night render `-aerial-night.png`.

The elevations must share scale, framing, lighting, exposure and projection; use
orthographic or long-lens cameras; label directions from the researched orientation.
**Review the aerial first and iterate on it**, then run the formal rig.

## Validate the exported GLB

Re-import `35-south-park.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY centre offset, material names, image-texture count,
camera count, light count, animation count, applied-transform status, negative-scale
status, normal-orientation status (per-object signed volume authoritative for the union
of solids; whole-model ray residual ≤ 0.15%), unexpected geometry, and per-material
contract compliance. Write `artifacts/35-south-park/validation.json` and
`artifacts/35-south-park/REPORT.md`.

Note that the axis-aligned XY bounding box will be roughly **41.3 × 39.6 m** even though
the building is 22.7 m wide and 35.8 m deep — that is the expected consequence of a
45.5° real-world heading, not a scale error.

## Manifest draft

Verify the anchor and architectural height yourself, then include the entry from 2.12
in `REPORT.md` with the measured `dims` and `tris` filled in. Do not edit
`app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or any
app code in this task — integration is a separate job
(`docs/asset-plans/INTEGRATION-PROMPT.md` plus 2.13 below).
````

---

## Part 2 — Research and design dossier

Compiled 16 August 2026 from the sources in 2.2. Values marked *inferred* or
*estimated* are visual or derived, not published figures.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Address | 35 South Park (OSM records the street as "South Park", not "S Park St"). Google Maps labels the frontage **33 S Park St** | OSM way/112759864 `addr:*`; Google Maps — **conflict recorded, see 2.15** |
| Block / lot (APN) | **3775 / 102** | DataSF footprint `mblr = SF3775102`, matched to the OSM ring (centroids 1.4 m apart); SF Assessor roll block 3775 lot 102 |
| Built | **1920** | SF Assessor secured roll, identical across all 19 rows 2007–2025 — **verified** |
| Storeys | **3** (assessor) | SF Assessor roll (`number_of_stories = 3.0`, every year 2007–2025). Building permits record 2 existing storeys until 2020 and 3 from 2021 — **conflict, see 2.15** |
| Assessor use class | Industrial | SF Assessor roll (`use_definition`, `property_class_code_definition`) |
| Building area | **16,420 sq ft** (1,525 m²) on a **8,197 sq ft** (761 m²) lot — a FAR of exactly 2.0 | SF Assessor roll, constant 2007–2025 — **verified** |
| Current tenant | **Accel** (venture capital), San Francisco office | `accel.com/contact-us` lists "35 South Park Street, San Francisco, CA 94107"; OSM node 11020498922 `name=Accel` at housenumber 35 — **verified** |
| Interior renovation | Perkins&Will, "South Park Venture Capital Firm", **16,420 sq ft, completed 2023**, client confidential; brick-clad 1920s building, double-height "birdcage" vestibule, split-flap sign, "large, arched metal-clad windows" | perkinswill.com project page; officesnapshots — **the project is verified; its identification with THIS building is *inferred*, see 2.15** |
| Footprint | **791.2 m²**, 8 vertices; 22.72 m frontage (NW) × 35.80 m deep; one 7.96 × 2.44 m notch out of the rear south-west corner | OSM way/112759864 geometry via Overpass, reprojected — **measured** |
| DataSF footprint (cross-check) | 750.4 m², centroid 1.36 m from the OSM anchor | DataSF Building Footprints `SF3775102` — agrees on position and shape |
| Anchor (OBB centre) | **−122.3933378, 37.7815714** | **measured**; the polygon area centroid is −122.3933395, 37.7815750, 0.42 m away |
| Frontage heading | South Park front faces **315.9° (NW)**; NE flank outward 45.5°; rear 135.8° (SE); SW party wall 225.5° | measured from the footprint polygon |
| Roof deck height | **10.87 m** (`hgt_majoritycm`), median 10.49 m | DataSF LiDAR (2010) — **measured, but pre-dates the penthouse** |
| Maximum feature height (2010) | **12.44 m** (`hgt_maxcm`) | DataSF LiDAR (2010) — **measured, pre-penthouse** |
| Ground elevation | 11.71 m NAVD88 (`gnd_min_m`); range 11.71–12.55 m | DataSF LiDAR — the app's terrain handles this, not the asset |
| Front parapet crest | **10.4 m** above the sidewalk | photogrammetric, 2.4 — **measured to ±0.3 m** |
| Cornice / rope band | **7.9 m** | photogrammetric, 2.4 |
| Water table / plinth | **1.0 m** | photogrammetric, 2.4 |
| Roof hedge crest | **11.3 m** | photogrammetric, 2.4 — *estimated* |
| Penthouse crest | **13.4 m** | photogrammetric, 2.4 — *estimated*, ±0.7 m, see 2.15 risk 1 |
| South-west neighbour | **41–43 South Park** — shares a **party wall**, gap 0.00 m; OSM has no height tag; DataSF `SF3775040` `hgt_max` 11.88 m | OSM way/112759867 and DataSF, measured against our polygon |
| North-east neighbour | **27 South Park** — **7.34 m gap**; the cream, dark-green-framed two-storey building | OSM way/112759868 |
| Row context (odd side, Second Street end) | 21, 27, **35**, 41–43, 45–47–49 (OSM `height=12`), running south-west from Second Street | OSM — **measured** |
| Historic district status | **Not a contributor** to the National Register South End Historic District — that district reaches South Park only at 1 South Park (570 Second Street) | 2008 NR nomination PDF, searched in full — **verified negative** |
| Permit history (material) | 1992 "structural stiffening of front wall" (UMB); 2001 elevator added + new roof; 2020-08-22 **"tenant improvement; new penthouse level"**; 2020-12 voluntary seismic shotcrete walls; 2021–23 sprinklering across 3 floors; 2023-04-14 **"roof trellis and associated structural and penthouse deck"**; 2025 first-floor TI | DataSF Building Permits, block 3775 lot 102, 40 permits — **verified** |

### 2.2 Sources

- `https://www.openstreetmap.org/way/112759864` — footprint geometry, address, `height=10`
  (a low shell tag; the plans README's standing warning applies and it is not used here)
- `https://data.sfgov.org/resource/ynuv-fyni` (DataSF Building Footprints, LiDAR-derived)
  — footprint `SF3775102`, deck 10.49 / 10.87 m, maximum 12.44 m, ground 11.71 m NAVD88
- `https://data.sfgov.org/resource/wv5m-vpq2` (Assessor Historical Secured Property Tax
  Rolls) — 1920, block/lot 3775/102, 3 storeys, Industrial, 16,420 sq ft on 8,197 sq ft
- `https://data.sfgov.org/resource/i98e-djp9` (SF Building Permits) — the 40-permit
  history above; the 2020 penthouse permit and the 2023 roof-trellis permit are the two
  that change this asset
- `https://www.accel.com/contact-us` — Accel's San Francisco office at 35 South Park Street
- `https://perkinswill.com/project/south-park-venture-capital-firm/` — the 2023
  renovation: brick-clad 1920s building, 16,420 sq ft, birdcage vestibule, arched
  metal-clad windows, salvaged materials
- `https://officesnapshots.com/2026/02/03/south-park-venture-capital-firm-offices-san-francisco/`
  — the same project, photographed (David Wakely); **interiors only**
- Google Street View, **Jan 2025**, pano `41nfDporXIT_NIfYe40GRQ` at
  `37.7817137, −122.3935663` (7.48 m from the facade plane) — the arcade, the roundels,
  the rope moulding, the ghost frieze, the parapet, the sconces, the ring chandeliers
  behind the glass. **The primary source for this asset.**
- Google Street View, Jan 2025, pano at `≈37.78196, −122.39384` (43.68 m, across the
  park) — the whole frontage in context, the roof hedge, the set-back penthouse
- Google Street View, Jan 2025, pano at `≈37.78185, −122.39330` (looking south-west down
  South Park St) — 27 South Park's number plate, the 7.3 m gap, the row context
- Esri World Imagery, nadir, z20 (~0.118 m/px), tiles 167789–167793 / 405269–405273 —
  the roof: bright membrane, the raised penthouse with its roof-light band toward the
  south-west, roof lights on the north-east half, the rear notch
- `https://sfplanninggis.org/docs/NatRegDistricts/2008-06-26_Final-NR-SouthEndHistDist.pdf`
  — searched in full; South Park appears only as 1 South Park (570 Second Street)
- `docs/asset-plans/2-south-park.md`, `168-south-park.md`, `135-south-park.md` — the
  district's material language and the three nearest precedents in this set

Exa searches run, for the record: "35 South Park San Francisco building architecture";
"Accel offices 35 South Park San Francisco Perkins&Will brick 1920s renovation";
"35 South Park San Francisco 1920 building history arched windows terra cotta warehouse
original company name". Domains that yielded material: accel.com, perkinswill.com,
officesnapshots.com, sfplanninggis.org. **Three results that Exa's summariser attached to
this address do not belong to it** and are deliberately excluded: LDP Architecture's
"One South Park" (that is 1 South Park, a 1920s tobacco warehouse with 35 *units* — the
"35" is a unit count); PCAD's Phelan Building (Third Street end, 1897); and HSE
Architects' "Accel Financial Staffing" (a different company in a different city). Do not
let them back in.

### 2.3 Orientation and placement

The building sits on the **north-east arc** of the South Park oval, 55.7 m from the
park's centre, its front looking north-west across the street into the park, its rear
onto the block interior toward Bryant Street. It is rotated 45.5° from the world axes,
like the whole SoMa grid.

Measured footprint polygon, in Blender coordinates (metres, `+X` east, `+Y` north),
already centred on the anchor `−122.3933378, 37.7815714`:

```
v0 (-20.653,   4.786)     west corner   (front / south-west)
v1 ( -4.338,  20.605)     north corner  (front / north-east)
v2 ( 19.139,  -3.261)     \ collinear split on the north-east flank
v3 ( 20.653,  -4.797)     east corner   (rear / north-east)
v4 ( 10.067, -15.078)     rear wall, inner end
v5 (  8.421, -13.409)     notch, step in
v6 (  2.701, -18.947)     notch, outer end          <-- see below
v7 ( -3.872, -12.270)     \ collinear split on the south-west flank
```

Edges, with outward normals:

| Edge | Length | Faces | Elevation |
|---|---|---|---|
| `v0 → v1` | **22.72 m** | NW 315.9° | **the South Park arcade — the hero elevation** |
| `v1 → v2` | 33.48 m | NE 45.5° | north-east flank, onto the 7.34 m gap to 27 South Park |
| `v2 → v3` | 2.16 m | NE 45.4° | same wall (a collinear vertex split, not a jog) |
| `v3 → v4` | 14.76 m | SE 135.8° | **rear wall**, main run |
| `v4 → v5` | 2.34 m | SW 225.4° | the notch's return |
| `v5 → v6` | 7.96 m | SE 135.9° | rear wall, set back 2.44 m |
| `v6 → v7` | 9.37 m | SW 225.4° | south-west party wall with 41–43 |
| `v7 → v0` | 23.93 m | SW 225.5° | same wall (a collinear vertex split) |

Resolved into building-local coordinates — `u` along the frontage, positive toward the
**north-east** (the Second Street end); `v` into the block from the front, positive
toward the **south-east** — the plan is a plain rectangle with one small bite:

```
        u = -11.37                              u = +11.36
 v = -17.9  +----------------------------------------+   <- the arcade (NW front)
            |                                        |
            |                                        |
            |                                        |
 v = +15.4  |               +------------------------+   <- rear wall
            |               |                            (notch: 7.96 u x 2.44 v)
 v = +17.9  +---------------+
          party wall (SW)              rear (SE)
```

So the shell is **22.72 × 35.80 m** minus a **7.96 × 2.44 m** notch at the rear
south-west corner — 19.4 m² out of 813 m². The two "jog" edges in the table above are
collinear vertex splits in the OSM ring, not real steps: the north-east flank is one
straight 35.6 m wall and the south-west flank one straight 33.3 m wall. **Keep the
notch, drop the splits.**

Because of the 45.5° heading the axis-aligned bounding box is ~41.3 × 39.6 m. That is
correct.

**Watch the sign of the heading.** An AABB check cannot distinguish +45.5° from −45.5°.
The mirror check here is: the **entrance bay must be at the south-west end** of the
frontage (nearest 41–43 South Park, the party wall) and the **service opening at the
north-east end** (nearest the 7.3 m gap to 27 South Park); the rear notch must be at the
**south-west** end of the rear wall, on the same side as the party wall. Verify in the
top render before anything else.

### 2.4 What each side shows

**North-west (South Park front) — the hero elevation, 22.72 m wide.** Confirmed from
the Jan 2025 Street View captures in 2.2, bottom to top:

- A **plinth / water table** to **1.0 m**, panelled, slightly proud, running the full
  width.
- **Five giant round-arched bays**, ~4.54 m on centre. Each has a plain moulded
  archivolt springing from a simple moulded impost, and a steel window of fine
  rectangular lights with radial glazing in the arch head. The end bay at each end
  carries a dark full-height opening instead of glazing — the south-west one is the
  recessed main entrance, the north-east one reads as a service/garage opening.
- A **plain circular roundel** on each pier between the arches: a flat disc inside a
  heavy moulded ring, roughly 1.3–1.5 m across, sitting just below the cornice.
- A **cornice band at 7.9 m** with a **twisted rope/cable enrichment** under a stepped
  moulded profile.
- A plain **frieze** above it carrying an inscription whose raised letters have been
  removed; only their shadows survive. The 2025 capture resolves "C … O … O" and no
  more.
- A **tall plain parapet** above the frieze, roughly as deep as the frieze itself,
  finishing at **10.4 m** with a shallow coping.
- Modern **cylindrical glass-and-black-metal sconces** on each pier at about 5 m, and
  warm **ring chandeliers** hanging inside, clearly visible through the glass. Both are
  from the 2023 renovation and both matter at night (2.8).
- The wall is smooth pale grey-cream ashlar (cast stone or plastered masonry) with fine
  coursing joints — **not** the raw brick the district's other warehouses show, and not
  what the Perkins&Will text ("brick-clad") describes. See 2.15.

**North-east flank (onto the 7.34 m gap to 27 South Park), 35.6 m long.** Not
photographed by anything consulted. The gap is real, so this side plausibly has
daylight; treat it as plain rendered masonry with a modest scatter of openings. Do not
invent a full grid. The near-corner return of the arcade's cornice and parapet does turn
this corner in the Street View captures — carry the parapet round.

**South-west flank (party wall with 41–43 South Park), 33.3 m.** Shared along its whole
length, gap 0.00 m. This is a **blank wall**: a party wall cannot carry openings. One of
the few free wins in the dossier — model it unbroken and it will be right.

**South-east (rear), 14.76 m + 7.96 m with the 2.44 m notch between.** Not photographed.
Service elevation onto the block interior; expect a roll-up door and small openings.

**Top — the surface the app's camera actually sees, and this asset's second design.**
From the Esri nadir at ~0.118 m/px plus the across-the-park Street View:

- A **bright white membrane roof** — conspicuously brighter than every neighbouring roof
  on the block, consistent with the 2020–23 re-roof.
- A **continuous clipped hedge along the whole north-west parapet**, crest ≈ 11.3 m. It
  reads from the park as a green line on a pale wall and from above as a green band
  inside the parapet. Nothing else on the oval has one.
- A **set-back penthouse volume** on the south-west half of the front part of the roof,
  darker in value, carrying a band of **four roof lights**, crest ≈ 13.4 m. It casts the
  roof's only real shadow.
- A scatter of **roof lights** on the north-east half of the deck (five or six
  rectangles in two loose rows) and one rounded plant unit near the east corner.
- The rear notch reads as a shadowed bite out of the south-west corner.

**How the heights were measured (photogrammetry).** Ratios of tangents against a known
camera geometry, from the Jan 2025 near pano `41nfDporXIT_NIfYe40GRQ`
(`37.7817137, −122.3935663`), rendered at 1400 × 1000 with a vertical fov of 90° and a
tilt of 105°, so `f = 500 px` and `elevation(y) = 15° − atan((y − 500) / 500)`. The
perpendicular distance from that pano to the facade plane is **7.48 m**, computed from
the OSM ring. Solving `h = h_cam + D·tan(e)` with the wall base pinned to 0 gives
`h_cam = 2.38 m`, which is within 0.12 m of Street View's nominal ~2.5 m camera height —
that agreement is what validates the frame:

| feature | viewport y | elevation | height |
|---|---|---|---|
| wall base at the sidewalk | 820 | −17.6° | 0 (datum) |
| water table | 737 | −10.4° | **1.0 m** |
| cornice / rope band | 303 | +36.5° | **7.9 m** |
| parapet crest | 215 | +44.7° | **9.8 m** (±0.25) |

Repeating the exercise on the across-the-park pano (D = 43.68 m, fov 28°, tilt 101°) and
calibrating `h_cam` to the same parapet gives parapet 10.4 m, hedge crest 10.9 m and
penthouse crest 13.7 m; taking the two frames' spread as the error band lands on
**parapet 10.4 m, hedge 11.3 m, penthouse 13.4 m**, which is what this plan uses. The
consistency check that matters: at 7.48 m the penthouse is *hidden* behind the parapet
(elevation 32° against the parapet's 47°) and at 43.68 m it is *visible above* it
(12.0° against 10.4°) — which is exactly what the two captures show.

### 2.5 Recognition cues (ranked)

1. **The five giant arches** in pale ashlar — the grandest elevation on the oval, and
   unmistakable from the park.
2. **The five roundels** under the cornice — the cheapest, most legible ornament on the
   building and the thing that says "this is not a plain warehouse".
3. **The green hedge line along the parapet** — unique on this block, and the roof's
   whole identity from the app's aerial camera.
4. The **cornice–frieze–parapet stack**: a heavy horizontal cap over a light arcade.
5. The **set-back penthouse** with its roof-light band.
6. Low, wide, flat-topped, at 45.5° to the world grid, blank on the south-west.

Cues 1–2 are read from the street, 3–5 from above. That split is the correct hierarchy
for this building: it is one of the few on the oval that earns both.

### 2.6 Miniature translation

**Preserve**

- The measured footprint, the rear notch and the 45.5° heading
- Five bays, five roundels, and the cornice/frieze/parapet proportion (the cap is
  2.5 m over a 7.9 m order — do not thin it)
- The hedge as a continuous unbroken band, and the penthouse's setback and position
- The blank party wall
- The value ladder: pale stone wall, darker glass, dark deck, green hedge

**Simplify / exaggerate**

- The window grids become a **coarse mullion pattern** — three vertical mullions and
  three transoms per bay, plus a radial fan of three in the arch head. The real glazing
  is far finer and will alias to mush at camera distance (§9).
- The **archivolt and impost mouldings** become one proud band each, 0.10–0.15 m —
  enlarged relative to reality so the arcade still reads as an arcade from 300 m (§9).
- The **roundels are enlarged to ~1.6 m** and given a deeper ring for the same reason.
  They are the one place ornament is worth spending.
- The **rope moulding becomes a single proud band**, not a modelled twist. At the app's
  camera a twist is noise; a band is rhythm.
- The frieze inscription is **not modelled**: the letters are gone in reality and ghost
  lettering cannot survive flat-colour materials. Record the decision.
- The **hedge becomes one clipped chamfered prism** with a slightly irregular top, not
  individual plants (§12: crowns interpenetrate into one volume).
- Roof clutter reduces to the penthouse, one roof-light band on it, four roof lights on
  the deck, one mechanical pair and one hatch. Nothing else.
- Sconces: keep them as five small cylinders — they are what the night state hangs on
  (2.8) — but drop the brackets.
- Dropped: coursing joints, downpipes, signage, the ring chandeliers as geometry (they
  become a glow shell behind the glass), the parapet's ghost lettering, the trellis over
  the penthouse deck (invisible under the hedge line from any camera the app uses).

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not a
straitjacket — adjust after the first aerial review render. Every level is a distinct
closed solid; nothing coplanar.

1. **Body:** extrude the 2.3 footprint from z = 0 to **z = 10.0** (the roof deck),
   `Toy_stone`. The rear notch comes free with the polygon — do not fill it.
2. **Water table:** z = 0 → **1.0**, a 0.12 m proud band around the north-west front and
   returning ~2 m onto the north-east flank, `Toy_stone`, half a tone lighter is not
   needed — the proud band reads on its own shadow.
3. **The arcade,** north-west front only: five bays at 4.54 m centres, springing line at
   **z = 4.6**, arch crown at **z = 6.9**, opening width 3.5 m, recessed 0.35 m.
   - Archivolt: a 0.30 m wide, 0.12 m proud moulded band following the arch,
     `Toy_stone`; impost blocks at the springing.
   - Glazing: `Toy_glass` panel set 0.35 m back, with `Toy_ink` mullions — three
     verticals, three transoms, and a three-ray fan in the head.
   - **End bays:** the south-west bay's lower 4.2 m is a recessed `Toy_roofd` entrance
     portal with a `Toy_ink` reveal; the north-east bay's lower 4.2 m is a
     `Toy_roofd` service opening. Both keep their arched heads and glazing above.
4. **Roundels:** five discs, r = 0.80 m, 0.10 m proud, inside a 0.15 m ring, centred on
   each pier at **z = 7.6**, `Toy_stone` with a `Toy_trim` ring.
5. **Cornice:** z = **7.9 → 8.3**, 0.25 m proud, carried across the front and returning
   0.6 m onto both flanks, `Toy_trim`; a 0.10 m proud rope band immediately under it at
   z = 7.75, `Toy_trim`.
6. **Frieze:** z = 8.3 → **9.3**, flush, `Toy_stone`.
7. **Parapet:** z = 9.3 → **10.4** on the front and both flank returns, 0.35 m thick,
   `Toy_stone`, under a 0.12 m proud `Toy_trim` coping carried right round the ring —
   the coping is what makes the ring read as a ring from the app's downward camera. The
   parapet runs the whole footprint ring, lower (10.2 m) on the rear and party-wall
   sides.
8. **Roof deck** at z = **10.0**, `Toy_roofd` — clearly darker than the parapet cap so
   the ring reads from above.
9. **Roof hedge:** a chamfered prism, 1.1 m wide × 1.3 m tall, from z = 10.0 to
   **11.3**, running the full 22.7 m immediately inside the front parapet, and returning
   ~4 m down each flank, `Toy_verdigris` on a 0.25 m `Toy_ink` planter kerb.
10. **Penthouse:** a set-back block on the south-west half of the front part of the
    roof, ~12.0 × 8.0 m in plan, its front face **8.0 m back** from the front parapet
    and its south-west face on the party wall, from z = 10.0 to **13.4**. Walls
    `Toy_roofd`, a 0.15 m `Toy_trim` upstand at its base, and a band of four
    `Toy_glassl` roof lights, 1.6 × 1.2 m, along its north-west face at z = 11.6.
    **This sets the bounding-box top and must land exactly on the verified crest.**
11. **Roof furniture:** four `Toy_glassl` roof lights 1.6 × 1.2 × 0.25 m on the
    north-east half of the deck; two HVAC blocks (1.8 × 1.4 × 0.8 m and
    1.2 × 1.0 × 0.6 m) `Toy_steel` toward the rear; one roof hatch
    1.2 × 1.0 × 0.5 m `Toy_roofd`.
12. **Sconces:** five cylinders r = 0.16 m, h = 1.0 m, `Toy_ink`, on the piers at
    z = 4.6.
13. Bevel 0.12 m, 2 segments, clamped to a third of the thinnest dimension.

### 2.8 Materials and palette

Flat colours only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_stone` | `d9d2c2` | all four walls, arcade piers, archivolts, frieze, parapet, water table, roundel discs |
| `Toy_trim` | `f3efe6` | cornice, rope band, parapet coping, roundel rings, penthouse upstand |
| `Toy_glass` | `2a4d73` | the five arched windows |
| `Toy_glassl` | `6f95b8` | roof lights on the penthouse and the deck |
| `Toy_roofd` | `45454a` | roof deck, penthouse walls, entrance portal, service opening, roof hatch |
| `Toy_verdigris` | `9fb8a8` | the roof hedge |
| `Toy_ink` | `3a3530` | window mullions, opening reveals, planter kerb, sconces |
| `Toy_steel` | `9aa0a6` | HVAC blocks |
| `Toy_glass_Glow` | `2a4d73` | the lit arched windows — **the hero night state** |
| `Toy_gold_Glow` | `caa64a` | the sconces and the ring chandeliers' spill |

Ten materials, all on-palette. No `Toy_body` (landmarks are never tintable).

The wall is `Toy_stone` (`d9d2c2`), **not** `Toy_brick` or `Toy_rust`. Every other
warehouse in this set swapped toward a brown because raw brick is what they are; this
one is genuinely a pale smooth ashlar facade in the photographs, and it is the value
contrast against its brick and painted-wood neighbours that makes it findable on the
oval. Record the choice in `REPORT.md`. If research shows the front is painted brick
rather than cast stone, the correct correction is a warmer `Toy_stone`, not a swap to
`Toy_brick` — the building must not become an accent (§7).

**Night state (required).** The hero is the **arcade**: five tall arched windows lit
from a double-height interior, which is exactly what the building does — the ring
chandeliers hang in the arch heads and are visible from the park through the glass. Glow
shells must be thin panels proud of the opaque `Toy_glass`, never the glazing itself
(the app renders `_Glow` at ~12% alpha by day; a closed shell reads at ~23% and will
tint the whole facade — see the two-layer note in the style bible). Supporting accent:
the five sconces in `Toy_gold_Glow`. **Nothing else glows** — in particular the
penthouse and the roof lights stay dark, so the night reading is one lit arcade under a
dark cap, which is the same statement the day makes.

This is the strongest street-level night proposition on the oval and a large part of the
reason to build this asset.

### 2.9 Top surface

Composition, north-west to south-east: the bright parapet ring; the green hedge band
just inside it along the whole front; the dark deck; the set-back penthouse on the
south-west half with its roof-light band facing the park; four roof lights loose on the
north-east half; the mechanical pair and hatch grouped at the rear; the notch biting in
at the rear south-west corner.

If the hedge band and the penthouse are not the first two things a viewer sees in the
top render, the asset is not finished.

### 2.10 Scope

**In the GLB:** the single 1920 building — masonry shell on the measured footprint
including the rear notch, arcade, roundels, cornice, frieze, parapet, roof deck, hedge,
penthouse and roof furniture, the two end openings, the sconces.

**Not in the GLB:** South Park (street or park), 27 and 41–43 South Park, the block
interior and its cars, street trees, sidewalk, vehicles, people, plinths, cameras or
lights.

### 2.11 Triangle budget

Cap **9,000**. Suggested split:

| Element | Estimate |
|---|---|
| body on the 8-vertex footprint + rear notch | 600 |
| parapet ring + coping + cornice + rope band returns | 1,600 |
| five arched openings (archivolts, imposts, reveals) | 2,400 |
| five glazed panels + mullions + arch-head fans | 1,300 |
| five roundels (disc + ring, 14-seg) | 700 |
| two end openings | 300 |
| water table | 250 |
| roof hedge prism + planter kerb | 400 |
| penthouse + roof-light band | 700 |
| roof furniture, hatch, HVAC | 400 |
| five sconces (10-seg) | 350 |
| **Total** | **~9,000** |

The arches are the expensive part and the cap should bind there: use 10–12 segments per
arch, not 24. Hard repo limit is 30,000 for a standard landmark; this sits well inside
it, which matters because the asset joins the densest cluster in the manifest — this is
the **twentieth** South Park landmark, all streaming in on one `loadRadius` centre.

### 2.12 Draft manifest entry

```json
{
  "id": "35-south-park",
  "file": "35-south-park.glb",
  "anchor": [
    -122.3933378,
    37.7815714
  ],
  "targetHeightM": 13.4,
  "cat": 3,
  "name": "Accel (35 South Park)",
  "estimated": true,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

`dims` and `tris` are placeholders until the asset is built and validated. `estimated:
true` because the penthouse crest is photogrammetric, not published (2.15 risk 1). The
name follows `101-south-park`'s "Kleiner Perkins (101 South Park)" convention: on this
oval the tenant is what people recognise. `loadRadius` is the default rule,
`max(2500, 13.4 × 30) = 2500`; `alwaysLoaded` would be wrong for a 13 m building.

### 2.13 Integration notes (for later, not this task)

- **New landmark, Case B.** Add a `pipeline/lib/landmarks.mjs` entry
  (`id: '35SouthPark'`) and re-bake the affected tiles, or the baked procedural building
  on this exact footprint will intersect the GLB.

- **`exclude: 6`.** Sized against the metric `excluded()` in `pipeline/buildings.mjs`
  actually uses — *the ring centroid **or** any ring vertex inside the circle*. Measured
  from this anchor:

  | | nearest vertex | centroid |
  |---|---|---|
  | own footprint (OSM way/112759864) | 12.87 m | **0.42 m** |
  | own footprint (DataSF `SF3775102`) | 12.99 m | **1.36 m** |
  | **nearest neighbour (DataSF `SF3775040`, 41–43 South Park, SW party wall)** | **10.68 m** | 14.59 m |
  | nearest neighbour (OSM way/112759867, 41–43 South Park) | 12.87 m | — |
  | next nearest (DataSF `SF3775015`, rear) | 15.51 m | 33.67 m |
  | next nearest (OSM way/112759868, 27 South Park, NE) | 24.73 m | — |

  Both of our own centroids sit within 1.4 m of the anchor, so *any* radius above ~1.5 m
  drops our own footprint from either source; the binding constraint is entirely the
  party-wall neighbour at 10.68 m. The safe window is **1.5 < r < 10.68**, and **6 m
  sits in the middle of it** with 4.5 m of headroom on each side. This is the most
  comfortable exclusion window in the South Park set — unlike `135SouthPark`, whose
  window is 1.5 m wide — and it should be left comfortable rather than tuned.

  **Verify empirically during the re-bake**, the way 375 Alabama and 380 Brannan were:
  procedural footprints dropped must be **exactly one**, and audit 1.6 must report no
  intrusion. If the count is 0 the radius is under our own ring and must go up; if it is
  2 or more it is eating 41–43 South Park, which has no GLB, and must come down.

- **No `clearTrees`.** This is a building, not a park; the oval's scatter is already
  handled by `64SouthPark`'s zone.

- **`camera` is not optional** — `context.mjs` bakes it into `context/landmarks.json`
  and `camera.js` reads `preset.yaw` unconditionally, so omitting it stops the whole city
  booting (see the note on `542PresidioBlvd`). `camera.js` places the eye at
  `target + distance × (sin yaw, ·, cos yaw)` with `+x` east and `+z` south, so to face
  the north-west arcade the camera must stand to the north-west: **yaw 225**. Suggested
  `{ distance: 130, yaw: 225, pitch: 24 }`. **Render it before believing it** — `592Third`
  shipped a yaw derived on paper that turned out to face two blank party walls.

- **Batch mode applies.** A Case B re-bake rewrites ~600 generated files under
  `app/public/tiles/` and `api/_data/` whatever the landmark was. Run the bake, do the
  full Step 5/6 QA on it — a Case B landmark cannot be judged without its exclusion
  applied — then `git checkout -- app/public/tiles api/_data` and commit source only,
  per `docs/asset-pipeline/ADDRESS-TO-ASSET.md`.

- **Streaming check.** This is the twentieth landmark on one 160 m oval and the densest
  cluster in the manifest. After integration run
  `node pipeline/landmark-streaming-check.mjs` against a build: the procedural fallback
  hides loader failures from the eye, and twenty assets sharing one `loadRadius` centre
  is exactly where a failure would hide.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0; XY centre offset within ~1 m
- [ ] Bounding-box top exactly the verified penthouse crest (loader scale lands at 1.0)
- [ ] Oriented footprint 22.72 × 35.80 m ± 0.3 m; AABB ≈ 41.3 × 39.6 m (the 45.5°
      heading, not a scale error)
- [ ] The rear notch is a real void in the exported geometry, 7.96 × 2.44 m, at the
      **south-west** end of the rear wall
- [ ] Five arched bays at 4.54 m centres; five roundels; the entrance bay at the
      **south-west** end and the service opening at the **north-east** end — the mirror
      check (2.3)
- [ ] No openings anywhere on the south-west party wall
- [ ] Cornice at 7.9 m, parapet crest at 10.4 m, hedge crest at 11.3 m, deck at 10.0 m —
      or the build's own corrected values, stated in REPORT.md
- [ ] Hedge is continuous across the full 22.7 m frontage
- [ ] Triangles at or under 9,000; ≤ 500 KB compressed
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the arched windows and the sconces; every glow surface a thin
      shell proud of an opaque parent, day colours matching their non-glow neighbours
- [ ] No cameras, lights, animations, armatures, constraints, or foreign geometry
- [ ] Applied transforms, no negative scales, outward normals (per-object signed volume
      for the union of solids; ray-test residual ≤ 0.15%)
- [ ] Top render resolves into: parapet ring, hedge band, dark deck, penthouse,
      roof lights, rear notch — in that order
- [ ] Night render shows one lit arcade under a dark cap, not a glowing block
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed, with the height
      question's status stated explicitly

### 2.15 Open questions and risks

1. **The target height is the dossier's dominant risk, and it is a dating problem.**
   The DataSF LiDAR is a **2010** product and the building grew between 2020 and 2023:
   permit 202008222419 is a tenant improvement with a **"new penthouse level"**, and its
   2023-04-14 deferred submittal is a **"roof trellis and associated structural and
   penthouse deck"**. So the LiDAR's 12.44 m maximum describes a building that no longer
   exists, and the 13.4 m in this plan is **photogrammetric and estimated**. Its largest
   error term is the penthouse's **setback** from the front parapet — assumed 8 m off a
   nadir aerial; at 5 m the crest is 12.6 m and at 12 m it is 14.1 m. Everything else in
   the height ladder is better founded: the parapet at 10.4 m, the cornice at 7.9 m and
   the water table at 1.0 m come from a frame whose self-calibrated camera height
   (2.38 m) lands within 0.12 m of Street View's nominal 2.5 m, and the parapet agrees
   with the LiDAR deck statistics (10.49 / 10.87 m) once the ~1 m datum offset is
   allowed for. **The error is contained**: because the build normalizes the crest to
   exactly the target and the loader scales by `targetHeightM / measuredHeight`, the
   scale lands on 1.0 whatever the number is, and a wrong value makes the penthouse
   wrong, not the building. Drive it from a named constant, assert it in the validator,
   and mark the manifest entry `"estimated": true`. **A tilted aerial settles this in
   one look — try before you model.**

2. **The storey count conflicts, and the assessor's floor area resolves it.** The
   assessor records 3 storeys every year from 2007; the permits record 2 existing
   storeys until 2020 and 3 from 2021. But `property_area` is **16,420 sq ft** on an
   **8,197 sq ft** lot — exactly 2.0 — for all nineteen years, and the street elevation
   is a single giant order about 10 m tall. The consistent reading is **two tall
   interior levels behind one giant order**, with the assessor's third counted at roof
   level and the permits' change of "existing storeys" in 2021 recording the new
   penthouse. It matters less than it sounds: the exterior is one order and one
   penthouse either way, and that is what gets modelled. **Do not put two rows of
   windows on the arcade to satisfy a storey count.**

3. **The Perkins&Will attribution is inferred, not stated.** The firm's project page
   names no address and its client is "Confidential". The chain is: OSM puts Accel at
   35 South Park; Accel's own contact page confirms 35 South Park Street; the assessor
   records 16,420 sq ft for block 3775 lot 102; Perkins&Will's "South Park Venture
   Capital Firm" is 16,420 sq ft, in a brick-clad 1920s South Park building, completed
   2023; and the permit record shows a 2020–23 ground-up interior renovation at this lot.
   That is a strong triangulation but it is a triangulation. **Label it *inferred* in
   REFERENCE.md.** Nothing in the model depends on it — the renovation's visible
   products (the hedge, the penthouse, the sconces, the ring chandeliers, the new
   glazing) are all confirmed by photography regardless of who designed them.

4. **"Brick-clad" does not match the photographs.** Perkins&Will describe a "brick-clad
   building"; the Street View captures show a smooth pale ashlar facade with cast-stone
   mouldings and no brick anywhere on the north-west front. Both can be true — the flanks
   and rear of a 1920 SoMa warehouse are almost certainly brick, and only the street
   elevation got the stone order. The model follows the photographs on the front and
   should treat the unphotographed flanks as plain rendered masonry rather than as either
   stone or brick. **If photography of the flanks turns up brick, use `Toy_rust` there
   and keep `Toy_stone` on the front** — that contrast is real and is worth having.

5. **The address is ambiguous in one direction.** OSM, every building permit and Accel
   all say **35**; Google Maps labels the frontage **33 S Park St**. The lot is a merged
   one (lot 102 on an 8,197 sq ft parcel behind a 22.7 m frontage), so 33 and 35 are
   almost certainly two historic numbers on one building. The manifest id, the plan and
   the registry use **35**, which is what the data sources and the occupant use.

6. **The frieze inscription is unread.** The raised letters have been removed and only
   their shadows survive; the Jan 2025 capture resolves "C … O … O" and nothing more.
   This plan does not model it, so nothing depends on it — but an older Street View
   capture may show the letters in place, and if it does, the building's original name
   belongs in REFERENCE.md and in the manifest `name`. It would also show the
   pre-renovation building, which is the cheapest available check on risk 1.

7. **The bay count is counted through winter foliage.** Five arched bays is read off two
   Jan 2025 captures with London plane branches across them. Five over 22.72 m gives
   4.54 m centres, which is a credible bay for this order, but a recount from a clean
   photograph should happen before the arcade is committed — the arcade *is* the asset,
   and a four- or six-bay rhythm changes it completely.

8. **The north-east flank, the rear and the notch's section are unphotographed.** The
   notch is measured in plan and unknown in section: whether it is open to the ground, a
   ground-floor-only setback with the upper level oversailing, or a roofed infill is
   unresolved. Modelling it as a full-height void is the safe choice — it is right at
   the roof, which is what the camera sees, and defensible at ground level.

9. **No architect is recorded for the 1920 building** in any source consulted, and the
   building carries no landmark or historic-district status: the National Register South
   End Historic District nomination was searched in full and reaches South Park only at
   1 South Park (570 Second Street).
