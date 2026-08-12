# muni-lrv — build report

The SF-SIM miniature of San Francisco's Muni Metro light rail vehicle, the
Siemens **S200 SF** / SFMTA **LRV4**, signed `N JUDAH`, fleet number `2059`.

**Status: PASS.** Every contract check and every shrink gate is green.
Research is in [`REFERENCE.md`](./REFERENCE.md); machine-readable results are in
[`validation.json`](./validation.json) and [`shrink.json`](./shrink.json).

Nothing outside `artifacts/muni-lrv/` was touched. No manifest edit, no app
code, no deploy.

| | |
|---|---|
| Deliverable | `muni-lrv.glb` — 3,522 tris, 96,896 bytes, 3 nodes, 19 primitives |
| Dimensions (glTF x, y, z) | **2.658 × 4.761 × 22.860 m** |
| Front | **−Z** (long axis measured, not assumed — see §2.1) |
| `min y` | **0.0000** |
| Origin | centred in X/Z (offset 0.0000 / 0.0000 m) |
| Triangle budget | 5,000 → **used 3,522 (70%)** |
| Rendered length at `carScale = 1.6` | **36.6 m** single · **74.4 m** coupled pair |
| Draw-call cost | **+1 permanent** |

---

## 1. Five corrections to the plan's dossier

The task said to verify the dossier rather than trust it. Five of its claims did
not survive. The model follows the corrected reading; evidence and sources are in
`REFERENCE.md` §3, §4 and §8.

**1.1 The LRV4 is double-ended — there is no blank rear.** The plan's §2.4 left
this open and warned it "doubles or halves the cab budget". Wikipedia, CPTDB and
the fleet-number suffixes (`2059A` / `2024B`) all agree: two cabs, bi-directional.
Both ends of this model are cabs, and the rear elevation gets the same scrutiny
as the front.

**1.2 The red is a horseshoe around the windshield, not a band beneath it.** This
is the single most important finding. The plan describes "red Muni accent below
the glass" and a band "sweeping up across the cab fascia". Every photograph shows
a bold red **U framing the entire windshield** — across the top above the sign,
down both A-pillars, turning in under the glass. It is the vehicle's graphic
identity and the thing that makes an LRV4 recognisable from the front
three-quarter, which is where the app's camera spends most of its time. A model
that puts a thin red band under the windshield gets the most legible feature of
this vehicle wrong.

The plan's "sweep" is real, but it belongs to the *side*: the low flank band runs
forward and climbs into the horseshoe. Both are modelled.

**1.3 The doors are not evenly spaced.** SFMTA states the arrangement directly:
four per side, "two single doors at either end of the cab and two double doors in
the middle". So it is **single–double–double–single**, symmetric about the
articulation. The plan's §2.6 asks for four "evenly spaced"; the count is right —
and is not even a simplification, four per side is the real number — but even
spacing discards a visible rhythm that costs nothing to keep.

**1.4 The skirt is lighter than the plan thinks, and the body is paler.** The
plan's §2.8 assigns a dark `Toy_ink` skirt and a mid-silver body. The vehicle has
a **near-white body** with a **medium-grey skirt**; the dark band on the flank is
the *window* band. The plan's own §2.9 worry — that a mid-grey slab reads as a
featureless brick — is real, but it is not solved by three greys. Four of the
seven horizontal bands are not grey at all: the near-black window band and the
broad red band carry the contrast, and roof/body/skirt are the supporting steps.

**1.5 Height is 3.51 m, not "~3.6 m".** The sourced figure is 3.51 m with the
pantograph locked down; the 3.5–4.1 m band in the S200 infobox spans every
operator's variant, not San Francisco's. Body and roof equipment are built to
3.51 m, with the raised pantograph above that.

---

## 2. Contract compliance

Validated by re-importing the **shipped** GLB (post-shrink, post-meshopt) into a
fresh, empty Blender scene — never the authoring scene.

