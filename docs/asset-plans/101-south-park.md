# 101 South Park — SF-SIM asset plan

A narrow-fronted 1947 commercial block at the east end of the South Park oval, re-skinned
into a charcoal-gray creative office and renovated by Perkins&Will in 2023 for Kleiner
Perkins. Not a monument and not a warehouse either — a *quiet, expensive* building: a
13-metre-wide dark box with a row of tall warm-oak shopfront windows at street level and a
recessed dark-glass upper storey floating behind a plain parapet plane. It is the second
plan in this set (after 380 Brannan) for an ordinary South-of-Market street building, and
the design brief is "the most self-possessed small building on the park", not "landmark".

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/101-south-park/`. This document is the plan only: Part 1 is the runnable task
prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `101-south-park` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3937582, 37.7812624` |
| Target height | **10.0 m** to the parapet crest — *estimated*, see 2.1 and 2.15; the single weakest number in this dossier |
| Footprint | 13.07 m (South Park frontage, NW) x 29.7 m deep; 380.1 m2, measured |
| Triangle cap | 9,000 |
| Category | `3` (office) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 101 South Park GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of 101 South Park in San Francisco and deliver it as
a downloadable, validated GLB.

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
7. `artifacts/380-brannan/` — the closest reference implementation in scale, character and
   district (small SoMa street building on a ~45°-rotated footprint, flat designed roof,
   restrained night state)
