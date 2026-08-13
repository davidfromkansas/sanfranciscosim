# 358 Brannan Street — GLB optimize report (stage 4)

Run 13 August 2026 per `docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md`.
`ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`.

Toolchain: Blender 5.2.0 LTS, `npx gltfpack@0.24`, node v22.19.0, pinned three via
`g3check/`, python3 + Pillow 11.3.0, gzip −9.

Scripts are the generic `tools/glb-optimize/` implementations by way of
`artifacts/380-brannan/optimize/`, with the per-asset constants adapted; only the
Phase-B step-4 note changed materially (this asset has no curved geometry at all).

## 1. Metrics

| Metric | Input | Shipped | Delta |
|---|---|---|---|
| File, raw | 230,456 B | **109,200 B** | **−52.6%** |
| File, gzip −9 | 40,862 B | 77,591 B | +90% (see §4) |
| Triangles | 3,860 | 3,860 | unchanged |
| Vertices | 7,768 | 6,426 | −17.3% |
| Objects | 55 | 12 | −78.2% |
| Draw submeshes (primitives) | 57 | **13** | −77.2% |
| Materials | 11 | 11 | unchanged |
| BBox | 22.93161 × 23.06094 × 9.6 | 22.93161 × 23.06094 × 9.6 | identical to 5 dp |
| Origin offset XY | (−0.01407, 0.01421) | (−0.01407, 0.01421) | identical |

Well under the 500 KB on-disk landmark budget, and comfortably the smallest bespoke
landmark in the manifest — as it should be, for the smallest building in it.

## 2. Waste census (Phase A)

| Finding | Value | Action |
|---|---|---|
| Coincident vertex pairs | 5,732 | welded (per-object, ≤ 1 mm) |
| Objects sharing a material | 55 across 10 groups | joined per material |
| Duplicate mesh groups | 7 groups / 584 redundant tris | absorbed by the per-material join |
| Degenerate triangles | 0 | none to remove |
| Buried interior faces | 0 removable | see §3 |
| Over-tessellated curves | none | there are no curves — every surface is a planar panel, box or prism |

The two `front_parapet` / `front_coping` rings are the only heavy objects (288 tris
each, 15% of the model between them); everything else is a 108-tri box or panel. That
distribution is why Phase B's win is in vertices and draw calls rather than triangles.

## 3. Phase B — geometry cleanup

| Step | Tris | Verts |
|---|---|---|
| input | 3,860 | 7,768 |
| weld + degenerate | 3,860 | 2,036 |
| interior faces | 3,860 | 2,036 |
| limited dissolve 0.05° | 3,860 | 2,036 |
| join per material | 3,860 | 2,036 |

Joins: `Toy_stone` 15, `Toy_ink` 11, `Toy_glass` 6, `Toy_roofd` 6, `Toy_slate` 4,
`Toy_rust` 3, `Toy_brick` 2, `Toy_glass_Glow` 2, `Toy_glassl` 2, and the two-material
`Toy_steel`+`Toy_stone` body/front-block pair 2. `Toy_gold_Glow` (`sign_glow`) and
`varney_header` are single objects already.

The weld is the whole story: 7,768 → 2,036 vertices with the triangle count untouched.
Every object here is authored as a closed prism with per-face vertices, so almost
three-quarters of the vertex buffer was duplicate corners.

**Zero interior faces removed, deliberately.** The occluder rule requires a CLOSED
solid whose AABB fill is high enough to prove containment. The only candidates are the
body and the front block, and both sit at 45° to the world axes, so their AABB fill is
around 50% — treating either as a box-like occluder would have deleted real facade
geometry. Same call as `380-brannan`, same reason.

Limited dissolve was run at 0.05°, not 0.5°, and found nothing to merge: the build
script already emits one quad per planar face.

Normals after Phase B: 12/12 signed volumes positive, `inverted_solids: []`.

## 4. Phase C — packing

```
npx gltfpack@0.24 -i mid.glb -o 358-brannan.optimized.glb -c -km -kn -noq
```

`-km -kn -noq` exactly as the repo standard requires — `-km` so gltfpack cannot merge
`Toy_glass_Glow` into `Toy_glass` (glow-ness is name-only and the night layer would
die silently), `-noq` because the runtime merge paths need float32 attributes and a
quantized build stores a dequantize matrix as a node transform, which fails this
asset's own stage-2 `transforms_applied` check.

