# Cable car — SF-SIM asset plan

The strongest "this is San Francisco" signal in the entire simulation after the
Golden Gate Bridge, and the only vehicle in the set that deserves a landmark's
attention rather than a vehicle's. A tiny 19th-century wooden box, open at the
sides, with people standing on the running boards, hauled up an absurd hill by a
cable in a slot in the street.

**Deliverable:** one validated miniature GLB plus dossier, renders and report
under `artifacts/cable-car/`. Part 1 is the runnable task prompt, Part 2 the
dossier, Part 3 the shrink stage.

| | |
|---|---|
| Slug | `cable-car` |
| Manifest | `app/public/sf-assets/vehicles_manifest.json` |
| Model | `cable-car-powell` — the single-ended Powell car. **One GLB.** |
| Real dimensions | 8.4 m × 2.4 m |
| Triangle cap | **6,000** — deliberately the highest in the transit set |
| Draw-call cost | **+1** permanent |
| System | 3 lines, 40 cars, National Historic Landmark, operating since 1873 |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create production-ready San Francisco cable car GLBs for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create one stylized miniature 3D model of San Francisco's single-ended Powell
Street cable car and deliver it as a downloadable, validated GLB.

Do not integrate or deploy the model yet. There is no rail network in the app —
this task produces the vehicle only.

**One model, not two.** The double-ended California Street car is deliberately
out of scope — see §2.16.

**Scope note, read before budgeting your effort:** this asset gets a higher
triangle budget and more attention than anything else in the transit set, on
purpose. Alongside the Golden Gate Bridge, the cable car is one of the two
strongest San Francisco signals in the whole model. Treat it as a landmark that
happens to move.

## Read the project sources first

1. `AGENTS.md`
2. `docs/styles/README.md`
3. `docs/styles/miniature-toy.md`
4. `.agents/skills/sf-asset-check/SKILL.md`
5. `docs/asset-plans/transit/README.md` — vehicle contract overrides, draw-call
   and scale facts, the shared shrink recipe, and the **no-rails-no-wires
   decision**
6. `app/public/sf-assets/vehicles_manifest.json` and the existing GLBs in
   `app/public/sf-assets/vehicles/` — the contract you must match
7. `app/src/agents.js` — `loadVehicles()`, `mergeVehicle()`, the instancing loop
8. `artifacts/palace-of-fine-arts/` or `artifacts/grace-cathedral/` — for how a
   high-detail asset's build script, validator and render passes are structured
9. `docs/asset-plans/transit/cable-car.md` — this plan

## Must capture

- Small, boxy 19th-century wooden vehicle
- **Open-air passenger sections**
- **Exposed running boards along the sides where riders stand**
- Vertical poles and handrails
- Wood-panelled body with decorative trim
- Destination boards
- Brass hardware
- Compact wheelbase
- **The gripman standing at the controls** — standing, not seated

Cable cars are pulled by a continuously moving underground cable, not an onboard
motor. There is no engine, no exhaust, no pantograph and no trolley pole. The
grip mechanism reaching down toward the street is the mechanical story — though
note that there is no cable slot in this scene (see the transit README), so the
grip reads as a lever and a housing rather than as something visibly engaged.

**The Powell car:** classic burgundy/red + cream, open sections at both ends,
single-ended (turned on a turntable at each terminus). It covers two of the three
lines — Powell–Mason and Powell–Hyde — and 28 of the system's 40 cars.

**Most important visual signature:** tiny vintage wooden car + open sides +
people hanging onto exterior poles + an extremely steep street.

## Riders and gripman are part of the asset

This is the exception to the usual "no people in the GLB" rule, and it is
deliberate. A cable car without riders on the running boards is not a cable car —
it is a small wooden shed. Bake in:

- A gripman **standing** at the grip lever
- A conductor at the rear on a Powell car
- 4–8 riders: some seated on the open-section benches, at least three standing on
  the running boards holding the vertical poles

Model them as chunky toy figures in the established style — see the people
clusters in `artifacts/` landmark work for the existing figure vocabulary and
the `Toy_p_*` saturated palette. They are silhouette, not portraiture: no faces,
no fingers.

