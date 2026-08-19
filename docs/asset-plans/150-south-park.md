# 150 South Park — SF-SIM asset plan

A 1959 two-storey commercial building at the **head of the South Park oval**, comprehensively
re-faced in 2017–18: a near-black painted-brick upper floor over a bright white stucco
ground floor, with a flat black steel canopy and two oxblood-framed windows. It is the
youngest building in its row and the only **non-contributor** on this stretch — which is
exactly why it is worth building: at diorama scale it is the one hard black-and-white note
in a row of grey and cream Edwardian industrial fronts, and it sits on the sightline every
camera takes down the length of the park.

Its footprint is the other reason. South Park Street curves around the west tip of the
oval, so this lot is a **wedge**: 5.34 m wide at the street, 9.72 m wide at the back, 18.7 m
deep, with party walls on both long sides. Nothing about it is square.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/150-south-park/`. This document is the plan only: Part 1 is the runnable task
prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `150-south-park` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3947673, 37.7813810` |
| Target height | **8.0 m** to the front parapet crest; roof deck 7.5 m (measured) |
| Footprint | 161.7 m2, measured; wedge 5.34 m (street) → 9.72 m (rear), 18.7 m deep; OBB 18.89 x 10.29 m |
| Triangle cap | 6,000 |
| Category | `3` (office) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 150 South Park GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of 150 South Park (150 S Park St), San Francisco
and deliver it as a downloadable, validated GLB.

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
   party-wall South Park front in this set, same scale, same "two-tone box on a
   5–6 m frontage" brief, and the same white-body / dark-base value split
8. `artifacts/135-south-park/` — the closest reference for a small flat-roofed South Park
   commercial building at almost the same height (8.5 m)