| Rule | Required | Measured | |
|---|---|---|---|
| Long axis / front | `−Z` | 22.86 m axis **is Z** | PASS |
| Ground | `min y = 0` | **0.0000** | PASS |
| Origin | centred in X/Z | **0.0000 / 0.0000** | PASS |
| Units | real metres | 2.658 × 4.761 × 22.860 | PASS |
| Triangles | ≤ 5,000 | **3,522** | PASS |
| Section node names | `LRV_Section_A/B`, `LRV_Bellows` | all three present | PASS |
| Exported straight | not pre-bent | lateral offset **0.00144 m** | PASS |
| Image textures | 0 | **0** | PASS |
| Transparency | none | all alpha 1.0 | PASS |
| Materials | `Toy_*` | all 9 prefixed | PASS |
| `Toy_body` | absent | absent | PASS |
| `_Glow` present | required | 3 (`Toy_mustard_Glow`, `Toy_white_Glow`, `Toy_red_Glow`) | PASS |
| Emission | 0.0 | 0.0 on every material | PASS |
| Cameras / lights | 0 / 0 | 0 / 0 | PASS |
| Animations / armatures / shape keys | 0 | 0 | PASS |
| Applied transforms | yes | no unapplied transforms | PASS |
| Negative scale | none | none | PASS |
| Per-object signed volume | positive | all 3 positive | PASS |
| Leaked foreign geometry | none | 3 objects in, 3 out | PASS |

### 2.1 A note on "front faces −Z" for a double-ended vehicle

The bus's validator infers the front from mass distribution. That test is a coin
flip here: the LRV4 is symmetric end to end, so there is no heavier end to find.
What `front = −Z` actually constrains on a symmetric vehicle is that **the 22.86 m
axis is Z**, and that is what is asserted. Which cab leads is a service matter,
not a modelling one — the `−Z` end is simply the one whose destination sign the
viewer reads first, and both signs are built independently so neither is mirrored.

### 2.2 Per-object

| Object | Tris | Materials | Signed volume (m³) | bbox z |
|---|---:|---:|---:|---|
| `LRV_Section_A` | 1,764 | 9 | 107.93 | −11.430 … −0.300 |
| `LRV_Section_B` | 1,686 | 9 | 127.91 | +0.300 … +11.430 |
| `LRV_Bellows` | 72 | 1 | 7.40 | −0.300 … +0.300 |

The two sections are exact mirrors: identical bounding boxes about the joint, and
the only differences are the pantograph — **78 triangles and the 1.29 m of extra
height on section A** — and the `A`/`B` fleet-number suffix.

Signed volume is used here as an **orientation gate, not a physical measurement**.
The sections are unions of interpenetrating solids that the 1 mm weld may fuse
differently on each side, so the two figures are not expected to match; what
matters is that both are comfortably positive, because `mergeVehicle()` in
`agents.js` flips any primitive whose signed volume is negative.

### 2.3 Palette deviations (WARN, not FAIL)

| Material | Hex | Why |
|---|---|---|
| `Toy_lrvbody` | `#dcdcd8` | New. The palette has no near-white silver, and `Toy_white` is needed one step above it for the roof. Without two distinct pale values the roof and flanks merge into one slab under flat diorama light. |
| `Toy_munired` | `#c1272d` | Carried over from `muni-bus` so the two Muni vehicles read as one fleet. Palette `red #c4453c` is a warm brick; Muni red is a cooler crimson. |
| `Toy_glass` | `#26405e` | Carried over from `muni-bus`. Palette `glass #2a4d73` reads navy across a 23 m panel where the brief wants a black window band. |
| `Toy_ink` | `#2e2b28` | Palette `ink #3a3530` taken slightly darker, for the same reason. |

---

## 3. The 1.6× in-city scale test — the verdict

**A single car is comfortable. A coupled pair takes 79% of a block face and does
not span one. No per-type scale override is needed — but the margin is thin, and
it is thin for a reason that will matter to the next asset.**

Method: the shipped `muni-lrv.glb` was re-imported and stood on **N Judah in the
Sunset** — real baked city geometry read from `app/public/tiles` through the app's
own `tilebin.js` reader — scaled by `carScale = 1.6` and rendered from the app's
42° diorama camera. The placement is 6.6 m from the real Judah/22nd Avenue
coordinates, found by targeting the alignment rather than by taking whatever
street sat nearest a cell centre.

