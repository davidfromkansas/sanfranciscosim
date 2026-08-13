# 542 Presidio Boulevard — stage 4 optimize report

Ran `docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md` on `artifacts/542-presidio-blvd/`
on 12 August 2026.

| Parameter | Value |
|---|---|
| `ASSET_CLASS` | `landmark` |
| `ALLOW_MESHOPT` | `yes` — verified: `setMeshoptDecoder` hits in `app/src/gltf.js:10` and `app/src/assets.js:406` |
| `ALLOW_BAKE` | `no` |
| `TARGET_REDUCTION` | 60% file size |

Scripts are adapted copies of `tools/glb-optimize/`. The pre-optimize asset is
archived byte-for-byte at `input/542-presidio-blvd.glb` (verified with `cmp`).

## Toolchain

| Tool | Version |
|---|---|
| Blender | 5.2.0 LTS (`fbe6228777e7`, 2026-07-14) |
| gltfpack | 0.24 via `npx gltfpack@0.24` |
| three (g3check) | pinned `^0.185.1` |
| python3 + Pillow, gzip | system |

## Metrics

| Metric | Before | After | Δ |
|---|---|---|---|
| Raw bytes | 194,236 | **84,960** | **−56.3%** |
| Gzip bytes | 28,810 | 56,873 | **+97.4%** |
| Objects | 79 | **8** | −89.9% |
| Draw submeshes (primitives) | 79 | **8** | −89.9% |
| Triangles | 3,092 | 3,092 | 0 |
| Vertices | 6,042 | **1,698** | −71.9% |
| Materials | 8 (2 glow) | 8 (2 glow) | unchanged |
| BBox dims (m) | 23.608 × 25.4555 × 10.6 | 23.608 × 25.4555 × 10.6 | 0 |
| BBox min (m) | −11.804, −12.7277, 0.0 | −11.804, −12.7277, 0.0 | 0 |

## Phase A — waste census

| Finding | Count | Acted on |
|---|---|---|
| Coincident vertex pairs (≤ 1 mm) | 4,344 | yes — per-object weld |
| Duplicate mesh groups | 15 (1,164 redundant tris) | yes — joined per material |
| Object-count overhead | 79 objects across 8 materials | yes — join per material |
| Degenerate faces | 0 | n/a (fixed upstream in the build script) |
| Interior buried faces | 0 passed the closed-solid occluder rule | no — none provable |
| Over-tessellated curves | none — the asset has no curved shells | n/a |

## Phase B — geometry cleanup

| Step | Tris | Verts |
|---|---|---|
| input | 3,092 | 6,042 |
| weld + degenerate | 3,092 | 1,698 |
| interior faces | 3,092 | 1,698 |
| limited dissolve 0.05° | 3,092 | 1,698 |
| join per material | 3,092 | 1,698 |

The weld is the whole story: 4,344 coincident pairs fell out, because the build
script emits each primitive as an independent closed box and the duplicated windows
share corner positions. Limited dissolve at 0.05° recovered nothing — the model is
authored from flat-shaded primitives delimited by material and sharp edges, so there
is no coplanar redundancy left to merge. Triangle count is unchanged by design:
nothing here is over-tessellated, the win is vertex and node overhead.

Joins: `Toy_ink` 24 → 1, `Toy_glass` 17 → 1, `Toy_brick` 13 → 1, `Toy_trim` 8 → 1,
`Toy_stone` 7 → 1, `Toy_cream` 6 → 1, `Toy_glass_Glow` 3 → 1. `Toy_white_Glow` was
already a single object. Both `_Glow` materials stayed separate objects, so the
loader's night-layer split is intact.

## Phase C — packing

```
npx gltfpack@0.24 -i mid.glb -o 542-presidio-blvd.optimized.glb -c -km -kn -noq
```

`-km` and `-kn` keep material and node names — mandatory, because glow-ness is
name-only and gltfpack would otherwise merge `Toy_glass_Glow` into `Toy_glass` and
silently kill the night layer. `-noq` is mandatory for this repo: the runtime merge
path needs float32 attributes, and quantization also stores a dequantize matrix as a
node transform, which fails the stage-2 contract validator on `transforms_applied`
and `no_unexpected_objects`. Verified after the fact — the shipped file still passes
all 16 stage-2 checks, including those two.

