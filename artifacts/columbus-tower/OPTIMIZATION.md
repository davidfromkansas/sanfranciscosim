# Optimization pass — columbus-tower

**Result: NO-OP (original ships).** Executed per the owner's GLB shrink-pass spec
(ASSET_CLASS=landmark), working copy only — the original authoring GLB is
preserved in the durable asset library.

| Metric | Input | Shipped | Δ |
|---|---|---|---|
| File raw (bytes) | 580,948 | 580,948 | +0.0% |
| File gzip (bytes) | 82,835 | 82,835 | +0.0% |
| Triangles | 9,360 | 9,360 | +0 |
| Mesh objects | 306 | 306 | |
| Primitives (file-level draw calls) | — | — | |

Every variant regressed the CDN wire size (join +23% gzip, join+pack +9.5% gzip) because the 306 small repeated elements (dome rings, window boxes) compress across objects extremely well as exported. Raw-size wins did not justify a wire regression; per the rollback rule the original ships unchanged.

Pipeline (deterministic scripts in ~/sf-3d-assets/optimized/_tools, run per
GLB-OPTIMIZE-PROMPT v1, ASSET_CLASS=landmark): Phase B - weld <=1mm within
objects, dissolve degenerate faces, join objects into one mesh per asset
(glow-named objects kept separate where the asset validator pins the night
contract to object names); Phase C - gltfpack 0.24 `-kn -km -noq` (lossless
repack; `-km` after catching gltfpack merging identically-colored glow/
non-glow materials). Quantization and EXT_meshopt_compression deliberately
OFF: the app registers no MeshoptDecoder, and dequantization node transforms
would violate the repo's applied-transforms contract. ALLOW_BAKE=no.
Gates: material set identical, bbox identical, transforms identity, signed
volumes positive, day+night A/B renders at 1.5x/6x long-axis 42-deg camera.
Toolchain: Blender 5.2.0 LTS, gltfpack 0.24, Pillow 11.3.0.

All acceptance gates passed on the shipped file: material name set identical
(every `_Glow` intact), bbox and origin identical, transforms at identity,
0 new flipped rays, and the asset's own fresh-scene validator returns PASS
on exactly the GLB in this folder. `validation.json` here is regenerated
against the shipped GLB and is the machine authority for its metrics.
