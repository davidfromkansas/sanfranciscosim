# 160 South Park — SF-SIM asset plan

A 1924 two-storey commercial-front building on the north-west rim of South Park, the oval
that is San Francisco's oldest planned residential square. It sits on a 6.17 m frontage
between two dark-painted neighbours and would be invisible except for one thing: a large
**round-arched, multi-pane window** centred on its upper storey under a **projecting
red barrel-tile eave**. Everything else on the building — walls, pilasters, mullions,
shopfront — is painted a single flat slate charcoal.

It is the second plan in this set for the **South Park rim** and the first for the
*Mediterranean-revival storefront-and-flat* type. Where 165–167 South Park is a sliver
defined by its proportion and one blue gate, this one is a sliver defined by a single
piece of geometry: the arch. The design brief is "the smallest building on the block that
you can still name from the air", not "landmark" and not "generic block".

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/160-south-park/`. This document is the plan only: Part 1 is the runnable task
prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `160-south-park` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor (manifest, placement) | `-122.3948669, 37.7812686` |
| WGS84 anchor (registry, exclusion only) | `-122.3949116, 37.7812949` — **deliberately different, see 2.13** |
| Target height | **9.4 m** to the tile eave crest (LiDAR maximum, measured); roof deck 8.8 m (LiDAR mode, measured) |
| Footprint | 6.17 m frontage, 6.08 m rear, ~26.5 m built depth on a 36.4 m lot; 166.4 m², derived from the surveyed parcel |
| Axis | front block 280.4°/284.0°, rear block 315.1°; front facade faces **108.1°** |
| Triangle cap | 7,000 |
| Category | `3` (office) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 160 South Park GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of the two-storey building at 160 South Park,
San Francisco, and deliver it as a downloadable, validated GLB.

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
7. `artifacts/165-south-park/` — the closest reference implementation in scale, budget and
   site: the other narrow party-wall building on the same oval
8. `docs/asset-plans/160-south-park.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Must capture

- **The arched window.** A large round-headed, multi-pane window centred on the upper
  storey, under a moulded archivolt, flanked by two smaller rectangular multi-pane
  windows. It is the only arch on this side of the oval and it is the entire reason this
  building is worth building. A modeller who squares it off has failed.
- **The red barrel-tile eave.** A shallow tiled pent roof projecting over the full width of
  the street facade at the top, sloping down toward the park. It is the one warm colour on
  an otherwise monochrome building and the only thing about the building that is legible
  from directly overhead. Do not flatten it into a parapet.
- **The monochrome.** Walls, pilasters, window mullions, belt course and shopfront are all
  one flat dark slate charcoal. The building is not a painted-lady; its interest is entirely
  in relief and in two accents (tile, door).
- **The narrowness.** 6.17 m of frontage against ~26.5 m of built depth. From the app's
  camera this proportion is the silhouette.
- **The ground-floor shopfront** — a wide recessed dark storefront window, a flush warm-wood
  door beside it, and a proud lintel band with two square tie-plates across the whole width.
- A **flat roof** behind the tile eave — no gable, no hip, no dormer.

## Research 160 South Park independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the built depth, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- The east-south-east (street) elevation, the only elevation the public ever sees
- The roof from above — the tile eave's projection and slope, the flat deck behind it, and
  any stack, vent, skylight or stair bulkhead. This is *inferred* in this dossier and is
  the weakest part of it.
- The rear (north-west) elevation and the rear yard, visible only from the air
- The two party-wall flanks, which are blind
- Day and night appearance
- The pane count and rhythm of all three upper windows and of the shopfront — the
  dossier's reading comes from one Street View capture and must be confirmed
- Whether the building is two full storeys over its whole depth or steps down at the rear

Prefer DataSF datasets, SF Planning records, assessor data, geolocated photography and
aerial imagery. Never rely on a single photograph, a single AI-generated image, or a
single unsourced 3D model. Separate verified facts from visual inference; if sources
disagree, document the disagreement and decide.

**Four source problems are already known and resolved in 2.1–2.3 and 2.15 — re-check them,
do not silently re-inherit the wrong value:**

1. **No OSM way carries the address 160.** The OSM traces on this block are coarse Bing
   traces whose house numbers do not line up with the surveyed parcels: `way/124884344`
   is tagged `158` (an address that does not exist in DataSF) and is a 76 m² stub;
   `way/124884357` is tagged `164` and is 468 m², spanning three lots. **Do not use OSM
   geometry for this building.** The footprint in 2.3 comes from the surveyed DataSF
   parcel `3775067`.
2. **The DataSF LiDAR "building footprint" for this lot is lot-shaped, not roof-shaped.**
   `mblr=SF3775067` is 220.0 m² against a 216.8 m² parcel — it covers the rear yard as
   well as the building, which is why its height minimum is 0.56 m and its height standard
   deviation is 2.56 m where every neighbour on the block is between 0.75 and 1.14 m. Use
   its *height statistics* (2.1) and its *centroid* (2.13); do not use its outline as the
   built footprint.
3. **The median height is therefore not the roof.** `hgt_median` 7.79 m is a blend of roof
   and yard. The roof deck is the **mode**, `hgt_majority` = 8.81 m, and the crest is
   `hgt_max` = 9.41 m. Do not build to 7.79 m.
4. **The building next door at 164 is a construction site.** Stanley Saitowitz | Natoma
   Architects filed a 2024 permit there for "a new front for an historically significant
   building" in large red-brick panels. In photographs from the south you will see a
   maroon hoarding and graffiti where 164 should be; none of it belongs to 160.

## Create a reference dossier

