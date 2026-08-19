# 246 Ritch Street — SF-SIM asset plan

A 2014 five-storey, nineteen-unit apartment building on the south-west side of Ritch Street,
mid-block between Bryant and Brannan. It is the newest and by far the tallest thing on this
block face: 15.87 m of cream stucco standing eight metres proud of the two-storey timber
houses at 248–250 and 252–254 Ritch next door, on a lot that was a roofless derelict
warehouse until 2011.

Its identity is one device, repeated: **twelve cantilevered, near-black perforated-metal
balcony boxes in a staggered grid across a pale front**, over a **charcoal ground-floor base**
holding a restaurant, a recessed lobby and a white sectional garage door. Nothing else in
SoMa's alley fabric looks like it, and the whole recognition problem is that grid — get the
stagger and the black-on-cream contrast right and the building reads instantly from the
aerial camera; make the balconies flush or grey and it becomes an anonymous white box.

Its Ritch Street neighbours `500-third`, `550-third`, `560-third` and `574-third` are already
in the manifest, and `248-ritch` / `254-ritch` are in flight in parallel sessions on the two
lots immediately south-east. None of them may be mistaken for this one: 246 is the only
modern white-and-charcoal apartment slab on the alley, the only building with projecting
metal balconies, and the only one over 11 m.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/246-ritch/`. This document is the plan only: Part 1 is the runnable task prompt,
Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `246-ritch` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3958481, 37.7802253` |
| Target height | **18.76 m** to the roof stair/elevator penthouse crest; main parapet **15.87 m** |
| Footprint | 16.68 m (Ritch Street frontage, NE) x 22.70 m (depth, NW–SE); 378.5 m2, measured |
| Triangle cap | 9,000 |
| Category | `2` (Apartments) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 246 Ritch Street GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of 246 Ritch Street in San Francisco and deliver it
as a downloadable, validated GLB.

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
7. `artifacts/500-third/` — the nearest reference implementation in site and method (the same
   alley, the same 45° heading, one block north-west, and the asset whose build script's
   `E_RITCH` comment is the control that validated this plan's street-side measurement). Read
   it for the *method*, not the *look*: 500 Third is a 26.5 m brick-and-steel loft, 246 Ritch
   is a 15.9 m cream stucco apartment slab with black metal balconies. They must not read as
   siblings.
8. `docs/asset-plans/246-ritch.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Must capture

- A **single clean five-storey slab** on a 45°-rotated mid-block lot, 16.68 m of Ritch Street
  frontage by 22.70 m deep, filling its lot wall to wall
- **Twelve cantilevered, near-black perforated-metal balcony boxes** on the Ritch Street
  front — three per floor on floors 2, 3 and 4, **horizontally offset floor to floor** so
  they read as a staggered grid rather than three stacked columns. This is the building's
  entire identity; see "Research" below, the row/column count is the one thing in this
  dossier that must be re-confirmed before modelling
- The **cream-and-charcoal panelled field**: warm off-white stucco piers and spandrels with
  **charcoal-grey recessed window bays** between them, offset floor to floor so the wall
  reads as an interlocking patchwork rather than a regular grid
- The **charcoal ground-floor base band** to ~3.4 m, under a hard shadow line, holding (left
  to right, looking at the front): the **restaurant/retail glazing**, the **recessed lobby
  entry**, and a **white sectional garage door with a grid of square panels**
- The **flat top floor** — floor 5 carries the same window rhythm but **no balconies**, so the
  silhouette is a clean parapet, not a stack of boxes
- A designed flat roof: the parapet ring with a dark coping band, the **stair/elevator
  penthouse** that sets the 18.76 m crest, a recessed lightwell/roof-deck, and a small
  mechanical cluster

## Research 246 Ritch Street independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- The Ritch Street elevation (north-east) and the exposed upper parts of both flanks
- Aerial and roof/top views (the penthouse, the lightwell, mechanical units)
- Ground-level views, particularly the base band, the lobby and the garage door
- Day and night appearance
- **The balcony grid — rows, count per row, and the horizontal offset between floors.** The
  dossier's reading of *three rows of three, floors 2–4, top floor flush* comes from one
  rectified panorama (2.3) and one aerial; two street trees planted with the project screen
  the front in every recent capture. Re-confirm before modelling. **Use the historical Street
  View panoramas** — `1EVAdp1_sD5des1l6a3eeQ` and `2dq2zz3CSqlPIJQRF03q4Q` are pre-canopy and
  show the whole facade; the current capture does not
- Whether the **rear (south-west) elevation** carries balconies too — the nadir aerial shows a
  second row of dark rectangles along that edge and the dossier treats it as probable but
  unconfirmed

Prefer architect/engineer publications, owner or institutional material,
planning and permitting documents, architectural press, geolocated photography,
and aerial/satellite imagery. Never rely on a single photograph, a single
AI-generated image, or a single unsourced 3D model. Separate verified facts from
visual inference; if sources disagree, document the disagreement and decide.

**Four source traps are already known and resolved in 2.1 — re-check them, do not silently
re-inherit the wrong value:**

1. **The address resolves to twenty parcels and no addressed OSM way.** Nominatim returns a
   *restaurant node* (Wabi-Sabi SF, node 10874867132), not a building. The building is
   condominium lots 3776/456 through 3776/475, all sharing ONE parcel polygon, and the
   footprint is OSM way **1174904714**, which carries `building=yes` and no address at all.
   Lot 456 also carries the address **240 Ritch** (the ground-floor commercial space) — that
   is the same building, not a neighbour.
2. **`hgt_maxcm` (18.76 m) is not the parapet.** The LiDAR footprint's height standard
   deviation is 3.84 m over a 3.99–18.76 m range — a multi-level footprint. The parapet is
   the median, 15.87 m; 18.76 m is the roof penthouse and it is the *bounding-box top*, so it
   is the manifest `targetHeightM`. Do not build a 19 m parapet.
3. **There is no `height` tag anywhere to inherit, and no Wikidata entry.** The only
   published architectural height is the entitlement's "five-story, 50-foot-tall" (15.24 m),
   which is the zoning height to the roof, not to the parapet and not to the penthouse.
4. **The 2010 LiDAR survey saw a vacant lot here** (`p2010_zminn88ft` and `p2010_zmaxn88ft`
   are both 0). The `hgt_*` statistics come from the later SF16 survey and *do* describe the
   current building, which completed 6 February 2014. Check any other height source's vintage
   against that date before believing it.

## Create a reference dossier

Write `artifacts/246-ritch/REFERENCE.md` containing: source links and what each
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
landmark: clear massing, one strong facade rhythm, a simple designed roof, and exactly two
identity cues carried hard — the staggered black balcony grid and the charcoal base under a
pale body. The balcony screens are **perforated in reality and must not be perforated in the
model**: a solid panel with two or three shallow slot reveals reads as the same object at the
app's camera distance and costs a twentieth of the triangles (style bible §4, §26).

The finished asset must be immediately recognizable as 246 Ritch Street, consistent with
the real building from all four sides and above, architecturally credible, and a
premium handcrafted miniature — not photorealistic, not voxel art, not generic
low-poly, and never accurate in one view while invented in the others.

## Scope of the exported asset

Export the single building: stucco body, parapet, the Ritch Street elevation with its
balconies and openings, the exposed upper parts of both flanks, the rear elevation, the
charcoal ground-floor base with its restaurant glazing, lobby and garage door, and the roof
furniture.

Do not include unrelated surrounding city geometry: Ritch Street, the three street trees in
front of the building, 248–250 Ritch, 252–254 Ritch, 230/236 Ritch, the Zoe Street buildings
behind, the sidewalk, parked cars, people, plinths, cameras or lights. The restaurant's
awning, A-board, planters and sidewalk seating are tenant fit-out and must not be modelled.
Temporary context may appear in review renders but must not leak into the GLB.

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
(`placeGeneric` in `app/src/assets.js` only scales and positions). The Ritch Street front
faces **north-east, bearing 45.0°**; the building is rotated roughly 45° off the world axes,
so build directly on the measured footprint polygon in 2.3 rather than modelling an
axis-aligned box and rotating it. Record the measured heading in `REPORT.md`.

**Height normalization:** the tallest geometry in the export (the roof penthouse) must
land at exactly **18.76 m** so the loader's `targetHeightM / measuredHeight` scale is 1.0.

## Reproducible Blender workflow

Blender 5.2 LTS. Headless: `blender -b --python script.py -- args`.

Keep `artifacts/246-ritch/build_246_ritch.py` (deterministic build script),
`artifacts/246-ritch/246-ritch.blend`, and `artifacts/246-ritch/246-ritch.glb`.
The script must rebuild the model reliably enough for future revision. Do not modify or
rename an unrelated existing GLB to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`246-ritch-top.png`, `246-ritch-north.png`, `246-ritch-east.png`,
`246-ritch-south.png`, `246-ritch-west.png`, plus `246-ritch-contact-sheet.png`,
at least one high three-quarter aerial beauty render `246-ritch-aerial.png`, and a
night render `246-ritch-aerial-night.png`.

The four elevations must share scale, framing, lighting, exposure and
projection; use orthographic or long-lens cameras; label directions from the
researched orientation; the top view must clearly show the parapet ring, the penthouse, the
lightwell and the mechanical cluster; the aerial view uses the style bible's camera
assumptions (30-50 degrees down, long lens). Simple tabletop lighting, neutral warm
background, minimal depth of field, and every image must depict the same exported model.

Aim the hero aerial from the **north-east**, so the Ritch Street front, the balcony grid and
the roof are all in frame at once — that is the view the app's camera actually gets, and the
two flanks are largely buried against neighbours.

## Validate the exported GLB

Re-import `246-ritch.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture
count, camera count, light count, animation count, applied-transform status,
negative-scale status, normal-orientation status, unexpected geometry, and
per-material contract compliance. Render at least one review image from the
re-imported asset. Write `artifacts/246-ritch/validation.json` and
`artifacts/246-ritch/REPORT.md`.

Note that the axis-aligned XY bounding box will be roughly **27.9 x 27.9 m** even though the
building is 16.7 x 22.7 m — that is the expected consequence of a ~45° real-world heading,
not a scale error.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "246-ritch",
  "file": "246-ritch.glb",
  "anchor": [
    -122.3958481,
    37.7802253
  ],
  "targetHeightM": 18.76,
  "cat": 2,
  "name": "246 Ritch Street",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a separate, explicitly requested job — run `docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in `docs/asset-plans/246-ritch.md`.
````

---

## Part 2 — Research and design dossier

Compiled 18 August 2026 from the sources in 2.2. Values marked *inferred* are visual or
derived estimates, not published figures — the executing agent must re-verify
anything it relies on.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Built | **completed 6 February 2014**; permit filed 5 January 2007 | DBI permit `200701051074` (`completed_date 2014-02-06`); assessor roll `year_property_built 2014` |
| Storeys | **5** | permit `200701051074` "to erect a new 5 story 19 dwelling unit"; every later permit repeats `5`; the DataSF unit list runs `#101`, `#201–205`, `#301–305`, `#401–404`, `#501–504` — floor prefixes 1 through 5 |
| Units | **19 dwellings** plus one ground-floor commercial space | permit `200701051074`; DataSF addresses (19 unit numbers) |
| Use | Apartments over ground-floor restaurant; 4 car spaces + 1 car-share + 6 bicycle spaces in a ground-floor garage | 2009 preliminary mitigated negative declaration (via SocketSite); permit `202111122308` (2021) "change of use from limited restaurant to full restaurant" |
| Ground-floor tenant | **Wabi-Sabi SF** (restaurant), addressed 246 Ritch; the space was permitted as 240 Ritch, a retail bakery, in 2014 | OSM node 10874867132; permits `M475367`, `201405095355`, `202111122308` |
| Previous building | A 4,130 sf single-storey warehouse "in very poor structural condition… does not contain a roof or north-facing wall"; demolished under permits `200701051070` / `201011164996`, completed 3 January 2011 | 2009 preliminary MND; DBI permits |
| Block / lot (APN) | 3776 / **456–475** (twenty condominium lots on one parcel polygon); the pre-condominium lot was 3776/092 | DataSF parcels (`acdm-wktn`); DataSF addresses (`ramy-di5m`); assessor roll |
| Lot area | **4,130 sq ft = 383.7 m2** | 2009 preliminary MND (twice); parcel polygon 16.7 x 23.9 m = 399 m2 |
| Gross floor area | ~16,442 gsf, of which 8,690 gsf common/circulation/garage/storage | 2009 preliminary MND |
| Footprint | **378.5 m2**; **16.68 m** (Ritch frontage, NE) x **22.70 m** (depth) | OSM way/1174904714, reprojected and reduced to its oriented bounding box — **measured**. Eight vertices, all within 0.05 m of a clean rectangle |
| DataSF footprint (cross-check) | 395.4 m2 (`mblr = SF3776456`, `sf16_bldgid 201006.0009413`) | 4.5% over the OSM ring, which is the balcony overhang at the front and ~1 m of reach at the rear |
| Roof deck / parapet | **15.87 m** above ground (`hgt_median_m`); modal cell 15.72 m | DataSF LiDAR — **measured** |
| Maximum feature height | **18.76 m** above ground (`hgt_maxcm`) | DataSF LiDAR — **measured**; read as the stair/elevator penthouse, see 2.15 risk 1 |
| Published height | "five-story, **50-foot-tall**" = 15.24 m | 2009 preliminary MND, quoted in SocketSite; this is the zoning height to the roof — parapet + 0.6 m lands on the LiDAR median |
| Photogrammetric parapet | **15.0 ± 1.0 m** | rectified from Street View pano `1EVAdp1_sD5des1l6a3eeQ` (2.3) — *independent, and consistent with both the 15.24 m entitlement and the 15.87 m LiDAR* |
| Height standard deviation | 3.84 m over 1,581 cells, range 3.99–18.76 m, mean 14.61 m | DataSF LiDAR. A three-level fit (15.87 m over 82%, 18.76 m over 5%, ~4.5 m over 13%) reproduces mean 14.61 and sd 3.88 — see 2.15 risk 2 |
| Ground elevation | 4.85 m min / 5.43 m median (NAVD88) | DataSF LiDAR `gnd_min_m` / `gnd_mediancm` — app terrain handles this, not the asset |
| Zoning | SLI (Service/Light Industrial) at entitlement, **55-X height and bulk district** | 2009 preliminary MND |
| Frontage heading | Ritch Street front faces **45.0°** (NE); rear 225.0° (SW); north-west party wall 315.0°; south-east party wall 135.0° | measured from the footprint polygon and cross-checked against DataSF street centrelines (2.3) |
| Exposed elevations | **one fully** (NE, Ritch Street) plus the upper parts of both flanks and the rear | measured against the neighbour footprints — see 2.4 |
| Street trees | **three**, planted with the project, along the Ritch Street frontage | 2009 preliminary MND; visible in every capture since 2015 and now large enough to screen the facade |
| Architect | *unconfirmed* — "Edmund Lai" and "D and S Leong Associates / David Leong" recur in the permit-agent records | checkpermits.com aggregation of DBI records — **treat as a lead, not a fact** |

### 2.2 Sources

- https://www.openstreetmap.org/way/1174904714 — the footprint, `building=yes`, **no address
  tags at all**. This is why the address does not geocode to a building; identification runs
  address → DataSF parcel APN → parcel polygon → the footprint inside it
- OSM node 10874867132 — `Wabi-Sabi SF`, `amenity=restaurant`, `addr:housenumber=246`. What
  Nominatim actually returns for "246 Ritch Street"; a point, not a building
- `https://data.sfgov.org/resource/ramy-di5m` (DataSF Addresses with Units) — 39 rows for
  246 Ritch: twenty condominium lots `#1–#20` on lots 456–475, and nineteen dwelling unit
  numbers `#101`, `#201–205`, `#301–305`, `#401–404`, `#501–504`. **The unit numbering is the
  cleanest proof of the storey count in the whole dossier**
- `https://data.sfgov.org/resource/acdm-wktn` (DataSF Parcels) — lots 456–475 all carry the
  *identical* polygon; lot 456 has `from_address_num 240`, `to_address_num 246`
- `https://data.sfgov.org/resource/ynuv-fyni` (DataSF Building Footprints, LiDAR-derived) —
  `SF3776456` / `sf16_bldgid 201006.0009413`: 395.4 m2, 15.87 m median, 18.76 m maximum,
  3.84 m standard deviation, and `p2010_zminn88ft = p2010_zmaxn88ft = 0` (nothing standing in
  the 2010 survey)
- `https://data.sfgov.org/resource/wv5m-vpq2` (SF Assessor Historical Secured Property Tax
  Rolls) — 2014, twenty condominium records: one `CZ` Commercial Store Condo (477 sq ft, the
  ground-floor restaurant) and nineteen `ZEU` Condominium Economic Units of 393–453 sq ft,
  totalling 8,387 sq ft. The per-unit areas corroborate the MND's "about 350 sf" studios
- `https://data.sfgov.org/resource/i98e-djp9` (SF Building Permits) — `200507288914` (2005,
  temporary shoring of the old warehouse), `200701051070` and `201011164996` (demolition),
  **`200701051074`** (the building: 5 storeys, 19 units, completed 2014-02-06),
  `201210172241` / `201306260540` / `201308094016` (sprinklers and fire alarm, all naming
  "5 story / 19 units" and one describing "new 19-unit plus commercial space condominium"),
  `M475367` and `201405095355` (the 240 Ritch retail bakery fit-out), `202111122308` (2021
  restaurant conversion)
- https://socketsite.com/archives/2009/08/from_sli_to_sro_for_246_ritch_street_as_proposed.html
  — quotes the **preliminary mitigated negative declaration** in full: 4,130 sf site, "a new
  five-story, 50-foot-tall building with 19 Single Room Occupancy (SRO) residential units
  totalling approximately 16,442 gross square feet", ~350 sf per unit, 8,690 gsf of
  common/circulation/garage/storage, a ground-floor garage of four spaces plus one car-share
  and six bicycle spaces, three new street trees, SLI zoning, 55-X height and bulk. **The
  primary source for height, storeys, unit count and programme.** The units were built as
  ordinary dwellings rather than SROs — the permit says "19 dwelling unit"
- https://socketsite.com/archives/2012/09/five_stories_and_nineteen_studios_ready_to_rise_at_246.html
  — September 2012, the lot excavated; repeats "five-story, 50-foot tall building with 19
  residential units"
- https://www.ritchstreet.com/ and https://www.marketapts.com/apartment-ritch-street-san-francisco-ca/NTEx
  — the building's own leasing sites, as **Ritch Street**: "floor to ceiling windows, radiant
  floor heating, white washed oak hardwood floors, designer kitchen with Grohe fixtures", plus
  "Balcony/Patio", "Covered Parking". Listing photography — label anything taken from it
  *observed (listing photo)*
- https://www.loopnet.com/Listing/246-Ritch-St-San-Francisco-CA/24073682/ — "246 Ritch at
  South Park", 16,150 SF, café/food-service space for lease (the ground floor)
- Google Street View, Ritch Street. **Current captures are useless for the facade** — the
  three project street trees have grown into a continuous canopy. Use the historical panos:
  `1EVAdp1_sD5des1l6a3eeQ` (the widest clear view of the whole front),
  `2dq2zz3CSqlPIJQRF03q4Q` (sharpest colour, shows the "246" plate, the lobby and the garage
  door), `KLsu2PG4b6fG4R2Q--CCYw` (current, labelled "240 Ritch St"),
  `Ygw6B2E0AIVV9jLc04IjdQ` (oblique from the south-east, shows the balcony boxes in relief),
  and `3Z7LwIFTgVxxujqZ-y0Jpw` / `OVPKMbexU_SjneNgsAJ2rw` (the vacant lot, pre-2011 — useful
  only for confirming that the whole building post-dates the 2010 LiDAR)
- Google Maps satellite z22 (Vexcel, 2026) — cream membrane roof, continuous parapet, a raised
  light-coloured penthouse block near the centre casting a clear shadow, a recessed
  cross-shaped lightwell/deck around it, scattered mechanical units, and the balcony boxes
  legible in plan along the north-east edge
- `pipeline/data/streets_datasf.geojson` — the street-side measurement (2.3)
- Consulted and **not used**: Nominatim's geocode of "246 Ritch Street" (returns the
  restaurant node, not a building); the Accela planning records `08HIS-0229P` and
  `13HIS-0032X` (project review and letter of determination, no design content online)