8. `docs/asset-plans/101-south-park.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract, `AGENTS.md`
governs repository and integration rules. Do not invent a new style and do not copy visual
instructions from unrelated prompts.

## Must capture

- A narrow, deep two-storey box: only 13 m of frontage on South Park, running 29.7 m back
- The **charcoal / dark warm-gray stucco** body — the building has almost no colour, and
  that restraint is its identity on a park ringed by pastel and brick neighbours
- The **row of tall warm-oak shopfront windows** at ground level, each a tall three-light
  bay with a transom above — the only warm element on the building and the strongest cue
- The oak entrance door at the north end of the front, with the small `101` plate above it
- The **recessed upper storey**: a continuous dark-metal ribbon window set back behind the
  plane of the front wall, so the parapet reads as a thin frame in front of a shadow
- A flat, light "cool roof" with a designed layout: skylights, a mechanical cluster, and a
  raised element at the front third
- The step down in mass from the taller front block to the lower middle/rear block

## Research 101 South Park independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world orientation, and
gather references covering:

- All four elevations, with particular attention to the front (NW) elevation on the park
- Aerial and roof/top views — the roof layout in 2.9 is read off satellite imagery only
- Ground-level views on South Park, and whatever exists on the Jack London Alley and
  Varney Place sides
- Day and night appearance
- The bay count and spacing of the oak shopfront windows — the dossier's 4-bay reading is
  *inferred* from a single Street View pano and must be confirmed
- Whether the second storey runs the full 29.7 m depth or stops partway, and where the
  mass steps down (this is the biggest open question — see 2.15)

Prefer architect/engineer publications, owner or institutional material, planning and
permitting documents, architectural press, geolocated photography, and aerial/satellite
imagery. Never rely on a single photograph, a single AI-generated image, or a single
unsourced 3D model. Separate verified facts from visual inference; if sources disagree,
document the disagreement and decide.

**Three source conflicts are already known and are NOT resolved — do not silently inherit
a number from any of them (see 2.1 and 2.15):**

1. **Height.** OSM tags `height=6` and the 2010 city LiDAR reports a *median* roof height
   of 5.56 m over this footprint. Both describe the building **before its second storey
   existed in its current form**, and both are wrong for today. The LiDAR *maximum* over
   the same footprint is 10.92 m. This plan's 10.0 m is a photogrammetric estimate from a
   single January 2025 pano. **Re-derive the height yourself and say how.**
2. **Storey count over time.** Building permits record 1 storey through 1994 and 2 storeys
   from 2002 onward; the assessor roll says 2 storeys and "built 1947"; the architect's
   own project copy says the building is "originally built in the 1920's". Build **two
   storeys** — that is what every current photograph shows — but do not treat any of the
   dates as established.
3. **Floor area.** The published renovation area is 16,420 sq ft, which is roughly double
   what two storeys on this 380 m2 footprint can hold. Either the published figure covers
   more than this parcel, or the tenancy spans the neighbouring structure to the southeast.
   **Model the addressed building on its own measured footprint only** (AGENTS rule 5) and
   record what you find.

## Create a reference dossier

Write `artifacts/101-south-park/REFERENCE.md` containing: source links and what each
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

This is a **secondary building** in the style bible's detail budget (§21), not a hero
landmark: clear massing, one strong facade rhythm, a simple designed roof, and exactly one
identity cue carried hard — the warm-oak shopfront row against the charcoal body. Resist
adding hero-tier ornament.

Note the specific style risk here: this building is *dark and plain*, and a naive miniature
of it reads as a grey slab. The oak windows, the recessed upper storey's shadow, and the
roof layout are the three things that keep it alive at diorama scale. Spend the detail
budget there.

The finished asset must be immediately recognizable as 101 South Park, consistent with the
real building from all four sides and above, architecturally credible, and a premium
handcrafted miniature — not photorealistic, not voxel art, not generic low-poly, and never
accurate in one view while invented in the others.

## Scope of the exported asset

Export the single building on lot 3775/038: body, parapet, all four elevations' openings,
the entrance, and the roof deck with its furniture.

Do not include unrelated surrounding city geometry: South Park (the oval, its lawn, paths
or play structure), South Park Street, Jack London Alley, Varney Place, the neighbouring
buildings on either flank, street trees, the sidewalk, parked cars, motorcycles, people,
plinths, cameras or lights. Temporary context may appear in review renders but must not
leak into the GLB.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary `.glb`;
real-world meters; origin at base center; minimum geometry Z ~ 0; applied transforms; no
negative scales; outward normals; no duplicate or foreign geometry; no image textures; no
transparency; flat-color materials named `Toy_*` from the project palette; `_Glow` suffix
only on surfaces that glow at night; no `Toy_body`; no cameras, lights, animations,
armatures or constraints; no external dependencies; at most 9,000 triangles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model drops
into the city at its real-world heading — the loader applies no rotation (`placeGeneric` in
`app/src/assets.js` only scales and positions). The South Park entrance front faces
**northwest, outward normal 318.3°**; the building is rotated roughly 45° off the world
axes, so build directly on the measured footprint polygon in 2.3 rather than modelling an
axis-aligned box and rotating it. This is the case the plans README calls out: the
contract's "front faces −Y" rule cannot be honoured literally here, real-world orientation
wins, and the deviation must be recorded in `REPORT.md` along with the measured heading.

**Height normalization:** the tallest geometry in the export must land at exactly the
height you verify (this plan's estimate is **10.0 m**) so the loader's
`targetHeightM / measuredHeight` scale is 1.0. If your research moves the height, move both
the model and the draft manifest entry together and say so in `REPORT.md`.

## Reproducible Blender workflow

Blender 5.2 LTS. Headless: `blender -b --python script.py -- args`.

Keep `artifacts/101-south-park/build_101_south_park.py` (deterministic build script),
`artifacts/101-south-park/101-south-park.blend`, and
`artifacts/101-south-park/101-south-park.glb`. The script must rebuild the model reliably
enough for future revision. Do not modify or rename an unrelated existing GLB to satisfy
the task.

## Required review renders

Render the exact final geometry from controlled cameras: `101-south-park-top.png`,
`101-south-park-north.png`, `101-south-park-east.png`, `101-south-park-south.png`,
`101-south-park-west.png`, plus `101-south-park-contact-sheet.png`, at least one high
three-quarter aerial beauty render `101-south-park-aerial.png`, and a night render
`101-south-park-aerial-night.png`.

The four elevations must share scale, framing, lighting, exposure and projection; use
orthographic or long-lens cameras; label directions from the researched orientation; the
top view must clearly show the parapet ring, skylights, mechanical cluster and the step in
roof level; the aerial view uses the style bible's camera assumptions (30-50 degrees down,
long lens). Simple tabletop lighting, neutral warm background, minimal depth of field, and
every image must depict the same exported model.

For the night render, drive the `_Glow` materials from Base Color (copy `Base Color` into
`Emission Color`, strength 1.0) — see the note at the end of `docs/asset-plans/README.md`.
A re-imported GLB's `_Glow` materials otherwise render as white slabs.

## Validate the exported GLB

Re-import `101-south-park.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture count, camera
count, light count, animation count, applied-transform status, negative-scale status,
normal-orientation status, unexpected geometry, and per-material contract compliance.
Render at least one review image from the re-imported asset. Write
`artifacts/101-south-park/validation.json` and `artifacts/101-south-park/REPORT.md`.

