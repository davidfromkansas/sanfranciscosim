# 326 Brannan Street (JAX Vineyards Wine Court) — SF-SIM asset plan

A 25-foot infill slot on the north-west side of Brannan Street, one lot southwest
of Second, holding a 1959 one-storey commercial shed at the back of the lot and,
in front of it, an outdoor **Wine Court** — the JAX Vineyards tasting garden that
replaced the lot's parking apron in 2013–14. It is the second asset in the set
that is more **site than building** (after `551-third`), and the first whose
subject is a *garden*: from Brannan the whole property is a black bottle-graphic
gate wall with an olive tree growing out from behind it.

It is also, by a wide margin, the **tightest exclusion-zone site in the registry**
— its own footprint and the 12.1 m neighbour next door literally share a
party-wall vertex, and the window of valid radii is **1.04 m wide**. Read §2.13
before integration; it is not routine.

Its neighbours on this block face — `350-brannan`, `358-brannan`, `362-brannan`,
`370-brannan`, `380-brannan`, `400-brannan` — are all masonry warehouse boxes
8–14 m tall. 326 must not come out as a seventh small box. It is a green gap in
a wall of brick and concrete, and that contrast is the asset.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/326-brannan/`. This document is the plan only: Part 1 is the runnable
task prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `326-brannan` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13, which is **not a routine case**) |
| WGS84 anchor | `-122.3928965, 37.7815080` (parcel centroid, measured) |
| Target height | **5.9 m** (shed parapet crest; LiDAR roof deck 5.66 m measured, mode 5.50 m; the 9.42 m LiDAR max is party-wall contamination — see 2.1) |
| Footprint | 7.98 m (Brannan frontage, SE) x 24.32 m deep; 194.1 m2 lot, measured (DataSF parcel 3775/012) |
| Built vs open | ~62 m2 enclosed shed at the NW rear; ~95 m2 open court in front of it |
| Triangle cap | 12,000 |
| Category | `6` (bar; sub `wine_bar`) — first use of that code in the manifest |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 326 Brannan Street GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of 326 Brannan Street in San Francisco — the
JAX Vineyards tasting room and its outdoor Wine Court — and deliver it as a
downloadable, validated GLB.

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
7. `docs/asset-plans/551-third.md` — **the closest precedent in kind.** It is the
   set's other "site, not a building" asset: a ground plate, fixed furniture, a
   canopy, and a night image that is the whole point. Read its 2.6, 2.9 and 2.15
   for how a site is composed and where sites go wrong. Do not read it for the
   look — a filling station and a wine garden share nothing visually.
8. `artifacts/380-brannan/` — the nearest neighbour already built, for the
   *method* (build/render/validate script layout, party-wall handling, the
   45-degree SoMa heading) and for what this asset must **not** look like.
9. `docs/asset-plans/326-brannan.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification. **Read its 2.15
   before you start modelling.**

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Must capture

- The **street wall**: a full-width, roughly 2.6–3.0 m charcoal vertical-board
  gate and fence running the whole 7.98 m Brannan frontage, with a solid
  double-leaf gate at the southwest end and, on the fence panels, large
  off-white **wine-bottle silhouettes** with small repeated `jax` wordmarks
- The **red/coral circular JAX disc** on the fence — the single saturated accent
  on the entire asset, and the only sign
- The **Wine Court** behind the gate: a pale concrete floor, raised planters,
  built-in lounge seating around a **fire table**, loose tables and chairs
- The **transplanted olive tree** (18 ft as planted) — silver-green, multi-stem,
  the tallest living thing on the lot and the element that reads from the aerial
- **Grape vines and climbing greenery on the court's side walls**, densest on the
  southwest side where the real ivy blankets 334 Brannan's party wall
- The dark metal-framed **canopy/pergola with translucent panels** over the
  middle of the court
- **Catenary string lights** across the court — the hero night element
- The **shed at the rear**: a small flat-roofed one-storey block in near-black
  painted concrete masonry, its court elevation dominated by a big multi-lite
  **glazed roll-up door**
- A designed top surface. **Two thirds of this asset's "roof" is open court** —
  the camera looks down, so the court plan *is* the elevation that matters most

## Research 326 Brannan Street independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- The Brannan Street (southeast) gate elevation, day and night
- The court from inside: floor, planters, seating, fire table, canopy, lighting
- The rear shed's court-facing elevation and its roof
- Aerial and roof/top views — the split between roofed shed and open court, the
  canopy's extent, and the tree canopy's spread