Judah is genuinely surface running in mixed traffic, which is what makes the
no-rails decision honest for this vehicle.

### The measurement

`export_city_cell.mjs` measures the real distance between cross-street
intersections along the alignment, so this is a measurement rather than an
impression. **110 block faces** in the 230 m crop:

| | metres |
|---|---:|
| Median block face | **94.5** |
| Interquartile spread | ~89 – 98 |
| Shortest | 28.8 |
| Longest (a park edge, not a city block) | 359 |

| | Real | On screen at 1.6× | Share of a 94.5 m block face |
|---|---:|---:|---:|
| Single LRV | 22.86 m | **36.6 m** | **39%** |
| Coupled pair (0.80 m coupler gap) | 46.5 m | **74.4 m** | **79%** |
| Shipped `commuter-bus`, for reference | 10.77 m | 17.2 m | 18% |

### The judgement

`renders/muni-lrv-in-city-1.6x.png` — a single car reads as a long vehicle in
mixed traffic, not as an intrusion. It is a little over twice the shipped bus.

`renders/muni-lrv-coupled-pair-1.6x.png` — the pair reaches from one intersection
to within about 20 m of the next. It does **not** span the block face, but it
will frequently be seen with one car crossing an intersection while the other
occupies most of the block. On the Sunset grid that is what a two-car Metro train
actually looks like, so it reads as correct rather than as a scale error.

Two things to carry into integration:

- **No override is required, but there is no headroom left.** At 79% of the
  median block face, a coupled pair already fills most of a block. Any longer
  consist, or any block shorter than the median (the 25th percentile here is
  ~89 m, and 28.8 m faces exist), will overrun. If the integration session ever
  spawns three-car trains, this test must be re-run before it ships.
- **The 1.6× scale is doing the right thing at both ends of the fleet.** The
  muni-bus report found the 40-footer "the friendliest length in the transit set"
  and predicted the LRV was where the test would bite. It bites, but it holds.

### The pantograph, and what the no-rails decision costs

`renders/muni-lrv-in-city-120m.png` answers the plan's §2.15 question directly.
At the far end of the vehicle camera band, with no overhead wire anywhere in the
scene, **the raised pantograph reads as a compact roof object, not as an arm
reaching for something missing.** The plan's judgement was right and the price is
small — much smaller than the trolley coach's 6 m poles. Confirmed and recorded.

---

## 4. Shrink stage

`ASSET_CLASS=vehicle`, per `docs/asset-plans/transit/README.md` Part 3.
Reproduce end to end with `./shrink.sh`.

### Before / after

| | Build | After Stage 2 | After Stage 1 (meshopt) |
|---|---:|---:|---:|
| Triangles | 3,620 | **3,522** | 3,522 |
| Vertices | 7,234 | **2,496** | 2,496 |
| Bytes | 207,992 | 191,464 | **96,896** |
| Primitives | 19 | 19 | 19 |
| Nodes | 3 | 3 | **3** |

End to end: **−2.7% triangles, −65% vertices, −53% bytes.** The vertex collapse is
the weld doing its job on a model built from independently generated beveled
boxes; the triangle count barely moves because there was little waste to remove,
which is the intended outcome of authoring to budget rather than decimating to it.

### Stage 2, step by step

