# 156 South Park Street — SF-SIM asset plan

A 1924 reinforced-concrete warehouse on the north-west side of the South Park oval: a tall
two-storey street bar in front of a long single-storey top-lit shed that runs the whole
depth of the block to Taber Place. Built for a drayage firm, occupied by **The Anchor
Packing Co. from about 1933 to about 1982**, converted from warehouse to offices under a
2019 permit, and since June 2023 the San Francisco studio of the architects Multistudio.

It is worth building for one specific reason. The 2009 Page & Turnbull survey of the
potential South Park Historic District looked at twenty-three contributing buildings and
found that every one of them had been altered — except this one. *"The building that
appears to be unaltered is 156 South Park Street."* It is the district's control sample:
the plainest thing on the oval and the only one still saying exactly what it said in 1924.

At diorama scale its whole read is a flat slate blue-grey wall, two big fields of small
steel-sash panes stacked one above the other, and a run of saw-tooth skylight monitors
marching away from the street across a roof the camera looks straight down on.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/156-south-park/`. This document is the plan only: Part 1 is the runnable task
prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `156-south-park` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3948748, 37.7813535` |
| Target height | **8.7 m** to the front parapet crest; rear shed roof ~5.7 m (measured) |
| Footprint | 260.3 m2, measured; through lot 32.3 m long — a tapering strip, 5.9 m wide at South Park widening to 9.8 m mid-lot, ending in a 7.9 m obliquely-cut wall on Taber Place |
| Triangle cap | 6,000 |
| Category | `3` (office) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 156 South Park Street GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of 156 South Park Street in San Francisco and
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
7. `artifacts/155-south-park/` — the closest reference implementation: the other narrow
   party-wall building on this same oval, same scale, same "memorable ordinary building"
   brief, and the same skewed-frontage problem
8. `artifacts/380-brannan/` — the closest reference for a SoMa industrial building with a
   restrained night state
