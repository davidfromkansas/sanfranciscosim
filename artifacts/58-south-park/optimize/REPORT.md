# 58-south-park — stage-4 optimize report

Stage 4 of the address-to-asset pipeline, run 17 August 2026 against the approved
`artifacts/58-south-park/58-south-park.glb` per `docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md`
with the defaults: `ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`.

Scripts are adapted copies of `artifacts/181-south-park/optimize/` (itself
`tools/glb-optimize/` plus two proven fixes — the flat-shading re-assert and the EEVEE A/B
engine). One per-asset change, in §3.

**Toolchain.** Blender 5.2.0 LTS (headless) · `npx gltfpack@0.24` · node v22.19.0 with
`three@^0.185.1` pinned in `g3check/` · python3 + Pillow 11.3.0 · gzip −9.

## 1. Metrics

| | Input | **Shipped** | Δ |
|---|---|---|---|
| File, raw | 281,428 B | **165,288 B** | **−41.3%** |
| File, gzip −9 | 46,626 B | 94,279 B | +102% (see §4) |
| Triangles | 4,664 | **4,664** | 0 |
| Vertices (Blender, post-import) | 9,368 | 11,370 | +21.4% (flat shading, §3) |
| Objects / nodes | 81 | **11** | −86.4% |
| Draw submeshes (primitives) | 83 | **13** | −84.3% |
| Materials | 10 | 10, identical set | — |
| BBox dims | 28.37642 × 28.48531 × 16.9 | identical to 5 dp | 0 |
| BBox min / origin offset | (−14.05198, −14.36644, 0.0) | identical | 0 |
| Inverted solids | — | none (11/11 positive) | — |
| Ray-test flipped fraction | — | 0.0% of 22,500 rays | — |

The shipped file carries `EXT_meshopt_compression` and **no** `KHR_mesh_quantization`,
matching `pipeline/compress-assets.mjs`.

## 2. Waste census (Phase A)

`inspect.json`. For a 4,664-triangle building the input was carrying:

| Finding | Size | Verdict |
|---|---|---|
| **Object-count overhead** — 81 nodes / 83 primitives across only 10 materials | the dominant cost | **fixed** by the per-material join → 11 objects / 13 primitives |
| **Unwelded coincident vertices** — 6,880 pairs | 9,368 → 2,488 verts in Blender | **fixed** by the ≤1 mm per-object weld |
| Duplicate meshes — 11 groups (3 deck seats, 3 planters, the transom bars, the gate slats, the window frames/fills) worth 1,032 redundant triangles | 22% of the model | **left alone**: these are 108-triangle boxes, and joining them per material already removes the node overhead that made them expensive. Sharing mesh data would add instancing complexity for a few hundred bytes. |
| Degenerate faces | 0 | nothing to do |
| Buried interior faces | 0 removed | the asset is a union of closed solids that touch but do not nest; the occluder rule (closed solids only) found nothing provably buried |
| Over-tessellated curves | none — the asset has **no** curved geometry at all | n/a |

Predicted before executing: node/primitive collapse ~85%, weld ~73% of vertices, no
triangle change. All three landed.

## 3. Phase B — per-asset decisions

**Step 3, the limited dissolve, is SKIPPED.** This is the one per-asset change to the
generic script, and it follows GLB-OPTIMIZE-PROMPT v2 §3 step 3 verbatim: *"Skip this step
entirely on assets with large coplanar ring bands."* This asset has three — `parapet`,
`coping` and `rear_low_cap` all follow the footprint the whole way round, and the main
coping ring is 9.7 × 30.1 m. Their top and bottom faces are perfectly coplanar annuli, so
even a strictly-coplanar dissolve merges each into one annulus ngon whose re-triangulation
emits ~0.2 mm-wide slivers up to 30 m long. Those pass an area-based degeneracy test,
survive Phase B and Phase E, and surface only two steps later as
`invalid_or_nonunit_loop_normal_count` in the **stored** normals of the packed file.

The evidence that skipping it worked: the post-swap stage-2 validator reports
`invalid_or_nonunit_loop_normal_count: 0` and `degenerate_triangle_count: 0` **on the
meshopt-packed shipping file**, which is the only place that failure is visible. On
`350-brannan` the step was worth 0.4% of triangles; here it would have been worth less,
because there is nothing curved to dissolve.

**Step 6b, the flat-shading re-assert, is kept** (inherited from 181-south-park). The
step-1 weld merges coincident verts inside each object, and where two faces of different
orientation shared those verts the loop normals get averaged — a smooth gradient across
what the style bible wants faceted. Every mesh in `build_58_south_park.py` is authored
`shade_flat()`, so re-asserting it after the weld is a restoration, not a change.

