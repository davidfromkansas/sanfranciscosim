# Ferry Station Post Office Building — optimize pass (stage 4)

`docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md` run against
`artifacts/ferry-station-post-office/`, 18 August 2026.
`ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`.

**Result: 716,492 → 309,136 bytes raw (−56.9%), 287 → 15 draw primitives, all
gates PASS.** The optimized file is now the shipping asset; the pre-optimize
original is archived byte-for-byte at `optimize/input/`.

## Toolchain

| Tool | Version |
|---|---|
| Blender | 5.2.0 LTS (fbe6228777e7) |
| gltfpack | `npx gltfpack@0.24`, flags `-c -km -kn -noq` |
| node | v22.19.0 |
| three (g3check) | ^0.185.1 |
| python3 + Pillow, gzip -9 | system |

## Phase A — forensic inspection (`inspect.json`)

| | Input |
|---|---|
| Raw bytes | 716,492 |
| gzip −9 | 116,026 |
| Objects | 285 |
| Triangles | 11,596 |
| Vertices | 22,756 |
| Draw primitives | 287 |
| Vertex attributes | POSITION + NORMAL only (no UVs, no colors) |
| Textures | 0 |
| bbox | 69.839 × 65.202 × 12.650 m, min Z 0.0, XY offset (−0.158, −0.253) |
| Materials | 11, two of them `_Glow` |

Cross-checks against the asset's own `validation.json`: triangle count,
dimensions, min Z and material set all agree exactly.

### Waste census and the plan it produced

| Technique | Census reading | Predicted | Actual |
|---|---|---|---|
| Duplicate meshes | 3,724 tris across repeated groups (3 roof monitors, 2 end pavilions, 6 window bays, 6 rustication blocks) | 0 tris — these are *repeated architecture*, not waste; the join is what collects them | 0 tris |
| Buried interior faces | occluder scan over closed solids | small | **0 faces** — the massing volumes intersect but almost never fully contain one another |
| Degenerate faces | 0 | 0 | 0 |
| Coincident vertex pairs | 16,402 | weld should win on this asset: every solid carries a 2-segment Bevel, so most coincident verts are bevel redundancy, not flat-shading splits | **−16,402 verts (22,756 → 6,354)** |
| Object-count overhead | 285 objects over 11 materials | 287 → 15 primitives | **287 → 15** |
| Over-tessellation | none — no cylinders or curved shells in this asset | 0 | 0 |

**No triangles were removed at any step and none should have been.** This asset
has no waste geometry: 0 degenerate, 0 buried, 0 duplicate meshes shipped
separately. Every one of its 11,596 triangles is silhouette or facade relief.
The whole win is vertex-count and draw-primitive count, which is what Phase B
step 1 and step 5 are for.

## Phase B — geometry cleanup (`phaseb_weldjoin.json`, `phaseb_join.json`)

| Step | Triangles | Vertices |
|---|---|---|
| input | 11,596 | 22,756 |
| 1. weld ≤ 1 mm + degenerate, per object | 11,596 | 6,354 |
| 2. buried interior faces (closed-solid occluders only) | 11,596 | 6,354 |
| 3. limited dissolve | **SKIPPED — see below** | |
| 4. curve retessellation | not applicable — no curved geometry | |
| 5. join per material | 11,596 | 6,354 (285 → 11 objects) |
| 7. normals audit | 0 inverted signed volumes | |

**Step 3 is off, deliberately.** This asset carries seven large coplanar ring
bands that follow the footprint the whole way round — the granite plinth, the
work-room parapet and its terracotta coping, the copper cornice, the mid-block
parapet and its coping, and the SE wing's cornice. Per the prompt's §3.3
warning (measured on `350-brannan`), a strictly-coplanar dissolve merges each of
those into a single annulus ngon whose re-triangulation emits sub-millimetre
slivers; they pass every area-based degeneracy test and only surface as
`invalid_or_nonunit_loop_normal_count` in the *packed* file. The step was worth
0.4% on that asset. `optimize.py` here takes `--dissolve` to re-enable it; it
was not used and the option exists only so the decision is legible.

**Step 1 is measured, not assumed** — the prompt's own §11 and the
`326-brannan` result say the 1 mm weld can make a flat-shaded box asset *worse*.
Three variants, each packed with the repo standard `gltfpack@0.24 -c -km -kn -noq`:

| variant | raw | gzip −9 | verts | primitives |
|---|---|---|---|---|
| pack only | 436,020 | 171,194 | 22,756 | 287 |
| join only (`--no-weld`) | 340,548 | 203,620 | 22,756 | 15 |
| **weld + join (shipped)** | **309,136** | 198,913 | **6,354** | **15** |