9. `docs/asset-plans/156-south-park.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Must capture

- **Two masses, not one.** A tall two-storey **street bar** on South Park, and behind it a
  long, wider, single-storey **shed** running back to Taber Place. The step down between
  them is the building's real shape and the thing an aerial camera reads first.
- The **uniform slate blue-grey** paint. One colour over the whole street elevation —
  wall, window frames, glazing bars, sills, parapet cap and door alike. There is no base
  course, no trim colour, no contrasting shopfront. That flatness *is* the building.
- The **two stacked fields of small steel-sash panes** on the street front: a tall
  ground-floor shopfront window with a dense grid of panes, and above it a near
  full-width upper ribbon of the same industrial sash. They are the only openings and
  they carry the whole facade.
- The **entrance bay** at the north-east edge of the frontage: a small flat pale canopy
  over a recessed flush door, the numerals **156** on the wall beside it, and two black
  cylindrical sconces stacked on the narrow pier between door and window.
- The **X-shaped steel star tie anchors** at the parapet line — the visible ends of the
  1990 parapet reinforcing. Two of them, high on the wall. They are small, they are the
  only ornament this building has, and they read as deliberate at miniature scale.
- The **skylight monitors** on the rear shed roof — a run of raised boxes stepping away
  from the street. The camera looks down; this is the roof's design, not clutter.
- The **tapering plan**. The lot is 5.9 m wide at South Park, widens steadily to 9.8 m
  about two thirds of the way back, then narrows slightly to a 7.9 m end wall on Taber
  Place that is cut ~19° off square. Over 32.3 m that is a visible taper. Do not build a
  rectangle.

## Research 156 South Park Street independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the depth of the two-storey front bar, the footprint, the WGS84
anchor, and the real-world orientation, and gather references covering:

- The South Park (east-south-east) elevation in detail — the pane grids' true counts, the
  canopy, the sconces, the numerals, the star anchors
- The Taber Place (west-north-west) rear elevation, which this dossier is weakest on
- Aerial and roof views: the parapet ring on the front bar, the step down to the shed,
  the skylight monitors' number and spacing, any mechanical plant
- Day and night appearance; the building is an architecture studio, and warm interior
  light through the two big sash fields is the intended night state
- **Where the two-storey front bar ends and the single-storey shed begins** — this is the
  single most important open question in the dossier, see 2.15

Prefer architect/engineer publications, owner or institutional material,
planning and permitting documents, architectural press, geolocated photography,
and aerial/satellite imagery. Never rely on a single photograph, a single
AI-generated image, or a single unsourced 3D model. Separate verified facts from
visual inference; if sources disagree, document the disagreement and decide.

**One source conflict is already known and resolved in 2.1 — re-check it, do not silently
re-inherit the wrong value:** OSM tags this building `height=6` and the DataSF LiDAR
*median* is 5.67 m, which agree with each other and are both wrong for the street front.
They describe the **single-storey rear shed**, which is most of the footprint. The
two-storey street bar reaches the LiDAR maximum, **8.74 m**, and that is the target
height. This is exactly the trap `docs/asset-plans/README.md` warns about.

## Create a reference dossier

Write `artifacts/156-south-park/REFERENCE.md` containing: source links and what each
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

This is a **background building** in the style bible's detail budget (§21) — the same
tier as 155 South Park across the oval, one below 380 Brannan, two below a hero landmark.
Two clean volumes, two window fields, a designed roof, and exactly two identity cues
carried hard: the flat monochrome wall and the skylight monitor run.

The discipline this particular building demands is **subtraction**. A 1924 warehouse for a
drayage company was built with no ornament at all, and the 2023 conversion added none —
it painted everything one colour. The temptation will be to give it a base course, a
contrasting cornice, or a lit shopfront to make it "read". Resist all three. Its
plainness next to the Victorians and flats on the same oval is the whole point, and it is
the reason the survey singled it out.

The finished asset must be immediately recognizable as 156 South Park Street,
consistent with the real building from all four sides and above, architecturally
credible, and a premium handcrafted miniature — not photorealistic, not voxel art, not
generic low-poly, and never accurate in one view while invented in the others.

## Scope of the exported asset

Export the single through-lot property: the two-storey front bar, the single-storey rear
shed, the parapets, the roof surfaces, the skylight monitors and the entrance canopy.

Do not include unrelated surrounding city geometry: South Park Street, the South Park
oval and its trees, Taber Place, the neighbouring buildings at 150 and 158–160 South
Park, sidewalks, parked cars, people, plinths, cameras or lights. Temporary context may
appear in review renders but must not leak into the GLB.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary
`.glb`; real-world meters; origin at base center; minimum geometry Z ~ 0;
applied transforms; no negative scales; outward normals; no duplicate or foreign
geometry; no image textures; no transparency; flat-color materials named `Toy_*`
from the project palette; `_Glow` suffix only on surfaces that glow at night; no
`Toy_body`; no cameras, lights, animations, armatures or constraints; no external
dependencies; at most 6,000 triangles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model
drops into the city at its real-world heading — the loader applies no rotation
(`placeGeneric` in `app/src/assets.js` only scales and positions). The South Park
entrance front faces **east-south-east, bearing 117.3°**; the Taber Place rear faces
**316.3°**; the party wall with 150 runs at bearing ~24.9° outward, the party wall with
158–160 at ~193.6°/229.9°. The lot sits at roughly 45° to the world axes, so build
directly on the measured footprint polygon in 2.3 rather than modelling an axis-aligned
box and rotating it. Record the measured heading in `REPORT.md`.

**Height normalization:** the tallest geometry in the export (the front parapet crest)
must land at exactly **8.7 m** so the loader's `targetHeightM / measuredHeight` scale is
1.0.

## Reproducible Blender workflow

Blender 5.2 LTS. Headless: `blender -b --python script.py -- args`.

Keep `artifacts/156-south-park/build_156_south_park.py` (deterministic build script),
`artifacts/156-south-park/156-south-park.blend`, and
`artifacts/156-south-park/156-south-park.glb`. The script must rebuild the model reliably
enough for future revision. Do not modify or rename an unrelated existing GLB to satisfy
the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`156-south-park-top.png`, `156-south-park-north.png`, `156-south-park-east.png`,
`156-south-park-south.png`, `156-south-park-west.png`, plus
`156-south-park-contact-sheet.png`, at least one high three-quarter aerial beauty render
`156-south-park-aerial.png`, and a night render `156-south-park-aerial-night.png`.

The four elevations must share scale, framing, lighting, exposure and
projection; use orthographic or long-lens cameras; label directions from the
researched orientation; the top view must clearly show the front bar's parapet ring, the
step down to the shed, and the full run of skylight monitors; the aerial view uses the
style bible's camera assumptions (30-50 degrees down, long lens). Simple tabletop
lighting, neutral warm background, minimal depth of field, and every image must depict
the same exported model.

Note that this building is long, thin and tapering — 32.3 m by 5.9-9.8 m. Frame the
elevation cameras to the long axis, not to a square, or the four views will not be
comparable. The top view is the most informative one for this asset; give it room.

## Validate the exported GLB

Re-import `156-south-park.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture
count, camera count, light count, animation count, applied-transform status,
negative-scale status, normal-orientation status, unexpected geometry, and
per-material contract compliance. Render at least one review image from the
re-imported asset. Write `artifacts/156-south-park/validation.json` and
`artifacts/156-south-park/REPORT.md`.

