# pier-17 — optimize report (GLB-OPTIMIZE-PROMPT v2)

Input: `optimize/input/pier-17.glb` (the approved stage-2 asset, archived
byte-for-byte). Output: `pier-17.optimized.glb` → shipped as
`artifacts/pier-17/pier-17.glb`. `ASSET_CLASS: landmark`,
`ALLOW_MESHOPT: yes` (`setMeshoptDecoder` present in `app/src/gltf.js` /
`app/src/assets.js`), `ALLOW_BAKE: no`.

Toolchain: Blender 5.2.0 LTS · gltfpack 0.24 (npx, pinned) · node 22.19.0 ·
pinned three via `g3check/` · python3 + Pillow.

## Phase A — inspection

| metric | input |
|---|---|
| raw bytes | 153,280 |
| gzip bytes | 31,324 |
| objects | 90 |
| primitives | 92 |
| triangles | 1,998 |
| vertices | 3,958 |
| degenerate tris | 0 |
| coincident vert pairs (export splits) | 2,779 |

Waste census: the vertex count is ~2× the geometry's need (glTF export
splits at every flat-shaded edge); 90 objects sharing 10 materials is pure
node/accessor overhead the join collapses; no degenerate faces; no buried
interiors worth hunting at 1,998 tris.

## Phase B — geometry cleanup (four-variant table)

Per the hard-learned rule, every variant is judged by bytes after packing,
with a pack-only control:

| variant | mid tris/verts | packed raw | packed gz |
|---|---|---|---|
| input (unpacked control) | 1,998 / 3,958 | 153,280 | 31,324 |
| A: pack only | — | 96,268 | 36,697 |
| B: weld+join (no dissolve), pack | 1,998 / 1,179 | 64,204 | 39,245 |
| C: full Phase B, pack | 1,998 / 1,179 | **57,784** | **36,234** |

- Weld (≤1 mm, per object) rejoined the export-split verts: 3,958 → 1,179.
- Limited dissolve at 0.05° was a **no-op** on this asset (identical counts)
  — and therefore harmless: the deck is a 243 m beveled ring, exactly the
  §3.3 sliver geometry, so the packed output was still put through the full
  stage-2 validator (below) to prove no manufactured degenerate geometry.
- Join-per-material: 90 objects → 13 meshes (no manifest-named nodes, no
  `Toy_body` in this asset).
- Signed volumes all positive after every step; `inverted: []`.

**Winner: variant C** — 62% raw reduction, best gz among packed variants.
(Note the gz row: meshopt data is high-entropy, so gz(packed) > gz(input
raw) at this asset's tiny size — but meshopt-on-intake is the repo standard
enforced by `pipeline/compress-assets.mjs`, and raw-on-disk is the budget
metric: 57,784 B ≪ 500 KB.)

## Phase C — packing

`npx gltfpack@0.24 -c -km -kn -noq` (repo standard: keep materials/names,
no quantization). Verified on the output, not the flags:

- material set identical (10, both `_Glow` intact) — **G1 PASS**
- bbox 233.9775 × 21.3 × 182.7369, min z 0 — identical to input — **G2 PASS**
- `g3check` (pinned three): loads, 13 submeshes, 1,998 tris, no decode
  errors — **G3 PASS**
- draw submeshes 92 → 13 — **G5 PASS**
- stage-2 contract validator re-run on the PACKED file
  (`optimize/validation.json`): **overall PASS**, 0 invalid loop normals,
  ray residual 0 — no post-pack slivers.

## Phase E — A/B appearance

`render_ab.py` day+night × near (1.5× long axis) + far (6×) + 4-elevation
sheet, input vs packed_c, same rig; `diff_ab.py` mean absolute RGB delta
ignoring background. Results: see `diffs.json` —

| pair | mean abs RGB | max px delta |
|---|---|---|
| day near | 0.014% | 89 |
| day far | 0.020% | 6 |
| night near | 0.061% | 76 |
| night far | 0.080% | 43 |
| elev n/e/s/w | 0.021 / 0.033 / 0.084 / 0.077% | ≤ 39 |

All within gates (≤2% far, ≤4% near). The 8x-amplified diffs show only
sub-pixel antialiasing speckle along silhouette edges; no missing elements,
no silhouette change, no shading artifacts — nothing a player would notice.
**G4 PASS.**

## Gates

| gate | result |
|---|---|
| G1 contract | PASS |
| G2 geometry | PASS |
| G3 round-trip | PASS |
| G4 appearance | PASS (max mean delta 0.084%) |
| G5 submeshes | PASS (92 → 13) |
| G6 size | PASS (153,280 → 57,784 raw, −62%) |
| G7 GPU (bake only) | n/a |
| G8 hygiene | PASS (re-import counts match; deterministic scripts committed; no .blend1) |

## Shipping swap

After all gates: `packed_c.glb` → `pier-17.optimized.glb` → copied over
`artifacts/pier-17/pier-17.glb`; original archived at
`optimize/input/pier-17.glb`; `validation.json` / REPORT tris+bytes updated
to shipped numbers.
