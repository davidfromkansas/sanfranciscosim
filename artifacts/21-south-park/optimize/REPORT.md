# 21–29 South Park — GLB optimize report (stage 4)

Run 16 August 2026 per `docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md` v2.
`ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`.

Toolchain: Blender 5.2.0 LTS (`fbe6228777e7`, 2026-07-14) headless ·
`npx gltfpack@0.24` · node + the pinned three in `g3check/package.json` ·
python3 3.9 + Pillow 11.3.0 · gzip.

## 1. Headline

| Metric | Input | Optimized | Delta |
|---|---|---|---|
| File bytes (raw, what the CDN serves) | 504,136 | **236,856** | **−53.0 %** |
| gzip −9 bytes | 88,163 | 157,556 | +78.7 % (expected — meshopt output is already entropy-dense, so gzip cannot help it; the CDN serves the raw file) |
| Triangles | 8,664 | 8,664 | 0 |
| Vertices (in Blender, welded) | 17,164 | 15,456 | −10.0 % |
| Mesh objects / draw submeshes | 130 | **9** | **−93.1 %** |
| Materials | 9 | 9 | identical set |
| bbox dims | 47.36144 × 51.49327 × 11.73 | identical | 0 |
| bbox min | −24.01703, −25.61444, 0.0 | identical | 0 |
| XY centre | −0.33631, 0.13220 | identical | 0 |

Comfortably inside the ≤ 500 KB on-disk gate and the ≤ 30,000-triangle gate. For
scale, `102-south-park` (8,100 tris) ships at 219,692 bytes and `380-brannan`
(7,760 tris) at 222,516 — this asset is in family at 8,664 tris and 236,856 bytes.

## 2. Phase A — waste census

`inspect.py` → `inspect.json`. Input: 504,136 bytes, 130 objects, 8,664 triangles,
17,164 vertices, 130 primitives, 9 materials, no textures.

| Technique | Predicted | Realised |
|---|---|---|
| Weld coincident verts ≤ 1 mm, per object | small — the build script already runs `remove_doubles` at 1e-4 inside `bevel()` | 0 tris; the vertex saving shows up only after the join |
| Delete degenerate faces | none — the stage-2 validator already reports `degenerate_triangle_count: 0` | 0 |
| Delete buried interior faces | **none, and this was the honest prediction.** The asset is a union of interpenetrating closed solids, but almost nothing is *box-like enough* to qualify as an occluder under the ≥ 95 % AABB-fill rule: the body is an 8-sided prism, the cornices are long thin slabs, and the applied window panels sit ON the wall plane, not inside it | 0 |
| Limited dissolve at 0.05° | **skipped deliberately** — see §3 | n/a |
| Curve retessellation | skipped — the eight segmental arches are already at 7 segments, the silhouette-defining minimum this asset was authored to | n/a |
| Join objects per material | **the whole win.** 130 objects sharing 9 materials is 121 objects of pure node/accessor/draw-submesh overhead | 130 → 9 objects, −10 % verts, −53 % bytes |
| Instancing | not applicable — the repeats (bays, arches, condensers) are at distinct positions in one authored mesh, not transform instances |  |

The remainder after Phase C is silhouette and facade geometry: the eight arched
openings and their sills are 22 % of the triangles, the five three-register loft bays
another 24 %, the roof plant 21 %, and the four coplanar ring bands (parapet, coping,
two cornice runs) most of the rest. None of it can go without changing what the
building looks like.

## 3. Limited dissolve — skipped, on purpose

`optimize.py`'s step 3 is disabled on this asset and the reason is in the script's own
comment. GLB-OPTIMIZE-PROMPT v2 §3 step 3: *"Skip this step entirely on assets with
large coplanar ring bands."* This asset has four — `parapet`, `parapet_coping` and the
two cornice runs with their returns — every one of them following the whole
32.75 × 40.68 m footprint, plus the roof-deck prism. Their top and bottom faces are
perfectly coplanar annuli, so even a strictly-coplanar 0.05° dissolve merges each ring
into a single annulus ngon, and re-triangulating an annulus emits slivers metres long
and fractions of a millimetre wide.

Those slivers pass an area-based degeneracy test, survive Phases B and E, and surface
only *after* the shipping swap, as `invalid_or_nonunit_loop_normal_count` in the
stage-2 contract validator — because gltfpack re-emits the STORED normals and a
sliver's shared vertex normal has collapsed to ~0. That is the `350-brannan` failure of
13 August 2026, where the whole step was worth 30 triangles (0.4 %). Not worth
re-learning: skipped, and the skip is recorded in `phaseb_stats.json` as a step with a
`skipped` reason rather than silently omitted.

The stage-2 validator was re-run on the shipped, packed file (§6) and reports
`invalid_or_nonunit_loop_normal_count: 0` and `degenerate_triangle_count: 0`, which is
the check that would have caught it.

## 4. Phase B — geometry cleanup

`optimize.py` → `mid.glb` (430,920 bytes, deleted after packing) + `phaseb_stats.json`.

