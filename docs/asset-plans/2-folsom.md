# 2 Folsom Street (Gap Inc. headquarters / 250 Embarcadero) — SF-SIM asset plan

Robert A.M. Stern's 2001 headquarters for Gap Inc., filling a whole 6,341 m2 block at the
foot of Folsom Street on the Embarcadero waterfront. A **six-storey brick-and-limestone
base** covering the entire site, a **red-brick superstructure** set back from the water,
and a **limestone tower** stepping up out of it to a crenellated crown at **88 m** — the
tallest bespoke landmark yet planned outside the true skyline pieces, and the fifth
tallest entry in the manifest after Salesforce, Transamerica, 555 California and the
Golden Gate.

It is a three-mass problem, and that is the whole brief. Every other SoMa landmark in this
set is one box with a parapet. This one only reads correctly if the aerial camera sees
**base → brick block → limestone tower**, stepping back and up toward the harbour, with
the seven-storey glass atrium skylight and the Olin roof gardens sitting on the base roof
beside it. Flatten it into a single extrusion and you have deleted the building.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/2-folsom/`. This document is the plan only: Part 1 is the runnable task prompt,
Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `2-folsom` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.390975, 37.790787` |
| Target height | **88.0 m** to the limestone crown; superstructure roof deck 72.1 m (measured); base roof / 7th-floor terrace 32.3 m (measured) |
| Footprint | 84.32 m (Folsom / northwest axis) x 77.15 m (Embarcadero / Spear axis); 6,341 m2, measured |
| Triangle cap | 24,000 |
| Category | `3` (office) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 2 Folsom Street GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of 2 Folsom Street (the Gap Inc. headquarters,
also addressed 250 Embarcadero) in San Francisco and deliver it as a downloadable,
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
7. `artifacts/501-second/` — the closest precedent for a LARGE multi-storey block with a
   tripartite composition and a roof penthouse; reuse its footprint, bay, opening,
   cornice-ring and roof helpers rather than reinventing them
8. `artifacts/chase-center/` and `artifacts/salesforce-tower/` — the only two references in
   the set for an asset whose silhouette is a stack of distinct masses rather than one
   extrusion; check how they spend triangles on the transitions
9. `docs/asset-plans/2-folsom.md` — this plan, whose dossier is your research starting
   point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract, `AGENTS.md`
governs repository and integration rules. Do not invent a new style and do not copy
visual instructions from unrelated prompts.

## Must capture

- The **three-mass stack**, which is the entire identity:
  1. a **six-storey base** covering the whole 84.32 x 77.15 m block, red brick with
     limestone piers and banding, topped at **32.3 m** by a wide planted roof terrace
     (the 7th-floor cafeteria plaza) behind a limestone parapet;
  2. a **red-brick superstructure block**, roughly 42 x 42 m, **set back about 16 m from
     the block centre toward Spear Street** so it stands away from the Embarcadero, roof
     deck at **72.1 m**;
  3. a **limestone tower** rising out of the superstructure's **northeast** corner —
     the harbour-facing corner — stepping back twice to a **crenellated crown at 88.0 m**.
- The **material split**: red brick for the base and the superstructure, pale tawny
  limestone for the tower, the piers, the frames, the cornices and the parapets. Two
  materials, read at a glance from a kilometre up. Never all-brick, never all-stone.
- The **glass atrium skylight** on the base roof in the **northeast quadrant**: a broad
  gridded panel of translucent laminated glazing over the seven-storey atrium. It is the
  single strongest thing on the roof plane and the camera looks down.
- The **Olin roof gardens** on the base terrace: two lawn-and-water parterres toward the
  north and east corners, and rows of clipped hedge parterres along the southwest and
  southeast terraces. Geometric, low, manicured.
- **Four public elevations.** The block is free-standing on at least three sides:
  northeast to The Embarcadero (77.15 m, the harbour elevation and the atrium entrance),
  southeast to Folsom Street (84.32 m, the mid-block atrium entrance), southwest to Spear
  Street (77.15 m), northwest (84.32 m) toward the 201 Spear / One Steuart Lane block.
  None of them may be a blank wall.
- The **porticoes**: RAMSA's "multiple porticoes of columns and lintels at the tower and
  the building's entrances", boldest on the harbour side. This is the ornament the budget
  is for.

## Research 2 Folsom Street independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the three roof levels, the footprint, the WGS84 anchor, and the
real-world orientation, and gather references covering:

- All four elevations. The building has no party wall — a model built from the Embarcadero
  photograph alone will have three invented 80 m walls
- Aerial and roof views — the atrium skylight, the two roof gardens, the hedge parterres,
  the tower deck's mechanical plant, and the crown
- The setback pattern of the limestone tower: how many steps, at what levels
- Ground-level views day and night, including the four Gap-brand retail stores added to
  the ground floor in 2022
- The storey count and the floor-to-floor height — the weakest derived numbers here (2.15)

Prefer architect/engineer publications, owner or institutional material, planning and
permitting documents, architectural press, geolocated photography, and aerial/satellite
imagery. Never rely on a single photograph, a single AI-generated image, or a single
unsourced 3D model. Separate verified facts from visual inference; if sources disagree,
document the disagreement and decide.

