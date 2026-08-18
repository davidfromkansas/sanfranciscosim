# 1 South Park (One South Park) — SF-SIM asset plan

The **Oriental Warehouse**-era tobacco warehouse that closes the east end of the South
Park oval, and the biggest building on the oval by a wide margin. A 1919–20 three-storey
reinforced-concrete warehouse on a 1,570 m² corner block, converted in 2004–2007 by
**LDP Architecture** for Santa Fe Partners (builder Webcor) into **One South Park** —
35 loft condominiums plus 5,000 ft² of ground-floor commercial and 35 stacked parking
spaces, with **two more storeys added as a set-back rooftop penthouse** and two curving
light courts carved down through the middle of the plan.

Where every other South Park landmark in this manifest is a 6–18 m tooth in a row, this
one is a **block**: 43 m of party wall on the south-west, 38 m on the south-east, and
two fully exposed hero elevations totalling 48 m — 33.0 m on South Park (north-west) and
28.2 + 5.1 + 15.3 m on Second Street (north-east). Its recognition rests on three things
and nothing else: a **ground-floor arcade of tall round-arched openings** with **white
circular medallions** in the spandrels, **two storeys of big gridded steel-sash windows**
above, and a **bold projecting cornice** at 15.7 m with a **dark, recessive two-level
penthouse** and **landscaped roof terraces** behind it. From the app's aerial camera the
roof is half the building: a raised white penthouse block over warm timber decks, hedges
and a light court.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/1-south-park/`. This document is the plan only: Part 1 is the runnable task
prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `1-south-park` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3928634, 37.7820480` (wall-box AABB centre; the build recentres on the model's own AABB and reports the shipped value) |
| Target height | **20.2 m** to the stair/lift overrun (penthouse roof 18.6 m, main cornice crest 15.75 m, roof deck 15.0 m) — LiDAR-derived, see 2.1 |
| Footprint | six-sided, 1,570 m²; AABB 57.7 × 53.7 m because the block sits at ~45° to the world axes; measured |
| Triangle cap | 20,000 |
| Category | `2` (apartments) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 1 South Park GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of **1 South Park** in San Francisco (One South
Park — the 1919 concrete tobacco warehouse converted to lofts in 2007) and deliver it
as a downloadable, validated GLB.

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
7. `artifacts/300-brannan/` — **the reference implementation.** The immediate
   south-east neighbour, sharing this building's party wall; a large SoMa
   masonry/concrete block on the same 45°-rotated authoring frame, with the same
   problem of a long repeating window grid that must not turn into corduroy.
8. `artifacts/21-south-park/` — the other immediate neighbour and the closest
   precedent for a warehouse arcade on this oval; also the entry whose `exclude: 16`
   sits 38 m from this anchor and must not be disturbed.
9. `artifacts/49-south-park/build_49_south_park.py` — the helper library this build
   should copy: `Face` frames, `prism`, `inset_polygon`, `polyline_offset`,
   `arc_band`, `glow_band`, `rim`, `bevel`, `recentre`, `report`.
10. `docs/asset-plans/1-south-park.md` — this plan, whose dossier is your research
    starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract, `AGENTS.md`
governs repository and integration rules. Do not invent a new style and do not copy
visual instructions from unrelated prompts.

## Must capture

- A **corner block**, not a tooth in a row. Two hero elevations: **33.0 m on South
  Park (north-west, outward normal 315.0°)** and **48.6 m on Second Street
  (north-east, outward normal 44.6°/45.3°) broken by a 5.1 m re-entrant step**.
  Two party walls: 43.2 m south-west (outward 224.6°, against 17–19 South Park, whose
  roof is only 6.6 m so ~9 m of this wall is exposed in the baked city) and 37.8 m
  south-east (outward 135.4°, against 300 Brannan, which is taller and hides it).
- **The arcade.** Every bay of both hero elevations is a tall round-arched opening —
  ~2.6 m wide, sill at 1.05 m, impost at 6.1 m, crown at 7.05 m — in a plain wall on a
  ~4.0 m bay pitch. The arches carry radiating fanlight glazing in the head and a
  gridded sash below. This is the strongest cue at street level.
- **The medallions.** A white circular relief roundel, ~0.75 m across, centred at
  7.0 m in the spandrel between every pair of arches, all the way round both hero
  elevations. Second-strongest cue and almost free to model.
- **The string course** — a projecting band 7.5–8.2 m running unbroken above the
  arcade — and the **main cornice**, a bold crown moulding from 14.55 m to a crest at
  **15.75 m**. Base / body / cap is what stops this reading as a slab.
- **Two storeys of steel-sash industrial windows** above the string course: a taller
  row (sill 8.35, head 11.00) and a shorter row (sill 11.90, head 13.90), each opening
  ~2.9 m wide, nearly filling its bay, with a fine dark grid.
- **The set-back penthouse.** Two storeys added in the 2004–07 conversion, standing
  behind the cornice and DARK against the pale block: roof at **18.6 m**, with a
  stair/lift overrun and mechanical to **20.2 m**, the model's crest.
- **The roof terraces.** Warm timber decking, clipped hedge rows along the parapets, a
  small lawn near the west corner, and pergolas — a ~12 m band on the north-west and a
  ~11 m band on the south-west. The camera looks down; this is half the model.
- **The light court** cut down through the penthouse block (LiDAR floor 9.4 m) — the
  "two curving courtyards" of the conversion, read from above as a dark slot.

## Research 1 South Park independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world orientation,
and gather references covering:

- The **north-west (South Park)** and **north-east (Second Street)** elevations —
  both are visible in the app and both must be right.
- **Aerial and roof views.** The penthouse footprint, terrace bands and light court in
  2.9 are read off Google satellite at z21 (0.059 m/px) plus a DataSF LiDAR height
  histogram. Confirm them.
- **The storey count.** This plan asserts three original storeys plus a two-storey
  set-back addition, on permit PA #200405194312 ("renovation of (e) 3 story concrete
  warehouse. add 2 more stories. adding 35 residential units") and on 36 assessor
  condo lots numbered 101–103 / 201–211 / 301–311 / 401–411. Both are cited in 2.2.
- **The current paint scheme.** The wall reads as a very light near-neutral grey with
  a faint cool cast, the trim a warmer off-white, the penthouse charcoal. Confirm
  before committing hues; the *relations* are much safer than the values.
- **The arch head geometry.** The rectified Second Street elevation in 2.4 measures a
  rise/span of ~0.38, i.e. slightly segmental rather than semicircular, but the
  north-west arches photograph as full semicircles. Pick one and say why.

Prefer architect/engineer publications, owner or institutional material, planning and
permitting documents, architectural press, geolocated photography, and aerial/satellite
imagery over aggregator listings. Real estate listing photos show the building as
marketed; label them *observed (listing photo)*.

## Create a reference dossier

Write `artifacts/1-south-park/REFERENCE.md` containing: source links and what each
establishes; verified dimensions and location; orientation; observations from all six
sides and above; the 3–5 strongest recognition cues; features to preserve; features to
simplify; uncertainties and conflicting evidence. A contact sheet of attributed
reference thumbnails is welcome if legally permissible — do not commit copyrighted
full-resolution imagery.

## Make your own design decisions

Follow the conversion process in `docs/styles/miniature-toy.md` §22: identify the
recognition cues, strip nonessential information, rebuild the massing from a few
confident volumes, exaggerate only the signature features, simplify the facade into
broad rhythms, deliberately design every surface visible from above, evaluate from the
app's high three-quarter aerial camera, then simplify again.

This is a **secondary building** in the style bible's detail budget (§21), but a large
one, and the budget is spent on exactly two things: the **arcade with its medallions**
and the **roof**. Everything else — sash grids beyond a suggestion, the fanlight
radials beyond three or four, the cornice's individual mouldings, the terrace
furniture — goes.

Note the specific style risk here: the failure mode is **corduroy**. Twenty-four
arcade bays and forty-eight upper windows on a 48 m run is a lot of repetition, and if
every opening is modelled at full literal depth the elevation turns into a striped
texture with no form. The discipline is: openings are shallow recesses on one shared
head line and one shared sill line, the piers stay plain, the string course and cornice
stay single clean unbroken rings, and the *silhouette* work happens on the roof.
Read the aerial render early — this building is judged from above first.

The finished asset must be immediately recognizable as One South Park, consistent with
the real building from all sides and above, architecturally credible, and a premium
handcrafted miniature — not photorealistic, not voxel art, not generic low-poly, and
never accurate in one view while invented in the others.

## Scope of the exported asset

Export the single building on assessor block 3775, lots 181–216: the three-storey
block on all six footprint faces, both hero elevations' arcades and window grids, the
string course and cornice, the roof deck with its terraces and planting, the two-level
penthouse, the stair/lift overrun and mechanical, and the light court.

Do not include any surrounding city geometry: South Park (the oval, its lawn, trees or
paths), South Park Street, Second Street, the neighbours at 17–19 South Park or
300 Brannan, the surface car park on the north-west side, street trees, sidewalks,
the sidewalk railroad spur, parked cars, people, plinths, cameras or lights. Temporary
context may appear in review renders but must not leak into the GLB.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary `.glb`;
real-world meters; origin at base center; minimum geometry Z ~ 0; applied transforms;
no negative scales; outward normals; no duplicate or foreign geometry; no image
textures; no transparency; flat-color materials named `Toy_*` from the project
palette; `_Glow` suffix only on surfaces that glow at night; no `Toy_body`; no
cameras, lights, animations, armatures or constraints; no external dependencies; at
most 20,000 triangles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model
drops into the city at its real-world heading — the loader applies no rotation
(`placeGeneric` in `app/src/assets.js` only scales and positions). The South Park
elevation faces **north-west, outward normal 315.0°**; the Second Street elevation
faces **north-east, outward normal 44.6° / 45.3°**. The block is rotated ~45° off the
world axes, so build directly on the measured footprint in 2.3 rather than modelling an
axis-aligned box and rotating it. This is the case the plans README calls out: the
contract's "front faces −Y" rule cannot be honoured literally here, real-world
orientation wins, and the deviation must be recorded in `REPORT.md` with the measured
heading.

**Height normalization:** the tallest geometry in the export — the stair/lift overrun —
must land at exactly the height you verify (this plan's figure is **20.2 m**, with the
penthouse roof at 18.6 m, the cornice crest at 15.75 m and the roof deck at 15.0 m) so
the loader's `targetHeightM / measuredHeight` scale is 1.0. If your research moves the
height, move the model and the draft manifest entry together and say so in `REPORT.md`.

## Reproducible Blender workflow

Blender 5.2 LTS. Headless: `blender -b --python script.py -- args`.

Keep `artifacts/1-south-park/build_1_south_park.py` (deterministic build script),
`artifacts/1-south-park/1-south-park.blend`, and
`artifacts/1-south-park/1-south-park.glb`. The script must rebuild the model reliably
enough for future revision. Do not modify or rename an unrelated existing GLB to
satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras: `1-south-park-top.png`,
`1-south-park-north.png`, `1-south-park-east.png`, `1-south-park-south.png`,
`1-south-park-west.png`, plus `1-south-park-contact-sheet.png`, at least one high
three-quarter aerial beauty render `1-south-park-aerial.png` taken over the **north
corner** so both hero elevations, the re-entrant step and the roof are in frame, and a
night render `1-south-park-aerial-night.png`.

The four elevations must share scale, framing, lighting, exposure and projection; use
orthographic or long-lens cameras; label directions from the researched orientation;
the top view must clearly show the penthouse block, the terrace bands, the light court
and the overrun; the aerial view uses the style bible's camera assumptions (30–50
degrees down, long lens). Simple tabletop lighting, neutral warm background, minimal
depth of field, and every image must depict the same exported model.

