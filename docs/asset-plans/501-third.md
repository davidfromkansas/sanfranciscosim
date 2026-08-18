# 501 Third Street — SF-SIM asset plan

> **CORRECTION, 18 August 2026 — this plan's street orientation is wrong, and
> the shipped asset does not follow it.** The plan puts the 3rd Street elevation
> on the NE face. The NE face is the mid-block party wall. Measured against the
> bake's own street centrelines (`pipeline/data/streets_datasf.geojson`) and the
> neighbouring DataSF footprints, and cross-checked by running the same method
> on shipped `500-third` as a control: **3rd Street is the SW face (normal
> 225.4°), Bryant Street the NW face (315.6°), Taber Place the SE face (135.7°),
> and the NE face (45.3°) is the party wall against SF3775075.** 501 Third is a
> corner building on 3rd and Bryant with an alley flank and exactly ONE blind
> face, not a one-street building with three party walls. §2.3, §2.4 and §2.13
> below are superseded; `artifacts/501-third/REFERENCE.md` and `REPORT.md` carry
> the corrected orientation and the measurements behind it. REPORT beats plan.

A 1920 unreinforced-masonry industrial loft holding the **west corner of 3rd
and the cross street**, a three-storey rhombus on the 45° SoMa grid with big
steel-sash factory windows on every elevation, a painted masonry parapet, and a
small rooftop bulkhead that is the building's crest. It is the low neighbour of
**500 Third Street** (26.5 m, the big five-storey concrete loft one block north
on 3rd) and sits among the small Third Street landmarks already in the scene —
550 Third (11 m), 551 Third (6.6 m), 599 Third (18.3 m). Its long-time
ground-floor tenant was **Gallery 16** (contemporary art gallery, 1993–2025);
One Heart Press (letterpress) shared the building.

It is a modest, characteristic SoMa loft — not a skyline piece. Its job in the
diorama is to be one more well-made diamond on the 3rd Street corridor, reading
as the same toy-box family as its neighbours without repeating their palette.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/501-third/`. This document is the plan only: Part 1 is the runnable
task prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `501-third` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3954601, 37.7813246` (footprint vertex centroid = OSM centroid, measured) |
| Target height | **16.4 m** (rooftop bulkhead crest; main parapet 14.0 m, both measured) |
| OSM footprint | 23.6 × 25.05 m rhombus on the 45° SoMa grid, 592 m2 (OSM way/147689541, measured) |
| Triangle cap | 12,000 |
| Category | `3` (Office) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 501 Third Street GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of 501 Third Street in San Francisco and
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
8. `artifacts/500-third/` and `artifacts/550-third/` — the closest neighbours:
   500 Third is the same SoMa industrial-loft type at larger scale (the big
   five-storey concrete block one block north); 550 Third is the small
   two-storey neighbour. This asset must look like it came out of the same toy
   box, must not out-detail 500 Third, and must not repeat its palette (500 is
   warm-grey concrete + charcoal base; 501 should find its own neutral)
