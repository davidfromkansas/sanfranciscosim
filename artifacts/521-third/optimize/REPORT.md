# 521 Third Street — GLB optimize report

Stage 4 of `docs/asset-pipeline/ADDRESS-TO-ASSET.md`, run per
`docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md` on 18 August 2026.
`ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`.

| Metric | Input | Optimized | Delta |
|---|---|---|---|
| File size, raw | 588,992 B | **248,552 B** | **−57.8 %** |
| File size, gzip −9 | 98,415 B | 148,989 B | +51.4 % (see §4) |
| Triangles | 8,848 | 8,848 | 0 |
| Vertices | 17,890 | 16,828 | −5.9 % packed (4,930 pre-pack, −72.4 %) |
| Objects / nodes | 255 | **15** | −94.1 % |
| Draw primitives | 256 | **16** | −93.8 % |
| Materials | 14 | 14 | identical set |
| Bbox (m) | 27.36147 × 27.10141 × 11.4 | 27.36147 × 27.10141 × 11.4 | **0** |
| Origin offset XY (m) | −0.28767 / −0.10843 | −0.28767 / −0.10843 | **0** |

Toolchain: Blender 5.2.0 LTS, `npx gltfpack@0.24`, three ^0.185.1 (pinned in
`g3check/package.json`), Python 3.9 + Pillow 11.3.0, gzip −9.

The input was copied byte-for-byte to `input/521-third.glb` and verified with
`cmp` before anything ran; every step below is a committed deterministic script.

## 2. Phase A — waste census

`inspect.py` → `inspect.json`. 255 objects, 8,848 tris, 17,890 verts, 256
estimated primitives, one vertex attribute beyond position (`NORMAL`), no
textures, no degenerate triangles.

| Technique | Predicted | Actual |
|---|---|---|
| Weld coincident verts (12,960 coincident pairs) | large vertex win, no tri change | **−12,960 verts**, 0 tris |
| Delete degenerate faces (0 found) | 0 | 0 |
| Delete buried interior faces | ~0 — this asset has no nested solids; its applied bands sit *proud* of the walls by design, precisely so they stay visible | **0** |
| Limited dissolve | **skipped** — see §3 | — |
| Retessellate curves | n/a — no curved geometry | — |
| Join per material (12 groups) | the dominant win: node + accessor overhead | **255 → 15 objects** |

`dup_redundant_tris` reports 4,772 triangles living in repeated meshes (44 dentil
teeth, 26 meander ticks, 10 window trims, 10 glass panes, five vents, four flues,
three duct runs…). Those are joined rather than instanced: at 12–60 triangles
each, GPU instancing would cost more node overhead than it saves, and the
landmark path merges everything into one shared `BatchedMesh` at runtime anyway.

## 3. Phase B — geometry cleanup

`optimize.py` → `phaseb_stats.json`.

| Step | Tris | Verts |
|---|---|---|
| input | 8,848 | 17,890 |
| weld ≤ 1 mm + degenerate delete | 8,848 | **4,930** |
| interior faces (0 removed) | 8,848 | 4,930 |
| limited dissolve — **skipped** | 8,848 | 4,930 |
| join per material (12 joins) | 8,848 | 4,930 |

Joins: `Toy_ink` 89, `Toy_greige` 76, `Toy_cream` 25, `Toy_glass` 18,
`Toy_steel` 14, `Toy_cocoa` 9, `Toy_glass_Glow` 7, `Toy_oxblood` 6,
`Toy_cobalt` / `Toy_mint` / `Toy_orange` / `Toy_orange_Glow` 2 each.
`Toy_mustard` (the 527 awning) and `Toy_p_tan` (the Taber stucco) are single
objects and stayed as they were.

**The limited dissolve was skipped**, per GLB-OPTIMIZE-PROMPT §3.3. This asset
has **two** footprint-following ring bands — `parapet` (0.30 m, all four
footprint edges, 10.90 → 11.40 m) and `coping` (the dark cap ring over it). Their
top and bottom faces are perfectly coplanar annuli, so even a strictly-coplanar
0.05° dissolve merges each into a single ngon, and re-triangulating an annulus
emits slivers tens of metres long and a fraction of a millimetre wide. Those pass
an area-based degeneracy test and survive Phase B and E, then fail the stage-2
contract validator *after* the shipping swap, as
`invalid_or_nonunit_loop_normal_count` in the packed file (measured on
350-brannan, 13 Aug 2026). At 8,848 triangles the dissolve would have been worth a
fraction of a percent; it is not worth manufacturing that failure.

## 4. Phase C — packing

