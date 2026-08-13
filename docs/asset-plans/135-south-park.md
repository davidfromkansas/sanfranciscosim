# 135 South Park — SF-SIM asset plan

A 1925 two-storey brick industrial building on the south-east arc of the South Park oval,
now an architecture studio. It is the smallest and plainest building yet planned for this
set: no architect of record, no published photography, no name. What it *does* have is an
unusual **L-shaped footprint with a re-entrant rear yard**, a **dark roof carrying a raised glazed
monitor** that its light-roofed neighbours do not have, and a party wall on one flank —
all measured, all visible from the app's aerial camera. The design brief is therefore
inverted relative to the rest of the set: **the roof is the identity, not the facade.**

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/135-south-park/`. This document is the plan only: Part 1 is the runnable task
prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `135-south-park` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3940203, 37.7811030` (footprint area centroid, measured) |
| Target height | **8.5 m** to the roof-monitor crest; street parapet 7.9 m; roof deck 7.0 m — LiDAR-derived, see 2.1 and 2.15 |
| Footprint | L-shaped, 383.1 m²; 19.71 m frontage on South Park (NW) × 28.65 m deep on the NE party wall; measured |
| Triangle cap | 8,000 |
| Category | `3` (office) — the assessor still classes it Industrial, see 2.1 |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 135 South Park GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of 135 South Park in San Francisco and deliver it
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
7. `artifacts/380-brannan/` — the closest reference implementation in every way: same
   block (3775), one block south-east, same era and construction, same 45° heading,
   same "memorable ordinary building" brief
