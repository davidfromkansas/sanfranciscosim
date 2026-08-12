# muni-trolley-40 — build report

The SF-SIM miniature of San Francisco's 40-foot electric trolley coach, New
Flyer Xcelsior **XT40**, signed `1 CALIFORNIA`, fleet number `5743`.

**Status: PASS.** Every contract check and every shrink gate is green. Research
is in [`REFERENCE.md`](./REFERENCE.md); machine-readable results are in
[`validation.json`](./validation.json) and [`shrink.json`](./shrink.json).

Nothing outside `artifacts/muni-trolley/` was touched. **`artifacts/muni-bus/`
is byte-identical** — its component functions are imported, never edited. No
manifest edit, no app code, no deploy.

| | |
|---|---|
| Deliverable | `muni-trolley-40.glb` — 2,596 tris, 69,640 bytes, 10 primitives |
| Dimensions (glTF x, y, z) | **3.30 × 5.791 × 12.490 m** |
| Body/footprint dimensions | 3.30 × 3.22 × 12.415 m |
| Front | **−Z** (measured, not assumed) |
| Poles | **trail aft** (measured, not assumed) |
| `min y` | **0.0000** |
| Origin | centred in X/Z — bbox offset 0.0 / 0.025 m, footprint offset 0.0 / −0.0125 m |
| Triangle budget | 3,400 → **used 2,596 (76%)** |
| Rendered length at `carScale = 1.6` | **20.0 m**; poles reach **9.3 m** |
| Depends on | `artifacts/muni-bus/build_muni_bus.py` — imported at build time |

---

## 1. The verdict the plan asked for

The plan's §2.15 calls the poles-into-empty-sky question "the one genuine open
question in this plan" and says to decide it **from the mandatory side-by-side
render against the hybrid bus, not in the abstract**. It offers three options:
ship the poles, stow them on the roof hooks, or drop the family.

**Ship the poles. Option 1, and not narrowly.**

The evidence is `renders/muni-trolley-40-vs-hybrid-bus-150m-app-min.png` and
`-120m.png`: the two coaches queued on real baked California Street geometry,
both at `carScale = 1.6`, through the app's own camera (42° pitch, 18° vertical
FOV, 1920×1080). At both distances the trolley coach is instantly the other
vehicle. The poles are not a subtle tell — they are a pair of hard diagonals
rising 3.5 m above a roofline that is otherwise identical to the bus beside it.

Two things the render also settled that were not asked:

- **The absence of a wire is a non-issue at this camera.** At 120–150 m and a
  42° downward pitch there is simply nothing above the coach to be conspicuously
  missing; the poles read as equipment reaching up, and the eye supplies the
  rest. The worry was reasonable in the abstract and does not survive contact
  with the actual frame.
- **Option 2 would have been a mistake.** Stowed poles flatten the roof to
  within a few centimetres of the hybrid's, and the side-by-side shows exactly
  how much of the recognition is carried by the vertical break. There would have
  been no reason for the asset to exist.

---

## 2. Contract compliance

Validated by re-importing each **shipped** GLB (post-shrink, post-meshopt) into a
fresh, empty Blender scene — never the authoring scene — cross-checked by
`glb_inspect.mjs` reading the raw glTF buffers with no axis conversion in the
way, and by `loader_roundtrip.mjs` loading it through the app's own
`createGLTFLoader()`.

