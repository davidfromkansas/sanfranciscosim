# 101 Grove Street (Public Health Building) — SF-SIM asset plan

Samuel Heiman's 1931–32 granite headquarters for the San Francisco Department of
Public Health: a four-storey Beaux-Arts Classical block filling the Grove/Polk
corner of the Civic Center Historic District, one street north of City Hall and
one door east of the Bill Graham Civic Auditorium. Its identity is a single
gesture — a **chamfered corner entrance bay** carrying a monumental arched
doorway with a carved oculus, a gold-rosetted balconette above it, and a
pedimented window over that — under a continuous modillion cornice and open
balustrade. Everything else is disciplined ashlar rhythm.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/101-grove/`. This document is the plan only: Part 1 is the runnable
task prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `101-grove` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.4186747, 37.7781359` (footprint AABB centre, measured) |
| Target height | **21.4 m** (balustrade rail top; cornice/eave 20.3 m measured, balustrade *estimated*) |
| OSM footprint | 63.2 x 37.1 m oriented block on the 80.6 deg Civic Center grid, 2,274 m2 (OSM way/35176281, measured) |
| Triangle cap | 22,000 |
| Category | `18` (Government) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 101 Grove Street GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of 101 Grove Street (the San Francisco
Department of Public Health Building) and deliver it as a downloadable,
validated GLB.

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
8. `artifacts/war-memorial-opera-house/` — the closest sibling: the same
   Civic Center, the same 1932 granite Beaux-Arts family, the same palette
   spine (`Toy_stone` body, `Toy_trim` ornament). Match its family, do not
   invent a new one.
