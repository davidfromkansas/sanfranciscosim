# Hiram W. Johnson State Office Building — SF-SIM asset plan

SOM's 1998 addition to the Civic Center: a 127 m, 14-storey slab of near-white
granite filling the northern half of the Earl Warren block, whose identity is the
pale sea-green glass grid punched into near-white stone, the **two sculpted end
drums** — a pair of convex granite piers flanking a deeply recessed curved glass
bay at each short end — and, on Golden Gate Avenue, a convex glass bay bulging out
over a wide curved canopy with STATE OF CALIFORNIA cut into the glass. From the
app's aerial camera it is a long pale roof with a set-back mechanical penthouse
running along its centre.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/hiram-johnson-state-office-building/`. This document is the plan only:
Part 1 is the runnable task prompt, Part 2 is the research and design dossier
behind it.

| | |
|---|---|
| Manifest id | `hiram-johnson-state-office-building` |
| Existing procedural builder | none — new landmark (Case B: needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.14) |
| WGS84 anchor | `-122.4179151, 37.7810345` (oriented-bounding-box centre, measured) |
| Target height | **61.9 m** architectural crest (SOM 203 ft); main roof plane **53.6 m** |
| Long/short faces | south and north fronts measure **flat**; the curves are at the two ends and the entrance (see 2.5) |
| OSM footprint | 127.38 x 47.81 m oriented box, 5,614 m2 polygon (OSM way/35176304, measured) |
| Long-axis bearing | 81.27 deg — the Civic Center grid, 8.73 deg north of due east |
| Triangle cap | 26,000 |
| Category | `18` (government / state offices) |

> **Address warning, in the other direction.** DGS files this building and the
> **Earl Warren Building** (350 McAllister Street, 1922, 27 m, already shipped as
> `earl-warren-building`) as one "Ronald M. George State Office Complex" under a
> single management record. They are two separate assets on one block. This plan
> covers **only the 1998 Johnson slab on Golden Gate Avenue**. Every photograph of
> the Earl Warren's south front has this building looming behind it, and every
> photograph of this building from the plaza has the Earl Warren in front of it.

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready Hiram W. Johnson State Office Building GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of the Hiram W. Johnson State Office Building
(455 Golden Gate Avenue, SOM 1998, the 14-storey state office slab that shares the
Civic Center block with the Earl Warren Building) and deliver it as a downloadable,
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
8. `artifacts/earl-warren-building/` — the closest sibling: the same block, the
   same grid rotation, and the building this one stands directly behind
9. `docs/asset-plans/hiram-johnson-state-office-building.md` — this plan, whose
   dossier is your research starting point, not a substitute for your own
   verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Do not model the wrong building

Two traps, both on this block and one across the street:

- The **Earl Warren Building** is the low 1922 Beaux-Arts granite bar with the
  giant round-arched arcade on McAllister Street. It is 27 m tall, it is already
  shipped, and it is NOT part of this asset. It stands in front of this building
  in every plaza photograph.
- The **Phillip Burton Federal Building**, 450 Golden Gate Avenue, is the tall
  curved-plan tower with a US flag and a glazed entrance directly across Golden
  Gate Avenue to the north. A Street View camera standing on Golden Gate Avenue
  sees it filling half the sky. It is a different, taller, older building and is
  NOT part of this asset. Confirm which way the camera is facing before you trust
  a reference frame: this building carries **STATE OF CALIFORNIA** etched into the
  glass over its entrance and **THE HIRAM W. JOHNSON STATE OFFICE BUILDING**
  beneath it.

## Must capture

- A long pale slab — 127 m by 48 m by 62 m, near-white granite in large ashlar
  panels, with a dense regular grid of punched square windows
- The **two sculpted end drums** (east onto Polk, west onto Larkin). Each end is
  not a flat wall and not a single round bulge: it is **two convex granite piers
  with a deeply recessed curved glass bay between them**, the bay set back about
  7 m, ten storeys high, in teal glass. The outer corners are cut back again. This
  is the recognition cue, and the OSM polygon's stepped ends are the mapper's
  polygonal trace of exactly this profile (2.5)
- Narrow full-height **louvre slots** cut into the granite of the piers
- The **Golden Gate Avenue entrance**: a convex curved glass bay bulging north out
  of the flat granite wall, over a wide, gently curved projecting glass-and-metal
  canopy carried on square granite piers, two storeys tall
- The **top band**: the uppermost three storeys read as a lighter, more
  continuously glazed ribbon than the punched grid below them
- The **set-back mechanical penthouse** running along the centre of the roof,
  above an otherwise level parapet
- The designed roof: pale deck, level parapet ring, the long set-back mechanical
  penthouse, and the skylights over the twin ten-storey atria
- Night: the entrance canopy and its curved bay lit, and the two end glass bays
  glowing as the stair/atrium volumes they are

## Research the building independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- North (Golden Gate Avenue), east (Polk), south (plaza) and west (Larkin)
  elevations
- Aerial and roof/top views — the roof is a major surface here and this dossier's
  roof reading is the weakest part of it (see 2.16)
- Ground-level views, especially the Golden Gate Avenue entrance group
- Day and night appearance
- **The height.** Three numbers disagree and 2.3 reconciles them: SOM publishes
  203 ft, the 2010 city LiDAR gives a 53.61 m median roof plane and a 60.04 m
  maximum, and OSM tags `height=54`. Do not take any one of them alone.
- **SOM's "sweeping curve".** SOM's own project text says *"the sweeping curve of
  the tallest slab gestures out toward the plaza"*. Do not turn that sentence into
  a bowed south wall without checking: the OSM polygon's south edge is
  mathematically straight (its four intermediate nodes are exactly collinear), and
  a **rectilinear** re-projection of the Civic Center Plaza panorama shows the
  parapet running dead straight next to the Earl Warren's straight cornice. A
  cylindrical/equirectangular crop of the same panorama makes both of them arc,
  which is how this dossier got it wrong the first time. 2.5 resolves the curve as
  the end drums and the entrance bay. If you find a drawing that shows a curved
  south wall, that beats this reasoning — but a panorama does not.

Prefer architect/engineer publications, owner or institutional material,
planning and permitting documents, architectural press, geolocated photography,
and aerial/satellite imagery. Never rely on a single photograph, a single
AI-generated image, or a single unsourced 3D model. Separate verified facts from
visual inference; if sources disagree, document the disagreement and decide.

## Create a reference dossier

Write `artifacts/hiram-johnson-state-office-building/REFERENCE.md` containing:
source links and what each establishes; verified dimensions and location;
orientation; observations from all four sides and above; the 3-5 strongest
recognition cues; features to preserve; features to simplify; uncertainties and
conflicting evidence. A contact sheet of attributed reference thumbnails is
welcome if legally permissible — do not commit copyrighted full-resolution imagery.

## Make your own design decisions

Follow the conversion process in `docs/styles/miniature-toy.md` §22: identify the
recognition cues, strip nonessential information, rebuild the massing from a few
confident volumes, exaggerate only the signature features, simplify the facade
into broad rhythms, deliberately design every surface visible from above,
evaluate from the app's high three-quarter aerial camera, then simplify again.

The finished asset must be immediately recognizable as the Hiram W. Johnson State
Office Building, consistent with the real building from all four sides and above,
architecturally credible, and a premium handcrafted miniature — not
photorealistic, not voxel art, not generic low-poly, and never accurate in one
view while invented in the others.

This is a 62 m slab standing 200 m from City Hall's gilded dome, and it is the
tallest thing on the Civic Center's north edge. Its job in the skyline is to be a
calm pale wall that the dome reads against. Spend the budget on the bow, the two
end drums, the entrance bay and the roof; do not spend it on the ashlar joints or
the louvre blades, which are sub-pixel from the app's camera.

## Scope of the exported asset

Export the 1998 Johnson building only: its granite base, window grid, bowed south
front, two end drums with their curved glass bays, Golden Gate Avenue entrance bay
and canopy, louvre slots, stepped end masses, parapet, roof deck, atrium
skylights and rooftop mechanical.

Do not include unrelated surrounding city geometry: the Earl Warren Building, the
Phillip Burton Federal Building, Civic Center Plaza, City Hall, the McAllister /
Polk / Larkin / Golden Gate streets, street trees, people, vehicles, plinths,
cameras or lights. Temporary context may appear in review renders but must not
leak into the GLB.

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
long axis runs at bearing **81.27 deg**; the public entrance faces **north** onto
Golden Gate Avenue, which is the opposite of the contract's nominal "front faces
−Y" convention. Real-world orientation wins; record the measured heading in
`REPORT.md` and note explicitly that the entrance is on +Y.

**Height normalisation:** normalise the bbox top to 61.90 m exactly, so the
loader's `targetHeightM / measuredHeight` scale lands at 1.0.

## Reproducible Blender workflow

Blender 4.5 LTS is at `/opt/blender` (`blender` on PATH). Headless only:
`blender -b --python script.py -- args`; no GPU, so use Workbench or CPU Cycles.

Keep `artifacts/hiram-johnson-state-office-building/build_hiram_johnson.py`
(deterministic build script),
`artifacts/hiram-johnson-state-office-building/hiram-johnson-state-office-building.blend`,
and `artifacts/hiram-johnson-state-office-building/hiram-johnson-state-office-building.glb`.
The script must rebuild the model reliably enough for future revision. Do not
modify or rename an unrelated existing GLB to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`hiram-johnson-top.png`, `hiram-johnson-north.png`, `hiram-johnson-east.png`,
`hiram-johnson-south.png`, `hiram-johnson-west.png`, plus
`hiram-johnson-contact-sheet.png`, at least one high three-quarter aerial beauty
render `hiram-johnson-aerial.png`, and a night render `hiram-johnson-night.png`.

The four elevations must share scale, framing, lighting, exposure and projection;
use orthographic or long-lens cameras; label directions from the researched
orientation; the top view must clearly show the arced parapet crest, the
mechanical band and the atrium skylights; the aerial view uses the style bible's
camera assumptions (30-50 degrees down, long lens). Simple tabletop lighting,
neutral warm background, minimal depth of field, and every image must depict the
same exported model. The night render must show the `_Glow` set driven from Base
Color (see the note at the end of `docs/asset-plans/README.md`).

## Validate the exported GLB

Re-import the GLB into a fresh isolated Blender scene and validate the re-import,
not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture
count, camera count, light count, animation count, applied-transform status,
negative-scale status, normal-orientation status, unexpected geometry, and
per-material contract compliance. Render at least one review image from the
re-imported asset. Write
`artifacts/hiram-johnson-state-office-building/validation.json` and
`artifacts/hiram-johnson-state-office-building/REPORT.md`.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "hiram-johnson-state-office-building",
  "file": "hiram-johnson-state-office-building.glb",
  "anchor": [
    -122.4179151,
    37.7810345
  ],
  "targetHeightM": 61.9,
  "cat": 18,
  "name": "Hiram W. Johnson State Office Building",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a separate, explicitly requested job — run `docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in `docs/asset-plans/hiram-johnson-state-office-building.md`.
