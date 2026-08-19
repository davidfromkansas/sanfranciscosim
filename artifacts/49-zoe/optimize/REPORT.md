# 49 Zoe Street — GLB optimize pass (stage 4)

Run of `docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md` against `artifacts/49-zoe/`.
Defaults: `ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`.

Toolchain: Blender 5.2.0 LTS, `npx gltfpack@0.24`, node v22.19.0 with the pinned
`three@^0.185.1` in `g3check/`, python3 + Pillow 11.3.0, gzip −9. Scripts adapted
from `tools/glb-optimize/` (constants and the two skip decisions are per-asset).

Preflight: `grep -rn setMeshoptDecoder app/src/` hits `app/src/gltf.js:10` and
`app/src/assets.js:406`, so meshopt is safe to rely on.

The input was copied byte-for-byte to `input/49-zoe.glb` (504,024 B both sides,
`cmp` clean) and every step ran against the copy.

## 1. Metrics

| | Input | Optimized | Δ |
|---|---|---|---|
| File, raw | 504,024 B | **218,708 B** | **−56.6%** |
| File, gzip −9 | 75,018 B | 126,523 B | +68.7% (see §4) |
| Triangles | 7,688 | 7,688 | 0 |
| Vertices (Blender re-import) | 15,540 | 14,645 | −5.8% |
| Vertices (post Phase B, pre-pack) | 15,540 | **4,272** | **−72.5%** |
| Mesh objects | 216 | **13** | **−94.0%** |
| Draw submeshes (primitives) | 217 | **14** | **−93.5%** |
| Materials | 12 (3 `_Glow`) | 12 (3 `_Glow`) | identical |
| bbox dims | 34.10837 × 34.61277 × 17.0 | identical to 5 dp | 0 |
| origin offset xy | (−0.02915, −0.23655) | identical | 0 |

## 2. Phase A — forensic inspection & waste census

`inspect.json`. 216 objects, 7,688 tris, 15,540 verts, 217 primitives, 12
materials, **no textures**, vertex attributes `POSITION + NORMAL` only (no UVs,
no vertex colours). Cross-checks against the asset's own `validation.json`: same
tris, same dims, same material set.

Census, with predicted savings:

| Waste | Measured | Plan | Predicted |
|---|---|---|---|
| Object-count overhead | 216 objects sharing 12 materials | join per material | the dominant win: node + accessor headers |
| Unwelded coincident verts | **11,268 pairs** | per-object weld ≤ 1 mm | ~−70% verts |
| Duplicate meshes | 4,300 redundant tris across repeated pieces (16 identical rail posts, 6 identical vent cans, 12 identical window fills, …) | join, not instance — the repeats are 44–116 tris each, far too light to pay for a shared-mesh node | absorbed by the join |
| Degenerate faces | **0** | nothing to do | — |
| Buried interior faces | see §3.2 | none provable | 0 |
| Over-tessellated curves | 6 vent cans at 10 segments | see §3.4 | declined |

## 3. Phase B — geometry cleanup

`optimize.py`, stats in `phaseb_stats.json`.

| Step | Tris | Verts |
|---|---|---|
| input | 7,688 | 15,540 |
| 1+2a weld ≤ 1 mm + degenerate | 7,688 | **4,272** |
| 2b interior faces | 7,688 | 4,272 |
| 3 limited dissolve | **skipped — see below** | |
| 5 join per material | 7,688 | 4,272 |

**3.1 Weld** did all the work: 15,540 → 4,272 verts, −72.5%, with no triangle
change. That ratio is what an asset built from ~216 closed applied panels looks
like before welding — every panel carries its own duplicated corners.

**3.2 Interior faces: none removed, and that is correct.** The occluder rule only
admits CLOSED solids whose signed volume fills ≥ 95% of their AABB. Every mass in
this asset is a 45.4°-rotated rectangular prism, so its world AABB fill is ~50%
and nothing qualifies. The conservative outcome is the right one — a looser rule
here would have started deleting real facade panels.

