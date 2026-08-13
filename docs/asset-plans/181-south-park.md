# 181 South Park — SF-SIM asset plan

A 2002 four-storey live/work loft building on the south-west rim of South Park, and one of
the strangest lots in SoMa: a 43 m long, 13.8 m wide slab that runs the full depth of the
block from the park frontage back to the Varney Place alley. It is the tallest thing on its
side of the oval by about 5 m, and it is the building Instagram was working out of on the
day Facebook bought them. Not a monument — a *character* building, and its character is
its proportion: a thin, tall sliver seen end-on from the park and broadside from above.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/181-south-park/`. This document is the plan only: Part 1 is the runnable task
prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `181-south-park` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3945113, 37.7807582` (oriented-bounding-box centre, measured) |
| Target height | **16.5 m** to the roof crest; main roof/parapet 14.3 m; roof deck ~14.2 m |
| Footprint | 43.31 m (deep, NW–SE) x 13.85 m (wide); 599.9 m2, measured — a plain rectangle at bearing 135.2° |
| Triangle cap | 9,000 |
| Category | `2` (apartments — live/work lofts over ground-floor commercial) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 181 South Park GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of 181 South Park in San Francisco and deliver it
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
7. `artifacts/380-brannan/` — the closest reference implementation in scale, character and
   neighbourhood (a secondary SoMa street building one block west, same detail tier, same
   flat-roof-with-designed-furniture problem)
