# 550 Third Street — GLB optimize report

Stage 4 of `docs/asset-pipeline/ADDRESS-TO-ASSET.md`, run 12 August 2026 with the
defaults: `ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`.

Input: `optimize/input/550-third.glb` — a byte-for-byte copy of the approved
asset (sha1 `1a135aa8…`, 380,076 B), never modified in place.

## Result

| Metric | Input | Shipped | Δ |
|---|---|---|---|
| Raw bytes | 380,076 | **69,364** | −81.8% (5.48×) |
| Gzipped bytes | 63,101 | **39,716** | −37.1% |
| Triangles | 6,280 | 6,244 | −36 |
| Vertices | 12,428 | 10,026 | −19.3% |
| Objects | 135 | **13** | −90.4% |
| Draw primitives | 136 | **14** | −89.7% |
| Materials | 13 | 13 | identical set |
| bbox (m) | 49.2093 × 50.4098 × 11.0000 | 49.2098 × 50.4098 × 11.0001 | ≤ 0.5 mm |
| bbox min | −24.5827, −25.1840, 0.0 | −24.5827, −25.1840, 0.0 | 0 |

Comfortably past the 60% `TARGET_REDUCTION`.

## Toolchain

| Tool | Version |
|---|---|
| Blender | 5.2.0 LTS (fbe6228777e7, 2026-07-14) |
| gltfpack | `npx gltfpack@0.24`, flags `-cc -kn -km` |
| three (g3check) | pinned in `g3check/package.json` |
| node | v22.19.0 |
| Python | 3.9 + Pillow 11.3.0 |

`-km` is not optional: without it gltfpack merges identical-parameter materials
across the `_Glow` boundary (glow-ness is name-only), which would silently kill
the night layer. Verified on the output — both `Toy_glassl_Glow` and
`Toy_white_Glow` survive as distinct materials.

`ALLOW_MESHOPT: yes` is safe here: `grep -rn setMeshoptDecoder app/src/` hits
`app/src/gltf.js:10` and `app/src/assets.js:406`.

## Waste census and where the bytes went

The census predicted — correctly — that this asset's cost was **node and
accessor overhead, not geometry**. 135 objects carrying 6,280 triangles is
~46 triangles per object: an authoring style of one closed solid per element
(every mullion, every hedge, every heat pump its own mesh). The geometry itself
was already lean.

| Technique | Predicted | Actual |
|---|---|---|
| Weld ≤ 1 mm, per object | small | −0 tris (the build emits welded solids) |
| Delete degenerate faces | 0 | 0 (the authoring validator already gates this) |
| Buried interior faces | small | −36 tris |
| Limited dissolve 0.05°, coplanar | small | folded into the above |
| **Join per material** | **the whole win** | **135 → 13 objects, 136 → 14 primitives** |
| Quantization + meshopt (`-cc`) | large | 292,224 → 69,364 B |

Phase B alone took 380,076 → 292,224 B. Phase C did the rest. No curve
retessellation was needed — there are no curved shells in this asset.

`ALLOW_BAKE` stayed `no`: the contract forbids textures, and there is no
bakeable facade relief worth 3× on a building whose detail is flat-coloured
boxes.

## Gate results

| Gate | Result | Evidence |
|---|---|---|
| **G1 Contract** | PASS | material name set identical (13, incl. both `_Glow`); no `Toy_body`; node names not manifest-referenced |
| **G2 Geometry** | PASS | bbox within 0.5 mm; origin unchanged; all 13 signed volumes positive; `inverted_solids: []`; flipped fraction **0.0000** of 13,804 ray hits |
| **G3 Round-trip** | PASS | re-imports in Blender; `g3check` loads it with pinned three — 14 meshes, 6,244 tris, 13 materials, no decode errors |
| **G4 Appearance** | PASS | see the table below — worst mean delta 0.396%, gates are ≤2% far / ≤4% near |
| **G5 Draw submeshes** | PASS | 14 ≤ 136 |
| **G6 Size** | PASS | −81.8% raw, target 60% |
| **G7 GPU budget** | n/a | bake mode off |
| **G8 Hygiene** | PASS | re-import object count matches; deterministic re-run reproduces the output; no `.blend1` left |

### G4 — A/B pixel deltas

| View | Mean abs RGB | Max px delta |
|---|---|---|
| day near (1.5× long axis) | 0.0875% | 57 |
| day far (6× long axis) | 0.0797% | 18 |
| night near | 0.2655% | 45 |
| night far | 0.2424% | 33 |
| elevation N | 0.3589% | 132 |
| elevation E | 0.0663% | 99 |
| elevation S | 0.0851% | 30 |
| elevation W | 0.3964% | 46 |

**Looked at, not just measured.** The pairs in `renders/` are visually
indistinguishable: same silhouette, same skylight row, same penthouse slab and
deck, same glow set at night, nothing missing. The residual is quantization
dither on large flat surfaces — the isolated max-delta pixels sit on bevel
highlights along the parapet coping and the pilaster edges, where a 16-bit
position snap moves a shading boundary by under a pixel. There is nothing here a
player would notice.

## The shipping swap

`550-third.optimized.glb` is now `artifacts/550-third/550-third.glb`. The
pre-optimize original is archived at `optimize/input/550-third.glb`.

`artifacts/550-third/validation.json` keeps the **authoring** validation (it
gates the authored contract: base-center origin, applied transforms, outward
normals, no textures, palette materials) and gains a `shipped` block with the
packed file's numbers. The authoring check `transforms_applied` deliberately
does not apply to the packed file — gltfpack bakes quantization scale into node
transforms — which is why the packed file is gated by this directory's
`validation.json` and `g3check` instead.

## Reproducing

```bash
BLENDER=/Applications/Blender.app/Contents/MacOS/Blender
"$BLENDER" -b --python inspect.py  -- input/550-third.glb inspect.json
"$BLENDER" -b --python optimize.py -- input/550-third.glb mid.glb phaseb_stats.json
npx gltfpack@0.24 -i mid.glb -o 550-third.optimized.glb -cc -kn -km
"$BLENDER" -b --python validate.py -- input/550-third.glb 550-third.optimized.glb validation.json
(cd g3check && npm install && node check.mjs ../550-third.optimized.glb)
"$BLENDER" -b --python render_ab.py -- input/550-third.glb renders/in
"$BLENDER" -b --python render_ab.py -- 550-third.optimized.glb renders/out
python3 diff_ab.py renders diffs.json
```