For the night render, drive the `_Glow` materials from Base Color (copy `Base Color`
into `Emission Color`, strength 1.0) — see the note at the end of
`docs/asset-plans/README.md`. A re-imported GLB's `_Glow` materials otherwise render as
white slabs.

## Validate the exported GLB

Re-import `1-south-park.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture count,
camera count, light count, animation count, applied-transform status, negative-scale
status, normal-orientation status, unexpected geometry, and per-material contract
compliance. Render at least one review image from the re-imported asset. Write
`artifacts/1-south-park/validation.json` and `artifacts/1-south-park/REPORT.md`.

Note that the axis-aligned XY bounding box will be roughly **58 × 54 m** even though no
side of the building is longer than 43 m — that is the expected consequence of a ~45°
real-world heading, not a scale error.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this draft
entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "1-south-park",
  "file": "1-south-park.glb",
  "anchor": [
    -122.3928634,
    37.7820480
  ],
  "targetHeightM": 20.2,
  "cat": 2,
  "name": "One South Park (1 South Park)",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`,
or any app code in this task. Integration is a separate, explicitly requested job — run
`docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes
in `docs/asset-plans/1-south-park.md`.
````

---

## Part 2 — Research and design dossier

Compiled 18 August 2026 from the sources in 2.2. Values marked *inferred* or
*estimated* are visual or derived, not published figures — the executing agent must
re-verify anything it relies on.

Two things make this dossier unusually firm for a building with no landmark
designation report. First, the assessor's 36 condominium lots give the storey
structure exactly: three retail/residential addresses on level 1, eleven units each on
levels 2, 3 and 4, of which eight of the level-4 units are recorded as two-storey —
2 + 11 + 11 + 11 = the 35 units the developer advertised. Second, the building was
photographed from two Google Street View positions whose camera coordinates could be
independently confirmed to under a metre from three known footprint corners, which
allowed the Second Street elevation to be **rectified to a true orthographic drawing
with a metric grid** (2.4). Every storey line below is read off that drawing.

### 2.1 Verified facts

| | | Source |
|---|---|---|
| Address | 1 South Park (a.k.a. 1 S Park St / 1 South Park Ave), SF 94107 | OSM, assessor |
| Assessor | block **3775**, lots **181–216** (36 condominium lots) | `wv5m-vpq2` |
| Original building | 1919–20 reinforced-concrete tobacco warehouse, 3 storeys | permits, LDP |
| Conversion | 2004–2007, **LDP Architecture**; developer Santa Fe Partners, builder Webcor | LDP, thefrontsteps |
| Programme | 35 loft condominiums (9 of them two-level penthouses), ~5,000 ft² ground-floor commercial, 35 at-grade stacked parking spaces, 2 interior light courts, roof decks | LDP |
| Gross area | 52,164 ft² (4,846 m²) | LDP |
| Storeys | **3 existing + 2 added = 5**, the upper two set back on the roof | permit PA #200405194312 |
| Footprint | **1,570 m²** (OSM way 112759870, cleaned); DataSF LiDAR polygon `SF3775181` 1,585 m² | OSM, DataSF |
| Roof heights | LiDAR over 5,142 cells: **median 17.77 m**, mean 17.21, mode 18.76, **max 20.22**, min 9.42, σ 1.80; ground 13.33 m NAVD88 | DataSF `ynuv-fyni` |
| OSM height tag | 18 m | OSM |
| Main cornice crest | **15.75 m** *(rectified photogrammetry, ±0.6 m)* | 2.4 |
| Penthouse roof | **18.6 m** *(derived — see the histogram argument below)* | 2.1 |
| Model crest | **20.2 m** = LiDAR `hgt_max` | DataSF |
| Anchor (wall-box AABB centre) | `-122.3928634, 37.7820480` | derived |

**Why the roof is two levels, from one histogram.** The LiDAR summary is not a single
roof: mean 17.21 sits *below* median 17.77, which sits below mode 18.76, and σ is
1.80 m over a footprint whose satellite image is plainly bimodal — a bright raised
membrane over about 60% of the plan and darker decking over the rest. Fitting a
two-level model, with fraction *f* at height *H* and the rest at *L*:

```
f·H + (1−f)·L = 17.21        (mean)
f(1−f)(H−L)²  = 1.80²        (variance, groups internally flat)
f             = 0.62         (bright-membrane fraction, measured at lum>170 inside the ring)
```

gives **H = 18.6 m, L = 14.9 m**. The independent rectified photogrammetry puts the
cornice crest at 15.75 m with the deck behind it a little lower, and terrace planting
and furniture standing on it — which is exactly what an *L* of 14.9 m means. The two
methods were not tuned to each other and they agree, so the roof structure in 2.9 is
treated as measured rather than inferred. `hgt_max` 20.22 m is the stair/lift overrun,
`hgt_min` 9.42 m the floor of the light court.

### 2.2 Sources

| Source | Establishes |
|---|---|
| **OSM** [`way/112759870`](https://www.openstreetmap.org/way/112759870) | The footprint (8 vertices, cleaned to 6 in 2.3), `addr:housenumber=1`, `addr:street=South Park`, `height=18`. |
| **DataSF Building Footprints** `ynuv-fyni` | Footprint `SF3775181` / `201006.0002174`: 1,585 m², and the full roof-height histogram quoted in 2.1. 2010 LiDAR survey — **after** the 2007 completion, so it sees the finished building including the penthouse. Neighbours: `SF3775046` (17–19 South Park) median **6.60 m**, max 16.90; `SF3775042` (21–29 South Park) median 9.60 m. |
| **SF Assessor secured roll** `wv5m-vpq2`, block 3775 lots **181–216** | 36 condominium lots, all `year_property_built = 2007`. Lot 181 is `Commercial Retail`, 3,611 ft², unit **103**. The rest are residential: **101, 102** (level 1), **201–211**, **301–311**, **401–411** — 2 + 11 + 11 + 11 = **35 units**, matching the developer's figure exactly. Eight of the 4xx lots (401, 403, 404, 407, 408, 409, 410, 411) are recorded as `number_of_stories = 2` — the two-level penthouses. Unit areas 724–2,659 ft². |
| **SF Building Permits** `i98e-djp9`, 85 permits at 1 South Park | The whole conversion in sequence. 1999‑08‑28 "core & shell alt to (e) **3 story** concrete bld seismic strengt"; 2000‑08‑26 "add 1 story w/in (e) bldg per city planning variance"; 2004‑03‑09 "revise seismic upgrade… revise slab elevations"; **2004‑05‑19 PA #200405194312 "renovation of (e) 3 story concrete warehouse. add 2 more stories. adding 35 residential units, off street park…", existing 3 storeys → proposed 5**; 2006–2007 fire, alarm and access-control revisions at 5 storeys; 2009‑11‑16 "convert (e) vacant office space to new deli (the american)" on the ground floor. |
| **LDP Architecture**, [One South Park project page](https://www.ldparchitecture.com/renovation-southpark.html) | "adaptive reuse of a 1920's former tobacco warehouse"; 52,164 ft²; 35 residential units; 5,000 ft² of first-floor commercial; a penthouse unit; at-grade stackers for 35 cars; a rooftop deck; **"two curving courtyards carved out of the interior"**; "enclosed an existing railroad spur with modern fenestration"; an at-grade terrace preserving the historic railroad tracks. Gold Nugget Grand Award 2011; California Construction *Best Renovation of California* 2008. |
| **thefrontsteps**, [Dec 2007 walkthrough](https://thefrontsteps.com/2007/12/16/1-one-south-park-a-walkthrough-and-sales-update/) | Developer Santa Fe Partners, builder Webcor; 35 units of which **9 penthouses**; seismic retrofit; wrap-around penthouse deck; ~$900–1,000/ft² at launch. *observed (sales coverage)*. |
| **Compass / stewardsgroup / helena7x7** listing pages | "modern conversion by LDP Architects preserving historic factory character"; oversized 9-foot windows; exposed concrete ceilings; **preserved railroad track remnants** inside; deeded parking. *observed (listing photo/copy)*; the "1906" and "3 storeys" figures on aggregator pages are wrong and are contradicted by the permits. |
| **Google Street View** panos `Bm7I6a4Jcm8yGuvM9xB_Iw` (South Park street, 23.0 m from the north corner) and `fsz2ATpXhpoUxD3vwNgjew` (Second Street, 16.7 m from the north-east wall) | Every elevation number in 2.4. Both panos' positions were confirmed against three known footprint corners (bearing residual ±0.06°), then the equirectangular tiles were reprojected onto each wall plane to give an orthographic elevation with a metric grid. The vertical scale was checked independently by the **circular medallions**, which come out 0.75 m wide × 0.69–0.75 m tall — i.e. round — so the vertical calibration is good to ~8%. |
| **Google Maps satellite**, z21 (0.0590 m/px) | The roof: the raised penthouse block and its extent, the terrace bands with hedge rows and a lawn patch near the west corner, the light court, the roof-top mechanical, and the fact that the terraces are on the **north-west and south-west** sides only. z22 returns the 1,555-byte no-data placeholder over this block. |
| `artifacts/21-south-park/`, `artifacts/300-brannan/` | The two party-wall neighbours: their heights, their palettes (both `Toy_stone` bodies — see 2.8), and 21 South Park's `exclude: 16` which this integration must not disturb (2.13). |

Not obtained: interior floor plans, the LDP drawing set, and any elevation of the two
party walls. None is needed — the party walls are blind and the south-east one is hidden
by a taller neighbour.

### 2.3 Orientation and placement

The block sits at ~45° to the world axes, like everything on the South Park oval. The
OSM ring has eight vertices, two of which are 1.1 m and 2.7 m survey slivers; cleaning
by intersecting the six real wall lines gives this hexagon. Coordinates are metres in
the project's tangent frame (`+X` east, `+Y` north), relative to the wall-box AABB
centre `-122.3928634, 37.7820480`:

```
S  (  1.939, -26.843)   south corner   (party × party)
E  ( 28.847,  -0.328)   east corner    (party × Second Street)
Cc (  9.003,  19.713)   step, outer
Dd (  5.387,  16.110)   step, inner
N  ( -5.498,  26.843)   north corner   (Second Street × South Park)
W  (-28.847,   3.527)   west corner    (South Park × party)
```

| Face | From → to | Length | Outward normal | What it is |
|---|---|---|---|---|
| South-east | S → E | **37.78 m** | **135.4°** | party wall, 300 Brannan (21 m — taller, hides it) |
| North-east (south) | E → Cc | **28.20 m** | **45.3°** | hero — Second Street |
| Step return | Cc → Dd | **5.11 m** | **315.1°** | hero — faces back up Second Street |
| North-east (north) | Dd → N | **15.29 m** | **44.6°** | hero — Second Street, recessed 5.1 m |
| North-west | N → W | **33.00 m** | **315.0°** | hero — South Park street |
| South-west | W → S | **43.25 m** | **224.6°** | party wall, 17–19 South Park (6.6 m — ~9 m exposed) |

The **re-entrant step** is real and was confirmed photographically: predicted from the
OSM ring at equirect columns 254 and 341 of pano `Bm7I6a4Jcm8yGuvM9xB_Iw`, the return
wall shows up there flat-on, with one arch in it. The northern 15.3 m of the Second
Street frontage stands 5.1 m back from the southern 28.2 m.

The area centroid is 0.69 m from the AABB centre. Use the **AABB centre**: `placeGeneric`
seats the model's origin, and the contract makes that origin the model's XY bbox centre,
so anchoring on the centroid would put the building 0.69 m off its real footprint. The
build script must recentre on the model's own AABB (which the cornice overhang shifts a
little further) and report the resulting lon/lat.

### 2.4 What each side shows

Every height below is read off the rectified Second Street elevation, which is
orthographic with a metric grid. Tolerance ±0.4 m on the storey lines, ±0.6 m on the
cornice.

**North-east (Second Street), 48.6 m over three planes — hero.** The public face. A
low plinth to 1.05 m; then the **arcade**: round-arched openings ~2.63 m wide on a
~4.0 m bay pitch, springing from a simple impost at 6.10 m to a crown at 7.05 m, the
head filled with a radiating fanlight and the body with a gridded sash. A **white
circular medallion** ~0.75 m across sits in each spandrel, centred at 7.00 m. Above the
arcade a **projecting string course**, 7.50 → 8.20 m, unbroken. Then two window
storeys, both of large steel-sash grids nearly filling their bays: the taller row
8.35 → 11.00 m, the shorter row 11.90 → 13.90 m. Then the **cornice**: bed mould at
14.55 m, crest at **15.75 m**, a bold projecting crown. Behind and above it the
**charcoal penthouse**, set back several metres, its roof at 18.6 m, with roof planting
visible over the parapet from the street. Seven bays on the 28.2 m plane, one in the
5.1 m step return, four on the 15.3 m plane.

**North-west (South Park), 33.0 m — hero.** The same three registers in the same
language: arcade with medallions, string course, two window storeys, cornice. Eight
bays. Two differences worth modelling. First, the arches on this side photograph as
full semicircular fanlights and read taller than the Second Street ones. Second, this
elevation carries the **service and entry bays**: one arch holds a roller shutter (the
car-stacker entrance), and a wider recessed bay near the west end holds the residential
entrance, with the **preserved railroad spur** curving out of it across the sidewalk.
The rails themselves are in the public right of way and are out of scope; the recessed
entry bay is not.

**South-west (party wall, 17–19 South Park), 43.25 m.** Blind. The neighbour's roof is
at 6.60 m (LiDAR median) against this building's 15.0 m deck, so roughly **9 m of this
wall stands exposed** above it and is fully visible in the baked city from the south.
Plain wall, same body colour, no openings, a plain parapet coping — *inferred*, and
safe to infer: a 1919 party wall against a one-storey neighbour is a blank concrete
plane. Above it, the terrace parapet and the hedge line show.

**South-east (party wall, 300 Brannan), 37.78 m.** Blind and hidden: 300 Brannan is
21 m to this building's 15.75 m cornice. Plain wall, no openings. *Inferred*, and no
camera position the app allows can see it.

**Top.** The half of the model that matters most. See 2.9.

### 2.5 Recognition cues (ranked)

1. **The arcade of tall round-arched openings** wrapping both hero elevations, on a
   plain wall, with nothing else at ground level.
2. **The white circular medallions** in the spandrels — small, cheap, and the detail
   nobody else on this oval has.
3. **The block-ness**: a 1,570 m² corner mass with a re-entrant step, twice the plan
   area of anything else on the oval.
4. **The dark two-level penthouse over the pale cornice**, and the landscaped terraces
   around it — the aerial camera's first read.
5. **The two window storeys of gridded steel sash**, one tall row and one short row.

### 2.6 Miniature translation

- Arcade openings: shallow recesses (0.18 m), not deep reveals. The arch head is what
  reads; the reveal depth is not.
- Medallions: exaggerate to **0.90 m** from the measured 0.75 m, and give them a real
  0.10 m proud disc so they catch light from above.
- String course and cornice: single unbroken rings, 0.30 m and 0.45 m proud
  respectively. Do not break them at the step — turn them into the return.
- Upper windows: one recessed panel per opening with a single crossed mullion pair.
  No pane grid. At 4 m bay pitch across 48 m of frontage a real grid is sub-pixel and
  becomes noise.
- Party walls: no openings, no articulation, and no cornice — only the terrace parapet
  above. Two blank planes are correct here and they buy the triangles the roof needs.
- The light court: model it as a real cut, not a painted dark rectangle. From the
  aerial camera a painted slot reads as a stain.

### 2.7 Massing recipe

Heights in metres above the base plane; `t` is measured along each face from its first
listed corner.

| Element | z |
|---|---|
| Plinth top / arch sill | 1.05 |
| Arch impost | 6.10 |
| Arch crown | 7.05 |
| Medallion centre | 7.00 |
| String course | 7.50 → 8.20 |
| Window row 1 | 8.35 → 11.00 |
| Window row 2 | 11.90 → 13.90 |
| Cornice bed mould | 14.55 |
| **Cornice crest** | **15.75** |
| Roof deck / terraces | 15.00 |
| Light-court floor | 9.40 |
| **Penthouse roof** | **18.60** |
| **Stair/lift overrun (crest)** | **20.20** |

1. **Block.** Prism on the six-sided footprint, 0 → 15.00 m, capped at the deck.
2. **Plinth.** 0.06 m proud band, 0 → 1.05 m, on the two hero faces only.
3. **Arcade.** Per hero face, uniform bay division: **7 bays** on E→Cc (pitch 4.03 m),
   **1 bay** in the step return, **4 bays** on Dd→N (pitch 3.82 m), **8 bays** on N→W
   (pitch 4.13 m). Each bay: a 0.18 m recess 0.67 × pitch wide, from the sill to a
   round head of rise 0.42 × width; glazing plate inset behind it; a trim archivolt
   ring 0.10 m proud. 24 bays in all.
4. **Medallions.** One in each spandrel between adjacent arches and one at each end —
   25 discs, r = 0.45 m, 0.10 m proud, 12 segments.
5. **String course.** Ring on the hero faces, 0.30 m proud, 7.50 → 8.20 m.
6. **Windows.** Two rows per hero bay, 0.73 × pitch wide, recessed 0.14 m, with a
   single mullion cross. 48 openings.
7. **Cornice.** Two-step ring on the hero faces (0.28 m proud 14.55 → 15.20, 0.45 m
   proud 15.20 → 15.75) returning at both party-wall corners; parapet coping only on
   the party walls, 15.00 → 15.55.
8. **Roof terraces.** Deck plates at 15.00 in the north-west (12.0 m wide) and
   south-west (11.0 m) bands; hedge rows 0.9 m tall along both parapets; one lawn
   plate near the west corner; two pergola frames.
9. **Penthouse.** Prism at 15.00 → 18.60 on the footprint inset by 4.0 m (SE), 4.0 m
   (NE south), 3.0 m (step and NE north), 12.0 m (NW) and 11.0 m (SW); banded glazing
   on all four visible sides; a 0.25 m coping.
10. **Light court.** A 20.0 × 5.5 m slot through the penthouse and the deck down to
    9.40 m, aligned with the Second Street wall, plus a smaller 7.0 × 4.5 m companion.
11. **Overrun and plant.** A 6.5 × 5.0 m box 18.60 → 20.20 m on the penthouse roof and
    two low mechanical blocks 18.60 → 19.35 m.

### 2.8 Materials and palette

Both party-wall neighbours (`21-south-park`, `300-brannan`) are `Toy_stone` bodies.
This building is measurably cooler and lighter than either — sampled off the rectified
elevation it is a near-neutral pale grey — so it takes **one documented off-palette
body colour**, exactly as `49-south-park` did with `Toy_sage`. That is a WARN in
`sf-asset-check`, not a fail, and it is deliberate: three adjacent `Toy_stone` blocks
on one corner would merge into a single beige mass from the aerial camera.

| Material | Hex | Used for |
|---|---|---|
| `Toy_dove` | `d4d6d4` | **off-palette (documented).** The body: all three storeys of wall on all six faces, the plinth, the piers. |
| `Toy_white` | `f7f4ec` | Cornice, string course, archivolts, medallions, window surrounds, parapet copings. |
| `Toy_slate` | `6f7883` | Penthouse walls and the overrun. Precedented by `300-brannan`. **Not `Toy_roofd`** — see the note below. |
| `Toy_ink` | `3a3530` | Arch reveals, the roller-shutter bay, penthouse mullions, mechanical blocks. |
| `Toy_glass` | `2a4d73` | Upper-storey glazing. |
| `Toy_glassl` | `6f95b8` | Arcade fanlights and penthouse glazing. |
| `Toy_steel` | `9aa0a6` | Roof membrane on the penthouse roof and the main deck. |
| `Toy_rust` | `a86444` | Roof-terrace timber decking. |
| `Toy_verdigris` | `9fb8a8` | Terrace hedges, planters and the lawn plate. |
| `Toy_glassl_Glow` | `6f95b8` | Lit residential windows and the penthouse band at night. |
| `Toy_mustard_Glow` | `d9a441` | The arcade at night — the warm spill from the retail and lobby. The hero glow. |

**Do not use `Toy_roofd` (45454a) on any large surface here.** It renders as
rgb(9,9,12) — effectively black — under the app's lighting, which is a shipped lesson
from another landmark on this oval. The penthouse is the model's second-biggest visible
mass and must stay a readable dark grey, not a hole.

**Glow discipline.** `_Glow` surfaces are single faces standing proud of the opaque
glazing, never closed shells: the app draws `_Glow` in a separate layer at opacity
`0.12 + 0.95·uNight`, so a closed shell is two alpha layers deep and reads ~23% by day
instead of 12%. The night composition is one hero — the arcade, lit warm and
continuous, because that is what the building actually does at night — plus an uneven
scatter of maybe two thirds of the 48 upper windows (35 flats, not an office floor) and
a quiet cool band on the penthouse.

### 2.9 Top surface

Read off Google satellite at z21 with the footprint ring drawn over it, and cross-checked
against the LiDAR histogram in 2.1.

- A **raised penthouse block** covering ~60% of the plan, pushed to the north-east and
  south-east and set well back from the other two sides. Bright near-white membrane
  roof with scattered small vents and two low mechanical blocks.
- A **light court** cut down through it — a dark slot roughly parallel to the Second
  Street wall, with greenery at the bottom — plus a smaller companion. LiDAR's 9.42 m
  minimum is this floor.
- A **stair/lift overrun** near the middle-north, the tallest thing on the building.
- A **north-west terrace band** ~12 m wide: warm timber decking, a continuous clipped
  **hedge row** along the parapet (clearly visible in the satellite image as a green
  dotted line), a small green **lawn patch** near the west corner, and planters.
- A **south-west terrace band** ~11 m wide: more decking, pergolas, furniture, planters
  and small storage structures.
- Both terraces are **private roof decks** belonging to the level-4 penthouses, which is
  why they are furnished rather than empty.

The single most important instruction for this model: the roof is not a lid, it is an
elevation. Half the model's readable design lives up there.

### 2.10 Scope

In: the building on lots 181–216, all six faces, the roof and everything on it.
Out: the oval, both streets, both neighbours, the surface car park north-west of the
block, street trees, sidewalks, the sidewalk railroad spur, vehicles, people.

### 2.11 Triangle budget

| Element | est. tris |
|---|---|
| Block prism + party walls + deck | 400 |
| Plinth, string course, cornice rings | 1,200 |
| 24 arcade bays (recess + arch head + glazing + archivolt) | 6,500 |
| 25 medallions (12-seg discs, proud) | 1,800 |
| 48 upper windows (recess + glazing + mullion) | 3,500 |
| Penthouse prism, glazing bands, coping | 1,400 |
| Light courts | 300 |
| Overrun + mechanical | 350 |
| Terraces: decks, hedges, lawn, pergolas, planters | 2,500 |
| Bevels and slack | 2,000 |
| **Total** | **~19,950** |

Cap **20,000**. Well inside the 30,000 standard-landmark budget in `AGENTS.md`, and the
first thing to cut if it runs over is the pane detail on the upper windows, then the
medallion segment count.

### 2.12 Draft manifest entry

```json
{
  "id": "1-south-park",
  "file": "1-south-park.glb",
  "anchor": [-122.3928634, 37.7820480],
  "targetHeightM": 20.2,
  "cat": 2,
  "name": "One South Park (1 South Park)",
  "estimated": false,
  "loadRadius": 2500
}
```

`loadRadius` by the default rule `max(2500, targetHeightM × 30)` = `max(2500, 606)` =
**2500**. Not `alwaysLoaded`: at 20 m this is not a skyline piece.

### 2.13 Integration notes (for later, not this task)

**Case B** — `1SouthPark` does not exist in `pipeline/lib/landmarks.mjs` or
`app/src/landmarks.js`, so integration needs a registry entry, an exclusion radius and
a tile re-bake, plus audit 1.6.

The exclusion must be sized against the real bake inputs (`pipeline/data/
buildings_datasf.geojson` and `overture_buildings.geojsonseq`) after `simplifyRing(0.6)`,
by the rule `excluded()` actually uses — a footprint is dropped when its **centroid OR
any ring vertex** is inside the radius. Two constraints are known in advance and both
are unusual for this oval:

- **The floor is large.** This is a 57.7 × 53.7 m AABB, so this building's own DataSF
  polygon has ring vertices ~28 m from the anchor. A radius that only clears the
  centroid will leave the procedural block standing through the asset. Expect the floor
  to be set by this building's own geometry, not by a gap-fill twin.
- **The ceiling is close.** `21SouthPark` sits **38.3 m** away with `exclude: 16`, and
  its own dossier records that its ceiling was already tight (17.29 m, set by
  17–19 South Park). `300Brannan` is **39.2 m** away with `exclude: 12`, `2SouthPark`
  **49.9 m** with `exclude: 9`. None of those may be disturbed, and 17–19 South Park
  (which has no GLB) must survive.

If the window turns out to be empty — i.e. no radius both clears this building's own
footprint and spares 17–19 South Park — the answer is a smaller radius plus an explicit
note, not a silently deleted neighbour. See the merged-parcel and two-ring cases already
recorded for this oval.

`clearTrees`: **no**. The street trees on both frontages are real, they are in every
photograph, and they stand in the road reserve outside the building line.

**Batch mode applies.** This landmark is being built alongside others: run the bake and
the full local QA on it, then `git checkout -- app/public/tiles api/_data` before
committing, and commit source only. `git diff --name-only origin/main` must list nothing
under `app/public/tiles/` or `api/_data/`.

### 2.14 Validation checklist

- Crest exactly 20.20 m; `targetHeightM / measuredHeight` = 1.000.
- min Z = 0 ±0.001; XY centre offset ≤ 0.01 m.
- AABB ≈ 58 × 54 m — expected, not a scale error.
- ≤ 20,000 triangles; no textures, no transparency, no `Toy_body`.
- All materials `Toy_*`; `Toy_dove` flagged as the one documented off-palette WARN.
- Normals: per-object signed volume positive for every solid; ray test residual ≤ 0.15%.
- `_Glow` surfaces are open plates standing proud of their opaque glazing, never shells.
- Fresh-scene re-import validated, not the source scene.

### 2.15 Open questions and risks

1. **Cornice height carries ±0.6 m.** It comes from photogrammetry with an assumed
   2.3–2.6 m camera height. The crest (20.2 m) and the penthouse roof (18.6 m) are
   LiDAR-backed and firm; the cornice is the softest number in the model. If it moves,
   move the storey lines under it proportionally, not the crest.
2. **Arch head geometry.** The rectified Second Street elevation gives rise/span ≈ 0.38
   (segmental); the north-west arches photograph as full semicircles. The plan models
   0.42 as a compromise. Verify and record whichever you pick.
3. **The 12-foot-ceiling claim.** Listings advertise 12-foot ceilings; the rectified
   elevation gives 3.2 m and 3.0 m floor-to-floor on levels 2 and 3. Both can be true
   only in the double-height ground floor or the penthouses. The elevation wins for
   modelling; the discrepancy is noted so nobody "corrects" the storey lines from a
   listing.
4. **Penthouse footprint setbacks** are eyeballed from a z21 satellite image against a
   segmentation that cannot separate bright roof membrane from bright terrace pavers.
   The 60% area fraction is solid; the individual setbacks in 2.7 step 9 are *estimated*.
5. **The two courtyards are described as "curving".** The satellite image shows what
   reads as one long rectilinear slot with a bulge. The plan models two rectilinear
   slots. If better imagery shows real curves, curve them — they are on the roof and the
   aerial camera will see it.
6. **Aggregator disagreement.** rubyhome gives "1906, 3 storeys"; Compass gives 2007.
   The permits and the assessor are the authority: a 1919–20 three-storey warehouse,
   converted to five storeys and 35 units, completed 2007.