### 2.3 Orientation and placement

The building sits mid-block on the **south-west side of Ritch Street**, between Bryant
(north-west) and Brannan (south-east), one lot north-west of 248–250 Ritch and one lot
south-east of 236 Ritch. Like the whole SoMa grid it is rotated about 45° from the world axes.

**Street side, measured** — perpendicular offsets of the DataSF street centrelines from the
anchor, bucketed by `streetname`:

| Street | Distance | Bearing from anchor |
|---|---|---|
| **Ritch St** | **17.9 m** | **45.1°** (north-east) |
| Zoe St | 39.6 m | 225.1° (south-west) |
| Welsh St | 44.2 m | 251.5° |
| 3rd St | 84.9 m | 45.1° |
| Bryant St | 86.9 m | 315.2° |

The same script run against the already-shipped `500-third` anchor returned 3rd Street 45.2°,
Bryant 315.3°, **Ritch 225.1°** — exactly what `artifacts/500-third/build_500_third.py`'s
`E_THIRD` / `E_BRYANT` / `E_RITCH` comments say, which is the control that makes this
measurement believable. 500 Third and 246 Ritch face each other across the alley and therefore
carry **opposite** normals (225° and 45°); that is agreement, not contradiction.

Measured footprint polygon, in Blender coordinates (metres, `+X` east, `+Y` north),
clockwise, already centred on the anchor `-122.3958481, 37.7802253`:

```
(  2.19,  13.87)     north corner
( 13.98,   2.07)     east corner   } two 0.5-0.8 m jogs on the run between them
(-13.98,  -2.07)     south corner
(-13.98,   2.07)  -> west corner at (-13.98, 2.07)
```

more precisely, the eight surveyed vertices (metres from the anchor, `+X` east, `+Y` north):

```
( 2.19,  13.87)   ( 13.98,   2.07)   ( 13.49,   1.59)   (  8.86,  -2.97)
( 8.25, -3.57)    (  3.68,  -8.09)   ( -2.18, -13.87)   (-13.97,  -2.07)
```

The two sub-metre jogs on the south-east run are survey noise on a party wall; four corners is
the honest simplification.

Edges, with outward normals:

| Edge | Length | Faces | Elevation |
|---|---|---|---|
| north corner -> east corner | **16.68 m** | NE 45.0° | **Ritch Street front** |
| east corner -> south corner | **22.70 m** | SE 135.0° | south-east party wall (248–250 Ritch) |
| south corner -> west corner | **16.68 m** | SW 225.0° | rear elevation |
| west corner -> north corner | **22.70 m** | NW 315.0° | north-west party wall (230/236 Ritch) |

Because of the 45° heading the axis-aligned bounding box is ~27.9 x 27.9 m. That is correct.