````

---

## Part 2 — Research and design dossier

Compiled 19 August 2026 from the sources in 2.2. Values marked *inferred* or
*estimated* are visual or derived, not published figures — the executing agent
must re-verify anything it relies on.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Built | selected 1995, design finished 1996, completed **1998** | SOM project page; Clark Construction; FoundSF |
| Architect | **Skidmore, Owings & Merrill**; Page & Turnbull on the Earl Warren half | SOM; Forell/Elsesser; Clark Construction |
| Developer / GC | Hines + Clark Construction, design-build, $265M | Hines; Clark Construction |
| Storeys | **14** | SOM ("Number of Stories: 14"); OSM `building:levels=14`; Clark; Hines |
| Building height | **203 ft = 61.87 m** | SOM project page ("Building Height: 203 feet") |
| Main roof plane above grade | **53.61 m** | DataSF Building Footprints `hgt_median_m`, record `mblr=SF0765003` (2010 LiDAR, measured) |
| Highest LiDAR return | **60.04 m** (`hgt_maxcm` 6004) | same record (measured) — see 2.3 |
| Site grade NAVD88 | 19.96 m minimum, 23.18 m median | DataSF `gnd_min_m`, `gnd_mediancm` |
| Gross area | 830,000 sq ft new build (1,030,000 sq ft with the Earl Warren) | Clark Construction; Hines; SOM |
| Floor plates | ~50,000 sq ft | Hines |
| Structure | welded steel moment frame with **292 passive dampers** — the first US use of that combination | Forell/Elsesser |
| Interior | **twin atria rising ten storeys** above the law libraries | Flickr/wallyg citing the building; Hines ("one-story twin atriums" at grade) |
| Why only 14 storeys | two more floors would have shadowed a neighbouring school playground | FoundSF |
| Replaced | a 1950s six-storey glass-and-steel state building damaged in Loma Prieta | FoundSF |
| Occupants | California Supreme Court support, 1st District Court of Appeal, Judicial Council, ~11 state agencies, ~2,100 staff | Clark Construction; FoundSF |
| Footprint (polygon) | **5,614 m2** | OSM way/35176304, reprojected + shoelace (measured) |
| Footprint (oriented box) | **127.38 x 47.81 m** | min-area OBB over the OSM polygon (measured) |
| Long-axis bearing | **81.27 deg** (8.73 deg north of due east) | derived from the OBB (measured) |
| OBB centre | **−122.4179151, 37.7810345** | derived (measured) |
| LiDAR footprint area | 5,632 m2 (22,530 cells at 0.5 m) | DataSF `mblr=SF0765003` — within 0.4% of the OSM polygon, confirming it is the right building |
| Awards | DBIA Western Pacific Design-Build (Public Sector) 2000; National Design-Build Award, Best Public Project over $15M | Clark Construction; Hines |

