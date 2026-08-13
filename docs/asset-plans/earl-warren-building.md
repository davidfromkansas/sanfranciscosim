# Earl Warren Building — SF-SIM asset plan

Bliss & Faville's 1922 California State Building at 350 McAllister Street: a 115 m
bar of pale granite facing City Hall across Civic Center Plaza, whose whole identity
is one uninterrupted arcade of tall round-arched windows over three carved entrance
portals. Home of the Supreme Court of California. From the app's aerial camera it is
also a designed roof — two big turquoise light-court skylights and a central
courtroom lantern.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/earl-warren-building/`. This document is the plan only: Part 1 is the
runnable task prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `earl-warren-building` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.14) |
| WGS84 anchor | `-122.4178413, 37.7806865` (oriented-bounding-box centre, measured) |
| Target height | **27.0 m** parapet crest; main roof plane **25.1 m** |
| OSM footprint | 115.49 x 31.52 m oriented box, 2,968 m2 polygon (OSM way/260137839, measured) |
| Long-axis bearing | 81.33 deg — the Civic Center grid, 8.67 deg north of due east |
| Triangle cap | 22,000 |
| Category | `18` (government / courthouse) |

> **Address warning.** This building is **350 McAllister Street**. The address
> *455 Golden Gate Avenue* belongs to the **Hiram W. Johnson State Office Building**
> (OSM way/35176304, 14 storeys, 54 m) — the white bow-fronted slab filling the north
> half of the same block. DGS manages the two as one "Earl Warren / Hiram W. Johnson"
> complex under a single address, which is how the confusion starts. They are two
> separate assets; this plan covers only the 1922 building.

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready Earl Warren Building GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of the Earl Warren Building (350 McAllister
Street, the 1922 California State Building, home of the Supreme Court of
California) and deliver it as a downloadable, validated GLB.

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
8. `artifacts/asian-art-museum/` — the closest sibling: same block, same grid
   rotation, same pale-granite Beaux-Arts problem, most recent scripts
9. `docs/asset-plans/earl-warren-building.md` — this plan, whose dossier is your
   research starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Do not model the wrong building

The Earl Warren Building is the **low 1922 granite bar on McAllister Street**, six
storeys, 27 m. The tall white curved slab immediately behind it in almost every
photograph is the **Hiram W. Johnson State Office Building** (455 Golden Gate
Avenue, 54 m) — a different building, not part of this asset. Every reference
photograph of the south elevation contains both. Crop the Johnson building out of
your thinking before you start massing.

## Must capture

- A long, low, pale-granite bar — 115 m by 31 m by 27 m, four times as long as it
  is tall. This is a wall of a building, not a block
- The **giant arcade**: one continuous run of tall round-arched window bays across
  the entire McAllister (south) front, each with a keystone cartouche and a
  balustraded sill. This is the recognition cue; nothing else comes close
- The **three carved entrance arches** at the centre of the south front, with their
  recessed porch, heavily ornamented archivolts and flanking bracket lanterns
- A heavy modillion cornice and a light attic storey above the arcade
- The diagonal flagpoles projecting from the south facade (California + US flags)
- The designed roof: two large turquoise glazed light-court skylights, a central
  raised courtroom lantern with twin ornamental laylights, and a dark sloping
  mansard band along the McAllister edge
- Night: the three entrance arches lit gold, and the courtroom laylights glowing
  from inside

## Research the Earl Warren Building independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- North, east, south and west elevations
- Aerial and roof/top views — the roof is a major surface here
- Ground-level views, especially the entrance group
- Day and night appearance
- Publicly available drawings, plans or diagrams (HABS/HAER documentation exists
  for "California State Building, 350 McAllister Street" at the Library of Congress)
- **The height.** OSM `height=27` on way/260137839 agrees with Wikipedia's 87 ft
  and with the 2010 city LiDAR roof plane (25.11 m median + parapet), so unusually
  for this repo the tag is trustworthy. What is NOT trustworthy is the same LiDAR
  record's `hgt_max` of 46.39 m — see this plan's 2.3 before using it.
- The exact bay count of the arcade, which this dossier read off photographs

Prefer architect/engineer publications, owner or institutional material,
planning and permitting documents, architectural press, geolocated photography,
and aerial/satellite imagery. Never rely on a single photograph, a single
AI-generated image, or a single unsourced 3D model. Separate verified facts from
visual inference; if sources disagree, document the disagreement and decide.

## Create a reference dossier

Write `artifacts/earl-warren-building/REFERENCE.md` containing: source links and
what each establishes; verified dimensions and location; orientation; observations
from all four sides and above; the 3-5 strongest recognition cues; features to
preserve; features to simplify; uncertainties and conflicting evidence. A contact
sheet of attributed reference thumbnails is welcome if legally permissible — do not
commit copyrighted full-resolution imagery.

## Make your own design decisions

Follow the conversion process in `docs/styles/miniature-toy.md` §22: identify the
recognition cues, strip nonessential information, rebuild the massing from a few
confident volumes, exaggerate only the signature features, simplify the facade
into broad rhythms, deliberately design every surface visible from above,
evaluate from the app's high three-quarter aerial camera, then simplify again.

The finished asset must be immediately recognizable as the Earl Warren Building,
consistent with the real building from all four sides and above, architecturally
credible, and a premium handcrafted miniature — not photorealistic, not voxel art,
not generic low-poly, and never accurate in one view while invented in the others.

This building is 115 m long and 27 m tall, and it sits 60 m from City Hall's dome.
It will be read mostly from above and at a shallow angle, and it must stay calm
enough not to compete with City Hall. Spend the budget on the arcade rhythm, the
cornice line and the roof; do not spend it on the carved archivolts, which are two
pixels wide from the app's camera.

## Scope of the exported asset

Export the 1922 building only: its plinth, rusticated base, entrance arches and
porch, arcade, cornice, attic, parapet, roof deck, mansard band, light-court
skylights, courtroom lantern and rooftop mechanical boxes, plus the facade
lanterns and flagpoles.

Do not include unrelated surrounding city geometry: the Hiram W. Johnson State
Office Building, Civic Center Plaza, City Hall, the Civic Center Plaza Garage
entrance kiosk that stands in front of the south facade, McAllister / Polk /
Larkin / Golden Gate streets, street trees, people, vehicles, plinths, cameras or
lights. Temporary context may appear in review renders but must not leak into the
GLB.

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
(`placeGeneric` in `app/src/assets.js` only scales and positions). The building's
long axis runs at bearing **81.33 deg**; the main entrance faces **south** onto
McAllister Street. Here the contract's "front faces −Y" rule and real-world
orientation happen to agree, up to the 8.67 deg grid rotation. Record the measured
heading in `REPORT.md`.

**Height normalisation:** normalise the bbox top to 27.00 m exactly, so the
loader's `targetHeightM / measuredHeight` scale lands at 1.0.

## Reproducible Blender workflow

Blender 4.5 LTS is at `/opt/blender` (`blender` on PATH). Headless only:
`blender -b --python script.py -- args`; no GPU, so use Workbench or CPU Cycles.

Keep `artifacts/earl-warren-building/build_earl_warren_building.py` (deterministic
build script), `artifacts/earl-warren-building/earl-warren-building.blend`, and
`artifacts/earl-warren-building/earl-warren-building.glb`. The script must rebuild
the model reliably enough for future revision. Do not modify or rename an unrelated
existing GLB to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`earl-warren-building-top.png`, `earl-warren-building-north.png`,
`earl-warren-building-east.png`, `earl-warren-building-south.png`,
`earl-warren-building-west.png`, plus `earl-warren-building-contact-sheet.png`, at
least one high three-quarter aerial beauty render `earl-warren-building-aerial.png`,
and a night render `earl-warren-building-night.png`.

The four elevations must share scale, framing, lighting, exposure and
projection; use orthographic or long-lens cameras; label directions from the
researched orientation; the top view must clearly show the two light-court
skylights, the central courtroom lantern and the mansard band; the aerial view uses
the style bible's camera assumptions (30-50 degrees down, long lens). Simple
tabletop lighting, neutral warm background, minimal depth of field, and every image
must depict the same exported model. The night render must show the `_Glow` set
driven from Base Color (see the note at the end of `docs/asset-plans/README.md`).

## Validate the exported GLB

Re-import `earl-warren-building.glb` into a fresh isolated Blender scene and
validate the re-import, not the source scene. Report object count, triangle count,
dimensions, bounding-box min/max, min Z, XY center offset, material names,
image-texture count, camera count, light count, animation count, applied-transform
status, negative-scale status, normal-orientation status, unexpected geometry, and
per-material contract compliance. Render at least one review image from the
re-imported asset. Write `artifacts/earl-warren-building/validation.json` and
`artifacts/earl-warren-building/REPORT.md`.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "earl-warren-building",
  "file": "earl-warren-building.glb",
  "anchor": [
    -122.4178413,
    37.7806865
  ],
  "targetHeightM": 27.0,
  "cat": 18,
  "name": "Earl Warren Building",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a separate, explicitly requested job — run `docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in `docs/asset-plans/earl-warren-building.md`.
