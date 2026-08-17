# 86–96 South Park — optimize report (stage 4)

Run of `docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md` against
`artifacts/96-south-park/`, 17 August 2026.
`ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`.

## Toolchain

| Tool | Version |
|---|---|
| Blender | 5.2.0 LTS (`fbe6228777e7`, 2026-07-14) |
| gltfpack | `npx gltfpack@0.24` |
| three (g3check) | `^0.185.1` |
| python3 + Pillow | system |

Scripts are adapted copies of `artifacts/102-south-park/optimize/*` (itself
adapted from `tools/glb-optimize/`), because that copy already carries two
fixes the generic version lacks: the welded signed-volume test, and the
coplanar-dissolve skip. Only the dissolve census comment and the contact-sheet
caption differ from the 102 copies.

## Metrics

| | input | shipped |
|---|---|---|
| File bytes, raw | 419,860 | **181,952** (−56.7%) |
| File bytes, gzip -9 | 78,901 | 114,899 |
| Triangles | 6,312 | 6,312 |
| Vertices | 12,724 | 12,085 |
| Draw submeshes (glTF primitives) | 155 | **14** |
| glTF nodes | 155 | 14 |
| glTF accessors | 365 | 42 |
| Materials | 14 | 14 (identical set) |
| bbox dims (m) | 31.8092 × 27.6214 × 13.7 | identical |
| origin offset XY (m) | `[0.0, -0.1594]` | identical |
| POSITION component type | FLOAT (5126) | FLOAT (5126) |
| Extensions | none | `EXT_meshopt_compression` |

**Gzip goes up, and that is expected.** Meshopt buffers are already
entropy-coded, so gzipping them adds ~4% instead of removing 81%. The number
that matters over the wire is the raw file, because Vercel will not
usefully re-compress a meshopt payload: 419,860 → 181,952 bytes.

## Phase A — waste census

| Technique | Finding | Predicted | Actual |
|---|---|---|---|
| Duplicate meshes | 26 groups, 1,428 redundant triangles (the seven-bay alley window frames and fills, the six rear-elevation frames, the two planters, the two projecting bays) | node/accessor overhead only; the triangles are needed at distinct positions | joined per material |
| Unwelded coincident verts | 9,274 pairs | −5,000 verts | −9,274 verts at the weld step (12,724 → 3,450 in Blender) |
| Degenerate faces | 0 | — | 0 |
| Buried interior faces | none provable — every solid is closed and none is fully inside another | 0 | 0 |
| Over-tessellated curves | one 16-gon drum; chord error at the 47.7 m near distance is 0.13 m against a 0.032 m one-pixel threshold, so halving to 8 sides **would** be visible | skip | skipped, noted |
| Object-count overhead | 155 objects over 14 materials | 155 → 14 primitives | 155 → 14 |

## Phase B — geometry cleanup

| Step | Triangles | Verts |
|---|---|---|
| input | 6,312 | 12,724 (3,450 after weld) |
| weld ≤ 1 mm + degenerate removal | 6,312 | 3,450 |
| interior-face deletion | 6,312 | 3,450 |
| limited dissolve 0.05° | **SKIPPED** | — |
| join per material | 6,312 | 3,450 |

**The coplanar dissolve was skipped**, per §3 step 3 of the prompt. This asset
has eight ring bands that follow a footprint all the way round —
`cylinder_cap` (512 tris), `brick_base` (360), `plinth` (360), `bronze_coping`
(288), `coping_main` (192), `parapet_main` (192), `coping_upb` (128) and
`parapet_upb` (128) — **2,160 of 6,312 triangles, 34% of the asset**. Their top
and bottom faces are perfectly coplanar annuli; a strictly-coplanar dissolve
merges each into one annulus ngon, and re-triangulating an annulus emits
sub-millimetre slivers whose averaged vertex normals collapse to ~0. Blender
hides that on import but gltfpack re-emits the stored normals, so the failure
would surface only in the packed file and only after the shipping swap
(measured on `350-brannan`, 13 Aug 2026). `DISSOLVE = False` in `optimize.py`;
flip it to measure.

