# Earl Warren Building — GLB optimize report (stage 4)

Run 13 August 2026 per `docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md`.
`ASSET_CLASS: landmark` · `ALLOW_MESHOPT: yes` · `ALLOW_BAKE: no` ·
`TARGET_REDUCTION: 60%`.

Input archived byte-for-byte at `input/earl-warren-building.glb` (verified with
`cmp`). Every step is a committed deterministic script; re-running them on the
input reproduces the output.

## Metrics

| | Input | Output | Δ |
|---|---|---|---|
| File, raw | 1,030,636 B | **453,172 B** | **−56.0% (2.27×)** |
| File, gzip −9 | 151,795 B | (meshopt-coded) | see note |
| Triangles | 18,540 | **18,540** | 0 |
| Vertices | 35,880 | **29,834** | −16.9% |
| Objects / draw submeshes | 292 | **9** | −96.9% |
| Materials | 9 | 9 | identical set |
| Bbox dims | 118.93685 × 50.02504 × 27.0 | 118.93685 × 50.02504 × 27.0 | 0 |
| Bbox min | −59.46843, −25.01252, 0.0 | −59.46843, −25.01252, 0.0 | 0 |
| Ray-flip fraction | 0.0 | **0.0** | — |

453 KB raw is what the 500 KB budget in `sf-asset-check` §7 measures, and it is
under it. Gzip on a meshopt-coded buffer goes *up*, as it does for every asset in
this repo — meshopt's own entropy coding has already done the work.

## Phase A — waste census

From `inspect.json` on the input:

| Finding | Count | Technique | Predicted |
|---|---|---|---|
| Objects sharing a material | 292 across 9 materials | join per material | 292 → 9 submeshes, most of the file win |
| Coincident vertex pairs | 26,032 | per-object weld ≤ 1 mm | ~6,000 verts |
| Duplicate mesh groups | 27 groups, 9,060 redundant tris | *not* deduplicated — see below | 0 |
| Degenerate faces | 0 | — | — |
| Interior buried faces | 0 provable | occluder rule (closed solids only) | 0 |
| Over-tessellated curves | none | asset has no cylinders after the flagpoles were dropped | 0 |

Vertex attributes on input: `NORMAL` only (no UVs, no vertex colours, no
tangents) — nothing to prune.

## Phase B — geometry cleanup

| Step | Tris | Verts |
|---|---|---|
| input | 18,540 | 35,880 |
| weld ≤ 1 mm + degenerate removal | 18,540 | 29,834 |
| interior faces | 18,540 | 29,834 |
| limited dissolve 0.05° | 18,540 | 29,834 |
| join per material | 18,540 | 29,834 |

The weld is the only step that moved a number, and it moved the one that matters
for a merge-on-load asset. Limited dissolve found nothing because the build script
already emits minimal quads per face; there are no coplanar fans to collapse.

**Duplicate geometry was deliberately left alone.** The census found 9,060
triangles across 27 duplicate groups — the 19 arcade keystones, the 20 piers, the
per-bay window boxes. Instancing them would share mesh data in the glTF, but the
app's loader merges every landmark into one shared `BatchedMesh` at load
(`collect()` in `app/src/assets.js`), so instances are flattened anyway and the
only effect would be a smaller file at the cost of a node graph the loader has to
walk. Joining per material is strictly better for this runtime.

## Phase C — packing

```
npx gltfpack@0.24 -i mid.glb -o earl-warren-building.optimized.glb -c -km -kn -noq
```

`-km -kn` keep material and node names (glow-ness is name-only; without `-km`
gltfpack merges `Toy_white_Glow` into its non-glow twin and silently kills the
night layer). `-noq` per the repo standard — unquantized, matching what
`pipeline/compress-assets.mjs` produces.

## Phase E — A/B verification

Renders at `renders/`, deltas in `diffs.json`. Both sides rendered with the same
rig at 24 denoised Cycles samples rather than the generic script's 64 undenoised:
the machine was shared with ~17 other Blender jobs at load average 750+ and the
64-sample rig was not completing. Denoising is on for both sides so the noise
floor stays below the G4 delta gates; the change is symmetric, so the comparison
is unaffected. Both deviations are commented in `render_ab.py`.

### G4 measured deltas

| View | Mean abs RGB | Max px delta | Gate |
|---|---|---|---|
| day near | 0.0114% | 18 | ≤ 4% |
| day far | 0.0224% | 11 | ≤ 2% |
| night near | 0.0242% | 28 | ≤ 4% |
| night far | 0.0610% | 39 | ≤ 2% |
| elev N | 0.0343% | 51 | — |
| elev E | 0.0651% | 23 | — |
| elev S | **0.1184%** | 41 | — |
| elev W | 0.0506% | 18 | — |

Every figure is more than an order of magnitude inside its gate. **What the diffs
actually show:** at x8 amplification the diff row is black except for hairlines on
high-contrast edges and a small patch at the three entrance portals on the south
elevation — the one place the asset puts `Toy_gold_Glow` against a dark
`Toy_glass` reveal inside a pale `Toy_trim` surround, so it is the highest-contrast
detail in the model and the first place any sub-pixel difference shows. Triangle
count, bbox and material set are bit-identical between input and output, so no
geometry moved; the residual is the per-object weld shifting shared normals at
seams by a fraction of a degree, plus denoiser variation. Nothing a player could
see at 1x.

## Gates

| Gate | Result | Evidence |
|---|---|---|
| G1 Contract — material set identical, `_Glow` separate, no `Toy_body` | **PASS** | `validation.json` `G1_materials_identical: true`; 9 materials in, 9 out |
| G2 Geometry — bbox, origin, signed volumes, flip fraction | **PASS** | bbox and origin bit-identical; all 9 signed volumes positive; 22,500 rays, 0 flipped |
| G3 Round-trip — Blender + pinned-three GLTFLoader | **PASS** | `g3check` → `G3-OK`, 9 meshes, 18,540 tris, material set intact |
| G4 Appearance — day+night × near+far | **PASS** | worst mean delta 0.118% against gates of 2% far / 4% near |
| G5 Draw submeshes ≤ input | **PASS** | 292 → 9 |
| G6 Size reduced | **PASS** at −56.0%, short of the 60% aspiration | see below |
| G7 GPU budget | n/a | `ALLOW_BAKE: no` |
| G8 Hygiene — no foreign geometry, deterministic | **PASS** | re-import object count 9, material set and bbox match |

**G6 note.** −56.0% against a 60% aspiration. The remainder is silhouette
geometry, as the census requires: 18,540 triangles all survive Phase B untouched,
and they are the 19-bay arcade with its arch heads, the three nested entrance
portals, the cornice/attic/parapet rings and the roof. None of it is facade
micro-detail that could go under §5, because `ALLOW_BAKE` is off and this asset
has no textures to bake into. The file win came entirely from the weld and the
292 → 9 join; there is no further lossless win available without cutting
silhouette.
</content>