````

---

## Part 2 — Research and design dossier

Compiled 13 August 2026 from the sources in 2.2. Values marked *inferred* are visual or
derived estimates, not published figures — the executing agent must re-verify
anything it relies on.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Built | competition 1915, cornerstone 1920, completed 1922 | Wikipedia; Wikidata Q1829495 P1619 = 1922 |
| Architect | Bliss & Faville | Wikipedia, PCAD |
| Renovation | vacated after the 1989 Loma Prieta earthquake; base-isolation retrofit and restoration by Page & Turnbull, reoccupied 1999 | Wikipedia, courthouses.co |
| Style | Beaux-Arts | Wikipedia |
| Materials | grey granite and terra-cotta masonry over a concrete frame | courthouses.co, Wikipedia |
| Storeys | 6 | Wikidata Q1829495 P1101 = 6; OSM `building:levels=5` disagrees (see 2.3) |
| Height to roof | **87 ft = 26.52 m** | Wikipedia infobox |
| Occupant | Supreme Court of California (Q2629503); also 1st District Court of Appeal and the Judicial Council | Wikidata P466 |
| Named for | Earl Warren (Q311197), 30th Governor of California, 14th Chief Justice of the United States | Wikidata P138 |
| Complex | part of the Ronald M. George State Office Complex with the Hiram W. Johnson State Office Building | Wikipedia, DGS |
| Footprint (polygon) | 2,968 m2 | OSM way/260137839, reprojected + shoelace (measured) |
| Footprint (oriented box) | 115.49 x 31.52 m | min-area OBB over the OSM polygon (measured) |
| Long-axis bearing | 81.33 deg (8.67 deg north of due east) | derived from the OBB (measured) |
| OBB centre | −122.4178413, 37.7806865 | derived (measured) |
| Main roof plane above grade | **25.11 m** | DataSF Building Footprints `hgt_median_m`, record `mblr=SF0765002`, `area_id=671` (2010 LiDAR, measured) |
| LiDAR footprint area | 3,019 m2 | same record — within 2% of the OSM polygon, confirming it is the right building |
| Site grade NAVD88 | 17.85 m minimum | DataSF `gnd_min_m` |
| South front | three large arches at the centre with recessed porch and entrances | courthouses.co |
| Second storey | arched windows | courthouses.co |
| Fourth storey | recessed, smaller fenestration; Supreme Court courtroom with a 30 ft skylight | courthouses.co, Wikipedia |

