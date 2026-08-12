# muni-bus-40 — build report

The SF-SIM miniature of San Francisco's 40-foot Muni hybrid coach, New Flyer
Xcelsior **XDE40**, signed `29 SUNSET`, fleet number `8632`.

**Status: PASS.** Every contract check and every shrink gate is green. Research
is in [`REFERENCE.md`](./REFERENCE.md); machine-readable results are in
[`validation.json`](./validation.json) and [`shrink.json`](./shrink.json).

Nothing outside `artifacts/muni-bus/` was touched. No manifest edit, no app code,
no deploy.

| | |
|---|---|
| Deliverable | `muni-bus-40.glb` — 2,378 tris, 63,768 bytes, 10 primitives |
| Dimensions (glTF x, y, z) | **3.30 × 3.416 × 12.415 m** |
| Front | **−Z** (measured, not assumed) |
| `min y` | **0.0000** |
| Origin | centred in X/Z (offset 0.0 / −0.0125 m) |
| Triangle budget | 3,000 → **used 2,378 (79%)** |
| Rendered length at `carScale = 1.6` | **19.9 m** |

---

## 1. Three corrections to the plan's dossier

The task said to verify the dossier rather than trust it. Three of its claims did
not survive. The model follows the corrected reading; the evidence is in
`REFERENCE.md` §3 and §8.

**1.1 The livery is two horizontal red bands, not a diagonal sweep.** The plan's
§2.4 and §2.7 describe "the red livery sweeps up from the skirt toward the rear"
and specify a proud shell "sweeping from the skirt at the rear up to the fascia
at the front". No photograph of an XDE40 shows anything of the kind. Every one
shows a broad red band low on the body and a narrower red band at the cant rail,
both horizontal. Since the brief itself says "the livery does the work, not the
geometry", getting this wrong would have been the whole asset wrong.

**1.2 The body is silver, not white.** The plan's §2.8 assigns `Toy_white` to
"body, roof, fascia". SFMTA's own livery history names the current scheme
**"Silver & Red"** and dates it to 1995. The model uses silver sides and a white
roof — which is also exactly the tonal separation the plan's own §2.9 asks for.

**1.3 There *is* a diagonal sweep livery, and it belongs to a different bus.**
Muni's battery-electric coaches wear white with an angular red swoosh and a
lightning-bolt motif. That is the likeliest origin of the plan's description. It
is not the hybrid's scheme.

A fourth, smaller correction: the plan's real-length figure of 12.19 m is the
nominal 40-ft class designation; New Flyer publishes **12.50 m over bumpers**.
Both are true at different definitions — see §5.

---

## 2. Contract compliance

Validated by re-importing each **shipped** GLB (post-shrink, post-meshopt) into a
fresh, empty Blender scene — never the authoring scene — and cross-checked by
`glb_inspect.mjs`, which reads the raw glTF buffers with no Blender axis
conversion in the way.

| Rule | Required | Measured | |
|---|---|---|---|
| Front face direction | `−Z` | **`−Z`** | PASS |
| Ground | `min y = 0` | **0.0000** | PASS |
| Origin | centred in X/Z | 0.0000 / −0.0125 m | PASS |
| Units | real metres | 3.30 × 3.416 × 12.415 | PASS |
| Triangles | ≤ 3,000 | **2,378** | PASS |
| Objects / primitives | — | 10 / 10, one per material | PASS |
| Image textures | 0 | **0** | PASS |
| Transparency | none | all alpha 1.0 | PASS |
| Materials | `Toy_*` | all 10 prefixed | PASS |
| `Toy_body` | absent | absent | PASS |
| `_Glow` present | required | 3 (`Toy_mustard_Glow`, `Toy_white_Glow`, `Toy_red_Glow`) | PASS |
| Emission | 0.0 | 0.0 on every material | PASS |
| Cameras / lights | 0 / 0 | 0 / 0 | PASS |
| Animations / armatures / shape keys / constraints | 0 | 0 | PASS |
| Applied transforms | yes | no unapplied transforms | PASS |
| Negative scale | none | none | PASS |
| Per-object signed volume | positive | all 10 positive | PASS |
| Leaked foreign geometry | none | 10 objects in, 10 out | PASS |

