# Louise M. Davies Symphony Hall — SF-SIM asset plan

The San Francisco Symphony's 1980 concert hall by Skidmore, Owings & Merrill with
Pietro Belluschi, on the Civic Center block bounded by Van Ness Avenue, Grove,
Franklin and Hayes. It is the one Modernist volume in a Beaux-Arts civic
composition, and SOM handled that by matching its neighbours' cornice line and
then doing something no neighbour does: sweeping a **103.6° convex arc of
two-storey glass promenade** across the Van Ness/Grove corner, aimed diagonally
at City Hall, under a shallow curved metal roof.

The design brief is "the glass crescent facing City Hall", not "1980s concrete
box". Seen from the app's aerial camera the building must read as an arc and a
dome next to the Opera House's rectangle and fly tower.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/davies-symphony-hall/`. This document is the plan only: Part 1 is the
runnable task prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `davies-symphony-hall` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.4206030, 37.7776227` |
| Target height | **35.0 m** to the roof crest; parapet/cornice ring 26.1 m; promenade glazing 2.5–17.5 m |
| Footprint | 122.6 m E–W x 91.2 m N–S envelope; 7,396 m2 measured; front arc R = 44.75 m |
| Long axis heading | 99.0° / 279.0° (the Civic Center grid, ~9° off the world axes) |
| Triangle cap | 16,000 |
| Category | `17` (theater_cinema — the same as the Opera House next door) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready Davies Symphony Hall GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of Louise M. Davies Symphony Hall, 201 Van Ness
Avenue, San Francisco, and deliver it as a downloadable, validated GLB.

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
7. `artifacts/war-memorial-opera-house/` — the immediate neighbour across Grove Street,
   the same civic block group, the same category, and the model this asset will be
   seen beside in every aerial frame. Match its value range and restraint.
8. `artifacts/cal-academy/` — the closest reference implementation for a *curved,
   horizontal, glass-fronted* institution rather than a masonry monument
9. `docs/asset-plans/davies-symphony-hall.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Must capture

- **The 103.6° convex glass arc** across the Van Ness/Grove corner — a true circular
  arc, centre `(10.03, -1.02)` and radius **44.75 m** in the local frame of 2.3,
  measured from OSM geometry with sub-metre residuals. This is the building. A
  modeller who chamfers the corner instead of sweeping it has failed.
- **Two glazed promenade levels** behind a close rhythm of slender vertical precast
  fins, running the whole arc and continuing along Grove Street and Van Ness Avenue
- **The solid attic band above them**, carrying a row of narrow dark clerestory slots
  just under the cornice, and the gold `LOUISE M DAVIES SYMPHONY HALL` lettering on
  the fascia
- **The shallow curved standing-seam roof** — a broad, low, radially ribbed metal
  shell over the hall, cresting at 35.0 m. It is not a hemisphere and not a flat
  roof; it is a shallow shell with about 9 m of rise over a 90 m span.
- **Pale grey precast concrete** everywhere else — the rear and west elevations are
  plain panelled boxes with almost no openings
- **The cantilevered curved terrace slabs** at both ends of the arc, with their
  rounded noses and pipe-rail edges
- **The stone plinth wall** along the sidewalk, with steps up to the promenade level

## Research Davies Symphony Hall independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- All four elevations — the north (Grove), east (Van Ness), south (Hayes) and west
  (Franklin) faces, and the arc that turns the north-east corner between the first two
- Aerial and roof views: the shell's curvature, the rib direction, the flagpole, and
  the rooftop plant over the rear block — the roof is the surface the app's camera
  spends the most time looking at and the dossier's roof reading is the weakest part of it
- Day and night appearance. The night state is the building's best moment and is
  required, not optional.
- The bay rhythm of the fins along the arc, which is *inferred* here

Prefer SOM's own project material, the San Francisco War Memorial and Performing Arts
Center's building documentation, architectural press from 1980 and the 1992
renovation, geolocated photography, and aerial/satellite imagery. Never rely on a
single photograph, a single AI-generated image, or a single unsourced 3D model.
Separate verified facts from visual inference; if sources disagree, document the
disagreement and decide.