9. `docs/asset-plans/501-third.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Must capture

- The rhombus footprint on the 45° SoMa grid — a diamond, not a rectangle.
  23.6 m along the 3rd Street axis (45.7°/225.6°) by 25.05 m along the cross
  axis (315.3°/135.4°), filling its lot corner to corner
- Three storeys above grade: one tall ground floor under two upper floors, flat
  parapet at 14 m. (The assessor says 4 storeys; see 2.15 — resolve before
  modelling.)
- **The steel-sash industrial window grid** — the identity. Large multi-pane
  factory windows on every elevation, framed by painted masonry pilasters and
  spandrel panels. This is a SoMa loft: the walls are more window than wall
- The painted masonry walls — a warm neutral (cream/sand) with a darker
  (charcoal or ink) storefront base at ground level
- The flat parapet with a small rooftop bulkhead (the crest at ~16.4 m) —
  stair/elevator head, the only silhouette event
- The stair and elevator shaft bumps on the exterior (resurfaced 2011, visible
  as slight projections on the rear elevations)
- The roof: pale membrane field, the central bulkhead, a roof deck with a
  guardrail (added 2006), and a small mechanical cluster

## Research 501 Third Street independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- All four elevations (3rd Street front, the cross-street front, and the two
  party-wall / rear sides)
- Aerial and roof views — the roof carries most of what the app's camera sees
- Ground-level views, day and night
- Publicly available drawings, plans, permits or survey documents
- **The storey count, which the sources disagree about.** The assessor's roll
  says 4 storeys; OSM tags `building:levels=3`; DBI permits reference 1st, 2nd
  and 3rd floors. Resolve it: is there a basement or mezzanine that makes the
  assessor's 4, or are there genuinely 4 above-grade floors? Say what you
  resolved it with.
- **The rooftop bulkhead height, which this dossier derives from LiDAR.** The
  2010 permit "build new accessories room and new storage room over extg roof"
  and the 2011 "alteration of (e) elevator shaft to mechanical room" establish
  that the bulkhead exists; the LiDAR `hgt_max` of 16.42 m gives its crest. A
  measured elevation, a planning drawing or a dated photograph beats the LiDAR.
  The LiDAR `peak_1st_m` of 22.38 m is almost certainly a neighbour bleeding
  into edge cells (8.6 m above the median, sigma only 0.92 m) — do not use it.

Prefer architect/engineer publications, owner or institutional material,
planning and permitting documents, architectural press, geolocated photography,
and aerial/satellite imagery. Never rely on a single photograph, a single
AI-generated image, or a single unsourced 3D model. Separate verified facts from
visual inference; if sources disagree, document the disagreement and decide.

## Create a reference dossier

Write `artifacts/501-third/REFERENCE.md` containing: source links and what each
establishes; verified dimensions and location; orientation; observations from
all four sides and above; the 3-5 strongest recognition cues; features to
preserve; features to simplify; uncertainties and conflicting evidence. A
contact sheet of attributed reference thumbnails is welcome if legally
permissible — do not commit copyrighted full-resolution imagery.

## Make your own design decisions

Follow the conversion process in `docs/styles/miniature-toy.md` §22: identify
the recognition cues, strip nonessential information, rebuild the massing from a
few confident volumes, exaggerate only the signature features, simplify the
facade into broad rhythms, deliberately design every surface visible from
above, evaluate from the app's high three-quarter aerial camera, then simplify
again.

This building's job is to be a **clean diamond prism with a window-grid identity
and one small roof event**. Its charm is the SoMa loft type: a disciplined grid
of big windows on a 45° rhombus, a quiet parapet, and one bulkhead. §5 (windows
as graphical rhythm) and §10 (roofs as secondary facades) govern; §11 (landmark
geometry) does not — there is no tower, no crown and no signature curve here,
and inventing one would be a lie about a very ordinary and very characteristic
SoMa building. Spend the budget on the window grid, the two-tone base/body
split, and a roof that reads as a working roof with one bulkhead and a deck.

At 16.4 m this is one of the shorter landmarks in the set, sitting between
500 Third (26.5 m) and 550 Third (11 m). Resist over-detailing it: from the
app's camera it is three storeys on the 3rd Street corridor, and what has to
survive is the diamond footprint, the window grid, and the two-tone reading,
not the mullion count.

The finished asset must be immediately recognizable as 501 Third Street,
consistent with the real building from all four sides and above, architecturally
credible, and a premium handcrafted miniature — not photorealistic, not voxel
art, not generic low-poly, and never accurate in one view while invented in the
others.

## Scope of the exported asset

Export the 501 Third Street building itself, including its parapet, rooftop
bulkhead, roof deck and guardrail, mechanical plant, storefront base, window
grid, and the stair/elevator shaft bumps.

Do not include unrelated surrounding city geometry: 3rd Street, the cross
street, neighbouring buildings, street furniture, street trees, people,
vehicles, plinths, cameras or lights. Temporary context may appear in review
renders but must not leak into the GLB.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary
`.glb`; real-world meters; origin at base center; minimum geometry Z ~ 0;
applied transforms; no negative scales; outward normals; no duplicate or foreign
geometry; no image textures; no transparency; flat-color materials named `Toy_*`
from the project palette; `_Glow` suffix only on surfaces that glow at night; no
`Toy_body`; no cameras, lights, animations, armatures or constraints; no external
dependencies; at most 12,000 triangles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model
drops into the city at its real-world heading — the loader applies no rotation
(`placeGeneric` in `app/src/assets.js` only scales and positions). The 3rd
Street front faces north-east (outward normal 45.7 deg true), so the contract's
"front faces −Y" cannot be honoured literally. Real-world orientation wins
(AGENTS rule 5). Record the decision and the measured heading in `REPORT.md`.

**Height normalization:** make the exported bounding-box top land exactly on the
verified architectural height (16.4 m, the bulkhead crest), so the loader's
`targetHeightM / measuredHeight` scale is 1.0. Nothing may rise above the
bulkhead.

## Reproducible Blender workflow

Blender 4.5 LTS or newer, headless only: `blender -b --python script.py -- args`;
no GPU, so use Workbench or CPU Cycles.

Keep `artifacts/501-third/build_501_third.py` (deterministic build script),
`artifacts/501-third/501-third.blend`, and `artifacts/501-third/501-third.glb`.
The script must rebuild the model reliably enough for future revision. Do not
modify or rename an unrelated existing GLB to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`501-third-top.png`, `501-third-north.png`, `501-third-east.png`,
`501-third-south.png`, `501-third-west.png`, plus `501-third-contact-sheet.png`,
at least one high three-quarter aerial beauty render `501-third-aerial.png`, and
a night render `501-third-night.png`.

The four elevations must share scale, framing, lighting, exposure and
projection; use orthographic or long-lens cameras; label directions from the
researched orientation; the aerial view uses the style bible's camera
assumptions (30-50 degrees down, long lens) and must show the **rhombus
footprint** and the rooftop bulkhead — the diamond and the bulkhead are the hero
views for this asset. Simple tabletop lighting, neutral warm background, minimal
depth of field, and every image must depict the same exported model.

## Validate the exported GLB

Re-import `501-third.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture
count, camera count, light count, animation count, applied-transform status,
negative-scale status, normal-orientation status, unexpected geometry, and
per-material contract compliance. Normals are checked two ways: per-object
signed volume (authoritative for a union of closed solids) and a deterministic
visibility-ray test (≤ 0.15% residual, zero for single shells). Render at least
one review image from the re-imported asset. Write
`artifacts/501-third/validation.json` and `artifacts/501-third/REPORT.md`.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include
this draft entry in `REPORT.md`. Do not edit the production manifest in this
task.