Note that the axis-aligned XY bounding box will be roughly **30 x 30 m** even though the
building is 13.1 x 29.7 m — that is the expected consequence of a ~45° real-world heading,
not a scale error.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this draft
entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "101-south-park",
  "file": "101-south-park.glb",
  "anchor": [
    -122.3937582,
    37.7812624
  ],
  "targetHeightM": 10.0,
  "cat": 3,
  "name": "101 South Park",
  "estimated": true,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`,
or any app code in this task. Integration is a separate, explicitly requested job — run
`docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in
`docs/asset-plans/101-south-park.md`.
````

---

## Part 2 — Research and design dossier

Compiled 12 August 2026 from the sources in 2.2. Values marked *inferred* or *estimated*
are visual or derived, not published figures — the executing agent must re-verify anything
it relies on. This dossier is thinner on published architectural detail than the civic
landmark plans, because the building has essentially no architectural literature: it is a
working office block, and the primary evidence is city data plus photography.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Address | 101 South Park (the street is signed "SOUTH PARK", not "South Park St") | SF Assessor `property_location`; Street View street sign |
| Block / lot | 3775 / 038 | SF Assessor secured roll; DataSF building footprint `mblr = SF3775038` |
| Built | 1947 | SF Assessor secured roll — **contradicted** by the architect's "1920's", see 2.15 |
| Storeys today | **2** | SF building permits 2002-2024 (`number_of_existing_stories = 2`); assessor roll; Street View Jan 2025 |
| Storeys before ~1995 | 1 | SF building permits 1988-1994 all record 1 existing storey |
| Use | Commercial / office; a restaurant occupied the ground floor c. 1989-1992 | assessor `use_definition = Commercial Retail`; permits for a Type I grease hood and restaurant hood/flue |
| Current occupant | Kleiner Perkins | 2018 permit "replace existing sign kpbc … 'kleiner perkins'"; OSM POI node 10874867174 |
| Interior renovation | Perkins&Will, completed 2023; ground-up interior rebuild | Office Snapshots project page |
| Recent permits | 2012-2016 office fit-out incl. a new flat skylight; 2014 four-ply "cool" Title-24 roof over the **entire building roof**; 2024 conference-room remodel | SF Building Permits |
| Footprint | 380.1 m2; 13.07 m (NW frontage) x 29.7 m deep; effectively a clean parallelogram | DataSF LiDAR building footprint, reprojected — **measured** |
| OSM footprint (cross-check) | 377.2 m2, OSM way/113545689 | agrees with DataSF within ~1% |
| Roof height, 2010 LiDAR **median** | 5.56 m | DataSF `hgt_median_m` — measured, but **describes the pre-renovation building, see 2.15** |
| Roof height, 2010 LiDAR **maximum** | 10.92 m | DataSF `hgt_maxcm` — measured, over a small part of the footprint |
| Ground elevation | 10.09 m (NAVD88) | DataSF `gnd_min_m` — the app's terrain handles this, not the asset |
| Parapet crest today | **~10.0 m** | *estimated*: photogrammetric from the Jan 2025 South Park pano, scaling the facade against a ~3.2 m ground-floor window opening; ±0.8 m |
| Frontage heading | front faces 318.3° (NW, toward the park); rear faces 138.3° (SE) | measured from the footprint polygon |

### 2.2 Sources

- https://www.openstreetmap.org/way/113545689 — footprint, `addr:housenumber=101`, `addr:street=South Park`, `building=yes`, `height=6`
- https://www.openstreetmap.org/node/10874867174 — the Kleiner Perkins POI at this address
- `https://data.sfgov.org/resource/ynuv-fyni` (DataSF Building Footprints, LiDAR-derived) — authoritative footprint polygon and the 5.56 m / 10.92 m heights
- `https://data.sfgov.org/resource/wv5m-vpq2` (SF Assessor Historical Secured Property Tax Rolls) — address, block/lot, 1947, storey count, use class
- `https://data.sfgov.org/resource/i98e-djp9` (SF Building Permits) — 28 permits on this lot, 1988-2024: the storey count over time, the restaurant era, the 2012-2016 office fit-out, the 2014 cool roof, the Kleiner Perkins sign
- https://officesnapshots.com/2026/02/03/south-park-venture-capital-firm-offices-san-francisco/ — Perkins&Will renovation, 2023, 16,420 sq ft, "brick-clad", "originally built in the 1920's", "large, arched metal-clad windows", double-height "birdcage" vestibule
- Google Street View, South Park pano (capture January 2025), and the Google Maps place record "101 S Park St" — the front elevation described in 2.4
- Google Maps satellite (Airbus / Maxar / Vexcel imagery, 2026) — the roof layout described in 2.9
- https://www.openstreetmap.org/way/24052083 — South Park itself; used only to establish which way the building faces

