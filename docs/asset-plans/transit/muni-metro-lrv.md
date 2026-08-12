# Muni Metro LRV — SF-SIM asset plan

The Siemens S200 light rail vehicle: a long silver articulated train with a
rounded black-faced cab and a pantograph on the roof. Per the transit README's
no-rails-no-wires decision this vehicle runs on the street like every other road
vehicle — San Francisco's surface Metro genuinely runs in mixed traffic on Judah,
Church and Third, so a train moving down a street reads correctly without a rail
under it.

**Deliverable:** one validated miniature GLB plus dossier, renders and report under `artifacts/muni-lrv/`. Part 1 is
the runnable task prompt, Part 2 the dossier, Part 3 the shrink stage.

| | |
|---|---|
| Slug | `muni-lrv` |
| Manifest | `app/public/sf-assets/vehicles_manifest.json` |
| Model | `muni-lrv` — the Siemens S200. **One GLB;** coupling is a runtime concern, not a second model. |
| Real vehicle | Siemens S200 SF (LRV4) |
| Real dimensions | 22.86 m × 2.65 m × ~3.6 m; 2 sections, 1 articulation, 8 plug doors |
| Triangle cap | 5,000 |
| Draw-call cost | **+1** permanent |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready Muni Metro LRV GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of San Francisco's Muni Metro light rail
vehicle (Siemens S200 SF / LRV4) and deliver it as a downloadable, validated GLB.

Do not integrate or deploy the model yet. Create the asset, validate it, render
review images, run the shrink stage, and commit the deliverables to your working
branch.

## Read the project sources first

1. `AGENTS.md`
2. `docs/styles/README.md`
3. `docs/styles/miniature-toy.md`
4. `.agents/skills/sf-asset-check/SKILL.md`
5. `docs/asset-plans/transit/README.md` — vehicle contract overrides, draw-call
   and scale facts, the shared shrink recipe, and **the no-rails-no-wires
   decision**
6. `app/public/sf-assets/vehicles_manifest.json` and the existing GLBs in
   `app/public/sf-assets/vehicles/` — the contract you must match
7. `app/src/agents.js` — `loadVehicles()`, `mergeVehicle()`, the instancing loop,
   so you understand exactly how your asset gets drawn
8. `docs/asset-plans/transit/muni-metro-lrv.md` — this plan

## Must capture

- Modern articulated light-rail vehicle; long, narrow body
- Rounded/sloped aerodynamic cab
- Huge dark front windshield
- Silver/light-gray body with red Muni accents
- Black window band
- Multiple large sliding doors
- Digital destination sign
- Roof equipment
- **Pantograph, visibly raised toward an overhead wire**

**Articulation:** the S200 is two body sections joined at one articulation. Model
the accordion joint — do not build it as a conventional single train car. The
bend is what makes it read as a modern LRV rather than a boxcar.

**Wheel area:** much lower to the ground than a traditional train, with the wheel
assemblies partially hidden behind the bodywork skirt.

**Most important visual signature:** long silver rail vehicle + red accents +
rounded black-faced cab + pantograph.

## Research the vehicle independently

Verify the dossier rather than trusting it. Re-check the model designation,
length, width, height, section count, door count and pantograph geometry, and
gather references covering:

- Front (cab), rear, both sides, and **roof views**
- The cab's compound curvature — where the windshield meets the roofline and the
  skirt, which is the hardest shape in this asset
- The articulation joint: bellows geometry, how the roofline and window band
  cross it
- The pantograph raised and lowered, and its mounting frame
- The red Muni accent geometry against the silver body
- Door arrangement and spacing along the body
- Day and night appearance, including which surfaces are lit
- Two coupled LRVs and how the coupler sits between them

Prefer SFMTA and Siemens publications, transit fleet documents, geolocated
photography, and aerial imagery. Never rely on a single photograph, a single
AI-generated image, or a single unsourced 3D model.

