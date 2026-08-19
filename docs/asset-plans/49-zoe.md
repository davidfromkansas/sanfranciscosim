# 49 Zoe Street — SF-SIM asset plan

A **16-unit artist live/work loft building of 1996–97** on a 25-foot SoMa alley, and one
of the purest examples in the scene of the typology that rebuilt this district: a two-
storey office/storage shed demolished in 1994, replaced by a five-level box of double-
height lofts over a garage, then **re-clad in 2011–13** in the flat rainscreen panel
system it wears today. Three things make it:

1. The **vertical "bar code" facade** — a flat panel rainscreen laid out as irregular
   full-height stripes in five near-neutral tones (off-white, warm pale, warm grey,
   sage-grey, blue-grey). No cornice, no base moulding, no reveal: the stripes simply
   run from the base shelf to the parapet and the windows are punched through them.
   This is the building's whole identity and the one place semantic exaggeration is
   spent.
2. The **double-height loft rhythm** — the 28 m Zoe elevation reads as *two* residential
   tiers, not four floors, because each tier is one double-height unit: a floor-to-
   ceiling window with a horizontal-slat juliet rail, a narrow spandrel, then the
   mezzanine window above it. Four bays wide, two tiers tall.
3. The **split-face CMU garage base** — a rusticated concrete-block plinth carrying five
   plain grey roll-up doors and one recessed pedestrian entry under a galvanised steel
   awning (permit 9704456, March 1997). The panel wall oversails it by ~0.2 m, so the
   base sits in its own shadow line.

Above all of that, and the reason the asset is worth building at this scale: a **designed
roof**. The aerial shows a pale grey membrane carrying a central spine of three raised
glazed monitors lighting the internal circulation, a scatter of square dome skylights, a
stair/elevator penthouse with a round vent at the south-east end, and — documented by the
sale listings rather than the imagery — a common roof deck. The camera looks down at this
building constantly; the roof is its fourth elevation and its night hero.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/49-zoe/`. This document is the plan only: Part 1 is the runnable task prompt,
Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `49-zoe` |
| Existing procedural builder | none — new landmark (**Case B**: needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3960338, 37.7800764` (simplified-footprint centroid, measured) |
| Target height | **17.0 m** (stair/elevator penthouse crest, DataSF LiDAR `hgt_maxcm` 16.99 m); parapet **14.4 m** (LiDAR median 14.42 m); roof deck **13.6 m** |
| Footprint | 558.6 m2; a clean 45-degree-grid rectangle **28.24 m (Zoe frontage) x 19.78 m (depth)** |
| Triangle cap | 11,000 |
| Category | `2` (apartments — live/work condominium) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 49 Zoe Street GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of 49 Zoe Street — the 16-unit live/work loft
building on the north-east side of Zoe Street between Bryant and Brannan in San
Francisco — and deliver it as a downloadable, validated GLB.

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
7. `artifacts/340-brannan/` — **the reference implementation.** 340 Brannan is the
   closest match in the repo: a flat-fronted SoMa box of the same era and roughly the
   same height, with a punched window grid over a distinct ground-floor base and a
   designed flat roof. Its build script is the skeleton to **adapt, not rewrite** — the
   footprint/edge helpers (`poly_edge`, `offset_polygon`, `wall_box`, `bay_spans`,
   `window_unit`, `glazed_elevation`) all carry over. `artifacts/318-brannan/` is the
   secondary reference for the roof-furniture composition and the palette discipline on
   a pale-walled building.
8. `docs/asset-plans/49-zoe.md` — this plan, whose dossier is your research starting
   point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract, `AGENTS.md`
governs repository and integration rules.

## Must capture

- A **flat-topped rectangular box** filling its whole lot: 28.24 m along Zoe Street by
  19.78 m deep, five levels (garage plus two double-height loft tiers), continuous
  parapet, no setbacks
- The **vertical stripe facade**: full-height panel bands of *irregular* width (0.35 m
  to 1.5 m) in five near-neutral tones, running from the base shelf to the parapet on
  the Zoe elevation. Irregular is the point — a regular stripe reads as a barcode
  pattern swatch, not as this building
- The **double-height loft rhythm**: four bays, two tiers, each tier = tall
  floor-to-ceiling glazing + horizontal-slat juliet rail + narrow spandrel + mezzanine
  window above
- The **split-face CMU base**, ~2.95 m tall, with five grey roll-up doors and one
  recessed pedestrian entry under a small galvanised steel awning, plus small louvre
  vents. The panel wall above **oversails the base by ~0.2 m** — keep that shadow line
- The **designed roof**: parapet ring, pale grey membrane, a central spine of three
  raised glazed monitors, a scatter of square dome skylights, small vent cans, the
  stair/elevator penthouse with its round vent at the south-east end, and a paved common
  roof deck
- A **blank party wall** on the north-west face, exposed above ~12 m because 33–35 Zoe
  next door is 2.5–3.5 m lower
