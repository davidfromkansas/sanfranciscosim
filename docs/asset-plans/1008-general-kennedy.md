# 1008 General Kennedy Avenue — SF-SIM asset plan

A 1930s concrete Mission Revival hospital ward in the Presidio's Letterman complex,
rehabilitated in 1994–96 as part of the Thoreau Center for Sustainability. Not a monument
and not an ordinary street building either — a *pavilion*: a long, thin, white-stuccoed
two-storey bar under an unbroken red barrel-tile hipped roof, with terracotta chimneys
punching through the ridge, a taller hipped head block at its east end facing General
Kennedy Avenue, and a covered arcade tying its west end into the ward row.

It is the first plan in this set for a **Presidio** building and the first for a *ward-row*
type, where the subject is one wing of a larger connected historic complex. The design
brief is "the most legible single pavilion in a row of near-identical pavilions", not
"monument" and not "background block".

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/1008-general-kennedy/`. This document is the plan only: Part 1 is the runnable
task prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `1008-general-kennedy` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.4514885, 37.8007968` |
| Target height | **11.9 m** to the chimney crest; roof ridge 10.9 m; eave ~7.8 m |
| Footprint | 55.14 m long x 12.02 m across (ward body 9.38 m wide; east head 12.02 x 10.28 m); 570 m2, measured |
| Long axis heading | 116.85° (east head) / 296.85° (arcade end); long elevations face 26.85° and 206.85° |
| Triangle cap | 9,000 |
| Category | `3` (office) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 1008 General Kennedy Avenue GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of the hospital ward at 1008 General Kennedy Avenue,
Presidio of San Francisco, and deliver it as a downloadable, validated GLB.

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
7. `artifacts/380-brannan/` — the closest reference implementation in scale, budget and
   character (small non-monument building, one strong facade rhythm, designed roof,
   restrained night state)
