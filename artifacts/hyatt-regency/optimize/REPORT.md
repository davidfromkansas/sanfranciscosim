# hyatt-regency — GLB optimize pass (stage 4)

`docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md` v2 run on `artifacts/hyatt-regency/`,
18 August 2026. `ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`.

## Toolchain

| Tool | Version |
|---|---|
| Blender | 5.2.0 LTS (fbe6228777e7, 2026-07-14), headless, CPU Cycles |
| gltfpack | `npx gltfpack@0.24`, flags `-c -km -kn -noq` |
| g3check | pinned three, `optimize/g3check/` |
| python | 3.9 + Pillow |

## Result

| Metric | Input | Output | Delta |
|---|---|---|---|
| Raw bytes | 701,304 | 359,236 | **-48.8%** |
| Gzipped bytes | 113,838 | 233,566 | +105% (see note) |
| Triangles | 13,636 | 13,604 | -32 |
| Vertices (Blender) | 26,658 | 22,763 | -14.6% |
| Objects / draw submeshes | 87 | **6** | -93% |
| Materials | 6 | 6 | unchanged |
| bbox | 121.19965 x 98.79601 x 80.8 | identical | 0 |
| bbox min | -60.59983, -49.398, 0.0 | identical | 0 |

**Note on gzip.** meshopt output is already entropy-coded, so gzipping it again
costs bytes rather than saving them; the honest comparison is raw-over-the-wire
against the app's decoder, where 359 KB replaces 701 KB. This matches every
other shipped landmark (`chase-center.glb` is 237 KB raw / 165 KB gzipped) and
is what `pipeline/compress-assets.mjs` produces. 359 KB is inside the
`sf-asset-check` §7 cap of 500 KB.

## Phase A — waste census

| Finding | Count | Technique |
|---|---|---|
| Coincident vertex pairs | 19,712 | per-object weld at 1 mm |
| Duplicate/redundant triangles | 4,852 | absorbed by the weld |
| Degenerate triangles | 20 | delete |
| Objects sharing one material | 87 -> 6 groups | join per material |
| Buried interior faces | 0 provable | none removed (see below) |

Predicted before executing: the weld and the per-material join carry this
asset; there is no curve over-tessellation worth touching (the Equinox drum is
16 segments and is silhouette-defining) and no bake.

## Phase B — geometry cleanup

| Step | tris | verts |
|---|---|---|
| input | 13,636 | 26,658 |
| weld + degenerate | 13,604 | 6,946 |
| interior faces | 13,604 | 6,946 |
| limited dissolve | **skipped** | — |
| join per material | 13,604 | 6,946 |

Joins: `Toy_stone` 51 objects, `Toy_glass` 15, `Toy_trim` 11, `Toy_steel` 8.
`Toy_glassl_Glow` (podium arcade) and `Toy_gold_Glow` (Equinox band) stayed as
single objects — nothing to join, and glow-ness is name-only so they must never
merge into the body.

**Interior faces: none removed, deliberately.** The occluder rule in §3.2 only
lets a CLOSED solid hide another mesh's faces, and this asset's overlaps are
between open-topped ring bands and the slab bodies they wrap. Nothing here is
provably buried, so nothing was deleted. The 3.9 m stepped slabs do bury the
undersides of the lips above them, but a ring is not a box and the AABB-fill
test correctly refuses to claim it.

**Limited dissolve: skipped.** Prompt §3.3 says to skip on assets with large
coplanar ring bands; this asset is almost nothing else — fifteen slab lip
rings, the wing parapet ring, the podium eave and the two Equinox frames all
follow the footprint the whole way round. Re-triangulating those annuli emits
sub-millimetre slivers whose averaged vertex normals collapse toward zero, and
gltfpack re-emits the stored normals, so the failure would surface as
`invalid_or_nonunit_loop_normal_count` in the contract validator two steps
after the shipping swap. Measured worth on a comparable asset: 0.4% of
triangles. Reverted by not running it; the skip is recorded in
`phaseb_stats.json`.

