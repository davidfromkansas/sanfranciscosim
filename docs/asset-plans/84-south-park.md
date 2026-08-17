# 84 South Park — SF-SIM asset plan

A 1907 post-earthquake sliver on the north-west rim of the South Park oval, raised
from two storeys to three by a 1992–94 vertical addition and re-fronted in the same
campaign as a contemporary live/work house. It sits on a 23 ft × 98 ft lot — 6.99 m
of frontage against 30.07 m of depth, a **4.3:1 sliver**, narrower than the Gran
Oriente Filipino Hotel four doors along the same rim and the thinnest building
planned for this set so far.

It has no published history and no landmark status, and that is exactly what makes
it a different modelling problem from its neighbours. There is no survey, no
nomination, no architect. What it does have is a facade nobody else on the oval
has: a **slate blue-green painted front** with a **living green wall** across the
ground floor, a rust-red timber door carrying the numerals, and — the thing that
matters from the app's camera — a **slatted pergola over a planted roof deck** at
the street end, standing ~1.7 m proud of a roofline where the neighbour on one side
is taller and the neighbour on the other is level. From directly above, that pergola
and roof garden *are* this building.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/84-south-park/`. This document is the plan only: Part 1 is the runnable
task prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `84-south-park` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor (manifest, placement) | `-122.3940683, 37.7819798` |
| WGS84 anchor (registry, exclusion only) | `-122.3940709, 37.7819871` — **not** the same point, see 2.13 |
| Target height | **13.20 m** to the roof-deck pergola crest; parapet / roof deck **11.50 m** |
| Footprint | 6.99 m frontage × 30.07 m deep, 210 m² — the building occupies the entire lot |
| Axis | long axis 135.2° / 315.2°; street facade faces **135.2°** (south-east, onto the oval) |
| Triangle cap | 7,000 |
| Category | `1` (house — assessor `SRES`, single-family dwelling with a homeowner exemption) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 84 South Park GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of the house at 84 South Park Street,
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
7. `artifacts/106-south-park/` — the closest reference implementation: the other
   4:1 party-wall sliver on the same oval, same background-building detail budget,
   same "legible only by its own width" problem. Take its massing discipline and its
   restraint. Note the differences: this building is a *contemporary* front on an
   old shell, it is a single dwelling not an SRO, its identity is carried by
   **colour and roof** rather than by a window grid, and unlike 106 it has almost no
   documentary record to lean on
8. `docs/asset-plans/84-south-park.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## This building is not what the assessor says it is

The 2025 secured roll still describes 84 South Park as a **two-storey**,
22-room, 7-bathroom dwelling built in 1907. Two of those three facts are stale.
The building permit record settles it:

- **1989** — permit filed against a **2-storey apartment** building.
- **1992-12-04** — `$361,782` **vertical addition**, `2 → 3 storeys`.
- **1994-06-13** — revision, again `2 → 3 storeys`; and a same-year permit to
  "move fireplace and garden area to **south deck**, revise **skylite**".
- **2008–2009** — three permits, all recorded at **3 storeys**, including
  "replace waterproof membrane on **roof deck**".

**Model three storeys, with a roof deck.** The 22 rooms and 7 baths are the 1907
rooming-house record and describe nothing you can see. See 2.1 and 2.15 risk 1.

## Must capture

- **The sliver proportion.** 6.99 m of frontage against 30.07 m of depth, three
  storeys. From the app's aerial camera this proportion *is* the building, and it is
  the sharpest one on the oval — thinner than 106's 7.32 m.
- **The colour.** A muted slate blue-green front, mid-dark, matte. Every other
  building on this stretch of the rim is taupe, cream, raw metal or brown shingle.
  This is the only tinted facade in the row and it is the single cue that survives
  being 30 m away in a 500 m tile.
- **The roof deck with its pergola**, at the **street (south-east) end**. An open
  slatted frame standing ~1.7 m above an 11.50 m parapet, with planting — including
  at least one small tree or palm — under and beside it. The pergola crest at
  **13.20 m** is the tallest geometry in the export and sets the target height.
- **The skylights.** Four square skylights in a row along the south-west half of
  the roof in the middle third, and a group of three along the north-east edge
  nearer the street. Confirm the count and position before building (2.9).
- **The rear light well.** The middle-rear of the roof opens into a planted
  court/deck at a lower level — the LiDAR minimum on this footprint is 8.18 m
  against an 11.36 m median, and the aerial shows greenery down in it.
- **The two-bay front.** A wide south-west bay carrying the ground-floor **living
  green wall** and a pale projecting box at second-floor level, and a narrow
  north-east bay carrying the **recessed entrance** (a rust-red timber door with the
  numerals "84") under a recessed third-floor terrace with a dark metal rail.
- **The stepped party walls.** 76–82 South Park on the north-east is **1.6 m
  taller**; 86–96 on the south-west is **0.2 m shorter** — effectively level. So
  both flanks are blind and the roof plane plus the pergola carry the whole
  silhouette. This is the opposite of 106, which had a visible flank strip.

## Research 84 South Park independently

Verify the dossier in this plan rather than trusting it. This building has the
**weakest documentary base** of any landmark in this set — no nomination, no
architect, no published description, and the one real-estate record found is a 1990
sale with no photographs. Everything in 2.4 below is read from Google Street View
(January 2025) and Bing aerial imagery. Re-check at minimum the architectural
height, the footprint, the WGS84 anchor and the real-world orientation, and gather
references covering:

- The **south-east street elevation** as it stands today — the exact bay split, the
  ground-floor green wall's extent, the entrance recess depth, the third-floor
  terrace, and whether the pale second-floor box is render, panel or metal
- The **roof from above** — settle the pergola (2.9). Its existence, extent and
  crest height are the largest single unknown in this plan and they set the target
  height. Also settle the skylight count and whether the dark structure near the
  street end is a stair bulkhead, a PV array or the pergola's own shadow