8. `docs/asset-plans/181-south-park.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Photo research is a hard gate on this one — do it before you model

The dossier below is unusually strong on geometry and unusually weak on appearance,
because no street-level or aerial photography could be consulted while it was written.
Every statement in 2.4 (what each side shows) and 2.8 (palette) is *inferred* and must be
replaced with observed fact before you build anything. In particular you must resolve, from
imagery, the question in 2.15 that the whole silhouette hangs on:

> The roof is flat at ~14.2 m over most of the footprint, and something reaches 16.5 m.
> Is that (a) a stair/elevator penthouse on a flat roof, or (b) a barrel-vaulted roof over
> the top-floor lofts? Listing copy for the units mentions "arched high ceilings", which
> hints at (b); the LiDAR height spread is easier to explain with (a).

Both readings give the same 16.5 m crest, so the target height is safe either way — but
they produce completely different buildings from the app's aerial camera, which is the
view that matters most. Settle it from an aerial/satellite image before modelling, and
record which you found and how in `REFERENCE.md` and `REPORT.md`.

## Must capture

- The **proportion**: a 43 m x 13.8 m slab, three times as deep as it is wide, running the
  full depth of the block. This is the building's whole identity and it must not be
  quietly squared up toward something more comfortable to model.
- Four storeys, standing ~5 m proud of every neighbour on its side of the oval
- Tall steel-sash loft windows in a regular bay rhythm on the long flanks
- A ground-floor commercial storefront at the South Park (NW) end and the residential entry
- The garage door at the Varney Place (SE) end
- The crest feature at 16.5 m, in whichever of the two forms your research establishes
- A deliberately designed roof — the camera looks down and this roof is 43 m long

## Research 181 South Park independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- All four elevations. Note that two of them are *ends*: the 13.8 m wide NW face onto
  South Park and the 13.8 m wide SE face onto Varney Place. The long faces are the
  43 m flanks.
- Aerial and roof views — this is where the crest question gets settled
- Ground-level views from South Park and from Varney Place
- Day and night appearance
- The bay count and window rhythm of the long flanks — the dossier's 10-bay reading is
  *inferred* and is the weakest number in it
- The facade material and colour, which the dossier does not know at all

Prefer architect/engineer publications, owner or institutional material,
planning and permitting documents, architectural press, geolocated photography,
and aerial/satellite imagery. Never rely on a single photograph, a single
AI-generated image, or a single unsourced 3D model. Separate verified facts from
visual inference; if sources disagree, document the disagreement and decide.

**One source conflict is already known and resolved in 2.1 — re-check it, do not silently
re-inherit the wrong value:** OSM tags `height=14` on this building, which is the LiDAR
*median* roof height, not the crest. The crest is 16.5 m. The assessor roll is also useless
for storeys here (it records the seven condominium units separately, at 0, 1 and 2 storeys
each); the 2000 construction permit says **four storeys** and is authoritative.

## Create a reference dossier

Write `artifacts/181-south-park/REFERENCE.md` containing: source links and what each
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
one identity cue carried hard — the slab proportion and the extra storey that lifts it
above its neighbours. Resist adding hero-tier ornament.

The finished asset must be immediately recognizable as 181 South Park, consistent with
the real building from all four sides and above, architecturally credible, and a
premium handcrafted miniature — not photorealistic, not voxel art, not generic
low-poly, and never accurate in one view while invented in the others.

## Scope of the exported asset

Export the single 2002 loft block: body, all four elevations' openings, the roof and its
furniture, the crest feature, and the ground-floor storefront and garage door.

Do not include unrelated surrounding city geometry: South Park itself, the park's trees or
lawn, Varney Place, 171 South Park next door, the Shell station across the flank, the
sidewalk, parked cars, people, plinths, cameras or lights. Temporary context may appear in
review renders but must not leak into the GLB.

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
(`placeGeneric` in `app/src/assets.js` only scales and positions). The South Park entrance
end faces **northwest, bearing 315.2°**; the building's long axis runs 135.2°/315.2°, so
build directly on the measured footprint rectangle in 2.3 rather than modelling an
axis-aligned box and rotating it. The contract's "front faces −Y" cannot be honoured
literally here; real-world orientation wins (AGENTS rule 5) and the deviation goes in
`REPORT.md`.

**Height normalization:** the tallest geometry in the export (the crest feature) must
land at exactly **16.5 m** so the loader's `targetHeightM / measuredHeight` scale is 1.0.

## Reproducible Blender workflow

Blender 5.2 LTS. Headless: `blender -b --python script.py -- args`.

Keep `artifacts/181-south-park/build_181_south_park.py` (deterministic build script),
`artifacts/181-south-park/181-south-park.blend`, and
`artifacts/181-south-park/181-south-park.glb`. The script must rebuild the model reliably
enough for future revision. Do not modify or rename an unrelated existing GLB to satisfy
the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`181-south-park-top.png`, `181-south-park-north.png`, `181-south-park-east.png`,
`181-south-park-south.png`, `181-south-park-west.png`, plus
`181-south-park-contact-sheet.png`, at least one high three-quarter aerial beauty render
`181-south-park-aerial.png`, and a night render `181-south-park-aerial-night.png`.

The four elevations must share scale, framing, lighting, exposure and
projection; use orthographic or long-lens cameras; label directions from the
researched orientation; the top view must clearly show the full 43 m roof — its parapet
ring, its crest feature and its mechanical layout; the aerial view uses the style bible's
camera assumptions (30-50 degrees down, long lens). Simple tabletop lighting, neutral warm
background, minimal depth of field, and every image must depict the same exported model.

Because the building is rotated ~45° from the world axes, the four compass renders will
each show two faces at 45°. That is correct and expected — do not rotate the model to make
the elevations square on.

## Validate the exported GLB

Re-import `181-south-park.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture
count, camera count, light count, animation count, applied-transform status,
negative-scale status, normal-orientation status, unexpected geometry, and
per-material contract compliance. Render at least one review image from the
re-imported asset. Write `artifacts/181-south-park/validation.json` and
`artifacts/181-south-park/REPORT.md`.

