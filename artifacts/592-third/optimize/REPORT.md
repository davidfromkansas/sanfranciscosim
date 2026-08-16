# 592 Third Street — GLB optimize report

Stage 4 of `docs/asset-pipeline/ADDRESS-TO-ASSET.md`, run per
`docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md` on 13 August 2026.
`ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`.

| Metric | Input | Optimized | Delta |
|---|---|---|---|
| File size, raw | 232,860 B | **104,828 B** | **−55.0 %** |
| File size, gzip −9 | 41,042 B | 70,664 B | +72.2 % (see §4) |
| Triangles | 3,352 | 3,352 | 0 |
| Vertices | 6,976 | 1,876 | **−73.1 %** |
| Objects / nodes | 101 | **10** | −90.1 % |
| Draw submeshes (`g3check`) | 102 est. | **11** | −89.2 % |
| Materials | 9 | 9 | identical set |
| Bbox (m) | 31.2145 × 32.2102 × 8.2 | 31.2145 × 32.2102 × 8.2 | 0 |
| Origin offset XY (m) | 0.1685 / −0.0008 | 0.1685 / −0.0008 | 0 |

Toolchain: Blender 5.2.0 LTS, `npx gltfpack@0.24`, Node v22.19.0, three
^0.185.1 (pinned in `g3check/package.json`), Python 3.9 + Pillow 11.3.0,
gzip −9.

The input was copied byte-for-byte to `input/592-third.glb` and verified with
`cmp` before anything ran; every step below is a committed deterministic script.

## 2. Phase A — waste census

`inspect.py` → `inspect.json`. 101 objects, 3,352 tris, 6,976 verts, 102
estimated primitives, one vertex attribute beyond position (`NORMAL`), no
textures, no degenerate triangles.

| Technique | Predicted | Actual |
|---|---|---|
| Weld coincident verts (5,100 coincident pairs) | large vertex win, no tri change | **−5,100 verts**, 0 tris |
| Delete degenerate faces (0 found) | 0 | 0 |
| Delete buried interior faces | ~0 — this asset has no nested solids; its applied panels sit *proud* of the walls by design, precisely so they stay visible | **0** |
| Limited dissolve | **skipped** — see §3 | — |
| Retessellate curves | n/a — the asset contains no curved geometry | — |
| Join per material (9 groups, 20 duplicate-mesh groups) | the dominant win: node + accessor overhead | **101 → 10 objects** |

`dup_redundant_tris` reports 1,928 triangles living in repeated meshes (four
identical condensers, eight identical skylight kerbs, eight caps, two hatches,
two vents, ten window trims…). Those are joined rather than instanced: at 44–108
triangles each, GPU instancing would cost more node overhead than it saves, and
the landmark path merges everything into one shared `BatchedMesh` at runtime
anyway.

## 3. Phase B — geometry cleanup

`optimize.py` → `phaseb_stats.json`.

| Step | Tris | Verts |
|---|---|---|
| input | 3,352 | 6,976 |
| weld ≤ 1 mm + degenerate delete | 3,352 | **1,876** |
| interior faces (0 removed) | 3,352 | 1,876 |
| limited dissolve — **skipped** | 3,352 | 1,876 |
| join per material (8 joins) | 3,352 | 1,876 |

Joins: `Toy_trim` 21, `Toy_glass` 20, `Toy_roofd` 15, `Toy_ink` 13, `Toy_stone`
11, `Toy_glass_Glow` 9, `Toy_glassl` 8, `Toy_glassl_Glow` 2. `body` keeps its
own mesh (two materials) and `garage` its own (`Toy_steel`, one other user).

**The limited dissolve was skipped deliberately**, per GLB-OPTIMIZE-PROMPT §3.3.
This asset has exactly the disqualifying feature: `parapet`, a 0.30 m band
following all four footprint edges from 7.82 to 8.20 m, whose top and bottom
faces are perfectly coplanar annuli. A strictly-coplanar 0.05° dissolve merges
each annulus into one ngon, and re-triangulating an annulus emits slivers tens
of metres long and a fraction of a millimetre wide — invisible, area-test-clean,
and fatal two steps later in the packed file as
`invalid_or_nonunit_loop_normal_count` (measured on `350-brannan`, 13 Aug 2026).
At 3,352 triangles the dissolve was worth a fraction of a percent. Not taken.

Normals audit: `inverted_solids: []`. Re-import verify: bbox within tolerance,
material set identical.

## 4. Phase C — packing

