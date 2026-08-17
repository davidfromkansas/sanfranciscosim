# 132 South Park (130-134 South Park) — SF-SIM asset plan

A 1913 three-storey Edwardian flats building on the north-west arc of the South Park
oval, and the **only painted twin-bay wood front left on this stretch of the park**.
Everything either side of it is a flat-fronted brick or corrugated-metal box: 126 South
Park next door is 7.3 m, 136 is 3.2 m, and this one stands 12.07 m — a tall narrow tooth
in a low row, in pale lap siding outlined edge to edge in **butter-yellow trim**, over an
**oxblood ground-floor base with a black segmental-arched carriage gate**.

It is also the only lot in the set planned so far that carries **two separate buildings**:
the flats on the street, an 8.7 m open courtyard behind them, and a two-storey rear
cottage on the back lot line. That is invisible from the street and unmissable from the
app's aerial camera, and it is the reason this asset is worth building rather than
leaving to the procedural box.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/132-south-park/`. This document is the plan only: Part 1 is the runnable task
prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `132-south-park` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3946190, 37.7815407` (bounding-box centre of the built form, measured — falls in the courtyard between the two structures, see 2.3) |
| Target height | **12.07 m** to the front block's cornice crest; roof deck 11.77 m; rear cottage crest 8.75 m — LiDAR-derived, see 2.1 and 2.15 |
| Footprint | two rectangles on a 6.689 × 29.974 m lot: front flats 6.689 × 10.30 m, rear cottage 6.689 × 10.98 m, 8.70 m courtyard between; measured |
| Triangle cap | 9,000 |
| Category | `2` (apartments) — assessor class A5, Apartment 5 to 14 Units |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 132 South Park GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of 130-134 South Park in San Francisco and deliver
it as a downloadable, validated GLB.

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
7. `artifacts/181-south-park/` — the closest reference implementation for the *front*
   block: same block (3775), same oval, same era, same 45° heading, same
   tall-narrow-residential brief
8. `artifacts/551-third/` — the closest reference implementation for the *lot*: the only
   shipped asset that is two separate structures with open ground between them, and the
   precedent this plan's exclusion design follows
