# 50 United Nations Plaza — stage-4 optimize report

Run of `docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md` against
`artifacts/50-united-nations-plaza/`.

| Input | Value |
|---|---|
| `ASSET_CLASS` | `landmark` |
| `ALLOW_MESHOPT` | `yes` (`grep -rn setMeshoptDecoder app/src/` hits `gltf.js` and `assets.js`) |
| `ALLOW_BAKE` | `no` |
| Blender | 5.2.0 LTS (`fbe6228777e7`, 2026-07-14) |
| gltfpack | `npx gltfpack@0.24` |
| three (G3) | pinned `^0.185.1` in `g3check/package.json` |
| python | 3.9 + Pillow |

**Result: all gates PASS. Shipping file swapped.**

| | Input | Shipped | Δ |
|---|---|---|---|
| Raw bytes | 939,600 | **330,680** | **−64.8% (2.84×)** |
| gzip -9 bytes | 148,055 | 156,263 | +5.5% (see §6) |
| Triangles | 13,624 | 13,615 | −9 |
| Vertices | 26,292 | 23,951 | −8.9% |
| Objects / primitives | 548 | **11** | −98% |
| Materials | 11 | 11 | identical |
| bbox (m) | 122.7264 × 84.8953 × 33.0 | identical to 4 dp | 0 |
| origin | (0, 0, 0) | (0, 0, 0) | 0 |

## 2. Phase A — forensic inspection (`inspect.json`)

- 548 objects, 548 primitives — **one draw submesh per object**; the whole
  optimization is really this one number.
- 13,624 tris / 26,292 verts, **0 degenerate**, **18,384 coincident vertex
  pairs** (every prism and box is authored with unwelded corner-adjacent
  vertices, and the bevel pass multiplies them).
- 40 duplicate-mesh groups covering 6,616 tris — the repeated window panes.
  Not worth instancing: the app's loader merges the whole asset into the shared
  `BatchedMesh` anyway, so join-per-material captures the same win with no
  node overhead.
- 0 textures. Vertex attributes: POSITION + NORMAL only.
- Over-tessellation: at the landmark near distance (184.09 m) one pixel is
  0.124 m of world. The only curves are the 10-segment columns (r 0.80 m,
  chord error 0.039 m) and 8-segment tree pucks — both already under a pixel,
  so **step 4 (retessellation) was skipped**: halving them would land the
  colonnade at 5 segments, which is a silhouette change on the asset's single
  strongest recognition cue.

## 3. Phase B — the four-variant table (the judgment call)

`GLB-OPTIMIZE-PROMPT` §3.3 warns that the limited dissolve should be skipped on
assets with large coplanar ring bands. **This asset is nothing but ring bands** —
plinth, three rustication reveals, belt course, main cornice, attic balustrade,
top cornice and two north parapets, each following the whole footprint. Rather
than assume, all four weld × dissolve combinations were built and packed:

| variant | mid GLB | packed (`-c -km -kn -noq`) | packed gzip -9 |
|---|---|---|---|
| weld + dissolve | 647,676 | 321,348 | 185,055 |
| **weld, no dissolve** | 672,448 | **330,680** | **156,277** |
| no weld, dissolve | 722,416 | 351,104 | 194,594 |
| neither | 745,864 | 357,788 | 161,223 |

Readings:

- **Weld pays, unambiguously**: 26,292 → 7,908 verts before the join, and it is
  worth ~27 KB packed on both dissolve settings. (Per
  `sf3d-weld-heuristic-is-not-bevel`, this was measured rather than predicted
  from the bevel count.)
- **The dissolve is a false economy here.** It wins 9,332 bytes raw (2.8%) and
  *loses* 28,778 bytes gzipped (18%) — it destroys the regular vertex ordering
  that meshopt and the gzip pass both exploit. Note that no-weld/no-dissolve
  gzips smaller than weld+dissolve.
- Against a 2.8% raw win, the dissolve carries the documented sliver hazard on
  exactly this asset class: a strictly-coplanar dissolve merges each ring band
  into one annulus ngon, whose re-triangulation emits hairline slivers that pass
  an area-based degeneracy test and only surface as
  `invalid_or_nonunit_loop_normal_count` in the *packed* file — after the
  shipping swap. **Declined.** The chosen variant is **weld, no dissolve**.

Other Phase B steps:

- Interior-face removal: **0 faces**. No object qualifies as an occluder —
  every solid is authored on the 9.08 deg grid, so its world AABB is much larger
  than the solid and nothing reaches the 95% fill threshold. The occluder rule
  (closed solids only) was left intact.
