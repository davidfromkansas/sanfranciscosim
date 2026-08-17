# 27 South Park — GLB optimize pass

Stage 4 of `docs/asset-pipeline/ADDRESS-TO-ASSET.md`, run per
`docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md` v2 with the defaults
`ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`.
Scripts are adapted copies of `tools/glb-optimize/`; the two adaptations are
documented in §3 and §7.

## Metrics

| | input | shipped | Δ |
|---|---|---|---|
| File, raw | 295,960 B (289 KB) | **139,072 B (136 KB)** | **−53.0%** |
| File, gzip -9 | 51,967 B | 92,218 B | +77% (see note) |
| Triangles | 4,968 | 4,968 | 0 |
| Vertices | 9,812 | 2,632 | **−73.2%** |
| Mesh objects | 77 | **11** | −85.7% |
| Draw submeshes (primitives) | 78 | **12** | −84.6% |
| Materials | 11 | 11 | identical set |
| Bbox | 32.6129 × 32.5074 × 10.2000 m | identical | 0 |
| Origin | (0, 0, 0), min Z 0 | identical | 0 |

**On the gzip row.** meshopt-compressed buffers are already entropy-coded, so
re-gzipping them expands rather than shrinks. The number that matters on disk
and over the wire is the raw 136 KB, which is what the CDN serves and what the
≤ 500 KB per-landmark budget in `AGENTS.md` is measured against. Every shipped
landmark carries `EXT_meshopt_compression` for the same reason.

## Phase A — waste census

`inspect.py` on `input/27-south-park.glb`:

| finding | count | technique | predicted |
|---|---|---|---|
| coincident vertex pairs ≤ 1 mm | 7,180 | per-object weld | −70% verts |
| objects sharing a material | 77 → 11 groups | join per material | −66 nodes, −66 primitives |
| duplicate/repeated mesh triangles | 2,572 | join (small counts) not instancing | 0 tris, node overhead only |
| degenerate faces | **0** | — | — |
| buried interior faces | 0 provable | occluder rule (closed solids only) | — |
| over-tessellated curves | 0 | — | — |

The vertex count is the whole story on this asset: it is built from ~77 closed
prisms authored independently, so almost every wall corner carries duplicated
verts. The triangle count is not waste — it is 4,968 triangles of arcade,
joinery, parapet ring and roof plant, all of it silhouette or facade relief at
the app's camera. Nothing here can be removed without removing the building.

## Phase B — geometry cleanup

| step | tris | verts |
|---|---|---|
| input | 4,968 | 9,812 |
| weld ≤ 1 mm + degenerate | 4,968 | 2,632 |
| interior faces (0 removed) | 4,968 | 2,632 |
| limited dissolve | **skipped — see below** | |
| join per material | 4,968 | 2,632 |

**Step 3 (limited dissolve) was skipped deliberately.** GLB-OPTIMIZE-PROMPT §3
step 3 says to skip it on assets with large coplanar ring bands, and this asset
has three that follow the whole footprint — `base`, `parapet` and `coping`.
Their top and bottom faces are perfectly coplanar annuli, so even a strictly
coplanar 0.05° dissolve merges each into one annulus ngon whose
re-triangulation emits slivers up to the building's full 33.55 m length at
~0.2 mm width. Those pass an area-based degeneracy test and only surface after
the shipping swap, as `invalid_or_nonunit_loop_normal_count` in the stage-2
contract validator, because gltfpack re-emits the stored collapsed normals
while Blender recomputes them on import and hides the problem
(measured on `350-brannan`, 13 Aug 2026).

It was also measured here before being removed: an unpatched run of the generic
script on this same input reported `tris=4968` before and after the dissolve, so
on this asset the step was worth **exactly zero triangles** and carried only the
risk. The skip and that measurement are recorded in `optimize.py` itself.

Step 4 (curve retessellation) was also skipped: the only curves are the
6-segment segmental arch heads and the 8/10-segment roof fans, all already at
the floor of what reads at the near distance.

## Phase C — packing

```
npx gltfpack@0.24 -i mid.glb -o 27-south-park.optimized.glb -c -km -kn -noq
```