- Night appearance (this asset's strongest view)

Prefer owner and designer material, planning and permitting documents, geolocated
photography, and aerial/satellite imagery. Never rely on a single photograph, a
single AI-generated image, or a single unsourced 3D model. Separate verified
facts from visual inference; if sources disagree, document the disagreement and
decide.

**Four source traps are already known and resolved in Part 2 — re-check them, do
not silently re-inherit the wrong value:**

1. The **OSM way is wrong geometry.** `way/1168876044` is a Bing-style trace 13.2 m
   wide on a lot that is 7.98 m wide, and it crosses the southwest property line.
   The survey is the DataSF parcel (`acdm-wktn`, `blklot=3775012`) plus the DataSF
   LiDAR footprints (`ynuv-fyni`, `mblr=SF3775012`). Treat OSM as a cross-check only.
2. **The LiDAR maxima on this parcel are junk.** `hgt_maxcm` is 9.42 m on the shed
   and 38.74 m on the court, both from 0.5 m cells sitting on party walls with
   taller neighbours. Use the median/mode (5.66 / 5.50 m), per the Earl Warren
   rule in `docs/asset-plans/README.md`.
3. **The 2010 LiDAR predates the site's entire current identity.** In 2010 the
   front of this lot was a *parking apron*; the Wine Court was permitted in
   2013–14 and renovated in 2020. Nothing in the LiDAR describes the court, the
   canopy, the tree or the gate. Use it for the shed and the ground only.
4. **"Back garden" is wrong.** Several aggregator listings describe a *back*
   garden. The survey, the areas and the permit history all agree the court is at
   the **front**, on Brannan, and the shed is at the **rear**. Confirm this
   yourself before you lay out the site; getting it backwards mirrors the whole
   asset.

## Create a reference dossier

Write `artifacts/326-brannan/REFERENCE.md` containing: source links and what each
establishes; verified dimensions and location; orientation; observations from all
four sides and above; the 3–5 strongest recognition cues; features to preserve;
features to simplify; uncertainties and conflicting evidence. A contact sheet of
attributed reference thumbnails is welcome if legally permissible — do not commit
copyrighted full-resolution imagery.

## Make your own design decisions

The plan's massing recipe (2.7) and palette map (2.8) are a starting point, not a
specification. Judge from the high three-quarter aerial first, iterate, and record
every departure in `REPORT.md`. `REPORT.md` beats the plan, always.

Two decisions are explicitly yours and both are load-bearing:

- **What defines the bounding-box top.** The plan sets `targetHeightM` to the
  shed's 5.9 m parapet and asks you to keep the olive tree's crest just under it.
  If your research says the tree is taller than the parapet, that is fine — but
  then the tree becomes the crest, you must verify its height, and
  `targetHeightM` moves with it. An error here rescales the whole site.
- **How far the court's side walls go up.** They must stay on the property line
  and stop well below the neighbours' real heights (12.1 m southwest, 8.1 m
  northeast) so the asset never pokes through the baked blocks that will stand
  beside it. Model the court's own enclosure, not the neighbours' buildings.

The finished asset must be immediately recognizable as this address, consistent
with the real site from all four sides and above, architecturally credible, and a
premium handcrafted miniature — not photorealistic, not voxel art, not generic
low-poly, and never accurate in one view while invented in the others.

## Scope of the exported asset

Export the property: the gate and fence wall with its graphics and disc sign, the
court floor slab and its kerbs and planters, the fire table and built-in seating,
loose furniture, the canopy and its frame, the string lights, the olive tree and
the vines, the court's own side walls, and the rear shed with its roll-up door and
roof.

The court floor slab is part of the asset — it is the ground plane the whole
composition sits on, and without it the furniture floats over baked terrain. Keep
it a thin slab confined to the parcel boundary.

Do not include unrelated surrounding city geometry: Brannan Street, the sidewalk
beyond the property line, the neighbouring buildings at 318 and 334 Brannan,
street furniture, street trees, people, **vehicles**, plinths, cameras or lights.
Temporary context may appear in review renders but must not leak into the GLB.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary
`.glb`; real-world meters; origin at base center; minimum geometry Z ~ 0; applied
transforms; no negative scales; outward normals; no duplicate or foreign geometry;
no image textures; no transparency; flat-color materials named `Toy_*` from the
project palette; `_Glow` suffix only on surfaces that glow at night; no
`Toy_body`; no cameras, lights, animations, armatures or constraints; no external
dependencies; at most 12,000 triangles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model
drops into the city at its real-world heading — the loader applies no rotation
(`placeGeneric` in `app/src/assets.js` only scales and positions). The lot's long
axis runs 315.2 deg / 135.2 deg true and its Brannan frontage faces 135.2 deg (SE),
so the contract's "front faces −Y" cannot be honoured literally. Real-world
orientation wins (AGENTS rule 5). Record the decision and the measured heading in
`REPORT.md`.

**Height normalization:** make the exported bounding-box top land exactly on the
verified height, so the loader's `targetHeightM / measuredHeight` scale is 1.0.

**Normals warning specific to this asset.** A fence is a thin panel, the canopy is
a thin plate, the court floor is a thin slab and the string lights are thin
elements — this model is not a union of closed solids in the usual way. Build
every panel and plate as a real closed box, never as a zero-thickness plane, or
the per-object signed-volume normals test is meaningless and the app's
single-sided rendering will punch holes in it.

**Glow warning specific to this asset.** Per the project's night rules, a `_Glow`
surface must be a **thin shell proud of an opaque surface**, never a closed shell
wrapped around a whole object — a closed glow shell reads as two stacked alpha
layers and tints the daytime asset. The string lights in particular must be small
emissive beads on an opaque cord, not a glowing tube.

## Reproducible Blender workflow

Blender 4.5 LTS or newer, headless only: `blender -b --python script.py -- args`;
no GPU, so use Workbench or CPU Cycles.

Keep `artifacts/326-brannan/build_326_brannan.py` (deterministic build script),
`artifacts/326-brannan/326-brannan.blend`, and
`artifacts/326-brannan/326-brannan.glb`. The script must rebuild the model
reliably enough for future revision. Do not modify or rename an unrelated existing
GLB to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`326-brannan-top.png`, `326-brannan-north.png`, `326-brannan-east.png`,
`326-brannan-south.png`, `326-brannan-west.png`, plus
`326-brannan-contact-sheet.png`, at least one high three-quarter aerial beauty
render `326-brannan-aerial.png`, and a night render `326-brannan-night.png`.

