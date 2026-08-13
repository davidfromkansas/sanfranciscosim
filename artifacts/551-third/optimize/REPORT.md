# 551-third — optimize pass report

Stage 4 of `docs/asset-pipeline/ADDRESS-TO-ASSET.md`, run per
`docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md` with the defaults:
`ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`.

**Result: all eight gates PASS.** `551-third.optimized.glb` is now the shipping
file at `artifacts/551-third/551-third.glb`; the pre-optimize asset is archived
byte-for-byte at `optimize/input/551-third.glb`.

## Metrics

| | Input | Output | Δ |
|---|---|---|---|
| Raw bytes | 613,056 | **252,408** | **−58.8%** |
| gzip -9 bytes | 96,387 | 168,664 | +75.0% (see below) |
| Triangles | 10,100 | 9,541 | −5.5% |
| Vertices | 20,508 | 16,266 | −20.7% |
| Objects / nodes | 147 | **14** | −90.5% |
| Draw submeshes (primitives) | 147 | **14** | −90.5% |
| glTF accessors | 351 | 42 | −88.0% |
| Materials | 14 | 14 | identical set |
| bbox dims | 41.80711 × 41.80711 × 6.6 | identical | 0 |
| Origin offset XY | 0.0, 0.0 | 0.0, 0.0 | 0 |

**On the gzip figure.** The optimized file gzips *worse* in relative terms
because meshopt output is already entropy-coded, while the unpacked input was
unusually gzip-friendly (ratio 0.16) — this asset is 147 near-identical extruded
prisms, which is close to the best case for a general-purpose compressor. The
meaningful comparison is against what actually ships: every landmark in
`app/public/sf-assets/landmarks/` is meshopt-encoded and gzips at 0.57–0.75, and
this asset now sits at 0.67 (252 KB raw / 169 KB gzip), squarely in that band and
between `380-brannan` (222/167 KB) and `101-grove` (421/267 KB). Well under the
500 KB budget in `AGENTS.md` on either measure. No action needed; recorded so the
number is not mistaken for a regression later.

## Phase A — waste census

`inspect.py` against the input:

| Finding | Size | Verdict |
|---|---|---|
| Object-count overhead: 144 objects across 11 materials joinable | 147 → 14 primitives | **the whole win** — executed |
| Coincident vertex pairs ≤ 1 mm | 15,436 | welded per object |
| Degenerate triangles | 544 | deleted |
| Duplicate mesh groups (34 groups, e.g. bollards, ribs, fascia slabs) | 4,820 redundant tris | **joined, not instanced** — see judgment calls |
| Interior faces buried in closed solids | 4 tris | deleted |
| Over-tessellated curves | none | the only curved things are 8-gon capsules and a 12-lobe scallop, already at minimum |
| Vertex attributes | POSITION + NORMAL only | nothing to prune; no UVs, no vertex colours, no textures |

The waste here was never triangles — it was 147 separate draw calls' worth of
node and accessor overhead on a model whose triangle count was already inside
budget. That is exactly what the join pass and meshopt address.

## Phases B–C

`optimize.py` (unmodified from `tools/glb-optimize/` — no per-asset constants
needed to change; the curve-retess step it skips for St Mary's hypar shell is a
no-op here for the reason in the census):

| Step | Tris | Verts |
|---|---|---|
| input | 10,100 | 20,508 |
| weld ≤1 mm + degenerate | 9,556 | 5,072 |
| interior faces | 9,552 | 5,072 |
| limited dissolve 0.05° | 9,552 | 5,072 |
| join per material | 9,552 | 5,072 |

Packing: `npx gltfpack@0.24 -i mid.glb -o out.glb -c -km -kn -noq` — the repo
standard. `-km -kn` keep the `_Glow` materials from being merged across the glow
boundary (glow-ness is name-only), `-noq` keeps float32 attributes so the
runtime merge path and the stage-2 contract validator both stay happy. The
output carries `EXT_meshopt_compression` and nothing else.

The re-export re-splits vertices by flat-shaded normal, which is why the
9,552-tri / 5,072-vert intermediate lands at 9,541 / 16,266 in the shipped file.
Triangle count differs by 11 between the Blender count and the loader count
(9,541 vs 9,552) — n-gon triangulation choice, not lost geometry; bbox and
material set are identical and G3 confirms the loader sees 9,552.

## Phase D

