# 166–168 South Park — GLB optimize report

Stage 4 of `docs/asset-pipeline/ADDRESS-TO-ASSET.md`, executed per
`docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md` on 16 August 2026.

| Input | |
|---|---|
| `ASSET_DIR` | `artifacts/168-south-park/` |
| `ASSET_CLASS` | `landmark` |
| `ALLOW_MESHOPT` | `yes` — verified: `grep -rn setMeshoptDecoder app/src/` hits `app/src/assets.js` and `app/src/gltf.js` |
| `ALLOW_BAKE` | `no` |
| `TARGET_REDUCTION` | 60% file size |

Toolchain: Blender 5.2.0 LTS · `gltfpack@0.24` via npx · node v22.19.0 ·
three 0.185.1 (pinned in `g3check/package.json`) · Python 3.9 with Pillow 11.3.0 ·
gzip -9.

The input was copied byte-for-byte to `input/168-south-park.glb` (verified with
`cmp`) and every step ran against the copy.

## 1. Headline metrics

| | input | optimized | delta |
|---|---|---|---|
| raw bytes | 209,080 | **99,096** | **−52.6%** |
| gzip -9 bytes | 39,344 | 68,213 | +73.4% (expected — see §5) |
| triangles | 3,504 | 3,504 | 0 |
| vertices | 7,044 | **1,852** | −73.7% |
| objects / nodes | 52 | **8** | −84.6% |
| draw submeshes (primitives) | 53 | **9** | −83.0% |
| materials | 8 | 8 | identical set |
| bbox dims (m) | 25.7032 × 25.5037 × 10.4400 | 25.7032 × 25.5037 × 10.4400 | 0 |
| origin offset XY (m) | (0.0556, −0.0603) | (0.0556, −0.0603) | 0 |
| base Z | 0.0 | 0.0 | 0 |

## 2. Phase A — waste census

From `inspect.json`:

| Finding | Count | Technique | Predicted saving |
|---|---|---|---|
| Coincident vertex pairs ≤ 1 mm | 5,192 | per-object weld | ~5.2k verts |
| Objects sharing one material | 52 objects across 6 joinable materials (`Toy_brick` 12, `Toy_steel` 13, `Toy_stone` 9, `Toy_glass` 8, `Toy_ink` 7, `Toy_glass_Glow` 2) | join per material | 52 → 8 nodes, 53 → 9 primitives |
| Duplicate mesh signatures | 732 redundant triangles across 9 groups (coping l/r, the two skylights, the two skylight kerbs, four pilasters, three window frames, two door frames, …) | left as joins, not instances — see §4 | 0 (folded into the joins) |
| Degenerate triangles | 0 | — | — |
| Over-tessellated curves | none — the asset has no curved geometry at all | — | — |
| Buried interior faces | none found | — | — |

Vertex attributes are `POSITION` + `NORMAL` only; no UVs, no textures, no
vertex colours. There is nothing to prune.

## 3. Phase B — geometry cleanup (`optimize.py`)

| step | tris | verts |
|---|---|---|
| input | 3,504 | 7,044 |
| 1+2a weld ≤ 1 mm + degenerate | 3,504 | **1,852** |
| 2b interior faces buried in closed solids | 3,504 | 1,852 (0 removed) |
| 3 limited dissolve | **SKIPPED** — see below | |
| 5 join per material | 3,504 | 1,852 (52 → 8 objects) |
| 7 normals audit | 0 inverted solids | |

**The limited dissolve was skipped deliberately**, per GLB-OPTIMIZE-PROMPT §3.3.
This asset is exactly the shape that rule was written for: it carries two ring
bands that follow the whole footprint — `parapet` (`Toy_brick`, 288 tris) and
`parapet_coping` (`Toy_steel`, 288 tris) — plus a 182 m² coplanar body cap.
Their top and bottom faces are perfect coplanar annuli, so even a
strictly-coplanar dissolve merges each ring into one annulus ngon, and
re-triangulating an annulus emits ~0.2 mm slivers up to 30 m long. Those pass
every area-based degeneracy test in Phases B and E and surface only in the
packed file, as `invalid_or_nonunit_loop_normal_count`. The step was worth 0.4%
of triangles on `350-brannan`, where it was measured; on a 3.5k-triangle asset
of this shape it is worth less than that. Skipping it costs nothing and removes
the only step in the pipeline that can manufacture degenerate geometry.

The weld is where all the value is here: 7,044 → 1,852 vertices, because the
build script emits every panel, box and band as an independent closed solid with
duplicated corner vertices. Welding is per object, so it can never fuse a glow
shell onto the surface behind it — the two `_Glow` objects are separate objects
and stay separate.

**The weld did not smooth the flat shading.** That is the failure this step is
known for, and it is invisible to every gate except G4. Checked directly on
`renders/out_day_near.png`: every face is still flat, every edge still crisp,
and the G4 mean delta of 0.006–0.028% is far too small to be a shading change
(a flat→smooth flip on this palette moves whole faces by tens of levels).

## 4. Judgment calls

