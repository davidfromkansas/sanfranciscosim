# 108-110 South Park (South Park Cafe) — SF-SIM asset plan

A 1914 two-storey wood-frame shop-and-flats building on the north rim of the South Park
oval, 21 feet wide and 100 feet deep, painted **dark forest green from cornice to
bulkhead on every elevation**. Built in what was then San Francisco's first Japantown —
the National Register nomination for the Gran Oriente Filipino Hotel next door names this
address as the **Omiya Shoten souvenir shop and Biwako Baths**, extant. For most of the
last forty years it has been the **South Park Cafe**, the French bistro whose gold serif
sign still runs across the fascia; the shopfront was papered over and vacant in the
January 2025 pano.

It is the darkest building on the oval's north rim, wedged between the pale stucco Gran
Oriente Filipino at 104-106 (11 m, three storeys) and the navy-blue 112 (6 m). Both party
walls are shared at **0.00 m** — this is a true row building, blind on both flanks, and
only its 6.4 m front on the park, its 6.4 m rear on Taber Place, and its roof are ever
seen. The design brief is "the dark green shopfront on the park", not "landmark".

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/108-south-park/`. This document is the plan only: Part 1 is the runnable task
prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `108-south-park` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3944841, 37.7816792` (OSM footprint area centroid; the lot is a parallelogram so this is also its OBB centre) |
| Target height | **8.45 m** to the front cornice crest — *estimated*; the roof deck at 7.80 m is LiDAR-measured (see 2.1 and 2.15) |
| Footprint | 6.433 m (South Park frontage, SE) x 29.750 m deep; 191.4 m2, measured |
| Triangle cap | 9,000 |
| Category | `5` (restaurant or café) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 108-110 South Park GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of 108-110 South Park (the South Park Cafe building)
in San Francisco and deliver it as a downloadable, validated GLB.

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
7. `artifacts/165-south-park/` — the closest reference implementation, and the source of
   the build machinery: a 6.2 m-frontage party-wall row building on the same oval, with
   footprint-driven prisms, a front frame (`front_rect`), `rim()` parapets and belt
   courses, and a single saturated identity cue