### 2.2 Sources

- https://www.openstreetmap.org/way/35176304 — footprint geometry, `height=54`, `building:levels=14`, `name=Hiram W. Johnson State Office Building`, `addr:housenumber=455`
- Overpass `way(35176304); out geom;` — the 26-node polygon actually measured here
- https://www.som.com/projects/san-francisco-civic-center-complex/ — **the design statement and the height**: "Building Height: 203 feet, Number of Stories: 14, Completion Year 1998", and the massing description: *"SOM tucked the addition behind the historic courthouse… A massing that consists of slim slabs that gradually step upward further integrates the new structure into its context… The sweeping curve of the tallest slab gestures out toward the plaza while deferring to the dome of the nearby City Hall."*
- https://www.hines.com/properties/san-francisco-civic-center-complex-san-francisco — 14 storeys, 830,000 sq ft, 50,000 sq ft floor plates, twin atriums, $265M, Hines/SOM/Clark JV selected 1995
- https://www.clarkconstruction.com/our-work/projects/san-francisco-civic-center — completion 1998, 830,000 sq ft, 14 storeys, ~11 agencies, 2,100 employees, design-build
- https://forell.com/projects/hiram-w-johnson-state-office-building-earl-warren-supreme-court-building — welded steel moment frame, 292 passive dampers, seismic joint between the two buildings, large atria
- https://www.foundsf.org/Fun_Facts_about_the_Ronald_M._George_State_Office_Complex — the 14-storey limit and the school playground, the 1950s predecessor, the atrium terrazzo, the complex naming
- https://www.dgs.ca.gov/RESD/Resources/List-of-DGS-Managed-Office-Buildings/Page-Content/List-of-DGS-Office-Buildings/Balance-of-the-State/Earl-Warren-Hiram-W-Johnson-Building — DGS treats the two addresses as one building, which is where the confusion with 350 McAllister starts
- https://www.flickr.com/photos/wallyg/3953727511 — "the adjoining Hiram W. Johnson Building… built in 1998 by Skidmore, Owings & Merrill… twin atria rising 10 stories above the law libraries"
- https://data.sfgov.org/resource/ynuv-fyni.json (`mblr=SF0765003`) — 2010 LiDAR: `hgt_median_m` 53.61, `hgt_maxcm` 6004, `hgt_meancm` 5351, `hgt_stdcm` 421, `hgt_majoritycm` 5305, `gnd_min_m` 19.96, 22,530 cells
- Google Street View panoramas, resampled to metric cylindrical strips (all four sides): `W2bcY729K7xMvPk6BrBEiw` (Golden Gate Avenue, the entrance bay and STATE OF CALIFORNIA lettering), `4c8cOs4QIqxMprgTr44lKg` (Polk, the NE drum), `hairaoqsCzZ5yUF9ZZO4-Q` (Larkin, the west drum and its curved glass bay), `ztTkGZ3MnkjO_cs4mOvpRw` (Civic Center Plaza — **the key frame**: the whole bowed south front rising behind the Earl Warren cornice), `by2PvOmdKeqlMZAdVQyy3Q` (Larkin & McAllister, the Earl Warren in front)
- Esri World Imagery nadir-ish tiles at z20 over the block — the roof band, the parapet ring, and the shadow the slab throws across Golden Gate Avenue