Because they are baked geometry, every instance of the car carries the same
riders. That is acceptable for a vehicle seen from 42° at distance and is far
cheaper than any alternative. Keep them cheap — see the triangle budget.

## Research the vehicles independently

Verify the dossier rather than trusting it. Re-check dimensions and the livery,
and gather references covering:

- Front, rear, both sides, and **roof views**
- The open end sections: bench arrangement, roof support posts, grab poles
- The running boards and their height above the street
- The grip lever and brake levers at the gripman's position
- The destination boards and where they mount
- The clerestory or monitor roof profile, if present
- Decorative trim, lettering, and the gold/brass detailing
- Day and night appearance
- Riders standing on running boards — for correct posture and spacing
- The wheel and truck arrangement (there is no track in this scene, but the
  trucks still have to look right where they meet the street)

Prefer SFMTA, the Cable Car Museum, historic-registry documentation, geolocated
photography and aerial imagery. Never rely on a single photograph, a single
AI-generated image, or a single unsourced 3D model.

## Create a reference dossier

Write `artifacts/cable-car/REFERENCE.md`: source links and what each establishes,
verified dimensions, livery specification, observations from all sides and above,
the 3–5 strongest recognition cues, features to preserve and simplify,
uncertainties. No copyrighted full-resolution imagery.

## Make your own design decisions

Follow `docs/styles/miniature-toy.md` §22. Four points specific to this asset:

- **Openness is the silhouette.** Every other vehicle in this city is a closed
  box. The cable car's identity is that you can see through it — the open end
  sections, the gaps between roof posts, the void where a wall should be. Protect
  that at every simplification step. A cable car that has closed up into a solid
  box has failed completely, no matter how good its trim is.
- **Riders complete the shape.** The figures on the running boards are not
  decoration; they extend the silhouette outward and are half of what makes the
  vehicle readable at distance.
- **The steepness is not yours to model, but it is yours to design for.** The car
  will be seen on a 20%+ grade. Check that the roofline, running boards and
  figures still read when the whole vehicle is pitched — render it tilted.
- **Trim is where the budget goes.** This is a Victorian object. The beveled
  panel lines, the arched window tops, the roof edge moulding and the gold
  lettering are what separate it from a shipping crate. This is why the cap is
  6,000 and not 3,000.

## Scope of the exported asset

Export the car body, roof, open end sections, running boards, grab poles,
handrails, wheels, the grip and brake levers, destination boards, and the baked
gripman, conductor and riders.

Do not include: rails, the cable slot, the street surface, the turntable,
overhead wires, buildings, ground plane, plinth, cameras or lights. None of that
track infrastructure exists in this scene — see the transit README.

## Technical asset contract — VEHICLE, not landmark

Follow `.agents/skills/sf-asset-check/SKILL.md` with the vehicle overrides in
`docs/asset-plans/transit/README.md`:

- **Front faces `−Z` in Blender** — the gripman's end.
- **Ground at `min y = 0`** — the wheel contact patch sits on the **street
  surface**, exactly like a bus. There are no rails in this scene, so there is no
  top-of-rail question.
- Origin centred in the X/Z footprint
- Real metres, applied transforms, no negative scales, outward normals
- No textures, no transparency, flat `Toy_*` colours
- `_Glow` only on night surfaces; no `Toy_body`; no cameras, lights, animation,
  armatures or constraints
- **≤ 6,000 triangles**

**Open geometry is a validation hazard.** The signed-volume gate assumes closed
solids, and an open-sided vehicle full of poles and figures will produce
open-shell objects. Every individual object must still be a closed solid — model
a grab pole as a capped cylinder, a bench as a closed box, a rider as a closed
figure. The *vehicle* is open; each *object* is closed. Getting this wrong is the
most likely validation failure on this asset.

## The night-glow set

The loader puts `_Glow` materials in a separate unlit layer at
`opacity = 0.12 + 0.95 * uNight` — a glow surface is **88% transparent by day**,
so author each as a thin shell 3–5 cm proud of an opaque surface with buried edges.

| Surface | Material | Reads as |
|---|---|---|
| Interior ceiling of the enclosed section | `Toy_mustard_Glow` | a warm lit cabin, visible straight through the open sides |
| Headlamp | `Toy_white_Glow` | the single forward lamp |
| Destination board face | `Toy_mustard_Glow` | line identification |

