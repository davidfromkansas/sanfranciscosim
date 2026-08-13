# 155 – 157 South Park Street — SF-SIM asset plan

A 1925 wood-frame flats building on the south side of the South Park oval: two residential
flats stacked over a ground floor that started life as a garage and is now a café. It is a
*character* building, not a monument — its whole read at diorama scale is a tall, narrow,
bright-white stucco box sitting on a near-black shopfront, with two sage-green window
groups and a pair of plaster lozenges as its only ornament. It is a **contributor to the
potential South Park Historic District**, which is the reason it is worth building at all:
it is one of the ten flats buildings that give the oval its scale.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/155-south-park/`. This document is the plan only: Part 1 is the runnable task
prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `155-south-park` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3942202, 37.7808993` |
| Target height | **10.1 m** to the front parapet crest; roof deck 9.25 m (measured); rear block ~7.0 m |
| Footprint | 209.3 m2, measured; through lot 8.16 x 31.22 m overall — front block ~6.2 m wide x 12.5 m deep, rear block ~8.2 m x 18 m |
| Triangle cap | 7,000 |
| Category | `1` (residential) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 155 – 157 South Park Street GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of 155 – 157 South Park Street in San Francisco and
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
7. `artifacts/380-brannan/` — the closest reference implementation: the other small
   SoMa street building in this set, one block away, same scale and same
   "memorable ordinary building" brief
8. `artifacts/543-presidio-blvd/` — the closest reference for a small residential
   building with a restrained night state