**One source problem is already known and resolved in 2.1 and 2.15 — re-check it, do
not silently re-inherit the wrong value:**

**The OSM `height=49 m` tag on way `32865746` is wrong and must not be used as the
target height.** DataSF's LiDAR-derived footprint layer (`ynuv-fyni`, building
`201006.0000141`, whose bounding box matches the OSM way to five decimal places over
28,160 half-metre cells) gives a median roof height of 26.12 m and a maximum of
34.95 m above a mean ground of 18.91 m NAVD88. Those two numbers correspond exactly
to the two things you can see in any photograph: the cornice ring, and the crest of
the shell roof. 49 m would put Davies above the Opera House's fly tower, which every
aerial photograph of Civic Center contradicts. Build to **35.0 m**.

## Create a reference dossier

Write `artifacts/davies-symphony-hall/REFERENCE.md` containing: source links and what
each establishes; verified dimensions and location; orientation; observations from all
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

This is a **hero landmark** in the style bible's detail budget (§21) — a named
building the concierge will fly to — but a *restrained* one. Its neighbours are City
Hall and the Opera House; the whole point of SOM's design is that it defers to them in
material and cornice line and asserts itself only in geometry. Spend the budget on the
arc, the fin rhythm and the shell, not on ornament.

The finished asset must be immediately recognizable as this building, consistent with
the real building from all four sides and above, architecturally credible, and a
premium handcrafted miniature — not photorealistic, not voxel art, not generic
low-poly, and never accurate in one view while invented in the others.

## Scope of the exported asset

Export the single building: plinth, main hall volume with its arc, the promenade
glazing and fins, the attic band and clerestory, the cornice, the shell roof, the rear
and west back-of-house blocks with their rooftop plant, and the two cantilevered
terrace slabs.

Do not include unrelated surrounding city geometry: the War Memorial Opera House, the
Veterans Building, City Hall, Van Ness Avenue and its overhead trolley wires, Grove
and Hayes Streets, the Henry Moore sculpture in the forecourt, street trees, traffic
lights, sidewalks, parked cars, people, plinths, cameras or lights. Temporary context
may appear in review renders but must not leak into the GLB.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary
`.glb`; real-world meters; origin at base center; minimum geometry Z ~ 0;
applied transforms; no negative scales; outward normals; no duplicate or foreign
geometry; no image textures; no transparency; flat-color materials named `Toy_*`
from the project palette; `_Glow` suffix only on surfaces that glow at night; no
`Toy_body`; no cameras, lights, animations, armatures or constraints; no external
dependencies; at most 16,000 triangles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model
drops into the city at its real-world heading — the loader applies no rotation
(`placeGeneric` in `app/src/assets.js` only scales and positions). The block sits on
the Civic Center grid, about 9° off the world axes; the arc opens toward the
north-east. Build directly on the measured footprint polygon in 2.3 rather than
modelling an axis-aligned box and rotating it. Record the measured heading in
`REPORT.md`.

**Height normalization:** the tallest geometry in the export (the crest of the shell
roof) must land at exactly **35.0 m** so the loader's `targetHeightM / measuredHeight`
scale is 1.0. The flagpole is *not* modelled; if you choose to model it, it must not
become the bounding-box top.

## Reproducible Blender workflow

Blender 5.2 LTS. Headless: `blender -b --python script.py -- args`.

Keep `artifacts/davies-symphony-hall/build_davies_symphony_hall.py` (deterministic
build script), `artifacts/davies-symphony-hall/davies-symphony-hall.blend`, and
`artifacts/davies-symphony-hall/davies-symphony-hall.glb`. The script must rebuild the
model reliably enough for future revision. Do not modify or rename an unrelated
existing GLB to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`davies-symphony-hall-top.png`, `-north.png`, `-east.png`, `-south.png`, `-west.png`,
plus `davies-symphony-hall-contact-sheet.png`, at least one high three-quarter aerial
beauty render `davies-symphony-hall-aerial.png`, and a night render
`davies-symphony-hall-aerial-night.png`.

