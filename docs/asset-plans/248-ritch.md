# 248–250 Ritch Street — SF-SIM asset plan

A 1915 wood-frame two-flat on a 25-foot SoMa alley lot: cream-painted shiplap,
a canted two-storey bay, a heavy bracketed cornice, twin stoops for its two
front doors, and a rear third of the lot that is not building at all but garden.
The smallest landmark in the Ritch Street family and the first in it that is a
**house** rather than a warehouse — its whole job is to be the one piece of
pre-earthquake domestic fabric left standing between a 2013 five-storey
apartment block and a parking lot.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/248-ritch/`. This document is the plan only: Part 1 is the runnable
task prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `248-ritch` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3956780, 37.7801725` (centre of the built quad, derived from the surveyed parcel — see 2.3) |
| Target height | **8.6 m** (cornice crest; roof deck 8.0 m — both measured, see 2.1) |
| Footprint | **7.60 m frontage x 13.9 m depth**, 105.6 m2, on the 45.05 deg SoMa grid |
| Triangle cap | 7,000 |
| Category | `2` (Apartments — a two-unit flat) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 248–250 Ritch Street GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of 248–250 Ritch Street in San Francisco and
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
7. `artifacts/salesforce-tower/` — the reference implementation of this exact
   deliverable (dossier, deterministic build script, validator, renders, report)
8. `artifacts/49-south-park/` — **the closest match in kind and scale**: a
   two-storey painted-timber residence with a bay, a bracketed cornice and a
   raised basement, built to this same contract. Its `build_49_south_park.py`
   is the structure to follow; its palette map is the starting point for 2.8.
9. `docs/asset-plans/248-ritch.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## What is already observed, and what is not

**Observed and measured** (2.15 shows the working):

- The whole north-east (Ritch Street) elevation, from a Google Street View
  panorama taken from 8.56 m out. It has been rectified to metres: every height
  and every horizontal position quoted in 2.4 and 2.7 is read off that
  rectification, not eyeballed.
- The roof outline and the rear garden, from a near-nadir Google satellite frame
  at z21 with the surveyed parcel overlaid.
- Heights, twice, independently: the DataSF LiDAR summary solved as a two-level
  mixture, and the rectified panorama. They agree to 0.1 m.

**Not observed by anything.** The two long party walls, the rear (south-west)
elevation of the house, and the roof surface itself in any detail. 2.4 says what
each of those is *inferred* to be and why; 2.15 lists them as the standing risks.
Do not present an invention of them as observation — but do design them, because
the app's camera looks down and the roof is a facade.

## Must capture

- The **canted two-storey bay** on the south-east half of the street face, with
  its three-window group (narrow / wide / narrow) at each level and its blue-grey
  capped sill courses — the single strongest recognition cue
- The **bracketed cornice**: modillion brackets over a dentil band, stepping out
  and around the bay's two angles, and returning across the flat half
- The **two entries side by side** under one continuous dentilled hood — 250 to
  the south-east, 248 to the north-west — each on its own blue-grey concrete
  stoop, the north-west one with a metal handrail
- The single tall window over the entry zone at the upper level
- The **raised basement**: a low blue-grey band with a small window and a
  service door, carrying the house 1.46 m above the pavement
- Cream shiplap siding with slate blue-grey trim on every sill, cap, water table,
  door and stoop
- The flat roof behind the cornice, designed for the downward camera
- The fact that the house stops two-thirds of the way back and the rest of the
  lot is garden — the model ends where the building ends

## Research 248–250 Ritch Street independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- The north-east (Ritch Street) elevation
- Both party walls and the rear — **nothing in this dossier saw them**; if you
  find anything that does, that is new evidence and belongs in `REFERENCE.md`
- Aerial and roof views
- Day and night appearance
- Any historic survey (this is a 1915 building in a 1998-mapped block; a Sanborn
  sheet or a Planning historic-resource survey would settle the rear)

Prefer architect/engineer publications, owner or institutional material,
planning and permitting documents, architectural press, geolocated photography,
and aerial/satellite imagery. Never rely on a single photograph, a single
AI-generated image, or a single unsourced 3D model. Separate verified facts from
visual inference; if sources disagree, document the disagreement and decide.

## Create a reference dossier

Write `artifacts/248-ritch/REFERENCE.md` containing: source links and what each
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

This building has no skyline silhouette and only one public elevation, 7.6 m
wide. Spend the budget on the bay, the cornice and the twin stoops — the three
things a person on Ritch Street actually sees — and on a roof that is worth
looking down at. Resist adding ornament the building does not have: it is a
plain builder's flat, not a Queen Anne, and the restraint is the character.

## Scope of the exported asset

Export the 248–250 Ritch Street house itself: its massing, bay, cornice, entries,
stoops, raised basement, roof and roof plant.

**Do not include the rear garden, the fence, the trees, the utility pole,
Ritch Street, the pavement, the neighbours at 246 or 252–254, vehicles, people,
plinths, cameras or lights.** The rear third of the lot is real garden and the
app's ground plane is what should show there. Temporary context may appear in
review renders but must not leak into the GLB.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary
`.glb`; real-world meters; origin at base center; minimum geometry Z ~ 0;
applied transforms; no negative scales; outward normals; no duplicate or foreign
geometry; no image textures; no transparency; flat-color materials named `Toy_*`
from the project palette; `_Glow` suffix only on surfaces that glow at night; no
`Toy_body`; no cameras, lights, animations, armatures or constraints; no external
dependencies; at most 7,000 triangles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model
drops into the city at its real-world heading — the loader applies no rotation
(`placeGeneric` in `app/src/assets.js` only scales and positions). The frontage
line runs 315.05 deg / 135.05 deg and the Ritch Street face looks **north-east,
outward normal 45.05 deg true**, so the contract's "front faces −Y" cannot be
honoured literally. Real-world orientation wins (AGENTS rule 5). Record the
decision and the measured heading in `REPORT.md`.

**Height normalization:** make the exported bounding-box top land exactly on
**8.6 m** — the cornice crest, not a vent or a chimney — so the loader's
`targetHeightM / measuredHeight` scale is 1.0.

## Reproducible Blender workflow

Blender 4.5 LTS or newer, headless only: `blender -b --python script.py -- args`;
no GPU, so use Workbench or CPU Cycles.

Keep `artifacts/248-ritch/build_248_ritch.py` (deterministic build script),
`artifacts/248-ritch/248-ritch.blend`, and `artifacts/248-ritch/248-ritch.glb`.
The script must rebuild the model reliably enough for future revision. Do not
modify or rename an unrelated existing GLB to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`248-ritch-top.png`, `248-ritch-north.png`, `248-ritch-east.png`,
`248-ritch-south.png`, `248-ritch-west.png`, plus `248-ritch-contact-sheet.png`,
at least one high three-quarter aerial beauty render `248-ritch-aerial.png`, and
a night render `248-ritch-night.png`.

The four elevations must share scale, framing, lighting, exposure and
projection; use orthographic or long-lens cameras; label directions from the
researched orientation. Add one extra square-on view along the **45.05 deg**
outward normal — the Ritch Street elevation is the hero image for this asset and
none of the four cardinal views is square onto it. The aerial view uses the style
bible's camera assumptions (30-50 degrees down, long lens). Simple tabletop
lighting, neutral warm background, minimal depth of field, and every image must
depict the same exported model.

## Validate the exported GLB

Re-import `248-ritch.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture
count, camera count, light count, animation count, applied-transform status,
negative-scale status, normal-orientation status, unexpected geometry, and
per-material contract compliance. Normals are checked two ways: per-object signed
volume (authoritative for a union of closed solids) and a deterministic
visibility-ray test (<= 0.15% residual, zero for single shells). Render at least
one review image from the re-imported asset. Write
`artifacts/248-ritch/validation.json` and `artifacts/248-ritch/REPORT.md`.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "248-ritch",
  "file": "248-ritch.glb",
  "anchor": [
    -122.3956780,
    37.7801725
  ],
  "targetHeightM": 8.6,
  "cat": 2,
  "name": "248-250 Ritch Street",
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
for that, together with the integration notes in `docs/asset-plans/248-ritch.md`.
````

