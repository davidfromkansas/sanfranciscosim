# 102 South Park (The Park View) — SF-SIM asset plan

A 1913 four-storey residential hotel on the north rim of the South Park oval, 25 feet wide
and 100 feet deep, with Caffe Centro under it. Built as the **Hotel Bo-Chow** in what was
then the Japanese quarter of South Park, later the **Park View Hotel**, and since the
1980s a Mission Housing SRO — 40 rooms of permanent supportive housing plus one commercial
space, rehabilitated 2019–2022 as part of the 108-unit *South Park Scattered Sites*
project with the Gran Oriente Filipino next door and the Hotel Madrid across the oval.

It is the first building in the South Park set that is neither a warehouse conversion nor
a tech office: a **greige stucco Edwardian hotel front with three round-arched windows per
floor, picked out in dusty blue-gray, under a white bracketed cornice**. On a park ringed
by charcoal offices and brick lofts, it is the one building with a period facade — and at
7.8 m of frontage it is also the narrowest thing in the manifest. The design brief is
"the little arched-window hotel on the park", not "landmark".

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/102-south-park/`. This document is the plan only: Part 1 is the runnable task
prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `102-south-park` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3943678, 37.7817707` (footprint OBB centre) |
| Target height | **14.0 m** to the front cornice crest — *estimated*; the roof deck at 12.9 m is LiDAR-measured (see 2.1 and 2.15) |
| Footprint | 7.78 m (South Park frontage, SE) x 29.76 m deep; 217.8 m2, measured |
| Triangle cap | 9,000 |
| Category | `7` (hotel) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 102 South Park GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of 102 South Park (The Park View) in San Francisco
and deliver it as a downloadable, validated GLB.

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
7. `artifacts/181-south-park/` — the closest reference implementation for the *build
   machinery* (footprint-driven prisms, `face_panel` openings, ring bands, the bevel
   budget) though its architecture is completely different
8. `artifacts/155-south-park/` — the closest reference for a narrow party-wall row
   building on the same oval