9. `docs/asset-plans/101-grove.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Must capture

- The **chamfered north-east corner bay** at Grove and Polk and its stacked
  composition: rusticated round-arched entrance with radiating voussoirs, a
  carved tympanum with a round oculus, a projecting balconette with a dark
  ground and gold rosettes, a pedimented window above it, a plain window above
  that, and the balustrade crowning it
- The **two-tone vertical order**: a tall rusticated ground-floor base under
  three storeys of smooth ashlar
- The **continuous modillion cornice and open balustrade** running the full
  Grove and Polk elevations — the single strongest horizontal
- The regular pedimented-window rhythm at second-floor level with its
  gold-rosetted balconettes
- The bright white flat roof (a modern cool-roof membrane over a 1932 block)
  with the low penthouse over the corner bay and the interior light court
- The two bronze lantern sconces flanking the entrance arch
- The plainer south (Dr. Tom Waddell Place) and west (light-court) elevations,
  which have the same ashlar grid without the ornament

## Research 101 Grove Street independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- North (Grove Street) and east (Polk Street) elevations — the two public faces
- The chamfered corner bay in detail
- **South (Dr. Tom Waddell Place) and west elevations, which this dossier only
  infers.** No photograph of either was located; §2.4 reasons from the aerial
  and from period practice. Any real photograph beats that inference.
- Aerial and roof views
- Ground-level views, day and night
- Publicly available drawings, plans or diagrams — in particular any Civic
  Center Historic District nomination or SF Planning HRE that gives a measured
  elevation
- **The crest height, which this dossier only estimates.** The cornice/roof
  plane at ~20.3 m is measured (2010 city LiDAR + the OSM `height` tag agreeing
  independently); the balustrade above it is a +1.1 m inference from photo
  proportion. Record eave and crest separately in `REPORT.md`.

Prefer architect/engineer publications, owner or institutional material,
planning and permitting documents, architectural press, geolocated photography,
and aerial/satellite imagery. Never rely on a single photograph, a single
AI-generated image, or a single unsourced 3D model. Separate verified facts from
visual inference; if sources disagree, document the disagreement and decide.

## Create a reference dossier

Write `artifacts/101-grove/REFERENCE.md` containing: source links and what each
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

This is a **quiet background-to-secondary building with one loud corner**. It is
not a hero landmark and must not compete with City Hall across Grove. §5 (facade
rhythm) and §24 (structure families) govern here, not §11 (landmark geometry).
Spend the budget on: the corner bay, the cornice/balustrade line, the two-tone
base-versus-ashlar split, and the second-floor pediment-and-balconette rhythm.
Everything else is a clean punched grid. Resist modelling individual balusters,
carved acanthus, dentil teeth, or ashlar joints as geometry — they become noise
two hundred metres up.

The finished asset must be immediately recognizable as 101 Grove Street,
consistent with the real building from all four sides and above, architecturally
credible, and a premium handcrafted miniature — not photorealistic, not voxel
art, not generic low-poly, and never accurate in one view while invented in the
others.

## Scope of the exported asset

Export the 101 Grove Street building itself, including its cornice, balustrade,
corner bay ornament, entrance lanterns, roof membrane, corner penthouse, light
court and rooftop plant.

Do not include unrelated surrounding city geometry: Grove Street, Polk Street,
Dr. Tom Waddell Place, Civic Center Plaza, City Hall, the Bill Graham Civic
Auditorium, street furniture, traffic signals, street trees, people, vehicles,
plinths, cameras or lights. Temporary context may appear in review renders but
must not leak into the GLB.

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
(`placeGeneric` in `app/src/assets.js` only scales and positions). The Grove
Street front faces north (outward normal 350.6 deg true) and the corner bay
faces north-east (34.4 deg true), so the contract's "front faces −Y" cannot be
honoured literally. Real-world orientation wins (AGENTS rule 5). Record the
decision and the measured heading in `REPORT.md`.

**Height normalization:** make the exported bounding-box top land exactly on the
verified architectural height, so the loader's `targetHeightM / measuredHeight`
scale is 1.0. Keep the corner penthouse and every rooftop object **below** the
balustrade crest — that is both true to the building (nothing breaks the cornice
silhouette from the street) and what keeps the normalization honest.

## Reproducible Blender workflow

Blender 4.5 LTS or newer, headless only: `blender -b --python script.py -- args`;
no GPU, so use Workbench or CPU Cycles.

Keep `artifacts/101-grove/build_101_grove.py` (deterministic build script),
`artifacts/101-grove/101-grove.blend`, and `artifacts/101-grove/101-grove.glb`.
The script must rebuild the model reliably enough for future revision. Do not
modify or rename an unrelated existing GLB to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`101-grove-top.png`, `101-grove-north.png`, `101-grove-east.png`,
`101-grove-south.png`, `101-grove-west.png`, plus `101-grove-contact-sheet.png`,
at least one high three-quarter aerial beauty render `101-grove-aerial.png`, and
a night render `101-grove-night.png`.

The four elevations must share scale, framing, lighting, exposure and
projection; use orthographic or long-lens cameras; label directions from the
researched orientation; **the aerial is the hero image for this asset** and must
be framed off the north-east so the corner bay, the Grove elevation and the
Polk elevation all read in one frame; the aerial view uses the style bible's
camera assumptions (30-50 degrees down, long lens). Simple tabletop lighting,
neutral warm background, minimal depth of field, and every image must depict the
same exported model.

Drive `_Glow` night renders from Base Color, not from the imported emission —
see the note at the end of `docs/asset-plans/README.md`.

## Validate the exported GLB

Re-import `101-grove.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture
count, camera count, light count, animation count, applied-transform status,
negative-scale status, normal-orientation status, unexpected geometry, and
per-material contract compliance. Normals are checked two ways: per-object signed
volume (authoritative for a union of closed solids) and a deterministic
visibility-ray test (≤ 0.15% residual, zero for single shells). Render at least
one review image from the re-imported asset. Write
`artifacts/101-grove/validation.json` and `artifacts/101-grove/REPORT.md`.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "101-grove",
  "file": "101-grove.glb",
  "anchor": [
    -122.4186747,
    37.7781359
  ],
  "targetHeightM": 21.4,
  "cat": 18,
  "name": "101 Grove Street (Public Health Building)",
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
for that, together with the integration notes in `docs/asset-plans/101-grove.md`.
````

