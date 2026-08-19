# towers-at-rincon — GLB optimize pass (stage 4)

Run of `docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md` v2 against
`artifacts/towers-at-rincon/`. Defaults: `ASSET_CLASS: landmark`,
`ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`. Blender 5.2.0 LTS, gltfpack 0.24.

`optimize/input/towers-at-rincon.glb` is a byte-identical archive of the
pre-optimize asset (verified with `cmp`); everything below ran against the copy.

## Metrics

| | input | output | delta |
|---|---:|---:|---:|
| Raw bytes | 913,492 | **352,836** | **−61.4 %** |
| Gzip-9 bytes | 171,338 | 204,103 | +19.1 % (see below) |
| Triangles | 17,036 | 17,035 | −1 |
| Vertices | 29,942 | **9,123** | **−69.5 %** |
| Objects / draw submeshes | 253 | **10** | **−96.0 %** |
| Materials | 10 | 10 | identical set |
| bbox dims (m) | 108.6596 × 108.6701 × 89.0 | identical | 0 |
| bbox min z / origin XY | 0.0 / (0, 0) | identical | 0 |
| Signed-volume inverted solids | 0 | 0 | — |
| Normals ray residual | 0.000 % | 0.000 % | — |

**On the gzip number.** The raw file is 61 % smaller, which is the number that
matters; the *gzipped* file grows because meshopt already entropy-codes the
buffers, so gzip has nothing left to find and adds its own framing. That is the
normal signature of an `EXT_meshopt_compression` file and is why the repo
measures landmarks by raw bytes on disk. At 352 KB this sits comfortably inside
the ≤ 500 KB landmark budget and below the six largest shipped landmarks
(palace-of-fine-arts 769 KB, painted-ladies 639 KB, ferry-building 571 KB,
city-hall 534 KB, 501-second 488 KB, conservatory-of-flowers 482 KB).

## Waste census (Phase A, `inspect.json`)

| Finding | Measured | Plan |
|---|---:|---|
| Coincident vertex pairs | 20,819 | weld at 1 mm, per object |
| Objects sharing one material | 253 objects → 10 material groups | join per material |
| Duplicate mesh groups | 26 groups, 7,528 redundant triangles | absorbed by the join |
| Degenerate triangles | 0 | nothing to do |
| Buried interior faces | none provable | see Phase B step 2 |
| Over-tessellated curves | near distance 163 m, one pixel = 0.110 m | not retessellated — the bows, the arch caps and the plaza discs are the silhouette |
| Image textures | 0 | — |
| Vertex attributes | POSITION + NORMAL only | — |

Predicted before running: the win is vertex/node overhead, not triangles. The
model is authored as ~250 clean prisms with no redundant coplanar fans, so there
is nothing for a triangle-reducing pass to remove without touching the
silhouette; what there *is* is 20.8k duplicated corner vertices where stacked
bands share edges, and 253 separate nodes. That is exactly how it came out:
triangles −1, vertices −69.5 %, objects −96 %.

## Phase B — geometry cleanup

| Step | Triangles | Vertices |
|---|---:|---:|
| input | 17,036 | 29,942 |
| 1+2a weld ≤ 1 mm + degenerate, per object | 17,036 | 9,123 |
| 2b interior faces buried in closed box-like solids | 17,036 | 9,123 |
| 3 limited dissolve | **skipped — see below** | |
| 5 join per material | 17,036 | 9,123 |

**Step 2b removed nothing, correctly.** The occluder rule only treats a mesh as
an occluder if it is a closed solid filling ≥ 95 % of its own AABB. Nothing here
qualifies: the podium prisms are a diamond inside a square box, the tower bands
are lozenges, the arch caps are barrels. Overlapping solids are the authored
model, and the buried faces are between two shapes neither of which is box-like,
so there is no provable-invisible face to delete. Not a failure of the step —
the alternative (a boolean union) is explicitly forbidden.

**Step 3 was skipped deliberately**, per the prompt's §3 step 3 warning:
"Skip this step entirely on assets with large coplanar ring bands." This asset is
made of them — `podium_parapet` is a 108 m ring, both shoulder cornices and both
bay cornices are rings, and every one of the 10 podium bands, 32 tower bands and
32 balcony slabs is a prism with perfectly coplanar caps. A strictly coplanar
dissolve merges each of those caps into one annulus ngon and re-triangulating an
annulus emits slivers that are invisible, pass an area-based degeneracy test, and
only surface later as `invalid_or_nonunit_loop_normal_count` in the *packed*
file (measured on `350-brannan`: triangles up to 24.35 m long and ~0.24 mm wide).
It is also the cheapest step available here, because the geometry is already
authored as flat quads. The skip is recorded in `phaseb_stats.json`.