**Three source conflicts are already known and resolved in 2.1 — re-check them, do not
silently re-inherit the wrong value:** RAMSA's own text reads "a six story base with a
fifteen story superstructure", which is **15 storeys in total**, not 6 + 15 — Gap Inc.'s
2022 press release says "15 floors" outright; SkyscraperPage lists **275 ft / 14 floors**
as *unconfirmed* and it is a mid-crown figure, neither the 72.1 m deck nor the 88.0 m
crown; and OSM tags `height=91` against a LiDAR maximum of **87.95 m** — 88.0 m is the
measured value and is what this asset normalizes to.

## Create a reference dossier

Write `artifacts/2-folsom/REFERENCE.md` containing: source links and what each
establishes; verified dimensions and location; orientation; observations from all four
sides and above; the 3-5 strongest recognition cues; features to preserve; features to
simplify; uncertainties and conflicting evidence. A contact sheet of attributed reference
thumbnails is welcome if legally permissible — do not commit copyrighted full-resolution
imagery.

## Make your own design decisions

Follow the conversion process in `docs/styles/miniature-toy.md` §22: identify the
recognition cues, strip nonessential information, rebuild the massing from a few confident
volumes, exaggerate only the signature features, simplify the facade into broad rhythms,
deliberately design every surface visible from above, evaluate from the app's high
three-quarter aerial camera, then simplify again.

This is a **hero-tier** asset by the style bible's §21 test: 88 m on a whole city block,
on the waterfront, visible from every approach. Spend the triangles on the **three mass
transitions** — base parapet, superstructure setback, tower steps — on the **crown**, and
on the **roof plane** (skylight, gardens, parterres). Spend nothing on individual window
muntins, the brick coursing, the storefront mullions or the balustrade balusters; at city
scale they are sub-pixel and they will eat the budget the transitions need.

The finished asset must be immediately recognizable as 2 Folsom Street, consistent with
the real building from all four sides and above, architecturally credible, and a premium
handcrafted miniature — not photorealistic, not voxel art, not generic low-poly, and never
accurate in one view while invented in the others.

## Scope of the exported asset

Export the single 2001 building: four elevations, the base parapet and roof terrace with
its skylight and gardens, the superstructure, the limestone tower and its crown, and the
rooftop plant.

Do not include unrelated surrounding city geometry: The Embarcadero, Folsom Street, Spear
Street, Rincon Park, the Muni/historic streetcar tracks, the neighbours at 201 Spear, One
Steuart Lane or Hills Plaza, street trees, the sidewalk, parked cars, people, plinths,
cameras or lights. Temporary context may appear in review renders but must not leak into
the GLB.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary `.glb`;
real-world meters; origin at base center; minimum geometry Z ~ 0; applied transforms; no
negative scales; outward normals; no duplicate or foreign geometry; no image textures; no
transparency; flat-color materials named `Toy_*` from the project palette; `_Glow` suffix
only on surfaces that glow at night; no `Toy_body`; no cameras, lights, animations,
armatures or constraints; no external dependencies; at most 24,000 triangles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model drops
into the city at its real-world heading — the loader applies no rotation (`placeGeneric`
in `app/src/assets.js` only scales and positions). The Embarcadero elevation faces
**northeast, bearing 45.2°**; Folsom Street faces **southeast, 135.2°**; Spear Street
faces **southwest, 225.2°**; the northwest elevation faces **315.2°**. The building is
rotated about 45° off the world axes, so build directly on the measured footprint
rectangle in 2.3 rather than modelling an axis-aligned box and rotating it.

**Height normalization:** the tallest geometry in the export (the limestone crown) must
land at exactly **88.0 m** so the loader's `targetHeightM / measuredHeight` scale is 1.0.

## Reproducible Blender workflow

Blender 5.2 LTS. Headless: `blender -b --python script.py -- args`.

Keep `artifacts/2-folsom/build_2_folsom.py` (deterministic build script),
`artifacts/2-folsom/2-folsom.blend`, and `artifacts/2-folsom/2-folsom.glb`. The script
must rebuild the model reliably enough for future revision. Do not modify or rename an
unrelated existing GLB to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras: `2-folsom-top.png`,
`2-folsom-north.png`, `2-folsom-east.png`, `2-folsom-south.png`, `2-folsom-west.png`, plus
`2-folsom-contact-sheet.png`, at least one high three-quarter aerial beauty render
`2-folsom-aerial.png`, and a night render `2-folsom-aerial-night.png`.

The four elevations must share scale, framing, lighting, exposure and projection; use
orthographic or long-lens cameras; label directions from the researched orientation; the
top view must clearly show the base parapet ring, the atrium skylight, both roof gardens,
the hedge parterres, the superstructure deck and the crown; the aerial view uses the style
bible's camera assumptions (30-50 degrees down, long lens), from the **northeast** so that
the harbour elevation and the tower's step-up are seen together.

Note that the axis-aligned elevation renders will each show the building at 45°. That is
the expected consequence of the real heading, not a camera error.

## Validate the exported GLB