### 2.3 The height (read this before modelling)

Three sources, three numbers, and they are all describing different things:

| Source | Value | What it is |
|---|---|---|
| DataSF 2010 LiDAR `hgt_median_m` | **53.61 m** | the main roof plane over most of the plate |
| DataSF 2010 LiDAR `hgt_maxcm` | **60.04 m** | the highest thing on the roof |
| OSM `height` | 54 | a roof-plane tag, agrees with the median |
| SOM project page | **203 ft = 61.87 m** | the architect's published building height |

Take **61.9 m as `targetHeightM`** (the architectural crest) and **53.6 m as the
main roof deck**. The composition that satisfies all four rows is a 53.6 m slab
with a raised element over the centre topping out near 62 m — which is exactly
what the plaza photograph shows: an arced parapet crest with a set-back band above
it. The 1.8 m between the LiDAR maximum and SOM's figure is the parapet or screen
wall that a 0.5 m LiDAR cell clips at a roof edge.

Sanity check on the storey count: 53.6 m over 14 storeys is 3.83 m floor to floor,
which is right for a 1990s court/office building with a tall ground floor. 61.9 m
over 14 would be 4.4 m, which is not.

Do **not** apply the `hgt_maxcm` caution from `docs/asset-plans/earl-warren-building.md`
§2.3 here. That rejection was for the Earl Warren record, whose 46.39 m maximum is
a single LiDAR cell on the party wall it shares with *this* building. This record's
own maximum is a large, coherent, in-footprint return, and it is corroborated by
SOM's published height. Different record, different verdict.

### 2.4 Orientation and placement

The building fills the northern band of the block bounded by Golden Gate Avenue
(north), Polk (east), McAllister (south) and Larkin (west). The Earl Warren
Building fills the southern band; a seismic joint, not a service alley, separates
them — the two structures are designed to move independently in an earthquake.

The long axis runs at bearing **81.27 deg**, the Civic Center grid, 8.73 deg
counter-clockwise from due east — the same rotation as the Earl Warren's 81.33 deg
and the Asian Art Museum's 81.68 deg. In Blender that is a +8.73 deg rotation about
Z from an axis-aligned box, with `+Y` = true north.

The public entrance faces **north** onto Golden Gate Avenue. This is one of the
landmarks where the contract's nominal "front faces −Y" and the real world
disagree; real-world orientation wins, because `placeGeneric` applies no rotation
and a mirrored building would be wrong from every side. Say so in `REPORT.md`.