9. `docs/asset-plans/150-south-park.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Must capture

- The **two-tone split**: a near-black painted-brick upper storey sitting directly on a
  bright white stucco ground floor, with a thin white drip line between them. The value
  contrast is the whole silhouette, and it is inverted relative to 155 South Park
  (which is white over black) — that inversion is the point of having both in the row.
- The **two square upper windows** in thick **oxblood / copper-brown** frames, evenly
  spaced on the 5.3 m front. They are the only warm colour on the building.
- The **flat black steel canopy** over the ground floor, carried on two thin diagonal rod
  stays, with a **black gooseneck lamp** on the wall either side of it.
- The **shopfront**: a large black-framed plate-glass display window at centre-left, a tall
  narrow glazed entrance door with a transom at the right end, and a narrow secondary door
  at the left end. The tall thin **"150"** numerals on the white wall between the display
  window and the entrance door.
- The **wedge plan** — 5.34 m at the street, 9.72 m at the rear, with a 26 degree kink
  partway along the south-west party wall. Do not square it up and do not model it as a
  rectangle; the wedge is what makes it sit correctly in the curving row.
- The **rear (Taber Place) elevation**: the same charcoal wall, a horizontal band of two
  large windows in the same brown frames, a plain flat parapet.
- A plain **flat membrane roof** inside a parapet ring, with skylights and one small vent
  cluster. No penthouse — see 2.15.

## Research 150 South Park independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- The South Park (south-east) elevation in detail — the exact window proportions and
  frame colour, the canopy depth, the shopfront divisions, whether the "150" numerals
  are painted or applied
- The Taber Place (north-west) rear elevation, which this dossier is weakest on: the
  rear volume was read through a 3 m fence from a single Jan 2025 pano
- Aerial and roof views: the parapet ring, skylight positions, any rooftop plant
- Day and night appearance; the ground floor is a commercial tenant space and the upper
  floor is a live/work unit, so the intended night state is a lit shopfront plus lit
  upper windows
- Whether the ground-floor tenant has changed since the Jan 2025 "FOR LEASE" signage.
  The lease sign is temporary — do **not** model it

Prefer architect/engineer publications, owner or institutional material,
planning and permitting documents, architectural press, geolocated photography,
and aerial/satellite imagery. Never rely on a single photograph, a single
AI-generated image, or a single unsourced 3D model. Separate verified facts from
visual inference; if sources disagree, document the disagreement and decide.

**Two source conflicts are already resolved in 2.1 and 2.15 — re-check them, do not
silently re-inherit a wrong value:** the LiDAR `hgt_max` of 9.95 m is a 3σ outlier on a
footprint whose height standard deviation is 0.78 m, and is the corner street tree, not a
penthouse (build to 8.0 m, not 9.95 m); and the SF Assessor's "Commercial Office" use code
describes the ground floor only — the 2017 permits name an "upper level unit", a "live/work
bathroom" and a "residential entry", so the upper storey is residential live/work and its
night state should read that way.

## Create a reference dossier

Write `artifacts/150-south-park/REFERENCE.md` containing: source links and what each
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
below 380 Brannan and at the same level as 155 South Park. One wedge volume, one hard
horizontal value split, two windows, one canopy, a plainly designed roof. Exactly two
identity cues carried hard: the black-over-white split and the oxblood window frames.
Resist adding ornament — this is a 1959 utility building with a 2017 designer re-face, and
its whole character is that it has almost no ornament at all while its neighbours have
cornices and industrial sash. That restraint is the recognition cue.

The finished asset must be immediately recognizable as 150 South Park, consistent with the
real building from all four sides and above, architecturally credible, and a premium
handcrafted miniature — not photorealistic, not voxel art, not generic low-poly, and never
accurate in one view while invented in the others.

## Scope of the exported asset

Export the single building: the two-storey wedge volume, the shopfront, the canopy and
lamps, the parapet, the roof surfaces and roof furniture, and the rear elevation.

Do not include unrelated surrounding city geometry: South Park Street, the South Park oval
and its trees, Taber Place, the rear yard and its 3 m steel fence, the neighbouring
buildings at 140 and 156 South Park, sidewalks, parked cars, people, plinths, cameras or
lights. Temporary context may appear in review renders but must not leak into the GLB.
The "FOR LEASE" sign is not part of the building.

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
entrance front faces **south-east, bearing 133.5°**; the north-east party wall faces
46.3°, the rear faces 315.2°. The lot is rotated roughly 43° off the world axes, so build
directly on the measured footprint polygon in 2.3 rather than modelling an axis-aligned
box and rotating it. Record the measured heading in `REPORT.md`.

**Height normalization:** the tallest geometry in the export (the front parapet crest)
must land at exactly **8.0 m** so the loader's `targetHeightM / measuredHeight` scale is
1.0. Keep all roof furniture at or below 7.9 m so the parapet ring, not a vent, sets the
bounding-box top.

## Reproducible Blender workflow

Blender 5.2 LTS. Headless: `blender -b --python script.py -- args`.

Keep `artifacts/150-south-park/build_150_south_park.py` (deterministic build script),
`artifacts/150-south-park/150-south-park.blend`, and
`artifacts/150-south-park/150-south-park.glb`. The script must rebuild the model reliably
enough for future revision. Do not modify or rename an unrelated existing GLB to satisfy
the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`150-south-park-top.png`, `150-south-park-north.png`, `150-south-park-east.png`,
`150-south-park-south.png`, `150-south-park-west.png`, plus
`150-south-park-contact-sheet.png`, at least one high three-quarter aerial beauty render
`150-south-park-aerial.png`, and a night render `150-south-park-aerial-night.png`.

The four elevations must share scale, framing, lighting, exposure and
projection; use orthographic or long-lens cameras; label directions from the
researched orientation; the top view must clearly show the parapet ring, the wedge plan
and the roof furniture; the aerial view uses the style bible's camera assumptions
(30-50 degrees down, long lens). Simple tabletop lighting, neutral warm background,
minimal depth of field, and every image must depict the same exported model.

Because the building's real front faces south-east, the labelled `south` and `east`
elevations will each catch part of the front at 45°. Say so in the render captions rather
than rotating the model to make the elevations tidy.

## Validate the exported GLB

Re-import `150-south-park.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture
count, camera count, light count, animation count, applied-transform status,
negative-scale status, normal-orientation status, unexpected geometry, and
per-material contract compliance. Render at least one review image from the
re-imported asset. Write `artifacts/150-south-park/validation.json` and
`artifacts/150-south-park/REPORT.md`.

