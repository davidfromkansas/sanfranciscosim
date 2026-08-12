# Powell Street cable car — build report

**Deliverable:** one validated miniature GLB, `cable-car-powell.glb`, plus
dossier, scripts, validation and renders. **Nothing is integrated:**
`vehicles_manifest.json`, `app/` and `pipeline/` are untouched, per
`docs/asset-plans/transit/README.md` ("Scope: models only").

| | |
|---|---|
| File | `artifacts/cable-car/cable-car-powell.glb` |
| Triangles | **3,776** of a 6,000 cap |
| Dimensions (glTF x, y, z) | **2.42 × 3.18 × 8.40 m** |
| Front | **−Z**, proved, not asserted |
| Ground | **min y = 0**, the street surface |
| Origin | centred in X/Z, offset 0.0000 m |
| Materials | 20, all `Toy_*`, no textures, no alpha, no `Toy_body` |
| Glow set | `Toy_mustard_Glow`, `Toy_white_Glow` |
| Baked figures | 8 (gripman, conductor, 3 standees, 3 seated) — 444 tris |
| GLB bytes | 90,736 after meshopt |
| Draw-call cost if integrated | +1 |

Reproduce everything with `./make.sh`.

---

## 1. Contract validation

Two stages are validated, because the shrink pass deliberately dissolves the
per-object structure the closure gate depends on (§3).

### 1a. Authored export — `validation.json` — **PASS**

227 objects, 3,888 tris, straight out of `build_cable_car.py`.

| Gate | Result | Evidence |
|---|---|---|
| Real metres, published dimensions | PASS | 2.42 × 3.18 × 8.40 vs published 2.40 × 3.18 × 8.40. Length and height exact; X is 2 cm over because standing riders lean past the running boards, which is the point of them |
| Ground at `min y = 0` | PASS | 0.0000 m. **It represents the wheel contact patch on the street surface** — there are no rails in this scene, so there is no top-of-rail question; the car grounds exactly like a bus |
| Origin centred in X/Z | PASS | offset (0.0000, 0.0000) |
| Front faces **−Z** | PASS | Not asserted — tested. Headlamp glow occupies z ∈ [−4.200, −4.135], i.e. the extreme −Z; cabin glazing occupies z ∈ [−0.780, +3.570], entirely behind it. Both figures are converted out of Blender into glTF space by (x, z, −y) before reporting |
| Narrow gauge | PASS | measured 1.067 m, not 1.435 |
| ≤ 6,000 triangles | PASS | 3,888 authored / 3,776 shipped |
| No image textures | PASS | 0 images, 0 textured materials |
| No transparency | PASS | every material alpha 1.0 |
| Materials follow contract | PASS | all `Toy_*`; **no `Toy_body`** |
| No cameras / lights | PASS | 0 / 0 |
| No animation, skin, armature, constraint | PASS | 0 fcurves, 0 armatures, 0 constraints |
| Transforms applied, no negative scales | PASS | every object identity-transformed |
| **Every object a closed solid** | PASS | 0 open shells of 227 |
| **Every object signed volume positive** | PASS | 0 inverted of 227 |
| Normals finite and unit | PASS | 0 bad loop normals |
| No degenerate geometry | PASS | 0 triangles under 1e-9 m² |
| No unexpected objects | PASS | 227 meshes, nothing else |
| Glow ships with emission off | PASS | emission strength 0.0 on both glow materials |
| Gripman **and** conductor present | PASS | both, both standing |
| ≥ 3 standees on the running boards | PASS | 3 |

**The hard gate behaved as predicted, twice.** Per-object closure on an open
vehicle is exactly where this asset was expected to fail, and two rounds of it
were real:

1. The first validator run reported *every* object as an open shell. That was
   the validator's bug, not the model's: the glTF exporter splits a vertex per
   distinct normal and this asset is shaded flat, so a re-imported cube arrives
   as six topologically disconnected quads. `is_closed()` now welds at 1e-5
   before counting edge/face incidence.
