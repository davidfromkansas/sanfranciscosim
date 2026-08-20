# 2 Folsom Street — optimize pass (stage 4)

Run of `docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md` v2 against `artifacts/2-folsom/`,
19 August 2026. `ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`.

**Result: all gates PASS; `2-folsom.optimized.glb` is the shipping file.**

## 1. Metrics

| | input | output | delta |
|---|---|---|---|
| File, raw | 1,248,312 B | **494,180 B** | **−60.4%** |
| File, gzip −9 | 165,765 B | 257,150 B | see §4 |
| Triangles | 16,996 | 16,996 | 0 |
| Vertices (Blender, welded) | 33,068 | 10,080 in `mid.glb` | −69.5% at the weld |
| Vertices (glTF accessors) | 33,068 | 35,985 | +8.8%, see §3 |
| Objects | 801 | **14** | −98.3% |
| Draw submeshes (primitives) | 806 | **16** | −98.0% |
| Materials | 13 | 13 | identical set |
| bbox | 113.9196 x 113.9579 x 88.0 | identical | 0 |
| origin offset | (1.45486, 1.42714) | identical | 0 |
| Ray-test flipped fraction | — | **0.000000** (0 of 13,284 hits) | — |

**494.2 KB is inside the 500 KB on-disk landmark budget**, with 5.8 KB of headroom. It got
there by cutting geometry in stage 2, not by anything this pass did — see §6.

Toolchain: Blender 5.2.0 LTS (fbe6228777e7); `npx gltfpack@0.24`; node with the pinned
`three@^0.185.1` in `g3check/`; python3 + Pillow; `gzip -9`. Scripts are adapted copies of
`tools/glb-optimize/`, committed here; re-running them on `input/2-folsom.glb` reproduces
the output.

## 2. Phase A — waste census

| Technique | Found | Predicted | Actual |
|---|---|---|---|
| Coincident vertex pairs (≤ 1 mm) | 22,988 | large vertex win, no triangle change | 33,068 → 10,080 verts in Blender |
| Duplicate mesh groups | 8,596 redundant triangles across 60+ signature groups (window fills, piers, bands, crenels, hedges) | 0 triangles — they are distinct instances at distinct places, so the win is node overhead, not geometry | 801 → 14 objects |
| Degenerate faces | 0 | 0 | 0 |
| Buried interior faces | none provable | 0 | 0 |
| Over-tessellated curves | none — the asset has no curved geometry at all; every surface is a planar panel, box or prism | n/a | n/a |
| Objects sharing a material | 13 material groups over 801 objects | the biggest win | 806 → 16 primitives |

## 3. Phase B — geometry cleanup

1. **Weld ≤ 1 mm, per object.** 33,068 → 10,080 vertices, no triangle change. Per-object
   only, so a glow shell can never fuse onto the opaque surface behind it.
2. **Degenerate + buried faces:** none found, none removed. No mesh here is an enclosing
   closed solid around another, so the occluder rule found nothing to delete.
3. **Limited dissolve: SKIPPED**, deliberately. This asset has seven coplanar ring bands
   that follow the footprint all the way round — `base_course`, `base_cornice`,
   `base_parapet`, `base_coping`, `sup_cornice`, `sup_parapet`, `sup_coping`, plus
   `crown_parapet` and both tower ledges. That is exactly the sliver trap the prompt's §3
   step 3 documents from `350-brannan`: a strictly-coplanar dissolve merges each ring's
   top and bottom faces into one annulus ngon, and re-triangulating an annulus emits
   metre-long, sub-millimetre-wide slivers that pass every area-based degeneracy test and
   then fail the stage-2 validator on collapsed vertex normals — only in the packed file.
   The step is worth a fraction of a percent on an asset like this. Not run.
4. **Curve retessellation:** not applicable, no curves.
5. **Join per material:** 801 → 14 objects. `Toy_glass` alone absorbed 419 objects,
   `Toy_stone` 187, `Toy_glass_Glow` 88. No manifest-named nodes and no `Toy_body` here,
   so nothing had to be held out.
6. **Normals audit:** every closed solid's signed volume positive; `inverted_solids: []`;
   22,500 deterministic visibility rays, 13,284 hits, **0 flipped**.

## 4. Phase C — packing

```
npx gltfpack@0.24 -i mid.glb -o 2-folsom.optimized.glb -c -km -kn -noq
```

`-km` and `-kn` keep the material and node names, which are API here: the loader splits
`*_Glow` into the unlit night layer by NAME, and `Toy_glassl` / `Toy_glassl_Glow` are
identical in every parameter except that name. Without `-km` gltfpack would merge them and
silently delete the atrium skylight's night state — the hero glow of this asset.

`-noq` (no quantization) is the repo standard, matching `pipeline/compress-assets.mjs`.
Verified on the output rather than trusted from the flags: material name set identical,
node names intact, re-imported bbox and origin bit-identical to the input's.

**Two numbers in §1 that look like regressions and are not.**