- The **rear (north-west) elevation and the small rear structure** on the same lot
  — DataSF LiDAR carries a separate 16 m² footprint (`sf16_bldgid 201006.0168103`,
  median height 7.99 m) at the back of this parcel that no photograph in this
  dossier shows
- Whether the facade colour is closer to a slate blue-green or a plain blue-gray,
  and how dark it reads in daylight (2.8 — this is a weak call)
- Day and night appearance

Prefer DataSF datasets, SF Planning records, assessor and permit data, geolocated
photography and aerial imagery. Never rely on a single photograph, a single
AI-generated image, or a single unsourced 3D model. Separate verified facts from
visual inference; if sources disagree, document the disagreement and decide.

**Three source problems are already resolved in 2.1–2.3 and 2.15 — re-check them,
do not silently re-inherit the wrong value:**

1. **OSM and DataSF do not agree on where this building is.** OSM `way/113545687`
   puts its centroid **2.7 m north-west** of the DataSF LiDAR footprint's, because
   OSM traces the full 29.6 m lot depth while the LiDAR footprint stops at 27.3 m,
   short of the rear light well. The DataSF **parcel** `3775055` — a clean surveyed
   rectangle, 30.07 × 6.99 m — sits between them and is the tie-breaker. The
   manifest anchor is the parcel centroid.
2. **`height=11` on the OSM way is the roof deck, not the crest.** It agrees with
   the LiDAR roof-deck median (11.36 m) and the LiDAR majority (11.49 m). The
   parapet is 11.50 m. The **pergola** is what stands at 13.20 m.
3. **The LiDAR maximum of 13.24 m is genuinely ambiguous and this plan reads it as
   the pergola, not as bleed.** The north-east neighbour 76–82 has a LiDAR median of
   13.08 m, so party-wall bleed would land in exactly the same place — the failure
   mode the Earl Warren and Gran Oriente plans both document. What tips it: the
   south-west neighbour 86–96 has its own maximum of 13.28 m against an 11.15 m
   median with *no* tall neighbour to bleed from, and Street View shows an open
   slatted frame standing above 84's parapet. **Settle this before you build**; it
   is the difference between a 13.20 m and an 11.50 m target height.

## Create a reference dossier

Write `artifacts/84-south-park/REFERENCE.md` containing: source links and what each
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

This is a **background building** in the style bible's detail budget (§21), one step
below the secondary tier. It has less documented content than 106 South Park did —
no bay grid, no cornice, no sign band — but two things 106 did not have: a colour
that carries at distance, and a roof that is genuinely designed rather than
inherited. Spend the budget on **the roof and the two-bay front**, and on nothing
else. Resist inventing period ornament: the 1907 building is inside this one, not
on it.

The finished asset must be immediately recognizable as this building, consistent
with the real one from all four sides and above, architecturally credible, and a
premium handcrafted miniature — not photorealistic, not voxel art, not generic
low-poly, and never accurate in one view while invented in the others.

## Scope of the exported asset

Export the single building: the three-storey volume on the measured footprint, the
two-bay street front with its green wall, entrance recess and terrace, the rear
light well and rear structure, and the flat roof with its parapet, skylights,
pergola and planting.

Do not include unrelated surrounding city geometry: 76–82 South Park, 86–96 South
Park, the South Park oval or its lawn and trees, the street trees in front of the
building, the street, the sidewalk, parked cars, people, plinths, cameras or
lights. Temporary context may appear in review renders but must not leak into the
GLB.

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
(`placeGeneric` in `app/src/assets.js` only scales and positions). The street facade
faces **135.2°** and the long axis runs back at **315.2°**. Build on the measured
rectangle in 2.3 rather than modelling an axis-aligned bar and rotating it. Record
the measured heading in `REPORT.md`.

**Height normalization:** the tallest geometry in the export (the pergola crest)
must land at exactly **13.20 m** so the loader's `targetHeightM / measuredHeight`
scale is 1.0. If your research overturns the pergola, the target becomes the
**11.50 m** parapet — say so loudly in `REPORT.md` and change the draft manifest
entry, do not quietly scale the model to the old number.

## Reproducible Blender workflow

Blender 5.2 LTS. Headless: `blender -b --python script.py -- args`.

Keep `artifacts/84-south-park/build_84_south_park.py` (deterministic build script),
`artifacts/84-south-park/84-south-park.blend`, and
`artifacts/84-south-park/84-south-park.glb`. The script must rebuild the model
reliably enough for future revision. Do not modify or rename an unrelated existing
GLB to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`84-south-park-top.png`, `-north.png`, `-east.png`, `-south.png`, `-west.png`, plus
`84-south-park-contact-sheet.png`, at least one high three-quarter aerial beauty
render `84-south-park-aerial.png`, and a night render
`84-south-park-aerial-night.png`.

The four elevations must share scale, framing, lighting, exposure and projection;
use orthographic or long-lens cameras; label directions from the researched
orientation; the top view must clearly show the roof plane, the parapet, the
pergola, the skylight layout and the rear light well; the aerial view uses the style
bible's camera assumptions (30–50 degrees down, long lens). Simple tabletop
lighting, neutral warm background, minimal depth of field, and every image must
depict the same exported model.

Because the building is more than four times deeper than it is wide **and** stands
at 135°, frame all four elevations to the long dimension and accept empty frame on
the north and east views rather than zooming each view to fit — the reviewer needs
to be able to compare them. Add one extra view looking square-on at the 135.2°
street facade; the four cardinal elevations all show this building obliquely and
none of them shows its public face properly. Add a second extra view looking
straight down at the roof at 3× the top view's zoom — the roof is this asset's
whole silhouette and the contact sheet's top tile is too small to judge it.

## Validate the exported GLB

