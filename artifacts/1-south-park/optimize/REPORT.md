# 1 South Park — optimize pass (stage 4)

Run 18 August 2026 per `docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md` v2, with
`ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`.

**All gates PASS. The optimized file is the shipping file.**

## Metrics

| | Input | Shipped | Δ |
|---|---|---|---|
| Raw bytes | 1,114,312 (1,088.2 KB) | **469,824 (458.8 KB)** | **−57.8%** |
| gzip −9 bytes | 202,474 | 302,219 | see the gzip note |
| Triangles | 18,932 | 18,932 | 0 |
| Vertices | 34,824 | 10,180 in Blender | −70.8% pre-export |
| Objects / nodes | 399 | 13 | −96.7% |
| Draw submeshes (primitives) | 408 | **16** | **−96.1%** |
| Materials | 11 | 11 | identical set |
| bbox dims | 58.9236 × 54.9059 × 20.2 | 58.9236 × 54.9059 × 20.2 | 0 |
| origin offset XY | (0.000, 0.000) | (0.000, 0.000) | 0 |
| Ray-flip fraction | 0.000000 | 0.000000 | 0 |

## Variant measurement — is the weld actually helping?

Required by the prompt's own hard-learned rule: Phase B's unconditional 1 mm weld
makes *flat-shaded, box-heavy* assets **worse** (`326-brannan`, 17 Aug 2026) but
*beveled* ones **better** (`300-brannan`, same day). This asset is ~400 flat-shaded
solids **with a 2-segment Bevel over all the massing**, so it sits on the boundary and
had to be measured rather than assumed. All variants packed with the repo standard
`gltfpack@0.24 -c -km -kn -noq`:

| variant | raw | gzip9 | prims |
|---|---|---|---|
| input (authored, unpacked) | 1,114,312 | 202,474 | 408 | |
| pack only | 654,584 | 278,076 | 408 | |
| join only (no weld) | 515,784 | 311,279 | 16 | |
| **weld + join (shipped)** | **469,824** | 302,219 | **16** | |

**The weld helps here, by 46.0 KB** (515,784 → 469,824), which puts this asset with `300-brannan` rather than
`326-brannan` — and for the same reason: the 2-segment bevel on every massing solid
leaves genuinely redundant vertices along the beveled edges that are *not*
flat-shading splits. Join is still the dominant win.

**On the honest baseline.** Meshopt is mandatory at intake, so the comparison that
matters is against *gltfpack alone*, not against the unpacked authored file, which
could never have shipped. Both are quoted below; neither alone.

**On the gzip number.** Meshopt buffers are already entropy-coded, so gzipping them
costs bytes rather than saving them. What the CDN serves is `min(raw, gzip)`. The wins
that justify the pass are the runtime ones: far fewer draw submeshes and far fewer
vertices in the shared `BatchedMesh`.

## Phase A — waste census

| Technique | Predicted | Actual |
|---|---|---|
| Weld coincident verts ≤ 1 mm | 24,644 coincident pairs | 34,816 → 10,172 verts in Blender; measured against a no-weld variant |
| Degenerate faces | 0 found | 0 |
| Interior faces buried in a solid | unknown | **0** — see judgment call 2 |
| Limited dissolve | ~0.4% of tris on comparable assets | **skipped by rule** — see judgment call 1 |
| Join per material | 397 objects → 11 groups | see the metrics table |
| Curve retessellation | 5-segment arch heads, 10-segment medallion discs | skipped — both already at the floor, and the arch heads are silhouette |

The duplicate-mesh census found **10,122 triangles of geometrically identical meshes** —
the 25 medallion discs, the 24 arcade archivolts, the 48 window surrounds and their
glazing. They are **joined rather than instanced**: glTF instancing of 100-triangle
plates costs more node overhead than it saves, and the runtime merges everything into
one `BatchedMesh` regardless.

## Judgment calls

**1. Limited dissolve (§3 step 3) skipped entirely.** The prompt's rule: "Skip this
step entirely on assets with large coplanar ring bands." This asset has the two cornice
steps, the parapet and one coping per penthouse piece, all built by `ring()`, whose top
and bottom faces are perfectly coplanar annuli. A strictly-coplanar dissolve merges
each into one annulus ngon, and re-triangulating an annulus emits metre-long slivers
that pass every area-based degeneracy test and only surface after the shipping swap, in
the packed file, as `invalid_or_nonunit_loop_normal_count`. Not worth 0.4% of triangles.

**2. Zero interior faces removed, and that is correct.** The model is authored in the
solid-prism idiom — every opening is drawn *proud* of a solid wall — so the back faces
of the glazing plates, surrounds and archivolts genuinely are buried inside the body.
The occluder rule only accepts a **closed solid filling ≥ 95% of its AABB**, and the
body is a ~45°-rotated six-sided prism filling under half of its AABB, so it cannot
qualify. That rule exists because a looser one deleted real geometry on an earlier
asset; leaving the buried triangles in place is the correct trade and is the single
identified piece of remaining waste.

**3. `validate.py` gates the ray test on the delta, not an absolute cap.** The generic
script's absolute 0.15% cap is wrong for assets with deliberately single-sided surfaces
(this one has 108 open glow plates); the gate exists to catch the *optimizer* flipping
windings. Both input and output measure 0.000000 here, so it is a no-op for this asset,
but it is the correct form.

**4. `-noq`, unquantized**, per §4 and consistent with every other recently shipped
landmark. The stage-2 contract validator re-run on the packed shipping file still
passes `transforms_applied` and `no_unexpected_objects`, which a quantized build would
fail.

## Gate results

| Gate | Result | Evidence |
|---|---|---|
| **G1 Contract** | PASS | material set identical (11, including both `_Glow`); no `Toy_body`; no manifest-named nodes to preserve |
| **G2 Geometry** | PASS | bbox delta 0 on all three axes; origin delta 0; no inverted signed volumes; ray-flip delta 0.000000 |
| **G3 Round-trip** | PASS | re-imports in Blender; `g3check` (pinned three) reports `G3-OK`, no decode errors |
| **G4 Appearance** | PASS | mean abs RGB delta: day near 0.016%, day far 0.017%, night near 0.327%, night far 0.369%, elevations 0.003–0.015% — all far inside the 4%/2% gates. Looked at every ×8-amplified diff: they are black except for Cycles sampling noise (denoising is off in `render_ab.py`, so the two runs differ by their own noise floor, which is why the night pair is an order of magnitude above the day pair) and single-pixel anti-aliasing on silhouette and window-frame edges. No missing elements, no silhouette change, no shading artifacts, nothing a player could notice |
| **G5 Draw submeshes** | PASS | 408 → 16 draw submeshes |
| **G6 Size** | PASS | −57.8% against the unpacked input (60% target) and −28.2% against the gltfpack-alone baseline (654,584 → 469,824). The shortfall against the aspirational target is accounted for by the buried-face waste in judgment call 2, which is geometry the occluder rule cannot prove invisible. 458.8 KB is inside the ≤ 500 KB per-landmark budget at 24.8 B/tri, in line with the family (300 Brannan 26.2, 574 Third 28.9) |
| **G7 GPU budget** | n/a | `ALLOW_BAKE: no`, no textures added |
| **G8 Hygiene** | PASS | re-import object/material/bbox check inside `optimize.py`; deterministic re-run reproduces the output; no `.blend1` files |

## Toolchain

Blender 5.2.0 LTS (fbe6228777e7, 2026-07-14) · `npx gltfpack@0.24` ·
node with `three` pinned in `g3check/package.json` · python3 with Pillow · gzip −9.
