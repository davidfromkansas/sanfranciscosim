# 164 South Park — SF-SIM asset plan

A single-storey 1907 brick-and-timber warehouse at the west tip of the South Park oval,
wearing a 2024–25 **Stanley Saitowitz | Natoma Architects** front: large-format red panels
laid in stretcher bond, one black ribbon window that tracks the shift around the oval and
drops to become a glazed entry recess, and a slender black canopy over the door. The
concrete "doormat" at that door reads *164 South Park — Twitter and Instagram were both
founded here*, which is the plain truth: Twitter's first office (2006–2008) and Instagram's
(2010) were this room.

It is the first plan in this set for the **applied-facade** type — a new architect-designed
screen standing in front of a retained industrial shell — and the first South Park building
whose street elevation is *shorter* than the mass behind it. Almost every other plan in this
set had to talk itself out of the LiDAR median and up to the LiDAR maximum. This one goes the
other way, and §2.15 explains why in detail: **`hgt_maxcm = 925` is not this building.**

The design brief is "the lowest, reddest, most deliberate object on the rim" — the only
saturated-red plane on the oval, sitting a metre and a third *below* its own roof.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/164-south-park/`. This document is the plan only: Part 1 is the runnable task
prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `164-south-park` |
| Existing procedural builder | none — new landmark (**Case B**: needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor (manifest and registry) | `-122.3949366, 37.7812097` — the model's recentred origin; design anchor was the parcel-union area centroid `-122.3949238, 37.7812072` |
| Target height | **5.4 m** to the rear parapet crest (*LiDAR median, measured*); street screen parapet **4.1 m** (*photogrammetric*) |
| Footprint | 439.5 m², surveyed; 42.1 m deep on the SW party line, 19.4 m of exposed street elevation in five facets |
| Axis | body runs 315.1°/135.1°; street facets face **86.0°, 91.1°, 95.8°, 100.6°** with a **135.2°** chamfer at the south end |
| Triangle cap | 8,000 |
| Category | `3` (commercial/industrial — matches 150, 156, 160, 168 on the same rim) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 164 South Park GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of 164 South Park, San Francisco — the
single-storey warehouse behind Stanley Saitowitz's 2025 red-panel front — and
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
7. `artifacts/156-south-park/` — the closest reference implementation: same rim, same
   industrial type, same two-mass front-bar/rear-shed problem solved in the opposite
   direction
8. `artifacts/165-south-park/` — the reference for authoring directly on a measured
   world-space polygon rather than modelling a box and rotating it
9. `docs/asset-plans/164-south-park.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Must capture

- **The red plane.** A continuous wall of large-format red panels in **stretcher bond**,
  ~0.47 m course height, wrapping all 19.4 m of exposed street elevation in five facets.
  This is the only saturated red on the South Park rim and it is the entire recognition.
  Do not break it into bays, do not add a cornice, do not add brick texture.
- **The ribbon window.** One continuous black-framed horizontal band, sill 1.55 m,
  head 2.95 m, running the whole frontage, *mitring around each facet corner* rather
  than stopping and restarting. It is a ribbon, not a row of windows.
- **The drop.** At the north end of the frontage the ribbon does not stop — it drops to
  the ground and becomes a full-height glazed **entry recess** set ~1.0 m back into the red
  plane, wrapping an outside corner. This move is the building's signature and the reason
  the facade exists; a modeller who ends the ribbon in a wall and punches a separate door
  has failed.
- **The canopy.** A thin black blade, soffit at ~2.98 m, projecting ~1.5 m over the entry,
  carried on small black outriggers bolted through the red panel above. Pale metal
  numerals **164** on its outer fascia.
- **The step.** The red screen parapet stands at **4.1 m**. The retained warehouse behind
  it stands at **5.4 m**. The screen is LOWER than its own building, so from the app's
  aerial camera you see the red band, then a shadow gap, then the pale roof behind it.
  This inversion is measured, it is unusual, and it is the massing.
- **The roof.** Flat pale membrane at 5.1 m inside a 5.4 m parapet, with four glazed
  skylight monitors in two staggered rows and two small mechanical boxes. The camera looks
  down; this is a facade.
- **The depth.** 42 m of party wall running back from a 19 m frontage. From above the
  building is a long blind wedge, not a shopfront.

## Research 164 South Park independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- The street (east/south-east) elevation — the only elevation the public ever sees
- The roof from above: membrane colour, parapet profile, skylight count and placement,
  mechanical plant. Photograph-confirmed from aerial imagery in 2.9; re-confirm.
- The two party flanks (SW to 166 South Park, N to 160 South Park), which are blind
- The rear (NW) wall onto the mid-block gap
- Day and night appearance, and how much of the interior is visible through the ribbon
- The panel module: course height, bond offset, joint reveal depth

Prefer DataSF datasets, SF Planning/DBI records, assessor data, the architect's own
project page, geolocated photography and aerial imagery. Never rely on a single
photograph, a single AI-generated image, or a single unsourced 3D model. Separate
verified facts from visual inference; if sources disagree, document the disagreement
and decide.

**Five source problems are already known and resolved in 2.1–2.3 and 2.15 — re-check them,
do not silently re-inherit the wrong value:**

1. **`hgt_maxcm = 925` (9.25 m) is NOT this building's height.** The DataSF LiDAR record
   for `SF3775069` has median 5.44 m, modal 4.61 m and standard deviation 0.84 m over 1,715
   cells — a tight, flat, single-storey distribution — with a 9.25 m outlier. The assessor
   records **one storey** on both parcels; aerial imagery shows an unbroken flat roof with
   no second-storey volume; the neighbouring 2-storey buildings at 160 and 166 visibly
   overtop it. Use **5.4 m**. This is the exact inverse of the 156 South Park case
   (`docs/asset-plans/156-south-park.md` §2.15), where the maximum *was* real.
