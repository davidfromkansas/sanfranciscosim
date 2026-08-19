# 424 Brannan Street (Tower Valet Parking lot) — SF-SIM asset plan

A 2,026 m2 hole in Central SoMa. 424 Brannan is not a building and never has
been: it is a Z-shaped through-block **surface parking lot** — 60 striped stalls
run by Tower Valet Parking — that reaches Brannan Street through a 15.8 m neck,
Ritch Street along a 68.4 m fence, and Zoe Street through a 25.6 m gate. The
assessor calls it a vacant lot and values the improvements at $0. An entitled
SOM office scheme (288 Ritch / 55 Zoe) has been on the boards since 2019 and has
never broken ground.

Its job in the city is the opposite of every other asset in the Brannan family:
where they hold a street wall, this one **breaks it**. From the app's aerial
camera the block reads as a solid ring of roofs with one pale, ordered rectangle
of asphalt punched through the middle of it — and that void, striped and fenced
and half full of parked cars, is the whole subject. Model the absence, not the
architecture.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/424-brannan/`. This document is the plan only: Part 1 is the runnable
task prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `424-brannan` |
| Existing procedural builder | none — new landmark (Case B). The bake currently draws **nothing** on this parcel, which changes what the exclusion radius is for; see 2.13 |
| WGS84 anchor | `-122.3954857, 37.7798744` (axis-aligned bbox centre of the parcel) |
| Target height | **the model's vertical extent**, not an architectural height — this is a terrain-draped ground asset. Expect ~8.6 m; the manifest takes the validated bbox height exactly |
| Footprint | 2,026.1 m2 measured; 88.72 x 59.59 m axis-aligned bbox at a 45.2 deg heading |
| Triangle cap | 18,000 |
| Category | `23` (parking) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 424 Brannan Street parking-lot GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of the surface parking lot at 424 Brannan
Street, San Francisco (block 3776 lot 455, operated as Tower Valet Parking) and
deliver it as a downloadable, validated GLB.

**There is no building on this site and you are not modelling one.** The subject
is the lot: the paved plate, its striping, its fence, its gates, its sign, its
attendant's booth and the cars standing in it. If you find yourself designing a
facade, you have misread the brief — re-read 2.1 of the plan.

Do not integrate or deploy the model yet. Create the asset, validate it, render
review images, and commit the deliverables to your working branch.

## Read the project sources first

Before any research or modeling, read in this order:

1. `AGENTS.md`
2. `docs/styles/README.md`
3. `docs/styles/miniature-toy.md` — especially §13 (roads and ground plane),
   §14 (vehicles), §16 (environmental storytelling) and §26, which names this
   exact problem: *"huge parking lot -> smaller graphic parking"*
4. `.agents/skills/sf-miniature-style/SKILL.md`
5. `.agents/skills/sf-asset-check/SKILL.md`
6. `app/public/sf-assets/landmarks_manifest.json`
7. **`artifacts/64-south-park/`** — the reference implementation. It is the only
   shipped asset whose subject is the GROUND, and its `REFERENCE.md` section
   "The terrain drape — read this before changing anything" is required reading
   before you model a single face. Its `sample_terrain.mjs` is the script to
   adapt, not to rewrite.
8. `artifacts/551-third/` — the other open-air site asset (Shell forecourt): pole
   sign, kiosk, painted ground graphics, and a measured site plan reprojected
   into the site's own frame. Copy its measurement discipline.
9. `artifacts/400-brannan/` — a neighbour on this block face, for the family's
   palette, bevel language and night restraint
10. `docs/asset-plans/424-brannan.md` — this plan, whose dossier is your research
    starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules.

## Must capture

- The **Z-shaped paved plate** on its real parcel polygon (2.3), pale warm grey,
  visibly a worn slab rather than fresh black asphalt
- **Ordered stall striping** — the lot's only architecture. 60 stalls in five
  rows around a central aisle (2.7), painted, reading clearly from the aerial
- **Concrete wheel stops** at the head of the perimeter bays
- A **chain-link perimeter fence with a barbed topping**, continuous on all three
  street frontages and along the party boundaries, with the two real gates:
  the wide rolling gate on **Brannan** and the swing gate on **Zoe**
- The **tall red-and-white PUBLIC PARKING pole sign** at the Brannan gate. This
  is the lot's identity and the one place semantic exaggeration is spent
- The **attendant's booth** against the Ritch fence, and the white box trailer
  standing beside it
- **Parked cars** — a curated ~18, not 60: chunky, cleanly coloured, in the rows,
  with deliberate gaps so the lot reads as a working lot and not a car park model
- The two green masses: the **volunteer thicket in the north notch** and the
  **shrub at the Brannan corner**
- The fall of the land: the site drops 1.47 m west-south-west and the plate must
  follow it (see "Terrain drape" below)

## Research the site independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
parcel polygon, the WGS84 anchor, the terrain profile, and — critically — **that
the lot is still a parking lot and not a construction site**. Two 2019 permits
for a 7-storey office building sit at status `filed` and the SFPD parking permit
was last renewed 2026-06-24, but imagery ages. If ground has broken, stop and
report; do not model a lot that no longer exists.

Gather references covering:

- Nadir aerial at the highest zoom available, with the parcel ring overlaid — the
  stall rows, the aisle, the booth and the surface patching are only legible there
- Street-level views from **all three** frontages (Brannan, Ritch, Zoe): the fence,
  the gates, the sign, the wheel stops, the surface colour
- The sign itself, close enough to read its proportions and its palette

## Create a reference dossier

Write `artifacts/424-brannan/REFERENCE.md` containing: source links and what each
establishes; verified dimensions and location; the terrain profile and how you
sampled it; observations from all three frontages and from above; the 3–5
strongest recognition cues; features to preserve; features to simplify;
uncertainties and conflicting evidence. Do not commit copyrighted full-resolution
imagery.

## Make your own design decisions

Follow the conversion process in `docs/styles/miniature-toy.md` §22, adapted:
identify the recognition cues, strip nonessential information, rebuild the site
from a few confident volumes and one strong ground graphic, exaggerate only the
signature features, evaluate from the app's high three-quarter aerial camera,
then simplify again.

The trap specific to this asset is **noise**. A real parking lot is 60 nearly
identical rectangles, a hundred cracks, a dozen patches and a scatter of debris —
render all of it and you get visual mush at city scale. The style bible's answer
(§26) is a *graphic* parking lot: one clean plate, one crisp stripe rhythm, one
strong fence line, one hero sign, a few chunky cars. Everything else is texture
you are not allowed to have.

The second trap is **emptiness**. Strip too much and the asset reads as a
demolition site or a hole in the tiles. Rule 3 of `AGENTS.md` means a landmark
that fails to appear degrades to procedural — but here there is no procedural
building to fall back to, so an under-designed asset simply looks like a bug.
Between those two failure modes, err toward the graphic and let the cars,
the sign and the booth carry the life.

## Terrain drape — the thing that will break this asset if you skip it

`placeGeneric()` in `app/src/assets.js` seats a landmark with ONE terrain sample
taken at the anchor. That is right for a building and wrong for an asset that IS
the ground. This site falls **1.470 m** across its 88.7 x 59.6 m bbox, so a flat
plate seated at the anchor would be buried ~0.78 m under the terrain at the Zoe
end and floating ~0.69 m above it at the Brannan corner — invisible in every
Blender render and obvious in the app.

The good news, measured: the terrain under this lot is very nearly a **plane**.
A least-squares fit over 8,104 samples gives

```
dy = 0.02047 * X + 0.00742 * Y + 0.0057      (metres, X east, Y north, relative to the anchor's ground)
```

with a **maximum residual of 0.101 m**. So the drape here is a simple tilt, not
South Park's 1-D profile — but sample it, do not hard-code these coefficients.
Write `artifacts/424-brannan/sample_terrain.mjs` (adapt South Park's), have it
emit the fitted plane AND the residual, and assert the residual in the validator.

Two deliberate contract deviations follow, and both must be asserted by your
validator rather than left looking like slips:

- **`min_z` goes negative.** z = 0 is the anchor's ground, because that is where
  the loader puts it. Replace the "min_z ≈ 0" check with "the plate's top face
  stands a constant height above the sampled terrain over its whole area" —
  measure the spread and report it.
- **`targetHeightM` is the model's vertical extent**, not an architectural
  height, because the loader's scale is `targetHeightM / bbox height` and must
  land on 1.0. Confirm it in the app console: `uniform x1.0000`.

## Scope of the exported asset

**In the GLB:** the paved plate and its edge kerb; the painted stall striping and
aisle markings; wheel stops; the perimeter chain-link fence, its barbed topping,
its posts, and the Brannan and Zoe gates; the PUBLIC PARKING pole sign; the
attendant's booth; the box trailer; ~18 parked cars; two or three lot light
poles; the north-notch thicket and the Brannan-corner shrub.

**Not in the GLB:** Brannan, Ritch or Zoe roadway or sidewalk; the city's wooden
utility poles and overhead wires; the cobra-head streetlight; the neighbouring
buildings on any side, including the mural painted on the party wall that faces
into the lot; the fire hydrant; street trees in the public right of way;
plinths, cameras or lights.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full, **with the two drape
deviations named above**. At minimum: binary `.glb`; real-world meters; applied
transforms; no negative scales; outward normals; no duplicate or foreign
geometry; no image textures; no transparency; flat-color materials named `Toy_*`
from the project palette; `_Glow` suffix only on surfaces that glow at night; no
`Toy_body`; no cameras, lights, animations, armatures or constraints; at most
18,000 triangles.

**Chain-link is not a texture and not an alpha plane.** The contract forbids
both. Build it the way the toy kit would: chunky posts, a top rail, and a single
thin recessed slab per bay in a light steel tone standing for the mesh, with a
darker barbed strand above the rail. Judge it from the aerial, where a fence is a
line, not a surface.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model
drops into the city at its real-world heading — the loader applies no rotation.
The Ritch fence runs 135.2/315.2 deg; the Brannan frontage faces 135.2 deg (SE);
the Zoe frontage faces 225.2 deg (SW). Build directly on the measured polygon in
2.3 rather than modelling an axis-aligned rectangle and rotating it.

## Reproducible Blender workflow

Blender 5.2 LTS. Headless: `blender -b --python script.py -- args`.

Keep `artifacts/424-brannan/build_424_brannan.py` (deterministic build script),
`artifacts/424-brannan/sample_terrain.mjs`, `artifacts/424-brannan/424-brannan.blend`,
and `artifacts/424-brannan/424-brannan.glb`. The script must rebuild the model
reliably enough for future revision, and must read the terrain fit from the
sampler's JSON rather than embedding numbers.

## Required review renders

Render the exact final geometry from controlled cameras:
`424-brannan-top.png`, `424-brannan-north.png`, `424-brannan-east.png`,
`424-brannan-south.png`, `424-brannan-west.png`, plus
`424-brannan-contact-sheet.png`, at least one high three-quarter aerial beauty
render `424-brannan-aerial.png`, and a night render
`424-brannan-aerial-night.png`.

The four elevations must share scale, framing, lighting, exposure and projection.
**The top view is the hero here, not the aerial** — this asset is a ground
graphic and the plan view is where it is judged. It must clearly show the stripe
rhythm, the aisle, the fence line and the gates.

Also render `424-brannan-grazing.png`: a low, near-horizon camera along the long
axis. A draped plate that has gone wrong shows up there and nowhere else.

## Validate the exported GLB

Re-import `424-brannan.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture
count, camera count, light count, animation count, applied-transform status,
negative-scale status, normal-orientation status, unexpected geometry, and
per-material contract compliance.

Add these three site-specific assertions:

- plate-above-terrain spread over the whole plate (target < 0.02 m)
- terrain-plane residual as measured by `sample_terrain.mjs` (report it)
- `targetHeightM` equals the measured bbox height to 1 mm

Write `artifacts/424-brannan/validation.json` and `artifacts/424-brannan/REPORT.md`.

The axis-aligned XY bounding box will be roughly **89 x 60 m** even though the
lot's own dimensions are 68.4 m along Ritch by 46.8 m across the belly — that is
the expected consequence of a 45 deg real-world heading, not a scale error.

## Manifest draft

Verify the real WGS84 anchor yourself, then include this draft entry in
`REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "424-brannan",
  "file": "424-brannan.glb",
  "anchor": [
    -122.3954857,
    37.7798744
  ],
  "targetHeightM": <measured bbox height>,
  "cat": 23,
  "name": "424 Brannan Street Parking",
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
for that, together with the integration notes in `docs/asset-plans/424-brannan.md`.
````

---

## Part 2 — Research and design dossier

Compiled 18 August 2026 from the sources in 2.2. Values marked *inferred* are
visual or derived estimates, not published figures — the executing agent must
re-verify anything it relies on.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Address resolution | `424 BRANNAN ST` -> parcel **3776455** (block 3776, lot 455) | DataSF EAS address layer (`ramy-di5m`) — **measured** |
| Parcel address range | 424–424 Brannan St, even side; one address on one lot | DataSF parcels (`acdm-wktn`) |
| **Buildings on the parcel** | **none** | DataSF building footprints (`ynuv-fyni`, `mblr = 3776455`): **0 records**. OSM has no `building` way on the lot either — **measured** |
| Assessor class | **V — Vacant Lot**; 0 stories, 0 units, property (improvement) area **0.0** | SF Assessor secured roll (`wv5m-vpq2`), rolls 2023, 2024, 2025 identical — **measured** |
| Assessor lot area | 21,348 sq ft (1,983 m2) | same |
| Measured lot area | **2,026.1 m2** (21,809 sq ft) | DataSF parcel polygon, reprojected — **measured**; +2.1% vs the assessor's figure, which is normal rounding on an irregular lot |
| Marketed area | ±21,400 sq ft / 0.49 acre | Colliers offering via LoopNet & MLS 423907247 — corroborates |
| Use | **Commercial parking lot, 60 stalls**, DBA Tower Valet Parking Inc | SFPD permit 500106, renewals granted Jan 2024 and **2026-06-24** — **measured** |
| OSM | way 124889469 `amenity=parking` `parking=surface` `surface=asphalt` `fee=yes` `access=yes` `operator=Tower Valet Parking`, 1,911.9 m2 | **measured**; agrees with the parcel to −5.6%, the difference being the fence line sitting inside the boundary |
| Zoning | CMUO (Central SoMa Mixed-Use Office) | DataSF parcels |
| Assessed value | land $24,541,417 / **improvements $0** | LoopNet public-record panel — corroborates "vacant lot" |
| Frontages | **Ritch St 68.40 m** (the long side, NE); **Zoe St 25.62 m** (SW); **Brannan St 15.83 m** (SE neck) | measured from the parcel polygon against DataSF/OSM street centrelines |
| Frontage headings | Brannan frontage faces **135.2 deg** (SE); Ritch fence faces **45.2 deg** (NE); Zoe frontage faces **225.2 deg** (SW) | measured |
| Ground | 5.11–6.58 m over the lot; **fall 1.470 m**, 2.18% toward bearing 250 deg | baked terrain (`app/public/tiles/terrain.bin`, the sampler the runtime uses), 8,104 samples — **measured** |
| Terrain shape | a plane to within **0.101 m** max residual | same — **measured**; this is what makes the drape a simple tilt |
| Entitled scheme | 288 Ritch St + 55 Zoe St, two offices, 126,600 sq ft, 74 ft, SOM for DECA Companies | SFYIMBY Dec 2021; an earlier 8-storey 239-room hotel and a Heller Manus office pair (2019) preceded it |
| Construction status | **not built.** DBI permits 201912230246 and 201912230259 (7-storey office + basement parking) are both still at status `filed`, filed 2019-12-23, never issued | DataSF DBI permits (`i98e-djp9`) — **measured** |

### 2.2 Sources

- `https://data.sfgov.org/resource/ramy-di5m` (DataSF EAS Addresses) — address -> parcel 3776455
- `https://data.sfgov.org/resource/acdm-wktn` (DataSF Parcels) — the 12-vertex lot polygon, zoning, address range
- `https://data.sfgov.org/resource/ynuv-fyni` (DataSF Building Footprints, LiDAR-derived) — **returns nothing for this parcel**, which is the single most important fact in this dossier and also means the bake has nothing here to exclude
- `https://data.sfgov.org/resource/wv5m-vpq2` (SF Assessor Historical Secured Property Tax Rolls) — class V, 0 stories, 0 improvement area
- `https://data.sfgov.org/resource/i98e-djp9` (DataSF DBI permits) — the two never-issued 2019 office permits
- `https://www.openstreetmap.org/way/124889469` — the parking polygon, operator, surface, fee
- `https://www.openstreetmap.org/way/1504713558` — a separate 407 m2 `access=private` surface lot filling the notch north of this parcel; **not part of this asset**
- `https://www.sanfranciscopolice.org/get-service/permits/hearing-calendar-results/permit-500106-2026-06-24` — commercial parking lot permit, renewal granted; and the Jan 2024 SFPD hearing-results PDF, which is where the **60 stalls** figure comes from
- `https://www.loopnet.com/Listing/424-Brannan-St-San-Francisco-CA/29453110/` (Colliers offering) — "currently improved as a surface parking lot with ±60 striped stalls, leased to Tower Valet Parking, Inc. on a month-to-month basis"
- `https://sfyimby.com/2021/12/new-renderings-for-som-designed-offices-at-424-brannan-street-soma-san-francisco.html` — the SOM 288 Ritch / 55 Zoe scheme and the site's three-frontage geometry
- `https://socketsite.com/archives/2019/10/hotel-plans-scrapped-office-buildings-now-on-the-boards.html` — the 2019 Heller Manus scheme and the lot-split manoeuvre
- `https://www.decaco.com/case-studies/424-brannan` — DECA's own project page
- Google satellite tiles z20/z21 (`mt1.google.com/vt/lyrs=s`), stitched and overlaid with the parcel ring — the stall rows, the aisle, the booth, the trailer, the two green masses, the surface patching
- Google Street View panoramas, all three frontages: `WXVXu81elVTxkdR3rXr1Zw` and `TUpIDbEopCNF5mypbXJ5aA` (Brannan), `SAz7nIhGlLCIhM4mORH_HQ` (Ritch), `c--Aph5B6JJAhIFghHOESA` (Zoe) — fence, gates, sign, wheel stops, striping colour, surface tone

Exa searches run: `424 Brannan Street San Francisco parking lot Tower Valet Parking development`
and `424 Brannan Street San Francisco surface parking lot aerial photo site plan 288 Ritch 55 Zoe`.
The domains that actually yielded site facts were sanfranciscopolice.org (the stall
count), loopnet.com (the lease and the improvement value), sfyimby.com and
socketsite.com (the unbuilt schemes). No photograph is redistributed here; the
URLs and the panorama ids are recorded so the modeller can open them.

### 2.3 Orientation and placement

The lot is a **through-block Z**. Its long boundary is the Ritch Street fence; a
15.8 m neck reaches southeast to Brannan between the Brickhouse restaurant (426
Brannan) and the corner; a 22.8 m tail reaches southwest to Zoe. The southwest
boundary is a party line against the backs of 426 and 434 Brannan — the wall that
faces into the lot carries a large mural, which belongs to the neighbour and is
**not** part of this asset.

Measured DataSF parcel ring, in Blender coordinates (metres, `+X` east, `+Y`
north), centred on the anchor `-122.3954857, 37.7798744`. `u` runs northeast
along Brannan, `v` runs southeast toward Brannan; the site frame is the honest
one to design in and the Blender columns are what the script builds from.

```
        X         Y          u        v      terrain dy
 V0   -26.315   18.367     -5.73   -31.58     -0.414
 V1   -20.948   12.985     -5.71   -23.97     -0.397
 V2    -3.942   29.793     18.20   -23.92     +0.153
 V3    44.358  -18.638     18.34   +44.48     +0.695     <- east corner, Brannan/Ritch
 V4    33.118  -29.793      2.51   +44.48     +0.374     <- south corner, Brannan gate
 V5    17.016  -13.647      2.46   +21.67     +0.332
 V6    11.621  -19.001     -5.14   +21.67     +0.178
 V7    -9.963    2.197     -5.52    -8.58     -0.248
 V8   -26.262  -13.978    -28.48    -8.59     -0.641
 V9   -44.358    4.167    -28.54   -34.21     -0.784     <- west corner, on Zoe
 V10  -28.140   20.197     -5.74   -34.16     -0.414
```

Edges, with what each one is:

| Edge | Length | Faces | What it is |
|---|---|---|---|
| V2→V3 | **68.40 m** | NE 45.2 deg | **Ritch Street fence** — the long side |
| V3→V4 | **15.83 m** | SE 135.2 deg | **Brannan Street frontage** — the gate and the sign |
| V4→V5 | 22.81 m | SW 225.2 deg | party line, rear of 426 Brannan (Brickhouse) |
| V5→V6 | 7.60 m | SE 135.2 deg | party line jog |
| V6→V7 | 30.25 m | SW 225.2 deg | party line, rear of 434 Brannan |
| V7→V8 | 22.96 m | SE 135.2 deg | party line — Row C1 backs onto it |
| V8→V9 | **25.62 m** | SW 225.2 deg | **Zoe Street frontage** — the swing gate |
| V9→V10 | 22.80 m | NW 315.2 deg | party line, rear of the Zoe Street row |
| V10→V0→V1 | 2.58 + 7.61 m | NE 45.2 deg | the **north notch**, around the private 407 m2 lot (OSM way 1504713558) |
| V1→V2 | 23.91 m | NW 315.2 deg | party line along the north notch |

Because of the 45 deg heading the axis-aligned bounding box is 88.72 x 59.59 m
against a site that is 68.4 m long by at most 46.8 m across. That is correct.

Measured positions of the things standing on the lot, same frame:

| Feature | X, Y | u, v | Confidence |
|---|---|---|---|
| Attendant's booth | 1.82, 19.29 | 14.88, −12.40 | measured from z21 nadir; against the Ritch fence |
| White box trailer | −2.96, 18.53 | 10.96, −15.23 | measured from z21 nadir |
| North-notch thicket | −23.14, 20.46 | −2.00, −30.82 | measured from z21 nadir |
| Brannan-corner shrub | 33.10, −27.99 | 3.76, +43.18 | measured from z21 nadir; just inside V4 |
| PUBLIC PARKING pole sign | ~40, −22 | ~17, +43 | *inferred* — the real pole stands at the kerb, see 2.15 |

### 2.4 What each side shows

**Southeast (Brannan Street)** — the public face, and the only one most people
see. A 15.8 m gap in the street wall between the low timber-clad Brickhouse
restaurant and the corner. Across it: a chain-link fence with a **wide rolling
gate**, razor topping on the fixed runs, a small white `424 BRANNAN` plate wired
to the mesh, and — the thing you actually notice — a **tall red-and-white pole
sign**: a dark header band reading TOWER VALET PARKING, then PUBLIC PARKING in
white on red, a paragraph of small print, and a red "Enter Here" flash at the
bottom. A sandwich-board `$40` sign stands on the sidewalk beside it. A leggy
shrub mass fills the corner just inside V4.

**Northeast (Ritch Street)** — 68 m of chain-link with barbed topping, posts on a
regular pitch, standing over the kerb. Behind it the lot's densest row of cars,
nose-in to the fence, on **yellow stall stripes** with **concrete wheel stops**
at the head of each bay. The attendant's booth sits in this row about a third of
the way along.

**Southwest (Zoe Street)** — chain-link again, with a **braced swing gate** and a
short return. Beyond it the lot opens up: the western belly, the rows against the
party walls, the box trailer, and the brick warehouse on Ritch closing the view.

**The party boundaries** — blank painted masonry of 426 and 434 Brannan on the
southwest, one of them carrying a large teal-and-pink mural that faces into the
lot. Neither wall belongs to this asset. Build the fence and stop.

**Top** — the subject. A pale, warm-grey slab, visibly patched (one obvious
rectangle of newer, lighter concrete in the eastern belly) and map-cracked, with
five rows of yellow stalls around a spine aisle that runs from the Brannan gate
northwest into the belly and out at Zoe. Roughly half to two-thirds of the stalls
are occupied at any time. Two green masses, at the north notch and the Brannan
corner. No canopy, no structure of any size except the booth.

### 2.5 Recognition cues (ranked)

1. **The void** — a large pale ordered rectangle punched through a block of
   otherwise continuous roofs. Read from the aerial, this asset's silhouette is
   the shape of what is missing
2. The **stripe rhythm**: five rows of yellow bays around one spine aisle, the
   only ordered geometry on the site
3. The **continuous chain-link line** with its two gates, drawing the parcel
   outline as a hard edge in a district of soft ones
4. The **red PUBLIC PARKING pole sign** at the Brannan neck
5. **Parked cars** — the colour, and the only thing that says "in use" rather
   than "abandoned"

### 2.6 Miniature translation

**Preserve**

- The exact Z-shaped parcel polygon and the 45.2 deg heading
- The three-frontage condition: long fence on Ritch, narrow neck on Brannan, gate on Zoe
- Five rows / one spine aisle / 60 stalls
- The fall of the land, west-south-west at 2.18%
- The pale surface. This lot is *not* charcoal, and its paleness against the
  city's darker streets is half of why the void reads

**Simplify / exaggerate**

- Map-cracking, patching, oil staining and debris: **all gone.** One optional
  colour-shift panel for the concrete patch, nothing else. Style bible §6:
  weathering minimal by default
- 60 literal cars become **~18**, chunky and cleanly coloured, distributed with
  deliberate gaps
- Chain-link becomes posts + top rail + one thin recessed slab per bay; the
  barbed topping becomes a single dark strand
- The pole sign is thickened and enlarged ~25% so it survives at thumbnail size.
  This is the one place semantic exaggeration is spent (§8, §9)
- Wheel stops are kept only on the perimeter rows; the striping carries the rest
- The sandwich board, the hydrant, the scooter, the address plate and the wires
  all disappear

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not
a straitjacket — adjust after the first aerial and top review renders. All z
values are `authored height + dy(X, Y)` from the sampled terrain plane.

1. **Plate.** Triangulate the 2.3 polygon, subdivide to a ≤ 2 m grid so it can
   follow the terrain, drape every vertex, and give it a 0.30 m downward skirt so
   no gap can open against the baked landcover. Top face `Toy_stone`, skirt
   `Toy_ink`. Top face stands **0.12 m** above the sampled terrain, constant.
2. **Kerb.** A 0.18 m proud lip, 0.25 m wide, following the polygon on all
   frontage edges, `Toy_trim`. It gives the plate an edge from the aerial and a
   contact shadow.
3. **Concrete patch.** One 9 x 6 m panel in `Toy_trim`, inset 3 mm into the plate,
   centred near u +6, v −6. Optional but it is the one honest piece of texture.
4. **Striping**, `Toy_mustard`, 0.12 m wide, inset 4 mm proud of the plate.
   Bay module 2.65 m wide x 5.20 m deep. Five rows:

   | Row | Bays | Occupies | Cars head toward |
   |---|---|---|---|
   | **R** Ritch fence | 23 | u 13.07…18.27, v −23.5…+43.5 (two pitches given to the booth) | +u |
   | **M** spine, facing R | 11 | u 1.17…6.37, v −8.0…+21.0 | −u |
   | **C1** party line V7→V8 | 8 | v −13.79…−8.59, u −28.0…−6.0 | +v |
   | **C2** party line V9→V10 | 8 | v −34.19…−28.99, u −28.0…−6.5 | −v |
   | **Z** Zoe fence | 10 | u −28.51…−23.31, v −33.5…−10.5 minus the 7 m gate opening | −u |

   **60 stalls total**, which is the permitted number. The spine aisle is
   u 6.37…13.07 (6.70 m) running from the Brannan gate to the belly; the belly
   cross-aisle is v −28.99…−13.79 (15.20 m).
5. **Wheel stops**, `Toy_ink`, 1.70 x 0.16 x 0.12 m, at the head of every bay in
   rows R, C1, C2 and Z (49 of them). Row M has none — it is the aisle-facing row.
6. **Fence.** Posts `Toy_steel` 0.09 m square, 2.10 m tall, at 3.00 m pitch on
   every boundary edge; top rail 0.07 m; per-bay mesh slab 0.04 m thick, recessed
   0.03 m from the post faces, `Toy_steel` at a lighter value; a single
   `Toy_ink` barbed strand 0.15 m above the rail on the three street runs.
   Openings: a **6.5 m rolling gate** on Brannan centred at v +44.48, u ~10, its
   leaf parked open against the fence; a **7.0 m swing gate** on Zoe centred at
   u −28.51, v ~−13, one leaf standing at 30 deg into the lot.
7. **PUBLIC PARKING sign.** A 0.22 m square `Toy_steel` post from the plate to
   **6.80 m**; a 2.60 x 1.60 x 0.16 m board at 4.90–6.50 m: `Toy_red` field,
   `Toy_white` band across the upper third for the wordmark, `Toy_ink` header
   strip. Bevelled 0.06 m. Set it just inside the fence at u ≈ 17, v ≈ 43 (2.15).
   **This is the model's crest** and therefore sets `targetHeightM`.
8. **Attendant's booth** at (X 1.82, Y 19.29): 3.0 x 2.4 m, walls to 2.4 m,
   shallow shed roof to 2.9 m overhanging 0.25 m. `Toy_ink` roof (not `Toy_roofd`
   — it reads black in the app), `Toy_cream` walls, one `Toy_glass` window band
   facing the aisle with a `Toy_trim_Glow` shell behind it.
9. **Box trailer** at (X −2.96, Y 18.53): 6.0 x 2.5 x 2.9 m `Toy_white` box on a
   `Toy_ink` chassis, long axis along v. Chunky, no wheels-as-cylinders detail.
10. **Lot lights.** Three `Toy_steel` poles, 0.14 m, to 5.20 m, with a
    0.9 x 0.5 x 0.22 m head in `Toy_ink` and a `Toy_gold_Glow` underface. Place
    them along the Ritch fence and one in the belly; they are the night's
    supporting accent.
11. **Cars — 18.** Chunky three-box masses ~4.3 x 1.85 x 1.45 m (two of them
    pickups at 5.4 m, one van at 5.2 x 2.0 x 2.2 m), bevel 0.10 m, `Toy_glass`
    greenhouse, no wheels beyond a dark skirt. Distribute: 8 in Row R (with two
    gaps), 3 in Row M, 3 in C1, 2 in C2, 2 in Z. Colours: three `Toy_white`,
    three `Toy_ink`, three `Toy_steel`, two `Toy_navy`, two `Toy_stone`, and one
    each of `Toy_red`, `Toy_teal`, `Toy_mustard`, `Toy_coral`, `Toy_sky`. Match
    the silhouette family of `app/public/sf-assets/vehicles/` so the standing
    cars and the driving fleet look like one toy box.
12. **Greenery.** North-notch thicket at (X −23.14, Y 20.46): a 7 x 4 m cluster of
    three overlapping crowns, 2.6–4.0 m, `Toy_verdigris` and `Toy_teal` over
    `Toy_rust` trunks. Brannan-corner shrub at (X 33.10, Y −27.99): one 4.5 m
    crown at 3.8 m. Both sit inside the fence.
13. **Bevel** 0.12 m / 2 segments on the chunky solids (booth, trailer, sign
    board, cars); 0.04 m / 1 segment on posts, rails and wheel stops; **none** on
    the plate, the striping, the patch or the glow shells.

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_stone` | `#d9d2c2` | the paved plate — the asset's dominant surface |
| `Toy_trim` | `#f3efe6` | kerb lip, concrete patch panel |
| `Toy_mustard` | `#d9a441` | stall striping, aisle arrows |
| `Toy_ink` | `#3a3530` | plate skirt, wheel stops, barbed strand, booth roof, lamp heads, trailer chassis, dark cars |
| `Toy_steel` | `#9aa0a6` | fence posts, rails, mesh slabs, sign post, light poles, grey cars |
| `Toy_red` | `#c4453c` | the sign field |
| `Toy_white` | `#f7f4ec` | sign wordmark band, the box trailer, white cars |
| `Toy_cream` | `#f2ede3` | booth walls |
| `Toy_glass` | `#2a4d73` | booth window, car greenhouses |
| `Toy_navy` / `Toy_teal` / `Toy_coral` / `Toy_sky` | palette | car accents |
| `Toy_verdigris` / `Toy_teal` | `#9fb8a8` / `#3fa8a0` | foliage |
| `Toy_rust` | `#a86444` | trunks |
| `Toy_red_Glow` | `#c4453c` | **hero glow** — the sign field at night |
| `Toy_trim_Glow` | `#f3efe6` | the booth window |
| `Toy_gold_Glow` | `#caa64a` | the three lamp heads' underfaces |

**Night state (required).** A parking lot at night is three lit things in a dark
field, and that is exactly the restraint the style wants. Hero: the **PUBLIC
PARKING sign**, which is a lit box sign in reality. Supporting: the **booth
window** and the **three lamp heads**. Nothing else glows — not the stripes, not
the cars, not the fence.

Glow shells must be thin plates proud of the opaque surface, never the primary
surface itself: the app renders `_Glow` in a separate unlit layer at
`opacity = 0.12 + 0.95 * uNight`, and because the shells are authored as closed
solids a viewing ray crosses two faces, so the **day** opacity is
`1 − 0.88² ≈ 0.23`, not 0.12. A saturated shell over the whole sign board will
therefore tint it in daylight. Cover the wordmark band and the field separately,
keep the shell 0.02 m proud, and check the day render with the shells deleted if
the sign reads wrong. When you copy a `render_<slug>.py`, add
`bsdf.inputs["Emission Strength"].default_value = 0.0` to `fade_glow()` — the
inherited version only drops Alpha, which washes a hero shell out in the *day*
render.

### 2.9 Top surface

There is nothing here *but* the top surface, so the whole of §10 of the style
bible applies to the ground plane instead of a roof. The plan view must carry:
the stripe rhythm as the dominant graphic; the spine aisle as a clean, obviously
navigable channel from Brannan to Zoe; the fence as an unbroken outline with two
readable interruptions; the cars as colour punctuation, clustered rather than
evenly spread; the booth, the trailer and the sign as the only vertical events;
the two green masses anchoring the north and southeast corners. Keep the belly
deliberately emptier than the rows — the real lot is, and a uniformly busy lot
reads as noise.

### 2.10 Scope

**In the GLB:** plate, skirt, kerb, concrete patch, striping, wheel stops,
perimeter fence with barbed topping and both gates, PUBLIC PARKING pole sign,
attendant's booth, box trailer, three lot lights, ~18 parked cars, north-notch
thicket, Brannan-corner shrub.

**Not in the GLB:** Brannan / Ritch / Zoe roadways or sidewalks; the wooden
utility poles and overhead wires; the cobra-head streetlight; 426 and 434 Brannan
or any other neighbour; the mural on the party wall; the private 407 m2 lot in the
north notch (OSM way 1504713558); the fire hydrant; sandwich boards; street
trees; plinths, cameras or lights.

### 2.11 Triangle budget

Cap **18,000** — high for a site with no building on it, because the cost here is
in count rather than complexity. Suggested split:

| Element | Budget |
|---|---|
| Draped plate + skirt + kerb + patch | 2,000 |
| Striping (60 bays) | 1,500 |
| Wheel stops (49) | 1,400 |
| Fence: posts, rails, mesh slabs, barbed strand, two gates | 4,500 |
| Cars (18) | 5,000 |
| Booth, trailer, sign, three lights | 2,000 |
| Greenery | 1,400 |
| Headroom | 200 |

If it comes in tight, cut wheel stops before cars and cars before striping. The
striping is the asset.

### 2.12 Draft manifest entry

```json
{
  "id": "424-brannan",
  "file": "424-brannan.glb",
  "anchor": [
    -122.3954857,
    37.7798744
  ],
  "targetHeightM": <measured bbox height, expected ~8.6>,
  "cat": 23,
  "name": "424 Brannan Street Parking",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

`targetHeightM` is the **vertical extent of the draped model**, not an
architectural height — see 2.7 step 7 and the drape section of Part 1.
`dims` and `tris` are placeholders until the asset is built and validated.
`loadRadius`: the default formula gives `max(2500, 8.6 x 30) = 2500` m. Take the
default; the far stand-in for this asset is an empty lot, which is exactly what
it looks like anyway, so the absence past the radius is illegible.

### 2.13 Integration notes (for later, not this task)

- **New landmark (Case B)** — add a `pipeline/lib/landmarks.mjs` entry with the
  anchor, a camera preset, and the exclusion decision below.
- **The exclusion radius here defends the neighbours, not the asset.** Every
  other landmark in this family needs `exclude` to delete the procedural building
  standing where the GLB goes. This one has no procedural building: DataSF
  returns zero footprints on parcel 3776455, and a scan of the current baked
  tiles (`app/public/tiles/buildings/23_13.bin`, plus 22_13, 23_14, 24_13) finds
  **no footprint whose centroid falls inside the parcel** — only three neighbours
  whose rings clip the boundary by a metre or two. So the entire risk is
  *over*-excluding: any radius large enough to matter starts eating 426 Brannan,
  434 Brannan or the Zoe Street row.
- Therefore: **measure first, then almost certainly ship no `exclude` at all.**
  Run the vertex-and-centroid scan from `pipeline/data/buildings_datasf.geojson`
  **and** `buildings_overture.geojson` against the anchor (the two disagree, and
  the binding neighbour is often Overture's polygon). If the smallest neighbour
  distance is comfortably larger than zero — which is what the tile scan predicts —
  omit `exclude` entirely; `exclusionZones()` skips a falsy `exclude`, so the
  re-bake becomes a **no-op**, and that is the correct outcome. Prove it:
  `git diff --name-only` must show zero files under `app/public/tiles/` and
  `api/_data/` after the bake.
- **If the bake really is a no-op, say so loudly in the report.** A Case B
  landmark that changes no tiles is unusual enough that a reviewer will assume
  the bake was skipped. Show the scan table and the empty diff.
- `pipeline/data/` is free: `cp -Rc <sibling-worktree>/pipeline/data/. pipeline/data/`
  is an APFS clone, ~700 MB in well under a second.
- **Batch mode applies** — this asset is being built alongside the rest of the
  Brannan and South Park families. Stage 5 ends at a source-only branch.
- The landcover under this parcel should be checked once in the running app: if
  the bake draws a `paved` or `grass` polygon over the lot it will z-fight the
  plate. Nothing was found in the current tiles, but 0.12 m of plate clearance is
  the margin, so look.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] **`min_z` is negative and that is asserted, not tolerated** — with the plate-
      above-terrain spread reported (target < 0.02 m over the whole plate)
- [ ] Terrain-plane residual reported by `sample_terrain.mjs` (expected ~0.10 m)
- [ ] `targetHeightM` equals the measured bbox height to 1 mm; loader scale 1.0000
- [ ] XY center offset within ~1 m; XY bbox ~89 x 60 m (expected at a 45 deg heading)
- [ ] Triangles at or under 18,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the sign field, the booth window and the three lamp heads;
      shells proud of the opaque surfaces; day render checked for glow tinting
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (per-object signed
      volume for the union of solids; ray test residual ≤ 0.15%)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + contact sheet + night render + the grazing render,
      all regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json`, `sample_terrain.mjs` committed

### 2.15 Open questions and risks

- **The brief said "building".** It is not one, and no source consulted suggests
  it ever was: zero DataSF footprints, assessor class V, improvements assessed at
  $0, and a live commercial-parking-lot permit. The asset is the lot. If a future
  reviewer expects a building here, the answer is 2.1, not a remodel.
- **The site is entitled and could be built at any time.** SOM's 288 Ritch / 55 Zoe
  scheme has design development behind it; the two DBI permits are filed but never
  issued. Re-check permit status before modelling, and expect this asset to have a
  shorter shelf life than its neighbours.
- **The sign's height is *inferred*.** 6.80 m comes from comparing the board
  against the second-floor window heads of the blue building across Ritch in
  panorama `TUpIDbEopCNF5mypbXJ5aA`, not from a rectified measurement. It is worth
  ±0.5 m, and because it sets `targetHeightM` the executing agent should rectify it
  properly (equirect tiles are levelled; elevation angle = `(H/2 − y)/H x 180 deg`)
  and record the result. Getting it wrong makes the sign wrong, not the lot: the
  loader scale still lands on 1.0 because `targetHeightM` is taken from the
  measured bbox either way.
- **The sign is pulled ~2 m inside the fence.** The real pole stands at the kerb,
  in the public right of way, which this asset does not own. Moving it inside the
  boundary is an authoring decision made so the GLB contains no ROW geometry; it
  is recorded here and must be repeated in `REPORT.md`.
- **The row layout is a reconstruction.** The 60-stall count is measured (SFPD
  permit and the Colliers offering agree), the row *positions* and the aisle are
  read off z21 nadir imagery, and the per-row bay allocation in 2.7 is chosen to
  total exactly 60. Treat the bay counts as *inferred*; the row structure and the
  aisle are *observed*.
- **The surface colour will be argued about.** Every reference reads pale warm
  grey — worn concrete and old asphalt, not new blacktop — and §13 of the style
  bible reaches for "clean charcoal asphalt". Follow the references: the paleness
  is what makes the void read from the air, and the city's darker streets around
  it do the contrast work.
- **The north notch is not ours.** OSM way 1504713558 is a separate 407 m2
  `access=private` lot filling the re-entrant between V10, V0 and V1. It is
  visually continuous with this lot on the ground and must still be left out —
  the parcel boundary is the asset boundary.
- **No exclusion may be the right answer.** See 2.13. That is unusual for a Case B
  landmark and needs to be argued from a measurement, not assumed.