Note that the axis-aligned XY bounding box will be roughly **20 x 18 m** even though the
building is a 5.3–9.7 m wide, 18.7 m deep wedge — that is the expected consequence of a
~43° real-world heading, not a scale error.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "150-south-park",
  "file": "150-south-park.glb",
  "anchor": [
    -122.3947673,
    37.781381
  ],
  "targetHeightM": 8.0,
  "cat": 3,
  "name": "150 South Park",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a separate, explicitly requested job — run `docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in `docs/asset-plans/150-south-park.md`.
````

---

## Part 2 — Research and design dossier

Compiled 16 August 2026 from the sources in 2.2. Values marked *inferred* are visual or
derived estimates, not published figures — the executing agent must re-verify
anything it relies on.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Built | **1959** | SF Assessor secured roll, block 3775 lot 065 (consistent 2024–2025); SF Planning South Park Historic District DPR form gives the same year |
| Historic status | **Non-contributor** to the potential South Park Historic District; CHRSC status code `6L` | SF Planning / Page & Turnbull DPR 523D, 30 June 2009 — the district's period of significance is 1854–1935 and every one of its 27 in-period buildings was built 1906–1935, so a 1959 building cannot contribute |
| DPR property type | "HP6. 1-3 Story Commercial Building" | same |
| Building type | **Commercial ground floor + upper live/work unit** | 2017 permits name an "upper level unit", a "live/work bathroom", a "residential entry" and a "commercial tenant space"; the Assessor's `COMO` use code sees only the commercial half — see 2.15 |
| Levels | **2** | SF Assessor (`number_of_stories = 2.0`); every permit 1992–2024 records "2 → 2"; street-level photography, Jan 2025 |
| Construction | Assessor construction type `C`; the upper storey is visibly **brick**, painted | SF Assessor roll; Jan 2025 photography (coursing legible through the paint) |
| Block / lot / APN | 3775 / 065 (APN 3775-065) | SF Assessor; LoopNet; DataSF building footprints (`mblr = SF3775065`) |
| Zoning | `SPD` (South Park District) | SF Assessor roll |
| Assessor floor area | 3,520 sq ft (327 m2) over a 3,060 sq ft (284 m2) lot | SF Assessor roll — 327 m2 over two floors is 163 m2 per floor, which matches the 161.7 m2 footprint, so unlike 155 South Park this figure *is* the whole building |
| Footprint | **161.7 m2**; wedge, 5.34 m at the street widening to 9.72 m at the rear, 18.7 m deep; OBB 18.89 x 10.29 m, 83.2% rectangular fill | DataSF LiDAR building footprint (`ynuv-fyni`, `mblr = SF3775065`), reprojected — **measured** |
| Overture footprint (cross-check) | 166.6 m2, same outline | `pipeline/data/overture_buildings.geojsonseq` — agrees with DataSF within 3% |
| OSM footprint (cross-check) | way/124884352, `addr:housenumber = 150`, `addr:street = South Park`, `height = 8`, `source = Bing` | OSM — a Bing trace, cross-check only (plans README) |
| Roof deck height | **7.48 m** above ground | DataSF LiDAR `hgt_majoritycm = 748` (the modal height cell) — **measured** |
| LiDAR median / mean | 7.63 m / 7.93 m, σ 0.78 m | DataSF `hgt_median_m`, `hgt_meancm`, `hgt_stdcm` — a tight, single-plane roof |
| Front parapet crest | **8.0 m** | OSM `height = 8` and Overture `height = 8.0` (independent of each other only in name — Overture carries the OSM tag), corroborated by the roof-deck mode 7.48 m plus a parapet read off the Jan 2025 frontage photograph. This is the target height |
| LiDAR max | 9.95 m | DataSF `hgt_maxcm` — **discarded**: 3σ above the median on a σ = 0.78 m footprint, and the corner street tree overhangs this frontage. See 2.15 |
| LiDAR min | 5.20 m | DataSF `hgt_mincm` — the matching edge artifact at the other end |
| Ground elevation | 7.76 m (NAVD88) | DataSF LiDAR `gnd_min_m` — the app terrain handles this, not the asset |
| Frontage heading | front faces **133.5° (SE)**; NE party wall faces 46.3°; rear faces 315.2° | measured from the DataSF footprint polygon |
| 2017–18 re-face | "replace windows & door to upper level unit, relocate window & door at commercial tenant space, add 1 new window over residential entry, bring recessed [entry]" ($40k, filed 23 May 2017), plus ADA restroom / live-work bathroom work ($21k), tenant improvement ($30k), grade deck replacement ($8k) | SF DBI permits (`i98e-djp9`), block 3775 lot 065 — this is the facade the model must build |
| Rear fence | replaced 2018, "same ht **10'**" (3.05 m) | SF DBI permit, 27 Jul 2018 — matches the Jan 2025 Taber Place pano. **Not in the GLB** |
| Owner / manager | **Kidson Land Company** (Jeremy Kidson, registered at this address Dec 2022); "South Park Street" LLC registered Jul 2021 | SF Registered Business Locations (`g8m3-pdis`); the Jan 2025 "FOR LEASE — Kidson Land Company" sign on the facade |
| Ground-floor status | **Vacant / for lease** as of the Jan 2025 pano; LoopNet lease listing activity May 2023 | Street View; LoopNet |
| Past tenants | Seedling Projects (2010–14), Tendril Studios (2010–18), Eitel Construction (2007–18), Paidpiper (2013–14), Renzu Inc "150 South Park St **2nd Fl**" (2014–15), Everlance (2015–17), Craft & Company (2017–18) | SF Registered Business Locations — the "2nd Fl" suffix is the independent confirmation of two occupied floors |
| Neighbours | **140 South Park** (NE, lot 064, 1907, 6.84 m frontage, LiDAR 9.88 m, occupied by Flourish Ventures, a district *contributor*) and **156 South Park** (SW, lot 066, 1925, 5.92 m frontage, LiDAR 5.67 m, the grey industrial front occupied by multistudio) — party walls both sides | DataSF footprints; DPR form; Jan 2025 photography |

### 2.2 Sources

- `https://data.sfgov.org/resource/ynuv-fyni` (DataSF Building Footprints, LiDAR-derived) — the authoritative footprint polygon `SF3775065` and the 7.48 m modal / 7.63 m median heights. **This is also the pipeline's primary bake input** (`pipeline/buildings.mjs` header), so it is the geometry the exclusion radius in 2.13 is sized against
- `https://data.sfgov.org/resource/wv5m-vpq2` (SF Assessor Historical Secured Property Tax Rolls) — 1959, block/lot, 2 storeys, floor area, construction type, zoning
- `https://data.sfgov.org/resource/i98e-djp9` (SF Building Permits) — 13 permits 1988–2024; the 2017–18 re-face and the 10 ft rear fence
- `https://data.sfgov.org/resource/g8m3-pdis` (SF Registered Business Locations) — tenant history and the "2nd Fl" suffix
- `https://default.sfplanning.org/GIS/SouthSoMa/Docs/2009-06-30_South%20Park%20Dform.pdf` — SF Planning / Page & Turnbull, *South Park Historic District*, DPR 523D, 30 June 2009: the 1854–1935 period of significance, the 27-building / 23-contributor count, and the parcel table entry `3775065 | 150 | SOUTH PARK | HP6. 1-3 Story Commercial Building | 1959 | 6L`
- `https://www.openstreetmap.org/way/124884352` — footprint and `height = 8`
- `pipeline/data/overture_buildings.geojsonseq` — the bake's gap-fill layer; carries `height = 8.0` on this footprint, `6.0` on 156 and `10.0` on 140
- Google Street View, South Park Street pano (capture Jan 2025) — the whole front elevation: black painted brick over white stucco, the two oxblood-framed windows, the steel canopy, the gooseneck lamps, the shopfront divisions, the "150" numerals, and the "FOR LEASE" sign
- Google Street View, Taber Place pano (capture Jan 2025) — the rear yard, the 3 m black steel fence with spear finials and festoon lights, and the charcoal rear elevation with its band of brown-framed windows
- Google Maps satellite (Vexcel imagery, 2026) — the flat roof, its skylights, and the wedge plan against the curving street
- Exa (`web_search_advanced_exa`), 16 Aug 2026 — queries `"150 South Park San Francisco building"` and `"150 South Park Street San Francisco office building photo facade brick"`. Yielding domains: `loopnet.com` (APN 3775-065, 3,520 SF office — *observed (listing record)*), `kidsonland.com` (owner/manager, no photos on the page), `images1.showcase.com` (Kidson lease flyer PDF), `property.compstak.com` (the neighbour at 140 South Park: 1907, 2 storeys, renovated 2018, Flourish Ventures). No architectural press, no architect, and no published photograph of this building was found — the visual dossier below is Street View and satellite only
- `https://en.wikipedia.org/wiki/South_Park,_San_Francisco` — the oval's history and 550-foot plan, context only

