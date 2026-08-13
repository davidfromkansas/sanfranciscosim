# 370 Brannan Street — SF-SIM asset plan

A 1937 wood-frame SoMa infill shop-and-loft, two doors NE of 380 Brannan on the same
block face. Seven metres of street frontage and twenty-four metres of depth: the
narrowest building yet planned in this set, and its narrowness *is* the subject. The
Brannan elevation is a single recessed panel inside a raised stucco frame, with a wide
mid-band carrying painted numerals, a black steel-sash window band above, and one
cobalt-blue door — the only saturated colour on the block face. Not a monument and not
even a character warehouse: the design brief is "the thin one between two fat
neighbours", and the model has to earn its place on proportion and one accent.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/370-brannan/`. This document is the plan only: Part 1 is the runnable task
prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `370-brannan` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3938572, 37.7807602` |
| Target height | **7.63 m** to the parapet crest; roof deck 7.05 m |
| Footprint | 7.00 m (Brannan frontage, SE) x 23.83 m deep; 166.9 m2, measured |
| Triangle cap | 7,000 |
| Category | `3` (office) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 370 Brannan Street GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of 370 Brannan Street in San Francisco and deliver
it as a downloadable, validated GLB.

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
7. `artifacts/380-brannan/` — the closest reference implementation: the same block
   face, the same SoMa 45-degree heading, the same two-storey flat-parapet typology,
   and a build script whose footprint/edge/panel helpers this asset should reuse
   rather than reinvent
8. `docs/asset-plans/370-brannan.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract, `AGENTS.md`
governs repository and integration rules. Do not invent a new style and do not copy
visual instructions from unrelated prompts.

## Must capture

- The **proportion**: a 7 m wide, 23.8 m deep, 7.6 m tall slab — nearly 3.4 times as
  deep as it is wide. Anything that reads as a normal-width building is wrong.
- The **framed-panel front**: a raised flat stucco border (pilaster each side, wide
  band across the middle) enclosing a recessed facade panel. This is the composition.
- The **painted "370" numerals** on the left end of the mid-band.
- The **cobalt-blue ground-floor door** — the one saturated colour, and the strongest
  single cue at thumbnail size.
- The dark plate-glass storefront window beside the door.
- The upper-floor **black steel-sash window band**, wide and multi-pane, set deep.
- A flat membrane roof with a plain parapet and **two large square pyramid skylights**
  spaced along the length, plus a smaller roof light nearer the street and a hatch.
- The fact that it is **lower than both neighbours** (LiDAR: 370 = 7.63 m, 374 = 8.80 m,
  366/362 = 8.58 m). Do not round the height up to match the block.

## Research 370 Brannan Street independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world orientation,
and gather references covering:

- The Brannan (SE) elevation in detail — the frame proportions, the vertical position
  of the mid-band, the pane grid of the upper window
- The Varney Place (NW) rear, which this dossier could **not** source (see 2.15) —
  everything about that elevation here is *inferred*, and confirming it is the single
  highest-value piece of research you can do
- Aerial and roof/top views (skylight positions and sizes)
- Day and night appearance

Prefer architect/engineer publications, owner or institutional material, planning and
permitting documents, architectural press, geolocated photography, and aerial/satellite
imagery. Never rely on a single photograph, a single AI-generated image, or a single
unsourced 3D model. Separate verified facts from visual inference; if sources disagree,
document the disagreement and decide.

**Two source conflicts are already resolved in 2.1 — re-check them, do not silently
re-inherit the wrong value:** OSM `height=7` on way/124890321 is the LiDAR *median*
(roof deck), not the crest, which is 7.63 m; and the OSM footprint is 5.83 m wide where
the DataSF LiDAR footprint and the assessor lot both say **7.00 m** — OSM's trace is
`source=Bing` and roughly a metre narrow. Build on the DataSF polygon in 2.3.

## Create a reference dossier

