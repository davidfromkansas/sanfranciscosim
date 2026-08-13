# 543 Presidio Blvd — optimize pass (stage 4)

`GLB-OPTIMIZE-PROMPT.md` run against `artifacts/543-presidio-blvd/`.
`ASSET_CLASS: landmark` · `ALLOW_MESHOPT: yes` · `ALLOW_BAKE: no`.

**Result: 184,296 → 87,484 bytes raw (−52.5%), 63 → 9 draw submeshes (−86%),
2,848 triangles unchanged, every acceptance gate PASS.** The optimized file is
now the shipping `artifacts/543-presidio-blvd/543-presidio-blvd.glb`; the
pre-optimize original is archived at `optimize/input/543-presidio-blvd.glb`.

One finding worth carrying back to the prompt: **for an asset this small,
meshopt compression makes the raw file 52% smaller but the *gzipped* file 87%
larger.** Details and reasoning in §4.

## Toolchain

| Tool | Version |
|---|---|
| Blender | 5.2.0 LTS (fbe6228777e7, 2026-07-14) |
| gltfpack | `npx gltfpack@0.24` (pinned) |
| three (g3check) | as pinned in `tools/glb-optimize/g3check/package.json` |
| Python | 3.9 + Pillow 11.3.0 |

Scripts are adapted copies of `tools/glb-optimize/`. The only edit to
`diff_ab.py` was the contact-sheet title, which still read "St Marys Cathedral"
in the generic copy.

## Metrics

| | Input | Output | Δ |
|---|---|---|---|
| File, raw | 184,296 B | **87,484 B** | **−52.5%** |
| File, gzip −9 | 30,524 B | 57,162 B | **+87.3%** (see §4) |
| Triangles | 2,848 | 2,848 | 0 |
| Vertices | 5,868 | 5,350 | −8.8% |
| Mesh objects | 63 | **9** | −86% |
| Draw submeshes (primitives) | 63 | **9** | −86% |
| Materials | 9 | 9 | identical set |
| bbox dims | 17.1972 × 17.7268 × 9.55 | 17.1972 × 17.7268 × 9.55 | 0 |
| bbox min | (−8.5986, −8.8634, 0.0) | (−8.5986, −8.8634, 0.0) | 0 |
| Origin offset XY | (0, 0) | (0, 0) | 0 |

## Phase A — waste census

`inspect.json`. 63 objects, 63 primitives, 2,848 tris, 5,868 verts, no textures,
no UV layers, `NORMAL` only.

| Waste | Measured | Technique | Predicted saving |
|---|---|---|---|
| Object/primitive overhead — 63 nodes and accessors for 9 materials | 63 → 9 possible | join per material | the dominant win: node + accessor + primitive overhead |
| Unwelded coincident verts | 4,320 candidate pairs | per-object weld ≤ 1 mm | ~40% of verts |
| Duplicate mesh geometry (19 window sills, 19 fills at 44 tris each) | 1,120 "redundant" tris | none — they are at different positions and joining per material already removes the node overhead. Instancing 44-tri meshes is not worth an extra node level. | 0 tris |
| Degenerate faces | 0 | — | 0 |
| Interior buried faces | 0 removable | occluder rule: no mesh here is a closed solid that provably buries another's faces | 0 |
| Over-tessellated curves | none — the asset has no curved shells | — | 0 |

## Phase B — geometry cleanup

`optimize.py` → `mid.glb`, stats in `phaseb_stats.json`.

| Step | tris | verts |
|---|---|---|
| input | 2,848 | 5,868 |
| weld ≤ 1 mm + degenerate | 2,848 | 1,548 |
| interior faces | 2,848 | 1,548 |
| limited dissolve 0.05° | 2,848 | 1,548 |
| join per material | 2,848 | 1,548 |

Joins: `Toy_trim` 23→1, `Toy_glass` 19→1, `Toy_red` 8→1, `Toy_glass_Glow` 5→1,
`Toy_stone` 3→1, `Toy_brick` 2→1. `Toy_white`, `Toy_ink` and `Toy_trim_Glow`
already had one user each.

**Triangles did not move at any step, and that is the correct answer here.** The
asset is built entirely from closed beveled prisms; there is no coplanar
redundancy for a 0.05° limited dissolve to find, no curved shell to retessellate,
and no buried interior face that passes the closed-solid occluder rule. The
weld's 5,868 → 1,548 vertex drop is real and is where the file-size win comes
from — it is duplicated corner vertices inside each prism, not geometry.

Per-object signed volumes all positive after the joins; `inverted_solids: []`.

## Phase C — packing

```
npx gltfpack@0.24 -i mid.glb -o 543-presidio-blvd.optimized.glb -c -km -kn -noq
```

`-km -kn` mandatory (glow-ness is name-only; without `-km` gltfpack would merge
`Toy_glass_Glow` into `Toy_glass` and silently kill the night layer). `-noq`
mandatory for this repo — the runtime merge paths need float32 attributes, and
quantization also breaks the stage-2 validator's `transforms_applied` and
`no_unexpected_objects` checks. Verified on the output, not trusted from the
flags: material name set identical, bbox identical, `EXT_meshopt_compression`
present, no `KHR_mesh_quantization`.