## Create a reference dossier

Write `artifacts/muni-lrv/REFERENCE.md`: source links and what each establishes,
verified dimensions, cab geometry, articulation geometry, pantograph geometry,
observations from all sides and above, the 3–5 strongest recognition cues,
features to preserve and simplify, uncertainties. No copyrighted
full-resolution imagery.

## Make your own design decisions

Follow `docs/styles/miniature-toy.md` §22. Three points specific to this asset:

- **The cab is the whole silhouette.** A light rail vehicle is a long extruded
  box with one interesting end. Every triangle you can afford beyond the basic
  massing belongs to the cab's rounded face and its dark windshield.
- **Articulation must be visible from above.** The app camera looks down at 42°.
  A bellows that only reads in side elevation is invisible where it matters —
  break the roofline across the joint so the articulation reads from the top.
- **Silver is dangerous under flat diorama lighting.** A single mid-grey body
  will read as a featureless slab. Separate the skirt, body and roof into three
  distinct values, and let the black window band and red accent carry the
  contrast.

## Scope of the exported asset

Export the vehicle body (both sections), the articulation bellows, wheels/bogie
skirts, roof equipment, the pantograph, and the destination sign.

Do not include: rails, sleepers, overhead wire, catenary poles, station
platforms, passengers, driver, road surface, ground plane, plinth, cameras or
lights. There are no rails or wires anywhere in this scene, and a vehicle GLB
carrying its own track would drag a floating rail around the city.

## Technical asset contract — VEHICLE, not landmark

Follow `.agents/skills/sf-asset-check/SKILL.md` with the vehicle overrides in
`docs/asset-plans/transit/README.md`:

- **Front (cab) faces `−Z` in Blender**
- **Ground at `min y = 0`** — the wheel contact patch sits on the **street
  surface**, exactly like a bus. With no rails in the scene there is no
  top-of-rail question: zero is the road.
- Origin centred in the X/Z footprint
- Real metres, applied transforms, no negative scales, outward normals
- No textures, no transparency, flat `Toy_*` colours
- `_Glow` only on night surfaces; no `Toy_body`; no cameras, lights, animation,
  armatures or constraints
- **≤ 5,000 triangles**

**Build the model straight, not bent.** The articulation must be modelled as real
geometry, but the exported pose is a straight vehicle. A runtime that bends the
train around curves needs the two sections separable and symmetric about the
joint; a pre-bent export is useless. Name the two section objects clearly
(`LRV_Section_A`, `LRV_Section_B`, `LRV_Bellows`) so a future runtime can split
them — node names survive the meshopt intake because it runs with `-kn`.

## The night-glow set

The loader puts `_Glow` materials in a separate unlit layer at
`opacity = 0.12 + 0.95 * uNight` — a glow surface is **88% transparent by day**,
so author each as a thin shell 3–5 cm proud of an opaque surface with buried
edges.

| Surface | Material | Reads as |
|---|---|---|
| Destination sign face | `Toy_mustard_Glow` | route identification |
| Headlight cluster | `Toy_white_Glow` | the cab at night |
| Tail lights | `Toy_red_Glow` | rear identification |
| Interior ceiling strip behind the window band | `Toy_mustard_Glow` | a lit, occupied train — the strongest cue on a vehicle this long |

Ship emission at 0.0 per contract. Remember the render gotcha: a glTF
`emissiveFactor` of (0,0,0) makes Blender's importer default Emission Color to
**white**, so copy Base Color into Emission Color before raising strength, or
every glow surface previews white.

## The destination sign

Use genuine Metro line designations. `N JUDAH`, `J CHURCH` and `T THIRD` are the
strongest choices because they are the surface lines a player will actually see —
the subway segments are invisible in this app. At most three variants, extruded
geometry on the `Toy_mustard_Glow` shell, no textures.

## Reproducible Blender workflow