- A **mostly blank south-east elevation** onto the parking lot, with small punched
  windows in vertical stacks and a black steel fire escape (permit 9621922, "east
  elevation", 1996)

## Research 49 Zoe Street independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor and the real-world orientation,
and gather references covering:

- The Zoe Street (south-west) elevation in full — it is the only street-visible face
- The south-east elevation across the surface parking lot at 5 Freelon / 52 Zoe
- Aerial and roof views (the monitor spine, the skylight scatter, the penthouse, the
  roof deck)
- The **bay count and stripe rhythm** of the Zoe elevation — the dossier reads four bays
  and roughly thirty stripes from a rectified Street View elevation, and the stripe
  widths are the single thing most worth re-measuring
- Whether the paved area at the **north-west end of the roof** belongs to 49 Zoe or to
  33–35 Zoe next door (see 2.15 risk 2)

**Four source traps are already known and resolved in 2.1 and 2.15 — re-check them, do
not silently re-inherit the wrong value:**

1. OSM way/147508937 tags `height=14`, sourced from Bing. It happens to agree with the
   LiDAR roof plane, but it is **not** the architectural top: the stair/elevator
   penthouse reaches 17.0 m. Do not normalise the model to 14 m.
2. **Kaplan Architects is a tenant of Suite 10, not the designer.** Business-registry and
   LinkedIn pages put an architecture practice at this address; that is where its
   principal lives, and it says nothing about who designed the building. No architect of
   record has been found — treat the building as anonymous developer work.
3. **Santos Prescott's "Ritch / Zoe Studio" is the neighbour, not this building.** That
   1998 project (Adele Santos, client and architect) is 33–35 Zoe Street, DataSF
   `mapblklot` 3776144, sharing our north-west party wall. The Curbed article
   "Concrete SoMa loft with floor-to-ceiling windows asks $1.95M" (May 2020) is about
   *that* building. Do not attribute its concrete/courtyard character to 49 Zoe.
4. **The facade you can see is from 2013, not 1997.** Permit 201110187089 (filed Oct
   2011, completed May 2013, $300,000) re-clad the whole exterior and replaced every
   window "to eliminate water intrusion issues". Any pre-2013 photograph shows a
   different building. Model the current state.

## Create a reference dossier

Write `artifacts/49-zoe/REFERENCE.md` containing: source links and what each
establishes; verified dimensions and location; orientation; observations from all four
sides and above; the 3–5 strongest recognition cues; features to preserve; features to
simplify; uncertainties and conflicting evidence. Do not commit copyrighted
full-resolution imagery.

## Make your own design decisions

Follow the conversion process in `docs/styles/miniature-toy.md` §22: identify the
recognition cues, strip nonessential information, rebuild the massing from a few
confident volumes, exaggerate only the signature features, simplify the facade into
broad rhythms, deliberately design every surface visible from above, evaluate from the
app's high three-quarter aerial camera, then simplify again.

This is a **background building with character** in the style bible's detail budget
(§21). It is not a monument and it is not the tallest thing on its block — 500 Third
Street (26.5 m) is 90 m south-east and the neighbour behind it reaches 15.9 m. It earns
its detail from two things only: the stripe facade, which nothing else in the scene has,
and the roof, which the camera sees constantly. Spend the budget there and keep the
north-east elevation nearly empty.

Watch the **value budget in the opposite direction from usual**: almost every surface
here is pale. The risk is not a black building, it is a white blob. The stripe tones must
be far enough apart to survive the app's flat lighting — check the aerial render, not the
Blender review rig, before settling the palette (see `docs/styles/` and the note in 2.8).

The finished asset must be immediately recognizable as this building, consistent with
the real one from all four sides and above, architecturally credible, and a premium
handcrafted miniature — not photorealistic, not voxel art, not generic low-poly, and
never accurate in one view while invented in the others.

## Scope of the exported asset

Export the single block: body, CMU base and its openings, all four elevations, the
stripe cladding, windows and juliet rails, the entry awning, the fire escape, parapet,
roof deck and roof furniture.

Do not include unrelated surrounding city geometry: Zoe Street, the surface parking lot
south-east of the building, 33–35 Zoe Street, 25 Zoe Street, 226/248 Ritch Street, the
two large street trees on the Zoe frontage, the overhead utility poles and wires (they
cross every photograph — they are not part of the building), the sidewalk, parked cars,
people, plinths, cameras or lights.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary `.glb`;
real-world meters; origin at base center; minimum geometry Z ≈ 0; applied transforms; no
negative scales; outward normals; no duplicate or foreign geometry; no image textures; no
transparency; flat-color materials named `Toy_*` from the project palette; `_Glow` suffix
only on surfaces that glow at night; no `Toy_body`; no cameras, lights, animations,
armatures or constraints; at most 11,000 triangles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model drops
into the city at its real-world heading — the loader applies no rotation (`placeGeneric`
in `app/src/assets.js` only scales and positions). The **Zoe Street elevation faces
south-west, bearing 225.4°**; the **rear elevation faces north-east, 45.2°**; the
**parking-lot elevation faces south-east, 134.8°**; the **party wall faces north-west,
315.0°**. Build directly on the measured footprint rectangle in 2.3 rather than modelling
an axis-aligned box and rotating it. Record the measured headings in `REPORT.md`.

**Height normalization:** the tallest geometry in the export (the penthouse cap) must land
at exactly **17.0 m** so the loader's `targetHeightM / measuredHeight` scale is 1.0.

## Reproducible Blender workflow

Blender 5.2 LTS. Headless: `blender -b --python script.py -- args`.

Keep `artifacts/49-zoe/build_49_zoe.py` (deterministic build script),
`artifacts/49-zoe/49-zoe.blend`, and `artifacts/49-zoe/49-zoe.glb`. The script must
rebuild the model reliably enough for future revision.

## Required review renders

Render the exact final geometry from controlled cameras: `49-zoe-top.png`,
`49-zoe-north.png`, `49-zoe-east.png`, `49-zoe-south.png`, `49-zoe-west.png`, plus
`49-zoe-contact-sheet.png`, at least one high three-quarter aerial beauty render
`49-zoe-aerial.png`, and a night render `49-zoe-aerial-night.png`.

The four elevations must share scale, framing, lighting, exposure and projection. The
**`south` render is the important one** — it looks down the Zoe elevation's outward
normal, which is this building's subject. The **top view** must clearly show the parapet
ring, the monitor spine, the skylight scatter, the penthouse and the roof deck; on a
building this plain, the top view is where a lazy roof is caught.

## Validate the exported GLB

Re-import `49-zoe.glb` into a fresh isolated Blender scene and validate the re-import,
not the source scene. Report object count, triangle count, dimensions, bounding-box
min/max, min Z, XY center offset, material names, image-texture count, camera count,
light count, animation count, applied-transform status, negative-scale status,
normal-orientation status, unexpected geometry, and per-material contract compliance.
Write `artifacts/49-zoe/validation.json` and `artifacts/49-zoe/REPORT.md`.

The axis-aligned XY bounding box will be roughly **33.8 x 34.1 m** even though no
elevation is longer than 28.24 m — that is the expected consequence of a 45° real-world
heading, not a scale error.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this draft
entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "49-zoe",
  "file": "49-zoe.glb",
  "anchor": [
    -122.3960338,
    37.7800764
  ],
  "targetHeightM": 17.0,
  "cat": 2,
  "name": "49 Zoe Street",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`,
or any app code in this task. Integration is a separate, explicitly requested job — run
`docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in
`docs/asset-plans/49-zoe.md`.
````

---

## Part 2 — Research and design dossier

Confidence labels follow `docs/asset-plans/README.md`: **measured** (from a survey,
open-data record or a metric rectification), **observed** (read off a photograph),
**inferred** (reasoned from typology or from a related record), **estimated** (a
judgement call with a stated basis).

### 2.1 Verified facts

| Fact | Value | Confidence | Source |
|---|---|---|---|
| Address | 49 Zoe Street, San Francisco CA 94107 | measured | DataSF parcels `acdm-wktn` |
| Block / lot | Block **3776**, `mapblklot` **3776128**, condo lots 128–143 (+ five `…Z` parking-stall lots) | measured | `acdm-wktn` |
| OSM way | `way/147508937` (`building=yes`, `addr:housenumber=49`, `addr:street=Zoe Street`, `height=14`, `source=Bing`) | measured | OSM API |
| Year built | **1997** (assessor); construction permits 1996–97 | measured | `wv5m-vpq2`; `i98e-djp9` |
| Previous building | a two-storey office/commercial/storage building, demolished under permit **9421357** (issued Dec 1994) | measured | checkpermits / SF DBI |
| Use | **artist live/work**, 16 units, "Live/Work Condominium" (assessor class `LZ`) | measured | `wv5m-vpq2`; permits |
| Units | **16**, in **two identical tiers of eight** — assessor areas repeat exactly: 694, 775, 860, 937, 832, 987, 900, 693 sq ft on lots 128–135 and again on 136–143 | measured | `wv5m-vpq2` (2025 roll) |
| Total unit area | 13,356 sq ft = 1,241 m2 | measured | `wv5m-vpq2` |
| Storeys | **5** per the 2018 re-roofing permit; visually **one CMU garage level plus two double-height loft tiers** (four window rows) | measured / observed | `i98e-djp9`; Street View |
| Zoning | CMUO (Central SoMa Mixed Use — Office); **SLI** at the time of construction | measured | `acdm-wktn`; `wv5m-vpq2` |
| Footprint | **558.6 m2** as a regularised rectangle; the raw DataSF ring is 561 m2 | measured | `ynuv-fyni` `SF3776128`; OSM |
| Plan dimensions | **28.24 m** (Zoe frontage) x **19.78 m** (depth) | measured | DataSF ring, opposite sides averaged |
| Roof plane | **14.42 m** above grade — LiDAR median over 2,268 cells, sd **1.13 m**, mean 14.41, modal 14.38 | measured | `ynuv-fyni` |
| Crest | **16.99 m** — LiDAR maximum, attributed to the stair/elevator penthouse visible on the aerial | measured / inferred | `ynuv-fyni`; Google satellite z21/z22 |
| Ground | 5.12–5.60 m NAVD88 across the footprint (range 0.48 m) — effectively flat | measured | `ynuv-fyni` `gnd_*` |
| Current facade | installed **2011–2013** under permit **201110187089** ("re-cladding of exterior of existing building and installation of new windows to eliminate water intrusion issues", $300,000, completed 31 May 2013) | measured | checkpermits / SF DBI |
| Entry awning | galvanised steel, permit **9704456**, completed 11 Mar 1997 | measured | checkpermits / SF DBI |
| Fire escape | "east elevation", permit **9621922**, $8,000, completed 1996–97 | measured | checkpermits / SF DBI |
| Roof deck | a **common-area roof deck** exists ("Common area roofdeck offers spectacular urban views") | measured (listing text) | Unit 6 sale listing, Jul 2020 |
| Architect | **not established.** No architect of record found | — | see 2.15 risk 1 |

**On the height.** The discriminator from `164-south-park` applies in reverse here: a
standard deviation of **1.13 m** over 2,268 half-metre cells, with mean (14.41), median
(14.42) and mode (14.38) all within 4 cm of each other, is a textbook **single flat
plane**. There is no second roof level. The 16.99 m maximum is therefore a discrete
object on that plane, and the aerial shows exactly one candidate: a pale rectangular
penthouse with a round vent at the south-east end, 2.6 m proud of the deck — an elevator
overrun and stair bulkhead, which is what the listing's "elevator and easy staircase
access" and its roof deck both require. It is not tree canopy: `peak_1st_m` (22.29 m)
minus `gnd_min_m` (5.12 m) is 17.17 m, i.e. the first-return peak and `hgt_max` agree, and
a canopy over the footprint would have pushed them apart.

**Independent corroboration of the roof plane.** A metric rectification of the Google
Street View panorama `c2ZLvpFONJnFRVJgvl9OMw` (see 2.2) put the parapet at **13.2 m ±0.7 m**
— it agrees with the LiDAR to within its own error, which is dominated by ±0.7 m of
uncertainty in the solved camera-to-facade distance at a 60° look-up angle. OSM's Bing
`height=14` is a third, independent agreement. **14.4 m is the roof; 17.0 m is the crest.**

### 2.2 Sources

**Open data (primary, all measured):**

- DataSF `ynuv-fyni` (Building Footprints, 2010 LiDAR-derived), record `SF3776128` —
  footprint ring, `hgt_mediancm` 1442, `hgt_maxcm` 1699, `hgt_stdcm` 113.4,
  `hgt_cells50cm` 2268, `gnd_min_m` 5.12, `peak_1st_m` 22.29.
- DataSF `acdm-wktn` (Parcels) — block 3776, `mapblklot` 3776128, sixteen residential
  condo lots 128–143 plus five parking-stall lots, zoning CMUO.
- DataSF `ramy-di5m` (Addresses) — "49 ZOE ST #1" through "#16" all resolving to a single
  point at `-122.3960123, 37.7800761`; **no other street number shares this footprint**,
  so the one-parcel-many-addresses trap does not apply here.
- DataSF `wv5m-vpq2` (Assessor secured roll, 2025) — year built 1997, class `LZ`
  Live/Work Condominium, the eight-value area fingerprint repeated across two tiers.
- DataSF `i98e-djp9` (Building permits) — 2018 re-roof (5 existing storeys, 16 units,
  "apartments"); 2019 unit alteration ("artist live/work", 16 units).
- OpenStreetMap `way/147508937` and the Zoe Street centrelines (`way/1459359169`,
  `way/8917324`) used to establish which face is the frontage.

**Permit history (measured, via checkpermits.com aggregation of SF DBI):**

- `9421357` Dec 1994 — demolish a two-storey office/commercial/storage building.
- `9421358` (+ revision `9623952`, Dec 1996) — the new building; "1 hr roof assembly using
  TJI joists".
- `9611330` Jun 1996 — automatic fire sprinkler system, use recorded as "apartments".
- `9618982` Oct 1996 — fire alarm, common area.
- `9621922` 1996–97 — **install fire escape at east elevation**, $8,000.
- `9704456` Mar 1997 — **install galvanised steel awning over entry**, $1,500.
- `201110187089` Oct 2011 → May 2013 — **re-cladding + all-new windows + new roof**,
  $300,000. *This permit is the current building.*
- `201804186674` Apr 2018 — re-roof, $133,500 (Tom Lee Roofing).

**Imagery (observed):**

- Google Street View panorama `c2ZLvpFONJnFRVJgvl9OMw`, on Zoe Street directly in front of
  the building, imagery ©2026 — the only street-visible elevation. A full equirectangular
  tile set was reprojected to a metric orthographic elevation for this dossier (method
  below); the derived images are **not committed** (see `docs/asset-plans/README.md` on
  copyrighted imagery).
- Google Street View panorama `HoUosdm6QHhH_l1AhoKXVw`, Zoe at Freelon — establishes the
  parking lot south-east of the building and the alley context; the building itself is
  occluded from there.
- Google satellite tiles at z21 and z22 (`mt1.google.com/vt/lyrs=s`) — the roof
  composition, rectified into building-local plan coordinates against the DataSF ring.

**Exa web research (observed / listing-sourced):**

- `web_search_advanced_exa("49 Zoe Street San Francisco live/work lofts building")` —
  yielded the Compass and BarbCo listings for Unit 6 (987 sq ft, sold $880,000 on
  2020-07-27), which are the source for *16 unit boutique building*, *elevator and easy
  staircase access*, *common area roofdeck*, *grand exclusive use patio*, *soaring floor
  to ceiling windows*, and *parking and storage in garage*. Label these **observed
  (listing copy)** — listings describe the building as marketed.
- `web_search_advanced_exa("49 Zoe Street ... architect developer new construction")` —
  returned no architect of record. It surfaced `santosprescott.com/project/ritch-zoe-studio`
  and `opengovus.com/san-francisco-business/0187171-01-001`, both of which are traps; see
  Part 1 and 2.15.
- Domain-restricted photo pass over redfin / zillow / compass / sf.curbed / socketsite
  produced **no exterior photograph of 49 Zoe** — the SoMa loft listings it returned are
  355 Bryant, 415 Bryant, 461 Second (Clocktower), 601 Fourth and 175 Bluxome, and the
  one Curbed piece is 33 Zoe next door. Street View is therefore the *only* elevation
  reference and the rectification below is what makes it quantitative.

**Method note — how the Street View elevation was made metric.** Following
`sf3d-streetview-photogrammetry`: the equirectangular tile set (zoom 3, 4096x2048) was
downloaded with a browser user-agent and referer; the panorama's own reported lat/lon was
*not* trusted. The two facade corners were read off the equirect at columns 183 and 1665,
giving a subtended angle of 130.2°; constraining the camera to the Zoe Street centreline
then fixes it at 6.2 m from the facade plane and 18.9 m along it from the north-west
corner, with a yaw offset of 136.07° and a panorama roll of −2.2°. Every facade point's
horizontal distance is then known, and the equirect resamples into a true orthographic
elevation whose scale is fixed by the surveyed 28.24 m frontage. The parapet fit has an
rms residual of **0.35 m** across 146 sampled columns, which is the accuracy to attach to
every height in 2.4 and 2.7.

### 2.3 Orientation and placement

The building sits on the standard 45° SoMa grid, one block north-west of Third Street and
between Bryant (82 m south-east) and Brannan (110 m north-west).

Regularised footprint, in the app's local tangent frame (`x=(lon−(−122.4375))·111320·cos(37.77°)`,
`z=−(lat−37.77)·110540`):

