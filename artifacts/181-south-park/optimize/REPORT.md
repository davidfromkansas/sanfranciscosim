# 181 South Park — optimize pass (stage 4)

Run of `docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md` against
`artifacts/181-south-park/`, 13 August 2026.
`ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`.

Toolchain: Blender 5.2.0 LTS (hash fbe6228777e7), `npx gltfpack@0.24`,
node + pinned three in `g3check/`, python3 + Pillow 11.3.0, gzip −9.

## Metrics

| | Input | Optimized | Δ |
|---|---|---|---|
| File, raw | 290,832 B | **139,356 B** | **−52.1%** |
| File, gzip −9 | 52,306 B | 86,139 B | +64.7% (see §4) |
| Objects / draw submeshes | 121 | **9** | −92.6% |
| Triangles | 4,200 | 4,200 | 0 |
| Vertices | 8,680 | **2,336** | −73.1% |
| Materials | 9 | 9 | identical set |
| bbox dims | 40.8359 × 40.5282 × 16.5 | 40.8359 × 40.5282 × 16.5 | 0 |
| bbox min | −20.4205, −20.2523, 0.0 | −20.4205, −20.2523, 0.0 | 0 |

## Waste census (Phase A)

`inspect.json`, run against the byte-identical archive at `input/`:

| Finding | Count | Technique | Predicted | Actual |
|---|---|---|---|---|
| One object per primitive | 121 objects / 121 primitives | join per material | → 9 | → 9 |
| Coincident vertex pairs | 6,344 | weld ≤ 1 mm, per object | large vert cut | 8,680 → 2,336 verts |
| Duplicate mesh groups | 13 groups, 1,976 redundant tris | absorbed by the join | — | no tri change |
| Degenerate faces | 0 | — | — | — |
| Buried interior faces | 0 removable | occluder rule: nothing here is a closed solid that provably hides another | 0 | 0 |
| Over-tessellated curves | none | asset has no curved shells; the gable is planar | 0 | 0 |

The triangle count does not move, and that is the correct outcome: every
triangle in this asset is on a visible surface. All the waste was **structural**
— 121 nodes and 121 draw submeshes for a 4,200-triangle building, plus a vertex
buffer nearly four times larger than it needed to be.

## Phase B — geometry cleanup

| Step | Tris | Verts |
|---|---|---|
| input | 4,200 | 8,680 |
| 1. weld ≤ 1 mm + degenerate | 4,200 | 2,336 |
| 2. interior faces | 4,200 | 2,336 |
| 3. limited dissolve 0.05° | 4,200 | 2,336 |
| 5. join per material | 4,200 | 2,336 (121 → 9 objects) |
| **6b. flat-shading re-assert** | 4,200 | 2,336 |

Steps 4 (curve retessellation) and 6 (instancing) are no-ops for this asset.
Normals audit: `inverted_solids: []`.

**Step 6b is an addition to the generic script, and it is the judgment call of
this pass.** The first run came out with a mean A/B pixel delta of 1.50% at the
near day camera — inside the 4% gate, but the 8×-amplified diff showed the
change was not noise: it was a smooth gradient across the roof slopes and
nothing else. The cause is step 1. Welding coincident vertices inside an object
averages the loop normals where faces of different orientation met at those
vertices, so the roof — a large planar surface whose eave, ridge cap and slope
met at welded seams — picked up interpolated shading. Measured as mean deviation
between loop normals and their face normals:

| | mean loop-vs-face normal deviation | smooth-flagged polys |
|---|---|---|
| input | 0.000278 | 1,098 |
| optimized, before 6b | **0.014617** | 1,184 |
| optimized, after 6b | **0.000000** | 232 |

The source model is authored `shade_flat` throughout, so re-asserting flat
shading after the weld restores the authored state rather than changing it — and
faceted, chunky surfaces are precisely what `docs/styles/miniature-toy.md` asks
for. It costs 19,076 bytes (flat shading splits vertices per face at the export
boundary) and takes the pixel delta to essentially zero. Worth it.

