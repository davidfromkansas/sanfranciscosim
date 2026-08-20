# pier-7 — GLB optimize report (stage 4)

Input: `optimize/input/pier-7.glb` (the stage-2 export, archived byte-for-byte).
Output: `pier-7.optimized.glb`, swapped to `artifacts/pier-7/pier-7.glb` as the
shipping file after all gates passed. `ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`,
`ALLOW_BAKE: no`.

## Result

| Metric | Input | Output | Δ |
|---|---|---|---|
| Raw bytes | 957,804 | **349,512** | −63.5% |
| Gzip −9 bytes | 150,206 | **168,174** | +12% (meshopt streams gzip worse; raw is what ships and the CDN serves it 2.7× smaller) |
| Triangles | 13,860 | 13,860 | 0 |
| Vertices | 8,008 | 8,008 | 0 |
| Objects / draw submeshes | 540 | **7** (one per material) | −533 |
| Materials | 7 (`Toy_amber_Glow` separate) | 7, identical set | — |

## Phases

- **Phase B**: weld ≤1 mm per object (0 tris removed — the build emits clean
  geometry); degenerate/interior-face pass (0 removed; piles meet the soffit
  face-on, nothing is buried); **limited dissolve SKIPPED** — the asset is made
  of coplanar ring bands (bullrail ring, two railing tubes on the 49-vertex
  footprint), the exact `350-brannan` sliver trap from GLB-OPTIMIZE-PROMPT §3.3;
  join per material 540 → 7 objects (the whole win).
- **Phase C**: `npx gltfpack@0.24 -c -km -kn -noq` (repo standard; no
  quantization).
- **Phase D**: not run (`ALLOW_BAKE: no`).

## Gates

| Gate | Result |
|---|---|
| G1 contract | PASS — material set identical, `_Glow` separate, no manifest node names on this asset |
| G2 geometry | PASS — dims 219.5688 × 165.9949 × 7.6 m unchanged; origin 0; signed volumes all positive; ray flipped fraction 0.0; invalid loop normals 0 (stage-2 validator re-run **on the packed file**: `optimize/validation.json`, overall PASS) |
| G3 round-trip | PASS — Blender re-import + `g3check` (pinned three): 7 meshes, 13,860 tris, no decode errors |
| G4 appearance | PASS — day/night × near/far + 4 elevations: worst mean abs RGB delta **0.25%** (night near; gate 4%), max px delta 16/255; diffs are sampler noise on the glow globes, nothing a player could notice (`renders/`, `diffs.json`) |
| G5 submeshes | PASS — 7 ≤ 540 |
| G6 size | PASS — 63.5% ≥ 60% target |
| G7 GPU | n/a (no bake) |
| G8 hygiene | PASS — deterministic scripts committed here; re-import contains only the asset; no `.blend1` |

Toolchain: Blender 5.2.0 LTS, gltfpack 0.24 (npx, pinned), three via
`tools/glb-optimize/g3check` (pinned), Python 3.9 + Pillow.

`artifacts/pier-7/validation.json` and REPORT.md updated to shipped numbers.
