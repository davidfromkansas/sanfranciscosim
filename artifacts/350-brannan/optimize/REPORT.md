# 350 Brannan Street — optimize pass (stage 4)

Run of `docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md` against `artifacts/350-brannan/`.
`ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`.

Toolchain: Blender 5.2.0 LTS, `npx gltfpack@0.24`, node v22.19.0 + the pinned three in
`g3check/`, python3 + Pillow 11.3.0, gzip −9.

## 1. Metrics

| | Input | Optimized | Δ |
|---|---|---|---|
| File, raw | 421,652 B | **195,500 B** | **−53.6%** |
| File, gzip −9 | 73,003 B | 122,691 B | +68% (see §4) |
| Triangles | 6,770 | 6,770 | unchanged |
| Vertices | 13,770 | 12,683 | −7.9% |
| Objects | 133 | 11 | −91.7% |
| Draw submeshes (primitives) | 134 | **12** | **−91.0%** |
| Materials | 10 | 10 | unchanged |
| BBox | 33.27376 × 33.29583 × 13.85 | identical | 0 |
| Origin XY | (0.036, −0.31038) | identical | 0 |

## 2. Phase A — waste census

| Technique | Finding | Predicted | Actual |
|---|---|---|---|
| Object-count overhead | 133 objects across 10 materials | join to ~11 | 133 → 11 |
| Unwelded coincident verts | 10,122 pairs | large vert drop | 13,770 → 12,683 verts |
| Duplicate meshes | 3,260 tris across skylights, kerbs, vents | join (small counts) | joined, not instanced |
| Degenerate faces | 4 | remove | removed |
| Buried interior faces | 0 closed-solid occluders qualified | 0 | 0 |
| Over-tessellated curves | near-distance 1 px = 33.7 mm | none — arch heads are 6-segment and silhouette-defining | skipped, recorded |

Vertex attributes are `POSITION` + `NORMAL` only; no UVs, no textures, nothing to prune.

## 3. Phase B — geometry cleanup

| Step | Tris | Verts |
|---|---|---|
| input | 6,770 | 13,770 |
| 1. weld ≤ 1 mm + degenerate faces | 6,770 | 3,647 (in-Blender, pre-export split) |
| 2. interior faces | 6,770 | 3,647 |
| 3. limited dissolve | **skipped — see below** | |
| 5. join per material | 6,770 | 3,647 |

Joins: `Toy_ink` 52 → 1, `Toy_glass` 30 → 1, `Toy_glassl` 17 → 1, `Toy_trim` 8 → 1,
`Toy_cream` 7 → 1, `Toy_glass_Glow` 6 → 1, `Toy_steel` 5 → 1, `Toy_roofd` 3 → 1,
`Toy_stone` 2 → 1, `Toy_trim_Glow` 2 → 1. `body` carries two materials and keeps its own
mesh. Signed volumes positive on all 11; `inverted_solids: []`.

### The limited dissolve was reverted — and it exposed a real defect

This is the one judgement call in the pass, and it is worth reading before the next
asset with a parapet.

The generic `optimize.py` runs a 0.05° strictly-coplanar limited dissolve. On this asset
the parapet and its coping are `ring_band` solids whose top and bottom faces are
**perfectly coplanar annuli following the footprint**. A strictly-coplanar dissolve is
therefore free to merge each ring into a single annulus ngon — and re-triangulating an
annulus emits slivers. Measured: **7 triangles up to 24.35 m long**, areas 0.003–0.016 m²,
i.e. about **0.24 mm wide**.

They are invisible, and they pass an area-based degeneracy test, so nothing in Phase B or
Phase E flagged them. What failed was the **stage-2 contract validator**, two steps later
and after the shipping swap: a sliver's shared vertex lies between faces with opposing
normals, so its averaged vertex normal collapses to ~0 (measured length **4.8e-05**).
Blender recomputes loop normals on import and hides this, so `mid.glb` looked clean; only
after gltfpack re-emits the **stored** normals does it surface, as
`invalid_or_nonunit_loop_normal_count = 2` → `normals_outward_ray_residual_within_tolerance:
false`.

Two dead ends worth not repeating: it is not a gltfpack encoding-precision problem
(`-vn 10/12/16` produced byte-identical output — `-vn` is ignored under `-noq`), and it is
not the 0.5°-transitive-chain hazard the prompt already documents. It is specific to large
coplanar ring bands.

The dissolve was worth **30 triangles** (6,770 → 6,740, 0.4%). Under
`GLB-OPTIMIZE-PROMPT` §11 ("phases are independent; revert any phase that regresses") it
was reverted rather than worked around. `optimize.py` in this directory has the step
disabled with the full reasoning inline, and §3.3 of the prompt has been updated so the
next asset with a parapet skips it by default.

A second, smaller fix went in upstream of the pass, in `build_350_brannan.py`: `bevel()`
now welds at 1 mm instead of 0.1 mm. That is the same tolerance Phase B uses and three
orders of magnitude below any authored feature here. It cost 6 triangles (6,776 → 6,770).

## 4. Phase C — packing

```
npx gltfpack@0.24 -i mid.glb -o 350-brannan.optimized.glb -c -km -kn -noq
```

`-km` and `-kn` keep the material names and node names that the loader treats as API;
`-noq` keeps float32 attributes, matching `pipeline/compress-assets.mjs`. Verified on the
output rather than trusted from the flags: material name set identical (both `_Glow`
materials survive as separate materials), `EXT_meshopt_compression` present and it is the
only extension used, bbox and origin unchanged to 1e-5.