The four elevations must share scale, framing, lighting, exposure and projection; use
orthographic or long-lens cameras; label directions from the researched orientation;
the top view must clearly show the shell's curvature, the rib direction, the cornice
ring and the rear roof plant; the aerial view uses the style bible's camera assumptions
(30–50 degrees down, long lens) and must be taken from the **north-east**, because that
is the only angle from which the arc reads as an arc.

## Validate the exported GLB

Re-import `davies-symphony-hall.glb` into a fresh isolated Blender scene and validate
the re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture
count, camera count, light count, animation count, applied-transform status,
negative-scale status, normal-orientation status, unexpected geometry, and
per-material contract compliance. Render at least one review image from the
re-imported asset. Write `artifacts/davies-symphony-hall/validation.json` and
`artifacts/davies-symphony-hall/REPORT.md`.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "davies-symphony-hall",
  "file": "davies-symphony-hall.glb",
  "anchor": [
    -122.4206030,
    37.7776227
  ],
  "targetHeightM": 35.0,
  "cat": 17,
  "name": "Davies Symphony Hall",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a separate, explicitly requested job — run `docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in `docs/asset-plans/davies-symphony-hall.md`.
````

---

## Part 2 — Research and design dossier

Compiled 12 August 2026 from the sources in 2.2. Values marked *inferred* are visual or
derived estimates, not published figures — the executing agent must re-verify
anything it relies on.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Official name | Louise M. Davies Symphony Hall | OSM `name`, Wikidata Q6688842 |
| Opened | 1980, cost US$28 M | Wikipedia; Wikidata P571/P1619 = 1980 |
| Architects | Skidmore, Owings & Merrill with Pietro Belluschi; acoustics Bolt, Beranek and Newman | Wikipedia, SOM project page |
| Renovation | $10 M acoustic remodel, SOM (Wikipedia credits Kirkegaard Associates for the acoustics), commissioned 1990, completed 1992 | SOM project page; Wikipedia |
| Capacity | 2,743 | OSM `capacity`, Wikidata P1083, Wikipedia |
| Gross area | 252,000 sq ft (23,400 m2) | SOM project page |
| Part of | San Francisco War Memorial and Performing Arts Center | Wikipedia |
| Footprint envelope | 122.61 m E–W x 91.16 m N–S; OBB 121.58 x 84.27 m; area 7,396 m2 | OSM way/32865746, 39 nodes, reprojected — **measured** |
| Front arc | circular, centre `(10.03, -1.02)`, R = **44.75 m**, sweep −4.5° → 99.1° (103.6°), residuals ≤ 0.85 m | least-squares fit to the 11 OSM arc nodes — **measured** |
| Grid heading | long axis 99.0° / 279.0° | measured from the footprint OBB |
| Cornice / parapet ring | **26.1 m** above grade | DataSF `ynuv-fyni` `201006.0000141`, `hgt_median_m` = 26.12 over 28,160 cells — **measured (LiDAR 2010)** |
| Roof crest | **34.95 m** above grade | same record, `hgt_maxcm` = 3495; `peak_1st_m` 53.91 − `gnd_meancm` 18.91 = 35.0 — **measured (LiDAR 2010)** |
| Ground | 18.91 m NAVD88 mean, 18.28 m min; OSM `ele` = 20 | same record |
| OSM `height` tag | **49 m — rejected, see 2.15** | OSM way/32865746 |
| Storeys of promenade glazing | 2 | photography; SOM ("glass-enclosed promenades along Grove Street and Van Ness Avenue") |
| Cladding | pale grey precast concrete panels with flush joints; one-inch structural glass curtain wall | Wikipedia (glass); photography (precast) |
| Contextual intent | "matching cornices, roof forms, colors, and textures" of its Beaux-Arts neighbours; curved facade aimed diagonally at City Hall | SOM project page |

### 2.2 Sources

- https://www.openstreetmap.org/way/32865746 — 39-node footprint, address, `wikidata`,
  `capacity`, and the rejected `height=49 m`
- `https://data.sfgov.org/resource/ynuv-fyni` (DataSF Building Footprints, LiDAR-derived),
  building `201006.0000141` — ground, median and maximum roof height over 28,160
  half-metre cells; the authoritative height source for this plan