Note that the axis-aligned XY bounding box will be roughly **30 x 24 m** even though the
building is a 32.5 m wedge — that is the expected consequence of a ~45° real-world
heading, not a scale error.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "156-south-park",
  "file": "156-south-park.glb",
  "anchor": [
    -122.3948748,
    37.7813535
  ],
  "targetHeightM": 8.7,
  "cat": 3,
  "name": "156 South Park",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a separate, explicitly requested job — run `docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in `docs/asset-plans/156-south-park.md`.
````

---

## Part 2 — Research and design dossier

Compiled 16 August 2026 from the sources in 2.2. Values marked *inferred* are visual or
derived estimates, not published figures — the executing agent must re-verify
anything it relies on.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Built | **1924** | SF Assessor secured roll, block 3775 lot 066 (consistent 2013-2025); SF Planning South Park Historic District DPR form narrative |
| Historic status | **Contributor** to the potential South Park Historic District; CHRSC status code `5D3` | SF Planning / Page & Turnbull DPR 523D, 30 June 2009, contributor table row `3775066 / 156 / SOUTH PARK / HP8. Industrial / 1924 / 5D3` |
| DPR property type | "HP8. Industrial" | same |
| Integrity | **The only one of the district's 23 contributors the survey found unaltered** | DPR form, Integrity section: *"The building that appears to be unaltered is 156 South Park Street."* |
| Building type | Small **reinforced concrete warehouse** | DPR form: *"156 South Park Street (1924) is an example of a small reinforced concrete warehouse at South Park."*; SF Assessor construction type `C` |
| Architectural style | 20th Century Commercial / simple utilitarian | DPR form, industrial buildings typology section |
| Contractor | **J.A. Bryant**, for **J.J. Welter & Co., draymen** | DPR form, builders section — no architect is recorded |
| Historic occupant | **The Anchor Packing Co., ca. 1933 – ca. 1982** | DPR form, occupants table; Multistudio's own site names the studio "formerly the Anchor Packing Co." |
| Levels | **2**, plus a partial mezzanine | SF Assessor `number_of_stories = 2`; DBI permits 2019-2023 repeatedly say "existing 2 / proposed 2" and reference an existing mezzanine; DPR: district industrial buildings "are only two stories in height" |
| Current use | Architecture studio (offices) — Multistudio's SF studio, opened **June 2023** | DBI permit 2019-07-10 "change of use from warehouse to office"; multi.studio; SF registered business locations |
| Block / lot / APN | 3775 / 066 (APN 3775-066) | SF Assessor; DataSF building footprints (`mblr = SF3775066`) |
| Zoning | `SPD` (South Park District) | SF Assessor roll |
| Assessor areas | 2,688 sq ft property over a 2,688 sq ft lot (249.7 m2) | SF Assessor roll — see the caution in 2.15 |
| Footprint | **260.3 m2**; through lot, 32.3 m along the long axis; **5.92 m** frontage on South Park, widening to a maximum **9.8 m** about two thirds back, then a **7.94 m** end wall on Taber Place cut ~19° off square | DataSF LiDAR building footprint (`ynuv-fyni`, `mblr = SF3775066`), reprojected — **measured** |
| OSM footprint (cross-check) | 263.2 m2; frontage edge 6.92 m | OSM way/124884346 — agrees with DataSF within ~1.1% |
| Front bar parapet crest | **8.74 m** above ground | DataSF LiDAR `hgt_maxcm = 874` — **measured**, and the tallest point on the lot |
| Rear shed roof | **5.66 m** | DataSF LiDAR `hgt_majoritycm` (modal cell) and `hgt_median_m = 5.67` — **measured**; most of the footprint sits here |
| LiDAR mean / std | 6.14 m / 1.14 m | DataSF `hgt_meancm`, `hgt_stdcm` — the arithmetic that splits the two masses, see 2.15 |
| OSM `height` (cross-check) | **6** | OSM way/124884346, Bing-sourced — this describes the *shed*, not the crest. Do not use it as the target height |
| Ground elevation | 6.69 m (NAVD88) | DataSF LiDAR `gnd_min_m` — the app terrain handles this, not the asset |
| Frontage heading | front faces **117.3° (ESE)**; rear faces **316.3° (WNW)** | measured from the footprint polygon |
| Neighbours | **150 South Park** (NE, APN 3775-065, **1959**, status `6L` — a *non*-contributor) and **158 / 160 South Park** (SW, APN 3775-067, **1924**, `5D3` contributor). Party walls both sides | DPR contributor/non-contributor tables; Jan 2025 street-level photography |
| Retrofit history | 1990 **parapet reinforcing** permit; 2003 reroofing; 2019 change of use warehouse→office; 2021 accessible entrance; 2022 new modified-bitumen Class A roof + new steel stair to second floor; 2023 interior tenant improvement | SF DBI permits (`i98e-djp9`), block 3775 lot 066 |

### 2.2 Sources

- `https://www.openstreetmap.org/way/124884346` — footprint, `addr:housenumber = 156`,
  `addr:street = South Park`, `addr:source:housenumber = survey`, `height = 6`
