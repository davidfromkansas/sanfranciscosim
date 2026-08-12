# 380 Brannan Street — SF-SIM asset plan

A 1908 unreinforced-brick SoMa warehouse converted to creative office, one block west of
South Park. Not a monument — a *character* building: a slate-gray painted box with a
single bold coral stripe under its parapet, segmental-arched openings, and a raw red-brick
back that faces the Varney Place alley. It is the first plan in this set for an ordinary
street building rather than a civic landmark, so the design brief is "the block's most
memorable ordinary building", not "monument".

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/380-brannan/`. This document is the plan only: Part 1 is the runnable task
prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `380-brannan` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3940217, 37.7806308` |
| Target height | **12.6 m** to the stair-penthouse crest; main street parapet 11.9 m; roof deck 11.02 m |
| Footprint | 20.17 m (Brannan frontage, SE) x 23.9 m deep; 480.3 m2, measured |
| Triangle cap | 9,000 |
| Category | `3` (office) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 380 Brannan Street GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of 380 Brannan Street in San Francisco and deliver it
as a downloadable, validated GLB.

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
7. `artifacts/columbus-tower/` — the closest reference implementation in scale and
   character (small masonry building, arched storefront, designed roof, night state)
8. `docs/asset-plans/380-brannan.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Must capture

- A low, chunky two-storey masonry box with a flat roof and a continuous parapet
- The **coral/salmon band** running the full width of the Brannan Street facade
  immediately below the parapet cap — this is the building's whole identity
- Slate blue-gray painted front elevation vs **raw red brick** on the rear and flanks
- Segmental-arched ground-floor openings, including the wide arched freight door
- Tall industrial steel-sash upper windows
- The front fire escape balcony
- A designed flat roof: skylights, mechanical cluster, stair penthouse

## Research 380 Brannan Street independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- All four elevations, with particular attention to the painted-front /
  raw-brick-rear split
- Aerial and roof/top views (skylight and mechanical layout)
- Ground-level views
- Day and night appearance
- The bay count and window rhythm of the Brannan elevation — the dossier's
  6-bay reading is *inferred* from photography and must be confirmed
- The exact vertical position and depth of the coral band
- Whether the twin roof mast visible from the street should be modelled

Prefer architect/engineer publications, owner or institutional material,
planning and permitting documents, architectural press, geolocated photography,
and aerial/satellite imagery. Never rely on a single photograph, a single
AI-generated image, or a single unsourced 3D model. Separate verified facts from
visual inference; if sources disagree, document the disagreement and decide.

**Three source conflicts are already known and resolved in 2.1 — re-check them, do not
silently re-inherit the wrong value:** the SF Assessor roll says 3 storeys, the building
permits and both street-level photographs say **2**; OSM `building:levels=2` is right but
OSM `height=11` describes the roof deck, not the crest; and several listing sites describe
the building as "brick and timber", which is true of the structure and the *rear*
elevation but not of the painted street front.

## Create a reference dossier

Write `artifacts/380-brannan/REFERENCE.md` containing: source links and what each
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

This is a **secondary building** in the style bible's detail budget (§21), not a hero
landmark: clear massing, one strong facade rhythm, a simple designed roof, and exactly
one identity cue carried hard — the coral band. Resist adding hero-tier ornament.

The finished asset must be immediately recognizable as 380 Brannan Street, consistent with
the real building from all four sides and above, architecturally credible, and a
premium handcrafted miniature — not photorealistic, not voxel art, not generic
low-poly, and never accurate in one view while invented in the others.

## Scope of the exported asset

Export the single 1908 warehouse block: masonry body, parapet, coral band, all four
elevations' openings, the front fire escape, and the roof furniture.

Do not include unrelated surrounding city geometry: Brannan Street, Varney Place, the
neighbouring buildings on either flank, South Park, street trees, the sidewalk, parked
cars, people, plinths, cameras or lights. Temporary context may appear in review renders
but must not leak into the GLB.

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
(`placeGeneric` in `app/src/assets.js` only scales and positions). The Brannan Street
entrance front faces **southeast, bearing 135.6°**; the building is rotated roughly 45°
off the world axes, so build directly on the measured footprint polygon in 2.3 rather
than modelling an axis-aligned box and rotating it. Record the measured heading in
`REPORT.md`.

**Height normalization:** the tallest geometry in the export (the stair penthouse) must
land at exactly **12.6 m** so the loader's `targetHeightM / measuredHeight` scale is 1.0.

## Reproducible Blender workflow

Blender 5.2 LTS. Headless: `blender -b --python script.py -- args`.

Keep `artifacts/380-brannan/build_380_brannan.py` (deterministic build script),
`artifacts/380-brannan/380-brannan.blend`, and `artifacts/380-brannan/380-brannan.glb`.
The script must rebuild the model reliably enough for future revision. Do not modify or
rename an unrelated existing GLB to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`380-brannan-top.png`, `380-brannan-north.png`, `380-brannan-east.png`,
`380-brannan-south.png`, `380-brannan-west.png`, plus `380-brannan-contact-sheet.png`,
at least one high three-quarter aerial beauty render `380-brannan-aerial.png`, and a
night render `380-brannan-aerial-night.png`.

The four elevations must share scale, framing, lighting, exposure and
projection; use orthographic or long-lens cameras; label directions from the
researched orientation; the top view must clearly show the parapet ring, skylights,
mechanical cluster and stair penthouse; the aerial view uses the style bible's camera
assumptions (30-50 degrees down, long lens). Simple tabletop lighting, neutral warm
background, minimal depth of field, and every image must depict the same exported model.

## Validate the exported GLB

Re-import `380-brannan.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture
count, camera count, light count, animation count, applied-transform status,
negative-scale status, normal-orientation status, unexpected geometry, and
per-material contract compliance. Render at least one review image from the
re-imported asset. Write `artifacts/380-brannan/validation.json` and
`artifacts/380-brannan/REPORT.md`.

