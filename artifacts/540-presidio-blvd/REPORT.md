# 540 Presidio Boulevard — build report

`540-presidio-blvd.glb` — a validated miniature of the 1912 Colonial Revival officers'
quarters at 540 Presidio Boulevard, Presidio of San Francisco.

**This report beats the plan.** Where `docs/asset-plans/540-presidio-blvd.md` and this
file disagree, this file records what was actually built and measured.

## Deliverables

| File | What it is |
|---|---|
| `540-presidio-blvd.glb` | the shipping asset **after the stage-4 optimize pass** — 112,108 bytes, meshopt-compressed, 10 draw submeshes. The pre-optimize original is archived at `optimize/input/`. |
| `540-presidio-blvd.blend` | the build's saved scene |
| `build_540_presidio_blvd.py` | deterministic build — rebuilds the GLB byte-for-byte |
| `validate_540_presidio_blvd.py` | fresh-scene contract validation of the exported GLB |
| `render_540_presidio_blvd.py` | the review render rig (`-- --night` for the dusk pass) |
| `make_contact_sheet.py` | composes the contact sheet |
| `validation.json` | the machine-readable validation report — **overall PASS** |
| `REFERENCE.md` | the research dossier and its confidence labels |
| `*-north/east/south/west/top/aerial.png`, `*-aerial-night.png`, `*-contact-sheet.png` | review renders, all from the re-imported GLB |

Reproduce:

```bash
blender -b --python build_540_presidio_blvd.py \
  && blender -b --python validate_540_presidio_blvd.py \
  && blender -b --python render_540_presidio_blvd.py \
  && blender -b --python render_540_presidio_blvd.py -- --night \
  && python3 make_contact_sheet.py
```

## The numbers

| | |
|---|---|
| Objects | **10** mesh objects shipped (76 as authored; joined per material in the optimize pass) |
| Triangles | **3,690** shipped (3,712 as authored; gltfpack dropped 22 degenerates). Cap 6,000; contract 30,000 |
| Dimensions | **16.6623 × 22.7566 × 11.5 m** |
| Bounding box | min `[−8.3312, −11.3783, 0.0]`, max `[8.3312, 11.3783, 11.5]` |
| Min Z | **0.0** · XY centre offset **[0.0, 0.0]** |
| Materials | 10, all `Toy_*`, all flat, all alpha 1.0, roughness 0.85 — unchanged by the optimize pass |
| Glow materials | `Toy_glass_Glow`, `Toy_gold_Glow` |
| File size | **112,108 bytes** raw / 71 KB gzipped (budget 500 KB compressed). The pre-optimize file was 234,548 raw / 36 KB gzipped — see `optimize/REPORT.md` §4 on why meshopt raises the gzip number and why it ships anyway |
| Loader scale | **1.000** — max Z is normalised to `targetHeightM` exactly |

The XY box (16.7 × 22.8 m) is larger than the 14.47 × 19.72 m footprint because it is the
+6.49° rotation of a footprint grown by the 0.75 m roof overhang, the porch, the entry
steps and the hedges. That is expected, not a scale error.

## Corrections made to the plan during the build

The plan is a research document written before any geometry existed; three of its numbers
moved once the model was real. All three are improvements, and all three are recorded
here rather than quietly applied:

| Plan said | Built | Why |
|---|---|---|
| Ridge **9.9 m**, from 4:12 over the 5.72 m *wall* half-span | Ridge **10.50 m**, from 4.5:12 over the **6.47 m eave half-span** | The plan measured the rise from the wall face, but the roof actually springs from the overhang edge, 0.75 m further out. Measuring from the real eave edge is the correct derivation. The steeper 4.5:12 was then chosen over 4:12 because at 4:12 the roof read as a flat red plate from the app's downward camera — the first aerial review render made that obvious. Chimney clearance above the ridge falls from 1.6 m to 1.00 m, which is still a normal clearance. **The 11.50 m top is unchanged**, so nothing downstream moves. |
| Eave overhang **0.9 m** | **0.75 m** | At 0.9 m the roof read as a lid floating over the walls in the aerial. 0.75 m still doubles the shadow line's visibility over the real ~0.6 m without detaching the roof. |
| Palette: roof `Toy_brick`, walls `Toy_cream`, no ridge tiles | Roof `Toy_red`, chimneys `Toy_brick`, plus terracotta ridge and hip caps | `artifacts/1008-general-kennedy/` was found mid-plan and is the same Presidio type; style bible §24 says build families, so the roof adopted 1008's `Toy_red` and its "chimneys in `Toy_brick`, deliberately not the roof colour" reasoning. The ridge/hip caps were added after the first top-view render: see below. |