9. `docs/asset-plans/132-south-park.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Read 2.15 before you start

This dossier is **asymmetric**. The lot geometry and the two heights are survey- and
LiDAR-grade. The **front elevation is documented from exactly one photograph** (a 2021
drone shot in an agent's sold-listing gallery) and the **rear cottage from one nadir
frame in the same gallery**. Section 2.15 says precisely which statements come from
which. Do not promote the single-photo readings to established fact in `REFERENCE.md`,
and do not invent detail for the two flanks and the rear elevation, which no source in
this dossier shows at all.

## Must capture

- **Two separate volumes on one lot** with a genuinely open courtyard between them:
  front flats (10.30 m deep), **8.70 m of open ground**, rear cottage (10.98 m deep).
  The courtyard is a void — no floor plate, no infill, no connecting bridge. Anyone
  looking down on this lot must see straight through to the terrain.
- The **twin full-height projecting square bays** on the front, running the three
  residential floors, with a narrow blank recessed stair strip between them
- **Butter-yellow trim outlining everything**: bay corner boards, every window
  surround, the belt course at each floor line, the cornice band, and the outer frame
  of the whole facade. This is the building's identity — carry it hard.
- The **oxblood ground-floor base**, visually a plinth rather than a storey, with the
  **black segmental-arched carriage gate** on the south-west half — the passage through
  to the courtyard — and a single square sash window on the north-east half
- The **gray shingled hipped false-mansard hood** tucked under the cornice, spanning
  between the two bay tops over the recessed centre
- A designed roof: light membrane deck, parapet/cornice ring, one skylight, two slim
  vent stacks
- The rear cottage as a plain two-storey light box with a flat roof and a small wood
  deck and stair on its courtyard face

## Research 132 South Park independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, both footprints, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- **Street-level photography of the South Park elevation.** The dossier rests on one
  aerial photograph. Google Street View has South Park coverage; the 2021 sale
  (Allison Chapleau, $2,000,000) and any rental listings for units 130/132/134/134A
  will carry exterior and courtyard shots; SF Assessor and Planning records may carry
  a facade photo.
- The **exact paint scheme**: this plan reads the field as a very pale warm gray-white
  lap siding, the trim as a butter/ochre yellow, and the base as a dark oxblood. Confirm
  all three, and confirm the base is painted wood or stucco rather than brick — brick
  reveal appears at the gate jambs in the one photo.
- The **bay window rhythm**: how many lights per bay face per floor, and whether the
  bay side returns are glazed
- Whether the **recessed centre strip** carries any opening above the ground floor
  (the one photo shows it blank)
- The **rear cottage**: storey count, cladding, window pattern, and whether its
  courtyard face really carries the wood deck and external stair visible in the nadir
- The **two flanks and the rear elevation** — no source in this dossier shows them
- **Whether the lot or the block is a designated historic resource.** Not established
  here either way; do not assert it.
- Day and night appearance

Prefer architect/engineer publications, owner or institutional material,
planning and permitting documents, architectural press, geolocated photography,
and aerial/satellite imagery. Never rely on a single photograph, a single
AI-generated image, or a single unsourced 3D model. Separate verified facts from
visual inference; if sources disagree, document the disagreement and decide.

**Three source conflicts are already known and resolved in 2.1 — re-check them, do not
silently re-inherit the wrong value:** OSM carries **no building at all** on this lot
(Nominatim's "132 South Park" match is the *street* way 8916553, not a building), so the
footprint comes from the DataSF parcel and the 2010 LiDAR footprints rather than OSM; the
assessor records **5 units** where the 2021 listing advertises **7**; and the LiDAR gives
the two structures ground elevations 0.48 m apart from two different source tiles, which
2.15 argues is measurement noise rather than a real fall.

## Create a reference dossier

Write `artifacts/132-south-park/REFERENCE.md` containing: source links and what each
establishes; verified dimensions and location; orientation; observations from all
four sides and above; the 3-5 strongest recognition cues; features to preserve;
features to simplify; uncertainties and conflicting evidence. Be explicit about which
facade statements you confirmed and which you inherited unconfirmed from this plan.
A contact sheet of attributed reference thumbnails is welcome if legally permissible —
do not commit copyrighted full-resolution imagery.

## Make your own design decisions

Follow the conversion process in `docs/styles/miniature-toy.md` §22: identify the
recognition cues, strip nonessential information, rebuild the massing from a few
confident volumes, exaggerate only the signature features, simplify the facade
into broad rhythms, deliberately design every surface visible from above,
evaluate from the app's high three-quarter aerial camera, then simplify again.

This is a **secondary building** in the style bible's detail budget (§21). It gets one
hero elevation and one hero plan reading, and nothing else. The hero elevation is the
South Park front — the bays and the yellow trim. The hero plan reading is the
front/courtyard/rear rhythm. Everything on the flanks and the rear is broad rhythm only.
Resist adding hero-tier ornament; the yellow trim already spends this building's entire
accent budget, and §7 will not carry a second saturated colour beyond the oxblood base.

The finished asset must be immediately recognizable as this building's real massing,
consistent from all four sides and above, architecturally credible, and a
premium handcrafted miniature — not photorealistic, not voxel art, not generic
low-poly, and never accurate in one view while invented in the others.

## Scope of the exported asset

Export the two 1913 structures on lot 3775/062: the front flats block with its bays,
base, gate, cornice, shingled hood, roof deck and roof furniture; and the rear cottage
with its courtyard deck and stair. Nothing between them.

Do not include unrelated surrounding city geometry: South Park (the street or the park),
the neighbouring buildings at 126 and 136 South Park, street trees, the sidewalk,
parked cars, the dumpsters standing in the real courtyard, people, plinths, cameras or
lights. Temporary context may appear in review renders but must not leak into the GLB.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary
`.glb`; real-world meters; origin at base center; minimum geometry Z ~ 0;
applied transforms; no negative scales; outward normals; no duplicate or foreign
geometry; no image textures; no transparency; flat-color materials named `Toy_*`
from the project palette; `_Glow` suffix only on surfaces that glow at night; no
`Toy_body`; no cameras, lights, animations, armatures or constraints; no external
dependencies; at most 9,000 triangles.

**Two-volume caveat on the origin rule.** The asset's XY centre lands in the *courtyard*,
between the two buildings, and there is no geometry there. That is correct and
deliberate — the anchor in the manifest is the same point. `min Z ≈ 0` is satisfied by
the front block's base; the rear cottage's base is deliberately extended below z=0 (see
the massing recipe) and must not be allowed to raise `min Z`.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model
drops into the city at its real-world heading — the loader applies no rotation
(`placeGeneric` in `app/src/assets.js` only scales and positions). The South Park
entrance front faces **south-east, outward bearing 135.1°**; the building is rotated
roughly 45° off the world axes, so build directly on the measured footprint polygons in
2.3 rather than modelling an axis-aligned box and rotating it. Record the measured
heading in `REPORT.md`.

**Height normalization:** the tallest geometry in the export (the front block's cornice
crest) must land at exactly **12.07 m** so the loader's `targetHeightM / measuredHeight`
scale is 1.0.

## Reproducible Blender workflow

Blender 5.2 LTS. Headless: `blender -b --python script.py -- args`.

Keep `artifacts/132-south-park/build_132_south_park.py` (deterministic build script),
`artifacts/132-south-park/132-south-park.blend`, and
`artifacts/132-south-park/132-south-park.glb`. The script must rebuild the model reliably
enough for future revision. Do not modify or rename an unrelated existing GLB to satisfy
the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`132-south-park-top.png`, `132-south-park-north.png`, `132-south-park-east.png`,
`132-south-park-south.png`, `132-south-park-west.png`, plus
`132-south-park-contact-sheet.png`, at least one high three-quarter aerial beauty render
`132-south-park-aerial.png`, and a night render `132-south-park-aerial-night.png`.

The four elevations must share scale, framing, lighting, exposure and
projection; use orthographic or long-lens cameras; label directions from the
researched orientation; **the top view has to prove the two-volume reading** — front
block, open courtyard, rear cottage, all three legible without a caption; the aerial
view uses the style bible's camera assumptions (30-50 degrees down, long lens). Simple
tabletop lighting, neutral warm background, minimal depth of field, and every image must
depict the same exported model.

## Validate the exported GLB

Re-import `132-south-park.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture
count, camera count, light count, animation count, applied-transform status,
negative-scale status, normal-orientation status, unexpected geometry, and
per-material contract compliance. Render at least one review image from the
re-imported asset. Write `artifacts/132-south-park/validation.json` and
`artifacts/132-south-park/REPORT.md`.