9. `docs/asset-plans/155-south-park.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Must capture

- A **three-level** box: near-black shopfront, then two floors of bright white stucco
  under a flat coped parapet. The dark base against the white body is the silhouette.
- The two **sage-green window groups**, one per upper floor — a wide centre light
  flanked by narrow sashes, in thick painted trim. Flat front, no bay windows.
- The pair of **cast-plaster diamond/lozenge rosettes** flanking the second-floor
  window — the building's only ornament and its signature.
- The **shopfront**: black awning across the full width, recessed centre entrance with
  brass doors, one display window, and the tall black security gate at the left-hand
  edge that leads to the flats.
- The **through lot**: a narrow front block on South Park stepping back to a wider,
  lower rear block that fronts the Varney Place alley with garage doors and a roof deck.
- The **skewed frontage** — the street edge is ~6 degrees off the party walls because
  South Park Street curves around the oval. Do not square it up.

## Research 155 – 157 South Park Street independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- The South Park (northwest) elevation in detail — window proportions, the rosettes'
  size and position, the shopfront's divisions
- The Varney Place (southeast) rear elevation, which this dossier is weakest on
- Aerial and roof views: the front block's flat roof, the step down to the rear block,
  the rear roof deck and its lattice screen
- Day and night appearance; the ground-floor tenancy is a café/bakery and the warm
  shopfront glow is the intended night state
- Whether the front parapet has a raised centre bay (the dossier reads one, *inferred*)

Prefer architect/engineer publications, owner or institutional material,
planning and permitting documents, architectural press, geolocated photography,
and aerial/satellite imagery. Never rely on a single photograph, a single
AI-generated image, or a single unsourced 3D model. Separate verified facts from
visual inference; if sources disagree, document the disagreement and decide.

**Two source conflicts are already known and resolved in 2.1 — re-check them, do not
silently re-inherit the wrong value:** the SF Assessor roll says **2 stories** and every
photograph shows **three levels** (the assessor counts the two residential flats and not
the converted ground-floor garage — build three levels); and OSM `height=9` together with
the LiDAR *median* 8.87 m describes the roof **deck**, not the crest — the parapet is
above it and the target height is 10.1 m.

## Create a reference dossier

Write `artifacts/155-south-park/REFERENCE.md` containing: source links and what each
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

This is a **background building** in the style bible's detail budget (§21) — one step
below 380 Brannan, and two below a hero landmark. Two clean volumes, one strong window
rhythm, a plainly designed roof, and exactly two identity cues carried hard: the dark
shopfront base and the plaster lozenges. Resist adding ornament the real building does
not have; a 1925 SoMa flats building is deliberately modest, and that modesty is the
point next to the warehouses around it.

The finished asset must be immediately recognizable as 155 – 157 South Park Street,
consistent with the real building from all four sides and above, architecturally
credible, and a premium handcrafted miniature — not photorealistic, not voxel art, not
generic low-poly, and never accurate in one view while invented in the others.

## Scope of the exported asset

Export the single through-lot property: the three-level front flats block, the lower
rear block, the shopfront, the parapets, the roof surfaces and the rear roof deck.

Do not include unrelated surrounding city geometry: South Park Street, the South Park
oval and its trees, Varney Place, the neighbouring buildings at 147 and 159 South Park,
sidewalks, bike racks, parked cars, people, plinths, cameras or lights. Temporary context
may appear in review renders but must not leak into the GLB.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary
`.glb`; real-world meters; origin at base center; minimum geometry Z ~ 0;
applied transforms; no negative scales; outward normals; no duplicate or foreign
geometry; no image textures; no transparency; flat-color materials named `Toy_*`
from the project palette; `_Glow` suffix only on surfaces that glow at night; no
`Toy_body`; no cameras, lights, animations, armatures or constraints; no external
dependencies; at most 7,000 triangles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model
drops into the city at its real-world heading — the loader applies no rotation
(`placeGeneric` in `app/src/assets.js` only scales and positions). The South Park
entrance front faces **north-northwest, bearing 327.2°**; the party walls run
140.8° / 320.8°. The lot is rotated roughly 41° off the world axes, so build directly on
the measured footprint polygon in 2.3 rather than modelling an axis-aligned box and
rotating it. Record the measured heading in `REPORT.md`.

**Height normalization:** the tallest geometry in the export (the front parapet crest)
must land at exactly **10.1 m** so the loader's `targetHeightM / measuredHeight` scale is
1.0.

## Reproducible Blender workflow

Blender 5.2 LTS. Headless: `blender -b --python script.py -- args`.

Keep `artifacts/155-south-park/build_155_south_park.py` (deterministic build script),
`artifacts/155-south-park/155-south-park.blend`, and
`artifacts/155-south-park/155-south-park.glb`. The script must rebuild the model reliably
enough for future revision. Do not modify or rename an unrelated existing GLB to satisfy
the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`155-south-park-top.png`, `155-south-park-north.png`, `155-south-park-east.png`,
`155-south-park-south.png`, `155-south-park-west.png`, plus
`155-south-park-contact-sheet.png`, at least one high three-quarter aerial beauty render
`155-south-park-aerial.png`, and a night render `155-south-park-aerial-night.png`.

The four elevations must share scale, framing, lighting, exposure and
projection; use orthographic or long-lens cameras; label directions from the
researched orientation; the top view must clearly show the parapet ring, the step down to
the rear block, the rear roof deck and the roof furniture; the aerial view uses the style
bible's camera assumptions (30-50 degrees down, long lens). Simple tabletop lighting,
neutral warm background, minimal depth of field, and every image must depict the same
exported model.

Note that this building is unusually long and thin — 31 m by 8 m. Frame the elevation
cameras to the long axis, not to a square, or the four views will not be comparable.

## Validate the exported GLB

Re-import `155-south-park.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture
count, camera count, light count, animation count, applied-transform status,
negative-scale status, normal-orientation status, unexpected geometry, and
per-material contract compliance. Render at least one review image from the
re-imported asset. Write `artifacts/155-south-park/validation.json` and
`artifacts/155-south-park/REPORT.md`.