| Corner | x | z | Note |
|---|---|---|---|
| A | 3631.94 | −1116.89 | north corner — Zoe frontage at the party wall |
| B | 3645.89 | −1130.85 | west corner — rear at the party wall |
| C | 3665.77 | −1110.85 | east corner — rear at the parking lot |
| D | 3651.81 | −1096.77 | south corner — Zoe frontage at the parking lot |

| Face | Length | Outward normal | What is beyond it |
|---|---|---|---|
| **South-west (D→A)** | **28.28 m** | **225.4°** | **Zoe Street.** The facade stands 6.2 m from the centreline of a ~13 m right-of-way. The only street-visible elevation |
| North-west (A→B) | 19.74 m | 315.0° | **Party wall** with 33–35 Zoe (`SF3776144`), which touches at 0.00 m and is 10.8–11.9 m tall — so our wall is exposed for its top ~2.5–3.5 m |
| North-east (B→C) | 28.20 m | 45.2° | A **2.4–2.7 m light gap**, then `SF3776456` (15.9 m) and `SF3776105` (8.0 m) fronting Ritch Street. Effectively invisible |
| South-east (C→D) | 19.83 m | 134.8° | An **open surface parking lot** — this elevation is fully exposed and is the second-most-seen face from the app's aerial camera |