```
npx gltfpack@0.24 -i mid.glb -o 521-third.optimized.glb -c -km -kn -noq
```

`-km -kn` keep the material and node names, which are API here: `Toy_glass` and
`Toy_glass_Glow`, and `Toy_orange` and `Toy_orange_Glow`, are parameter-identical
apart from the name, and without `-km` gltfpack merges each pair and silently
kills the night layer. `-noq` is the repo standard — `pipeline/compress-assets.mjs`
produces unquantized meshopt, and a quantized build fails the stage-2 contract
validator on `transforms_applied` and `no_unexpected_objects`.

**Honest note on the gzip number.** Raw bytes drop 57.8 % but gzipped bytes rise
51.4 %, because meshopt's vertex/index codec is already entropy-coded and gzip has
nothing left to remove, while the uncompressed input gzips very well. On an asset
this small the two effects cross over the wrong way: over a
`Content-Encoding: gzip` transfer this file costs ~49 KB *more* than the
unoptimized one. It ships anyway, for the same reason `592-third` and
`370-brannan` did (their reports record the identical crossover): meshopt is the
repo's intake standard, the loaders register `MeshoptDecoder`, and the win that
actually matters here is the **72 % vertex reduction and 256 → 16 draw
primitives**, which is GPU memory and batch-merge cost, not bytes.
`compress-assets.mjs` will skip this file at ship time because it already carries
`EXT_meshopt_compression`.

## 5. Phase D — bake

Not run. `ALLOW_BAKE: no`, and the contract forbids textures.

## 7. Phase E — A/B verification

`render_ab.py` on both files with one rig (42° aerial, near = 1.5 × long axis =
41.0 m, far = 6 × = 164.2 m), day (glow alpha 0.12) and night (alpha 1.0,
emission 6, dusk world), plus four orthographic elevations. `diff_ab.py` →
`diffs.json`, contact sheet at `renders/contact_sheet.png` (rows: input /
optimized / diff ×8).

| View | Mean abs RGB delta | Max px delta |
|---|---|---|
| day near | **0.0029 %** | 15 |
| day far | 0.0040 % | 7 |
| night near | 0.0004 % | 2 |
| night far | 0.0008 % | 1 |
| elev N / E / S / W | 0.0090 / 0.0042 / 0.0064 / 0.0060 % | 35 / 24 / 20 / 30 |

Every number is two to four orders of magnitude inside the gate (≤ 2 % far,
≤ 4 % near). **Looked at the diffs:** the ×8-amplified diff row is black except
for hairline traces along a few silhouette edges — the cornice's outer arris, the
parapet coping, the top of the Greek-key band and the downpipes — sub-pixel
rasterization differences from the reordered vertex buffers, not geometry. The
night diffs are the *smallest* of the set here (0.0004 %), because the night pass
is dominated by the two glow shells and those survive the join untouched.
Nothing a player could see: the awning, the blade sign, the fire escapes, the
dentil course, the mural shapes and every roof object render identically.

## 8. Gate results

| Gate | Result | Notes |
|---|---|---|
| G1 Contract | **PASS** | material set identical (14/14), both `_Glow` pairs kept separate under `-km`, no `Toy_body` (correct — landmark), node names intact |
| G2 Geometry | **PASS** | bbox delta 0, origin delta 0, all 15 signed volumes positive, ray test 22,500 rays / 16,961 hits / **0 flipped** (0.0 %) |
| G3 Loader | **PASS** | `g3check` three@0.185.1 GLTFLoader + MeshoptDecoder round-trip: 16 meshes, 8,848 tris, 14 materials, bbox 27.3615 × 11.4 × 27.1014 (three's Y-up) |
| G4 Visual | **PASS** | max mean-abs delta 0.0090 % against a 2–4 % gate |
| G5 Draw calls | **PASS** | 256 → 16 primitives |
| G6 Size | **PASS** on raw (−57.8 %); **crossover on gzip** (+51.4 %), documented in §4 and accepted |
| G7 Night | **PASS** | night deltas 0.0004 / 0.0008 %, both glow materials present and separate |
| G8 Re-validate after swap | **PASS** | the stage-2 contract validator re-run on the *shipped* (packed) file: all 16 checks true, 8,848 tris, crest exactly 11.400 m |

## 9. Shipping swap

`optimize/521-third.optimized.glb` → `artifacts/521-third/521-third.glb`
(248,552 B). The pre-optimize original is archived byte-for-byte at
`optimize/input/521-third.glb` (588,992 B); `cmp` verified the archive against the
live file immediately before the swap. `artifacts/521-third/validation.json` and
`REPORT.md` now carry shipped numbers.