Note on the Office Snapshots copy: it describes the **interior** project and its exterior
sentences do not match the building as photographed — see 2.15. Treat it as a source for
architect, year and tenancy, not for materials.

### 2.3 Orientation and placement

The building sits on the southeast side of the South Park oval, near its east end, with its
narrow front on the park and its long flanks running back toward Jack London Alley
(northeast) and the neighbour at 117 South Park (southwest). Like the whole SoMa grid it is
rotated about 45° from the world axes. South Park's own long axis runs at bearing 45.0°.

Measured footprint polygon, in Blender coordinates (metres, `+X` east, `+Y` north), already
centred on the anchor `-122.3937582, 37.7812624`:

```
(  0.717,  -9.826)
( -4.650,  -4.402)
( -6.241,  -3.044)
(-14.940,   5.840)
(-14.994,   5.895)
( -5.419,  14.435)
( 15.195,  -5.708)
(  6.037, -15.039)
```

Edges, with outward normals:

| Edge | Length | Faces | Elevation |
|---|---|---|---|
| `(-14.994,5.895) -> (-5.419,14.435)` | 12.83 m | NW 318.3° | **South Park front** |
| `(-5.419,14.435) -> (15.195,-5.708)` | 28.82 m | NE 44.3° | northeast flank (Jack London Alley side) |
| `(15.195,-5.708) -> (6.037,-15.039)` | 13.07 m | SE 134.5° | rear |
| the four segments back to `(-14.994,5.895)` | 29.60 m total | SW 224.5° | southwest flank (party wall with 117 South Park) |

The southwest boundary is drawn as four short segments in the survey, but they are collinear
to within 0.18 m — treat it as one straight wall. The 0.08 m segment between
`(-14.940,5.840)` and `(-14.994,5.895)` is a survey chamfer; keep it or drop it, it costs
nothing either way.

Because of the ~45° heading the axis-aligned bounding box is ~30 x 30 m. That is correct.

### 2.4 What each side shows

**Northwest (South Park front)** — The hero elevation and the only one that has been
photographed well. A flat charcoal / dark warm-gray stucco wall, 13 m wide, in two clearly
different registers:

- *Ground floor*: a row of tall window bays in **warm natural oak frames** — each bay is
  three narrow vertical lights with a horizontal transom above, set in a plain reveal, with
  frosted or shaded glazing behind. Four such bays are visible; toward the north end of the
  front there is a single oak-framed glazed entrance door, set in a shallow recess, with a
  small dark `101` plate above it and a discreet wall-mounted sign beside it. A pair of slim
  black gooseneck lamps is mounted on the wall above the openings.
- *Upper floor*: the wall plane continues blank for a deep band, then a **continuous ribbon
  window in dark metal frames, recessed roughly half a metre behind the front plane**, so
  the parapet and the two side piers read as a thin frame around a rectangle of shadow. The
  glazing is divided into a few wide lights; behind it the interior ceiling is visible.
- *Parapet*: a plain flat coping, no cornice, no ornament, no signage.

The whole elevation has essentially one colour and one accent: charcoal, and oak.

**Northeast flank (Jack London Alley side)** — 28.8 m of flank facing an open paved strip,
so it is genuinely visible in the real world and unavoidably visible to the app's camera.
No usable ground-level photography was found. Treat it as the same charcoal stucco with a
sparse, regular scatter of openings; *inferred*.

**Southwest flank** — Shares a boundary with 117 South Park; effectively a party wall for
most of its length. *Inferred*: blank charcoal stucco.

**Southeast (rear)** — 13.07 m facing the interior of the block toward Varney Place. No
usable photography. *Inferred*: service elevation, blank apart from a door and one or two
openings.

**Top** — See 2.9. This is the surface the app's camera sees most, and it is the one surface
for which the evidence is good.

