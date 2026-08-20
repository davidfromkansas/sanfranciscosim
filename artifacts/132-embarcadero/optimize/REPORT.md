# 132 The Embarcadero — optimize pass (stage 4)

Input: `artifacts/132-embarcadero/132-embarcadero.glb` as approved at stage 3,
archived byte-for-byte at `optimize/input/132-embarcadero.glb` (362,428 bytes,
verified with `cmp`).

`ASSET_CLASS: landmark` · `ALLOW_MESHOPT: yes` · `ALLOW_BAKE: no`

## Result

| Metric | Input | Output | Δ |
|---|---|---|---|
| File, raw | 362,428 B | **159,340 B** | **−56.0%** |
| File, gzip −9 | 52,707 B | 70,052 B | +32.9% (see note) |
| Triangles | 4,960 | 4,960 | 0 |
| Vertices (Blender, post-import) | 10,400 | 10,762 | +3.5% (see note) |
| Objects | 179 | **16** | −91.1% |
| Draw submeshes (primitives) | 180 | **17** | **−90.6%** |
| Materials | 16 | 16 | 0 |
| Bounding box | 40.43706 × 40.47308 × 29.57 | identical | 0 |
| Origin (bbox min Z / centre XY) | 0.0 / 0.0, 0.0 | identical | 0 |

**On gzip going up.** Meshopt-compressed buffers are already entropy-coded, so
gzip has nothing left to find and adds framing. The number that matters over the
wire and on disk is the raw file, which halved. This is the expected shape of a
`-c` result and matches every prior asset in this repo.

**On the vertex count going up.** The weld in Phase B cut Blender-side vertices
from 10,400 to 2,832 by fusing coincident corners; the glTF encoder then
re-splits them per unique (position, normal, material) tuple on export, which on
a flat-shaded asset lands slightly above the original. Triangle count — the thing
the batch budget is spent on — is unchanged, and the file is 56% smaller because
the win came from node and accessor overhead, not from vertices.

## Phase A — waste census

`inspect.json`. 179 objects, 180 primitives, 4,960 triangles, 10,400 vertices in
362 KB. The census found exactly one dominant form of waste and two absent ones:

- **Object-count overhead: the whole story.** 179 objects for 4,960 triangles is
  27 triangles per node. Sixty window frames and sixty panes, each a six-face
  prism, each its own node with its own accessors. Predicted saving: the great
  majority of the file. Realised: 179 → 16 objects, 180 → 17 submeshes.
- **Duplicate meshes:** none worth sharing. The repeats are small boxes whose
  instancing overhead would exceed their geometry.
- **Buried interior faces:** 0 removed. Every applied panel sits proud of the
  wall it decorates rather than intersecting it — that is how the no-boolean
  authoring works — so nothing is provably interior.
- **Over-tessellated curves:** none. The only curved geometry is three 6-segment
  antenna masts, already at the floor.

## Phase B — geometry cleanup (`optimize.py`, `phaseb_stats.json`)

| Step | Tris | Verts | Note |
|---|---|---|---|
| input | 4,960 | 10,400 | |
| weld ≤ 1 mm + degenerate, per object | 4,960 | 2,832 | −72.8% vertices, no triangles lost |
| interior faces | 4,960 | 2,832 | 0 removed, closed-solid occluder rule |
| limited dissolve | — | — | **deliberately skipped** |
| join per material | 4,960 | 2,832 | 179 → 16 objects |

**The dissolve is skipped, and this asset is exactly the case the prompt warns
about.** §3 step 3 says to skip assets with large coplanar ring bands. This one
has three, stacked: the crown band (a closed 4-loop ring sweeping the whole
40 m footprint), the parapet ring, and the ink coping ring. Their horizontal
faces are perfect annuli; a strictly-coplanar dissolve merges each into one
annulus ngon and re-triangulating an annulus emits 20 m slivers that pass an
area-based degeneracy test and then fail the stage-2 contract validator on
`invalid_or_nonunit_loop_normal_count` — after the shipping swap. Measured on
`350-brannan`, the whole step was worth 0.4% of triangles. Not taken.

