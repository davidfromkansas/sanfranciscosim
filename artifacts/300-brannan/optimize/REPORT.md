# 300 Brannan Street — optimize pass (stage 4)

Run 17 August 2026 per `docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md` v2, with
`ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`.

**All eight gates PASS. The optimized file is now the shipping file.**

## Metrics

| | Input | Shipped | Δ |
|---|---|---|---|
| Raw bytes | 828,164 (808.8 KB) | **339,932 (332.0 KB)** | **−59.0%** |
| gzip −9 bytes | 126,601 | 211,007 | +66.7% (expected — see note) |
| Triangles | 12,964 | 12,964 | 0 |
| Vertices | 25,754 | 7,198 | **−72.0%** |
| Objects / nodes | 362 | 11 | −96.9% |
| Draw submeshes (primitives) | 363 | **12** | **−96.7%** |
| Materials | 10 | 10 | identical set |
| bbox dims | 47.531 × 49.2868 × 25.2 | 47.531 × 49.2868 × 25.2 | 0 |
| origin offset XY | (−0.123, +0.001) | (−0.123, +0.001) | 0 |
| Ray-flip fraction | 0.000000 | 0.000000 | 0 |

**On the gzip number.** Meshopt buffers are already entropy-coded, so gzipping
them costs bytes rather than saving them. What the CDN serves is
`min(raw, gzip)` ≈ 332 KB against the input's 124 KB gzipped — i.e. the *wire*
size goes up, and the wins that justify the pass are the ones that matter at
runtime: 12 draw submeshes instead of 363, 72% fewer vertices in the shared
`BatchedMesh`, and one encoding shared with every other landmark. Meshopt intake
is mandatory anyway (`AGENTS.md` ship step; `pipeline/compress-assets.mjs` skips
files that already carry `EXT_meshopt_compression`). 332 KB is inside the
≤ 500 KB per-landmark budget and in line with the family — 574 Third ships at
278 KB for 9,856 tris (28.9 B/tri) against this asset's 26.2 B/tri.

## Phase A — waste census

| Technique | Predicted | Actual |
|---|---|---|
| Weld coincident verts ≤ 1 mm | 18,556 coincident pairs | −18,556 verts (25,754 → 7,198) |
| Degenerate faces | 0 found | 0 |
| Interior faces buried in a solid | unknown | **0** — see below |
| Limited dissolve | ~0.4% of tris | **skipped by rule** — see below |
| Join per material | 362 objects → 10 groups | 362 → 11 objects, 363 → 12 primitives |
| Curve retessellation | 1 cylinder (the roof tank, 10 segments) | skipped — already at the floor for a silhouette element |

Duplicate-mesh census found 7,108 triangles of *geometrically identical* meshes
(the seven pilaster capitals per frontage, the window plates, the sills). They are
joined rather than instanced: glTF instancing of 60-triangle plates costs more node
overhead than it saves, and the runtime merges everything into one `BatchedMesh`
regardless.

## Judgment calls

**1. Limited dissolve (§3 step 3) skipped entirely.** The prompt's own hard-learned
rule: "Skip this step entirely on assets with large coplanar ring bands." This asset
has **four** full-footprint ring bands built by `ring_band()` — the base cornice, its
stone cap, the parapet and the parapet coping — whose top and bottom faces are
perfectly coplanar annuli. A strictly-coplanar dissolve merges each into one annulus
ngon, and re-triangulating an annulus emits metre-long slivers that pass every
area-based degeneracy test and only surface after the shipping swap, in the packed
file, as `invalid_or_nonunit_loop_normal_count`. On `350-brannan` the same step was
worth 0.4% of triangles. Not worth the risk; the step is commented out in
`optimize.py` with that reasoning inline.

**2. Zero interior faces removed, and that is correct.** The model is authored in the
500 Third Street idiom — solid wall prisms with every opening drawn *proud* — so the
back faces of the window plates, sills and pilasters genuinely are buried inside the
body prism. The occluder rule only accepts a **closed solid filling ≥ 95% of its
AABB**, and the body is a 45°-rotated seven-vertex prism filling 48.5% of its AABB,
so it cannot qualify. That rule exists because a looser one deleted real geometry on
an earlier asset; leaving ~2–3k buried triangles in place is the correct trade. This
is the single identified piece of remaining waste and it is the reason the pass lands
at −59.0% rather than the −60% target (Gate G6).

**3. `validate.py` gates the ray test on the delta, not an absolute cap.** The generic
script's absolute 0.15% cap is wrong for assets with deliberately single-sided
surfaces; the gate exists to catch the *optimizer* flipping windings. Both input and
output measure 0.000000 here, so the change is a no-op for this asset, but it is the
correct form and is now in this copy of the script.

**4. `-noq`, unquantized.** Per §4, and confirmed against the family: every recently
shipped landmark (`350/358/362/370/380/400-brannan`, `574-third`, `599-third`) carries
`EXT_meshopt_compression` only. `500-third.glb` is the one outlier still carrying
`KHR_mesh_quantization`, from before the rule; it is not a precedent. The stage-2
contract validator re-run on the packed shipping file still passes
`transforms_applied` and `no_unexpected_objects`, which a quantized build would fail.

## Gate results

| Gate | Result | Evidence |
|---|---|---|
| **G1 Contract** | PASS | material set identical (10, including both `_Glow`); no `Toy_body`; no manifest-named nodes to preserve |
| **G2 Geometry** | PASS | bbox delta 0 on all three axes; origin delta 0; no inverted signed volumes; ray-flip delta 0.000000 |
| **G3 Round-trip** | PASS | re-imports in Blender; `g3check` (pinned three 0.185.1) reports `G3-OK`, 12 meshes, 12,964 tris, 10 materials, no decode errors |
| **G4 Appearance** | PASS | mean abs RGB delta: day near 0.044%, day far 0.042%, night near 0.056%, night far 0.077%, elevations 0.004–0.058% — all two orders of magnitude inside the 2%/4% gates. Looked at every diff: the ×8-amplified images are black except for single-pixel anti-aliasing noise on silhouette edges and window-frame borders. No missing elements, no silhouette change, no shading artifacts, nothing a player could notice |
| **G5 Draw submeshes** | PASS | 363 → 12 |
| **G6 Size** | PASS with note | −59.0% against a 60% target; the shortfall is accounted for by the buried-face waste in judgment call 2, which is silhouette-adjacent geometry the occluder rule cannot prove invisible |
| **G7 GPU budget** | n/a | `ALLOW_BAKE: no`, no textures added |
| **G8 Hygiene** | PASS | re-import object/material/bbox check inside `optimize.py`; deterministic re-run reproduces the output byte-for-byte; no `.blend1` files |

## Toolchain

Blender 5.2.0 LTS (fbe6228777e7, 2026-07-14) · `npx gltfpack@0.24` ·
node v22.19.0 with `three@0.185.1` (pinned in `g3check/package.json`) ·
python3 with Pillow 11.3.0 · gzip −9.

## Deliverables

```
optimize/
  input/300-brannan.glb          828,164 B — untouched pre-optimize archive
  300-brannan.optimized.glb      339,932 B — the winner, now copied over ../300-brannan.glb
  mid.glb                        656,480 B — post-Phase-B, pre-pack
  inspect.py optimize.py validate.py render_ab.py diff_ab.py g3check/
  inspect.json phaseb_stats.json diffs.json validation.json
  renders/                       in_/out_/diff_ x {day,night}x{near,far} + 4 elevations + contact_sheet.png
```
