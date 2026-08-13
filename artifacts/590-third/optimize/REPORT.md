# 590 Third Street — GLB optimize report (stage 4)

Run 13 August 2026 per `docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md` v2.
`ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`.

**Toolchain:** Blender 5.2.0 LTS (headless, CPU Cycles), `gltfpack@0.24` via
`npx`, node v22.19.0 with three ^0.185.1 in `g3check/`, python3 + Pillow 11.3.0,
gzip −9.

## 1. Metrics

| | input | shipped | Δ |
|---|---|---|---|
| File, raw | 310,156 B | **143,672 B** | **−53.7%** |
| File, gzip −9 | 52,503 B | 92,622 B | +76% (see §4) |
| Triangles | 5,312 | 5,312 | 0 |
| Vertices | 10,464 | 10,464 (2,832 unique pre-pack) | — |
| Mesh objects | 92 | **12** | −87% |
| Draw submeshes (primitives) | 94 | **14** | −85% |
| Materials | 11 | 11 | identical set |
| bbox dims | 31.913 × 31.531 × 9.500 m | 31.913 × 31.531 × 9.500 m | 0 |
| bbox min Z | 0.000 | 0.000 | 0 |
| XY centre | (+0.151, −0.000) | (+0.151, −0.000) | 0 |
| Ray-flip fraction | — | **0.000000** (22,500 rays, 16,322 hits) | — |

Vertex attributes are `POSITION` + `NORMAL` only; no UVs, no textures, no
tangents, so there is nothing to prune and nothing to bake.

## 2. Phase A — waste census

| Technique | Found | Predicted saving | Actual |
|---|---|---|---|
| Duplicate mesh data | 2,424 redundant tris across repeated skylight frames/panes, plant boxes, AC boxes, coping bars | 0 tris (glTF already shares nothing here; the win is accessor/node overhead, which the join and the pack collect) | collected by steps 5 + Phase C |
| Degenerate faces | **0** | 0 | 0 |
| Coincident vertex pairs | 7,632 | 0 tris — these are *between* objects (each solid is separately welded by `bevel`), and a cross-object weld would fuse glow shells onto base surfaces | 0 |
| Buried interior faces | 0 provable | 0 | 0 |
| Over-tessellation | none — the asset has no curved shells at all, only beveled boxes | 0 | 0 |
| Object-count overhead | 92 objects across 11 materials; 8 join groups | 92 → 12 objects, 94 → 14 submeshes | **achieved** |

The census says plainly what this asset is: geometry that was already clean when
it left the build script. **All of the win is packing and draw-call overhead,
none of it is triangles** — and that is the correct outcome, because every
triangle here is silhouette or a recognition cue at the app's camera distance
(Gate G6's escape clause).

## 3. Phase B — geometry cleanup

| Step | tris | verts |
|---|---|---|
| input | 5,312 | 2,832 |
| 1+2a weld ≤1 mm + degenerate | 5,312 | 2,832 |
| 2b buried interior faces | 5,312 | 2,832 |
| 3 limited dissolve | **skipped — see below** | |
| 5 join per material | 5,312 | 2,832 |

Weld and degenerate found nothing: `bevel()` in the build script already welds
each solid, and the validator had already reported zero degenerate triangles.

**Step 3 (limited dissolve) was skipped without measuring the win**, per
`GLB-OPTIMIZE-PROMPT.md` §3 step 3. That rule exists for assets with large
coplanar ring bands, and 590 Third has **four**: `parapet` and `parapet_cap`
follow the footprint the whole way round, and `body` and `roof_field` are genus-1
solids whose top and bottom caps are annuli bridged corner to corner around the
light well. A strictly-coplanar dissolve merges each such ring into one annulus
ngon, and re-triangulating an annulus emits slivers whose averaged vertex normals
collapse to ~0 — invisible in Blender (which recomputes loop normals on import),
fatal in the packed file (gltfpack re-emits the stored normals), and caught only
by the stage-2 contract validator two steps after the shipping swap. On
`350-brannan` the same step was worth 30 triangles out of 6,770. Here the caps at
risk are the light well, which is the asset's most distinctive feature. Not a
trade.

Step 4 (curve retessellation) is not applicable: no curved shells.

Step 5 joined 92 objects into 12, one per material. No manifest-named nodes and
no `Toy_body` exist on this asset, so nothing had to be held out.

Normals audit after the joins: zero inverted signed volumes.

## 4. Phase C — packing

```
npx gltfpack@0.24 -i mid.glb -o 590-third.optimized.glb -c -km -kn -noq
```

`-km -kn` are mandatory (glow-ness is name-only; without `-km` gltfpack merges
`Toy_sky` into `Toy_sky_Glow` and kills the night layer). `-noq` is the repo
standard and matches `pipeline/compress-assets.mjs`. Material set verified
identical on the output, not assumed from the flags.

**The gzip number goes the wrong way, and that is expected.** Meshopt-encoded
buffers are already entropy-coded, so they do not recompress: raw drops 53.7%
while gzip −9 rises from 52.5 KB to 92.6 KB. `350-brannan` recorded the same
shape (raw −51.8%, gzip +102%) on 12 August. Meshopt is currently costing
*transfer* bytes on small assets relative to plain gzip, and buying decode-time
and GPU-memory wins plus one uniform encoding across every shipped asset. That is
the repo's standing trade (`AGENTS.md`: every GLB entering `app/public/sf-assets/`
is meshopt-compressed at intake), not a regression in this asset, and the
decision is not re-opened here.

