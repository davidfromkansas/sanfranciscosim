# 340 Brannan Street — optimize pass (stage 4)

Run of `docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md` against `artifacts/340-brannan/`.
`ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`.

Toolchain: Blender 5.2.0 LTS, `npx gltfpack@0.24`, node + the pinned three in
`g3check/`, python3 + Pillow 11.3.0, gzip −9. Scripts adapted from
`tools/glb-optimize/` via `artifacts/350-brannan/optimize/`.

## 1. Metrics

| | Input | Optimized | Δ |
|---|---|---|---|
| File, raw | 570,276 B | **256,848 B** | **−55.0%** |
| File, gzip −9 | 101,319 B | 169,895 B | +67.7% (see §4) |
| Triangles | 8,880 | 8,871 | −9 |
| Vertices (Blender re-import) | 17,999 | 17,010 | −5.5% |
| Vertices (post Phase B, pre-pack) | 17,999 | 4,788 | −73.4% |
| Objects | 176 | **13** | **−92.6%** |
| Draw submeshes (primitives) | 177 | **14** | **−92.1%** |
| Materials | 13 | 13 | unchanged |
| BBox | 41.05273 × 40.67751 × 17.79 | identical | 0 |
| Origin XY | (−0.01511, −0.11875) | identical | 0 |

## 2. Phase A — waste census

| Technique | Finding | Predicted | Actual |
|---|---|---|---|
| Object-count overhead | 176 objects across 13 materials | join to ~13 | 176 → 13 |
| Unwelded coincident verts | 13,211 pairs | large vert drop | 17,999 → 4,788 (in-Blender) |
| Duplicate meshes | 3,168 redundant tris across the 30 window frames, fills and glow shells | join (small counts, cheap meshes) | joined, not instanced |
| Degenerate faces | 0 | — | 0 |
| Buried interior faces | 0 closed-solid occluders qualified | 0 | 0 |
| Over-tessellated curves | near distance 61.58 m, 1 px = 41.5 mm | none — the only curves are the two 12-segment cooling towers, already at the miniature style's low-seg floor | skipped, recorded |
| Unused vertex data | a **UV layer on every object** | prune | removed (see §3) |

The UV layer is worth calling out: this asset has no textures and the contract
forbids them, but the `"340"` numerals are a Blender text object converted to a
mesh and that converter always emits UVs. Once Phase B joins per material, that
one object's UVs force a `TEXCOORD_0` accessor onto the whole joined `Toy_white`
group. Pruning is free and it is now step 6 of this asset's `optimize.py`.

## 3. Phase B — geometry cleanup

| Step | Tris | Verts |
|---|---|---|
| input | 8,880 | 17,999 |
| weld ≤1 mm + degenerate removal | 8,880 | 4,788 |
| interior faces (0 qualifying occluders) | 8,880 | 4,788 |
| limited dissolve | **skipped — see below** | |
| join per material | 8,880 | 4,788 |
| prune UV layers | 8,880 | 4,788 |

Joins: `Toy_trim` 66 → 1, `Toy_glass` 36 → 1, `Toy_bronze` 22 → 1,
`Toy_steel` 20 → 1, `Toy_ink` 6 → 1, `Toy_glass_Glow` 6 → 1,
`Toy_white_Glow` 6 → 1, `Toy_sage` 3 → 1, `Toy_glassl` 3 → 1,
`Toy_roofd` 3 → 1, `Toy_rust` 3 → 1. `body` (two materials) and `numerals`
keep their own meshes.

**Limited dissolve stays disabled.** This is the hazard
`GLB-OPTIMIZE-PROMPT` §3 step 3 documents, first measured on `350-brannan`
across the alley — and 340 Brannan has more of it, with a parapet `ring_band`,
a coping `ring_band` **and** a raised parapet course all following the
footprint. Their top and bottom faces are perfectly coplanar annuli, so even a
strictly-coplanar dissolve merges each ring into one annulus ngon whose
re-triangulation emits ~0.2 mm slivers. Those slivers are invisible, they pass
an area-based degeneracy test, and they fail the stage-2 contract validator only
*after* the shipping swap, because gltfpack re-emits stored normals and a
sliver's shared vertex normal averages to ~0. On 350 Brannan the step was worth
30 triangles (0.4%). Not a trade there, not a trade here.

Signed volumes are positive on all 13 output solids; `inverted_solids: []`.

## 4. Phase C — packing

```
npx gltfpack@0.24 -i mid.glb -o 340-brannan.optimized.glb -c -km -kn -noq
```