Note that the axis-aligned XY bounding box will be roughly **31 x 31 m** even though the
building is 20.2 x 23.9 m — that is the expected consequence of a ~45° real-world heading,
not a scale error.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "380-brannan",
  "file": "380-brannan.glb",
  "anchor": [
    -122.3940217,
    37.7806308
  ],
  "targetHeightM": 12.6,
  "cat": 3,
  "name": "380 Brannan Street",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a separate, explicitly requested job — run `docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in `docs/asset-plans/380-brannan.md`.
````

---

## Part 2 — Research and design dossier

Compiled 12 August 2026 from the sources in 2.2. Values marked *inferred* are visual or
derived estimates, not published figures — the executing agent must re-verify
anything it relies on.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Built | 1908 | SF Assessor secured roll, block 3775 lot 022 (consistent 2007-2025) |
| Storeys | **2** | SF building permits 1990-2015 (`number_of_existing_stories = 2`); confirmed by street-level photography on both Brannan and Varney |
| Assessor storey count | 3 | SF Assessor roll — **contradicted**, see 2.15; most likely counts a mezzanine |
| Construction | Unreinforced brick masonry (UMB) with timber framing | permit 1998 "earthquake retrofit-umb ordinance / anchor bolt, vertical brac"; listing copy "brick and timber" |
| Parapet | Present, reinforced 1990 | permit 1990-04-23 "parapet reinforcing" |
| Entrance canopy | Built 1993/1994 | permits "fabricate & install complete canopy", "construct canopy over doorway" |
| Block / lot | 3775 / 022 | SF Assessor, DataSF building footprints (`mblr = SF3775022`) |
| Footprint | 480.3 m2; 20.17 m (SE frontage) x 23.9 m deep; 99.1% rectangular fill | DataSF LiDAR building footprint, reprojected — **measured** |
| OSM footprint (cross-check) | 461.3 m2, 24.2 x 19.1 m | OSM way/1171034242 — agrees with DataSF within ~1.5 m |
| Roof deck height | 11.02 m above ground | DataSF LiDAR `hgt_median_m` — **measured** |
| Maximum feature height | 12.64 m above ground | DataSF LiDAR `hgt_maxcm` — **measured** |
| Parapet crest | ~11.9 m | *inferred*, roof deck + ~0.9 m parapet |
| Ground elevation | 8.31 m (NAVD88) | DataSF LiDAR `gnd_min_m` — app terrain handles this, not the asset |
| Building area | 11,560 sq ft | commercial listings; ~2.24 x the footprint, consistent with 2 full floors + mezzanine |
| Current occupant | South Park Commons (incubator) | OSM tags, occupant website |
| Frontage heading | Brannan front faces 135.6° (SE); rear faces 315.3° (NW) | measured from the footprint polygon |

### 2.2 Sources

- https://www.openstreetmap.org/way/1171034242 — footprint, address, `building=commercial`, occupant name
- `https://data.sfgov.org/resource/ynuv-fyni` (DataSF Building Footprints, LiDAR-derived) — authoritative footprint polygon and the 11.02 m / 12.64 m heights
- `https://data.sfgov.org/resource/wv5m-vpq2` (SF Assessor Historical Secured Property Tax Rolls) — 1908, block/lot, storey count
- `https://data.sfgov.org/resource/i98e-djp9` (SF Building Permits) — storey count, UMB retrofit, parapet reinforcing, entrance canopy
- Google Street View, Brannan Street pano (capture May 2025) — front elevation: slate-gray paint, coral band, arched openings, fire escape, "380" plate
- Google Street View, Varney Place pano (capture Jan 2025) — rear elevation: raw red brick, corbelled cornice, segmental-arched barred windows, roll-up service door
- Google Maps satellite (Vexcel imagery, 2026) — flat light-membrane roof, skylights, mechanical cluster
- Commercial listing copy (LoopNet / Showcase, "376-380 Brannan St") — 11,560 sq ft, "standalone brick and timber building", 15 ft ceilings, second-floor skylights