At 143.7 KB raw the asset is well inside the ≤ 500 KB per-landmark budget either
way.

## 5. Phase E — A/B verification

Same rig for both files: 42° aerial from **due east** (the bisector of the
3rd Street front at 45.2° and the Brannan front at 135.1°, so both designed
elevations and the raised corner parapet are in frame), near = 1.5 × long axis
= 47.9 m, far = 6 × = 191.5 m, day and night, plus four orthographic elevations.

| View | mean abs RGB Δ | max px Δ | gate |
|---|---|---|---|
| day near | 0.0020% | 24 | ≤ 4% |
| day far | 0.0028% | 8 | ≤ 2% |
| night near | 0.0362% | 28 | ≤ 4% |
| night far | 0.0456% | 24 | ≤ 2% |
| elev N / E / S / W | 0.0019 / 0.0016 / 0.0057 / 0.0035% | ≤ 27 | — |

**Looked at, not just measured.** At ×8 amplification the day diffs are black.
The night diffs show a faint outline along the edges of the glowing shopfront
bays and around the café panel — sub-pixel edge sampling on the highest-contrast
boundary in the scene, which is exactly where a re-encoded normal buffer would
show first. Nothing is missing, no silhouette moved, no shading changed, and
there is nothing here a player could notice. Night deltas are ~20× the day ones
in relative terms and still two orders of magnitude inside the gate.

## 6. Gate results

| Gate | Result |
|---|---|
| G1 Contract — material set identical, `_Glow` separate, no `Toy_body`, no manifest node names to preserve | **PASS** |
| G2 Geometry — bbox within max(1 cm, 0.1%); origin within 1 cm; all signed volumes positive; flipped fraction 0.000000 ≤ 0.15% | **PASS** |
| G3 Round-trip — re-imports in Blender; loads in pinned three@0.185.1 via `g3check` with `MeshoptDecoder`, 14 meshes, 5,312 tris, 11 materials, bbox 31.913 × 9.5 × 31.531 (Y-up) | **PASS** |
| G4 Appearance — day+night × near+far, max mean delta 0.0456% | **PASS** |
| G5 Draw submeshes — 94 → 14 | **PASS** |
| G6 Size — raw −53.7%, below the 60% target; the census shows the remainder is silhouette and recognition geometry with zero removable triangles | **PASS** (with the documented escape clause) |
| G7 GPU budget — bake mode not used | n/a |
| G8 Hygiene — re-import object/material check clean, deterministic re-run reproduces the output, no `.blend1` files | **PASS** |

## 7. Shipping swap

`590-third.optimized.glb` copied over `artifacts/590-third/590-third.glb`. The
pre-optimize original is archived byte-for-byte at
`optimize/input/590-third.glb` (310,156 B).

The stage-2 contract validator (`artifacts/590-third/validate_590_third.py`) was
re-run **on the shipped file** and returns **PASS on all 15 checks** — 12
objects, 5,312 triangles, min Z 0.000, max Z 9.500, loader scale factor 1.000000.
`artifacts/590-third/validation.json` and `REPORT.md` now carry the shipped
numbers, so the integration stage writes its manifest entry from reality.