The raw DataSF ring carries two 0.33 m in/out jogs part-way along the south-east face.
They are digitising-scale articulation, below the miniature's resolution; **regularise the
plan to a clean rectangle** and note the simplification in `REPORT.md`.

Anchor: **`-122.3960338, 37.7800764`** — the centroid of the four corners above.
Nominatim independently returns `-122.3960408, 37.7800750` for the address (0.6 m away),
and the DataSF address point is `-122.3960123, 37.7800761` (1.9 m away, the parcel
centroid). Use the corner centroid: it is the point the model is actually centred on.

Ground is flat here (LiDAR ground range 0.48 m over the whole footprint), so no terrain
compensation is needed.

### 2.4 What each side shows

**South-west — Zoe Street (28.24 m, the subject).** Measured off the rectified elevation,
±0.35 m:

| Element | Height band |
|---|---|
| Split-face CMU base, sidewalk to shelf | 0.00 – 2.95 m |
| Roll-up doors within the base | ~0.15 – 2.40 m |
| Panel wall starts, oversailing the base ~0.20 m | 2.95 – 3.10 m |
| **Tier 1** main glazing (floor-to-ceiling) | 3.10 – 5.55 m |
| Tier 1 juliet rail (horizontal slats, ~0.15 m proud) | 3.30 – 4.30 m |
| Tier 1 spandrel | 5.55 – 5.90 m |
| Tier 1 mezzanine window | 5.90 – 7.80 m |
| Panel band between tiers | 7.80 – 8.40 m |
| **Tier 2** main glazing | 8.40 – 10.70 m |
| Tier 2 juliet rail | 8.50 – 9.50 m |
| Tier 2 spandrel | 10.70 – 11.00 m |
| Tier 2 mezzanine window | 11.00 – 12.50 m |
| Blank panel (roof structure zone) | 12.50 – 13.60 m |
| Parapet | 13.60 – 14.40 m |