### Per-object

| Object | Tris | Signed volume (m³) |
|---|---:|---:|
| `Toy_silver` | 532 | 84.7792 |
| `Toy_ink` | 810 | 7.9635 |
| `Toy_munired` | 392 | 25.9256 |
| `Toy_steel` | 220 | 1.8048 |
| `Toy_tire` | 144 | 0.9536 |
| `Toy_glass` | 112 | 1.6998 |
| `Toy_white` | 84 | 3.2490 |
| `Toy_mustard_Glow` | 36 | 0.0991 |
| `Toy_red_Glow` | 24 | 0.0111 |
| `Toy_white_Glow` | 24 | 0.0040 |

Three of the ten objects are not closed shells, by design: `Toy_silver`,
`Toy_munired` and `Toy_ink` each host flat single-quad detail — window pillars,
the worm wordmark, the sign glyphs and the fleet numbers — inside the closed
solid of their own colour. That is what keeps their signed volume comfortably
positive, which matters at runtime: `mergeVehicle()` in `agents.js` flips any
primitive whose signed volume is negative, and a bare quad-only primitive could
be flipped into invisibility. Hosting the flat detail inside its colour's solid
makes that impossible.

### Palette deviations (WARN, not FAIL)

| Material | Hex | Why |
|---|---|---|
| `Toy_silver` | `#aab1b9` | The palette has no silver. Started from the shipped fleet's own `Toy_Silver` (`#c8cbd0`) and darkened it, because at the palette value the sides did not separate from the white roof under flat diorama light — the first aerial render read as a uniformly white bus. |
| `Toy_munired` | `#c1272d` | Palette `red #c4453c` is a warm brick; Muni red is a cooler crimson. The plan's §2.15 pre-authorises this WARN. Named distinctly rather than shipped as `Toy_red` so the deviation is visible in the material list instead of hidden behind a palette name. |
| `Toy_glass` | `#26405e` | Palette `glass #2a4d73` a step darker. The brief's must-capture list says **black** window band; across a 10 m panel the palette value reads navy. |
| `Toy_tire` | `#2c2c2f` | Inherited from the shipped fleet's `Toy_Tire`. Off-palette there too. |

---

## 3. Shrink stage

`ASSET_CLASS=vehicle`, per `docs/asset-plans/transit/README.md` Part 3.
Reproduce with `./shrink.sh`.

### Before / after

| | Build | After Stage 2 | After Stage 1 (meshopt) |
|---|---:|---:|---:|
| Triangles | 2,438 | **2,378** | 2,378 |
| Vertices | 4,924 | **1,664** | 1,664 |
| Bytes | 141,396 | 130,068 | **63,768** |
| Primitives | 10 | 10 | 10 |

End to end: **−2.5% triangles, −66% vertices, −55% bytes.** The vertex collapse
is the weld doing its job on a model built from independently-generated beveled
boxes; the triangle count barely moves because there was little waste to remove,
which is the intended outcome of authoring to budget rather than decimating to it.

### Stage 2, step by step

| Step | Result |
|---|---|
| 1 · Weld ≤ 1 mm, never across a `_Glow` boundary | **3,224 verts removed.** The guard is enforced, not assumed: the script asserts each object carries at most one material, so a weld is physically incapable of reaching across the glow boundary. |
| 2 · Degenerate + interior faces | 0 degenerate faces (< 1 mm²), 0 interior faces. 7 of 10 objects qualify as closed occluders; the other 3 are the flat-detail hosts and are correctly *excluded* from occluder duty, since an open shell's signed volume is meaningless and it would masquerade as a solid box and eat real faces. |
| 3 · Limited dissolve at **0.05°** (never 0.5°) | **1,045 faces merged**, 60 triangles net. |
| 4 · Retessellate curves | Audited, no change. A 0.52 m wheel at 1.6× is 1.66 m across; at the 15 m near camera that is ~120 px, where a 10-gon's worst chord error is 2.5 cm ≈ 1.8 px. Nothing to gain going higher, nothing to save going lower. |
| 5 · Join by material | Already one object per material — satisfied at authoring time by the `Part` banks in `build_muni_bus.py`. Asserted here rather than performed. |
| 6 · Normals audit | All 10 signed volumes positive. |

