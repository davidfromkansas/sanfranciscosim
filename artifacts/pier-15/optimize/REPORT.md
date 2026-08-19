# Pier 15 — stage 4 optimize report

`GLB-OPTIMIZE-PROMPT.md` v2 run against `artifacts/pier-15/`.
`ASSET_CLASS: landmark` · `ALLOW_MESHOPT: yes` · `ALLOW_BAKE: no`.

## Headline

| | input | shipped | delta |
|---|---|---|---|
| File, raw | 749,952 B | **360,516 B** | **−51.9%** |
| File, gzip | 139,907 B | 238,145 B | +70% (same meshopt-vs-gzip trade documented on pier-3 §6) |
| Draw submeshes (primitives) | 324 | **12** | −96.3% |
| Objects / nodes | 324 | 12 | −96.3% |
| Triangles | 11,152 | 11,152 | 0 |
| Verts (welded) | 22,856 | 6,212 | −72.8% |
| Materials | 12 | 12 | identical set |

**All gates pass.** The optimized file is now `artifacts/pier-15/pier-15.glb`;
the pre-optimize original is archived byte-for-byte at `optimize/input/pier-15.glb`.
The 500 KB on-disk budget was BLOWN by the raw build (750 KB) and is now met
with 28% headroom.

## Toolchain

Blender 5.2.0 LTS (fbe6228777e7) · gltfpack@0.24 via npx · three ^0.185 in
`g3check/` · python3 3.9 + Pillow · gzip (macOS).

## Phase A — census (`inspect.json`)

324 objects/primitives · 11,152 tris · 22,856 verts · POSITION+NORMAL only ·
no textures · 12 materials (3 glow). Dominant waste: node/accessor overhead
(324 single-material objects) and 16,644 coincident vertex pairs. 0 degenerate
tris. The 115 piles / 12 lamps / bollards are repeated boxes — joining removes
the overhead, not the geometry.

## Phase B (`phaseb_stats.json`)

| Step | tris | verts |
|---|---|---|
| input | 11,152 | 22,856 |
| weld ≤ 1 mm + degenerate | 11,152 | **6,212** |
| interior faces (0 found) | 11,152 | 6,212 |
| limited dissolve | **SKIPPED** (prompt §3.3) | |
| join per material (12 groups) | 11,152 | 6,212 |

Dissolve skipped deliberately: this asset carries the same large coplanar ring
bands as pier-3 (deck slab/surface, fender curb ring, bulkhead cornice/parapet/
cap rings) whose coplanar annuli re-triangulate into invisible slivers that
fail the stage-2 validator only after packing (350-brannan incident).

## Phase C — pack, with control row

`npx gltfpack@0.24 -c -km -kn -noq` (repo standard; no quantization):

| Variant | raw | gzip |
|---|---|---|
| input (unpacked) | 749,952 | 139,907 |
| pack only (no Phase B) | 449,116 | 178,467 |
| **weld+join+pack (shipped)** | **360,516** | 238,145 |

Phase B earns its round-trip: −88.6 KB raw vs pack-only. Gzip regresses on both
packed variants (meshopt streams gzip worse than raw duplicated floats); raw
on-disk bytes are the budget metric and the CDN serves its own encoding.

## Gates

- **G1** materials identical (12, glow set intact) — PASS
- **G2** bbox identical to 4 dp; origin exact; 0 inverted solids; ray flips 0.0% — PASS
- **G3** Blender re-import + pinned-three g3check: 12 meshes, 11,152 tris, no decode errors — PASS
- **G4** A/B day+night × near+far + 4 elevations: means ≤ 0.76% (night glow layer),
  day ≤ 0.004%; diffs are isolated 1-2 px edge-AA sparkles, nothing structural — PASS
- **G5** submeshes 324 → 12 — PASS
- **G6** −51.9% raw — PASS
- **G8** deterministic re-run reproduces; no foreign geometry; no .blend1 — PASS

## Post-swap check

The stage-2 contract validator (`validate_pier_15.py`) re-run against the
SHIPPED packed GLB: **PASS** — 0 invalid/non-unit loop normals (the packed-file
sliver failure mode cannot occur here; dissolve was skipped).
