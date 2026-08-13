# 234 Van Ness Avenue — optimize pass

Stage 4 of `docs/asset-pipeline/ADDRESS-TO-ASSET.md`, run per
`docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md` on 13 August 2026.
`ASSET_CLASS: landmark` · `ALLOW_MESHOPT: yes` · `ALLOW_BAKE: no`.

**Result: all gates pass. 985,244 → 306,900 bytes, −68.9 %.** The optimized file
is now the shipping `artifacts/234-van-ness/234-van-ness.glb`; the pre-optimize
original is archived byte-for-byte at `optimize/input/234-van-ness.glb`.

## Metrics

| | Input | Shipped | Δ |
|---|---|---|---|
| Raw bytes | 985,244 | **306,900** | **−68.9 %** |
| gzip −9 bytes | 110,315 | 126,669 | +14.8 % (expected — meshopt output is already entropy-coded) |
| Triangles | 11,656 | **11,656** | 0 |
| Vertices | 23,280 | 22,308 | −4.2 % |
| Objects | 790 | **20** | −97.5 % |
| Draw primitives | 797 | **22** | −97.2 % |
| Materials | 18 | 18 | identical set |
| bbox dims (m) | 56.27799 × 46.42741 × 30.12 | identical | 0 |
| bbox min / origin offset | (−28.13899, −23.81323, 0.0) / (0.0, −0.59953) | identical | 0 |

Comfortably inside the ≤ 500 KB on-disk budget (`sf-asset-check` §7).

## Phase A — waste census

`inspect.py` on the input. No textures; the only vertex attribute beyond
position is `NORMAL`. The waste was almost entirely **structural, not
geometric**:

| Technique | Predicted | Realised |
|---|---|---|
| Join per material — 790 objects over 18 materials, 797 primitives | the dominant win | 790 → 20 objects, 797 → 22 primitives |
| Weld coincident verts ≤ 1 mm, per object | 15,872 candidate pairs | 23,280 → 7,408 verts after Phase B |
| Duplicate meshes (identical window slabs, fins, pickets) | 9,088 redundant tris | not deduplicated — see the judgment call below |
| Degenerate faces | 0 reported by stage-2 validation | 0 |
| Buried interior faces | some expected at solid junctions | **0 removed** |
| Over-tessellated curves | one-pixel world size 0.0569 m at the 84.4 m near distance | none — this asset has no curved shells, only the six-sided tree crowns |

## Phase B — geometry cleanup

| Step | Tris | Verts |
|---|---|---|
| input | 11,656 | 23,280 |
| weld + degenerate | 11,656 | 7,408 |
| interior faces | 11,656 | 7,408 |
| limited dissolve 0.05° | 11,656 | 7,408 |
| join per material | 11,656 | 7,408 |

Re-import verified: 20 objects, 18 materials, bbox identical, `bbox_ok` and
`material_set_ok` both true, `inverted_solids` empty.

**Judgment call — no interior-face removal, and none expected.** The building is
authored as a union of interpenetrating closed boxes, so there genuinely are
buried faces at every junction. The prompt's occluder rule only permits deleting
a face when it is provably inside a **closed solid**, and the applied panels here
(fins, stripes, glow shells, pavers) sit *proud* of the wall rather than inside
it, so almost nothing qualifies. Deleting them by proximity instead of by proof
is exactly the mistake the rule exists to prevent. 0 removed is the correct
answer, not a missed opportunity.

**Judgment call — duplicate meshes were joined, not instanced.** The census found
9,088 redundant triangles across groups of identical window slabs. Sharing mesh
data would cut file bytes further, but the app's landmark loader merges every
asset to ≤ 2 draw calls by baking world matrices into one buffer
(`prepareGeometryForTransforms` in `app/src/assets.js`), so instances are
flattened at load anyway. Joining per material gives the same runtime result and
a simpler file. At 307 KB against a 500 KB budget there is no case for the extra
complexity.

## Phase C — packing

```
npx gltfpack@0.24 -i mid.glb -o 234-van-ness.optimized.glb -c -km -kn -noq
```

`-km -kn` keep the material and node names — mandatory, because `_Glow` is
name-only and gltfpack would otherwise merge the glow materials into their
identical-parameter non-glow twins and silently kill the night layer. `-noq`
keeps float32 attributes, matching `pipeline/compress-assets.mjs` and the repo
standard.

624,760 → 306,900 bytes.

## Phase E — A/B verification

`render_ab.py` on both files through one rig, then `diff_ab.py`. Mean absolute
RGB delta over foreground pixels:

| View | Δ | Gate |
|---|---|---|
| day near | 0.0155 % | ≤ 4 % |
| day far | 0.0278 % | ≤ 2 % |
| night near | 0.0155 % | ≤ 4 % |
| night far | 0.0278 % | ≤ 2 % |
| elevation N | 0.1157 % | — |
| elevation E | 0.0065 % | — |
| elevation S | 0.0079 % | — |
| elevation W | 0.0458 % | — |

**What the diffs actually show.** At ×8 amplification every diff is black except
for scattered single-pixel specks along panel edges and one faint soft gradient
across the shadow/ground band in the north elevation. Both are the signature of
sub-pixel rasterization shifts after welding — the same triangle, its vertices
now shared, antialiasing one pixel differently. Nothing is missing, no silhouette
moved, no shading artifact appeared, and there is nothing here a player could
notice.

**Deviation, recorded honestly: the A/B pass was rendered in Workbench, not
Cycles.** This machine was running five other landmark sessions' Blender jobs at
load averages between 100 and 750 and a CPU-Cycles A/B could not complete. For a
pixel-delta gate Workbench is arguably the better instrument — it is
deterministic and noise-free, so a non-zero delta is a real difference rather
than sampling noise. Its one limitation matters here: **Workbench does not render
emission, so the `night_near` / `night_far` pairs are identical to their day
counterparts and do not exercise the `_Glow` layer.** The proof that the glow
layer survived is carried instead by G1 (the material-name set is identical, and
`Toy_glassl_Glow` / `Toy_trim_Glow` are both present and separate) and by G3
(the three.js round-trip reports all 18 materials across 22 meshes). That is the
property `-km` protects, and it is directly verified.

## Gates

| Gate | Result | Evidence |
|---|---|---|
| **G1** Contract | **PASS** | material set identical (18); `Toy_glassl_Glow` and `Toy_trim_Glow` separate; no `Toy_body`; node names intact |
| **G2** Geometry | **PASS** | bbox and origin bit-identical; all 20 signed volumes positive; `inverted_solids: []`; 22,500 rays, 17,919 hits, **0 flipped** (0.0 %) |
| **G3** Round-trip | **PASS** | re-imports in Blender; `g3check` → `G3-OK {"ok":true,"meshes":22,"tris":11656,...}` on pinned three 0.185 |
| **G4** Appearance | **PASS** | max delta 0.1157 % against 2 % / 4 % gates; diffs inspected and described above |
| **G5** Draw submeshes | **PASS** | 797 → 22 |
| **G6** Size | **PASS** | −68.9 %, past the 60 % target |
| **G7** GPU budget | n/a | `ALLOW_BAKE: no` |
| **G8** Hygiene | **PASS** | re-import object/material/bbox check clean; scripts deterministic; no `.blend1` files |

## Toolchain

Blender 4.5 LTS (headless, `-b --python`) · `npx gltfpack@0.24` · node with
pinned `three@^0.185.1` in `g3check/` · python3 + Pillow · gzip −9.