Re-import `2-folsom.glb` into a fresh isolated Blender scene and validate the re-import,
not the source scene. Report object count, triangle count, dimensions, bounding-box
min/max, min Z, XY center offset, material names, image-texture count, camera count, light
count, animation count, applied-transform status, negative-scale status,
normal-orientation status, unexpected geometry, and per-material contract compliance.
Render at least one review image from the re-imported asset. Write
`artifacts/2-folsom/validation.json` and `artifacts/2-folsom/REPORT.md`.

Note that the axis-aligned XY bounding box will be roughly **114.2 x 114.2 m** even though
the building is 84.32 x 77.15 m — that is the expected consequence of a ~45° real-world
heading, not a scale error.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this draft
entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "2-folsom",
  "file": "2-folsom.glb",
  "anchor": [
    -122.390975,
    37.790787
  ],
  "targetHeightM": 88.0,
  "cat": 3,
  "name": "2 Folsom Street (Gap Inc. headquarters)",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2640
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a separate, explicitly requested job — run `docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in `docs/asset-plans/2-folsom.md`.
````

---

## Part 2 — Research and design dossier

Compiled 19 August 2026 from the sources in 2.2. Values marked *inferred* or *estimated*
are visual or derived, not published figures — the executing agent must re-verify anything
it relies on.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Names | **2 Folsom Street**; also **250 Embarcadero**; "the Gap Building"; Gap Inc. global headquarters | RAMSA; Kriebel & Associates project profile; Gap Inc. press release 2022 |
| Design architect | **Robert A.M. Stern Architects** (partners Robert A.M. Stern, Graham S. Wyatt, Michael D. Jones) | ramsa.com project page |
| Architect of record | **Gensler**; lobby/atrium documentation by Powell & Partners; MEP by CB Engineers; core & shell by Swinerton | Kriebel; powellarchs.com; cbengineers.com |
| Landscape (roof gardens) | **The Olin Partnership**, in association with RAMSA | ramsa.com |
| Completed | **2001** | RAMSA, Kriebel, CB Engineers, Powell — four independent sources |
| Storeys | **15** | Gap Inc. press release, June 2022: "2 Folsom boasts 15 floors of flexible, creative office space". RAMSA's "six story base with a fifteen story superstructure" is the same 15, not 21 (see 2.15) |
| Building area | 540,000 sq ft (CB Engineers) / 545,000 sq ft (SF Business Times) / 583,000-600,000 sq ft gross incl. two parking levels (Engent, Kriebel) | the spread is rentable vs gross vs garage |
| Structure / cladding | Structural steel; **precast panel exterior with brick and limestone**; tawny French limestone and red brick | Kriebel; RAMSA |
| Footprint | 6,341 m2; **84.32 m x 77.15 m** OBB, 97.5% rectangular fill | DataSF LiDAR footprint `201006.0000175` OBB — **measured**; OSM way 93817368 independently gives 84.49 x 77.32 m and 6,344 m2, a 0.2% agreement |
| Cell count check | 25,463 LiDAR cells at 50 cm = 6,366 m2 | DataSF `hgt_cells50cm` — agrees with the polygon area to 0.4% |
| Base roof / 7th-floor terrace | **32.28 m** | DataSF LiDAR `hgt_mediancm 3228` over 25,463 cells — **measured**; corroborated by RAMSA's "roof garden... at the sixth floor" and the "7th floor cafeteria opens to an extensive outdoor plaza" |
| Superstructure roof deck | **72.11 m** | DataSF LiDAR `hgt_majoritycm 7211` (the modal plane — a large dead-flat deck) — **measured** |
| Crown / architectural top | **87.95 m** | DataSF LiDAR `hgt_maxcm 8795`; `peak_1st_m 91.55` less `gnd_mean 3.60` reproduces it exactly. OSM tags `height=91`. Rounded to **88.0 m** for the manifest — **measured** |
| Level areas | base 70.6%, superstructure 23.1% (1,467 m2), crown 6.3% (402 m2) | three-level decomposition of the LiDAR mean/median/mode/sigma — **derived**, see 2.15 |
| Ground elevation | 3.32 m NAVD88 (`gnd_min_m`), 3.60 m mean, sigma 0.07 m | DataSF LiDAR — a dead-flat reclaimed waterfront site; the app's terrain handles this, not the asset |
| Block frontages | The Embarcadero (NE, 77.15 m); Folsom Street (SE, 84.32 m); Spear Street (SW, 77.15 m); northwest lot line (84.32 m) toward 201 Spear / One Steuart Lane | measured from the footprint OBB against OSM street ways |
| Entrances | Two, both into the seven-storey atrium: one **from the Embarcadero** (NE), one **mid-block on Folsom Street** (SE) | RAMSA |
| Atrium | Seven storeys, skylit with **translucent laminated glass**, French-limestone-lined, containing Richard Serra's 60 ft "Charlie Brown" | RAMSA; Kriebel |
| Ground-floor retail | Four Gap-brand "laboratory" stores (Gap, Banana Republic, Athleta, Old Navy), ~18,000 sq ft, opened June 2022 as part of a two-year renovation | Gap Inc. press release; The Real Deal, Feb 2022 |
| Owner / occupant | **Gap Inc.**, owner-occupier | The Real Deal, 2022 ("the company, which owns the 545,000-square-foot building") |

### 2.2 Sources

- https://www.ramsa.com/projects/project/gap-inc-offices — the design intent in the
  architect's own words: the six-storey base, the setback superstructure, "a cubical
  background mass and a slender foreground tower", the tawny French limestone and red
  brick, the porticoes "at its boldest facing the harbor", the seven-storey skylit atrium,
  the sixth-floor Olin roof garden, the two entrances
- http://kriebelandassociates.com/projects05.html — written by Gap's own Senior Director of
  Corporate Architecture & Construction: "250 Embarcadero (also known as 2 Folsom)",
  600,000 sf, structural steel, **precast panel exterior with brick and limestone**, the
  7th-floor cafeteria opening onto the outdoor plaza
- https://www.cbengineers.com/project/gap/ — the MEP engineer: "**15-story**, 540,000
  square foot design", cafeteria, art gallery, two levels of underground parking, outdoor
  decks, exhibition hall, rooftop garden; 10'8" ceilings and underfloor air
- https://www.gapinc.com/en-us/articles/2022/06/gap-inc-welcomes-customers-to-four-new-retail-stor
  — the owner, June 2022: "2 Folsom boasts **15 floors**... a rooftop cafeteria and outdoor
  dining terrace overlooking the Bay, a coffee bar and lounge in the lobby, and a ground
  floor 'Co-Lab'"; the four retail stores
- https://therealdeal.com/san-francisco/2022/02/07/gap-to-open-banana-republic-old-navy-athleta-in-embarcadero-hq/
  — 545,000 sq ft, Gap-owned, 18,000 sq ft of ground-floor retail conversion
- https://skyscraperpage.com/cities/?buildingID=4212 — "Gap Building", 2 Folsom Street,
  R.A.M. Stern, finished 2001, floor count 14, roof **275 ft, marked Unconfirmed**
  (reconciled in 2.15)
- https://www.openstreetmap.org/way/93817368 — `addr:housenumber=2`,
  `addr:street=Folsom Street`, `building=office`, `building:levels=15`, **`height=91`**;
  20-node ring
- https://data.sfgov.org/resource/ynuv-fyni — DataSF Building Footprints (LiDAR-derived),
  record `sf16_bldgid 201006.0000175`, `mblr SF3741035`: 25,463 cells at 50 cm,
  `hgt_median 32.28`, `hgt_majority 72.11`, `hgt_mean 44.98`, `hgt_std 20.01`,
  `hgt_max 87.95`, `gnd_min_m 3.32`, `peak_1st_m 91.55`
- Google Maps satellite (near-nadir, z20, 2026 capture) — the roof: the atrium skylight
  grid, both roof gardens, the hedge parterres, the superstructure deck with its
  mechanical pens and two round fans, the stepped crown, and the setback pattern
- https://commons.wikimedia.org/wiki/File:The_Gap_headquarters.jpg (2010, CC) — the one
  clean elevation photograph found: the brick field with limestone frames, the base
  parapet with its glass railing and hedges, the limestone tower's double setback and its
  crenellated crown pavilion
- OSM `building:part` ways 944981401, 1487162810 and 1487162811 — used only as weak
  corroboration of a stepped crown; their geometry is coarse and their `building:levels`
  disagree with every other source (2.15)

### 2.3 Orientation and placement

The building fills the whole block at the foot of Folsom Street where it meets The
Embarcadero, on made ground at the edge of the bay. Like the whole SoMa grid it is rotated
about 45° from the world axes; its corners point north, east, south and west and its faces
point at the four intercardinals.

DataSF LiDAR and OSM agree to 0.2% on the footprint here. The DataSF OBB is used.

Footprint rectangle, in Blender coordinates (metres, `+X` east, `+Y` north),
already centred on the anchor `-122.390975, 37.790787`:

```
(-57.10,  -2.35)   west corner    — Spear x Folsom end
( -2.72, -57.08)   south corner   — Folsom Street end
( 57.10,   2.35)   east corner    — Embarcadero x Folsom
(  2.72,  57.08)   north corner   — Embarcadero x northwest line
```

Edges, with outward normals:

| Edge | Length | Faces | Elevation |
|---|---|---|---|
| `(2.72,57.08) -> (57.10,2.35)` | 77.15 m | NE 45.2° | **The Embarcadero** — the harbour elevation and an atrium entrance |
| `(57.10,2.35) -> (-2.72,-57.08)` | 84.32 m | SE 135.2° | **Folsom Street** — the address, mid-block atrium entrance |
| `(-2.72,-57.08) -> (-57.10,-2.35)` | 77.15 m | SW 225.2° | **Spear Street** |
| `(-57.10,-2.35) -> (2.72,57.08)` | 84.32 m | NW 315.2° | toward the 201 Spear / One Steuart Lane block |

The real ring has small notched jogs at every corner (the porticoes and service recesses)
which take the polygon from 6,504 m2 of OBB to 6,341 m2 of actual area. Model the jogs as
1.5-2.5 m chamfers/recesses at the four corners; do not model the 20 individual vertices.

Because of the 45.2° heading the axis-aligned bounding box is ~114.2 x 114.2 m for a
building that is 84.32 x 77.15 m. That is correct.

**Mass centres**, in the same Blender frame (derived in 2.7):

| Mass | Plan size | Centre (X, Y) | Top |
|---|---|---|---|
| Base | 84.32 x 77.15 | (0, 0) | 32.3 m |
| Superstructure | ~42 x 42 | (-11.35, -11.28) | 72.1 m |
| Limestone tower / crown | ~20 x 20 | (-2.14, -4.94) | 88.0 m |

The superstructure sits **16 m southwest of the block centre along the footprint's own
axis** — that is RAMSA's "set back from the Embarcadero to minimize shadows on the
waterfront park", and it is measurable in the satellite. The tower then sits at the
superstructure's **northeast** edge, flush with it: "at its boldest facing the harbor".

### 2.4 What each side shows

**Northeast — The Embarcadero (77.15 m).** The harbour elevation and the one the whole
composition is aimed at. Red brick base with limestone piers and a limestone base course;
a portico of columns and lintels at the entrance to the atrium; the base parapet at 32.3 m
with its glass railing and planted edge; then a wide gap of roof terrace before the
superstructure begins, so from the Embarcadero the tower reads as standing *behind* a
garden. The limestone tower's crown is dead ahead over the entrance. This is the elevation
the aerial hero render must show.

**Southeast — Folsom Street (84.32 m).** The address elevation and the longest face. Brick
field with limestone-framed openings in a regular bay rhythm; the **mid-block entrance**
into the atrium under a portico, roughly on the centre of the face; the four Gap-brand
retail fronts along the ground floor (2022). Above the base parapet, the superstructure's
southeast flank rises with the same rhythm, and the terrace runs along in front of it with
the hedge parterres.

**Southwest — Spear Street (77.15 m).** The service-and-back elevation, but still a public
street front: the same brick-and-limestone system, a plainer rhythm, the garage entry, and
the superstructure sitting close to this edge because it is set back from the water. From
Spear the building looks tallest and closest — the mass is over you.

**Northwest (84.32 m).** Faces the 201 Spear / One Steuart Lane block. No party wall: the
block is free-standing, with a service way between (*inferred* from imagery — verify).
Same system as the southwest face, plainest rhythm, and where the roof plant is
concentrated on the base terrace.

**Above.** The most important view in this whole plan, because the camera looks down and
because the base roof is 6,341 m2 of designed surface at 32.3 m — bigger than any complete
building in the SoMa set. Composition, read off the near-nadir satellite:

- the **atrium skylight** in the northeast quadrant: a large gridded translucent-glass
  panel, roughly 30 x 22 m, its cells clearly expressed;
- two **lawn parterres** with reflecting strips (Olin), one toward the north corner beside
  the skylight, one toward the east corner;
- rows of **clipped hedge parterres** in a regular grid along the southeast and southwest
  terraces, with tables between them;
- a wide **paved terrace ring** inside the limestone parapet;
- the **superstructure deck** at 72.1 m: pale membrane, a screened mechanical pen with two
  round fans toward its east side, a stair/lift penthouse toward its southwest, low screens;
- the **crown** at 88.0 m on the northeast corner of the deck: a stepped limestone pavilion.

### 2.5 Recognition cues (ranked)

1. **The three-mass step-up toward the harbour.** Base → brick block → limestone tower,
   each smaller and each shifted, is the building. If the silhouette is one box, nothing
   else matters
2. **Brick body, limestone tower.** The two-material split is what tells the masses apart
   from a kilometre up
3. **The whole-block base with a garden on top.** 6,341 m2 of terrace with a glass roof
   over the atrium — unique on this waterfront
4. **88 m on the Embarcadero.** It is the tall thing between the Ferry Building and Hills
   Plaza; from the water it is a skyline event
5. The crenellated stepped crown, which is the only silhouette that is not a flat parapet

### 2.6 Miniature translation

**Preserve**

- The 84.32 x 77.15 m footprint, the three measured roof levels (32.3 / 72.1 / 88.0) and
  the real 45.2° heading, exactly
- The 16 m southwest setback of the superstructure and the northeast placement of the tower
  — these two offsets carry the architect's whole idea
- The brick / limestone split, unmistakable
- The atrium skylight and both roof gardens as designed roof objects, not clutter
- The porticoes at the two entrances and at the tower, exaggerated rather than lost

**Simplify / exaggerate**

- Cornices, the base parapet and each setback ledge are thickened and their projection
  increased so the three transitions survive at distance. This is where the semantic
  exaggeration is spent
- The regular brick bay becomes one glazed panel per opening in a limestone frame; the
  brick coursing, the mullions and the spandrel detail are dropped
- The crown's crenellation becomes a small number of chunky stepped blocks, not a real
  merlon rhythm
- Hedge parterres become low extruded strips in a grid; individual plants, tables, chairs,
  umbrellas and railings are dropped
- The skylight becomes one raised panel with a coarse grid of ribs — 6 x 5 cells, not the
  real ~11 x 8
- The 2022 retail fronts become a glowing sign band at ground level on the Folsom and
  Embarcadero faces; no lettering is modelled
- Downpipes, louvres, window-washing rigs, the garage door detail and the streetcar poles
  are dropped

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not a
straitjacket — adjust after the first aerial review render. All heights are metres above
the asset's z=0.

1. **Base body**: extrude the 2.3 rectangle (with its four corner chamfers) from z=0 to
   z=31.4, `Toy_brick` walls, cap `Toy_sand` — the terrace paving.
2. **Base course**: 0.15 m proud `Toy_stone` band, z=0 to z=6.4, on all four faces —
   the ground-floor storey, which is limestone-faced in reality.
3. **Base piers**: one 1.4 m `Toy_stone` pier per bay boundary, z=6.4 to z=29.6, projecting
   0.15 m. Bay pitch ~6.5 m: 12 bays on the 84.32 m faces, 11 on the 77.15 m faces
   (*inferred* — see 2.15).
4. **Base openings**: one `Toy_glass` panel per bay per floor at 6.4 + k*4.6
   (k = 0..4), each 3.0 m tall, in a 0.25 m `Toy_stone` frame.
5. **Base cornice**: ring on all four faces, z=29.6 to z=30.6, projecting 0.9 m, `Toy_stone`.
6. **Base parapet**: ring, z=30.6 to **z=32.3**, 0.5 m thick, `Toy_stone` with a
   `Toy_trim` coping. This is the terrace edge.
7. **Terrace deck**: `Toy_sand` plane at z=31.4 inside the parapet.
8. **Atrium skylight**: a raised `Toy_glassl` panel centred about (+22, +16) in the Blender
   frame, ~30 x 22 m, sitting 1.2 m proud of the deck on a `Toy_stone` kerb, ribbed into a
   6 x 5 grid with 0.35 m `Toy_stone` ribs. The one strong positive on the roof plane.
9. **Roof gardens**: two `Toy_mint` lawn panels ~14 x 9 m, 0.25 m proud, one near the north
   corner and one near the east corner, each with a `Toy_glassl` water strip inset.
10. **Hedge parterres**: two banks of 5-6 `Toy_mint` strips, 1.0 m wide x 8 m long x 0.9 m
    tall, laid in a grid on the southeast and southwest terraces.
11. **Superstructure body**: 42 x 42 m box centred at (-11.35, -11.28), z=31.4 to z=70.4,
    `Toy_brick`, with `Toy_stone` corner piers and the same bay/opening system at a 6.5 m
    pitch (6 bays per face).
12. **Superstructure cornice + parapet**: ring z=70.4 to z=71.2 projecting 0.8 m
    (`Toy_stone`), parapet to **z=72.1** with a `Toy_trim` coping; deck `Toy_sand` at z=71.4.
13. **Tower shaft**: ~24 x 24 m `Toy_stone` mass on the superstructure's northeast corner,
    centred at (-2.14, -4.94), rising from z=31.4 (it is a full-height mass, not a cap) to
    z=78.0, with `Toy_stone` piers and `Toy_glass` openings on all four faces.
14. **Tower setback 1**: at z=78.0, step in to ~20 x 20 m; ledge ring `Toy_trim`,
    continue to z=84.0.
15. **Tower setback 2 / crown pavilion**: at z=84.0 step in to ~15 x 15 m, continue to
    z=86.6, with tall `Toy_glassl` openings under `Toy_stone` lintels — the portico motif
    at the top.
16. **Crown crenellation**: eight chunky `Toy_stone` blocks, 2.2 x 2.2 x 1.4 m, on the
    pavilion parapet, tops landing exactly at **z=88.0**. This sets the bounding-box top.
17. **Roof plant** on the superstructure deck: one `Toy_steel` screened pen ~10 x 7 x 2.0 m
    with two `Toy_roofd` cylinders (12 segments) for the fans, one `Toy_steel` stair
    penthouse ~7 x 5 x 3.0 m. Nothing may out-top the crown.
18. **Porticoes**: at the Embarcadero and Folsom entrances, a 9 m wide x 7.5 m tall
    recessed `Toy_ink` opening with four 1.0 m `Toy_stone` columns and a 0.9 m lintel
    projecting 1.5 m.
19. Bevel 0.12 m, 2 segments on the three masses; 0.04/1 on applied panels, piers, cornices
    and parterres.

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_brick` | `#c96f4a` | the base body and the superstructure body — **the identity colour of the two lower masses** |
| `Toy_stone` | `#d9d2c2` | the limestone tower, all piers, frames, cornices, parapets, the base course, the crown | 
| `Toy_trim` | `#f3efe6` | parapet copings and the two tower setback ledges — a half-tone lighter than `Toy_stone` so the transitions read from directly above |
| `Toy_sand` | `#ece4d4` | the base terrace paving and the superstructure roof membrane |
| `Toy_glass` | `#2a4d73` | all facade windows |
| `Toy_glassl` | `#6f95b8` | the atrium skylight, the crown pavilion glazing, the garden water strips |
| `Toy_mint` | `#8fd0a8` | the two roof lawns and the hedge parterres |
| `Toy_steel` | `#9aa0a6` | rooftop plant and screens |
| `Toy_roofd` | `#45454a` | the two round fans only |
| `Toy_ink` | `#3a3530` | the recessed entrance porticoes and the garage opening |
| `Toy_glassl_Glow` | `#6f95b8` | the atrium skylight at night — **the night hero** |
| `Toy_glass_Glow` | `#6f95b8` | scattered lit office windows |
| `Toy_gold_Glow` | `#caa64a` | the ground-floor retail sign band on the Folsom and Embarcadero faces |