Anchor on the OBB centre. The area-weighted centroid of the OSM polygon
(−122.4179135, 37.7810351) sits 0.15 m from it, so the two agree here and either
would do; the OBB centre is the convention for a slab of this shape.

### 2.5 What each side shows

**South (Civic Center Plaza) — the hero elevation, and the only one most people
ever read.** From the plaza, above the Earl Warren's modillion cornice, a broad
pale wall rises for about nine storeys. It is **flat**, not bowed — see the note
below. The facade is a dense grid of square punched windows in near-white granite,
grouped three-to-a-bay between wider piers; the glass reads pale **sea-green** in
daylight, which is the one colour on the building. The uppermost three storeys
change: the punched grid gives way to a lighter, more continuously glazed ribbon
with thin white mullions. Above that, a level parapet, and set back behind it a
long **mechanical penthouse** running most of the length of the roof, reading as a
dark recessed band with pale posts.

*On the curve.* SOM writes that "the sweeping curve of the tallest slab gestures
out toward the plaza", and this dossier's first draft turned that into a 5 m bow
across the south front. It is not there. Two independent checks: the OSM polygon's
south edge is a straight line to within 1 cm over 91 m (nodes at E = 26.4, 51.1,
77.5, 103.2 in the grid frame are exactly collinear), and a **rectilinear**
re-projection of the Civic Center Plaza panorama shows the Johnson parapet running
dead straight beside the Earl Warren's straight cornice. The arcs that appear in a
cylindrical crop of the same panorama are the projection, not the building — the
Earl Warren cornice arcs identically in those frames and it is known to be
straight. The curves SOM is describing are real, but they are the **end drums and
the north entrance bay**, which are unmistakable from three separate Street View
positions.

**North (Golden Gate Avenue) — the entrance.** A flatter granite wall with the
same punched grid, interrupted at the centre by the building's best piece of
architecture: a **convex curved glass bay** bulging out of the wall, five or six
storeys tall, in pale glass with strong horizontal mullions and a projecting metal
eyebrow at its top. Under it, a wide, gently curved, projecting **glass-and-metal
canopy** carried on four square granite piers, and behind that a two-storey glazed
lobby with **STATE OF CALIFORNIA** etched across it and **THE HIRAM W. JOHNSON
STATE OFFICE BUILDING** in smaller letters beneath. A flagpole stands in front.
(Directly across the street, and in every frame, is the Phillip Burton Federal
Building — not this asset.)

**East (Polk Street) and west (Larkin Street) — the drums.** The best-resolved part
of the building, because the OSM polygon and the photographs agree exactly. Each
short end is a five-part profile, read here off the reprojected polygon in the grid
frame (E measured from the west face, N from the south face):

| N band | west end E | what it is |
|---|---|---|
| 0.0 – 7.5 | 7.2 | south corner, cut back |
| 7.5 – 18.3 | 0.0 | **convex granite pier**, the full projection |
| 18.3 – 30.7 | 8.0 | the **recessed curved glass bay**, set back ~7.5 m |
| 30.7 – 40.5 | 1.4 | **convex granite pier** |
| 40.5 – 47.8 | 8.0 | north corner, cut back |

The east end mirrors it (piers at E = 126.7 and 127.4, bay recessed to E = 120.1,
corners at E = 119.6). Photographs turn that stepped trace into what it really is:
large-panel granite walls curving continuously round each pier, no punched windows
over long stretches, tall narrow full-height **louvre slots** cut into the stone,
and between the piers a tall **recessed curved glass bay** about ten storeys high
in teal glass with horizontal mullion bands — a great glazed slot between two stone
drums. The ground floor on Polk carries a small retail/café window; Larkin's base
is blind stone and louvres.

**Top.** A pale roof deck inside a level parapet ring. Along the centre, set back
from both long faces, the **mechanical penthouse** rises to ~60 m and carries the
architectural crest to 61.9 m — this is the 60.04 m LiDAR maximum and the 6 m gap
between the 53.61 m median roof plane and SOM's 203 ft. Long skylight strips run
over the two ten-storey atria, and a cluster of low mechanical enclosures and a
stair penthouse sit toward the Golden Gate Avenue edge. *The roof reading is the
weakest part of this dossier* — the only imagery available is off-nadir and half in
the building's own shadow. See 2.16.

### 2.6 Recognition cues (ranked)

1. **The end drums.** Two convex granite piers with a deeply recessed ten-storey
   curved glass bay between them, at both short ends. Nothing else in Civic Center
   does this, and it is the one thing every close view of the building shows
2. The proportion and colour pair: a 127 m near-white granite slab, dense square
   window grid, pale sea-green glass, standing twice the height of the Beaux-Arts
   bar in front of it
3. The Golden Gate Avenue **entrance bay and canopy** — a convex glass bulge over a
   wide curved canopy on granite piers, with STATE OF CALIFORNIA on the glass