Horizontally the elevation reads as **four bays on a ~7.06 m module**, each carrying
roughly 3.5 m of glazing centred in it. The base carries **five roll-up doors** of about
2.9–3.4 m each with 0.5–0.9 m CMU piers between them, and a **recessed pedestrian entry**
at the south-east end under the galvanised steel awning. Two large street trees stand in
front of the middle of the frontage and occlude bays 2 and 3 in every available
photograph — *the bay widths and stripe rhythm are the numbers to re-verify.*

The stripes themselves: full-height vertical panel bands, roughly thirty of them across
the frontage, widths from about 0.35 m to 1.5 m, in five tones. They continue across the
spandrels and the blank band below the parapet; the windows are cut through them. There
is no cornice, no coping projection, no expressed structure.

**North-west — party wall.** Blind. 33–35 Zoe is 2.5–3.5 m lower, so the top ~3 m of our
wall stands clear. **inferred:** a plain panel or painted-blockwork wall, no openings.

**North-east — rear.** Onto a 2.4–2.7 m light gap with a 15.9 m neighbour immediately
behind. **observed (aerial, oblique):** a plain pale wall with a small number of
punched openings. Keep it nearly empty.

**South-east — parking lot (19.78 m).** **observed (aerial, oblique):** a largely blank
cream wall with small punched windows in vertical stacks, and the black steel fire escape
of permit 9621922. This is the face the aerial camera sees second-most; it must be
credible but it must not compete with Zoe.

**Above — the roof (558 m2).** **observed (Google satellite z21/z22, rectified into plan
coordinates against the DataSF ring):**

- A pale grey membrane over the whole footprint, inside a continuous parapet ring.
- **A central spine of three raised glazed monitors** running roughly along the long axis,
  staggered rather than collinear, each about 7 m long and 2 m wide and made of five or
  six mullioned panes. They light the internal circulation between the Zoe-facing and
  rear units, and they are the roof's subject.
- **A scatter of square dome skylights**, roughly 1.5–2 m, six to eight of them,
  distributed across both halves.
- **Small vent cans**, 0.3–0.5 m, in loose clusters near the monitors.
- **The stair/elevator penthouse** at the south-east end: a pale rectangular block roughly
  8 x 6 m in plan, 2.6 m proud of the deck (crest 17.0 m), with a **round vent or dome**
  on top. This is the tallest thing on the building.
- **A paved common roof deck** at the north-west end — documented by the sale listing,
  and matching a walled paved area visible on the aerial at that corner. See 2.15 risk 2:
  the aerial cannot distinguish it from the neighbour's roof court with certainty.

### 2.5 Recognition cues (ranked)

1. **The irregular vertical stripe facade.** Nothing else in the scene has it. If the
   model reads as a plain pale box, the asset has failed even if every dimension is right.
2. **The double-height loft rhythm** — two tall tiers, not four floors, each with a juliet
   rail across its lower window.
3. **The rusticated CMU garage base with its row of grey roll-up doors**, in its own
   shadow line under the oversailing panel wall.
4. **The monitor spine on the roof** — three staggered glazed ridges down the middle of an
   otherwise plain grey membrane.
5. **The penthouse with its round vent** at the south-east end, breaking the flat
   silhouette exactly once.

### 2.6 Miniature translation

The building is already a box; the toy translation is entirely about *rhythm and value*,
not massing.

- **Chunk the stripes.** Thirty real stripes become **fourteen to eighteen** on the model,
  keeping the irregularity (a 3:1 range of widths) and the five-tone palette. Model them
  as flat panels 0.04 m proud/recessed in an alternating pattern so the aerial sun rakes
  them and they read even when the colour difference washes out. This is the single most
  important decision in the asset.
- **Exaggerate the base shadow.** Push the panel wall's oversail from 0.20 m to **0.35 m**
  so the CMU plinth reads as a separate object from the aerial.
- **Exaggerate the juliet rails.** Real ones project ~0.15 m; model them at **0.30 m** with
  three chunky horizontal slats. They are what makes the tier rhythm legible from above.
- **Simplify the windows** to one flat `Toy_glass` pane per opening in a `Toy_white` frame
  0.10 m wide, set back 0.12 m. No mullion grids: at this scale they turn to noise.
- **Keep the CMU as texture-by-geometry, not by colour** — a single horizontal reveal at
  about 1.5 m plus the door reveals is enough; do not model block courses.
- **Design the roof deliberately** (§2.9). The monitors get real glazed tops; the skylights
  are simple kerbs and panes; the deck is a paved rectangle with a 1.1 m wall.
- Bevel everything 0.10–0.12 m, two segments, per the style bible.

### 2.7 Massing recipe

All heights are metres above the model's z=0 (grade). Build on the 45°-grid rectangle from
2.3, not on an axis-aligned box.

1. **Body.** Extrude the 28.24 x 19.78 m rectangle from z=0 to **z=13.60** (`Toy_sand`
   as the base wall colour; the stripes overlay it on the Zoe face).