The lit interior is the highest-value glow surface in the entire transit set,
precisely because the car is open — at night you see the warm light through the
vehicle rather than reflected off it. Design for that.

## Reproducible Blender workflow

Blender headless: `blender -b --python script.py -- args`. No GPU — Workbench or
CPU Cycles. Blender 5.x uses `surface_render_method`, not `blend_method`.

Keep `artifacts/cable-car/build_cable_car.py` (deterministic, written as
reusable component functions — trucks, poles, benches, trim vocabulary, figures —
because a future California car shares all of them),
`artifacts/cable-car/cable-car.blend`, and the exported GLB.

Leak-proof export: temp scene with only the export collection,
`use_active_scene=True`, `export_apply=True`, re-import and verify object count,
bbox and material set. Wrap exporter calls in `contextlib.redirect_stdout`.

## Required review renders

`cable-car-powell-front.png`, `-rear.png`, `-left.png`, `-right.png`,
`-top.png`, `-aerial.png`, `-night.png`, plus a contact sheet.

**Plus three mandatory extra renders:**

1. **1.6× in-city scale test** against real baked city geometry. At 1.6× a Powell
   car renders at 13.4 m — the friendliest scale in the transit set, and one of
   the few places where the exaggeration helps rather than hurts. Confirm it.
2. **Tilted render at 20% grade** from the app camera, which is how this vehicle
   will actually be seen on Hyde or Powell. Verify the riders, running boards and
   roofline still read when pitched.
3. **Backlit render** proving the open sections read as open — the car
   silhouetted against a bright background, from the app's 42° camera. If the
   openness does not survive at 120 m, the model has lost its identity and the
   posts and voids need exaggerating.

## Validate the exported GLBs

Fresh-scene re-import of each. Report object count, triangle count, dimensions,
bbox min/max, **min y and what it represents**, XZ centre offset, **front-face
direction**, material names, texture/camera/light/animation counts, applied
transforms, negative scales, **per-object signed volume (expect this to be the
hard gate)**, per-material compliance. Write `artifacts/cable-car/validation.json`
and `REPORT.md`.

## Shrink stage

Run the shrink and intake stages from `docs/asset-plans/transit/README.md`
Part 3 with `ASSET_CLASS=vehicle`. Record before/after and every gate in
`REPORT.md`. Limited dissolve at **0.05°**; never weld across a `_Glow`
boundary; gltfpack `-cc -kn -km -noq`.

**Two shrink-stage cautions specific to this asset:**

- The interior-face deletion step assumes solids enclosed by other solids. On an
  open vehicle almost nothing is enclosed, so this step should find very little.
  If it reports large savings, it is deleting faces that are genuinely visible
  through the open sides — stop and investigate.
- The join-by-material step will merge all the grab poles into one mesh. That is
  correct and desirable, but verify the poles survive the subsequent retessellation
  step: they are thin cylinders and halving their segments will square them off.

Do not run the high→low texture bake.

## Manifest draft

```json
{ "id": "cable-car-powell", "file": "vehicles/cable-car-powell.glb", "kind": "cable-car",
  "dims": [x, y, z], "targetLengthM": 8.4, "front": "-Z",
  "tris": N, "weight": 1,
  "notes": "Single-ended Powell car. No rails or cable slot in the scene." }
```

Do not edit the production manifest. `weight` is set at integration, not here.

Do not edit the production manifest.

## Do not

- close up the open sections to simplify the model
- omit the riders and gripman
- author to the landmark `−Y` front convention
- include rails, the cable slot or the street surface in the GLB
- use `Toy_body`, add textures, or ship a `_Glow` primary surface
- give either entry a non-zero `weight`
- edit `vehicles_manifest.json` or any app code
- skip the tilted and backlit renders
````

---

## Part 2 — Research and design dossier

Compiled 12 August 2026. Values marked *inferred* are visual or derived
estimates — re-verify anything you rely on.

### 2.1 Verified facts

