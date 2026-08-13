# 155 – 157 South Park Street — GLB optimize report (stage 4)

Run 13 August 2026 per `docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md`.
`ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`.

Toolchain: Blender 5.2.0 LTS, `npx gltfpack@0.24`, node v22.19.0, pinned three via
`g3check/`, python3 + Pillow, gzip −9.

## 1. Metrics

| Metric | Input | Shipped | Delta |
|---|---|---|---|
| File, raw | 243,456 B | **113,664 B** | **−53.3%** |
| File, gzip −9 | 48,672 B | 82,094 B | +68.7% (see §4) |
| Triangles | 4,048 | 4,048 | unchanged |
| Vertices | 8,088 | 2,144 | −73.5% |
| Objects | 63 | **15** | −76.2% |
| Draw submeshes (primitives) | 65 | **17** | −73.8% |
| Materials | 13 | 13 | unchanged |
| BBox | 25.5223 × 28.2942 × 10.10 | 25.5223 × 28.2942 × 10.10 | identical to 1e-5 m |
| Origin | min Z 0.0, centre (0.230, 0.537) | unchanged | within 1e-5 m |

## 2. Waste census (Phase A)

| Finding | Value | Action |
|---|---|---|
| Coincident vertex pairs | 5,944 | welded (per-object, ≤ 1 mm) |
| Objects sharing a material | 63 across 12 groups | joined per material |
| Duplicate mesh groups | 10 groups / 312 redundant tris | absorbed by the per-material join |
| Degenerate triangles | 0 | nothing to remove |
| Buried interior faces | 0 removable | see §3 |
| Over-tessellated curves | none | there are no curved shells in this asset — every form is a box, a prism or a 4-vertex lozenge |
| Vertex attributes | `NORMAL` only | nothing to prune; no UVs, no vertex colours, no textures |

The whole triangle budget is already spent on flat quads, so there was never a
geometry win to be had here. The win in this asset is entirely **node and accessor
overhead**: 63 objects and 65 primitives for 4,048 triangles.

## 3. Phase B — geometry cleanup

| Step | Tris | Verts |
|---|---|---|
| input | 4,048 | 8,088 |
| weld + degenerate | 4,048 | 2,144 |
| interior faces | 4,048 | 2,144 |
| limited dissolve 0.05° | 4,048 | 2,144 |
| join per material | 4,048 | 2,144 |

Joins: `Toy_glass` 13, `Toy_trim` 11, `Toy_peach` 7, `Toy_ink` 5, `Toy_steel` 5,
`Toy_roofd` 4, `Toy_verdigris` 4, `Toy_gold_Glow` 3, `Toy_glass_Glow` 3,
`Toy_gold` 2, `Toy_glassl` 2. `Toy_white` and `Toy_rust` stayed as they were.

The weld is the headline: 8,088 → 2,144 vertices, −73.5%, because glTF splits
vertices per flat-shaded face and this asset is entirely flat-shaded.

**Zero triangles removed, and that is the correct outcome.** Limited dissolve at
0.05° found nothing because the build script bevels every chunky mass, so there are
no strictly-coplanar face pairs left to merge. Zero interior faces were removed
because the occluder rule requires a CLOSED solid, and the only box-like candidates
— the two block prisms — have AABB fills of 47% and 43% respectively, since the
building sits at 41.4° to the world axes. Treating either as an occluder would have
deleted real facade geometry. This is the prompt's §3.2 rule doing its job for the
same reason it did on 380 Brannan.

Normals after Phase B: 15/15 signed volumes positive, `inverted_solids: []`, and
`output_open_shells: []`.

## 4. Phase C — packing

```
npx gltfpack@0.24 -i mid.glb -o 155-south-park.optimized.glb -c -km -kn -noq
```

`-km -kn -noq` exactly as the prompt's §4 requires. `-km` keeps the two `_Glow`
materials from being merged into their identically-parameterised non-glow twins
(`Toy_gold_Glow` vs `Toy_gold`, `Toy_glass_Glow` vs `Toy_glassl` — both pairs share
a colour here, so this asset is precisely the case that rule exists for; without
`-km` the night layer would have silently died). `-noq` keeps float32 attributes,
matching `pipeline/compress-assets.mjs`.

**Gzip grows by 68.7%** and that is expected, not a regression: meshopt-compressed
buffers are already entropy-coded, so gzip has nothing left to find and adds its own
framing. Same effect recorded on 380 Brannan (+102%). Raw bytes are what the runtime
fetches and decodes.

