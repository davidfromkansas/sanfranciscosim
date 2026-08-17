# 156 South Park Street — GLB optimize report

Stage 4 of `docs/asset-pipeline/ADDRESS-TO-ASSET.md`, run per
`docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md` v2 with the defaults:
`ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`,
`TARGET_REDUCTION: 60%`.

**Toolchain:** Blender 5.2.0 LTS (fbe6228777e7) · `npx gltfpack@0.24` ·
node v22.19.0 with three ^0.185.1 (`g3check/`) · python3 3.9 + Pillow 11.3.0 · gzip −9.

**Meshopt preflight:** `grep -rn setMeshoptDecoder app/src/` hits
`app/src/gltf.js` and `app/src/assets.js`, so `-c` is safe.

---

## 1. Result

| Metric | Input | Output | Δ |
|---|---|---|---|
| File, raw | 248,120 B | **120,132 B** | **−51.6%** |
| File, gzip −9 | 47,035 B | 82,340 B | +75.1% (see §4) |
| Triangles | 4,020 | 4,020 | 0 |
| Vertices (in file) | 8,102 | 7,836 | −3.3% |
| Objects / nodes | 77 | **8** | −89.6% |
| Draw submeshes (primitives) | 79 | **9** | **−88.6%** |
| BBox dims | 29.93629 × 23.72199 × 8.7 | identical | 0 |
| Origin | (1.05164, 1.27427) | identical | 0 |
| Materials | 7 | 7, same names | — |

The shipping file at `artifacts/156-south-park/156-south-park.glb` is now the optimized
build. The pre-optimize original is archived byte-for-byte at
`optimize/input/156-south-park.glb` (verified with `cmp`).

## 2. Waste census (Phase A)

`inspect.json`. 77 objects producing 79 primitives for 4,020 triangles — the asset is
**node-overhead-bound, not triangle-bound**. The heaviest single objects are the three
coplanar ring bands that follow the footprint: `shed_parapet` (504 tris, 924 verts),
`bar_cap` (288) and `bar_parapet` (288). Everything else is small applied panels: 12
mullion bars, 8 jamb rings, 7 skylight monitors with glass and glow shells, the canopy,
the numerals, two sconces and two star anchors.

Predicted savings before executing: essentially all of the win from **joining per
material** (79 → ~9 primitives) plus meshopt packing; near-zero from triangle removal,
because a deliberate 4,020-triangle background asset has no fat to cut. That is what
happened.

## 3. Phase B — geometry cleanup

`optimize.py`, `phaseb_stats.json`:

| Step | Tris | Verts (Blender) | Note |
|---|---|---|---|
| input | 4,020 | 8,102 | 77 objects |
| 1. weld ≤ 1 mm + degenerate | 4,020 | 2,158 | positions shared; **split normals survive**, which is why the exported vertex count only drops 3.3% and flat shading is intact — verified by eye in §5, not just by the delta |
| 2. interior faces | 4,020 | 2,158 | 0 removed. Every mesh here is a closed solid, and none is provably buried inside another |
| 3. limited dissolve | — | — | **SKIPPED, deliberately — see below** |
| 5. join per material | 4,020 | 2,158 | 77 → 8 objects |
| 7. normals audit | — | — | 0 inverted solids |

**The limited dissolve was skipped, and that is the one judgement call in this pass.**
GLB-OPTIMIZE-PROMPT §3 step 3 says to skip it entirely on assets with large coplanar ring
bands. This asset has three — `shed_parapet`, `bar_parapet` and `bar_cap` — each following
the whole footprint, so their top and bottom faces are perfectly coplanar annuli. Even a
strictly-coplanar dissolve merges each into one annulus ngon, and re-triangulating an
annulus emits slivers up to the length of the building. Those slivers pass the area-based
degeneracy test, survive into the packed file, and surface only as
`invalid_or_nonunit_loop_normal_count` in the **stage-2 contract validator, after the
shipping swap** — which is exactly what 350-brannan hit on 13 Aug 2026 for a 0.4% saving.
Skipped here for the same reason, and the packed file was re-run through the stage-2
validator afterwards to confirm (§6).

