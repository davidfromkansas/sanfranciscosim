# 250 Van Ness Avenue (171–195 Grove Street) — SF-SIM asset plan

A two-storey 1913 commercial block holding the south-east corner of Van Ness and
Grove, one intersection west of City Hall. Architecturally it is the quietest
building for three blocks: a plain stuccoed box with a punched window grid, a
belt cornice and a capped parapet. What makes it unmistakable is paint — the
**entire ground floor is a saturated ultramarine blue** that wraps the corner and
runs the full length of both street frontages, the only saturated base plane in
a Civic Center made of cream granite. From the app's aerial camera it reads as a
short blue dash at the corner of the City Hall block.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/250-van-ness/`. This document is the plan only: Part 1 is the runnable
task prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `250-van-ness` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.4194756, 37.7781332` (footprint AABB centre = centroid, measured) |
| Target height | **10.0 m** (parapet cap; LiDAR roof deck 9.32 m measured, parapet *estimated*) |
| OSM footprint | 32.07 x 14.51 m rectangle on the 80.3 deg Civic Center grid, 465 m2 (OSM way/35176289, measured) |
| Triangle cap | 9,000 |
| Category | `3` (Office) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 250 Van Ness Avenue GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of 250 Van Ness Avenue (the two-storey
corner block at Van Ness and Grove, addressed 171–195 Grove Street on its long
side) and deliver it as a downloadable, validated GLB.

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
8. `artifacts/101-grove/` — the closest sibling: the same block (811), the same
   street corner grid, the same stone/trim palette spine. This asset is the
   *quiet* member of that family: share its `Toy_stone` body and `Toy_trim`
   horizontals so the two read as neighbours, and let the blue base be the only
   thing that differs loudly.
9. `artifacts/380-brannan/` — the closest sibling by *scale*: a small
   flat-roofed commercial block that shipped at 7,760 triangles. That is the
   budget this building deserves, not a landmark budget.
10. `docs/asset-plans/250-van-ness.md` — this plan, whose dossier is your
    research starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Must capture

- The **ultramarine ground-floor band**, unbroken from sidewalk to belt cornice,
  wrapping the Van Ness corner and running the full Grove and Van Ness
  frontages. This is the whole identity of the building; everything else is
  background architecture.
- The **two clean horizontals**: a projecting belt cornice at the top of the
  blue band (the storefront cornice) and a plain capped parapet at 10 m. Between
  them, one storey of flat cream stucco.
- The **square, unchamfered corner** — a sharp vertical arris at Van Ness and
  Grove, no corner bay, no entrance splay. That bluntness is what makes it
  different from 101 Grove at the other end of the block.
- The **punched upper-window grid**: plain rectangular openings on a regular
  bay rhythm, with a single **round-arched head** on the westernmost Grove bay.
- The **bright white cool-roof membrane** inside the parapet, with three small
  tight clusters of rooftop plant and a roof hatch — nothing breaking the
  parapet line.
- The plainer **south and east elevations**, which are party/back walls against
  the neighbouring lots and carry no ornament.

## Research 250 Van Ness Avenue independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- North (Grove Street) and west (Van Ness Avenue) elevations — the two public
  faces. Both are heavily overhung by mature street trees in every aerial and in
  most street-level imagery; look for winter/leaf-off photography.
- The corner itself, and the exact extent of the blue band.
- **The upper-floor window pattern and bay count, which this dossier only
  estimates.** No unobstructed elevation photograph was located. §2.4 reasons
  from partial street-level views.
- **South and east elevations, which this dossier only infers.** They are party
  walls against lots 019 and the block interior; if they are visible at all it
  will be from the block-interior parking area.
- Aerial and roof views.
- Ground-level views, day and night.
- **The crest height, which this dossier estimates at 10.0 m.** The roof deck at
  9.32 m is measured (2010 city LiDAR modal height); the parapet above it is
  inferred, and OSM's `height=10` agrees with the sum. Overture — the pipeline's
  own bake input — carries **12.4 m** for this footprint and is the one source
  that disagrees; §2.1 and §2.15 explain why it is read as a LiDAR-max artefact
  and not as the architectural crest. Record eave and crest separately in
  `REPORT.md`, and if a measured elevation turns up, use it and re-normalize.
- **The provenance and exact colour of the blue.** It is present in Street View
  imagery across multiple years, so it is the building's colour rather than
  fresh graffiti, but no source naming its origin was located. Sample the hue
  from the best available photograph rather than trusting §2.8's estimate.
- Publicly available drawings, plans, or diagrams — in particular the 2010 SF
  Planning "Van Ness Auto Row Support Structures" survey, which covers 1910s
  commercial buildings on this stretch and may contain a DPR form for this
  parcel (the copy at `default.sfplanning.org` is a scan whose text layer did
  not extract; try OCR or the SF Planning Property Information Map).

