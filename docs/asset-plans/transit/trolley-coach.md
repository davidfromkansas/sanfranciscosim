# Muni trolley coach — SF-SIM asset plan

The bus that is easily confused with the hybrid bus. The key is the roof: two
long poles angled back off the roof. Everything else is the same New Flyer
Xcelsior body, so this plan deliberately **imports the hybrid bus's component
functions rather than forking them** — the poles are the entire job.

**Deliverable:** one validated miniature GLB plus dossier, renders and report
under `artifacts/muni-trolley/`. Part 1 is the runnable task prompt, Part 2 the
research and design dossier, Part 3 the shrink stage.

| | |
|---|---|
| Slug | `muni-trolley` |
| Manifest | `app/public/sf-assets/vehicles_manifest.json` |
| Model | `muni-trolley-40` — the 40 ft rigid coach. **One GLB.** |
| Real vehicle | New Flyer Xcelsior XT40, electric trolleybus |
| Real dimensions | 12.19 m × 2.59 m × ~3.3 m body; poles reach ~5.5 m |
| Triangle cap | 3,400 |
| Draw-call cost | **+1** permanent |
| Depends on | **[muni-hybrid-bus.md](./muni-hybrid-bus.md) must be built first** |
| Poles | reach into empty sky — no wires in the scene, by owner decision. See §2.15 |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create production-ready Muni trolley coach GLBs for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create one stylized miniature 3D model of San Francisco's 40-foot Muni electric
trolley coach and deliver it as a downloadable, validated GLB.

Do not integrate or deploy the model yet.

**One model, not two.** The 60-foot articulated coach is deliberately out of
scope — see §2.16.

## Read the project sources first

1. `AGENTS.md`
2. `docs/styles/README.md`
3. `docs/styles/miniature-toy.md`
4. `.agents/skills/sf-asset-check/SKILL.md`
5. `docs/asset-plans/transit/README.md` — vehicle contract overrides, draw-call
   and scale facts, shared shrink recipe. **It wins over the asset-check skill
   wherever the two disagree about vehicles.**
6. `docs/asset-plans/transit/muni-hybrid-bus.md` and
   **`artifacts/muni-bus/build_muni_bus.py`** — the body you are reusing
7. `app/src/agents.js` — `loadVehicles()`, `mergeVehicle()`, the instancing loop
8. `docs/asset-plans/transit/trolley-coach.md` — this plan

**This asset must not be built from scratch.** `artifacts/muni-bus/` already
contains a deterministic build script whose component functions produce the
Xcelsior body, window band, livery, doors, roof pod, wheels and mirrors. Import
them. If they are not importable as written, refactor `build_muni_bus.py` into
shared functions and rebuild both assets from it — a diverged trolley body is a
bug, because in reality these two vehicles share a shell.

## Must capture

- Modern New Flyer bus body, essentially identical to the hybrid coach
- Silver/white + red Muni livery
- Dark window band
- Low-floor design
- Digital destination display
- Large windshield
- **Two long trolley poles extending from the roof, angled backward**

**Two poles are essential.** Unlike the Metro's single pantograph, a trolley
coach carries two thin individual poles running to two separate overhead wires.
That is the single most important modeling detail in this asset — it is the only
thing distinguishing it from the hybrid bus at any distance.

## Research the vehicles independently

Verify the dossier rather than trusting it. Re-check the model designation,
dimensions, current livery, and — most importantly — the **pole geometry**:
mounting base position on the roof, resting angle, extended angle, length,
and the shoe/harp at the tip. Gather references covering:

- Front, rear, both sides, and **roof views** (the poles live on the roof and
  the app camera looks down)
- The pole base assembly and its spring housing
- Poles in the running position vs stowed on the roof hooks
- Day and night appearance

## Create a reference dossier

Write `artifacts/muni-trolley/REFERENCE.md`: source links and what each
establishes, verified dimensions, pole geometry, the livery, observations from
all sides and above, recognition cues, features to preserve and simplify,
uncertainties. No copyrighted full-resolution imagery.

## Make your own design decisions