The four elevations must share scale, framing, lighting, exposure and projection;
use orthographic or long-lens cameras; label directions from the researched
orientation. **The top view is a hero image for this asset, not a checkbox** — it
is the view that shows the court plan, and the court plan is the asset. Give it
the same iteration you give the aerial.

**The night render is the other hero image.** A lit garden between two dark blank
party walls is something nothing else on this block face can do.

Simple tabletop lighting, neutral warm background, minimal depth of field, and
every image must depict the same exported model.

## Validate the exported GLB

Re-import `326-brannan.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture
count, camera count, light count, animation count, applied-transform status,
negative-scale status, normal-orientation status, unexpected geometry, and
per-material contract compliance. Normals are checked two ways: per-object signed
volume (authoritative for a union of closed solids) and a deterministic
visibility-ray test (<= 0.15% residual, zero for single shells). Render at least
one review image from the re-imported asset. Write
`artifacts/326-brannan/validation.json` and `artifacts/326-brannan/REPORT.md`.

## Manifest draft

Verify the real WGS84 anchor and height yourself, then include this draft entry in
`REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "326-brannan",
  "file": "326-brannan.glb",
  "anchor": [
    -122.3928965,
    37.781508
  ],
  "targetHeightM": 5.9,
  "cat": 6,
  "name": "326 Brannan Street (JAX Vineyards)",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`,
`pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a
separate, explicitly requested job — run `docs/asset-plans/INTEGRATION-PROMPT.md`
for that, together with the integration notes in `docs/asset-plans/326-brannan.md`,
**whose exclusion zone has the narrowest valid window of any landmark in the set.**
````

---

## Part 2 — Research and design dossier

Research compiled 16 August 2026. Everything marked *measured* was computed from a
primary geometry source (DataSF parcels, DataSF LiDAR footprints, OSM API) and
reprojected into the app's local tangent frame. Everything else is labelled
*observed*, *inferred* or *estimated*, and the soft parts are collected again in
2.15.

### 2.1 Verified facts

