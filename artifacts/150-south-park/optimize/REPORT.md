# 150 South Park — optimize pass (stage 4)

`docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md` run against `artifacts/150-south-park/`.
Defaults: `ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`.
16 August 2026.

**Toolchain:** Blender 5.2.0 LTS (fbe6228777e7, 2026-07-14), `npx gltfpack@0.24`,
node v22.19.0 with the pinned three in `g3check/`, python3 + Pillow, gzip −9.

---

## 1. Headline

| Metric | Input | Shipped | Δ |
|---|---|---|---|
| File, raw | 186,872 B | **91,256 B** | **−51.2%** |
| File, gzip −9 | 36,362 B | 64,878 B | +78.4% (expected — see §4) |
| Triangles | 3,084 | 3,084 | 0 |
| Vertices (Blender, welded) | 6,190 | 1,646 | −73.4% |
| Vertices (glTF accessors) | 6,190 | 5,645 | −8.8% |
| Objects | 54 | 10 | −81.5% |
| Draw submeshes (primitives) | 55 | **11** | −80.0% |
| Materials | 9 | 9 | identical set |
| Bbox dims | 19.85214 × 17.58550 × 8.00000 | identical to 5 dp | 0 |
| Origin offset XY | (0.29233, 0.51817) | identical | 0 |

The shipping file at `artifacts/150-south-park/150-south-park.glb` is now the optimized
build; the pre-optimize original is archived byte-for-byte at
`optimize/input/150-south-park.glb`.

## 2. Phase A — waste census

`inspect.json`. 54 objects, 3,084 triangles, 6,190 vertices, 55 primitives, one vertex
attribute beyond position (`NORMAL`), no textures, no degenerate triangles.

| Technique | Finding | Predicted | Actual |
|---|---|---|---|
| Weld coincident verts | **4,544 coincident pairs** — glTF splits every vertex per face normal on a flat-shaded asset | large vertex win, zero triangle win | 6,190 → 1,646 verts |
| Join per material | 9 material groups across 54 objects | 55 → ~11 primitives | 55 → 11 |
| Duplicate mesh groups | 720 redundant triangles across 8 groups (3 skylights, 3 kerbs, 2 lamp arms, 2 shades, 2 window frames, 2 sills, 2 lights, 2 glow shells) | absorbed by the per-material join | absorbed |
| Interior faces buried in a closed solid | none provable | 0 | 0 |
| Degenerate faces | 0 | 0 | 0 |
| Over-tessellated curves | none — there is not a single curved surface on this building | 0 | 0 |

**There is no triangle waste in this asset and none was expected.** It was authored as
closed boxes and wall panels at 3,084 triangles against a 6,000 cap; the entire win here is
vertex-count and draw-submesh overhead, which is exactly what the census predicted.

## 3. Phase B — geometry cleanup

| Step | Tris | Verts |
|---|---|---|
| input | 3,084 | 6,190 |
| weld ≤ 1 mm + degenerate (per object) | 3,084 | 1,646 |
| interior faces | 3,084 | 1,646 |
| limited dissolve | **SKIPPED** | — |
| join per material | 3,084 | 1,646 |

Joins: `Toy_ink` 17 objects, `Toy_steel` 8, `Toy_roofd` 6, `Toy_oxblood` 6, `Toy_glass` 5,
`Toy_white` 4, `Toy_glassl` 3, `Toy_gold_Glow` 2, `Toy_glass_Glow` 2. `shell` is
multi-material (`Toy_ink` walls + `Toy_roofd` roof cap) and keeps its own mesh, which is why
10 objects produce 11 primitives.

**The limited dissolve was skipped outright, and that is the one judgment call in this
pass.** GLB-OPTIMIZE-PROMPT §3.3 says to skip it on assets with large coplanar ring bands.
This building has **two of them stacked**: `parapet` (360 tris) and `coping` (360 tris) both
follow the whole ~55 m footprint perimeter, and their top and bottom faces are perfectly
coplanar annuli. Even a strictly-coplanar dissolve merges each into one annulus ngon, and
re-triangulating an annulus emits the sub-millimetre slivers that `350-brannan` documented
on 13 Aug 2026 — invisible, clean against an area-based degeneracy test, and fatal at the
stage-2 contract validator, because a sliver's shared vertex sits between opposing normals
so its averaged normal collapses to ~0 and gltfpack re-emits the stored value. On
155 South Park the same step removed exactly zero triangles. It is the cheapest step in
Phase B and the only one that can manufacture degenerate geometry, so on a two-ring asset it
is not worth running. The skip is recorded in `optimize.py` at the point of the skip and in
`phaseb_stats.json`.

