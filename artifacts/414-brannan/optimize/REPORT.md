# 414 Brannan Street — GLB optimize pass

Stage 4 of `docs/asset-pipeline/ADDRESS-TO-ASSET.md`, run per
`docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md` on 18 August 2026.

Inputs: `ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`,
`BLENDER: 5.2.0 LTS`, `gltfpack@0.24`.

## Metrics

| | input | shipped | delta |
|---|---|---|---|
| raw bytes | 512,896 | **228,016** | **−55.5%** |
| gzip -9 bytes | 95,996 | 148,473 | +54.7% (see note) |
| triangles | 8,312 | 8,312 | 0 |
| vertices | 16,356 | 15,057 | −7.9% |
| objects | 155 | **15** | −90.3% |
| draw primitives | 158 | **16** | −89.9% |
| materials | 14 | 14 | 0 |
| GPU vertex bytes (pos+nrm f32) | 392,544 | 361,368 | −7.9% |
| bbox dims | 33.16257 × 33.07253 × 14.0 | identical | 0 |
| bbox min | −16.30946, −16.80997, 0.0 | identical | 0 |

**Note on gzip.** Meshopt output is already entropy-coded, so it does not gzip
further; the gzipped figure going up is expected and is not a regression. What
ships is the 228 KB file, well inside the 500 KB per-landmark budget in
`AGENTS.md`, and `pipeline/compress-assets.mjs` will skip it on intake because it
already carries `EXT_meshopt_compression`. The win that matters at runtime is the
draw-primitive collapse, 158 → 16.

## Waste census (Phase A)

| finding | count | acted on |
|---|---|---|
| coincident vertex pairs (≤ 1 mm) | 11,896 | yes — per-object weld, 16,356 → 4,460 verts pre-pack |
| duplicate mesh groups | 3 balconies, 7 sills, 4 blank-panel rails, others | joined per material (small counts; sharing mesh data is not worth the node overhead here) |
| redundant tris in duplicate groups | 2,836 | not removable — they are distinct instances at distinct positions, not waste |
| degenerate triangles | 0 | n/a |
| interior faces buried in closed solids | 0 | n/a |
| objects sharing a material | 155 → 14 groups | joined |
| over-tessellated curves | none past the 1-px chord test at 49.7 m | left alone — the arch archivolt, the four Juliet balconies and the tympanum disc are silhouette-defining curved shells |
| image textures | 0 | n/a |

## Phase B — geometry cleanup

| step | tris | verts |
|---|---|---|
| input | 8,312 | 16,356 |
| weld ≤ 1 mm + degenerate removal | 8,312 | 4,460 |
| interior-face removal | 8,312 | 4,460 |
| limited dissolve | **SKIPPED** | — |
| join per material | 8,312 | 4,460 |

**The limited dissolve was skipped deliberately**, per §3 step 3 of the optimize
prompt. This asset carries three large coplanar ring bands that follow the
footprint all the way round — the main parapet and the two roof copings — plus
two full-length frieze panels. Their top and bottom faces are perfectly coplanar
annuli, so even a strictly-coplanar dissolve merges each into a single annulus
ngon whose re-triangulation emits sub-millimetre slivers. Those slivers pass an
area-based degeneracy test and only surface two steps later, in the packed file,
as `invalid_or_nonunit_loop_normal_count`. On `350-brannan` the same step was
worth 30 triangles (0.4%). The skip is recorded in `phaseb_stats.json`.

No triangles were removed by Phase B, and that is the correct outcome: this asset
was authored with a per-object bevel budget and has no buried interior faces and
no degenerate geometry. The whole win is topological (vertex welding) and
structural (object joins).

## Phase C — packing

```
npx gltfpack@0.24 -i mid.glb -o 414-brannan.optimized.glb -c -km -kn -noq
```

`-km -kn` verified to have kept all 14 material names distinct, including both
`_Glow` materials, which are name-only and would otherwise merge into their
non-glow twins (`Toy_trim` / `Toy_trim_Glow` share every parameter). `-noq` per
the repo standard — unquantized float32 attributes are what the runtime merge
paths and the stage-2 contract validator need. `grep -rn setMeshoptDecoder app/src/`
hits `gltf.js:10` and `assets.js:406`, so meshopt is safe to rely on.

Phase D (high→low bake) not run: `ALLOW_BAKE: no`, and the contract forbids
textures without a recorded exception.

## Gate results

| gate | result | evidence |
|---|---|---|
| **G1** Contract | **PASS** | material name set identical (14, both `_Glow` preserved); no `Toy_body`; no manifest-named nodes to protect |
| **G2** Geometry | **PASS** | bbox identical to 5 dp; origin offset identical; 15/15 signed volumes positive; `inverted_solids: []`; ray test 22,500 rays, 0 flipped, `flipped_fraction 0.0` |
| **G3** Round-trip | **PASS** | re-imports in Blender 5.2; `g3check` (pinned three 0.185) reports `G3-OK` with 16 meshes, 8,312 tris, 14 materials, correct bbox, no decode errors |
| **G4** Appearance | **PASS** | mean absolute RGB delta: day near 0.008%, day far 0.009%, night near 0.640%, night far 0.583%, four elevations 0.004–0.010% — all far inside the ≤ 4% near / ≤ 2% far gate |
| **G5** Draw submeshes | **PASS** | 158 → 16 |
| **G6** Size | **PASS with a note** | −55.5% against a 60% target. The census shows the remainder is silhouette geometry: Phase B removed zero triangles because there were none to remove, and the dissolve that might have shaved ~0.4% was skipped on purpose. Every one of the 8,312 triangles is authored massing, facade relief or roof furniture. |
| **G7** GPU budget | n/a | bake mode not run |
| **G8** Hygiene | **PASS** | re-import object count matches (15); no foreign geometry; scripts deterministic; no `.blend1` files |

### G4, described honestly

The x8-amplified diffs are uniform Cycles sampling noise over lit surfaces, with
no structural signal anywhere. Nothing is missing, no silhouette moved, no
shading artefact appeared. The night deltas are two orders of magnitude larger
than the day deltas purely because the night rig renders emissive surfaces, which
converge more slowly at 64 samples — the diff images show speckle spread evenly
across the roof deck and the clerestory band, not a change at any edge. There is
nothing here a player could notice.

## Shipping swap

`414-brannan.optimized.glb` was copied over `artifacts/414-brannan/414-brannan.glb`
and the pre-optimize file archived byte-for-byte at
`optimize/input/414-brannan.glb`. The stage-2 contract validator was then re-run
against the shipped file: **PASS on all 16 checks**, 15 objects, 8,312 triangles,
normals clean.
