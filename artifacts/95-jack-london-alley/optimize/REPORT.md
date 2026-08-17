# 95 Jack London Alley — GLB optimize pass

Stage 4 of `docs/asset-pipeline/ADDRESS-TO-ASSET.md`, run per
`docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md` (v2) on 17 August 2026.
`ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`.

## Toolchain

| Tool | Version |
|---|---|
| Blender | 5.2.0 LTS (`fbe6228777e7`, 2026-07-14), headless |
| gltfpack | `npx gltfpack@0.24`, flags `-c -km -kn -noq` |
| g3check | pinned three, `tools/glb-optimize/g3check/package.json` |
| python3 | 3.9 + Pillow |

Scripts are the generic `tools/glb-optimize/` copies with per-asset constants
only; `diff_ab.py`'s hard-coded contact-sheet title was the single edit.

## Metrics

| | input | shipped |
|---|---|---|
| File, raw | 236,120 B (230.6 KB) | **112,904 B (110.3 KB)** — **−52.2%** |
| File, gzip -9 | 49,953 B | 79,933 B |
| Triangles | 3,888 | **3,888** (unchanged) |
| Vertices | 7,816 | **6,832** (−12.6%; 2,040 in Blender before the exporter re-splits by normal) |
| Mesh objects | 48 | **13** |
| Draw primitives | 49 | **14** |
| Materials | 13 | 13, identical set |
| bbox dims | 16.1965 × 16.0932 × 8.4 | identical to 5 dp |
| bbox min | −7.9973, −7.9425, 0.0 | identical |

Compressed on-disk size is **110 KB against a 500 KB budget**. The gzip figure
grows because meshopt buffers are already entropy-coded; the raw size is the wire
size that matters, and `compress-assets.mjs` will skip this file at intake because
it already carries `EXT_meshopt_compression`.

## Waste census (Phase A) and what each technique actually returned

| Finding | Predicted | Delivered |
|---|---|---|
| 5,776 coincident vertex pairs | the big one — every applied panel is a closed prism butted against the wall | **weld: 7,816 → 2,040 verts in Blender (−74%)**, the single largest win |
| 48 objects across 13 materials | node/accessor overhead, 49 draw primitives | **join per material: 48 → 13 objects, 49 → 14 primitives** |
| 1,076 "duplicate redundant" tris (two columns, two vents, two flanking windows, two mullions) | absorbed by the joins | absorbed |
| 0 degenerate tris | nothing to reclaim | 0 |
| interior faces buried in box-like solids | ~0 — this asset's panels are butted, not buried, and the occluder rule requires a provably closed solid | **0 removed**, as predicted |
| over-tessellated curves | the two 10-segment column shafts and two 10×5 globes are already at the style bible's floor | **skipped** — halving them would be visible on the silhouette at 24 m near distance |

**Limited dissolve returned exactly 0 triangles and was left in.** The prompt's
ring-band warning (a coping or parapet that follows the footprint all the way round
dissolves into an annulus ngon and re-triangulates into 0.24 mm slivers) does not
bite here: this asset's parapet is four separate flat panels, not a `ring_band`
annulus, so there is no annulus to merge. The stage-2 contract validator was
re-run **on the packed file** specifically to check for that failure mode and
returns `invalid_or_nonunit_loop_normal_count: 0`, `degenerate_triangle_count: 0`.

Triangle count is unchanged end to end, which is the correct outcome for an asset
whose 3,888 triangles are all silhouette or facade relief on a 6,000 budget. The
52% came entirely from vertex welding, node consolidation and meshopt.

## Gates

| Gate | Result | Evidence |
|---|---|---|
| **G1 Contract** | **PASS** | material name set identical (13/13); `Toy_gold_Glow` and `Toy_trim_Glow` still separate from `Toy_gold`/`Toy_trim` (this is what `-km` protects); no `Toy_body`; no manifest-named nodes on this asset |
| **G2 Geometry** | **PASS** | bbox identical to 5 dp, origin offset unchanged at `[0.101, 0.104]`; all signed volumes positive; ray-flip fraction 0.0000 |
| **G3 Round-trip** | **PASS** | re-imports in Blender; `g3check` → `G3-OK {"ok":true,"meshes":14,"tris":3888,...}`, all 13 materials present, no decode errors |
| **G4 Appearance** | **PASS** | day/night × near(24.3 m)/far(97.2 m) + 4 elevations. Mean absolute RGB delta **0.0009%–0.0130%**, against gates of 2% far / 4% near. Max single-pixel delta 113 on one elevation, on an anti-aliased silhouette edge. The ×8-amplified diff row is black apart from hairlines tracing the outline and the arch reveal — **there is nothing here a player could notice.** |
| **G5 Draw submeshes** | **PASS** | 49 → 14 |
| **G6 Size** | **PASS with a note** | −52.2%, short of the 60% aspiration. The census accounts for the remainder: triangles did not move because all 3,888 of them are silhouette or facade relief, and this asset was already under 240 KB before the pass |
| **G7 GPU budget** | n/a | bake mode off |
| **G8 Hygiene** | **PASS** | re-import object/material counts match; deterministic re-run reproduces the output; no `.blend1` files |

## Shipping swap

`95-jack-london-alley.optimized.glb` copied over
`artifacts/95-jack-london-alley/95-jack-london-alley.glb`. The pre-optimize
original is archived byte-for-byte at `optimize/input/95-jack-london-alley.glb`
(verified with `cmp` before the pass began).

The asset's own `validation.json` and `REPORT.md` were re-run and updated to the
shipped numbers, so the integration stage writes its manifest entry from reality:
**13 objects, 3,888 tris, 110.3 KB, dims 16.1965 × 16.0932 × 8.4, crest 8.40 m,
overall PASS.**