`-km -kn` keep material and node names (glow-ness is name-only, so without
`-km` gltfpack would merge `Toy_gold_Glow` into an identically-parameterised
opaque material and silently kill the night layer). `-noq` is the repo standard
— `pipeline/compress-assets.mjs` produces unquantized output and the
kit/landmark merge paths need float32 attributes.

`compress-assets.mjs` will skip this file at ship time because it already
carries `EXT_meshopt_compression`; that is the intended behaviour, and this pass
IS the intake compression.

Phase D (high→low bake) not run — `ALLOW_BAKE: no`, and the contract forbids
textures.

## Phase E — A/B verification

`render_ab.py` at azimuth **315°** rather than the generic script's 45°: this
building's only public elevation faces 314.8°, and a pixel diff taken against a
blind party wall proves nothing. Landmark distances: near 48.92 m
(1.5 × long axis), far 195.68 m (6×).

| view | mean abs RGB Δ | max px Δ |
|---|---|---|
| day near | **0.031%** | 34 |
| day far | 0.027% | 11 |
| night near | 0.011% | 12 |
| night far | 0.010% | 3 |
| elev N | 0.036% | 21 |
| elev E | 0.043% | 25 |
| elev S | 0.025% | 24 |
| elev W | 0.023% | 44 |

Gate G4 allows 4% near / 2% far; the worst reading here is 0.043%.

**Looking at the ×8-amplified diffs honestly:** the only thing visible is a
hairline along the parapet coping edge and a few isolated pixels at the arch
crowns and the roof-unit corners — antialiasing on edges whose vertices were
welded from two coincident copies into one. Nothing is missing, no silhouette
moved, no shading changed, and at 1× the two renders are indistinguishable.
There is nothing here a player could notice.

## Gate results

| gate | result | evidence |
|---|---|---|
| **G1** contract | **PASS** | material set identical (11, `Toy_glass_Glow` and `Toy_gold_Glow` still separate); no `Toy_body`; no manifest-named nodes on this asset |
| **G2** geometry | **PASS** | bbox identical to 4 dp; origin (0,0,0); all signed volumes positive; 22,500 rays, 15,257 hits, **0 flipped** (0.000%) |
| **G3** round-trip | **PASS** | re-imports in Blender 5.2; `g3check` (pinned three, node v22.19.0) → `{"ok":true,"meshes":12,"tris":4968,...}` |
| **G4** appearance | **PASS** | table above; worst 0.043% against a 2–4% gate |
| **G5** draw submeshes | **PASS** | 78 → 12 |
| **G6** size | **PASS with a note** | −53.0% raw against a 60% aspiration. The census shows why: Phase B removed **zero triangles** because there is no triangle waste — the remainder is arcade, joinery, parapet ring and roof plant, all silhouette or facade relief. The win available on this asset was vertex duplication (−73%) and node overhead (−86%), and both were taken in full |
| **G7** GPU budget | n/a | bake mode not used |
| **G8** hygiene | **PASS** | re-import object/material counts match; deterministic re-run reproduces byte-identical output; no `.blend1` files |

## Shipping swap

`27-south-park.optimized.glb` copied over `artifacts/27-south-park/27-south-park.glb`.
The pre-optimize original is archived byte-for-byte at
`optimize/input/27-south-park.glb` (verified with `cmp` before any work started).

**The stage-2 contract validator was re-run on the packed shipping file**, not
just on the pre-pack mid — this is the step that catches the sliver-normal
failure described in Phase B, which exists only in the packed encoding:

```
overall PASS — 16/16 checks
tris 4968 · objects 11 · dims [32.6129, 32.5074, 10.2] · materials 11
```

`artifacts/27-south-park/validation.json` and `REPORT.md` now carry the shipped
numbers, so the integration stage writes its manifest entry from reality.

## Toolchain

Blender 5.2.0 LTS (fbe6228777e7) · gltfpack 0.24 via `npx` · node v22.19.0 ·
python3 + Pillow · gzip -9 · `g3check` with the pinned three from
`tools/glb-optimize/g3check/package.json`.