**Roof membrane note.** `Toy_sand` on both decks, never `Toy_roofd`. This was settled
empirically on `524-second` and confirmed on `501-second`: `Toy_roofd` measured at
rgb(9,9,12) on a lit deck in the live scene — a black hole from the aerial camera. The two
decks here total 8,200 m2, the largest roof area in the bespoke set. Start pale, keep the
plant dark.

**Night state (required).** Glow surfaces must be thin shells proud of the opaque surface
behind them — the app renders `_Glow` in a separate layer that is roughly 12% alpha per
face by day, so a closed shell reads at ~23% and a primary surface must never be authored
as glow. Hero glow: the **atrium skylight**, lit from the seven-storey atrium below — a
single softly glowing rectangle on a dark roof plane is the whole night identity, and it
is truthful. Supporting: a scatter of lit windows across the base and superstructure (keep
it under about a fifth of the openings — a fully lit block reads as a render), the crown
pavilion's glazing, and the retail sign band at ground level. Do **not** glow the tower's
limestone; the crown reads at night as a dark silhouette above a lit skylight, which is
what the building actually looks like from the Bay Bridge.

### 2.9 Top surface

8,200 m2 across two decks — by a wide margin the largest top surface in the bespoke set,
and the reason this asset cannot be judged from the street. The base terrace must read as a
**designed garden with a glass roof in it**, not as a grey field with clutter: the skylight
is the one strong positive, the two lawns are the one strong colour, the hedge parterres
give the regular grain, and the paved ring frames all of it inside the limestone parapet.
The superstructure deck above is deliberately plainer — pale membrane, dark plant grouped
to the east side — so that the eye goes base garden → tower, which is the order the
architecture wants.