`-km -kn` keep the material and node names, which are API for the loader —
without `-km` gltfpack merges identical-parameter materials across the `_Glow`
boundary and silently kills the night layer. `-noq` is the repo standard and
matches `pipeline/compress-assets.mjs`; the ship step skips any file that
already carries `EXT_meshopt_compression`, so this pack is the final encoding.

**Gzip goes up, raw goes down.** 101 KB → 170 KB gzipped against 570 KB → 257 KB
raw. Meshopt buffers are already entropy-coded, so gzipping them a second time
adds overhead. The number that matters over the wire is the raw size — Vercel
serves `.glb` as `application/octet-stream` without re-compressing it — and the
number that matters on the GPU is the vertex buffer, which is unchanged under
`-noq`. Same behaviour recorded on `350-brannan` and `380-brannan`.

## 5. Phase D — bake

Not run (`ALLOW_BAKE: no`). No textures added.

## 6. Phase E — A/B verification

Landmark distances from the long axis of 41.05 m: near 61.6 m, far 246.3 m.
Day state renders `_Glow` at 0.12 alpha to mimic the app's day pass; night at
alpha 1.0 with emission ≈ 6 under a dusk world.

| View | Mean abs RGB Δ | Max px Δ | Gate |
|---|---|---|---|
| day near | 0.0122% | 47 | ≤ 4% |
| day far | 0.0145% | 31 | ≤ 2% |
| night near | 0.0039% | 14 | ≤ 4% |
| night far | 0.0050% | 5 | ≤ 2% |
| elevation N | 0.0051% | 50 | — |
| elevation E | 0.0087% | 35 | — |
| elevation S | 0.0138% | 41 | — |
| elevation W | 0.0092% | 25 | — |

Looked at every ×8 diff. They are black except for single-pixel outlines on
silhouette and window-frame edges — anti-aliasing landing differently once
coincident verts are welded. No element is missing, the raised central parapet
and its chamfered shoulders are intact, the `"340"` numerals are intact, the
roof furniture is intact, and the night glow set is identical (lobby bays, sign
panel, six lit windows). Nothing here is visible in the app.

## 7. Gate results

| Gate | Result | Evidence |
|---|---|---|
| G1 Contract | **PASS** | material set identical (13, both `_Glow` names preserved); no `Toy_body`; no manifest-named nodes to preserve |
| G2 Geometry | **PASS** | bbox identical to 5 dp; origin identical; 13/13 signed volumes positive; ray flip fraction **0.0** of 16,606 hits |
| G3 Round-trip | **PASS** | Blender re-import OK; `g3check` → `G3-OK {"ok":true,"meshes":14,...}` under pinned three |
| G4 Appearance | **PASS** | all deltas ≤ 0.015%, two orders of magnitude under the gates; diffs described above |
| G5 Draw submeshes | **PASS** | 177 → 14 |
| G6 Size | **PASS** | −55.0% raw, past the 60%-aspirational/measured-remainder rule; the remainder is silhouette geometry and the 1,028-triangle numerals |
| G7 GPU budget | n/a | bake mode not run |
| G8 Hygiene | **PASS** | re-import object count 13 = expected; no foreign geometry; deterministic re-run reproduces byte-identical output; no `.blend1` files |

## 8. Shipping swap

`340-brannan.optimized.glb` copied over `artifacts/340-brannan/340-brannan.glb`.
The pre-optimize original is archived at `optimize/input/340-brannan.glb`.
`artifacts/340-brannan/validation.json` and `REPORT.md` were regenerated/updated
to the shipped numbers (8,871 tris, 256,848 B), and the stage-2 contract
validator was re-run against the **packed** file: **PASS, all 16 checks**.

## 9. Reproduce

```
B=/Applications/Blender.app/Contents/MacOS/Blender
"$B" -b --python inspect.py  -- input/340-brannan.glb inspect.json
"$B" -b --python optimize.py -- input/340-brannan.glb mid.glb phaseb_stats.json
npx gltfpack@0.24 -i mid.glb -o 340-brannan.optimized.glb -c -km -kn -noq
"$B" -b --python validate.py -- input/340-brannan.glb 340-brannan.optimized.glb validation.json
(cd g3check && npm install && node check.mjs ../340-brannan.optimized.glb)
"$B" -b --python render_ab.py -- input/340-brannan.glb renders/in
"$B" -b --python render_ab.py -- 340-brannan.optimized.glb renders/out
python3 diff_ab.py renders diffs.json
```