The weld wins here by 31,412 bytes, which is the `300-brannan` outcome rather
than the `326-brannan` one, and for the same reason: every chunky solid in this
model runs a 2-segment Bevel modifier, so its coincident vertices are genuine
bevel redundancy rather than the flat-shading splits the exporter would just
re-create.

## Phase C — packing

`npx gltfpack@0.24 -i mid_weldjoin.glb -o ferry-station-post-office.optimized.glb -c -km -kn -noq`

`-km` and `-kn` keep the material and node names — mandatory, because `_Glow`
is name-only and merging `Toy_gold_Glow` into `Toy_gold` would silently delete
the night layer. `-noq` (no quantization) is the repo standard, matching
`pipeline/compress-assets.mjs`; the output material set was verified equal to
the input's rather than trusted from the flags.

**Byte accounting, both numbers, honestly.** Meshopt buffers are already
entropy-coded, so gzip goes the wrong way: 116,026 → 198,913. Meshopt is
mandatory at intake, so the fair baseline for judging *this pass* is gltfpack
alone at 436,020 raw, against which the pass is **−29.1%**; against the
unpacked authored file it is **−56.9%**. On disk and over the wire the shipped
file is 309,136 bytes raw / ~198.9 KB gzipped, comfortably inside AGENTS.md's
500 KB budget.

## Phase D — bake

Not run (`ALLOW_BAKE: no`). The asset has no textures and must not acquire any.

## Phase E — A/B verification (`diffs.json`, `renders/`)

Same rig, azimuth 250° (off the Embarcadero frontage normal), 42° elevation,
near = 1.5× long axis, far = 6×, day (glow alpha 0.12) and night (alpha 1.0,
emission 6), plus four orthographic elevations.

| View | mean abs RGB delta | max px delta |
|---|---|---|
| day near | 0.041% | 34 |
| day far | 0.041% | 24 |
| night near | 0.023% | 30 |
| night far | 0.025% | 18 |
| elev N | 0.045% | 24 |
| elev E | 0.278% | 55 |
| elev S | 0.030% | 33 |
| elev W | 0.141% | 36 |

**What the diffs actually show, having looked at them:** the amplified (×8)
diffs are black except for hairline traces along edges and one small cluster at
the central entrance. The edge traces are anti-aliasing on silhouette and
material boundaries, which move by a sub-pixel amount because the join changes
primitive draw order. The entrance cluster is the `Toy_gold_Glow` transom and
door plates sitting coplanar-adjacent to the opaque glazing behind them — same
sub-pixel ordering effect, concentrated because those are the highest-contrast
small elements in the frame. Nothing is missing, no silhouette moved, no
shading artefact appeared, and nothing here is visible at 1:1 let alone at the
app's camera distances.

## Gates

| Gate | Result | Evidence |
|---|---|---|
| **G1 Contract** | PASS | material set identical (11, including both `_Glow`); no `Toy_body` in this asset; no manifest-named nodes to preserve |
| **G2 Geometry** | PASS | bbox identical to 5 dp (69.83858 × 65.20236 × 12.65); origin identical; 0 inverted signed volumes; ray-flip fraction 0.0% output against 0.0% input (gate applied as a **delta**, per the single-sided-surface caveat) |
| **G3 Round-trip** | PASS | re-imports in Blender; `g3check` (pinned three ^0.185.1) reports `ok: true`, 15 meshes, 11,596 tris, all 11 materials, bbox 69.8386 × 12.65 × 65.2024 |
| **G4 Appearance** | PASS | max mean delta 0.278% against gates of 2% far / 4% near; described above |
| **G5 Draw submeshes** | PASS | 287 → 15 |
| **G6 Size** | PASS with note | −56.9% raw against the 60% aspiration. The census above shows why the remainder cannot shrink: zero triangles are waste, so there is nothing left to remove that is not silhouette or facade relief |
| **G7 GPU budget** | n/a | bake mode not used |
| **G8 Hygiene** | PASS | re-import object/material counts match; deterministic re-run reproduced the packed file **byte-identically** (sha256 `e03267df…`); no `.blend1` files |

## Shipping swap

`ferry-station-post-office.optimized.glb` copied over
`artifacts/ferry-station-post-office/ferry-station-post-office.glb`. The
pre-optimize original is archived at
`optimize/input/ferry-station-post-office.glb` (716,492 bytes, sha256 recorded
by the byte-compare at copy time). The asset-level `validation.json` and
`REPORT.md` were re-run / updated to the shipped numbers so the integration
stage writes its manifest entry from reality.
