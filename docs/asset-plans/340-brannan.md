# 340 Brannan Street — SF-SIM asset plan

A 1911 reinforced-concrete loft on the northeast corner of Brannan Street and Jack London
Alley, one lot northeast of 350 Brannan and directly across the alley from it. Extensively
remodelled in 1984–85 and again in the 1990s–2010s, it is the block's odd one out: where
its neighbours are white concrete (350) or raw brick (380), 340 is a **flat sage / gray-green
stucco box** with **wide horizontal punched windows in five bays**, a **deeply recessed
bronze ground floor** under a continuous soffit, and a **broad raised parapet with chamfered
shoulders** across the middle of the Brannan front. It is a corner building with exactly
two finished elevations — the Brannan front and the Jack London Alley flank — and two party
walls.

Its neighbours `350-brannan`, `358-brannan`, `362-brannan`, `370-brannan` and `380-brannan`
are already in the manifest, and `106-south-park` (the Gran Oriente Filipino Hotel) is the
building it shares its northwest party wall with. None of them may be mistaken for this one:
340 is the only mid-tone gray-green building on the block, the only one with a modern bronze
storefront, and — at 17.79 m — the tallest of the set by 4 m. Build that difference.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/340-brannan/`. This document is the plan only: Part 1 is the runnable task
prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `340-brannan` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3932324, 37.7812786` |
| Target height | **17.79 m** to the roof penthouse crest; main parapet ~15.45 m; roof deck 14.82 m |
| Footprint | 29.25 m (Brannan frontage, SE) x 28.22 m (Jack London Alley, SW); 821.0 m2, measured |
| Triangle cap | 11,000 |
| Category | `3` (office) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 340 Brannan Street GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of 340 Brannan Street in San Francisco and deliver it
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
7. `artifacts/350-brannan/` — the nearest reference implementation in site and method (same
   block face, same 45° heading, the building directly across Jack London Alley). Read it
   for the *method*, not the *look*: 350 is a white three-storey box with arched portals,
   340 is a sage five-bay slab with a bronze recessed base. They must not read as siblings.