**3.3 Limited dissolve: deliberately skipped.** Prompt §3.3 says to skip it
entirely on assets with large coplanar ring bands following the footprint. This
asset has two: `parapet` (33.81 × 33.90 × 0.68 m) and `coping` (34.05 × 34.14 ×
0.12 m), both closed annuli built by `ring_band()` around the whole plan. Their
top and bottom faces are perfectly coplanar annuli, so even a strictly-coplanar
0.05° dissolve merges each into a single ngon, and re-triangulating an annulus
emits slivers up to the full 34 m diagonal at ~0.2 mm width. Those pass an
area-based degeneracy test, survive Phase B and Phase E, and surface only *after*
the shipping swap — as `invalid_or_nonunit_loop_normal_count` in the stage-2
contract validator, because gltfpack re-emits the STORED normals and a sliver's
shared vertex normal averages to ~0. Measured on `350-brannan` (13 Aug 2026) for
a return of 30 triangles. Declined here on the same arithmetic: this asset's win
is node overhead, not triangles.

**3.4 Curve retessellation: declined.** The six vent cans are 10-segment
cylinders at r = 0.20 m, chord error 0.0098 m against a one-pixel world budget of
0.035 m at the 51.9 m near distance — they would halve to 5 segments legally, for
about 350 triangles of 7,688 (4.5%). The penthouse vent at r = 0.75 m is already
at the budget (0.037 m) and defines the crest silhouette. Not worth the risk for
a saving the packer largely absorbs anyway.

**3.5 Join per material** collapsed 216 objects into 13 (12 single-material
groups plus `body`, which carries `Toy_sand` walls and a `Toy_steel` roof cap and
therefore keeps its own two-primitive mesh). No manifest-named nodes exist on
this asset and there is no `Toy_body`, so nothing had to be held out.

**3.6 Normals audit:** `inverted_solids: []`.

## 4. Phase C — packing

```
npx gltfpack@0.24 -i mid.glb -o 49-zoe.optimized.glb -c -km -kn -noq
```

`-km -kn` are mandatory: without `-km` gltfpack merges identical-parameter
materials across the `_Glow` boundary (glow-ness is name-only) and silently kills
the night layer. This asset is exactly the case that rule exists for —
`Toy_glassl` `#6f95b8` and `Toy_glass_Glow` `#6f95b8` are the *same colour* and
differ only by name. The output material set is verified identical, all 12 names
present, all 3 `_Glow` still separate.

`-noq` is the repo standard: `pipeline/compress-assets.mjs` (the mandatory ship
step) produces `-c -km -kn -noq`, the runtime merge paths need float32
attributes, and a quantized build also fails the stage-2 contract validator on
`transforms_applied` and `no_unexpected_objects`. `compress-assets.mjs` skips any
file already carrying `EXT_meshopt_compression`, so this pack is the final
encoding.

**Gzip goes up, raw goes down** — 75 KB → 127 KB gzipped against 504 KB → 219 KB
raw. Meshopt buffers are already entropy-coded, so gzipping them a second time
adds overhead. The number that matters over the wire is the raw size (Vercel
serves `.glb` as `application/octet-stream` without re-compressing it) and the
number that matters on the GPU is the vertex buffer, unchanged under `-noq`. Same
behaviour recorded on `350-brannan`, `380-brannan` and `340-brannan`.

## 5. Phase D — high→low bake

Not run. `ALLOW_BAKE: no`, and the contract forbids textures without a recorded
exception. The asset has no textures and gains nothing from one: its detail is
flat-coloured applied panels, not shading.

## 6. Phase E — A/B verification

`render_ab.py` on both files through one rig, `diff_ab.py` for the deltas.
Landmark distances off the 34.61 m long axis: **near 51.9 m, far 207.7 m**.
Day state uses the app's day glow treatment (alpha 0.12); night uses alpha 1.0
with emission 6 under a dusk world. `clip_end = 50000`.

