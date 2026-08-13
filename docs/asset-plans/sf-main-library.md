# San Francisco Main Public Library — SF-SIM asset plan

James Ingo Freed's 1996 New Main: a Sierra White granite block that wears two
faces at once — Beaux-Arts on the Civic Center sides, late-modernist on the
Market Street sides — over a roof that is the real design event, carrying a
circular atrium oculus, a glazed pyramid and two big skylight sheds.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/sf-main-library/`. This document is the plan only: Part 1 is the runnable
task prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `sf-main-library` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.14) |
| WGS84 anchor | `-122.4157709, 37.7791281` (oriented-bounding-box centre, measured) |
| Target height | **28.98 m** crest (skylight sheds / pyramid apex); main roof plane **24.02 m** |
| OSM footprint | 106.42 x 56.88 m oriented box, 6,027 m2 polygon (OSM way/24446086, measured) |
| Long-axis bearing | 80.94 deg — the Civic Center grid, 9.06 deg north of due east |
| Triangle cap | 26,000 |
| Category | `15` (Library) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready San Francisco Main Public Library GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of the San Francisco Main Public Library
(100 Larkin Street, the 1996 "New Main") and deliver it as a downloadable,
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
8. `docs/asset-plans/asian-art-museum.md` — the Old Main across Fulton Street, the
   nearest sibling in scale, site and grid rotation
9. `docs/asset-plans/sf-main-library.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Must capture

- **The two-faced building.** This is the whole idea of the design and the one
  thing a viewer must be able to read: Larkin (west) and Fulton (north) are
  ordered, classical, cornice-and-pilaster Civic Center facades; Grove (south) and
  Hyde (east) are flat granite grids with scattered punched windows and dark
  spandrel bands. Same stone, two grammars, meeting at the corners.
- The Larkin ceremonial front: a raised centre pavilion, a giant order of flat
  pilasters with tall lattice-glazed windows between them, the incised
  SAN FRANCISCO PUBLIC LIBRARY frieze over three sets of double doors, an attic of
  small square windows, and the cresting of small studs along the parapet
- The tall square granite corner pier at Grove & Hyde — the modern face's anchor
- **The roof, which is the asset's largest surface and its best material:** the
  circular atrium oculus, the low glazed pyramid west of it, the two big pitched
  skylight sheds over the eastern half, and the mechanical enclosure near the
  Grove/Hyde corner
- Night: the skylights glowing from the lit atrium below, plus the entrance

## Research the Main Library independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- North (Fulton), east (Hyde), south (Grove) and west (Larkin) elevations
- Aerial and roof/top views — **the roof is this building's most designed surface**
  and the reason to spend budget here rather than on facade ornament
- Ground-level views
- Day and night appearance
- Publicly available drawings, plans or diagrams
- **The height.** The OSM `height=46` tag on way/24446086 is NOT a height: it is
  the NAVD88 roof *elevation* (153.78 ft = 46.87 m), the same trap as the Asian Art
  Museum across the street. Do not use it. Establish the crest and the main roof
  plane separately and say which is which.
- Which of the roof objects actually makes the 28.98 m crest — the pyramid apex,
  a shed ridge, or the mechanical enclosure

Prefer architect/engineer publications, owner or institutional material,
planning and permitting documents, architectural press, geolocated photography,
and aerial/satellite imagery. Never rely on a single photograph, a single
AI-generated image, or a single unsourced 3D model. Separate verified facts from
visual inference; if sources disagree, document the disagreement and decide.

## Create a reference dossier

Write `artifacts/sf-main-library/REFERENCE.md` containing: source links and what each
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

The finished asset must be immediately recognizable as the Main Library,
consistent with the real building from all four sides and above, architecturally
credible, and a premium handcrafted miniature — not photorealistic, not voxel art,
not generic low-poly, and never accurate in one view while invented in the others.