- `https://data.sfgov.org/resource/ynuv-fyni` (DataSF Building Footprints, LiDAR-derived)
  — authoritative footprint polygon for `mblr = SF3775066` and the 5.66 m modal / 8.74 m
  maximum heights that split the two masses
- `https://data.sfgov.org/resource/wv5m-vpq2` (SF Assessor Historical Secured Property Tax
  Rolls) — 1924, block/lot, two storeys, industrial use, construction type `C`, `SPD`
  zoning, areas
- `https://data.sfgov.org/resource/i98e-djp9` (SF DBI Building Permits) — the 1990 parapet
  reinforcing, the 2019 warehouse→office change of use (PA 201907105483), the 2022 roof
  and steel stair, the 2023 fit-out, and the repeated "2 storeys + mezzanine" statements
- `https://default.sfplanning.org/GIS/SouthSoMa/Docs/2009-06-30_South%20Park%20Dform.pdf`
  — SF Planning / Page & Turnbull, *South Park Historic District*, DPR 523D continuation
  sheets, 30 June 2009 (53 pp): contributor table, the "small reinforced concrete
  warehouse" description, the J.A. Bryant / J.J. Welter attribution, the Anchor Packing
  Co. tenancy, the district period of significance (1854–1935), and the Integrity finding
  that this is the district's only unaltered contributor
- `https://www.multi.studio/studios/san-francisco` — *"Our current studio, formerly the
  Anchor Packing Co., is located in the historic South Park neighborhood of SoMa"*;
  confirms the address as 156 South Park Street, 94107
- `https://www.multi.studio/perspective/perspective/multistudio-welcomes-greg-johnson-to-lead-san-francisco-studio`
  — *"In June 2023, Multistudio San Francisco opened the doors to its new home in the
  South Park neighborhood"*
- Google Street View, South Park Street pano (capture **Jan 2025**), viewed from
  `37.78120, -122.39465` at headings 310°–318° — the whole front elevation: slate
  blue-grey wall, the two steel-sash fields, the entrance bay with canopy and numerals,
  the paired sconces, the star anchors, and both neighbours for comparison
- Esri World Imagery (z20) with the DataSF parcel footprints overlaid, and Google Maps
  satellite (Vexcel 2026, z21–z22) — the flat roof, the skylight monitor run, the step to
  150's lower roof, and confirmation that 156's roof shadow falls onto 150
- `https://en.wikipedia.org/wiki/South_Park,_San_Francisco` — the oval's history and plan,
  context only