4. The lighter, more glazed **top three storeys** over the punched grid below
5. From above: a level parapet with a long set-back **mechanical penthouse** down
   the centre of the roof

### 2.7 Miniature translation

**Preserve**

- The 127 x 48 x 62 m proportion and the 8.73 deg grid rotation
- The five-part end profile — pier, recessed glass bay, pier — at both ends, with
  the piers genuinely curved. If the ends flatten into a box, the building stops
  being this building
- The level parapet with the set-back mechanical penthouse behind it
- The lighter glazed band over the top three storeys
- The near-white granite / one-accent-colour discipline — this building's job in
  the skyline is to be calm

**Simplify / exaggerate**

- The punched window grid becomes a regular field of recessed square panels at a
  ~6.4 m horizontal pitch and one per storey vertically, grouped into readable
  bands rather than 14 x 20 individually modelled openings
- The curved glass bays become single smooth recessed cylindrical surfaces with
  four horizontal mullion bands, not curtain-wall grids
- The entrance bay and canopy are semantically enlarged — a storey taller and a
  metre deeper than scale demands, because they are the building's face and are a
  few pixels from the app's camera
- All ashlar jointing collapses into the material colour; all louvre blades
  collapse into a single dark recessed slot
- Rooftop clutter becomes: one penthouse mass, two skylight strips, three
  mechanical boxes, one stair penthouse

### 2.8 Massing recipe

Build order for the deterministic script. Author in the **grid frame** — E from 0
(west face) to 127.38 (east face), N from 0 (south face) to 47.81 (north face),
Z up — then rotate the whole assembly +8.73 deg about Z and recentre. Dimensions
are the starting point, not a straitjacket; adjust after the first aerial render.

The plan outline (used for the base, the body and the parapet) is the reprojected
OSM polygon of 2.5, with the two end profiles rebuilt as arcs: each granite pier
is a convex arc bulging to the end face, and the bay between them a concave arc
recessed 7.5 m, with the outer corners cut back.

1. Granite base: full outline, z=0 to z=6.0, `Toy_stone`, projecting 0.3 m — the
   two-storey base, blind except for the entrance and the Polk shopfront.
2. Main body: same outline inset 0.3 m, z=6.0 to z=53.6, `Toy_cream`.
3. Punched window grid: recessed `Toy_glass` panels 3.6 m wide x 2.4 m tall,
   0.35 m deep, at 6.4 m horizontal pitch and 3.83 m vertical pitch, from z=9.8 to
   z=42.1, on the north and south faces only.
4. Storey banding: `Toy_trim` bands 0.3 m tall projecting 0.12 m at z=9.5, 21.0,
   32.5 and 42.1 — enough rhythm to stop the grid reading as wallpaper.
5. Top band: z=42.1 to z=53.6, inset 0.5 m from the body face, a lighter, more
   continuously glazed ribbon — three `Toy_glass` bands 2.8 m tall running the full
   length of the north and south faces, separated by `Toy_trim` spandrels.
6. End glass bays: in the recessed middle of each end, a concave `Toy_teal`
   cylindrical surface 12.4 m wide (N 18.3-30.7), from z=13.4 to z=51.5, with four
   `Toy_trim` mullion bands.
7. Louvre slots: four `Toy_roofd` slots per end, 1.6 m wide, 0.5 m deep, running
   z=6.0 to z=53.6 on the pier faces.
8. Parapet: `Toy_trim` ring z=53.6 to z=55.0, inset 1.0 m, 1.0 m thick and hollow,
   so the roof deck reads inside it.
9. Roof deck at z=53.6, `Toy_roofd`, spanning inside the parapet.
10. Mechanical penthouse: `Toy_cream` block, E 22 to 96, N 13 to 35, z=53.6 to
    z=60.4, with a `Toy_roofd` louvre band around it z=56.0 to z=58.6 and a
    `Toy_trim` cap z=60.4 to z=61.9 — this is what carries the bbox to 61.90 m.
11. Atrium skylights: two `Toy_teal` panels, each 20 x 7 m, centred at E = 34 and
    E = 93, N = 24, top at z=54.6, on 0.5 m `Toy_trim` curbs.
12. Mechanical: three `Toy_roofd` boxes 5 x 4 x 2.2 m and one 10 x 5 x 3.0 m stair
    penthouse along the north edge of the deck.
13. Entrance bay: a convex `Toy_glassl_Glow` cylindrical bulge on the north face,
    centred at E = 63.7, 24 m wide, projecting 3.5 m, from z=6.0 to z=27.0, with
    three `Toy_trim` mullion bands and a `Toy_trim` eyebrow cap projecting 1.2 m at
    its top.
14. Entrance canopy: a curved `Toy_trim` slab 30 m wide, 7 m deep, 0.8 m thick at
    z=10.5, carried on four `Toy_stone` piers 2.2 x 2.2 m; `Toy_gold_Glow` soffit
    plate beneath it.