2. **Parapet.** Ring on all four edges, z=13.60 to **z=14.40**, 0.30 m thick,
   `Toy_white` coping.
3. **Roof deck.** Cap at z=13.60, `Toy_steel` (pale grey membrane — *not* `Toy_roofd`, see
   2.8).
4. **CMU base.** z=0 to **z=2.95**, `Toy_stone`, set **0.35 m back** from the panel wall
   above on the Zoe elevation (flush on the other three). One 0.05 m horizontal reveal at
   z=1.50.
5. **Roll-up doors.** Five `Toy_steel` panels in the base, z=0.15 to z=2.40, each ~3.1 m
   wide, recessed 0.20 m, with a 0.10 m `Toy_ink` head reveal and a small `Toy_ink` louvre
   at the foot.
6. **Pedestrian entry.** At the south-east end of the base: a 1.6 m recess 0.45 m deep, a
   `Toy_ink` door z=0 to z=2.30, and a **galvanised steel awning** — a `Toy_steel` slab
   0.12 m thick projecting 1.10 m at z=2.55, with a 0.08 m `Toy_ink` underside reveal.
7. **Stripe cladding, Zoe elevation.** z=2.95 to z=14.40 (i.e. up the parapet too — the
   stripes run out at the coping). Fourteen to eighteen vertical bands of irregular width
   between 0.55 m and 2.00 m summing to 28.24 m, alternating 0.04 m proud/flush, in the
   five tones of 2.8. **No two adjacent bands the same tone; no repeating group of four.**
8. **Tier 1 openings.** Four bays on a 7.06 m module. In each bay: main glazing 3.5 m wide,
   z=3.10 to z=5.55, in a `Toy_white` frame, set back 0.12 m; a `Toy_steel` juliet rail
   (three 0.10 m slats on two posts) 0.30 m proud, z=3.30 to z=4.30; a flush spandrel
   z=5.55 to z=5.90; mezzanine glazing 3.5 m wide, z=5.90 to z=7.80.
9. **Tier 2 openings.** The same, shifted up: main glazing z=8.40 to z=10.70 with its rail
   z=8.50 to z=9.50; spandrel to z=11.00; mezzanine glazing z=11.00 to z=12.50.
10. **South-east elevation.** `Toy_sand` wall, no stripes. Two vertical stacks of small
    punched `Toy_glass` windows 1.0 x 1.2 m at z=4.0, 6.2, 9.3, 11.5. A **fire escape** on
    the north-east half: `Toy_ink` — two 1.10 x 2.60 m platforms at z=5.7 and z=11.0,
    0.90 m proud, joined by a diagonal stair, with a 1.0 m rail; a drop ladder below the
    lower platform.
11. **North-east elevation.** `Toy_sand`, blank except three small `Toy_glass` windows
    1.0 x 1.0 m at z=9.5 spread across the length, and one `Toy_ink` service door at the
    south-east end.
12. **North-west party wall.** `Toy_sand`, entirely blank. A 0.06 m `Toy_stone` reveal at
    z=11.9 marks where the neighbour's roof meets it — the only articulation.
13. **Roof furniture.**
    - **Monitor spine:** three raised glazed monitors, each 7.0 x 1.9 m in plan and 1.05 m
      tall, running parallel to the long axis, staggered along a line that drifts about
      4 m across the roof from the north-west end to the south-east. `Toy_white` kerbs and
      cheeks, `Toy_glassl` glazed tops, each divided by four `Toy_white` mullions 0.10 m
      wide.
    - **Skylights:** seven `Toy_glassl` domes on `Toy_white` kerbs, 1.6 x 1.6 m x 0.45 m,
      scattered — four on the Zoe half, three on the rear half, none within 1.5 m of the
      parapet.
    - **Penthouse:** 8.0 x 6.0 m block at the south-east end, z=13.60 to **z=17.00**,
      `Toy_white` walls with a `Toy_steel` cap, and a `Toy_steel` cylindrical vent 1.2 m
      diameter x 0.55 m tall on top, set off-centre. One `Toy_ink` door on its north-west
      face.
    - **Roof deck:** a 8.0 x 4.5 m `Toy_stone` paved rectangle at the north-west end,
      enclosed on its roof-facing sides by a 1.10 m `Toy_white` wall, with a 0.9 x 2.0 m
      `Toy_ink` stair hatch against the party-wall parapet.
    - **Vent cans:** six `Toy_steel` cylinders 0.35 m diameter x 0.50 m, in two loose
      clusters flanking the monitor spine.

Nothing on this roof except the penthouse and the monitor spine should exceed 1.1 m above
the deck — the parapet is only 0.80 m and anything taller breaks the silhouette for no
gain.

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_white` | `#f7f4ec` | the lightest stripe; parapet coping; window frames; monitor kerbs and mullions; skylight kerbs; the penthouse walls; the roof-deck wall |
| `Toy_trim` | `#f3efe6` | the second-lightest stripe |
| `Toy_sand` | `#ece4d4` | the warm pale stripe; **the three non-street elevations** and the body wall behind the stripes |
| `Toy_stone` | `#d9d2c2` | the split-face CMU base; the party-wall reveal; the roof-deck paving |
| `Toy_verdigris` | `#9fb8a8` | the sage-grey stripe — the one tone with any hue in it |
| `Toy_steel` | `#9aa0a6` | the blue-grey stripe; the roof membrane; the roll-up doors; the juliet rails; the entry awning; the penthouse cap; the vent cans |
| `Toy_glass` | `#2a4d73` | all loft glazing and the punched windows on the side elevations |
| `Toy_glassl` | `#6f95b8` | the monitor glazing and the skylight domes |
| `Toy_ink` | `#3a3530` | the fire escape, the pedestrian and service doors, the stair hatch, door-head and awning-underside reveals, base louvres |
| `Toy_glass_Glow` | `#2a4d73` | the lit loft windows (night) |
| `Toy_glassl_Glow` | `#6f95b8` | **the lit monitor spine** — the night hero |
| `Toy_gold_Glow` | `#caa64a` | two warm-lit loft windows and the strip over the pedestrian entry |

