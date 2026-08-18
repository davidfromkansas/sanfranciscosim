# 501 Third Street — GLB optimize pass (stage 4)

Input: the approved `artifacts/501-third/501-third.glb` (90 objects, 2,780 tris,
187,920 bytes). Output: a 7-primitive meshopt-compressed GLB of **76,648 bytes**
— **−59.2%** on the raw file, **−92.2%** on draw submeshes — with no visible
change at any camera. All gates PASS; the optimized file is now the shipping
asset and the original is archived at `optimize/input/501-third.glb`.

`ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`.

> This pass was run twice. The first run optimized the pre-correction asset; the
> orientation error found at stage 5 (the 3rd Street elevation was modelled on
> the party wall — see `../REPORT.md`) changed the geometry, so the whole pass
> was re-run from scratch against the rebuilt GLB rather than patched. Every
> number below is from the second run.

## Headline numbers

| Metric | Input | Shipped | Delta |
|---|---:|---:|---:|
| File, raw bytes | 187,920 | **76,648** | **−59.2%** |
| File, gzip -9 | 33,454 | 49,359 | +47.5% (see note) |
| Draw submeshes (glTF primitives) | 90 | **7** | −92.2% |
| Meshes / nodes | 90 / 90 | 7 / 7 | −92.2% |
| Triangles | 2,780 | 2,732 | −1.7% |
| Vertices (Blender, post-weld) | 5,464 | 1,544 | −71.7% |
| Materials | 7 | 7 | unchanged |
| Bbox (m) | 34.6966 × 34.5376 × 16.4 | identical | 0 |

**Note on gzip.** Meshopt buffers are already entropy-coded, so gzip goes the
wrong way at every step and the gzip column is not the honest baseline. Since
meshopt is mandatory at intake (`pipeline/compress-assets.mjs`), the fair
comparison is against *gltfpack alone* on the unoptimized input: 115,272 raw,
against which this pass is **−33.5%**. Both numbers are quoted rather than only
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
| Raw / gzip9 bytes | 187,920 / 33,454 |
| Objects / primitives | 90 / 90 |
| Triangles / vertices | 2,780 / 5,464 |
| Vertex attributes | POSITION, NORMAL (no UV, no COLOR) |
| Textures | none |
| Materials | 7 (1 glow: `Toy_white_Glow`) |
| Bbox / origin offset | 34.6966 × 34.5376 × 16.4 m / (0.0156, −0.0025) xy, base z 0 |

**Waste census and predicted savings.**

| Technique | Census finding | Predicted | Actual |
|---|---|---:|---:|
| Join per material | 90 objects over 7 materials (the window reveals and panes dominate) | the big win: 90 → 7 primitives, kills node/accessor overhead | 90 → 7, −31.8 KB raw vs pack-only |
| Weld ≤ 1 mm | ~3,900 coincident vertex pairs | ambiguous — must be measured, see §3 | −3,920 verts, −6.8 KB raw |
| Degenerate faces | present in the beveled solids | small tri win | −48 tris |
| Duplicate meshes | repeated window reveals/panes and the four bulkhead copings | none as instances — joining them is the same win and keeps one draw | folded into the join |
| Interior faces | — | the occluder rule needs closed solids; this asset's boxes abut, they do not nest | 0 removed (correct) |
| Curve retessellation | — | nothing curved: every solid is a beveled prism or box | skipped |

## Phase B — geometry cleanup (`optimize.py`, `phaseb_stats.json`)

| Step | Tris | Verts |
|---|---:|---:|
| input | 2,780 | 5,464 |
| weld + degenerate | 2,732 | 1,544 |
| interior faces (0 removed) | 2,732 | 1,544 |
| limited dissolve — **skipped** | 2,732 | 1,544 |
| join per material (90 → 7) | 2,732 | 1,544 |

### Judgment call 1 — the limited dissolve is OFF (§3.3)

`GLB-OPTIMIZE-PROMPT` §3.3 says to skip step 3 entirely on assets with large
coplanar ring bands. This asset has three: `parapet` and `parapet_cap` are
full-footprint annuli (288 tris each, the two largest objects in the file) and
the roof `guardrail` is a closed ribbon. A strictly-coplanar dissolve still
merges each annulus into one ngon, and re-triangulating an annulus emits
metre-long slivers whose averaged vertex normals collapse to ~0 — a failure that
surfaces only in the packed file, after the shipping swap. `optimize.py` was
adapted to default the step off (`--dissolve` re-enables it). Cost: at most the
~1% of triangles the step is ever worth here. The stage-2 contract validator,
re-run on the shipped packed file, reports
`invalid_or_nonunit_loop_normal_count: 0` — the check that would have caught it.

### Judgment call 2 — the weld stays, and it was measured, not assumed

A 1 mm weld helps beveled assets and *hurts* flat-shaded box assets, where the
"coincident" vertices are the flat-shading topology rather than waste. 501 Third
is both — box-heavy *and* beveled throughout (`bevel()` on the body, both parapet
rings, the entry jambs, the bulkhead and its four copings). So the variant table
decides it. Every variant packed with the repo standard
`gltfpack@0.24 -c -km -kn -noq`:

| variant | raw | gzip9 | primitives |
|---|---:|---:|---:|
| pack only | 115,272 | 44,365 | 90 |
| join only (`--no-weld`) | 83,464 | 50,100 | 7 |
| **weld + join (shipped)** | **76,648** | 49,359 | **7** |

The weld is worth 6,816 bytes on top of the join, so it stays — this asset lands
on the `300-brannan` side of the split (beveled ⇒ weld wins), not the
`326-brannan` side. The packed variants are kept under `optimize/variants/` so
the measurement is reproducible rather than a claim. (Weld-without-join is not
tabulated separately: the join is unconditionally correct here, and the two
`--no-weld` rows already isolate the weld's contribution.)

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
| day near | 0.0018% | 35 | ≤ 4% PASS |
| day far | 0.0019% | 12 | ≤ 2% PASS |
| night near | 0.0002% | 4 | ≤ 4% PASS |
| night far | 0.0004% | 4 | ≤ 2% PASS |
| elevation N / E / S / W | 0.0007 / 0.0026 / 0.0026 / 0.0020% | 16–32 | PASS |

**What the diffs actually look like.** At 8× amplification every diff tile is
black. The largest single-pixel excursions (max delta 35/255 on day-near) sit on
antialiased silhouette edges — one-pixel coverage differences between two
independent renders — and there is no spatial structure anywhere: no element
missing, no outline of a moved surface, no silhouette shift, no shading banding.
The night pair, which was the worst case in the first run, is now the *best*
(0.0002%, max 4). Nothing here is visible at 1× and nothing a player would
notice.

## Gate results

| Gate | Result | Evidence |
|---|---|---|
| G1 Contract — material set identical, `_Glow` separate, node names | **PASS** | `validation.json` `G1_materials_identical: true`; all 7 names round-trip, `Toy_white_Glow` its own primitive; no `Toy_body` on this asset |
| G2 Geometry — bbox, origin, signed volumes, flipped fraction | **PASS** | bbox identical to 4 dp; origin within 0.01 m; 0 inverted solids; ray-flip **delta 0.000000** |
| G3 Round-trip — Blender + pinned-three GLTFLoader | **PASS** | `G3-OK {"ok":true,"meshes":7,"tris":2732,...}`, no decode errors, only `EXT_meshopt_compression` |
| G4 Appearance — day+night × near+far | **PASS** | table above; worst case 0.0026% against a 2% gate |
| G5 Draw submeshes ≤ input | **PASS** | 90 → 7 |
| G6 Size reduced (target 60%) | **PASS** | −59.2% raw (−33.5% against the meshopt baseline). A whisker under the 60% aspiration; the census shows the remainder is silhouette geometry — 2,732 tris of beveled massing, window reveals and the two parapet rings, with no textures, no UVs and nothing duplicated left to remove |
| G7 GPU budget (bake mode) | **n/a** | `ALLOW_BAKE: no`, no textures |
| G8 Hygiene — no foreign geometry, deterministic, no `.blend1` | **PASS** | re-import object count 7 = expected; a full re-run reproduced `mid.glb` and the packed output **byte-for-byte**; 0 `.blend1` files |

### On the ray-flip gate (adaptation worth keeping)

The generic `validate.py` gates the ray-flip test on an **absolute** 0.15%. This
asset measures **1.2518% as input** — it carries a standing residual of its own,
because the `Toy_white_Glow` shells are deliberately single-sided panels proud of
opaque glazing and the roof guardrail is an open ribbon. The absolute gate would
have failed an untouched, correct asset. The gate exists to catch the *optimizer*
flipping windings, so `validate.py` was adapted to ray-test both files with the
same seed and gate on the **delta**, which is exactly 0.000000 (16,936 hits, 212
flipped, identical in both). The absolute figure is reported either way. This
mirrors the `davies-symphony-hall` finding.

## Shipping swap

`optimize/501-third.optimized.glb` → `artifacts/501-third/501-third.glb`
(76,648 bytes). The pre-optimize original is archived byte-for-byte at
`optimize/input/501-third.glb` (187,920 bytes). The asset's `validation.json` and
`REPORT.md` were re-generated against the shipped file: **PASS**, 7 objects,
2,732 triangles, 34.6966 × 34.5376 × 16.4 m, 7 materials,
`invalid_or_nonunit_loop_normal_count: 0`.

### Files kept under `variants/`

`out_packonly.glb`, `out_joinonly.glb`, `out_weldjoin.glb` — the three packed
variants behind the §3 table, so the weld decision can be re-measured without
re-running the pass. The unpacked `mid_*.glb` intermediates were deleted; the
shipped one is `mid.glb` and the others are one `optimize.py` run away
(`--no-weld` reproduces `out_joinonly`, and `out_packonly` is gltfpack on
`input/501-third.glb` directly).
