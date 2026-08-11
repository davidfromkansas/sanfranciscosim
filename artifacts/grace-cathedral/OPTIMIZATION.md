# Optimization pass — grace-cathedral

**Result: OPTIMIZED.** Executed per the owner's GLB shrink-pass spec
(ASSET_CLASS=landmark), working copy only — the original authoring GLB is
preserved in the durable asset library.

| Metric | Input | Shipped | Δ |
|---|---|---|---|
| File raw (bytes) | 790,520 | 549,388 | -30.5% |
| File gzip (bytes) | 122,421 | 111,857 | -8.6% |
| Triangles | 10,814 | 10,814 | +0 |
| Mesh objects | 550 | 1 | |
| Primitives (file-level draw calls) | 561 | 11 | |

The clean win of the batch: -30.5% raw AND -8.6% gzip. A/B mean pixel delta <= 0.086%.

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