**Note on the stripe tones.** The six-tone set above (`white`, `trim`, `sand`, `stone`,
`verdigris`, `steel`) spans `#f7f4ec` down to `#9aa0a6` — a wide enough value range to
survive the app's flatter lighting, which is the actual risk on an all-pale building. Use
`Toy_trim` sparingly: it is only 4 units from `Toy_white` and two adjacent bands of them
will read as one. `Toy_verdigris` is the only stripe with a hue and should appear three or
four times at most — the real facade's sage panels are a minority accent, and
over-using them turns a neutral building green.

**Note on the roof membrane.** `Toy_steel` (mid grey), not `Toy_roofd` (near-black).
`Toy_roofd` renders as rgb(9,9,12) under the app's lighting — a dark deck here would be
both untrue (the aerial shows a genuinely pale grey membrane) and would kill the white
monitor kerbs and coping ring that make the roof read. Record the choice in `REPORT.md`.

**Night state (required).** Glow surfaces must be thin shells proud of the opaque surface
behind them — the app renders `_Glow` in a separate layer at roughly 12% alpha per layer
by day, so a closed shell reads at about 23% and a primary surface must never be authored
as glow. A `_Glow` material's **base colour is its night appearance**; do not judge it
from a Blender emission render.

- **Hero: the monitor spine, lit end to end** in `Toy_glassl_Glow`. The internal
  circulation of a 16-unit building is on all night, and three glowing ridges down the
  middle of a dark roof is an image no other asset in this district gives the aerial
  camera. This is the reason to build the monitors properly.
- **Supporting:** an uneven residential scatter — six of the sixteen loft windows on the
  Zoe elevation lit, four in `Toy_glass_Glow` and two in `Toy_gold_Glow`, deliberately
  asymmetric across bays and tiers (never a full row, never a full bay), plus a small
  warm `Toy_gold_Glow` strip under the entry awning.
- The stripes, the CMU base, the roll-up doors, the roof deck and the three non-street
  elevations do **not** glow.

### 2.9 Top surface

558 m2 of roof at 14.4 m, under a camera that spends most of its time above it, on a
building with only one street-visible elevation. The roof is not a finishing touch here;
it is half the asset.

The composition is: a white coping ring; a pale grey field; **the monitor spine as a
single strong diagonal-ish gesture down the middle**, splitting the field into a Zoe half
and a rear half; a skylight scatter that is deliberately *denser on the Zoe half*; the
penthouse anchoring the south-east end; and the walled deck anchoring the north-west end.
The two ends are therefore weighted and the middle carries the one linear event — that is
what stops it reading as sprinkled.

Keep a genuinely **empty quarter** in the rear half towards the north-west. The contrast
between the busy spine and one clear field is what makes the roof read as designed.

### 2.10 Scope

**In the GLB:** the single 1996–97 building as re-clad in 2013 — body, CMU base and its
doors, the entry recess and awning, all four elevations, the stripe cladding, windows and
juliet rails, the south-east fire escape, the parapet, the roof and all its furniture.

**Not in the GLB:** Zoe Street, the surface parking lot to the south-east, 33–35 Zoe,
25 Zoe, 52 Zoe, 226 and 248–254 Ritch, the two street trees on the frontage, the utility
poles and the overhead wires that cross every photograph, the sidewalk and its planters,
the estate-agent sign, parked cars, people, plinths, cameras or lights.

### 2.11 Triangle budget

Cap **11,000** — above 340 Brannan's 8,871 because the stripe cladding and the monitor
spine each cost real geometry, below 300 Brannan's 15,000 because the massing is one box
with no canted corner. Suggested split: body, parapet and roof deck ~1.0k; stripe
cladding ~1.8k; Zoe openings (16 glazed units, 8 rails, frames) ~3.0k; CMU base, doors,
entry and awning ~1.4k; three side elevations, punched windows and fire escape ~1.3k;
roof furniture (monitors, skylights, penthouse, deck, vents) ~2.0k; margin ~0.5k.

### 2.12 Draft manifest entry