---

## Part 2 — Research and design dossier

Compiled 18 August 2026 from the sources in 2.2. Values marked *inferred* or
*estimated* are visual or derived, not published figures — the executing agent
must re-verify anything it relies on.

**A note on the evidence quality of this dossier.** The record side is complete
and unanimous: the Assessor's roll (nineteen years), the surveyed parcel, seven
DBI permits, the EAS address file and the LiDAR footprint all describe the same
two-storey 1915 wood-frame two-flat and none of them disagree with any other.
The street elevation is not merely described but **rectified** — a Street View
panorama solved for camera position from three collinear surveyed corners, then
read in metres (2.15). Two independent methods put the roof within 0.1 m of each
other. What nothing sees is the rear of the house and the two party walls; those
are inferred from the type and are named as risks in 2.15.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Address | 248 **and** 250 Ritch Street, San Francisco, CA 94107 — one building, two flats | DataSF EAS addresses (`ramy-di5m`), both rows on parcel 3776105 |
| Parcel | Block 3776, Lot 105 (APN 3776-105); address range **248–250**, no other number on the lot | DataSF Parcels `acdm-wktn` — **measured**; see 2.15 on why this matters |
| Built | **1915** | SF Assessor secured roll, `year_property_built = 1915` (all roll years agree); corroborated by the augrented summary |
| Use / class | Multi-Family Residential, class **F** "Flats & Duplex", **2 units, 9 rooms** | SF Assessor `wv5m-vpq2` |
| Storeys | **2** | Assessor `number_of_stories = 2.0`; every DBI permit 2008–2025 also records 2 → 2, i.e. **never altered vertically** |
| Construction | **wood frame (Type V)** | DBI permits 200810083723, 200812198883, 202305308789, 202510217835 |
| Building area | **2,100 sq ft** (195.1 m2) over two floors → ~97.6 m2 per floor | Assessor `property_area` |
| Lot area | **1,873 sq ft** (174.0 m2) — the standard 25 x 75 ft SoMa alley lot | Assessor `lot_area`; parcel geometry gives 7.601 m frontage — **measured** |
| Zoning | **CMUO** — Central SoMa Mixed Use Office | DataSF Parcels |
| Neighbourhood | South of Market (South Beach / Mission Bay edge), Supervisorial District 6 | DataSF Parcels |
| Frontage (surveyed) | **7.601 m**, bearing 315.05 deg / 135.05 deg | DataSF Parcels, corners `(3687.77, -1126.69)` and `(3682.40, -1132.07)` in app metres — **measured** |
| Lot depth (surveyed) | 23.9 m | DataSF Parcels — **measured** |
| Built depth | **13.9 m**; the rear ~10 m of the lot is garden | two independent derivations agreeing to 0.2 m: the LiDAR mixture solve (14.05 m) and the OSM oriented bbox (13.84 m) — see 2.15 |
| Footprint (built) | **7.60 x 13.9 m, 105.6 m2** | derived from the two above; agrees with the Assessor's 97.6 m2/floor once light wells and wall thickness are allowed |
| Footprint (OSM) | 13.84 x 7.88 m oriented bbox, 101.2 m2 ring area | OSM way/147508934 (`addr:housenumber=248;250`, `source=Bing`) — **measured**, but **misregistered ~2.5 m to the north-west**, see 2.15 |
| Footprint (LiDAR) | 162.7 m2 raw ring, 657 cells at 50 cm — **the house plus the garden**, not the house | DataSF `ynuv-fyni` SF3776105 — **measured**; the mixture solve in 2.15 splits it |
| Roof deck | **7.95 m** (median) / 8.27 m (modal) above ground | DataSF LiDAR `hgt_mediancm` / `hgt_majoritycm` — **measured** |
| Cornice crest | **8.6 m** | two methods: the LiDAR two-level mixture solve gives the high level at **8.65 m**; the rectified Street View panorama puts the cornice top at **8.50 m ± 0.4** — see 2.15 |
| LiDAR height stats | max 14.27, min 0.88, mean 6.24, median 7.95, mode 8.27, sd 3.08 m | DataSF `ynuv-fyni` — **measured**. `hgt_maxcm` is **refused** as the target height; see 2.15 |
| Ground elevation | 4.79 m min / 6.03 m max (NAVD88) across the lot | DataSF LiDAR `gnd_mincm`/`gnd_maxcm` — app terrain handles this, not the asset |
| Main floor level | **1.46 m** above the pavement (raised basement below) | rectified panorama — **measured** |
| Floor to floor | **3.26 m** | rectified panorama, window heads at 4.00 and 7.26 m — **measured** |
| Works on record | reroof 1996 ($3.6k); vinyl siding to the **rear** of #250 only, 2008 ($8.3k, "not visible from the street"); two fireplaces and their chimneys removed 2008 ("chimneys 1/2 way back on side"); street space 2012; **reroof May 2023 ($24.8k)**; front-stair concrete repair Oct 2025 | DBI permits `i98e-djp9`, block 3776 lot 105 (7 records, 1996–2025) |
| Other history | sewer line repair 2018, kitchen/laundry remodel 2016, sewer trap 2012; several unintentional fire-alarm activations, no fire damage | augrented building summary |
| Neighbours | **246 Ritch** (north-west): a 2013 five-storey, 50 ft, 19-unit apartment building, LiDAR median **15.87 m**. **252–254 Ritch** (south-east): a twin two-flat of the same era and height, LiDAR median **8.04 m** | DataSF LiDAR SF3776456 / SF3776106; SocketSite for 246's programme — **measured** |

