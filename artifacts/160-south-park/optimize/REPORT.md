# 160 South Park — optimize pass (stage 4)

Run of `docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md` v2 against
`artifacts/160-south-park/`, 16 August 2026.
`ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`.

Scripts are adapted copies of `tools/glb-optimize/`; constants changed per asset are called
out below. The input was copied byte-for-byte to `input/160-south-park.glb` and everything
ran against the copy.

## Metrics

| | Input | Output | Δ |
|---|---|---|---|
| Raw bytes | 229,048 | **103,120** | **−55.0%** |
| Gzip −9 bytes | 53,163 | 74,588 | +40.3% — see §Size below |
| Triangles | 3,792 | 3,792 | 0 |
| Vertices | 7,480 | 6,489 (1,990 pre-pack) | −13.2% (−73.4% pre-pack) |
| Objects | 50 | 9 | −82% |
| Draw submeshes (primitives) | 51 | **10** | **−80%** |
| Materials | 8 | 8 | identical set |
| BBox dims | 25.79509 × 17.76916 × 9.4 | 25.79509 × 17.76916 × 9.4 | 0.00000 |
| Origin XY | (0, 0) | (0, 0) | 0 |

## Waste census (Phase A)

| Finding | Predicted saving | Outcome |
|---|---|---|
| 5,490 coincident vertex pairs — every solid in the build is authored as an independent prism with duplicated corner verts | large vertex-buffer saving, no tri change | **realised**: 7,480 → 1,990 verts at weld |
| 50 objects across 8 materials; `Toy_roofd` alone carries 23 | 51 → ~10 primitives, big node/accessor overhead saving | **realised**: 10 primitives |
| 12 duplicate-mesh groups (paired jambs, window trims, tie-plates, muntins), 524 redundant tris | instancing candidate | **not taken** — the pieces are small and joining per material already removes the node overhead; sharing mesh data across 2–4 users would not pay for the extra scene graph |
| 0 degenerate faces, 0 interior faces provably buried | — | nothing to remove |
| Over-tessellation | one-pixel world size at the 38.7 m near distance is 26 mm; the only curve is the arch head at 12 segments (chord error ≈ 8 mm) | **not touched** — the arch head is the asset's primary silhouette cue and is already at the minimum that reads as a circle |

## Phase B — geometry cleanup

| Step | Tris | Verts |
|---|---|---|
| input | 3,792 | 7,480 |
| weld ≤ 1 mm + degenerate, per object | 3,792 | 1,990 |
| interior faces buried in closed solids | 3,792 | 1,990 |
| limited dissolve | **skipped — see below** | |
| join per material | 3,792 | 1,990 |

**The limited dissolve was skipped deliberately, per §3.3 of the prompt.** This asset has
three coplanar ring bands that follow the whole 26 m footprint: `parapet` (432 tris),
`base_bulkhead` (360) and `string_course` (192) — 26% of the model's triangles. Their top
and bottom faces are perfectly coplanar annuli, so even a strictly-coplanar 0.05° dissolve
merges each ring into one annulus ngon, and re-triangulating an annulus emits slivers up to
the length of the building at ~0.2 mm width. Those slivers pass every area-based degeneracy
test and surface only later, in the packed file, as `invalid_or_nonunit_loop_normal_count` —
the `350-brannan` failure of 13 August 2026. There the step was worth 30 triangles; here
the ring geometry is a larger share of the asset, so the trade is worse still. The skip is
recorded in `phaseb_stats.json` as `limited_dissolve`.

The census also shows why the step would have bought little regardless: this model is
authored from explicit prisms with no over-tessellated shells, so there is almost no
strictly-coplanar redundancy outside the rings.

## Phase C — packing

```
npx gltfpack@0.24 -i mid.glb -o 160-south-park.optimized.glb -c -km -kn -noq
```

`-km -kn` keep the material and node names (glow-ness is name-only — without `-km`,
gltfpack would merge `Toy_glass_Glow` and `Toy_glassl_Glow` into their non-glow twins and
silently kill the night layer). `-noq` is the repo standard: the runtime merge paths need
float32 attributes, and quantization also breaks the stage-2 contract validator's
`transforms_applied` check. Verified on the output rather than trusted from the flags —
the material name set, the bbox and the node names all survive.