Note that the axis-aligned XY bounding box will be roughly **40 x 40 m** even though the
building is 43.3 x 13.9 m — that is the expected consequence of a ~45° real-world heading,
not a scale error.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "181-south-park",
  "file": "181-south-park.glb",
  "anchor": [
    -122.3945113,
    37.7807582
  ],
  "targetHeightM": 16.5,
  "cat": 2,
  "name": "181 South Park",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a separate, explicitly requested job — run `docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in `docs/asset-plans/181-south-park.md`.
````

---

## Part 2 — Research and design dossier

Compiled 12 August 2026 from the sources in 2.2. Values marked *inferred* are visual or
derived estimates, not published figures — the executing agent must re-verify
anything it relies on.

**A warning specific to this dossier.** No street-level or aerial imagery could be
consulted while writing it: Google Maps and Street View were unreachable from the
authoring session, and no open street-imagery substitute covered the block. Everything
geometric here is measured from survey data and is solid. Everything *visual* — facade
material, colour, window rhythm, roof furniture, the form of the crest — is inference from
permit records and listing copy and is flagged as such. Section 2.4 in particular is a
hypothesis, not an observation. Treat photo research as gate zero of stage 2.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Built | 2000–2002; construction permit completed 24 Dec 2002 | SF building permit 200005099501 |
| Storeys | **4** | permit 200005099501 "erect a four story, five unit live/work loft"; permit 200112145293 "a new 4-story live/work bldng"; every permit 2006–2022 records `number_of_existing_stories = 4` |
| Assessor storey count | 0, 1 and 2 across the seven condo lots | SF Assessor roll — **not a building storey count**, see 2.15 |
| Replaced | a two-storey warehouse/office building, demolished under permit 200005099504 | SF building permits |
| Construction | wood frame (Type V) over a garage level | permits (`wood frame (5)`; the 2002 exit revision records `constr type 4`) |
| Programme | 5 live/work loft units above ground-floor office/retail, plus a garage | permits 200005099501, 200209106108, 200211131341 |
| Condominium lots | 7 (block 3775, lots 172–178), all addressed 181 South Park | SF Assessor secured roll 2025, DataSF parcels |
| Floor area | 15,516 sq ft total across the seven lots (8,631 commercial + 6,885 residential) | SF Assessor secured roll 2025 |
| Construction cost | $2,300,000 | permit 200005099501 |
| Roof | **unoccupied** — a roof deck was designed and then removed by revision | permit 200108166212 "change roof deck to unoccupied roof" |
| Garage | exits to Varney Place at the SE end | permit 200211131341 "exit from garage to varney" |
| Block / lot | 3775 / 172 (map block lot) | SF Assessor, DataSF parcels, DataSF footprint `mblr = SF3775172` |
| Footprint | 43.31 m x 13.85 m, 599.9 m2, a plain rectangle at bearing 135.2° | OSM way/124889463, reprojected — **measured** |
| DataSF footprint (cross-check) | 42.35 x 13.66 m OBB, 535.3 m2 polygon | DataSF LiDAR footprint SF3775172 — agrees within ~1 m per side; its 42 vertices are LiDAR edge jitter on the same rectangle |
| Main roof height | 14.18 m above ground (median), 14.28 m (majority of cells) | DataSF LiDAR `hgt_mediancm` / `hgt_majoritycm` — **measured** |
| Maximum feature height | 16.54 m above ground | DataSF LiDAR `hgt_maxcm` — **measured**; its *form* is unresolved, see 2.15 |
| Ground elevation | 6.84 m (NAVD88) | DataSF LiDAR `gnd_min_m` — app terrain handles this, not the asset |
| Height above neighbours | ~5 m: 171 South Park 11 m, 167 unknown, 159 5 m, Shell canopy 4 m, 147 12 m | OSM `height` tags on the neighbouring ways |
| Notable occupant | Instagram, 2012 — the office they were in when Facebook announced the acquisition on 9 April 2012 | Getty Images news photo, 9 April 2012; commercial listing copy |
| Zoning | SPD (SoMa — South Park) | DataSF parcels |
| Architect | not recorded in any source consulted | — |

### 2.2 Sources

- https://www.openstreetmap.org/way/124889463 — footprint rectangle, address, `height=14`
- `https://data.sfgov.org/resource/ynuv-fyni` (DataSF Building Footprints, LiDAR-derived) — cross-check footprint and the 14.18 m / 16.54 m heights
- `https://data.sfgov.org/resource/acdm-wktn` (DataSF Parcels) — the seven 181 South Park condo lots, zoning
- `https://data.sfgov.org/resource/wv5m-vpq2` (SF Assessor Historical Secured Property Tax Rolls) — 2002 build year, per-unit use and floor area
- `https://data.sfgov.org/resource/i98e-djp9` (SF Building Permits) — the 2000 four-storey five-unit construction permit, the demolition it replaced, the roof-deck-to-unoccupied-roof revision, the Varney garage exit, the ground-floor change of use, and the 2006–2022 four-storey record
- https://www.gettyimages.com/detail/news-photo/instagrams-new-office-is-seen-at-181-south-park-avenue-on-news-photo/142617135 — Instagram at this address, 9 April 2012
- Commercial and residential listing copy (Zillow, Redfin, Homes.com "Park 181", ApartmentList) — 5 loft units, 2002, "arched hardwood high ceilings", "towering steel-framed windows", downtown skyline views, former Instagram offices