8. `docs/asset-plans/1008-general-kennedy.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Must capture

- A **long, thin two-storey bar** — 55 m long and only 9.4 m wide. The extreme slenderness
  *is* the building; a modeller who rounds it toward a normal block has failed.
- An unbroken **red barrel-tile hipped roof** running the whole length, with deep
  overhanging eaves
- **Terracotta chimney stacks** rising through the ridge — the only vertical incident on
  the roof and the feature that sets the model's crest height
- **White / cream smooth stucco** walls (concrete Mission Revival), not wood siding —
  see the source conflict below
- The taller **hipped head block** at the east end facing General Kennedy Avenue, wider
  than the bar (12.0 m vs 9.4 m), with the exterior steel stair and upper-level landing
- A regular rhythm of punched double-hung windows with projecting sills, in two storeys
- The **covered arcade stub** at the west end where the ward joins the connecting corridor

## Research 1008 General Kennedy Avenue independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- All four elevations — the two long flanks (northeast and southwest), the east head, and
  the west arcade end
- Aerial and roof views: the hip geometry, the ridge line, and the chimney positions and
  count, which are *inferred* in this dossier and are the weakest numbers in it
- Ground-level views on General Kennedy Avenue and from the Edie Road parking lot
- Day and night appearance
- The bay count and window rhythm of the long elevations — the dossier's reading is
  *inferred* from oblique photography and must be confirmed
- Whether the ward's own eave and ridge heights differ from the complex-wide figures used
  here

Prefer NPS and Presidio Trust historic documentation (the Letterman Hospital Complex is a
contributing element of the Presidio National Historic Landmark District, and HABS surveys
CA-2633 / CA-2634 cover neighbouring Letterman buildings), architect publications,
planning documents, geolocated photography, and aerial/satellite imagery. Never rely on a
single photograph, a single AI-generated image, or a single unsourced 3D model. Separate
verified facts from visual inference; if sources disagree, document the disagreement and
decide.

**Three source problems are already known and resolved in 2.1 and 2.15 — re-check them, do
not silently re-inherit the wrong value:**

1. **OSM and Overture both map the whole Thoreau Center as ONE building** (OSM way
   `288374440`, 49 nodes; the Overture building inherits it). So does the DataSF LiDAR
   footprint layer (`201006.0000207`, 5,845 m2). None of them isolates 1008. The footprint
   in 2.3 was cut out of those polygons by hand; it is the ward wing that contains the
   authoritative 1008 address point, and it is the thing to build.
2. **The Overture height of 10.9 m is a complex-wide figure**, not this ward's. It is used
   here as the ridge because it agrees with a two-storey Mission Revival ward, but it is
   not a per-building measurement.
3. **Neighbouring wards in the same row are wood-sided and pale blue-gray; 1008 is white
   stucco.** Street-level imagery of the row will show both. Model the stucco ward.

## Create a reference dossier

Write `artifacts/1008-general-kennedy/REFERENCE.md` containing: source links and what each
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
one identity cue carried hard — the long unbroken tile roof with its chimneys. Resist
adding hero-tier ornament.

The finished asset must be immediately recognizable as this ward, consistent with the real
building from all four sides and above, architecturally credible, and a premium
handcrafted miniature — not photorealistic, not voxel art, not generic low-poly, and never
accurate in one view while invented in the others.

## Scope of the exported asset

Export the single ward pavilion: the long two-storey bar, its hipped tile roof and
chimneys, the east head block with its exterior stair and landing, all four elevations'
openings, and the covered arcade stub at the west end where the ward meets the connecting
corridor.

Do not include unrelated surrounding city geometry: the neighbouring wards at 1007 and
1009, the rest of the Thoreau Center, the connecting corridor beyond the arcade stub,
General Kennedy Avenue, the Edie Road parking lot, the courtyard lawns, trees, sidewalks,
parked cars, people, plinths, cameras or lights. Temporary context may appear in review
renders but must not leak into the GLB.

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
(`placeGeneric` in `app/src/assets.js` only scales and positions). The ward's long axis
runs **116.85° / 296.85°**, with the head block at the 116.85° (east-southeast) end facing
General Kennedy Avenue. The building is rotated roughly 27° off the world axes, so build
directly on the measured footprint polygon in 2.3 rather than modelling an axis-aligned
bar and rotating it. Record the measured heading in `REPORT.md`.

**Height normalization:** the tallest geometry in the export (the chimney crest) must land
at exactly **11.9 m** so the loader's `targetHeightM / measuredHeight` scale is 1.0.

## Reproducible Blender workflow

Blender 5.2 LTS. Headless: `blender -b --python script.py -- args`.

Keep `artifacts/1008-general-kennedy/build_1008_general_kennedy.py` (deterministic build
script), `artifacts/1008-general-kennedy/1008-general-kennedy.blend`, and
`artifacts/1008-general-kennedy/1008-general-kennedy.glb`. The script must rebuild the
model reliably enough for future revision. Do not modify or rename an unrelated existing
GLB to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`1008-general-kennedy-top.png`, `-north.png`, `-east.png`, `-south.png`, `-west.png`, plus
`1008-general-kennedy-contact-sheet.png`, at least one high three-quarter aerial beauty
render `1008-general-kennedy-aerial.png`, and a night render
`1008-general-kennedy-aerial-night.png`.

The four elevations must share scale, framing, lighting, exposure and projection; use
orthographic or long-lens cameras; label directions from the researched orientation; the
top view must clearly show the hip geometry, the ridge, the chimneys and the head block's
separate hip; the aerial view uses the style bible's camera assumptions (30–50 degrees
down, long lens). Simple tabletop lighting, neutral warm background, minimal depth of
field, and every image must depict the same exported model.

Because the building is 4.6x longer than it is wide, frame the elevations to the long
dimension and accept a lot of empty frame on the end views rather than zooming each view
to fit — the reviewer needs to be able to compare them.

## Validate the exported GLB

Re-import `1008-general-kennedy.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture
count, camera count, light count, animation count, applied-transform status,
negative-scale status, normal-orientation status, unexpected geometry, and
per-material contract compliance. Render at least one review image from the
re-imported asset. Write `artifacts/1008-general-kennedy/validation.json` and
`artifacts/1008-general-kennedy/REPORT.md`.