### 2.2 Sources

- https://www.openstreetmap.org/way/147508934 — footprint, `addr:housenumber=248;250`, `addr:street=Ritch Street`, `source=Bing`
- `https://data.sfgov.org/resource/acdm-wktn` (DataSF Parcels) — blklot 3776105, "248–250 RITCH", zoning CMUO, surveyed corner geometry; and 3776106, 3776456, 3776144, 3776120, 3776093, 3776128 for the block face
- `https://data.sfgov.org/resource/ramy-di5m` (DataSF EAS addresses) — 248 and 250 Ritch on the same parcel; 246 with 24 unit rows; 252/254 on 3776106
- `https://data.sfgov.org/resource/wv5m-vpq2` (SF Assessor secured roll) — 1915, 2 storeys, 2 units, 9 rooms, 2,100 sq ft on a 1,873 sq ft lot, class F
- `https://data.sfgov.org/resource/i98e-djp9` (SF Building Permits) — the seven records listed in 2.1; the load-bearing ones are the 2008 pair (both "2 → 2 storeys", wood frame, the rear-only vinyl siding, the chimney removal) and the 2025 front-stair repair
- `https://data.sfgov.org/resource/ynuv-fyni` (DataSF Building Footprints, LiDAR-derived) — SF3776105 (657 cells), SF3776456 (246 Ritch), SF3776106 (252–254 Ritch)
- `https://data.sfgov.org/resource/3psu-pn9h` (DataSF street centrelines) — CNN 11039000, Ritch St between Bryant and Brannan, bearing 135.08 deg — **this is how the street side was established, not the address point**
- https://augrented.com/sf/3776105-248-250-ritch-st — the building summary: 1915, two units, two storeys, the 2023 reroof cost, the plumbing history, the January 2025 fallen tree
- https://socketsite.com/archives/2009/08/from_sli_to_sro_for_246_ritch_street_as_proposed.html and https://socketsite.com/archives/2012/09/five_stories_and_nineteen_studios_ready_to_rise_at_246.html — 246 Ritch next door: a 4,130 sq ft derelict building demolished for a five-storey, 50-foot, 19-unit SRO/studio block. **This is why the LiDAR maximum on our lot is not our building** (2.15)
- Google Street View panoramas `NZPnD4HS00ZlmXcGCinZew` (2025, the one rectified in 2.15), `HQ6do5b67CwJjoJKQJ0G3w`, `Ygw6B2E0AIVV9jLc04IjdQ` — the north-east elevation, **observed and measured**
- Google Maps satellite, z21 tiles over `37.78017,-122.39572` — the roof outline, the rear garden and the block face, **observed**, with the surveyed parcel ring overlaid
- Exa search (18 Aug 2026), queries "248 Ritch Street San Francisco building", "250 Ritch Street San Francisco", "248-250 Ritch St SF 94107 flats", "Ritch Street SoMa San Francisco alley cottages history" — **ten results, and nine of them are about 246 Ritch, not this building.** The one that is (augrented) is a permit-derived summary. There is no architectural press, no listing photography and no Wikipedia entry for this house. That absence is itself a finding: the visual record here is Street View and the satellite, and nothing else

