# 541 Presidio Boulevard — SF-SIM asset plan

A World War I–era officer's family quarters in the Presidio's East Housing area: a
two-storey cream-stucco box under a red barrel-tile hip roof, with a one-storey porch
across its street face and stucco chimneys breaking the ridge. Building 541 is one of
twelve near-identical houses (Bldgs. 540–551) strung along the curve of Presidio
Boulevard as it climbs a forested hill southeast of the Main Post.

This is the second **Presidio** plan (after `1008-general-kennedy.md`) and the first for
a *house* — the smallest and most ordinary subject in the set. The design brief is
"the most legible house in a curving row of twelve near-identical houses", not
"monument" and not "background block". Its job in the scene is to make the East Housing
hillside read as a designed military neighbourhood rather than a scatter of baked boxes.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/541-presidio/`. This document is the plan only: Part 1 is the runnable task
prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `541-presidio` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.4518601, 37.7969312` |
| Target height | **10.0 m** to the chimney crest; hip ridge 9.6 m; eave 7.2 m |
| Footprint | 19.77 m long x 11.65 m wide main block, plus a 9.68 x 1.75 m front porch and a 4.61 x 0.86 m rear bay; 250.7 m2, measured |
| Long axis heading | 30.68° / 210.68°; long elevations face 120.68° (front, Presidio Blvd) and 300.68° (rear) |
| Triangle cap | 8,000 |
| Category | `1` (house) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 541 Presidio Boulevard GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of the officer's quarters at 541 Presidio
Boulevard, Presidio of San Francisco, and deliver it as a downloadable, validated GLB.

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
7. `artifacts/380-brannan/` — the closest reference implementation in scale, budget and
   character (small non-monument building, one strong facade rhythm, designed roof,
   restrained night state)
8. `artifacts/1008-general-kennedy/` — the other Presidio building, and the reference for
   red barrel-tile hip roofs, white stucco walls and chimney treatment
