# Orpheum Theatre — optimize pass (stage 4)

Ran `docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md` v2 on `artifacts/orpheum-theatre/`
with `ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`.
Scripts are adapted copies of `tools/glb-optimize/`; the pre-optimize asset is
archived byte-for-byte at `input/orpheum-theatre.glb`.

## Result

| | Input | Shipped | Δ |
|---|---|---|---|
| File, raw | 488,736 B | **193,912 B** | **−60.3 %** |
| File, gzip | 81,871 B | 119,175 B | +45.6 % (see §Bytes) |
| Objects / draw submeshes | 242 | **11** | −95.5 % |
| Triangles | 7,200 | 7,200 (Blender evaluates 7,193 on the packed file) | −0.1 % |
| Vertices | 14,240 | 4,080 (Phase B), 13,529 as re-imported from the packed file | −71 % pre-pack |
| Materials | 11 | 11, identical set | — |
| bbox | 67.6506 × 77.6234 × 27.2 m | identical to 5 dp | 0 |
| Origin | (0, 0, 0) | identical | 0 |

## Toolchain

Blender 5.2.0 LTS · `gltfpack` 0.24 via `npx` · node + pinned three 0.185 in
`g3check/` · python3 + Pillow · gzip. All steps are the deterministic scripts in
this directory; re-running them on `input/` reproduces the output.

## Phase B — the four-variant table

The prompt's §3.3 says to skip the limited dissolve on assets with large coplanar
ring bands, and this asset is almost nothing but: every parapet, tile eave and cap
is a `ring_prism`/`band_prism` annulus. Rather than take that on faith, all four
weld × dissolve variants were built and packed:

| variant | tris | verts | mid GLB | packed | packed gzip |
|---|---|---|---|---|---|
| weld + dissolve | 7,316 | 4,138 | 372,344 | 198,080 | 135,962 |
| **weld only (shipped)** | 7,496 | 4,228 | 388,640 | **198,888** | **123,156** |
| dissolve only | 7,284 | 14,432 | 399,824 | 209,864 | 137,109 |
| neither | 7,496 | 14,644 | 415,640 | 208,120 | 121,121 |

(Measured before the collinear fix below; the ranking did not change after it.)

**Shipped: weld on, dissolve off.** The dissolve buys 808 raw bytes — 0.4 % — and
costs 12.8 KB of gzip, and it is the one step in Phase B that can manufacture
degenerate geometry on exactly this kind of asset. The weld is where the real win
is: 14,644 → 4,228 vertices, because every box and prism arrives with split
vertices per face.

Interior-face deletion removed 0 faces: the occluder rule only trusts closed solids
that fill ≥ 95 % of their AABB, and this asset's overlapping prisms are mostly
L- and ring-shaped, so nothing qualified. Curve retessellation was skipped — the
arcade arch heads are already at 8 segments and are silhouette geometry.

Join-per-material is the headline: 242 objects → 11 (9 join groups plus two
materials that were already single objects), which is what takes the draw submeshes
from 242 to 11. Phase B measured: 7,200 tris / 14,240 verts in → 7,200 / 4,080 out,
i.e. the weld alone removed 71 % of the vertices and no triangles at all.

## A degenerate sliver, found here and fixed upstream

The first shipping swap failed the stage-2 contract validator on
`no_degenerate_geometry`: one zero-area triangle in `low_cap`, edges
18.94493 + 8.93000 = 27.87493 — perfectly collinear.

It was **not** created by this pass. `M1`, `M2` and `HM` are inserted mid-edge in
the build's footprint to split the wings, so several ring polygons carry collinear
vertex triples; Blender stores the cap n-gon happily and the glTF exporter
triangulates it into a sliver. It survives the weld (its edges are metres long, not
millimetres) and it passes an area-based degeneracy test only by luck of which
triangulation the exporter picks — which is why stage 2 passed on the unpacked
242-object build and failed on the packed 11-object one.

Fixed at the source rather than worked around: `build_orpheum_theatre.py` now drops
collinear vertices from every ring polygon before building its faces
(`collinear_drops` / `without`). The asset rebuilt at 7,200 triangles instead of
7,496, `optimize/input/` was refreshed from it, and every gate was re-run from
scratch on the new pair. Shipped asset: **0 degenerate triangles**.

## Phase C — packing

```
npx gltfpack@0.24 -i mid.glb -o orpheum-theatre.optimized.glb -c -km -kn -noq
```

`-km -kn` mandatory (glow-ness is name-only; without `-km` gltfpack merges
`Toy_white_Glow` into `Toy_trim` and kills the night layer — the two have identical
parameters here, so this asset would have hit it). `-noq` per the repo standard:
unquantized float32, matching `pipeline/compress-assets.mjs`.

### Bytes

Raw is down 60.3 %, which is the number the repo's other assets report and the one
that matters for `EXT_meshopt_compression` parse cost and GPU upload. **Gzip goes
up**, because meshopt output is already entropy-coded and gzips poorly, whereas a
plain Blender GLB gzips extremely well. Both numbers are recorded here so nobody
re-opens it: the shipped file is 193,912 B on disk, ~119 KB over the wire, well
inside AGENTS' ≤ 500 KB compressed budget either way.

## Gates

| Gate | Result | Evidence |
|---|---|---|
| G1 Contract | **PASS** | material set identical (11, both glow names preserved); no `Toy_body`; no manifest node names to protect |
| G2 Geometry | **PASS** | bbox identical to 5 dp; origin (0,0,0); all signed volumes positive; ray test 0 flipped of 17,233 hits over 22,500 rays |
| G3 Round-trip | **PASS** | Blender re-import clean; `g3check` (pinned three 0.185) `G3-OK`, 11 meshes, 7,200 tris, 11 materials, bbox matches |
| G4 Appearance | **PASS** | mean abs RGB delta 0.033 % day-near, 0.033 % day-far, 0.108 % night-near, 0.121 % night-far, 0.045–0.212 % on the four elevations — all far inside the ≤ 4 % near / ≤ 2 % far gates. The ×8-amplified diffs are sampling noise on bevel highlights (denoising is off); nothing structural, no missing element, no silhouette change |
| G5 Draw submeshes | **PASS** | 242 → 11 |
| G6 Size | **PASS** | 488,736 → 193,912 B raw, −60.3 %, at the 60 % target |
| G7 GPU budget | n/a | bake mode off |
| G8 Hygiene | **PASS** | re-import object count matches; deterministic re-run reproduces the output; no `.blend1` left |

## Shipping swap

`orpheum-theatre.optimized.glb` was copied over `artifacts/orpheum-theatre/orpheum-theatre.glb`.
The stage-2 contract validator was re-run on the shipped file: **overall PASS, all 15
checks true**, 7,193 triangles, 11 objects, 0 degenerate, 0 invalid loop normals,
flipped fraction 0.0. `validation.json` and `REPORT.md` in the parent directory carry
the shipped numbers, and the review renders were regenerated from the shipped GLB.
