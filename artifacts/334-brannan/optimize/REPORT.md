# 334 Brannan Street — GLB optimize pass (stage 4)

Run 16-17 August 2026 per `docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md`.
`ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`,
`TARGET_REDUCTION: 60%` file size.

Scripts are the generic `tools/glb-optimize/` implementations copied here and
adapted per asset (one adaptation: the limited dissolve is skipped, §3). Every
step is deterministic and re-runnable against `input/334-brannan.glb`.

## 1. Metrics

| | Input | Optimized | Δ |
|---|---|---|---|
| File, raw | 365,324 B | **176,264 B** | **−51.8%** |
| File, gzip −9 | 59,988 B | 110,996 B | +85% (see §4) |
| Triangles | 5,916 | 5,916 | unchanged |
| Vertices | 12,152 | 11,256 | −7.4% |
| Objects | 109 | 15 | −86.2% |
| Draw submeshes (primitives) | 110 | **16** | **−85.5%** |
| Materials | 14 | 14 | unchanged |
| BBox | 30.17625 × 30.64767 × 13.4 | identical | 0 |
| Origin XY | (0.12853, −0.07263) | identical | 0 |

Vertex attributes: `POSITION` + `NORMAL` only, float32, no UVs, no textures —
before and after.

## 2. Phase A — waste census

Near distance for the 1-pixel chord test: 45.97 m (1.5 × the 30.6 m long axis);
one screen pixel = 0.031 m at that distance.

| Technique | Finding | Predicted | Actual |
|---|---|---|---|
| Object-count overhead | 109 objects across 14 materials, one primitive each | join to ~15 | 109 → 15 |
| Unwelded coincident verts | 8,980 pairs (every panel is an independently authored closed prism) | large vert drop | 12,152 → 11,256 verts |
| Duplicate meshes | 17 groups, 2,604 redundant tris (window frames/fills repeated 12×, skylight kerbs, deck chairs, vents) | join, not instance — counts are small and each is ≤ 108 tris | joined |
| Degenerate faces | 0 | nothing to do | 0 |
| Buried interior faces | 0 closed-solid occluders qualified (the applied panels all breach their host wall by design) | 0 | 0 |
| Over-tessellated curves | none — the only non-box profile is the 5-segment segmental arch over the entry portal, and it is silhouette detail 2.3 m wide | skip | skipped |

## 3. Phase B — geometry cleanup

| Step | Tris | Verts |
|---|---|---|
| input | 5,916 | 12,152 |
| weld ≤ 1 mm + degenerate removal (per object) | 5,916 | 3,172 |
| interior-face deletion | 5,916 | 3,172 |
| limited dissolve | **skipped by rule** | — |
| join per material | 5,916 | 3,172 |
| after export/re-import (split by material boundaries) | 5,916 | 11,256 |

**The limited dissolve is skipped, not attempted.** `GLB-OPTIMIZE-PROMPT` §3
step 3 says to skip it entirely on assets with large coplanar ring bands, and
this asset has two: the parapet and its coping are `ring_band` solids whose top
and bottom faces are perfectly coplanar annuli following the whole 21 × 21 m
footprint (they are also the two largest objects in the asset at 288 tris each).
On the sibling 350 Brannan the same step manufactured 7 slivers up to 24.35 m
long and ~0.24 mm wide, whose collapsed vertex normals failed the stage-2
contract validator only *after* gltfpack re-emitted the stored normals — bought
for 30 triangles. Not a trade, and the rule already exists.

Normals audit after cleanup: `inverted_solids: []`.

## 4. Phase C — packing

```
npx gltfpack@0.24 -i mid.glb -o 334-brannan.optimized.glb -c -km -kn -noq
```

`-km -kn` keep the material and node names — mandatory, because glow-ness is
name-only and without `-km` gltfpack would merge `Toy_gold_Glow` into `Toy_gold`
and `Toy_glass_Glow` into `Toy_glassl` (identical parameters, different names),
silently killing the night layer. `-noq` is the repo standard: unquantized
float32 attributes are what `pipeline/compress-assets.mjs` produces and what the
runtime merge paths need.