### 2.2 Sources

- https://www.openstreetmap.org/way/260137839 — footprint geometry, `height=27`, `building:levels=5`, wikidata link
- https://api.openstreetmap.org/api/0.6/way/260137839/full.json — the 18-node polygon actually measured here
- https://www.wikidata.org/wiki/Q1829495 — Earl Warren Building: 1922, 6 floors, occupant Supreme Court of California, named after Earl Warren
- https://en.wikipedia.org/wiki/Earl_Warren_Building — 87 ft to roof, 6 storeys, granite and terra-cotta, Bliss & Faville + Page & Turnbull, Loma Prieta vacancy and 1999 return, Ronald M. George complex
- https://courthouses.co/us-states/states-a-g/california/district-court-of-appeal-san-francisco/ — six-storey grey granite and concrete, three centre arches with recessed porch, second-storey arched windows, recessed fourth floor, 30 ft courtroom skylight
- https://data.sfgov.org/resource/ynuv-fyni.json (`mblr=SF0765002`, `area_id=671`) — 2010 LiDAR: `hgt_median_m` 25.11, `hgt_maxcm` 4639, `gnd_min_m` 17.85, polygon area 3,019 m2
- https://www.dgs.ca.gov/RESD/Resources/List-of-DGS-Managed-Office-Buildings/Page-Content/List-of-DGS-Office-Buildings/Balance-of-the-State/Earl-Warren-Hiram-W-Johnson-Building — DGS lists the two buildings as one complex, which is the origin of the 455 Golden Gate Avenue mix-up
- https://www.loc.gov/pictures/item/ca2183/ — HABS "California State Building, 350 McAllister Street" documentation set
- https://commons.wikimedia.org/wiki/File:Earl_Warren_Building_(San_Francisco).JPG — the full south elevation from Civic Center Plaza; the arcade, the cornice, the entrance group, and the Johnson slab behind it
- https://commons.wikimedia.org/wiki/File:The_Earl_Warren_Building_and_Courthouse.jpg — close oblique of the entrance arches: carved archivolts, keystone cartouches, bracket lanterns, diagonal flagpoles, rusticated ashlar
- Esri World Imagery nadir tiles at z19 over the block — roof layout: two turquoise light-court skylights, central lantern with twin laylights, south mansard band

