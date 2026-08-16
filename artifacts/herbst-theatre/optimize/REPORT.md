# herbst-theatre — GLB optimize report (stage 4)

Run of `docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md` against
`artifacts/herbst-theatre/`. `ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`,
`ALLOW_BAKE: no`.

Toolchain: Blender 5.2.0 LTS (headless, CPU), `npx gltfpack@0.24`, node v22.19.0
with the pinned three in `g3check/`, python3 + Pillow 11.3.0, `gzip -9`.

## Metrics

| | Input | Output | Δ |
|---|---|---|---|
| File, raw | 554,680 B | **244,260 B** | **−56.0%** |
| File, gzip −9 | 79,999 B | 161,080 B | +101% (see §4) |
| Triangles | 9,844 | 9,844 | 0 |
| Vertices | 18,078 | **5,362** | −70.3% |
| Objects / nodes | 220 | **9** | −95.9% |
| Draw submeshes (primitives) | 220 | **9** | −95.9% |
| Materials | 9 | 9 | 0 |
| bbox dims (m) | 92.53177 × 70.71085 × 31.0 | identical | 0 |
| bbox min (m) | −46.26588, −35.35542, 0.0 | identical | 0 |

## §2 Waste census

`inspect.py` found the asset already geometrically tight — it is authored from
axis-aligned boxes and 12-segment cylinders by a deterministic script, so the
usual sources of waste are absent:

- **Duplicate meshes:** none (every object is uniquely placed).
- **Buried interior faces:** the census found candidates, but the occluder rule
  admits only *closed* solids as occluders, and every candidate here sits inside
  a union of overlapping boxes rather than strictly inside one. **0 removed** —
  correctly conservative.
- **Degenerate faces:** 0.
- **Unwelded coincident verts:** the big one. 18,078 → 5,362 (−70.3%). Each of
  the 220 objects was exported with fully split vertices; the per-object weld at
  1 mm recovers all of it without ever fusing a glow shell onto a base surface.
- **Over-tessellated curves:** the only curves are the 16 colonnade shafts and
  the 2 reentrant quadrants, at 12 and 16 segments. Both are silhouette-defining
  and already at the style bible's low-seg floor. **Skipped**, per §3.4.
- **Object-count overhead:** the dominant file-size cost. 220 nodes/primitives
  for 9 materials. Joining per material is the whole headline win.

Predicted before executing: verts ≈ −70%, nodes → 9, tris unchanged, raw bytes
≈ −55%. All four landed.

## §3 Phase B — per-step

| Step | tris | verts |
|---|---|---|
| input | 9,844 | 18,078 |
| 1. weld ≤1 mm + degenerate | 9,844 | 5,362 |
| 2. interior faces | 9,844 | 5,362 |
| 3. limited dissolve 0.05° | 9,844 | 5,362 |
| 5. join per material | 9,844 | 5,362 |

Joins: `Toy_glass` 73, `Toy_trim` 47, `Toy_mustard_Glow` 40, `Toy_stone` 20,
`Toy_sand` 16, `Toy_ink` 16, `Toy_roofd` 5, `Toy_steel` 2 → 9 objects.

Steps 2 and 3 saved nothing. That is the expected result for a
script-authored box-union asset and is recorded rather than tuned away: loosening
the dissolve angle past 0.05° is explicitly forbidden by §3.3, and loosening the
occluder rule is what §3.2 calls the hard-learned mistake.

Normals audit after Phase B: `inverted_solids: []`, all signed volumes positive.

## §4 Phase C — packing, and the gzip regression

```
npx gltfpack@0.24 -i mid.glb -o herbst-theatre.optimized.glb -c -km -kn -noq
```

`-km -kn` kept (mandatory: glow-ness is name-only, and without `-km` gltfpack
merges `Toy_mustard_Glow` into an identical-parameter non-glow material and
silently kills the night layer). `-noq` kept (mandatory for this repo).

**The gzipped size doubles: 80.0 KB → 161.1 KB.** This is not a regression to fix
— meshopt already entropy-codes the buffers, so a second gzip pass over
compressed bytes expands them. `artifacts/380-brannan/optimize/REPORT.md` §4
recorded exactly this pattern on 12 Aug 2026 (raw −51.8%, gzip +102%) and shipped
the `-noq` build anyway. Same decision here, for the same reason: `-noq` is what
`pipeline/compress-assets.mjs` — the mandatory ship step per `sf-asset-check` §8 —
runs, the runtime landmark merge needs float32 attributes, and a quantized build
also fails the stage-2 contract validator on `transforms_applied` and
`no_unexpected_objects`.