Its cost is the +21.4% vertex count in the table: flat shading splits vertices per face at
export, so Blender's 2,488 post-weld verts become 11,370 on re-import. That is a deliberate
quality choice, and it is why the raw-byte win is 41% rather than 60%.

**Step 4, curve retessellation, is not applicable** — the asset contains no curved shells.

## 4. The gzip number

Raw drops 41.3% while gzip rises 102%. This is expected and matches `181-south-park`
(−52.1% / +64.7%) and `380-brannan` (−51.8% / +102%) on the same recipe: meshopt-encoded
buffers are already compressed, so gzip cannot compress them further, while the unpacked
input's repetitive float arrays gzip extremely well.

The wins that matter here are runtime, not transfer: **84.3% fewer draw submeshes** and a
73.4% cut in Blender-side vertex data before the export split. Meshopt is also mandatory on
intake for this repo regardless of the byte arithmetic (`sf-asset-check` §8) — the loaders
register `MeshoptDecoder`, and `compress-assets.mjs` skips files that already carry the
extension, so this step is the only place the encoding is chosen.

## 5. Phase E — A/B verification

`render_ab.py` at the landmark distances (near 42.73 m = 1.5 × long axis, far 170.91 m =
6×), day and night, plus a four-elevation sheet. `diff_ab.py` → `diffs.json`:

| View | Mean abs RGB Δ | Max single-pixel Δ |
|---|---|---|
| day near | **0.0017%** | 3 |
| day far | **0.0020%** | 1 |
| night near | **0.0007%** | 2 |
| night far | **0.0006%** | 0 |
| elevation N | 0.0010% | 2 |
| elevation E | 0.0036% | 50 |
| elevation S | 0.0040% | 44 |
| elevation W | 0.0011% | 4 |

Gate G4 allows ≤ 2% far and ≤ 4% near; the worst view here is 0.004%, three orders of
magnitude inside it.

**Looked at, honestly:** the amplified diffs are black. The only non-zero pixels are
isolated single-pixel specks along the vertical edges of the window frames on the south-east
front, in the two elevations that see that facade square-on (E and S) — sub-pixel
rasterisation of an edge that moved by nothing. The night glow layer is unchanged: the
glazed bay, the two middle-storey lights, the cap-band light and the roof-office window all
render identically, and `Toy_glass_Glow` survived as its own material (`-km`). Nothing in
these images is visible to a player.

## 6. Gate results

| Gate | Result | Evidence |
|---|---|---|
| **G1 Contract** | **PASS** | material set identical (10, listed above); `Toy_glass_Glow` still separate; no `Toy_body`; no manifest node names to preserve on this asset |
| **G2 Geometry** | **PASS** | bbox identical to 5 dp; origin offset identical; 11/11 signed volumes positive; ray-flipped fraction 0.0% of 22,500 rays |
| **G3 Round-trip** | **PASS** | re-imports in Blender; `g3check` (pinned three 0.185.1) → `G3-OK {"ok":true,"meshes":13,"tris":4664,...}` |
| **G4 Appearance** | **PASS** | worst mean Δ 0.004% against a 2–4% budget; description above |
| **G5 Draw submeshes** | **PASS** | 83 → 13 |
| **G6 Size** | **PASS with note** | raw −41.3%, short of the 60% aspiration. The census shows the remainder is all visible-surface geometry: 4,664 triangles with zero degenerate, zero buried and nothing curved to retessellate, plus the deliberate flat-shading vertex split (§3). There is no waste left to take. |
| **G7 GPU budget** | n/a | bake mode off |
| **G8 Hygiene** | **PASS** | re-import object count 11 = expected; no foreign geometry; deterministic re-run reproduces the same bytes; no `.blend1` in `optimize/` |

## 7. Shipping swap

`58-south-park.optimized.glb` was copied over `artifacts/58-south-park/58-south-park.glb`;
the pre-optimize original is archived byte-for-byte at
`optimize/input/58-south-park.glb` (281,428 B, verified with `cmp` before any step ran).

The stage-2 contract validator was then re-run **against the shipped, packed file** — this
is the check the dissolve-sliver failure mode only shows up in — and passes all 16 checks:
4,664 triangles, 11 objects, dims 28.3764 × 28.4853 × 16.9, min Z 0.0, 0 invalid loop
normals, 0 degenerate triangles, 0.0% ray-flipped. The six review renders, the contact
sheet and the night render were regenerated from the shipped file, so every image in
`artifacts/58-south-park/` depicts what ships.

`artifacts/58-south-park/REPORT.md` and `validation.json` carry the shipped numbers.
