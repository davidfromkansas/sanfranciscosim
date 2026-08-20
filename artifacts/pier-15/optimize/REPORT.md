# Pier 15 — stage 4 optimize report

`GLB-OPTIMIZE-PROMPT.md` v2 run against `artifacts/pier-15/`.
`ASSET_CLASS: landmark` · `ALLOW_MESHOPT: yes` · `ALLOW_BAKE: no`.

## Headline

| | input | shipped | delta |
|---|---|---|---|
| File, raw | 727,752 B | **350,496 B** | **−51.8%** (rebuilt asset, review 3) |
| File, gzip | 137,619 B | 231,350 B | +68% (same meshopt-vs-gzip trade documented on pier-3 §6) |
| Draw submeshes (primitives) | 315 | **12** | −96.2% |
| Objects / nodes | 315 | 12 | −96.2% |
| Triangles | 10,852 | 10,852 | 0 |
| Verts (welded) | 22,192 | 6,044 | −72.8% |
| Materials | 12 | 12 | identical set |

**All gates pass.** The optimized file is now `artifacts/pier-15/pier-15.glb`;
the pre-optimize original is archived byte-for-byte at `optimize/input/pier-15.glb`.
The 500 KB on-disk budget was BLOWN by the raw build (728-750 KB across
reviews) and is now met with 30% headroom.

## Toolchain

Blender 5.2.0 LTS (fbe6228777e7) · gltfpack@0.24 via npx · three ^0.185 in
`g3check/` · python3 3.9 + Pillow · gzip (macOS).

## Phase A — census (`inspect.json`)

315 objects/primitives · 10,852 tris · 22,192 verts · POSITION+NORMAL only ·
no textures · 12 materials (3 glow). Dominant waste: node/accessor overhead
(315 single-material objects) and ~16k coincident vertex pairs. 0 degenerate
tris. The 115 piles / 12 lamps / bollards are repeated boxes — joining removes
the overhead, not the geometry.

## Phase B (`phaseb_stats.json`)

| Step | tris | verts |
|---|---|---|
| input | 10,852 | 22,192 |
| weld ≤ 1 mm + degenerate | 10,852 | **6,044** |
| interior faces (0 found) | 10,852 | 6,044 |
| limited dissolve | **SKIPPED** (prompt §3.3) | |
| join per material (12 groups) | 10,852 | 6,044 |

Dissolve skipped deliberately: this asset carries the same large coplanar ring
bands as pier-3 (deck slab/surface, fender curb ring, bulkhead cornice/parapet/
cap rings) whose coplanar annuli re-triangulate into invisible slivers that
fail the stage-2 validator only after packing (350-brannan incident).

## Phase C — pack, with control row

`npx gltfpack@0.24 -c -km -kn -noq` (repo standard; no quantization):

| Variant | raw | gzip |
|---|---|---|
| input (unpacked, rebuilt asset) | 727,752 | 137,619 |
| pack only (no Phase B, measured on review-2 asset) | 449,116 | 178,467 |
| **weld+join+pack (shipped)** | **350,496** | 231,350 |

Phase B earns its round-trip: ~−90 KB raw vs the pack-only control. Gzip regresses on both
packed variants (meshopt streams gzip worse than raw duplicated floats); raw
on-disk bytes are the budget metric and the CDN serves its own encoding.

## Gates

- **G1** materials identical (12, glow set intact) — PASS
- **G2** bbox identical to 4 dp; origin exact; 0 inverted solids; ray flips 0.0% — PASS
- **G3** Blender re-import + pinned-three g3check: 12 meshes, 10,852 tris, no decode errors — PASS
- **G4** A/B day+night × near+far + 4 elevations: means ≤ 0.66% (night glow layer),
  day ≤ 0.004%; diffs are isolated 1-2 px edge-AA sparkles, nothing structural — PASS
- **G5** submeshes 315 → 12 — PASS
- **G6** −51.8% raw — PASS
- **G8** deterministic re-run reproduces; no foreign geometry; no .blend1 — PASS

## Post-swap check

The stage-2 contract validator (`validate_pier_15.py`) re-run against the
SHIPPED packed GLB: **PASS** — 0 invalid/non-unit loop normals (the packed-file
sliver failure mode cannot occur here; dissolve was skipped).