9. `docs/asset-plans/541-presidio.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Must capture

- A **compact two-storey box** — 19.77 x 11.65 m, almost square in feel compared to the
  1008 ward. This is a *house*, and its domestic scale is the point.
- The **red barrel-tile hip roof with deep overhanging eaves** — the single dominant
  element from the app's aerial camera, and what ties the whole row 540–551 together
- **Cream / white smooth stucco** walls, unornamented — flat planes with punched openings
- The **one-storey porch across the street (front) elevation**: a 9.68 x 1.75 m
  projection with its own hipped tile roof, the only relief on the facade
- **Stucco chimney stacks** rising through the ridge — the only vertical incident on the
  roof and the feature that sets the model's crest height
- A **regular two-tier rhythm of double-hung windows** with light trim against dark glass
- The **raised plinth** the house sits on, which also hides the terrain seam

## Research 541 Presidio Boulevard independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- All four elevations — the front (southeast-facing, toward Presidio Boulevard), the rear
  (northwest, into the hill and trees), and both short ends (northeast and southwest,
  facing the neighbours at 542 and 540)
- Aerial and roof views: the hip geometry, the ridge line, and the chimney positions and
  count, which are *inferred* in this dossier and are the weakest numbers in it
- Ground-level views from Presidio Boulevard and from Sumner Avenue below
- Day and night appearance
- The bay count and window rhythm of each elevation, which is *inferred* here and must be
  confirmed
- **Whether the front projection is an open porch, an enclosed sun porch, or a
  full-height projecting bay** — this dossier reads it as a one-storey porch and that is
  the single most consequential open question (see 2.15)

Prefer NPS and Presidio Trust historic documentation (the row is a contributing element
of the Presidio National Historic Landmark District), the ACHP Section 213 report, HABS
surveys, planning documents, geolocated photography, and aerial/satellite imagery. Never
rely on a single photograph, a single AI-generated image, or a single unsourced 3D model.
Separate verified facts from visual inference; if sources disagree, document the
disagreement and decide.

**Three source problems are already known and resolved in 2.1, 2.2 and 2.15 — re-check
them, do not silently re-inherit the wrong value:**

1. **The OSM `height=8` tag is not the building's height.** It matches the 2010 city
   LiDAR's *median* roof height over the footprint (8.16 m) almost exactly, which is what
   you get when you average a hip roof between eave and ridge. The LiDAR maximum is
   10.04 m. Use 10.0 m as the crest; never 8.
2. **The NPS architectural history assigns "the cluster of large officers' quarters
   located at Funston and Presidio Boulevards" to the Queen Anne style (1880–1890).**
   That is a *different* cluster — the 1880s quarters further up Presidio Boulevard near
   the Main Post. The ACHP Section 213 report is specific that Bldgs. **540–551**, on the
   curve of Presidio Boulevard, are World War I–era and "exhibit white stucco walls
   barrel tile roof". Model the stucco-and-tile house, not a Queen Anne.
3. **This is a row of twelve near-identical houses, ~25 m apart.** Photographs and aerial
   imagery of "541 Presidio Blvd" will frequently show 540, 542 or 543 instead. Confirm
   which building you are looking at from its position in the arc before drawing a
   conclusion from any image.

## Create a reference dossier

Write `artifacts/541-presidio/REFERENCE.md` containing: source links and what each
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

This is a **secondary building** in the style bible's detail budget (§21), and at the
small end of it: clear massing, one strong facade rhythm, a simple designed roof, and
exactly one identity cue carried hard — the red tile hip roof with its chimneys and deep
eaves. Resist adding hero-tier ornament. A house that out-details the landmarks around it
is a failure even if it is beautiful.

The finished asset must be immediately recognizable as this house, consistent with the
real building from all four sides and above, architecturally credible, and a premium
handcrafted miniature — not photorealistic, not voxel art, not generic low-poly, and
never accurate in one view while invented in the others.

## Scope of the exported asset

Export the single house: the plinth, the two-storey stucco block, its hipped tile roof
and chimneys, the front porch with its own roof, the shallow rear bay, and all four
elevations' openings.

Do not include unrelated surrounding city geometry: the neighbouring houses at 540 and
542, the rest of the row, Presidio Boulevard, Sumner Avenue, driveways, garden walls,
lawns, hedges, trees, sidewalks, parked cars, people, plinths, cameras or lights.
Temporary context may appear in review renders but must not leak into the GLB.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary
`.glb`; real-world meters; origin at base center; minimum geometry Z ~ 0;
applied transforms; no negative scales; outward normals; no duplicate or foreign
geometry; no image textures; no transparency; flat-color materials named `Toy_*`
from the project palette; `_Glow` suffix only on surfaces that glow at night; no
`Toy_body`; no cameras, lights, animations, armatures or constraints; no external
dependencies; at most 8,000 triangles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model
drops into the city at its real-world heading — the loader applies no rotation
(`placeGeneric` in `app/src/assets.js` only scales and positions). The long axis runs
**30.68° / 210.68°**, with the front porch on the **120.68°** (east-southeast) elevation
facing Presidio Boulevard. The building is rotated ~31° off the world axes, so build
directly on the measured footprint polygon in 2.3 rather than modelling an axis-aligned
box and rotating it. Record the measured heading in `REPORT.md`.

**Height normalization:** the tallest geometry in the export (the chimney crest) must
land at exactly **10.0 m** so the loader's `targetHeightM / measuredHeight` scale is 1.0.

## Reproducible Blender workflow

Blender 5.2 LTS. Headless: `blender -b --python script.py -- args`.

Keep `artifacts/541-presidio/build_541_presidio.py` (deterministic build script),
`artifacts/541-presidio/541-presidio.blend`, and
`artifacts/541-presidio/541-presidio.glb`. The script must rebuild the model reliably
enough for future revision. Do not modify or rename an unrelated existing GLB to satisfy
the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`541-presidio-top.png`, `-north.png`, `-east.png`, `-south.png`, `-west.png`, plus
`541-presidio-contact-sheet.png`, at least one high three-quarter aerial beauty render
`541-presidio-aerial.png`, and a night render `541-presidio-aerial-night.png`.

The four elevations must share scale, framing, lighting, exposure and projection; use
orthographic or long-lens cameras; label directions from the researched orientation; the
top view must clearly show the hip geometry, the ridge, the chimneys and the porch's
separate hip; the aerial view uses the style bible's camera assumptions (30–50 degrees
down, long lens). Simple tabletop lighting, neutral warm background, minimal depth of
field, and every image must depict the same exported model.

Because the building is rotated ~31° off the world axes, the compass-named elevation
views will each show the house obliquely unless the cameras are aligned to the
*building's* axes. Align them to the building and say so in the labels — a reviewer
comparing "north" and "south" needs two opposite faces, not two three-quarter views.

## Validate the exported GLB

Re-import `541-presidio.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture
count, camera count, light count, animation count, applied-transform status,
negative-scale status, normal-orientation status, unexpected geometry, and
per-material contract compliance. Render at least one review image from the
re-imported asset. Write `artifacts/541-presidio/validation.json` and
`artifacts/541-presidio/REPORT.md`.