---

## Part 2 — Research and design dossier

Compiled 12 August 2026 from the sources in 2.2. Values marked *inferred* or
*estimated* are visual or derived, not published figures — the executing agent
must re-verify anything it relies on.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Address | 101 Grove Street, San Francisco, CA 94102 (the "#105" in the request is a suite inside the building) | Nominatim / OSM addr tags |
| Occupant | San Francisco Department of Public Health headquarters; also the SF Public Health Laboratory | SF.gov, PCAD |
| Parcel | Block 811, Lot 001 (MBLR `SF0811001`) | SF 2010 LiDAR building-footprint record (measured) |
| Architect | Samuel Heiman | San Anselmo Historical Museum architect biography; PCAD lists the building but leaves the architect field blank |
| Designed / built | designed 1931, completed 1932 | San Anselmo Historical Museum; a 29 July 1935 photograph of the finished building exists (healthysf.org) |
| Style | Beaux-Arts Classical | PCAD |
| Storeys | 4 | PCAD |
| Historic status | Contributor to the San Francisco Civic Center Historic District (NRHP ref. 78000757, listed 10 Oct 1978; district boundary as designated 27 Feb 1987) | PCAD, NRHP |
| Footprint | 63.2 x 37.1 m oriented block, 2,274 m2 polygon area (OBB fill 97%) | OSM way/35176281, reprojected + oriented bbox (measured) |
| Roof / cornice plane | **20.3 m** above grade | SF 2010 LiDAR `SF0811001`: `hgt_median_m` 19.77, `hgt_majoritycm` 20.29 — and OSM `height=20` independently (measured) |
| Crest (balustrade rail) | **21.4 m** | cornice 20.3 m + a balustrade read at ~1.1 m from photo proportion (*estimated*) |
| Ground slope | site falls ~2.4 m across the block (LiDAR `gnd_mincm` 1724 → `gnd_maxcm` 1963) | measured — the app seats the asset on `sampleElevation`, so this is context, not model geometry |
| LiDAR max return | 32.4 m | measured — almost certainly a slender roof mast, not architecture. Deliberately **not** modelled (see 2.9) |
| Anchor | -122.4186747, 37.7781359 | footprint AABB centre (measured) |
| Long-axis heading | 80.6 deg / 260.6 deg true (the Civic Center grid) | OSM geometry (measured) |
| Seismic note | the City has long planned to vacate the building as seismically unsound and relocate DPH; a $150 M relocation was approved in 2020 | SF Examiner — affects occupancy, not form |

### 2.2 Sources

- https://www.openstreetmap.org/way/35176281 — footprint geometry, `building=civic`, `height=20`
- https://nominatim.openstreetmap.org — address resolution: node 11198865806 (the DPH office point) and node 358803227 (the `addr:housenumber=101` point), both inside way/35176281
- https://data.sfgov.org/resource/ynuv-fyni.json — SF 2010 LiDAR building footprints, record `SF0811001` (10,920 half-metre cells ≈ 2,730 m2 including the cornice overhang): ground min 17.24 m, first-return median 38.78 m, height median 19.77 m, height majority 20.29 m, height max 32.42 m
- https://pcad.lib.washington.edu/building/17419 — Pacific Coast Architecture Database: "City and County of San Francisco, Department of Public Health, Headquarters Building", 101 Grove Street, 4 storeys, Beaux-Arts Classical, Civic Center Historic District contributor (district created 27 Feb 1987)
- https://sananselmohistory.org/articles/samuel-heiman/ — attributes the Health Department building at 101 Grove Street to Samuel Heiman, designed 1931
- https://commons.wikimedia.org/wiki/File:Department_of_Public_Health_(San_Francisco).JPG — the primary visual reference: a 2 March 2008 three-quarter photograph by Wikimedia user Sanfranman59 (CC BY-SA 4.0) showing the whole Grove/Polk corner, the full corner bay, the second-floor balconettes, the cornice and the balustrade. §2.4's north, east and corner descriptions come from this image.
- Esri World Imagery (ArcGIS `World_Imagery` export service) — overhead orthoimagery at the parcel; the basis of §2.9's roof description, checked against the OSM polygon by overlay
- https://www.healthysf.org/bdi/more/101grove.html — a 29 July 1935 photograph of the completed building (page located; the image file itself 404s, so it corroborates the completion date only)
- https://www.sf.gov/departments/san-francisco-public-health-laboratory/about — current occupancy
- https://www.sfexaminer.com/news/supervisors-approve-150m-to-relocate-public-health-department-replace-hospital-chillers/ — the 2020 relocation funding and the seismic assessment