### 2.3 Orientation and placement

Ritch Street is a 25-foot alley running Bryant to Brannan through the middle of
the block, on the SoMa 45-degree grid: its centreline bears **135.08 deg /
315.08 deg**. This lot is on the **south-west** side, so the house faces
**north-east** across the alley.

The surveyed parcel is a 7.601 x 23.9 m rectangle. Its two street corners are, in
app metres (`+x` east, `+z` south, projection per AGENTS.md):

```
A = (3687.77, -1126.69)   south-east front corner, party line with 252-254
B = (3682.40, -1132.07)   north-west front corner, party line with 246
```

giving a frontage line bearing **315.05 deg** (A → B) and a front outward normal
of **45.05 deg true**. The house occupies the front **13.9 m** of the lot,
built to the street line and to both side lines, so the built quad is:

```
( 3687.77, -1126.69)   E corner  — front x south-east party wall
( 3682.40, -1132.07)   S corner  — front x north-west party wall
( 3672.56, -1122.25)   W corner  — rear  x north-west party wall
( 3677.93, -1116.87)   N corner  — rear  x south-east party wall
```

Its centre — **the manifest anchor** — is `(3680.16, -1124.47)` =
**`-122.3956780, 37.7801725`**.

Relative to that anchor, in Blender coordinates (metres, `+X` east, `+Y` north):

```
(  7.61, -2.22)   E corner   front x SE party wall
(  2.24, -7.60)   S corner   front x NW party wall
( -7.61,  2.22)   W corner   rear  x NW party wall
( -2.24,  7.60)   N corner   rear  x SE party wall
```

| Edge | Length | Outward normal (true) | What it is |
|---|---|---|---|
| S corner → E corner | 7.60 m | **45.05 deg (NE)** | **Ritch Street front** — the only public face |
| E corner → N corner | 13.90 m | 135.05 deg (SE) | party wall against 252–254 |
| N corner → W corner | 7.60 m | 225.05 deg (SW) | **rear**, onto the garden |
| W corner → S corner | 13.90 m | 315.05 deg (NW) | party wall against 246 |

Because of the 45-degree heading the axis-aligned bounding box is about
**15.2 x 15.2 m**. That is correct and expected.

**Do not use the OSM ring to place this.** It is Bing-traced and sits about
2.5 m north-west of the survey — far enough that its own centroid lands nearer
246 Ritch's ring than to the middle of this lot. Its *size* (13.84 x 7.88 m) is
good and is used above as a depth check; its *position* is not (2.15).

### 2.4 What each side shows

**North-east (Ritch Street) — observed and rectified to metres.** A 7.60 m wide,
two-storey painted-timber front, cream body with slate blue-grey trim,
composed in two unequal halves.

The **south-east half (t = 0.5 to 3.9 m from the party line)** carries a canted
bay running through both storeys: a flat front face about 2.3 m wide with a
narrow angled return either side. Each level shows a three-light group in the bay
— a narrow sash on each return, a wide one across the front — set in broad flat
cream architraves. The bay is capped at each level by a projecting blue-grey sill
course: one at **5.44 m** under the upper windows, one at **2.31 m** under the
lower ones, and a water table at **1.46 m** where the bay meets the raised
basement.

The **north-west half (t = 3.9 to 7.60 m)** is flat wall. Upstairs it has one
tall window, centred about t = 5.6 m, head at **7.26 m**. Downstairs it is the
entrance zone: a continuous dentilled hood at about **4.0 m**, and under it two
doorways side by side — **250** at roughly t = 4.8 m and **248** at roughly
t = 6.6 m — each reached by its own short blue-grey concrete stoop, the
north-west one carrying a thin metal handrail. Both doors are recessed a few
tens of centimetres behind the wall plane.

Across the top, a **bracketed cornice**: a row of modillion brackets over a
dentil band, with a plain crown above. It projects roughly 0.35 m, steps out and
back around the bay's two angles, and its top edge is the highest point of the
building at **8.50–8.65 m**.

The **raised basement** below the water table is a 1.46 m band, painted the same
blue-grey as the trim, with one small square window under the bay and a service
opening toward the north-west end.