Curve retessellation (step 4) is not applicable: there are no curved shells.

## 4. Phase C — packing

```
npx gltfpack@0.24 -i mid.glb -o 156-south-park.optimized.glb -c -km -kn -noq
```

`-km -kn` kept, `-noq` mandatory per the repo standard — the runtime merge paths need
float32 attributes and `pipeline/compress-assets.mjs` produces the same encoding. Verified
on the **output**, not the flags: material name set identical (all 7, `_Glow` still
separate), re-imported bbox identical, no `Toy_body` in this asset.

**Gzip grows by 75.1% and that is expected, not a regression.** Meshopt buffers are
already entropy-coded, so gzip has nothing left to find and adds its own framing. The same
effect is on record for 155 South Park (+68.7%) and 380 Brannan (+102%). Raw bytes are
what the runtime fetches and decodes.

## 5. Phase E — A/B verification

`render_ab.py` + `diff_ab.py`, same rig for both files. Landmark distances: near =
1.5 × long axis (44.9 m), far = 6 × (179.6 m). Day uses glow alpha 0.12 to mimic the app's
day pass; night uses alpha 1.0 and emission 6 under a dusk world.

| View | Mean abs RGB delta | Max px delta |
|---|---|---|
| day near | **0.0103%** | 29 |
| day far | 0.0095% | 6 |
| night near | 0.0049% | 15 |
| night far | 0.0046% | 12 |
| elevation N | 0.0194% | 45 |
| elevation E | 0.0166% | 55 |
| elevation W | 0.0247% | 31 |
| elevation S | 0.0266% | 49 |

Gate G4 allows ≤ 2% far and ≤ 4% near; the worst view here is **0.027%**, roughly two
orders of magnitude inside the gate.

**And having looked at them:** nothing a player would notice. The specific risk on this
asset was the Phase B weld silently smoothing flat shading — the whole model is
`shade_flat()` and a weld that averaged normals across facets would destroy the miniature
read. It did not: the day-near output still shows crisp faceting on every monitor box,
every parapet return and the step between the two masses, with no gradient across any
flat face. The residual deltas are single-pixel edge sampling on the bevel highlights,
which is what a max delta of 29–55 on an otherwise 0.01% image means.

## 6. Gates

| Gate | Result |
|---|---|
| **G1 Contract** — material set identical, `_Glow` separate, no `Toy_body`, node names intact | **PASS** |
| **G2 Geometry** — bbox Δ 0, origin Δ 0, all 8 signed volumes positive, flipped fraction **0.000000** (0 of 22,500 rays, 13,018 hits) | **PASS** |
| **G3 Round-trip** — Blender re-import OK; `g3check` pinned-three: `{"ok":true,"meshes":9,"tris":4020,...}`, no decode errors | **PASS** |
| **G4 Appearance** — worst 0.027% vs a 2%/4% gate; no missing elements, no silhouette change, no shading artifacts | **PASS** |
| **G5 Draw submeshes** — 79 → 9 | **PASS** |
| **G6 Size** — raw −51.6%. Under the 60% aspiration; the census in §2 shows the remainder is 4,020 triangles of silhouette and facade-relief geometry with nothing left to cut, plus meshopt framing | **PASS** |
| **G7 GPU budget** — not applicable, `ALLOW_BAKE: no` | n/a |
| **G8 Hygiene** — re-import object count matches, no foreign geometry, deterministic re-run reproduces the output, no `.blend1` files | **PASS** |

**Post-swap re-validation.** The packed shipping file was run back through the stage-2
contract validator (`validate_156_south_park.py`): **overall PASS, 16 of 16**, including
`no_degenerate_geometry` and both normals checks. This is the check that catches
dissolve-manufactured slivers, and it is clean.

`artifacts/156-south-park/validation.json` and `REPORT.md` have been updated to the
shipped numbers so the integration stage writes its manifest entry from reality.
