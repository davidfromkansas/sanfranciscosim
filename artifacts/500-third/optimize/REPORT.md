# 500 Third Street — GLB optimize report

Stage 4 of `docs/asset-pipeline/ADDRESS-TO-ASSET.md`, run 13 August 2026 with the
defaults: `ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`.

Input: `optimize/input/500-third.glb` — a byte-for-byte copy of the approved
asset (sha1 `1656241af6e2b439e0ce36df888035099af2e6bc`, 1,151,788 B), never
modified in place.

## Result

| Metric | Input | Shipped | Δ |
|---|---|---|---|
| Raw bytes | 1,151,788 | **183,916** | −84.0% (6.26×) |
| Gzipped bytes | 167,849 | **91,026** | −45.8% |
| Triangles | 17,320 | 17,320 | 0 |
| Vertices | 35,184 | 31,545 | −10.3% |
| Objects | 546 | **13** | −97.6% |
| Draw primitives | 547 | **14** | −97.4% |
| Materials | 13 | 13 | identical set |
| bbox (m) | 75.2386 × 76.2383 × 26.5000 | 75.2378 × 76.2383 × 26.5017 | ≤ 1.7 mm |
| bbox min | −37.6187, −38.1188, 0.0 | −37.6187, −38.1188, 0.0 | 0 |

Comfortably past the 60% `TARGET_REDUCTION`, and inside the AGENTS budget of
≤ 500 KB compressed on disk with room to spare.

## Toolchain

| Tool | Version |
|---|---|
| Blender | 5.2.0 LTS (fbe6228777e7, 2026-07-14) |
| gltfpack | `npx gltfpack@0.24`, flags `-cc -kn -km` |
| three (g3check) | pinned in `g3check/package.json` |
| Python | 3.9 + Pillow 11.3.0 |

`-km` is not optional: without it gltfpack merges identical-parameter materials
across the `_Glow` boundary (glow-ness is name-only), which would silently kill
the night layer. Verified on the output — both `Toy_glassl_Glow` and
`Toy_white_Glow` survive as distinct materials, and the night A/B render shows
the crown band and the lit bays intact.

`ALLOW_MESHOPT: yes` is safe here: `grep -rn setMeshoptDecoder app/src/` hits
`app/src/gltf.js:10` and `app/src/assets.js:406`.

## Waste census and where the bytes went

The census predicted — correctly — that this asset's cost was **node and
accessor overhead, not geometry**. 546 objects carrying 17,320 triangles is
~32 triangles per object: an authoring style of one closed solid per element
(every mullion, every window reveal, every flag its own mesh). The geometry
itself was already lean, and the authoring validator had already driven
degenerate faces to zero.

| Technique | Predicted | Actual |
|---|---|---|
| Weld ≤ 1 mm, per object | small | −0 tris, −3,639 verts |
| Delete degenerate faces | 0 | 0 (the authoring validator gates this) |
| Buried interior faces | small | 0 |
| Limited dissolve 0.05°, coplanar | small | 0 |
| **Join per material** | **the whole win** | **546 → 13 objects, 547 → 14 primitives** |
| Quantization + meshopt (`-cc`) | large | 874,584 → 183,916 B |

Phase B alone took 1,151,788 → 874,584 B. Phase C did the rest. No curve
retessellation was needed — there are no curved shells in this asset.

`ALLOW_BAKE` stayed `no`: the contract forbids textures, and there is no
bakeable facade relief worth 3× on a building whose detail is flat-coloured
boxes and whose window grid is already the cheapest possible expression of it.

## Gate results

| Gate | Result | Evidence |
|---|---|---|
| **G1 Contract** | PASS | material name set identical (13, incl. both `_Glow`); no `Toy_body`; node names not manifest-referenced |
| **G2 Geometry** | PASS | bbox within 1.7 mm; origin unchanged; all 13 signed volumes positive; `inverted_solids: []`; flipped fraction **0.0000** of 16,411 ray hits |
| **G3 Round-trip** | PASS | re-imports in Blender; `g3check` loads it with pinned three — 14 meshes, 17,320 tris, 13 materials, no decode errors |
| **G4 Appearance** | PASS | worst mean delta 0.378%, gates are ≤2% far / ≤4% near |
| **G5 Draw submeshes** | PASS | 14 ≤ 547 |
| **G6 Size** | PASS | −84.0% raw, target 60% |
| **G7 GPU budget** | n/a | bake mode off |
| **G8 Hygiene** | PASS | re-import object count matches; the scripts here reproduce the output from the input; no `.blend1` left in `optimize/` |

### G4 — A/B pixel deltas

| View | Mean abs RGB | Max px delta |
|---|---|---|
| day near (1.5× long axis) | 0.1913% | 55 |
| day far (6× long axis) | 0.1469% | 32 |
| night near | 0.1450% | 86 |
| night far | 0.1314% | 48 |
| elevation N (3rd Street) | 0.3777% | 49 |
| elevation E (SE) | 0.2905% | 102 |
| elevation S (Ritch) | 0.2361% | 36 |
| elevation W (Bryant) | 0.3242% | 46 |

**Looked at, not just measured.** The pairs in `renders/` are visually
indistinguishable: same silhouette, same nine/seven/seven bay rhythm, same
charcoal storefront band, same roof composition, same glow set at night — the
crown sign band still reads as the hero and the scattered lit bays as the
supporting rhythm. The residual is quantization dither on large flat surfaces;
the isolated max-delta pixels sit on bevel highlights along the pilaster edges
and the parapet coping, where a 16-bit position snap moves a shading boundary by
under a pixel. Nothing a player would notice.

## The shipping swap

`500-third.optimized.glb` is now `artifacts/500-third/500-third.glb`. The
pre-optimize original is archived at `optimize/input/500-third.glb`.

`artifacts/500-third/validation.json` keeps the **authoring** validation (it
gates the authored contract: base-center origin, applied transforms, outward
normals, no textures, palette materials) and gains a `shipped` block with the
packed file's numbers. The authoring check `transforms_applied` deliberately
does not apply to the packed file — gltfpack bakes quantization scale into node
transforms — which is why the packed file is gated by this directory's
`validation.json` and `g3check` instead.

## Reproducing

```bash
BLENDER=/Applications/Blender.app/Contents/MacOS/Blender
"$BLENDER" -b --python inspect.py  -- input/500-third.glb inspect.json
"$BLENDER" -b --python optimize.py -- input/500-third.glb mid.glb phaseb_stats.json
npx gltfpack@0.24 -i mid.glb -o 500-third.optimized.glb -cc -kn -km
"$BLENDER" -b --python validate.py -- input/500-third.glb 500-third.optimized.glb validation.json
(cd g3check && npm install && node check.mjs ../500-third.optimized.glb)
"$BLENDER" -b --python render_ab.py -- input/500-third.glb renders/in
"$BLENDER" -b --python render_ab.py -- 500-third.optimized.glb renders/out
python3 diff_ab.py renders diffs.json
```

`render_ab.py` was given a Metal-GPU device selection in this run: the machine
was hosting a dozen parallel Blender sessions and CPU Cycles was getting ~5% of
one core. Both sides of every pair render on the same device, so the comparison
is unaffected.