9. `docs/asset-plans/102-south-park.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract, `AGENTS.md`
governs repository and integration rules. Do not invent a new style and do not copy visual
instructions from unrelated prompts.

## Must capture

- The **extreme narrow-front proportion**: 7.78 m of frontage on South Park running
  29.76 m back. Four storeys on a 25-foot lot. This proportion IS the building and it is
  what makes it read next to its 13–30 m-wide neighbours.
- The **three round-arched windows per floor** on the second and third storeys, with
  semicircular fanlights, blue-gray architraves, a keystone at each crown and impost
  blocks at the springing. Three bays across 7.78 m — the rhythm is tight and vertical.
- The **fourth-floor register change**: three plain rectangular double-hung windows, same
  bay centres, same blue-gray surrounds, no arches. The facade gets simpler as it rises.
- The **dusty blue-gray trim against warm greige stucco** — the building has exactly two
  colours and that pairing is its identity on an otherwise neutral block face.
- The **white bracketed cornice** capping the front, with a flat parapet above it. The
  cornice is a front-elevation event only; the flanks and rear get a plain parapet.
- The **Caffe Centro storefront** at ground level: dark shopfront joinery, a projecting
  green awning across most of the frontage, and a separate narrow residential entry at the
  northeast end that serves the 40 SRO rooms above.
- The **white membrane roof carrying rows of dark solar panels** (installed in the
  2019–2022 Mission Housing rehab) — the surface the app's camera actually sees most.
- The **light-well notches on the southwest party-wall side**, which the roof shows as
  slots from above.

## Research 102 South Park independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world orientation, and
gather references covering:

- The southeast (South Park) front, which is the only well-photographed elevation
- Aerial and roof views — the solar layout in 2.9 is read off satellite imagery only
- The northeast flank toward Jack London Alley, which is genuinely exposed
- The rear (northwest) elevation toward Bryant Street, for which nothing was found
- Day and night appearance
- Whether the fourth-floor windows are really rectangular and the second and third really
  arched — the dossier's reading is from one January 2025 pano and one zoom of it
- Where the roof stair penthouse sits and how tall it is (see 2.15)

Prefer architect/engineer publications, owner or institutional material, planning and
permitting documents, architectural press, geolocated photography, and aerial/satellite
imagery. Never rely on a single photograph, a single AI-generated image, or a single
unsourced 3D model. Separate verified facts from visual inference; if sources disagree,
document the disagreement and decide.

**Two source conflicts are already known and are NOT resolved (see 2.1 and 2.15):**

1. **Build year.** The SF Assessor roll says **1912**; the Alamy caption on a 2017
   photograph of this exact address says **1913** and names the building the Hotel
   Bo-Chow. Neither affects the model. Do not present either as established.
2. **Height.** The 2010 city LiDAR gives a roof-plane median of **12.88 m** and a maximum
   of **15.20 m** over this footprint, with a standard deviation of 1.60 m. The plan takes
   12.9 m as the roof deck and estimates the cornice crest at **14.0 m**; it deliberately
   does **not** take 15.20 m as the crest. **Re-derive the height yourself and say how.**

## Create a reference dossier

Write `artifacts/102-south-park/REFERENCE.md` containing: source links and what each
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
identity cue carried hard — the arched blue-gray window rhythm on a greige wall. Resist
adding hero-tier ornament.

Note the specific style risk here: the building is only 7.78 m wide and four storeys tall,
so at diorama scale the front is a *sliver*. The failure mode is a thin grey stick with
unreadable dots on it. Everything that keeps it alive — the arches, the blue-gray trim,
the white cornice, the green awning — has to be drawn boldly and slightly oversized
(§9 semantic scale). Three windows per floor is the correct count; do not add more.

The finished asset must be immediately recognizable as 102 South Park, consistent with the
real building from all four sides and above, architecturally credible, and a premium
handcrafted miniature — not photorealistic, not voxel art, not generic low-poly, and never
accurate in one view while invented in the others.

## Scope of the exported asset

Export the single building on lot 3775/057: body, cornice and parapet, all four
elevations' openings, the storefront and its awning, and the roof deck with its solar
array and furniture.

Do not include unrelated surrounding city geometry: South Park (the oval, its lawn, paths
or play structure), South Park Street, Jack London Alley, Taber Place, Bryant Street, the
Gran Oriente Filipino next door or any other neighbouring building, street trees (the
flowering trees in front of this building are prominent in every photograph and must
**not** be modelled), the sidewalk, parked cars, café tables, people, plinths, cameras or
lights. Temporary context may appear in review renders but must not leak into the GLB.

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
**southeast, outward normal 135.4°**; the building is rotated roughly 45° off the world
axes, so build directly on the measured footprint polygon in 2.3 rather than modelling an
axis-aligned box and rotating it. This is the case the plans README calls out: the
contract's "front faces −Y" rule cannot be honoured literally here, real-world orientation
wins, and the deviation must be recorded in `REPORT.md` along with the measured heading.

**Height normalization:** the tallest geometry in the export must land at exactly the
height you verify (this plan's estimate is **14.0 m** at the front cornice crest; the roof
deck sits at 12.9 m) so the loader's `targetHeightM / measuredHeight` scale is 1.0. If
your research moves the height, move both the model and the draft manifest entry together
and say so in `REPORT.md`.

## Reproducible Blender workflow

Blender 5.2 LTS. Headless: `blender -b --python script.py -- args`.

Keep `artifacts/102-south-park/build_102_south_park.py` (deterministic build script),
`artifacts/102-south-park/102-south-park.blend`, and
`artifacts/102-south-park/102-south-park.glb`. The script must rebuild the model reliably
enough for future revision. Do not modify or rename an unrelated existing GLB to satisfy
the task.

## Required review renders

Render the exact final geometry from controlled cameras: `102-south-park-top.png`,
`102-south-park-north.png`, `102-south-park-east.png`, `102-south-park-south.png`,
`102-south-park-west.png`, plus `102-south-park-contact-sheet.png`, at least one high
three-quarter aerial beauty render `102-south-park-aerial.png`, and a night render
`102-south-park-aerial-night.png`.

The four elevations must share scale, framing, lighting, exposure and projection; use
orthographic or long-lens cameras; label directions from the researched orientation; the
top view must clearly show the solar array, the parapet ring, the stair penthouse and the
light-well slots; the aerial view uses the style bible's camera assumptions (30-50 degrees
down, long lens). Simple tabletop lighting, neutral warm background, minimal depth of
field, and every image must depict the same exported model.

For the night render, drive the `_Glow` materials from Base Color (copy `Base Color` into
`Emission Color`, strength 1.0) — see the note at the end of `docs/asset-plans/README.md`.
A re-imported GLB's `_Glow` materials otherwise render as white slabs.

## Validate the exported GLB

Re-import `102-south-park.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture count, camera
count, light count, animation count, applied-transform status, negative-scale status,
normal-orientation status, unexpected geometry, and per-material contract compliance.
Render at least one review image from the re-imported asset. Write
`artifacts/102-south-park/validation.json` and `artifacts/102-south-park/REPORT.md`.

