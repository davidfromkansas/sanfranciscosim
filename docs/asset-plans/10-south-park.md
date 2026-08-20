# 10 South Park (South Park Lofts) — SF-SIM asset plan

A 1993 live/work loft condominium by **Ramon Zambrano** on the north-east arc of the
South Park oval, wedged between the sage-green Hotel Madrid at 22–24 South Park and
the Kohler warehouse at 2 South Park. It is the newest building on the oval's north
rim by half a century and the only one on this block that is not one building but
**two**: a front block on South Park and a rear block on Taber Place, with a
landscaped courtyard and a pond between them, all on one 585 m² through-lot.

Where every neighbour is a flat-fronted Victorian, Edwardian or brick warehouse in a
row, 10 South Park is **apricot stucco with a bowed front** — the developer called it
"Contemporary Mediterranean", the broker who sold the lofts called the stucco
"reminiscent of the South West" — carrying two stacked 16-foot loft tiers, each read
from the street as a **wide window band with an elongated oval mullion inscribed
across it**, an arched wood French door on a wrought-iron juliet balcony, and a deep
recessed loggia. From the app's aerial camera it is the one plan on the oval's north
rim that is a **pentagon with a hole in the middle**.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/10-south-park/`. This document is the plan only: Part 1 is the runnable
task prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `10-south-park` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry with THREE exclusion zones and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3934999, 37.7823712` |
| Target height | **14.67 m** to the roof bulkhead (parapet crest 13.10 m, roof deck 12.27 m) — LiDAR maximum, corroborated photogrammetrically, see 2.1 |
| Footprint | 14.2 m wide × 42.3 m deep lot; front block 262 m², rear block 181 m², courtyard ≈ 142 m²; measured |
| Triangle cap | 12,000 |
| Category | `2` (apartments) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 10 South Park GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of 10 South Park in San Francisco (the South Park
Lofts, 1993, Ramon Zambrano) and deliver it as a downloadable, validated GLB.

Do not integrate or deploy the model yet. Create the asset, validate it, render review
images, and commit the deliverables to your working branch.

## Read the project sources first

Before any research or modeling, read in this order:

1. `AGENTS.md`
2. `docs/styles/README.md`
3. `docs/styles/miniature-toy.md`
4. `.agents/skills/sf-miniature-style/SKILL.md`
5. `.agents/skills/sf-asset-check/SKILL.md`
6. `app/public/sf-assets/landmarks_manifest.json`
7. `artifacts/132-south-park/` — **the reference implementation for the hard part.**
   It is the other South Park lot in this set that carries TWO baked footprints with
   an open courtyard between them, and its build script, its anchor-in-the-courtyard
   convention and its three-zone exclusion are the pattern to copy.
8. `artifacts/22-south-park/` — the immediate south-west neighbour, sharing the
   36.28 m party wall. Its REFERENCE.md §4 already records this building from the
   outside ("10 South Park … is 11.88–12.27 m"), its §2 works the same oval-arc
   frontage geometry, and its build script shows the 45°-rotated authoring frame
   every building on this block needs.
9. `artifacts/2-south-park/` — the immediate north-east neighbour, 17.72 m, four
   metres taller than us; its flank is what our north-east party wall stands against.
10. `docs/asset-plans/10-south-park.md` — this plan, whose dossier is your research
    starting point, not a substitute for your own verification. **Read §2.15 before
    you start.**

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract, `AGENTS.md`
governs repository and integration rules. Do not invent a new style and do not copy
visual instructions from unrelated prompts.

## Must capture

- **Two buildings and the courtyard between them, as one asset.** A front block
  20.7 m deep on South Park, a rear block 15.6 m deep on Taber Place, and a ~10 m
  courtyard between them. The courtyard is open to the sky and the app's camera looks
  down: it is a designed surface, not a hole. Give it paving, a planting bed, a
  specimen tree and the pond.
- **The bowed frontage.** The lot sits where the oval turns its east end: the
  frontage is 8.13 m of straight wall facing south-east, then a ~30° break, then
  8.6 m of shallow arc facing very nearly due south. 44.5° of total turn across
  16.7 m of frontage. If the front is one flat plane the model is wrong.
- **Two stacked 16-foot loft tiers, each read as one composition.** Per tier, from
  south-west to north-east: a **wide window band with a long flattened oval inscribed
  across its small-pane grid**, a **round-arched wood French door** with a wrought-iron
  juliet balcony and a projecting metal grate under it, and a **deep recessed loggia**
  behind a plain iron railing. The tier repeats identically twice. This rhythm is the
  building.
- **The oval window motif.** A single elongated ellipse with a curled tail drawn in
  heavy mullion across the middle of each wide window band, inside a pale flat
  surround. It is the one ornament on the building, it appears nowhere else on the
  oval, and it is recognition cue #1. Do not lose it to simplification.
- **The garage level.** A wide flush apricot garage door with three shallow horizontal
  reveals, and beside it a recessed pedestrian entry with a dark door and a planted
  slot. Ground floor is 3.3 m; the composition above starts at the first balcony deck.
- **The flat roof and its bulkhead.** A plain parapet 0.83 m above a pale membrane
  deck, no cornice; a low stair bulkhead ~5.7 × 2.4 m at the rear edge of the front
  block's roof (the tallest thing in the model at 14.67 m); mechanical units and a
  dark skylight/PV panel clustered along the north-east parapet.
- **Taber Place is a real elevation, not a service back.** Same apricot stucco, same
  dark-framed multi-pane windows in pairs, a dark door behind an iron security gate at
  one end and a second garage at the other, with a "10 SOUTH PARK" plaque beside it.
- **Both party walls are blind.** 22–24 South Park (south-west, 14.22 m) and 2 South
  Park (north-east, 17.72 m) are both TALLER than this building, so neither flank is
  seen from the aerial camera. Do not spend geometry on them.

## Research 10 South Park independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the two footprints, the WGS84 anchor and the real-world
orientation, and gather references covering:

- The South Park (south-east) elevation and the Taber Place (north-west) elevation —
  both are visible in the app and both must be right.
- **The roof of both blocks and the courtyard, from above.** §2.9 is read off Google
  z21 satellite imagery that leans several metres in this block, and is the least
  certain part of this plan. Nothing here is measured to better than a metre.