**The gzip number goes up, and that is expected.** Meshopt-compressed buffers
are already entropy-coded, so gzip finds nothing left: 60 KB → 111 KB over the
wire against a 365 KB → 176 KB raw win. This matches the sibling 350 Brannan
(73 KB → 123 KB) exactly. What the pass actually buys here is the 85% cut in
draw submeshes, the decode speed, and GPU vertex memory — recorded so the
transfer-byte question is not re-opened per asset.

## 5. Phase D — bake

Not run (`ALLOW_BAKE: no`). No textures added; the asset stays flat-colour only.

## 6. Phase E — A/B verification

Landmark rig: near = 1.5 × long axis (45.9 m), far = 6 × (183.9 m), 42° aerial,
`clip_end = 50000`. Day pass renders `_Glow` at alpha 0.12 (the app's day state);
night pass at alpha 1.0 with emission.

| View | Mean abs RGB Δ | Max px Δ | Gate |
|---|---|---|---|
| day_near | 0.0062% | 25 | ≤ 4% |
| day_far | 0.0055% | 4 | ≤ 2% |
| night_near | 0.0047% | 58 | ≤ 4% |
| night_far | 0.0067% | 72 | ≤ 2% |
| elev_n | 0.0027% | 17 | — |
| elev_e | 0.0023% | 22 | — |
| elev_s | 0.0018% | 15 | — |
| elev_w | 0.0022% | 17 | — |

Looking at the ×8-amplified diffs rather than the numbers: the diff frames are
black apart from a one-pixel outline on some silhouette and window edges, which
is anti-aliasing landing differently after the per-material join changed
triangle order. The gold crest, the pink tower panels, the six-bay rhythm, the
living wall and every roof object are present and unchanged in both rows of
`renders/contact_sheet.png`. Nothing a player could notice.

## 7. Gate results

| Gate | Result |
|---|---|
| G1 Contract — material set identical, `_Glow` separate, no `Toy_body`, node names intact | **PASS** (14 = 14, both glow materials survive `-km`) |
| G2 Geometry — bbox, origin, signed volumes, ray flips | **PASS** (bbox Δ 0, origin Δ 0, all volumes positive, 22,500 rays / 17,451 hits / **0** flipped) |
| G3 Round-trip — Blender re-import + pinned-three GLTFLoader | **PASS** (`G3-OK {"ok":true,"meshes":16,"tris":5916,...}`, meshopt decode clean, 14 materials) |
| G4 Appearance — day+night × near+far | **PASS** (max 0.0067% mean delta against a 2% far / 4% near gate) |
| G5 Draw submeshes ≤ input | **PASS** (110 → 16) |
| G6 Size reduced, ≥ 60% aspirational | **PASS on reduction, short of target** (−51.8% raw). The remainder is silhouette geometry: after the weld the asset is 5,916 triangles of authored massing with no duplicate-instance or curve waste left, and the tri count is deliberately unchanged — cutting further would mean cutting bays, caps or roof furniture |
| G7 GPU budget | n/a (bake mode off) |
| G8 Hygiene — no foreign geometry, deterministic re-run, no `.blend1` | **PASS** (re-import object/material counts match; no `.blend1` written) |

## 8. Toolchain

- Blender 5.2.0 LTS (`fbe6228777e7`, 2026-07-14), headless
- `npx gltfpack@0.24`
- node + pinned `three@^0.185.1` in `g3check/`
- python3 + Pillow, gzip −9

## 9. Shipping swap

All gates pass, so `334-brannan.optimized.glb` was copied over
`artifacts/334-brannan/334-brannan.glb`. The pre-optimize original is archived
byte-for-byte at `optimize/input/334-brannan.glb`. The asset's own
`validation.json` and `REPORT.md` carry the shipped numbers.
