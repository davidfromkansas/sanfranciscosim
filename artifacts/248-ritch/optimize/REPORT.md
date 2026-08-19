# 248–250 Ritch Street — optimize pass (stage 4)

`docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md` run on `artifacts/248-ritch/`,
18 August 2026. Defaults: `ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`,
`ALLOW_BAKE: no`.

**Result: all eight gates PASS. 255,560 → 98,024 bytes (−61.6%), 131 → 9 draw
submeshes, appearance unchanged.** The optimized file is now the shipping
`artifacts/248-ritch/248-ritch.glb`; the pre-optimize original is archived
byte-for-byte at `optimize/input/248-ritch.glb`.

## Metrics

| | input | mid (Phase B) | shipped (Phase C) |
|---|---|---|---|
| raw bytes | 255,560 | 188,148 | **98,024** |
| gzip -9 bytes | 40,063 | 42,582 | 60,709 |
| triangles | 3,572 | 3,572 | 3,572 |
| vertices | 7,164 | 2,052 | 2,052 |
| mesh objects | 129 | 8 | 8 |
| draw submeshes (primitives) | 131 | 9 | **9** |
| materials | 7 | 7 | 7 |
| bbox (m) | 15.8158 × 15.8177 × 8.6 | — | 15.8158 × 15.8177 × 8.6 |

Bytes per triangle: **27.4**, against a shipped-fleet median of **27.3** across
the 90 landmarks currently in the manifest. This asset is exactly typical.

## Waste census (Phase A)

| Finding | Count | Acted on |
|---|---|---|
| coincident vertex pairs | 5,112 | yes — weld ≤ 1 mm, per object |
| join candidates | 129 objects over 7 material sets (`Toy_trim` 54, `Toy_steel` 33, `Toy_glass` 13) | yes — joined to 8 |
| duplicate mesh groups | 1,082 redundant triangles across repeated pieces (the two chimney breasts, the two entry pockets, the two drains, the bracket run) | no — joining removes the node overhead; the triangles are real geometry in distinct places |
| degenerate triangles | 0 | n/a |
| over-tessellated curves | only the three 6-sided vent prisms | no — already at the floor |
| textures | 0 | n/a |

## Phase B — geometry cleanup

| Step | tris | verts |
|---|---|---|
| input | 3,572 | 7,164 |
| 1–2a weld + degenerate | 3,572 | **2,052** |
| 2b interior faces | 3,572 | 2,052 |
| 3 limited dissolve | **skipped — see below** | |
| 5 join per material | 3,572 | 2,052 |

**Step 2b removed nothing, and that is correct.** The occluder test only accepts
closed solids that fill ≥ 95% of their axis-aligned bounding box. Every prism in
this model stands at 45.05° to the world axes, so its AABB is roughly twice its
true volume and nothing qualifies. There is no buried geometry to find here.

**Step 3 was skipped deliberately.** §3 of the optimize prompt says to skip the
limited dissolve entirely on assets with large coplanar ring bands, and this
asset is largely made of them: the cornice dentil and crown run the whole street
front and both flank returns, three parapet upstands ring the roof deck, and the
water table, the entry hood, its dentil band and the two bay caps are all long
coplanar strips. Their top and bottom faces are perfectly coplanar annuli, so
even a strictly-coplanar dissolve merges each into a single ngon, and
re-triangulating an annulus emits slivers metres long and sub-millimetre wide.

Those slivers pass an area-based degeneracy test, so nothing in Phase B or Phase
E catches them. What catches them is the stage-2 contract validator — two steps
later, *after* the shipping swap: a sliver's shared vertex sits between faces
with opposing normals, so its averaged vertex normal collapses to ~0. Blender
recomputes loop normals on import and hides it; gltfpack re-emits the stored
normals, so the failure appears only in the packed file. On `350-brannan` this
step was worth 30 triangles out of 6,770 (0.4%) and was reverted. This asset is
half that size with proportionally more band geometry, so the upside is smaller
still. Not run, and the skip is recorded in `optimize.py` rather than left
implicit.

## Phase C — packing

```
npx gltfpack@0.24 -i mid.glb -o 248-ritch.optimized.glb -c -km -kn -noq
```

`-km` and `-kn` keep the material and node names, which are API here: the
loader splits `*_Glow` into the unlit night layer, and glow-ness is name-only,
so without `-km` gltfpack would merge `Toy_glassl_Glow` into an
identical-parameter sibling and silently kill the night state. Verified on the
output rather than trusted from the flags — the packed glTF's material list is
`Toy_cream, Toy_steel, Toy_glass, Toy_glassl_Glow, Toy_ink, Toy_stone,
Toy_trim`, and the node list still reads `grp_Toy_glassl_Glow`.