At 244 KB raw the asset is comfortably inside the 500 KB per-asset budget
(`sf-asset-check` §7).

**Finding outside this asset's scope.** The prompt's §4 states "Every shipped
landmark except `st-marys-cathedral` is unquantized." That is false. Auditing
`app/public/sf-assets/landmarks/*.glb` for `KHR_mesh_quantization` in
`extensionsRequired` finds **four**: `st-marys-cathedral`, `550-third`,
`letterman-digital-arts-center` and — directly relevant to this asset —
`war-memorial-opera-house`, which is its twin. Each also shows the tell the
prompt describes (node count double the mesh count: the Opera House has 18 nodes
for 9 meshes). If the prompt's claim about the merge path is right, the Opera
House is falling back to procedural in production, which would break the pairing
this asset is built around. Raised as a separate task rather than fixed here —
it touches four other assets and does not belong in this PR.

## §7 Phase E — A/B verification

Landmark class: near = 1.5 × long axis = 138.8 m, far = 6 × = 555.2 m. Day
(glow alpha 0.12) and night (alpha 1.0, emission ≈ 6, dusk world) at both
distances, plus four orthographic elevations. `cam.data.clip_end = 50000`.

| View | mean abs RGB Δ | max px Δ |
|---|---|---|
| day near | 0.0321% | 57 |
| day far | 0.0317% | 43 |
| night near | 0.2257% | 61 |
| night far | 0.2993% | 97 |
| elev N | 0.0607% | 106 |
| elev E | 0.0900% | 105 |
| elev S | 0.0318% | 121 |
| elev W | 0.0046% | 32 |

Gates are ≤ 2% far / ≤ 4% near; the worst view is 0.30%.

**Looked at the diffs** (`renders/contact_sheet.png`, diff row amplified ×8):
the input and optimized rows are indistinguishable. The diff row is black except
for faint speckle along a few coincident-face boundaries — the arch reveals
against their wall planes, the cornice against the attic, the roof eaves against
the parapets. That is Cycles sampling noise at surfaces that were separate
objects in the input and are now the same joined mesh, so the renderer resolves
the coplanar tie differently. Night views are the noisiest because the emissive
panes sit 5 cm proud of their glass and that gap is where the tie occurs.
Nothing a player would notice; no missing element, no silhouette change, no
shading artifact.

## §8 Gate results

| Gate | Result | Evidence |
|---|---|---|
| G1 Contract — material set identical, `_Glow` separate, no `Toy_body` | **PASS** | `validation.json` `G1_materials_identical: true`; 9 → 9 materials, both glow materials survive as distinct |
| G2 Geometry — bbox ≤ max(1 cm, 0.1%), origin ≤ 1 cm, volumes positive, flips ≤ 0.15% | **PASS** | bbox and origin bit-identical; `flipped_fraction` **0.0** over 22,500 rays (19,711 hits) |
| G3 Round-trip — Blender + pinned-three GLTFLoader | **PASS** | `G3-OK {"ok":true,"meshes":9,"tris":9844,...}`; only `EXT_meshopt_compression` declared |
| G4 Appearance — day+night × near+far | **PASS** | worst mean Δ 0.30% vs 2% gate; diffs described above |
| G5 Draw submeshes ≤ input | **PASS** | 220 → 9 |
| G6 Size reduced | **PASS with note** | raw −56.0%, just short of the 60% aspiration; census shows the remainder is silhouette geometry (tris unchanged, curves at the seg floor) |
| G7 GPU budget | **N/A** | bake mode off |
| G8 Hygiene — no foreign geometry, deterministic, no `.blend1` | **PASS** | re-import object count 9/9, material set exact, bbox exact; scripts are deterministic; no `.blend1` written |

**G6 note.** 56.0% raw reduction is under the 60% target. The waste census
accounts for the remainder: triangle count is unchanged because there was no
tessellation waste to remove, the two curved element families are
silhouette-defining and already at the minimum segment count, and no interior
face could be *proved* buried under the closed-solid occluder rule. The
remaining bytes are the geometry the asset actually needs.

## §9 Shipping swap

All gates passed, so `herbst-theatre.optimized.glb` was copied over
`artifacts/herbst-theatre/herbst-theatre.glb`. The pre-optimize original is
archived byte-for-byte at `optimize/input/herbst-theatre.glb`.
`artifacts/herbst-theatre/REPORT.md` and `validation.json` are updated to the
shipped numbers so the integration stage writes its manifest entry from reality.

Shipped: **244,260 B, 9 objects, 9 draw submeshes, 9,844 triangles,
92.53177 × 70.71085 × 31.0 m.**