Follow `docs/styles/miniature-toy.md` §22. Three points specific to this asset:

- **The poles are the asset.** Everything else is a solved problem inherited from
  the bus. Spend your attention and a disproportionate share of the triangle
  budget on the poles, their bases, and the angle that reads as "connected to
  something overhead."
- **Semantic exaggeration applies.** A real trolley pole is a thin rod. At the
  app's camera a scale-accurate rod is a sub-pixel line that vanishes. Thicken
  them until they read from 120 m — the style bible explicitly sanctions
  exaggerating identity features, and this is the identity feature.
- **The poles must read as poles with no wire above them — permanently.** There
  are no overhead wires in this scene and there will not be (see the transit
  README's no-rails-no-wires decision). These coaches run with their poles
  reaching into empty air, and that is the shipped state, not a temporary gap.
  Design for it: angle the poles backward and slightly apart so the silhouette
  says "electric vehicle" rather than "broken antenna," and keep the pair
  visually coupled — two parallel poles read as equipment, two divergent ones
  read as damage.

## Scope of the exported asset

Export the coach body, wheels, mirrors, roof equipment, destination sign, and
**both trolley poles with their base assemblies and shoes**.

Do not include: overhead wires, wire hardware, poles-along-the-street,
passengers, driver, road surface, ground plane, plinth, cameras or lights. There
are no wires in this scene at all — and even if there were, a vehicle GLB
carrying its own wire segment would drag a floating wire around the city.

## Technical asset contract — VEHICLE, not landmark

Follow `.agents/skills/sf-asset-check/SKILL.md` with the vehicle overrides in
`docs/asset-plans/transit/README.md`:

- **Front faces `−Z` in Blender**; `agents.js` applies `rotateY(Math.PI)`
- **Ground at `min y = 0`**, origin centred in the X/Z footprint
- Real metres, applied transforms, no negative scales, outward normals
- No textures, no transparency, flat `Toy_*` colours
- `_Glow` only on night surfaces; no `Toy_body`; no cameras, lights, animation
- **≤ 3,400 triangles**

Note the bbox consequence of the poles: `min y = 0` is still the tyre contact
patch, but the model's height becomes ~5.5 m rather than ~3.4 m. That is correct
and intentional — record it in `REPORT.md` so nobody "fixes" it later.

## The night-glow set

Same as the hybrid bus (destination sign `Toy_mustard_Glow`, headlights
`Toy_white_Glow`, tail lights `Toy_red_Glow`, interior ceiling strip
`Toy_mustard_Glow`), authored as thin shells 3–5 cm proud of opaque surfaces —
the loader renders `_Glow` at `opacity = 0.12 + 0.95 * uNight`, so a glow
primary surface is 88% transparent by day.

Do **not** add a glow at the pole shoe. Real trolley shoes spark intermittently;
a permanently glowing shoe reads as a bug.

## The destination sign

Pick from genuine **trolley coach** lines — this is where the families differ and
where the detail pays off. `49 VAN NESS`, `1 CALIFORNIA`, `22 FILLMORE`,
`30 STOCKTON`, `14 MISSION` and `24 DIVISADERO` are historically trolleybus
routes. Verify current assignments against SFMTA before committing glyphs to
geometry — some lines have been temporarily converted to motor coach during
construction projects.

At most three variants, extruded geometry on the `Toy_mustard_Glow` shell, no
textures.

## Reproducible Blender workflow

Blender headless: `blender -b --python script.py -- args`. No GPU — Workbench or
CPU Cycles. Blender 5.x uses `surface_render_method`, not `blend_method`.

Keep `artifacts/muni-trolley/build_muni_trolley.py` (deterministic, **imports
the shared body functions from `artifacts/muni-bus/`**),
`artifacts/muni-trolley/muni-trolley.blend`, and the exported GLB.

Leak-proof export: temp scene with only the export collection,
`use_active_scene=True`, `export_apply=True`, re-import and verify object count,
bbox and material set. Wrap exporter calls in `contextlib.redirect_stdout`.

## Required review renders

`muni-trolley-40-front.png`, `-rear.png`, `-left.png`, `-right.png`,
`-top.png`, `-aerial.png`, `-night.png`, plus a contact sheet.

The top view matters more here than on any other transit asset — it is the view
that proves the two poles are two poles, correctly spaced for a two-wire
overhead.

**Plus two mandatory extra renders:**

1. **1.6× in-city scale test** against real baked city geometry from the diorama
   camera. The app applies `carScale = 1.6`, so the coach renders at 19.5 m and
   the poles reach ~8.8 m — taller than the two-storey housing it drives past.
   Judge whether that reads as charming or broken, and say which.
2. **A side-by-side against the hybrid bus** at the app camera distance. If a
   player cannot tell the two apart at 120 m, the poles are too thin and the
   asset has failed its one job.

## Validate the exported GLBs

Fresh-scene re-import of each GLB. Report object count, triangle count,
dimensions, bbox min/max, **min y**, XZ centre offset, **front-face direction**,
material names, texture/camera/light/animation counts, applied transforms,
negative scales, per-object signed volume, per-material compliance. Write
`artifacts/muni-trolley/validation.json` and `REPORT.md`.

Watch the signed-volume gate on the poles: thin swept cylinders are the most
likely objects in this asset to end up with inverted winding.

## Shrink stage

Run the shrink and intake stages from `docs/asset-plans/transit/README.md`
Part 3 with `ASSET_CLASS=vehicle`. Record the before/after table and every gate
in `REPORT.md`. Limited dissolve at **0.05°**; never weld across a `_Glow`
boundary; gltfpack `-cc -kn -km -noq`.

**Do not let the retessellation step thin the poles.** Step 4 of the shrink
recipe halves segment counts on curves whose chord error is sub-pixel — applied
naively to a deliberately-exaggerated pole it will undo the exaggeration. Exclude
the poles from that step and say so in the report.

Do not run the high→low texture bake.

## Manifest draft

```json
{ "id": "muni-trolley-40", "file": "vehicles/muni-trolley-40.glb", "kind": "trolleybus",
  "dims": [x, y, z], "tris": N, "weight": 3 }
```

Do not edit the production manifest. `weight` is set at integration, not here.

## Do not

- build the body from scratch instead of importing the bus components
- author to the landmark `−Y` front convention
- include overhead wires in the vehicle GLB
- use `Toy_body`, add textures, or ship a `_Glow` primary surface
- model scale-accurate hairline poles
- delete or bypass `carArchetype()`
- edit `vehicles_manifest.json` or any app code
````

---

## Part 2 — Research and design dossier

Compiled 12 August 2026. Values marked *inferred* are visual or derived
estimates — re-verify anything you rely on.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Rigid model | New Flyer Xcelsior **XT40** | Muni fleet roster |
| Rigid fleet numbers | 5701–5885 (185 coaches, 2017–2019) | Muni fleet roster |
| Articulated model | New Flyer Xcelsior **XT60** | Muni fleet roster |
| Articulated fleet numbers | 7201–7293 (93 coaches, 2015–2018) | Muni fleet roster |
| Body dimensions | identical to XDE40 / XDE60: 12.19 m / 18.29 m × 2.59 m | New Flyer Xcelsior spec |
| Power collection | **two** trolley poles to a two-wire overhead, 600 V DC | SFMTA |
| Off-wire capability | battery operation for short detours | SFMTA |
| Grade capability | 23% fully loaded | SFMTA |
| Pole length | ~6 m extended | *inferred* from photography |
| Wire height | ~5.5 m above street | *inferred* — verify |

### 2.2 Sources

- https://www.sfmta.com/muni-transit — the family taxonomy, off-wire and grade claims
- https://en.wikipedia.org/wiki/San_Francisco_Municipal_Railway_fleet — XT40/XT60 models, fleet numbers, quantities
- New Flyer Xcelsior trolleybus literature — body dimensions, pole assembly
- SFMTA route pages — current trolleybus line assignments (**verify before choosing signs**)

### 2.3 Orientation and placement

Identical to the hybrid bus: front `−Z`, ground `min y = 0`, origin centred in
X/Z. Heading is computed per-instance from the road path.

The poles introduce one new consideration: they are **not symmetric front-to-
back**. They mount near the rear of the roof and trail backward, so a coach
authored with poles trailing the wrong way looks wrong from every angle. Verify
against the `−Z` front convention explicitly and state it in `REPORT.md`.

### 2.4 What each side shows

**Front** — Indistinguishable from the hybrid bus: wrapped dark windshield, amber
sign, white fascia, red sweep, low wide headlights, big mirrors. The poles are
just visible above the roofline from a low angle and clearly visible from the
app's aerial one.

**Sides** — Same window band, doors and livery as the hybrid. The pole pair
projects up and back at roughly 25–35° from horizontal when running.

**Rear** — Same as the hybrid, plus the two poles converging overhead and, at
their tips, the shoe/harp assemblies.

**Top** — The differentiating view. Two pole bases side by side on a raised
plinth toward the rear of the roof, poles trailing back, plus the HVAC pod and
electrical boxes. The pole spacing must match a plausible two-wire spacing
(~0.6 m apart at the base, converging slightly toward the tips).

### 2.5 Recognition cues (ranked)

1. **Two thin poles angled backward off the roof** — nothing else in the city has this
2. Muni bus body: white + red sweep + black window band
3. Roof pole bases on their plinth, visible from the aerial camera
5. The absence of an exhaust or engine bay at the rear

### 2.6 Miniature translation

**Preserve**

- The shared Xcelsior body, unmodified from the hybrid bus asset
- Two poles, two bases, correct rearward mounting
- The backward trailing angle

**Simplify / exaggerate**

- **Poles thickened well past scale** — start at 3× real diameter and judge from
  120 m. This is the sanctioned semantic exaggeration and it is the whole asset.
- Pole shoes become a single chunky wedge; no harp wire detail
- Pole base springs become one beveled cylinder each
- Retractor rope omitted entirely — it will not read and it will not survive the
  shrink pass

### 2.7 Massing recipe

1. **Import the bus body** from `artifacts/muni-bus/build_muni_bus.py`:
   shell, skirt, window band, windshield, livery, doors, sign, roof pod, wheels,
   mirrors, lights. Do not re-derive any of it.
2. **Remove the hybrid's exhaust/engine detail** from the rear if the bus build
   added any — a trolley coach has none.
3. **Pole plinth** — low box 1.2 × 0.9 × 0.12 m on the roof, ~2.5 m forward of
   the rear face, `Toy_ink`.
4. **Pole bases** — two beveled cylinders, radius 0.14 m, height 0.25 m, centred
   0.6 m apart on the plinth, `Toy_steel`.
5. **Poles** — two tapered cylinders, base radius 0.09 m tapering to 0.06 m
   (exaggerated; real is ~0.03 m), length 6.0 m, 8 segments, angled 30° above
   horizontal and splayed ~4° apart, `Toy_steel`.
6. **Shoes** — chunky wedge 0.28 × 0.16 × 0.10 m at each tip, `Toy_ink`.
Bevel everything 0.12 m / 2 segments except the poles, which take 0.02 m / 1
segment so they stay crisp.

### 2.8 Materials and palette

Inherits the hybrid bus palette exactly. Additions:

| Material | Hex | Used for |
|---|---|---|
| `Toy_steel` | `#9aa0a6` | poles, pole bases (already in the bus palette) |
| `Toy_ink` | `#3a3530` | pole plinth, shoes (already in the bus palette) |

**No new materials.** If the trolley coach introduces a material the bus does not
have, the two assets have diverged and something is wrong.

### 2.9 Top surface

The most important top surface in the transit set, because the roof is where the
family identity lives. Composition from front to back: HVAC pod, electrical box,
hatches, then the pole plinth with its two bases and the poles trailing off the
rear edge. Keep the plinth dark against the white roof so it separates cleanly
under flat diorama lighting.

### 2.10 Scope

**In the GLB:** body, wheels, mirrors, roof equipment, destination sign, lights,
both poles with bases and shoes

**Not in the GLB:** overhead wires, span wires, wire hardware, trackside poles,
passengers, driver, road surface, ground plane, plinth, cameras, lights

### 2.11 Triangle budget

Cap 3,400: inherited bus body 3,000 · poles, bases and shoes 400.

If the inherited body comes in under its own cap, spend the surplus on the poles,
not on new body detail.

### 2.12 Draft manifest entries

```json
{ "id": "muni-trolley-40", "file": "vehicles/muni-trolley-40.glb", "kind": "trolleybus",
  "dims": [x, y, z], "tris": N, "weight": 3 }
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
- [ ] Poles trail **backward** relative to the `−Z` front
- [ ] Model height ~5.5 m (poles), recorded and explained in `REPORT.md`
- [ ] Body geometry identical to `artifacts/muni-bus/` output, not re-derived
- [ ] Material set identical to the hybrid bus's
- [ ] Triangles at or under 3,400
- [ ] `_Glow` only on sign, headlights, tail lights, interior strip — no shoe glow
- [ ] Per-object signed volume positive, **including both poles**
- [ ] No cameras, lights, animations, armatures, constraints; no leaked geometry
- [ ] Day and night renders; elevations + top + aerial + contact sheet
- [ ] **1.6× in-city scale render**
- [ ] **Side-by-side vs the hybrid bus at 120 m — the poles must read**
- [ ] Shrink stage run with poles excluded from retessellation; gates recorded
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

- **Pole thinness is the failure mode.** The whole asset exists to be
  distinguishable from the hybrid bus, and the distinguishing feature is two thin
  rods viewed from 120 m at a 42° angle. Err aggressively toward too thick, and
  judge only from the app camera.
- **The shrink pass will attack the poles.** Retessellation of low-error curves
  is exactly the optimisation that undoes deliberate exaggeration. Exclude them
  explicitly.
- **Poles into empty sky — the one genuine open question in this plan.** There
  will never be wires above them. Three options, in order of preference:

  1. **Ship the poles anyway (recommended).** A viewer reads "electric transit"
     from the poles themselves; the wire is inferred, not required. Toy dioramas
     abstract constantly and this is a mild abstraction.
  2. **Stow the poles on the roof hooks.** Physically correct for an off-wire
     coach, and Muni's current fleet genuinely runs off-wire on battery. But it
     flattens the roof silhouette and the coach becomes near-identical to the
     hybrid bus — which removes the reason for the asset to exist.
  3. **Drop the family.** If neither pole treatment reads well on screen, one
     bus covering both hybrid and trolley service is a defensible scene, saves a
     draw call, and loses little a player would name.

  **Decide this from the mandatory side-by-side render against the hybrid bus,
  not in the abstract.** The render exists precisely to answer this question, and
  it should be reviewed before the rest of the asset is polished.
- **`49 VAN NESS` was listed under the hybrid bus in the original brief** but is
  historically a trolleybus route — it belongs here. Verify current assignment;
  Van Ness BRT construction temporarily shifted some services to motor coach.
- **Two assets, one body.** If the bus plan changes after this one ships, both
  must be rebuilt from the shared script. Note the dependency in both reports.

### 2.16 The deferred 60-foot articulated variant

Not in scope, for the same reason as the hybrid bus: the 511 SIRI feed resolves
vehicle **mode** from `LineRef`, and rigid versus articulated is not a mode.

Research kept for a later pass:

| Item | Value |
|---|---|
| Model | New Flyer Xcelsior **XT60** |
| Fleet numbers | 7201–7293 (93 coaches, 2015–2018) |
| Length | 18.29 m (60 ft); same 2.59 m width |
| Build | the rigid coach plus a second rear section and bellows, with the pole assembly on the **rear** section |
| Triangle cap | 4,600 |

`VehicleRef` in the feed is the real fleet number and Muni's ranges are blocked
by model — 5701–5885 is XT40, 7201–7293 is XT60 — so a lookup table could pick
the right GLB per vehicle if the variant is ever built.