This building is 106 m long and only 29 m tall, and it stands 90 m from the Asian
Art Museum, which is the same size and the same shade of pale stone. Two things
follow. First, most of the budget belongs on the roof — that is where this
building differs from its neighbour and where the camera looks. Second, the
classical/modern split has to survive simplification, because without it the two
buildings become the same pale slab from the air.

## Scope of the exported asset

Export the library block only: the granite mass, its base, the Larkin and Fulton
classical fronts, the Grove and Hyde modern fronts, the Grove/Hyde corner pier, the
parapets and cresting, the roof deck, the oculus, the pyramid, the skylight sheds,
the mechanical enclosure and the Larkin entrance steps.

Do not include unrelated surrounding city geometry: Fulton Mall, the Pioneer
Monument, the Asian Art Museum, Civic Center Plaza, City Hall, UC Law, the Orpheum,
Larkin / Fulton / Hyde / Grove Streets, street trees, people, vehicles, plinths,
cameras or lights. Temporary context may appear in review renders but must not leak
into the GLB.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary
`.glb`; real-world meters; origin at base center; minimum geometry Z ~ 0;
applied transforms; no negative scales; outward normals; no duplicate or foreign
geometry; no image textures; no transparency; flat-color materials named `Toy_*`
from the project palette; `_Glow` suffix only on surfaces that glow at night; no
`Toy_body`; no cameras, lights, animations, armatures or constraints; no external
dependencies; at most 26,000 triangles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model
drops into the city at its real-world heading — the loader applies no rotation
(`placeGeneric` in `app/src/assets.js` only scales and positions). The building's
long axis runs at bearing **80.94 deg**; the main entrance faces **west** onto
Larkin Street. The contract's "front faces −Y" cannot be honoured literally here;
real-world orientation wins (AGENTS rule 5). Record the decision and the measured
heading in `REPORT.md`.

**Height normalisation:** normalise the bbox top to the verified crest exactly, so
the loader's `targetHeightM / measuredHeight` scale lands at 1.0.

## Reproducible Blender workflow

Blender 4.5 LTS is at `/opt/blender` (`blender` on PATH). Headless only:
`blender -b --python script.py -- args`; no GPU, so use Workbench or CPU Cycles.

Keep `artifacts/sf-main-library/build_sf_main_library.py` (deterministic build script),
`artifacts/sf-main-library/sf-main-library.blend`, and
`artifacts/sf-main-library/sf-main-library.glb`. The script must rebuild the model
reliably enough for future revision. Do not modify or rename an unrelated existing
GLB to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`sf-main-library-top.png`, `sf-main-library-north.png`, `sf-main-library-east.png`,
`sf-main-library-south.png`, `sf-main-library-west.png`, plus
`sf-main-library-contact-sheet.png`, at least one high three-quarter aerial beauty
render `sf-main-library-aerial.png`, and a night render `sf-main-library-night.png`.

The four elevations must share scale, framing, lighting, exposure and
projection; use orthographic or long-lens cameras; label directions from the
researched orientation; **the top view must clearly show the oculus, the pyramid,
both skylight sheds and the mechanical enclosure**; the aerial view uses the style
bible's camera assumptions (30-50 degrees down, long lens). Simple tabletop
lighting, neutral warm background, minimal depth of field, and every image must
depict the same exported model. The night render must show the `_Glow` set driven
from Base Color (see the note at the end of `docs/asset-plans/README.md`).

## Validate the exported GLB

Re-import `sf-main-library.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture
count, camera count, light count, animation count, applied-transform status,
negative-scale status, normal-orientation status, unexpected geometry, and
per-material contract compliance. Render at least one review image from the
re-imported asset. Write `artifacts/sf-main-library/validation.json` and
`artifacts/sf-main-library/REPORT.md`.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "sf-main-library",
  "file": "sf-main-library.glb",
  "anchor": [
    -122.4157709,
    37.7791281
  ],
  "targetHeightM": 28.98,
  "cat": 15,
  "name": "San Francisco Main Public Library",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a separate, explicitly requested job — run `docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in `docs/asset-plans/sf-main-library.md`.
````

---

## Part 2 — Research and design dossier