8. `docs/asset-plans/135-south-park.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Read 2.15 before you start

This dossier is **asymmetric**: its massing is measured to survey accuracy and its
facade is a typological reconstruction with no photographic confirmation. Section 2.15
says exactly which is which. Do not treat the facade paragraphs as established fact,
and do not quietly promote them to fact in `REFERENCE.md`.

## Must capture

- A low, chunky two-storey brick box on the real **L-shaped footprint**, with the
  re-entrant **rear yard** on the south-west side left as a genuine void — not
  filled in, not simplified to a rectangle
- A continuous parapet ring, higher than the roof deck, reading clearly from above
- The **raised glazed roof monitor** running along the deep north-east wing — the one
  feature that distinguishes this roof from every neighbour's, and this asset's whole
  identity cue
- A **dark charcoal roof deck** against the light-gray roofs either side
- The **blank north-east party wall** shared with 123 South Park: no openings at all
- Tall industrial upper glazing on the South Park (north-west) front
- A designed roof: monitor, mechanical cluster at the rear, roof hatch, parapet ring

## Research 135 South Park independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- **Street-level photography of the South Park elevation.** This is the single
  biggest gap in the dossier — nothing in 2.2 shows the front of this building.
  Google Street View has South Park coverage (a Jan 2025 pano sits outside 157);
  the occupant, Mark Horton / Architecture, may publish photographs of its own
  studio; commercial listings for the second-floor suite carry exterior shots.
- Whether the front is **raw brick, painted brick, or stucco**, and its colour
- The bay count and window rhythm of the South Park elevation
- What the ground floor actually does: freight opening, garage, storefront, or
  a plain pedestrian entrance
- The rear (south-east) elevation onto the courtyard, and whether the re-entrant yard on
  the south-west is open to the ground or infilled at ground level
- Aerial and roof views: confirm the raised element on the deep wing is a **glazed
  monitor / clerestory** and not simply a mechanical penthouse. The dossier's whole
  design proposition rests on this and it is *inferred* from one aerial (2.4).
- Day and night appearance

Prefer architect/engineer publications, owner or institutional material,
planning and permitting documents, architectural press, geolocated photography,
and aerial/satellite imagery. Never rely on a single photograph, a single
AI-generated image, or a single unsourced 3D model. Separate verified facts from
visual inference; if sources disagree, document the disagreement and decide.

**Two source conflicts are already known and resolved in 2.1 — re-check them, do not
silently re-inherit the wrong value:** the 1990 parapet permit records 1 storey while the
1986 permit and every assessor roll from 2007 to 2025 record **2**; and the building
carries **no OSM `height` tag at all**, so its height comes entirely from 2010 LiDAR —
which means the 8.52 m maximum could be either a roof monitor or simply the front
parapet. 2.15 explains why it does not change the target height, and why it does change
the roof design.

## Create a reference dossier

Write `artifacts/135-south-park/REFERENCE.md` containing: source links and what each
establishes; verified dimensions and location; orientation; observations from all
four sides and above; the 3-5 strongest recognition cues; features to preserve;
features to simplify; uncertainties and conflicting evidence. Be explicit about which
facade statements you confirmed and which you inherited unconfirmed from this plan.
A contact sheet of attributed reference thumbnails is welcome if legally permissible —
do not commit copyrighted full-resolution imagery.

## Make your own design decisions

Follow the conversion process in `docs/styles/miniature-toy.md` §22: identify the
recognition cues, strip nonessential information, rebuild the massing from a few
confident volumes, exaggerate only the signature features, simplify the facade
into broad rhythms, deliberately design every surface visible from above,
evaluate from the app's high three-quarter aerial camera, then simplify again.

This is a **secondary building** in the style bible's detail budget (§21) — in fact the
plainest one in the set. Clear massing, one strong facade rhythm, a designed roof, and
exactly one identity cue carried hard: the glazed roof monitor. Resist adding hero-tier
ornament, and resist inventing facade detail to compensate for thin references —
§29 says a building that lacks personality should strengthen ONE defining characteristic,
and here that characteristic is on the roof.

The finished asset must be immediately recognizable as this building's real massing,
consistent from all four sides and above, architecturally credible, and a
premium handcrafted miniature — not photorealistic, not voxel art, not generic
low-poly, and never accurate in one view while invented in the others.

## Scope of the exported asset

Export the single 1925 building: brick shell on the L footprint, parapet, all four
elevations' openings, roof deck, roof monitor and roof furniture.

Do not include unrelated surrounding city geometry: South Park (the street or the park),
the neighbouring buildings at 123 and 147 South Park, the rear courtyard and its parked
cars, street trees, the sidewalk, people, plinths, cameras or lights. Temporary context
may appear in review renders but must not leak into the GLB.

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
(`placeGeneric` in `app/src/assets.js` only scales and positions). The South Park
entrance front faces **north-west, outward bearing 315.4°**; the building is rotated
roughly 45° off the world axes, so build directly on the measured footprint polygon in
2.3 rather than modelling an axis-aligned box and rotating it. Record the measured
heading in `REPORT.md`.

**Height normalization:** the tallest geometry in the export (the roof monitor) must
land at exactly **8.5 m** so the loader's `targetHeightM / measuredHeight` scale is 1.0.

## Reproducible Blender workflow

Blender 5.2 LTS. Headless: `blender -b --python script.py -- args`.

Keep `artifacts/135-south-park/build_135_south_park.py` (deterministic build script),
`artifacts/135-south-park/135-south-park.blend`, and
`artifacts/135-south-park/135-south-park.glb`. The script must rebuild the model reliably
enough for future revision. Do not modify or rename an unrelated existing GLB to satisfy
the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`135-south-park-top.png`, `135-south-park-north.png`, `135-south-park-east.png`,
`135-south-park-south.png`, `135-south-park-west.png`, plus
`135-south-park-contact-sheet.png`, at least one high three-quarter aerial beauty render
`135-south-park-aerial.png`, and a night render `135-south-park-aerial-night.png`.

The four elevations must share scale, framing, lighting, exposure and
projection; use orthographic or long-lens cameras; label directions from the
researched orientation; **the top view is the important one here** and must clearly show
the parapet ring, the rear yard, the roof monitor and the mechanical cluster; the aerial
view uses the style bible's camera assumptions (30-50 degrees down, long lens). Simple
tabletop lighting, neutral warm background, minimal depth of field, and every image must
depict the same exported model.

## Validate the exported GLB

Re-import `135-south-park.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture
count, camera count, light count, animation count, applied-transform status,
negative-scale status, normal-orientation status, unexpected geometry, and
per-material contract compliance. Render at least one review image from the
re-imported asset. Write `artifacts/135-south-park/validation.json` and
`artifacts/135-south-park/REPORT.md`.