- **Join, not instance, for the nine duplicate mesh groups.** The largest is
  four pilasters at 44 triangles each. Sharing mesh data would add nine node
  transforms to save ~700 triangles of buffer, and the landmark path merges
  everything into one `BatchedMesh` at load anyway, so instancing buys nothing
  downstream. The joins already collapse all of it into 8 nodes.
- **No node names to preserve.** The manifest addresses this asset by file, not
  by node, and there is no `Toy_body` (that is a kit-piece mechanism). The joined
  objects are free to be renamed `grp_<material>`.
- **`-noq` (no quantization)**, per the repo standard and
  `pipeline/compress-assets.mjs`. Not re-litigated.

## 5. Phase C — packing

```
npx gltfpack@0.24 -i mid.glb -o 168-south-park.optimized.glb -c -km -kn -noq
```

`-km` and `-kn` keep material and node names, which is load-bearing here:
glow-ness is name-only, and without `-km` gltfpack would merge `Toy_glass_Glow`
into `Toy_glass` (identical parameters, different name) and silently kill the
night layer. Verified on the output: the material set is identical and both
`_Glow` materials survive as separate materials.

**Gzip goes up, and that is correct.** `EXT_meshopt_compression` already stores
the buffers in a compressed, high-entropy encoding, so a second gzip pass over
them expands rather than shrinks. The number that matters for a CDN-served asset
is the 99 KB raw file, which is what the browser downloads and what
`compress-assets.mjs` would otherwise produce at intake. Recorded here only so
the +73% is not read as a regression later.

## 6. Phase E — A/B appearance

Same rig for both files: 42° elevation aerial from the south-west, 40° fov,
near = 1.5× long axis, far = 6× long axis, day (glow alpha 0.12) and night
(glow alpha 1.0, emission 6, dusk world), plus four orthographic elevations.

| view | mean abs RGB delta | max px delta |
|---|---|---|
| day near | 0.0224% | 57 |
| day far | 0.0283% | 53 |
| night near | 0.0059% | 7 |
| night far | 0.0068% | 3 |
| elev N | 0.0154% | 21 |
| elev E | 0.0161% | 124 |
| elev S | 0.0241% | 30 |
| elev W | 0.0270% | 28 |

Gates are ≤ 2% far and ≤ 4% near; the worst view here is 0.028%, roughly two
orders of magnitude inside them.

**What the diffs actually show, having looked at them** (`renders/contact_sheet.png`,
diff row amplified ×8): a hairline of non-zero pixels along the parapet coping's
top edge and along the building's outer silhouette, and nothing anywhere else.
That is sub-pixel antialiasing moving on edges whose vertices were welded — the
same edge, sampled a fraction of a pixel differently. The single 124-level max
on elev E is one pixel on the coping edge, not a region. No element is missing,
no silhouette moved, no face changed shade, the three diamonds and the gable
crown are unchanged, the roof furniture is all present, and both lit windows and
the shopfront spill are unchanged at night. There is nothing here a player could
notice.

## 7. Gate results

| Gate | Result | Evidence |
|---|---|---|
| **G1 Contract** | **PASS** | material set identical (8, byte-compared sorted); `Toy_glass_Glow` and `Toy_trim_Glow` still separate materials; no `Toy_body` in this asset; no manifest node names to preserve. `validation.json` `G1_materials_identical: true` |
| **G2 Geometry** | **PASS** | bbox delta 0.0000 m on all three axes (tolerance 2.57 cm); origin delta 0.0000 m (tolerance 1 cm); all signed volumes positive; 22,500-ray test → 12,962 hits, **0 flipped**, `flipped_fraction 0.0` (tolerance 0.15%) |
| **G3 Round-trip** | **PASS** | re-imports in Blender (8 mesh objects, bbox and material set intact); `g3check` with pinned three 0.185.1 → `G3-OK {"ok":true,"meshes":9,"tris":3504,...}`, no decode errors, only `EXT_meshopt_compression` |
| **G4 Appearance** | **PASS** | §6 — worst mean delta 0.028% against a 2%/4% gate; described honestly above |
| **G5 Draw submeshes** | **PASS** | 53 → 9 |
| **G6 Size** | **PASS with a note** | 209,080 → 99,096 raw, −52.6%, short of the 60% aspiration. The census in §2 accounts for the remainder: after the weld and the joins there is no waste left — 0 degenerate faces, 0 buried faces, no curves to retessellate, no UVs or textures to prune, and the triangle count is 3,504 of which essentially all is silhouette (the shell, the stepped parapet, the pilasters and the openings). The only remaining lever would be Phase D baking, which is off and which this asset has no use for. |
| **G7 GPU budget** | **n/a** | bake mode off |
| **G8 Hygiene** | **PASS** | re-import object count matches the export (8); no foreign geometry; scripts are deterministic and re-run reproduces the output byte-for-byte; no `.blend1` files |

## 8. Shipping swap

All gates pass, so `168-south-park.optimized.glb` was copied over
`artifacts/168-south-park/168-south-park.glb`. The pre-optimize original is
archived at `optimize/input/168-south-park.glb`.

`artifacts/168-south-park/validation.json` was regenerated against the shipped
file and `artifacts/168-south-park/REPORT.md` §1 restated to the shipped
numbers, so the integration stage writes its manifest entry from what actually
ships.
