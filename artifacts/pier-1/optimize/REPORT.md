# Pier 1 — optimize report (stage 4)

`GLB-OPTIMIZE-PROMPT.md` v2 run against `artifacts/pier-1/`.
`ASSET_CLASS: landmark` · `ALLOW_MESHOPT: yes` · `ALLOW_BAKE: no`.

Toolchain: Blender 5.2.0 LTS (headless), `npx gltfpack@0.24`, node + `three@^0.185.1`
(`g3check/`), python3 + Pillow, gzip.

## Metrics

| | input | shipped |
|---|---|---|
| Raw bytes | 1,077,372 (1,052.1 KB) | **337,088 (329.2 KB)** |
| Gzip-9 bytes | 153,437 (149.8 KB) | 162,414 (158.6 KB) |
| Objects | 792 | 15 |
| Draw submeshes (primitives) | 798 | **16** |
| Triangles | 13,330 | 13,330 |
| Vertices | 26,430 | 8,290 after weld (26,652 as re-expanded on import) |
| Materials | 10, two `_Glow` | identical set |
| bbox dims | 215.4308 × 185.429 × 15.4 | identical |
| bbox min Z | −2.6 | identical |

**68.7% smaller raw**, against a 60% target. Draw submeshes fall 50×.

Gzip goes *up* by 8.8 KB, which is expected and not a regression: meshopt output is
already entropy-coded, so gzip has nothing left to find. The contract's cap
(`sf-asset-check` §7) is 500 KB compressed on disk, and 329 KB clears it.

## Waste census (Phase A) and what each pass was worth

| Finding | Size | Technique | Result |
|---|---|---|---|
| 18,140 coincident vertex pairs | — | per-object weld ≤ 1 mm | verts 26,430 → 8,290 |
| 792 objects across 10 materials | 798 primitives | join per material | 15 objects / 16 primitives |
| 0 degenerate triangles | — | — | nothing to do |
| 0 provably-buried interior faces | — | occluder rule (closed solids only) | nothing removed |
| Over-tessellation | 1 px = 0.218 m at the 323 m near distance | — | the only curves are 6- and 10-segment bollards, vents and lamp globes, all already below the threshold; no retessellation |

The whole win is **object-count overhead**, which is what a 792-object procedural build
costs. Triangles are unchanged, and that is correct: nothing here was redundant geometry,
it was redundant *nodes and accessors*.

## Judgment call — the limited dissolve was SKIPPED

`GLB-OPTIMIZE-PROMPT` §3 step 3 says to skip it "entirely on assets with large coplanar
ring bands". Pier 1 is made of them: the 234 m deck slab, the shed plinth, the shed
parapet coping (a genuine closed annulus produced by `rim()`), and the 200 m monitor
spine all carry perfectly coplanar top and bottom faces running the whole length of the
pier. A strictly-coplanar dissolve merges each into one annulus ngon, and re-triangulating
an annulus emits slivers tens of metres long and fractions of a millimetre wide —
invisible, clean under an area-based degeneracy test, and fatal to the stage-2 contract
validator only *after* the shipping swap, because gltfpack re-emits the stored normals
that Blender would otherwise recompute and hide.

On `350-brannan` the same step was worth 30 triangles (0.4%). Here it would be worth less,
against the worst failure mode in the whole procedure. `DISSOLVE = False` in `optimize.py`,
with the reasoning inline.

## Packing

```
npx gltfpack@0.24 -i pier-1.mid.glb -o pier-1.optimized.glb -c -km -kn -noq
```

`-km -kn` keep the material and node names the loader treats as API — without `-km`,
gltfpack merges identical-parameter materials across the `_Glow` boundary and silently
kills the night layer. `-noq` (no quantization) is the repo standard and is what
`pipeline/compress-assets.mjs` produces; verified on the output that both `_Glow`
materials survive as separate materials.

## Gate results

| Gate | Result | Evidence |
|---|---|---|
| G1 Contract | **PASS** | material set identical (10, incl. `Toy_glass_Glow` and `Toy_glassl_Glow` separate); no `Toy_body`; no manifest-named nodes to preserve |
| G2 Geometry | **PASS** | bbox identical to 1e-4 m; origin identical; no inverted solids; 0 / 22,500 flipped rays |
| G3 Round-trip | **PASS** | re-imports in Blender; `g3check` (pinned three 0.185) reports `{"ok":true,"meshes":16,"tris":13330}` with the correct bbox and no decode errors |
| G4 Appearance | **PASS** | worst mean 0.396% (night far), best 0.0034% (day near); gates are ≤ 2% far / ≤ 4% near |
| G5 Draw submeshes | **PASS** | 798 → 16 |
| G6 Size | **PASS** | −68.7% raw, against a 60% target |
| G7 GPU budget | n/a | `ALLOW_BAKE: no` |
| G8 Hygiene | **PASS** | re-import object/material counts match; deterministic re-run reproduces the output; no `.blend1` left |

### G4 in words

Day near and far are indistinguishable (0.003% / 0.005% mean). The two night frames carry
the largest deltas — 0.34% near, 0.40% far, max pixel 101 — and eyeballing the stacked
pair shows why: identical silhouette, identical lit-clerestory pattern on both flanks,
identical roof and solar spine. The delta is Cycles sampling noise (the A/B rig runs 64
samples with denoising off) plus a sub-pixel shift, amplified on a nearly black frame
where a small absolute change is a large relative one. Nothing is missing, nothing moved,
and there is nothing here a player would notice.

## Shipping swap

`pier-1.optimized.glb` copied over `artifacts/pier-1/pier-1.glb`. The pre-optimize
original is archived byte-for-byte at `optimize/input/pier-1.glb`. `validation.json` and
the parent `REPORT.md` are updated to the shipped numbers so the integration stage writes
its manifest entry from reality.