- **Whether the frontage breaks or rounds.** The surveyed parcel resolves the front
  line as a straight 8.13 m segment, a ~30° corner, then a 14°-sweep arc of R ≈ 35 m.
  Street-level photography reads it as a continuous bow. Decide, and say which.
- **The current colour.** §2.8's apricot is sampled off a January 2025 Street View
  capture under mixed light and is the weakest number in this dossier. The stucco was
  stripped and replaced across the whole South Park elevation under permit
  201211274894 (2012–13), so the current coat is at most fourteen years old. The
  *relations* (warm mid-tone body, pale window surrounds, near-black glazing bars,
  dark iron, natural wood doors) are far safer than the values.
- **Whether the rear block's roof is tiled.** The aerial shows a terracotta-coloured
  surface over the rear block and two tan hipped shapes near the courtyard, which
  would fit "Contemporary Mediterranean" — but at 2 cm/px and several metres of
  building lean, it could equally be a paver terrace. §2.15 risk 3.

Prefer architect/engineer publications, owner or institutional material, planning and
permitting documents, architectural press, geolocated photography, and aerial/satellite
imagery. Never rely on a single photograph, a single AI-generated image, or a single
unsourced 3D model. Separate verified facts from visual inference; if sources disagree,
document the disagreement and decide.

**One trap is already known and is signposted here so you do not fall into it:**
**no OSM building carries this address.** Nominatim resolves "10 South Park" by TIGER
interpolation onto the South Park *roadway* (way 8916551) and returns
`osm_type: way`, which looks exactly like a building hit. This is the 350 Brannan
Street failure mode, and this lot is worse than 350 Brannan because the resolution
also has to survive a **condominium**: the address exists ten times over, on lots
3775/106 through 3775/115, all sharing one parcel polygon. The route that works is
address → DataSF address table (`ramy-di5m`) → any of those APNs → parcel
(`acdm-wktn`, blklot 3775106) → the two DataSF footprints inside it. Do not geocode
this building spatially and do not trust an OSM ring here.

## Create a reference dossier

Write `artifacts/10-south-park/REFERENCE.md` containing: source links and what each
establishes; verified dimensions and location; orientation; observations from all four
sides and above; the 3–5 strongest recognition cues; features to preserve; features to
simplify; uncertainties and conflicting evidence. A contact sheet of attributed
reference thumbnails is welcome if legally permissible — do not commit copyrighted
full-resolution imagery.

## Make your own design decisions

Follow the conversion process in `docs/styles/miniature-toy.md` §22: identify the
recognition cues, strip nonessential information, rebuild the massing from a few
confident volumes, exaggerate only the signature features, simplify the facade into
broad rhythms, deliberately design every surface visible from above, evaluate from the
app's high three-quarter aerial camera, then simplify again.

This is a **secondary building** in the style bible's detail budget (§21), and the
budget is spent on three things and nothing else: the oval window motif, the loggia
recesses that give the front real depth, and the courtyard.

Note the specific style risk here: the failure mode is a **pair of blank apricot
boxes**. Two simple flat-roofed blocks in one colour with no cornice, no bay and no
ornament is what this building becomes if you model it literally and stop. The
discipline is the opposite of 49 South Park's: there, seven bays had to be restrained;
here, three or four moves have to be *pushed* — deepen the loggias so they read as
shadow from above, keep the window surrounds wide and pale so the bands read as bands,
and make the courtyard green enough to be legible as an opening in the block rather
than a gap in the geometry.

The finished asset must be immediately recognizable as 10 South Park, consistent with
the real building from all four sides and above, architecturally credible, and a
premium handcrafted miniature — not photorealistic, not voxel art, not generic
low-poly, and never accurate in one view while invented in the others.

## Scope of the exported asset

Export both structures on parcel 3775/106-115 and the courtyard between them: the
front block with its garage level, two loft tiers, parapet and roof bulkhead; the rear
block with its Taber Place elevation and roof; and the courtyard's paving, planting
bed, tree and pond.

Do not include any surrounding city geometry: South Park (the oval, its lawn, paths or
elms), South Park Street, Taber Place, 22–24 South Park, 2 South Park, street trees —
including the large magnolia standing directly in front of the north-east end, which
hides part of this facade in every street-level photograph and must not be modelled —
the sidewalk, parked cars, people, plinths, cameras or lights. Temporary context may
appear in review renders but must not leak into the GLB.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary `.glb`;
real-world meters; origin at base center; minimum geometry Z ~ 0; applied transforms;
no negative scales; outward normals; no duplicate or foreign geometry; no image
textures; no transparency; flat-color materials named `Toy_*` from the project
palette; `_Glow` suffix only on surfaces that glow at night; no `Toy_body`; no
cameras, lights, animations, armatures or constraints; no external dependencies; at
most 12,000 triangles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model
drops into the city at its real-world heading — the loader applies no rotation
(`placeGeneric` in `app/src/assets.js` only scales and positions). The two party walls
run **45.2° / 225.2°**; the Taber Place rear faces **315.2° north-west**; the
straight north-east third of the South Park frontage faces **135.2° south-east**; the
bowed south-west two-thirds faces **179.7°, very nearly due south**. The building is
rotated ~45° off the world axes, so build directly on the measured lot geometry in 2.3
rather than modelling an axis-aligned box and rotating it
(`artifacts/22-south-park/build_22_south_park.py` does exactly this on the same block
and is the pattern to copy). This is the case the plans README calls out: the
contract's "front faces −Y" rule cannot be honoured literally here, real-world
orientation wins, and the deviation must be recorded in `REPORT.md` with the measured
heading.

**Height normalization:** the tallest geometry in the export — the crest of the roof
bulkhead — must land at exactly the height you verify (this plan's figure is
**14.67 m**, with the parapet crest at 13.10 m and the roof deck at 12.27 m) so the
loader's `targetHeightM / measuredHeight` scale is 1.0. If your research moves the
height, move the model and the draft manifest entry together and say so in `REPORT.md`.

## Reproducible Blender workflow

Blender 5.2 LTS. Headless: `blender -b --python script.py -- args`.

Keep `artifacts/10-south-park/build_10_south_park.py` (deterministic build script),
`artifacts/10-south-park/10-south-park.blend`, and
`artifacts/10-south-park/10-south-park.glb`. The script must rebuild the model reliably
enough for future revision. Do not modify or rename an unrelated existing GLB to
satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras: `10-south-park-top.png`,
`10-south-park-north.png`, `10-south-park-east.png`, `10-south-park-south.png`,
`10-south-park-west.png`, plus `10-south-park-contact-sheet.png`, at least one high
three-quarter aerial beauty render `10-south-park-aerial.png` taken over the
**south-south-east** so both front planes and the courtyard beyond the front block are
in frame, and a night render `10-south-park-aerial-night.png`.

