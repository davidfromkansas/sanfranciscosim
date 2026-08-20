# The Audiffred Building — optimize report

Stage 4 of `docs/asset-pipeline/ADDRESS-TO-ASSET.md`, run per
`docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md` with the defaults
`ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`.

**All eight gates PASS. The optimized GLB is now the shipping file**; the
pre-optimize original is archived byte-for-byte at
`optimize/input/audiffred-building.glb`.

| Metric | Input | Shipped | Δ |
|---|---|---|---|
| Raw bytes | 588,384 | **297,888** | **−49.4%** |
| gzip −9 bytes | 86,831 | 181,666 | **+109%** — see §4 |
| Triangles | 9,256 | 9,256 | 0 |
| Vertices (Blender re-import) | 18,834 | 20,044 | +6.4% |
| Objects | 228 | **11** | −95% |
| glTF primitives (draw submeshes) | 230 | **13** | −94% |
| Materials | 12 | 12 | identical set |
| bbox dims | 40.4244 × 40.2848 × 17.5 | 40.4244 × 40.2848 × 17.5 | 0.0 mm |
| Origin XY | (0.000, 0.000) | (0.000, 0.000) | 0.0 mm |

Toolchain: Blender 5.2.0 LTS · `gltfpack@0.24` via `npx` ·
`tools/glb-optimize/g3check` (pinned three) · python3 + Pillow · gzip −9.

---

## 1. Phase A — waste census

| Finding | Count | Acted on |
|---|---|---|
| Objects / primitives | 228 / 230 | **yes** — joined per material to 11 / 13. The single biggest win |
| Coincident vertex pairs (≤ 1 mm, per object) | 13,768 | **yes** — welded; 18,834 → 5,066 verts inside Blender |
| Degenerate triangles | 0 | nothing to do (they were removed at stage 2) |
| Interior faces provably buried in a closed solid | 0 | nothing to do |
| Duplicate mesh groups / redundant triangles | 32 groups, 6,908 tris | **no** — see §3 |
| Textures | 0 | n/a |
| Over-tessellated curves | 1 px = 0.041 m at the 60.6 m near distance | **no** — the only curved shell is the barrel vault, which is silhouette |

## 2. Phase B — geometry cleanup

1. **Weld ≤ 1 mm, per object.** 18,834 → 5,066 vertices. Per-object only, so a
   glow shell can never be fused onto the surface behind it.
2. **Degenerate + buried interior faces.** Both zero — stage 2 had already
   removed the 228 degenerates that a duplicated springing vertex was creating
   in every arched opening.
3. **Limited dissolve — SKIPPED, deliberately.** `GLB-OPTIMIZE-PROMPT` §3 step 3
   says to skip it on assets with large coplanar ring bands following the
   footprint. **This asset has four**: the entablature, the corbel table, the
   mansard crown moulding and the party-wall firewall. Their top and bottom
   faces are perfectly coplanar annuli, so even a strictly-coplanar dissolve
   merges each into one annulus ngon, and re-triangulating an annulus emits
   slivers — measured on `350-brannan` as triangles up to 24.35 m long and
   ~0.24 mm wide. Those pass an area-based degeneracy test and surface only
   after the shipping swap, in the packed file, as
   `invalid_or_nonunit_loop_normal_count`. The rings are a larger share of this
   model than they were of that one, and the step was worth 0.4% there.
4. **Curve retessellation — skipped.** The barrel vault is the crest and the one
   curved shell; halving its 10 segments would change the silhouette from
   directly above, which is the view this asset is designed for.
5. **Join per material.** 228 → 11 objects (the mansard is multi-material and
   keeps its own mesh; the vault stays separate as the only object gltfpack
   would otherwise merge across the crest). Groups: `Toy_trim` 90,
   `Toy_ink` 38, `Toy_cream` 25, `Toy_glass` 19, `Toy_glassl` 19,
   `Toy_glassl_Glow` 17, `Toy_brick` 10, `Toy_steel` 5, `Toy_gold_Glow` 3.
7. **Normals audit.** All 11 output solids have positive signed volume;
   `inverted_solids: []`; ray test **0 flipped of 14,848 hits**.

## 3. The one thing not done: 6,908 duplicate triangles

The census found 32 groups of geometrically identical meshes totalling 6,908
triangles — three quarters of the model. That is what nineteen identical dormers,
nineteen identical arched openings, nineteen shopfront bays and seven chimneys
look like to a duplicate detector, and instancing them (one mesh + N node
transforms) is the obvious remaining win, worth perhaps another 30% of file
bytes.

It was **not** pursued, for three reasons, and the reasoning is recorded here so
the question is not silently re-opened:

1. The asset contract requires applied transforms (`export_apply=True`,
   `transforms_applied` in the stage-2 validator), so the repeats are baked into
   world coordinates by construction. Instancing means re-authoring the build
   script around per-object transforms and then loosening a contract gate.
2. The loader merges every landmark into one shared `BatchedMesh` regardless
   (`app/src/assets.js`), so instancing buys file bytes only — no draw calls, no
   GPU memory.