Note that the axis-aligned XY bounding box will be roughly **54.6 x 35.6 m** even though
the building is 55.1 x 12.0 m — that is the expected consequence of the ~27° real-world
heading, not a scale error.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "1008-general-kennedy",
  "file": "1008-general-kennedy.glb",
  "anchor": [
    -122.4514885,
    37.8007968
  ],
  "targetHeightM": 11.9,
  "cat": 3,
  "name": "1008 General Kennedy Avenue",
  "estimated": true,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

`"estimated": true` is deliberate — the crest height is inferred, not published. See 2.15.

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a separate, explicitly requested job — run `docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in `docs/asset-plans/1008-general-kennedy.md`.
````

---

## Part 2 — Research and design dossier

Compiled 12 August 2026 from the sources in 2.2. Values marked *inferred* are visual or
derived estimates, not published figures — the executing agent must re-verify
anything it relies on.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Complex | Letterman U.S. Army General Hospital, established 1 Dec 1898, built 1899–1902, architect W.H. Wilcox | NPS Letterman Hospital Complex history |
| This building | Concrete ward replacing the original wood-frame Ward "G" | militarymuseum.org Letterman AMC history — the only source that names 1008 directly |
| Build date | 1930s | NPS: "In the 1930s, many of the wood-frame Greek Revival hospital wards were replaced with concrete Mission Revival style buildings" — decade only, no year found |
| Style | Mission Revival, concrete | as above; corroborated by street-level imagery (smooth white stucco, red barrel tile, terracotta chimneys) |
| Storeys | **2** over a raised base | street-level imagery: two window tiers, ground floor entered up a short flight, upper floor reached by an exterior stair to a landing |
| Rehabilitation | 1994 proposed, opened 1996, as the Thoreau Center for Sustainability | Wikipedia (Thoreau Center for Sustainability) |
| Rehab architect | Tanner Leddy Maytum Stacy / LMS Architects, 75,000 sq ft Phase 1 + 37,000 sq ft Phase 2A, to the Secretary of the Interior's Standards | LMS Architects project page |
| Historic status | Contributing building, Letterman Hospital Complex, within the Presidio National Historic Landmark District | NPS; LMS ("within National Register historic structures") |
| Current use | Non-profit office; the Thoreau Center's main entrance serves buildings 1007, 1008 and 1009 together | Thoreau Center / tenant listings |
| Address point | `-122.4515229, 37.800814` | Overture `addresses` release 2026-07-22 — the only authoritative source that resolves 1008 as distinct from 1007/1009 |
| Ward envelope | 55.14 m long x 12.02 m across, 570 m2 | cut from DataSF LiDAR footprint `201006.0000207` and cross-checked against OSM way `288374440` — **measured** |
| Ward body width | 9.38 m | both sources agree to within 0.03 m — **measured** |
| East head block | 12.02 x 10.28 m | both sources agree to within 0.02 m — **measured** |
| Long axis heading | 116.85° / 296.85° | measured from the footprint polygon |
| Roof ridge | 10.9 m above grade | Overture `buildings` height for the parent polygon — complex-wide, see 2.15 |
| LiDAR heights (complex) | median 8.88 m, max 15.79 m; ground 8.69 m NAVD88 | DataSF `ynuv-fyni`, `201006.0000207` — the median mixes one-storey arcades in, the max includes tree returns |
| Eave height | ~7.8 m | *inferred*: raised base ~1.0 m + two 3.4 m storeys |
| Chimney crest | ~11.9 m | *inferred*: ridge + ~1.0 m stack |
| Neighbours in the row | 1007 (north) and 1009 (south), same geometry, connected at the west arcade | address points + footprint |

### 2.2 Sources

- Overture Maps `addresses` theme, release 2026-07-22 — the 1008 address point, and the
  1007 / 1009 points that bound it. This is what made the building identifiable at all.
- Overture Maps `buildings` theme, release 2026-07-22 — 10.9 m height on the parent polygon
- `https://data.sfgov.org/resource/ynuv-fyni` (DataSF Building Footprints, LiDAR-derived),
  building `201006.0000207` — 101-vertex footprint of the whole complex, ground and height
  statistics