Compiled 13 August 2026 from the sources in 2.2. Values marked *inferred* are visual or
derived estimates, not published figures — the executing agent must re-verify
anything it relies on.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Built | Groundbreaking 1992, construction from 15 March 1993, completed 1995, opened **18 April 1996** | SFPL "Other facts about the building" |
| Architects | James Ingo Freed, Pei Cobb Freed & Partners (New York) with Cathy Simon, Simon Martin-Vegue Winkelstein Moris (San Francisco) | SFPL, PCF&P, Wikipedia |
| Cost | $104.5 M construction, from a $109.5 M 1988 bond; $30 M private furnishings | SFPL |
| Size | **376,000 sq ft**, **six floors above ground + one below** | SFPL (PCF&P says 377,000 gross) |
| Site | Marshall Square, the full block bounded by **Larkin (W), Fulton (N), Hyde (E), Grove (S)**; 2.65 acres | SFPL, PCF&P |
| Footprint (polygon) | 6,027 m2 | OSM way/24446086, reprojected + shoelace (measured) |
| Footprint (oriented box) | 106.42 x 56.88 m | min-area OBB over the OSM polygon (measured) |
| Long-axis bearing | 80.94 deg (9.06 deg north of due east) | derived from the OBB (measured) |
| OBB centre | −122.4157709, 37.7791281 | derived (measured) |
| Polygon centroid | −122.4157712, 37.7791276 | derived (measured) — 0.07 m from the OBB centre |
| Crest above grade | **28.98 m** | DataSF Building Footprints `hgt_maxcm` = 2898 (2010 LiDAR, measured) |
| Main roof plane above grade | **24.02 m** | DataSF `hgt_mediancm` = 2402 (measured) |
| Roof elevation NAVD88 | 42.31 m median / 46.91 m peak | DataSF `median_1st_m`, `peak_1st_m` |
| Site grade NAVD88 | 18.34 m median (13.73–19.50 m range) | DataSF `gnd_*` |
| Levels | 5 signed in OSM; 6 above ground per SFPL | OSM `building:levels`, SFPL |
| Facade stone | Sierra White granite, **from the same quarry as the other Civic Center buildings** | SFPL |
| Civic Center facades | Larkin + Fulton: "two symmetrical facades ... echoes in a modernist way the materials and massing of the neighboring Beaux-Arts institutions" | PCF&P |
| Market Street facades | Grove + Hyde: "a more contemporary feel, compatible with the commercial activity on Market Street" | SFPL |
| Atrium | five-story, **60 ft (18.3 m) diameter**, monumental open staircase, top-lit | PCF&P, SFPL |
| Contributor to | SF Civic Center Historic District / National Historic Landmark district (as a non-contributing modern infill) | Civic Center district listing — *inferred* status, not load-bearing for this asset |

### 2.2 Sources