Re-import `84-south-park.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture
count, camera count, light count, animation count, applied-transform status,
negative-scale status, normal-orientation status, unexpected geometry, and
per-material contract compliance. Render at least one review image from the
re-imported asset. Write `artifacts/84-south-park/validation.json` and
`artifacts/84-south-park/REPORT.md`.

Note that the axis-aligned XY bounding box will be roughly **26.2 × 26.2 m** even
though the building is 6.99 × 30.07 m — that is the exact consequence of a 45°
heading on a long thin box, not a scale error.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "84-south-park",
  "file": "84-south-park.glb",
  "anchor": [
    -122.3940683,
    37.7819798
  ],
  "targetHeightM": 13.2,
  "cat": 1,
  "name": "84 South Park",
  "estimated": true,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

`"estimated": true` is deliberate — no height for this building is published
anywhere. 13.20 m is the DataSF LiDAR maximum, read as the pergola crest; 11.50 m
is the LiDAR majority read as the parapet. Both are derived, neither is a source.
See 2.1 and 2.15 risk 2.

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a separate, explicitly requested job — run `docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in `docs/asset-plans/84-south-park.md`.
````

---

## Part 2 — Research and design dossier

Compiled 16 August 2026 from the sources in 2.2. Values marked *inferred* are visual
or derived estimates, not published figures — the executing agent must re-verify
anything it relies on. **This dossier has no survey, no nomination and no
architectural publication behind it**, which is unusual for this set; treat 2.4 in
particular as observation, not record.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Address | 84 South Park (Street), San Francisco CA 94107 | DataSF parcels `acdm-wktn`, `blklot=3775055`, `from_address_num` = `to_address_num` = 84 — **one property, one building, one address** |
| Block / lot | 3775 / 055; zoning `SPD` (SOMA–South Park) | DataSF parcels; assessor roll |
| Built | **1907** | Assessor secured roll `wv5m-vpq2`, `year_property_built` — post-earthquake reconstruction, same year as the Gran Oriente four doors along |
| Architect | **unknown** — none found | no nomination, no publication, no permit attribution located |
| Storeys | **3** since a 1992–94 vertical addition; **2** before it | DBI permits `i98e-djp9`: 1992-12-04 `2 → 3`, `$361,782`, "vertical addition"; 1994-06-13 revision `2 → 3`; every permit from 1993 on records `3` |
| Use | single-family dwelling (`SRES`, property class `D`), homeowner exemption, in the same ownership since a **1990-08-28** sale | assessor roll — **current**; the 1989 permit still says "apartments", so the conversion to one dwelling is part of the same 1990–94 campaign |
| Assessor storeys / rooms | 2 storeys, 22 rooms, 7 bathrooms, 4,462 sq ft | assessor roll — **stale**, describes the 1907 rooming house; see 2.15 risk 1 |
| Lot | **22.94 ft × 98.66 ft = 6.99 × 30.07 m**, 210.3 m²; the building occupies the entire lot | DataSF parcel polygon `3775055` — **surveyed**; the assessor roll's `lot_area` 2,242.5 sq ft (208.3 m²) and `lot_depth` 97.5 ft corroborate to ~1% |
| OSM footprint | `way/113545687`, min-area OBB **29.60 × 7.29 m** at 135.0°, 203.7 m² | OSM API, reprojected — **measured**, but 2.7 m off the LiDAR centroid, see 2.3 |
| DataSF LiDAR footprint | `mblr` SF3775055 / `sf16_bldgid` 201006.0028685, OBB **27.31 × 7.43 m** at 136.3°, 184.8 m² polygon, 746 cells at 50 cm | DataSF `ynuv-fyni` — **measured**; short of the lot's rear because of the light well |
| Rear structure | a second SF3775055 footprint, `sf16_bldgid` 201006.0168103, **16 m²**, roof-height median **7.99 m**, 15.6 m behind the main footprint's centroid | same — **measured**; no photograph of it was found |
| Roof deck | **11.36 m** above grade (LiDAR height median); majority **11.49 m**; mean 10.95 m; minimum 8.18 m; σ **1.25 m** | DataSF `ynuv-fyni` — **measured**; the low tail is the rear light well, the σ is the roof's own structures |
| LiDAR maximum | **13.24 m** | same — read here as the **pergola crest**, not as party-wall bleed; see 2.15 risk 2 |
| Ground | 10.76 m NAVD88 minimum, 11.22 m median, 11.63 m maximum (0.87 m of fall across the lot) | same — the app's terrain handles this, not the asset |
| OSM tags | `building=yes`, `height=11`, `addr:housenumber=84` | OSM — the height matches the roof deck, not the crest |
| Facade heading | street elevation faces **135.18°** (SE, onto the oval); long axis 315.18° | measured from the DataSF parcel rectangle; OSM's 135.03° and the LiDAR footprint's 136.3° both agree to within 1.2° |
| Neighbours | **76–82 South Park** (lot 3775054, NE party wall, LiDAR median **13.08 m** — *1.6 m taller*) and **86–96 South Park** (lot 3775116, SW party wall, LiDAR median **11.15 m** — *0.2 m shorter*) | DataSF parcels + `ynuv-fyni` — **measured**; this near-symmetry is a design fact, see 2.4 |
| Neighbourhood | South Park, laid out 1852–54 by George Gordon; a 550 ft × 75 ft oval bisected NE–SW by South Park Street and NW–SE by Jack London Alley; this building is on the north-west rim, ~24 m north-east of the oval's centre and one lot north-east of Jack London Alley's block | DataSF geometry; FoundSF; Curbed SF |
| Designation | **none found** — not NR-listed, not NR-nominated, no Article 10/11 designation located | absence of evidence; see 2.15 risk 6 |

### 2.2 Sources

- **DataSF `acdm-wktn` (Parcels)**, `blklot=3775055` — the surveyed lot rectangle,
  the single 84 address, SPD zoning, and the neighbour lots 3775054 and 3775116.
  This is the strongest geometry in the dossier: a clean 30.07 × 6.99 m rectangle.