### 2.3 Orientation and placement

The building sits mid-block on the northwest side of Brannan Street, its rear against the
Varney Place alley. It is rotated about 45° from the world axes, like the whole SoMa grid.

Measured footprint polygon, in Blender coordinates (metres, `+X` east, `+Y` north),
counter-clockwise, already centred on the anchor `-122.3940217, 37.7806308`:

```
( 15.615,  -1.519)
( 15.493,  -1.396)
( -1.191,  15.507)
( -1.270,  15.586)
(-15.394,   1.621)
(  1.213, -15.642)
```

Edges, with outward normals:

| Edge | Length | Faces | Elevation |
|---|---|---|---|
| `(1.213,-15.642) -> (15.615,-1.519)` | 20.17 m | SE 135.6° | **Brannan Street front** |
| `(15.493,-1.396) -> (-1.191,15.507)` | 23.75 m | NE 45.4° | northeast flank |
| `(-1.270,15.586) -> (-15.394,1.621)` | 19.86 m | NW 315.3° | **Varney Place rear** |
| `(-15.394,1.621) -> (1.213,-15.642)` | 23.95 m | SW 226.1° | southwest flank |

The two remaining 0.11-0.17 m segments are corner chamfers; keep them, they cost nothing
and they keep the model honest to the survey.

Because of the 45° heading the axis-aligned bounding box is ~31 x 31 m. That is correct.

### 2.4 What each side shows

**Southeast (Brannan Street front)** — The hero elevation and the only painted one. A
slate blue-gray masonry wall carrying, top to bottom: a plain parapet cap; a **continuous
coral/salmon band** the full width of the facade; a row of tall industrial steel-sash
windows with dark frames and multi-light glazing; a string course at the floor line; and a
ground floor of segmental-arched openings — a wide arched freight door toward the
southwest end, several barred arched windows, and the recessed pedestrian entrance with
the "380" numerals above it. A steel fire escape balcony with a drop ladder hangs off the
upper floor, right of centre. A slim twin-pole mast rises above the parapet.

**Northwest (Varney Place rear)** — Raw, unpainted red brick, finished with a corbelled
brick cornice at the parapet. Segmental-arched windows on both floors, all heavily barred,
with pale stone sills. A segmental-arched roll-up service door at ground level. The alley
is narrow, so this face is only ever seen obliquely in the real world — but the app's
aerial camera sees it plainly, so it must be built properly.

**Northeast / southwest flanks** — Raw red brick, largely blank party-wall surfaces with
sparse openings. Treat them as brick with a light scatter of arched windows toward the
rear half; do not invent a full window grid.