- https://www.openstreetmap.org/way/288374440 — independent 49-vertex outline of the same
  complex; used to cross-check the cut-out ward footprint
- https://www.nps.gov/prsf/learn/historyculture/letterman-complex.htm and the NPS
  *Letterman Hospital* brochure (npshistory.com/publications/goga/letterman-hospital.pdf) —
  complex history, the 1930s concrete Mission Revival ward replacement programme
- https://militarymuseum.org/LettermanAMC.html — the only source consulted that names
  Building 1008 and its predecessor Ward "G"
- https://lmsarch.com/projects/thoreau-center-sustainability/ — rehabilitation architect,
  areas, preservation approach
- https://en.wikipedia.org/wiki/Thoreau_Center_for_Sustainability — 1994 proposal, 1996 opening
- Google Street View, General Kennedy Avenue panos labelled "1008 General Kennedy Ave" and
  "1002 General Kennedy Ave" (capture May 2025) — east head elevation: white stucco,
  exterior steel stair to an upper landing, punched double-hung windows with projecting
  sills, red barrel-tile hip, terracotta chimney
- Google Street View, Edie Road parking lot pano (capture Apr 2022) — the row's west
  elevations and the connecting arcade
- Esri World Imagery (z19/z20) — hip geometry, ridge lines, the courtyard rhythm between
  wards, chimney positions

### 2.3 Orientation and placement

The ward is one of three parallel pavilions projecting east-southeast from a north-south
connecting corridor that runs along the east edge of the Edie Road parking lot. Its east
head faces General Kennedy Avenue. The whole complex is rotated about 27° from the world
axes.

Measured footprint polygon, in Blender coordinates (metres, `+X` east, `+Y` north),
already centred on the anchor `-122.4514885, 37.8007968`:

```
(-26.743,   8.214)
(-21.883,  17.814)
( -3.317,   8.415)
( -3.931,   7.180)
( 17.535,  -3.687)
( 18.167,  -2.461)
( 27.312,  -7.090)
( 21.883, -17.814)
( 12.703, -13.167)
( 13.281, -12.025)
```

Read as four pieces:

| Piece | Extent | Faces |
|---|---|---|
| Arcade stub, west end | 12.02 m across x ~4.9 m | west end faces 296.85° |
| Ward bar | 9.38 m across x 44.9 m long | long elevations face 26.85° (NE, toward the 1007 courtyard) and 206.85° (SW, toward the 1009 courtyard) |
| East head block | 12.02 x 10.28 m, stepping out 1.32 m on each flank | head end faces 116.85° |

Because of the 27° heading the axis-aligned bounding box is ~54.6 x 35.6 m. That is correct.

### 2.4 What each side shows

**East (head block, General Kennedy Avenue)** — The public face and the one with the most
incident. Smooth white stucco, two storeys, under its own hip that sits slightly above the
bar's hip. An exterior steel stair with plain pipe rails climbs across the elevation from
left to right to a small flat-roofed landing at the upper floor; beneath the landing a
recessed ground-floor doorway with a glazed panel and a small light fixture. Punched
double-hung windows with white projecting sills, irregularly placed rather than in a strict
grid. A terracotta chimney is visible against the sky at the roof's right shoulder.

**Northeast and southwest long elevations** — Two storeys of punched double-hung windows in
a steady rhythm the full 45 m length, white stucco throughout, no string course, no
ornament. The deep tile eave shades the upper row. These are the faces the courtyards see,
and they are near-identical to one another; do not differentiate them.

**West (arcade end)** — Where the ward meets the connecting corridor. A single-storey
covered arcade stub, flat-roofed, lower and wider than the bar, with plain posts. Almost
never seen at ground level in the real world, but the app's aerial camera reads it as the
join between this asset and the (procedural) neighbours, so it must be built.

