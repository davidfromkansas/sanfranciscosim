# Muni hybrid bus — SF-SIM asset plan

The modern white-and-red New Flyer Xcelsior that most San Franciscans actually
ride. This is the pilot of the transit set: the simplest family and the one
closest to the existing fleet, so it proves the vehicle contract, the
destination-sign pattern, the night-glow pass and the shrink stage before
anything else is attempted.

**Deliverable:** one validated miniature GLB plus dossier, renders and report
under `artifacts/muni-bus/`. This document is the plan only: Part 1 is the
runnable task prompt, Part 2 is the research and design dossier, Part 3 is the
shrink stage.

| | |
|---|---|
| Slug | `muni-bus` |
| Manifest | `app/public/sf-assets/vehicles_manifest.json` |
| Model | `muni-bus-40` — the 40 ft rigid coach. **One GLB.** |
| Real vehicle | New Flyer Xcelsior XDE40, diesel-electric hybrid |
| Real dimensions | 12.19 m × 2.59 m × ~3.3 m |
| Triangle cap | 3,000 |
| Draw-call cost | **+1** permanent (one `InstancedMesh` per manifest entry) |
| Replaces | nothing; `commuter-bus.glb` stays as the generic non-Muni coach |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create production-ready Muni hybrid bus GLBs for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create one stylized miniature 3D model of San Francisco's 40-foot Muni hybrid
bus and deliver it as a downloadable, validated GLB.

Do not integrate or deploy the model yet. Create the asset, validate it, render
review images, run the shrink stage, and commit the deliverables to your working
branch.

**One model, not two.** The 60-foot articulated coach is deliberately out of
scope — see §2.16. Build the rigid bus only, but structure
`build_muni_bus.py` as reusable component functions so the articulated variant
(and the trolley coach, which shares this body) can be built from it later
without a rewrite.

## Read the project sources first

Before any research or modeling, read in this order:

1. `AGENTS.md`
2. `docs/styles/README.md`
3. `docs/styles/miniature-toy.md`
4. `.agents/skills/sf-asset-check/SKILL.md`
5. `docs/asset-plans/transit/README.md` — **the vehicle contract overrides,
   the draw-call and scale facts, and the shared shrink recipe. It wins over
   the asset-check skill wherever the two disagree about vehicles.**
6. `app/public/sf-assets/vehicles_manifest.json` and the existing GLBs in
   `app/public/sf-assets/vehicles/` — the contract you must match
7. `app/src/agents.js` — `loadVehicles()`, `mergeVehicle()`, and the instancing
   loop, so you understand exactly how your asset gets drawn