Note that the axis-aligned XY bounding box will be roughly **21.6 x 24.3 m** even though
the building is 19.8 x 11.7 m plus a porch — that is the expected consequence of the
~31° real-world heading plus the eave overhang, not a scale error.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "541-presidio",
  "file": "541-presidio.glb",
  "anchor": [
    -122.4518601,
    37.7969312
  ],
  "targetHeightM": 10.0,
  "cat": 1,
  "name": "541 Presidio Boulevard",
  "estimated": true,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

`"estimated": true` is deliberate — the crest height is derived from 2010 city LiDAR,
not published. See 2.15.

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a separate, explicitly requested job — run `docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in `docs/asset-plans/541-presidio.md`.
````

---

## Part 2 — Research and design dossier

Everything below is the research behind Part 1. The executing agent is expected to
re-verify it, not cite it.

### 2.1 Verified facts

| Fact | Value | Confidence | Source |
|---|---|---|---|
| Address | 541 Presidio Blvd, San Francisco, CA 94129 | measured | Nominatim reverse/forward geocode |
| OSM way | `288361187`, 12 distinct vertices, closed | measured | OSM Overpass `way(288361187); out geom tags` |
| Footprint area | 250.7 m2 | measured | shoelace over the reprojected OSM ring |
| Oriented bounding box | 14.27 x 19.77 m | measured | min-area rotating-caliper fit over the OSM ring |
| Main block | 19.77 x 11.65 m | measured | OBB-frame decomposition of the ring (2.3) |
| Front porch projection | 9.68 x 1.75 m, on the 120.68° elevation | measured (extent) / *inferred* (that it is a porch) | same; see 2.15 |
| Rear bay projection | 4.61 x 0.86 m, on the 300.68° elevation | measured | same |
| Long axis heading | 30.68° / 210.68° | measured | OBB principal direction |
| WGS84 anchor (main-block centre) | `-122.4518601, 37.7969312` | measured | main-block centre, reprojected back (2.3) |
| Ground pad elevation | 41.05 m NAVD88 median (min 40.50, max 41.34) | measured | DataSF LiDAR building footprints, `sf16_bldgid` `201006.0016742` |
| Pad slope across footprint | 0.84 m range, 0.12 m std — effectively level | measured | same |
| Roof crest above ground | **10.04 m** | measured | same, `hgt_maxcm` = 1004 |
| Median roof height above ground | 8.16 m | measured | same, `hgt_mediancm` = 816 |
| Hip ridge | ~9.6 m | *inferred* | solved from the crest/median pair against a straight-skeleton hip model (2.3) |
| Eave | ~7.2 m | *inferred* | same solve; cross-checks to two ~3.15 m storeys over a 0.9 m plinth |
| Roof pitch | ~22° | *inferred* | ridge/eave over the 5.83 m half-span |
| Storeys | 2 over a raised plinth | *inferred* | two window tiers in Google Maps place photography; consistent with the height solve |
| Roof form | hipped | measured | OSM `roof:shape=hipped`, confirmed in aerial imagery |
| Roof colour | red | measured | OSM `roof:colour=red`, confirmed in aerial imagery |
| Roof material | barrel tile | high | ACHP Section 213 report, for the row 540–551 |
| Wall material | white / cream stucco | high | ACHP Section 213 report, for the row 540–551 |
| Era | World War I (1915–1918) | high | ACHP Section 213 report places the row in its WWI construction period |
| Original use | officer family housing | high | same, "an imposing row of officer housing (Bldgs. 540–551)" |
| Current use | Presidio Trust residential leasing | medium | Presidio Trust leasing presence at 558 Presidio Blvd (OSM `name`), Presidio residential leasing marketing for the adjacent Simonds Loop neighbourhood |
| Row membership | one of Bldgs. 540–551, ~25 m apart along the boulevard curve | measured | ACHP report for the range; OSM centres for the spacing |
| Historic status | contributing element, Presidio of San Francisco NHL District | high | NHLD covers the East Housing area; ACHP Section 213 report |

### 2.2 Sources

- **ACHP, "Section 213 Report: Presidio of San Francisco National Historic Landmark
  District", 6 April 2009** —
  https://www.achp.gov/sites/default/files/whitepapers/2022-12/Presidio%20(of%20San%20Francisco)%20NHL%20Section%20213%20Report_2009.pdf
  The load-bearing source for identity, era and materials. In the World War I section:
  "An imposing row of officer housing (Bldgs. 540 – 551) located along the curve of
  Presidio Boulevard, southeast of the Main Post represent the more permanent type of
  construction completed during the period. The curvilinear layout that ascends one of the
  forested hills of the Presidio reflects and utilizes the terrain in a manner similar to
  the officer housing at Infantry Terrace. The designs for the housing at both areas
  exhibit white stucco walls barrel tile roof combined with the basic forms characteristic
  at the Post." Also establishes the East & West Cantonment Areas (1899) as today's East
  Housing Area.
- **NPS / GGNRA, "The Presidio of San Francisco: An Architectural History" (D-31D)** —
  https://npshistory.com/publications/prsf/arch-hist.pdf
  Establishes the Mission Revival (1910–1940) vocabulary the row belongs to: "large flat
  stucco surfaces, often punctuated by deep windows and door openings… The gable and hip
  roofs were typically sheathed in red tiles", and that "the shadows cast on walls by
  overhanging roofs were usually the building's only decorative features". Also the source
  of the Queen Anne conflict resolved in 2.15.
- **OSM way 288361187** — footprint geometry and the `roof:shape` / `roof:colour` /
  `height` tags. Geometry via Overpass; the ring is the measured basis for 2.3.
- **DataSF, Building Footprints (2010 LiDAR), `ynuv-fyni`, `sf16_bldgid`
  `201006.0016742`** — https://data.sfgov.org/resource/ynuv-fyni.json
  Ground and roof elevations: `gnd_min_m` 40.5, `gnd_mediancm` 4105, `gnd_rangecm` 84,
  `peak_1st_m` 50.97, `hgt_maxcm` 1004, `hgt_mediancm` 816, `hgt_cells50cm` 992 (≈248 m2,
  i.e. full roof coverage). This is the height authority for the plan.
- **Google Maps place page for 541 Presidio Blvd** — aerial imagery (Airbus / Maxar /
  Vexcel, 2026) for the roof plan and the row's setting, and place photography for the
  wall colour, window pattern and two-storey reading. Not committed to the repo.
- **NPS, "Presidio of San Francisco Architecture"** —
  https://www.nps.gov/articles/presidio-architecture.htm — general style context.

### 2.3 Orientation and placement

The measured OSM ring, reprojected with the project's tangent projection
(`x=(lon−(−122.4375))·111320·cos(37.77°)`, `z=−(lat−37.77)·110540`) and reduced to the
min-area oriented bounding box, gives a frame in which the plan decomposes cleanly.
`u` runs along bearing **120.68°** (east-southeast) with extent 14.27 m; `v` runs along
bearing **30.68°** (north-northeast) with extent 19.77 m.

| # | u (m) | v (m) |
|---|---|---|
| 0 | 0.94 | 0.00 |
| 1 | 12.58 | 0.00 |
| 2 | 12.54 | 5.19 |
| 3 | 14.27 | 5.19 |
| 4 | 14.20 | 14.87 |
| 5 | 12.47 | 14.87 |
| 6 | 12.44 | 19.77 |
| 7 | 0.81 | 19.77 |
| 8 | 0.85 | 12.40 |
| 9 | 0.00 | 12.40 |
| 10 | 0.03 | 7.79 |
| 11 | 0.89 | 7.79 |

Reading it:

- **Main block** u ≈ 0.85 → 12.50, v = 0 → 19.77 — a **19.77 x 11.65 m** rectangle.
- **Front porch** u 12.50 → 14.27 over v 5.19 → 14.87 — a **9.68 m long, 1.75 m deep**
  projection, centred on the u-max long elevation. u increases toward bearing 120.68°, so
  this is the **east-southeast face, toward Presidio Boulevard** — the front.
- **Rear bay** u 0.85 → 0.00 over v 7.79 → 12.40 — a **4.61 m long, 0.86 m deep**
  projection on the opposite (300.68°, west-northwest) face — a stair or chimney breast.

So the two long elevations face **120.68°** (front, to the boulevard) and **300.68°**
(rear, into the hill and the tree cover). The two short 11.65 m ends face **30.68°**
(toward 542) and **210.68°** (toward 540).

**Anchor.** The full-ring centroid and the main-block centre differ by only 0.36 m here —
the projections are small and nearly opposed, so they very nearly cancel. Use the
**main-block centre**, `-122.4518601, 37.7969312`, because that is the volume the model is
built around and the volume the loader should centre; the ring centroid
(`-122.4518566, 37.7969294`) is an acceptable 0.36 m alternative.

**Ground.** The pad is effectively level: 0.84 m of range and 0.12 m of standard
deviation across 248 m2 of LiDAR ground cells. The hill is *around* the house, not under
it — these houses sit on graded terraces. Model a flat base; do not step the plinth.

**Height solve.** Two LiDAR numbers constrain the roof: the maximum (10.04 m) and the
median (8.16 m) height above ground. Modelling a uniform-pitch hip as
`h(p) = eave + pitch · d(p)` where `d` is distance to the nearest footprint edge, and
computing `d` over the real ring on a 0.1 m grid (25,149 cells, 251.5 m2) gives
median `d` = 2.16 m and max `d` = 6.88 m. Restricting to the 19.77 x 11.65 m main-block
rectangle (median `d` = 2.12 m, max `d` = 5.83 m) and solving:

| assumed ridge | pitch | eave |
|---|---|---|
| 9.4 m | 18.6° | 7.44 m |
| **9.6 m** | **21.2°** | **7.34 m** |
| 9.8 m | 23.6° | 7.25 m |
| 10.04 m | 26.9° | 7.09 m |

Every solution lands the eave at 7.1–7.4 m and the pitch inside the 18–27° band that
barrel tile is actually laid at. Take **eave 7.2 m, ridge 9.6 m (pitch ~22°), chimney
crest 10.04 m**, which also divides cleanly into a 0.9 m plinth plus two ~3.15 m storeys.
The 0.44 m between ridge and LiDAR maximum is the chimney: `hgt_max` exceeds a
uniform-pitch hip's ridge by exactly the kind of margin a stack produces, and the roof
otherwise covers 992 cells consistently (std 1.30 m).

**The `height=8` trap.** OSM's `height=8` for this way is within 0.16 m of the LiDAR
*median* (8.16 m). That is not a coincidence and not a crest — it is what you measure if
you average a hip roof. Using it would build a house 2 m too short with a flat top.

### 2.4 What each side shows

Directions below are the building's own faces, named by the bearing they look toward.

- **Front, 120.68° (east-southeast, to Presidio Boulevard).** The public face and the
  only one with relief: the 9.68 x 1.75 m one-storey porch across the middle half of the
  19.77 m elevation, with the entrance in it, and two tiers of windows to either side and
  above. The boulevard is ~30 m away and downhill-ish; this is the elevation a visitor and
  the app's camera both see first.
- **Rear, 300.68° (west-northwest, into the hill).** Plain stucco with the same two-tier
  window rhythm, interrupted by the shallow 4.61 x 0.86 m bay. Heavily screened by mature
  cypress and eucalyptus — in the app it will almost always be seen against tree cover.
  *Inferred*: the bay is a stair projection or chimney breast; a service door at plinth
  level is plausible but unconfirmed.
- **Northeast end, 30.68° (toward 542).** An 11.65 m gable-free hip end, two tiers of
  windows, narrower rhythm than the long sides. ~29 m of lawn to the neighbour.
- **Southwest end, 210.68° (toward 540).** The mirror condition, ~30 m to 540.
- **From above.** A single red barrel-tile hip over the main block with a continuous ridge
  running north-northeast, the porch's separate lower hip attached on the front slope, and
  stucco chimneys breaking the ridge. Deep eaves throw a hard shadow line all the way
  round. This is the surface the app's camera spends nearly all its time looking at, and
  in the aerial imagery it is unambiguously the building's identity — twelve of these
  tile hips stepping along a curve through dark trees is what the East Housing hillside
  looks like. *Inferred*: chimney count and position — the dossier assumes two, one near
  each end of the ridge.

### 2.5 Recognition cues (ranked)

1. **The red barrel-tile hip roof with deep overhanging eaves.** At the app's viewing
   distance this is ~90% of the building. Get the hip lines crisp and the eave shadow deep
   and the asset works even if everything else is approximate.
2. **Flat cream stucco walls** with no ornament — bright, clean planes that make the roof
   read.
3. **The one-storey front porch** breaking the street elevation's base — the silhouette
   cue that distinguishes this from a plain box.
4. **Stucco chimneys through the ridge** — the only vertical incident, and the crest.
5. **The two-tier window rhythm**, as a rhythm rather than as individual windows.
6. **Domestic scale.** 19.8 x 11.7 m and 10 m tall, sitting beside a 22 m Letterman
   campus and a 12.6 m 380 Brannan. It must read as a *house*.

### 2.6 Miniature translation

**Preserve**

- The 19.77 x 11.65 m main block and the real 30.68° heading, exactly
- The continuous hip and ridge, and the porch's separate lower hip
- Deep eave overhangs — they are what make a tile roof read as a tile roof at 20 px
- The chimneys, thickened so they survive at thumbnail size
- The two-storey window rhythm as a rhythm, not as individual windows
- The raised plinth, which also hides the terrain seam

**Simplify / exaggerate**

- Individual barrel tiles become flat colour; the eave becomes one chunky fascia band
- Each long elevation's real window count becomes **5 clean bays**, all identical,
  recessed 0.12 m; each short end becomes **3 bays**
- Double-hung subdivision, sashes, screens and blinds disappear — sub-pixel at city scale
- The porch becomes a simple one-storey volume with its own hip and a recessed door;
  no balustrade, no individual porch columns unless the aerial review asks for them
- Chimneys are exaggerated in section (to ~0.9 x 0.7 m) but not in height; they set the
  10.0 m crest and must land on it exactly
- The rear bay stays as a plain 0.86 m pilaster of wall — it is a silhouette event from
  above, nothing more
- The plinth becomes a 0.9 m band in a slightly darker value

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not
a straitjacket — adjust after the first aerial review render.

1. Plinth: extrude the full 2.3 footprint (main block + porch + rear bay) from z=0 to
   z=0.9, `Toy_stone`.
2. Main block: extrude the 19.77 x 11.65 m rectangle from z=0.9 to z=7.2, `Toy_white`.
3. Rear bay: extrude the 4.61 x 0.86 m projection from z=0.9 to z=7.2, `Toy_white` — full
   height, flush into the main roof's slope.
4. Front porch: extrude the 9.68 x 1.75 m projection from z=0.9 to z=3.4, `Toy_white`.
5. Long elevations, front and rear: 5 bays each, openings 1.1 x 1.9 m, two tiers with
   sills at z=1.7 and z=4.6, recessed 0.12 m, `Toy_glass`; 0.10 m proud `Toy_trim` sill
   under each. On the front, the porch occupies the middle — put the ground tier's centre
   three bays *in the porch face* and keep all five in the upper tier.
6. Short ends: 3 bays per tier, same family, same sill heights.
7. Entrance: 1.0 x 2.2 m recessed doorway centred in the porch's front face at plinth
   level, `Toy_ink`.
8. Main roof: hipped, eave line at z=7.2 with a **0.7 m overhang on all four sides**,
   ridge at **z=9.6** running along the 30.68° axis, pitch ~22°, `Toy_red`. Fascia band
   0.22 m in `Toy_trim` under the eave.
9. Porch roof: its own hip, eave at z=3.4 with a 0.5 m overhang, ridge ~z=4.1, same
   materials — clearly subordinate to the main roof.
10. Chimneys: two stucco stacks on the main ridge at roughly 25% and 75% of its length,
    0.9 x 0.7 m in section, rising to **z=10.04** — these set the bounding-box top and
    must land exactly on 10.0 after normalization.
11. Bevel 0.12 m, 2 segments.

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_white` | `#f7f4ec` | stucco walls — main block, porch, rear bay |
| `Toy_stone` | `#d9d2c2` | plinth band, chimney stacks |
| `Toy_red` | `#c4453c` | **the tile roof** — main hip, porch hip |
| `Toy_trim` | `#f3efe6` | eave fascia, window sills, porch soffit |
| `Toy_glass` | `#2a4d73` | all windows |
| `Toy_ink` | `#3a3530` | entrance doorway recess |
| `Toy_glass_Glow` | `#2a4d73` | lit windows at night |
| `Toy_trim_Glow` | `#f3efe6` | porch soffit at night |