**Top** — This is the surface that matters most and the one the recognition rests on: an
unbroken red barrel-tile **hipped** roof, one continuous ridge running the 45 m of the bar,
hipping down at both ends, with the head block carrying its own slightly higher hip on the
same tile. Deep eave overhangs on all four sides. Terracotta chimney stacks rise through
the ridge — the dossier reads **three** on the bar plus one on the head block, but the
count and spacing are *inferred* and must be confirmed from aerial imagery. No mechanical
plant, no skylights, no roof clutter: the roof's whole character is that it is empty.

### 2.5 Recognition cues (ranked)

1. **Extreme slenderness** — a 55 m bar only 9.4 m wide. From the aerial camera this is the
   building's silhouette and it is what distinguishes the ward row from every other
   building in the Presidio.
2. **The unbroken red tile hipped roof** with deep eaves and no clutter
3. **Terracotta chimneys** through the ridge — the only vertical event
4. White stucco walls with a steady two-storey punched-window rhythm
5. The wider hipped head block at the east end, with its exterior stair

### 2.6 Miniature translation

**Preserve**

- The 55.1 x 9.4 m proportion and the real 27° heading, exactly
- The continuous hip and ridge, and the step up to the head block's hip
- Deep eave overhangs — they are what make a tile roof read as a tile roof at 20 px
- The chimneys, thickened so they survive at thumbnail size
- The two-storey window rhythm as a rhythm, not as individual windows

**Simplify / exaggerate**

- Individual barrel tiles become flat colour; the eave becomes one chunky fascia band
- Roughly 22 window pairs per long elevation become 11 clean bays, all identical, recessed
  0.15 m
- Double-hung subdivision, sashes and blinds disappear — sub-pixel at city scale
- The exterior stair becomes a single chunky ramped slab with two rail bars and a landing
  block; no treads
- The arcade stub becomes one flat slab on four posts
- Chimneys are exaggerated in section (to ~0.9 x 0.9 m) but not in height; they set the
  11.9 m crest and must land on it exactly
- The raised base becomes a 1.0 m plinth band in a slightly darker value, which also hides
  the terrain seam

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not
a straitjacket — adjust after the first aerial review render.

1. Plinth: extrude the 2.3 footprint from z=0 to z=1.0, `Toy_stone` darkened, all pieces.
2. Ward bar: extrude the 9.38 m wide central section from z=1.0 to z=7.8, `Toy_white`.
3. Head block: extrude the 12.02 x 10.28 m east piece from z=1.0 to z=8.6, `Toy_white`.
4. Long elevations, both sides: 11 bays, openings 1.2 x 1.8 m, two tiers with sills at
   z=2.0 and z=5.2, recessed 0.15 m, `Toy_glass`; 0.12 m proud `Toy_trim` sill under each.
5. East head elevation: four windows in the same family, asymmetrically placed, plus a
   1.1 x 2.3 m recessed doorway at plinth level in `Toy_ink`.
6. Bar roof: hipped, ridge at **z=10.9**, eave line at z=7.8 with a 0.6 m overhang on all
   four sides, pitch ~30°, `Toy_red`. Fascia band 0.25 m in `Toy_trim` under the eave.
7. Head roof: its own hip, ridge at z=10.9 as well but springing from the higher z=8.6 eave
   so it reads as a shorter, steeper cap on a wider block, same materials.
8. Chimneys: three on the bar ridge (roughly at 25%, 55% and 85% of its length) and one on
   the head block, 0.9 x 0.9 m in section, rising to **z=11.9** — these set the
   bounding-box top and must land exactly on 11.9.
9. Arcade stub: slab 12.02 x 4.9 x 0.35 m at z=3.4 on four 0.35 m posts, `Toy_trim` slab,
   `Toy_white` posts.
10. East stair: ramped slab 6.0 x 1.2 x 0.25 m rising from z=1.0 to z=4.6 across the head
    elevation, plus a 2.2 x 1.6 m landing at z=4.6 and two 1.0 m rail bars, `Toy_ink`.