### 2.3 Orientation and placement

A corner block in the Civic Center, on the **south** side of Grove Street facing
City Hall, at the **west** corner of Polk Street. The Bill Graham Civic
Auditorium (99 Grove) abuts to the west; Dr. Tom Waddell Place, a service alley,
runs along the south. The Civic Center grid is rotated ~9.4 deg from cardinal:
Grove Street runs 80.6 deg / 260.6 deg true.

Measured footprint, reprojected with the app's tangent projection (LON0
-122.4375, LAT0 37.77) and recentred on the footprint AABB centre (x east,
y north, metres, **CCW**):

```
(-34.17,  13.32)   P0  north-west corner (Grove / west party line)
(-31.87,   0.21)   P1  light-court step
(-28.53,  -0.31)   P2
(-26.81, -11.20)   P3  light-court step
(-30.10, -11.62)   P4
(-28.25, -22.72)   P5  south-west corner
( 34.17, -12.99)   P6  south-east corner (Polk / Waddell)
( 28.99,  18.29)   P7  chamfer, south end
( 22.52,  22.72)   P8  chamfer, north end
```

| Edge | Length | Outward normal (true) | What it is |
|---|---|---|---|
| P8 → P0 | 57.46 m | 350.6 deg (N) | **Grove Street front** — the long public face |
| P7 → P8 | 7.84 m | 34.4 deg (NE) | **the chamfered corner entrance bay** |
| P6 → P7 | 31.71 m | 80.6 deg (E) | **Polk Street** — the second public face |
| P5 → P6 | 63.17 m | 170.6 deg (S) | Dr. Tom Waddell Place, service elevation |
| P0 → P1 … P4 → P5 | 13.31 + 3.38 + 11.02 + 3.31 + 11.25 m | 260.6 deg (W) | west elevation with two light-court steps, against 99 Grove |

Author `+Y` = north and place the polygon exactly as measured. The contract's
"front faces −Y" cannot be met — the real front faces north and the entrance
north-east — so real-world orientation wins per the README orientation note and
AGENTS rule 5.

### 2.4 What each side shows

**North (Grove Street) — the long public face, 57.5 m.** Four storeys of light
warm-grey granite ashlar. A tall rusticated base with deep horizontal joints
carries three smooth-ashlar storeys above a slim string course. Second-floor
windows are the enriched ones: each sits under a small triangular pediment on
consoles and over a projecting balconette whose dark, near-black ground carries
a **row of gold rosettes** — the only saturated colour on the building. Third-
and fourth-floor windows are plain rectangles in the ashlar field, the fourth
noticeably shorter. The wall terminates in a plain frieze, a bold projecting
cornice on modillions, and a continuous open balustrade above it. Regular bay
rhythm, no projections, no entrances.