### 2.3 The height (read this before modelling)

Three independent figures agree, which is rare in this repo:

- Wikipedia infobox: **87 ft = 26.52 m** to roof
- OSM `height=27`
- DataSF 2010 LiDAR `hgt_median_m` = **25.11 m** — the main roof plane, which sits
  below the parapet by roughly the height of a parapet

Take **27.0 m as the parapet crest** (`targetHeightM`) and **25.1 m as the roof
deck**. The 1.9 m difference is the attic parapet, and it reconciles all three
sources.

Two traps in the same records:

- The same LiDAR row carries `hgt_maxcm` = 4639, i.e. **46.39 m**. Do not use it.
  Nothing in the nadir aerial is 19 m above the roof deck; the Earl Warren polygon
  shares a wall with the 60 m Hiram W. Johnson record (`mblr=SF0765003`,
  `hgt_median_m` 53.61) and a 0.5 m LiDAR cell on that boundary picks up the tower.
  A single-cell maximum at a shared party wall is the least reliable number in the
  dataset. *Inferred*, but strongly: the aerial shows a flat roof.
- OSM says `building:levels=5`, Wikidata says 6 floors, and the architectural
  sources describe a fourth-floor courtroom under a recessed fifth and an attic.
  Six is right. It does not change the massing — the arcade reads as one
  double-height order regardless of how many floors sit behind it.

### 2.4 Orientation and placement

The building occupies the southern band of the block bounded by McAllister (south),
Polk (west), Golden Gate Avenue (north) and Larkin (east). The Hiram W. Johnson
building fills the northern band; the two are separated by a narrow service gap.
The long axis runs at bearing 81.33 deg — the Civic Center grid, 8.67 deg
counter-clockwise from due east, essentially the same rotation as the Asian Art
Museum's 81.68 deg one block east. In Blender that is a +8.67 deg rotation about Z
from an axis-aligned box, with `+Y` = true north.

The ceremonial front faces **south** onto McAllister Street and, across it, Civic
Center Plaza and City Hall. This is the one landmark in the set where the contract's
"front faces −Y" and real-world orientation agree.

Anchor on the OBB centre. The OSM polygon has deep light-court notches cut into its
north edge, so its centroid sits inside the mass the model actually centres on but
biased south; the OBB centre is the right anchor for a slab of this shape.

### 2.5 What each side shows