Two palette decisions to record in `REPORT.md`:

- **Roof.** `Toy_red` (`#c4453c`) is cooler and more saturated than real weathered barrel
  tile. It is used anyway, for consistency with `1008-general-kennedy`, which faced the
  same choice. If the aerial render says otherwise, an off-palette weathered terracotta at
  roughly `#b85a44` is a WARN not a FAIL — but justify it, and change both assets or
  neither.
- **Chimneys.** These stacks are stuccoed to match the walls, not exposed brick, so
  `Toy_brick` would be wrong here even though 1008 uses it. `Toy_stone` (`#d9d2c2`) keeps
  them a half-value darker than `Toy_white` so they still read as separate objects from
  directly above, which is the only view that matters for them.

**Night state (required).** Glow surfaces must be thin shells proud of the opaque glazing —
the app renders `_Glow` in a separate layer that is ~12% alpha by day, so a primary
surface must never be authored as glow. Hero glow: **three or four lit windows on the front
elevation only** — one ground-tier window in the porch and two or three upper-tier windows.
This is a single-family house on a quiet Presidio street; a fully lit twelve-window box
would read as an institution, and the whole row lit identically would look like a
rendering error. Supporting accent: the porch soffit over the entrance. The roof does not
glow.

### 2.9 Top surface