8. `docs/asset-plans/340-brannan.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Must capture

- A **sage / gray-green stucco slab** on a 45°-rotated corner lot, with **two finished
  elevations** (Brannan southeast, Jack London Alley southwest) and **two blind party walls**
  (northeast against 334 Brannan, northwest against the Gran Oriente Filipino block)
- **Four window-line storeys**: a tall recessed ground floor plus three upper floors of
  **wide horizontal punched windows, five bays per finished elevation**, with pale frames
- The **deeply recessed bronze ground floor** — a continuous soffit/fascia band the full
  width, dark bronze storefront framing set back behind it, the recessed lobby entrance and
  its dark brick-clad pier, and the big white **"340"** numerals on the fascia
- The **subtle horizontal banding** of the stucco: broad reveal/score lines at each floor
  line dividing the wall into stacked bands of slightly different tone
- The **raised central parapet with chamfered shoulders** on the Brannan front — the roofline
  steps up across the middle five-eighths of the facade and ramps back down at each end
- A designed flat roof: the parapet ring, the **stair/elevator penthouse** that sets the
  17.79 m crest, the **atrium skylight/trellis frame**, the **two round cooling towers**, the
  **timber roof deck** (a real 460 sq ft permitted structure), and scattered small skylights

## Research 340 Brannan Street independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- Both exposed elevations (Brannan SE, Jack London Alley SW) and the two party walls
- Aerial and roof/top views (the penthouse, atrium skylight, cooling towers, roof deck)
- Ground-level views, particularly the recessed base and the entrance bay
- Day and night appearance
- The bay count and window rhythm — the dossier's reading of **five bays per finished
  elevation** is *inferred* from photography partly screened by two mature street trees and
  must be confirmed
- The exact geometry of the raised central parapet (how far it extends, how steep the
  shoulders are) — see 2.15, this is the building's one signature and the dossier only ever
  saw it foreshortened

Prefer architect/engineer publications, owner or institutional material,
planning and permitting documents, architectural press, geolocated photography,
and aerial/satellite imagery. Never rely on a single photograph, a single
AI-generated image, or a single unsourced 3D model. Separate verified facts from
visual inference; if sources disagree, document the disagreement and decide.

**Three source traps are already known and resolved in 2.1 — re-check them, do not silently
re-inherit the wrong value:**

1. OSM `height=15` is the LiDAR *roof-deck* figure, not the crest, and must never be the
   target height.
2. Every commercial listing, and the assessor roll, calls this a **5-storey** building. The
   street elevations carry **four** window lines, and 4 storeys is exactly what the measured
   14.82 m roof deck supports. Several 1982–89 permits say 4 and several say 5. Model what
   the photographs show; see 2.15 for the reconciliation.
3. The Page & Turnbull National Register form says **stucco**, not brick and not board-formed
   concrete. The South End Historic District literature that surrounds this lot describes
   brick warehouses and will push you toward brick. It is stucco, painted sage.

## Create a reference dossier

Write `artifacts/340-brannan/REFERENCE.md` containing: source links and what each
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
two identity cues carried hard — the raised chamfered parapet and the dark recessed base
under a light body. Resist adding hero-tier ornament; this building has none, and inventing
some would make it a different building.

The finished asset must be immediately recognizable as 340 Brannan Street, consistent with
the real building from all four sides and above, architecturally credible, and a
premium handcrafted miniature — not photorealistic, not voxel art, not generic
low-poly, and never accurate in one view while invented in the others.

## Scope of the exported asset

Export the single building: stucco body, parapet (including the raised central section), both
finished elevations' openings, the recessed ground floor and its entrance, the two blind
party walls, and the roof furniture.

Do not include unrelated surrounding city geometry: Brannan Street, Jack London Alley, the
neighbouring buildings (334 Brannan, the Gran Oriente Filipino block, 350 Brannan across the
alley), South Park, the two street trees, the sidewalk, planters outside the building line,
parked cars, people, plinths, cameras or lights. The leasing banner on the alley wall and the
tenant signage are temporary and must not be modelled. Temporary context may appear in review
renders but must not leak into the GLB.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary
`.glb`; real-world meters; origin at base center; minimum geometry Z ~ 0;
applied transforms; no negative scales; outward normals; no duplicate or foreign
geometry; no image textures; no transparency; flat-color materials named `Toy_*`
from the project palette; `_Glow` suffix only on surfaces that glow at night; no
`Toy_body`; no cameras, lights, animations, armatures or constraints; no external
dependencies; at most 11,000 triangles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model
drops into the city at its real-world heading — the loader applies no rotation
(`placeGeneric` in `app/src/assets.js` only scales and positions). The Brannan Street
entrance front faces **southeast, bearing 135.4°**; the building is rotated roughly 45° off
the world axes, so build directly on the measured footprint polygon in 2.3 rather than
modelling an axis-aligned box and rotating it. Record the measured heading in `REPORT.md`.

**Height normalization:** the tallest geometry in the export (the roof penthouse) must
land at exactly **17.79 m** so the loader's `targetHeightM / measuredHeight` scale is 1.0.

## Reproducible Blender workflow

Blender 5.2 LTS. Headless: `blender -b --python script.py -- args`.

Keep `artifacts/340-brannan/build_340_brannan.py` (deterministic build script),
`artifacts/340-brannan/340-brannan.blend`, and `artifacts/340-brannan/340-brannan.glb`.
The script must rebuild the model reliably enough for future revision. Do not modify or
rename an unrelated existing GLB to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`340-brannan-top.png`, `340-brannan-north.png`, `340-brannan-east.png`,
`340-brannan-south.png`, `340-brannan-west.png`, plus `340-brannan-contact-sheet.png`,
at least one high three-quarter aerial beauty render `340-brannan-aerial.png`, and a
night render `340-brannan-aerial-night.png`.

The four elevations must share scale, framing, lighting, exposure and
projection; use orthographic or long-lens cameras; label directions from the
researched orientation; the top view must clearly show the parapet ring, the penthouse,
the atrium skylight frame, the cooling towers and the roof deck; the aerial view uses the
style bible's camera assumptions (30-50 degrees down, long lens). Simple tabletop lighting,
neutral warm background, minimal depth of field, and every image must depict the same
exported model.

Aim the hero aerial from the **south**, so the Brannan front, the Jack London Alley flank and
the roof are all in frame at once — that is the view the app's camera actually gets, and the
two party walls are the faces the city never shows.

## Validate the exported GLB

Re-import `340-brannan.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture
count, camera count, light count, animation count, applied-transform status,
negative-scale status, normal-orientation status, unexpected geometry, and
per-material contract compliance. Render at least one review image from the
re-imported asset. Write `artifacts/340-brannan/validation.json` and
`artifacts/340-brannan/REPORT.md`.