### 2.10 Scope

**In the GLB:** the single 2001 building — base body with its four elevations, base course,
piers, openings, cornice and parapet; the terrace deck with the atrium skylight, both roof
gardens and the hedge parterres; the superstructure with its openings, cornice, parapet and
deck; the limestone tower with both setbacks, the crown pavilion and its crenellation; the
two entrance porticoes; the rooftop plant

**Not in the GLB:** The Embarcadero, Folsom Street, Spear Street, the streetcar tracks and
poles, Rincon Park, 201 Spear, One Steuart Lane, Hills Plaza, street trees, sidewalk,
vehicles, people, plinths, cameras or lights

### 2.11 Triangle budget

Cap 24,000 — the largest in the bespoke set, and justified by 323 m of public elevation
over fifteen storeys plus 8,200 m2 of designed roof. Suggested split: three mass bodies,
cornices and parapets ~4.0k; base piers and openings ~7.5k; superstructure piers and
openings ~4.0k; tower shaft, both setbacks, crown pavilion and crenellation ~3.5k; atrium
skylight ~1.2k; gardens and parterres ~1.8k; porticoes ~0.8k; roof plant ~1.2k.

**The base openings are the risk.** 46 bays x 5 floors is 230 openings before anything
else. If the first build lands over budget, **drop a floor of openings from the northwest
and southwest faces before touching a single mass transition** — the transitions are the
identity and the windows are texture.

