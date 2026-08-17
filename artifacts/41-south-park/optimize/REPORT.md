# 41–43 South Park — optimize pass (stage 4)

`docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md` run against `artifacts/41-south-park/`.
`ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`.

**Result: all gates PASS. The optimized file is the shipping asset.**

## 1. Metrics

| | Input | Output | Δ |
|---|---|---|---|
| File, raw | 380,384 B (371.5 KB) | **173,108 B (169.1 KB)** | **−54.5%** |
| File, gzip -9 | 78,623 B (76.8 KB) | 125,781 B (122.8 KB) | +60.0% — see §5 |
| Triangles | 6,380 | 6,380 | 0 |
| Vertices | 12,822 | **10,577** | −17.5% |
| Objects | 72 | **13** | −81.9% |
| Draw submeshes (primitives) | 76 | **16** | **−78.9%** |
| Materials | 11 | 11 | identical set |
| bbox dims | 22.4556 × 22.4731 × 10.6 | 22.4556 × 22.4731 × 10.6 | 0 |
| bbox min | −11.2278, −11.2366, 0.0 | −11.2278, −11.2366, 0.0 | 0 |
| XY origin offset | 0.0, 0.0 | 0.0, 0.0 | 0 |

Vertices in the intermediate (pre-pack) mesh fell 12,822 → **3,330** on the weld
alone; gltfpack re-splits to 10,577 to satisfy per-primitive attribute layout,
which is expected and is not a regression — the file, the submesh count and the
GPU vertex-buffer layout are what matter.

## 2. Toolchain

| Tool | Version |
|---|---|
| Blender | 5.2.0 LTS (`fbe6228777e7`, 2026-07-14) |
| gltfpack | 0.24 (`npx gltfpack@0.24`) |
| node | v22.19.0 |
| three (g3check, pinned) | see `g3check/package.json` |
| python3 + Pillow | Pillow 11.3.0 |
| gzip | `gzip -9` via python `gzip.compress(..., 9)` |

## 3. Phase A — waste census

| Finding | Measured | Plan |
|---|---|---|
| Coincident vertex pairs (flat-shade splits) | **9,492** | weld — the single biggest win |
| Objects sharing one material | 7 groups covering 71 of 72 objects | join per material |
| Duplicate mesh groups | 16 groups, 588 redundant triangles | left alone: joining already removes the node overhead, and instancing 2-copy groups is not worth the complexity |
| Degenerate triangles (< 1 mm²) | 5 | deleted in Phase B |
| Buried interior faces | 0 found | the layered-relief stack buries its inner faces *inside* a host solid, but the occluder rule (closed solids only) correctly declines to guess |
| Over-tessellated curves | 1 px ≈ 22.7 mm at the 33.7 m near distance | the spa's 14-gon and the arch's 12-segment soffit are both above that chord error — not retessellated |

Biggest single object was `spa_shell` at 840 triangles (13% of the model) — a
0.16 m annulus wall whose bevel is disproportionate to its size. Left as-is: the
asset is 6,380 triangles against an 8,000 cap and a 27,000 repo limit, and the
spa is the roof's only recognition incident.

## 4. Phase B — geometry cleanup

| Step | Triangles | Vertices |
|---|---|---|
| input | 6,380 | 12,822 |
| weld ≤ 1 mm + degenerate delete | 6,380 | **3,330** |
| interior faces (0 removed) | 6,380 | 3,330 |
| limited dissolve @ 0.05° | 6,380 | 3,330 |
| join per material | 6,380 | 3,330 |

Joins: `Toy_roofd` 9 → 1, `Toy_steel` 16 → 1, `Toy_ink` 21 → 1, `Toy_glass`
10 → 1, `Toy_glass_Glow` 4 → 1, `Toy_glassl`+`Toy_ink` 2 → 1, `Toy_rust` 4 → 1.

**Asset adaptation — five objects skipped by the dissolve.** `parapet`,
`spa_shell` and the three cornice bands (`cornice_bed`, `cornice_dentil`,
`cornice_crown`) are closed ring bands whose top and bottom faces are coplanar
annuli — the cornice runs the whole frontage and returns over both bay
projections. This is the case §3 step 3 of the prompt warns about: a
strictly-coplanar dissolve merges each into one annulus n-gon, and
re-triangulating an annulus emits sub-millimetre slivers that only the *stage-2*
contract validator sees, two steps later and after the shipping swap. They are
skipped by name (the dissolve runs before the per-material join, so names are
still meaningful there). The dissolve found nothing anywhere else either — this
model is authored from beveled prisms with no coplanar-face redundancy to
recover — so the skip cost zero triangles.

`inverted_solids: []` after Phase B.

## 5. Phase C — packing, and the gzip question

```
npx gltfpack@0.24 -i mid.glb -o 41-south-park.optimized.glb -c -km -kn -noq
```