Note that the axis-aligned XY bounding box will be roughly **40.7 x 40.3 m** even though the
building is 29.3 x 27.1 m — that is the expected consequence of a ~45° real-world heading,
not a scale error.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "340-brannan",
  "file": "340-brannan.glb",
  "anchor": [
    -122.3932324,
    37.7812786
  ],
  "targetHeightM": 17.79,
  "cat": 3,
  "name": "340 Brannan Street",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a separate, explicitly requested job — run `docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in `docs/asset-plans/340-brannan.md`.
````

---

## Part 2 — Research and design dossier

Compiled 16 August 2026 from the sources in 2.2. Values marked *inferred* are visual or
derived estimates, not published figures — the executing agent must re-verify
anything it relies on.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Built | **1911** | Page & Turnbull National Register building data form; SF Assessor secured roll (2020–2025, consistent); Transwestern, LoopNet, CompStak all agree |
| Storeys | **5 of record; 4 window lines on the street** | Assessor roll and every listing say 5; the National Register form says 5; 1982–89 permits say 4 on nine applications and 5 on eleven; photography shows four window lines. See 2.15 |
| Construction | **Reinforced concrete**, exterior material **stucco** | Page & Turnbull NR building data form (block/lot 3775/015); assessor construction class **B**; confirmed visually — smooth painted stucco with scored horizontal reveals, no brick coursing and no board-form marks anywhere |
| Historic status | **Non-contributory** to the South End Historic District; NR status code **7N**; "appears extensively altered from original appearance" | Page & Turnbull, *National Register Certification — South End Historic District*, 26 June 2008, Appendix 2 building data form, and its list of non-contributors (item 7). The body text of the same report contradicts this once — see 2.15 |
| Major remodel | **1984–85**, "removated building" | permits 1982-11-19 through 1985-11-15; listings record "Year Renovated 1985" |
| Block / lot (APN) | 3775 / 015 | SF Assessor; DataSF addresses (`ramy-di5m`); DataSF footprints (`mblr = SF3775015`); CompStak |
| Lot area | 8,604 sq ft = 799.3 m2 | SF Assessor |
| Footprint | **821.0 m2**; 29.25 m (SE, Brannan) x 28.22 m (SW, Jack London Alley) | DataSF LiDAR building footprint, reprojected and reduced to its four real corners (2.3) — **measured** |
| OSM footprint (cross-check) | 768.1 m2 | OSM way/71211340, tagged `addr:housenumber=340`, `addr:street=Brannan Street`, `height=15` — 6.5% under the LiDAR polygon, which carries the parapet/roof overhang |
| Building area | 41,880 sq ft (assessor) / 38,317–42,149 sq ft (listings); typical floor 8,430 sq ft = 783 m2 | SF Assessor; Transwestern; LoopNet; CompStak |
| Roof deck height | **14.82 m** above ground (majority cell 15.03 m) | DataSF LiDAR `hgt_median_m` / `hgt_majoritycm` — **measured** |
| Maximum feature height | **17.79 m** above ground | DataSF LiDAR `hgt_maxcm` — **measured** |
| Main parapet crest | ~15.45 m | *inferred*, roof deck + ~0.6 m |
| Ground elevation | 10.18 m min / 11.23 m median (NAVD88) | DataSF LiDAR `gnd_min_m` / `gnd_mediancm` — app terrain handles this, not the asset |
| Frontage heading | Brannan front faces **135.4°** (SE); Jack London Alley **225.2°** (SW); northwest party wall 315.3°; northeast party wall 44.5° | measured from the footprint polygon |
| Exposed elevations | **two** (SE, SW); NE and NW are party walls | measured — the footprint touches SF3775101 (334 Brannan) on the northeast and SF3775039 / SF3775102 (the Gran Oriente Filipino block) on the northwest, gap 0.00 m to all three |
| Roof deck (timber) | 460 sq ft = 42.7 m2 "removable panel roof deck" | permit 1987-10-22 — the terrace visible in satellite imagery |
| Cooling towers | Two, roof-mounted, replaced in place 2010 | permit 2010-10-20 "replace cooling towers, replace hydronic boiler, no change in equipment size, same locations on roof" |
| Windows | 27 on one elevation group, reflashed 2017, "existing windows to remain, replace in kind" | permit 2017-10-31 — confirms the current punched-window pattern is the one to model |
| No vertical additions | none 1982–2026 | full permit history is tenant improvements, fire alarm and sprinkler work, reroofing (1990, 2011), mechanical replacement — so the 2010 LiDAR crest is still current |
| Current use | Office (creative office suites) throughout; `COMO` / class B | assessor `use_definition`; every permit 1990–2026 `existing_use = office`; Transwestern leasing |

### 2.2 Sources

- https://www.openstreetmap.org/way/71211340 — footprint, `building=yes`, `addr:housenumber=340`, `addr:street=Brannan Street`, `height=15`. Unlike 350 Brannan, **this way is addressed**, so identification needs no derivation
- `https://data.sfgov.org/resource/ramy-di5m` (DataSF Addresses with Units) — 340 BRANNAN ST -> parcel 3775015, point 37.781265 / -122.393229; units #101–#501 confirm five leasable levels
- `https://data.sfgov.org/resource/ynuv-fyni` (DataSF Building Footprints, LiDAR-derived) — authoritative footprint polygon and the 14.82 m / 17.79 m heights (`sf16_bldgid 201006.0003676`)
- `https://data.sfgov.org/resource/wv5m-vpq2` (SF Assessor Historical Secured Property Tax Rolls) — 1911, block/lot, 5 storeys, class B, 8,604 sq ft lot, 41,880 sq ft building, `COMO`
- `https://data.sfgov.org/resource/i98e-djp9` (SF Building Permits, 80+ permits 1982-2026) — the 1984-85 remodel, the 1987 roof deck, the 2010 cooling towers, the 2017 window reflashing, the 4-vs-5 storey split
- https://sfplanninggis.org/docs/NatRegDistricts/2008-06-26_Final-NR-SouthEndHistDist.pdf — Page & Turnbull, *National Register Certification: South End Historic District*, 26 June 2008. Appendix 2 carries a building data form for 340 Brannan Street (1911, 5 storeys, reinforced concrete, **stucco**, **non-contributory**, code 7N, "appears extensively altered from original appearance") and lists it as non-contributor #7. **Primary source, and the only one that describes the material**
- https://transwestern.com/property/340-brannan-st — 1911, renovated 1985, 5 stories, class B, typical floor 8,430 sf, 1 elevator, 39,375 sf available
- https://www.loopnet.com/Listing/340-Brannan-St-San-Francisco-CA/11829135/ — 42,149 sf; "creative building at the entrance to South Park with great natural light"; **atrium, conference facility, kitchen, roof terrace**
- https://property.compstak.com/340-Brannan-Street-San-Francisco/p/2241 — 38,317 sf, APN 3775-015, coordinates 37.781265 / -122.393229, last sold 2014
- Google Street View, Brannan Street panos (capture **May 2025**), headings ~315-325° — the SE elevation: sage stucco, four window lines, five bays, the raised chamfered parapet, the recessed bronze base, the "340" numerals
- Google Street View, **Jack London Alley** pano at 98 Jack London Alley (capture **January 2025**), heading ~30° — the SW elevation close up: the same body colour, the horizontal banding, the flat metal eyebrow canopy, the ground-floor window wall, a flush service door, wall-mounted cameras
- Google Street View, Brannan/Jack London Alley three-quarter (capture May 2025, from the south side of Brannan) — the corner, both finished elevations at once, and the party-wall junctions with 350 Brannan across the alley and 334 Brannan to the northeast
- Google Maps satellite (Vexcel Imaging, 2026) — white membrane roof, parapet ring, the central penthouse with a reddish roof, the atrium skylight/trellis frame, two round cooling towers, the timber roof deck, small skylights
- Consulted and **not used**: `noehill.com` South End Historic District page and the district's brick-warehouse descriptions — the report itself classes this building as a non-contributor, so district-level material descriptions are not evidence about it