2. **OSM `way/124884357` tags `height = 5`, sourced from Bing.** It is the right order of
   magnitude by luck, not by measurement. Its geometry is also a coarse single blob 6.4%
   larger than the surveyed parcels. Use the DataSF parcels for the footprint.
3. **164 South Park is TWO parcels, `3775068` and `3775069`, both addressed 164.** One
   building spans both. Do not model half the site; do not treat 3775068 as a neighbour.
   (Assessor: 3775069 = 1907, 3,170 sq ft, 1 storey; 3775068 = 1946, 1,581 sq ft, 1 storey.)
4. **The commercial listings disagree with themselves.** Showcase says 7,400 sq ft and
   "2-story"; Compass says 3,170 sq ft and 1 story; CNBC and Business Insider say the
   Twitter room was 6,400 sq ft. The assessor's two records sum to 4,751 sq ft of
   *assessed* area on a 439.5 m² (4,730 sq ft) site — a one-storey building that covers
   its lot. The "2-story" is a listing error. Ignore it.
5. **The red facade is 2025 work and post-dates every aerial and Street View capture you
   will find.** The 2010 LiDAR, the DataSF footprint and the satellite imagery all show the
   *previous* front. DBI permit `202305248506` (Natoma Architects, issued 2024-05-03,
   $179,615) and `202406104101` (Atrium Structural, 2024-06-21) are the work. Trust the
   architect's photographs for the facade and the LiDAR/aerial only for the mass behind it.

## Create a reference dossier

Write `artifacts/164-south-park/REFERENCE.md` containing: source links and what each
establishes; verified dimensions and location; orientation; observations from all
four sides and above; the 3–5 strongest recognition cues; features to preserve;
features to simplify; uncertainties and conflicting evidence. A contact sheet of
attributed reference thumbnails is welcome if legally permissible — do not commit
copyrighted full-resolution imagery.

## Make your own design decisions

Follow the conversion process in `docs/styles/miniature-toy.md` §22: identify the
recognition cues, strip nonessential information, rebuild the massing from a few
confident volumes, exaggerate only the signature features, simplify the facade
into broad rhythms, deliberately design every surface visible from above,
evaluate from the app's high three-quarter aerial camera, then simplify again.

This is a **secondary** building in the style bible's detail budget (§21) — it earns one
tier above background because the facade is a designed object, not a vernacular one. Two
clean volumes, one uninterrupted ribbon, one recess, one canopy, one designed roof. Resist
adding ornament of any kind; the real building has none.

The finished asset must be immediately recognizable as this building, consistent with the
real one from all four sides and above, architecturally credible, and a premium
handcrafted miniature — not photorealistic, not voxel art, not generic low-poly, and never
accurate in one view while invented in the others.

## Scope of the exported asset

Export the single building: the warehouse volume on the measured footprint with its flat
roof, parapet, skylights and mechanical boxes; the red panel screen on the exposed street
elevation with its coursing reveals; the ribbon window; the entry recess and its glazing
and doors; the canopy, its outriggers and the numerals.

Do not include unrelated surrounding city geometry: 160 South Park, 166–168 South Park,
the South Park oval or its lawn and trees, the street, the sidewalk, the four street trees
in front of the facade, the utility pole, parked cars, people, plinths, cameras or lights.
The concrete doormat inscription is *sidewalk*, not building — leave it out. Temporary
context may appear in review renders but must not leak into the GLB.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary
`.glb`; real-world meters; origin at base center; minimum geometry Z ~ 0;
applied transforms; no negative scales; outward normals; no duplicate or foreign
geometry; no image textures; no transparency; flat-color materials named `Toy_*`
from the project palette; `_Glow` suffix only on surfaces that glow at night; no
`Toy_body`; no cameras, lights, animations, armatures or constraints; at most
8,000 triangles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model
drops into the city at its real-world heading — the loader applies no rotation
(`placeGeneric` in `app/src/assets.js` only scales and positions). Build directly on the
measured polygon in 2.3. Derive "outward" from the polygon winding or from the facet's own
middle segment, never from the building centroid — this footprint has a 135° chamfer and a
15° arc, and a centroid-derived normal folds at both (see `docs/asset-plans/168-south-park.md`
and the offset-handedness note in 2.7). Record the measured facet headings in `REPORT.md`.

**Height normalization:** the tallest geometry in the export (the rear parapet crest) must
land at exactly **5.4 m** so the loader's `targetHeightM / measuredHeight` scale is 1.0.
Nothing — no skylight monitor, no mechanical box, no canopy — may exceed it.

## Reproducible Blender workflow

Blender 5.2 LTS. Headless: `blender -b --python script.py -- args`.

Keep `artifacts/164-south-park/build_164_south_park.py` (deterministic build script),
`artifacts/164-south-park/164-south-park.blend`, and
`artifacts/164-south-park/164-south-park.glb`. The script must rebuild the model reliably
enough for future revision. Do not modify or rename an unrelated existing GLB to satisfy
the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`164-south-park-top.png`, `-north.png`, `-east.png`, `-south.png`, `-west.png`, plus
`164-south-park-contact-sheet.png`, at least one high three-quarter aerial beauty
render `164-south-park-aerial.png`, and a night render
`164-south-park-aerial-night.png`.

The four elevations must share scale, framing, lighting, exposure and projection; use
orthographic or long-lens cameras; label directions from the researched orientation; the
top view must clearly show the roof plane, the parapet, the skylights and the 1.3 m step
down to the red screen; the aerial view uses the style bible's camera assumptions (30–50
degrees down, long lens). Simple tabletop lighting, neutral warm background, minimal depth
of field, and every image must depict the same exported model.