Blender headless: `blender -b --python script.py -- args`. No GPU — Workbench or
CPU Cycles. Blender 5.x uses `surface_render_method`, not `blend_method`.

Keep `artifacts/muni-lrv/build_muni_lrv.py` (deterministic),
`artifacts/muni-lrv/muni-lrv.blend`, and the exported GLB.

Leak-proof export: temp scene with only the export collection,
`use_active_scene=True`, `export_apply=True`, re-import and verify object count,
bbox and material set. Wrap exporter calls in `contextlib.redirect_stdout`.

## Required review renders

`muni-lrv-front.png`, `-rear.png`, `-left.png`, `-right.png`, `-top.png`,
`-aerial.png`, `-night.png`, plus `muni-lrv-contact-sheet.png`.

The four elevations must share scale, framing, lighting, exposure and
projection. The top view must show the roof equipment and the articulation break.

**Plus two mandatory extra renders, both of which are where this asset fails:**

1. **1.6× in-city scale test** against real baked city geometry from the diorama
   camera, on a real surface segment — Judah in the Sunset or Church in Noe.
   The app applies `carScale = 1.6`, so a single LRV renders at **36.6 m** and a
   coupled pair at **73.2 m**, longer than many of the blocks it runs down.
   Judge honestly and report: if a coupled pair spans an entire block face, say
   so and recommend either single-car operation in the app or a per-type scale
   override at integration.
2. **A coupled-pair render** — two instances nose to tail at the correct coupler
   gap, at 1.6×, from the app camera. Coupling is the normal Metro configuration
   and it doubles every scale problem.

## Validate the exported GLB

Fresh-scene re-import. Report object count, triangle count, dimensions, bbox
min/max, **min y**, XZ centre
offset, **front-face direction**, section node names, material names,
texture/camera/light/animation counts, applied transforms, negative scales,
per-object signed volume, per-material compliance. Write
`artifacts/muni-lrv/validation.json` and `REPORT.md`.

## Shrink stage

Run the shrink and intake stages from `docs/asset-plans/transit/README.md`
Part 3 with `ASSET_CLASS=vehicle`. Record before/after and every gate in
`REPORT.md`. Limited dissolve at **0.05°** — this matters more here than on any
other transit asset, because the cab is a curved shell and 0.5° dissolve on
curved shells builds twisted ngons that re-triangulate with flipped windings.
Never weld across a `_Glow` boundary. gltfpack `-cc -kn -km -noq`, and **verify
`-kn` preserved the section node names** you will need for articulation.

Do not run the high→low texture bake.

## Manifest draft

```json
{ "id": "muni-lrv", "file": "vehicles/muni-lrv.glb", "kind": "lrv",
  "dims": [x, y, z], "targetLengthM": 22.86, "front": "-Z",
  "tris": N, "weight": 1,
  "notes": "No rails or overhead wire in the scene." }
```

`weight: 0` is deliberate and load-bearing: `agents.js` filters
`(entry.weight ?? 1) > 0`, so a zero-weight entry is loaded into the fleet array
but never dealt a road instance. Without it, Metro trains drive down Lombard.

Do not edit the production manifest.

## Do not

- author to the landmark `−Y` front convention
- export the vehicle pre-bent at the articulation
- include rails, wires or catenary poles in the vehicle GLB
- use `Toy_body`, add textures, or ship a `_Glow` primary surface
- give the entry a non-zero `weight`
- edit `vehicles_manifest.json`, `app/src/agents.js` or any app code
- skip the 1.6× and coupled-pair renders
````

---

## Part 2 — Research and design dossier