### 2.5 Recognition cues (ranked)

1. **The row of warm-oak shopfront windows on a charcoal wall** — the only warmth on the
   building and the thing that identifies it at a glance
2. The **recessed dark upper storey** behind a plain parapet frame — the front reads as a
   solid band, a shadow band, and a cap
3. The narrow (13 m) front on a deep (29.7 m) plan, on the ~45° SoMa heading
4. Total absence of ornament, colour or signage — deliberate restraint next to noisier
   neighbours
5. The big pale flat roof with its skylight and mechanical cluster, seen from above

### 2.6 Miniature translation

**Preserve**

- The narrow-front / deep-plan proportion and the real 45° heading
- The two-register front: solid oak-and-charcoal base, recessed dark band above
- The oak as the single accent colour on an otherwise neutral building
- The step down from the front block to the lower rear block, if 2.15's question resolves
  in favour of one existing

**Simplify / exaggerate**

- The three-light-plus-transom window bays become one clean oak-framed opening each, with a
  single flat glass panel and a chunky frame — the mullion pattern is sub-pixel at city
  scale
- The oak frames are **widened** (to ~0.25 m) and their colour pushed slightly warmer than
  reality; this is the one place semantic exaggeration is spent, and it is what stops the
  model reading as a grey slab
- The upper ribbon window becomes one recessed rectangle with a real 0.5 m reveal, so the
  shadow does the work rather than a drawn frame
- Gooseneck lamps, the sign, the door hardware and the `101` plate all disappear; a plate is
  a couple of pixels
- Flank openings become a regular rhythm, not a survey of the real ones
- Roof clutter becomes three skylight boxes, one HVAC cluster of two blocks, and one raised
  penthouse volume

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not a
straitjacket — adjust after the first aerial review render, and adjust *all* of them if the
verified height differs from 10.0 m.

1. Body: extrude the 2.3 footprint from z=0 to z=9.4, `Toy_ink` (see 2.8 on the body
   colour). This is the charcoal shell that all four elevations show.
2. Rear/middle block step-down (**conditional on 2.15**): if the second storey does not run
   the full depth, drop the rear ~14 m of the body to z=5.4 and give it its own parapet;
   otherwise keep the body full height and put the step in the roof furniture instead.
3. Front ground floor, z=0 to z=4.4, on the NW face: four oak-framed window bays 2.0 x 3.2 m
   at 2.6 m centres, recessed 0.15 m, plus a 1.4 m entrance door bay at the northeast end of
   the front recessed 0.3 m. Frames `Toy_rust` at 0.25 m, glass `Toy_glass`.
4. Upper storey band on the NW face: one opening 11.4 x 2.6 m, **recessed 0.5 m**, head at
   z=8.6. Reveal walls `Toy_ink`, glass `Toy_glass`. The depth of this recess is the whole
   effect — do not flatten it into a surface panel.
5. Flank openings: on the NE flank, six bays 1.4 x 2.4 m per storey, recessed 0.15 m,
   `Toy_glass`. SW flank blank (party wall). Rear: one door and two small openings.
6. Parapet: z=9.4 to z=10.0, following the footprint, 0.3 m thick, `Toy_ink` with a
   `Toy_steel` coping strip on the front elevation only. The parapet top sets the bounding
   box and must land exactly on the verified height.
7. Roof deck at z=9.4, `Toy_white` — this is a real 2014 "cool roof" and it must read pale
   from above, in deliberate contrast with the dark walls. Three skylight boxes
   2.4 x 1.6 x 0.3 m `Toy_glassl`; two HVAC blocks (2.2 x 1.6 x 1.0 m and 1.6 x 1.2 x 0.8 m)
   `Toy_steel`; one penthouse 3.2 x 2.6 m rising from z=9.4 toward the crest, `Toy_roofd`.
8. Bevel 0.12 m, 2 segments.

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_ink` | `#3a3530` | the whole body, parapet, window reveals |
| `Toy_rust` | `#a86444` | **the signature oak window frames and entrance door** |
| `Toy_glass` | `#2a4d73` | all windows |
| `Toy_glassl` | `#6f95b8` | skylights |
| `Toy_white` | `#f7f4ec` | roof deck ("cool roof") |
| `Toy_steel` | `#9aa0a6` | parapet coping, HVAC blocks |
| `Toy_roofd` | `#45454a` | roof penthouse |
| `Toy_rust_Glow` | `#a86444` | the lit ground-floor window row at night |
| `Toy_glass_Glow` | `#2a4d73` | a few lit upper-storey lights |