**South (McAllister Street) — the hero elevation.** Reading the plaza photograph
bottom to top: a low granite plinth; a rusticated ashlar ground storey carrying
small rectangular windows, interrupted at the centre by **three tall arched
portals** with deeply carved archivolts, keystone cartouches, rosette soffits and
paired bracket lanterns in patinated bronze; a low second storey of small square
windows above a string course; then the building's whole identity — a **giant arcade
of tall round-arched window bays** running unbroken end to end, each arch springing
from a flat pilaster strip, each with a keystone medallion, a balustraded sill and
small square spandrel windows; above it an architrave, a heavy **modillion cornice**
that is the strongest silhouette line on the building; then a light **attic storey**
of small square windows, slightly inset; then a plain parapet cap. Three flagpoles
project diagonally from the facade at arcade level. Behind and above it all, the
white curved slab of the Johnson building — not part of this asset.

**East (Larkin Street) and west (Polk Street).** The short 31 m ends. Same base,
cornice, attic and parapet wrapping the corner; the arcade continues as a shortened
three-or-four-bay version. Quieter, no entrances of consequence.

**North (Golden Gate Avenue side).** Faces the service gap and the Johnson building,
not a street. Plainest elevation: the same horizontal banding with plain rectangular
windows instead of arches, and the two light-court notches cut into it.

**Top.** From the nadir aerial, south to north: a broad **dark sloping mansard band**
about a third of the depth along the McAllister edge, with small vent dormers; a pale
parapet walkway; then a mid-grey flat roof deck carrying, symmetrically, **two large
turquoise glazed light-court skylights** — the glazed-over light courts, the
brightest thing on the roof by a wide margin; between them a **raised central lantern
block** with **twin square ornamental laylights** (the Supreme Court and Court of
Appeal courtroom skylights, the 30 ft one among them); and a scatter of low grey
mechanical boxes and a stair penthouse along the north edge.

### 2.6 Recognition cues (ranked)

1. The unbroken giant arcade of round-arched bays along a 115 m front — no other
   building in Civic Center does this
2. The extreme proportion: four times as long as it is tall, a low bar sitting at
   the foot of the much taller white Johnson slab
3. The three carved entrance arches at the centre of the south front
4. From above: two turquoise light-court skylights flanking a raised central
   courtroom lantern, with a dark mansard band along McAllister
5. The heavy modillion cornice and pale attic that cap the whole length

### 2.7 Miniature translation

**Preserve**

- The 115 x 31 x 27 m proportion and the 8.67 deg grid rotation
- The arcade as one continuous rhythm, unbroken corner to corner — if it breaks,
  the building stops being recognizable
- The cornice as a single hard silhouette line running the full length
- The roof's symmetry: two bright skylights about a raised centre

**Simplify / exaggerate**

- ~19 arcade bays on the south, chunky and deep-recessed, with the arch heads read
  as simple half-cylinder cuts, not mouldings
- The three entrance arches semantically enlarged — taller and deeper than scale
  demands, because they are the building's face and are 4 pixels tall otherwise
- All carving (archivolts, cartouches, rosettes, modillions) collapses into three
  horizontal `Toy_trim` bands: string course, cornice, parapet cap
- The bracket lanterns become six small gold pucks; the flagpoles become three
  thin diagonal cylinders with no flags
- Rooftop clutter becomes: two skylight panels, one lantern block with two
  laylights, one mansard band, four mechanical boxes, one stair penthouse

### 2.8 Massing recipe

Build order for the deterministic script; author axis-aligned (X along the 115.5 m
length, +Y north) then rotate the whole assembly +8.67 deg about Z. Dimensions are
the starting point, not a straitjacket — adjust after the first aerial review render.

1. Plinth: 115.5 x 31.5 m, z=0 to z=1.0, `Toy_stone`, projecting 0.35 m.
2. Rusticated base storey: 115.5 x 31.5, z=1.0 to z=7.2, `Toy_stone`, four deep
   horizontal grooves, small `Toy_glass` window slots on all four faces.
3. String course: `Toy_trim` band z=7.2 to z=8.0, projecting 0.5 m.
4. Second storey: z=8.0 to z=10.4, `Toy_cream`, a band of small square `Toy_glass`
   windows on all four faces; `Toy_trim` sill/balustrade band z=10.4 to z=11.0.
