# 41–43 South Park — SF-SIM asset plan

A 1911 Edwardian two-flat on the **north-east rim** of the South Park oval, 7.30 m of
frontage against 24 m of depth, gutted and rebuilt as one house in 2012–13 and sold for
$5.7 M in 2014. It survives in the row because of exactly three things, and they are all
on the street elevation: **two canted bay windows**, a **recessed arched entry** on a
stoop between them, and a **charcoal-and-oxblood paint scheme** that makes it the darkest
object on an oval of cream, sage and pale grey neighbours.

It is the second plan in this set for the *narrow-lot party-wall flats* type after
[165–167 South Park](./165-south-park.md), and the useful contrast with it: 165 is the
same footprint proportion with a **flat, bay-less, pale** facade and one blue gate; this
one is **dark, bayed and ornamented**. Built side by side they demonstrate that the type
has range, which is the argument for continuing to hand-build the rim rather than
kit-stamping it.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/41-south-park/`. This document is the plan only: Part 1 is the runnable task
prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `41-south-park` |
| Registry id | `41SouthPark` (`camelId()` in `app/src/assets.js` maps one to the other) |
| Existing procedural builder | none — new landmark (**Case B**: needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor (manifest, placement) | `-122.3934770, 37.7815017` — centroid of the design footprint |
| WGS84 anchor (registry, exclusion only) | `-122.3934851, 37.7815109` — **deliberately different, see 2.13** |
| Target height | **10.60 m** to the front cornice crest (*estimated*, photogrammetric); roof deck **9.83 m** (measured, LiDAR) |
| Footprint | **7.297 m** frontage × **24.0 m** built depth = 175.1 m², on a 7.297 × 32.287 m (235.6 m²) surveyed lot |
| Axis | lot axis **135.08°**; street facade faces **315.08°** (north-west, onto the park) |
| Axis-aligned XY bbox | ~22.8 × 22.8 m — expected, not a scale error: a 3.3:1 bar at 45° to the world axes has a square AABB |
| Triangle cap | 8,000 |
| Category | `1` (House — `CATEGORY_LABELS` in `app/src/context.js`; the assessor classes it `SRES`, Single Family Residential) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 41–43 South Park GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of the Edwardian two-flat at 41–43 South Park,
San Francisco, and deliver it as a downloadable, validated GLB.

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
7. `artifacts/165-south-park/` — **the reference implementation.** Same type (narrow-lot
   party-wall flats on this same oval), same budget class, same authoring frame. Read its
   build script before writing a line; then note that this building is its opposite in
   character — dark where 165 is pale, bayed where 165 is flat, ornamented where 165 is
   plain. Reuse its structure, not its facade.
8. `artifacts/132-south-park/` and `artifacts/168-south-park/` — the two nearest already-built
   rim houses with bay windows, for bay proportion and cornice weight continuity.
9. `docs/asset-plans/41-south-park.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules.

## Must capture

Ranked; if the budget forces a cut, cut from the bottom.

1. **The two canted bay windows, and their asymmetry.** They are not a matched pair.
   The **south-west bay** (garage side) is **two storeys** tall; the **north-east bay**
   (entry side) is **one storey**, at the top only, because the two-storey-high arched
   entry recess occupies the level below it. A modeller who builds two identical
   full-height bays has built the wrong house.
2. **The oxblood top-storey bay.** The north-east bay's top storey is painted a deep
   plum/oxblood; everything else on the building is charcoal. It is the single strongest
   identity cue and the only saturated colour on this stretch of the oval.
3. **The recessed arched entry on a stoop**, between and below the bays, on the north-east
   half of the frontage. It must read as a *hole* — a deep dark recess with steps rising
   into it — not as a painted arch on a flat wall.
4. **The heavy bracketed cornice** with a dentil band, crowning the whole frontage at
   10.60 m and returning over each bay. It is what makes the building read as Edwardian
   rather than modern, and it is the crest the target height normalizes to.
5. **The garage door** filling the south-west half of the ground storey, ~3.15 m wide.
6. **The proportion** — 7.30 m of frontage against 24 m of depth. From the app's aerial
   camera this is the silhouette.
7. **The roof terrace** — a timber deck with a round spa, on the flat pale roof. The
   camera looks down; this is the top surface's only incident and it is documented in
   three independent sources.

## Research 41–43 South Park independently

Do not take the dossier on trust. Re-verify before modelling (plans in this repo have been
wrong before). Re-check at minimum the architectural height, the footprint, the WGS84
anchor, and the real-world orientation, and gather references covering:

- The **north-west (street) elevation**, which is the only elevation the public sees. The
  dossier's facade reading is measured off a single 2013 MLS photograph (2.2); confirm it
  against a second source before building, especially the bay widths, the window counts and
  whether the north-east bay really is single-storey.
- The **roof from above** — flatness, parapet profile, the terrace and spa position, any
  stair bulkhead, chimney or skylight. This is the weakest part of the dossier (2.15).
- The **rear (south-east) elevation** and the rear yard, visible only from the air.
- The two **party-wall flanks**, which are blind.
- Day and night appearance.

Prefer DataSF datasets, SF Planning records, assessor data, geolocated photography and
aerial imagery. Never rely on a single photograph or a single unsourced 3D model. Separate
verified facts from visual inference; if sources disagree, document the disagreement and
decide.

**Four source problems are already known and resolved in 2.1–2.3 and 2.15 — re-check them,
do not silently re-inherit the wrong value:**

1. **Three geometries exist and they do not agree.** The DataSF **parcel** `3775040` is
   authoritative for shape and position; the DataSF **LiDAR footprint** `201006.0038546`
   is authoritative for built depth only (it is offset ~1.9 m streetward); the **OSM way**
   `112759867` is a 5-vertex trace offset ~2.9 m streetward and is used only as a proxy
   for the Overture gap-fill polygon at integration time. See 2.3.
2. **The streetward overshoot of both raster footprints is partly real.** SF bay windows
   project over the property line. Do not "correct" it away entirely: the design carries a
   0.95 m bay projection in front of the wall plane, and only the remainder is treated as
   registration error.