8. `artifacts/135-south-park/` — the same oval at a similar 8.5 m height
9. `docs/asset-plans/108-south-park.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract, `AGENTS.md`
governs repository and integration rules. Do not invent a new style and do not copy visual
instructions from unrelated prompts.

## Must capture

- The **dark forest green**, on all four elevations and the parapet. Front, rear and the
  sliver of the southwest flank that shows above 112 are all the same paint. This colour
  IS the building: on a rim of greige, white and pale grey it is the one dark object, and
  it is what a viewer uses to find it. Do not lighten it to "match the palette" — but do
  not let it collapse to black at aerial distance either (see 2.8).
- The **extreme narrow-front proportion**: 6.43 m of frontage on South Park running
  29.75 m back to Taber Place. Two storeys on a 21-foot lot.
- The **Edwardian shopfront**, which is the whole of the building's close-range identity,
  read bottom to top: green bulkhead, two big plate-glass display bays with a recessed
  entry at the southwest end, two flat black awnings, a pale leaded-glass transom band,
  and above it the **gold sign fascia** running the full frontage.
- The **gold sign band** is the single saturated accent on the building and the equivalent
  of 165 South Park's blue gate. Model it as a flat gold band — the lettering itself is
  not modelled (flat-colour contract, and it is sub-pixel from the app's camera).
- The **three tall upper-storey windows** in a recessed panel between flat pilaster
  strips, under a boxed cornice with a modillion course.
- The **flat roof** with its parapet ring and its line of skylights — the surface the
  app's camera actually sees most.
- The **rear elevation on Taber Place**: the same dark green clapboard, a wide multi-pane
  glazed carriage door at grade, and a paired sash window above. It is genuinely visible
  from the app's aerial camera looking over the alley.

## Research 108-110 South Park independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world orientation, and
gather references covering:

- The southeast (South Park) front. It is well photographed but a large ficus stands
  directly in front of it in every recent capture; the January 2025 pano only clears at
  narrow field of view and from two positions.
- The northwest (Taber Place) rear, which Street View covers at very close range.
- Aerial and roof views — the skylight layout in 2.9 is read off satellite imagery only.
- Day and night appearance, and whether the ground floor is tenanted.
- Whether the upper storey really has **three** windows. Two are clearly visible; the
  third is inferred from the bay spacing behind the tree (see 2.15).

Prefer architect/engineer publications, owner or institutional material, planning and
permitting documents, architectural press, geolocated photography, and aerial/satellite
imagery. Never rely on a single photograph, a single AI-generated image, or a single
unsourced 3D model. Separate verified facts from visual inference; if sources disagree,
document the disagreement and decide.

**Two source conflicts are already known and are NOT resolved (see 2.1 and 2.15):**

1. **Footprint width.** OSM gives a clean 6.433 x 29.750 m parallelogram (191.4 m2); the
   DataSF LiDAR footprint `SF3775059` gives 218.8 m2 over a ragged 14-vertex ring. The
   assessor's lot area is 2,145 sq ft = 199.3 m2. The plan authors on the OSM polygon
   because it is the only one consistent with a 21 x 100 ft lot. **The DataSF ring is
   still what the bake reads, so the exclusion radius at integration must be measured
   against it, not against the OSM polygon.**
2. **Height.** The 2010 city LiDAR over `SF3775059` gives a roof-plane median of
   **7.76 m** and a maximum of **11.88 m**, σ 1.46 m, with the mean (8.63 m) well above
   the median. The plan takes 7.80 m as the roof deck, estimates the cornice crest at
   **8.45 m**, and attributes the 11.88 m maximum to bleed from the attached Gran Oriente
   next door (LiDAR median 11.02 m). OSM tags this way `height=8`. **Re-derive the height
   yourself and say how.**

## Create a reference dossier

Write `artifacts/108-south-park/REFERENCE.md` containing: source links and what each
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

## Scope of the exported asset

Export the single building on lot 3775/059: body, cornice and parapet, the shopfront with
its awnings and sign band, the upper-storey windows, the rear carriage door and window,
and the roof with its skylights and mechanical block.

Do not include unrelated surrounding city geometry: South Park (the oval, its lawn, paths
or play structure), South Park Street, Taber Place, Jack London Alley, Bryant Street, the
Gran Oriente Filipino at 104-106 or 112 next door or any other neighbouring building, the
large ficus street trees in front (prominent in every photograph and must **not** be
modelled), the sidewalk, parked cars, motorcycles, people, plinths, cameras or lights.
Temporary context may appear in review renders but must not leak into the GLB.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary `.glb`;
real-world meters; origin at base center; minimum geometry Z ~ 0; applied transforms; no
negative scales; outward normals; no duplicate or foreign geometry; no image textures; no
transparency; flat-color materials named `Toy_*` from the project palette; `_Glow` suffix
only on surfaces that glow at night; no `Toy_body`; no cameras, lights, animations,
armatures or constraints; no external dependencies; at most 9,000 triangles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model drops
into the city at its real-world heading — the loader applies no rotation (`placeGeneric` in
`app/src/assets.js` only scales and positions). The South Park shopfront faces
**southeast, outward normal 135.34°**; the rear faces **315.34°**. The building is rotated
roughly 45° off the world axes, so build directly on the measured footprint polygon in 2.3
rather than modelling an axis-aligned box and rotating it. This is the case the plans
README calls out: the contract's "front faces −Y" rule cannot be honoured literally here,
real-world orientation wins, and the deviation must be recorded in `REPORT.md` along with
the measured heading.

**Height normalization:** the tallest geometry in the export must land at exactly the
height you verify (this plan's estimate is **8.45 m** at the front cornice crest; the roof
deck sits at 7.80 m) so the loader's `targetHeightM / measuredHeight` scale is 1.0. Nothing
on the roof may poke above the crest. If your research moves the height, move both the
model and the draft manifest entry together and say so in `REPORT.md`.

## Reproducible Blender workflow

Blender 5.2 LTS. Headless: `blender -b --python script.py -- args`.

Keep `artifacts/108-south-park/build_108_south_park.py` (deterministic build script),
`artifacts/108-south-park/108-south-park.blend`, and
`artifacts/108-south-park/108-south-park.glb`. The script must rebuild the model reliably
enough for future revision. Do not modify or rename an unrelated existing GLB to satisfy
the task.

## Required review renders

Render the exact final geometry from controlled cameras: `108-south-park-top.png`,
`108-south-park-north.png`, `108-south-park-east.png`, `108-south-park-south.png`,
`108-south-park-west.png`, plus `108-south-park-contact-sheet.png`, at least one high
three-quarter aerial beauty render `108-south-park-aerial.png`, and a night render
`108-south-park-aerial-night.png`.

The four elevations must share scale, framing, lighting, exposure and projection; use
orthographic or long-lens cameras; label directions from the researched orientation; the
top view must clearly show the skylight line, the parapet ring and the cornice; the aerial
view uses the style bible's camera assumptions (30-50 degrees down, long lens). Simple
tabletop lighting, neutral warm background, minimal depth of field, and every image must
depict the same exported model.

For the night render, drive the `_Glow` materials from Base Color (copy `Base Color` into
`Emission Color`, strength 1.0) — see the note at the end of `docs/asset-plans/README.md`.
A re-imported GLB's `_Glow` materials otherwise render as white slabs.

## Validate the exported GLB

Re-import `108-south-park.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture count, camera
count, light count, animation count, applied-transform status, negative-scale status,
normal-orientation status, unexpected geometry, and per-material contract compliance.
Render at least one review image from the re-imported asset. Write
`artifacts/108-south-park/validation.json` and `artifacts/108-south-park/REPORT.md`.