Exa searches run (`web_search_advanced_exa`): *"156 South Park San Francisco building
Multistudio office"* and *"Anchor Packing Company building South Park San Francisco
Multistudio studio renovation 2023"*, 8 results each with summaries. Productive domains:
`multi.studio` (the Anchor Packing Co. identification and the June 2023 opening date),
`opengovus.com` (the tenancy chain at this address — Zack/De Vito Architecture 2003,
Randy Thueme Design 2007, Zero Ten Design 2012-2021, Multistudio from May 2023),
`sfdesignweek.org`. **Exa found no photographs of the building's exterior and no
architectural description of it** — every result was a business listing or a firm news
post. The exterior evidence in this dossier is Street View, aerial imagery and the DPR
form, not press coverage. Nothing was found on J.A. Bryant either; the DPR form says the
same.

### 2.3 Orientation and placement

The building occupies a **through lot** on the north-west side of the South Park oval: it
fronts South Park Street to the east-south-east and backs onto the Taber Place alley to
the west-north-west, with party walls on both long sides. Like the whole SoMa grid it is
rotated about 45° from the world axes, and because South Park Street curves around the
oval the lot is a **wedge** — narrow at the street, wide at the alley.

Measured footprint polygon, in Blender coordinates (metres, `+X` east, `+Y` north),
already centred on the anchor `-122.3948748, 37.7813535`:

```
(  -0.14,   5.46)   <- party wall with 150, street end
(   4.00,   0.31)
(  15.69,  -5.11)
(  15.83,  -5.16)   <- SOUTH PARK corner, north-east side
(  13.12, -10.42)   <- SOUTH PARK corner, south-west side
(  -1.59,  -6.88)   \  party wall with 158-160, kink
( -13.17,   6.89)   /
( -13.91,   7.64)   <- TABER PLACE corner, south-west side
(  -8.16,  13.12)   <- TABER PLACE corner, north-east side
```

(The authoritative version is the DataSF ring for `mblr = SF3775066`, and the executing
agent should re-pull it rather than retype these numbers.)

Read in a frame aligned to the lot's long axis, where `+v` points toward South Park:

| Zone | `v` range (approx) | Width across the lot | What it is |
|---|---|---|---|
| Front bar | +10 to +16.4 (~6.4 m deep) | 5.9 → 7.2 m | the two-storey street building — **depth is *inferred*, see 2.15** |
| Rear shed | -15.9 to +10 (~26 m deep) | 7.2 → 9.8 → 7.9 m | the single-storey top-lit warehouse running back to Taber Place |

Edges, with outward normals:

| Edge(s) | Length | Faces | Elevation |
|---|---|---|---|
| street end | 5.92 m (6.92 m in OSM) | ESE 117.3° | **South Park Street front** |
| NE party wall | 19.6 m in three runs | NNE 21-51° | 150 South Park |
| SW party wall | 34.2 m in three runs | SSW/SW 194-230° | 158 – 160 South Park |
| Taber end | 7.94 m | WNW 316.3° | **Taber Place rear** |
| Taber end, NE return | 11.09 m | NE 43.7° | open rear yard behind 140-150 |

Because of the ~45° heading the axis-aligned bounding box is ~30 x 24 m for a 32.5 m
wedge. That is correct.

### 2.4 What each side shows

**South Park (ESE) front — the only well-documented elevation.** A flat, unbroken plane
of slate blue-grey painted render over concrete, two storeys, capped by a plain parapet
with a slim projecting cap and no cornice. From the Jan 2025 pano, north-east to
south-west:

- a narrow entrance bay at the north-east edge: a small flat pale canopy (a shallow shed
  hood, the only non-grey element on the building), a recessed dark flush door with a
  vertical pull, an intercom plate and a mail slot, a tall narrow slot window beside it,
  and the numerals **156** on the wall
- a narrow pier carrying **two black cylindrical wall sconces, stacked vertically**
- the **ground-floor sash field**: one very large steel-sash window, a dense grid of small
  panes (read as roughly 6 columns x 5 rows) in a lightly projecting frame on a heavy
  sill, occupying about two thirds of the frontage, with the word **multistudio** applied
  in small white letters low on the right-hand glass