Note on the body colour: the real wall is a dark warm gray a shade or two lighter than
`Toy_ink`. `Toy_ink` is the closest palette entry and is the safe choice; `Toy_roofd`
(`#45454a`) is cooler and slightly lighter and may read better against the pale roof.
Off-palette is a WARN not a FAIL, so a dedicated `Toy_charcoal` at roughly `#4a4540` is
permissible if the render justifies it. Decide from the aerial render and record the
decision in `REPORT.md`.

Note on `Toy_rust` for the oak: `#a86444` is the palette's warm brown and is the right
family, but the real joinery is a lighter, yellower natural oak. If the render shows the
frames disappearing against the charcoal, going one step lighter (toward `#c08a5a`) is the
correct call — the whole point of this element is that it is the one thing that reads.

**Night state (required).** Glow surfaces must be thin shells proud of the opaque glazing —
the app renders `_Glow` in a separate layer that is ~12% alpha by day, so a primary surface
must never be authored as glow. Hero glow: the ground-floor oak window row, lit warm and
lit *fully* — this is a small building and its street-level glow is what places it on the
park at night. Supporting accent: two or three lights in the upper ribbon window, not all of
it. Nothing else glows; there is no signage and no crown.

### 2.9 Top surface

A flat pale roof about 9.4 m up, on a block the camera flies over constantly, and the one
surface for which the evidence is good. From 2026 satellite imagery: a light, near-white
membrane roof inside a continuous parapet; a dense cluster of dark mechanical units and
bright skylights grouped toward the **northwest (front) third**; scattered individual
skylights and small units down the rest of the length; and a visible change in roof level
partway along (see 2.15). The neighbouring roof to the southwest is a distinctly different
terracotta-red — a useful sanity check that the pale roof is genuinely this building.

Keep the parapet coping value clearly darker than the deck so the ring reads from above, and
keep the mechanical cluster asymmetric and grouped at the front third rather than spread
evenly — that asymmetry is what makes the roof read as a real roof.

### 2.10 Scope

**In the GLB:** the single building on lot 3775/038 — charcoal body, parapet, all four
elevations' openings, the entrance, roof deck and roof furniture

**Not in the GLB:** South Park itself, South Park Street, Jack London Alley, Varney Place,
the neighbouring buildings, street trees, sidewalk, vehicles, people, plinths, cameras or
lights

### 2.11 Triangle budget

Cap 9,000 — a secondary building, and the cap should bind. Suggested split: body, parapet
and step ~2k, ground-floor oak bays ~2.5k, upper recessed band ~1k, flank openings ~2k, roof
furniture ~1.5k.

### 2.12 Draft manifest entry