Note that the axis-aligned XY bounding box will be roughly **26 x 29 m** even though the
building is 8.2 x 31.2 m — that is the expected consequence of a ~41° real-world heading,
not a scale error.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "155-south-park",
  "file": "155-south-park.glb",
  "anchor": [
    -122.3942202,
    37.7808993
  ],
  "targetHeightM": 10.1,
  "cat": 1,
  "name": "155 South Park",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a separate, explicitly requested job — run `docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in `docs/asset-plans/155-south-park.md`.
````

---

## Part 2 — Research and design dossier

Compiled 12 August 2026 from the sources in 2.2. Values marked *inferred* are visual or
derived estimates, not published figures — the executing agent must re-verify
anything it relies on.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Built | **1925** | SF Assessor secured roll, block 3775 lot 030 (consistent 2020-2025); SF Planning South Park Historic District DPR form |
| Historic status | **Contributor** to the potential South Park Historic District; CHRSC status code `5D3` | SF Planning / Page & Turnbull DPR 523D, 30 June 2009 |
| DPR property type | "HP3. Multiple Family Property; HP6. 1-3 Story Commercial Building" | same |
| Building type | Residential **flats** — 2 units — over a ground floor **converted from a garage to commercial** | DPR form (Integrity section names 155 South Park explicitly); SF Assessor `number_of_units = 2` |
| Levels | **3** (commercial ground + 2 residential floors) | street-level photography, Jan 2025 |
| Assessor storey count | 2 | SF Assessor roll — **not contradicted, differently scoped**: it counts the two flats, see 2.15 |
| Construction | Wood frame (assessor construction type `D`) | SF Assessor roll |
| Block / lot / APN | 3775 / 030 (APN 3775-030) | SF Assessor; DataSF building footprints (`mblr = SF3775030`) |
| Zoning | `SPD` (South Park District) | SF Assessor roll |
| Assessor floor area | 2,350 sq ft over a 2,443 sq ft lot | SF Assessor roll — this is the *flats*, not the whole through-lot mass, see 2.15 |
| Footprint | **209.3 m2**; through lot, overall OBB 8.16 x 31.22 m; 82.1% rectangular fill | DataSF LiDAR building footprint (`ynuv-fyni`), reprojected — **measured** |
| OSM footprint (cross-check) | 206.6 m2, OBB 8.18 x 31.21 m | OSM way/124889488 — agrees with DataSF within ~1.3% |
| Roof deck height (front block) | **9.25 m** above ground | DataSF LiDAR `hgt_majoritycm = 925` (the modal height cell) — **measured** |
| LiDAR median height | 8.87 m | DataSF `hgt_median_m` — median across the whole through lot, so it sits between the taller front block and the lower rear |
| LiDAR max | 16.23 m | DataSF `hgt_maxcm` — the South Park street tree overhanging the frontage, **not** the building |
| Front parapet crest | ~10.1 m | *inferred*, roof deck + ~0.85 m parapet read from the frontage photograph |
| Rear block roof | ~7.0 m | *inferred* from the Varney Place photograph and the LiDAR mean/median spread |
| Ground elevation | 8.23 m (NAVD88) | DataSF LiDAR `gnd_min_m` — the app terrain handles this, not the asset |
| Frontage heading | front faces **327.2° (NNW)**; party walls run 140.8° / 320.8° | measured from the footprint polygon |
| Current ground-floor tenant | Flour & Branch (bakery), registered 17 Feb 2026 at "155 South Park St Bldg A" | SF Registered Business Locations (`g8m3-pdis`) |
| Previous tenants | The Velvet Raven (chocolate / wine bar / café), signage in place Jan 2025; before that The Butler & The Chef Bistro at 155A, closed end of 2017 | Street-level photography; press coverage |
| Neighbours | 147 South Park (NE, modern replacement building, 2010s) and 159 South Park (SW, 1907 industrial, non-contributing) — party walls both sides | DPR form contributor/non-contributor tables; photography |

### 2.2 Sources

- `https://www.openstreetmap.org/way/124889488` — footprint, `addr:housenumber = 155;157`, `addr:street = South Park`, `height = 9`
- `https://data.sfgov.org/resource/ynuv-fyni` (DataSF Building Footprints, LiDAR-derived) — authoritative footprint polygon and the 8.87 m median / 9.25 m modal heights
- `https://data.sfgov.org/resource/wv5m-vpq2` (SF Assessor Historical Secured Property Tax Rolls) — 1925, block/lot, storeys, units, floor area, construction type, zoning
- `https://data.sfgov.org/resource/g8m3-pdis` (SF Registered Business Locations) — the current ground-floor tenant and the "Bldg A" suffix that confirms more than one structure on the lot
- `https://default.sfplanning.org/GIS/SouthSoMa/Docs/2009-06-30_South%20Park%20Dform.pdf` — SF Planning / Page & Turnbull, *South Park Historic District*, DPR 523D continuation sheets, 30 June 2009: contributor status, property type, the flats typology, and the explicit note that this building's ground-floor garage was converted to commercial space while the upper floors stayed residential
- Google Street View, South Park Street pano (capture Jan 2025) — the whole front elevation: white stucco, sage-green window groups, plaster lozenges, black shopfront, security gate, parapet
- Google Street View, Varney Place pano (capture Jan 2025) — the alley and the rears of the row; the salmon-stucco rear block with garage doors and a lattice-screened roof deck
- Google Maps satellite (Vexcel imagery, 2026) — flat roofs, the step down from front block to rear block, the rear deck and garden
- `https://en.wikipedia.org/wiki/South_Park,_San_Francisco` — the oval's history and 550-foot plan, context only