3. **An Exa search will return `archpaper.com`'s "1910 Quarter-Round House" as a match for
   this address. It is not this building** — that project is in Ashbury Heights. The
   summariser hallucinated the address; the page text names the neighbourhood. Discard it.
4. **The Jerry Kler Architects "South Park Facade Restoration" page is a plausible but
   unconfirmed match.** Its description (full facade restoration, 18 windows, new envelope,
   upgraded colour scheme) fits this building's present appearance, but the page never
   states the address. Do not cite it as fact.

## Create a reference dossier

Write `artifacts/41-south-park/REFERENCE.md` containing: source links and what each
establishes; verified dimensions and location; orientation; observations from all four
sides and above; the recognition cues; features to preserve; features to simplify;
uncertainties and conflicting evidence; and **every correction made to this plan**. A
contact sheet of attributed reference thumbnails is welcome if legally permissible — do not
commit copyrighted full-resolution imagery.

## Make your own design decisions

Follow the conversion process in `docs/styles/miniature-toy.md` §22: identify the
recognition cues, strip nonessential information, rebuild the massing from a few confident
volumes, exaggerate only the signature features, simplify the facade into broad rhythms,
deliberately design every surface visible from above, evaluate from the app's high
three-quarter aerial camera, then simplify again.

This is a **secondary-tier building** in the style bible's detail budget (§21) — one step
above 165–167, because it has real ornament and the ornament is the point. Clear massing,
two bays carried hard, one saturated accent, a designed roof. Resist adding ornament the
photographs do not show.

What is NOT negotiable:

- the measured footprint, the 135.08° lot axis and the 315.08° facade heading;
- the bay asymmetry (2.7 recipe steps 5–7);
- the style bible and the asset contract;
- a designed night state.

## Scope of the exported asset

**In:** the single building — the volume on the measured footprint, the two canted bays,
the arched entry recess and its stoop, the garage door, the cornice, the flat roof with its
parapet, the roof terrace and spa, and the rear elevation's openings.

**Out:** 35 South Park (north-east) and 45–49 South Park (south-west), the South Park oval,
its lawn, paths, benches or trees, the street tree in front of the building, the street,
the sidewalk, the rear yard and its planting, fences, vehicles, people, plinths, cameras or
lights. Temporary context may appear in review renders but must not leak into the GLB.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary `.glb`;
real-world metres; origin at base centre; minimum geometry Z ~ 0; XY centre within 0.5 m of
origin; applied transforms; no negative scales; outward normals; no duplicate or foreign
geometry; no image textures; no transparency; flat-colour materials named `Toy_*`; `_Glow`
suffix only on surfaces that glow at night; no `Toy_body`; no cameras, lights, animations,
armatures or constraints; at most **8,000** triangles and 500 KB compressed.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model drops
into the city at its real heading — the loader applies no rotation (`placeGeneric` in
`app/src/assets.js` only scales and positions). Build directly on the measured polygon in
2.3; do not model an axis-aligned bar and rotate it. Record the measured heading in
`REPORT.md`.

**Watch the sign of the heading.** An AABB check cannot tell +45° from −45°, and this
building is symmetric enough in plan to hide a mirror. The check is: in the top render,
the **oxblood bay and the entry stoop must be on the NORTH-EAST half** of the frontage
(the 35 South Park side) and the **garage on the SOUTH-WEST half** (the 45–49 side).
Verify that before anything else.

**Height normalization:** the tallest geometry in the export (the front cornice crest) must
land at exactly **10.60 m** so the loader's `targetHeightM / measuredHeight` scale is 1.0.
Nothing on the roof — parapet, spa, bulkhead — may exceed it. If research proves a roof
structure that does, raise the target and say so; do not clip it.

**Glow shells must be open, not closed.** A closed `_Glow` box is two alpha layers and
reads ~23% by day rather than the intended ~12%, tinting the facade it sits on. Author each
glow surface as a single thin panel proud of its opaque parent.

## Reproducible Blender workflow

Blender 5.2 LTS, headless, one deterministic script:

```
blender -b --python build_41_south_park.py -- --out artifacts/41-south-park
```

No interactive modelling, no random numbers. Keep `build_41_south_park.py`,
`41-south-park.blend` and `41-south-park.glb` under `artifacts/41-south-park/`. Do not
modify or rename an unrelated existing GLB to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`41-south-park-top.png`, `-north-west.png` (the street elevation), `-north-east.png`,
`-south-east.png` (rear), `-south-west.png`, plus `41-south-park-contact-sheet.png`, a high
three-quarter aerial `41-south-park-aerial.png`, and a night render
`41-south-park-aerial-night.png`.

The four elevations must share scale, framing, lighting, exposure and projection; use
orthographic or long-lens cameras; label directions from the researched orientation. The
top view must clearly show the roof plane, the parapet, the terrace and spa, and the
cornice returning over the two bays. Review the **aerial day render first and iterate on
it** before running the formal rig.

Because the building is over three times deeper than it is wide, frame the elevations to
the long dimension and accept empty frame on the street and rear views rather than zooming
each view to fit — the reviewer needs to compare them.

## Validate the exported GLB

`validate_41_south_park.py`: fresh isolated Blender scene, re-import the final GLB, and
validate the re-import, not the source scene. Check every item in 2.14. Report object
count, triangle count, dimensions, bbox min/max, min Z, XY centre offset, material names,
image-texture count, camera count, light count, animation count, applied-transform status,
negative-scale status, normal-orientation status, unexpected geometry, and per-material
contract compliance. Per-object signed-volume normals test is authoritative for the union
of solids; whole-model ray residual ≤ 0.15%. Write `validation.json` and `REPORT.md`.
All checks must PASS before you present.

The axis-aligned XY bounding box will be roughly **22.8 × 22.8 m** even though the building
is 7.3 × 25.0 m. That is the expected consequence of the 135.08° heading, not a scale
error.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this draft
entry in `REPORT.md`. **Do not edit** `app/public/sf-assets/landmarks_manifest.json`,
`pipeline/lib/landmarks.mjs`, or any app code in this task — integration is a separate,
explicitly requested job (`docs/asset-plans/INTEGRATION-PROMPT.md` plus 2.13 below).