### 2.3 Orientation and placement

The building sits on the **north-west rim of the South Park oval, at its west tip**, where
South Park Street curves around the end of the ellipse. That curve is the whole story of
this footprint: the frontages either side of it swing through 24 degrees over four lots
(140 South Park faces 135.0°, 150 faces 133.5°, 156 faces 117.2°, 160 faces 111.0°), and
because the party walls stay on the old rectilinear lot lines while the street edge
follows the curve, 150's lot comes out as a **wedge**.

The building fronts South Park Street to the south-east and backs onto a rear yard and the
Taber Place alley to the north-west, with party walls on both long sides.

Measured footprint polygon, in Blender coordinates (metres, `+X` east, `+Y` north),
clockwise, already centred on the anchor `-122.3947673, 37.7813810`:

```
( 10.14,  -4.15)   <- street corner, NE side (party wall meets the frontage)
(  6.37,  -8.21)   <- street corner, SW side
( -5.46,  -2.73)   <- 26 degree kink in the SW party wall
( -9.59,   2.42)   <- rear corner, SW side
( -2.69,   9.27)   <- rear corner, NE side
```

(The authoritative version is the DataSF ring for `mblr = SF3775065`; the executing agent
should re-pull it rather than retype these numbers.)

Edges, with outward normals:

| Edge | Length | Faces | Elevation |
|---|---|---|---|
| street end | **5.34 m** | SE 133.5° | **South Park Street front** — the hero elevation |
| NE party wall | 18.57 m (one straight run) | NE 46.3° | 140 South Park |
| rear end | 9.72 m | NW 315.2° | **rear yard / Taber Place** |
| SW party wall, rear run | 6.60 m | SW 231.3° | 156 South Park |
| SW party wall, front run | 12.89 m | SW 204.9° | 156 South Park |