11. Bevel 0.12 m, 2 segments.

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_white` | `#f7f4ec` | stucco walls, arcade posts |
| `Toy_stone` | `#d9d2c2` | plinth band |
| `Toy_red` | `#c4453c` | **the tile roof** — bar hip, head hip |
| `Toy_trim` | `#f3efe6` | eave fascia, window sills, arcade slab |
| `Toy_glass` | `#2a4d73` | all windows |
| `Toy_brick` | `#c96f4a` | terracotta chimney stacks |
| `Toy_ink` | `#3a3530` | doorway recess, exterior stair and rails |
| `Toy_glass_Glow` | `#2a4d73` | lit windows at night |
| `Toy_trim_Glow` | `#f3efe6` | the head-block doorway soffit at night |

Note on the roof: `Toy_red` (`#c4453c`) is cooler and more saturated than real weathered
barrel tile, and `Toy_brick` (`#c96f4a`) is closer to the true colour but is also the
chimney material, which would flatten the two together. Build with `Toy_red` on the roof
and `Toy_brick` on the chimneys so the stacks read as separate objects from above, and
record the decision in `REPORT.md`. If the aerial render says otherwise, an off-palette
weathered terracotta at roughly `#b85a44` is a WARN not a FAIL — but justify it.

**Night state (required).** Glow surfaces must be thin shells proud of the opaque glazing —
the app renders `_Glow` in a separate layer that is ~12% alpha by day, so a primary surface
must never be authored as glow. Hero glow: a scatter of lit windows along **one** long
elevation and the head block — six or eight in total, not the whole rhythm. This is an
office building that empties in the evening, and a fully lit 45 m bar would read as a
hospital, which it has not been since 1994. Supporting accent: the doorway soffit under
the east landing. The roof does not glow.

### 2.9 Top surface

An empty 55 m tile hip, seen constantly from above. Its quality comes entirely from three
things: the crispness of the hip lines, the depth of the eave shadow, and the chimneys.
Model the hip as real geometry with proper ridge and hip edges — do not fake it with a
flat plane and a bevel. Keep the fascia value clearly lighter than the tile so the eave
reads as an edge from directly overhead.

### 2.10 Scope

**In the GLB:** the single ward pavilion — plinth, two-storey stucco bar, east head block,
hipped tile roofs, chimneys, all four elevations' openings, the east exterior stair and
landing, and the west arcade stub

**Not in the GLB:** the wards at 1007 and 1009, the rest of the Thoreau Center, the
connecting corridor beyond the arcade stub, General Kennedy Avenue, the Edie Road parking
lot, courtyard lawns, trees, sidewalk, vehicles, people, plinths, cameras or lights

### 2.11 Triangle budget

Cap 9,000 — a secondary building, and the cap should bind. Suggested split: plinth, bar and
head ~1.5k, hipped roofs and eaves ~2k, 22 window bays across both long elevations ~3k,
head elevation and doorway ~0.8k, chimneys ~0.6k, stair and arcade ~1k.

### 2.12 Draft manifest entry