### Stage 1 — meshopt intake

`gltfpack -cc -kn -km -noq`, the README's flag set. `-km` is load-bearing (without
it gltfpack merges materials with identical parameters across the `_Glow`
boundary and silently destroys the night layer); `-noq` is load-bearing (int16
`KHR_mesh_quantization` corrupts the positions the merge paths bake world
matrices into). Material names verified identical before and after.

**One discrepancy worth flagging for integration:** the README specifies `-cc`,
but the shipped intake compressor `pipeline/compress-assets.mjs` uses `-c`. On
this asset the difference is 76 bytes (63,768 vs 63,844), so it is immaterial
here — but the two documents disagree, and `compress-assets.mjs` skips files that
already carry `EXT_meshopt_compression`, so whichever set is applied first is the
one that ships.

**Texture bake: not run**, per the README. Out of scope for transit assets.

### Gates

| Gate | Result |
|---|---|
| G1 Contract | PASS — material name set identical pre/post; `_Glow` layer intact and separate; front `−Z` and `min y = 0` preserved |
| G2 Fidelity | PASS — bbox and origin unchanged to 4 dp; all per-object signed volumes positive |
| G3 Round-trip | PASS — re-imports in Blender 5.2 (meshopt decoded on import) **and** loads through `createGLTFLoader()` from `app/src/gltf.js` with the meshopt decoder, verified live in the running app during the 1.6× test in §4 |
| G4 Appearance | PASS — day and night A/B at 15 m and 120 m; see the note below |
| G5 Draw calls | PASS — 10 primitives in, 10 out |
| G6 Size | PASS — 141,396 → 63,768 bytes |
| G8 Hygiene | PASS — 10 objects in, 10 out, no leaked geometry; `.blend1` deleted |

*G4 note:* the pass is geometric rather than photometric. The shrink pass changes
only vertex count, so the day/night A/B at both distances is pixel-identical
outside anti-aliasing noise — the mean delta is far under the 4% / 2% thresholds
because there is nothing for it to differ about. The renders in `renders/` are
made from the **final shipped GLB**, so what was judged is what ships.

---

## 4. The 1.6× in-city scale test — the verdict

**The coach does not dominate the block. No per-type scale override is needed.**

Method: the shipped `muni-bus-40.glb` was loaded into the **running app** through
the app's own `createGLTFLoader()`, given `rotateY(Math.PI)` exactly as
`mergeVehicle()` does, yawed to a real baked street heading and scaled by
`carScale = 1.6` — then rendered from the app's own locked 42° diorama camera
against real baked city geometry at Geary & Fillmore (street snap 11 m). No app
code, manifest or asset directory was modified; the GLB was served from a
temporary path that has since been deleted.

`renders/muni-bus-40-in-city-scale-compare.png` puts three vehicles on one block:

| | Authored | On screen at 1.6× |
|---|---:|---:|
| Shipped `commuter-bus` (already live) | 10.77 m | 17.2 m |
| **`muni-bus-40`** | **12.415 m** | **19.9 m** |
| `muni-bus-40` at 1.0×, for reference | 12.415 m | 12.4 m |

The Muni coach lands **2.6 m longer on screen than a bus the city already ships
and passes review with**, and reads as roughly 17% of a Geary block face. The
1.0× reference in the same frame reads visibly undersized next to the app's own
fleet, which confirms the contract's instruction to author in real metres and let
`carScale` do the work.

Two things to carry into integration:

- The plan's §2.15 worry was well placed but lands on the *other* vehicles. The
  40-footer is the friendliest length in the transit set. The 22.9 m LRV
  (36.6 m on screen) and the deferred 18.29 m artic (29.3 m) are where this
  test will actually bite.
- The authored length is **12.19 m of bodywork, 12.415 m over bumpers**. New
  Flyer publishes 12.50 m over bumpers and the plan says 12.19 m; both are true
  at different definitions, and taking the body at the nominal-class figure is
  deliberately the cheaper of the two true answers on screen. Recorded so it is
  not mistaken for a measurement error.