Note that the axis-aligned XY bounding box will be roughly **26 x 26 m** even though the
building is 7.78 x 29.76 m — that is the expected consequence of a ~45° real-world
heading, not a scale error.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this draft
entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "102-south-park",
  "file": "102-south-park.glb",
  "anchor": [
    -122.3943678,
    37.7817707
  ],
  "targetHeightM": 14.0,
  "cat": 7,
  "name": "The Park View (102 South Park)",
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
`docs/asset-plans/102-south-park.md`.
````

---

## Part 2 — Research and design dossier

Compiled 16 August 2026 from the sources in 2.2. Values marked *inferred* or *estimated*
are visual or derived, not published figures — the executing agent must re-verify anything
it relies on. Like the other South Park plans this dossier is thin on published
architectural literature: the building has never been written about as architecture. The
primary evidence is city data plus photography, and the strongest single source is the
January 2025 Street View pano of the front.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Address | 102 South Park (the street is signed "SOUTH PARK"; Google and the café both write "102 S Park St") | SF Assessor `property_location`; OSM `addr:housenumber=102` |
| Block / lot | 3775 / 057 | SF Assessor secured roll 2018–2025; DataSF building footprint `mblr = SF3775057` |
| Built | **1912** per the assessor; **1913** per the Alamy caption naming it the Hotel Bo-Chow | assessor secured roll vs. Alamy J7M52Y — **unresolved**, see 2.15 |
| Storeys | **4** | SF Assessor `number_of_stories = 4.0`; confirmed by the Jan 2025 pano (ground floor + three upper) |
| Property class / use | "Residential Hotel & SRO" / "Commercial Hotel" | SF Assessor secured roll |
| Lot area / building area | 2,583.75 sq ft (240.0 m2) / 10,350 sq ft — i.e. four floors of full-lot plate | SF Assessor secured roll |
| Units | 40 SRO rooms plus one commercial space | Mission Housing property page for The Park View |
| Original name | **Hotel Bo-Chow**, built in the Japanese community of South Park; later the **Park View Hotel** | Alamy caption on a 23 May 2017 photograph located at 102 South Park St |
| Owner / operator | Mission Housing Development Corporation; management by Hyder Property Management | missionhousing.org/parkview |
| Rehabilitation | Part of *South Park Scattered Sites* — Park View (40 units) + Hotel Madrid (44) + Gran Oriente (24) = 108 units, rehabbed as one asset; $34.2 M JPMorgan Chase construction bond, MOHCD, LDP Architecture; construction c. 2019–2022 | Bisnow, ConnectCRE, missionhousing.org |
| Ground-floor tenant | **Caffe Centro**, South Park's oldest coffee shop; closed Aug 2023, reopened 24 May 2024 as a worker-owned collective | SFGate, Mission Local, Mission Housing |
| Footprint | 217.8 m2; 7.78 m (SE frontage) x 29.76 m deep, oriented bounding box, 93.7% filled | OSM way/124884353 reprojected — **measured** |
| DataSF footprint (cross-check) | 251.3 m2, `SF3775057`, 84% overlapping the OSM polygon | DataSF LiDAR building footprints |
| Roof height, 2010 LiDAR **median** | **12.88 m** (majority 12.71 m, mean 12.58 m, σ 1.60 m) | DataSF `hgt_median_m` — measured; this is the roof deck |
| Roof height, 2010 LiDAR **maximum** | 15.20 m | DataSF `hgt_maxcm` — measured, small area; **not** taken as the crest, see 2.15 |
| Ground elevation | 9.62 m (NAVD88) | DataSF `gnd_min_m` — the app's terrain handles this, not the asset |
| Front cornice crest | **~14.0 m** | *estimated*: 12.88 m LiDAR roof deck plus a cornice/parapet of ~1.1 m read off the Jan 2025 pano; ±0.6 m |
| Frontage heading | front faces 135.4° (SE, toward the park); rear faces 315.4° (NW) | measured from the footprint polygon |
| OSM tagging | `building=retail`, no `height`, no `building:levels` | OSM way/124884353 — the `retail` tag describes the café, not the building; do not inherit it |

### 2.2 Sources

- https://www.openstreetmap.org/way/124884353 — footprint, `addr:housenumber=102`,
  `addr:street=South Park`, `building=retail`