**North-east chamfer — the corner bay, 7.8 m.** The whole identity of the
building. Bottom to top: a monumental **round-arched entrance** whose voussoirs
radiate out into the rustication; a carved tympanum with a **round oculus**
flanked by foliate relief; a bronze-and-glass double door under a flat
entablature reading DEPARTMENT OF PUBLIC HEALTH / 101 GROVE STREET; two ornate
**bronze lantern sconces on scroll brackets** flanking the arch; a carved
cartouche keystone above; then the projecting **balconette with gold rosettes**;
then a tall window in a full pedimented aedicule with consoles; then a plain
window; then the cornice and balustrade carrying straight across.

**East (Polk Street), 31.7 m.** The same order and the same enrichment as Grove,
just shorter — the corner bay is shared between the two, so the building reads as
one continuous L of public facade wrapping the corner.

**South (Dr. Tom Waddell Place), 63.2 m.** *Inferred — no photograph located.*
The service elevation on a 12 m alley. Period practice for a 1932 civic block,
and the plain wall visible in the orthoimagery, both say: the same four-storey
punched window grid on the same floor lines, but without pediments, balconettes
or rustication, and with a plain capped parapet in place of the balustrade.

**West, 13.3 + 11.0 + 11.3 m in three steps.** *Inferred.* A party/light-court
wall against the Bill Graham Civic Auditorium: the two steps in the OSM polygon
are a light court. Plainest of all — a few punched windows facing into the court,
plain parapet.

**Top.** See 2.9.

### 2.5 Recognition cues (ranked)

1. **The chamfered corner bay with its arched entrance and oculus**, holding the
   Grove/Polk corner. Nothing else in the block does this.
2. **The unbroken cornice-plus-balustrade line** wrapping Grove and Polk at a
   dead-level 20.3 / 21.4 m — the Civic Center's mandated cornice height, which
   is exactly what makes the district read as a district.
3. **The two-tone vertical order**: a tall rusticated base under three smooth
   ashlar storeys.
4. **The second-floor pediment-and-gold-balconette rhythm** — a dashed dark-and-
   gold line across the middle of an otherwise pale building.
5. **A brilliant white flat roof** on a granite Beaux-Arts block: the modern
   cool-roof membrane is the strongest thing about the building from directly
   overhead, and it is genuinely what is there.

### 2.6 Miniature translation

**Preserve**

- The true footprint polygon including the corner chamfer and the two west steps
- The 4-storey proportion with a tall base: floor lines at 5.4 / 10.3 / 14.6 /
  18.6 m, cornice 20.3 m, crest 21.4 m
- The corner bay's full stack — arch, oculus, balconette, pediment — at
  deliberately exaggerated scale
- The cornice/balustrade as one continuous horizontal on Grove, the chamfer and
  Polk
- The gold rosettes: the building's only saturated accent, and worth their tris
- The bright white roof membrane

**Simplify / exaggerate**

- Ashlar joints, dentils, modillions, acanthus and egg-and-dart: **removed**.
  The cornice becomes two clean beveled bands; the rustication becomes three
  broad horizontal grooves in the base, not courses.
- Balusters become a row of plain 0.16 m blocks at 1.15 m pitch between a solid
  bottom rail and a solid top rail — the balustrade must read as *pierced*, and
  that is all it needs to do (§26)
- Windows become a `Toy_ink` reveal plate with a `Toy_glass` slab proud of it,
  one per bay per floor — no mullions except a single cross on the second floor
- Each balconette becomes one `Toy_navy` panel with **three** oversized
  `Toy_gold` rosette blocks (the real one has nine; three is what reads)
- Pediments become a single low triangular prism per bay
- The entrance arch becomes a recessed `Toy_ink` plate inside a `Toy_trim`
  archivolt ring, with a `Toy_gold` oculus disc and a `Toy_gold` door
- Lanterns become two small `Toy_gold` blocks on brackets, ~1.7x true size (§9)
- The south and west elevations get the same window grid, no ornament, plain
  parapet — plainer, not blank