### 2.12 Draft manifest entry

```json
{
  "id": "2-folsom",
  "file": "2-folsom.glb",
  "anchor": [
    -122.390975,
    37.790787
  ],
  "targetHeightM": 88.0,
  "cat": 3,
  "name": "2 Folsom Street (Gap Inc. headquarters)",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2640
}
```

`dims` and `tris` are placeholders until the asset is built and validated.
`"estimated": false` because all three roof levels are LiDAR measurements over 25,463 cells
and the crown is independently corroborated by the OSM `height` tag — nothing here is
photogrammetric. `loadRadius` is the default formula's result: `max(2500, 88.0 * 30) = 2640`.

### 2.13 Integration notes (for later, not this task)

- **Case B / new landmark.** Add a `pipeline/lib/landmarks.mjs` entry (`id: '2Folsom'`) and
  re-bake the affected tiles, or the baked procedural building on this footprint will
  intersect the GLB. The procedural block here is driven by the same 87.95 m LiDAR figure,
  so it is roughly as tall as the asset — an unbaked check will look fine and be wrong.
- **Exclusion radius.** Size it from the bake input's ring **vertices**, not centroids, and
  measure it against the real `pipeline/data/overture_buildings.geojsonseq`. The footprint
  half-diagonal is 57.14 m, which is large; the block is street-bounded on at least three
  sides, so the risk edge is the **northwest** line toward 201 Spear. Do the measurement;
  do not assume the streets protect you.
