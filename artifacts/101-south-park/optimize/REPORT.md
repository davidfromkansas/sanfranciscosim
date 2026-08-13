# 101 South Park — optimize report (stage 4)

Run 13 August 2026 per `docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md`, with the defaults:
`ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`. Scripts here are copies of
`tools/glb-optimize/` — only the contact-sheet title was adapted; the geometry pipeline
needed no per-asset changes.

The optimized GLB is now the shipping file at `artifacts/101-south-park/101-south-park.glb`.
The approved pre-optimize asset is archived byte-for-byte at
`optimize/input/101-south-park.glb`.

## 1. Headline

| | Input (approved) | **Shipped (optimized)** |
|---|---|---|
| File, raw | 479,732 B | **191,700 B (−60.0%)** |
| File, gzip-9 | 104,937 B | see `inspect.json` |
| Triangles | 7,534 | **7,502** (−0.4%) |
| Vertices | 15,108 | **3,874** (−74.4%) |
| Objects | 86 | **11** |
| Draw submeshes (primitives) | 87 | **12** |
| Materials | 11 | 11, identical set |
| Dimensions (AABB) | 30.5306 × 29.8696 × 10.90 m | identical to 5 decimals |
| Origin offset XY | (−0.00279, −0.17191) | identical |
| Compression | none | `EXT_meshopt_compression`, **unquantized** |

Packing command, exactly as the prompt's §4 mandates for this repo:

```
npx gltfpack@0.24 -i mid.glb -o 101-south-park.optimized.glb -c -km -kn -noq
```

`-km` keeps `Toy_rust_Glow` and `Toy_glass_Glow` from being merged into their
identical-parameter non-glow twins, which would silently kill the night layer. `-noq`
matches `pipeline/compress-assets.mjs`, which is the repo standard.

## 2. Waste census (Phase A) and what each technique actually returned

`inspect.json` found, before any work:

| Finding | Count | Outcome |
|---|---|---|
| Coincident vertex pairs | 11,225 | The dominant waste. Per-object weld at ≤ 1 mm took vertices 15,108 → 3,883. |
| Duplicate mesh groups | 14 groups, 2,164 redundant triangles | Left in place — these are the repeated window bays and roof boxes, and joining per material (below) already collapses their node overhead. Sharing mesh data would need instancing, which is not worth it at 11 objects. |
| Join candidates | 10 materials over 85 objects | The second big win: 86 objects → 11, primitives 87 → 12. |
| Degenerate triangles | 3 | Removed. |
| Buried interior faces | 0 removed | The occluder rule applies: this asset is a union of interpenetrating solids where the only genuine box-like occluder is `body`, and every panel that touches it is a proud surface, not a buried one. Nothing was provably invisible. |
| Over-tessellated curves | none applicable | The asset has no curved shells — everything is flat-faced. |

Triangle count barely moved (7,534 → 7,502) and that is the correct outcome: the geometry
was authored at budget, so the win here is vertex count, node count and draw submeshes, not
triangles. Gate G6's 60% target was met on file size anyway.

## 3. Gates

| Gate | Result |
|---|---|
| **G1 Contract** — material set identical, `_Glow` separate, no `Toy_body`, node names intact | **PASS** — 11 materials in, 11 out, same names |
| **G2 Geometry** — bbox within max(1 cm, 0.1%), origin within 1 cm, signed volumes positive, flip ≤ 0.15% | **PASS** — bbox delta 0.00000 m on all three axes, origin delta 0.00000 m, 11/11 signed volumes positive, `inverted_solids: []`, ray flip **0.0385%** of 15,574 hits |
| **G3 Round-trip** — Blender re-import and pinned-three `g3check` | **PASS** — `G3-OK {"ok":true,"meshes":12,"tris":7502}`, no decode errors |
| **G4 Appearance** — day+night × near+far, ≤ 2% far / ≤ 4% near | **PASS** — worst case **0.129%** (elevation N); aerials 0.047% day-near, 0.004% night-near |
| **G5 Draw submeshes** ≤ input | **PASS** — 12 vs 87 |
| **G6 Size** reduced, target 60% | **PASS** — −60.0% |
| **G7 GPU budget** | n/a — `ALLOW_BAKE: no`, no textures |
| **G8 Hygiene** — no foreign geometry, deterministic scripts | **PASS** — re-import object/material counts match; every step is a committed script |

Stage-2 contract validation was re-run on the shipped file and still returns
**PASS on all 16 checks** (`../validation.json`): 7,502 triangles, 11 objects, crest still
exactly 10.9 m, min Z 0.0.

## 4. Looking at the diffs honestly

The amplified (×8) diff row in `renders/contact_sheet.png` shows faint anti-aliasing
shimmer along two places only: the steel coping line where it meets the pale roof deck, and
the vertical edges of a few ground-floor oak frames. Both are sub-pixel edge sampling, not
geometry change — the welded vertices sit in the same positions, and the bbox is identical
to five decimals. The night pairs are essentially black (0.004% mean), which is the useful
signal: the `_Glow` split survived packing intact, so the night layer is unchanged.

Nothing in these diffs is visible at 1× and nothing a player would notice.

## 5. Note on the wordmark

The "Kleiner Perkins" lettering is the one part of this asset where triangle count is
sensitive to authoring choices rather than to this stage. It survives optimization
untouched — it joins into `grp_Toy_trim` (2 objects → 1) and its glyph outlines were
already welded at 9% of cap height in the build script, so Phase B's 1 mm weld found
nothing further to merge. If the wordmark ever needs to grow, change `cap_h` in
`build_101_south_park.py`; the weld is proportional, so the cost does not follow.