Read in a frame aligned to the lot's long axis, where `+v` points toward the street, the
building is 18.7 m deep and tapers from 9.72 m wide at `v = -9.3` to 5.34 m wide at
`v = +9.4`. The taper is not uniform: the north-east wall is dead straight for its whole
18.57 m, and **all** of the narrowing happens on the south-west side, in two runs meeting
at a 26 degree kink 6.6 m from the back. Build it that way — a symmetric taper will look
right in plan and wrong in every elevation.

Because of the ~43° heading the axis-aligned bounding box is ~20 x 18 m for a building
that is nowhere more than 9.72 m wide. That is correct.

### 2.4 What each side shows

**South-east (South Park Street front)** — The hero elevation, and 5.34 m of it. Two
storeys, split hard across the middle:

- The **upper storey is near-black / charcoal painted brick** (roughly `#2f3338`), with
  the coursing still legible under the paint. It is capped by a completely plain flat
  parapet — no cornice, no coping band, no ornament of any kind, and noticeably **lower
  than 140 South Park's bracketed cornice next door**.
- Two **square-ish punched windows**, roughly 1.7 m wide by 1.6 m tall, evenly spaced,
  each in a thick **oxblood / copper-brown painted frame** with a matching sill. Flat
  face, no bays, no reveals to speak of. A "FOR LEASE" sign hangs between them (Jan 2025,
  temporary — do not model it).
- A thin **white drip line** where the brick meets the stucco below.
- The **ground floor is bright white stucco** (roughly `#f4f2ee`), a full storey taller
  than a domestic floor at ~3.8 m.
- A **flat black steel canopy** projects ~1.0 m across the middle of the frontage, carried
  on two thin diagonal rod stays back to the wall, with a **black gooseneck wall lamp**
  either side of it.
- Under and beside the canopy: a large **black-framed plate-glass display window** at
  centre-left, a **tall narrow glazed entrance door with a transom** in a black frame at
  the north-east end, and a **narrow black-framed secondary door** at the south-west end.
- The address **"150"** in tall, thin, widely-spaced black numerals on the white wall
  between the display window and the entrance door. It is the single most legible piece of
  graphic identity on the building and should survive to thumbnail size.
- A small security camera sits at the black/white junction on the south-west side.

**North-west (rear, onto the yard and Taber Place)** — The same charcoal wall, with a
**horizontal band of two large windows** in the same brown frames, and the same plain flat
parapet. Blunter and flatter than the front; no canopy, no white base. Seen in the real
world only over a 3.05 m black steel fence with spear finials, across a planted rear yard
strung with festoon lights — but the app's aerial camera reads it plainly, so it must be
built properly. *Evidence: one Jan 2025 pano through the fence; see 2.15.*

**North-east / south-west flanks** — Party walls. Blank painted brick, hard up against
140 and 156 on both sides for the full 18.57 m and 19.5 m. Do not invent a window grid or
a light well; there is no gap on either side.

**Top** — One **flat membrane roof** at ~7.5 m inside a plain parapet ring, with a scatter
of **skylights** and one small vent cluster visible in the 2026 satellite imagery. The
permit record contains no penthouse, no stair bulkhead and no solar. This roof was never
designed and inventing plant on it would be a lie about the building — but it *is* the
surface the app's camera sees most, so the parapet ring, the skylight rhythm and the
wedge plan have to do the work. See 2.9.

### 2.5 Recognition cues (ranked)

1. **Black brick box on a white stucco base** — a hard, high-contrast horizontal split at
   mid-height, and the exact inverse of 155 South Park across the oval
2. The **wedge plan**: a 5.3 m frontage on an 18.7 m deep lot that widens to 9.7 m behind
3. The **two oxblood-framed square windows**, the only warm colour on the building
4. The **flat black canopy on rod stays** with a gooseneck lamp either side
5. The thin **"150"** numerals on white stucco

### 2.6 Miniature translation

**Preserve**

- The hard two-tone split and its height on the wall (the black band is the taller of the
  two, and the split sits at about 47% of the crest)
- The plain flat parapet — resist the temptation to give it a cap band; its plainness next
  to 140's cornice is a recognition cue
- The wedge plan, the straight north-east wall and the 26 degree kink on the south-west
- The oxblood frames, and the fact that there are exactly two windows

**Simplify / exaggerate**

- The brick coursing becomes flat colour. Do not model courses, and do not try a
  brick-texture stand-in — flat colour only (asset contract)
- The window frames thicken to ~0.25 m and gain ~0.08 m of relief so the oxblood reads at
  thumbnail size; this is the one place semantic exaggeration is spent