A 250 m2 tile hip, seen constantly from above, and the entire reason this asset earns its
place. Its quality comes from four things: the crispness of the hip lines, the depth of
the eave shadow, the two chimneys, and the porch's subordinate hip breaking the front
slope. Model the hips as real geometry with proper ridge and hip edges — do not fake them
with a flat plane and a bevel. Keep the fascia value clearly lighter than the tile so the
eave reads as an edge from directly overhead.

The porch hip is the detail that stops this reading as a generic hipped box from the air.
Do not delete it to save triangles.

### 2.10 Scope

**In the GLB:** the single house — plinth, two-storey stucco block, rear bay, front porch,
hipped tile roofs on both, chimneys, and all four elevations' openings

**Not in the GLB:** the neighbouring houses at 540 and 542, the rest of the row 543–551,
Presidio Boulevard, Sumner Avenue, driveways, garden walls, retaining walls, lawns,
hedges, trees, sidewalk, vehicles, people, plinths, cameras or lights

### 2.11 Triangle budget

Cap 8,000 — a small secondary building, and the cap should bind. Suggested split: plinth
~0.4k, main block and rear bay ~0.8k, porch ~0.5k, main hip roof with eaves and fascia
~1.8k, porch hip ~0.7k, 16 window bays across four elevations ~2.5k, doorway ~0.2k,
chimneys ~0.5k.