- https://www.openstreetmap.org/way/24446086 — footprint geometry, address, `height=46`, `ele=18`, `building:levels=5`, `check_date=2025-04-10`
- https://data.sfgov.org/resource/ynuv-fyni.json (`area_id=186`, `mblr=SF0354001`, 24,696 LiDAR cells ≈ 6,174 m2) — `hgt_maxcm` 2898, `hgt_mediancm` 2402, `median_1st_m` 42.31, `peak_1st_m` 46.91, ground median 18.34 m
- https://sfpl.org/locations/main-library/about/architecture-main-library — Sierra White granite from the Civic Center quarry; Grove and Hyde "more contemporary ... compatible with the commercial activity on Market Street"; skylight over the five-story atrium; 142 base isolators
- https://sfpl.org/locations/main-library/about/other-facts-about-building — 376,000 sq ft, six floors above ground and one below, dates, cost, Marshall Square bounded by Larkin/Fulton/Hyde/Grove
- https://www.pcf-p.com/projects/san-francisco-main-public-library/ — full-block 2.65-acre site, "two symmetrical facades" onto the Civic Center, 60-ft atrium, roof garden, 377,000 sq ft
- https://en.wikipedia.org/wiki/Main_Library_(San_Francisco) — opening date, cost, floor count, Freed/Simon authorship, the atrium controversy
- https://commons.wikimedia.org/wiki/File:San_Francisco_Public_Library_-_Main_Branch,_exterior,_from_Larkin_Street.jpg (CC BY 2.0) — the Larkin front: giant order, lattice glazing, incised frieze, attic, parapet cresting
- https://commons.wikimedia.org/wiki/File:SFPL_Main_Library_Full_Exterior.jpg (CC BY-SA) — the whole west end from Civic Center Plaza; the raised centre pavilion against the lower flanks; the skylight sheds visible above the parapet
- https://commons.wikimedia.org/wiki/File:San_Francisco_Public_Library_-_Main_Branch,_exterior,_from_Grove_Street.jpg (CC BY 2.0) — the Grove (south) modern facade: flat granite grid, scattered punched windows, dark spandrel band, banded base
- https://commons.wikimedia.org/wiki/File:SFPL_Main_Branch_Exterior_from_Grove_%26_Hyde_St.jpg (CC BY-SA) — the Grove/Hyde corner pier and the stepped modern massing
- https://commons.wikimedia.org/wiki/File:San_Francisco_Public_Library_-_Main_Branch,_exterior,_from_Market_Street.jpg (CC BY 2.0) — the same corner from the south-east, showing how the corner pier reads on the skyline
- Esri World Imagery nadir aerial over the block — the roof layout: oculus, pyramid, two skylight sheds, mechanical enclosure, roof terrace

### 2.3 The height correction (read this before modelling)

OSM way/24446086 carries `height=46`. That figure is **not a height** — it is the
building's NAVD88 roof *elevation*, 153.78 ft = 46.87 m, which appears verbatim as
`p2010_zmaxn88ft` in the DataSF LiDAR record for the same footprint. The tag also
carries `ele=18`, the site grade, which is the giveaway: 46.87 − 18.34 = 28.5 m.
This is the identical trap the Asian Art Museum plan documents in its §2.3, on the
identical `height=46` value, one block north.

The measured values are:

- **Crest 28.98 m** — the tallest roof structures. From the aerial and from the
  Civic Center Plaza photograph these are the glazed skylight sheds and the pyramid,
  which stand clear above the parapet and are visible from the street. This is
  `targetHeightM`.
- **Main roof plane 24.02 m** — the LiDAR median, i.e. the general roof/parapet
  level around the block. The Civic Center cornice datum.

Whether the crest is a shed ridge, the pyramid apex or the mechanical enclosure is
*inferred* from the nadir aerial and one oblique; the executing agent should settle
it and say which, because it decides where the model's 28.98 m point sits.

### 2.4 Orientation and placement

The block is bounded by Larkin (west), Fulton (north, the pedestrianised Fulton Mall
with the Pioneer Monument), Hyde (east) and Grove (south). Its long axis runs
east–west at bearing 80.94 deg — the Civic Center grid, 9.06 deg counter-clockwise
from due east. In Blender that is a +9.06 deg rotation about Z from an axis-aligned
box, with `+Y` = true north.

The main entrance faces **west** onto Larkin, across Civic Center Plaza from City
Hall. Anchor on the OBB centre; here the polygon centroid and the OBB centre agree
to within 0.07 m, so the choice is not load-bearing — unlike the Asian Art Museum,
this footprint has no service notch pulling them apart.

The block is a near-twin of the Asian Art Museum's one street north (106.60 x 54.71 m
at bearing 81.68 deg). That is not coincidence — they are two halves of the same
Civic Center grid — and it is exactly why the two assets must not end up looking
alike. See 2.7.

### 2.5 What each side shows