| Rule | Required | Measured | |
|---|---|---|---|
| Front face direction | `−Z` | **`−Z`** | PASS |
| **Poles trail aft** | all pole-zone geometry at `+Z` | **z ∈ [6.100, 6.270]** | PASS |
| Ground | `min y = 0` | **0.0000** | PASS |
| Origin, footprint | centred in X/Z | 0.0000 / −0.0125 m | PASS |
| Origin, full bbox | — | 0.0000 / 0.0250 m | PASS |
| Units | real metres | 3.30 × 5.791 × 12.490 | PASS |
| Triangles | ≤ 3,400 | **2,596** | PASS |
| Objects / primitives | — | 10 / 10, one per material | PASS |
| Image textures | 0 | **0** | PASS |
| Transparency | none | all alpha 1.0 | PASS |
| Materials | `Toy_*` | all 10 prefixed | PASS |
| **Material set identical to the hybrid bus** | required by the plan §2.8 | **identical, 10 for 10** | PASS |
| `Toy_body` | absent | absent | PASS |
| `_Glow` present | required | 3 (`Toy_mustard_Glow`, `Toy_white_Glow`, `Toy_red_Glow`) | PASS |
| **No `_Glow` in the pole zone** | required — no glowing shoe | pole zone carries only `Toy_ink`, `Toy_steel` | PASS |
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
| `Toy_ink` | 900 | 8.2599 |
| `Toy_silver` | 532 | 84.7792 |
| `Toy_munired` | 392 | 25.9256 |
| `Toy_steel` | 348 | 1.9610 |
| `Toy_tire` | 144 | 0.9536 |
| `Toy_glass` | 112 | 1.6998 |
| `Toy_white` | 84 | 3.2490 |
| `Toy_mustard_Glow` | 36 | 0.0991 |
| `Toy_red_Glow` | 24 | 0.0111 |
| `Toy_white_Glow` | 24 | 0.0040 |

The plan warned that "thin swept cylinders are the most likely objects in this
asset to end up with inverted winding". They did not, and the check that would
have caught it is not the Blender one — `mergeVehicle()` in `agents.js` **flips
any primitive whose signed volume is negative**, so an inverted pole would
re-import in Blender without complaint and be silently reversed at runtime.
`loader_roundtrip.mjs` recomputes the signed volume through three's own
attribute arrays after the real loader has decoded the meshopt payload, which is
the only place that failure mode is actually visible. Result: none.

The poles are safe by construction as well as by measurement — `_ring()` in the
build script frames each pole's end rings from the pole's own axis, so a tilted,
tapered, splayed rod is still a closed loft with consistent winding.

### Delta against the hybrid bus

| | `muni-bus-40` | `muni-trolley-40` |
|---|---:|---:|
| Triangles | 2,378 | **2,596** (+218) |
| Bytes | 63,768 | **69,640** |
| Height | 3.416 m | **5.791 m** |
| Length | 12.415 m | 12.490 m |
| Materials | 10 | **the same 10** |

+218 triangles is the entire pole assembly plus the enlarged electronics box,
against the plan's 400-triangle allowance for poles. The plan budgeted 3,000 for
the inherited body and 400 for the poles; the body arrived at 2,378 because the
bus came in under its own budget, so the whole asset lands 24% under cap.

### Palette deviations (WARN, not FAIL)

Inherited from `muni-bus` unchanged — `Toy_silver #aab1b9`, `Toy_munired
#c1272d`, `Toy_glass #26405e`, `Toy_tire #2c2c2f`, each justified in that
asset's REPORT §2. **This asset introduces no new material and no new colour**,
which is the plan's §2.8 test for whether the two vehicles have diverged.

---

## 3. The pole geometry, and the one place it departs from reality

`REFERENCE.md` §4 has the full derivation. The short version, because it is the
main judgement call in this asset:

**The plan's pole numbers are internally inconsistent.** §2.7 says 6.0 m at 30°;
§2.14 says the model should end up ~5.5 m tall. A 6 m pole at 30° off a 3.5 m
base reaches 6.5 m and trails 5.2 m — 2.7 m of pole past the tail.

The model resolves it by anchoring on the only figure that is a physical
constraint rather than a modelling choice: **the wire is 5.5–6.1 m above the
street, and the shoe has to be at the wire.** That fixes the tip height at
~5.7 m. Length and angle are then free, and the model takes **3.60 m at 38°**
instead of 6.0 m at 30° — same tip height (5.74 m), whole assembly inside the
body's own length.

The pole length is therefore **compressed, deliberately**, and it is the one
measurable thing in this asset that is not true to the vehicle. Authoring the
real 5–6 m pole costs three concrete things:

1. **The contract.** A 14.5 m bounding box on a 12.2 m body puts the origin over
   a metre off the footprint the coach actually occupies.