Note that the axis-aligned XY bounding box will be roughly **25.6 x 25.6 m** even though
the building is 6.43 x 29.75 m — that is the expected consequence of a ~45° real-world
heading, not a scale error.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this draft
entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "108-south-park",
  "file": "108-south-park.glb",
  "anchor": [
    -122.3944841,
    37.7816792
  ],
  "targetHeightM": 8.45,
  "cat": 5,
  "name": "108-110 South Park (South Park Cafe)",
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
`docs/asset-plans/108-south-park.md`.
````

---

## Part 2 — Research and design dossier

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Address | 108-110 South Park (the street is signed "SOUTH PARK"; Google writes "108 S Park St") | SF Assessor `property_location = "0110 0108 SOUTH PARK ST"`; OSM `addr:housenumber=108;110` |
| Block / lot | 3775 / 059 | SF Assessor secured roll; DataSF building footprint `mblr = SF3775059` |
| Built | **1914** | SF Assessor `year_property_built`; LoopNet listing 31654148 "Year Built 1914" — two independent sources agree |
| Storeys | **2** | SF Assessor `number_of_stories = 2.0`; confirmed front and rear in the Jan 2025 panos |
| Units | 2 | SF Assessor `number_of_units = 2.0` |
| Property class / use | "Commercial Retail"; LoopNet subtype "Storefront Retail/Residential" | SF Assessor secured roll; LoopNet |
| Lot area / building area | 2,145 sq ft (199.3 m2) / 4,268 sq ft — i.e. two floors of full-lot plate | SF Assessor secured roll (LoopNet gives 4,000 SF gross leasable) |
| Historic identity | former **Omiya Shoten souvenir shop and Biwako Baths**, in South Park's pre-war Japanese quarter; "extant" | National Register nomination for the Gran Oriente Filipino Hotel (SF Planning case 2016-008192SRV), figure 4 caption and body text |
| Recent tenant | **South Park Cafe** (registered business, Brex Retail LLC, at 108 South Park St); the gold fascia sign is still in place | SF registered-business records via opengovus; Jan 2025 Street View |
| Current state | ground floor **vacant** — display glazing papered/blanked in Jan 2025, and a July 2026 Mission Local piece calls Caffe Centro at 102 the oval's only operating restaurant | Jan 2025 pano; missionlocal.org — *inference from two sources, not a filing* |
| Footprint | 191.37 m2; 6.433 m (SE frontage) x 29.750 m deep, exact parallelogram | OSM way/124884358 reprojected — **measured** |
| DataSF footprint (cross-check) | 218.8 m2, `SF3775059`, 14-vertex ragged ring ~7.4 x 29.4 m | DataSF LiDAR building footprints — **the bake's input, see 2.13** |
| Roof height, 2010 LiDAR **median** | **7.76 m** (majority 7.47 m, mean 8.63 m, σ 1.46 m, 853 cells) | DataSF `hgt_median_m` — measured; this is the roof deck |
| Roof height, 2010 LiDAR **maximum** | 11.88 m | DataSF `hgt_maxcm` — measured; attributed to party-wall bleed from 104-106, see 2.15 |
| Ground elevation | 8.77 m (NAVD88) | DataSF `gnd_min_m` — the app's terrain handles this, not the asset |
| Front cornice crest | **~8.45 m** | *estimated*: 7.80 m deck plus a boxed cornice of ~0.65 m read off the Jan 2025 pano; ±0.4 m |
| OSM height tag | `height=8` | OSM way/124884358 — consistent with the LiDAR deck, no `building:levels` |
| Frontage heading | front faces 135.34° (SE, toward the park); rear faces 315.34° (NW, toward Taber Place) | measured from the footprint polygon |
| Party walls | **both flanks attached at 0.00 m** — 104-106 (way/124884343, `height=11`) on the northeast, 112 (way/124884354, `height=6`) on the southwest | OSM vertex-sharing, measured |

