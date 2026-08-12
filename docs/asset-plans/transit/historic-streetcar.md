# Historic streetcar (F Market & Wharves) — SF-SIM asset plan

The one family where there deliberately **should not be a single model**. Muni
runs a visually diverse heritage fleet on the F line, and the variety is the
feature: streamlined 1940s PCCs painted in the liveries of transit systems from
other cities, alongside boxy orange 1928 Peter Witt cars from Milan. Colourful
vintage railcars moving through an otherwise modern San Francisco.

This plan solves the variety problem **without** paying a draw call per livery.

**Deliverable:** one validated miniature GLB plus dossier, renders and report
under `artifacts/f-line/`. Part 1 is the runnable task prompt, Part 2 the
dossier, Part 3 the shrink stage.

| | |
|---|---|
| Slug | `f-line` |
| Manifest | `app/public/sf-assets/vehicles_manifest.json` |
| Model | `f-line-pcc` — one geometry, **3–5 liveries by per-instance tint**. **One GLB.** |
| Real vehicle | PCC streetcar, built 1946–48 |
| Real dimensions | 14.02–15.39 m × 2.54–2.74 m |
| Triangle cap | 4,000 |
| Draw-call cost | **+1** permanent (not +5 — see §2.6) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create production-ready F-line historic streetcar GLBs for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create one stylized miniature 3D model for San Francisco's F Market & Wharves
heritage line — a PCC streetcar, authored so a single geometry can carry 3–5
liveries by per-instance tint — and deliver it as a downloadable, validated GLB.

Do not integrate or deploy the model yet. There is no rail network in the app —
this task produces the vehicle only.

**One model, not two.** The 1928 Milan Peter Witt car is deliberately out of
scope — see §2.17.

## Read the project sources first

1. `AGENTS.md`
2. `docs/styles/README.md`
3. `docs/styles/miniature-toy.md`
4. `.agents/skills/sf-asset-check/SKILL.md`
5. `docs/asset-plans/transit/README.md` — vehicle contract overrides, the
   draw-call arithmetic, the shared shrink recipe, and the **no-rails-no-wires
   decision**
6. `app/src/kitfleet.js` — **read this carefully.** It implements per-instance
   tinting of a designated `Toy_body` material over a shared geometry, which is
   the mechanism this plan's PCC liveries depend on.
7. `app/src/agents.js` — `loadVehicles()`, `mergeVehicle()`, the instancing loop.
   Note that it does **not** currently implement `kitfleet.js`'s tinting.
8. `app/public/sf-assets/vehicles_manifest.json` and the existing GLBs in
   `app/public/sf-assets/vehicles/` — the contract you must match
9. `docs/asset-plans/transit/historic-streetcar.md` — this plan

## The livery problem, and how this plan solves it

Muni's PCC fleet is painted in the colours of past transit operators — the
"cities series" — and that variety is the whole point of the asset. The naive
implementation is one GLB per livery, but `agents.js` builds **one
`InstancedMesh` per manifest entry**, so five liveries would be five permanent
draw calls for one silhouette, against a 300-call city budget.

**Author one PCC geometry with the livery surfaces on a tintable material**,
exactly as the 207-piece building kit does. In `app/src/kitfleet.js` a material
named `Toy_body` is authored mid-neutral and multiplied per instance by a colour
from a palette table, so one geometry serves many colourways at one draw call.

This asset must therefore break one rule the other transit plans state:

- **The PCC car DOES use `Toy_body`**, on the panels that change between
  liveries. Everything that does not change between liveries — windows, roof,
  trucks, trolley pole, bumpers, headlight — uses ordinary fixed `Toy_*`
  materials so the tint cannot wash them out.
