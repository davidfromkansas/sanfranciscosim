# 590 Third Street — SF-SIM asset plan

A two-storey painted-stucco commercial corner block of about 1905, holding the
**west corner of 3rd and Brannan** with two street elevations, a continuous
glossy-black shopfront band wrapping the whole ground floor, and a parapet that
steps up over the corner itself. Upstairs is plain grey wall with punched
windows and through-wall air conditioners; downstairs is signage — `kinoko`
three times on 3rd, `DIVINE YOGA STUDIO` and a black roll-up garage door on
Brannan, and the blue `CAFE BUENOS AIRES` panel that carries the street number.

It is the low, dark-based counterpart to **599 Third across the street** (18.3 m,
buff stucco and white window grids, the north corner of the same intersection).
Together they make the intersection read as an intersection: 599 is the wall,
590 is the base. Its other neighbours already in the scene are 550 Third (11 m)
and 380 Brannan (12.6 m), both a block away.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/590-third/`. This document is the plan only: Part 1 is the runnable
task prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `590-third` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3946749, 37.7800837` (parcel-polygon centroid = vertex mean, measured) |
| Target height | **9.5 m** (raised corner parapet crest; main parapet ~8.4 m, roof membrane 7.77 m LiDAR-measured) |
| OSM/parcel footprint | 21.28 m along 3rd x 23.10 m along Brannan, a true parallelogram on the 45.2 deg SoMa grid, 491.5 m2 (DataSF parcel 3776114, measured) |
| Triangle cap | 11,000 |
| Category | `4` (Shop) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 590 Third Street GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of 590 Third Street in San Francisco and
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
8. `artifacts/599-third/` and `artifacts/550-third/` — the neighbours already
   built. 599 Third stands directly across 3rd Street from this building and
   the two will be seen in the same frame constantly; this asset must look like
   it came out of the same toy box, must not out-detail it, and must not repeat
   its palette (599 is buff walls + white grids; 590 is grey walls + a black
   base)