### 2.2 Sources

- https://www.openstreetmap.org/way/124884358 — footprint, `addr:housenumber=108;110`,
  `addr:street=South Park`, `building=yes`, `height=8`
- https://www.openstreetmap.org/way/124884343 — 104-106 South Park, the Gran Oriente
  Filipino, the attached northeast neighbour (`height=11`)
- https://www.openstreetmap.org/way/124884354 — 112 South Park, the attached southwest
  neighbour (`height=6`)
- `https://data.sfgov.org/resource/ynuv-fyni` (DataSF Building Footprints, LiDAR-derived),
  record `SF3775059` — the 7.76 m / 11.88 m heights and the height distribution; also
  `SF3775058` (11.02 m) and `SF3775060` (5.73 m) for the neighbours
- `https://data.sfgov.org/resource/wv5m-vpq2` (SF Assessor Historical Secured Property Tax
  Rolls), block 3775 lot 059 — address, 1914, 2 storeys, 2 units, Commercial Retail,
  2,145 sq ft lot / 4,268 sq ft building
- https://commissions.sfplanning.org/hpcpackets/2016-008192SRV%20-%20Gran%20Oriente.pdf —
  National Register nomination, Gran Oriente Filipino Hotel, 104-106 South Park. Names
  108-110 as the Omiya Shoten souvenir shop and Biwako Baths (figure 4, c. 1915), notes
  the Morino family's Omiya Hotel at 108, and records a 1960 fire that "broke out in the
  adjacent building at 108 South Park Street" and damaged the Gran Oriente's roof and
  southwest wall. Also the best description of this block's building type: "two to
  four-story attached, mixed-use flats and multi-unit apartment buildings primarily
  constructed between 1906 and 1924."
- https://www.loopnet.com/Listing/108-110-S-Park-St-San-Francisco-CA/31654148/ — year
  built 1914, 4,000 SF gross leasable, Storefront Retail/Residential, "creative, high-end
  finishes" — *observed (listing)*
- https://opengovus.com/san-francisco-business/1243777-01-201 — South Park Cafe registered
  at 108 South Park St
- https://www.sabariainc.com/properties/108-110-south-park/ — property-manager page for
  108-110 South Park (stub; establishes ownership/management only)