Compiled 12 August 2026. Values marked *inferred* are visual or derived
estimates — re-verify anything you rely on.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Model | Siemens **S200 SF** (LRV4) | Muni Metro fleet |
| Order size | 219 LRV4 units ordered; first in service Nov 2017 | Siemens S200 |
| Length | 22.86 m (75 ft) single; 45.7 m (150 ft) coupled pair | Muni Metro |
| Width | 2.650 m (104.32 in) | Siemens S200 |
| Height | 3.5–4.1 m over roof equipment | Siemens S200 |
| Floor height | 0.85 m | Siemens S200 |
| Articulated sections | **2 sections, 1 articulation** | Siemens S200 |
| Doors | 8 plug doors | Siemens S200 |
| Boarding | level boarding with retractable steps (SF-specific) | Siemens S200 |
| Current collection | Faiveley **pantograph**, 600 V DC | Siemens S200 / Muni Metro |
| Track gauge | 1,435 mm standard gauge | Muni Metro |
| Surface lines | J Church, K Ingleside, L Taraval, M Ocean View, N Judah run on surface alignments before entering tunnel | Muni Metro |

The gauge figure matters only for **wheel spacing on the model itself** — there
is no track in the scene. Note in passing that Metro is standard gauge
(1,435 mm) while the cable cars are narrow gauge (1,067 mm), so the two families'
wheels genuinely sit at different widths.

### 2.2 Sources

- https://www.sfmta.com/muni-transit — the family taxonomy
- https://en.wikipedia.org/wiki/Muni_Metro — fleet, surface lines, gauge, 600 V DC
- https://en.wikipedia.org/wiki/Siemens_S200 — dimensions, sections, doors, pantograph, floor height, delivery
- Siemens S200 product literature — body geometry
- SFMTA line pages — current surface alignments

### 2.3 Orientation and placement

Vehicle contract: cab faces `−Z`, origin centred in X/Z. `min y = 0` is the
**wheel contact patch on the street surface**, identical to the buses. There are
no rails in the scene, so there is no railhead offset to reason about.

### 2.4 What each side shows

**Front (cab)** — The signature view. A rounded, forward-raked face dominated by
a single large dark windshield wrapping into the body sides. Headlight clusters
low in the fascia. The destination sign sits above the windshield. Red Muni
accent below the glass. Coupler visible at the bottom.

**Sides** — A long silver flank broken by a continuous black window band and four
door openings per side. The skirt below the window line hides most of the bogie.
The articulation bellows breaks the flank at the midpoint. Red accent runs as a
band low on the body.

**Rear** — On a single-ended vehicle, a simpler version of the cab; on the SF
fleet, verify whether the LRV4 is double-ended (it operates in both directions in
the subway, which strongly suggests it is — confirm before modelling a blank rear).

**Top** — Long silver expanse with roof equipment boxes over each section, the
pantograph mounted on the roof of one section, and the articulation break
crossing the roofline. The pantograph is the strongest identifying feature from
the app's aerial camera.

### 2.5 Recognition cues (ranked)