2. Two real geometry bugs were caught by the closure/volume machinery and
   fixed at the source rather than patched at validation: mirrored parts
   written as `sx * a, sx * a + sx * b` arrived with `x1 < x0` on the left
   side, silently inverting the winding — `box()` now sorts its own extents;
   and a wheel authored with `disc_y` came out as a disc lying flat against the
   car side rather than a wheel, which the front elevation caught and `disc_x`
   fixed.

### 1b. Shipped file — `validation-final.json` — **PASS**

20 objects, 3,776 tris. Identical dimensions, min y, front direction, material
set and glow set. The four per-object checks are recorded as observations, not
gates, at this stage, with the reason stated in the file: after
join-by-material a group is a *union* of solids rather than one closed solid.
What must still hold is gated in `shrink-stats.json` as `merge_vehicle_safe`
— see §3.

### Off-palette WARNs (2)

| Material | Hex | Why |
|---|---|---|
| `Toy_maroon` | `#7b2230` | The Powell livery is the asset's identity. The plan's `Toy_brick` `#c96f4a` is a warm terracotta that reads as a brick building. `cable-car.md` §2.8 explicitly authorises taking this WARN |
| `Toy_oak` | `#c08e50` | Varnished wood — posts, benches, window frames, monitor wall. Half of why the car reads as a 19th-century wooden vehicle; the palette has no wood tone |

`Toy_p_*` is a **new figure palette** this asset introduces (`Toy_p_navy`,
`_coral`, `_teal`, `_mustard`, `_cream`, `_tan`). The plan says to reuse "the
existing figure vocabulary" from earlier `artifacts/` work — there is none: no
committed artifact ships baked people. The colours are drawn from the contract
accents so the riders sit inside the existing colour world; `Toy_p_tan`
`#d8a878` is a skin tone the palette does not carry.

---

## 2. Design decisions

Style bible §22 was applied as a decision procedure, not a checklist. The four
points the plan called out:

**Openness is the silhouette.** Every void is real geometry. The grip section
has no side wall above 1.30 m, the roof there stands on four slim posts per
side, and the rear platform is open on both flanks. The `-backlit` renders are
the proof: at 120 m the gaps between the posts punch through as bright shapes
and the running boards read as a dark line with figures on it. Two changes came
out of protecting this:

- The open section's low panel was first built full width — a solid slab
  through the middle of the car. It buried the bench seats (which then read as
  missing, and which the shrink pass correctly deleted as interior) and quietly
  filled the lower half of the void. It is now **two side walls**.
- The grab poles were moved from `Toy_gold` to `Toy_ink`, which is both
  photo-accurate (§6 of the dossier) and what makes the verticals survive the
  backlit test.

**Riders complete the shape.** 8 figures, 444 triangles — 11% of the model, and
deliberately so. Three stand on the running boards with a raised arm to the
pole; three sit outward-facing on the open benches; the gripman stands at the
levers and the conductor at the rear. They are closed stacks of boxes, ~60
triangles standing and ~48 seated, no faces and no fingers.

**Designed for the grade.** The `-tilted` render puts the car on a real 20.2%
residential segment on Russian Hill, taken from the baked street tiles, square
to the kerb so the pitch is a slope and not foreshortening. Roofline, running
boards and figures all still read.

**Trim is where the budget went.** The gold pinstripe rectangle on the maroon
panel, the arched (chamfered-top) window heads, the maroon roof fascia under a
gold moulding ring, the monitor deck with its clerestory lights and hinged vent
panels, the decorative brackets at every post head, the banded rocker with its
lettering strip. This is why the model is 3,776 triangles and not 2,000.

**Roof.** The camera looks down at 42°, so the roof is a primary surface. It
carries the maroon fascia, the gold moulding, the raised monitor deck with
arched ends, five clerestory lights per side, four vent panels and the gong —
photo-verified, and it settles the plan's open question (`cable-car.md` §2.9):
**the monitor deck is present**.

### Night-glow set