- https://en.wikipedia.org/wiki/Louise_M._Davies_Symphony_Hall — architects, 1980, cost,
  capacity, the structural-glass curtain wall, the 1992 acoustic renovation
- https://www.wikidata.org/wiki/Q6688842 — 1980, capacity, architect claim (P84); note
  that it carries **no** height claim (P2048)
- https://www.som.com/projects/davies-symphony-hall-san-francisco-war-memorial-and-performing-arts-center/
  — gross area, the glass-enclosed promenades on Grove and Van Ness, the diagonal
  orientation toward City Hall, and the explicit intent to match neighbouring cornices
  and roof forms
- https://commons.wikimedia.org/wiki/Category:Louise_M._Davies_Symphony_Hall — the
  exterior set used for this dossier: `Daviessymphonyhall.jpg` (north-east corner, day,
  the whole arc and the shell roof), `Louise M. Davies Symphony Hall at night.jpg` (the
  same view lit, and the source of the night-state design),
  `San Francisco Davies Symphony Hall 2.jpg` (close-up of the rear/west precast
  elevation, the terrace nose and the arched window)
- https://commons.wikimedia.org/wiki/File:Aerial_view_of_the_Beaux_Arts_Civic_Center_of_SF.jpg
  — Davies' shell roof read against the Opera House roof and City Hall's dome; the
  cross-check that killed the 49 m figure
- `docs/asset-plans/war-memorial-opera-house.md` — the neighbour's plan, for cornice
  height and palette continuity

### 2.3 Orientation and placement

The building fills its Civic Center block: Grove Street north, Van Ness Avenue east,
Hayes Street south, Franklin Street west. The Civic Center grid runs about 9° off the
world axes, so the straight edges are not axis-aligned. The great arc turns the
north-east corner and faces City Hall diagonally across Van Ness. Back-of-house fills
the south-west quadrant.

Measured footprint polygon, in Blender coordinates (metres, `+X` east, `+Y` north),
already centred on the anchor `-122.4206030, 37.7776227`:

```
(-48.51,  38.89)  (-47.70,  32.98)  (-33.99,  34.98)  (-26.79,  -6.84)
(-61.31, -12.43)  (-56.07, -45.58)  (-22.44, -40.25)  ( 58.50, -27.44)
( 56.77, -16.19)  ( 58.56, -15.41)  ( 60.07, -14.17)  ( 61.08, -12.19)
( 61.31,  -9.45)  ( 60.35,  -7.29)  ( 59.04,  -5.69)  ( 56.93,  -4.78)
( 55.17,  -4.57)  ( 52.56,   9.97)  ( 49.62,  19.71)  ( 44.68,  27.31)
( 37.13,  34.80)  ( 32.07,  38.19)  ( 26.57,  40.81)  ( 20.07,  42.53)
( 13.98,  43.48)  (  8.42,  43.57)  (  2.99,  43.14)  ( -7.43,  41.55)
( -8.91,  42.65)  (-11.20,  43.05)  (-14.07,  42.21)  (-15.43,  40.97)
(-16.53,  39.15)  (-17.16,  36.88)  (-18.73,  45.58)  (-39.91,  42.30)
(-39.69,  40.22)  (-44.03,  39.57)
```

Read as four pieces:

| Piece | Extent | Faces |
|---|---|---|
| Front arc | R 44.75 m about `(10.03, -1.02)`, sweeping −4.5° → 99.1° | north-east, at City Hall |
| Van Ness flank | short straight run at x ≈ +57 to +61, y −27 to −5, with a small radiused bay at y ≈ −10 | east |
| Grove flank | straight run y ≈ +40 to +45, x −44 to −17, with a small rounded stair bay at x ≈ −12 | north |
| Back-of-house | the south-west quadrant, x −61 to −22, y −45 to −7 | west (Franklin) and south (Hayes) |

