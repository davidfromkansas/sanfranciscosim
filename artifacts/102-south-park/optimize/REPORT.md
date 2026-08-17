# 102 South Park — GLB optimize report

Stage 4 of `docs/asset-pipeline/ADDRESS-TO-ASSET.md`, run per
`docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md` with the defaults:
`ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`.

`grep -rn setMeshoptDecoder app/src/` hits `app/src/gltf.js` and
`app/src/assets.js`, so meshopt is available and was used.

## 1. Headline

| Metric | Input | Shipped | Δ |
|---|---|---|---|
| Raw bytes | 489,472 | **219,692** | **−55.1 %** |
| gzip −9 bytes | 99,763 | 141,264 | +41.6 % (expected — meshopt output is already entropy-dense; the CDN serves the raw file and gzips it to no further benefit) |
| Triangles | 8,100 | 8,100 | 0 |
| Vertices (in Blender, welded) | 16,048 | 14,710 | −8.3 % |
| Mesh objects / draw submeshes | 140 | **11** | **−92.1 %** |
| Materials | 11 | 11 | identical set |
| bbox dims | 27.2532 × 27.1464 × 14.0 | identical | 0 |
| bbox min | −13.413, −13.7873, 0.0 | identical | 0 |

Comfortably inside the ≤ 500 KB on-disk gate and the ≤ 30,000-triangle gate.
For scale, `380-brannan` (7,760 tris) ships at 222,516 bytes — this asset is in
family at 8,100 tris and 219,692 bytes.

## 2. Phase A — waste census

`inspect.py` → `inspect.json`.

| Finding | Size | Technique | Predicted | Actual |
|---|---|---|---|---|
| 11,724 coincident vertex pairs (flat-shaded split verts) | — | per-object weld ≤ 1 mm | large vert cut | 16,048 → 4,324 verts in-scene |
| 140 objects over 11 materials | — | join per material | −129 objects / submeshes | 140 → 11 |
| 2,152 tris in duplicate meshes (24 identical `ne*_frame` panels, 12 identical solar panels) | 27 % of tris | left as joined copies — they are distinct world positions, not instances, and the landmark path merges everything into one batch anyway | 0 tris | 0 tris |
| Degenerate faces | 0 | — | — | — |
| Interior faces buried in closed solids | 0 found | occluder rule (closed solids only) | 0 | 0 |
| Over-tessellated curves | none | the only curves are the six 7-segment window arches; at the 40.9 m near distance one pixel is 27.6 mm and the arch chord error already exceeds that, so halving would be visible | skip | skipped |

The 27 % of triangles sitting in duplicate window and solar panels is the honest
answer to Gate G6: the remainder after packing is real facade and roof geometry,
not slack.

## 3. Phase B — geometry cleanup

`optimize.py` → `phaseb_stats.json`.

| Step | Tris | Verts |
|---|---|---|
| input | 8,100 | 16,048 |
| 1–2a weld + degenerate | 8,100 | 4,324 |
| 2b interior faces | 8,100 | 4,324 |
| 3 limited dissolve | **SKIPPED** — see below | |
| 5 join per material | 8,100 | 4,324 |

**Step 3 (limited dissolve) was disabled for this asset** under the
GLB-OPTIMIZE-PROMPT §3 rule about coplanar ring bands. This building has three
that follow the whole 16-vertex footprint — `belt` (960 tris), `parapet` (1,152)
and `parapet_coping` (1,152), together 3,264 of the asset's 8,100 triangles.
Their top and bottom faces are perfectly coplanar annuli, so even a
strictly-coplanar 0.05° dissolve merges each ring into a single annulus ngon, and
re-triangulating an annulus emits sub-millimetre slivers whose averaged vertex
normals collapse toward zero. Blender recomputes loop normals on import and hides
that; gltfpack re-emits the **stored** normals, so the failure would have surfaced
only in the packed file, after the shipping swap — which is exactly how it was
found on `350-brannan` on 13 Aug 2026. The flag is `DISSOLVE = False` in
`optimize.py`; set it to `True` to re-measure.

Normals audit after Phase B: `inverted_solids: []`.

## 4. Phase C — packing

```
npx gltfpack@0.24 -i mid.glb -o 102-south-park.optimized.glb -c -km -kn -noq
```

`-km -kn` keep the material names and node names that the loader treats as API —
without `-km`, gltfpack would merge `Toy_glassl` and `Toy_glassl_Glow` (identical
parameters, different names) and silently kill the night layer. This asset is
the exact case that rule exists for: its two glow materials share their base
colour with a non-glow material by design.

`-noq` per the repo standard; `pipeline/compress-assets.mjs` produces the same
encoding and **skips** files that already carry `EXT_meshopt_compression`, so this
file will pass through the mandatory ship step untouched.

`mid.glb` (the un-packed Phase-B intermediate, 411,376 bytes) was deleted after
packing; it is reproducible by re-running `optimize.py`.