| Item | Powell (single-ended) | California (double-ended) | Source |
|---|---|---|---|
| Length | 8.4 m (27 ft 6 in) | 9.2 m (30 ft 3 in) | SF cable car system |
| Width | 2.4 m (8 ft) | 2.4 m (8 ft) | SF cable car system |
| Weight | 7,000 kg (15,500 lb) | 7,600 kg (16,800 lb) | SF cable car system |
| Capacity | 60 total / 29 seated | 68 total / 34 seated | SF cable car system |
| Fleet | 28 cars | 12 cars | SF cable car system |
| Height | ~3.1 m to roof | ~3.1 m | *inferred* — verify |
| Livery | burgundy/maroon + cream | *verify — differs from Powell* | *inferred* |

System facts:

| Item | Value | Source |
|---|---|---|
| Track gauge | **1,067 mm (3 ft 6 in) narrow gauge** | SF cable car system |
| Cable diameter | 3.2 cm (1.25 in) | SF cable car system |
| Cable speed | 15.3 km/h (9.5 mph) — constant | SF cable car system |
| Cable construction | six steel strands of 19 wires around a sisal core | SF cable car system |
| Lines | Powell–Mason, Powell–Hyde, California Street | SF cable car system |
| System dates from | 1873; National Historic Landmark | SFMTA |

The gauge figure matters only for **wheel spacing on the model itself** — there
is no track in this scene. It is worth honouring anyway: at 1,067 mm the cable
car's wheels sit visibly narrower than the Metro's 1,435 mm, and the narrow
track is part of why the car reads as small and old.

### 2.2 Sources

- https://www.sfmta.com/muni-transit — the family taxonomy, 1873, National Historic Landmark
- https://en.wikipedia.org/wiki/San_Francisco_cable_car_system — dimensions, weights, capacities, fleet counts, gauge, cable spec, lines
- San Francisco Cable Car Museum — grip mechanism, car construction, livery
- Historic-registry documentation — car types and their differences

### 2.3 Orientation and placement

Vehicle contract: nominal front `−Z`, origin centred in X/Z, `min y = 0` at the
**street surface**, identical to the buses — there are no rails in this scene.

The California car is genuinely double-ended: a grip and an open section at both
ends, no turntable. Pick one end as `−Z`, verify symmetry, and note that a
runtime may drive it in either direction without rotating it.

### 2.4 What each side shows

**Front** — An open end section: a roof carried on slim posts over a
transverse bench, with the gripman standing at the grip lever behind it. A single
headlamp. The destination board above. You can see straight through to the
enclosed cabin behind.

**Sides** — The enclosed centre cabin with arched-top windows and
panelled wood below, flanked by open sections. A running board runs the full
length at roughly knee height above the street, with grab poles rising from it
to the roof edge. Gold lettering on the panel below the windows.

**Rear** — A second open section with the conductor's position, closed at the
very end.

**Top** — A simple gently-crowned roof with edge moulding, roof-support posts
meeting it at the open ends, and the destination boards standing proud at each
end. Possibly a clerestory/monitor strip — verify. Small, but on a 42° camera
this is a fully visible surface and it must not be a blank slab.

### 2.5 Recognition cues (ranked)

1. **Openness** — you can see through the ends of the vehicle
2. Riders standing on the running boards, holding the poles
3. Tiny burgundy-and-cream wooden box, far smaller than any other vehicle
4. The roof carried on slim posts over the open sections
5. The gripman standing upright at the controls

### 2.6 Miniature translation

**Preserve**

- 8.4 m length at real scale — the smallness *is* the character
- The open end sections and the see-through silhouette
- Running boards and grab poles at the correct heights
- Standing figures on the boards

**Simplify / exaggerate**

- Window arches become a simple chamfered top on each opening
- Panel trim becomes 2–3 beveled horizontal reveals, not individual mouldings
- The grip mechanism becomes a lever and a simple housing; nothing below the
  floor line is visible once the car is on embedded track
- Brass hardware becomes `Toy_gold` accents on the lever, lamp bezel and roof
  edge — no modelled fittings
- Figures are chunky toy silhouettes: no faces, no fingers, ~40–60 triangles each
- **Grab poles thickened** past scale so they read at 120 m; they are what make
  the open sections read as open rather than as holes