- https://www.sfheritage.org/cultural-districts/soma-pilipinas/landmark-tuesdays-gran-oriente-filipino-hotel/
  — SoMa Pilipinas context for the block
- Google Street View, South Park pano, capture **January 2025** — the front elevation
  described in 2.4, at three fields of view; and the Taber Place pano, same capture, at
  very close range for the rear
- Google Maps satellite, 2026 Vexcel imagery — the roof described in 2.9
- `docs/asset-plans/102-south-park.md` — the immediately adjacent-but-one plan; its 2.3
  orientation analysis and its 2.13 exclusion warning apply verbatim to this lot

Exa searches run: `108 110 South Park San Francisco building Gran Oriente Filipino`;
`108 South Park Street San Francisco facade photo two-story brick storefront`;
`South Park San Francisco historic resource survey 108-110 South Park Biwako Baths Omiya
Shoten building`; `"108 South Park" San Francisco restaurant bar green facade South Park
Cafe tenant`. **No historic-resource survey, DPR 523 form or architectural description of
this building was found** — the only published prose about it is the two paragraphs in the
neighbour's National Register nomination. Everything in 2.4 below the assessor row is read
off photographs.

### 2.3 Orientation and placement

The building sits on the **north rim** of the South Park oval, near its west end, with its
narrow front on the park (southeast) and its long flanks running back to Taber Place. The
Gran Oriente Filipino at 104-106 is attached on the northeast; 112 South Park is attached
on the southwest. Like the whole SoMa grid it is rotated ~45° from the world axes.

Measured footprint polygon, in Blender coordinates (metres, `+X` east, `+Y` north),
already centred on the anchor `-122.3944841, 37.7816792`. The lot is an exact
parallelogram, so its area centroid and its OBB centre coincide and `recentre()` moves
nothing:

```
A  (-12.812,  +8.252)   rear-southwest corner   (Taber Place end)
B  ( -8.236, +12.773)   rear-northeast corner
C  (+12.812,  -8.252)   front-northeast corner  (against 104-106)
D  ( +8.236, -12.773)   front-southwest corner  (against 112)
```

- front edge `D -> C`, 6.433 m, outward normal **135.34°**
- rear edge `B -> A`, 6.433 m, outward normal **315.34°**
- northeast party wall `C -> B`, 29.750 m — blind, hidden by an 11 m neighbour
- southwest party wall `A -> D`, 29.750 m — blind, but ~1.8 m of it shows above 112's 6 m
- axis-aligned XY bounding box **25.62 x 25.55 m** — expected, not a scale error

### 2.4 What each side shows

**Southeast (South Park front)** — the only designed elevation. Bottom to top:

- a green bulkhead about half a metre tall under the glazing;
- two large plate-glass display bays in heavy green frames, occupying most of the
  frontage, with a **recessed entry at the southwest end**: a dark green door with a
  coloured leaded-glass panel over it;
- two **flat black awnings**, one over each display bay, projecting about 0.9 m;
- above them a band of **pale leaded transom lights** with an oval motif in each panel —
  the prettiest thing on the building and the clearest sign of its age;
- above that the **gold serif sign fascia** reading SOUTH P[ARK] CAFE across the full
  frontage, on the green ground;
- a belt course, then the upper storey: **three tall windows** in a shallow recessed panel
  framed by flat pilaster strips at the party lines;
- a **boxed cornice with a small modillion course** under it, capping the front. There is
  no ornate bracket work and no parapet above the cornice; the cornice IS the crest.

**Northwest (Taber Place rear)** — utilitarian but the same paint. A wide pair of
**multi-pane glazed carriage doors** at grade (divided lights over solid panels, dark
green), a small louvered vent above them, a galvanised downspout at the southwest edge, a
security camera and a utility box stencilled `W110 SP`. Upper storey: a **paired
double-hung window group** with light-coloured sash, set roughly centred. Flat top with a
plain boxed cornice, no ornament.

**Northeast flank** — a blind party wall against 104-106, which is 11 m tall. Never seen.