### 2.3 Orientation and placement

The building occupies a **through lot** on the south-east side of the South Park oval: it
fronts South Park Street to the north-west and backs onto the Varney Place alley to the
south-east, with party walls on both long sides. Like the whole SoMa grid it is rotated
about 41° from the world axes, and because South Park Street curves around the oval the
street edge is skewed about 6° relative to the party walls.

Measured footprint polygon, in Blender coordinates (metres, `+X` east, `+Y` north),
counter-clockwise, already centred on the anchor `-122.3942202, 37.7808993`:

```
( -6.66,  13.70)   <- street corner, NE side
( -6.46,  13.46)
(  1.24,   4.02)
( -0.10,   2.81)   \
(  0.44,   2.16)    |  small NE light well, 1.8 x 0.85 m
(  1.83,   3.38)   /
( 13.03,  -8.62)
(  8.12, -13.66)   <- Varney Place rear
( -5.03,  -0.46)
( -3.78,   0.60)   <- SW wall steps in: rear block is wider than the front block
( -6.21,   4.47)   \
( -7.34,   3.40)    |  SW light well / chimney notch, 1.55 m
( -2.10,  15.61)   <- street corner, SW side
( -8.91,  12.00)
```

(The list above is the survey ring reordered for readability; the authoritative version is
the DataSF ring for `mblr = SF3775030`, and the executing agent should re-pull it rather
than retype these numbers.)

Read in a frame aligned to the lot's long axis, where `+v` points toward the street:

| Zone | `v` range | Width across the lot | What it is |
|---|---|---|---|
| Front block | +3.0 to +15.6 (12.6 m deep) | ~6.2 m | the three-level flats building on South Park |
| Rear block | -15.6 to +3.0 (18.6 m deep) | ~8.2 m | the lower rear structure fronting Varney Place |

Edges, with outward normals:

| Edge | Length | Faces | Elevation |
|---|---|---|---|
| street end | ~6.2 m | NNW 327.2° | **South Park Street front** |
| NE party wall | ~29 m (in two runs) | NE 50.8° | 147 South Park |
| Varney end | ~7.0 m | SSE 147.2° | **Varney Place rear** |
| SW party wall | ~29 m (in three runs) | SW 230.8° | 159 South Park |

Because of the 41° heading the axis-aligned bounding box is ~26 x 29 m for an 8 x 31 m
building. That is correct.

### 2.4 What each side shows

**North-north-west (South Park Street front)** — The hero elevation, and the only one with
any design in it. Top to bottom: a plain coped parapet with what reads as a slightly raised
centre bay (*inferred*); a smooth **bright white / off-white stucco** wall carrying two
**sage-green (celadon) window groups**, one per floor, each a wide fixed centre light
flanked by narrow double-hung sashes in thick painted trim with a shallow sill apron; a
pair of **cast-plaster diamond / lozenge rosettes** set into the stucco either side of the
second-floor group; then a horizontal break, and below it the ground floor, which is a
**near-black painted timber shopfront** with fine copper/orange pinstripe lines outlining
its panels, a black fabric awning running the full width, a recessed centre entrance with
brass-handled double doors under a transom, one display window to the left of the entrance
and a smaller one to the right, and at the far left a tall **black wrought-iron security
gate** over the passage to the flats, with the "155 / 157" address plate on it. The right
edge of the facade carries a downpipe and a run of ivy.