Write `artifacts/370-brannan/REFERENCE.md` containing: source links and what each
establishes; verified dimensions and location; orientation; observations from all four
sides and above; the 3-5 strongest recognition cues; features to preserve; features to
simplify; uncertainties and conflicting evidence. A contact sheet of attributed
reference thumbnails is welcome if legally permissible — do not commit copyrighted
full-resolution imagery.

## Make your own design decisions

Follow the conversion process in `docs/styles/miniature-toy.md` §22: identify the
recognition cues, strip nonessential information, rebuild the massing from a few
confident volumes, exaggerate only the signature features, simplify the facade into
broad rhythms, deliberately design every surface visible from above, evaluate from the
app's high three-quarter aerial camera, then simplify again.

This is a **background building** in the style bible's detail budget (§21) — a tier
below 380 Brannan, which is itself a secondary building. One volume, one facade
composition, one accent colour, a designed but quiet roof. Resist adding ornament: at
7 m wide this asset is a few dozen pixels across in the default view, and every extra
element is noise.

The finished asset must be immediately recognizable as 370 Brannan Street, consistent
with the real building from all four sides and above, architecturally credible, and a
premium handcrafted miniature — not photorealistic, not voxel art, not generic
low-poly, and never accurate in one view while invented in the others.

## Scope of the exported asset

Export the single 1937 building: stucco body, parapet, the framed front composition,
all four elevations' openings, roof deck and roof furniture.

Do not include unrelated surrounding city geometry: Brannan Street, Varney Place, the
neighbouring buildings at 372-374 and 362-366, the street tree in front of the door,
South Park, the sidewalk, parked cars, people, plinths, cameras or lights. Temporary
context may appear in review renders but must not leak into the GLB.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary `.glb`;
real-world meters; origin at base center; minimum geometry Z ~ 0; applied transforms;
no negative scales; outward normals; no duplicate or foreign geometry; no image
textures; no transparency; flat-color materials named `Toy_*` from the project palette;
`_Glow` suffix only on surfaces that glow at night; no `Toy_body`; no cameras, lights,
animations, armatures or constraints; no external dependencies; at most 7,000 triangles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model drops
into the city at its real-world heading — the loader applies no rotation
(`placeGeneric` in `app/src/assets.js` only scales and positions). The Brannan Street
front faces **southeast, bearing 134.9°**; the building is rotated roughly 45° off the
world axes, so build directly on the measured footprint polygon in 2.3 rather than
modelling an axis-aligned box and rotating it. Record the measured heading in
`REPORT.md`.

**Height normalization:** the tallest geometry in the export (the parapet crest) must
land at exactly **7.63 m** so the loader's `targetHeightM / measuredHeight` scale is
1.0. Nothing on the roof may poke above it.

## Reproducible Blender workflow

Blender 5.2 LTS. Headless: `blender -b --python script.py -- args`.

Keep `artifacts/370-brannan/build_370_brannan.py` (deterministic build script),
`artifacts/370-brannan/370-brannan.blend`, and `artifacts/370-brannan/370-brannan.glb`.
The script must rebuild the model reliably enough for future revision. Do not modify or
rename an unrelated existing GLB to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras: `370-brannan-top.png`,
`370-brannan-north.png`, `370-brannan-east.png`, `370-brannan-south.png`,
`370-brannan-west.png`, plus `370-brannan-contact-sheet.png`, at least one high
three-quarter aerial beauty render `370-brannan-aerial.png`, and a night render
`370-brannan-aerial-night.png`.

The four elevations must share scale, framing, lighting, exposure and projection; use
orthographic or long-lens cameras; label directions from the researched orientation;
the top view must clearly show the parapet ring, both pyramid skylights, the small roof
light and the hatch; the aerial view uses the style bible's camera assumptions (30-50
degrees down, long lens). Simple tabletop lighting, neutral warm background, minimal
depth of field, and every image must depict the same exported model.

Note that on this footprint the elevation renders are deceptive: the 7 m ends and the
23.8 m flanks are at 45° to the world axes, so a "north" orthographic camera shows a
three-quarter view of two faces at once. Label the images by world direction as
required, but judge the facades from the aerial.

## Validate the exported GLB