`-noq` (no quantization) per the repo standard. `extensionsUsed` is exactly
`["EXT_meshopt_compression"]`.

**One honest caveat on the size number.** The −61.6% is raw bytes. *Gzipped*,
the packed file is larger than the original — 60,709 against 40,063 — because
meshopt-encoded data does not compress further. That is not specific to this
asset: every shipped landmark sits at a 0.62–0.73 gzip ratio and this one is
0.62. Meshopt is mandatory here regardless (`pipeline/compress-assets.mjs` is
the ship step named in `AGENTS.md`), and the win it buys is disk footprint,
decode speed and GPU vertex memory rather than wire bytes. Recorded so nobody
re-derives it and thinks something regressed.

## Phase E — A/B appearance (G4)

Sixteen Cycles frames, same rig, input vs output: day and night × near
(1.5 × long axis = 23.7 m) and far (6 × = 94.9 m), plus four elevations.

| View | mean abs RGB delta | max pixel delta | pixels > 8/255 after ×8 amplify |
|---|---|---|---|
| day_near | **0.0097%** | 52 | 1,719 / 691,200 |
| day_far | 0.0124% | 19 | 259 |
| night_near | **0.1273%** | 46 | 31,359 |
| night_far | 0.1254% | 26 | 2,228 |
| elev_n | 0.0273% | 123 | 3,382 |
| elev_e | 0.0232% | 87 | 3,496 |
| elev_s | 0.0039% | 83 | 1,056 |
| elev_w | 0.0055% | 121 | 1,349 |

Worst case **0.127%**, against gates of 4% near and 2% far.

**Looked at, not just measured.** The elevation diffs are a scatter of
single-pixel hairlines along the bay sill courses, the cornice edge and the roof
line — re-triangulation moving an edge by less than a pixel. The night_near diff
is a faint speckle over the surfaces nearest the lit bay: that is Cycles
sampling noise on indirect light bounced off the emissive glow plates, and it is
the reason night scores an order of magnitude above day. Nothing in any of the
eight pairs is a change a player could see.

Samples were 32 rather than the generic 64, because four concurrent CPU Cycles
jobs from sibling pipeline sessions had this machine at load 150–260 and the
pass is sixteen frames. Denoising stayed **off**: the measurement is the pair's
*difference*, and a denoiser would smooth away exactly the small shading changes
the gate exists to catch. The cost is a higher noise floor, which is what the
night_near figure mostly is, and it is still 30× inside the gate.

## Gates

| Gate | Result | Evidence |
|---|---|---|
| **G1** contract | PASS | material set identical; `Toy_glassl_Glow` separate; no `Toy_body`; node names intact |
| **G2** geometry | PASS | bbox identical to 4 dp; origin unmoved; all signed volumes positive; 0 of 22,500 rays flipped |
| **G3** round-trip | PASS | Blender re-import clean; `g3check` (pinned three.js 0.185) reports 9 meshes, 3,572 tris, correct bbox, no decode errors, only `EXT_meshopt_compression` |
| **G4** appearance | PASS | worst mean delta 0.127% vs 4%/2% gates; diffs inspected |
| **G5** submeshes | PASS | 131 → 9 |
| **G6** size | PASS | −61.6% raw, above the 60% target |
| **G7** GPU budget | n/a | bake mode off |
| **G8** hygiene | PASS | re-import object count 8, no foreign geometry; scripts deterministic; no `.blend1` left |

Re-running the stage-2 contract validator against the shipped file gives
**PASS on all seventeen checks**, including `glow_strips_face_outward` (16 faces,
16 outward) and `invalid_or_nonunit_loop_normal_count = 0` — which is the check
that the skipped dissolve would have put at risk.

## A note on the triangle count

Blender's re-import of the packed file counts **3,563** triangles; `g3check` and
the pre-pack file both count **3,572**. The nine-triangle difference is ngon
re-triangulation in the joined meshes, not lost geometry. The manifest carries
**3,572**, the number three.js — which is what the app actually runs — reports.

## Toolchain

| Tool | Version |
|---|---|
| Blender | 5.2.0 LTS (fbe6228777e7, 2026-07-14) |
| gltfpack | 0.24 (pinned via `npx gltfpack@0.24`) |
| three.js | 0.185.1 (`optimize/g3check/package.json`) |
| Python | 3 + Pillow |