If the budget binds, drop window bays from the rear elevation before touching the roof or
the porch.

### 2.12 Draft manifest entry

```json
{
  "id": "541-presidio",
  "file": "541-presidio.glb",
  "anchor": [
    -122.4518601,
    37.7969312
  ],
  "targetHeightM": 10.0,
  "cat": 1,
  "name": "541 Presidio Boulevard",
  "estimated": true,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

`dims` and `tris` are placeholders until the asset is built and validated.

`loadRadius: 2500` is the default-rule floor: `max(2500, 10.0 × 30)` = 2500. A 10 m house
should never be `alwaysLoaded`.

### 2.13 Integration notes (for later, not this task)

- **New landmark.** Add a `pipeline/lib/landmarks.mjs` entry (`id: '541Presidio'`, camelCase
  there, kebab `541-presidio` in the manifest) and re-bake the affected tiles, or the baked
  procedural building will intersect the GLB.
- **The exclusion radius is the delicate part, and it is delicate in the opposite
  direction from 375 Alabama.** This house is one of twelve on a ~25 m pitch. The
  measured window is wide but bounded: our own ring centroid sits **0.36 m** from the
  anchor, while the nearest *neighbour* centroids are **29 m** (542) and **30 m** (540).
  Anything from roughly 2 m to 28 m drops 541 alone. Use **`exclude: 14`** — the middle of
  the window, tolerant of the few metres by which the baked footprint's simplified ring
  centroid may differ from the OSM one, and nowhere near taking a neighbour. A generous
  radius here would punch a hole in the row and be immediately visible as two missing
  houses.
- **Do not set `clearTrees`.** Unlike Letterman, this asset has no hand-modelled grounds,
  and the baked cypress/eucalyptus scatter around it *is* the East Housing character. The
  Presidio `PARK_COVER` entry (`base: 'trees'`, cypress/eucalyptus) should keep running
  right up to the house.
- **Camera preset:** a close domestic one is appropriate, in the family of 380 Brannan's
  `{ distance: 220, yaw: 45, pitch: 24 }`. Suggest `{ distance: 170, yaw: 300, pitch: 22 }`
  — looking at the front elevation from over the boulevard.
- **Height, not `alwaysLoaded`.** `height: 10` in the registry entry.
- **Watch the terrain seating.** The pad is level but it is a *cut terrace* on a hillside,
  and the app's `sampleElevation` comes from AWS Terrarium tiles whose resolution is much
  coarser than a 20 m terrace. Expect to check that the plinth is not floating or buried on
  the downhill (front) side, and record the result. This is the most likely integration
  defect for this asset.

### 2.14 Validation checklist

- [ ] Binary `.glb`, real metres, no external dependencies
- [ ] Origin at base centre; min Z ≈ 0; XY centre ≈ 0,0
- [ ] Tallest geometry (chimney crest) at exactly 10.0 m
- [ ] Axis-aligned XY bbox ≈ 21.6 x 24.3 m — the expected consequence of the 30.68°
      heading plus eaves, not a scale error
- [ ] Long axis measured at 30.68° in the export; front porch on the 120.68° face
- [ ] Applied transforms, no negative scales, outward normals
- [ ] ≤ 8,000 triangles
- [ ] Materials only from the 2.8 table; no textures, no transparency
- [ ] `_Glow` only on the lit windows and the porch soffit; glow shells proud of glazing
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] No foreign geometry (fresh-scene re-import proves it)
- [ ] Day and night aerial renders plus four building-aligned elevations and a top view
- [ ] `validation.json` all-PASS, `REPORT.md` written, dossier corrections recorded

### 2.15 Open questions and risks

1. **Is the front projection a porch?** *The single biggest open question.* The 9.68 x
   1.75 m extent is measured; reading it as a one-storey porch with its own hip is
   *inferred* from the aerial imagery and from the type. The alternatives are an enclosed
   sun porch (same massing, windows instead of an open face — visually almost identical at
   app scale, so low risk) or a **full-height two-storey projecting bay** (materially
   different silhouette and roof plan — the main hip would have to cross-gable over it).
   The executing agent must settle this from street-level photography before modelling
   step 4 and 9. If it turns out to be full-height, the porch hip in 2.9 becomes a cross
   hip and the triangle split in 2.11 shifts toward the roof.
2. **Chimney count and position.** Two stacks at 25%/75% of the ridge is a guess consistent
   with a 10.04 m LiDAR maximum over a 9.6 m ridge. One central stack, or three, are
   equally consistent with the height data. Confirm from aerial imagery. This matters
   because the chimneys carry the crest and are the roof's only incident.
3. **Ridge, eave and pitch are all *inferred*.** Only the crest (10.04 m) and the median
   (8.16 m) are measured. The solve in 2.3 is well-constrained and self-consistent, but a
   published elevation drawing or a HABS survey of any building in the row 540–551 would
   replace three inferences with one measurement and should be looked for.
4. **Window counts are invented rhythms.** 5 / 5 / 3 / 3 bays is a design decision that
   respects the elevation lengths, not a count from a photograph. Confirm the real rhythm
   and prefer it if it is legible; keep the invented rhythm only if the real one is not.
5. **The exact construction year is not pinned.** The ACHP report places the row in its
   World War I (1915–1918) section; it does not give a year for Building 541 specifically.
   Presidio Trust or NPS building records would settle it. Nothing in the model depends on
   it, but `REFERENCE.md` should not state a year it cannot support.
6. **Queen Anne vs Mission Revival — resolved, but re-check.** The NPS architectural
   history's Queen Anne section names "the cluster of large officers' quarters located at
   Funston and Presidio Boulevards", which a careless reading applies to this row. The
   ACHP report is specific and later: 540–551 are WWI-era white stucco with barrel tile.
   The OSM tags (`roof:shape=hipped`, `roof:colour=red`) and the aerial imagery agree with
   the ACHP reading. Resolved in favour of Mission Revival; documented here so it is not
   silently re-litigated.
7. **Duplex or single-family?** `cat: 1` (house) is used. The row is described as officer
   *family* housing, and 250 m2 over two storeys is large for one household, so a two-unit
   plan is possible; the adjacent Simonds Loop neighbourhood is marketed as duplexes. The
   category affects only the card chip and prop garnish, not the geometry, so this is a
   low-stakes call — but say which was chosen and why.
8. **Terrain seating on a cut terrace.** Flagged in 2.13 and repeated here because it is
   the defect most likely to survive to production: a level 20 m pad on a hillside is
   exactly the case coarse Terrarium elevation gets wrong.