**Photogrammetric check.** Pano `1EVAdp1_sD5des1l6a3eeQ` sits 7.86 m out from the facade plane
and 9.14 m along it from the north corner. Reprojected to a metric elevation (equirect,
horizon at the centre row, camera 2.5 m), the parapet lands at **15.0 m**, the ground-floor
base band at **3.3 m**, and the three balcony rows at deck heights of roughly 3.5, 6.6 and
10.4 m. The dominant error is the assumed camera distance — `dh/dD = tan θ ≈ 1.8` at the
parapet — so quote this as **15.0 ± 1.0 m** and prefer the LiDAR median for the model.

### 2.4 What each side shows

**North-east (Ritch Street front)** — The hero elevation and effectively the only designed
one, 16.68 m wide and 15.87 m tall. Reading it bottom to top:

- a **charcoal ground-floor base band** to ~3.4 m, running the full width and reading as one
  dark plinth under the pale body. Within it, left to right as you face the building: the
  **restaurant glazing** (a tall shopfront, the old bakery space, with the white **"246"**
  plate on the pier beside it); the **recessed residential lobby** — a glazed door set back
  about 0.8 m in a charcoal reveal; and a **white sectional garage door** with a grid of
  square panels, roughly 3 x 3, at the south-east end. A red fire-department connection sits
  on the wall between the lobby and the garage;