### 2.3 Orientation and placement

The lot runs the full depth of the block, from the south-west rim of the South Park oval
back to the Varney Place alley. It shares its north-east long wall with 171 South Park;
its south-west long wall faces the open forecourt of the Shell station on Third Street and
is therefore an exposed elevation, not a party wall.

Measured distances from the footprint edge: the South Park sidewalk 1.9 m off the NW end,
the South Park roadway centreline 10.6 m, the park boundary 15.1 m; Varney Place 2.7 m off
the SE end.

The footprint is a clean rectangle. OSM way/124889463 records it with eight nodes, but six
of them are collinear — the real shape is four corners:

Rectangle corners in Blender coordinates (metres, `+X` east, `+Y` north),
centred on the anchor `-122.3945113, 37.7807582`:

```
( -20.255,  10.322)   NW corner, west side
( -10.443,  20.082)   NW corner, north side
(  20.250, -10.327)   SE corner, east side
(  10.438, -20.088)   SE corner, south side
```

in ring order: `(-10.443, 20.082) → (-20.255, 10.322) → (10.438, -20.088) → (20.250, -10.327)`.

Edges, with outward normals:

| Edge | Length | Faces | Elevation |
|---|---|---|---|
| `(-10.443,20.082) -> (-20.255,10.322)` | 13.85 m | NW 315.2° | **South Park front** |
| `(-20.255,10.322) -> (10.438,-20.088)` | 43.31 m | SW 225.2° | **exposed south-west flank** |
| `(10.438,-20.088) -> (20.250,-10.327)` | 13.85 m | SE 135.2° | **Varney Place end (garage)** |
| `(20.250,-10.327) -> (-10.443,20.082)` | 43.31 m | NE 45.2° | north-east flank, party wall with 171 |

Because of the 45° heading the axis-aligned bounding box is ~40 x 40 m. That is correct.

### 2.4 What each side shows — *inferred, verify before modelling*

Nothing in this section is observed. It is the most probable reading of a 2002 SoMa
live/work loft building given the permit record, the programme and the neighbourhood, and
it exists so that stage 2 has something specific to confirm or overturn.

**Northwest (South Park front)** — The address elevation and the only one the park sees:
13.85 m wide and 16.5 m tall, so a distinctly vertical face. Expect a ground-floor
commercial storefront (the 8,631 sq ft commercial condo) with a large glazed shopfront and
a separate recessed residential entry door, then three loft levels of tall steel-sash
windows — the listings' "towering steel-framed windows", probably two wide bays per floor
on a face this narrow. This is the face that would carry the street number.

**Southeast (Varney Place end)** — The service end. A vehicle garage door (permits confirm
the garage exits here), a pedestrian exit door, and a plainer, more closed upper wall than
the park front. Alleys in SoMa are working faces.

**Southwest flank** — 43 m long, four storeys, and *exposed*: the Shell station forecourt
means there is no neighbour against it. Expect the building's main window rhythm here —
a long regular run of loft windows, probably with a lightwell or setback somewhere along
its length, because a 43 m deep floor plate cannot be lit from its two ends alone. From
the app's aerial camera this is the largest single surface the asset presents.

**Northeast flank** — Party wall against 171 South Park for most of its length, so in the
real world it is largely blind and only its upper storey clears the neighbour's 11 m roof.
The app's camera sees it plainly from the north-east, so it must be built as a finished
wall with a sparse, honest window scatter in the part that clears 171 — not a full grid,
and not a blank slab either.