## 4. Phase C — packing

```
npx gltfpack@0.24 -i mid.glb -o 150-south-park.optimized.glb -c -km -kn -noq
```

`-km -kn` mandatory (glow-ness is name-only; without `-km` gltfpack merges materials across
the `_Glow` boundary and silently kills the night layer). `-noq` mandatory — the repo
standard, matching `pipeline/compress-assets.mjs`. Verified on the output rather than
trusting the flags: material name set identical (9), bbox identical to 5 dp,
`EXT_meshopt_compression` present, `KHR_mesh_quantization` absent.

163,700 B mid → 91,256 B packed.

**Gzip grows 78.4% and that is not a regression.** Meshopt buffers are already
entropy-coded, so gzip finds nothing and adds its own framing. 155 South Park recorded the
same effect at +68.7%. The number that matters is the 91,256 B the browser decodes, against
AGENTS.md's ≤ 500 KB per-landmark budget.

## 5. Phase E — A/B verification

`render_ab.py` on both files, same rig; landmark distances near = 1.5× long axis (29.8 m),
far = 6× (119.1 m); day (glow alpha 0.12) and night (alpha 1.0, emission 6, dusk world),
plus four orthographic elevations. `diff_ab.py` → `diffs.json`, `renders/contact_sheet.png`.

| View | Mean abs RGB Δ | Max px Δ |
|---|---|---|
| day near | 0.0166% | 36 |
| day far | 0.0215% | 22 |
| night near | 0.0018% | 8 |
| night far | 0.0028% | 14 |
| elev N | 0.0152% | 19 |
| elev E | 0.0247% | 68 |
| elev S | 0.0368% | 22 |
| elev W | 0.0210% | 46 |

Gate G4 allows ≤ 2% far and ≤ 4% near. The worst view is **0.037%**, fifty times inside the
tightest gate.

**Looked at the ×8-amplified diffs, honestly:** every non-zero pixel is a one-pixel
anti-aliasing seam along an existing silhouette edge — the parapet/coping junction, the
canopy slab's outline and its two rod stays, and the skylight kerbs seen from above. Nothing
moved, nothing vanished, no shading changed, and the address numerals, the two oxblood
window frames and the warm shopfront glow are pixel-stable. The isolated 68-level maximum on
elev E lands on the canopy's leading edge, one pixel wide. There is nothing here a player
could notice.

## 6. Gates

| Gate | Result |
|---|---|
| G1 Contract — material set identical (9), `_Glow` materials separate, no `Toy_body`, no manifest node names to preserve | **PASS** |
| G2 Geometry — bbox identical to 5 dp, origin identical, all closed-mesh signed volumes positive, ray-flip fraction 0.0 in **and** out (delta 0.0 over 22,500 rays / 17,000 hits) | **PASS** |
| G3 Round-trip — Blender re-import clean; `g3check` pinned-three loader: 11 meshes, 3,084 tris, 9 materials, no decode errors, `EXT_meshopt_compression` only | **PASS** |
| G4 Appearance — worst mean delta 0.037% against a 2%/4% gate; visually identical | **PASS** |
| G5 Draw submeshes — 55 → 11 | **PASS** |
| G6 Size — 186,872 → 91,256 B, −51.2% | **PASS with justification** (below) |
| G7 GPU budget — not applicable, `ALLOW_BAKE: no` | n/a |
| G8 Hygiene — re-import object count matches, no foreign geometry, deterministic re-run reproduces the output byte-for-byte, no `.blend1` left | **PASS** |

**G6 against the 60% aspirational target.** −51.2% falls short, and §2's census is the
required justification. After welding, 100% of the remaining geometry is silhouette: closed
box solids and wall panels, no curves to retessellate, no interior faces to remove, no
duplicate meshes left un-joined, and a triangle count already at half its own budget. The
only lever that could go further is decimation, which on an asset whose entire read is a
crisp wedge with a hard horizontal split would cost silhouette for bytes — a bad trade at
91 KB against a 500 KB budget.

## 7. Post-swap re-validation

The stage-2 contract validator (`validate_150_south_park.py`) was re-run against the packed
shipping file and returned **overall PASS**, all 16 checks, 3,084 triangles, dims
19.8521 × 17.5855 × 8.0, min Z 0.0. This is the check that would have caught a dissolve
sliver (`invalid_or_nonunit_loop_normal_count`), and it is clean.

`artifacts/150-south-park/validation.json` and `REPORT.md` carry the shipped numbers.