- **DataSF `ynuv-fyni` (Building Footprints, LiDAR-derived, 2010 survey, refreshed
  2023-09-11)**, `mblr` SF3775055 — footprint, ground elevation, roof-deck height
  statistics, the 16 m² rear structure, and the neighbours' heights that make the
  13.24 m maximum arguable in both directions.
- **DataSF `wv5m-vpq2` (Assessor secured roll, 2025 and 2024 closed rolls)**,
  `parcel_number 3775055` — 1907, `SRES`, homeowner exemption, the 1990-08-28 sale,
  and the stale 2-storey / 22-room / 7-bath record.
- **DataSF `i98e-djp9` (Building permits)**, block 3775 lot 055 — 14 permits,
  1989–2009. This is the document that reconstructs the building's real history:
  the 1992 `$361,782` vertical addition from 2 to 3 storeys, the 1994 south-deck and
  skylight revision, the 1993–94 sprinkler retrofit, and the 2009 roof-deck
  membrane replacement.
- **OSM `way/113545687`** — the footprint cross-check and the `height=11` tag.
- **Google Street View, South Park, January 2025 capture**, viewed from
  `37.781845, -122.393885` and `37.781790, -122.393930`, headings 309–318°, pitch
  −18 to −25° — the current street elevation, the green wall, the rust-red door with
  the numerals, the pale second-floor box, the third-floor terrace, and the roof
  pergola seen against the sky from the south-west.
- **Bing aerial imagery (Virtual Earth `a`-layer, z20, ~0.118 m/px)** at
  `37.7819922, -122.3940881`, rotated to the building's long axis and cropped to the
  parcel — the roof plan: the rear light well and its planting, the four skylights,
  the pergola grid, the north-east skylight group, the roof-garden planting and the
  parapet. Esri World Imagery at the same location is materially worse here (dark,
  and mis-registered against the footprint by several metres) and was discarded.
- The Hawthorne Group listing for **76–82 South Park Street**
  (`thgcommercial.com/project/76-82-south-park-street/`) — establishes that the
  north-east neighbour is a three-storey live/work building with 82 on the first
  floor, 80 on the second and 78 on the third, which is why its LiDAR median is
  13.08 m.
- The Grubb Company record for 84 S Park Street
  (`grubbco.com/property/84-s-park-street-san-francisco-ca-94107/78764035/`) — the
  1990 sale at `$360,000` and the 1907 build year, with **no photographs**. It is the
  only real-estate record for this address that was located and it adds nothing
  visual.
- FoundSF, "South Park First Buildings"; Curbed SF, "Then & Now: South Park Used to
  Be Home to San Francisco's Elite" (27 July 2012) — neighbourhood history only. No
  source describing this building specifically was found.

### 2.3 Orientation and placement

South Park is an oval whose rim buildings face inward. This one sits on the
**north-west rim**, one lot north-east of the Jack London Alley corner, and faces
**south-east across the oval**. It is *not* a through lot — the rear faces the
mid-block open space behind the Bryant Street parcels, not a second street.

Three geometries exist and, unlike 106 South Park, they do **not** all agree:

| Source | What it is | Verdict |
|---|---|---|
| DataSF parcel `3775055` | surveyed lot rectangle, 30.07 × 6.99 m at 135.18°, area centroid `-122.3940683, 37.7819798` | **authoritative for dimensions and for the anchor** |
| DataSF LiDAR footprint SF3775055 | 2010 raster-derived built area, OBB 27.31 × 7.43 m at 136.3°, area centroid `-122.3940630, 37.7819753` | **confirms the axis**, but 2.8 m short at the rear — it stops before the light well |
| OSM `way/113545687` | building trace tagged `84` | **confirms the depth** (29.60 m) but its centroid sits **2.7 m north-west** of the LiDAR's |

The parcel centroid sits between the other two — 0.68 m from the LiDAR centroid and
1.93 m from the OSM centroid — and it is the only one of the three that is a survey.
**Take the parcel centroid for placement.** The 2.7 m OSM/LiDAR spread is not an
error in either: OSM traces the whole lot depth, the LiDAR footprint stops where the
roof does. It matters for the exclusion radius (2.13), where both traces have to be
dropped.

Design footprint: a plain rectangle **6.99 m × 30.07 m** centred on the manifest
anchor, long axis running back at 315.18° (north-west). In Blender coordinates
(metres, `+X` east, `+Y` north, origin on the anchor) the four corners are:

```
corner              X (east)   Y (north)   which end / which flank
street north-east    +8.03      -12.99     South Park St frontage, 76–82 party wall
street south-west   +12.99       -8.03     South Park St frontage, 86–96 party wall
rear   north-east   -12.99       +8.03     rear end, 76–82 party wall
rear   south-west    -8.03      +12.99     rear end, 86–96 party wall
```

The street frontage is the +8.03/+12.99 edge (6.99 m long, facing 135.2°); the two
long 30.07 m edges are the party walls, the north-east one facing 45.2° toward
76–82 South Park and the south-west one facing 225.2° toward 86–96.

Because the heading is 45° off the axes, the axis-aligned XY bounding box of the
bare volume is **26.21 × 26.21 m**. That is correct and is not a scale error.

**Party walls on both sides, and both of them are effectively blind.** 76–82 to the
north-east is 1.6 m taller, so that wall is completely hidden. 86–96 to the
south-west is only 0.2 m shorter, so at most a 0.2–0.35 m strip of that wall shows —
below the threshold at which the app's camera can resolve it. **Only the street
front, the rear elevation and the roof are ever seen.** This is the opposite of
106 South Park, whose 3.2 m exposed flank was one of its two silhouette cues, and it
is why this asset's budget goes to the roof.

### 2.4 What each side shows

All of this is read from the January 2025 Street View capture and the Bing aerial.
None of it is documented in prose anywhere. Treat it as observation.

**South-east (street elevation, the public face)** — Three storeys of smooth,
matte, **mid-dark slate blue-green** wall, unbroken by trim, in a row where every
neighbour is taupe, cream, brown shingle or raw metal. It divides into two unequal
bays:

- The **wide south-west bay** (roughly 4.2 m of the 6.99 m frontage) carries at
  ground level a **living green wall** — a framed, recessed panel of dense planting
  and trailing ferns, roughly 3 m wide and 2 m tall, with a horizontal window behind
  or beside it. Above it at second-floor level a **pale, near-white box projects**
  from the face, carrying a large window with a broad light frame. Above that, at
  third-floor level, the wall steps back again to darker glazing.
- The **narrow north-east bay** (roughly 2.7 m) carries the **entrance**: a
  **rust-red / dark red-brown timber door** in a shallow recess, with the numerals
  **84** mounted on the wall beside its head. Above the door the wall opens into a
  **recessed terrace** running up through the second and third floors, fitted with a
  dark metal rail and a planter.

**North-east (party flank toward 76–82 South Park)** — Abuts the neighbour, which is
1.6 m taller. Not visible at all. Build it blind.

**South-west (party flank toward 86–96 South Park)** — Abuts the neighbour, which is
0.2 m shorter. Effectively not visible either; a 0.2 m strip at the top is below what
the app's camera resolves. Build it blind and do **not** spend budget on a flank
treatment. The one thing that *does* stand above both neighbours is the pergola.

**North-west (rear)** — Faces the mid-block open space behind the Bryant Street
lots, so it is seen in the app only from above and obliquely. The aerial shows the
rear third of the lot is not a solid roof: a **planted light well or rear deck**
sits down in it, with visible greenery, and beyond it at the very back of the lot
the separate **16 m² rear structure** with a glazed or gridded roof, standing about
8.0 m tall against the main building's 11.4 m. No elevation photograph of this side
was located.

**Top** — The whole point of this asset. Reading from the rear (north-west) to the
street (south-east) along the 30 m axis, the aerial shows:

1. the **rear structure**, low, with a gridded glazed roof;
2. the **open planted light well / rear deck**, pale-surfaced, with greenery;
3. a run of **four square skylights** in a line along the south-west half of the
   roof width, occupying roughly the middle third of the depth;
4. a plain stretch of pale membrane deck;
5. the **pergola** — a dark, regularly slatted open frame, roughly 3–4 m along the
   axis and spanning most of the roof width, reading in plan as a ladder of shadow
   bars;
6. a group of **three skylights** along the north-east edge, nearer the street;
7. the **roof garden** at the street end — planting including at least one small
   tree or palm, a darker structure that may be a stair bulkhead, and something
   distinctly reddish;
8. the **parapet**, a bright band along the street edge.

### 2.5 Recognition cues (ranked)

1. **The colour.** A mid-dark slate blue-green facade in a row of taupe, cream, raw
   metal and brown shingle. At the distance the app usually views this oval, colour
   is the only channel with any bandwidth left, and this is the only building on the
   rim using it.
2. **The 4.3:1 sliver.** 6.99 m wide, 30.07 m deep, three storeys — the thinnest
   building planned for this set, thinner than 106's 7.32 m.
3. **The pergola over the roof garden**, at the street end. It is the tallest thing
   on this stretch of the rim's roofline (13.20 m against 13.08 m next door and
   11.15 m on the other side) and, because both flanks are blind, it is the only
   part of this building that breaks the row's silhouette.
4. **The skylit roof with a hole in it.** Four skylights along one edge, three along
   the other, and an open planted light well cut into the rear third. From directly
   overhead that reads as a designed surface rather than a slab.
5. **The two-bay front**: a wide bay with a green wall under a pale projecting box,
   and a narrow bay with a rust-red door under a recessed terrace.

### 2.6 Miniature translation

**Preserve**

- The 6.99 × 30.07 m footprint, the 315.2° axis and the 135.2° facade heading,
  exactly
- Three storeys, the 11.50 m parapet and the 13.20 m pergola crest
- The **two-bay split** and its handedness: green wall and projecting box on the
  **south-west**, entrance and terrace on the **north-east**. Mirroring this puts
  the front door against the wrong party wall
- The rear light well as a real hole in the roof plane, not a painted patch
- The skylight asymmetry: four on the south-west side, three on the north-east side
- The pergola as an **open** frame — you must be able to see roof through it from
  above

**Simplify / exaggerate**

- The living green wall becomes one recessed panel in a single saturated green,
  with a 0.06 m proud frame. No individual plants, no fronds
- The projecting box becomes a clean rectangular volume, 0.35 m proud, with one
  recessed window and a broad flat surround
- The entrance recess becomes a single deep rectangular hole with a dark back
  plane; the door is one slab in the accent red. The numerals are sub-pixel and must
  **not** be modelled as glyphs
- The third-floor terrace becomes one recess with a flat rail slab across it — no
  balusters, no posts
- The pergola becomes **five to seven** square-section beams on two end frames.
  Do not model joinery, do not model a full grid in both directions
- The roof planting becomes two or three low blocked masses plus one simple
  small-tree form; no foliage detail
- The rear structure becomes one low box with a flat glazed cap
- Downpipes, meters, vents, conduit and the parapet coping profile all disappear
- Neither neighbour is modelled, and neither flank gets any treatment

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not a
straitjacket — adjust after the first aerial review render. All heights are metres
above the model's z = 0.

1. Main volume: extrude the 2.3 rectangle from z=0 to z=11.20, `Toy_verdigris`.
2. Parapet: a 0.30 m band around the whole roof edge from z=11.20 to **z=11.50**,
   0.06 m proud, `Toy_trim`. This sets the roof crest.
3. Roof plane: flat cap at z=11.20, `Toy_stone`.
4. Rear light well: cut a **4.6 × 4.6 m** opening in the roof plane centred
   10.4 m back from the anchor along the long axis, dropping to a floor at z=8.10 in
   `Toy_stone`, with `Toy_verdigris` reveals. Two low `Toy_mint` planting blocks on
   its floor.