9. `docs/asset-plans/590-third.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Must capture

- The two-storey parallelogram block, 21.3 m along 3rd Street by 23.1 m along
  Brannan Street, flat-roofed, filling its lot corner to corner
- **The black shopfront band.** A continuous glossy near-black fascia and
  glazed shopfront wrapping both street faces at ground level, unbroken around
  the east corner. This is the building's strongest cue and the thing that makes
  it legible from the air: a dark ribbon under a pale block
- **The raised corner parapet.** The wall steps up roughly 1.1 m over the
  corner bay, spanning about a third of each street face, with a clean vertical
  jog down to the main parapet on both sides. It is the building's only
  silhouette event and it points at the intersection
- The pale warm-grey painted stucco of the whole upper storey — smooth, plain,
  no cornice, no ornament, a thin dark parapet cap
- **3rd Street (north-east, 21.3 m):** sparse large square windows with dark
  frames; the `CAFE BUENOS AIRES` blue sign panel at the north-west end (this is
  the 590 address); three `kinoko` fascia panels; a flat white blade sign on the
  wall near the north-west end
- **Brannan Street (south-east, 23.1 m):** a longer, more regular rhythm of
  seven or eight tall punched windows, several with through-wall AC boxes under
  them; awnings over the shopfronts; a black roll-up garage door at the
  south-west end
- The two blind party walls (north-west toward the brick warehouse at 574–578
  3rd, south-west toward 414 Brannan) as plain stucco with no openings
- **The roof as a warm brown built-up membrane field**, not grey: a scatter of
  small skylights, two or three mechanical boxes, a small **light well**
  (an actual hole through the roof, 3.5 x 2.2 m, toward the south-west rear) and
  the parapet running the perimeter

## Research 590 Third Street independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- North-east (3rd Street) and south-east (Brannan Street) elevations
- Aerial and roof views — the roof carries most of what the app's camera sees
- Ground-level views of the corner and of the shopfront band on both faces
- Day and night appearance
- Publicly available drawings, plans, permits or survey documents
- **The crest height, which this dossier derives, not quotes.** The LiDAR record
  gives a roof membrane at 7.77 m median with a standard deviation of only
  0.64 m, and OSM independently tags `height=8`. The main parapet at ~8.4 m and
  the raised corner block at ~9.5 m are *estimated* by photogrammetric scaling
  off Street View against the known 23.1 m Brannan face. The LiDAR maximum of
  11.65 m is believed to be the taller brick neighbour bleeding into edge cells,
  **not** a rooftop structure on this building — verify that before using it.
  A measured elevation, a planning drawing or a dated photograph against a known
  neighbour beats all of it. Document what you find.
- **The build date.** The assessor's roll says 1905 for a block that burned in
  April 1906; a post-fire rebuild of 1906–08 recorded under the pre-fire date is
  the likelier reading. Check the Sanborn maps and any Central SoMa historic
  survey before repeating "1905" as fact.

Prefer architect/engineer publications, owner or institutional material,
planning and permitting documents, architectural press, geolocated photography,
and aerial/satellite imagery. Never rely on a single photograph, a single
AI-generated image, or a single unsourced 3D model. Separate verified facts from
visual inference; if sources disagree, document the disagreement and decide.

## Create a reference dossier

Write `artifacts/590-third/REFERENCE.md` containing: source links and what each
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

This building's job is to be a **dark base on a bright corner**. Its identity is
two-tone: a black ribbon at street level under a plain pale block, cut once by
the raised corner parapet. §5 (facade rhythm over mullion count) and §10 (roofs
as secondary facades) govern; §11 (landmark geometry) does not — there is no
tower, no crown and no signature curve here, and inventing one would be a lie
about a very ordinary and very characteristic SoMa corner. Spend the budget on
the shopfront band, the corner step, the Brannan window rhythm and a roof that
reads as a working roof.

At 9.5 m this is one of the shortest landmarks in the set. Resist over-detailing
it: from the app's camera it is two storeys tall next to an 18.3 m neighbour, and
what has to survive is the two-tone reading, not the joinery.

The finished asset must be immediately recognizable as 590 Third Street,
consistent with the real building from all four sides and above, architecturally
credible, and a premium handcrafted miniature — not photorealistic, not voxel
art, not generic low-poly, and never accurate in one view while invented in the
others.

## Scope of the exported asset

Export the 590 Third Street building itself, including its parapets, raised
corner parapet, roof field, light well, skylights, mechanical boxes, shopfront
band, awnings, signage panels and the roll-up garage door.

Do not include unrelated surrounding city geometry: 3rd Street, Brannan Street,
neighbouring buildings at 574–578 3rd or 414 Brannan, the rooftop billboard on
the brick neighbour to the north-west, street trees, street furniture, traffic
signals, people, vehicles, plinths, cameras or lights. Temporary context may
appear in review renders but must not leak into the GLB.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary
`.glb`; real-world meters; origin at base center; minimum geometry Z ~ 0;
applied transforms; no negative scales; outward normals; no duplicate or foreign
geometry; no image textures; no transparency; flat-color materials named `Toy_*`
from the project palette; `_Glow` suffix only on surfaces that glow at night; no
`Toy_body`; no cameras, lights, animations, armatures or constraints; no external
dependencies; at most 11,000 triangles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model
drops into the city at its real-world heading — the loader applies no rotation
(`placeGeneric` in `app/src/assets.js` only scales and positions). The street
faces are normal to 45.2 deg (3rd Street) and 135.1 deg (Brannan Street) true,
so the contract's "front faces −Y" cannot be honoured literally. Real-world
orientation wins (AGENTS rule 5). Record the decision and the measured heading in
`REPORT.md`.

**Height normalization:** make the exported bounding-box top land exactly on the
verified architectural height, so the loader's `targetHeightM / measuredHeight`
scale is 1.0. Note that the bbox top is the **raised corner parapet**, not the
main parapet.

## Reproducible Blender workflow

Blender 4.5 LTS or newer, headless only: `blender -b --python script.py -- args`;
no GPU, so use Workbench or CPU Cycles.

Keep `artifacts/590-third/build_590_third.py` (deterministic build script),
`artifacts/590-third/590-third.blend`, and `artifacts/590-third/590-third.glb`.
The script must rebuild the model reliably enough for future revision. Do not
modify or rename an unrelated existing GLB to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`590-third-top.png`, `590-third-north.png`, `590-third-east.png`,
`590-third-south.png`, `590-third-west.png`, plus `590-third-contact-sheet.png`,
at least one high three-quarter aerial beauty render `590-third-aerial.png`, and
a night render `590-third-night.png`.

The four elevations must share scale, framing, lighting, exposure and
projection; use orthographic or long-lens cameras; label directions from the
researched orientation; the aerial view uses the style bible's camera assumptions
(30-50 degrees down, long lens) and must show the **east corner** where the two
street faces and the raised parapet meet — that corner is the hero view for this
asset. Simple tabletop lighting, neutral warm background, minimal depth of field,
and every image must depict the same exported model.

## Validate the exported GLB

Re-import `590-third.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture
count, camera count, light count, animation count, applied-transform status,
negative-scale status, normal-orientation status, unexpected geometry, and
per-material contract compliance. Normals are checked two ways: per-object signed
volume (authoritative for a union of closed solids) and a deterministic
visibility-ray test (≤ 0.15% residual, zero for single shells). **The light well
makes the shell non-convex and non-simply-connected — expect the ray test to
carry a small residual and use the signed-volume test as authoritative.** Render
at least one review image from the re-imported asset. Write
`artifacts/590-third/validation.json` and `artifacts/590-third/REPORT.md`.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "590-third",
  "file": "590-third.glb",
  "anchor": [
    -122.3946749,
    37.7800837
  ],
  "targetHeightM": 9.5,
  "cat": 4,
  "name": "590 Third Street",
  "estimated": true,
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
for that, together with the integration notes in `docs/asset-plans/590-third.md`.
````