```json
{
  "id": "41-south-park",
  "file": "41-south-park.glb",
  "anchor": [
    -122.3934770,
    37.7815017
  ],
  "targetHeightM": 10.6,
  "cat": 1,
  "name": "41–43 South Park",
  "estimated": true,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

`"estimated": true` is deliberate — the crest height is photogrammetric, not published.
See 2.15.
````

---

## Part 2 — Research and design dossier

Compiled 16 August 2026 from the sources in 2.2. Values marked *inferred* or *estimated*
are visual or derived, not published figures — the executing agent must re-verify anything
it relies on.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Address | 41 and 43 South Park, San Francisco CA 94107 | DataSF addresses `ramy-di5m`: both numbers resolve to block 3775, lot 040 — **verified** |
| Parcel | `3775040`, `from_address_num` 41, `to_address_num` 43, zoning `SPD` (SoMa–South Park) | DataSF parcels `acdm-wktn` — **the authoritative confirmation that 41 and 43 are one property** |
| OSM feature | way `112759867`, `building=yes`, `addr:housenumber=41;43` | Overpass — **verified** (geometry rejected for placement, see 2.3) |
| Year built | **1911** | assessor roll `wv5m-vpq2`, `year_property_built` — **verified**; independently corroborated by One Kindesign ("the building's original 1911 facade") |
| Storeys | **3 occupied levels** over grade, plus a roof terrace | Skybox Realty ("4 bedrooms & 3.5 baths over 3 floors"), corroborated by the facade photograph. The assessor's `number_of_stories = 2` counts the two upper flats and ignores the garage level — **do not use it** |
| Units | **2** (a two-flat, since combined into one residence) | assessor roll (`number_of_units` 2, `use_definition` "Single Family Residential") + SocketSite ("technically a two-unit building") — **verified** |
| Construction | type `D` — wood frame | assessor roll — **verified** |
| Gross floor area | 3,600 sq ft (334 m²) on the assessor roll; 4,259 sq ft (396 m²) as marketed in 2023 | assessor roll / Compass MLS 423723952 — the difference is the 2012–13 rebuild, which the roll has not absorbed |
| Lot | **235.6 m²** measured (2,578 sq ft on the roll), **7.297 m** frontage × **32.287 m** deep, a true parallelogram | DataSF parcel polygon — **measured**; the roll's 2,578 sq ft = 239.5 m² agrees to 1.6% |
| Built footprint | **175.1 m²**, 7.297 × 24.0 m, leaving an 8.3 m rear yard | parcel truncated at the LiDAR rear extent; see 2.3 — **derived** |
| LiDAR building | `201006.0038546` (`mblr` SF3775040), 164.8 m², 672 cells at 50 cm | DataSF Building Footprints `ynuv-fyni`, 2010 survey refreshed 2023-09-11 — **measured, but offset, see 2.3** |
| Ground | **11.76 m** NAVD88 (median), 11.46 m minimum, 67 cm total range | same — **measured**; the site is essentially flat, so `placeGeneric`'s single terrain sample is correct here |
| Roof deck | **9.83 m** above grade (LiDAR height median); majority 9.53 m, σ 1.08 m | same — **measured**; a flat roof, so median ≈ deck |
| LiDAR maximum | **11.88 m** above grade; peak first return 23.63 m NAVD88 | same — unexplained, and it predates the 2012–13 rebuild. See 2.15 |
| Cornice crest | **10.60 m** | *estimated*, photogrammetric: 417 px of a 288 px = 7.297 m facade scale, cross-checked against the garage door. See 2.4 and 2.15 |
| Street facade heading | faces **315.08°** (north-west, square onto the park) | measured from the parcel's front line — **measured** |
| Lot axis | **135.08°** into the block, constant (the lot is a parallelogram, not a wedge) | same — **measured** |
| 2012–13 rebuild | gutted and rebuilt behind the retained facade: double-height dining room, ground-floor media room, two-car garage, rollaway skylights, roof terrace with a custom spa | One Kindesign, SocketSite, Leverage/Vanguard, Skybox Realty — **verified across four independent sources** |
| Sale | listed $7,650,000 (Apr 2013), cut to $6,250,000, withdrawn, traded **$5,700,000** on **2014-09-22** | SocketSite + assessor `current_sales_date` — **verified**; the assessor date confirms the blog |
| Owner-occupied | Home Owners exemption on the 2025 roll | assessor roll — **verified** |
| Neighbours | **35 South Park** (lot 102, north-east, pale cream, LiDAR deck 10.49 m) and **45–47–49 South Park** (lot 039, south-west, sage green, LiDAR deck 12.08 m), both party-wall | DataSF parcels + `ynuv-fyni` — **measured** |
| Neighbourhood | South Park, laid out 1852 by George Gordon and built out from 1854 by George Goddard on the model of a London crescent; SF's oldest planned residential square | Wikipedia, TCLF — **verified** |

### 2.2 Sources

- **DataSF `acdm-wktn` (Parcels)**, `blklot=3775040` (and `3775039`, `3775102` for the
  neighbours) — the surveyed lot polygon, the 41→43 address range, the SPD zoning. This is
  the geometric backbone of the plan.
- **DataSF `ramy-di5m` (Addresses with Units)**, `street_name=SOUTH PARK` — the mapping of
  both 41 and 43 to block 3775 lot 040, and of 35 and 45/47/49 to the neighbour lots.
- **DataSF `ynuv-fyni` (Building Footprints, LiDAR-derived)**, building `201006.0038546` —
  footprint, ground elevation and the height statistics behind the 9.83 m roof deck.
- **DataSF `wv5m-vpq2` (Assessor Historical Secured Property Tax Rolls)**, row
  `20253775040` — 1911 build year, 2 units, 3,600 sq ft, wood frame, SRES use, the
  2014-09-22 sale, the Home Owners exemption.
- **Compass MLS #423723952** (`compass.com/listing/41-south-park-street-san-francisco-ca-94107/...`)
  — **the primary photographic source**: a straight-on colour photograph of the street
  elevation from the park lawn, © SFARMLS, from which every facade dimension in 2.4 is
  measured. *Observed (listing photo).*
- `https://socketsite.com/archives/2013/04/41_south_park_a_peek_inside_the_swinging_765_million_ho.html`
  and `https://socketsite.com/archives/2014/10/swinging-7-65m-2013-modern-south-park-home-sells.html`
  — the rebuild, the two-unit status, the rooftop terrace and spa, the price history.