5. Arcade body: z=11.0 to z=20.0, `Toy_cream`. South face: 19 bays at 5.6 m pitch,
   each a 3.4 m wide `Toy_glass` recess 0.5 m deep with a semicircular head at
   z=16.6 (radius 1.7 m), separated by flat pilaster strips; small square
   `Toy_glass` spandrel windows between the arch heads. East and west faces: 4 bays
   each, same rhythm. North face: the same pitch as flat rectangular slots, no arches.
6. Entablature: `Toy_trim` z=20.0 to z=22.6, projecting 1.0 m — the continuous
   cornice, the strongest silhouette line on the model.
7. Attic storey: `Toy_cream` z=22.6 to z=25.4, inset 0.5 m from the body face,
   small square `Toy_glass` windows at 5.6 m pitch.
8. Parapet cap: `Toy_trim` z=25.4 to z=27.0, inset 1.3 m, 1.2 m thick — a hollow
   ring, so the roof deck is visible inside it.
9. Roof deck at z=25.4, `Toy_roofd`, spanning inside the parapet.
10. Mansard band: along the south edge only, 10 m deep in plan, from z=25.4 at the
    inner edge rising to z=26.6 at the parapet, `Toy_roofd`, with four small
    `Toy_trim` vent dormers.
11. Light-court skylights: two `Toy_teal` panels, each 26 x 9 m, centred at
    x = ±31 m, y = +4 m, top at z=26.3, on 0.5 m `Toy_trim` curbs.
12. Central lantern: `Toy_cream` block 18 x 14 m at x=0, y=+2, z=25.4 to z=26.6,
    carrying two 5.5 x 5.5 m `Toy_white_Glow` laylights capped at z=27.0.
13. Mechanical: four `Toy_roofd` boxes 3 x 3 x 1.6 m and one 8 x 4 x 2.4 m stair
    penthouse along the north edge.
14. Entrance group: three arched portals in the south base, centred at x = −4 m,
    9.0 m tall, 5.0 m wide, 1.4 m deep recesses with `Toy_gold_Glow` soffits;
    a three-tread `Toy_stone` step block 24 m wide in front; six `Toy_gold_Glow`
    lantern pucks flanking them.
15. Flagpoles: three `Toy_trim` cylinders radius 0.18 m, 9 m long, springing from
    z=18 on the south face at 30 deg above horizontal.
16. Bevel 0.12 m, 2 segments.

### 2.9 Materials and palette

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_cream` | `#f2ede3` | main granite walls, attic, central lantern |
| `Toy_stone` | `#d9d2c2` | plinth, rusticated base storey, entrance steps |
| `Toy_trim` | `#f3efe6` | string course, cornice, parapet cap, skylight curbs, dormers, flagpoles |
| `Toy_glass` | `#2a4d73` | arcade recesses, base and attic windows |
| `Toy_roofd` | `#45454a` | roof deck, mansard band, mechanical boxes, stair penthouse |
| `Toy_teal` | `#3fa8a0` | the two glazed light-court skylights |
| `Toy_gold_Glow` | `#caa64a` | the three entrance arch soffits and the six lantern pucks |
| `Toy_white_Glow` | `#f7f4ec` | the twin courtroom laylights on the roof lantern |

Night glow: hero = the three entrance arches, the one thing that is genuinely lit
at night on this facade; supporting = the courtroom laylights, which is both true
and the only glow the app's aerial camera sees. Two glow surfaces, nothing else —
the arcade windows stay dark, or a 115 m wall of lit windows will out-shout City
Hall two blocks away. Their day colors (`caa64a` gold, `f7f4ec` white) are palette
neighbours, so the daylight asset stays calm.

### 2.10 Top surface

115 x 31 m of roof under a camera that looks down. The design is the real one,
compressed: dark mansard band south, pale parapet ring, mid-grey deck, two
turquoise skylights flanking a raised pale lantern. The turquoise is the only
saturated colour on the asset and it is doing real work — it is what makes this
building identifiable from the app's default altitude, where the arcade has
dissolved into texture. Do not desaturate it toward grey "for realism"; the aerial
imagery genuinely reads that colour.

### 2.11 Scope