Prefer architect/engineer publications, owner or institutional material,
planning and permitting documents, architectural press, geolocated photography,
and aerial/satellite imagery. Never rely on a single photograph, a single
AI-generated image, or a single unsourced 3D model. Separate verified facts from
visual inference; if sources disagree, document the disagreement and decide.

## Create a reference dossier

Write `artifacts/250-van-ness/REFERENCE.md` containing: source links and what
each establishes; verified dimensions and location; orientation; observations
from all four sides and above; the 3-5 strongest recognition cues; features to
preserve; features to simplify; uncertainties and conflicting evidence. A
contact sheet of attributed reference thumbnails is welcome if legally
permissible — do not commit copyrighted full-resolution imagery.

## Make your own design decisions

Follow the conversion process in `docs/styles/miniature-toy.md` §22: identify the
recognition cues, strip nonessential information, rebuild the massing from a few
confident volumes, exaggerate only the signature features, simplify the facade
into broad rhythms, deliberately design every surface visible from above,
evaluate from the app's high three-quarter aerial camera, then simplify again.

This is a **background building with one saturated colour move**. §5 (facade
rhythm), §7 (neutral architecture + saturated accent) and §24 (structure
families) govern here; §11 (landmark geometry) does not — there is no landmark
geometry to design, and inventing some would be a lie about a real building
(AGENTS rule 5). Spend the budget on: the blue band and its two bounding
horizontals, the window grid, and the roof. Resist modelling storefront
mullions, stucco texture, downpipes, or the paint splatters on the blue.

**One deliberate deviation from the reference, to be recorded in `REPORT.md`:**
the building is currently vacant and its upper-floor windows are boarded with
brown plywood. Model them as the project's standard dark blue-grey graphical
windows, not as boards. `docs/styles/miniature-toy.md` §6 puts decay out of
scope by default, and boarded windows would make this the only derelict-looking
building in the city. The blue stays — it is paint, not decay, and it is the
reason this asset exists.

The finished asset must be immediately recognizable as 250 Van Ness Avenue,
consistent with the real building from all four sides and above, architecturally
credible, and a premium handcrafted miniature — not photorealistic, not voxel
art, not generic low-poly, and never accurate in one view while invented in the
others.

## Scope of the exported asset

Export the 250 Van Ness building itself, including its blue base band, belt
cornice, upper window grid, parapet, roof membrane and rooftop plant.

Do not include unrelated surrounding city geometry: Van Ness Avenue, Grove
Street, the Van Ness BRT median and stations, City Hall, Civic Center Plaza, the
Bowes Center, the neighbouring buildings on lots 018/019, sidewalks, street
trees, traffic signals, trolley wire, parked cars, people, plinths, cameras or
lights. Temporary context may appear in review renders but must not leak into
the GLB.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary
`.glb`; real-world meters; origin at base center; minimum geometry Z ~ 0;
applied transforms; no negative scales; outward normals; no duplicate or foreign
geometry; no image textures; no transparency; flat-color materials named `Toy_*`
from the project palette; `_Glow` suffix only on surfaces that glow at night; no
`Toy_body`; no cameras, lights, animations, armatures or constraints; no external
dependencies; at most 9,000 triangles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model
drops into the city at its real-world heading — the loader applies no rotation
(`placeGeneric` in `app/src/assets.js` only scales and positions). The Grove
front faces north (outward normal 350.3 deg true) and the Van Ness front faces
west (260.2 deg true), so the contract's "front faces −Y" cannot be honoured
literally. Real-world orientation wins (AGENTS rule 5). Record the decision and
the measured heading in `REPORT.md`.

**Height normalization:** make the exported bounding-box top land exactly on the
verified architectural height, so the loader's `targetHeightM / measuredHeight`
scale is 1.0. Every rooftop object must stay **below** the parapet cap — that is
both true to the building (nothing breaks its silhouette) and what keeps the
normalization honest.

## Reproducible Blender workflow

Blender 4.5 LTS or newer, headless only: `blender -b --python script.py -- args`;
no GPU, so use Workbench or CPU Cycles.

Keep `artifacts/250-van-ness/build_250_van_ness.py` (deterministic build script),
`artifacts/250-van-ness/250-van-ness.blend`, and
`artifacts/250-van-ness/250-van-ness.glb`. The script must rebuild the model
reliably enough for future revision. Do not modify or rename an unrelated
existing GLB to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`250-van-ness-top.png`, `250-van-ness-north.png`, `250-van-ness-east.png`,
`250-van-ness-south.png`, `250-van-ness-west.png`, plus
`250-van-ness-contact-sheet.png`, at least one high three-quarter aerial beauty
render `250-van-ness-aerial.png`, and a night render `250-van-ness-night.png`.

