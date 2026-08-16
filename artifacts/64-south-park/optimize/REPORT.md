# South Park — GLB optimize pass (stage 4)

`ASSET_CLASS: landmark` · `ALLOW_MESHOPT: yes` · `ALLOW_BAKE: no` ·
`TARGET_REDUCTION: 60%`. Procedure: `docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md`.
Scripts are adapted copies of `tools/glb-optimize/`; the two per-asset adaptations are
called out in §3 and both are commented in the scripts themselves.

## Result

| | input | shipped |
|---|---|---|
| File, raw | **609,080 B** | **283,916 B** (−53.4%) |
| File, gzip −9 | 159,782 B | 172,924 B |
| Triangles | 11,500 | **11,500** (unchanged) |
| Vertices (Blender, post-import) | 21,824 | 20,422 |
| Mesh objects / primitives | 20 | **15** |
| Materials | 13 | 13, identical set |
| bbox | 122.4585 × 121.0471 × 15.0 | identical |
| Signed volumes | all positive | all positive |
| Ray flip fraction | — | **0.0** (22,500 rays, 7,691 hits, 0 flipped) |

The shipped file is `artifacts/64-south-park/64-south-park.glb`; the pre-optimize
original is archived byte-for-byte at `optimize/input/64-south-park.glb`. The shipped
file re-passes the **stage-2 contract validator** in full (all 20 checks), not just the
optimize gates.

**Note on the gzip figure.** The packed file gzips *larger* than the input (172,924 vs
159,782). That is expected: meshopt output is already entropy-dense, so a second
compressor has nothing left to find. The number that matters against the repo's
"≤ 500 KB compressed on disk" budget is the 283,916 B file itself, which is what the
loader fetches and what `MeshoptDecoder` expands.

## 1. Toolchain

Blender 5.2.0 LTS (fbe6228777e7, 2026-07-14) · `npx gltfpack@0.24` · node v22.19.0 ·
Python 3.9.6 · Pillow 11.3.0 · gzip −9. `grep -rn setMeshoptDecoder app/src/` hits
`app/src/gltf.js:10` and `app/src/assets.js:406`, so meshopt is available and `-c` is
used.

## 2. Phase A — waste census

20 objects carrying 13 materials, so the dominant waste is **object-count overhead**:
five materials are shared by two or three objects each (`Toy_stone` → ground plate, seat
walls, path field; `Toy_cream` → tablets, kerb; `Toy_verdigris` → crowns, beds;
`Toy_steel` → trunks, furniture frames, lamp poles; `Toy_mint` → lawns, play mound).
Nothing else stood out:

- **No duplicate meshes.** Every object is a distinct union of solids.
- **No buried interior faces recoverable.** The occluder rule requires a closed solid
  filling ≥ 95% of its own AABB. Every object here is a *scattered* union — 96 wall
  boxes spread over 104 × 97 m, 34 crowns over the whole park — so nothing qualifies as
  an occluder and the pass removed 0 faces, as expected.
- **No over-tessellated curves worth halving.** The crowns are 10-gons, the Shout's
  tubes 6-gon sections on 48 segments, the tablets are 4-gons. All are silhouette.
- **Unwelded coincident verts:** 21,824 → 6,550 in Blender after a 1 mm per-object weld,
  but this is bookkeeping rather than a saving — glTF splits vertices by normal on both
  import and export, so the exported count lands at 20,422 either way.

Predicted savings before executing: ~5 primitives from the join, and the packing pass
carrying the file win. Both landed.

## 3. Phase B — geometry cleanup

| Step | Tris | Verts |
|---|---|---|
| input | 11,500 | 21,824 |
| weld + degenerate (1 mm, per object) | 11,500 | 6,550 |
| interior faces (0 removed — see §2) | 11,500 | 6,550 |
| limited dissolve | **SKIPPED** | |
| join per material | 11,500 | 6,550 |

**Two per-asset adaptations, both deliberate:**

1. **The limited dissolve is skipped entirely.** GLB-OPTIMIZE-PROMPT §3.3 says to skip
   it on assets with large coplanar ring bands, and this asset has several: the kerb is a
   0.70 m band following the whole 47-vertex footprint, the ground plate's top and bottom
   are the same annulus, and the 72 tablets and 13 beds all have perfectly coplanar caps.
   Dissolving those merges each ring into one annulus ngon whose re-triangulation emits
   metre-long sub-millimetre slivers — which pass every area-based degeneracy test and
   surface only later, in the *packed* file, as `invalid_or_nonunit_loop_normal_count`
   (measured on `350-brannan`, 13 Aug 2026). The step was worth a few dozen triangles
   here. Not run.