```json
{
  "id": "101-south-park",
  "file": "101-south-park.glb",
  "anchor": [
    -122.3937582,
    37.7812624
  ],
  "targetHeightM": 10.0,
  "cat": 3,
  "name": "101 South Park",
  "estimated": true,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

`dims` and `tris` are placeholders until the asset is built and validated. `estimated` is
`true` because the target height is not a published figure — flip it to `false` only if the
executing agent establishes the height from a citable source.

### 2.13 Integration notes (for later, not this task)

- **New landmark, Case B.** Neither `pipeline/lib/landmarks.mjs` nor `app/src/landmarks.js`
  knows this id. Integration needs a `pipeline/lib/landmarks.mjs` entry
  (`id: '101-south-park'`, `exclude: ~16`) **and a re-bake of the affected tiles**, or the
  baked procedural building on this exact footprint will intersect the GLB.
- The exclusion radius must be tight. 16 m is a little over the footprint's half-diagonal
  (16.2 m) and the neighbours are attached on the southwest side — a generous radius would
  punch a hole in the middle of the block face.
- **The procedural stand-in here is 6 m tall and the asset is ~10 m**, because the baked
  city takes OSM's `height=6`. Expect the neighbourhood silhouette to change visibly when
  this lands; that is the correct outcome, not a bug. It is also why an unbaked local check
  proves nothing — the procedural block is *shorter* than the asset here, which is the
  inverse of the usual case and will hide an exclusion-zone mistake rather than reveal it.
  Do the bake before judging.
- `loadRadius`: the default formula gives `max(2500, 10.0 * 30) = 2500` m. Take the default.
- This is the second one-off SoMa street building in the landmark manifest after
  380 Brannan. The question that plan raised stands: if the intent is to keep doing
  individual South Park / SoMa blocks, the kit/instancing route
  (`KIT-INTEGRATION-PROMPT.md`) is probably the better long-term home for this class of
  building. A manifest of 300 one-off street buildings would not stream well.
- If other landmarks are in flight, run stage 5 in **batch mode** (see
  `docs/asset-pipeline/ADDRESS-TO-ASSET.md`): still bake, still QA the bake, then throw the
  bake away and commit source only.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Bounding-box top exactly the verified height (loader scale lands at 1.0)
- [ ] Dimensions plausible in meters and consistent with 2.1 (XY bbox ~30 x 30 m is expected)
- [ ] Triangles at or under 9,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the ground-floor window row and a few upper lights; glow shells proud
      of the opaque glazing
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (per-object signed volume for
      the union of solids; ray test residual <= 0.15%)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + contact sheet + night render regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

- **The height is the weakest number in this dossier, and it is unresolved.** Three
  measurements exist and none of them is today's crest: OSM `height=6`; the 2010 city LiDAR
  *median* of 5.56 m over this footprint; and the 2010 LiDAR *maximum* of 10.92 m. The
  distribution behind those LiDAR figures is tight — mean 5.80 m, standard deviation 0.87 m,
  majority value 5.39 m — which says that in 2010 **almost the entire roof was at about
  5.5 m** and only a small element reached 10.92 m. Yet every current photograph shows a
  full two-storey building. So the second storey as it stands today postdates the 2010
  LiDAR, and every LiDAR-derived height for this lot is stale. This plan's 10.0 m is a
  photogrammetric estimate off a single January 2025 pano (facade height scaled against a
  ~3.2 m ground-floor window opening), with a real uncertainty of about ±0.8 m. **Re-derive
  it, from more than one photograph, and record the method.**
- **Does the second storey run the full depth?** Related to the above and equally
  unresolved. The 2010 LiDAR says one small element was tall and the rest was low; the 2026
  satellite roof shows a change in roof level partway along. The massing recipe in 2.7
  therefore has a conditional step: confirm from oblique aerial or from the Jack London
  Alley flank whether the building steps down toward the rear, and where. Getting this
  wrong is worse than getting the absolute height wrong, because the step is visible from
  the app's default camera angle.
- **"Originally built in the 1920's" vs the assessor's 1947.** The architect's project copy
  and the city's tax roll disagree by two decades. Neither affects the model directly, but
  it is a reminder that the Office Snapshots copy is marketing text about an interior.
- **The Office Snapshots exterior description does not match the photographs.** It calls the
  building "brick-clad" with "large, arched metal-clad windows". The front elevation as
  photographed in January 2025 is charcoal stucco with rectangular oak-framed windows and no
  arches at all. Possible explanations: the copy describes the interior's salvaged brick and
  its internal arched openings; or it describes a different building in the same tenancy; or
  the exterior was re-skinned after the copy was written. **Do not model brick or arches on
  the strength of that sentence** — but do look for a photograph that would justify it
  before ruling it out.
- **16,420 sq ft does not fit on this lot.** Two storeys on a 380 m2 footprint is about
  8,200 sq ft. The published area is double that. Either the tenancy spans the neighbouring
  structure to the southeast (DataSF records a separate, taller footprint `SF3775179` /
  `SF3775016` on that side) or the figure counts something else. AGENTS rule 5 settles what
  to do: model the addressed building on its own measured footprint.
- **Three of the four elevations are inferred.** Only the northwest front has usable
  ground-level photography; the northeast flank faces an open paved strip and is genuinely
  visible, so it deserves a real attempt at reference before it is invented. The Jack London
  Alley and Varney Place panos were not reachable during this research pass.
- **The bay count on the front (four oak window bays plus a door) is inferred from one
  pano** and part of the elevation was outside the frame. Confirm before committing the
  facade rhythm.
- **Style risk.** This is a dark, deliberately plain building. The failure mode is a grey
  slab that reads as untextured procedural geometry rather than as an authored asset. The
  three things that prevent it — the oak accent, the real depth of the upper recess, and the
  pale designed roof — are all called out in 2.6 and 2.7 and none of them is optional.