Note that the axis-aligned XY bounding box will be roughly **26.3 × 26.3 m** even though
the lot is 6.7 m wide and 30.0 m deep — that is the expected consequence of a ~45°
real-world heading, not a scale error. Note also that the model is two disjoint shells:
the normals test must use the **per-object signed volume** as authoritative, not a single
union ray test.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "132-south-park",
  "file": "132-south-park.glb",
  "anchor": [
    -122.3946190,
    37.7815407
  ],
  "targetHeightM": 12.07,
  "cat": 2,
  "name": "130-134 South Park",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a separate, explicitly requested job — run `docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in `docs/asset-plans/132-south-park.md`.
````

---

## Part 2 — Research and design dossier

Confidence labels follow `docs/asset-plans/README.md`: **measured** = read off survey or
API geometry; **verified** = stated by an authoritative record; **observed** = read off a
photograph, with the photograph named; **inferred** = reasoned from type and period;
**estimated** = a number chosen to fill a gap.

### 2.1 Verified facts

| Fact | Value | Confidence / source |
|---|---|---|
| Addresses on the parcel | 130, 132, 134, 134A South Park | verified — DataSF EAS address dataset `ramy-di5m`, four rows, all block 3775 lot 062 |
| APN | block **3775**, lot **062** (`3775062`) | verified — DataSF parcels `acdm-wktn`, active, `from_address_num` 130, `to_address_num` 134 |
| Lot geometry | rectangle **6.689 m × 29.974 m**, 200.5 m² | measured — parcel polygon, four corners, orthogonal to 0.14° |
| Lot area, assessor | 2,145 sq ft = 199.3 m² | verified — assessor roll `wv5m-vpq2`, agrees with the parcel to 0.6% |
| Year built | **1913** | verified — assessor roll, every year 2007-2025; the 2021 sale listing says the same |
| Storeys | 3 | verified — assessor roll (the three residential floors; the oxblood base is a plinth, not a counted storey — see 2.4) |
| Units | 5 (assessor) / 7 (2021 listing) | conflicting — see 2.15 risk 3; irrelevant to the model |
| Building area | 3,630 sq ft = 337 m² | verified — assessor roll; consistent with 3 floors on the front block plus 2 on the rear (2.7) |
| Assessor class | A5, *Apartment 5 to 14 Units*; use *Multi-Family Residential* | verified — assessor roll 2014-2025 (class A, *Apartment 4 units or less*, 2007-2013) |
| Two structures on the lot | yes | verified — 2021 sale listing, "Two Separate Structures on One Lot"; independently measured as two disjoint DataSF footprints under one MBLR |
| Front block height | **12.07 m** crest, **11.77 m** median roof deck, σ 0.36 m over 234 LiDAR cells | measured — DataSF footprints `ynuv-fyni`, `sf16_bldgid` 201006.0158439 |
| Rear cottage height | **8.75 m** crest, **8.40 m** median deck, σ 0.27 m over 241 cells | measured — same dataset, `sf16_bldgid` 201006.0158273 |
| OSM building | **none** | measured — Overpass over the whole South Park oval returns 91 buildings and none on lot 062; Nominatim's "132 South Park" hit is way 8916553, the *street* |
| Recent permits | 5 since 2019: one $10k OTC alteration (2019, still open), two electrical (2025), two plumbing (2025, 2026) | verified — DataSF via openpermitdata.com |
| Architect | not found | — searched; see 2.15 risk 5 |
| Historic status | not established | — see 2.15 risk 5 |

**Why the height is not in doubt.** Unlike 135 South Park, this building has no OSM
`height` tag to conflict with, and the LiDAR return is unusually clean: standard
deviation 0.36 m across 234 half-metre cells on the front block, 0.27 m across 241 on the
rear. Both are flat roofs behind parapets, exactly the case the 2010 LiDAR reads well.
The 12.07 m maximum is corroborated independently by the one photograph: measured off
the drone frame, the oxblood base is 2.24 m and each of the three residential floors is
3.28 m, which totals 12.08 m to the top of the cornice band. Two unrelated methods
agreeing to 1 cm is the strongest height evidence in this whole set.

### 2.2 Sources

| Source | What it establishes |
|---|---|
| DataSF parcels `acdm-wktn`, blklot `3775062` | the surveyed lot rectangle and its two neighbours 3775061 / 3775063 — the entire basis of 2.3 |
| DataSF building footprints `ynuv-fyni`, MBLR `SF3775062` (two rows) | both footprints, both heights, both ground elevations; this is also the dataset the bake consumes, which is why 2.13 measures against it |
| DataSF EAS addresses `ramy-di5m` | that 130 / 132 / 134 / 134A are one parcel, and where 126 / 136 / 140 sit either side |
| DataSF assessor roll `wv5m-vpq2`, block 3775 lot 062, 19 annual rows | 1913, 3 storeys, 3,630 sq ft, class A5 |
| [Allison Chapleau, "130-134 South Park Street"](https://www.allisonchapleau.com/listing/130-south-park-street) — sold listing | "Two Separate Structures on One Lot", 1913, 7 units, $2,000,000, and the photo gallery below |
| Same gallery, `130 S Park St Drone CLEAN MLS` (2021) | **the only front elevation this dossier has.** Three-quarter aerial from over the park, the whole facade unobstructed, plus the roof deck, the two vent stacks, the skylight, and both neighbours' roofs for height comparison |
| Same gallery, `DJI_0611` (2021) | nadir over the lot: the shingled hood at the street edge, the flat roof, the courtyard, the wooden deck and stair, the rear cottage |
| Same gallery, `DJI_0602` (2021) | wide aerial context — the building in its row, downtown behind |
| [openpermitdata.com, 130 South Park](https://openpermitdata.com/sf/address/130-south-park) | the permit history, which is what says the building is materially unchanged since the LiDAR |
| Overpass API over the South Park oval | that OSM has no building here, and the heights/addresses of the 91 that it does have |

Everything in the gallery is **observed (listing photo)**: it shows the building as
marketed in 2021, which the permit record says is still current, but it is one
photographer's set from one afternoon and it never shows the flanks or the rear.

Photographs are **not** committed to the repo. The URLs above are the record.

### 2.3 Orientation and placement

The lot is a standard SoMa 22 ft × 98 ft slot on the **north-west arc** of the South Park
oval, its short end on the street, looking **south-east** across South Park itself. The
whole block is rotated ~45° off the world axes like the rest of the SoMa grid. The rear
lot line abuts the backs of the Bryant Street lots.

Local lot frame used throughout this dossier: `s` runs along the frontage from the
**north-east** party line (`s=0`, shared with 126 South Park) to the **south-west** party
line (`s=6.689`, shared with 136 South Park); `t` runs into the lot from the **front**
line (`t=0`) to the **rear** line (`t=29.974`).

Parcel corners, projected with the repo's own `project()` (`pipeline/lib/geo.mjs`,
`LON0 −122.4375`, `LAT0 37.77`, `M_PER_DEG_LON = 111320·cos(37.77°) = 87995.7684`):

| Corner | `(s, t)` | World `(x, z)` |
|---|---|---|
| NE front | `(0, 0)` | `(3786.111, −1267.645)` |
| SW front | `(6.689, 0)` | `(3781.363, −1262.933)` |
| SW rear | `(6.689, 29.974)` | `(3760.204, −1284.149)` |
| NE rear | `(0, 29.974)` | `(3764.945, −1288.868)` |

Edge bearings, all measured, all consistent with the 45° grid:

| Edge | Outward bearing | What it is |
|---|---|---|
| front (`t=0`) | **135.1° SE** | **the South Park front** — the hero elevation |
| north-east flank (`s=0`) | 45.2° NE | party line with 126 South Park |
| south-west flank (`s=6.689`) | 225.2° SW | party line with 136 South Park |
| rear (`t=29.974`) | 315.1° NW | back line, onto the Bryant Street lots |

**The two footprints.** The 2010 LiDAR polygons, projected into `(s, t)`, land at
`s [0.88, 6.91] × t [1.42, 11.71]` and `s [0.19, 6.89] × t [20.09, 31.12]`. Both are
about 0.2 m south-west and 1.1 m rear of the parcel — a uniform registration offset
between the two datasets, not a real setback, and `t = 31.12` on the rear block is 1.15 m
*past* the surveyed rear lot line, which settles it. Correcting for that offset and
snapping to the lot lines, which is what a 22 ft SF lot with party walls on both sides
actually does:

```
   t = -0.55  ---- bay faces (project over the sidewalk)
   t =  0.00  ==== FRONT BLOCK front wall, on the property line
                   |                            |
                   |   front flats, 10.30 m     |   3 floors + oxblood base
                   |                            |   crest 12.07 m
   t = 10.30  ==== rear wall of the front block
                   .                            .
                   .   COURTYARD, 8.70 m        .   open ground, no geometry
                   .                            .
   t = 19.00  ==== front wall of the rear cottage
                   |                            |
                   |   rear cottage, 10.98 m    |   2 floors, crest 8.75 m
                   |                            |
   t = 29.974 ==== rear property line
                 s=0                          s=6.689
                 NE party wall               SW party wall