- `https://onekindesign.com/extraordinary-city-retreat-with-eccentric-details/` — "the
  Edwardian appeal of the building's original 1911 facade", the 3,600 sq ft, the two-car
  garage/workspace, the rollaway skylights, the rooftop terrace with custom spa.
- `https://skyboxrealty.com/portfolio/41-south-park/` — "the historically maintained
  Edwardian facade", **three floors** of living space, the roof terrace with SF views.
- `https://www.leveragere.com/articles/view/113/property-of-the-week-41-south-park-san-francisco-ca-vanguard-properties`
  — "from the historically maintained Edwardian façade to the modern amenities".
- **Google satellite imagery, z21 nadir (~0.059 m/px), 2026 capture** — *observed*: the
  flat pale membrane roof, a dark rectangular deck with a pale circular object (read as the
  spa) roughly 12–16 m back from the street, round roof penetrations, and the shaded rear
  yard behind the rear wall.
- **Esri World Imagery, z20 nadir** — *observed*, cross-check on the roof and the row.
- `https://en.wikipedia.org/wiki/South_Park,_San_Francisco` — the oval's 1852 origin, the
  curved line of buildings, the three-and-four-storey character of the rim.

Exa searches run, for the record: "41 South Park San Francisco building"; "43 South Park
Street San Francisco 94107 building history"; "41-43 South Park San Francisco architect
built"; "41 South Park San Francisco Edwardian 1911 facade exterior bay window renovation
architect"; "41 South Park San Francisco rooftop terrace spa roof deck"; "South Park San
Francisco historic district 41 43 South Park 1911 Edwardian". Domains that yielded
material: compass.com, socketsite.com, onekindesign.com, skyboxrealty.com, leveragere.com,
en.wikipedia.org. Two results are traps and are called out in Part 1 and 2.15:
`archpaper.com` (wrong building) and `jerryklerarchitects.com` (address never stated).

### 2.3 Orientation and placement

The building occupies the whole width of its lot on the **north-east rim** of the South
Park oval, sharing party walls with 35 South Park to the north-east and 45–49 South Park to
the south-west. Its street facade sits on the oval's curve and faces **315.08°** — square
onto the park, which is 11.4 m away across the sidewalk and roadway.

Three geometries exist for this building and they do not agree. The plan resolves them as
follows:

| Source | What it is | Verdict |
|---|---|---|
| DataSF **parcel** `3775040` | surveyed lot boundary, 235.6 m², a clean parallelogram | **authoritative for shape and position** |
| DataSF **LiDAR footprint** `201006.0038546` | 2010 raster-derived built area, 164.8 m², 28 ragged vertices | **authoritative for built depth only** — along the lot axis it spans −1.92 m to +24.55 m where the parcel front line is 0 |
| OSM `way/112759867` | 5-vertex trace, 177.5 m², spans −2.88 m to +21.15 m on the same axis | **rejected for placement**; retained only as the stand-in for the Overture gap-fill polygon at integration time (2.13) |

**The streetward overshoot is partly real.** Both raster footprints put geometry in front
of the property line, and San Francisco bay windows legitimately project over it. The
design therefore splits the difference: the **main wall plane sits on the property line**
(u = 0) and the **bays project 0.95 m in front of it** (u = −0.95), which is a normal SF
bay projection and reproduces most of the LiDAR overshoot. The residual ~1 m is treated as
raster registration error and discarded. Applying the same ~0.9 m correction to the rear
extent moves 24.55 m to ~23.6 m, which is why the built depth is set at **24.0 m** — a
figure that also reproduces the assessor's 3,600 sq ft over two counted storeys to within
7%.

**Authoring frame.** Origin at the design footprint's centroid, on the ground, at
`-122.3934770, 37.7815017`. Let `u` run into the lot along bearing **135.08°** and `v`
across it along bearing **45.22°** (so **+v is north-east**, the 35 South Park side, and
**−v is south-west**, the garage/45–49 side). Extents: u −0.95 → +24.00, v −3.6485 →
+3.6485.

Measured design polygon of the main volume, in Blender coordinates (metres, `+X` east,
`+Y` north), already centred on the anchor:

```
( -11.064,   5.926)   front (street) corner, SOUTH-WEST — garage side
(  -5.884,  11.066)   front (street) corner, NORTH-EAST — entry side
(  11.064,  -5.926)   rear corner, north-east
(   5.884, -11.066)   rear corner, south-west
```

The bays project from the front edge to `u = −0.95`, i.e. a further `(−0.671, +0.673)` in
X/Y from each front corner.

Because of the 135.08° heading the axis-aligned bounding box comes out ~**22.8 × 22.8 m**
for a building that is 7.3 × 25.0 m. That is correct and is not a scale error; the
validator should assert the oriented dimensions.

### 2.4 What each side shows

**North-west (street elevation, 315.08° — the only public face).** Measured from the
Compass photograph by scaling the 288-pixel facade width to the surveyed 7.297 m frontage
(39.45 px/m), cross-checked against the garage door, which comes out 3.30 × 2.00 m — a
standard San Francisco garage opening, so the scale is right to within about 5%.

| Element | Measured | Notes |
|---|---|---|
| Cornice crest | **z 10.60 m** | the top of the crown moulding, silhouetted against the sky |
| Dentil band top | z 9.71 m | a continuous row of small dentils under the crown |
| Bay cornice / soffit | z 9.08 m | the bays' own cornices tuck under the main one |
| Storey line, 2nd→3rd | z ≈ 5.60 m | belt cornice on the south-west bay; underside of the oxblood bay |
| South-west bay springs | z ≈ 2.48 m | its apron underside |
| Garage lintel | z 2.05 m | |
| Grade | z 0.00 | sidewalk |
| North-east bay | v +0.50 → +3.45 (2.95 m wide) | **top storey only**, painted oxblood |
| South-west bay | v −0.50 → −3.45 (2.95 m wide) | **two storeys**, charcoal |
| Central pier | v −0.50 → +0.50 (1.0 m) | the only flat strip of frontage |
| Arched entry recess | v +0.55 → +3.15 (2.6 m), z 1.45 → 5.15 head | deep, dark, with the stoop rising into it |
| Garage door | v −0.20 → −3.35 (3.15 m), z 0 → 2.05 | |