The small bays at `(59, −10)` and `(−12, 42)` are rounded stair/entry pavilions. Keep
them — they are cheap and they break the two straight flanks — but do not make them
events.

### 2.4 What each side shows

**North-east (the arc, Van Ness × Grove)** — The face the whole design is about, and
the only one that matters at thumbnail size. From the ground up: a low stone plinth
wall with planting and steps; two levels of continuous glass promenade behind a close
rhythm of slender white precast fins, the upper level taller than the lower and
separated from it by a slim spandrel; a solid precast attic band; a row of narrow dark
clerestory slots near the top of that band; a thin cornice; then the shell roof
oversailing everything with a visible fascia carrying gold lettering. At each end of
the arc a curved terrace slab cantilevers out with a rounded nose and a pipe rail.

**East (Van Ness) and north (Grove)** — The promenade glazing and fin rhythm continue
off the arc onto both streets, so the arc does not read as a bolt-on. Openings thin out
toward the south and west ends.

**South (Hayes) and west (Franklin)** — Back-of-house. Large plain precast panel walls
with flush reveals and very few openings: a stepped parapet, one arched window high on
the wall, a cantilevered curved canopy over a service entrance, a louvre panel, and a
loading dock. This is where the building is honest about being a machine for
performances, and it should look calm and blank, not detailed.

**Top** — A broad, shallow, radially ribbed standing-seam metal shell over the hall,
about 9 m of rise across a 90 m span, cresting at 35.0 m with a flagpole at the crest.
The shell sits inside the cornice ring rather than overhanging it on the back sides.
Over the south-west back-of-house block the roof is flat, darker, and carries tidy
clusters of mechanical plant. The rib direction — running with the curve, not across
it — is the detail that makes the shell read as metal from above.

### 2.5 Recognition cues (ranked)

1. **The 103.6° glass arc** turning the corner toward City Hall — silhouette-level
   recognition, visible from any altitude
2. **The shallow ribbed shell roof** cresting over it
3. **The two-level fin-and-glass promenade**, warm and transparent against pale precast
4. **Pale grey precast** matched to the Civic Center's cornice line, not a tower
5. The cantilevered curved terrace noses at the ends of the arc

### 2.6 Miniature translation

**Preserve**

- The arc's true radius, centre and sweep, exactly. Everything else can move a metre.
- The 26.1 m cornice ring and the 35.0 m crest as *two distinct heights* — the whole
  massing is a cylinder-segment with a cap on it
- The two promenade levels as two continuous glass bands, and the fins as a rhythm
- The plain, near-blank back — the contrast with the front is the composition
- The rounded terrace noses; they are what stops the arc ending in a raw edge

**Simplify / exaggerate**

- Individual mullions vanish; each promenade level becomes one recessed glass band with
  ~60 fins across the arc rather than the real 100-plus
- The clerestory becomes one dark slot band with regular teeth, not individual windows
- The standing-seam roof becomes ~40 shallow ribs modelled as real geometry, wide enough
  to survive at 30 px; individual seams are dropped
- The gold lettering becomes a single thin `Toy_gold` fascia band, not letterforms
- Back-of-house parapet steps reduce to two levels; the loading dock becomes one recess
- The plinth wall is thickened to ~1.6 m so it hides the terrain seam
- The flagpole is dropped from the export (it would take the bounding-box top and cost
  the scale normalization for two pixels of mast)

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not
a straitjacket — adjust after the first aerial review render.

1. Plinth: extrude the 2.3 footprint, inflated 1.2 m, from z=0 to z=1.6, `Toy_stone`.
2. Main hall volume: extrude the 2.3 footprint from z=0 to z=26.1, `Toy_cream`.
3. Promenade recess: cut a band 1.0 m deep into the arc and the Grove/Van Ness flanks
   from z=2.5 to z=17.5, filled with `Toy_glass`, split by a 1.0 m `Toy_cream` spandrel
   at z=9.5–10.5 so it reads as two levels.