```

Both blocks run the full 6.689 m lot width, party wall to party wall.

Footprint polygons in **Blender coordinates** (metres, `+X` east, `+Y` north), already
centred on the anchor `-122.3946190, 37.7815407`:

```
front block                     rear cottage
( 12.763,  -8.061)  NE front    ( -0.654,   5.392)  NE front
(  8.015, -12.773)  SW front    ( -5.402,   0.681)  SW front
(  0.742,  -5.480)  SW rear     (-13.151,   8.450)  SW rear
(  5.489,  -0.768)  NE rear     ( -8.403,  13.162)  NE rear
```

The bay faces sit 0.55 m proud of the front wall, on the line
`(13.151, −8.450) → (8.403, −13.162)`.

**The anchor is in the courtyard.** `-122.3946190, 37.7815407` is the bounding-box centre
of the built form (`s = 3.345`, `t = 14.715`) and there is no geometry within 4.4 m of it
in either direction. That is correct: the loader centres the GLB's bounding box on the
anchor, and the alternative — anchoring on one of the two blocks — would put the other
one 19 m off its surveyed position. It does mean the exclusion design in 2.13 cannot use
a single radius, and it means the validator's "XY centre ≈ 0,0" check passes on a point
in mid-air.

For reference, the area centroid of the built form is `t = 15.29`, 0.58 m behind the
bbox centre. The DataSF assessor point for the parcel is `-122.3946212, 37.7815424`,
0.25 m from the anchor — an independent confirmation.

Because of the 45° heading the axis-aligned bounding box is ~26.3 × 26.3 m for a lot
that is 6.7 × 30.0 m. That is correct.

### 2.4 What each side shows

**South-east (the South Park front)** — the hero elevation, 6.689 m wide, 12.07 m tall,
looking across the street into the park. *Everything in this section is observed from the
one 2021 drone frame*, and it is the best-documented facade in the small-building set
even so, because that frame is square-on and unobstructed.

Bottom to top:

- **The oxblood base, 0 → 2.24 m.** Dark red-brown, painted, reading as a plinth rather
  than a storey. Two openings: a square four-light sash window on the north-east half,
  and on the south-west half a **wide segmental-arched opening filled with a black metal
  gate** — the carriage passage through to the courtyard, with brick reveal visible at
  the jambs. The address numerals sit between them.
- **Three residential floors, 2.24 → 11.77 m**, each 3.18 m, in **horizontal lap siding**
  a very pale warm gray-white.
- **Two projecting square bays**, ~2.80 m wide each, running all three floors from the
  top of the base to the cornice, 0.55 m proud. Each bay face carries a pair of tall
  windows; each bay return carries one narrow window.
- **The recessed centre strip**, ~1.09 m, between the bays: blank siding all the way up,
  with a vertical yellow trim board. It is the stair wall.
- **Yellow trim on every edge**: bay corner boards, all window surrounds, a belt course
  at each floor line, the outer frame of the facade, and the cornice band at the top.
- **The shingled hood**, ~10.6 → 11.8 m: a hipped, gray-shingled false mansard spanning
  between the two bay tops over the recessed centre, hipped at both ends, tucked under
  the cornice.
- **The cornice band, 11.77 → 12.07 m**: a flat yellow-trimmed parapet band, the crest.

**North-east flank** — party line with 126 South Park, whose roof is 7.3 m. The upper
4.8 m of this wall therefore stands clear above the neighbour and is visible from the
park and from the air. *No source shows it.* Treat it as blank painted siding: that is
what a 1913 party wall over a lower neighbour is, and it is the honest default. Do not
invent windows on it.

**South-west flank** — party line with 136 South Park, whose roof is only 3.2 m, so
almost 9 m of this wall is exposed. The one aerial frame shows an open yard on this side
before the tall corrugated-metal building further along, meaning this flank reads as a
full-height blank wall from the street. *Inferred*, same treatment as the north-east.

**North-west (rear)** — the back of the rear cottage on the rear lot line. *No source
shows it.* Blank, one or two small openings at most.

**The courtyard** — from the 2021 nadir: bare concrete and hardstanding, a **wooden deck
and external stair** against the rear cottage's south-east face, dumpsters and a tarped
pile against the party walls. Model the deck and stair; the dumpsters and the tarp are
this-week clutter and are excluded by the scope rule.

**Above** — see 2.9.

### 2.5 Recognition cues (ranked)

1. **The twin bays outlined in butter-yellow trim** over pale siding. Nothing else on
   this arc of the oval is a painted wood front, and the trim is what a viewer at any
   distance actually sees.
2. **The two-volume lot** — flats, open courtyard, rear cottage. Unique in the planned
   set apart from 551 Third, and the only reading available from directly overhead.
3. **The oxblood base with the black arched carriage gate.** A dark saturated band at
   ground level under a pale body, with a hole punched through it.
4. **The height step.** 12.07 m between a 7.3 m neighbour and a 3.2 m one; from the park
   the building reads as a narrow tower in a low row.
5. **The shingled hipped hood** under the cornice — small, but it is the one piece of
   period ornament and it breaks the roofline silhouette.

### 2.6 Miniature translation

The style bible's toy grammar suits this building almost without argument: it is already
a chunky rectangular solid with two projecting boxes, a plinth of a different colour, and
a trim system that reads as an outline. The translation is mostly about *what to leave
out*.

- **Exaggerate the trim.** Real trim boards are ~0.15 m; take them to 0.22 m and give
  them 0.04 m of relief so the yellow reads as a drawn outline from 200 m up. This is the
  one semantic exaggeration this asset gets and it should be unapologetic.
- **Exaggerate the bay projection** from 0.55 m to 0.70 m, so the shadow line between bay
  and centre strip survives the toy lighting.
- **Chamfer everything.** 0.06 m bevels on the bay corners, the cornice, the base cap and
  the parapet ring, per the bible's chunky-beveled-massing rule.
- **Simplify the windows** to flat `Toy_glass` panels recessed 0.08 m in a yellow
  surround. No mullion geometry, no sills beyond the trim, no glazing bars — the rhythm
  carries the reading, not the joinery.
- **Keep the base a plinth.** Do not let it grow toward a storey; its shortness relative
  to the floors above is a real proportional signature of the type.
- **Do not model the shingles.** The hood is one hipped solid in a flat gray, with a
  0.06 m bevel. Shingle texture is exactly the "information the camera cannot resolve"
  the bible tells you to strip.
- **The courtyard stays empty.** The temptation is to floor it so the asset reads as one
  object; resist it. The void is cue 2.

### 2.7 Massing recipe

All heights are metres above the asset datum `y = 0`, which is the **front block's**
ground.

**Front block** — extrude the front polygon, `t 0 → 10.30`, full lot width.

| Element | From | To | Notes |
|---|---|---|---|
| oxblood base | 0.00 | 2.24 | plinth; 0.05 m proud of the siding above, with a bevelled cap |
| floor 1 | 2.24 | 5.42 | |
| floor 2 | 5.42 | 8.59 | |
| floor 3 | 8.59 | 11.77 | |
| roof deck | 11.77 | — | flat membrane |
| cornice band | 11.77 | **12.07** | the crest; a continuous ring around all four walls |

- **Bays**: two boxes 2.80 m wide, from `y = 2.24` to `y = 11.77`, projecting 0.70 m
  (exaggerated) beyond `t = 0`. Left bay at `s [0.00, 2.80]`, centre strip
  `s [2.80, 3.89]`, right bay at `s [3.89, 6.69]`.
- **Shingled hood**: a hipped solid over the centre strip and returning onto the bay
  tops, `y 10.60 → 11.80`, hipped at both ends, projecting to the bay face line.
- **Base openings**: the sash window at `s [0.55, 2.05]`, `y [0.75, 1.85]`; the arched
  gate at `s [3.55, 6.25]`, `y [0, 2.05]`, springing to a segmental arch at 1.55 m.
  Recess both 0.12 m into `Toy_ink`.
- **Roof furniture**: one 1.1 × 0.8 m skylight, two 0.15 m vent stacks 1.0 m tall, both
  toward the rear third of the deck, as the 2021 nadir shows.

**Rear cottage** — extrude the rear polygon, `t 19.00 → 29.974`, full lot width.

| Element | From | To |
|---|---|---|
| base (buried) | **−0.60** | 0.00 |
| floor 1 | 0.00 | 3.94 |
| floor 2 | 3.94 | 8.40 |
| roof deck | 8.40 | — |
| parapet | 8.40 | **8.75** |

The base is deliberately extended to `y = −0.60` so that any real fall in the ground
toward the rear (see 2.15 risk 4) cannot open a gap under it. **This must not become the
model's `min Z`** — the front block's base at `y = 0` is the datum, and the validator
checks `min Z ≈ 0`, so either author the buried skirt as part of the front block's object
or accept a `min Z` of −0.60 and justify it explicitly in `validation.json`. Preferred:
keep `min Z = 0` by seating the cottage at 0 and adding a separate 0.60 m skirt below,
excluded from the height normalization.

- **Openings**: a simple punched grid, three per floor on the courtyard (south-east)
  face, none on the flanks, at most two on the rear.
- **Courtyard deck and stair**: a wood platform ~2.6 × 1.6 m against the cottage's
  south-east face at `y ≈ 0`, with an external stair rising to the first floor along the
  north-east party wall. Observed in the 2021 nadir.

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_cream` | `#f2ede3` | front block lap siding, all three floors, all four walls |
| `Toy_mustard` | `#d9a441` | **all trim**: bay corner boards, window surrounds, floor belt courses, facade outer frame, cornice band |
| `Toy_red` | `#c4453c` | the oxblood ground-floor base and its cap |
| `Toy_glass` | `#2a4d73` | every window, front block and cottage |
| `Toy_roofd` | `#45454a` | the shingled hipped hood; the arched carriage gate leaf |
| `Toy_steel` | `#9aa0a6` | both roof membranes, vent stacks, skylight frame |
| `Toy_ink` | `#3a3530` | window and gate recesses, the arch soffit |
| `Toy_sand` | `#ece4d4` | rear cottage walls |
| `Toy_rust` | `#a86444` | the courtyard deck and stair |
| `Toy_glass_Glow` | `#2a4d73` | the lit bay windows at night |