Everything is painted one **charcoal slate grey** except the north-east top-storey bay,
which is **deep oxblood/plum**. The window sashes and the horizontal mouldings under each
bay read a full value lighter — pale grey — and that contrast is what makes the ornament
legible at all in a near-black facade. Two burgundy phormium clumps flank the stoop at
grade; a young street tree stands in front of the north-east half.

**North-east and south-west (party flanks).** Blind. The north-east flank abuts 35 South
Park; the south-west flank abuts 45–49. Neither is visible from the app's camera at any
useful angle. Build them as flat charcoal planes with no openings.

**South-east (rear).** Faces a private walled patio and yard, visible only from directly
above. The 2013 rebuild put a "soaring glass wall" here opening onto that yard, so expect a
large opening rather than punched windows. Unverified in elevation; keep it to one big
recessed glazed panel and a door, consistent in materials with the front.

**Top (the real facade).** A flat pale membrane roof at 9.83 m, running the full 24 m
behind a parapet that rises to the 10.60 m cornice at the street end only. Its incidents,
from the nadir imagery and the listing texts: a **timber roof terrace with a round spa**,
roughly 12–16 m back from the street; **rollaway skylights**; and small round penetrations.
The value contrast between the pale roof and the charcoal walls is the single most useful
thing about this building from the app's camera and must be preserved.

### 2.5 Recognition cues (ranked)

1. **The asymmetric pair of bays** — one two-storey, one single-storey — over a recessed
   arched entry. No other house on this rim has that composition.
2. **The oxblood bay against a charcoal building**, on an oval of cream, sage and pale grey.
   The only saturated colour for fifty metres.
3. **The value of the thing.** It is the darkest building on the rim; at thumbnail size it
   reads as a dark notch in a pale row before any detail resolves.
4. **The heavy bracketed cornice with dentils**, returning over both bays.
5. **The pale flat roof with its timber terrace and round spa**, which is what the aerial
   camera actually sees.
6. **The proportion** — 7.3 m of frontage against 24 m of depth, shared with every other
   house on the rim and part of what makes the rim read as a rim.

### 2.6 Miniature translation

**Preserve**

- The 7.297 m frontage, the 24.0 m depth, the 135.08° axis and the 315.08° facade heading,
  exactly
- The bay asymmetry, and which side each bay is on
- The 0.95 m bay projection over the property line
- The arched entry as a genuine recess, and the stoop rising into it
- The flat roof as a genuinely flat plane with the parapet lifting at the street end only
- The single-colour discipline of the real building: charcoal everywhere, one accent

**Simplify / exaggerate**

- Canted bays get **five facets** (front + two 45° returns + two side panels), not a curve.
  Bevel 0.10 m, 2 segments.
- Window openings become clean recessed rectangles, recessed 0.12 m, with a 0.08 m proud
  pale sill and surround. Three lights per bay face on the top storey, one per face below;
  no muntins, no sash divisions — they are sub-pixel.
- The cornice is **exaggerated**: modelled as a 1.50 m tall three-step band (bed, dentil
  course, crown) projecting 0.45 m, where the real one projects perhaps 0.35 m. Justified
  under style bible §9 — it is the Edwardian signature and at 300–500 m viewing distance an
  accurately-scaled cornice is a single dark pixel. The dentils become a repeating notch cut
  0.06 m deep, not modelled blocks.
- The **oxblood** is carried over the *whole* north-east top-storey bay including its
  cornice return, slightly more than the photograph shows, so the accent survives at
  thumbnail size.
- The arched entry's head becomes an 8-segment semicircle; the recess is 0.80 m deep with a
  darker interior, so it reads as a hole from every angle.
- The stoop becomes five 0.29 m risers with solid cheek walls — no balusters, no railings.
- Brackets, mouldings, panel lines, downpipes, meters, house numbers, the phormium and the
  street tree all disappear.
- The spa becomes a 2.0 m diameter cylinder with a 0.25 m rim; the terrace a 4.0 × 3.0 m
  timber platform 0.20 m proud of the membrane.

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are a starting point, not a
straitjacket — adjust after the first aerial review render. All `z` are above grade, all
`v` are across the frontage with **+v north-east**.

| # | Element | Extent | Material |
|---|---|---|---|
| 1 | Main volume | the 2.3 polygon, z 0 → 9.83 | `Toy_roofd` |
| 2 | Roof membrane | flat cap at z 9.83, inset 0.15 m | `Toy_stone` |
| 3 | Parapet | 0.25 m thick, z 9.83 → 10.10, all four sides | `Toy_roofd` |
| 4 | Cornice | street elevation + 0.4 m returns, z 9.10 → **10.60**, projecting 0.45 m, three steps with a dentil notch course at z 9.45–9.71 | `Toy_roofd`, dentil course `Toy_steel` |
| 5 | **South-west bay** | v −3.45 → −0.50, z 2.30 → 9.10, projecting 0.95 m, five facets, its own belt cornice at z 5.50–5.70 | `Toy_roofd` |
| 6 | **North-east bay** | v +0.50 → +3.45, z 5.60 → 9.10, projecting 0.95 m, five facets | `Toy_plum` |
| 7 | Bay aprons | a 0.30 m pale band under each bay's underside | `Toy_steel` |
| 8 | Arched entry recess | v +0.55 → +3.15, z 0 → 5.15, cut 0.80 m into the wall, semicircular head springing at z 3.75 | recess `Toy_ink` |
| 9 | Stoop | five risers 0.29 m, v +1.00 → +2.70, rising to a landing at z 1.45, solid cheeks | `Toy_ink` |
| 10 | Entry door | 1.1 × 2.4 m at the back of the recess | `Toy_ink`, glazing `Toy_glass` |
| 11 | Garage door | v −3.35 → −0.20, z 0 → 2.05, recessed 0.10 m, six shallow horizontal grooves | `Toy_ink` |
| 12 | Bay windows | top storey: 3 lights per bay across the front facet + 1 per return; middle storey (SW bay only): the same; recessed 0.12 m | `Toy_glass`, trim `Toy_steel` |
| 13 | Roof terrace | 4.0 × 3.0 m platform, z 9.83 → 10.03, centred u ≈ 14 | `Toy_rust` |
| 14 | Spa | ø 2.0 m cylinder, z 10.03 → 10.45, 12 segments, water disc inset 0.10 m | shell `Toy_steel`, water `Toy_glassl` |
| 15 | Skylights | two 1.2 × 0.9 m raised curbs, z 9.83 → 10.13, u ≈ 6 and u ≈ 19 | `Toy_ink` |
| 16 | Rear elevation | one 4.0 × 3.0 m recessed glazed panel at z 0.3 → 3.3, one 1.0 × 2.1 m door | `Toy_glass`, `Toy_ink` |
| 17 | Bevel | 0.10 m, 2 segments, clamped to a third of the thinnest dimension | — |