**Top** — 43 x 13.8 m of unoccupied roof at ~14.2 m, plus whatever reaches 16.5 m. No roof
deck (permit 200108166212), so no railings, planters or paving: a membrane roof with a
parapet ring, mechanical units, and the crest feature. This is the most-seen surface in the
app and it is a long one — it needs a deliberate composition along its length, not one
object dropped in the middle.

### 2.5 Recognition cues (ranked)

1. **The proportion** — a 43 x 13.8 m slab, 3.1:1, running the whole depth of the block
   from the park to the alley. Nothing else on this side of South Park is shaped like it.
2. **The extra storey** — four storeys where the neighbours are two and three, standing
   about 5 m proud of the roofline on both sides.
3. Tall steel-sash loft windows in a regular bay rhythm along the long flanks.
4. The crest feature at 16.5 m breaking an otherwise flat 43 m roof.
5. Ground-floor commercial storefront on the park end; garage door on the alley end.

### 2.6 Miniature translation

**Preserve**

- The 3.1:1 slab proportion and the real 135.2° heading, exactly
- The four-storey height standing proud of the neighbours — this is what makes it findable
- The two-different-ends story: shopfront and entry at the park, garage at the alley
- The long flanks' window rhythm as a rhythm, not as individual windows

**Simplify / exaggerate**

- The real window count on each 43 m flank becomes ~10 identical bays, all the same size
- Steel sashes become a single chunky frame band per opening; no mullion grids
- The storefront becomes one wide glazed opening plus one recessed entry, not a shopfitted
  facade
- Roof clutter becomes a small, composed set: two HVAC blocks, one vent cluster, the crest
  feature, and a continuous parapet ring
- The vertical proportion of the NW end is the one place semantic exaggeration is spent:
  keep the storey bands crisp and let the face read as tall and thin

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not
a straitjacket — adjust after the first aerial review render, and after the 2.15 crest
question is settled.

1. Body: extrude the 2.3 rectangle from z=0 to z=14.2, `Toy_stone`.
2. Ground floor, z=0 to z=4.3: on the NW end, one 6.0 m wide glazed storefront and one
   1.4 m recessed residential entry; on the SE end, one 3.6 m garage door (`Toy_ink`) and
   one 1.0 m pedestrian door; on the SW flank, two or three small openings only.
3. Floor band: 0.18 m `Toy_trim` course at z=4.3, carried around all four faces — it is
   what separates the commercial base from the lofts at a glance.
4. Loft levels, three of them, z=4.9 to z=13.9: on each long flank, 10 bays of
   1.5 x 2.6 m openings recessed 0.18 m, `Toy_glass`, with a 0.12 m `Toy_steel` frame band.
   On the NW end, 2 bays per floor, same size. On the NE flank, use the same rhythm but
   only above z=11 (below that it is a party wall against 171) — below, leave it blind.
5. Parapet: z=14.2 to z=14.3 following the footprint, 0.3 m thick, `Toy_trim` cap.
6. Roof deck at z=14.2, `Toy_roofd`. Two HVAC blocks (2.2 x 1.6 x 0.9 m and
   1.6 x 1.2 x 0.7 m) `Toy_steel`, placed off-centre and well apart along the 43 m length;
   one vent cluster near the SE third.
7. **Crest feature to z=16.5** — the exact geometry depends on 2.15:
   - if a penthouse: a 4.0 x 3.2 m box from z=14.2 to z=16.5, `Toy_roofd`, sitting toward
     the NW third of the roof;
   - if a barrel vault: a low 8-to-10-segment arc spanning the 13.85 m width, springing at
     z=14.2 and crowning at z=16.5, running along part or all of the length, `Toy_roofd`.

   Whichever it is, its top must land exactly on 16.5.
8. Bevel 0.12 m, 2 segments.