| Item | Value | Confidence |
|---|---|---|
| Address | 326 Brannan Street, San Francisco CA 94107 | measured (DataSF `ramy-di5m`) |
| Parcel | Block 3775, Lot 012 (APN 3775012), `mblr` SF3775012 | measured |
| Zoning | CMUO — Central SoMa Mixed Use Office (assessor roll still carries the older SSO) | source |
| Year built | **1959** | assessor roll (`wv5m-vpq2`, 19 roll-years, all agree) |
| Storeys | **1** | assessor roll + all six building permits |
| Assessor class | C — Commercial Stores; use code COMR — Commercial Retail | assessor roll |
| Assessed building area | 1,007 sq ft (93.6 m2) | assessor roll |
| Lot area | 2,099 sq ft (195.0 m2) assessor / 194.1 m2 surveyed | measured, agrees to 0.5% |
| Architect | none recorded for the 1959 shell | absence of evidence |
| Landscape design (Wine Court) | **Terra Ferma Landscapes**, GC TFL Construction | source (designer's own project page) |
| Shed roof deck | **5.66 m** above grade (LiDAR median; mode 5.50 m, min 5.25 m, sd 0.91 m over 252 cells) | measured |
| Shed parapet crest | **~5.9 m** | inferred (deck + 0.25 m) |
| Court ground | open, LiDAR mode 0.14 m over 384 cells | measured |
| Ground elevation | 11.55–11.91 m NAVD88 across the lot (range 0.36 m) | measured — the app's terrain owns this, not the asset |
| Occupant | JAX Vineyards SF tasting room; location opened 2015-03-16, renovated 2020 | source |

**The height trap, in full.** The DataSF LiDAR record for the shed
(`sf16_bldgid 201006.0157667`) reports `hgt_mincm` 525, `hgt_majoritycm` 550,
`hgt_mediancm` 566, `hgt_stdcm` 91 — and `hgt_maxcm` **942**. That maximum is
3.9 sigma above the mode on a 62 m2 polygon whose party wall is shared with a
12.1 m building. It is the Earl Warren case in `docs/asset-plans/README.md`
exactly: *a single-cell `hgt_max` on a party wall is unusable*. The shed is a
flat-roofed one-storey box at 5.5–5.7 m, full stop.

The court polygon (`201006.0135574`) is worse and in the opposite direction: mode
**0.14 m**, median 2.93 m, sd 7.19 m, max **38.74 m** on a 95 m2 sliver flanked by
two tall walls. Nothing about that record describes a structure. It is open ground
with edge contamination, which is exactly what the 2013 permit says it was in
2010 — *"existing parking lot"*.

### 2.2 Sources

| Source | Establishes |
|---|---|
| DataSF Parcels `acdm-wktn`, `blklot=3775012` | **authoritative lot geometry**: 7.98 x 24.32 m, 194.1 m2, corner coordinates, zoning, centroid |
| DataSF Building Footprints `ynuv-fyni`, `mblr=SF3775012` | **authoritative built geometry and heights**: two polygons — shed 61.6 m2 at 5.66 m, court 95.2 m2 at ground; also the neighbour rings used in 2.13 |
| DataSF Addresses `ramy-di5m`, `326 BRANNAN ST` | address to APN resolution; point 37.781508 / −122.392896 |
| DataSF Assessor Secured Roll `wv5m-vpq2`, block 3775 lot 012 | 1959, 1 storey, class C, COMR, 1,007 sq ft building on 2,099 sq ft lot |
| DataSF Building Permits `i98e-djp9`, block 3775 lot 012 (6 permits, 1997–2014) | the whole site history — see below |
| [OSM way/1168876044](https://www.openstreetmap.org/way/1168876044) | address, `building=yes`, `shop=wine`, `name=JAX Tasting Room` — **geometry rejected**, see 2.3 |
| Google Street View, Brannan Street pano, capture May 2025 | the gate elevation: charcoal vertical boards, bottle graphics, `jax` wordmarks, red disc, solid gate leaf at the SW end, foliage and canopy over the fence, ivy on 334's party wall |
| Google Maps satellite (Vexcel, 2026) | the site plan from above: pale rear shed roof, canopy and tree canopies mid-lot, gate at the sidewalk, the slot between two larger neighbours |
| jaxvineyards.com, SF tasting room page (hero image) | the shed interior and its court elevation: black-painted CMU, multi-lite glazed roll-up door, polished concrete, black bar |
| Terra Ferma Landscapes project page (`tflandscapes.com/jax-vineyards`, photo credit Jason Liske) | the court's design program: ~1,000 sq ft, fire table with built-in lounge seating, **mature olive trees**, grape vines, raised planters, dramatic evening lighting, vine-covered walls |
| Eventective / VenueKonnex venue listings | **600 sq ft indoor + 900 sq ft outdoor**, 100 standing / 60 seated, **18-foot olive tree**, built-in fire pit, projector, covered patio for winter, "year of renovation 2020" |
| Yelp photo `DXAKbTAMZk7HZKKOEvN8vA` (court at night) | the night image: warm catenary string lights, candle and fire glow, red heat lamps, the neighbours' brick reading dark behind |
| CA ABC licences 00535821 / 00624057; SF business registry `1024047-03-151` | occupancy dates and that the premise is licensed to pour on site |

**Permit history**, which is the spine of this site's story:

| Filed | Permit | What it says |
|---|---|---|
| 1997-09-09 | 9717507 | reroofing; existing use *office* |
| 2013-09-04 | 201309045959 | *"change use of outdoor space from existing parking lot to a wine tasting area/retail sales. **existing building not to be open to the public and not to be modified**"* — use `parking lot` → `parking lot` |
| 2013-12-10 | 201312103834 | *"retail sales. new restrooms, change door swing, interior non structural alterations. change of use"* — `manufacturing` → `retail sales` |
| 2014-01-30 | 201401307463 | outdoor space `parking` → tasting/retail again; ADA bathroom; **gas line extension** (the fire table) |
| 2014-06-02 | 201406027264 | *"to erect **front gate sign**. non electric, single faced"* |
| 2014-08-11 | 201408113522 | accessible restroom work; construction type recorded as **wood frame (5)** where earlier records say type 1 |

Read in order these say: a 1959 shed used for manufacturing then office, with a
parking apron on Brannan; the apron becomes the tasting garden first (Sept 2013,
explicitly *without* opening the building), the building follows three months
later, the gas line for the fire table and the front gate sign arrive in 2014,
and the whole thing is renovated in 2020.

### 2.3 Orientation and placement

**Anchor (measured):** `-122.3928965, 37.7815080` — the DataSF parcel centroid.
In the app's local frame (`x=(lon+122.4375)·111320·cos 37.77`, `z=−(lat−37.77)·110540`)
that is `x = 3924.92, z = −1272.09`, which lands in streaming cell **23_13**
(500 m grid, origin −8000/−8000).

**The lot (measured), as a closed ring in local metres:**

| Corner | x | z | |
|---|---|---|---|
| A | 3936.32 | −1266.28 | east corner, on Brannan |
| B | 3930.66 | −1260.65 | north corner, on Brannan |
| C | 3913.51 | −1277.89 | west corner, at the rear |
| D | 3919.18 | −1283.52 | south corner, at the rear |

| Edge | Length | Outward | Elevation |
|---|---|---|---|
| A–B | **7.98 m** | SE 135.2 deg | **Brannan Street front** |
| B–C | 24.32 m | NE 45.2 deg | northeast party line (318 Brannan / KCA Engineers) |
| C–D | 7.98 m | NW 315.2 deg | rear property line |
| D–A | 24.32 m | SW 225.2 deg | southwest party line (334 Brannan) |

The whole lot sits at the SoMa grid's 45 degrees, like every other asset on this
block face. The axis-aligned XY bounding box of a 7.98 x 24.32 m site rotated
45 degrees is about **22.8 x 22.8 m** — that is correct, not a scale error, and it
is the same effect documented in `artifacts/380-brannan/REFERENCE.md` §4.

**Which end is the street** was checked rather than assumed, because the answer
mirrors the entire asset. The DataSF Brannan Street centreline (`3psu-pn9h`) runs
through `(3997, −1309) → (3950, −1263) → (3899, −1212)` in local metres. Measured
perpendicular from that line:

- A–B midpoint `(3933.49, −1263.47)` → **12.0 m** from the centreline
- C–D midpoint `(3916.35, −1280.71)` → 36.3 m

12.0 m is a Brannan half-right-of-way. **A–B is the street frontage**, and it is
the *court* that fronts Brannan while the *shed* stands at the back.

**The split, measured.** Both DataSF footprints lie inside the lot:

| Polygon | Where | Size | Area | LiDAR height |
|---|---|---|---|---|
| `201006.0157667` | rear (NW) half | 9.05 x 6.88 m | 61.6 m2 | 5.66 m median, 5.50 m mode |
| `201006.0135574` | front (SE) half | 13.40 x 6.88 m | 95.2 m2 | 0.14 m mode — open ground |

Those areas are the independent confirmation that the listing numbers describe
this lot and not some other: **600 sq ft = 55.7 m2** indoor against a 61.6 m2
survey polygon, and **900–1,000 sq ft = 84–93 m2** outdoor against 95.2 m2. Both
agree within the width of a wall.

**Why the OSM way is rejected.** `way/1168876044` carries the right address and
the right occupant name and the wrong shape: 104.8 m2, minimum-area box
**13.18 x 7.98 m**, long axis running *along* Brannan. The lot is 7.98 m wide and
24.32 m deep, so OSM has the building's proportions rotated 90 degrees, and its
ring crosses the southwest property line by up to 2.1 m. This is the
`358-brannan` failure repeated — a Bing trace on a narrow SoMa lot — and the
README's standing rule applies: *where a plan cites a DataSF `mblr`/`sf16_bldgid`
footprint, that is the survey; OSM geometry on small SoMa lots is a cross-check
only.*

### 2.4 What each side shows

**Southeast — Brannan Street front.** The only public elevation, and it is not a
building at all. A charcoal, almost-black **vertical-board fence and gate** spans
the full 7.98 m frontage at roughly 2.6–3.0 m (*estimated from Street View
against the parked-car and parking-meter datums beside it*). The southwest third
is a solid double-leaf gate with a slim vertical pull; the remaining panels carry
five or six **large off-white wine-bottle silhouettes**, each with a small `jax`
wordmark, and one **red/coral filled circle** with the `jax` mark reversed out of
it. Above the fence line: dense foliage, the dark edge of the court canopy, and
one red heat lamp. Nothing of the shed is visible from the street.

**Northeast — 318 Brannan party line.** A blind boundary. The neighbour (KCA
Engineers / Zephyr Real Estate, a 2-storey white stucco block, LiDAR 8.11 m) has
its own blank wall on or near this line, so the asset's own northeast court wall
is a low painted enclosure carrying planters and vines, not a facade.

**Southwest — 334 Brannan party line.** The same in principle and much more
important visually: 334 Brannan is a 3-storey sage-green and tan building
(LiDAR 12.14 m) whose flank wall is **blanketed in climbing ivy for its lower two
thirds** where it faces the court. That green wall is the court's backdrop in
every photograph of the site. It belongs to the neighbour and must not be modelled
as part of this asset — but the asset's own southwest court wall should carry the
densest vine mass, so the reading survives even before the baked neighbour loads.

**Northwest — rear.** The shed's back wall against the rear property line, and the
one elevation with no research at all (see 2.15).

**From above.** The single most informative view, and the one the app actually
uses. In order from Brannan: gate wall; open court floor with raised planters down
both sides; the olive tree canopy roughly a third of the way in, spreading wider
than the 6.9 m court is broad; the fire table and its seating ring; a dark
metal-framed canopy over the middle; then the shed's pale flat roof filling the
rear 9 m of the lot.

### 2.5 Recognition cues (ranked)

1. **The black bottle-graphic gate wall.** It is the whole street elevation and it
   is unmistakable. Get the bottles and the red disc right and the asset is
   identified from the sidewalk camera.
2. **A green slot in a masonry wall.** Seen from the aerial, this lot is the only
   opening in 200 m of 8–14 m warehouse boxes, and it is full of plants. That
   contrast is the asset's reason to exist.
3. **The olive tree.** Silver-green, multi-stem, wider than the court — the one
   living silhouette on the block face.
4. **The string lights at night.** A lit garden between two dark blank party
   walls; nothing else here does this.
5. **The black CMU shed with its big glazed roll-up door** at the back of the
   court — small, deliberately secondary, but it is what makes the court a
   *room* rather than a vacant lot.

### 2.6 Miniature translation

This is a **site asset**, and the second in the set after `551-third`. The rules
that make a site work are different from the rules that make a building work:

- **The ground plane is a first-class object.** A thin court slab, confined to the
  property line, in a pale warm concrete that sits *near* the baked street tone
  but not identical to it. If the slab colour drifts, the lot reads as a hole in
  the city; if it matches exactly, the court disappears.
- **Composition happens in plan, not in elevation.** Everything the viewer will
  actually see is arranged on 13 x 7 m of floor. Lay it out as a plan first,
  render the top view, and judge that before building anything vertical.
- **Semantic exaggeration goes to the tree and the graphics.** The style bible's
  exaggeration budget is best spent making the olive read as an *olive* (pale
  silver-green, open irregular multi-stem crown, not a lollipop) and making the
  bottle silhouettes big enough to survive at the block-scale zoom. It is not
  spent on making the shed taller.
- **Restraint everywhere else.** One saturated accent — the red disc. The fire
  glow at night is the second. Everything else is charcoal, concrete, terracotta
  and green.
- **Resist the urge to fill it.** A hundred people fit in this court at a party
  and none of them belong in the GLB. A handful of tables, one seating ring, two
  or three planter groups. Small clusters of life, per the style bible, not a
  crowd.

The failure mode to avoid: this becoming a seventh grey box with a shrub on it. If
the top render does not read as *a garden*, it is wrong regardless of what the
elevations say.

### 2.7 Massing recipe

Author in true-world orientation; all dimensions in metres, all positions relative
to the parcel centroid anchor.

1. **Court slab.** A 7.6 x 24.0 m thin plate (0.15 m), inset ~0.15 m inside the
   property line, top at 0.0. Split it visually: a smoother pale apron over the
   front 14 m and a slightly darker threshold band at the shed door.
2. **Court side walls.** Two closed boxes 0.25 m thick along the northeast and
   southwest property lines, 3.2 m tall, running from the gate to the shed. These
   are the court's enclosure, not the neighbours' buildings — keep them at 3.2 m
   so they can never intersect the baked 8.1 m and 12.1 m blocks beside them.
3. **Gate wall.** A 7.98 x 0.20 m closed panel at the A–B edge, 2.8 m tall, with a
   0.10 m cap rail. Sub-divide the face into a solid gate leaf (2.4 m wide, at the
   southwest end) and four fence panels. Bottle silhouettes and the red disc are
   *inset geometry*, 0.02 m proud — flat colour, no textures.
4. **Rear shed.** A closed box filling the rear 9.05 x 6.88 m of the lot, walls to
   5.66 m, plus a 0.24 m parapet ring to the 5.9 m crest. On the court elevation,
   a recessed 4.2 x 3.4 m opening holding a multi-lite roll-up door (a 4 x 3 grid
   of glazed panes in a slim dark frame). A shallow flat roof with two small
   mechanical boxes and a roof hatch — the camera looks down, and a blank plate
   here wastes the one built roof the asset has.
5. **Canopy.** A 6.6 x 5.0 m thin plate at 3.6 m over the middle of the court, on
   four slim posts, with a 0.12 m perimeter fascia. Build the plate as a closed
   box. Keep it clearly below the shed parapet so it never competes for the crest.
6. **Olive tree.** Planted in a raised 1.8 m square planter at +0.45 m, roughly
   9 m in from the gate, offset to the northeast side of the court. Multi-stem
   trunk, open irregular crown ~5.0 m across, crest at **5.8 m** — deliberately
   0.1 m under the parapet, so the parapet defines the bounding box. Silver-green,
   two tones.
7. **Vines and planters.** A dense vine mass on the southwest wall covering its
   upper two thirds, a lighter one on the northeast. Three raised planters per
   side, terracotta or board-formed concrete, 0.5 m tall, with low mounded
   planting. Two vertical vine columns on the gate's inner face.
8. **Fire table and seating.** A 1.4 x 0.8 m low table at 0.42 m, centred about
   5 m in from the gate, ringed on two sides by a built-in bench 0.45 m high and
   0.6 m deep. Three or four loose tables with two chairs each, spread down the
   court.
9. **String lights.** Two catenaries spanning the court between the side walls,
   sagging to about 2.6 m at mid-span, with small beads at ~0.8 m spacing. An
   opaque cord with separate emissive beads — never a glowing tube.

Total vertical stack: crest 5.9 m (shed parapet) > 5.8 m (olive crest) > 3.6 m
(canopy) > 3.2 m (court walls) > 2.8 m (gate) > 0.0 (slab).

### 2.8 Materials and palette

| Material | Where | Note |
|---|---|---|
| `Toy_charcoal` | gate and fence boards, shed CMU walls, canopy fascia | warm near-black, never pure black |
| `Toy_ink` | canopy frame, posts, door frame, furniture, railings | the darkest tone, used sparingly |
| `Toy_cream` | bottle silhouettes and `jax` wordmarks on the gate | flat, high contrast against the charcoal |
| `Toy_coral` | the JAX disc — **the only saturated accent on the asset** | one object |
| `Toy_stone` | court slab, kerbs | pale warm concrete, near but not equal to the baked street tone |
| `Toy_plaster` | court side walls | a shade warmer than the slab so the enclosure reads |
| `Toy_terra` | raised planters | muted terracotta |
| `Toy_olive` | olive foliage | **pale silver-green** — must not match the ivy |
| `Toy_vine` | wall vines, ground planting | a fresher, deeper green |
| `Toy_bark` | trunk and stems | grey-brown |
| `Toy_glass` | roll-up door panes, day state | dark blue-grey graphical windows per the style bible |
| `Toy_roofd` | shed roof deck, mechanical boxes | mid grey |
| `Toy_glass_Glow` | roll-up door panes at night | thin shell proud of the opaque pane |
| `Toy_bulb_Glow` | string-light beads | small separate beads on an opaque cord |
| `Toy_fire_Glow` | fire table burner face | one small warm-orange disc |
| `Toy_coral_Glow` | the JAX disc face at night | thin shell proud of `Toy_coral` |

**Night composition.** One hero — the string lights — plus three supporting
accents: the fire table, the roll-up door, the disc. Four glow groups total. The
court walls, the tree and the planters stay dark; a garden at night is lit *points*
in *darkness*, and lighting the whole court would throw away the effect. Every
glow surface is a thin shell, per the warning in Part 1.

### 2.9 Top surface

Unusually for this set, the top surface is mostly not roof. From above the asset
is: gate cap rail (7.98 m of it), then 14 m of open court reading as slab,
planters, furniture, canopy plate and tree crown, then 9 m of shed roof.

Design implications:

- The **court plan carries the aerial view**. Vary it: the planters should not be
  a symmetric double row, the furniture should not be on a grid, and the tree
  should sit off-centre.
- The **canopy plate is a large flat rectangle seen from directly above** and will
  dominate if it is too big or too pale. Keep it at 6.6 x 5.0 m and dark.
- The **tree crown overhangs the canopy and the walls** — that overlap is what
  makes the lot read as green from altitude, so let it spread past the court
  edges rather than trimming it to the property line. It must still stay inside
  the asset's bounding box.
- The **shed roof gets real objects** — two mechanical boxes and a hatch — for the
  same reason every other roof in this set does.

### 2.10 Scope

**In:** gate and fence with graphics, court slab and kerbs, court side walls,
planters and planting, vines, olive tree, fire table, built-in seating, loose
furniture, canopy and posts, string lights, rear shed with roll-up door, shed roof
and its equipment.

**Out:** Brannan Street, sidewalk, kerb, parking meters, the buildings at 318 and
334 Brannan (including 334's ivy — the asset carries its *own* vine mass on its
*own* wall), street trees, people, vehicles, wine bottles and glassware, signage
belonging to neighbours, plinths, cameras, lights.

### 2.11 Triangle budget

| Group | Estimate |
|---|---|
| Court slab, kerbs, threshold | 300 |
| Court side walls | 400 |
| Gate wall, panels, graphics, disc | 900 |
| Rear shed shell, parapet, roof, equipment | 900 |
| Roll-up door and its 12-pane grid | 700 |
| Canopy plate, fascia, four posts | 500 |
| Olive tree (multi-stem + crown) | 3,200 |
| Vine masses (two walls + two columns) | 2,200 |
| Planters and mounded planting | 1,400 |
| Fire table, built-in seating | 500 |
| Loose furniture (4 tables, 8 chairs) | 800 |
| String lights (cords + ~40 beads) | 600 |
| **Total** | **~12,400** |

That is 400 over. The two places to take it from are the vine masses (which can be
simplified to fewer, larger clumps without losing the reading) and the chair
count. **Cap 12,000.** Both the tree and the vines are the expensive items and
both are load-bearing for identity — trim geometry elsewhere before trimming
those.

### 2.12 Draft manifest entry

```json
{
  "id": "326-brannan",
  "file": "326-brannan.glb",
  "anchor": [-122.3928965, 37.781508],
  "targetHeightM": 5.9,
  "cat": 6,
  "name": "326 Brannan Street (JAX Vineyards)",
  "estimated": false,
  "dims": [22.8, 22.8, 5.9],
  "tris": 0,
  "loadRadius": 2500
}
```

`cat 6` is `bar` in `pipeline/taxonomy.mjs` (sub `wine_bar`), whose `NIGHT_PROFILE`
is 1 — commercial. **This is the first manifest entry to use category 6**; check
after integration that nothing downstream assumed the category set in use was
sparse.

`loadRadius` follows the default rule `max(2500, targetHeightM x 30)` =
`max(2500, 177)` = **2500**, and this asset is emphatically not `alwaysLoaded`.

### 2.13 Integration notes (for later, not this task)

**New landmark**, and the exclusion zone here is the tightest in the registry.
Read this before running `INTEGRATION-PROMPT.md`.

`excluded()` in `pipeline/buildings.mjs` drops a baked footprint when its ring
centroid **or any ring vertex** falls inside a landmark's exclusion circle. Both
of this lot's DataSF footprints must go — the 5.66 m shed block would z-fight the
modelled shed, and the court block would stand *inside* the modelled garden.
Measured from the parcel-centroid anchor against the DataSF footprints:

| Footprint | Ring centroid | Nearest vertex | Closest |
|---|---|---|---|
| Own court `201006.0135574` (95.2 m2) | 5.84 m | 3.54 m | **3.54 m** |
| Own shed `201006.0157667` (61.6 m2) | 6.86 m | 3.54 m | **3.54 m** |
| **Neighbour 334 Brannan `201006.0007711`** (462.5 m2, 12.14 m tall) | 12.25 m | **4.58 m** | **4.58 m** |
| Neighbour 318 Brannan `201006.0008516` (428.8 m2, 8.11 m) | 14.00 m | 12.22 m | 12.22 m |

So the valid window is **(3.54 m, 4.58 m)** — **1.04 m wide**. Ship
**`exclude: 4`**, its midpoint (4.06 m), with 0.46 m of margin at each end.

Two things make this worse than the numbers alone suggest:

- **The binding vertex is physically shared.** The point at local
  `(3920.45, −1271.10)` is a vertex of 334 Brannan's ring *and* of both of 326's
  rings — it is the party-wall corner, and the DataSF traces agree on it exactly.
  This is the `sf3d-exclusion-unavoidable-collateral` situation; it is survivable
  here only because 326's own polygons happen to have a *closer* vertex (3.54 m)
  further down the shared boundary. There is no margin to be won by re-tracing.
- **Moving the anchor is not available.** A numeric search over anchor offsets
  finds a 6.88 m-wide window at `(+1.75, −4.25)` local — 4.60 m from the parcel
  centroid. Displacing the asset 4.6 m on a 24 m lot to buy exclusion margin is
  exactly what AGENTS rule 5 forbids. The same conclusion `551-third` reached.

**Before integrating, re-run this table against the pipeline's own cleaned rings**,
not the raw DataSF geometry. The `550-third` integration found that the
pipeline's 0.6 m ring simplification and its `ringCentroid` moved the numbers
enough to change the answer. With a 1.04 m window, a 0.6 m simplification
tolerance is the same order as the margin. Specifically check:

1. That both SF3775012 rings still fall inside 4 m after simplification.
2. That 334 Brannan's simplified ring does **not**. If it does, 4 m is unshippable
   and the fallback order is: try 3.9, then 4.2; if neither separates them,
   **stop and report** rather than shipping a radius that deletes a 462 m2,
   12.1 m neighbour and opens a hole in the block face.
3. The **Overture / OSM gap-fill twins**. The bake also carries non-DataSF rings.
   OSM `way/1168876044` measures centroid 7.56 m, nearest vertex 3.24 m from this
   anchor, so 4 m catches it — but 334's Overture ring has not been measured and
   is the one that could bite.

Other notes:

- Manifest id `326-brannan` maps to registry id `326Brannan`.
- Registry height `5.9`, matching `targetHeightM`.
- No camera preset key. At 5.9 m this is texture in the block, not a destination.
- The lot is flat made ground (LiDAR ground range 0.36 m over 24 m), so terrain
  seating should be uneventful — but the court slab is a 7.6 x 24 m plate, and a
  plate shows terrain error a small building would hide. The loader seats a
  ground-plane asset from **one** elevation sample (see the `64-south-park`
  experience), so check the seating at all four lot corners, not just the anchor.
- Batch mode applies: this is a Case B landmark, so the re-bake must be run for QA
  and then thrown away before committing, per
  `docs/asset-pipeline/ADDRESS-TO-ASSET.md`.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] bbox top exactly 5.9 m so the loader's scale factor is 1.0
- [ ] Site geometry confined to the 7.98 x 24.32 m parcel (tree crown overhang is
      the one allowed exception and must be stated in `REPORT.md`)
- [ ] Court side walls at or below 3.2 m — they must never reach the neighbours'
      8.1 m and 12.1 m baked blocks
- [ ] Triangles at or under 12,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the string-light beads, the fire table burner face, the
      roll-up door panes and the JAX disc — every one a thin shell proud of an
      opaque surface, no closed glow shells
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (per-object signed
      volume + deterministic ray test); every panel and plate a closed box, no
      zero-thickness planes
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] No people, no vehicles, no glassware, no neighbour geometry in the export
- [ ] Six review renders + night render + contact sheet regenerated from the final
      export; top view and night render iterated as hero images
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