4. Fins: ~60 vertical `Toy_white` fins, 0.55 m wide x 0.5 m deep, on the arc at a
   constant angular pitch, continuing at the same spacing onto both flanks, from z=2.5
   to z=17.5.
5. Attic band: solid `Toy_cream` from z=17.5 to z=26.1, with a 1.6 m band of `Toy_ink`
   clerestory slots (0.5 m wide, 1.6 m tall, 1.6 m pitch) centred at z=23.5.
6. Cornice: 0.9 m `Toy_trim` ring at z=25.2–26.1, projecting 0.6 m.
7. Fascia: 0.7 m `Toy_gold` band on the shell's leading edge above the arc only.
8. Shell roof: a shallow spherical-cap surface springing from the cornice ring at
   z=26.1 to a crest of **exactly 35.0 m**, `Toy_steel`, with ~40 radial ribs 0.35 m
   proud modelled as real geometry.
9. Back-of-house: the south-west quadrant capped flat at z=22.0 with a stepped parapet
   to z=23.5, `Toy_roofd` roof, plus three tidy plant clusters and a stair penthouse.
10. Terrace slabs: two 0.45 m slabs with rounded noses cantilevering 5.5 m at z=17.5
    from the two ends of the arc, `Toy_trim`, with a 1.0 m `Toy_steel` pipe rail.
11. Service canopy and loading recess on the Hayes elevation; one arched window high on
    the Franklin wall.
12. Bevel 0.12 m, 2 segments.

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_cream` | `#f2ede3` | precast walls, attic band, spandrel |
| `Toy_white` | `#f7f4ec` | the promenade fins |
| `Toy_stone` | `#d9d2c2` | plinth wall and steps |
| `Toy_trim` | `#f3efe6` | cornice ring, terrace slabs |
| `Toy_steel` | `#9aa0a6` | the shell roof and its ribs, pipe rails |
| `Toy_glass` | `#2a4d73` | promenade glazing, arched window |
| `Toy_ink` | `#3a3530` | clerestory slots, loading recess |
| `Toy_roofd` | `#45454a` | back-of-house flat roof and plant |
| `Toy_gold` | `#caa64a` | the fascia lettering band |
| `Toy_mustard_Glow` | `#d9a441` | **hero:** both promenade levels at night |
| `Toy_gold_Glow` | `#caa64a` | clerestory slot band and the fascia band at night |

Night state (required). The night photograph is the design: the two glass levels burn
warm right around the arc, the clerestory slots glow above them, and the gold lettering
is picked out. Nothing else lights — the precast stays dark, the shell roof stays dark,
the back-of-house is black. Hero glow = the two promenade bands (a warm `Toy_mustard_Glow`
shell proud of the opaque `Toy_glass`, never the glass itself, because the app renders
`_Glow` at ~12% alpha by day). Supporting accents = the clerestory band and the fascia.
The day colours of both glow materials are palette members, so the daytime read stays
consistent with its neighbours.

### 2.9 Top surface

The single most-seen surface. Three things carry it: the shell's curvature (it must
visibly dome — a flat disc with a bevel will not do), the rib direction running with
the curve, and the clean contrast between the pale shell and the dark, tidy
back-of-house roof behind it. The cornice ring should stay visible as a lighter edge
all the way round from directly overhead. No skylights on the shell; the hall below has
none.

### 2.10 Scope

**In the GLB:** plinth, hall volume, arc, promenade glazing and fins, spandrel, attic
band and clerestory, cornice, gold fascia, shell roof and ribs, back-of-house block with
parapet and plant, terrace slabs and rails, Hayes service canopy and loading recess,
Franklin arched window

**Not in the GLB:** the Opera House, the Veterans Building, City Hall, Van Ness Avenue
and its trolley wires, Grove and Hayes Streets, the Henry Moore sculpture, street trees,
traffic signals, sidewalks, vehicles, people, plinths, cameras or lights

### 2.11 Triangle budget