Nothing in steps 2–16 may exceed **z 10.60**. The spa at 10.45 and the parapet at 10.10 are
sized to keep the cornice crest the unique maximum.

### 2.8 Materials and palette

Flat colours only, from the `sf-asset-check` palette except where noted.

| Material | Hex | Used for |
|---|---|---|
| `Toy_roofd` | `45454a` | the whole charcoal body — walls, south-west bay, cornice, parapet |
| `Toy_plum` | `6e3947` | **the north-east top-storey bay** — off-palette, see below |
| `Toy_steel` | `9aa0a6` | window sashes and trim, bay aprons, the dentil course, the spa shell |
| `Toy_glass` | `2a4d73` | all windows and the rear glazed wall |
| `Toy_ink` | `3a3530` | garage door, entry recess interior, stoop, skylight curbs, rear door |
| `Toy_stone` | `d9d2c2` | the flat roof membrane |
| `Toy_rust` | `a86444` | the roof terrace decking |
| `Toy_glassl` | `6f95b8` | the spa water |
| `Toy_glass_Glow` | `2a4d73` | the lit top-storey bay windows at night — **hero** |
| `Toy_glassl_Glow` | `6f95b8` | the lit spa at night |
| `Toy_gold_Glow` | `caa64a` | a warm spill in the entry recess at night |

Eleven materials. No `Toy_body` — landmarks are never tintable.

**On `Toy_plum` (off-palette).** The real colour is a deep oxblood around `#6e3947`. No
palette entry is close: `Toy_rust` (`a86444`) is far too orange, `Toy_red` (`c4453c`) far
too bright, `Toy_ink` too neutral. The style bible's San Francisco exception — painted
residential rows keep their tinted facades — sanctions a tinted deviation exactly here, and
this accent *is* recognition cue #2. Off-palette colours are a **WARN, not a FAIL**
(`sf-asset-check` §7). Justify the final choice in `REPORT.md`; if the reviewer prefers to
stay on-palette, `Toy_rust` is the fallback and the loss should be stated plainly.

**On `Toy_roofd` as a body colour.** It is the darkest neutral in the palette and it is
right for this building, but a 10 m volume in `45454a` next to a baked city of pale
procedural blocks can read as a hole rather than a house. That is why steps 4, 7 and 12 put
`Toy_steel` on every moulding and sash: the building must be *dark and legible*, not dark
and blank. If the first aerial render shows a black slab, lighten the mouldings before
lightening the body — the darkness is the identity.

**Night state (required).** Hero: the **four top-storey bay windows** lit — two on the
oxblood bay, two on the charcoal one — which is the composition that reads as "a house on
a park at night" and also picks out the bay geometry that identifies the building.
Supporting accents: the **spa**, glowing pale blue on the roof terrace, which is the only
thing on this rim that does and is visible from the app's aerial camera; and a small warm
spill in the arched entry recess, which is what tells the eye at night that the arch is a
hole. The garage, the middle storey and the roof membrane stay dark. Every glow surface is
a **single thin panel proud of an opaque parent** — never a closed shell.

### 2.9 Top surface

The app's camera looks down, so the roof is the primary elevation. It must resolve into
four things, in this order:

1. the **pale membrane rectangle**, 7.3 × 24 m, sharp against two darker neighbours and its
   own charcoal parapet;
2. the **cornice lift at the street end**, reading as a heavier dark band across the narrow
   end;
3. the **timber terrace** with the **round spa** — the only saturated warm note and the
   only circle;
4. two small skylight curbs.

If the terrace and spa are not immediately readable in the top render, the asset is not
finished. Do not add invented rooftop clutter beyond this list: the emptiness of the rest
is accurate and the neighbours' roofs supply the texture.

### 2.10 Scope

**In the GLB:** the single building — main volume on the measured footprint, two canted
bays, arched entry recess and stoop, garage door, cornice and parapet, flat roof with
terrace, spa and skylights, rear glazed wall and door.

**Not in the GLB:** 35 South Park, 45–49 South Park, the South Park oval, its lawn, paths,
benches or trees, the street tree in front, the street, the sidewalk, the rear yard and its
planting, fences, vehicles, people, plinths, cameras or lights.

### 2.11 Triangle budget

| Element | Estimate |
|---|---|
| main volume + roof membrane + parapet | 500 |
| cornice, three steps with dentil notches and returns | 1,400 |
| south-west bay (two storeys, five facets, belt cornice) | 1,100 |
| north-east bay (one storey, five facets) | 700 |
| bay windows, ~14 openings with trim and sills | 1,800 |
| arched entry recess, arch head and door | 900 |
| stoop and cheeks | 300 |
| garage door and grooves | 250 |
| roof terrace, spa, two skylights | 650 |
| rear glazed wall and door | 200 |
| glow shells | 200 |
| **Total** | **~8,000** |

Cap **8,000** — a secondary-tier building, and the cap should bind hard. The repo limit is
27,000 for a landmark, but this asset streams in alongside twenty other South Park houses
sharing one `loadRadius` centre, and the shared batch is the constraint, not the file. If
the first build lands above 8,000, the answer is fewer window subdivisions and a coarser
dentil course, not a raised cap.