One further change, made against the plan's own massing table: the plan called for a
single plinth under the whole house. Built as **three separate bases** (body, service bay,
porch deck), because one continuous slab read as a terrace the house does not have.

## The one detail that mattered most

The first top view was a blank red plane. `roof:shape=hipped` was modelled correctly —
real ridge, four real hips at 45° in plan — but with a single flat material the hip lines
carried no value change and the roof read as a lid.

Adding **ridge and hip tiles** as five thin `Toy_brick` bars centred on the ridge and hip
lines (half above the roof plane, half below, exactly how capping courses sit on a real
tile roof) cost **~250 triangles** and turned the roof into the building's strongest
surface. On a house whose whole identity is its roof, and in an app whose camera looks
down, that is the highest-value 250 triangles in the asset. A sixth bar caps the porch
roof so it reads as the same tile roof rather than a painted awning.

## Night state

Five glow objects, two glow materials — a small building gets a small night state.

| Surface | Material | Reads as |
|---|---|---|
| `glow_lantern` | `Toy_gold_Glow` (`caa64a`) | the porch lantern over the entry: the hero, the only warm point, and the only thing that spills light onto the porch |
| `win_e_hi_1_glow`, `win_e_hi_2_glow` | `Toy_glass_Glow` (`6f95b8`) | two lit rooms on the east front |
| `win_n_hi_0_glow`, `win_n_lo_1_glow` | `Toy_glass_Glow` | two more on the north end, so the night state is not invisible from half the camera's orbit |

**The constraint every one of them obeys.** Nothing in the GLB switches: `assets.js`
splits the file into a lit body buffer and one unlit glow buffer purely by the `_Glow`
material-name suffix, and `updateLandmarkGlow` in `kit.js` ramps that buffer's opacity
from **0.12 to 1.0** as `shared.uNight` goes 0 → 1. So a glow face is still drawn at
noon, 88% transparent — which means it can never be the only skin at its spot. Here every
glow pane is 0.04 m proud of an opaque recessed `Toy_glass` fill, and the lantern hangs
under the solid porch roof. Nothing goes see-through in daylight.

The glow colour is `6f95b8` (palette `glassl`), not the `2a4d73` of the glass behind it:
a lit pane has to be *lighter* than the dark glass to read as lit. At the app's daytime
12% opacity that leaves the lit panes a barely perceptible shade lighter than their
neighbours — visible if you look for it in the east elevation, invisible at any real
camera distance. The day renders reproduce that honestly by putting alpha 0.12 on the
same materials rather than rendering them solid.

The night render sets `_Glow` emission to **2.0**, not the 6.0 the sibling artifact used.
`assets.js` draws the glow set as a flat unlit `MeshBasicMaterial` with no bloom, so a hot
value flatters the asset into something the scene never shows; 2.0 is the smallest value
that survives the render's Standard view transform at this exposure.

## Contract validation

Fresh factory-reset Blender scene, importing **only** the exported GLB — the source
`.blend` is not inspected. Run twice: once on the authored export, and again on the
optimized file after the stage-4 shipping swap. Both **overall PASS**; the numbers below
are the shipped ones.

| Check | Result | Measured |
|---|---|---|
| Metres, plausible dimensions | PASS | 16.66 × 22.76 × 11.50 m |
| Crest normalised to target | PASS | max Z = 11.5000, target 11.5 → loader scale 1.000 |
| Base at z = 0 | PASS | min Z = 0.0 |
| Centred in XY | PASS | offset [0.0, 0.0] |
| Under triangle budget | PASS | 3,690 / 6,000 |
| No image textures | PASS | 0 images, 0 textured materials |
| No transparency | PASS | every material alpha 1.0 |
| Materials follow contract | PASS | 10 materials, all `Toy_*`, no `Toy_body` |
| No cameras or lights | PASS | 0 / 0 |
| No animation, skin or constraints | PASS | 0 f-curves, 0 armatures, 0 constraints |
| Transforms applied | PASS | every object identity transform |
| No negative scales | PASS | — |
| Normals outward (signed volume) | PASS | **10 / 10** objects positive |
| Normals outward (ray test) | PASS | 31,500 rays, **0** flipped first faces (0.0000%) |
| No degenerate geometry | PASS | 0 triangles under 1e-8 area |
| No unexpected objects | PASS | 10 meshes, nothing else |