The four elevations must share scale, framing, lighting, exposure and projection; use
orthographic or long-lens cameras; label directions from the researched orientation;
the top view must clearly show both roofs, the bulkhead, the parapet ring and the
whole courtyard; the aerial view uses the style bible's camera assumptions (30–50
degrees down, long lens). Simple tabletop lighting, neutral warm background, minimal
depth of field, and every image must depict the same exported model.

For the night render, drive the `_Glow` materials from Base Color (copy `Base Color`
into `Emission Color`, strength 1.0) — see the note at the end of
`docs/asset-plans/README.md`. A re-imported GLB's `_Glow` materials otherwise render as
white slabs.

## Validate the exported GLB

Re-import `10-south-park.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture count,
camera count, light count, animation count, applied-transform status, negative-scale
status, normal-orientation status, unexpected geometry, and per-material contract
compliance. Render at least one review image from the re-imported asset. Write
`artifacts/10-south-park/validation.json` and `artifacts/10-south-park/REPORT.md`.

Note that the axis-aligned XY bounding box will be roughly **40 × 36 m** even though
the lot is 14.2 × 42.3 m — that is the expected consequence of a ~45° real-world
heading, not a scale error. Note also that the model is **two disjoint solids plus a
ground plane**, so the union-of-solids normals rule applies: use the per-object signed
volume test as authoritative, with the ray test as the cross-check.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this draft
entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "10-south-park",
  "file": "10-south-park.glb",
  "anchor": [
    -122.3934999,
    37.7823712
  ],
  "targetHeightM": 14.67,
  "cat": 2,
  "name": "10 South Park (South Park Lofts)",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`,
or any app code in this task. Integration is a separate, explicitly requested job — run
`docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes
in `docs/asset-plans/10-south-park.md`.
````

---

## Part 2 — Research and design dossier

Compiled 18 August 2026 from the sources in 2.2. Values marked *inferred* or
*estimated* are visual or derived, not published figures — the executing agent must
re-verify anything it relies on.

This dossier is unusually strong on documents and unusually weak on pictures. The
building's construction, ownership, unit count, floor areas, architect and every
dimension of its lot are on the public record; but it is an ordinary 1993 condominium
that no architectural publication has ever photographed, no historic survey has ever
described, and Google's aerial imagery leans several metres across this block. Every
number in 2.1 is measured or cited. Everything in 2.9 (the roof) is inference from one
oblique satellite image, and it says so.

### 2.1 Verified facts

| Fact | Value | Source / confidence |
|---|---|---|
| Address | 10 South Park (also written 10 South Park Avenue and 10 S Park St), San Francisco CA 94107 | DataSF `ramy-di5m`; Google Street View labels the pano in front of it "10 S Park St" |
| Marketing name | **South Park Lofts** | bayareamodern.com, somapro.com. Note the collision: `188-south-park` in this manifest is also sold as "South Park Lofts". The manifest name below disambiguates by address. |
| Block / lot | 3775 / **106–115** — ten condominium lots sharing one parcel | DataSF `acdm-wktn`; condo map recorded 1 July 1998 |
| Parcel | **585 m²**, a trapezoid 14.2 m wide, 42.34 m deep on the north-east boundary and 36.28 m on the south-west | measured from `acdm-wktn` blklot 3775106, reprojected |
| Built | **March 1993**; permit 9123974 filed 19 Dec 1991 for "erect a three story ten unit reisdential bldg" [sic], status complete | DataSF permits `i98e-djp9`; somapro.com gives the March 1993 completion; assessor `year_property_built` = 1993 on nine of ten units |
| Architect | **Ramon Zambrano** | somapro.com SOMA loft database — a single source, see 2.15 risk 5 |
| Use | 10 live/work loft condominiums, assessor class **LZ**; 930–1,196 ft² per unit (assessor `property_area`: 929, 931, 1065 ×5, 1069, 1145, 1196) | DataSF assessor `wv5m-vpq2`, 2024 roll |
| Unit type | two-level lofts, **16-foot ceilings**, deeded garage parking and storage for every unit | somapro.com; corroborated by listing copy ("2-level loft", "soaring ceilings", "French doors to shared courtyard") |
| Form | **two separate buildings around a central courtyard** with a pond | bayareamodern.com; somapro.com; confirmed by the two DataSF footprints and by aerial imagery |
| Front block footprint | **262 m²**, 20.67 m deep, full lot width | DataSF `ynuv-fyni` id 201006.0015438, measured |
| Rear block footprint | **181 m²**, 15.65 m deep, full lot width with a 2.9 × 4.3 m wing reaching forward on the north-east | DataSF `ynuv-fyni` id 201006.0030231, measured |
| Courtyard | ≈ **142 m²**, ~10 m deep across the full 14.2 m width | derived: parcel less both footprints |
| Roof deck | **12.27 m** front block (LiDAR median = LiDAR mode, 1,044 cells, σ 0.78 m); **11.88 m** rear block | DataSF `ynuv-fyni` `hgt_median_m` |
| Parapet crest | **13.10 m** ± 0.15 | photogrammetric, see below — *estimated* |
| Roof bulkhead crest | **14.67 m** front block; 14.27 m rear block | DataSF `hgt_maxcm`, corroborated by a hard-edged rectangular structure visible in aerial imagery |
| **Target height** | **14.67 m** | the crest of the tallest modelled geometry |
| Storey heights | garage 0 → 3.30 m; loft tier 1 → 8.20 m; loft tier 2 → 13.10 m | *estimated*, see the arithmetic below |
| Party walls | 36.28 m shared with 22–24 South Park (SW); 42.34 m shared with 2 South Park (NE); both neighbours taller (14.22 m and 17.72 m) | parcel geometry + `artifacts/22-south-park/REFERENCE.md` §2 |

**Why 14.67 m and not 13.10 m.** The DataSF LiDAR maximum sits 2.40 m above its own
median on a 1,044-cell footprint whose standard deviation is 0.78 m — 3.1σ, which is
exactly the band where 592 Third Street's street-tree artifact lived and where 22–24
South Park's parapet was believed. Three things settle it for the maximum here:

1. The overhanging-tree trap is ruled out by *position*. The only large tree touching
   this building is the magnolia on the sidewalk at the **north-east front corner**;
   the LiDAR maximum cannot be reached from there without also lifting the front
   parapet cells, and the median is undisturbed.
2. The party-wall trap that killed 26–28 South Park's maximum is ruled out by
   *direction*. Both neighbours are taller than this building, so a cell bleeding
   across a party wall would pull the maximum toward 14.22 m or 17.72 m from the
   outside — but the same 2.4 m step appears on the **rear** block too (14.27 over
   11.88), and the rear block's own party-wall neighbours are different buildings.
   Two independent footprints reporting the same 2.4 m step is a building feature,
   not an edge artifact.
3. Google z21 imagery shows a hard-edged rectangular structure roughly **5.7 × 2.4 m**
   sitting at the rear edge of the front block's roof, casting its own shadow — a
   stair bulkhead, which is what a 2.4 m step over a 12.27 m deck is.

**The photogrammetric parapet.** Measured from Street View pano
`aFRDCNG9w0lcHJ9ngJI8LQ` (Jan 2025, labelled "10 S Park St"), stitched to a
4096 × 2048 equirectangular, sky/stucco edge detected per column, elevation converted
with `h = h_cam + D·tan(θ)` at `h_cam` = 2.5 m and `D` solved by intersecting each
bearing with the measured footprint polyline:

| bearing | 314° | 320° | 326° | 332° | 338° | 344° | 350° | 354° |
|---|---|---|---|---|---|---|---|---|
| D (m) | 10.48 | 9.53 | 8.83 | 8.32 | 7.94 | 7.67 | 7.50 | 7.44 |
| derived crest (m) | 13.14 | 13.08 | 13.10 | 13.09 | 13.10 | 13.04 | 13.05 | 13.03 |

The derived crest is flat to **±0.06 m while the distance varies by 41 %**, which is
the strongest possible confirmation that both the calibration and the footprint
polyline are right (a wrong `D` drifts systematically; a wrong `h_cam` shifts the whole
column but stays flat). 13.10 m sits **0.83 m above the LiDAR roof deck** — an ordinary
parapet — and 1.57 m below the bulkhead crest. Camera height is the only unshared
error term and is worth ±0.15 m.

**The storey arithmetic, and why it is a confirmation rather than a guess.** The
garage-door head measures 2.3 m and the first balcony deck 3.3 m. Subtracting that
ground floor from the 13.10 m parapet leaves **9.80 m for the two loft tiers, i.e.
4.90 m each — 16.07 feet.** The broker's "16 foot ceilings" and the 1991 permit's
"three story" (garage story plus two loft stories) and the photographed facade (four
window bands above the garage, alternating French-door-and-balcony with wide window
band, exactly two of each) all land on the same number from three independent
directions.

### 2.2 Sources

**Survey and public record (all measured or quoted, not inferred):**

- **DataSF building footprints** `ynuv-fyni` — the bake's own primary input.
  `201006.0015438` (front, 262 m², `hgt_median_m` 12.27, `hgt_maxcm` 1467,
  `hgt_mincm` 1014, `hgt_stdcm` 78.4, 1,044 cells) and `201006.0030231` (rear,
  181 m², median 11.88, max 1427, min 849, σ 79.6, 717 cells). Ground elevations
  differ: `gnd_meancm` 1424.6 front, 1472.1 rear, so the site rises **0.47 m** from
  South Park to Taber Place and the two roof planes are level in absolute terms
  (26.52 m vs 26.60 m NAVD88-ish).
- **DataSF parcels** `acdm-wktn`, blklot 3775106 (and 107–115, identical geometry) —
  585 m², 20 vertices, the surveyed lot lines including the 15-vertex densified front
  arc. This is the authority for the frontage curve; the LiDAR outline approximates it
  with two chords.
- **DataSF addresses** `ramy-di5m` — ten records, `10 SOUTH PARK #1` … `#10`, parcels
  3775106–3775115, all at the same point.