**South-east (party wall, 13.9 m) — inferred.** Blind. 252–254 Ritch is a
building of the same era and within 0.1 m of the same height (LiDAR median
8.04 m against 7.95 m), built to the same party line, so almost none of this wall
is ever exposed. The 2008 permit that removed two fireplaces describes their
chimneys as "1/2 way back on side", which places at least one chimney breast on
one of these two walls about 7 m back. Model both flanks as plain cream wall with
the cornice returning a short distance and stopping.

**South-west (rear, 7.60 m) — inferred, and nothing observed it.** The 2008
permit put **vinyl siding on the back of #250 only**, "not visible from the
street" — so the rear is a mixed, utilitarian elevation, not a designed one. A
1915 two-flat of this type would carry a rear stair and small windows. Keep it
plain: siding, two or three modest openings, a rear door onto the garden, no
cornice. Do **not** invent a second bay.

**North-west (party wall, 13.9 m) — inferred.** Blind, and unlike the other flank
it *is* exposed: 246 Ritch next door is 15.87 m tall, nearly twice this house, so
this wall is a visible cream flank in the app whenever the camera is north-west of
the site. It deserves the same care as the front: flat cream siding, the cornice
returning, and nothing else.

**Top — a designed facade.** A flat roof at **7.95 m** behind the cornice, which
stands 0.55–0.7 m proud of it on the street side. Re-roofed May 2023, so the
membrane is clean and light. Nothing on the satellite frame contradicts a plain
deck; design it as one, with a small stair bulkhead or roof hatch toward the
rear, two or three vent stacks, and the chimney the permits imply. The rear
parapet is lower than the front one — SF flats of this type raise only the street
face.

### 2.5 Recognition cues (ranked)

1. **The canted two-storey bay** on the left half of a 7.6 m front. Everything
   else about this house is generic; the bay is what a person points at.
2. **The bracketed cornice** stepping around the bay — the one piece of real
   ornament, and the line that reads from across the alley.
3. **Twin stoops, twin doors, one hood.** Two front doors in 7.6 m is the visible
   signature of a two-flat and the reason the address is a range.
4. **Cream over blue-grey.** The body/trim split is unusually clean and is the
   colour memory of the building.
5. **Its size next to 246.** Two storeys against five, immediately north-west.
   The model cannot draw the neighbour, but getting this height exactly right is
   what makes the contrast land in the scene.

### 2.6 Miniature translation

Per §22 of the style bible, and the same reductions that worked on 49 South Park:

- **One volume, one bay, one cornice.** The house is a single rectangular prism
  7.60 x 13.90 x 8.0 m with a bay added to the front and a cornice band on top.
  Do not model wall thickness, do not model the light wells.
- **Chunky ornament, few pieces.** The modillion brackets become a row of small
  bevelled blocks — eight to ten across the front is plenty; the dentil band
  becomes one scored strip, not individual teeth. Bevel 0.10–0.15, 2 segments.
- **Windows as recessed geometric openings**, `Toy_glass` set 0.06–0.08 m behind
  a `Toy_trim` architrave. Nine openings on the street face (three per bay level,
  two upper flat-wall/entry, one basement) and three or four on the rear. None
  on the party walls.
- **The two entries read as one event**: one hood, one recess, two door leaves,
  two stoops. Do not model handrail balusters — one slim bar is enough.
- **Semantic exaggeration, sparingly.** Push the bay's projection to ~0.55 m
  (real is nearer 0.4) and the cornice to ~0.40 m so both survive at diorama
  scale. Do not exaggerate the height: the whole point of this asset is that it
  is short.
- **Simplify again at the end.** If the front reads at the aerial camera with the
  bay, the cornice and the twin doors, everything else is optional.

### 2.7 Massing recipe

Heights are metres above the model's z = 0 (the pavement), all measured in 2.15
unless marked.

| # | Element | Extent |
|---|---|---|
| 1 | Main prism | the 7.60 x 13.90 m quad of 2.3, z 0 → 7.95 |
| 2 | Raised basement band | same plan, z 0 → 1.46, `Toy_roofd`-family blue-grey; front face only needs the two small openings |
| 3 | Water table | a 0.10 m proud strip at z 1.40–1.52 across the front and returning 0.4 m onto each flank |
| 4 | Canted bay | front face 2.30 m wide, two 0.55 m returns at 45 deg, projecting 0.55 m, z 1.46 → 7.60; centred at t = 2.2 m from the south-east party line |
| 5 | Bay sill courses | 0.12 m proud caps at z 2.25–2.37 and z 5.38–5.50, following the bay's three faces |
| 6 | Lower windows | bay group: 0.55 / 1.30 / 0.55 m wide, z 2.37 → 4.00 |
| 7 | Entry hood | dentilled band, z 3.95 → 4.25, from t = 4.0 to t = 7.60, projecting 0.30 m |
| 8 | Entry recess | z 1.46 → 3.95, from t = 4.3 to t = 7.60, set back 0.35 m; two door leaves 0.95 m wide at t ≈ 4.6 and t ≈ 6.3 |
| 9 | Stoops | two blue-grey blocks, 1.2 m deep, stepping 0 → 1.46 m, one under each door; handrail bar on the north-west one |
| 10 | Upper windows | bay group as #6, z 5.50 → 7.26; single flat-wall window 0.90 m wide at t ≈ 5.6, z 5.60 → 7.26 |
| 11 | Cornice | brackets + dentil + crown, z 7.60 → **8.60**, projecting 0.40 m across the front and returning 1.0 m onto each flank, stepping around the bay |
| 12 | Roof deck | flat at z 7.95, `Toy_steel`; front parapet inside face at 8.40, rear upstand 8.15 |
| 13 | Roof plant | stair bulkhead ~1.6 x 1.2 x 0.9 m at the rear third; chimney 0.5 x 0.5 x 1.1 m on the south-east flank about 7 m back; two vent stacks |
| 14 | Rear elevation | plain wall, three openings, a rear door at z 1.46, no cornice |

