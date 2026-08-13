# 171 South Park Street — optimize report

Stage 4 of the address-to-asset pipeline, run per
`docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md` on the approved asset in
`artifacts/171-south-park/`.

`ASSET_CLASS: landmark` · `ALLOW_MESHOPT: yes` · `ALLOW_BAKE: no` ·
`TARGET_REDUCTION: 60%`

**Result: shipped.** All eight gates pass; `171-south-park.optimized.glb` has
replaced `artifacts/171-south-park/171-south-park.glb` as the shipping file, and
the pre-optimize original is archived byte-for-byte at
`optimize/input/171-south-park.glb`.

## 1. Metrics

| | Input | Phase B (`mid.glb`) | **Shipped** |
|---|---|---|---|
| Raw bytes | 360,248 | 273,200 | **155,596** (−56.8%) |
| Gzip-9 bytes | 63,875 | 76,087 | 107,925 |
| Objects | 100 | 11 | 11 |
| Draw submeshes | 101 | 11 | **12** |
| Triangles | 5,816 | 5,808 | 5,808 |
| Vertices | 11,804 | 3,104 | 3,104 |
| BBox dims (m) | 19.2565 × 18.497 × 12.6 | identical | identical |
| Origin offset XY (m) | (−0.1247, −1.3736) | identical | identical |
| Materials | 12 | 12, same set | 12, same set |
| Vertex attributes | NORMAL | NORMAL | NORMAL (float32, `-noq`) |
| Textures | 0 | 0 | 0 |

**Gzip goes up, and that is expected.** Meshopt-compressed buffers are already
entropy-coded, so gzip cannot compress them further and adds framing. The raw
file is what the CDN serves and what the budget is measured against; it is down
56.8%. Every other meshopt landmark in this repo behaves the same way.

## 2. Waste census (Phase A) and what each technique actually returned

`inspect.py` against the input found:

| Finding | Measured | Predicted saving | Actual |
|---|---|---|---|
| Coincident vertex pairs | **8,696** | large vertex-count cut | 11,804 → 3,104 verts (−73.7%) |
| Objects sharing a material | **100 objects / 12 materials** | biggest single win (node + accessor overhead, draw submeshes) | 100 → 11 objects, 101 → 12 submeshes |
| Duplicate mesh groups | 6 skylights, 6 kerbs, brackets (2,456 redundant tris) | absorbed by join-per-material | absorbed |
| Degenerate faces | **0** | — | — |
| Buried interior faces | none provable (see below) | 0 | 0 |
| Over-tessellated curves | none — this asset has no curved shells | 0 | 0 |
| Textures | 0 | — | — |

The census explains why triangles barely moved (5,816 → 5,808, −0.14%): **the
waste in this asset was never triangles, it was topology and node overhead.**
The building is authored from closed prisms and applied panels with no curves, no
tessellated arcs and no duplicated geometry beyond what join absorbs. What is
left is silhouette: the wedge, the three facets, the cornice assembly, the two
frieze bands, the bracket row and the roof furniture.

**Interior faces were not deleted.** The occluder rule in §3.2 of the prompt only
permits treating a mesh as an occluder if it is a closed solid, and here the
applied panels (window frames, fills, glow shells, frieze bands) sit *proud of*
the body rather than inside it — the body cannot hide them, and the panels are
too thin to hide each other. Attempting it would have risked exactly the
failure the rule exists to prevent.

## 3. Phase B — per-step deltas

| Step | Tris | Verts |
|---|---|---|
| input | 5,816 | 11,804 |
| weld ≤ 1 mm + degenerate (per object) | 5,816 | 3,108 |
| interior faces | 5,816 | 3,108 |
| limited dissolve 0.05°, delimit material + sharp | 5,808 | 3,104 |
| join per material | 5,808 | 3,104 |

Per-object welding is what keeps the glow shells safe: `Toy_glass_Glow` and
`Toy_trim_Glow` are separate objects, so no weld can fuse them onto the opaque
surfaces behind them. Confirmed in the output — both glow materials survive with
their own geometry.

Normals audit after Phase B: every closed solid has positive signed volume,
`inverted_solids: []`.

## 4. Phase C — packing

```
npx gltfpack@0.24 -i mid.glb -o 171-south-park.optimized.glb -c -km -kn -noq
```

`-km -kn` keep the material and node names, which are API here: the loader
splits `*_Glow` into the unlit night layer by **name**, and without `-km`
gltfpack would merge `Toy_glass_Glow` into `Toy_glassl` (identical parameters,
different name) and silently kill the night layer. `-noq` is the repo standard
and matches `pipeline/compress-assets.mjs`; it is also what keeps this asset
passing the stage-2 contract validator's `transforms_applied` and
`no_unexpected_objects` checks, which quantization breaks by storing a dequantize
matrix as a node transform.

Preflight confirmed the app registers the decoder — `setMeshoptDecoder` appears
in both `app/src/gltf.js:10` and `app/src/assets.js:406`.

Submeshes went 11 → 12 across the pack step: gltfpack splits the multi-material
`body` object (its walls are `Toy_slate`, its top cap is `Toy_sand`) into two
primitives. That is still ≤ the input's 101, so G5 holds.

## 5. Phase D — high→low bake