Write `artifacts/160-south-park/REFERENCE.md` containing: source links and what each
establishes; verified dimensions and location; orientation; observations from all
four sides and above; the 3–5 strongest recognition cues; features to preserve;
features to simplify; uncertainties and conflicting evidence. A contact sheet of
attributed reference thumbnails is welcome if legally permissible — do not commit
copyrighted full-resolution imagery.

## Make your own design decisions

Follow the conversion process in `docs/styles/miniature-toy.md` §22: identify the
recognition cues, strip nonessential information, rebuild the massing from a few
confident volumes, exaggerate only the signature features, simplify the facade
into broad rhythms, deliberately design every surface visible from above,
evaluate from the app's high three-quarter aerial camera, then simplify again.

This is a **background building** in the style bible's detail budget (§21) — one step below
even the secondary tier. Clear massing, one facade rhythm, a flat designed roof, and
exactly two identity cues carried hard: the arch and the tile. Resist adding ornament of
any other kind. The correct outcome is a building that is obviously *this* one and
obviously not the steel-sash warehouse next door, achieved with under 7,000 triangles.

The finished asset must be immediately recognizable as this building, consistent with the
real one from all four sides and above, architecturally credible, and a premium
handcrafted miniature — not photorealistic, not voxel art, not generic low-poly, and never
accurate in one view while invented in the others.

## Scope of the exported asset

Export the single building: the two-storey volume on the measured footprint, the street
facade's pilasters, belt course, three upper openings and shopfront, the projecting
red-tile eave, the flat roof behind it, and whatever roof incident the research confirms.

Do not include unrelated surrounding city geometry: 156 South Park, 164 South Park, the
South Park oval or its lawn, paths and trees, the street tree standing in front of this
building, the street, the sidewalk, the rear yard and its fence, parked cars, people,
plinths, cameras or lights. Temporary context may appear in review renders but must not
leak into the GLB.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary
`.glb`; real-world meters; origin at base center; minimum geometry Z ~ 0;
applied transforms; no negative scales; outward normals; no duplicate or foreign
geometry; no image textures; no transparency; flat-color materials named `Toy_*`
from the project palette; `_Glow` suffix only on surfaces that glow at night; no
`Toy_body`; no cameras, lights, animations, armatures or constraints; at most
7,000 triangles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model
drops into the city at its real-world heading — the loader applies no rotation
(`placeGeneric` in `app/src/assets.js` only scales and positions). The street facade faces
**108.1°**, the front block runs back at 280.4° (south party line) and 284.0° (north party
line), and the rear block at 315.1°. Build directly on the measured polygon in 2.3 rather
than modelling an axis-aligned bar and rotating it. Record the measured heading in
`REPORT.md`, together with the deviation from the contract's "front faces −Y" rule (see
the orientation note in `docs/asset-plans/README.md`).

**Height normalization:** the tallest geometry in the export (the tile eave crest) must
land at exactly **9.4 m** so the loader's `targetHeightM / measuredHeight` scale is 1.0.

## Reproducible Blender workflow

Blender 5.2 LTS. Headless: `blender -b --python script.py -- args`.

Keep `artifacts/160-south-park/build_160_south_park.py` (deterministic build script),
`artifacts/160-south-park/160-south-park.blend`, and
`artifacts/160-south-park/160-south-park.glb`. The script must rebuild the model reliably
enough for future revision. Do not modify or rename an unrelated existing GLB to satisfy
the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`160-south-park-top.png`, `-north.png`, `-east.png`, `-south.png`, `-west.png`, plus
`160-south-park-contact-sheet.png`, at least one high three-quarter aerial beauty
render `160-south-park-aerial.png`, and a night render
`160-south-park-aerial-night.png`.

The four elevations must share scale, framing, lighting, exposure and projection; use
orthographic or long-lens cameras; label directions from the researched orientation; the
top view must clearly show the roof plane, the tile eave, the taper and the bend; the
aerial view uses the style bible's camera assumptions (30–50 degrees down, long lens).
Simple tabletop lighting, neutral warm background, minimal depth of field, and every image
must depict the same exported model.

Because the building is more than four times deeper than it is wide and sits at a ~108°
heading, frame the elevations to the long dimension and accept empty frame on some views
rather than zooming each view to fit — the reviewer needs to be able to compare them.
The street elevation is *not* one of the four cardinal views; add a fifth, square-on
render of the facade along its 108.1° normal, because that face carries the whole design.

**Night renders:** copy `Base Color` into `Emission Color` at strength 1.0 on the `_Glow`
materials of the re-imported GLB. Do not raise `Emission Strength` on the imported
material — glTF writes `emissiveFactor = 0`, so a re-imported `_Glow` material carries a
default white emission and every glow surface renders as a white slab. See the note at the
end of `docs/asset-plans/README.md`; `tools/glb-optimize/render_ab.py` already does it
correctly.

## Validate the exported GLB

Re-import `160-south-park.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture
count, camera count, light count, animation count, applied-transform status,
negative-scale status, normal-orientation status, unexpected geometry, and
per-material contract compliance. Render at least one review image from the
re-imported asset. Write `artifacts/160-south-park/validation.json` and
`artifacts/160-south-park/REPORT.md`.

One expected result that is **not** a fault, and must be stated rather than "fixed":

- The axis-aligned XY bounding box will be roughly **25.3 × 17.5 m** even though the
  building is 6.2 × 26.5 m. That is the consequence of the ~108° heading, not a scale error.

**Anchor convention** (as in `artifacts/165-south-park/build_165_south_park.py`): author the
polygon in world metres relative to the *design anchor* (the design footprint's area
centroid, given in 2.3), then recentre the model so its XY **bounding-box** centre is the
origin — contract rule 2 — and move the anchor by the same vector. The build script must
print the resulting manifest anchor; that printed value, not 2.3's design anchor, is what
goes in the manifest. On a bent strip the two are about 1.4 m apart.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "160-south-park",
  "file": "160-south-park.glb",
  "anchor": [
    -122.3948669,
    37.7812686
  ],
  "targetHeightM": 9.4,
  "cat": 3,
  "name": "160 South Park",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

`"estimated": false` because 9.4 m is a direct LiDAR maximum over 882 cells, not an
extrapolation — but read 2.15 before trusting what that maximum is a maximum *of*.

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a separate, explicitly requested job — run `docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in `docs/asset-plans/160-south-park.md`.
````