The bounding-box top **must** be #11's crown at exactly 8.60 m. #13's chimney
must stay below it — cap it at 8.5 m if it wants to be taller.

### 2.8 Materials and palette

Start from `artifacts/49-south-park/build_49_south_park.py`'s map and change the
body and trim. All flat, roughness ~0.85, no textures, no alpha.

| Material | Hex | Used for |
|---|---|---|
| `Toy_cream` | `f2ede3` | the body — every square metre of siding on all four sides |
| `Toy_trim` | `f3efe6` | window architraves, the cornice crown and brackets, the entry hood |
| `Toy_stone` | `d9d2c2` | the dentil band and the bay's flat returns, so the ornament separates from the wall without a second colour |
| `Toy_steel` | `9aa0a6` | the slate blue-grey trim: sill courses, bay caps, water table, stoops, basement band, door leaves. **The building's second colour, and the one that makes it recognisable** |
| `Toy_glass` | `2a4d73` | all windows |
| `Toy_ink` | `3a3530` | the entry recess interior and the basement service opening |
| `Toy_roofd` | `45454a` | the chimney cap and vent stacks only |
| `Toy_glassl_Glow` | `6f95b8` | the lit windows at night — see below |

**Night state (required).** This is a house, not a landmark, and its night state
should read as *domestic*: warm, partial, uneven. Light the **bay windows on both
levels** (the hero glow: six panes, the shape of the bay picked out) plus the
**two door lights**, and leave the flat-wall upper window and the rear dark. Use
`Toy_glassl_Glow` (`6f95b8`) as slim shells set **proud** of the opaque
`Toy_glass` pane — never a closed shell around it. Two recorded traps apply here:
a closed glow shell is two alpha layers and reads ~23% by day, tinting the
facade; and a `_Glow` material's **base** colour is its night appearance, so
judge the colour unlit before trusting a night render.

### 2.9 Top surface

The camera looks down and this roof is 60% of what anyone sees. It is also, on
the evidence, plain — so the design job is composition, not invention:

- a light `Toy_steel` membrane deck at 7.95 m, one plane, no slope worth modelling
- the front parapet standing 0.45 m above it and the rear upstand 0.20 m, so the
  roof reads as a shallow tray tipped toward the garden