### 2.7 Massing recipe

Build order for the deterministic script; a starting point, adjust after the
backlit and tilted renders.

1. **Underframe** — box 8.4 × 2.4 × 0.35 m, top at y 0.75, `Toy_ink`.
2. **Trucks and wheels** — two trucks, 4 wheels total, radius 0.28 m, 8 segments,
   `Toy_ink`, gauge **1.067 m** between wheel centres.
3. **Enclosed cabin** — box 4.2 × 2.2 × 1.9 m sitting on the underframe,
   `Toy_brick` (burgundy) below the window line, `Toy_cream` above; bevel 0.10 m
   / 2 segments.
4. **Windows** — 4 bays per side, chamfered-top openings, `Toy_glass` panes inset
   0.04 m in `Toy_ink` reveals.
5. **Open end sections** — 2.0 m long at each end. Floor continues from the
   underframe; **no walls**. Transverse bench, `Toy_brick`.
6. **Roof posts** — 4 per open section, 0.09 m square (exaggerated), `Toy_cream`,
   carrying the roof over the open ends.
7. **Roof** — 8.4 × 2.4 m, gently crowned, `Toy_roofd`, with a `Toy_gold` edge
   moulding strip 0.06 m proud.
8. **Running boards** — 0.30 m deep strips at y 0.62 along both flanks, full
   length, `Toy_ink`.
9. **Grab poles** — 6 per side, radius 0.045 m (exaggerated from ~0.02 m),
   running board to roof edge, `Toy_gold`.
10. **Grip and brake levers** — two `Toy_steel` levers on a low `Toy_ink`
    housing at the gripman's position.
11. **Destination boards** — flat plates above each end, opaque `Toy_ink` backing
    with a `Toy_mustard_Glow` shell 0.03 m proud and extruded line lettering.
12. **Headlamp** — `Toy_gold` bezel with a `Toy_white_Glow` lens shell.
13. **Lettering** — extruded `Toy_gold` text on the cabin panel below the windows.
14. **Figures** — gripman standing at the levers; conductor at the rear;
    3 riders standing on the running boards holding poles; 3–4 seated on the open
    benches. `Toy_p_*` saturated palette. Every figure a closed solid.

### 2.8 Materials and palette

| Material | Hex | Used for |
|---|---|---|
| `Toy_brick` | `#c96f4a` | body panels below the window line (burgundy read) |
| `Toy_cream` | `#f2ede3` | upper body, roof posts |
| `Toy_ink` | `#3a3530` | underframe, trucks, wheels, running boards, window reveals, lever housing |
| `Toy_glass` | `#2a4d73` | cabin windows |
| `Toy_gold` | `#caa64a` | grab poles, roof edge moulding, lettering, lamp bezel |
| `Toy_steel` | `#9aa0a6` | grip and brake levers |
| `Toy_roofd` | `#45454a` | roof surface |
| `Toy_p_*` | saturated | figures — reuse the established landmark figure palette |
| `Toy_mustard_Glow` | `#d9a441` | cabin ceiling strip, destination board faces |
| `Toy_white_Glow` | `#f7f4ec` | headlamp lens |

`Toy_brick` at `#c96f4a` is warmer and lighter than true cable car maroon. If it
does not read, take the off-palette WARN and record it — the livery is a
substantial part of this asset's identity and is worth the warning.

### 2.9 Top surface

Small but fully visible from the 42° camera, and easy to neglect. Design it: a
gently crowned roof plane, a proud `Toy_gold` edge moulding running the
perimeter, the roof posts meeting it at the open ends, and the destination boards
standing above each end. Verify whether the real cars carry a clerestory or
monitor strip — if so, it is the roof's only interesting feature and worth
modelling.

### 2.10 Scope

**In the GLB:** body, roof, open end sections, running boards, grab poles,
handrails, trucks and wheels, grip and brake levers, destination boards, headlamp,
lettering, gripman, conductor and riders

**Not in the GLB:** rails, cable slot, street surface, turntable, buildings,
ground plane, plinth, cameras, lights

### 2.11 Triangle budget

Cap 6,000 — the highest in the transit set, justified by the directive that this
family deserves disproportionate detail.