---

## Part 2 — Research and design dossier

Compiled 13 August 2026 from the sources in 2.2. Values marked *inferred* or
*estimated* are visual or derived, not published figures — the executing agent
must re-verify anything it relies on.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Address | 590 3rd Street, San Francisco, CA 94107; the same building also carries 400, 408 and 410 Brannan Street | DataSF parcels; DBI permits filed under both street names on one block/lot |
| Parcel | Block 3776, lot 114 (single lot, not subdivided) | DataSF parcels `acdm-wktn` (measured) |
| Lot area | 5,318 sf = 494.0 m2 | Assessor roll `wv5m-vpq2` (measured); the parcel polygon integrates to 491.5 m2 |
| Zoning | CMUO — Central SoMa Mixed Use Office | DataSF parcels |
| Built | **1905** on the assessor's roll — treat as *approximate*, see 2.15 | Assessor roll `wv5m-vpq2`, every year 2023–2025 |
| Construction | Assessor construction type `D` (wood frame); DBI permits 2011–2015 all record "wood frame (5)" | Assessor roll + DBI permits |
| Storeys | 2, on every permit 2003–2018 and on the assessor's roll | DBI permits `i98e-djp9`, assessor roll |
| Use | Ground-floor storefronts (real-estate office, yoga studio, café, formerly retail and a garage) with space above; assessor still classes the parcel `Industrial` | DBI permits; assessor roll; observed signage |
| Footprint | 21.28 m (3rd Street) x 23.10 m (Brannan Street) parallelogram, 491.5 m2 | DataSF parcel 3776114, reprojected (measured) |
| Building = lot | DataSF LiDAR footprint `SF3776114` integrates to 489 m2 against the parcel's 491.5 m2 — the building fills its lot corner to corner, so two of four faces are party walls | DataSF `ynuv-fyni` (measured) |
| Anchor | -122.3946749, 37.7800837 | parcel-polygon centroid; the polygon is a true parallelogram, so this equals the vertex mean exactly (measured). DataSF publishes -122.39467485, 37.78008375 for the same parcel |
| Street-grid heading | 3rd Street runs 134.5 / 314.5 deg; Brannan Street runs 45.6 / 225.6 deg | OSM street geometry, nearest-segment fit (measured) |
| Roof membrane | **7.77 m** median above local ground, mean 7.69 m, majority 7.82 m, sigma **0.64 m** | SF 2010 LiDAR `ynuv-fyni` record `SF3776114`, 1,946 half-metre cells (measured). The tiny sigma is what says the roof is genuinely flat |
| OSM height tag | 8 m | OSM way/124903637, `#sfbuildingheights` import (independent corroboration of the parapet band) |
| Main parapet | ~8.4 m | *estimated*: LiDAR roof + a 0.6 m parapet scaled off Street View |
| Raised corner parapet (crest) | **~9.5 m** | *estimated*: ~1.1 m above the main parapet, scaled off Street View against the known 23.10 m Brannan face (see 2.15) |
| LiDAR maximum | 11.65 m | same record — believed to be the 11.05 m brick neighbour's parapet in edge cells, *not* this building (see 2.15) |
| Ground | 7.25 m NAVD88 mean over the footprint, range 6.94–7.46 m | same LiDAR record (measured) — flat made ground |
| Light well | a genuine hole through the roof, 3.54 x 2.18 m, centred 4.81 m west and 1.94 m south of the anchor | interior ring of the DataSF LiDAR footprint (measured); visible as a pale rectangle in 2026 aerial imagery |
| Lot condition | Corner lot: 3rd Street front (NE), Brannan Street front (SE), party walls NW and SW | OSM street geometry + parcel adjacency (measured) |
| Nearest neighbour | the brick warehouse on the NW party wall, LiDAR height 11.05 m, 1,906 m2 — **taller than this building** | DataSF `ynuv-fyni` (measured) |
| Neighbour already in the scene | 599 Third (`599-third`, 18.3 m) directly across 3rd Street, ~57 m NE; 550 Third (`550-third`, 11 m) and 380 Brannan (`380-brannan`, 12.6 m) a block away | repo manifest + measured bearings |

### 2.2 Sources

