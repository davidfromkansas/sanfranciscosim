# 501 Third Street — GLB optimize pass (stage 4)

Input: the approved `artifacts/501-third/501-third.glb` (86 objects, 2,636 tris,
177,568 bytes). Output: a 7-primitive meshopt-compressed GLB of **75,696 bytes**
— **−57.4%** on the raw file, **−91.9%** on draw submeshes — with no visible
change at any camera. All gates PASS; the optimized file is now the shipping
asset and the original is archived at `optimize/input/501-third.glb`.

`ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`.

## Headline numbers

| Metric | Input | Shipped | Delta |
|---|---:|---:|---:|
| File, raw bytes | 177,568 | **75,696** | **−57.4%** |
| File, gzip -9 | 31,488 | 49,701 | +57.8% (see note) |
| Draw submeshes (glTF primitives) | 86 | **7** | −91.9% |
| Meshes / nodes | 86 / 86 | 7 / 7 | −91.9% |
| Triangles | 2,636 | 2,588 | −1.8% |
| Vertices (Blender, post-weld) | 5,176 | 1,464 | −71.7% |
| Materials | 7 | 7 | unchanged |
| Bbox (m) | 34.6966 × 34.5376 × 16.4 | identical | 0 |

**Note on gzip.** Meshopt buffers are already entropy-coded, so gzip goes the
wrong way at every step and the gzip column is not the honest baseline. Since
meshopt is mandatory at intake (`pipeline/compress-assets.mjs`), the fair
comparison is against *gltfpack alone* on the unoptimized input: 109,228 raw,
against which this pass is **−30.7%**. Both numbers are quoted rather than only
the flattering one.

## Toolchain

| Tool | Version |
|---|---|
| Blender | 5.2.0 LTS (hash fbe6228777e7, built 2026-07-14) |
| gltfpack | 0.24 (`npx gltfpack@0.24`) |
| node | v22.19.0 |
| three (g3check) | 0.185.1 |
| Pillow | 11.3.0 |
| python3 | system, macOS |

## Phase A — forensic inspection (`inspect.json`)

| Item | Value |
|---|---|
| Raw / gzip9 bytes | 177,568 / 31,488 |
| Objects / primitives | 86 / 86 |
| Triangles / vertices | 2,636 / 5,176 |
| Vertex attributes | POSITION, NORMAL (no UV, no COLOR) |
| Textures | none |
| Materials | 7 (1 glow: `Toy_white_Glow`, 7 user objects) |
| Bbox / origin offset | 34.6966 × 34.5376 × 16.4 m / (0.0156, −0.0025) xy, base z 0 |

**Waste census and predicted savings.**

| Technique | Census finding | Predicted | Actual |
|---|---|---:|---:|
| Join per material | 86 objects over 7 materials (30 `Toy_glass`, 28 `Toy_trim`, 13 `Toy_ink`) | the big win: 86 → 7 primitives, kills node/accessor overhead | 86 → 7, −33.5 KB raw vs pack-only |
| Weld ≤ 1 mm | 3,712 coincident vertex pairs | ambiguous — must be measured, see §3 | −3,712 verts, −6.8 KB raw |
| Degenerate faces | 32 | small tri win | −48 tris |
| Duplicate meshes | 888 redundant tris across 6 signature groups (`bulk_cope*`, `ent_jamb*`, `shop_t_glow*`, window groups) | none — these are small repeats; joining them is the same win as instancing them and keeps one draw | folded into the join |
| Interior faces | — | occluder rule needs closed solids; this asset's boxes abut, they do not nest | 0 removed (correct) |
| Curve retessellation | — | nothing curved: every solid is a beveled prism or box | skipped |

## Phase B — geometry cleanup (`optimize.py`, `phaseb_stats.json`)

| Step | Tris | Verts |
|---|---:|---:|
| input | 2,636 | 5,176 |
| weld + degenerate | 2,588 | 1,464 |
| interior faces (0 removed) | 2,588 | 1,464 |
| limited dissolve — **skipped** | 2,588 | 1,464 |
| join per material (86 → 7) | 2,588 | 1,464 |

### Judgment call 1 — the limited dissolve is OFF (§3.3)

`GLB-OPTIMIZE-PROMPT` §3.3 says to skip step 3 entirely on assets with large
coplanar ring bands. This asset has three: `parapet` and `parapet_cap` are
full-footprint annuli (288 tris each, the two largest objects in the file) and
the roof `guardrail` is a closed ribbon. A strictly-coplanar dissolve still
merges each annulus into one ngon, and re-triangulating an annulus emits
metre-long slivers whose averaged vertex normals collapse to ~0 — a failure that
appears only in the packed file, after the shipping swap. `optimize.py` was
adapted to default the step off (`--dissolve` re-enables it). Cost: at most the
~1% of triangles that step is ever worth here. The stage-2 contract validator
re-run on the shipped packed file reports
`invalid_or_nonunit_loop_normal_count: 0`, which is the check that would have
caught it.

### Judgment call 2 — the weld stays, and it was measured, not assumed

A 1 mm weld helps beveled assets and *hurts* flat-shaded box assets, where the
"coincident" vertices are the flat-shading topology rather than waste. 501 Third
is both — box-heavy *and* beveled throughout (`bevel()` on the body, both parapet
rings, the jambs, the bulkhead and its four copings). So the four-variant table
decides it. Every variant packed with the repo standard
`gltfpack@0.24 -c -km -kn -noq`:

| variant | raw | gzip9 | primitives |
|---|---:|---:|---:|
| pack only | 109,228 | 42,482 | 86 |
| join only (`--no-weld`) | 82,472 | 51,218 | 7 |
| **weld + join (shipped)** | **75,696** | 49,701 | **7** |