8. `docs/asset-plans/transit/muni-hybrid-bus.md` — this plan, whose dossier is
   your research starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` + the transit README govern the
technical contract, `AGENTS.md` governs repository rules.

## Must capture

- Modern New Flyer low-floor bus proportions
- Large dark windshield wrapping around the front
- White/silver body with the prominent red Muni stripe and graphics
- Black window band running along the sides
- Large rectangular side windows
- Front and rear passenger doors
- Digital amber route display above the windshield
- Small four-digit fleet numbers
- The Muni "worm" logo
- Large side mirrors
- Roof-mounted HVAC and electrical equipment

**Most important visual signature:** silver/white + red Muni livery + black
windows + big rectangular modern bus silhouette.

## Research the vehicles independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
model designation, the overall dimensions, the current livery, and the door
arrangement, and gather references covering:

- Front, rear and both side elevations
- Roof views (the app camera looks down — the roof is a primary surface here,
  not an afterthought)
- The window band and how it terminates at front and rear
- The exact geometry of the red livery sweep and where it sits on the body
- Destination sign appearance, typeface weight, and colour
- Day and night appearance, including which surfaces are lit

Prefer SFMTA and New Flyer publications, transit-agency fleet documents,
geolocated photography and aerial imagery. Never rely on a single photograph, a
single AI-generated image, or a single unsourced 3D model.

## Create a reference dossier

Write `artifacts/muni-bus/REFERENCE.md` containing: source links and what each
establishes; verified dimensions; the livery geometry; observations from all
four sides and above; the 3–5 strongest recognition cues; features to preserve;
features to simplify; uncertainties. Do not commit copyrighted full-resolution
imagery.

## Make your own design decisions

Follow the conversion process in `docs/styles/miniature-toy.md` §22. The
finished assets must be immediately recognizable as Muni buses, consistent from
all four sides and above, and premium handcrafted miniatures — not photoreal,
not voxel, not generic low-poly.

Two style points specific to this asset:

- **The livery does the work, not the geometry.** A city bus is a box. What
  makes it a *Muni* bus is the red sweep against white and the black window
  band. Get those three shapes right at 120 m and the model is done; add
  panel-line detail nobody will ever see and you have spent your triangle
  budget on nothing.
- **The roof is a primary surface.** From a 42° camera you see more roof than
  side. Design the HVAC pod, the electrical box and the roof hatches as a
  deliberate composition, not as greeblies.

## Scope of the exported asset

Export the bus body, wheels, mirrors, roof equipment and destination sign.

Do not include: passengers, drivers, bus stops, shelters, road surface, wires,
plinths, ground planes, cameras or lights. Temporary context may appear in
review renders but must not leak into the GLB.

## Technical asset contract — VEHICLE, not landmark

Follow `.agents/skills/sf-asset-check/SKILL.md` **with the vehicle overrides in
`docs/asset-plans/transit/README.md`**. The differences are not cosmetic:

- **Front faces `−Z` in Blender** (headlights and windshield at negative Z).
  `agents.js` applies `merged.rotateY(Math.PI)` at load; a bus authored to the
  landmark `−Y` convention will drive sideways through San Francisco.
- **Ground at `min y = 0`**, origin centred in the X/Z footprint.
- Real-world metres, applied transforms, no negative scales, outward normals.
- No image textures, no transparency, flat `Toy_*` colours.
- `_Glow` suffix only on night-glow surfaces (see the glow set below).
- No `Toy_body` — the fleet loader bakes material colours to vertex colours and
  does not support per-instance tint. Colour variation must be geometry-baked.
- No cameras, lights, animations, armatures or constraints.
- **≤ 3,000 triangles.**

## The night-glow set (new for vehicles — no shipped vehicle has one)

The loader puts `_Glow` materials in a separate unlit layer at
`opacity = 0.12 + 0.95 * uNight`. A `_Glow` surface is therefore **88%
transparent by day**, so it must never be a primary surface — author it as a
thin shell 3–5 cm proud of an opaque surface with its edges buried, exactly as
`artifacts/conservatory-of-flowers/` and the Grace Cathedral work established.

| Surface | Material | Reads as |
|---|---|---|
| Destination sign face | `Toy_mustard_Glow` | the single strongest "alive" cue |
| Headlight pair | `Toy_white_Glow` | front identification at distance |
| Tail lights | `Toy_red_Glow` | rear identification |
| Interior ceiling strip visible through the window band | `Toy_mustard_Glow` | a lit, occupied bus |

Ship emission at 0.0 per the contract — the app's glow layer drives it. Note the
known render gotcha: glTF `emissiveFactor` of (0,0,0) makes Blender's importer
default Emission Color to **white**, so a night preview that only raises Emission
Strength lights every glow surface white. Copy Base Color into Emission Color
before setting strength.

## The destination sign

Put a route number and destination on the front sign. This is the detail that
makes the fleet feel authentically Muni rather than generically municipal.

Author **at most three** sign variants, and pick routes that are genuinely
hybrid-bus (motor coach) lines, not trolleybus lines — getting this wrong is the
kind of error a San Franciscan notices immediately. Verify current assignments
against SFMTA route pages before committing: `38 GEARY`, `9 SAN BRUNO` and
`29 SUNSET` are strong candidates. Note that **49 VAN NESS is a trolley coach
line**, so it belongs on the trolley coach asset, not this one.

Implement the sign as extruded geometry on the `Toy_mustard_Glow` shell, not a
texture. Keep the glyphs chunky and few — at 120 m the sign reads as a lit amber
rectangle, and at 15 m the number should be legible. If three variants push past
the triangle budget, ship one and record why.

## Reproducible Blender workflow

Blender is headless: `blender -b --python script.py -- args`. No GPU, so use
Workbench or CPU Cycles. Blender 5.x removed `blend_method` — use
`surface_render_method`.

Keep `artifacts/muni-bus/build_muni_bus.py` (deterministic, written as reusable
component functions — body shell, window band, livery, doors, roof pod, wheels,
mirrors — because the trolley coach plan imports them and a future articulated
variant would extend them), `artifacts/muni-bus/muni-bus.blend`, and the
exported GLB.

Export via the leak-proof pattern: temp scene containing only the export
collection, `use_active_scene=True`, `export_apply=True`, then re-import and
verify object count, bbox and material set. Wrap exporter calls in
`contextlib.redirect_stdout` — its stdout floods tool responses.

## Required review renders

Render the exact final geometry from controlled cameras:

`muni-bus-40-front.png`, `-rear.png`, `-left.png`, `-right.png`, `-top.png`,
`-aerial.png`, `-night.png`, plus `muni-bus-contact-sheet.png`.

The four elevations must share scale, framing, lighting, exposure and
projection. The top view must clearly show the roof equipment composition. The
aerial uses the style bible's camera assumptions (42° down, long lens).

**Plus the scale test, which is mandatory and is where this asset most likely
fails:** render the bus at **1.6× scale** against real baked city geometry from
the app's diorama camera — the app applies `carScale = 1.6` to fleet instances,
so a 12.19 m coach renders at **19.5 m**. If it dominates the block, say so in
the report and propose the fix (shorten toward the low end of the real dimension
range, or recommend a per-type scale override at integration) rather than
quietly shipping it.

## Validate the exported GLBs

Re-import each GLB into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count,
dimensions, bbox min/max, **min y**, XZ centre offset, **front-face direction**,
material names, image-texture count, camera count, light count, animation count,
applied-transform status, negative-scale status, per-object signed volume, and
per-material contract compliance. Write `artifacts/muni-bus/validation.json` and
`artifacts/muni-bus/REPORT.md`.

## Shrink stage

Run the shrink and intake stages from `docs/asset-plans/transit/README.md`
Part 3 with `ASSET_CLASS=vehicle`, and record the before/after table plus every
gate result in `REPORT.md`. In particular: limited dissolve at **0.05°**, never
0.5°; never weld across a `_Glow` boundary; gltfpack flags `-cc -kn -km -noq`.

Do **not** run the high→low texture bake. It is out of scope for transit assets
and the reason is in the README.

## Manifest draft

Include these draft entries in `REPORT.md`. **Do not edit the production
manifest in this task.**

```json
{ "id": "muni-bus-40", "file": "vehicles/muni-bus-40.glb", "kind": "bus",
  "dims": [x, y, z], "tris": N, "weight": 3 }