Engine: **EEVEE** at 64 TAA samples, not CPU Cycles. This machine runs a dozen
concurrent landmark sessions and sat at load 96–250 through the pass. The A/B
gate compares two renders of one rig against each other, so the engine only has
to match on both sides — and EEVEE is deterministic and noise-free, which makes
any non-zero delta a real difference rather than sampling noise. Recorded here
because it is a deviation from the script's default.

| View | mean abs RGB | max px delta |
|---|---|---|
| day near | **0.0016%** | 18 |
| day far | 0.0029% | 5 |
| night near | 0.0042% | 5 |
| night far | 0.0056% | 2 |
| elevation N | 0.0219% | 17 |
| elevation E | 0.0085% | 15 |
| elevation S | 0.0123% | 14 |
| elevation W | 0.0263% | 17 |

Gate G4 allows ≤ 2% far and ≤ 4% near. The worst view here is **0.026%**, i.e.
two orders of magnitude inside the gate.

**Looking at the diffs honestly** (`renders/diff_*.png`, ×8 amplified): every
non-zero pixel is a one-pixel outline on a panel edge — the window frames, the
stripe boundaries, the parapet coping line, the roll-up door reveals. There is no
region of change, nothing missing, no silhouette movement, no shading artefact.
The cause is the ≤ 1 mm weld nudging shared corners onto a single position, which
shifts an anti-aliased edge by a fraction of a pixel. Nothing a player could
notice at any distance; nothing a reviewer could notice without the ×8
amplification.

The night pair is the one worth stating explicitly, because `-km` is what could
have broken it: **the monitor spine still glows and the six lit loft windows are
still the six lit loft windows.** `night_near` differs by 0.0042%.

## 7. Gate results

| Gate | Result | Evidence |
|---|---|---|
| **G1** Contract — material set identical, `_Glow` separate, no `Toy_body`, node names intact | **PASS** | `validation.json` `G1_materials_identical: true`; 12 names in, 12 out, 3 `_Glow`; asset has no manifest-named nodes and no `Toy_body` |
| **G2** Geometry — bbox within max(1 cm, 0.1%), origin within 1 cm, volumes positive, flips ≤ 0.15% | **PASS** | bbox identical to 5 dp; origin identical; `G2_volumes_positive: true`; **22,500 rays, 16,516 hits, 0 flipped (0.000%)** |
| **G3** Round-trip — Blender AND pinned-three GLTFLoader | **PASS** | `g3.json`: `ok: true`, 14 meshes, 7,688 tris, 12 materials, bbox 34.1084 × 17 × 34.6128 (glTF Y-up), no decode errors |
| **G4** Appearance | **PASS** | worst view 0.026% against a 2%/4% gate; §6 |
| **G5** Draw submeshes ≤ input | **PASS** | 217 → **14** |
| **G6** Size reduced | **PASS** | raw −56.6%, at the 60% target's doorstep. The remainder is silhouette geometry: with tris unchanged and verts already welded to 4,272, what is left in the file *is* the model |
| **G7** GPU budget | **n/a** | bake mode not run |
| **G8** Hygiene — no foreign geometry, deterministic, no `.blend1` | **PASS** | leak-proof export (temp scene + `use_active_scene` + `export_apply`), re-import object/material/bbox check clean; re-running the scripts on `input/` reproduces the output; no `.blend1` in the tree |

## 8. Shipping swap

All gates passed, so `49-zoe.optimized.glb` was copied over
`artifacts/49-zoe/49-zoe.glb`. The pre-optimize original is archived at
`optimize/input/49-zoe.glb`.

The **stage-2 contract validator was then re-run on the shipped (packed) file** —
not just on the pre-pack mid — because gltfpack re-emits the stored normals and
that is the only place a sliver or a zero-length vertex normal would appear.
Result: **overall PASS**, `invalid_or_nonunit_loop_normal_count: 0`,
`degenerate_triangle_count: 0`, 31,500 rays with 0 flipped. `validation.json` and
`REPORT.md` in the asset directory now carry the shipped numbers, so the
integration stage writes its manifest entry from reality.