- **floors 2 to 5** in **warm off-white stucco**, articulated as **vertical piers and
  spandrel panels alternating with charcoal-grey recessed window bays**. The charcoal recesses
  do not line up floor to floor: they step sideways, so the wall reads as an interlocking
  cream/charcoal patchwork rather than a regular grid. Windows are large, white-framed
  aluminium, one or two lights wide, set inside the charcoal recesses;
- **twelve cantilevered balcony boxes** on floors 2, 3 and 4 — three per floor, each roughly
  2.6 m wide, projecting about 0.9 m, with a **near-black perforated metal screen** about
  1.1 m high. The perforation is a scatter of short horizontal slots of varying length, which
  reads as a fine dark texture at any distance the app's camera works at. **They are offset
  horizontally floor to floor**, which is the single thing that makes this facade memorable;
- **floor 5 carries no balconies** — the same window rhythm, flat wall, so the top of the
  building is a clean band under the parapet;
- a **dark coping band** about 0.4 m deep caps the parapet at 15.87 m. There is no cornice, no
  step and no ornament.

**South-east** — Party wall against **248–250 Ritch** (`SF3776105`, a two-storey house,
7.95 m median / 14.27 m maximum, 164 m2). The lower ~8 m is buried; the upper ~8 m stands
clear and is visible from the alley. Oblique panos show it carries a rank of windows and at
least one balcony on the exposed part — build it as body-coloured wall with a modest punched
window rank above ~8 m and nothing below.

**North-west** — Party wall against **230/236 Ritch** (`SF3776144`, 10.75 m median / 17.87 m
maximum, 484 m2). More of this flank is covered; treat it as flat body-coloured wall with at
most a couple of small openings near the top.

**South-west (rear)** — Faces a shallow rear yard (the parcel is 23.9 m deep, the building
22.7 m) and then the Zoe Street lots — `SF3776128` at 14.42 m sits 19.3 m away. Not visible
from any street, but the app's aerial camera sees it obliquely. The nadir aerial shows a
second row of dark rectangles along this edge, which is probably a matching set of rear
balconies; that is *inferred* and is called out in 2.15.

**Top** — A flat cream membrane roof inside a continuous parapet, and the surface the app's
camera sees most:

- a **stair / elevator penthouse** near the centre, a light-coloured block standing about
  2.9 m proud of the parapet and casting a clear shadow in the 2026 aerial. It is what the
  18.76 m LiDAR maximum measures and it is the only thing on this block face that breaks a
  flat roofline;
- a **recessed lightwell / roof deck** around it, reading in plan as a cross-shaped darker
  area. The MND's 16,442 gsf over five floors is ~305 m2 per floor against a 378 m2
  footprint, so roughly 70 m2 of the plan is lightwell — this feature is arithmetic as well as
  observation;
- a scatter of **mechanical units and vents**, mostly toward the north-east half;
- the balcony boxes themselves are legible in plan along the north-east parapet.

### 2.5 Recognition cues (ranked)

1. **The staggered grid of near-black balcony boxes** on a pale front — twelve dark
   rectangles that step sideways floor to floor. Survives to thumbnail size and exists nowhere
   else on the alley
2. **Cream body over a charcoal base**, with the base band at one constant height across the
   whole frontage — a hard horizontal shadow line at 3.4 m
3. **Being the tallest and newest thing on the block face** at 15.87 m: eight metres above
   248–250 (7.95 m) and 252–254 (8.04 m), five above 230 Ritch (10.75 m)
4. The **cream/charcoal interlocking panel patchwork** of the upper wall — offset, not gridded
5. The **rooftop penthouse** at 18.76 m, the only break in an otherwise dead-flat parapet

### 2.6 Miniature translation

**Preserve**

- The single clean slab and its real 45° heading, filling its lot wall to wall
- The balcony grid: count, stagger and near-black value. If triangles have to come from
  somewhere, take them from the window mullions, never from the balconies
- The constant-height charcoal base and its three distinct openings (restaurant, lobby,
  garage)
- The flat top floor — the balconies must stop at floor 4 or the silhouette loses its cap
- The height difference against its two-storey neighbours; this building's job in the street
  is to be the tall one

**Simplify**

- The perforated screens → solid panels with two or three shallow horizontal slot reveals
- Twenty-odd distinct window openings → four bays per floor of one repeated opening
- The window frames → a single pale surround, no mullion grids
- The rooftop mechanical scatter → three clean blocks
- The lightwell → one rectangular recess, not the real cross plan