**Not run.** `ALLOW_BAKE: no`, and the contract forbids textures without a
recorded exception. This asset has no bakeable relief worth the trade: its
detail is 5,808 triangles of chunky ornament, not shading.

## 6. Phase E — A/B verification

Landmark distances: near = 1.5 × long axis = 28.9 m, far = 6 × long axis =
115.5 m. Day pass renders `_Glow` at alpha 0.12 (mimicking the app's day layer);
night pass at alpha 1.0 with emission ≈ 6 under a dusk world. Both sides use
identical rigs and 32 Cycles samples (lowered from the script's 64 — this is a
same-vs-same pixel comparison and the setting is identical on both sides).

| View | Mean abs RGB delta | Max px delta | FG pixels |
|---|---|---|---|
| day near | **0.036%** | 167 | 437,331 |
| day far | **0.038%** | 22 | 30,183 |
| night near | **0.040%** | 59 | 437,331 |
| night far | **0.034%** | 20 | 30,183 |
| elevation N | 0.050% | 134 | 418,836 |
| elevation E | 0.022% | 169 | 398,052 |
| elevation S | 0.025% | 188 | 424,378 |
| elevation W | 0.033% | 144 | 396,449 |

Gate G4 allows ≤ 2% far and ≤ 4% near; the worst view here is 0.050%, roughly
**40× inside** the near budget.

**Looked at, not just measured.** Every diff image is black apart from
single-pixel antialiasing threads along silhouette edges and around the roof
furniture, plus a few faint speckled patches on window glass that are denoiser
noise rather than geometry (they appear on flat, unchanged surfaces and do not
follow any edge). The contact sheet's input and optimized rows are
indistinguishable: same three-facet front, same stepped cornice and raised
crown, same frieze bands, same pedimented entry hood, same skylight row and
mechanical box, same rear deck. Nothing is missing, no silhouette moved, no
shading artifact appeared. Nothing here is anything a player would notice.

## 7. Gate results

| Gate | Result | Evidence |
|---|---|---|
| **G1 Contract** | **PASS** | material name set identical (12, incl. both `_Glow`); `_Glow` kept separate by `-km`; no `Toy_body` (landmark); node names intact |
| **G2 Geometry** | **PASS** | bbox identical to 4 dp; origin offset identical; all signed volumes positive; ray test 22,500 rays / 16,032 hits / **0 flipped (0.00%)** |
| **G3 Round-trip** | **PASS** | re-imports in Blender; `g3check` (pinned three ^0.185.1) → `G3-OK`, 12 meshes, 5,808 tris, 12 materials, no decode errors |
| **G4 Appearance** | **PASS** | worst delta 0.050% vs 2%/4% budget; diffs inspected and described in §6 |
| **G5 Draw submeshes** | **PASS** | 12 ≤ 101 |
| **G6 Size** | **PASS (below target, justified)** | −56.8% vs 60% aspiration. The gate permits this only when the census shows the remainder is silhouette geometry — §2 shows exactly that: 0 degenerates, 0 curves to retessellate, 0 textures, and the vertex and node waste already fully recovered. Cutting further would mean cutting the building. |
| **G7 GPU budget** | **N/A** | bake mode not used |
| **G8 Hygiene** | **PASS** | re-import object/material/bbox check clean, no foreign geometry; no `.blend1` in `optimize/`; scripts are deterministic and committed here |

## 8. Post-swap re-validation

The stage-2 contract validator was re-run against the **shipped** file, not the
pre-optimize one:

```
checks 16 | failing: NONE
tris 5808 | dims [19.2565, 18.497, 12.6] | minZ 0.0 | objs 11 | mats 12
```

This is the check that would have caught a quantized build (`-noq` is why
`transforms_applied` and `no_unexpected_objects` still pass).

`artifacts/171-south-park/REPORT.md` and `validation.json` now carry the shipped
numbers, so the integration stage writes its manifest entry from reality.

## 9. Toolchain

| Tool | Version |
|---|---|
| Blender | 5.2.0 LTS (hash `fbe6228777e7`, built 2026-07-14) |
| gltfpack | 0.24 (pinned via `npx gltfpack@0.24`) |
| node | v22.19.0 |
| three (g3check) | ^0.185.1 |
| Pillow | 11.3.0 |

## 10. Deliverables

```
optimize/
  input/171-south-park.glb          # byte-identical archive of the pre-optimize asset
  171-south-park.optimized.glb      # the winner, now also the shipping file
  mid.glb                           # Phase B output, kept for reproducibility
  inspect.py optimize.py validate.py render_ab.py diff_ab.py g3check/
  inspect.json phaseb_stats.json validation.json diffs.json
  renders/                          # in_*, out_*, diff_* × day/night × near/far + 4 elevations + contact sheet
  REPORT.md
```

Re-run end to end with:

```bash
blender -b --python inspect.py -- input/171-south-park.glb inspect.json
blender -b --python optimize.py -- input/171-south-park.glb mid.glb phaseb_stats.json
npx gltfpack@0.24 -i mid.glb -o 171-south-park.optimized.glb -c -km -kn -noq
blender -b --python validate.py -- input/171-south-park.glb 171-south-park.optimized.glb validation.json
```