- above a blank spandrel band, the **upper sash ribbon**: the same industrial sash running
  nearly the full width, read as roughly 8 columns x 4 rows of panes, slightly recessed
  with a plain sill and lintel band
- a broad blank wall band above the ribbon, then the parapet, with **two X-shaped steel
  star tie anchors** set high — the visible ends of the 1990 parapet reinforcing
- service clutter that should **not** be modelled: a downpipe, a CCTV dome, conduit runs

Everything on this elevation — sash frames, glazing bars, sills, door, parapet cap — is
painted the same slate blue-grey as the wall. Only the canopy (pale) and the sconces
(black) break it.

**Taber Place (WNW) rear — weak evidence.** Street View coverage of the alley is partial
and shot from close range against the wall. What the nearest pano shows for this row is a
blue-grey painted industrial wall with multi-pane steel windows and a large roll-up
garage door, which is exactly the type this building would present to a service alley,
but it could not be attributed to this lot with confidence. **Treat the rear elevation as
unverified** and re-shoot it. A drayage warehouse's alley end almost certainly has a
vehicle door; do not invent detail beyond that.

**Party walls (NE and SW).** Both are shared, blind, and invisible in the city. Model
them as plain closed walls. The step down from the front bar to the shed happens on both.

**Roof — the important one.** Flat throughout, a dark grey membrane (the 2022 modified
bitumen). The front bar carries a parapet ring. The rear shed carries a run of **raised
skylight monitors** — pale boxes stepping away from the street down the length of the
lot, clearly legible in both Esri and Vexcel imagery. Aerial imagery also shows 156's
roof shadow falling onto **150's lower roof**, confirming this building is the taller of
the two despite 150 being the newer one.

### 2.5 Recognition cues (ranked)

1. **One colour, two grids.** A flat slate blue-grey wall carrying two stacked fields of
   small steel-sash panes and nothing else. No base, no trim, no cornice.
2. **The skylight monitor run** on the long single-storey roof behind — the identity cue
   the app's aerial camera actually sees.
3. **The step** from a tall two-storey street bar to a low wide shed.
4. **The entrance bay**: pale canopy, recessed dark door, `156`, two stacked sconces.
5. **The X star anchors** high on the parapet.

### 2.6 Miniature translation

The style bible's conversion is unusually easy here and unusually easy to overdo. The
real building is already a toy: two boxes, two window grids, one colour. The work is
almost entirely in *proportion* and *roof design*, not in ornament.

- Keep the monochrome. Give the wall one `Toy_*` slate blue-grey and let the window
  fields be a single darker graphical field each, in the style bible's dark blue-gray
  window colour, with a chunky mullion grid modelled as a few relieved bars — not 30
  individual panes.
- Exaggerate the **pane grid density** slightly rather than the pane size: the read is
  "industrial sash", and that read comes from many small squares.
- Exaggerate the **step** between bar and shed by a few percent so the aerial silhouette
  is unmistakable.
- Exaggerate the **monitors** — make them a touch taller and a touch more regular than
  reality, because they are the roof's only event and the camera looks down.
- Do **not** exaggerate the canopy, the sconces or the anchors. They are small on purpose.
- Semantic exaggeration stops at the property line: the wedge, the heading and the
  heights are real (AGENTS rule 5).

### 2.7 Massing recipe

1. Extrude the measured wedge polygon (2.3) to 5.66 m — this is the shed, and it is most
   of the building.
2. Cut the front ~6 m of the lot (street end) and raise it to 8.34 m, then add a 0.36 m
   parapet ring on top of it to reach **8.7 m**. Re-verify this split first (2.15).
3. Add the parapet cap as a thin proud band on the street elevation only.
4. Recess the two sash fields ~0.12 m into the front wall; model the mullion grid as
   relieved bars, one bar per column and row, not as individual glazed panes.
5. Recess the entrance bay ~0.25 m; add the flat canopy as a thin slab, the door as a
   flush panel, the numerals as a small proud plate.
6. Add two small proud X plates high on the front wall.
7. Lay the skylight monitors across the shed roof: a regular run of low boxes with a
   sloped glazed face, aligned to the long axis, stepping back from the front bar.
8. Close the party walls and the Taber Place end flat. One vehicle door recess at the
   alley end, no more.