- The canopy becomes one 0.20 m slab with two 0.06 m rod stays; the gooseneck lamps become
  a small arm-and-shade pair, ~0.5 m across, or are dropped if they cost more than ~250
  triangles between them
- The shopfront becomes: one display window, one entrance door with transom, one narrow
  secondary door, and the "150" as three extruded numerals ~0.5 m tall, 0.04 m proud
- The rear window band becomes one three-part opening in a single frame
- Roof clutter becomes three skylights and one vent cluster; nothing else
- Security camera, downpipes, the lease sign, the address plate lettering on the doors and
  the wall-mounted standpipe all disappear

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not
a straitjacket — adjust after the first aerial review render.

1. Main volume: extrude the 2.3 footprint from z=0 to z=7.5, `Toy_ink` (the charcoal
   brick). Keep the wedge and the 26 degree kink.
2. Ground-floor skin, z=0 to z=3.80, applied to the **front 12 m** of both party walls and
   the whole frontage: a `Toy_white` panel standing 0.06 m proud of the brick, with a
   0.10 m white drip lip along its top edge. Behind the front 12 m the party walls are
   never visible, so the skin can stop.
3. Front shopfront openings, all in the 5.34 m frontage, recessed 0.15 m:
   - display window 2.30 x 1.90 m, `Toy_glass` in a 0.12 m `Toy_ink` frame, centred
     0.9 m south-west of the frontage midpoint, sill at z=0.85
   - entrance door 1.05 x 2.55 m with a 0.45 m transom above, `Toy_glass` in a 0.12 m
     `Toy_ink` frame, at the north-east end
   - secondary door 0.85 x 2.30 m, `Toy_ink`, at the south-west end
4. Canopy: a 0.20 m `Toy_roofd` slab at z=3.15, projecting 1.0 m, 3.4 m wide, centred on
   the display window and entrance; two 0.06 m `Toy_steel` rod stays back to the wall at
   z=3.75.
5. Gooseneck lamps: two `Toy_roofd` arm-and-shade pairs at z=3.30, 0.5 m across, one at
   each end of the canopy.
6. Address numerals: "150" in `Toy_ink`, 0.50 m tall, 0.04 m proud, on the white wall
   between the display window and the entrance door, at z=2.1.
7. Upper windows, z=4.55 to z=6.15: two openings 1.70 x 1.60 m, recessed 0.18 m,
   `Toy_glass`, each in a 0.25 m proud `Toy_oxblood` frame with a 0.12 m sill. Space them
   evenly on the 5.34 m frontage (centres about 1.45 m either side of the midpoint).
8. Front parapet: z=7.5 to z=**8.0**, following the frontage and returning ~1.5 m down
   each party wall, 0.25 m thick, `Toy_ink`. The frontage run sets the bounding-box top
   and must land exactly on 8.0.
9. Rear parapet at z=7.5 to z=7.85, `Toy_ink`, along the 9.72 m rear edge.
10. Rear elevation, z=4.55 to z=6.15: one three-part opening 4.2 x 1.6 m, recessed 0.18 m,
    `Toy_glass` in a 0.25 m `Toy_oxblood` frame.
11. Roof deck at z=7.5, `Toy_roofd`: three `Toy_glassl` skylights ~1.2 x 0.9 m spaced down
    the long axis, and one vent cluster (2 blocks, ~0.5 m tall, `Toy_steel`) near the rear
    third. Nothing reaches above 7.9 m.
12. Bevel 0.10 m, 2 segments.

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_ink` | `#3a3530` | the painted-brick upper storey, both parapets, shopfront frames, secondary door, the "150" numerals |
| `Toy_white` | `#f7f4ec` | the ground-floor stucco skin and its drip lip |
| `Toy_oxblood` | `#8c4a3c` | the four upper-window and rear-window frames and sills (see the note below) |
| `Toy_glass` | `#2a4d73` | display window, doors, upper and rear windows |
| `Toy_glassl` | `#6f95b8` | roof skylights |
| `Toy_roofd` | `#45454a` | canopy slab, gooseneck lamps, roof deck |
| `Toy_steel` | `#9aa0a6` | canopy rod stays, roof vent cluster |
| `Toy_glass_Glow` | `#6f95b8` | the lit shopfront and the two lit upper windows at night |
| `Toy_gold_Glow` | `#caa64a` | the warm pool of light under the canopy |

Note on the window frames: the real colour is a dark warm brown-red with no exact palette
match. `Toy_rust` (`#a86444`) is too orange and too light for a frame this small, and
`Toy_coral` far too saturated. Off-palette is a WARN not a FAIL, so a dedicated
`Toy_oxblood` at roughly `#8c4a3c` is permissible, on the same argument that 155 South
Park's `Toy_peach` and 380 Brannan's `Toy_slate` were. Decide from the aerial render and
record the decision in `REPORT.md`.