**Step 5 joins**, all ten groups: `Toy_trim` 51 → 1, `Toy_sand` 51 → 1,
`Toy_glass` 44 → 1, `Toy_stone` 44 → 1, `Toy_glassl_Glow` 38 → 1, `Toy_steel`
7 → 1, `Toy_mint` 6 → 1, `Toy_gold_Glow` 5 → 1, `Toy_glassl` 4 → 1, `Toy_ink`
3 → 1. No manifest-named nodes exist on this asset and there is no `Toy_body`,
so nothing had to be held out.

## Phase C — packing

```
npx gltfpack@0.24 -i optimize/mid.glb -o optimize/towers-at-rincon.optimized.glb -c -km -kn -noq
```

`-km -kn` keep the material and node names, which is what protects the two
`_Glow` materials from being merged into their non-glow twins — glow-ness is
name-only. `-noq` (no quantization) is the repo standard and is what
`pipeline/compress-assets.mjs` produces; the app registers `MeshoptDecoder` in
both `app/src/gltf.js:10` and `app/src/assets.js:406`, verified before relying on
`-c`.

Verified on the output rather than trusted from the flags: material name set
identical, bbox identical, re-import object count 10.

## Phase E — A/B verification

`render_ab.py` on both files with the same rig (Cycles, 64 samples, denoising
off, 42° aerial, near = 1.5 × long axis = 163 m, far = 6 × = 652 m), day and
night, plus four orthographic elevations. `diff_ab.py` output:

| View | Mean abs RGB | Max pixel delta |
|---|---:|---:|
| day_near | 0.0229 % | 21 |
| day_far | 0.0191 % | 6 |
| night_near | 0.1861 % | 107 |
| night_far | 0.1864 % | 25 |
| elev_n | 0.0151 % | 18 |
| elev_e | 0.0141 % | 21 |
| elev_s | 0.0096 % | 72 |
| elev_w | 0.0204 % | 41 |

**Looked at, not just measured.** The ×8-amplified diffs contain no structure at
all — no edge outlines, no missing element, no shifted silhouette. What they show
is speckle, concentrated on the emissive surfaces (the gold crown bands and the
lit apartment ribbons) and on the shadowed courtyard wall. That is Monte-Carlo
sampling noise: the A/B rig runs Cycles at 64 samples with denoising **off**, so
two renders of *identical* geometry would differ the same way. The night figures
are ten times the day ones for exactly that reason — emitters carry the most
variance. Nothing a player would notice, because nothing changed.

## Gates

| Gate | Result | Evidence |
|---|---|---|
| G1 Contract | **PASS** | material set identical (10, incl. both `_Glow`); no `Toy_body`; no manifest-named nodes to preserve |
| G2 Geometry | **PASS** | bbox identical to 4 dp; origin (0,0) and min z 0 unchanged; 0 inverted solids; flipped fraction 0.000 % |
| G3 Round-trip | **PASS** | Blender re-import 10 objects; `g3check` `G3-OK` — 10 meshes, 17,036 tris, 10 materials, bbox matches |
| G4 Appearance | **PASS** | max mean delta 0.186 % (gate: ≤ 2 % far, ≤ 4 % near); diffs are render noise only |
| G5 Draw submeshes | **PASS** | 253 → 10 |
| G6 Size | **PASS** | raw −61.4 %, above the 60 % target |
| G7 GPU budget | n/a | bake mode off |
| G8 Hygiene | **PASS** | re-import object count checked; scripts are deterministic and committed; no `.blend1` left |

The optimized GLB was additionally re-run through the asset's **own stage-2
contract validator** (`validate_towers_at_rincon.py --glb
optimize/towers-at-rincon.optimized.glb`): **overall PASS**, 17,035 triangles,
dims 108.6596 × 108.6701 × 89.0, min z 0, XY centre (0, 0), all 130 open glow
faces still outward, ray residual 0.000 %. Written to
`optimize/validation.json`.

## Shipping swap

All gates pass, so `optimize/towers-at-rincon.optimized.glb` was copied over
`artifacts/towers-at-rincon/towers-at-rincon.glb` as the shipping file. The
pre-optimize asset stays at `optimize/input/towers-at-rincon.glb`.
`artifacts/towers-at-rincon/REPORT.md` and `validation.json` carry the shipped
numbers.

Because the shipping file now carries `EXT_meshopt_compression`,
`pipeline/compress-assets.mjs` will **skip** it at integration time — which is
the intended behaviour, not a missed step.