---

## Part 2 — Research and design dossier

Compiled 16 August 2026 from the sources in 2.2. Values marked *inferred* are visual or
derived estimates, not published figures — the executing agent must re-verify
anything it relies on.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Address | 160 South Park, San Francisco CA 94107 | DataSF address dataset `ramy-di5m`, one record, `37.781292 / -122.394902` |
| Parcel | `3775067`, `from_address_num` 160, `to_address_num` 160, zoning `SPD` (South Park District) | DataSF parcels `acdm-wktn` — **authoritative for shape and position** |
| Build year | **1924** | Assessor secured roll `wv5m-vpq2`, `year_property_built`; corroborated by the Redfin public-records page |
| Storeys | **2** | assessor roll `number_of_stories`; corroborated by three permits (2002, 2004, 2005) each recording 2 → 2, and by Street View |
| Rooms / baths | 6 rooms, 2 baths, 0 bedrooms recorded | assessor roll |
| Assessor use | `SRES` — Single Family Residential, class `D` Dwelling, Homeowners exemption | assessor roll — **conflicts with the Planning record below, see 2.15** |
| Planning land use | `MIPS` (office/professional), **3,674 sq ft** commercial, 0 sq ft residential, 1 residential unit | DataSF land use `fdfd-xptc`, `mapblklot=3775067` |
| Current ground-floor tenant | "Curie.Bio" (vinyl decal on the storefront glass) | Google Street View, Jan 2025 capture |
| Lot | **216.8 m²** (2,334 sq ft measured; 2,291 sq ft on the roll), 6.17 m frontage chord, 6.08 m rear, 36.4 m deep on the south party line / 33.2 m on the north | DataSF parcel polygon — **measured** |
| Built footprint | **166.4 m²**, ~26.5 m deep, leaving a ~50 m² rear yard | parcel truncated; reconciliation in 2.3 — **derived** |
| LiDAR building | `201006.0020110` (`mblr` SF3775067), 220.0 m², 882 cells at 50 cm | DataSF Building Footprints `ynuv-fyni` — **lot-shaped, see 2.3** |
| Ground | 6.91 m NAVD88 (median), 6.51 m minimum, 8.05 m maximum — the lot rises ~1.5 m from the park toward 3rd Street | same |
| Roof deck | **8.81 m** above grade (LiDAR height *mode*, `hgt_majoritycm` 881) | same — **measured** |
| LiDAR maximum | **9.41 m** above grade (`hgt_maxcm` 941); first-return peak 17.05 m is the street tree, not the building | same — **measured** |
| LiDAR median / mean / σ | 7.79 m / 6.66 m / 2.56 m | same — the median and mean are dragged down by the rear yard inside the polygon (2.3) |
| Tile eave crest | **9.4 m** | LiDAR maximum, adopted as the target height. See 2.15 |
| Front facade heading | faces **108.1°** (east-south-east) | measured, perpendicular to the parcel's curved front chord |
| Lot axis | front ~282° for ~12.8 m, then 315.1° to the rear | measured from the parcel side lines, which bend where the oval's radial lots meet the block grid |
| Permit history | 2002 rear-yard fence ($10k); 2004 rear windows/doors + baths ($32k); 2005 voluntary seismic upgrade, rear stucco → lap siding ($1) | DataSF building permits `i98e-djp9`, block 3775 lot 067 — **no vertical addition since at least 2002, so the 2010 LiDAR is current for height** |
| North neighbour | 156 South Park (lot `3775066`) — two-storey steel-sash industrial building, tenant "multistudio", party wall | DataSF parcels; Street View |
| South neighbour | 164 South Park (lots `3775068` + `3775069`) — 1907, under reconstruction by Stanley Saitowitz \| Natoma Architects (2024 permits), new red-brick-panel front | DataSF parcels; saitowitz.com; openpermitdata.com |
| Neighbourhood | South Park, laid out 1852–54 by George Gordon, designed by George Goddard on the model of a London crescent; SF's oldest planned residential square; renovated 2016–17 | Wikipedia, SF Curbed |

### 2.2 Sources

- DataSF `acdm-wktn` (Parcels), `blklot=3775067` — the surveyed lot polygon, the single
  160 address, and the SPD zoning. This is the geometric backbone of the plan.
- DataSF `ramy-di5m` (Addresses with Units), `street_name=SOUTH PARK` — the confirmation
  that 160 exists as an address (OSM has no `160` on this street) and the ordering of the
  rim: 150, 156, 160, 164, 166 running south-west from the park's north corner.
- DataSF `wv5m-vpq2` (Assessor Historical Secured Property Tax Rolls), block 3775 lot 067,
  rolls 2023–2025 — build year 1924, two storeys, six rooms, two baths, 2,291 sq ft lot,
  SRES use with a Homeowners exemption.
- DataSF `fdfd-xptc` (Land Use), `mapblklot=3775067` — 3,674 sq ft of MIPS floor area, one
  residential unit, zero residential floor area. The 3,674 sq ft is what makes the built
  depth in 2.3 solvable.