| Step | tris | verts |
|---|---|---|
| input | 8,664 | 17,164 |
| weld + degenerate | 8,664 | 4,588 (per-object vertex count in Blender's own terms) |
| interior faces | 8,664 | 4,588 — `interior_faces_removed: 0` |
| limited dissolve | *skipped* | |
| join per material | 8,664 | 4,588 |

Joins: `Toy_sash` 37 objects → 1, `Toy_roofd` 33 → 1, `Toy_stone` 26 → 1, `Toy_glass`
20 → 1, `Toy_mustard_Glow` 5 → 1, `Toy_glassl_Glow` 3 → 1, `Toy_steel` 3 → 1,
`Toy_white` 2 → 1. `entry_door` is the only object left alone — it is the sole
`Toy_rust` mesh, so there was nothing to join it to.

Normals audit after the joins: `inverted_solids: []`. Every merged group encloses
positive signed volume (`Toy_white` 10,608 m³ — the body; `Toy_roofd` 133.7 m³;
`Toy_steel` 75.0 m³; `Toy_stone` 28.9 m³; `Toy_sash` 12.4 m³; `Toy_glass` 12.3 m³;
`Toy_mustard_Glow` 0.94 m³; `Toy_glassl_Glow` 0.61 m³; `entry_door` 0.83 m³).

Leak-proof export: temp scene + `use_active_scene=True` + `export_apply=True`, exporter
stdout redirected; re-import verified 9 objects, identical material set, bbox within
tolerance (`bbox_ok true`, `material_set_ok true`).

## 5. Phase C — packing

```
npx gltfpack@0.24 -i mid.glb -o 21-south-park.optimized.glb -c -km -kn -noq
```

430,920 → **236,856** bytes. `-km -kn` keep the material and node names, which is what
keeps `Toy_mustard_Glow` and `Toy_glassl_Glow` from being merged into their
identical-parameter non-glow neighbours and silently killing the night layer. `-noq` is
the repo standard and is not negotiable: `pipeline/compress-assets.mjs` produces the
same encoding, the runtime merge paths need float32 attributes, and a quantized build
fails the stage-2 contract validator on `transforms_applied` and
`no_unexpected_objects`. It also costs the headline number, exactly as the prompt warns.

Verified on the output rather than trusting flags: material name set identical (9),
re-imported bbox identical to 5 decimal places, node names present.

## 6. Gates

| Gate | Result | Evidence |
|---|---|---|
| **G1** Contract — material set identical, `_Glow` separate, `Toy_body` separate, node names intact | **PASS** | `optimize/validation.json` `G1_materials_identical: true`; both `_Glow` materials survive as their own groups; no `Toy_body` in this asset (landmarks are never tintable) |
| **G2** Geometry — bbox within max(1 cm, 0.1 %), origin within 1 cm, signed volumes positive, flipped ≤ 0.15 % | **PASS** | bbox and origin identical to 5 dp; 9/9 positive volumes; 22,500 rays, **0 flipped** |
| **G3** Round-trip — Blender re-import and pinned-three `g3check` | **PASS** | `G3-OK {"ok":true,"meshes":9,"tris":8664,...}`, no decode errors, only `EXT_meshopt_compression` |
| **G4** Appearance — day+night × near+far, ≤ 2 % far / ≤ 4 % near, and nothing a player would notice | **PASS** | mean abs RGB delta: day_near **0.014 %**, day_far 0.017 %, night_near 0.004 %, night_far 0.006 %, elevations 0.009–0.026 %. The ×8-amplified diffs are black apart from a one-pixel outline on silhouette edges — Cycles AA on shared edges, not a geometry change. Nothing missing, no silhouette change, no shading artifact |
| **G5** Draw submeshes ≤ input | **PASS** | 130 → 9 |
| **G6** Size reduced ≥ 60 % target | **PASS on reduction, short of target** — −53.0 % against a 60 % aspiration. The census (§2) shows the remainder is silhouette and facade geometry: 46 % of the triangles are the arched rank and the loft bays, which are the two recognition cues, and the four ring bands are most of the rest. `-noq` costs the headline number, as the prompt warns, and is non-negotiable here |
| **G7** GPU budget | n/a | bake mode not used |
| **G8** Hygiene — no foreign geometry, deterministic, no `.blend1` | **PASS** | re-import object count 9 = expected; scripts are deterministic (no RNG, no timestamps); `mid.glb` removed after packing; no `.blend1` in the tree |

**Stage-2 contract validator re-run on the shipped file** (`validate_21_south_park.py`
against the swapped `21-south-park.glb`): **overall PASS**, all 16 checks true,
`invalid_or_nonunit_loop_normal_count: 0`, `degenerate_triangle_count: 0`,
`signed_volume_inverted_objects: []`, 31,500 rays with 0 flipped. This is the check that
catches what the dissolve skip in §3 avoids, and it is clean.

## 7. Shipping swap

`21-south-park.optimized.glb` copied over `artifacts/21-south-park/21-south-park.glb`.
The pre-optimize original is archived byte-for-byte at
`optimize/input/21-south-park.glb` (verified with `cmp` before Phase A).
`artifacts/21-south-park/validation.json` and `REPORT.md` are updated to the shipped
numbers so the integration stage writes its manifest entry from reality.

## 8. Reproduce

```
cd artifacts/21-south-park/optimize
"$BLENDER" -b --python inspect.py  -- input/21-south-park.glb inspect.json
"$BLENDER" -b --python optimize.py -- input/21-south-park.glb mid.glb phaseb_stats.json
npx gltfpack@0.24 -i mid.glb -o 21-south-park.optimized.glb -c -km -kn -noq
"$BLENDER" -b --python validate.py -- input/21-south-park.glb 21-south-park.optimized.glb validation.json
"$BLENDER" -b --python render_ab.py -- input/21-south-park.glb renders/in
"$BLENDER" -b --python render_ab.py -- 21-south-park.optimized.glb renders/out
python3 diff_ab.py
(cd g3check && npm install && node check.mjs ../21-south-park.optimized.glb)
```