Note that the axis-aligned XY bounding box will be roughly **34.3 × 25.8 m** even though
the building is 19.7 m wide and 28.7 m deep — that is the expected consequence of a ~45°
real-world heading, not a scale error.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "135-south-park",
  "file": "135-south-park.glb",
  "anchor": [
    -122.3940203,
    37.7811030
  ],
  "targetHeightM": 8.5,
  "cat": 3,
  "name": "135 South Park",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a separate, explicitly requested job — run `docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in `docs/asset-plans/135-south-park.md`.
````

---

## Part 2 — Research and design dossier

Compiled 12 August 2026 from the sources in 2.2. Values marked *inferred* are visual or
derived estimates, not published figures — the executing agent must re-verify
anything it relies on. **This dossier's facade section is materially weaker than its
massing section; read 2.15 before relying on any of it.**

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Address | 135 South Park (OSM records the street as "South Park", not "S Park St") | OSM way/113545684 `addr:*` tags |
| Block / lot (APN) | 3775 / 033 | SF Assessor roll; DataSF footprint `mblr = SF3775033`; LoopNet "APN/Parcel ID: 3775-033" |
| Built | **1925** | SF Assessor secured roll, consistent across all 19 rows 2007–2025 |
| Storeys | **2** | SF Assessor roll (`number_of_stories = 2.0`, every year); 1986 building permit (`number_of_existing_stories = 2`) |
| Conflicting storey count | 1 | 1990 parapet permit — **contradicted**, see 2.15 |
| Assessor use class | Industrial | SF Assessor roll (`use_definition` and `property_class_code_definition`) |
| Current use | Office — architecture studio (Mark Horton / Architecture), plus a second-floor office suite offered for lease | LoopNet listing for 135 South Park; Yelp business listing at 135 S Park St |
| Parapet | Present, strengthened 1990 | permit 1990-12-31 "parapet strengthening" |
| Re-roofed | 1999 | permit 1999-04-07 "reroofing" |
| Footprint | **383.1 m²**, L-shaped, 10 vertices; 19.71 m frontage (NW) × 28.65 m along the NE party wall | OSM way/113545684 geometry via Overpass, reprojected — **measured** |
| DataSF footprint (cross-check) | 432.1 m², centroid 0.6 m from the OSM centroid | DataSF Building Footprints `SF3775033` — agrees on position, disagrees on the rear boundary (see 2.15) |
| Roof deck height | **~7.0 m** above ground (`hgt_majoritycm` 7.06 m, `hgt_mediancm` 6.95 m) | DataSF LiDAR — **measured** |
| Maximum feature height | **8.52 m** above ground (`hgt_maxcm`) | DataSF LiDAR — **measured** |
| Street parapet crest | ~7.9 m | *inferred*, roof deck + ~0.9 m parapet |
| Ground elevation | 8.77 m (NAVD88, `gnd_min_m`) | DataSF LiDAR — app terrain handles this, not the asset |
| Frontage heading | South Park front faces **315.4° (NW)**; NE party wall outward 45.0°; rear faces 135° (SE) | measured from the footprint polygon |
| North-east neighbour | **123 South Park** — shares a party wall, 0.0 m gap; OSM `height=7` | OSM way/113545683, measured against our polygon |
| South-west neighbour | **147 South Park** — 5.6 m gap; OSM `height=12` | OSM way/124889475 |
| Rear neighbour | unnamed building, nearest vertex 6.18 m from our anchor | OSM way/1311547493 — the binding constraint on the exclusion radius, see 2.13 |
| Row context | The SE arc of the oval runs 101 (h=6), 115/117 (h=7), 123 (h=7), **135**, 147 (h=12), 155/157 (h=9) | OSM height tags — 7 m puts this building squarely in its row |

### 2.2 Sources

- https://www.openstreetmap.org/way/113545684 — footprint geometry and address. Note it carries **no** `height` and **no** `building:levels`.
- `https://data.sfgov.org/resource/ynuv-fyni` (DataSF Building Footprints, LiDAR-derived) — footprint `SF3775033` and the 6.95 / 7.06 / 8.52 m heights, ground elevation 8.77 m NAVD88
- `https://data.sfgov.org/resource/wv5m-vpq2` (SF Assessor Historical Secured Property Tax Rolls) — 1925, block/lot, 2 storeys, Industrial class
- `https://data.sfgov.org/resource/i98e-djp9` (SF Building Permits) — 1986 partitions (2 storeys), 1990 parapet strengthening, 1999 reroofing
- Esri World Imagery (ArcGIS Online `World_Imagery`, z20 tiles 167788–167790 / 405272–405274) — the roof observations in 2.4 and 2.9, at ~0.12 m/px
- LoopNet listing "135 South Park, San Francisco, CA 94107-1808" (APN 3775-033) — office use, second-floor suite with kitchen and shower
- Yelp, "Mark Horton Architecture", 135 S Park St — occupant
- Wikimedia Commons, geo-tagged South Park photographs (`South Park SF top view January 2020.jpg`, `South Park SF January 2020.jpg`, `South Park Facing NE.jpg`) — **neighbourhood character only; none of them shows this building**
- `docs/asset-plans/380-brannan.md` — the same block, 55 m south-east; its 2.4/2.8 are the best available proxy for the district's material language