2. **`ground_plate` and `tree_crowns` are held out of the per-material join.** The
   stage-2 contract validator finds the plate by name to measure the oriented
   159.5 × 23.5 m footprint and the anchor offset, and the crowns by name to confirm all
   20 measured tree positions survived. A per-material join buries them inside
   `grp_Toy_stone` and `grp_Toy_verdigris`, after which the *shipped* file can no longer
   be checked against the survey it was built from. Cost: 13 → 15 primitives. The loader
   merges every landmark to ≤ 2 draw calls regardless, so the runtime cost is zero.

Normals audit after the join: `inverted_solids: []`.

## 4. Phase C — packing

```
npx gltfpack@0.24 -i mid.glb -o 64-south-park.optimized.glb -c -km -kn -noq
```

`-km -kn` keep material and node names (glow-ness is name-only, so without `-km`
gltfpack would merge `Toy_cream_Glow` into `Toy_cream` and silently kill the night
layer). `-noq` is the repo standard and matches `pipeline/compress-assets.mjs`; the
headline win is smaller than the quantized numbers quoted in the prompt, and that is
the intended trade.

571,608 B (post-Phase-B, unpacked) → **283,916 B**.

## 5. Phase D

Not run. `ALLOW_BAKE: no`, and the contract forbids textures.

## 6. Phase E — A/B verification

Same rig, input vs shipped, day (glow alpha 0.12) and night (glow emission 6, dusk
world), near = 1.5× long axis, far = 6×, plus four orthographic elevations.
`renders/contact_sheet.png` is input / optimized / diff ×8.

| View | mean abs RGB delta | max px delta |
|---|---|---|
| day near | 0.0167% | 12 |
| day far | 0.0137% | 7 |
| night near | 0.0529% | 51 |
| night far | 0.0526% | 28 |
| elevation N / E / S / W | 0.0223 / 0.0177 / 0.0126 / 0.0152% | 34 / 29 / 70 / 42 |

**What the diffs actually show, having looked at them:** the ×8-amplified images are
black except for scattered single-pixel speckle, concentrated on the Shout's circular
tube edges and on one lamp head, plus a faint dusting along the ground line in the
elevations. That is sub-pixel silhouette difference from the meshopt vertex re-encode on
the asset's highest-curvature geometry, plus Cycles sampling noise (24 samples with a
denoiser is not bit-identical between runs). No element is missing, no silhouette moved,
no shading changed, no glow surface lost its layer. At ×1 the pairs are
indistinguishable. Nothing here a player could notice.

## 7. Gates

| Gate | Result | Evidence |
|---|---|---|
| **G1** Contract — material set identical, `_Glow` separate, `Toy_body` absent, kept node names intact | **PASS** | `validation.json` `G1_materials_identical: true`; `ground_plate` and `tree_crowns` present in the shipped file |
| **G2** Geometry — bbox within tolerance, origin within 1 cm, volumes positive, flip ≤ 0.15% | **PASS** | bbox identical to 4 dp; `flipped_fraction: 0.0` over 22,500 rays |
| **G3** Round-trip — Blender re-import + pinned-three GLTFLoader | **PASS** | `G3-OK … meshes 15, tris 11500, 13 materials, bbox 122.4585 × 15 × 121.0471` |
| **G4** Appearance — ≤ 2% far, ≤ 4% near, nothing visible | **PASS** | max 0.053%, ~38× inside the tightest gate; description above |
| **G5** Draw submeshes ≤ input | **PASS** | 20 → 15 |
| **G6** Size reduced | **PASS** (−53.4%, short of the 60% aspiration) | The census shows the remainder is silhouette geometry: 2,584 tris of tree crowns, 1,152 of the Shout's tubes, 1,152 of seat walls, 952 of trunks. Nothing left to remove without changing what the asset looks like. The prompt also notes that `-noq` gives a smaller headline win than the quantized figures it quotes, and `-noq` is the repo standard. |
| **G7** GPU budget | n/a | bake mode off |
| **G8** Hygiene — no foreign geometry, deterministic, no `.blend1` | **PASS** | re-import object count matches; a full re-run of Phase B + C reproduced a byte-identical GLB (md5 compared); no `.blend1` files |

All gates pass, so the shipping swap was made: `64-south-park.optimized.glb` →
`artifacts/64-south-park/64-south-park.glb`, original archived under `input/`.