- https://www.openstreetmap.org/way/124903637 — building footprint (a Bing trace: 478 m2 with a spurious 0.6 m jog on the NW edge, which is why this dossier uses the parcel polygon instead) and the independent `height=8` tag from the `#sfbuildingheights` import
- https://www.openstreetmap.org/node/12983432802 — the `Cafe Buenos Aires` shop node carrying `addr:housenumber=590`, `addr:street=3rd Street`; the point-in-polygon test that ties the address to way/124903637
- https://data.sfgov.org/resource/acdm-wktn.json — DataSF parcels, `blklot=3776114`: address 590 03RD ST, CMUO zoning, a single active lot, the parallelogram polygon this plan measures, and the published centroid used as the anchor
- https://data.sfgov.org/resource/wv5m-vpq2.json — Assessor secured roll, block 3776 lot 114: year built 1905, 2 storeys, construction type D, lot area 5,318 sf, use class Industrial
- https://data.sfgov.org/resource/i98e-djp9.json — DBI building permits, block 3776 lot 114 (6 records, 2003–2018): 2 storeys and wood frame throughout; PA 201403100290 + 201407080660 (2014) convert ground-floor retail at **410 Brannan** to a ballet studio; PA 201502027189 (2015) remodels a ground-floor toilet room at **590 3rd** under a food/beverage occupancy; PA 201103071525 (2011) repairs "exterior stucco to (e) retail store @ corner" — the one permit that describes the material of the walls
- https://data.sfgov.org/resource/ynuv-fyni.json — SF 2010 LiDAR building footprints, record `SF3776114` (`sf16_bldgid` 201006.0007274): 1,946 half-metre cells, ground mean 7.25 m, height median 7.77 m, mean 7.69 m, sigma 0.64 m, max 11.65 m, and the interior ring that proves the light well
- Google Street View, imagery capture **May 2025** (3rd Street and the 3rd/Brannan intersection) and **April 2025** (Brannan Street) — the primary elevation reference and the basis of every paragraph in 2.4
- Google Maps / Vexcel aerial imagery, 2026 — the roof reading in 2.4 "Top"

Deliberately **not** used as evidence: commercial listing aggregators (LoopNet, PropertyShark). Their floor areas at this address describe individual leased suites, not the building.

### 2.3 Orientation and placement

The west corner of 3rd and Brannan, in SoMa two blocks from South Park and three
from Oracle Park. The grid here is rotated ~45 deg from true north. 599 Third
holds the north corner of the same intersection, directly across 3rd Street.

Measured parcel polygon, reprojected with the app's tangent projection and
recentred on the anchor (x east, y north, metres). It is a true parallelogram —
four vertices, no kink:

```
W ( -15.709,  -0.602)
N (   0.684,  15.669)
E (  15.714,   0.602)   <- the street corner of 3rd and Brannan
S (  -0.689, -15.669)
```

| Edge | Length | Outward normal (true) | What it is |
|---|---|---|---|
| W → N | 23.10 m | 315.1 deg (NW) | party wall toward the brick warehouse at 574–578 3rd |
| N → E | 21.28 m | 45.2 deg (NE) | **3rd Street front** — the 590 address face |
| E → S | 23.10 m | 135.1 deg (SE) | **Brannan Street front** — the 400–410 face, the long one |
| S → W | 21.28 m | 225.2 deg (SW) | party wall toward 414 Brannan |

Vertex **E** is the corner of 3rd and Brannan and the building's hero point; the
raised parapet sits over it. Author `+Y` = north and place the polygon exactly as
measured. The contract's "front faces −Y" cannot be met — neither street face
points south — so real-world orientation wins per the README orientation note and
AGENTS rule 5.

Note that the *shorter* face (21.28 m) is the address face on 3rd Street and the
*longer* one (23.10 m) is on Brannan. It is a near-square block, and getting the
two backwards would put the sparse window face on the wrong street.

### 2.4 What each side shows

**North-east (3rd Street) — the address face, 21.3 m.** Two storeys. The ground
floor is a continuous **glossy near-black fascia band** carrying three white
`kinoko` / `REAL ESTATE` panels, with black awnings and full-height plate glass
below, dark frames, and a recessed dark entry door between bays. At the
north-west end of the face the band changes to a **blue panel reading
`CAFE BUENOS AIRES` / `COFFEE  EMPANADAS  PASTRIES`** — this is the 590 address
and the only saturated colour on the building. The upper storey is smooth
**pale warm-grey painted stucco**, sparsely windowed: large square-ish windows
with dark frames and interior blinds, two or three across the face, not a dense
rhythm. A **flat white blade sign** (blank, vertical, roughly 0.9 x 2.2 m) is
fixed to the wall near the north-west end and stops below the parapet. The
parapet is a plain flat line with a thin dark cap and no cornice. *(Observed
directly, Street View May 2025.)*