Re-import `370-brannan.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture count,
camera count, light count, animation count, applied-transform status, negative-scale
status, normal-orientation status, unexpected geometry, and per-material contract
compliance. Render at least one review image from the re-imported asset. Write
`artifacts/370-brannan/validation.json` and `artifacts/370-brannan/REPORT.md`.

Note that the axis-aligned XY bounding box will be roughly **21.9 x 21.7 m** even
though the building is 7.0 x 23.8 m — that is the expected consequence of a ~45°
real-world heading, not a scale error.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this draft
entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "370-brannan",
  "file": "370-brannan.glb",
  "anchor": [
    -122.3938572,
    37.7807602
  ],
  "targetHeightM": 7.63,
  "cat": 3,
  "name": "370 Brannan Street",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a separate, explicitly requested job — run `docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in `docs/asset-plans/370-brannan.md`.
````

---

## Part 2 — Research and design dossier

Compiled 12 August 2026 from the sources in 2.2. Values marked *inferred* are visual or
derived estimates, not published figures — the executing agent must re-verify anything
it relies on.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Built | 1937 | SF Assessor secured roll 2025, block 3775 lot 020 |
| Storeys | **2** | SF Assessor roll AND all four building permits 1990-2015 (`number_of_existing_stories = 2`) — no conflict here, unlike 380 |
| Construction | **Wood frame (Type V)**, stucco-faced | SF building permits 2009-2014, `existing_construction_type_description = "wood frame (5)"` |
| Block / lot | 3775 / 020 | SF Assessor; DataSF footprint `mblr = SF3775020` |
| Footprint | 166.9 m2; 7.00 m (SE frontage) x 23.83 m deep; a clean rectangle | DataSF LiDAR building footprint, reprojected — **measured** |
| DataSF ring area as published | 173.9 m2 | includes four sub-600 mm survey-noise segments, dropped in 2.3 |
| OSM footprint (cross-check) | 5.83 x 24.24 m — **1.2 m too narrow** | OSM way/124890321, `source=Bing`; see 2.15 |
| Roof deck height | 7.05 m above ground | DataSF LiDAR `hgt_median_m` 7.07, `hgt_majoritycm` 7.45, std 0.33 m — **measured**, and the low std confirms one uniform flat roof with no lower rear wing |
| Parapet crest / max feature | **7.63 m** above ground | DataSF LiDAR `hgt_maxcm` 763 — **measured** |
| Ground elevation | 9.34 m (NAVD88) | DataSF LiDAR `gnd_min_m` — app terrain handles this, not the asset |
| Assessor floor area | 3,700 sq ft (343.7 m2) | ~2.06x the footprint — two full floors, no mezzanine |
| Lot area | 1,760 sq ft (163.5 m2) | commercial listings; agrees with the measured footprint to ~2% |
| Zoning / use | CMUO; assessor class Industrial, permitted use "public assmbly other" since 2013, office before that | SF Assessor, SF permits, listings |
| Recent occupants | Typeform US (floor 1), Spherecast, radiantgraph, ARRIS Design Partners | OSM office node 13765490846, Google Maps place listing, storefront decal |
| Frontage heading | Brannan front faces 134.9° (SE); rear faces 315.0° (NW) | measured from the DataSF footprint polygon |
| Rear condition | Varney Place alley, **4.7 m** from the rear wall | measured against OSM highway geometry — the rear is a real, exposed elevation |
| Neighbour heights | 372-374 (lot 021) 8.80 m; 362-366 (lot 018) 8.58 m | DataSF LiDAR `hgt_maxcm` — 370 is the **lowest** of the three |

### 2.2 Sources