- **DataSF assessor** `wv5m-vpq2`, 2024 closed roll — class LZ, 1993, unit areas.
- **DataSF permits** `i98e-djp9`, 48 records on these lots. The ones that matter:
  **9123974** (filed 19 Dec 1991, complete) "erect a three story ten unit reisdential
  bldg"; **9711232** (1997, complete) "repair seismic resisting elements. remove
  /replace stucco"; **201211274894** (filed 27 Nov 2012, complete) "remove (e) stucco
  to correct waterproofing @ windows entire facade, replace stucco in kind @ entire
  facade @ south park st elevation w/ expansion joints"; **201108263429** and
  **201210182300** (2011, 2012) reroofing; **202109279232** (2021) fire-alarm
  replacement "garage, 1/f & 2/f" — three levels named, matching the permit's
  "three story". No permit after 2012 touches the exterior; the 2025 unit-9 bathroom
  permit explicitly says "no exterior work".
- **`artifacts/22-south-park/REFERENCE.md`** — the neighbour's dossier, which measures
  the shared party wall at **36.28 m at 45.19°**, records this building's height from
  the outside as "11.88–12.27 m", and works the same oval-arc frontage problem one lot
  to the south-west (there the oval turns 31° across 15.14 m of frontage).

**Published description (secondary, single-source in places):**

- `http://www.somapro.com/db/loft.html` — the SOMA loft database entry: *"The South
  Park lofts have a stucco exterior reminiscent of the South West, although the
  developer has dubbed them Contemporary Mediterranean. This is a ground up … project
  … The architecture for the project was done by Ramon Zambrano. The lofts feature 16
  foot ceilings, park, courtyard and City Views, deeded parking and storage for each
  unit. The building was built in March of 1993 with square footage running from 930
  square feet to 1195 square feet."* Establishes: architect, completion month, ceiling
  height, unit range, the developer's own style label.
- `http://www.somapro.com/San%20Francisco%20Lofts%20South%20Park.html` — establishes
  the **pond**: "Mediterranean style architecture built around a Pond and recently
  restored landscaped courtyard".
- `https://www.bayareamodern.com/lofts/south-park-lofts/` — establishes the two-building
  courtyard plan, 1993, 10 units, 930–1,195 ft², "stucco-finished Mediterranean
  exterior", "most units have small patios or French balconies".