**Southwest flank** — a blind party wall against 112, which is ~6 m tall, so roughly
1.8 m of the upper wall and the parapet show above the neighbour from the aerial camera.
Plain painted wall, no openings.

**Roof** — see 2.9.

### 2.5 Recognition cues (ranked)

1. **It is the dark green one.** On a rim of greige, white and pale grey, this building
   and its navy neighbour are the only dark objects, and this is the green one.
2. **The gold sign band** across the full frontage — the only saturated colour, and the
   thing that says "shopfront on the park" from the aerial camera.
3. **The narrow-deep proportion** — 6.4 m of frontage over 29.8 m of depth, a sliver even
   by South Park standards.
4. **The two black awnings** over the display bays, which give the ground floor a shadow
   line and read as a café even in silhouette.
5. **The three tall upper windows** in their recessed panel under a boxed cornice.

### 2.6 Miniature translation

- Keep the dark green, but at a value that survives the app's daylight: the real paint
  photographs near-black in shade, and a near-black 6 m sliver reads as a hole in the row.
  Author it around **#35493e** — recognisably the same colour, one step up in value.
- Exaggerate the gold sign band: full frontage width, a confident 0.7 m tall, standing
  proud of the wall so it catches its own highlight. No lettering.
- Exaggerate the awnings: two clean black slabs, not fabric. They are the ground floor's
  whole silhouette contribution.
- Collapse the leaded transoms to a single **pale cream band** between the awnings and the
  sign. The oval motif is sub-pixel; the light band under a gold band over black awnings
  is the rhythm that carries.
- Three upper windows as simple recessed dark-blue panes with proud sills, in a recessed
  field between two pilaster strips. No sash divisions.
- The cornice gets a real projection and a modillion course of seven blocks — cheap, and
  it is the only thing above the deck.
- The rear gets exactly two events: the carriage door and the paired window. Nothing else.
- The roof gets a designed line of skylights (§10) and one low mechanical block.

### 2.7 Massing recipe

Everything is authored in world metres on the 2.3 polygon, using the 165 South Park
machinery (`prism`, `rim`, `front_rect`, `edge_return`).

| # | Element | Z range | Notes |
|---|---|---|---|
| 1 | `body` — footprint prism | 0 → 7.80 | dark green walls, `Toy_roofd` top |
| 2 | `parapet` — rim, 0.16 inset | 7.80 → 8.02 | dark green, whole perimeter |
| 3 | `cornice` — front band, 0.22 proud | 7.80 → 8.45 | the crest; `edge_return` dies at both front corners |
| 4 | `modillions` — 7 blocks under the cornice | 7.62 → 7.80 | 0.16 wide, 0.16 proud |
| 5 | `belt` — rim, 0.05 proud | 4.30 → 4.36 | whole perimeter (the SW flank shows) |
| 6 | `bulkhead` — front band, 0.06 proud | 0 → 0.50 | dark green |
| 7 | `display_0/1` — recessed glazing | 0.50 → 2.60 | `Toy_glass`, 0.12 recess |
| 8 | `entry` — recess + door at the SW end | 0 → 2.45 | `Toy_ink` recess, glass over |
| 9 | `awning_0/1` — flat slabs | 2.62 → 2.72 | `Toy_ink`, 0.85 proud |
| 10 | `transom` — pale band | 2.80 → 3.40 | `Toy_trim`, 0.04 proud, over the display bays |
| 11 | `sign` — gold fascia | 3.50 → 4.20 | `Toy_gold`, 0.10 proud, full frontage |
| 12 | `pilaster_w/e` — flat strips | 4.36 → 7.80 | 0.34 wide, 0.07 proud |
| 13 | `upper_0..2` — three windows + sills | 5.05 → 7.20 | 1.05 x 2.15, 0.12 recess |
| 14 | `rear_door` — carriage opening | 0 → 3.40 | recess + glazed upper half |
| 15 | `rear_win_0/1` — paired sash | 5.10 → 6.90 | 0.85 x 1.80 |
| 16 | `skylight_0..3` — roof line | 7.80 → 8.06 | cream frame + dark glass |
| 17 | `mech` — low block, rear third | 7.80 → 8.30 | `Toy_steel`; stays under the crest |