- https://www.openstreetmap.org/way/124890321 — address, `building=yes`, `height=7`, `source=Bing`
- `https://data.sfgov.org/resource/ynuv-fyni` (DataSF Building Footprints, LiDAR-derived) — authoritative footprint polygon, the 7.05 / 7.63 m heights, and the neighbour heights
- `https://data.sfgov.org/resource/wv5m-vpq2` (SF Assessor Historical Secured Property Tax Rolls, 2025) — 1937, block/lot, 2 storeys, 3,700 sq ft
- `https://data.sfgov.org/resource/i98e-djp9` (SF Building Permits) — 2 storeys, wood-frame construction type, 2009 office fit-out, 2013 T.I. and channel-letter sign
- Google Street View, Brannan Street pano `QGmjHr1j26kBQJg4CIIlyQ` (capture 2025) — the entire front-elevation description in 2.4
- Esri World Imagery and Google satellite tiles at z20-21 (2026) — roof: membrane deck, two square pyramid skylights, one small roof light, one hatch
- Google Maps place listing for 370 Brannan St — current occupants
- Commercial listing copy (LoopNet / Crexi / Cityfeet, 370 Brannan St) — 3,700 sq ft, 1,760 sq ft lot, built 1937, "high ceilings, natural light, skylights". Listing pages themselves are 403 to automated fetches; figures reached via search result summaries and cross-checked against the assessor roll, which they match.

### 2.3 Orientation and placement

The building sits mid-block on the northwest side of Brannan Street between 372-374 to
the southwest and 362-366 to the northeast, with party walls on both long sides and its
rear on the Varney Place alley. It is rotated about 45° from the world axes, like the
whole SoMa grid — the same heading as 380 Brannan two doors along.

Measured footprint polygon, in Blender coordinates (metres, `+X` east, `+Y` north),
counter-clockwise, already centred on the anchor `-122.3938572, 37.7807602`:

```
(-10.946,   5.907)
(  5.999, -10.863)
( 10.941,  -5.901)
( -5.994,  10.857)
```

Edges, with outward normals:

| Edge | Length | Faces | Elevation |
|---|---|---|---|
| 0: `(-10.946,5.907) -> (5.999,-10.863)` | 23.84 m | SW 224.7° | southwest party wall (372-374) |
| 1: `(5.999,-10.863) -> (10.941,-5.901)` | 7.00 m | SE 134.9° | **Brannan Street front** |
| 2: `(10.941,-5.901) -> (-5.994,10.857)` | 23.82 m | NE 44.7° | northeast party wall (362-366) |
| 3: `(-5.994,10.857) -> (-10.946,5.907)` | 7.00 m | NW 315.0° | **Varney Place rear** |

Four sub-600 mm survey-noise segments in the published DataSF ring were dropped: the
tile bake simplifies rings at a 0.6 m tolerance anyway, so keeping them would make the
asset more precise than the city it sits in. Unlike 380 Brannan's chamfers these are
not a real building feature.

Because of the 45° heading the axis-aligned bounding box is ~21.9 x 21.7 m. That is
correct.

### 2.4 What each side shows

**Southeast (Brannan Street front)** — The only designed elevation, and it is one
composition: a raised flat stucco **frame** — a pilaster up each side, a wide band
across the middle — enclosing a recessed panel. Top to bottom the frame encloses, first,
a **wide black steel-sash window band** filling most of the upper storey, set well back
in its reveal, with a roughly 4-column by 3-row pane grid and a dark transom row behind;
then the **mid-band** itself, plain and slightly darker than the field, carrying the
painted numerals **"370"** at its southwest end; then the ground floor, split between a
**cobalt-blue solid door with a six-light window** at the southwest end and a large
**dark plate-glass storefront window** occupying the rest, with a small tenant decal on
the glass. Above the upper window the frame runs up into a plain parapet with no
cornice, no coping course, no ornament at all. The whole wall is painted a mid warm
gray; the frame reads one step lighter than the recessed field. A young street tree
stands directly in front of the door — not part of the asset.

**Northwest (Varney Place rear)** — **Not sourced.** No Street View coverage of the
alley was found and the satellite imagery only shows the roof edge. The 2.7 massing
recipe treats it as what this typology almost always is at the back — a plain stucco
wall with a service door and two small high windows — and every number for it is
*inferred*. See 2.15; this is the dossier's one real hole.