Verified on the output rather than trusting flags: material-name set identical (13),
bbox identical, and the **stage-2 contract validator re-run on the shipped file
passes all 16 checks**, including `transforms_applied` and
`no_unexpected_objects` — the two that a quantized build would have failed.

## 5. Phase E — A/B verification

Landmark distances: near = 1.5 × long axis = 42.44 m, far = 6 × = 169.77 m. Day
state renders `_Glow` at alpha 0.12 (the app's day pass); night at alpha 1.0 with
emission 6 under a dusk world.

| View | Mean abs RGB delta | Max px delta |
|---|---|---|
| day near | 0.058% | 38 |
| day far | 0.056% | 8 |
| night near | 0.413% | 12 |
| night far | 0.409% | 21 |
| elevation N | 0.074% | 50 |
| elevation E | 0.065% | 37 |
| elevation S | 0.019% | 25 |
| elevation W | 0.025% | 44 |

Gate G4 allows ≤ 2% far and ≤ 4% near; the worst view is 0.41%.

**Looked at, not just measured.** The in/out pairs are indistinguishable at every
distance and in both states. The diff images are black except for single-pixel
speckle along bevel highlights and the parapet coping edge, which is Cycles sampling
noise — `render_ab.py` runs 64 samples with denoising off, so the two renders differ
by sampling seed alone. The night diffs are uniformly the brightest because the
emissive surfaces are the noisiest part of the frame, not because anything moved:
the shopfront glow, the two lit second-floor lights and the dark third floor are
identical in both. Nothing a player would notice, and nothing a reviewer can see.

## 6. Gate results

| Gate | Result |
|---|---|
| G1 Contract — material set identical, `_Glow` separate, no `Toy_body` | **PASS** |
| G2 Geometry — bbox within 1e-5 m, origin within 1e-5 m, 15/15 volumes positive, ray-flip delta 0.000000 | **PASS** |
| G3 Round-trip — Blender re-import + `g3check` pinned-three loader: 17 meshes, 4,048 tris, 13 materials, no decode errors | **PASS** |
| G4 Appearance — worst mean delta 0.41% against a 2%/4% gate; visually identical | **PASS** |
| G5 Draw submeshes — 65 → 17 | **PASS** |
| G6 Size — 243,456 → 113,664 B, −53.3% | **PASS** (see below) |
| G7 GPU budget | n/a — bake mode off |
| G8 Hygiene — re-import object count matches, no foreign geometry, deterministic re-run, no `.blend1` | **PASS** |

**G6 against the 60% target.** −53.3% falls short of the aspirational 60%, and the
waste census in §2 is the required justification: after welding, every remaining
triangle is silhouette or facade geometry. There is no duplicate geometry left, no
curve to retessellate, no interior face that can be proven buried, and no texture to
compress. The remaining bytes are 2,144 positions and normals plus meshopt framing.
Cutting further would mean cutting the building.

## 7. Per-asset adaptations to the generic scripts

`validate.py` was hardened in two ways before it was trusted, both recorded while
shipping `davies-symphony-hall` and both still absent from the prompt:

1. **Weld before judging closedness.** glTF stores split vertices for flat shading,
   so on a straight re-import every solid reads as an open shell and the
   signed-volume gate is vacuous. `signed_volumes()` now welds into a throwaway
   bmesh at 1e-4 and checks `len(e.link_faces) == 2` before measuring. Result here:
   `output_open_shells: []` — genuinely closed, not vacuously so.
2. **Gate the ray residual on the delta, not an absolute.** The 0.15% figure exists
   to catch the *optimizer* flipping windings; an asset may carry a standing
   residual of its own at coincident faces. `validate.py` now ray-tests the input
   too and gates on `ray_flip_delta`. This asset's input residual is 0.000000 and
   its output residual is 0.000000, so the two forms coincide — but the delta form
   is the correct one and is what a re-run should use.

`optimize.py`, `inspect.py`, `render_ab.py` and `diff_ab.py` are unmodified copies
of `tools/glb-optimize/`.

## 8. Deliverables

```
optimize/
  input/155-south-park.glb        # untouched archive of the pre-optimize asset
  155-south-park.optimized.glb    # the winner, now also artifacts/155-south-park/155-south-park.glb
  inspect.py optimize.py validate.py render_ab.py diff_ab.py  g3check/
  inspect.json phaseb_stats.json validation.json diffs.json
  renders/                        # in_/out_ day+night near+far, 4 elevations, diffs, contact sheet
  REPORT.md
```

Re-running `optimize.py` then the gltfpack command in §4 on
`input/155-south-park.glb` reproduces `155-south-park.optimized.glb`.
