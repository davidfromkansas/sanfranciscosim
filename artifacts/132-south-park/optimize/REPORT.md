# 132 South Park — optimize pass (stage 4)

Run of `docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md` against
`artifacts/132-south-park/`. `ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`,
`ALLOW_BAKE: no`.

**All eight gates PASS. The optimized file is now the shipping GLB.**

## Metrics

| | Input | Shipped | Δ |
|---|---|---|---|
| Raw bytes | 276,436 | **126,760** | **−54.1%** |
| gzip -9 bytes | 36,565 | 72,612 | +98.6% (see note) |
| Triangles | 3,928 | 3,928 | 0 |
| Vertices | 8,576 | 8,569 | −7 |
| Objects | 108 | **11** | −89.8% |
| Draw submeshes (primitives) | 112 | **13** | −88.4% |
| Materials | 10 | 10 | 0 |
| bbox dims | 26.68437 × 26.70643 × 12.07 | identical | 0 |
| bbox min | −13.34218, −13.35322, 0.0 | identical | 0 |
| XY origin offset | 0.0, 0.0 | 0.0, 0.0 | 0 |

**On the gzip figure.** The input is uncompressed float32 geometry, which gzip
crushes; the output is meshopt-compressed, which is already entropy-coded and
therefore gzips badly. The comparison to make is against the rest of the shipped
set, not against the input: `135-south-park` ships 108,524 raw / 79,703 gzip,
`188-south-park` 119,312 / 61,724, `551-third` 252,408 / 168,650. At
126,760 / 72,612 this asset is squarely in family, and well inside the 500 KB
budget in `AGENTS.md`.

## Toolchain

Blender 5.2.0 LTS (fbe6228777e7), `npx gltfpack@0.24`, node v22.19.0,
three ^0.185.1 (pinned in `g3check/package.json`), python3 + Pillow 11.3.0, gzip -9.

## Phase A — waste census

`inspect.json`. 108 objects, 112 primitives, 3,928 tris, 8,576 verts, 10
materials, no textures, `NORMAL` the only non-position attribute.

| Finding | Count | Plan |
|---|---|---|
| Coincident vertex pairs (≤1 mm) | 6,400 | weld per object — the bevel pass leaves every box with duplicated corner verts |
| Objects joinable per material | 108 → 10 groups | join; this is the whole win here |
| Duplicate mesh groups | 1,644 redundant tris reported | left alone: they are the repeated window/trim solids, and joining per material collapses their *node* overhead, which is what actually costs bytes |
| Degenerate tris | 0 | — |
| Buried interior faces | 0 provable | the occluder rule needs a closed solid with ≥95% AABB fill; every solid here stands at 45° to the world axes, so none qualifies. Correctly conservative — no faces removed. |
| Over-tessellated curves | none | there are no curved shells; the segmental arch is five straight stepped courses |

Predicted, and achieved: essentially all of the saving comes from node/accessor
overhead and the weld, not from triangles. The triangle count is unchanged by
design — at 3,928 against a 9,000 cap, the geometry is not the problem.

## Phase B — geometry cleanup

`optimize.py` (adapted copy), `phaseb_stats.json`.

| Step | Tris | Verts |
|---|---|---|
| input | 3,928 | 8,576 |
| 1+2a weld ≤1 mm + degenerate | 3,928 | **2,176** |
| 2b interior faces | 3,928 | 2,176 (0 removed) |
| 3 limited dissolve 0.05° | 3,928 | 2,176 |
| 5 join per material | 3,928 | 2,176 |

**One asset adaptation, and it is the important one.** Step 3's limited dissolve
is skipped by name on `front_cornice` and `rear_parapet`. Both are closed ring
bands following the footprint all the way round — precisely the case
`GLB-OPTIMIZE-PROMPT` §3 step 3 warns about. Their top and bottom faces are
coplanar annuli; a strictly-coplanar dissolve merges each into a single ngon, and
re-triangulating an annulus emits sub-millimetre slivers whose averaged vertex
normals collapse to ~0. Blender hides that on import, gltfpack re-emits the stored
normals, and the failure surfaces only in the packed file as
`invalid_or_nonunit_loop_normal_count` — two steps later, after the shipping swap.
`350-brannan` hit exactly this on 13 Aug 2026.

The skip cost nothing: the dissolve saved 0 triangles on this asset either way.
The shipped file reports `invalid_or_nonunit_loop_normal_count: 0`.