**South-east (Brannan Street) — the long face, 23.1 m.** Same two storeys, same
grey stucco, same black shopfront band. This face is the regular one: **seven or
eight tall punched windows** in a steady rhythm, several with **through-wall air
conditioners** in the wall directly below them — a detail that is genuinely
characteristic and worth keeping at miniature scale as small dark boxes. The
ground floor carries a `DIVINE YOGA STUDIO` awning with the numbers 410 / 408 /
400, and at the south-west end a **black roll-up garage door**. The `kinoko`
band wraps around from 3rd and continues to the corner. *(Observed directly,
Street View April 2025.)*

**The east corner.** The wall **steps up over the corner bay** — roughly 1.1 m
above the main parapet, spanning about a third of each street face, with a clean
vertical jog down on both sides. Blank grey stucco above the shopfront band, no
window in the raised portion. It is the one piece of composition the building
has, and it is aimed at the intersection. *(Observed directly; the step is
visible as a real vertical discontinuity, not a perspective artefact, in the
May 2025 corner pano.)*

**North-west party wall (23.1 m).** Abuts the brick warehouse at 574–578 3rd,
which is **taller** (11.05 m LiDAR) — so this wall is not merely blind, it is
largely hidden. Plain stucco. *Inferred.*

**South-west party wall (21.3 m).** Abuts 414 Brannan. Plain stucco, no
openings, possibly a service door. *Inferred.*

**Top — a working brown roof.** Flat, behind the parapet, and notably **warm
brown** in 2026 aerial imagery — a built-up cap-sheet roof, not the grey
membrane of its neighbours. On it:

1. five or six **small skylights**, mostly pale/white squares, loosely scattered
   rather than gridded;
2. two or three **mechanical / vent boxes**;
3. the **light well** — a real 3.5 x 2.2 m hole through the roof toward the
   south-west rear, reading as a dark rectangle from above;
4. one larger pale raised box near the centre-west, *inferred* to be a roof hatch
   or stair head;
5. the parapet cap running the whole perimeter, stepping up once over the east
   corner.

*(Item counts and positions are* inferred *from 2026 Vexcel aerial imagery;
treat the pattern as real and the exact placement as free. The light well and the
brown colour are the two things worth being faithful to.)*

### 2.5 Recognition cues (ranked)

1. **The two-tone reading** — a dark ribbon wrapping the whole ground floor under
   a plain pale block. From the app's camera this is the building. Nothing else
   on this corner is built that way.
2. **The raised corner parapet**, stepping up over the 3rd/Brannan corner. The
   only silhouette event, and the thing that makes the corner read as a corner
   rather than as two walls that happen to meet.
3. **The Brannan window rhythm with its air conditioners** — seven or eight tall
   openings with small dark boxes under them, the honest badge of a converted
   early-century commercial block.
4. **The brown roof with its light well** — warm brown against its neighbours'
   grey, punched by one dark rectangle.
5. **The blue `CAFE BUENOS AIRES` panel** at the north-west end of the 3rd Street
   face — the single saturated accent, and literally the address.

### 2.6 Miniature translation

**Preserve**

- The parallelogram footprint and its 45.2 deg heading, filling the lot
- Two storeys to a ~8.4 m parapet, corner block crest at 9.5 m
- The continuous black shopfront band, unbroken around the east corner
- The step in the parapet, and its asymmetric placement over the corner
- Two designed street faces; two blind party walls
- Grey walls + black base: the pairing is the identity, and it must not drift
  toward 599 Third's buff-and-white across the street

**Simplify / exaggerate**

- The shopfront band becomes one `Toy_ink` fascia solid plus a recessed
  `Toy_glass` shopfront ribbon, with `Toy_ink` awnings proud of it. Thicken the
  band past its real proportion (§9) so it survives at city distance — it is the
  cue that has to read from 300 m
- The parapet step is **exaggerated to ~1.2 m** and given a crisp `Toy_ink` cap
  so it holds a shadow line at aerial distance
- Brannan windows become seven `Toy_glass` punched openings in a steady rhythm
  with `Toy_trim` reveals — rhythm, not sash count (§5) — each with one small
  `Toy_roofd` AC box below
- 3rd Street windows become three larger `Toy_glass` squares, deliberately
  sparser than Brannan's; the contrast between the two faces is real and worth
  keeping
- The café sign becomes one flat `Toy_sky` panel with a `Toy_trim` edge — the
  only saturated element on the model
- The blade sign becomes one thin `Toy_trim` slab proud of the wall
- The garage door becomes one recessed `Toy_roofd` panel with a horizontal
  groove or two