*gzip rises, 165.8 KB → 257.2 KB.* Meshopt buffers are already entropy-coded, so gzip has
nothing left to find and its own framing adds bytes. The raw file — what the CDN stores
and what the decoder streams — fell 60.4%. This is the same pattern recorded on
`501-second` and `380-brannan`.

*glTF accessor vertices rise, 33,068 → 35,985, while Blender's welded count fell to
10,080.* Those count different things. Blender counts mesh vertices; glTF must split a
vertex wherever the normal or the material differs across it, and this asset is 16,996
flat-shaded triangles on hard-edged boxes, so nearly every corner splits. The weld still
paid — it is why the raw file more than halved — but it pays in the buffer's redundancy,
not in the accessor count.

## 5. Phase E — A/B verification

Input vs output, same rig, `clip_end = 50000`, day (glow alpha 0.12, the app's day pass)
and night (alpha 1.0, emission 6, dusk world), near 170.9 m and far 683.7 m, plus a
four-elevation contact sheet.

| View | mean abs RGB delta | max pixel delta | gate |
|---|---|---|---|
| day near | **0.0065%** | 17 | ≤ 4% |
| day far | **0.0151%** | 27 | ≤ 2% |
| night near | **1.3324%** | 123 | ≤ 4% |
| night far | **1.1230%** | 110 | ≤ 2% |
| elevations N / E / S / W | 0.0030 / 0.0192 / 0.0009 / 0.0017% | 41 max | — |

**Looked at, honestly.** The day diffs are effectively black. The night diffs are the only
ones with any energy, and amplified 8x they are a uniform grain spread evenly over every
lit surface with no structure anywhere — Cycles path-tracing noise between two renders of
a scene lit almost entirely by emissive materials, which is the noisiest thing this rig
does. Nothing is missing: the atrium skylight's 5 x 4 grid, the crown pavilion's glazing,
the scattered lit windows and both portico sign bands are present and identical in
position and extent in both. No silhouette change, no shading artifact, nothing a player
would notice.

## 6. Judgment calls

- **The 500 KB budget was met in stage 2, not here.** The first optimize run produced a
  correct, all-gates-passing 721 KB file from a 23,852-triangle asset — 44% over the
  landmark budget. Packing cannot fix that; only geometry can. The asset went back to the
  build script three times (bevel policy tightened to drop every applied panel, bay pitch
  widened from ~6.2 m to ~8.5 m, tower window bands from 9 to 8 and the crown's second
  setback from 3 bays to 2, skylight rib grid 6x5 → 5x4) for a net 23,852 → **16,996**
  triangles, and only then did the same optimize chain land at 494 KB. The deciding
  measurement was `inspect.json`'s own `one_px_world_m: 0.1152` at the near landmark
  distance: a 0.05 m bevel on a 0.18 m proud pier is less than half a screen pixel there,
  so it was buying nothing and costing 3,000 triangles and far more vertices.
- **No bake.** `ALLOW_BAKE: no`, and nothing here argued for reopening it: the contract
  forbids textures without a recorded exception, and the facade detail that a bake would
  capture is a flat-colour pier-and-band system that already costs almost nothing.
- **The remainder is silhouette and rhythm.** After the weld and the join there is no
  duplicate mesh, no degenerate face and no buried face left — 10,080 welded vertices for
  16,996 triangles across 14 objects. What is left is the three mass transitions, the
  four articulated elevations and the roof composition, which is the asset.

## 7. Gate results

| Gate | Result | Evidence |
|---|---|---|
| G1 Contract — material set identical, `_Glow` separate, no `Toy_body` | **PASS** | `validation.json` `G1_materials_identical: true`; all 13 names round-trip |
| G2 Geometry — bbox ≤ max(1 cm, 0.1%), origin ≤ 1 cm, volumes positive, flips ≤ 0.15% | **PASS** | bbox and origin identical to 5 decimals; `inverted_solids: []`; flipped fraction **0.000000** |
| G3 Round-trip — Blender and the pinned three | **PASS** | `G3-OK {"ok":true,"meshes":16,"tris":16996,...}`; no decode errors; only `EXT_meshopt_compression` |
| G4 Appearance — day+night x near+far | **PASS** | table in §5; worst case 1.33% against a 4% gate |
| G5 Draw submeshes ≤ input | **PASS** | 806 → **16** |
| G6 Size reduced (target 60%) | **PASS** | −60.4% raw, and inside the 500 KB landmark budget |
| G7 GPU budget | n/a | bake mode off |
| G8 Hygiene — no foreign geometry, deterministic, no `.blend1` | **PASS** | re-import object count 14 = joined group count; scripts committed and reproducible; no `.blend1` |

## 8. Shipping swap

`2-folsom.optimized.glb` copied over `artifacts/2-folsom/2-folsom.glb`; the pre-optimize
asset is archived byte-for-byte at `optimize/input/2-folsom.glb`. The asset's own
`validation.json` and `REPORT.md` were re-run and updated to the shipped numbers so the
integration stage writes its manifest entry from reality.