### 2.12 Draft manifest entry

```json
{
  "id": "41-south-park",
  "file": "41-south-park.glb",
  "anchor": [
    -122.3934770,
    37.7815017
  ],
  "targetHeightM": 10.6,
  "cat": 1,
  "name": "41–43 South Park",
  "estimated": true,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

`dims` and `tris` are placeholders until the asset is built and validated. `cat: 1` is
House (`CATEGORY_LABELS`, `app/src/context.js`), matching the assessor's `SRES`.
`loadRadius` is the default rule, `max(2500, 10.6 × 30) = 2500`; `alwaysLoaded` would be
wrong — this is a 10 m house, not a skyline piece. `"estimated": true` because the crest
is photogrammetric (2.15).

### 2.13 Integration notes (for later, not this task)

> **Superseded — read `artifacts/41-south-park/REPORT.md` §8.2 instead.** The
> numbers below were derived with OSM standing in for Overture, because
> `pipeline/data/` is gitignored and was not on disk when this plan was written.
> Measured against the real bake input at integration time, the registry point
> moved to `-122.3934867, 37.7815158` and `exclude` to **2.8** (safe window
> 1.83–3.73 m, versus the 0.42 m window the manifest anchor gives). The
> prediction that two rings would disappear also turned out to be wrong: one
> did, because `occupiedFraction(bbox) > 0.25` blocks the Overture gap-fill on
> this lot. The method below is right; the values are not.

**Case B** — new landmark. It needs a `pipeline/lib/landmarks.mjs` entry and a tile
re-bake, or the baked procedural building will intersect the GLB.

```js
{
  id: '41SouthPark',
  name: '41-43 South Park',
  lon: -122.3934851,
  lat: 37.7815109,
  height: 10.6,
  exclude: 2.7,
  camera: { distance: 150, yaw: 225, pitch: 26 },
}
```

**The manifest anchor and the registry `lon`/`lat` differ, deliberately.** They are
independent fields: `placeGeneric` in `app/src/assets.js` positions the GLB from the
**manifest** `anchor` alone, while `pipeline/lib/landmarks.mjs` `lon`/`lat` is only the
centre of the bake-time exclusion circle.

| Field | Value | Why |
|---|---|---|
| manifest `anchor` | `-122.3934770, 37.7815017` | centroid of the design footprint — where the building actually stands |
| registry `lon`/`lat` | `-122.3934851, 37.7815109` | centroid of the **DataSF LiDAR footprint** — the point that gives the widest workable exclusion band |

They are 1.3 m apart.

**Sizing `exclude`.** `excluded()` in `pipeline/buildings.mjs` drops a footprint when its
centroid **or any ring vertex** falls inside the circle. Measured from the registry point
above, against DataSF footprints and OSM standing in for Overture:

| Polygon | Triggers at | Source |
|---|---|---|
| **this building** | **0.00 m** (its own centroid) | DataSF `201006.0038546` |
| **this building** | **2.00 m** (its centroid) | OSM `way/112759867`, as an Overture proxy |
| 45–49 South Park (front) | **3.38 m** (nearest vertex) | DataSF `201006.0014671` |
| 45–49 South Park | 8.14 m | OSM `way/71211339` |
| 35 South Park | 10.66 m | OSM `way/112759864` |
| 45–49 South Park (rear building) | 11.83 m | DataSF `201006.0108499` |
| 35 South Park | 12.67 m | DataSF `201006.0004109` |

So the radius must be **greater than 2.00 m** (to drop the Overture gap-fill version too)
and **less than 3.38 m** (to spare 45–49). **Use `exclude: 2.7`** — 0.70 m of margin on
each side, which is a comfortable window by this registry's standards (165–167's is 0.4 m
wide). Measured from the manifest anchor instead the band collapses to 3.01 → 3.20 m, only
0.19 m wide, which is exactly why the two fields differ.

**Expect exactly two rings to disappear** — the DataSF footprint and the Overture gap-fill
— not one. That is correct behaviour on a site both datasets trace, not evidence of
collateral damage. `pipeline/verify-rebake.mjs` should confirm the affected cell loses two
buildings and that 35 and 45–49 both survive.

**Verify the Overture gap-fill explicitly.** `pipeline/buildings.mjs` only calls
`markOccupied` for footprints that survive exclusion, so removing this building's DataSF
footprint leaves its bbox unoccupied and the Overture pass may re-add a wrong-shaped
building in its place; it may equally be blocked by the `occupiedFraction(bbox) > 0.25`
test. Which happens cannot be determined without
`pipeline/data/overture_buildings.geojsonseq`, so **re-measure against the real Overture
polygon at integration time**. The OSM numbers above are a proxy, not the answer.

**Do not set `clearTrees`.** At 2.7 m the radius clears no trees and no street furniture,
which is the right outcome: the street tree in front of this house is real, and South
Park's furniture sits inside the oval, outside the lot.

**Camera preset.** The building is legible only from the park side. `camera.js` puts the
eye at `target + distance × (sin yaw, ., cos yaw)` with `+x` east and `+z` south, so camera
bearing = `180 − yaw`; the 315.08° facade wants **yaw 225**, standing north-west out over
the park, square onto the two bays. 150 m suits a 10.6 m building (cf. 165–167 at 160 for
9.0 m, 160 South Park at 155 for 9.4 m, 135 South Park at 150 for 8.5 m). **Render it
before believing it** — `592Third`'s yaw was derived on paper and turned out to face two
blank party walls.

**Batch mode applies.** A Case B re-bake rewrites ~600 generated files under
`app/public/tiles/` and `api/_data/` whatever the landmark was. Run the bake, do the full
QA on it — a Case B landmark cannot be judged without its exclusion applied, because the
procedural block here is taller than the asset and would simply hide it — then
`git checkout -- app/public/tiles api/_data` and commit source only, per
`docs/asset-pipeline/ADDRESS-TO-ASSET.md`.

**Streaming check.** This makes twenty-one landmarks on one 160 m oval, the densest cluster
in the manifest. After integration run `node pipeline/landmark-streaming-check.mjs` against
a build: the procedural fallback hides loader failures from the eye and this is what
catches them.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0; XY centre offset within 0.5 m
- [ ] Bounding-box top **exactly 10.60 m**, and it is the cornice crest — not the parapet,
      not the spa (loader scale must land on 1.0)
- [ ] Oriented footprint 7.297 m × 24.0 m ± 0.05 m; bays project 0.95 m ± 0.05 m in front
- [ ] AABB ≈ 22.8 × 22.8 m (the 135.08° heading, not a scale error)
- [ ] **The mirror check**: the oxblood bay and the entry stoop are on the NORTH-EAST half,
      the garage on the SOUTH-WEST half
- [ ] The two bays are **not** the same height: south-west spans two storeys, north-east one
- [ ] The arched entry reads as a recess ≥ 0.7 m deep from all viewing angles
- [ ] Triangles ≤ 8,000; ≤ 500 KB compressed
- [ ] All materials `Toy_*`, flat, no textures, no alpha, no `Toy_body`; `Toy_plum`
      documented as a deliberate off-palette SF-exception tint
- [ ] `_Glow` only on the four top-storey bay windows, the spa and the entry recess; every
      glow surface a single thin panel proud of an opaque parent, never a closed shell
- [ ] No cameras, lights, animations, armatures, constraints, or foreign geometry
- [ ] Applied transforms, no negative scales; per-object signed-volume normals test clean;
      whole-model ray residual ≤ 0.15%
- [ ] Top view resolves into the four shapes of 2.9, in that order
- [ ] Night render shows lit bays and a lit spa on a dark building — not a glowing slab
- [ ] Six review renders + contact sheet + night render regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

1. **The crest height is photogrammetric and everything scales off it.** The 9.83 m roof
   deck is a real LiDAR measurement over 672 cells (σ 1.08 m) and for a flat roof it is
   trustworthy. The 10.60 m crest is not measured: it comes from scaling the Compass
   photograph by the surveyed 7.297 m frontage, and it depends on the camera having been
   level. The verticals in that photograph are parallel to within a pixel or two, which is
   the evidence that it was — but it is one photograph. The cross-check is the garage door,
   which the same scale puts at 3.30 × 2.00 m, a standard SF opening. **The error is
   contained**: the build normalizes the crest to exactly 10.60 and the loader scales by
   `targetHeightM / measuredHeight`, so the scale lands on 1.0 and the plan dimensions stay
   exact whatever the truth is. A wrong number here makes the building slightly tall or
   short, not wrong. Mark the manifest entry `"estimated": true` and drive the crest from a
   named constant so it is a two-minute change.
2. **The LiDAR maximum of 11.88 m is unexplained and it is 1.28 m above the modelled
   crest.** Candidates: a rear stair penthouse, a chimney, or a parapet higher than the one
   in the photograph. Two things argue for ignoring it. The survey is from **2010** and the
   building was gutted and rebuilt in 2012–13, so whatever produced that return may no
   longer exist; and the nadir imagery shows no tall structure on the roof today. But this
   is the single highest-value verification before modelling, because if a bulkhead does
   exist the target height becomes 11.88 m and the whole building rescales. **Resolve it
   from oblique aerial imagery and say what you found.**
3. **The facade reading rests on one photograph.** Every dimension in 2.4 — the bay widths,
   the storey lines, the arch head, the garage opening — is measured off the single Compass
   listing image, which is a 2013 marketing photograph partly obscured by a street tree and
   a passing dog. The bay asymmetry is unambiguous in it, and that is the important part;
   the exact widths are not. Confirm against a second source (Street View, a second listing
   set, the 2023 rental photographs) before building, and treat any disagreement as
   authoritative over this plan.
4. **Two search results are traps.** `archpaper.com`'s "Quarter-Round House" is in Ashbury
   Heights, not South Park — an Exa summariser attached this address to it; the page text
   does not. The Jerry Kler Architects "South Park Facade Restoration" fits this building's
   present appearance suspiciously well (full facade restoration, 18 windows, a new envelope
   and "an upgraded colour scheme") but never states an address, so it is **plausible and
   uncited**. If someone can confirm it, the paint scheme gains a designer and a date; until
   then it stays out of the facts table.
5. **The rear elevation is unverified.** No photograph of it was located. The "soaring glass
   wall that opens to a private backyard" is documented in text from three sources but its
   size, position and storey are all *inferred*. It faces a walled yard and is visible only
   from directly above, so the cost of being wrong is low — but say so rather than implying
   it was seen.
6. **The roof terrace's position is inferred to ±3 m.** The nadir imagery shows a dark
   rectangle with a pale circular object inside it, which reads convincingly as decking and
   a spa, roughly 12–16 m back from the street. Registration error between the parcel
   polygon and the imagery is 2–3 m on this block, and building lean adds more. The
   listings say the terrace "overlooks South Park", which argues for the front half. If
   better imagery settles it, move it; if not, keep it mid-roof and record the uncertainty.
7. **The present facade is 2012–13 work over 1911 fabric.** The massing, the bays, the arch
   and the cornice are original; the charcoal-and-oxblood scheme, the garage door and the
   window sashes are not. The model depicts the building as it stands, which is what the app
   renders — the "1911 Edwardian" framing describes its form, not its surfaces.
8. **`Toy_roofd` on a whole 10 m volume is the riskiest style call in this plan.** It is
   accurate and it is the identity, but the palette has nothing darker and a dark building
   surrounded by pale procedural blocks can read as a missing tile rather than a house. The
   mitigations are in 2.8 (pale mouldings and sashes on every edge) and they should be
   judged on the aerial render before anything else is polished. If it still reads as a hole,
   the honest fix is lighter mouldings and a lighter roof, not a lighter body.
9. **Twenty-one hand-built landmarks now ring one 160 m oval.** 165–167's plan raised the
   question of whether the rim should be a kit family rather than a series of one-offs, and
   every plan since has made the question sharper. This building is a genuinely poor
   candidate for a kit piece — the asymmetric bays and the arched entry are not parameters
   of a generic rim house — which is the argument for building it by hand. It is not an
   argument for the next one.