The loader draws `_Glow` in a separate unlit layer at
`opacity = 0.12 + 0.95 * uNight`, so each glow surface is authored as a thin
shell standing 3.5–4 cm proud of an opaque surface with its **back face buried**
inside that surface.

| Surface | Material | Opaque surface behind it |
|---|---|---|
| Cabin ceiling strip, full length | `Toy_mustard_Glow` | `Toy_cream` ceiling slab |
| Side letterboards, both flanks | `Toy_mustard_Glow` | `Toy_mustard` board |
| Front and rear route boards | `Toy_mustard_Glow` | `Toy_mustard` board |
| Headlamp lens | `Toy_white_Glow` | `Toy_white` lens behind a `Toy_gold` bezel |
| **Cabin window panes (4 per side)** | `Toy_mustard_Glow` | `Toy_glass` pane |

The lit panes are a **fourth surface the plan's table does not list**, added
deliberately: without them the enclosed half of the car goes black at night
while the open half glows, which is the opposite of the plan's own stated goal
("at night you see the warm light through the vehicle"). They are inset far
enough that a navy border of real glass survives by day.

Emission ships at 0.0 per contract. The render scripts take emission from Base
Color rather than raising strength, because a glTF `emissiveFactor` of (0,0,0)
makes Blender's importer default Emission Color to white.

---

## 3. Shrink stage — `shrink-stats.json`

Run per `docs/asset-plans/transit/README.md` Part 3 with `ASSET_CLASS=vehicle`.

| Step | Tris | Verts | Objects |
|---|---:|---:|---:|
| input (authored) | 3,888 | 2,396 | 227 |
| 1–2a weld ≤ 1 mm + degenerate, per object | 3,888 | 2,396 | 227 |
| 2b interior faces | 3,776 | 2,392 | 227 |
| 3 limited dissolve **0.05°** | 3,776 | 2,392 | 227 |
| 4 curve retessellation | **skipped, deliberately** | | |
| 5 join per material | 3,776 | 2,392 | **20** |

| File | Bytes |
|---|---:|
| authored | 312,724 |
| after shrink | 218,716 |
| **after meshopt intake (shipped)** | **90,736** |

### The two cautions the plan attached to this asset

**Caution 1 — the interior-face step on an open vehicle.** It fired. The first
run deleted **342 of 3,888 faces (8.7%)** and the script raised its alarm. The
investigation found three separate causes, two of them real defects:

1. *Real bug.* The open section's full-width low panel buried both bench seat
   pans completely. The seats were invisible in the shipped model and the
   shrink was right to delete them. Fixed by building the open section's low
   panel as two side walls, which also opens the lower half of the void.
2. *Real bug.* The letterboard's lettering bar sat **inside** its own glow
   shell — so it was neither readable by day nor present at night. Moved
   outboard of the shell.
3. *False positive.* The 0.95 AABB-fill test accepted a gently **crowned**
   prism as a solid box, and the AABB of a crowned prism contains air the solid
   does not: the roof vent panels sitting on that crown were condemned. The
   occluder test now additionally requires every face normal to be axis-aligned
   and raises the fill threshold to 0.99.

After the fixes the step removes **112 faces (2.9%)**, and every one is
enumerated in `shrink-stats.json → interior_faces_by_object` with its occluder:
the pole shanks inside the running boards (72), the outboard tips of the bench
pans inside the side walls (20), lever roots inside the lever housing, cabin
bench ends inside the body, the running-board strips' inner faces. All provably
buried. The alarm threshold now sits above this audited baseline so a
regression still trips it.

**A defect this step introduced, and the fix.** Deleting buried faces *opens*
the solid it deletes them from. On the first clean run that turned the glow
shells into open shells, and `grp_Toy_mustard_Glow` came out of the join with a
**negative signed volume**. That is not cosmetic: `mergeVehicle()` in
`app/src/agents.js` does

```js
if (signedVolume(geometry) < 0) reverseGeometry(geometry);
```