**West (Larkin Street) — the hero elevation, 57 m wide.** Pale Sierra White granite
in a large ashlar grid, visible as a fine joint pattern over the whole surface. The
centre is a **raised pavilion** that rises above the flanking parapets, carrying a
giant order of **flat, slightly rounded pilasters** on a plinth, with tall windows
between them filled by a distinctive **diagonal diamond-lattice glazing**. Below the
order runs an incised frieze — SAN FRANCISCO PUBLIC LIBRARY — over **three sets of
double doors** reached by a shallow flight of steps, flanked by two dark lamp
standards. Above the order: a plain entablature band, then an **attic of small
square punched windows**, then a flat parapet finished with a **cresting of small
studs** — a row of little vertical pins along the top edge, one of the building's
most particular details. The flanking bays left and right of the pavilion are lower
and plainer with the same lattice windows.

**North (Fulton Street), 106 m.** The second "symmetrical" Civic Center face, on the
axis with the Old Main across Fulton Mall. Same granite, same cornice datum, same
parapet cresting, but a longer and quieter rhythm: a repeated bay of tall windows in
a pilaster grid, without the raised centre pavilion of Larkin.

**South (Grove Street), 106 m — the modern face.** The same stone, a completely
different grammar: a **flat granite panel grid with no order and no cornice**,
scattered **punched rectangular windows** placed asymmetrically (some square, some
vertical slots), one continuous **dark grey spandrel band** running the length at
roughly the third-floor line, and a **banded/rusticated granite base** about 2 m
tall at the pavement. Toward the east end the mass steps forward and up into a
glazed bay with a canopy.

**East (Hyde Street), 57 m — the modern face's front.** Dominated by the **tall
square granite corner pier at Grove & Hyde**, which rises above the neighbouring
parapets and is banded with the same dark grey strips and sparse punched windows.
North of it the Hyde elevation steps down to a lower three-storey granite block with
dark bands, then rises again toward the Fulton corner.

**Top — the reason this asset exists.** Reading the nadir aerial, inside a pale
parapet band and a darker inset roof deck:

- a **circular glazed oculus** just west of the roof's centre, a shallow segmented
  glass cone over the five-storey atrium, with the spiral of the grand stair legible
  through it — the single most identifiable thing on the building
- immediately west of the oculus, a **low glazed pyramid** on a square base set
  diamond-wise to the block, roughly 30 m across
- over the **eastern half, two large pitched glazed skylight sheds**, set at an angle
  to each other so they read as a shallow chevron
- a **mechanical enclosure with three circular units** near the Grove/Hyde corner
- scattered white rooftop units along the north band, a linear light slot near the
  west edge, and a small roof terrace with planting at the south-west

### 2.6 Recognition cues (ranked)

1. **The circular oculus** in a big flat roof, with the pyramid beside it — from the
   app's camera this is the building, and nothing else in the city looks like it
2. **The two-grammar facade**: ordered pilastered granite on Larkin and Fulton,
   flat punched granite with dark bands on Grove and Hyde
3. The raised Larkin centre pavilion with the incised frieze over three doors
4. The tall square corner pier at Grove & Hyde
5. The parapet cresting of small studs along the classical sides
6. Two big pitched glazed sheds on the eastern roof

### 2.7 Miniature translation

**Preserve**

- The 106 x 57 m proportion and the 9.06 deg grid rotation — a slab on the Civic
  Center grid, not a free-standing block
- **The classical/modern split.** This is the non-negotiable one. The Asian Art
  Museum sits 90 m north at the same size and the same pale value; if both assets
  reduce to "long pale block with a cornice", the city loses the joke Freed was
  making. The library must read as *ordered on two sides, loose on two sides*, even
  at thumbnail size.
- The roof as a designed composition, not a lid
- The raised Larkin centre and the Grove/Hyde corner pier as the two points where
  the silhouette breaks the parapet line

**Simplify / exaggerate**

- The giant order becomes ~6 chunky pilasters on Larkin and a pilaster strip rhythm
  on Fulton; no free-standing columns anywhere
- The diamond-lattice glazing becomes a flat `Toy_glass` panel with one incised
  cross — the pattern is a texture in reality and must not become geometry
- The incised inscription becomes a slightly proud `Toy_trim` frieze band, not
  letterforms