**Night state (required).** Glow surfaces must be thin shells proud of the opaque glazing —
the app renders `_Glow` in a separate layer that is ~12% alpha by day, so a primary surface
must never be authored as glow. Hero glow: the **shopfront** — display window and entrance
— plus a warm `Toy_gold_Glow` wash under the canopy, reading as the one lit ground floor at
the head of the park. Supporting accent: the **two upper windows**, cool and both lit,
because that floor is a live/work unit and a home with one window lit and one dark reads as
an office. The rear elevation does not glow; a back yard that lights up would misread.

### 2.9 Top surface

One flat roof, one parapet ring, on a wedge, in a district the camera flies over
constantly. Three things carry it: keep the parapet ring a shade lighter than the deck
inside it so the ring reads from above; let the **wedge itself** be the composition — the
taper is far more legible from the aerial camera than from the street, and it is the only
plan in the row that is not a rectangle; and space the skylights down the long axis so
they draw the eye along that taper. Nothing else. This building's roof was never designed,
and a mechanical farm on it would be an invention (2.15).

### 2.10 Scope

**In the GLB:** the two-storey wedge volume, the white ground-floor skin, the shopfront
and its three openings, the canopy, rod stays and gooseneck lamps, the "150" numerals, the
two upper windows, both parapets, the roof and its furniture, the rear elevation

**Not in the GLB:** South Park Street, the oval and its trees, Taber Place, the rear yard
and its 3.05 m steel fence, 140 and 156 South Park, sidewalk, vehicles, people, plinths,
cameras or lights, and the "FOR LEASE" sign

### 2.11 Triangle budget

Cap 6,000 — a background building at 155 South Park's level (4,048 tris shipped) and one
step below 380 Brannan (7,760). Suggested split: the wedge volume, parapets and white skin
~1.5k; shopfront openings, doors and frames ~1.5k; canopy, stays, lamps and numerals ~1.2k;
two upper windows and the rear band ~1.0k; roof furniture ~0.8k.

### 2.12 Draft manifest entry