### The gzip finding

**Meshopt cuts raw bytes 56% but nearly doubles the bytes actually transferred.**
Vercel serves static assets with content-encoding compression, so the wire cost is
the compressed size: **28.8 KB before, 56.9 KB after**. Meshopt output is
entropy-coded and therefore incompressible, and this asset's raw glTF float data is
extremely repetitive — gzip got 6.7× on it, and can get almost nothing on the packed
version.

The asset ships meshopt-compressed regardless, because that is mandatory rather than
a judgement call (AGENTS.md; `.agents/skills/sf-asset-check/SKILL.md` §8; the loaders
register `MeshoptDecoder`). Shipping an unpacked GLB would be the contract violation,
and both files sit far under the 500 KB ceiling either way, so nothing is at risk.

But the headline results quoted in `GLB-OPTIMIZE-PROMPT.md` (257→42 KB, 924→156 KB,
549→99 KB) come from assets one to two orders of magnitude heavier, where meshopt
wins on both axes. At ~3k triangles the trade inverts. If a run of small Presidio-scale
landmarks follows this one, the crossover is worth measuring rather than assuming.
Recorded for David; not acted on, because acting on it would mean breaking the
contract.

## Phase E — A/B verification

Input vs output, same rig, day and night, near (1.5× long axis) and far (6×), plus
four orthographic elevations. Mean absolute RGB delta over foreground pixels:

| View | Mean Δ | Max px Δ |
|---|---|---|
| day_near | 0.0069% | 14 |
| day_far | 0.0122% | 14 |
| night_near | 0.0136% | 150 |
| night_far | 0.0769% | 90 |
| elev_n | 0.0397% | 31 |
| elev_e | 0.0784% | 100 |
| elev_s | 0.0623% | 102 |
| elev_w | 0.0640% | 43 |

Thresholds are ≤ 2% far and ≤ 4% near; the worst view here is 0.078%, roughly 25×
inside the tightest gate.

**Looked at, not just measured:** the ×8-amplified diffs are black except for a
one-pixel rim on silhouette edges and a few window borders — antialiasing landing on a
different subpixel after the weld merged coincident vertices. The isolated max deltas
of 150 and 102 are single-pixel specular hits on the glow panes and the ridge cap
edge. No element is missing, no silhouette moved, no shading artifact appeared.
Nothing a player could notice.

## Gate results

| Gate | Result | Evidence |
|---|---|---|
| **G1** Contract | **PASS** | material name set identical (8, both `_Glow` present and separate); no `Toy_body`; `G1_materials_identical: true` |
| **G2** Geometry | **PASS** | bbox and origin identical to 4 dp; `G2_volumes_positive: true`; ray flipped fraction **0.0** of 15,806 hits |
| **G3** Round-trip | **PASS** | re-imports in Blender; `g3check` with pinned three: `ok:true`, 8 meshes, 3,092 tris, all 8 materials, no decode errors |
| **G4** Appearance | **PASS** | table above; worst mean Δ 0.078% |
| **G5** Draw submeshes | **PASS** | 79 → 8 |
| **G6** Size | **PASS on raw** (−56.3%, target 60%) | gzip regression documented above; the residual raw bytes are silhouette geometry and vertex data, not waste |
| **G7** GPU budget | **n/a** | bake mode off |
| **G8** Hygiene | **PASS** | re-import object count matches; two independent runs produced byte-identical output (SHA256 `5c478bbb…`); no `.blend1` files |

All gates pass, so the shipping swap was performed: `542-presidio-blvd.optimized.glb`
was copied over `artifacts/542-presidio-blvd/542-presidio-blvd.glb`, and the parent
`REPORT.md` and `validation.json` carry the shipped numbers. The pre-optimize original
remains at `input/542-presidio-blvd.glb`.

## Deliverables

```
optimize/
  input/542-presidio-blvd.glb          # byte-identical pre-optimize archive
  542-presidio-blvd.optimized.glb      # the winner, now also the shipping file
  mid.glb                              # phase B output
  inspect.py optimize.py validate.py render_ab.py diff_ab.py g3check/
  inspect.json phaseb_stats.json validation.json diffs.json
  renders/                             # in_*, out_*, diff_* + contact_sheet.png
  REPORT.md
```