This is generic behaviour, not asset-specific: any welded asset authored flat
will drift the same way. It is a candidate to promote into
`tools/glb-optimize/optimize.py` after one more asset confirms it.

## Phase C — packing

```
npx gltfpack@0.24 -i mid.glb -o 181-south-park.optimized.glb -c -km -kn -noq
```

`-km` and `-kn` keep the material set intact across the `_Glow` boundary;
`-noq` is the repo standard (see the prompt's §4 note) and is what
`pipeline/compress-assets.mjs` produces.

**§4 gzip note.** Raw drops 52.1% while gzip rises 64.7%. This is expected and
matches `380-brannan`, which recorded raw −51.8% / gzip +102% on the same
recipe: meshopt-encoded buffers are already compressed, so gzip cannot compress
them further, while the unpacked input's repetitive float arrays gzip very well.
The wins that matter here are the 92.6% cut in draw submeshes and the 73.1% cut
in vertex-buffer bytes, both of which are runtime costs, not transfer costs.

## Phase E — A/B verification

Landmark cameras: near = 1.5 × long axis, far = 6 × long axis, day
(glow alpha 0.12) and night (glow lit), plus four orthographic elevations.
Rendered in EEVEE at 96 samples rather than Cycles — the materials are flat,
untextured and opaque so the engines are equivalent here, both sides of the A/B
were rendered identically, and the authoring machine was running several batch
sessions at once (load average ~490) where Cycles CPU could not finish the pass.
`SF_AB_ENGINE=CYCLES` switches back.

| View | Mean abs RGB delta | Max px delta | Gate |
|---|---|---|---|
| day near | 0.0002% | 3 | ≤ 4% |
| day far | 0.0001% | 0 | ≤ 2% |
| night near | 0.0004% | 1 | ≤ 4% |
| night far | 0.0001% | 0 | ≤ 2% |
| elev N | 0.0059% | 8 | — |
| elev E | 0.0023% | 5 | — |
| elev S | 0.0073% | 4 | — |
| elev W | 0.0059% | 6 | — |

**What the diffs actually show, honestly:** nothing. After step 6b the 8×
amplified diff images are black apart from a scatter of single-pixel edge
samples on the orthographic elevations, where a max delta of 8/255 on a handful
of silhouette pixels is antialiasing, not geometry. No missing elements, no
silhouette change, no shading artifacts, and the night layer lights the same six
windows, two roof slots, storefront and canopy in both. Before 6b there was a
visible-under-amplification roof gradient; that is what 6b removed.

## Gates

| Gate | Result | Evidence |
|---|---|---|
| G1 Contract | **PASS** | material set identical (9), `_Glow` pair kept separate, no `Toy_body`, node names not manifest-referenced |
| G2 Geometry | **PASS** | bbox and origin identical to 4 dp; signed volumes all positive; flipped fraction 0.0000 over 22,500 rays / 14,000 hits |
| G3 Round-trip | **PASS** | Blender re-import OK; `g3check` pinned-three `G3-OK`, 9 meshes, 4,200 tris, meshopt only |
| G4 Appearance | **PASS** | table above; max 0.0073% against a 4%/2% budget |
| G5 Draw submeshes | **PASS** | 121 → 9 |
| G6 Size | **PASS with note** | raw −52.1%, short of the 60% aspiration; census shows the remainder is all visible-surface geometry and the 19 KB spent on 6b is a deliberate quality choice |
| G7 GPU budget | **N/A** | `ALLOW_BAKE: no` |
| G8 Hygiene | **PASS** | re-import object count 9, no foreign geometry; scripts deterministic (Phase B re-run reproduced identical stats); `mid.glb` and `.blend1` removed |

## Shipping swap

`181-south-park.optimized.glb` copied over `artifacts/181-south-park/181-south-park.glb`.
The pre-optimize original is archived byte-for-byte at
`optimize/input/181-south-park.glb`. The asset's stage-2 validator was re-run
against the shipped file and returns **PASS** on all 16 checks, now reporting
9 objects instead of 121; `../validation.json` and `../REPORT.md` carry the
shipped numbers.