| Step | Result |
|---|---|
| 1 · Weld ≤ 1 mm, never across a `_Glow` boundary | **4,656 verts removed.** The guard is enforced, not assumed. This model exports three *multi-material* objects, so the muni-bus's "one material per object" structural guarantee is unavailable; instead the weld runs per-vertex and only merges a vertex when every face touching it shares one material index. A weld therefore cannot pull a 4 cm proud `_Glow` shell down onto the opaque surface behind it. |
| 2 · Degenerate + interior faces | 0 degenerate faces (< 1 mm²). **Interior-face removal was correctly not run**: the occluder test needs closed meshes, and each section is a union of solids with flat detail hosted inside them, not a closed manifold. An open shell's signed volume is meaningless and would let it masquerade as a solid box and eat real faces. Recorded rather than silently skipped. |
| 3 · Limited dissolve at **0.05°** (never 0.5°) | **1,820 faces merged**, 98 triangles net. This asset is the reason the README specifies 0.05°: the cab is a curved shell built from chamfered plan outlines stacked in z, and at 0.5° the dissolve merges transitively across those chamfers into twisted n-gons that re-triangulate with flipped windings. Windings verified after. |
| 4 · Retessellate curves | Audited, no change. A 0.68 m wheel at 1.6× is 1.09 m across; at the 15 m near camera that is ~80 px, where an 8-gon's worst chord error is 2.1 cm ≈ 1.5 px — and the wheels are ~70% hidden behind the skirt. Pantograph arms are 5- and 6-gon capsules for the same reason. |
| 5 · Join by material | Satisfied at authoring time **within each section**: one primitive per material per section. Materials are deliberately *not* joined across sections, because the brief requires `LRV_Section_A/B/Bellows` to stay separable. This is the one place where the section requirement and the join step genuinely trade off; the trade is recorded in `shrink.json`. |
| 6 · Normals audit | All 3 signed volumes positive. |

### Stage 1 — meshopt intake

`gltfpack -cc -kn -km -noq`, the README's flag set. `-km` is load-bearing (without
it gltfpack merges materials with identical parameters across the `_Glow`
boundary and silently destroys the night layer); `-noq` is load-bearing (int16
`KHR_mesh_quantization` corrupts the positions the app's merge paths bake world
matrices into). **`-kn` is load-bearing on this asset specifically**, and
`shrink.sh` verifies rather than assumes it: after intake it reads the raw glTF
and fails the build if `LRV_Section_A`, `LRV_Section_B` or `LRV_Bellows` is
missing. All three survive, and all 9 material names are unchanged.

The `-cc` / `-c` discrepancy between the README and the shipped
`pipeline/compress-assets.mjs` that the muni-bus report flagged still stands; it
is not re-litigated here.

**Texture bake: not run**, per the README. Out of scope for transit assets.

### Gates

| Gate | Result |
|---|---|
| G1 Contract | PASS — material name set identical pre/post; `_Glow` layer intact; node names intact; front axis and `min y = 0` preserved |
| G2 Fidelity | PASS — bbox and origin unchanged to 4 dp; all signed volumes positive |
| G3 Round-trip | PASS — re-imports in Blender 5.2 with the meshopt decode, and carries `EXT_meshopt_compression` for `createGLTFLoader()` |
| G4 Appearance | PASS — day and night renders made from the **final shipped GLB**; see the note below |
| G5 Draw calls | PASS — 19 primitives in, 19 out |
| G6 Size | PASS — 207,992 → 96,896 bytes |
| G8 Hygiene | PASS — 3 objects in, 3 out, no leaked geometry; no `.blend1` committed |

*G4 note:* as on the bus, the pass is geometric rather than photometric. The
shrink pass changes only vertex count, so a day/night A/B at 15 m and 120 m is
pixel-identical outside anti-aliasing noise. Every render in `renders/` is made
from the shipped GLB, so what was judged is what ships.

---

## 5. Three bugs worth recording

All three were invisible in flat-shaded previews and all three would have shipped.

**5.1 Mirroring geometry that already spanned both sides inverted the normals of
half the vehicle.** The body bands, skirt and roof equipment are authored full
width; mirroring them in X laid a second coincident copy of every face on top of
the first with reversed winding. The result is non-manifold, so
`recalc_face_normals` can no longer tell inside from outside, and those surfaces
exported with inward normals and rendered **pure black** — including the entire
roof, in an app whose camera looks down at 42°. Flat-shaded previews do not
consult normals at all, so the first three review passes looked fine. `build()`
now sorts components into three banks by how much of the vehicle each actually
draws, and the banking is documented as load-bearing rather than stylistic.

**5.2 `mirror_y()` duplicates; section B needed a reflection.** Building section B
with the duplicating mirror laid a whole second vehicle on top of the first —
caught because section B came out heavier than section A, when A carries the
pantograph and must be heavier. `Part.flip_y()` now reflects in place.