15. Lobby glazing: `Toy_gold_Glow` recessed plane 22 m wide, z=1.0 to z=9.6, set
    2.0 m back behind the canopy.
16. Polk shopfront: one `Toy_glass` recess 7 x 3 m in the east base at z=1.5.
17. Curve segments 14 per arc; bevel 0.12 m, 2 segments.

### 2.9 Materials and palette

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_cream` | `#f2ede3` | main granite body above the base, crest / mechanical band |
| `Toy_stone` | `#d9d2c2` | two-storey granite base, entrance piers |
| `Toy_trim` | `#f3efe6` | storey bands, parapet, mullion bands, canopy, eyebrow, skylight curbs, flagpole |
| `Toy_glass` | `#2a4d73` | the punched window grid, Polk shopfront |
| `Toy_teal` | `#3fa8a0` | the two end curved glass bays, the two atrium skylights |
| `Toy_roofd` | `#45454a` | roof deck, louvre slots, mechanical boxes, stair penthouse |
| `Toy_glassl_Glow` | `#6f95b8` | the Golden Gate Avenue entrance bay glazing |
| `Toy_gold_Glow` | `#caa64a` | the canopy soffit and the lobby glazing behind it |

**One deliberate deviation, recorded here so nobody "fixes" it later.** The real
punched windows read pale sea-green in daylight, not dark navy. `Toy_glass`
`#2a4d73` is used for them anyway: 260 pale windows in a pale wall give the aerial
camera nothing to read, and the style bible's window philosophy (§5) is explicit
that windows are graphical elements before they are literal openings. The sea-green
is kept where it is doing identity work — the two big curved bays and the roof
skylights, in `Toy_teal`. If a reviewer wants the honest colour on the grid,
`Toy_glassl` is the swap, but check it from the app's camera first.

Night glow: hero = the Golden Gate Avenue entrance (`Toy_glassl_Glow` bay +
`Toy_gold_Glow` canopy soffit and lobby), which is genuinely the only lit thing on
this building at street level. Supporting = nothing else. Three glow surfaces,
grouped in one place, so the night silhouette is a pale slab with one warm doorway
under a lit bulge. Their day colours (`6f95b8` light glass, `caa64a` gold) are
palette neighbours of the non-glow set, so the daylight asset stays calm — and per
the repo's standing correction, a `_Glow` material's **base colour is its night
look**, so do not pick a dark base and expect the night render to rescue it.

Explicitly **not** glowing: the two end curved bays and the window grid. A 127 m
wall of lit windows 200 m from City Hall would out-shout the dome, which is the
one thing SOM designed this building not to do.

### 2.10 Top surface

127 x 48 m of roof under a camera that looks down, and the second-largest roof in
Civic Center after City Hall. The design: a pale deck inside a parapet ring whose
top edge **arcs with the bow**, a long `Toy_cream` crest block over the centre
carrying the set-back mechanical band up to 61.9 m, two teal atrium skylight
strips flanking it, a small mechanical cluster and stair penthouse along the
Golden Gate Avenue edge, and the two stepped-down end decks 11.5 m lower with
their own parapets. The teal skylights and the height break are what make this
building identifiable from the app's default altitude, where the window grid has
dissolved into texture. Do not flatten the crest to a single plane "for
simplicity" — the step is the silhouette.

### 2.11 Scope

**In the GLB:** granite base, main body with bowed south front and two end drums,
punched window grid, storey bands, end curved glass bays, louvre slots, stepped
end masses, parapet, roof deck, crest and mechanical band, atrium skylights,
mechanical boxes, stair penthouse, entrance bay, canopy, piers, lobby glazing,
Polk shopfront, flagpole

**Not in the GLB:** the Earl Warren Building, the Phillip Burton Federal Building
across Golden Gate Avenue, Civic Center Plaza, City Hall, the McAllister / Polk /
Larkin / Golden Gate streets, street trees, people, vehicles, plinths, cameras or
lights

### 2.12 Triangle budget

Cap 26,000. Suggested split: body shell with the bow and the two drums ~6k; the
punched window grid ~8k; storey bands and parapet ~2k; the two end curved bays and
their louvre slots ~3k; roof deck, crest, mechanical band, skylights and
mechanical ~3k; entrance bay, canopy, piers, lobby and flagpole ~3k.

### 2.13 Draft manifest entry