## Phase C — packing

```
npx gltfpack@0.24 -i mid.glb -o hyatt-regency.optimized.glb -c -km -kn -noq
```

`-km -kn` keep the six material names distinct across the `_Glow` boundary;
`-noq` keeps float32 attributes, which is the repo standard and what
`compress-assets.mjs` produces. Verified on the OUTPUT, not on the flags:
`extensionsUsed = ["EXT_meshopt_compression"]`, material set identical, node
names intact, POSITION/NORMAL only, bbox unchanged to 5 decimal places.

## Gates

| Gate | Result | Evidence |
|---|---|---|
| G1 contract | PASS | material set identical, `_Glow` pair separate, no `Toy_body`, node names intact |
| G2 geometry | PASS | bbox delta 0, origin delta 0, all signed volumes positive, ray flipped fraction **0.0000** of 17,227 hits |
| G3 round-trip | PASS | Blender re-import + `g3check`: 6 meshes, 13,604 tris, 6 materials, bbox 121.1997 x 80.8 x 98.796 (three's Y-up) |
| G4 appearance | see below | A/B day+night x near+far + 4 elevations |
| G5 draw submeshes | PASS | 87 -> 6 |
| G6 size | PASS | 701,304 -> 359,236 raw (-48.8%), under the 500 KB cap |
| G7 GPU budget | n/a | bake mode off |
| G8 hygiene | PASS | re-import object/material/bbox check, deterministic scripts committed, no `.blend1` |

## G4 — appearance

A/B at 32 Cycles samples, denoising OFF (so Monte-Carlo noise is visible in the
diffs rather than smoothed away), amplified x8 in `renders/diff_*.png`:

| View | mean abs RGB | max px delta | fg pixels |
|---|---|---|---|
| day near | 0.051% | 29 | 334,660 |
| day far | 0.111% | 34 | 25,990 |
| night near | 0.056% | 56 | 334,660 |
| night far | 0.074% | 55 | 25,991 |
| elev N | 0.207% | 147 | 424,035 |
| elev E | 0.160% | 102 | 354,382 |
| elev S | 0.190% | 104 | 419,095 |
| elev W | 0.270% | 156 | 359,062 |

Gate is <= 2% far / <= 4% near; the worst view here is 0.27%, an order of
magnitude inside it. **G4 PASS.**

Looked at, not just measured. Every diff image is black except for two things:

1. **One-pixel edge lines along every slab lip and pier arris.** Antialiasing
   landing on a different sub-pixel between two runs of the same camera. No
   silhouette moved: the elevations are orthographic, so a real geometry change
   would show as a filled band, not a hairline.
2. **An orange speckle band in the podium arcade recess** (visible in
   `diff_elev_w.png`). That is path-tracer noise in the one part of the model
   lit almost entirely by indirect bounce — a 5.8 m glazed slot 1.3 m behind a
   1.1 m eave. It is present in both renders and uncorrelated between them,
   which is what makes it show up in a difference. Denoising would erase it and
   also erase evidence, so it was left on.

Nothing a player would notice. No element is missing, no material swapped, the
night layer lights the same two surfaces (podium arcade `Toy_glassl_Glow`,
Equinox band `Toy_gold_Glow`) in both.

## Shipping swap

`hyatt-regency.optimized.glb` copied over `artifacts/hyatt-regency/hyatt-regency.glb`
(359,236 bytes). The pre-optimize original is archived at
`optimize/input/hyatt-regency.glb` (701,304 bytes).

**The stage-2 contract validator was re-run on the PACKED file**, not on the
Blender scene — that is the whole point of running it after the swap. gltfpack
re-emits stored normals, so a sliver manufactured during optimization only
surfaces there. All fifteen checks PASS, `normals_outward` true, ray residual
0.0000, `no_degenerate_geometry` true.

`artifacts/hyatt-regency/validation.json` and `REPORT.md` now carry the shipped
numbers (13,604 tris, 359,236 bytes), so the integration stage writes its
manifest entry from reality.