**Do not add** a tower, a dome, a signature curve, rooftop signage, or any
silhouette drama. This building's job in the scene is to be the well-mannered
granite block that makes City Hall look monumental.

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not
a straitjacket — adjust after the first aerial review render.

1. **Body:** extrude the measured footprint from z=0 to z=19.35, `Toy_stone`.
2. **Rusticated base:** a `Toy_sand` ring band from z=0 to z=5.40, proud 0.10 m,
   with three `Toy_ink`-free recessed grooves (bands inset 0.06 m) at z=1.8,
   3.0 and 4.2 to read as rustication; a `Toy_trim` water table 0 → 0.55 proud
   0.16 m.
3. **String course:** `Toy_trim` ring band z=5.40 → 5.75, proud 0.18 m.
4. **Frieze:** `Toy_trim` ring band z=18.60 → 19.35, flush.
5. **Cornice:** `Toy_trim` ring band z=19.35 → 20.30, proud 0.95 m, beveled —
   the building's strongest horizontal.
6. **Balustrade:** `Toy_trim` bottom rail z=20.30 → 20.55 (proud 0.55 m), plain
   blocks 0.16 x 0.16 m from 20.55 → 21.05 at 1.15 m pitch along Grove, the
   chamfer and Polk, top rail 21.05 → **21.40** (the crest). South and west get
   a solid `Toy_trim` parapet band 20.30 → 21.05 with a cap to 21.20 instead.
7. **Window grid:** bays at ~4.8 m pitch — 12 on Grove, 6 on Polk, 1 on the
   chamfer, 13 on the south, 7 across the three west segments. Per bay per
   floor: `Toy_ink` reveal 2.2 x band-height proud 0.04 m, `Toy_glass` slab
   inset 0.12 m and proud 0.11 m. Bands: 1.70–4.30, 6.60–9.60, 11.10–13.90,
   15.40–17.90.
8. **Second-floor enrichment (Grove, chamfer, Polk only):** a `Toy_navy`
   balconette panel 6.10 → 6.60 proud 0.30 m with three `Toy_gold` rosette
   blocks; a `Toy_trim` pediment prism above the window head at 9.60 → 10.15.
9. **Corner bay:** widen the chamfer's window openings by 25%; a `Toy_trim`
   archivolt ring from z=0 to 5.10 around a `Toy_ink` arch recess; a `Toy_gold`
   oculus disc at z=3.9; a `Toy_gold` door 0 → 2.9; two `Toy_gold` lantern
   blocks on `Toy_ink` brackets at z=2.6, flanking; a full `Toy_trim` aedicule
   (two pilaster strips + pediment) around the second-floor window.
10. **Roof:** `Toy_white` membrane slab, top at z=19.60, inset 0.30 m from the
    parapet inner face.
11. **Light court:** a `Toy_roofd` recessed pad 19.20 → 19.35 over the
    south-central roof (~22 x 11 m), with one long `Toy_steel` plant block on it.
12. **Corner penthouse:** a `Toy_trim` block following the chamfer plan over the
    corner bay, z=19.60 → 20.90 (**below** the crest), with a `Toy_roofd`
    monitor curb and a `Toy_glassl` skylight pane on top.
13. **Rooftop plant (west field):** four `Toy_roofd` boxes on a low curb, two
    duct runs, two `Toy_steel` roof hatches — tight clusters, not scatter.

### 2.8 Materials and palette

Deliberately the War Memorial Opera House's family — same district, same decade,
same stone (§24 structure families).