5. Rear structure: a 4.0 × 4.0 × 8.00 m box at the extreme rear (north-west) end,
   `Toy_verdigris`, capped with a 0.15 m `Toy_glass` slab at z=8.00.
6. Skylights, south-west row: four 1.30 × 1.30 m boxes, 0.28 m proud of z=11.20,
   `Toy_glass` tops with `Toy_trim` kerbs, at long-axis stations −9.5, −7.2, −4.9
   and −2.6 m, offset 1.6 m toward the south-west party wall.
7. Skylights, north-east group: three 1.20 × 1.20 m boxes, same construction, at
   stations +6.0, +7.8 and +9.6 m, offset 1.7 m toward the north-east party wall.
8. Pergola: two `Toy_ink` end frames 0.16 m square standing from z=11.20 to
   **z=13.20**, spanning 5.4 m across the roof at stations +3.0 and +6.6 m, carrying
   **six** 0.14 m square cross-beams at z=13.06. The top of the beams is the
   bounding-box top and must land exactly on 13.20.
9. Roof garden: two `Toy_mint` planting blocks 1.6 × 0.9 × 0.55 m at station +10.5 m,
   one `Toy_ink` bulkhead box 1.4 × 1.2 × 1.9 m at station +11.8 m against the
   north-east wall, and one simple small-tree form (a 0.14 m `Toy_rust` trunk to
   z=12.4 with a single 1.5 m `Toy_mint` canopy blob) at station +12.6 m.
10. Street front, south-west bay: recess the wall 0.10 m over a 4.20 m width from
    the south-west corner. Inside it, the green-wall panel — 3.00 × 2.10 m in
    `Toy_mint`, sill at z=1.05, recessed a further 0.08 m, with a 0.06 m proud
    `Toy_trim` frame — and a 1.60 × 0.70 m `Toy_glass` window beside it at the same
    sill height.
11. Street front, projecting box: a 4.00 × 3.10 × 0.35 m volume in `Toy_trim` from
    z=4.10 to z=7.20 over the south-west bay, with one 2.60 × 1.60 m recessed
    `Toy_glass` window in its face.
12. Street front, third floor: a 3.80 × 1.90 m `Toy_glass` window recessed 0.14 m in
    the south-west bay, sill at z=8.30.
13. Street front, north-east bay: a 2.55 m wide, 8.20 m tall recess 0.55 m deep from
    z=0 to z=8.20, back plane `Toy_roofd`. Inside it at ground level a 1.05 × 2.30 m
    `Toy_red` door slab; at z=4.10 and z=7.40 two 2.30 × 0.12 m `Toy_ink` rail slabs
    standing 0.10 m proud of the recess floor.
14. Rear (north-west) elevation: `Toy_steel` value change over the whole face; three
    1.00 × 1.40 m `Toy_glass` windows at z=4.30 and three at z=7.60.
15. Bevel 0.10 m, 2 segments.

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_verdigris` | `#9fb8a8` | the whole body — the slate blue-green facade, all three storeys, the rear structure, the light-well reveals |
| `Toy_trim` | `#f3efe6` | the parapet, the projecting second-floor box, window surrounds, skylight kerbs, the green-wall frame |
| `Toy_stone` | `#d9d2c2` | the roof deck membrane and the light-well floor |
| `Toy_mint` | `#8fd0a8` | the ground-floor living green wall, the roof-garden planting blocks, the tree canopy |
| `Toy_ink` | `#3a3530` | the pergola frame and beams, the roof bulkhead, the terrace rails |
| `Toy_red` | `#c4453c` | the entrance door — the one saturated accent |
| `Toy_rust` | `#a86444` | the roof tree's trunk |
| `Toy_roofd` | `#45454a` | the entrance/terrace recess back plane |
| `Toy_steel` | `#9aa0a6` | the rear elevation |
| `Toy_glass` | `#2a4d73` | all windows, the skylight tops, the rear structure's glazed cap |
| `Toy_glassl_Glow` | `#6f95b8` | two lit windows at night |
| `Toy_trim_Glow` | `#f3efe6` | a warm spill in the entrance recess at night |

Two notes on colour:

- **`Toy_verdigris` is a compromise and the executing agent should expect to argue
  with it.** The real facade is a *mid-dark* slate blue-green — around `#6d8188` by
  eye, on a north-east-facing wall in January shade under a full-grown street tree.
  `Toy_verdigris` is the palette's nearest hue but it is roughly two values lighter
  and more chalky. The style bible's SF exception explicitly allows painted
  residential rows to keep their tinted facades, and off-palette colours are a WARN
  and not a FAIL in `sf-asset-check`. If the first aerial render shows the building
  reading as pale sage next to the cream and taupe neighbours — losing the one cue
  that made it worth modelling — **darken it off-palette toward `#6d8188` and record
  the decision in `REPORT.md`.** Do not split the difference into a colour that is
  neither.
- **The green wall must stay green, and it must stay small.** It is a 3 m panel on a
  7 m frontage. `Toy_mint` at that size is a jewel; `Toy_mint` spread across the
  whole ground floor is a lawn stapled to a house.

**Night state (required).** Glow surfaces must be thin shells proud of the opaque
glazing — the app renders `_Glow` in a separate layer that reads ~12% alpha by day
per surface, and a closed shell is two of those layers, so a primary surface must
never be authored as glow. Hero glow: **two** windows lit — the big projecting-box
window on the second floor and one third-floor window — unevenly, because this is
one family's house on a quiet oval and a fully lit front would read as an office.
Supporting accent: a warm spill in the entrance recess, which at night is also what
tells the eye the recess is a door. The skylights, the rear elevation, the green
wall and the pergola do **not** glow.

### 2.9 Top surface

A 6.99 × 30.07 m roof at 11.20 m with an 11.50 m parapet, seen constantly from
above and — because both party walls are blind — from almost nowhere else. Four
things carry it:

1. **The pergola.** A dark slatted open frame at the street end, 2.0 m above the
   parapet. It is the tallest geometry in the export, it is the only part of this
   building that stands clear of both neighbours, and in plan it reads as a ladder
   of bars that nothing else on this rim has.
2. **The roof garden** around and beyond it: planting blocks, a small tree, a
   bulkhead. Small saturated greens against a pale membrane.
3. **The skylight asymmetry** — four along one long edge, three along the other.
4. **The rear light well** — a real 4.6 m hole in the roof plane with a planted
   floor 3 m down. From overhead it is the difference between a slab and a building.

**The open question is the pergola itself, and it is the biggest one in this plan.**
The evidence for it: Street View from the south-west (`37.781790, -122.393930`,
heading 318°, pitched up) shows an open frame of horizontal beams standing against
the sky above this building's parapet; the Bing aerial shows a regularly slatted
dark rectangle in the corresponding position; the DataSF LiDAR maximum on this
footprint is 13.24 m against an 11.36 m median, which a 2 m pergola explains
exactly; and the 1994 permit moved a "garden area to south deck", the 2009 permit
replaced a roof-deck membrane. The evidence against: the north-east neighbour's
LiDAR median is 13.08 m, so party-wall bleed would produce the same maximum, and
that failure mode has already caught two plans in this set.

**Settle it before building.** If the pergola is real, it sets the target height at
13.20 m and it is the asset's best feature. If it is not, the target height is the
11.50 m parapet, the roof is carried by the skylights and the light well alone, and
this asset becomes a much plainer object. Do **not** hedge by modelling a token
low frame.

### 2.10 Scope

**In the GLB:** the single building — the three-storey volume on the measured
footprint, the parapet, the two-bay street front with its green wall, projecting
box, entrance recess, door and terrace rails, the rear elevation, the rear light
well and its planting, the separate rear structure, and the roof with its
skylights, pergola, planting, tree and bulkhead

**Not in the GLB:** 76–82 South Park, 86–96 South Park, the South Park oval, its
lawn, paths or trees, the street trees in front of the building, the street, the
sidewalk, fences, vehicles, people, plinths, cameras or lights

### 2.11 Triangle budget

Cap 7,000 — a background building, but one whose whole budget goes upward.
Suggested split: main volume ~300, parapet ~400, roof plane and light well ~700,
rear structure ~200, seven skylights ~900, pergola (two frames plus six beams)
~800, roof garden blocks, bulkhead and tree ~900, green wall panel and frame ~350,
projecting box with window ~600, third-floor window ~200, entrance recess with
door and two rails ~700, rear windows ~500, bevel overhead ~450. If the first build
lands above 7,000 the answer is fewer pergola beams and blockier planting, not a
raised cap.

### 2.12 Draft manifest entry

```json
{
  "id": "84-south-park",
  "file": "84-south-park.glb",
  "anchor": [
    -122.3940683,
    37.7819798
  ],
  "targetHeightM": 13.2,
  "cat": 1,
  "name": "84 South Park",
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

- **New landmark.** Add a `pipeline/lib/landmarks.mjs` entry (`id: '84SouthPark'`)
  and re-bake the affected tiles, or the baked procedural building will intersect
  the GLB. This is the Case B path in `docs/asset-plans/INTEGRATION-PROMPT.md`.

- **The exclusion window is tight, and the manifest anchor is the wrong point to
  measure it from.** `excluded()` in `pipeline/buildings.mjs` drops a footprint when
  its centroid **or any ring vertex** falls inside the circle. Two rings have to go
  — the DataSF footprint and the Overture/OSM trace of the same building, which sit
  2.7 m apart — while both party-wall neighbours have vertices under 4 m away.
  Measured against the DataSF footprints and the OSM ways as an Overture proxy:

  | Registry point | own rings dropped by | nearest neighbour trigger | usable window |
  |---|---|---|---|
  | manifest anchor (parcel centroid) | 2.00 m | 3.43 m (86–96) | (2.00, 3.43) — 1.43 m |
  | DataSF LiDAR area centroid | 2.66 m | 3.70 m (86–96) | (2.66, 3.70) — 1.04 m |
  | OSM OBB centre | 2.67 m | 3.27 m (86–96) | (2.67, 3.27) — 0.60 m |
  | **`-122.3940709, 37.7819871`** | **1.48 m** | **3.73 m** (86–96) | **(1.48, 3.73) — 2.25 m** |

  Use the last row as the **registry** point and **`exclude: 2.6`** — 1.12 m of
  margin below and 1.13 m above, the widest band available anywhere near this
  building and more than double what the manifest anchor would give. It is only
  **0.84 m** from the manifest anchor, on a bearing of 344° (just west of north);
  the two points are deliberately different, which is allowed and is what the
  `540/541/542/543 Presidio` and `106 South Park` plans set the precedent for.

  The full trigger table from that registry point:

  | Polygon | Triggers at | Via |
  |---|---|---|
  | this building, OSM `way/113545687` (Overture proxy) | **1.47 m** | its centroid |
  | this building, DataSF SF3775055 (201006.0028685) | **1.48 m** | its centroid |
  | 86–96 South Park (SF3775116 / 201006.0022147) | **3.73 m** | nearest ring vertex |
  | 76–82 South Park (SF3775054 / 201006.0026693) | 3.86 m | nearest ring vertex |
  | OSM `way/113545685` (untagged, on the 86–96 lot) | 4.36 m | nearest ring vertex |
  | 76–82 South Park, OSM `way/124884340` | 4.89 m | nearest ring vertex |
  | this lot's 16 m² rear structure (201006.0168103) | ~14 m | nearest ring vertex |

  Note the last row: at `exclude: 2.6` the **rear structure survives the bake**,
  which is correct — it is a real 8 m outbuilding and the asset models its own
  version of it. Watch for a double at QA; if the baked one and the modelled one
  both appear, the fix is to model the rear structure *out* of the GLB, not to widen
  the radius past 3.73 m and lose a neighbour.

  Confirm against the real `pipeline/data/overture_buildings.geojsonseq` at
  integration time — the table above uses OSM as a stand-in — and prove the outcome
  with `pipeline/verify-rebake.mjs`: exactly two footprints dropped in this cell
  (the DataSF and Overture traces of 84), no neighbour lost.

- **`exclude` is also the tree-clear and street-furniture radius.** At 2.6 m it
  clears neither, which is correct: the large street tree in front of this building
  is real and is in every photograph of it. Do **not** set `clearTrees: true`.

- `loadRadius`: the default formula gives `max(2500, 13.2 × 30) = 2500` m. Take the
  default.

- **Camera preset.** In `app/src/camera.js` the rig places the camera at
  `(sin(yaw), sin(pitch), cos(yaw)) × distance` from the pivot, and the project's
  `+z` is **south**, so `yaw: 45` puts the camera south-east of the building looking
  north-west at its street elevation — the only view of this building worth flying
  to. Start from `camera: { distance: 150, yaw: 45, pitch: 26 }` and tune against
  the live scene. `106SouthPark` uses the same convention; `165SouthPark`'s preset
  reads as the opposite one and is the odd entry, not this.

- **This is the twentieth South Park rim building to enter the manifest by hand, and
  it does not earn the bespoke route on merit.** 84 South Park has no designation,
  no architect, no published history and no cultural claim; what it has is a
  distinctive contemporary front and a good roof. The honest reading is that this
  oval has now been finished by hand and the argument 165 and 106 both made has
  come due: the next building on this rim, and any similar row anywhere in SoMa,
  belongs to `KIT-INTEGRATION-PROMPT.md`. Say so in the integration report.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Bounding-box top exactly 13.20 m — and it is the **pergola beams** that reach
      it, not the parapet (loader scale lands at 1.0)
- [ ] Parapet crest at 11.50 m, roof deck at 11.20 m
- [ ] Dimensions plausible in meters and consistent with 2.1 (XY bbox ~26.2 × 26.2 m
      is expected for a 6.99 × 30.07 m building at 45°)
- [ ] Frontage 6.99 m and depth 30.07 m, not rounded toward a squarer plan
- [ ] Green wall and projecting box on the **south-west** bay, entrance and terrace
      on the **north-east** bay (not mirrored)
- [ ] The rear light well is a real hole through the roof plane with a floor at
      8.10 m, not a decal
- [ ] Skylights present and asymmetric: four on the south-west side, three on the
      north-east side
- [ ] The pergola is **open** — roof deck visible between its beams from directly
      above
- [ ] Neither party-wall flank carries any treatment or opening
- [ ] Triangles at or under 7,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`; any
      off-palette body colour recorded and justified in `REPORT.md`