### 2.8 Materials and palette — *inferred, confirm from photography*

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_stone` | `#d9d2c2` | main body walls |
| `Toy_trim` | `#f3efe6` | floor band, parapet cap, entry surround |
| `Toy_glass` | `#2a4d73` | loft windows and storefront glazing |
| `Toy_steel` | `#9aa0a6` | window frame bands, HVAC blocks |
| `Toy_roofd` | `#45454a` | roof deck, crest feature |
| `Toy_ink` | `#3a3530` | garage door, door recesses |
| `Toy_glass_Glow` | `#2a4d73` | lit loft windows at night |
| `Toy_trim_Glow` | `#f3efe6` | storefront spill at the park end |

The body colour is the single largest unknown in this plan. `Toy_stone` is a safe neutral
that will sit correctly next to the neighbourhood's palette, but a 2002 SoMa loft building
is as likely to be a warmer stucco (`Toy_sand`, `#ece4d4`) or to carry a metal-panel
element. Decide from photography, and if the real building has a signature accent colour,
say so in `REPORT.md` and spend one palette slot on it — this plan deliberately does not
invent one.

**Night state (required).** Glow surfaces must be thin shells proud of the opaque glazing —
the app renders `_Glow` in a separate layer that is ~12% alpha by day, so a primary surface
must never be authored as glow. Hero glow: a scatter of lit loft windows on the exposed
south-west flank, where the long rhythm reads best — five or six of the thirty, not all.
Supporting accent: the storefront glazing at the South Park end. The north-east flank stays
dark below 11 m (it is a party wall) and the alley end stays dark entirely; a service alley
that glows would misread.

### 2.9 Top surface

43 x 13.8 m of unoccupied membrane roof at 14.2 m, in a district the camera flies over
constantly, and long enough that a single centred object would look accidental. Compose
along the length: parapet ring continuous, mechanical grouped in one place, the crest
feature somewhere off-centre, and a clear darker deck value so the parapet ring reads from
above. No deck furniture — the roof-deck permit was revoked by revision in 2001 and railings
or planters would be a fabrication.

### 2.10 Scope

**In the GLB:** the single 2002 loft block — body, all four elevations' openings, storefront
and residential entry, garage door, parapet, roof deck, roof furniture and the crest feature

**Not in the GLB:** South Park, its trees or lawn, Varney Place, 171 South Park, the Shell
station, the sidewalk, vehicles, people, plinths, cameras or lights

### 2.11 Triangle budget

Cap 9,000 — a secondary building, and the cap should bind. Suggested split: body, parapet
and floor band ~2k; the two 10-bay flanks ~3.5k; the NW end's storefront, entry and loft
bays ~1.5k; the SE end's garage and door ~0.5k; roof furniture and crest ~1.5k.

The long flanks are where this budget gets spent, so keep each bay to a simple recessed box
with one frame band. Twenty bays of a fussy window will not fit and will not read.

### 2.12 Draft manifest entry