```json
{
  "id": "hiram-johnson-state-office-building",
  "file": "hiram-johnson-state-office-building.glb",
  "anchor": [
    -122.4179151,
    37.7810345
  ],
  "targetHeightM": 61.9,
  "cat": 18,
  "name": "Hiram W. Johnson State Office Building",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

`dims` and `tris` are placeholders until the asset is built and validated.
`loadRadius` is the default rule `max(2500, 61.9 x 30)` = 2500.

### 2.14 Integration notes (for later, not this task)

- **New landmark (Case B).** Add a `pipeline/lib/landmarks.mjs` entry
  (`id: 'hiramJohnsonStateOfficeBuilding'` under the registry's camel conversion —
  confirm against `app/src/landmarks.js` before wiring), lon/lat as above,
  height 61.9, plus an exclusion radius, **and re-bake the affected tiles**, or the
  baked procedural slab will intersect the GLB.
- **The exclusion radius must be small, and that is not a mistake.** `excluded()`
  drops a footprint whose centroid *or any ring vertex* falls inside the radius.
  This building's own footprint centroid sits 0.15 m from the anchor, so it is
  caught by any radius at all. Meanwhile the OBB half-diagonal is **68.0 m**, and a
  circle anywhere near that reaches straight through the seismic joint into the
  Earl Warren footprint 39 m away — and the Earl Warren is a shipped landmark whose
  own `exclude: 12` already removed it from the bake, so a fat radius here would
  delete nothing useful and risk the Civic Center Plaza Garage kiosk instead.
  Start the measurement at **6–12 m** and size it the repo way: against the real
  bake input (`pipeline/data/overture_buildings.geojsonseq`), with the same
  centroid-or-vertex metric, over every footprint in the surrounding bbox, printing
  the drop count per radius. Record that table in the integration report.
- Do not assume the bake's footprint for this building is the OSM one. Overture and
  DataSF both trace this block and they disagree at the ends; verify the anchor
  actually falls inside whatever ring the bake carries before choosing the radius.
- Civic Center already carries `city-hall`, `opera-house`, `asian-art-museum`,
  `civic-center-courthouse`, `civic-center-plaza`, `earl-warren-building`,
  `500-van-ness` and more in flight. If other landmarks are being built alongside
  this one, run stage 5 in **batch mode** — commit source only and let
  `docs/asset-pipeline/BATCH-INTEGRATE.md` bake the city once.
- The shared landmark `BatchedMesh` is the other constraint: this is a 26k-triangle
  asset landing in the densest landmark cluster in the city. Check the reserve
  before and after (`sf3d-batch-reserve-overflow`), not just the draw-call count.

### 2.15 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Bbox Z normalised to 61.90 m exactly, so the loader's scale lands at 1.0
- [ ] Long axis 127.4 m, depth 47.8 m, both after the +8.73 deg rotation
- [ ] Triangles at or under 26,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the entrance bay, canopy soffit and lobby glazing
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (per-object signed
      volume authoritative; ray test residual <= 0.15%)
- [ ] No foreign/leaked geometry — and specifically no trace of the Earl Warren
      Building or the Phillip Burton Federal Building
- [ ] Seven review renders + night render + contact sheet regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.16 Open questions and risks

- **The roof is the weakest evidence in this dossier.** The only nadir-ish imagery
  available (Esri z20) is off-nadir enough that the north facade leans across its
  own roof, and half the block is in the slab's shadow. The parapet ring, the crest
  block and the stepped ends are read from the plaza elevation and the LiDAR
  statistics; the two atrium skylight strips are *inferred* from the published
  "twin atria rising ten storeys" and the roof band, not seen clearly. Positions,
  sizes and count in 2.8 steps 10–11 are *estimated*. One good oblique aerial would
  settle all of it.
- **The flat-south-front finding is a correction to this dossier's own first
  draft**, and it is argued from two sources (the collinear OSM nodes and a
  rectilinear panorama re-projection), not from a drawing. It is the strongest
  claim here that a plan set could overturn. If it is overturned, the fix is local:
  bow the body profile and the parapet, nothing else changes.
- **The z=42.1 m break between the punched grid and the glazed top band is
  *inferred*** from the plaza photograph, where the upper three storeys visibly
  change character. Three storeys is a reading, not a count off drawings.
- **The mechanical penthouse footprint (E 22-96, N 13-35) is *estimated*.** The
  LiDAR maximum of 60.04 m and standard deviation of 4.21 m over 22,530 cells say
  something substantial stands ~6.4 m above the median roof plane; they do not say
  where it sits or how big it is. The plaza photograph shows it running along the
  centre. Size and position are a design choice consistent with both.
- **Wrong-building risk runs both ways on this block.** Working from the address
  "455 Golden Gate Avenue" is safe; working from a Golden Gate Avenue Street View
  frame is not, because the Phillip Burton Federal Building fills the north side of
  the street and is also a big pale curved-plan slab with a flag and a glazed
  entrance. The STATE OF CALIFORNIA lettering is the tell.
- **SOM's "slim slabs that gradually step upward" may describe more steps than this
  plan models.** The dossier resolves it into one main plate at 53.6 m plus a
  set-back penthouse at 60.4-61.9 m. That is a defensible simplification at toy
  scale and it satisfies every measured number, but it is a compression of the
  architect's own description — say so in `REPORT.md` rather than presenting it as
  measured.
- This building is 200 m from City Hall's gilded dome and stands directly behind a
  Beaux-Arts landmark that is already shipped. SOM designed it to defer to the
  dome. If it reads as loud in the aerial render, take saturation out of everything
  except the two end bays and the roof skylights.
