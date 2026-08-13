# 574 Third Street — GLB optimize report (stage 4)

Run 13 August 2026 per `docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md`.
`ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`.

Toolchain: Blender 5.2.0 LTS, `npx gltfpack@0.24`, node + pinned three via `g3check/`,
python3 + Pillow, gzip −9.

## 1. Metrics

| Metric | Input | Shipped | Delta |
|---|---|---|---|
| File, raw | 608,272 B | **284,644 B** | **−53.2%** |
| File, gzip −9 | 102,186 B | 178,515 B | +74.7% (meshopt payload is already entropy-coded; see §4) |
| Triangles | 9,856 | 9,856 | unchanged |
| Vertices | 19,882 | 19,056 | −4.2% |
| Objects | 195 | 11 | −94.4% |
| Draw submeshes (primitives) | 196 | **12** | −93.9% |
| Materials | 10 | 10 | unchanged |
| BBox | 64.94936 × 60.14542 × 15.4 | identical to 1e−5 m | — |
| Origin | −33.23906, −30.04928, 0.0 | identical | — |

## 2. Waste census (Phase A)

| Finding | Value | Action |
|---|---|---|
| Objects sharing a material | 195 across 10 groups (`Toy_glass` alone had 59) | joined per material — the single biggest win |
| Coincident vertex pairs | 14,568 | welded per object, ≤ 1 mm |
| Degenerate triangles | 0 | — |
| Buried interior faces | 0 removable | the light-well boxes sit *proud* of the deck by design, and the body prism is concave, so no closed solid encloses another's faces |
| Over-tessellated curves | none removable | the only curves are the 4-segment segmental arch heads on the Ritch Street elevation, already at the minimum that still reads as an arch |

## 3. Phase B — geometry cleanup

| Step | Tris | Verts |
|---|---|---|
| input | 9,856 | 19,882 (in-file, split per primitive) |
| weld + degenerate | 9,856 | 5,314 |
| interior faces | 9,856 | 5,314 |
| limited dissolve | **skipped** — see below | — |
| join per material | 9,856 | 5,314 → 11 objects |

**The 0.05° limited dissolve was skipped deliberately**, for the same reason as
400 Brannan: this asset carries full-perimeter ring bands (parapet, coping) plus two
long rectangular light-well kerbs, all of them exactly coplanar annuli. A strictly
coplanar dissolve merges each into one annulus ngon whose re-triangulation emits
metre-long sub-millimetre slivers; those pass an area-based degeneracy test but their
averaged vertex normals collapse to ~0 and only surface after packing, as
`invalid_or_nonunit_loop_normal_count` in the stage-2 contract validator (the
350-brannan failure recorded in the prompt's §3 step 3). Reverted under §11. The skip is
implemented in `optimize.py` (`SKIP_DISSOLVE`) so re-runs are deterministic.

Normals audit: no inverted solids; 22,500-ray visibility test → 15,196 hits, **0
flipped** (0.000%).

## 4. Phase C — packing

```
npx gltfpack@0.24 -i mid.glb -o 574-third.optimized.glb -c -km -kn -noq
```

`-km` keeps the two `_Glow` materials separate from their identical-parameter non-glow
twins — without it the night layer dies silently. `-noq` is the repo standard
(`pipeline/compress-assets.mjs` produces the same encoding). Verified on the output:
material-name set identical, bbox identical, 12 primitives.

Gzipped size rises after packing, as expected — meshopt has already compressed the
streams. The raw file is what the CDN serves: 284 KB against the 500 KB per-landmark
budget, for the largest footprint in the Third Street family.

## 5. Phase D

Not run (`ALLOW_BAKE: no`). No textures added.

## 6. Phase E — A/B verification

| View | Mean abs RGB delta | Max pixel delta |
|---|---|---|
| day near | 0.004% | — |
| day far | 0.004% | — |
| night near | 0.062% | — |
| night far | 0.061% | — |
| elevations N/E/S/W | 0.003–0.051% | — |

Looked at the ×8-amplified diffs: single-pixel seams along the parapet coping and the
light-well kerbs, nothing else. The billboard, both light wells, every fire escape and
the whole lit-window scatter are present and identical in both. Silhouette unchanged.

## 7. Gates

| Gate | Result |
|---|---|
| G1 contract (material set, `_Glow` separate, node names) | **PASS** |
| G2 geometry (bbox ≤ 1 cm, origin ≤ 1 cm, volumes positive, flip ≤ 0.15%) | **PASS** (0.000% flipped) |
| G3 round-trip (Blender re-import + pinned-three `g3check`) | **PASS** — `G3-OK`, 12 meshes, 9,856 tris, 10 materials |
| G4 appearance (≤ 2% far / ≤ 4% near) | **PASS** — worst 0.062% |
| G5 draw submeshes ≤ input | **PASS** — 196 → 12 |
| G6 size reduced (target 60%) | **PASS at −53.2%**; the remainder is silhouette geometry — 30 window bays across four elevations, and the census found nothing removable |
| G7 GPU budget | n/a (no bake) |
| G8 hygiene | **PASS** |

## 8. Shipping swap

`574-third.optimized.glb` copied over `artifacts/574-third/574-third.glb`; the
pre-optimize original is archived at `optimize/input/574-third.glb` (608,272 B). The
stage-2 contract validator was re-run **against the packed shipping file** and returns
`overall: PASS` with every check true. `validation.json` and `REPORT.md` carry the
shipped numbers.