- DataSF `i98e-djp9` (Building Permits), block 3775 lot 067 — three permits since 2002,
  all recording two storeys before and after, which is what licenses the 2010 LiDAR.
- DataSF `ynuv-fyni` (Building Footprints, LiDAR-derived, 2010 survey, refreshed
  2023-09-11), building `201006.0020110` — the ground elevations and the height statistics
  used for the roof deck and the crest. Its *outline* is rejected; see 2.3.
- Google Street View, South Park north-west rim, **Jan 2025** capture, viewpoints around
  `37.78123 / -122.39470–122.39475`, headings 288°–293° — the street elevation: flat slate
  charcoal paint over the whole facade, the arched multi-pane window between two smaller
  rectangular multi-pane windows, the moulded archivolt, the projecting red barrel-tile
  eave, the proud lintel band with two square tie-plates, the recessed dark shopfront with
  the "Curie.Bio" decal, and the flush warm-wood door. The same panoramas establish that
  the "156" numeral is on the *steel-sash* building to the north, which is how 160 was
  identified.
- Esri World Imagery (z20, ~0.12 m/px), stitched and overlaid with the DataSF parcels —
  the flat roof, the rear yard and its vegetation. **Poorly registered against the parcel
  layer at this scale**; used only for the presence of a rear yard, not for measurement.
- https://www.redfin.com/CA/San-Francisco/160-S-Park-St-94107/home/726414 — public-records
  mirror: 1924, single-family, 2,291 sq ft lot, last sold 15 Feb 2002 for $600,000,
  off-market since. *Observed (listing page)*; no interior or exterior photography.
- https://www.saitowitz.com/164-south-park and
  https://openpermitdata.com/sf/address/164-south-park — the neighbour at 164, so it is not
  mistaken for this building.
- https://en.wikipedia.org/wiki/South_Park,_San_Francisco and
  https://sf.curbed.com/2017/3/8/14855870/south-park-renovation-sf — the oval's 1852–54
  origin and its 2016–17 renovation.
- Negative results worth recording: no Wikipedia or Wikidata entry, no SF Planning historic
  resource record located, no architect attributed, no real-estate listing photography, and
  no rooftop or oblique-aerial photograph of this building anywhere. The building's web
  footprint is three public-records mirrors and one Street View pass.

### 2.3 Orientation and placement

The building occupies the whole width of its lot on the north-west rim of the South Park
oval. Its street facade sits on the oval's curve and faces **108.1°** — east-south-east,
across the park. The lot runs back from the curve as a narrow strip that bends about 33°
partway along, because South Park's lots are radial at the street and orthogonal at the
rear where they meet the 3rd Street block grid.

Three separate geometries exist for this building and they do not agree. The plan resolves
them as follows:

| Source | What it is | Verdict |
|---|---|---|
| DataSF **parcel** `3775067` | surveyed lot boundary, 216.8 m² | **authoritative for shape and position** |
| DataSF **LiDAR footprint** `SF3775067` | 2010 raster-derived polygon, 220.0 m² | **authoritative for heights and for the exclusion centroid only** — its outline is the *lot*, not the building |
| OSM `way/124884344` (`158`) and `way/124884357` (`164`) | Bing traces, 76 m² and 468 m², neither carrying the address 160 | **rejected** — the house numbers do not match the surveyed parcels and one spans three lots |

**Why the LiDAR outline is rejected.** Its 220.0 m² is 1.5% larger than the whole surveyed
parcel, and its vertices are the parcel's vertices simplified. That would be harmless if
the lot were fully built, but the height statistics say it is not: `hgt_min` is 0.56 m and
`hgt_std` is 2.56 m, where the five neighbouring lots on the same block run 0.75–1.14 m.
Something inside that polygon is at ground level. The 2002 permit — "new fence at rear
yard to replace (e) fence & gate" — says what it is.

**Deriving the built depth.** Two independent routes agree:

1. *Floor area.* Planning records 3,674 sq ft = 341.3 m² over two storeys = **170.7 m²**
   per floor.
2. *LiDAR mixture.* With the roof at the 8.81 m mode and the yard at ~0.4 m, a mean of
   6.66 m over 882 cells implies a built fraction of 0.74–0.76, i.e. **164–168 m²**.

The design footprint is therefore the parcel truncated at **166.4 m²**, which is a rear wall
28.1 m back along the south party line and 24.9 m back along the north one (the two differ
because the lot's bend is not symmetric), leaving a rear yard of about 50 m². That
reproduces the Planning floor area to within 2.5%.

Measured design polygon, in Blender coordinates (metres, `+X` east, `+Y` north), relative to
the **design anchor** `-122.3948669, 37.7812686` — the polygon's own area centroid. (The
*manifest* anchor is this point moved by the recentring shift the build applies; see Part 1's
anchor convention.) The eleven short segments at the start are the oval's curve and may be
simplified to two:

```
( 12.873,  -1.497)  ─┐   north end of the street frontage
( 12.637,  -2.062)   │
( 12.411,  -2.631)   │
( 12.195,  -3.204)   │
( 11.988,  -3.781)   │
( 11.792,  -4.361)   ├─ street frontage, on the oval's curve (6.17 m chord)
( 11.606,  -4.944)   │
( 11.430,  -5.531)   │
( 11.265,  -6.120)   │
( 11.110,  -6.712)   │
( 10.952,  -7.365)  ─┘   south end of the street frontage
( -1.523,  -5.075)       south party line, bend
(-12.409,   5.841)       rear wall, south corner
( -8.103,  10.134)       rear wall, north corner
(  0.397,   1.611)       north party line, bend
```

Read as two pieces:

| Piece | Extent | Notes |
|---|---|---|
| Front block | 6.17 m wide × 12.8 m deep, running back at 280.4°/284.0° | carries the whole public elevation; the two party lines are not parallel — the lot fans 3.6°, as radial lots do |
| Rear block | 6.08 m wide × ~13–15 m deep, running back at 315.1° | party walls parallel; blind on both flanks |

Because of the ~108° facade heading the axis-aligned bounding box is **25.3 × 17.5 m**.
That is correct and is not a scale error. The bounding-box centre sits about
(+0.2, +1.4) m from the area centroid, so the recentring shift is about that much and the
manifest anchor lands about 1.4 m north-north-east of the design anchor above.

### 2.4 What each side shows

**East-south-east (street elevation, the only public face)** — Two storeys, flat and
uniformly painted a dark cool slate charcoal: walls, end pilasters, window surrounds,
mullions, belt course and shopfront frame are all the same colour.

*Upper storey.* Three openings in a slightly recessed panel field between two flat end
pilasters. Centred, a **round-arched multi-pane window** roughly 2.1 m wide, its
semicircular head ringed by a moulded archivolt that stands ~60–80 mm proud; the glazing is
a grid of small square panes that continues radially into the arch head. Flanking it, two
**rectangular multi-pane windows** with plain flat surrounds, the southern one slightly
wider than the northern. Pane counts are *inferred* from one capture: read as roughly
6 × 6 for the arch's rectangular portion and 4 × 5 / 3 × 5 for the flanking pair.

*Cornice.* A plain moulded band runs the full width at the top of the wall, and above it a
**shallow pent roof of dark red barrel tiles** projects over the sidewalk, sloping down
toward the park. Behind the tile the roof is flat. One small square stack rises at the
north end just above the tile line — *inferred*, and the most likely explanation of the
9.41 m LiDAR maximum.

*Ground storey.* A recessed dark shopfront under a proud horizontal lintel band carrying two
square tie-plates. From south to north: a narrow pier, a wide storefront window (a grid of
large panes, presently carrying a "Curie.Bio" decal), a slim pier, and a **flush
warm-wood-veneer door** with a plain transom panel above it. The door is the only warm
value at street level. Surface conduit, a downpipe and a security camera are present and
should not be modelled.

**North-east and south-west (party flanks)** — Blind. The north-east flank abuts 156's
steel-sash warehouse; the south-west flank abuts 164. Neither is visible from the app's
camera at any useful angle. Build them as flat planes with no openings.

**West-north-west (rear elevation)** — Faces the ~50 m² rear yard, visible only from
directly above. The 2004 permit replaced its windows and doors with steel, and the 2005
permit changed its finish from stucco to lap siding, so it is a plainer, more utilitarian
face than the street front. Unverified; keep it simple and consistent.

**Top** — This is the surface the app's camera actually sees. A **flat roof** running the
full 26.5 m at a constant 8.81 m, with the **red-tile eave** lifting to 9.4 m at the street
end only. That tile band is the single most valuable thing in the whole asset from the air:
it is warm, it is 6 m wide, and no neighbour on this rim has one. The stack at the north
end, if confirmed, is the roof's only other incident. Do not invent more.

### 2.5 Recognition cues (ranked)

1. **The arched window** — the only arch on this side of the oval, dead centre on a 6.17 m
   facade. Everything else about the building is a rectangle.
2. **The red barrel-tile eave** — the one warm colour, the one non-flat plane, and the only
   cue that survives at thumbnail size from directly overhead.
3. **The monochrome slate facade** — flat, matte, uniform, with relief instead of colour.
   It is what separates 160 from the painted rows elsewhere in the city and from its own
   steel-and-glass neighbour at 156.
4. **The proportion** — 6.17 m of frontage against ~26.5 m of depth, bending 33° partway
   back.
5. **The warm-wood door** beside the shopfront, the single warm accent at street level.

### 2.6 Miniature translation

**Preserve**

- The 6.17 m frontage, the 6.08 m rear, the ~26.5 m built depth, the 315.1° rear axis and
  the 108.1° facade heading, exactly
- The arch as a true semicircular head, not a flattened segmental one
- The tile eave as a genuinely projecting, genuinely sloping plane, and the flat roof
  behind it as genuinely flat
- The tripartite upper rhythm: small, big-and-arched, small
- The single warm door

**Simplify / exaggerate**

- The arched window's glazing becomes a `Toy_glass` panel with a coarse grid of proud
  muntin bars — three verticals, three horizontals and three radial bars in the head — not
  36 modelled panes. The grid must read as a grid at 40 px, which the real pane count
  will not.
- The archivolt is exaggerated: model it as a 0.14 m proud, 0.20 m wide band around the
  head, roughly twice its real relief, so the arch survives the aerial camera
- The tile eave is exaggerated in projection, to ~0.55 m, so it casts a real shadow line
  and reads as a band of colour from above; individual tiles become a flat colour with at
  most a shallow ribbed profile
- The two flanking windows become plain recessed rectangles with a single cross of muntins
  each
- The shopfront becomes one recessed opening plus one door, with the lintel band and its
  two tie-plates kept because they carry the whole ground floor
- Surface conduit, meters, downpipes, cameras, decals and house numbers all disappear
- The rear yard is not modelled at all — the asset stops at the rear wall

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not
a straitjacket — adjust after the first aerial review render. Heights are metres above
grade; the frontage is described from its south end.

1. Main volume: extrude the 2.3 polygon from z=0 to z=8.81, `Toy_roofd`.
2. Roof plane: flat cap at z=8.81, `Toy_ink` — one clear step darker than the walls so the
   outline reads from directly overhead.
3. Base bulkhead: a 0.35 m tall, 0.05 m proud band along the street elevation only,
   `Toy_ink`.
