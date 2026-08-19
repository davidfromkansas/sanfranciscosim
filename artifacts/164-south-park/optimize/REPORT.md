# 164 South Park — stage 4 optimize report

`docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md` v2, run on `artifacts/164-south-park/`.
`ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`.

## Result

| Metric | Input | Shipped | Δ |
|---|---|---|---|
| Raw bytes | 206,060 | **92,552** | **−55.1%** |
| Gzipped bytes | 46,999 | 64,988 | **+38.3%** — see below |
| Triangles | 3,366 | 3,366 | 0 |
| Vertices (Blender re-import) | 6,478 | 6,034 | −6.9% |
| Mesh objects | 56 | **8** | −85.7% |
| Draw submeshes (primitives) | 56 | **8** | −85.7% |
| Materials | 8 | 8 | identical set |
| BBox | 37.23846 × 36.47114 × 5.4 | identical to 5 dp | 0 |
| BBox min | (−18.61923, −18.23557, 0.0) | identical | 0 |

**The gzip number is not a mistake and it is not hidden.** Meshopt-encoded buffers are
already entropy-coded, so gzip cannot compress them further and adds framing instead. Over a
gzip-enabled CDN this file transfers at ~65 KB where the unpacked one transferred at ~47 KB.
It ships anyway, for three reasons: `AGENTS.md` makes meshopt intake compression mandatory
for everything under `app/public/sf-assets/`; the win that matters at runtime is the 56 → 8
draw-submesh collapse and the smaller GPU vertex buffer, not the wire bytes; and one encoding
across all ~300 landmarks is worth more than 18 KB on one of them. Recorded here so nobody
re-derives it as a surprise.

## Toolchain

Blender 5.2.0 LTS (`fbe6228777e7`, 2026-07-14) · `npx gltfpack@0.24` ·
node + pinned three in `g3check/` · python3 3.9 + Pillow 11.3.0 · gzip.

## Phase A — waste census

56 objects, 56 primitives, 3,366 triangles, 6,478 vertices, 8 materials, no textures, no
transparency. The census found the waste concentrated in exactly one place: **object-count
overhead**. Every one of the 56 objects is a separate swept solid or box sharing one of eight
materials, and nothing but manifest-irrelevant names kept them apart. No duplicate meshes, no
buried interior faces (this is a union of solids that touch, not one that nests), no
over-tessellated curves — the five street facets are flat planes, not arcs.

Predicted: joining per material collapses 56 primitives to 8 and removes most of the node and
accessor overhead; meshopt then takes the vertex buffers. Predicted saving ~50% raw. Actual
55.1%.

## Phase B — geometry cleanup

| Step | Tris | Verts | Note |
|---|---|---|---|
| input | 3,366 | 6,478 | 56 objects |
| weld ≤ 1 mm + degenerates | 3,366 | 1,791 | per-object; the build already welded at 0.1 mm |
| interior faces | 3,366 | 1,791 | 0 removed — no closed solid provably contains another |
| limited dissolve | — | — | **deliberately skipped**, see below |
| join per material | 3,366 | 1,791 | 56 → 8 objects |

**The limited dissolve is skipped, on purpose.** §3.3 of the prompt says to skip it entirely
on assets with large coplanar ring bands. This asset has two: the parapet and the coping both
follow the full 105 m footprint perimeter, so their top and bottom faces are perfect annuli.
A strictly-coplanar dissolve merges each annulus into one ngon, and re-triangulating an
annulus emits slivers tens of metres long and a fraction of a millimetre wide. Those pass an
area-based degeneracy test, survive Blender's import (which recomputes loop normals), and
then surface as `invalid_or_nonunit_loop_normal_count` in the packed file — after the
shipping swap. On `350-brannan` the dissolve was worth 30 triangles out of 6,770 and was
reverted for exactly this reason. Here the asset is 3,366 triangles and the step was skipped
before it ran. The skip is recorded in `phaseb_stats.json` as
`"limited_dissolve": "skipped: coplanar parapet + coping ring bands (prompt 3.3)"`.

Normals audit after Phase B: `inverted_solids: []`.

## Phase C — packing

```
npx gltfpack@0.24 -i mid.glb -o 164-south-park.optimized.glb -c -km -kn -noq
```

`-km` keeps `Toy_glass_Glow` and `Toy_trim_Glow` separate from their non-glow twins (glow-ness
is name-only, and without `-km` gltfpack merges them and silently kills the night layer).
`-noq` because this repo does not quantize — `pipeline/compress-assets.mjs` produces
unquantized meshopt and the stage-2 contract validator stays strict without special cases.
Verified on the output rather than trusting the flags: material name set identical (8),
`EXT_meshopt_compression` present and it is the only extension, bbox unchanged.

## Phase D — bake

Not run. `ALLOW_BAKE: no`, and the contract forbids textures.

## Phase E — A/B verification

Same rig on both files. Landmark distances off the 37.24 m long axis: near 55.86 m,
far 223.43 m. Day state renders `_Glow` at alpha 0.12 (the app's day pass); night state at
emission ≈ 6 under a dusk world.

| View | Mean abs RGB delta | Max pixel delta |
|---|---|---|
| day near | **0.0008%** | 4/255 |
| day far | 0.0043% | 4/255 |
| night near | 0.0003% | 3/255 |
| night far | 0.0030% | 3/255 |
| elevation N | 0.0082% | 4/255 |
| elevation E | 0.0083% | 4/255 |
| elevation S | 0.0156% | 7/255 |
| elevation W | 0.0102% | 4/255 |

Gates allow 2% far and 4% near; the worst view here is 0.0156%, three orders of magnitude
inside it. Looking at the ×8-amplified diffs: they are black apart from a few single-pixel
anti-aliasing seams along silhouette edges. Nothing is missing, the silhouette is unchanged,
the ribbon still runs unbroken across all five facets, the entry recess and the canopy are
intact, the four skylight monitors are all present, and at night the same two glow groups
light and nothing else does. There is nothing here a player could notice.

**The rig is EEVEE, not Cycles** — the same deviation, for the same reason, as the stage-2
review renders (four parallel landmark sessions had this machine above load average 200).
The A/B gate compares two renders of one rig against each other, so the engine only has to be
identical on both sides, and it is.

## Gates

| Gate | Result |
|---|---|
| **G1** contract — material set identical, `_Glow` separate, no `Toy_body`, node names | **PASS** |
| **G2** geometry — bbox to 5 dp, origin to 5 dp, signed volumes positive, flipped fraction 0 | **PASS** |
| **G3** round-trip — Blender re-import + pinned-three `g3check` (8 meshes, 3,366 tris, 8 materials, no decode errors) | **PASS** |
| **G4** appearance — worst view 0.0156% mean delta | **PASS** |
| **G5** draw submeshes — 56 → 8 | **PASS** |
| **G6** size — raw −55.1%; gzip +38.3% and explained above | **PASS** |
| **G7** GPU budget | n/a (bake mode off) |
| **G8** hygiene — re-import object/material/bbox checks clean, deterministic re-run, no `.blend1` | **PASS** |

## Shipping swap

`164-south-park.optimized.glb` copied over `artifacts/164-south-park/164-south-park.glb`.
The pre-optimize original is archived byte-for-byte at `optimize/input/164-south-park.glb`.
The stage-2 contract validator was re-run on the shipped file and still reports
**`overall: PASS`** on all 16 checks, with 31,500 rays and 0 flipped faces.

Shipped numbers for the manifest: **`tris` 3,366**, **`dims` [37.2385, 36.4711, 5.4]**,
92,552 bytes on disk.