Skipped. `ALLOW_BAKE: no`, and the asset has no textures and no bakeable facade
relief worth 3× — its detail is all silhouette (umbrella edges, dispensers,
bollards) or flat colour.

## Phase E — A/B verification

Same rig, input vs output, Cycles, day (glow α 0.12) and night (α 1.0,
emission ≈ 6, dusk world), near = 1.5× and far = 6× long axis, plus four
elevations. Mean absolute RGB delta over foreground pixels:

| View | Mean Δ | Max px Δ | Gate |
|---|---|---|---|
| day near | 0.0204% | 167 | ≤ 4% PASS |
| day far | 0.0213% | 22 | ≤ 2% PASS |
| night near | 1.2154% | 142 | ≤ 4% PASS |
| night far | 1.4332% | 111 | ≤ 2% PASS |
| elevations N/E/S/W | 0.110–0.127% | 78–124 | PASS |

**Looked at, not just measured.** `renders/ab_night_near.png` and
`ab_day_near.png` are side-by-side input | output | ×6-amplified difference
strips. Both umbrellas keep their glowing yellow lightbar rings and the pecten
stays lit, so the `_Glow` split survived packing — that was the one thing worth
checking, since a `-km`-less pack would have silently merged the glow materials
away. The amplified night difference is Monte Carlo sampling noise spread evenly
over the dark apron, plus faint edge outlines where n-gon triangulation differs;
there is no missing element, no silhouette change and no shading artefact.

The night figures are an order of magnitude above the day ones purely because
the night frame is dark: the same absolute noise divided by a much smaller mean
luminance. Nothing a player would notice.

## Judgment calls

- **Joined the 34 duplicate mesh groups rather than instancing them.** §3.6 of
  the prompt allows either. The repeats here are small (bollards, ribs, fascia
  slabs — tens of triangles each) and the app's landmark loader merges every
  landmark down to one batched body plus one glow set anyway, so shared mesh
  data would be discarded at load. Joining wins on both file size and submesh
  count; instancing would have won nothing.
- **Kept all eight ribs per umbrella and the 12-lobe scallop.** Both are
  silhouette-defining at the aerial camera and both are already at their minimum
  segment counts.
- **G6 is 58.8% against a 60% aspiration.** The census accounts for the
  remainder: only 559 of 10,100 triangles were removable waste (degenerate and
  buried), and the other 9,541 are silhouette geometry the prompt protects.
  There is no further byte-level win available without touching the model's
  shape, which G4 and the contract forbid.

## Gate results

| Gate | Result | Evidence |
|---|---|---|
| G1 Contract — material set identical, `_Glow` separate, no `Toy_body` | **PASS** | `validation.json` `G1_materials_identical`; 14 in, 14 out, same names |
| G2 Geometry — bbox, origin, signed volumes, flip fraction | **PASS** | bbox delta 0; origin delta 0; 14/14 volumes positive; 22,500 rays, 10,253 hits, **0 flipped** |
| G3 Round-trip — Blender + pinned three | **PASS** | `G3-OK {"ok":true,"meshes":14,"tris":9552,...}`; only `EXT_meshopt_compression` |
| G4 Appearance — day+night × near+far | **PASS** | table above; visual description above |
| G5 Draw submeshes ≤ input | **PASS** | 14 ≤ 147 |
| G6 Size reduced | **PASS** | −58.8%; shortfall against the 60% aspiration justified above |
| G7 GPU budget | **n/a** | bake mode off |
| G8 Hygiene — no foreign geometry, deterministic, no `.blend1` | **PASS** | re-import 14 objects; re-run reproduces `mid.glb` and the packed output byte-for-byte (md5 `0e953014…` / `e0a841f8…`); zero `.blend1` files |

## Post-swap contract re-validation

The stage-2 contract validator was re-run against the **shipped** file:

```
VALIDATION {"result": "PASS", "failed": [], "tris": 9541, "dims": [41.807, 41.807, 6.6]}
```

14 objects, crest still exactly 6.600 m, min Z 0.0, XY centre 0.0/0.0, all 19
checks green. `artifacts/551-third/validation.json` and `REPORT.md` now carry the
shipped numbers.

## Toolchain

Blender 5.2.0 LTS (fbe6228777e7, 2026-07-14) · `gltfpack@0.24` via npx ·
node v22.19.0 with the pinned three in `g3check/package.json` · python3 with
Pillow 11.3.0 · gzip -9.