**South-south-east (Varney Place rear)** — Two storeys of **salmon / peach painted
stucco**, blunt and utilitarian, with a pair of white roll-up garage doors at alley level,
a painted pilaster strip between them, and above the roof a **diagonal-lattice screen**
enclosing a roof deck. Varney Place is barely 5 m wide, so in the real world this face is
only ever seen at an extreme oblique — but the app's aerial camera reads it plainly, so it
must be built properly.

**North-east / south-west flanks** — Party walls. Blank stucco with a couple of light-well
returns (the two notches in 2.3) and nothing else. Do not invent a window grid; the
neighbours are hard up against them on both sides.

**Top** — Two flat roofs at different heights: the front block's plain membrane roof inside
its parapet ring at ~9.25 m, then a step down to the rear block's roof at ~7.0 m, part of
which is a **timber roof deck behind the lattice screen**, with a small stair bulkhead and
a scatter of vents. Between the two blocks, at the side steps, sits a strip of planting /
light well visible from above. This is the surface the app's camera sees most — design it,
do not leave it flat.

### 2.5 Recognition cues (ranked)

1. **Near-black shopfront under a bright white box** — the value contrast is the entire
   silhouette at diorama scale, and no neighbour on the oval has it
2. Tall, narrow, flat-fronted three-level stucco block on a very deep lot
3. The two **sage-green window groups**, thick-trimmed, one per upper floor
4. The **pair of plaster lozenges** flanking the second-floor window
5. The step down to a lower salmon rear block with an alley garage and a roof deck

### 2.6 Miniature translation

**Preserve**

- Three distinct levels with a clearly taller ground floor
- The white body / black base split, carried all the way to the party-wall corners
- The sage-green window colour — it is the second-strongest colour note after the black
- The two-block through-lot massing and the real 41° heading with its 6° skewed frontage

**Simplify / exaggerate**

- The window groups become one three-part opening per floor, identical, with a single
  chunky 0.25 m frame — no muntins, no sash rails
- The lozenges are enlarged to ~0.9 m across and given 0.1 m relief so they survive at
  thumbnail size; this is the one place semantic exaggeration is spent
- The shopfront becomes: one awning slab, one recessed entrance with a brass door panel,
  one display window, one gate panel. The copper pinstriping becomes a single thin trim
  line along the awning fascia, or is dropped if it reads as noise
- Ivy, downpipe, signage lettering and the address plate all disappear
- The rear lattice screen becomes a solid slab with a coarse cut-out pattern or, if that
  costs more than ~300 triangles, a plain screen wall
- Roof clutter becomes one stair bulkhead, one vent cluster and one skylight

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not
a straitjacket — adjust after the first aerial review render.

1. Rear block: extrude the rear portion of the 2.3 footprint (`v` from -15.6 to +3.0,
   full 8.2 m width) from z=0 to z=7.0, `Toy_sand` tinted toward peach (see 2.8).
2. Front block: extrude the front portion (`v` from +3.0 to +15.6, ~6.2 m wide) from z=0
   to z=9.25, `Toy_white`. Keep the skewed street edge.
3. Ground floor, z=0 to z=3.8, front block only: a `Toy_ink` shopfront panel inset 0.1 m
   into the white wall across the full frontage, with a 0.9 m deep recessed entrance bay
   at the centre (brass door panel `Toy_gold`, z=0 to z=2.4), a 2.0 x 1.6 m display window
   `Toy_glass` to its left, and a 1.1 m wide `Toy_steel` gate panel at the NE end.
4. Awning: a 0.35 m thick `Toy_roofd` slab at z=3.5, projecting 1.1 m, full frontage width.
5. Second floor, z=4.2 to z=6.55: one three-part opening 3.6 x 1.9 m, recessed 0.2 m,
   `Toy_glass`, in a 0.25 m proud `Toy_verdigris` frame with a 0.15 m sill.
6. Lozenges: two `Toy_trim` diamonds ~0.9 m across, 0.1 m proud, centred at z=5.6, set
   0.5 m outboard of the second-floor frame on each side.
7. Third floor, z=6.9 to z=9.05: the same opening and frame, repeated.
8. Front parapet: z=9.25 to z=**10.1**, following the front-block footprint, 0.3 m thick,
   `Toy_white` with a `Toy_trim` cap; a slightly raised centre bay over the middle third
   sets the bounding-box top and must land exactly on 10.1.