- Listing copy (Vanguard, Compass, KW, BHHS, cchp.com, 2024–25) — establishes, in
  aggregate: "boutique courtyard building", two-level lofts, "wall of windows",
  "French doors to a shared courtyard", skylights, wood-burning fireplaces, radiant
  floors, one garage space per unit. Label these *observed (listing photo)*.
- `socketsite.com`, Oct 2009 and Jun 2007 — unit sales, and a reader confirming "Garden
  is shared with the other units in the building. It opens up into the courtyard".

**Imagery (all keyless, all re-fetchable):**

- Google Street View pano **`aFRDCNG9w0lcHJ9ngJI8LQ`** — © 2025, standing 5 m off the
  frontage, labelled "10 S Park St" by Google's own metadata. Camera at
  37.78215707, −122.39335946, pano heading 290.854°. **The equirectangular's column 0
  corresponds to bearing (heading − 180) = 110.854°**, verified against the surveyed
  party-wall corner. This is the single most useful image of the building.
- Google Street View pano **`q6hwZn8Ks9tq4nSLfTZuDw`** — © 2025, Taber Place, 5.8 m off
  the rear elevation; heading 45.309°. Wall-filling; use `8nlV6lfftmnNN_DPOQEuTw`
  (19 m out) or `R-iQLstrsGsxKlyH8o_PMQ` ("20 Taber Pl") for context.
- Tile recipe (needs both a browser UA **and** a `https://www.google.com/` referer or
  it 403s):
  `https://streetviewpixels-pa.googleapis.com/v1/tile?cb_client=maps_sv.tactile&panoid=<ID>&x=<0-7>&y=<0-3>&zoom=3&nbt=1&fover=2`
  for the 4096 × 2048 equirect, and
  `.../v1/thumbnail?cb_client=maps_sv.tactile&w=1600&h=1100&pitch=<-up/+down>&panoid=<ID>&yaw=<true bearing>`
  for a rectilinear view.
- **Google satellite z21** (`https://mt1.google.com/vt/lyrs=s&x=&y=&z=21`, 0.059 m/px)
  — the only aerial that resolves the courtyard. Bing z20 and Esri z20 were both
  fetched and both lean worse. **All three lean**: this block is imaged well off nadir
  and 2 South Park's 17.7 m roof overhangs our parcel line in every one of them. See
  2.15 risk 3.
- **OSM: nothing.** No way in the vicinity carries `addr:housenumber=10` +
  `addr:street=South Park`. Way 112926341 (untagged, `height=12`, 10 nodes,
  centroid −122.3934695, 37.7823194) is almost certainly this building's front block
  as traced by Bing, and Overture carries it as `…79f82d14b81c` (251 m²) plus a rear
  ring `…e716f25d7e5b` (150 m²). Neither is addressed; do not resolve through them.

### 2.3 Orientation and placement

The whole block is on SoMa's 45° grid. Working in a lot-local frame with **+u = 44.8°
north-east** (along the party walls, positive toward 2 South Park) and **+v = 134.8°
south-east** (positive toward the park), origin at the parcel centroid
(−122.393446, 37.782262):

| lot edge | length | faces (outward normal) | elevation |
|---|---|---|---|
| South Park front, north-east third | **8.13 m** | **135.2° SE** | hero, straight |
| South Park front, south-west two-thirds | **8.64 m of arc**, chord 8.62 m, R ≈ 35.3 m, sweep 14.1° | chord normal **179.7°, due south** | hero, bowed |
| south-west boundary | **36.28 m** | 225.2° | party wall with 22–24 South Park, blind |
| Taber Place rear | **14.29 m** | 315.2° NW | secondary but finished |
| north-east boundary | **42.34 m** (21.43 + 20.91) | 45.2° | party wall with 2 South Park, blind |

The two front segments meet at a **~30° corner** at u +1.56, v +9.77; adding the arc's
own 14.1° sweep gives **44.5° of total turn across the 16.77 m frontage**. That is the
oval turning its eastern end, and it is why the north-east boundary is 6.06 m longer
than the south-west one — the same asymmetry 22–24 South Park records (6.15 m) one lot
along. A single circle fitted through all sixteen surveyed front vertices does **not**
close (residuals to 0.67 m, nonsense radius), so the break is real and the survey is
not describing one smooth curve.

Built extents inside that lot, measured from the DataSF footprints:

- **front block** v +8.53 → −12.14 (20.67 m deep), u −4.32 → +10.58 (full width)
- **courtyard** v −12.14 → −22.12 (9.98 m), full width, less the wing below
- **rear block** v −22.12 → −33.34 (11.22 m) full width, **plus** a wing on the
  north-east, u +7.48 → +10.52, reaching forward to v −17.69

The LiDAR front edge sits 1.2–1.3 m behind the surveyed front property line. That is
LiDAR erosion plus a possible balcony overhang, not a setback: build the front wall on
the **parcel** line and treat the LiDAR outline as the depth authority only. (This is
the 165–167 South Park rule: on dense narrow SoMa lots prefer the parcel layer.)

**Anchor.** `−122.3934999, 37.7823712` — the centre of the parcel's **world-axis**
bounding box (39.97 m east–west × 35.81 m north–south), which is where the GLB's
base-centre origin has to land. In lot coordinates that is u +4.21, v −12.89: inside
the front block's rear wall by a whisker, i.e. essentially on the courtyard edge. It is
**not** the centre of the lot in lot coordinates (u +2.7) — the 45° heading moves it.
Do not substitute the address point (−122.393411, 37.782262), which is the Assessor's
condo point and sits 4.4 m away.

### 2.4 What each side shows

**South-east (South Park) — observed, Street View Jan 2025, the hero elevation.**
Apricot stucco, four levels, no cornice, flat parapet with a thin pale cap. Reading up
from the sidewalk:

- **Garage level, 0 → 3.30 m.** A wide flush garage door with three shallow horizontal
  reveals, painted the body colour so it disappears into the wall; to its south-west a
  **recessed pedestrian entry** — a dark door at the back of a shadowed slot with
  planting spilling out of it. At the south-west end, one square window.