**Northeast / southwest flanks** — Party walls. Both are built hard against neighbours
that are ~1 m taller, so in reality only the top ~1 m of each flank and none of the
lower wall is ever visible from the street. From the app's aerial camera the flanks are
still drawn, so build them as plain blank stucco with no openings; inventing a window
grid on a party wall would be a straightforward lie.

**Top** — A pale flat membrane roof inside a plain parapet, with visible transverse seam
lines. Two **square pyramid skylights** — raised pale curbs with dark glazing, roughly
2.6 m square — sit on the centre line, one about a third of the way in from the rear
and one just past the middle. A smaller rectangular dark roof light, roughly 1.6 x 1.0 m,
sits between the second skylight and the street. A small pale hatch box sits near the
southwest edge two-thirds of the way back. No HVAC plant, no penthouse, no masts: this
is a small wood-frame building and its roof is genuinely quiet. That quietness is the
design problem — the two skylights are what has to carry it.

### 2.5 Recognition cues (ranked)

1. **The proportion** — a 7 m wide slab 23.8 m deep, visibly narrower and lower than
   both neighbours. At city scale this is the whole recognition.
2. **The framed front panel** — raised border with a wide mid-band, the numerals on it
3. **The cobalt-blue door** — the only saturated colour, and the only thing that
   survives at thumbnail size besides the silhouette
4. The black steel-sash upper window band
5. The two square pyramid skylights on an otherwise empty roof

### 2.6 Miniature translation

**Preserve**

- The 7.00 x 23.83 m footprint and the real 45° heading, exactly
- Being lower than both neighbours — the 7.63 m crest is not negotiable
- The framed-panel composition and the mid-band's position
- The blue door as the single accent

**Simplify / exaggerate**

- The upper window's ~12-pane grid becomes one recessed glazed panel with a 3-mullion
  division — the individual panes are sub-pixel
- The frame is thickened to 0.55 m wide and 0.10 m proud so it survives at thumbnail
  size; this is the one place semantic exaggeration is spent on the massing
- The painted numerals are **not** modelled as geometry and not textured (the contract
  forbids textures); their band is modelled and the numerals are dropped. Recorded here
  so the omission is a decision, not an oversight.
- The storefront decal, the tree, the sidewalk grate and the wall-mounted meter go
- The rear gets a service door and two small windows and nothing else
- The roof's seam lines go; the two skylights, the small roof light and the hatch stay,
  and the skylight curbs are thickened slightly so they read from above

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not a
straitjacket — adjust after the first aerial review render. `SKIN` = 0.10 m, the depth
the front frame stands proud of the wall.

1. Body: extrude the 2.3 footprint from z=0 to z=7.05 (roof deck), `Toy_stone` tinted
   warm gray, with a `Toy_roofd` top cap.
2. Parapet ring: z=7.05 to z=**7.63**, 0.30 m thick, following the footprint,
   `Toy_stone`. This sets the bounding-box top and must land exactly on 7.63.
3. Front recessed panel: on edge 1 only, a `Toy_stone`-darker field inset 0.06 m,
   spanning the full 7.00 m width from z=0 to z=7.63.
4. Front frame: raised flat border 0.55 m wide, 0.10 m proud, `Toy_trim` — a pilaster
   at each end of the front edge from z=0 to z=7.20, and the mid-band across the full
   width from z=3.40 to z=4.50.
5. Ground floor, on edge 1: a 1.00 m wide door opening z=0 to z=2.35 filled
   `Toy_navy` (the cobalt door) with a `Toy_trim` surround; a 3.90 m wide storefront
   window z=0.35 to z=3.20 filled `Toy_glass`, frame `Toy_ink`.
6. Upper floor, on edge 1: one 5.30 m wide steel-sash band z=4.60 to z=6.45, recessed
   0.22 m, fill `Toy_glass`, frame `Toy_ink`, with two 0.10 m `Toy_ink` mullions.
7. Rear, on edge 3 (*inferred*): a 1.10 m service door z=0 to z=2.30 filled
   `Toy_roofd`; two 0.90 x 0.90 m windows at z=4.90, fill `Toy_glass`.