```
npx gltfpack@0.24 -i mid.glb -o 592-third.optimized.glb -c -km -kn -noq
```

`-km -kn` keep the material and node names, which are API here: `Toy_glass` and
`Toy_glass_Glow` are parameter-identical apart from the name, and without `-km`
gltfpack merges them and silently kills the night layer. `-noq` is the repo
standard — `pipeline/compress-assets.mjs` produces unquantized meshopt, and a
quantized build fails the stage-2 contract validator on `transforms_applied`
and `no_unexpected_objects`.

**Honest note on the gzip number.** Raw bytes drop 55 % but gzipped bytes rise
72 %, because meshopt's vertex/index codec is already entropy-coded and gzip has
nothing left to remove, while the uncompressed input gzips very well. On an
asset this small the two effects cross over the wrong way: over a
`Content-Encoding: gzip` transfer this file costs ~29 KB *more* than the
unoptimized one. It ships anyway, for the same reason `370-brannan` did (its
report §4 records the identical crossover): meshopt is the repo's intake
standard, the loaders register `MeshoptDecoder`, and the win that actually
matters here is the **73 % vertex reduction and 102 → 11 draw submeshes**, which
is GPU memory and batch-merge cost, not bytes. `compress-assets.mjs` will skip
this file at ship time because it already carries `EXT_meshopt_compression`.

## 5. Phase D — bake

Not run. `ALLOW_BAKE: no`, and the contract forbids textures.

## 7. Phase E — A/B verification

`render_ab.py` on both files with one rig (42° aerial, near = 1.5 × long axis =
48.3 m, far = 6 × = 193.3 m, clip_end 50,000), day (glow alpha 0.12) and night
(alpha 1.0, emission 6, dusk world), plus four elevations. `diff_ab.py` →
`diffs.json`, contact sheet at `renders/contact_sheet.png` (rows: input /
optimized / diff ×8).

| View | Mean abs RGB delta | Max px delta |
|---|---|---|
| day near | **0.0042 %** | 21 |
| day far | 0.0055 % | 9 |
| night near | 0.0167 % | 19 |
| night far | 0.0171 % | 8 |
| elev N / E / S / W | 0.0068 / 0.0227 / 0.0289 / 0.0091 % | 27 / 25 / 21 / 26 |

Every number is two orders of magnitude inside the gate (≤ 2 % far, ≤ 4 % near).
**Looked at the diffs:** the ×8-amplified diff row is black except for
hairline traces along a few silhouette edges and along the top edge of the
shopfront fascia — sub-pixel rasterization differences from the reordered
vertex buffers, not geometry. The night diffs are the largest of the set and are
concentrated on the lit shopfront band's edges, for the same reason. Nothing a
player could see: the glow band, all eight skylights, the two glow shells, the
condenser row, the garage door and the entry all render identically.

## 8. Gate results

| Gate | Result | Notes |
|---|---|---|
| G1 Contract | **PASS** | material set identical (9/9), `_Glow` pair kept separate under `-km`, no `Toy_body` (correct — landmark), node names intact |
| G2 Geometry | **PASS** | bbox delta 0, origin delta 0, all signed volumes positive, ray test 22,500 rays / 16,453 hits / **0 flipped** (0.0 %) |
| G3 Round-trip | **PASS** | re-imports in Blender; `g3check` (pinned three ^0.185.1) loads it: `{"ok":true,"meshes":11,"tris":3352}`, no decode errors, only `EXT_meshopt_compression` |
| G4 Appearance | **PASS** | max mean delta 0.029 %; diffs inspected and described above |
| G5 Draw submeshes | **PASS** | 102 → 11 |
| G6 Size | **PASS** | raw −55.0 %, just under the 60 % aspiration. The census explains the remainder: 0 degenerates, 0 buried faces, no curves, no dissolve — after the weld and the joins, the residual 3,352 triangles are all silhouette and facade box geometry with nothing left to remove |
| G7 GPU budget | n/a | bake mode not used |
| G8 Hygiene | **PASS** | re-import object count matches (10), deterministic re-run reproduces the output, no `.blend1` files, `mid.glb` intermediate removed |

## 9. Shipping swap

`592-third.optimized.glb` was copied over `artifacts/592-third/592-third.glb`.
The pre-optimize original is archived at `optimize/input/592-third.glb`. The
asset's `validation.json` and `REPORT.md` were regenerated against the shipped
file — the stage-2 contract validator re-run on it returns **PASS on all 16
checks** with `object_count: 10`, so the integration stage writes its manifest
entry from shipped reality.