- **The exclusion window is 1.04 m wide and the binding vertex is shared with the
  neighbour.** This is the single largest risk in the plan and it lands at
  integration, not at modelling. Do not start integration assuming it is routine;
  read 2.13 in full and re-measure against the pipeline's cleaned rings first.
- **The gate height is estimated, and it is the asset's whole street elevation.**
  2.6–3.0 m comes from reading the May 2025 Street View pano against the parked
  cars and the parking meters beside it, not from a measurement. It does not
  affect `targetHeightM` (the shed parapet does), so an error here is a
  proportion error rather than a scale error — but it is the most-seen surface on
  the model. Verify it if any better source exists.
- **The parapet crest is inferred.** 5.66 m to the roof deck is measured and tight
  (252 LiDAR cells, sd 0.91 m, mode 5.50 m). The 0.25 m parapet on top of it is a
  typological assumption for a 1959 flat-roofed commercial shed, not an
  observation, and the shed's roof edge has not been seen in any photograph. If
  nothing above the deck can be confirmed, set the crest to 5.66 m, move the olive
  crest under it, and say so in `REPORT.md`.
- **The olive tree's height is a marketing number.** "18 foot olive tree" (5.49 m)
  comes from venue listings, repeated across several of them, and is
  characteristic of copy written once and syndicated. It is also from around 2015
  — a transplanted mature olive planted eleven years ago will have grown. The plan
  sets the crest at 5.8 m *by design*, to sit just under the parapet, rather than
  by measurement. If research shows the tree clearly overtopping the shed, the
  tree becomes the crest and `targetHeightM` moves with it.