**Top** — Flat light-gray membrane roof inside a continuous parapet. Visible from
satellite: a cluster of rectangular skylights (the listing's "skylights on the second
floor"), several dark mechanical/HVAC units grouped toward the middle of the roof, and a
stair penthouse. This is the surface the app's camera sees most — design it, do not leave
it flat.

### 2.5 Recognition cues (ranked)

1. **The coral band under the parapet** on a slate-gray box — unmistakable, and it happens
   to be almost exactly the project palette's `Toy_coral` (`#e8735a`)
2. Two-storey chunky masonry box with a flat roof and continuous parapet
3. The painted front / raw red-brick back-and-flanks split
4. Segmental-arched ground-floor openings, especially the wide freight arch
5. The front fire escape

### 2.6 Miniature translation

**Preserve**

- The single-volume chunky box and its real 45° heading
- The coral band's full-width continuity and its position directly under the cap
- The two-material story: painted front, brick everywhere else
- The arched ground-floor openings as arches, not rectangles

**Simplify / exaggerate**

- Roughly 14 upper windows become 6 clean bays per long elevation, all identical
- Individual bricks become flat colour; the corbelled rear cornice becomes one 0.25 m
  proud band
- Window bars and grilles disappear entirely — they are sub-pixel at city scale
- The coral band is thickened slightly (to ~1.0 m) so it survives at thumbnail size; this
  is the one place semantic exaggeration is spent
- The fire escape becomes a single chunky balcony slab plus two rails — no ladder treads
- Roof clutter becomes three clean skylight boxes, one HVAC cluster of two blocks, and one
  stair penthouse
- The twin mast is dropped: it is a hairline at the app's camera and would set the
  bounding-box top on a feature that reads as nothing

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not
a straitjacket — adjust after the first aerial review render.

1. Body: extrude the 2.3 footprint from z=0 to z=11.0, `Toy_brick`. This is the brick
   shell that the rear and flanks show.
2. Front skin: a 0.12 m proud panel on the SE edge only, z=0 to z=11.0, `Toy_stone`
   tinted slate — the painted elevation. (Use `Toy_steel` if a cooler gray reads better;
   decide from the render, record the choice.)
3. Ground floor, z=0 to z=4.6: on the SE face, one 4.2 m wide segmental-arched freight
   opening toward the southwest end, three 1.6 m arched windows, and a 1.6 m recessed
   entrance with a flat canopy at z=3.2. On the NW face, one 3.4 m arched roll-up door and
   two arched windows. Arches: 8-segment, rise 0.5 m.
4. String course: 0.2 m `Toy_trim` band at z=4.6, front elevation only.
5. Upper floor, z=5.1 to z=9.6: 6 bays per long elevation, openings 1.5 x 3.2 m, recessed
   0.2 m, `Toy_glass`. Flat heads on the front, segmental heads on the rear.
6. Coral band: `Toy_coral`, z=9.9 to z=10.9, wrapping the SE front full width and returning
   0.6 m onto each flank so it reads from three-quarter angles.
7. Parapet: z=11.0 to z=11.9, following the footprint, 0.35 m thick, `Toy_stone` cap on the
   front and `Toy_brick` with a 0.25 m proud corbel band on the rear and flanks.
8. Roof deck at z=11.0, `Toy_roofd`. Three skylight boxes 2.6 x 1.8 x 0.35 m in a row,
   `Toy_glassl`; two HVAC blocks (2.2 x 1.6 x 1.0 m and 1.6 x 1.2 x 0.8 m) `Toy_steel`;
   stair penthouse 3.6 x 2.8 m from z=11.0 to **z=12.6** `Toy_roofd` — this sets the
   bounding-box top and must land exactly on 12.6.
9. Fire escape: balcony slab 3.0 x 0.9 x 0.15 m at z=5.4 on the SE face, `Toy_ink`, with
   two 1.0 m rail bars.
10. Bevel 0.12 m, 2 segments.

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_brick` | `#c96f4a` | rear and flank walls, rear parapet and corbel |
| `Toy_stone` | `#d9d2c2` | painted front skin, parapet cap, sills |
| `Toy_coral` | `#e8735a` | **the signature band** |
| `Toy_trim` | `#f3efe6` | string course, entrance canopy |
| `Toy_glass` | `#2a4d73` | all windows |
| `Toy_glassl` | `#6f95b8` | skylights (lighter, reads as up-facing glazing) |
| `Toy_roofd` | `#45454a` | roof deck, stair penthouse, freight door |
| `Toy_steel` | `#9aa0a6` | HVAC blocks |
| `Toy_ink` | `#3a3530` | fire escape, door recesses |
| `Toy_glass_Glow` | `#2a4d73` | lit upper windows at night |
| `Toy_trim_Glow` | `#f3efe6` | entrance canopy underside at night |

Note on the painted front: the real colour is a slate blue-gray with no exact palette
match. `Toy_stone` is warmer than reality and `Toy_steel` is cooler; off-palette is a WARN
not a FAIL, so a dedicated `Toy_slate` at roughly `#6f7883` is permissible if the render
justifies it. Decide from the aerial render and record the decision in `REPORT.md`.

**Night state (required).** Glow surfaces must be thin shells proud of the opaque glazing —
the app renders `_Glow` in a separate layer that is ~12% alpha by day, so a primary surface
must never be authored as glow. Hero glow: a scatter of lit upper windows on the Brannan
front (not all of them — this is a small building, four or five is plenty). Supporting
accent: the entrance canopy underside. The coral band does **not** glow; it is a daylight
identity feature and lighting it would misread as signage.

### 2.9 Top surface

A flat roof 11 m up in a district the camera flies over constantly. Three skylight boxes in
a row parallel to the Brannan edge, an HVAC pair grouped off-centre, one stair penthouse at
the rear corner, and a continuous parapet ring so the deck never reads as an open tray.
Keep the deck value clearly darker than the parapet cap so the ring reads from above.

### 2.10 Scope

**In the GLB:** the single 1908 warehouse block — masonry body, parapet, coral band, all
four elevations' openings, front fire escape, roof deck and roof furniture

**Not in the GLB:** Brannan Street, Varney Place, the neighbouring buildings, South Park,
street trees, sidewalk, vehicles, people, plinths, cameras or lights

### 2.11 Triangle budget

Cap 9,000 — this is a secondary building, not a hero, and the cap should bind. Suggested
split: body and parapet ~2k, upper window bays ~2.5k, ground-floor arched openings ~2k,
roof furniture ~1.5k, fire escape and canopy ~0.5k.

### 2.12 Draft manifest entry

```json
{
  "id": "380-brannan",
  "file": "380-brannan.glb",
  "anchor": [
    -122.3940217,
    37.7806308
  ],
  "targetHeightM": 12.6,
  "cat": 3,
  "name": "380 Brannan Street",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

`dims` and `tris` are placeholders until the asset is built and validated.

### 2.13 Integration notes (for later, not this task)

- **New landmark.** Add a `pipeline/lib/landmarks.mjs` entry (`id: '380-brannan'`,
  `exclude: ~18`) and re-bake the affected tiles, or the baked procedural building on this
  exact footprint will intersect the GLB. The exclusion radius must be tight: neighbours
  are only a few metres away on both flanks and a generous radius would punch holes in the
  block.
- `loadRadius`: the skill's default formula gives `max(2500, 12.6 * 30) = 2500` m. Because
  the procedural stand-in is carved out, beyond that radius the site is a gap — but at
  2.5 km a 12 m building is far below a pixel, so the absence is illegible. Take the
  default.
- This is the first non-monument building in the landmark manifest. If the intent is to
  keep doing individual SoMa blocks, consider whether the kit/instancing route
  (`KIT-INTEGRATION-PROMPT.md`) is the better long-term home for buildings of this class —
  a manifest of 300 one-off warehouses would not stream well.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Bounding-box top exactly 12.6 m (loader scale lands at 1.0)
- [ ] Dimensions plausible in meters and consistent with 2.1 (XY bbox ~31 x 31 m is expected)
- [ ] Triangles at or under 9,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the lit upper windows and the canopy underside; glow shells proud of opaque glazing
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (per-object signed volume for the union of solids; ray test residual <= 0.15%)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + contact sheet + night render regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

- **Storey count conflict, resolved.** The SF Assessor roll records 3 storeys in every year
  from 2007 to 2025; every building permit from 1990 to 2015 records 2, and both street-level
  photographs plainly show 2. The 11,560 sq ft floor area is ~2.24x the 480 m2 footprint,
  which fits two full floors plus a mezzanine — the most likely explanation for the
  assessor's third storey. **Build 2 storeys.**
- **OSM `height=11` is the roof deck, not the crest.** It happens to match the LiDAR median
  (11.02 m) almost exactly, which is a coincidence worth not being fooled by: the crest is
  ~11.9 m and the tallest feature 12.64 m. This is exactly the trap the plans README warns
  about, in a building where the tag looks plausible.
- **"Brick and timber" is only half true externally.** The structure is brick and timber and
  the rear and flanks are raw brick, but the Brannan front is painted slate gray. A modeller
  who reads only the listing copy will build the wrong front elevation.
- The 6-bay window rhythm is *inferred* from photography at an oblique angle and is the
  weakest number in this dossier. Confirm before committing to the facade.
- The exact vertical extent of the coral band is *inferred* (~1.0 m, top at ~10.9 m).
- Whether the flanks are true party walls or have a small gap to the neighbours is
  unresolved; the listing calls the building "standalone". Modelling all four faces as
  finished brick is the safe choice either way.
- No architect is recorded for the 1908 building in any source consulted.
</content>
</invoke>