Two palette notes to record in `REPORT.md`:

- **`Toy_red` is brighter than the real base**, which is a dark oxblood closer to
  `#6d2c2e`. The palette carries no dark maroon, and the bible's §7 wants accents
  saturated rather than muddy. Taking the base to `Toy_red` reads as the same decision
  the real painter made, one step toward candy. If it fights the yellow at review, the
  fallback is `Toy_rust` `#a86444`, not an off-palette maroon.
- **`Toy_mustard` is the accent budget, all of it.** The trim is the identity; nothing
  else on this asset may take a second saturated colour. In particular do not reach for
  `Toy_gold` on the cornice.

**Night state (required).** Glow surfaces must be thin shells proud of the opaque glazing —
the app renders `_Glow` in a separate layer that is ~12% alpha by day, so a primary surface
must never be authored as glow. **Hero glow: the two bays**, lit as a pair of stacked
lanterns — five or six of the twelve bay windows, scattered across floors and across both
bays, never a full grid. This is a lived-in building on a park and the night reading is
"someone is home", not "office tower". Supporting accent: one window on the rear
cottage's courtyard face, so the void between the two volumes is legible at night as well
as by day. Nothing else glows — no gate lamp, no roof, no cornice.

The night proposition here is deliberately quieter than 135 South Park's lit roof
monitor. From the aerial camera this building's job at night is to be the one *warm*
residential front on an arc of dark commercial roofs.

