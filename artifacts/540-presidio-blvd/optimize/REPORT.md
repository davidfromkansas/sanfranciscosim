# 540 Presidio Boulevard — GLB optimize pass

Stage 4 of `docs/asset-pipeline/ADDRESS-TO-ASSET.md`, run per
`docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md` with the defaults
(`ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`).

**Outcome: all gates PASS. The optimized GLB is now the shipping file.** The
pre-optimize original is archived byte-for-byte at
`optimize/input/540-presidio-blvd.glb`.

## Headline metrics

| | Input | Shipped | Δ |
|---|---|---|---|
| Raw bytes | 234,548 | **112,108** | **−52.2%** |
| Gzip-9 bytes | 35,950 | 71,428 | **+98.7%** (see §4 — expected, and not a regression) |
| Mesh objects / draw submeshes | 76 | **10** | −86.8% |
| glTF nodes | 76 | 10 | −86.8% |
| Vertices | 7,686 | **2,002** | −74.0% |
| Triangles | 3,712 | 3,690 | −0.6% |
| Materials | 10 | 10 | unchanged |
| bbox dims (m) | 16.6623 × 22.7566 × 11.5 | identical | 0 |
| bbox min (m) | −8.3312, −11.3783, 0.0 | identical | 0 |

Toolchain: Blender 5.2.0 LTS, `npx gltfpack@0.24`, node + the pinned three in
`g3check/`, python3 + Pillow, gzip -9.

## 1. Phase A — waste census (`inspect.py` → `inspect.json`)

| Finding | Count | Verdict |
|---|---|---|
| Coincident vertex pairs (≤ 1 mm) | 5,684 | the dominant waste: every bevelled corner duplicates its verts. Welding is free and lossless. |
| Duplicate mesh groups | 11 sills + further window groups, 1,500 redundant triangles | real, but they are *distinct objects at distinct positions* — the win is node/accessor overhead, taken by the per-material join, not by instancing (11 tiny sills are not worth a shared-mesh indirection). |
| Objects sharing one material | `Toy_trim` 29, `Toy_glass` 19, `Toy_brick` 8, `Toy_stone` 7, `Toy_glass_Glow` 4, `Toy_red` 3, `Toy_cream` 2, `Toy_mint` 2 | 76 → 10 by joining per material. The biggest structural win. |
| Degenerate triangles | 0 | nothing to reclaim — the build script's bevel already runs `dissolve_degenerate`. |
| Over-tessellated curves | none | this asset has no curved geometry at all. Step 4 of Phase B is a no-op, not a skip. |
| Vertex attributes | `NORMAL` only | no UVs, no colours, no tangents to prune. |

Predicted savings before executing: ~74% of vertices from the weld, 76 → 10
primitives from the join, no triangle change. That is exactly what happened.

## 2. Phase B — geometry cleanup (`optimize.py` → `phaseb_stats.json`)

| Step | Tris | Verts | Note |
|---|---|---|---|
| input | 3,712 | 7,686 | |
| 1–2a weld ≤ 1 mm + degenerate, per object | 3,712 | **2,002** | the whole vertex win, and lossless |
| 2b interior faces buried in closed solids | 3,712 | 2,002 | **0 removed — correctly** |
| 3 limited dissolve 0.05°, delimit material+sharp | 3,712 | 2,002 | 0 removed |
| 5 join per material | 3,712 | 2,002 | 76 objects → **10** |
| 7 normals audit | — | — | `inverted_solids: []` |

Two of those zeros are worth explaining rather than glossing:

**Interior-face removal found nothing, and that is the right answer.** The
occluder rule only admits *closed solids that fill ≥ 95% of their world AABB*.
Every mass in this asset is yawed +6.49° off the world axes, so a 11.44 × 19.72 m
rectangle presents a 13.57 × 20.86 m AABB and fills only 80% of it — below the
threshold. Nothing qualifies as an occluder, so nothing was deleted. The buried
back faces of the recessed window fills therefore survive. That is a few hundred
wasted triangles kept on purpose: the alternative is loosening a threshold that
exists precisely because a too-eager occluder test once ate real geometry.