- `loadRadius`: 2640 m from the default formula. Not `alwaysLoaded` — 88 m is well below
  skyline scale and the shared batch is the scarce resource.
- **Batch reserve.** At 24,000 triangles this is one of the heaviest single entries in the
  shared landmark `BatchedMesh`. Check the reserve headroom before integrating (see the
  batch-reserve notes in `docs/asset-pipeline/BATCH-INTEGRATE.md`); a landmark that
  overflows the buffer silently evicts a different one on every reload.
- **Judge it against `ferry-building`**, 700 m northwest along the same waterfront, and
  against the procedural Hills Plaza block to the south. RAMSA designed this building to
  take its cue from the Ferry Building and to complete Hills Plaza's step-up; if that
  three-way relationship does not read from the Bay-side aerial, the massing has failed
  even if every dimension is right.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Bounding-box top exactly 88.0 m (loader scale lands at 1.0)
- [ ] Dimensions plausible in meters and consistent with 2.1 (XY bbox ~114.2 x 114.2 m is expected)
- [ ] Footprint proportion preserved: the base must measure 84.32 x 77.15 m along its own axes
- [ ] Base parapet lands at 32.3 m; superstructure parapet at 72.1 m; both read from directly above
- [ ] The superstructure is visibly offset southwest and the tower visibly offset northeast
- [ ] Triangles at or under 24,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the skylight, the scattered windows, the crown glazing and the retail band; glow shells proud of the opaque surface, never closed shells around a primary mass
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (per-object signed volume for the union of solids; ray test residual <= 0.15%)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + contact sheet + night render regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