4. Ground storey openings, recessed 0.22 m, sills at z=0.35, heads at z=3.55:
   a 3.35 m storefront window in `Toy_glass` starting 0.50 m from the south end; then a
   0.32 m pier; then a 1.10 m door in `Toy_rust` (head z=2.40, with a plain panel above it
   to z=3.55); 0.90 m of pier to the north end.
5. Lintel band: 0.35 m tall from z=3.90 to z=4.25, 0.12 m proud, `Toy_roofd`, with two
   0.22 m square tie-plates in `Toy_ink` at the third points.
6. Upper panel field: recess the wall 0.08 m between z=4.25 and z=8.35, leaving a 0.55 m
   pilaster at each end.
7. Upper windows, recessed 0.14 m, sills at z=5.20:
   south rectangular 1.15 m wide, head z=7.55; central arched 2.10 m wide, springing at
   z=7.55, crest z=8.30; north rectangular 1.00 m wide, head z=7.55. All `Toy_glass`.
8. Archivolt: a 0.20 m wide, 0.14 m proud band in `Toy_roofd` following the arch head.
9. Muntins: 0.05 m square bars proud of the glass, `Toy_trim` — three verticals and three
   horizontals on the arch plus three radial bars in its head, one cross on each flanking
   window.
10. Cornice band: z=8.35 to z=8.81, 0.15 m proud, `Toy_roofd`.
11. Tile eave: a shallow pent slab over the full 6.17 m frontage, sloping *down* toward the
    street. Its ridge sits against the wall at **z=9.40**; its outer edge projects 0.55 m
    beyond the facade plane and lands at about z=9.05. `Toy_brick`. **The ridge sets the
    bounding-box top and must land exactly on 9.40.**
12. Roof stack (only if research confirms one): a 0.55 × 0.55 m box near the north party
    wall rising to no more than z=9.40, `Toy_roofd`. If it is confirmed *taller* than the
    tile ridge it becomes the tallest geometry and the target height must change to its
    crest — flag that to the reviewer rather than clipping it.
13. Rear elevation: one 1.0 × 2.1 m recessed door in `Toy_ink`, plus two plain recessed
    windows in `Toy_glass`, centred.
14. Bevel 0.10 m, 2 segments.

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_roofd` | `#45454a` | the whole facade and flanks — walls, pilasters, lintel band, archivolt, cornice |
| `Toy_ink` | `#3a3530` | the flat roof plane, the base bulkhead, the tie-plates, the rear door |
| `Toy_brick` | `#c96f4a` | **the tile eave** |
| `Toy_glass` | `#2a4d73` | all glazing, street and rear |
| `Toy_trim` | `#f3efe6` | the muntin bars only |
| `Toy_rust` | `#a86444` | **the street door** |
| `Toy_glass_Glow` | `#2a4d73` | the arched window at night (hero) |
| `Toy_glass_Glow` | `#2a4d73` | the ground-floor storefront window at night (supporting) |

Note on the wall colour: the real paint is a cool blue-charcoal around `#4a505a`.
`Toy_roofd` (`#45454a`) is the nearest palette entry and reads very slightly warm and
green. If the aerial render says it goes muddy against the tile, an off-palette `#4a505a`
is a WARN not a FAIL — justify whichever you pick in `REPORT.md`. Do **not** reach for
`Toy_ink` on the walls: the roof needs to stay darker than the walls or the plan outline
disappears from above, which is the one view that matters.

Note on `Toy_brick`: it must be used on the tile eave and nowhere else on this asset. It is
the building's only saturated colour and the whole reason the roof reads.

**Night state (required).** Glow surfaces must be thin shells proud of the opaque glazing —
the app renders `_Glow` in a separate layer that is ~12% alpha by day, so a primary surface
must never be authored as glow. Hero glow: **the arched window**, lit as one warm plane —
it is the building's identity by day and should be its identity by night. Supporting
accent: the ground-floor storefront window, at a lower value. The two flanking upper
windows stay dark; a fully lit facade would read as an office block and this is a
six-room building on a quiet oval. The tile does not glow. The roof does not glow.

### 2.9 Top surface

A flat 26.5 m strip, 6.1 m wide, bending 33° partway back, seen constantly from above and
from almost no other angle. Its quality comes from four things and nothing else: the
crispness of the bend, the red tile band across the street end, the cornice lift reading as
a bright edge against the darker roof plane, and whatever single stack the research
confirms. Keep the roof value clearly darker than both the walls and the tile so the
outline reads from directly overhead. Do not add invented rooftop clutter to make it
"interesting" — the emptiness is accurate, and the tile band already gives this roof more
to look at than any of its neighbours.

### 2.10 Scope

**In the GLB:** the single building — two-storey volume on the measured footprint, street
facade with pilasters, lintel band, shopfront and door, three upper openings with their
muntins and archivolt, cornice, projecting red-tile eave, flat roof, rear door and windows,
and a roof stack only if confirmed

**Not in the GLB:** 156 South Park, 164 South Park, the South Park oval, its lawn, paths or
trees, the street tree standing in front of this building, the street, the sidewalk, the
rear yard and its fence, vehicles, people, plinths, cameras or lights

### 2.11 Triangle budget

Cap 7,000 — a background building, 1,000 above the 165–167 cap purely because of the arch.
Suggested split: main volume and bend ~700, roof plane ~150, base bulkhead ~250, shopfront
and door ~800, lintel band and tie-plates ~350, upper panel field and pilasters ~450, two
rectangular windows with muntins ~700, arched window with archivolt and radial muntins
~1,600, cornice ~300, tile eave ~500, rear openings ~300, bevel overhead ~900. If the first
build lands above 7,000 the answer is fewer arch segments (10–12 is plenty) and fewer
muntins, not a raised cap.