**Limited dissolve removed nothing** because the triangle count is measured after
triangulation, and merging coplanar quads into ngons does not change how many
triangles they fan into. It still ran at 0.05°, not 0.5°, per the prompt's
hard-learned rule.

## 3. Phase C — packing (`gltfpack@0.24 -i mid.glb -o out.glb -c -km -kn -noq`)

All four flags as mandated: `-c` meshopt, `-km`/`-kn` keep material and node
names, `-noq` **no quantization**.

Verified on the output rather than trusted from the flags:

- `extensionsUsed: ["EXT_meshopt_compression"]` — and nothing else.
- Material name set identical to the input's, all ten. Critically,
  `Toy_glass_Glow` and `Toy_gold_Glow` are still separate materials: without
  `-km`, gltfpack merges identical-parameter materials across the `_Glow`
  boundary and silently kills the night layer.
- 10 nodes, 10 meshes, 10 primitives, node names intact
  (`grp_Toy_*`, plus `front_door` and `glow_lantern` which were singletons).
- No dequantize node transforms and no `Mesh_N` child splitting — the failure
  mode `-noq` exists to avoid. Confirmed by re-running the **stage-2 contract
  validator** on the shipped file: still `overall: PASS`, including
  `transforms_applied` and `no_unexpected_objects`.

gltfpack's reindex dropped **22 triangles** (3,712 → 3,690) as degenerate after
welding. Appearance impact is inside the Phase E numbers below.

## 4. On the gzip number — the one honest caveat

Raw bytes fell 52%, but **gzip-9 bytes roughly doubled**, 35,950 → 71,428.

That is not a regression, it is what meshopt is: `EXT_meshopt_compression`
entropy-codes the vertex and index buffers, so the result is already near-random
and gzip has nothing left to find. The input, by contrast, was 76 tiny meshes of
highly repetitive float data — ideal gzip fodder. The comparison the prompt's
own quoted results use (st-marys 257 → 42 KB, salesforce 924 → 156 KB) is raw
bytes, and on raw bytes this asset behaves normally.

It is also not optional. `.agents/skills/sf-asset-check/SKILL.md` §8 makes
`node pipeline/compress-assets.mjs` — which runs the identical
`-c -km -kn -noq` — a **mandatory** ship step for every GLB entering
`app/public/sf-assets/`, and `fairmont-san-francisco.glb` on disk already carries
`EXT_meshopt_compression`. Shipping the unpacked file would simply mean the same
pass runs later, on a file with 76 draw submeshes instead of 10.

What the pass actually buys at this size: **7.6× fewer draw submeshes, 3.8× fewer
vertices, half the raw bytes, and a faster parse** — with the wire cost for this
particular small asset going from ~36 KB to ~71 KB on a gzipping CDN. For an
11.5 m house on a 2,500 m `loadRadius` that is a rounding error against the
500 KB compressed budget.

## 5. Phase E — A/B verification (`render_ab.py`, `diff_ab.py` → `diffs.json`)

Input vs shipped, same rig, 42° aerial: day (glow alpha 0.12) and night
(emission, dusk world) at near (1.5× long axis = 34 m) and far (6× = 137 m),
plus four orthographic elevations. Contact sheet at
`renders/contact_sheet.png`, rows input / optimized / diff ×8.

| View | Mean abs RGB delta | Max pixel delta | Gate |
|---|---|---|---|
| day_near | **0.0391%** | 88 | ≤ 4% |
| day_far | **0.0413%** | 30 | ≤ 2% |
| night_near | **0.1651%** | 109 | ≤ 4% |
| night_far | **0.1924%** | 33 | ≤ 2% |
| elev_n / e / s / w | 0.0644 / 0.0894 / 0.0189 / 0.0083% | 152 / 50 / 34 / 25 | — |