### 2.9 Top surface

Two flat roofs 12 m and 8.8 m up, 8.7 m of open ground between them, in a district the
camera flies over constantly. Composition, south-east to north-west:

- the **shingled hood** at the street edge, a mid-dark gray wedge breaking the parapet
  line — the first thing seen from above and the tell that this is not another flat box;
- the **light membrane deck** of the front block with the **yellow cornice ring** bright
  around it, one skylight and two slim stacks grouped toward its rear third;
- the **courtyard**, a shadowed void the full width of the lot, with the wood deck and
  stair as the only objects in it — this reads as a dark slot between two light roofs
  and it is the plan-view identity;
- the **cottage roof**, lower, plainer, its own thin parapet, nothing on it.

Keep three values clearly separated from above: cornice/parapet rings brightest
(`Toy_mustard` on the front, `Toy_sand` on the cottage), membranes mid (`Toy_steel`),
hood darkest (`Toy_roofd`). The courtyard supplies the fourth value for free, as
terrain in shadow.

### 2.10 Scope

**In the GLB:** the front flats block (base, gate, sash window, bays, trim system,
shingled hood, cornice, roof deck, skylight, two vent stacks); the rear cottage (two
storeys, parapet, roof deck, punched openings); the courtyard wood deck and external
stair.

**Not in the GLB:** South Park (street or park), 126 and 136 South Park, the corrugated
building further along the row, street trees, sidewalk, parked cars, the courtyard
dumpsters and tarped pile, utility poles and overhead wires, people, plinths, cameras or
lights.