### 2.8 Materials and palette

| Material | Where | Notes |
|---|---|---|
| `Toy_wall_slate` | every external wall, parapet, party walls, rear | one flat desaturated blue-grey; this is the building |
| `Toy_trim_pale` | entrance canopy, `156` plate | the only light element on the elevation |
| `Toy_window_dark` | sash fields, mullion grid, vehicle door | the style bible's dark blue-gray graphical window |
| `Toy_roof_dark` | roof membrane, parapet top | darker than the wall, matte |
| `Toy_metal_black` | sconces, star anchors | small, black |
| `Toy_window_dark_Glow` | the two street sash fields at night | see below |
| `Toy_skylight_Glow` | the monitors' glazed faces | supporting accent, dimmer than the street fields |

**Night state.** This is an architecture studio, so the hero glow is **warm interior light
behind the two big sash fields** — the ground-floor field brighter than the upper ribbon.
The supporting accent is a faint spill from the skylight monitors, which reads beautifully
from the aerial camera and is the reason to bother modelling them properly. Nothing else
glows: no shopfront band, no sconce glow, no parapet wash. Follow the README's
"drive `_Glow` from Base Color, not from the imported emission" note, and keep the day
colours of the `_Glow` materials matched to their non-glow neighbours.

### 2.9 Top surface

The roof is the primary surface for this asset. Design it: dark membrane, a clean parapet
ring over the front bar, the monitor run stepping away down the shed, and a small amount
of restrained plant near the step. Keep the monitors regularly spaced and aligned to the
lot's long axis — a ragged run reads as noise from above, a regular one reads as
architecture.

### 2.10 Scope

In: the front bar, the rear shed, parapets, roof, monitors, entrance canopy, sash fields,
sconces, star anchors, one rear vehicle door.

Out: South Park Street and the oval, Taber Place, the neighbours at 150 and 158-160,
sidewalks, street trees, vehicles, people, signage beyond the `156` numerals and the small
`multistudio` lettering (which may be omitted entirely — it is a tenancy, not the
building).

### 2.11 Triangle budget

| Element | Budget |
|---|---|
| Shed volume + party walls + rear | 700 |
| Front bar volume + parapet ring + cap | 700 |
| Two sash fields with mullion grids | 2,200 |
| Skylight monitors (run of ~7) | 1,400 |
| Entrance bay, canopy, door, numerals | 400 |
| Sconces, star anchors, vehicle door | 350 |
| Slack | 250 |
| **Total** | **6,000** |

155 South Park landed at 4,048 triangles for a comparable building; 6,000 is a ceiling,
not a target.

### 2.12 Draft manifest entry