- **Loft tier 1, 3.30 → 8.20 m**, and **loft tier 2, 8.20 → 13.10 m** — the same
  composition twice, which is the building's whole rhythm:
  - a **wide window band** (roughly 6 m long, 2 m tall) set in a **broad flat pale
    surround**, glazed as a grid of small panes in near-black bars, with a **long
    flattened oval drawn across the middle of the grid in heavy mullion**, its
    south-west end curling into a small circle;
  - beside it, one bay south-west, a **tall round-arched French door** in **natural
    stained wood**, opening onto a **wrought-iron juliet balcony** with a projecting
    perforated metal grate beneath it;
  - and to the north-east a **deep recessed loggia**, two bays wide, behind a plain
    dark iron railing, with a solid stucco return at its far end;
  - plus, at the south-west end against the party wall, one plain square window per
    tier in a pale surround.
- **Parapet, 13.10 m.** Plain, no ornament. The wall simply stops.

The north-east end of the front — the last ~4 m before 2 South Park — steps back and
its parapet reads roughly a metre lower; that part is behind a large sidewalk magnolia
in every available capture and is the least certain part of this elevation. See 2.15
risk 2.

**North-west (Taber Place) — observed, Street View Jan 2025.** A finished elevation,
not a service back. Same apricot stucco. Dark-framed multi-pane windows in **pairs**,
some with internal blinds, arranged in two upper bands over a solid base. At the
south-west end a **dark door behind an ornate iron security gate**; at the north-east
end a **garage opening**, with a small **"10 SOUTH PARK" plaque** on the wall beside
it. Wall-mounted flood and security lights, a camera, and a shallow vertical
expansion-joint line running the height of the wall.

**North-east and south-west — party walls, blind.** 22–24 South Park to the south-west
is 14.22 m and 2 South Park to the north-east is 17.72 m. **Both neighbours are
taller**, so unlike 22–24 (whose own flank stands 4 m proud of its neighbour) neither
of this building's flanks is ever seen. Model them as flat stucco and spend nothing.

**Courtyard — inferred from aerial and from listing copy.** Roughly 10 × 14 m, open to
the sky, enclosed on all four sides. Paved, with planting beds along both party walls,
at least one **specimen tree with purple-bronze foliage** (a plum or Japanese maple)
near the centre, and a **pond** — the one element every broker mentions, visible in the
aerial as a pale kidney shape in the shadow. Units on both blocks have French doors
onto it, so expect a run of doors and small patios at courtyard ground level.

**Top — see 2.9.**

### 2.5 Recognition cues (ranked)

1. **The oval window motif.** A single long flattened ellipse with a curled tail drawn
   in heavy mullion across each wide window band. Nothing else on the South Park oval
   has an ornament like it, and it is legible from the app's camera because it sits in
   a pale surround on a warm wall.
2. **Apricot stucco on the north rim.** Every neighbour is sage-green clapboard, cream
   ashlar, red brick or grey warehouse. This is the only warm-orange building on the
   arc, and colour is what the aerial camera reads first.
3. **The two-block plan with an open courtyard** — a pentagon with a hole in it, on a
   rim where every other lot is one solid mass wall to wall.
4. **The bowed front**: 44.5° of turn across 16.8 m, sharp enough that the two front
   planes catch the sun differently.
5. **The stacked loggias** — two deep shadow recesses one above the other at the
   north-east end of the front, the only real depth in the elevation.

### 2.6 Miniature translation

- Keep the two-block plan, the courtyard, the frontage break, the four window bands,
  the two loggias and the oval motif. These are the building.
- Keep the parapet as a clean unbroken ring with a thin pale cap; keep the bulkhead as
  one chunky box.
- Simplify the window grids: the small-pane grid becomes 3–4 heavy mullions per band,
  not a literal lattice. The oval survives at full weight; the grid behind it does not.
- Simplify the juliet balconies to a rail, two posts and the grate slab. The ironwork's
  scrollwork goes.
- Simplify the Taber Place windows to paired dark rectangles in pale surrounds.
- Drop entirely: expansion joints, downpipes, light fittings, cameras, the plaque, unit
  numbers, the security-gate pattern, roof-drain scuppers, the sidewalk magnolia.
- Exaggerate: the loggia recess depth (push to ~1.2 m so it reads as black from above),
  the pale window surrounds (widen so the bands read as bands), the courtyard's green.

### 2.7 Massing recipe

1. **Lot prism.** Build the parcel outline in the lot frame: front line (8.13 m
   straight, then the 8.64 m arc as 4–5 facets), 36.28 m south-west party wall,
   14.29 m Taber rear, 42.34 m north-east party wall.
2. **Front block:** extrude the front 20.67 m of that outline to the 12.27 m deck, then
   the parapet ring to 13.10 m with a 0.25 m inset and a thin cap.
3. **Rear block:** extrude the rear 11.22 m of the outline to 11.88 m deck plus its own
   parapet to ~12.7 m, and add the 3.0 × 4.3 m north-east wing forward of it.
4. **Bulkhead:** a 5.7 × 2.4 m box on the front block's roof, at the courtyard edge,
   centred about u 0 → +3.7, rising to **14.67 m** — the model's tallest point.
5. **Courtyard floor:** a paved slab at ~0.15 m, planting beds along both party walls,
   the pond as a shallow inset disc, one tree.
6. **Front elevation:** cut the garage opening and the entry slot; cut the two loggias
   as 1.2 m recesses through both tiers at the north-east; add the four window bands
   with their surrounds and ovals; add the two arched French doors and their balconies.
7. **Taber elevation:** two bands of paired windows, one door with gate, one garage.
8. **Roof furniture:** three or four chunky mechanical boxes and one dark panel along
   the north-east parapet of the front block. Nothing on the south-west half.
9. Bevel everything (0.1–0.15 m, 2 segments) and check from the aerial before adding
   anything else.

### 2.8 Materials and palette

All values *estimated* from a January 2025 Street View capture in mixed light; the
sunlit stucco medians to `#b58f70` in the raw pixels, which under that exposure implies
a considerably lighter apricot in life. Sample a better photograph before committing.