- a stair bulkhead in the rear third, offset to the north-west flank
- one chimney on the south-east flank about 7 m back (the permits' "1/2 way back
  on side")
- two vent stacks, small, near the bulkhead
- **nothing else.** No solar, no deck furniture, no planters: there is no evidence
  for any of it, and a plain roof between 252's plain roof and 246's five-storey
  wall is the honest reading

### 2.10 Scope

**In:** the house — massing, bay, cornice, entries, stoops, raised basement,
rear elevation, roof, roof plant.

**Out:** the rear garden and its trees and fence (real, but ground, not
building); Ritch Street and its pavement; the utility pole and overhead wires
directly in front of the house; 246 and 252–254 Ritch; vehicles; people;
plinths; cameras; lights.

The rear-garden exclusion is deliberate and is the one scope decision worth
re-reading. The Case B exclusion in 2.13 clears the whole parcel's procedural
footprint, so the rear third will be bare ground in the app. That is correct —
it *is* bare ground, planted. Do not add a ground plate to fill it: ground-plane
assets in this project must be terrain-draped, and the loader seats an asset
from a single elevation sample at the anchor, which over 24 m of lot with a
1.24 m LiDAR ground range would float or sink one end.

### 2.11 Triangle budget

Cap **7,000** — a small secondary building with one public face, and the cap
should bind. Suggested split: main prism, party walls and rear ~0.6k; raised
basement, water table and stoops ~0.7k; the bay with its two sill courses ~0.9k;
nine front openings with architraves and recesses ~1.5k; the entry hood, recess
and two door leaves ~0.7k; the cornice — crown, dentil strip and ten brackets,
stepping around the bay ~1.4k; roof deck, parapets, bulkhead, chimney and vents
~0.7k; glow shells ~0.3k.

The runaway risk here is **the cornice**. Ten brackets modelled as bevelled
solids that step around two 45-degree bay angles is easy to write as thirty
pieces. Build one bracket and array it; make the dentil band a single scored
strip. If the count passes 7,000 this is where it went.

### 2.12 Draft manifest entry

```json
{
  "id": "248-ritch",
  "file": "248-ritch.glb",
  "anchor": [
    -122.3956780,
    37.7801725
  ],
  "targetHeightM": 8.6,
  "cat": 2,
  "name": "248-250 Ritch Street",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

`dims` and `tris` are placeholders until the asset is built and validated.
Append this entry to `landmarks_manifest.json` **as text**, not by parsing and
re-serialising the file — `JSON.stringify` rewrites `11.0` as `11` and produces a
spurious diff across other landmarks.

### 2.13 Integration notes (for later, not this task)

- **New landmark — Case B.** Add a `pipeline/lib/landmarks.mjs` entry and re-bake
  the affected tiles, or the baked procedural building on this footprint will
  stand inside the GLB. Note the id is camelCase with the digits kept:
  **`248Ritch`**.

- **The registry point is NOT the manifest anchor here, deliberately.** The
  manifest anchor `-122.3956780, 37.7801725` is the centre of the built quad,
  which is where the model must sit. Measured from *that* point the exclusion
  window is only (1.95, 2.88) m — 0.93 m wide — because the misregistered OSM
  ring pulls one way and 252–254's equally misregistered Overture ring pulls the
  other. Moving the circle's centre 5.4 m south-west, to
  **`-122.3957213, 37.7801827`** (still inside the house, on the north-west flank
  8.9 m back), opens the window to **(0.92, 5.04) m**. Use:

  ```
  id: '248Ritch', lon: -122.3957213, lat: 37.7801827, height: 8.6, exclude: 3
  ```

  2.08 m of margin below, 2.04 m above — the middle of the band.

- **The exclusion window, measured against the real bake input.** `excluded()` in
  `pipeline/buildings.mjs` drops a footprint when its centroid **or any ring
  vertex** falls inside the circle — but only *after* `simplifyRing(ring, 0.6)`.
  Measuring on the raw rings is wrong and gives a window less than half as wide,
  because 0.6 m simplification deletes exactly the small jogs that sit closest to
  this lot. Measured on the simplified rings, from the registry point above:

  | Polygon | Triggers at | Via |
  |---|---|---|
  | this building, DataSF SF3776105 | **0.91 m** | nearest ring vertex — **the FLOOR** |
  | this building, Overture / OSM way 147508934 (`height=7`) | **0.92 m** | nearest ring vertex |
  | 252–254 Ritch, Overture / OSM way 147508935 (`height=8`) | **5.04 m** | nearest vertex — **the CEILING** |
  | 252–254 Ritch, DataSF SF3776106 (h 8.04) | 6.07 m | nearest vertex |
  | 246 Ritch, Overture / OSM way 1174904714 | 7.33 m | nearest vertex |
  | 246 Ritch, DataSF SF3776456 (h 15.87) | 7.83 m | nearest vertex |

  The safe window is **(0.92, 5.04) m**; **use `exclude: 3`**. A correct exclusion
  drops **exactly two rings** — the DataSF footprint and its Overture/OSM twin.
  If `verify-rebake.mjs` reports one, the Overture gap-fill re-added the building
  (`addBuilding()` returns null on exclusion, so `markOccupied()` never ran and
  the twin is always re-attempted); if it reports three or more, the circle has
  eaten a neighbour and the first casualty is 252–254, which would leave a hole
  in the alley wall. **Do not go above 4.5 m under any circumstance**, and treat
  a count of exactly two as necessary but not sufficient — confirm from the tile
  which rings went, not how many.

- **`verify-rebake.mjs` compares per-cell counts and can call a working exclusion
  "dropped nothing"** when a gap-fill happens to replace the count elsewhere in
  the same 500 m cell. Settle it by decoding the tile and checking that no
  geometry stands within 8 m of the anchor, not by the count.

- **Do not set `clearTrees`.** The street tree opposite and the garden trees
  behind are real. At 3 m the radius clears neither, which is right.

- `loadRadius`: the default formula gives `max(2500, 8.6 x 30) = 2500` m. Take
  the default. This is emphatically **not** an `alwaysLoaded` asset.

- **Camera preset.** `app/src/camera.js` places the camera at
  `(sin(yaw), sin(pitch), cos(yaw)) x distance` from the pivot and the project's
  `+z` is south, so app yaw = 180 − true bearing. This building's one public face
  looks 45.05 deg, giving **`yaw: 135`** — the eye on Ritch Street, north-east of
  the pivot, square onto the front. That is the same value `560Third` arrived at
  by render for a 44.1 deg elevation two blocks away, which is the strongest
  available corroboration. Start from
  `camera: { distance: 120, yaw: 135, pitch: 28 }` and tune against the live
  scene. **No `key`:** at 8.6 m this is texture in the alley, not a destination.

- **Batch mode applies.** Other landmarks are in flight. Run the full Case B bake
  and the full local QA on it — an unbaked check proves nothing here, because the
  procedural block on this footprint is 7 m tall and would hide the asset — then
  `git checkout -- app/public/tiles api/_data` before committing, and commit
  source only. `git diff --name-only origin/main` must list nothing under
  `app/public/tiles/` or `api/_data/`.

- **The shared landmark `BatchedMesh` is close to full in SoMa.** There are
  already twelve integrated landmarks within 130 m of this one. Check the buffer
  in the console before blaming this asset for another landmark disappearing.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Bounding-box top **exactly 8.60 m** — the cornice crown, not the chimney and
      not a vent (loader scale lands at 1.0)
- [ ] XY bbox ~15.2 x 15.2 m, which is what a 7.60 x 13.90 m building at 45 deg gives
- [ ] Frontage **7.60 m** and depth **13.90 m** measured in plan, not eyeballed,
      and not rounded toward a squarer building
- [ ] The roof deck sits at 7.95 m and the front parapet inside face at 8.40 m
- [ ] The bay is on the **south-east** half of the front and the two entries on the
      **north-west** half — not mirrored
- [ ] Two door leaves, two stoops, one continuous hood
- [ ] Both party walls and the rear carry no cornice ornament and no bay
- [ ] The rear garden is **not** in the export, and no ground plate is
- [ ] Triangles at or under 7,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the six bay panes and the two door lights; glow shells proud
      of the opaque glazing, never a closed shell around it; the `_Glow` base
      colour judged unlit
- [ ] No utility pole, no overhead wires, no street tree, no neighbours
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (per-object signed
      volume for the union of solids; ray test residual <= 0.15%)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + the square-on 45.05 deg facade view + contact sheet +
      night render, all regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed
- [ ] Any 2.15 question this task answered is answered **in `REPORT.md`**, with
      the evidence that answered it

### 2.15 Open questions, risks, and the measurements behind 2.1

**1. Why `hgt_maxcm` is refused.** The LiDAR summary for SF3776105 reports a
maximum of **14.27 m**. Taking it would make this a five-storey building. It is
not: the Assessor says two storeys and every one of seven permits from 1996 to
2025 records "2 → 2". The tell is that `hgt_maxcm` on this record is describing
the **five-storey neighbour**: 246 Ritch was rebuilt in 2012–13 as a 50-foot,
19-unit block (SocketSite, and its own LiDAR record reads median 15.87 m), and
its wall stands on the shared party line. A handful of boundary cells is all it
takes. The January 2025 fallen-tree report on this address is a second candidate
explanation for a few high returns. Either way the maximum is not the roof.

**2. How the height was actually derived — twice, independently.**

*Method A, the LiDAR mixture.* The summary has **mean 6.24 < median 7.95 < mode
8.27** with **sd 3.08 m** over 657 cells, which is the signature of a two-level
footprint, not a noisy one-level one. Solving `f·H + (1−f)·L = mean` and
`f(1−f)(H−L)² = sd²` for the high level, with H fixed at the value method B
returns, gives **f = 0.650, L = 2.04 m**. Run the other way — fixing f from the
OSM ring's share of the LiDAR ring (0.62) and solving for H — it gives
**H = 8.65 m, L = 2.30 m**. The two-level structure is the house (high) and the
garden with its shrubs and fence (low), and f = 0.650 of 164.25 m² is
**106.8 m²** of house, i.e. **14.05 m** of depth on a 7.601 m frontage. That is
where 2.1's built depth comes from, and it agrees with the OSM oriented bbox
(13.84 m) to 0.2 m without being derived from it.

*Method B, the rectified panorama.* Street View pano `NZPnD4HS00ZlmXcGCinZew`
was solved rather than trusted. Its reported position places the lens 5.32 m from
the block face; solving instead from **three collinear surveyed corners** — the
far corner of 252–254's parcel, the 252|248 party line, and the 248|246 party
line, spaced 7.601 m apart — against their observed columns in the zoom-3
equirectangular tiles puts the camera **8.56 m out** and essentially opposite the
252|248 party line. That is a 3.9 m correction, and it is the difference between
a facade that measures 4.3 m wide and one that measures 7.60 m. **This is the
recorded failure mode for Street View photogrammetry in this project and it
happened again here.** With the corrected camera and a 2.5 m lens height, the
cornice top reads **8.50 m ± 0.4**.

*Why the two agree.* The rectification also returns the internal storey
structure: main floor at **1.46 m**, window heads at **4.00** and **7.26 m**, i.e.
**3.26 m floor to floor**. Stacking 1.46 + 3.26 + 3.26 puts the second-floor
ceiling at **7.98 m** — against the LiDAR's median roof of **7.95 m**. Neither
number was tuned to the other. That coincidence is what licenses "measured"
rather than "estimated" in 2.1, and it pins the 2.5 m camera-height assumption to
about 0.1 m.

**3. The rear elevation and both party walls are unobserved.** Nothing in the
record — no listing, no press, no Sanborn sheet consulted here — shows them. 2.4
infers them from the type and from two permit fragments (rear vinyl siding on
#250; chimneys "1/2 way back on side"). If the executing agent finds a historic
survey or any rear-yard photograph, that outranks 2.4 and belongs in
`REFERENCE.md` and `REPORT.md`.

**4. The exact bay geometry is rectified, not surveyed.** The bay's width,
projection and the two entry positions in 2.7 come from the panorama
rectification, which is good to roughly ±0.15 m horizontally. Treat them as
proportions to hit, not as survey.

**5. Scope is safe on the one axis that usually bites.** The parcel's address
range is **248–250 and nothing else**, and no sibling worktree or asset plan
exists for 246 or 252–254. This is one asset for one parcel with no risk of a
second session building an overlapping model of the same mass — the failure that
produced the 21/27 South Park and 92/96 South Park duplicates. Re-check
`ls ~/sf-worktrees/` before starting anyway; it costs nothing.

**6. The honest argument against building this at all.** This is a plain
builder's two-flat with no architect, no press and no landmark status, and the
building kit exists precisely to fill alley walls with exactly this. The case for
a bespoke asset is that it is the **last pre-1920 domestic fabric on this face of
Ritch Street**, standing directly against a 2013 five-storey block, and that the
height contrast is the whole story of what happened to SoMa. That is a real
argument, but it is an argument about *one* building. It does not extend to
252–254, and the next Ritch Street cottage should go to the kit.