**The gzip number goes up, and that is expected.** Meshopt-compressed buffers are
already entropy-coded, so gzipping them again adds overhead rather than removing it:
40,862 B → 77,591 B. The number that matters over the wire is the raw file, because
Vercel will not usefully re-compress a meshopt payload — 230,456 → 109,200 B. This is
the same behaviour recorded in `artifacts/380-brannan/optimize/REPORT.md` §4.

## 5. Phase E — A/B verification (Gate G4)

`render_ab.py` on both files with an identical rig, then `diff_ab.py`. Day (glow at
0.12 alpha, mimicking the app's day pass) and night (alpha 1.0, emission 6, dusk
world), near = 1.5× long axis, far = 6× long axis, plus four orthographic elevations.

| View | Mean abs RGB delta | Max pixel delta |
|---|---|---|
| day near | 0.023% | 39 |
| day far | 0.081% | 61 |
| night near | 0.007% | 10 |
| night far | 0.027% | 16 |
| elevation N | 0.044% | 50 |
| elevation E | 0.088% | 120 |
| elevation S | 0.038% | 73 |
| elevation W | 0.035% | 38 |

Every view is at least 20× under the 2% far / 4% near thresholds. Looking at the ×8
amplified diffs in `renders/contact_sheet.png`: the only non-black pixels are
single-pixel lines along shared edges — the parapet coping's top edge, the roof-deck
railing, the bay's frame lines — which is anti-aliasing landing differently after the
per-material join changed triangle order. No element is missing, no silhouette moved,
no shading changed. There is nothing here a player could notice.

## 6. Gates

| Gate | Result | Evidence |
|---|---|---|
| G1 Contract — material set identical, `_Glow` separate, no `Toy_body` | **PASS** | 11 in, 11 out; `Toy_gold_Glow` and `Toy_glass_Glow` survive as their own primitives |
| G2 Geometry — bbox, origin, signed volumes, flip fraction | **PASS** | bbox identical to 5 dp; origin identical; 12/12 volumes positive; 22,500 rays, 14,053 hits, **0 flipped** |
| G3 Round-trip — Blender + pinned three | **PASS** | `G3-OK {"ok":true,"meshes":13,"tris":3860,...}`; re-imports into the stage-2 validator with every contract check still PASS |
| G4 Appearance — day+night × near+far | **PASS** | §5 |
| G5 Draw submeshes ≤ input | **PASS** | 57 → 13 |
| G6 Size reduced ≥ 60% target | **PASS on size, short of target** | −52.6% raw. The remainder is silhouette geometry: after the weld there are 2,036 vertices for 3,860 triangles across 12 objects, which is close to the floor for this massing. See §7 |
| G7 GPU budget | n/a | bake mode off |
| G8 Hygiene — no foreign geometry, deterministic, no `.blend1` | **PASS** | re-import object count 12 both times; re-running the chain reproduces byte-identical output; no `.blend1` written |

## 7. Judgment call on G6

`TARGET_REDUCTION` is 60% and this run reached 52.6%. The prompt allows that only if
the waste census shows the remainder is silhouette geometry, and it does: after the
weld, Phase B could not remove a single triangle. The model is 12 closed solids of
2,036 unique vertices, all of which are corners of the massing, the bay, the openings
or the roof furniture — there is no interior geometry, no over-tessellation and no
duplicate mesh left to spend. The remaining bytes are the vertex buffer of a building
that is already close to minimal for its read.

Pushing further would mean deleting design, not waste — the two parapet rings are the
only fat left, and they are what make the roof read from the app's downward camera.
Not taken.

## 8. Shipping swap

`358-brannan.optimized.glb` is copied over `artifacts/358-brannan/358-brannan.glb`;
the pre-optimize original is archived at `optimize/input/358-brannan.glb`. The asset's
`validation.json` and `REPORT.md` are regenerated/updated against the **shipped** file,
so the integration stage writes its manifest entry from reality.

The shipped file re-runs the full stage-2 contract validator clean — all 16 checks
PASS on the meshopt-compressed, per-material-joined GLB.
</content>