`-km -kn` keep material and node names, which are API here (`*_Glow` is the
night layer and glow-ness is name-only). `-noq` is the repo standard — it is what
`pipeline/compress-assets.mjs` produces, and quantization silently breaks the
kit/vehicle merge paths and fails the stage-2 validator on `transforms_applied`.

**Raw bytes fell 55% and gzipped bytes rose 60%.** Both are real. The meshopt
buffer is already entropy-coded, so it does not gzip further, while the
pre-optimize file was plain glTF float buffers that gzip compressed 4.8 : 1.
Over the wire the un-optimized file would have been about 47 KB smaller.

This is the same trade `165-south-park` recorded (−55% raw, +30% gzip), and the
answer is the same:

1. **Meshopt at intake is mandatory** (`AGENTS.md`, the asset pipeline section):
   every GLB entering `app/public/sf-assets/` is packed once with these exact
   flags, and `compress-assets.mjs` skips files that already carry
   `EXT_meshopt_compression`. Shipping an unpacked file would put this asset
   outside the one encoding every other landmark uses.
2. **The structural wins are the real ones.** 76 → 16 draw submeshes and 72 → 13
   objects is what the shared `BatchedMesh` cares about, and this asset streams
   in alongside twenty other South Park landmarks on one `loadRadius` centre.
3. 123 KB over the wire is comfortably inside the ≤ 500 KB per-landmark budget.

## 6. Phase E — A/B verification

Same rig, input vs output, day (glow α 0.12) and night (glow α 1.0, emission 6),
near (1.5 × long axis) and far (6 ×), plus four elevations.

| View | Mean abs RGB delta | Max pixel delta | Gate |
|---|---|---|---|
| day near | **0.0078%** | 27 | ≤ 4% |
| day far | **0.0121%** | 25 | ≤ 2% |
| night near | **0.0043%** | 32 | ≤ 4% |
| night far | **0.0100%** | 30 | ≤ 2% |
| elevation N | 0.0231% | 83 | — |
| elevation E | 0.0077% | 36 | — |
| elevation S | 0.0071% | 126 | — |
| elevation W | 0.0254% | 145 | — |

**Looked at, not just measured.** Input and output are indistinguishable at every
view. The residual is denoiser noise on the Cycles renders, not geometry: the
max-pixel outliers sit on bevel highlights and on the contact shadow's edge, and
they move between runs. No missing elements, no silhouette change, no shading
artifacts, no change to the glow layer in either state.

**One defect this pass found and sent back upstream.** The first A/B run showed
the spa's water surface speckling in `in_day_near` and clean in `out_day_near` —
a coincident face pair between the water's top cap and the glow disc, which Phase
B's weld happened to fix downstream. That was fixed in
`build_41_south_park.py` instead (the glow disc now bites 0.03 m into the water)
and the whole chain re-run, because the optimizer accidentally repairing a source
defect is not a reason to ship it. day-near delta fell 0.041% → 0.0078% as a
result.

## 7. Gate results

| Gate | Result | Evidence |
|---|---|---|
| **G1** contract | **PASS** | material set identical (11 → 11); `_Glow` materials separate; no `Toy_body`; node names preserved by `-kn` |
| **G2** geometry | **PASS** | bbox identical to 4 dp; origin offset 0.0; per-object signed volumes positive; ray-flip fraction 0.0% in **and** 0.0% out |
| **G3** round-trip | **PASS** | re-imports in Blender; `g3check` → `G3-OK {"ok":true,"meshes":16,"tris":6380,...}` with the full material list and the right bbox |
| **G4** appearance | **PASS** | table in §6; ≤ 0.026% everywhere against 2% / 4% gates; visually identical |
| **G5** draw submeshes | **PASS** | 76 → 16 |
| **G6** size | **PASS on raw, qualified on gzip** | −54.5% raw; see §5 |
| **G7** GPU budget | n/a | `ALLOW_BAKE: no` |
| **G8** hygiene | **PASS** | re-import object/material/bbox check in `phaseb_stats.json`; scripts deterministic; no `.blend1` left |

`validate.py` reports `grp_Toy_rust` as an open shell after the per-material
join. That is expected and is not a failure: the terrace slab and its three guard
rails are four separate closed solids that overlap by the build's 0.03 m `LAP`,
and welding a joined mesh of interpenetrating solids at 1e-4 produces
non-manifold edges. Every mesh that *is* closed has a positive signed volume, and
the ray test — which does not care about manifoldness — is clean at 0.0%.

## 8. Shipping swap

`41-south-park.optimized.glb` was copied over `artifacts/41-south-park/41-south-park.glb`.
The pre-optimize original is archived byte-for-byte at
`optimize/input/41-south-park.glb`. `artifacts/41-south-park/REPORT.md` and
`validation.json` carry the shipped numbers so the integration stage writes its
manifest entry from reality.