- The parapet cresting becomes a shallow notched `Toy_trim` strip, read as a dotted
  line from above, not 200 individual pins
- The scattered modern windows become ~14 punched `Toy_glass` rectangles per long
  side in a deliberately irregular but designed arrangement, plus one continuous
  dark `Toy_roofd` spandrel band
- The oculus becomes one clean glazed drum with a low segmented cone and a visible
  spiral ramp inside — semantically enlarged, because it is the recognition cue
- Rooftop clutter becomes: parapet band, inset deck, oculus drum, pyramid, two
  sheds, one mechanical box with three pucks, one planted terrace corner

### 2.8 Massing recipe

Build order for the deterministic script; author axis-aligned then rotate the whole
assembly +9.06 deg about Z. Dimensions are the starting point, not a straitjacket —
adjust after the first aerial review render. X is the 106.42 m long axis (east
positive), Y the 56.88 m short axis (north positive).

1. Base: 106.4 x 56.9 m block, z=0 to z=2.4, `Toy_stone`, three horizontal banding
   grooves — the banded plinth that runs all four sides.
2. Body: same plan, z=2.4 to z=22.6, `Toy_cream`, carrying the per-face rhythms of
   6 and 7.
3. Cornice/parapet: `Toy_trim` band z=22.6 to z=24.6, projecting 0.6 m on the north
   and west (classical) faces and flush on the south and east (modern) faces — the
   projection *is* the split.
4. Cresting: a notched `Toy_trim` strip z=24.6 to z=25.1, on the north and west
   parapets only, notch pitch ~1.6 m.
5. Larkin centre pavilion: the middle 30 m of the west face pushed 0.8 m proud and
   raised to parapet z=26.4, cresting to z=26.9.
6. West order: 6 pilasters 2.2 m wide, 0.9 m proud, z=6.0 to z=20.0, `Toy_trim`,
   with `Toy_glass` panels between; frieze band `Toy_trim` z=5.2 to z=6.0 across the
   pavilion; three `Toy_gold_Glow` doorways at z=0 to z=4.2 behind a 3-tread
   `Toy_stone` step block 20 m wide.
7. North (Fulton) order: 14 pilaster strips 1.4 m wide, 0.5 m proud, z=6.0 to
   z=20.0, `Toy_trim`, `Toy_glass` between; same base and cornice.
8. South (Grove) and east (Hyde) faces: flat `Toy_cream`, one continuous
   `Toy_roofd` spandrel band z=11.4 to z=12.6, and ~14 (south) / ~7 (east) punched
   `Toy_glass` rectangles in an irregular arrangement, 2.0 x 3.2 m and 2.0 x 2.0 m.
9. Grove/Hyde corner pier: 17 x 17 m, from z=0 to parapet z=27.0, `Toy_cream`, two
   `Toy_roofd` bands, four punched windows, plain flat top — no cresting.
10. Roof deck at z=23.0, `Toy_roofd`, inset 6 m from the parapet face all round.
11. Oculus: drum radius 10.5 m centred 8 m west and 2 m north of the block centre,
    z=23.0 to z=25.4 `Toy_trim`, capped by a 12-segment `Toy_glass` cone to z=27.2,
    with a `Toy_trim` spiral ramp read inside the drum.
12. Pyramid: 30 x 30 m square base rotated 45 deg, centred 26 m west of the block
    centre, z=23.0 to apex z=28.98 — **the crest** — `Toy_glass` faces on a
    `Toy_trim` frame ridge.
13. Skylight sheds: two 30 x 20 m pitched `Toy_glass` planes on `Toy_trim` curbs
    over the eastern third, ridges at z=27.8, set at ±12 deg to each other.
14. Mechanical enclosure: 14 x 11 m `Toy_stone` box z=23.0 to z=26.2 near the
    Grove/Hyde corner, three `Toy_roofd` pucks on top.
15. Roof terrace: 16 x 10 m `Toy_sand` deck at z=23.4 in the south-west corner, low
    `Toy_trim` rail, two `Toy_mint` planter strips.