Every solid in this asset is closed, so the per-object signed-volume test is
authoritative and the ray test is a redundant second opinion. It came back at exactly
zero, not merely inside the 0.15% coincident-face tolerance.

## Orientation and placement

- Authored in **true-world orientation**: Blender +Y = north, +X = east, with the plan's
  **+6.49° CCW** yaw baked into the geometry. `placeGeneric()` never rotates, so the
  house lands on its real heading with no manifest `yawDeg`.
- **The porch front bears 83.51° true — it faces east**, onto the walk that descends to
  Presidio Boulevard. Evidence for that in `REFERENCE.md` §5.
- The contract's "front faces −Y" rule is superseded here by true-world orientation, as
  `docs/asset-plans/README.md` requires for every asset whose real front is not south.
- The build recentres to the XY bbox centre and shifts the anchor by the same vector, so
  the origin obeys contract rule 2 while the building stays on its real footprint:
  footprint OBB centre `−122.4519267, 37.7966669` + `[0.380 m E, −0.025 m N]` →
  **manifest anchor `−122.4519224, 37.7966667`**.

## Draft manifest entry

```json
{
  "id": "540-presidio-blvd",
  "file": "540-presidio-blvd.glb",
  "anchor": [-122.4519224, 37.7966667],
  "targetHeightM": 11.5,
  "cat": 1,
  "name": "540 Presidio Boulevard",
  "estimated": true,
  "dims": [16.6623, 22.7566, 11.5],
  "tris": 3690,
  "loadRadius": 2500
}
```

`"estimated": true` because the 11.5 m height is derived, not published — the full
derivation and its error bar are in `REFERENCE.md` §4.

`loadRadius: 2500` is the default rule `max(2500, targetHeightM × 30)`. The skill's
absence-illegibility test passes trivially at any radius past ~600 m for an 11.5 m house,
so there was no reason to tune below the default. `alwaysLoaded` would be absurd here.

`cat: 1` (House) rather than `2` (Apartments) is a judgement call for a two-unit rental;
House matches the built form the model shows.

## Optimize pass (stage 4)

Full account in `optimize/REPORT.md`. Summary: 76 objects → 10 (joined per material),
7,686 → 2,002 vertices (weld ≤ 1 mm), 234,548 → 112,108 raw bytes, meshopt-compressed with
`-c -km -kn -noq`. All eight gates pass; the largest A/B pixel delta across day/night ×
near/far is **0.19%** against a 2% gate. Gzipped bytes rise from 36 KB to 71 KB, which is
inherent to meshopt and is declared rather than buried — and the repo's mandatory ship step
(`pipeline/compress-assets.mjs`) applies the same compression regardless.

## Known limitations

Stated plainly, because a hidden FAIL is worse than a declared one:

1. **The height is derived, not measured.** Eave 8.0 m is well corroborated; the 4.5:12
   pitch and the 1.0 m chimney clearance are conventions. Worst case the top is off by
   ~0.7 m (6%). The manifest says `estimated: true`. A Presidio Trust or NPS inventory
   record with a measured height would supersede it — one constant (`Z_CREST`) and one
   manifest field.
2. **Three of the four elevations are inferred.** Street-level imagery of 540 itself was
   unreachable in this session (Google Maps, Bing Bird's Eye and Mapillary all failed to
   load in the available browser). The east front is evidenced by a photograph of the
   near-identical 544; north, south and west are honest reconstructions of a type. Window
   positions and counts on every elevation are invented rhythm, not survey.
3. **The row is four near-identical houses** (540/541/542/543). This asset leaves a
   bespoke house standing next to three baked boxes — visible at close range. The
   honest fix is to build the row as a family later; it is not a reason to skip the
   exclusion zone, because a doubled building is worse than a plain neighbour.
4. **Terrain sensitivity.** On a wooded rise, at 11.5 m tall, a metre of terrain sampling
   error is 9% of the building. Integration QA must check the seating at street level,
   not only from the air.