**Drop**

- The perforation pattern as literal geometry
- The fire-department connection, wall lights, cameras, downpipes, vent grilles
- The restaurant's awning, A-boards, planters and sidewalk seating
- The three street trees (they are the bake's job, not the asset's — and they are real, so the
  registry entry must not carry `clearTrees`)

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not
a straitjacket — adjust after the first aerial review render.

1. Body: extrude the 2.3 footprint from z=0 to z=15.87, `Toy_sand`.
2. Ground-floor base band, z=0 to z=3.40, all four elevations: a `Toy_ink` band flush with
   the wall plane (do **not** project it — see the plinth trap in 2.14). On the **NE**
   elevation only, cut three openings into it:
   - **restaurant glazing** — 5.2 m wide, z=0.35 to 3.05, recessed 0.25 m, `Toy_glass`, with
     a 0.12 m `Toy_trim` surround, starting 0.9 m from the north corner;
   - **lobby** — 2.2 m wide, z=0 to 2.95, recessed 0.8 m, `Toy_glass` door leaf in a
     `Toy_ink` reveal, centred 8.6 m along;
   - **garage door** — 4.6 m wide, z=0 to 3.05, recessed 0.15 m, `Toy_trim` (white) leaf
     scored into a 3 x 3 grid by 0.06 m recessed reveals, 1.1 m from the east corner;
   - the white **"246"** plate, 0.5 x 0.35 m `Toy_white`, on the pier at z=2.6.
3. Upper wall panelling, **NE elevation**, floors 2–5 (floor levels z=3.40, 6.52, 9.64,
   12.76; parapet 15.87 — four floors of 3.12 m):
   - four bays at 4.17 m pitch. In each bay and on each floor, a **charcoal recessed panel**
     (`Toy_slate`, 0.15 m deep) 2.9 m wide x 2.55 m tall, sill 0.35 m above the floor line;
   - the recesses are **offset**: shift the panel horizontally by +0.55 m on floors 3 and 5
     and by -0.55 m on floor 4, so no two floors line up;
   - inside each recess, a `Toy_glass` window 2.4 x 2.1 m with a 0.10 m `Toy_trim` surround.
4. Balconies — **floors 2, 3 and 4 only**, three per floor:
   - deck slab 2.6 x 0.95 x 0.14 m, `Toy_ink`, top face at the floor line, projecting from
     the wall plane;
   - screen 2.6 x 1.10 x 0.07 m, `Toy_ink`, standing on the deck's outer edge, with two
     0.06 x 0.02 m horizontal slot reveals across its face and a 0.05 m `Toy_roofd` cap;
   - two 0.07 m `Toy_ink` returns at the ends;
   - floor 2 at bays 1, 2 and 4; floor 3 at bays 1, 3 and 4; floor 4 at bays 2, 3 and 4 —
     that is the stagger, and it must be re-checked against the panos before it is built.
5. South-east flank, above z=8.0 only: two ranks of the same recessed panel and window,
   3 wide, no balconies. Below z=8.0, flat `Toy_sand` wall — the neighbour buries it.
6. North-west flank: flat `Toy_sand` wall, no openings.
7. Rear (SW): the same four-bay panel rhythm as the front on floors 2–5, `Toy_glass` windows,
   **no** balcony boxes unless the executing agent confirms them (2.15 risk 3).
8. Parapet: follow the footprint, 0.30 m thick, `Toy_sand`, z=15.87 minus 0.75 m up to
   z=15.87, capped by a 0.35 m `Toy_roofd` coping band on its outer face — that dark line
   under the roof edge is visible in every photograph and is what stops the top of the model
   reading as a bare extrusion.
9. Roof membrane at z=15.12 (0.75 m below the parapet top), `Toy_steel`. **Not `Toy_roofd`** —
   see 2.14.
10. Roof furniture:
    - **penthouse** 5.6 x 4.2 m, z=15.12 to **z=18.76**, `Toy_sand` walls with a
      `Toy_steel` cap — this sets the bounding-box top and must land exactly on 18.76;
    - **lightwell recess** 7.0 x 4.5 m, 0.9 m deep, `Toy_slate`, immediately south-west of
      the penthouse;
    - three **mechanical blocks** 1.6 x 1.1 x 0.8 m, `Toy_steel`, on a 0.2 m `Toy_roofd`
      plinth, clustered toward the north-east half;
    - one **roof hatch** 1.2 x 0.9 x 0.35 m, `Toy_roofd`.
11. Bevel 0.12 m, 2 segments.

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette except where noted.

| Material | Hex | Used for |
|---|---|---|
| `Toy_sand` | `#ece4d4` | the stucco body on all four elevations, parapet, penthouse walls |
| `Toy_slate` | `#5d646d` (off-palette) | the charcoal-grey recessed window bays and the roof lightwell |
| `Toy_ink` | `#3a3530` | the ground-floor base band, the lobby reveal, and every balcony deck and screen |
| `Toy_glass` | `#2a4d73` | all windows and the restaurant/lobby glazing |
| `Toy_trim` | `#f3efe6` | window surrounds, the garage door leaf, the restaurant shopfront surround |
| `Toy_steel` | `#9aa0a6` | roof membrane, penthouse cap, mechanical blocks |
| `Toy_roofd` | `#45454a` | the parapet coping band, balcony screen caps, roof hatch, mechanical plinth — **small dark props only** |
| `Toy_white` | `#f7f4ec` | the "246" plate |
| `Toy_glass_Glow` | `#2a4d73` | lit residential windows at night |
| `Toy_trim_Glow` | `#f3efe6` | the lit restaurant and lobby band at night |

One palette extension, with precedent (`380-brannan` and `181-south-park` both extended with
`Toy_slate`, `140-south-park` with `Toy_olive`, `340-brannan` with `Toy_sage`), a WARN and not
a FAIL under the contract:

- **`Toy_slate` ≈ `#5d646d`.** The recessed bays are a mid-dark blue-grey, clearly lighter
  than the balconies and clearly darker than the body. `Toy_roofd` (`45454a`) is too dark and
  will merge with the balcony boxes — the whole patchwork disappears; `Toy_steel` (`9aa0a6`)
  is too light and the recesses stop reading as recesses; `Toy_ink` (`3a3530`) is the balcony
  colour and using it here destroys cue 1. Note that the repo already carries three different
  `Toy_slate` values (`39434f`, `6f7883`, `a7b3bc`) in different plans — pick one *for this
  asset*, state the hex in `REPORT.md`, and judge it from the aerial render against the cream
  body and the black balconies, which is the only comparison that matters.

Do **not** use `Toy_roofd` for the roof membrane — see 2.14.

**Night state (required).** Glow surfaces must be thin shells proud of the opaque glazing —
the app renders `_Glow` in a separate unlit layer at ~12% alpha per layer by day, and a closed
shell crosses two layers, so it reads at roughly 23%; a primary surface must never be authored
as glow. Hero glow: the **ground-floor restaurant and lobby**, a wide warm band under the
dark base band — this building's night identity is a lit restaurant at the bottom of a dark
alley, and it is the exact inverse of its daytime dark plinth. Supporting accents: **six or
seven lit residential windows** scattered across floors 2–5 of the Ritch Street front, never
all twenty, and never a whole floor. The balconies, the parapet, the penthouse and the roof
furniture do not glow.

### 2.9 Top surface

A flat roof 16 m up, in a district the camera flies over constantly, on a block face where
every other roof is 8–11 m — so this roof is both the highest and the most exposed thing here.
It has three pieces of real content: the penthouse that sets the model's height, the lightwell
recess, and a small mechanical cluster. Keep the parapet ring continuous so the deck never
reads as an open tray, keep the mechanical cluster to three blocks in one group rather than
scattered, and get the separation from *value* — a `Toy_steel` membrane against `Toy_sand`
parapet walls and a `Toy_slate` lightwell — not by darkening the membrane.

### 2.10 Scope

**In the GLB:** the single building — stucco body, parapet and coping, the Ritch Street
elevation with its twelve balconies and all openings, the charcoal base band with restaurant,
lobby and garage door, the "246" plate, the exposed upper parts of both flanks, the rear
elevation, the roof membrane, penthouse, lightwell and mechanical cluster

**Not in the GLB:** Ritch Street, the three street trees, 248–250 Ritch, 252–254 Ritch,
230/236 Ritch, the Zoe Street buildings, the rear yard, the sidewalk, the restaurant's awning,
A-boards, planters and seating, the fire-department connection, vehicles, people, plinths,
cameras or lights

### 2.11 Triangle budget

Cap 9,000 — a secondary building whose cost is concentrated in twelve repeated balcony boxes.
Suggested split: body, flanks, rear and parapet ~1.5k; upper window bays (four floors x four
bays on the front, plus the rear and the exposed flank) ~2.5k; the twelve balconies ~2.5k
(≈200 each: a deck, a screen with two slot reveals, two returns, one cap); the ground-floor
base band with restaurant, lobby, garage door and plate ~1.5k; roof furniture ~1k.

If the balconies overrun, cut the slot reveals before cutting balconies — the count and the
stagger carry the identity, the slots do not.

### 2.12 Draft manifest entry