1. Long silver body + rounded black-faced cab
2. Pantograph raised from the roof (the aerial camera's read)
3. Red Muni accent band against silver
4. Articulation joint breaking the body into two
5. Low skirt hiding the wheels — it does not read as a heavy-rail train

### 2.6 Miniature translation

**Preserve**

- 22.86 m × 2.65 m at real scale, and the low 0.85 m floor
- 2 sections, 1 articulation
- Pantograph on the roof, raised
- The cab's rounded, raked face

**Simplify / exaggerate**

- 8 plug doors become 4 chunky `Toy_ink` recesses per side, evenly spaced —
  modelling plug-door hardware is invisible at any app distance
- The cab's compound curvature becomes 3–4 chamfered planes, not a lofted
  surface; the toy style wants faceted, and a lofted cab will eat 2,000 triangles
- Pantograph exaggerated: thicken the arms well past scale and simplify to a
  single-arm Z shape with a chunky contact bar. Like the trolley poles, this is
  the identity feature and scale accuracy makes it vanish.
- Bogies reduced to two wheel discs per truck behind a solid skirt
- Articulation bellows exaggerated in rib count and depth so it reads from above
- No interior, no seats, no coupler hardware beyond a simple block

### 2.7 Massing recipe

Build order for the deterministic script; adjust after the first 1.6× in-city
render.

1. **Section A body** — box 11.2 × 2.65 × 2.2 m, floor at y 0.85, roof at y 3.05,
   bevel 0.12 m / 2 segments, `Toy_steel` (silver).
2. **Section B body** — same, mirrored about the articulation.
3. **Cab** — chamfer the leading 2.0 m of Section A: rake the front face ~18°,
   round the upper corners with a 0.5 m chamfer, drop the roofline 0.1 m.
4. **Windshield** — one `Toy_glass` volume wrapping the raked face into the
   front corners, inset 0.05 m.
5. **Window band** — recess 0.05 m from y 1.95 to 2.65 along both flanks,
   `Toy_ink` reveal with `Toy_glass` panes 0.02 m inside.
6. **Doors** — 4 per side, `Toy_ink` recesses with `Toy_glass`, evenly spaced.
7. **Red accent** — a 0.02 m proud `Toy_red` band running the full length below
   the window line and sweeping up across the cab fascia. Author as geometry so
   the shrink pass cannot dissolve it.
8. **Skirt** — inset 0.08 m per side from y 0.35 to 0.85, `Toy_ink`, hiding the
   bogies.
9. **Wheels** — 8 discs, radius 0.35 m, 8 segments, `Toy_ink`, set behind the skirt.
10. **Articulation** — 0.5 m gap between sections filled with a ribbed bellows
    (8 ribs, `Toy_ink`), carried across the roofline so it reads from above.
11. **Roof equipment** — two chunky `Toy_steel` boxes, one per section, with
    `Toy_ink` grille insets.
12. **Pantograph** — Z-arm on Section A's roof: lower arm 1.1 m, upper arm 0.9 m,
    arm radius 0.07 m (exaggerated), rising to a 1.9 m contact bar at y ~4.6,
    `Toy_steel`. Mount on a low `Toy_ink` insulator plinth.
13. **Destination sign** — recessed above the windshield; opaque `Toy_ink`
    backing with a `Toy_mustard_Glow` shell 0.04 m proud, extruded glyphs.
14. **Lights** — `Toy_white_Glow` headlight shells, `Toy_red_Glow` tail shells,
    each proud of an opaque `Toy_ink` housing.

### 2.8 Materials and palette

| Material | Hex | Used for |
|---|---|---|
| `Toy_steel` | `#9aa0a6` | body, roof equipment, pantograph |
| `Toy_white` | `#f7f4ec` | roof (a lighter value so the roof separates from the flanks) |
| `Toy_red` | `#c4453c` | Muni accent band, cab fascia sweep |
| `Toy_ink` | `#3a3530` | window band reveal, doors, skirt, bellows, wheels, insulator |
| `Toy_glass` | `#2a4d73` | windows, windshield, door glazing |
| `Toy_mustard_Glow` | `#d9a441` | destination sign face |
| `Toy_white_Glow` | `#f7f4ec` | headlights |
| `Toy_red_Glow` | `#c4453c` | tail lights |
| `Toy_mustard_Glow` | `#d9a441` | interior ceiling strip |

Three distinct values — skirt (dark), body (mid silver), roof (light) — are what
stop a 23 m silver box from reading as a featureless slab under flat lighting.

### 2.9 Top surface

The most-seen surface on the longest vehicle in the set. Composition: cab roof
sloping into the body, roof equipment box over Section A, the pantograph on its
insulator plinth, the articulation break crossing the roofline, roof equipment
box over Section B. Keep the roof a lighter value than the flanks so the
silhouette separates, and make the articulation break a real geometric step, not
a colour change.

### 2.10 Scope

**In the GLB:** both body sections, articulation bellows, wheels and bogie
skirts, roof equipment, pantograph, destination sign, lights

**Not in the GLB:** rails, sleepers, overhead wire, catenary poles, platforms,
passengers, driver, road surface, ground plane, plinth, cameras, lights

### 2.11 Triangle budget

Cap 5,000. Suggested split: two body sections 1,600 · cab chamfers and
windshield 900 · glazing and doors 700 · red accent 300 · skirt and wheels 500 ·
bellows 300 · roof equipment 300 · pantograph 250 · sign and lights 150.

The cab is where a budget overrun happens. If the chamfered cab pushes past 900,
reduce chamfer segments before taking triangles from the pantograph — the
pantograph is the aerial read and the cab is the ground-level read, and this app
is an aerial app.

### 2.12 Draft manifest entry

```json
{ "id": "muni-lrv", "file": "vehicles/muni-lrv.glb", "kind": "lrv",
  "dims": [x, y, z], "targetLengthM": 22.86, "front": "-Z",
  "tris": N, "weight": 1,
  "notes": "No rails or overhead wire in the scene." }
```

### 2.13 Integration notes — deferred

Placement, spawning, weighting and live Muni data are **out of scope for this
task** and are parked in
[`docs/asset-plans/transit/INTEGRATION-LATER.md`](./INTEGRATION-LATER.md).

What this task owes the follow-up is only the draft manifest entry in
`REPORT.md`, and anything the renders revealed about how the vehicle behaves at
1.6× scale in the real city — that evidence is what the integration decisions
will be made from.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB
- [ ] **Cab faces `−Z`**; `min y` within 0.05 m of 0; XZ centre offset within 0.1 m
- [ ] Exported straight, not pre-bent at the articulation
- [ ] Section node names present and survive meshopt intake (`-kn` verified)
- [ ] Dimensions match 2.1 in real metres
- [ ] Triangles at or under 5,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] Three distinct body values (skirt / body / roof) verified under flat lighting
- [ ] `_Glow` only on sign, headlights, tail lights, interior strip — proud shells
- [ ] Per-object signed volume positive, **including the pantograph arms**
- [ ] No cameras, lights, animations, armatures, constraints; no leaked geometry
- [ ] Day and night renders; elevations + top + aerial + contact sheet
- [ ] **1.6× in-city scale render on a real surface segment**
- [ ] **Coupled-pair render at 1.6×**
- [ ] Shrink stage run at 0.05° dissolve; gates recorded
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