2. **The traffic sim.** At `carScale = 1.6` that is ~4.8 m of thin pole
   projecting into whatever vehicle is behind — a visible intersection artefact
   on a road network where the spacing is not ours to choose.
3. **The manifest.** `dims[2]` would read 14.5 m for a coach with a 12.2 m road
   footprint, which is the number a later integration pass would space traffic by.

What is lost is horizontal reach. What is kept — 2.2 m of clearance above the
roof, 65% of the body height, 3.5 m on screen at 1.6× — is what actually carries
the silhouette, and §1 is the evidence that it carries it comfortably. Style
bible §26 names this move exactly: "deliberate compression of reality, not
arbitrary cartoon distortion."

**Recorded here so it is not mistaken for an error, and so a future pass that
wants the full-length pole knows what it has to solve first.**

### On the bbox and the origin

The plan predicted the height consequence of the poles and asked for it to be
recorded: **the model is 5.79 m tall, not 3.4 m, and that is correct.**
`min y = 0` is still the tyre contact patch.

It did not predict the *length* consequence, which is why §4 of `REFERENCE.md`
exists. In the shipped geometry it turned out not to bite: because the poles are
compressed, the full bbox centre offset is **0.025 m** — inside the 0.10 m gate
on its own terms, with no special pleading needed. The validator reports the
footprint-only centre (**−0.0125 m**, identical to the hybrid bus's) separately
anyway, because the two numbers diverging is the early warning that a future
pole change has pushed the origin off the road footprint.

---

## 4. Shrink stage

`ASSET_CLASS=vehicle`, per `docs/asset-plans/transit/README.md` Part 3.
Reproduce with `./shrink.sh`.

### Before / after

| | Build | After Stage 2 | After Stage 1 (meshopt) |
|---|---:|---:|---:|
| Triangles | 2,662 | **2,596** | 2,596 |
| Vertices | 5,356 | **1,738** | 1,738 |
| Bytes | 153,108 | 141,456 | **69,640** |
| Primitives | 10 | 10 | 10 |

End to end: **−2.5% triangles, −68% vertices, −55% bytes.**

### Stage 2, step by step

| Step | Result |
|---|---|
| 1 · Weld ≤ 1 mm, never across a `_Glow` boundary | **3,576 verts removed.** The guard is enforced, not assumed: the script asserts each object carries at most one material, so a weld is physically incapable of reaching across the glow boundary. |
| 2 · Degenerate + interior faces | 0 degenerate faces (< 1 mm²), 0 interior faces. 7 of 10 objects qualify as closed occluders; the other 3 host flat detail and are correctly excluded from occluder duty. |
| 3 · Limited dissolve at **0.05°** (never 0.5°) | **1,168 faces merged**, 42 triangles net. |
| 4 · Retessellate curves | Audited, no change — **and the pole assembly is excluded by name.** See below. |
| 5 · Join by material | Already one object per material — satisfied at authoring time by the `Part` banks. Asserted here rather than performed. |
| 6 · Normals audit | All 10 signed volumes positive. |

### Step 4: the poles are excluded, and the exclusion is enforced

The plan is explicit: *"Do not let the retessellation step thin the poles …
applied naively to a deliberately-exaggerated pole it will undo the
exaggeration. Exclude the poles from that step and say so in the report."*

That is not hypothetical. The poles are 8-segment lofts whose chord error at
every distance the app offers is far under a pixel — which is precisely the
argument a naive chord-error rule uses to cut a curve to 4 or 5 sides. Applied
to these poles it would take the deliberate 3.7× diameter exaggeration
(`REFERENCE.md` §6) with it, and the exaggeration is the asset.

`optimize_muni_trolley.py` finds every object with geometry above 4.5 m and
excludes it from step 4 **by assertion**, so a future edit cannot quietly drop
the exclusion. The excluded set logged in `shrink.json` is:

    ['Toy_ink', 'Toy_steel']

**The exclusion is coarser than "the poles" and that is worth naming.** Because
the model is one object per material, the poles share `Toy_steel` with the wheel
hubs and the shoes share `Toy_ink` with most of the body's dark detail. Object-
level exclusion therefore covers all of it. No geometry was lost to this: the
audit found nothing to cut from the wheels either (a 0.52 m wheel at 1.6× is
1.66 m across; at 120 m a 10-gon's worst chord error is 2.5 cm, under a pixel),
so the coarse exclusion costs zero triangles. If a future pass ever does want to
retessellate the wheels, it will have to split the objects first.

### Stage 1 — meshopt intake

`gltfpack -cc -kn -km -noq`, the README's flag set. `-km` is load-bearing
(without it gltfpack merges materials with identical parameters across the
`_Glow` boundary and silently destroys the night layer); `-noq` is load-bearing
(int16 `KHR_mesh_quantization` corrupts the positions the merge paths bake world
matrices into). Material names verified identical before and after.

The `-cc` vs `-c` discrepancy between the transit README and the shipped
`pipeline/compress-assets.mjs` that the bus report flagged still stands, and is
still immaterial at this size.

**Texture bake: not run**, per the README. Out of scope for transit assets.

### Gates

| Gate | Result |
|---|---|
| G1 Contract | PASS — material name set identical pre/post; `_Glow` layer intact and separate; front `−Z`, poles aft and `min y = 0` preserved |
| G2 Fidelity | PASS — bbox and origin unchanged to 4 dp; all per-object signed volumes positive |
| G3 Round-trip | PASS — re-imports in Blender 5.2 (meshopt decoded on import) **and** loads through `createGLTFLoader()` from `app/src/gltf.js` with the meshopt decoder, verified headlessly by `loader_roundtrip.mjs`, which additionally recomputes every primitive's signed volume the way `mergeVehicle()` does |
| G4 Appearance | PASS — day and night A/B at 90 / 120 / 150 m rendered at 1.6×; see the note below |
| G5 Draw calls | PASS — 10 primitives in, 10 out |
| G6 Size | PASS — 153,108 → 69,640 bytes |
| G8 Hygiene | PASS — 10 objects in, 10 out, no leaked geometry; `.blend1` deleted |

*G4 note:* as on the bus, the pass is geometric rather than photometric. The
shrink pass changes only vertex count, so the A/B at each distance is
pixel-identical outside anti-aliasing noise. Every render in `renders/` is made
from the **final shipped GLB**, so what was judged is what ships.

---

## 5. The 1.6× in-city test and the side-by-side

Both extra renders are produced by `render_in_city.py`, which rebuilds the city
from **the repository's own shipped tiles** — `app/public/tiles/toy/*.bin` and
`toystreets/*.bin`, decoded with the record layouts in `app/src/tilebin.js`,
with the palette and street-class widths from `toy.json`. Real footprints, real
heights, real positions, real palette: 13,162 baked buildings across 25 cells at
**California & Larkin on the 1 California**, the line the shipped sign names.

The camera is the app's: **42° pitch** (`camera.js`, `DIORAMA.pitch`), **18°
vertical FOV** (`main.js`, `camera.fov` in toy mode), 1920×1080. A pixel here is
a pixel there.

What the stand-in does *not* reproduce is the toy shader's window banding,
storefront strip, landcover, trees and street furniture — it is a massing
stand-in for scale judgement, not a second renderer. Both questions it is used
to answer depend on massing and silhouette.

### The scale verdict

**The coach does not dominate the block, and no per-type scale override is
needed.**

| | Authored | On screen at 1.6× |
|---|---:|---:|
| Shipped `commuter-bus` (already live) | 10.77 m | 17.2 m |
| `muni-bus-40` | 12.415 m | 19.9 m |
| **`muni-trolley-40`** | **12.490 m** | **20.0 m** |
| `muni-trolley-40` pole height | 5.791 m | **9.3 m** |

Length is a non-issue — the trolley is 0.1 m longer on screen than the hybrid,
which passed this test. Height is the new question, and 9.3 m of poles against
Nob Hill's two- and three-storey housing reads as **charming, not broken**: the
poles clear the parapets of the buildings the coach drives past by a couple of
metres, which is exactly what a real trolley coach does and what the overhead
wires would be at. The frame that shows this is
`renders/muni-trolley-40-in-city-1.6x.png`.

### One finding for the transit set: 120 m is not the near limit, 150 m is

The transit README budgets curve segments against "near 15 m, far 120 m". The
app does not offer either: `camera.js` sets `DIORAMA.min = 150`, so **150 m is
the closest a player can get in diorama mode**, and diorama mode is the only
mode. Every distance-based simplification argument in the transit plans is
therefore *conservative by at least 25%* — which is a good direction to be wrong
in, but worth knowing before someone spends triangles defending a 15 m view that
cannot happen.

This asset renders the side-by-side at 90 m, 120 m and 150 m for that reason.
The 150 m frame is the one that matters.

### Pole thickness: the A/B, and why the thinner one shipped

`renders/muni-trolley-40-pole-radius-ab.png` — identical frame at 150 m, the
shipped 0.095 → 0.062 m pole against a 0.115 → 0.075 m variant. Reproduce the
variant with `--pole-radius 0.115`.

The plan's §2.15 says to "err aggressively toward too thick". The shipped pole
is already 3.7× scale-accurate and measures **6.9 px at 150 m and 8.6 px at
120 m** (`REFERENCE.md` §6), which the side-by-side confirms is a legible line,
not a shimmer. Going thicker buys robustness the evidence says is not needed,
and costs something the evidence says matters more: at 0.115 m the gap between
the two poles falls from about 1.4 pole-widths to about 1.0, and the pair starts
to read as one wedge rather than as **two** poles — which is the identity the
whole asset exists to carry, and the thing the plan calls "the single most
important modeling detail".

So: thick enough to read, thin enough to still read as two. The A/B is committed
so the call can be overruled on the evidence rather than in the abstract.

---

## 6. Design decisions worth reviewing

**The body is imported, not rebuilt.** `build_muni_trolley.py` imports 18
component functions plus `Part`, the palette, the stroke font and the leak-proof
exporter from `artifacts/muni-bus/build_muni_bus.py`. The trolley adds five new
functions (`pole_plinth`, `pole_bases`, `poles`, `pole_shoes`,
`rear_face_trolley`) and one cfg override. `artifacts/muni-bus/` is unmodified —
verified by `git status`.

**The stroke font gained an `F`, without touching the bus.** No XDE40 route has
one; two of the three trolley lines do. The trolley script adds the glyph to the
shared bank at import time (`bus.LETTER.setdefault("F", ...)`) rather than
editing the bus source, so the bus GLB is provably unchanged: a new key cannot
alter a glyph the bus never draws.

**The rear loses the engine louvre band.** The bus's `rear_face()` puts a dark
louvre band across the tail at the cant rail. A trolley coach has no engine bay —
its propulsion equipment is on the roof — so `rear_face_trolley()` keeps the rear
window and drops the band, letting the red cant band run clean across the tail.
That absence is recognition cue 5 in the plan.

**The roof electronics box is enlarged rather than supplemented.** New Flyer puts
the Vossloh Kiepe inverters and resistors on the roof *ahead of* the current
collector (`REFERENCE.md` §1), so a busier roof forward of the poles is a real
difference from the hybrid, not decoration. The first pass expressed it as a
separate louvred resistor box — and the top view came back reading as a barcode:
four masses plus two hatches plus the plinth on one white field, exactly the
scatter style bible §10 warns about. Enlarging the box the bus already has says
the same thing with one fewer mass and 80 fewer triangles.

**The aerial camera moved, twice, for a reason worth recording.** The obvious
choice for this asset is a rear three-quarter, since the poles live at the back.
It is wrong: the poles trail aft, so a camera placed aft looks straight down them
and they foreshorten into stubs. The day aerial stands off the flank (yaw 118°)
where the full diagonal shows. The **night** frame needs a different answer again
— the glow set's most important surface is the destination sign and it faces dead
ahead — so night gets its own yaw (143°). Two cameras, because one frame cannot
serve both jobs.

**No glow at the pole shoe**, per the brief. Real shoes spark intermittently and
a permanently lit one reads as a rendering bug. Enforced as a validator check
(`no_glow_in_pole_zone`), not just avoided.

**The splay is 4°, not converging.** The plan's §2.4 and §2.7 disagree; the wires
are parallel at 610–700 mm, so real poles are essentially parallel. 4° puts the
tips 1.00 m apart against 0.60 m at the bases — enough that the aerial reads two
poles rather than one thick one, small enough that the pair still reads as
coupled equipment rather than as damage.

---

## 7. Sign variants

Three built, **all verified XT40 lines** — `1 CALIFORNIA` (shipped),
`22 FILLMORE`, `24 DIVISADERO`. Each is confirmed as XT40 rolling stock on its
own line article, and lines 1 and 24 are additionally photo-documented on
5701–5885 coaches.

**Three of the plan's six suggested signs were rejected as the wrong vehicle:**
`49 VAN NESS`, `30 STOCKTON` and `14 MISSION` are **XT60 articulated** lines, i.e.
the variant the plan's own §2.16 defers. `REFERENCE.md` §8.1–8.2 has the roster.
This is the same class of error the bus asset caught with `38 GEARY`, and it is
invisible unless someone checks rolling stock per line.

As on the bus, **only `muni-trolley-40.glb` is proposed for the manifest** — not
for triangles but for draw calls, since `loadVehicles()` builds one permanent
`InstancedMesh` per manifest entry. The other two are kept as evidence the
mechanism works and as ready-made entries if a future `VehicleRef` lookup wants
per-route signs.

---

## 8. Draft manifest entry — **not applied**

`app/public/sf-assets/vehicles_manifest.json` was not edited. For the integration
session:

```json
{ "id": "muni-trolley-40", "file": "vehicles/muni-trolley-40.glb", "kind": "trolleybus",
  "dims": [3.30, 5.79, 12.49], "tris": 2596, "weight": 3 }
```

`weight` is carried over from the plan as a placeholder and is set at
integration, not here. Adding this entry costs **+1 permanent draw call**.

Two notes for whoever applies it:

- **`dims[1]` is 5.79 m and that is correct** — it is the pole tip, not the roof.
  The body height is 3.22 m and the road footprint is 3.30 × 12.415 m. If
  anything downstream wants a *clearance* height rather than a bounding height,
  it wants the body figure, and the two now differ by 2.6 m for the first time in
  this fleet.
- **This asset and `muni-bus-40` share a build script.** If the bus changes,
  re-run `artifacts/muni-trolley/shrink.sh` and re-ship both. The dependency is
  noted in both reports.

---

## 9. Files

```
artifacts/muni-trolley/
  REFERENCE.md                        research dossier, sources, pole derivation
  REPORT.md                           this file
  build_muni_trolley.py               deterministic build; IMPORTS the bus components
  optimize_muni_trolley.py            Stage 2 shrink, poles excluded from retessellation
  validate_muni_trolley.py            fresh-scene re-import validator
  render_muni_trolley.py              elevations, top, aerial, night
  render_in_city.py                   1.6x in-city + side-by-side, from the baked tiles
  make_contact_sheet.py               contact sheet composition
  glb_inspect.mjs                     raw glTF reader — front/min-y with no axis conversion
  loader_roundtrip.mjs                gate G3 through the app's OWN loader
  shrink.sh                           build -> shrink -> meshopt -> validate, end to end
  muni-trolley.blend                  authoring scene
  muni-trolley-40.glb                 THE DELIVERABLE
  muni-trolley-40-22-fillmore.glb     sign variant, not proposed for the manifest
  muni-trolley-40-24-divisadero.glb   sign variant, not proposed for the manifest
  validation.json                     machine-readable contract results
  shrink.json                         machine-readable shrink log
  build/  shrunk/                     pre-shrink and post-shrink intermediates (gitignored)
  renders/                            elevations, top, aerial, night, contact sheet,
                                      in-city 1.6x, side-by-side at 90/120/150 m,
                                      pole-radius A/B
```

Reproduce everything with `./shrink.sh`, then:

```bash
blender -b --python render_muni_trolley.py -- --samples 96
blender -b --python render_in_city.py -- --samples 72
python3 make_contact_sheet.py
node loader_roundtrip.mjs muni-trolley-40.glb
```

`loader_roundtrip.mjs` needs `npm install` in `app/` (three is already a
dependency there; nothing new is added).