Joins: `Toy_mustard` 35 objects, `Toy_glass` 19, `Toy_ink` 19, `Toy_sand` 7,
`Toy_roofd` 7, `Toy_gold_Glow` 7, `Toy_rust` 6, `Toy_steel` 3,
`Toy_cream`+`Toy_steel` 3 (the multi-material box tops). `front_base`,
`rear_body` and the two ring bands stay individually addressable.

`grp_Toy_gold_Glow` is joined only with itself — glow-ness is name-only and the
`_Glow` set must never merge into the base layer.

## Phase C — packing

```
npx gltfpack@0.24 -i mid.glb -o 132-south-park.optimized.glb -c -km -kn -noq
```

`-km -kn` keep the material and node names the loader treats as API; `-noq` is the
repo standard (`pipeline/compress-assets.mjs` produces the same encoding, and the
kit/landmark merge paths need float32 attributes). Preflight:
`grep -rn setMeshoptDecoder app/src/` hits `app/src/gltf.js:10` and
`app/src/assets.js:406`, so meshopt is decodable at runtime.

239,860 → 126,760 bytes. Material name set, bbox and origin verified on the output
rather than trusted from flags.

## Phase D

Not run. `ALLOW_BAKE: no`, and the contract forbids textures without a recorded
exception. Nothing here wants one: the asset has no bakeable shading beyond 0.06 m
bevels and 0.05 m trim relief.

## Phase E — A/B verification

`render_ab.py` on both files at the same rig, `diff_ab.py` for the deltas.
Landmark distances: near 1.5 × long axis (40.0 m), far 6 ×.

| View | Mean abs RGB Δ | Max px Δ |
|---|---|---|
| day near | 0.0001% | 7 |
| day far | 0.0003% | 4 |
| night near | 0.0256% | 26 |
| night far | 0.0240% | 26 |
| elevation N | 0.0000% | 7 |
| elevation E | 0.0036% | 23 |
| elevation S | 0.0035% | 35 |
| elevation W | 0.0000% | 1 |

Gate is ≤2% far / ≤4% near; the worst view is 0.026%, three orders of magnitude
inside it.

**Looked at, not just measured.** The ×8-amplified diff row of
`renders/contact_sheet.png` is black except for a scatter of single pixels on the
mustard trim edges and the arch steps — normal-quantisation rounding on
high-contrast silhouette edges. The night pair's slightly larger delta is the same
effect on the emissive window shells, where a one-bit change is amplified by the
emission strength. No element is missing, no silhouette moved, no shading artifact
appeared. Nothing here is visible to a player.

## Gate results

| Gate | Result | Evidence |
|---|---|---|
| G1 Contract | **PASS** | material name set identical (10/10); `Toy_gold_Glow` still its own object and material; no `Toy_body` in a landmark; node names intact |
| G2 Geometry | **PASS** | bbox and origin bit-identical; 11/11 signed volumes positive; `inverted_solids: []`; ray test 22,500 rays / 11,322 hits / **0 flipped** |
| G3 Round-trip | **PASS** | re-imports in Blender; `g3check` (pinned three ^0.185.1) reports `G3-OK`, 13 meshes, 3,928 tris, 10 materials, correct bbox, no decode errors |
| G4 Appearance | **PASS** | table above; worst 0.026% against a 2%/4% gate; diffs inspected |
| G5 Draw submeshes | **PASS** | 112 → 13 |
| G6 Size | **PASS** | 276,436 → 126,760 raw, −54.1%. Below the 60% aspiration, and the census says why: the remainder is silhouette geometry and 8,569 welded vertices carrying real corners, not waste. |
| G7 GPU budget | n/a | bake mode not run |
| G8 Hygiene | **PASS** | re-import object count 11 = export count; no foreign geometry; deterministic re-run reproduces the output; no `.blend1` files |

## Shipping swap

`132-south-park.optimized.glb` copied over `artifacts/132-south-park/132-south-park.glb`.
The pre-optimize original is archived byte-for-byte at
`optimize/input/132-south-park.glb` (verified with `cmp`).

The stage-2 contract validator was then re-run **on the shipped file** — this is
the step that catches dissolve slivers, and the reason to run it after the swap
rather than before:

```
overall PASS   objects 11   tris 3928   dims 26.6844 x 26.7064 x 12.07
min_z 0.0   xy_center_offset 0.0, 0.0   invalid_or_nonunit_loop_normal_count 0
```

`artifacts/132-south-park/validation.json` and `REPORT.md` now carry the shipped
numbers, so the integration stage writes its manifest entry from reality.