```json
{
  "id": "49-zoe",
  "file": "49-zoe.glb",
  "anchor": [
    -122.3960338,
    37.7800764
  ],
  "targetHeightM": 17.0,
  "cat": 2,
  "name": "49 Zoe Street",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

`loadRadius` follows the default rule `max(2500, targetHeightM × 30)` = `max(2500, 510)`
= **2500**. Not `alwaysLoaded`: at 17 m this is neighbourhood fabric, not a skyline piece.

`estimated: false` — the anchor is surveyed, the plan dimensions are surveyed, and the
height is LiDAR-derived rather than guessed.

### 2.13 Integration notes (for later, not this task)

**Case B.** There is no `49-zoe` id in `pipeline/lib/landmarks.mjs` or
`app/src/landmarks.js`, so integration needs a registry entry *and* a tile re-bake, per
`docs/asset-plans/INTEGRATION-PROMPT.md`.

Registry entry (id follows the `550Third` / `318Brannan` / `49SouthPark` convention):

```js
{
  id: '49Zoe',
  name: '49 Zoe Street',
  lon: -122.3960338,
  lat: 37.7800764,
  height: 17.0,
  exclude: 9.5,
  camera: { distance: 180, yaw: 338, pitch: 28 },
}
```

**The exclusion radius must be measured, not reasoned about** — follow
`sf3d-exclusion-radius` / the procedure in `INTEGRATION-PROMPT.md`: stream the real bake
inputs (`pipeline/data/buildings_datasf.geojson` **and** the Overture file — the binding
neighbour is frequently Overture's, not DataSF's), and for each candidate radius count
the rings satisfying `nearestVertex < r || centroid < r`. Then pick the middle of the band
that drops exactly one.

**MEASURED at integration, 2026-08-18 — and the prediction below was wrong, so read
the correction first.** The band is `(5.37, 14.28]`, 8.9 m wide, and **`exclude: 9.5`
shipped**. Full table in `pipeline/lib/landmarks.mjs` next to the `49Zoe` entry and in
`artifacts/49-zoe/REPORT.md`.

*The prediction this section originally carried, kept because the error is instructive:*

| Ring | nearest vertex **to our footprint** | centroid distance from anchor |
|---|---|---|
| our own `SF3776128` | — | ~1.3 m |
| `SF3776144` (33–35 Zoe, **party wall**) | **0.00 m** | 20.7 m |
| `SF3776105` (Ritch St, rear) | 2.41 m | 29.4 m |
| `SF3776456` (Ritch St, rear) | 2.69 m | 23.6 m |

From that table this section concluded that the party wall touching at 0.00 m was a hard
constraint and that the site might be an unavoidable-collateral case
(`sf3d-exclusion-unavoidable-collateral`, `sf3d-exclusion-two-rings`). **It is not.**
`excluded()` measures every distance from the landmark's **anchor**, not from this
building's footprint, and 33–35 Zoe's nearest vertex *to the anchor* is 14.28 m. The
column above answers a question the bake never asks. The real numbers, from the actual
bake inputs including Overture:

| Ring | nearest vertex to anchor | centroid to anchor | gate |
|---|---|---|---|
| `SF3776128` (this building) | 14.13 | 0.11 | **0.11** |
| Overture twin (this building) | 15.94 | 5.37 | **5.37** ← floor |
| `SF3776144` (33–35 Zoe, party wall) | 14.28 | 21.87 | **14.28** ← ceiling |
| `SF3776144` (second ring) | 14.29 | 19.37 | 14.29 |
| Overture (33–35 Zoe) | 14.39 | 26.52 | 14.39 |
| `SF3776456` (Ritch St, rear) | 14.92 | 24.17 | 14.92 |
| `SF3776105` (Ritch St, rear) | 15.51 | 30.26 | 15.51 |

The floor is this building's own **Overture** centroid, not its DataSF one: an excluded
DataSF ring never calls `markOccupied()`, so the Overture gap-fill would re-add the
building on top of the asset. No anchor offset was needed.

Because this landmark is being built in a batch, stage 5 runs in **batch mode**: run the
re-bake and do the full QA on it, then `git checkout -- app/public/tiles api/_data`
before committing, and ship a source-only branch. `git diff --name-only origin/main` must
list nothing under `app/public/tiles/` or `api/_data/`.

### 2.14 Validation checklist

- [ ] `min_z` ≈ 0, XY centre ≈ (0, 0)
- [ ] Tallest geometry (penthouse cap) at exactly 17.00 m
- [ ] Parapet top at 14.40 m; roof deck at 13.60 m
- [ ] XY bounding box ≈ 33.8 x 34.1 m (the 45° heading, not a scale error)
- [ ] Zoe elevation normal 225.4°; rear 45.2°; parking-lot 134.8°; party wall 315.0°
- [ ] ≤ 11,000 triangles
- [ ] All materials `Toy_*`, no textures, no transparency, no `Toy_body`
- [ ] `_Glow` shells proud of their opaque backing, never a primary surface
- [ ] No cameras, lights, animations, armatures, constraints or foreign geometry
- [ ] Transforms applied, no negative scales, normals outward (per-object signed volume
      authoritative for the union of solids; ray test ≤ 0.15% residual)
- [ ] Aerial day render checked for the pale-on-pale failure mode before sign-off
- [ ] Aerial night render shows the monitor spine as the dominant light

### 2.15 Open questions and risks

1. **No architect of record.** Two plausible-looking attributions are both wrong and both
   are one search away. *Kaplan Architects* appears at "49 Zoe St, Suite 10" in the SF
   business registry (location start 1997-06-01) and on LinkedIn — it is a two-person
   residential practice **occupying a unit**, exactly what a live/work building is for.
   *Santos Prescott and Associates* really did build a Zoe Street live/work loft in 1998,
   but it is 33–35 Zoe (the "Ritch / Zoe Studio", client Adele Santos, `mapblklot`
   3776144), our party-wall neighbour, and the Curbed piece about a $1.95M concrete loft
   with 20-foot ceilings is about *that* building. Leave 49 Zoe unattributed unless a
   primary permit document says otherwise.

2. **Whose roof deck?** The aerial shows a walled, paved area with furniture at the
   north-west end of the block, straddling the party-wall line to within the accuracy of
   the imagery. Two readings are consistent with the pixels: (a) it is 49 Zoe's common
   roof deck, which the Unit 6 listing independently proves exists; (b) it is the *central
   courtyard* that Santos Prescott describe carving out of 33–35 Zoe. Relief displacement
   cannot separate them here because our roof (14.4 m) and the neighbour's (10.8–11.9 m)
   are displaced by different amounts in a view that is ~8–19° off nadir. The plan places
   a modest 8.0 x 4.5 m deck at that end because the listing evidence for *a* deck is
   direct; **the position is inferred and should be re-checked** against any listing
   photograph of the roof deck, which would settle it in one image.

3. **Bay widths and stripe rhythm are the weakest measured numbers.** Two street trees
   stand in front of bays 2 and 3 in the only available panorama, and the stripe widths
   were read from a rectification with a 0.35 m rms residual. The four-bay module is
   solid (it is corroborated by the assessor's eight-units-per-tier fingerprint, four
   fronting Zoe and four to the rear). The individual widths are not. Re-count them from
   any newer Street View capture before committing the cladding.

4. **The `hgt_max` attribution is inference, not measurement.** 16.99 m is certainly a
   real return on the footprint and the aerial certainly shows a penthouse; that the two
   are the same object is inferred. If a later capture shows the penthouse is shorter,
   the correct fix is to lower the penthouse and re-normalise, **not** to change the
   14.4 m roof plane, which is the best-supported number in this dossier.

5. **Only one elevation is street-visible.** The north-east and south-east faces are
   described from oblique satellite pixels at ~0.02 m/px, which is enough for "blank wall
   with small punched windows" and not enough for their positions. They are labelled
   *inferred* in 2.7 and must be labelled *inferred* in `REPORT.md` too. The fire escape
   is the exception — the permit is documentary, though the permit's word "east" has been
   interpreted as the south-east face on the grounds that a fire escape must discharge to
   the open parking lot rather than into a 2.5 m light gap.

6. **The 2013 re-clad means old photographs are a different building.** Anything from
   before mid-2013 shows the original 1997 exterior. Date every reference before using it.