**The gzip number goes the wrong way, and that is expected here.** Meshopt-encoded buffers
are already entropy-coded, so they do not recompress: raw drops 53.6% but gzip −9 rises
68% (73.0 KB → 122.7 KB). The shipped sibling `380-brannan` shows the same shape (raw
−51.8%, gzip +102%), so this is the repo's standing trade, not a regression in this asset.
It is also not optional — `AGENTS.md`'s ship step mandates `pipeline/compress-assets.mjs`,
which is this exact gltfpack invocation, because the loaders register `MeshoptDecoder` and
the runtime merge path wants float32.

Worth flagging as a repo-wide question rather than an asset one: across the landmark set,
meshopt is currently costing **transfer** bytes relative to plain gzip, while buying decode
speed, GPU-side vertex memory and a 91% cut in draw submeshes. Nothing to change on this
branch; recorded so someone can measure it deliberately.

## 5. Phase D — bake

Not run (`ALLOW_BAKE: no`). No textures added; the asset remains flat-colour only.

## 6. Phase E — A/B verification

Landmark rig: near = 1.5 × long axis (49.9 m), far = 6 × (199.8 m), 42° aerial,
`clip_end = 50000`. Day pass renders `_Glow` at alpha 0.12 (the app's day state); night
pass at alpha 1.0 with emission.

| View | Mean abs RGB Δ | Max px Δ | Gate |
|---|---|---|---|
| day_near | 0.0378% | 32 | ≤ 4% |
| day_far | 0.0465% | 17 | ≤ 2% |
| night_near | 0.0637% | 35 | ≤ 4% |
| night_far | 0.0762% | 105 | ≤ 2% |
| elev_n | 0.0527% | 21 | — |
| elev_e | 0.0533% | 19 | — |
| elev_s | 0.0233% | 43 | — |
| elev_w | 0.0165% | 189 | — |

**What the diffs actually show, having looked at them.** The ×8-amplified diff row of
`renders/contact_sheet.png` is black except for hairline outlines along material
boundaries and the parapet silhouette. Nothing is missing, no element moved, no silhouette
changed, no shading artifact appeared. The isolated large max-pixel values are
single-pixel anti-aliasing decisions on high-contrast silhouette edges: counting pixels
over threshold, out of 691,200 per view at most **857 differ by more than 8/255** and at
most **6 by more than 32/255** — the elev_w max of 189 is literally 2 pixels. There is
nothing here a player could notice.

## 7. Gate results

| Gate | Result | Evidence |
|---|---|---|
| G1 Contract — material set, `_Glow` separate, node names | **PASS** | `G1_materials_identical: true`; 10 materials in, 10 out, both `_Glow` preserved through `-km` |
| G2 Geometry — bbox, origin, volumes, flips | **PASS** | bbox and origin identical to 1e-5; 11/11 signed volumes positive; 22,500 rays, 17,046 hits, **0 flipped** |
| G3 Round-trip — Blender + pinned three | **PASS** | `G3-OK` — 12 meshes, 6,770 tris, 10 materials, only `EXT_meshopt_compression` |
| G4 Appearance — day/night × near/far | **PASS** | max mean Δ 0.0762% against a 2% far / 4% near gate; diffs inspected, §6 |
| G5 Draw submeshes ≤ input | **PASS** | 134 → 12 |
| G6 Size reduced | **PASS with note** | raw −53.6%, short of the 60% aspiration; see below |
| G7 GPU budget | **N/A** | bake mode not used |
| G8 Hygiene | **PASS** | re-import object/material/bbox match; scripts committed and deterministic; no `.blend1` |

**G6 note.** 53.6% raw is under the 60% aspiration, and the census accounts for the
remainder: after welding and joining, what is left is 6,770 triangles of silhouette and
facade geometry stored at float32, and float32 is a deliberate repo constraint (§4), not
slack. The triangle count did not fall at all in this pass — by design. The two
techniques that would have cut it are quantization (rejected: breaks the runtime merge
path and the stage-2 validator) and the limited dissolve (rejected: 0.4% for a contract
failure, §3). The real win here is structural: 134 draw submeshes → 12.

**Stage-2 re-validation of the shipped file: PASS, 16/16** (`../validation.json`), run
against the optimized GLB after the swap — including
`normals_outward_ray_residual_within_tolerance`, which is the check that caught the
sliver defect in the first place.

## 8. Deliverables

```
optimize/
  input/350-brannan.glb        # untouched archive of the pre-optimize asset
  350-brannan.optimized.glb    # the winner, copied over ../350-brannan.glb
  mid.glb                      # Phase B output, kept for reproduction
  inspect.py optimize.py validate.py render_ab.py diff_ab.py g3check/
  inspect.json phaseb_stats.json validation.json diffs.json
  renders/                     # A/B day+night × near+far, 4 elevations, diffs, contact sheet
  REPORT.md                    # this file
```

Reproduce with:

```bash
B=/Applications/Blender.app/Contents/MacOS/Blender
$B -b --python optimize.py -- input/350-brannan.glb mid.glb phaseb_stats.json
npx gltfpack@0.24 -i mid.glb -o 350-brannan.optimized.glb -c -km -kn -noq
$B -b --python validate.py -- input/350-brannan.glb 350-brannan.optimized.glb validation.json
```