- https://www.openstreetmap.org/way/124884343 — 106 South Park, the Gran Oriente Filipino,
  the attached southwest neighbour (`height=11`)
- https://www.openstreetmap.org/way/113545691 — 92 Jack London Alley, 4 levels, the
  northeast neighbour
- `https://data.sfgov.org/resource/ynuv-fyni` (DataSF Building Footprints, LiDAR-derived),
  record `SF3775057` — the 12.88 m / 15.20 m heights and the height distribution
- `https://data.sfgov.org/resource/wv5m-vpq2` (SF Assessor Historical Secured Property Tax
  Rolls), block 3775 lot 057, rolls 2018–2025 — address, 1912, 4 storeys, SRO class, areas
- https://www.alamy.com/stock-photo-caffe-centro-formerly-the-park-view-and-bo-chow-hotels-built-1913-142428579.html
  — "Built as the Hotel Bo-Chow in 1913 in the Japanese community of South Park … Later the
  Park View Hotel", photograph located at 102 South Park St, 23 May 2017
- https://www.missionhousing.org/parkview — 40 units plus one commercial space, SRO
  programme, management
- https://www.missionhousing.org/granoriente — the attached neighbour at 106, built 1907,
  24 units, acquired 2018
- https://www.bisnow.com/san-francisco/news/affordable-housing/mission-housing-locks-in-funding-for-soma-redevelopments-106048
  — the three-hotel 108-unit scattered-sites deal and its financing
- https://www.connectcre.com/stories/chase-provides-funding-for-rehab-of-three-historic-sros-in-san-francisco/
  — same project, September 2020
- https://www.sccsgroupllc.com/projects/south-park-scattered-sites — contractor page:
  Type V wood frame, ground-floor restaurant tenancy, "preserved historic integrity"
- https://calisphere.org/item/f5f8b90a1a0a9f8bbe6e5220afc76544/ — SFPL Historical
  Photograph Collection, "Park View Hotel, 102 South Park", 24 January 1955 (catalogue
  record; the image itself was not examined)
- https://missionlocal.org/2026/07/south-park-offices-overshadow-the-only-operating-restaurant/
  and https://thedissentsf.com/article/the-last-table-at-south-park — 2026 context: Caffe
  Centro as the oval's only remaining restaurant, three SROs, worker-owned since 2024
- Google Street View, South Park pano, capture **January 2025** — the front elevation
  described in 2.4, at two zoom levels
- Google Maps satellite, 2026 Vexcel imagery — the roof described in 2.9; the "The Park
  View", "Caffe Centro SP" and "Gran Oriente Filipino Hotel" labels in that view are what
  confirm which roof belongs to which address

Exa searches run: `102 South Park San Francisco building Caffe Centro`;
`102 South Park Street San Francisco SRO residential hotel 1912`;
`Park View Hotel 102 South Park San Francisco Mission Housing SRO rehabilitation historic`;
`Mission Housing South Park Community three SRO hotels rehab Park View Madrid Gran Oriente`;
`Hotel Bo-Chow 1913 South Park San Francisco Japanese community history`;
`South Park San Francisco historic resource survey 102 South Park brick facade`. The
architecture-press and historic-survey queries returned **nothing** — there is no
published architectural description of this building. Everything in 2.4 below the assessor
row is read off photographs.

### 2.3 Orientation and placement

The building sits on the **north rim** of the South Park oval, near its west end, with its
narrow front on the park (southeast) and its long flanks running back toward Bryant Street.
The Gran Oriente Filipino at 106 South Park is attached on the southwest; the northeast
flank faces the open ground toward Jack London Alley. Like the whole SoMa grid it is
rotated 45° from the world axes; South Park's own long axis runs at bearing 45°.