Worst case is **0.19%** against a 2% gate — an order of magnitude of headroom.

**And having looked at the diffs, not just the numbers:** the amplified diff row
is black except for two things. Single-pixel anti-aliasing fringes along the roof
hips and the plinth edge, from the weld nudging shared vertices by sub-millimetre
amounts. And a faint speckle on the two lit window panes on the east front — the
`_Glow` shells at 12% day alpha, where a sub-millimetre shift changes how the
translucent pane composites over the glass behind it. The night views show the
same speckle slightly stronger, which is why night_near/far are the largest of
the eight and still under a fifth of one percent.

Nothing is missing, no silhouette moved, no shading artifact appeared, and there
is nothing here a player could notice at any distance the app ever uses.

## 6. Gate results

| Gate | Result | Evidence |
|---|---|---|
| **G1** Contract — material set identical, `_Glow` separate, node names intact | **PASS** | all 10 materials byte-identical by name; both `_Glow` materials survive `-km`; `front_door` / `glow_lantern` / `grp_Toy_*` names preserved. No `Toy_body` in this asset (landmark). |
| **G2** Geometry — bbox ≤ max(1 cm, 0.1%), origin ≤ 1 cm, volumes positive, flips ≤ 0.15% | **PASS** | bbox and origin **exactly** identical to 4 dp; all closed solids positive; ray test 22,500 rays, 18,726 hits, **0 flipped (0.0000%)** |
| **G3** Round-trip — Blender **and** pinned-three `g3check` | **PASS** | `G3-OK {"ok":true,"meshes":10,"tris":3712,...}` with `MeshoptDecoder`, no decode errors, only `EXT_meshopt_compression` |
| **G4** Appearance — day+night × near+far | **PASS** | max 0.1924% vs 2% gate; visual description above |
| **G5** Draw submeshes ≤ input | **PASS** | 10 ≤ 76 |
| **G6** Size reduced | **PASS** on raw (−52.2%); **declared** on gzip (+98.7%) | §4. The remainder after Phase B is silhouette geometry: 3,690 triangles of chunky bevelled massing with no curves and nothing left to weld. |
| **G7** GPU budget | **N/A** | bake mode off (`ALLOW_BAKE: no`), no textures anywhere |
| **G8** Hygiene — no foreign geometry, deterministic, no `.blend1` | **PASS** | re-import object count 10 = expected; scripts are deterministic and committed; `mid.glb` intermediate removed; no `.blend1` |

## 7. Shipping swap

`540-presidio-blvd.optimized.glb` was copied over
`artifacts/540-presidio-blvd/540-presidio-blvd.glb`. The stage-2 contract
validator was then **re-run against the swapped-in file** and returned
`overall: PASS`, and `validation.json` and `REPORT.md` now carry the shipped
numbers (10 objects, 3,690 triangles, 112,108 bytes) so the integration stage
writes its manifest entry from reality rather than from the pre-optimize file.

Reproduce the whole pass:

```bash
cd artifacts/540-presidio-blvd/optimize
BL=/Applications/Blender.app/Contents/MacOS/Blender
"$BL" -b --python inspect.py  -- input/540-presidio-blvd.glb inspect.json
"$BL" -b --python optimize.py -- input/540-presidio-blvd.glb mid.glb phaseb_stats.json
npx gltfpack@0.24 -i mid.glb -o 540-presidio-blvd.optimized.glb -c -km -kn -noq
"$BL" -b --python validate.py -- input/540-presidio-blvd.glb 540-presidio-blvd.optimized.glb validation.json
(cd g3check && npm install && node check.mjs ../540-presidio-blvd.optimized.glb)
"$BL" -b --python render_ab.py -- input/540-presidio-blvd.glb renders/in
"$BL" -b --python render_ab.py -- 540-presidio-blvd.optimized.glb renders/out
python3 diff_ab.py
```