```

Do not edit the production manifest. `weight` is set at integration, not here.

## Do not

- author to the landmark `−Y` front convention
- use `Toy_body` (the fleet loader does not tint per instance)
- add a texture, including for the destination sign
- ship a `_Glow` material as a primary surface
- delete or bypass `carArchetype()` — the procedural fallback is AGENTS rule 3
- edit `vehicles_manifest.json`, `app/src/agents.js` or any app code
- skip the 1.6× in-city scale render
````

---

## Part 2 — Research and design dossier

Compiled 12 August 2026 from the sources in 2.2. Values marked *inferred* are
visual or derived estimates, not published figures — the executing agent must
re-verify anything it relies on.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Rigid model | New Flyer Xcelsior **XDE40**, diesel-electric hybrid | Muni fleet roster |
| Rigid fleet numbers | 8601–8662, 8701–8780, 8751–8780, 8800–8969 (~312 buses, 2013–2019) | Muni fleet roster |
| Articulated model | New Flyer Xcelsior **XDE60** | Muni fleet roster |
| Articulated fleet numbers | 6500–6554, 6560–6697, 6700–6730 (~224 buses, 2015–2018) | Muni fleet roster |
| Rigid length | 12.19 m (40 ft) | New Flyer Xcelsior spec |
| Articulated length | 18.29 m (60 ft) | New Flyer Xcelsior spec |
| Width | 2.59 m (102 in) | New Flyer Xcelsior spec |
| Height | ~3.3 m to roof, ~3.4 m over HVAC | *inferred* from Xcelsior drawings |
| Floor | low-floor, no steps at front and centre doors | New Flyer product line |
| Propulsion | biodiesel-electric hybrid | SFMTA |
| Fleet numbers on body | four digits | roster ranges above |

### 2.2 Sources

- https://www.sfmta.com/muni-transit — the five-family taxonomy this set follows
- https://en.wikipedia.org/wiki/San_Francisco_Municipal_Railway_fleet — models, fleet number ranges, quantities, delivery years
- New Flyer Xcelsior product literature — dimensions, low-floor layout, door arrangement
- SFMTA route pages — current motor-coach vs trolley-coach line assignments (**verify before choosing destination signs**)

### 2.3 Orientation and placement

Vehicle contract: **front faces `−Z`**, ground at `min y = 0`, origin centred in
the X/Z footprint. `agents.js` rotates by π at load and drives the model down
`+Z`. There is no world-true orientation question here — unlike a landmark, a bus
is placed at a heading computed per-instance from the road path.

### 2.4 What each side shows

**Front** — The signature view. A large dark windshield wrapping around the
corners, the amber destination sign in a recessed hood above it, a white fascia
below with the red livery sweep rising into it, headlight clusters low and wide,
and two large mirrors on stalks projecting well beyond the body.

**Sides** — A continuous black window band at roughly two-thirds height,
interrupted by the front door (ahead of the front axle) and the centre door. The
red livery sweeps up from the skirt toward the rear. Fleet number small, near the
front. The Muni worm sits on the white field.

**Rear** — Mostly flat: engine access panels, a smaller window, tail-light
clusters, and the red livery wrapping around from the sides.

**Top** — Long white expanse with the HVAC pod forward of centre, an electrical
box, roof hatches, and the slight crown of the roofline. On a 42° camera this is
the surface the player sees most.

### 2.5 Recognition cues (ranked)

1. White body + red livery sweep + black window band — the three-shape read
2. Big rectangular modern bus silhouette with a wrapped dark windshield
3. Amber destination sign glowing above the windshield
5. Roof HVAC pod (the only thing that distinguishes the roof from a white slab)

### 2.6 Miniature translation

**Preserve**

- 12.19 m / 18.29 m lengths and 2.59 m width at real scale
- Low-floor proportion: the body sits low, the window band is high
- Door positions — they are what makes it read as a *bus* and not a truck
- The red livery's diagonal energy

**Simplify / exaggerate**

- Window band becomes one continuous chunky `Toy_ink` recess with `Toy_glass`
  panes, not individually modelled windows
- Mirrors exaggerated ~1.3× — at 1.6× render scale they still read as toy-model
  detail, and they are a strong bus cue
- HVAC pod becomes one chunky beveled box with a grille inset
- Wheels: 8-segment cylinders, deeply inset behind the skirt
- No panel lines, no rivets, no wiper geometry, no interior seating

### 2.7 Massing recipe

Build order for the deterministic script; a starting point, not a straitjacket.
Adjust after the first 1.6× in-city render.

1. **Body shell** — box 12.19 × 2.59 × 2.55 m, top at y 3.15, bottom at y 0.60,
   bevel 0.12 m / 2 segments. `Toy_white`.
2. **Skirt** — box inset 0.06 m per side from y 0.35 to 0.60, `Toy_steel`.
3. **Window band** — recess 0.05 m deep from y 1.85 to 2.75, `Toy_ink` reveal
   with `Toy_glass` panes set 0.02 m inside it.
4. **Windshield** — a single chamfered volume wrapping the front corners,
   `Toy_glass`, raked ~12° from vertical.
5. **Red livery** — a 0.02 m proud shell in `Toy_red` sweeping from the skirt at
   the rear up to the fascia at the front. Author as geometry, not a material
   split on a shared surface, so the shrink pass cannot dissolve it away.
6. **Doors** — two `Toy_ink` recesses with `Toy_glass`, front ahead of the front
   axle, centre just behind the midpoint.
7. **Destination sign** — recessed hood above the windshield; opaque
   `Toy_ink` backing plate with a `Toy_mustard_Glow` shell 0.04 m proud, extruded
   route glyphs on the shell.
8. **Roof pod** — HVAC box 3.2 × 2.1 × 0.35 m forward of centre, `Toy_white`
   with a `Toy_steel` grille inset; small electrical box behind it.
9. **Wheels** — 4 cylinders, radius 0.52 m, 8 segments,
   `Toy_tire` dark with a `Toy_steel` hub disc.
10. **Mirrors** — two stalks + heads at the front corners, `Toy_ink`.
11. **Lights** — `Toy_white_Glow` headlight pucks, `Toy_red_Glow` tail pucks,
    each a shell proud of an opaque `Toy_ink` housing.
(A future articulated variant duplicates the rear body section, separates it by
0.9 m, fills the gap with a ribbed bellows and carries the window band and red
livery across the joint — which is why steps 1–11 must be functions, not a
straight-line script.)

### 2.8 Materials and palette

Flat colours from the `sf-asset-check` palette. Off-palette entries are a WARN,
not a fail, and Muni red is worth the warn if `Toy_red` reads wrong.

| Material | Hex | Used for |
|---|---|---|
| `Toy_white` | `#f7f4ec` | body, roof, fascia |
| `Toy_red` | `#c4453c` | Muni livery sweep, worm logo |
| `Toy_ink` | `#3a3530` | window band reveal, door recesses, mirrors, light housings |
| `Toy_glass` | `#2a4d73` | windows, windshield, door glazing |
| `Toy_steel` | `#9aa0a6` | skirt, wheel hubs, HVAC grille |
| `Toy_tire` | *off-palette, ~#242428* | tyres (WARN — record it) |
| `Toy_mustard_Glow` | `#d9a441` | destination sign face |
| `Toy_white_Glow` | `#f7f4ec` | headlights |
| `Toy_red_Glow` | `#c4453c` | tail lights |
| `Toy_mustard_Glow` | `#d9a441` | interior ceiling strip behind the window band |

