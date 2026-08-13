# 500 Van Ness Avenue — GLB optimize report (stage 4)

Run of `docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md` against
`artifacts/500-van-ness/`. `ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`,
`ALLOW_BAKE: no`. Scripts adapted from `tools/glb-optimize/`.

Toolchain: Blender 5.2.0 LTS (headless, Cycles) · `npx gltfpack@0.24` ·
Node v22.19.0 · python3 + Pillow · gzip -9.

## Metrics

| | input | shipped |
|---|---|---|
| Raw bytes | 574,548 | **247,576** (−56.9 %) |
| gzip -9 bytes | 99,887 | 166,459 (**+66.6 %** — see note) |
| Triangles | 9,522 | 9,512 (−0.1 %) |
| Vertices | 18,534 | **5,108** (−72.4 %) |
| Mesh objects | 190 | **12** |
| Draw primitives | 192 | **13** |
| Materials | 11 | 11 (identical set) |
| Bbox | 43.28593 × 45.09732 × 17.0 | identical to 5 dp |
| Origin (xy centre) | (−0.00071, −0.00022) | identical |

**The gzip number went up, and that is expected.** meshopt (`-c`) produces
high-entropy buffers that gzip cannot compress further, so a meshopt file is
larger *after* gzip than an uncompressed GLB is. It is still the correct
shipping form: meshopt is the mandatory intake compression for everything under
`app/public/sf-assets/` (`sf-asset-check` §8, and the loaders register
`MeshoptDecoder`), and the decode cost is paid once at load while the 190 → 12
object collapse is paid every frame. Raw bytes — what the CDN stores and what
the 500 KB budget is written against — fell 57 %, to 248 KB. Every other
landmark in the repo carries the same trade.

## Waste census (phase A)

| Finding | Count | Addressed by |
|---|---|---|
| Coincident vertex pairs | 13,423 | per-object weld ≤ 1 mm |
| Redundant duplicate triangles | 3,488 | weld |
| Buried interior faces | 4 | closed-solid occluder test |
| Objects sharing a material | 190 → 12 groups | join-per-material |
| Degenerate faces | 0 | — |
| Image textures | 0 | — |

The object-count overhead was the whole story here, and the triangle count
barely moved because there is almost nothing to remove: 8 bay solids, the
cornice/parapet/plinth ring bands and ~140 window, glow and shopfront panels
that are each a 12-triangle box and every one of them visible. This is what
Gate G6's "the remainder is silhouette geometry" clause is for.

## Phase B steps

| Step | Tris | Verts |
|---|---|---|
| input | 9,522 | 18,534 |
| weld + degenerate | 9,522 | 5,111 |
| interior faces (4 removed) | 9,518 | 5,111 |
| limited dissolve @ 0.05° | 9,512 | 5,108 |
| join per material | 9,512 | 5,108 (12 objects) |

Limited dissolve ran at **0.05°**, not 0.5° — the prompt's hard-learned rule.

Retessellation of curves was **skipped**. The four rounded bays are 10-segment
segmental bows; they are the asset's identity feature (silhouette rule §1.5) and
are already at the low end of the style bible's 8–14 band. Halving them is
visible.

## Phase C packing

```
npx gltfpack@0.24 -i mid.glb -o 500-van-ness.optimized.glb -c -km -kn -noq
```

`-km` and `-kn` keep material and node names — without `-km`, gltfpack merges
identical-parameter materials across the `_Glow` boundary and silently kills the
night layer, which for this asset would erase the sign fascia and every lit
window. `-noq` (no quantization) is mandatory in this repo: the runtime merge
path needs float32 attributes, and quantization also stores a dequantize matrix
as a node transform, which fails the stage-2 contract validator on
`transforms_applied`.

## Gates

| Gate | Result | Evidence |
|---|---|---|
| **G1** contract | **PASS** | material set identical (11); `Toy_gold_Glow` + `Toy_sky_Glow` still separate; no `Toy_body` |
| **G2** geometry | **PASS** | bbox identical to 5 dp; origin within 0.01 mm; all 12 signed volumes positive; 0 flipped of 20,322 ray hits (0.0000 %) |
| **G3** round-trip | **PASS** | re-imports in Blender; `g3check` (pinned three) `{"ok":true,"meshes":13,"tris":9512}`, material set and bbox intact, no decode errors |
| **G4** appearance | **PASS** | see table below; max mean delta 0.1223 % against 2 % far / 4 % near |
| **G5** draw submeshes | **PASS** | 192 → 13 |
| **G6** size | **PASS** | raw −56.9 %; short of the 60 % aspiration, and the census above shows the remainder is silhouette and facade-panel geometry |
| **G7** GPU budget | n/a | bake mode off |
| **G8** hygiene | **PASS** | re-import object/material counts match; no `.blend1`; deterministic scripts committed here |

### G4 pixel deltas

| View | mean abs RGB | max px |
|---|---|---|
| day near | 0.0258 % | 31 |
| day far | 0.0578 % | 23 |
| night near | 0.0530 % | 119 |
| night far | 0.1010 % | 43 |
| elev N / E / S / W | 0.0919 / 0.0938 / 0.1223 / 0.0890 % | ≤ 42 |

**What the diffs actually show:** nothing a player would notice. At ×8
amplification every diff tile is black except for a hairline along the
ground-contact silhouette, faint outlines on a few window panels, and — in the
night pair — a warm speckle at the entrance-court soffit and a cyan hairline
along the sign fascia. Those are path-tracing noise on fully-emissive edges
(the A/B rig deliberately runs with denoising **off**), plus welding moving
shared vertices by sub-millimetre amounts and re-resolving which coincident face
wins. The single 119-value max pixel is one such emissive-edge sample. No
element is missing, the silhouette is unchanged, and no shading artifact
appeared.

## Per-asset script adaptations

`render_ab.py` here opts into Metal/CUDA compute (`_enable_gpu()`), because this
machine was running six other Blender sessions and the A/B pass was taking 13
minutes per frame on a contended CPU. Same integrator, same 64 samples,
denoising still off — the pixel deltas the gate measures are unaffected, and the
run drops to about a minute per frame. `diff_ab.py` carries the asset's caption.
Everything else is `tools/glb-optimize/` unchanged.

## Shipping swap

`500-van-ness.optimized.glb` was copied over
`artifacts/500-van-ness/500-van-ness.glb`. The pre-optimize original is archived
byte-identical at `optimize/input/500-van-ness.glb` (574,548 bytes, verified with
`cmp`). The asset's `validation.json` was re-run against the shipped file and is
**all-PASS at 9,512 triangles / 12 objects**, so the manifest's `tris` and `dims`
come from the geometry that actually ships.

## Reproduce

```bash
B=/Applications/Blender.app/Contents/MacOS/Blender
$B -b --python inspect.py  -- input/500-van-ness.glb inspect.json
$B -b --python optimize.py -- input/500-van-ness.glb mid.glb phaseb_stats.json
npx gltfpack@0.24 -i mid.glb -o 500-van-ness.optimized.glb -c -km -kn -noq
$B -b --python validate.py -- input/500-van-ness.glb 500-van-ness.optimized.glb validation.json
$B -b --python render_ab.py -- input/500-van-ness.glb renders/in
$B -b --python render_ab.py -- 500-van-ness.optimized.glb renders/out
python3 diff_ab.py
(cd g3check && npm install && node check.mjs ../500-van-ness.optimized.glb)
```