8. Flanks (edges 0 and 2): blank. No openings.
9. Roof at z=7.05, `Toy_roofd` deck. Two skylights: pale `Toy_stone` curbs
   2.6 x 2.6 x 0.20 m with `Toy_glassl` pyramid caps to z=7.55, centred on the building
   axis at 8.4 m and 14.6 m back from the front edge; one `Toy_glassl` roof light
   1.6 x 1.0 x 0.25 m at 5.2 m back; one `Toy_roofd` hatch 1.1 x 0.9 x 0.45 m at 17.0 m
   back, offset toward the SW flank. Nothing exceeds z=7.63.
10. Bevel 0.12 m / 2 segments on the solids, 0.05 m / 1 segment on the applied frames,
    none on fills and glow shells — the same budget that kept 380 Brannan under cap.

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_stone` | `#d9d2c2` | body walls, parapet, skylight curbs |
| `Toy_trim` | `#f3efe6` | the raised front frame and mid-band, door surround |
| `Toy_navy` | `#2c4a70` | **the cobalt door — the signature accent** |
| `Toy_glass` | `#2a4d73` | storefront and upper-band glazing |
| `Toy_glassl` | `#6f95b8` | skylight caps, roof light |
| `Toy_roofd` | `#45454a` | roof deck, rear service door |
| `Toy_ink` | `#3a3530` | window frames and mullions, reveals |
| `Toy_glass_Glow` | `#6f95b8` | lit upper window band at night |
| `Toy_navy_Glow` | `#6db3d9` | the door's fanlight/threshold spill at night |

Note on the recessed field: the real wall is a mid warm gray with the frame one step
lighter. `Toy_stone` for the field and `Toy_trim` for the frame reproduces that
relationship, but both are lighter than reality. If the aerial render shows the building
disappearing into its pale neighbours, a dedicated `Toy_greige` at roughly `#b9b2a4` for
the field is permissible — off-palette is a WARN not a FAIL. Decide from the render and
record the decision in `REPORT.md`.

**Night state (required).** Glow surfaces must be thin shells proud of the opaque
glazing — the app renders `_Glow` in a separate layer that is ~12% alpha by day, so a
primary surface must never be authored as glow. Hero glow: the upper steel-sash band,
lit as one continuous panel — on a 7 m frontage a scatter of individually lit windows
would be indistinguishable mush, and one lit band is the more legible and more honest
reading of a single open loft floor. Supporting accent: a narrow spill at the door.
The storefront window does **not** glow; a dark shopfront under a lit loft is what the
street actually looks like at night, and it keeps the composition to one hero.

### 2.9 Top surface

A flat roof 7 m up in a district the camera flies over constantly, and the quietest roof
in this plan set. Two square skylights with pale curbs and light glazing on the centre
line, a small roof light toward the street, a hatch toward the rear, a continuous
parapet ring so the deck never reads as an open tray, and nothing else. Keep the deck
value clearly darker than the parapet so the ring reads from above, and keep the
skylight caps in `Toy_glassl` so the roof has two bright points — on a footprint this
narrow they are the only thing that distinguishes it from a blank strip.

### 2.10 Scope

**In the GLB:** the single 1937 building — stucco body, parapet, framed front
composition, front and rear openings, blank flanks, roof deck and roof furniture

**Not in the GLB:** Brannan Street, Varney Place, 372-374, 362-366, the street tree,
South Park, sidewalk, vehicles, people, plinths, cameras or lights

### 2.11 Triangle budget

Cap 7,000 — two thirds of 380 Brannan's, because this building has one designed
elevation instead of four and a roof with four objects instead of twelve. Suggested
split: body, parapet and recessed panel ~1.5k, front frame ~1k, front openings ~1.5k,
rear openings ~0.8k, roof furniture ~1.2k, slack ~1k.

### 2.12 Draft manifest entry