### 2.8 Materials and palette

| Material | Hex | Used for | Palette status |
|---|---|---|---|
| `Toy_verdigris` | `35493e` | body, parapet, bulkhead, pilasters, all four elevations | **off-palette, deliberate** — the palette entry is `9fb8a8`, far too pale. The style bible's SF exception (painted facades are saturated identity) covers it, and 165 South Park set the precedent of keeping the palette NAME while overriding the hex. WARN, not FAIL; recorded in REPORT.md |
| `Toy_mint` | `4f6858` | cornice, modillions, belt course, window casings | **off-palette, deliberate** — a lighter green so the crown and the belt read as articulation rather than as a flat wall. Same justification |
| `Toy_gold` | `caa64a` | the sign fascia, and nothing else | on palette. Using it anywhere else destroys the one identity cue |
| `Toy_trim` | `f3efe6` | transom band, window sills, skylight frames | on palette |
| `Toy_ink` | `3a3530` | awnings, entry recess, rear carriage door frame | on palette |
| `Toy_glass` | `2a4d73` | display glazing, upper windows, rear glazing, skylight glass | on palette |
| `Toy_roofd` | `45454a` | roof deck | on palette |
| `Toy_steel` | `9aa0a6` | roof mechanical block | on palette |
| `Toy_trim_Glow` | `f3efe6` | the transom band at night — the hero glow | day colour matches `Toy_trim` |
| `Toy_glass_Glow` | `6f95b8` | two lit upper windows and one display bay | day colour matches the established glow neighbour |

### 2.9 Top surface

Flat membrane roof, `Toy_roofd`, ringed by a 0.22 m dark green parapet. On it:

- **four skylights** in a line down the long axis, 0.9 x 1.3 m, cream frames with dark
  glass, 0.26 m tall. Satellite imagery shows a run of dark rectangles along the spine of
  this roof; a regular line of four is the graphic simplification (§10, §26).
- **one low mechanical block**, 2.0 x 1.6 x 0.50, in the rear third, `Toy_steel`.
- nothing else, and **nothing above 8.45 m** — the cornice is the crest so the loader's
  scale lands at 1.0.

### 2.10 Scope

In: the building on lot 3775/059 only. Out: the oval and its lawn/paths, the street, the
alleys, both attached neighbours, the ficus street trees, the sidewalk, vehicles, people,
signage lettering, plinths, cameras, lights.

### 2.11 Triangle budget

Cap 9,000. 165 South Park shipped 5,808 tris pre-optimize on comparable content; this
building has a busier shopfront (awnings, transom, sign, entry) but a simpler plan (a
parallelogram, not a bent wedge). Expect 6,000-7,500. If it runs over: drop the modillion
course first, then the skylight frames.

### 2.12 Draft manifest entry

```json
{
  "id": "108-south-park",
  "file": "108-south-park.glb",
  "anchor": [-122.3944841, 37.7816792],
  "targetHeightM": 8.45,
  "cat": 5,
  "name": "108-110 South Park (South Park Cafe)",
  "estimated": true,
  "dims": [25.62, 25.55, 8.45],
  "tris": 0,
  "loadRadius": 2500
}
```

### 2.13 Integration notes (for later, not this task)

- **New landmark, Case B.** Neither `pipeline/lib/landmarks.mjs` nor `app/src/landmarks.js`
  knows this id. Integration needs a `pipeline/lib/landmarks.mjs` entry
  (`id: '108SouthPark'`) **and a re-bake of the affected tiles**, or the baked procedural
  building on this exact footprint will intersect the GLB.