```json
{
  "id": "501-third",
  "file": "501-third.glb",
  "anchor": [
    -122.3954601,
    37.7813246
  ],
  "targetHeightM": 16.4,
  "cat": 3,
  "name": "501 Third Street",
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
for that, together with the integration notes in `docs/asset-plans/501-third.md`.
````

---

## Part 2 — Research and design dossier

Compiled 15 August 2026 from the sources in 2.2. Values marked *inferred* or
*estimated* are visual or derived, not published figures — the executing agent
must re-verify anything it relies on.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Address | 501 3rd Street, San Francisco, CA 94107 | OSM addr tags, DataSF parcel, DBI permits |
| Parcel | Block 3775, Lot 073 | DataSF parcels `acdm-wktn` (measured) |
| Lot area | 6,100 sf = 567.7 m2 | Assessor secured roll `wv5m-vpq2` (measured); the parcel polygon integrates to 592 m2 (OSM) / 568 m2 (LiDAR cells) |
| Zoning | Central SoMa Mixed Use Office (CMUO) | DataSF parcels |
| Built | **1920** | Assessor secured roll, every year 2023–2025 |
| Construction | Unreinforced masonry building (UMB); assessor construction type `C` | DBI permit 200202280352 ("seismic retrofit of unreinforced masonry building"); assessor roll |
| Storeys | **3 above grade** — OSM `building:levels=3`; DBI permits reference 1st, 2nd and 3rd floors; assessor says 4 (likely includes basement or mezzanine, see 2.15) | OSM tags, DBI permits, assessor roll — *contradicted by assessor, see 2.15* |
| Use | Ground-floor gallery/retail + upper-floor offices; assessor classes the parcel `Industrial` | DBI permits (current use Office/Retail), assessor roll; long-time tenant Gallery 16 (1993–2025), One Heart Press |
| Footprint | 23.6 m (3rd Street axis) × 25.05 m (cross axis) rhombus, 592 m2 | OSM way/147689541, reprojected + measured |
| Building = lot | DataSF LiDAR footprint `SF3775073` integrates to 568 m2 against the parcel's ~567 m2 — the building fills its lot corner to corner, so two of four faces are party walls or near-party | DataSF `ynuv-fyni` (measured) |
| Parapet height | **14.0 m** above grade | OSM `height=14` and SF 2010 LiDAR `SF3775073` hgt median 13.73 m — two independent sources agreeing |
| Rooftop crest | **16.4 m** (bulkhead) | SF 2010 LiDAR `SF3775073` hgt max 16.42 m, corroborated by DBI permits: 2010 "build new accessories room and new storage room over extg roof", 2011 "alteration of (e) elevator shaft to mechanical room" |
| LiDAR maximum (peak) | 22.38 m | same record — believed to be a neighbour bleeding into edge cells (8.6 m above median, sigma 0.92 m), *not* this building (see 2.15) |
| Ground | 5.84 m NAVD88 mean over the footprint | SF 2010 LiDAR `SF3775073` (measured) — flat made ground |
| Anchor | -122.3954601, 37.7813246 | footprint vertex centroid = OSM centroid (measured); the rhombus is a true parallelogram, so vertex centroid = diagonal intersection |
| Grid heading | 3rd Street axis 45.7 / 225.6 deg true; cross axis 315.3 / 135.4 deg true | OSM geometry (measured) |
| Lot condition | Corner lot: 3rd Street front (NE), cross-street front (SE/NW), two party or near-party walls | OSM street geometry + parcel adjacency (measured) |
| Roof deck | Guardrail added 2006 ("roof strengthening, new guardrail at roof deck") | DBI permit 200607146644 |
| Seismic retrofit | UMB seismic strengthening 2002–2006 ($380k) | DBI permits 200202280352, 200312122257 |
| Roof plant | Rooftop accessories/storage room (2010), elevator shaft to mechanical room (2011), VRF mechanical system (2019) | DBI permits |
| Other fabric | Parapet work 1992; reroof 1995; window replacements 2004; fire sprinklers throughout 1986/2011; 2018 voluntary seismic strengthening + ADA upgrades | DBI permits |
| Building area | 18,300 sf assessed | Assessor secured roll |
| Neighbour already in the scene | 500 Third (`500-third`, 26.5 m) 63 m north on 3rd; 550 Third (`550-third`, 11 m) 98 m south; 551 Third (`551-third`, 6.6 m) 103 m south | repo manifest + measured bearings |

### 2.2 Sources

- https://www.openstreetmap.org/way/147689541 — footprint geometry (4-node rhombus), addr tags, `building:levels=3`, `height=14` (Bing-traced)
- https://data.sfgov.org/resource/acdm-wktn.json — DataSF parcels, `blklot=3775073`: address 501 03RD ST, CMUO zoning, the parallelogram polygon, published centroid
- https://data.sfgov.org/resource/wv5m-vpq2.json — Assessor secured roll, block 3775 lot 073: year built 1920, 4 storeys, construction type C, lot area 6,100 sf, building area 18,300 sf, use class Industrial
- https://data.sfgov.org/resource/i98e-djp9.json — DBI building permits, block 3775 lot 073 (37 records, 1986–2019): the 2002 UMB seismic retrofit, the 2006 roof deck + guardrail, the 2010 rooftop accessories/storage room, the 2011 elevator-shaft-to-mechanical-room conversion + stair/elevator shaft exterior re-surfacing, the 2019 VRF mechanical system, and a long run of floor-by-floor office TIs on floors 1–3
- https://data.sfgov.org/resource/ynuv-fyni.json — SF 2010 LiDAR building footprints, record `SF3775073` (`sf16_bldgid` 201006.0005914): 2,273 half-metre cells (≈568 m2, corroborating the OSM polygon), ground mean 5.84 m, height median 13.73 m, height max 16.42 m, sigma 0.92 m, peak_1st 22.38 m
- https://www.checkpermits.com/property/501+03rd+St+San+Francisco+Ca — aggregated permit history with full descriptions and dates, corroborating the DBI feed
- https://gallery16.com/ — Gallery 16 (long-time ground-floor tenant, 1993–2025, closed September 2025); confirms the gallery use and the SoMa location
- https://www.mapquest.com/us/california/gallery-16-304656788 — Gallery 16 listing with address 501 3rd St, corroborating tenancy
- Google Street View panoramas around the block — the four elevations, the storefront base, the window grid, the parapet and the roof bulkhead (verify capture dates and panoids during research)

### 2.3 Orientation and placement

A corner lot in South Beach/SoMa, on the 45° SoMa grid. The 3rd Street frontage
runs 45.7 / 225.6 deg true and the cross-street frontage 315.3 / 135.4 deg true.
The footprint is a true rhombus (parallelogram with equal diagonals ≈ 34.4 m),
so the vertex centroid equals the diagonal intersection exactly.

Measured footprint, reprojected with the app's tangent projection and recentred
on the vertex centroid (x east, y north, metres, CCW):

```
1608947485   (+0.354, -17.175)   south corner  (3rd St lower end)
1608947488   (+17.267, -0.660)   east corner   (3rd St x cross st)
1608947505   (-0.385, +17.170)   north corner  (cross st upper end)
10874867135  (-17.236, +0.666)   west corner   (rear / party wall side)
```

| Edge | Length | Outward normal (true) | What it is — CORRECTED, see the banner |
|---|---|---|---|
| 485 → 488 | 23.64 m | 135.7 deg (SE) | **Taber Place** — the alley flank |
| 488 → 505 | 25.09 m | 45.3 deg (NE) | **party wall** vs SF3775075 (h 14.90 m) |
| 505 → 7135 | 23.59 m | 315.6 deg (NW) | **Bryant Street** front |
| 7135 → 485 | 25.05 m | 225.4 deg (SW) | **3rd Street** front (the address side) |

(The edge lengths and normals were always right; only the street assignment was
wrong. The version of this table shipped before 18 August 2026 read the same
four edges as NE-front / NW-cross-street / two party walls.)

Author `+Y` = north and place the polygon exactly as measured. The contract's
"front faces −Y" cannot be met — the real front faces south-west — so real-world
orientation wins per the README orientation note and AGENTS rule 5.

### 2.4 What each side shows

**North-east (3rd Street) — the address face, 23.6 m.** A painted masonry
industrial loft front. The ground floor is tall and darker: a storefront/gallery
front with glazed entries and a solid base, divided by masonry pilasters. Above
it, two upper floors each carry a row of large steel-sash industrial windows —
a fine grid of small panes in dark frames — recessed behind narrow pilaster
strips with light spandrel panels under each. The parapet is plain and light.
This is the side the camera sees first from 3rd Street.

**North-west (cross street), 25.1 m.** The same elevation language, a few bays
of the same big industrial windows, a ground-floor entry or loading opening.
The corner at 3rd and the cross street is the building's public corner.

**South-west / south-east (the two rear faces).** Plainer painted masonry with
punched windows rather than the big sashes, the stair and elevator shaft bumps
(resurfaced 2011, visible as slight projections), and possibly a roll-up door or
service entry. These faces abut neighbouring lots; confirm during photo research
whether they are true party walls (blind) or exposed with windows.

**Top.** A pale flat membrane field bounded by the parapet, carrying:

1. the rooftop bulkhead near the centre — the stair/elevator head converted to
   a mechanical room (2011), the tallest thing on the building and the crest at
   16.4 m;
2. the accessories/storage room added in 2010, a smaller rooftop box;
3. the roof deck with its guardrail (added 2006);
4. a small mechanical cluster (VRF units, 2019);
5. the parapet running the perimeter.

### 2.5 Recognition cues (ranked)

1. **The 45° rhombus footprint** — a diamond on the SoMa grid, not a rectangle.
   This is the building's strongest plan-form cue from the aerial camera
2. **The steel-sash industrial window grid**, repeated across the street
   elevations — a wall that is more window than wall, in a painted masonry frame
3. **The two-tone base/body split** — a darker storefront ground floor under a
   light painted upper block, the single strongest value contrast
4. **The small rooftop bulkhead** — the only silhouette event on an otherwise
   flat-topped prism, pointing at the stair/elevator head
5. **The 1920 SoMa loft type** — three storeys, tall floors, big windows, flat
   parapet. It reads as the same family as 500 Third but smaller and older

### 2.6 Miniature translation

**Preserve**

- The true rhombus footprint and the 45° heading — the diamond is the identity
- The three-storey proportion: tall ground floor + two upper window bands
- The window grid as the dominant facade language on the street faces
- The two-tone base/body value split
- The flat parapet with one small bulkhead — the only roof event

**Simplify / exaggerate**

- The window grid becomes a clean recessed grid of identical bays, not real
  mullion counts — two upper bands of 4–5 bays per street face
- Ornament becomes two horizontal bands: a base cap and a parapet cap
- The stair/elevator shaft bumps become one or two small projections on the rear
- The roof becomes a membrane field, one bulkhead, one small box, a deck
  guardrail, and one mechanical cluster — no more

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not
a straitjacket — adjust after the first aerial review render.

1. Base prism: the rhombus footprint (23.6 × 25.05 m, 45° heading), z=0 to z=14,
   `Toy_sand` or `Toy_cream` painted masonry walls. Bevel 0.12 m, 2 segments.
2. Storefront base: same plan, z=0 to z=4.5, `Toy_ink` or a darker neutral — the
   ground-floor value contrast. Recessed glazed bays on the two street faces.
3. Window grid: two upper bands (z=4.5–9, z=9–13.5) of large recessed
   `Toy_glass` windows on the two street faces, framed by `Toy_sand` pilaster
   strips and spandrel panels. 4–5 bays per face per band. Rear faces: punched
   windows only.
4. Parapet: `Toy_trim` cap at z=14, projecting 0.3 m, 1.0 m tall.
5. Stair/elevator shaft bump: a small projection on one rear face, z=0 to z=14,
   2–3 m wide, 0.6 m proud — `Toy_sand` matching the body.
6. Roof: flat `Toy_roofd` membrane field. Bulkhead: 4 × 3 × 2.4 m box at z=14 to
   z=16.4, `Toy_roofd` with a `Toy_trim` cap — the crest. Accessories box: 3 × 2
   × 1.5 m at z=14 to z=15.5. Roof deck guardrail: a low `Toy_steel` rail along
   one roof edge. One small `Toy_steel` mechanical unit.
7. Bevel 0.12 m, 2 segments throughout.

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_sand` | `#ece4d4` | main painted masonry walls (warm neutral — distinct from 500 Third's warm-grey) |
| `Toy_ink` | `#3a3530` | storefront base, dark ground-floor value contrast |
| `Toy_trim` | `#f3efe6` | parapet cap, bulkhead cap, base cap band |
| `Toy_glass` | `#2a4d73` | industrial windows (dark blue-gray graphical) |
| `Toy_roofd` | `#45454a` | roof membrane, bulkhead body |
| `Toy_steel` | `#9aa0a6` | roof deck guardrail, mechanical unit |
| `Toy_white_Glow` | `#f7f4ec` | storefront uplight + a few lit upper windows at night |

Night glow: the storefront band uplight plus a few lit upper-floor windows
(restrained — 3–4 windows on the street faces). A working SoMa loft reads as
quietly lit at night, not as a beacon. Keep it to two glow surfaces.

### 2.9 Top surface

A flat roof at 14 m on a small corner lot is very exposed to the app camera.
Design it properly: the central bulkhead (the crest), the smaller accessories
box, a roof deck with a guardrail along one edge, one mechanical unit, and the
parapet perimeter. No clutter — every object earns its place.

### 2.10 Scope

**In the GLB:** the 501 Third Street building itself — rhombus prism, storefront
base, window grid, parapet, rooftop bulkhead, accessories box, roof deck
guardrail, mechanical unit, stair/elevator shaft bump.

**Not in the GLB:** 3rd Street, the cross street, neighbouring buildings, street
furniture, street trees, people, vehicles, plinths, cameras or lights.

### 2.11 Triangle budget

Cap 12,000. Suggested split: base prism + window grid ~6k, storefront base ~1.5k,
parapet + shaft bump ~1k, roof + bulkhead + accessories + guardrail ~2k, bevels
+ margins ~1.5k. This is a small building; spend the budget on the window grid
and the roof, not on ornament.

### 2.12 Draft manifest entry

```json
{
  "id": "501-third",
  "file": "501-third.glb",
  "anchor": [
    -122.3954601,
    37.7813246
  ],
  "targetHeightM": 16.4,
  "cat": 3,
  "name": "501 Third Street",
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

- **New landmark.** Add a `pipeline/lib/landmarks.mjs` entry (`id: '501Third'`,
  camelCase per `camelId()`) and re-bake the affected tiles.
  **`exclude: 11`, NOT the ~20 this plan originally suggested.** That estimate
  reasoned from the half-diagonal instead of measuring, and `excluded()` in
  `pipeline/buildings.mjs` fires on a footprint's centroid *or any of its ring
  vertices* — so 20 m reaches three neighbours. Measured against the real bake
  inputs (`pipeline/data/buildings_datasf.geojson` and
  `overture_buildings.geojsonseq`), by `min(nearest vertex, centroid)` from this
  anchor:

  ```
    3.43 m  own Overture ring (1355349a)      <- floor
    5.70 m  own DataSF ring (SF3775073)       <- floor: both must go
   16.23 m  own footprint's nearest vertex
   16.31 m  DataSF SF3775075 (h 14.90)        <- ceiling: the party neighbour
   17.17 m  Overture 0f2baf8a (h 11)
   19.55 m  DataSF SF3775072 (h 13.53)
  ```

  Band that drops exactly this building's two rings and nothing else:
  **(5.70, 16.23) m**, 10.5 m wide. Shipped **11**, the middle of it, so the
  registry centre needs no offset. Note 11 does not reach this footprint's own
  corners at 17.3 m; it does not need to, and reaching them would delete
  SF3775075.
- Manifest id `501-third` maps directly (no camel conversion needed).
- `loadRadius: 2500` per the default rule `max(2500, 16.4 × 30)` = max(2500, 492)
  = 2500. This is a small landmark, not a skyline piece — stream it, do not make
  it `alwaysLoaded`.
- The nearest neighbour already in the scene is 500 Third (26.5 m), which is
  ~55 m SSW across 3rd Street, not 63 m north as this plan said. At
  `exclude: 11` it is nowhere near the exclusion; the binding neighbour is the
  party-wall building SF3775075 at 16.31 m, which is not a bespoke landmark.
- **Residual, and why it is acceptable:** with `exclude: 11`, SF3775075 survives
  and one of its vertices sits 0.147 m inside this asset's footprint — a shared
  party-wall survey vertex, inside a wall thickness. Clearing it would need
  `exclude` ≥ 16.31, which deletes the whole 14.9 m neighbour for 15 cm of
  overlap. Prove the result from the baked tile rather than from the radius.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Dimensions plausible in meters and consistent with 2.1 (rhombus 23.6 × 25.05, height 16.4)
- [ ] Triangles at or under 12,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the storefront uplight and lit upper windows
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (deterministic ray test)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + contact sheet + night render regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

- **Storey count: 3 or 4?** The assessor's roll says 4 storeys; OSM tags
  `building:levels=3`; DBI permits reference 1st, 2nd and 3rd floors (no 4th).
  The likeliest reconciliation is 3 above-grade floors (ground + 2 upper) with a
  basement or mezzanine making the assessor's 4. With hgt_median 13.73 m and 3
  storeys, that is ~4.6 m per storey — typical for a 1920 industrial loft with
  tall floors. With 4 storeys it would be 3.4 m per storey, unusually short for
  the type. **Resolve with street-level photography before modelling** — count
  the window bands. If there are genuinely 4 above-grade window bands, the
  height and the massing recipe change.
- **The LiDAR `peak_1st_m` of 22.38 m is almost certainly a neighbour bleed.**
  It sits 8.6 m above the median with a sigma of only 0.92 m — a 9σ outlier on a
  roof whose own max is 16.42 m. Treat it as unusable; do not model anything at
  22 m. The `hgt_max` of 16.42 m is the credible crest (the 2010/2011 permits
  establish the bulkhead exists).
- **The rear faces may be party walls.** The LiDAR footprint (568 m2) matches
  the parcel (567 m2), suggesting the building fills its lot corner to corner.
  Two of the four faces may be blind party walls. Confirm during photo research
  — if they are blind, model them as plain painted masonry with no windows.
- **The cross street.** The OSM geometry gives the heading (315.3°) but not the
  street name. 501 3rd St is between Brannan and Bryant on the 3rd Street
  corridor — confirm which cross street forms the corner during research, as it
  affects the address-face identification.
- **No published architectural height was found.** The 14 m parapet and 16.4 m
  crest are LiDAR-derived (corroborated by the OSM `height=14` tag and the DBI
  rooftop-structure permits). A measured elevation or drawing would beat them.