per source mesh, so the app would have shipped the destination boards, the side
letterboards and the lit cabin ceiling **inside out**. Fixed by exempting every
`_Glow` object from interior-face deletion — the same rule as the README's
"never weld across a `_Glow` boundary", applied to the deletion step — and the
condition is now a hard gate: `merge_vehicle_safe: true`, with every group's
signed volume recorded.

**Caution 2 — the poles must survive the join.** They do. The join folds all
39 `Toy_ink` objects (including all 12 grab poles) into one mesh, which is
correct and desirable, and `poles_survived_join: true` verifies the geometry
came through. Step 4 is **not run at all**: the poles are 8-segment cylinders
already sized against the vehicle camera band (near 15 m, far 120 m) multiplied
by the 1.6× render scale, and halving their segments would square off the
verticals that carry the whole open-section read.

**Texture bake:** not run, per the README's explicit exclusion.

### Gates

| Gate | Threshold | Result |
|---|---|---|
| G1 Contract | material name set identical pre/post; `_Glow` layer intact; front −Z and min y = 0 preserved | **PASS** — 20/20 material names identical, both glow materials present, front −Z and min y 0.0000 |
| G2 Fidelity | bbox within max(1 cm, 0.1%); origin within 1 cm; per-object signed volume positive | **PASS** — bbox identical to 4 dp; origin 0.0000; no negative group (`merge_vehicle_safe`) |
| G3 Round-trip | re-imports in Blender **and** loads through `createGLTFLoader()` with the meshopt decoder | **PASS in Blender** (validation-final.json is a fresh-scene re-import of the shipped meshopt file). The `createGLTFLoader()` half is **NOT VERIFIED** — see §6 |
| G4 Appearance | day and night A/B at 15 m and 120 m at 1.6×, mean pixel delta ≤ 4% near / ≤ 2% far | **NOT RUN as an A/B** — see §6 |
| G5 Draw calls | primitive count ≤ input | **PASS** — 227 → 20 |
| G6 Size | file smaller after the pass | **PASS** — 312,724 → 90,736 bytes (71% smaller) |
| G8 Hygiene | no leaked objects; `.blend1` deleted | **PASS** — the build starts from `read_factory_settings(use_empty=True)` (Blender's startup Cube was leaking into the first export), exports from a temp scene with `use_active_scene=True`, and the re-import object count matches. No `.blend1` committed |

### One doc discrepancy worth fixing upstream

`docs/asset-plans/transit/README.md` Part 3 specifies gltfpack `-cc -kn -km
-noq`. The shipped compressor `pipeline/compress-assets.mjs` actually runs
**`-c -km -kn -noq`**. This asset was compressed with the shipped compressor's
flags, since that is what every other GLB in the tree was built with and what
`app/src/gltf.js`'s decoder is proven against. `-cc` was measured for
comparison and produced 90,600 bytes against `-c`'s 90,604 — a 4-byte
difference, so nothing is lost by matching the code. The README line is the
stale one.

---

## 4. Renders

All rendered from the **shipped** GLB, re-imported into an empty scene, with
`_Glow` knocked to alpha 0.12 for daylight to match what the loader shows at
noon.

`renders/cable-car-powell-{front,rear,left,right,top,aerial,night}.png` plus
`-contact-sheet.png`, and the three mandatory decision renders:

**1. In-city at 1.6× — `-in-city.png`.** The car on a real baked SF street
(cell 19_8, Russian Hill) with the real baked buildings, beside a shipped
`commuter-bus` and `sedan-red` at the same 1.6×. `export_city_cell.mjs` rebuilds
the tiles through the app's own `app/src/tilebin.js` reader — buildings,
streets, landcover and the `terrain.bin` heightfield — so this is the city, not
a stand-in. **Confirmed: 13.4 m is the friendliest scale in the transit set.**
Against the 19.5 m bus the cable car reads as a small vintage vehicle rather
than a shrunken one, and against the 8.0 m sedan it reads as public transport.
The exaggeration helps here.

**2. Tilted at 20.2% — `-tilted.png`.** A real residential segment on Russian
Hill, chosen by the exporter as the segment nearest 20% grade within 150 m of
the cell centre (the same cell also holds Lombard's 40%+ crooked block, which
no cable car has ever climbed, so "steepest" was the wrong selector). Pitched
11.4° about its own origin — which, because min y = 0 and the origin is centred,
puts the wheel line exactly on the slope. Roofline, running boards, poles and
figures all still read.

**3. Backlit — `-backlit.png` and `-backlit-detail.png`.** From the app's 42°
camera at 120 m against a bright emissive backdrop. The voids punch through as
bright shapes between the dark posts and poles; the running board reads as a
dark line with a standee on it. **The openness survives at 120 m** — no
exaggeration of the posts or voids was needed beyond the 45 mm pole radius the
plan already called for.

Two render-scene notes, stated because they are visible in the images:

- Context geometry is shaded **part self-lit** (45% emission of its own vertex
  colour). The baked tiles contain volumes that enclose their own ground —
  OSM footprints extruded from sea level swallow the roadway on a hillside —
  and a physically shaded interior renders pure black, which reads as a hole in
  the street. The app never shows this because its city shader is a flat
  Lambert with a large ambient term. **The cable car itself is shaded
  normally**; it is the thing under review.
- The context mesh also gets a backface-flipped shading normal, because the
  baked ground triangulations do not guarantee a winding and the app draws them
  double-sided.

---

## 5. Draft manifest entry — **not applied**

`app/public/sf-assets/vehicles_manifest.json` is **not modified by this work.**
For the integration session:

```json
{ "id": "cable-car-powell", "file": "vehicles/cable-car-powell.glb", "kind": "cable-car",
  "dims": [2.42, 3.18, 8.40], "targetLengthM": 8.4, "front": "-Z",
  "tris": 3776, "weight": 1,
  "notes": "Single-ended Powell car. No rails or cable slot in the scene." }
```

`weight` is set at integration, not here. The plan's own "Do not" list says to
give the entry a non-zero weight only at integration; the draft above carries
the plan's literal `"weight": 1` so the integration session sees the intended
value, and it is inert until someone copies it into the production manifest.

**What this work owes the follow-up**, beyond the entry: the vehicle is 8.4 m
and renders at 13.4 m, which is comfortable on a residential street and on a
20% grade — the in-city render shows a lane's width to spare beside a parked
sedan. The remaining integration risk is not scale, it is placement: a cable car
in the Outer Sunset is worse than no cable car. See
`docs/asset-plans/transit/INTEGRATION-LATER.md`.

---

## 6. Honest gaps

- **G3, the `createGLTFLoader()` half, is not verified.** The shipped file
  re-imports cleanly in Blender, and it was compressed with the exact flags
  `pipeline/compress-assets.mjs` uses on every other GLB in the tree, so the
  decoder path is the same one already proven. But nothing in this session
  loaded the file through the app. That is an integration-session check.
- **G4 is not run as a numeric A/B.** The gate compares a shrunk asset against
  its pre-shrink self at 15 m and 120 m, day and night, with a mean-pixel-delta
  threshold. Day and night renders exist at both distances and were compared by
  eye — the shrink removed 112 provably buried faces and joined meshes, so no
  visible change is expected or seen — but no pixel-delta number was computed.
- **The in-city context is a reconstruction, not the app.** It reads the same
  tiles through the same reader, but it re-implements the extrusion rather than
  running `city.worker.js`, and it is lit as described in §4. It answers the
  scale question it was built to answer; it is not a screenshot of the app.
- **`city-cell.json` is not committed** — it is 2.3 MB of derived data.
  `export_city_cell.mjs` regenerates it in about a second, and `make.sh` does.
- **Deferred, as scoped:** the double-ended California Street car
  (`cable-car.md` §2.16). Every component function in `build_cable_car.py` —
  trucks, poles, benches, the band vocabulary, the arched window, the figures —
  is written to be reused for it. Its livery is still unverified; do not assume
  it matches the Powell scheme.