```json
{
  "id": "370-brannan",
  "file": "370-brannan.glb",
  "anchor": [
    -122.3938572,
    37.7807602
  ],
  "targetHeightM": 7.63,
  "cat": 3,
  "name": "370 Brannan Street",
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

- **New landmark.** Add a `pipeline/lib/landmarks.mjs` entry (`id: '370Brannan'`,
  `exclude: 3`) and re-bake the affected tiles, or the baked procedural building on this
  exact footprint will intersect the GLB.
- **The exclusion radius is the tightest in the registry, and it has to be.** Measured
  against the DataSF footprints `excluded()` actually consumes, from this anchor:
  this building's own footprint centroid is **0.59 m** away, but 372-374's centroid
  (`SF3775021`, itself a 7 m sliver) is only **6.57 m** away, and the nearest ring
  vertex of anything is 11.98 m. The entire safe window is **(0.6, 6.5) m** — a radius
  of 7 would delete the neighbour, and the 9 m used for 380 Brannan two doors away
  would delete two. **3 m** sits in the middle of the window; it also comfortably
  catches the Overture/OSM gap-fill footprint for this parcel, whose centroid is 1.4 m
  from the anchor. Re-run the measurement against the actual bake before committing.
- `loadRadius`: the skill's default formula gives `max(2500, 7.63 * 30) = 2500` m. Take
  the default. Beyond it the carved-out site is a gap, but at 2.5 km a 7 m building is
  far below a pixel.
- Camera preset: this is a small building on a narrow lot; `{ distance: 150, yaw: 45,
  pitch: 28 }` frames it with its neighbours rather than isolating it, which is the
  only way it reads.
- 370 and 380 Brannan are now both manifest landmarks on the same block face, 60 m
  apart, with 372-374 and 376 left procedural between them. Check in the local QA that
  the two GLBs and the surviving baked buildings form a continuous street wall — a
  visible step where a landmark meets a baked neighbour is the failure mode this
  block will show first.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Bounding-box top exactly 7.63 m (loader scale lands at 1.0)
- [ ] Dimensions plausible in meters and consistent with 2.1 (XY bbox ~21.9 x 21.7 m is expected)
- [ ] Triangles at or under 7,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the upper window band and the door spill; glow shells proud of opaque glazing
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (per-object signed volume for the union of solids; ray test residual <= 0.15%)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + contact sheet + night render regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

- **The rear elevation is unsourced.** No Street View coverage of Varney Place was
  found and satellite imagery shows only the roof edge, so every opening on edge 3 in
  2.7 is *inferred* from typology. The rear is 4.7 m from the alley and fully visible to
  the app's aerial camera, so this is not a face that can be left blank and forgotten.
  Confirming it is the highest-value research the executing agent can do.
- **OSM's footprint is 1.2 m too narrow.** Way/124890321 traces 5.83 x 24.24 m against
  the DataSF LiDAR footprint's 7.00 x 23.83 m and the assessor's 1,760 sq ft lot. The
  OSM way is `source=Bing`, i.e. a rooftop trace from oblique imagery on a building
  whose neighbours are 1 m taller on both sides — exactly the case where a Bing trace
  loses the eaves. **Build on DataSF.** This matters more here than it would elsewhere:
  a 1.2 m error on a 7 m frontage is 17%.
- **`height=7` on the OSM way is the LiDAR median, not the crest.** It matches
  `hgt_median_m` 7.07 to within 1%. The crest is 7.63 m. Same trap as 380 Brannan's
  `height=11`, and the plans README's standing warning.
- **The upper window's pane grid is *inferred*** from a single Street View capture
  partly occluded by a street tree. The 4x3 reading is the weakest number in this
  dossier — but since 2.6 simplifies it to one panel with three mullions, being wrong
  about it costs almost nothing.
- **Vertical band positions are *inferred*** from photogrammetric estimates off one
  pano at an oblique angle, scaled against the measured 7.63 m crest. The mid-band's
  3.40-4.50 m and the window band's 4.60-6.45 m are consistent with each other and with
  the overall height, but none of the three is a published figure.
- **The assessor calls the use "Industrial" and the 2013 permit calls it "public
  assembly"; the current tenants are software and design firms.** None of this affects
  the massing, and `cat: 3` (office) is the honest manifest category for what the
  building is today.
- No architect is recorded for the 1937 building in any source consulted.
