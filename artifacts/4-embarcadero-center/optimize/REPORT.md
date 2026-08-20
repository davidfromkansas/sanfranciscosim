# Four Embarcadero Center — optimize report (stage 4)

`docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md` run on
`artifacts/4-embarcadero-center/` with the pipeline defaults:
`ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`.

**Result: 1,306 KB → 466 KB raw, −64.3%. 882 primitives → 10. All eight gates PASS.**
The optimized file is now the shipping `4-embarcadero-center.glb`; the pre-optimize
original is archived at `optimize/input/4-embarcadero-center.glb`.

## Headline metrics

| | input | shipped | Δ |
|---|---|---|---|
| raw bytes | 1,337,932 | **477,540** | **−64.3%** |
| gzip-9 bytes | 169,281 | 205,126 | +21.2% (see §"gzip is not the budget") |
| triangles | 17,904 | 17,904 | 0 |
| vertices | 34,813 | 10,662 | **−69.4%** |
| mesh objects | 869 | 9 | −99.0% |
| glTF primitives | 882 | 10 | −98.9% |
| materials | 9 | 9 | 0 |
| bbox (m) | 73.0216 × 51.9818 × 179.0000 | identical to 4 dp | 0 |
| origin offset | (0.3098, 0.0000) | identical | 0 |

## Toolchain

Blender 5.2.0 LTS (`fbe6228777e7`, macOS) · `npx gltfpack@0.24` ·
node + the pinned three in `g3check/package.json` · python3 + Pillow · gzip -9.

## Phase A — waste census (`inspect.json`)

| Finding | Count | Verdict |
|---|---|---|
| Mesh objects sharing a material | `Toy_glass` 673, `Toy_glassl_Glow` 155, `Toy_steel` 19, `Toy_cream` 14, `Toy_sand` 13, `Toy_ink` 5 | **the whole story** — 882 primitives of node/accessor overhead for 17,904 triangles |
| Duplicate mesh groups | 35 groups, 11,172 redundant triangles | left alone: they are the window panes, and joining them per material collapses the overhead anyway |
| Coincident vertex pairs | 24,151 | mostly *within* objects (bevelled prism corners); a per-object weld recovers 24,151 → 10,662 verts |
| Degenerate triangles | 2 | from the build's bevel + remove_doubles; Phase B's `dissolve_degenerate` clears them, and **they are the reason pack-only fails** (below) |
| Interior faces buried in closed solids | 0 removed | nothing provably buried: the fins abut the core but do not nest inside its AABB |
| Over-tessellated curves | 4 cooling towers, 14 segments | kept: chord error is already under the 0.181 m one-pixel-at-near threshold |

Vertex attributes are POSITION + NORMAL only. No textures, no UVs, no colours.

## Phase B — the variant table

Six variants, each packed identically with `gltfpack@0.24 -c -km -kn -noq`:

| variant | raw | gzip-9 | prims | contract |
|---|---|---|---|---|
| pack only (Phase B skipped) | 848,420 | **177,137** | 882 | **FAIL** — 2 degenerate triangles |
| degenerate only | 894,300 | 244,760 | 882 | — |
| join only | 491,932 | 204,845 | 10 | — |
| **weld + degenerate + join** | **477,512** | 205,156 | **10** | **PASS** |
| dissolve + join | 456,944 | 213,460 | 10 | — |
| weld + degenerate + dissolve + join | 439,892 | 208,285 | 10 | **FAIL** — 1 degenerate triangle |

Two judgment calls came out of this table.

**1. Pack-only loses here, unlike on `fulton-plaza`.** The known trap is that the
Blender import → re-export round-trip can cost more bytes than every Phase-B step
saves, so a pack-only row must always be measured. It was, and on this asset it
lost decisively on raw bytes (848 KB against 478 KB) because this model's waste is
*object-count overhead*, not vertex-layout inefficiency — 882 primitives for
17,904 triangles. It also **fails the contract validator**: the build's two
degenerate triangles survive gltfpack, and Phase B's degenerate pass is what
removes them. Reverting Phase B under §11 was therefore not available.

**2. The limited dissolve was measured and rejected — as §3.3 predicts.** It is
worth 37,620 raw bytes (−7.9%) and 344 triangles, but this asset carries **14
large coplanar ring bands** (the core parapet, the base trim band and twelve fin
caps). Exactly as documented, re-triangulating a merged annulus emits a hairline
sliver: the `dissolve + join` build lands **1 degenerate triangle** in the packed
file and fails `no_degenerate_geometry`. Shipping 8% more bytes is the cheap side
of that trade. `optimize.py` now takes `--no-weld` / `--no-degenerate` /
`--no-interior` / `--no-dissolve` / `--no-join`, so the whole table is five
Blender runs plus six gltfpack calls; the shipped build is `--no-dissolve`.