- **"A six story base with a fifteen story superstructure" is 15 storeys, not 21.** RAMSA's
  sentence is the single most misreadable fact about this building. Gap Inc.'s own 2022
  press release ("15 floors"), CB Engineers ("15-story"), and the OSM tag
  (`building:levels=15`) all agree on fifteen total. The arithmetic agrees too: the base
  roof is measured at 32.28 m, which is seven levels at 4.6 m — exactly the floor-to-floor
  a 10'8" ceiling plus an underfloor air plenum plus structure produces — and the 72.11 m
  deck is a further 8.6 such levels. **An agent that builds 21 storeys will be 40 m too
  tall and will have to invent the difference.**
- **SkyscraperPage's 275 ft / 14 floors is not the number to use.** It is flagged
  *Unconfirmed* on its own page, 83.8 m sits between the 72.1 m deck and the 88.0 m crown,
  and 14 floors contradicts four independent sources. It is most likely a mid-crown
  estimate off a drawing. Recorded here only so nobody re-imports it.
- **The three level areas are derived, not measured directly.** DataSF gives one summary
  row for the whole footprint, so the split was solved from it: with the base plane fixed at
  the median (32.28 m) and the two upper planes at the mode (72.11 m) and the maximum
  (87.95 m), the published mean (44.98 m) and standard deviation (20.01 m) determine the
  three area fractions uniquely — 70.6% / 23.1% / 6.3%, i.e. 1,467 m2 of superstructure and
  402 m2 of crown. Those numbers then agree independently with the near-nadir satellite
  (a ~42 m deck and a ~20 m crown, after correcting the image for a measured 1.98 px/m
  building lean) and with the two small OSM `building:part` rings (197 m2 and 103 m2 at the
  crown). Three methods, none tuned to the others. **Still: the 42 x 42 m superstructure and
  the 20 x 20 m crown are the least certain dimensions in this plan.**
- **`hgt_maxcm` = 87.95 m is real here.** The usual failure mode — a LiDAR maximum that is
  a crane, an antenna or edge bleed from a taller neighbour — does not apply: the standard
  deviation is 20.01 m over 25,463 cells with a distinct modal plane 16 m below the
  maximum, the elevation photograph shows a genuine architectural crown pavilion at the top
  of a limestone tower, and OSM independently tags `height=91`. Model the crown.
- **OSM's `building:part` geometry is not trustworthy here and was not used for placement.**
  Way 944981401 is tagged 10 levels over 2,363 m2, ways 1487162810/11 are tagged 13 and 14
  levels, and when projected they land tens of metres from where the satellite puts the
  masses. Only their *areas* were used, as a weak third check on the crown.
- **The bay counts are inferred.** 12 bays on the 84.32 m faces and 11 on the 77.15 m faces
  at a ~6.5 m pitch are read from a single 2010 elevation photograph plus the satellite;
  neither shows a full square-on face. Verify before committing — this is the most likely
  place for the model to be visibly wrong.
- **The tower's setback levels (78.0 m and 84.0 m) are estimated**, read off the same
  photograph by counting window rows between the measured 32.28 m terrace and the measured
  87.95 m crown. Only the three principal planes are measured.
- **The northwest condition is inferred.** Imagery suggests a service way rather than a
  party wall, but no source consulted states it. If it turns out to be a party wall, that
  face should lose its openings, and the exclusion measurement in 2.13 becomes the critical
  one.
- **The 2022 renovation's exterior scope is unknown** beyond the four ground-floor retail
  fronts. The 2010 photograph is the best elevation source found and may predate a facade
  change at ground level.