| Material | Hex | Where |
|---|---|---|
| `Toy_stone` | `d9d2c2` | the ashlar body, all four elevations |
| `Toy_sand` | `ece4d4` | the rusticated ground-floor base |
| `Toy_trim` | `f3efe6` | water table, string course, frieze, cornice, balustrade, pediments, archivolt, aedicule, corner penthouse |
| `Toy_glass` | `2a4d73` | all window glazing |
| `Toy_glassl` | `6f95b8` | the corner-penthouse skylight pane |
| `Toy_ink` | `3a3530` | window reveals, arch recess, lantern brackets |
| `Toy_navy` | `2c4a70` | the balconette panels |
| `Toy_gold` | `caa64a` | rosettes, the oculus, the entrance door, the lanterns |
| `Toy_white` | `f7f4ec` | the cool-roof membrane |
| `Toy_steel` | `9aa0a6` | roof hatches, light-court plant |
| `Toy_roofd` | `45454a` | rooftop mechanical, light-court pad, monitor curb |
| `Toy_gold_Glow` | `caa64a` | the two lanterns, the oculus, the door transom — the night hero |
| `Toy_glassl_Glow` | `6f95b8` | a scatter of lit windows on Grove and Polk |

**Night design.** One hero and one supporting group, per the style bible's
restraint rule. Hero: the corner entrance — the two lanterns, the oculus and the
door read as a single warm gold pool at the chamfer, which is exactly how the
building is lit in life. Supporting: an irregular scatter of lit windows across
the Grove and Polk elevations (a 24-hour public-health building), never a full
grid. Nothing on the roof glows. Glow shells are thin, inset and lifted clear of
the opaque glazing behind them — the app draws `_Glow` in a separate layer at
~12% alpha by day, so coincident faces read as a smear.

### 2.9 Top surface

From orthoimagery, overlaid against the OSM polygon to confirm what belongs to
this building and what belongs to 99 Grove:

- The dominant fact is a **brilliant white cool-roof membrane** covering nearly
  the whole footprint — a hard, bright plane inside a grey cornice frame.
- A **low penthouse over the north-east corner bay**, its plan following the
  chamfer, carrying a dark rectangular monitor/skylight. Set back and low enough
  that nothing breaks the balustrade line from the street.
- An **interior light court** in the south-central roof: a recessed, darker pad
  with a long light-coloured plant block along it.
- The west third carries scattered small plant: a few low units, two duct runs,
  roof hatches, and a slender mast (the LiDAR 32.4 m max return). The mast is
  **deliberately not modelled** — it would be sub-pixel at the app's camera and
  it would break the height normalization by becoming the bbox top.
- No signage, no terrace, no greenery.

### 2.10 Scope

In: the building, its cornice, balustrade, corner ornament, entrance lanterns,
roof membrane, corner penthouse, light court and rooftop plant.

Out: Grove Street, Polk Street, Dr. Tom Waddell Place, Civic Center Plaza, City
Hall, the Bill Graham Civic Auditorium, street trees, traffic signals, banners,
vehicles, people, plinths, cameras, lights.

### 2.11 Triangle budget

Cap **22,000**. Indicative split:

| Group | Est. tris |
|---|---|
| Body prism + base + string course + frieze + cornice (beveled ring bands) | ~2,600 |
| Balustrade (rails + ~84 blocks on Grove/chamfer/Polk) + solid S/W parapet | ~1,900 |
| Window grid, ~155 openings x (reveal + glass) | ~3,900 |
| Second-floor enrichment: 19 balconettes + 57 rosettes + 19 pediments | ~1,400 |
| Corner bay: archivolt, arch recess, oculus, door, lanterns, aedicule | ~900 |
| Roof: membrane, light court, penthouse, plant, hatches | ~1,300 |
| Glow shells (entrance group + lit-window scatter) | ~600 |
| Bevel overhead on the chunky solids | the balance |

If it overshoots: drop the west elevation's window count first, then the south's,
then the rosettes from three to two. Never the cornice or the corner bay.

### 2.12 Draft manifest entry

```json
{
  "id": "101-grove",
  "file": "101-grove.glb",
  "anchor": [-122.4186747, 37.7781359],
  "targetHeightM": 21.4,
  "cat": 18,
  "name": "101 Grove Street (Public Health Building)",
  "estimated": true,
  "dims": [68.34, 45.44, 21.4],
  "tris": N,
  "loadRadius": 2500
}
```