**Sources deliberately NOT used:** no photograph of 135 South Park's own street elevation
was located. Google Maps and Street View would not render in the available browser
environment, and the LoopNet and Yelp galleries were not retrievable (403). Everything in
2.5 below that concerns the facade is typological reasoning, not observation.

### 2.3 Orientation and placement

The building sits on the south-east arc of the South Park oval, its front looking
north-west across the street into the park, its rear onto a courtyard toward Varney Place.
It is rotated about 45° from the world axes, like the whole SoMa grid — and like 380
Brannan one block away, whose front faces the exactly opposite bearing.

Measured footprint polygon, in Blender coordinates (metres, `+X` east, `+Y` north),
counter-clockwise, already centred on the anchor `-122.3940203, 37.7811030`:

```
( -2.133,  13.562)
(-16.178,  -0.267)
( -6.331, -10.127)
( -0.180,  -4.070)
( -1.456,  -2.798)
(  0.920,  -0.455)
( 11.550, -11.089)
( 12.685, -12.227)
( 18.114,  -6.700)
(  1.457,   9.969)
```

Edges, with outward normals:

| Edge | Length | Faces | Elevation |
|---|---|---|---|
| `(-2.133,13.562) -> (-16.178,-0.267)` | 19.71 m | NW 315.4° | **South Park front** |
| `(-16.178,-0.267) -> (-6.331,-10.127)` | 13.93 m | SW 225.0° | south-west flank (5.6 m gap to 147) |
| `(-6.331,-10.127) -> (-0.180,-4.070)` | 8.63 m | SE 135.4° | rear wall of the front block |
| `(-0.180,-4.070) -> (-1.456,-2.798)` | 1.80 m | NE 44.9° | jog at the step |
| `(-1.456,-2.798) -> (0.920,-0.455)` | 3.34 m | SE 135.4° | jog at the step |
| `(0.920,-0.455) -> (11.550,-11.089)` | 15.04 m | SW 225.0° | **south-west flank of the deep wing**, onto the rear yard |
| `(11.550,-11.089) -> (12.685,-12.227)` | 1.61 m | SW 225.1° | corner chamfer |
| `(12.685,-12.227) -> (18.114,-6.700)` | 7.75 m | SE 134.5° | **rear wall**, onto the courtyard |
| `(18.114,-6.700) -> (1.457,9.969)` | 23.57 m | NE 45.0° | **party wall with 123 South Park** |
| `(1.457,9.969) -> (-2.133,13.562)` | 5.08 m | NE 45.0° | party wall, front return |

Resolved into building-local coordinates — `u` along the party wall from the rear corner
towards the front, `v` the depth into the block from that wall — the plan is exactly a
rectangle with one big bite taken out:

```
 v=19.71 |  v1(28.79) ------------------- v2(14.85)          front block:
         |      |                              |             full 19.71 m width
 v=11.08 |      |                    v3(14.79)-v4(16.59)     for the front 13.9 m
  v=7.75 |      |          v6(1.535)--------------v5(16.57)  ---------------------
         |      |              |                             deep wing: 7.75 m
   v=0   |  v0(28.64) -- v9(23.56) ------------ v8(0)        strip along the wall
         +---------------------------------------------->  u
            front                                rear
```

So: the full 19.71 m frontage runs back only **13.9 m**; past that only the **7.75 m strip
along the party wall** continues another 14.8 m to the rear. The missing rectangle —
roughly **14.8 m × 12.0 m** — is a **re-entrant rear yard**, open to the south-west (the
5.6 m gap to 147) and to the south-east (the courtyard). It is not an enclosed light well.
The 1.80 × 3.33 m jog at edges 3–4 is a real step in the survey; keep it, it costs
nothing.

This is what makes the footprint worth extruding literally rather than approximating with
a box.