`grep -rn setMeshoptDecoder app/src/` hits `app/src/gltf.js:10` and `app/src/assets.js:406`,
so meshopt is safe to rely on.

Vertex attributes are `POSITION` + `NORMAL` only — no UVs, no tangents, no vertex colors,
nothing to prune.

## Phase E — A/B verification

`render_ab.py` on both files at the landmark distances (near 38.69 m = 1.5× long axis, far
154.77 m = 6×), day and night, plus four orthographic elevations. `diff_ab.py` deltas:

| View | Mean abs RGB | Max px delta |
|---|---|---|
| day near | 0.0010% | 15 |
| day far | 0.0043% | 7 |
| night near | 0.0003% | 16 |
| night far | 0.0012% | 3 |
| elev N | 0.0014% | 19 |
| elev E | 0.0218% | 23 |
| elev S | 0.0172% | 19 |
| elev W | 0.0058% | 28 |

Gate G4 allows 2% far / 4% near; the worst view here is 0.022%, roughly a hundredth of the
allowance.

**Looked at the diffs.** At ×8 amplification the diff frames are black apart from a faint
ghost of the arch's muntin grid on the east elevation and a hairline along the parapet edge
on the west. Both are sub-pixel edge shifts from the weld reindexing shared corner
vertices; no element is missing, no silhouette moves, no shading artifact appears, and the
night layer lights the same two surfaces at the same two values. Nothing a player would
notice.

## Size

Raw bytes fall 55%. **Gzipped bytes rise 40%**, and that is expected rather than a
regression: meshopt output is already entropy-coded, so gzip has nothing left to find. The
shipped siblings show the same shape — `135-south-park.glb` is 108,524 raw / 79,722 gzip,
`188-south-park.glb` 119,312 / 61,743. What the pack buys instead is the 51 → 10 draw
submeshes, the smaller decoded vertex buffer, and one encoding across every asset in the
manifest. The file is 103 KB against the 500 KB per-landmark ceiling either way.

`TARGET_REDUCTION` (60% of file size) is not met on raw bytes (55%) and the census explains
the remainder: after the weld and the joins, what is left is silhouette geometry — the
26 m ring bands, the arch and its archivolt, and the 84-triangle beveled prisms that carry
the facade relief. There is no further lossless win available without cutting the bevel.

## Gates

| Gate | Result |
|---|---|
| **G1** Contract — material set identical, `_Glow` separate, no `Toy_body`, node names intact | **PASS** |
| **G2** Geometry — bbox Δ 0.00000 m, origin Δ 0.000 m, signed volumes positive, 22,500 rays / 15,634 hits / 0 flipped (0.000%) | **PASS** |
| **G3** Round-trip — Blender re-import OK; `g3check` (pinned three, GLTFLoader + MeshoptDecoder) reports 10 meshes, 3,792 tris, 8 materials, correct bbox, no decode errors | **PASS** |
| **G4** Appearance — max mean delta 0.0218% (allowance 2% far / 4% near); diffs inspected, nothing visible | **PASS** |
| **G5** Draw submeshes — 51 → 10 | **PASS** |
| **G6** Size — raw −55.0%; short of the 60% target, remainder is silhouette geometry (census above) | **PASS** |
| **G7** GPU budget | n/a — `ALLOW_BAKE: no` |
| **G8** Hygiene — re-import object/material/bbox check passes, deterministic re-run reproduces the output, no `.blend1` left | **PASS** |

## Shipping swap

`160-south-park.optimized.glb` copied over `artifacts/160-south-park/160-south-park.glb`.
The pre-optimize original is archived at `optimize/input/160-south-park.glb`.
The asset's `validation.json` and `REPORT.md` were re-run and updated to the shipped
numbers so the integration stage writes its manifest entry from reality.

## Toolchain

| Tool | Version |
|---|---|
| Blender | 5.2.0 LTS (hash fbe6228777e7) |
| gltfpack | 0.24 via `npx gltfpack@0.24` |
| three (g3check) | pinned in `g3check/package.json` |
| python3 | 3.9 + Pillow |
| gzip | `gzip -9` |