9. Front roof deck at z=9.25, `Toy_roofd`, with one vent cluster (2 blocks, ~0.6 m tall).
10. Rear block roof at z=7.0, `Toy_roofd`: a timber deck panel `Toy_rust` over the outer
    two-thirds, a 1.1 m lattice screen wall `Toy_trim` along the Varney edge and the two
    flanks, one stair bulkhead 2.2 x 1.6 m to z=7.9, one skylight `Toy_glassl`.
11. Varney elevation, z=0 to z=3.4: two 2.4 x 2.9 m `Toy_steel` roll-up doors with a
    0.4 m `Toy_trim` pilaster between them.
12. Bevel 0.12 m, 2 segments.

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_white` | `#f7f4ec` | front block stucco, front parapet |
| `Toy_sand` | `#ece4d4` | rear block walls (see the note below) |
| `Toy_trim` | `#f3efe6` | parapet cap, the two lozenges, lattice screen, Varney pilaster |
| `Toy_ink` | `#3a3530` | the shopfront panel, entrance recess |
| `Toy_gold` | `#caa64a` | brass entrance doors, awning fascia trim line |
| `Toy_verdigris` | `#9fb8a8` | the sage-green window frames and sills |
| `Toy_glass` | `#2a4d73` | all windows and the display window |
| `Toy_glassl` | `#6f95b8` | rear roof skylight |
| `Toy_roofd` | `#45454a` | awning slab, both roof decks |
| `Toy_steel` | `#9aa0a6` | security gate, Varney roll-up doors |
| `Toy_rust` | `#a86444` | the timber roof-deck boards on the rear block |
| `Toy_gold_Glow` | `#caa64a` | the lit café shopfront at night |
| `Toy_glass_Glow` | `#2a4d73` | two or three lit flat windows at night |

Note on the rear block: the real colour is a warm salmon/peach with no exact palette match.
`Toy_sand` is too pale and `Toy_coral` (`#e8735a`) far too saturated for a whole wall.
Off-palette is a WARN not a FAIL, so a dedicated `Toy_peach` at roughly `#e0a98c` is
permissible if the render justifies it. Decide from the aerial render and record the
decision in `REPORT.md`.

**Night state (required).** Glow surfaces must be thin shells proud of the opaque glazing —
the app renders `_Glow` in a separate layer that is ~12% alpha by day, so a primary surface
must never be authored as glow. Hero glow: the **café shopfront** — the display window and
the recessed entrance, warm gold, reading as the one lit thing on a dark residential
street. Supporting accent: two or three lit windows in the flats above, cool, and not all
of them. The rear block does not glow; a service alley that lights up would misread.

### 2.9 Top surface

Two flat roofs at different heights on a very long thin lot, in a district the camera flies
over constantly. Keep the front parapet ring clearly lighter than the deck inside it so the
ring reads from above; keep the rear deck's timber boards warm so the step down is legible
as a *use*, not as a mistake; and let the lattice screen cast the only interesting shadow
on the whole roof. Nothing else — this building's roof was never designed, and inventing a
mechanical farm on it would be a lie about a 1925 flats building.

### 2.10 Scope

**In the GLB:** the through-lot property — front flats block, shopfront, front parapet and
roof, rear block, Varney elevation, rear roof deck and lattice screen

**Not in the GLB:** South Park Street, the oval and its trees, Varney Place, 147 and 159
South Park, sidewalk, bike racks, vehicles, people, plinths, cameras or lights

### 2.11 Triangle budget

Cap 7,000 — a background building one step below 380 Brannan (7,760 tris shipped), and the
cap should bind. Suggested split: two block volumes and parapets ~1.5k, the two upper
window groups and frames ~1.5k, shopfront and awning ~1.5k, rear block openings and deck
~1.5k, lozenges and roof furniture ~1k.

### 2.12 Draft manifest entry