- **The canopy is the least-verified built element.** Street View shows a dark
  metal-framed structure with translucent panels over the middle of the court, and
  the listings mention a cover that can be deployed in winter. Whether it is fixed
  or retractable, and how far it extends, is *inferred* from one oblique view
  partly screened by foliage. Its 6.6 x 5.0 m plate is a large flat rectangle in
  the top render, so getting it wrong is visible.
- **The rear (northwest) elevation has no research at all.** Nothing published
  looks at the back of this lot, and no public vantage exists. It is a blind wall
  in the model by inference from the site plan. This is the same gap `350-brannan`
  had on Varney Place and it is called out here for the same reason.
- **The 2010 LiDAR describes a site that no longer exists.** In 2010 the front of
  the lot was a parking apron. Every element that gives this asset its identity —
  court, tree, canopy, gate, planting — post-dates the survey by three to ten
  years. Use LiDAR for the shed and the ground; use nothing else from it.
- **Two records disagree about the shed's construction type**: the 2013–14 permits
  say "constr type 1" (fire-resistive) while the August 2014 permit says "wood
  frame (5)", and the tasting-room photographs show painted **concrete masonry**
  inside. The model follows the photographs. The disagreement does not change any
  dimension, but it is on the record.
- **Aggregator listings describe a "back garden."** They are wrong — the survey,
  the areas and the permits all put the court at the front — but they are the
  first thing a search returns, and a modeller who reads them casually will build
  the site backwards. This is the plan's most likely research failure.
- **This is the second site-not-a-building asset and the first garden.** The style
  risk is that it lands as a grey box with a shrub. Judge the top render and the
  aerial before anything else; if the lot does not read as green from altitude,
  the asset has failed even if every dimension is right.