Because of the 45° heading the axis-aligned bounding box is ~34.3 × 25.8 m. That is
correct.

### 2.4 What each side shows

**North-west (South Park front)** — the hero elevation, 19.71 m wide, facing the park
across the street. *All of the following is inferred* from the building's 1925 date,
Industrial assessor class, unreinforced-masonry parapet permit, and the material language
of the block (see 380 Brannan's 2.4): a two-storey brick wall under a plain parapet, a
band of tall industrial upper glazing, and a ground floor with a wide opening (freight or
garage) alongside a pedestrian entrance. The aerial shows the parapet as a crisp bright
line and the sidewalk beneath in tree shadow; nothing more can be read from above.
**Confirm this elevation from photography before modelling it.**

**North-east (party wall with 123 South Park)** — 28.65 m long, shared with the
neighbouring building along its entire length, gap 0.0 m. This is a **blank wall**: a
party wall cannot carry openings. This is a verified fact and it is one of the few
free wins in the dossier — model it as unbroken brick and it will be right.

**South-west (flank and rear yard)** — 13.93 m of front-block flank facing the 5.6 m gap
to 147 South Park, then the plan steps back and the deep wing presents its 15.04 m flank
to the open rear yard. Because both the gap and the yard are real, this side genuinely has
daylight and therefore plausibly has windows — which is presumably why the building was
cut back at all. Treat it as brick with a modest scatter of openings; do not invent a
full grid.

**South-east (rear)** — 7.75 m of rear wall plus the 8.63 m rear wall of the west wing,
onto a tan open courtyard clearly visible in the aerial with cars parked in it. Service
elevation: expect a roll-up door and a few small openings.

**Top** — the surface that matters, and the one with real evidence. From the Esri aerial
at ~0.12 m/px:

- A **mid-to-dark gray flat membrane roof**, conspicuously darker in value than the
  light-gray roofs of 123 to the north-east and of the buildings across the courtyard.
- A **raised, lighter-toned linear element** running north-west/south-east along the deep
  wing — parallel to the party wall, i.e. along the building's depth — roughly 11–13 m
  long and 4–5 m wide, casting its own shadow to the south-west. This is the tallest thing on the building and the most likely explanation
  for the 8.52 m LiDAR maximum over a 7.0 m deck. Read as a **roof monitor / clerestory**
  — the classic daylighting device of a 1925 industrial building, and exactly the feature
  an architecture practice would keep. *Inferred*; see 2.15.
- A small **round object** (~1 m) on the north-west half of the deck — a vent cowl or a
  round rooflight.
- A **mechanical cluster** of small units toward the rear, and what appears to be a roof
  hatch or stair bulkhead near the south-west corner.
- A continuous **parapet ring**, visible as a bright edge on the north-west and south-west
  sides.

### 2.5 Recognition cues (ranked)

1. **The L footprint with its re-entrant rear yard** — measured, unusual on this row, and
   the silhouette a top-down camera reads first
2. **The dark roof deck** against the light roofs either side — a real value contrast,
   free legibility
3. **The raised glazed roof monitor** on the deep wing — the identity feature, and the
   one worth exaggerating
4. Low two-storey brick box, flat roof, continuous parapet, 45° to the world grid
5. The unbroken north-east party wall

Note that cues 1–3 are all read from above. That is the correct hierarchy for this
building: at the app's camera, this is a roof.

### 2.6 Miniature translation

**Preserve**

- The L footprint and the rear yard as a true void, at their real 45° heading
- The roof monitor's position, orientation and dominance of the roof composition
- The blank party wall
- The value contrast: dark deck, lighter parapet cap, lighter monitor glazing

**Simplify / exaggerate**

- The monitor is the one place semantic exaggeration is spent: build it taller and more
  clearly glazed than reality (crest at 8.5 m, i.e. 1.5 m above the deck) so it reads as
  a lantern from the aerial camera rather than as another mechanical box
- Individual bricks become flat colour; any cornice becomes one shallow proud band
- Roughly a dozen upper windows become 5 clean bays on the front and 4 on the deep wing's
  south-west flank
- Ground-floor openings reduce to one wide opening, one entrance, one rear roll-up door
- Roof clutter becomes one mechanical pair and one hatch — nothing else
- Window bars, downpipes, fire escapes, signage: dropped unless photography turns up
  something that earns a place

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not
a straitjacket — adjust after the first aerial review render.

1. Body: extrude the 2.3 footprint from z=0 to **z=7.0**, `Toy_brick`. The rear yard
   comes free with the polygon — do not fill it.
2. Ground floor, z=0 to z=4.0: on the NW front, one 4.0 m wide opening toward the
   south-west end (`Toy_roofd`, reading as a freight/garage door) and a 1.6 m recessed
   pedestrian entrance with a flat `Toy_trim` canopy at z=3.0. On the SE rear, one 3.0 m
   roll-up door. Nothing on the NE party wall.
3. Upper floor, z=4.4 to z=6.5: 5 bays on the NW front and 4 on the deep wing's SW flank,
   openings 1.6 × 2.1 m, recessed 0.2 m, `Toy_glass`. Two small openings on the rear.
   **None on the NE party wall.**
4. Parapet: z=7.0 to **z=7.9**, following the whole footprint ring, 0.35 m thick,
   `Toy_rust` under a 0.15 m proud `Toy_trim` coping carried right round the ring — the
   coping is what makes the ring read as a ring from the app's downward camera.
5. Roof deck at z=7.0, `Toy_roofd` — keep it clearly darker than the parapet cap so the
   ring reads from above.
6. **Roof monitor**: a raised block on the deep NE wing, long axis running NW–SE parallel
   to the party wall (i.e. along the wing's length), ~11.0 × 4.2 m in plan, centred about
   7.5 m forward of the rear corner and in the middle of the 7.75 m wing, from z=7.0 to
   **z=8.5**. Sides `Toy_glassl`
   (the clerestory glazing), cap `Toy_roofd`, 0.15 m `Toy_trim` upstand at its base.
   This sets the bounding-box top and must land exactly on 8.5.
7. Roof furniture: two HVAC blocks (1.8 × 1.4 × 0.8 m and 1.2 × 1.0 × 0.6 m) `Toy_steel`
   grouped toward the rear; one roof hatch 1.2 × 1.0 × 0.5 m `Toy_roofd` near the
   south-west corner; one round vent cowl r=0.4 m, h=0.5 m, `Toy_steel`, 10-segment, on
   the north-west half of the deck.
8. Bevel 0.12 m, 2 segments.

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_rust` | `#a86444` | all four walls, parapet |
| `Toy_trim` | `#f3efe6` | parapet cap, entrance canopy, monitor upstand |
| `Toy_glass` | `#2a4d73` | upper-floor windows |
| `Toy_glassl` | `#6f95b8` | **the roof-monitor clerestory glazing** |
| `Toy_trim` | `#f3efe6` | full parapet coping ring |
| `Toy_roofd` | `#45454a` | roof deck, monitor cap, freight/roll-up doors, roof hatch |
| `Toy_steel` | `#9aa0a6` | HVAC blocks, vent cowl |
| `Toy_ink` | `#3a3530` | door and window recesses |
| `Toy_glassl_Glow` | `#6f95b8` | **the lit monitor at night** |
| `Toy_glass_Glow` | `#2a4d73` | a few lit upper windows on the front |

Masonry is `Toy_rust` (`#a86444`) rather than the palette's `Toy_brick` (`#c96f4a`) for
the same reason 380 Brannan made that swap one block away: `c96f4a` is saturated enough
that a whole building of it becomes an accent rather than a neutral, which the style
bible's §7 reserves for identity features. Using the browner value also makes the two
buildings read as one district. Record the choice in `REPORT.md`.

If photography shows the front is painted rather than raw brick, `Toy_stone` (`#d9d2c2`)
on a 0.12 m proud panel on the NW edge only is the right correction — again the device
380 Brannan uses.

**Night state (required).** Glow surfaces must be thin shells proud of the opaque glazing —
the app renders `_Glow` in a separate layer that is ~12% alpha by day, so a primary surface
must never be authored as glow. **Hero glow: the roof monitor**, lit along its full length,
so the building reads at night as a glowing lantern on a dark roof — the night-time
statement of the same identity cue that carries the day. Supporting accent: three or four
lit windows on the South Park front, not all of them. Nothing else glows.

This is the strongest night proposition in the small-building set and it is the reason to
build this asset at all: from the app's aerial camera at night, a lit roof monitor on an
otherwise dark SoMa block is legible in a way a 8.5 m brick box never is.

### 2.9 Top surface

A flat roof 7 m up in a district the camera flies over constantly, and this asset's
primary elevation. Composition, north-west to south-east: clean dark deck with the single
round cowl; the parapet ring bright against it; the rear yard biting in from the
south-west as a shadowed void; the glazed monitor running the length of the deep wing as
the roof's spine; the mechanical pair and hatch grouped at the rear. Keep the deck value
clearly darker than both the parapet cap and the monitor so all three read separately
from above.

### 2.10 Scope

**In the GLB:** the single 1925 building — brick shell on the L footprint, rear yard,
parapet, all four elevations' openings, roof deck, roof monitor and roof furniture

**Not in the GLB:** South Park (street or park), 123 and 147 South Park, the rear
courtyard and its cars, street trees, sidewalk, vehicles, people, plinths, cameras
or lights

### 2.11 Triangle budget

Cap 8,000 — smaller and simpler than 380 Brannan's 9,000, and the cap should bind.
Suggested split: body, rear yard and parapet ring ~2.5k (the 10-vertex L costs more
than a box), upper window bays ~1.5k, ground-floor openings ~1k, roof monitor ~1.5k,
roof furniture and cowl ~1k.

### 2.12 Draft manifest entry

```json
{
  "id": "135-south-park",
  "file": "135-south-park.glb",
  "anchor": [
    -122.3940203,
    37.7811030
  ],
  "targetHeightM": 8.5,
  "cat": 3,
  "name": "135 South Park",
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

- **New landmark, Case B.** Add a `pipeline/lib/landmarks.mjs` entry
  (`id: '135SouthPark'`) and re-bake the affected tiles, or the baked procedural building
  on this exact footprint will intersect the GLB.

- **`exclude: 5`.** This is the tightest exclusion window in the whole registry and it was
  sized against the metric `excluded()` in `pipeline/buildings.mjs` actually uses —
  *the ring centroid **or** any ring vertex inside the circle*. Measured from this anchor:

  | | nearest vertex | centroid |
  |---|---|---|
  | own footprint (OSM) | 1.03 m | 3.04 m |
  | own footprint (DataSF `SF3775033`) | 4.68 m | 3.29 m |
  | **nearest neighbour (OSM way/1311547493, rear)** | **6.18 m** | 12.96 m |
  | nearest neighbour (DataSF `SF3775036`) | 10.32 m | 15.37 m |

  The bake reads DataSF first and gap-fills from Overture (which carries OSM geometry), so
  both rows bind. The safe window is therefore `4.68 < r < 6.18` if the rear building
  arrives via Overture, and `3.29 < r < 10.32` if it arrives via DataSF. **5 m satisfies
  both**, with 0.3 m of headroom over our own DataSF vertex and 1.2 m below the nearest
  neighbour. Do not raise it: at 7 m the rear building disappears and leaves a hole with
  no GLB to fill it, and at 11 m so does 123 South Park.

  **Verify empirically during the re-bake**, the way 375 Alabama and 380 Brannan were:
  procedural footprints dropped must be **exactly one**, and audit 1.6 must report no
  intrusion. If the count is 0, the radius is under our own ring and must go up; if it is
  2 or more, it is eating a neighbour and must come down.

- `loadRadius`: the skill's default formula gives `max(2500, 8.5 * 30) = 2500` m. Beyond
  that radius the carved-out site is a gap, but an 8.5 m building at 2.5 km is far below a
  pixel, so the absence is illegible. Take the default.

- **`camera` is not optional** — `context.mjs` bakes it straight into
  `context/landmarks.json` and `camera.js` reads `preset.yaw` unconditionally, so omitting
  it stops the whole city booting (see the note on `542PresidioBlvd`). `camera.js` places
  the eye at `target + distance * (sin yaw, ., cos yaw)` with `+x` east and `+z` south, so
  to face the north-west front the camera must stand to the north-west: **yaw 225**.
  Suggested `{ distance: 150, yaw: 225, pitch: 26 }` — between 543 Presidio's 120 at
  9.55 m and 542's 200 at 10.6 m.

- **This is the third one-off SoMa block in the manifest** (after 380 Brannan and 550
  Third) and the concern raised in 380 Brannan's 2.13 now has three data points: a
  manifest of individual warehouses will not stream well. If South Park is going to be
  built out address by address, the kit/instancing route
  (`KIT-INTEGRATION-PROMPT.md`) is the better long-term home for buildings of this class,
  and that decision should be taken before the fourth.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Bounding-box top exactly 8.5 m (loader scale lands at 1.0)
- [ ] Dimensions plausible in meters and consistent with 2.1 (XY bbox ~34.3 × 25.8 m is expected)
- [ ] The rear yard is a real void in the exported geometry, not a filled recess
- [ ] No openings anywhere on the north-east party wall
- [ ] Triangles at or under 8,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the roof monitor and a few front windows; glow shells proud of opaque glazing
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (per-object signed volume for the union of solids; ray test residual <= 0.15%)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + contact sheet + night render regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed, with the facade's
      confirmed/unconfirmed status stated explicitly

### 2.15 Open questions and risks

- **The facade is unverified, and that is this dossier's dominant risk.** No photograph of
  135 South Park's own street elevation was located (see the note at the end of 2.2).
  Everything in 2.4's north-west paragraph, the bay counts in 2.7 step 3, and the choice of
  `Toy_brick` in 2.8 are typological reasoning from the building's 1925 date, its Industrial
  assessor class, its unreinforced-masonry parapet permit, and the material language of
  380 Brannan on the same block. They are *plausible*, not *established*. The executing
  agent must find street-level photography before committing to the front, and must say
  in `REPORT.md` which of these it confirmed and which it did not. AGENTS rule 5 makes
  massing accuracy non-negotiable; it does not license inventing a facade and presenting
  it as researched.

- **No OSM `height` tag at all** — unusually, this building escapes the trap the plans
  README warns about, because there is no tag to be misled by. Every height here comes
  from the 2010 DataSF LiDAR: deck mode 7.06 m, median 6.95 m, maximum 8.52 m. The
  neighbouring OSM height tags (123 → 7, 115/117 → 7, 101 → 6) corroborate the deck
  reading independently, and no permit since 1999 suggests the building has changed.

- **Is 8.52 m a roof monitor or just the parapet?** A 7.06 m deck with a 0.9–1.1 m parapet
  lands at 7.9–8.2 m; 8.52 m is only 0.3 m above that, so the LiDAR maximum alone cannot
  distinguish the two. The aerial resolves it in favour of a raised element — there is a
  distinct lighter plane with its own shadow across the deep wing, far wider than a
  parapet line — but at 0.12 m/px that reading is *inferred*, and whether the element is
  **glazed** (a monitor) or **solid** (a mechanical penthouse) is not resolved at all.
  It does not change the target height either way: 8.5 m is the crest whatever the thing
  is. It changes the design completely, because the glazed reading is the asset's entire
  identity cue and its night state. **Confirm it, and if it turns out to be a solid
  penthouse, say so and re-plan the night state around the front windows instead.**

- **Storey count conflict, resolved.** The 1990 parapet permit records 1 existing storey;
  the 1986 permit and all 19 assessor rolls record 2, and a 7.0 m deck is two ~3.4 m
  industrial floors. The 1990 figure is almost certainly clerical — a parapet permit has
  no reason to survey the building. **Build 2 storeys.**

- **DataSF and OSM disagree about the rear boundary.** The DataSF polygon (432.1 m²)
  extends ~7 m further south-east than the OSM polygon (383.1 m²), into what the aerial
  shows as the open courtyard. The two centroids agree to 0.6 m, so this is not a
  registration error — it is DataSF's 2010 trace including something (a canopy, a shed,
  a since-demolished rear structure) that OSM's later trace does not. **Model the OSM
  footprint**: it matches the aerial, and the LiDAR's `hgt_mincm` of 1.05 m over the
  DataSF polygon is consistent with a low structure or open ground in exactly that
  overshoot area, which also explains why the LiDAR mean (6.04 m) sits well below its
  median (6.95 m).

- **The rear yard is measured in plan but not in section.** Whether the notch is open to
  the ground, a first-floor-only setback with the upper storey oversailing, or a roofed
  single-storey infill is unresolved — the aerial shows a lower, darker surface there but
  cannot say how low. Modelling it as a full-height void is the safe choice: it is right
  at the roof (which is what the camera sees) and defensible at ground level.

- **The exclusion radius has almost no margin.** See 2.13. This is the tightest window in
  the registry and it must be verified against the actual re-bake, not assumed.

- No architect is recorded for the 1925 building in any source consulted, and the
  building carries no name.