- Roof: five `Toy_glassl` skylight caps, three `Toy_roofd` boxes, one `Toy_trim`
  stair-head box, and the light well modelled as a genuine opening with
  `Toy_ink` reveals — not painted on
- Party walls get flat `Toy_stone` and nothing else

**Do not add** a cornice, a corbel course, storefront pilasters, a corner turret
or a chamfered corner. This is a plain box with a black base and one step in the
parapet, and every one of those additions has been observed *not* to be there.

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not
a straitjacket — adjust after the first aerial review render.

1. **Body:** extrude the measured parallelogram from z=0 to z=7.80,
   `Toy_stone` (pale warm-grey stucco), with the light well cut through as a
   3.54 x 2.18 m hole centred at (−4.81 E, −1.94 N), `Toy_ink` reveals.
2. **Main parapet:** 0.30 m thick, `Toy_stone`, from z=7.80 to **z=8.40**,
   capped with a 0.10 m `Toy_ink` band, running the full perimeter.
3. **Raised corner parapet:** the same section carried up to **z=9.50**, from
   the corner vertex **E** back 7.0 m along the 3rd Street face and 8.0 m along
   the Brannan face, with a clean vertical jog at each end and the same
   `Toy_ink` cap. This is the bbox top.
4. **Roof field:** `Toy_rust` slab inset 0.30 m from the parapet inner face, top
   at z=7.90, pierced by the light well.
5. **Storey datum:** shopfront head at z=4.10, upper-storey floor at z=4.30,
   parapet at 7.80 — a tall commercial ground floor under one office storey.
6. **Shopfront band (both street faces, continuous around vertex E):**
   - `Toy_ink` fascia 1.00 m deep, from z=3.10 to z=4.10, proud 0.12 m.
   - `Toy_glass` shopfront ribbon below it, z=0.20 to z=3.10, recessed 0.25 m,
     divided by 0.15 m `Toy_ink` mullions into 3 bays on 3rd and 4 on Brannan.
   - `Toy_ink` awnings 0.8 m deep at z=3.05 over the middle bays only.
   - Two recessed `Toy_ink` entry doors, one per face.
7. **3rd Street face (NE, 21.3 m):** three `Toy_glass` windows 2.0 x 1.6 m at
   z=5.30, evenly spread, in 0.14 m `Toy_trim` reveals. `Toy_sky` café panel
   1.9 x 0.7 m set into the fascia at the north-west end, `Toy_trim` edge. Blank
   `Toy_trim` blade sign 0.9 x 2.2 m, proud 0.15 m, at z=4.9, near the north-west
   end.
8. **Brannan face (SE, 23.1 m):** seven `Toy_glass` windows 1.1 x 1.9 m at
   z=5.00 on a 2.9 m pitch, in 0.14 m `Toy_trim` reveals; a 0.6 x 0.4 x 0.25 m
   `Toy_roofd` AC box under four of them at z=4.55. `Toy_roofd` roll-up door
   3.2 x 3.0 m recessed 0.20 m at the south-west end of the shopfront band.
9. **Party walls (NW and SW):** flat `Toy_stone`, no openings.
10. **Roof objects:** five `Toy_glassl` skylight caps 1.2 x 0.9 m, 0.22 m proud,
    loosely scattered; three `Toy_roofd` boxes 0.8 x 0.6 x 0.5 m on a 0.10 m
    curb; one `Toy_trim` stair-head box 2.4 x 1.8 x 1.1 m near the centre-west.
11. Bevel 0.08 m, 2 segments, on everything.

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_stone` | `#d9d2c2` | pale grey-stucco walls, parapets, party walls |
| `Toy_ink` | `#3a3530` | shopfront fascia, awnings, mullions, entry doors, parapet caps, light-well reveals |
| `Toy_glass` | `#2a4d73` | shopfront glazing, upper-storey windows |
| `Toy_glassl` | `#6f95b8` | roof skylight caps |
| `Toy_trim` | `#f3efe6` | window reveals, blade sign, café-panel edge, stair-head box |
| `Toy_rust` | `#a86444` | the brown built-up roof field |
| `Toy_roofd` | `#45454a` | mechanical boxes, AC units, roll-up garage door |
| `Toy_sky` | `#6db3d9` | the `CAFE BUENOS AIRES` panel (the one saturated accent) |
| `Toy_glass_Glow` | `#2a4d73` | the shopfront ribbon at night, plus two or three upper windows |
| `Toy_trim_Glow` | `#f3efe6` | the `kinoko` fascia panels reading as lit signage |
| `Toy_sky_Glow` | `#6db3d9` | the café panel at night |