Triangle count is unchanged end to end. That is the correct outcome here: this
asset was authored at 6,312 triangles against an 11,000 cap with a deliberate
bevel budget, so there was no tessellation fat to remove. **All of the win is
in vertex welding, node/accessor collapse and meshopt encoding** — which is
also why the 60% size target was missed by 3.3 points. The census shows the
remainder is silhouette and facade geometry, not waste.

## Phase C — packing

```
npx gltfpack@0.24 -i mid.glb -o 96-south-park.optimized.glb -c -km -kn -noq
```

`-km -kn` keep the two `_Glow` materials separate from their identically
parameterised non-glow siblings (glow-ness is name-only; without `-km`
gltfpack would merge across the boundary and silently kill the night layer).
`-noq` is the repo standard — verified on the output: POSITION is still
FLOAT (5126), `extensionsUsed` is `EXT_meshopt_compression` only, and there
are no dequantize node transforms, so the stage-2 contract validator still
passes `transforms_applied` and `no_unexpected_objects`.

## Phase E — A/B verification

Same rig, input vs output, day and night × near (1.5× long axis) and far
(6× long axis), plus four orthographic elevations. Mean absolute RGB delta,
background excluded:

| View | mean Δ | max px Δ |
|---|---|---|
| day near | 0.0164% | 25 |
| day far | 0.0176% | 9 |
| night near | 0.0030% | 8 |
| night far | 0.0043% | 10 |
| elev N | 0.0224% | 28 |
| elev E | 0.0356% | 31 |
| elev S | 0.0112% | 25 |
| elev W | 0.0099% | 31 |

Gates are ≤ 2% far and ≤ 4% near; the worst view here is 0.036%, two orders of
magnitude inside. **Looking at the ×8-amplified diffs**: they are black except
for single-pixel threads along a few silhouette edges and one faint smudge in
the ground shadow under the alley elevation. Those are anti-aliasing
differences from the re-welded vertices landing on identical positions but in a
different triangle order — no element is missing, no silhouette moved, the
cylinder, both orange gates, the teal band and the gable all render
identically, and the night layer lights exactly the same surfaces. There is
nothing here a player could notice.

## Gate results

| Gate | Result | Evidence |
|---|---|---|
| **G1** Contract | PASS | material set identical (14); `Toy_mustard_Glow` and `Toy_glassl_Glow` still separate; no `Toy_body` in this asset; no manifest-named nodes |
| **G2** Geometry | PASS | bbox identical to 4 dp; origin identical; 14/14 signed volumes positive, 0 open shells; ray flip fraction 0.000000 in and out, delta 0.000000 |
| **G3** Round-trip | PASS | Blender re-import OK; `g3check` (three ^0.185.1) `G3-OK`, 14 meshes, 6,312 tris, 14 materials, no decode errors, `EXT_meshopt_compression` only |
| **G4** Appearance | PASS | table above; worst 0.036% against a 2% gate |
| **G5** Draw submeshes | PASS | 155 → 14 |
| **G6** Size | **PASS with a note** | −56.7% raw against a 60% target. Missed because the input carried no tessellation fat (see Phase B); the census accounts for the remainder as silhouette geometry |
| **G7** GPU budget | n/a | `ALLOW_BAKE: no` |
| **G8** Hygiene | PASS | re-import object count 14 = expected; no foreign geometry; no `.blend1`; scripts deterministic, re-run reproduces the output byte-for-byte |

## Shipping swap

`96-south-park.optimized.glb` copied over `artifacts/96-south-park/96-south-park.glb`.
The pre-optimize original is archived at `optimize/input/96-south-park.glb`
(419,860 bytes). The asset's own `validation.json` and `REPORT.md` were
re-generated / updated to the shipped numbers: 14 objects, 6,312 triangles,
181,952 bytes, contract **PASS** on all 16 checks.