### 2.9 Top surface

From the app's 42° camera the roof is roughly as visible as the sides and much
more visible than the front. Design it: HVAC pod forward of centre, a smaller
electrical box behind it, two flush hatches, and a subtle roofline crown so the
white does not read as a flat sticker. Keep the roof slightly off-white against
the body white so the two planes separate under the diorama's flat lighting.

### 2.10 Scope

**In the GLB:** body, wheels, mirrors, roof equipment, destination sign, lights

**Not in the GLB:** passengers, driver, bus stops, shelters, road surface,
overhead wires, ground plane, plinth, cameras, lights

### 2.11 Triangle budget

Cap 3,000. Suggested split: body + livery 1,000 · glazing 500 · wheels 500 ·
roof 400 · sign + lights 300 · mirrors 300.

Comfortably under the shipped fleet's 4,888–9,688, deliberately: buses are the
first of ~13 planned transit types, and the whole set has to fit inside a
triangle budget that already sees 22–26M tris at hero night.

### 2.12 Draft manifest entries

```json
{ "id": "muni-bus-40", "file": "vehicles/muni-bus-40.glb", "kind": "bus",
  "dims": [x, y, z], "tris": N, "weight": 3 }
```

`dims` and `tris` are placeholders until built and validated.

### 2.13 Integration notes — deferred

