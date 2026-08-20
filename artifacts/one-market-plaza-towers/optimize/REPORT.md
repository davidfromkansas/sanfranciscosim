# One Market Plaza towers — GLB optimize pass (stage 4)

`docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md`, 19 August 2026.
`ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`.
Blender 5.2.0 LTS, `gltfpack 0.24`, node v22.19.0.

## 0. Result

| Metric | Input | Shipped | Δ |
|---|---|---|---|
| Raw bytes | 644,940 (629.8 KB) | **218,144 (213.0 KB)** | **−66.2%** |
| Gzip −9 | 118,999 | 128,963 | +8.4% |
| Triangles | 9,428 | 8,925 | −5.3% |
| Objects | 329 | **10** | −97.0% |
| Draw submeshes | 330 | **12** | −96.4% |
| Materials | 10 | 10 | identical set |
| bbox / origin | 123.0233 × 128.8103 × 177.6 | identical | 0 |

All gates **G1–G6, G8 PASS**; G7 n/a (`ALLOW_BAKE: no`).

## 1. Phase B, and the sliver that decided the variant

Both switchable steps measured rather than assumed:

| Variant | Tris | Packed raw | Packed gzip | Slivers (area < 1e-4 m2) |
|---|---|---|---|---|
| weld + dissolve | 8,845 | 212,840 | 137,421 | **1** — area **2.4e-07 m2**, longest edge **4.71 m**, in the joined `grp_Toy_white` |
| **weld only — shipped** | 8,925 | 218,144 | **128,963** | **0** |

`GLB-OPTIMIZE-PROMPT` §3 step 3 warns that a strictly-coplanar dissolve turns a
ring band's annulus into one ngon whose re-triangulation emits hairline slivers.
**This asset is the first measured instance of it in this repo.** It has five
ring bands (podium parapet, two tower parapets, the retail band, the garden
kerb); the neighbouring `1-market` asset has *eight* and produced none, because
the bevels on its bands break each annulus into separate coplanar runs. The
failure is real, it is asset-specific, and it has to be measured in both
directions rather than assumed.

Audited two ways: `slivergeo.py` on the **mid** (unpacked) file, where the
slivers are born, and `slivercheck.py` reading the `NORMAL` accessor min/max out
of the **packed** binary, because Blender recomputes loop normals on import and
hides the collapse.

The dissolve was worth 5.3 KB of raw and cost 8.5 KB of gzip, so rejecting it is
free in both directions. The **weld** is the whole win, as it was on 1-market.

The interior-face pass removed **503 triangles** of provably buried geometry —
the podium's top cap under each shaft and the pier backs — which the occluder
rule could reach here because the shafts are closed solids filling ≥95% of their
own AABBs, unlike 1-market's U-shaped body.

## 2. Phase C — packing

```
npx gltfpack@0.24 -i mid_weldonly.glb -o one-market-plaza-towers.optimized.glb -c -km -kn -noq
```

`-km -kn` mandatory: glow-ness is name-only, and without them gltfpack merges
`Toy_glassl_Glow` into `Toy_glassl` and silently kills the night layer. Verified
on the output — all 10 names present, both `_Glow` materials distinct. `-noq` per
the repo standard. `EXT_meshopt_compression` is the only extension.

## 3. Gates

| Gate | Result |
|---|---|
| **G1** material set identical, `_Glow` separate, no `Toy_body` | PASS |
| **G2** bbox and origin identical, 0 inverted signed volumes, 0.00% ray residual | PASS |
| **G3** Blender re-import + pinned-three `g3check`: `G3-OK {"ok":true,"meshes":12,"tris":8925}` | PASS |
| **G4** day+night × near+far + 4 elevations | PASS — mean abs RGB **0.0004–0.0076%** day/elevations, **0.50–0.56%** night |
| **G5** draw submeshes 330 → 12 | PASS |
| **G6** −66.2% against a 60% target | PASS |
| **G8** deterministic, no foreign geometry, no `.blend1` | PASS |

**G4 in words:** indistinguishable. The night figure is an order of magnitude
above the day one because the night frame is almost entirely black with thin
bright glow strips, where a percentage delta is at its most sensitive to
denoiser sampling; side by side the two frames show the same lit slot columns,
the same retail band and the same canopies, with nothing missing.

## 4. Shipping swap

`one-market-plaza-towers.optimized.glb` copied over the artifact's shipping GLB;
the pre-optimize build archived byte-for-byte at `optimize/input/`. The asset's
`validation.json` and `REPORT.md` regenerated from the shipped file: **8,917
tris** (as re-counted on the packed re-import), 213.0 KB, 10 objects, 12 draw
submeshes, bbox top exactly 177.600 m, loader scale 1.000.