### 2.11 Triangle budget

Cap **9,000** — above 135 South Park's 8,000 because this asset is two shells with a
trim system, and the cap should bind. Suggested split:

| Element | Tris |
|---|---|
| front block shell, base, cornice ring, bevels | 2,000 |
| two bays with bevelled corners | 1,200 |
| trim system (belt courses, surrounds, frame) | 1,800 |
| 20 window recesses + glass panels | 1,400 |
| shingled hood | 400 |
| base openings incl. the segmental arch | 600 |
| front roof deck, skylight, stacks | 400 |
| rear cottage shell, parapet, openings | 900 |
| courtyard deck and stair | 300 |

The trim system is the expensive part and it is the identity — if the cap binds, take
the tris out of the window recesses (flatten them to decals on the wall plane) before
touching the trim.

### 2.12 Draft manifest entry

```json
{
  "id": "132-south-park",
  "file": "132-south-park.glb",
  "anchor": [
    -122.3946190,
    37.7815407
  ],
  "targetHeightM": 12.07,
  "cat": 2,
  "name": "130-134 South Park",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

`loadRadius` follows the default rule `max(2500, targetHeightM × 30)` = `max(2500, 362)`
= **2500**, the same as every other South Park asset. Nothing about a 12 m residential
building justifies `alwaysLoaded`.

### 2.13 Integration notes (for later, not this task)

**Case B — new landmark.** No `132SouthPark` exists in `pipeline/lib/landmarks.mjs` or
`app/src/landmarks.js`, so integration needs a registry entry and a tile re-bake as well
as the manifest entry. `camelId('132-south-park')` = `132SouthPark`; the registry id must
match exactly or the loader will not associate the two.

**This lot needs three exclusion zones, and a single radius cannot work.** The reasoning,
measured against the rings the bake actually sees — DataSF `ynuv-fyni` after
`simplifyRing(0.6)`, with `excluded()` dropping a footprint whose ring **centroid OR any
vertex** falls inside a zone:

*From the anchor (the courtyard bbox centre, `-122.3946190, 37.7815407`):*

| Distance | What |
|---|---|
| 3.60 m | **126 South Park (SF3775061), nearest vertex — the ceiling** |
| 3.94 m | this lot's own front block, nearest vertex |
| 6.13 m | this lot's own rear block, nearest vertex |
| 8.49 m | own front block, ring centroid |
| 10.40 m | own rear block, ring centroid |

So the usable window at the anchor is `(0, 3.60)` and **nothing this lot owns is inside
it**. A single radius that reaches either of this lot's own centroids at 8.49 / 10.40 m
would delete 126 South Park, and at 9.6 m it would also take 136. 126 and 136 have no
GLB to replace them, and the failure is silent.

*Therefore: two extra zones, each sitting exactly on one footprint's ring centroid and
dropping it by the centroid test, sized the way 551 Third's kiosk zone is:*

| Zone | Centre | Own trigger | Nearest foreign trigger | Radius | Margin |
|---|---|---|---|---|---|
| front flats | `-122.3945566, 37.7814859` | 0.00 m (centroid) | 5.86 m — 126 South Park vertex | **3** | 2.86 m |
| rear cottage | `-122.3947038, 37.7816116` | 0.00 m (centroid) | 5.31 m — 136 South Park vertex | **3** | 2.31 m |

*And a third, small zone at the anchor itself, which drops nothing today and is there for
one specific reason:* `markOccupied()` in `pipeline/buildings.mjs` runs only for
footprints that survive `excluded()`. Once the two DataSF footprints are dropped, this
lot registers as **unoccupied**, and the Overture gap-fill pass adds any footprint whose
bbox is less than 25% occupied. Overture is not known to carry a building here (OSM does
not, and Overture's SF buildings are largely OSM), but if it does, a whole-lot polygon
would have its centroid within ~0.6 m of the anchor and would sail straight through the
two off-centre zones and reappear as a procedural box inside the model. `exclude: 2` at
the anchor catches that centroid with 1.60 m of clearance to 126's vertex. **Verify this
at re-bake time rather than trusting the argument** — `node pipeline/verify-rebake.mjs`
reports what is left standing in each zone.

Proposed registry entry:

```js
{
  // 1913 flats on the North-west arc of the South Park oval. The lot carries TWO
  // baked footprints — the flats 8.5 m south-east of the anchor and the rear
  // cottage 10.4 m north-west of it — and the anchor itself sits in the open
  // courtyard between them, because that is where the GLB's bounding-box centre
  // has to be. No single radius works: reaching either own centroid needs
  // r > 8.4 m and 126 South Park's nearest vertex is 3.60 m out. Hence one zone
  // per structure, each dropping its footprint by the centroid test.
  //
  // The 2 m zone at the anchor drops nothing today. It is the guard against the
  // Overture gap-fill pass re-filling a lot that `markOccupied()` no longer sees
  // as occupied once the DataSF footprints are excluded — a whole-lot Overture
  // polygon would centre within ~0.6 m of the anchor and miss both other zones.
  // Do not raise it: 126 South Park's vertex is at 3.60 m and it has no GLB.
  id: '132SouthPark',
  name: '130-134 South Park',
  lon: -122.3946190,
  lat: 37.7815407,
  height: 12.07,
  exclude: 2,
  extraExclusions: [
    { lon: -122.3945566, lat: 37.7814859, r: 3 }, // front flats
    { lon: -122.3947038, lat: 37.7816116, r: 3 }, // rear cottage
  ],
  // Camera bearing = 180 − yaw (camera.js apply(): offset is (sin yaw, ., cos yaw)
  // and +z is south), so yaw 45 stands the camera at bearing 135 = SE, square onto
  // the park front. Same value as 380Brannan, whose front faces the same way.
  camera: { distance: 200, yaw: 45, pitch: 26 },
},
```

No `key`: at 12 m this is texture in the block, not a destination.

**Batch mode.** Other South Park landmarks are in flight. Run the bake for the Step 5/6
QA — a Case B landmark cannot be judged without its exclusion applied — then discard it
(`git checkout -- app/public/tiles api/_data`) and commit source only: the GLB, the
manifest entry, the registry entry, this plan and `artifacts/132-south-park/`. See
`docs/asset-pipeline/BATCH-INTEGRATE.md`.

**Expect the terrain under this asset to be flat.** The sim samples one elevation at the
anchor and seats the whole GLB there. See 2.15 risk 4 for the 0.48 m question that makes
the rear cottage's buried skirt necessary.

### 2.14 Validation checklist

- [ ] Binary `.glb`, real metres, applied transforms, no negative scales
- [ ] Tallest geometry exactly **12.07 m** (front block cornice crest)
- [ ] `min Z ≈ 0` at the front block base; the cottage's buried skirt does not lower it
- [ ] XY centre ≈ (0, 0) — **in the courtyard, with no geometry near it**; confirm this
      is the bbox centre and not a mis-centred export
- [ ] Axis-aligned XY bbox ≈ 26.3 × 26.3 m; front wall bearing 135.1°
- [ ] Two disjoint shells; **per-object signed volume** used as the normals authority,
      not a union ray test
- [ ] The courtyard is empty — no floor plate, no accidental connecting geometry
- [ ] ≤ 9,000 triangles
- [ ] Materials all `Toy_*`, flat, no textures, no transparency, no `Toy_body`
- [ ] Exactly one `_Glow` material, on thin shells proud of the opaque glazing
- [ ] No cameras, lights, animations, armatures, constraints, foreign geometry
- [ ] Night render shows a scattered subset of bay windows lit, not a full grid
- [ ] Top view reads front block / courtyard / cottage without a caption

### 2.15 Open questions and risks

1. **One photograph carries the entire facade.** Every statement in 2.4 about the front
   — the lap siding, the yellow trim, the oxblood base, the arched gate, the shingled
   hood, the bay rhythm — comes from a single 2021 drone frame in a real-estate gallery.
   It is a good frame: square-on, unobstructed, high resolution. It is still one frame,
   from one afternoon, by one photographer with an interest in the building looking
   well. The modeller's first job is Street View. *Mitigation:* the massing and the
   heights do not depend on it at all, so a wrong colour is a repaint, not a rebuild.

2. **Nothing shows the flanks or the rear.** Nearly 5 m of the north-east wall and 9 m of
   the south-west wall stand clear above their neighbours and will be seen from the park
   and from the air. This plan says "blank painted siding" on both, which is what a 1913
   party wall over a lower neighbour normally is, and is `inferred`. If photography shows
   windows, add them; do not add them speculatively.

3. **5 units or 7.** The assessor has recorded 5 units and 20 rooms unchanged since 2007;
   the 2021 listing advertises 7. The likely explanation is unpermitted or
   unreported-to-assessor units, quite possibly in the rear cottage. It changes nothing
   about the geometry and is recorded only so the next reader does not spend an hour on
   it.

4. **The 0.48 m ground question.** The LiDAR gives the front block a ground elevation of
   8.98 m NAVD88 and the rear cottage 8.50 m — but from two different source tiles
   (`Sanfran_Orig_1384.flt` and `_1380.flt`). South Park is flat, and a 0.48 m fall over
   20 m of a mid-block lot is more likely a seam between tiles than real topography. This
   plan therefore adopts **one datum** and puts the cottage crest at its full 8.75 m,
   with a 0.60 m buried skirt so that if the fall *is* real, nothing floats. The cost of
   being wrong in this direction is a skirt nobody sees; the cost of the other direction
   is a visible gap.

5. **No architect, no historic status established.** Searches turned up neither an
   architect of record for the 1913 building nor any designation for the lot. South Park
   as a whole has obvious historic interest and several neighbours are named
   contributors, but this dossier could not confirm anything for lot 062 and therefore
   asserts nothing. Do not write "contributor to the South Park Historic District" into
   `REFERENCE.md` on the strength of the neighbourhood.

6. **OSM has nothing here.** Worth stating plainly because every other plan in this set
   starts from an OSM way: for lot 062 there is no building, no address node, no height
   tag. Nominatim answers "132 South Park" with the *street* (way 8916553). The
   consequence is that the footprint in 2.3 is reconstructed from the surveyed parcel
   plus the 2010 LiDAR polygons and a 1.1 m registration correction, rather than traced.
   The reconstruction is defensible — party-wall-to-party-wall on a 22 ft SF lot is not a
   guess — but it is a reconstruction, and if the modeller finds a source that shows a
   real setback or a light well, that source wins.

7. **The exclusion design is the most intricate in the registry.** Three zones, two of
   them working through the centroid test only, and one of them a guard against a
   footprint that may not exist. Every number in 2.13 was measured; none of them should
   be adjusted without re-measuring, and `node pipeline/audit.mjs` check 1.6 plus
   `node pipeline/verify-rebake.mjs` are the gate.