16. Bevel 0.12 m, 2 segments.

### 2.9 Materials and palette

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_cream` | `#f2ede3` | main granite walls, corner pier |
| `Toy_stone` | `#d9d2c2` | banded base, entrance steps, mechanical enclosure |
| `Toy_trim` | `#f3efe6` | pilasters, cornice, cresting, frieze, oculus drum, curbs, rails |
| `Toy_glass` | `#2a4d73` | all windows, the oculus cone, the pyramid, the skylight sheds |
| `Toy_roofd` | `#45454a` | roof deck, the modern faces' spandrel bands, mechanical pucks |
| `Toy_sand` | `#ece4d4` | roof terrace deck |
| `Toy_mint` | `#8fd0a8` | roof terrace planters |
| `Toy_white_Glow` | `#f7f4ec` | the oculus cone and the two skylight sheds at night |
| `Toy_gold_Glow` | `#caa64a` | the three Larkin entrance doorways at night |

Night glow: hero = the roof glazing lit from the atrium below — this is both the
truthful reading (the atrium is the lit volume) and the one that pays off under a
camera that looks down. Supporting = the entrance doorways. Two glow surfaces,
nothing else; the pyramid stays dark so the oculus and sheds carry the composition.
Their day colors must match non-glow palette neighbours so the daylight asset stays
calm.

Note the glow set and the day set both want to be `Toy_glass` blue on the same
surfaces. Split them: the cone and shed *panes* are `Toy_white_Glow` (day colour
`#f7f4ec`, a pale glazing that reads as skylight rather than window), while the
facade windows stay `Toy_glass`. That is also what the real building does — its
skylights are white-frosted and its windows are dark.

### 2.10 Top surface

106 x 57 m of roof under a camera that looks down: the largest single surface on the
asset and the one that distinguishes it from every other pale Civic Center slab. It
must not be a flat gray rectangle. The design is the real one, compressed: pale
parapet band, dark inset deck, then the four glazed events — oculus, pyramid, two
sheds — laid across it west to east, with the mechanical box and the planted terrace
as the two non-glass incidents. The value contrast that carries it is pale stone
against dark deck against bright glass.

### 2.11 Scope

**In the GLB:** the granite block (base, body, cornice, cresting), the Larkin centre
pavilion and steps, the Fulton pilaster rhythm, the Grove and Hyde punched facades
and spandrel bands, the Grove/Hyde corner pier, the roof deck, oculus, pyramid, two
skylight sheds, mechanical enclosure and roof terrace

**Not in the GLB:** Fulton Mall, the Pioneer Monument, the Asian Art Museum, Civic
Center Plaza, City Hall, UC Law, the Orpheum, the two 1.2 m site structures that
DataSF records inside the block, Larkin / Fulton / Hyde / Grove Streets, street
trees, people, vehicles, plinths, cameras or lights

### 2.12 Triangle budget

Cap 26,000. Suggested split: body, base and cornice/cresting ~7k; the west pavilion
and its order ~4k; the Fulton pilaster rhythm ~3k; the modern faces' punched windows
and bands ~3k; the corner pier ~1k; roof deck, oculus, pyramid, sheds, mechanical
and terrace ~7k; steps ~1k.

### 2.13 Draft manifest entry