```json
{
  "id": "181-south-park",
  "file": "181-south-park.glb",
  "anchor": [
    -122.3945113,
    37.7807582
  ],
  "targetHeightM": 16.5,
  "cat": 2,
  "name": "181 South Park",
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

- **New landmark.** Add a `pipeline/lib/landmarks.mjs` entry (`id: '181-south-park'`,
  `lon: -122.3945113`, `lat: 37.7807582`, `height: 16.5`, `exclude: 5`) and re-bake the
  affected tiles, or the baked procedural building on this exact footprint will intersect
  the GLB.
- **The exclusion radius has an unusually narrow safe window, and 5 is near its middle.**
  `excluded()` in `pipeline/buildings.mjs` drops a procedural footprint when its centroid
  *or any of its ring vertices* falls inside the radius, so the constraint is two-sided.
  Measured against the anchor above:

  | | trigger distance |
  |---|---|
  | 181 South Park's own footprint (via its centroid) | **2.02 m** |
  | 171 South Park (nearest ring vertex — a shared party-wall node) | **7.00 m** |
  | the Shell canopy at 551 (nearest ring vertex) | 9.17 m |
  | 167 South Park | 12.32 m |

  Anything in `(2.1, 7.0)` clears this building and keeps its neighbours. Below ~2.1 the
  procedural slab survives and pokes through the model; at or above 7.0 the re-bake punches
  a hole where 171 South Park should be. `exclude: 5` leaves ~3 m of tolerance for the
  difference between these OSM rings and the Overture footprints the pipeline actually
  bakes from — but that difference is exactly the risk, so **verify with `pipeline/audit.mjs`
  check 1.6 after the re-bake** and confirm visually that 171 is still standing before
  committing.
- `loadRadius`: the skill's default formula gives `max(2500, 16.5 * 30) = 2500` m. Take the
  default. Beyond it the site is a gap rather than a procedural stand-in, but at 2.5 km a
  16 m building is far below a pixel.
- This is the second South Park-area building in the landmark manifest after 380 Brannan,
  and the same question applies: a manifest of one-off SoMa blocks will not stream well
  forever. If the intent is to keep doing individual buildings around this oval, the
  kit/instancing route (`KIT-INTEGRATION-PROMPT.md`) is the better long-term home for
  buildings of this class.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Bounding-box top exactly 16.5 m (loader scale lands at 1.0)
- [ ] Dimensions plausible in meters and consistent with 2.1 (XY bbox ~40 x 40 m is expected)
- [ ] The slab is still 3.1:1 in plan — measure it, do not eyeball it
- [ ] Triangles at or under 9,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the lit loft windows and the storefront; glow shells proud of opaque glazing
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (per-object signed volume for the union of solids; ray test residual <= 0.15%)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + contact sheet + night render regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed
- [ ] The 2.15 crest question answered in `REPORT.md`, with the source that answered it

### 2.15 Open questions and risks

- **The crest at 16.5 m has an unresolved form, and it is the biggest risk in this plan.**
  The LiDAR is unambiguous that the main roof is at 14.18 m (median) / 14.28 m (majority)
  and that something reaches 16.54 m. What that something *is* was not established. Two
  readings fit:
  (a) a stair/elevator penthouse — a 2.3 m overrun is exactly standard for a four-storey
  building with a lift, and the height histogram's tight majority at 14.28 m with a thin
  tail above it is what a small penthouse looks like;
  (b) a barrel-vaulted roof over the top-floor lofts — the unit listings describe "arched
  hardwood high ceilings", and an arched ceiling on the top floor of a loft building is
  usually the underside of an arched roof.
  Against (b): a vault spanning the full 13.85 m width would put the *mean* cell height
  near 15.7 m, and the measured mean is 13.15 m. In favour of (b): the same measured mean
  is below the median either way, which means a genuinely low element exists somewhere in
  the footprint and the height statistics are not clean enough to arbitrate on their own.
  **Settle it from an aerial image before modelling.**
- **A low element exists somewhere in the footprint.** LiDAR mean 13.15 m against median
  14.18 m and minimum 0.04 m says roughly a sixth of the footprint sits well below the main
  roof. Candidates: a lightwell or setback breaking the 43 m depth (which a floor plate
  this deep needs), a single-storey rear element at the Varney end, or LiDAR shadow cast by
  171 South Park along the party wall. The first would change the massing materially. Look
  for it in the aerial.
- **OSM `height=14` is the roof, not the crest.** It matches the LiDAR median almost
  exactly, which makes it look trustworthy — the same trap the plans README documents. The
  crest is 16.5 m.
- **The assessor roll cannot be used for storeys here.** It records the seven condominium
  lots separately at 0, 1 and 2 storeys each; none of those is the building. The 2000
  construction permit and every permit since say four.
- **The entire visual reading in 2.4 and the palette in 2.8 are unverified.** No photography
  was available to the author. Facade material, colour, window rhythm, bay count, whether
  there is a signature accent, and what the roof actually carries are all open.
- The 10-bay flank rhythm is a proportion guess (43.31 m / 10 ≈ 4.3 m centres, which is a
  plausible loft bay) and nothing more.
- No architect is recorded for the 2002 building in any source consulted, so there is no
  design-intent document to check the reading against.
- The Instagram association is well sourced for April 2012 and is worth carrying in the
  building's card copy, but it must not become a visual instruction — there is no reason to
  think the building looked different then, and nothing about it should be styled to
  reference the tenant.