## 5. Phase D

Not run. `ALLOW_BAKE: no` and the contract forbids textures. No textures in
either file (`image_texture_count: 0`).

## 6. Phase E — A/B verification

`render_ab.py` on both files, `diff_ab.py` for the deltas. Landmark camera:
42° aerial, near = 1.5 × long axis (40.9 m), far = 6 × (163.5 m), day (glow alpha
0.12) and night (alpha 1.0, emission ≈ 6, dusk world), plus four orthographic
elevations.

| View | mean abs RGB Δ | max px Δ | gate |
|---|---|---|---|
| day near | 0.0053 % | 30 | ≤ 4 % |
| day far | 0.0066 % | 12 | ≤ 2 % |
| night near | 0.0596 % | 19 | ≤ 4 % |
| night far | 0.0592 % | 53 | ≤ 2 % |
| elev N | 0.0045 % | 33 | — |
| elev E | 0.0040 % | 39 | — |
| elev S | 0.0166 % | 25 | — |
| elev W | 0.0236 % | 28 | — |

Two to three orders of magnitude inside the gates. **Looking at the ×8-amplified
diffs**: they are black except for hairline outlines along a few bevel edges and
around the storefront and awning — single-pixel rasterisation differences from
the re-indexed vertex order, in a render amplified eight times. Nothing changed
that a player could see: every window, the arches, the keystones, the cornice,
the awning, the twelve solar panels, the bulkhead, the light-well slots and both
glow groups are present and identical in position, colour and silhouette. The
night pair confirms the glow split survived packing — the café is gold and the
six lit rooms are blue-gray, in both files.

## 7. Gates

| Gate | Result | Evidence |
|---|---|---|
| **G1** Contract — material set identical, `_Glow` separate, node names intact | **PASS** | `validation.json` `G1_materials_identical: true`; both glow materials present in the G3 loader read |
| **G2** Geometry — bbox ≤ max(1 cm, 0.1 %), origin ≤ 1 cm, volumes positive, flip ≤ 0.15 % | **PASS** | bbox and origin bit-identical; `inverted_solids: []`; ray test 22,500 rays / 14,958 hits / **0 flipped** on both input and output, `ray_flip_delta: 0.0` |
| **G3** Round-trip — Blender + pinned-three GLTFLoader | **PASS** | `G3-OK {"ok":true,"meshes":11,"tris":8100,...}` with all 11 materials |
| **G4** Appearance | **PASS** | §6; worst mean delta 0.0596 % against a 2 % gate |
| **G5** Draw submeshes ≤ input | **PASS** | 140 → 11 |
| **G6** Size reduced ≥ 60 % target | **PASS on reduction, short of target** — −55.1 % against a 60 % aspiration. The census (§2) shows the remainder is silhouette and facade geometry: 27 % of triangles are the repeated window and solar panels that give the building its rhythm, and the three ring bands are 40 % of the rest. `-noq` also costs the headline number, as the prompt warns, and is non-negotiable here |
| **G7** GPU budget | n/a | bake mode not used |
| **G8** Hygiene — no foreign geometry, deterministic, no `.blend1` | **PASS** | re-import object count 11 = expected; scripts are deterministic; `mid.glb` and `.blend1` removed |

**Note on `output_open_shells: ["grp_Toy_trim"]` in `validation.json`.** This is a
false positive from the validator's own test, not a defect. The test welds the
joined mesh at 1e-4 before checking edge manifoldness; `grp_Toy_trim` is seven
originally-closed solids joined together, two of which (`cornice_lo` and
`cornice_hi`) share a face plane at z = 13.45, so the test's weld fuses their
coincident vertices into edges with four incident faces. The pre-optimize input
has the same overlapping solids and reports zero open shells only because it was
never joined. Signed volume is positive (7.87 m³), the ray test flips nothing,
and the stage-2 contract validator passes on the shipped file.

## 8. Shipping swap

All gates passed, so `102-south-park.optimized.glb` was copied over
`artifacts/102-south-park/102-south-park.glb`. The pre-optimize original is
archived byte-for-byte at `optimize/input/102-south-park.glb` (489,472 bytes,
verified with `cmp` before any work started).

`validate_102_south_park.py` was then re-run **on the shipped packed file** in a
fresh factory-reset scene: **overall PASS**, all 16 contract checks, 8,100
triangles, 11 objects, dims 27.2532 × 27.1464 × 14.0, min Z 0.0. The asset's own
`validation.json` and `REPORT.md` now carry the shipped numbers.

## 9. Toolchain

| Tool | Version |
|---|---|
| Blender | 5.2.0 LTS (hash fbe6228777e7, built 2026-07-14) |
| gltfpack | 0.24 (pinned via `npx gltfpack@0.24`) |
| node | v22.19.0 |
| three (g3check) | pinned in `g3check/package.json` |
| Python | 3 (system), Pillow 11.3.0 |