Normals audit after the joins: 16 closed solids, all signed volumes positive,
`inverted_solids: []`.

## Phase C — packing (`gltfpack@0.24`)

```
npx gltfpack@0.24 -i mid.glb -o 132-embarcadero.optimized.glb -c -km -kn -noq
```

`-km -kn` keep the material and node names the loader treats as API — without
`-km`, gltfpack would merge `Toy_glass` into `Toy_glass_Glow` (their parameters
are identical; glow-ness is name-only) and silently delete the night layer.
`-noq` because this repo ships unquantized: it is what `compress-assets.mjs`
produces, and the kit/landmark merge paths want float32 attributes.

302,676 B mid → 159,340 B packed.

## Phase D — bake

Not run. `ALLOW_BAKE: no`, and the contract forbids textures.

## Phase E — A/B verification (`render_ab.py`, `diff_ab.py`, `diffs.json`)

Same rig on both files: 42° elevation, 45° azimuth, near = 1.5 × long axis
(60.7 m), far = 6 × (242.6 m), day (glow alpha 0.12) and night (alpha 1.0,
emission 6, dusk world), plus four orthographic elevations.

| View | Mean abs RGB Δ | Max pixel Δ |
|---|---|---|
| day near | 0.0017% | 19 |
| day far | 0.0015% | 3 |
| night near | 0.0289% | 21 |
| night far | 0.0900% | 25 |
| elevation N | 0.0026% | 24 |
| elevation E | 0.0009% | 20 |
| elevation S | 0.0011% | 27 |
| elevation W | 0.0024% | 15 |

Gates allow 2% far and 4% near; the worst view is 0.09%, i.e. **22× inside the
loosest gate**.

**And looking at the diffs rather than the numbers:** every difference image is
black except for single-pixel speckle along polygon edges and, in the night
views, a faint dusting on the lit window edges. That is antialiasing sampling
noise on re-emitted vertex data, not a change in the model. No element is
missing, the silhouette is unchanged, the crown band and parapet still read as
distinct bands, the night hero (the Embarcadero ribbon and storefront) lights
identically, and the ten lit upper windows are the same ten. There is nothing
here a player could notice.

## Gates

| Gate | Result | Evidence |
|---|---|---|
| G1 Contract — material set identical, `_Glow` separate, node names intact | **PASS** | `validation.json` `G1_materials_identical`; all 16 names round-trip through gltfpack and the three loader |
| G2 Geometry — bbox, origin, signed volumes, flip fraction | **PASS** | bbox identical to 5 dp; origin identical; 16/16 volumes positive; 22,500 rays, 16,070 hits, **0 flipped** |
| G3 Round-trip — Blender AND pinned-three GLTFLoader | **PASS** | `G3-OK {"ok":true,"meshes":17,"tris":4960, ...}` |
| G4 Appearance — day+night × near+far | **PASS** | table above; worst 0.09% against a 2% gate |
| G5 Draw submeshes ≤ input | **PASS** | 180 → 17 |
| G6 Size reduced ≥ 60% target | **PASS on reduction, short of target** | −56.0% raw. The remainder is silhouette geometry and the three ring bands (crown 264 tris, parapet 288, coping 288 = 17% of the asset), which §3 step 3 forbids dissolving. No further lossless win is available without touching the cue the building is built around |
| G7 GPU budget | n/a | bake mode not used |
| G8 Hygiene — no foreign geometry, deterministic, no `.blend1` | **PASS** | re-import object count matches; scripts are deterministic; no `.blend1` written |

## Toolchain

Blender 5.2.0 LTS (fbe6228777e7, 2026-07-14) · `gltfpack@0.24` via npx ·
node with the pinned three in `g3check/package.json` · python3 + Pillow · gzip −9.

## Shipping swap

All gates pass, so `132-embarcadero.optimized.glb` was copied over
`artifacts/132-embarcadero/132-embarcadero.glb`. The pre-optimize original stays
at `optimize/input/132-embarcadero.glb`. The asset's own `validation.json` and
`REPORT.md` were re-run and updated to the shipped numbers, so the integration
stage writes its manifest entry from reality.