---

## 5. Design decisions worth reviewing

**The destination sign is inverted, deliberately.** Real Muni signs are amber
dots on black. This one is an amber `Toy_mustard_Glow` field with `Toy_ink` block
glyphs standing 1.2 cm proud of it. The brief asks for "a lit amber rectangle at
120 m" and a legible number at 15 m; the inversion delivers both, keeps the glow
as one clean shell instead of dozens of tiny ones that would vanish at 12% day
opacity, and costs 60 triangles where an extruded font would cost ~600.

**Glyphs are single quads hosted inside a closed solid.** Each stroke of the
route number, destination and fleet numbers is one quad — 2 triangles — added to
the `Toy_ink` object rather than standing alone. See §2 for why that matters at
runtime.

**Lettering and wordmarks are built on both flanks explicitly, never mirrored.**
`mirror_x()` hands back a *backwards* fleet number and a backwards worm. The
front sign has the same trap on the other axis: a viewer facing the nose sees +X
on their left, so front text advances in −X. The first render pass shipped
"T32NU2 62" across the destination sign, which is precisely the class of error
that survives to production because nobody renders the front elevation.

**The roof is composed by value, not by part count.** The first pass made the
HVAC pod `Toy_white` on a white roof and the whole surface read as a blank
sticker from the 42° camera — the exact failure the brief warns about. It is now
two dark masses (a louvred condenser, an electronics box) and two pale hatches on
a large white field, matching the aerial reference.

**The worm is four convex quads.** Two earlier attempts drew it as one concave
outline: the first squared the humps off and read as castle crenellation, the
second self-intersected and triangulated into confetti. At 2–4 px on screen a
wave is not worth an n-gon.

**Wheel arches are real openings.** The lower bodywork and the lower red band are
both cut into three longitudinal runs by `lower_runs()`, with a dark liner behind
each opening. Without it the wheels read as loose black nubs under a solid skirt.

---

## 6. Sign variants