`estimated: true` because the crest is an inference on top of a measured cornice
(2.1). `loadRadius` follows the default rule `max(2500, 21.4 x 30)` = 2500 —
this is a low building whose absence beyond the radius is illegible, and the
Civic Center is a dense cluster, so there is no case for `alwaysLoaded`.

### 2.13 Integration notes (for later, not this task)

**Case B — new landmark.** No `101-grove` id exists in
`pipeline/lib/landmarks.mjs` or `app/src/landmarks.js`, so integration needs a
registry entry *and* a re-bake of the affected tiles, or the baked procedural
building will intersect the GLB.

Draft registry entry:

```js
{
  // Civic Center corner block, 63 x 37 m. The exclusion test drops a footprint
  // when its centroid OR any vertex falls inside the circle, and this
  // footprint's centroid sits on the anchor, so a modest radius already clears
  // it. The constraint is the other direction: the Bill Graham Civic
  // Auditorium's east wall is the nearest neighbour geometry to the west and
  // the Waddell Place side is only ~23 m away, so keep the radius well under
  // the distance to the nearest neighbour vertex and verify against the audit.
  id: '101Grove',
  name: '101 Grove Street (Public Health Building)',
  lon: -122.4186747,
  lat: 37.7781359,
  height: 21.4,
  exclude: 22,
  camera: { distance: 300, yaw: 35, pitch: 22 },
}
```

The camera preset looks down the corner bay's normal (34.4 deg true) from
300 m — close enough that the corner ornament reads, far enough that City Hall
frames the shot behind it.

Then run `docs/asset-plans/INTEGRATION-PROMPT.md` in full: manifest entry with
the explicit `loadRadius`, registry entry, tile re-bake, audit 1.6 (confirm the
procedural footprint count drops by exactly the number of Overture footprints on
block 811 lot 001, and that no neighbour is taken with it), local verification
(single building, scale 1.0, orientation, terrain seating, night glow, draw calls
< 300), and the mandatory fallback drill.

### 2.14 Validation checklist

- Fresh-scene re-import of the exported GLB, not the source scene
- `dims.z` exactly 21.40 so `targetHeightM / measuredHeight` = 1.0
- `min_z` within 0.5 m of 0; XY centre within 1 m of origin
- ≤ 22,000 triangles
- No image textures, no transparency, no cameras/lights/animation/armatures
- Every material `Toy_*`, no `Toy_body`
- `_Glow` only on the entrance group and the lit-window scatter
- Per-object signed volume positive for every object; ray residual ≤ 0.15%
- No degenerate triangles (the usual cause is a bevel on a plate thinner than
  twice the bevel width — leave the rosettes, balusters and thin plates
  unbeveled)
- Aerial render reviewed **before** the formal rig, and again after

### 2.15 Open questions and risks

1. **The crest is estimated.** Cornice/roof at 20.3 m is measured twice
   (LiDAR 19.77–20.29, OSM `height=20`); the +1.1 m balustrade is read off a
   photograph. If a measured elevation turns up, use it and re-normalize.
2. **South and west elevations are inferred.** No photograph of either was
   located. The plan reasons from orthoimagery and period practice. This is the
   single largest correctness risk in the asset and must be flagged in
   `REPORT.md`.
3. **Bay counts are a design choice, not a measurement.** The 2008 photograph is
   foreshortened and does not show the whole Grove elevation; 12 bays at 4.79 m
   is a proportional fit, not a count off a drawing.
4. **The LiDAR 32.4 m max return** is unexplained; it is read as a mast and
   excluded. If it turns out to be a real penthouse the massing changes.
5. **Exclusion radius.** 22 m is a first estimate. The Bill Graham Civic
   Auditorium abuts to the west and the audit must confirm it is not taken with
   the re-bake.
6. **Architect attribution** rests on one local-history source; PCAD leaves the
   architect field blank. Recorded as such, not as certain.