Per-step geometry deltas for the shipped variant (`phaseb_stats.json`):

| step | tris | verts |
|---|---|---|
| input | 17,904 | 34,813 |
| weld + degenerate | 17,904 | 10,662 |
| interior faces | 17,904 | 10,662 |
| join per material | 17,904 | 10,662 |

## Phase C — packing

`npx gltfpack@0.24 -i mid.glb -o 4-embarcadero-center.optimized.glb -c -km -kn -noq`

`-km -kn` keep the nine material names distinct, which is what keeps
`Toy_glassl_Glow` and `Toy_red_Glow` on the night layer — gltfpack would otherwise
merge identical-parameter materials across the `_Glow` boundary and silently kill
the glow. `-noq` is the repo standard (float32 attributes for the merge paths, and
what `pipeline/compress-assets.mjs` produces); the output carries
`EXT_meshopt_compression`, so `compress-assets.mjs` will skip it at ship time.

## gzip is not the budget

The shipped file is 21% *larger* gzipped than the input, and 16% larger than the
pack-only variant. That is meshopt doing its job: it already entropy-codes the
vertex streams, so there is less left for gzip to find, and the comparison flatters
the loosest file. The numbers that matter here are

- **raw bytes on disk**, which is what `AGENTS.md`'s "≤ 500 KB compressed on disk"
  landmark budget measures — 466 KB **passes**, and pack-only's 829 KB would not; and
- **GPU vertex memory**, which follows the vertex count: 34,813 → 10,662, −69%.

## Phase E — A/B verification

Same rig, input against output, day and night at near (1.5× long axis = 268.5 m)
and far (6× = 1,074 m), plus the four orthographic elevations.

| view | mean abs RGB Δ | max px Δ | gate |
|---|---|---|---|
| day near | 0.062% | 25 | ≤ 4% |
| day far | 0.044% | 12 | ≤ 2% |
| night near | **0.338%** | 45 | ≤ 4% |
| night far | 0.291% | 44 | ≤ 2% |
| elevation N / E / S / W | 0.013 / 0.131 / 0.073 / 0.097% | 16–32 | — |

Looked at, not just measured: `renders/contact_sheet.png` and
`renders/ab_night_near.png`. The ×8-amplified diffs are black except for
single-pixel speckle along window-pane edges and the fin reveals — the sub-pixel
consequence of welding coincident corner vertices, plus EEVEE sampling noise, which
is why night (dense small emissive rectangles on a dark field) scores an order of
magnitude above day. Nothing is missing, no silhouette moves, no shading changes,
the crown rings and the aviation bead are identical, and there is nothing here a
player could notice.

## Gate results

| Gate | Result | Evidence |
|---|---|---|
| **G1** contract | **PASS** | material set identical (9, same names); `Toy_glassl_Glow` / `Toy_red_Glow` still separate; no `Toy_body`; no manifest-referenced node names on this asset |
| **G2** geometry | **PASS** | bbox identical to 4 dp; origin identical; 9/9 signed volumes positive; 0/31,500 flipped visible faces; 0 non-unit loop normals |
| **G3** round-trip | **PASS** | Blender fresh-scene re-import PASS; `g3check` → `G3-OK {"ok":true,"meshes":10,"tris":17904,…}` |
| **G4** appearance | **PASS** | max 0.338% against a 4%/2% budget; visual review above |
| **G5** draw submeshes | **PASS** | 882 → 10 |
| **G6** size | **PASS** | −64.3% raw against a 60% target |
| **G7** GPU budget | n/a | `ALLOW_BAKE: no`, no textures added |
| **G8** hygiene | **PASS** | re-import object count 9 = expected; no foreign geometry; deterministic scripts committed; no `.blend1` |

## Deliverables

`input/4-embarcadero-center.glb` (untouched archive) ·
`4-embarcadero-center.optimized.glb` (the winner, now also the shipping file) ·
`inspect.py optimize.py validate.py render_ab.py diff_ab.py g3check/` ·
`inspect.json phaseb_stats.json diffs.json validation.json` ·
`var/table.json` and the three candidate contract reports ·
`renders/` (A/B day/night × near/far, four elevations, ×8 diffs, contact sheet).

`mid.glb` is not committed — it is a reproducible intermediate, and
`optimize.py --no-dissolve` regenerates it byte-identically.