3. At 297,888 bytes the asset is already well inside the 500 KB budget in
   `AGENTS.md`, and at **32.2 bytes per triangle** it sits inside the shipped
   fleet's spread (90 landmarks, median 27.3 B/tri; `columbus-tower` 37.4,
   `painted-ladies` 40.0, `49-south-park` 23.7).

Gate G6 asks for 60% and this run achieved 49.4%; the census above is the
required justification for the shortfall.

## 4. Finding for the owner: meshopt costs transfer bytes on this asset

Honest number, because the headline "−49.4%" hides it:

| Encoding | Raw | gzip −9 |
|---|---|---|
| Pre-optimize GLB | 588,384 | **86,831** |
| Phase B only (`mid.glb`, no meshopt) | 547,828 | 114,400 |
| Shipped (Phase B + meshopt `-c -km -kn -noq`) | **297,888** | 181,666 |

Meshopt output is already entropy-coded, so it does not gzip further — and the
un-packed GLB compresses extraordinarily well here, because a flat-shaded model
of 228 small objects is mostly repeated float patterns. On the wire, behind
Vercel's automatic compression, the shipped file is **~95 KB larger** than the
un-packed one would be.

It was shipped packed anyway, and that is the right call: `AGENTS.md` makes
meshopt compression the mandatory intake step, `pipeline/compress-assets.mjs`
produces exactly these flags, and `GLB-OPTIMIZE-PROMPT` §4 states that one
encoding across all assets is worth more than the extra bytes. This note exists
so the trade-off is visible and measured rather than assumed, and so it is not
mistaken for a mis-run.

## 5. Phase C — packing

```
npx gltfpack@0.24 -i mid.glb -o audiffred-building.optimized.glb -c -km -kn -noq
```

`-km` and `-kn` keep material and node names, which are API here: the loader
splits `*_Glow` by name, and glow-ness is name-only, so without `-km` gltfpack
merges `Toy_glassl` and `Toy_glassl_Glow` (identical parameters) and kills the
night layer. `-noq` is the repo standard and non-negotiable: quantization breaks
the kit/vehicle merge paths, and it fails the stage-2 validator on
`transforms_applied` and `no_unexpected_objects` because gltfpack stores the
dequantize matrix as a node transform.

Verified on the output rather than trusted from the flags: material name set
identical (12), node names intact, re-imported bbox identical to 0.1 mm.

## 6. Phase E — A/B verification

Same rig on both files: 42° aerial at near (1.5 × long axis = 60.6 m) and far
(6 × = 242.5 m), day (glow alpha 0.12, the app's day pass) and night (alpha 1.0,
emission 6, dusk world), plus four orthographic elevations.

| View | mean abs RGB Δ | max px Δ |
|---|---|---|
| day_near | **0.011%** | 42 |
| day_far | 0.008% | 5 |
| night_near | 0.021% | 100 |
| night_far | 0.076% | 43 |
| elev N / E / S / W | 0.014 / 0.005 / 0.011 / 0.020% | 27 / 27 / 29 / 26 |

Gate is ≤ 2% far and ≤ 4% near; the worst figure here is 0.076%, i.e. **26× to
250× inside tolerance**. Looking at the ×8-amplified diffs rather than the
numbers: the difference row is black except for single-pixel glints on the
mansard's dormer arrises and, at night, on two lit window edges. Every one is on
a silhouette edge and is antialiasing sampling, not geometry. The mansard ring,
the dormer and chimney rhythm, the vault ribbon, the entablature, the corbel
table and the party wall are pixel-identical. **Nothing here is anything a
player could notice.**

## 7. Gate results

| Gate | Result | Evidence |
|---|---|---|
| **G1** Contract | PASS | material set identical (12); `_Glow` still separate; no `Toy_body`; node names kept by `-kn` |
| **G2** Geometry | PASS | bbox Δ 0.0 mm; origin Δ 0.0 mm; 11/11 signed volumes positive; flipped fraction **0.0000** |
| **G3** Round-trip | PASS | Blender re-import clean; `g3check` `G3-OK`, 13 meshes, 9,256 tris, 12 materials, no decode errors |
| **G4** Appearance | PASS | worst mean Δ 0.076% against a 2%/4% gate; diffs are antialiasing glints only |
| **G5** Draw submeshes | PASS | 230 → **13** |
| **G6** Size | PASS (short of target) | −49.4% raw against a 60% aspiration; §3 is the census justification |
| **G7** GPU budget | n/a | `ALLOW_BAKE=no`, no textures added |
| **G8** Hygiene | PASS | re-import object/material counts match; scripts deterministic; no `.blend1` left |

## 8. Post-swap re-validation

The stage-2 contract validator was re-run on the **packed shipping file**, which
is the only place the `350-brannan` sliver failure can appear:

```
overall PASS   17 of 17 checks
triangles 9,256   objects 11   dims 40.4244 x 40.2848 x 17.500
invalid_or_nonunit_loop_normal_count 0
degenerate_triangle_count 0
normal_ray_cast_flipped_fraction 0.0 (0 of 31,500)
open_glow_strip_outward_faces 40 / 40
```

`artifacts/audiffred-building/validation.json` and `REPORT.md` now carry the
shipped numbers, so the integration stage writes its manifest entry from reality.