### 2.12 Draft manifest entry

```json
{
  "id": "160-south-park",
  "file": "160-south-park.glb",
  "anchor": [
    -122.3948669,
    37.7812686
  ],
  "targetHeightM": 9.4,
  "cat": 3,
  "name": "160 South Park",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

`dims` and `tris` are placeholders until the asset is built and validated.

`cat` is `3` (Office) rather than `1` (House) because the SF Planning land use record for
this parcel is 3,674 sq ft of MIPS floor area and zero residential floor area, and the
ground floor visibly carries a commercial tenant. The assessor's `SRES` classification is
noted in 2.15; the category only drives the card's label chip and the honest label for what
a visitor sees is "Office".

### 2.13 Integration notes (for later, not this task)

- **New landmark.** Add a `pipeline/lib/landmarks.mjs` entry (`id: '160SouthPark'`) and
  re-bake the affected tiles, or the baked procedural building will intersect the GLB.

- **The site is currently baked.** Cell `23_13` contains a DataSF-sourced block on this
  exact footprint: 220 m², 8.6 m tall (`datasfHeight` = the midpoint of the 7.79 m median
  and the 9.41 m max), `topY` 15.9, `baseY` 6.2. It is 0.8 m shorter than the asset, so an
  unbaked check would show the asset poking through rather than the asset vanishing — do
  not let that make the re-bake look optional.

- **The manifest anchor and the registry `lon`/`lat` must differ, deliberately.** These are
  independent fields: `placeGeneric` in `app/src/assets.js` positions the GLB from the
  **manifest** `anchor` alone, while `pipeline/lib/landmarks.mjs` `lon`/`lat` is only the
  centre of the bake-time exclusion circle. On this site they cannot be the same point:

  | Field | Value | Why |
  |---|---|---|
  | manifest `anchor` | design anchor `-122.3948669, 37.7812686` plus the build's recentring shift (~1.4 m NNE) | the **design** (built) footprint, as the model is actually centred — where the building stands |
  | registry `lon`/`lat` | `-122.3949116, 37.7812949` | area centroid of the **DataSF LiDAR footprint**, which is the polygon the bake actually reads |

  They are 4.89 m apart, because the LiDAR polygon includes the rear yard and the design
  footprint does not. Measured from the manifest anchor, the exclusion window collapses:
  the design centroid is 4.89 m from the baked polygon's centroid and only 3.0 m from 156's
  nearest vertex, so no radius both drops this building and spares the neighbour. From the
  LiDAR centroid the window is wide open, because the baked polygon's own centroid is at
  0.00 m.

- **The exclusion radius. Measured, not guessed.** `excluded()` in `pipeline/buildings.mjs`
  drops a footprint when its centroid **or any ring vertex** falls inside the circle.
  Measured from the registry point above, against the DataSF footprints that the bake reads
  and against the committed tile `23_13`:

  | Polygon | Triggers at | Source |
  |---|---|---|
  | this building | **0.00 m** (its own centroid) | DataSF `SF3775067`, confirmed in tile `23_13` |
  | 156 South Park | **1.70 m** (shared party-line vertex) | DataSF `SF3775066`, confirmed in tile `23_13` |
  | 164 South Park | 5.92 m | DataSF `SF3775069` |
  | 150 South Park | 9.92 m | DataSF `SF3775065` |
  | 166–168 South Park | 16.35 m | DataSF `SF3775070` |

  So the radius must be **greater than 0** and **less than 1.70 m**. **Use `exclude: 1.2`**
  — 0.5 m of margin below the ceiling. A grid search over candidate centres confirms the
  LiDAR centroid is optimal: every alternative point trades our own zero-distance trigger
  for a smaller window, because our polygon's vertices are *shared* with the neighbours'.

- **The Overture gap-fill needs an explicit check, and OSM says it may not be catchable.**
  `pipeline/buildings.mjs` only calls `markOccupied` for footprints that survive exclusion,
  so removing this building's DataSF footprint leaves its bbox unoccupied and the Overture
  pass may re-add a building in its place. Using OSM as a proxy for Overture, both
  `way/124884344` and `way/124884346` trigger at **1.96 m** from the registry point — i.e.
  *outside* the 1.70 m ceiling, so no legal radius would drop them. The saving grace is the
  `occupiedFraction(bbox) > 0.25` test: this lot's bbox is a 32 × 24 m diagonal rectangle
  that overlaps 156, 164, 150 and 166, all of which survive exclusion and mark themselves
  occupied, so the gap-fill should be blocked before it starts. **That cannot be confirmed
  without `pipeline/data/overture_buildings.geojsonseq`** — re-measure against the real
  Overture polygon at integration time and confirm with `pipeline/verify-rebake.mjs` that
  the affected cell loses exactly one building and no neighbour. If a wrong-shaped building
  does come back, report it as a known FAIL rather than hiding it.

- **`exclude` is also the tree-clear and street-furniture radius.** At 1.2 m it clears
  neither, which is the right outcome: there is a real street tree directly in front of
  this building, tall enough to appear in the LiDAR first-return peak at 17.05 m, and it
  should stay. Do **not** set `clearTrees: true`.

- `loadRadius`: the default formula gives `max(2500, 9.4 × 30) = 2500` m. Take the default.

- Camera preset: the building is only legible from the park side, so fly to it from the
  east-south-east. `camera.js` puts the eye at `target + distance·(sin yaw, ·, cos yaw)`
  with `+x` east and `+z` south, so camera bearing = `180 − yaw`; a 108.1° facade wants
  **yaw 72**. `camera: { distance: 155, yaw: 72, pitch: 26 }` as a starting point, tuned
  against the live scene (cf. 165–167 at distance 160 for 9.0 m, 135 at 150 for 8.5 m).

- **Batch mode applies.** Several South Park rim buildings are in flight at once and a
  Case B re-bake rewrites ~600 generated files, so run the bake, QA against it, then
  `git checkout -- app/public/tiles api/_data` and commit source only. See
  `docs/asset-pipeline/ADDRESS-TO-ASSET.md` "Batch mode" and
  `docs/asset-pipeline/BATCH-INTEGRATE.md`.

- **The case for a kit piece keeps getting stronger, and this building is the counter-example
  that keeps it honest.** 165–167's plan argued that a row of near-identical narrow flats on
  a residential oval is what `KIT-INTEGRATION-PROMPT.md` exists for. That argument holds for
  the rim's plain lap-sided houses. It does not hold here: an arched window under a barrel-tile
  eave is not a tintable variant of anything else on the block, and a kit piece that tried to
  cover it would have to carry geometry nine other placements would never use. Build this one
  bespoke; build its plain neighbours from the kit.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0
- [ ] XY bounding-box centre at the origin (within ~0.01 m), and the recentring shift
      carried into the manifest anchor and printed by the build script
- [ ] Bounding-box top exactly 9.40 m (loader scale lands at 1.0) — or the stack's crest if
      one is confirmed taller, flagged explicitly rather than clipped
- [ ] Dimensions plausible in meters and consistent with 2.1 (XY bbox ~25.3 × 17.5 m is expected)
- [ ] Frontage 6.17 m and rear 6.08 m, not rounded toward a square plan; built depth ~26.5 m
- [ ] The arch is a true semicircle, centred, and its archivolt is proud of the wall
- [ ] The tile eave projects beyond the facade plane and slopes down toward the street
- [ ] The roof plane is darker than the walls
- [ ] Triangles at or under 7,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the arched window and the storefront window; glow shells proud of
      opaque glazing
- [ ] `Toy_brick` used on the tile eave and nowhere else; `Toy_rust` on the door and nowhere else
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (per-object signed volume for
      the union of solids; ray test residual <= 0.15%)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + the extra square-on facade view + contact sheet + night render,
      all regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

- **The 9.41 m maximum is the weakest number in the dossier and everything scales off it.**
  The 8.81 m roof deck is solid: it is the *mode* of 882 LiDAR cells, and for a flat roof the
  mode is the deck. The crest is not. 9.41 m is 0.60 m above the mode, which is exactly the
  margin a projecting tiled eave produces — and also exactly the margin a small roof stack
  produces, and this facade appears to have both. The two readings give the same target
  height, which is why the plan adopts 9.4 m, but they give different *geometry*: if the
  9.41 m belongs to a stack, the tile ridge is lower than 9.4 and the model's top is a
  0.3 m² box rather than a 6 m band. Resolving this from aerial or oblique imagery is the
  single highest-value verification before modelling. **Do not resolve it by taking the
  median** — 7.79 m is a roof-and-yard blend and would build a one-and-a-half storey house.
- **No source isolates this building's built footprint.** The parcel is surveyed and
  trustworthy; the LiDAR polygon is the lot; OSM is unusable. The 26.5 m built depth in 2.3
  is a reconciliation of a Planning floor area with a LiDAR height mixture, not a survey,
  and the rear wall's position is the part of it most likely to be wrong. It is also the
  part that matters least: no camera in the app ever sees that wall.
- **The assessor and Planning disagree about what this building is.** The tax roll calls it
  Single Family Residential, class D Dwelling, six rooms, two baths, with a *Homeowners*
  exemption — which means somebody's primary residence. SF Planning's land use record calls
  it 3,674 sq ft of MIPS office and zero square feet of residential. Both are current. The
  most likely reconciliation is a live/work or ground-floor-commercial arrangement typical
  of the SPD zoning, and the plan sides with Planning for `cat` because that is what the
  street shows. It does not affect the geometry either way.
- **Every facade number is inferred from one Street View pass (Jan 2025), partly obscured by
  a street tree.** Pane counts, the archivolt's relief, the tile's projection, the shopfront's
  division and the presence of the roof stack are all readings, not measurements. The pane
  counts are the least important of these (they get simplified anyway); the tile's projection
  is the most important, because it is what the aerial camera sees.
- **164 next door will not look like its photographs for long.** Its 2024 Saitowitz permit
  is for a new red-brick-panel front. A modeller working from a wide photograph taken from
  the south will see a maroon hoarding and graffiti immediately beside 160 and may read it as
  part of this building. It is not; 160's south flank is a blind party wall.
- **156 next door is the confusable one in the other direction.** It is the same dark grey,
  the same two storeys, and shares a party wall, but it is a steel-sash industrial building
  with horizontal window bands and no arch, no tile, and no shopfront. In the January 2025
  panoramas the numeral "156" is mounted beside *its* recessed entry, which is what
  identifies 160 as the arched building to the south — check that numeral before believing
  any other identification.
- **No architect, no historic-resource record, no primary documentation.** 1924 and "two
  storeys" come from the assessor's roll via DataSF, which is a public record but not an
  architectural one. No SF Planning survey record for this address was located, no
  Wikipedia or Wikidata entry exists, and no listing photography of any kind was found. A
  1924 Mediterranean-revival storefront on a 6 m South Park lot would not be expected to
  have a named architect, but the absence is worth stating rather than glossing.
- **The exclusion band is one-sided, not two-sided.** Unlike 165–167, the lower bound here is
  zero — the baked polygon's own centroid sits at the registry point — so the only real
  constraint is the 1.70 m ceiling set by 156's shared party-line vertex. That makes the
  DataSF side of the re-bake safe. The Overture side is not proven; see 2.13.