```json
{
  "id": "150-south-park",
  "file": "150-south-park.glb",
  "anchor": [
    -122.3947673,
    37.781381
  ],
  "targetHeightM": 8.0,
  "cat": 3,
  "name": "150 South Park",
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

- **New landmark.** Add a `pipeline/lib/landmarks.mjs` entry (`id: '150SouthPark'`,
  `lon: -122.3947673`, `lat: 37.7813810`, `height: 8.0`, `exclude: 4.5`) and re-bake the
  affected tiles, or the baked procedural building on this exact footprint will intersect
  the GLB.

- **The exclusion radius is `4.5`, and the window is narrow at both ends.** Measured
  against the real bake input — DataSF `ynuv-fyni` (primary) and
  `pipeline/data/overture_buildings.geojsonseq` (gap-fill), distances in metres from the
  anchor:

  |  | nearest vertex | centroid |
  |---|---|---|
  | own footprint (DataSF SF3775065) | 6.10 | **3.24** |
  | own footprint (Overture) | 6.56 | 1.37 |
  | 156 South Park (DataSF SF3775066) | **6.10** | 8.50 |
  | 156 South Park (Overture) | 6.56 | 9.52 |
  | 140 South Park (DataSF SF3775064) | 11.34 | 13.18 |
  | 140 South Park (Overture) | 9.83 | 9.73 |

  `excluded()` in `pipeline/buildings.mjs` drops a footprint when **either** its centroid
  **or any ring vertex** falls inside the circle, so the floor is our own DataSF centroid
  at 3.24 m and the ceiling is 156 South Park's nearest vertex at 6.10 m. **The safe
  window is 3.24 < r < 6.10**; 4.5 sits mid-window with 1.3 m of headroom over our own
  centroid and 1.6 m below the neighbour.

  Two traps here. First, this footprint is cleared **by its centroid, not by a vertex** —
  the usual half-diagonal rule would give ~9.5 m and would delete 156 *and* 140 and punch
  a two-lot hole in the row. Second, **150 and 156 share a party-wall node**: both report
  a nearest vertex of exactly 6.10 m in DataSF and exactly 6.56 m in Overture, which is
  not a coincidence, it is the same point. There is no radius that reaches 156's corner
  without reaching ours, so the ceiling is hard.

  Run the same drop-count check 380 Brannan documents: the re-bake must drop **exactly
  one** procedural footprint.

- `camera` preset: `{ distance: 140, yaw: 46, pitch: 26 }`. `camera.js` puts the eye at
  target + distance·(sin yaw, ·, cos yaw) with +x east and +z south, so yaw 46 stands
  south-east of the building — square onto the South Park front, looking back over the
  head of the oval. 140 m suits an 8.0 m building (cf. 135 South Park at 150 m for 8.5 m).

- `loadRadius`: the skill's default formula gives `max(2500, 8.0 × 30) = 2500` m. Take the
  default, as 155 South Park and 135 South Park did.

- This is the eighth South Park row building in the manifest. The open question raised in
  380 Brannan's 2.13 and sharpened in 155 South Park's stands: a manifest of individual
  South Park row buildings does not stream well, and the kit/instancing route
  (`KIT-INTEGRATION-PROMPT.md`) is probably the right long-term home for this class. This
  one has an unusually good argument for staying bespoke, though — the wedge plan is not
  something a kit piece can express.

- **Batch mode applies.** This landmark is being built alongside others; stage 5 runs the
  bake for QA and then throws it away (`git checkout -- app/public/tiles api/_data`), and
  the branch commits source only. See `docs/asset-pipeline/ADDRESS-TO-ASSET.md`, "Batch
  mode".

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Bounding-box top exactly 8.0 m (loader scale lands at 1.0), set by the front parapet
- [ ] No roof furniture above 7.9 m
- [ ] Dimensions plausible in meters and consistent with 2.1 (XY bbox ~20 x 18 m is expected)
- [ ] The wedge is asymmetric: straight NE wall, kinked SW wall
- [ ] Triangles at or under 6,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the shopfront, the canopy wash and the two upper windows; glow shells proud of opaque glazing
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (per-object signed volume for the union of solids; ray test residual <= 0.15%)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + contact sheet + night render regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

- **The LiDAR `hgt_max` of 9.95 m is not the crest, and it is the trap this plan most
  wants you to avoid.** It sits 2.3 m above the median on a footprint whose height
  standard deviation is 0.78 m — a 3σ outlier — and the matching artifact at the other end
  is a 5.20 m `hgt_min`. There is a large street tree at the corner of the frontage in the
  2026 satellite imagery, and the permit record for this lot contains no penthouse, no
  stair bulkhead and no rooftop plant of any kind across 13 permits from 1988 to 2024.
  This is the same failure mode 592 Third Street and 250 Van Ness document. **Build to
  8.0 m.** If you find real evidence of a rooftop structure, the target height moves and
  the manifest entry with it.
- **8.0 m is the weakest number in this dossier that is still load-bearing.** It rests on
  the OSM `height = 8` tag (which Overture repeats, so those two are one source, not two)
  plus a parapet read off a single street-level photograph on top of a measured 7.48 m
  roof-deck mode. The internal check is reassuring — taking 140 South Park's crest as the
  scale reference, the photograph puts the two-tone split at 3.8 m and the upper windows
  at 4.7–6.3 m, which is a coherent set of floor heights for a 7.5 m roof deck — but it is
  still a photograph. Re-verify before normalising the export.
- **The Assessor's "Commercial Office" use code is only half the building.** The 2017
  permits name an "upper level unit", a "live/work bathroom" and a "residential entry"
  alongside the "commercial tenant space", and a 2014 business registered at "150 South
  Park St **2nd Fl**". The upper floor is residential live/work. This matters for exactly
  one decision — the night state — but it is the decision most likely to be got wrong from
  the assessor record alone.
- **The rear elevation is the weakest *evidence* in this dossier.** It was read from a
  single Jan 2025 Taber Place pano, shot through a 3.05 m steel fence across a planted
  yard, at an angle that puts the parapet against bright sky. The charcoal wall, the flat
  parapet and the band of two brown-framed windows are all legible; their dimensions are
  not. Everything in 2.7 step 10 is *inferred*. Confirm it before modelling, and if you
  cannot, say so in `REPORT.md` rather than presenting the rear as observed.
- **No architect, no builder, no published photograph.** Exa found no architectural press,
  no permit-record designer for either the 1959 building or the 2017 re-face, and no
  photograph of this building anywhere outside Street View and real estate listing
  records. Unlike the contributors on this block, 150 South Park has no DPR narrative — the
  district form records it only as a table row. The visual dossier here is Street View and
  satellite; treat it as such.
- **The 5.34 m frontage is real and will feel too narrow while you are modelling it.** It
  is measured, it is corroborated by the neighbours (140 at 6.84 m, 156 at 5.92 m, 160 at
  6.26 m — this is a row of very narrow frontages), and it is confirmed in the photograph,
  where 150's facade is visibly about four fifths the width of 140's. Everything on the
  front elevation has to fit inside it: two windows above, and a display window plus two
  doors below. Do not widen it to make the shopfront comfortable.
- **The wedge is easy to lose.** The temptation is to model a rectangle 7.5 m wide and be
  done. The taper is 4.4 m across 18.7 m, all of it on one side, and it is the second
  recognition cue on the list — it is also what makes the model sit correctly against 140
  and 156 when the exclusion zone drops the procedural block.