Measured footprint polygon, in Blender coordinates (metres, `+X` east, `+Y` north),
already centred on the anchor `-122.3943678, 37.7817707` (the OBB centre, which sits
0.18 m from the polygon's area centroid):

```
( -7.761,  13.243)   ( 13.296,  -7.782)   (  7.761, -13.243)   (  2.376,  -7.859)
(  4.030,  -6.234)   (  2.235,  -4.433)   (  0.581,  -6.069)   ( -1.936,  -3.559)
( -1.373,  -3.007)   ( -3.810,  -0.575)   ( -4.373,  -1.128)   ( -6.468,   0.962)
( -4.981,   2.432)   ( -6.644,   4.090)   ( -8.131,   2.620)   (-13.296,   7.782)
(-10.595,  10.446)
```

Edges, with outward normals:

| Edge | Length | Faces | Elevation |
|---|---|---|---|
| `(-7.761,13.243) -> (13.296,-7.782)` | 29.76 m | NE 45.0° | northeast flank (Jack London Alley side), **exposed** |
| `(13.296,-7.782) -> (7.761,-13.243)` | 7.78 m | SE 135.4° | **South Park front** |
| the seven segments back to `(-13.296,7.782)` | 29.4 m net | SW 225.0° | southwest party wall with 106 South Park, **with three light-well notches** |
| `(-13.296,7.782) -> (-7.761,13.243)` | 7.77 m (two collinear segments) | NW 315.4° | rear |

The southwest boundary is not straight. Three notches are cut into it, all shared with the
Gran Oriente next door: **2.32 m deep x 2.54 m wide**, **0.79 m x 3.44 m**, and
**2.09 m x 2.35 m**, reading from the park end. They are enclosed light wells — invisible
from any street, but they show as slots on the roof, which is the surface the app's camera
sees. Build them; they cost almost nothing on a prism and they are the roof's only
irregularity. The two collinear rear segments are one wall.

Because of the ~45° heading the axis-aligned bounding box is ~26 x 26 m. That is correct.

### 2.4 What each side shows

**Southeast (South Park front)** — The hero elevation and the only one with usable
photography (Google Street View, January 2025). Warm greige stucco, 7.78 m wide, in four
clearly separated registers:

- *Ground floor*: the Caffe Centro storefront. Dark shopfront joinery with a panelled
  bulkhead, a large fixed window, a recessed café entrance with a dark timber door, a
  wall-mounted menu case, and a **projecting dark-green awning** running across most of the
  frontage with the café's name on its valance. At the northeast end, a separate narrow
  entrance door — the residential entry to the 40 rooms above. A plain white beltcourse
  caps the whole ground floor.
- *Second and third floors*: three **round-arched windows** each, on the same bay centres.
  Every window has a semicircular fanlight divided by radiating muntins over a
  double-hung sash, set in a **dusty blue-gray architrave** with a projecting **keystone**
  at the crown and small impost blocks where the arch springs, on a projecting blue-gray
  sill. The two floors are identical; a shallow blue-gray band runs under the third-floor
  sills.
- *Fourth floor*: three **plain rectangular** double-hung windows, same centres, same
  blue-gray flat surrounds and sills, no arches. The facade simplifies as it rises — that
  register change is a real and useful cue.
- *Cornice*: a heavy projecting **white/pale** cornice with a regular row of small
  brackets or dentils under it, and a flat parapet cap above. No signage, no ornament above
  the cornice.

The elevation has exactly two colours: greige and blue-gray, plus the green awning.

**Northeast flank (Jack London Alley side)** — 29.76 m of flank facing open paved ground,
so it is genuinely visible in the real world and unavoidably visible to the app's camera.
No usable ground-level photography was found. *Inferred*: the same greige stucco with a
regular, plain rhythm of rectangular SRO windows on the three upper floors and a mostly
blind ground floor.

**Southwest flank** — Attached to 106 South Park (the Gran Oriente, ~11 m) for its whole
length, with the three light wells of 2.3 between them. The top ~3 m of this wall stands
above the neighbour and is visible. *Inferred*: blank greige stucco, no openings on the
shared plane; the light wells are the only articulation.

**Northwest (rear)** — 7.77 m facing the interior of the block toward Bryant Street. No
photography found. *Inferred*: service elevation — a door and one or two small openings per
floor.

**Top** — See 2.9. The best-evidenced surface after the front.

### 2.5 Recognition cues (ranked)

1. **Three round-arched blue-gray windows per floor on a greige wall**, twice over — the
   only period facade on the oval and the thing that identifies it instantly
2. The **7.78 m frontage on a 29.76 m depth**: four storeys on a 25-foot lot, taller than
   it is wide by nearly a factor of two
3. The **white bracketed cornice** capping a facade that has no other ornament
4. The **register change at the fourth floor** — arches below, plain rectangles above
5. The **green café awning** at the base, the one saturated thing on the building
6. The **white roof striped with dark solar panels**, seen from above

### 2.6 Miniature translation

**Preserve**

- The narrow-front / deep-plan proportion and the real 45° heading
- Three bays, three storeys of them, and the arch-to-rectangle register change
- The two-colour scheme: greige body, blue-gray trim
- The cornice as a front-elevation event, with a plain parapet elsewhere
- The light-well slots on the roof

**Simplify / exaggerate**

- Each arched window becomes one clean opening: a blue-gray arched architrave, a flat glass
  fill, and a keystone block. The radiating fanlight muntins are sub-pixel at city scale
  and are dropped; the **arch itself is what has to survive**, so it is drawn with 7
  segments and a frame widened to ~0.22 m
- The impost blocks and the under-sill band merge into one projecting sill per window
- The cornice brackets become a single chunky two-step cornice profile, not a row of
  modelled brackets — a bracket is one pixel
- The storefront becomes one shopfront window, one café door, one residential door and one
  awning slab; the menu case, signage lettering, lamps and door hardware disappear
- The awning is **widened and thickened** past reality; it is the only saturated element and
  it anchors the base of a very thin facade
- Flank openings become a regular eight-bay rhythm, not a survey of the real ones
- Roof clutter becomes three solar rows, one stair penthouse and two vents

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not a
straitjacket — adjust after the first aerial review render, and adjust *all* of them if the
verified height differs from 14.0 m.

1. Body: extrude the 2.3 footprint (including the three light-well notches) from z=0 to
   z=12.9, `Toy_stone`. One volume; there is no setback anywhere.
2. Storefront beltcourse: a ring band at z=4.00–4.25 following the footprint, projecting
   0.10 m, `Toy_trim`. This is the line that separates the café from the hotel.
3. Front (SE) ground floor: shopfront window 3.5 x 2.6 m at 0.55–3.15 m; café entrance
   1.15 m wide, 0–2.65 m, recessed 0.30 m; residential entrance 1.05 m wide, 0–2.55 m at
   the northeast end. Frames `Toy_ink`, glass `Toy_glass`, doors `Toy_ink`.
4. Awning: a slab across 5.4 m of the frontage at z=3.30–3.62, projecting 1.00 m,
   `Toy_verdigris`. Thicker and deeper than reality on purpose.
5. Front second and third floors: three arched openings each, 1.40 m wide on 1.945 m
   centres, sill at 4.90 / 7.90, spring at 6.10 / 9.10, crown at 6.80 / 9.80. Architrave
   `Toy_glassl` 0.22 m, glass `Toy_glass`, keystone `Toy_glassl` proud of the arch crown,
   sill `Toy_glassl`.
6. Front fourth floor: three rectangular openings 1.40 x 1.55 m, same centres, sill 10.90,
   head 12.45. Surround `Toy_glassl`, glass `Toy_glass`.
7. Northeast flank: eight bays at 3.72 m centres, three floors, 1.10 x 1.70 m rectangular
   openings recessed 0.14 m, surround `Toy_glassl`, glass `Toy_glass`. Ground floor: four
   blind recessed panels.
8. Southwest flank and the light wells: blank. No openings.
9. Rear (NW): a service door 1.0 x 2.4 m and two 0.9 x 1.5 m openings per upper floor.
10. Cornice: on the SE front only, plus 0.9 m returns onto both flanks. Two steps —
    z=12.90–13.45 projecting 0.22 m and z=13.45–14.00 projecting 0.42 m — `Toy_trim`. **The
    upper step's top face is the bounding-box top and must land exactly on 14.00 m.**
11. Parapet: a ring band on the other three sides, z=12.90–13.40, 0.28 m thick,
    `Toy_stone` with a `Toy_steel` coping.
12. Roof deck at z=12.90, `Toy_white`. Three solar rows of 4 panels each,
    2.4 x 1.1 x 0.12 m, tilted flat, `Toy_navy`; one stair penthouse
    2.6 x 2.2 m from 12.90 to 13.90, `Toy_steel`; two vents 0.5 x 0.5 x 0.7 m, `Toy_steel`.
13. Bevel 0.12 m / 2 segments on the masses, 0.05 m / 1 segment on the applied frames, none
    on fills, glow shells or solar panels.

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_stone` | `#d9d2c2` | the whole body, parapet, light-well walls |
| `Toy_glassl` | `#6f95b8` | **the signature blue-gray window architraves, keystones, sills** |
| `Toy_glass` | `#2a4d73` | all glazing |
| `Toy_trim` | `#f3efe6` | the cornice and the storefront beltcourse |
| `Toy_ink` | `#3a3530` | shopfront joinery, both entrance doors, reveals |
| `Toy_verdigris` | `#9fb8a8` | **the Caffe Centro awning** — the one saturated accent |
| `Toy_white` | `#f7f4ec` | roof deck |
| `Toy_navy` | `#2c4a70` | roof solar panels |
| `Toy_steel` | `#9aa0a6` | parapet coping, stair penthouse, vents |
| `Toy_mustard_Glow` | `#d9a441` | the café storefront at night — the hero glow |
| `Toy_glassl_Glow` | `#6f95b8` | a scatter of lit SRO rooms |

`Toy_glassl` is nominally the palette's "light glass" entry; here it is used as an opaque
trim colour because it is the palette's exact match for the observed blue-gray joinery.
The loader only bakes the colour, so the key name carries no behaviour — but say so in
`REPORT.md` so a later reader does not think it is a mistake.

Note on the awning: the real awning is a deeper, more saturated green than
`Toy_verdigris`'s soft sage. The palette has no dark green and off-palette is a WARN, not a
FAIL, so a dedicated `Toy_awning` at roughly `#4f7d63` is permissible if the render shows
the sage disappearing against the greige. Decide from the aerial render and record it.

**Night state (required).** Glow surfaces must be thin shells proud of the opaque glazing —
the app renders `_Glow` in a separate layer that is ~12% alpha by day, so a primary surface
must never be authored as glow. Hero glow: the café storefront, lit warm and lit *fully* —
this is the only lit ground floor on this stretch of the oval and it is the whole reason
the building has a story. Supporting accent: five or six lit windows scattered across the
three upper floors and both visible elevations, never a full floor — an SRO at night is
mostly dark with a few rooms on. Nothing else glows; there is no signage and no crown.

### 2.9 Top surface

A flat white roof 12.9 m up on a 7.78 x 29.76 m plate, in a district the camera flies over
constantly. From 2026 Vexcel satellite imagery the whole Mission Housing row — Park View,
Gran Oriente and their neighbours — carries a bright membrane roof with **large arrays of
dark solar panels laid in regular rows**, installed in the 2019–2022 rehab. On this
building the array runs down the long axis with mechanical units and a stair bulkhead
grouped toward the middle and rear.

This is a gift: solar panels are exactly the "strong graphical repetition" the style bible
asks for from a roof (§10), and a white deck striped with dark navy rows on a narrow plate
will read from any altitude. Keep the array asymmetric — leave the park end of the roof
clear, which is both what the imagery shows and what keeps the cornice edge legible from
above. Keep the parapet coping clearly darker than the deck so the ring reads.

### 2.10 Scope

**In the GLB:** the single building on lot 3775/057 — greige body with its three
light-well notches, cornice and parapet, all four elevations' openings, the storefront and
awning, roof deck, solar array, stair penthouse and vents

**Not in the GLB:** South Park itself, South Park Street, Jack London Alley, Taber Place,
Bryant Street, the Gran Oriente Filipino or any other neighbour, the flowering street trees
in front of the building, sidewalk, café tables, vehicles, people, plinths, cameras or
lights

### 2.11 Triangle budget

Cap 9,000 — a secondary building, and the cap should bind. Suggested split: body with
notches, parapet, cornice and beltcourse ~2k; six arched front openings ~2k; three
rectangular front openings ~0.6k; twenty-four flank openings ~2.4k; storefront and awning
~0.7k; roof furniture and solar ~1k.

The arches are the one place where segment count matters. Seven segments per arch is
enough to read as a curve at diorama scale and is what the budget assumes; going to twelve
costs ~700 triangles for nothing visible.

### 2.12 Draft manifest entry

```json
{
  "id": "102-south-park",
  "file": "102-south-park.glb",
  "anchor": [
    -122.3943678,
    37.7817707
  ],
  "targetHeightM": 14.0,
  "cat": 7,
  "name": "The Park View (102 South Park)",
  "estimated": true,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

`dims` and `tris` are placeholders until the asset is built and validated. `estimated` is
`true` because the cornice crest is not a published figure — flip it to `false` only if the
executing agent establishes the height from a citable source. `cat: 7` is Hotel in
`CATEGORY_LABELS`, which is what the assessor calls it and what the building has always
been; `2` (Apartments) would also be defensible for its present use as permanent
supportive housing.

### 2.13 Integration notes (for later, not this task)

- **New landmark, Case B.** Neither `pipeline/lib/landmarks.mjs` nor `app/src/landmarks.js`
  knows this id. Integration needs a `pipeline/lib/landmarks.mjs` entry
  (`id: '102SouthPark'`) **and a re-bake of the affected tiles**, or the baked procedural
  building on this exact footprint will intersect the GLB.
- The exclusion radius must be **measured against the real bake input**
  (`data/buildings_datasf.geojson`), not guessed from the half-diagonal. This is a
  party-wall site on a 7.78 m-wide lot: 106 South Park is attached, so its ring vertices
  are metres away and `excluded()` tests vertices as well as centroids. Expect the safe
  band to be narrow and low — the 358 Brannan and 165 South Park entries in the registry
  are the precedents for how to write the measurement up.
- **The procedural stand-in here is roughly 12.9 m and the asset is 14.0 m.** The baked
  city takes its height from DataSF/Overture, not from OSM (which has no `height` tag on
  this way), so unlike 101 South Park the procedural block is only ~1 m shorter than the
  asset. An unbaked local check will therefore show a near-perfect overlap and prove
  nothing at all. Do the bake before judging.
- `loadRadius`: the default formula gives `max(2500, 14.0 * 30) = 2500` m. Take the default.
- This is the eighth one-off South Park building. The question 380 Brannan and 101 South
  Park both raised stands and is getting louder: a manifest of individually authored
  25-foot row buildings does not stream well, and the kit/instancing route
  (`KIT-INTEGRATION-PROMPT.md`) is probably the right long-term home for this class.
- If other landmarks are in flight, run stage 5 in **batch mode** (see
  `docs/asset-pipeline/ADDRESS-TO-ASSET.md`): still bake, still QA the bake, then throw the
  bake away and commit source only.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Bounding-box top exactly 14.00 m (loader scale lands at 1.0)
- [ ] Dimensions plausible in meters and consistent with 2.1 (XY bbox ~26 x 26 m is expected)
- [ ] Triangles at or under 9,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the storefront and a scatter of upper windows; glow shells proud of
      the opaque glazing
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (per-object signed volume for
      the union of solids; ray test residual <= 0.15%)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + contact sheet + night render regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

- **The crest is estimated; the deck is not.** The 2010 LiDAR is unusually well-behaved on
  this footprint — median 12.88 m, majority 12.71 m, mean 12.58 m, σ 1.60 m — so the roof
  deck at ~12.9 m is about as solid as a derived number gets, and unlike 101 South Park
  next door there is no evidence of a post-2010 addition. What is *not* measured is the
  1.1 m from deck to cornice crest, which is read off one January 2025 pano at ±0.6 m.
  Re-derive it from a second photograph if one can be found.
- **The 15.20 m LiDAR maximum is deliberately not used.** It sits 1.6σ above the mean, so
  it is not the street-tree artifact that 592 Third Street's max turned out to be — but the
  flowering trees directly in front of this building's cornice are exactly the geometry that
  produces such a reading, and a 2.3 m-tall element above a 12.9 m deck would be a very
  large stair bulkhead on a 7.78 m-wide plate. The plan puts the stair penthouse at 13.9 m,
  *below* the cornice crest, so the bbox top stays the cornice. **If the executing agent
  finds photographic evidence of a tall roof bulkhead, that decision flips and both the
  model and the manifest height move together.**
- **Three of the four elevations are inferred.** Only the southeast front has usable
  photography. The northeast flank faces open ground toward Jack London Alley and is
  genuinely visible from the app's camera, so it deserves a real attempt at reference
  before it is invented.
- **The light-well notches may not run full height.** They are traced from the OSM/DataSF
  footprint, which is a plan outline. If they are only a ground-floor condition, the roof
  loses its slots. Nothing outside the building changes either way, so the risk is limited
  to the roof read — but check the satellite imagery for the slots before committing.
- **1912 vs 1913, and the Bo-Chow name.** The assessor and the Alamy caption disagree by a
  year, and the "Hotel Bo-Chow … Japanese community of South Park" attribution rests on a
  single stock-photo caption. It is a good story and it is probably right — South Park was
  a Japanese neighbourhood before 1942 — but it is one uncorroborated source. Do not put it
  in the manifest `name`; `The Park View (102 South Park)` is what the owner calls it today.
- **No historic-resource survey was found.** Neither an Article 10/11 designation nor a
  DPR 523 form surfaced for this address, despite the contractor's "preserved historic
  integrity" language and the neighbouring Gran Oriente's Filipino-heritage designation
  effort. If one exists it would settle the facade description completely; it is the single
  highest-value source still missing.
- **Style risk.** This is a very thin building — 7.78 m wide and 14 m tall. The failure mode
  is a grey stick whose windows read as noise. The three things that prevent it are the
  boldly drawn arches, the two-colour contrast, and the green awning grounding the base.
  None of them is optional, and none of them should be made *smaller* to be more accurate.