```json
{
  "id": "246-ritch",
  "file": "246-ritch.glb",
  "anchor": [
    -122.3958481,
    37.7802253
  ],
  "targetHeightM": 18.76,
  "cat": 2,
  "name": "246 Ritch Street",
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

- **New landmark, Case B.** Add a `pipeline/lib/landmarks.mjs` entry (`id: '246Ritch'` — that
  is what `camelId()` in `app/src/assets.js` produces from `246-ritch`, since digits do not
  start a segment; get it wrong and the procedural block is never hidden and there is no
  warning), `lon: -122.3958481`, `lat: 37.7802253`, `height: 18.76`, `exclude: 5.3`,
  `camera: { distance: 130, yaw: 135, pitch: 26 }`, and re-bake the affected tiles, or the
  baked procedural building on this exact footprint will intersect the GLB.
- **Exclusion radius, measured.** `excluded()` in `pipeline/buildings.mjs` drops a footprint
  when its **area centroid or any ring vertex** falls inside the radius. Measured from this
  anchor against *both* bake inputs, with the bake's own `simplifyRing(0.6)` and
  `ringCentroid()` applied first:

  ```
    0.01 m  Overture  0e69af6c-…  (this building, the OSM trace, 379 m2)   <- must go
    1.69 m  DataSF    SF3776456   (this building, 394 m2)                  <- must go
    8.89 m  Overture  d280b71a-…  (248-250 Ritch, 101 m2)                  <- must survive
   11.10 m  DataSF    SF3776105   (248-250 Ritch, 167 m2)                  <- must survive
   12.71 m  DataSF    SF3776144   (230/236 Ritch, 484 m2)                  <- must survive
   14.03 m  Overture  2259b5ef-…  (230/236 Ritch, 472 m2)                  <- must survive
  ```

  The safe window is **(1.69, 8.89) m** — 7.2 m wide, which is unusually generous for a SoMa
  party-wall lot. **5.3 m sits dead centre**, 3.6 m clear of the last own-ring trigger and
  3.6 m clear of the first neighbour. Both of this building's rings are dropped by their
  centroids, so do **not** reason "the radius has to cover the building" — the footprint
  reaches 13.98 m from the anchor and that is fine. Do not raise past 7 without re-running
  the check. At 5.3 m the circle is entirely inside the building, so no street furniture and
  none of the three street trees are cleared: the entry must **not** carry `clearTrees`, and
  the trees are real and in every photograph.
- Expect the bake to drop **one** ring per cell, not two: the bake runs DataSF first and
  gap-fills from Overture, so `markOccupied()` has usually already claimed the Overture copy
  of a building DataSF carries. The exclusion still has to cover both, because that is what
  stops the gap-fill re-adding a building into the ground the DataSF drop just freed. Prove
  "no procedural block under my asset" by decoding the tile and measuring penetration depth
  against the real footprint, not from the radius and not from `verify-rebake.mjs`'s per-cell
  counts.
- `loadRadius`: the skill's default formula gives `max(2500, 18.76 * 30) = 2500` m. Take the
  default.
- **Batch mode applies.** `248-ritch` and `254-ritch` are being built in parallel sessions on
  the two lots immediately south-east, and this block already has four integrated siblings on
  3rd Street. Follow "Batch mode" in `docs/asset-pipeline/ADDRESS-TO-ASSET.md`: run the bake
  and do the full QA on it, then `git checkout -- app/public/tiles api/_data` before
  committing, and let `docs/asset-pipeline/BATCH-INTEGRATE.md` bake the city once for the
  whole batch. Before merging, grep the sibling plans for this address — 240 Ritch is *this*
  building's ground floor, not a neighbour, and only one asset per parcel can own the
  exclusion.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Bounding-box top exactly 18.76 m (loader scale lands at 1.0)
- [ ] Dimensions plausible in meters and consistent with 2.1 (XY bbox ~27.9 x 27.9 m expected)
- [ ] Triangles at or under 9,000
- [ ] Materials all `Toy_*`; `Toy_slate` hex recorded in `REPORT.md`; no textures, no alpha
- [ ] No `Toy_body`, no cameras, lights, animation or armatures
- [ ] **Roof membrane is not `Toy_roofd`.** `Toy_roofd` (`45454a`) measured rgb(9,9,12) in the
      running app on a `92-south-park` roof deck — below what the diorama's ambient can lift —
      while `Toy_steel` on the same asset read rgb(94,103,112). Keep `Toy_roofd` for the
      coping band, the screen caps and the hatch, and judge it from the app, not from the
      stage-2 renders where it looks like a reasonable charcoal
- [ ] **The ground-floor base band is flush, not projecting.** If the base stands proud of the
      wall above and the restaurant / lobby / garage layers are dimensioned from the *wall*,
      their outermost layer lands exactly in the base's outer plane and z-fights. Give the
      opening helper a `base_d` defaulting to the base projection (0 here)
- [ ] Night render driven from Base Color, not from the imported emission — glTF writes
      `emissiveFactor = 0` when authored strength is 0, so a re-imported `_Glow` material
      carries default white and every glow surface renders as a white slab. Copy `Base Color`
      into `Emission Color` at strength 1.0, and make sure `fade_glow()` zeroes
      `Emission Strength` for the *day* render as well as dropping alpha
- [ ] Aerial review render inspected from the north-east before the formal rig runs

### 2.15 Open questions and risks

1. **The 18.76 m crest is a penthouse, and that is an inference.** What is measured is the
   LiDAR maximum. It is attributed to a stair/elevator bulkhead because (a) the 2026 nadir
   aerial shows a raised light-coloured block near the roof centre casting a shadow, (b) a
   five-storey, 19-unit building has an elevator and therefore an overrun, and (c) 2.9 m above
   the roof is exactly a bulkhead's height. It is *not* a tree — `peak_1st_m` (23.96 m) minus
   `gnd_min_m` (4.85 m) is 19.11 m, i.e. within 0.35 m of `hgt_max`, so there is no canopy
   over this footprint. If the executing agent finds no penthouse, the target height becomes
   15.87 m and the manifest entry changes; say so loudly rather than modelling a box to fill
   the number.
2. **The 13% of the footprint at ~4.5 m.** The LiDAR sd (3.84 m) and minimum (3.99 m) say
   about 50 m2 of this ring is one storey high. A three-level fit reproduces the published
   mean and sd almost exactly, so the low element is real, but *what* it is — a low rear
   portion inside the building line, or the ring over-reaching onto the rear yard and the
   neighbours' low roofs — is unresolved. The OSM trace (378.5 m2) and the surveyed lot
   (383.7 m2) agree with each other against the LiDAR ring (395.4 m2), which is the reason
   this plan builds on the OSM rectangle. If the rear turns out to step down, model the step;
   do not invent one to explain a statistic.
3. **Rear balconies.** The nadir aerial shows a second row of dark rectangles along the
   south-west edge. They are probably balconies matching the front's, but the rear is not
   photographable from any street and the aerial is off-nadir enough that they could be
   mechanical units on the roof edge. The massing recipe leaves them out; add them only on
   evidence.
4. **The balcony stagger is read from one rectified panorama.** Three rows of three on floors
   2–4 with a flush top floor is what the metric reprojection of `1EVAdp1_sD5des1l6a3eeQ`
   shows across s = 0…13 m of a 16.68 m frontage, and the oblique panos are consistent with
   it — but the right-hand two metres are behind a tree in every capture, and an oblique from
   the south-east can be read as four rows. This is cue 1; get it right before building, and
   record the count actually used in `REPORT.md`.
5. **Two neighbours are in flight.** `248-ritch` (lot 3776/105) and `254-ritch` (lot 3776/106)
   are separate parcels with separate footprints, so there is no exclusion conflict — but the
   three assets will stand side by side on a 60 m stretch of alley and must not read as one
   family. 246 is the tall modern white one; the other two are low painted timber houses.
6. **The architect is unattributed.** "Edmund Lai" and "D and S Leong Associates" appear in
   permit-agent aggregations, and no primary source confirms either. Do not put a name in
   `REFERENCE.md` without one.
7. **No published photograph shows the whole facade unobstructed after about 2019.** The three
   street trees the project was required to plant have grown into a continuous canopy. Every
   facade fact in this dossier comes from the 2015–2019 historical panoramas listed in 2.2;
   anything sourced from a current capture will be partial.