Cap 16,000. Suggested split: hall volume and arc ~2k, 60 fins ~4k, promenade glazing and
spandrel ~1k, attic band and clerestory teeth ~2k, cornice ring ~1k, shell roof with 40
ribs ~4k, back-of-house and plant ~1k, terraces, canopy and rails ~1k.

### 2.12 Draft manifest entry

```json
{
  "id": "davies-symphony-hall",
  "file": "davies-symphony-hall.glb",
  "anchor": [
    -122.4206030,
    37.7776227
  ],
  "targetHeightM": 35.0,
  "cat": 17,
  "name": "Davies Symphony Hall",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

`dims` and `tris` are placeholders until the asset is built and validated.
`"estimated": false` — both the cornice and the crest are LiDAR measurements, not
guesses.

### 2.13 Integration notes (for later, not this task)

- **New landmark.** Add a `pipeline/lib/landmarks.mjs` entry (`id: 'davies-symphony-hall'`)
  and re-bake the affected tiles, or the baked procedural building will intersect the GLB.
- **Exclusion radius:** the building fills its own block and has no attached neighbours,
  so a plain radius works here — unlike 1008 General Kennedy. Half the 122.6 m envelope
  is 61 m; take ~62 m, which stays inside Grove, Van Ness, Hayes and Franklin and
  therefore cannot punch a hole in the Opera House block across Grove.
- `loadRadius`: the default formula gives `max(2500, 35 × 30) = 2500` m. Take the default.
- **Check the Opera House's exclusion zone at the same time.** The two blocks are 25 m
  apart across Grove Street; whichever radius `opera-house` currently uses should be
  confirmed not to reach into the Davies footprint now that something real stands there.
- Category `17` matches `opera-house`, so the concierge and the search card treat the two
  Performing Arts Center halls consistently.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Bounding-box top exactly 35.0 m (loader scale lands at 1.0)
- [ ] XY bbox ≈ 122.6 x 91.2 m, consistent with 2.1
- [ ] The arc measures R 44.75 m about the local point `(10.03, −1.02)`
- [ ] Cornice ring at 26.1 m, distinct from the crest
- [ ] Triangles at or under 16,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the promenade bands, clerestory and fascia; glow shells proud of
      the opaque glazing
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (per-object signed volume
      for the union of solids; ray test residual ≤ 0.15%)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + contact sheet + night render regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

- **The OSM `height=49 m` is the dossier's one hard conflict, and it is resolved
  against OSM.** The DataSF LiDAR record for the same polygon gives 26.12 m median and
  34.95 m maximum over 28,160 half-metre cells, its bounding box matches the OSM way to
  five decimals, and the two figures land exactly on the two visible datums (cornice,
  crest). SOM's own statement that the design matches its neighbours' cornices puts the
  26.1 m ring within a metre of the Opera House's, which is what the photographs show.
  49 m would make Davies taller than the Opera House fly tower; no aerial photograph
  supports that. If a published architectural height ever turns up, prefer it — but it
  will have to beat a 28,000-sample LiDAR measurement.
- **The LiDAR is from 2010** and post-dates every change to this building, so age is not
  a risk here the way it is for 550 Third Street.
- **The shell's rise is derived, not published**: 35.0 − 26.1 = 8.9 m of rise, treated as
  a spherical cap over the hall. The real roof may be a segmental vault rather than a
  cap; from the app's camera the difference is a few pixels, but an aerial photograph
  would settle it and should be sought.
- **The fin count on the arc is *inferred*.** Sixty is a stylistic choice tuned to
  survive at thumbnail size, not a count from the drawings.
- **No published height, no published dimensions.** Wikidata carries no P2048 and SOM
  publishes only gross area. Everything dimensional in this plan is measured from
  geometry, which is why 2.1 marks it measured rather than sourced.
- **The Henry Moore *Large Four Piece Reclining Figure*** sits in the forecourt at the
  Van Ness/Grove corner. It is not in scope, but it is the kind of thing a future props
  pass should place, and it is worth a note in `REPORT.md`.
