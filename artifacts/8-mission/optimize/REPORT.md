# 8 Mission Street — optimize report (stage 4)

`GLB-OPTIMIZE-PROMPT.md` v2 on `artifacts/8-mission/`.
`ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`.

## Result

| | input | shipped |
|---|---|---|
| File, raw | 1,330,784 B | **485,656 B** (−63.5%) |
| File, gzip | 242,232 B | 271,335 B |
| Mesh objects | 689 | **14** |
| Draw submeshes (glTF primitives) | 696 | **16** |
| Triangles | 19,082 | 19,082 |
| Vertices | 36,282 | 35,638 (11,006 before the packer re-splits by primitive) |
| Materials | 12 | 12, identical set |
| bbox | 74.13806 × 56.54835 × 28.66 | **identical to 5 dp** |
| origin XY | (0, 0) | (0, 0) |

**Toolchain:** Blender 5.2.0 LTS; `npx gltfpack@0.24`; node v22.19.0 with pinned
`three@^0.185.1` in `g3check/`; python3 + Pillow; gzip.

`8-mission.optimized.glb` has been copied over `artifacts/8-mission/8-mission.glb`.
The pre-optimize original is archived byte-for-byte at `input/8-mission.glb`.

## Phase A — waste census

689 objects, 19,082 tris, 36,282 verts, 696 primitives, 0 degenerate triangles,
**25,276 coincident vertex pairs**, 7,442 triangles in duplicate meshes (the eight
turret fins, the eight brick ribs, the roof vents, the terrace panels). Predicted:
the weld takes roughly 60% of the vertices and the per-material join takes the
primitive count from 696 to ~14. Both landed.

## Phase B — geometry cleanup

| Step | tris | verts |
|---|---|---|
| input | 19,082 | 36,282 |
| weld ≤ 1 mm + degenerate | 19,082 | **11,006** |
| interior faces | 19,082 | 11,006 |
| limited dissolve | **skipped** | |
| join per material | 19,082 | 11,006 |

- **The weld is the whole Phase B win here:** −69.7% vertices for zero triangles,
  because a build script that emits one prism per window, pier, rib, vent and terrace
  panel duplicates a vertex at every shared corner.
- **Interior-face removal found nothing**, which is correct rather than
  disappointing: the occluder rule only trusts CLOSED solids that fill ≥ 95% of their
  own AABB, and every large mass on this asset is a rotated L or a cylinder, so none
  of them qualifies as a box-like occluder. No faces were guessed at.
- **The limited dissolve was skipped deliberately** (prompt §3.3). This asset is
  almost nothing but ring bands — three parapets, three copings, three plinths and two
  sill courses, each a closed annulus following the footprint the whole way round.
  Their top and bottom faces are perfectly coplanar annuli, so even a strictly-coplanar
  0.05° dissolve merges each into one ngon, and re-triangulating an annulus emits
  hairline slivers that pass an area-based degeneracy test and only surface in the
  packed file as `invalid_or_nonunit_loop_normal_count`. That is the recorded
  `350-brannan` failure, and on this asset the dissolve had even less to win than there.
- The join collapsed 689 objects into 14 groups, one per material set. Signed volume
  is positive on all 14; `inverted_solids: []`.

## Phase C — packing

```
npx gltfpack@0.24 -i mid.glb -o 8-mission.optimized.glb -c -km -kn -noq
```

`-km -kn` keep the material and node names, which are API here: the loader splits
`*_Glow` into the unlit night layer by NAME, and `Toy_glassl` and `Toy_glassl_Glow`
have identical parameters — without `-km` gltfpack merges them and the turret's
lantern stops existing at night. `-noq` is the repo standard and what
`compress-assets.mjs` produces; the float32 attributes it preserves are what the
runtime merge paths need.

983,680 B → 485,656 B. The gzip figure rises (242 KB → 271 KB) because meshopt output
is already entropy-coded; the raw byte count is the one the CDN and the loader see.

485.7 KB / 19,082 tris sits squarely in the shipped landmark band — 501 Second is
476 KB / 16,008 tris and Salesforce Tower 451 KB / 20,086 — and inside the 500 KB
per-landmark budget in `AGENTS.md`.

## Phase E — A/B verification

Renders: `BLENDER_EEVEE`, 64 TAA samples, one rig, input vs output, day (glow alpha
0.12) and night (alpha 1.0, emission ≈ 6) at near (1.5 × long axis) and far (6 ×), plus
four orthographic elevations. EEVEE rather than Cycles: the build machine was at load
average ~150 with ~16 concurrent Blender processes and CPU Cycles makes no progress
there. For an A/B gate that is an improvement, not a compromise — EEVEE is
deterministic and noise-free, so a non-zero delta means a real difference rather than
sampling noise.

| View | mean abs RGB Δ | max px Δ |
|---|---|---|
| day near | 0.0036% | 7 |
| day far | 0.0030% | 3 |
| night near | 0.0018% | 4 |
| night far | 0.0019% | 1 |
| elev N / E / S / W | 0.0070 / 0.0071 / 0.0130 / 0.0090% | 6 / 15 / 7 / 11 |

Thresholds are 2% far and 4% near; the worst view here is 0.013%, i.e. **150× inside
tolerance**. Looking at the ×8-amplified diffs: they are black except for single-pixel
outlines on a few silhouette edges — the weld moved coincident vertices onto each
other and the rasteriser resolves one or two boundary pixels differently. Nothing
changed that a player could see: the turret's lantern, the three parapet lines, the
plaster attic band, the arcade, the terraces and every glow surface are pixel-identical
away from those edges.

## Gate results

| Gate | Result | Evidence |
|---|---|---|
| **G1** Contract | **PASS** | material set identical (12/12); `_Glow` still three separate materials; no `Toy_body`; node names not manifest-referenced |
| **G2** Geometry | **PASS** | bbox identical to 5 dp; origin (0,0); 14/14 signed volumes positive, `inverted_solids: []`; 22,500 rays, 16,025 hits, **0 flipped** |
| **G3** Round-trip | **PASS** | re-imports in Blender; `g3check` (pinned three 0.185.1): `G3-OK meshes:16 tris:19082`, 12 materials, bbox 74.138 × 28.66 × 56.548 (three's Y-up), no decode errors |
| **G4** Appearance | **PASS** | worst mean delta 0.013% vs a 2%/4% tolerance; diffs are edge pixels only |
| **G5** Draw submeshes | **PASS** | 696 → **16** |
| **G6** Size | **PASS** | −63.5% raw, above the 60% target |
| **G7** GPU budget | n/a | `ALLOW_BAKE: no` |
| **G8** Hygiene | **PASS** | re-import object/material/bbox check inside `optimize.py`; deterministic scripts committed here; no `.blend1` left |

## Post-swap contract re-validation

The stage-2 contract validator was re-run against the **shipped** (packed) file, not
just the mid-stage one, because that is where a sliver failure would surface:

`artifacts/8-mission/validation.json` — **overall PASS**, 17/17 checks, 14 mesh
objects, 19,082 triangles, 206/206 open glow-strip faces outward, 31,432 visibility
rays with 0 flipped, 0 degenerate triangles, 0 non-unit loop normals.