```json
{
  "id": "1008-general-kennedy",
  "file": "1008-general-kennedy.glb",
  "anchor": [
    -122.4514885,
    37.8007968
  ],
  "targetHeightM": 11.9,
  "cat": 3,
  "name": "1008 General Kennedy Avenue",
  "estimated": true,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

`dims` and `tris` are placeholders until the asset is built and validated.

### 2.13 Integration notes (for later, not this task)

- **New landmark.** Add a `pipeline/lib/landmarks.mjs` entry (`id: '1008-general-kennedy'`)
  and re-bake the affected tiles, or the baked procedural building will intersect the GLB.
- **The exclusion radius is the hard part of this integration and it needs care.** The
  procedural source polygon is the *whole* Thoreau Center, not this ward. A radius large
  enough to clear the ward (~28 m from the anchor, half the 55 m length) will also punch
  out most of 1007 and 1009, leaving two holes where two real buildings stand — an AGENTS
  rule 5 violation and visually worse than doing nothing. Options, in order of preference:
  1. Give the exclusion a **rectangular / oriented footprint** rather than a radius, matching
     the 2.3 polygon. Check whether `landmarks.mjs` supports this; if it does not, adding
     it is the right fix and benefits every future ward-row asset.
  2. Model 1007 and 1009 as sibling assets in the same pass and exclude the group together.
  3. Ship with a tight radius that under-clears, accepting a visible procedural remnant, and
     record it as a known FAIL in the report.
  Do not silently pick option 3.
- `loadRadius`: the skill's default formula gives `max(2500, 11.9 * 30) = 2500` m. Take the
  default. At 2.5 km a 12 m building is far below a pixel.
- This is the second non-monument building in the landmark manifest, after 380 Brannan. The
  question raised there applies harder here: a row of near-identical historic pavilions is
  exactly the case the kit/instancing route (`KIT-INTEGRATION-PROMPT.md`) exists for. If
  the Presidio's ward rows are going to be built out, build the *ward* as a kit piece and
  place three of it, rather than three one-off manifest landmarks.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Bounding-box top exactly 11.9 m (loader scale lands at 1.0)
- [ ] Dimensions plausible in meters and consistent with 2.1 (XY bbox ~54.6 x 35.6 m is expected)
- [ ] Ward body width 9.4 m, not rounded up toward a normal block
- [ ] Triangles at or under 9,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the scattered lit windows and the doorway soffit; glow shells proud of opaque glazing
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (per-object signed volume for the union of solids; ray test residual <= 0.15%)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + contact sheet + night render regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

- **No source isolates this building's footprint, and that is the dossier's central
  weakness.** OSM, Overture and DataSF LiDAR all map the Thoreau Center as one polygon. The
  footprint in 2.3 was cut out by hand along the ward's own walls, using the 1008 address
  point to choose the wing and the two independent outlines to confirm the dimensions. They
  agree to within 0.03 m on the 9.38 m body width and 0.02 m on the 12.02 x 10.28 m head,
  which is why those numbers are marked measured. The *ends* of the cut — where the ward
  merges into the west block — are a judgement call, not a survey.
- **The 10.9 m ridge is a complex-wide Overture figure**, not a measurement of this ward.
  The DataSF LiDAR median for the same polygon is 8.88 m, which mixes in one-storey arcade
  sections, and its 15.79 m maximum is almost certainly a tree return. 10.9 m is consistent
  with two 3.4 m storeys on a 1.0 m base under a 30° hip, so it is used — but a
  per-building height from a DSM or a Presidio Trust drawing would be better and should be
  sought before modelling.
- **The chimney count and spacing are inferred** and set the crest height, which the whole
  scale normalization hangs off. This is the single most valuable thing to confirm from
  aerial imagery before building.
- **"Concrete Mission Revival" vs the wood-sided neighbours.** The NPS account of the 1930s
  replacement programme and the militarymuseum.org note that 1008 specifically replaced
  wood-frame Ward "G" both point to concrete, and the May 2025 Street View of the head
  block shows smooth white stucco. But at least one neighbouring ward in the same row is
  pale blue-gray wood siding, and the Apr 2022 parking-lot pano shows a cream *wood-sided*
  ward with a lattice skirt and a long accessible ramp. Do not build that building. If
  fresh imagery contradicts the stucco reading for 1008, follow the imagery and say so.
- **The build year is a decade, not a year.** No source consulted gives an exact date for
  Building 1008.
- **No architect is recorded** for the 1930s ward. The 1899–1902 complex is W.H. Wilcox's;
  the 1994–96 rehabilitation is LMS Architects'. The building itself falls between them.
- The bay count on the long elevations (11 per side) is *inferred* from oblique photography
  and satellite, and is the weakest facade number here.
- Whether the arcade stub is single-storey open, single-storey enclosed, or two-storey at
  this particular ward is unresolved; the plan assumes open single-storey.
</content>