```json
{
  "id": "sf-main-library",
  "file": "sf-main-library.glb",
  "anchor": [
    -122.4157709,
    37.7791281
  ],
  "targetHeightM": 28.98,
  "cat": 15,
  "name": "San Francisco Main Public Library",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

`dims` and `tris` are placeholders until the asset is built and validated.
`loadRadius` is the default rule `max(2500, 28.98 x 30)` = 2500.

### 2.14 Integration notes (for later, not this task)

**New landmark (Case B).** Add a `pipeline/lib/landmarks.mjs` entry
(`id: 'sfMainLibrary'`, lon/lat as above, `height: 28.98`, `exclude: 40`) **and
re-bake the affected tiles**, or the baked procedural building will intersect the
GLB. Note the registry's camel conversion turns manifest id `sf-main-library` into
`sfMainLibrary` — confirm against `app/src/landmarks.js` before wiring.

**The exclusion radius is measured, not guessed** — Civic Center is the tightest
site in the registry and this is its tightest block. `excluded()` in
`pipeline/buildings.mjs` drops a footprint when its centroid **or any ring vertex**
falls inside the circle, so the radius has to clear the library's *nearest* vertex
while staying inside the *nearest neighbour's* nearest vertex. Measured from this
anchor against the actual bake input:

| Distance | What it is |
|---|---|
| 28.9 m | the library's own nearest footprint vertex — Overture (30.7 m in DataSF) |
| 30.3 / 31.7 m | two 1.2 m site structures inside the block (DataSF only, 27 and 30 LiDAR cells) — fine to drop |
| **50.6 m** | the nearest real neighbour: the ~9 m and 15.9 m buildings on the far side of Hyde/Market, agreed by Overture and DataSF |
| 54.0–54.4 m | the next neighbours across Grove |
| 60.3 m | the OBB half-diagonal — **too large, would eat the Hyde/Market frontage** |

**40 m** therefore drops the library in both sources with a 9.3 m margin (against the
tighter DataSF figure) and clears every real neighbour by 10.6 m. It is the same
value the Asian Art Museum carries one block north, for the same reason. Do not use
the half-diagonal here.

Also worth knowing: Overture carries `height=46` for this footprint — the NAVD88
elevation again — so the baked city currently renders the library ~46 m tall,
overtopping the Asian Art Museum and reading as a mid-rise in the Civic Center
skyline. Excluding it fixes that too, exactly as it did for the museum.

Civic Center is dense with already-integrated and in-flight landmarks
(`city-hall`, `opera-house`, `asianArtMuseum`, `billGrahamCivicAuditorium`,
`civicCenterCourthouse`, `101Grove`, `505VanNess`, `daviesSymphonyHall`,
`herbstTheatre`). Check this circle against theirs — exclusion circles union, and
the Asian Art Museum's 40 m circle sits 92 m away, so they do not overlap.

### 2.15 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Bbox Z normalised to 28.98 m exactly, so the loader's scale lands at 1.0
- [ ] Dimensions plausible in meters and consistent with 2.1
- [ ] Triangles at or under 26,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the roof glazing (oculus cone, two sheds) and the entrance doorways
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (per-object signed
      volume authoritative; ray test residual <= 0.15%)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Seven review renders + night render + contact sheet regenerated from the final export
- [ ] The top view legibly shows oculus, pyramid, both sheds and the mechanical box
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.16 Open questions and risks

- **The height tag is a trap, twice over.** OSM and Overture both carry `height=46`
  for this footprint, and it is the NAVD88 roof elevation, not a height. Anyone
  re-deriving the height from either will build it 1.6x too tall — the same error
  the Asian Art Museum plan had to head off on the identical number.
- **Which object makes the 28.98 m crest is *inferred*.** The aerial and the Civic
  Center Plaza photograph both show glazed structures standing clear above the
  parapet, and 2.8 puts the pyramid apex at the crest, but the sheds and the
  mechanical enclosure are plausible alternatives. Settle it before normalising.
- **The twin problem.** This building and the Asian Art Museum are the same size,
  the same stone and 90 m apart. The classical/modern split and the glazed roof are
  the only things that separate them at diorama scale. If a review render puts them
  side by side and they read the same, the asset has failed even if every dimension
  is right.
- The window arrangement on Grove and Hyde is deliberately irregular in reality and
  was read from photography, not drawings. It is *inferred* and chosen for rhythm.
- The pyramid's exact plan size and the sheds' pitch angles are scaled off the nadir
  aerial, not published drawings — *estimated*, ±15%.
- The site grade range in DataSF is wide (13.73–19.50 m NAVD88), but that minimum is
  a below-grade artefact; the median 18.34 m is the working figure. The app seats
  assets on sampled terrain at a single anchor, so the model's base is level. Accept
  it; do not model a stepped base.