- **Scale is the top risk in the entire transit set.** A coupled pair at 1.6×
  is 73.2 m. Many SF blocks are shorter than that. This may be the asset that
  forces a per-type scale override in `agents.js`, and the plan should surface
  that conversation with a render rather than assume it away.
- **Single-ended or double-ended?** The LRV4 operates bidirectionally in the
  subway. Confirm before modelling a blank rear — a wrong answer here is visible
  from every angle and doubles or halves the cab budget.
- **Curved-shell dissolve.** The cab is the exact geometry the 0.5° limited
  dissolve was found to destroy. Use 0.05° and check windings after.
- **Silver under flat lighting.** If the three body values do not separate the
  form, the model reads as a grey brick regardless of how good the cab is. Judge
  this from the app camera at 120 m, not from a studio turntable.
- **This is the asset the no-rails decision costs the most, and it is still
  fine.** SF's surface Metro runs in mixed street traffic, so a train on a street
  is not a lie. What is lost is the pantograph's reason for existing — it now
  reaches toward nothing. Unlike the trolley coach's 6 m poles, a pantograph is a
  compact roof object that reads as roof equipment at the app's camera distance,
  so this is a much smaller price. Confirm that at 120 m and record the judgement.
- **Length, not detail, is what will make or break this asset.** Everything hard
  about it — the cab curvature, the articulation, the silver values — is
  secondary to whether a 36.6 m vehicle looks right on a San Francisco block. Do
  the in-city render early, before polishing anything.