### 2.3 Orientation and placement

The building occupies the northeast corner of Brannan Street and Jack London Alley, at the
Brannan end of the alley, one lot up from South Park. Brannan Street is to the southeast,
Jack London Alley to the southwest. The northeast side is a party wall against 334 Brannan
Street and the northwest side a party wall against the Gran Oriente Filipino block (the same
block as `106-south-park`). Like the whole SoMa grid it is rotated about 45° from the world
axes.

Measured footprint polygon, in Blender coordinates (metres, `+X` east, `+Y` north),
counter-clockwise, already centred on the anchor `-122.3932324, 37.7812786`:

```
(-20.281,  -0.177)     west corner
( -0.396, -20.202)     south corner  (Brannan x Jack London Alley)
( 20.429,   0.339)     east corner
(  0.267,  20.139)     north corner
```

The DataSF survey carries eleven vertices, but **every one of them lies within 0.12 m of
this quadrilateral** (worst case 0.115 m, on the northwest run) — the extra points are
survey noise, not corners. Four vertices is the honest simplification here, unlike 350
Brannan across the alley where the sub-metre jogs were real.

Edges, with outward normals:

| Edge | Length | Faces | Elevation |
|---|---|---|---|
| `(-0.396,-20.202) -> (20.429,0.339)` | **29.25 m** | SE 135.4° | **Brannan Street front** |
| `(-20.281,-0.177) -> (-0.396,-20.202)` | **28.22 m** | SW 225.2° | **Jack London Alley flank** |
| `(0.267,20.139) -> (-20.281,-0.177)` | 28.90 m | NW 315.3° | northwest party wall (blind) |
| `(20.429,0.339) -> (0.267,20.139)` | 28.26 m | NE 44.5° | northeast party wall (blind) |

Because of the 45° heading the axis-aligned bounding box is ~40.7 x 40.3 m. That is correct.

### 2.4 What each side shows

**Southeast (Brannan Street front)** — The hero elevation, 29.25 m wide. A flat **sage /
gray-green stucco** wall in four levels:

- a **tall recessed ground floor**, set back roughly 1.2 m behind a continuous horizontal
  **fascia/soffit band** that runs the full width at ~4.6 m. Behind it, a dark **bronze-brown
  storefront system** — anodized mullions, solid spandrel panels and a transom band above the
  glazing, so the base reads as two horizontal glass strips separated by a metal band. The
  lobby entrance sits right of centre, recessed further, flanked by a **dark brick-clad pier**,
  with the white **"340"** numerals on the fascia beside it. Ornamental-grass planters, bollards
  and bike hoops sit on the sidewalk in front (not in the GLB);
- three upper floors of **wide horizontal punched windows in five bays**, pale frames, a
  two-light horizontal division per window, set high in each floor band with a broad blank
  spandrel below;