**Night state.** This is a street-level building, so its night state lives in the
band, not in the block: the **shopfront ribbon glows continuously around the
corner** (the hero — a lit ribbon at ground level is exactly what a
storefront corner looks like after dark and it re-states the daytime cue), the
signage panels read as lit fascia, and only two or three upper windows are on.
The walls, the parapet, the AC boxes and the roof stay dark. Do not light the
whole upper storey — an evenly-lit second floor turns a shop corner into an
office block. Glow shells must be thin surfaces proud of the opaque glazing
behind them: the app renders `_Glow` in a separate layer at ~12% alpha by day, so
a primary surface must never be authored as glow. Drive `_Glow` emission from
Base Color at strength 1.0 in the render rig (see the README's note on
re-imported GLBs).

Note the deliberate contrast with **599 Third** across the street, whose night
state is a *scatter* of residential windows. 590 is a continuous ground-level
ribbon. Seen together, the two states say "shops below, homes above" about the
whole intersection — which is what SoMa actually is.

### 2.9 Top surface

At 9.5 m with a 21 x 23 m plan, this building is nearly all roof from the app's
camera, and it is also the shortest thing on its corner — the eye lands on it as
a *plane* next to 599 Third's wall. That plane has to be designed, and the two
things that make it interesting are free: it is **brown** where every roof around
it is grey, and it has a **hole in it**. Model both honestly and the roof needs
almost nothing else — five skylights, three boxes, a stair head. Resist adding
deck pads or planting; there is no evidence of either, and a busy roof here would
compete with 599's genuinely inhabited one across the street. The step in the
parapet is the roof's only edge event and should stay the only one.

### 2.10 Scope

**In the GLB:** the building, main and raised parapets, roof field, light well,
skylights, mechanical boxes, stair head, shopfront band with fascia, glazing,
awnings, entry doors, signage panels, blade sign, AC boxes and the roll-up
garage door

**Not in the GLB:** 3rd Street, Brannan Street, neighbouring buildings, the
rooftop billboard on the brick neighbour, street trees, street furniture,
traffic signals, people, vehicles, plinths, cameras or lights

### 2.11 Triangle budget

Cap 11,000 — below 599 Third's 15,000 because this building is half the height,
has one storey of windows instead of four, and carries no entry recess, numerals
or brace. Suggested split: shell, parapets (including the corner step) and roof
field ~2k; shopfront band on both faces ~3k; Brannan windows and AC boxes ~2k;
3rd Street windows and signage ~1.5k; light well ~0.3k; roof objects ~1.5k;
spare ~0.7k.

### 2.12 Draft manifest entry

