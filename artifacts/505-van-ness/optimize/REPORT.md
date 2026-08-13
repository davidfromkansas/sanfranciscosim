# 505 Van Ness Avenue — GLB optimize report (stage 4)

Run of `docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md` against
`artifacts/505-van-ness/`. `ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`,
`ALLOW_BAKE: no`. Scripts adapted from `tools/glb-optimize/`.

Toolchain: Blender 5.2.0 LTS (headless) · `npx gltfpack@0.24` · Node v22.19.0 ·
python3 + Pillow · gzip -9.

## Metrics

| | input | shipped |
|---|---|---|
| Raw bytes | 1,038,208 | **449,024** (−56.8 %) |
| gzip -9 bytes | 179,109 | 303,405 (**+69 %** — see note) |
| Triangles | 19,122 | 18,774 (−1.8 %) |
| Vertices | 36,217 | **9,814** (−72.9 %) |
| Mesh objects | 190 | **13** |
| Draw primitives | 191 | **14** |
| Materials | 12 | 12 (identical set) |
| Bbox | 124.2265 × 95.3195 × 27.0 | identical |

**The gzip number went up, and that is expected.** meshopt (`-c`) produces
high-entropy buffers that gzip cannot compress further, so a meshopt file is
larger *after* gzip than an uncompressed GLB is. It is still the correct
shipping form: meshopt is the mandatory intake compression for everything under
`app/public/sf-assets/` (`sf-asset-check` §8, and the loaders register
`MeshoptDecoder`), and the decode cost is paid once at load while the 190 → 13
object collapse is paid every frame. Raw bytes — what the CDN stores and what
the 500 KB budget is written against — fell 57 %. Every other landmark in the
repo carries the same trade.

## Waste census (phase A)

| Finding | Count | Addressed by |
|---|---|---|
| Coincident vertex pairs | 26,324 | per-object weld ≤ 1 mm |
| Redundant duplicate triangles | 7,640 | weld + interior-face removal |
| Buried interior faces | 342 | closed-solid occluder test |
| Objects sharing a material | 190 → 12 groups | join-per-material |
| Degenerate faces | 0 | — |
| Image textures | 0 | — |

The object-count overhead was the whole story: 190 separate closed solids, most
of them piers, ribbons and roof props that share one of twelve flat materials.

## Phase B steps

| Step | Tris | Verts |
|---|---|---|
| input | 19,122 | 36,217 |
| weld + degenerate | 19,122 | 9,893 |
| interior faces (342 removed) | 18,780 | 9,817 |
| limited dissolve @ 0.05° | 18,774 | 9,814 |
| join per material | 18,774 | 9,814 (13 objects) |

Limited dissolve ran at **0.05°**, not 0.5° — the prompt's hard-learned rule.
The drum, court octagon and seal are curved shells, exactly the geometry a 0.5°
transitive chain twists into flipped-winding ngons.

Retessellation of curves was **skipped**. The drum arc at 14 segments and the
court octagon at 8 are silhouette-defining (§1 rule 5), and the seal at 14
segments is the identity feature. Halving any of them is visible.

## Phase C packing

```
npx gltfpack@0.24 -i mid.glb -o 505-van-ness.optimized.glb -c -km -kn -noq
```

`-km` and `-kn` keep material and node names — without `-km`, gltfpack merges
identical-parameter materials across the `_Glow` boundary and silently kills the
night layer, which for this asset would erase the seal ring. `-noq` (no
quantization) is mandatory in this repo: the runtime merge path needs float32
attributes, and quantization also stores a dequantize matrix as a node transform,
which fails the stage-2 contract validator on `transforms_applied`.

## Gates

| Gate | Result | Evidence |
|---|---|---|
| **G1** contract | **PASS** | material set identical (12); `Toy_glass_Glow` + `Toy_trim_Glow` still separate; no `Toy_body` |
| **G2** geometry | **PASS** | bbox identical to 4 dp; origin within 1 cm; all signed volumes positive; 0 flipped of 22,500 rays (0.0000 %) |
| **G3** round-trip | **PASS** | re-imports in Blender; `g3check` (pinned three) `{"ok":true,"meshes":14,"tris":18774}`, no decode errors |
| **G4** appearance | **PASS** | see table below; max mean delta 0.2389 % against 2 % far / 4 % near |
| **G5** draw submeshes | **PASS** | 191 → 14 |
| **G6** size | **PASS** | raw −56.8 % |
| **G7** GPU budget | n/a | bake mode off |
| **G8** hygiene | **PASS** | re-import object/material counts match; no `.blend1`; deterministic scripts committed here |

### G4 pixel deltas

| View | mean abs RGB | max px |
|---|---|---|
| day near | 0.0166 % | 37 |
| day far | 0.0190 % | 40 |
| night near | 0.2030 % | 129 |
| night far | 0.2389 % | 121 |
| elev N / E / S / W | 0.0081 / 0.0258 / 0.0180 / 0.0048 % | ≤ 34 |

**What the diffs actually show:** nothing a player would notice. At ×8
amplification the diff row is black except for hairline outlines on high-contrast
edges — pier arrises, the fascia lip and the seal rim — which is welding moving
shared vertices by sub-millimetre amounts and re-resolving which coincident face
wins. Night deltas run ~10× the day ones because the `_Glow` layer is fully
emissive there, so the same hairline edge shift carries much more luminance;
0.24 % of a fully-lit surface is still an order of magnitude inside the gate.
No element is missing, the silhouette is unchanged, and no shading artifact
appeared.

## Shipping swap

`505-van-ness.optimized.glb` was copied over `artifacts/505-van-ness/505-van-ness.glb`
and from there into `app/public/sf-assets/landmarks/505-van-ness.glb`. The
pre-optimize original is archived byte-identical at `optimize/input/505-van-ness.glb`
(1,038,208 bytes, verified with `cmp`). The asset's `validation.json` and
`REPORT.md` were re-run against the shipped file, so the manifest's `tris`
(18,774) and `dims` come from the geometry that actually ships.

## Reproduce

```bash
B=/Applications/Blender.app/Contents/MacOS/Blender
$B -b --python inspect.py  -- input/505-van-ness.glb inspect.json
$B -b --python optimize.py -- input/505-van-ness.glb mid.glb phaseb_stats.json
npx gltfpack@0.24 -i mid.glb -o 505-van-ness.optimized.glb -c -km -kn -noq
$B -b --python validate.py -- input/505-van-ness.glb 505-van-ness.optimized.glb validation.json
$B -b --python render_ab.py -- input/505-van-ness.glb renders/in
$B -b --python render_ab.py -- 505-van-ness.optimized.glb renders/out
python3 diff_ab.py
(cd g3check && npm install && node check.mjs ../505-van-ness.optimized.glb)
```