- the stucco is divided by **horizontal scored reveals at each floor line**, so the wall
  reads as stacked bands of very slightly different tone rather than one flat plane;
- the roofline is **not level**: a **raised parapet section spans the middle of the facade**
  and ramps back down to the lower end parapets on **chamfered shoulders**. It is a shallow,
  modern, almost-Deco gesture and it is the single thing that distinguishes this roofline
  from every other flat parapet on the block.

**Southwest (Jack London Alley flank)** — 28.22 m of the same wall: same colour, same
banding, same window rhythm and bay count. Differences: a **flat metal eyebrow canopy** runs
along the wall above the ground floor instead of a deep recess; the ground level is a
**continuous glazed window wall** with a heavy transom band and an exposed diagonal brace
visible behind the glass; there is one **flush dark service door** near the northwest end,
and wall-mounted lights and cameras. The alley is narrow and rarely photographed at street
level, but the app's aerial camera sees this face plainly — build it properly.

**Northeast** — Party wall against 334 Brannan Street (a pale pilastered concrete loft, 12.14 m
tall). Blind, no openings. Because the neighbour is 12.1 m and this building is 15 m, the top
~3 m of this wall is exposed above the neighbour's parapet — model it as flat wall in the body
colour and let it show.

**Northwest** — Party wall against the Gran Oriente Filipino block (7.84 m and 10.49 m
sections). Blind. The same logic applies with more of the wall exposed: roughly the upper 4.5
to 7 m is visible above the neighbours. Flat wall in the body colour, no openings.

**Top** — A bright white membrane roof inside a continuous parapet, with a real, legible
cluster of furniture toward the southwest (alley) half:

- a **penthouse block with a reddish-brown roof**, roughly 9 x 7 m, the tallest thing on the
  building and almost certainly what the 17.79 m LiDAR maximum measures — a stair and
  elevator bulkhead (the building has one elevator);
- an open **light-framed trellis/skylight structure** immediately northeast of it, over the
  atrium — it reads in satellite as a rectangular frame with an open or glazed interior;
- **two round cooling towers** west of the penthouse, with associated ductwork;
- the **timber roof deck** — a run of reddish-brown decking heading southwest from the
  penthouse toward the alley parapet (the permitted 460 sq ft terrace);
- a small cluster of flat **skylights** near the west corner.

This is the surface the app's camera sees most, and unusually for this block it has real
content. Design it.

### 2.5 Recognition cues (ranked)

1. **The raised central parapet with chamfered shoulders** — a stepped silhouette on a street
   of dead-flat parapets, and it survives to thumbnail size
2. **The sage / gray-green body** — the only mid-tone green-gray building on the block, sitting
   between white 350, pale 334 and brick 380
3. The **dark recessed bronze base** under a continuous light fascia — a heavy shadow line
   that separates the body from the ground at exactly one height across both finished faces
4. Four window lines of **wide horizontal five-bay punched windows** — horizontal, not the
   vertical industrial sash of its neighbours
5. Being the **tallest building on this block face** at 17.79 m, standing ~3 m proud of both
   party-wall neighbours

### 2.6 Miniature translation

**Preserve**

- The single chunky slab and its real 45° heading
- The raised central parapet, as a real step with real chamfered shoulders
- The two-finished-sides / two-blind-sides asymmetry, and the fact that the blind sides
  stand proud of their neighbours
- The value contrast: light sage body over a dark recessed base — that contrast *is* the
  building

**Simplify / exaggerate**

- Five bays per finished elevation, all identical, on all three upper floors
- Window openings become single flat glazing panels recessed 0.2 m with one horizontal
  mullion — no frames-within-frames
- The stucco banding becomes a 0.06 m recessed reveal at each floor line, nothing more; do
  not model separate band volumes
- The bronze storefront becomes one recessed dark band with a single horizontal metal rail
  across it; the entrance is one wider recess with the brick pier beside it
- The raised parapet section is widened and its step deepened slightly so it still reads at
  thumbnail size; this is the one place semantic exaggeration is spent
- The "340" numerals stay — they are 1.2 m tall, they are the address, and they read from the
  aerial. The leasing banner and tenant signage go
- Roof clutter becomes one penthouse block, one open trellis frame, two cylinders, one deck
  slab with a low rail, and two skylight boxes
- The two street trees, planters, bollards and bike hoops are dropped — they belong to the
  city, not the asset

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not
a straitjacket — adjust after the first aerial review render.

1. Body: extrude the 2.3 footprint from z=0 to z=14.82, `Toy_sage`.
2. Ground floor recess, z=0 to z=4.60, **SE and SW elevations only**: inset the wall 1.2 m,
   `Toy_ink` back wall. Across the SE recess, a `Toy_bronze` storefront band: glazing
   z=0.4–2.2 and z=2.6–4.1 (`Toy_glass`), separated by a 0.4 m `Toy_bronze` rail, on 0.35 m
   mullions every 3.6 m. Entrance: a 4.2 m bay centred 4 m northeast of the facade midpoint,
   recessed a further 0.6 m, `Toy_glass` doors, with a 1.1 m wide `Toy_brick` pier on its
   northeast side running the full 4.60 m.