- **The exclusion radius will be the tightest kind in the registry.** Both neighbours share
  party-wall vertices at 0.00 m in OSM, and `excluded()` drops a footprint when its
  centroid OR any ring vertex falls inside the radius. That is the 165 South Park
  situation exactly: the window may only be workable if the circle is centred on the
  **DataSF ring's** area centroid rather than on the manifest anchor. **Measure it against
  `pipeline/data/buildings_datasf.geojson` and the Overture gap-fill, not against OSM and
  not against the half-diagonal.** Write the measurement up the way 165 South Park and
  358 Brannan do.
- **The procedural stand-in is roughly 7.8 m and the asset is 8.45 m**, so an unbaked local
  check will show a near-perfect overlap and prove nothing. Do the bake before judging.
- `loadRadius`: the default formula gives `max(2500, 8.45 * 30) = 2500` m. Take the default.
- This is the ninth one-off South Park row building. The question 380 Brannan, 101 South
  Park and 102 South Park all raised stands: a manifest of individually authored 21-foot
  row buildings does not stream well, and the kit/instancing route
  (`KIT-INTEGRATION-PROMPT.md`) is probably the right long-term home for this class.
- If other landmarks are in flight, run stage 5 in **batch mode** (see
  `docs/asset-pipeline/ADDRESS-TO-ASSET.md`): still bake, still QA the bake, then throw the
  bake away and commit source only.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Bounding-box top exactly 8.45 m (loader scale lands at 1.0)
- [ ] Dimensions plausible in meters and consistent with 2.1 (XY bbox ~25.6 x 25.6 m is expected)
- [ ] Triangles at or under 9,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the transom band, one display bay and two upper windows; glow shells
      proud of the opaque glazing
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (per-object signed volume for
      the union of solids; ray test residual <= 0.15%)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + contact sheet + night render regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

- **The crest is estimated; the deck is not.** The 2010 LiDAR median of 7.76 m over 853
  cells, the OSM `height=8` tag and a two-storey assessor record all agree, so the deck at
  ~7.8 m is solid. What is *not* measured is the ~0.65 m from deck to cornice crest, read
  off one January 2025 pano at ±0.4 m.
- **The 11.88 m LiDAR maximum is deliberately not used.** It sits 2.2σ above the mean, and
  the attached Gran Oriente next door has a LiDAR median of 11.02 m — a party-wall cell
  bleeding across the shared line explains 11.88 m exactly, and a 4.1 m element over a
  7.8 m deck on a 6.4 m-wide plate would be an implausible bulkhead. The plan therefore
  puts nothing on the roof above 8.30 m. **If the executing agent finds photographic
  evidence of a tall roof bulkhead, that decision flips and both the model and the manifest
  height move together.**
- **The third upper window is inferred.** Two upper windows are clearly visible in the
  Jan 2025 pano; the third is placed on the bay rhythm behind the ficus. If a clear
  photograph shows two, drop to two and widen them — do not keep three "because the plan
  said so".
- **Two footprints disagree by 14%.** OSM 191.4 m2 vs DataSF 218.8 m2. The assessor's
  2,145 sq ft (199.3 m2) sits between them and much nearer OSM, and a 21 x 100 ft lot is
  what a 1914 South Park parcel should be, so the plan authors on OSM. The DataSF ring is
  visibly buffered and ragged (14 vertices for a rectangle). This has no effect on the
  model and a large effect on the exclusion radius — see 2.13.
- **The ground floor is vacant and the night state depicts it lit.** The Jan 2025 pano
  shows blanked display glazing, and a July 2026 Mission Local piece implies the café is
  gone. The asset still glows its transom and one display bay at night. That is a style
  bible §16 storytelling choice on a building whose entire identity is its shopfront, not
  a claim about tenancy, and it is recorded here so it is not mistaken for a research
  error.
- **No historic-resource survey was found**, despite the address being named in a National
  Register nomination as an extant pre-war Japantown commercial building. If a DPR 523
  form exists it would settle the facade description completely; it is the single
  highest-value source still missing.
- **Style risk.** A 6.4 m-wide dark building next to an 11 m neighbour can read as a gap
  in the row rather than as a building. The three things that prevent it are the raised
  value of the green, the gold sign band, and the cornice's projection catching the sun.
  None of them is optional.