Because the building is a 42 m wedge presented at 45° to the world axes, frame the
elevations to the long dimension and accept empty frame on the short views rather than
zooming each view to fit — the reviewer needs to be able to compare them.

**Review the high three-quarter aerial FIRST and iterate there before running the formal
elevation rig.** The two questions that view has to answer are: does the red band read as
one continuous plane, and is the step down from the roof legible as a designed move rather
than as a modelling error?

## Validate the exported GLB

Re-import `164-south-park.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture
count, camera count, light count, animation count, applied-transform status,
negative-scale status, normal-orientation status, unexpected geometry, and
per-material contract compliance. Render at least one review image from the
re-imported asset. Write `artifacts/164-south-park/validation.json` and
`artifacts/164-south-park/REPORT.md`.

Note that the axis-aligned XY bounding box will be roughly **35.7 × 36.2 m** even though
the building is a 42 × 16 m wedge — that is the expected consequence of the 45° real-world
heading, not a scale error.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "164-south-park",
  "file": "164-south-park.glb",
  "anchor": [
    -122.3949238,
    37.7812072
  ],
  "targetHeightM": 5.4,
  "cat": 3,
  "name": "164 South Park",
  "estimated": true,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

`"estimated": true` is deliberate — no published height exists and the crest is the LiDAR
median rather than a surveyed figure. See 2.15.

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a separate, explicitly requested job — run `docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in `docs/asset-plans/164-south-park.md`.
````

---

## Part 2 — Research and design dossier

Method and confidence conventions follow `docs/asset-plans/README.md`. Every row below is
labelled **measured** (from a primary dataset or from geometry I computed myself),
**observed** (read off a photograph), **photogrammetric** (computed from a photograph with
a stated scale reference), or **inferred**.

### 2.1 Verified facts

| Fact | Value | Source / confidence |
|---|---|---|
| Address | 164 South Park (also published as 164 S Park St and 164 South Park Ave), SF 94107 | DataSF parcels, assessor, architect — **measured** |
| Parcels | block 3775, lots **068** and **069**, *both* addressed 164 | DataSF `acdm-wktn` — **measured** |
| Site area | **439.5 m²** (4,731 sq ft), the union of the two lots | computed from the DataSF parcel polygons — **measured** |
| Year built | **1907** (lot 069) and **1946** (lot 068) | SF Assessor `wv5m-vpq2`, 2025 roll — **measured** |
| Storeys | **1** on both parcels | SF Assessor — **measured** |
| Use / class | Industrial (`IND`), class `I`; zoning `SPD` | SF Assessor — **measured** |
| Assessed area | 3,170 sq ft (069) + 1,581 sq ft (068) = 4,751 sq ft | SF Assessor — **measured** |
| Facade architect | **Stanley Saitowitz \| Natoma Architects** | architect's project page — **measured** |
| Facade date | permit issued 2024-05-03, photographed complete 2025-05-26 | DBI permit `202305248506`; architect photo EXIF dates — **measured** |
| Facade material | large-format red panels, **stretcher bond**; black ribbon window; slender canopy | architect's own project text — **measured** |
| Historical significance | Twitter's first office 2006–2008; Instagram 2010; inscribed in the entry sidewalk | CNBC 2018, Business Insider 2021, architect — **measured** |
| Roof (LiDAR) | median **5.44 m**, modal 4.61 m, mean 5.53 m, sd **0.84 m**, min 3.24 m, max 9.25 m, over 1,715 cells at 50 cm | DataSF `ynuv-fyni`, `mblr = SF3775069` — **measured** |
| Ground elevation | 6.31 m NAVD88 (`gnd_min_m`) | DataSF — **measured**; the app's terrain handles this, not the asset |
| **Target height** | **5.4 m** rear parapet crest | LiDAR median — **measured**, see 2.15 |
| Street screen parapet | **4.1 m** | **photogrammetric**, two independent photographs, §2.3 |
| Ribbon window sill / head | **1.55 m / 2.95 m** | **photogrammetric** |
| Canopy soffit | **2.98 m** | **photogrammetric** |
| Panel course | **0.47 m** | **photogrammetric** — 8.7 uniform courses between grade and parapet |
| OSM way | `way/124884357`, `height = 5`, `source = Bing` | OSM — **measured** that the tag exists; the value is not trustworthy |

### 2.2 Sources

Exa searches run 2026-08-18. Queries and what each yielded:

- `164 South Park San Francisco building` (10 results, summaries on) — found
  **`saitowitz.com/164-south-park`**, the architect's own project page, which is the single
  most valuable source here: it states the design intent verbatim ("large scale red panels
  in stretcher bond", "a ribbon window tracks the shift around the oval, dropping to form
  the glazed entry recess", "a slender canopy shelters the front", "the doormat remembers
  the building's history") and carries 14 project photographs.
  Also `compass.com` (1907, 1 story, 3,170 sq ft, lot 3,275 sq ft, SPD),
  `cityfeet.com` and `showcase.com` (7,400 sq ft, class C, "recently remodeled facade by
  Stanley Saitowicz", "new foundation for the front half" — *observed (listing photo)*, and
  the "2-story" here is wrong, see 2.15), `openpermitdata.com/sf/address/164-south-park`
  (three permits, Natoma Architects and Atrium Structural, 2024).
- `Stanley Saitowitz Natoma Architects 164 South Park facade red panels ribbon window photos`
  (8 results, highlights on) — confirmed the project text and the firm's catalogue listing.
- Tenant history: `cnbc.com/2018/06/04/photos-of-twitters-first-offices.html` (Twitter at
  164 South Park Ave, 6,400 sq ft, 2006–2008),
  `businessinsider.com/startup-rent-office-in-silicon-valley-where-instagram-twitter-started-2021-9`
  ("warehouse-like, light-starved space with two skylights and small glass windows" —
  the skylights are corroborated from the air, see 2.9),
  `businessinsider.com/photos-san-francisco-office-instagram-twitter-available-rent-2021-10`.
- `opengovus.com` business registrations at 164 South Park St: Nus America Inc. dba
  **Block 71 San Francisco** (2016–2021), Ambit Analytics Inc. (2018–2019).

Photographs used for the photogrammetry in 2.3, all from `saitowitz.com/164-south-park`
(© Stanley Saitowitz | Natoma Architects; URLs recorded, images not committed):

| File | What it establishes |
|---|---|
| `001.jpg` | The whole street elevation straight on, with the entry doors in frame — the primary scale reference |
| `002.jpg` | Near-orthographic elevation of the southern facade: uniform 0.47 m coursing, ribbon proportions, the old wall standing above the screen |
| `003.jpg` | The south end where the red panel meets the brick neighbour |
| `005b.jpg`, `005c.jpg` | The entry from the north — canopy, outriggers, numerals, recess depth, corner-wrapping glazing |
| `022b.jpg` | The full frontage raking from the south: proves the screen parapet is level, shows all five facets |
| `023.jpg` | The frontage raking from the south-east: the chamfer and the ribbon's mitred corners |
| `025.jpg` | Oblique close-up of the panel grid and joint reveals |
| `20250526_191305049`, `_191348966`, `_191412380` | Entry recess interior/exterior, canopy soffit, numerals on the fascia, the sidewalk inscription |
| `20250526_201111127`, `_201212438`, `_201430930` | Interior — how much of the ceiling and floor is visible through the ribbon, which is what the night glow has to imply |

Aerial imagery: Google satellite z21 tiles (roof form, skylight count and placement,
mechanical boxes, party-wall relationships) and Esri World Imagery z20 (cross-check).
Geometry: DataSF parcels `acdm-wktn`, DataSF LiDAR building footprints `ynuv-fyni`,
OSM `way/124884357` and the South Park highway ways (for the frontage test in 2.3).

### 2.3 Orientation and placement

**Anchor (manifest / placement): `-122.3949238, 37.7812072`** — the area centroid of the
union of the two surveyed parcels. **measured.**

The union is a 9-vertex polygon, 439.5 m². Design footprint, metres east/north from the
anchor (this is the polygon to build on — Blender `+X` east, `+Y` north):

```
v0  (-19.725,  12.057)   rear-west corner
v1  (  9.974, -17.722)   south corner, street end of the SW party line
v2  ( 15.275, -12.461)   south end of the frontage arc
v3  ( 15.061,  -9.380)
v4  ( 15.117,  -6.321)
v5  ( 15.395,  -3.595)
v6  ( 15.957,  -0.586)   north corner of the frontage
v7  (  3.482,   1.704)   north party corner with 160 South Park
v8  (-13.260,  18.491)   rear-north corner
```

Edges, with outward normals computed from the polygon winding (**not** from the centroid —
see 2.7):

| Edge | Length | Faces | Condition |
|---|---|---|---|
| v0→v1 | 42.06 m | 225.1° SW | party wall with **166 South Park** (lot 070) — blind |
| v1→v2 | 7.47 m | 135.2° SE | **exposed** — the chamfer at the south end of the frontage |
| v2→v3 | 3.09 m | 86.0° E | **exposed** — arc facet 1 |
| v3→v4 | 3.06 m | 91.1° E | **exposed** — arc facet 2 |
| v4→v5 | 2.74 m | 95.8° E | **exposed** — arc facet 3 |
| v5→v6 | 3.06 m | 100.6° E | **exposed** — arc facet 4 |
| v6→v7 | 12.68 m | 10.4° N | party line with **160 South Park** (lot 067) |
| v7→v8 | 23.71 m | 45.1° NE | rear flank onto the mid-block gap |
| v8→v0 | 9.12 m | 315.1° NW | rear wall |

Total exposed street elevation **19.4 m**, in five planes turning through 49°. The arc
facets are the "shift around the oval" the architect names: South Park's road wraps the
west tip of the oval immediately east of this lot, and the lot line follows it. Measured
against the OSM South Park centreline, the arc facet midpoints sit 5.25–5.98 m out and the
chamfer 8.96 m; every other edge is ≥ 11.5 m and is a party or rear condition. **measured.**

Cross-checks on the footprint:

- The DataSF LiDAR building footprint `SF3775069` (423.8 m², 11 vertices) has an
  **IoU of 0.895** with the parcel union and its centroid is 0.96 m away. Two independent
  sources, one shape. Use the parcels — they are surveyed, and the LiDAR raster carries
  registration error.
- OSM `way/124884357` (468 m², Bing trace) is 6.4% larger and its centroid is 2.60 m away.
  It agrees on the general shape and on the faceted street end, and it is the source the
  bake gap-fills from, which is why it matters in 2.13 — but it is not the modelling
  geometry.

**The entry is at the NORTH end of the frontage.** This was worth pinning down because the
whole facade composition hangs off it, and three independent readings agree:

1. In `001.jpg`, shot square from across the street (camera facing west, so north is to the
   right), the entry sits about a quarter of the way in from the right-hand end, with a
   brick neighbour beyond the left end. 166 South Park (lot 070, 1912, "Flat & Store") is
   the south neighbour and is brick; 160 South Park (lot 067, 1924) is the north one.
2. In `20250526_191412380`, shot from inside the entry recess looking out along the
   facade, a Bay Wheels dock and its shelter are visible in the direction the facade runs
   away. The only Bay Wheels station within 200 m is 42 m away on a bearing of **172°** —
   due south. The facade therefore runs south from the entry.
3. The entry glazing wraps an outside corner (`20250526_191348966`), which places it on the
   v5 facet corner, 3.06 m south of v6.

Design placement: the entry recess spans **1.9 m to 5.5 m south of v6**, straddling the v5
corner, leaving a 1.9 m red pier between it and the north party line. The ribbon window
then runs continuously from 5.5 m south of v6 all the way around the arc and across the
chamfer to v1 — **13.9 m of unbroken glass in five mitred planes.**

**Vertical scheme** (all heights above the model's z = 0, which the loader seats on terrain):

| Element | Height | Confidence |
|---|---|---|
| Screen parapet crest | **4.10 m** | photogrammetric (see below) |
| Ribbon window sill | 1.55 m | photogrammetric |
| Ribbon window head | 2.95 m | photogrammetric |
| Canopy soffit / blade top | 2.98 m / 3.12 m | photogrammetric |
| Entry glazing head | 3.50 m | inferred |
| Warehouse roof deck | 5.10 m | inferred (parapet crest less a 0.30 m lip) |
| **Rear parapet crest = target height** | **5.40 m** | measured (LiDAR median 5.44 m) |

The 4.10 m screen parapet is the one number in this plan that comes only from photographs,
so here is the working. Both photographs put a vertical of known height (a commercial door
leaf, 2.134 m) and the screen parapet in the same frame, which fixes the horizon and makes
the result almost independent of the assumed camera height:

- `005c.jpg`: door threshold y = 1720 px, door head y = 1195 px, pier base y = 1790 px,
  parapet y = 595 px → **4.11 m** at eye height 1.55 m, **4.14 m** at 1.65 m.
- `001.jpg`: door bottom y = 722 px, door head y = 540 px, pier base y = 742 px,
  parapet y = 348 px → **4.01 m** at 1.55 m, **4.04 m** at 1.65 m.

Two photographs, two camera positions, 4.0–4.1 m. Take **4.10 m**. The same construction
gives the canopy soffit at 2.87–3.09 m (take 2.98 m), and `002.jpg` — near-orthographic,
long lens, with a uniform 116 px panel course over its whole height — fixes the ribbon at
0.382 H and 0.721 H, i.e. sill 1.57 m and head 2.96 m.

`022b.jpg` is the check that the parapet is **level**: over the three sample columns its
apparent wall height falls 700 → 670 → 610 px purely in step with the receding base line,
so there is no step in the parapet along the frontage. Model it flat.

### 2.4 What each side shows

- **East / south-east (the street elevation, 19.4 m in five planes).** The entire design.
  Red panel plane from grade to 4.10 m, unbroken except by the ribbon and the recess.
  Horizontal joint reveals every 0.47 m, vertical joints offset half a panel course to
  course (stretcher bond); the panels are roughly 1.4 m long. Ribbon window 1.55–2.95 m,
  black frame, mitred at each facet corner. Entry recess 3.6 m wide, 1.0 m deep, glazed
  floor-to-3.5 m, wrapping the v5 corner, with black double doors and a transom. Canopy
  blade over it at 2.98 m, four outriggers, **164** in pale metal on its fascia. Above the
  4.10 m parapet, a 1.3 m gap and then the pale roof and the 5.40 m rear parapet.
- **South-west (42.06 m).** Party wall with 166 South Park. Blind old brick, no openings.
  The neighbour is two storeys and overtops it, so in the city this face is almost never
  seen; model it as a plain brick plane with the parapet lip and nothing else.
- **North (12.68 m).** Party line with 160 South Park, also blind brick. The red screen
  returns about 0.4 m around the v6 corner and stops — the panel system is a front, not a
  wrap, and this is where you can see that.
- **North-east (23.71 m) and north-west (9.12 m).** Rear flank and rear wall onto the
  mid-block gap. Blind brick, one steel roll-up door at the rear implied by the service
  access visible from the air. Low visual priority.
- **From above.** The most important view. See 2.9.

### 2.5 Recognition cues (ranked)

1. **The red plane** — the only saturated red facade on the South Park rim, and it is
   low, so from the air it reads as a red bar lying against a pale roof. If a viewer can
   find only one thing about this building, it is this.
2. **The step down.** The street screen is 1.3 m *shorter* than the building behind it.
   Every other building on the rim presents its tallest face to the park. This one does not,
   and the shadow line between the red band and the pale roof is the tell.
3. **The ribbon that becomes a door.** One continuous band of glass that drops to the
   ground at the north end. Reads at mid-range and is the design's whole idea.
4. **The canopy blade and the numerals.** A thin dark horizontal shelf at 3 m with pale
   **164** on its edge — the only text on the building, and the one close-range cue.
5. **The wedge.** 19 m of frontage, 42 m of depth, tapering. From directly above the
   building is a long blind triangle with a red lip on its short end.

### 2.6 Miniature translation

The style bible's conversion (§22) applied here:

- **Strip.** The panel joints are 8 mm reveals on a 0.47 m module — 8.7 courses over the
  parapet. At the app's aerial scale that is noise. Keep the *rhythm*, drop the *count*:
  cut a 0.05 m reveal every **0.94 m** (every second real course), giving four bands. The
  bond offset survives as a single staggered vertical joint per band, not as a real pattern.
- **Exaggerate.** The step between the screen (4.10 m) and the rear parapet (5.40 m) is the
  massing cue and it is only 1.3 m. Do **not** exaggerate the heights — AGENTS rule 5 —
  but *do* pull the screen 0.35 m proud of the wall it hides, so the step reads as two
  separate objects with a shadow between them rather than as one wall with a setback.
  That thickness is real (a rainscreen cavity plus panel) and it does the work.
- **Exaggerate.** The canopy in reality projects ~1.5 m and is ~0.10 m thick. At miniature
  scale a 0.10 m blade disappears. Take it to **0.14 m** and give it a crisp 0.02 m bevel;
  it is the only thing casting a shadow on the facade.
- **Simplify.** The real ribbon has intermediate mullions roughly every 1.6 m. Keep them,
  but as 0.06 m black bars in the plane of the frame — enough to read as glazing, not
  enough to break the band.
- **Design the roof.** See 2.9. Four skylight monitors, two mechanical boxes, a parapet
  lip. Nothing else.
- **Resist.** No cornice, no plinth, no signage band, no planters, no street furniture.
  The real building has none of these and the design is an exercise in having none.

### 2.7 Massing recipe

Two volumes and four attachments.

1. **Body.** Extrude the 9-vertex footprint from z = 0 to the roof deck at **5.10 m**.
   Material `Toy_brick`. Add a parapet lip 0.22 m wide around the whole perimeter, top at
   **5.40 m** — this is the bbox top and the manifest height.
2. **Screen.** Along the five exposed edges only (v1→v2 through v5→v6), a wall standing
   **0.35 m proud** of the body face, from z = 0 to **4.10 m**, material `Toy_red`.
   Return it 0.40 m around the v6 corner onto the north party line and 0.40 m around the v1
   corner onto the SW party line, then stop. Mitre it at every facet corner.
   **Build the offsets from each edge's own outward normal (winding-derived) or from the
   facet's middle segment. A centroid-derived "outward" folds at the 135.2° chamfer and at
   the 49° of arc, and the normals test will fail.**
3. **Ribbon.** A rectangular void through the screen, sill 1.55 m to head 2.95 m, running
   from 5.5 m south of v6 continuously to v1. Recess the glass 0.12 m behind the panel face,
   frame it with a 0.08 m `Toy_ink` surround, and mitre the frame at each facet corner so it
   reads as one band. Mullions: `Toy_ink` bars 0.06 m wide at ~1.6 m centres.
4. **Entry recess.** From 1.9 m to 5.5 m south of v6, cut the screen full height (0 to
   4.10 m) and set the glazed plane **1.0 m** back, wrapping the v5 corner. Glass 0 to
   3.50 m, `Toy_glass` behind a `Toy_ink` frame; a pair of doors 1.90 m wide, 2.35 m to the
   transom rail, in the middle. Panel returns on both reveals in `Toy_red`.
5. **Canopy.** A blade 4.40 m long (0.4 m past the recess each side) × 1.50 m deep ×
   0.14 m thick, soffit at 2.98 m, `Toy_ink`, projecting from the screen face. Four
   outriggers 0.10 × 0.10 × 0.55 m on top of it, back to the panel. `Toy_trim` numerals
   **164** on the outer fascia, 0.09 m tall, extruded 0.02 m. Keep the numerals as extruded
   solids, not a texture.
6. **Roof furniture.** Four skylight monitors and two mechanical boxes, per 2.9.

Expected triangles: body + parapet ≈ 900; screen with reveals and returns ≈ 1,800; ribbon
frame and mullions ≈ 1,400; entry recess and doors ≈ 900; canopy, outriggers, numerals ≈
900; roof furniture ≈ 1,200; bevels ≈ 600. **≈ 7,700, inside the 8,000 cap.**

### 2.8 Materials and palette

All from the project palette; no off-palette colour is needed here, which is unusual and
welcome.

| Material | Hex | Where |
|---|---|---|
| `Toy_red` | `c4453c` | the screen panels — the hero surface, and nothing else |
| `Toy_brick` | `c96f4a` | the retained warehouse walls: both party flanks, the rear, and the strip of body visible above the screen |
| `Toy_ink` | `3a3530` | ribbon frame and mullions, entry frame and doors, the canopy and its outriggers |
| `Toy_glass` | `2a4d73` | ribbon glazing and entry glazing, daytime |
| `Toy_steel` | `9aa0a6` | roof membrane, skylight frames, mechanical boxes |
| `Toy_trim` | `f3efe6` | the **164** numerals, and the parapet coping caps |
| `Toy_glass_Glow` | `6f95b8` | ribbon + entry glazing at night — the hero glow |
| `Toy_trim_Glow` | `f3efe6` | a single thin spill panel on the canopy soffit |

The measured facade colour is worth recording because the palette match is unusually good:
sampling `002.jpg` and `001.jpg` gives `#C44B38` in full sun and `#A63F32` in shade. The
palette's `Toy_red` is `#c4453c`. That is the sunlit sample to within two units per channel,
so no off-palette entry is justified — use `Toy_red` as authored.

**Do not use `Toy_roofd` for the roof deck.** On a flat roof under the app's lighting it
renders at roughly `rgb(9,9,12)` — a black hole where a pale membrane should be. `Toy_steel`
is the correct choice and it also happens to be right: the real roof is a pale grey-white
membrane (aerial, 2.9).

**Glow discipline.** `_Glow` surfaces are rendered in a separate layer that is roughly 12%
alpha by day *per surface*, so a closed shell is two layers and reads at ~23% — enough to
tint the whole facade pink in daylight. Author every glow surface as a **single-sided shell
0.01 m proud of the opaque glazing**, never as a box, and never make a primary surface a
glow material. The glow colour is what you see at night — it is unlit — so `6f95b8` must be
chosen to look right on its own, not to look right multiplied by an emission strength in the
Blender rig.

Night composition: the ribbon and the entry are one continuous lit band, which is exactly
the daytime idea seen at night; the canopy soffit spill is the single supporting accent.
Nothing else glows. The roof does not glow.

### 2.9 Top surface

From Google satellite z21, the roof is a **flat pale grey-white membrane** filling the whole
footprint, with:

- **Four glazed skylight monitors**, rectangular, mullioned into roughly 3 × 4 panes,
  arranged in two staggered rows running with the long axis. These are the "two skylights"
  the Business Insider piece describes from inside — there are four from above. Model them
  as low boxes, 2.4 × 1.4 m, 0.35 m tall, `Toy_steel` frames with `Toy_glass` tops.
- **Two small mechanical boxes** near the north-east flank, roughly 1.2 × 0.9 × 0.6 m,
  `Toy_steel`.
- A continuous **parapet lip** 0.22 m wide, crest 5.40 m, deck 5.10 m — a 0.30 m upstand.
  Cap it in `Toy_trim`.

Nothing on the roof may exceed 5.40 m; the monitors at 0.35 m above a 5.10 m deck top out at
5.45 m as drawn, so **drop the deck under the monitors or shorten them to 0.28 m** — the
crest must be the parapet. Record which you chose in `REPORT.md`.

The skylights are the reason to bother with the roof at all: they are what makes a blind
warehouse read as a *daylit* warehouse from the app's camera, and they are the physical
reason the Twitter room was famous for being dark except for two bright patches.

### 2.10 Scope

In: the building, its screen, its ribbon, its entry, its canopy, its roof furniture.
Out: neighbours, the oval, the lawn, the four street trees on the frontage (they are real
and they are in every photograph, but they are the app's street-tree system's job), the
utility pole and its wires, the sidewalk and its inscription, cars, people.

### 2.11 Triangle budget

Cap **8,000**. Estimate in 2.7 is ≈ 7,700. If it runs over, the first thing to cut is the
number of ribbon mullions, then the skylight pane divisions. Do not cut the coursing
reveals or the screen's 0.35 m offset — those are the two things carrying the design.

### 2.12 Draft manifest entry

```json
{
  "id": "164-south-park",
  "file": "164-south-park.glb",
  "anchor": [-122.3949238, 37.7812072],
  "targetHeightM": 5.4,
  "cat": 3,
  "name": "164 South Park",
  "estimated": true,
  "dims": [<measured>, <measured>, 5.4],
  "tris": <measured>,
  "loadRadius": 2500
}
```

`loadRadius` 2500 is the default rule `max(2500, 5.4 × 30)` — a 5.4 m building never needs
more. Streamed, not `alwaysLoaded`.

### 2.13 Integration notes (for later, not this task)

**Case B.** No `164SouthPark` id exists in `pipeline/lib/landmarks.mjs` or
`app/src/landmarks.js`, so the baked city still carries a procedural block on this footprint
and the registry needs a new entry plus a re-bake.

**MEASURED OUTCOME (stage 5) — the plan's recommendation was superseded.** The paragraphs
below record what was actually measured against the bake's own input, which is what the
registry now carries. The earlier draft recommended a separate registry anchor at the OSM way
centroid with `exclude: 3`; measuring against the real input rather than the live APIs showed
the **manifest anchor itself gives the widest window**, so there is only one anchor here and
no second number to explain.

`excluded()` in `pipeline/buildings.mjs` drops a footprint when its area centroid **or any
ring vertex** falls inside the circle, and the bake reads DataSF first and gap-fills from
Overture, so both sources bind. Measured from the manifest anchor `-122.3949366, 37.7812097`
against `pipeline/data/buildings_datasf.geojson` and
`pipeline/data/overture_buildings.geojsonseq`, both simplified at the bake's own
`SIMPLIFY_TOLERANCE = 0.6`, with neighbours already dropped by an existing landmark's
exclusion discounted (a GLB stands in their place):

| Ring | Nearest vertex | Centroid | Role |
|---|---|---|---|
| DataSF `SF3775069` (ours, 419 m²) | 3.06 m | **0.60 m** | own footprint |
| Overture 469 m² (ours) | 3.76 m | **1.43 m** | own footprint — **the floor** |
| DataSF `SF3775067` (160 South Park) | 3.06 m | 9.67 m | already dropped by `160SouthPark` |
| Overture 76 m² (OSM "158 South Park" sliver) | **3.76 m** | 10.36 m | **the ceiling** — uncovered |
| everything else | ≥ 8.57 m | | covered by 156 / 168 / 188 `SouthPark` |

Safe window **(1.43, 3.76)**, 2.33 m wide. **`exclude: 2.6`** sits in the middle with 1.17 m
below and 1.16 m above, both comfortably over the 0.6 m simplify tolerance. Below 1.43 the
Overture ring survives and the procedural block pokes through the model; above 3.76 the
re-bake punches a hole where the 158 sliver stands and nothing fills it.

The binding ceiling is worth naming: OSM `way/124884344`, tagged `addr:housenumber = 158`,
a 76 m² fragment that **shares a party-wall vertex with our own Overture ring** and is not
covered by `160SouthPark`'s `exclude: 1.2`. It is the same shared-vertex trap that made
`181SouthPark`'s window 2.9 m wide.

Candidate anchors compared, for the record (floor → ceiling, both measured the same way):

| Anchor | Floor | Ceiling | Window |
|---|---|---|---|
| parcel-union area centroid | 2.54 m | 3.45 m | 0.92 m |
| DataSF LiDAR centroid | 1.59 m | 3.32 m | 1.73 m |
| OSM way centroid | 1.86 m | 4.06 m | 2.21 m |
| **manifest anchor (chosen)** | **1.43 m** | **3.76 m** | **2.33 m** |

No `clearTrees`: there are four real street trees on this frontage — they are in every
photograph and they belong to the app's tree system.

Suggested camera preset: the facade faces roughly 95°, so `camera.js` (eye at
target + distance·(sin yaw, ·, cos yaw), bearing = 180 − yaw) wants **yaw 85**, standing out
over the oval. 120 m suits a 5.4 m building — the shortest landmark on this rim, so pull in
closer than the 150–170 m used for the 9–10 m neighbours.

```js
{ id: '164SouthPark', name: '164 South Park', lon: -122.3949366, lat: 37.7812097,
  height: 5.4, exclude: 2.6, camera: { distance: 120, yaw: 85, pitch: 26 } }
```

**Batch mode applies.** Other South Park landmarks are in flight; run the bake and the full
QA, then `git checkout -- app/public/tiles api/_data` before committing, per
`docs/asset-pipeline/ADDRESS-TO-ASSET.md`.

### 2.14 Validation checklist

- [ ] Re-imported into a fresh scene; every check run on the re-import
- [ ] ≤ 8,000 triangles
- [ ] bbox top **exactly 5.400 m**; min Z 0.000; XY centre offset ≈ 0
- [ ] AABB ≈ 35.7 × 36.2 m (expected — 45° heading, not a scale error)
- [ ] Materials exactly the eight in 2.8; no textures, no transparency, no `Toy_body`
- [ ] `_Glow` only on the ribbon shell, the entry shell and the canopy soffit spill; all
      single-sided, 0.01 m proud, none of them a primary surface
- [ ] Normals outward: per-object signed volume for the union-of-solids, ray test residual
      ≤ 0.15%
- [ ] Screen offsets built from winding-derived normals; no folded facet at v1 or across the arc
- [ ] Nothing on the roof above 5.400 m
- [ ] No cameras, lights, animations, armatures; transforms applied; no negative scale
- [ ] Night render present; day and night contact-sheet tiles present
- [ ] Aerial three-quarter reviewed *before* the formal rig, and the iteration logged

### 2.15 Open questions and risks

**The height, and why this plan overrules the LiDAR maximum.** Every other South Park plan
in this set reaches for `hgt_maxcm` and this one refuses it, so the reasoning has to be
explicit.

`SF3775069` reports max 9.25 m, min 3.24 m, **median 5.44 m, modal 4.61 m, mean 5.53 m,
standard deviation 0.84 m** over 1,715 cells. A two-mass building — the 156 South Park case,
where a two-storey front bar reached the maximum and a shed sat at the median — produces a
*wide* distribution: 156's standard deviation is 1.14 m over a 5.7 m spread. This one is
0.84 m, and 0.84 m of spread cannot contain a 4 m step. The 9.25 m figure is a small number
of cells sitting well outside a tight, flat, single-storey distribution.

Four independent facts agree with the median and not the maximum:

1. The **assessor records one storey on both parcels** (`number_of_stories = 1.0`, 2025 roll).
2. **Aerial imagery** shows an unbroken flat membrane roof over the whole footprint with no
   second-storey volume anywhere on it.
3. The neighbours at 160 (LiDAR max 9.41 m, two storeys) and 166 (10.44 m, two storeys) are
   both **visibly taller** in the aerial — you can see their side walls and windows in plan,
   which only happens when a building overtops its neighbour.
4. **Photogrammetry** puts the new street screen at 4.1 m and the old wall standing behind
   it at 4.7–5.6 m, bracketing the median.

The residual risk: I have not identified *what* is at 9.25 m. The record's `peak_1st_m` is
16.53 m, which is a tree — there is a large tree overhanging the north-west end of this roof
in the aerial — and tree canopy is the most likely contaminant, with the taller party wall of
166 South Park bleeding into edge cells as the second candidate. Neither is a building mass
we should model. If a future source establishes a real 9.25 m element, the fix is a
**localised bulkhead**, not a rescale of the whole model.

**Other open items:**

- **The roof deck at 5.10 m is inferred**, as parapet crest less a 0.30 m upstand. Only the
  crest is measured (as the median). If the real upstand is taller the deck drops; nothing
  else in the model moves and the manifest height is unaffected.
- **The panel course at 0.47 m is photogrammetric**, derived from a uniform 116 px course in
  `002.jpg` scaled by the 4.10 m parapet. It is internally consistent (8.7 courses) but it is
  a derived number twice over. A specified panel size from the manufacturer would settle it.
  The design does not depend on it: 2.6 already halves the count for the miniature.
- **The number of ribbon mullions is observed, not counted** — the photographs are oblique
  and the reflections make it hard. ~1.6 m centres is a reading, not a count.
- **The rear (north-west) wall is unphotographed.** Nothing in the sources shows it. It is
  modelled as blind brick with a service door, which is what the aerial implies and what the
  type demands, and it is the weakest inference in this plan. It is also almost never visible
  in the app.
- **The listings' "2-story" claim** (Showcase, and by implication the 7,400 sq ft) is treated
  as an error against the assessor, the aerial and the LiDAR. If it turns out to describe a
  mezzanine — which the 1907 industrial type routinely has, and which would be invisible from
  outside — nothing in this plan changes.
- **The facade is one year old.** Every dataset used for the mass predates it. That is fine
  for the mass, which did not change, but it means no dataset will ever corroborate the
  screen: the architect's photographs are the only source, and the photogrammetry in 2.3 is
  the only measurement.