```json
{
  "id": "156-south-park",
  "file": "156-south-park.glb",
  "anchor": [
    -122.3948748,
    37.7813535
  ],
  "targetHeightM": 8.7,
  "cat": 3,
  "name": "156 South Park",
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

- **New landmark.** Add a `pipeline/lib/landmarks.mjs` entry (`id: '156SouthPark'`,
  `lon: -122.3948748`, `lat: 37.7813535`, `height: 8.7`) and re-bake the affected tiles,
  or the baked procedural building on this exact footprint will intersect the GLB.
- **The exclusion radius must be very tight, and tighter than 155's neighbourhood
  suggests.** Measured against neighbour *vertices*, not centroids: the nearest vertex of
  150 South Park's footprint is **4.02 m** from this anchor and the nearest vertex of
  158-160's is **7.06 m**. `exclude` must stay **below 4 m** or the re-bake eats 150.
  Start at `exclude: 3` — the same value 155 South Park settled on — and run the drop-count
  check that 380 Brannan documents: the re-bake must drop **exactly one** procedural
  footprint. Punching a hole in this row is far more visible than the building itself.
- A `camera` preset is optional at this size; if one is added,
  `{ distance: 170, yaw: 297, pitch: 26 }` looks back at the front from over the oval.
- `loadRadius`: the default formula gives `max(2500, 8.7 * 30) = 2500` m. Take the default,
  as 155 South Park, 380 Brannan and 550 Third did.
- **Batch it.** This is now the eighth individual South Park row building with a plan. A
  Case B re-bake rewrites ~600 generated files whatever the landmark was, so this must go
  through `docs/asset-pipeline/BATCH-INTEGRATE.md` rather than committing a bake of its
  own. The concern first raised in 380 Brannan's 2.13 — that a manifest of individual
  South Park row buildings does not stream well and the kit/instancing route is the right
  long-term home for this class — now applies to eight buildings on one oval and should be
  decided before a ninth.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Bounding-box top exactly 8.7 m (loader scale lands at 1.0)
- [ ] Dimensions plausible in meters and consistent with 2.1 (XY bbox ~30 x 24 m is expected)
- [ ] Triangles at or under 6,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the two street sash fields and the monitor glazing; glow shells proud of opaque glazing
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (per-object signed volume for the union of solids; ray test residual <= 0.15%)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + contact sheet + night render regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

- **Where the two-storey bar ends is the weakest number in this dossier, and it is the one
  that shapes the model.** The split is *derived*, not observed. The DataSF LiDAR gives
  mean 6.14 m over 260.3 m2 with a modal cell at 5.66 m and a maximum of 8.74 m; solving
  `A_front x 8.74 + (260.3 - A_front) x 5.66 = 260.3 x 6.14` puts only **~41 m2** at the
  taller level, which against a 5.9-9 m width is a front bar barely **6 m deep**. The
  median (5.67 m) independently says the tall part is under half the footprint, so the
  upper bound is ~130 m2 and ~15 m deep. Both ends of that range are architecturally
  plausible for the type. Re-verify from an oblique aerial or a roof view before
  modelling; if it turns out deeper, the massing changes but the 8.7 m target height does
  not.
- **OSM `height=6` and the LiDAR median 5.67 m agree with each other and are both wrong
  for the street front.** They describe the shed, which is most of the area. The Jan 2025
  photograph plainly shows two full storeys with a tall ground floor, and the front
  parapet is visibly *above* 150 South Park next door (OSM `height=8`) and below 140
  (`height=10`). Take the LiDAR maximum, 8.74 m, rounded to **8.7 m**. This is the same
  trap 543 Presidio Blvd fell into.
- **The assessor's 2,688 sq ft is a single figure used for both lot area and property
  area**, which cannot be right for a two-storey-plus-mezzanine building on a fully covered
  lot. Do not use it to derive floor heights or a storey count. Use the DBI permits, which
  state two storeys and a mezzanine repeatedly between 2019 and 2023.
- **The rear elevation is unverified.** Taber Place Street View coverage exists but could
  not be attributed to this lot with confidence. Everything said about the alley end in
  2.4 is *inferred* from the building type. Re-shoot it before modelling, and if it
  remains unresolved, keep the rear deliberately plain rather than inventing detail.
- **The pane grids are read off one photograph.** The 6x5 ground field and 8x4 upper
  ribbon are counted from a single Jan 2025 pano at an oblique angle; the true counts may
  differ by a column or a row. They matter — the grid *is* the facade — so re-count them
  from a straighter view.
- **The star anchors may not be structural.** They read as the classic tie-rod star
  washers and there is a 1990 "parapet reinforcing" permit that would explain them
  exactly, but the DPR form calls the building reinforced concrete, not unreinforced
  masonry, and a concrete building does not normally need them. Model what is visible;
  do not assert a cause in `REFERENCE.md` beyond "observed, consistent with the 1990
  parapet permit".
- **The taper is real and easy to lose.** A 5.9 m frontage widening to 9.8 m over 32.3 m,
  with both side walls out of parallel and an oblique end on Taber Place, is an odd plan,
  and squaring it into a rectangle is the most likely way for this model to sit wrong in
  the row and to fight the neighbouring footprints at bake time. Note the earlier reading
  of a 19 m rear width was wrong: that number is the sum of the 7.94 m Taber end wall and
  the 11.09 m north-east side wall, which meet at a corner — it is not a width.
- **Resist making it interesting.** The survey's finding that this is the district's only
  unaltered contributor is a statement about how *plain* it is. Every ornament added here
  is a small lie about the one building on the oval that never told any.
- No architect is recorded — the DPR form names only the contractor, J.A. Bryant, and
  found nothing about him at the City, the Public Library or SF Architectural Heritage.
  Exa found nothing either. Do not go looking for a designer's intent that was never
  documented.