Suggested split: cabin body and trim 1,400 · windows and glazing 700 · roof and
moulding 500 · open sections, posts and benches 800 · running boards and grab
poles 700 · trucks and wheels 500 · grip, levers, lamp, boards, lettering 500 ·
**figures 700** (≈ 8 figures at 50–90 tris each) · spare 200.

Note that 700 triangles of people is a real cost and a deliberate one. If the
budget binds, cut trim detail before cutting riders — the figures are load-bearing
for recognition and the trim is not.

### 2.12 Draft manifest entries

```json
{ "id": "cable-car-powell", "file": "vehicles/cable-car-powell.glb", "kind": "cable-car",
  "dims": [x, y, z], "targetLengthM": 8.4, "front": "-Z",
  "tris": N, "weight": 1 }
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

- [ ] Fresh-scene re-import of each exported GLB
- [ ] **Front faces `−Z`**; `min y` within 0.05 m of 0; XZ centre offset within 0.1 m
- [ ] Wheel gauge is **1.067 m**, not 1.435 m
- [ ] Dimensions match 2.1 in real metres
- [ ] Triangles at or under 6,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on cabin ceiling, destination boards, headlamp — proud shells
- [ ] **Per-object signed volume positive — every pole, bench and figure a closed
      solid**, even though the vehicle as a whole is open
- [ ] No cameras, lights, animations, armatures, constraints; no leaked geometry
- [ ] Gripman is standing; at least three riders on the running boards
- [ ] Day and night renders; elevations + top + aerial + contact sheet
- [ ] **1.6× in-city scale render**
- [ ] **Tilted 20% grade render**
- [ ] **Backlit render proving the open sections read at 120 m**
- [ ] Shrink stage run; interior-face step audited for over-deletion; gates recorded
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

- **Closing up is the failure mode.** Every simplification pass, every shrink
  step and every triangle-budget squeeze pushes this model toward a solid box.
  The backlit render exists specifically to catch that, and it is not optional.
- **The signed-volume gate will fight this asset.** An open vehicle made of many
  small closed solids is exactly the shape that produces open-shell objects if
  built carelessly. Model every component closed from the start rather than
  fixing it at validation.
- **Figures at 1.6× scale.** Riders that read correctly at 1:1 become slightly
  cartoonish at 1.6×. Check them in the in-city render rather than the turntable.
- **Roof clerestory unconfirmed.** If present it is the roof's only feature; if
  absent the roof needs its moulding to carry the whole surface.
- **The no-rails decision costs this asset almost nothing.** Of the five
  families, the cable car is the one that reads completely on its own: a tiny
  open wooden car with people standing on the running boards is unmistakable with
  or without a slot in the street. The grip lever loses its visible purpose, but
  the grip is a small object and the silhouette carries the identity. This is
  therefore the highest-value asset in the set *and* one of the cheapest to get
  right — build it early.
- **What it does still need is the route whitelist.** The vehicle survives having
  no track; it does not survive appearing in the Outer Sunset. See §2.13.

### 2.16 The deferred California Street car

Not in scope. The 511 SIRI feed resolves vehicle **mode** from `LineRef`, and
both cable car types are the same mode — one cable car GLB renders all three
lines faithfully. The Powell car is the right single choice: it covers
Powell–Mason and Powell–Hyde, and 28 of the system's 40 cars.

Research kept for a later pass, because the car is genuinely different and should
never be a reskin:

| Item | Value |
|---|---|
| Type | **Double-ended** — a grip and an open section at both ends, no turntable |
| Length | 9.2 m (30 ft 3 in) versus the Powell's 8.4 m |
| Width | 2.4 m, same |
| Weight | 7,600 kg versus 7,000 kg |
| Capacity | 68 total / 34 seated versus 60 / 29 |
| Fleet | 12 cars, California Street line only |
| Livery | **unverified** — sources give dimensions but not colours per type; confirm before assuming it matches the Powell |

`LineRef` in the feed distinguishes the California line from the two Powell
lines, so the split could be driven from data with no guessing if it is ever
built. The build script's component functions (trucks, poles, benches, trim,
figures) are written to be reused for exactly that.