**In the GLB:** plinth, rusticated base, entrance arches, porch and steps, arcade,
cornice, attic, parapet, roof deck, mansard band, skylights, courtroom lantern,
mechanical boxes, stair penthouse, lantern pucks, flagpoles

**Not in the GLB:** the Hiram W. Johnson State Office Building, the Civic Center
Plaza Garage entrance kiosk in front of the south facade, Civic Center Plaza, City
Hall, McAllister / Polk / Larkin / Golden Gate streets, street trees, people,
vehicles, plinths, cameras or lights

### 2.12 Triangle budget

Cap 22,000. Suggested split: body, base rustication and banding ~5k; the 19-bay
south arcade with its arch heads ~7k; east/west/north rhythms ~3k; cornice, attic
and parapet ~2k; roof deck, mansard, skylights, lantern and mechanical ~3k;
entrance group, steps, lanterns and flagpoles ~2k.

### 2.13 Draft manifest entry

```json
{
  "id": "earl-warren-building",
  "file": "earl-warren-building.glb",
  "anchor": [
    -122.4178413,
    37.7806865
  ],
  "targetHeightM": 27.0,
  "cat": 18,
  "name": "Earl Warren Building",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

`dims` and `tris` are placeholders until the asset is built and validated.
`loadRadius` is the default rule `max(2500, 27.0 x 30)` = 2500.

### 2.14 Integration notes (for later, not this task)

- **New landmark (Case B).** Add a `pipeline/lib/landmarks.mjs` entry
  (`id: 'earl-warren-building'`, lon/lat as above, height 27.0, an exclusion radius
  sized from neighbour *vertices*, not centroids) **and re-bake the affected tiles**,
  or the baked procedural building will intersect the GLB.
- **The exclusion radius is the risky number here.** The OBB half-diagonal is 59.7 m,
  but a 60 m circle centred on this building reaches ~30 m into the Hiram W. Johnson
  footprint to the north and would delete a 54 m procedural slab that should stay.
  Size it against the real bake input and check the Johnson building survives.
- Civic Center is dense with landmarks already integrated (`city-hall`,
  `opera-house`, `asian-art-museum`, `civic-center-courthouse`) and more in flight.
  If other landmarks are being built alongside this one, run stage 5 in **batch
  mode** — commit source only and let `docs/asset-pipeline/BATCH-INTEGRATE.md` bake
  the city once.
- Manifest id `earl-warren-building` maps to `earlWarrenBuilding` under the
  registry's camel conversion — confirm against `app/src/landmarks.js` before wiring.

### 2.15 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Bbox Z normalised to 27.00 m exactly, so the loader's scale lands at 1.0
- [ ] Dimensions plausible in meters and consistent with 2.1
- [ ] Triangles at or under 22,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the entrance arches/lanterns and the courtroom laylights
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (per-object signed
      volume authoritative; ray test residual <= 0.15%)
- [ ] No foreign/leaked geometry from other Blender scenes — and specifically no
      trace of the Hiram W. Johnson building
- [ ] Seven review renders + night render + contact sheet regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.16 Open questions and risks

- **The wrong-building risk is the big one.** "455 Golden Gate Avenue" resolves in
  OSM to the Hiram W. Johnson State Office Building, and every photograph of the
  Earl Warren Building's south front has the Johnson slab looming behind it. Anyone
  working from the address rather than the name will build a 54 m curved white tower.
- The 46.39 m LiDAR `hgt_max` is the second trap; 2.3 explains why it is rejected.
  The rejection is *inferred* from nadir imagery and deserves one oblique-aerial check.
- The arcade bay count (19 on the south, 4 on each end) was read off a single
  plaza photograph, not drawings — *inferred*, chosen for rhythm at 5.6 m pitch
  rather than counted authoritatively. The HABS set at the Library of Congress
  should settle it if the executing agent wants certainty.
- The mansard band's depth and the exact lantern height come from a nadir aerial
  where verticals are foreshortened to nothing — both *estimated*.
- This building sits 200 m from City Hall's gilded dome and 120 m from the Asian Art
  Museum. It is long, pale and low, and its job in the skyline is to be the calm
  base the dome rises out of. If it reads as loud in the aerial render, take
  saturation out of everything except the roof skylights.
</content>
</invoke>