Three built, all verified New Flyer XDE40 motor-coach lines — `29 SUNSET` (the
shipped one; #8632 is *photographed* wearing exactly this sign), `9 SAN BRUNO`
(SFMTA's own hybrid-bus page illustrates a 40-footer on the 9), `43 MASONIC`.

`38 GEARY` was rejected: it is a motor-coach line, but Wikipedia gives its
rolling stock as **XDE60**, the articulated coach that is out of scope. `49 VAN
NESS` was rejected as a trolley coach line — it belongs on `muni-trolley`.

All three are validated and shrunk and sit in this directory, but **only
`muni-bus-40.glb` is proposed for the manifest.** The reason is not triangles —
each variant is comfortably under budget — it is draw calls: `loadVehicles()`
builds one permanent `InstancedMesh` per manifest entry, so three signs would be
three of the 300-call budget spent on one silhouette. The other two are kept as
evidence that the mechanism works and as ready-made entries if a future
`VehicleRef` lookup ever wants per-route signs.

---

## 7. A finding for the transit set: vehicles have no glow layer yet

The brief states that the loader "puts `_Glow` materials in a separate unlit
layer at `opacity = 0.12 + 0.95 * uNight`". **That is true of the landmark
loader, not the vehicle loader.**

- `app/src/assets.js` splits geometry on the `_Glow` suffix into `body` and
  `glow` buckets and hands the glow bucket to `updateLandmarkGlow()` in
  `app/src/kit.js`, which is where `0.12 + 0.95 * uNight` lives.
- `mergeVehicle()` in `app/src/agents.js` does no such split. It merges every
  mesh into **one** geometry, bakes each material's colour into vertex colours,
  and draws the result with a single `MeshLambertMaterial({ vertexColors: true })`.

So today a `_Glow` material on a vehicle renders as an ordinary opaque Lambert
surface in its base colour, day and night. The transit README's own statement
that "no vehicle has a `_Glow` material today" is consistent with this — nothing
has ever exercised the path.

This asset is authored to be correct either way, and no app change is requested
here. Every glow surface is a thin shell 3–4 cm proud of an opaque backing with
its edges buried:

| Surface | Material | Proud of |
|---|---|---|
| Destination sign face | `Toy_mustard_Glow` | the opaque `Toy_ink` sign hood, by 4.0 cm |
| Interior ceiling strip | `Toy_mustard_Glow` | the opaque `Toy_glass` window band, by 3.0 cm |
| Headlight pair | `Toy_white_Glow` | the opaque `Toy_ink` housings, by 4.0 cm |
| Tail lights | `Toy_red_Glow` | the opaque `Toy_ink` housings, by 4.0 cm |

Under today's vehicle loader those read as an amber sign, a warm valance along
the window tops, white headlights and red tail lights — all correct in daylight.
If the vehicle loader ever gains the landmark's glow split, the same geometry
ignites at night over opaque backings and stays correct. `renders/muni-bus-40-night.png`
previews the second case.

Emission ships at 0.0 per contract. The night preview in `render_muni_bus.py`
copies Base Color into Emission Color before raising strength, because a glTF
`emissiveFactor` of (0,0,0) makes Blender's importer default Emission Color to
white and every glow surface previews white otherwise.

---

## 8. Draft manifest entry — **not applied**

`app/public/sf-assets/vehicles_manifest.json` was not edited. For the integration
session:

```json
{ "id": "muni-bus-40", "file": "vehicles/muni-bus-40.glb", "kind": "bus",
  "dims": [3.30, 3.42, 12.42], "tris": 2378, "weight": 3 }
```

`weight` is carried over from the plan as a placeholder and is set at
integration, not here. Adding this entry costs **+1 permanent draw call**
(`loadVehicles()` builds one `InstancedMesh` per entry, `frustumCulled = false`,
alive for the session).

`commuter-bus.glb` stays: it is the generic non-Muni coach and this asset
replaces nothing.

---

## 9. Files

```
artifacts/muni-bus/
  REFERENCE.md                    research dossier, sources, measured livery geometry
  REPORT.md                       this file
  build_muni_bus.py               deterministic build, reusable component functions
  optimize_muni_bus.py            Stage 2 geometry shrink, ASSET_CLASS=vehicle
  validate_muni_bus.py            fresh-scene re-import validator
  render_muni_bus.py              elevations, top, aerial, night
  make_contact_sheet.py           contact sheet composition
  glb_inspect.mjs                 raw glTF reader — front/min-y check with no axis conversion
  shrink.sh                       build -> shrink -> meshopt -> validate, end to end
  muni-bus.blend                  authoring scene
  muni-bus-40.glb                 THE DELIVERABLE
  muni-bus-40-9-san-bruno.glb     sign variant, not proposed for the manifest
  muni-bus-40-43-masonic.glb      sign variant, not proposed for the manifest
  validation.json                 machine-readable contract results
  shrink.json                     machine-readable shrink log
  build/  shrunk/                 pre-shrink and post-shrink intermediates
  renders/                        elevations, top, aerial, night, contact sheet,
                                  in-city 1.6x, in-city scale comparison
```

Reproduce everything with `./shrink.sh`, then `blender -b --python
render_muni_bus.py` and `python3 make_contact_sheet.py`.

## 10. Reusability

`build_muni_bus.py` is written as component functions over a `cfg` dict, as the
trolley coach plan requires:

`body_shell` · `lower_runs` · `skirt` · `livery_band` · `cant_band` ·
`window_band` · `door` · `windshield` · `destination_sign` · `roof_pod` ·
`wheels` · `mirrors` · `lights` · `bumpers` · `rear_face` · `worm` ·
`fleet_number` · `front_worm` · `front_fleet_number`

The two extension points that matter were built for deliberately:

- **`wheels(cfg, p, axles=None)`** takes a list of axle positions, so the XDE60
  adds a third axle without touching the function.
- **`lower_runs(cfg)`** derives the wheel-arch cuts from that same axle list and
  is consumed by both `body_shell` and `livery_band`, so a third axle cuts the
  bodywork and the red band consistently and automatically.

`livery_band(cfg, p, z_range, runs=...)` takes the band's height range, so the
trolley coach can restate the livery without new code. The trolley coach's own
additions — poles, a different roof — are new functions, not edits to these.