- [ ] `_Glow` only on two windows and the entrance recess; glow shells proud of the
      opaque glazing, never a closed shell around a primary surface
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (per-object signed
      volume for the union of solids; ray test residual ≤ 0.15%)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + the square-on 135.2° facade view + the 3× roof view +
      contact sheet + night render, all regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

1. **The assessor record describes a building that stopped existing in 1994.** Two
   storeys, 22 rooms, 7 bathrooms, `SRES`, 4,462 sq ft — that is the 1907 rooming
   house, still on the 2025 closed roll. The permit trail (1992 vertical addition,
   `2 → 3`, `$361,782`; 1994 revision; every permit since recorded at 3) and the
   LiDAR (11.36 m median, far too tall for two storeys of 1907 wood frame) both say
   three. **A modeller who trusts the assessor will build a two-storey building.**
   This is the single likeliest way to get this asset wrong.
2. **The pergola is unconfirmed and it sets the target height.** See 2.9. 13.20 m
   versus 11.50 m is a 15% scale difference across the whole asset, so this is not a
   detail decision — it is the first thing to settle and the last thing to
   re-check before export.
3. **There is no documentary source for this building at all.** No nomination, no
   architect, no survey, no publication, and the only real-estate record found (the
   1990 Grubb sale) carries no photographs. Everything in 2.4 is read from one
   January 2025 Street View capture and one Bing aerial. Compare that with 106 South
   Park, whose National Register nomination described all four elevations in
   survey-grade prose. **This plan's facade description is the weakest in the set**,
   and the executing agent should expect to correct it rather than confirm it.
4. **The facade colour is read from a shaded, tree-obscured, north-east-facing wall
   in January.** The *relation* is confident — a tinted blue-green body against a
   pale projecting box, a rust-red door, a green panel. The hue and value are not.
   See 2.8, and expect to go off-palette.
5. **OSM and DataSF disagree about where the building is by 2.7 m**, and the parcel
   is the only survey among the three. The disagreement is explicable (the LiDAR
   footprint stops at the light well, OSM traces the lot) but it means the anchor is
   a judgement and not a measurement, and it is why 2.13 needs a separate registry
   point and a verified re-bake rather than a copied radius.
6. **No historic designation was found, and absence of evidence is not evidence of
   absence.** South Park has been repeatedly surveyed and the rim contains
   NR-eligible buildings on either side of this one. If a district or survey listing
   turns up, it changes nothing geometric but it changes the card copy — describe
   the building as undesignated only for as long as that holds.
7. **The 16 m² rear structure is modelled from two LiDAR numbers and nothing else.**
   Its footprint area, its 7.99 m roof height and its position on the lot are
   measured; its form, material and whether it is even a separate building rather
   than a lower rear wing of the main one are inferred. It is visible in the app
   only from directly above and obliquely, so the risk is bounded — but see the
   double-bake warning in 2.13.
8. **The four-plus-three skylight count is read off 0.118 m/px imagery.** The
   asymmetry is clear; the exact counts are not. Getting 4/3 wrong by one either way
   costs nothing; getting the *asymmetry* wrong turns a designed roof into a
   symmetrical one and is worth the extra look.