3. SW ground floor: the same band without the entrance, plus one 1.4 x 2.6 m flush
   `Toy_roofd` service door 3 m from the northwest end, and a flat `Toy_steel` eyebrow canopy
   0.9 m deep at z=4.35 running the full 28.22 m.
4. Fascia band: a continuous `Toy_trim` band z=4.60 to z=5.05, flush with the outer wall
   plane, on the SE and SW elevations — this is the light line the recessed base hangs under.
5. Upper floors, five bays per finished elevation, bay pitch 5.30 m (SE) / 4.90 m (SW):
   - floor 2: opening 3.60 x 1.95 m, sill z=5.90, recessed 0.20 m, `Toy_glass`
   - floor 3: opening 3.60 x 1.95 m, sill z=9.30, recessed 0.20 m, `Toy_glass`
   - floor 4: opening 3.60 x 1.95 m, sill z=12.70, recessed 0.20 m, `Toy_glass`
   Each opening gets one 0.10 m `Toy_trim` horizontal mullion at mid-height and a 0.08 m
   `Toy_trim` surround.
6. Banding: 0.06 m deep, 0.12 m tall recessed reveals at z=5.05, 8.45 and 11.85 on the SE and
   SW elevations only.
7. Parapet: follow the footprint, 0.35 m thick, `Toy_sage`, z=14.82 to **z=15.45** everywhere;
   then on the **SE elevation** raise the section between 18% and 80% of the frontage to
   z=16.10, with 2.2 m chamfered ramps at both ends. Cap the whole ring with a 0.10 m
   `Toy_trim` band.
8. Roof deck at z=14.82, `Toy_stone` (the real membrane is white — do not default to a dark
   deck).
9. Roof furniture, all on the southwest half:
   - penthouse 9.0 x 7.0 m, z=14.82 to **z=17.79**, `Toy_sage` walls with a `Toy_rust` flat
     roof slab — this sets the bounding-box top and must land exactly on 17.79;
   - trellis frame 7.0 x 5.0 m immediately northeast of the penthouse: four 0.25 m
     `Toy_steel` posts, a 0.2 m perimeter beam at z=17.0 and five cross members, open to
     the sky, with a `Toy_glassl` skylight panel at z=15.0 inside it;
   - two cooling towers, cylinders r=1.1 m, h=2.4 m, 12 segments, `Toy_steel`, 3.5 m apart,
     west of the penthouse, on a 0.3 m `Toy_roofd` plinth;
   - roof deck 8.0 x 5.0 m of `Toy_rust` decking at z=15.02, southwest of the penthouse, with
     a 1.0 m `Toy_ink` rail on its two open sides;
   - two skylight boxes 2.2 x 1.4 x 0.35 m `Toy_glassl` near the west corner.
10. Party walls (NE and NW): flat `Toy_sage`, no openings, no banding, no recess.
11. Bevel 0.12 m, 2 segments.

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette except where noted.

| Material | Hex | Used for |
|---|---|---|
| `Toy_sage` | `#8d9082` (off-palette) | the stucco body on all four elevations, parapet, penthouse walls |
| `Toy_trim` | `#f3efe6` | the ground-floor fascia band, parapet cap, window surrounds and mullions |
| `Toy_glass` | `#2a4d73` | upper-floor windows and the ground-floor storefront glazing |
| `Toy_glassl` | `#6f95b8` | roof skylights and the atrium skylight panel |
| `Toy_stone` | `#d9d2c2` | roof membrane deck |
| `Toy_bronze` | `#5a4a3a` (off-palette) | ground-floor storefront framing, mullions and rail |
| `Toy_brick` | `#c96f4a` | the entrance pier |
| `Toy_rust` | `#a86444` | penthouse roof slab and the timber roof deck |
| `Toy_steel` | `#9aa0a6` | cooling towers, eyebrow canopy, trellis frame |
| `Toy_roofd` | `#45454a` | service door, mechanical plinth |
| `Toy_ink` | `#3a3530` | ground-floor recess back wall, roof-deck rail |
| `Toy_white` | `#f7f4ec` | the "340" numerals |
| `Toy_glass_Glow` | `#2a4d73` | lit upper windows at night |
| `Toy_white_Glow` | `#f7f4ec` | the lit "340" numerals and the lit lobby at night |

Two palette extensions, both with precedent (`380-brannan` extended with `Toy_slate`,
`140-south-park` with `Toy_olive`, `155-south-park` with `Toy_peach`), both a WARN and not a
FAIL under the contract:

- **`Toy_sage` ≈ `#8d9082`.** The real paint is a mid-tone gray-green that reads olive in sun
  and cool gray in shade. `Toy_steel` (`9aa0a6`) is a blue-gray and kills the green;
  `Toy_verdigris` (`9fb8a8`) is far too mint; `Toy_olive` (`5f655c`, from `140-south-park`) is
  the right hue but much too dark for a five-storey street wall. Decide from the aerial render
  against 350 Brannan's cream and 334's pale concrete, and record the decision in `REPORT.md`.
- **`Toy_bronze` ≈ `#5a4a3a`.** The dark anodized base. `Toy_ink` (`3a3530`) is close but
  reads black and flattens the entrance detail against the recess behind it; `Toy_roofd`
  (`45454a`) is a cool gray. If the render shows no difference, collapse `Toy_bronze` into
  `Toy_ink` and say so.

Do **not** reach for `Toy_brick` for the body — see 2.15.

**Night state (required).** Glow surfaces must be thin shells proud of the opaque glazing —
the app renders `_Glow` in a separate layer that is ~12% alpha by day per glow *layer*, so a
closed shell reads at roughly twice that and a primary surface must never be authored as
glow. Hero glow: the **recessed ground floor**, lit as a lobby — a wide, low, warm band under
the dark fascia, which is exactly how this building reads at night and is the inverse of its
daytime dark base. Supporting accents: the **"340" numerals**, and a scatter of lit upper
windows — five or six across the two finished faces, not all fifteen. The parapet, the
penthouse and the roof furniture do not glow.

### 2.9 Top surface

A flat roof 15 m up in a district the camera flies over constantly — and unlike most of this
block, it has real content: a penthouse standing 3 m proud, an open trellis frame beside it, a
pair of cooling towers and a timber terrace. That cluster is legible from the aerial camera and
it is what sets the model's height, so it is worth its triangles. Keep it all in the southwest
half, leave the northeast half of the membrane clean, and keep the parapet ring continuous so
the deck never reads as an open tray. Because the real membrane is white, get separation from
the *warm* elements (`Toy_rust` penthouse roof and deck) and the *cool* ones (`Toy_steel`
towers), not by darkening the deck.

### 2.10 Scope

**In the GLB:** the single building — stucco body, parapet including the raised central
section, both finished elevations' openings, the recessed ground floor and entrance, the "340"
numerals, the two blind party walls, the roof deck and all roof furniture

**Not in the GLB:** Brannan Street, Jack London Alley, 334 Brannan, the Gran Oriente Filipino
block, 350 Brannan, South Park, the two street trees, sidewalk planters, bollards, bike hoops,
the leasing banner, tenant signage, vehicles, people, plinths, cameras or lights

### 2.11 Triangle budget

Cap 11,000 — a secondary building, but the largest of the Brannan set: two finished elevations
of five bays over three floors, a stepped parapet, and the richest roof on the block.
Suggested split: body, party walls and parapet (including the raised section and its ramps)
~2.5k, upper window bays (three floors x two elevations x five bays) ~3.5k, recessed ground
floor, storefront and entrance ~2k, "340" numerals ~0.5k, roof furniture ~2k.

### 2.12 Draft manifest entry

```json
{
  "id": "340-brannan",
  "file": "340-brannan.glb",
  "anchor": [
    -122.3932324,
    37.7812786
  ],
  "targetHeightM": 17.79,
  "cat": 3,
  "name": "340 Brannan Street",
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
  (`id: '340Brannan'`, `lon: -122.3932324`, `lat: 37.7812786`, `height: 17.79`,
  `exclude: 8`, `camera: { distance: 240, yaw: 55, pitch: 26 }`) and re-bake the affected
  tiles, or the baked procedural building on this exact footprint will intersect the GLB.
- **Exclusion radius, measured.** `excluded()` in `pipeline/buildings.mjs` drops a footprint
  when its centroid **or any ring vertex** falls inside the radius. Measured from this anchor
  against the DataSF footprints:
  - our own footprint's centroid sits at ~0 m, so any radius > ~1 m drops this building;
  - the nearest **neighbour** ring vertex is at **14.16 m** (SF3775039, the Gran Oriente
    Filipino block, northwest);
  - the next are at 15.52 m (SF3775102, same block) and 16.80 m (SF3775101, 334 Brannan).

  So the safe band is roughly 1 m to 14.1 m and **8 m sits comfortably inside it**. Note that
  our own footprint reaches 20.43 m from the anchor — that is fine, because the centroid test
  alone is enough to drop it, but it means you must **not** reason "the radius has to cover
  the building". Do not raise it past 12 without re-running the check. Re-verify against the
  actual baked footprint source (Overture as well as DataSF — both trace some buildings here)
  before committing, then run `pipeline/audit.mjs` 1.6 and `pipeline/verify-rebake.mjs`.
- `loadRadius`: the skill's default formula gives `max(2500, 17.79 * 30) = 2500` m. Take the
  default; at 2.5 km an 18 m building is far below a pixel, so the carved-out gap is
  illegible.
- **Batch mode applies.** This block already has five integrated siblings and more may be in
  flight. Follow "Batch mode" in `docs/asset-pipeline/ADDRESS-TO-ASSET.md`: run the bake and
  do the full QA on it, then `git checkout -- app/public/tiles api/_data` before committing,
  and let `docs/asset-pipeline/BATCH-INTEGRATE.md` bake the city once for the whole batch.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Bounding-box top exactly 17.79 m (loader scale lands at 1.0)
- [ ] Dimensions plausible in meters and consistent with 2.1 (XY bbox ~40.7 x 40.3 m is expected)
- [ ] Triangles at or under 11,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`; the two palette
      extensions documented as WARNs in `REPORT.md`