```json
{
  "id": "590-third",
  "file": "590-third.glb",
  "anchor": [
    -122.3946749,
    37.7800837
  ],
  "targetHeightM": 9.5,
  "cat": 4,
  "name": "590 Third Street",
  "estimated": true,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

`dims` and `tris` are placeholders until the asset is built and validated.
`estimated: true` is deliberate: the roof membrane is LiDAR-measured but the
parapet and the corner step that set `targetHeightM` are scaled off photographs
(2.15). `loadRadius` is the skill's default `max(2500, targetHeightM * 30)` =
2500; at 9.5 m the building is illegible long before 2,500 m, so the carved hole
left beyond the radius costs nothing.

### 2.13 Integration notes (for later, not this task)

- **New landmark.** Add a `pipeline/lib/landmarks.mjs` entry (`id: '590Third'`,
  lon/lat as above, `height: 9.5`) and re-bake the affected tiles, or the baked
  DataSF block will sit inside the model.
- **Exclusion radius — measured, not estimated.** `excluded()` in
  `pipeline/buildings.mjs` drops a footprint when its `ringCentroid` **or any
  vertex** falls inside the radius. Measured against the bake's own source
  (DataSF `ynuv-fyni` footprints, reprojected with the app's tangent
  projection), around this anchor:

  | | distance from anchor |
  |---|---|
  | this building's ring centroid | **0.88 m** |
  | this building's nearest vertex | 11.24 m |
  | nearest **neighbour** vertex (`SF3776008`, the 1,906 m2 brick warehouse on the NW party wall) | **13.82 m** |
  | second neighbour vertex (`SF3776011`) | 15.08 m |

  The window that drops exactly this building is therefore
  `0.88 < r <= 13.82`, and the margin on the upper end is thin because the
  building shares a party wall. **Start at `exclude: 7`** — comfortably clear of
  the centroid, comfortably clear of the neighbour, and in line with the
  neighbours already integrated (`550Third` 8, `551Third` 8, `380Brannan` 9,
  `599Third` 10). Re-measure against the actual bake input before committing:
  the pipeline runs `simplifyRing` at a 0.6 m tolerance, which moves vertices.
  Note also that the brick warehouse is *taller* than this asset, so a radius
  that swallowed it would leave a very visible hole.
- Manifest id `590-third` maps to registry id `590Third`.
- No camera preset key. At 9.5 m this is a block texture, not a destination —
  but `camera` is still mandatory on the registry entry (main.js maps every
  manifest landmark into `presets` and camera.js reads `preset.yaw`
  unconditionally; omitting it boots to a crash). Suggested
  `camera: { distance: 180, yaw: 90, pitch: 30 }`: app yaw = 180 − true bearing,
  and 90 stands the camera due east, the bisector of the 3rd Street front
  (normal 45.2 deg) and the Brannan front (135.1 deg) — the one angle where both
  designed elevations and the raised corner read at once. 180 m suits a 9.5 m
  block (cf. `550Third` 190 at 11 m, `380Brannan` 220 at 12.6 m).
- The building sits on flat made ground (LiDAR ground mean 7.25 m NAVD88, range
  0.52 m). Terrain seating should be uneventful; check it anyway.
- **The light well is a hole in a landmark GLB.** The loader merges everything
  into the shared `BatchedMesh`; a genuine opening is fine geometrically, but
  confirm the normals test and the merge line behave (see the validation note in
  Part 1).
- **Batch note.** This landmark completes the 3rd/Brannan intersection opposite
  `599-third`. If it is built alongside other landmarks, follow batch mode in
  `docs/asset-pipeline/ADDRESS-TO-ASSET.md` — commit source only and let
  `BATCH-INTEGRATE.md` bake the city once.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] bbox top exactly 9.5 m (the raised corner parapet) so the loader's scale
      factor is 1.0
- [ ] Dimensions plausible in meters and consistent with 2.1 (21.3 x 23.1 m plan)
- [ ] Triangles at or under 11,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the shopfront ribbon, the signage panels and two or three
      upper windows
- [ ] The light well is a real opening, with reveals, not a painted rectangle
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (per-object signed
      volume authoritative; the light well means the ray test may carry a small
      residual)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + night render + contact sheet regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

- **The crest is estimated, not measured.** The LiDAR record gives the roof
  membrane at 7.77 m with sigma 0.64 m, and OSM independently tags `height=8` —
  those two agree and are safe. The 8.4 m parapet and the 9.5 m raised corner
  block are scaled off Street View against the known 23.10 m Brannan face, with
  an eye-level camera about 20 m out, so a ±0.5 m error is entirely possible.
  This is why the manifest entry carries `estimated: true`. If the crest moves,
  only `targetHeightM` and the top of the corner block move with it.
- **The 11.65 m LiDAR maximum is probably not this building.** It is 6 sigma
  above a roof whose sigma is 0.64 m, and the building shares a party wall with a
  brick warehouse whose own LiDAR median is 11.05 m — edge cells along that wall
  would produce exactly this number. Nothing on the roof in 2026 aerial imagery
  or in any street-level view rises anywhere near 11.6 m. **Do not model a
  penthouse to explain it.** If a later source shows a real rooftop structure,
  that changes `targetHeightM`; check before assuming.
- **"Built 1905" is an assessor's date on a block that burned in April 1906.**
  A post-fire rebuild recorded under the pre-fire year is the likelier reading,
  and the fabric — wood frame, two storeys, plain stucco over a commercial base —
  fits 1906–08 SoMa reconstruction. It changes nothing about the massing; it
  changes what the REFERENCE.md may claim.
- **The Brannan window count is inferred** from Street View at an oblique angle;
  seven is the working number, eight is possible. Getting it wrong changes the
  rhythm on the building's longest face, which is the face 599 Third's residents
  look at.
- **The raised corner parapet's extent is inferred.** The step itself is
  observed and unambiguous (a clean vertical jog on both faces); how far it runs
  back along each face is read off one oblique photograph. 7 m and 8 m are the
  working numbers.
- **The roof is read entirely from one aerial source.** The brown colour and the
  light well are corroborated (the light well by the LiDAR footprint's interior
  ring, which is independent evidence); the skylight and box positions are not.
  Do not chase pixel positions.
- **The OSM footprint disagrees with the parcel by 2.8%** (478 m2 vs 491.5 m2)
  and carries a 0.6 m jog on the NW edge that no other source shows. This plan
  uses the parcel polygon, which agrees with the assessor's 5,318 sf lot to 0.5%
  and with the LiDAR footprint to 0.5%. If the executing agent prefers OSM, it
  must say why — but the anchor and the heading barely move either way.
- **Do not let this asset drift toward 599 Third.** They are 57 m apart, will be
  in frame together permanently, and are the same era of SoMa in two different
  registers. If the grey/black pairing starts creeping toward buff-and-white
  during authoring, the two buildings will merge into one block at city distance
  and both will get worse.