- Author `Toy_body` near-neutral (`#d8d3c8`, matching the kit's convention) so a
  multiply lands on the intended palette entry rather than a muddied version of it.

**This requires an integration-side change to `agents.js`** to port
`kitfleet.js`'s tinting into the vehicle fleet path. That is not your task —
but your asset is designed for it, and your `REPORT.md` must state the
dependency prominently.

**Fallback if tinting is rejected:** ship **three** baked-livery PCC GLBs, not
five, and say so in the report. Three draw calls is a defensible cost for the F
line's identity; five is not. Do not silently pick this path — it changes the
manifest and the draw-call budget, so surface it as a decision.

## Must capture

- Beautiful streamlined 1930s–50s shape
- Rounded nose
- Curved roof
- Large front windows
- **Single central headlight**
- Rows of rectangular side windows
- Metal bumpers
- **Trolley pole connecting to the overhead wire**

**Most important visual signature:** colourful vintage railcars travelling
through an otherwise modern San Francisco. The liveries carry that, which is why
the tinting design below is the centre of this plan rather than a detail of it.

## Research the vehicles independently

Verify the dossier rather than trusting it. Re-check dimensions, the SF fleet's
actual composition, and the livery set, and gather references covering:

- Front, rear, both sides, and **roof views**
- The PCC's compound nose curvature and how the roof crown meets it
- Window arrangement and count
- Door arrangement; whether the SF cars are single- or double-ended (the fleet
  contains both — decide which you are modelling and say so)
- The trolley pole: base position, resting angle, length, shoe
- Specific Muni PCC liveries with their colours, so the palette table is real
  rather than invented
- Day and night appearance

Prefer SFMTA, Market Street Railway, transit-museum documentation, geolocated
photography and aerial imagery. Never rely on a single photograph, a single
AI-generated image, or a single unsourced 3D model.

## Create a reference dossier

Write `artifacts/f-line/REFERENCE.md`: source links and what each establishes,
verified dimensions, **the specific liveries chosen with their source systems and
hex colours**, observations from all sides and above, recognition cues, features
to preserve and simplify, uncertainties. No copyrighted full-resolution imagery.

## Make your own design decisions

Follow `docs/styles/miniature-toy.md` §22. Three points specific to this asset:

- **Silhouette carries the era, colour carries the identity.** The rounded nose
  and curved roof say 1940s at any distance; the livery says which city.
- **The nose is the PCC.** A PCC with a flat front is just a tram. Spend the
  chamfer budget there.
- **Design the livery split for tinting.** Decide early which surfaces are
  `Toy_body` and which are fixed. A livery that needs three tinted colours cannot
  work with a single-colour instance tint — pick liveries that read with one
  body colour plus fixed cream/dark trim, and record any livery you rejected for
  that reason.

## Scope of the exported assets

Export the car body, roof, windows, doors, trucks and wheels, bumpers,
headlight, destination sign, and the trolley pole with its base and shoe.

Do not include: rails, sleepers, overhead wire, catenary poles, passengers,
driver, street surface, ground plane, plinth, cameras or lights.

## Technical asset contract — VEHICLE, not landmark

Follow `.agents/skills/sf-asset-check/SKILL.md` with the vehicle overrides in
`docs/asset-plans/transit/README.md`:

- **Front faces `−Z` in Blender.** If modelling a double-ended car, pick a
  nominal front and record the choice.
- **Ground at `min y = 0`** — the wheel contact patch = **top of rail**, not
  street level. State this in `REPORT.md`.
- Origin centred in the X/Z footprint
- Real metres, applied transforms, no negative scales, outward normals
- No textures, no transparency, flat `Toy_*` colours
- `_Glow` only on night surfaces
- **`Toy_body` allowed on the livery panels only** (this asset's exception,
  justified above).
- No cameras, lights, animations, armatures or constraints
- **≤ 4,000 triangles**

## The night-glow set

The loader puts `_Glow` materials in a separate unlit layer at
`opacity = 0.12 + 0.95 * uNight` — a glow surface is **88% transparent by day**,
so author each as a thin shell 3–5 cm proud of an opaque surface with buried
edges.

| Surface | Material | Reads as |
|---|---|---|
| Headlight lens | `Toy_white_Glow` | the PCC's single central lamp — a signature |
| Interior ceiling strip behind the window band | `Toy_mustard_Glow` | a warm lit vintage interior |
| Destination sign face | `Toy_mustard_Glow` | route board |
| Tail lights | `Toy_red_Glow` | rear identification |

Keep the interior glow warmer than the modern fleet's. These are incandescent-era
vehicles and the warmth is characterful.

## Reproducible Blender workflow

Blender headless: `blender -b --python script.py -- args`. No GPU — Workbench or
CPU Cycles. Blender 5.x uses `surface_render_method`, not `blend_method`.

Keep `artifacts/f-line/build_f_line.py` (deterministic, written as reusable
component functions — trucks, trolley pole, glazing pattern — because a future
Milan car shares all of them but not the body),
`artifacts/f-line/f-line.blend`, and the exported GLB.

Leak-proof export: temp scene with only the export collection,
`use_active_scene=True`, `export_apply=True`, re-import and verify object count,
bbox and material set. Wrap exporter calls in `contextlib.redirect_stdout`.

## Required review renders

`f-line-pcc-front.png`, `-rear.png`, `-left.png`, `-right.png`, `-top.png`,
`-aerial.png`, `-night.png`, plus a contact sheet.

**Plus two mandatory extra renders:**

1. **1.6× in-city scale test** against real baked city geometry on the Embarcadero
   or lower Market. At 1.6× a PCC renders at ~23 m.
2. **The livery sheet** — the PCC rendered with every proposed tint applied, as
   one contact sheet, from the app camera. This proves the tinting design works
   before anyone writes the `agents.js` change. If a livery reads muddy or the
   fixed trim fights the body colour, this render is where you find out.
## Validate the exported GLBs

Fresh-scene re-import of each. Report object count, triangle count, dimensions,
bbox min/max, **min y and what it represents**, XZ centre offset, **front-face
direction**, material names (**confirm `Toy_body` is present and separately
addressable**), texture/camera/light/
animation counts, applied transforms, negative scales, per-object signed volume,
per-material compliance. Write `artifacts/f-line/validation.json` and `REPORT.md`.

## Shrink stage

Run the shrink and intake stages from `docs/asset-plans/transit/README.md`
Part 3 with `ASSET_CLASS=vehicle`. Record before/after and every gate in
`REPORT.md`. Limited dissolve at **0.05°** — critical here, because the PCC nose
is a curved shell and 0.5° dissolve on curved shells builds twisted ngons that
re-triangulate with flipped windings. Never weld across a `_Glow` boundary.
gltfpack `-cc -kn -km -noq`.

**Critical for this asset:** the join-by-material step must **not** merge
`Toy_body` into any other material, and `-km` must be verified to have preserved
it as its own material in the output. If `Toy_body` disappears or merges, every
PCC in the city is the same colour and the entire livery design is dead. Check
the output's material list explicitly and record it.

Do not run the high→low texture bake.

## Manifest draft

```json
{ "id": "f-line-pcc", "file": "vehicles/f-line-pcc.glb", "kind": "streetcar",
  "dims": [x, y, z], "targetLengthM": 14.0, "front": "-Z",
  "tris": N, "weight": 1,
  "tints": ["#...", "#...", "#...", "#...", "#..."],
  "notes": "Heritage vehicle. One geometry, per-instance Toy_body tint supplies the cities-series liveries. Requires kitfleet.js-style tinting in agents.js." }
```

The `tints` array is a proposed manifest extension — no existing entry has one.
Flag it as such; the integration decides whether tints live in the manifest or in
a code-side palette table like `KIT_TINTS`.

Do not edit the production manifest.

## Do not

- ship one GLB per livery without surfacing the draw-call cost as a decision
- let the shrink pass merge `Toy_body` into another material
- author to the landmark `−Y` front convention
- include rails or overhead wire in the vehicle GLB
- add textures or ship a `_Glow` primary surface
- give either entry a non-zero `weight`
- edit `vehicles_manifest.json`, `app/src/agents.js` or any app code
````

---

## Part 2 — Research and design dossier

Compiled 12 August 2026. Values marked *inferred* are visual or derived
estimates — re-verify anything you rely on.

### 2.1 Verified facts

**PCC streetcars**

| Item | Value | Source |
|---|---|---|
| Built | 1946–1948 | F Market & Wharves |
| In service on the F line | ~27 cars | F Market & Wharves |
| SF fleet composition | 3 original SF double-ended · 16 ex-Philadelphia single-ended (acquired 1992) · 11 ex-Newark single-ended, originally built for Minneapolis–St Paul (acquired 2002) | F Market & Wharves |
| Additional stored | ~30 unrestored, incl. ex-St Louis, Pittsburgh, Philadelphia | F Market & Wharves |
| Length | 14.02–15.39 m (46–50.5 ft), varies by city | PCC streetcar |
| Width | 2.54–2.74 m (100–108 in) | PCC streetcar |
| Weight | 15,900–19,100 kg | PCC streetcar |
| Seats | 52–61 | PCC streetcar |
| Post-war side window pattern | front door, seven windows, side door, four windows, two rear quarter windows | PCC streetcar |
| Double-ended variant | 15.4 m × 2.7 m, pre-war body styling | PCC streetcar |
| Liveries | painted in the colour schemes of past and present PCC operators — the "cities series" | F Market & Wharves |

**Milan Peter Witt cars**

| Item | Value | Source |
|---|---|---|
| Built | **1928**, Milan, Italy | F Market & Wharves |
| Operating on the F line | 11 cars | F Market & Wharves |
| Fleet numbers | 1807, 1811, 1814–1815, 1818, 1834, 1856, 1859, 1888, 1893, 1895 | Muni fleet roster |
| Livery | most in the original Milan **orange**; some in yellow-and-white trim or two-tone green | F Market & Wharves / Muni roster |
| Design lineage | Italian derivative of a common US streetcar design, never previously operated in SF | F Market & Wharves |
| Dimensions | ~14 m × ~2.4 m | *inferred* — **verify** |

Also on the line: pre-PCC SF veteran cars (1895–1924) and ~10 international trams
from Blackpool, Hamburg, Osaka, Melbourne, Moscow, Porto and Brussels. Out of
scope for this plan — noted because a future session may want them, and because
they reinforce that variety is the family's defining trait.

### 2.2 Sources

- https://www.sfmta.com/muni-transit — the family taxonomy
- https://en.wikipedia.org/wiki/F_Market_%26_Wharves — fleet composition, origins, liveries, the international collection
- https://en.wikipedia.org/wiki/San_Francisco_Municipal_Railway_fleet — Milan fleet numbers, build year, livery variants
- https://en.wikipedia.org/wiki/PCC_streetcar — dimensions, weights, window and door patterns
- Market Street Railway — livery documentation and per-car histories (**the best source for specific colour schemes**)

### 2.3 Orientation and placement

Vehicle contract: nominal front `−Z`, origin centred in X/Z, `min y = 0` at the
**street surface**, identical to the buses — there are no rails in this scene.

The SF PCC fleet contains both single- and double-ended cars. Decide which you
are modelling — the ex-Philadelphia and ex-Newark majority are single-ended, so
single-ended is the defensible default — and state it.

### 2.4 What each side shows

**PCC, front** — The signature: a rounded, forward-leaning nose with large curved
windows, a **single central headlight** low in the fascia, a metal bumper below,
and the destination sign above the windscreen. The roof crown curves down to meet
the nose.

**PCC, sides** — A long flank of rectangular windows in a regular rhythm, broken
by the front and centre doors. The livery is typically a body colour below the
window line with a contrasting band above or a swept division — this is what the
tint design must accommodate. Fleet number near the front.

**PCC, rear** — On single-ended cars, a rounded but blanker version of the nose,
with tail lights and the trolley pole base above.

**PCC, top** — A gently crowned roof with the trolley pole mounted toward the
rear, trailing back. Roof ventilators in a line. On the app's 42° camera this is
a fully visible surface.

### 2.5 Recognition cues (ranked)

**Family**

1. Colourful vintage railcars against modern San Francisco
2. Trolley poles trailing to an overhead wire

**PCC**

3. Rounded streamlined nose and curved roof
4. Single central headlight
5. Regular rhythm of rectangular side windows

### 2.6 The draw-call arithmetic

This is the design decision that shapes the whole plan.

`loadVehicles()` in `app/src/agents.js` creates one `InstancedMesh` per manifest
entry. Five PCC liveries as five entries = five permanent draw calls for one
silhouette. Against AGENTS rule 2's 300-call budget, and with five transit
families to fit, that is not affordable.

The repo already solved this problem for buildings. `app/src/kitfleet.js`:

```js
// Toy_body is authored mid-warm-grey, and the batch colour multiplies it, so
// a tint has to be divided by the body colour to land on the palette entry.
const BODY_BASE = new Color().setRGB(0.694, 0.659, 0.586);
```

One geometry, a `KIT_TINTS` palette, per-instance colour, one draw call. The
vehicle fleet path in `agents.js` does not implement it — it bakes material
colours to vertex colours and shares a single `MeshLambertMaterial`.

Porting that mechanism is a small, well-precedented change, and the F line is the
feature that justifies it. **The asset should be authored for the tinted design
now**, so that when the change lands the liveries are free.

Constraint that follows: a livery must read with **one** tinted colour plus fixed
trim. A three-colour scheme cannot be expressed. Choose the cities-series liveries
accordingly and record any rejected for that reason.

### 2.7 Miniature translation

**Preserve**

- The 1940s streamline read: rounded nose, curved roof, single central headlight
- Trolley pole trailing backward
- Real length (~14 m) at real scale

**Simplify / exaggerate**

- PCC nose becomes 4–5 chamfered planes, not a lofted surface — the toy style
  wants faceted, and a lofted nose eats the entire budget
- Window rows become uniform chunky openings; do not model the real irregular
  pattern, model its rhythm
- Trolley poles thickened well past scale, as on the trolley coach — a
  scale-accurate pole is sub-pixel at the app camera
- Trucks reduced to two wheel discs each behind a skirt
- No interior, no seats, no destination roll hardware, no coupler detail

### 2.8 Massing recipe

**PCC** — build order for the deterministic script:

1. **Underframe** — box 14.0 × 2.6 × 0.30 m, top at y 0.85, `Toy_ink`.
2. **Trucks and wheels** — two trucks, 4 wheels, radius 0.33 m, 8 segments,
   `Toy_ink`, wheels spaced at standard gauge 1.435 m (a model detail only —
   there is no track in the scene, but the width still reads).
3. **Body shell** — 14.0 × 2.6 × 2.2 m on the underframe, crown the roof 0.15 m,
   bevel 0.12 m / 2 segments. **`Toy_body`** on the panels below and around the
   window line.
4. **Nose** — chamfer the leading 1.6 m: rake the front face ~10°, round the
   upper corners with a 0.6 m chamfer, curve the roof crown down into it.
5. **Window band** — 8 openings per side in a regular rhythm, chamfered,
   `Toy_glass` inset 0.04 m in `Toy_ink` reveals. Fixed materials — not tinted.
6. **Front windows** — two large curved-corner panes wrapping the nose,
   `Toy_glass`.
7. **Doors** — front and centre, `Toy_ink` recesses with `Toy_glass`.
8. **Livery band** — a `Toy_cream` fixed band above the window line, giving the
   tint something to sit against. Fixed, not tinted.
9. **Bumpers** — front and rear `Toy_steel` bars, 0.12 m deep.
10. **Headlight** — single central `Toy_steel` bezel with a `Toy_white_Glow` lens
    shell 0.03 m proud.
11. **Roof** — `Toy_roofd`, crowned, with a line of 5 small ventilator boxes.
12. **Trolley pole** — base plinth `Toy_ink` toward the rear of the roof; tapered
    pole, base radius 0.075 m (exaggerated), length 5.5 m, angled 30° above
    horizontal, trailing backward, `Toy_steel`; chunky `Toy_ink` shoe at the tip.
13. **Destination sign** — above the windscreen; opaque `Toy_ink` backing with a
    `Toy_mustard_Glow` shell 0.03 m proud, extruded route letter.

### 2.9 Materials and palette

| Material | Hex | Used for |
|---|---|---|
| **`Toy_body`** | `#d8d3c8` | **livery panels — the tinted surface** |
| `Toy_cream` | `#f2ede3` | fixed livery band above the window line |
| `Toy_ink` | `#3a3530` | underframe, trucks, wheels, window reveals, doors, pole base, shoe |
| `Toy_glass` | `#2a4d73` | windows and windscreen |
| `Toy_steel` | `#9aa0a6` | bumpers, headlight bezel, trolley pole |
| `Toy_roofd` | `#45454a` | roof, ventilators |
| `Toy_white_Glow` | `#f7f4ec` | headlight lens |
| `Toy_mustard_Glow` | `#d9a441` | destination sign, interior ceiling strip |
| `Toy_red_Glow` | `#c4453c` | tail lights |

Proposed PCC tint palette — **replace these with researched cities-series colours
before building**; they are placeholders illustrating the one-colour constraint:

| Livery | Tint | Notes |
|---|---|---|
| Muni "wings" | `#c4453c` | the home livery |
| Boston | `#d9a441` | |
| Kansas City | `#3fa8a0` | |
| Philadelphia | `#6db3d9` | |
| Chicago | `#e8735a` | |

### 2.10 Top surface

The car is long and fully visible from above: crowned roof, a line of
ventilators, the trolley pole base and the pole trailing off the rear. Keep the
roof a distinct value from the flanks so the crown reads as a curve rather than
as a flat lid.

### 2.11 Scope

**In the GLB:** body, roof, windows, doors, trucks and wheels, bumpers,
headlight, destination sign, trolley pole with base and shoe

**Not in the GLB:** rails, sleepers, overhead wire, catenary poles, passengers,
driver, street surface, ground plane, plinth, cameras, lights

### 2.12 Triangle budget

Cap 4,000: body and nose chamfers 1,200 · glazing 800 · window reveals and doors
500 · roof and ventilators 350 · trucks and wheels 450 · trolley pole 250 ·
bumpers, headlight, sign 300 · spare 150.

### 2.13 Draft manifest entries

```json
{ "id": "f-line-pcc", "file": "vehicles/f-line-pcc.glb", "kind": "streetcar",
  "dims": [x, y, z], "targetLengthM": 14.0, "front": "-Z",
  "tris": N, "weight": 1, "tints": ["#...", "#...", "#...", "#...", "#..."] },
{ "id": "f-line-milan", "file": "vehicles/f-line-milan.glb", "kind": "streetcar",
  "dims": [x, y, z], "targetLengthM": 14.0, "front": "-Z",
  "tris": N, "weight": 1 }
```

### 2.14 Integration notes — deferred

Placement, spawning, weighting and live Muni data are **out of scope for this
task** and are parked in
[`docs/asset-plans/transit/INTEGRATION-LATER.md`](./INTEGRATION-LATER.md).

What this task owes the follow-up is only the draft manifest entry in
`REPORT.md`, and anything the renders revealed about how the vehicle behaves at
1.6× scale in the real city — that evidence is what the integration decisions
will be made from.

### 2.15 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB
- [ ] **Front faces `−Z`**; `min y` within 0.05 m of 0; XZ centre offset within 0.1 m
- [ ] Wheel spacing is **1.435 m**, visibly wider than the cable cars' 1.067 m
- [ ] **`Toy_body` present and separately addressable**
- [ ] **`Toy_body` survives the shrink stage and meshopt intake as its own material**
- [ ] Dimensions match 2.1 in real metres
- [ ] Triangles at or under 4,000
- [ ] Materials flat, no textures, no alpha
- [ ] `_Glow` only on headlight, sign, interior strip, tail lights — proud shells
- [ ] Per-object signed volume positive, including the trolley poles
- [ ] No cameras, lights, animations, armatures, constraints; no leaked geometry
- [ ] Day and night renders; elevations + top + aerial + contact sheet
- [ ] **1.6× in-city scale render**
- [ ] **Livery sheet — every proposed tint applied, from the app camera**
- [ ] Shrink stage run at 0.05° dissolve; material list verified post-gltfpack
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.16 Open questions and risks

- **`Toy_body` merging is the catastrophic failure.** gltfpack merges materials
  with identical parameters, and `-km` is what prevents it. If `Toy_body` is
  authored with the same parameters as another neutral material and `-km` is
  omitted or fails, every PCC in the city becomes one colour and the failure is
  silent. Verify the output material list explicitly, not by inference.
- **One-colour liveries are a real constraint.** Several cities-series schemes are
  genuinely two- or three-colour. Research the set first, pick the ones that
  survive the constraint, and record the rejections — do not discover this while
  modelling.
- **The tinting dependency may be rejected**, in which case three baked liveries
  is the fallback. Surface that as a decision with the draw-call cost attached,
  never as a silent choice.
- **Curved-shell dissolve** will attack the PCC nose exactly as it attacked the
  cathedral shells. 0.05°, and check windings after.
- **Single- vs double-ended** changes the rear entirely. The SF fleet has both;
  pick, justify, and record.
- **The trolley pole now touches nothing**, per the README's no-rails-no-wires
  decision. This is a much smaller problem than the trolley coach's: a streetcar
  pole is shorter and lies closer to the roofline, and on a vintage vehicle a
  viewer reads it as period detail rather than as a connection they expect to
  trace. Keep it.

### 2.17 The deferred Milan Peter Witt car

Not in scope. The 511 SIRI feed resolves vehicle **mode** from `LineRef`, and
both the PCC and the Milan run as `F` — one heritage streetcar GLB renders the
line faithfully. The PCC is the right single choice: ~27 cars in service against
the Milan's 11, and the cities-series liveries already deliver the visual variety
the heritage line is prized for.

Research kept for a later pass, because the car is genuinely different and should
never be a reskinned PCC:

| Item | Value | Source |
|---|---|---|
| Built | **1928**, Milan, Italy | F Market & Wharves |
| In service on the F line | 11 cars | F Market & Wharves |
| Fleet numbers | 1807, 1811, 1814–1815, 1818, 1834, 1856, 1859, 1888, 1893, 1895 | Muni fleet roster |
| Livery | most in the original Milan **orange**; some yellow-and-white trim or two-tone green | F Market & Wharves |
| Dimensions | ~14 m × ~2.4 m — **inferred, unverified** | — |

Design notes if it is picked up: boxy slab sides, a nearly flat front with one
prominent headlight, 10 smaller windows per side each in a proud `Toy_cream`
frame (the framing is the identity), `Toy_rust` wooden-look doors, a squarer roof
with a **0.25 m overhang** that is its best aerial cue, and a fixed
`Toy_ioorange` body with **no `Toy_body`** — it is a single livery, not a tinted
one. Budget 4,000: body and overhang 900 · window framing 1,100 · glazing 700 ·
doors 300 · roof 250 · trucks and wheels 450 · trolley pole 250 · headlight and
sign 150. It shares trucks, trolley pole and glazing vocabulary with the PCC,
which is why `build_f_line.py` is written as component functions.

`VehicleRef` in the feed is the real fleet number and the Milan cars occupy the
1807–1895 block against the PCCs' 1006–1080, so the split could be driven from
data with no guessing.