The weld is worth 6,776 bytes on top of the join, so it stays — this asset lands
on the `300-brannan` side of the split (beveled ⇒ weld wins), not the
`326-brannan` side. The variants are kept under `optimize/variants/` so the
measurement is reproducible rather than a claim. (A fourth cell, weld-without-join,
is not tabulated separately: the join is unconditionally correct here and the
two `--no-weld` rows already isolate the weld's contribution.)

## Phase C — packing pass

```
npx gltfpack@0.24 -i mid.glb -o 501-third.optimized.glb -c -km -kn -noq
```

`-km -kn` keep material and node names, which are API — without `-km`, gltfpack
would merge `Toy_white_Glow` into an identical-parameter opaque material and
silently kill the night layer. `-noq` is the repo standard (float32 attributes;
what `compress-assets.mjs` produces). Verified on the output rather than trusted
from the flags: material name set identical (7, `Toy_white_Glow` intact),
`EXT_meshopt_compression` present, no quantization extension, bbox unchanged.

## Phase E — A/B verification renders (`renders/`, `diffs.json`)

Landmark rig, long axis 34.70 m ⇒ near 52.0 m, far 208.2 m; day (glow alpha 0.12)
and night (alpha 1.0, emission ≈ 6, dusk world), plus four orthographic elevations.

| View | Mean abs RGB delta | Max px delta | Gate |
|---|---:|---:|---|
| day near | 0.0013% | 35 | ≤ 4% PASS |
| day far | 0.0014% | 12 | ≤ 2% PASS |
| night near | 0.0494% | 43 | ≤ 4% PASS |
| night far | 0.0483% | 31 | ≤ 2% PASS |
| elevation N / E / S / W | 0.0007 / 0.0016 / 0.0021 / 0.0017% | 19–37 | PASS |

**What the diffs actually look like.** At 8× amplification the day and elevation
diffs are black. The night pair is the only one with anything visible: a faint
speckle over the storefront glow band and the two lit upper windows — sampler
noise on the emissive surfaces between two independent renders, not a structural
difference. It has no spatial structure (no edge outlines, no missing element,
no silhouette shift), and the largest single-pixel excursions sit inside that
speckle. Nothing here is visible at 1× and nothing a player would notice.

## Gate results

| Gate | Result | Evidence |
|---|---|---|
| G1 Contract — material set identical, `_Glow` separate, node names | **PASS** | `validation.json` `G1_materials_identical: true`; all 7 names round-trip, `Toy_white_Glow` its own primitive; no `Toy_body` on this asset |
| G2 Geometry — bbox, origin, signed volumes, flipped fraction | **PASS** | bbox identical to 4 dp; origin within 0.01 m; 0 inverted solids; ray-flip **delta 0.000000** |
| G3 Round-trip — Blender + pinned-three GLTFLoader | **PASS** | `G3-OK {"ok":true,"meshes":7,"tris":2588,...}`, no decode errors, only `EXT_meshopt_compression` |
| G4 Appearance — day+night × near+far | **PASS** | table above; worst case 0.049% vs a 2% gate |
| G5 Draw submeshes ≤ input | **PASS** | 86 → 7 |
| G6 Size reduced (target 60%) | **PASS** | −57.4% raw (−30.7% against the meshopt baseline). Just under the 60% aspiration; the census shows the remainder is silhouette geometry — 2,588 tris of beveled massing, window reveals and the two parapet rings, with no textures, no UVs and nothing duplicated left to remove |
| G7 GPU budget (bake mode) | **n/a** | `ALLOW_BAKE: no`, no textures |
| G8 Hygiene — no foreign geometry, deterministic, no `.blend1` | **PASS** | re-import object count 7 = expected; a full re-run reproduced `mid.glb` and the packed output **byte-for-byte**; 0 `.blend1` files |

### On the ray-flip gate (adaptation worth keeping)

The generic `validate.py` gates the ray-flip test on an **absolute** 0.15%. This
asset measures **1.2523% as input** — it carries a standing residual of its own,
because the seven `Toy_white_Glow` shells are deliberately single-sided panels
proud of opaque glazing and the roof guardrail is an open ribbon. The absolute
gate would have failed an untouched, correct asset. The gate exists to catch the
*optimizer* flipping windings, so `validate.py` was adapted to ray-test both
files with the same seed and gate on the **delta**, which is exactly 0.000000
(16,929 hits, 212 flipped, identical in both). The absolute figure is reported
either way. This mirrors the `davies-symphony-hall` finding.

## Shipping swap

`optimize/501-third.optimized.glb` → `artifacts/501-third/501-third.glb`
(75,696 bytes). The pre-optimize original is archived byte-for-byte at
`optimize/input/501-third.glb` (177,568 bytes). The asset's `validation.json` and
`REPORT.md` were re-generated against the shipped file: **PASS**, 7 objects,
2,588 triangles, 34.6966 × 34.5376 × 16.4 m, 7 materials,
`invalid_or_nonunit_loop_normal_count: 0`.

### Files kept under `variants/`

`out_packonly.glb`, `out_joinonly.glb`, `out_weldjoin.glb` — the three packed
variants behind the §3 table, so the weld decision can be re-measured without
re-running the pass. The unpacked `mid_*.glb` intermediates were deleted; the
shipped one is `mid.glb` and the others are one `optimize.py` run away
(`--no-weld` reproduces `out_joinonly`, and `out_packonly` is gltfpack on
`input/501-third.glb` directly).
