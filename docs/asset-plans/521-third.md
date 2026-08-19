# 521 Third Street — SF-SIM asset plan

A 1914 three-storey **red-brick apartment-over-store** block holding the corner of
**3rd Street and Taber Place**, filling its 14.7 m × 23.1 m lot completely. It is
the oldest and lowest thing on its stretch of 3rd: a dark red brick box with a
heavy **cream cornice over a dentil course**, a **Greek-key (meander) belt band**
running the whole storefront head and turning the corner into Taber, recessed
**basketweave brick panels** scattered through the upper wall, five bays of plain
punched sash windows, and a black **fire escape** hung on the middle bay. The
ground floor is two shops — a bright **orange Neill's Grocery & Liquor** awning on
the left and a **black SouthBeach Food Collective** fascia over a graffiti-tagged
roll-up shutter on the right — with the residential entry between them. Down
Taber Place the ground storey turns to painted stucco carrying a big **mural and
graffiti piece**, with plain brick and small punched windows above.

It is the **low, ornamented** one. 501 Third across Taber is a 13.7 m brick loft
with big steel windows; 549 Third on its south-east party wall is a 13.0 m modern
condominium. At 11.4 m this building is 2 m shorter than both neighbours and the
only one on the corner with a cornice — getting it *lower* and *fussier* than
what flanks it is most of the job.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/521-third/`. This document is the plan only: Part 1 is the runnable
task prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `521-third` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3952384, 37.7811509` (parcel oriented-bbox centre, measured) |
| Target height | **11.4 m** to the parapet crest (*estimated*, two independent measurements agree); roof deck 10.9 m (LiDAR-measured) |
| Footprint | 14.74 m (3rd Street, SW) × 23.13 m (Taber Place, NW), 338.8 m²; a true rhombus on the 45° SoMa grid, measured |
| Triangle cap | 10,000 |
| Category | `2` (apartments) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 521 Third Street GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of 521 Third Street (the 521–527 3rd St /
Taber Place corner building, Neill's Grocery & Liquor) in San Francisco and
deliver it as a downloadable, validated GLB.

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
7. `artifacts/574-third/` — the closest **typological** reference already built:
   a taller masonry apartment block on the same street with a cornice and a
   regular punched-window rank. 521 must look like it came out of the same toy
   box, at a smaller and older scale.
8. `artifacts/592-third/` and `artifacts/599-third/` — the two nearest built
   assets on 3rd Street. They set the shopfront-band language and the render rig
   this asset shares.
9. `artifacts/550-third/` — the other 11 m building on this block face; use it to
   calibrate how much wall detail an 11 m box can carry before it reads busy.
10. `docs/asset-plans/521-third.md` — this plan, whose dossier is your research
    starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Must capture

- The **corner condition at 3rd and Taber Place**: a sharp 90° corner (verified
  from rectilinear Street View — it is *not* chamfered or rounded; the curve you
  will see in any equirectangular panorama is projection distortion). Two
  designed elevations meet here: the 14.7 m 3rd Street front and the 23.1 m
  Taber Place flank.
- The **cream cornice with its dentil course**, projecting hard off the top of
  the brick and returning around the corner into Taber for a short run before
  it stops. It is the single strongest silhouette cue at thumbnail size, and it
  is the only cornice on this corner.
- The **Greek-key (meander) belt band** in cream at the storefront head, running
  the full 3rd Street frontage and turning the corner to run the full Taber
  elevation. This is the second-strongest cue and the one that ties the two
  elevations into one building.
- The **dark red-brown brick** body — noticeably darker and browner than 501
  Third's brighter orange-red brick across Taber. Do not paint it the generic
  toy terracotta and leave it there.
- The **recessed basketweave / diaper brick panels**: square panels at the
  spandrel between the 2nd and 3rd floors on the end piers, and a row of
  horizontal panels immediately under the corbel band above each 3rd-floor
  opening. Model them as shallow recesses, not as texture.
- The **five-bay rhythm** on the 3rd Street front, both upper floors: bay 1
  window, **bay 2 a fire-escape door**, bays 3–5 windows. The rhythm is slightly
  uneven; do not regularise it into five equal bays.
- The **black fire escape** on bay 2 — two balconies and a diagonal stair. It
  is the busiest object on the facade and the thing that says "1914 SoMa
  apartment house". Keep it, and keep it thin.
- The **two-tenant shopfront**: a bright **orange** Neill's Grocery & Liquor
  awning and fascia on the north-west (Taber) half, a **black** SouthBeach Food
  Collective fascia over a dark roll-up shutter on the south-east half, and a
  recessed dark residential entry between them. The orange is the only saturated
  colour on the building and it must stay the accent — a single hero note, not a
  second body colour.
- The **projecting corner blade sign** (black box, orange lettering) hung off
  the 3rd Street face near the Taber corner at second-floor level.
- The **Taber Place elevation**: painted **stucco** ground storey covered by a
  mural and a graffiti piece, plain dark brick above with **small punched
  windows and vent openings** in a loose, irregular pattern — much sparser and
  smaller than the 3rd Street front — and a secondary fire escape toward the
  rear end. Render the mural as three to five flat inset colour shapes, not as
  an image texture (textures are forbidden by the contract).
- The **flat white membrane roof** inside a parapet ring, with the roof-edge
  **hoist davit frame and ladder** that stand proud of the parapet on the 3rd
  Street edge, plus a small stair hatch and a handful of vents. The camera looks
  down: this is the largest surface the app ever shows.
- The fact that it is **lower than both neighbours**: 11.4 m against 501 Third's
  13.7 m across Taber and 549 Third's 13.0 m on the south-east party wall. Do
  not round the height up to match them.

## Research 521 Third Street independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- The 3rd Street (south-west) elevation in detail — the bay rhythm, the
  fire-escape door position, the exact extents of the two shopfronts and the
  residential entry between them
- The Taber Place (north-west) elevation for its full 23.1 m — window and vent
  positions, where the Greek-key band stops, where the stucco/brick line sits,
  and the rear fire escape
- The 3rd/Taber corner itself: whether the cornice, the Greek-key band and the
  brick all return, and how far
- The rear (north-east) elevation, which no street view reaches — infer it
  conservatively from the Taber flank and say so
- Aerial and roof views — parapet ring, roof furniture, the davit frame
- Day and night appearance; the storefront signage is the only meaningful light
  source on this building

Prefer architect/engineer publications, owner or institutional material,
planning and permitting documents, architectural press, geolocated photography,
and aerial/satellite imagery. Never rely on a single photograph, a single
AI-generated image, or a single unsourced 3D model. Separate verified facts from
visual inference; if sources disagree, document the disagreement and decide.

**Three source problems are already resolved in 2.1 and 2.3 — re-check them, do
not silently re-inherit the wrong value:**

1. The DataSF LiDAR `hgt_max` on this footprint is **13.53 m**, 2.6 m above the
   roof-deck mode. It is *not* the crest: the roof-edge **hoist davits and
   ladder** on the 3rd Street parapet stand roughly that much proud of it, and
   they are visible in the 2025 Street View capture. Same failure mode as 592
   Third's street trees. Do not model a 13.5 m building.
2. The OSM `height=11` tag describes the **roof deck**, not the crest. It agrees
   with the LiDAR mode (10.87 m) and is 0.5 m short of the parapet.
3. The **DataSF LiDAR footprint ring is not the building outline.** It measures
   327.7 m² where the surveyed parcel measures 338.8 m² and the assessor's
   3,610 sq ft lot measures 335.4 m²; it overhangs the 3rd Street property line
   by about 0.5 m (the cornice) and falls about 1 m short at the rear. Build on
   the **parcel rhombus in 2.3**, which the assessor's 76 ft lot depth confirms
   exactly.

## Create a reference dossier

Write `artifacts/521-third/REFERENCE.md` containing: source links and what each
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

This is a **secondary building** in the style bible's detail budget (§21) — a
tier below 574 Third, a tier above 592 Third. Two designed elevations, one strong
horizontal ornament system (cornice + Greek-key band) carried around the corner,
one saturated accent (the orange awning), and a genuinely designed roof.

Unlike the plain 1905 lofts already built on this street, this building **does**
have ornament, and leaving it out would be as much a lie as inventing it. But the
ornament is *horizontal and repetitive*: two cream bands, a dentil course, a
corbel course and a scatter of recessed brick panels. Spend the budget there and
keep the windows dumb.

The finished asset must be immediately recognizable as this corner, consistent
with the real building from all four sides and above, architecturally credible,
and a premium handcrafted miniature — not photorealistic, not voxel art, not
generic low-poly, and never accurate in one view while invented in the others.

## Scope of the exported asset

Export the single building: brick body, cornice and parapet, the 3rd Street
front's shopfront band and upper windows, the Taber Place flank with its stucco
base and mural panels, the rear wall, the blank south-east party wall, both fire
escapes, the projecting blade sign, and the roof deck with its parapet ring,
davit frame and roof furniture.

Do not include unrelated surrounding city geometry: 3rd Street, Taber Place, 501
Third, 549 Third, the sidewalk, the utility pole and its trolley wires (they pass
directly in front of the facade in every photograph and are **not** part of the
building), the street tree, parking meters, traffic signs, the 511 transit-stop
flag, parked cars, people, plinths, cameras or lights. Temporary context may
appear in review renders but must not leak into the GLB.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary
`.glb`; real-world meters; origin at base center; minimum geometry Z ~ 0; applied
transforms; no negative scales; outward normals; no duplicate or foreign
geometry; no image textures; no transparency; flat-color materials named `Toy_*`
from the project palette; `_Glow` suffix only on surfaces that glow at night; no
`Toy_body`; no cameras, lights, animations, armatures or constraints; no external
dependencies; at most 10,000 triangles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model
drops into the city at its real-world heading — the loader applies no rotation
(`placeGeneric` in `app/src/assets.js` only scales and positions). The 3rd Street
front faces **south-west, bearing 225.1°**; the Taber Place flank faces
**north-west, bearing 315.1°**; the rear faces north-east (45.1°) and the party
wall south-east (135.2°). The building is rotated roughly 45° off the world axes,
so build directly on the measured footprint polygon in 2.3 rather than modelling
an axis-aligned box and rotating it.

**Height normalization:** the tallest geometry in the export must land at exactly
**11.4 m** so the loader's `targetHeightM / measuredHeight` scale is 1.0. The
parapet crest is the datum; the roof-edge davit frame is the one thing allowed to
reach it, and nothing may poke above it. If you model the davits proud of the
parapet, they become the crest and the parapet drops below 11.4 m — decide which
you mean and record it in REPORT.md.

## Reproducible Blender workflow

Blender 5.2 LTS. Headless: `blender -b --python script.py -- args`.

Keep `artifacts/521-third/build_521_third.py` (deterministic build script),
`artifacts/521-third/521-third.blend`, and `artifacts/521-third/521-third.glb`.
The script must rebuild the model reliably enough for future revision. Do not
modify or rename an unrelated existing GLB to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras: `521-third-top.png`,
`521-third-north.png`, `521-third-east.png`, `521-third-south.png`,
`521-third-west.png`, plus `521-third-contact-sheet.png`, at least one high
three-quarter aerial beauty render `521-third-aerial.png`, and a night render
`521-third-aerial-night.png`.

The four elevations must share scale, framing, lighting, exposure and projection;
use orthographic or long-lens cameras; label directions from the researched
orientation; the top view must clearly show the parapet ring, the davit frame and
every hatch and vent; the aerial view uses the style bible's camera assumptions
(30–50 degrees down, long lens). Simple tabletop lighting, neutral warm
background, minimal depth of field, and every image must depict the same exported
model.

Because the building sits at 45° to the world axes, the "west" orthographic
camera looks straight at the west corner and shows the 3rd Street front and the
Taber Place flank at once — that view is the hero, and it is the one to iterate
on first. Label the images by world direction as required, but judge the facades
from the aerial.

For the night render, drive `_Glow` from **Base Color**, not from the imported
emission — glTF writes `emissiveFactor = 0`, so a re-imported `_Glow` material
renders white otherwise. `tools/glb-optimize/render_ab.py` does this correctly.

## Validate the exported GLB

Re-import `521-third.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture
count, camera count, light count, animation count, applied-transform status,
negative-scale status, normal-orientation status, unexpected geometry, and
per-material contract compliance. Render at least one review image from the
re-imported asset. Write `artifacts/521-third/validation.json` and
`artifacts/521-third/REPORT.md`.

Note that the axis-aligned XY bounding box will be roughly **26.7 × 26.7 m** (a
little more once the cornice overhang is added) even though the building is
14.7 × 23.1 m — that is the expected consequence of a ~45° real-world heading,
not a scale error.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "521-third",
  "file": "521-third.glb",
  "anchor": [
    -122.3952384,
    37.7811509
  ],
  "targetHeightM": 11.4,
  "cat": 2,
  "name": "521 Third Street",
  "estimated": true,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a separate, explicitly requested job — run `docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in `docs/asset-plans/521-third.md`.
````

---

## Part 2 — Research and design dossier

Compiled 18 August 2026 from the sources in 2.2. Values marked *inferred* or
*estimated* are visual or derived, not published figures — the executing agent
must re-verify anything it relies on.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Built | **1914** | SF Assessor secured roll 2023–2025, block 3775 lot 072 |
| Storeys | **3** | SF Assessor roll AND every building permit 1989–2024 (`number_of_existing_stories = 3`) |
| Units | **15** residential (12 for a period after the 1989–90 permits, back to 15 by 2014) | SF building permits `i98e-djp9`, block 3775 lot 072 |
| Use class | **AC — "Apartment & Commercial Store"**, use code COMM | SF Assessor 2025 |
| Construction | Class **C** (masonry). The 1989 permit reads *"seismic bracing, parapet bracing, electrical & plumbing"* — the signature of an **unreinforced-masonry retrofit** | SF Assessor + SF permit 8903753 group |
| Block / lot | 3775 / 072 | SF Assessor; DataSF footprint `mblr = SF3775072`; parcel `blklot 3775072` |
| Parcel address of record | **521–527 3rd St** (odd) | DataSF parcels `acdm-wktn`: `from_address_num 521`, `to_address_num 527`. Tenant addresses 521, 521A, 523, 525, 527 all sit on this one lot — see 2.15 |
| Footprint (build on this) | **338.8 m²**; 14.74 m (3rd St, SW) × 23.13 m (Taber Pl, NW), a true rhombus with 90° corners on the 45° grid | DataSF surveyed parcel `3775072`, reprojected — **measured** |
| Lot area / depth | 3,610 sq ft (335.4 m²), depth **76.0 ft = 23.16 m** | SF Assessor — depth matches the measured 23.13 m to 3 cm; the building covers the lot |
| Floor area | 10,260 sq ft (953 m²) over 3 storeys = 318 m²/floor | SF Assessor — 94 % lot coverage, i.e. no rear yard and no light court big enough to model |
| DataSF LiDAR footprint (cross-check, **do not build on**) | 327.7 m²; overhangs the 3rd St line ~0.5 m and stops ~1 m short at the rear | DataSF `ynuv-fyni` `SF3775072` — see 2.3 |
| OSM footprint (cross-check) | 325.4 m², 14.01 × 23.41 m | OSM way/124884350, `addr:housenumber = 521;523;525;527`, `height = 11` |
| Roof deck height | **10.87 m** above ground (`hgt_majoritycm` 1087; median 10.95, mean 10.98, std 0.96 m over 1,309 cells) | DataSF LiDAR — **measured** |
| Parapet crest | **11.4 m** above ground | *estimated*, but from two independent measurements that agree — LiDAR roof-deck mode + parapet, and Street View photogrammetry (2.16). Not published anywhere |
| LiDAR `hgt_max` | 13.53 m — **not the crest** | the roof-edge hoist davits and ladder above the 3rd Street parapet, plainly visible in the 2025 capture. `hgt_min` 6.47 m is the matching low artifact |
| OSM `height` tag | `11` | OSM way/124884350 — agrees with the LiDAR roof **deck**, i.e. it describes the deck, not the crest |
| Ground elevation | 5.66 m (NAVD88) `gnd_min_m`, mean 6.03 m, max 6.57 m, range 0.91 m | DataSF LiDAR — the app's terrain handles this, not the asset |
| Zoning | **CMUO** (Central SoMa Mixed Use Office); Supervisorial District 6; analysis neighbourhood Financial District/South Beach; planning district South of Market | DataSF parcels |
| Frontage headings | 3rd Street front faces **225.1° (SW)**; Taber Place flank **315.1° (NW)**; rear **45.1° (NE)**; party wall **135.2° (SE)** | measured from the surveyed parcel polygon |
| Current occupants | **Neill's Grocery & Liquor** (521, 3rd St, orange awning); **SouthBeach Food Collective** (521A, 3rd St, black fascia — the unit HRD Coffee Shop held 2009 → June 2023); **527 3rd Apartments** residential entry at the south-east end; upper floors residential | OSM POI node 10874867136 (`check_date = 2026-04-26`); SF business registrations 0441146-01/02-001; CA ABC licence 00554688; 2025 Street View signage |
| Neighbour heights (LiDAR mode) | **501 Third** across Taber Place `SF3775073` **13.72 m** (max 16.42); **549 Third** on the SE party wall `SF3775125` **13.03 m** (max 15.93); `SF3775070` 23 m east **7.86 m**; **164 South Park** `SF3775069` **4.61 m** | DataSF LiDAR — 521 is the **lowest** building on its own corner |

### 2.2 Sources

- https://www.openstreetmap.org/way/124884350 — footprint, `building=yes`, `height=11`, `addr:housenumber=521;523;525;527`
- OSM node 10874867136 — Niell's Grocery & Liquor, `shop=convenience`, `check_date=2026-04-26`, the ground-floor tenant that names the corner
- `https://data.sfgov.org/resource/ynuv-fyni` (DataSF Building Footprints, 2010 LiDAR-derived), record `SF3775072` — the 10.87 m roof deck, the 13.53 m max, and every neighbour height quoted in 2.1
- `https://data.sfgov.org/resource/acdm-wktn` (DataSF Parcels) — `blklot 3775072`, the surveyed 338.8 m² rhombus this asset is built on, address range 521–527, zoning CMUO
- `https://data.sfgov.org/resource/wv5m-vpq2` (SF Assessor Historical Secured Property Tax Rolls, 2023–2025) — 1914, 3 storeys, 15 units, 25 rooms, class AC, 3,610 sq ft lot, 76 ft depth, 10,260 sq ft floor area, construction type C
- `https://data.sfgov.org/resource/i98e-djp9` (SF Building Permits), block 3775 lot 072 — 9 records 1989–2024: the 1989 seismic/parapet bracing, the 1990 unit-count revisions and garbage-chute sprinkler, the **1991 awning fabrication permit**, the 2014 kitchen-hood pair, the 2023 fire-alarm replacement, the 2024 health-inspector counter repair
- Google Street View, capture **2025**, panorama `8bbQy0YWLwpYOWjU44C52Q` from 3rd Street opposite the frontage and `Z7M9DH3anUhr-UCyCfWsJw` at the mouth of Taber Place — the 3rd Street elevation in detail, the corner, and the Taber flank with its mural. Equirect tiles at zoom 5 (16384 × 8192) carried the cornice and the Greek-key band; the rectilinear thumbnails settled the corner geometry (2.15 risk 1)
- Google satellite tiles at z21 — the flat white membrane roof and its parapet ring
- SF Planning, *Central SoMa Historic Context Statement & Historic Resource Survey* (draft, 16 March 2015), Jonathan Lammers — the building type: post-1906 brick lodging houses and apartment-over-store blocks along 3rd, Classical Revival detailing, the SoMa single-worker district this belongs to. Context, not a parcel-level rating
- `https://www.hbgrealty.net/soma/` — HBG Realty lists "521-527 3rd Street" among eight restored historic buildings on 3rd; confirms current residential use and the 521–527 range
- SF business registration `0441146` and CA ABC licence `00554688` — HRD Coffee Shop at 521A from July 2009 to 23 June 2023, which dates the black fascia's predecessor
- `app/public/tiles/buildings/23_13.bin` (this repo's committed bake) — what the procedural city currently puts here: a 330 m² block, base 5.4 m, top 18.3 m, i.e. **12.9 m tall**. Used for the exclusion measurement in 2.13

Nothing here is behind a paywall or a login; no copyrighted imagery is committed
to the repo.

### 2.3 Orientation and placement

The building holds the **east corner of 3rd Street and Taber Place**: 3rd Street
runs NW–SE past its south-west face, Taber Place — a 6 m dead-end alley, signed
`END Taber` at its mouth — runs NE into the block past its north-west face. Its
south-east side is a party wall against 549 Third; its north-east side is the
rear, against the South Park block interior.

Measured footprint polygon, in Blender coordinates (metres, `+X` east, `+Y`
north), **counter-clockwise**, already centred on the anchor
`-122.3952384, 37.7811509`:

```
s ( -3.032, -13.320)   south corner — 3rd Street / SE party wall
e ( 13.368,   2.960)   east corner  — SE party wall / rear
n (  2.998,  13.350)   north corner — rear / Taber Place
w (-13.372,  -2.950)   west corner  — 3rd Street / Taber Place, the hero corner
```

| Edge | Length | Outward normal | Elevation |
|---|---|---|---|
| s→e | 23.11 m | 135.2° (SE) | blind party wall against 549 Third |
| e→n | 14.68 m | 45.1° (NE) | rear wall, block interior — no public view |
| n→w | 23.10 m | 315.1° (NW) | **Taber Place flank** — stucco base + mural, brick above |
| w→s | 14.64 m | 225.1° (SW) | **3rd Street front** — 521 / 521A / 523 / 525 / 527 |

Area 338.8 m², within 1.0 % of the assessor's 3,610 sq ft lot. The corners are
square to within 0.1°, and the two pairs of opposite edges differ by 4 cm and
1 cm — this really is a regular rhombus, unlike most of the SoMa lots already
modelled. Do not introduce skew for flavour.

**Why not the LiDAR ring.** `SF3775072` publishes 10 vertices enclosing 327.7 m².
Reprojected, its 3rd Street edge sits about **0.5 m outside** the surveyed
property line — the cornice overhang, captured from above — and its rear edge
falls about **1.1 m short** of the parcel's north-east boundary. Taken at face
value it gives a 15.26 m frontage on a 22.01 m depth, against the surveyed
14.74 × 23.13 and the assessor's 76.0 ft depth. It also carries a 5.2 m jog
across the 3rd/Taber corner that reads as a chamfer and is not one (it is the
awning and the projecting blade sign). Everything in this plan uses the parcel.

Because of the ~45° heading the axis-aligned bounding box is ~26.74 × 26.67 m for
the wall planes, rising to roughly **27.3 × 27.3 m** once the cornice overhang is
included. That is correct.

### 2.4 What each side shows

**South-west (3rd Street front, 14.6 m)** — Three storeys, read as three
horizontal bands.

*Base.* A continuous shopfront the full width, capped by the cream **Greek-key
belt band** at first-floor head height. Left (north-west, at the Taber corner) is
**Neill's Grocery & Liquor**: a bright **orange** sloped awning with black
lettering — `NEILL'S GROCERY & LIQUOR 521 THIRD STREET` on the valance, and
`BEER/WINE` and `LIQUOR` on the returns — over a glazed shopfront with a low
brick bulkhead and neon beer signs inside the glass. A **projecting black blade
sign** with orange lettering hangs off the wall above it, near the corner. Centre
is a narrow, deeply **recessed dark residential entry** with a small `521A 3rd
Street` sign over it. Right (south-east) is **SouthBeach Food Collective**: a flat
**black fascia** carrying a large circular baseball-style logo and white-outlined
lettering, over a wide **dark grey roll-up shutter** with a large graffiti tag on
it. At the far south-east end, a small tan/mustard awning marks the `527 3rd`
apartment entry.

*Upper wall.* Dark red-brown brick, two floors, **five bays** each: bay 1 a
window, **bay 2 a fire-escape door**, bays 3–5 windows. Openings are plain
rectangles with flat brick heads and simple sills; sashes are 1-over-1 with dark
frames and pale blinds behind most of them. Bay spacing is slightly uneven — the
gap between bays 1 and 2 is the widest. A **black steel fire escape** hangs on
bay 2: a balcony at each upper floor and a diagonal stair between them, with the
drop ladder folded at the second floor.

*Ornament.* Recessed **basketweave brick panels** — a square panel on the
north-west pier at the 2nd/3rd floor spandrel, a matching one on the south-east
pier, and a row of horizontal panels immediately below the top corbel course, one
over each 3rd-floor opening. Above them, two courses of **corbelled dogtooth
brick**, then a **dentil course**, then the heavy **cream cornice**, then a low
dark brick parapet band and its coping.

**North-west (Taber Place flank, 23.1 m)** — The same three bands, but demoted.
The Greek-key band turns the corner and runs the full length. Below it the ground
storey is **painted stucco**, not brick, in a warm peach-cream, and it is covered
end to end by a **mural and graffiti**: a cartoon figure, a large hat/saucer form
in cream and lavender, cloud swirls, and a blue-and-white piece with a
skyline-shaped fill, plus tags. Above the band, plain dark brick with **small
punched windows and small vent/louvre openings** in an irregular pattern — far
sparser than the front, and clearly secondary. A **second fire escape** in
grey-blue steel hangs near the rear end. The cornice returns around the corner for
a short run and then stops; from there the parapet is plain brick with a flat
coping.

**North-east (rear, 14.7 m)** — Not reachable from any public vantage; not
visible in any available photograph or from the aerial at a useful angle.
*Inferred:* plain brick with a scatter of small utility openings, matching the
far end of the Taber flank, and the rear fire escape's landing. Keep it as quiet
as possible and label it inferred in REFERENCE.md.

**South-east (party wall, 23.1 m)** — Blind. It abuts 549 Third, which stands
1.6 m taller, so in reality only a sliver of parapet ever shows. **549 Third is
absent from this repo's committed bake** (see 2.13), so in the app this wall will
be exposed until that gap is fixed — model it as a credible blank brick wall with
the cornice stopping cleanly at the corner, not as a hidden face.

**Roof** — Flat white/light-grey membrane inside a parapet ring, dead level
(LiDAR std 0.96 m across 1,309 cells, and that number is inflated by the davits).
Roof furniture is sparse: a **hoist davit frame and roof ladder** at the 3rd
Street parapet — two curved arms clearly visible above the cornice in every
street photograph — a small stair hatch, and a handful of vents and small ducts.
The 13.53 m LiDAR maximum is the davit frame, not a bulkhead: a stair penthouse
2.6 m tall over a 328 m² roof would have pushed the height standard deviation
well past 1 m.

### 2.5 Recognition cues, in priority order

1. **The cream cornice + Greek-key band pair** — two bright horizontal lines on a
   dark red box, one at the top and one at the storefront head, both turning the
   corner. Nothing else on this block face has them.
2. **The orange awning.** The only saturated colour for a hundred metres in
   either direction, and at the corner where the eye lands.
3. **The black fire escape on the middle bay** of the 3rd Street front.
4. **The dark red-brown brick**, read against 501 Third's brighter orange-red
   across the alley.
5. **The mural wall down Taber Place** — from the aerial camera this is the face
   that tells you the building has a second designed side.

### 2.6 Massing recipe

1. Extrude the 2.3 rhombus to 10.9 m — the roof deck.
2. Add the parapet ring inboard of the wall plane, 0.5 m tall, crest at 11.4 m.
3. Add the cornice as a single mitred band projecting ~0.35 m, its top at
   ~11.15 m, running the 3rd Street front and returning ~6 m into Taber. Dentils
   as one shallow repeating strip under it; corbel as two chamfered courses under
   that. Model the dentils as a single toothed profile swept once — do not
   instance 60 cubes.
4. Cut the five bays on the 3rd Street front and the sparse openings on Taber as
   recesses in the brick, then place flat glazing planes inboard.
5. Add the Greek-key band as a 0.35 m tall cream fascia at 4.0 m, wrapping the
   front and the full Taber flank. The meander itself is a shallow inset pattern
   on the front only; on Taber it can be a plain band.
6. Ground storey: brick bulkhead + glazing on 3rd Street; a flat stucco plane on
   Taber with three to five inset mural shapes.
7. Awning (orange, sloped), black fascia, roll-up shutter, recessed entry, blade
   sign.
8. Fire escapes: two per side, thin box-section balconies and a single diagonal
   stringer each. Budget them at no more than 1,200 triangles combined.
9. Roof: deck plane, parapet inner face, davit frame, hatch, four vents.

Per the style bible's semantic scale (§9): the cornice, the Greek-key band and
the awning may be exaggerated by up to ~1.3× in depth and thickness. The window
openings, the bay rhythm and the overall box may not.

### 2.7 Palette map

| Element | Material | Hex |
|---|---|---|
| Brick body, parapet | `Toy_brick` | `c96f4a` — darkened toward the real brown-red; if the executor keeps the stock value, compensate with `Toy_rust` panels rather than lightening it further |
| Recessed basketweave / diaper panels, corbel course | `Toy_rust` | `a86444` |
| Cornice, dentils, Greek-key band, window trim | `Toy_cream` | `f2ede3` |
| Taber ground-storey stucco | `Toy_peach` | `e8cdc9` |
| Mural shapes (3–5 flats) | `Toy_cobalt`, `Toy_mint`, `Toy_cream` | `2f5fb0`, `8fd0a8`, `f2ede3` |
| Window glass | `Toy_glass` | `2a4d73` |
| Window sashes, fire escapes, black fascia, blade sign, entry recess | `Toy_ink` | `3a3530` |
| Neill's awning + blade-sign face | `Toy_orange` | `d4622a` |
| Roll-up shutter, davit frame, roof ladder, vents | `Toy_steel` | `9aa0a6` |
| Roof membrane | `Toy_greige` | `b0aa9e` |
| Night: awning, blade sign, shopfront glass | `Toy_orange_Glow`, `Toy_glass_Glow` | `d4622a`, `6f95b8` |
| Night: a minority of upper windows | `Toy_gold_Glow` | `caa64a` |

**Do not use `Toy_roofd` on the roof deck.** It renders near-black in the app
(measured rgb(9,9,12) on a comparable deck) and this roof is a light membrane.

**Glow discipline.** Hero glow = the orange awning + blade sign. Supporting = the
shopfront glazing behind it. Ambient = four or five of the ten upper-floor windows
in `Toy_gold_Glow`, never all ten. A `_Glow` material's **base colour is its
daytime appearance** — pick colours that sit in the non-glow palette by day, and
never wrap the building in a closed glow shell (a closed shell reads as two alpha
layers, ~23 % tint, by day).

### 2.8 Triangle budget

| Element | Budget |
|---|---|
| Brick body + parapet + openings | 2,600 |
| Cornice, dentils, corbel, Greek-key band | 2,400 |
| Windows (glass + sashes, 5+5 front, ~8 Taber, ~4 rear) | 1,400 |
| Basketweave panels (7) | 500 |
| Shopfront: awning, fascia, shutter, entry, bulkhead, blade sign | 1,200 |
| Fire escapes (2) | 1,200 |
| Roof deck, davit frame, hatch, vents | 500 |
| Headroom | 200 |
| **Total** | **10,000** |

### 2.9 Night state

The building is dark. Two lit shopfronts at the base, a scatter of apartment
windows above, nothing on the Taber flank except spill from the corner. The
orange awning and its blade sign carry the whole composition — get their glow
right and the rest can stay almost black. Required deliverables: a night
`_Glow` design whose day colours match their non-glow neighbours, a night aerial
render, and a night tile on the contact sheet.

### 2.10 Camera preset

`{ distance: 200, yaw: 270, pitch: 28 }`. `camera` is **mandatory** even for a
landmark with no number key — `main.js` maps every manifest landmark into
`presets` and `camera.js` reads `preset.yaw` unconditionally. The bisector of the
3rd Street front (normal 225.1°) and the Taber Place flank (normal 315.1°) is
270.1°, which is where both designed elevations and the hero corner read at once;
under either reading of the app's yaw convention (`yaw = bearing` or
`yaw = 180 − bearing`) that lands on 270, so this one is unambiguous. 200 m suits
an 11.4 m building (cf. `550Third` 190 at 11 m, `592Third` 200 at 8.2 m).
**Render it before believing it.**

### 2.11 Streaming decision

`loadRadius`: the default rule gives `max(2500, 11.4 × 30) = 2500` m. Take the
default. Not `alwaysLoaded` — this is a 11 m background building, nowhere near
skyline scale.

### 2.12 Detail-budget placement

Secondary. One primary elevation (3rd Street), one secondary designed elevation
(Taber Place), one blind party wall, one inferred rear, one designed roof. It sits
below 574 Third and 599 Third and above 592 Third and 370 Brannan in the block's
hierarchy. If the triangle count starts pushing 10,000, cut the rear openings and
the Taber vents first, the fire escapes last — the fire escape is a recognition
cue and the rear is invisible.

### 2.13 Integration notes (for later, not this task)

- **New landmark.** Add a `pipeline/lib/landmarks.mjs` entry (`id: '521Third'`,
  `exclude: 5`) and re-bake the affected tiles, or the baked procedural building
  on this exact footprint will intersect the GLB. It will also *tower* over it:
  the committed bake gives this footprint a base of 5.4 m and a top of 18.3 m,
  i.e. **12.9 m** against the asset's 11.4 m, so without the exclusion the asset
  is simply invisible inside a taller block. Do not judge the integration before
  the bake.
- **Exclusion radius, measured two ways.** Against this repo's committed bake
  (`app/public/tiles/buildings/23_13.bin`, ring index 98, the rings `excluded()`
  actually consumes): this footprint's own ring centroid sits **0.18 m** from the
  anchor, its own nearest vertex 8.60 m, and the nearest **neighbour** vertex is
  18.39 m (`SF3775073`, 501 Third across Taber). Against the raw DataSF LiDAR
  polygons — which is what a re-bake consumes — the same numbers are **1.91 m**
  for this building's own polygon centroid and **8.60 m** for the nearest
  neighbour vertex, and that neighbour is **549 Third (`SF3775125`), which shares
  the party-wall vertex exactly**. Since `excluded()` drops a ring on centroid
  **or** any vertex, the window that drops exactly this building is
  **1.91 m < r < 8.60 m**. **5 m** sits in the middle of it with 3.1 m of margin
  below and 3.6 m above. The exclusion fires on the **centroid** test, not the
  vertex test — do not shrink it below 2 m expecting the vertices to catch it,
  and do not push it past 8.6 m or it deletes 549 Third. Re-run the measurement
  against the actual bake before committing.
- **549 Third is missing from the committed bake.** DataSF carries it
  (`SF3775125`, 565 m², 13.03 m mode) 24 m to the south-east, sharing this
  building's party-wall vertex, but no ring exists anywhere within 87 m at that
  bearing in `23_13.bin`. That is a **pre-existing gap in the procedural city, not
  something this landmark causes** — but it means the south-east party wall will
  be exposed in the app, so build that wall to be looked at, and note the gap in
  the integration report rather than silently absorbing it. Do not widen the
  exclusion to "tidy" it.
- `loadRadius`: 2500 m (2.11). `cat`: 2 (apartments — `CAT.apartments` in
  `app/src/props.js`; the building is 15 residential units over two shops).
- **`camelId()` check.** `app/src/assets.js` derives the registry id as
  `id.replace(/-([a-z])/g, upper)`; digits do not start a segment, so
  `521-third` → **`521Third`**, matching `550Third` / `592Third` / `599Third`.
  Get this wrong and the procedural version is never hidden: two buildings, no
  warning.
- **Manifest append discipline.** Splice the new block into
  `landmarks_manifest.json` as **text**, in front of the closing `  }\n]` — a
  `json.load`/`json.dump` round-trip rewrites `11.0` → `11` across unrelated
  entries. A clean append is +19 lines, 0 deletions.
- **This makes six manifest landmarks on this stretch of 3rd** — 500, 521, 550,
  551, 560, 574 — with 501 Third across Taber and 549 Third on the party wall left
  procedural (and 549 currently absent entirely). In local QA check that 521's
  parapet meets 501 Third across the alley without the alley closing up, and that
  the 3rd Street wall reads continuously from 501 through 521 to 549.
- **Batch mode applies.** This landmark is being built alongside others, so
  stage 5 runs the bake, does the full QA on it, then throws it away
  (`git checkout -- app/public/tiles api/_data`) and commits source only.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Bounding-box top exactly 11.4 m (loader scale lands at 1.0)
- [ ] Dimensions plausible in meters and consistent with 2.1 (XY bbox ~27 × 27 m is expected)
- [ ] Triangles at or under 10,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the awning, blade sign, shopfront glazing and a minority of upper windows; no closed glow shells
- [ ] Roof deck is **not** `Toy_roofd`
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (per-object signed volume for the union of solids; ray test residual ≤ 0.15 %)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + contact sheet + night render regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

1. **The corner is square, and every panorama says otherwise.** In the
   equirectangular Street View tiles the cornice and the Greek-key band appear to
   curve smoothly around the 3rd/Taber corner, and the LiDAR ring carries a 5.2 m
   jog there. Both are artefacts: a straight horizontal line above the horizon is
   *always* a curve in an equirect, and the LiDAR jog is the awning and the
   projecting blade sign. The rectilinear thumbnails from panorama
   `Z7M9DH3anUhr-UCyCfWsJw` at yaw 112 show a crisp 90° arris. **Do not build a
   rounded corner.**
2. **The crest is estimated, not published.** 11.4 m comes from agreement between
   the LiDAR roof-deck mode (10.87 m) plus a visible parapet of roughly 0.5 m,
   and an independent photogrammetric fit (2.16) giving 11.4–11.8 m above the
   roadway, which reduces to roughly 11.3–11.6 m once the 0.2–0.35 m rise from
   the roadway to the building's ground is removed. A measured elevation drawing
   or a planning document would beat both. Mark `"estimated": true`.
3. **The rear elevation is inferred.** No public vantage reaches it and no aerial
   shows it usefully. Whatever is modelled there must be labelled inferred.
4. **The mural will date.** The Taber Place mural and graffiti are ephemeral — the
   2025 capture is a snapshot. Model it as a few abstract flat shapes that read as
   "painted alley wall" rather than as a portrait of that specific piece, so it
   ages gracefully. This is the same call already made for tagged shutters
   elsewhere on the block.
5. **The shopfront tenants will change.** HRD Coffee Shop held 521A from 2009 to
   June 2023; SouthBeach Food Collective holds it now. Neill's is long-running and
   its orange awning dates to the 1991 awning permit, so the orange is the durable
   part — the lettering is not. Keep the orange awning and the black fascia as
   *forms*, and keep the lettering coarse enough that it reads as signage rather
   than as a specific business.
6. **One parcel, five addresses — check before a sibling starts.** 521, 521A,
   523, 525 and 527 3rd Street are all on **APN 3775-072**, a single 3,610 sq ft
   lot with one building. Only one asset per parcel can own the exclusion, so no
   sibling in the 521–527 range may be planned separately. Checked 18 August
   2026: no plan, artifact or worktree exists for any of them.
7. **Historic status is unconfirmed at parcel level.** The Central SoMa Historic
   Resource Survey covers this block and describes exactly this building type,
   but a parcel-level rating for 3775/072 was not located in the public datasets.
   It does not change the model; it is recorded here so nobody re-searches for it.

### 2.16 Appendix — the photogrammetric height check

Method per the project's Street View photogrammetry procedure. Panorama
`8bbQy0YWLwpYOWjU44C52Q` (3rd Street, opposite the frontage), equirect tiles at
zoom 5 (16384 × 8192, horizon on row 4096, 0.02197°/px).

The building's sky boundary was extracted per column and fitted to
`tan θ = (h/n)·cos(ψ − φ)`, the equirect locus of a horizontal line at height `h`
above the camera, perpendicular distance `n`, normal yaw `φ`. Robust
trimmed-median fit over 2,430 columns converged to `h/n = 0.671` with a residual
RMS of 0.003 in tan units.

The frontage subtends 53.61° of yaw (edges at 245.39° and 299.00° in raw equirect
yaw). With the surveyed 14.74 m frontage that gives a perpendicular distance
`n = 13.9 m` — consistent with a camera in the traffic lane of a street whose
building line to centreline is about that. Crest height above the roadway,
sweeping `φ` across its whole plausible range and taking the camera at 2.5 m:

| assumed φ | n (m) | crest above roadway (m) |
|---|---|---|
| 255° | 12.91 | 11.41 |
| 265° | 14.22 | 11.94 |
| 270° | 14.48 | 12.05 |
| 275° | 14.46 | 12.04 |
| 285° | 13.61 | 11.70 |

So **11.7 ± 0.35 m above the roadway**, ±0.3 m more for camera-height
uncertainty. The LiDAR ground under the footprint runs 5.66–6.57 m NAVD88 against
a roadway near the low end, so subtract 0.2–0.35 m to reach the LiDAR frame:
**11.3–11.6 m**, against a LiDAR roof-deck mode of 10.87 m. A parapet of 0.45–0.65 m
closes the gap, which is what the photographs show. 11.4 m is the middle of that.

The same fit run on the cream cornice band rather than the sky boundary gives
11.72 m above the roadway — 0.08 m below the parapet crest, which is the right
sign and the right order of magnitude for a cornice sitting just under a coping.