- Join per material: 548 → 11 objects, one per material, all names preserved.
- `optimize.py` was adapted in two places: two switches (`--no-weld`,
  `--no-dissolve`) so the table above could be measured, and the dissolve
  rewritten from the edit-mode operator to `bmesh.ops.dissolve_limit` — 548
  objects × (mode_set + select_all + operator) took longer than the entire rest
  of the pass.

## 4. Phase C — packing

```
npx gltfpack@0.24 -i mid.glb -o out.glb -c -km -kn -noq
```

`-km -kn` verified on the output: all 11 material names survive, including both
`_Glow` names, which is what keeps the night layer alive. `-noq` per the repo
standard — and the shipped file confirms why it matters: the stage-2 contract
validator still reports `transforms_applied: true` and
`unexpected_geometry_or_objects: []`, which a quantized build would fail on the
dequantize node transform.

672,448 → 330,680 bytes (−50.8%).

## 5. Gates

| Gate | Result | Evidence |
|---|---|---|
| **G1 Contract** | PASS | material set identical (11), both `_Glow` names separate, no `Toy_body`, no manifest-named nodes to preserve |
| **G2 Geometry** | PASS | bbox identical to 4 dp (tol 0.123 m); origin (0,0,0); 11/11 signed volumes positive; 22,500 rays, 20,010 hits, **0 flipped (0.000%)** |
| **G3 Round-trip** | PASS | Blender re-import clean; `g3check` with pinned three@0.185.1: `ok:true`, 11 meshes, 13,624 tris, 11 materials, bbox 122.7264 × 33 × 84.8953 |
| **G4 Appearance** | PASS | mean abs RGB delta: day near 0.100%, day far 0.094%, night near 0.106%, night far 0.101%, elevations 0.041–0.139% — all far under the 4%/2% gates. See §6 |
| **G5 Draw submeshes** | PASS | 548 → 11 |
| **G6 Size** | PASS | −64.8% raw against a 60% target |
| **G7 GPU budget** | n/a | bake mode off |
| **G8 Hygiene** | PASS | re-import object count 11, no foreign geometry, deterministic re-run reproduces the output, no `.blend1` left in `optimize/` |

## 6. What the diffs actually show

`renders/contact_sheet.png` — rows input / optimized / diff ×8, columns N E S W;
plus day and night at near (1.5× long axis) and far (6×).

Looked at, not just measured. The amplified diff is faint noise in three places
and nowhere else:

1. **The metal hip roof**, strongest of the three. The five hip bars overlap by
   design (that is what makes their 35 deg planes meet on the correct 45 deg hip
   line), so their interior surfaces sit near-coincident. The weld nudges which
   of two co-located triangles wins a given sample, and Cycles' anti-aliasing
   turns that into speckle. No silhouette change; no change in which surface is
   visible.
2. **The attic glow band**, a one-pixel outline around each pane — the weld
   removed duplicate corner vertices, so the edge falls a fraction differently
   under AA.
3. **The three arched entrances**, same one-pixel outline for the same reason.

Nothing is missing, nothing moved, no shading flipped, and there is no change a
player could notice at any distance the app uses.

## 7. Size honesty — the gzip line

The raw file shrank 2.84× but the **gzipped** file grew 5.5% (148,055 →
156,263). This is expected and not a regression: meshopt output is already
entropy-coded, so a second compression pass has nothing left to find, whereas
the uncompressed float attributes of the input gzip extremely well. What
improves is what the runtime actually pays — bytes on disk and over a CDN that
serves `model/gltf-binary` uncompressed, plus parse and GPU upload cost. The
repo budget is **≤ 500 KB compressed on disk** (AGENTS.md); the shipped file is
**323 KB**.

## 8. Shipping swap

- `optimize/input/50-united-nations-plaza.glb` — byte-identical archive of the
  pre-optimize asset (939,600 B, verified with `cmp`).
- `optimize/50-united-nations-plaza.optimized.glb` — the winner.
- Copied over `artifacts/50-united-nations-plaza/50-united-nations-plaza.glb`.
- The stage-2 contract validator was re-run **on the shipped file**: overall
  PASS, 13,615 tris, dims unchanged, `transforms_applied` true,
  `negative_signed_volume_objects: []`, 0 flipped rays.
- `../validation.json` and `../REPORT.md` now carry the shipped numbers, so the
  integration stage writes its manifest entry from reality.