The four elevations must share scale, framing, lighting, exposure and
projection; use orthographic or long-lens cameras; label directions from the
researched orientation; **the aerial is the hero image for this asset** and must
be framed off the north-west so the Grove elevation, the Van Ness elevation and
the corner all read in one frame, with the white roof visible; the aerial view
uses the style bible's camera assumptions (30-50 degrees down, long lens). Simple
tabletop lighting, neutral warm background, minimal depth of field, and every
image must depict the same exported model.

Drive `_Glow` night renders from Base Color, not from the imported emission —
see the note at the end of `docs/asset-plans/README.md`.

## Validate the exported GLB

Re-import `250-van-ness.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture
count, camera count, light count, animation count, applied-transform status,
negative-scale status, normal-orientation status, unexpected geometry, and
per-material contract compliance. Normals are checked two ways: per-object signed
volume (authoritative for a union of closed solids) and a deterministic
visibility-ray test (≤ 0.15% residual, zero for single shells). Render at least
one review image from the re-imported asset. Write
`artifacts/250-van-ness/validation.json` and `artifacts/250-van-ness/REPORT.md`.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "250-van-ness",
  "file": "250-van-ness.glb",
  "anchor": [
    -122.4194756,
    37.7781332
  ],
  "targetHeightM": 10.0,
  "cat": 3,
  "name": "250 Van Ness Avenue",
  "estimated": true,
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
for that, together with the integration notes in
`docs/asset-plans/250-van-ness.md`.
````

---

## Part 2 — Research and design dossier

Compiled 13 August 2026 from the sources in 2.2. Values marked *inferred* or
*estimated* are visual or derived, not published figures — the executing agent
must re-verify anything it relies on.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Address | 250 Van Ness Avenue, San Francisco, CA 94102; the same building is addressed 171–195 Grove Street on its long frontage | DataSF EAS address point 460243-681009-506985; Assessor `property_location` "0195 0171 GROVE ST" |
| Parcel | Block 0811, Lot 020 (MBLR `SF0811020`, APN 0811020) | DataSF EAS + Assessor secured roll (measured) |
| Built | **1913** | SF Planning Historic Resources layer (`YearBuilt` 1913) and Assessor `year_property_built` 1913, independently |
| Storeys | 2 | Assessor secured roll |
| Use | Commercial Office (`COMO`), C3-G zoning; building area 9,450 sq ft on a 4,721 sq ft lot | Assessor secured roll |
| Historic name | "CHURCH OF CHRIST" | SF Planning Historic Resources layer, `buildingname` for 171 Grove |
| Historic status | CEQA code **A** (historic resource present), `ceqacodea10a11` "A*"; inside the Article 10 **Civic Center Historic District** (Ord. 413-94, period of significance 1913–1951, 23 contributors / 23 non-contributors) | SF Planning PlanningData layers 0 and 17 |
| Survey rating | **D — "Minor Or No Importance"**, Foundation for SF Architectural Heritage survey (evaluated 1978) | SF Planning Historic Survey Ratings layer, APN 0811020 |
| Architect | not located | — |
| Footprint | 32.07 x 14.51 m rectangle, 465 m2, long axis 80.3 deg / 260.3 deg true (the Civic Center grid); OBB fill 99.9% | OSM way/35176289, reprojected + oriented bbox (measured) |
| Roof deck | **9.32 m** above grade (modal), 9.71 m median, 9.75 m mean over 1,719 half-metre cells | SF 2010 LiDAR `SF0811020` (measured) |
| Crest (parapet cap) | **10.0 m** | roof deck 9.32 m + a parapet read at ~0.7 m from photo proportion (*estimated*); OSM `height=10` agrees independently |
| LiDAR max return | 13.03 m; LiDAR min return 2.52 m | measured — both are almost certainly street-tree canopy overhanging the footprint, not building (see 2.15) |
| Overture / bake height | 12.4 m on a 427 m2 footprint | read from the committed tile `app/public/tiles/buildings/19_14.bin` (measured) — **the procedural block is 2.4 m taller than this asset**, so the exclusion is what makes the GLB visible at all |
| Ground slope | site falls ~2.15 m across the footprint (LiDAR `gnd_mincm` 1674 → `gnd_maxcm` 1889) | measured — the app seats the asset on `sampleElevation`, so this is context, not model geometry |
| Anchor | -122.4194756, 37.7781332 | footprint AABB centre; the polygon centroid lands on the same point to 7 decimal places (measured) |
| Current occupancy | vacant / boarded. Registered businesses at this address: 42nd St Moon (theatre company, 1993–present) and Theatre Rhinoceros (2017–2022) | DataSF registered business locations |
| Neighbourhood | Civic Center / Tenderloin, Supervisorial District 5; one block west of City Hall, across Van Ness from the War Memorial complex | DataSF |

### 2.2 Sources

- https://www.openstreetmap.org/way/35176289 — footprint geometry, `building=commercial`, `height=10`
- https://api.openstreetmap.org/api/0.6/way/35176289/full.json — the node geometry actually used for §2.3
- https://data.sfgov.org/resource/ramy-di5m.json — DataSF Enterprise Addressing System: "250 VAN NESS AVE" → parcel 0811020, -122.419614 / 37.778059
- https://data.sfgov.org/resource/ynuv-fyni.json — SF 2010 LiDAR building footprints, record `SF0811020`: 1,719 half-metre cells, ground min 16.74 m, height modal 9.32 m, height median 9.71 m, height max 13.03 m
- https://data.sfgov.org/resource/wv5m-vpq2.json — Assessor secured roll 2025, parcel 0811020: "0195 0171 GROVE ST", Commercial Office, built 1913, 2 storeys, 9,450 sq ft on 4,721 sq ft
- https://data.sfgov.org/resource/g8m3-pdis.json — registered business locations at 250 Van Ness Ave
- https://sfplanninggis.org/arcgiswa/rest/services/PlanningData/MapServer/0 — SF Planning Historic Resources: `mapblklot` 0811020, `YearBuilt` 1913, `buildingname` "CHURCH OF CHRIST", CEQA code A
- https://sfplanninggis.org/arcgiswa/rest/services/PlanningData/MapServer/30 — Historic Survey Ratings: APN 0811020, Heritage rating D, "Minor Or No Importance"
- https://sfplanninggis.org/arcgiswa/rest/services/PlanningData/MapServer/17 — Article 10 Historic Districts: Civic Center Historic District, Ord. 413-94
- https://codelibrary.amlegal.com/codes/san_francisco/latest/sf_planning/0-0-0-28483#JD_Article10AppendixJ — Article 10 Appendix J, the district's designating text
- Esri World Imagery (ArcGIS `World_Imagery` export service) — overhead orthoimagery at the parcel; the basis of §2.9's roof description, checked against the OSM polygon by overlay
- Google Street View, panoramas dated May 2025 (Van Ness at Grove, looking ESE) and an earlier leaf-off pass on Grove — the only usable elevation imagery located; the basis of §2.4. **Not committable**: describe what it shows, do not copy the images into the repo.
- https://default.sfplanning.org/DPRforms/Van%20Ness%20Auto%20Row%20Context%20revised%20June%202010.pdf — SF Planning, "Van Ness Auto Row Support Structures", June 2010. Located but **not read**: the PDF is a scan with no extractable text layer. Worth OCR by the executing agent; it is the most likely single source for this building's original use and architect.
- `app/public/tiles/buildings/19_14.bin` in this repo — the committed bake, read directly for §2.13's exclusion measurements

### 2.3 Orientation and placement

The south-east corner of Van Ness Avenue and Grove Street: **Grove along the
north** (32 m, the long frontage), **Van Ness along the west** (14.5 m, the short
frontage and the numbered address), a party wall south against lot 019 and a back
wall east into the block interior. The Civic Center grid is rotated ~9.7 deg from
cardinal: Grove runs 80.3 deg / 260.3 deg true.

Measured footprint, reprojected with the app's tangent projection (LON0
-122.4375, LAT0 37.77) and recentred on the footprint AABB centre (x east,
y north, metres, **CCW**):

```
(-14.57,  -9.84)   P0  south-west corner (Van Ness / party line)
( 17.04,  -4.45)   P1  south-east corner (block interior)
( 14.56,   9.84)   P2  north-east corner (Grove / block interior)
(-17.04,   4.44)   P3  north-west corner (Van Ness / Grove) — the corner
```

| Edge | Length | Outward normal (true) | What it is |
|---|---|---|---|
| P2 → P3 | 32.06 m | 350.3 deg (N) | **Grove Street front** — the long public face |
| P3 → P0 | 14.49 m | 260.2 deg (W) | **Van Ness Avenue front** — the address face |
| P0 → P1 | 32.07 m | 170.3 deg (S) | party wall against lot 019 |
| P1 → P2 | 14.51 m | 80.2 deg (E) | back wall into the block interior |

Author `+Y` = north and place the polygon exactly as measured. The contract's
"front faces −Y" cannot be met — the two public faces are north and west — so
real-world orientation wins per the README orientation note and AGENTS rule 5.

Note that the corner P3 is a true 90-degree-ish arris, not a chamfer: the OSM
polygon has exactly four vertices and the street-level imagery confirms a sharp
vertical corner with the blue band turning it unbroken.

### 2.4 What each side shows

*All four descriptions below come from partial street-level views; mature London
plane trees overhang both public frontages in every image located, so no
unobstructed elevation was available. Bay counts in particular are proportional
fits, not counts off a photograph.*

**North (Grove Street) — the long public face, 32.1 m.** Two storeys. The whole
ground floor, from sidewalk to belt cornice at ~4.9 m, is **saturated
ultramarine blue** — a flat painted plane broken only by storefront openings:
large display windows near the corner (their glass backed with cream boards and
taped notices), a dark recessed entrance roughly a third of the way along, and
further openings east of it. Lighter blue drips and splashes run down the band
in the 2025 imagery; they are sub-pixel at the app's camera and are not
modelled. Above the belt cornice, one storey of flat warm off-white stucco
carrying a regular grid of plain rectangular windows, presently boarded with
brown plywood. The **westernmost upper bay has a round-arched head** — the one
piece of architectural incident on the building. The wall terminates in a modest
projecting cornice and a plain capped parapet at 10 m. No pilasters, no
rustication, no ornament.

**West (Van Ness Avenue) — the address face, 14.5 m.** The same two-part order,
just short: blue base with a doorway and a blank painted panel, belt cornice,
three upper bays of plain rectangular windows in cream stucco, cornice, parapet.
The blue band turns the corner without a break or a change of plane, which is
what makes the corner read as one object rather than two facades.

**South, 32.1 m.** *Inferred — not visible.* A party wall against the
neighbouring building on lot 019, which is of the same era and roughly the same
height (LiDAR median 10.27 m). Model it as plain stucco with no openings and no
cornice return; nothing of it is ever seen.

**East, 14.5 m.** *Inferred.* A back wall onto the block interior — from the
orthoimagery, a paved service/parking area. Plain stucco, a couple of small
punched openings at most, plain parapet.

**Top.** See 2.9.

### 2.5 Recognition cues (ranked)

1. **The ultramarine ground-floor band wrapping the corner.** Civic Center is
   cream, granite and grey; this is the only saturated base plane in it. At the
   app's aerial camera the building is legible as a blue dash at the Van Ness /
   Grove corner before any of its architecture resolves.
2. **Its shortness.** Two storeys and 10 m, diagonally opposite a 14-storey
   apartment tower and one block from a 94 m City Hall dome. The silhouette gap
   in the block is the second cue.
3. **The two horizontals** — belt cornice at ~5 m and capped parapet at 10 m —
   splitting the elevation almost exactly in half, blue below, cream above.
4. **The square corner.** No chamfer, no corner entrance, no splay: a blunt
   arris where 101 Grove at the far end of the same block has a full ceremonial
   corner bay.
5. **The white roof** inside a cream parapet frame, with three tight clusters of
   plant — what the camera actually sees most of.

### 2.6 Miniature translation

**Preserve**

- The true 32.07 x 14.51 m footprint and its 80.3 deg heading
- The near-50/50 vertical split: blue base 0 → 4.90, belt cornice to 5.25,
  cream upper 5.25 → 9.30, cornice to 9.75, parapet cap to **10.00**
- The blue band as one unbroken plane turning the corner — never two
  differently-toned faces
- The single arched upper bay at the west end of Grove
- The white roof membrane and its parapet frame

**Simplify / exaggerate**

- Storefront mullions, transoms, taped notices, downpipes, meter boxes, the
  paint splatters and the security roll-gate: **removed**
- Boarded plywood windows become the project's standard `Toy_glass` graphical
  windows (see the deviation note in Part 1)
- The blue is pushed slightly toward pure ultramarine and kept perfectly flat —
  it is the identity, and §7 of the style bible earns it its saturation
- Windows become a `Toy_ink` reveal plate with a `Toy_glass` slab proud of it,
  one per bay per floor; the arched bay gets a semicircular head, everything
  else is rectangular
- The belt cornice becomes one clean beveled band proud 0.30 m; the top cornice
  one band proud 0.22 m with a flat cap — two horizontals, not five mouldings
- Storefront openings become `Toy_ink` reveals with `Toy_cream` display panels;
  the recessed entrance is one 0.35 m recess, not a modelled vestibule
- South and east walls get the same stucco and parapet, no openings, no cornice

**Do not add** a corner tower, a pediment, signage, a cupola, a roof deck, or
any silhouette event. This building's job in the scene is to be the small blue
thing that makes City Hall look enormous.

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not
a straitjacket — adjust after the first aerial review render.

1. **Body:** extrude the measured footprint from z=0 to z=9.30, `Toy_stone`.
2. **Blue base:** a `Toy_ultramarine` ring band from z=0 to z=4.90 on the north
   and west faces only, proud 0.06 m of the body face; carry it around the P3
   corner as one continuous surface. South and east stay `Toy_stone` to grade.
3. **Belt cornice:** `Toy_trim` ring band z=4.90 → 5.25, proud 0.30 m, beveled;
   returns on all four faces so the roof reads as one object from above.
4. **Top cornice:** `Toy_trim` ring band z=9.30 → 9.75, proud 0.22 m, beveled.
5. **Parapet cap:** `Toy_trim` ring z=9.75 → **10.00**, proud 0.30 m, flat top —
   the crest, and the highest geometry in the file.
6. **Upper window grid:** bays at ~4.0 m pitch — **7 on Grove, 3 on Van Ness**,
   none on the south or east. Per bay: `Toy_ink` reveal 1.55 x 2.40 m proud
   0.04 m, `Toy_glass` slab inset 0.10 m and proud 0.10 m. Band 6.20 → 8.60.
7. **Arched bay:** the westernmost Grove bay gets a semicircular head of radius
   0.775 m on the same reveal, raising its head to 9.05 — 24 segments is
   plenty; do not smooth-shade it.
8. **Storefront openings:** in the blue band, 5 on Grove and 2 on Van Ness,
   `Toy_ink` reveals 3.20 x 2.70 m (sill 1.10, head 3.80) with a `Toy_cream`
   display panel inset 0.12 m. One of the Grove bays, the third from the corner,
   becomes a **recessed entrance**: the same reveal taken to grade and pushed
   0.35 m into the wall, with a `Toy_ink` door plane.
9. **Roof:** `Toy_white` membrane slab, top at z=9.45, inset 0.35 m from the
   parapet inner face — a bright plane inside a cream frame.
10. **Rooftop plant (three clusters, all below z=9.90):** a long low
    `Toy_steel` duct run at the west end; a pair of `Toy_roofd` HVAC boxes on a
    low curb mid-roof; one small `Toy_roofd` unit at the east end; one
    `Toy_steel` roof hatch beside the west cluster. Tight clusters, not scatter
    (§10).

### 2.8 Materials and palette

Deliberately 101 Grove's family for everything except the one colour that is the
point of the building (§24 structure families).

| Material | Hex | Where |
|---|---|---|
| `Toy_stone` | `d9d2c2` | the stucco body, all four elevations |
| `Toy_trim` | `f3efe6` | belt cornice, top cornice, parapet cap |
| `Toy_ultramarine` | `2436ae` | **the ground-floor band, north and west** (*estimated* — sample the real hue from photography and correct this) |
| `Toy_glass` | `2a4d73` | all upper-floor glazing |
| `Toy_ink` | `3a3530` | window reveals, storefront reveals, the entrance door |
| `Toy_cream` | `efe6d2` | storefront display panels |
| `Toy_white` | `f7f4ec` | the cool-roof membrane |
| `Toy_steel` | `9aa0a6` | duct run, roof hatch |
| `Toy_roofd` | `45454a` | rooftop mechanical units and their curb |
| `Toy_cream_Glow` | `efe6d2` | the Grove storefront display panels — the night hero |
| `Toy_glassl_Glow` | `6f95b8` | two lit upper windows on Grove |

`Toy_ultramarine` is a **new** palette entry. Check
`artifacts/*/build_*.py` before adding it — if a saturated blue of this family
already exists under another name, reuse that name instead of minting one.

**Night design.** One hero and one supporting group, per the style bible's
restraint rule. Hero: the Grove storefront display panels, which in the
reference imagery are lit from within even though the building is vacant — a
single low horizontal dash of warm light sitting *inside* the dark blue band,
which is a genuinely good night image and true to the building. Supporting: two
lit upper windows on Grove, irregularly spaced, never a full grid. Nothing on the
roof glows, nothing on Van Ness glows, and the blue itself does not glow. Glow
shells are thin, inset and lifted clear of the opaque panel behind them — the
app draws `_Glow` in a separate layer at ~12% alpha by day, so coincident faces
read as a smear.

### 2.9 Top surface

From orthoimagery, overlaid against the OSM polygon:

- A **bright white cool-roof membrane** covering essentially the whole footprint
  — a hard, blown-out plane inside a narrow grey-cream parapet frame. This is by
  far the dominant fact from directly overhead.
- **Three small clusters of plant**, all low: an elongated dark object at the
  west end (read as a duct run or a long skylight), a cluster of two or three
  units near the middle of the roof, and one small unit toward the east end.
- A shadow line along the south edge confirms a **raised parapet**, not a flush
  roof edge.
- **No** penthouse, no bulkhead, no stair tower, no terrace, no greenery, no
  signage, no solar. Nothing breaks the parapet silhouette.
- The north third of the roof is under **street-tree canopy** in every image; the
  trees belong to the pipeline's baked tree layer, not to this asset, but they
  are the likely explanation for the LiDAR outliers in §2.15.

### 2.10 Scope

In: the building, its blue base band, belt cornice, window grid, top cornice,
parapet, roof membrane and rooftop plant.

Out: Van Ness Avenue, Grove Street, the BRT median and stations, trolley wire,
City Hall, Civic Center Plaza, the Bowes Center, the lot 018/019 neighbours,
sidewalks, street trees, traffic signals, parked cars, people, plinths, cameras,
lights.

### 2.11 Triangle budget

Cap **9,000**. Indicative split:

| Group | Est. tris |
|---|---|
| Body prism + blue band shell + belt cornice + top cornice + parapet cap (beveled ring bands) | ~1,600 |
| Upper window grid, 10 openings x (reveal + glass), incl. the arched head | ~1,900 |
| Storefront band, 7 openings x (reveal + panel) + the recessed entrance | ~1,900 |
| Roof: membrane, parapet inner face, three plant clusters, hatch | ~1,900 |
| Glow shells (storefront strip + two upper windows) | ~400 |
| Bevel overhead on the chunky solids | the balance |

If it overshoots: drop the storefront count on Van Ness first, then merge the
mid-roof HVAC pair into one box. Never the blue band, the two cornices, or the
arched bay.

### 2.12 Draft manifest entry

```json
{
  "id": "250-van-ness",
  "file": "250-van-ness.glb",
  "anchor": [-122.4194756, 37.7781332],
  "targetHeightM": 10.0,
  "cat": 3,
  "name": "250 Van Ness Avenue",
  "estimated": true,
  "dims": [34.08, 19.69, 10.0],
  "tris": N,
  "loadRadius": 2500
}
```

`dims` above is the footprint AABB, which is wider than the 32.07 x 14.51 m
oriented rectangle because the building sits on the rotated Civic Center grid;
the real exported dims come from the validator.

`estimated: true` because the crest is a parapet inference on top of a measured
roof deck (2.1). `loadRadius` follows the default rule
`max(2500, 10.0 x 30)` = 2500 — a 10 m building is illegible well before 2.5 km,
and there is no case whatsoever for `alwaysLoaded`.

### 2.13 Integration notes (for later, not this task)

**Case B — new landmark.** No `250-van-ness` / `250VanNess` id exists in
`pipeline/lib/landmarks.mjs` or `app/src/landmarks.js`, so integration needs a
registry entry *and* a re-bake of the affected tiles.

This is not optional cosmetics here: **the baked procedural block on this parcel
is 12.4 m tall and the asset is 10.0 m**, so without the exclusion the GLB is
completely buried and an un-baked QA pass would show a perfectly healthy scene
with an invisible landmark in it. Batch mode's "still run the bake, then throw it
away" rule exists for exactly this case.

The exclusion radius is measured, not guessed. `excluded()` in
`pipeline/buildings.mjs` drops a footprint when its centroid **or any ring
vertex** falls inside the circle. Read from the committed tile
`app/public/tiles/buildings/19_14.bin` (the same cell as `101Grove`), around this
anchor:

| Footprint | area | height | centroid dist | nearest vertex |
|---|---|---|---|---|
| **this building** | 427 m2 | 12.4 m | **1.50 m** | 16.04 m |
| south neighbour (lot 019) | 506 m2 | 12.7 m | 16.69 m | **16.48 m** |
| next building east | 267 m2 | 10.5 m | 25.81 m | 26.69 m |

So the window is `1.50 < r < 16.04`: anything in it drops this footprint by the
centroid test and nothing else. Above 16.48 m it starts eating the attached
neighbour on lot 019, which has no hand-built replacement. **14 m** is chosen —
2.5 m of margin under the neighbour, and wide enough that `exclude`'s second job
(the tree-clear and street-furniture radius) covers all but the two far corner
tips of the shell, which sit on the property line where no furniture is placed.

Draft registry entry:

```js
{
  // Two-storey 1913 corner block at Van Ness and Grove, 32 x 14.5 m, attached
  // to its southern neighbour. The radius is small because it has to be:
  // excluded() drops a footprint when its centroid OR any vertex is inside,
  // and measured against the committed tile 19_14 the numbers are
  //   this footprint   centroid  1.50 m, nearest vertex 16.04 m
  //   lot 019 neighbour centroid 16.69 m, nearest vertex 16.48 m
  // so 1.50 < r < 16.04 drops exactly this building. 14 m takes it with
  // margin. Note the procedural block here is 12.4 m and the asset is 10.0 m,
  // so skipping the re-bake does not "just leave a small error" — it hides
  // the asset entirely.
  id: '250VanNess',
  name: '250 Van Ness Avenue',
  lon: -122.4194756,
  lat: 37.7781332,
  height: 10,
  exclude: 14,
  camera: { distance: 180, yaw: 305, pitch: 26 },
}
```

The camera preset looks back along the corner's bisector (the mean of the two
public normals, ~305 deg true) from 180 m — close enough that a 10 m building
fills the frame, with City Hall's dome behind it.

Then run `docs/asset-plans/INTEGRATION-PROMPT.md` in full: manifest entry with
the explicit `loadRadius`, registry entry, tile re-bake, audit 1.6, local
verification (single building, scale 1.0, orientation, terrain seating, night
glow, draw calls < 300), and the mandatory fallback drill. In **batch mode**,
finish the QA on the bake and then `git checkout -- app/public/tiles api/_data`
before committing, per `docs/asset-pipeline/BATCH-INTEGRATE.md`.

After the re-bake, `node pipeline/verify-rebake.mjs` must show cell `19_14`
dropping by exactly one building and a nearest surviving vertex of ~16.5 m
against the 14 m radius.

### 2.14 Validation checklist

- Fresh-scene re-import of the exported GLB, not the source scene
- `dims.z` exactly 10.00 so `targetHeightM / measuredHeight` = 1.0
- `min_z` within 0.5 m of 0; XY centre within 1 m of origin
- ≤ 9,000 triangles
- No image textures, no transparency, no cameras/lights/animation/armatures
- Every material `Toy_*`, no `Toy_body`
- `_Glow` only on the Grove storefront strip and the two lit upper windows
- The blue band appears on the north and west faces only, and is one continuous
  surface around the corner
- Nothing on the roof rises above z=9.90
- Per-object signed volume positive for every object; ray residual ≤ 0.15%
- No degenerate triangles (the usual cause is a bevel on a plate thinner than
  twice the bevel width — leave the display panels and glass slabs unbeveled)
- Aerial render reviewed **before** the formal rig, and again after

### 2.15 Open questions and risks

1. **The crest is estimated, and one source disagrees.** LiDAR modal 9.32 m
   (roof deck) plus an inferred ~0.7 m parapet gives 10.0 m, which OSM's
   `height=10` matches independently. Overture — the pipeline's own bake input —
   says **12.4 m**, and the 2010 LiDAR max return is 13.03 m. Both are read as
   the same artefact: mature street trees overhang the north edge of this
   footprint in every image, and the LiDAR min return of 2.52 m on a 9.3 m
   building shows the same raster is contaminated at its edges. A rough
   photogrammetric check against the Street View horizon puts the parapet at
   9–11 m, and a 12.4 m two-storey building would need ~6 m storeys. The
   decision is 10.0 m; **if the executing agent finds a measured elevation, use
   it and re-normalize**, and say so loudly in `REPORT.md` because the manifest,
   the registry `height` and the exclusion note all move with it.
2. **Bay counts and window sizes are a design choice, not a measurement.** Seven
   Grove bays at ~4.0 m and three on Van Ness is a proportional fit; the trees
   hide most of the Grove elevation in every image located.
3. **The blue is not sourced.** It is present across multiple Street View
   passes, so it is not fresh graffiti, but nothing was found explaining what it
   is — repaint, mural, or graffiti abatement — and the hex in §2.8 is eyeballed
   from a sunlit photograph. This is the building's entire identity, so getting
   the hue right matters more here than anywhere else in the asset.
4. **South and east elevations are inferred.** Neither is visible from any
   public vantage located. They are party/back walls; the risk is low but real.
5. **Historic use is a single-source label.** SF Planning's `buildingname` for
   171 Grove is "CHURCH OF CHRIST"; no corroborating source was found, and the
   Heritage survey rated the building D ("Minor Or No Importance") in 1978. The
   2010 Van Ness Auto Row survey is the most likely place to resolve both the
   original use and the architect, and it was not readable.
6. **Exclusion radius.** 14 m is measured against the committed tile, not
   guessed — but it must still be confirmed by `verify-rebake` after the bake,
   because the attached neighbour on lot 019 sits only 2.5 m outside it.
7. **The building is vacant and boarded.** Part 1 rules that the boards are not
   modelled. If David prefers the honest boarded state, that is a one-material
   change (`Toy_glass` → `Toy_oak`) and should be raised at stage 3 rather than
   assumed.