| surface | material | hex | note |
|---|---|---|---|
| body stucco, both blocks, all elevations | `Toy_apricot` | `dda87b` | **off-palette** — the palette has no warm mid-orange (`rust a86444` is far too dark, `brick c96f4a` too red, `mustard d9a441` too yellow). Off-palette is a WARN, not a FAIL, and the block already carries `Toy_verdigris`, `Toy_sash` and `Toy_plum` for the same reason. Record it in REPORT.md. |
| window surrounds, parapet cap | `Toy_sand` | `ece4d4` | the pale flat bands that make the window bands read |
| glazing | `Toy_glass` | `2a4d73` | |
| mullions, glazing bars, the oval motif | `Toy_ink` | `3a3530` | the oval must be `Toy_ink` on `Toy_glass`, not a lighter tone, or it vanishes at distance |
| French doors | `Toy_rust` | `a86444` | natural stained wood; the nearest palette entry |
| iron railings, grates, security gate | `Toy_ink` | `3a3530` | |
| roof deck, both blocks | `Toy_stone` | `d9d2c2` | pale membrane. **Do not use `Toy_roofd`** — it renders as `rgb(9,9,12)` under the app's lighting and a roof deck in it reads black. |
| bulkhead, mechanical, roof panel | `Toy_steel` | `9aa0a6` | |
| courtyard paving | `Toy_stone` | `d9d2c2` | |
| courtyard planting | `Toy_mint` | `8fd0a8` | the style bible allows vegetation to be vivid |
| courtyard tree foliage | `Toy_plum` | `6b4270` | matches the purple-bronze specimen in the aerial; borrowed from `46-south-park` |
| pond | `Toy_navy` | `2c4a70` | flat, no transparency |

**Night.** The hero glow is the **four front window bands** — this is a residential
building whose whole street face is glass, and at night that is what it is. Use
`Toy_glassl_Glow` `6f95b8` for the bands and the Taber Place paired windows, and leave
the loggias, the arched doors, the garage and both roofs dark. Remember that a `_Glow`
material's **base colour is its night appearance** in the app (the night layer is an
unlit overlay at the material's own baked colour), so pick the base colour for how it
should look at night, and confirm the day appearance sits next to `Toy_glass`
acceptably. One supporting accent only: a small warm `Toy_mustard_Glow` at the
pedestrian entry slot. Do not glow the courtyard.

### 2.9 Top surface — *the least certain section in this plan*

Read off Google z21 satellite imagery that leans several metres across this block.
Everything here is inference and the executing agent should re-derive it.

- **Front block:** a clean pale membrane deck at 12.27 m inside a plain parapet. A
  **grey rectangular bulkhead ~5.7 × 2.4 m** at the rear (courtyard) edge, roughly
  centred on the lot's width, with a small T-shaped return. A cluster of small
  mechanical units and one **dark rectangular panel** (skylight or PV, ~0.9 × 1.8 m)
  along the north-east parapet. Several small round vents. Nothing on the south-west
  half of the deck.
- **Rear block:** appears to carry a **terracotta-coloured surface** over much of its
  roof, with a pale band along the Taber Place edge that may be planters. Two
  **tan hipped shapes** with visible diagonal ridges sit near the courtyard — one at
  the rear block's north-east corner, one at the front block's courtyard edge. These
  read as small hipped tile roofs over stair heads, which would be entirely in
  character for a "Contemporary Mediterranean" building — or as paver terraces. See
  2.15 risk 3.
- **Courtyard:** in deep shadow in the only usable capture. Legible: a
  **purple-bronze specimen tree** roughly 3 m across near the centre, green shrub
  masses against both party walls, and a pale curved shape at the south-west that is
  most likely the pond.

### 2.10 Scope

**In:** both blocks, the courtyard and everything in it, the roof furniture of both.

**Out:** South Park (the oval, its lawn, paths and elms), South Park Street, Taber
Place, both neighbours, the sidewalk, the sidewalk magnolia at the north-east front
corner, parked cars, people, plinths, cameras, lights.

### 2.11 Triangle budget

12,000, above the 9,000 that is this block's norm, because this asset is two buildings
plus a designed ground plane rather than one building:

| element | budget |
|---|---|
| front block shell + faceted bowed front + parapet ring | 2,000 |
| rear block shell + wing + parapet | 1,200 |
| 4 window bands: surrounds, mullions, oval motifs | 2,600 |
| 2 arched French doors + juliet balconies + grates | 1,100 |
| 2 loggia recesses + railings | 900 |
| Taber Place openings (paired windows, door, gate, garage) | 900 |
| garage door, entry slot, ground-floor windows | 500 |
| bulkhead + roof mechanical + panel | 500 |
| courtyard: slab, beds, pond, tree | 1,300 |
| bevels and slack | 1,000 |

### 2.12 Draft manifest entry

```json
{
  "id": "10-south-park",
  "file": "10-south-park.glb",
  "anchor": [
    -122.3934999,
    37.7823712
  ],
  "targetHeightM": 14.67,
  "cat": 2,
  "name": "10 South Park (South Park Lofts)",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

`loadRadius` follows the default rule `max(2500, targetHeightM × 30)` =
`max(2500, 440)` = **2500**, the same as every other South Park asset. Nothing about a
15 m residential building justifies `alwaysLoaded`.

`name` deliberately leads with the address rather than "South Park Lofts", because
`188-south-park` already ships in this manifest under that marketing name.

### 2.13 Integration notes (for later, not this task)

**Case B — new landmark.** No `10SouthPark` id exists in `pipeline/lib/landmarks.mjs`
or `app/src/landmarks.js`, so integration needs a registry entry, a manifest entry and
a re-bake of the affected tiles, or the two baked procedural blocks will stand inside
the GLB.

**This lot needs THREE exclusion zones, not one.** It carries two baked footprints with
an open courtyard between them, exactly like `132SouthPark`, and its anchor sits in
that courtyard because that is where the GLB's bounding-box centre lands. Measured from
each candidate centre **against the rings the bake actually reads** — the DataSF
`ynuv-fyni` pass and the Overture gap-fill pass, both extracted from
`pipeline/data/` — and remembering that `excluded()` drops a footprint whose ring
**centroid OR any vertex** is inside:

```
from the anchor (-122.3934999, 37.7823712):
    1.35 m  own front block, nearest vertex     (drops it, by vertex)
    1.89 m  own front block, Overture ring vertex
    5.21 m  2 South Park (Overture) vertex      <- the ceiling
    5.90 m  own rear block, nearest vertex
    6.41 m  2 South Park (DataSF) vertex

from the front-block zone (-122.3934359, 37.7823083):
    1.24 m  own front block, DataSF ring CENTROID
    1.48 m  own front block, Overture ring CENTROID
    8.94 m  22-24 South Park (DataSF) vertex    <- the ceiling
    9.09 m  22-24 South Park (Overture) vertex