### §4 — the gzip inversion

| | raw | gzip −9 |
|---|---|---|
| input (uncompressed float32 GLB) | 184,296 | 30,524 |
| mid.glb (Phase B, uncompressed) | 153,560 | 38,614 |
| output (meshopt) | **87,484** | 57,162 |

Meshopt entropy-codes the vertex buffers, so the output is close to
incompressible and gzip has almost nothing left to remove. On a large asset the
meshopt file still wins on the wire; on a 2,848-triangle house it does not — a
CDN serving gzip or brotli would transfer **57 KB compressed instead of 30 KB**.

**Shipped meshopt anyway, deliberately.** `sf-asset-check` §8 and
`pipeline/compress-assets.mjs` make meshopt compression a *mandatory* intake step
for every GLB under `app/public/sf-assets/`, the loaders register
`MeshoptDecoder` unconditionally, and `compress-assets.mjs` skips files that
already carry `EXT_meshopt_compression` — so an uncompressed file would either be
compressed later anyway or stand out as the one exception in the tree. A 27 KB
wire delta on one house is not worth becoming that exception. Recording the
measurement here so the repo has the data point: **the meshopt intake rule is
probably worth a size floor**, below which the uncompressed file is the smaller
one on the wire. Every landmark shipped so far is far above that floor; this is
the first asset small enough for it to matter.

Also worth noting against the prompt's headline results (49→9 KB etc.): those
were measured with quantization on. `-noq` gives a materially smaller headline
win, exactly as the prompt's own §4 note says.

## Phase D — bake

Not run. `ALLOW_BAKE: no`, and the asset has no texture-bakeable relief worth the
contract exception.

## Phase E — A/B verification

`render_ab.py` on both files with an identical rig (42° elevation, 45° azimuth,
40° FOV, Cycles 64 samples, denoising off), then `diff_ab.py`.
Landmark distances: near = 1.5 × long axis = 26.6 m, far = 6 × = 106.4 m.

| View | mean abs RGB delta | max px delta | gate |
|---|---|---|---|
| day near | 0.012% | 19 | ≤ 4% PASS |
| day far | 0.017% | 13 | ≤ 2% PASS |
| night near | 0.163% | 88 | ≤ 4% PASS |
| night far | **0.285%** | 90 | ≤ 2% PASS |
| elevation N | 0.019% | 30 | PASS |
| elevation E | 0.049% | 30 | PASS |
| elevation S | 0.064% | 40 | PASS |
| elevation W | 0.016% | 33 | PASS |

**Looked at the diffs.** At 8× amplification every one is scattered speckle along
lit window edges, the porch soffit and the eave line — Cycles sampling noise from
re-rendering with denoising off, not a geometry change. No missing element, no
silhouette change, no shading artifact, no material swap. The night views carry
the largest numbers precisely because they are the noisiest: an emissive surface
against a near-black background is where a stochastic renderer disagrees with
itself most. Nothing here a player would notice.

## Gate results

| Gate | Result | Evidence |
|---|---|---|
| **G1** Contract — material set identical, `_Glow` separate, node names intact | **PASS** | `validation.json` `G1_materials_identical: true`; 9 in, 9 out, same names; `Toy_glass_Glow` and `Toy_trim_Glow` still distinct primitives. No `Toy_body` (landmark). |
| **G2** Geometry — bbox ≤ max(1 cm, 0.1%), origin ≤ 1 cm, volumes positive, flips ≤ 0.15% | **PASS** | bbox and origin **bit-identical**; 9/9 signed volumes positive, `inverted_solids: []`; ray test 0 flipped of 17,969 hits (0.000%) |
| **G3** Round-trip — Blender AND pinned-three GLTFLoader | **PASS** | Blender re-import clean; `g3check` `G3-OK {"ok":true,"meshes":9,"tris":2848,...}`, no decode errors |
| **G4** Appearance — day+night × near+far | **PASS** | max 0.285% against a 2% gate; diffs are render noise (above) |
| **G5** Draw submeshes ≤ input | **PASS** | 63 → 9 |
| **G6** Size reduced | **PASS on raw (−52.5%)**, with the gzip caveat in §4 recorded rather than hidden | 184,296 → 87,484 B |
| **G7** GPU budget | n/a — bake mode off | |
| **G8** Hygiene — no foreign geometry, deterministic, no `.blend1` | **PASS** | re-import object count 9 = expected; scripts are deterministic (fixed seeds, no time/random); no `.blend1` written |

## Shipping swap

`543-presidio-blvd.optimized.glb` copied over
`artifacts/543-presidio-blvd/543-presidio-blvd.glb`. The stage-2 contract
validator (`validate_543_presidio_blvd.py`) was then **re-run against the swapped
file** — not assumed — and returns `overall: PASS` with all 16 checks true,
2,848 triangles, 9 objects, dims 17.1972 × 17.7268 × 9.55, crest 9.55,
31,500 rays / 0 flipped. The artifact's `validation.json` and `REPORT.md` now
carry the shipped numbers.

Pre-optimize original archived byte-for-byte at
`optimize/input/543-presidio-blvd.glb` (184,296 B, verified with `cmp`).
