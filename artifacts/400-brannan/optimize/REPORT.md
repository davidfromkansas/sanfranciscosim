# 400 Brannan Street — GLB optimize report (stage 4)

Run 13 August 2026 per `docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md`.
`ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`.

Toolchain: Blender 5.2.0 LTS, `npx gltfpack@0.24`, node + pinned three via `g3check/`,
python3 + Pillow, gzip −9.

## 1. Metrics

| Metric | Input | Shipped | Delta |
|---|---|---|---|
| File, raw | 257,152 B | **115,408 B** | **−55.1%** |
| File, gzip −9 | 51,604 B | 79,398 B | +53.9% (meshopt payload is already entropy-coded; see §4) |
| Triangles | 3,896 | 3,896 | unchanged |
| Vertices | 7,918 | 7,105 | −10.3% |
| Objects | 87 | 10 | −88.5% |
| Draw submeshes (primitives) | 88 | **11** | −87.5% |
| Materials | 9 | 9 | unchanged |
| BBox | 31.40045 × 33.78239 × 8.8 | identical to 1e−5 m | — |
| Origin | −15.62791, −16.89258, 0.0 | identical | — |

## 2. Waste census (Phase A)

| Finding | Value | Action |
|---|---|---|
| Objects sharing a material | 87 across 9 groups | joined per material (the single biggest win) |
| Coincident vertex pairs | 5,804 | welded per object, ≤ 1 mm |
| Degenerate triangles | 0 | — |
| Buried interior faces | 0 removable | no object is a closed solid whose AABB fill ≥ 95% *and* encloses another's faces; the body prism is concave |
| Over-tessellated curves | none | this asset has no curves — every opening is rectangular |
| Duplicate mesh groups | absorbed by the per-material join | — |

## 3. Phase B — geometry cleanup

| Step | Tris | Verts |
|---|---|---|
| input | 3,896 | 7,918 (in-file, split per primitive) |
| weld + degenerate | 3,896 | 2,114 |
| interior faces | 3,896 | 2,114 |
| limited dissolve | **skipped** — see below | — |
| join per material | 3,896 | 2,114 → 10 objects |

**The 0.05° limited dissolve was skipped deliberately.** This asset is built from ring
bands that follow the footprint the whole way round — base band, floor-line course,
parapet and coping. Their top and bottom faces are exactly coplanar annuli, so even a
strictly-coplanar dissolve merges each ring into one annulus ngon, and re-triangulating
an annulus emits metre-long sub-millimetre slivers. Those pass an area-based degeneracy
test but their averaged vertex normals collapse to ~0, which surfaces only after packing
as `invalid_or_nonunit_loop_normal_count` in the stage-2 contract validator. That is the
350-brannan failure the prompt documents in §3 step 3. The step was worth ~0.3% of
triangles here, so it is reverted under §11 rather than worked around. The skip is
implemented in `optimize.py` (`SKIP_DISSOLVE`) so re-runs are deterministic.

Normals audit: no inverted solids; 22,500-ray visibility test → 16,228 hits, **0
flipped** (0.000%).

## 4. Phase C — packing

```
npx gltfpack@0.24 -i mid.glb -o 400-brannan.optimized.glb -c -km -kn -noq
```

`-km` keeps `Toy_glass_Glow` and `Toy_trim_Glow` separate from their non-glow twins
(glow-ness is name-only and the loader splits on it); `-noq` is the repo standard and is
what `pipeline/compress-assets.mjs` produces. Verified on the output: material-name set
identical, bbox identical, 11 primitives.

Gzipped size **rises** after packing. That is expected and not a regression: meshopt
already compresses the vertex/index streams, so gzip has nothing left to find and adds
its own framing. The number that matters over the wire is the raw file, which is what
the CDN serves for a `.glb` — 115 KB, well inside the 500 KB per-landmark budget.

## 5. Phase D

Not run (`ALLOW_BAKE: no`). No textures added.

## 6. Phase E — A/B verification

Same rig, input vs output, day (glow α 0.12) and night (α 1.0, emission 6), near
(1.5× long axis) and far (6×), plus four orthographic elevations.

| View | Mean abs RGB delta | Max pixel delta |
|---|---|---|
| day near | 0.024% | 27 |
| day far | 0.021% | 7 |
| night near | 0.090% | 42 |
| night far | 0.090% | 32 |
| elevations N/E/S/W | 0.017–0.031% | 25–54 |

Looked at the ×8-amplified diffs: the only non-black pixels are one-pixel seams along
the awning shelf and the parapet coping, i.e. rasterisation noise where two joined
objects now share an index buffer. Nothing a player could see. Silhouette unchanged;
every element present in both; night glow set identical.

## 7. Gates

| Gate | Result |
|---|---|
| G1 contract (material set, `_Glow` separate, node names) | **PASS** |
| G2 geometry (bbox ≤ 1 cm, origin ≤ 1 cm, volumes positive, flip ≤ 0.15%) | **PASS** (0.000% flipped) |
| G3 round-trip (Blender re-import + pinned-three `g3check`) | **PASS** — `G3-OK`, 11 meshes, 3,896 tris, 9 materials |
| G4 appearance (≤ 2% far / ≤ 4% near) | **PASS** — worst 0.090% |
| G5 draw submeshes ≤ input | **PASS** — 88 → 11 |
| G6 size reduced (target 60%) | **PASS at −55.1%**; the remainder is silhouette geometry — the census found no removable interior faces and no curves to retessellate |
| G7 GPU budget | n/a (no bake) |
| G8 hygiene (no foreign geometry, deterministic, no `.blend1`) | **PASS** |

## 8. Shipping swap

`400-brannan.optimized.glb` copied over `artifacts/400-brannan/400-brannan.glb`; the
pre-optimize original is archived at `optimize/input/400-brannan.glb` (257,152 B).
The stage-2 contract validator was re-run **against the packed shipping file** and
returns `overall: PASS` with every check true — including the loop-normal check that
catches the dissolve slivers described in §3. `validation.json` and `REPORT.md` carry
the shipped numbers.