**5.3 Cab-face features drawn as single spans dived inside the shell.** The cab is
a chain of loft segments that bends at each declared level, so a windshield drawn
as one straight row between its top and bottom heights is a chord across that bend
and disappears into the bodywork in the middle of its span, leaving only its edges
poking out. The windshield and the entire black fascia were lost this way.
`_z_steps()` now subdivides every cab-face feature at the same heights the shell
bends at.

---

## 6. Design decisions worth reviewing

**The horseshoe is proud along +Y only, never outboard in X.** Pushing the frame
sideways to make it read would have widened the vehicle past its real 2.65 m. All
six cab-face features stack in a fixed proud order (fascia and cap +12 mm, glass
+16 mm, sign hood +14 mm, sign glow +48 mm, glyphs +62 mm, horseshoe +40 mm), so
the frame always stands 24 mm forward of the glass it frames.

**The destination sign is inverted, as on the bus.** Amber `Toy_mustard_Glow`
field with `Toy_ink` block glyphs standing proud of it. It keeps the glow as one
clean shell instead of dozens of tiny ones that vanish at 12% day opacity, and
costs tens of triangles where an extruded font would cost hundreds.

**Both signs are built independently, never mirrored.** `front_text()` takes an
`end` and lays glyphs so a viewer standing in front of *either* cab reads them
left to right. Verified by rendering both signs in close-up — mirrored lettering
is exactly the class of error that survives to production because nobody renders
the rear elevation.

**Doors are mullions, not holes.** The first pass made each door a full-height ink
slab, which chopped the livery into pieces and made the flank read as four black
holes. They are now dark mullions down each leaf edge plus a shallow threshold, so
the pale bodyside and the red band run on across the door as they do in reality.

**The articulation is a real geometric step in the roofline.** The plan is
specific that a bellows which only reads in side elevation is invisible where it
matters, and the top view confirms the step reads from directly overhead.

**The prow is set back 12 mm from its nominal position.** The proud fascia shell,
not the shell itself, is the furthest-forward geometry, so the declared prow is
set back by exactly that amount to land the overall length on 22.860 m rather
than 22.884 m.

---

## 7. The vehicle loader still has no glow layer

The brief states that the loader "puts `_Glow` materials in a separate unlit layer
at `opacity = 0.12 + 0.95 * uNight`". **That is true of the landmark loader, not
the vehicle loader** — first established by the muni-bus report §7, re-verified
here and unchanged: `mergeVehicle()` in `app/src/agents.js` merges every mesh into
one geometry, bakes each material's colour into vertex colours, and draws the
result with a single `MeshLambertMaterial({ vertexColors: true })`. `ferries.js`
*does* split on the `_Glow` suffix, which is the shape a future Muni-live module
would take.

This asset is authored to be correct either way. Every glow surface is a thin
shell proud of an opaque backing with its edges buried:

| Surface | Material | Proud of |
|---|---|---|
| Destination sign face (both cabs) | `Toy_mustard_Glow` | the opaque `Toy_ink` sign hood, by 3.4 cm |
| Interior ceiling strip | `Toy_mustard_Glow` | the opaque `Toy_glass` window band, by 4.0 cm |
| Headlights (both cabs) | `Toy_white_Glow` | the opaque `Toy_ink` housings, by 3.5 cm |
| Tail lights (both cabs) | `Toy_red_Glow` | the opaque `Toy_ink` housings, by 3.5 cm |

Under today's vehicle loader those read as an amber sign, a warm valance along
the window tops, white headlights and red tail lights — all correct in daylight.
If the vehicle loader ever gains the landmark's glow split, the same geometry
ignites at night over opaque backings and stays correct.
`renders/muni-lrv-night.png` previews the second case. The ceiling strip is broken
at each door, so the lit band reads as windows rather than as a continuous tube.

Emission ships at 0.0 per contract.

---

## 8. Draft manifest entry — **not applied**

`app/public/sf-assets/vehicles_manifest.json` was not edited. For the integration
session:

```json
{ "id": "muni-lrv", "file": "vehicles/muni-lrv.glb", "kind": "lrv",
  "dims": [2.66, 4.76, 22.86], "targetLengthM": 22.86, "front": "-Z",
  "tris": 3522, "weight": 0,
  "notes": "Muni Metro LRV4. No rails or overhead wire in the scene. weight 0 keeps it off the road spawner; a future Muni-live module spawns it the way ferries.js spawns the ferry. Nodes LRV_Section_A/LRV_Section_B/LRV_Bellows are preserved for a future articulation runtime." }
```

**`weight` is 0, and the plan contradicts itself about this.** Its prose says
`weight: 0` is "deliberate and load-bearing" and its Do-not list says "give the
entry a non-zero `weight`" — but both JSON snippets in the plan (Part 1 and
§2.12) show `"weight": 1`. The prose is right and the snippets are a copy-paste
slip: a Metro train dealt onto the road spawner drives down Lombard. `weight: 0`
matches the `sf-bay-ferry` precedent exactly.

One small correction to the plan's reasoning: it says a zero-weight entry "is
loaded into the fleet array but never dealt a road instance". In fact
`loadVehicles()` filters on `(entry.weight ?? 1) > 0` **before** loading
(`app/src/agents.js:543`), so a zero-weight entry is never fetched at all. The
effect is the same and the recommendation is unchanged.

Adding this entry costs **+1 permanent draw call** — `loadVehicles()` builds one
`InstancedMesh` per entry, `frustumCulled = false`, alive for the session.

---

## 9. Files

```
artifacts/muni-lrv/
  REFERENCE.md              research dossier, sources, measured livery geometry
  REPORT.md                 this file
  build_muni_lrv.py         deterministic build, reusable component functions
  optimize_muni_lrv.py      Stage 2 geometry shrink, ASSET_CLASS=vehicle
  validate_muni_lrv.py      fresh-scene re-import validator
  render_muni_lrv.py        elevations, top, aerial, night
  render_scenarios.py       the 1.6x in-city, coupled-pair and 120 m renders
  export_city_cell.mjs      real baked city geometry + block-face measurement
  make_contact_sheet.py     contact sheet composition
  shrink.sh                 build -> shrink -> meshopt -> validate, end to end
  muni-lrv.blend            authoring scene
  muni-lrv.glb              THE DELIVERABLE (post-shrink, post-meshopt)
  city-cell.json            the exported Judah slab the scale renders stand on
  validation.json           machine-readable contract results
  shrink.json               machine-readable shrink log
  build/  shrunk/           pre-shrink and post-shrink intermediates
  renders/                  elevations, top, aerial, night, contact sheet,
                            in-city 1.6x, coupled pair, 120 m
```

Reproduce everything with `./shrink.sh`, then
`blender -b --python render_muni_lrv.py`,
`node export_city_cell.mjs`,
`blender -b --python render_scenarios.py`,
`python3 make_contact_sheet.py`.

## 10. Reusability

`build_muni_lrv.py` is written as component functions over a `cfg` dict, matching
the muni-bus pattern:

`body_shell` · `glazing` · `window_runs` · `doors` · `livery_details` ·
`bellows` · `wheels` · `underframe` · `roof_equipment` · `pantograph` · `cab` ·
`sweep` · `lights` · `destination_sign` · `fleet_number` · `ceiling_glow`

Three extension points were built for deliberately:

- **`cab_levels`** is a table of plan outlines by height, so the cab's whole
  shape is data. A different S200 variant is a different table, not different code.
- **`nose_arc(..., trim, segs)`** places anything on the cab face from that same
  table, so a new front feature never needs its own projection maths.
- **The three-bank structure in `build()`** means a component only has to declare
  how much of the vehicle it draws; mirroring is then automatic and, critically,
  correct (§5.1).

`LINES` carries `n-judah`, `j-church` and `t-third`; `--line` selects one and
`--all-lines` builds all three. Only `muni-lrv.glb` (`N JUDAH`) is proposed for
the manifest — not for triangles but for draw calls, exactly as on the bus.