```json
{
  "id": "155-south-park",
  "file": "155-south-park.glb",
  "anchor": [
    -122.3942202,
    37.7808993
  ],
  "targetHeightM": 10.1,
  "cat": 1,
  "name": "155 South Park",
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

- **New landmark.** Add a `pipeline/lib/landmarks.mjs` entry (`id: '155SouthPark'`,
  `lon: -122.3942202`, `lat: 37.7808993`, `height: 10.1`) and re-bake the affected tiles,
  or the baked procedural building on this exact footprint will intersect the GLB.
- **The exclusion radius must be very tight.** This is a party-wall row on 6-8 m frontages:
  the nearest neighbour centroids (147 and 159 South Park) sit only ~7.1 m and ~7.9 m from
  this anchor. Start at `exclude: 6` and run the same drop-count check 380 Brannan
  documents — the re-bake must drop **exactly one** procedural footprint. The usable band
  is roughly 2-6 m; anything at or above ~7 m starts taking the neighbours out and punches
  a hole in the row, which on this block is far more visible than the building itself.
- A `camera` preset is optional for a building this small; if one is added,
  `{ distance: 170, yaw: 147, pitch: 26 }` looks back at the front from over the oval.
- `loadRadius`: the skill's default formula gives `max(2500, 10.1 * 30) = 2500` m. Take
  the default, as 380 Brannan and 550 Third did.
- This is the third one-off SoMa street building in the manifest after 380 Brannan and
  550 Third, and the first that is a *residential* one. The open question raised in
  380 Brannan's 2.13 stands and gets sharper here: a manifest of individual South Park
  row buildings would not stream well, and the kit/instancing route
  (`KIT-INTEGRATION-PROMPT.md`) is probably the right long-term home for this class.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Bounding-box top exactly 10.1 m (loader scale lands at 1.0)
- [ ] Dimensions plausible in meters and consistent with 2.1 (XY bbox ~26 x 29 m is expected)
- [ ] Triangles at or under 7,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the shopfront and two or three upper windows; glow shells proud of opaque glazing
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (per-object signed volume for the union of solids; ray test residual <= 0.15%)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + contact sheet + night render regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

- **Storey count, resolved.** The SF Assessor roll says 2 storeys and 2 units; the 2009
  DPR form says the ground-floor garage was converted to commercial while the upper floors
  stayed residential; the Jan 2025 photograph plainly shows three levels. These agree once
  you notice the assessor is counting *dwelling* floors. **Build three levels**, with the
  ground floor clearly taller than the two above it.
- **The assessor's 2,350 sq ft is not the whole mass.** 218 m2 of floor area against a
  209 m2 footprint would be less than one full floor over the through lot, which is
  obviously wrong for a three-level front block. The figure describes the flats; the rear
  block and the ground-floor commercial space are assessed or recorded separately (the
  business registration's "155 South Park St **Bldg A**" is the same signal). Do not use
  it to derive floor heights or a storey count.
- **OSM `height=9` and the LiDAR median 8.87 m both describe the roof deck**, and they are
  close enough to each other to look like corroboration. They are not the crest. This is
  the trap the plans README warns about, and the same one 543 Presidio Blvd fell into.
  The modal LiDAR cell, 9.25 m, is the better roof-deck figure; the parapet is above it.
- **The front parapet crest, 10.1 m, is the weakest number in this dossier.** It is roof
  deck (measured) plus a parapet height read off a single street-level photograph. So is
  the raised centre bay. Re-verify both before normalising the export; if the parapet turns
  out to be flat and lower, the target height moves and the manifest entry with it.
- **The rear block is the weakest *evidence* in this dossier.** It was identified by
  elimination along Varney Place — the blue corrugated building at 62 Varney Pl is the rear
  of the modern 147 South Park, which puts the salmon-stucco rear with the garage doors and
  the lattice-screened deck on lot 030. That inference is good but it is an inference, and
  its ~7.0 m height is a visual estimate. Confirm it before modelling.
- **The front block is only ~6.2 m wide** while the rear is ~8.2 m. That is measured, and
  it is the correct read of a narrow South Park frontage on a lot that widens behind the
  neighbours' side yards — but it makes the front elevation tighter than the photograph
  intuitively suggests, so double-check the widths against the survey before laying out the
  window groups.
- **The skewed frontage is real and easy to lose.** The street edge is ~6° off the party
  walls because South Park Street curves. Squaring it up is the most likely way for this
  model to end up looking subtly wrong in the row.
- No architect or builder is recorded for the 1925 building in the DPR form or in any other
  source consulted; several other South Park buildings in the same document do name theirs.
