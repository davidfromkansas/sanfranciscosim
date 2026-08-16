# 188 South Park — optimize report

## Metrics

| Metric | Input | Phase B (mid) | Output (optimized) | Δ |
|---|---|---|---|---|
| Raw bytes | 276,164 | 220,372 | **119,312** | **−56.8%** |
| Gzip bytes | 43,250 | — | — | — |
| Objects | 129 | 9 | 9 | −93% |
| Triangles | 3,864 | 3,864 | 3,864 | 0% |
| Vertices | 8,040 | 2,184 | 2,184 | −72.9% |
| Primitives (draw submeshes) | 129 | 9 | 9 | −93% |
| Materials | 9 | 9 | 9 | 0% |

## Phase A — Forensic inspection

- 129 objects, 3,864 triangles, 8,040 vertices
- 9 materials (all `Toy_*`, 2 glow groups)
- No textures, no UV layers, no color attributes
- No duplicate mesh groups
- No degenerate triangles
- 5,856 coincident vert pairs (welded in Phase B)
- Join candidates: all 9 materials have multiple user objects

## Phase B — Geometry cleanup

1. **Weld + degenerate:** 8,040 → 2,184 verts (−72.9%). No tris change. The
   build script's `bmesh.ops.remove_doubles` during bevel left many coincident
   verts that the per-object weld cleaned up.
2. **Interior faces:** 0 removed. The asset has no buried interior faces — the
   build script's closed-solid prisms and face panels are all externally visible.
3. **Limited dissolve: SKIPPED.** The asset has ring bands (parapet, floor_band,
   pent_railing) whose coplanar annuli would merge into sliver ngons on
   re-triangulation. Per GLB-OPTIMIZE-PROMPT §3 step 3, this step is skipped
   when ring bands are present. The ~30-tri savings (0.4%) are not worth the
   risk of manufacturing sliver geometry that passes area-based degeneracy
   tests but fails the stage-2 contract validator's normal check.
4. **Join per material:** 129 objects → 9 (one per material). This is the
   single biggest win: node/accessor overhead + draw submeshes reduced by 93%.
5. **Normals audit:** 0 inverted solids. All 9 joined objects have positive
   signed volume.

## Phase C — Packing pass

```
npx gltfpack@0.24 -i mid.glb -o 188-south-park.optimized.glb -c -km -kn -noq
```

- `-c`: meshopt compression
- `-km`: keep materials separate (mandatory — glow boundary)
- `-kn`: keep nodes
- `-noq`: no quantization (repo standard — keeps float32 attributes for merge paths)

Result: 220,372 → 119,312 bytes (−45.9% from Phase B, −56.8% from input).

## Phase E — A/B verification

| View | Mean RGB delta | Max px delta | Gate (≤2% far / ≤4% near) |
|---|---|---|---|
| day_near | 0.0034% | 29 | PASS |
| day_far | 0.0041% | 6 | PASS |
| night_near | 0.0009% | 8 | PASS |
| night_far | 0.0019% | 10 | PASS |
| elev_n | 0.0046% | 48 | PASS |
| elev_e | 0.0023% | 35 | PASS |
| elev_s | 0.0026% | 19 | PASS |
| elev_w | 0.0042% | 39 | PASS |

All deltas are well under the 2% far / 4% near thresholds. The optimized asset
is visually identical to the input.

## Gate results

| Gate | Result |
|---|---|
| G1 Contract (materials identical, glow separate) | PASS |
| G2 Geometry (bbox, origin, volumes, ray) | PASS (0 flipped / 16,668 hits) |
| G3 Round-trip (Blender re-import + g3check) | PASS (9 meshes, 3,864 tris, all materials) |
| G4 Appearance (day+night × near+far) | PASS (all deltas < 0.005%) |
| G5 Draw submeshes (≤ input) | PASS (9 ≤ 129) |
| G6 Size (reduced) | PASS (276 KB → 119 KB, −56.8%) |
| G8 Hygiene (no foreign geometry, deterministic) | PASS |

## Shipping swap

`188-south-park.optimized.glb` copied over `188-south-park.glb` (the shipping
file). Pre-optimize original archived at `optimize/input/188-south-park.glb`.

## Toolchain

- Blender 5.2.0 LTS (headless)
- gltfpack 0.24 (npx)
- g3check: pinned three.js r170
- Python 3 + Pillow