- [ ] `_Glow` only on the lobby band, the numerals and the scattered lit windows; glow shells
      proud of opaque glazing and never closed around a primary surface
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (per-object signed volume for the
      union of solids; ray test residual <= 0.15%)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + contact sheet + night render regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

- **Four window lines versus five storeys of record.** Every commercial listing, the assessor
  roll and the National Register form say five storeys; eleven permits say five and nine say
  four; the LiDAR says the roof deck is 14.82 m. Photography from three separate Street View
  positions shows a tall recessed ground floor plus **three** upper window lines — four levels.
  Those reconcile arithmetically: a 4.60 m ground floor plus three 3.40 m floors is 14.80 m,
  within 2 cm of the measured deck. Five floors of 8,430 sq ft over a 783 m2 floor plate then
  requires a fifth leasable level that is not a fifth window line — most plausibly a mezzanine
  inside the double-height base, which is also where the atrium sits, or the penthouse level.
  **Model what the photographs show: four window lines.** Do not add a fifth row to satisfy the
  paperwork. But confirm this before you commit to the facade — it is the single largest risk
  in this dossier, and if a photograph shows four upper rows then the floor heights in 2.7 are
  all wrong.
- **The National Register report contradicts itself.** Its body text (p. 13) says "two
  resources, 340 Brannan Street and 350 Brannan Street, appear to be contributors to the South
  End Historic District", while its own list of non-contributors names 340 Brannan as item 7
  and its Appendix 2 building data form for 340 Brannan records "Non-contributory", status code
  **7N**, "appears extensively altered from original appearance". Two independent places against
  one sentence: treat it as **non-contributory**. This matters because a contributory 1911
  warehouse would be modelled very differently from a 1985-remodelled office box, and the
  building is emphatically the latter.
- **OSM `height=15` is the roof deck, not the crest.** It matches the LiDAR majority cell
  (15.03 m) almost exactly, which makes it look trustworthy. The crest is ~15.45 m at the main
  parapet, ~16.1 m at the raised central section, and 17.79 m at the penthouse. This is the trap
  the plans README warns about, again, in a building where the tag looks plausible.
- **Whether 17.79 m is the penthouse is *inferred*.** The satellite view shows a clearly raised
  block with a reddish roof and that is the natural candidate for a stair/elevator bulkhead in a
  building with one elevator, but the LiDAR maximum is a single cell and the trellis frame beside
  it is a competing candidate. Either way the bounding-box top lands on 17.79; only the shape of
  what tops out is at stake.
- **The raised central parapet was only ever seen foreshortened.** Both Street View positions
  that show it are close to the building and low, so the fractions in 2.7 (raised between 18%
  and 80% of the frontage, 2.2 m ramps, +0.65 m step) are *inferred* from a perspective image.
  Confirm against a flatter photograph or an oblique aerial before committing — this is the
  building's signature and getting its proportions wrong wastes the one cue that carries.
- **The stucco banding may be control joints, not tonal bands.** The alley pano reads as broad
  horizontal stripes of slightly different tone; the Brannan panos read as a plain wall with
  faint horizontal score lines. It may simply be lighting. Model it as a shallow reveal (2.7
  step 6) which is defensible either way, and do not model separate coloured bands.
- **The brick trap, in reverse.** The neighbouring assets `380-brannan` (brick) and the South
  End Historic District literature will push toward masonry. The National Register form for
  *this* building says stucco over reinforced concrete, and every photograph shows a smooth
  painted wall with no coursing. Reserve `Toy_brick` for the entrance pier only.
- **The two street trees hide roughly a third of the Brannan facade** in every Street View
  capture. The five-bay reading is a regularisation of what is visible at the two ends plus the
  alley elevation. Confirm the bay count from the alley face, from listing photography, or from
  an older Street View capture before the trees matured (`See more dates`).
- **`cat: 3` (office)** matches the assessor `COMO`, every permit since 1990, and the
  neighbouring `350-brannan` and `380-brannan` entries. `19` (industrial) or `20` (warehouse)
  are not defensible here: unlike its neighbours this building has been an office box since the
  1985 remodel and looks like one.
- No architect is recorded for the 1911 building, or for the 1984–85 remodel, in any source
  consulted. The Page & Turnbull form leaves both the Architect and Builder fields blank.