from the rear-block zone (-122.3936335, 37.7824581):
    2.38 m  own rear block, DataSF ring CENTROID
    2.43 m  own rear block, Overture ring CENTROID
    7.09 m  22-24 South Park (Overture) vertex  <- the ceiling
    7.61 m  2 South Park rear (Overture) vertex
```

So:

| zone | centre | r | window | margins |
|---|---|---|---|---|
| `exclude` (anchor guard) | −122.3934999, 37.7823712 | **2** | (—, 5.21) | 3.2 m to the nearest neighbour |
| front block | −122.3934359, 37.7823083 | **5** | (1.48, 8.94) | 3.5 below, 3.9 above |
| rear block | −122.3936335, 37.7824581 | **4.5** | (2.43, 7.09) | 2.1 below, 2.6 above |

Each block is dropped by its ring **centroid**, never by reaching its far corners: the
front block's own vertices run to 14.7 m from its zone centre and the rear block's to
7.3 m, and a radius that reached them would delete 22–24 South Park and 2 South Park,
neither of which has a GLB to replace it and both of whose failures are silent. The
2 m guard at the anchor drops the front block today (by vertex, at 1.35 m) but its real
job is `132SouthPark`'s: stopping the Overture gap-fill from re-filling a lot that
`markOccupied()` no longer sees as occupied once the DataSF footprints are excluded. A
whole-lot Overture polygon would centre within about a metre of the anchor and sail
past both other zones. **Do not raise it** — 2 South Park's Overture vertex is 5.21 m
out.

Note that **both** of this lot's buildings are traced twice, by DataSF and by Overture
(`…79f82d14b81c` 251 m² front, `…e716f25d7e5b` 150 m² rear), so a correct exclusion
drops **four** rings here, not two. Expect the re-bake diff to show that.

Draft registry entry:

```js
{
  id: '10SouthPark',
  name: '10 South Park (South Park Lofts)',
  lon: -122.3934999,
  lat: 37.7823712,
  height: 14.67,
  exclude: 2,
  extraExclusions: [
    { lon: -122.3934359, lat: 37.7823083, r: 5 },   // front block on South Park
    { lon: -122.3936335, lat: 37.7824581, r: 4.5 }, // rear block on Taber Place
  ],
  // Camera bearing = 180 - yaw (camera.js apply(): offset is (sin yaw, ., cos yaw)
  // and +z is south), so yaw 30 stands the camera at bearing 150 = SSE. That is
  // square onto the bowed south-west two-thirds of the front (normal 179.7 deg)
  // and still oblique enough to read the straight north-east third (135.2 deg).
  // Pitch 30 rather than the block's usual 26 so the courtyard between the two
  // blocks is visible over the front block's parapet — it is half the point of
  // this asset. No `key`: at 15 m this is texture in the block, not a destination.
  camera: { distance: 200, yaw: 30, pitch: 30 },
}
```

**Batch mode.** If other landmarks are in flight, run the bake and the full QA on it,
then `git checkout -- app/public/tiles api/_data` before committing, and commit source
only. See `docs/asset-pipeline/ADDRESS-TO-ASSET.md` stage 5.

### 2.14 Validation checklist

- Re-import validation on the exported GLB, fresh scene.
- Two disjoint solids plus a courtyard slab: use the **per-object signed volume** test
  for normals as authoritative, ray test ≤ 0.15 % residual as cross-check.
- Tallest geometry at exactly 14.67 m; min Z ≈ 0; XY centre ≈ (0, 0).
- Axis-aligned XY bbox ≈ 40 × 36 m — expected at a 45° heading, not a scale error.
- Materials: `Toy_*` only, one `_Glow` group, no `Toy_body`, no textures, no alpha.
- ≤ 12,000 triangles.
- Day and night renders from the aerial, and a top view that shows the whole courtyard.
- Sanity: the model must be visibly *shorter* than 2 South Park (17.72 m) and *taller*
  than 22–24 South Park (14.22 m) by only half a metre at the bulkhead — its parapet
  at 13.10 m is more than a metre below 22–24's crest. If the finished asset towers
  over its neighbours, the height is wrong.

### 2.15 Open questions and risks

1. **The bulkhead is inferred, and it is the target height.** 14.67 m is a LiDAR
   maximum 3.1σ above the median, corroborated by a shape in an oblique satellite image
   and by the rear block reporting the same 2.4 m step. It is not corroborated by any
   photograph — a roof bulkhead set back behind a 13.1 m parapet is invisible from both
   streets. If the executing agent cannot find it, the fallback is to model the parapet
   crest at **13.10 m** as the target height and say so; that number is photogrammetric
   and solid. Do not split the difference.
2. **The north-east end of the front elevation is guessed.** A large sidewalk magnolia
   stands exactly there and hides the last ~4 m of frontage plus the corner with 2 South
   Park in every Street View capture from either direction. The photogrammetric crest
   drops from 13.10 m to about 11.6 m across bearings 356°–2° from the front pano,
   which reads as a set-back or lower top level at that end — but it could equally be
   the detector finding a loggia soffit through foliage. Find an aerial or listing photo
   before deciding, and if you cannot, model it flush and record the assumption.
3. **The roof is read from imagery that leans.** Google z21, Bing z20 and Esri z20 were
   all fetched and registered against the parcel and footprint rings; in all three, 2
   South Park's roof overhangs our surveyed parcel line by metres. Everything in 2.9 —
   including whether the rear block is tile-roofed, whether the two tan hipped shapes
   are ours or the neighbours', and where exactly the bulkhead sits — carries that
   error. This is the section most likely to be wrong.
4. **The colour is one capture under mixed light.** See 2.8. The 2012–13 permit
   confirms the current stucco is a replacement of the whole South Park elevation, so
   the coat is recent, but nothing dates the colour.
5. **The architect is a single source.** Ramon Zambrano appears on somapro.com's loft
   database and nowhere else found. It is a plausible attribution from a broker who
   sold the units new, and nothing contradicts it, but it is one page. Label it
   accordingly in REFERENCE.md.
6. **The frontage: break or bow?** The survey says a straight segment, a ~30° corner
   and a 14° arc. The photographs read as a continuous curve. At the miniature's scale
   the difference is 0.26 m of sagitta and it will not be visible — but the 30° corner
   will be, and getting it in the wrong place moves the whole composition. Resolve it
   against a rectilinear Street View frame before laying out the window bands.
7. **Nominatim will lie to you.** See the trap note in Part 1. Every spatial route into
   this lot has to start from the Assessor's parcel, not from a geocoder.