Placement, spawning, weighting and live Muni data are **out of scope for this
task** and are parked in
[`docs/asset-plans/transit/INTEGRATION-LATER.md`](./INTEGRATION-LATER.md).

What this task owes the follow-up is only the draft manifest entry in
`REPORT.md`, and anything the renders revealed about how the vehicle behaves at
1.6× scale in the real city — that evidence is what the integration decisions
will be made from.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of each exported GLB (never validate the authoring scene)
- [ ] **Front faces `−Z`**; `min y` within 0.05 m of 0; XZ centre offset within 0.1 m
- [ ] Dimensions match 2.1 in real metres
- [ ] Triangles at or under 3,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on sign, headlights, tail lights, interior strip — and each is
      a proud shell, not a primary surface
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, per-object signed volume positive
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Day **and** night renders; elevations + top + aerial + contact sheet
- [ ] **1.6× in-city scale render against real baked geometry**
- [ ] Shrink stage run, gates recorded, meshopt intake applied with `-cc -kn -km -noq`
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

- **The 1.6× scale problem** puts this coach on screen at 19.5 m. That is the
  friendliest length in the transit set, but still check it against real block
  geometry.
- **Destination sign routes must be verified as motor-coach lines.** `49 VAN NESS`
  appears in the original brief but is a trolley coach line — it belongs on the
  trolley coach asset. Route assignments shift; check SFMTA before committing
  glyphs to geometry.
- **Muni red vs `Toy_red`.** The palette's `#c4453c` is a warm brick red. If it
  reads wrong against `Toy_white`, take the off-palette WARN and record it —
  the livery is the entire identity of this asset.
- **Extruded sign glyphs are a triangle trap.** Three variants × a legible route
  number can eat 400+ triangles. Budget them first, not last.
- The bus and the trolley coach share a body. Build this one so the trolley
  coach plan can import its component functions rather than fork them.

### 2.16 The deferred 60-foot articulated variant

Not in scope. The 511 SIRI feed resolves vehicle **mode** from `LineRef`, and
mode is what these five plans model — one GLB per Muni fleet family. Rigid
versus articulated is not a mode distinction, so it is not required to render
the feed faithfully.

The research is kept here because the variant is cheap to add later and the data
would support it:

| Item | Value |
|---|---|
| Model | New Flyer Xcelsior **XDE60** |
| Fleet numbers | 6500–6554, 6560–6697, 6700–6730 (~224 buses, 2015–2018) |
| Length | 18.29 m (60 ft); same 2.59 m width and ~3.3 m height |
| Build | the rigid body plus a second rear section, a 0.9 m ribbed bellows, and 6 wheels |
| Triangle cap | 4,200 |

Two things to know if it is ever picked up. **The feed can drive it:** SIRI
returns `VehicleRef`, which is the real fleet number, and Muni's number ranges
are blocked by model — 8601–8969 is XDE40, 6500–6730 is XDE60 — so a lookup
table would pick the right GLB per vehicle with no guessing. **And the reason it
was cut is scale:** at `carScale = 1.6` a 60-footer renders at 29.3 m, most of a
Sunset block, which made it the riskiest asset in the set.
